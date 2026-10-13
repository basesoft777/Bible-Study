"""F94.1 (FELADATOK #94): az 1. és 2. szótövezési minta `strong` oszlopának újraszámítása a repó Károli–Strong
párosításából (`adat/karoli_strong/szavak_<könyv>.tsv`, SEMA 2.20; modell-kimenet, javaslat), a régi
`token_karoli`-ból vett érték helyett.

A minta-sor `pelda_igehely` versében az `alak`-kal egyező Károli-token(ok) (`oldal=hu`; előbb pontos, majd
kisbetűs egyezés) `strong` mezője. Ha az alak a versben többször áll, az első előfordulásé kerül a mezőbe, az
összes előfordulás a listában látszik. Betoldás (nincs eredeti pár): üres `strong`.

Használat:
    python eszkozok/szoto/minta_strong.py            # eltérés-lista (markdown) a standard kimenetre, írás nélkül
    python eszkozok/szoto/minta_strong.py --ir       # a strong oszlop átírása (csak ez a mező változik)"""
import argparse
import datetime
import hashlib
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MINTAK = [os.path.join(REPO, 'adat', 'szoto', 'szoto_minta_1_fejlesztes.tsv'),
          os.path.join(REPO, 'adat', 'szoto', 'szoto_minta_2_fejlesztes.tsv')]
KS = os.path.join(REPO, 'adat', 'karoli_strong')
NORM = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
FAJLNEV = {'1Móz': '1Moz', 'Zsolt': 'Zsolt', 'Ézs': 'Ezs'}


def olvas(p):
    sorok = open(p, encoding='utf-8').read().split('\n')
    if sorok[-1] == '':
        sorok = sorok[:-1]
    i = next(k for k, s in enumerate(sorok) if not s.startswith('#'))
    return sorok[:i], sorok[i].split('\t'), [s.split('\t') for s in sorok[i + 1:]]


_cache = {}


def szavak(konyv):
    if konyv not in _cache:
        p = os.path.join(KS, f'szavak_{FAJLNEV[konyv]}.tsv')
        d = {}
        for s in open(p, encoding='utf-8').read().split('\n'):
            if not s or s.startswith('#') or s.startswith('vers\t'):
                continue
            m = s.split('\t')
            if m[1] == 'hu':
                d.setdefault(m[0], []).append(m)
        _cache[konyv] = (d, hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12])
    return _cache[konyv][0]


def keres(alak, igehely):
    konyv = igehely.split(' ')[0]
    tok = szavak(konyv).get(igehely, [])
    egyezo = [t for t in tok if t[3] == alak] or [t for t in tok if t[3].lower() == alak.lower()]
    return egyezo  # [vers, oldal, sorszam, szo, allapot, partner, strong, bizonyossag, forras]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ir', action='store_true')
    a = ap.parse_args()
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    elteres, ossz, nincs = [], 0, []
    for p in MINTAK:
        meta, fej, rek = olvas(p)
        ix = {n: i for i, n in enumerate(fej)}
        eredeti = [list(r) for r in rek]
        for r in rek:
            ossz += 1
            e = keres(r[ix['alak']], r[ix['pelda_igehely']])
            regi = r[ix['strong']]
            if not e:
                nincs.append((os.path.basename(p)[12], r[ix['alak']], r[ix['pelda_igehely']], regi))
                uj = ''
            else:
                uj = e[0][6] if e[0][4] == 'parositva' else ''
            if uj != regi:
                tobb = '; '.join(f'#{t[2]} {t[4]} {t[6] or "—"} ({t[7]})' for t in e)
                elteres.append((os.path.basename(p)[12], r[ix['alak']], r[ix['pelda_igehely']], regi or '—', uj or '—', tobb or 'nincs ilyen token'))
            r[ix['strong']] = uj
        if a.ir:
            for r0, r1 in zip(eredeti, rek):
                for n in fej:
                    if n != 'strong' and r0[ix[n]] != r1[ix[n]]:
                        sys.exit('HIBA: a strong-on kívül más mező változna')
            prov = (f'# strong: scope=a pelda_igehely verse | forras=adat/karoli_strong/szavak_<könyv>.tsv (modell-kimenet, javaslat; '
                    f'nem ellenőrizve), eszkozok/szoto/minta_strong.py, F94.1 | ts={ts}')
            meta = [m for m in meta if not m.startswith('# strong:')] + [prov]
            with open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write('\n'.join(meta + ['\t'.join(fej)] + ['\t'.join(r) for r in rek]) + '\n')
    if a.ir:
        print(f'átírva: {len(elteres)} strong-mező')
        return
    h = ', '.join(f'szavak_{FAJLNEV[k]}.tsv sha256:{v[1]}' for k, v in sorted(_cache.items()))
    print(f'Az 1–2. minta {ossz} sorából **{len(elteres)}** sor `strong` mezője tér el a repó párosításától '
          f'(ebből {sum(1 for x in elteres if x[4] == "—")} a párosításban betoldás vagy nincs ilyen token: üres lesz); '
          f'a példaversben nem található alak: {len(nincs)}.\n')
    print('| minta | alak | példa | régi (token_karoli) | új (karoli_strong) | a vers azonos alakú tokenjei (sorszám, állapot, Strong, bizonyosság) |')
    print('|---|---|---|---|---|---|')
    for x in elteres:
        print('| ' + ' | '.join(x) + ' |')
    print(f'\nscope=adat/szoto/szoto_minta_1_fejlesztes.tsv + szoto_minta_2_fejlesztes.tsv, a pelda_igehely verse | '
          f'forras=eszkozok/szoto/minta_strong.py + {h} (modell-kimenet, javaslat) | ts={ts}')


if __name__ == '__main__':
    main()
