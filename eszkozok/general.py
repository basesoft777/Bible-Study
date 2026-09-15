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
ala. A G5/G6 celok (naplok, study, nyitott) ebben a menetben (G1/G3/G4) meg
nincsenek megirva -- --cel-kent elfogadottak, de meg nem valositottak meg;
futtatasuk 2-es kilepesi koddal jelzi ezt, nem hamis sikerrel.

TSV-olvasas kizarolag split('\\t')-vel, iras '\\t'.join()-nal -- a `csv` modul
importja is tilos (CLAUDE.md, "TSV-olvasas" szakasz).

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
NAPLO_MD = os.path.join(ROOT, 'motivumlog', 'PaRDeS_motivumok.md')
INDEX_MD = os.path.join(ROOT, 'Lezart_tematikus_tanulmanyok_index.md')

TS = datetime.date.today().isoformat()

# A tablaban ma nem szereplo, de a naploban mar konyvkent hasznalt ujszovetsegi
# tokenek -- csak a ma ELOFORDULO alakok, nem az osszes bibliai konyv (l. a
# konyv_teszament() dokumentaciojat lent).
UJSZOVETSEGI_TOKENEK = {
    '1Kor', '1Pét', '1Thessz', '2Pét', '2Tim', 'ApCsel', 'Jelenések', 'Júd',
    'Luk', 'Lukács', 'Máté', 'Róm', 'Róma', 'Zsid',
}


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
    """A '## Tematikus áttekintés' szakasz top-szintű ('- ' kezdetű, nem
    '  - ↳' alpont) tételeinek száma -- a hatókör-sor 'a fájl további N tétele
    kézi' állítását ebből számolja, nem beégetett konstansból."""
    m = re.search(r'^## Tematikus áttekintés\n(.*?)\n## ', naplo_szoveg, re.S | re.M)
    if not m:
        return None
    szakasz = m.group(1)
    return sum(1 for sor in szakasz.split('\n') if re.match(r'^- ', sor))


def render_naplo_attekintes(motivumok, elof_id_szerint, naplo_szoveg):
    n_betoltott = len(motivumok)
    n_bullet = naplo_bullet_szamlalo(naplo_szoveg)
    if n_bullet is None:
        hatokor = 'Ez a blokk a táblában betöltött %d motívum-ID-t fedi.' % n_betoltott
    else:
        hatokor = ('Ez a blokk a táblában betöltött %d motívum-ID-t fedi; a napló '
                    'Tematikus áttekintés szakasza %d tételt sorol fel, ebből %d '
                    'még nincs a táblában.' % (n_betoltott, n_bullet, n_bullet - n_betoltott))

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


def render_naplo_kulcsszo_index(motivumok, elof_id_szerint):
    n_betoltott = len(motivumok)
    hatokor = ('Ez a blokk a táblában betöltött %d motívum-ID kulcsszó-sorát fedi; '
                'a ⭐ küszöb (3+ előfordulás) kizárólag a fő előfordulás oszlopot nézi.'
                % n_betoltott)

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
        igehelyek = ', '.join(s['igehely'] for s in sorai)
        sorok.append('| %s `[ID: %s]` | %s | %s | %d | %s |'
                      % (m['ui_cimke'], m['id'], m.get('tema') or '—', irany,
                         len(csoportok), igehelyek))

    return blokk('naplo#kulcsszo_index', ['adat/motivumok.tsv', 'adat/elofordulasok.tsv'],
                  hatokor, '\n'.join(sorok))


def render_naplo_konyv_index(elofordulasok):
    hatokor = ('Ez a blokk az elofordulasok.tsv mind a %d sorát könyv szerint bontja, '
                'a táblában betöltött motívum-ID-kre korlátozva.' % len(elofordulasok))

    konyv_szerint = {}
    for sor in elofordulasok:
        token = konyv_token(sor['igehely'])
        konyv_szerint.setdefault(token, []).append(sor)

    def rendezo_kulcs(token):
        return (konyv_teszamentum(token), token)

    sorok = ['| Könyv | Igehely-sor | Tételek |', '|---|---|---|']
    for token in sorted(konyv_szerint, key=rendezo_kulcs):
        tetelek = konyv_szerint[token]
        lista = ', '.join('%s [%s]' % (s['igehely'], s['id']) for s in tetelek)
        sorok.append('| %s | %d | %s |' % (token, len(tetelek), lista))

    return blokk('naplo#konyv_index', ['adat/elofordulasok.tsv'], hatokor, '\n'.join(sorok))


