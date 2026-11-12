#!/usr/bin/env python
"""szakasz_forditas.py — egy igeszakasz Strong-szavainak hiányzó szótári fordítása, egy kötegre előkészítve (F205 M4).

A tanulmány a szakasz minden szavát olvassa; a motívumcikk eddig utólag pótolta a hiányzó fordítást (F182, F31). Ez az
eszköz a tanulmány A2 lépése után (`MUNKAMENET.md` A2c) egyszerre megmondja, a szakasz mely Strongjának hiányzik érvényes
magyar szótári fordítása, és a hiányt a **meglévő** fordítóláncok bemenetének alakjában adja ki. Új fordítómotor nincs,
fordítás és API-hívás nem fut; a láncok saját őre (`forditas_vedelem.py`) érvényes sort nem fordít újra.

Lépések:
  1. a szakasz versei a Károli-kulcson (`TAHOT_kivonat.tsv` / `TAGNT_kivonat.tsv` `Igehely` = Károli-vers, CLAUDE.md
     „Adat-tár”; a fájlsorrendre nem támaszkodik, kulcs szerint olvas); a `+`-szal összevont Strong elemenként;
  2. a nyelvtani Strongok (`adat/grammatikai_strongok.tsv`) kimaradnak, a jelentés megszámolja őket;
  3. Strongonként a fordítás állapota az `adat/forditasok.tsv`-ből, láncanként:
       - **BDB-szakasz** (héber): a `bdb_szakaszok.tsv` szakaszai és a `szotar = BDB`, `sz<n>` sorok (a jóváhagyott `kezi`
         `teljes` sor elsőbbségével, DT290 (3); az összefűző: `bdb_jelolt/szakasz_bemenet.strong_magyar_sorok`);
       - **Thayer-szakasz** (görög): a `thayer_szakaszok.tsv` szakaszai és a `szotar = Thayer`, `sz<n>` sorok
         (`thayer_jelolt/szolista.allapot`, ugyanaz a szabály, mint az M3 szólistáé);
       - **TBESG-glossza** (görög): `szotar = TBESG`, `jelentes_szam = rovid`, `mezo = glosszak_hu`, a forrás a
         `glossza_lexikon_forditas.tovabbi_forras` (a 13. szabályé);
     érvényes = nem `elavult`, nem üres, és a `forras_hash` a mai forrásé. Állapot: `kesz` | `hianyzik` | `hianyos` |
     `elavult_hash` | `nincs_szakasz` / `nincs_forras` (a szótárban nincs mit fordítani; nem pótolt, kimondva);
  4. kimenet: jelentés (stdout) és — `--ki <mappa>`, a repón kívül — a láncok bemenete:
       `thayer_strongok.txt` (`thayer_api_koteg.py --strongok`), `glossza_lista.tsv` (`glossza_api_koteg.py --lista`),
       `bdb_strongok.txt` (a BDB-lánc adag-sorrendjébe kézzel kerül: a `bdb_api_koteg.py`-nak nincs Strong-listás
       bemenete; a másodlagos Strong a `BDB_strong_alias.tsv` szerinti szócikk-Strongként áll benne), és `becsles.tsv` (láncanként a fordítandó egységek és a forrás karakterszáma — száraz becslés).

  python eszkozok/szakasz_forditas.py --szakasz "1Móz 8:20-22" [--ki MAPPA] [--ts NAP]

TSV: split('\\t') / '\\t'.join, csv modul nélkül. A repóban fájlt nem ír.
"""
import argparse
import collections
import datetime
import hashlib
import os
import re
import sys

ITT = os.path.dirname(os.path.abspath(__file__))
for _d in (ITT, os.path.join(ITT, 'thayer_jelolt')):
    if _d not in sys.path:
        sys.path.insert(0, _d)
import kulcs  # noqa: E402  (thayer_jelolt)
import szolista  # noqa: E402  (thayer_jelolt)
import thayer_bemenet as TB  # noqa: E402  (thayer_jelolt)
import glossza_lexikon_forditas as GLF  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SB = TB.K                     # a bdb_jelolt/szakasz_bemenet modul (a thayer_bemenet saját néven tölti be)
GYOKER = os.path.dirname(ITT)
KONK = os.path.join(GYOKER, 'konkordancia')
ADAT = os.path.join(GYOKER, 'adat')
FORRAS = 'szakasz_forditas.py (fejléc)'

