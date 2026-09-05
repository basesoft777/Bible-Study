# A `Nem_parszolhato_terkep_ertekek.tsv` kategorizálása (145 sor)

Ez a dokumentum a `konkordancia/Nem_parszolhato_terkep_ertekek.tsv` 145 sorát
mintázat szerint csoportosítja, és kategóriánként értékeli, hogy elvileg
feloldható lenne-e egy szűkebb parszolási szabállyal, vagy ugyanaz a
tartalmi-döntési probléma áll fenn, mint a betű-utótagos vers-albontásnál
(l. `LXX_kivonat_README.md` 2. szakasz). **Ebben a körben semmi nem lett
javítva** — ez kizárólag elemzés és javaslat.

A feloldhatóság-értékeléshez minden kategóriánál közvetlenül megnéztem a
nyers `studybible.info/LXX_WH/` forrásoldalt is (nem csak a térkép-fájlból
következtettem), ugyanúgy, ahogy a betű-utótagnál is tettük.

## Összesítő tábla

| # | Kategória | Sorszám | Érintett könyvek | Feloldhatóság |
|---|---|---|---|---|
| 1 | Kétszeres `"X / Y"` alternatíva | 57 | Dán (34), Neh (22), 1Móz (1) | **Vegyes** — könyvenként eltér, l. részletek |
| 2 | Csillagos többbetűs tartomány (`*a-w`) | 14 | Eszt (7), 2Móz (3), Józs (2), Dán (1), 1Kir (1) | Nem — tartalmi döntés |
| 2b | Betű-tartomány csillag nélkül (`a-c`) | 5 | 1Kir (4), Józs (1) | Nem — tartalmi döntés (ua. család, mint 2/3) |
| 2c | Betű+szám kombinált utótag (`a1`, `b2`) | 6 | 1Kir (6) | Nem — tartalmi döntés (ua. család) |
| 3 | Szögletes-zárójeles kereszthivatkozás (`[=X:Y]`) | 27 | 1Kir (27) | Nem — tartalmi döntés (ua. család, 1Kir Miscellanies) |
| 4a | Pontosvesszős lista | 10 | 2Móz (8), Józs (1), Eszt (1) | Nem — tartalmi döntés |
| 4b | Vesszős lista | 8 | 2Móz (6), 1Kir (2) | Nem — tartalmi döntés |
| 5 | Kettős kötőjel tartomány (`X--Y`) | 1 | Ézs (1) | Nem érdemes külön kezelni (1 eset) |
| 6 | Ismert korrupt duplikált prefix (`Psa.Psa.`) | 6 | Zsolt (6) | Igen, de **feleslegesen** — l. részletek |
| 7 | Egyéb (vegyes, kis darabszámú minták) | 11 | 1Kir (4), 2Móz (3), 1Móz (2), Józs (1), Péld (1) | Nem — tartalmi döntés |

**Összesen: 145 sor.**

## Részletes értékelés kategóriánként

### 1. Kétszeres `"X / Y"` alternatíva (57 sor) — VEGYES eredmény, könyvenként eltér

Ez volt az egyetlen kategória, ahol a nyers oldal ellenőrzése **pozitív**
eredményt hozott az egyik mintavett könyvnél, de **negatívat** a másiknál —
ezért nem javaslom blanket-javítását, csak célzott, könyvenkénti
utóvizsgálatot.

- **Nehémiás** (`Neh.3:33 / 4:1` stílus, 22 sor): a nyers `Nehemiah 4` oldalon
  **mindkét fél külön, valódi zárójelként létezik** (`[3:33]` ÉS `[4:1]` is
  megtalálható a lapon, különböző szavaknál). Ez arra utal, hogy itt a "/"
  valójában két, a Károli-versbe **összevont** görög félverset jelöl
  (hasonlóan a betű-utótaghoz, csak itt mindkét fél egész számmal, nem betűvel
  van jelölve) — ez **elvileg feloldható** lenne: mindkét felet külön
  parszolva, mindkettőt ugyanarra a Károli-célra indexelve.
