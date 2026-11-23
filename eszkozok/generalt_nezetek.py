#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generalt_nezetek.py -- F217: a generált nézetek jegyzékének (`adat/generalt_nezetek.tsv`) végrehajtója.

A generált nézeteket (lexikonlap, marker-blokkok, nyílt mag) nem az ágak commitolják: a main-en a
`feladatok.yml` ezt a szkriptet hívja (`--ir`), és egy gépi commitban írja vissza; a PR-ban a CI ugyanígy,
ideiglenesen generál a munkapéldányán, és a kapuk a friss nézeten futnak (naplok/F217_terv.md 3. pont).
A `szamkiosztas_ujragen.py` (F201) utódja.

**Egyetlen belépési pont a lapgenerátorhoz** (F217, az F218a-val párhuzamos feltétel): a lapot minden fogyasztó
(ez a szkript, az E28, a kiadás és a lapjavítás helyi átnézése) a `lexikon_general()` függvényen át generálja,
amely a jegyzék G01-sorának `parancs` mezőjét futtatja. A generátor cseréjekor csak ez a mező változik.

Módok:
  --lista          a futtatandó sorok sorrendje (az `utana` szerint), írás nélkül
  --ellenoriz      a jegyzék kapuja (oszlopok, értékek, hivatkozások, körmentesség, futtatható parancs)
  --ir             a repóba ír (main: az Action; PR: a CI munkapéldánya); előbb ideiglenes gyökérbe generál,
                   hiba esetén mindent visszaállít (nem ír félig)
  --gyoker DIR     átnézés: csak a lapokat generálja a DIR alá (a repón kívül), a repóba nem ír
  --jelentes FILE  Markdown-jelentés: mely nézet változott, és melyik őrzött lap változna
  --kapuk          a friss nézeten a jegyzék `kapuk` mezőjében megnevezett, lemezt olvasó kapuk (E29, E38, E39,
                   olvasói kapu); a main-en a commit előtt fut

Dátumszabály (GK-B9, F217.3a): a lap először a commitolt lap `ts=` dátumával generálódik; ha így bájtra azonos,
a lap marad. Ha eltér, a HEAD commit dátumával (UTC) generálódik újra, így az újrafuttatás ugyanazt adja.

Őrzött lap (3.4): a kiadott lap (sora van az `adat/kiadasok.tsv`-ben) tartalma csak akkor változhat, ha
(a) az utolsó lap-commit óta új `kiadasok.tsv`-sor jött rá, (b) a különbség csak a DT-szám (számkiosztás), vagy
(c) az utolsó lap-commit óta új `lap_javitasok.tsv`-sor jött rá. Különben a lap nem íródik ki, a kilépési kód 2.

Kilépési kód: 0 rendben; 1 generálási vagy jegyzékhiba (semmi nem íródott); 2 őrzött lap változna (a többi
nézet kiíródott, az őrzött lap nem); 3 kapuhiba (`--kapuk`).

CLI:
    python eszkozok/generalt_nezetek.py --lista
    python eszkozok/generalt_nezetek.py --ellenoriz
    python eszkozok/generalt_nezetek.py --ir [--jelentes FILE]
    python eszkozok/generalt_nezetek.py --gyoker <tmp> [--id HAMART-001] [--jelentes FILE]
    python eszkozok/generalt_nezetek.py --kapuk