LANCOK = ('BDB', 'Thayer', 'TBESG')
GLOSSZA_FEJLEC = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash', 'allapot']
JELENTES_FEJLEC = ['strong', 'lanc', 'allapot', 'reszlet', 'karakter', 'versek', 'proveniencia']
BECSLES_FEJLEC = ['lanc', 'fordítandó_strong', 'fordítandó_egyseg', 'forras_karakter', 'bemenet', 'parancs']
SZAKASZ_RX = re.compile(r'^(?P<konyv>\S+)\s+(?P<c1>\d+)(?::(?P<v1>\d+))?(?:\s*[-–]\s*(?:(?P<c2>\d+):)?(?P<v2>\d+))?$')
IGEHELY_RX = re.compile(r'^(?P<konyv>\S+)\s+(?P<c>\d+):(?P<v>\d+)$')


# ---------------------------------------------------------------- beolvasás

def tsv_sorok(ut):
    """[(fejléc, sorok dict-ként)] — `#`-sorok nélkül; az első nem `#` sor a fejléc."""
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s.rstrip('\r') for s in f.read().split('\n')]
    sorok = [s for s in sorok if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return fej, [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def sha12(ut):
    h = hashlib.sha256()
    with open(ut, 'rb') as f:
        h.update(f.read())
    return h.hexdigest()[:12]


def szakasz_elemez(szoveg):
    """'1Móz 8:20-22' | '1Móz 4:25-5:32' | '1Móz 14' | 'Mt 5:3' -> (könyv, (c1, v1), (c2, v2)); v None = a fejezet vége."""
    m = SZAKASZ_RX.match((szoveg or '').strip())
    if not m:
        raise SystemExit('a szakasz nem értelmezhető: %r (alak: „1Móz 8:20-22”, „1Móz 4:25-5:32”, „1Móz 14”)' % szoveg)
    c1 = int(m.group('c1'))
    v1 = int(m.group('v1')) if m.group('v1') else None
    if m.group('v2') is None:
        return m.group('konyv'), (c1, v1 or 1), (c1, v1)
    if v1 is None:
        raise SystemExit('a szakasz nem értelmezhető: %r (fejezettartománynál versszám kell)' % szoveg)
    c2 = int(m.group('c2')) if m.group('c2') else c1
    eleje, vege = (c1, v1), (c2, int(m.group('v2')))
    if vege < eleje:
        raise SystemExit('a szakasz vége az eleje előtt áll: %r' % szoveg)
    return m.group('konyv'), eleje, vege


def benne(igehely, konyv, eleje, vege):
    m = IGEHELY_RX.match(igehely or '')
    if not m or m.group('konyv') != konyv:
        return False
    cv = (int(m.group('c')), int(m.group('v')))
    if vege[1] is None:                     # a teljes fejezet (vagy az utolsó fejezet vége)
        return eleje <= cv and cv[0] <= vege[0]
    return eleje <= cv <= vege


def szakasz_strongok(konyv, eleje, vege, konk=KONK):
    """-> (OrderedDict: Strong -> a versek listája, a forrásfájl neve, a talált versek száma). Kulcs szerint olvas."""
    for nev in ('TAHOT_kivonat.tsv', 'TAGNT_kivonat.tsv'):
        fej, sorok = tsv_sorok(os.path.join(konk, nev))
        talalt = [r for r in sorok if benne(r.get('Igehely'), konyv, eleje, vege)]
        if talalt:
            ki = collections.OrderedDict()
            versek = set()
            for r in talalt:
                versek.add(r['Igehely'])
                for tok in (r.get('Strong-szám') or '').split('+'):
                    tok = tok.strip()
                    if re.fullmatch(r'[HG]\d{4}', tok):
                        ki.setdefault(tok, [])
                        if r['Igehely'] not in ki[tok]:
                            ki[tok].append(r['Igehely'])
            return ki, nev, len(versek)
    return collections.OrderedDict(), None, 0


def bdb_aliasok(ut=os.path.join(KONK, 'BDB_strong_alias.tsv')):
    """{másodlagos Strong: a szócikket hordozó Strong} (`BDB_strong_alias.tsv`, a `pardes.db` `bdb_alias` forrása)."""
    if not os.path.exists(ut):
        return {}
    _, sorok = tsv_sorok(ut)
    return {r['masodlagos_strong']: r['tabla_strong'] for r in sorok if r.get('masodlagos_strong') and r.get('tabla_strong')}


def nyelvtani_strongok(ut=os.path.join(ADAT, 'grammatikai_strongok.tsv')):
    _, sorok = tsv_sorok(ut)
    return {r['strong'] for r in sorok if r.get('strong')}


# ---------------------------------------------------------------- állapot láncanként

def forditas_sorok(ut=os.path.join(ADAT, 'forditasok.tsv')):
    """{(szótár, Strong_padded): [sor, …]} a három lánc szótárára."""
    _, sorok = tsv_sorok(ut)
    d = collections.defaultdict(list)
    for r in sorok:
        sz = r.get('szotar')
        if sz not in LANCOK:
            continue
        st = r.get('strong', '')
        if sz in ('Thayer', 'TBESG'):
            st = kulcs.strong_pad(st) or st
        d[(sz, st)].append(r)
    return d


def bdb_allapot(strong, sorok, tabla=None):
    """-> (állapot, részlet, a fordítandó forrás karakterszáma, egység)."""
    szak = SB.szakaszok(strong, tabla) if tabla else SB.szakaszok(strong)
    if szak is None:
        szoveg, _, felh = SB.strong_magyar_sorok(sorok)
        if szoveg:
            return 'kesz', 'szakasztáblán kívül; `teljes` sor (%s)' % felh[0].get('allapot', ''), 0, 0
        return 'nincs_szakasz', 'a Strong nincs a bdb_szakaszok.tsv-ben, és `teljes` sora sincs', 0, 0
    _, mod, felh = SB.strong_magyar_sorok(sorok)
    if mod == 'teljes' and felh and felh[0].get('allapot') == 'kezi':
        return 'kesz', 'jóváhagyott `kezi` `teljes` sor (DT290 (3))', 0, 0
    if mod == 'teljes' and felh and felh[0].get('allapot') != 'elavult':
        # a 13. szabály a lefedést csak a szakaszsorral bíró Strongon méri; a nem `elavult` `teljes` sor érvényes
        # fordítás (a forras_hash-ét a 13. szabály őrzi), a szakaszos újrafordítás a #38 dolga, nem hiány
        return 'kesz', '`teljes` sor (%s), szakaszsor nélkül' % felh[0].get('allapot', ''), 0, 0
    st, ok, megj = szolista.allapot(strong, szak, sorok)
    if st == 'kihagyva':
        return 'kesz', megj, 0, 0
    return _forditando(ok, megj, szak, sorok)


def thayer_allapot(strong, sorok, tabla=None):
    szak = TB.szakaszok(strong, tabla)
    st, ok, megj = szolista.allapot(strong, szak, sorok)
    if st == 'kihagyva':
        return ('kesz' if ok == 'kesz' else ok), megj, 0, 0
    return _forditando(ok, megj, szak, sorok)


def _forditando(ok, megj, szak, sorok):
    """A fordítandó szakaszok karakterszáma: a hiányzó és az eltérő hash-ű szakaszoké (ok `nincs_szakaszos`: mindé)."""
    ervenyes = collections.defaultdict(set)
    for r in sorok:
        n = SB.sorszam_jelentesbol(r.get('jelentes_szam'))
        if n is not None and r.get('allapot') != 'elavult' and (r.get('forditas_hu') or '').strip():
            ervenyes[n].add(r.get('forras_hash', ''))
    kell = [x for x in szak if x['hash'] not in ervenyes.get(x['sorszam'], set())]
    allapot = {'nincs_szakaszos': 'hianyzik', 'hianyos': 'hianyos', 'elavult_hash': 'elavult_hash'}.get(ok, ok)
    return allapot, megj or ok, sum(len(x['szoveg']) for x in kell), len(kell)


def tbesg_allapot(strong, sorok, cache):
    """-> (állapot, részlet, karakter, egység, forras_hash)."""
    minta = {'szotar': 'TBESG', 'strong': strong, 'entry_id': strong, 'jelentes_szam': 'rovid', 'mezo': 'glosszak_hu'}
    forras = GLF.tovabbi_forras(minta, cache=cache)
    if not forras:
        return 'nincs_forras', 'a TBESG.txt-ben nincs rövid jelentés', 0, 0, ''
    h = hashlib.sha1(forras.encode('utf-8')).hexdigest()
    rovid = [r for r in sorok if r.get('jelentes_szam') == 'rovid' and r.get('mezo') == 'glosszak_hu']
    ervenyes = [r for r in rovid if r.get('allapot') != 'elavult' and (r.get('forditas_hu') or '').strip()]
    if any(r.get('forras_hash') == h for r in ervenyes):
        return 'kesz', '', 0, 0, h
    if ervenyes:
        return 'elavult_hash', 'a forras_hash nem a mai forrásé', len(forras), 1, h
    return 'hianyzik', 'nincs érvényes `rovid` sor', len(forras), 1, h


# ---------------------------------------------------------------- a futás

def futtat(szakasz, ts, konk=KONK, ford_ut=None, nyelvtani=None, bdb_tabla=None, thayer_tabla=None):
    konyv, eleje, vege = szakasz_elemez(szakasz)
    strongok, fajl, versszam = szakasz_strongok(konyv, eleje, vege, konk)
    if not fajl:
        raise SystemExit('a szakaszra nincs sor a TAHOT/TAGNT kivonatban: %r (a könyvnév a projekt alakja, pl. „1Móz”)'
                         % szakasz)
    nyelvtani = nyelvtani_strongok() if nyelvtani is None else nyelvtani
    ford = forditas_sorok(ford_ut) if ford_ut else forditas_sorok()
    kihagyott = [s for s in strongok if s in nyelvtani]
    alias = bdb_aliasok()
    cache = {}
    sorok, glossza = [], []
    for st, versek in strongok.items():
        if st in nyelvtani:
            continue
        prov = 'scope=%s | forras=%s | ts=%s' % (st, FORRAS, ts)
        vlista = '; '.join(versek)
        if st.startswith('H'):
            cel = alias.get(st, st)
            a, r, k, e = bdb_allapot(cel, ford.get(('BDB', cel), []), bdb_tabla)
            if cel != st:
                r = 'a BDB-szócikk a %s-n áll (BDB_strong_alias.tsv); %s' % (cel, r)
            sorok.append({'strong': st, 'cel': cel, 'lanc': 'BDB', 'allapot': a, 'reszlet': r, 'karakter': k,
                          'egyseg': e, 'versek': vlista, 'proveniencia': prov})
        else:
            a, r, k, e = thayer_allapot(st, ford.get(('Thayer', st), []), thayer_tabla)
            sorok.append({'strong': st, 'lanc': 'Thayer', 'allapot': a, 'reszlet': r, 'karakter': k, 'egyseg': e,
                          'versek': vlista, 'proveniencia': prov})
            a, r, k, e, h = tbesg_allapot(st, ford.get(('TBESG', st), []), cache)
            sorok.append({'strong': st, 'lanc': 'TBESG', 'allapot': a, 'reszlet': r, 'karakter': k, 'egyseg': e,
                          'versek': vlista, 'proveniencia': prov})
            if a in ('hianyzik', 'elavult_hash'):
                glossza.append({'szotar': 'TBESG', 'strong': st, 'entry_id': st, 'jelentes_szam': 'rovid',
                                'mezo': 'glosszak_hu', 'forras_hash': h, 'allapot': 'hianyzik'})
    return {'szakasz': szakasz, 'fajl': fajl, 'versek': versszam, 'strongok': len(strongok),
            'kihagyott': kihagyott, 'sorok': sorok, 'glossza': glossza, 'ts': ts}


FORDITANDO = ('hianyzik', 'hianyos', 'elavult_hash')


def becsles(eredmeny):
    ki = []
    bemenet = {'BDB': ('bdb_strongok.txt', 'a BDB-lánc adag-sorrendjébe kézzel (`bdb_api_koteg.py --adag N szaraz`)'),
               'Thayer': ('thayer_strongok.txt', 'python eszkozok/thayer_api_koteg.py szaraz --adag N --strongok thayer_strongok.txt '
                                                 '--munka <repón kívüli mappa> (a lánc a Strong összes szakaszát küldi)'),
               'TBESG': ('glossza_lista.tsv', 'python eszkozok/glossza_api_koteg.py szaraz --lista glossza_lista.tsv')}
    for lanc in LANCOK:
        f = [r for r in eredmeny['sorok'] if r['lanc'] == lanc and r['allapot'] in FORDITANDO]
        ki.append({'lanc': lanc, 'fordítandó_strong': len(f), 'fordítandó_egyseg': sum(r['egyseg'] for r in f),
                   'forras_karakter': sum(r['karakter'] for r in f), 'bemenet': bemenet[lanc][0],
                   'parancs': bemenet[lanc][1]})
    return ki


def jelentes_szoveg(e):
    sz = collections.Counter((r['lanc'], r['allapot']) for r in e['sorok'])
    out = ['# Szakasz-fordítás: %s' % e['szakasz'], '',
           '- forrás: `konkordancia/%s` (Károli-kulcs), %d vers, %d Strong; nyelvtani (kihagyva): %d%s'
           % (e['fajl'], e['versek'], e['strongok'], len(e['kihagyott']),
              (' (%s)' % ', '.join(e['kihagyott'])) if e['kihagyott'] else ''),
           '- proveniencia: `scope=%s | forras=%s | ts=%s`' % (e['szakasz'], FORRAS, e['ts']), '',
           '| lánc | állapot | Strong |', '|---|---|---|']
    for (lanc, a), n in sorted(sz.items()):
        out.append('| %s | %s | %d |' % (lanc, a, n))
    out += ['', '## Száraz becslés (fordítás és API-hívás nem fut)', '',
            '| lánc | fordítandó Strong | egység | forrás karakter | bemenet |', '|---|---|---|---|---|']
    for b in becsles(e):
        out.append('| %s | %d | %d | %d | `%s` |' % (b['lanc'], b['fordítandó_strong'], b['fordítandó_egyseg'],
                                                    b['forras_karakter'], b['bemenet']))
    f = [r for r in e['sorok'] if r['allapot'] in FORDITANDO]
    out += ['', '## Fordítandó', '']
    if not f:
        out.append('üres — a szakasz minden nem nyelvtani Strongjának érvényes fordítása van a három láncban.')
    for r in f:
        out.append('- %s %s: %s — %s (versek: %s)' % (r['strong'], r['lanc'], r['allapot'], r['reszlet'], r['versek']))
    n = [r for r in e['sorok'] if r['allapot'] in ('nincs_szakasz', 'nincs_forras')]
    if n:
        out += ['', '## Nincs mit fordítani (a szótárban nincs forrás; nem pótolt)', '']
        out += ['- %s %s: %s' % (r['strong'], r['lanc'], r['reszlet']) for r in n]
    return '\n'.join(out) + '\n'


def repon_kivul(ut):
    a, g = os.path.abspath(ut), os.path.abspath(GYOKER)
    try:
        return os.path.normcase(os.path.commonpath([a, g])) != os.path.normcase(g)
    except ValueError:          # más meghajtó (Windows): biztosan a repón kívül
        return True


def kiir(e, mappa):
    if not repon_kivul(mappa):
        raise SystemExit('a --ki mappa a repón kívül legyen (a lista futásonkénti munkaanyag, nem adattábla): %s' % mappa)
    os.makedirs(mappa, exist_ok=True)
    fej = '# GENERÁLT: eszkozok/szakasz_forditas.py --szakasz "%s" --ts %s; forras: adat/forditasok.tsv@%s' % (
        e['szakasz'], e['ts'], sha12(os.path.join(ADAT, 'forditasok.tsv')))
    for lanc, nev in (('BDB', 'bdb_strongok.txt'), ('Thayer', 'thayer_strongok.txt')):
        f = [r.get('cel', r['strong']) for r in e['sorok'] if r['lanc'] == lanc and r['allapot'] in FORDITANDO]
        f = list(collections.OrderedDict.fromkeys(f))
        with open(os.path.join(mappa, nev), 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join([fej] + f) + '\n')
    with open(os.path.join(mappa, 'glossza_lista.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\t'.join(GLOSSZA_FEJLEC) + '\n')
        for r in e['glossza']:
            fh.write('\t'.join(r[k] for k in GLOSSZA_FEJLEC) + '\n')
    with open(os.path.join(mappa, 'becsles.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(fej + '\n' + '\t'.join(BECSLES_FEJLEC) + '\n')
        for b in becsles(e):
            fh.write('\t'.join(str(b[k]) for k in BECSLES_FEJLEC) + '\n')
    with open(os.path.join(mappa, 'jelentes.tsv'), 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(fej + '\n' + '\t'.join(JELENTES_FEJLEC) + '\n')
        for r in e['sorok']:
            fh.write('\t'.join(str(r[k]).replace('\t', ' ') for k in JELENTES_FEJLEC) + '\n')


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--szakasz', required=True, help='pl. „1Móz 8:20-22”, „1Móz 4:25-5:32”, „Mt 5:3-12”')
    ap.add_argument('--ki', default=None, help='a láncok bemenetének mappája, a repón kívül')
    ap.add_argument('--ts', default=None, help='a proveniencia dátuma (alapérték: ma)')
    a = ap.parse_args(argv)
    ts = a.ts or datetime.date.today().isoformat()
    e = futtat(a.szakasz, ts)
    sys.stdout.write(jelentes_szoveg(e))
    if a.ki:
        kiir(e, a.ki)
        sys.stdout.write('\nA láncok bemenete: %s\n' % os.path.abspath(a.ki))
    return 0


if __name__ == '__main__':
    sys.exit(main())
