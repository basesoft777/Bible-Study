# Rendszerfejlesztési playbook — PaRDeS/STEPBible-projekt

*Ez a fájl NEM a datasetek tartalmát dokumentálja (arra a döntési fájl és a
konkordancia/ mappa README-i valók) — ez a projekt saját, ismétlődően bevált
FEJLESZTÉSI MÓDSZERÉT vonja ki, hogy egy jövőbeli munkamenet, új rendszerfejlesztési
kéréssel szembesülve, ne kelljen a teljes döntési fájl-történetet újraolvasnia a
mintázatért — csak ezt a rövid receptet.*

---

## Az alaplépéssor — ez ismétlődött minden eddigi fejlesztésnél

```
1. KONTEXTUS-beolvasás
2. FORRÁS-azonosítás és licenc-ellenőrzés
3. KIS MINTA validálása
4. TELJES feldolgozás, explicit megállási szabállyal
5. NAPLÓZÁS
6. LELTÁR-frissítés
```

Az alábbi szakaszok mindegyik lépést részletezik, a projektben ténylegesen előfordult
esetekkel illusztrálva.

---

## 1. KONTEXTUS-beolvasás — mindig innen indulunk

Minden Claude Code-feladat első lépése: a `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md`
teljes beolvasása, plusz a feladathoz közvetlenül kapcsolódó fájlok (pl. egy korábbi
validációs jelentés, egy már meglévő dataset README-je).

**Miért fontos ez ennyire konzisztensen:** a projekt architektúrája (Claude Code nem
látja a claude.ai memóriát, csak a repó fájljait) miatt a döntési fájl az EGYETLEN
híd a korábbi döntésekhez. Enélkül minden feladat "nulláról indulna", és megismételné
a már megválaszolt kérdéseket.

---

## 2. FORRÁS-azonosítás és licenc-ellenőrzés — MINDIG a letöltés/feldolgozás ELŐTT

Ez a leggyakrabban visszatérő, és a legtöbb hibalehetőséget rejtő lépés. A projekt
története többször is megmutatta, hogy **a forrás NEVE vagy metaadata félrevezető
lehet** — mindig a TÉNYLEGES tartalmat kell ellenőrizni, nem a leírást.

**Bevált licenc-kategóriák és a velük járó bánásmód:**

| Licenc-típus | Példa a projektből | Bánásmód |
|---|---|---|
| CC BY 4.0 | STEPBible-Data, openscriptures/HebrewLexicon, GreekResources | Szabadon beépíthető, forrásmegjelöléssel |
| Public Domain | Károli 1908 (HunKar), KJV, ASV, Vizsolyi Biblia | Szabadon beépíthető |
| Unlicense | byztxt/byzantine-majority-text | Szabadon beépíthető |
| GPL 3.0 | openscriptures/strongs (eredeti Strong-szótár), scrollmapper KJV+Strongs forrásmodulok | **NEM építendő be** publikus repóba — copyleft-kockázat, más licencű adatokkal ütközhet |
| © védett, nyílt engedéllyel | — | Csak a licenc pontos feltételeinek ellenőrzése után, esetenként |
| © védett, engedély nélkül/bizonytalan | Veritas 2011 Károli-revízió, Biblia-Felfedező (Zsidó Miklós) | **Felfüggesztve/elutasítva** — nem használjuk, amíg nincs explicit, projektspecifikus engedély |

**Ismétlődő hibaminta, amire mindig figyelni kell:** egy forrás NEVE vagy leírása
ígérhet valamit (pl. "KJV with Strong's Numbers"), amit a TÉNYLEGES adat NEM
tartalmaz. Ez KÉTSZER is előfordult a projektben (scrollmapper KJV-JSON, getbible.net
API) — mindkét esetben csak a nyers kimenet tényleges ellenőrzése derítette ki.
**Szabály: soha ne higgy a fájlnévnek/leírásnak ellenőrzés nélkül.**

---

## 3. KIS MINTA validálása — mielőtt a teljes adatra lefuttatnánk

Minden nagyobb feldolgozásnál (nem csak adatletöltésnél) előbb egy kis mintán (3-10
tétel) kell bemutatni az eredményt, és csak jóváhagyás után folytatni a teljes
volumenre.

**Miért ez a szabály, nem csak óvatosság:** a projekt története konkrét, valós
hibákat is feltárt ezzel a módszerrel:
- A KJV/ASV Példabeszédek-feldolgozásnál egy class-name eltérés ("ref english" vs
  "english") miatt minden vers ELSŐ szava kimaradt volna, ha nincs mintavizsgálat.
