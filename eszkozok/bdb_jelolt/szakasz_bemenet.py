#!/usr/bin/env python
"""A BDB szakaszonkénti fordításának bemenete (F128, FELADATOK #128; DT181 (b), DT269 (1), DT-F128a–d).

Strongonként a szakasztábla (`adat/bdb_szakaszok.tsv`, 2.30) sorai, sorszám szerint: a szakasz szövege a `jel` + `szoveg` egy
szóközzel (mint a `nezet_general.py` nézetében), a javítótábla (`adat/bdb_forras_javitas.tsv`, 2.31) `hivatkozas` / `javitva`
soraival, **pe/mem csere nélkül** (DT269 (1)). A hivatkozás-javítás a Strong nézet-szövegében áll (a `forras_alak` k-adik
egész-token előfordulása), ezért a csere a Strong-nézeten történik, és a szakaszhatár mentén vágódik vissza; határon átnyúló
javítás hibát ad (mért: 0 / 412).

A fordító bemenete a szakaszok egymásutánja, minden szakasz előtt a határtokennel: `⟪<sorszam>⟫` (a sorszám a szakasztábla
`sorszam`-a; a `⟦n⟧` az `emeles.py` héber/görög helyőrzője, ezért a határtoken más jel). A tokent a fordítás változatlanul
viszi át (prompt v5; kapu: `forditas_kapuk.ellenoriz_szakasz`).

  - `szakaszok(strong)`: [{sorszam, jel, utvonal, szoveg, hash}] vagy None (a 9 táblán kívüli Strong: a régi `teljes` út,
    DT-F128d (2)); a `szoveg` a javított szakaszszöveg token nélkül, a `hash` ennek SHA-1-e (a `forditasok.tsv` `sz<n>`
    sorának `forras_hash`-e, DT-F128b (1)).
  - `tokenes(szakaszok)`: a bemenet szövege, soronként `⟪n⟫ <szöveg>`.
  - `csoportok(szakaszok)`: a hívások egysége (DT-F128c (2)): 20 000 karakterig egy csoport; fölötte egymást követő csoportok
    legfeljebb ~10 000 karakterig, csak tokenhatáron, a törzs- vagy a számszint váltásánál előnyben.
  - `strong_magyar(sorok)`: a közös összefűző (DT-F128a (a)): egy Strong `forditasok.tsv`-sorainak magyar szövege — a nem
    `elavult` `sz<n>` sorok sorszám szerint, egy szóközzel; ha nincs ilyen, a `teljes` sor (a nem `elavult` elsőbbséggel).

CLI:
  python eszkozok/bdb_jelolt/szakasz_bemenet.py H0001 [--ki PATH]   a tokenes bemenet (a csoportokkal)
  python eszkozok/bdb_jelolt/szakasz_bemenet.py --ellenoriz        determinizmus, egyezés a nezet_general.py (pe/mem nélküli)
                                                                   nézetével, 0 pe/mem csere, csoport-statisztika
TSV: split('\\t'), csv modul nélkül. Fájlt nem ír (csak a --ki útvonalra).
"""
import argparse
import collections
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(os.path.dirname(ITT))
TABLA = os.path.join(GYOKER, 'adat', 'bdb_szakaszok.tsv')
JAV = os.path.join(GYOKER, 'adat', 'bdb_forras_javitas.tsv')


def _modulok():
    """A forras_javit és a nezet_general lustán: a `strong_magyar` (az olvasó szerver, F128 DT-F128g) csak stdlib-et húz be."""
    if ITT not in sys.path:
        sys.path.insert(0, ITT)
    import forras_javit
    import nezet_general
    return forras_javit, nezet_general


def __getattr__(nev):
    # visszafelé: `szakasz_bemenet.nezet_general` (tesztek, eseti szkriptek)
    if nev in ('nezet_general', 'forras_javit'):
        fj, ng = _modulok()
        return ng if nev == 'nezet_general' else fj
    raise AttributeError(nev)


TOKEN = re.compile(r'⟪(\d+)⟫')
EGY_HIVAS_HATAR = 20000   # DT-F128c (2): eddig a Strong egy hívás
CSOPORT_CEL = 10000       # DT-F128c (2): fölötte ~10 000 karakteres csoportok
SZAKASZ_ELOTAG = 'sz'     # DT-F128a (a): jelentes_szam = sz<sorszam>


