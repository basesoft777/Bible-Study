#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
general.py -- F4 G1/G3/G4: a motivumlexikon generatorai.

Az `adat/` reteg (kanonikus igazsagforras, l. adat/SEMA.md) determinisztikus
kepe markdown-blokkokra forditva. Alapelv (F4_GENERATOR_BRIEF.md D1): a
generator elso korben SEMMIT nem ir felul -- alapertelmezesben a --kimenet
konyvtar ala termel (alapertelmezes: generalt_proba/), es a kimenet maga a
diff. Az elesites (a marker-blokkok tenyleges beirasa az eles fajlokba) kulon
tetel (G7), kulon commit, kimenetenkent emberi jovahagyas utan -- ezt a
szkript soha nem vegzi el magatol.

Marker-blokk, vegyes fajlban (D2):

    <!-- GENERÁLT-KEZDET: general.py --cel naplo#attekintes | forrás: ... | ts=... -->

    *Ez a blokk a táblában betöltött N motívum-ID-t fedi; ...*

    ...torzs...

    <!-- GENERÁLT-VÉGE: naplo#attekintes -->

A hatokor-sor szamai mindig a tablarol jonnek (sose beegetve), l.
hatokor_naplo_attekintes() es tarsai.

CLI:
    python eszkozok/general.py --cel {naplo,index,naplok,study,nyitott,mind}
                               [--id ID]
                               [--kimenet DIR]      # alapertelmezes: generalt_proba/
                               [--ir]               # csak ezzel ir eles fajlba
                               [--ellenoriz]         # nem ir; diffel, 1-gyel lep ki eltéresnel

--ir nelkul a szkript SOHA nem ir eles fajlba -- csak a --kimenet konyvtar
ala. Elesitheto cel harom van (ELESITHETO): naplo, index, nyitott. A naplok es
a study cel a briefek G7 tetele szerint ebben a fazisban NEM elesitheto --
csak probat termel, es --ellenoriz-zel PIROS, mert nincs mihez merni.

TSV-olvasas kizarolag split('\\t')-vel, iras '\\t'.join()-nal -- a `csv` modul
importja is tilos (CLAUDE.md, "TSV-olvasas" szakasz).

A forrasretegbol (`motivumok/[ID].md`) a beolvasztas KIZAROLAG a
BEOLVASZTHATO_SZAKASZOK allowlistjet olvashatja: a "Kulcsszavak részletesen"
szakaszt es a ⭐-prozat. A harom archiv szakasz (ARCHIV_SZAKASZOK) elavult,
tablarol levezetheto erteket hordoz, es nem olvashato -- l. K16 / D15.

Futtatas a repo gyokerebol:
    python eszkozok/general.py --cel naplo
    python eszkozok/general.py --cel index --ellenoriz
