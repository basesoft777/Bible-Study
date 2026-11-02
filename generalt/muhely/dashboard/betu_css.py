#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F156: a Dashboard betű-CSS-ei (data: URL) az olvasó-szerver OFL betűfájljaiból (latin + latin-ext).
Használat: python generalt/muhely/dashboard/betu_css.py <kimeneti könyvtár>"""
import base64
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
F = os.path.join(GYOKER, 'eszkozok', 'olvaso_szerver', 'statikus', 'fonts')
css_src = open(os.path.join(F, '..', 'fonts.css'), encoding='utf-8').read()
SPEC = [
    ('serif-latin.css', 'Source Serif 4', '400 600', 'SourceSerif4-normal-400-600-latin.woff2'),
    ('serif-latext.css', 'Source Serif 4', '400 600', 'SourceSerif4-normal-400-600-latin-ext.woff2'),
    ('sans-latin.css', 'IBM Plex Sans', '400 600', 'IBMPlexSans-normal-400-600-latin.woff2'),
    ('sans-latext.css', 'IBM Plex Sans', '400 600', 'IBMPlexSans-normal-400-600-latin-ext.woff2'),
    ('mono-latin.css', 'IBM Plex Mono', '400', 'IBMPlexMono-normal-400-latin.woff2'),
]


def ranges(fname):
    i = css_src.index('fonts/' + fname)
    blk = css_src[css_src.rfind('@font-face', 0, i):css_src.index('}', i)]
    return re.search(r'unicode-range: ([^;]+);', blk).group(1)


out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for nev, fam, suly, fajl in SPEC:
    b = base64.b64encode(open(os.path.join(F, fajl), 'rb').read()).decode()
    css = ("/* %s, %s; SIL Open Font License 1.1 */\n@font-face{font-family:'%s';font-style:normal;font-weight:%s;"
           "font-display:swap;src:url(data:font/woff2;base64,%s) format('woff2');unicode-range:%s;}\n"
           % (fam, fajl, fam, suly, b, ranges(fajl)))
    open(os.path.join(out, nev), 'w', encoding='utf-8', newline='\n').write(css)
    print(nev, len(css))
