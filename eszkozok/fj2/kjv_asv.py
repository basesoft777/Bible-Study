#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kjv_asv.py -- F06 3. lepes, teljes KJV/ASV (N29): van-e elerheto, licencelt forras
szo-szintu Strong-illesztessel.

Harom agon keres, mindegyik eredmenye egy sor (vagy tobb) a kimenetben:
  A. studybible.info  -- HTTP-elerhetoseg (a repo jelenlegi forrasa, KJV_/ASV_Strongs oldalak)
  B. eBible.org       -- HTTP-elerhetoseg; ha USFM-zip jon, a Strong-cimkek merese
  C. GitHub           -- kereses (GITHUB_TOKEN-nel, ha van) + a legjobb jeloltek es az ismert
                         jeloltek shallow klonja; a KJV/ASV nevu szoveges fajlokban Strong-cimke-
                         minta szamlalas es Genezis 1:1 pelda (szo-szintu illesztes bizonyitekaul)

Lefedettseg (konyv, vers) csak USFM-forrasra merheto automatikusan; mas formatumnal a
'lefedettseg' oszlop 'nem_merheto_automatikusan' -- ez kezi jelolt, nem "nincs adat".
A licenc-/README-fajlokat szo szerint gyujti (kozos.licenc_gyujt).

Kimenet: naplok/F06_kjv_asv.tsv (forras, mero, ertek, megjegyzes -- hosszu alak)
"""

import io
import json
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kozos  # noqa: E402

PROBAK = [
    ('studybible_info', 'https://studybible.info/KJV_Strongs/Genesis%201'),
    ('studybible_info', 'https://studybible.info/ASV_Strongs/Genesis%201'),
    ('ebible_org', 'https://ebible.org/Scriptures/eng-kjv_usfm.zip'),
    ('ebible_org', 'https://ebible.org/Scriptures/engkjv_usfm.zip'),
    ('ebible_org', 'https://ebible.org/Scriptures/eng-asv_usfm.zip'),
    ('ebible_org', 'https://ebible.org/Scriptures/engasv_usfm.zip'),
    ('ebible_org', 'https://ebible.org/find/details.php?id=eng-kjv'),
    ('ebible_org', 'https://ebible.org/find/details.php?id=eng-asv'),
]
ISMERT_JELOLTEK = ['scrollmapper/bible_databases']
KERESESEK = ['kjv strongs', 'kjv strong numbers json', 'asv strongs', 'bible strongs word-level kjv tagged']
CIMKE_MINTAK = {
    'kapcsos_H_G': re.compile(r'\{[HG]\d{1,4}\}'),
    'S_tag': re.compile(r'<S>\d{1,4}</S>'),
    'strong_attr': re.compile(r'strong[a-z]*="[^"]*[HG]\d{1,4}'),
    'lemma_strong': re.compile(r'lemma="[^"]*strong:[HG]\d{1,4}'),
    'usfm_w': re.compile(r'\\w [^|\\]+\|[^\\]*strong="[HG]\d{1,4}'),
}
SZOVEGES = ('.json', '.txt', '.xml', '.usfm', '.sfm', '.sql', '.csv', '.tsv', '.osis', '.md', '.html')


def http_proba(url):
    import requests
    try:
        r = requests.get(url, timeout=60, stream=True, headers={'User-Agent': 'Bible-Study-F06/1.0'})
        elso = next(r.iter_content(200000), b'')
        return r.status_code, r.headers.get('content-type', ''), elso, r
    except Exception as e:  # noqa: BLE001
        return None, type(e).__name__ + ': ' + str(e)[:150], b'', None


def usfm_meres(szovegek):
    """szovegek: [(fajlnev, szoveg)] -> (konyvek_db, versek, versek_strongal, strong_cimkek)"""
    versek = strongos = cimkek = kanoni_versek = kanoni_strongos = 0
    konyvek, kanoni = set(), set()
    for fn, sz in szovegek:
        m = re.search(r'\\id\s+([A-Z0-9]{3})', sz)
        if m:
            konyvek.add(m.group(1))
        kan = bool(m and m.group(1) in KANONI_USFM)
        if kan:
            kanoni.add(m.group(1))
        for v in re.split(r'\\v\s+\d+', sz)[1:]:
            versek += 1
            n = len(re.findall(r'strong="[HG]\d', v))
            cimkek += n
            strongos += 1 if n else 0
            if kan:
                kanoni_versek += 1
                kanoni_strongos += 1 if n else 0
    return len(konyvek), versek, strongos, cimkek, len(kanoni), kanoni_versek, kanoni_strongos


KANONI_USFM = set('GEN EXO LEV NUM DEU JOS JDG RUT 1SA 2SA 1KI 2KI 1CH 2CH EZR NEH EST JOB PSA PRO ECC SNG ISA JER LAM EZK DAN HOS JOL AMO OBA JON MIC NAM HAB ZEP HAG ZEC MAL MAT MRK LUK JHN ACT ROM 1CO 2CO GAL EPH PHP COL 1TH 2TH 1TI 2TI TIT PHM HEB JAS 1PE 2PE 1JN 2JN 3JN JUD REV'.split())


def json_lefedettseg(ut):
    """JSON-bol (rekurziv) a book/chapter/verse/text dict-eket gyujti: (konyv, vers, vers_cimkevel) vagy None."""
    try:
        with open(ut, encoding='utf-8') as f:
            adat = json.load(f)
    except Exception:  # noqa: BLE001
        return None
    talalt = {}

    def jar(x):
        if isinstance(x, dict):
            if all(k in x for k in ('book', 'chapter', 'verse', 'text')) and isinstance(x['text'], str):
                talalt[(str(x['book']), str(x['chapter']), str(x['verse']))] = bool(re.search(r'\{[HG]\d', x['text']))
            else:
                for v in x.values():
                    jar(v)
        elif isinstance(x, list):
            for v in x:
                jar(v)
    jar(adat)
    if not talalt:
        return None
    return len({k[0] for k in talalt}), len(talalt), sum(1 for v in talalt.values() if v)


def tag_meres(ut):
    szoveg = open(ut, encoding='utf-8', errors='replace').read()
    szamok = {k: len(p.findall(szoveg)) for k, p in CIMKE_MINTAK.items()}
    pelda = ''
    m = re.search(r'In the beginning.{0,400}', szoveg, re.S)
    if m and (any(p.search(m.group(0)) for p in CIMKE_MINTAK.values()) or re.search(r'H\d{3,4}', m.group(0))):
        pelda = re.sub(r'\s+', ' ', m.group(0))[:220]
    return szamok, pelda


def github_kereses(sorok):
    import requests
    fejlec = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Bible-Study-F06/1.0'}
    if os.environ.get('GITHUB_TOKEN'):
        fejlec['Authorization'] = 'Bearer ' + os.environ['GITHUB_TOKEN']
    egyedi = {}
    for q in KERESESEK:
        try:
            r = requests.get('https://api.github.com/search/repositories', params={'q': q, 'per_page': 10},
                             headers=fejlec, timeout=60)
            if r.status_code != 200:
                sorok.append(('github', 'kereses:' + q, 'HTTP %d' % r.status_code, ''))
                continue
            elemek = r.json().get('items', [])
            sorok.append(('github', 'kereses:' + q, '%d talalat' % len(elemek), ''))
            for it in elemek:
                egyedi.setdefault(it['full_name'], it)
        except Exception as e:  # noqa: BLE001
            sorok.append(('github', 'kereses:' + q, 'hiba', str(e)[:120]))
    for nev, it in sorted(egyedi.items()):
        lic = (it.get('license') or {}).get('spdx_id') or 'nincs_megadva'
        sorok.append(('github:' + nev, 'repo_adatlap',
                      'star=%s meret_kb=%s licenc=%s frissitve=%s' % (it.get('stargazers_count'), it.get('size'), lic, (it.get('pushed_at') or '')[:10]),
                      it.get('description') or ''))
    jeloltek = [n for n, it in sorted(egyedi.items(), key=lambda kv: -(kv[1].get('stargazers_count') or 0))
                if (egyedi[n].get('size') or 0) <= 300_000][:6]
    for n in ISMERT_JELOLTEK:
        if n not in jeloltek:
            jeloltek.append(n)
    return jeloltek


def fut(munka, parancs):
    sorok = []
    forras_urlok = ['https://studybible.info/', 'https://ebible.org/', 'https://api.github.com/search/repositories']
    if kozos.SZARAZ:
        print('kjv_asv: szaraz futas, %d HTTP-proba, %d kereses, %d ismert jelolt' % (len(PROBAK), len(KERESESEK), len(ISMERT_JELOLTEK)))
        return
    for azon, url in PROBAK:
        allapot, tipus, elso, valasz = http_proba(url)
        megj = 'content-type: %s; elso_blokk_bajt: %d' % (tipus, len(elso)) if allapot else tipus
        sorok.append((azon, 'http:' + url, 'HTTP %s' % allapot if allapot else 'nem_elerheto', megj))
        if allapot == 200 and url.endswith('.zip'):
            try:
                import requests
                adat = requests.get(url, timeout=300, headers={'User-Agent': 'Bible-Study-F06/1.0'}).content
                with zipfile.ZipFile(io.BytesIO(adat)) as z:
                    szovegek = [(n, z.read(n).decode('utf-8', errors='replace')) for n in z.namelist()
                                if n.lower().endswith(('.usfm', '.sfm'))]
                    for n in z.namelist():  # licenc-/jogi szovegek szo szerint
                        if re.search(r'(?i)copr|licen|readme|copyright', os.path.basename(n)) and z.getinfo(n).file_size <= kozos.FAJL_LIMIT:
                            sz = z.read(n).decode('utf-8', errors='replace')
                            mentett = '%s__%s__%s.txt' % (azon, os.path.basename(url), n.replace('/', '__'))
                            os.makedirs(kozos.LICENC_MAPPA, exist_ok=True)
                            with open(os.path.join(kozos.LICENC_MAPPA, mentett), 'w', encoding='utf-8', newline='') as f:
                                f.write(sz)
                            kozos.LICENC_SOROK.append((azon, mentett, url + '#' + n, len(sz)))
                kdb, v, vs, c, kk, kv, kvs = usfm_meres(szovegek)
                sorok.append((azon, 'usfm_meres:' + url, 'konyv=%d vers=%d vers_strongos=%d strong_cimke=%d' % (kdb, v, vs, c),
                              'lefedettseg: USFM-bol merve (minden id-jelolt fajl, apokrifokkal egyutt)'))
                sorok.append((azon, 'usfm_meres_kanoni66:' + url, 'konyv=%d vers=%d vers_strongos=%d' % (kk, kv, kvs),
                              'csak a 66 kanoni konyv USFM-azonositoi'))
            except Exception as e:  # noqa: BLE001
                sorok.append((azon, 'zip_feldolgozas', 'hiba', str(e)[:150]))
        if valasz is not None:
            valasz.close()

    for nev in github_kereses(sorok):
        azon = 'github:' + nev
        cel = os.path.join(munka, 'kjvasv', nev.replace('/', '__'))
        commit, hiba = kozos.klonoz('https://github.com/%s' % nev, cel)
        if not commit:
            sorok.append((azon, 'elerheto', 'nem', hiba))
            continue
        forras_urlok.append('https://github.com/' + nev)
        sorok.append((azon, 'elerheto', 'igen', 'commit ' + commit))
        van_cimke = False
        for m, almappak, fajlok in os.walk(cel):
            almappak[:] = [a for a in almappak if a != '.git']
            for fn in sorted(fajlok):
                ut = os.path.join(m, fn)
                rel = os.path.relpath(ut, cel).replace(os.sep, '/')
                if not (fn.lower().endswith(SZOVEGES) and re.search(r'(?i)kjv|asv|king.?james|american.?standard', rel)):
                    continue
                if os.path.getsize(ut) > 80_000_000:
                    sorok.append((azon, 'tul_nagy_fajl', rel, '%d bajt' % os.path.getsize(ut)))
                    continue
                szamok, pelda = tag_meres(ut)
                if any(szamok.values()) or pelda:
                    van_cimke = True
                    jl = json_lefedettseg(ut) if fn.lower().endswith('.json') else None
                    if jl:
                        sorok.append((azon, 'json_lefedettseg:' + rel, 'konyv=%d vers=%d vers_strong_cimkevel=%d' % jl,
                                      'JSON book/chapter/verse/text rekordokbol merve'))
                    sorok.append((azon, 'strong_cimkek:' + rel, ' '.join('%s=%d' % kv for kv in szamok.items() if kv[1]) or 'nincs_mintaillesztes',
                                  'lefedettseg=nem_merheto_automatikusan (kezi); genezis_1_1_pelda: %s' % pelda))
        sorok.append((azon, 'szo_szintu_strong_bizonyitek', 'igen' if van_cimke else 'nem', 'KJV/ASV nevu fajlokban talalt cimke-minta'))
        for rel, k in kozos.licenc_gyujt(azon.replace(':', '_').replace('/', '__'), cel):
            sorok.append((azon, 'licenc_fajl', rel, '%d karakter' % k))
    kozos.tsv_ir(os.path.join(kozos.NAPLOK, 'F06_kjv_asv.tsv'),
                 kozos.fejlec(' ; '.join(forras_urlok), 'lasd a soronkenti commit-megjegyzest', parancs),
                 ['forras', 'mero', 'ertek', 'megjegyzes'], sorok)
    print('kjv_asv: %d sor' % len(sorok))
