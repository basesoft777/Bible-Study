# F186 — A Thayer vers → jelentéspont hozzárendelés mérése és javítása (THAYER_JELENTESPONT_97)

*FELADATOK #186 · végrehajtó: claude-opus-5-5 · ág: `claude/f186-thayer-jelentespont-97` · 2026-11-10*

A mérés a javítás előtt áll. Az 1. szakasz (eljárás és kapu) a seed-201 kitöltése **előtt** került commitba (F186.1).
A későbbi szakaszok a mért eredményeket rögzítik.

## 1. Az eljárás és a kapu (rögzítve a kitöltés előtt)

*Proveniencia: scope=adat/thayer_vers_jelentes.tsv (ÚSZ-sorok) + konkordancia/lexikonok_nyers/Thayer.lexicon |
forras=f186_minta.py (a 7. melléklet forrása) | ts=2026-11-10.*

### 1.1 Mit mérünk

A mért kimenet az `adat/thayer_vers_jelentes.tsv` egy sora: egy Thayer-szócikk egy ÚSZ-hivatkozása (a `bcv`-jelölt
hivatkozás, vagy a `</ref>` utáni jelöletlen folytatás), két mezővel:

- **könyv/vers:** `konyv` + `fejezet:vers` (a hivatkozott hely, Károli-könyvrövidítéssel);
- **jelentéspont:** `utvonal` (`<felső>/<szám>/<betű>`, a felső a nagybetű és a római szám ponttal: `A`, `I`, `A.I`;
  hiányzó szint `-`; különleges: `fej` — az első fej előtti rész, `cim` — a címsor).

A kettőt külön mérjük, külön számmal.

### 1.2 A minta (seed-201; a T4-ben seed-202)

- **Sokaság:** a tábla ÚSZ-sorai (a `konyv` a `Konyv_normalizalo_tabla.tsv` 40–66. könyve): 58 712 sor, 5 352 Strong.
- **Rétegzés gyakori és ritka Strongra:** a Strongok az ÚSZ-sorszámuk szerint csökkenő sorrendben (egyezésnél Strong
  szerint); **gyakori** az a legrövidebb előtag, amelynek kumulált sorszáma eléri a sokaság felét (213 Strong, 29 357
  sor, a küszöb 55 hivatkozás); **ritka** a többi (5 139 Strong, 29 355 sor).
- **Választás:** rétegenként 100 sor, `random.Random(seed).sample` a `(strong, sorszam)` szerint rendezett listán,
  majd a 200 sor ugyanazzal a generátorral keverve; azonosító `T001`–`T200` (seed-202: `U001`–`U200`, a seed-201
  sorai kizárva).
- **Súlyozás:** a két réteg a sokaság egy-egy fele, rétegenként egyenlő mintával, ezért a minta önsúlyozó: a 200 sor
  nyers aránya a sokaság becslése. A rétegenkénti szám tájékoztató.

### 1.3 A kitöltés (vak, két független kéz)

- **Két független kitöltő**, mindkettő Opus (`general-purpose` subagent, `model: opus`): **A** és **B**. A
  terjedelem miatt kitöltőnként két köteg (A1, A2, B1, B2; a köteg Strongonként zárt). A kitöltők egymás
  eredményét nem látják.
- **Vak:** a kitöltő a gépi hozzárendelést (`utvonal`, `konyv`, `fejezet`, `vers`), a szakasztáblát és a kulcsot nem
  látja, és a táblákat nem olvashatja. Amit kap: a munkalap (`azon`, `strong`, a hivatkozás megjelenő szövege,
  környezet) és a szócikkek teljes szövege (a `Thayer.lexicon` HTML-je címkék nélkül, a forrás bekezdéseivel, a mért
  hivatkozás előtt `⟦azon⟧` jelölővel; 40 000 karakter fölött a szöveg az utolsó jelölt bekezdés utáni bekezdésig).
