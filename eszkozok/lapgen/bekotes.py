"""lapgen.bekotes — a kész szakaszok bekötése a szakaszrendbe.

Egy szakasz akkor kerül ide, amikor a szelete elkészült: a számító függvény a `szamitas/`, a megjelenítő
a `megjelenites/md/` alól jön.
"""


from lapgen.megjelenites.md import elofordulas as md_elofordulas
from lapgen.szamitas import elofordulas as sz_elofordulas


def bekot(rend):
    """A kész szakaszok bekötése."""
    rend.bekot(md_elofordulas.AZONOSITO, sz_elofordulas.szamit, md_elofordulas.megjelenit)
    return rend
