"""F117 (VERSMEGF_JAVITAS): a konkordancia/Karoli_versmegfeleltetes.tsv A–D′ osztályú javítása (DT-F117a–e).

A szabály egy helyen él (F91-minta, DT-F117a): a verziózott kézi bemenet a konkordancia/Karoli_versmegfeleltetes_javitas.tsv,
ez a modul alkalmazza. A naplok/KAROLI_KK4_tabla_veglegesit.py az F91-javítás (eszkozok/f91_versmegf_javit.py) UTÁN
importálja és a `javit()`-ot hívja.

A `javit(sorok)`:
  * a bemenet minden sorát alkalmazza: ha a Károli-versnek van sora a táblában, felülírja (`felulir`), ha nincs, pótolja (`potol`);
    a tábla `forras` mezője `szoveg_osszevetes_f117`, a `megjegyzes` a bemenetéből jön (benne a felülírt sor régi értéke);
  * a sorokat a KK4 rendezése szerint (az `igehely_karoli` karakterlánc-sorrendje) illeszti be;
  * a fejlécbe F91-mintájú jegyzetsort tesz (a szabály rögzített dátumával; idempotens);
  * HALMAZ-ŐR (`halmaz_or`, F117.8 (8)): a KÉSZ kimeneti sorokat függetlenül újraolvassa és a bemeneti táblával veti
    össze: a javító kulcsokon kívül minden adatsor bájtra azonos, sor nem törlődik, idegen kulcs nem jelenik meg, a
    nem-F117 fejlécsorok és az oszlopfej változatlan; eltérésnél HalmazOrHiba (megállás, a tábla nem íródik ki);
  * üres sor a tábla belsejében: kimondott hiba (UresSorHiba); a záró üres sor (a fájlvégi sorvég) megengedett.
A bemenet ellenőrzése (`betolt`): 7 oszlop; egyedi kulcs; `forras` = szoveg_osszevetes_f117 vagy macula_mt_f146; osztály-szabály
(DT-F117b, DT-F117e): KJV: igehely_kjv = Károli-szám, igehely_mt üres; MT: igehely_mt = Károli-szám ≠ igehely_kjv; KEZI:
igehely_kjv ≠ Károli-szám, kitöltött igehely_mt ≠ Károli-szám (új kombináció, DT-F117e); `;`-os KJV-érték nincs (DT-F91c).
F146 (DT-F146b): a `forras=macula_mt_f146` sorokban a KEZI a Károli = KJV ≠ MT esetet is jelenti (a Jóel 2:28–3:21 → MT 3:1–4:21):
kitöltött igehely_mt ≠ Károli-szám, az igehely_kjv lehet a Károli-szám. Az F146-soroknak saját fejléc-jegyzetük van.

Önállóan: python eszkozok/versmegf_javitas.py   (csak mér: a repó tábláján a javítás hatása; nem ír)
Írás '\\t'.join, olvasás split('\\t') (a csv modul tilos).
"""
import os
import re
import sys
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLA = os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')
JAVITAS = os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes_javitas.tsv')
FORRAS = 'szoveg_osszevetes_f117'
FORRAS_F146 = 'macula_mt_f146'
# Rögzített időbélyeg: a SZABÁLY dátuma (a DT-F117a–e döntéseié), nem a futásé; így a generátor kimenete determinisztikus.
TS = '2026-10-18'
TS_F146 = '2026-10-28'   # a DT-F146b dátuma
JEGYZET_ELO = '# F117 javítás'
JEGYZET_F146 = '# F146 javítás'
JEGYZETEK = (JEGYZET_ELO, JEGYZET_F146)
FEJ = ['igehely_karoli', 'igehely_kjv', 'igehely_mt', 'osztaly', 'forras', 'megjegyzes']
_VERS = re.compile(r'^(.+) (\d+:\d+)$')


class HalmazOrHiba(AssertionError):
    """A javító bemenet kulcsain kívüli változás (F117.8 (8))."""


class UresSorHiba(AssertionError):
    """Üres sor a tábla belsejében (F117.8 (8))."""


