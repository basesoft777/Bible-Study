"""F94.7 (FELADATOK #94, DT-F94f, N-F94h): a `regies_jegy` hibaarányának becslése a kiadott táblán — rögzített magú,
egyszerű véletlen minta a jegyes sorokból (`regies_jegy` nem üres), példaverssel a kézi besoroláshoz.

1. lépés (`--jeloltek`): a minta alakjai a példaverssel (az első Károli-vers, amelyben az alak pontosan így áll) a
   standard kimenetre — a kézi besorolás munkalapja (nem kerül a repóba).
2. lépés (alapértelmezés): a `BESOROLAS` szótár (kézi, modell: claude-opus-5-5, a példavers alapján) beírása az
   `adat/szoto/regies_jegy_minta.tsv`-be, és a becsült hibaarány Wilson 95%-os konfidenciaintervallummal.
Besorolás soronként: `igei` (igen | nem | ketes), `jegy_helyes` (igen | nem | ketes); `ellenorzes=modell_ellenorizetlen`.

Használat: python eszkozok/szoto/jegy_minta.py [--jeloltek] [--mag 20261013] [--n 100]"""
import argparse
import datetime
import hashlib
import math
import os
import random
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TABLA = os.path.join(REPO, 'adat', 'szoto', 'karoli_szotari_alak.tsv')
KAROLI = os.path.join(REPO, 'konkordancia', 'Karoli_1908.tsv')
KI = os.path.join(REPO, 'adat', 'szoto', 'regies_jegy_minta.tsv')
SZO = re.compile(r"[\wÁÉÍÓÖŐÚÜŰáéíóöőúüű-]+")

# kézi besorolás: alak -> (igei, jegy_helyes, indoklás)
BESOROLAS = {
    'Elbocsátá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Elmenének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Előhivatának': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Előhozatá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Futa': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Fölkele': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Intének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes; mellékes lemmahiba: intik (helyesen: int)'),
    'Javítgatá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Kivonulának': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Megfutamodék': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Meggyökerezvén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes; mellékes lemmahiba: meggyökerez (helyesen: meggyökerezik)'),
    'Megindítá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Szerzék': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Terjede': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Uralkodék': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'beküldének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'betérének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'bevevé': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'borulának': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'bíráskodának': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'bízál': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'elfeledkezétek': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'elhengeríté': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'elhívatá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'eljárván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'elkezde': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'eloszlának': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes; mellékes lemmahiba: eloszl (helyesen: eloszlik)'),
    'elrejtőzének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes; mellékes lemmahiba: elrejtőz (helyesen: elrejtőzik)'),
    'elszakasztván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'eltisztítá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'elutazék': ('igen', 'nem', 'az -ik-es elutazik E/3-a (Mt 21:33: a gazda „elutazék”); a jegy mult.E1, helyesen E/3 — a lemmából hiányzik az -ik (elutaz), ezért az N-F94e-szabály nem fogta'),
    'elveszté': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'elválának': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'előhivatván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'felszedé': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'felszökvén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'felöltözteté': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'föltekintvén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'füstölögtete': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'hajlának': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'irigykedének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes; mellékes lemmahiba: irigyked (helyesen: irigykedik)'),
    'kihányván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'kiirtatván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'kivonván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'kiálta': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'kiáltának': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'kiűzék': ('igen', 'nem', 'T/3 tárgyas (4Móz 5:4: „Izráel fiai … kiűzék azokat”); a jegy mult.E1 — a magas hangrendű -ék E/1 / T/3 tárgyas kétértelműség (N-F94e megjegyzés)'),
    'készítél': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'könyörűle': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'lehányván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'leszállván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'leszállál': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'levevé': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'levága': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'leülének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megbáná': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megcselekedvén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megcsókolván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megeleveníttetvén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megelégedvén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megerősíte': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megfordulánk': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'meghasítá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megmenté': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megsegítteték': ('igen', 'nem', 'szenvedő E/3 (2Krón 26:15: „csudálatosan megsegítteték”); a jegy mult.E1, helyesen E/3 (a szenvedő -tetik -ik-es; a lemma megsegíttet)'),
    'megszámlálá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megtaláltaték': ('igen', 'nem', 'szenvedő E/3 (2Krón 15:15: „megtaláltaték általok”); a jegy mult.E1, helyesen E/3'),
    'megverettetének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megvervén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megélede': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megépüle': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'megölelé': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes; mellékes lemmahiba: megölelik (helyesen: megölel)'),
    'megövedzvén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'menénk': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes; mellékes lemmahiba: men (helyesen: megy)'),
    'metélék': ('igen', 'nem', 'T/3 tárgyas (2Móz 39:3: „fonalakká metélék”); a jegy mult.E3, mert a lemma tévesen -ik-es (metélik); helyesen T/3 tárgyas'),
    'méré': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'nemzének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'növekedék': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'odaszólítá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'rohana': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'rohanván': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'szólhata': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'szűle': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'találá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'teremvén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'tétetének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'utóléré': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'veszté': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'vevé': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'virágozék': ('igen', 'nem', 'E/3 (1Móz 40:10: a szőlőtő „virágozék”), az -ik-es virágzik/virágozik alakja; a jegy mult.E1, a lemmából hiányzik az -ik'),
    'visszafordula': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'visszamarada': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'visszatérének': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'visszatérétek': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'visszavevé': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'vonakodék': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'Áldá': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'állíta': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'általkelvén': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
    'érkezénk': ('igen', 'igen', 'igei alak; a jegy a példavers szerint helyes'),
}


