"""F117.3: a javító bemenet összeállítása — konkordancia/Karoli_versmegfeleltetes_javitas.tsv (DT-F117a–e).

Források (soronként a `proveniencia` oszlopban is):
  * KJV-pár: a kézi ítélet (naplok/F117_itelet.tsv, scope=manual); az Ézs 64:1-nél a DT-F117c (2) szerinti 64:1;
  * igehely_mt: az MT-levezetés (naplok/F117_mt_levezetes.tsv, DT-F117d (c));
  * osztály (DT-F117b, DT-F117e (c)): Károli = KJV = MT -> KJV (üres igehely_mt); Károli = MT ≠ KJV -> MT (igehely_mt =
    Károli-szám); Károli ≠ KJV és ≠ MT -> KEZI kitöltött igehely_mt-vel (új kombináció, DT-F117e);
  * forras: szoveg_osszevetes_f117 (DT-F117b);
  * megjegyzes: a felülírt sor régi értéke (`elozo: kjv|mt|osztaly|forras|megjegyzes`) vagy `potolt: nincs_sor`;
    a DT-F117c döntései; az N-F117c újraellenőrzési jelölése.
A „régi” tábla RÖGZÍTETT: a javítás előtti állapot a 89b30c2e commitból (`git show 89b30c2e:konkordancia/Karoli_versmegfeleltetes.tsv`),
nem a munkafa (már javított) táblája — így a szkript újrafuttatva is ugyanazt a bemenetet adja (F117.8 (3), ELLENOR 3. pont).
Írási őr: ha a cél létezik és a kimenet eltér tőle, `--felulir` nélkül leáll (a kézi bemenetet nem írja felül szó nélkül).
A célhalmaz (346) a naplok/F117_szoveg_osszevetes.tsv nem-kontextus soraiból.
Futtatás: python naplok/F117_javitas_bemenet_general.py [--kimenet FÁJL] [--felulir]   (alap: a repó javító-TSV-je)
TSV split('\\t') / '\\t'.join(), a csv modul nélkül.
"""
import argparse
import os
import subprocess
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = os.path.join(ROOT, 'naplok')
BASE_COMMIT = '89b30c2e'   # a javítás előtti tábla (a #114 utáni main); a "régi" érték innen jön, nem a munkafából
TABLA_GIT = 'konkordancia/Karoli_versmegfeleltetes.tsv'
KIMENET = os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes_javitas.tsv')
TS = '2026-10-18'
FORRAS = 'szoveg_osszevetes_f117'
KJV_DONTES = {'Ézs 64:1': '64:1'}
DONTES_MEGJ = {
    'Ézs 64:1': 'KJV 64:1–2 egy Károli-versben (F91-szabály: az első KJV-vers a pár; DT-F117c (2); a KJV 64:2 visszairánya: N-F117b)',
    '1Kir 22:43': 'KJV 22:43 két Károli-versben (22:43–44; DT-F117c (3) (a))',
    '1Kir 22:44': 'KJV 22:43 két Károli-versben (22:43–44; DT-F117c (3) (a))',
    '1Sám 20:43': 'KJV 20:42 két Károli-versben (20:42–43; DT-F117c (3) (a))',
    'Hós 2:1': 'a csak szöveg-jelű igazítás eltért (DT-F117c (1)); a KJV 2:1 a Károli Hós 1:11-ben (N-F117b)',
    'Jób 17:1': 'a csak szöveg-jelű igazítás eltért (DT-F117c (1)); a KJV 17:1 a Károli Jób 16:22-ben (N-F117b)',
    'Jób 17:2': 'a csak szöveg-jelű igazítás eltért (DT-F117c (1))',
    'Jób 17:3': 'a csak szöveg-jelű igazítás eltért (DT-F117c (1))',
}


def sorok(path):
    with open(path, encoding='utf-8') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if s and not s.startswith('#'):
                yield s.split('\t')