def _bont(lines):
    """-> (nem-F117 fejlécsorok, oszlopfej, {kulcs: sor}); kettős kulcsnál és belső üres sornál hiba."""
    sorok = list(lines)
    while sorok and sorok[-1] == '':
        sorok.pop()                      # a fájlvégi sorvég (záró üres sor) megengedett
    fej, oszlop, adat = [], None, {}
    for i, ln in enumerate(sorok):
        if ln == '':
            raise UresSorHiba('üres sor a tábla belsejében (%d. sor)' % (i + 1))
        if ln.startswith('#'):
            if not ln.startswith(JEGYZETEK):
                fej.append(ln)
            continue
        if oszlop is None:
            oszlop = ln
            continue
        k = ln.split('\t')[0]
        if k in adat:
            raise HalmazOrHiba('kettős kulcs: %s' % k)
        adat[k] = ln
    return fej, oszlop, adat


def halmaz_or(be_sorok, ki_sorok, jav_kulcsok):
    """A valódi halmaz-őr: a kimenet (ki_sorok) a bemenethez (be_sorok) képest csak a jav_kulcsok soraiban térhet el."""
    bf, bo, ba = _bont(be_sorok)
    kf, ko, ka = _bont(ki_sorok)
    jav = set(jav_kulcsok)
    if bf != kf:
        raise HalmazOrHiba('a nem-F117 fejlécsorok változtak')
    if bo != ko:
        raise HalmazOrHiba('az oszlopfej változott: %r -> %r' % (bo, ko))
    torolt = [k for k in ba if k not in ka]
    if torolt:
        raise HalmazOrHiba('sor törlődött: %s' % torolt[:5])
    idegen = [k for k in ka if k not in ba and k not in jav]
    if idegen:
        raise HalmazOrHiba('a javító bemeneten kívüli új kulcs: %s' % idegen[:5])
    valt = [k for k in ba if k not in jav and ka[k] != ba[k]]
    if valt:
        raise HalmazOrHiba('a javító bemeneten kívüli sor változott: %s' % valt[:5])
    hiany = [k for k in jav if k not in ka]
    if hiany:
        raise HalmazOrHiba('a javító bemenet sora hiányzik a kimenetből: %s' % hiany[:5])
    return len(ka)


def betolt(path=JAVITAS):
    """-> {igehely_karoli: (igehely_kjv, igehely_mt, osztaly, forras, megjegyzes)}, ellenőrzéssel."""
    out = {}
    fej = None
    with open(path, encoding='utf-8') as f:
        for s in f:
            s = s.rstrip('\n').rstrip('\r')
            if not s or s.startswith('#'):
                continue
            p = s.split('\t')
            if fej is None:
                fej = p
                assert fej == FEJ + ['proveniencia'], 'a javító bemenet fejléce: %s' % fej
                continue
            assert len(p) == 7, 'oszlopszám: %r' % s[:80]
            kk, kjv, mt, osz, forras, megj, prov = p
            m = _VERS.match(kk)
            assert m, 'igehely: %r' % kk
            kar = m.group(2)
            assert kk not in out, 'kettős kulcs: %s' % kk
            assert forras in (FORRAS, FORRAS_F146), '%s: forras=%s' % (kk, forras)
            assert kjv and ';' not in kjv, '%s: igehely_kjv=%r' % (kk, kjv)
            assert prov.startswith('scope='), '%s: proveniencia' % kk
            if osz == 'KJV':
                assert kjv == kar and mt == '', '%s: KJV-szabály' % kk
            elif osz == 'MT':
                assert mt == kar and kjv != kar, '%s: MT-szabály' % kk
            elif osz == 'KEZI' and forras == FORRAS_F146:
                assert mt and mt != kar, '%s: KEZI-szabály (DT-F146b)' % kk
            elif osz == 'KEZI':
                assert kjv != kar and mt and mt != kar, '%s: KEZI-szabály (DT-F117e)' % kk
            else:
                raise AssertionError('%s: ismeretlen osztály %r' % (kk, osz))
            out[kk] = (kjv, mt, osz, forras, megj)
    return out