"""

import argparse
import datetime
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAT = os.path.join(ROOT, 'adat')
MOTIVUMOK_TSV = os.path.join(ADAT, 'motivumok.tsv')
ELOFORDULASOK_TSV = os.path.join(ADAT, 'elofordulasok.tsv')
JELOLTEK_TSV = os.path.join(ADAT, 'jeloltek.tsv')
NAPLO_MD = os.path.join(ROOT, 'motivumlog', 'PaRDeS_motivumok.md')
INDEX_MD = os.path.join(ROOT, 'Lezart_tematikus_tanulmanyok_index.md')
NYITOTT_MD = os.path.join(ROOT, 'NYITOTT_FELADATOK.md')
NAPLOK_DIR = os.path.join(ROOT, 'tematikus_lezart', 'naplok')

# A meglévő 7 kereszthivatkozás-napló fájlneve -> motívum-ID (mérve, l.
# F4_GENERATOR_BRIEF.md G5). A HAMART-001-hez van napló, de nincs betöltve a
# motivumok.tsv-be; az ANTROP-001-hez nincs napló (a G5 ezt új fájlnévvel
# rendereli). A leképezés nem vezethető le fájlnév-mintából (a Melkizedek-fájl
# megtartja a "_tematikus" tagot, a többi eldobja), ezért tételes.
NAPLO_ID_TERKEP = {
    'Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md': 'HAMART-001',
    'Hadesz_Seol_kereszthivatkozas_naplo.md': 'ALVIL-001',
    'Isten_fiai_Nefilim_Gibborim_kereszthivatkozas_naplo.md': 'MENNY-001',
    'Melkizedek_tematikus_kereszthivatkozas_naplo.md': 'KIRALY-001',
    'Rafaim_kereszthivatkozas_naplo.md': 'HODIT-001',
    'Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md': 'ISTENTISZT-001',
    'Tehom_kereszthivatkozas_naplo.md': 'TEREMT-001',
}
ID_NAPLO_TERKEP = {azon: fajlnev for fajlnev, azon in NAPLO_ID_TERKEP.items()}

MOTIVUMOK_DIR = os.path.join(ROOT, 'motivumok')

# --- K16 / D15: mit szabad a forrasretegbol beolvasztani -------------------
#
# A het `motivumok/[ID].md` ot szakaszbol all, de kozuluk harom ARCHIV: a
# tartalmuk a D13 ota a generalt blokk birtoka (elofordulas-szam, statusz-
# cimke, index-sorszam), es a forrasretegben szandekosan ELAVULT ertekkel all
# -- pl. az ALVIL-001 "4 elofordulas"-a, miutan a tabla 6-ot mond. Ezek a
# szakaszok a fejlecukben *(archív ...)* jelolest hordoznak (K16), es a
# beolvasztas SOHA nem olvashatja oket: kulonben az elavult ertek visszaszivarog
# a generalt blokkba, es pont azt a reteget rontja el, amelyet a generator
# birtokol.
#
# A szures ALLOWLIST, nem tiltolista: nem a jelolest keressuk (az emberi
# olvasonak szol es elirhato), hanem tetelesen felsoroljuk, mi olvashato.
# Uj szakasz a forrasretegben alapertelmezesben NEM olvashato -- csak akkor,
# ha ide is felkerul, dontessel.
BEOLVASZTHATO_SZAKASZOK = (
    '## Kulcsszavak részletesen — naplóbejegyzés',
    '## ⭐ Emlékeztető küszöb — a napló mai bekezdése',
)

ARCHIV_SZAKASZOK = (
    '## Tematikus áttekintés — a napló mai tétele',
    '## Kulcsszó-index — a napló mai sora',
    '## Lezárt tanulmányok indexe — a mai kézi sor',
)


def forrasreteg_beolvaszthato_szakaszok(motivum_id):
    """A `motivumok/[ID].md` beolvaszthato szakaszai: {fejlec: torzs}.

    Csak a BEOLVASZTHATO_SZAKASZOK-ban felsorolt fejlecek kerulnek bele; minden
    mas szakasz -- nevezetesen a harom ARCHIV_SZAKASZOK-beli -- kimarad, akkor
    is, ha a fejlecrol hianyzik az *(archív ...)* jeloles. A fejlec-illesztes
    prefix-alapu, mert a jeloles a fejlec-sor vegen all.

    Hianyzo fajl eseten ures dict -- nem hiba: az ANTROP-001-nek pl. nincs
    minden szakasza.
    """
    ut = os.path.join(MOTIVUMOK_DIR, '%s.md' % motivum_id)
    if not os.path.exists(ut):
        return {}
    with io.open(ut, encoding='utf-8', newline='') as fh:
        sorok = fh.read().split('\n')

    eredmeny = {}
    aktualis = None
    for sor in sorok:
        if sor.startswith('## '):
            aktualis = None
            for fejlec in BEOLVASZTHATO_SZAKASZOK:
                if sor == fejlec or sor.startswith(fejlec + ' '):
                    aktualis = fejlec
                    eredmeny[fejlec] = []
                    break
            continue
        if aktualis is not None:
            eredmeny[aktualis].append(sor)

    return {k: '\n'.join(v).strip() for k, v in eredmeny.items()}


TS = datetime.date.today().isoformat()

# A ma az elofordulasok.tsv-ben ELOFORDULO ujszovetsegi konyv-tokenek -- nem az
# osszes bibliai konyv (l. a konyv_teszamentum() dokumentaciojat lent). A K15
# utan kizarolag a normalizalo tabla roevid alakjai allnak itt: a hosszu
# variansok (`Jelenések`, `Lukács`, `Máté`, `Róma`) kikerultek a tablabol.
UJSZOVETSEGI_TOKENEK = {
    '1Kor', '1Pét', '1Thessz', '2Pét', '2Tim', 'ApCsel', 'Jel', 'Júd',
    'Luk', 'Mt', 'Róm', 'Zsid',
}

KONYV_NORMALIZALO_TSV = os.path.join(ROOT, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')

# SZANDEKOSAN URES (K15/D14). Korabban ez a szotar javitotta a renderelo
# oldalan az elofordulasok.tsv negy hosszu konyvnev-varianset (`Jelenések`,
# `Lukács`, `Máté`, `Róma`). A javitas 2026-09-15-tol a TABLABAN tortent meg
# (13 sor, eszkozok/k15_konyvnev_normalizalas.py), mert a tabla kulcsa
# id + igehely: a renderelo-oldali alias csak a generatort javitotta volna
# meg, a gate.py-t, a lekerdez.py-t es minden jovobeli joint nem.
#
# JELENTO OR, amely NEM javit: ha ide barmi visszakerul, az azt jelenti, hogy
# a tabla ujra ket alakban tarol egy konyvet -- a helyes valasz a tabla
# javitasa, nem a szotar bovitese. A konyv_sorszam() ezert NEM hasznalja
# feloldasra; az ismeretlen token a hianyzo_konyvek jelentesbe kerul.
KONYV_ALIAS = {}


def konyv_sorrend_betolt():
    """{magyar_rövidítés: sorszám} -- a konkordancia/Konyv_normalizalo_tabla.tsv
    SORRENDJE maga a kanonikus sorrend (nincs önálló sorszám-oszlop, K13)."""
    _, sorok = tsv_beolvas(KONYV_NORMALIZALO_TSV)
    return {sor['Magyar rövidítés']: i for i, sor in enumerate(sorok)}


def konyv_sorszam(token, konyv_sorrend, hianyzo_konyvek):
    """A token kanonikus sorszáma. Ismeretlen könyvet a lista VÉGÉRE teszi,
    de felveszi a hianyzo_konyvek halmazba -- a hívó ezt jelentse, ne
    hallgassa el (F4_GENERATOR_BRIEF.md K13: "ne rendezd a lista végére
    némán").

    A KONYV_ALIAS itt szándékosan NEM oldja fel a tokent (K15/D14) -- a
    szótár üres, és ha nem az, az őr jelent, nem javít."""
    if KONYV_ALIAS:
        print('  K15-ŐR: a KONYV_ALIAS nem üres (%s) -- a könyvnév-normalizálás '
              'a táblában történik, nem a renderelőben (D14).'
              % ', '.join(sorted(KONYV_ALIAS)), file=sys.stderr)
    kulcs = token
    if kulcs in konyv_sorrend:
        return konyv_sorrend[kulcs]
    hianyzo_konyvek.add(token)
    return len(konyv_sorrend) + 1


def igehely_fejezet_vers(igehely):
    """(fejezet, vers) -- az igehely ELSŐ fejezet:vers párja; tartománynál
    (pl. '9:1-2', '7:1-28') a kezdőpont szerint rendezendő (K13)."""
    m = re.search(r'(\d+):(\d+)', igehely)
    return (int(m.group(1)), int(m.group(2))) if m else (0, 0)


def igehely_rendezo_kulcs(igehely, konyv_sorrend, hianyzo_konyvek):
    """Rendezőkulcs egy igehelyhez (vagy fő-előfordulás csoport-szöveghez):
    (könyv kanonikus sorszáma, fejezet, vers) -- K13."""
    token = konyv_token(igehely)
    fejezet, vers = igehely_fejezet_vers(igehely)
    return (konyv_sorszam(token, konyv_sorrend, hianyzo_konyvek), fejezet, vers)


# ---------------------------------------------------------------------------
# TSV I/O -- split('\t') / '\t'.join(), a csv modul nem hasznalhato ezeken a
# tablakon (CLAUDE.md, "TSV-olvasas" szakasz: a mezok szabad magyar szoveget
# tartalmaznak idezojelekkel, a csv ezt idezes-szintaxisnak veszi).
# ---------------------------------------------------------------------------

def tsv_beolvas(path):
    """(fejlec:list[str], sorok:list[dict]) -- '#' elotetsorok es ures sorok kihagyva."""
    with io.open(path, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    nyers_sorok = nyers.split(sorveg)
    if nyers_sorok and nyers_sorok[-1] == '':
        nyers_sorok = nyers_sorok[:-1]
    fejlec_idx = next(i for i, s in enumerate(nyers_sorok) if s and not s.startswith('#'))
    fejlec = nyers_sorok[fejlec_idx].split('\t')
    sorok = []
    for s in nyers_sorok[fejlec_idx + 1:]:
        if not s.strip() or s.startswith('#'):
            continue
        mezok = s.split('\t')
        if len(mezok) != len(fejlec):
            raise ValueError('oszlopszám-eltérés a %s fájlban: %r' % (path, s))
        sorok.append(dict(zip(fejlec, mezok)))
    return fejlec, sorok


def sorveg_elemez(path):
    """(domináns_sorvég, crlf_db, lf_db) -- a célfájl mai sorvég-arányának mérése (K7)."""
    with io.open(path, 'rb') as f:
        adat = f.read()
    crlf = adat.count(b'\r\n')
    lf_osszes = adat.count(b'\n')
    lf = lf_osszes - crlf
    domináns = '\r\n' if crlf > lf else '\n'
    return domináns, crlf, lf


def szoveg_beolvas(path):
    with io.open(path, encoding='utf-8') as f:
        return f.read()


def konyv_token(igehely):
    """A vezető könyvnév-token (pl. '1Móz', 'Zsolt', 'Lukács') a fejezet:vers előtt."""
    m = re.match(r'^(\d*[^\d\s]+)', igehely)
    return m.group(1) if m else igehely


def konyv_teszamentum(token):
    """'ÓSZ' vagy 'ÚSZ' -- kizárólag a ma az elofordulasok.tsv-ben ténylegesen
    előforduló könyv-tokenek alapján (UJSZOVETSEGI_TOKENEK), nem a teljes
    bibliai kánon alapján. Ha egy jövőbeli betöltés új könyvet hoz be, ezt a
    halmazt bővíteni kell -- a szkript ezt nem találja ki magától."""
    return 'ÚSZ' if token in UJSZOVETSEGI_TOKENEK else 'ÓSZ'


# ---------------------------------------------------------------------------
# Marker-blokkok
# ---------------------------------------------------------------------------

def blokk(cel_kulcs, forras_lista, hatokor_sor, torzs):
    fejl = '<!-- GENERÁLT-KEZDET: general.py --cel %s | forrás: %s | ts=%s -->' % (
        cel_kulcs, ', '.join(forras_lista), TS)
    veg = '<!-- GENERÁLT-VÉGE: %s -->' % cel_kulcs
    return '\n\n'.join([fejl, '*%s*' % hatokor_sor, torzs, veg])


def fejlec_stampel(cel, forras_lista):
    return '<!-- GENERÁLT: general.py --cel %s | forrás: %s | ts=%s -->' % (
        cel, ', '.join(forras_lista), TS)


# --- G7: marker-parok kezelese eles fajlban -------------------------------
#
# A blokk azonossaga a CEL-KULCS, nem a tartalom es nem a ts. A kezdo marker
# ts-e futasonkent valtozik, ezert az --ellenoriz a marker-parok KOZOTTI
# torzset veti ossze, nem a markereket.

MARKER_KEZDET = '<!-- GENERÁLT-KEZDET: general.py --cel %s |'
MARKER_VEGE = '<!-- GENERÁLT-VÉGE: %s -->'


def blokk_torzs(blokk_szoveg, cel_kulcs):
    """A marker-par kozotti torzs (a hatokor-sorral egyutt), markerek nelkul."""
    veg = MARKER_VEGE % cel_kulcs
    i = blokk_szoveg.index('-->') + len('-->')
    j = blokk_szoveg.index(veg)
    return blokk_szoveg[i:j]


def marker_par_keres(fajl_szoveg, cel_kulcs):
    """(kezdet_idx, torzs_kezdet, torzs_veg, veg_idx) vagy None."""
    kezd_minta = MARKER_KEZDET % cel_kulcs
    i = fajl_szoveg.find(kezd_minta)
    if i < 0:
        return None
    torzs_kezd = fajl_szoveg.index('-->', i) + len('-->')
    veg = MARKER_VEGE % cel_kulcs
    j = fajl_szoveg.find(veg, torzs_kezd)
    if j < 0:
        raise ValueError('nyitó marker záró pár nélkül: %s' % cel_kulcs)
    return i, torzs_kezd, j, j + len(veg)


def marker_blokkok_nelkul(fajl_szoveg):
    """A fajl szovege a GENERÁLT-KEZDET…GENERÁLT-VÉGE szakaszok NELKUL --
    a hatokor-szamlalok csak a kezi tartalmat lathatjak (l.
    naplo_bullet_szamlalo)."""
    return re.sub(r'<!-- GENERÁLT-KEZDET:.*?<!-- GENERÁLT-VÉGE: [^>]*-->',
                  '', fajl_szoveg, flags=re.S)


def blokk_beilleszt(fajl_szoveg, cel_kulcs, uj_blokk, horgony):
    """(uj_szoveg, mit_csinalt). Ha a marker-par megvan, a TORZSET csereli
    (a kezi tartalom a blokkon kivul erintetlen); ha nincs, a horgony-sor
    utan szurja be a teljes blokkot. Horgony nelkul/nem talalt horgonynal
    hibat dob -- nem tippel helyet."""
    talalat = marker_par_keres(fajl_szoveg, cel_kulcs)
    if talalat:
        _, tk, tv, _ = talalat
        regi = fajl_szoveg[tk:tv]
        uj = blokk_torzs(uj_blokk, cel_kulcs)
        if regi == uj:
            return fajl_szoveg, 'változatlan'
        return fajl_szoveg[:tk] + uj + fajl_szoveg[tv:], 'frissítve'
    if horgony is None:
        raise ValueError('nincs marker-pár és nincs horgony: %s' % cel_kulcs)
    if fajl_szoveg.count(horgony) != 1:
        raise ValueError('a horgony %d helyen illeszkedik (%s): %r'
                         % (fajl_szoveg.count(horgony), cel_kulcs, horgony))
    return fajl_szoveg.replace(horgony, horgony + '\n\n' + uj_blokk, 1), 'beszúrva'


# ---------------------------------------------------------------------------
# Adatszervezés
# ---------------------------------------------------------------------------

def elofordulasok_id_szerint(elofordulasok):
    csoport = {}
    for sor in elofordulasok:
        csoport.setdefault(sor['id'], []).append(sor)
    return csoport


def fo_elofordulas_csoportok(sorok):
    """Egy ID sorai közül a fo_elofordulas mező distinct értékei, a sorokban
    való első megjelenés sorrendjében (l. adat/SEMA.md 2.2.3 -- csoportkulcs,
    nem igen/nem)."""
    latott = []
    for sor in sorok:
        cs = sor.get('fo_elofordulas', '')
        if cs and cs not in latott:
            latott.append(cs)
    return latott


# ---------------------------------------------------------------------------
# G3 -- motívumnapló generált szakaszai
# ---------------------------------------------------------------------------

def naplo_bullet_szamlalo(naplo_szoveg):
    """(felszint, alpont) -- a '## Tematikus áttekintés' szakasz '- ' kezdetű
    top-szintű, illetve behúzott '  - ↳' alpont tételeinek száma.

    K12': a hatókör-sor számlálója és nevezője azonos granularitású legyen.
    A HODIT-001 betöltött ID ebben a szakaszban CSAK alpontként szerepelt
    ('  - ↳ Rafeusok/óriás-népek …'), tehát a puszta top-szintű szám nem
    volna azonos granularitású -- a generátor ezért a felszint + alpont
    számot használja (l. render_naplo_attekintes()).

    A GENERÁLT MARKER-BLOKKOK TARTALMA KIMARAD a számlálásból (G7). Enélkül
    a blokk a SAJÁT sorait is beleszámolná az élesítés után, tehát a
    hatókör-sor önmagától függne, és soha nem érne fixpontot."""
    szoveg = marker_blokkok_nelkul(naplo_szoveg)
    m = re.search(r'^## Tematikus áttekintés\n(.*?)\n## ', szoveg, re.S | re.M)
    if not m:
        return None
    szakasz = m.group(1)
    sorok = szakasz.split('\n')
    felszint = sum(1 for sor in sorok if re.match(r'^- ', sor))
    alpont = sum(1 for sor in sorok if re.match(r'^\s+- ', sor))
    return felszint, alpont


def render_naplo_attekintes(motivumok, elof_id_szerint, naplo_szoveg):
    n_betoltott = len(motivumok)
    bullet_szamok = naplo_bullet_szamlalo(naplo_szoveg)
    if bullet_szamok is None:
        hatokor = 'Ez a blokk a táblában betöltött %d motívum-ID-t fedi.' % n_betoltott
    else:
        felszint, alpont = bullet_szamok
        teljes = felszint + alpont
        hatokor = ('Ez a blokk a táblában betöltött %d motívum-ID-t fedi; a napló '
                    'Tematikus áttekintés szakasza a blokkon kívül további %d kézi '
                    'tételt sorol fel (%d felső szint + %d alpont -- K12\': azonos '
                    'granularitás, az alpontok is számítanak), amelyek kézi '
                    'karbantartásban maradnak.'
                    % (n_betoltott, teljes, felszint, alpont))

    tema_szerint = {}
    for m in motivumok:
        tema_szerint.setdefault(m.get('tema') or '(nincs téma megadva)', []).append(m)

    sorok = []
    for tema in sorted(tema_szerint):
        sorok.append('**%s**' % tema)
        for m in tema_szerint[tema]:
            sorai = elof_id_szerint.get(m['id'], [])
            n_fo = len(fo_elofordulas_csoportok(sorai))
            m_sor = len(sorai)
            sorok.append('- %s `[ID: %s]` — %s fő előfordulás / %s igehely-sor — %s (%s, %s)'
                          % (m['cim'], m['id'], n_fo, m_sor, m['statusz'],
                             m['statusz_verzio'], m['statusz_datum']))
        sorok.append('')

    return blokk('naplo#attekintes', ['adat/motivumok.tsv', 'adat/elofordulasok.tsv'],
                  hatokor, '\n'.join(sorok).strip())


def render_naplo_kuszob(motivumok, elof_id_szerint):
    n_betoltott = len(motivumok)
    hatokor = 'Ez a blokk a táblában betöltött %d motívum-ID fejsorát fedi.' % n_betoltott

    sorok = []
    for m in sorted(motivumok, key=lambda r: r['id']):
        sorai = elof_id_szerint.get(m['id'], [])
        n_fo = len(fo_elofordulas_csoportok(sorai))
        sorok.append('**%s** `[ID: %s]` — %s (%s, %s), %s fő előfordulás.'
                      % (m['cim'], m['id'], m['statusz'], m['statusz_verzio'],
                         m['statusz_datum'], n_fo))
        sorok.append('*(a bekezdés-próza a G2 után a `motivumok/%s.md`-ből fűződik ide)*'
                      % m['id'])
        sorok.append('')

    return blokk('naplo#kuszob', ['adat/motivumok.tsv', 'adat/elofordulasok.tsv'],
                  hatokor, '\n'.join(sorok).strip())


def render_naplo_kulcsszo_index(motivumok, elof_id_szerint, konyv_sorrend, hianyzo_konyvek):
    n_betoltott = len(motivumok)
    hatokor = ('Ez a blokk a táblában betöltött %d motívum-ID kulcsszó-sorát fedi; '
                'a ⭐ küszöb (3+ előfordulás) kizárólag a fő előfordulás oszlopot nézi. '
                'Az Igehelyek oszlop a fő előfordulásokat hozza, nem a teljes listát '
                '(K14) -- a teljes lista a könyv-indexben áll.' % n_betoltott)

    fejlec = '| Kulcsszó | Téma | ÓSZ/ÚSZ | Fő előfordulás | Igehelyek |'
    elvalaszto = '|---|---|---|---|---|'
    sorok = [fejlec, elvalaszto]
    for m in sorted(motivumok, key=lambda r: r['id']):
        sorai = elof_id_szerint.get(m['id'], [])
        csoportok = fo_elofordulas_csoportok(sorai)
        tokenek = {konyv_teszamentum(konyv_token(s['igehely'])) for s in sorai}
        if tokenek == {'ÓSZ'}:
            irany = 'ÓSZ'
        elif tokenek == {'ÚSZ'}:
            irany = 'ÚSZ'
        else:
            irany = 'ÓSZ+ÚSZ'
        csoportok_rendezve = sorted(
            csoportok, key=lambda cs: igehely_rendezo_kulcs(cs, konyv_sorrend, hianyzo_konyvek))
        igehelyek = ', '.join(csoportok_rendezve)
        sorok.append('| %s `[ID: %s]` | %s | %s | %d | %s |'
                      % (m['ui_cimke'], m['id'], m.get('tema') or '—', irany,
                         len(csoportok), igehelyek))

    return blokk('naplo#kulcsszo_index', ['adat/motivumok.tsv', 'adat/elofordulasok.tsv'],
                  hatokor, '\n'.join(sorok))


def render_naplo_konyv_index(elofordulasok, konyv_sorrend, hianyzo_konyvek):
    hatokor = ('Ez a blokk az elofordulasok.tsv mind a %d sorát könyv szerint bontja, '
                'a táblában betöltött motívum-ID-kre korlátozva; a könyvek és az '
                'igehelyek kanonikus sorrendben állnak (K13).' % len(elofordulasok))

    konyv_szerint = {}
    for sor in elofordulasok:
        token = konyv_token(sor['igehely'])
        konyv_szerint.setdefault(token, []).append(sor)

    def konyv_rendezo(token):
        return (konyv_sorszam(token, konyv_sorrend, hianyzo_konyvek), token)

    sorok = ['| Könyv | Igehely-sor | Tételek |', '|---|---|---|']
    for token in sorted(konyv_szerint, key=konyv_rendezo):
        tetelek = sorted(
            konyv_szerint[token],
            key=lambda s: igehely_rendezo_kulcs(s['igehely'], konyv_sorrend, hianyzo_konyvek))
        lista = ', '.join('%s [%s]' % (s['igehely'], s['id']) for s in tetelek)
        sorok.append('| %s | %d | %s |' % (token, len(tetelek), lista))

    return blokk('naplo#konyv_index', ['adat/elofordulasok.tsv'], hatokor, '\n'.join(sorok))


def general_naplo_blokkok(motivumok, elofordulasok, naplo_szoveg,
                           konyv_sorrend, hianyzo_konyvek):
    """[(cel_kulcs, blokk_szoveg)] -- a napló négy generált blokkja, az
    élesítéshez (G7) és a próba-kimenethez egyaránt ebből épül a fájl."""
    elof_id_szerint = elofordulasok_id_szerint(elofordulasok)
    return [
        ('naplo#attekintes',
         render_naplo_attekintes(motivumok, elof_id_szerint, naplo_szoveg)),
        ('naplo#kuszob',
         render_naplo_kuszob(motivumok, elof_id_szerint)),
        ('naplo#kulcsszo_index',
         render_naplo_kulcsszo_index(motivumok, elof_id_szerint, konyv_sorrend,
                                      hianyzo_konyvek)),
        ('naplo#konyv_index',
         render_naplo_konyv_index(elofordulasok, konyv_sorrend, hianyzo_konyvek)),
    ]


def general_naplo(motivumok, elofordulasok, naplo_szoveg, konyv_sorrend, hianyzo_konyvek):
    blokkok = [b for _, b in general_naplo_blokkok(
        motivumok, elofordulasok, naplo_szoveg, konyv_sorrend, hianyzo_konyvek)]
    fejl = fejlec_stampel('naplo', ['adat/motivumok.tsv', 'adat/elofordulasok.tsv'])
    return fejl + '\n\n' + '\n\n---\n\n'.join(blokkok) + '\n'


# ---------------------------------------------------------------------------
# G4 -- Lezárt tematikus tanulmányok index
# ---------------------------------------------------------------------------

def naplo_zart_id_lista(naplo_szoveg):
    """[ID: XXX-NNN] tokenek, amelyek ugyanabban a SORBAN '✅' ÉS 'LEZÁRVA'
    szót viselnek -- ugyanaz az elsődleges ellenőrzési módszer, amit a
    Lezart_tematikus_tanulmanyok_index.md karbantartási szabálya leír
    ('grep -n "✅.*LEZÁRVA"'), sor-szinten (nem bekezdés-szinten -- a
    Kulcsszó-index egyetlen, blank-line nélküli markdown-táblázat-bekezdés,
    ahol bekezdés-szintű keresés minden benne szereplő ID-t hamisan
    "zártnak" jelölne)."""
    talalt = set()
    for sor in marker_blokkok_nelkul(naplo_szoveg).split('\n'):
        if '✅' in sor and 'LEZÁRVA' in sor:
            for m in re.finditer(r'\[ID:\s*([A-ZÁÉÍÓÖŐÚÜŰ]+-\d+)\]', sor):
                talalt.add(m.group(1))
    return talalt


def render_index(motivumok, elofordulasok, naplo_szoveg, konyv_sorrend, hianyzo_konyvek):
    elof_id_szerint = elofordulasok_id_szerint(elofordulasok)
    lezart_szurt = [m for m in motivumok if m.get('statusz') != 'feldolgozás alatt']
    n_betoltott = len(lezart_szurt)

    zart_a_naploban = naplo_zart_id_lista(naplo_szoveg)
    tablaban_levo_id = {m['id'] for m in motivumok}
    hianyzo = sorted(zart_a_naploban - tablaban_levo_id)

    hatokor = ('Ez a blokk a táblában publikálható/véglegesített %d motívum-ID-t fedi; '
                'a Megjegyzés oszlop nem generálható (l. G2), a marker-blokkon kívül marad.'
                % n_betoltott)

    sorok = ['| # | Motívum | Fájlnév | Érintett igehelyek |', '|---|---|---|---|']
    for i, m in enumerate(sorted(lezart_szurt, key=lambda r: r['id']), start=1):
        sorai = elof_id_szerint.get(m['id'], [])
        csoportok = sorted(
            fo_elofordulas_csoportok(sorai),
            key=lambda cs: igehely_rendezo_kulcs(cs, konyv_sorrend, hianyzo_konyvek))
        erintett = ('%s (%d fő előfordulás / %d igehely-sor)'
                     % (' → '.join(csoportok) if csoportok else '—', len(csoportok), len(sorai)))
        sorok.append('| %d | %s `[ID: %s]` | %s | %s |'
                      % (i, m['cim'], m['id'], m.get('forras_study') or '—', erintett))

    torzs = '\n'.join(sorok)
    if hianyzo:
        torzs += ('\n\n⚠️ **HIÁNYZÓ TÉTEL** -- a napló a következő ID(k)et "✅ ... LEZÁRVA" '
                   'jelöléssel dokumentálja, de a `adat/motivumok.tsv` nem tartalmazza őket: '
                   '%s. (K8 -- ez nem generálási hiba, hanem az F3 betöltés hatókörének '
                   'hiánya; l. F4_GENERATOR_BRIEF.md §5.)' % ', '.join(hianyzo))

    blk = blokk('index', ['adat/motivumok.tsv', 'adat/elofordulasok.tsv'], hatokor, torzs)
    return blk, hianyzo


def general_index(motivumok, elofordulasok, naplo_szoveg, konyv_sorrend, hianyzo_konyvek):
    """(fajl_tartalom, [(cel_kulcs, blokk)], hianyzo) -- a próba-kimenethez a
    teljes fájl, az élesítéshez a blokk-lista."""
    blk, hianyzo = render_index(motivumok, elofordulasok, naplo_szoveg,
                                 konyv_sorrend, hianyzo_konyvek)
    fejl = fejlec_stampel('index', ['adat/motivumok.tsv', 'adat/elofordulasok.tsv'])
    return fejl + '\n\n' + blk + '\n', [('index', blk)], hianyzo


# ---------------------------------------------------------------------------
# G6 -- NYITOTT_FELADATOK.md: a nyitott jelöltek és a motívum-státuszok
# ---------------------------------------------------------------------------
#
# A fájl túlnyomó része kézzel írt, hosszú prózájú feladatlista, és az is
# marad: EGYETLEN blokk generálódik, marker közé (brief G7). A blokk azt a két
# listát fedi, amely ma is a táblából olvasható ki, de a fájlban nem szerepel
# -- a `jeloltek.tsv` `dontes=nyitva` sorait (ezek a 2. szabály szerinti,
# döntésre váró jelöltek) és a `motivumok.tsv` státusz-oszlopát.

def cella(ertek):
    """Markdown-tábla cella: a `|` elhatárolna egy oszlopot, a sortörés
    szétvágná a sort -- mindkettő escape-elendő. Üres mező `—`."""
    sz = (ertek or '').strip()
    if not sz:
        return '—'
    return sz.replace('|', '\\|').replace('\n', ' ')


def render_nyitott(motivumok, elofordulasok, jeloltek, konyv_sorrend, hianyzo_konyvek):
    nyitott = [j for j in jeloltek if j.get('dontes') == 'nyitva']
    n_be = sum(1 for j in jeloltek if j.get('dontes') == 'beépítve')
    n_el = sum(1 for j in jeloltek if j.get('dontes') == 'elutasítva')
    erintett_id = sorted({j['id'] for j in nyitott})

    hatokor = ('Ez a blokk a `jeloltek.tsv` %d nyitott (`dontes=nyitva`) sorát fedi '
                '%d motívum-ID-ről, és a `motivumok.tsv` %d státusz-sorát. A %d '
                'beépítve és %d elutasítva döntésű jelölt nem tartozik ide. A fájl '
                'minden más szakasza kézi, a marker-blokkon kívül marad.'
                % (len(nyitott), len(erintett_id), len(motivumok), n_be, n_el))

    sorok = ['### Nyitott jelöltek (`adat/jeloltek.tsv`, `dontes=nyitva`)', '']
    if nyitott:
        sorok.append('| # | Motívum-ID | Igehely | Forrás-keresés | Indoklás | Dátum |')
        sorok.append('|---|---|---|---|---|---|')
        rendezett = sorted(
            nyitott,
            key=lambda j: (j['id'],
                           igehely_rendezo_kulcs(j.get('igehely', ''),
                                                  konyv_sorrend, hianyzo_konyvek)))
        for i, j in enumerate(rendezett, start=1):
            sorok.append('| %d | `[ID: %s]` | %s | %s | %s | %s |'
                          % (i, j['id'], cella(j.get('igehely')),
                             cella(j.get('forras_kereses')), cella(j.get('indoklas')),
                             cella(j.get('datum'))))
    else:
        sorok.append('*Nincs nyitott jelölt a táblában.*')

    elof_id_szerint = elofordulasok_id_szerint(elofordulasok)
    sorok.append('')
    sorok.append('### Motívum-státuszok (`adat/motivumok.tsv`)')
    sorok.append('')
    sorok.append('| Motívum | Státusz | Verzió | Státusz dátuma | Fő előfordulás | '
                  'Nyitott jelölt | Forrás-study |')
    sorok.append('|---|---|---|---|---|---|---|')
    nyitott_darab = {}
    for j in nyitott:
        nyitott_darab[j['id']] = nyitott_darab.get(j['id'], 0) + 1
    for m in sorted(motivumok, key=lambda r: r['id']):
        sorai = elof_id_szerint.get(m['id'], [])
        n_fo = len(fo_elofordulas_csoportok(sorai))
        sorok.append('| %s `[ID: %s]` | %s | %s | %s | %d fő / %d sor | %d | %s |'
                      % (cella(m.get('cim')), m['id'], cella(m.get('statusz')),
                         cella(m.get('statusz_verzio')), cella(m.get('statusz_datum')),
                         n_fo, len(sorai), nyitott_darab.get(m['id'], 0),
                         cella(m.get('forras_study'))))

    return blokk('nyitott',
                  ['adat/jeloltek.tsv', 'adat/motivumok.tsv', 'adat/elofordulasok.tsv'],
                  hatokor, '\n'.join(sorok))


def general_nyitott(motivumok, elofordulasok, jeloltek, konyv_sorrend, hianyzo_konyvek):
    """(fajl_tartalom, [(cel_kulcs, blokk)]) -- a próba-kimenethez a teljes
    fájl, az élesítéshez a blokk-lista."""
    blk = render_nyitott(motivumok, elofordulasok, jeloltek,
                          konyv_sorrend, hianyzo_konyvek)
    fejl = fejlec_stampel('nyitott', ['adat/jeloltek.tsv', 'adat/motivumok.tsv'])
    return fejl + '\n\n' + blk + '\n', [('nyitott', blk)]


# ---------------------------------------------------------------------------
# G5 -- kereszthivatkozás-naplók + a hiánylista (K9)
# ---------------------------------------------------------------------------

def jeloltek_id_szerint(jeloltek):
    csoport = {}
    for sor in jeloltek:
        csoport.setdefault(sor['id'], []).append(sor)
    return csoport


def render_naplo_egy_id(m, jeloltek_id, elof_id, konyv_sorrend, hianyzo_konyvek):
    """A sablon szerkezete (4_PaRDeS_tematikus_sablon.md, 'Kötelező napló'):
    vizsgált kulcsszavak -> nyers találatok forrásonként -> tartalmi
    minősítés MINDEN jelöltre -> végső döntés és indoklás -> összegzés.
    A vizsgált kulcsszavak Strong-listája és a named-teacher gap-jelzés a
    jeloltek.tsv-ből nem vezethető le (l. brief G5) -- ez itt explicit
    jelölve, nem hallgatva el."""
    gerinc_elemek = sorted({s['gerinc_elem'] for s in elof_id if s.get('gerinc_elem')})

    forrasok = {}
    for j in jeloltek_id:
        forrasok.setdefault(j['forras_kereses'], []).append(j)

    sorok = []
    sorok.append('## Vizsgált kulcsszavak (részleges, a `gerinc_elem` mezőből -- Strong-lista nem vezethető le a `jeloltek.tsv`-ből)')
    sorok.append(', '.join('`%s`' % g for g in gerinc_elemek) if gerinc_elemek else '(nincs gerinc_elem rögzítve)')
    sorok.append('')
    sorok.append('## Nyers találatok forrásonként')
    for forras in sorted(forrasok):
        sorok.append('- **%s** — %d jelölt' % (forras, len(forrasok[forras])))
    sorok.append('')
    sorok.append('## Tartalmi minősítés minden jelöltre')
    sorok.append('| Igehely | Forrás | Döntés | Indoklás | Dátum |')
    sorok.append('|---|---|---|---|---|')
    jeloltek_rendezve = sorted(
        jeloltek_id, key=lambda r: igehely_rendezo_kulcs(r['igehely'], konyv_sorrend, hianyzo_konyvek))
    for j in jeloltek_rendezve:
        sorok.append('| %s | %s | %s | %s | %s |'
                      % (j['igehely'], j['forras_kereses'], j['dontes'], j['indoklas'], j['datum']))
    sorok.append('')

    n = len(jeloltek_id)
    n_be = sum(1 for j in jeloltek_id if j['dontes'] == 'beépítve')
    n_el = sum(1 for j in jeloltek_id if j['dontes'] == 'elutasítva')
    n_ny = sum(1 for j in jeloltek_id if j['dontes'] == 'nyitva')
    sorok.append('## Végső döntés és összegzés')
    sorok.append('%d jelölt vizsgálva a `jeloltek.tsv`-ben; %d beépítve, %d elutasítva, %d nyitva.'
                  % (n, n_be, n_el, n_ny))
    sorok.append('')
    sorok.append('*Named-teacher gap-jelzés és a vizsgált kulcsszavak teljes Strong-listája a '
                  'forrásrétegben (`motivumok/%s.md`, G2) él -- innen nem vezethető le '
                  '(F4_GENERATOR_BRIEF.md G5).*' % m['id'])

    fejsor = '# %s -- kereszthivatkozás-napló `[ID: %s]` (generált)' % (m['cim'], m['id'])
    hatokor = ('Ez a blokk a `jeloltek.tsv` %d sorát fedi a `[ID: %s]` motívumhoz; a vizsgált '
                'kulcsszavak Strong-listája és a named-teacher gap-jelzés nem generálható, '
                'a forrásrétegben él (G2).' % (n, m['id']))
    return blokk('naplok --id %s' % m['id'], ['adat/jeloltek.tsv', 'adat/elofordulasok.tsv'],
                  hatokor, fejsor + '\n\n' + '\n'.join(sorok))


def naplo_hianylista_sorok(jeloltek):
    """G5 kötelező melléktermék (K9): a tematikus_lezart/naplok/ alatti hét
    meglévő napló minősítő táblázatainak ❌-sorai, amelyek NINCSENEK a
    jeloltek.tsv-ben. A táblázat-cella szerkezete a hét fájlban nem
    egységes (3 vagy 4 oszlop) -- ezért a döntés-cellát tartalom szerint
    (a '❌'-lal kezdődő cella), nem pozíció szerint azonosítja."""
    jel_id_szerint = jeloltek_id_szerint(jeloltek)
    sorok = []
    for fajlnev in sorted(NAPLO_ID_TERKEP):
        azon = NAPLO_ID_TERKEP[fajlnev]
        path = os.path.join(NAPLOK_DIR, fajlnev)
        if not os.path.exists(path):
            continue
        szoveg = szoveg_beolvas(path)
        meglevo_elutasitott = {j['igehely'] for j in jel_id_szerint.get(azon, [])
                                if j['dontes'] == 'elutasítva'}
        for sor in szoveg.split('\n'):
            sor = sor.strip()
            if not sor.startswith('|') or '❌' not in sor:
                continue
            cellak = [c.strip() for c in sor.strip('|').split('|')]
            if len(cellak) < 3:
                continue
            dontes_cella = next((c for c in cellak if c.startswith('❌')), None)
            if dontes_cella is None:
                continue
            jelolt = cellak[0]
            indoklas = cellak[-1]
            if jelolt in meglevo_elutasitott:
                continue
            teljes_lc = ' '.join(cellak).lower()
            if 'gap' in teljes_lc:
                tipus = 'gap'
            elif 'elhatárol' in teljes_lc:
                tipus = 'elhatarolas'
            else:
                tipus = 'elutasitva'
            sorok.append({
                'id': azon,
                'jelolt': jelolt,
                'tipus': tipus,
                'forras_naplo': 'tematikus_lezart/naplok/' + fajlnev,
                'indoklas': indoklas,
            })
    return sorok


# K9': a HAMART-001-nek egyetlen sora sincs a jeloltek.tsv-ben -- a teljes ID
# hianyzik a tablabol (ismert F3-betoltesi hiany). Az o "hianyai" ezert nem
# 32 onallo lelet, hanem egyetlen ismert hiany kovetkezmenye; a hat betoltott
# ID tenyleges hianyaitol kulon blokkban allnak, hogy a szam ne fusson ossze.
K9_KULON_BLOKK_ID = 'HAMART-001'


def hianylista_blokkok(sorok, jeloltek):
    """(betoltott_sorok, kulon_sorok) -- a K9' ketteosztas. A besorolas nem
    beegetett ID-lista: az kerul a kulon blokkba, amelynek EGYETLEN sora sincs
    a jeloltek.tsv-ben (tehat a teljes ID hianyzik), es amely a
    K9_KULON_BLOKK_ID."""
    jel_id_szerint = jeloltek_id_szerint(jeloltek)
    kulon = [s for s in sorok
             if s['id'] == K9_KULON_BLOKK_ID and not jel_id_szerint.get(s['id'])]
    kulon_id = {s['id'] for s in kulon}
    betoltott = [s for s in sorok if s['id'] not in kulon_id]
    return betoltott, kulon


def hianylista_tsv_szoveg(betoltott, kulon):
    """A ket blokk egyetlen TSV-ben, lathato blokkhatarral. A '#' elotetsorokat
    a tsv_beolvas() kihagyja, tehat a fajl gepileg tovabbra is egy tabla."""
    fejlec = ['id', 'jelolt', 'tipus', 'forras_naplo', 'indoklas']

    def adatsorok(lista):
        return ['\t'.join(s[m].replace('\t', ' ') for m in fejlec) for s in lista]

    kulon_id = sorted({s['id'] for s in kulon})
    ki = []
    ki.append('# F4 napló-hiánylista (K9/K9\') -- KÉT BLOKK, l. F4_GENERATOR_BRIEF.md 3. pont')
    ki.append('# 1. blokk: a betöltött motívum-ID-k TÉNYLEGES hiányai (%d sor) -- '
              'ezek a naplókban ❌-szal minősített jelöltek, amelyek nincsenek a '
              'jeloltek.tsv-ben.' % len(betoltott))
    ki.append('# 2. blokk: %s (%d sor) -- EGYETLEN ismert F3-hiány következménye, '
              'nem %d önálló lelet: ennek az ID-nek egyetlen sora sincs a '
              'jeloltek.tsv-ben, mert maga az ID nincs betöltve.'
              % (', '.join(kulon_id) or '(üres)', len(kulon), len(kulon)))
    ki.append('#')
    ki.append('\t'.join(fejlec))
    ki.append('# --- 1. BLOKK: betöltött ID-k tényleges hiányai (%d sor) ---' % len(betoltott))
    ki.extend(adatsorok(betoltott))
    ki.append('# --- 2. BLOKK: %s -- ismert F3-betöltési hiány következménye (%d sor) ---'
              % (', '.join(kulon_id) or '(üres)', len(kulon)))
    ki.extend(adatsorok(kulon))
    return '\n'.join(ki) + '\n'


# ---------------------------------------------------------------------------
# G6 -- tematikus study 1. pont (hétoszlopos táblázat)
# ---------------------------------------------------------------------------

def studytabla_pardes_oszlop(sor):
    """A harmadik oszlop -- pardes_szint + felmerult_tanulmany összefűzése.
    Ahol a felmerult_tanulmany üres, csak a szint áll ott -- nem pótolható
    találgatással (F4_GENERATOR_BRIEF.md G6)."""
    szint = sor.get('pardes_szint') or ''
    felmerult = sor.get('felmerult_tanulmany') or ''
    if szint and felmerult:
        return '%s — %s' % (szint, felmerult)
    return szint or felmerult or '—'


def studytabla_jelentes_oszlop(sor):
    en = sor.get('jelentes_en') or ''
    hu = sor.get('jelentes_hu') or ''
    if en and hu:
        return '"%s" — magyarul: "%s"' % (en, hu)
    if en:
        return '"%s"' % en
    if hu:
        return 'magyarul: "%s"' % hu
    return '—'


def render_study_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek):
    sorai_rendezve = sorted(
        sorai, key=lambda s: igehely_rendezo_kulcs(s['igehely'], konyv_sorrend, hianyzo_konyvek))
    hatokor = ('Ez a blokk a `[ID: %s]` motívum %d igehely-sorát fedi az `elofordulasok.tsv`-ből, '
                'kanonikus sorrendben (K13); a hiányzó BDB-mezők helyén "—" áll.'
                % (m['id'], len(sorai_rendezve)))
    sorok = ['| Igehely | Kapcsolódás | PaRDeS-szint, ahol felmerült | Strong-szám(ok) | '
             'BDB-entry-id | Sense-szám | Jelentés-szöveg (EN + HU) |',
             '|---|---|---|---|---|---|---|']
    for s in sorai_rendezve:
        bdb_cella = s.get('lexikon_entry_id') or '—' if s.get('lexikon_szotar') == 'BDB' else '—'
        sorok.append('| %s | %s | %s | %s | %s | %s | %s |' % (
            s['igehely'], s['kapcsolodas'], studytabla_pardes_oszlop(s),
            s.get('strong') or '—', bdb_cella,
            s.get('jelentes_szam') or '—', studytabla_jelentes_oszlop(s)))
    return blokk('study --id %s' % m['id'], ['adat/elofordulasok.tsv'], hatokor, '\n'.join(sorok))


# ---------------------------------------------------------------------------
# Kimenet-írás
# ---------------------------------------------------------------------------

def kimenet_ir(args, relativ_ut, tartalom, forras_ut_a_sorveghez):
    domináns, crlf, lf = sorveg_elemez(forras_ut_a_sorveghez)
    print('  sorvég a célfájlban (%s): CRLF=%d, LF=%d -> domináns=%r'
          % (os.path.relpath(forras_ut_a_sorveghez, ROOT), crlf, lf, domináns))

    cel_ut = os.path.join(args.kimenet, relativ_ut)
    if args.ellenoriz:
        print('  --ellenoriz: nincs írás (K az első futásnál pirosnak számít, l. §3.1).')
        return cel_ut

    os.makedirs(os.path.dirname(cel_ut), exist_ok=True)
    sorok = tartalom.split('\n')
    with io.open(cel_ut, 'w', encoding='utf-8', newline='') as f:
        f.write(domináns.join(sorok))
    print('  megírva: %s (%d bájt)' % (os.path.relpath(cel_ut, ROOT), os.path.getsize(cel_ut)))
    return cel_ut


def hianylista_ir(args, sorok, jeloltek):
    """A K9 melléktermék írása -- LF-es (a .gitattributes szerint minden
    *.tsv LF-es), nem a célfájl-sorvég-megtartó kimenet_ir() útján, mert ez
    egy ÚJ artefaktum, nincs neki 'mai' célfájlja."""
    betoltott, kulon = hianylista_blokkok(sorok, jeloltek)
    tartalom = hianylista_tsv_szoveg(betoltott, kulon)
    cel_ut = os.path.join(args.kimenet, 'naplok', 'F4_naplo_hianylista.tsv')
    print('  hiánylista (K9\'): %d sor = 1. blokk %d (betöltött ID-k tényleges hiányai) '
          '+ 2. blokk %d (%s -- egyetlen ismert F3-hiány következménye)'
          % (len(sorok), len(betoltott), len(kulon), K9_KULON_BLOKK_ID))
    if args.ellenoriz:
        print('  --ellenoriz: nincs írás.')
        return cel_ut
    os.makedirs(os.path.dirname(cel_ut), exist_ok=True)
    with io.open(cel_ut, 'w', encoding='utf-8', newline='') as f:
        f.write(tartalom)
    print('  megírva: %s (%d bájt)' % (os.path.relpath(cel_ut, ROOT), os.path.getsize(cel_ut)))
    return cel_ut


# ---------------------------------------------------------------------------
# G7 -- élesítés és ellenőrzés az ÉLES fájlokon
# ---------------------------------------------------------------------------
#
# Horgony: az a SOR az éles fájlban, amely UTÁN a blokk első beszúrása
# történik. Ha a marker-pár már ott van, a horgonyra nincs szükség -- akkor a
# törzs cserélődik, és a blokkon kívüli kézi tartalom érintetlen marad.

HORGONY = {
    'naplo#attekintes': '## Tematikus áttekintés',
    'naplo#kuszob': '## ⭐ Emlékeztető küszöb (3+ előfordulás)',
    'naplo#kulcsszo_index': '## Kulcsszó-index',
    'naplo#konyv_index': '## Könyv szerinti index',
    'index': '<!-- A GENERÁLT BLOKK HELYE: index -->',
    'nyitott': '<!-- A GENERÁLT BLOKK HELYE: nyitott -->',
}


def eles_fajl_beolvas(path):
    """(LF-re normalizált szöveg, domináns sorvég) -- a repó core.autocrlf=true,
    és a .gitattributes csak a *.tsv-t köti LF-hez, tehát a .md munkapéldány
    sorvége checkoutonként változhat. A visszaírás a fájl saját sorvégével
    történik (K7)."""
    with io.open(path, encoding='utf-8', newline='') as f:
        nyers = f.read()
    crlf = nyers.count('\r\n')
    lf = nyers.count('\n') - crlf
    return nyers.replace('\r\n', '\n'), ('\r\n' if crlf > lf else '\n'), crlf, lf


def eles_fajl_ir(path, szoveg_lf, sorveg):
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(sorveg.join(szoveg_lf.split('\n')))


def blokkok_ellenoriz(path, blokkok):
    """[(cel_kulcs, allapot)] -- allapot: 'zöld' | 'eltér' | 'hiányzik'."""
    szoveg, _, _, _ = eles_fajl_beolvas(path)
    eredmeny = []
    for cel_kulcs, blk in blokkok:
        talalat = marker_par_keres(szoveg, cel_kulcs)
        if not talalat:
            eredmeny.append((cel_kulcs, 'hiányzik'))
            continue
        _, tk, tv, _ = talalat
        eredmeny.append((cel_kulcs,
                          'zöld' if szoveg[tk:tv] == blokk_torzs(blk, cel_kulcs) else 'eltér'))
    return eredmeny


def build_parser():
    p = argparse.ArgumentParser(
        prog='general.py',
        description='A motivumlexikon generatorai -- F4_GENERATOR_BRIEF.md.',
    )
    p.add_argument('--cel', required=True,
                    choices=['naplo', 'index', 'naplok', 'study', 'nyitott', 'lexikon', 'mind'])
    p.add_argument('--id', help='egyetlen motívum-ID-re szűkítés (opcionális)')
    p.add_argument('--kimenet', default=os.path.join(ROOT, 'generalt_proba'),
                    help='alapértelmezés: generalt_proba/')
    p.add_argument('--ir', action='store_true',
                    help='ÉLESÍTÉS (G7): a marker-blokkokat az ÉLES fájlba írja. '
                         'Nélküle a szkript soha nem ír éles fájlba, csak a '
                         '--kimenet könyvtár alá. Csak a naplo és az index cél '
                         'élesíthető; a study-fájlok nem (brief G7).')
    p.add_argument('--ellenoriz', action='store_true',
                    help='nem ír; a generált blokkot az ÉLES fájlban álló marker-blokk '
                         'törzsével veti össze, eltérésnél/hiánynál 1-gyel lép ki')
    return p


ELESITHETO = {'naplo', 'index', 'nyitott'}

CEL_FAJL = {'naplo': NAPLO_MD, 'index': INDEX_MD, 'nyitott': NYITOTT_MD}


MEG_NEM_KESZ = {}


def blokk_lista_eles(cel, motivumok, elofordulasok, konyv_sorrend, hianyzo_konyvek):
    """A cél élesíthető blokkjai, MINDIG az éles fájl aktuális szövegéből
    számolva (a naplo#attekintes hatóköre a napló saját kézi listáját méri)."""
    if cel == 'naplo':
        naplo_szoveg = szoveg_beolvas(NAPLO_MD)
        return general_naplo_blokkok(motivumok, elofordulasok, naplo_szoveg,
                                      konyv_sorrend, hianyzo_konyvek), None
    if cel == 'nyitott':
        _, jeloltek = tsv_beolvas(JELOLTEK_TSV)
        _, blokkok = general_nyitott(motivumok, elofordulasok, jeloltek,
                                      konyv_sorrend, hianyzo_konyvek)
        return blokkok, None
    naplo_szoveg = szoveg_beolvas(NAPLO_MD)
    _, blokkok, hianyzo = general_index(motivumok, elofordulasok, naplo_szoveg,
                                         konyv_sorrend, hianyzo_konyvek)
    return blokkok, hianyzo


def elesites(cel, path, motivumok, elofordulasok, konyv_sorrend, hianyzo_konyvek,
             max_iteracio=6):
    """A marker-blokkok beírása/frissítése az ÉLES fájlba, FIXPONTIG.

    Miért iteráció: a naplo#attekintes hatókör-sora a napló saját, blokkon
    KÍVÜLI kézi listáját számolja, tehát az első beírás után a szám
    megváltozik. A marker_blokkok_nelkul() kiveszi a generált blokkokat a
    számlálásból, ezért a második kör után a szám már nem mozdul -- a ciklus
    ezt MÉRI (addig fut, amíg egyetlen blokk sem változik), nem feltételezi."""
    for kor in range(1, max_iteracio + 1):
        blokkok, _ = blokk_lista_eles(cel, motivumok, elofordulasok,
                                       konyv_sorrend, hianyzo_konyvek)
        szoveg, sorveg, crlf, lf = eles_fajl_beolvas(path)
        if kor == 1:
            print('  sorvég élesítés előtt (%s): CRLF=%d, LF=%d -> domináns=%r'
                  % (os.path.relpath(path, ROOT), crlf, lf, sorveg))
        valtozott = []
        for cel_kulcs, blk in blokkok:
            szoveg, mit = blokk_beilleszt(szoveg, cel_kulcs, blk, HORGONY.get(cel_kulcs))
            if mit != 'változatlan':
                valtozott.append((cel_kulcs, mit))
        if valtozott:
            eles_fajl_ir(path, szoveg, sorveg)
        print('  %d. kör: %s' % (kor, ', '.join('%s=%s' % t for t in valtozott)
                                  if valtozott else 'nincs változás (fixpont)'))
        if not valtozott:
            return kor
    raise SystemExit('MEGALLAS: az élesítés %d kör alatt sem ért fixpontot (%s).'
                     % (max_iteracio, cel))


def main():
    args = build_parser().parse_args()

    if args.ir and args.cel not in ELESITHETO and args.cel != 'mind':
        print('FIGYELEM: a(z) %r cél NEM élesíthető (brief G7) -- a kimenet a '
              '--kimenet könyvtár alá megy.' % args.cel, file=sys.stderr)

    celok = ['naplo', 'index', 'naplok', 'study', 'nyitott'] \
        if args.cel == 'mind' else [args.cel]
    vegso_kod = 0
    konyv_sorrend = konyv_sorrend_betolt()
    hianyzo_konyvek = set()

    for cel in celok:
        if cel in MEG_NEM_KESZ:
            print('%s: %s' % (cel, MEG_NEM_KESZ[cel]), file=sys.stderr)
            vegso_kod = max(vegso_kod, 2)
            continue

        _, motivumok = tsv_beolvas(MOTIVUMOK_TSV)
        _, elofordulasok = tsv_beolvas(ELOFORDULASOK_TSV)
        if args.id:
            motivumok = [m for m in motivumok if m['id'] == args.id]
            elofordulasok = [s for s in elofordulasok if s['id'] == args.id]
        naplo_szoveg = szoveg_beolvas(NAPLO_MD)

        print('--- cél: %s ---' % cel)

        if cel in ELESITHETO and (args.ir or args.ellenoriz):
            path = CEL_FAJL[cel]
            blokkok, hianyzo = blokk_lista_eles(cel, motivumok, elofordulasok,
                                                  konyv_sorrend, hianyzo_konyvek)
            if args.ir:
                korok = elesites(cel, path, motivumok, elofordulasok,
                                  konyv_sorrend, hianyzo_konyvek)
                print('  élesítve: %s (%d kör, fixpont)' % (os.path.relpath(path, ROOT), korok))
                blokkok, hianyzo = blokk_lista_eles(cel, motivumok, elofordulasok,
                                                     konyv_sorrend, hianyzo_konyvek)
            print('  --ellenoriz (%s):' % os.path.relpath(path, ROOT))
            for cel_kulcs, allapot in blokkok_ellenoriz(path, blokkok):
                jel = '✓ ZÖLD' if allapot == 'zöld' else '✗ PIROS'
                print('    %-24s %s (%s)' % (cel_kulcs, jel, allapot))
                if allapot != 'zöld':
                    vegso_kod = max(vegso_kod, 1)
            if cel == 'index' and hianyzo:
                print('  HIÁNYZÓ ZÁRT ID (K8): %s' % ', '.join(hianyzo), file=sys.stderr)
                vegso_kod = max(vegso_kod, 1)
            continue

        if cel == 'naplo':
            tartalom = general_naplo(motivumok, elofordulasok, naplo_szoveg,
                                       konyv_sorrend, hianyzo_konyvek)
            kimenet_ir(args, os.path.join('motivumlog', 'PaRDeS_motivumok.md'),
                       tartalom, NAPLO_MD)

        elif cel == 'index':
            tartalom, _, hianyzo = general_index(motivumok, elofordulasok, naplo_szoveg,
                                                   konyv_sorrend, hianyzo_konyvek)
            kimenet_ir(args, 'Lezart_tematikus_tanulmanyok_index.md', tartalom, INDEX_MD)
            if hianyzo:
                print('  HIÁNYZÓ ZÁRT ID (K8): %s' % ', '.join(hianyzo), file=sys.stderr)
                if args.ellenoriz:
                    vegso_kod = 1

        elif cel == 'nyitott':
            _, jeloltek = tsv_beolvas(JELOLTEK_TSV)
            tartalom, _ = general_nyitott(motivumok, elofordulasok, jeloltek,
                                            konyv_sorrend, hianyzo_konyvek)
            kimenet_ir(args, 'NYITOTT_FELADATOK.md', tartalom, NYITOTT_MD)

        elif cel == 'naplok':
            _, jeloltek = tsv_beolvas(JELOLTEK_TSV)
            if args.id:
                jeloltek = [j for j in jeloltek if j['id'] == args.id]
            jel_id_szerint = jeloltek_id_szerint(jeloltek)
            elof_id_szerint = elofordulasok_id_szerint(elofordulasok)
            for m in motivumok:
                jelt = jel_id_szerint.get(m['id'], [])
                if not jelt:
                    continue
                blk = render_naplo_egy_id(m, jelt, elof_id_szerint.get(m['id'], []),
                                            konyv_sorrend, hianyzo_konyvek)
                fejl = fejlec_stampel('naplok --id %s' % m['id'], ['adat/jeloltek.tsv'])
                tartalom = fejl + '\n\n' + blk + '\n'
                celfajlnev = ID_NAPLO_TERKEP.get(m['id'])
                if celfajlnev:
                    relativ = os.path.join('tematikus_lezart', 'naplok', celfajlnev)
                    forras_ut = os.path.join(NAPLOK_DIR, celfajlnev)
                else:
                    relativ = os.path.join('tematikus_lezart', 'naplok',
                                             '%s_kereszthivatkozas_naplo_GENERALT.md' % m['id'])
                    forras_ut = NAPLO_MD
                kimenet_ir(args, relativ, tartalom, forras_ut)

            # K9 -- a hiánylista MINDIG a teljes (nem --id-szűkített) jeloltek.tsv-hez
            # képest készül, hogy a --id ne rejtse el a más ID-khez tartozó hiányt.
            _, jeloltek_teljes = tsv_beolvas(JELOLTEK_TSV)
            hianylista_sorok = naplo_hianylista_sorok(jeloltek_teljes)
            hianylista_ir(args, hianylista_sorok, jeloltek_teljes)

        elif cel == 'lexikon':
            import lexikon_general
            vegso_kod = max(vegso_kod, lexikon_general.run(
                args, motivumok, elofordulasok, konyv_sorrend, hianyzo_konyvek))

        elif cel == 'study':
            elof_id_szerint = elofordulasok_id_szerint(elofordulasok)
            for m in motivumok:
                sorai = elof_id_szerint.get(m['id'], [])
                if not sorai:
                    continue
                blk = render_study_egy_id(m, sorai, konyv_sorrend, hianyzo_konyvek)
                fejl = fejlec_stampel('study --id %s' % m['id'], ['adat/elofordulasok.tsv'])
                tartalom = fejl + '\n\n' + blk + '\n'
                elso_study = (m.get('forras_study') or '').split(';')[0].strip()
                forras_ut = os.path.join(ROOT, elso_study) if elso_study else ''
                if not elso_study or not os.path.exists(forras_ut):
                    forras_ut = NAPLO_MD
                alap = os.path.splitext(elso_study)[0] if elso_study else \
                    os.path.join('tematikus_lezart', m['id'])
                relativ = alap + '_1_pont_GENERALT.md'
                kimenet_ir(args, relativ, tartalom, forras_ut)

        if args.ellenoriz:
            # A naplok/study célok NEM élesíthetők ebben a fázisban (brief G7),
            # tehát nincs marker-pár, amihez a blokkot mérni lehetne.
            print('  --ellenoriz: a(z) %r cél nem élesíthető (G7), nincs mihez '
                  'mérni -- PIROS.' % cel)
            vegso_kod = max(vegso_kod, 1)

    if hianyzo_konyvek:
        print('  K13 -- a normalizáló táblában NEM található könyvnév(s): %s'
              % ', '.join(sorted(hianyzo_konyvek)), file=sys.stderr)
        vegso_kod = max(vegso_kod, 1)
    else:
        print('  K13/K15: minden könyvnév feloldva a normalizáló táblán, '
              'alias nélkül (a KONYV_ALIAS üres).')

    return vegso_kod


if __name__ == '__main__':
    sys.exit(main())
