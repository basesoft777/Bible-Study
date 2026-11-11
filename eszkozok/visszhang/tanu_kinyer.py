#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tanu_kinyer.py -- a hatástörténeti szakasz tanúrétegének kinyerő táblája (F183, FELADATOK #183): `adat/visszhang_tanuk.tsv`
(séma: adat/SEMA.md 2.57).

A tanú egy ókori értelmező (egyházatyai vagy rabbinikus), aki a motívum egy Remez/Sod-helyét ugyanazzal a
kapcsolattal olvassa, amelyet a lap leír. Hagyományonként (görög, latin, szír, rabbinikus) helyenként legfeljebb egy.
A keresési találat (a tanúindex, `konkordancia/Tanu_*`, vagy a Chain Lineage Browser) jelölt, nem a lap sora: a lapra csak
ennek a táblának ellenőrzött sora kerül (CLAUDE.md 2. szabály). Három út:

    beolvas  KINYERT.tsv --ellenor MODELL --atnezes ATN.tsv
             a modell-kinyerés (HCF- vagy Sefaria-szöveg alapján, `kinyeres=modell`) sorai: a `kapcsolat` egy mondat,
             saját szavakkal, idézet nélkül. A másik kéz (`--ellenor`: a tényleges modellnév, nem a kinyerőé) soronkénti
             ítélete az átnézés-bemenetben (motivum, igehely, hagyomany, tanu, atnezo, itelet = jo | elvet, megjegyzes); a
             kód az ítéletet nem állítja, csak átírja. Átnézés nélkül vagy elvetve az `ellenorzes` üres (nem renderel).
    cl       SPEC.tsv
             a Chain Lineage Browser tényadat-sorai (`kinyeres=gepi`): a SPEC soronként (motivum, igehely, hagyomany, q,
             szerzo, mu) egy lekérdezést ad; a szkript a `chain_lineage.lekerdez` futásával újra lekérdezi, és csak akkor ír
             sort, ha a megadott szerző és mű a válaszban mindkét magverset idézi. A `kapcsolat` gépi mondat (a lánc
             magversei Károli-alakban); az `ellenorzes` a lekérdezés újrafuttatása (gépi), a válasz szövege nem kerül át.
             A SPEC `tanu_nev` oszlopa (nem kötelező) a szerző magyar névalakja a lapon (Origen → Órigenész).
    ellenoriz
             a tábla szerkezete: oszlopszám, zárt értékek, kulcs-egyediség, hagyományonként helyenként legfeljebb egy
             sor, proveniencia; kilépési kód 1 hibánál.

