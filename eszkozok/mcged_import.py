"""Mounce Concise Greek-English Dictionary (MCGED) import.

F05_SZOTAR_BRIEF.md S6. Forras: konkordancia/lexikonok_nyers/MCGED.lexicon
(SQLite, biblematedata-csomag, l. konkordancia/lexikonok_nyers/README.md).
Csak a `G####` Strong-kulcsu sorokat hasznalja (a `gkG5####`
Goodrick-Kohlenberger-kulcs UGYANAZT a szoveget ismetli meg mas kulcs
alatt -- l. lexikonok_nyers/README.md "Kulcs-formatum elteresek").

CC BY minden jog fenntartva (c) Mounce 1993, www.teknia.com/greek-dictionary
-- a forrasmegjeloles KOTELEZO minden idezetnel (F6 D16).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import hashlib
import os
import re
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')
NYERS_DB = os.path.join(KONKORDANCIA, 'lexikonok_nyers', 'MCGED.lexicon')
KIMENET = os.path.join(KONKORDANCIA, 'MCGED_teljes.tsv')

STRONG_G_RE = re.compile(r'^G\d+$')
TAG_RE = re.compile(r'<[^>]+>')
WS_RE = re.compile(r'\s+')
GK_RE = re.compile(r'lex\("(gkG5\d+)"\)')
LEMMA_RE = re.compile(r'<grk>([^<]*)</grk>')
TRANSLIT_RE = re.compile(r'<b>Transliteration</b>:\s*([^<]*)<br')
FREQ_RE = re.compile(r'<b>Frequency</b>:\s*([^<]*)<br')
DEF_RE = re.compile(r'<b>Definition</b>:\s*(.*?)</p>', re.S)


def clean(s):
    if not s:
        return ''
    s = TAG_RE.sub(' ', s)
    s = s.replace('&amp;', '&').replace('&#39;', "'").replace('&quot;', '"')
    return WS_RE.sub(' ', s).strip()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def parse_row(topic, html):
    # a nyers "gkG50270" a MCGED.lexicon sajat, "gk" elotagu Goodrick-
    # Kohlenberger-kulcsa (lexikonok_nyers/README.md) -- csak a "gk"
    # elotagot vagjuk le, a "G5####" format valtozatlanul hagyjuk.
    m = GK_RE.search(html)
    gk_szam = m.group(1)[2:] if m else ''
    lemma_html = LEMMA_RE.search(html)
    lemma_gorog = clean(lemma_html.group(1)) if lemma_html else ''
    m2 = TRANSLIT_RE.search(html)
    atirat = clean(m2.group(1)) if m2 else ''
    m3 = FREQ_RE.search(html)
    gyakorisag = clean(m3.group(1)) if m3 else ''
    m4 = DEF_RE.search(html)
    glossza = clean(m4.group(1)) if m4 else ''
    return gk_szam, lemma_gorog, atirat, gyakorisag, glossza


def run():
    conn = sqlite3.connect(NYERS_DB)
    cur = conn.cursor()
    cur.execute("SELECT Topic, Definition FROM Lexicon WHERE Topic LIKE 'G%' AND Topic NOT LIKE 'gk%'")
    sorok = []
    hibas = []
    for topic, html in cur.fetchall():
        if not STRONG_G_RE.match(topic):
            hibas.append(topic)
            continue
        strong = 'G' + topic[1:].zfill(4)
        gk_szam, lemma_gorog, atirat, gyakorisag, glossza = parse_row(topic, html)
        sorok.append((strong, gk_szam, lemma_gorog, atirat, gyakorisag, glossza))
    conn.close()

    sorok.sort(key=lambda r: r[0])

    forras_hash = sha256_file(NYERS_DB)
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/mcged_import.py — kézzel nem szerkesztendő.\n')
        f.write('# forras: konkordancia/lexikonok_nyers/MCGED.lexicon (biblematedata) | '
                'sha256=%s\n' % forras_hash)
        f.write('# licenc: (c) Mounce 1993, www.teknia.com/greek-dictionary — '
                'kotelezo forrasmegjeloles minden idezetnel (F6 D16)\n')
        f.write('\t'.join(['strong', 'gk_szam', 'lemma_gorog', 'atirat', 'gyakorisag', 'glossza']) + '\n')
        for row in sorok:
            f.write('\t'.join(row) + '\n')

    print('sorok: %d' % len(sorok))
    print('hibas Topic (kihagyva): %d' % len(hibas))
    if hibas:
        print('  pelda: %r' % hibas[:5])
    print('irva: %s' % KIMENET)


if __name__ == '__main__':
    run()