"""

import argparse
import datetime
import os
import re
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JEGYZEK = 'adat/generalt_nezetek.tsv'
BEMENETI_JEGYZEK = 'adat/lapgen_bemenetek.tsv'   # a lapgenerátor bemeneti jegyzéke (F218a, #729); a B-sorok gazdája
REGI_LISTA = 'eszkozok/ellenorzes/e28_migralt_nezetek.tsv'   # kivezetve (F217.6): adatsor nem állhat benne
LAP_SOR = 'G01'   # a lapgenerátor sora: az egyetlen belépési pont (lexikon_general)

OSZLOPOK = ['id', 'utvonal', 'leiras', 'parancs', 'bemenetek', 'utana', 'orzes', 'determinizmus', 'kapuk',
            'gazda', 'futtato', 'allapot', 'forras']
ORZES = {'szabad', 'befagyasztas', 'kiadas'}
DETERMINIZMUS = {'det', 'det:PARDES_DATUM', 'nemdet'}
GAZDA = {'action', 'ag'}
FUTTATO = {'jegyzek', 'workflow', 'kezi'}
ALLAPOT = {'aktiv', 'kimarad'}
KAPU_NEVEK = {'E18', 'E28', 'E29', 'E35', 'E38', 'E39', 'olvasoi_kapu'}
_ID = re.compile(r'^G\d{2,3}$')
_B = re.compile(r'^!?B\d{2,3}$')
_B_TARTOMANY = re.compile(r'^B(\d{2,3})\.\.B(\d{2,3})$')
_TS = re.compile(r'GENERÁLT[^\n]*?\bts=(\d{4}-\d{2}-\d{2})')
_DT = re.compile(r'\bDT-?F?\d+[a-z]?\b')
# az olvasói szövegben a DT-szám helyén „szerkesztői döntés”, végleges számnál a feloldott dátummal
# (lexikon_general: _DT_RX → dontes_datum); a számkiosztás ezt a dátumot is hozza (3.4 (b))
_DT_DATUM = re.compile(r'szerkesztői döntés(?:, \d{4}-\d{2}-\d{2})?')


def _dt_norm(szoveg):
    return _DT_DATUM.sub('szerkesztői döntés#', _DT.sub('DT#', szoveg))


# ---------------------------------------------------------------------------
# A jegyzék olvasása és kapuja
# ---------------------------------------------------------------------------

def _sorok(ut):
    """(fejlec, [(fajl_sorszam, {oszlop: ertek})]) -- `#` kezdetű sor a fejléc előtt megjegyzés.
    A TSV olvasása split('\\t') (CLAUDE.md, „TSV-olvasás”)."""
    with open(ut, 'rb') as f:
        sorok = f.read().decode('utf-8').split('\n')
    fej, ki = None, []
    for n, s in enumerate(sorok, start=1):
        s = s.rstrip('\r')
        if not s.strip():
            continue
        if fej is None:
            if s.startswith('#'):
                continue
            fej = s.split('\t')
            continue
        ki.append((n, dict(zip(fej, s.split('\t')))))
    return fej or [], ki


def jegyzek(gyoker=ROOT):
    """[(fajl_sorszam, sor)] a jegyzék sorai."""
    return _sorok(os.path.join(gyoker, *JEGYZEK.split('/')))[1]


def sor(azon, gyoker=ROOT):
    for _, d in jegyzek(gyoker):
        if d.get('id') == azon:
            return d
    raise KeyError('a jegyzékben nincs %s sor' % azon)


def _lista(mezo):
    mezo = (mezo or '').strip()
    if mezo in ('', '-'):
        return []
    return [x.strip() for x in mezo.split(';') if x.strip()]


def b_azonositok(gyoker=ROOT):
    """A bemeneti jegyzék B-azonosítói, vagy None, ha a jegyzék még nincs a repóban (a #729 előtt)."""
    ut = os.path.join(gyoker, *BEMENETI_JEGYZEK.split('/'))
    if not os.path.exists(ut):
        return None
    return {d.get('id', '').strip() for _, d in _sorok(ut)[1]}


def sorrend(sorok):
    """A sorok topologikus sorrendje az `utana` szerint (stabil: a jegyzék sorrendjén belül).
    ValueError, ha kör van."""
    by_id = {d['id']: d for d in sorok}
    kesz, ki, folyamatban = set(), [], set()

    def latogat(azon, ut):
        if azon in kesz:
            return
        if azon in folyamatban:
            raise ValueError('kör az `utana` mezőben: %s' % ' -> '.join(ut + [azon]))
        folyamatban.add(azon)
        for elozo in _lista(by_id[azon].get('utana')):
            if elozo in by_id:
                latogat(elozo, ut + [azon])
        folyamatban.discard(azon)
        kesz.add(azon)
        ki.append(by_id[azon])

    for d in sorok:
        latogat(d['id'], [])
    return ki


def jegyzek_ellenoriz(gyoker=ROOT):
    """A jegyzék kapuja: [hibaüzenet]. Üres lista = rendben."""
    hibak = []
    ut = os.path.join(gyoker, *JEGYZEK.split('/'))
    if not os.path.exists(ut):
        return ['%s: nincs meg' % JEGYZEK]
    fej, sorok = _sorok(ut)
    if fej != OSZLOPOK:
        return ['%s: a fejléc %r, elvárt %r' % (JEGYZEK, fej, OSZLOPOK)]
    b_idk = b_azonositok(gyoker)
    idk = [d.get('id', '') for _, d in sorok]
    for n, d in sorok:
        h = lambda uz: hibak.append('%s %d. sor (%s): %s' % (JEGYZEK, n, d.get('id', '?'), uz))
        if len(d) != len(OSZLOPOK) or any(v is None for v in d.values()):
            h('a mezők száma nem %d' % len(OSZLOPOK))
            continue
        for o in OSZLOPOK:
            if not d[o].strip():
                h('üres mező: %s (üres helyett `-`)' % o)
        if not _ID.match(d['id']):
            h('az id nem ^G\\d{2,3}$')
        if idk.count(d['id']) > 1:
            h('ismétlődő id')
        for o in _lista(d['orzes']):
            if o not in ORZES:
                h('ismeretlen orzes: %s' % o)
        if d['determinizmus'] not in DETERMINIZMUS:
            h('ismeretlen determinizmus: %s' % d['determinizmus'])
        if d['gazda'] not in GAZDA:
            h('ismeretlen gazda: %s' % d['gazda'])
        if d['futtato'] not in FUTTATO:
            h('ismeretlen futtato: %s' % d['futtato'])
        if d['allapot'] not in ALLAPOT:
            h('ismeretlen allapot: %s' % d['allapot'])
        for k in _lista(d['kapuk']):
            if k not in KAPU_NEVEK:
                h('ismeretlen kapu: %s' % k)
        for b in _lista(d['bemenetek']):
            if b == 'B*':
                continue
            if b.startswith('G'):
                if b not in idk:
                    h('a bemenet nem létező sorra mutat: %s' % b)
                continue
            m = _B_TARTOMANY.match(b)
            if not m and not _B.match(b):
                h('hibás bemenet-hivatkozás: %s (B<nn>, !B<nn>, B<nn>..B<nn>, B*, G<nn>)' % b)
                continue
            if b_idk is not None and not m and b.lstrip('!') not in b_idk:
                h('a bemenet nincs a %s-ben: %s' % (BEMENETI_JEGYZEK, b))
        for u in _lista(d['utana']):
            if u not in idk:
                h('az utana nem létező sorra mutat: %s' % u)
        if d['determinizmus'] == 'nemdet' and d['gazda'] == 'action' and d['allapot'] == 'aktiv':
            h('nem determinisztikus nézetet a main-en az Action nem írhat (gazda=action, allapot=aktiv)')
        if d['gazda'] == 'action' and d['futtato'] == 'jegyzek' and d['allapot'] == 'aktiv':
            p = d['parancs'].strip()
            if p.startswith('='):
                if p[1:] not in idk:
                    h('a parancs nem létező sorra mutat: %s' % p)
            else:
                szkript = _szkript(p)
                if not szkript or not os.path.exists(os.path.join(gyoker, *szkript.split('/'))):
                    h('a parancs nem futtatható szkriptre mutat: %s' % p)
    try:
        sorrend([d for _, d in sorok])
    except (ValueError, KeyError) as e:
        hibak.append('%s: %s' % (JEGYZEK, e))
    hibak.extend(regi_lista_ellenoriz(gyoker))
    return hibak


def regi_lista_ellenoriz(gyoker=ROOT):
    """A kivezetett E28-lista (F217.6) nem lehet párhuzamos forrás: adatsor nem állhat benne."""
    ut = os.path.join(gyoker, *REGI_LISTA.split('/'))
    if not os.path.exists(ut):
        return []
    _, sorok = _sorok(ut)
    if sorok:
        return ['%s: kivezetve (F217), adatsor nem állhat benne (%d sor); a lapok listája: %s %s'
                % (REGI_LISTA, len(sorok), JEGYZEK, LAP_SOR)]
    return []


def _szkript(parancs):
    """A parancs első `.py` tagja (repó-relatív)."""
    for tag in parancs.split():
        if tag.endswith('.py'):
            return tag
    return None


# ---------------------------------------------------------------------------
# A lapok halmaza, a dátum, az őrzés
# ---------------------------------------------------------------------------

def befagyasztott_idk(gyoker=ROOT):
    eszkozok = os.path.join(ROOT, 'eszkozok')
    if eszkozok not in sys.path:
        sys.path.insert(0, eszkozok)
    import lap_befagyasztas
    return lap_befagyasztas.befagyasztott_idk(os.path.join(gyoker, 'adat', 'lap_befagyasztas.tsv'))


def _lap_ut(minta, azon):
    return minta.replace('<ID>', azon)


def aktiv_lapok(gyoker=ROOT):
    """A G01 ID-halmaza: van `motivumok/<ID>.md` és commitolt lap, és a lap nincs befagyasztva.
    (Az új cikk lapját az ág egyszer, a születésekor commitolja; onnan a main-en az Action tartja karban.)"""
    fagy = befagyasztott_idk(gyoker)
    return [a for a in _lapos_forrasok(gyoker) if a not in fagy]


def _lapos_forrasok(gyoker):
    """Az ID-k, amelyeknek van `motivumok/<ID>.md` forrása és commitolt lapja (G01-útvonal)."""
    minta = sor(LAP_SOR, gyoker)['utvonal']
    ki = []
    mdir = os.path.join(gyoker, 'motivumok')
    if not os.path.isdir(mdir):
        return ki
    for nev in sorted(os.listdir(mdir)):
        if not nev.endswith('.md'):
            continue
        azon = nev[:-3]
        if os.path.exists(os.path.join(gyoker, *_lap_ut(minta, azon).split('/'))):
            ki.append(azon)
    return ki


def migralt_lapok(gyoker=ROOT):
    """A forrásból generált (migrált vagy új) lapok a befagyasztottakkal együtt: van forrás és lap, és nincs
    törzscikk (a migráció archiválta, D6). Az E29 hatóköre: a befagyasztott lap kimenete is kiadható kimenet."""
    return [a for a in _lapos_forrasok(gyoker)
            if not os.path.exists(os.path.join(gyoker, 'lexikon', a + '_TORZSCIKK.md'))]


def lap_fajlok(azon, gyoker=ROOT):
    """A G01 hívása által előállított aktív nézetek repó-relatív útja (G01 és a `=G01` parancsú sorok)."""
    ki = []
    for _, d in jegyzek(gyoker):
        if d['allapot'] != 'aktiv':
            continue
        if d['id'] == LAP_SOR or d['parancs'].strip() == '=' + LAP_SOR:
            ki.append(_lap_ut(d['utvonal'], azon))
    return ki


def lap_datuma(szoveg):
    m = _TS.search(szoveg or '')
    return m.group(1) if m else None


def head_datum(gyoker=ROOT):
    """A HEAD commit dátuma UTC-ben (YYYY-MM-DD); git nélkül a mai nap (UTC)."""
    try:
        p = subprocess.run(['git', 'log', '-1', '--format=%ct'], cwd=gyoker, capture_output=True, check=True)
        ts = int(p.stdout.decode().strip())
        return datetime.datetime.fromtimestamp(ts, datetime.timezone.utc).date().isoformat()
    except (subprocess.CalledProcessError, OSError, ValueError):
        return datetime.datetime.now(datetime.timezone.utc).date().isoformat()


def _olvas(ut):
    try:
        with open(ut, 'rb') as f:
            return f.read().decode('utf-8')
    except OSError:
        return None


def _lf(s):
    return None if s is None else s.replace('\r\n', '\n')


def _git_show(gyoker, rev, relut):
    try:
        p = subprocess.run(['git', 'show', '%s:%s' % (rev, relut)], cwd=gyoker, capture_output=True, check=True)
        return p.stdout.decode('utf-8')
    except (subprocess.CalledProcessError, OSError):
        return None


def _id_sorszam(szoveg, azon):
    if szoveg is None:
        return 0
    n = 0
    for s in szoveg.split('\n'):
        if s.startswith('#'):
            continue
        if s.split('\t')[0].strip() == azon:
            n += 1
    return n


def kiadott(azon, gyoker=ROOT):
    return _id_sorszam(_olvas(os.path.join(gyoker, 'adat', 'kiadasok.tsv')), azon) > 0


def orzes_sertes(azon, relut, commitolt, generalt, gyoker=ROOT):
    """None, ha a kiadott lap változása megengedett (vagy nincs változás); különben az ok szövege (3.4)."""
    commitolt, generalt = _lf(commitolt), _lf(generalt)
    if commitolt is None or commitolt == generalt:
        return None
    if not kiadott(azon, gyoker):
        return None
    if _dt_norm(commitolt) == _dt_norm(generalt):
        return None   # (b) számkiosztás: csak a DT-szám változott
    try:
        p = subprocess.run(['git', 'log', '-1', '--format=%H', '--', relut], cwd=gyoker,
                           capture_output=True, check=True)
        utolso = p.stdout.decode().strip()
    except (subprocess.CalledProcessError, OSError):
        utolso = ''
    if utolso:
        for tabla in ('adat/kiadasok.tsv', 'adat/lap_javitasok.tsv'):
            most = _id_sorszam(_olvas(os.path.join(gyoker, *tabla.split('/'))), azon)
            akkor = _id_sorszam(_git_show(gyoker, utolso, tabla), azon)
            if most > akkor:
                return None   # (a) új kiadás, (c) új lapjavítás-sor az utolsó lap-commit óta
    return ('a kiadott lap (%s) tartalma változna új kiadás nélkül: nincs új adat/kiadasok.tsv- vagy '
            'adat/lap_javitasok.tsv-sor az utolsó lap-commit óta, és a különbség nem csak DT-szám. '
            'Út: /kiadas %s (új kiadás) vagy /lap-javit %s (javítás kiadás nélkül)' % (relut, azon, azon))


# ---------------------------------------------------------------------------
# Az egyetlen belépési pont a lapgenerátorhoz
# ---------------------------------------------------------------------------

def _parancs(sablon, **helyorzok):
    tagok = []
    for tag in sablon.split():
        for k, v in helyorzok.items():
            tag = tag.replace('{%s}' % k, v)
        tagok.append(tag)
    if tagok and tagok[0] == 'python':
        tagok[0] = sys.executable
    return tagok


def _futtat(tagok, cwd, env_kieg=None):
    env = dict(os.environ, PYTHONIOENCODING='utf-8', **(env_kieg or {}))
    p = subprocess.run(tagok, cwd=cwd, env=env, capture_output=True)
    return p.returncode, (p.stdout.decode('utf-8', errors='replace')[-1500:]
                          + p.stderr.decode('utf-8', errors='replace')[-1500:])


def lexikon_general(azon, kimenet, datum, gyoker=ROOT):
    """A lap generálása a `kimenet` könyvtár alá (a repó szerkezete szerint), `PARDES_DATUM=datum`-mal.
    Az EGYETLEN belépési pont a lapgenerátorhoz: a jegyzék G01-sorának parancsát futtatja.
    (kilépési kód, kimenet-részlet)."""
    sablon = sor(LAP_SOR, gyoker)['parancs']
    # F241.2: a kiadott lap kiadás módban generálódik (a Kolofon jóváhagyás-mondata és a GK-27 kapuja), a többi munka
    # módban
    tagok = _parancs(sablon, id=azon, gyoker=kimenet, mod='kiadas' if kiadott(azon, gyoker) else 'munka')
    return _futtat(tagok, gyoker, {'PARDES_DATUM': datum})


def lap_ujragen(azon, gyoker=ROOT, forras_gyoker=None):
    """Egy lap újragenerálása a dátumszabállyal, írás nélkül.
    {relut: (commitolt, generalt)} vagy RuntimeError. A `commitolt` a munkafa-fájl (None: új lap)."""
    forras_gyoker = forras_gyoker or gyoker
    fajlok = lap_fajlok(azon, gyoker)
    regi = {r: _olvas(os.path.join(forras_gyoker, *r.split('/'))) for r in fajlok}
    datum0 = lap_datuma(regi.get(fajlok[0])) or head_datum(gyoker)
    eredmeny = _general_tmp(azon, datum0, fajlok, gyoker)
    valtozott = any(_lf(regi[r]) != _lf(eredmeny.get(r)) for r in fajlok)
    hd = head_datum(gyoker)
    if valtozott and datum0 != hd:
        eredmeny = _general_tmp(azon, hd, fajlok, gyoker)   # dátumszabály: tartalomváltozáskor a HEAD dátuma
        eredmeny['__regi_datummal__'] = _general_tmp(azon, datum0, fajlok, gyoker)
    return regi, eredmeny


def _general_tmp(azon, datum, fajlok, gyoker):
    tmp = tempfile.mkdtemp(prefix='gn_')
    try:
        kod, uz = lexikon_general(azon, tmp, datum, gyoker)
        if kod != 0:
            raise RuntimeError('%s: a lapgenerátor hibával állt le (kód %d): %s' % (azon, kod, uz.strip()[-400:]))
        ki = {}
        for r in fajlok:
            ki[r] = _olvas(os.path.join(tmp, *r.split('/')))
        if ki.get(fajlok[0]) is None:
            raise RuntimeError('%s: a lapgenerátor nem állította elő: %s' % (azon, fajlok[0]))
        return ki
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# Végrehajtás
# ---------------------------------------------------------------------------

def futtatando(gyoker=ROOT):
    """Az aktív, `gazda=action`, `futtato=jegyzek` sorok az `utana` szerinti sorrendben."""
    sorok = [d for _, d in jegyzek(gyoker)
             if d['allapot'] == 'aktiv' and d['gazda'] == 'action' and d['futtato'] == 'jegyzek']
    return sorrend(sorok)


def _celfajlok(d, gyoker, lapok):
    """A sor által írt repó-relatív fájlok (a pillanatképhez)."""
    ut = d['utvonal'].split('#')[0].strip()
    if '<ID>' in ut:
        return [_lap_ut(ut, a) for a in lapok]
    if ut.endswith('/'):
        ki = []
        for gy, _, nevek in os.walk(os.path.join(gyoker, *ut.rstrip('/').split('/'))):
            for n in nevek:
                ki.append(os.path.relpath(os.path.join(gy, n), gyoker).replace('\\', '/'))
        return ki
    return [ut]


def _pillanatkep(relutak, gyoker):
    return {r: (open(os.path.join(gyoker, *r.split('/')), 'rb').read()
                if os.path.exists(os.path.join(gyoker, *r.split('/'))) else None) for r in relutak}


def _visszaallit(kep, gyoker, uj_fajlok=()):
    for r, tartalom in kep.items():
        ut = os.path.join(gyoker, *r.split('/'))
        if tartalom is None:
            if os.path.exists(ut):
                os.remove(ut)
        else:
            os.makedirs(os.path.dirname(ut), exist_ok=True)
            with open(ut, 'wb') as f:
                f.write(tartalom)
    for r in uj_fajlok:
        if r not in kep:
            ut = os.path.join(gyoker, *r.split('/'))
            if os.path.exists(ut):
                os.remove(ut)


def _ir_fajl(gyoker, relut, szoveg):
    ut = os.path.join(gyoker, *relut.split('/'))
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'wb') as f:
        f.write(szoveg.encode('utf-8'))


