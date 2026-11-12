"""A befagyasztott lexikonlapok jegyzéke (F212, DT-F212a): egy hely, gépileg olvasható.

A befagyasztott motívum lapja (`lexikon/<ID>_TUDOMANYOS.md`) a generátor javításai után nem generálódik újra: új
cikkként, nulláról készül majd (F123). Az adata és a forrása a helyén marad, a nyílt magban az adata benne marad.
A jegyzéket a generátor (`lexikon_general.run`: nem írja a lapot), az E28 (`ellenorzes/szabalyok.py`: nem veti össze)
és az állítás–adat kapu (`ellenorzes/allitas_adat.py --minden`: nem méri) olvassa, ebből a függvényből.

Tábla: `adat/lap_befagyasztas.tsv` (SEMA 2.59). Olvasás `split('\t')`-tel (CLAUDE.md, TSV-olvasás).
"""
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(GYOKER, 'adat', 'lap_befagyasztas.tsv')
OSZLOPOK = ['id', 'ok', 'dontes', 'datum']


def sorok(ut=None):
    """A tábla sorai szótárként; hiányzó tábla: üres lista. Hibás fejléc: ValueError."""
    ut = ut or TABLA
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        nyers = [s.rstrip('\r\n') for s in f if s.strip()]
    if not nyers:
        return []
    fej = nyers[0].split('\t')
    if fej != OSZLOPOK:
        raise ValueError('%s: a fejléc %r, várt: %r' % (ut, fej, OSZLOPOK))
    ki = []
    for s in nyers[1:]:
        mezok = s.split('\t')
        if len(mezok) != len(OSZLOPOK):
            raise ValueError('%s: %d mező a(z) %r sorban, várt: %d' % (ut, len(mezok), s[:40], len(OSZLOPOK)))
        ki.append(dict(zip(OSZLOPOK, mezok)))
    return ki


def befagyasztott_idk(ut=None):
    """A befagyasztott motívum-azonosítók halmaza."""
    return {r['id'] for r in sorok(ut) if r['id'].strip()}


def befagyasztott(motivum_id, ut=None):
    return motivum_id in befagyasztott_idk(ut)


if __name__ == '__main__':
    for r in sorok():
        print('%s\t%s' % (r['id'], r['ok']))
