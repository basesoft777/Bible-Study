# SZOTAR S1.7 — héber kiejtés-jelöltek (D28, 26 lemma)

*2026.09.28 · `SZOTAR_BRIEF.md` v1.7 §3 S1.7. Csak jelölt-lista, nem ír a
kivétel-táblába — a jóváhagyás az S1.7 utáni ÁLLJ tárgya.*

## 1. 24 vagy 26? — az eltérés oka

A `SZOTAR_BRIEF.md`-ben **mindkét szám előfordul**, mert két, egymást
felülíró döntésréteg van benne:

- A **8. szakasz (Döntésnapló) D13 sora** — a brief v1-es, 2026.09.23-i
  eredeti szövege — **24/24 lemmát** ír célként. Ez a bejegyzés a
  döntésnapló append-only konvenciója szerint **nem lett utólag
  átírva** (a projekt szokása: a döntésnapló historikus, a hatályát egy
  későbbi D-sor vonja vissza vagy pontosítja, a régi sor szövege marad).
- A **D28 (2026.09.27)** ezt kifejezetten felülírja: a `T2.2` (`ed79575`)
  két új héber tokent (H8414 *tohu*, H0922 *bohu*, a `TEREMT-002`
  motívumhoz) vitt be a jóváhagyott brief előtt — a felhasználó a
  szűkítés helyett a bővítést választotta, és rögzítette az általános
  hatókör-szabályt: *„a szótári réteg héber hatóköre a menet indító
  commitjának tokenhalmaza; a szám ebből származik, nem rögzített”*
  (D28). Ez a szám **24 → 26**.
- A brief minden **más** helye — a §0 0.4/0.5/0.11/0.17 sora, az S3/S9/S14
  szerep-leírás, a **§3 S1.7 tétel maga** („26 lemmájára”), a §3 ÁLLJ-sor,
  a §4 Várt számok táblája („héber kiejtés-jelöltek: 26 (D28)”) és a §7
  1. menet prompt záró sora — **26-ra van frissítve** (l. a fejléc „v1.2 →
  v1.3 változásai” bekezdését: „D28 új” és a §3/§4/§7 26-ra igazítva).

**Következtetés: az irányadó szám 26, nem 24.** A D13 24-es száma
történeti maradvány egy már felülírt döntésből, nem érvényes cél. Ez a
menet a **26**-os hatókört állítja elő.

## 2. Hatókör-ellenőrzés (D28 szabálya: „a menet indító commitjának
tokenhalmaza”)

Az `adat/elofordulasok.tsv` `strong` mezőjének `+`-on szétbontott,
H-kezdetű, egyedi értékei (a `lexikon_general.py` `strong_tokens =
strong.split('+')` logikájával, minden motívumon át) **jelen menetben
(2026.09.28, `claude/szotar-s1-menet`) pontosan 26 tokent adnak** — nincs
eltérés a D28-nál mért 26-tól, tehát **nincs ok új ÁLLJ-ra** (a D28
szabálya csak akkor kívánna megállást, ha egy token kiesne vagy a
G-halmaz változna).

| Strong | Motívum(ok) | OSHL lemma |
|---|---|---|
| H0127 | HAMART-001 | אֲדָמָה |
| H0430 | MENNY-001 | אֱלֹהִים |
| H0779 | HAMART-001 | אָרַר |
| H0922 | TEREMT-002 | בֹּהוּ |
| H1121 | MENNY-001 | בֵּן |
| H2403 | HAMART-001 | חַטָּאָה |
| H2416 | ANTROP-001 | חַי |
| H2555 | HAMART-001 | חָמָס |
| H3548 | KIRALY-001 | כֹּהֵן |
| H3678 | KIRALY-001 | כִּסֵּא |
| H4467 | KIRALY-001 | מַמְלָכָה |
| H5303 | HODIT-001, MENNY-001 | נְפִלִים |
| H5315 | ANTROP-001 | נֶ֫פֶשׁ |
| H6093 | HAMART-001 | עִצָּבוֹן |
| H6975 | HAMART-001 | קוֹץ |
| H7043 | HAMART-001 | קָלַל |
| H7121 | ISTENTISZT-001 | קָרָא |
| H7451 | HAMART-001 | רַע |
| H7496 | HODIT-001 | רְפָאִים |
| H7497 | HODIT-001 | רָפָה |
| H7585 | ALVIL-001 | שְׁאוֹל |
| H7843 | HAMART-001 | שָׁחַת |
| H8004 | KIRALY-001 | שָׁלֵם |
| H8034 | ISTENTISZT-001 | שֵׁם |
| H8414 | TEREMT-002 | תֹּ֫הוּ |
| H8415 | TEREMT-001 | תְּהוֹם |