def _konyvtar_szinkron(forras, cel):
    """A `cel` könyvtár tartalma = a `forras`-é (új és változott fájl másolva, a hiányzó törölve).
    A változott repó-relatív utak listája."""
    valt = []
    uj = {}
    for gy, _, nevek in os.walk(forras):
        for n in nevek:
            uj[os.path.relpath(os.path.join(gy, n), forras).replace('\\', '/')] = os.path.join(gy, n)
    regi = set()
    if os.path.isdir(cel):
        for gy, _, nevek in os.walk(cel):
            for n in nevek:
                regi.add(os.path.relpath(os.path.join(gy, n), cel).replace('\\', '/'))
    for rel, src in uj.items():
        dst = os.path.join(cel, *rel.split('/'))
        a = open(src, 'rb').read()
        b = open(dst, 'rb').read() if os.path.exists(dst) else None
        # a sorvég nem tartalmi eltérés (core.autocrlf=true munkapéldány): a git úgyis normalizál
        if b is None or a.replace(b'\r\n', b'\n') != b.replace(b'\r\n', b'\n'):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            with open(dst, 'wb') as f:
                f.write(a)
            valt.append(rel)
    for rel in regi - set(uj):
        os.remove(os.path.join(cel, *rel.split('/')))
        valt.append(rel)
    return valt


