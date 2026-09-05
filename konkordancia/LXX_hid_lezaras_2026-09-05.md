# LXX-híd lezárás és merge-javaslat (2026-09-05)

**Branch:** `lxx-hid-teljes-oszovetseg-2026-09-04`
**Státusz:** lezárva, mergelésre javasolva `main`-be

---

## 1. Összegzés

A teljes 39 könyves ószövetségi LXX (Septuaginta) görög Strong-számos konkordancia-híd elkészült, Károli 1908 verseléshez igazítva. Minden könyv `konkordancia/LXX_kivonat_<Könyv>.tsv` formában elérhető, egységes 5 oszlopos sémával (`Igehely | Strong-szám | Görög szóalak | Morfológiai kód | Forrás`), és egy közös, összesített dokumentáció (`konkordancia/LXX_kivonat_README.md`) írja le a forrást, a módszertant, az ismert korlátokat és a könyv-specifikus megjegyzéseket.

A munka során 8 általános hibaosztály és 4 további, egyedi könyvekhez kötődő "Dániel-mintázatú" fejezethatár-eltolódás került azonosításra és javításra, teljes tartalmi (nem csak szám alapú) egyeztetéssel. Egyetlen ismert, dokumentált, nem blokkoló nyitott eset maradt: Énekek éneke 6/7 fejezethatár.

## 2. Az utolsó 5 pontos ellenőrzési kör eredménye

| # | Terület | Eredmény | Ellenőrzés módja |
|---|---|---|---|
| 1 | 4Móz 12/13 fejezethatár | Javítva (`numeri_12_13_eltolas()`) | Felhasználó önállóan ellenőrizte: `4Móz 12:16` nem létezik, `4Móz 13:1` helyesen kezdődik |
| 2 | Jób 38-40 lánc-eltolódás | Javítva (`job_38_41_eltolas()`) | Felhasználó önállóan ellenőrizte: Jób 39 pontosan 38 verssel zárul — ez a Károli-hagyomány valódi felosztása, nem hiba |
| 3 | Prédikátor (térkép nélküli könyv) | Javítva (`predikator_eltolas()`, 4 határpont) | Felhasználó önállóan ellenőrizte mind a 7 érintett fejezetet (1, 2, 8, 9, 10, 11, 12) — mindegyik pontosan a Károli valódi utolsó versszámával zárul |
| 4 | Jób/Péld genuin LXX-többletek | Dokumentálva, nincs kódmódosítás | README rögzíti: Jób 17:16, 37:24, Péld 12:28 — ugyanaz a jelenség, mint a már ismert Jób 42:17 toldalék |
| 5 | `Betu_utotag_kizarva.tsv` duplikátumok | Törölve | Felhasználó önállóan ellenőrizte: 136 sor (135 adat + fejléc), 0 duplikátum |

Mind az 5 pont hibamentesen lezárva, felhasználói önálló ellenőrzéssel megerősítve.

## 3. Ismert, nyitva hagyott eset: Énekek éneke 6/7

- **Jelenség:** a kimenetben bogus `Én 6:11`–`6:13` címkék jelennek meg (Károli 6. fejezete valójában 10 versig tart).
- **Gyökérok:** a nyers `Song of Solomon 6` oldalon LÉTEZIK egy valódi `[7:1]` zárójeles kereszthivatkozás, de ez a blokk KÖZEPÉN helyezkedik el (a nyers "13" jelölésen), nem a "11" vagy "12" jelöléseken, amelyek megelőzik. A kód `zarojel_volt` alapú átirányítási mechanizmusa csak a zárójeltől kezdve, előre hat az adott blokkon belül — így a blokk korábbi szavai (a nyers 11-12 jelölésű versek) nem kapják meg az átirányítást, és érvénytelen, oldal-lokális számozással kerülnek be.
- **Döntés:** ez a hibaosztály (VAN zárójel, mégsem aktiválódik időben) eltér a "Dániel-mintázattól" (NINCS zárójel egyáltalán), és külön, célzottabb kódmódosítást igényelne (pl. visszafelé néző zárójel-keresés a blokkon belül). A felhasználó kifejezett döntése alapján ez jelenleg **nem lett javítva**, csak diagnosztizálva és dokumentálva a README-ben.
- **Miért nem blokkoló:** izolált, egyetlen könyv egyetlen fejezethatárára korlátozódik; a hiba jellege (bogus, ki nem található verscímke) önmagában is felismerhető és ellenőrizhető a felhasználó vagy egy jövőbeli felhasználó számára, nem néma/rejtett adatvesztés. A README explicit módon, "nincs javítva" jelöléssel rögzíti — ez tudatosan vállalt, dokumentált korlát, nem elfelejtett hiba.

## 4. Lefedettség

- **39/39 ószövetségi könyv** feldolgozva, `konkordancia/LXX_kivonat_*.tsv` fájlokban.
- Közös riport-fájlok:
  - `konkordancia/Betu_utotag_kizarva.tsv` — 135 sor, duplikátum-mentes.
  - `konkordancia/Nem_parszolhato_terkep_ertekek.tsv` — 145 sor, kategorizálva (`Nem_parszolhato_ertekek_kategorizalas.md`).
- Egységes dokumentáció: `konkordancia/LXX_kivonat_README.md` (forrás/módszertan, ismert korlátok, összesített táblázat, könyv-specifikus megjegyzések — beleértve a "Dániel-mintázat" 4 esetét és az Énekek éneke 6/7 nyitott esetet).

## 5. Merge-javaslat

**Javaslat: a `lxx-hid-teljes-oszovetseg-2026-09-04` branch mergelhető a `main`-be.**

Indoklás:
- Mind a 39 könyv elkészült, egységes sémával és dokumentációval.
- Minden korábban azonosított hibaosztály (8 általános + 4 "Dániel-mintázatú" egyedi eset) javítva és tartalmilag (nem csak szám alapján) ellenőrizve, a felhasználó saját, független ellenőrzésével megerősítve.
- Az egyetlen fennmaradó nyitott eset (Énekek éneke 6/7) egy jól körülhatárolt, izolált, a README-ben explicit módon dokumentált korlát — nem rejtett vagy néma hiba, és nem érinti a többi 38 könyv integritását.
- A forrás (`studybible.info`) licenc-státusza tisztázatlan, ezért az adat továbbra is csak belső, nem publikus felhasználásra dokumentált — ez a korlátozás a README-ben rögzítve marad a merge után is.

**Fenntartás/emlékeztető:** a felhasználó korábbi explicit utasítása szerint ez a branch csak külön jóváhagyással kerülhet be a `main`-be — ez a dokumentum a tartalmi lezárást és a technikai javaslatot adja, a tényleges merge-műveletet a felhasználó hagyja jóvá és hajtja végre (vagy kéri annak végrehajtását külön lépésben).

---

*Készült: 2026-09-05, Claude Sonnet 5 közreműködésével.*