## 3. Módszer

- Forrás: `konkordancia/OSHL_lexikalis_index.tsv` `atiras` mezője (SBL
  Academic-stílusú, Unicode diakritikus jelekkel), **nem** a nyers
  niqqud-szöveg — a D24 szerint ez a jobb irányú módszer, mert a nehéz
  esetek (néma *he*, shuruk/holam-vav mint magánhangzó-hordozó, dagesh)
  már eldöntöttek az OSHL-átírásban (l. a `naplok/
  SZOTAR_S0_heber_jeloltek.tsv` korábbi, nyers-niqqud-alapú próbájának
  tanulsága, amely pontosan ezt a következtetést vonta le 55,6%-os
  egyezéssel, D24).
- Szabálytábla: `adat/kiejtes_heber_jeloltszabalyok.tsv` — 20 szekvenciális,
  literális karakter-csere (aleph/ayin elesik; š→s, ṣ→c, ṭ→t, ḥ→h, q→k,
  y→j; a makron/cirkumflex hosszú magánhangzók á/é/í/ó/ú-ra; a redukált
  a/e rövidre). A két meglévő, jóváhagyott `adat/kiejtes_kivetelek.tsv`
  sor (H7121 *qārāʾ*→„kárá", H8034 *šēm*→„sém") igazolja a fő szabályokat
  — mindkettő pontosan visszaadva.
- Generátor: `eszkozok/heber_kiejtes_jeloltek.py` → `naplok/
  SZOTAR_S1_heber_jeloltek.tsv` (26 sor, nem ír a kivétel-táblába).
- **Homográf/inflektált OSHL-változatok** (5 Strong-nál van több OSHL-sor:
  H1121, H2403, H2416, H7451, H7497): a fájl-sorrend szerinti **első**
  bejegyzés a reprezentatív (nincs gyakorisági mező a választáshoz) — a
  további változat(ok) a `megjegyzes` oszlopban fel vannak sorolva, hogy a
  jóváhagyó ne veszítse el őket.

## 4. Egyezési arány — méréshatár

