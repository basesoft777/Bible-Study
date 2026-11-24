#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
visszaeses_kapu.py -- „ne legyen visszaesés a régi laphoz képest” (DT952, 0. kapu): egy lap új kiadása előtt az új
és a régi (a main-en kiadott) lapot ugyanazokkal az olvasói kapukkal méri, és BUKÁS-t ad, ha az új lapon bármely
kategóriában több a találat, mint a régin.

A szerkesztő célja (2026-11-08): „fontos hogy most már visszaesés ne legyen innen”. A korábbi helyettesítő mérce (a
bájtra azonos kimenet) a régi lap hibáit is megőrizte; ez a kapu a célt méri közvetlenül: a régi lap hibáit nem kell
lemásolni, az egyezés nem cél, csak egyik olvasói hibafajtából sem lehet több.

Kategóriák (mindkét lapon ugyanazzal a szabállyal):
- az olvasói kapu (`olvasoi_kapu.lap_meres`) minden ellenőrzése azonosító és súlyosság szerint (BUKÁS és FIGYELMEZTETÉS
  külön kategória), benne a MINTA, a kerek próza (PROZA_1A, átvett), a lábjegyzet és a VISSZHANG; a darabszám a
  csoportosított találatok `db` összege;
- FORDITASRA_VAR: a „fordításra vár” előfordulása a látható szövegben (a HTML-megjegyzésen kívül).
Mindkét lap az új szerkezet szigorú szabályával mérődik (kivétel nélkül, F178.4): a régi szerkezetű lap kivett szakaszai
(Tartalomjegyzék, Jelmagyarázat, Kolofon) itt nem mentesülnek, mert az olvasó mindkét lapon mindent lát.

Használat:
    python eszkozok/visszaeses_kapu.py ID --uj UJ_LAP [--regi REGI_LAP | --regi-ref REF] [--json FAJL] [--elfogadas TSV]
