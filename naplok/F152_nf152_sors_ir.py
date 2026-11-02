"""F152.23: az N-F152a–g tételek sorsa a #152 lezárásakor (NYITOTT_FELADATOK.md).

Egyik tétel sem zárul: mindegyik sor végére egy jegyzet kerül arról, hova tartozik.
A sorvég a fájlé (newline='' olvasás és írás; a main-en LF).
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

UT = 'NYITOTT_FELADATOK.md'
E = ' *(F152 zárás, 2026.11.02: %s)*'
SORS = {
    'N-F152a': 'nyitva marad; rendszerszintű olvasó-szerver tétel (#149-cel), nem az ISTENTISZT-001 2. kiadásának feltétele',
    'N-F152b': 'nyitva marad; szerkezeti döntés minden lexikonra, nem az ISTENTISZT-001 2. kiadásának feltétele',
    'N-F152c': '**az ISTENTISZT-001 2. kiadására tartozik**, a lektori kérdésekkel (`naplok/KIADAS_ISTENTISZT-001_lektor.md`) együtt (DT-F152d)',
    'N-F152d': 'nyitva marad, részben megvalósult: a #125 a mérőt (`eszkozok/proza_lefedettseg.py`, DT471) és a MUNKAMENET C-z lépését elkészítette; a JELENTÉS szintű ellenőrző-szabály (az `ellenorzes/` alatt) nincs meg. A lezárás a hiányzó rész ellenőrzése után',
    'N-F152e': 'nyitva marad, részben megvalósult: a (2) a MUNKAMENET C-w lépése (#125); az (1), a motívumonkénti értelmező feladat mint a „kész” állapot feltétele, nincs rögzítve',
    'N-F152f': 'nyitva marad; generátor-tétel minden lexikonra, nem az ISTENTISZT-001 2. kiadásának feltétele',
    'N-F152g': 'nyitva marad; a `sablonok/`-ban kilenclépéses prózasablon nincs (a #125 körébe tartozik)',
}

with open(UT, encoding='utf-8', newline='') as f:
    szoveg = f.read()
NL = '\r\n' if '\r\n' in szoveg else '\n'
sorok = szoveg.split(NL)
db = 0
for i, s in enumerate(sorok):
    for k, v in SORS.items():
        if s.startswith('* **ÚJ (F152, 2026.11.01) — %s:' % k):
            assert 'F152 zárás' not in s
            sorok[i] = s + E % v
            db += 1
assert db == 7, db
with open(UT, 'w', encoding='utf-8', newline='') as f:
    f.write(NL.join(sorok))
print('NYITOTT: 7 N-F152 tétel jegyzetet kapott')
