"""lapgen.bekotes — a kész szakaszok bekötése a szakaszrendbe.

Egy szakasz akkor kerül ide, amikor a szelete elkészült: a számító függvény a `szamitas/`, a megjelenítő
a `megjelenites/md/` alól jön.
"""


from lapgen.megjelenites.md import dontesi_ut as md_dontesi_ut
from lapgen.megjelenites.md import eleje as md_eleje
from lapgen.megjelenites.md import elofordulas as md_elofordulas
from lapgen.megjelenites.md import hatastortenet as md_hatastortenet
from lapgen.megjelenites.md import idezes as md_idezes
from lapgen.megjelenites.md import kapcsolatok as md_kapcsolatok
from lapgen.megjelenites.md import kereszthiv as md_kereszthiv
from lapgen.megjelenites.md import kizarasok as md_kizarasok
from lapgen.megjelenites.md import kolofon as md_kolofon
from lapgen.megjelenites.md import lxx as md_lxx
from lapgen.megjelenites.md import resek as md_resek
from lapgen.megjelenites.md import szocikkek as md_szocikkek
from lapgen.szamitas import dontesi_ut as sz_dontesi_ut
from lapgen.szamitas import eleje as sz_eleje
from lapgen.szamitas import elofordulas as sz_elofordulas
from lapgen.szamitas import hatastortenet as sz_hatastortenet
from lapgen.szamitas import idezes as sz_idezes
from lapgen.szamitas import kapcsolatok as sz_kapcsolatok
from lapgen.szamitas import kereszthiv as sz_kereszthiv
from lapgen.szamitas import kizarasok as sz_kizarasok
from lapgen.szamitas import kolofon as sz_kolofon
from lapgen.szamitas import lxx as sz_lxx
from lapgen.szamitas import resek as sz_resek
from lapgen.szamitas import szocikkek as sz_szocikkek


def bekot(rend):
    """A kész szakaszok bekötése."""
    rend.bekot(md_eleje.FEJ, sz_eleje.szamit_fej, md_eleje.megjelenit_fej)
    rend.bekot(md_eleje.KIVONAT, sz_eleje.szamit_kivonat, md_eleje.megjelenit_kivonat)
    rend.bekot(md_eleje.TARTALOM, sz_eleje.szamit_ures, md_eleje.megjelenit_tartalom)
    rend.bekot(md_eleje.JELMAGYARAZAT, sz_eleje.szamit_ures, md_eleje.megjelenit_jelmagyarazat)
    rend.bekot(md_dontesi_ut.AZONOSITO, sz_dontesi_ut.szamit, md_dontesi_ut.megjelenit, kapu=sz_dontesi_ut.kapu)
    rend.bekot(md_elofordulas.AZONOSITO, sz_elofordulas.szamit, md_elofordulas.megjelenit)
    rend.bekot(md_szocikkek.AZONOSITO, sz_szocikkek.szamit, md_szocikkek.megjelenit, kapu=sz_szocikkek.kapu)
    rend.bekot(md_resek.AZONOSITO_MIERT_FONTOS, sz_resek.szamit_miert_fontos, md_resek.megjelenit_miert_fontos)
    rend.bekot(md_lxx.AZONOSITO, sz_lxx.szamit, md_lxx.megjelenit)
    rend.bekot(md_kereszthiv.AZONOSITO, sz_kereszthiv.szamit, md_kereszthiv.megjelenit, kapu=sz_kereszthiv.kapu)
    rend.bekot(md_kapcsolatok.AZONOSITO, sz_kapcsolatok.szamit, md_kapcsolatok.megjelenit, kapu=sz_kapcsolatok.kapu)
    rend.bekot(md_kapcsolatok.AZONOSITO_KAPCSOLODO, sz_kapcsolatok.szamit_kapcsolodo,
               md_kapcsolatok.megjelenit_kapcsolodo, kapu=sz_kapcsolatok.kapu_kapcsolodo)
    rend.bekot(md_hatastortenet.AZONOSITO, sz_hatastortenet.szamit, md_hatastortenet.megjelenit)
    rend.bekot(md_resek.AZONOSITO_ERTELMEZES, sz_resek.szamit_ertelmezes, md_resek.megjelenit_ertelmezes)
    rend.bekot(md_resek.AZONOSITO_MODSZERTAN, sz_resek.szamit_modszertan, md_resek.megjelenit_modszertan)
    rend.bekot(md_idezes.AZONOSITO, sz_idezes.szamit, md_idezes.megjelenit, gyujto=True)
    rend.bekot(md_kolofon.AZONOSITO, sz_kolofon.szamit, md_kolofon.megjelenit, kapu=sz_kolofon.kapu, gyujto=True)
    rend.bekot(md_kizarasok.AZONOSITO, sz_kizarasok.szamit, md_kizarasok.megjelenit, kapu=sz_kizarasok.kapu)
    return rend
