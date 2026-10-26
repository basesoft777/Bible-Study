#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.3 — a modernizált Károli-réteg kiadott táblái (DT128, DT-F96b, DT-F96f, DT-F96o).

A .2 kimenetére épül: a .1 + .2 lépcsőt az `igealak.py` függvényeivel újraszámolja, és összeveti a kiadott
`adat/karoli_modern/helyesiras_tokenek.tsv`-vel és `adat/karoli_modern/igealak_tokenek.tsv`-vel; eltérésnél
megáll, és nem ír. Determinisztikus, API, LLM és Hunspell nélkül (az LLM-jelöltek a .2 tábláiból jönnek).

Ír (generált, kézzel nem szerkeszthető; a javítás a szabályban vagy a kivételtáblában):
  adat/karoli_modern/karoli_modern.tsv         token-soronként a teljes Károli 1908 (599 367 token): vers-kulcs,
                                               tokenizal-sorszám, 1908-as alak, modern alak, kieső-jelölés és
                                               a kieső token gazdaszava (DT-F96o); Strong-oszlop nincs (DT-F96f)
  adat/karoli_modern/karoli_modern_versek.tsv  versenként a modern szöveg (31 158 vers)

Ellenőrzések (eltérésnél megáll):
  K2   a modern versszöveg újratokenizálva pontosan a nem kieső tokenek modern alakjait adja (igealak.py)
  K3   minden tokensor az 1908-as token vers-kulcsán és tokenizal-sorszámán áll; a tokenek száma versenként
       az 1908-as tokenizálásé
  K3b  (DT-F96o) a #22 párosítás (adat/karoli_strong/szavak_*.tsv) minden Strongos magyar tokenjének kulcsa
       szerepel a táblában, ugyanazzal az 1908-as alakkal; a Strong így token-kulcson illeszthető, és nem változik

Használat:
    python eszkozok/karoli_modern/karoli_modern.py
    python eszkozok/karoli_modern/karoli_modern.py --kimenet <könyvtár>   (próba a repón kívülre)