def ir(gyoker=ROOT, csak_id=None):
    """A jegyzék végrehajtása a repóba. (kód, jelentés-sorok)."""
    jel = []
    hibak = jegyzek_ellenoriz(gyoker)
    if hibak:
        return 1, ['## Jegyzékhiba', ''] + ['- %s' % h for h in hibak]
    lapok = aktiv_lapok(gyoker)
    if csak_id:
        lapok = [a for a in lapok if a in csak_id]
    sorok = futtatando(gyoker)
    kep = _pillanatkep(sorted({r for d in sorok for r in _celfajlok(d, gyoker, lapok)}), gyoker)
    uj_fajlok, sertesek, valtozott = [], [], []
    try:
        for d in sorok:
            p = d['parancs'].strip()
            if p.startswith('='):
                continue   # a hivatkozott sor hívása állítja elő
            if d['id'] == LAP_SOR:
                for azon in lapok:
                    regi, gen = lap_ujragen(azon, gyoker)
                    regi_datummal = gen.pop('__regi_datummal__', gen)
                    fajlok = lap_fajlok(azon, gyoker)
                    if all(_lf(regi[r]) == _lf(gen.get(r)) for r in fajlok):
                        jel.append('- %s: nem változott' % azon)
                        continue
                    ok = None
                    if 'kiadas' in _lista(d['orzes']):
                        for r in fajlok:
                            ok = ok or orzes_sertes(azon, r, regi[r], regi_datummal.get(r), gyoker)
                    if ok:
                        sertesek.append(ok)
                        jel.append('- %s: **ŐRZÖTT LAP, NEM ÍRÓDOTT KI**: %s' % (azon, ok))
                        continue
                    for r in fajlok:
                        if gen.get(r) is not None and _lf(regi[r]) != _lf(gen[r]):
                            if regi[r] is None:
                                uj_fajlok.append(r)
                            _ir_fajl(gyoker, r, gen[r])
                            valtozott.append(r)
                    jel.append('- %s: újragenerálva (%s)' % (azon, ', '.join(fajlok)))
                continue
            if '{gyoker}' in p:
                tmp = tempfile.mkdtemp(prefix='gn_')
                try:
                    kod, uz = _futtat(_parancs(p, gyoker=tmp), gyoker)
                    if kod != 0:
                        raise RuntimeError('%s: %s hibával állt le (kód %d): %s' % (d['id'], p, kod, uz.strip()[-400:]))
                    ut = d['utvonal'].strip()
                    if ut.endswith('/'):
                        v = _konyvtar_szinkron(os.path.join(tmp, *ut.rstrip('/').split('/')),
                                               os.path.join(gyoker, *ut.rstrip('/').split('/')))
                        valtozott.extend(ut + r for r in v)
                        uj_fajlok.extend(ut + r for r in v)
                        jel.append('- %s (%s): %d fájl változott' % (d['id'], ut, len(v)))
                    else:
                        raise RuntimeError('%s: a {gyoker} csak könyvtár-kimenettel támogatott' % d['id'])
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)
                continue
            # marker-blokk: a generátor a repóban, helyben ír (idempotens; hiba esetén a pillanatkép áll vissza)
            elotte = _pillanatkep(_celfajlok(d, gyoker, lapok), gyoker)
            kod, uz = _futtat(_parancs(p), gyoker)
            if kod != 0:
                raise RuntimeError('%s: %s hibával állt le (kód %d): %s' % (d['id'], p, kod, uz.strip()[-400:]))
            utana = _pillanatkep(list(elotte), gyoker)
            v = [r for r in elotte if elotte[r] != utana[r]]
            valtozott.extend(v)
            jel.append('- %s (%s): %s' % (d['id'], d['utvonal'], 'változott' if v else 'nem változott'))
    except Exception as e:   # a hiba nem csendes, és nem marad félig írt nézet
        _visszaallit(kep, gyoker, uj_fajlok)
        return 1, ['## Generálási hiba (minden nézet visszaállítva)', '', '- %s: %s' % (type(e).__name__, e)]
    fej = ['## Generált nézetek (F217)', '',
           'Változott: %s' % (', '.join(sorted(set(valtozott))) if valtozott else 'nincs'), '']
    if sertesek:
        fej += ['**Őrzött lap változna új kiadás nélkül (%d)** — a lap nem íródott ki.' % len(sertesek), '']
    return (2 if sertesek else 0), fej + jel


