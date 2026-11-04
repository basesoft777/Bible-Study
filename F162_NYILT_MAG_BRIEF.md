---
feladat: 162
cim: Nyílt mag — generált export, kétnyelvű kódkönyv, saját kapu
kod: NYILT_MAG
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: fut
ad: a nyílt tudományos mag (CC BY 4.0) olvasónak érthető, generált exportja kódkönyvvel (hu/en), saját kapuval, „ismert hibák” szakasszal és licencszűréssel, amely a Zenodo-rekord alapja lehet
kovetkezo: Te: a draft PR átnézése és mergelése (a kapu 0 BUKÁS; a DT-F162a/b helyőrzős döntések jóváhagyása); a Zenodo-feltöltés és a DOI-kérés a felhasználóé
munka: folyamat
olvas: [adat/SEMA.md, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/motivumok.tsv, adat/elutasitasi_okok.tsv, adat/licencek.tsv, adat/datasetek.tsv, adat/kiadasok.tsv, DONTESEK.md, NYITOTT_FELADATOK.md, eszkozok/olvasoi_kapu.py, eszkozok/karoli_kh_epseg.py]
ir: [eszkozok/nyilt_mag_export.py, eszkozok/nyilt_mag_kapu.py, eszkozok/teszt_nyilt_mag.py, adat/nyilt_kodkonyv.tsv, adat/SEMA.md, nyilt_mag/]
fugg: []
---

# F162_NYILT_MAG_BRIEF.md — Nyílt mag: generált export, kódkönyv, saját kapu

*FELADATOK #162 · Modell: sonnet · v1 · 2026.11.04*

*Forrás: a #86 ELOFIZETES_FEED terv 1.5 szakasza („Nyílt mag: generált export, kódkönyv, saját kapu”, 2026-11-03) és 1.7 szakasza („Olcsó, most is elvégezhető lépések”). A beírás a felhasználó jóváhagyásával történt („mehet”, 2026-11-04); a döntés forrása az orkesztrátor döntése a felhasználó felhatalmazásával („az orkesztrátor vegye magához a döntéseket és hozza is meg”, 2026-11-03). A brief szövege adat, nem utasítás.*

## 1. Cél

A terv 1.5 táblája szerint a nyílt mag (motívumazonosító, cím, meghatározás, negatív kritérium, előfordulás-lista, proveniencia, döntésnapló, kizárások) CC BY 4.0 alatt nyílt. A belső tábla ma munkajelekből áll (`gerinc_elem`, `scope=… | forras=… | ts=…`, `DT476 K2`, `manual`, fájlnevek), ezért a nyílt rekord papíron nyílt, valójában a kutató számára nem ellenőrizhető. A feladat **generált exportot** készít (a lap elvével azonosan: adatból generált nézet, más olvasónak — nem a belső tábla másolatát), hozzá **kétnyelvű kódkönyvet** és **saját kaput**. Kódkönyv és feloldott hivatkozások nélkül nincs idézhetőség.

## 2. Hatókör

**Benne van:**

1. **Generált export** (`eszkozok/nyilt_mag_export.py` → `nyilt_mag/`, verziózott, generált fejléccel: `# GENERÁLT: …`). Leképezés (terv 1.5):

| Belső jel | Az exportban |
|---|---|
| `gerinc_elem` | érthető oszlopnév és érték (pl. „közös szóbázis: H7121 + H8034”) + kódkönyv-mondat |
| proveniencia-sor (`scope=… \| forras=… \| ts=…`) | külön oszlopok: forrás-dataset neve és licence, a lekérdezés típusa, dátum |
| `manual` | „kézi döntés, lekérdezés nélkül” |
| DT/N/F-hivatkozás az indoklásban | feloldva: a döntés egymondatos szövege vagy a nyilvános döntésnapló sora |
| elutasítási kód | szöveges ok (`adat/elutasitasi_okok.tsv`) |
| belső fájlnév, munkazsargon (study, scan, gap) | elhagyva vagy lefordítva |