def token(sorszam):
    return '⟪%s⟫' % sorszam


def jelentes_szam(sorszam):
    return '%s%s' % (SZAKASZ_ELOTAG, sorszam)


def sorszam_jelentesbol(jsz):
    m = re.match(r'^%s(\d+)$' % SZAKASZ_ELOTAG, jsz or '')
    return int(m.group(1)) if m else None


def sha1(t):
    return hashlib.sha1(t.encode('utf-8')).hexdigest()


_CACHE = {}


def _betolt(tabla=None, jav_ut=None):
    """(szakasztábla Strongonként, `hivatkozas` / `javitva` javítások Strongonként); útvonalanként gyorsítótárazva
    (az `ellenoriz.py` 13. szabálya a saját `adat_dir`-jéből hívja)."""
    tabla, jav_ut = tabla or TABLA, jav_ut or JAV
    kulcs = (os.path.abspath(tabla), os.path.abspath(jav_ut))
    if kulcs not in _CACHE:
        _, ng = _modulok()
        tab = collections.OrderedDict()
        for r in ng.olvas(tabla):
            tab.setdefault(r['strong'], []).append(r)
        jav = collections.defaultdict(list)
        for d in ng.olvas(jav_ut):
            if d['allapot'] == 'javitva' and d['hiba'] == 'hivatkozas':
                jav[d['strong']].append(d)
        _CACHE[kulcs] = (tab, jav)
    return _CACHE[kulcs]


def szakaszok(strong, tabla=None, jav_ut=None):
    """A Strong szakaszai a javított szöveggel; None, ha a Strong nincs a szakasztáblában."""
    forras_javit, _ = _modulok()
    tab, jav = _betolt(tabla, jav_ut)
    sorok = tab.get(strong)
    if sorok is None:
        return None
    szoveg, hatar = forras_javit.strong_nezet(sorok)
    # a hivatkozás-javítás a nezet_general.py logikájával: a k-adik egész-token előfordulás, a szakaszhoz rendelve
    cserek = collections.defaultdict(list)
    for d in jav.get(strong, []):
        poz = forras_javit.token_elofordulas(szoveg, d['forras_alak'])
        k = int(d['elofordulas'])
        if k < 1 or k > len(poz):
            raise ValueError('%s: a hivatkozás-javítás nem alkalmazható (%s, %d.)' % (strong, d['forras_alak'], k))
        p = poz[k - 1]
        e = p + len(d['forras_alak'])
        h = [i for i, (a, b, _) in enumerate(hatar) if a <= p < b]
        if not h or e > hatar[h[0]][1]:
            raise ValueError('%s: a hivatkozás-javítás szakaszhatáron nyúlik át (%s)' % (strong, d['forras_alak']))
        cserek[h[0]].append((p - hatar[h[0]][0], d['forras_alak'], d['javitott_alak']))
    ki = []
    for i, (a, b, x) in enumerate(hatar):
        t = szoveg[a:b]
        for p, regi, uj in sorted(cserek.get(i, []), reverse=True):
            t = t[:p] + uj + t[p + len(regi):]
        ki.append({'sorszam': int(x['sorszam']), 'jel': x['jel'], 'utvonal': x['utvonal'], 'szoveg': t, 'hash': sha1(t)})
    return ki


def nezet(szak):
    """A token nélküli Strong-szöveg (= a nezet_general.py pe/mem nélküli nézete)."""
    return ' '.join(x['szoveg'] for x in szak)


def tokenes(szak):
    return '\n'.join('%s %s' % (token(x['sorszam']), x['szoveg']) for x in szak)


def _hossz(x):
    return len(token(x['sorszam'])) + 1 + len(x['szoveg'])


def _torzs_szam(utvonal):
    r = (utvonal or '').split('/')
    return (r[0] if r else ''), (r[1] if len(r) > 1 else ''), (r[2] if len(r) > 2 else '')


def _vagas_elonye(elozo, x):
    """2: törzsváltás, 1: új számszintű pont (betű nélkül), 0: egyéb tokenhatár."""
    t0, _, _ = _torzs_szam(elozo['utvonal'])
    t1, s1, b1 = _torzs_szam(x['utvonal'])
    if t1 not in ('', '-', 'cim', 'fej') and t1 != t0:
        return 2
    if s1 not in ('', '-') and b1 in ('', '-'):
        return 1
    return 0


