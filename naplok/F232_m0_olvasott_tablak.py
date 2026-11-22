"""F232 M0: mely táblákat olvassa a mintakészlet oldala a pardes.db-n (sqlite authorizer). Csak olvas."""
import json
import os
import sys
import time

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

SZ = os.environ['SZERVER']
sys.path.insert(0, SZ)
import adatbazis
import alkalmazas

OLV = {}
akt = [None]
orig = adatbazis.Adatbazis._authorizer


def aut(self, action, arg1, arg2, dbname, forras):
    if action == adatbazis.SQLITE_READ and akt[0] is not None:
        OLV.setdefault(akt[0], set()).add(arg1)
    return orig(self, action, arg1, arg2, dbname, forras)


adatbazis.Adatbazis._authorizer = aut
app = alkalmazas.letrehoz(db_ut=os.environ['PARDES_DB'], kiadas='belso')
c = app.test_client()
oldalak = (['/szo/' + s for s in 'H1242 H7451 H3615 H0251 H7837 H2398 G0264 G3056 G1311 G2671'.split()]
           + ['/1Moz/1/1', '/1Moz/1/5', '/1Moz/3/6', '/1Moz/4/7', '/Zsolt/22/2', '/Jn/1/1', '/1Moz/1', '/Zsolt/22'])
ido = {}
for u in oldalak:
    akt[0] = u
    t = time.time()
    r = c.get(u)
    ido[u] = (r.status_code, len(r.get_data()), round(time.time() - t, 2))
akt[0] = None
mind = set()
for u in oldalak:
    print(u, ido[u], sorted(OLV.get(u, [])))
    mind |= OLV.get(u, set())
print('OSSZES TABLA', len(mind), sorted(mind))
json.dump(sorted(mind), open(os.environ['KI'], 'w'))
