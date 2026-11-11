"""forditas_vedelem.py — a meglévő érvényes fordítás nem fordul újra (F182, 2. fázis, F31): egy szabály, egy hely.

A fordítóláncok (`glossza_api_koteg.beir`: TBESG/UBS-glossza; `thayer_jelolt/forditas.beir`: Thayer-szakaszok;
`emeles.cmd_beir`: BDB) a `adat/forditasok.tsv` meglévő sorát csak akkor írhatják felül, ha az elavult (`allapot` =
`elavult`), vagy a forrása azóta változott (más `forras_hash`). Az érvényes, ugyanarra a forrásszövegre készült fordítás
soha nem fordul újra; a jóváhagyott kézi csere (`kezi` új sor, a lánc kifejezett kapcsolójával) kivétel. A pótlás listája
a tábla `allapot` mezőjéből számolódik (a hiányzó és az elavult sor), nem korábbi listából.

Csak standard könyvtár.
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')


def ervenyes_ujraforditas(regi, uj, fejlec):
    """True, ha az `uj` sor (cellák listája) egy érvényes, ugyanarra a forrásra készült `regi` sort írna felül modell-
    fordítással: ezt a lánc nem teheti (F31). A `kezi` új sor (jóváhagyott csere) nem ilyen."""
    i_all, i_hash, i_hu = fejlec.index('allapot'), fejlec.index('forras_hash'), fejlec.index('forditas_hu')
    if len(regi) <= max(i_all, i_hash, i_hu) or len(uj) <= max(i_all, i_hash):
        return False
    if uj[i_all] == 'kezi':
        return False
    return regi[i_all] != 'elavult' and bool(regi[i_hu].strip()) and regi[i_hash] == uj[i_hash]


def ellenoriz(regi, uj, fejlec, kulcs):
    """SystemExit, ha az `uj` sor érvényes fordítást fordítana újra (F31)."""
    if ervenyes_ujraforditas(regi, uj, fejlec):
        raise SystemExit('%s: érvényes fordítás ugyanarra a forrásra (allapot=%s) — nem fordul újra (F31); a pótlás csak '
                         'a hiányzó és az elavult sort érinti' % ('|'.join(kulcs), regi[fejlec.index('allapot')]))
