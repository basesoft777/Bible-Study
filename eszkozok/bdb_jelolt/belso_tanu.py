#!/usr/bin/env python
"""A BDB-digitalizálás pe/mem és rés/dálet hibajelöltjeinek tanús döntése (F185 P4; DT-F185c, DT-F185d).

A `forras_javit.py` hívja (a 2.31 `pe_mem` `jelolt_marad` soraira és az új `res_dalet` osztályra); önállóan csak a
Sefaria-lekérdezendő szavak listáját írja ki (`--sefaria-szavak`).

Egy jelölt pár (hibás = a DictBDB alakja; javított = mem → pe, ill. rés ↔ dálet csere) ítélete:
  1. BELSŐ TANÚ (`tanu=tahot/oshb`): a TAHOT teljes grafikus szavai (elöljáró + tő + szuffixum a tokenhatárok szerint, a maqqéffel
     kapcsolt szópár egybeírva is) és tő-tokenjei, az OSHL lemmái és a Strong-szótár szótövei.
       L1 — a pontos pontozott alak (NFD; kantilláció, meteg, maqqéf, rafe, geresh, sin/sin-pont nélkül; U+05BA = U+05B9):
            csak a javított áll → `javit`; csak a hibás → `marad`; mindkettő vagy egyik sem → `ketes`;
       L2 — a mássalhangzó-váz, csak ha az L1 `ketes`, és a szó legalább 3 mássalhangzós, nem rövidítéstöredék (nincs „׳”).
     (A mérés: a pe/mem 50-es mintán az L1+L2 37 sort dönt el, a Sefariával 24/24 egyezik; a vázszint a töredéken tévedett,
     ezért a töredék kizárva. F185_P0b 7.)
  2. KÜLSŐ TANÚ (`tanu=sefaria-api 2026-11-10`; DT-F185c): csak ahol a belső tanú `ketes`. A Sefaria BDB-szócikke (a
     `/api/words` válasza, a repón KÍVÜLI gyorsítótárból olvasva; a repóba Sefaria-szöveg nem kerül, csak az ítélet) a Strong
     táblaszövegével leginkább átfedő (≥ 0,25) „BDB Dictionary” szócikk; ugyanaz az L1, majd L2 szabály a szócikk héber szavain.
  3. Ha a belső és a külső tanú ellentmond (az egyik `javit`, a másik `marad`), a sor `ketes` marad.
A `marad` csak azt mondja, hogy a hibásnak jelölt alak létező szó; a helyet nem igazolja (a jelölt jelölt marad, a tanú rögzítve).
Ismert gyenge pontok (`ketes`-ként maradnak, nem javít): homográf pár (מִי/פִּי, מָנָה/פָּנָה), elöljáró- és névelő-dages, pauzális
alak, nem bibliai (arámi, újhéber) BDB-alak.

Rés/dálet jelölt (DT-F185d): a 2.30 `szoveg` héber szava (teljes, szuffixumos szóként), amelynek váza (≥ 3 mássalhangzó; a szó
eleji vagy végi rövidítő geres nem számít) a belső tanú vázai között nincs, de egyetlen ר ↔ ד cserével olyan vázat ad, amely a TAHOT teljes szavai között legalább
5-ször áll.

TSV: split('\\t'), csv modul nélkül.
"""
import argparse
import collections
import hashlib
import json
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
GYOKER = os.path.dirname(os.path.dirname(ITT))
TAHOT_UT = os.path.join(GYOKER, 'konkordancia', 'TAHOT_kivonat.tsv')
OSHL_UT = os.path.join(GYOKER, 'konkordancia', 'OSHL_lexikalis_index.tsv')
STRONG_UT = os.path.join(GYOKER, 'konkordancia', 'Strong_szotar.tsv')
SEFARIA_TANU = 'sefaria-api 2026-11-10'
BELSO_TANU = 'tahot/oshb'

HEB = re.compile(r'[֐-׿]+')
CONS = re.compile(r'[א-ת]')
_DROP = set(range(0x0591, 0x05B0)) | {0x05BD, 0x05C0, 0x05C3, 0x200E, 0x05BF, 0x05BE, 0x05C4, 0x05C5, 0x05C6, 0x05F3, 0x05F4,
                                      0x05C1, 0x05C2}
ELOLJARO = {'H9001', 'H9002', 'H9003', 'H9004', 'H9005', 'H9006', 'H9007', 'H9008', 'H9009'}


def nfd(s):
    return unicodedata.normalize('NFD', s)


def norm1(s):
    """L1: a pontozott alak összevetési kulcsa."""
    o = []
    for ch in nfd(s):
        c = ord(ch)
        if c in _DROP:
            continue
        o.append('ֹ' if c == 0x05BA else ch)
    s = ''.join(o).replace('ֹֹ', 'ֹ')
    return nfd(unicodedata.normalize('NFC', s))


