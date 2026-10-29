"""F146.2 (DT-F146b): a Jóel 26 sorának felvétele a javító bemenetbe — konkordancia/Karoli_versmegfeleltetes_javitas.tsv.

Halmaz (DT-F146b, a felhasználó döntése): a naplok/F146_mt_felmeres.tsv `Jóel` + `elteres` sorai (Károli 2:28–3:21 → MT 3:1–4:21).
Sor: igehely_kjv = a tábla KJV-párja (= Károli-szám); igehely_mt = a mért MT-vers; osztaly = KEZI; forras = macula_mt_f146;
megjegyzes = a felülírt sor régi értéke (`elozo: kjv|mt|osztaly|forras|megjegyzes`) + a mérés; proveniencia soronként.
A „régi” tábla RÖGZÍTETT: a 0a245b4e commit (a #146 előtti main) táblája, így az újrafuttatás ugyanazt adja.
Őr: a bemenet meglévő sorai (fejléc és adat) bájtra változatlanok; pontosan 26 új adatsor és 1 új fejléc-jegyzet;
a cél már a kimenet → „változatlan”, nem ír. Futtatás: python naplok/F146_javitas_bemenet.py [--kimenet FÁJL]
TSV split('\\t') / '\\t'.join(), a csv modul nélkül.
"""
import argparse
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JAVITAS = os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes_javitas.tsv')
FELMERES = os.path.join(ROOT, 'naplok', 'F146_mt_felmeres.tsv')
BASE = '0a245b4e'
FORRAS = 'macula_mt_f146'
TS = '2026-10-28'
N = 26
JEGYZET = ('# F146 (DT-F146b): + %d sor, a Jóel Károli 2:28–3:21 → MT 3:1–4:21 (osztaly=KEZI kitöltött igehely_mt-vel, Károli = KJV ≠ MT); '
           'proveniencia: scope=gepi:Jóel 2–4 | forras=naplok/F146_mt_felmeres.tsv (TAHOT_kivonat.tsv + Macula_heber_Joel.tsv ref) + '
           'naplok/F146_joel_kjv_tanu.py (KJV-tanú, 26/26) + DONTESEK.md DT-F146b | ts=%s' % (N, TS))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kimenet', default=JAVITAS)
    a = ap.parse_args()
    regi_tabla = subprocess.run(['git', 'show', '%s:konkordancia/Karoli_versmegfeleltetes.tsv' % BASE], cwd=ROOT,
                                capture_output=True, check=True).stdout.decode('utf-8').split('\n')
    tabla = {}
    for s in regi_tabla:
        if s and not s.startswith('#'):
            p = s.split('\t')
            tabla[p[0]] = p
    uj = {}
    with open(FELMERES, encoding='utf-8') as f:
        for s in f:
            p = s.rstrip('\n').split('\t')
            if s.startswith('#') or p[0] != 'Jóel' or p[11] != 'elteres':
                continue
            kk, kjv, mt, ja = p[3], p[5], p[6], p[9]
            r = tabla[kk]
            assert r[3] == 'KJV' and r[2] == '' and r[1] == kjv, kk
            uj[kk] = '\t'.join([
                kk, kjv, mt, 'KEZI', FORRAS,
                'elozo: %s · mért MT %s (J=%s, 1-1, a két igazítás egyezik; KJV-tanú: naplok/F146_joel_kjv_tanu.py)' % ('|'.join(r[1:6]), mt, ja),
                'scope=gepi:%s (blokk: Károli c-1..c+1 ↔ MT c-2..c+2) | forras=TAHOT_kivonat.tsv+Macula_heber_Joel.tsv(ref)+KJV_Strongs_teljes.tsv '
                '| eszkoz=naplok/F146_mt_felmeres.py | dontes=DT-F146b | ts=%s' % (kk.rsplit(':', 1)[0], TS)])
    assert len(uj) == N, len(uj)

    with open(JAVITAS, encoding='utf-8', newline='') as f:
        be = f.read().split('\n')
    if be and be[-1] == '':
        be = be[:-1]
    fej = [s for s in be if s.startswith('#') and not s.startswith('# F146 (')]
    oszlop = [s for s in be if not s.startswith('#')][0]
    adat = {s.split('\t')[0]: s for s in be if not s.startswith('#') and s != oszlop}
    for k, v in adat.items():
        if k in uj:
            assert v == uj[k], 'eltérő meglévő F146-sor: %s' % k
    meglevo = {k: v for k, v in adat.items() if k not in uj}
    assert not (set(meglevo) & set(uj))
    ki_adat = dict(meglevo)
    ki_adat.update(uj)
    ki = fej + [JEGYZET, oszlop] + [ki_adat[k] for k in sorted(ki_adat)]

    # őr: a meglévő (nem-F146) sorok bájtra változatlanok, sorrendjük is; pontosan N új sor
    regi_nem146 = [s for s in be if not s.startswith('# F146 (') and s.split('\t')[0] not in uj]
    uj_nem146 = [s for s in ki if not s.startswith('# F146 (') and s.split('\t')[0] not in uj]
    assert regi_nem146 == uj_nem146, 'a meglévő sorok változtak'
    assert len(ki) == len(regi_nem146) + N + 1

    tartalom = '\n'.join(ki) + '\n'
    if os.path.exists(a.kimenet):
        with open(a.kimenet, encoding='utf-8', newline='') as f:
            if f.read() == tartalom:
                print('változatlan: %s (%d sor)' % (a.kimenet, len(ki)))
                return
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(tartalom)
    print('írva: %s (%d sor; ebből %d F146-sor; a meglévő %d sor bájtra változatlan)' % (a.kimenet, len(ki), N, len(regi_nem146)))


if __name__ == '__main__':
    main()