- **Dániel** (`Dan.4:7 / 4:10` stílus, 34 sor, a kategória zöme): a nyers
  `Daniel 4` oldalon **egyetlen zárójel sem található** (0 db, ellenőrizve).
  Ez azt jelenti, hogy ennél a könyvnél ez a fajta javítás **nem alkalmazható**
  — de emellett egy **külön, eddig fel nem tárt kérdést** vet fel: ha Dániel 4.
  fejezetében valóban van egy számozási eltolódás (amit a térkép dokumentál),
  de az oldal nem jelzi zárójellel, akkor ez a tartalom jelenleg a nyers
  oldal-helyi számozással kerül ki — **ismeretlen, hogy ez helyes-e vagy
  csendben hibás**. Ezt **nem ellenőriztem tovább** (túlmutat a mostani kör
  keretein), de érdemes lenne külön megnézni Dániel 4. fejezetét.
- **1Móz** (1 sor, `Gen.2:25 / 3:1a`): egyedi eset, nem vizsgáltam külön —
  túl kevés előfordulás ahhoz, hogy megérje.

**Javaslat:** NE implementálj most semmit. Ha van rá kapacitás, egy **külön,
szűk körű** vizsgálat javasolt: (a) Nehémiás 22 sorára egy célzott,
alacsony kockázatú "oszd ketté a '/'-t, parszold mindkét felet, mindkettőt a
közös Károli-célra indexeld" logika hozzáadása; (b) Dániel 4. fejezetének
független ellenőrzése, hogy a jelenlegi (zárójel nélküli, nyers számozásra
támaszkodó) kimenet helyesen van-e címkézve.

### 2, 2b, 2c, 3. A "reorganizált tartalom" család (52 sor együtt) — NEM feloldható

Ez a négy alkategória (csillagos többbetűs tartomány, betű-tartomány csillag
nélkül, betű+szám kombinált utótag, szögletes-zárójeles kereszthivatkozás)
ugyanazt a jelenséget írja le különböző jelölési variánsokban: a LXX egy adott
szakaszt **jelentősen átrendezett sorrendben** ad vissza a maszoretai
szöveghez képest (leghíresebb példa: 1Kir "Miscellanies" — Jeroboám
királyságának kétszeres, eltérő sorrendű elbeszélése; illetve Exodus 36-39
sátor-építési szakasza).

**Konkrétan ellenőrizve a nyers oldalon:**
- `2Móz 36:9` (`Exo.37:2*a-aa`): az `Exodus 37` oldalon a várt `[37:2a]`
  helyett **`[28:29α]`** zárójel található — teljesen más szám ÉS görög betű,
  nem latin "a".
- `Józs 24:33`, `1Kir` több sora, `Eszt 3:13`/`5:1` (`*a-g`, `*a-f` stílus): a
  megfelelő nyers oldalakon **egyáltalán nincs** zárójel a várt helyen (0
  találat mind Exodus 38, mind Daniel 4, mind Eszter 3 oldalán a releváns
  szakaszra nézve).
- `1Kir 10:26` (`[=4:21]` stílus): a `[=X:Y]` jelölés egy MÁSIK fejezetben
  ismétlődő tartalomra mutat — ez tartalmilag két, egymástól távoli helyen
  megjelenő, azonos szöveg összekapcsolása, amit a nyers oldal szintén nem
  jelöl semmilyen kereszthivatkozással.

**Verdikt:** ugyanaz a probléma, mint a betű-utótagnál — a nyers oldal nem ad
elég információt a szónkénti szétosztáshoz, a döntés tartalmi ítéletet
igényelne. **Javaslat: zárjuk le véglegesen elfogadott, dokumentált
hiányként**, pontosan úgy, mint a `Betu_utotag_kizarva.tsv` esetét.

### 4a, 4b. Pontosvesszős / vesszős lista (18 sor) — NEM feloldható