def gyoker_mod(cel, csak_id=None):
    """Átnézés: a lapok generálása a `cel` könyvtár alá (a repón kívül), a dátumszabállyal. (kód, jelentés)."""
    cel = os.path.abspath(cel)
    try:
        repon_belul = os.path.commonpath([cel, ROOT]) == ROOT
    except ValueError:   # Windows: más meghajtó, tehát a repón kívül
        repon_belul = False
    if repon_belul:
        return 1, ['HIBA: a --gyoker a repón kívüli könyvtár kell legyen: %s' % cel]
    jel = ['## Ideiglenes generálás (átnézés, F217.8)', '']
    lapok = aktiv_lapok(ROOT)
    if csak_id:
        lapok = [a for a in lapok if a in csak_id]
    for azon in lapok:
        try:
            regi, gen = lap_ujragen(azon, ROOT)
        except RuntimeError as e:
            return 1, jel + ['- HIBA: %s' % e]
        gen.pop('__regi_datummal__', None)
        for r, szoveg in gen.items():
            if szoveg is not None:
                _ir_fajl(cel, r, szoveg)
                jel.append('- %s: %s' % (r, 'változott' if _lf(regi.get(r)) != _lf(szoveg) else 'nem változott'))
    return 0, jel


# ---------------------------------------------------------------------------
# Kapuk a friss nézeten (a main-en a commit előtt)
# ---------------------------------------------------------------------------