def csoportok(szak, hatar=EGY_HIVAS_HATAR, cel=CSOPORT_CEL):
    """A szakaszok hívásonkénti csoportjai (listák listája, a szakaszok sorrendjében)."""
    if sum(_hossz(x) for x in szak) <= hatar:
        return [list(szak)]
    ki, cur = [], []
    for x in szak:
        if cur and sum(_hossz(y) for y in cur) + _hossz(x) > cel:
            jelolt = cur + [x]
            legjobb = len(cur)
            elony = _vagas_elonye(cur[-1], x)
            for k in range(1, len(cur)):
                if sum(_hossz(y) for y in cur[:k]) < cel / 2:
                    continue
                e = _vagas_elonye(jelolt[k - 1], jelolt[k])
                if e > elony:
                    legjobb, elony = k, e
            ki.append(cur[:legjobb])
            cur = cur[legjobb:]
            if cur and sum(_hossz(y) for y in cur) + _hossz(x) > cel:
                ki.append(cur)
                cur = []
        cur.append(x)
    if cur:
        ki.append(cur)
    return ki


def strong_magyar_sorok(sorok):
    """A közös összefűző (DT-F128a (a), DT-F128f (3)). sorok: egy Strong `forditasok.tsv`-sorai (dict, a tábla fejlécével),
    egy szótárból, a tábla sorrendjében. -> (szöveg, 'szakasz' | 'teljes' | None, a felhasznált sorok).
      - a nem `elavult` `sz<n>` sorok sorszám szerint, egy szóközzel;
      - de ha van nem `elavult`, `kezi` (jóváhagyott) `teljes` sor, és a szakaszsorok nem mind `kezi`-k, a `kezi` `teljes` sor
        az érvényes (DT-F128f (3): az új szakaszsorok csak jóváhagyás után kapnak `kezi`-t, addig a régi sor él);
      - szakaszsor nélkül a `teljes` sor (nem `elavult` elsőbbséggel; több esetén az utolsó).
    Üres `forditas_hu` nem számít; más `jelentes_szam` (pl. `2.c`, `részlet`) nem a Strong teljes szövege."""
    def fh(r):
        return r.get('mezo', 'forditas_hu') == 'forditas_hu' and (r.get('forditas_hu') or '').strip()
    sz = sorted(((sorszam_jelentesbol(r.get('jelentes_szam')), r) for r in sorok
                 if fh(r) and sorszam_jelentesbol(r.get('jelentes_szam')) is not None and r.get('allapot') != 'elavult'),
                key=lambda p: p[0])
    teljes = [r for r in sorok if fh(r) and r.get('jelentes_szam') == 'teljes']
    elo = [r for r in teljes if r.get('allapot') != 'elavult']
    kezi = [r for r in elo if r.get('allapot') == 'kezi']
    if sz and not (kezi and any(r.get('allapot') != 'kezi' for _, r in sz)):
        return ' '.join(r['forditas_hu'] for _, r in sz), 'szakasz', [r for _, r in sz]
    if kezi:
        return kezi[-1]['forditas_hu'], 'teljes', [kezi[-1]]
    if elo or teljes:
        r = (elo or teljes)[-1]
        return r['forditas_hu'], 'teljes', [r]
    return None, None, []


def strong_magyar(sorok):
    """(szöveg, 'szakasz' | 'teljes' | None) — l. `strong_magyar_sorok`."""
    return strong_magyar_sorok(sorok)[:2]


HU_TABLA = os.path.join(GYOKER, 'adat', 'bdb_szakasz_hu.tsv')


def kesz_magyar_csoportositva(strong):
    """A kész magyar fordítás (`adat/bdb_szakasz_hu.tsv`, 2.32) szakaszai tokenes párként, a kapu próbájához (F128 M3, M4).
    A csoport az `illeszkedik` sornál (és az 1. sornál) kezdődik; a többi sor (`horgonnyal`, `elakad`, `jelolo_nelkul`) a
    megelőző csoportba olvad, mert a magyar szövegének határa nem biztos. -> (forrás tokenes, magyar tokenes, összeolvasztott
    sorok száma) vagy None, ha a Strongnak nincs illesztett magyar szövege vagy szakaszsora."""
    szak = szakaszok(strong)
    if szak is None:
        return None
    if 'hu' not in _CACHE:
        hu = collections.defaultdict(dict)
        for r in _modulok()[1].olvas(HU_TABLA):
            hu[r['strong']][int(r['sorszam'])] = r
        _CACHE['hu'] = hu
    hu = _CACHE['hu'].get(strong)
    if not hu:
        return None
    csop = []
    for x in szak:
        r = hu.get(x['sorszam'])
        if r is None:
            return None
        if not csop or r['kategoria'] == 'illeszkedik':
            csop.append([x['sorszam'], [], []])
        csop[-1][1].append(x['szoveg'])
        if r['szoveg_hu']:
            csop[-1][2].append(r['szoveg_hu'])
    f = '\n'.join('%s %s' % (token(n), ' '.join(a)) for n, a, _ in csop)
    h = '\n'.join('%s %s' % (token(n), ' '.join(b)) for n, _, b in csop)
    return f, h, len(szak) - len(csop)


