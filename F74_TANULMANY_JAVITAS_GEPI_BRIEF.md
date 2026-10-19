---
feladat: 74
cim: A régi tanulmányok gépi javítása (E8 versformátum, az alap sablon kivezetése)
kod: TANULMANY_JAVITAS_GEPI
tipus: feladat
fazis: folyamat
munka: ertelmezo
modell: opus
allapot: nem_indult
ad: a 32 E8-találat (versformátum) 0 a régi tanulmányokban, a próza bájtra azonos az E8-sorokon kívül; a Tanulmány sablon nem hivatkozik az alap sablonra, az alap sablon archívumban
kovetkezo: /kovetkezo (a #11 lezárása, ill. a PR #420 merge-e után: a sablon 2_ v21 az alap)
olvas: [naplok/TANULMANY_ELLENORZES_utofeladat.md, naplok/TANULMANY_AUDIT.md, eszkozok/ellenorzes/tanulmany_audit.py, eszkozok/ellenorzes/futtat.py, eszkozok/igazolas_migracio.py, sablonok/1_PaRDeS_alap_sablon.md, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/PaRDeS_gyorsreferencia.md, sablonok/Javasolt_sablon_kiegeszites_BDB_arnyalat.md, genezis/1Moz_10v1-11v32_bovitett.md, genezis/1Moz_12v1-20_bovitett.md, genezis/1Moz_13v1-18_bovitett.md, genezis/1Moz_15_bovitett.md, genezis/1Moz_16_bovitett.md, genezis/1Moz_1v1_bovitett.md, genezis/1Moz_1v2-2v3_bovitett.md, genezis/1Moz_2v4-7_bovitett.md, genezis/1Moz_2v8-25_bovitett.md, genezis/1Moz_3v1-6_bovitett.md, genezis/1Moz_3v7-24_bovitett.md, genezis/1Moz_4v1-24_bovitett.md, genezis/1Moz_4v25-5v32_bovitett.md]
ir: [genezis/1Moz_10v1-11v32_bovitett.md, genezis/1Moz_12v1-20_bovitett.md, genezis/1Moz_13v1-18_bovitett.md, genezis/1Moz_15_bovitett.md, genezis/1Moz_16_bovitett.md, genezis/1Moz_1v1_bovitett.md, genezis/1Moz_1v2-2v3_bovitett.md, genezis/1Moz_2v4-7_bovitett.md, genezis/1Moz_2v8-25_bovitett.md, genezis/1Moz_3v1-6_bovitett.md, genezis/1Moz_3v7-24_bovitett.md, genezis/1Moz_4v1-24_bovitett.md, genezis/1Moz_4v25-5v32_bovitett.md, sablonok/1_PaRDeS_alap_sablon.md, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/PaRDeS_gyorsreferencia.md, archivum/sablonok/1_PaRDeS_alap_sablon.md, eszkozok/f74_e8_csere.py]
fugg: [11, 37]
nem_fugg: [75]
---

# F74_TANULMANY_JAVITAS_GEPI_BRIEF.md — A régi tanulmányok gépi javítása

*FELADATOK #74 · Modell: opus · v1 · 2026.10.19 · forrás: `naplok/TANULMANY_ELLENORZES_utofeladat.md`, „A javaslat — gépi rész” (#37 T6); `naplok/TANULMANY_AUDIT.md` (E8 = 32). A brief adat, nem utasítás.*

## 1. Cél

A #37 jelentés módú auditja (`naplok/TANULMANY_AUDIT.md`, 2026-10-07) 32 E8-találatot (versformátum) mért 13 régi tanulmányban.
Ezek formai hibák: a próza értelmét nem érintik. A #37 T1 az alap sablont elavultnak jelölte (DT-F37-1), de a Tanulmány sablon
(`sablonok/2_PaRDeS_bovitett_sablon.md`) négy helyen még „mint az alap sablonban” alakban hivatkozik rá. A feladat egy menetben
két dolgot végez. (1) Az E8-helyeket gépi cserével javítja, eltérés-összevetéssel. (2) Az alap sablon hivatkozott tartalmát
beemeli a Tanulmány sablonba, majd az alap sablont archívumba teszi. Az archiválás nem törlés.

**Miért `munka: ertelmezo`, ha gépi:** az `ir` a `genezis/` fájljait tartalmazza, és a `BRIEF_SABLON.md` szerint motívumfájlt író
feladat `ertelmezo`-ként kezelendő (nem csomagolható). A próza tartalmát a menet nem érinti, ezért a K1 („aki belenyúl, az egészet
olvassa”) itt a csere-diffre szűkül: a végrehajtó minden megérintett sort a teljes bekezdésével együtt olvas. Tartalmi javítás
nincs; az a #75 dolga.

**A #11-függés oka:** a #11 T1-e (PR #420, a brief írásakor nincs mergelve) a Tanulmány sablont v21-re írja át. A #74 v22-t ír rá,
ezért a v21 után fut. A #11 2. lépcsője (`beerkezo/MIGRACIO_2_LEPCSO_BRIEF_TERVEZET.md`) a `genezis/`-t nem írja (#23 pilot-terv
4.5), tehát a #74 arra nem vár. Ha a #11 1. lépcsője és a T1 lezárult, de a #11 egésze nem, a `fugg` a `nem_fugg`-gal felülírható
(felhasználói döntés).