def general_naplo(motivumok, elofordulasok, naplo_szoveg):
    elof_id_szerint = elofordulasok_id_szerint(elofordulasok)
    blokkok = [
        render_naplo_attekintes(motivumok, elof_id_szerint, naplo_szoveg),
        render_naplo_kuszob(motivumok, elof_id_szerint),
        render_naplo_kulcsszo_index(motivumok, elof_id_szerint),
        render_naplo_konyv_index(elofordulasok),
    ]
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
    for sor in naplo_szoveg.split('\n'):
        if '✅' in sor and 'LEZÁRVA' in sor:
            for m in re.finditer(r'\[ID:\s*([A-ZÁÉÍÓÖŐÚÜŰ]+-\d+)\]', sor):
                talalt.add(m.group(1))
    return talalt


def render_index(motivumok, elofordulasok, naplo_szoveg):
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
        csoportok = fo_elofordulas_csoportok(sorai)
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
    fejl = fejlec_stampel('index', ['adat/motivumok.tsv', 'adat/elofordulasok.tsv'])
    return fejl + '\n\n' + blk + '\n', hianyzo


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


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(
        prog='general.py',
        description='A motivumlexikon generatorai -- F4_GENERATOR_BRIEF.md.',
    )
    p.add_argument('--cel', required=True,
                    choices=['naplo', 'index', 'naplok', 'study', 'nyitott', 'mind'])
    p.add_argument('--id', help='egyetlen motívum-ID-re szűkítés (opcionális)')
    p.add_argument('--kimenet', default=os.path.join(ROOT, 'generalt_proba'),
                    help='alapértelmezés: generalt_proba/')
    p.add_argument('--ir', action='store_true',
                    help='NÉLKÜLE a szkript soha nem ír éles fájlba -- ez a kapcsoló '
                         'ebben a fázisban (G1/G3/G4) még nem old fel semmit, mert az '
                         'élesítés G7 külön tétele')
    p.add_argument('--ellenoriz', action='store_true',
                    help='nem ír; a generált blokkot a célfájlban álló marker-blokkal '
                         'veti össze, eltérésnél/hiánynál 1-gyel lép ki')
    return p


MEG_NEM_KESZ = {
    'naplok': 'G5 -- a 2. menetben készül (kereszthivatkozás-napló renderelő).',
    'study': 'G6 -- a 2. menetben készül (tematikus study 1. pont renderelő).',
    'nyitott': 'G7 -- a 3. menetben készül (NYITOTT_FELADATOK.md blokk-generátor).',
}


def main():
    args = build_parser().parse_args()

    if args.ir:
        print('FIGYELEM: --ir kapcsoló ebben a fázisban (G1/G3/G4) nem old fel semmit -- '
              'az élesítés a G7 külön tétele, külön emberi jóváhagyással. A kimenet '
              'továbbra is a --kimenet könyvtár alá megy.', file=sys.stderr)

    celok = ['naplo', 'index'] if args.cel == 'mind' else [args.cel]
    vegso_kod = 0

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

        if cel == 'naplo':
            tartalom = general_naplo(motivumok, elofordulasok, naplo_szoveg)
            kimenet_ir(args, os.path.join('motivumlog', 'PaRDeS_motivumok.md'),
                       tartalom, NAPLO_MD)

        elif cel == 'index':
            tartalom, hianyzo = render_index(motivumok, elofordulasok, naplo_szoveg)
            kimenet_ir(args, 'Lezart_tematikus_tanulmanyok_index.md', tartalom, INDEX_MD)
            if hianyzo:
                print('  HIÁNYZÓ ZÁRT ID (K8): %s' % ', '.join(hianyzo), file=sys.stderr)
                if args.ellenoriz:
                    vegso_kod = 1

        if args.ellenoriz:
            # Az első futásnál minden blokk pirosnak számít -- még nincs
            # marker a célfájlokban (l. F4_GENERATOR_BRIEF.md §3.1).
            print('  --ellenoriz: a célfájlban még nincs marker-blokk -- PIROS.')
            vegso_kod = max(vegso_kod, 1)

    return vegso_kod


if __name__ == '__main__':
    sys.exit(main())
