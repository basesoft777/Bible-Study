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

- **Igehely:** a STEPBible-natív hivatkozás VÁLTOZATLANUL (pl. `Gen.1.1`, `Pro.23.7`) —
  a magyar formátumra (`1Móz 1:1`) alakítás egy külön, még hátralévő lépés (lásd a döntési
  fájl 8. szakaszának "könyv-rövidítés normalizáló tábla" pontja).
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

**Ismert, dokumentált ritka eset (~0,2% a TAGNT-sorokban) — egybeolvadt (krázis) szavak.**
Néhány görög szó két morfémát olvaszt egybe egyetlen írott alakba (pl. `κἂν` = `καί`
"és" + `ἐάν` "ha"), amit a forrás a `sStrong+Instance` oszlopban vesszővel elválasztott
Strong-listával jelez (pl. `G1437, G2532`), miközben maga a görög szóalak **nem** bontható
szét két külön írott részre (ellentétben a héber "/" morfémákkal). Ezekben az esetekben a
kivonat **egy sort** ad a szóhoz, a Strong-számokat `+`-jellel összefűzve (pl.
`G1437+G2532`); a Szótő/Rövid jelentés oszlop hasonlóan összefűzve, ha a forrás
`Dictionary form = Gloss` mezője is szétbontva adja meg őket, egyébként az egybeolvadt szó
saját szótári alakja szerint.

## Méret és sorszám

| Fájl | Nyers sorok (STEPBible) | Generált sorok | Fájlméret |
|---|---|---|---|
| TAHOT_kivonat.tsv | 283 734 | 435 723 | ~24 MB |
| TAGNT_kivonat.tsv | 141 720 | 141 720 | ~13 MB |

Mindkét fájl jóval a GitHub 100 MB-os fájlméret-korlátja alatt van, könyvenkénti bontás
nem volt szükséges.

Lefedettség: TAHOT — 39 ószövetségi könyv, 21 178 egyedi igehely; TAGNT — 27 újszövetségi
könyv, 7 948 egyedi igehely.

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
