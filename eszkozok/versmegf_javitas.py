"""F117 (VERSMEGF_JAVITAS): a konkordancia/Karoli_versmegfeleltetes.tsv A–D′ osztályú javítása (DT-F117a–e).

A szabály egy helyen él (F91-minta, DT-F117a): a verziózott kézi bemenet a konkordancia/Karoli_versmegfeleltetes_javitas.tsv,
ez a modul alkalmazza. A naplok/KAROLI_KK4_tabla_veglegesit.py az F91-javítás (eszkozok/f91_versmegf_javit.py) UTÁN
importálja és a `javit()`-ot hívja.

A `javit(sorok)`:
  * a bemenet minden sorát alkalmazza: ha a Károli-versnek van sora a táblában, felülírja (`felulir`), ha nincs, pótolja (`potol`);
    a tábla `forras` mezője `szoveg_osszevetes_f117`, a `megjegyzes` a bemenetéből jön (benne a felülírt sor régi értéke);
  * a sorokat a KK4 rendezése szerint (az `igehely_karoli` karakterlánc-sorrendje) illeszti be;
  * a fejlécbe F91-mintájú jegyzetsort tesz (a szabály rögzített dátumával; idempotens);
  * HALMAZ-ŐR: a bemenet kulcsain kívül minden adatsor bájtra azonos marad, sor nem törlődik, az új kulcsok mind a
    bemenetből jönnek; különben AssertionError (megállás, a tábla nem íródik ki).
A bemenet ellenőrzése (`betolt`): 7 oszlop; egyedi kulcs; `forras` = szoveg_osszevetes_f117; osztály-szabály (DT-F117b, DT-F117e):
  KJV: igehely_kjv = Károli-szám, igehely_mt üres; MT: igehely_mt = Károli-szám ≠ igehely_kjv; KEZI: igehely_kjv ≠ Károli-szám,
  kitöltött igehely_mt ≠ Károli-szám (új kombináció, DT-F117e); `;`-os KJV-érték nincs (DT-F91c).

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
# Rögzített időbélyeg: a SZABÁLY dátuma (a DT-F117a–e döntéseié), nem a futásé; így a generátor kimenete determinisztikus.
TS = '2026-10-18'
JEGYZET_ELO = '# F117 javítás'
FEJ = ['igehely_karoli', 'igehely_kjv', 'igehely_mt', 'osztaly', 'forras', 'megjegyzes']
_VERS = re.compile(r'^(.+) (\d+:\d+)$')


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
            assert forras == FORRAS, '%s: forras=%s' % (kk, forras)
            assert kjv and ';' not in kjv, '%s: igehely_kjv=%r' % (kk, kjv)
            assert prov.startswith('scope='), '%s: proveniencia' % kk
            if osz == 'KJV':
                assert kjv == kar and mt == '', '%s: KJV-szabály' % kk
            elif osz == 'MT':
                assert mt == kar and kjv != kar, '%s: MT-szabály' % kk
            elif osz == 'KEZI':
                assert kjv != kar and mt and mt != kar, '%s: KEZI-szabály (DT-F117e)' % kk
            else:
                raise AssertionError('%s: ismeretlen osztály %r' % (kk, osz))
            out[kk] = (kjv, mt, osz, forras, megj)
    return out


def javit(lines, javitas=None, ts=TS, naplo=print):
    """A tábla sorai (sorvég nélkül) -> az új sorok listája. Halmaz-őrrel."""
    jav = betolt() if javitas is None else javitas
    fejsorok, adat, egyeb = [], [], []
    fejlec_idx = None
    for i, ln in enumerate(lines):
        if ln.startswith('#'):
            if not ln.startswith(JEGYZET_ELO):
                fejsorok.append(ln)
            continue
        if fejlec_idx is None and ln:
            assert ln.split('\t') == FEJ, 'a tábla fejléce: %r' % ln
            fejlec_idx = i
            continue
        if ln == '':
            egyeb.append(i)
            continue
        adat.append(ln)
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

    # HALMAZ-ŐR
    for k, ln in regi.items():
        if k not in jav:
            assert uj[k] == ln, 'halmaz-őr: a javító bemeneten kívüli sor változott: %s' % k
    assert set(regi) <= set(uj), 'halmaz-őr: sor törlődött'
    assert set(uj) - set(regi) <= set(jav), 'halmaz-őr: a bemeneten kívüli új kulcs'
    kivul = [k for k in sorted(regi) if k not in jav]
    assert [uj[k] for k in kivul] == [regi[k] for k in kivul]

    db = Counter(v[2] for v in jav.values())
    jegyzet = (JEGYZET_ELO + ' (DT-F117a–e): az A–D′ osztályú táblahibák javítása a verziózott kézi bemenetből '
               '(konkordancia/Karoli_versmegfeleltetes_javitas.tsv, %d sor: KJV %d, MT %d, KEZI %d); a Károli↔KJV pár a '
               'versenkénti szöveg-összevetésből (naplok/F117_itelet.tsv), az igehely_mt a TAHOT↔Macula-MT levezetésből '
               '(naplok/F117_mt_levezetes.tsv); ÚJ KOMBINÁCIÓ (DT-F117e): osztaly=KEZI kitöltött igehely_mt-vel = a Károli-szám '
               'eltér a KJV-től és az MT-től is; forras=%s | forras=eszkozok/versmegf_javitas.py | ts=%s (a szabály dátuma, nem a futásé)'
               % (len(jav), db['KJV'], db['MT'], db['KEZI'], FORRAS, ts))
    ki = fejsorok + [jegyzet, '\t'.join(FEJ)] + uj_adat
    naplo('F117 javítás: felülír %d, pótol %d, változatlan %d | tábla: %d -> %d adatsor' % (
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
