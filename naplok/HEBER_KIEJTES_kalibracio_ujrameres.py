"""Újramérés az első kalibráló mintán a DT-F131y szabályaival (N-F131w).

Az első minta 50 alakját (naplok/HEBER_KIEJTES_kalibracio.py, ugyanaz a seed)
a DT-F131y szabálykészletével (naplok/HEBER_KIEJTES_meres.py dt_f131y()) írja át,
és összeveti a felhasználó választásával
(naplok/HEBER_KIEJTES_kalibracio_valasztas.txt, a kulccsal feloldva):
  elfogadható   -- az új gépi alak egy elfogadott változattal egyezik
  (ebből preferált)
  nem elfogadott -- egy NEM elfogadott változattal egyezik (valódi hiba)
  új alak       -- egyik változattal sem egyezik: nincs rá ítélet (a felhasználónak)

Kimenet: naplok/HEBER_KIEJTES_kalibracio_ujrameres.md. Adatot nem ír.
"""

import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'naplok'))
import HEBER_KIEJTES_meres as m  # noqa: E402
import HEBER_KIEJTES_kalibracio as k  # noqa: E402
import HEBER_KIEJTES_kalibracio_kiertekel as ke  # noqa: E402

VALASZTAS = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kalibracio_valasztas.txt')
KIMENET = os.path.join(ROOT, 'naplok', 'HEBER_KIEJTES_kalibracio_ujrameres.md')
# a nem elfogadott és az új alakok oka (manual, a session elemzése)
OK = {
    4: 'a döntés következménye: R4 elutasítva (a meteg nélküli kámec utáni sevá néma)',
    11: 'a döntés következménye: R8 (ח = ch); a felhasználó itt h-t választott',
    17: 'nyitott: a zajin alatti sevát a felhasználó kiejtette; szabály nem fedi',
    19: 'nyitott: cere + jod furtív előtt (réjach); R9 nem lett szabály',
    24: 'nyitott: a kettőzött betű alatti sevát a felhasználó nem ejtette (missól); R3 itt ellentétes',
    37: 'nyitott: R3 kiejtett sevát ad (kiseól), a felhasználó itt kisól-t fogadott el; új alak, nincs ítélet',
    41: 'nyitott: hosszúság (a felhasználó vesalém-et fogadott el, a gép vesálém-et ad)',
    46: 'a döntés következménye: R1 + R8 (chámász); a felhasználó itt hámász-t fogadott el; új alak',
    48: 'a döntés következménye: R8 (ח = ch); a felhasználó itt h-t választott',
}


def main():
    p = m.dt_f131y()
    _, _, _, _, valasztott = k.minta()
    with open(k.KI_JSON, encoding='utf-8') as f:
        tetelek = {t['sorszam']: t for t in json.load(f)['tetelek']}
    with open(VALASZTAS, encoding='utf-8') as f:
        valasztas = ke.chat_beolvas(f.read())
    stat = {}
    sorok = []
    for w in valasztott:
        t = tetelek[w['sorszam']]
        if t['heber'] != w['tiszta']:
            raise SystemExit(f"{w['sorszam']}. sor: a minta eltér a JSON-tól")
        uj, _ = k.kiejt(w, p)
        v = valasztas[w['sorszam']]
        kiejt = {x['betu']: x['kiejtes'] for x in t['variansok']}
        betu = next((b for b, x in kiejt.items() if x == uj), None)
        if betu is None:
            ered = 'új alak'
        elif betu in v['elfogadhato']:
            ered = 'elfogadható (preferált)' if betu == v['preferalt'] else 'elfogadható'
        else:
            ered = 'nem elfogadott'
        s = stat.setdefault(t['kategoria'], {})
        s[ered] = s.get(ered, 0) + 1
        elf = ', '.join(kiejt[b] + ('*' if b == v['preferalt'] else '') for b in v['elfogadhato'])
        sorok.append((w['sorszam'], t['kategoria'], t['heber'], w['gepi'], uj, elf, ered))
    kat_sor = []
    for t in tetelek.values():
        if t['kategoria'] not in kat_sor:
            kat_sor.append(t['kategoria'])
    oszl = ['elfogadható (preferált)', 'elfogadható', 'nem elfogadott', 'új alak']
    ossz = {o: sum(s.get(o, 0) for s in stat.values()) for o in oszl}
    L = ['# Újramérés az első kalibráló mintán a DT-F131y szabályaival (N-F131w)', '',
         '*A szabályok a kísérleti átíróban (`naplok/HEBER_KIEJTES_meres.py`, `dt_f131y()`); '
         'nincsenek az `eszkozok/` alatt, és a lapokba sincsenek bekötve. Adat nem változott.*', '',
         '- **Proveniencia:** `scope=naplok/HEBER_KIEJTES_kalibracio.json (50 alak) + naplok/HEBER_KIEJTES_kalibracio_valasztas.txt '
         '| forras=naplok/HEBER_KIEJTES_kalibracio_ujrameres.py | ts=2026-10-30`',
         '- **Mérték:** az új gépi alak egyezik-e egy elfogadott változattal. Ha egyik változattal sem egyezik '
         '(„új alak”), arra a kalibrálás nem ad ítéletet.', '',
         f"**Eredmény: {ossz['elfogadható (preferált)'] + ossz['elfogadható']}/50 elfogadható** "
         f"(ebből {ossz['elfogadható (preferált)']} preferált), {ossz['nem elfogadott']} nem elfogadott, "
         f"{ossz['új alak']} új alak (nincs ítélet). Előtte, a mai szabályokkal: 25/50.", '',
         '| kategória | ' + ' | '.join(oszl) + ' |', '|---|' + '---|' * len(oszl)]
    for kat in kat_sor:
        L.append(f'| {kat} | ' + ' | '.join(str(stat.get(kat, {}).get(o, 0)) for o in oszl) + ' |')
    L.append('| **összesen** | ' + ' | '.join(f'**{ossz[o]}**' for o in oszl) + ' |')
    L += ['', '## Soronként', '',
          '| # | kategória | héber | gépi (régi) | gépi (DT-F131y) | elfogadható (* preferált) | eredmény | ok |',
          '|---|---|---|---|---|---|---|---|']
    for n, kat, heb, regi, uj, elf, ered in sorok:
        L.append(f'| {n} | {kat} | {heb} | {regi} | {uj} | {elf} | {ered} | {OK.get(n, "")} |')
    L += ['', '**A 9 nem elfogadott vagy új alakból 4 a DT-F131y egyenes következménye** (4: R4; 11, 46, 48: R8), '
          '**5 nyitott** (17, 19, 24, 37, 41). A nyitottak közül egy sem egyezik egy másikkal annyira, hogy '
          'szabályt lehetne rá építeni; a 2. minta mutatja meg, ismétlődnek-e.']
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L[8:20]))
    for r in sorok:
        if r[6] in ('nem elfogadott', 'új alak'):
            print(r)


if __name__ == '__main__':
    main()
