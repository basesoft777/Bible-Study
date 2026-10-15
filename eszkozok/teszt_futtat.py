"""Az olvasó-szerver tesztjeinek közös belépési pontja (#100, DT-F100a (c)).

Miért kell: a projekt venv-je (Flask, Python 3.12) a WSL `pardes` disztribúcióban van, és a WSL a `/mnt/c` fájlrendszert nagyon
lassan olvassa. A `teszt_olvaso_szerver.py` a `PARDES_DB` nélkül a `/mnt/c/…/pardes.db`-t nyitná meg (45+ perc a natív ~2 perc
helyett). Ez a szkript magától a gyors környezetet választja:

  * Windowsról hívva magát a WSL `pardes` disztribúcióban futtatja újra (a repót a `/mnt/c/…` útról használja);
  * a WSL venv-jét (`~/pardes/eszkozok/olvaso_szerver/.venv/bin/python`, Python 3.12) használja, ha van;
  * a `PARDES_DB`-t a WSL-natív `~/pardes/pardes.db`-re állítja (ha nincs kézzel megadva), és kiírja, melyiket nyitotta meg; ha az
    adatbázis a `/mnt/c` alatt van, FIGYELMEZTET (a lassúság oka);
  * a kód és a `konkordancia/` a `/mnt/c`-ről olvasódik (DT-F100a (c): nincs másolat).

Használat (a repó gyökeréből, Windowsról vagy WSL-ből ugyanúgy):
    python eszkozok/teszt_futtat.py                       # az olvasó-szerver mind a teszt_*.py fájlja
    python eszkozok/teszt_futtat.py --gyors               # a lassú teszt_szintek.py nélkül
    python eszkozok/teszt_futtat.py --fajl teszt_tervezo  # csak a megnevezett fájl(ok); többször is megadható
    python eszkozok/teszt_futtat.py --reszletes           # a tesztek teljes kimenete (alapból csak az összegzés, hibánál minden)
Kilépési kód: 0, ha minden fájl zöld; egyébként 1.
"""
import argparse
import os
import re
import subprocess
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SZERVER = os.path.join(REPO, 'eszkozok', 'olvaso_szerver')
LASSU = ('teszt_szintek.py',)                      # #98-nál párhuzamos futás mellett ~19 perc; külön mérendő
WSL_DISZTRO = 'pardes'
WSL_VENV_PY = '$HOME/pardes/eszkozok/olvaso_szerver/.venv/bin/python'


def tesztfajlok():
    return sorted(f for f in os.listdir(SZERVER) if f.startswith('teszt_') and f.endswith('.py'))


def wsl_ut(ut):
    """`C:\\a\\b` -> `/mnt/c/a/b`."""
    ut = os.path.abspath(ut).replace('\\', '/')
    if len(ut) > 1 and ut[1] == ':':
        return '/mnt/%s%s' % (ut[0].lower(), ut[2:])
    return ut


def wslben_ujra(argv):
    """Windowsról: ugyanez a szkript a WSL-ben, a venv Pythonjával. A kilépési kód átöröklődik."""
    szkript = wsl_ut(os.path.abspath(__file__))
    parancs = 'cd "%s" && exec "%s" "%s" %s' % (wsl_ut(REPO), WSL_VENV_PY.replace('$HOME', '$HOME'), szkript, ' '.join(argv))
    print('[teszt_futtat] Windows észlelve: újraindítás a WSL "%s" disztribúcióban' % WSL_DISZTRO, flush=True)
    return subprocess.call(['wsl', '-d', WSL_DISZTRO, '--', 'bash', '-lc', parancs])


def adatbazis_valasztas():
    """(út, forrás-leírás). Kézi PARDES_DB > a WSL-natív ~/pardes/pardes.db > a repó gyökerének pardes.db-je (lassú: figyelmeztetéssel)."""
    kezi = os.environ.get('PARDES_DB')
    if kezi:
        return kezi, 'PARDES_DB (kézzel megadva)'
    nativ = os.path.join(os.path.expanduser('~'), 'pardes', 'pardes.db')
    if os.path.isfile(nativ):
        return nativ, 'WSL-natív alapérték (~/pardes/pardes.db)'
    return os.path.join(REPO, 'pardes.db'), 'a repó gyökerének pardes.db-je (nincs WSL-natív példány)'


def epites_ts(ut):
    try:
        sys.path.insert(0, SZERVER)
        import allapot
        return allapot.db_epites_ts(ut) or '(nincs)'
    except Exception as ex:                                             # a kiírás csak tájékoztat
        return '(nem olvasható: %s)' % ex


