#!/usr/bin/env python
"""A Thayer szakaszonkénti fordításának adatblokkja (F132, brief 2a/3, 2a/4, 2a/5, 2a/6).

Csoportonként (a fordító egy hívásának szakaszai) gépileg előállított, proveniencia-soros blokk a prompt `{{ADATBLOKK}}` helyére.
Nem értelmez és nem egészít ki emlékezetből (CLAUDE.md 3. szabály); hiánynál kifejezett jelzés.

  1. Károli-alakok (2a/3): a Strong Károli-szóalakjai a #22 párosításából (`adat/karoli_strong/parok_*.tsv`), gyakorisággal,
     magas / alacsony bizonyosság szerint; a párosítás le nem fedett ÚSZ-könyvei (ma: Mt, Mk, Lk, Jn, ApCsel) explicit.
  2. Idézett versek Károli-szövege (2a/4): a csoport szakaszaiban `bcv`-vel idézett versek (`adat/thayer_vers_jelentes.tsv`) a
     `Karoli_1908.tsv` szerint; Károli-kulcs nélkül `[nincs Károli-vers]`; hosszú vers `VERS_MAX` karakterre vágva (`…`).
  3. Siglák (2a/5): a csoport szövegében előforduló `adat/thayer_sigla.tsv`-sorok; besorolt sornál a kötelező alak; besorolatlannál
     a terminológiai szójegyzék alakja, ha van (`adat/terminologia.tsv` `angol` = a forrásalak), különben a forrás alakja marad.
  4. Nyelvközi híd (2a/6): a csoport héber szavai (a `Thayer.lexicon` `ref0` jelölése, szerkezetként; csak héber írású) a
     `Strong_szotar.tsv` pontozott szótövével pontosan egyezve (többszavas kifejezésnél szavanként); a találat H-Strongjának
     meglévő magyar BDB-fordítása (a közös összefűzővel, rövidítve); egyezés nélkül `[nincs Strong-egyezés]`. A terminológiai
     szójegyzék a prompt kötelező alakjaiban jön (nem itt).

  python eszkozok/thayer_jelolt/adatblokk.py G1941 [--csoport 1] [--ki PATH]
TSV: split('\\t'), csv modul nélkül.
"""
import argparse
import collections
import datetime
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
if ITT not in sys.path:
    sys.path.insert(0, ITT)
import bont  # noqa: E402
import kulcs  # noqa: E402
import szolista  # noqa: E402
import thayer_bemenet as TB  # noqa: E402
import thayer_kapuk as TK  # noqa: E402

