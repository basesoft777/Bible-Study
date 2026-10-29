"""Kiosztott helyőrzők mechanikus cseréje az `eszkozok/` alatt (a szamkiosztas da942af6 szerint):
DT-F121g → DT393, DT-F146b → DT398. Bájtszintű csere (a sorvégek változatlanok); csak azonosító.
Kiírja fájlonként a cserék számát. A felhasználó döntése (orkesztrátor-chat, 2026-10-29): „Igen, mindkettő”.
"""
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CSERE = {b'DT-F121g': b'DT393', b'DT-F146b': b'DT398'}
osszes = 0
for gyoker, _, fajlok in os.walk('eszkozok'):
    for nev in sorted(fajlok):
        if not nev.endswith('.py'):
            continue
        ut = os.path.join(gyoker, nev)
        with open(ut, 'rb') as f:
            regi = f.read()
        uj = regi
        db = {}
        for mit, mire in CSERE.items():
            db[mit.decode()] = uj.count(mit)
            uj = uj.replace(mit, mire)
        if uj != regi:
            with open(ut, 'wb') as f:
                f.write(uj)
            osszes += sum(db.values())
            print(ut.replace(os.sep, '/'), db)
print('összes csere:', osszes)
