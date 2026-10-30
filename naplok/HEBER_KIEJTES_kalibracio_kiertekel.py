"""A kalibráló minta kiértékelése a felhasználó választása után (N-F131w).

Bemenet (egyik):
  --chat "1A 2C 3BA …"  -- sorszám + betűk; az első betű a preferált, a többi
                           is elfogadható (pl. 3BA: B preferált, A elfogadható)
  --fajl valasztas.json  -- {"valasztasok": [{"sorszam": 1, "elfogadhato": ["A", "C"],
                           "preferalt": "C"}, ...]} (a kalibráló oldal kimenete)
A minta és a kulcs: naplok/HEBER_KIEJTES_kalibracio.json és
naplok/HEBER_KIEJTES_kalibracio_kulcs.json.

Mértékek forrásonként (gépi / javaslat / alternatíva):
  egyezik    -- a forrás változata a preferált
  (b) konvenció-eltérés -- elfogadható, de nem a preferált (a szabály ehhez igazodik)
  (a) hibás  -- nem elfogadható (valódi hiba)
Ha egy változat két forrásból is jött (pl. gepi+javaslat), mindkettőhöz számít.

Kimenet: naplok/HEBER_KIEJTES_kalibracio_eredmeny.md (vagy --kimenet).
Adatot nem ír, szabályt nem módosít.
"""

import argparse
import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MINTA = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kalibracio.json')
KULCS = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kalibracio_kulcs.json')
KIMENET = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kalibracio_eredmeny.md')
FORRASOK = ['gepi', 'javaslat', 'alternativa']


def chat_beolvas(szoveg):
    ki = {}
    for tok in szoveg.replace(',', ' ').split():
        mt = re.fullmatch(r'(\d+)([A-Ca-c]+)', tok.strip())
        if not mt:
            raise SystemExit(f'értelmezhetetlen tétel: {tok!r} (várt alak: 12A vagy 12BA)')
        betuk = mt.group(2).upper()
        ki[int(mt.group(1))] = {'preferalt': betuk[0], 'elfogadhato': sorted(set(betuk))}
    return ki


def fajl_beolvas(ut):
    with open(ut, encoding='utf-8') as f:
        d = json.load(f)
    ki = {}
    for v in d['valasztasok']:
        elf = sorted(set(v.get('elfogadhato', [])) | {v['preferalt']})
        ki[int(v['sorszam'])] = {'preferalt': v['preferalt'], 'elfogadhato': elf}
    return ki


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chat')
    ap.add_argument('--fajl')
    ap.add_argument('--kimenet', default=KIMENET)
    a = ap.parse_args()
    if bool(a.chat) == bool(a.fajl):
        raise SystemExit('pontosan egy bemenet kell: --chat vagy --fajl')
    valasztas = chat_beolvas(a.chat) if a.chat else fajl_beolvas(a.fajl)
    with open(MINTA, encoding='utf-8') as f:
        minta = {t['sorszam']: t for t in json.load(f)['tetelek']}
    with open(KULCS, encoding='utf-8') as f:
        kulcs = {k['sorszam']: k['forras'] for k in json.load(f)['kulcs']}
    hianyzik = sorted(set(minta) - set(valasztas))
    ismeretlen = sorted(set(valasztas) - set(minta))
    if ismeretlen:
        raise SystemExit(f'nem létező sorszám: {ismeretlen}')

    stat = {}      # (kategória, forrás) -> [egyezik, b, a]
    sorok = []
    for n in sorted(valasztas):
        t, v = minta[n], valasztas[n]
        kiejt = {x['betu']: x['kiejtes'] for x in t['variansok']}
        forras_betu = {}
        for betu, cimke in kulcs[n].items():
            for c in cimke.split('+'):
                forras_betu[c.replace('alternativa2', 'alternativa')] = betu
        for fr in FORRASOK:
            betu = forras_betu.get(fr)
            if betu is None:
                continue
            s = stat.setdefault((t['kategoria'], fr), [0, 0, 0])
            if betu == v['preferalt']:
                s[0] += 1
                ered = 'egyezik'
            elif betu in v['elfogadhato']:
                s[1] += 1
                ered = '(b) konvenció-eltérés'
            else:
                s[2] += 1
                ered = '(a) hibás'
            if fr == 'gepi' and ered != 'egyezik':
                sorok.append((n, t['kategoria'], t['heber'], kiejt[betu], kiejt[v['preferalt']], ered))
    kategoriak = []
    for t in minta.values():
        if t['kategoria'] not in kategoriak:
            kategoriak.append(t['kategoria'])

    L = ['# Gépi héber kiejtés — a kalibrálás kiértékelése (N-F131w)', '',
         f'*Bemenet: {"chat" if a.chat else a.fajl}; {len(valasztas)} választás, '
         f'{len(hianyzik)} kihagyott sor{(" (" + ", ".join(map(str, hianyzik)) + ")") if hianyzik else ""}. '
         'Adat és szabály nem változott.*', '',
         'Mértékek: **egyezik** (a preferált) · **(b) konvenció-eltérés** (elfogadható, nem preferált; a szabály ehhez igazodik) · '
         '**(a) hibás** (nem elfogadható; valódi hiba).', '',
         '| kategória | gépi: egyezik / (b) / (a) | javaslat: egyezik / (b) / (a) | alternatíva: egyezik / (b) / (a) |',
         '|---|---|---|---|']
    tot = {fr: [0, 0, 0] for fr in FORRASOK}
    for kat in kategoriak:
        cell = []
        for fr in FORRASOK:
            s = stat.get((kat, fr), [0, 0, 0])
            tot[fr] = [x + y for x, y in zip(tot[fr], s)]
            cell.append(' / '.join(map(str, s)))
        L.append(f'| {kat} | ' + ' | '.join(cell) + ' |')
    L.append('| **összesen** | ' + ' | '.join('**' + ' / '.join(map(str, tot[fr])) + '**' for fr in FORRASOK) + ' |')
    L += ['', '## A gépi változat eltérései', '',
          '| # | kategória | héber | gépi | preferált | eredmény |', '|---|---|---|---|---|---|']
    for n, kat, heb, g, p, e in sorok:
        L.append(f'| {n} | {kat} | {heb} | {g} | {p} | {e} |')
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L[:8 + len(kategoriak) + 1]))


if __name__ == '__main__':
    main()