def kapuk(gyoker=ROOT):
    """A jegyzék aktív soraiban megnevezett, lemezt olvasó kapuk. (kód, jelentés)."""
    nevek = set()
    for _, d in jegyzek(gyoker):
        if d['allapot'] == 'aktiv' and d['gazda'] == 'action':
            nevek.update(_lista(d['kapuk']))
    lapok = aktiv_lapok(gyoker)
    lepesek = []
    if 'E38' in nevek:
        lepesek.append(('E38', [sys.executable, 'eszkozok/ellenorzes/allitas_adat.py', '--minden', '--szigoru']))
    for azon in lapok:
        if 'E39' in nevek:
            lepesek.append(('E39 %s' % azon,
                            [sys.executable, 'eszkozok/ellenorzes/kovetelmeny_kapu.py', azon, '--szigoru']))
        if 'olvasoi_kapu' in nevek:
            lepesek.append(('olvasói kapu %s' % azon, [sys.executable, 'eszkozok/olvasoi_kapu.py', azon]))
    jel, kod = ['## Kapuk a friss nézeten (F217.5)', ''], 0
    if 'E29' in nevek:
        h = e29_friss(gyoker, lapok)
        jel.append('- E29: %s' % ('rendben' if not h else 'HIBA (%d): %s' % (len(h), '; '.join(h[:5]))))
        kod = kod or (3 if h else 0)
    for nev, tagok in lepesek:
        k, uz = _futtat(tagok, gyoker)
        jel.append('- %s: %s' % (nev, 'rendben' if k == 0 else 'HIBA (kód %d)' % k))
        if k != 0:
            jel.append('```\n%s\n```' % uz.strip()[-1200:])
            kod = 3
    return kod, jel


