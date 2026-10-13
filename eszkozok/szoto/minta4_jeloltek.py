"""F94.3/1 (FELADATOK #94): a negyedik, független szótövezési minta alakjainak mintavétele — a hibrid v3
befagyasztása UTÁN, a hibrid futtatása NÉLKÜL.

Forrás: `konkordancia/Karoli_1908.tsv`, az eddig nem mintázott könyvek: 5Móz, 1Sám, Péld, Ez, Mk, Ján, Róm, Jel.
Kizárva az 1–3. minta minden alakja (`adat/szoto/szoto_minta_{1,2,3}_*.tsv`). A rétegek szabályai és a rétegen
belüli gyakoriság-rétegzés az előmérés harmadik mintájáéval azonosak (harmadik_jeloltek.py, a 3. minta forrása);
rögzített véletlen-mag. Kimenet: a jelölt-lista (alak, gyakoriság, réteg, példa-igehely, példavers) a megadott
fájlba (alapértelmezés: a standard kimenet); a minta-TSV-t a modell-javaslatokkal a `minta4_ir.py` írja.

Használat: python eszkozok/szoto/minta4_jeloltek.py [--mag 20261013] [--kimenet <tsv>]"""
import argparse
import collections
import glob
import hashlib
import os
import random
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KAROLI = os.path.join(REPO, 'konkordancia', 'Karoli_1908.tsv')
KONYVEK = ('5Móz', '1Sám', 'Péld', 'Ez', 'Mk', 'Ján', 'Róm', 'Jel')
SZO = re.compile(r"[\wÁÉÍÓÖŐÚÜŰáéíóöőúüű-]+")
CEL = {'gyakori': 25, 'ragos_nevszo': 35, 'regies_ige': 20, 'regies_helyesiras': 12, 'ige_mai_alak': 13, 'tulajdonnev': 8}


def kizart_alakok():
    k = set()
    for p in sorted(glob.glob(os.path.join(REPO, 'adat', 'szoto', 'szoto_minta_[123]_*.tsv'))):
        sorok = [s for s in open(p, encoding='utf-8').read().split('\n') if s and not s.startswith('#')]
        for s in sorok[1:]:
            k.add(s.split('\t')[0])
    return k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mag', type=int, default=20261013)
    ap.add_argument('--kimenet')
    a = ap.parse_args()
    kizart = kizart_alakok()
    kizart_kis = {w.lower() for w in kizart}
    gy, pelda, vszov = collections.Counter(), {}, {}
    for s in open(KAROLI, encoding='utf-8').read().split('\n')[1:]:
        if '\t' not in s:
            continue
        ig, sz = s.split('\t', 1)
        if ig.rsplit(' ', 1)[0] not in KONYVEK:
            continue
        vszov[ig] = sz
        for w in SZO.findall(sz):
            if w[:1].isdigit() or w in kizart or w.lower() in kizart_kis:
                continue
            gy[w] += 1
            pelda.setdefault(w, ig)
    alak = [w for w, _ in gy.most_common()]
    kis = [w for w in alak if not w[:1].isupper()]
    retegek = {
        'tulajdonnev': [w for w in alak if w[:1].isupper() and w.lower() not in gy],
        'regies_ige': [w for w in kis if re.search(r'(á|é|ának|ének|ál|él|ék|ánk|énk|ván|vén)$', w) and len(w) > 3],
        'regies_helyesiras': [w for w in kis if re.search(r'(űl|űle|szűl|körűl|nyny|cz|ö[kt]$|ő[kt]$|tész|setét|mostan|néki|nékem|néked|kiván|lyly)', w)],
        'ragos_nevszo': [w for w in kis if re.search(r'(nak|nek|ban|ben|ból|ből|ra|re|ról|ről|tól|től|hoz|hez|höz|val|vel|ért|ként|at|et|öt|ot|vá|vé)$', w) and len(w) > 4],
        'ige_mai_alak': [w for w in kis if re.search(r'(ok|ek|ök|unk|ünk|tok|tek|nak|nek|ja|je|ják|jük|ott|ett|ött|ni|j|jon|jen|jön)$', w) and len(w) > 3],
    }
    rnd = random.Random(a.mag)
    valasztott, hol = [], {}
    for w in alak[:200]:
        if len([x for x in valasztott if hol[x] == 'gyakori']) >= CEL['gyakori']:
            break
        valasztott.append(w)
        hol[w] = 'gyakori'
    for r in ('regies_helyesiras', 'regies_ige', 'tulajdonnev', 'ragos_nevszo', 'ige_mai_alak'):
        pool = [w for w in retegek[r] if w not in hol]
        # a fele a gyakoribb feléből, a fele a ritkább feléből (rétegen belüli gyakoriság-rétegzés)
        fel = len(pool) // 2
        n = CEL[r]
        db = rnd.sample(pool[:fel], min(n - n // 2, fel)) + rnd.sample(pool[fel:], min(n // 2, len(pool) - fel))
        for w in db:
            valasztott.append(w)
            hol[w] = r
    h = hashlib.sha256(open(KAROLI, 'rb').read()).hexdigest()[:12]
    ki = open(a.kimenet, 'w', encoding='utf-8', newline='\n') if a.kimenet else sys.stdout
    ki.write(f'# proveniencia: scope={",".join(KONYVEK)} Károli-szóalakjai, az 1–3. minta alakjai nélkül, rétegzett, mag {a.mag} | '
             f'forras=konkordancia/Karoli_1908.tsv (sha256:{h}) + eszkozok/szoto/minta4_jeloltek.py | '
             f'alak a nyolc könyvben: {len(gy)}, token: {sum(gy.values())}\n')
    ki.write('alak\tgyakorisag\tkategoria\tpelda_igehely\tpelda_vers\n')
    for w in valasztott:
        ki.write(f'{w}\t{gy[w]}\t{hol[w]}\t{pelda[w]}\t{vszov[pelda[w]]}\n')
    print(f'választott: {len(valasztott)} {dict(collections.Counter(hol.values()))}', file=sys.stderr)


if __name__ == '__main__':
    main()
