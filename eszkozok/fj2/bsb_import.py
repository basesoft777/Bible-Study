#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bsb_import.py -- F16 (FELADATOK #16, N30): a BSB teljes Biblia-merese es importja.

Modszer: azonos az eszkozok/fj2/bsb.py (F06, PR #75) 1Mozes-meresevel:
  - kuszob es definicio az eszkozok/fj2/kuszob.txt-bol (kuszob=95, definicio=tahot_resze_bsb,
    nevezo=tahot_lefedett_versek); a szkript ezt nem modositja;
  - egyezes: a vers forras-Strong-halmaza (TAHOT: H, 9000-es prefixkodok nelkul) resze a
    BSB-halmaznak; nevezo: a forrassal rendelkezo versek;
  - UJ (a 27 ujszovetsegi konyvre): a forras a konkordancia/TAGNT_kivonat.tsv (G-Strongok),
    minden mas azonos. A BSB-oldali Strong-gyujtes (bsb.bsb_vers_strongok) csak H-t gyujt;
    itt a [HG] mintat a konyv nyelvehez szurjuk.
A kuszobot elero konyveket importalja: konkordancia/BSB_Strongs.tsv (a KJV_Strongs_*.tsv
formatumaban: Igehely STEP-alakban, Szosorszam, Strong-szam, Angol szo, Morfologiai kod (ures)).

Hasznalat:  python eszkozok/fj2/bsb_import.py --munka <mappa>   (a mappaban bsb-data-output/ klon)

Kimenet: naplok/F16_bsb_lefedettseg.tsv, konkordancia/BSB_Strongs.tsv.
"""

import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402
import bsb  # noqa: E402

URL = bsb.URL
STRONG_MINTA = {'H': re.compile(r'H0*(\d+)'), 'G': re.compile(r'G0*(\d+)')}
SZURT = {'nem_szamjegy_versszam_kulcs (meres)': 0, 'nem_szamjegy_versszam_kulcs (import)': 0}  # kategoria -> darab: minden, ami a mereshez/importhoz nem kerul be, itt szamolodik


def szur(kat, n=1):
    SZURT[kat] = SZURT.get(kat, 0) + n


FEJLEC_SOR = 'Igehely\tSzósorszám\tStrong-szám\tAngol szó\tMorfológiai kód\n'


def konyvek():
    """[(step_kod, magyar, nyelv)] kanonikus sorrendben: a Konyv_normalizalo_tabla 66 sora."""
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'Konyv_normalizalo_tabla.tsv'))
    ki = []
    for i, s in enumerate(sorok):
        ki.append((s[0], s[1], 'H' if i < 39 else 'G'))
    assert len(ki) == 66, len(ki)
    return ki


def forras_halmazok(nyelv, na28=False):
    """{igehely: set(Strong)}. H: TAHOT (F06 fuggvenye); G: TAGNT (Igehely, Strong-szam, ..., Kritikai kiadas)."""
    if nyelv == 'H':
        return kozos.tahot_strongok()
    ki = {}
    fej, sorok = kozos.tsv_olvas(os.path.join(kozos.KONKORDANCIA, 'TAGNT_kivonat.tsv'))
    for s in sorok:
        if len(s) < 2 or not s[1].startswith('G'):
            continue
        ki.setdefault(s[0], set())
        if na28 and (len(s) < 8 or 'NA28' not in s[7]):
            continue
        n = kozos.strong_szam(s[1])
        if n is not None:
            ki[s[0]].add(n)
    return ki


def tbesg_normalizalo():
    """{Strong-szam(int): fő Strong-szam(int)} a TBESG.txt ' = a Form/Spelling/Meaning of' soraibol
    (a STEPBible kiterjesztett szamai -> a lemma szama). Csak tajekoztato mutatohoz."""
    ki = {}
    with open(os.path.join(kozos.KONKORDANCIA, 'TBESG.txt'), encoding='utf-8') as f:
        for sor in f:
            mezo = sor.split('	')
            if len(mezo) < 3 or not mezo[0].startswith('G'):
                continue
            if re.search(r' = a (Form|Spelling|Meaning) of$', mezo[1]):
                a, b = kozos.strong_szam(mezo[0]), kozos.strong_szam(mezo[2])
                if a is not None and b is not None and a != b:
                    ki[a] = b
    return ki


def vers_strongok(adat, nyelv):
    """Mint bsb.bsb_vers_strongok, de a nyelvnek megfelelo (H vagy G) Strongokat gyujti."""
    minta = STRONG_MINTA[nyelv]
    ki = {}
    for vs, spanok in adat['eng'].items():
        if not str(vs).isdigit():
            szur('nem_szamjegy_versszam_kulcs (meres)')
            continue
        h = set()
        for span in spanok:
            if isinstance(span, (list, tuple)) and len(span) >= 2 and span[1]:
                for m in minta.finditer(json.dumps(span[1])):
                    h.add(int(m.group(1)))
        ki[int(vs)] = h
    return ki


def vers_sorok(adat, step, fej):
    """A BSB import sorai egy fejezetbol: (Igehely, Szosorszam, Strong, Angol szo, Morf).
    Minden kihagyott span kategoriankent szamolva (SZURT)."""
    ki = []
    for v in adat['eng']:
        if not str(v).isdigit():
            szur('nem_szamjegy_versszam_kulcs (import)')
    for vs in sorted(int(v) for v in adat['eng'] if str(v).isdigit()):
        poz = 0
        for span in adat['eng'][str(vs)]:
            if not (isinstance(span, (list, tuple)) and len(span) >= 2):
                szur('hibas_alaku_span')
                continue
            if not span[1]:
                szur('strong_nelkuli_span_szoveggel' if re.search(r'\w', str(span[0])) else 'strong_nelkuli_span_csak_szokoz_irasjel')
                continue
            jel = span[1]
            if not (isinstance(jel, str) and re.fullmatch(r'[HG]\d+[a-z]?', jel)):
                raise ValueError('varatlan Strong-jeloles: %r (%s %s:%s)' % (jel, step, fej, vs))
            poz += 1
            if len(span) > 2 and isinstance(span[2], dict) and span[2].get('elided'):
                szur('elided_span_bent_ures_Angol_szo_jeloles_nelkul')
            ki.append(('%s.%d.%d' % (step, fej, vs), str(poz), jel, span[0], ''))
    return ki


def text_only_sorok(cel, kod, fej):
    """A base/text-only (CC0) fejezetfajl nemures sorainak szama = a BSB versszama (fuggetlen teljessegi ellenorzes)."""
    ut = os.path.join(cel, 'base', 'text-only', '%s_%03d_BSB.txt' % (kod, fej))
    if not os.path.exists(ut):
        szur('nincs_text_only_fajl')
        return 0
    with open(ut, encoding='utf-8') as f:
        return sum(1 for sor in f if sor.strip())


def fut(munka, parancs):
    kuszob, definicio, nevezo = bsb.kuszob_olvas()
    assert definicio == 'tahot_resze_bsb' and nevezo == 'tahot_lefedett_versek'
    cel = os.path.join(munka, 'bsb-data-output')
    commit, hiba = kozos.klonoz(URL, cel)
    if not commit:
        raise SystemExit('HIBA: a BSB nem toltheto le: %s' % hiba)
    halm = {'H': forras_halmazok('H'), 'G': forras_halmazok('G')}
    halm_na28 = forras_halmazok('G', na28=True)
    norm = tbesg_normalizalo()
    kep = lambda halmaz: {norm.get(x, x) for x in halmaz}  # noqa: E731
    mappa = os.path.join(cel, 'base', 'display')
    lefedettseg, import_sorok = [], []
    for step, mag, nyelv in konyvek():
        kod = step.upper()
        bmappa = os.path.join(mappa, kod)
        if not os.path.isdir(bmappa):
            raise SystemExit('HIBA: nincs BSB-mappa: ' + kod)
        fejezetek = sorted(int(m.group(1)) for fn in os.listdir(bmappa)
                           for m in [re.fullmatch(kod + r'(\d+)\.json', fn)] if m)
        forras = halm[nyelv]
        bsb_versek = forras_van = egyezo = egyezo_na28 = egyezo_norm = 0
        text_only_versek = 0
        bsb_ref = set()
        konyv_sorok = []
        for fej in fejezetek:
            with open(os.path.join(bmappa, '%s%d.json' % (kod, fej)), encoding='utf-8') as f:
                adat = json.load(f)
            b = vers_strongok(adat, nyelv)
            text_only_versek += text_only_sorok(cel, kod, fej)
            konyv_sorok += vers_sorok(adat, step, fej)
            for vs in sorted(b):
                bsb_versek += 1
                ref = '%s %d:%d' % (mag, fej, vs)
                bsb_ref.add(ref)
                t = forras.get(ref)
                if t is None:
                    continue
                forras_van += 1
                if t <= b[vs]:
                    egyezo += 1
                if nyelv == 'G' and kep(t) <= kep(b[vs]):
                    egyezo_norm += 1
                if nyelv == 'G' and halm_na28.get(ref, set()) <= b[vs]:
                    egyezo_na28 += 1
        forras_versek = {r for r in forras if r.rsplit(' ', 1)[0] == mag}
        forras_bsb_nelkul = len(forras_versek - bsb_ref)
        szaz = 100.0 * egyezo / forras_van if forras_van else 0.0
        eredmeny = 'ELERI' if szaz >= kuszob else 'NEM_ERI_EL'
        lefedettseg.append((mag, kod, 'heber' if nyelv == 'H' else 'gorog',
                            str(bsb_versek), str(forras_van), str(egyezo),
                            str(bsb_versek - forras_van), str(forras_bsb_nelkul), str(text_only_versek),
                            str(text_only_versek - bsb_versek),
                            '%.2f' % szaz,
                            ('%.2f' % (100.0 * egyezo_na28 / forras_van)) if nyelv == 'G' and forras_van else '',
                            ('%.2f' % (100.0 * egyezo_norm / forras_van)) if nyelv == 'G' and forras_van else '',
                            '%g' % kuszob, eredmeny,
                            str(len(konyv_sorok)) if eredmeny == 'ELERI' else '0'))
        if eredmeny == 'ELERI':
            import_sorok += konyv_sorok
    ered_db = sum(1 for s in lefedettseg if s[14] == 'ELERI')
    fej = kozos.fejlec(URL + ' + konkordancia/TAHOT_kivonat.tsv (OSZ) + konkordancia/TAGNT_kivonat.tsv (USZ)',
                       'BSB commit ' + commit, parancs)
    fej += ['rogzitett kuszob=%g%% definicio=%s nevezo=%s (kuszob.txt, F06-ban meres elott rogzitve); konyvenkenti alkalmazas: FELADATOK D15' % (kuszob, definicio, nevezo),
            'licenc: base/display/ CC0 1.0 (README.md, ATTRIBUTION.md); a CC-BY index-cc-by/ nem importalt',
            'nincs_forras_vers = a BSB-versek szama, amelyekhez a TAHOT/TAGNT-nak nincs sora (nem elteres, nem szamit a nevezobe); forras_vers_nincs_bsb = a forras verseinek szama, amelyek igehelye a BSB-ben nincs meg (verszamozas-elteres jele)',
            'egyezes_na28_szurve: csak USZ; a TAGNT-nak csak a NA28-cimkes soraival szamolt egyezes, ugyanazzal a nevezovel (tajekoztato, nem a kuszob alapja)',
            'egyezes_normalizalt: csak USZ; mindket oldal Strong-szamai a TBESG.txt Form/Spelling/Meaning of soraival a lemma szamara kepezve (%d szam); tajekoztato, nem a kuszob alapja' % len(norm),
            'ELTERES AZ F06-MODSZERTOL: az F06 (bsb.py) csak az 1Mozest merte, TAHOT-tal; a 27 ujszovetsegi konyvre a forras a TAGNT (G-Strongok) -- ez uj, az F06-ban nem mert alkalmazas, a kuszob es az egyezes-definicio valtozatlan',
            'text_only_versek = a base/text-only (CC0) nemures sorai; display_hianyzo_versek = text_only_versek - display-versek: az upstream display-JSON-bol hianyzo versek (masodlagos, fuggetlen ellenorzes)',
            'szurt sorok kategoriankent (MIND A 66 KONYVRE, az importalt es a nem importalt konyvekre egyarant; a nem_szamjegy_versszam_kulcs kulcsok 0 ertekkel is szerepelnek; az elided_span_* nem szurt: az adatsorban bent van, ures Angol szo-val, jeloles nelkul): ' + '; '.join('%s=%d' % kv for kv in sorted(SZURT.items())),
            'konyvek: %d ELERI, %d NEM_ERI_EL; importalt sorok: %d' % (ered_db, 66 - ered_db, len(import_sorok))]
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F16_bsb_lefedettseg.tsv'), fej,
                 ['konyv', 'bsb_kod', 'nyelv', 'versek_bsb', 'forras_lefedett_versek', 'egyezo', 'nincs_forras_vers',
                  'forras_vers_nincs_bsb', 'text_only_versek', 'display_hianyzo_versek', 'egyezes_szazalek', 'egyezes_na28_szurve', 'egyezes_normalizalt', 'kuszob', 'eredmeny', 'importalt_sorok'],
                 lefedettseg)
    # BSB_Strongs.tsv: nagy fajl (a kozos.tsv_ir 1 MB-os korlatja a naplokra vonatkozik); csv nelkul
    ut = os.path.join(kozos.KONKORDANCIA, 'BSB_Strongs.tsv')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(FEJLEC_SOR)
        for s in import_sorok:
            f.write('\t'.join(kozos.tisztit(x) for x in s) + '\n')
    for s in lefedettseg:
        print('\t'.join(s))
    print(fej[-1])


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--munka', required=True, help='mappa, amelyben a bsb-data-output/ klon van (vagy ide klonozodik)')
    a = ap.parse_args()
    fut(a.munka, 'python eszkozok/fj2/bsb_import.py --munka <mappa>')


if __name__ == '__main__':
    main()
