# A join-tábla (Károli-Strong számozás) felépítésének folyamata — bővített és tematikus sablonoknál

*Kiegészítés a PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md-hez. Az SzPA-integráció felfüggesztése (v23) óta a join-tábla gyakorlati formájában kétoszlopos: Strong-szám + Károli-szó — nem a korábban tervezett háromoszlopos (Strong+Károli+SzPA) szerkezet. Ez a fájl azt írja le, hogyan épül fel ez a kétoszlopos join a két fő sablontípusnál.*

---

## Oszlopszerkezet — `konkordancia/Karoli_Strong_kivonat.tsv` (2026.08.24-től, 8 oszlop)

```
Igehely | Strong-szám | Károli-szó | Azonosítás módja | Forrás-tanulmány |
Megbízhatóság | Szófaj | Gyök/Származtatás
```

Az utolsó két oszlop (**Szófaj**, **Gyök/Származtatás**) nem a tanulmány-készítés melléktermeéke, hanem a `konkordancia/Strong_szotar.tsv`-ből (lásd `Strong_szotar_README.md`) származó, Strong-szám alapú, egyszerű összefésüléssel (nem manuálisan) feltöltött adat — az `eszkozok/merge_karoli_szofaj.py` script generálja. A script a Strong-szám nulla-kitöltési eltérését normalizálja (a join-tábla `H430` formája ↔ a szótár `H0430` formája), de **nem bontja szét** az összetett, `+`-jellel jelölt sorokat (pl. `H8414+H922`) — ezeknél a két új oszlop üresen marad, mert nincs egyértelmű egy-az-egyhez Strong-szám megfeleltetés. Új Károli-Strong sor felvételekor a két oszlopot **ugyanezzel a scripttel** (vagy azonos logikával) kell újragenerálni, nem kézzel kitölteni.

---

## Alapelv: a join-tábla nem külön projekt, hanem a tanulmány-készítés melléktermeéke

A korábban rögzített "tanulmányvezérelt, kumulatív" elv (7.1-7.2 pont) most, hogy csak a Károli-oldal aktív, a lehető legegyszerűbb formájában valósul meg: **Strong-szám + Károli-szó, semmi több**. Nincs előre, egyben legenerálandó teljes join-tábla — minden tanulmány csak annyit ad hozzá, amennyire ténylegesen szüksége van, és ez a "melléktermék" egy közös `Karoli_Strong_kivonat.tsv`-be visszaírva a következő tanulmány számára is azonnal elérhetővé válik (grep, nem újragenerálás).

---

## 1. Bővített sablonnál — a szűkítés a keresés ELŐTT történik

```
1. Tanulmány 2. pontja: kiválasztunk kb. 6-8 kulcsszót a kritériumlista alapján
   (teológiai súly / elmosódás a fordításban / motívum-kapcsolódás /
   kereszthivatkozási potenciál / exegetikai vita / objektív ritkaság)
2. Minden kiválasztott kulcsszóhoz: TAHOT/TAGNT Strong-szám lekérdezve
   (gépi, gyors — grep a konkordancia/TAHOT_kivonat.tsv-ből)
3. Károli-szó azonosítva hozzá — tartalom-alapon (angol gloss/KJV-híd
   segítségével, ahogy 1Móz 1:2-nél és 1:3-4-nél gyakoroltuk)
4. Ez a pár (Strong + Károli-szó) bekerül A) a tanulmányba, B) a közös
   Karoli_Strong_kivonat.tsv-be
5. Legközelebb, ha egy másik tanulmány ugyanerre a szóra hivatkozik →
   már csak grep, nincs új munka
```

**Jellemző mennyiség:** egy tanulmányonként 6-8 új Károli-Strong sor, ebből jellemzően csak 1-3 igényel ténylegesen tartalom-alapú (nem gépi) mérlegelést.

---

## 2. Tematikus sablonnál — a szűkítés a keresés UTÁN történik

**A kulcskülönbség:** nincs előzetes válogatás — a feladat maga (egy motívum *összes* előfordulásának megtalálása) automatikusan generál egy találati listát, és *minden egyes találathoz* kell Károli-Strong pár, nem csak néhányhoz.

```
1. Motívum Strong-száma azonosítva
2. Teljes körű grep a TAHOT_kivonat.tsv / TAGNT_kivonat.tsv-n erre a
   Strong-számra → találati lista (pl. 15 igehely)
3. MINDEN egyes találatnál: Károli-szó azonosítása (tartalom-alapon)
   → akár 10-20 db Károli-Strong párosítás egy tanulmányban
4. Tartalmi értékelés: melyik a valódi lexikai egyezés, melyik zárandó ki
   (mint korábban a Mat 12:18 / 1Pét 1:22 eset a pneuma/pszükhé-motívumnál)
5. A megerősített találatok Károli-Strong párjai bekerülnek a közös
   Karoli_Strong_kivonat.tsv-be
```

**Jellemző mennyiség:** egy tanulmányonként akár 10-20 új Károli-Strong sor — nagyobb egyszeri terhelés, mint a bővítettnél, de ugyanaz a kumulatív elv érvényes.

---

## A két folyamat összehasonlítása

| | Bővített sablon | Tematikus sablon |
|---|---|---|
| Szűkítés helye | keresés ELŐTT (kritériumlista) | keresés UTÁN (találati lista értékelése) |
| Tipikus mennyiség/tanulmány | 6-8 szó | 10-20 előfordulás |
| Kritériumlista szerepe | közvetlenül szűkít | nincs — a Strong-keresés maga a szűrő |
| Kapcsolódás a Lezárási checklisthez | nem releváns (nincs "lezárás" fogalom) | igen — a 11. pont (🔍 STEPBible-ellenőrizve) most a Károli-Strong párosítás tényét is dokumentálhatja, nem csak a Strong-keresés megtörténtét |

---

## Gyakorlati következmény: a négy lezárt tematikus tanulmány visszamenőleges ellenőrzése felértékelődött

A korábban nyitva hagyott tétel (tehóm, segítségül hívni, Rafeusok, hádész visszamenőleges STEPBible-ellenőrzése) most **kettős haszonnal** járna, ha elindulna: nemcsak a Strong-adatot validálná (ahogy eredetileg terveztük), hanem **egyúttal a Károli-Strong join-táblát is építené** minden megerősített előforduláshoz — nem csak ellenőrzés, hanem egyben adatgenerálás is.