def e29_friss(gyoker=ROOT, lapok=None):
    """Az E29 mintái (szabalyok.E29_MINTAK) a friss lapokon: [hely: minta]."""
    eszkozok = os.path.join(ROOT, 'eszkozok')
    for p in (eszkozok, os.path.join(eszkozok, 'ellenorzes')):
        if p not in sys.path:
            sys.path.insert(0, p)
    import szabalyok as SZ
    ki = []
    for azon in (lapok if lapok is not None else aktiv_lapok(gyoker)):
        for r in lap_fajlok(azon, gyoker)[:1]:
            szoveg = _lf(_olvas(os.path.join(gyoker, *r.split('/')))) or ''
            for i, s in enumerate(szoveg.split('\n'), start=1):
                for minta in SZ.E29_MINTAK:
                    if minta in s:
                        ki.append('%s:%d: %s' % (r, i, minta))
    return ki


def pr_generalt_modositas(valtozott, gyoker=ROOT):
    """O4 (F217.6a): a PR által MÓDOSÍTOTT (nem újonnan létrehozott) fájlok közül azok, amelyeket a main-en az Action
    ír (`gazda=action`, egész fájlos kimenet: lap vagy könyvtár). Az új cikk lapját az ág egyszer, a születésekor
    commitolja, ezért a hozzáadott fájl nem számít. A marker-blokkos fájl kézi részét a PR szabadon írja."""
    mintak = []
    for _, d in jegyzek(gyoker):
        if d['gazda'] != 'action' or d['allapot'] != 'aktiv':
            continue
        for ut in d['utvonal'].split(' ; '):
            ut = ut.strip()
            if '#' in ut:
                continue
            if '<ID>' in ut:
                mintak.append(re.compile('^' + re.escape(ut).replace(re.escape('<ID>'), r'[A-Z0-9]+-\d{3}') + '$'))
            elif ut.endswith('/'):
                mintak.append(re.compile('^' + re.escape(ut)))
    return [f for f in valtozott if any(m.match(f.replace('\\', '/')) for m in mintak)]