Ellenőrizve: `2Móz 37:11` (`Exo.38:9,11b`) esetén az `Exodus 38` oldalon a
`38:9` érték **nem szerepel** a fellelhető zárójelek között (miközben `38:21`
—`38:26` igen) — ez ugyanannak a sátor-építési átrendezésnek a jele, mint a 2.
kategóriánál. **Verdikt:** ugyanaz a család, ugyanaz a javaslat — véglegesen
elfogadott hiány.

### 5. Kettős kötőjel tartomány (1 sor) — nem éri meg külön kezelni

Az `Ézs 63:19` (`Isa.63:19--64:1`) egyetlen előfordulás egy fejezethatáron
átnyúló tartomány — ismert, dokumentált jelenség (Ézsaiás 63/64 fejezethatár
eltolódása, l. `LXX_kivonat_README.md` 4. szakasz "Hóseás, Ézsaiás"
bekezdése). Egyetlen sor miatt nem éri meg speciális parszolási szabályt írni.

### 6. Ismert korrupt duplikált prefix (`Psa.Psa.`, 6 sor) — feloldható lenne, de FELESLEGES

Ez technikailag a **legkönnyebben** javítható minta (egyszerű
string-csere: `"Psa.Psa."` → `"Psa."`), és ez a hiba már a v1 szkript
dokumentációjában is ismert volt ("korrupt Psa.Psa.151:x sor"). **DE**:
ellenőrizve — ez a 6 sor mind a Zsoltár 1. fejezet elejére vonatkozik
(`Zsolt 1:1`–`1:6`), ahol **nincs ismert LXX/Károli számozási eltolódás**
(az eltolódás csak a 9-10. zsoltártól kezdődik). A nyers oldal ezekhez a
szavakhoz **nem is ad zárójelet**, tehát a jelenlegi (nyers oldal-helyi
számozásra támaszkodó `else`-ági) kimenet már most is helyes — a corrupt
térkép-sor javítása **semmilyen tényleges kimeneti változást nem hozna**.
**Javaslat:** dokumentáljuk tudott, ártalmatlan hibaként, ne fordítsunk rá
fejlesztői időt.

### 7. Egyéb (11 sor) — vegyes, kis darabszám, nem éri meg egyenként kezelni

Ide tartozik pl. `1Móz 5:31` (`Gen.5:31-6:1a`, fejezethatáron átnyúló
tartomány betűvel) és `2Móz 36:34` (`Exo.37:2aa`, kettős-betűs utótag
csillag nélkül). Mindegyik 1-3 előfordulású, egyedi formátum — nem indokolt
külön parszolási szabályt írni ilyen kis darabszám miatt. **Javaslat:**
elfogadott hiányként dokumentálva lezárni, a 2/2b/2c/3 családdal együtt.

## Összefoglaló javaslat

- **Nincs olyan kategória, amit alacsony kockázattal, azonnal érdemes lenne
  megoldani** — a `Psa.Psa.` eset technikailag triviális, de gyakorlati haszna
  nulla.
- **Egyetlen kategória érdemel esetleg további vizsgálatot** (nem
  implementációt): a Nehémiás-féle `"X / Y"` minta, ahol a nyers oldal
  ténylegesen mindkét felet külön zárójelként adja — ez egy jövőbeli, célzott
  kör tárgya lehetne, DE csak könyvenkénti ellenőrzéssel (a Dániel-negatív
  eredmény mutatja, hogy nem általánosítható).
- **Külön, a jelen kör keretein túlmutató nyitott kérdés:** Dániel 4.
  fejezetének számozása — a térkép szerint van eltolódás, de a nyers oldal
  nem jelzi zárójellel, így nem tudni, hogy a jelenlegi kimenet helyes-e.
  Érdemes lenne külön ellenőrizni.
- **Minden más kategória (2, 2b, 2c, 3, 4a, 4b, 5, 7 — összesen 87 sor):**
  javaslom véglegesen, dokumentáltan elfogadott hiányként lezárni, ugyanabba
  a "nem rekonstruálható a nyers oldalból" csoportba sorolva, mint a
  betű-utótagos kizárásokat.