def vaz(s):
    return ''.join(CONS.findall(nfd(s)))


def toredek(s):
    return '׳' in s or "'" in s or len(vaz(s)) < 3


_HALMAZ = None


def tanu_halmaz():
    """(L1-halmaz, L2-halmaz, TAHOT teljes-szó vázgyakoriság)."""
    global _HALMAZ
    if _HALMAZ is not None:
        return _HALMAZ
    t1, w1, vgy = set(), set(), collections.Counter()
    versek = collections.OrderedDict()
    with open(TAHOT_UT, encoding='utf-8') as f:
        for sor in f:
            p = sor.rstrip('\n').split('\t')
            if len(p) < 4 or p[0] == 'Igehely':
                continue
            versek.setdefault(p[0], []).append((p[1], p[2], p[3]))
    for toks in versek.values():
        szavak, maq, elo = [], [], ''
        for st, alak, kiejt in toks:
            a = norm1(alak)
            if not a:
                continue
            if st in ELOLJARO:
                elo += a
                continue
            if st.startswith('H90'):
                if szavak:
                    szavak[-1] += a
                else:
                    elo += a
                continue
            t1.add(a)
            szavak.append(elo + a)
            maq.append(kiejt.rstrip().endswith('-'))
            elo = ''
        for i, w in enumerate(szavak):
            w1.add(w)
            vgy[vaz(w)] += 1
            if maq[i] and i + 1 < len(szavak):
                w1.add(w + szavak[i + 1])
    l1 = set()
    with open(OSHL_UT, encoding='utf-8') as f:
        for sor in f:
            p = sor.rstrip('\n').split('\t')
            if len(p) > 7 and p[0].startswith('H'):
                l1.add(norm1(p[6]))
    with open(STRONG_UT, encoding='utf-8') as f:
        for sor in f:
            p = sor.rstrip('\n').split('\t')
            if len(p) > 2 and p[0].startswith('H'):
                l1.add(norm1(p[1]))
    s1 = t1 | w1 | l1
    _HALMAZ = (s1, set(vaz(x) for x in s1), vgy)
    return _HALMAZ


def _itel(jeloltek, hibas, s1, s2):
    """-> (ítélet, szint): L1, majd (ha kétes, és nem töredék) L2; a `ketes` szintje az utolsó vizsgált szint."""
    j = {norm1(x) for x in jeloltek} - {norm1(hibas)}
    if not j:
        return 'ketes', 'L1'
    ji, hi = any(x in s1 for x in j), norm1(hibas) in s1
    if ji != hi:
        return ('javit' if ji else 'marad'), 'L1'
    if toredek(hibas):
        return 'ketes', 'L1'
    jv = {vaz(x) for x in j} - {vaz(hibas)}
    if not jv:
        return 'ketes', 'L1'
    ji, hi = any(x in s2 for x in jv), vaz(hibas) in s2
    if ji != hi:
        return ('javit' if ji else 'marad'), 'L2'
    return 'ketes', 'L2'


def belso_itelet(jeloltek, hibas):
    s1, s2, _ = tanu_halmaz()
    return _itel(jeloltek, hibas, s1, s2)


# ---------------------------------------------------------------- Sefaria (csak gyorsítótárból)

def _sef_cache(cache, szo):
    fn = os.path.join(cache, hashlib.md5(szo.encode()).hexdigest() + '.json')
    if not os.path.exists(fn):
        return None
    with open(fn, encoding='utf-8') as f:
        return json.load(f)


def _lapit(x, ki):
    if isinstance(x, dict):
        for k in ('definition', 'num'):
            if isinstance(x.get(k), str):
                ki.append(x[k])
        for v in x.values():
            if isinstance(v, (dict, list)):
                _lapit(v, ki)
    elif isinstance(x, list):
        for y in x:
            _lapit(y, ki)
    return ki


def _heber_szavak(szoveg):
    t = nfd(re.sub(r'<[^>]+>', ' ', szoveg)).replace('־', '').replace('ֿ', '')
    return [norm1(m.group(0)) for m in HEB.finditer(t)]


def _fold(x):
    return x.translate(str.maketrans('פףםדר', 'מממרר'))


def sefaria_kerdesek(lemma, jeloltek):
    """A lekérdezendő szavak (pontozott, kantilláció nélkül; legfeljebb 6)."""
    ki = []
    for q in ([lemma] if lemma else []) + sorted(jeloltek):
        q = ''.join(c for c in nfd(q) if not (0x0591 <= ord(c) <= 0x05AF or ord(c) in (0x05BD, 0x05C0, 0x05C3, 0x200E, 0x05F3)))
        q = ''.join(q.replace('ֿ', '').split())
        if len(vaz(q)) >= 2 and q not in ki:
            ki.append(q)
    return ki[:6]


