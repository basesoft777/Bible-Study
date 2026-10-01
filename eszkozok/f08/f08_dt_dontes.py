"""f08_dt_dontes.py -- F8.8/F8.10: a DT23 Dontes es Allapot oszlopanak kitoltese (a felhasznalo 2026.09.30-i dontese).
CRLF-hu iras; csak a DT23 sor vegzodeset csereli (a 🟡 allapotut, vagy az F8.8-as ✅ szoveget az F8.10-esre).
Futtatas: python eszkozok/f08/f08_dt_dontes.py
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UT = os.path.join(GYOKER, 'DONTESEK.md')

REGI_VEG = '| 🟡 | | `naplok/F08_zaras.md`, `naplok/ELLENOR_F08.md` |'
# az F8.8-as kitoltes eleje (F8.10: erre cserel)
F88_KEZDET = '| ✅ | Felhasználó, 2026.09.30: '
UJ_VEG = (
    '| ✅ | '
    'Felhasználó, 2026.09.30: „(d) elfogadva, feltétel: az LD001–LD004 renderje nem változik (nulla-diff vagy CI igazolja). '
    '(g) külön menet, N-F08 helyőrzővel a NYITOTT_FELADATOK.md-be. (f) a kulcs a TAHOT H7497, a Macula H7498 megjegyzésként; '
    'ahol a vers személynévi Rafa (1Krón 8), a besorolás valószínű. A többi pont a javasolt alapértelmezés szerint.” '
    '**Alkalmazva (F8.8, F8.10):** (a) a 9 sor marad `valoszinu`, nem jelenik meg; '
    '(b) LD027 καταράομαι G2672, LD035 ἀσέβεια G0763, LD052 Ραφαϊν (`eltero_forditas`), LD050 `lxx_minusz` a munkalap-szóra — kitöltve, `valoszinu` (a brief „biztos” definíciója nem teljesül), proveniencia `dontes=DT23(b)`; LD027, LD035, LD052: ellentmondásos források (Macula_heber és LXX_OS), felhasználói döntéssel feloldva, `feloldas=DT23` (SEMA 2.11, `ellenoriz.py` 10. szabály); LD050: egy forrás (a Macula nem illeszt, nem ellentmond), `feloldas=` nélkül; LD009, LD058, LD064, LD008 marad nyitott; '
    '(c) → ~~külön tétel~~ **N-F08a** (NYITOTT_FELADATOK.md, helyőrző az F30 szerint); '
    '(d) elfogadva; a feltétel (nulla-diff vagy CI igazolja) teljesült: nulladiff a main-nel összefésülve, `naplok/F08_nulladiff.txt` — az LD001–LD004-et renderelő ISTENTISZT-001_TUDOMANYOS.md és a 8 TORZSCIKK -0/+0, soronként azonos; az eltérés csak az LXX-sorok (+61 „eltérő”) és a forráslista; '
    '(e) → ~~külön tétel~~ **N-F08b**; '
    '(f) a `heber_strong` a TAHOT H7497, a Macula H7498 a megjegyzésben; az 1Krón 8 (személynévi Rafa) nincs a 87 hely között, a szabály jelenleg tárgytalan; '
    '(g) nincs teendő (a DT7 (a) nem hat ki); a felhasználó „(g) külön menet, N-F08” mondatát az orkesztrátor a (c)/(e) külön tételeire vonatkoztatta, így N-F08a/N-F08b lett; '
    '(h), (j) tudomásul véve; (i) marad G2672. '
    'Új besorolás: biztos 61, valószínű 13, nyitott 4, nem_alkalmazhato 8. '
    '| `naplok/F08_zaras.md`, `naplok/ELLENOR_F08.md`, `naplok/F08_nulladiff.txt` |'
)


def main():
    with io.open(UT, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorok = nyers.split('\r\n')
    idx = [i for i, s in enumerate(sorok) if s.startswith('| DT23 |')]
    if len(idx) != 1:
        print('DT23 sor nem egyertelmu')
        sys.exit(1)
    s = sorok[idx[0]]
    if s.endswith(UJ_VEG):
        print('a DT23 mar a vegleges szoveget tartalmazza')
        return
    if s.endswith(REGI_VEG):
        sorok[idx[0]] = s[:-len(REGI_VEG)] + UJ_VEG
    elif s.count(F88_KEZDET) == 1:
        sorok[idx[0]] = s[:s.index(F88_KEZDET)] + UJ_VEG
    else:
        print('a DT23 sor vege nem a vart')
        sys.exit(1)
    with io.open(UT, 'w', encoding='utf-8', newline='') as f:
        f.write('\r\n'.join(sorok))
    print('DT23: Dontes kitoltve, allapot ✅')


if __name__ == '__main__':
    main()
