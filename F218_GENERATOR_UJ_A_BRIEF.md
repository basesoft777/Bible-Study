---
feladat: 218
cim: A lapgenerátor újraírása, 1. rész — építés a regresszióig (új fájlokban)
kod: GENERATOR_UJ_A
tipus: feladat
fazis: folyamat
modell: opus
allapot: megallt
ag: claude/f218-generator-uj-a
pr: 729
ad: új lapgenerátor az `eszkozok/lapgen/` alatt, amely a HAMART-001 lapját a mai lappal szakaszonként egyezően állítja elő (csak a felsorolt, darabszámhoz kötött eltérésekkel), és az ISTENTISZT-001 lapját belső szöveg nélkül; a látható szöveg cserével nem készülhet, ezt típus és festékpróba bizonyítja; a régi generátor és minden mai kapu érintetlen marad
kovetkezo: "Te: a DT-F218n (az ismétlés megszüntetése) az 1. szakaszban kész, a kézi szöveg változásai a 218a végi listában várnak; az S3 (F218.6) alszeletekre bontva; az S3a (Áttekintés, 4.1) kész, az S3c (4.3–4.10) részben kész (4.3, 4.4, 4.5, 4.7, 4.9, 4.10); az S3d (4.12–4.14) kész; a 4. ellenőrzés (S3a, S3d, DT-F218n) lefutott, öt tétele javítva, az E2 döntést kér; a modell a DT-F218o szerint opus: következik az S3c maradéka (4.8; opus, high), majd az S3b (4.2 BDB-kártya) a Thayer-kártyával (opus, xhigh), új sessionben, a naplok/F218_folytatas.md „Következő lépés” pontja szerint; a független ellenőr mostantól Fable, két alszeletenként"
munka: folyamat
olvas: ["eszkozok/lexikon_general.py", "eszkozok/szerep_*.py", eszkozok/olvasoi_kovetkeztetes.py, eszkozok/olvasoi_utofeldolg.py, eszkozok/tablajegyzet.py, eszkozok/kiejtes.py, eszkozok/heber_kiejtes.py, eszkozok/kiejtes_szoveg.py, eszkozok/bdb_tagolas.py, eszkozok/bdb_rovidites.py, eszkozok/bdb_vj_szabaly.py, eszkozok/karoli_kh_szuro.py, eszkozok/lap_befagyasztas.py, eszkozok/lekerdez.py, eszkozok/olvasoi_kapu.py, eszkozok/ellenoriz.py, adat/, konkordancia/, adat/kiadasok.tsv, adat/lap_atnezesek.tsv, adat/lap_befagyasztas.tsv, adat/licencek.tsv, naplok/HIBA_MECHANIZMUSOK.md, naplok/KAROLI_PONTOSSAG_jelentes.md, motivumok/HAMART-001.md, motivumok/ISTENTISZT-001.md, lexikon/HAMART-001_TUDOMANYOS.md, lexikon/HAMART-001_KIZARASOK.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md]
ir: [eszkozok/lapgen/, adat/lapgen_bemenetek.tsv, adat/lapgen_sablonok.tsv, adat/olvasoi_nevtabla.tsv, adat/tematikus_sajat_szo.tsv, dontesek/uj/f218-generator-uj-a.md, adat/SEMA.md, adat/elofordulasok.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, eszkozok/general.py, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, naplok/F218_jelentes.md, naplok/F218_folytatas.md, naplok/F218_referencia.tsv, naplok/F218_elteres_engedely.tsv]
fugg: []
nem_fugg: [121, 123, 146, 178, 179]
---

# F218_GENERATOR_UJ_A_BRIEF.md — A lapgenerátor újraírása, 1. rész: építés a regresszióig

*FELADATOK #218 · Modell: opus (a DT-F218o óta, 2026-11-13; az S3d-ig és a 4. ellenőrzés javítóköréig fable) · v2 (tervezet, átdolgozva) · 2026.11.13 · forrás: a felhasználó („vegyük korábbra a generátor írást”; „Igen, dolgoztasd át”, 2026-11-13); DT-F212e, DT-F212f; a generátor-térkép és a súlyossági leltár; a `FABLE_VALASZ_UJ_JAVASLATOK_2026-11-13.md` (mind a megosztott jegyzetmappában). Alap: main `b5d93ea8`.*

**Három rész.** Ez a brief a **218a**: építés a regresszióig. A szerver-átkötés (218b) és az átállás (218c) külön befogadásra váró N-tétel a 13. pontban.

**A `nem_fugg` indoka** (a /befogad a `feladatok.py fuggesek` kimenetéből véglegesíti; ha más tétel is megjelenik, az ⛔, nem felülírás):
- **179** — a `general.py`-t írja; ez a brief egyetlen új `--cel` értéket ad hozzá (`lexikon2`), meglévő ágat nem érint.
- **178** — a 6-os sablont írja; ez a brief egy új szakaszt fűz hozzá (az alapszabály szövege), meglévő szakaszt nem módosít.
- **121** — a `lexikon_general.py`-t írja (gyűjtő-/generátorkör-tétel); ez a brief új modulokba ír, a régi generátort nem módosítja.
- **146** — a lezárt ISTENTISZT-001 tudományos lap; csak regressziós bemenet, a brief nem várja.
- **123** — az `elofordulasok.tsv`-t és a HAMART-forrást írja; ez a brief egy új oszlopot ad (T3), meglévő értéket nem ír át.

Mindhárom `megallt` állapotú. Ha bármelyik újraindul, vagy a main megváltoztatja a mérce bemeneteit, a 8. pont bemenet-hash őre kimondott hibával megállítja a regressziót.

---

## 0. A main mai állapota (b5d93ea8) — amihez a térkép és a leltár képest elavult

A térkép és a leltár a `cf68d0a9`/`63f3f126` pillanatképre szól. **A régi generátort szimbólum szerint kell keresni, nem sorszám szerint.** A mai helyek:

| Szimbólum | Ma | A térképben | Változás |
|---|---|---|---|
| `lexikon_general.py` hossza | 10 153 sor | 10 051 | #709 |
| `UJ_LAPSZERKEZET` | 7109 | 7099 | ma `{HAMART-001, ISTENTISZT-001}` |
| `KETRETEGU_BDB_KARTYA` | 3889 | 3885 | ua. |
| `BDB_BETU_JAVIT` | 4552 | 4548 | ua. |
| `TEMATIKUS_SAJAT_SZO` | 871 | 871 | változatlan |
| `SECE_LABJEGYZET` | 1919 | 1920 | változatlan szöveg |
| `gerinc_adat` | 3225 | 3221 | |
| `kolofon_szerzoseg` | 5999 | 5992 | a `lap_commit`-ot ma sem olvassa |
| `teljesseg_kapu` | 7558 | 7548 | |
| `olvasoi_atiras` | 8228 | – | a csere-lánc |
| `frissit_meglevo_fajlt` | 10036 | 9935 | |
| `BEFAGYASZTOTT` / `run` | 10046 / 10049 | 9945 / 9948 | |