- A héber TAHOT-feldolgozásnál egy nyers sor gyakran több Strong-egységet takart
  (elő-/utórag + gyök), ami csak morfémánkénti szétbontással derült ki helyesen.

**Gyakorlati forma:** "mutass egy mintát 3-5 tételre, mielőtt a teljes listára
lefuttatnád" — ez szinte minden eddigi promptban szerepelt, explicit kérésként.

---

## 4. TELJES feldolgozás — explicit megállási szabállyal

A teljes feldolgozás során is be kell tartani egy alapszabályt: **bizonytalanság
esetén NEM szabad automatikusan dönteni** — meg kell állni, és emberi döntésre várni.

**Tipikus megállási helyzetek, amik a projektben ténylegesen előfordultak:**
- Két, egymáshoz közeli, rokon Strong-szám közül egyik sem egyértelműen "helyes"
  (pl. H2895/H2896 a "jó" szónál, H1892/H1893 az "Ábel neve" névetimológiánál)
- KJV és ASV eltérő szöveget ad ugyanarra a versre (pl. Pro.23.1 "what"/"him") — ez
  NEM feltétlenül hiba, néha az eredeti szöveg valódi kétértelműségét jelzi
- A forrásfájl formátuma bonyolultabbnak bizonyul, mint a minta mutatta (pl. a görög
  GreekWordList lemma-alapú indexe, szemben a héber egyszerű Strong-szám-kulcsú
  szerkezetével)

**A helyes válasz minden esetben:** JELÖLNI a bizonytalanságot (pl. "bizonytalan"
megbízhatósági kategória, vagy "TÖBBSZÖRÖS ELŐFORDULÁS, PONTOSÍTANDÓ" jelölés), NEM
automatikusan eldönteni. Ez a "tartalmi mérlegelés vs. gépi feladat" alapelv
gyakorlati alkalmazása (lásd 4.4 pont a döntési fájlban).

---

## 5. NAPLÓZÁS — minden változás nyomon követhető marad

A projekt HÁROM naplózási helyet használ, más-más célra:

| Napló | Mit rögzít |
|---|---|
| `konkordancia/Validacios_naplo.md` | Konkrét validációs események (mit, mivel, milyen eredménnyel vetettünk össze) |
| Az adott fájl saját fejléc-changelogja | Az adott dataset/sablon saját verziótörténete |
| A döntési fájl fejléc-changelogja | A PROJEKT EGÉSZÉNEK döntéstörténete, minden érdemi lépésnél |

**Szabály:** egy új dataset vagy módszertani döntés NEM tekinthető késznek, amíg
legalább a releváns naplók egyike nem frissült.

---

## 6. LELTÁR-frissítés — a "0. Dataset-leltár" mindig tükrözze a valóságot

A döntési fájl 0. szakasza egy táblázatos gyorsáttekintés minden datasetről (hely,
státusz, forrás). Minden fejlesztési feladat UTOLSÓ lépése ennek frissítése —
enélkül egy jövőbeli munkamenet TÉVESEN azt hihetné, hogy egy dataset még nem
létezik, vagy fordítva.

---

## Gyors ellenőrzőlista új rendszerfejlesztési kéréshez

Ha egy jövőbeli munkamenetben új dataset/eszköz építése merül fel, ez a hat kérdés
adja meg a keretet:

- [ ] Elolvastam a döntési fájlt ÉS a közvetlenül kapcsolódó korábbi fájlokat?
- [ ] Ellenőriztem a TÉNYLEGES forrás-tartalmat (nem csak a nevét/leírását), és
      tisztáztam a licencet a fenti táblázat kategóriái szerint?
- [ ] Mutattam egy kis mintát validálásra, mielőtt a teljes feldolgozásra
      lefuttattam?
- [ ] Van explicit szabályom arra, mikor kell megállnom bizonytalanság esetén?
- [ ] Frissítettem a megfelelő naplót/naplókat?
- [ ] Frissítettem a 0. szakasz dataset-leltárát?

---

## Egy fontos, a projekt jellegéből adódó záró megjegyzés

Ez a playbook a jelenlegi, kb. 24+ verziós fejlesztési történetből lett kivonva — ha
a projekt módszertana érdemben változik (pl. új típusú forrás kerül elő, vagy a
Claude Code/claude.ai munkamegosztás átalakul), ezt a fájlt is frissíteni kell, nem
csak a döntési fájlt. Ez a fájl maga is a döntési fájl 0. szakaszába veendő fel, mint
egy különálló, "meta" jellegű tétel.