A brief a „26 lemmán mért egyezési arányt" kéri. **Létező, jóváhagyott
magyar referencia jelenleg csak 2 a 26 tokenből** van (`adat/
kiejtes_kivetelek.tsv`, KIEJT-migráció): H7121 és H8034. A projektben
elérhető másik héber „arany" készlet (`naplok/
SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv`, 49 pár, raw niqqud-alapú) csak
ugyanezt a két Stronggot fedi a 26-os készletből (a többi arany pár más
lemmákhoz tartozik — l. a `naplok/SZOTAR_S0_heber_jeloltek.tsv` régi
próbájának 36 egyedi párja, amelyből is csak ugyanez a kettő egyezik
Stronggal). **Ez a korlát nem új felismerés — a D24 már rögzítette, hogy
„az 55,6%-os próba nem mérföldkő", és a S1.7-nek éppen ez a szerepe: az
OSHL-alapú módszertan újramérése, amelyhez ez a menet minden elérhető
referenciát felhasznált.**

| Mérőszám | Érték |
|---|---|
| Jóváhagyott referenciával rendelkező token | 2/26 (H7121, H8034) |
| Ezekre az egyezés | **2/2 (100%)** |
| Referencia nélküli (új jelölt, jóváhagyásra vár) | 24/26 |

**A 24 új jelölt helyessége emberi jóváhagyást igényel** — ez pontosan az
S1.7-utáni ÁLLJ tárgya, nem gépi mérhető ezen a mintaméreten.

## 5. Eredmény (1. kör, 2026.09.28)

`naplok/SZOTAR_S1_heber_jeloltek.tsv`: 26 sor, mind a 26 Stronghoz van
OSHL-referencia (0 hiányzó), 2/2 egyezés a meglévő jóváhagyott
mintákon, 0 eltérés.

**A felhasználó az 1. kört NEM hagyta jóvá egyben** — l. a 7. szakaszt.

## 6. H0430 BDB-etimológia-határ — vizsgálat (2026.09.29)

A felhasználó ÁLLJ-t kért a `konkordancia/BDB_etimologia_kezi_hatarok.tsv`
H0430-sorára: a határvég (`...compare also Nes^l. c,)`) csonkának vagy
OCR-hibának tűnt. Ellenőrzés a nyers `konkordancia/lexikonok_nyers/
BDB.lexicon` (SQLite) `Definition` HTML-mezőjén, közvetlenül a forrásból:

```html
... compare also <lookup onclick="bdbabb('Nes')">Nes<sup>l. c</sup></lookup>,)
```

Ez pontosan megfelel a tisztított TSV-ben látott `Nes^l. c,)` alaknak — a
`^` a `<sup>` (superscript) jelölés konszolidált karaktere, ugyanaz a
konvenció, mint minden más rövidítésnél a táblában (pl. `Jos^Ant.`,
`Ba^ZMG`). A `Nes` egy kattintható BDB-rövidítés-hivatkozás (`Nes` =
Nestle, bibliakutató neve), az `l. c` (*loco citato*, „a hivatkozott
helyen”) a szokásos latin rövidítés, utána egyetlen vessző és a nyitó
zárójel lezárása. **A raw HTML-ben sincs semmi a `,)` előtt vagy után,
ami hiányzik a tisztított szövegből — a határ NEM csonka, NEM
OCR-hiba.** A `)` a `(feminine 1Kin 11:33; ... compare also Nes^l. c,)`
teljes zárójeles betoldást zárja le, közvetlenül utána a szócikk
számozott (`1. plural in number...`) használati szakasza kezdődik — ez
pontosan az a fajta határ, amit a `gepi` (em-dash + „1 ”) minta más
szócikkeknél automatikusan megtalál, itt csak azért `javaslat`, mert
nincs em-dash a forrásban.

**Javaslat: a jelenlegi határ helyes, nincs jobb végpont.**

**Jóváhagyva (2026.09.29):** a felhasználó a fenti vizsgálat alapján
jóváhagyta a H0430-sort is — `konkordancia/BDB_etimologia_kezi_hatarok.tsv`
`allapot=jovahagyott` (a forrás: `eszkozok/bdb_etim_hatarok_import.py`
`JOVAHAGYOTT` halmaza, most már mind az 5 Stronggal). Ezzel a BDB-
etimológia-határ mind az 5 kézi javaslata jóváhagyott állapotban van, 0
`javaslat` maradt.

## 7. 2. kör — szabályjavítás (D34–D37) és eredmény (2026.09.29)

A felhasználó a chatben megadott, kézzel ellenőrzött 26-soros várt
listával mérte az 1. kört, és 9 eltérést talált (mind a begadkefat-
spirantizáció hiánya vagy a `ḥ→h` szabály miatt). Javítás:

- **D34** — új `spirantize()` lépés (`eszkozok/heber_kiejtes_jeloltek.py`),
  amely a pontozott `oshl_lemma` mezőben minden ב/כ/פ előfordulásnál
  megnézi, van-e dagesh (a rákövetkező kombináló jelek közt `ּ`) vagy
  szókezdő-e a betű — ha egyik sem, a megfelelő atirás-karaktert (b/k/p)
  lágy alakra (v/ch/f) cseréli, MIELŐTT a szabálytábla lefutna. Igazolva:
  sem a lemma, sem az atirás nem tartalmaz két különböző nyers alakot
  (pl. `b` és a hozzá tartozó lemma-betű) ugyanabban a szóban átfedő
  sorrendben — a pozíció-igazítás (a lemma ב/כ/פ-sorrendje = az atirás
  b/k/p-sorrendje) mind a 26 szóra ellenőrizve helyes.
- **D35** — `adat/kiejtes_heber_jeloltszabalyok.tsv` 6. sora `ḥ→h`-ról
  `ḥ→ch`-ra javítva; a plain `h` (he) karaktert nem érinti (nincs rá
  szabálysor, változatlan marad).
- **D36** — új `adat/kiejtes_heber_kivetelek.tsv` (strong, ertek, indok,
  datum): H2555 → „hámás” kézi felülbírálással, a szabályfuttatás UTÁN
  alkalmazva. A jelentésben (`arany_egyezes` oszlop) „kivetel” jelölést
  kap.
- **D37** — az alef/ajin-elhagyás (már az 1. körben is így volt) explicit
  megerősítve a H2403-ra is (nincs eltérő eset).

**Újrafuttatva** (`python eszkozok/heber_kiejtes_jeloltek.py`): mind a 26
sor **pontosan** egyezik a felhasználó által megadott várt listával.

| Strong | 1. kör (hibás) | 2. kör (javított) | Várt | Egyezik |
|---|---|---|---|---|
| H0127 | adámá | adámá | adámá | ✔ (változatlan) |
| H0430 | elóhím | elóhím | elóhím | ✔ (változatlan) |
| H0779 | árar | árar | árar | ✔ (változatlan) |
| H0922 | bóhú | bóhú | bóhú | ✔ (változatlan) |
| H1121 | bén | bén | bén | ✔ (változatlan) |
| H2403 | hattáá | **chattáá** | chattáá | ✔ (javítva, ḥ→ch) |
| H2416 | haj | **chaj** | chaj | ✔ (javítva, ḥ→ch) |
| H2555 | hámás | hámás | hámás | ✔ (kivétel, D36) |
| H3548 | kóhén | kóhén | kóhén | ✔ (változatlan) |
| H3678 | kissé | kissé | kissé | ✔ (változatlan) |
| H4467 | mamláká | **mamláchá** | mamláchá | ✔ (javítva, begadkefat) |
| H5303 | nepilím | **nefilím** | nefilím | ✔ (javítva, begadkefat) |
| H5315 | nepes | **nefes** | nefes | ✔ (javítva, begadkefat) |
| H6093 | iccábón | **iccávón** | iccávón | ✔ (javítva, begadkefat) |
| H6975 | kóc | kóc | kóc | ✔ (változatlan) |
| H7043 | kálal | kálal | kálal | ✔ (változatlan) |
| H7121 | kárá | kárá | kárá | ✔ (jóváhagyott gold) |
| H7451 | ra | ra | ra | ✔ (változatlan) |
| H7496 | repáím | **refáím** | refáím | ✔ (javítva, begadkefat) |
| H7497 | rápá | **ráfá** | ráfá | ✔ (javítva, begadkefat) |
| H7585 | seól | seól | seól | ✔ (változatlan) |
| H7843 | sáhat | **sáchat** | sáchat | ✔ (javítva, ḥ→ch) |
| H8004 | sálém | sálém | sálém | ✔ (változatlan) |
| H8034 | sém | sém | sém | ✔ (jóváhagyott gold) |
| H8414 | tóhú | tóhú | tóhú | ✔ (változatlan) |
| H8415 | tehóm | tehóm | tehóm | ✔ (változatlan) |

**Eredmény: 26/26 egyezés — mind a 26 jelölt jóváhagyva (2026.09.29).**
Nem íródott az `adat/kiejtes_kivetelek.tsv`-be (az S1 „nulla-diff” menet
kimenetet nem változtat) — a formális rögzítés az S2.1 tétele. A
`nulladiff.sh 8f5a1eb` a D31 két `--csere`-jével ezen a ponton lefutott:
`exit 0`, üres diff.

## 8. Lezárás (2026.09.29)

A H2555-kivétel (D36) helye egyértelműsítve: `adat/kiejtes_heber_kivetelek.tsv`
a **jelölt-generátor** (`eszkozok/heber_kiejtes_jeloltek.py`) bemenete,
csak a `naplok/SZOTAR_S1_heber_jeloltek.tsv` jelölt-listát alakítja —
**nem azonos** a végleges, render által olvasott `adat/kiejtes_kivetelek.tsv`
kivétel-táblával, abba (mind a 26 jóváhagyott lemmával) csak az S2.1
tétel ír.

A H0430 BDB-határ a 6. szakasz vizsgálata alapján szintén jóváhagyva —
mind a 26 héber kiejtés-jelölt és mind az 5 BDB-etimológia-határ
jóváhagyott állapotban van. **Az S1 (1. menet) ezzel lezárva.** A branch
(`claude/szotar-s1-menet`) még nincs a `main`-ben — következő lépés a CI
és a `fuggetlen-ellenor` ügynök, majd a merge.
