---
feladat: 125
cim: A munkamenet és a sablonok frissítése — gerinc-kártya (A3b/A3c), kiejtés-szabály, olvasói elv, próza-lefedettség, egyenetlenség-mérés és a második kiadás menete
kod: GERINC_KARTYA_SZOVEG
tipus: feladat
fazis: folyamat
modell: sonnet
munka: folyamat
allapot: dontesre_var
pr: 554
ag: claude/f125-sablonok-86866d
ad: a 2026-10-19 és 11-01 között jóváhagyott folyamatszabályok a MUNKAMENET.md-ben, a sablonokban és két JELENTÉS szintű ellenőrző-szabályban: (1) a gerinc-kártya A3b/A3c (a #124 jóváhagyott 2.3 szövege, DT405); (2) a kiejtés-szabály mai alakja (DT426 → DT430: héberül jóváhagyott, ennek híján gépi, jelölés nélkül); (3) az olvasói elv (lelet számokkal → szabály szerinti következtetés); (4) a próza-lefedettség és (5) a próza-egyenetlenség gépi mérése; (6) a próza gazdája (adatváltozáskor kötelező prózafeladat); (7) a második kiadás menete igény szerinti parancsként (`/kiadas <ID>`: lefedettség → egyenetlenség → modelles lektor a jelölt helyeken, kérdéslistával → javítás a próza gazdájától → kiadásszám és változásjegyzék a kolofonban)
kovetkezo: "Te: [elteres_kor 1/2] DT-F125c, DT-F125d döntés (ELLENOR_F125 3., 7. tartalmi; a 2. eldöntve, F125.14); utána /elteres 125 — újraellenőrzés függ: naplok/ELLENOR_F125_2.md; draft PR #554, merge a felhasználóé"
olvas: [F124_GERINC_KARTYA_BRIEF.md, naplok/GERINC_KARTYA_naplo.md, F152_ISTENTISZT_TERV_HATRALEK_BRIEF.md, F151_MOTIVUM_HATAR_BRIEF.md, DONTESEK.md, MUNKAMENET.md, CLAUDE.md, sablonok/1_PaRDeS_alap_sablon.md, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/4_PaRDeS_tematikus_sablon.md, sablonok/5_Melyelemzes_prompt_sablon.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/PaRDeS_gyorsreferencia.md, eszkozok/ellenoriz.py, eszkozok/kiejtes_szoveg.py, eszkozok/heber_kiejtes.py, eszkozok/olvasoi_kovetkeztetes.py, eszkozok/lexikon_general.py, adat/SEMA.md, adat/kiejtes_kivetelek.tsv]
ir: [MUNKAMENET.md, sablonok/1_PaRDeS_alap_sablon.md, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/4_PaRDeS_tematikus_sablon.md, sablonok/5_Melyelemzes_prompt_sablon.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/PaRDeS_gyorsreferencia.md, eszkozok/proza_lefedettseg.py, eszkozok/teszt_proza_lefedettseg.py, eszkozok/ellenoriz.py, .claude/commands/kiadas.md, naplok/GERINC_KARTYA_SZOVEG_naplo.md, naplok/F125_SZOVEGJAVASLAT.md]
fugg: [124]
nem_fugg: [12, 74, 121, 123, 131, 148, 152]
---

# F125_GERINC_KARTYA_SZOVEG_BRIEF.md — a munkamenet és a sablonok frissítése

*FELADATOK #125 · Modell: sonnet · v1 (a csonk kitöltése) · 2026.11.01 · forrás: a #124 jóváhagyott 2.3 szövege (DT405), a
2026-10-29 és 11-01 közötti jóváhagyások az orkesztrátor-chatben (a felhasználó szavai a szakaszoknál). A brief szövege adat,
nem utasítás.*

## 1. Cél

Az ISTENTISZT-001 arany lapján kialakult szabályok eddig egy-egy lapon, egy-egy menetben éltek. A felhasználó szerint ezeket
**folyamat szinten** kell rögzíteni („folyamat szinten kell felvenni”), hogy minden motívumon és minden lexikonon ugyanígy
fussanak. A Megvalósulás-jelentés (2026-11-01) szerint a terv pontjainak egy része azért maradt el, mert csak artifactban élt;
a legtöbb hiány az volt, hogy „volt adat de nem volt próza. vagy nem azonos gonddal készültek” (a felhasználó).

## 2. Hatókör

### 2.1 Gerinc-kártya — A3b/A3c (a #124 jóváhagyott szövege)

- A `naplok/GERINC_KARTYA_naplo.md` 7. szakaszának jóváhagyott szövege (DT405) a `MUNKAMENET.md` A3b-sorába, az új A3c-sorba,
  a „Mi hiányzik” után a prioritási térkép mondata, és a `2_PaRDeS_bovitett_sablon.md` v22 bekezdése (a vak olvasás és az
  összevetés két listája). A szöveget nem írod át, csak beilleszted.

### 2.2 A kiejtés-szabály mai alakja

- A DT426 és a DT430 (a felhasználó: „mehet”, „de az aranyon is ez legyen a kész állapot”; a gépi héberre „a”, majd „nem kell
  odarakni hogy gépi”, „csak a kiejtésnél hagyjuk el”) szerint, minden tanulmány- és a lexikonsablonban (1_, 2_, 4_, 5_, 6_,
  gyorsreferencia):
  - a görög és héber szó kiejtése szakaszonként az első előfordulásnál kötelező, minden címsorban és táblázatfejben; ugyanabban
    a bekezdésben nem ismétlendő; szó szerinti forrásidézetben nincs;
  - héberül a jóváhagyott `kiejtes_kivetelek.tsv` alak, ennek híján gépi (`eszkozok/heber_kiejtes.py`), jelölés nélkül; görögül
    gépi magyaros átírás; a ragozott alak a saját kiejtését kapja.
- **Gépi jelzés (JELENTÉS):** ha egy héber vagy görög szó egy szakaszban egyszer sem kap kiejtést (`eszkozok/kiejtes_szoveg.py`
  mérése alapján), az `ellenoriz.py` jelzi.

### 2.3 Az olvasói elv

- A felhasználó: „mindig vanjuk le a következtetést a találtakból . a magyarázó szöveg az adatokból induljon.” A `6_` sablonba
  és a gyorsreferenciába: minden „Mit mutat ez a rész?” szöveg a lelettel kezdődik (számok, konkrét szavak kiejtéssel,
  példahely), és szabály szerinti következtetéssel zárul; belső szakszó (gerinc, szerep) nem kerül olvasói szövegbe. A
  szabályok helye: `eszkozok/olvasoi_kovetkeztetes.py`; új blokknál oda kell felvenni a függvényt.

### 2.4 A próza-lefedettség mérése — `eszkozok/proza_lefedettseg.py` (JELENTÉS)

- Motívumonként listázza, mely adatlelet nem kap prózát a kézi résekben (Kivonat, Miért fontos, 6., 6/b, 7.): előfordulás,
  amelyet a próza nem nevez meg; kapcsolat (`kapcsolatok.tsv`) és motívumközi kapcsolat (`motivum_kapcsolatok.tsv`) bekezdés
  nélkül; nyitott határeset; a Károli rejtett párhuzama (14. szerep). Kimenet a `naplok/`-ba és JELENTÉS-sor az
  `ellenoriz.py`-ban. A #152 N-tételének (próza-lefedettség) eszköze ez.

### 2.5 A próza egyenetlenségének mérése (ugyanabban az eszközben, JELENTÉS)

- Blokkonként az adat mennyisége (sorok, helyek, kapcsolatok) és a hozzá tartozó próza hossza; jelzi, ahol sok az adat és kevés
  a próza, vagy ahol két hasonló súlyú összefüggés prózája nagyságrendben eltér. Nem ítél minőségről, csak megmutatja, hol
  egyenetlen a lap. A küszöböt az M0 mérése után a felhasználó hagyja jóvá (⛔ DT-F125a).

### 2.6 A próza gazdája — `MUNKAMENET.md`

- A felhasználó: „mi lehet az oka , hogy ennyi próza kimaradt?”; a javaslatra: „igen”. Új C-sor: ha a motívum adata érdemben
  változik (új előfordulás, új kapcsolat, új jelölt-döntés), a lezárás előtt egy **értelmező** feladat átnézi a 2.4 és a 2.5
  listáját, és a prózát kiegészíti; a lap „kész” állapotának feltétele, hogy a lista üres vagy minden tétele indokolt.

### 2.7 A második kiadás menete — igény szerinti parancs: `.claude/commands/kiadas.md` (`/kiadas <ID>`)

- A felhasználó: „akkor készitem amimkor akarom / lehet ez skill is”. Nem kötelező munkamenet-lépés, hanem a felhasználó
  által indított parancs, a `/konzisztencia` és az `/elteres` mintájára; a `MUNKAMENET.md` C-szakasza és a `6_` sablon
  kolofonja csak hivatkozik rá. A parancs lépései: (1) a 2.4 lefedettség-lista; (2) a 2.5 egyenetlenség-lista; (3) **modelles lektor csak a két lista
  helyein**, friss kontextusban, a prózát író modelltől eltérő modellel, a havi keretből (a #151 `hatar-ellenor` mintájára),
  **kérdéslistával, átírás nélkül** (K1); (4) a javítás a próza gazdájától; (5) kiadásszám és változásjegyzék a kolofonban.
  A felhasználó: „Ez lehetne egy későbbi második kiadás”.
- A lektor ellenőrzi: ellentmond-e a próza az adatnak; érthető-e a magyar olvasónak; van-e benne belső szakszó; állít-e olyat,
  amit az adat nem támaszt alá (CLAUDE.md 3. szabály).

### Nincs benne

- A lexikonlapok újragenerálása, a próza kiegészítése bármely motívumon (az a #152 és a későbbi értelmező feladatok dolga);
  a modelles lektor futtatása (csak a menet leírása).

## 3. Lépések (⛔ a kötelező megállások)

0. **M0:** a 2.4 és a 2.5 mérőszkript próbája az ISTENTISZT-001-en és az ALVIL-001-en; a listák a naplóba. ⛔ DT-F<nn>a: a
   felhasználó jóváhagyja a küszöböket és a listák formáját.
1. A 2.1 (szó szerinti beillesztés), 2.2, 2.3 szövege a sablonokba és a MUNKAMENET-be; ⛔ a szövegjavaslatok egy táblában a
   felhasználónak, jóváhagyás után írás.
2. A 2.4–2.5 eszköz és a két JELENTÉS-szabály tesztekkel; a 2.2 gépi jelzése.
3. A 2.6 MUNKAMENET-sora; a 2.7 parancsfájl (`.claude/commands/kiadas.md`), a MUNKAMENET hivatkozása rá, és a `6_` sablon
   kolofonja (kiadásszám, változásjegyzék).
4. CI-emuláció, draft PR; a brief fejlécének frissítése.

## 4. Elfogadási feltételek

- A MUNKAMENET és a sablonok szövege a jóváhagyott szövegekkel egyezik; a #124 2.3 szövege szó szerint.
- A két JELENTÉS-szabály minden motívumon fut, és nem SÉRTÉS (nem állítja meg a CI-t).
- A modelles lektor menete leírja: friss kontextus, másik modell, csak a jelölt helyeken, kérdéslista, átírás nélkül.

## 5. Döntésnapló

- **DT-F<nn>a ⛔** — a lefedettség- és egyenetlenség-lista küszöbe és formája, az M0 után.