- A `lexikon_general`-t az `eszkozok/` alatt **53 fájl** említi vagy importálja (git grep, b5d93ea8). Az archiválás ezért a 218c dolga, nem ezé a briefé.
- **Az ISTENTISZT-001 befagyasztott** (`adat/lap_befagyasztas.tsv`, DT835): a main-en a lapja az 1. kiadás (régi szerkezet, 2 025 sor). A látható szövegében ma is 73 DT-szám, 385 `.tsv` fájlnév, 12 fejlesztői hivatkozás, 2 héber számláló, 2 nyers BDB-fej áll (mérés a b5d93ea8-on, HTML-megjegyzések nélkül). A forrása és az adata viszont a #709 óta az új szerkezethez kész.
- **A HAMART-001** (3 271 sor) látható szövegében ma: 2× a hamis SECE-állapotmondat, 1× a jóváhagyás-mondat; a „Thayer-fordításból (… sz<n> sorok,; …)” töredék a #709-cel megszűnt.
- A leltár magas tételei közül a forrás szintjén már nem áll: lg_3900.28, lg_2600.14, seged_B.24, szabalyok.9 (a HAMART-only BDB-kapcsolók), és részben a „kapu csak az új ágon” csoport. A gyökérok (motívumazonosító a kódban) változatlan: a halmaz kételemű lett.
- Az `adat/generalt_nezetek.tsv` nem létezik; a #217 várakozik. **Ez a brief nem függ tőle** (4. pont).
- A `fable` érvényes fejlécérték (#727).

## 1. Cél

Új, rétegzett generátor új fájlokban, amely a visszatérő hibák négy gyökérokát szerkezetileg zárja ki:

| Gyökérok | Hibanapló | Mi zárja ki |
|---|---|---|
| a látható szöveg belső adatból, cserével készül | M-CSERE | látható-szöveg típus három konstruktorral, AST-teszt, festékpróba (2. pont) |
| ugyanazt az adatot több út olvassa | M-NYERS | bemeneti réteg, B-azonosítónként egy függvény (4. pont) |
| a javított adat mellett a nyers maradt a bemenet | M-NYERS | a nyers forrás csak a bemeneti rétegen belül; pillanatkép csak frissességi kapuval |
| motívumra szabott ágak | – | 0 motívumazonosító a `lapgen/` kódjában; minden kapu minden lapon |

**Reális terjedelem.** A teljes lap (9 szelet) becslés szerint 3–5 munkamenet. A brief szeletenként áll meg zöld állapotban; minden szelet önmagában átvehető eredmény.

## 2. Alapszabály (DT-F212e) és gépi kikényszerítése

**A szabály.** A lap látható szövege csak kézi prózából, strukturált értékű sablonmondatból vagy szó szerinti idézetből jöhet. Belső szövegből cserével olvasói szöveg nem készül. Minden belső kulcsnak olvasói neve van a névtáblában; ismeretlen kulcs kemény hiba. Proveniencia csak HTML-megjegyzésben és a Kolofonban áll. A szabály szövege a `sablonok/6_…`-ba kerül új szakaszként (F184); a brief csak hivatkozik rá.

**Kikényszerítés — három réteg, erősség szerint:**

1. **Típus (`lapgen/szoveg.py`).** A látható szöveg külön típus (`Lathato`), amelynek pontosan három konstruktora van:
   - `proza(res)` — a kézi forrás egy rése, változatlanul;
   - `sablon(kulcs, **parameterek)` — a `lapgen_sablonok.tsv` egy sora; a paraméter típusa csak enum, szám, névtábla-elem (`Nev`), igehely (`Igehely`) vagy másik `Lathato` lehet, **nyers `str` nem**;
   - `idezet(forras, hely, szoveg)` — bibliavers vagy szótárszöveg, a bemeneti rétegből, forrásmegjelöléssel.

   A megjelenítő csak `Lathato`-t fogad el. A proveniencia külön típus (`Proveniencia`), amelyet a megjelenítő csak HTML-megjegyzésbe és a Kolofonba tud írni.
2. **AST-teszt (GK-08a).** A lapmodell adatosztályaiban nincs szabad `str` mező a `Lathato`, `Nev`, `Igehely`, `Proveniencia` és a belső azonosító (`Kulcs`) típusokon kívül. A `szamitas/` és a `megjelenites/` rétegben `Lathato` értéken nincs string-átíró hívás (`replace`, `re.sub`, `translate`, `split`+`join`, szeletelés, `%`/f-string összefűzés a konstruktorokon kívül).
3. **Festékpróba (GK-08b) — ez a bizonyíték.** Egy tesztbemenetben minden belső szövegmező (`forras_kereses`, `megjegyzes`, `indoklas`, `proveniencia`, állapot- és azonosítómezők, fájlnevek, döntésszámok) egyedi jelzőszót kap (`ZZQ<mező>ZZ`). A generált lapon a jelzőszó **a HTML-megjegyzéseken kívül sehol nem állhat**; az idézet-mezők jelzőszava csak idézet-jelölésű helyen. Mindkét mintalap teljes bemenetén fut.

A grep-alapú ellenőrzés (0 `re.sub`/`.replace` a `megjelenites/` alatt) csak kiegészítés (GK-08c).

**Alakosztály-kapu, típus szerint.** A renderelt szövegen a kapu tudja, melyik rész próza, sablon vagy idézet: a sablon-eredetű szövegen minden alakosztály tilos (aláhúzásos azonosító, `.tsv`/`.py` fájlnév, `DT\d+`, `#\d{2,3}`, `N-?F?\d+`, nyers szótárfej, héber + `_\d+`, `sz<n>`, nyers `<br>`, tört írásjel `,;` `;.`); az idézeten csak a proveniencia-alakok; a prózán a mai prózakapuk. A kaput a két jóváhagyott lapon kalibrálni kell: 0 hamis találat a mai HAMART-lap prózáján és idézetein. Szólista nem kapu.

## 3. Hatókör

**Benne van.**
- `eszkozok/lapgen/`: `szoveg.py` (típusok), `bemenet/`, `konfig.py`, `szamitas/`, `megjelenites/md/`, `tesztek/`, `regresszio.py` (szakasz-diff és engedély-összevető), `festek.py`.
- Három új tábla: `adat/lapgen_bemenetek.tsv`, `adat/lapgen_sablonok.tsv`, `adat/olvasoi_nevtabla.tsv`, SEMA-bejegyzéssel.
- A TUDOMANYOS- és a KIZARASOK-nézet a HAMART-001-re és az ISTENTISZT-001-re, ideiglenes könyvtárba (a repón kívül).
- Három additív módosítás meglévő fájlban: `general.py` (`--cel lexikon2`), `elofordulasok.tsv` (T3 oszlop), `Konyv_normalizalo_tabla.tsv` (alias-sorok, GK-17). Mindháromnál az F218.1 méri, hogy a **régi** generátor HAMART-kimenete utána is bájtra azonos; ha nem, ⛔.

**Nincs benne (218b, 218c, l. 13. pont).**
- Az olvasó szerver átkötése; a `nyilt_mag_export`; a TORZSCIKK (ma mind befagyasztott motívumé).
- A `lexikon/` bármely fájljának írása; az E28, a `feladatok.yml`, az `olvasoi_kapu.py`, az `ellenoriz.py`, a `szabalyok.py` módosítása; a régi generátor archiválása.
- Új tartalom, új próza. A rések szövege nem változik.

**Befagyasztás.** A befagyasztott motívum lapját az új generátor sem írja a `lexikon/` alá. **Kimondott kivétel:** a `--kimenet <repón kívüli könyvtár>` próbagenerálás befagyasztott motívumra is fut (regressziós és átnéző cél); így lehet az ISTENTISZT-001 mérce, miközben a kiadott lapja érintetlen. A kivételt teszt fedi: `--kimenet` nélkül befagyasztott ID → kimondott kihagyás.

## 4. Bemeneti réteg — saját tábla

**`adat/lapgen_bemenetek.tsv`** (új, ez a brief írja; nem a #217 jegyzéke). Egy sor egy bemenet; a térkép B01–B64 számai változatlanok, új bemenet B65-től. A #217 `bemenetek` oszlopa majd ezekre a B-azonosítókra hivatkozik (két entitás, két tábla).

Oszlopok: `id` · `utvonal` (repó-relatív, glob, `<ID>` helyőrző; nem fájl-forrásnál `-`) · `leiras` · `kotelezo` (`igen`/`nem`) · `javitas` (a kötelező javítótábla B-azonosítója vagy `-`) · `frissesseg` (`-` / `hash:<B…>` / `strong_halmaz`) · `allapot` (`aktiv` / `kivezetve` / `nem_vizsgalt` / `reszleges`; a T7 állapotmondatai ebből és a sablontáblából jönnek) · `licenc_kulcs` (a `licencek.tsv` kulcsa) · `olvasoi_nev_kulcs` (a névtábla kulcsa) · `forras` (proveniencia).

**A réteg szerződése (`lapgen/bemenet/`):**
- B-azonosítónként egy nyilvános függvény; az útvonal a táblából jön, a kódban `adat/` vagy `konkordancia/` útvonal nincs (GK-01, statikus teszt).
- Betöltéskor kapu: létezés; **oszlopnév** szerinti fejléc; a javítótábla alkalmazva; frissesség a pillanatképeken.
- Hiányzó kötelező bemenet → BUKÁS. Opcionális hiánya → a lapmodellben kimondott hiány (enum), nem üres lista (GK-06).
- Immutábilis kimenet; gyorsítótár csak itt, a fájl hash-ére kulcsolva.
- **Olvasási napló** (B-azonosító, útvonal, hash): a Kolofon, a 12. Irodalom és a blokkfejlécek forráslistája ebből jön (GK-07); a regresszió bemenet-hash őre is ezt használja (8. pont).
- TSV: `split('\t')` / `'\t'.join()`.
- **A bemeneti függvény a szelettel együtt készül** (9. pont), nem előre mind a 64.

**Módosítások a térkép B-soraihoz képest** (a tábla `forras=manual` soraiban, okkal):

| B | Változás | Ok |
|---|---|---|
| B03 | új oszlop: `sajat_szo` (a vers saját, nem lánc-szava; T3); a `TEMATIKUS_SAJAT_SZO` megfelelője | T3, HN-16 |
| B04/B06 | a csoportos kizárás versszáma a B06 mérésből, frissességi kapuval | M13 |
| B08 | (vers, Strong) ismétlődésnél az első előfordulás (T4); az összevont 9 versnél a kulcs a versösszevonás szerint | M1, GK-14 |
| B10/B12/B13 | egy kiejtés-szolgáltatás (`kiejtes.py` + `heber_kiejtes.py` + lemma-változat) | M2, H6, GK-13 |
| B11 | `kivezetve` | O7 |
| B14 | az `allapot` mező a lapmodellbe kerül (T5) | M5, GK-15 |
| B15 | egy glossza-függvény, egyféle hiány | M10, GK-16 |
| B17 | a betűjavítás minden motívumra; az olvasói réteg is a teljesen javított szöveget kapja | GK-18, seged_B.2 |
| B20 | `thayer_bemenet.szakaszok(strong)` | M8, GK-N178 |
| B43 | csak `karoli_kh_szuro.megerositett_sorok`; az elvetett-szám a szűrő nyilvános API-jából | kapuk.1, lg_6500.18 |
| B48 | a jóváhagyás érvényessége a `lap_commit` szerint (T9) | lg_5200.31 |
| B49 | a lektor-sor egy helyen, a bemeneti rétegben olvasódik, kapuval; adattáblába költöztetése a 218c-ben | lg_5200.12 |
| B51 | a döntés dátuma a `dontes_allapot` modulból | lg_6500.5 |
| B54 | minden pár használható, szűrő és páronkénti jelölés nélkül; hiányzó könyvfájl = kimondott hiány (T6) | H10, GK-19 |
| B60 | nem bemenet (a meglévő lap) | GK-12 |
| B61/B62 | a `_lapit` és a `csoport_tagjai` logikája a `szamitas/`-ban újraírva; a régi modulok érintetlenek | O5 |
| B63 | a `KH_KONYV_JAVIT` és az `EXTRA_KONYV` sorai a normalizáló táblába | M17, H12, GK-17 |
| B65 | `adat/olvasoi_nevtabla.tsv` | 2. pont |
| B66 | `adat/lapgen_sablonok.tsv` | 2. pont |

## 5. Felépítés

`szoveg` ← `bemenet` ← `szamitas` ← `megjelenites` (egyirányú; statikus teszt). A `konfig.py` mindenkié.

- **`konfig.py`** — a spec 5. pontjának küszöbei, szűrő-halmazai és heurisztikái egy modulban, nevesített konstansként, teszttel (TSK `Votes ≥ 15`, `ALAPVONAL_*`, `LXX_TARS_KUSZOB`, `KAROLI_*`, `LXX_PAROK_TOP`, `LXX_DONTES_MEGJELENO_*`, a tő-heurisztikák, a szerző, a cím, a webcím, a DOI-k mostani értéke [T8], a Károli-párosítás mért pontossága [T6]). **Táblába csak az kerül, ami látható mondat** (sablon, név). A mondatban álló szám a konstansból formázott sablonparaméter.
- **`szamitas/`** — tiszta függvények, motívumazonosító-ág nélkül; kimenetük a lapmodell. Globális állapot nincs (GK-11).
- **`megjelenites/md/`** — a lapmodellből a TUDOMANYOS és a KIZARASOK; csak `Lathato`-t és `Proveniencia`-t ír.
- **Belépési pont:** `python eszkozok/general.py --cel lexikon2 --id <ID> --kimenet <könyvtár> [--mod munka|kiadas]`. A `--cel lexikon` változatlanul a régi generátor.

**Lapmodell.** Szakaszonként egy adatosztály: `azonosito`, `cim` (`Lathato`), `sorszam`, `horgony` (a szakaszmodellből; minden „N. szakasz” és `#horgony` ebből jön, GK-10), `szamok`, `sorok`, `hianyok` (enum + paraméter), `kovetkeztetes_kod` (enum), `forrasok` (B-azonosítók az olvasási naplóból). JSON-sorosítás nem készül.

**Két mód.** `munka`: az elavult fordítás a régi magyar szöveggel áll, „a fordítás felülvizsgálat alatt” sablonjelöléssel (T5); a jóváhagyás-mondat a `lap_commit` szerint „a szerző a lap korábbi változatát hagyta jóvá (dátum)” (T9). `kiadas`: elavult vagy hiányzó fordítás, illetve nem friss jóváhagyás → BUKÁS. **A regresszió `munka` módban mér.**

**Futásidő.** Egy lap generálása ≤ 60 s ugyanazon a gépen, ahol a régi kb. 50 s (az F218.1 méri az alapot; 1,5-szeres túllépés megállás).

## 6. Sablontábla és névtábla — a felhasználó hagyja jóvá

- **`adat/lapgen_sablonok.tsv`**: `kulcs` · `mondat` (helyőrzőkkel) · `parameterek` (név:típus) · `szakasz` · `eredet` (a régi generátor szimbóluma, ahonnan a mondat jön, vagy `uj`) · `dontes`. A mondatok a mai jóváhagyott HAMART-lap szövegét adják vissza betűre; ahol a mai szöveg hibás (HN-eset, hamis állapotmondat), az új mondat `eredet=uj`.
- **`adat/olvasoi_nevtabla.tsv`**: `tipus` (forrás / mező / állapot / szerep / háló / igazolás / azonosság) · `kulcs` · `olvasoi_nev` · `eredet`.
- **Két felhasználói átnézés, nem szeletenkénti** (a felhasználó: „ne legyen több kör”):
  - ⛔ **az első szelet (S1) után:** az új `eredet=uj` sablonmondatok és névtábla-sorok rövid listája (régi → új). Ez jelöli ki a mintát a többi szelethez; az 1. független ellenőrzéssel egy megállásban.
  - ⛔ **a 218a végén (S9):** a többi szelet összes új sora egy listában, a két renderelt lappal és az eltérés-összesítéssel egy megállásban.
- **Közben megállás csak egy esetben:** ha egy új sablonmondat olyan tartalmi állítást tesz, amelyet a mai lap nem tartalmaz (új tény, új minősítés, új számállítás). A megfogalmazás, a szórend, a névcsere és a hibás mai szöveg javítása (HN-eset) nem ilyen: ezek a végső listába gyűlnek, a folytatási fájlban vezetve.
- Az `eredet=<szimbólum>` sorok (betűre egyező mai szöveg) nem igényelnek jóváhagyást.

## 7. Követelmények

Minden sor egy teszt a `lapgen/tesztek/`-ben; az azonosító a tesztfüggvény nevében áll. **A tesztváz előre készül (F218.3): név + docstring + `skip`; a teszt törzse azzal a szelettel íródik meg, amelyik teljesíti.** A HN-esetek API-független szövegminták (bemenet: lapszöveg-részlet; elvárt: a kapu BUKÁS-a, illetve az új lapon 0 találat).

### 7.1 Szerkezeti követelmények

| ID | Követelmény | Mérhető teljesülés | Szelet |
|---|---|---|---|
| GK-01 | egy adat, egy hozzáférési pont | `adat/`, `konkordancia/`, `naplok/` útvonalat csak a `bemenet/` nyit, a tábla szerint | T |
| GK-02 | a javított változat kötelező | a nyers függvény a `bemenet/`-en kívül nem hívható | T |
| GK-03 | pillanatkép csak kapuval | elavított másolattal BUKÁS (B05, B06, B18, B19, B21, B36, B38) | szeletenként |
| GK-04 | kapu minden lapon | `lxx_egyezes`, `hely_egyseg`, `teljesseg` (strong, karoli, szotar háló), melléklet-kapu a modellen, mindkét lapon | S2, S4 |
| GK-05 | nincs motívumazonosító a kódban | `[A-Z]+-\d{3}` a `lapgen/` kódján 0 (a `tesztek/` kivételével) | T |
| GK-06 | nincs néma hiány | kötelezőnél BUKÁS, opcionálisnál kimondott hiány | szeletenként |
| GK-07 | forrásmegjelölés a valódi olvasásból | a Kolofon/Irodalom/blokkfej forrás-halmaza = olvasási napló; licencszöveg csak B01-ből | S8 |
| GK-08a | típus + AST | 2. pont 2. | T |
| GK-08b | festékpróba | 2. pont 3.; 0 szivárgás mindkét lapon | T, szeletenként bővül |
| GK-08c | grep-kiegészítés | 0 csere a `megjelenites/` alatt | T |
| GK-09 | kapu a modellen | a számegyezés-kapuk a lapmodellt olvassák | S2 |
| GK-10 | szakaszszám és horgony a modellből | szakaszrend-csere után 0 hibás belső link | S8 |
| GK-11 | nincs globális állapot | a két lap fordított sorrendben bájtra azonos | S9 |
| GK-12 | a generált fájl nem bemenet | a `lapgen/` nem olvas `lexikon/` alatti fájlt (a `regresszio.py` kivétel: referencia) | T |
| GK-13 | egy kiejtési út | H2403a/b, H2398, H7121 | S1 |
| GK-14 | TAHOT-ismétlődés: az első előfordulás (T4) | nevesített szabály, teszt; a változó sorok az engedélyfájlban | S1 |
| GK-15 | fordítás-állapot (T5) | `munka`: régi magyar + jelölés; `kiadas`: BUKÁS elavult/hiányzó fordításnál; a modell listázza az érintett sorokat | S3 |
| GK-16 | egy glossza-út | egy függvény, egyféle hiány | S3 |
| GK-17 | könyvnév egy táblából | 0 kódba írt alias | S1 |
| GK-18 | BDB-betűjavítás mindenütt | a kártya és az olvasói réteg ugyanazt a teljesen javított szöveget adja | S3 |
| GK-19 | Károli-párosítás (T6) | minden pár számít; a látható szövegben 0 bizonyossági címke és 0 páronkénti jelölés; a 95,06% egyszer, a Módszertanban, a konfigból | S3 |
| GK-21 | a HAMART regressziós kapui (sablon 597) | a Döntési út számai összeadódnak; döntés nélküli vers 0; Nave-blokk nem üres | S2, S3 |
| GK-23 | névtábla | ismeretlen kulcs → kivétel | T |
| GK-24 | alakosztály-kapu, típus szerint | 0 találat mindkét új lapon; 0 hamis találat a mai HAMART prózáján és idézetein | T, S9 |
| GK-25 | pozitív szerkezeti kapu | szakaszrend; minden igehely alatt teljes mondat + „Funkció:”; **a táblajegyzet a tábla alatt áll** (mint a HAMART 1. kiadásában; a HAMART-on ma 23 jegyzet: 17 a 2., 6 a 3. tábla alatt), rövid, egysoros, a cellát nem ismétli, nincs benne forrásnév a mondat közepén, belső név vagy tört írásjel | S1, S9 |
| GK-26 | mutációs próba | hat hibaváltozat (szivárgó mezőnév, ismételt címke, tört írásjel, jegyzet = cella, belső szám a mondatban, hiányzó „Funkció:”); mindet megfogja legalább egy kapu; jelentés kapunként | S1 (váz), S9 |
| GK-27 | jóváhagyás a lapállapothoz (T9) | `munka`/`kiadas` szerint | S8 |
| GK-28 | állapotmondat adatból (T7) | a SECE-, Peshitta-, Targum-, közel-keleti, Chain Lineage-mondat a bemeneti tábla `allapot` mezőjéből és az adat tényleges állapotából; a hamis „még nincs” mondat nem áll | S3, S7, S8 |
| GK-29 | determinizmus | a `ts=` explicit `PARDES_DATUM`-ból vagy a bemenetek hash-éből; két futás bájtra azonos | T |
| GK-30 | befagyasztás-kivétel | 3. pont | T |
| GK-31 | futásidő | 5. pont | S9 |

*Kimaradt innen (218b/218c): GK-20 (törzscikk), GK-22 (olvasó = lap), OLV-1–3.*

### 7.2 Átvett tételek

- **N-F212a:** GK-A1, A6, A10, A11, A12, A13, A14, A15, B5, B8, B9, C3, C9, D3 (a spec 6.1 táblája). A cím nélküli tételek leírását az F218.1 veszi át a `GENERATOR_HIBALELTAR_2026-11-11.md`-ből a teszt docstringjébe.
- **GK-N178 (N178):** a Thayer-kártya a `thayer_bemenet.szakaszok(strong)`-ból; a 15 érintett Strong tesztje. (S3)
- **GK-SZOPAR (DT833, korábban DT-F194h):** a spec 6.3 feltételei a main mai kódjából portolva; a `teszt_f194_szopar.py` esetei az új generátoron is zöldek. (S7)
- **A spec 5. pontja:** nem minden sorra külön teszt. A küszöbök a `konfig.py` tesztjében; a motívumkapcsoló a GK-05-ben; a holt kód nem portolandó és nem tesztelendő.

### 7.3 A hibanapló példányai (HN)

| ID | Mechanizmus | Eset | Hol él ma |
|---|---|---|---|
| HN-01 | M-CSERE | a tábla alatti jegyzet ismétli a cellát | HAMART (kisebb számban), ISTENTISZT 2. kiadás-próba |
| HN-02 | M-CSERE | címke-ismétlés: „A formula nincs a versben: Nincs meg a formula a versben…” | ISTENTISZT-próba |
| HN-03 | M-CSERE | forrásnév a mondat közepén: „(a BDB-szótár)” | mindkettő |
| HN-04 | M-CSERE | „hivatkozas_kezi,;”, „kollokacio … szerkesztő-chat … negativ_kriterium” | ISTENTISZT-próba |
| HN-05 | M-CSERE | „felhasználó”, „orkesztrátor” a lapon (#178) | javítva; teszt |
| HN-06 | M-CSERE | „gerinc” a látható szövegben | javítva; teszt |
| HN-07 | M-CSERE | „…Thayer-fordításból (… sz<n> sorok,; …)” | ISTENTISZT 1. kiadás (1×); HAMART-on a #709 óta 0 |
| HN-08 | M-CSERE | DT-szám, „#142”, „N59”, „(G10)”, „(F131, DT272 (d))” a látható szövegben | ISTENTISZT 1. kiadás (73 + 1 + 2 + 12) |
| HN-09 | M-CSERE | nyers BDB-fej „H7121. q…”, héber számláló „…_724” | ISTENTISZT 1. kiadás (2 + 2) |
| HN-10 | M-NYERS | Károli-KH: a forrásdeklaráció a nyers fájlt nevezi | mindkettő (proveniencia) |
| HN-11 | M-NYERS | teljesség-mérés pillanatképe; az ISTENTISZT-naplóban nincs `strong=` token | mérendő (F218.1) |
| HN-12 | M-NYERS | angol Thayer nyersen (N178) | mérendő (F218.1) |
| HN-15 | állapotmondat | „magyar rövid glossza-tábla a görögre még nincs” | HAMART 2×, ISTENTISZT 3× |
| HN-16 | motívum-ág | `TEMATIKUS_SAJAT_SZO` néma `replace` (Jel 22:3, G2652) | HAMART |
| HN-18 | M-ZOLD | „0 BUKÁS” ≠ minőség | a GK-26 fedi |

*A szervert érintő esetek (korábban HN-13, HN-14, HN-17) a 218b/218c N-tételeibe kerültek.*

### 7.4 A leltár nyomon követése

Az F218.1 a súlyossági leltár minden tételéhez `kovetelmeny` oszlopot ír: GK/HN/N-tétel azonosító, vagy „nem portolandó: <ok>” (CI-oldali, holt kód, a mai main-en már nem áll). A 24 magas tétel leképezése e brief 7.1–7.3 pontja; a 272 közepes tételé az F218.1 kimenete. Leképezetlen tétel a lezáráskor nem maradhat.

## 8. Regressziós mérce

### 8.1 HAMART-001 — szakaszonkénti bájt-egyezés, darabszámhoz kötött engedéllyel

- **Referencia:** a main-en commitolt `lexikon/HAMART-001_TUDOMANYOS.md` és `_KIZARASOK.md` az F218.1 commitján. Az F218.1 ellenőrzi, hogy a régi generátor rögzített `PARDES_DATUM`-mal bájtra ugyanezt adja.
- **Bemenet-hash őr:** a `naplok/F218_referencia.tsv` rögzíti a referencia hash-ét és **minden olvasott bemenet hash-ét** (az új generátor olvasási naplója + a régi generátor B-sorai + a `motivumok/HAMART-001.md`). Ha egy hash a main változása miatt eltér, a `regresszio.py` kimondott hibával megáll („a mérce bemenete megváltozott: <B…>”); a referencia újrafelvétele külön commit, okkal.
- **Engedélyfájl** (`naplok/F218_elteres_engedely.tsv`): `id` · `szakasz` · `mechanizmus` (HN/GK/T) · `kotes` (`sor`: a régi és az új sor hash-e; vagy `minta`: régi minta → új minta) · **`elvart_db`** · `ok`.
  - Minden diff-sor pontosan egy engedélysorhoz tartozik, különben BUKÁS.
  - **A fel nem használt és a túlhasznált engedélysor is BUKÁS** (`tenyleges_db ≠ elvart_db`).
  - **Az `elvart_db` előre áll:** az F218.1 alapmérés osztályonként megszámolja a mai lapon a HN-esetek és a T-döntések által érintett sorokat, és ezt rögzíti a jelentésben. Az építő session az engedélysort ebből tölti; ha egy osztály tényleges száma 20%-nál jobban eltér az előre rögzítettől, megállás és ⛔ (a küszöb becslés).
  - A független ellenőr az engedélysorokból mintát vesz; a felhasználó az osztályonkénti összesítést látja.
- **Előre ismert eltérés-osztályok:** (a) `ts=`; (b) a forrásnév a valóban olvasott javított forrást nevezi (GK-07, HN-10); (c) a Thayer-szöveg, ha érintett (GK-N178); (d) T4: a kiejtés az első előfordulásból; (e) az N-F212a javításai; (f) HN-01, HN-03 (jegyzet, forrásnév helye); (g) HN-15 (a hamis SECE-mondat, 2 db); (h) T9: a jóváhagyás-mondat `munka` módban (1 db); (i) T7: az állapotmondatok, ha a szövegük változik.
- **A „HAMART-on a várt diff kicsi” állítás nincs megmérve.** Az első szelet ennek a próbája (9. pont, megállási szabály).

### 8.2 ISTENTISZT-001 — bájt-diff nincs

A kiadott 1. kiadás ismerten rossz referencia. A mérce:
1. **Számok:** a lapmodell számai (igehely-halmazok, Döntési út, LXX-összesítés, KH-darabszám, szópár-lánc) az adattáblákból független számlálással egyeznek (a `regresszio.py` saját, egyszerű számlálói; nem a generátor kódja).
2. **Szerkezeti kapuk:** GK-04, GK-24, GK-25, GK-SZOPAR zöld.
3. **Festékpróba:** 0 szivárgás.
4. **A HN-esetek száma az új lapon 0** (HN-02, 04, 07, 08, 09, 15).
5. ⛔ **A felhasználó olvasata** a renderelt lapon (a memória szerint: a lapot megnyitva).

## 9. Lépések — függőleges szeletek

Minden szelet: bemeneti függvények → számítás → sablonmondatok és nevek → megjelenítés → **szakasz-diff 0** (HAMART) → az ISTENTISZT ugyanazon szakasza a 8.2 szerint → tesztek zöldek → commit(ok) → push. Commit: `F218.<t>: …`, legfeljebb kb. 400 sor vagy 1–2 óra munka; minden commit zöld tesztekkel áll meg.

**Előkészítés — olcsó modellel (sonnet), az építő session előtt.** *Kimondott kivétel a fejléc `modell` mezője alól: ez a két tétel nem tervez és nem ír generátorkódot.*
- **F218.0** — modell-ellenőrzés; a `fuggesek` kimenete egyezik a fejléccel; `get_usage` (a heti keret és a Fable-plafon állása a jelentésbe).
- **F218.1** — referencia és alapmérés:
  - a HAMART-referencia és a bemenet-hashek (`F218_referencia.tsv`); a régi generátor futásideje;
  - a három additív módosítás (`--cel lexikon2` váz, T3 oszlop, alias-sorok) után a régi generátor HAMART-kimenete bájtra azonos (ha nem: ⛔);
  - osztályonként a várt eltérés-darabszám (8.1); a HN-esetek száma és helye a két mai lapon;
  - T4: hány sor kiejtése változik; N178: a 15 Strong érintettsége; az `elavult` fordítások érintettsége;
  - a leltár `kovetelmeny` oszlopa (7.4);
  - a régi generátor **szimbólumtérképe szakaszonként** (melyik függvény melyik lapszakaszt adja, mai sorszámmal), hogy az építő session a 10 153 sort soha ne olvassa egészben.

**Tervezés és az első két szelet — fable, xhigh.**
- **F218.2 (T)** — típusok és szerződések: `szoveg.py`, a bemeneti réteg váza és a tábla, a névtábla- és sablonbetöltő, a `regresszio.py` (szakasz-diff, engedély-összevető, bemenet-hash őr), a `festek.py`; GK-01, 02, 05, 08a–c, 12, 23, 29, 30 zöld.
- **F218.3** — a tesztváz (7. pont): név, docstring, `skip`; a HN-szövegminták.
- **F218.4 (S1)** — **„2. Előfordulások” és „2.1 Az igehelyek szövege”**, táblajegyzettel, a T3 és a T4 döntéssel, HN-01, HN-03, HN-16; GK-13, 14, 17, 25; a mutációs próba váza. *Ez a „kicsi diff” próbája.*
  - ⛔ **Független ellenőrzés (1.)** az S1 után: típusok, festékpróba, szerződések, az engedélysorok mintája. Egy javítókör. **Ugyanebben a megállásban** kapja a felhasználó az S1 új sablonmondatait és neveit (6. pont; a két felhasználói kör közül az első). Az ellenőr modellje nem Fable (ha a `fuggetlen-ellenor` fájlja Fable-t adna, megállás).
- **F218.5 (S2)** — „1. Döntési út” (1.1–1.5) és a KIZARASOK-melléklet; GK-04 (teljesség minden hálóra), GK-09, GK-21, HN-11.

**A további szeletek — fable, high** (szeletenként új session a `naplok/F218_folytatas.md`-ből).
- **F218.6 (S3)** — „4. Szótári háttér”: Áttekintés, 4.1–4.10 (BDB/Thayer-kártya), 4.12 Nave, 4.13/4.14; GK-15, 16, 18, 19, N178, HN-15. Szükség szerint két-három commitra bontva (4.1–4.5 · 4.6–4.10 · 4.11–4.14).
- **F218.7 (S4)** — „5. LXX-fordítói döntések”; `lxx_egyezes` a modellen.
- **F218.8 (S5)** — „6. Kereszthivatkozások” és a Minősítés; HN-10, GK-A1.
- **F218.9 (S6)** — „7. Kapcsolatok”, Alátámasztás, „8. Kapcsolódó motívumok”.
- **F218.10 (S7)** — „9. Hatástörténet” (ÓSZ, ÚSZ, tanúk), a szópár; GK-SZOPAR, GK-A6, GK-28.
- **F218.11 (S8)** — a keret: cím, Tartalomjegyzék, Jelmagyarázat, a rések (Kivonat, Miért fontos, 10., 11.), „12. Irodalom és idézés”, Kolofon; GK-07, 10, 27, 28.
- **F218.12 (S9)** — a teljes lap: HAMART teljes diff 0 engedélyen kívül; az ISTENTISZT 8.2 szerint; GK-11, 24, 26, 31; a festékpróba mindkét teljes bemeneten.
  - ⛔ **A felhasználó** (a második, egyben utolsó kör) megnyitja a két renderelt lapot, és megkapja az osztályonkénti eltérés-összesítést meg az S2–S9 összes új sablonmondatát és nevét egy listában (6. pont).
  - ⛔ **Független ellenőrzés (2.)**, egy javítókör.
- **F218.13** — zárás: jelentés, mérőszámok, a 13. pont N-tételei a `nyitott/uj/<ágnév>.md`-be; `kovetkezo`: „Te: a 218b és a 218c befogadása”.

**Folytatási fájl.** A `naplok/F218_folytatas.md` **minden commitban** frissül: kész szeletek; nyitott diff-sorok szakaszonként; a következő lépés; a régi generátorból visszafejtett mondatszabályok (ezeket veszíti el először a kompaktálás); a mérőszámok sora.

**Olvasási fegyelem.** A régi generátort szimbólum szerint, a szelethez tartozó függvényenként olvasni; a diff fájlba megy, a kontextusba csak az összesítés; a mintalapot egészben nem olvasni (memória: cikk-session kontextus).

**Push.** Szeletenként, vázlat-PR az első committól, hogy a CI minden push után fusson. *Ehhez a felhasználó előzetes engedélye kell az ágra (a szabály szerint push csak kérésre megy): a /befogad kérdezze meg.*

**Megállási szabály.** Ha az építő session indulásakor mért maradék heti keret **felének** elfogyásáig az S1 szakasz-diffje nem 0 (engedélyen kívül), megállás: jelentés a diff-maradék osztályairól, és újratervezés a felhasználóval. Ugyanígy megállás, ha egy eltérés-osztály 20%-nál jobban eltér az előre rögzítettől, vagy a futásidő 1,5-szeres.

**Mérőszámok** (a jelentés és a folytatási fájl táblájában; napló, nem modell-összevetés):
- szeletenkénti keretfogyás (`get_usage` a szelet előtt és után, százalékpont egy zöld szeletre);
- diff-görbe: engedélyen kívüli diff-sorok szakaszonként, commitonként; az engedélysorok száma osztályonként;
- festékpróba: szivárgások száma futásonként; mutációs próba: megfogott / összes;
- **átszökési arány:** a zöld kapuk után a felhasználó és az ellenőr által talált hibák, mechanizmus szerint (a `HIBA_MECHANIZMUSOK.md`-be is);
- átírás: a `lapgen/` később módosított sorainak aránya; session-váltások és kompaktálások száma.

## 10. Technikai döntések (a brief írója döntötte el)

- **O1 — nincs új ellenőrző kör** a térképre. A leltár elkészült; a magas tételeket saját grep ellenőrizte; a közepeseket az F218.1 képezi le követelményre.
- **O2 — saját bemeneti tábla** (`lapgen_bemenetek.tsv`), nem a #217 jegyzéke. A #217 `bemenetek` oszlopa hivatkozik majd a B-azonosítókra. *(A v1 itt egy meg nem írt formátumra épített; javítva.)*
- **O3 — a 4.11 egysoros mutató marad** a 9. szakaszra, a szakaszmodellből generált horgonnyal (a 4.12–4.14 számozása nem mozdul).
- **O4 — a `fordit.py`/`emeles.py` sorsa a 218c-ben** dől el, mérés után.
- **O5 — a szerver a `szamitas/`-t importálja majd** (218b), nem JSON-pillanatképet olvas; ezért JSON-sorosítás itt nem készül. A futásidő-mércét a 218b rögzíti.
- **O6 — a mai lapszöveg-kapukhoz ez a brief nem nyúl.** Az új generátor a saját kapuit a modellen futtatja; a régiek átírása a 218c-ben.
- **O7 — a `TBESH_konszolidalt` (B11) kivezetve.**
- **O8 — a holt kód nem portolandó**, külön mérés nélkül.
- **Táblák száma:** három (bemenet, sablon, névtábla). A forrás-állapot (T7) a bemeneti tábla `allapot` oszlopa; a küszöbök és a kiadási azonosítók (T8) a `konfig.py` konstansai; az engedélyfájl napló, nem adattábla.
- **Nincs 6 ügynökös PR-átnézés.** Két független ellenőrzés van, és a felhasználó olvasata.

## 11. Elfogadási feltételek

1. A HAMART-001 új lapja a referenciától csak az engedélyfájl sorai szerint tér el; minden engedélysor `tenyleges_db = elvart_db`; a bemenet-hashek egyeznek.
2. Az ISTENTISZT-001 új lapja a 8.2 öt pontját teljesíti.
3. A festékpróba 0 szivárgást ad mindkét teljes bemeneten; a mutációs próba mind a hat változatát megfogja egy kapu.
4. A 7. pont tesztjei zöldek, `skip` nem marad (kivéve a 218b/218c-re jelölteket, kimondva).
5. A `lapgen/` kódjában 0 motívumazonosító és 0 útvonal a `bemenet/`-en kívül; a régi generátor HAMART-kimenete a brief végén is bájtra azonos a referenciával.
6. A felhasználó a két renderelt lapot megnyitotta, és az új sablonmondatokat, neveket jóváhagyta.
7. A két független ellenőrzés `TISZTA`, vagy az egy-egy javítókör után az.
8. A leltár minden tétele követelményre vagy „nem portolandó”-ra van képezve.

**Részleges lezárás.** Ha a keret vagy a megállási szabály a 9 szelet előtt megállít, a brief `megallt` állapotba kerül a kész szeletekkel; a folytatás a folytatási fájlból indul. A kész szelet ettől még érvényes eredmény.

## 12. Döntésnapló

*A T1 és a T2 eldőlt (a felhasználó, 2026-11-13): az ISTENTISZT-001 az új generátorral jön ki (DT835); egy lapszerkezet marad; a befagyasztott lapok nem generálódnak csendben. A T3–T9 válaszai a döntési oldalról (https://claude.ai/artifact/7bH2eSKPfcrasLA9aSBqB2, `dontesek` gyűjtemény, kiolvasva 2026-11-13); a T5 és a T6 szövegét az orkesztrátor is továbbította, a két forrás szó szerint egyezik. Az átdolgozás a döntéseken nem változtatott.*

| T | Kérdés | Válasz | Forrás |
|---|---|---|---|
| T3 | A Jel 22:3 saját szava (G2652) adatba kerül-e, és kapjon-e szócikket? | **Adatba kerül, szócikk nélkül**: külön „a vers saját szava” mező az előfordulás-táblában (`sajat_szo`); a 4. szakasz nem kap róla szócikket | a felhasználó, döntési oldal, 2026-11-13 (gomb: „Adatba kerül, szócikk nélkül”) |
| T4 | Ha egy szó kétszer áll egy versben, melyik alak kiejtése álljon? | **Az első előfordulás** a vers szövegrendje szerint; a változó sorok az engedélyfájlban | a felhasználó, döntési oldal, 2026-11-13 (gomb: „Az első előfordulás”) |
| T5 | Elavult magyar fordítás helyett mi álljon? | **Munka közben a régi magyar szöveg áll, jelölve; kiadni elavult fordítással nem lehet (kapu); az érintett sorokat a cikk menete újrafordíttatja.** A megjegyzés az irányadó, nem a gomb | a felhasználó, döntési oldal, 2026-11-13, szó szerint: „Kiadás előtt újra kell fordítani. Kapu tiltja, hogy egy lap elavult fordítással kiadásra kerüljön. Az érintett sorokat a cikk menete újrafordíttatja, ahogy korábban döntöttél: az új cikk hiányzó fordításai az előfizetésből készülnek. Munka közben a piszkozatban a 2. változat áll” |
| T6 | Kell-e bizonyossági küszöb a Károli–Strong párosításra? | **Nem kell.** Minden párosítás használható; a mért pontosság egyszer, a Módszertanban áll; páronkénti bizonytalan-jelölés nincs; a címke belső | a felhasználó, döntési oldal, 2026-11-13, szó szerint: „Minden párosítás használható; a mért pontosság (95%, F172) egyszer, a módszertanban áll; páronkénti bizonytalan-jelölés nincs; az alacsony/magas címke belső, nem jelenik meg.” Előzmény a chatben: „ez igy nagyon bizonytalannak hat az olvasónak / miközben a mérésünk jók” |
| T7 | A forrás-állapotot leíró mondatok szövege marad-e? | **Adattáblából, az állapot szerint**; a mai mondatok a kiinduló értékek, a táblát a felhasználó hagyja jóvá. *Megvalósítás: a bemeneti tábla `allapot` oszlopa + a sablontábla mondatai (nem külön tábla).* | a felhasználó, döntési oldal, 2026-11-13 (gomb: „Adattáblából, az állapot szerint”) |
| T8 | A szerző neve, a lexikon címe, a webcím és a DOI-k hova kerülnek? | **A mostani értékek mennek át**, változatlanul, egy helyre. *Megvalósítás: a `konfig.py` nevesített konstansai (nem külön tábla).* | a felhasználó, döntési oldal, 2026-11-13 (gomb: „A mostani értékek mennek át”) |
| T9 | Mit mondjon a Kolofon, ha a szerző a lap egy korábbi változatát hagyta jóvá? | **Kiadott lap csak friss jóváhagyással**: `munka` módban „a szerző a lap korábbi változatát hagyta jóvá (dátum)”; `kiadas` módban a `lap_commit` egyezése kötelező | a felhasználó, döntési oldal, 2026-11-13 (gomb: „Kiadott lap csak friss jóváhagyással”) |

**A T6 indoklása.** A `parok_<könyv>.tsv` `bizonyossag` mezője nem mért bizonytalanság, hanem a párosítás módjának címkéje: a „magas” az 1–2Móz, ahol két modell egyezett; az „alacsony” a többi könyv. A mérés szerint az összes pár 95,06%-ban helyes (93,81–96,32; 1 600 pár, 8 réteg), a külső összevetésben a fő-szó párok 98,72%-ban (98,22–99,08; n = 2 663), rétegenként 92–99%. *Proveniencia: `scope=naplok/KAROLI_PONTOSSAG_jelentes.md 11., 14., 55. sor | forras=cf68d0a9 | ts=2026-11-13`.*

**A táblajegyzetek helye (nem nyitott kérdés).** A felhasználó döntése (az orkesztrátor közvetítésével, 2026-11-13): a táblajegyzetek a tábla alatt maradnak, ahogy a HAMART 1. kiadásánál eldőlt, és az új generátorban is így lesz; a mostani forma megtartandó (GK-25). A jegyzet áthelyezése tehát nem szándékolt eltérés, a regresszióban BUKÁS.

**Két megvalósítási megjegyzés, amelyet a befogadó erősítsen meg a felhasználóval** (a döntés tartalma nem változik, csak a helye): a T7 „adattáblája” a bemeneti tábla egy oszlopa; a T8 „beállítótáblája” egy konfig-modul. Ha a felhasználó külön, kézzel szerkeszthető táblát akar, az egy-egy új sor az `ir`-ben.

## 13. Külön befogadásra váró tételek (N-tételek; az F218.13 írja a `nyitott/uj/<ágnév>.md`-be)

- **N-F218b — 218b: az olvasó szerver átkötése a lapmodellre.** `fugg: [218]`. A szerver blokkjai a `lapgen/szamitas/`-t hívják („egy számítás, két megjelenítés”).
  - OLV-1: a kiejtés a lap kiejtés-szolgáltatásából, nem a `strong_szotar.kiejtes` mezőből (`lekerdezesek.py`) és nem a `token_eredeti.kiejtes`-ből; teszt: H2398, H7121.
  - OLV-2: a szótári fordítás ugyanazon a bemeneti ponton, mint a lap (F213-eset).
  - OLV-3: a szerver felülete ugyanazt a névtáblát és alakosztály-kaput használja („lxx_bridge”, „token_par”, „(#121)”).
  - GK-22: a szerver és a lap számai gépi összevetésben azonosak.
  - Futásidő-mérce szerverblokkra (kérésenkénti számítás, pillanatkép nélkül).
  - Ütközik a #121-gyel (`blokkok.py`, `lekerdezesek.py`, `forditasok.tsv`): valódi `fugg` vagy sorrend kell.
- **N-F218c — 218c: átállás.** `fugg: [217, 218]`.
  - A #217 jegyzékének G01/G02 sora az új generátorra mutat; a `bemenetek` oszlop a `lapgen_bemenetek.tsv` B-azonosítóira hivatkozik.
  - Az E28 és a `feladatok.yml`/#217 Action az új generátorral; a `--cel lexikon` az újra mutat.
  - A lapszövegre kereső kapuk átírása a modellre (`olvasoi_kapu.py`, `ellenoriz.py` lapszöveg-szabályai, E38, E39; HN-17: a „3. LXX” előtagú kapu), a fogyasztóikkal egy commitban.
  - **Visszaút:** a régi generátor egy kiadásig futtatható marad külön célnévvel (`--cel lexikon_regi`); archiválás csak utána.
  - Archiválás: a `lexikon_general`-t 53 fájl említi vagy importálja; fogyasztónkénti átkötés, nem egy commit; `archivum/lexikon_general/`, `ARCHÍV` fejléccel; a hivatkozások frissítése (E27).
  - GK-20: a TORZSCIKK a lapmodellből; B62: a `nyilt_mag_export` körkörös függése; B49: a lektor-sor adattáblába (`kiadasok.tsv`); O4.
  - A valódi függések, amelyeket a v1 `nem_fugg`-listája elfedett: #212 (F212-kapuk, `ellenorzes.yml`, `karoli_kh_szuro.py`), #178 (`olvasoi_kapu.py`, `ellenoriz.py`), #181 (`karoli_kh_szuro` API), #203 (Thayer-lánc), #70 és #123 (a mérce-motívumok forrása).
  - Utána: az ISTENTISZT-001 2. kiadása (`/kiadas`), a befagyasztás feloldásával.

---

## Változáslista (v1 → v2, 2026-11-13)

1. **Három részre bontva.** Ez a brief a 218a (építés a regresszióig). A szerver-átkötés és az átállás N-tétel a 13. pontban.
2. **Fejléc:** `modell: fable`; `fugg: []`; az `ir` a 218a hatókörére szűkítve és pótolva (`general.py`, `elofordulasok.tsv`, `Konyv_normalizalo_tabla.tsv`, a 6-os sablon, a jelentés, a folytatási, a referencia- és az engedélyfájl); kikerült belőle a szerver, a lexikonlapok, az `olvasoi_kapu.py`, az `ellenoriz.py`, a `szabalyok.py`, a `generalt_nezetek.tsv`, az archívum. `nem_fugg`: 3 tétel, indokkal.
3. **Nem függ a #217-től:** saját bemeneti tábla (`adat/lapgen_bemenetek.tsv`); a v1 4. pontja és O2-je egy nem létező formátumra épült.
4. **A csere gépi tiltása:** látható-szöveg típus három konstruktorral, AST-teszt, festékpróba. A grep-alapú szabály kiegészítés lett.
5. **HAMART-regresszió:** engedélysor kötéssel és elvárt darabszámmal; a fel nem használt és a túlhasznált sor is BUKÁS; az osztályonkénti várt szám előre áll (F218.1); bemenet-hash őr.
6. **ISTENTISZT:** bájt-diff nincs; mérce a számok, a szerkezeti kapuk, a festékpróba, a HN-esetek 0 száma és a felhasználó olvasata. A befagyasztás alól a repón kívüli próbagenerálás kimondott kivétel.
7. **Függőleges szeletek** (9 szelet) a vízszintes fázisok helyett; az első: „2. Előfordulások” + 2.1. A tesztváz `skip`-pel készül előre, nem bukó tesztekkel.
8. **Futtatás:** F218.0–1 olcsó modellel; xhigh csak a típusokra és az első két szeletre, utána high; két független ellenőrzés (nem Fable); folytatási fájl minden commitban; push szeletenként (előzetes engedéllyel); megállási szabály; mérőszámok.
9. **Kivágva:** a konfig-, a forrás-állapot- és az engedély-adattábla (három tábla maradt); a JSON-sorosítás; a 6 ügynökös átnézés; a spec 5. pontjának soronkénti TS-tesztjei; a szerver és a TORZSCIKK.
10. **Felhasználói körök:** kettő (az S1 után és a végén), nem szeletenként; közben megállás csak új tartalmi állítást tevő sablonmondatnál.
10a. **Új:** két mód (`munka`/`kiadas`), a regresszió `munka` módban mér; futásidő-mérce; típus szerinti alakosztály-kapu kalibrálással; ⛔ a sablonmondatok és nevek jóváhagyására; a leltár `kovetelmeny` oszlopa.
11. **A 0. pont:** a sorszámok és az állapot a mai main (b5d93ea8) szerint; a leltár forrásszinten már nem álló magas tételei megnevezve.
12. **Változatlan:** a T3–T9 döntések és forrásaik. Két megvalósítási megjegyzés a 12. pont végén (T7, T8 helye) megerősítésre vár.

**Amit ez az átdolgozás nem végzett el:** a `nem_fugg` három tétele a Fable-válasz és a fájllista alapján becslés, a `feladatok.py fuggesek` nem futott rá; a 272 közepes leltártétel leképezése az F218.1 feladata; a HN-01 és a HN-03 mai darabszáma nincs megmérve.
