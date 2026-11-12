#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_modern_export.py -- a modernizált Károli – Strong nyílt mag (CC BY 4.0) generált exportja (F174, FELADATOK #174).

A modernizált Károli (#96, `adat/karoli_modern/karoli_modern.tsv`) és a Károli–Strong párosítás (#22,
`adat/karoli_strong/parok_*.tsv`, `szavak_*.tsv`) kulcs szerinti összekapcsolása: (igehely, token-sorszám).
A vetítés determinisztikus, modell nélküli kulcs-illesztés; új Strong-állítás nem keletkezik (DT305, DT314: a
modern réteg Strongot nem tárol, a join éri el). A kieső token (összevont „a”, segédigei *vala*) saját sorában
marad, a gazdaszó sorszámával; a Strongja nem vész el.

Kimenet: `nyilt_karoli_modern/` — a mappa tartalma 1:1-ben a nyilvános adatrepó gyökere. Determinisztikus,
újrafuttatva bájtazonos. A `kozlemeny/` almappa (a közlemény hu/en tervezete) generált, de nincs az ellenőrző
összegben, és a `.gitattributes` a kiadási archívumból kihagyja (export-ignore) a megjelenésig.

A nyilvános szövegek (MODSZER/METHODS, közlemény, kódkönyv, ismert hibák) prózája itt áll; minden szám az
adatból vagy a forrásnaplóból számolódik (a `szamok()` függvény), kézzel nem kerül a szövegbe. Ha egy
forrásnapló-szám nem olvasható ki, a szkript megáll.

TSV-olvasás `split('\\t')`, írás `'\\t'.join()` (nem `csv`).

Használat:
    python eszkozok/karoli_modern_export.py [--kimenet nyilt_karoli_modern]
