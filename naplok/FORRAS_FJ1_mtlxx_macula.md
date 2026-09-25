# FORRAS_FJ1_mtlxx_macula.md — 3a: szószintű MT–LXX-illesztés

*FJ1 — FORRASJELOLTEK_BRIEF.md §3, G3 szerint mindkét jelölt mérve.*

## 1. Letöltés, szerkezet

### CenterBLC/MT-LXX
- **URL:** `github.com/CenterBLC/MT-LXX` · **commit:** `e9d803e36ea7da91ab37d8f7603dd2340c206ec2`
  (a repó gyökér méretes, ~834 MB, ezért `_nyers/`-be nem került be, `/tmp`-ben maradt)
- **Szerkezet:** Text-Fabric adathalmaz (`tf/0.0.8/*.tf`, 52 feature-fájl) + forrás-XML
  (`xml/2025-04-24/<NN-KÖNYV>/*-lowfat.xml`, 39 ÓSZ-könyv, csak protokanonikus).
  A TF fejléc (`ref.tf`, `greekstrong.tf` stb.) `@dataSource=MACULA Greek Linguistic
  Datasets… github.com/Clear-Bible/macula-hebrew/blob/main/WLC/lowfat` —
  **ez a jelölt a Macula Hebrew lowfat-XML-jét Text-Fabricbe konvertálja**, nem önálló
  illesztés. A `@converterSourceLocation` és `@dataSourceLocation` mezők
  `sergeypanfilov[tobecreated]/tflxx[tobecreated]` — a konverter forráskódjának
  saját repója **soha nem lett közzétéve** (helyőrző szöveg maradt a fejlécben).
- **Licenc:** **nincs LICENSE- vagy README-fájl a repóban** (`grep -rli
  "license|copyright|CC BY|public domain"` nulla találat). Idézhető licencszöveg
  nem létezik. A D17 szerint ez önmagában kizáró ok.
- **sha256** (minta, `tf/0.0.8/greekstrong.tf`):
  `e4c020d7e601ed6468070b08e3552dbabd529a22f4557cc380d7a33b24bff03`

### Macula Hebrew (Clear-Bible)
- **URL:** `github.com/Clear-Bible/macula-hebrew` · **commit:**
  `47db250bd55d0d8577f2a94fba114ef16c35b23c`
- **Szerkezet:** `WLC/lowfat/<NN-Könyv>-<fejezet:03d>-lowfat.xml`, szó-szintű
  `<w>` elemek `lemma`, `strongnumberx` (héber Strong), `greek`, `greekstrong`
  (görög lemma + Strong) attribútumokkal — **ugyanaz az adat**, amit a CenterBLC
  Text-Fabricbe konvertált, csak közvetlenül, licenccel.
- **Lefedettség (ez a session, sparse-checkout `WLC/lowfat`):** 930 fájl, 33
  protokanonikus könyv. **Hiányzik: 1Sám, 2Sám, 1Kir, 2Kir, 1Krón, 2Krón**
  (a repó jelenlegi állapotában ezek a könyvek még nincsenek feldolgozva —
  valódi forráskorlát, nem letöltési hiba).
- **Licenc (szó szerint, `LICENSE.md`):**
  > "MACULA Hebrew Linguistic Datasets, available at
  > http://github.com/Clear-Bible/macula-hebrew/ © 2022-2024 by Biblica, Inc
  > is licensed under CC BY 4.0."
  A README szerint az adat tartalmaz "Greek equivalents drawn from the
  Septuagint" és "Strong's numbers for both Hebrew and Greek equivalents" —
  tehát a szó-szintű MT→LXX-illesztés **dokumentáltan a Macula Hebrew saját
  adatkészlete**, a CenterBLC csak átcsomagolja.
- **sha256** (`LICENSE.md`): `df45ba3224e7d6f9dba3ec8fd2d0b3f1d2febb2620147c889667886fccd4d8e1`
  (`WLC/lowfat/01-Gen-001-lowfat.xml`): `523856a1f2953408d847e8d3fcc231f2bd681e540aa91c349cd9c4e128f30f6`