GYOKER = TB.GYOKER
PAROK_MAPPA = os.path.join(GYOKER, 'adat', 'karoli_strong')
KONYV_UT = os.path.join(GYOKER, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
KAROLI_UT = os.path.join(GYOKER, 'konkordancia', 'Karoli_1908.tsv')
VERS_UT = os.path.join(GYOKER, 'adat', 'thayer_vers_jelentes.tsv')
SZOTAR_UT = os.path.join(GYOKER, 'konkordancia', 'Strong_szotar.tsv')
FORDITASOK_UT = os.path.join(GYOKER, 'adat', 'forditasok.tsv')
TERM_UT = os.path.join(GYOKER, 'adat', 'terminologia.tsv')
NINCS_KAROLI_ALAK = '[NINCS KÁROLI-ALAK]'
ALAK_MAX = 10
VERS_MAX = 220
HID_MAGYAR_MAX = 200
HEBER = re.compile(r'[֐-׿]')
REF0 = re.compile(r'<ref0\b[^>]*\bentry="([^"]*)"')

_C = {}


def _c(k, fv):
    if k not in _C:
        _C[k] = fv()
    return _C[k]


def prov(scope, forras, ts):
    return '*proveniencia: scope=%s | forras=%s | ts=%s*' % (scope, forras, ts)


def tsv(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s.rstrip('\r') for s in f.read().split('\n')]
    return [s.split('\t') for s in sorok if s and not s.startswith('#')]


def usz_konyvek():
    """A Konyv_normalizalo_tabla.tsv 40–66. adatsorának magyar rövidítése, sorrendben."""
    def be():
        s = tsv(KONYV_UT)
        i = s[0].index('Magyar rövidítés')
        return [r[i] for r in s[40:66]]
    return _c('usz', be)


def parok_g():
    """{Strong_padded: [(vers, hu_szo, bizonyossag)]} és a párosítás könyvei (a G-sort tartalmazó fájlok)."""
    def be():
        d, konyvek = collections.defaultdict(list), set()
        for fn in sorted(os.listdir(PAROK_MAPPA)):
            if not re.match(r'^parok_.+\.tsv$', fn):
                continue
            s = tsv(os.path.join(PAROK_MAPPA, fn))
            fej = s[0]
            iv, isz, ist, ib = fej.index('vers'), fej.index('hu_szo'), fej.index('strong'), fej.index('bizonyossag')
            for r in s[1:]:
                p = kulcs.strong_pad(r[ist])
                if p:
                    d[p].append((r[iv], r[isz], r[ib]))
                    konyvek.add(r[iv].rsplit(' ', 1)[0])
        return d, konyvek
    return _c('parok', be)


def karoli():
    def be():
        s = tsv(KAROLI_UT)
        return {r[0]: r[1] for r in s[1:]}
    return _c('karoli', be)


def vers_jelentes():
    def be():
        s = tsv(VERS_UT)
        fej = s[0]
        d = collections.defaultdict(list)
        for r in s[1:]:
            x = dict(zip(fej, r))
            d[(x['strong'], int(x['szakasz']))].append(x)
        return d
    return _c('vers', be)


def szotar_heber():
    def be():
        s = tsv(SZOTAR_UT)
        d = collections.defaultdict(list)
        for r in s[1:]:
            if r[0].startswith('H'):
                d[unicodedata.normalize('NFC', r[1])].append(r[0])
        return d
    return _c('szotar', be)


def forditasok_szotar(szotar):
    def be():
        s = tsv(FORDITASOK_UT)
        fej = s[0]
        d = collections.defaultdict(list)
        for r in s[1:]:
            x = dict(zip(fej, r))
            if x.get('szotar') == szotar:
                d[x['strong']].append(x)
        return d
    return _c('ford_' + szotar, be)


def terminologia():
    def be():
        s = tsv(TERM_UT)
        fej = s[0]
        return [dict(zip(fej, r)) for r in s[1:]]
    return _c('term', be)


def lexikon_szerkezet(sp):
    lex = _c('lex', bont.lexikon_beolvas)
    if sp not in lex:
        return []
    return bont.szerkezet(lex[sp][1])


# ------------------------------------------------------------------ szakaszok

def szakasz_karoli(sp, ts):
    d, konyvek = parok_g()
    hiany = [k for k in usz_konyvek() if k not in konyvek]
    sor = ['**1. Károli-szóalakok** (a #22 Károli–Strong párosítás; az ÚSZ-ből le nem fedett könyvek: %s — ezekre az arány nem érvényes, '
           'a hiány nem pótolt; a szóalakok kisbetűsítve)' % (', '.join(hiany) or 'nincs')]
    p = d.get(sp, [])
    if not p:
        sor.append(NINCS_KAROLI_ALAK)
    else:
        magas, egyeb = collections.Counter(), collections.Counter()
        for _v, szo, biz in p:
            (magas if biz == 'magas' else egyeb)[szo.lower()] += 1

        def lista(c):
            l = sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))
            r = ', '.join('%s ×%d' % kv for kv in l[:ALAK_MAX])
            return (r + (' (+%d további alak)' % (len(l) - ALAK_MAX) if len(l) > ALAK_MAX else '')) or '—'
        sor.append('- magas bizonyosságú pár: %s' % lista(magas))
        sor.append('- alacsonyabb bizonyosságú pár: %s' % lista(egyeb))
        sor.append('- %d link, %d különböző vers' % (len(p), len({v for v, _, _ in p})))
    sor.append(prov(sp, 'adat/karoli_strong/parok_*.tsv', ts))
    return sor


def szakasz_versek(sp, csoport, ts):
    vj = vers_jelentes()
    kv = karoli()
    sor = ['**2. Az idézett versek Károli-szövege** (a szakaszok `bcv`-hivatkozásai; a hivatkozást a Károli-rövidítéssel írd)']
    lattam, db = set(), 0
    for x in csoport:
        for r in vj.get((sp, x['sorszam']), []):
            k = r['karoli_vers'] or '%s %s:%s' % (r['konyv'], r['fejezet'], r['vers'])
            if k in lattam:
                continue
            lattam.add(k)
            db += 1
            if not r['karoli_vers']:
                sor.append('- ⟪%d⟫ %s: [nincs Károli-vers ezzel a számmal]' % (x['sorszam'], k))
                continue
            t = kv.get(r['karoli_vers'], '')
            if len(t) > VERS_MAX:
                t = t[:VERS_MAX].rsplit(' ', 1)[0] + ' …'
            sor.append('- ⟪%d⟫ %s „%s”' % (x['sorszam'], k, t))
    if not db:
        sor.append('— (a szakaszokban nincs `bcv`-hivatkozás)')
    sor.append(prov(sp, 'adat/thayer_vers_jelentes.tsv + konkordancia/Karoli_1908.tsv', ts))
    return sor