"""
import argparse
import glob
import hashlib
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nyilt_mag_export as NM  # noqa: E402  (OSIS-kulcs, közös azonosítók)

GYOKER = NM.GYOKER
KIMENET = 'nyilt_karoli_modern'
DOI = '10.5281/zenodo.24141950'
DOI_KAROLI_STRONG = NM.DOI_KAROLI_STRONG
DOI_MAG = NM.DOI_MAG
KANONIKUS_HELY = 'https://doi.org/' + DOI
SZERZO = NM.SZERZO
ORCID = NM.ORCID
LEXIKON_HU = NM.LEXIKON_CIM_HU
LEXIKON_EN = NM.LEXIKON_CIM_EN
CIM_HU = 'Modernizált Károli – Strong'
CIM_EN = 'Modernised Károli – Strong'
KOZLEMENY_DIR = 'kozlemeny/'

MODERN = 'adat/karoli_modern/karoli_modern.tsv'
MODERN_VERS = 'adat/karoli_modern/karoli_modern_versek.tsv'
IGEALAK_TOKENEK = 'adat/karoli_modern/igealak_tokenek.tsv'
PAROK = 'adat/karoli_strong/parok_*.tsv'
SZAVAK = 'adat/karoli_strong/szavak_*.tsv'
NEM_TR = 'adat/karoli_strong/nem_tr_parositott.tsv'
LLM_SONNET = ['adat/karoli_modern/igealak_llm_hivasok.jsonl']
LLM_OPUS = ['adat/karoli_modern/igealak_llm_opus_hivasok.jsonl', 'adat/karoli_modern/igealak_llm_kor3_hivasok.jsonl',
            'adat/karoli_modern/igealak_llm_kor4_hivasok.jsonl', 'adat/karoli_modern/igealak_llm_kor5_hivasok.jsonl']
MINTA_IGEALAK = 'adat/karoli_modern/igealak_minta.tsv'
MINTA2 = 'adat/karoli_modern/igealak_minta2.tsv'
NAPLO_MERES = 'naplok/KAROLI_MODERN_meres.md'
NAPLO_ELLENOR = 'naplok/ELLENOR_F96.md'
F172_MERES = 'f172/meres_eredmeny.tsv'
F172_KULSO = 'f172/kulso/kulso_eredmeny.tsv'

FEJ = ['osis', 'token', 'alak_1908', 'alak_modern', 'valtozott', 'kieso', 'gazda_token', 'bizonytalan', 'allapot',
       'strong', 'eredeti_token', 'kapcsolat', 'bizonyossag']
VERS_FEJ = ['osis', 'szoveg_modern', 'valtozott']
FEJLEC_HU = ('# GENERÁLT: a(z) %s – %s nyílt magjának exportja (CC BY 4.0), a projekt adataiból generálva — kézzel '
             'nem szerkesztendő; a „#” kezdetű sor megjegyzés.' % (LEXIKON_HU, CIM_HU))
FEJLEC_EN = ('# GENERATED: export of the %s – %s open core (CC BY 4.0), generated from the project data — do not '
             'edit by hand; a line starting with "#" is a comment.' % (LEXIKON_EN, CIM_EN))
STEP_ATTRIB = ('Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0)')
K96_NELKUL = ('Mt', 'Mk', 'Luk', 'Ján', 'ApCsel')   # a #96 lezárásakor még nem párosított könyvek
MORFEMA_RX = re.compile(r'^H90(0[1-9]|[1-4]\d)$')       # H9001–H9049: a TAHOT előtag-/rag-morfémái


# ----------------------------------------------------------------------------- olvasás

def tsv(rel):
    return NM.tsv(rel)


def fejsorok(rel):
    """A fájl `#` kezdetű sorai (proveniencia)."""
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        return [s.rstrip('\n') for s in f if s.startswith('#')]


def relglob(minta):
    return sorted(os.path.relpath(p, GYOKER).replace('\\', '/') for p in glob.glob(os.path.join(GYOKER, minta)))


def kapcsolat(strong):
    reszek = strong.split('+')
    return 'morfema' if all(MORFEMA_RX.match(r) for r in reszek) else 'szo'


def beolvas():
    """A vetítés bemenete: modern tokenek, párok (tokenkulcsonként), a magyar oldal tokenállapota."""
    _, modern = tsv(MODERN)
    parok = {}
    par_db = 0
    for rel in relglob(PAROK):
        _, ps = tsv(rel)
        for p in ps:
            parok.setdefault((p['vers'], p['hu_sorszam']), []).append(p)
            par_db += 1
    allapot = {}
    for rel in relglob(SZAVAK):
        _, ss = tsv(rel)
        for s in ss:
            if s['oldal'] == 'hu':
                allapot[(s['vers'], s['sorszam'])] = s
    _, versek = tsv(MODERN_VERS)
    return modern, parok, par_db, allapot, versek


# ----------------------------------------------------------------------------- vetítés

ALLAPOT = {'parositva': 'javaslat', 'betoldas': 'betoldas', 'fuggoben': 'fuggoben'}


def vetit(modern, parok, allapot):
    """Könyvenként a kimeneti sorok. A token pár nélkül egy sor; párral páronként egy sor, azonos token-kulccsal.
    Megáll, ha a pár kulcsa vagy alakja nem illeszkedik (nem találgat)."""
    konyvek = []           # [(osis_konyv, [sor])], a forrás könyvsorrendjében
    index = {}
    lefedett = set()
    for t in modern:
        kulcs = (t['igehely'], t['sorszam'])
        sz = allapot.get(kulcs)
        if sz is None:
            raise SystemExit('vetítés: a modern token kulcsa nincs a párosítás tokenjei között: %s %s' % kulcs)
        if sz['szo'] != t['alak_1908']:
            raise SystemExit('vetítés: az 1908-as alak eltér: %s %s (%r <> %r)' % (kulcs + (sz['szo'], t['alak_1908'])))
        o = NM.osis(t['igehely'])
        kk = o.split('.')[0]
        if kk not in index:
            index[kk] = len(konyvek)
            konyvek.append((kk, []))
        sorok = konyvek[index[kk]][1]
        valt = 'igen' if (t['kieso'] or t['alak_1908'] != t['alak_modern']) else ''
        alap = [o, t['sorszam'], t['alak_1908'], t['alak_modern'], valt, t['kieso'], t['kieso_gazda'],
                'igen' if t['bizonytalan'] else '']
        ps = parok.get(kulcs, [])
        if not ps:
            if sz['allapot'] == 'parositva':
                raise SystemExit('vetítés: párosított token pár nélkül: %s %s' % kulcs)
            sorok.append(alap + [ALLAPOT[sz['allapot']], '', '', '', ''])
            continue
        lefedett.add(kulcs)
        for p in sorted(ps, key=lambda p: (int(p['er_sorszam']), p['strong'])):
            if p['hu_szo'] != t['alak_1908']:
                raise SystemExit('vetítés: a pár magyar szava eltér: %s %s' % kulcs)
            sorok.append(alap + ['javaslat', p['strong'], p['er_sorszam'], kapcsolat(p['strong']), p['bizonyossag']])
    hianyzo = set(parok) - lefedett
    if hianyzo:
        raise SystemExit('vetítés: %d pár kulcsa nincs a modern táblában (pl. %s)' % (len(hianyzo), sorted(hianyzo)[0]))
    return konyvek


# ----------------------------------------------------------------------------- számok (generált)

def _llm_token(rels):
    ossz = 0
    for rel in rels:
        with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
            for s in f:
                if s.strip():
                    ossz += json.loads(s)['total_tokens']
    return ossz


def _napló(rel, rx, nev):
    m = re.search(rx, NM.olvas(rel))
    if not m:
        raise SystemExit('szám: a(z) %s nem olvasható ki a forrásnaplóból (%s)' % (nev, rel))
    return m


def wilson(x, n, z=1.959964):
    """Wilson 95%-os intervallum (alsó, felső) az x/n arányra."""
    p = x / n
    k = z * z / n
    kozep = (p + k / 2) / (1 + k)
    fel = z * ((p * (1 - p) / n + k / (4 * n)) ** 0.5) / (1 + k)
    return max(0.0, kozep - fel), min(1.0, kozep + fel)


def _f172(rel, oszlop, ertek):
    _, ss = tsv(rel)
    for s in ss:
        if s.get(oszlop) == ertek:
            return s
    raise SystemExit('szám: hiányzó sor %s=%s (%s)' % (oszlop, ertek, rel))


def _ts_datumok(rels):
    d = []
    for rel in rels:
        for s in fejsorok(rel):
            d += re.findall(r'\bts=(\d{4}-\d{2}-\d{2})', s)
    return d


def szamok(modern, konyvek, par_db, allapot, versek):
    N = {}
    N['token'] = len(modern)
    N['vers'] = len(versek)
    N['konyv'] = len(konyvek)
    N['valtozo_token'] = sum(1 for t in modern if t['kieso'] or t['alak_1908'] != t['alak_modern'])
    N['valtozo_vers'] = sum(1 for v in versek if v['valtozott'] == 'igen')
    N['osszevonva'] = sum(1 for t in modern if t['kieso'] == 'osszevonva')
    N['segedige'] = sum(1 for t in modern if t['kieso'] == 'segedige')
    N['bizonytalan'] = sum(1 for t in modern if t['bizonytalan'])
    N['par'] = par_db
    sorok = [s for _, ss in konyvek for s in ss]
    parsor = [s for s in sorok if s[9]]
    N['strongos_token'] = len({(s[0], s[1]) for s in parsor})
    N['kieso_strongos'] = len({(s[0], s[1]) for s in parsor if s[5]})
    N['betoldas'] = sum(1 for a in allapot.values() if a['allapot'] == 'betoldas')
    N['fuggoben'] = sum(1 for a in allapot.values() if a['allapot'] == 'fuggoben')
    N['magas'] = sum(1 for s in parsor if s[12] == 'magas')
    N['alacsony'] = sum(1 for s in parsor if s[12] == 'alacsony')
    N['morfema'] = sum(1 for s in parsor if s[11] == 'morfema')
    N['heber_par'] = sum(1 for s in parsor if s[9].startswith('H'))
    N['gorog_par'] = sum(1 for s in parsor if s[9].startswith('G'))
    N['sor'] = len(sorok)
    _, nt = tsv(NEM_TR)
    N['nem_tr'] = len(nt)
    # a modernizálás jelöltként maradt tokenjei (a modern alak = a helyesírási alak, de van igealak-jelölt)
    _, it = tsv(IGEALAK_TOKENEK)
    N['jelolt_maradt'] = sum(1 for t in it if t['jelolt'] and t['alak_modern'] == t['alak_helyesiras'] and not t['kieso'])
    # nyelvi modell (hívásnaplók)
    N['llm_sonnet'] = _llm_token(LLM_SONNET)
    N['llm_opus'] = _llm_token(LLM_OPUS)
    N['llm_kor'] = len(LLM_SONNET) + len(LLM_OPUS)
    # minták
    _, m1 = tsv(MINTA_IGEALAK)
    N['minta1_vers'] = len(m1)
    N['minta1_jo'] = sum(1 for s in m1 if s['ellenorzes'] == 'jó')
    _, m2 = tsv(MINTA2)
    N['minta2_vers'] = len(m2)
    cs = hb = kh = 0
    for s in m2:
        m = re.search(r'csere=(\d+) hiba=(\d+) kihagyas=(\d+)', s['megjegyzes'])
        if not m:
            raise SystemExit('szám: a minta2 %s sorának nincs csere/hiba/kihagyás értéke' % s['minta_id'])
        cs, hb, kh = cs + int(m.group(1)), hb + int(m.group(2)), kh + int(m.group(3))
    N['minta2_csere'], N['minta2_hiba'], N['minta2_kihagyas'] = cs, hb, kh
    m = _napló(NAPLO_MERES, r'minta, cserék \(`→`\) \| \*\*(\d+) / (\d+) \(100%\)\*\*', 'helyesírási minta')
    N['hminta_jo'], N['hminta_ossz'] = int(m.group(1)), int(m.group(2))
    m = _napló(NAPLO_MERES, r'szövegváltozó sorok \| \*\*(\d+) / (\d+) \((\d+,\d)%\)\*\*', '„a mi” ellenőrző halmaz')
    N['ami_jo'], N['ami_ossz'], N['ami_p'] = int(m.group(1)), int(m.group(2)), m.group(3)
    m = _napló(NAPLO_ELLENOR, r'Lefedettség igealakra: (\d+) / \(\d+ \+ (\d+)\) = (\d+,\d)%', 'lefedettség')
    N['lef_csere'], N['lef_kihagyas'], N['lef_p'] = int(m.group(1)), int(m.group(2)), m.group(3)
    m = _napló(NAPLO_ELLENOR, r'\*\*Összesen \((\d+) vers\):\*\*\n- igealak: \*\*(\d+) csere, (\d+) hiba, (\d+) kihagyás\*\*',
               'a független ellenőr mintája')
    N['ell_vers'], N['ell_hiba'] = int(m.group(1)), int(m.group(3))
    if (int(m.group(2)), int(m.group(4))) != (N['lef_csere'], N['lef_kihagyas']):
        raise SystemExit('szám: a független ellenőr mintájának két sora ellentmond (%s)' % NAPLO_ELLENOR)
    m = _napló(NAPLO_ELLENOR, r'Korpuszbecslés: kb\. ([\d ]+) token; Poisson 95%-os sáv kb\. ([\d ]+)–([\d ]+)\.',
               'korpuszbecslés')
    N['korp'], N['korp_a'], N['korp_f'] = (int(m.group(i).replace(' ', '')) for i in (1, 2, 3))
    # Wilson 95% (a kiadás számolja a mért darabszámokból; a forrásnaplóban intervallum nincs)
    N['lef_w'] = wilson(N['lef_csere'], N['lef_csere'] + N['lef_kihagyas'])
    N['ell_hiba_w'] = wilson(N['ell_hiba'], N['lef_csere'])
    N['minta2_hiba_w'] = wilson(N['minta2_hiba'], N['minta2_csere'])
    N['hminta_hiba_w'] = wilson(N['hminta_ossz'] - N['hminta_jo'], N['hminta_ossz'])
    N['ami_hiba'] = N['ami_ossz'] - N['ami_jo']
    # a #96 lezárásakor párosított könyvek (az ÚSZ öt könyve később készült; a kapu ugyanezt méri)
    N['strongos_61'] = sum(1 for k, a in allapot.items()
                           if a['allapot'] == 'parositva' and k[0].rsplit(' ', 1)[0] not in K96_NELKUL)
    N['konyv_61'] = N['konyv'] - len(K96_NELKUL)
    N['konyv_uj'] = len(K96_NELKUL)
    N['hminta_ossz_hiba'] = N['hminta_ossz'] - N['hminta_jo']
    # a párosítás pontossága (#172)
    o = _f172(F172_MERES, 'cimke', 'OSSZES (súlyozott)')
    N['p_osszes'], N['p_osszes_a'], N['p_osszes_f'] = o['p'], o['also95'], o['felso95']
    o = _f172(F172_MERES, 'cimke', 'OSSZES · morféma (H9001–H9049)')
    N['p_morfema'], N['p_morfema_a'], N['p_morfema_f'] = o['p'], o['also95'], o['felso95']
    o = _f172(F172_KULSO, 'csoport', 'OSSZES')
    N['k_n'], N['k_fs'], N['k_fs_a'], N['k_fs_f'] = o['n_fo'], o['forras_szerint'], o['fs_also95'], o['fs_felso95']
    N['k_h3'], N['k_h3_a'], N['k_h3_f'], N['k_mi'] = o['haromutas'], o['h3_also95'], o['h3_felso95'], o['elter_mi_hibank']
    # adatállapot: a forrástáblák utolsó commitjának dátuma (az ÚSZ-könyvek párjainak nincs ts-dátuma), és a
    # fejlécek ts-dátuma közül a későbbi
    datumok = _ts_datumok([MODERN, MODERN_VERS] + relglob(PAROK) + relglob(SZAVAK))
    try:
        g = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', 'adat/karoli_modern', 'adat/karoli_strong'],
                           cwd=GYOKER, capture_output=True, text=True, encoding='utf-8')
        if re.match(r'^\d{4}-\d{2}-\d{2}$', g.stdout.strip()):
            datumok.append(g.stdout.strip())
    except OSError:
        pass
    N['adatallapot'] = max(datumok)
    return N


def ezres(n, nyelv='hu'):
    s = '{:,}'.format(int(n))
    return s.replace(',', ' ' if nyelv == 'hu' else ',')


def szazalek(p, nyelv='hu'):
    s = '%.2f' % (float(p) * 100)
    return s.replace('.', ',') if nyelv == 'hu' else s


def millio(n, nyelv='hu'):
    s = '%.2f' % (n / 1e6)
    return (s.replace('.', ',') + ' M') if nyelv == 'hu' else (s + ' M')


def fmt(N, nyelv):
    """A szövegek behelyettesítő szótára: ezres tagolás, százalék, millió."""
    F = {}
    for k, v in N.items():
        if isinstance(v, int):
            F[k] = ezres(v, nyelv)
    for k in ('p_osszes', 'p_osszes_a', 'p_osszes_f', 'p_morfema', 'p_morfema_a', 'p_morfema_f', 'k_fs', 'k_fs_a',
              'k_fs_f', 'k_h3', 'k_h3_a', 'k_h3_f'):
        F[k] = szazalek(N[k], nyelv)
    F['k_n'] = ezres(N['k_n'], nyelv)
    F['k_mi'] = N['k_mi']
    F['llm_sonnet_m'] = millio(N['llm_sonnet'], nyelv)
    F['llm_opus_m'] = millio(N['llm_opus'], nyelv)
    for k in ('lef_w', 'ell_hiba_w', 'minta2_hiba_w', 'hminta_hiba_w'):
        for i, utotag in ((0, '_a'), (1, '_f')):
            s = '%.1f' % (N[k][i] * 100)
            F[k + utotag] = s.replace('.', ',') if nyelv == 'hu' else s
    F['lef_p'] = N['lef_p'] if nyelv == 'hu' else N['lef_p'].replace(',', '.')
    F['ami_p'] = N['ami_p'] if nyelv == 'hu' else N['ami_p'].replace(',', '.')
    F['doi'] = DOI
    F['uj_konyvek_hu'] = 'Máté, Márk, Lukács, János, Apostolok cselekedetei'
    F['uj_konyvek_en'] = 'Matthew, Mark, Luke, John, Acts'
    F['doi_ks'] = DOI_KAROLI_STRONG
    F['doi_mag'] = DOI_MAG
    F['lex_hu'] = LEXIKON_HU
    F['lex_en'] = LEXIKON_EN
    F['szerzo'] = SZERZO
    F['orcid'] = ORCID
    F['adatallapot'] = N['adatallapot']
    return F


# ----------------------------------------------------------------------------- szövegek (próza; a számok behelyettesítve)

OLVASSEL = """# {cim} — nyílt adatkészlet