def sefaria_itelet(cache, lemma, strong_szoveg, jeloltek, hibas):
    """-> (ítélet, szint) a gyorsítótárazott Sefaria-válaszokból; ('', '') ha nincs válasz a gyorsítótárban."""
    if not cache or not os.path.isdir(cache):
        return '', ''
    szocikkek, latott, volt = [], set(), False
    for q in sefaria_kerdesek(lemma, jeloltek):
        v = _sef_cache(cache, q)
        if v is None:
            continue
        volt = True
        for e in v if isinstance(v, list) else []:
            if e.get('parent_lexicon') == 'BDB Dictionary' and e.get('rid') not in latott:
                latott.add(e.get('rid'))
                szocikkek.append(e)
    if not volt:
        return '', ''
    a = {_fold(vaz(t)) for t in _heber_szavak(strong_szoveg) if len(vaz(t)) >= 3}
    legjobb = None
    for e in szocikkek:
        tok = _heber_szavak(' '.join(_lapit(e.get('content', {}), [])))
        b = {_fold(vaz(t)) for t in tok if len(vaz(t)) >= 3}
        o = len(a & b) / max(1, len(a)) if a else 0.0
        if legjobb is None or o > legjobb[0]:
            legjobb = (o, tok)
    if legjobb is None or legjobb[0] < 0.25:
        return 'ketes', 'L0'          # nincs illeszthető BDB-szócikk
    tok = legjobb[1]
    return _itel(jeloltek, hibas, set(tok), set(vaz(t) for t in tok))


def osszesit(belso, kulso):
    """A végső ítélet és a tanú: (ítélet, tanú-mező)."""
    b, bsz = belso
    k, ksz = kulso
    if b != 'ketes':
        if k and k != 'ketes' and k != b:
            return 'ketes', '%s:%s:%s; %s:%s:%s; ellentmondás' % (BELSO_TANU, bsz, b, SEFARIA_TANU, ksz, k)
        return b, '%s:%s:%s' % (BELSO_TANU, bsz, b)
    if k and k != 'ketes':
        return k, '%s:%s:%s' % (SEFARIA_TANU, ksz, k)
    return 'ketes', '%s:%s:ketes' % (BELSO_TANU, bsz or 'L1') + ('; %s:%s:ketes' % (SEFARIA_TANU, ksz or 'L0') if k else '')


def rogzitett_itelet(tanu):
    """A korábban rögzített `tanu` mező Sefaria-része (szint, ítélet), vagy ('', ''): a gyorsítótár nélküli újragenerálás ezzel
    tartja meg a Sefaria-ítéletet (SEMA 2.31 `tanu`)."""
    for t in (tanu or '').split(';'):
        r = t.strip().split(':')
        if len(r) == 3 and r[0] == SEFARIA_TANU:
            return r[2], r[1]
    return '', ''


# ---------------------------------------------------------------- rés/dálet jelöltek

def csere(szo, i):
    """A szó i-edik mássalhangzójának ר ↔ ד cseréje (a pontozás marad)."""
    ki, n = [], 0
    for ch in nfd(szo):
        if 'א' <= ch <= 'ת':
            if n == i:
                ch = 'ד' if ch == 'ר' else ('ר' if ch == 'ד' else ch)
            n += 1
        ki.append(ch)
    return ''.join(ki)


def res_dalet_jeloltek(sorok):
    """[(sor, szó-sorszám, szó, javított alak)] a 2.30 soraiból."""
    _s1, s2, vgy = tanu_halmaz()
    ki = []
    for r in sorok:
        szavak = HEB.findall(nfd(r['szoveg']).replace('־', ' '))
        for k, w in enumerate(szavak, 1):
            # a rövidítő geres (׳) a szó elején vagy végén a BDB jele (HAMART H0127 „׳עָפָד”), nem a szó része
            v = vaz(w)
            if len(v) < 3 or toredek(w.strip('׳')) or v in s2:
                continue
            for i, ch in enumerate(v):
                if ch in 'רד':
                    alt = v[:i] + ('ד' if ch == 'ר' else 'ר') + v[i + 1:]
                    if vgy.get(alt, 0) >= 5:
                        ki.append((r, k, w, csere(w, i)))
                        break
    return ki


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sefaria-szavak', metavar='KI', help='a belső tanú után kétes sorok Sefaria-lekérdező szavai (soronként egy)')
    a = ap.parse_args()
    if a.sefaria_szavak:
        sys.path.insert(0, ITT)
        import forras_javit as FJ
        szavak = FJ.sefaria_lekerdezendo()
        with open(a.sefaria_szavak, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(szavak) + '\n')
        print('%d szó: %s' % (len(szavak), a.sefaria_szavak))
    return 0


if __name__ == '__main__':
    sys.exit(main())
