#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
vulgata_import.py -- F176.2: az eBible `latVUC` (Clementina) USFM-csomagjanak konverzioja
konkordancia/Vulgata_Clementina.tsv-be.

Bemenet (CLI):  --zip <latVUC_usfm.zip>   a letoltott csomag (a repon kivul; a szkript zipfile-lal olvas, nem bont ki)
Kimenet: konkordancia/Vulgata_Clementina.tsv

Szabalyok:
  * csak a 66 kanonikus konyv (a Konyv_normalizalo_tabla.tsv szerint); a deuterokanonikus konyvek (TOB, JDT, WIS,
    SIR, BAR, 1MA, 2MA) kimaradnak, szamuk a fejlecben.
  * a Glossa Ordinaria lábjegyzetek (`\\f ... \\f*`) NEM kerulnek at: csak a vers szovege (a csomag leirasa szerint
    a Glossa Migne 1880-as kiadasabol van; ez kulon, recepcios forras, nem ebben a tablaban).
  * a versszamozas a forras (Vulgata-) sajat szamozasa: az `igehely` a magyar konyvrovidites + a forras fejezet:verse,
    nem Karoli-atszamozas (a zsoltarok Vulgata-szamozasa elter); a `forras_vers` USFM-kod + forras fejezet:verse;
    a `forras_kulcs` csak azt jelzi, letezik-e az igehely-kulcs a Karoli_1908.tsv-ben.
Futtatas:  python -I eszkozok/visszhang/vulgata_import.py --zip <latVUC_usfm.zip>
"""
import argparse
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos as K  # noqa: E402

BS = chr(92)
RE_FN = re.compile(re.escape(BS) + r'f ' + r'.*?' + re.escape(BS) + r'f\*', re.S)
RE_C = re.compile(re.escape(BS) + r'c ([0-9]+)')
RE_V = re.compile(re.escape(BS) + r'v ([0-9]+)(?:-([0-9]+))?[ \t]*')
RE_MARK = re.compile(re.escape(BS) + r'[a-z]+[0-9]*\*?')
FAJL_RX = re.compile(r'^[0-9]+-([0-9A-Z]{3})latVUC\.usfm$')


def konyv_versek(usfm):
    """-> ([(fejezet, vers, vers_vege, szoveg)], labjegyzetszam)"""
    lj = len(RE_FN.findall(usfm))
    t = RE_FN.sub('', usfm)
    # a fejezet-hatarokon vagunk: \c N ... \v ...
    ki = []
    fej = 0
    jelek = sorted([(m.start(), 'c', m) for m in RE_C.finditer(t)] + [(m.start(), 'v', m) for m in RE_V.finditer(t)])
    for i, (pos, tip, m) in enumerate(jelek):
        if tip == 'c':
            fej = int(m.group(1))
            continue
        veg = jelek[i + 1][0] if i + 1 < len(jelek) else len(t)
        nyers = t[m.end():veg]
        nyers = RE_MARK.sub(' ', nyers)
        nyers = re.sub(r'\s+', ' ', nyers).strip()
        ki.append((fej, int(m.group(1)), int(m.group(2)) if m.group(2) else 0, nyers))
    return ki, lj


def fut(zippath, ki):
    magyar, sorrend = K.normalizalo()
    karoli = K.karoli_kulcsok()
    z = zipfile.ZipFile(zippath)
    fajlok = {}
    for n in z.namelist():
        m = FAJL_RX.match(n)
        if m:
            fajlok[m.group(1)] = n
    sorok, kimaradt, labj, ures, tartomany = [], [], 0, 0, 0
    for step in sorrend:
        usfm = step.upper()
        if usfm not in fajlok:
            raise SystemExit('hianyzo USFM-fajl: %s' % usfm)
        versek, lj = konyv_versek(z.read(fajlok[usfm]).decode('utf-8-sig'))
        labj += lj
        for fej, v, veg, sz in versek:
            if not sz:
                ures += 1
                continue
            if veg:
                tartomany += 1
            kulcs = '%s %d:%d' % (magyar[step], fej, v)
            fv = '%s %d:%d%s' % (usfm, fej, v, ('-%d' % veg) if veg else '')
            sorok.append([kulcs, fv, 'igen' if kulcs in karoli else 'nem', sz])
    ismert = {step.upper() for step in sorrend}
    kimaradt = sorted(k for k in fajlok if k not in ismert)
    fejlec = [
        'GENERÁLT: eszkozok/visszhang/vulgata_import.py (F176.2); kézzel nem szerkeszthető.',
        'forras=https://ebible.org/Scriptures/latVUC_usfm.zip (Bibbia Vulgata Clementina na 1598; "Clementine Vulgate of 1598 with Glossa Ordinaria Migne edition 1880 in Latin"), sha256=%s | ts=%s' % (K.sha256_fajl(zippath), K.ts()),
        'kiadás (az eBible saját megjelölése szerint): Clementina 1598; a Glossa Ordinaria lábjegyzeteit (%d db) NEM vettük át; kimaradt deuterokanonikus könyvek: %s' % (labj, ' '.join(kimaradt)),
        'igehely = magyar könyvrövidítés + a FORRÁS (Vulgata-) fejezet:verse; NEM Károli-átszámozás (a zsoltárok és egyes könyvek számozása eltér). forras_kulcs: az igehely-kulcs létezik-e a Karoli_1908.tsv-ben (jelzés, nem feloldás; versegyezést nem állít, a Károli-feloldás nézetoldali; l. VISSZHANG_README.md 1.).',
        'üres vers (kihagyva): %d; versszám-tartomány (\\v a-b, a kulcs az első szám): %d' % (ures, tartomany),
    ]
    K.ir_tsv(ki, fejlec, ['igehely', 'forras_vers', 'forras_kulcs', 'szoveg'], sorok)
    print('sorok: %d; labjegyzet (nem atvett): %d; kimaradt konyv: %s; ures: %d; tartomany: %d; forras_kulcs=nem: %d' % (
        len(sorok), labj, ' '.join(kimaradt), ures, tartomany, sum(1 for s in sorok if s[2] == 'nem')))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--zip', required=True)
    ap.add_argument('--ki', default=os.path.join(K.GYOKER, 'konkordancia', 'Vulgata_Clementina.tsv'))
    a = ap.parse_args()
    fut(a.zip, a.ki)