A Károli Gáspár-féle bibliafordítás 1908-as szövegének modernizált változata, szavanként összekapcsolva a héber
és görög eredeti szavaival és azok Strong-számaival. A {lex_hu} nyílt adatmagjainak egyike.

- **Licenc:** CC BY 4.0 (`LICENSE`); a felhasznált külső adatok forrásmegjelölése: `ATTRIBUCIO.md`.
- **DOI:** {doi} — a kiadás azonosítója és a tartalmi hash: `KIADAS.txt`.
- **Szerző:** {szerzo} (ORCID {orcid}).

## Tartalom

| fájl | tartalom |
|---|---|
| `konyvek/NN_Konyv.tsv` | könyvenként: minden szó 1908-as és modern alakja, és a hozzá párosított Strong-számok |
| `versek.tsv` | a modernizált szöveg versenként |
| `kodkonyv.tsv`, `KODKONYV.md` | az oszlopok és az értékek leírása (magyarul és angolul) |
| `MODSZER.md`, `METHODS.md` | hogyan készült a modernizálás és a Strong-összekapcsolás |
| `ISMERT_HIBAK.md`, `KNOWN_ISSUES.md` | ismert hibák és korlátok |
| `ATTRIBUCIO.md` | forrásmegjelölés és licencek |
| `CITATION.cff` | idézési adatok |
| `ELLENORZO_OSSZEG.sha256` | minden fájl SHA-256 összege |

## Számokban

- {konyv} könyv, {vers} vers, {token} szó (token); ebből {valtozo_token} szó és {valtozo_vers} vers változott
  a modernizálásban.
- {par} szópár (magyar szó – héber vagy görög szó, Strong-számmal) {strongos_token} magyar szón; {betoldas} szó a
  fordító betoldása (nincs eredeti megfelelője), {fuggoben} szó párosítása függőben van.

## Rövid használati útmutató

A kulcs a vers OSIS-azonosítója (`Gen.1.1`) és a szó sorszáma a versen belül (`token`). Egy szó annyi sorban áll,
ahány eredeti szóhoz párosítva van; a pár nélküli szó egy sorban. A modern szöveg olvasásához a `kieso` oszlop
üres sorait kell a `token` sorrendjében venni, szavanként egyszer; a szöveg írásjelekkel a `versek.tsv`-ben áll.

A párosítás gépi javaslat, mért pontossággal (`MODSZER.md`, 5. pont); a `bizonyossag` oszlop jelzi, hol egyezett két
független modell.

## Kapcsolódó adatkészletek

- Károli 1908 – Strong szóillesztés: https://doi.org/{doi_ks}
- A {lex_hu} nyílt adatmagja (motívumok): https://doi.org/{doi_mag}
"""

README = """# {cim_en} — open dataset

A modernised version of the 1908 text of the Károli Bible (the classic Hungarian translation), linked word by word
to the Hebrew and Greek source words and their Strong's numbers. One of the open data cores of the {lex_en}.

- **Licence:** CC BY 4.0 (`LICENSE`); attribution of the third-party data used: `ATTRIBUCIO.md`.
- **DOI:** {doi} — release identifier and content hash: `RELEASE.txt`.
- **Author:** {szerzo} (ORCID {orcid}).

## Contents

| file | content |
|---|---|
| `konyvek/NN_Book.tsv` | per book: every word in its 1908 and modern form, with the Strong's numbers aligned to it |
| `versek.tsv` | the modernised text, verse by verse |
| `kodkonyv.tsv`, `KODKONYV.md` | description of the columns and values (Hungarian and English) |
| `METHODS.md`, `MODSZER.md` | how the modernisation and the Strong linkage were made |
| `KNOWN_ISSUES.md`, `ISMERT_HIBAK.md` | known issues and limitations |
| `ATTRIBUCIO.md` | attribution and licences |
| `CITATION.cff` | citation metadata |
| `ELLENORZO_OSSZEG.sha256` | SHA-256 checksum of every file |

## In numbers

- {konyv} books, {vers} verses, {token} words (tokens); {valtozo_token} words and {valtozo_vers} verses changed in
  the modernisation.
