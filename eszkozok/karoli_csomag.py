# -*- coding: utf-8 -*-
"""
karoli_csomag.py -- a két nyílt Károli-csomag (`nyilt_karoli_strong/`, `nyilt_karoli_modern/`) közös szerkezete
(F175.N). A csomag mappája pontosan a nyilvános adatrepó tartalma; az almappák angol nevűek:

    gyökér      README.md, LICENSE, CITATION.cff, .gitattributes, KIADAS.txt, RELEASE.txt, ELLENORZO_OSSZEG.sha256
    data/       a táblák (generált)
    docs/hu/    KODKONYV, MODSZER, ISMERT_HIBAK, ATTRIBUCIO, OLVASSEL (generált)
    docs/en/    CODEBOOK, METHODS, KNOWN_ISSUES, ATTRIBUTION (generált)
    paper/      a folyóiratcikk kézirata: kezirat_hu.md, kezirat_en.md (KÉZI FORRÁS: a generátor nem írja, nem
                törli; ha ott áll, az ellenőrző összegbe kerül)

Az exportálók csak a generált részeket írják (`GENERALT_MAPPAK`); a `kiir()` a `paper/`-hez nem nyúl. A csomagmappában
csak az `engedett_regex()` által elfogadott fájl lehet (a kapuk HARMADIK pontja ezt hívja). Nincs `export-ignore`: a
csomag mappája pontosan a nyilvános repó tartalma (`git archive HEAD:<csomag>` mindent kiad, ami a mappában áll).

A rövid közlemény hu/en tervezete (belső anyag) a csomagon kívül, `kozlemeny/note/<csomag>/` alatt áll, a
`kozlemeny/data_paper/` mellett: generált, gépi jelöléssel (`note_utak()`).

TSV-olvasás `split('\\t')`, írás `'\\t'.join()` (nem `csv`).
"""
import os
import re

GYOKER_FAJLOK = ('README.md', 'LICENSE', 'CITATION.cff', '.gitattributes', 'KIADAS.txt', 'RELEASE.txt',
                 'ELLENORZO_OSSZEG.sha256')
GENERALT_MAPPAK = ('data', 'docs')
KEZI_MAPPAK = ('paper',)

# a rövid közlemény tervezete: belső anyag, a csomagon kívül (a csomagmappa a nyilvános repó tartalma)
NOTE_BELSO = 'kozlemeny/note/'


def note_utak(csomag):
    """A csomag közleményének (hu, en) útja a repó gyökeréhez viszonyítva; `csomag`: `karoli_strong`/`karoli_modern`."""
    return NOTE_BELSO + csomag + '/note_hu.md', NOTE_BELSO + csomag + '/note_en.md'


KIHAGYOTT_OSSZEGBOL = ('ELLENORZO_OSSZEG.sha256', 'KIADAS.txt', 'RELEASE.txt')

DOCS_HU = 'docs/hu/'
DOCS_EN = 'docs/en/'
OLVASSEL = DOCS_HU + 'OLVASSEL.md'
KODKONYV_HU = DOCS_HU + 'KODKONYV.md'
KODKONYV_EN = DOCS_EN + 'CODEBOOK.md'
MODSZER = DOCS_HU + 'MODSZER.md'
METHODS = DOCS_EN + 'METHODS.md'
ISMERT_HIBAK = DOCS_HU + 'ISMERT_HIBAK.md'
KNOWN_ISSUES = DOCS_EN + 'KNOWN_ISSUES.md'
ATTRIBUCIO = DOCS_HU + 'ATTRIBUCIO.md'
ATTRIBUTION = DOCS_EN + 'ATTRIBUTION.md'
MAGYAR_FAJLOK = (OLVASSEL, KODKONYV_HU, MODSZER, ISMERT_HIBAK, ATTRIBUCIO, 'LICENSE', 'data/kodkonyv.tsv')