def ellenoriz():
    """-> (hibák listája, statisztika)."""
    import unicodedata
    hibak, stat = [], collections.Counter()
    tab, _ = _betolt()
    ref, _, _ = _modulok()[1].general(pe_mem=False)
    mem_dag = unicodedata.normalize('NFD', 'מּ')
    pe_dag = unicodedata.normalize('NFD', 'פּ')
    nagy = []
    for st in tab:
        a = szakaszok(st)
        b = szakaszok(st)
        if a != b:
            hibak.append('%s: nem determinisztikus' % st)
        if nezet(a) != ref[st]:
            hibak.append('%s: a token nélküli szöveg eltér a nezet_general.py nézetétől' % st)
        nyers = ' '.join(' '.join(y for y in (x['jel'], x['szoveg']) if y) for x in tab[st])
        for jel in (mem_dag, pe_dag, 'מּ', 'פּ'):
            if unicodedata.normalize('NFD', nezet(a)).count(jel) != unicodedata.normalize('NFD', nyers).count(jel):
                hibak.append('%s: pe/mem eltérés a nyers táblához képest' % st)
                break
        if [int(x['sorszam']) for x in tab[st]] != [x['sorszam'] for x in a]:
            hibak.append('%s: a szakaszsorrend eltér' % st)
        t = tokenes(a)
        if [int(n) for n in TOKEN.findall(t)] != [x['sorszam'] for x in a]:
            hibak.append('%s: a tokenek sorrendje hibás' % st)
        cs = csoportok(a)
        if [x for c in cs for x in c] != a:
            hibak.append('%s: a csoportok nem fedik le a szakaszokat' % st)
        stat['strong'] += 1
        stat['szakasz'] += len(a)
        if len(cs) > 1:
            nagy.append((st, len(nezet(a)), [sum(_hossz(x) for x in c) for c in cs]))
            for c in cs:
                if sum(_hossz(x) for x in c) > CSOPORT_CEL and len(c) > 1:
                    hibak.append('%s: %d karakteres csoport több szakasszal' % (st, sum(_hossz(x) for x in c)))
    stat['tobbcsoportos'] = len(nagy)
    return hibak, stat, nagy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('strong', nargs='?')
    ap.add_argument('--ki')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    if a.ellenoriz:
        hibak, stat, nagy = ellenoriz()
        print('Strong %d, szakasz %d; több csoportos Strong: %d' % (stat['strong'], stat['szakasz'], stat['tobbcsoportos']))
        for st, h, cs in nagy:
            print('  %s %d karakter -> csoportok %s' % (st, h, cs))
        for h in hibak[:50]:
            print('HIBA', h)
        print('RENDBEN' if not hibak else 'HIBA: %d' % len(hibak))
        sys.exit(1 if hibak else 0)
    if not a.strong:
        ap.error('Strong-szám vagy --ellenoriz kell')
    szak = szakaszok(a.strong)
    if szak is None:
        print('%s: nincs a szakasztáblában — a régi `teljes` út (DT-F128d (2))' % a.strong)
        sys.exit(2)
    ki = []
    cs = csoportok(szak)
    for i, c in enumerate(cs):
        if len(cs) > 1:
            ki.append('# csoport %d/%d (%d karakter)' % (i + 1, len(cs), sum(_hossz(x) for x in c)))
        ki.append(tokenes(c))
    szoveg = '\n'.join(ki) + '\n'
    if a.ki:
        with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write(szoveg)
        print('irva: %s (%d szakasz, %d csoport)' % (a.ki, len(szak), len(cs)))
    else:
        sys.stdout.write(szoveg)


if __name__ == '__main__':
    main()