- **Amit kitölt:** `konyv_vers` (Károli-rövidítéssel, pl. `Jn 3:16`; a folytatásnál a láncból feloldva);
  `jelentespont` a fenti formátumban, a szócikk **tényleges tagolása** szerint (a fejek: `A.`, `I.`, `1.`, `a.`; a
  bekezdéshatár nem dönt; a kereszthivatkozásban álló jelölő — pl. „cf. B. 2 c.” — nem fej); `melyebb` (a görög betűs
  vagy mélyebb szint, ha van; nem része a fő mutatónak); `megjegyzes` (bizonytalanság, forráshiba gyanúja).
- **Aki dönt, nem ellenőriz:** a kitöltők döntenek; az eltérések feloldását a végrehajtó végzi a forrásszöveg alapján
  (1.5), a független ellenőrzést a `fuggetlen-ellenor`.

### 1.4 Az összevetés szabályai

- **könyv/vers:** pontos egyezés (könyv + fejezet + vers).
- **jelentéspont, fő mutató:** a három szint (`felső/szám/betű`) pontos egyezése; a `melyebb` szint nem része. Egyenértékű:
  `fej` = `tagolatlan` (a szócikknek nincs fejes tagolása). A `cim` csak `cim`-mel egyezik.
- **`zaro`** (kiegészítés, a kitöltés előtt rögzítve, F186.2): a tagolás után álló, az utolsó jelentésponthoz tartalmilag
  nem tartozó záró rész (pl. szinonima-jegyzet, „[SYNONYMS …]”, összetételek felsorolása) hivatkozása. A gépi kimenetben
  ilyen érték nincs: ha az arany érték `zaro`, a gépi útvonal hibásnak számít.
- **jelentéspont, előtag-mutató (tájékoztató):** a gépi útvonal a kitöltött útvonal előtagja (a gépi durvább, de nem hibás).

### 1.5 Az eltérések feloldása (a BDB seed-101 mintája, `naplok/BDB_SZELETELO_M2_seed101_iteletek.md`)

Arany érték: ha A = B, az; ha A ≠ B, vagy A = B ≠ gépi, soronkénti ítélet a forrásszöveg alapján (idézettel). Kategóriák:
**hozzárendelés-hiba** (a gépi kimenet hibás), **kitöltő-hiba** (csak a forrással bizonyítva), **forrás-hiba** (a
forrás maga hibás, pl. a `bcv` mást mond, mint a megjelenő szöveg — a gépi kimenet hibásnak számít, javítása a
`adat/thayer_forras_javitas.tsv`-be). Az ítéletek az `adat/thayer_aranyminta.tsv`-be kerülnek (a kitöltések, az arany
érték, az ítélet, proveniencia és a tényleges modellnév), és a jelentés 3. szakaszába.

### 1.6 A mutatók és a kapu

- **Mutatók:** a gépi kimenet egyezése az arany értékkel, nyers számmal (x / 200) és **Wilson-féle 95%-os
  konfidencia-intervallummal**, külön a könyv/versre és a jelentéspontra; tájékoztatóul A-ra és B-re külön, és
  rétegenként.
- **A kapu (előre rögzítve):** a jelentéspont **≥ 97%**, azaz **≥ 194 / 200** egyezés az arany értékkel, és a
  könyv/vers is ≥ 194 / 200. A kapu a pontbecslésre vonatkozik; a CI a jelentésben áll.
- **T2 után** a seed-201 újramérése a javított táblán tájékoztató (ugyanazok a sorok, ezért nem független);
  **⛔ T3** csak akkor kell, ha a T2 utáni seed-201 érték 97% alatt marad (költségbecslés, megállás).
- **T4:** új vak mérés (seed-202) ugyanezzel az eljárással; ez a kapu döntő mérése.

## 7. Melléklet — a mintavevő forrása (`f186_minta.py`)

A szkript a repón kívül fut (a brief `ir` mezője nem tartalmaz mérőszkriptet); a mintát ez a forrás és a seed teljesen meghatározza.