def szakasz_sigla(sp, csoport, ts):
    szoveg = TB.nezet(csoport)
    sor = ['**3. Siglák és rövidítések** (a sigla-tábla szerint; a besorolt alak kötelező, 16. kapu; a terminológiai '
           'szójegyzék alakja minden esetben elsőbbséget kap)']
    term = {}
    for r in terminologia():
        term.setdefault(r.get('angol', ''), r.get('magyar', ''))
    db = 0
    for r in TK.sigla_betolt():
        if not r.get('forrasalak') or not TK._re(r['forrasalak']).search(szoveg):
            continue
        db += 1
        if r.get('allapot') == 'besorolt' and r.get('magyar_alak') == TK.NINCS_EGYSEGES:
            sor.append('- `%s` [nincs egységes magyar alak: a szövegkörnyezet szerint%s]'
                       % (r['forrasalak'], (' — %s' % r['jelentes']) if r.get('jelentes') else ''))
        elif r.get('allapot') == 'besorolt' and r.get('magyar_alak'):
            sor.append('- `%s` → `%s`%s' % (r['forrasalak'], r['magyar_alak'], (' (%s)' % r['jelentes']) if r.get('jelentes') else ''))
        elif r['forrasalak'] in term:
            sor.append('- `%s` [besorolatlan a sigla-táblában; a terminológia szerint: `%s`]' % (r['forrasalak'], term[r['forrasalak']]))
        else:
            sor.append('- `%s` [besorolatlan: a forrás alakjában marad, amíg a tábla be nem sorolja]' % r['forrasalak'])
    if not db:
        sor.append('—')
    sor.append(prov(sp, 'adat/thayer_sigla.tsv + adat/terminologia.tsv', ts))
    return sor


def szakasz_hid(sp, csoport, ts):
    szerk = lexikon_szerkezet(sp)
    sor = ['**4. Nyelvközi híd** (a szakaszok héber szavai; a héber szó meglévő magyar BDB-fordításának eleje — '
           'a görög és a héber azonos magyar szót kapjon; rangsor: szójegyzék > Károli > BDB > szótár)']
    szavak = []
    for x in csoport:
        if 1 <= x['sorszam'] <= len(szerk):
            for e in REF0.findall(szerk[x['sorszam'] - 1]['raw']):
                e = unicodedata.normalize('NFC', e)
                if HEBER.search(e) and e not in szavak:
                    szavak.append(e)
    if not szavak:
        sor.append('— (a szakaszokban nincs héber szó)')
    sz = szotar_heber()
    bdb = forditasok_szotar('BDB')
    for e in szavak:
        h = sz.get(e, [])
        if not h and ' ' in e:
            # többszavas kifejezés: szavanként (csak pontos szótő-egyezés)
            h = [hs for w in e.split() for hs in sz.get(w, [])]
            if h:
                sor.append('- %s: szavanként:' % e)
        if not h:
            sor.append('- %s: [nincs Strong-egyezés]' % e)
            continue
        for hs in h:
            hu, mod = TB.strong_magyar(bdb.get(hs, []))[:2] if bdb.get(hs) else (None, None)
            if hu:
                hu = hu if len(hu) <= HID_MAGYAR_MAX else hu[:HID_MAGYAR_MAX].rsplit(' ', 1)[0] + ' …'
                sor.append('- %s = %s: BDB magyarul (%s): „%s”' % (e, hs, mod, hu))
            else:
                sor.append('- %s = %s: [nincs magyar BDB-fordítás]' % (e, hs))
    sor.append(prov(sp, 'Thayer.lexicon (ref0, szerkezet) + konkordancia/Strong_szotar.tsv + adat/forditasok.tsv (BDB)', ts))
    return sor


def blokk(strong, csoport=None, ts=None):
    """A csoport (szakaszlista; alapból a Strong minden szakasza) adatblokkja, markdown szövegként."""
    sp = kulcs.strong_pad(strong)
    szak = TB.szakaszok(sp)
    if szak is None:
        return 'nincs adatblokk'
    csoport = szak if csoport is None else csoport
    ts = ts or datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    reszek = [szakasz_karoli(sp, ts), szakasz_versek(sp, csoport, ts), szakasz_sigla(sp, csoport, ts), szakasz_hid(sp, csoport, ts)]
    illeszt = szak[0]['illesztes']
    fej = ['### Adatblokk — Thayer %s (gépi, a projekt adataiból; nem értelmezés)' % kulcs.strong_eredeti(sp)]
    if illeszt == 'javitassal':
        fej.append('[a forrásszöveg a Thayer_teljes.tsv szövegvesztése miatt a lexikonból kiegészítve (adat/thayer_forras_javitas.tsv, '
                   'DT-F132i (2)); a szakaszok szövege teljes]')
    elif illeszt != 'egyezik':
        fej.append('[FIGYELEM: a forrásszöveg illesztése `%s` (a Thayer_teljes.tsv szövegrészt veszít; DT-F132i) — a hiányt ne pótold]'
                   % illeszt)
    return '\n'.join(fej + [''] + ['\n'.join(r) + '\n' for r in reszek]).rstrip('\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('strong')
    ap.add_argument('--csoport', type=int, help='a csoport sorszáma (1-től; thayer_bemenet.csoportok)')
    ap.add_argument('--ki')
    ap.add_argument('--ts')
    a = ap.parse_args()
    szak = TB.szakaszok(a.strong)
    cs = None
    if a.csoport and szak:
        cs = TB.csoportok(szak)[a.csoport - 1]
    t = blokk(a.strong, cs, a.ts) + '\n'
    if a.ki:
        with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write(t)
        print('irva: %s (%d karakter)' % (a.ki, len(t)))
    else:
        sys.stdout.write(t)
    return 0


if __name__ == '__main__':
    sys.exit(main())