def fut(fajl, kornyezet, reszletes):
    """(kilépési kód, másodperc, utolsó összegző sorok)."""
    t0 = time.monotonic()
    p = subprocess.run([sys.executable, os.path.join(SZERVER, fajl)], cwd=REPO, env=kornyezet, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       text=True, encoding='utf-8', errors='replace')
    mp = time.monotonic() - t0
    kimenet = p.stdout or ''
    if reszletes or p.returncode != 0:
        print(kimenet, end='' if kimenet.endswith('\n') else '\n')
    sorok = [s for s in kimenet.splitlines() if s.strip()]
    osszegzo = ' | '.join(s for s in sorok[-4:] if re.match(r'^(Ran |OK|FAILED|skipped)', s)) or (sorok[-1] if sorok else '(nincs kimenet)')
    return p.returncode, mp, osszegzo


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--gyors', action='store_true', help='a lassú fájlok (%s) kihagyása' % ', '.join(LASSU))
    ap.add_argument('--fajl', action='append', default=[], help='csak ez a fájl (teszt_x vagy teszt_x.py)')
    ap.add_argument('--reszletes', action='store_true')
    ap.add_argument('--nincs-wsl', action='store_true', help='Windowson se induljon újra a WSL-ben (a hívó felel a környezetért)')
    a, _ = ap.parse_known_args()
    if os.name == 'nt' and not a.nincs_wsl:
        return wslben_ujra(sys.argv[1:])

    db, honnan = adatbazis_valasztas()
    kornyezet = dict(os.environ, PARDES_DB=db, PYTHONIOENCODING='utf-8')
    print('[teszt_futtat] python: %s (%s)' % (sys.executable, sys.version.split()[0]))
    print('[teszt_futtat] adatbázis: %s -- %s' % (db, honnan))
    if os.path.isfile(db):
        print('[teszt_futtat] adatbázis mérete: %.0f MB, epites_ts: %s' % (os.path.getsize(db) / 1048576, epites_ts(db)))
    else:
        print('[teszt_futtat] FIGYELEM: az adatbázis nem létezik (%s): a DB-s tesztek kimaradnak' % db)
    if os.path.abspath(db).replace('\\', '/').startswith('/mnt/'):
        print('[teszt_futtat] FIGYELEM: az adatbázis a /mnt/c alatt van -- a WSL ezt nagyon lassan olvassa (45+ perc a ~2 perc helyett). '
              'Másold a WSL-natív ~/pardes/pardes.db-re (az indit.sh ezt teszi), vagy állítsd a PARDES_DB-t arra.')
    try:
        import flask  # noqa: F401
    except ImportError:
        print('[teszt_futtat] FIGYELEM: ebben a Pythonban nincs Flask: a Flask-os tesztek kimaradnak. A venv: ~/pardes/eszkozok/olvaso_szerver/.venv')

    fajlok = tesztfajlok()
    if a.fajl:
        kert = {f if f.endswith('.py') else f + '.py' for f in a.fajl}
        hianyzik = sorted(kert - set(fajlok))
        if hianyzik:
            print('[teszt_futtat] HIBA: nincs ilyen tesztfájl: %s (van: %s)' % (', '.join(hianyzik), ', '.join(fajlok)))
            return 2
        fajlok = [f for f in fajlok if f in kert]
    elif a.gyors:
        fajlok = [f for f in fajlok if f not in LASSU]

    eredmenyek = []
    for f in fajlok:
        print('[teszt_futtat] fut: %s ...' % f, flush=True)
        kod, mp, ossz = fut(f, kornyezet, a.reszletes)
        eredmenyek.append((f, kod, mp, ossz))
        print('[teszt_futtat] %s: %s, %.1f mp -- %s' % (f, 'ZÖLD' if kod == 0 else 'HIBA (%d)' % kod, mp, ossz), flush=True)

    print('\n[teszt_futtat] összegzés')
    for f, kod, mp, _ in eredmenyek:
        print('  %-34s %8.1f mp  %s' % (f, mp, 'zöld' if kod == 0 else 'HIBA'))
    gyors_mp = sum(mp for f, _, mp, _ in eredmenyek if f not in LASSU)
    lassu_mp = sum(mp for f, _, mp, _ in eredmenyek if f in LASSU)
    print('  %-34s %8.1f mp  (a lassú fájlok nélkül)' % ('együtt', gyors_mp))
    if lassu_mp:
        print('  %-34s %8.1f mp  (%s)' % ('lassú fájlok külön', lassu_mp, ', '.join(LASSU)))
    return 0 if all(k == 0 for _, k, _, _ in eredmenyek) else 1


if __name__ == '__main__':
    sys.exit(main())