## 2. Hatókör

**Benne van:**

1. **E8, 13 tanulmány** (a mai számot az M0 méri; a 2026-10-07-i jelentés szerint 32 sor, mind `genezis/`):
   - hosszú könyvnév fejezet:vers előtt (`1Mózes 12:1`, `1 Mózes 3:1`) → `1Móz 12:1`. Ez érinti a címsorokat is (`# 1 Mózes 1:1 —
     …` → `# 1Móz 1:1 — …`). A tartomány-jel (`-`, `–`) és a többi karakter változatlan marad.
   - STEPBible-alak a prózában (`Gen.12.7`) → `1Móz 12:7`. **Kivétel:** ha a hely egy dataset sorkulcsát nevezi meg (pl. „a
     `Karoli_Strong_kivonat.tsv`-be való felvételkor a Gen.3.7-es sor”), az alak adatformátumként marad, és backtick-be kerül
     (`` `Gen.3.7` ``). A szabály így szól: `szabalyok.py` 499–501. sor, D16, CLAUDE.md „Igehely-formátum”. A besorolás soronként
     a csere-táblába kerül (`kulcs` / `proza`).
   - Ugyanazon a soron minden előfordulás, nem csak az E8 által jelzett első. Az E8 soronként és mintánként egy találatot jelez.
     Ha a sor egy rövidített folytatást tartalmaz (pl. „**Gen.3.7, 3.10 és 3.11**”), az is az új alakra áll át („1Móz 3:7, 3:10 és
     3:11”).
