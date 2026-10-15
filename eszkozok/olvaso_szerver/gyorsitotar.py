"""Korlátos LRU-gyorsítótár a kész lapokra (#76 M2, M0 3.8): legfeljebb `max_lap` lap vagy `max_bajt` bájt."""
import hashlib
import threading
from collections import OrderedDict


class Gyorsitotar:
    def __init__(self, max_lap=512, max_bajt=64 * 1024 * 1024):
        self.max_lap = max_lap
        self.max_bajt = max_bajt
        self._d = OrderedDict()
        self._bajt = 0
        self._zar = threading.Lock()
        self.talalat = 0
        self.melle = 0

    @staticmethod
    def etag(kulcs):
        return '"%s"' % hashlib.sha256(repr(kulcs).encode('utf-8')).hexdigest()[:24]

    def kap(self, kulcs):
        with self._zar:
            v = self._d.get(kulcs)
            if v is None:
                self.melle += 1
                return None
            self._d.move_to_end(kulcs)
            self.talalat += 1
            return v

    def tesz(self, kulcs, html):
        meret = len(html.encode('utf-8'))
        if meret > self.max_bajt:
            return
        with self._zar:
            if kulcs in self._d:
                self._bajt -= len(self._d[kulcs].encode('utf-8'))
            self._d[kulcs] = html
            self._d.move_to_end(kulcs)
            self._bajt += meret
            while self._d and (len(self._d) > self.max_lap or self._bajt > self.max_bajt):
                _, r = self._d.popitem(last=False)
                self._bajt -= len(r.encode('utf-8'))

    def urit(self):
        """Minden lap törlése (a tervező mód mentése után, #98 M2: a régi kulcsok úgyis elérhetetlenek)."""
        with self._zar:
            self._d.clear()
            self._bajt = 0

    def meret(self):
        return len(self._d), self._bajt
