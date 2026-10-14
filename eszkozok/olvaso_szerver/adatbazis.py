"""A pardes.db csak olvasó kapcsolata (#76 M2, M0 3.5/3.6).

- `mode=ro` URI és `PRAGMA query_only=ON`: írni nem lehet;
- `set_authorizer`: a kiadás által kizárt táblák olvasását az SQLite megtiltja (SQLITE_DENY), tehát a kizárás
  nem csak a megjelenítésen múlik; a tiltott olvasási kísérleteket az objektum naplózza (`kiserletek`);
- szálanként egy kapcsolat (`thread-local`), mert az sqlite3 kapcsolat nem osztható szálak közt.
Az SQL szövegét kizárólag a `lekerdezesek.py` tartalmazza.
"""
import os
import sqlite3
import threading

SQLITE_OK = 0
SQLITE_DENY = 1
SQLITE_READ = 20

GY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/') + '/'

KIADASOK = ('belso', 'nyilvanos', 'kereskedelmi')
# tábla -> a kiadások, amelyekből kimarad (DT124): a KJV-Strong-címkék GPL-eredetűek, az MCGED nem kereskedelmi
TABLA_KIZARAS = {'kjv': ('nyilvanos', 'kereskedelmi'), 'mcged': ('kereskedelmi',)}


def kizart_tablak(kiadas):
    return frozenset(t for t, k in TABLA_KIZARAS.items() if kiadas in k)


class Adatbazis:
    """Egy kiadáshoz kötött, csak olvasó kapcsolat-gyár."""

    def __init__(self, ut, kiadas='belso', mmap_bajt=0):
        if kiadas not in KIADASOK:
            raise ValueError('ismeretlen kiadás: %r (%s)' % (kiadas, ', '.join(KIADASOK)))
        self.ut = ut.replace('\\', '/')
        if not os.path.exists(self.ut):
            raise FileNotFoundError('nincs adatbázis: %s' % self.ut)
        self.kiadas = kiadas
        self.kizart = kizart_tablak(kiadas)
        self.mmap_bajt = mmap_bajt
        self._lokal = threading.local()
        self.kiserletek = []          # a tiltott olvasási kísérletek (tábla); a teszt ezt nézi
        self._zar = threading.Lock()

    def _authorizer(self, action, arg1, arg2, dbname, forras):
        if action == SQLITE_READ and arg1 in self.kizart:
            with self._zar:
                self.kiserletek.append(arg1)
            return SQLITE_DENY
        return SQLITE_OK

    def _uj(self):
        con = sqlite3.connect('file:%s?mode=ro' % self.ut, uri=True, check_same_thread=False)
        con.execute('PRAGMA query_only=ON')
        if self.mmap_bajt:
            con.execute('PRAGMA mmap_size=%d' % int(self.mmap_bajt))
        con.set_authorizer(self._authorizer)
        return con

    def kapcsolat(self):
        con = getattr(self._lokal, 'con', None)
        if con is None:
            con = self._lokal.con = self._uj()
        return con

    def bezar(self):
        con = getattr(self._lokal, 'con', None)
        if con is not None:
            con.close()
            self._lokal.con = None