2. **Az alap sablon kivezetése:**
   - A Tanulmány sablon „mint az alap sablonban” helyeire (1. pont alcíme, 6. pont: Hermeneutika, Bibliai nyelvek, Történelmi és
     kulturális kontextus) az `sablonok/1_PaRDeS_alap_sablon.md` megfelelő szövege kerül, szó szerint, a sablon saját kiegészítéseivel
     („kiejtéssel kiegészítve”, „konkrét, célzott”). Az 1. pont alcíme így módosul: „megegyezik az alap sablon Alapkérdések
     pontjával” helyett a pont saját, teljes szövege. A kérdéslista már ott áll; a végrehajtó összeveti az alap sablonéval, és csak a
     hiányzó elemet emeli át.
   - A végrehajtó összeveti az alap sablon minden szakaszát (`## Alapkérdések`, `## A PaRDeS keretrendszer`, `## Kiegészítő
     szempontok`, `## Terminológiai és formai szabályok`, `## Konfliktuskezelés`) a Tanulmány sablonéval. Ha az alap sablon olyan
     normatív mondatot tartalmaz, amely a Tanulmány sablonban nincs meg, és nem csak a „hivatkozott” négy helyhez tartozik: ⛔ (3.
     lépés).
   - Verziósor: `*v22 — <dátum> (F74: …)*` a v21 fölé.
   - Az alap sablon az `archivum/sablonok/1_PaRDeS_alap_sablon.md` helyre kerül (`git mv`), változatlan szöveggel. Fölé ARCHÍV
     fejléc kerül: dátum, DT-F37-1, #74, és hogy a tartalma a Tanulmány sablon v22-ben él. Ez a DT84 (12) a. mintája.
   - A rá mutató élő hivatkozások ugyanabban a commitban frissülnek (CLAUDE.md „Git”, E27): a `sablonok/PaRDeS_gyorsreferencia.md`
     39. sora (az alap sablon sora: „archívumban, tartalma a Tanulmány sablonban”), és minden olyan brief `olvas` mezője, amelyben az
     út szerepel. A lezárt briefek fejlécét az E27 dönti el; ha jelez, az út az archív helyre áll át. A `naplok/` történeti szövegei
     változatlanok. A `sablonok/Javasolt_sablon_kiegeszites_BDB_arnyalat.md` 59. sora elavultságot állít, utat nem nevez meg, ezért
     változatlan marad.