def javit(lines, javitas=None, ts=TS, naplo=print):
    """A tábla sorai (sorvég nélkül) -> az új sorok listája. Halmaz-őrrel."""
    jav = betolt() if javitas is None else javitas
    fejsorok, oszlop, _ = _bont(lines)     # belső üres sor: UresSorHiba (nem hagyjuk el szó nélkül)
    assert oszlop is not None and oszlop.split('\t') == FEJ, 'a tábla fejléce: %r' % oszlop
    adat = [ln for ln in lines if ln and not ln.startswith('#') and ln != oszlop]
    regi = {}
    for ln in adat:
        k = ln.split('\t')[0]
        assert k not in regi, 'kettős kulcs a táblában: %s' % k
        regi[k] = ln
    kulcsok = [ln.split('\t')[0] for ln in adat]
    assert kulcsok == sorted(kulcsok), 'a tábla nincs igehely_karoli szerint rendezve'

    uj = dict(regi)
    stat = Counter()
    for k, (kjv, mt, osz, forras, megj) in jav.items():
        sor = '\t'.join([k, kjv, mt, osz, forras, megj])
        if k in regi:
            stat['felulir' if regi[k] != sor else 'valtozatlan'] += 1
        else:
            stat['potol'] += 1
        uj[k] = sor
    uj_adat = [uj[k] for k in sorted(uj)]

    f117 = {k: v for k, v in jav.items() if v[3] == FORRAS}
    f146 = {k: v for k, v in jav.items() if v[3] == FORRAS_F146}
    db = Counter(v[2] for v in f117.values())
    jegyzet = (JEGYZET_ELO + ' (DT-F117a–e): az A–D′ osztályú táblahibák javítása a verziózott kézi bemenetből '
               '(konkordancia/Karoli_versmegfeleltetes_javitas.tsv, %d sor: KJV %d, MT %d, KEZI %d); a Károli↔KJV pár a '
               'versenkénti szöveg-összevetésből (naplok/F117_itelet.tsv), az igehely_mt a TAHOT↔Macula-MT levezetésből '
               '(naplok/F117_mt_levezetes.tsv); ÚJ KOMBINÁCIÓ (DT-F117e): osztaly=KEZI kitöltött igehely_mt-vel = a Károli-szám '
               'eltér a KJV-től és az MT-től is; forras=%s | forras=eszkozok/versmegf_javitas.py | ts=%s (a szabály dátuma, nem a futásé)'
               % (len(f117), db['KJV'], db['MT'], db['KEZI'], FORRAS, ts))
    jegyzetek = [jegyzet]
    if f146:
        jegyzetek.append(
            JEGYZET_F146 + ' (DT-F146b): a Jóel Károli 2:28–3:21 MT-megfeleltetése (MT 3:1–4:21) a verziózott kézi bemenetből '
            '(konkordancia/Karoli_versmegfeleltetes_javitas.tsv, %d sor, mind KEZI); ÚJ ESET: osztaly=KEZI kitöltött igehely_mt-vel '
            'akkor is, ha a Károli-szám = a KJV-szám ≠ az MT-szám; az igehely_mt a TAHOT↔Macula-MT mérésből (naplok/F146_mt_felmeres.tsv); '
            'forras=%s | forras=eszkozok/versmegf_javitas.py | ts=%s (a szabály dátuma, nem a futásé)' % (len(f146), FORRAS_F146, TS_F146))
    ki = fejsorok + jegyzetek + ['\t'.join(FEJ)] + uj_adat
    halmaz_or(lines, ki, jav.keys())       # a valódi halmaz-őr a kész kimeneten (F117.8 (8))
    naplo('javítás (F117+F146): felülír %d, pótol %d, változatlan %d | tábla: %d -> %d adatsor' % (
        stat['felulir'], stat['potol'], stat['valtozatlan'], len(regi), len(uj_adat)))
    pv = [l for l in uj_adat if ';' in l.split('\t')[1]]
    assert not pv, '`;`-os igehely_kjv a táblában: %s' % pv[:3]
    return ki


def rows(path):
    with open(path, encoding='utf-8', newline='') as f:
        data = f.read()
    return data.split('\n')


if __name__ == '__main__':
    sorok = rows(TABLA)
    if sorok and sorok[-1] == '':
        sorok = sorok[:-1]
    uj = javit(sorok)
    print('mérés: %d -> %d sor (nem ír)' % (len(sorok), len(uj)))
