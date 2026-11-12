#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kovetelmeny_kapu.py -- F196.2: a követelménylista-kapu (JELENTÉS szint).

Mit mér: a `sablonok/KESZ_LAP_KOVETELMENY.md` (a kész lap lezárt követelménylistája, DT738) K-sorait olvassa. Ahol a
sor „Ellenőrzés” oszlopában gépi szabály áll, a kapu lefuttatja vagy összegyűjti a szabály eredményét az adott lapra,
és kiírja: „HAMART-001: N/M követelmény teljesül (gépi)”, utána a nem teljesülő sorok listáját. A lista csak bemenet:
a kapu nem írja, és a szabályok szövegét sem ismétli (a kanonikus helyük a lista „Forrás” oszlopa).

Az „Ellenőrzés” oszlop felismert szabályai (`szabalyok_a_cellabol`):
  * az olvasói kapu azonosítói (`olvasoi_kapu.KAPUK`, pl. BELSO, ATIRAS, KIVONAT_SZAM) és a VISSZHANG alszabályai
    (V1–V7): a lap `olvasoi_kapu.motivum_meres` mérése; a szabály nem teljesül, ha a lapon találata van (BUKÁS vagy
    FIGYELMEZTETÉS);
  * az `ellenoriz.py` szabályai (`ellenoriz.py` 40., 36., 2/b; „a #182 42. szabálya”): a szabályfüggvény a táblákon
    fut; a lapra nem teljesül, ha SÉRTÉS- vagy JELENTÉS-példája a motívumot nevezi meg;
  * a CI-szabályok (`CI E8`, `E28`): a `szabalyok.SZABALYOK_FUGGVENYEI` függvénye a lapfájlra; nem teljesül, ha a lapra
    találatot ad. Az E28 a generátort futtatja (a HAMART-001-en perceket): csak az `--e28` kapcsolóval fut, különben
    „gépi, a kapu nem gyűjti” (a CI a változott lapra az E2–E37 lépésben amúgy is futtatja).
Ami nem ilyen (lektor, szerkesztő, „gépi: nincs”, „gépi: tervezett …”), az „ember ellenőrzi”. Ami gépi, de a kapu nem
tudja összegyűjteni (pl. „az F24 kapuja”, „grep a markerre”), az „gépi, a kapu nem gyűjti” — külön számolva, nem
teljesülésként.

A HAMART-001-nél a jelentés a lista „HAMART-állapot” oszlopát is mellé teszi: ha a lista „teljesül”-t mond, a gép nem,
vagy fordítva, az eltérés külön jelölést kap (a lista állapota elavulhat, a gépi mérés a mai lapon fut).

Szint: JELENTÉS. A kilépési kód 0 (`--szigoru`: 1, ha van nem teljesülő gépi sor; a HIBA-szintre emelés külön döntéssel
jön, DT-F196a).

CLI:
    python eszkozok/ellenorzes/kovetelmeny_kapu.py HAMART-001
    python eszkozok/ellenorzes/kovetelmeny_kapu.py HAMART-001 ISTENTISZT-001 --e28
"""

import argparse
import collections
import inspect
import io
import os
import re
import sys

ESZKOZOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ESZKOZOK not in sys.path:
    sys.path.insert(0, ESZKOZOK)
ELLENORZES = os.path.dirname(os.path.abspath(__file__))
if ELLENORZES not in sys.path:
    sys.path.insert(0, ELLENORZES)
GYOKER = os.path.dirname(ESZKOZOK)
LISTA = os.path.join(GYOKER, 'sablonok', 'KESZ_LAP_KOVETELMENY.md')
ADAT = os.path.join(GYOKER, 'adat')

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# ---------------------------------------------------------------------------
# A lista beolvasása
# ---------------------------------------------------------------------------

Sor = collections.namedtuple('Sor', 'k blokk kovetelmeny forras ellenorzes allapot')
_K_SOR = re.compile(r'^\|\s*(K\d+[a-z]?)\s*\|')


def cellak(sor):
    """A táblasor cellái (a `\\|` escape-elt pipe nem határ)."""
    resz = re.split(r'(?<!\\)\|', sor.strip())
    return [c.strip() for c in resz[1:-1]]


def lista_sorai(ut=LISTA):
    """A követelménylista K-sorai, a fájl sorrendjében."""
    ki = []
    with io.open(ut, encoding='utf-8') as f:
        for s in f:
            if not _K_SOR.match(s):
                continue
            c = cellak(s)
            if len(c) < 6:
                continue
            ki.append(Sor(*c[:6]))
    return ki


# ---------------------------------------------------------------------------
# A szabályok felismerése az „Ellenőrzés” cellából
# ---------------------------------------------------------------------------

EMBER, NEM_GYUJTHETO, GEPI = 'ember', 'nem_gyujtheto', 'gepi'
Szabaly = collections.namedtuple('Szabaly', 'tipus azon')   # tipus: olvasoi | visszhang | ellenoriz | ci

_ELLENORIZ_SZAM = re.compile(r'(\d+)(/[a-z])?\.?')


def _olvasoi_azonositok():
    import olvasoi_kapu as OK
    return {k[0] for k in OK.KAPUK}


def szabalyok_a_cellabol(cella, olvasoi=None):
    """(osztály, [Szabaly], megjegyzés) — osztály: GEPI (van gyűjthető szabály), NEM_GYUJTHETO (gépi, de egyik sem
    gyűjthető), EMBER (nincs gépi szabály: lektor, szerkesztő, „gépi: nincs”, „gépi: tervezett”)."""
    olvasoi = olvasoi if olvasoi is not None else _olvasoi_azonositok()
    c = cella.strip()
    kis = c.lower()
    if not kis.startswith('gépi'):
        return EMBER, [], c
    torzs = re.sub(r'^gépi(?:\s*\+\s*\w+)?\s*:?\s*', '', c)
    if re.match(r'^(nincs|tervezett)\b', torzs):
        return EMBER, [], 'nincs gépi szabály (%s)' % torzs
    szab = []
    tisztitott = re.sub(r'`', '', torzs)
    # az ellenoriz.py szabályai: „ellenoriz.py 36., 37., 38.”, „ellenoriz.py 2/b”, „a #182 42. szabálya”
    for m in re.finditer(r'ellenoriz\.py\s+((?:\d+(?:/[a-z])?\.?(?:,\s*|\s+|$))+)', tisztitott):
        for n in _ELLENORIZ_SZAM.finditer(m.group(1)):
            szab.append(Szabaly('ellenoriz', n.group(1) + (n.group(2) or '')))
    for m in re.finditer(r'#182 (\d+)\. szabálya', tisztitott):
        szab.append(Szabaly('ellenoriz', m.group(1)))
    m = re.match(r'^(\d+)\.\s', tisztitott)   # „39. (a döntés-commit …)”: a szám az ellenoriz.py szabálya
    if m:
        szab.append(Szabaly('ellenoriz', m.group(1)))
    # CI-szabályok: „CI E28”, „E28 (generált)”
    for m in re.finditer(r'\bE(\d{1,2})\b', tisztitott):
        szab.append(Szabaly('ci', 'E' + m.group(1)))
    # az olvasói kapu azonosítói és a VISSZHANG alszabályai
    for m in re.finditer(r'\b([A-Z][A-Z0-9_]{2,})\b', tisztitott):
        if m.group(1) in olvasoi:
            szab.append(Szabaly('olvasoi', m.group(1)))
    for m in re.finditer(r'\bV([1-7])\b', tisztitott):
        szab.append(Szabaly('visszhang', 'V' + m.group(1)))
    # az olvasói kapu egésze (K03: „olvasói kapu (Feed 9)”): a lapon 0 BUKÁS
    if re.search(r'olvasói kapu', tisztitott):
        szab.append(Szabaly('olvasoi_egesz', 'BUKÁS'))
    # az állítás–adat kapu (F196): a lista „Ellenőrzés” cellája ezen a néven hivatkozhat rá (N-F196d)
    if re.search(r'\ballitas_adat\b|állítás–adat kapu', tisztitott):
        szab.append(Szabaly('allitas', 'allitas_adat'))
    egyedi = []
    for s in szab:
        if s not in egyedi:
            egyedi.append(s)
    if not egyedi:
        if re.search(r'\btervezett\b', torzs):
            return EMBER, [], 'nincs gépi szabály (%s)' % torzs
        return NEM_GYUJTHETO, [], torzs or c
    if VEGYES.search(tisztitott):
        return GEPI, egyedi, 'részben gépi: ' + torzs
    return GEPI, egyedi, torzs


# A cella nem gépi része (lektor, szerkesztő, „grep”, „nincs”): a sor gépi mérése csak részleges.
VEGYES = re.compile(r'\blektor|\bszerkesztő|\bgrep\b|:\s*nincs\b')


# ---------------------------------------------------------------------------
# A szabályok futtatása egy lapra
# ---------------------------------------------------------------------------

# CI-szabályok, amelyek a lapfájlra nem adnak mérést (a találatuk az adattáblára esik, vagy a lapot nem olvassák): a
# rájuk hivatkozó sor ezen a részén nem gyűjthető, nem teljesülés.
CI_LAPRA_NEM_FUT = {
    'E19': 'csak az adat/ szótári tábláin fut (E19_FAJLOK)',
    'E34': 'a találata az adat/elofordulasok.tsv-re esik (E34_TABLA)',
}


class Futtato(object):
    """A szabályok eredménye egy motívum lapjára, gyorsítótárral (egy szabály egyszer fut)."""

    def __init__(self, mid, e28=False):
        self.mid = mid
        self.e28 = e28
        self.lap_rel = 'lexikon/%s_TUDOMANYOS.md' % mid
        self._olvasoi = None
        self._ell = {}
        self._ci = {}
        self._tablak = None

    # -- olvasói kapu --------------------------------------------------------------
    def olvasoi(self):
        if self._olvasoi is None:
            import olvasoi_kapu as OK
            talalatok, _megj = OK.motivum_meres(self.mid)
            self._olvasoi = talalatok or []
        return self._olvasoi

    # Minden eredmény (teljesül, üzenet, kemény): `teljesül` None, ha a szabály nem gyűjthető; `kemény` True, ha a
    # találat gátló szintű (BUKÁS, SÉRTÉS, HIBA, adat-eltérés), False, ha csak FIGYELMEZTETÉS vagy JELENTÉS.
    def olvasoi_eredmeny(self, azon):
        t = [x for x in self.olvasoi() if x['azonosito'] == azon]
        db = sum(x.get('db', 1) for x in t)
        suly = sorted({x['sulyossag'] for x in t})
        return (not t), ('%d találat (%s)' % (db, ', '.join(suly)) if t else ''), ('BUKÁS' in suly)

    def visszhang_eredmeny(self, v):
        t = [x for x in self.olvasoi() if x['azonosito'] == 'VISSZHANG' and (x.get('uzenet') or '').startswith(v + ' ')]
        db = sum(x.get('db', 1) for x in t)
        return (not t), ('%d találat (BUKÁS)' % db if t else ''), bool(t)

    # -- ellenoriz.py --------------------------------------------------------------
    def _tabla_argumentumok(self):
        if self._tablak is None:
            import general as G
            jf, jel = G.tsv_beolvas(os.path.join(ADAT, 'jeloltek.tsv'))
            _, mot = G.tsv_beolvas(os.path.join(ADAT, 'motivumok.tsv'))
            _, elof = G.tsv_beolvas(os.path.join(ADAT, 'elofordulasok.tsv'))
            _, kapcs = G.tsv_beolvas(os.path.join(ADAT, 'kapcsolatok.tsv'))
            _, dat = G.tsv_beolvas(os.path.join(ADAT, 'datasetek.tsv'))
            _, aud = G.tsv_beolvas(os.path.join(ADAT, 'auditok.tsv'))
            _, lh = G.tsv_beolvas(os.path.join(ADAT, 'lexikon_hivatkozasok.tsv'))
            self._tablak = {'adat_dir': ADAT, 'jeloltek': jel, 'jeloltek_fejlec': jf, 'motivumok': mot,
                            'elofordulasok': elof, 'kapcsolatok': kapcs, 'datasetek': dat, 'auditok': aud,
                            'lexikon_hivatkozasok': lh, 'motivum_id_halmaz': {m['id'] for m in mot}}
        return self._tablak

    def ellenoriz_eredmeny(self, szam):
        if szam in self._ell:
            return self._ell[szam]
        import ellenoriz as E
        nev = 'szabaly%s_' % szam.replace('/', '')
        fv = [getattr(E, n) for n in dir(E) if n.startswith(nev) and callable(getattr(E, n))]
        fv = [f for f in fv if f.__name__ != 'szabaly13_konkordancia_forrasok']
        if len(fv) != 1:
            self._ell[szam] = (None, 'az ellenoriz.py %s. szabálya nem található' % szam, None)
            return self._ell[szam]
        f = fv[0]
        tab = self._tabla_argumentumok()
        kw = {}
        for p in inspect.signature(f).parameters.values():
            if p.name in tab:
                kw[p.name] = tab[p.name]
            elif p.default is inspect.Parameter.empty:
                self._ell[szam] = (None, 'a %s paramétere (%s) nem adható át' % (f.__name__, p.name), None)
                return self._ell[szam]
        try:
            ered = f(**kw)
        except Exception as e:  # noqa: BLE001 -- a szabály hibája: nem gyűjthető, nem teljesülés
            self._ell[szam] = (None, '%s: %s' % (type(e).__name__, e), None)
            return self._ell[szam]
        if isinstance(ered, tuple):
            ered = ered[0]
        verdict = getattr(ered, 'verdict', '')
        szovegek = list(getattr(ered, 'peldak', []) or []) + [getattr(ered, 'megjegyzes', '') or '']
        erinti = [p for p in szovegek if self.mid in str(p)]
        if verdict.startswith('KÉZI'):
            self._ell[szam] = (None, 'KÉZI', None)
        elif erinti and (verdict.startswith('SÉRTÉS') or verdict.startswith('JELENTÉS')):
            self._ell[szam] = (False, '%s, a lapot %d példa nevezi meg' % (verdict, len(erinti)),
                               verdict.startswith('SÉRTÉS'))
        else:
            self._ell[szam] = (True, verdict + ('' if verdict.startswith('RENDBEN') else ', a lap nincs a példák között'),
                               False)
        return self._ell[szam]

    # -- CI-szabályok ----------------------------------------------------------------
    def ci_eredmeny(self, e):
        if e in self._ci:
            return self._ci[e]
        import szabalyok as SZ
        if e == 'E28' and not self.e28:
            self._ci[e] = (None, 'nem futott (az E28 a generátort futtatja; --e28 kapcsolóval fut)', None)
            return self._ci[e]
        if e in CI_LAPRA_NEM_FUT:
            self._ci[e] = (None, 'a %s nem a lapfájlon fut (%s)' % (e, CI_LAPRA_NEM_FUT[e]), None)
            return self._ci[e]
        fv = SZ.SZABALYOK_FUGGVENYEI.get(e)
        if fv is None:
            self._ci[e] = (None, 'a %s nem fájlra futó szabály' % e, None)
            return self._ci[e]
        try:
            t = [x for x in fv([self.lap_rel]) if (getattr(x, 'fajl', None) or '').replace('\\', '/') == self.lap_rel]
        except TypeError:
            self._ci[e] = (None, 'a %s nem fájllistán fut' % e, None)
            return self._ci[e]
        except Exception as ex:  # noqa: BLE001
            self._ci[e] = (None, '%s: %s' % (type(ex).__name__, ex), None)
            return self._ci[e]
        szint = sorted({getattr(x, 'szint', '') for x in t})
        self._ci[e] = ((not t), ('%d találat (%s)' % (len(t), ', '.join(szint))) if t else 'nincs találat',
                       'HIBA' in szint)
        return self._ci[e]

    def allitas_eredmeny(self):
        if 'allitas' not in self._ci:
            import allitas_adat as AA
            e = AA.meres(self.mid)
            if e['hiba']:
                self._ci['allitas'] = (None, e['hiba'], None)
            else:
                minden = e['lap'] + e['melleklet']
                n = sum(1 for r in minden if r.allapot == AA.ELTER)
                mert = sum(1 for r in minden if r.allapot != AA.NEM_MERHETO)
                if not mert:   # csupa nem mérhető (vagy semmi): se teljesülés, se nem teljesülés
                    self._ci['allitas'] = (None, 'nincs mért állítás', None)
                else:
                    self._ci['allitas'] = ((n == 0), '%d állítás eltér az adattól' % n if n else
                                           '%d mért állítás, nincs eltérés' % mert, bool(n))
        return self._ci['allitas']

    def olvasoi_egesz_eredmeny(self):
        if not os.path.exists(os.path.join(GYOKER, self.lap_rel)):
            return None, 'nincs lap', None
        t = [x for x in self.olvasoi() if x['sulyossag'] == 'BUKÁS']
        return (not t), ('%d BUKÁS' % sum(x.get('db', 1) for x in t)) if t else '0 BUKÁS', bool(t)

    def eredmeny(self, sz):
        if sz.tipus == 'olvasoi_egesz':
            return self.olvasoi_egesz_eredmeny()
        if sz.tipus == 'allitas':
            return self.allitas_eredmeny()
        if sz.tipus == 'olvasoi':
            return self.olvasoi_eredmeny(sz.azon)
        if sz.tipus == 'visszhang':
            return self.visszhang_eredmeny(sz.azon)
        if sz.tipus == 'ellenoriz':
            return self.ellenoriz_eredmeny(sz.azon)
        return self.ci_eredmeny(sz.azon)


# ---------------------------------------------------------------------------
# Mérés és jelentés
# ---------------------------------------------------------------------------

Meres = collections.namedtuple('Meres', 'sor osztaly teljesul reszletek megjegyzes kemeny')


def _lista_allapot(allapot):
    """A „HAMART-állapot” cella első kiemelt szava: 'teljesül' / 'nem teljesül' / 'részben' / ''."""
    m = re.match(r'\*\*([^*]+)\*\*', allapot.strip())
    return m.group(1).strip().lower() if m else ''


def meres(mid, sorok=None, e28=False, futtato=None):
    sorok = sorok if sorok is not None else lista_sorai()
    f = futtato or Futtato(mid, e28=e28)
    olv = _olvasoi_azonositok()
    ki = []
    for s in sorok:
        osztaly, szab, megj = szabalyok_a_cellabol(s.ellenorzes, olv)
        if osztaly != GEPI:
            ki.append(Meres(s, osztaly, None, [], megj, None))
            continue
        reszletek = []
        for sz in szab:
            ok, uz, kemeny = f.eredmeny(sz)
            reszletek.append((sz, ok, uz, kemeny))
        gyujtott = [r for r in reszletek if r[1] is not None]
        if not gyujtott:
            ki.append(Meres(s, NEM_GYUJTHETO, None, reszletek, megj, None))
            continue
        teljesul = all(r[1] for r in gyujtott)
        kemeny = None if teljesul else any(r[3] for r in gyujtott if r[1] is False)
        ki.append(Meres(s, GEPI, teljesul, reszletek, megj, kemeny))
    return ki


def _szab_nev(sz):
    return {'olvasoi': '%s', 'olvasoi_egesz': 'olvasói kapu (%s)', 'visszhang': 'VISSZHANG %s', 'ellenoriz': 'ellenoriz.py %s.', 'ci': 'CI %s',
            'allitas': 'állítás–adat kapu (%s)'}[sz.tipus] % sz.azon


def _nevelo(n):
    """A névelő a szám kiejtése szerint: „az 1”, „az 5”, „az 50”, „az 1000”, de „a 10”, „a 100”."""
    s = str(n)
    return 'az' if s[0] == '5' or (s[0] == '1' and len(s) in (1, 4)) else 'a'


def osszegzo_sor(mid, eredmeny):
    """„HAMART-001: N/M követelmény teljesül (gépi)”, és ha van nem teljesülő: hány gátló szintű, hány csak
    figyelmeztetés (FIGYELMEZTETÉS vagy JELENTÉS)."""
    gepi = [m for m in eredmeny if m.osztaly == GEPI]
    nem = [m for m in gepi if not m.teljesul]
    sor = '%s: %d/%d követelmény teljesül (gépi)' % (mid, len(gepi) - len(nem), len(gepi))
    if nem:
        kem = sum(1 for m in nem if m.kemeny)
        sor += ' — %s %d nem teljesülőből %d gátló szintű, %d csak figyelmeztetés' % (
            _nevelo(len(nem)), len(nem), kem, len(nem) - kem)
    return sor


def jelentes(mid, eredmeny, hamart_osszevetes=None):
    if hamart_osszevetes is None:
        hamart_osszevetes = (mid == 'HAMART-001')
    gepi = [m for m in eredmeny if m.osztaly == GEPI]
    nem = [m for m in gepi if not m.teljesul]
    ember = [m for m in eredmeny if m.osztaly == EMBER]
    ngy = [m for m in eredmeny if m.osztaly == NEM_GYUJTHETO]
    ki = ['## %s' % osszegzo_sor(mid, eredmeny), '',
          '%d K-sor: %d gépi szabállyal mérve (ebből %d csak részben: a cella lektori, „grep” vagy „nincs” részét a '
          'gép nem méri), %d ember ellenőrzi, %d gépi, de a kapu nem gyűjti.'
          % (len(eredmeny), len(gepi), sum(1 for m in gepi if (m.megjegyzes or '').startswith('részben gépi')),
             len(ember), len(ngy)), '']
    if nem:
        ki += ['**Nem teljesül (gépi):**', '',
               '| K | Blokk | Szint | Szabály: eredmény |' + (' A lista szerint |' if hamart_osszevetes else ''),
               '|---|---|---|---|' + ('---|' if hamart_osszevetes else '')]
        for m in sorted(nem, key=lambda x: not x.kemeny):
            sz = '; '.join('%s: %s' % (_szab_nev(sz), uz) for sz, ok, uz, _k in m.reszletek if ok is False)
            ki.append('| %s | %s | %s | %s |%s' % (
                m.sor.k, m.sor.blokk, 'gátló' if m.kemeny else 'figyelmeztetés', sz.replace('|', '\\|'),
                (' %s |' % (_lista_allapot(m.sor.allapot) or '—')) if hamart_osszevetes else ''))
        ki.append('')
    if hamart_osszevetes:
        elter = [m for m in gepi if m.teljesul and _lista_allapot(m.sor.allapot) in ('nem teljesül',)]
        elter += [m for m in gepi if not m.teljesul and _lista_allapot(m.sor.allapot) == 'teljesül']
        if elter:
            ki += ['**A lista „HAMART-állapot” oszlopa és a gépi mérés eltér** (a lista a #182 egy korábbi commitján '
                   'mért, és a figyelmeztetést nem számolja nem teljesülésnek): %s.' % ', '.join(
                       '%s (lista: %s, gép: %s)' % (m.sor.k, _lista_allapot(m.sor.allapot),
                                                   'teljesül' if m.teljesul else 'nem teljesül, ' +
                                                   ('gátló' if m.kemeny else 'figyelmeztetés')) for m in elter), '']
    if ngy:
        ki += ['<details><summary>Gépi, de a kapu nem gyűjti (%d)</summary>' % len(ngy), '']
        for m in ngy:
            ok = '; '.join('%s: %s' % (_szab_nev(sz), uz) for sz, _o, uz, _k in m.reszletek) or m.megjegyzes
            ki.append('- %s — %s' % (m.sor.k, ok))
        ki += ['', '</details>', '']
    ki += ['<details><summary>Ember ellenőrzi (%d)</summary>' % len(ember), '',
           ', '.join('%s (%s)' % (m.sor.k, m.megjegyzes) for m in ember), '', '</details>', '']
    return '\n'.join(ki)


def main(argv=None):
    ap = argparse.ArgumentParser(description='Követelménylista-kapu (F196): a K-sorok gépi szabályai egy lapra, JELENTÉS.')
    ap.add_argument('id', nargs='*', default=['HAMART-001'], help='motívum-azonosító(k); alap: HAMART-001')
    ap.add_argument('--e28', action='store_true', help='az E28 (generátor-futtatás, lassú) is fusson')
    ap.add_argument('--szigoru', action='store_true',
                    help='gátló szintű nem teljesülő gépi sornál 1-es kilépési kód (a kapuemelési döntés: a figyelmeztetés JELENTÉS)')
    args = ap.parse_args(argv)
    sorok = lista_sorai()
    print('# Követelménylista-kapu (F196, E39)\n')
    print('*Forrás: `sablonok/KESZ_LAP_KOVETELMENY.md` (%d K-sor). Szint: a CI-ben E39 (a kapuemelési döntés): a gátló szintű hiány HIBA, a figyelmeztetés JELENTÉS; a befagyasztott lap kimarad.*\n' % len(sorok))
    van_nem = False
    eredmenyek = []
    import lap_befagyasztas
    fagy = lap_befagyasztas.befagyasztott_idk()
    for mid in args.id:
        if mid in fagy:   # F212 (a kapuemelési döntés): a befagyasztott lapot az E28 jelölésével kihagyja
            print('%s: befagyasztva, nem mérve (adat/lap_befagyasztas.tsv)\n' % mid)
            continue
        e = meres(mid, sorok, e28=args.e28)
        eredmenyek.append((mid, e))
        # F212 (a kapuemelési döntés): szigorú módban csak a gátló szintű hiány bukik; a figyelmeztetés jelentés marad
        van_nem = van_nem or any(m.osztaly == GEPI and not m.teljesul and m.kemeny for m in e)
    for mid, e in eredmenyek:
        print(osszegzo_sor(mid, e))
    print()
    for mid, e in eredmenyek:
        print(jelentes(mid, e))
    return 1 if (args.szigoru and van_nem) else 0


if __name__ == '__main__':
    sys.exit(main())