**Nincs benne:** tartalmi javítás bármely tanulmányban (#75). Ugyancsak nincs benne az E13 (206) és az E12 (195) régi találatainak
egyben javítása: a D8 szerint a megérintett sorokon a tartalmi menet rendezi őket. Kivétel a 3. lépés 5. pontja. Nincs benne a
`genezis/1Moz_16_bovitett.md` nullázatlan Strong-értéke sem (N-F62c, külön tétel). Végül nincs benne a `sablonok/4_`, `5_`, `9_`
és a tanítói lista: az alap sablonra útvonallal nem hivatkoznak (`grep`, 2026-10-19). Végül a `GitHub_feltoltesi_workflow.md`
könyvtárfája (14. sor) sincs benne: leírás, az E27 nem követi, és a fájlt a #112 olvassa. Ha a #74 írná, a #112 a #74-től
függne. A fa a zárójelentésben utófeladatként áll.

## 3. Lépések

1. **Modell-ellenőrzés** (CLAUDE.md). Ágellenőrzés: van-e már a #74-nek ága vagy worktree-je. A Tanulmány sablon fejléce v21
   (a PR #420 a main-en)? Ha nem: megállás, „Te:” jelzéssel.
2. **M0 — mérés.** `python eszkozok/ellenorzes/tanulmany_audit.py --kimenet <ideiglenes, a repón kívül>`: a mai E8-szám
   fájlonként. Ezután soronként minden előfordulás (nem csak az első) egy csere-táblába kerül:
   `naplok/TANULMANY_JAVITAS_GEPI_csere.tsv`, oszlopok: fájl, sor, régi alak, új alak, besorolás (`proza`/`kulcs`). Ha a szám
   eltér a 32-től, az eltérés és oka a naplóba kerül (`naplok/TANULMANY_JAVITAS_GEPI_naplo.md`). Ez nem ⛔, ha minden új
   találat ugyanabba a két mintába esik.
3. **E8-csere** (`eszkozok/f74_e8_csere.py`, a CLAUDE.md shell- és TSV-szabályai szerint, fájlból futtatva, UTF-8 wrapperrel):
   1. A szkript a csere-táblából dolgozik, nem szabad regexből. A cél nem TSV, de a mintát az `eszkozok/igazolas_migracio.py`
      adja: írás előtt összeveti a fájlt az eredetivel. A csere-táblán kívüli sorok bájtra azonosak, a táblás sorokon pedig a
      régi alak → új alak csere az egyetlen különbség. Eltérésnél megáll, és nem ír.
   2. ⛔ Ha egy hely besorolása nem egyértelmű (`proza` vagy `kulcs`), vagy a csere a mondat állítását változtatná meg: a
      végrehajtó a helyet a naplóba írja javasolt alakkal, `DT-F74a` tételt vesz fel a `DONTESEK.md`-be, és megáll. A névelő és a
      toldalék igazítása az új alakhoz (pl. „a Gen.2.25-nél” → „az 1Móz 2:25-nél”) formai ügy, nem ⛔; a táblában jelölve áll.
   3. Commit (`F74.1: …`).
4. **Az alap sablon kivezetése** (2. pont), külön commitban (`F74.2: …`). ⛔ ha az összevetés az alap sablonban olyan normatív
   szabályt talál, amely a Tanulmány sablonból hiányzik (1. bekezdés): `DT-F74b`, megállás.
5. **Ellenőrzés:**
   - `tanulmany_audit.py`: E8 = 0 mind a 23 tanulmányban; a többi szabály száma nem nő.
   - `python eszkozok/ellenorzes/futtat.py --valtozott <a módosított fájlok> --diff-alap origin/main --diff-fej HEAD` (D8):
     HIBA-szintű találat nincs. Ha egy megérintett soron az E13 jelez (héber/görög szó kiejtés nélkül), a sor kiejtést kap a
     tanulmány saját átírásából, ha ugyanaz a szó a fájlban máshol kiejtéssel áll. Ha nem áll, ⛔, mert a kiejtés megválasztása
     nem gépi.
   - `git diff --word-diff` összesítés a naplóba: a csere-táblán kívül 0 eltérés.
   - `python eszkozok/feladatok.py ellenoriz` és az E27 (hivatkozás-ellenőrzés): 0 hiba.
6. **Független ellenőrzés:** `fuggetlen-ellenor` a base..head diffen → `naplok/ELLENOR_F74.md`. ELTÉRÉS esetén `/elteres`.
7. **Zárás:** zárójelentés (`naplok/TANULMANY_JAVITAS_GEPI_zaras.md`); a brief fejléce `allapot: lezarva`, `pr`,
   `lezarva_osszegzes`. Push a saját ágra, egy PR; merge csak a felhasználótól.

## 4. Elfogadási feltételek

- E8 = 0 a 23 tanulmányban (`tanulmany_audit.py`, proveniencia-sorral a naplóban). A STEPBible-alak csak backtick-ben, `kulcs`
  besorolással maradhat.
- A tanulmányok tartalma a csere-tábla sorain kívül bájtra azonos (a szkript összevetése és a `git diff` igazolja); a táblás
  sorokon csak a versformátum változott. Ha az 5. lépés szerinti kiejtés-kiegészítés is történt, az a táblában külön jelölve áll.
- A `sablonok/2_PaRDeS_bovitett_sablon.md` (v22) nem tartalmazza az „alap sablon” hivatkozást (kivéve a történeti verziósorokat).
  A `sablonok/1_PaRDeS_alap_sablon.md` nincs a `sablonok/` alatt; az `archivum/sablonok/` alatt ARCHÍV fejléccel áll, a szövege
  változatlan.
- Élő hivatkozás a régi útra nincs (E27 zöld); `feladatok.py ellenoriz`: 0 hiba.

## 5. Döntésnapló

- Brief írásakor (2026-10-19), a forrásjavaslat pontosítása: a STEPBible-alakú *sorkulcs* nem cserélődik, hanem backtick-be
  kerül. A szabály kommentje (`szabalyok.py` 499–501.) és a CLAUDE.md „Igehely-formátum” pontja ezt az alakot adatformátumként
  legitimnek tartja. A cseréje a mondat állítását („a … tsv Gen.3.7-es sora”) hamisítaná.
- Brief írásakor: `fugg` a #11 (a PR #420 a Tanulmány sablont v21-re írja; ugyanaz a fájl), `nem_fugg` a #75 (a #75 függ a
  #74-től, nem fordítva).
- (helyőrző a futáskor: DT-F74a — E8-besorolás vagy ragozás tartalmi kérdése, 3. lépés; DT-F74b — az alap sablon nem hivatkozott
  normatív szabálya, 4. lépés)
