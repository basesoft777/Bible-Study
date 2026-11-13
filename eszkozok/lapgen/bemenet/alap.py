"""lapgen.bemenet.alap — a lap keretéhez tartozó kis bemenetek."""
from lapgen.szoveg import MotivumId


def b59_befagyasztott(b):
    """B59 — a befagyasztott motívumok halmaza (futásidőben olvasva, nem importkor)."""
    tabla = b._tabla('B59', oszlopok=('id',))
    i = tabla.oszlop('id')
    return frozenset(MotivumId(sor[i]) for sor in tabla.sorok)