def celfajlok_mind(gyoker=ROOT):
    """Minden fájl, amelyet az `--ir` írhat (a helyi push előtti kapu pillanatképéhez)."""
    lapok = aktiv_lapok(gyoker)
    return sorted({r for d in futtatando(gyoker) for r in _celfajlok(d, gyoker, lapok)})


def pillanatkep(gyoker=ROOT):
    """A `--ir` által írható fájlok tartalma; a `visszaallit` ezt állítja vissza (a helyi kapu a munkapéldányt nem
    hagyja generált változással)."""
    return _pillanatkep(celfajlok_mind(gyoker), gyoker)


def visszaallit(kep, gyoker=ROOT):
    _visszaallit(kep, gyoker, celfajlok_mind(gyoker))


def main():
    ap = argparse.ArgumentParser(description='F217: a generált nézetek jegyzékének végrehajtója')
    ap.add_argument('--lista', action='store_true')
    ap.add_argument('--ellenoriz', action='store_true')
    ap.add_argument('--ir', action='store_true')
    ap.add_argument('--gyoker')
    ap.add_argument('--id', action='append', help='csak ezekre a lapokra (több is megadható)')
    ap.add_argument('--kapuk', action='store_true')
    ap.add_argument('--jelentes')
    ap.add_argument('--pr-modositott', help='a PR által módosított fájlok listája (soronként); O4: FIGYELMEZTETÉS')
    a = ap.parse_args()
    kod, jel = 0, []
    if a.pr_modositott:
        with open(a.pr_modositott, encoding='utf-8') as f:
            felesleges = pr_generalt_modositas([s.strip() for s in f if s.strip()])
        for r in felesleges:
            # O4: FIGYELMEZTETÉS; az első sikeres main-oldali újragenerálás után HIBA (N-F217a)
            print('::warning file=%s::FIGYELMEZTETES (F217, O4): generált nézet a PR-ban; felesleges, a main-en az '
                  'Action írja (a merge után ütközést okozhat)' % r)
        if not (a.ir or a.lista or a.ellenoriz or a.gyoker or a.kapuk):
            return 0
    if a.lista:
        for d in futtatando():
            jel.append('%s\t%s\t%s' % (d['id'], d['utvonal'], d['parancs']))
        jel.append('lapok (G01): %s' % (', '.join(aktiv_lapok()) or '-'))
    elif a.ellenoriz:
        hibak = jegyzek_ellenoriz()
        jel = ['HIBA: %s' % h for h in hibak] or ['%s: rendben (%d sor)' % (JEGYZEK, len(jegyzek()))]
        if b_azonositok() is None:
            jel.append('megjegyzés: a %s még nincs a repóban, a B-hivatkozások nincsenek ellenőrizve'
                       % BEMENETI_JEGYZEK)
        kod = 1 if hibak else 0
    elif a.ir:
        kod, jel = ir(csak_id=a.id)
    elif a.gyoker:
        kod, jel = gyoker_mod(a.gyoker, a.id)
    elif a.kapuk:
        kod, jel = kapuk()
    else:
        ap.print_help()
        return 2
    szoveg = '\n'.join(jel) + '\n'
    print(szoveg, end='')
    if a.jelentes:
        with open(a.jelentes, 'w', encoding='utf-8') as f:
            f.write(szoveg)
    return kod


if __name__ == '__main__':
    sys.exit(main())
