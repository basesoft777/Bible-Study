"""lapgen.megjelenites.md.keret — a szakaszok közös kerete: címsor, a generált blokk nyitó és záró jelölője.

A jelölő proveniencia (megjegyzés): a forrás- és licenclista a szakasz valódi olvasásaiból jön (GK-07).
"""
from lapgen import konfig
from lapgen.megjelenites.md.iro import OLVASOI_JEL
from lapgen.szoveg import cim_horgony, prov


def _szamozott_cim(keret, azonosito):
    return keret.ny.s('cim.szamozott', sorszam=keret.rend.sorszam(azonosito),
                      cim=keret.ny.s(keret.rend.cim_kulcs(azonosito)))


def szakasz_cim(iro, keret, azonosito):
    """A számozott szakasz 2. szintű címsora a szakaszrendből, utána üres sor."""
    iro.cimsor(2, _szamozott_cim(keret, azonosito))
    iro.ures()


def szakasz_horgony(keret, azonosito):
    """A számozott szakasz címsorának horgonya: a szakaszrendből és a címből, nem kódba írt számból."""
    return cim_horgony(_szamozott_cim(keret, azonosito))


def blokk_nyit(iro, keret, azonosito, forrasok):
    """A generált blokk nyitó jelölője, utána üres sor."""
    iro.sor(prov('GENERÁLT-KEZDET: {}#{}#{} | forrás: {} | licenc: {} | {}', konfig.GENERATOR_JELOLO,
                 keret.motivum, azonosito, forrasok.utvonalak, forrasok.licencek, keret.ts))
    iro.ures()


def blokk_zar(iro, keret, azonosito):
    """A generált blokk záró jelölője, utána üres sor."""
    iro.sor(prov('GENERÁLT-VÉGE: {}#{}#{}', konfig.CEL_NEV, keret.motivum, azonosito))
    iro.ures()


def olvasoi_bekezdes(iro, szoveg):
    """Olvasói bekezdés: a sor végén a láthatatlan jelölővel, utána üres sor."""
    iro.sor(szoveg, OLVASOI_JEL)
    iro.ures()
