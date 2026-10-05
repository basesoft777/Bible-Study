"""Közös útvonal-konstansok a repón kívüli (gitignore-olt) és a visszaállítható
forrásfájlokhoz (F42, M2).

A `konkordancia/_nyers/` a .gitignore-ban van: ide kerülnek azok a nyers
fájlok, amelyek nem verziózhatók. Ha egy olvasó hiányzó fájlt talál, ne
hagyja ki csendben: `kotelezo()` egyértelmű hibát ad, amely a
`eszkozok/forras_letolt.py`-ra mutat.
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')
NYERS = os.path.join(KONKORDANCIA, '_nyers')
TBESH_NYERS = os.path.join(NYERS, 'tbesh')

# A TBESH.txt a repóban marad (DT-F42e), a letöltő szkript sha256-os helyreállító.
TBESH_TXT = os.path.join(KONKORDANCIA, 'TBESH.txt')
# Csak helyben élnek (DT-F42b): a .lexicon forrása nem rögzíthető, a konszolidált
# tábla belőle és a TBESH.txt-ből generálódik (eszkozok/tbesh_konszolidalt_import.py).
TBESH_LEXICON = os.path.join(TBESH_NYERS, 'TBESH.lexicon')
TBESH_KONSZOLIDALT = os.path.join(TBESH_NYERS, 'TBESH_konszolidalt.tsv')

_UZENET = {
    TBESH_TXT: ('letölthető és sha256-tal ellenőrizhető: python eszkozok/forras_letolt.py'),
    TBESH_LEXICON: ('NEM tölthető le rögzített forrásból (Google Drive, biblematedata; '
                    'l. konkordancia/lexikonok_nyers/README.md): csak helyben élő fájl, '
                    'a sha256-ja a konkordancia/TBESH_TBESG_README.md-ben; a letöltő szkript nem ígér letöltést. '
                    'Visszaállítás a git-történetből: git show 08d88dc:konkordancia/lexikonok_nyers/TBESH.lexicon '
                    '> konkordancia/_nyers/tbesh/TBESH.lexicon (l. konkordancia/TBESH_TBESG_README.md)'),
    TBESH_KONSZOLIDALT: ('generált: python eszkozok/tbesh_konszolidalt_import.py '
                         '(a TBESH.txt és a helyben élő TBESH.lexicon kell hozzá)'),
}


def kotelezo(ut, uzenet=None):
    """Visszaadja az útvonalat, ha a fájl megvan; különben FileNotFoundError
    egyértelmű üzenettel (nincs csendes kihagyás, nincs üres eredmény)."""
    if not os.path.isfile(ut):
        rel = os.path.relpath(ut, ROOT).replace(os.sep, '/')
        mod = uzenet or _UZENET.get(ut, 'python eszkozok/forras_letolt.py')
        raise FileNotFoundError('Hiányzó forrásfájl: %s — %s' % (rel, mod))
    return ut