def jegyes():
    sorok = [s for s in open(TABLA, encoding='utf-8').read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:] if s.split('\t')[fej.index('regies_jegy')]]


def pelda_versek(alakok):
    kell, ki = set(alakok), {}
    for s in open(KAROLI, encoding='utf-8').read().split('\n')[1:]:
        if '\t' not in s:
            continue
        ig, sz = s.split('\t', 1)
        for w in SZO.findall(sz):
            if w in kell and w not in ki:
                ki[w] = (ig, sz)
    return ki


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--jeloltek', action='store_true')
    ap.add_argument('--mag', type=int, default=20261013)
    ap.add_argument('--n', type=int, default=100)
    ap.add_argument('--ts', default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'))
    a = ap.parse_args()
    j = jegyes()
    minta = sorted(random.Random(a.mag).sample(j, a.n), key=lambda r: r['alak'])
    pv = pelda_versek([r['alak'] for r in minta])
    if a.jeloltek:
        print(f'jegyes sor: {len(j)}; minta: {a.n}; mag: {a.mag}')
        for r in minta:
            ig, sz = pv.get(r['alak'], ('—', ''))
            print(f"{r['alak']}\t{r['szotari_alak']}\t{r['regies_jegy']}\t{r['modszer']}\t{ig}\t{sz}")
        return
    hiany = [r['alak'] for r in minta if r['alak'] not in BESOROLAS]
    if hiany:
        sys.exit(f'HIBA: besorolás nélküli alak: {hiany}')
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
    oszlop = ['alak', 'szotari_alak', 'regies_jegy', 'modszer', 'pelda_igehely', 'igei', 'jegy_helyes', 'ellenorzes', 'indoklas']
    with open(KI, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# proveniencia: scope=a karoli_szotari_alak.tsv {len(j)} jegyes sorából (regies_jegy nem üres) {a.n} elemű egyszerű véletlen minta, '
                f'mag {a.mag} | forras=adat/szoto/karoli_szotari_alak.tsv (sha256:{h(TABLA)}) + konkordancia/Karoli_1908.tsv (sha256:{h(KAROLI)}; a '
                f'példavers: az első vers, amelyben az alak pontosan így áll) + manual (a besorolás modell-állítás, modell: claude-opus-5-5) + '
                f'eszkozok/szoto/jegy_minta.py | ts={a.ts}\n')
        f.write('# allapot: ellenorzes=modell_ellenorizetlen minden sorban (a felhasználó nem nézte át); a hibaarány-becslés a naplóban és a '
                'zárójelentésben (N-F94h). igei / jegy_helyes: igen | nem | ketes (ketes: a példavers alapján nem dönthető)\n')
        f.write('\t'.join(oszlop) + '\n')
        for r in minta:
            igei, helyes, ind = BESOROLAS[r['alak']]
            ig = pv.get(r['alak'], ('—', ''))[0]
            f.write('\t'.join([r['alak'], r['szotari_alak'], r['regies_jegy'], r['modszer'], ig, igei, helyes, 'modell_ellenorizetlen', ind]) + '\n')
    hibas = sum(1 for r in minta if BESOROLAS[r['alak']][1] == 'nem')
    ketes = sum(1 for r in minta if BESOROLAS[r['alak']][1] == 'ketes')
    nem_igei = sum(1 for r in minta if BESOROLAS[r['alak']][0] == 'nem')
    lo, hi = wilson(hibas, a.n)
    lo2, hi2 = wilson(hibas + ketes, a.n)
    lo3, hi3 = wilson(nem_igei, a.n)
    print(f'jegyes sor: {len(j)}; minta: {a.n} (mag {a.mag})')
    print(f'hibás jegy: {hibas} ({100 * hibas / a.n:.0f}%; Wilson 95%: {100 * lo:.1f}–{100 * hi:.1f}%); kétes: {ketes}; '
          f'hibás + kétes: {hibas + ketes} ({100 * lo2:.1f}–{100 * hi2:.1f}%)')
    print(f'nem igei alak jeggyel: {nem_igei} ({100 * nem_igei / a.n:.0f}%; Wilson 95%: {100 * lo3:.1f}–{100 * hi3:.1f}%)')
    print(f'becsült hibás jegyes sor a táblában: {round(len(j) * hibas / a.n)} ({round(len(j) * lo)}–{round(len(j) * hi)})')


if __name__ == '__main__':
    main()
