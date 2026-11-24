#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gepsor.py -- a gép nehéz futásainak közös, érkezési sorrendű (FIFO) sora: a lapgen-futás (3–4 GB) és a teljes push előtti
kapu egyszerre csak egy lehet a gépen (CLAUDE.md Munkamód 7.). A sor a kézi „szabad” jelet váltja ki: aki nehéz futást
indít, beáll a sorba, és a sor engedi tovább, ha az előtte állók végeztek.

Használat (a repó gyökeréből, bármelyik worktree-ből; a sor a worktree-k között közös):
    python eszkozok/gepsor.py futtat --leiras "lapgen-tesztek" -- python eszkozok/lapgen/tesztek/futtat.py
    python eszkozok/gepsor.py allapot          # ki fut, ki vár (sorrendben); a halott jegyeket nem törli
Kódból:
    import gepsor
    with gepsor.Sor('push_elott.py teljes kapu'):
        ...
A `futtat` kilépési kódja a parancsé (a sor hibájánál 2).

Működés:
  * A sor egy könyvtár a repón kívül: `~/.pardes/gepsor/` (Windowson `%USERPROFILE%\\.pardes\\gepsor\\`, WSL-ben a WSL home-ja;
    a `PARDES_ZAR_KONYVTAR` felülírja a `~/.pardes`-t, mint a helyi ellenőrzés-zárnál). Egy beálló egy jegyfájl:
    `<idő ns>_<pid>_<véletlen>.jegy`, JSON (pid, a folyamat indulási ideje, gép, platform, leírás, munkakönyvtár, kezdet).
    A jegy ideiglenes névre íródik, és atomi átnevezéssel (`os.replace`) kerül a sorba: félig írt jegy nincs.
  * A sorrend a fájlnév (az érkezés ideje). Az fut, akinek a jegye az első; a többi 2 mp-enként újranéz, és kiírja,
    hányadik, és ki van előtte.
  * Halott jegy: ugyanazon a gépen és platformon a jegy pid-je már nem él, vagy él, de más folyamat (a pid újrahasznosult:
    az indulási idő eltér). A váró a halott jegyet törli, de **csak a jegy újraolvasása és a pid újbóli ellenőrzése után,
    közvetlenül a törlés előtt**; élő pid jegyét soha nem törli, más gépről/platformról (pl. WSL ↔ Windows) jött jegyet sem
    (azt csak jelzi), és más folyamatot soha nem állít le. A jegynév egyedi, és soha nem íródik újra, ezért a törölt fájl
    pontosan az, amelyet halottnak ítéltünk.
  * Ha a sor eleje a `PARDES_SOR_JELZES_PERC` (alap 90) percnél régebben fut, a váró egyszer FIGYELEM-sort ír (ki tartja, mióta);
    a jegyet nem törli.
  * Újrabelépés: a sorban állás a `PARDES_SOR_TARTVA` környezeti változót a gyerekfolyamatokra is ráteszi; a gyerek (pl. a teljes
    kapu által indított lapgen-futás) ilyenkor nem áll be újra (különben önmagára várna).
  * A GitHub-futás (`GITHUB_ACTIONS`) nem áll sorba.
  * Holtpont-védelem: a helyi ellenőrzés-zár alatt futó folyamat (`PARDES_ZAR_TARTVA`, a `HelyiZar` állítja) nem áll sorba, csak jelzi.
    Különben az E28 (a zár alatt lapot generál) a sorra várna, a sor eleje pedig (pl. egy teljes kapu) a zárra.