**Macula Greek (Clear-Bible/macula-greek) licence e menetben nem lett
külön ellenőrizve** — mivel a szó-szintű görög megfelelő már a Macula
Hebrew `WLC/lowfat` fájljaiban benne van (a `greek`/`greekstrong`
attribútumokban), a Macula Greek repóra ehhez a feladathoz nincs
szükség; a G3 által előírt licenc-ellenőrzés emiatt nem releváns erre a
konkrét 3a-célra.

## 2. Aranykészlet-mérés (K4: szkript `naplok/FORRAS_FJ1_mtlxx_illesztes.py`
ill. `naplok/FORRAS_FJ1_macula_illesztes.py`, kimenet `naplok/FORRAS_FJ1_mtlxx_teszt.tsv`
ill. `naplok/FORRAS_FJ1_macula_teszt.tsv`)

**Módszer:** az A-halmaz (123 "egyező" sor, mind a 8 lexikon-TUDOMANYOS táblából,
`naplok/FORRAS_FJ1_arany.tsv`) minden sorára: az igehelyet (`1Móz 37:35` stb.)
a `Konyv_normalizalo_tabla.tsv`-vel a jelölt könyvkódjára fordítva megkeresi a
megfelelő verset a jelölt XML-jében, és megnézi, hogy a táblázat "Görög
megfelelő" oszlopában szereplő Strong-szám (pl. `G0086`) előfordul-e **a vers
bármely szavának `greekstrong` attribútumában** (verzió-szintű, nem
szigorúan szó-szintű teszt — enyhébb mérce, tehát felső becslés).

| Jelölt | A mérhető sorai | TALALAT | Arány | B (LD001–004) |
|---|---|---|---|---|
| CenterBLC/MT-LXX | 123 | 97 | **78,9%** | 4/4 |
| Macula Hebrew | 115 (8 sor kimaradt: 2Sám/1Krón hiánya) | 90 | **78,3%** | 4/4 |

C (3 "eltérő" sor): mindkét jelöltnél mind a 3 TALALAT — ezek csak jelentésre
voltak szánva, nem küszöbre.

**B-részletek (LD001–LD004), mindkét jelöltön azonos, szó-szintű pontossággal
ellenőrizve:**
- LD001 (2Móz 33:19, H7121 קָרָא → G2564 καλέω): **pontos találat**
  (`greekstrong="2564"`, `greek="καλέσω"`).
- LD002 (2Móz 34:5, ugyanaz): **pontos találat** (`greek="ἐκάλεσεν"`, `2564`).
- LD003 (Ézs 12:4, H7121 → G0994 βοάω): **pontos találat** (`greek="βοᾶτε"`, `994`).
- LD004 (Zsolt 116:17, LXX-minusz): a jelölt adat **maga is None/None**-t ad a
  קָרָא szóra (nincs görög megfelelő rendelve) — ez pontosan megerősíti a
  kutatói döntést (a LXX valóban nem fordítja a vers második felét).

**Miért csak ~78–79%, nem magasabb:** mintavizsgálat (Jób 26:6, H7585 שְׁאוֹל
→ várt G0086 ᾅδης) megmutatta, hogy a jelölt adat **nem 100%-ban teljes
szó-szintű illesztés**: a שְׁאוֹל szónak a Jób 26:6-ban `greek=None,
greekstrong=None` van rendelve (nincs görög társ rögzítve), holott az
LXX_OS versszintű adat szerint a vers *tartalmazza* a ᾅδης szót. A verzió-szintű
teszt (bármely szó a versben) ennél enyhébb mérce, mint egy szigorú szó-szintű
teszt lenne — tehát a valós szó-szintű pontosság **legfeljebb** ennyi, valószínűleg
kevesebb.

## 3. Verdikt a §1 küszöbei szerint

Egyik jelölt sem éri el a 90%-ot az A-halmazon → **egyik sem "beválik", egyik
sem "feltétellel"** — mindkettő a **"nem: < 90% → D14 marad (versszintű)"**
ágba esik. A B-halmaz 4/4-es teljesítménye önmagában nem elég, mert a §1
szövege "és"-t ír elő a "beválik" ágban, a "feltétellel" ágban pedig az A-nak
90–95% között kellene lennie — 78–79% ez alatt is van.

