#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tagnt_valtozatok.py -- F176.2: a STEPBible TAGNT szavankenti kiadas-jelolesenek kivonata
-> konkordancia/TAGNT_valtozatok.tsv.

Bemenet (CLI):  --be <konyvtar>  a ket nyers TAGNT-fajl (TAGNT_Mat-Jhn.txt, TAGNT_Act-Rev.txt), a repon kivul
                --commit <sha>   a STEPBible-Data commit, amibol a fajlok valok (a fejlecbe)
Kimenet: konkordancia/TAGNT_valtozatok.tsv

Egy sor = egy olyan TAGNT-szo, amelynel a kiadas-jelolo nem a teljes NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz halmaz
VAGY a szo-tipus nem NKO (azaz van szovegvaltozat-vonatkozasa). A THGNT (Tyndale House GNT, `Tyn`) SZOVEGE nem kerul
at: csak az, hogy a szo mely kiadasokban all (`kiadasok`); a `Meaning variants` es a `Spelling variants` oszlop
(amelyek Tyn-alakot is hordoznak) nincs a kimenetben, csak a `jelentesvaltozat` igen/nem jelzese. Ha egy szo CSAK a
Tyn-ben all, a `gorog` mezo ures (a szoveg THGNT-eredetu lenne).
A versszamozas a forras (NRSV-) szamozasa: az `igehely` a magyar konyvrovidites + a forras elsodleges fejezet:verse,
a `forras_ref` valtozatlanul tartalmazza a forras hivatkozasat (zarojeles alternativaval egyutt); a Karoli-kulcs
eldontese (F22/F90) tartalmi dontes, itt NEM tortenik; a `karoli_kulcs` csak letezest jelez.
Futtatas:  python -I eszkozok/visszhang/tagnt_valtozatok.py --be <letoltes/tagnt> --commit <sha>
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos as K  # noqa: E402

RX = re.compile(r'^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)(?:([\[({])(\d+)\.(\d+)[\])}])?#(\d+)=(\S+)\t')
TELJES = ['NA28', 'NA27', 'Tyn', 'SBL', 'WH', 'Treg', 'TR', 'Byz']
JEL = {'[': 'kjv', '{': 'egyeb', '(': 'na'}
FAJLOK = ['TAGNT_Mat-Jhn.txt', 'TAGNT_Act-Rev.txt']


def fut(be, commit, ki):
    magyar, sorrend = K.normalizalo()
    karoli = K.karoli_kulcsok()
    sorok, osszes, nyers_sha = [], 0, []
    tyn_csak = 0
    for fn in FAJLOK:
        ut = os.path.join(be, fn)
        nyers_sha.append('%s=%s' % (fn, K.sha256_fajl(ut)))
        for line in open(ut, encoding='utf-8-sig'):
            m = RX.match(line)
            if not m:
                continue
            osszes += 1
            c = line.rstrip('\n').split('\t')
            c += [''] * (13 - len(c))
            szerk = c[5].strip()
            tip = m.group(8)
            lista = [e for e in szerk.split('+') if e]
            nevek = [re.sub(r'[»«]\d+$', '', e) for e in lista]
            if tip == 'NKO' and szerk == '+'.join(TELJES):
                continue            # teljes halmaz, NKO: nincs valtozat-vonatkozas
            step = m.group(1)
            # a STEP-kod (Mat, 1Co ...) a normalizalo tabla elso oszlopa
            if step not in magyar:
                raise SystemExit('ismeretlen konyvkod: %s' % step)
            fej, v = int(m.group(2)), int(m.group(3))
            kulcs = '%s %d:%d' % (magyar[step], fej, v)
            ref = line.split('\t')[0].split('#')[0]
            szamozas = JEL.get(m.group(4), 'nrsv')
            gorog = c[1].strip()
            gorog = re.sub(r'\s*\(.*$', '', gorog)
            if set(nevek) <= {'Tyn'}:
                gorog = ''
                tyn_csak += 1
            hianyzik = [e for e in TELJES if e not in nevek]
            mozg = ' '.join(e for e in lista if re.search(r'[»«]\d+$', e))
            strong = re.sub(r'_[A-Za-z]$', '', c[11].strip())
            sorok.append([(sorrend.index(step), fej, v, int(m.group(7)), len(sorok)), kulcs, ref, szamozas, '#' + m.group(7), tip,
                          strong, gorog, szerk, ' '.join(hianyzik), mozg,
                          'igen' if c[6].strip() else 'nem', 'igen' if kulcs in karoli else 'nem'])
    sorok.sort(key=lambda r: r[0])
    sorok = [r[1:] for r in sorok]
    fejlec = [
        'GENERÁLT: eszkozok/visszhang/tagnt_valtozatok.py (F176.2); kézzel nem szerkeszthető.',
        'forras=github.com/STEPBible/STEPBible-Data @ %s, "Translators Amalgamated OT+NT/TAGNT Mat-Jhn" és "TAGNT Act-Rev" (CC-BY.txt) | sha256: %s | ts=%s' % (commit, '; '.join(nyers_sha), K.ts()),
        'licenc: CC BY 4.0 (a nyers fájlok fejléce: "Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0)"); kötelező megjelölés: Tyndale House és STEPBible.org, hivatkozás: STEPBible.github.io/STEPBible-Data',
        'egy sor = egy TAGNT-szó, amelynél a kiadás-jelölő nem a teljes NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz halmaz, vagy a tipus nem NKO. A THGNT (Tyn) szövege nem került át, csak a jelölés; a Meaning/Spelling variants oszlop nincs benne.',
        'összes TAGNT-szó: %d; a kimenetben: %d; csak-Tyn szó (görög mező üres): %d' % (osszes, len(sorok), tyn_csak),
        'igehely = magyar könyvrövidítés + a FORRÁS (NRSV) elsődleges fejezet:verse; szamozas: nrsv | kjv ([..]) | egyeb ({..}) | na ((..)) a forrás zárójel-jelölése szerint; forras_ref szó szerint. NEM Károli-átszámozás.',
    ]
    ok = ['igehely', 'forras_ref', 'szamozas', 'szo_sorszam', 'tipus', 'strong', 'gorog', 'kiadasok', 'hianyzik_ebbol',
          'mozgatas', 'jelentesvaltozat', 'karoli_kulcs']
    K.ir_tsv(ki, fejlec, ok, sorok)
    print('osszes szo: %d; kimeneti sor: %d; csak-Tyn: %d; karoli_kulcs=nem: %d' % (
        osszes, len(sorok), tyn_csak, sum(1 for s in sorok if s[-1] == 'nem')))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--be', required=True)
    ap.add_argument('--commit', required=True)
    ap.add_argument('--ki', default=os.path.join(K.GYOKER, 'konkordancia', 'TAGNT_valtozatok.tsv'))
    a = ap.parse_args()
    fut(a.be, a.commit, a.ki)