A helyi ellenőrzés-zár (`ellenorzes.zar`, `eszkozok/ellenorzes/futtat.py` `HelyiZar`) mellette marad: az az E2–E39-et és az olvasó
tesztjeit védi; a sor a nehéz futások sorrendjét adja. A sor mindig kívül van (sor → zár), így a kettő nem akad össze.
A szabály: MUNKAMENET.md „Menet-ellenőrzés”, 5. pont.
"""

import argparse
import json
import os
import socket
import subprocess
import sys
import time
import uuid

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KONYVTAR_VALTOZO = 'PARDES_ZAR_KONYVTAR'   # közös a helyi ellenőrzés-zárral (`futtat.py` `ZAR_KONYVTAR_VALTOZO`)
TARTVA_VALTOZO = 'PARDES_SOR_TARTVA'
ZAR_TARTVA_VALTOZO = 'PARDES_ZAR_TARTVA'   # a helyi ellenőrzés-zár tartója állítja (`futtat.py` `HelyiZar`)
JELZES_VALTOZO = 'PARDES_SOR_JELZES_PERC'
SOR_NEV = 'gepsor'
JEGY_UTOTAG = '.jegy'
ALAP_JELZES_PERC = 90
VARAKOZAS_MP = 2.0


def sor_konyvtar():
    alap = os.environ.get(KONYVTAR_VALTOZO) or os.path.join(os.path.expanduser('~'), '.pardes')
    return os.path.join(alap, SOR_NEV)


def platform_jel():
    return 'nt' if os.name == 'nt' else 'posix'


# ---------------------------------------------------------------------------
# folyamat-azonosság: él-e a pid, és ugyanaz a folyamat-e (indulási idő)
# ---------------------------------------------------------------------------

def _win_folyamat(pid):
    """(él-e, indulási idő vagy None). Windowson az os.kill(pid, 0) nem használható (leállítaná). Ha a folyamat létezik, de
    nem nyitható meg (jogosultság), élőnek számít: a kétes esetben nem törlünk."""
    import ctypes
    from ctypes import wintypes
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel32.OpenProcess.restype = wintypes.HANDLE
    kernel32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
    h = kernel32.OpenProcess(0x1000, False, pid)   # PROCESS_QUERY_LIMITED_INFORMATION
    if not h:
        hiba = ctypes.get_last_error()
        return (hiba == 5), None   # ERROR_ACCESS_DENIED: létezik; 87 (ERROR_INVALID_PARAMETER): nincs ilyen pid
    try:
        kod = wintypes.DWORD()
        if kernel32.GetExitCodeProcess(h, ctypes.byref(kod)) and kod.value != 259:   # 259: STILL_ACTIVE
            return False, None
        letre, kilep, kern, felh = (wintypes.FILETIME() for _ in range(4))
        if kernel32.GetProcessTimes(h, ctypes.byref(letre), ctypes.byref(kilep), ctypes.byref(kern), ctypes.byref(felh)):
            return True, (letre.dwHighDateTime << 32) | letre.dwLowDateTime
        return True, None
    finally:
        kernel32.CloseHandle(h)


def _posix_folyamat(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False, None
    except PermissionError:
        pass
    except OSError:
        return False, None
    try:
        with open('/proc/%d/stat' % pid, encoding='utf-8', errors='replace') as f:
            mezok = f.read().rsplit(')', 1)[1].split()
        return True, int(mezok[19])   # a 22. mező (starttime); a `)` utáni rész a 3. mezővel kezdődik
    except (OSError, IndexError, ValueError):
        return True, None


def folyamat(pid):
    """(él-e, indulási idő vagy None) ezen a gépen."""
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False, None
    if pid <= 0:
        return False, None
    return _win_folyamat(pid) if os.name == 'nt' else _posix_folyamat(pid)


def jegy_el(adat, folyamat_fn=folyamat, gep=None, plat=None):
    """(él-e, ok). Más gépről vagy platformról jött jegy élőnek számít (nem ítélhető meg, nem törölhető)."""
    gep = socket.gethostname() if gep is None else gep
    plat = platform_jel() if plat is None else plat
    if not isinstance(adat, dict):
        return True, 'olvashatatlan jegy (nem törölhető)'
    if adat.get('gep') != gep or adat.get('platform') != plat:
        return True, 'más gép/platform jegye (%s/%s): nem ítélhető meg' % (adat.get('gep'), adat.get('platform'))
    el, indulas = folyamat_fn(adat.get('pid'))
    if not el:
        return False, 'a pid %s már nem él' % adat.get('pid')
    if indulas is not None and adat.get('indulas') is not None and indulas != adat.get('indulas'):
        return False, 'a pid %s él, de más folyamat (a pid újrahasznosult)' % adat.get('pid')
    return True, ''


# ---------------------------------------------------------------------------
# a sor
# ---------------------------------------------------------------------------

def jegyek(konyvtar):
    """A sor jegyfájljai érkezési sorrendben (fájlnevek)."""
    try:
        return sorted(n for n in os.listdir(konyvtar) if n.endswith(JEGY_UTOTAG) and not n.startswith('.'))
    except FileNotFoundError:
        return []


def jegy_olvas(konyvtar, nev):
    """A jegy tartalma (dict), 'nincs' (közben törlődött), vagy None (olvashatatlan)."""
    try:
        with open(os.path.join(konyvtar, nev), encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return 'nincs'
    except (OSError, ValueError):
        return None


def halott_torol(konyvtar, nev, folyamat_fn=folyamat, gep=None, plat=None, kiir=None):
    """A halott jegy törlése. Közvetlenül a törlés előtt újraolvassa a jegyet, és újra ellenőrzi a pid-et; élő pid jegyét
    soha nem törli. Visszaad: True, ha törölte (vagy közben eltűnt)."""
    adat = jegy_olvas(konyvtar, nev)
    if adat == 'nincs':
        return True
    el, ok = jegy_el(adat, folyamat_fn, gep, plat)
    if el:
        return False
    try:
        os.remove(os.path.join(konyvtar, nev))
    except FileNotFoundError:
        return True
    except OSError:
        return False
    if kiir:
        kiir('[sor] halott jegy törölve (%s): %s -- %s' % (ok, adat.get('leiras', '?'), nev))
    return True


def allapot(konyvtar=None, folyamat_fn=folyamat):
    """A sor állapota: [(jegynév, adat, él-e, ok)], érkezési sorrendben. Nem töröl."""
    konyvtar = konyvtar or sor_konyvtar()
    ki = []
    for n in jegyek(konyvtar):
        adat = jegy_olvas(konyvtar, n)
        if adat == 'nincs':
            continue
        el, ok = jegy_el(adat, folyamat_fn)
        ki.append((n, adat, el, ok))
    return ki


def _jegy_leiras(adat):
    if not isinstance(adat, dict):
        return '(olvashatatlan jegy)'
    return 'pid %s, %s, %s óta: %s' % (adat.get('pid'), adat.get('munkakonyvtar', '?'), adat.get('kezdet', '?'),
                                       adat.get('leiras', '?'))


class Sor(object):
    """Context manager: beáll a gép közös sorába, és akkor tér vissza, ha ő a sor eleje. Kilépéskor törli a saját jegyét.
    `konyvtar`, `kiir`, `alvas`, `folyamat_fn`, `varakozas` a tesztekhez cserélhető."""

    def __init__(self, leiras, konyvtar=None, kiir=None, alvas=None, folyamat_fn=folyamat, varakozas=VARAKOZAS_MP):
        self.leiras = leiras
        self.konyvtar = konyvtar or sor_konyvtar()
        self.kiir = kiir or (lambda s: print(s, file=sys.stderr, flush=True))
        self.alvas = alvas or time.sleep
        self.folyamat_fn = folyamat_fn
        self.varakozas = varakozas
        self.aktiv = not os.environ.get('GITHUB_ACTIONS') and not os.environ.get(TARTVA_VALTOZO)
        if self.aktiv and os.environ.get(ZAR_TARTVA_VALTOZO):
            self.aktiv = False
            self.kiir('[sor] nem áll sorba: a helyi ellenőrzés-zár alatt fut (holtpont-védelem): %s' % leiras)
        self.jegy = None
        self.vart = 0.0
        self._regi_tartva = None

    def beall(self):
        """A saját jegy kiírása (atomi átnevezéssel). Visszaad: a jegy neve."""
        os.makedirs(self.konyvtar, exist_ok=True)
        pid = os.getpid()
        _, indulas = self.folyamat_fn(pid)
        nev = '%020d_%d_%s%s' % (time.time_ns(), pid, uuid.uuid4().hex[:12], JEGY_UTOTAG)
        tmp = os.path.join(self.konyvtar, '.%s.tmp' % uuid.uuid4().hex)
        with open(tmp, 'w', encoding='utf-8') as f:
            json.dump({'pid': pid, 'indulas': indulas, 'gep': socket.gethostname(), 'platform': platform_jel(),
                       'leiras': self.leiras, 'munkakonyvtar': os.getcwd(), 'ts': time.time(),
                       'kezdet': time.strftime('%Y-%m-%d %H:%M:%S')}, f, ensure_ascii=False)
        os.replace(tmp, os.path.join(self.konyvtar, nev))
        self.jegy = nev
        return nev

    def elottem(self):
        """Az előttem álló jegyek (a halottakat közben törli). Visszaad: [(név, adat)]."""
        ki = []
        for n in jegyek(self.konyvtar):
            if n == self.jegy:
                break
            if halott_torol(self.konyvtar, n, self.folyamat_fn, kiir=self.kiir):
                continue
            adat = jegy_olvas(self.konyvtar, n)
            if adat == 'nincs':
                continue
            ki.append((n, adat))
        return ki

    def __enter__(self):
        if not self.aktiv:
            return self
        self.beall()
        jelzes_perc = float(os.environ.get(JELZES_VALTOZO, ALAP_JELZES_PERC) or ALAP_JELZES_PERC)
        utolso = None
        jelzett_regi = set()
        while True:
            elotte = self.elottem()
            if not elotte:
                break
            if self.jegy not in jegyek(self.konyvtar):
                raise RuntimeError('a saját jegy eltűnt a sorból: %s' % os.path.join(self.konyvtar, self.jegy))
            hely = len(elotte) + 1
            if hely != utolso:
                self.kiir('[sor] vár: %d. a gép sorában (%s); fut: %s' % (hely, self.leiras, _jegy_leiras(elotte[0][1])))
                utolso = hely
            eleje_nev, eleje = elotte[0]
            if isinstance(eleje, dict) and eleje_nev not in jelzett_regi:
                kor = (time.time() - float(eleje.get('ts', time.time()))) / 60.0
                if kor > jelzes_perc:
                    self.kiir('[sor] FIGYELEM: a sor eleje %.0f perce fut, a folyamata él (%s); a sor nem törli, és nem állítja '
                              'le: ha elakadt, a gazdája állítja le.' % (kor, _jegy_leiras(eleje)))
                    jelzett_regi.add(eleje_nev)
            self.alvas(self.varakozas)
            self.vart += self.varakozas
        if utolso is not None:
            self.kiir('[sor] sorra került %.0f mp várakozás után: %s' % (self.vart, self.leiras))
        self._regi_tartva = os.environ.get(TARTVA_VALTOZO)
        os.environ[TARTVA_VALTOZO] = self.jegy
        return self

    def __exit__(self, *exc):
        if not self.aktiv or not self.jegy:
            return False
        if self._regi_tartva is None:
            os.environ.pop(TARTVA_VALTOZO, None)
        else:
            os.environ[TARTVA_VALTOZO] = self._regi_tartva
        try:
            os.remove(os.path.join(self.konyvtar, self.jegy))
        except OSError:
            pass
        self.jegy = None
        return False


def main(argv=None):
    ap = argparse.ArgumentParser(description='A gép nehéz futásainak közös FIFO-sora (lapgen, teljes kapu).')
    al = ap.add_subparsers(dest='parancs')
    f = al.add_parser('futtat', help='beáll a sorba, és sorra kerülve futtatja a parancsot (a -- után)')
    f.add_argument('--leiras', default=None, help='mi fut (a többi váró ezt látja)')
    f.add_argument('cmd', nargs=argparse.REMAINDER)
    al.add_parser('allapot', help='a sor jegyei érkezési sorrendben')
    a = ap.parse_args(argv)
    if a.parancs == 'allapot':
        sor = allapot()
        if not sor:
            print('A gép sora üres (%s).' % sor_konyvtar())
            return 0
        for i, (n, adat, el, ok) in enumerate(sor):
            allas = 'fut' if i == 0 else '%d. vár' % (i + 1)
            print('%-7s %s%s' % (allas, _jegy_leiras(adat), '' if el else '  [HALOTT: %s; a következő váró törli]' % ok))
        return 0
    if a.parancs == 'futtat':
        cmd = a.cmd[1:] if a.cmd[:1] == ['--'] else a.cmd
        if not cmd:
            print('HIBA: a futtatandó parancs hiányzik (… futtat --leiras "…" -- <parancs>)', file=sys.stderr)
            return 2
        with Sor(a.leiras or ' '.join(cmd)):
            return subprocess.call(cmd)
    ap.print_help()
    return 2


if __name__ == '__main__':
    sys.exit(main())
