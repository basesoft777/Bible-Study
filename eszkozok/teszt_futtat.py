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
    python eszkozok/teszt_futtat.py --diff origin/main    # a lassú fájlok csak akkor, ha a diff a lefedett fájljaikat érinti
Kilépési kód: 0, ha minden fájl zöld; egyébként 1.

F188 (MUNKAMENET.md „Menet-ellenőrzés”, 3–4. pont):
  * a lassú tesztek lefedett fájljainak egyetlen listája a `LASSU_LEFEDETT`; a `--diff ALAP` a többi tesztet futtatja, a lassút
    csak akkor, ha a diff (a munkafa a `git merge-base ALAP HEAD`-hez képest, az új fájlokkal) a lefedett fájlok valamelyikét
    érinti; különben kiírja, melyiket nem futtatta, és miért. A CI ezeket a teszteket nem futtatja: ha a diff érinti őket,
    helyben futniuk kell (ELLENOR_F188 2.);
  * a futás a közös helyi ellenőrzés-zárat veszi (`eszkozok/ellenorzes/futtat.py` `HelyiZar`, `~/.pardes/ellenorzes.zar`);
    Windowsról a Windows-oldalon veszi, mielőtt a WSL-be lép, és a WSL-beli futás (`--zar-tartva`) már nem vesz újat.
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
LASSU = ('teszt_szintek.py', 'teszt_arculat.py')  # ~19 perc (#98, párhuzamos futás mellett); ~30 perc (#104 javítóköre)
# F188 T4 (ELLENOR_F188 2.): a lassú tesztfájlok lefedett fájljai (repó-relatív; `/`-re végződő = könyvtár). Egy hely: ez.
# A lista a tesztek importfüggése: az olvasó-szerver kódja, és amit fájlútról vagy a sys.path-on át betölt (`blokkok.py`:
# olvaso_pilot/bdb_szelet, bdb_rovidites -> kiejtes, tanulmany_regiszter; `bdb_szelet.py`: bdb_konyv_javit -> normalizal,
# forditas_kapuk -> naplok/FORDITAS_P4_ellenoriz.py; `lekerdezesek.py`: bdb_jelolt/szakasz_bemenet). A `teszt_szintek` a
# `_pilot_json`-on át az `olvaso_pilot/adat.py`-t is futtatja, amely a TSV-kből épít (tsk_kulcs, karoli_kh_szuro, bdb_jelolt):
# ezért az `adat/` és a `konkordancia/` változása is érinti. A `test_zar.py` statikusan ellenőrzi, hogy az olvasó-szerver
# fájlútról betöltött moduljai a listán vannak.
_OLVASO_KOD = ('eszkozok/olvaso_szerver/', 'eszkozok/olvaso_pilot/', 'eszkozok/bdb_jelolt/', 'eszkozok/bdb_rovidites.py',
               'eszkozok/kiejtes.py', 'eszkozok/tanulmany_regiszter.py', 'eszkozok/bdb_konyv_javit.py',
               'eszkozok/normalizal.py', 'eszkozok/forditas_kapuk.py', 'naplok/FORDITAS_P4_ellenoriz.py',
               'eszkozok/tsk_kulcs.py', 'eszkozok/karoli_kh_szuro.py', 'eszkozok/teszt_futtat.py')
LASSU_LEFEDETT = {
    'teszt_szintek.py': _OLVASO_KOD + ('adat/', 'konkordancia/'),
    'teszt_arculat.py': _OLVASO_KOD,
}
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


def erintett_lassu(valtozott):
    """{lassú fájl: True/False}: érinti-e a változott fájlok listája a lefedett fájljait."""
    valtozott = [v.replace('\\', '/') for v in valtozott]
    ki = {}
    for fajl, elotagok in LASSU_LEFEDETT.items():
        ki[fajl] = any(v == e.rstrip('/') or v.startswith(e if e.endswith('/') else e + '/') or v == e
                       for v in valtozott for e in elotagok)
    return ki


def diff_fajlok(alap):
    """A munkafa változott és új fájljai a `git merge-base alap HEAD`-hez képest, vagy None (git-hiba)."""
    def git(*args):
        try:
            return subprocess.check_output(['git'] + list(args), cwd=REPO, stderr=subprocess.DEVNULL).decode('utf-8', 'replace')
        except (subprocess.CalledProcessError, OSError):
            return None
    mb = git('merge-base', alap, 'HEAD')
    if mb is None:
        return None
    lista = (git('diff', '--name-only', mb.strip()) or '').splitlines()
    lista += (git('ls-files', '--others', '--exclude-standard') or '').splitlines()
    return sorted({x.strip() for x in lista if x.strip()})


