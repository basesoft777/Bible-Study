#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
futtat.py -- CI.0/CI.2: az E2-E29 ellenorzesek kozos futtatoja
(F02_CI_ELLENORZES_BRIEF.md). Az E1-et (SEMA 1-12, Q1, Q7) NEM ez futtatja --
azt a meglevo `eszkozok/ellenoriz.py --study FILE` adja, kulon hivassal
(l. .github/workflows/ellenorzes.yml).

CLI:
    python eszkozok/ellenorzes/futtat.py --teljes
    python eszkozok/ellenorzes/futtat.py --valtozott fajl1.md fajl2.md
    python eszkozok/ellenorzes/futtat.py --valtozott fajl.md --diff-alap origin/main --diff-fej HEAD --pr-cim "..."

Kimenet: markdown jelentes stdout-ra, szabalyonkent talalatszam + minta.
Kilepesi kod: 0 = nincs HIBA-szintu talalat, 1 = van, 2 = futasi hiba.

--teljes modban MINDEN talalat csak JELENTES (a HIBA-besorolas a diff-
hatokorre vonatkozik, D3 -- l. brief "Diff-hatokor" szakasz), tehat a
kilepesi kod --teljes modban mindig 0.

D8 (--valtozott + --diff-alap/--diff-fej modban): a HIBA csak a diff altal
HOZZAADOTT/MODOSITOTT sorokra vonatkozik -- egy szabaly regi (a PR altal
nem erintett) talalata csak JELENTES. Kivetel a SZ.FAJLSZINTU_SZABALYOK
(E4, E5, E6, E7, E16, E19, E20, E25, E26, E27, E28, E29, E30, E31): ezeknel a talalat nem egy konkret uj sorhoz kotheto,
tehat mindig a sajat szintjukon jelentkeznek. Ha --diff-alap/--diff-fej
hianyzik --valtozott modban is, a regi (D8 elotti) viselkedes ervenyesul:
a talalat fajlszinten a sajat szintjen jelentkezik -- ezt CI.2 mindig
diff-refekkel hivja, csak a helyi, kezi futtatashoz marad tartalek.
"""

import argparse
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kozos import md_fajlok, kizart_e, git_diff_hozzaadott_sorok, ROOT
import szabalyok as SZ


# ---------------------------------------------------------------------------
# F188 (T5/T6 kiegészítés): egyszerre egy helyi teljes ellenőrzés -- közös fájlzár a repón kívül
# ---------------------------------------------------------------------------
# A zár helye: ~/.pardes/ellenorzes.zar (Windowson %USERPROFILE%\.pardes\, WSL-ben a WSL home-ja), a worktree-k
# között közös; a PARDES_ZAR_KONYVTAR felülírja. A zárfájl JSON: pid, gép, időbélyeg, leírás, munkakönyvtár.
# Foglalt zárnál a futás kiírja, ki tartja, és vár. Elavult (az átvételi zár alatt veszi át, l. HelyiZar): a tartó folyamat ugyanazon a gépen már nem
# él, vagy a zár a korlátnál (PARDES_ZAR_KORLAT_PERC, alap 120 perc) régebbi. A GitHub-futás nem vesz zárat. A
# szabály: MUNKAMENET.md „Menet-ellenőrzés”, 4. pont. Az `eszkozok/teszt_futtat.py` ugyanezt a zárat használja.
ZAR_KONYVTAR_VALTOZO = 'PARDES_ZAR_KONYVTAR'
ZAR_KORLAT_VALTOZO = 'PARDES_ZAR_KORLAT_PERC'
ZAR_NEV = 'ellenorzes.zar'
ZAR_ALAP_KORLAT_PERC = 120
ZAR_VARAKOZAS_MP = 5


def json_betolt(f):
    import json
    return json.load(f)


def zar_ut():
    konyvtar = os.environ.get(ZAR_KONYVTAR_VALTOZO) or os.path.join(os.path.expanduser('~'), '.pardes')
    return os.path.join(konyvtar, ZAR_NEV)


def zar_korlat_perc():
    try:
        return float(os.environ.get(ZAR_KORLAT_VALTOZO, ZAR_ALAP_KORLAT_PERC))
    except ValueError:
        return float(ZAR_ALAP_KORLAT_PERC)


def folyamat_el(pid):
    """El-e a `pid` folyamat ezen a gepen. Windowson az os.kill(pid, 0) nem hasznalhato (leallitana)."""
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    if os.name == 'nt':
        import ctypes
        kernel32 = ctypes.windll.kernel32
        h = kernel32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        try:
            kod = ctypes.c_ulong()
            if not kernel32.GetExitCodeProcess(h, ctypes.byref(kod)):
                return True
            return kod.value == 259  # STILL_ACTIVE
        finally:
            kernel32.CloseHandle(h)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def zar_elavult(adat, most=None, korlat_perc=None, gep=None, el_e=folyamat_el):
    """(elavult-e, ok) a zarfajl tartalmara (dict, vagy None, ha olvashatatlan)."""
    import socket
    import time as _time
    most = _time.time() if most is None else most
    korlat_perc = zar_korlat_perc() if korlat_perc is None else korlat_perc
    gep = socket.gethostname() if gep is None else gep
    if not adat:
        return False, 'olvashatatlan zárfájl'
    kor = (most - float(adat.get('ts', most))) / 60.0
    if kor > korlat_perc:
        return True, 'a zár %.0f perces (korlát: %.0f perc)' % (kor, korlat_perc)
    if adat.get('gep') == gep and not el_e(adat.get('pid')):
        return True, 'a zárat tartó folyamat (pid %s) már nem él' % adat.get('pid')
    return False, ''


ZAR_ATVETEL_UTOTAG = '.atvetel'
ZAR_ATVETEL_ELAVULT_MP = 60   # az átvételi zár (rövid kritikus szakasz) ennyi idő után elavult: a tartója összeomlott
ZAR_TURELEM_MP = 60           # az olvashatatlan/üres fő zár (még íródik vagy sérült) csak ennyi idő után elavult


class HelyiZar(object):
    """Context manager: a kozos helyi ellenorzes-zar (l. fent). `kiir`, `alvas`, `el_e` a tesztekhez cserelheto.

    Helyesseg (ELLENOR_F188_2 1.). Ket fajl: a fo zar (`ut`) es az atveteli zar (`ut + '.atvetel'`).
    (1) A fo zar csak `os.open(O_CREAT | O_EXCL)`-lel jon letre: egyszerre legfeljebb egy letrehozo nyer.
    (2) A fo zarat csak az atveteli zar tartoja torli: az elavult zar atvetelekor (ujraolvasas utan, ha meg mindig
        elavult), es a tarto a sajat zarat kilepeskor (ugyancsak az atveteli zar alatt, `azon` szerint).
    (3) Az atveteli zar alatt a fo zar ujraolvasasa es torlese kozott senki mas nem torolheti a fo zarat (2), es amig
        letezik, senki nem hozhat letre ujat (1); a torolt fajl tehat pontosan az, amelyet elavultnak iteltunk.
    (4) Torles utan az atvevo is `O_EXCL`-lel probal fo zarat letrehozni; ha kozben mas nyert, tovabb var.
    Atnevezes es visszateves nincs. Olvashatatlan vagy ures fo zar (a letrehozo meg irja) csak `ZAR_TURELEM_MP`
    utan elavult (mtime). Maradek kockazat: ha egy folyamat az atveteli zar ezredmasodperces kritikus szakaszaban
    omlik ossze, a `ZAR_ATVETEL_ELAVULT_MP` utan az atveteli zarat torolni kell; ha ezt ket varo egyszerre teszi,
    ketten lehetnek a kritikus szakaszban. Ehhez osszeomlas es pontos idozites egyszerre kell; a fo zar (1) akkor is
    kizarja, hogy ket fo zar egyszerre letezzen."""

    def __init__(self, leiras, ut=None, varakozas=ZAR_VARAKOZAS_MP, kiir=None, alvas=None, el_e=folyamat_el):
        import time as _time
        import uuid
        self.leiras = leiras
        self.ut = ut or zar_ut()
        self.atvetel_ut = self.ut + ZAR_ATVETEL_UTOTAG
        self.varakozas = varakozas
        self.kiir = kiir or (lambda s: print(s, file=sys.stderr, flush=True))
        self.alvas = alvas or _time.sleep
        self.el_e = el_e
        self.aktiv = not os.environ.get('GITHUB_ACTIONS')
        self.vart = 0.0
        self.azon = uuid.uuid4().hex

    def _olvas(self, ut=None):
        import json
        try:
            with open(ut or self.ut, encoding='utf-8') as f:
                return json.load(f)
        except (OSError, ValueError):
            return None

    def _elavult(self):
        """(elavult-e, ok, adat) a fo zar MOSTANI allapotara; (False, 'nincs', None), ha nincs fo zar."""
        import time as _time
        adat = self._olvas()
        if adat is None:
            try:
                kor = _time.time() - os.path.getmtime(self.ut)
            except OSError:
                return False, 'nincs', None
            if kor > ZAR_TURELEM_MP:
                return True, 'olvashatatlan zárfájl, %.0f mp óta' % kor, None
            return False, 'íródó vagy olvashatatlan zárfájl', None
        elavult, ok = zar_elavult(adat, el_e=self.el_e)
        return elavult, ok, adat

    def _atveteli_zar(self):
        """Az atveteli zar megszerzese (rovid varakozassal), vagy None, ha most nem sikerult. Visszaad: a tartott
        zar azonositoja (a torleshez)."""
        import time as _time
        try:
            fd = os.open(self.atvetel_ut, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except (FileExistsError, PermissionError):
            try:
                if _time.time() - os.path.getmtime(self.atvetel_ut) > ZAR_ATVETEL_ELAVULT_MP:
                    self.kiir('[zár] elavult átvételi zár törölve: %s' % self.atvetel_ut)
                    os.remove(self.atvetel_ut)
            except OSError:
                pass
            return False
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(self.azon)
        return True

    def _atveteli_zar_el(self):
        for _ in range(400):
            try:
                with open(self.atvetel_ut, encoding='utf-8') as f:
                    sajat = f.read().strip() == self.azon
                if sajat:
                    os.remove(self.atvetel_ut)
                return
            except FileNotFoundError:
                return
            except PermissionError:
                import time as _time
                _time.sleep(0.005)

    def _torol(self, ut):
        """Fajl torlese; Windowson a mas altal eppen olvasott fajlra rovid ideig ujraprobal."""
        import time as _time
        for _ in range(400):
            try:
                os.remove(ut)
                return True
            except FileNotFoundError:
                return False
            except PermissionError:
                _time.sleep(0.005)
        return False

    def atvesz(self):
        """Az elavult fo zar torlese az atveteli zar alatt. True: torolte (utana O_EXCL-lel probal); False: nem kapta
        meg az atveteli zarat, vagy a fo zar az ujraolvasaskor mar nem elavult (vagy nincs)."""
        if not self._atveteli_zar():
            return False
        try:
            elavult, ok, _ = self._elavult()
            if not elavult:
                return False
            if self._torol(self.ut):
                self.kiir('[zár] elavult zár átvéve (%s): %s' % (ok, self.ut))
                return True
            return False
        finally:
            self._atveteli_zar_el()

    def __enter__(self):
        import json
        import socket
        import time as _time
        if not self.aktiv:
            return self
        os.makedirs(os.path.dirname(self.ut), exist_ok=True)
        jelezve = False
        foglalt_torles = 0
        while True:
            try:
                fd = os.open(self.ut, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except PermissionError:
                # Windows: a fájl törlése folyamatban (pending delete); rövid várakozás, újra.
                # Tartós jogosultsághiba nem várakoztat végtelenül.
                foglalt_torles += 1
                if foglalt_torles > 2000:
                    raise
                _time.sleep(0.005)
                continue
            except FileExistsError:
                foglalt_torles = 0
                elavult, ok, adat = self._elavult()
                if elavult:
                    self.atvesz()
                    continue
                if ok == 'nincs':
                    continue  # közben eltűnt
                if not jelezve:
                    adat = adat or {}
                    self.kiir('[zár] vár: a helyi ellenőrzést más futás tartja (pid %s, %s, %s óta: %s) -- %s'
                              % (adat.get('pid'), adat.get('munkakonyvtar', '?'), adat.get('kezdet', '?'),
                                 adat.get('leiras', '?'), self.ut))
                    jelezve = True
                self.alvas(self.varakozas)
                self.vart += self.varakozas
                continue
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                json.dump({'azon': self.azon, 'pid': os.getpid(), 'gep': socket.gethostname(), 'ts': _time.time(),
                           'kezdet': _time.strftime('%Y-%m-%d %H:%M:%S'), 'leiras': self.leiras,
                           'munkakonyvtar': os.getcwd()}, f, ensure_ascii=False)
            if jelezve:
                self.kiir('[zár] megszerezve %.0f mp várakozás után' % self.vart)
            return self

    def __exit__(self, *exc):
        import time as _time
        if not self.aktiv:
            return False
        # A saját zár törlése is az átvételi zár alatt (2): így a törlés nem kerülhet egy átvevő újraolvasása és
        # törlése közé. Ha az átvételi zár sokáig foglalt (elavult), legfeljebb ZAR_ATVETEL_ELAVULT_MP + ráhagyás.
        hatar = _time.time() + ZAR_ATVETEL_ELAVULT_MP + 10
        while not self._atveteli_zar():
            if _time.time() > hatar:
                break
            _time.sleep(0.005)
        try:
            for _ in range(400):
                try:
                    with open(self.ut, encoding='utf-8') as f:
                        sajat = json_betolt(f).get('azon') == self.azon
                except FileNotFoundError:
                    break
                except PermissionError:
                    _time.sleep(0.005)
                    continue
                except (OSError, ValueError, AttributeError):
                    break
                if sajat:
                    self._torol(self.ut)
                break
        finally:
            self._atveteli_zar_el()
        return False


def _szint_diff_szerint(talalat, alap_szint, hozzaadott_cache, diff_alap, diff_fej):
    """D8: a talalat vegleges szintje -- HIBA csak akkor marad, ha a
    talalat sora a diff altal hozzaadott/modositott sorok kozott van."""
    if talalat.sor is None or talalat.sor == 0:
        return alap_szint
    if not diff_alap or not diff_fej:
        return alap_szint
    if talalat.fajl not in hozzaadott_cache:
        hozzaadott_cache[talalat.fajl] = git_diff_hozzaadott_sorok(diff_alap, diff_fej, talalat.fajl)
    hozzaadott = hozzaadott_cache[talalat.fajl]
    if hozzaadott is None:
        # Nem allapithato meg a diff (pl. a fajl nincs a base-ben es a
        # head-ben sem elerheto) -- konzervativan a sajat szinten marad.
        return alap_szint
    if talalat.sor in hozzaadott:
        return alap_szint
    return 'JELENTES'


def fut(valtozott_fajlok, teljes, diff_alap=None, diff_fej=None, pr_cim='', commit_uzenet='', esemeny=''):
    """Visszaad: {szabaly: [Talalat, ...]} -- a Talalat.szint mar a vegleges
    (D8-cal leminositett) szint."""
    valtozott_fajlok = [f for f in valtozott_fajlok if not kizart_e(f)]  # D14
    hatokor = ['__TELJES__'] if teljes else list(valtozott_fajlok)
    fajlok_a_szabalyoknak = md_fajlok() if teljes else valtozott_fajlok

    nyers = {}
    for nev, fv in SZ.SZABALYOK_FUGGVENYEI.items():
        if nev in SZ.HATOKOR_SZABALYOK:
            # E3, E19: adattablan futnak; --teljes modban a '__TELJES__'
            # jelzo kell nekik, nem az md-fajlok listaja (ELLENOR_F28 2. tetel).
            nyers[nev] = fv(hatokor if teljes else valtozott_fajlok)
        else:
            nyers[nev] = fv(fajlok_a_szabalyoknak)

    nyers['E5'] = SZ.e5_tartalomvesztes_or(diff_alap, diff_fej, commit_uzenet)
    # E26 (F30): veglegesszam az agon; push-esemenynel (main) nem ertelmezett
    nyers['E26'] = SZ.e26_vegleges_szam_agon(diff_alap, diff_fej, commit_uzenet, esemeny)
    # E27 (F40): hivatkozas-ellenorzes; a diff-hatokort maga kezeli
    nyers['E27'] = SZ.e27_hivatkozas(diff_alap, diff_fej, esemeny)
    # E30 (F112): ekezet nelkuli magyar szo a PR commit-uzeneteiben; --teljes modban nincs base..head
    nyers['E30'] = [] if teljes else SZ.e30_ascii_commit(diff_alap, diff_fej, commit_uzenet, esemeny)
    # E35 (F169.3): a commitolt nyilt_mag/ naprakesz, ha a PR adat-tablat vagy az exportgeneratort modositja
    nyers['E35'] = SZ.e35_nyilt_mag_naprakesz(valtozott_fajlok, teljes)
    # E16: push-esemenynel nincs PR-cim, ezert nem ertelmezett (a PR-en fut)
    if esemeny == 'push':
        nyers['E16'] = []
    else:
        nyers['E16'] = SZ.e16_ellenorzo_onmodositas(valtozott_fajlok if not teljes else [], pr_cim)

    hozzaadott_cache = {}
    eredmeny = {}
    for nev, talalatok in nyers.items():
        if teljes:
            for t in talalatok:
                t.szint = 'JELENTES'
        elif nev not in SZ.FAJLSZINTU_SZABALYOK:
            # F37: az alap szint a talalat sajat szintje (az E13 tanulmany-
            # fajlon HIBA, mashol FIGYELMEZTETES); a tobbi szabalynal ez
            # azonos az SZ.SZINT[nev]-vel.
            for t in talalatok:
                alap_szint = t.szint or SZ.SZINT[nev]
                t.szint = _szint_diff_szerint(t, alap_szint, hozzaadott_cache, diff_alap, diff_fej)
        eredmeny[nev] = talalatok

    return eredmeny


E16_PUSH_MEGJEGYZES = 'E16: push-esemény, nem értelmezett (a PR-en fut)'


def jelentes_szoveg(eredmeny, teljes, minta_db=3, esemeny=''):
    sorok = []
    sorok.append('# Ellenorzes jelentes (%s)' % ('teljes repo' if teljes else 'valtozott fajlok'))
    sorok.append('')
    hiba_van = False
    for nev in sorted(eredmeny.keys(), key=lambda n: int(n[1:])):
        talalatok = eredmeny[nev]
        hiba_szamu = sum(1 for t in talalatok if t.szint == 'HIBA')
        jelentes_szamu = len(talalatok) - hiba_szamu
        cim_reszek = []
        if hiba_szamu:
            cim_reszek.append('HIBA: %d' % hiba_szamu)
        if jelentes_szamu:
            cim_reszek.append('JELENTES: %d' % jelentes_szamu)
        if not cim_reszek:
            cim_reszek.append('0 talalat')
        sorok.append('## %s (%s)' % (nev, ', '.join(cim_reszek)))
        if nev == 'E16' and esemeny == 'push':
            sorok.append('- %s' % E16_PUSH_MEGJEGYZES)
        if nev == 'E28':
            # F116: a futás egy-soros megjegyzései (pl. "E28: 0 migrált nézet")
            for jegyzet in SZ.E28_JEGYZETEK:
                sorok.append('- %s' % jegyzet)
        for t in talalatok[:minta_db]:
            sorok.append('- `%s` `%s:%s` -- %s' % (t.szint, t.fajl, t.sor, t.reszlet))
        if len(talalatok) > minta_db:
            sorok.append('- ... es tovabbi %d' % (len(talalatok) - minta_db))
        sorok.append('')
        if hiba_szamu:
            hiba_van = True
    return '\n'.join(sorok), hiba_van


def annotaciok_kiirasa(talalatok):
    """F40: az E27 talalatai GitHub-annotaciokent (stderr), sorszammal, hogy a
    PR-ban a sorra mutassanak. Csak GitHub Actions alatt."""
    if not os.environ.get('GITHUB_ACTIONS'):
        return
    for t in talalatok:
        if t.szint not in ('HIBA', 'FIGYELMEZTETES'):
            continue  # a regi (JELENTES) talalat nem annotal: csak a jelentesben
        szint = 'error' if t.szint == 'HIBA' else 'warning'
        sor = ',line=%d' % t.sor if t.sor else ''
        uzenet = ('E27: %s' % t.reszlet).replace('%', '%25').replace('\r', '%0D').replace('\n', '%0A')
        print('::%s file=%s%s::%s' % (szint, t.fajl, sor, uzenet), file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--valtozott', nargs='*', default=[])
    ap.add_argument('--teljes', action='store_true')
    ap.add_argument('--diff-alap', default=None)
    ap.add_argument('--diff-fej', default=None)
    ap.add_argument('--pr-cim', default='')
    ap.add_argument('--esemeny', default='',
                    help='a GitHub-esemeny neve (pl. push, pull_request); push-esemenynel az E16 nem ertelmezett')
    ap.add_argument('--commit-uzenet', default='')
    ap.add_argument(
        '--commit-uzenet-fajl', default=None,
        help=(
            'Fajl, amelynek tartalma a PR osszes commit-uzenete '
            '(base..head, osszefuzve). Ekezetes/idezojeles szoveg miatt '
            'biztonsagosabb, mint a --commit-uzenet shell-argumentum '
            '(l. CLAUDE.md "Shell" szakasz). Ha meg van adva, felulirja '
            'a --commit-uzenetet.'
        ),
    )
    ap.add_argument('--minta', type=int, default=3)
    args = ap.parse_args()

    if not args.teljes and not args.valtozott:
        print('Hiba: --teljes vagy --valtozott FAJL... kotelezo.', file=sys.stderr)
        return 2

    valtozott_relativ = []
    for f in args.valtozott:
        rel = os.path.relpath(os.path.abspath(f), ROOT).replace(os.sep, '/')
        valtozott_relativ.append(rel)

    commit_uzenet = args.commit_uzenet
    if args.commit_uzenet_fajl:
        with open(args.commit_uzenet_fajl, encoding='utf-8') as f:
            commit_uzenet = f.read()

    with HelyiZar('futtat.py %s' % ('--teljes' if args.teljes else '--valtozott (%d fájl)' % len(valtozott_relativ))):
        eredmeny = fut(
            valtozott_relativ, args.teljes,
            diff_alap=args.diff_alap, diff_fej=args.diff_fej,
            pr_cim=args.pr_cim, commit_uzenet=commit_uzenet, esemeny=args.esemeny,
        )
    szoveg, hiba_van = jelentes_szoveg(eredmeny, args.teljes, args.minta, args.esemeny)
    print(szoveg)
    annotaciok_kiirasa(eredmeny.get('E27', []))
    return 1 if hiba_van else 0


if __name__ == '__main__':
    sys.exit(main())