def engedett_regex(adat_minta):
    """A csomagmappában álló fájlok engedett útjai. `adat_minta`: a csomag `data/` alatti fájljainak regexe."""
    return re.compile(
        r'^(?:' + '|'.join([
            '|'.join(re.escape(n) for n in GYOKER_FAJLOK),
            r'data/(?:' + adat_minta + r')',
            r'docs/hu/(?:KODKONYV|MODSZER|ISMERT_HIBAK|ATTRIBUCIO|OLVASSEL)\.md',
            r'docs/en/(?:CODEBOOK|METHODS|KNOWN_ISSUES|ATTRIBUTION)\.md',
            r'paper/kezirat_(?:hu|en)\.md',
        ]) + r')$')


def engedett(rel, rx):
    return bool(rx.match(rel))


def kezi_forras(abs_ki):
    """A kézi forrású almappák (`paper/`) fájljai a lemezről, hogy az ellenőrző összegbe kerüljenek."""
    ki = {}
    for mappa in KEZI_MAPPAK:
        ut = os.path.join(abs_ki, mappa)
        if not os.path.isdir(ut):
            continue
        for gy, _, nevek in os.walk(ut):
            for n in nevek:
                p = os.path.join(gy, n)
                rel = os.path.relpath(p, abs_ki).replace('\\', '/')
                with open(p, encoding='utf-8', newline='') as f:
                    ki[rel] = f.read().replace('\r\n', '\n')
    return ki


def kiir(fajlok, abs_ki):
    """Kiírja a fájlokat; törli, ami a kimeneti mappában a `fajlok`-ban nincs — kivéve a kézi forrású almappákat
    (`paper/`), amelyekhez a generátor nem nyúl. Az üres almappákat is eltakarítja."""
    if os.path.isdir(abs_ki):
        for gy, _, nevek in os.walk(abs_ki):
            for n in nevek:
                rel = os.path.relpath(os.path.join(gy, n), abs_ki).replace('\\', '/')
                if rel.split('/')[0] in KEZI_MAPPAK:
                    continue
                if rel not in fajlok:
                    os.remove(os.path.join(gy, n))
        for gy, _, _ in sorted(os.walk(abs_ki), key=lambda x: -len(x[0])):
            if gy != abs_ki and not os.listdir(gy):
                os.rmdir(gy)
    for rel, tartalom in fajlok.items():
        if rel.split('/')[0] in KEZI_MAPPAK:
            continue                      # a kézi forrást nem írjuk felül
        ut = os.path.join(abs_ki, rel)
        os.makedirs(os.path.dirname(ut), exist_ok=True)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(tartalom)
    return abs_ki


def attribucio_nyelvek(szoveg):
    """A kétnyelvű forrásmegjelölés-sablont (`## Magyarul` / `## In English`) két önálló dokumentumra bontja:
    (magyar, angol)."""
    fej, _, utana = szoveg.partition('## Magyarul\n')
    hu, _, en = utana.partition('## In English\n')
    if not fej.startswith('# ') or not hu.strip() or not en.strip():
        raise SystemExit('attribúció-sablon: a „## Magyarul” / „## In English” tagolás hiányzik')
    return ('# Forrásmegjelölés és licencek\n' + hu.rstrip('\n') + '\n',
            '# Attribution and licences\n' + en.rstrip('\n') + '\n')


def kodkonyv_md(nyelv, cim, fajlok, sorok):
    """Egynyelvű kódkönyv-dokumentum. `fajlok`: [(fajl-kulcs, fejléc)]; `sorok`: (fajl, oszlop, ertek, hu, en)."""
    hu = nyelv == 'hu'
    ki = ['# Kódkönyv' if hu else '# Codebook', '', '*%s*' % cim, '']
    for fajl, fejlec in fajlok:
        ki += ['## %s' % fejlec, '',
               '| oszlop | érték | leírás |' if hu else '| column | value | description |', '|---|---|---|']
        for f, o, e, h, a in sorok:
            if f == fajl:
                ki.append('| `%s` | %s | %s |' % (o, ('`%s`' % e) if e else '', h if hu else a))
        ki.append('')
    return '\n'.join(ki)