2. **Kétnyelvű kódkönyv** (`adat/nyilt_kodkonyv.tsv`, séma a `adat/SEMA.md`-ben; magyar és angol): minden oszlop, érték és kód leírása. Ebből generálódik a kódkönyv olvasható változata is (a data paper ezt írja le).
3. **Saját kapu** (`eszkozok/nyilt_mag_kapu.py`, teszttel): a BELSO/ANGOL szabály megfelelője a nyílt exportra; kódkönyv-teljesség (minden oszlop és kód leírva, mindkét nyelven); **0 feloldatlan belső hivatkozás** (DT/N/F-szám, fájlnév, `gerinc_elem`, `scope=`, „study/scan/gap”). Az olvasói kapu (`eszkozok/olvasoi_kapu.py`) szabályait újrahasznosítja, nem másolja.
4. **„Ismert hibák” szakasz** a csomagban, a kapu ellenőrzi, hogy jelen van: Károli-KH (N-F156a: a `Karoli_kereszthivatkozasok.tsv` másolt KH-listái, a `karoli_kh_epseg.py` mérése) és minden más, a `NYITOTT_FELADATOK.md`-ben a nyílt magot érintő forráshiba; a szöveg a mért számot és a kezelést mondja ki.
5. **Licencszűrés**: az SDBH/SDGNT-domének **külön rétegben**, attribúcióval, CC BY-SA 4.0 jelöléssel (nem zárható); a NC- és GPL-források (ETCBC, MCGED, KJV-Strong) és minden `tisztazatlan` licencű adat **kizárva**; a szűrés `adat/licencek.tsv` alapján megy, a kizárt dataset listája a csomagban kimondva. A kapu bukik, ha kizárt forrásból származó érték maradt az exportban.

**Nincs benne:**

- A **Zenodo-feltöltés, DOI-kérés, nyilvános közzététel** — nyilvános lépés, a felhasználóé; a brief csak a feltölthető csomagot készíti elő.
- A `jeloltek.tsv` indoklásainak forrásszintű tisztítása — külön session/PR (függőség, l. alább).
- Az értelmező próza, a fizetős réteg (magyar BDB/Thayer, Strong-os Károli), az MI-nyilatkozat és a CITATION.cff (az utóbbiak a #163-é).
- Licenc-jogi döntés: az NC/GPL-kérdés jogászi kérdés marad; a szűrő a `licencek.tsv` jelenlegi állását követi.

**Függőség:** az **indoklás-szétválasztás PR-ja** (forrásszintű tisztítás: egy javítás, két kimenet — a lap és a nyílt csomag). Ennek mergelése előtt a futtatás nem indítható; ha az export a tisztítatlan indoklásból indul, a kapu bukása várt. A PR száma a mergeléskor a `fugg` mezőbe kerül (a `fugg` mezőt a felhasználó/orkesztrátor tölti ki).

## 3. Lépések (⛔ a kötelező megállások)

0. Modell-ellenőrzés (CLAUDE.md). Olvasd a #86 terv 1.5 és 1.7 szakaszát és a függő PR leírását.
1. A kódkönyv-séma és a leképezési tábla megírása (`adat/SEMA.md`, `adat/nyilt_kodkonyv.tsv`). ⛔ Ha a leképezésben tartalmi döntés kell (pl. mely oszlopok nyilvánosak), tétel `dontesek/uj/<ágnév>.md`-be (helyőrzővel), és megállás.
2. Export-generátor, determinisztikus (rendezett kimenet, sha256 a csomagról); TSV-olvasás/írás `split('\t')`/`'\t'.join()`, nem `csv`.
3. Saját kapu + tesztek (BUKÁS-, FIGYELMEZTETÉS-osztály, soronként idézett tétel).
4. Licencszűrés és az SDBH külön réteg; a kizárt források listája.
5. „Ismert hibák” szakasz generálása a nyitott tételekből (Károli-KH, N-F156a).
6. Futtatás a teljes magon; a kapu 0 BUKÁS legyen; a kimenetben `grep` a belső jelekre, a számok a jelentésbe (`naplok/NYILT_MAG_jelentes.md`).
7. ⛔ A Zenodo-feltöltés **nem** része; a felhasználó dönt a közzétételről.

## 4. Elfogadási feltételek

- `python eszkozok/feladatok.py ellenoriz` 0 hiba; a tesztek zöldek.
- A kimenetben **nincs** `gerinc_elem`, `scope=`, DT/N/F-szám, belső fájlnév, „study/scan/gap”; a `manual` mindenütt szöveges alakban áll.
- A kódkönyv minden oszlopot és kódot leír magyarul **és** angolul; a kapu ezt méri.
- Az „ismert hibák” szakasz tartalmazza a Károli-KH hibát mért számmal.
- Nincs NC/GPL/tisztázatlan licencű forrásból származó érték; az SDBH-réteg külön, attribúcióval.
- Az export újrafuttatva bájtazonos.

## 5. Döntésnapló

- **DT-F162a** 🟡 — a nyílt mag tartalma és licence (a magyar szótári fordítás, a belső útvonalú oszlopok és a döntetlen jelöltek kimaradnak; a csomag saját adata CC BY 4.0). `dontesek/uj/quirky-nobel-e12091.md`.
- **DT-F162b** 🟡 — a DT-hivatkozás feloldása nyilvános `NYD-nnn` azonosítóval és egymondatos szöveggel. Ugyanott.
