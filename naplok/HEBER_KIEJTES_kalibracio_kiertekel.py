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
FORRASOK = ['gepi', 'javaslat', 'alternativa', 'alternativa2']


def chat_beolvas(szoveg):
    ki = {}
    if ':' in szoveg:
        # a kalibráló oldal alakja: „1:A*,B 4:A 13:B,C 41:B[káreú]” -- vesszővel az elfogadhatók,
        # „*” a preferált; csillag nélkül nincs preferált; [..] saját alak, amely a preferált
        # (ha más nincs csillaggal jelölve); a saját alak belső jele: '#'
        for tok in szoveg.split():
            mt = re.fullmatch(r'(\d+):((?:[A-Ca-c]\*?|\[[^\]]+\]|,)+)', tok.strip())
            if not mt:
                raise SystemExit(f'értelmezhetetlen tétel: {tok!r} (várt alak: 12:A*,B vagy 12:B[saját])')
            elemek = re.findall(r'([A-Ca-c])(\*?)|\[([^\]]+)\]', mt.group(2))
            betuk = [(b.upper(), cs == '*') for b, cs, e in elemek if b]
            egyeni = next((e for b, cs, e in elemek if e), None)
            pref = [b for b, csillag in betuk if csillag]
            if len(pref) > 1:
                raise SystemExit(f'több preferált: {tok!r}')
            ki[int(mt.group(1))] = {'preferalt': pref[0] if pref else ('#' if egyeni else None),
                                    'elfogadhato': sorted({b for b, _ in betuk}), 'egyeni': egyeni}
        return ki
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
    ap.add_argument('--kimenet')
    ap.add_argument('--menet', type=int, default=1, help='1: kalibracio.json; 2: kalibracio2.json')
    a = ap.parse_args()
    sfx = '' if a.menet == 1 else str(a.menet)
    minta_ut = os.path.join(ROOT, 'naplok', f'HEBER_KIEJTES_kalibracio{sfx}.json')
    kulcs_ut = os.path.join(ROOT, 'naplok', f'HEBER_KIEJTES_kalibracio{sfx}_kulcs.json')
    a.kimenet = a.kimenet or (KIMENET if a.menet == 1 else
                              os.path.join(ROOT, 'naplok', f'HEBER_KIEJTES_kalibracio{sfx}_eredmeny.md'))
    if bool(a.chat) == bool(a.fajl):
        raise SystemExit('pontosan egy bemenet kell: --chat vagy --fajl')
    valasztas = chat_beolvas(a.chat) if a.chat else fajl_beolvas(a.fajl)
    with open(minta_ut, encoding='utf-8') as f:
        minta = {t['sorszam']: t for t in json.load(f)['tetelek']}
    with open(kulcs_ut, encoding='utf-8') as f:
        kulcs = {k['sorszam']: k['forras'] for k in json.load(f)['kulcs']}
    hianyzik = sorted(set(minta) - set(valasztas))
    ismeretlen = sorted(set(valasztas) - set(minta))
    if ismeretlen:
        raise SystemExit(f'nem létező sorszám: {ismeretlen}')

    # (kategória, forrás) -> [egyezik a preferálttal, elfogadható (nincs preferált), (b), (a)]
    stat = {}
    sorok = []
    reszletes = []
    for n in sorted(valasztas):
        t, v = minta[n], valasztas[n]
        kiejt = {x['betu']: x['kiejtes'] for x in t['variansok']}
        if v.get('egyeni'):
            kiejt['#'] = v['egyeni'] + ' (saját alak)'
        forras_betu = {}
        for betu, cimke in kulcs[n].items():
            for c in cimke.split('+'):
                # az alternativa2 csak akkor létezik, ha a gépi = javaslat (külön forrás)
                forras_betu[c] = betu
        eredmenyek = {}
        for fr in FORRASOK:
            betu = forras_betu.get(fr)
            if betu is None:
                continue
            s = stat.setdefault((t['kategoria'], fr), [0, 0, 0, 0])
            if betu not in v['elfogadhato']:
                s[3] += 1
                ered = '(a) hibás'
            elif v['preferalt'] is None:
                s[1] += 1
                ered = 'elfogadható'
            elif betu == v['preferalt']:
                s[0] += 1
                ered = 'egyezik'
            else:
                s[2] += 1
                ered = '(b) konvenció-eltérés'
            eredmenyek[fr] = ered
            if fr == 'gepi' and ered not in ('egyezik', 'elfogadható'):
                elf = ', '.join(kiejt[b] + ('*' if b == v['preferalt'] else '')
                                for b in v['elfogadhato'] + (['#'] if v.get('egyeni') else []))
                sorok.append((n, t['kategoria'], t['heber'], kiejt[betu], elf, ered))
        reszletes.append((n, t['kategoria'], t['heber'],
                          {fr: kiejt[forras_betu[fr]] for fr in FORRASOK if fr in forras_betu},
                          ', '.join(kiejt[b] + ('*' if b == v['preferalt'] else '')
                                    for b in v['elfogadhato'] + (['#'] if v.get('egyeni') else [])),
                          eredmenyek))
    kategoriak = []
    for t in minta.values():
        if t['kategoria'] not in kategoriak:
            kategoriak.append(t['kategoria'])

    L = ['# Gépi héber kiejtés — a kalibrálás kiértékelése (N-F131w)', '',
         f'*Bemenet: {"chat" if a.chat else a.fajl}; {len(valasztas)} választás, '
         f'{len(hianyzik)} kihagyott sor{(" (" + ", ".join(map(str, hianyzik)) + ")") if hianyzik else ""}. '
         'Adat és szabály nem változott.*', '',
         'Mértékek: **egyezik** (a preferált) · **elf.** (elfogadható, a sorban nincs preferált) · '
         '**(b) konvenció-eltérés** (elfogadható, nem preferált; a szabály ehhez igazodik) · '
         '**(a) hibás** (nem elfogadható; valódi hiba).', '',
         '| kategória | n | gépi: egyezik / elf. / (b) / (a) | javaslat: egyezik / elf. / (b) / (a) | '
         'alternatíva: egyezik / elf. / (b) / (a) | 2. alternatíva (ha gépi = javaslat): egyezik / elf. / (b) / (a) |',
         '|---|---|---|---|---|---|']
    tot = {fr: [0, 0, 0, 0] for fr in FORRASOK}
    for kat in kategoriak:
        cell = []
        for fr in FORRASOK:
            s = stat.get((kat, fr), [0, 0, 0, 0])
            tot[fr] = [x + y for x, y in zip(tot[fr], s)]
            cell.append(' / '.join(map(str, s)))
        n_kat = sum(stat.get((kat, 'gepi'), [0, 0, 0, 0]))
        L.append(f'| {kat} | {n_kat} | ' + ' | '.join(cell) + ' |')
    L.append(f'| **összesen** | {sum(tot["gepi"])} | '
             + ' | '.join('**' + ' / '.join(map(str, tot[fr])) + '**' for fr in FORRASOK) + ' |')
    if any(k.startswith('vegyes') for k in kategoriak):
        atl = [0, 0, 0, 0]
        neh = [0, 0, 0, 0]
        for kat in kategoriak:
            s = stat.get((kat, 'gepi'), [0, 0, 0, 0])
            cel = atl if kat.startswith('vegyes') else neh
            for i in range(4):
                cel[i] += s[i]
        L += ['', '| gépi változat | n | egyezik / elf. / (b) / (a) | elfogadható |', '|---|---|---|---|']
        for nev, x in (('átlagos (vegyes)', atl), ('nehéz (a többi kategória)', neh)):
            L.append(f'| {nev} | {sum(x)} | ' + ' / '.join(map(str, x)) + f' | {sum(x[:3])}/{sum(x)} |')
    L += ['', '## A gépi változat eltérései', '',
          '| # | kategória | héber | gépi | elfogadható (* preferált) | eredmény |', '|---|---|---|---|---|---|']
    for n, kat, heb, g, p, e in sorok:
        L.append(f'| {n} | {kat} | {heb} | {g} | {p} | {e} |')
    L += ['', '## Soronként (a kulccsal feloldva)', '',
          '| # | kategória | héber | gépi | javaslat | alternatíva | 2. alternatíva | elfogadható (* preferált) | gépi | javaslat | alternatíva | 2. alternatíva |',
          '|---|---|---|---|---|---|---|---|---|---|---|---|']
    for n, kat, heb, kj, elf, er in reszletes:
        L.append(f"| {n} | {kat} | {heb} | {kj.get('gepi', '')} | {kj.get('javaslat', '')} | "
                 f"{kj.get('alternativa', '')} | {kj.get('alternativa2', '')} | {elf} | {er.get('gepi', '')} | "
                 f"{er.get('javaslat', '')} | {er.get('alternativa', '')} | {er.get('alternativa2', '')} |")
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L[:8 + len(kategoriak) + 1]))


if __name__ == '__main__':
    main()