def helyi_zar(leiras):
    """A közös helyi ellenőrzés-zár (`eszkozok/ellenorzes/futtat.py` `HelyiZar`), fájlútról betöltve."""
    import importlib.util
    ut = os.path.join(REPO, 'eszkozok', 'ellenorzes', 'futtat.py')
    spec = importlib.util.spec_from_file_location('ellenorzes_futtat', ut)
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul.HelyiZar(leiras)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--gyors', action='store_true', help='a lassú fájlok (%s) kihagyása' % ', '.join(LASSU))
    ap.add_argument('--fajl', action='append', default=[], help='csak ez a fájl (teszt_x vagy teszt_x.py)')
    ap.add_argument('--reszletes', action='store_true')
    ap.add_argument('--nincs-wsl', action='store_true', help='Windowson se induljon újra a WSL-ben (a hívó felel a környezetért)')
    ap.add_argument('--diff', metavar='ALAP', help='a lassú fájlok csak akkor, ha a diff (merge-base ALAP) a lefedett fájljaikat érinti')
    ap.add_argument('--kihagy', action='append', default=[], help='ez a fájl kimarad (a --diff tölti ki a WSL-futásnak)')
    ap.add_argument('--zar-tartva', action='store_true', help='a hívó már tartja a helyi ellenőrzés-zárat (belső)')
    a, _ = ap.parse_known_args()
    argv = [x for x in sys.argv[1:]]
    if a.diff and not a.fajl:
        valtozott = diff_fajlok(a.diff)
        if valtozott is None:
            print('[teszt_futtat] FIGYELEM: a diff nem állapítható meg (%s); a lassú fájlok is futnak' % a.diff)
        else:
            for f, erint in sorted(erintett_lassu(valtozott).items()):
                if not erint:
                    print('[teszt_futtat] NEM FUTOTT: %s -- a diff (%d fájl, merge-base %s) egyik lefedett fájlját sem érinti '
                          '(LASSU_LEFEDETT: %d elem); ezt a tesztet a CI sem futtatja' % (f, len(valtozott), a.diff,
                                                                                         len(LASSU_LEFEDETT[f])))
                    argv += ['--kihagy', f]
                    a.kihagy.append(f)
        i = argv.index('--diff')
        del argv[i:i + 2]
    if a.zar_tartva:
        return _fut(a, argv)
    with helyi_zar('teszt_futtat.py %s' % ' '.join(argv)):
        return _fut(a, argv + ['--zar-tartva'])


def _fut(a, argv):
    if os.name == 'nt' and not a.nincs_wsl:
        return wslben_ujra(argv)

    db, honnan = adatbazis_valasztas()
    kornyezet = dict(os.environ, PARDES_DB=db, PYTHONIOENCODING='utf-8')
    print('[teszt_futtat] python: %s (%s)' % (sys.executable, sys.version.split()[0]))
    print('[teszt_futtat] adatbázis: %s -- %s' % (db, honnan))
    if os.path.isfile(db):
        print('[teszt_futtat] adatbázis mérete: %.0f MB, epites_ts: %s' % (os.path.getsize(db) / 1048576, epites_ts(db)))
    else:
        print('[teszt_futtat] HIBA: az adatbázis nem létezik (%s): a DB-s tesztek kimaradnának (hamis zöld), ezért megállok.' % db)
        return 2
    if os.path.abspath(db).replace('\\', '/').startswith('/mnt/'):
        print('[teszt_futtat] FIGYELEM: az adatbázis a /mnt/c alatt van -- a WSL ezt nagyon lassan olvassa (45+ perc a ~2 perc helyett). '
              'Másold a WSL-natív ~/pardes/pardes.db-re (az indit.sh ezt teszi), vagy állítsd a PARDES_DB-t arra.')
    try:
        import flask  # noqa: F401
    except ImportError:
        venv = os.path.expanduser('~/pardes/eszkozok/olvaso_szerver/.venv/bin/python')
        if os.path.isfile(venv) and os.path.abspath(venv) != os.path.abspath(sys.executable):
            print('[teszt_futtat] ebben a Pythonban nincs Flask: újraindítás a WSL venv-jével (%s)' % venv, flush=True)
            sys.stdout.flush()
            os.execv(venv, [venv] + sys.argv)
        print('[teszt_futtat] HIBA: ebben a Pythonban nincs Flask, és a WSL venv sem található (%s): a Flask-os tesztek kimaradnának (hamis zöld), ezért megállok.' % venv)
        return 2

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
    if a.kihagy:
        kihagy = {f if f.endswith('.py') else f + '.py' for f in a.kihagy}
        fajlok = [f for f in fajlok if f not in kihagy]

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
