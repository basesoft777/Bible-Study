# LXX kivonat — Zsoltárok (teljes könyv)

Ez a dokumentum a `konkordancia/LXX_kivonat_Zsoltarok.tsv` fájlt írja le: forrás,
letöltés dátuma, licenc-státusz, módszertan, sor-szám és a validációs
eredmény.

**Ez a teljes Zsoltárok könyv (150 fejezet) kivonata**, a
`LXX_kivonat_Zsoltar_Joel_pilot.tsv` 3 igehelyre célzott pilotjának
hatókör-bővítése. A pilot-fájl megmarad, nem törlődik — validációs
referenciaként szolgál (l. lent).

## Forrás

- **Weboldal:** [studybible.info](https://studybible.info/), verzió: `LXX_WH`
  ("Septuagint OT and Westcott-Hort Greek NT")
- **URL-minta:** `https://studybible.info/LXX_WH/Psalms%20<fejezetszám>`
  (1-től 150-ig, fejezetenként külön oldal, változatlan a Genezis- és a
  pilot-README-hez képest)
- **Letöltés dátuma:** 2026-09-04

## Licenc-státusz — explicit gap

A studybible.info oldalon (sem a főoldalon/about-on, sem a `/version/LXX_WH`
verzió-leíró oldalon) **nem található explicit copyright- vagy
licenc-nyilatkozat** a Septuaginta-szövegre vagy a Strong-taggelésre
vonatkozóan. A `/version/LXX_WH` oldal csak annyit közöl, hogy a szöveg
"Septuagint LXX Greek Old Testament keyed to Strong's numbers with complete
parsing information" — forrást vagy jogi státuszt nem jelez.

**Ez nyitott kérdés marad.** A LXX görög alapszövege (Rahlfs/Swete-hagyomány)
önmagában közkincs, de a Strong-számozás és morfológiai kódolás hozzáadott
szerkesztői munka lehet, aminek jogi státusza a studybible.info-n nincs
dokumentálva. Mielőtt ez az adat bármilyen publikált vagy továbbterjesztett
kimenetbe kerülne, a licenc-kérdést tisztázni kell (pl. a studybible.info
üzemeltetőjének megkeresésével, vagy alternatív, explicit CC-licencű LXX-forrás
keresésével, mint pl. a Rahlfs-LXX STEPBible-féle Strong-taggelt változata,
amit a `Validacios_naplo.md` 1. fázisa már azonosított jövőbeli alternatívaként).

**Nem publikus, nem kimenő adat.** Ez a fájl kizárólag belső munkafolyamat-
célra készült, a fenti licenc-kérdés tisztázásáig nem kerülhet publikált vagy
továbbterjesztett kimenetbe.

## Módszertan

Az `eszkozok/lxx_kivonat_fetch.py` újrafelhasználható szkripttel:

```bash
python eszkozok/lxx_kivonat_fetch.py --konyv Psalms --fejezet-tol 1 --fejezet-ig 150 \
  --versifikacios-terkep konkordancia/LXX_versificacios_terkep.tsv \
  --karoli-konyv-prefix Zsolt \
  --kimenet konkordancia/LXX_kivonat_Zsoltarok.tsv
```

### Miért kellett a `--versifikacios-terkep` opció (szemben a Genezis- és a pilot-fájllal)

A Genezis-kivonatnál (és a 3-verses pilotnál, mert ott a kiválasztott 2 zsoltár
egyike sem volt cím-eltolásos) a kért Károli-fejezet/vers-szám közvetlenül
megegyezett az oldal helyi vers-sorszámával. A Zsoltárok nagy részénél ez NEM
igaz: a zsoltár-feliratok (pl. "Az éneklőmesternek; Dávid zsoltára.") LXX-ben
gyakran önálló 1. versnek számítanak, amit a Károli vagy szintén önálló
versnek számoz, vagy az 1. vers szövegébe olvaszt, vagy — ritkábban — a
Károli 1. verse két LXX-verset von össze (pl. Zsolt 102:1 = LXX 101:1-2).

A studybible.info nyers HTML-je minden ilyen eltérésnél a szó elejére írt
`[fejezet:vers]` zárójeles jelöléssel látja el az érintett szót (pl.
`[109:4]` a Zsolt 110:4 versben) — ez a valódi LXX belső hivatkozás. A
szkript ezt a zárójelet olvassa ki, és a `LXX_versificacios_terkep.tsv`
táblázatban keres rá egyezést, majd a talált sor `Karoli_igehely` értékét
írja a kimenet `Igehely` oszlopába. Zárójel hiányában (a fejezet nem
eltolt) a nyers oldal-helyi fejezet/vers-szám kerül közvetlenül
használatra, ugyanúgy, mint a Genezis-kivonatnál.

**Fontos, empirikusan ellenőrzött részlet:** a zárójeles LXX-hivatkozás
könyvenként *következetesen* vagy a térkép `Gorog_LXX_vers`, vagy a
`Heber_vers` oszlopával egyezik (Zsoltároknál a `Gorog_LXX_vers`-szel, pl.
Zsolt 110:4 → `[109:4]`; Jóelnél viszont a `Heber_vers`-szel, l. a Jóel-
README-t) — soha nem mindkettővel egyszerre egy adott könyvön belül. Emiatt
a szkript **két külön kereső-szótárat** épít (elsődleges: `Gorog_LXX_vers`,
tartalék: `Heber_vers`), nem egyet — enélkül a két oszlop verszám-terei
hamisan ütköztek volna (pl. Zsolt 147-nél a `Heber_vers` értékei a fejezet
első felében ugyanazt a fejezetszámot használják, mint a `Gorog_LXX_vers` a
második felében, mert Zsolt 147 a LXX 146+147 fejezetek összevonása).

A kereső-kulcs emellett tartalmazza a **kért** (Károli-)fejezetszámot is,
mert ugyanaz a zárójeles érték (pl. `53:4`) két különböző oldalon is
előfordulhat eltérő jelentéssel: saját oldalán (pl. a "Psalms 53" oldalon egy
belső cím-eltolódás miatt) ÉS egy másik zsoltár oldalán kereszthivatkozásként
(pl. a "Psalms 54" oldalon a LXX-fejezet-eltolódás miatt) — a kért fejezet
nélkül ezek hamisan ütköznének egy lapos globális szótárban.

### Két további, a térkép hiányosságait pótló szabály

A `LXX_versificacios_terkep.tsv` — amit egy korábbi munkamenet állított elő —
nem dokumentál minden verset kimerítően, hanem csak az "eltérés"-eseteket
rögzíti. Két rendszeres, ellenőrzött mintázat esetén ez hiányos sorokat
eredményezett, amit a szkript pótol:

1. **Cím-felirat-vers pótlása.** Néhány zsoltárnál (pl. Zsolt 12, 18, 19, 20,
   21, 30... — összesen 39 fejezetnél) a Károli maga is önálló 1. versnek
   számozza a puszta zsoltár-feliratot (pl. "Zsolt 20:1: Az éneklőmesternek;
   Dávid zsoltára."), szemben a többségi esettel, ahol a felirat az 1. vers
   szövegébe olvad vagy egyáltalán nincs is felirat. A térkép ezt a mintát
   nem ismerte fel, ezért nem dokumentált külön sort ehhez a vershez. Mivel a
   felirat mindig a fejezet első zárójeles szava, és a fejezet többi verse
   már dokumentált egy adott zárójel-fejezettel, ez biztonságosan levezethető
   (kézzel ellenőrizve mind a 39 esetnél a Károli-szöveg alapján: mindegyik
   valóban puszta felirat-szöveg).
2. **Záró-vers pótlása.** Hasonló okból néhány zsoltárnál (pl. könyv-
   elválasztó doxológiák, "Áldott az Úr..." típusú záró sorok) a térkép a
   fejezet utolsó Károli-verséhez sem dokumentált sort. A szkript ezt is
   pótolja, ha a térképben dokumentált legnagyobb Károli-vers pontosan
   eggyel kisebb, mint a `Karoli_1908.tsv`-ben ténylegesen létező utolsó
   vers. **A gyakorlatban ez a pótlás egyetlen esetben sem eredményezett
   tényleges kimeneti sort** (l. "Ismert lefedettségi hiányok" lent) — a
   studybible.info `LXX_WH` szövege ezeknél a verseknél (jellemzően a
   Zsoltárok könyvének 5 részre osztását jelző könyv-doxológiák, pl.
   Zsolt 41:14, 89:53) egyáltalán nem tartalmaz külön Strong-taggelt görög
   szót — ez tehát nem térkép-hiány, hanem a forrásszöveg saját hiánya.

Mindkét pótlás forráskódszinten dokumentált (`eszkozok/lxx_kivonat_fetch.py`,
`load_versifikacios_terkep` függvény).

### Kizárt tartalom: apokrif 151. zsoltár és a Zsolt 1:7 térkép-műtermék

A `LXX_versificacios_terkep.tsv`-ben egyetlen zsoltár-sor szerepel
`ELLENORZESRE_VAR` státusszal: `Zsolt 1:7 → Psa.Psa.151:7` (a `Gorog_LXX_vers`
oszlop kettőzött, hibás "Psa.Psa.151" prefixű értékkel). Ez — és a vele együtt
szereplő, de `EGYIK_SEM`-ként jelölt `Zsolt 1:1`–`1:6` sorok ugyanezzel a
hibás `Psa.Psa.151:x` értékkel — **térkép-generálási műtermék**: a valódi
Zsoltár 1 fejezet (mind Héberben, mind a LXX-ben, mind a Károliban) 6 versből
áll, nincs 7. verse, és a live oldal (`Psalms 1`) nem is tartalmaz zárójeles
LXX-hivatkozást (nincs eltolás), ezért ezek a hibás sorok a gyakorlatban
ártalmatlanok — a szkript soha nem hivatkozik rájuk, mert a "Psa.Psa.151"
minta nem illeszkedik a zárójel-kereső reguláris kifejezésre.

**A valódi 151. zsoltár tartalom máshol, ténylegesen előfordul a forrásban:**
a `Psalms 150` oldal lekérdezésekor a live HTML a rendes 6 verses tartalom
UTÁN további, `[151:1]`–`[151:7]` zárójellel jelölt szavakat is tartalmaz — ez
a görög kéziratokban (és sok LXX-kiadásban) a 150. zsoltár után hagyományosan
közölt **apokrif 151. zsoltár-toldalék**. Mivel ennek nincs Károli-
megfeleltetése (a Károli nem tartalmazza a 151. zsoltárt), ez a 7 szócsoport
a szkript "nincs térkép-egyezés" ága miatt **szándékosan kimarad** a
kimenetből (ugyanaz a kezelés, mint a Zsolt 1:7 térkép-műtermék esetén: mindkettő
"151. zsoltár"-hivatkozás, csak eltérő forrásból/okból kerül elő).

## Kimeneti fájl és oszlopok

**`LXX_kivonat_Zsoltarok.tsv`** (4 oszlop, azonos séma, mint a
`LXX_kivonat_Genezis.tsv` és a pilot-fájl):
```
Igehely | Strong-szám | Görög szóalak | Morfológiai kód
```

## Sor-szám és lefedettség

- **32 575 adatsor** + 1 fejléc-sor = 32 576 sor összesen.
- A `Karoli_1908.tsv` szerint a Zsoltárok könyve 2527 verset tartalmaz
  (Zsolt 1:1 – Zsolt 150:6). Ebből **2457 vers kapott legalább egy
  Strong-taggelt szót** (97,2%).
- **70 Károli-vers maradt lefedetlen** (0 kimeneti sor), két kategóriában:
  - **68 vers**: a chapter végi, jellemzően doxológia-/lezáró jellegű verse
    (pl. Zsolt 3:9, 41:14, 89:53, 102:29, 150:… — a Zsoltárok könyvének
    hagyományos 5 részre osztását jelző könyv-doxológiák és hasonló záró
    sorok). A studybible.info `LXX_WH` szövege ezeknél nem ad külön
    Strong-taggelt görög szót — ez a forrásszöveg saját hiánya, nem a
    szkript vagy a térkép hibája (l. fent, "Záró-vers pótlása").
  - **2 vers** (`Zsolt 13:6`, `Zsolt 54:2`): valódi vers-szintű felosztási
    kétértelműség. A `LXX_versificacios_terkep.tsv` ezeknél egy közös LXX-
    verset (pl. `Psa.12:6`) Károli-oldalon KÉT külön versre bont
    (`Concatenation/Merge` típus, "a"/"b" utótaggal, pl. `12:6a` → Zsolt
    13:5, `12:6b` → Zsolt 13:6), de a nyers HTML nem jelöl belső
    al-vers-határt ezen az egy LXX-versen belül — a szkript emiatt a teljes
    LXX-vers szavait a KISEBB sorszámú Károli-vershez rendeli (Zsolt 13:5,
    ill. Zsolt 54:1), a másik (13:6, 54:2) így 0 sort kap. Ez dokumentált,
    ismert korlát, forráskódszinten is jelzett figyelmeztetéssel fut le.
- Ezen felül **7 szócsoport szándékosan kimaradt** (a `Psalms 150` oldal
  végén található apokrif 151. zsoltár-toldalék, l. fent).

## Validáció

A korábbi 3-verses pilot mindhárom sora (Zsolt 16:10, Zsolt 110:4) szó szerint
egyezik a teljes-könyves kimenettel (a harmadik, Jóel 2:32, a Jóel-fájlban
ellenőrzött, l. `LXX_kivonat_Joel_README.md`):

```bash
diff <(grep "^Zsolt 16:10	" konkordancia/LXX_kivonat_Zsoltarok.tsv) \
     <(grep "^Zsolt 16:10	" konkordancia/LXX_kivonat_Zsoltar_Joel_pilot.tsv)
diff <(grep "^Zsolt 110:4	" konkordancia/LXX_kivonat_Zsoltarok.tsv) \
     <(grep "^Zsolt 110:4	" konkordancia/LXX_kivonat_Zsoltar_Joel_pilot.tsv)
```

Mindkét `diff` üres kimenetet ad (teljes egyezés) — ellenőrizve 2026-09-04.

Emellett ellenőrizve: a `Zsolt 147:1` és `Zsolt 147:12` (a LXX 146+147
fejezetek összevonásának két fele, azonos "Alleluia, Aggeus és Zakariás"
felirattal induló szövegrész) helyesen KÜLÖN Károli-igehelyre kerül, nem
ütközik egymással — ez a szkript két-szótáras (Gorog/Heber) tervezésének
közvetlen ellenőrzése (l. Módszertan).