A régi lap alapból a `REF:lexikon/<ID>_TUDOMANYOS.md` (REF: `origin/main`, ha nincs, `main`).
Elfogadás: az `adat/visszaeses_elfogadas.tsv` (SEMA 2.76) pontosan egyező sora (lap, kategória, régi → új) a növekedést
átengedi; a kimenet `ELFOGADVA` sora a nézési csomagba kerül. Az elavult sort (a mérés már nem ez) `ELAVULT ELFOGADÁS` jelzi.
Kilépési kód: 0 = egyik kategóriában sem több (az elfogadottakon túl); 1 = BUKÁS (a kategóriák listájával); 2 = hívási hiba.
"""

import argparse
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import olvasoi_kapu as OK  # noqa: E402

FORDITASRA_VAR = 'FORDITASRA_VAR'
# Az elfogadási tábla (SEMA 2.76; az integrátor döntése, 2026-11-24): egy növekedés csak lapra és kategóriára szóló,
# indokolt, döntéshez kötött sorral engedhető át, a pontos régi → új darabszámmal (a D19 okonkénti engedélyének mintája).
# Téves szabálytalálatnál nem elfogadás jár, hanem a szabály javítása.
ELFOGADAS_TSV = 'adat/visszaeses_elfogadas.tsv'
ELFOGADAS_OSZLOPOK = ('id', 'kategoria', 'regi', 'uj', 'ok', 'dontes_ref', 'proveniencia')
_MINDIG = re.compile('')     # az új szerkezet jele helyett: minden lap a szigorú szabállyal mérődik


def kategoriak(szoveg):
    """{kategória: darab} egy lapszövegen. A kategória `<azonosító> <súlyosság>` vagy FORDITASRA_VAR."""
    eredeti = OK.UJ_SZERKEZET_RX
    OK.UJ_SZERKEZET_RX = _MINDIG
    try:
        talalatok, _megj = OK.lap_meres(szoveg)
    finally:
        OK.UJ_SZERKEZET_RX = eredeti
    ki = {}
    for t in talalatok:
        k = '%s %s' % (t['azonosito'], t['sulyossag'])
        ki[k] = ki.get(k, 0) + t.get('db', 1)
    lathato = re.sub(r'<!--.*?-->', '', szoveg, flags=re.S)
    n = lathato.count('fordításra vár')
    if n:
        ki[FORDITASRA_VAR] = n
    return ki


def osszevet(regi_szoveg, uj_szoveg):
    """[(kategória, régi, új)] minden kategóriára (rendezve); a visszaesés az, ahol új > régi."""
    regi, uj = kategoriak(regi_szoveg), kategoriak(uj_szoveg)
    return [(k, regi.get(k, 0), uj.get(k, 0)) for k in sorted(set(regi) | set(uj))]


def visszaesesek(sorok):
    return [s for s in sorok if s[2] > s[1]]


def elfogadasok(ut):
    """Az elfogadási tábla sorai ({oszlop: érték}); hiányzó fájl: üres. Hibás sornál ValueError (SEMA 2.76)."""
    if not os.path.isfile(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\r\n') for s in f if s.strip()]
    if not sorok or tuple(sorok[0].split('\t')) != ELFOGADAS_OSZLOPOK:
        raise ValueError('%s: a fejléc %s kell' % (ut, '\t'.join(ELFOGADAS_OSZLOPOK)))
    ki, kulcsok = [], set()
    for n, sor in enumerate(sorok[1:], 2):
        mezok = sor.split('\t')
        if len(mezok) != len(ELFOGADAS_OSZLOPOK):
            raise ValueError('%s:%d: %d mező kell' % (ut, n, len(ELFOGADAS_OSZLOPOK)))
        s = dict(zip(ELFOGADAS_OSZLOPOK, mezok))
        try:
            s['regi'], s['uj'] = int(s['regi']), int(s['uj'])
        except ValueError:
            raise ValueError('%s:%d: a regi és az uj egész szám' % (ut, n)) from None
        if s['uj'] <= s['regi']:
            raise ValueError('%s:%d: csak növekedés fogadható el (uj > regi)' % (ut, n))
        for m in ('id', 'kategoria', 'ok', 'dontes_ref', 'proveniencia'):
            if not s[m].strip():
                raise ValueError('%s:%d: üres mező: %s' % (ut, n, m))
        if not s['proveniencia'].startswith(('scope=', 'manual')):
            raise ValueError('%s:%d: a proveniencia `scope=… | forras=… | ts=…` vagy `manual`' % (ut, n))
        kulcs = (s['id'], s['kategoria'])
        if kulcs in kulcsok:
            raise ValueError('%s:%d: kétszer szereplő lap és kategória: %s %s' % ((ut, n) + kulcs))
        kulcsok.add(kulcs)
        ki.append(s)
    return ki


def szetvalaszt(azonosito, rossz, tabla):
    """(elfogadott, maradék): az elfogadott az a növekedés, amelyhez a táblában pontosan egyező sor áll (lap, kategória,
    régi és új darabszám); minden más növekedés megmarad, és BUKÁS-t ad. Elfogadott: [((kat, régi, új), sor)]."""
    by = {(s['id'], s['kategoria']): s for s in tabla}
    elfogadott, maradek = [], []
    for k, r, u in rossz:
        s = by.get((azonosito, k))
        if s is not None and (s['regi'], s['uj']) == (r, u):
            elfogadott.append(((k, r, u), s))
        else:
            maradek.append((k, r, u))
    return elfogadott, maradek


def elavult_elfogadasok(azonosito, sorok, tabla):
    """A lap azon elfogadási sorai, amelyek a mai mérésre már nem illenek (a növekedés megszűnt vagy más lett)."""
    mert = {k: (r, u) for k, r, u in sorok}
    return [s for s in tabla if s['id'] == azonosito and mert.get(s['kategoria']) != (s['regi'], s['uj'])]


def regi_lap(azonosito, ref=None):
    """A régi (kiadott) lap szövege a git-refből; None, ha nincs (új lap: nincs mihez mérni)."""
    utvonal = 'lexikon/%s_TUDOMANYOS.md' % azonosito
    for r in ([ref] if ref else ['origin/main', 'main']):
        p = subprocess.run(['git', 'show', '%s:%s' % (r, utvonal)], cwd=GYOKER, capture_output=True)
        if p.returncode == 0:
            return p.stdout.decode('utf-8')
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description='Az új lap visszaesése a régihez képest, az olvasói kapuk kategóriái szerint')
    ap.add_argument('id')
    ap.add_argument('--uj', required=True, help='az új lap (pl. a kiadás módban generált lexikon/<ID>_TUDOMANYOS.md)')
    ap.add_argument('--regi', help='a régi lap fájlja (alapból a --regi-ref lexikon/<ID>_TUDOMANYOS.md-je)')
    ap.add_argument('--regi-ref', help='a régi lap git-refje (alapból origin/main, ha nincs: main)')
    ap.add_argument('--json', help='a kategóriánkénti összevetés JSON-fájlba')
    ap.add_argument('--elfogadas', default=os.path.join(GYOKER, *ELFOGADAS_TSV.split('/')),
                    help='az elfogadási tábla (alapból %s)' % ELFOGADAS_TSV)
    a = ap.parse_args(argv)
    try:
        with open(a.uj, encoding='utf-8') as f:
            uj = f.read()
        if a.regi:
            with open(a.regi, encoding='utf-8') as f:
                regi = f.read()
        else:
            regi = regi_lap(a.id, a.regi_ref)
    except OSError as e:
        print('HIBA: %s' % e, file=sys.stderr)
        return 2
    if regi is None:
        print('NINCS RÉGI LAP\t%s\tnincs kiadott lap, nincs mihez mérni (új lap)' % a.id)
        return 0
    try:
        tabla = elfogadasok(a.elfogadas)
    except (OSError, ValueError) as e:
        print('HIBA: %s' % e, file=sys.stderr)
        return 2
    sorok = osszevet(regi, uj)
    rossz = visszaesesek(sorok)
    elfogadott, maradek = szetvalaszt(a.id, rossz, tabla)
    if a.json:
        with open(a.json, 'w', encoding='utf-8', newline='\n') as f:
            json.dump({'id': a.id, 'kategoriak': [{'kategoria': k, 'regi': r, 'uj': u} for k, r, u in sorok],
                       'visszaeses': [k for k, _r, _u in maradek],
                       'elfogadva': [dict(s) for _x, s in elfogadott]},
                      f, ensure_ascii=False, indent=1)
    for k, r, u in sorok:
        jel = 'TÖBB' if u > r else ('kevesebb' if u < r else '')
        print('%-28s régi %4d · új %4d  %s' % (k, r, u, jel))
    # az elfogadott növekedés a nézési csomagba kerül: mindig kiíródik, a döntés hivatkozásával
    for (k, r, u), s in elfogadott:
        print('ELFOGADVA\t%s\t%s (%d → %d)\t%s\t%s' % (a.id, k, r, u, s['ok'], s['dontes_ref']))
    for s in elavult_elfogadasok(a.id, sorok, tabla):
        print('ELAVULT ELFOGADÁS\t%s\t%s (%d → %d)\ta mért növekedés már nem ez: a sor törlendő vagy újra eldöntendő'
              % (a.id, s['kategoria'], s['regi'], s['uj']))
    if maradek:
        print('BUKÁS\t%s\tvisszaesés a régi laphoz képest %d kategóriában: %s'
              % (a.id, len(maradek), ', '.join('%s (%d → %d)' % s for s in maradek)))
        return 1
    print('RENDBEN\t%s\tegyik kategóriában sincs több találat, mint a régi lapon%s'
          % (a.id, ' (az elfogadott növekedésen túl: %d)' % len(elfogadott) if elfogadott else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main())