- {par} word pairs (Hungarian word – Hebrew or Greek word, with Strong's number) on {strongos_token} Hungarian
  words; {betoldas} words are translator's additions (no source word), {fuggoben} words are pending alignment.

## Quick guide

The key is the OSIS verse identifier (`Gen.1.1`) and the position of the word within the verse (`token`). A word
appears in as many rows as source words it is aligned to; a word without a pair appears in one row. To read the
modern text, take the rows with an empty `kieso` column in `token` order, once per word; the punctuated text is in
`versek.tsv`.

The alignment is a machine proposal with measured accuracy (`METHODS.md`, section 5); the `bizonyossag` column marks
where two independent models agreed.

## Related datasets

- Károli 1908 – Strong word alignment: https://doi.org/{doi_ks}
- The open data core of the {lex_en} (motifs): https://doi.org/{doi_mag}
"""

LICENSE = """{cim} / {cim_en}
Copyright (c) 2026 {szerzo}

A saját rész (a modernizált szöveg, a szópárosítás és az összekapcsolás) licence:
The project's own part (the modernised text, the word alignment and the linkage) is licensed under:

Creative Commons Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/

A Károli 1908 szövege közkincs; a STEPBible TAHOT és TAGNT adatai CC BY 4.0 alatt állnak (ATTRIBUCIO.md).
The 1908 Károli text is in the public domain; the STEPBible TAHOT and TAGNT data are under CC BY 4.0 (ATTRIBUCIO.md).
"""

ATTRIBUCIO = """# Forrásmegjelölés és licencek / Attribution and licences

## Magyarul

| összetevő | licenc | megjegyzés |
|---|---|---|
| a modernizált szöveg, a szópárosítás, az összekapcsolás | CC BY 4.0 | a projekt saját munkája ({szerzo}) |
| Károli Gáspár fordítása, 1908-as kiadás | közkincs | a szöveg kora miatt; digitális forrás: a HunKar-szöveg |
| STEPBible TAHOT (héber Ószövetség, Strong-számokkal) | CC BY 4.0 | a Strong-számok és az eredeti szó sorszáma innen |
| STEPBible TAGNT (görög Újszövetség, Strong-számokkal) | CC BY 4.0 | a Strong-számok és az eredeti szó sorszáma innen |

A TAHOT és a TAGNT kötelező forrásmegjelölése, szó szerint:

> {step}

A csomag a TAHOT és a TAGNT szövegéből semmit nem tartalmaz: a héber és görög szóalak nincs benne, csak a
Strong-szám és a szó sorszáma a versben. Más külső adat nincs a csomagban.

## In English

| component | licence | note |
|---|---|---|
| the modernised text, the word alignment, the linkage | CC BY 4.0 | the project's own work ({szerzo}) |
| Károli Gáspár's translation, 1908 edition | public domain | by age; digital source: the HunKar text |
| STEPBible TAHOT (Hebrew Old Testament with Strong's numbers) | CC BY 4.0 | source of the Strong's numbers and source-word positions |
| STEPBible TAGNT (Greek New Testament with Strong's numbers) | CC BY 4.0 | source of the Strong's numbers and source-word positions |

Required attribution of TAHOT and TAGNT, verbatim:

> {step}

The package contains none of the TAHOT or TAGNT text: no Hebrew or Greek word forms, only the Strong's number and
the position of the word in the verse. No other third-party data is included.
"""

KODKONYV_SOROK = [
    # fajl, oszlop, ertek, hu, en
    ('konyvek', 'osis', '', 'A vers OSIS-azonosítója (könyv.fejezet.vers), a Károli-versszámozás szerint.',
     'OSIS verse identifier (book.chapter.verse), in Károli versification.'),
    ('konyvek', 'token', '', 'A szó sorszáma a versben (1-től), az 1908-as szöveg szavai szerint; a (osis, token) pár a szó kulcsa.',
     'Position of the word in the verse (from 1), counted on the 1908 text; (osis, token) is the word key.'),
    ('konyvek', 'alak_1908', '', 'A szó alakja a Károli 1908-as szövegében.', 'Word form in the 1908 Károli text.'),
    ('konyvek', 'alak_modern', '', 'A szó modernizált alakja; üres, ha a szó a modern szövegből kiesik (l. kieso).',
     'Modernised word form; empty if the word drops out of the modern text (see kieso).'),
    ('konyvek', 'valtozott', 'igen', 'A modern alak eltér az 1908-astól, vagy a szó kiesik.',
     'The modern form differs from the 1908 form, or the word drops out.'),
    ('konyvek', 'kieso', 'osszevonva', 'A szó egybeíródott a következővel (a kik → akik); a modern alak a gazdaszón áll.',
     'The word merged with the following one (a kik → akik); the modern form is on the host word.'),
    ('konyvek', 'kieso', 'segedige', 'Segédigei „vala”, amely a modern múlt időben kiesik (mondja vala → mondta); a gazdaszó az ige.',
     'Auxiliary "vala", dropped in the modern past tense (mondja vala → mondta); the host word is the verb.'),
    ('konyvek', 'gazda_token', '', 'Kieső szónál a gazdaszó sorszáma ugyanabban a versben; a kieső szó Strong-párja ehhez a szóhoz tartozik a modern szövegben.',
     'For a dropped word, the position of its host word in the same verse; its Strong pair belongs to that word in the modern text.'),
    ('konyvek', 'bizonytalan', 'igen', 'A modern alak szabályos, de a választás szövegkörnyezettől függ (pl. tárgyas vagy alanyi ragozás); a szöveg ezen a szón óvatosan kezelendő.',
     'The modern form is regular, but the choice depends on context (e.g. definite or indefinite conjugation); treat with care.'),
    ('konyvek', 'allapot', 'javaslat', 'A sor egy szópár: gépi párosítási javaslat, mért pontossággal (MODSZER.md 5.).',
     'The row is a word pair: a machine alignment proposal with measured accuracy (METHODS.md 5).'),
    ('konyvek', 'allapot', 'betoldas', 'A fordító betoldása: a szónak nincs héber vagy görög megfelelője.',
     "Translator's addition: the word has no Hebrew or Greek counterpart."),
    ('konyvek', 'allapot', 'fuggoben', 'A szó párosítása függőben van (kézi döntésre vár); pár nincs.',
     'Alignment of the word is pending (awaiting a manual decision); no pair.'),
    ('konyvek', 'strong', '', 'A párosított eredeti szó Strong-száma (H… héber, G… görög), a STEPBible TAHOT/TAGNT szerint; „+” két számot köt össze, ha az eredeti szó összetett.',
     "Strong's number of the aligned source word (H… Hebrew, G… Greek), from STEPBible TAHOT/TAGNT; \"+\" joins two numbers for a compound source word."),
    ('konyvek', 'eredeti_token', '', 'Az eredeti szó sorszáma a TAHOT/TAGNT versében (a Károli-vers kulcsán).',
     'Position of the source word in the TAHOT/TAGNT verse (keyed to the Károli verse).'),
    ('konyvek', 'kapcsolat', 'szo', 'A pár egy eredeti szóhoz köti a magyar szót.', 'The pair links the Hungarian word to a source word.'),
    ('konyvek', 'kapcsolat', 'morfema', 'A pár egy héber előtag- vagy ragmorfémához köti (H9001–H9049: névelő, kötőszó, elöljáró).',
     'The pair links it to a Hebrew prefix or suffix morpheme (H9001–H9049: article, conjunction, preposition).'),
    ('konyvek', 'bizonyossag', 'magas', 'Két független nyelvi modell ugyanazt a párt adta (Mózes 1–2. könyve).',
     'Two independent language models gave the same pair (Genesis and Exodus).'),
    ('konyvek', 'bizonyossag', 'alacsony', 'Egy nyelvi modell javaslata; a pontosságát a mérés adja meg (MODSZER.md 5.).',
     'Proposal of one language model; its accuracy is given by the measurement (METHODS.md 5).'),
    ('versek', 'osis', '', 'A vers OSIS-azonosítója.', 'OSIS verse identifier.'),
    ('versek', 'szoveg_modern', '', 'A modernizált vers szövege, írásjelekkel.', 'Modernised verse text, with punctuation.'),
    ('versek', 'valtozott', 'igen', 'A vers szövege változott a modernizálásban.', 'The verse text changed in the modernisation.'),
    ('versek', 'valtozott', 'nem', 'A vers szövege változatlan.', 'The verse text is unchanged.'),
]

MODSZER = """# Módszer — a modernizált Károli és a Strong-összekapcsolás

*{cim} · {lex_hu} · adatállapot: {adatallapot} · DOI: {doi}*

## 1. Mi ez az adatkészlet

Károli Gáspár fordításának 1908-as szövege mai helyesírással és mai igealakokkal, szavanként összekapcsolva a héber
és görög eredeti szavak Strong-számaival. A szöveg {konyv} könyvet, {vers} verset és {token} szót tartalmaz. A
modernizálás {valtozo_token} szót (a kieső szavakkal együtt, 4.3) és {valtozo_vers} verset érint; a többi szó és vers változatlan.

A modernizált szöveg a projekt saját munkája. A szópárosítás a Károli 1908 szövegén készült, és önálló
adatkészletként is megjelenik (https://doi.org/{doi_ks}). Ez az adatkészlet a kettő összekapcsolása.

## 2. A kiinduló szöveg és a kulcs

A kiinduló szöveg a Károli 1908 közkincs szövege. Minden vers szavakra (tokenekre) bontva áll; egy szót a vers és a
versen belüli sorszáma azonosít. A modernizálás ezt a kulcsot nem változtatja meg: minden modern alak az 1908-as szó
helyén áll. Ezért kapcsolható össze a modern szöveg a párosítással szótár, újrapárosítás és modell nélkül.

## 3. A modernizálás határa

A szerkesztői döntés szerint a modernizálás két dologra terjed ki: a **helyesírásra** és az **igealakokra**. A
szókincs, a szórend, az írásjelek és a fordító betoldásainak jelölése változatlan. Ahol egy alak a határon állt, ott a
szerkesztő mérés után döntött:

- a mutató *e* (*ez*), az *oh*, a *férfiú*, a *leány* és a hasonló szóváltozatok maradnak: ez szókincs, nem helyesírás;
- a *reá* → *rá* és a *néki, nékem, néked, nékik* → *neki, nekem…* csere a helyesírás része;
- a birtokos *-jok/-jök* → *-juk/-jük* része; a *j* nélküli *-ök* → *-ük* csak ott, ahol a szó többes száma
  egyértelműen más (*szívök* → *szívük*); a mély hangrendű *-ok* marad, mert ott a többes számmal egybeesik;
- a puszta *a mi* csak akkor lesz *ami*, ha a szövegkörnyezet vonatkozó névmást mutat (*a mi Istenünk* marad);
- a kötőhangzós régi múlt (*mondotta* → *mondta*, *szólott* → *szólt*) cserélődik; a felszólító *-jál/-jél*
  (*cselekedjél*) és a *-jék* marad, mert a mai nyelvben is élő, választékos változat;
- a jövő idejű *-nd-* (*mondándok*) marad.

## 4. Az eljárás

### 4.1 Helyesírás

Szabálykészlet, szavanként. A fő szabályok: a különírt vonatkozó névmás egybeírása (*a kik* → *akik*, *a mely* →
*amely*; az „a” a következő szóba olvad); a régi betűkapcsolatok (*cz* → *c*, *lyl* → *ll*, *szsz* → *ssz*); a
*néki*-család és a *reá*; a szótagolási régiségek (*dícsér* → *dicsér*); végül egy saját szótári tábla, amely a Károli
szavainak mai szótári alakját adja, és amelynek helyesírási eltéréseit (*miképen* → *miképpen*, *kivül* → *kívül*) a
szabály átveszi. A magyar Hunspell helyesírási szótár csak mérce volt: a szabályok ellenőrzésére futott, a kiadott
szöveget nem befolyásolta.

### 4.2 Igealak

Szabálykészlet a gyakori régi igealakokra (*teremté* → *teremtette*, *monda* → *mondta*, *lőn* → *lett*,
*vagyon* → *van*, *jő* → *jön*), saját igeragozó modullal (rendhagyó tövek, hangkivetés, hangrend). A *vala* két
szerepét a szabály választja szét: a létigei *vala* → *volt*; a segédigei *vala* a múlt idejű igealakba olvad
(*mondja vala* → *mondta*), és a modern szövegből kiesik. A tárgyas és alanyi ragozás választása a régi alakból nem
mindig olvasható ki: ott a szabály a tagmondatban álló határozott tárgyat keresi, és a szót bizonytalannak jelöli.

A ritka és a jegy nélküli régies alakokra a szabály csak jelöltet ad. Ezeket nyelvi modell nézte át, {llm_kor}
körben, vakon (a modell a szabály jelöltjét nem látta):

1. egy első modell (Claude Sonnet) minden ritka és gyanús alakot;
2. egy második modell (Claude Opus) a vitatott alakokat, ahol a szabály és az első modell eltért;
3–5. a második modell három további körben: két körben a teljes szövegen újra felmért régies alakokat, az utolsóban
   szavanként, a teljes verssel, a szövegkörnyezettől függő eseteket.

A modell válasza önmagában semmit nem írt át. Csere ott történt, ahol legalább két jelölt (a szabály, az első és a
második modell) egyezett, és a tőellenőrzés átengedte: a modern alak egyetlen szó, és megtartja a régi alak
igekötőjét és igetövét, így a modell nem cserélhette másik szóra. Ahol nem volt egyezés, a szó változatlan
maradt. A felhasznált token a hívásnaplók szerint: az első modell {llm_sonnet_m}, a második {llm_opus_m}.

Néhány alak kézi kivétellistába került, ahol a szabály vagy a szótári tábla hibás alakot adott volna (*gyűl-*,
*dűl-* marad; *érte* névutós névmás, nem ige).

### 4.3 Kiesés és összevonás

Két esetben tűnik el szó a modern szövegből: az egybeírt vonatkozó névmás „a”-ja ({osszevonva} szó) és a segédigei
*vala* ({segedige} szó). A kieső szó nem törlődik: saját sorában marad, a `kieso` oszlop jelöli, a `gazda_token`
pedig megadja, melyik szóba olvadt. Ha a kieső szónak Strong-párja van ({kieso_strongos} ilyen szó), az a pár
megmarad, és a modern szövegben a gazdaszóhoz tartozik. Összevonásnál így mindkét régi szó Strong-száma megmarad.

### 4.4 Önellenőrzés és ellenőrzés

Minden versen gépi önellenőrzés fut: a modern szöveget újra szavakra bontva pontosan a nem kieső szavak modern
alakjait kell adnia, sorrendben, és az írásjelek váza nem változhat. Minden szó kulcsa a táblában van.

A szöveget független ellenőr négy körben vizsgálta, ezek után két javítókör következett. A mérés mintákon (a
Wilson-féle 95%-os intervallumot a kiadás számolja a mért darabszámokból):

- helyesírás: a minta {hminta_ossz} cseréjéből {hminta_jo} helyes (a hibaarány 95%-os felső határa
  {hminta_hiba_w_f}%); a puszta *a mi* {ami_ossz} elemes ellenőrző halmazán {ami_hiba} hiba ({ami_jo}/{ami_ossz},
  {ami_p}%);
- igealak: a {minta1_vers} verses mintán {minta1_jo} vers hibátlan; a második, {minta2_vers} verses mintán
  {minta2_csere} csere, ebből {minta2_hiba} hibás (felső határ {minta2_hiba_w_f}%); a független ellenőr friss,
  {ell_vers} verses mintáján {lef_csere} csere, ebből {ell_hiba} hibás (felső határ {ell_hiba_w_f}%);
- lefedettség (maradt-e régies igealak): ugyanezen a friss mintán {lef_p}% ({lef_csere} csere, {lef_kihagyas}
  kihagyás; 95%: {lef_w_a}–{lef_w_f}%). Ebből a teljes szövegben kb. {korp} régies alakban maradt igealak
  becsülhető (95%-os Poisson-sáv kb. {korp_a}–{korp_f}). A második minta magasabb lefedettsége torzított, mert a
  későbbi körök éppen a kihagyásait vették célba.

A maradék ismert hibákat az `ISMERT_HIBAK.md` sorolja fel.

## 5. A Strong-párosítás és a pontossága

A szópárosítás nyelvi modellek javaslata a STEPBible TAHOT (héber) és TAGNT (görög) szövegén: minden magyar szóhoz a
modell kijelöli a héber vagy görög szavakat, a Strong-szám ezekből a forrásokból jön, a modell nem írja. Mózes első
két könyvében két független modell párosított; ahol egyeztek, a pár `magas` bizonyosságú ({magas} pár), máshol egy
modell javaslata (`alacsony`, {alacsony} pár). Minden pár „javaslat” állapotú.

A pontosságot rétegzett véletlen mintán mértük, vak ellenőrrel, és egy független, Strong-számos Károli-kiadással:

- a teljes párkészlet (mellékszavakkal, morfémákkal) egyezése a vak ellenőrrel: {p_osszes}% (95%: {p_osszes_a}–{p_osszes_f}%);
- a fő szavak párjai a független forrással összevetve, {k_n} páron: {k_fs}% (95%: {k_fs_a}–{k_fs_f}%); a
  háromutas ítélet után, amely az eltéréseket a vak ellenőr bevonásával döntötte el, {k_h3}%;
- a héber előtag- és ragmorfémák párjai: {p_morfema}% (95%: {p_morfema_a}–{p_morfema_f}%); ezeket a független forrás
  nem jelöli.

## 6. Az összekapcsolás

A modern szöveg és a párosítás összekapcsolása kulcs szerinti illesztés: a vers és a szó sorszáma. Új pár nem
keletkezik, és egy sem vész el. Gépi kapu igazolja: mind a {par} pár átkerült, mind a {strongos_token} párosított
szó kulcsa megvan a modern táblában, azonos 1908-as alakkal; minden modern szó szerepel; a csomag újragenerálva
bájtra azonos. A betoldott ({betoldas}) és a függőben lévő ({fuggoben}) szónak nincs párja; a három szám összege a
szöveg {token} szava.

A modernizálás lezárásakor a párosítás még {konyv_61} könyvön állt: ezeken {strongos_61} párosított szó volt, és mind
illeszkedett a modern szöveghez. Azóta elkészült a további {konyv_uj} könyv ({uj_konyvek_hu}) párosítása; a modern
szöveg ezeken is szóról szóra illeszkedik. Ezért áll itt {strongos_token} párosított szó; a kapu a {konyv_61}
könyvön a régi számot ({strongos_61}) is igazolja.

## 7. Korlátok

- A párosítás gépi javaslat; a pontossága fent, az ismert hibák az `ISMERT_HIBAK.md`-ben.
- A modernizálás nem fordítás és nem revízió: a szókincs és a szórend a Károlié.
- A szövegkörnyezettől függő igealakok egy része bizonytalannak jelölt ({bizonytalan} szó).
"""

METHODS = """# Methods — the modernised Károli and the Strong linkage

*{cim_en} · {lex_en} · data state: {adatallapot} · DOI: {doi}*

## 1. What this dataset is

The 1908 text of Gáspár Károli's Hungarian Bible translation in present-day spelling and present-day verb forms, linked
word by word to the Strong's numbers of the Hebrew and Greek source words. The text has {konyv} books, {vers} verses and
{token} words. The modernisation touches {valtozo_token} words (including dropped words, 4.3) and {valtozo_vers} verses; all other words and verses are
unchanged.

The modernised text is the project's own work. The word alignment was made on the 1908 Károli text and is also
published as a separate dataset (https://doi.org/{doi_ks}). This dataset links the two.

## 2. Source text and key

The source is the public-domain 1908 Károli text. Every verse is split into words (tokens); a word is identified by its
verse and its position in the verse. The modernisation does not change this key: every modern form stands in the place
of the 1908 word. This is why the modern text can be linked to the alignment without a dictionary, re-alignment or
model.

## 3. Scope of the modernisation

By editorial decision the modernisation covers two things: **spelling** and **verb forms**. Vocabulary, word order,
punctuation and the marking of the translator's additions are unchanged. Where a form lay on the boundary, the editor
decided after measurement:

- the demonstrative *e* (*ez*), *oh*, *férfiú*, *leány* and similar word variants stay: that is vocabulary, not spelling;
- *reá* → *rá* and *néki, nékem, néked, nékik* → *neki, nekem…* are spelling;
- the possessive *-jok/-jök* → *-juk/-jük* is included; *-ök* without *j* → *-ük* only where the plural of the word is
  clearly different (*szívök* → *szívük*); back-vowel *-ok* stays, as it coincides with the plural;
- bare *a mi* becomes *ami* only where the context shows a relative pronoun (*a mi Istenünk*, "our God", stays);
- the old past with a linking vowel (*mondotta* → *mondta*, *szólott* → *szólt*) is replaced; the imperative
  *-jál/-jél* (*cselekedjél*) and *-jék* stay, as they are living, elevated variants today;
- the future in *-nd-* (*mondándok*) stays.

## 4. Procedure

### 4.1 Spelling

A rule set, word by word. Main rules: joining the separately written relative pronoun (*a kik* → *akik*, *a mely* →
*amely*; the "a" merges into the next word); old letter combinations (*cz* → *c*, *lyl* → *ll*, *szsz* → *ssz*); the
*néki* family and *reá*; old syllable spellings (*dícsér* → *dicsér*); and a dictionary table of the project giving the
present-day dictionary form of Károli's words, whose spelling differences (*miképen* → *miképpen*, *kivül* → *kívül*)
the rule adopts. The Hungarian Hunspell dictionary was only a benchmark: it was run to check the rules and did not
influence the published text.

### 4.2 Verb forms

A rule set for the frequent old verb forms (*teremté* → *teremtette*, *monda* → *mondta*, *lőn* → *lett*, *vagyon* →
*van*, *jő* → *jön*), with the project's own conjugation module (irregular stems, vowel elision, vowel harmony). The rule
separates the two roles of *vala*: existential *vala* → *volt*; auxiliary *vala* merges into the past-tense verb
(*mondja vala* → *mondta*) and drops out of the modern text. The choice between definite and indefinite conjugation is
not always readable from the old form: there the rule looks for a definite object in the clause and marks the word as
uncertain.

For rare and unmarked archaic forms the rule only proposes a candidate. These were reviewed by language models in
{llm_kor} rounds, blind (the model did not see the rule's candidate):

1. a first model (Claude Sonnet) on every rare and suspect form;
2. a second model (Claude Opus) on the disputed forms, where the rule and the first model differed;
3–5. the second model in three further rounds: two on archaic forms re-surveyed over the whole text, the last word by
   word, with the full verse, on context-dependent cases.

A model's answer on its own changed nothing. A replacement was made where at least two candidates (the rule, the first
and the second model) agreed and the stem check passed: the modern form is a single word and keeps the verbal prefix
and stem of the old form, so the model could not substitute another word. Where there was no agreement, the word
stayed unchanged. Tokens used according to the call logs: first model {llm_sonnet_m}, second model {llm_opus_m}.

Some forms went into a manual exception list where the rule or the dictionary table would have produced a wrong form
(*gyűl-*, *dűl-* stay; *érte* is a pronoun with postposition, not a verb).

### 4.3 Dropped and merged words

Two kinds of word disappear from the modern text: the "a" of the joined relative pronoun ({osszevonva} words) and
auxiliary *vala* ({segedige} words). A dropped word is not deleted: it keeps its own row, marked in the `kieso` column,
and `gazda_token` gives the word it merged into. If the dropped word has a Strong pair ({kieso_strongos} such words),
that pair is kept and belongs to the host word in the modern text. When words merge, the Strong's numbers of both old
words are therefore kept.

### 4.4 Self-checks and review

An automatic self-check runs on every verse: re-tokenising the modern text must give exactly the modern forms of the
non-dropped words, in order, and the punctuation skeleton must not change. Every word key is in the table.

An independent reviewer examined the text in four rounds, followed by two correction rounds. Measured on samples (the
Wilson 95% intervals are computed by the release from the measured counts):

- spelling: {hminta_jo} of the {hminta_ossz} replacements in the sample correct (95% upper bound of the error rate
  {hminta_hiba_w_f}%); on the {ami_ossz}-item check set for bare *a mi* {ami_hiba} error ({ami_jo}/{ami_ossz},
  {ami_p}%);
- verb forms: on the {minta1_vers}-verse sample {minta1_jo} verses without error; on the second, {minta2_vers}-verse
  sample {minta2_csere} replacements, {minta2_hiba} wrong (upper bound {minta2_hiba_w_f}%); on the independent
  reviewer's fresh {ell_vers}-verse sample {lef_csere} replacements, {ell_hiba} wrong (upper bound {ell_hiba_w_f}%);
- coverage (did archaic verb forms remain): {lef_p}% on the same fresh sample ({lef_csere} replacements,
  {lef_kihagyas} misses; 95%: {lef_w_a}–{lef_w_f}%). This projects to about {korp} verb forms left archaic in the
  whole text (95% Poisson band about {korp_a}–{korp_f}). The higher coverage of the second sample is biased, because
  later rounds targeted exactly its misses.

The remaining known issues are listed in `KNOWN_ISSUES.md`.

## 5. The Strong alignment and its accuracy

The word alignment is a proposal of language models on the STEPBible TAHOT (Hebrew) and TAGNT (Greek) texts: for every
Hungarian word the model marks the Hebrew or Greek words; the Strong's number comes from these sources, the model does
not write it. In Genesis and Exodus two independent models aligned; where they agreed, the pair has `magas` (high)
confidence ({magas} pairs), elsewhere it is one model's proposal (`alacsony`, low; {alacsony} pairs). Every pair has
the status "proposal".

Accuracy was measured on a stratified random sample with a blind reviewer, and against an independent Károli edition
with Strong's numbers:

- the full pair set (with function words and morphemes), agreement with the blind reviewer: {p_osszes}% (95%:
  {p_osszes_a}–{p_osszes_f}%);
- pairs of main words against the independent source, on {k_n} pairs: {k_fs}% (95%: {k_fs_a}–{k_fs_f}%); after
  three-way adjudication, which settled the differences with the blind reviewer, {k_h3}%;
- pairs of Hebrew prefix and suffix morphemes: {p_morfema}% (95%: {p_morfema_a}–{p_morfema_f}%); the independent
  source does not mark these.

## 6. The linkage

Linking the modern text and the alignment is a join on the key: verse and word position. No pair is created and none
is lost. An automatic gate verifies that all {par} pairs were carried over, that the key of all {strongos_token}
aligned words is in the modern table with the same 1908 form, that every modern word is present, and that the package
regenerates byte for byte. Added ({betoldas}) and pending ({fuggoben}) words have no pair; the three numbers add up to
the {token} words of the text.

When the modernisation was completed, the alignment covered {konyv_61} books: they had {strongos_61} aligned words, all
of which matched the modern text. Since then the remaining {konyv_uj} books ({uj_konyvek_en}) have been aligned, and
the modern text matches them word for word as well. Hence the {strongos_token} aligned words here; the gate also
verifies the earlier figure ({strongos_61}) on the {konyv_61} books.

## 7. Limitations

- The alignment is a machine proposal; its accuracy is given above, known issues in `KNOWN_ISSUES.md`.
- The modernisation is neither a new translation nor a revision: vocabulary and word order are Károli's.
- Some context-dependent verb forms are marked uncertain ({bizonytalan} words).
"""

ISMERT_HIBAK = """# Ismert hibák és korlátok

*{cim} · adatállapot: {adatallapot}*

## A modernizálás

1. **Jelöltként maradt régies igealakok.** {jelolt_maradt} szónál a szabály vagy egy modell cserét javasolt, de nem
   volt egyezés, ezért a szó régies alakban maradt.
2. **Magánhangzóval kezdődő ige a mutató *az* után** (*az monda*, *az felele*): néhány ilyen ige régies alakban maradt.
3. **Személyhiba:** három helyen az 1908-as szöveg egyes szám első személyű múlt idejű igéje a modern szövegben
   többes szám harmadik személyű lett: 1Móz 39:15 *kezdék* → *kezdték* (helyesen *kezdtem*), Dán 7:16 *kérék* →
   *kérték* (helyesen *kértem*), Ez 22:30 *keresék* → *keresték* (helyesen *kerestem*). A *-ék* végű régi alak
   egyes szám első és többes szám harmadik személyű is lehet; ezekben a versekben a beszélő első személyben szól.
4. **Az ellenőrzés kihagyásai:** *egybegyűle, sétála, Helybenhagyák, felveheték, béméne, elplántálám, lövének,
   megszerzém* régies alakban maradt.
5. **A mély hangrendű birtokos *-ok*** (*atyjok*-típus *j* nélkül) szándékosan marad, mert a többes számmal egybeesik.
6. **Egyedi régi írásmódok,** amelyeket a szabályok nem fednek (*irígy, akképen, husvét, bölcseség, nyilásának,
   hizelkedő, sujts, nékie*), és az összetételben álló *-jok* (*atyjokfiai*).
7. **Bizonytalan választás:** {bizonytalan} szónál a modern alak a szövegkörnyezettől függ (tárgyas vagy alanyi
   ragozás, személy); a `bizonytalan` oszlop jelöli.

## A Strong-párosítás

8. **Megerősített párhibák:** Péld 3:18 (az „Életnek” és a „fája” párja felcserélt), Ez 43:13 („közsinget”),
   2Kir 10:15 (a kérdő „-é” a kérdő partikula, H9008, nem H3426), Róm 1:12 („Azaz”: a G1161 fordítatlan, nem tartozik
   a párhoz).
9. **Szomszédos szó:** a mintabeli eltérések nagyjából fele a szomszédos héber előtag, névelő vagy elöljáró
   hozzákötése a szóhoz.
10. **Morfémák:** a héber előtag- és ragmorfémák párjait ({morfema} pár) csak a vak ellenőr mérte ({p_morfema}%); a
    független forrás nem jelöli őket.
11. **Függőben:** {fuggoben} szó párosítása kézi döntésre vár; ezeknek nincs párjuk.
12. **A görög szövegváltozat:** a Károli a Textus Receptust fordította, a párosítás alapja a TAGNT, amely több kiadás
    szövegét tartalmazza; {nem_tr} párosított görög szó nem szerepel a Textus Receptusban.

A javítások a következő kiadásba kerülnek; a kiadás a `KIADAS.txt` azonosítójával idézhető.
"""

KNOWN_ISSUES = """# Known issues and limitations

*{cim_en} · data state: {adatallapot}*

## The modernisation

1. **Archaic verb forms left as candidates.** For {jelolt_maradt} words the rule or a model proposed a replacement, but
   there was no agreement, so the word stayed archaic.
2. **Vowel-initial verb after demonstrative *az*** (*az monda*, *az felele*): some such verbs stayed archaic.
3. **Person error:** in three places a first-person singular past verb of the 1908 text became third-person plural
   in the modern text: Gen 39:15 *kezdék* → *kezdték* (correctly *kezdtem*, "I began"), Dan 7:16 *kérék* → *kérték*
   (correctly *kértem*, "I asked"), Ezek 22:30 *keresék* → *keresték* (correctly *kerestem*, "I sought"). The old
   ending *-ék* can be either first-person singular or third-person plural; in these verses the speaker uses the
   first person.
4. **Review misses:** *egybegyűle, sétála, Helybenhagyák, felveheték, béméne, elplántálám, lövének, megszerzém*
   remained archaic.
5. **Back-vowel possessive *-ok*** (without *j*) is left on purpose, as it coincides with the plural.
6. **Isolated old spellings** not covered by the rules (*irígy, akképen, husvét, bölcseség, nyilásának, hizelkedő,
   sujts, nékie*), and *-jok* inside compounds (*atyjokfiai*).
7. **Uncertain choice:** for {bizonytalan} words the modern form depends on context (definite or indefinite
   conjugation, person); marked in the `bizonytalan` column.

## The Strong alignment

8. **Confirmed pair errors:** Prov 3:18 (the pairs of "Életnek" and "fája" are swapped), Ezek 43:13 ("közsinget"),
   2Kgs 10:15 (the interrogative "-é" is the interrogative particle, H9008, not H3426), Rom 1:12 ("Azaz": G1161 is
   untranslated and not part of the pair).
9. **Neighbouring word:** about half of the sample differences attach a neighbouring Hebrew prefix, article or
   preposition to the word.
10. **Morphemes:** pairs of Hebrew prefix and suffix morphemes ({morfema} pairs) were measured by the blind reviewer
    only ({p_morfema}%); the independent source does not mark them.
11. **Pending:** {fuggoben} words await a manual alignment decision and have no pair.
12. **Greek text form:** Károli translated the Textus Receptus, while the alignment uses TAGNT, which covers several
    editions; {nem_tr} aligned Greek words are not in the Textus Receptus.

Corrections go into the next release; a release is cited by its identifier in `RELEASE.txt`.
"""

CITATION = """cff-version: 1.2.0
message: "Ha az adatokat használja, kérjük, ezt az adatkészletet idézze. / If you use the data, please cite this dataset."
type: dataset
title: "{cim} / {cim_en}"
authors:
  - family-names: "Demeter"
    given-names: "Tamás"
    orcid: "https://orcid.org/{orcid}"
doi: "{doi}"
license: CC-BY-4.0
abstract: >-
  A Károli-biblia 1908-as szövegének modernizált változata (helyesírás és
  igealak), szavanként összekapcsolva a héber és görög eredeti szavak
  Strong-számaival (STEPBible TAHOT/TAGNT, CC BY 4.0). (English) The 1908
  Károli Bible text modernised in spelling and verb forms, linked word by word
  to the Strong's numbers of the Hebrew and Greek source words (STEPBible
  TAHOT/TAGNT, CC BY 4.0).
keywords:
  - Károli-biblia
  - Strong-számok
  - szópárosítás
  - Hungarian Bible
  - word alignment
references:
  - type: dataset
    title: "Károli 1908 – Strong szóillesztés / Károli 1908 – Strong word alignment"
    authors:
      - family-names: "Demeter"
        given-names: "Tamás"
    doi: "{doi_ks}"
  - type: dataset
    title: "{lex_en} — open data core"
    authors:
      - family-names: "Demeter"
        given-names: "Tamás"
    doi: "{doi_mag}"
"""

GITATTRIBUTES = """# Sorvég: minden fájl LF-fel, minden checkouton (az ellenőrző összeg az LF-es bájtokra szól).
* text eol=lf
# A közlemény-tervezet a megjelenésig nem része a kiadásnak.
kozlemeny/ export-ignore
"""

KOZLEMENY_HU = """# A Károli-biblia mai helyesírással, szavanként az eredeti nyelvekhez kötve

*Közlemény-tervezet · {cim} · {lex_hu} · DOI: {doi}*

A Károli Gáspár-féle bibliafordítás a magyar nyelv egyik alapszövege, de 1908-as kiadásának helyesírása és igealakjai
— *teremté, monda, vala, lőn, a kik* — a mai olvasót megállítják. A {lex_hu} most közreadja a szöveg modernizált
változatát, szabad licenccel, és minden szavát összekapcsolja azzal a héber vagy görög szóval, amelyet fordít.

**Mit és mit nem.** A modernizálás szándékosan szűk: csak a helyesírás és az igealakok változnak (*teremtette, mondta,
volt, lett, akik*). A szókincs, a szórend, az írásjelek és a fordító betoldásai a Károliéi maradnak. Ahol egy alak a
határon állt — a *reá* vagy a *-jok* birtokos —, ott mérés után szerkesztői döntés született, és ez a döntés a
módszertani leírásban olvasható. A szöveg {vers} versében {valtozo_vers} vers változott.

**Hogyan.** A munka nagy része szabályokkal készült, szavanként, saját szótári táblával és igeragozó modullal. A ritka
és kétes igealakokat nyelvi modellek nézték át, vakon, öt körben; egy alak csak ott változott, ahol legalább két
független javaslat egyezett, és a szótő ellenőrzése átengedte. A szöveget független ellenőr négy körben vizsgálta. Az ő
friss, {ell_vers} verses mintáján a {lef_csere} igealak-cseréből {ell_hiba} volt hibás (a hibaarány
95%-os felső határa {ell_hiba_w_f}%), a helyesírási minta {hminta_ossz} cseréjéből szintén {hminta_ossz_hiba}, a második, {minta2_vers} verses igealak-minta
{minta2_csere} cseréjéből szintén {minta2_hiba}; a puszta „a mi” {ami_ossz} elemes ellenőrző halmazán {ami_hiba} hiba volt. Ugyanezen a friss mintán a régies igealakok
{lef_p}%-a lett modern ({lef_csere} csere, {lef_kihagyas} kihagyás; 95%: {lef_w_a}–{lef_w_f}%); ebből a teljes
szövegben kb. {korp} régies alakban maradt igealak becsülhető (95%-os sáv kb. {korp_a}–{korp_f}). A maradék ismert
hibákat a közölt ismert-hibák lista meg is nevezi.

**A Strong-számok.** A szópárosítás a Károli 1908-as szövegén készült, és önálló adatkészletként is megjelenik. Mivel a
modernizálás minden szót a helyén hagyott, a két réteg egyszerű kulccsal — vers és szósorszám — összekapcsolható:
új párosítás nem kellett, egy pár sem veszett el. Ahol két régi szó egybeolvadt (*a kik* → *akik*), mindkettő párja
megmaradt. A párosítás pontosságát független forrással mértük: a fő szavakon {k_fs}%, a teljes párkészleten a vak
ellenőrrel {p_osszes}%.

**Kinek.** Bibliaolvasóknak, akik a megszokott Károlit mai alakban és az eredeti szavak felé nyitva szeretnék olvasni;
kutatóknak, akik a magyar bibliai szóhasználatot a héber és görög szöveggel együtt vizsgálják; fejlesztőknek, akik
szabad, szavanként kulcsolt magyar bibliaszövegre építenének.

Az adatkészlet CC BY 4.0 licenccel szabadon felhasználható: https://doi.org/{doi}
"""

KOZLEMENY_EN = """# The Károli Bible in present-day spelling, linked word by word to the original languages

*Announcement draft · {cim_en} · {lex_en} · DOI: {doi}*

Gáspár Károli's Bible translation is one of the foundational texts of the Hungarian language, but the spelling and verb
forms of its 1908 edition — *teremté, monda, vala, lőn, a kik* — stop the present-day reader. The {lex_en} now releases a
modernised version of the text under an open licence, and links every word to the Hebrew or Greek word it translates.

**What, and what not.** The modernisation is deliberately narrow: only spelling and verb forms change (*teremtette,
mondta, volt, lett, akik*). Vocabulary, word order, punctuation and the translator's additions remain Károli's. Where a
form lay on the boundary — *reá*, or the possessive *-jok* — an editorial decision was taken after measurement, and it
is documented in the methods description. Of the text's {vers} verses, {valtozo_vers} changed.

**How.** Most of the work was done by rules, word by word, with the project's own dictionary table and conjugation
module. Rare and doubtful verb forms were reviewed by language models, blind, in five rounds; a form changed only where
at least two independent proposals agreed and the stem check let it through. An independent reviewer examined the text
in four rounds. On the reviewer's fresh {ell_vers}-verse sample {ell_hiba} of the {lef_csere} verb-form replacements
were wrong (95% upper bound of the error rate {ell_hiba_w_f}%), and {hminta_ossz_hiba} of the {hminta_ossz} replacements
in the spelling sample, and {minta2_hiba} of the {minta2_csere} replacements in
the second, {minta2_vers}-verse verb-form sample; the {ami_ossz}-item check set for bare "a mi" had {ami_hiba} error. On the same fresh sample
{lef_p}% of archaic verb forms were modernised ({lef_csere} replacements, {lef_kihagyas} misses; 95%:
{lef_w_a}–{lef_w_f}%), which projects to about {korp} verb forms left archaic in the whole text (95% band about
{korp_a}–{korp_f}). The remaining errors are named in the published list of known issues.

**The Strong's numbers.** The word alignment was made on the 1908 Károli text and is also published as a separate
dataset. Since the modernisation left every word in its place, the two layers join on a simple key — verse and word
position: no re-alignment was needed and no pair was lost. Where two old words merged (*a kik* → *akik*), the pairs of
both were kept. The accuracy of the alignment was measured against an independent source: {k_fs}% on main words, and
{p_osszes}% on the full pair set against a blind reviewer.

**For whom.** Bible readers who want the familiar Károli in present-day form and open towards the original words;
researchers studying Hungarian biblical usage together with the Hebrew and Greek text; developers building on an open,
word-keyed Hungarian Bible text.

The dataset is freely usable under CC BY 4.0: https://doi.org/{doi}
"""


# ----------------------------------------------------------------------------- összeállítás

def tsv_szoveg(fej, sorok, en=True):
    ki = [FEJLEC_HU] + ([FEJLEC_EN] if en else []) + ['\t'.join(fej)]
    ki += ['\t'.join(s) for s in sorok]
    return '\n'.join(ki) + '\n'


def kodkonyv_md():
    ki = ['# Kódkönyv / Codebook', '', '*%s / %s*' % (CIM_HU, CIM_EN), '']
    for fajl, cim in (('konyvek', '`konyvek/NN_Konyv.tsv`'), ('versek', '`versek.tsv`')):
        ki += ['## %s' % cim, '', '| oszlop / column | érték / value | leírás | description |', '|---|---|---|---|']
        for f, o, e, hu, en in KODKONYV_SOROK:
            if f == fajl:
                ki.append('| `%s` | %s | %s | %s |' % (o, ('`%s`' % e) if e else '', hu, en))
        ki.append('')
    return '\n'.join(ki)


def export():
    modern, parok, par_db, allapot, versek = beolvas()
    konyvek = vetit(modern, parok, allapot)
    N = szamok(modern, konyvek, par_db, allapot, versek)
    hu, en = fmt(N, 'hu'), fmt(N, 'en')
    for d in (hu, en):
        d.update({'cim': CIM_HU, 'cim_en': CIM_EN, 'step': STEP_ATTRIB})
    fajlok = {}
    for i, (kk, sorok) in enumerate(konyvek, 1):
        fajlok['konyvek/%02d_%s.tsv' % (i, kk)] = tsv_szoveg(FEJ, sorok)
    vsorok = [[NM.osis(v['igehely']), v['szoveg_modern'], 'igen' if v['valtozott'] == 'igen' else 'nem']
              for v in versek]
    fajlok['versek.tsv'] = tsv_szoveg(VERS_FEJ, vsorok)
    fajlok['kodkonyv.tsv'] = tsv_szoveg(['fajl', 'oszlop', 'ertek', 'leiras_hu', 'leiras_en'],
                                        [list(s) for s in KODKONYV_SOROK])
    fajlok['KODKONYV.md'] = kodkonyv_md()
    fajlok['OLVASSEL.md'] = OLVASSEL.format(**hu)
    fajlok['README.md'] = README.format(**en)
    fajlok['LICENSE'] = LICENSE.format(**hu)
    fajlok['ATTRIBUCIO.md'] = ATTRIBUCIO.format(**hu)
    fajlok['MODSZER.md'] = MODSZER.format(**hu)
    fajlok['METHODS.md'] = METHODS.format(**en)
    fajlok['ISMERT_HIBAK.md'] = ISMERT_HIBAK.format(**hu)
    fajlok['KNOWN_ISSUES.md'] = KNOWN_ISSUES.format(**en)
    fajlok['CITATION.cff'] = CITATION.format(**hu)
    fajlok['.gitattributes'] = GITATTRIBUTES
    # ellenőrző összeg: minden kiadott fájl, a közlemény-tervezet nélkül
    sor = ['%s  %s' % (hashlib.sha256(fajlok[rel].encode('utf-8')).hexdigest(), rel) for rel in sorted(fajlok)]
    fajlok['ELLENORZO_OSSZEG.sha256'] = '\n'.join(sor) + '\n'
    hash_ = hashlib.sha256(fajlok['ELLENORZO_OSSZEG.sha256'].encode('utf-8')).hexdigest()
    datum = N['adatallapot']
    fajlok['KIADAS.txt'] = ('kiadas_azonosito: %s-%s\nadatallapot_datuma: %s\ntartalmi_hash_sha256: %s\n'
                            'kozzeteteli_hely: %s\n' % (datum, hash_[:16], datum, hash_, KANONIKUS_HELY))
    fajlok['RELEASE.txt'] = ('release_id: %s-%s\ndata_state_date: %s\ncontent_hash_sha256: %s\n'
                             'publication_place: %s\n' % (datum, hash_[:16], datum, hash_, KANONIKUS_HELY))
    # a közlemény-tervezet (export-ignore; nincs az ellenőrző összegben)
    fajlok[KOZLEMENY_DIR + 'kozlemeny_hu.md'] = KOZLEMENY_HU.format(**hu)
    fajlok[KOZLEMENY_DIR + 'kozlemeny_en.md'] = KOZLEMENY_EN.format(**en)
    return fajlok, N


def kiir(fajlok, kimenet):
    abs_ki = os.path.join(GYOKER, kimenet) if not os.path.isabs(kimenet) else kimenet
    if os.path.isdir(abs_ki):
        for gy, _, nevek in os.walk(abs_ki):
            for n in nevek:
                rel = os.path.relpath(os.path.join(gy, n), abs_ki).replace('\\', '/')
                if rel not in fajlok:
                    os.remove(os.path.join(gy, n))
    for rel, tartalom in fajlok.items():
        ut = os.path.join(abs_ki, rel)
        os.makedirs(os.path.dirname(ut), exist_ok=True)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(tartalom)
    return abs_ki


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    ap.add_argument('--kimenet', default=KIMENET)
    a = ap.parse_args()
    fajlok, N = export()
    ut = kiir(fajlok, a.kimenet)
    print('modernizált Károli – Strong exportálva: %s (%d fájl)' % (ut, len(fajlok)))
    for k in ('konyv', 'vers', 'token', 'valtozo_token', 'par', 'strongos_token', 'kieso_strongos', 'sor'):
        print('  %-16s %9d' % (k, N[k]))
    return 0


if __name__ == '__main__':
    sys.exit(main())