"""

import argparse
import collections
import datetime
import glob
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_modern'))
import tokenek  # noqa: E402
import igealak  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KI_DIR = igealak.KI_DIR
I_TOKENEK = os.path.join(KI_DIR, 'igealak_tokenek.tsv')
STRONG_SZAVAK = os.path.join('adat', 'karoli_strong', 'szavak_*.tsv')
SZKRIPT = 'eszkozok/karoli_modern/karoli_modern.py'
BEMENETEK = [igealak.KAROLI, igealak.SZOTARI, igealak.H_TOKENEK, I_TOKENEK, igealak.LLM_TABLA, igealak.LLM2_TABLA,
             igealak.KOR3_TABLA, igealak.KOR4_TABLA, igealak.KOR5_TABLA, 'eszkozok/karoli_strong/tokenek.py', 'eszkozok/karoli_modern/fedettseg.py',
             'eszkozok/karoli_modern/helyesiras.py', igealak.SZKRIPT, igealak.MODUL, SZKRIPT]


def sha(ut):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, ut), 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def tabla_sorok(ut):
    ki = []
    with open(os.path.join(ROOT, ut), encoding='utf-8') as f:
        for l in f:
            if l.startswith('#'):
                continue
            ki.append(l.rstrip('\n').split('\t'))
    return ki[0], ki[1:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kimenet', default=None, help='próba-kimenet könyvtára (a repón kívül)')
    a = ap.parse_args()
    ki_dir = a.kimenet or os.path.join(ROOT, KI_DIR)
    tabla, versek, gy, kis_szavak, alakszotar, dont, alakok = igealak.elokeszit()
    fd = igealak.Feldolgozo(alakok, alakszotar, dont, igealak.llm_beolvas())

    h_vart = set(igealak.h_tokenek_beolvas())
    h_kapott = set()
    _, i_sorok = tabla_sorok(I_TOKENEK)
    i_vart = {(r[0], r[1]): r for r in i_sorok}
    tok_ki, vers_ki = [], []
    i_egyezik = 0
    for igehely, sz in versek:
        t, modern = fd.vers(igehely, sz)  # a K2-t a vers() maga ellenőrzi, eltérésnél megáll
        if [r[1] for r in t] != tokenek.tokenizal(sz):
            raise SystemExit('K3 hiba (tokenszám vagy sorrend): %s' % igehely)
        for r in t:
            if r[1] != r[2] or r[4] == 'osszevonva' or r[7]:
                h_kapott.add((igehely, str(r[0]), r[1], r[2] if r[4] != 'osszevonva' else '',
                              'osszevonva' if r[4] == 'osszevonva' else '', r[5], r[7]))
            gazda = str(r[0] + 1) if r[4] == 'osszevonva' else (str(r[0] - 1) if r[4] == 'segedige' else '')
            szabaly = igealak.cimke(r[5], r[6]) if r[5] and r[6] else (r[5] or r[6])
            bizonytalan = igealak.cimke(r[7], r[8]) if r[7] and r[8] else (r[7] or r[8])
            k = (igehely, str(r[0]))
            if k in i_vart:
                v = i_vart[k]
                if (v[2], v[4], v[5], v[6], v[7]) != (r[1], r[3], r[4], szabaly, bizonytalan):
                    raise SystemExit('a .2 kimenetétől eltér: %s %s' % k)
                i_egyezik += 1
            elif r[1] != r[3] or r[4] or r[7] or r[8] or r[9]:
                raise SystemExit('a .2 kimenetéből hiányzik: %s %s' % k)
            tok_ki.append([igehely, str(r[0]), r[1], r[3], r[4], gazda, szabaly, bizonytalan])
        vers_ki.append([igehely, modern, 'igen' if modern != sz else 'nem'])
    if h_kapott != h_vart:
        raise SystemExit('a .1 újraszámolása eltér a %s-től' % igealak.H_TOKENEK)
    if i_egyezik != len(i_vart):
        raise SystemExit('a .2 kimenetének %d sora nem került elő' % (len(i_vart) - i_egyezik))
    print('a .1 és a .2 újraszámolva: egyezik (%d + %d sor); K2, K3 minden versen átment'
          % (len(h_vart), len(i_vart)))

    # K3b (DT-F96o): a #22 Strongos tokenjeinek kulcs-lefedettsége
    kulcs = {(r[0], r[1]): r[2] for r in tok_ki}
    strongos = hiany = alak_elter = 0
    konyvek = 0
    kieso_strong = collections.Counter()
    tok_index = {(r[0], r[1]): r for r in tok_ki}
    for ut in sorted(glob.glob(os.path.join(ROOT, STRONG_SZAVAK))):
        konyvek += 1
        with open(ut, encoding='utf-8') as f:
            fej = None
            for l in f:
                if l.startswith('#'):
                    continue
                m = l.rstrip('\n').split('\t')
                if fej is None:
                    fej = m
                    continue
                d = dict(zip(fej, m))
                if d.get('oldal') != 'hu' or not d.get('strong'):
                    continue
                strongos += 1
                k = (d['vers'], d['sorszam'])
                if k not in kulcs:
                    hiany += 1
                    if hiany <= 5:
                        print('K3b: hiányzó kulcs %s %s (%s)' % (k[0], k[1], d['szo']))
                elif kulcs[k] != d['szo']:
                    alak_elter += 1
                    if alak_elter <= 5:
                        print('K3b: eltérő 1908-as alak %s %s: %s / %s' % (k[0], k[1], kulcs[k], d['szo']))
                elif tok_index[k][4]:
                    kieso_strong[tok_index[k][4]] += 1
    if hiany or alak_elter:
        raise SystemExit('K3b hiba: %d hiányzó kulcs, %d eltérő alak (a %d Strongos tokenből)'
                         % (hiany, alak_elter, strongos))
    print('K3b: a #22 %d könyvének %d Strongos magyar tokenje mind a táblában, azonos 1908-as alakkal; '
          'ebből kieső (a gazdaszón át illeszthető): %s' % (konyvek, strongos, dict(kieso_strong)))

    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    hk = ' + '.join('%s (sha256:%s)' % (b, sha(b)) for b in BEMENETEK if os.path.exists(os.path.join(ROOT, b)))
    h = hashlib.sha256()
    szavak = sorted(glob.glob(os.path.join(ROOT, STRONG_SZAVAK)))
    for ut in szavak:
        with open(ut, 'rb') as f:
            h.update(f.read())
    hk += ' + %s (%d fájl, a K3b bemenete, összesített sha256:%s)' % (STRONG_SZAVAK, len(szavak), h.hexdigest())
    fejlec = ('# GENERÁLT: %s (F96.3) — kézzel nem szerkeszthető; a javítás a szabályban (helyesiras.py, igealak.py, '
              'igeragozas.py) vagy a kivételtáblában (helyesiras.py: KIVETEL_LEMMA, ALAK_KIVETEL; igealak.py: KEZI, GYANU_KEZI, '
              'VALA_ELOTT_KEZI, VALA_ELOTT_MULT_KEZI, TOKEN_KIVETEL, E1_TARGYAS_KEZI, OK_KEZI, E1_MINDIG_VEG, KOR3_VALA_HOMOGRAF) | forras=%s | a modernizálás '
              'szintje: helyesírás + igealak, szókincs, szórend, írásjel és betoldás-jelölés változatlan (DT128) | '
              'tokenizálás: eszkozok/karoli_strong/tokenek.py tokenizal (a #22 hu_sorszam-a; a Strong token-kulcson '
              'illeszthető, a réteg Strongot nem tárol, DT-F96f, DT-F96o) | mérés: naplok/KAROLI_MODERN_meres.md 4.9 '
              '(.1, K1 246/246), 5.7 és 7.–8. (.2, K1 a javítások után a 8. szakasz szerint), 10. (a 3. kör, DT-F96q; a lefedettséget is mérő K1: igealak_minta2.tsv) 11. (a 4. kör, DT-F96r), 12. (DT-F96s) és 14. (az 5. kör, DT-F96u), modell-ellenőrzés, a felhasználó elfogadta | ts=%s\n'
              % (SZKRIPT, hk, ts))
    os.makedirs(ki_dir, exist_ok=True)
    with open(os.path.join(ki_dir, 'karoli_modern.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=a Károli 1908 minden tokenje (%d), versenként a tokenizal sorrendjében\n'
                               % len(tok_ki)))
        f.write('\t'.join(['igehely', 'sorszam', 'alak_1908', 'alak_modern', 'kieso', 'kieso_gazda', 'szabaly',
                           'bizonytalan']) + '\n')
        for r in tok_ki:
            f.write('\t'.join(r) + '\n')
    with open(os.path.join(ki_dir, 'karoli_modern_versek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=a Károli 1908 minden verse (%d), a konkordancia/Karoli_1908.tsv '
                               'sorrendjében\n' % len(vers_ki)))
        f.write('\t'.join(['igehely', 'szoveg_modern', 'valtozott']) + '\n')
        for r in vers_ki:
            f.write('\t'.join(r) + '\n')
    c = collections.Counter(r[4] for r in tok_ki)
    print('tokenek: %d (változó: %d, kieső: %s); versek: %d (változó: %d)'
          % (len(tok_ki), sum(1 for r in tok_ki if r[2] != r[3] and not r[4]), dict((k, v) for k, v in c.items() if k),
             len(vers_ki), sum(1 for r in vers_ki if r[2] == 'igen')))


if __name__ == '__main__':
    main()