def base_tabla():
    """A javítás előtti tábla sorai a BASE_COMMIT-ból (git show), a munkafától függetlenül."""
    ki = subprocess.run(['git', 'show', '%s:%s' % (BASE_COMMIT, TABLA_GIT)], cwd=ROOT, capture_output=True, check=True)
    for s in ki.stdout.decode('utf-8').split('\n'):
        s = s.rstrip('\r')
        if s and not s.startswith('#'):
            yield s.split('\t')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kimenet', default=KIMENET)
    ap.add_argument('--felulir', action='store_true', help='a létező, eltérő célfájl felülírása')
    a = ap.parse_args()
    cel = {p[0]: p[1] for p in sorok(os.path.join(N, 'F117_szoveg_osszevetes.tsv'))
           if p[0] != 'igehely_karoli' and p[1] != 'kontextus'}
    itelet = {p[0]: (p[1], p[3] if len(p) > 3 else '') for p in sorok(os.path.join(N, 'F117_itelet.tsv'))
              if p[0] != 'igehely_karoli'}
    mt = {p[0]: p[3] for p in sorok(os.path.join(N, 'F117_mt_levezetes.tsv')) if p[0] != 'igehely_karoli'}
    tabla = {}
    for p in base_tabla():
        if p[0] != 'igehely_karoli':
            assert p[0] not in tabla
            tabla[p[0]] = p
    assert len(cel) == 346 and set(cel) == set(itelet) == set(mt)
    ki = []
    stat = Counter()
    for kk in sorted(cel):
        kar = kk.rsplit(' ', 1)[1]
        kjv = KJV_DONTES.get(kk, itelet[kk][0])
        assert ';' not in kjv, kk
        m = mt[kk]
        assert m and ';' not in m, kk
        if kjv == kar and m == kar:
            osz, mt_ertek = 'KJV', ''
        elif m == kar:
            osz, mt_ertek = 'MT', m
        elif kjv == kar:
            raise SystemExit('Károli = KJV ≠ MT: nincs szabálya (DT-F117e): %s' % kk)
        else:
            osz, mt_ertek = 'KEZI', m
        megj = []
        if kk in tabla:
            r = tabla[kk]
            megj.append('elozo: %s' % '|'.join(r[1:6]))
        else:
            megj.append('potolt: nincs_sor')
        if kk in DONTES_MEGJ:
            megj.append(DONTES_MEGJ[kk])
        if osz == 'KEZI':
            megj.append('KEZI + igehely_mt (DT-F117e): Károli ≠ KJV és ≠ MT')
        if itelet[kk][1]:
            megj.append('újraellenőrizendő a teljes KJV-szövegen (N-F117c)')
        megj_s = ' · '.join(megj)
        prov = ('scope=manual (KJV-pár: naplok/F117_itelet.tsv) + gepi (MT: naplok/F117_mt_levezetes.tsv) | osztaly=%s (cel) | '
                'forras=Karoli_1908.tsv+KJV_Strongs_teljes.tsv+TAHOT_kivonat.tsv+Macula_heber_*.tsv | dontes=DT-F117a..e | ts=%s'
                % (cel[kk], TS))
        sor = [kk, kjv, mt_ertek, osz, FORRAS, megj_s, prov]
        assert not any('\t' in x or '\n' in x for x in sor)
        ki.append('\t'.join(sor))
        stat[(cel[kk], osz, 'felulir' if kk in tabla else 'potol')] += 1
    fejlec = [
        '# KÉZI BEMENET (F117, DT-F117a–e): a konkordancia/Karoli_versmegfeleltetes.tsv javító sorai; az alkalmazó: '
        'eszkozok/versmegf_javitas.py (a naplok/KAROLI_KK4_tabla_veglegesit.py az F91 után importálja). Kézzel csak a kézi ítélet '
        '(naplok/F117_itelet.tsv) és a döntések (DONTESEK.md DT-F117a–e) szerint módosítható; összeállítva: naplok/F117_javitas_bemenet_general.py.',
        '# proveniencia: scope=A–D′ (346 Károli-vers; FELADATOK #117) | forras=naplok/F117_itelet.tsv (scope=manual) + '
        'naplok/F117_mt_levezetes.tsv + DONTESEK.md DT-F117a–e | n=346 | ts=%s' % TS,
        '# osztály: KJV = a Károli-, a KJV- és az MT-szám azonos (igehely_mt üres); MT = Károli = MT ≠ KJV (igehely_mt = Károli-szám); '
        'KEZI = Károli ≠ KJV és ≠ MT, kitöltött igehely_mt-vel (új kombináció, DT-F117e)',
        '\t'.join(['igehely_karoli', 'igehely_kjv', 'igehely_mt', 'osztaly', 'forras', 'megjegyzes', 'proveniencia']),
    ]
    tartalom = '\n'.join(fejlec + ki) + '\n'
    if os.path.exists(a.kimenet):
        with open(a.kimenet, encoding='utf-8', newline='') as f:
            meglevo = f.read()
        if meglevo == tartalom:
            print('változatlan: %s (%d sor, bájtra azonos)' % (a.kimenet, len(ki)))
            return
        if not a.felulir:
            raise SystemExit('ŐR: a cél (%s) létezik és eltér a kimenettől; --felulir nélkül nem írom felül' % a.kimenet)
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(tartalom)
    print('írva: %s (%d sor)' % (a.kimenet, len(ki)))
    for k in sorted(stat):
        print('  %s %s %s: %d' % (k + (stat[k],)))
    print('osztály összesen:', dict(Counter(s.split('\t')[3] for s in ki)))


if __name__ == '__main__':
    main()
