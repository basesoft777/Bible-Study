"""Hozzáférési szintek konfigurációból (#76 M2, M0 3.5).

A kódban csak a mechanizmus van; a szintek és a blokk–szint hozzárendelés a `konfig/hozzaferes.toml`-ban.
Biztonsági irány: ha a blokk-id nem szerepel a regiszterben, a blokk a LEGMAGASABB szintre esik (nem a
legalacsonyabbra); ismeretlen szintnévnél az indulás hibával megáll.
"""
import os
import tomllib

KONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'konfig')


class Hozzaferes:
    def __init__(self, szintek, alap_szint, blokk_szint, default):
        if not szintek or len(set(szintek)) != len(szintek):
            raise ValueError('hozzaferes.toml: a szintek lista üres vagy ismétlődik')
        self.szintek = list(szintek)
        self.rang = {n: i for i, n in enumerate(self.szintek)}
        if alap_szint not in self.rang:
            raise ValueError('hozzaferes.toml: ismeretlen alapertelmezett_szint: %r' % alap_szint)
        if default not in self.rang:
            raise ValueError('hozzaferes.toml: ismeretlen default szint: %r' % default)
        for b, n in blokk_szint.items():
            if n not in self.rang:
                raise ValueError('hozzaferes.toml: a(z) %r blokk ismeretlen szintje: %r' % (b, n))
        self.alap_szint = alap_szint
        self.blokk_szint = dict(blokk_szint)
        self.default = default

    @classmethod
    def betolt(cls, konfig_dir=None, fajl='hozzaferes.toml'):
        """`fajl`: az éles konfig a `hozzaferes.toml`; a tesztek saját próba-konfigja (`hozzaferes_proba.toml`) ugyanezen a könyvtáron át tölthető."""
        ut = os.path.join(konfig_dir or os.environ.get('PARDES_KONFIG_DIR') or KONFIG_DIR, fajl)
        with open(ut, 'rb') as f:
            c = tomllib.load(f)
        b = dict(c.get('blokk', {}))
        default = b.pop('default', c['szintek'][0])
        return cls(c['szintek'], c['alapertelmezett_szint'], b, default)

    def ellenoriz_blokkok(self, ismert_idk):
        """A konfigban szereplő minden blokk-azonosítónak a regiszterben kell lennie; különben ValueError (indulási hiba)."""
        ismeretlen = sorted(set(self.blokk_szint) - set(ismert_idk))
        if ismeretlen:
            raise ValueError('hozzaferes.toml: ismeretlen blokk-azonosító(k): %s' % ', '.join(ismeretlen))

    def szint(self, kerés=None):
        """A kérés szintje (rang). Belépés nincs: az alapértelmezett szint; később a bejelentkezés cseréli le."""
        return self.rang[self.alap_szint]

    def szint_nevbol(self, nev):
        """A szintnév rangja, vagy None, ha ismeretlen (a szintváltó süti értékének ellenőrzése)."""
        return self.rang.get(nev)

    def szint_neve(self, rang):
        return self.szintek[rang]

    def blokk_min_szint(self, blokk_id, ismert=True):
        """A blokk legkisebb szintje (rang). Ismeretlen blokk-id: a legmagasabb szint."""
        if not ismert:
            return len(self.szintek) - 1
        return self.rang[self.blokk_szint.get(blokk_id, self.default)]

    def lathato(self, blokk_id, kerelo_szint, ismert=True):
        return kerelo_szint >= self.blokk_min_szint(blokk_id, ismert)
