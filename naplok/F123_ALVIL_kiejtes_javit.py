"""F123.ALVIL.Z1: a kézi forrás négy görög szavának kiejtése (ALVIL-001, Feed 6. kapu).

A kiejtés-szabály (`eszkozok/kiejtes_szoveg.py`, F125 22. szabály): szakaszonként az első előfordulásnál a szó után
zárójelben a kiejtés. Görögül gépi magyaros átírás, jóváhagyás nélkül (DT430); a lap prózájának alakját követi
(*hádész*, *abüsszosz*; a F152.3 a Kivonat ᾍδης-ét már így írta). Minta: `naplok/F152_kiejtes_javit.py`.
Csak a négy cserét végzi, egyenként pontosan egyszer; eltérésnél megáll, és nem ír.
"""
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAJL = os.path.join(GYOKER, 'motivumok', 'ALVIL-001.md')

CSERE = [
    ('(*tehóm*)/ἄβυσσος kozmikus', '(*tehóm*)/ἄβυσσος (*abüsszosz*) kozmikus'),
    ('**ᾍδης — *hádész*** (görög, eredetileg', '**ᾍδης** (*hádész*, görög, eredetileg'),
    ('ugyanazt a szót (ᾍδης) használja', 'ugyanazt a szót — ᾍδης (*hádész*) — használja'),
    ('**Mt 16:18** (ᾍδης, „a pokol kapui”, ekkleziológiai kontextus):',
     '**Mt 16:18** — ᾍδης (*hádész*), „a pokol kapui”, ekkleziológiai kontextus:'),
]


def main():
    with io.open(FAJL, encoding='utf-8', newline='') as f:
        s = f.read()
    for regi, uj in CSERE:
        if s.count(regi) != 1:
            sys.exit('HIBA: nem pontosan egyszer áll: %r (%d)' % (regi, s.count(regi)))
        s = s.replace(regi, uj)
    with io.open(FAJL, 'w', encoding='utf-8', newline='') as f:
        f.write(s)
    print('kész: %d csere' % len(CSERE))


if __name__ == '__main__':
    main()
