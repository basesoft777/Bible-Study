"""lapgen.bekotes — a kész szakaszok bekötése a szakaszrendbe.

Egy szakasz akkor kerül ide, amikor a szelete elkészült: a számító függvény a `szamitas/`, a megjelenítő
a `megjelenites/md/` alól jön.
"""


from lapgen.megjelenites.md import dontesi_ut as md_dontesi_ut
from lapgen.megjelenites.md import elofordulas as md_elofordulas
from lapgen.megjelenites.md import kizarasok as md_kizarasok
from lapgen.szamitas import dontesi_ut as sz_dontesi_ut
from lapgen.szamitas import elofordulas as sz_elofordulas
from lapgen.szamitas import kizarasok as sz_kizarasok


def bekot(rend):
    """A kész szakaszok bekötése."""
    rend.bekot(md_dontesi_ut.AZONOSITO, sz_dontesi_ut.szamit, md_dontesi_ut.megjelenit, kapu=sz_dontesi_ut.kapu)
    rend.bekot(md_elofordulas.AZONOSITO, sz_elofordulas.szamit, md_elofordulas.megjelenit)
    rend.bekot(md_kizarasok.AZONOSITO, sz_kizarasok.szamit, md_kizarasok.megjelenit, kapu=sz_kizarasok.kapu)
    return rend