**G3 rangsor** (ha mindkettő beválna, a magasabb A-egyezésű a javasolt): mivel
egyik sem vált be, ez a szabály formálisan nem lép életbe. Ha egy jövőbeli
menetben a küszöböt puhábbra vennék, vagy csak forrásjavaslatként kérdeznék:
**a Macula Hebrew a javasolt a kettő közül**, mert (a) azonos alapadat, gyakorlatilag
azonos mérőszám, (b) **licence van** (CC BY 4.0, szó szerint idézve fent),
a CenterBLC/MT-LXX-nek **nincs**, ami a D17 szerint önmagában kizárja az
importra javaslást.

**S13-ra (versszintű együtt-előfordulás kiváltása):** nem javasolt — a
szó-szintű illesztés jelenlegi pontossága (~78%) nem elég megbízható ahhoz,
hogy a SZOTAR S0.8 versszintű co-occurrence-ét kiváltsa; az félrevezető
lenne, mert hamis pozitív/negatív arányban rosszabb, mint amit a jelenlegi
módszer explicit "zajos" jelzése mutat.

## 4. A 87 függő LXX-hely munkalapja (`naplok/FORRAS_FJ1_lxx_jeloltek.tsv`, csak
munkalap, `adat/`-ba NEM kerül, G4 szerint)

Mind a 87 "kutatói azonosítás függőben" sor feldolgozva a Macula Hebrew
adatból (szó-szintű keresés lemma/unicode-egyezés alapján a heber_kulcsszó
oszlop transzliterált tokenjéhez):

| Állapot | Darab | Jelentés |
|---|---|---|
| `javasolt` | 58 | van görög lemma+Strong javaslat (kézi megerősítésre vár, l. brief G4 / 4c) |
| `nincs_konyv` | 13 | 2Sám / 1Krón — a Macula Hebrew jelenleg nem fedi ezeket a könyveket |
| `nincs_szoszintu_talalat` | 9 | a transzliterált héber token nem illeszkedik egyértelműen egy szóra (kézi ellenőrzés kell) |
| `nincs_gorog_parositas_LXX_minusz_v_hianyos` | 5 | a héber szónak nincs görög társa rögzítve (LXX-minusz-gyanú, l. LD004 mintája) |
| `nincs_vers` | 2 | a vers nem található a jelölt fájlban |

A `bizonyossag` oszlop minden `javasolt` sornál **"kozepes"** (nem magasabb) —
a §2 A-halmazon mért ~78%-os pontosság miatt egyik javaslat sem tekinthető
automatikusan elfogadhatónak; mindegyik a `LEXIKON_LEZARAS_BRIEF.md` 4c
kézi döntési körébe tartozik.

## 5. G8 — NYITOTT 1. tétel (`morphology.sqlite` `ClauseID`)

A Macula Hebrew `WLC/lowfat` XML-je `<wg class="cl" rule="...">`
tagmondat-csoportokat ad (l. a Jób 26:6 minta: `<wg role="v" class="cl">`
elemek), amelyek **funkcionálisan lefedik** a NYITOTT 1. tételben leírt célt
(a formula-motívum-kutatáshoz szükséges tagmondat-szintű csoportosítás) —
a `<wg>`-elemek `xml:id`-je és beágyazása ugyanazt az információt hordozza,
mint amit a `morphology.sqlite` `ClauseID` mezeje adna. **Javaslat:** a
`morphology.sqlite`/Google Drive-integráció (file ID `11QfpwEd5fjdDglPiqzygLNN99AVz2mw5`)
technikai költsége minden bizonnyal elkerülhető, ha a Macula Hebrew
`<wg class="cl">` szerkezetét használjuk — ez a licencelt, repóban tárolható
forrás is egyben (D17). Végső döntés a NYITOTT_FELADATOK.md tulajdonosáé.