```python
"""F186 T1/T4 — a Thayer vers -> jelentéspont vak mintája (seed-201 / seed-202).

Sokaság: az adat/thayer_vers_jelentes.tsv ÚSZ-sorai (konyv a Konyv_normalizalo_tabla 40-66. könyve), egy sor = egy hivatkozás.
Rétegek: a Strongok az ÚSZ-sorszámuk szerint csökkenő sorrendben (egyezésnél Strong szerint); `gyakori` az az előtag, amelynél a
kumulált sorszám először éri el a sokaság felét; `ritka` a többi. Rétegenként 100 sor egyenletesen (random.Random(seed).sample a
(strong, sorszam) szerint rendezett listán), majd a 200 sor ugyanazzal a generátorral keverve, azon T001..T200 (seed-202: U001..).
Mivel a két réteg a sokaság egy-egy fele, a minta önsúlyozó: a 200 nyers aránya a sokaság becslése.

Kimenet (a --ki könyvtárba): <tag>_vak.tsv (a kitöltőnek), <tag>_szocikkek.txt (a szócikkek szövege a jelölőkkel, a kitöltőnek),
<tag>_kulcs.tsv (a gépi hozzárendelés; a kitöltőnek NEM adandó).
Használat: python f186_minta.py --seed 201 --elotag T --ki <könyvtár> [--kizar <kulcs.tsv> ...]
"""
import argparse
import collections
import html
import os
import random
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

REPO = r'E:\Claude\Bible-Study\cranky-easley-763e7c'
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'thayer_jelolt'))
import bont  # noqa: E402
import vers_jelentes as VJ  # noqa: E402

TAG = re.compile(r'<[^>]+>')
WS = re.compile(r'[ \t\r\n]+')
MAX_SZOCIKK = 40000


def olvas(ut):
    L = [l.rstrip('\n').rstrip('\r').split('\t') for l in open(ut, encoding='utf-8') if l.strip() and not l.startswith('#')]
    return [dict(zip(L[0], r)) for r in L[1:]]


def usz_konyvek():
    L = [l.rstrip('\n').split('\t') for l in open(VJ.KONYV_UT, encoding='utf-8')]
    i = L[0].index('Magyar rövidítés')
    return [r[i] for r in L[40:67]]


def hivatkozas_poziciok(raw, f0):
    """A bekezdés hivatkozásai a vers_jelentes.general sorrendjében: [(poz a raw-ban, megjelenő szöveg)]."""
    ki = []
    for m in VJ.BCV.finditer(raw):
        vege = VJ.REF_VEG.search(raw, m.end())
        ki.append((m.start(), TAG.sub('', raw[m.end():vege.start() if vege else m.end()])))
        if not vege:
            continue
        # a folytatás-lánc pozíciói (a VJ.folytatasok logikája, pozícióval)
        q = vege.end()
        t = VJ.FOLYT_TARTOMANY.match(raw, q)
        if t:
            q = t.end()
        while True:
            mm = VJ.FOLYT_VERS.match(raw, q)
            if mm:
                ki.append((mm.start(1), mm.group(1)))
            else:
                mm = VJ.FOLYT_FEJEZET.match(raw, q)
                if not mm:
                    break
                ki.append((mm.start(1), mm.group(1) + ':' + mm.group(2)))
            q = mm.end()
            t = VJ.FOLYT_TARTOMANY.match(raw, q)
            if t:
                q = t.end()
    return ki


def sima_jelolovel(raw, jelolok):
    """A bekezdés sima szövege; a jelolok {raw-poz: azon} helyére „⟦azon⟧ ” kerül."""
    darabok, p = [], 0
    for poz in sorted(jelolok):
        darabok.append(raw[p:poz])
        darabok.append('\x00%s\x01' % jelolok[poz])
        p = poz
    darabok.append(raw[p:])
    s = html.unescape(TAG.sub('', ''.join(darabok)))
    s = WS.sub(' ', s).strip()
    return s.replace('\x00', '⟦').replace('\x01', '⟧ ')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, required=True)
    ap.add_argument('--elotag', required=True)
    ap.add_argument('--ki', required=True)
    ap.add_argument('--kizar', nargs='*', default=[])
    a = ap.parse_args()
    usz = set(usz_konyvek())
    sorok = [r for r in olvas(VJ.KI_UT) if r['konyv'] in usz]
    kizart = set()
    for k in a.kizar:
        kizart |= {(r['strong'], r['sorszam']) for r in olvas(k)}
    db = collections.Counter(r['strong'] for r in sorok)
    rend = sorted(db, key=lambda s: (-db[s], s))
    fel, acc, gyakori = len(sorok) / 2, 0, set()
    for s in rend:
        if acc >= fel:
            break
        gyakori.add(s)
        acc += db[s]
    retegek = {'gyakori': [], 'ritka': []}
    for r in sorok:
        if (r['strong'], r['sorszam']) in kizart:
            continue
        retegek['gyakori' if r['strong'] in gyakori else 'ritka'].append(r)
    rng = random.Random(a.seed)
    minta = []
    for nev in ('gyakori', 'ritka'):
        L = sorted(retegek[nev], key=lambda r: (r['strong'], int(r['sorszam'])))
        for r in rng.sample(L, 100):
            minta.append(dict(r, reteg=nev))
    rng.shuffle(minta)
    for i, r in enumerate(minta, 1):
        r['azon'] = '%s%03d' % (a.elotag, i)
    print('sokaság ÚSZ-sor: %d; Strong: %d; gyakori Strong: %d (%d sor), ritka Strong: %d (%d sor); kizárt: %d'
          % (len(sorok), len(db), len(gyakori), acc, len(db) - len(gyakori), len(sorok) - acc, len(kizart)))

    lex = bont.lexikon_beolvas()
    cel = collections.defaultdict(dict)  # strong -> {sorszam: azon}
    for r in minta:
        cel[r['strong']][int(r['sorszam'])] = r['azon']
    szoveg, kornyezet, nyers = {}, {}, {}
    for sp in sorted(cel):
        topic, d = lex[sp]
        n, bekezdesek, utolso = 0, [], -1
        for x in bont.szerkezet(d):
            jel = {}
            for poz, megj in hivatkozas_poziciok(x['raw'], 0):
                n += 1
                if n in cel[sp]:
                    az = cel[sp][n]
                    jel[poz] = az
                    nyers[az] = megj
            bekezdesek.append(sima_jelolovel(x['raw'], jel))
            if jel:
                utolso = len(bekezdesek) - 1
        for az in cel[sp].values():
            for b in bekezdesek:
                i = b.find('⟦%s⟧' % az)
                if i >= 0:
                    kornyezet[az] = b[max(0, i - 160):i + 120]
        teljes = '\n\n'.join(bekezdesek)
        if len(teljes) > MAX_SZOCIKK:
            teljes = '\n\n'.join(bekezdesek[:utolso + 2]) + '\n\n[… a szócikk folytatódik; a jelölt hivatkozások mind a fenti részben állnak]'
        szoveg[sp] = teljes
    os.makedirs(a.ki, exist_ok=True)
    tag = 'seed%d' % a.seed
    with open(os.path.join(a.ki, tag + '_szocikkek.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for sp in sorted(szoveg):
            f.write('=== %s ===\n%s\n\n' % (sp, szoveg[sp]))
    with open(os.path.join(a.ki, tag + '_vak.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['azon', 'strong', 'nyers', 'kornyezet', 'konyv_vers', 'jelentespont', 'melyebb', 'megjegyzes']) + '\n')
        for r in sorted(minta, key=lambda r: r['azon']):
            f.write('\t'.join([r['azon'], r['strong'], nyers[r['azon']], kornyezet[r['azon']].replace('\t', ' '), '', '', '', '']) + '\n')
    with open(os.path.join(a.ki, tag + '_kulcs.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        mezok = ['azon', 'reteg', 'strong', 'sorszam', 'szakasz', 'konyv', 'fejezet', 'vers', 'utvonal']
        f.write('\t'.join(mezok) + '\n')
        for r in sorted(minta, key=lambda r: r['azon']):
            f.write('\t'.join(r[m] for m in mezok) + '\n')
    print('szócikk: %d; szöveg összesen %d karakter' % (len(szoveg), sum(len(v) for v in szoveg.values())))
    hiany = [az for az in (r['azon'] for r in minta) if az not in nyers or az not in kornyezet]
    print('jelölő nélkül maradt: %s' % hiany)


if __name__ == '__main__':
    main()
```
