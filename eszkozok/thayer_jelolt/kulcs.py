#!/usr/bin/env python
"""A Thayer Strong-kulcsának egyetlen normalizáló függvénye (F132, FELADATOK #132; DT-F132b (4)).

A `Thayer.lexicon` `Topic`-ja kitöltés nélküli (`G12`, `G1941`), az adatréteg és a `Thayer_teljes.tsv`
`Strong_padded`-et használ (`G0012`). Normalizálás nélkül a kulcs-összevetés néma nem-találatot ad
(mért, M0: G0012, G0086, G0282, G0813). A `thayer_jelolt` minden eszköze innen importál; máshol nincs
saját normalizálás (`teszt_bont.py` ellenőrzi).
"""
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

_MINTA = re.compile(r'^\s*([Gg])0*(\d{1,4})\s*$')


def strong_pad(s):
    """`G12` / `G0012` / `g12` -> `G0012`; nem görög Strong-alakra None (nem kivétel: a hívó dönt)."""
    m = _MINTA.match(s or '')
    if not m or int(m.group(2)) == 0:
        return None
    return 'G%04d' % int(m.group(2))


def strong_eredeti(s):
    """`G0012` -> `G12` (a `Thayer.lexicon` `Topic`-ja és a `forditasok.tsv` `entry_id`-je)."""
    p = strong_pad(s)
    return None if p is None else 'G%d' % int(p[1:])
