"""F105 (FELADATOK #105) ⛔: vak mintafájl a két független kitöltőnek (az 50-es minta, seed 105).

Bemenet: a `naplok/F105_meres.py` futamtáblája (`F105_futamok.tsv`, a `--be` könyvtárban); a kiválasztás a
`naplok/F105_minta.py`-é (ugyanaz az 50 tétel, ugyanabban a sorrendben).
Kimenet a `--ki` könyvtárba (a repón KÍVÜL; a fájlokat nem commitoljuk):
  - `vak_minta.md`: tételenként sorszám, a hivatkozott vers Károli-kulcsa, a vers héber szövege a TAHOT-ból (a `Ragozott alak`
    mezők a Károli-kulcson, szóközzel; a TAHOT morfémánként tagol), és két sorrend „A” és „B” címkével. Nincs benne a gépi
    döntés, a DT445-állapot, a Strong-szám, a nyers forrásalak, és semmi, ami megmondja, melyik a forrás.
  - `kulcs.tsv`: sorszám, és melyik betű (A/B) a helyreállított alak.
Az A/B hozzárendelés tételenként rögzített seeddel (`random.Random(105000 + sorszám)`) véletlenszerű.
A két alakon ugyanaz a megjelenítési normalizálás fut, hogy a forma ne árulja el a forrást: (1) a rafe-maqqéf feloldása
(`F105_minta.maqqef`); (2) a geres egységesítése: minden szóban (szóköz és maqqéf között) a geres a szó végére kerül
(módszertani döntés, 2026-11-10: a forrás `׳X` alakja helyesírási hiba volna, és a vers nélkül is elárulná a forrást; a
kérdés csak a szavak sorrendje). A fájl elején ez jelölve áll.

Futtatás: python naplok/F105_vak.py --be <könyvtár> --ki <könyvtár a repón kívül>
"""
import argparse
import os
import random
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

NAPLOK = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(NAPLOK)
sys.path.insert(0, NAPLOK)
import F105_minta as FM  # noqa: E402

TAHOT = os.path.join(REPO, 'konkordancia', 'TAHOT_kivonat.tsv')
GERES = '׳'
JELOLES = 'a geres helye mindkét alakban egységesítve; a kérdés csak a szavak sorrendje'


def kivalasztas(be):
    """Ugyanaz az 50 tétel, mint az `F105_minta.py`-ban (seed 105)."""
    futam = FM.tsv(os.path.join(be, 'F105_futamok.tsv'))
    jelolt = [d for d in futam if d['itelet'] == 'F0_M0_R1' and d['dt445'] in ('jelolt_marad', 'nincs_sor', 'reszleges')]
    rnd = random.Random(105)
    return sorted(rnd.sample(jelolt, 50), key=lambda d: (d['strong'], int(d['poz'])))


def geres_vegre(szo):
    """A szóban álló geres a szó végére (egy darab)."""
    return szo.replace(GERES, '') + GERES if GERES in szo else szo


def _token(t):
    """Egy (szóközzel határolt) token maqqéffel tagolt részei; a csak geresből álló rész (pl. a rafe feloldása után
    `׳־צ…`) geresét az előző rész kapja, ha nincs előző, a következő; utána minden részben a geres a végére kerül."""
    reszek = FM.maqqef(t).split('־')
    tiszta, plusz = [], [False] * len(reszek)
    for i, r in enumerate(reszek):
        if r and not r.replace(GERES, ''):
            j = i - 1 if i else i + 1
            if 0 <= j < len(reszek):
                plusz[j] = True
            continue
        tiszta.append(i)
    return '־'.join(geres_vegre(reszek[i] + (GERES if plusz[i] else '')) for i in tiszta)


def alak(futam):
    return ' '.join(_token(t) for t in futam.split(' '))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--be', required=True)
    ap.add_argument('--ki', required=True)
    a = ap.parse_args()
    ki = os.path.abspath(a.ki)
    if os.path.commonpath([ki, REPO]) == REPO:
        sys.exit('A kimenet a repón kívülre menjen: %s' % ki)
    os.makedirs(ki, exist_ok=True)
    minta = kivalasztas(a.be)
    kell = {d['karoli_vers'] for d in minta}
    vers = {}
    for d in FM.tsv(TAHOT):
        if d['Igehely'] in kell:
            vers.setdefault(d['Igehely'], []).append(d.get('Ragozott alak', '').strip())
    md = ['# Vak minta: a BDB héber idézeteinek szórendje (50 tétel)', '',
          '**Jelölés: %s.**' % JELOLES, '',
          'Tételenként: a hivatkozott vers (Károli-kulcs), a vers héber szövege (TAHOT; a TAHOT morfémánként tagol, ezért '
          'egyes előtagok és végződések külön állnak), és ugyanannak a BDB-idézetnek két sorrendje, A és B. '
          'Kérdés: melyik sorrend egyezik a vers szövegével (illetve a nyomtatott BDB-vel)? '
          'Válasz tételenként: A / B / nem tudom.', '']
    kulcs = ['sorszam\thelyreallitott']
    for i, d in enumerate(minta, 1):
        hely, forr = alak(d['r_hib']), alak(d['forras'])
        a_hely = random.Random(105000 + i).random() < 0.5
        A, B = (hely, forr) if a_hely else (forr, hely)
        md += ['## %d.' % i, '',
               '- vers: %s' % d['karoli_vers'],
               '- a vers héber szövege: %s' % ' '.join(m for m in vers.get(d['karoli_vers'], []) if m),
               '- A: %s' % A,
               '- B: %s' % B,
               '- válasz: ', '']
        kulcs.append('%d\t%s' % (i, 'A' if a_hely else 'B'))
    with open(os.path.join(ki, 'vak_minta.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(md))
    with open(os.path.join(ki, 'kulcs.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(kulcs) + '\n')
    hibas = sum(1 for s in md if s.startswith(('- A: ', '- B: ')) and re.search(r'(^|[\s־])' + GERES, s[5:]))
    print('geres szó elején:', hibas)
    print('tétel:', len(minta), '| A = helyreállított:', sum(1 for s in kulcs[1:] if s.endswith('A')))


if __name__ == '__main__':
    main()