TSV: split('\\t') / '\\t'.join(), a csv modul nem használható (CLAUDE.md). Írás előtt a régi sorokkal összevetve.
"""
import argparse
import collections
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TABLA = os.path.join(GYOKER, 'adat', 'visszhang_tanuk.tsv')
OSZLOPOK = ['motivum', 'igehely', 'tanu_hely', 'hagyomany', 'tanu', 'mu', 'kor', 'kapcsolat', 'forras', 'forras_url',
            'lekerdezve', 'biblindex', 'kinyeres', 'modell', 'ellenorzes', 'proveniencia']
HAGYOMANYOK = ('gorog', 'latin', 'szir', 'rabbinikus')
FORRASOK = ('hcf', 'sefaria', 'glossa', 'chain_lineage')
KINYERES = ('gepi', 'modell')
FEJ_MEGJ = ('# A hatástörténeti szakasz tanúrétegének kinyerő táblája (F183). Kulcs: motivum + igehely + hagyomany + tanu + '
            'forras. Séma: adat/SEMA.md 2.57. Ellenőrizetlen sor (üres `ellenorzes`) a lapon nem renderel. Szöveget '
            '(idézetet) a tábla nem tartalmaz, csak tényadatot és saját szavas egy mondatot.')


def ma():
    return datetime.date.today().isoformat()


def tsv_olvas(ut):
    if not ut or not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if not s.startswith('#') and s.strip()]
    if not sorok:
        return []
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def kulcs(r):
    return (r['motivum'], r['igehely'], r['hagyomany'], r['tanu'], r['forras'])


def tabla_ir(sorok):
    regi = {kulcs(r): r for r in tsv_olvas(TABLA)}
    sorok = sorted(sorok, key=lambda r: (r['motivum'], r['igehely'], r['hagyomany'], r['tanu']))
    for r in sorok:
        for o in OSZLOPOK:
            if '\t' in r.get(o, '') or '\n' in r.get(o, ''):
                raise SystemExit('HIBA: tab vagy sortörés a mezőben: %s / %s' % (o, kulcs(r)))
    valtozott = [k for k in (kulcs(r) for r in sorok) if k in regi]
    with open(TABLA, 'w', encoding='utf-8', newline='\n') as f:
        f.write(FEJ_MEGJ + '\n' + '\t'.join(OSZLOPOK) + '\n')
        for r in sorok:
            f.write('\t'.join(r.get(o, '') for o in OSZLOPOK) + '\n')
    print('visszhang_tanuk.tsv: %d sor (ebből %d korábban is állt)' % (len(sorok), len(valtozott)))


# --- igehely: STEPBible-alak („gen 3.14”) -> Károli-alak („1Móz 3:14”) ---------------------------------------------
_konyv = None


def karoli_alak(ref):
    global _konyv
    if _konyv is None:
        _konyv = {}
        with open(os.path.join(GYOKER, 'konkordancia', 'Konyv_normalizalo_tabla.tsv'), encoding='utf-8') as f:
            next(f)
            for s in f:
                c = s.rstrip('\n').split('\t')
                if len(c) >= 2:
                    _konyv.setdefault(c[0].lower(), c[1])
                    for alt in (c[3].split(',') if len(c) > 3 else []):
                        if alt.strip():
                            _konyv.setdefault(alt.strip().lower(), c[1])
    m = re.match(r'^\s*([1-3]?[a-z]+)\s+(\d+)\.(\d+)\s*$', ref.lower())
    if not m:
        return None
    k = _konyv.get(m.group(1)) or _konyv.get(m.group(1)[:3])
    return '%s %s:%s' % (k, m.group(2), m.group(3)) if k else None


def atnezes_ellenoriz(sorok):
    hibak, latott = [], collections.Counter()
    for i, r in enumerate(sorok, 1):
        if r.get('itelet') not in ('jo', 'elvet'):
            hibak.append('%d. sor: az ítélet nem jo/elvet' % i)
        if not (r.get('atnezo') or '').strip():
            hibak.append('%d. sor: nincs átnéző' % i)
        if not (r.get('megjegyzes') or '').strip():
            hibak.append('%d. sor: nincs megjegyzés (az ítélet indoka)' % i)
        latott[(r['motivum'], r['igehely'], r['hagyomany'], r['tanu'])] += 1
    hibak += ['a kulcs többször áll: %s' % ' | '.join(k) for k, n in latott.items() if n > 1]
    megj = collections.Counter((r.get('megjegyzes') or '').strip() for r in sorok)
    hibak += ['sablonmondat: ugyanaz a megjegyzés %d sorban' % n for m, n in megj.items() if m and n > 1]
    return hibak


def beolvas(a):
    kinyert = tsv_olvas(a.kinyert)
    atn = tsv_olvas(a.atnezes)
    hibak = atnezes_ellenoriz(atn)
    if hibak:
        raise SystemExit('HIBA: az átnézés-bemenet nem érdemi:\n  ' + '\n  '.join(hibak))
    atnezes = {(r['motivum'], r['igehely'], r['hagyomany'], r['tanu']): r for r in atn}
    meglevo = {kulcs(r): r for r in tsv_olvas(TABLA)}
    uj = []
    for r in kinyert:
        r = {o: (r.get(o) or '').strip() for o in OSZLOPOK}
        if r['hagyomany'] not in HAGYOMANYOK or r['forras'] not in ('hcf', 'sefaria', 'glossa') or r['kinyeres'] != 'modell':
            raise SystemExit('HIBA: zárt érték: %s / %s / %s' % (r['hagyomany'], r['forras'], r['kinyeres']))
        at = atnezes.get((r['motivum'], r['igehely'], r['hagyomany'], r['tanu']))
        if r['modell'] == a.ellenor:
            ok = 'a kinyerő és az ellenőr ugyanaz'
        elif not at or at['itelet'] != 'jo':
            ok = 'nincs kézi átnézés' if not at else 'az átnézés elvetette: %s' % at['megjegyzes']
        elif at['atnezo'] != a.ellenor:
            ok = 'az átnéző nem az ellenőr'
        else:
            ok = None
        r['ellenorzes'] = '' if ok else '%s, %s: kézi átnézés a forrásszövegen (%s)' % (
            a.ellenor, ma(), at['megjegyzes'])
        if ok:
            print('  ELLENŐRIZETLEN: %s %s %s (%s)' % (r['igehely'], r['hagyomany'], r['tanu'], ok))
        uj.append(r)
    kulcsok = {kulcs(r) for r in uj}
    tabla_ir(uj + [r for k, r in meglevo.items() if k not in kulcsok])


def cl(a):
    import chain_lineage as CL
    meglevo = {kulcs(r): r for r in tsv_olvas(TABLA)}
    uj = []
    for s in tsv_olvas(a.spec):
        talalat = [t for t in CL.lekerdez(s['q'], 8) if t[2] == s['szerzo'] and t[3] == s['mu']]
        if not talalat:
            print('  NINCS TALÁLAT (sor nem íródik): %s | %s | %s' % (s['q'], s['szerzo'], s['mu']))
            continue
        fam, mag, szerzo, mu, szazad, nyelv, n_bi = talalat[0]
        versek = [karoli_alak(v) or v for v in mag.split(' ; ')]
        url = CL.csaladok_url(s['q'])
        r = {o: '' for o in OSZLOPOK}
        r.update({
            'motivum': s['motivum'], 'igehely': s['igehely'], 'tanu_hely': '; '.join(versek),
            # a `tanu_nev` a szerző magyar névalakja (a SPEC adja; a lekérdezés a forrás névalakjára illeszt)
            'hagyomany': s['hagyomany'], 'tanu': (s.get('tanu_nev') or '').strip() or szerzo,
            'mu': mu.replace('[BiblIndex] ', ''),
            'kor': '%s. sz.' % szazad, 'forras': 'chain_lineage', 'forras_url': url, 'lekerdezve': ma(),
            'biblindex': 'igen' if mu.startswith('[BiblIndex]') else '',
            'kapcsolat': 'Egy versláncban idézi a következő helyeket: %s.' % ', '.join(versek),
            'kinyeres': 'gepi',
            'ellenorzes': 'gépi: a lekérdezés újrafuttatása (chain_lineage.py), %s; lánccsalád %s' % (ma(), fam),
            'proveniencia': 'scope=chain_lineage q="%s" | forras=%s | ts=%s' % (s['q'], url, ma()),
        })
        uj.append(r)
    kulcsok = {kulcs(r) for r in uj}
    tabla_ir(uj + [r for k, r in meglevo.items() if k not in kulcsok])


def ellenoriz(_a):
    sorok = tsv_olvas(TABLA)
    hibak, hely = [], collections.Counter()
    for r in sorok:
        if len(r) != len(OSZLOPOK):
            hibak.append('oszlopszám: %s' % (kulcs(r),))
            continue
        if r['hagyomany'] not in HAGYOMANYOK or r['forras'] not in FORRASOK or r['kinyeres'] not in KINYERES:
            hibak.append('zárt érték: %s' % (kulcs(r),))
        if not r['proveniencia'].startswith('scope='):
            hibak.append('proveniencia: %s' % (kulcs(r),))
        if not r['kapcsolat']:
            hibak.append('üres kapcsolat: %s' % (kulcs(r),))
        if r['ellenorzes']:
            hely[(r['motivum'], r['igehely'], r['hagyomany'])] += 1
    hibak += ['hagyományonként helyenként több ellenőrzött tanú: %s' % ' | '.join(k) for k, n in hely.items() if n > 1]
    for h in hibak:
        print('HIBA:', h)
    print('visszhang_tanuk.tsv: %d sor, %d hiba' % (len(sorok), len(hibak)))
    return 1 if hibak else 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    al = p.add_subparsers(dest='parancs', required=True)
    b = al.add_parser('beolvas')
    b.add_argument('kinyert')
    b.add_argument('--ellenor', required=True)
    b.add_argument('--atnezes', required=True)
    c = al.add_parser('cl')
    c.add_argument('spec')
    al.add_parser('ellenoriz')
    a = p.parse_args()
    return {'beolvas': beolvas, 'cl': cl, 'ellenoriz': ellenoriz}[a.parancs](a) or 0


if __name__ == '__main__':
    sys.exit(main())
