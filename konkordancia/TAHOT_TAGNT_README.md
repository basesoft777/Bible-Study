# TAHOT / TAGNT kivonat — teljes ÓSZ+ÚSZ, szavankénti bontásban

Ez a dokumentum a `konkordancia/TAHOT_kivonat.tsv` és `konkordancia/TAGNT_kivonat.tsv`
fájlokat írja le: forrás, letöltés dátuma, licenc, és — mivel a nyersadat mezőazonosítása
nem triviális — a pontos módszertan, hogy egy jövőbeli módosításnál ne kelljen újra
kitalálni.

## Forrás

- **Repó:** [STEPBible/STEPBible-Data](https://github.com/STEPBible/STEPBible-Data) (GitHub, publikus)
- **Mappa:** `Translators Amalgamated OT+NT/`
- **Felhasznált fájlok:**
  - `TAHOT Gen-Deu - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt`
  - `TAHOT Jos-Est - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt`
  - `TAHOT Job-Sng - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt`
  - `TAHOT Isa-Mal - Translators Amalgamated Hebrew OT - STEPBible.org CC BY.txt`
  - `TAGNT Mat-Jhn - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt`
  - `TAGNT Act-Rev - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt`
- **Letöltés dátuma:** 2026-08-24 (`git clone --depth 1`)
- **Licenc:** CC BY 4.0, Tyndale House Cambridge / STEPBible.org — lásd a döntési fájl
  2. szakaszát a pontos hivatkozásért.

## Kimeneti fájlok és oszlopok

**`TAHOT_kivonat.tsv`** (héber ÓSZ, 7 oszlop):
```
Igehely | Strong-szám | Ragozott alak | Kiejtés | Szótő | Rövid jelentés | Angol tükörfordítás
```

**`TAGNT_kivonat.tsv`** (görög ÚSZ, 8 oszlop):
```
Igehely | Strong-szám | Ragozott alak | Kiejtés | Szótő | Rövid jelentés | Angol tükörfordítás | Kritikai kiadás
```

- **Igehely — TAHOT_kivonat.tsv:** Károli-natív, magyar formátumú hivatkozás (pl.
  `1Móz 1:1`, `Péld 23:7`) — lásd lent a "Károli-natív kulcs és a zárójeles kettős
  hivatkozás javítása" szakaszt a pontos módszertanért.
- **Igehely — TAGNT_kivonat.tsv:** a STEPBible-natív hivatkozás VÁLTOZATLANUL (pl.
  `Gen.1.1`, `Pro.23.7`), **kivéve** a 4 zárójeles kettős hivatkozású ÚSZ-esetet (lásd
  "Zárójeles kettős hivatkozás" szakasz lent) — ott az `Igehely` mező rögtön Károli-natív.
- **Strong-szám:** tiszta forma, homográf-jelölés és instance-toldalék nélkül (pl. `H7225`,
  nem `H7225G` vagy `H7225G_A`).

## A nyersadat szerkezete és a mezőazonosítás módszere

### TAHOT (héber)

A nyers fájl minden szó-sorát (pl. `Gen.1.1#01=L`) tabulátorral elválasztott mezők adják.
A ténylegesen releváns oszlopok (a fájlban lévő literális fejléc-sor alapján, lásd
`Eng (Heb) Ref & Type | Hebrew | Transliteration | Translation | dStrongs | Grammar | ... | Root dStrong+Instance | ... | Expanded Strong tags`):

| # | Oszlopnév | Példa (Gen.1.1#01) |
|---|---|---|
| 1 | Eng (Heb) Ref & Type | `Gen.1.1#01=L` |
| 2 | Hebrew | `בְּ/רֵאשִׁ֖ית` |
| 3 | Transliteration | `be./re.Shit` |
| 4 | Translation | `in/ beginning` |
| 5 | dStrongs | `H9003/{H7225G}` |
| 12 | Expanded Strong tags | `H9003=ב=in/{H7225G=רֵאשִׁית=: beginning»first:1_beginning}` |

**Kulcsfelismerés — egy nyers sor gyakran TÖBB szótári/Strong-egységet takar.** A héber
szavak elő-/utóragjait (névelő, kötőszó, elöljárószó, birtokos névmási toldalék) a forrás
saját maga is külön Strong-számmal (`H9xxx` tartomány) látja el, és a `Hebrew`,
`Transliteration`, `Translation`, `dStrongs`, `Expanded Strong tags` oszlopok mindegyike
**"/" jellel** választja külön ezeket a morfémákat, egymással pozíció szerint összefésülve
(pl. a fenti Gen.1.1#01 sor 2 sort ad: `H9003` "in" prefix + `H7225` "beginning" gyök).
**A kivonat ezért NEM nyers-soronként, hanem morfémánként generál egy-egy sort** — ez az
egyetlen módszer, ami a döntési fájl validációs referenciájával (Gen.1.1, 2. szó = H7225)
egyezést ad.

**Feldolgozási lépések soronként:**
1. A `Hebrew` és `dStrongs` (és `Expanded Strong tags`) mezőket előbb `\` (backslash) mentén
   vágjuk — ez választja el a szótól az utána álló írásjel-Strong-kódot (pl. `H9016`=mondatvégi
   pont, `H9014`=maqqef-kötőjel, `H9015`=paseq). **A backslash utáni rész (írásjel) el lett
   hagyva** a kivonatból — nem szó, nincs kiejtése/fordítása, csak zajt jelentene egy
   szókonkordanciában.
2. A megmaradt (szó-)részt `/` mentén vágjuk szét — ez adja a morfémákat (elő-/utórag + gyök),
   pozíció szerint összefésülve a `Hebrew`/`Transliteration`/`Translation`/`dStrongs`/
   `Expanded Strong tags` oszlopok között.
3. **Strong-szám** = a `dStrongs` adott szegmense, `{}` zárójel, `_instance` toldalék és a
   homográf-betű (pl. `G`, `A`) eltávolítva.
4. **Ragozott alak / Kiejtés / Angol tükörfordítás** = a `Hebrew` / `Transliteration` /
   `Translation` megfelelő szegmense.
5. **Szótő + Rövid jelentés** = az `Expanded Strong tags` megfelelő szegmensének
   `STRONG=SZÓTŐ=GLOSSZ` alakjából: Szótő = a `=` közti középső rész; Rövid jelentés = ha a
   glossz tartalmaz `»` jelet, az utána (és a következő `:`/`@` előtti) rész (pl.
   `: beginning»first:1_beginning` → `first`); ha nincs `»`, a teljes glossz (vezető `: `
   levágva).

**Ismert, dokumentált egyszerűsítések:**
- **Ketiv/Qere-illesztési üres helyőrzők** (pl. `Rut.3.5#05`, ahol a Qere két Ketiv-szót
  eggyé von össze, a forrás egy üres `/  /` szegmenssel tartja egyenesben az oszlopszámot) —
  ezek a szegmensek Strong-szám nélküliek, a kivonat **kihagyja** őket.
- **`+` végű Strong-kód** (pl. `H0045+`) — a forrás jelölése arra, hogy "ugyanez a címke a
  következő szóra is vonatkozik"; a kivonat a `+`-t levágja, a Strong-számot megtartja.

### TAGNT (görög)

A görög adat egyszerűbb: **egy nyers sor = egy szó = általában egy Strong-szám**, nincs
prefix/suffix "/" szétválasztás (a görög igekötők már eleve egybeírva szerepelnek az
igealakban, nem külön taggelve). Releváns oszlopok (a fájl literális fejléc-sora alapján:
`Word & Type | Greek | English translation | dStrongs = Grammar | Dictionary form = Gloss |
editions | ... | sStrong+Instance | Alt Strongs`):

| # | Oszlopnév | Példa (Heb.4.12#19) |
|---|---|---|
| 1 | Word & Type | `Heb.4.12#19=NKO` |
| 2 | Greek | `ψυχῆς (psuchēs)` |
| 3 | English translation | `of soul` |
| 5 | Dictionary form = Gloss | `ψυχή=soul` |
| 6 | editions | `NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz` |
| 12 | sStrong+Instance | `G5590` |

- **Ragozott alak / Kiejtés**: a `Greek` mezőből, a `SZÓ (transzliteráció)` formátumot
  regex-szel szétbontva.
- **Strong-szám**: a `sStrong+Instance` oszlopból (ez már eleve tiszta, homográf-jel
  nélküli forma), `_instance` toldalék levágva.
- **Szótő + Rövid jelentés**: a `Dictionary form = Gloss` mezőből (`=` mentén vágva).
- **Angol tükörfordítás**: az `English translation` oszlop változatlanul.
- **Kritikai kiadás**: az `editions` oszlop változatlanul (pl. `NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz`).

**Zárójeles kettős hivatkozás — kritikai kiadások közötti versheletér-eltérés.**
Négy helyen a nyers `Word & Type` mező `Könyv.Fejezet.Vers(Fejezet.Vers)` alakú
(pl. `Rom.3.25(3.26)#24=NKO`): a zárójel előtti szám a fájl alap-versifikációja (NRSV
szerinti), a zárójeles rész pedig azt jelzi, hogy a NA-kiadás (a legtöbb modern fordítás
alapja) ezt a szórészt a másik vershez sorolja. **Ez a jelenség a kritikai kiadások közötti
eltérés, nem a héber/görög nyelvek közötti versificaiós kérdés** — utóbbi kizárólag az
ÓSZ-t (TAHOT) érinti. Az érintett négy hely (a nyers fájl fejlécének "FIELD DESCRIPTIONS"
szakasza is megerősíti: "NA is rarely different (Mrk.12.15; Act.13.39; Rom.3.26)"):

| Nyers Igehely | Szó-szegmens | Szavak száma |
|---|---|---|
| `Rom.3.25(3.26)` | #24–#28 | 5 |
| `Act.13.39(13.38)` | #01–#11 | 11 |
| `Mrk.12.15(12.14)` | #01–#04 | 4 |
| `Act.19.41(19.40)` | #01–#06 | 6 |

Mind a négy esetben a zárójeles szegmens a verset **részlegesen** fedi le — a nyers fájlban
közvetlenül utána (paren nélkül) folytatódik a verse többi szava a fő (nem zárójeles)
hivatkozással (pl. `Mrk.12.15#05=NKO` és utána), ami már a jelenlegi kivonatban is szerepelt.
A kivonat-generáló regexe ezért `^([A-Za-z0-9]+)\.(\d+)\.(\d+)(\((\d+)\.(\d+)\))?#(\d+)=`
alakú, és a zárójeles részt **nem dobja el**.

**Károli-natív kulcs a 4 kivételre.** Mivel a Károli 1908 az elsődleges/másodlagos STEPBible-
hivatkozás közül eseteként eltérően dönt (lásd `konkordancia/Verzifikacios_elteres_tabla.tsv`
— ez a tábla rögzíti a Károli-szöveggel való tartalmi összevetés eredményét), a kivonat-
generátor ennél a 4 esetnél nem a STEPBible-natív kulcsot írja az `Igehely` mezőbe, hanem
egy hardcode-olt, előre igazolt táblázat (`KAROLI_DONTES`) alapján rögtön a Károli-natív,
magyar formátumú hivatkozást:

| Nyers Igehely | Károli-döntés | `Igehely` mező értéke |
|---|---|---|
| `Rom.3.25(3.26)` | másodlagos | `Róm 3:26` |
| `Act.13.39(13.38)` | elsődleges | `ApCsel 13:39` |
| `Mrk.12.15(12.14)` | másodlagos | `Mk 12:14` |
| `Act.19.41(19.40)` | másodlagos | `ApCsel 19:40` |

Minden más (paren nélküli) sor `Igehely` mezője változatlanul a STEPBible-natív formátumot
kapja — ez a Károli-natív kulcs kizárólag erre a 4, egyedileg igazolt esetre vonatkozó
kivétel, nem általános magyar-formátum-konverzió.

**Ismert, dokumentált ritka eset (~0,2% a TAGNT-sorokban) — egybeolvadt (krázis) szavak.**
Néhány görög szó két morfémát olvaszt egybe egyetlen írott alakba (pl. `κἂν` = `καί`
"és" + `ἐάν` "ha"), amit a forrás a `sStrong+Instance` oszlopban vesszővel elválasztott
Strong-listával jelez (pl. `G1437, G2532`), miközben maga a görög szóalak **nem** bontható
szét két külön írott részre (ellentétben a héber "/" morfémákkal). Ezekben az esetekben a
kivonat **egy sort** ad a szóhoz, a Strong-számokat `+`-jellel összefűzve (pl.
`G1437+G2532`); a Szótő/Rövid jelentés oszlop hasonlóan összefűzve, ha a forrás
`Dictionary form = Gloss` mezője is szétbontva adja meg őket, egyébként az egybeolvadt szó
saját szótári alakja szerint.

## Károli-natív kulcs és a zárójeles kettős hivatkozás javítása (TAHOT)

**A jelenség.** A nyers TAHOT-fájlokban ~21 918 sor (2094 egyedi igehely) hivatkozása
zárójeles kettős alakú, pl. `Gen.31.55(32.1)#01=L` vagy `Psa.51.0(51.2)#01=L`. A `Ref` mező
definíciója a nyersadat fejlécében: *"Bible reference in English Bibles, as defined by the
NRSV (with Heb refs in brackets when they are different)"* — vagyis a zárójel **előtti**
rész az angol/NRSV-stílusú (a kódban "elsődleges"), a zárójel**ben** lévő a héber maszoréta
szöveg natív (a kódban "másodlagos") hivatkozása. A két rendszer néhány könyvben eltérő
fejezet-/vershatárokat használ (pl. Gen 31/32, Mal 3/4, Jóel 2/3, zsoltárcímek, amikre a
héber Biblia önálló versszámot ad, az angol/NRSV viszont nem).

**A régi generátor ezeket a sorokat szó nélkül eldobta** — emiatt pl. teljes fejezetek
(Gen 32, Zsolt 88/89/90/140/142 stb.) teljesen hiányoztak a kivonatból. A javítás két
részből áll:

1. **Eltolódási pontok azonosítása verspár-szinten** (`eszkozok/tahot_step1_shifts.py`
   jellegű elemzés — lásd a scratchpad-ben elkészült `step1_shifts2.py`-t): a négy nyers
   fájl összes egyedi (elsődleges, másodlagos) verspárja fejezetenként csoportosítva,
   union-find-del összekötve azokat a fejezeteket, amik között a másodlagos hivatkozás
   fejezethatárt lép át (pl. Gen 31↔32).
2. **Döntés fejezethossz-egyezés alapján**: minden csoportra összevetve a Károli 1908
   tényleges utolsó versszámát az adott fejezetben az elsődleges, ill. a másodlagos
   hipotézis szerinti várható hosszal. Ahol csak az egyik egyezik, automatikus döntés
   (**ELSŐDLEGES** vagy **MÁSODLAGOS**); ahol mindkettő egyezik (jellemzően zsoltárcímek,
   amik az 1. verssel olvadnak egybe — pl. Zsolt 11, 13, 24 stb., 55 eset), az alapértelmezett
   soronkénti szabály (lásd lent) magától helyesen működik; ahol egyik sem egyezik, tartalmi
   (szöveg-összevetéses) ellenőrzés Károli_1908.tsv alapján.

**Végső soronkénti szabály** (minden zárójeles nyers sorra):
- Ha a fejezet **ELSŐDLEGES** csoportba tartozik → a zárójel előtti (angol/NRSV-stílusú)
  hivatkozás lesz az `Igehely` mező alapja, a zárójel figyelmen kívül marad.
- Ha **MÁSODLAGOS** → a zárójelben lévő (héber) hivatkozás lesz az alap.
- Ha a fejezet **ADATMINŐSÉGI_GYANÚ** (lásd lent) → a sor **kimarad** a fő kivonatból,
  helyette a `TAHOT_kivonat_nyitott_esetek.tsv`-be kerül.
- Egyetlen egyedi kivétel (`1Sa.20.42(21.1)`): tartalmilag ellenőrizve, hogy Károli
  1Sám 20:43-as, önálló verseként adja vissza ezt a szövegrészt (nem tolja át a 21.
  fejezetbe) — ez a sor kézzel `1Sám 20:43`-ra van célozva.

A kapott hivatkozás ezután a `Konyv_normalizalo_tabla.tsv` alapján egyszerű
könyv-rövidítés-cserével válik Károli-formátumúvá (pl. `Gen` → `1Móz`). Ugyanez a
könyv-rövidítés-csere történik a kivonat **összes** (nem csak a zárójeles) sorára is —
ez a TAHOT-oldal érdemi különbsége a TAGNT-oldal (nem érintett) precedensétől: TAHOT-nál
minden `Igehely` rögtön Károli-natív, TAGNT-nál csak a 4 kivételes eset.

**Validált esetek** (a döntési logikát ezekkel a korábban ismert referenciapontokkal
ellenőriztük, mindegyik pontosan egyezik a várttal):

| Eset | Döntés | Ellenőrzés |
|---|---|---|
| Gen 31/32 | ELSŐDLEGES | Károli 1Móz 31:55 = "Reggel pedig felkele Lábán…", 1Móz 32:1 = "Jákób tovább méne…" (fejezethossz: 55/32) |
| Jóel 2/3(/4) | ELSŐDLEGES | Károli Jóel 2 = 32 vers, Jóel 3 = 21 vers, nincs Jóel 4. |
| Malakiás 3/4 | ELSŐDLEGES | Károli Malakiás 4 önálló, 6 verses fejezet. |
| Zsolt 3 | MÁSODLAGOS | Károli Zsolt 3:1 = cím önállóan, 3:2 = "Uram! mennyire…" |
| Zsolt 51 | MÁSODLAGOS | Károli Zsolt 51:1–2 = cím két önálló versben, 51:3 = "Könyörülj rajtam…" |
| Zsolt 11 | (mindkettő egyezik → soronkénti szabály) | Károli Zsolt 11:1 = cím és tartalom egybeolvasztva — a cím-sor másodlagos (1), a tartalom elsődleges (1) hivatkozása véletlenül ugyanoda mutat. |
| 1Sám 20/21 | ELSŐDLEGES + 1 egyedi kivétel | Károli 1Sám 20:43 önálló versként tartalmazza a héber 21:1 szövegét. |
| 1Sám 23/24 | MÁSODLAGOS | Károli 1Sám 23 = 28 vers, 24 = 23 vers (a héber szerint). |
| Ezékiel 20/21 | **ADATMINŐSÉGI_GYANÚ** | Károli Ez 20:44 összeolvadt/túlhosszú vers (a héber 21:1–5 "erdőtűz"-oráció szövege belefolyt a vers végébe), a numerikus fejezethossz-egyezés (MÁSODLAGOS: 44/37) félrevezető lenne — korábbi audit (Ez 20:44) által is dokumentált anomália. |
| Jób 40/41 | **ADATMINŐSÉGI_GYANÚ** | Sem az elsődleges (24/34), sem a másodlagos (32/26) fejezethossz nem egyezik a Károli tényleges 28/25 hosszal — korábbi audit szerint Jób 41:25 is összeolvadt vers. |

Az `ADATMINŐSÉGI_GYANÚ` alá eső sorok (Ez 20:45–49(21.1–5) és Jób 40:25–41.34(41.1–26)
zárójeles tartománya, összesen 1068 szó-sor) a `TAHOT_kivonat_nyitott_esetek.tsv`-be
kerültek, `Státusz`/`Indoklás` oszloppal, tényleges javítás nélkül — ez összhangban van
azzal, hogy a Károli-adatminőségi audit (`Karoli_adatminosegi_anomaliak.tsv`) külön,
nem e feladat része.

**Kereszt-ellenőrzés.** A fő kivonatba bekerülő minden Károli-kulcsot (a régről megmaradt
435 723 sort is) leellenőriztük a `Karoli_1908.tsv` tényleges igehely-készlete ellen. Az
összes **új** (korábban eldobott, most bekerülő) sorra 0 eltérés. A **régről** megmaradt
sorok közül 102 szó-sor (6 egyedi igehely: 4Móz 12:16; Jób 38:39–41; Préd 11:9–10) NEM
található meg a `Karoli_1908.tsv`-ben — ez egy, a zárójeles-hivatkozás javítástól
FÜGGETLEN, már korábban is fennálló Károli-oldali versszámozási/adatminőségi jelenség
(a STEPBible nyers adatban ezekhez a sorokhoz nem tartozik zárójeles kettős hivatkozás,
tehát nem e feladat hatóköre — lásd a Károli-adatminőségi audit kizárását a feladat
korlátai közt). A sorok tartalma emiatt is változatlanul bekerült a kivonatba (STEPBible-
könyv+fejezet+vers → Károli-könyv+fejezet+vers egyszerű csere), csak a Károli-oldali
igehely maga nem létezik — érdemes egy külön, jövőbeli Károli-adatminőségi vizsgálat
tárgyává tenni.

## Méret és sorszám

| Fájl | Nyers sorok (STEPBible) | Generált sorok | Fájlméret |
|---|---|---|---|
| TAHOT_kivonat.tsv | 283 734 (+ 21 918 korábban eldobott zárójeles sor) | 468 232 | ~26 MB |
| TAHOT_kivonat_nyitott_esetek.tsv | — | 1 068 | ~0,1 MB |
| TAGNT_kivonat.tsv | 141 746 | 141 746 | ~13 MB |

Mindkét fő fájl jóval a GitHub 100 MB-os fájlméret-korlátja alatt van, könyvenkénti
bontás nem volt szükséges.

Lefedettség: TAHOT — 39 ószövetségi könyv, ~23 000 egyedi igehely (a korábbi 21 178 +
az újonnan bekerült, korábban hiányzó igehelyek, pl. Gen 32, Zsolt 88/89/90/140/142,
Jóel 3); TAGNT — 27 újszövetségi könyv, 7 948 egyedi igehely.

## Validáció

A döntési fájl 2. szakaszában és a feladat-referenciában rögzített három ellenőrző eset
mindegyike számjegyre pontosan egyezik a generált adattal:

| Referencia | Elvárt | Generált |
|---|---|---|
| Gen.1.1, 2. szó | Strong=H7225, kiejtés≈"reshit", gloss="beginning", szótári jelentés="first" | `H7225 / רֵאשִׁ֖ית / re.Shit / רֵאשִׁית / first / beginning` |
| Pro.1.1, 1. szó | Strong=H4912, gloss="[the] proverbs of" | `H4912 / מִ֭שְׁלֵי / Mish.lei / מָשָׁל / proverb / [the] proverbs of` |
| Heb.4.12, ψυχῆς | Strong=G5590, gloss≈"of soul", kritikai kiadás="NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz" | `G5590 / ψυχῆς / psuchēs / ψυχή / soul / of soul / NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz` |

**Kereszt-ellenőrzés a KJV_Strongs_Proverbs.tsv-vel:** Pro.23.7 mind a hat Strong-száma
(H8176, H5315, H0398, H8354, H0559, H3820) megjelenik a TAHOT-kivonat Pro.23.7 sorai
között — ugyanazokat a szavakat azonosítja a héber oldalról, mint amit a KJV-Strongs
adat az angol fordítás oldaláról.

Emellett minden sor Strong-száma ellenőrizve `^H\d{4}$` (TAHOT) ill. `^G\d{4,5}(\+G\d{4,5})*$`
(TAGNT) mintára — mindkét fájlban 0 eltérés.

**A Károli-natív kulcsra való átállás validációja:** `Gen.1.1` → `1Móz 1:1`, `Pro.1.1` →
`Péld 1:1` — mindkettő pontosan egyezik. Lásd fentebb a "Károli-natív kulcs és a zárójeles
kettős hivatkozás javítása" szakasz validált eset-táblázatát a teljes döntési naplóért.
