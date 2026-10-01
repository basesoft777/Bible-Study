"""f08_bemenet.py -- F08.1: a 87 fuggo LXX-hely bemenetenek osszegyujtese.

Soronkent (naplok/F17_87_hely.tsv) harom forras egymas mellett:
  - Macula_heber: a KK szerinti Karoli-vers osszes heber szava a Macula
    szo-szintu gorog illesztesevel (gorog_lxx, gorog_strong);
  - LXX_OS: a Karoli-vershez kotott LXX-vers szavai (szoalak, lemma, Strong);
  - az FJ1 gepi jeloltje (naplok/FORRAS_FJ1_lxx_jeloltek.tsv) -- NEM fuggetlen
    forras, a Macula XML-bol szarmazik (naplok/FORRAS_FJ1_mtlxx_macula.md).

Kimenet: naplok/F08_bemenet.txt (munkaanyag a kutatoi donteshez; nem adattabla).
Futtatas: python eszkozok/f08/f08_bemenet.py
"""
import glob
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def tsv(path):
    with io.open(path, encoding='utf-8', newline='') as f:
        sorok = [s for s in f.read().split('\n') if s and not s.startswith('#')]
    sorok = [s.rstrip('\r') for s in sorok]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def main():
    f17 = tsv(os.path.join(GYOKER, 'naplok', 'F17_87_hely.tsv'))
    fj1 = tsv(os.path.join(GYOKER, 'naplok', 'FORRAS_FJ1_lxx_jeloltek.tsv'))
    celok = {r['igehely_karoli'] for r in f17}

    macula = {}
    for p in sorted(glob.glob(os.path.join(GYOKER, 'konkordancia', 'Macula_heber_*.tsv'))):
        for r in tsv(p):
            for k in (r.get('karoli') or '').split(';'):
                k = k.strip()
                if k in celok:
                    macula.setdefault(k, []).append(r)

    lxx = {}
    for p in sorted(glob.glob(os.path.join(GYOKER, 'konkordancia', 'LXX_OS', '*.tsv'))):
        for r in tsv(p):
            k = (r.get('igehely_karoli') or '').strip()
            if k in celok:
                lxx.setdefault(k, []).append(r)

    ki = []
    for i, r in enumerate(f17, 1):
        hely = r['igehely_karoli']
        j = fj1[i - 1] if i - 1 < len(fj1) else {}
        ki.append('=== %02d %s | %s | MT %s (%s) | kulcs: %s %s | F17: %s / %s %s | FJ1: %s %s %s' % (
            i, r['motivum'], hely, r['igehely_mt'], r['kk_mod'], r['heber_kulcsszo'],
            r['heber_strong_munkalap'], r['allapot'], r['macula_gorog'], r['macula_gorog_strong'],
            j.get('javasolt_gorog_lemma', ''), j.get('javasolt_gorog_strong', ''), j.get('allapot', '')))
        mw = macula.get(hely, [])
        ki.append('  HEB (%d, ref %s): %s' % (len(mw), mw[0]['ref'].split('!')[0] if mw else '-', ' '.join(
            '%s[%s>%s%s]' % (w['szo'], w['strong'] or w['strong_x'], w['gorog_lxx'] or '0',
                             (':' + w['gorog_strong']) if w['gorog_strong'] else '')
            for w in mw)))
        lw = lxx.get(hely, [])
        ki.append('  LXX (%d, %s): %s' % (len(lw), lw[0]['igehely_lxx'] if lw else '-', ' '.join(
            '%s(%s,%s)' % (w['szoalak'], w['lemma'], w['strong'] or '-') for w in lw)))
    with io.open(os.path.join(GYOKER, 'naplok', 'F08_bemenet.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/f08/f08_bemenet.py — kézzel nem szerkesztendő.\n')
        f.write('# proveniencia: scope=87 fuggo LXX-hely (naplok/F17_87_hely.tsv) | forras=konkordancia/Macula_heber_*.tsv (macula-hebrew@47db250b) + konkordancia/LXX_OS/*.tsv (lxx-morph@c91f6b1e) + naplok/FORRAS_FJ1_lxx_jeloltek.tsv | ts=2026-09-30\n')
        f.write('\n'.join(ki) + '\n')
    print('sorok=%d, macula-vers=%d, lxx-vers=%d' % (len(f17), len(macula), len(lxx)))


if __name__ == '__main__':
    main()
