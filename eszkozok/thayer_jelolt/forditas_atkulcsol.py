#!/usr/bin/env python
"""A Thayer-fordítássorok átkulcsolása a szakasztábla újraszámozása után (F186, DT-F186b (b), orkesztrátori döntés, 2026-11-10).

Az F186 a bekezdésen belüli fejnél kettévágja a bekezdést (`bont.py`, K1), ezért az érintett szócikkekben a szakaszok
`sorszam`-a eltolódik. Az `adat/forditasok.tsv` Thayer-sorai (`szotar = Thayer`, `mezo = forditas_hu`, `jelentes_szam =
sz<n>`, nem `elavult`) a régi sorszámon állnak. A szabály soronként:

  * **változatlan** — a `forras_hash` a mai `sz<n>` szakasz hash-e (`thayer_bemenet.szakaszok`): nincs teendő;
  * **átkulcsolás** — a `forras_hash` a Strong mai szakaszai között **pontosan egy** szakasz hash-e (bájtazonos
    forrásszöveg, máshol): `jelentes_szam` sz<n> → sz<m>, a `forras_hash` és a fordítás változatlan;
  * **elavult** — különben (a szöveg megváltozott, vagy a hash többértelmű): `allapot = elavult`, és a sor a forrásbekezdés
    új kezdő szakaszának kulcsára kerül (sz<a régi n. bekezdés első mai szakasza>; a régi `sz<n>` a bekezdés sorszáma volt).
    Ezen a kulcson érvényes fordítás nem állhat, mert annak a szakasznak a szövege új, így kulcsütközés nincs.
A `megjegyzes` mindkét változásnál kiegészül (proveniencia). `kezi` sor nem lehet `elavult` (megáll).

Írás bájtőrző (az `eszkozok/igazolas_migracio.py` mintája): a módosított sorokon kívül minden sor bájtra azonos, írás előtt
összevetve; a kulcsok egyedisége az írás előtt ellenőrizve. Alapmódban csak terv (írás nélkül); `--ir` ír.
  python eszkozok/thayer_jelolt/forditas_atkulcsol.py [--ir] [--lista KI.tsv] [--datum 2026.11.10]
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
if ITT not in sys.path:
    sys.path.insert(0, ITT)
import bont  # noqa: E402
import kulcs  # noqa: E402
import thayer_bemenet as TB  # noqa: E402

FORDITASOK_UT = os.path.join(bont.GYOKER, 'adat', 'forditasok.tsv')
SZ = re.compile(r'^sz(\d+)$')


def bekezdes_elso(strong, lex=None):
    """{régi bekezdés-sorszám: a bekezdés első mai szakaszának sorszáma} a Strongra."""
    lex = lex if lex is not None else bont.lexikon_beolvas()
    ki = {}
    # az F186.9 köre az összevonás (ELLENOR_F186_2 1–2.) előtti szerkezeten futott: ez az út változatlanul azt használja
    for i, x in enumerate(bont.szerkezet(lex[strong][1], osszevonas=False), 1):
        ki.setdefault(x['bekezdes'], i)
    return ki


def osszevonas_terkep(strong, lex=None):
    """{összevonás előtti szakasz-sorszám: összevont szakasz-sorszám} a Strongra (ELLENOR_F186_2 1–2.; `bont.osszevon` szabálya)."""
    lex = lex if lex is not None else bont.lexikon_beolvas()
    ki, m, elozo = {}, 0, None
    for i, x in enumerate(bont.szerkezet(lex[strong][1], osszevonas=False), 1):
        if not (elozo is not None and x['utvonal'] == elozo and x['utvonal'] != 'cim'):
            m += 1
        ki[i] = m
        elozo = x['utvonal']
    return ki


OSSZEVONAS_JEGY = 'azonos útvonalú szakaszok összevonása'


def terv_osszevonas(sorok, szakaszok, terkep):
    """A második kör (ELLENOR_F186_2 1–2.): a szakaszok összevonása után. sorok: [(sorindex, {mezők})]; szakaszok(sp) -> a mai
    (összevont) szakaszok; terkep(sp) -> {régi sorszám: új sorszám}. Soronként, a régi kulcs új csoportja szerint:
      * a csoportba egy régi sor esik: nem `elavult` sor azonos hash-sel -> `atkulcsol` (vagy változatlan, ha a kulcs sem
        változik); nem `elavult`, eltérő hash -> `elavult`; `elavult` sor -> csak a kulcsa követi a térképet (`athelyez`);
      * a csoportba több régi sor esik (összevont szakasz): az új kulcson egy összefűzött sor áll, a fordítások sorrendben
        egy szóközzel fűzve (`osszefuz`); a régi sorok nem törlődnek, hanem `elavult` tagsorként `sz<új>~<régi>` kulcsot
        kapnak, és az összefűzött sorra mutatnak (SEMA 2.14, DT-F186f). `kezi` sor nem avulhat el (megáll).
    -> [{'i', 'strong', 'regi', 'uj', 'tipus', 'tagok'}]"""
    csoport = collections.defaultdict(list)
    for i, r in sorok:
        if r.get('szotar') == 'Thayer' and r.get('mezo') == 'forditas_hu' and SZ.match(r.get('jelentes_szam', '')):
            csoport[kulcs.strong_pad(r['strong'])].append((i, r))
    ki = []
    for sp in sorted(csoport):
        # egyszeri lépés: a térkép az összevonás előtti számozást feltételezi; a már átkulcsolt Strong kimarad (idempotens)
        if any(OSSZEVONAS_JEGY in (r.get('megjegyzes') or '') for _, r in csoport[sp]):
            continue
        t = terkep(sp)
        hash_itt = {x['sorszam']: x['hash'] for x in (szakaszok(sp) or [])}
        uj_csop = collections.defaultdict(list)
        for i, r in csoport[sp]:
            n = int(SZ.match(r['jelentes_szam']).group(1))
            if n not in t:
                raise SystemExit('%s sz%d: a régi sorszám nincs a térképen — megállok' % (sp, n))
            uj_csop[t[n]].append((n, i, r))
        for m, tagok in sorted(uj_csop.items()):
            tagok.sort()
            if len(tagok) == 1:
                n, i, r = tagok[0]
                if r.get('allapot') == 'elavult':
                    if n != m:
                        ki.append({'i': i, 'strong': sp, 'regi': n, 'uj': m, 'tipus': 'athelyez', 'tagok': []})
                elif hash_itt.get(m) == r.get('forras_hash'):
                    if n != m:
                        ki.append({'i': i, 'strong': sp, 'regi': n, 'uj': m, 'tipus': 'atkulcsol', 'tagok': []})
                else:
                    if r.get('allapot') == 'kezi':
                        raise SystemExit('%s sz%d: védett kezi sor lenne elavult — megállok' % (sp, n))
                    ki.append({'i': i, 'strong': sp, 'regi': n, 'uj': m, 'tipus': 'elavult', 'tagok': []})
                continue
            if any(r.get('allapot') == 'kezi' for _, _, r in tagok):
                raise SystemExit('%s: védett kezi sor egy összevont szakaszban — megállok' % sp)
            n0, i0, _ = tagok[0]
            ki.append({'i': i0, 'strong': sp, 'regi': n0, 'uj': m, 'tipus': 'osszefuz',
                       'tagok': [(n, i, r) for n, i, r in tagok[1:]]})
    return ki


TAGSOR = re.compile(r'^sz(\d+)~(\d+)$')
TAB = chr(9)


def tagsor_kulcs(uj, regi):
    """Az összevont csoport megmaradó tagsorának `jelentes_szam`-a (DT-F186f, SEMA 2.14): `sz<új>~<régi>` — egyedi kulcs, nem
    `sz<n>` alakú, ezért a szakasz-fogyasztók (lefedés, Strong magyar szövege, szólista) kihagyják."""
    return 'sz%d~%d' % (uj, regi)


def alkalmaz_osszevonas(sorok, fej, valtozasok, datum):
    """-> (új sorlista, üres halmaz); csak a `valtozasok` sorai változnak. Az összevont csoport első sora az összefűzött `elavult` sor
    (a tagsoraira hivatkozik); a többi régi sor nem törlődik (DT289, DT-F186f): `elavult`, `jelentes_szam = sz<új>~<régi>`,
    a jegye az összefűzött sorra mutat."""
    i_jsz, i_all, i_megj, i_hu = (fej.index('jelentes_szam'), fej.index('allapot'), fej.index('megjegyzes'),
                                  fej.index('forditas_hu'))
    uj = list(sorok)
    for v in valtozasok:
        m = uj[v['i']].split(TAB)
        assert m[i_jsz] == 'sz%d' % v['regi']
        m[i_jsz] = 'sz%d' % v['uj']
        if v['tipus'] == 'atkulcsol':
            jegy = 'F186 (%s): átkulcsolva sz%d → sz%d, azonos forras_hash (azonos útvonalú szakaszok összevonása)' % (
                datum, v['regi'], v['uj'])
        elif v['tipus'] == 'athelyez':
            jegy = 'F186 (%s): elavult sor áthelyezve sz%d → sz%d (azonos útvonalú szakaszok összevonása)' % (datum, v['regi'], v['uj'])
        elif v['tipus'] == 'elavult':
            m[i_all] = 'elavult'
            jegy = 'F186 (%s): elavult — a szakasz szövege megváltozott (azonos útvonalú szakaszok összevonása); sz%d → sz%d' % (
                datum, v['regi'], v['uj'])
        else:
            m[i_all] = 'elavult'
            szovegek = [m[i_hu]] + [r['forditas_hu'] for _, _, r in v['tagok']]
            m[i_hu] = ' '.join(x for x in szovegek if x)
            jegy = ('F186 (%s): elavult — azonos útvonalú szakaszok összevonása: sz%s → sz%d; a régi sorok fordítása egy szóközzel '
                    'fűzve, a forras_hash az elsőé; tagsor: %s' % (
                        datum, ', sz'.join(str(n) for n in [v['regi']] + [n for n, _, _ in v['tagok']]), v['uj'],
                        ', '.join(tagsor_kulcs(v['uj'], n) for n, _, _ in v['tagok'])))
            for n, i, _ in v['tagok']:
                t = uj[i].split(TAB)
                assert t[i_jsz] == 'sz%d' % n
                t[i_jsz] = tagsor_kulcs(v['uj'], n)
                t[i_all] = 'elavult'
                t[i_megj] = '; '.join(x for x in (t[i_megj], (
                    'F186 (%s): elavult — azonos útvonalú szakaszok összevonása: tagsor (a régi sz%d); a szövege az sz%d összefűzött '
                    'sorában' % (datum, n, v['uj']))) if x)
                uj[i] = TAB.join(t)
        m[i_megj] = '; '.join(x for x in (m[i_megj], jegy) if x)
        uj[v['i']] = TAB.join(m)
    return uj, set()


def ellenoriz_iras_osszevonas(regi, uj, valtozasok, torol):
    """Írás előtti összevetés: a nem érintett sorok bájtra azonosak és sorrendben maradnak; csak a `torol` sorai esnek ki; a kulcsok
    egyediek."""
    erintett = {v['i'] for v in valtozasok} | {i for v in valtozasok for _, i, _ in v['tagok']}
    maradt = [k for k in range(len(regi)) if k not in torol]
    if len(maradt) != len(uj):
        raise SystemExit('a sorok száma nem a várt — megállok')
    for k, s in zip(maradt, uj):
        if k not in erintett and regi[k] != s:
            raise SystemExit('váratlan eltérés a %d. sorban — megállok' % (k + 1))
    kulcsok = collections.Counter(tuple(s.split('\t')[:5]) for s in uj if s and not s.startswith('#'))
    dupla = [k for k, c in kulcsok.items() if c > 1]
    if dupla:
        raise SystemExit('duplikált kulcs az írás után: %s — megállok' % dupla[:3])


def terv(sorok, szakaszok, elso):
    """sorok: [(sorindex, {mezők})] — a fájl minden adatsora; szakaszok(sp) -> [{sorszam, hash}]; elso(sp) -> {bekezdés: sorszám}.
    -> [{'i', 'strong', 'regi', 'uj', 'tipus'}] (tipus: atkulcsol | elavult); SystemExit, ha a terv nem végrehajtható."""
    csoport = collections.defaultdict(list)
    for i, r in sorok:
        if r.get('szotar') == 'Thayer' and r.get('mezo') == 'forditas_hu' and SZ.match(r.get('jelentes_szam', '')):
            csoport[kulcs.strong_pad(r['strong'])].append((i, r))
    ki = []
    for sp in sorted(csoport):
        aktiv = [(i, r) for i, r in csoport[sp] if r.get('allapot') != 'elavult']
        if not aktiv:
            continue
        sz = szakaszok(sp) or []
        hash_itt = {x['sorszam']: x['hash'] for x in sz}
        hol = collections.defaultdict(list)
        for x in sz:
            hol[x['hash']].append(x['sorszam'])
        valtozas = []
        for i, r in aktiv:
            n = int(SZ.match(r['jelentes_szam']).group(1))
            fh = r.get('forras_hash', '')
            if hash_itt.get(n) == fh:
                continue
            if len(hol.get(fh, [])) == 1:
                valtozas.append({'i': i, 'strong': sp, 'regi': n, 'uj': hol[fh][0], 'tipus': 'atkulcsol'})
                continue
            e = elso(sp)
            if n not in e:
                raise SystemExit('%s sz%d: a régi sorszám nem bekezdés a mai forrásban — megállok' % (sp, n))
            if r.get('allapot') == 'kezi':
                raise SystemExit('%s sz%d: védett kezi sor lenne elavult — megállok' % (sp, n))
            valtozas.append({'i': i, 'strong': sp, 'regi': n, 'uj': e[n], 'tipus': 'elavult'})
        # a végső kulcsok egyedisége a Strongon belül (az elavult sorokkal együtt)
        mozdul = {v['i']: v['uj'] for v in valtozas}
        vegso = collections.Counter()
        for i, r in csoport[sp]:
            vegso[mozdul.get(i, int(SZ.match(r['jelentes_szam']).group(1)))] += 1
        dupla = sorted(k for k, c in vegso.items() if c > 1)
        if dupla:
            raise SystemExit('%s: kulcsütközés a terv után: %s — megállok' % (sp, ['sz%d' % k for k in dupla]))
        for v in valtozas:
            if v['tipus'] == 'atkulcsol':
                assert hash_itt[v['uj']] == dict(csoport[sp])[v['i']]['forras_hash']  # csak azonos hash-nél
        ki.extend(valtozas)
    return ki


# ---------------------------------------------------------------------------------------------------------------------------
# F203 (N125/N126 javítása után; gyökérok-szabály): általános átkulcsolás a RÉGI és a MAI szakasztábla összevetéséből. Az F186
# két köre egy-egy egyszeri, a saját szabályváltozásához kötött térképet használt (`bekezdes_elso`, `osszevonas_terkep`); a
# `bont.py` minden további szabályváltozása újabb egyedi módot kívánna. Ez a mód a változás fajtájától független: a régi
# szakaszt a szócikk szövegében elfoglalt helye szerint a mai szakaszra vetíti (a legnagyobb átfedés), így bármely vágás,
# összevonás vagy újraszámozás után ugyanaz a szabály fut. Használat a `bont.py` bármely változása után, a commit előtt:
#   python eszkozok/thayer_jelolt/forditas_atkulcsol.py --regi-rev HEAD [--ir]
# ---------------------------------------------------------------------------------------------------------------------------
TAGSOR_ALT = re.compile(r'^sz(\d+)~(\d+)$')


def _nows_hossz(s):
    return len(re.sub(r'\s+', '', s or ''))


def intervallumok(szak):
    """[{sorszam, szoveg}] -> {sorszam: (kezdet, vég)} a szócikk szóközök nélküli szövegében (a szakaszok sorban, hézag nélkül)."""
    ki, p = {}, 0
    for x in szak:
        h = _nows_hossz(x['szoveg'])
        ki[x['sorszam']] = (p, p + h)
        p += h
    return ki


def vetites(regi_szak, uj_szak):
    """{régi sorszám: mai sorszám}: a régi szakasz a mai szakaszok közül arra esik, amellyel a szövegben a legnagyobb az átfedése
    (döntetlennél a kisebb sorszám; üres régi szakasznál az, amelyik a kezdőpontját tartalmazza)."""
    ri, ui = intervallumok(regi_szak), intervallumok(uj_szak)
    ki = {}
    for n, (a, b) in ri.items():
        legjobb, atf = None, -1
        for m, (c, d) in ui.items():
            o = min(b, d) - max(a, c)
            if b == a:
                o = 0 if c <= a < d or (a == d and m == max(ui)) else -1
            if o > atf:
                legjobb, atf = m, o
        ki[n] = legjobb
    return ki


def terv_tabla(sorok, regi, mai, datum='', jegy_elotag='F203'):
    """Általános terv. sorok: [(sorindex, {mezők})]; regi(sp) / mai(sp) -> [{sorszam, hash, szoveg}] (a `thayer_bemenet.szakaszok`
    alakja, a régi és a mai táblából). Soronként (Thayer, forditas_hu):
      * nem `elavult`, a hash a mai sz<n>-é: változatlan;
      * nem `elavult`, a hash pontosan egy mai szakaszé: `atkulcsol` (a fordítás és a hash változatlan);
      * nem `elavult`, különben: `elavult`, a kulcs a vetített mai szakasz (`vetites`); `kezi` sor nem avulhat el (megáll);
      * `elavult` sor: a kulcsa a vetítést követi (`athelyez`);
      * `sz<a>~<b>` tagsor: az `a` az sz<a> sor új kulcsát követi.
    Ütközés (egy mai kulcsra több sor): érvényes sor mellé más sor nem kerülhet sz<m> kulcsra — azok `sz<m>~<régi>` tagsorok
    (`elavult`); ha nincs érvényes sor, a legkisebb régi sorszámú kapja az sz<m>-et, a fordítások sorrendben egy szóközzel fűzve
    (DT-F186f mintája, `osszefuz`), a többi tagsor. -> [{'i', 'strong', 'regi', 'uj', 'tipus', 'uj_kulcs', 'hu'}]"""
    csoport = collections.defaultdict(list)
    for i, r in sorok:
        if r.get('szotar') == 'Thayer' and r.get('mezo') == 'forditas_hu' and (
                SZ.match(r.get('jelentes_szam', '')) or TAGSOR_ALT.match(r.get('jelentes_szam', ''))):
            csoport[kulcs.strong_pad(r['strong'])].append((i, r))
    ki = []
    for sp in sorted(csoport):
        rs, ms = regi(sp) or [], mai(sp) or []
        if [(x['hash'], x.get('utvonal')) for x in rs] == [(x['hash'], x.get('utvonal')) for x in ms]:
            continue
        vet = vetites(rs, ms)
        mai_hash = {x['sorszam']: x['hash'] for x in ms}
        hol = collections.defaultdict(list)
        for x in ms:
            hol[x['hash']].append(x['sorszam'])
        cel = {}            # sorindex -> (mai sorszám, érvényes-e, típus)
        fej_uj = {}         # régi sz<n> (fősor) -> mai sorszám
        for i, r in csoport[sp]:
            m = SZ.match(r['jelentes_szam'])
            if not m:
                continue
            n = int(m.group(1))
            if n not in vet:
                raise SystemExit('%s sz%d: a régi sorszám nincs a régi táblában — megállok' % (sp, n))
            fh = r.get('forras_hash', '')
            if r.get('allapot') != 'elavult':
                if mai_hash.get(n) == fh:
                    cel[i] = (n, True, None)
                elif len(hol.get(fh, [])) == 1:
                    cel[i] = (hol[fh][0], True, 'atkulcsol')
                else:
                    if r.get('allapot') == 'kezi':
                        raise SystemExit('%s sz%d: védett kezi sor lenne elavult — megállok' % (sp, n))
                    cel[i] = (vet[n], False, 'elavult')
            else:
                cel[i] = (vet[n], False, 'athelyez' if vet[n] != n else None)
            fej_uj[n] = cel[i][0]
        # ütközések: mai kulcs -> sorok
        kulcson = collections.defaultdict(list)
        for i, r in csoport[sp]:
            if i in cel:
                kulcson[cel[i][0]].append((int(SZ.match(r['jelentes_szam']).group(1)), i, r))
        for m_, tagok in sorted(kulcson.items()):
            tagok.sort()
            ervenyes = [t for t in tagok if cel[t[1]][1]]
            if len(ervenyes) > 1:
                raise SystemExit('%s sz%d: két érvényes fordítás egy szakaszon — megállok' % (sp, m_))
            if ervenyes:
                fo, tobbi = ervenyes[0], [t for t in tagok if t is not ervenyes[0]]
                fo_tipus = cel[fo[1]][2]
                if fo_tipus:
                    ki.append({'i': fo[1], 'strong': sp, 'regi': fo[0], 'uj': m_, 'tipus': fo_tipus,
                               'uj_kulcs': 'sz%d' % m_, 'hu': None})
                for n, i, r in tobbi:
                    ki.append({'i': i, 'strong': sp, 'regi': n, 'uj': m_, 'tipus': 'tagsor', 'uj_kulcs': 'sz%d~%d' % (m_, n),
                               'hu': None, 'fo': 'sz%d' % m_})
                continue
            fo, tobbi = tagok[0], tagok[1:]
            n0, i0, r0 = fo
            if tobbi:
                hu = ' '.join(x for x in [r0.get('forditas_hu', '')] + [r.get('forditas_hu', '') for _, _, r in tobbi] if x)
                ki.append({'i': i0, 'strong': sp, 'regi': n0, 'uj': m_, 'tipus': 'osszefuz', 'uj_kulcs': 'sz%d' % m_, 'hu': hu,
                           'tagok': ['sz%d~%d' % (m_, n) for n, _, _ in tobbi]})
                for n, i, r in tobbi:
                    ki.append({'i': i, 'strong': sp, 'regi': n, 'uj': m_, 'tipus': 'tagsor', 'uj_kulcs': 'sz%d~%d' % (m_, n),
                               'hu': None, 'fo': 'sz%d' % m_})
            elif cel[i0][2]:
                ki.append({'i': i0, 'strong': sp, 'regi': n0, 'uj': m_, 'tipus': cel[i0][2], 'uj_kulcs': 'sz%d' % m_, 'hu': None})
        # a meglévő tagsorok (sz<a>~<b>) a fősoruk új kulcsát követik
        for i, r in csoport[sp]:
            t = TAGSOR_ALT.match(r['jelentes_szam'])
            if t and int(t.group(1)) in fej_uj and fej_uj[int(t.group(1))] != int(t.group(1)):
                a_uj = fej_uj[int(t.group(1))]
                ki.append({'i': i, 'strong': sp, 'regi': int(t.group(1)), 'uj': a_uj, 'tipus': 'tagsor_kovet',
                           'uj_kulcs': 'sz%d~%s' % (a_uj, t.group(2)), 'hu': None, 'regi_kulcs': r['jelentes_szam']})
    return ki


def alkalmaz_tabla(sorok, fej, valtozasok, datum, elotag='F203'):
    """-> az új sorlista; csak a `valtozasok` sorai változnak (a sorok száma és sorrendje marad)."""
    i_jsz, i_all, i_megj, i_hu = (fej.index('jelentes_szam'), fej.index('allapot'), fej.index('megjegyzes'),
                                  fej.index('forditas_hu'))
    uj = list(sorok)
    for v in valtozasok:
        m = uj[v['i']].split(TAB)
        regi_kulcs = m[i_jsz]
        m[i_jsz] = v['uj_kulcs']
        t = v['tipus']
        if t == 'atkulcsol':
            jegy = '%s (%s): átkulcsolva %s → %s, azonos forras_hash (szakasztábla-változás)' % (elotag, datum, regi_kulcs, v['uj_kulcs'])
        elif t == 'athelyez':
            jegy = '%s (%s): elavult sor áthelyezve %s → %s (szakasztábla-változás)' % (elotag, datum, regi_kulcs, v['uj_kulcs'])
        elif t == 'elavult':
            m[i_all] = 'elavult'
            jegy = '%s (%s): elavult — a szakasz szövege megváltozott (szakasztábla-változás); %s → %s' % (
                elotag, datum, regi_kulcs, v['uj_kulcs'])
        elif t == 'osszefuz':
            m[i_all] = 'elavult'
            m[i_hu] = v['hu']
            jegy = ('%s (%s): elavult — a szakaszok egy mai szakaszba estek (szakasztábla-változás): %s → %s; a fordítások '
                    'egy szóközzel fűzve, a forras_hash az elsőé; tagsor: %s' % (elotag, datum, regi_kulcs, v['uj_kulcs'],
                                                                               ', '.join(v['tagok'])))
        elif t == 'tagsor':
            m[i_all] = 'elavult'
            jegy = '%s (%s): elavult tagsor (a régi %s); a szakasz mai kulcsa %s' % (elotag, datum, regi_kulcs, v['fo'])
        else:  # tagsor_kovet
            jegy = '%s (%s): tagsor áthelyezve %s → %s (a fősor új kulcsa)' % (elotag, datum, regi_kulcs, v['uj_kulcs'])
        m[i_megj] = '; '.join(x for x in (m[i_megj], jegy) if x)
        uj[v['i']] = TAB.join(m)
    return uj


def regi_tabla_gitbol(rev, ut='adat/thayer_szakaszok.tsv'):
    """A `rev` commit `ut` táblája (alapból a szakasztábla) egy ideiglenes fájlba (a régi tábla a `--regi-rev` módhoz)."""
    import subprocess
    import tempfile
    o = subprocess.run(['git', 'show', '%s:%s' % (rev, ut)], cwd=bont.GYOKER, capture_output=True)
    if o.returncode:
        raise SystemExit('a régi tábla nem olvasható (%s): %s' % (rev, o.stderr.decode('utf-8', 'replace')[:200]))
    f = tempfile.NamedTemporaryFile('wb', suffix='.tsv', delete=False)
    f.write(o.stdout)
    f.close()
    return f.name


def beolvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        szoveg = f.read()
    assert szoveg.endswith('\n'), 'a forditasok.tsv nem sortöréssel végződik'
    sorok = szoveg.split('\n')[:-1]
    fej_i = next(i for i, s in enumerate(sorok) if s and not s.startswith('#'))
    fej = sorok[fej_i].split('\t')
    adat = [(i, dict(zip(fej, s.split('\t')))) for i, s in enumerate(sorok) if i > fej_i and s and not s.startswith('#')]
    return szoveg, sorok, fej, adat


def alkalmaz(sorok, fej, valtozasok, datum):
    """-> az új sorlista; csak a `valtozasok` sorai változnak."""
    i_jsz, i_all, i_megj = fej.index('jelentes_szam'), fej.index('allapot'), fej.index('megjegyzes')
    uj = list(sorok)
    for v in valtozasok:
        m = uj[v['i']].split('\t')
        assert m[i_jsz] == 'sz%d' % v['regi']
        m[i_jsz] = 'sz%d' % v['uj']
        # A megjegyzés szövege bájtra az, amit az F186.9 a forditasok.tsv-be írt (ELLENOR_F186 2e): a helyőrzőt az adatban a
        # szamkiosztas merge-kor cseréli, a .py-ban nem; ezért a két sor szándékosan történeti literál (e32-kihagy).
        if v['tipus'] == 'atkulcsol':
            jegy = 'F186 (%s): átkulcsolva sz%d → sz%d, azonos forras_hash (a szakaszok újraszámozása; DT-F186b)' % (datum, v['regi'], v['uj'])  # e32-kihagy
        else:
            m[i_all] = 'elavult'
            jegy = ('F186 (%s): elavult — a forrásbekezdés szövege a szakasztáblában megváltozott (bekezdésen belüli fej vagy hamis '
                    'fej); sz%d → sz%d, a bekezdés új kezdő szakasza (DT-F186b)' % (datum, v['regi'], v['uj']))  # e32-kihagy
        m[i_megj] = '; '.join(x for x in (m[i_megj], jegy) if x)
        uj[v['i']] = '\t'.join(m)
    return uj


def ellenoriz_iras(regi, uj, valtozasok, fej):
    """Írás előtti összevetés: a nem módosított sorok bájtra azonosak, a sorszám és a mezőszám változatlan, a kulcsok egyediek."""
    if len(regi) != len(uj):
        raise SystemExit('a sorok száma változna — megállok')
    erintett = {v['i'] for v in valtozasok}
    for i, (a, b) in enumerate(zip(regi, uj)):
        if i not in erintett and a != b:
            raise SystemExit('váratlan eltérés a %d. sorban — megállok' % (i + 1))
        if i in erintett and len(a.split('\t')) != len(b.split('\t')):
            raise SystemExit('mezőszám-eltérés a %d. sorban — megállok' % (i + 1))
    kulcsok = collections.Counter(tuple(s.split('\t')[:5]) for s in uj if s and not s.startswith('#'))
    dupla = [k for k, c in kulcsok.items() if c > 1]
    if dupla:
        raise SystemExit('duplikált kulcs az írás után: %s — megállok' % dupla[:3])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    ap.add_argument('--lista')
    ap.add_argument('--datum', default='2026.11.10')
    ap.add_argument('--forditasok', default=FORDITASOK_UT)
    ap.add_argument('--osszevonas', action='store_true',
                    help='a második kör (ELLENOR_F186_2 1–2.): az azonos útvonalú szakaszok összevonása utáni átkulcsolás')
    ap.add_argument('--regi-tabla', help='F203: általános mód — a régi thayer_szakaszok.tsv útja')
    ap.add_argument('--regi-rev', help='F203: általános mód — a régi tábla ebből a git-commitból (pl. HEAD)')
    a = ap.parse_args()
    szoveg, sorok, fej, adat = beolvas(a.forditasok)
    if a.regi_tabla or a.regi_rev:
        regi_ut = a.regi_tabla or regi_tabla_gitbol(a.regi_rev)
        # a régi táblához a régi javítótábla tartozik (a `sorszam`-a a régi számozásé)
        regi_jav = regi_tabla_gitbol(a.regi_rev, 'adat/thayer_forras_javitas.tsv') if a.regi_rev else None
        v = terv_tabla(adat, lambda sp: TB.szakaszok(sp, regi_ut, regi_jav), TB.szakaszok)
        db = collections.Counter(x['tipus'] for x in v)
        print('általános mód (régi tábla: %s): %s; érintett Strong: %d' % (
            a.regi_tabla or a.regi_rev, ', '.join('%s %d' % kv for kv in sorted(db.items())) or 'nincs teendő',
            len({x['strong'] for x in v})))
        if a.lista:
            with open(a.lista, 'w', encoding='utf-8', newline='\n') as f:
                f.write('strong\tregi\tuj_kulcs\ttipus\n')
                for x in v:
                    f.write('%s\t%s\t%s\t%s\n' % (x['strong'], x.get('regi_kulcs') or 'sz%d' % x['regi'], x['uj_kulcs'], x['tipus']))
        uj = alkalmaz_tabla(sorok, fej, v, a.datum)
        ellenoriz_iras(sorok, uj, v, fej)
        if not a.ir:
            print('terv (írás nélkül); --ir ír')
            return 0
        with open(a.forditasok, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(uj) + '\n')
        print('írva: %s' % a.forditasok)
        return 0
    lex = bont.lexikon_beolvas()
    if a.osszevonas:
        v = terv_osszevonas(adat, TB.szakaszok, lambda sp: osszevonas_terkep(sp, lex))
        db = collections.Counter(x['tipus'] for x in v)
        print('átkulcsolás: %d; elavult: %d; összefűzött (elavult): %d, ebből tagsor (elavult, megmarad): %d; áthelyezett elavult: %d; '
              'érintett Strong: %d' % (db['atkulcsol'], db['elavult'], db['osszefuz'], sum(len(x['tagok']) for x in v),
                                       db['athelyez'], len({x['strong'] for x in v})))
        if a.lista:
            with open(a.lista, 'w', encoding='utf-8', newline='\n') as f:
                f.write('strong\tregi\tuj\ttipus\ttagok\n')
                for x in v:
                    f.write('%s\tsz%d\tsz%d\t%s\t%s\n' % (x['strong'], x['regi'], x['uj'], x['tipus'],
                                                          ','.join('sz%d' % n for n, _, _ in x['tagok'])))
        uj, torol = alkalmaz_osszevonas(sorok, fej, v, a.datum)
        ellenoriz_iras_osszevonas(sorok, uj, v, torol)
        if not a.ir:
            print('terv (írás nélkül); --ir ír')
            return 0
        with open(a.forditasok, 'w', encoding='utf-8', newline='') as f:
            f.write('\n'.join(uj) + '\n')
        print('írva: %s' % a.forditasok)
        return 0
    v = terv(adat, TB.szakaszok, lambda sp: bekezdes_elso(sp, lex))
    db = collections.Counter(x['tipus'] for x in v)
    print('átkulcsolás: %d; elavult: %d; érintett Strong: %d' % (db['atkulcsol'], db['elavult'], len({x['strong'] for x in v})))
    if a.lista:
        with open(a.lista, 'w', encoding='utf-8', newline='\n') as f:
            f.write('strong\tregi\tuj\ttipus\n')
            for x in v:
                f.write('%s\tsz%d\tsz%d\t%s\n' % (x['strong'], x['regi'], x['uj'], x['tipus']))
    uj = alkalmaz(sorok, fej, v, a.datum)
    ellenoriz_iras(sorok, uj, v, fej)
    if not a.ir:
        print('terv (írás nélkül); --ir ír')
        return 0
    with open(a.forditasok, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(uj) + '\n')
    print('írva: %s' % a.forditasok)
    return 0


if __name__ == '__main__':
    sys.exit(main())
