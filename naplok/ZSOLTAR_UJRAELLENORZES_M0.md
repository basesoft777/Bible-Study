# ZSOLTAR_UJRAELLENORZES — M0 felmérés

*Brief: `F55_ZSOLTAR_UJRAELLENORZES_BRIEF.md` · ág: `claude/f55-zsoltar` · 2026-10-19 · modell: `claude-opus-5-5` (kért: opus, egyezik). Csak olvas. A mérés `manual` (keresőszkript és összevetés), kivéve az `lxx-hid` futásokat, ezeknek saját proveniencia-soruk van (`naplok/ZSOLTAR_UJRAELLENORZES_helyek.tsv`).*

## 1. A befagyasztás feloldása

A DT74 (3) feltétele, a #11 1. lépcsője teljesült: a PR #417 2026-10-19-én bekerült a main-be. A feloldást a felhasználó 2026-10-19-én jóváhagyta (F55.0). A #54 lezárva (PR #276), tehát az ítélet a javított `LXX_OS`-en áll.

## 2. Keresés (K1)

- **Szkript:** `python naplok/ZSOLTAR_UJRAELLENORZES_M0_kereses.py`. A régi `LXX_kivonat_Zsoltarok.tsv`-t a git-történetből olvassa (`0c2d1b44^`, az F42.12 törlés előtt). Az összevetés az `eszkozok/lxx_osszevetes.py` kategóriáit és függvényeit használja.
- **Minta:** `(Zsolt(ár)?|Psalm|Ps) N[:,.]v`, tartományokkal (`–`), vesszős versfolytatással és `/`, `;` vagy `,` utáni `N:v` folytatással. „Görög kontextus”: görög betű, `G####`, vagy `LXX`, `Septuaginta`, `görög` ugyanabban a sorban.
- **Fájlkör és találatszám:**

| Réteg | Fájlkör | Fájl | Zsoltárhiv. | Görög kontextusban |
|---|---|---|---|---|
| forrás | `tematikus_lezart/**`, `genezis/**`, `ujszovetseg/**`, `melyelemzesek/**`, `motivumok/**`, `motivumlog/*.md` | 58 | 499 | 77 |
| archív | `archivum/ISTENTISZT-001/*.md` | 4 | 161 | 55 |
| adat | `adat/jeloltek.tsv`, `auditok.tsv`, `elofordulasok.tsv`, `lxx_dontesek.tsv`, `kapcsolatok.tsv` | 5 | 204 | 39 |
| csak számolva | `lexikon/*.md`, `generalt_proba/**`, `motivumlog/lexikon_pilot/**` | 75 | 2 807 | 458 |

`motivumlog/[ID].md` alakú fájl ma nincs. A `motivumlog/*.md` (pl. `PaRDeS_motivumok.md`, `Olvasoi_szint_pilot_ISTENTISZT-001.md`) a forrás-körben szerepel. A nyers találatlista: `naplok/ZSOLTAR_UJRAELLENORZES_M0_talalatok.tsv` (864 sor, a generált és próba-fájlok nélkül).

## 3. Szűrés: az eltéréslista a #54 után (M0.2)

A régi kivonat és a mai `LXX_OS` újra-összevetése (Zsoltárok) a #54 után:

| | `zsoltar_eltolas` | `csak_regi_vers` | `nagy_eltero` | `strong_eltero` | `csak_uj_vers` | azonos |
|---|---|---|---|---|---|---|
| F42 (2026-10-05) | 739 | 66 | 424 | 686 | 67 | (nem listázott) |
| ma | **745** | **0** | 488 | 684 | 69 | 540 |

72 vers kategóriája változott. 63 `csak_regi_vers` most `nagy_eltero`, mert a #54 kulcsolta a feliratokat. 6 vers újonnan `zsoltar_eltolas`: Zsolt 13:2–5 (a #54 Zsolt 13-javítása), 89:1, 108:1. Szűrő: a vers az F42-listán **vagy** a mai összevetésben `zsoltar_eltolas`/`csak_regi_vers`. A 6 új vers egyetlen kézi forrásban sem fordul elő görög kontextusban.

Szűrt hely (görög kontextus és érintett kategória): **152**. Ebből 120 generált vagy próba-példány, **32 forrás-, adat- vagy archív sor**. Az archívumban 0. A 32 sor (és a brief előfelmérésének két kontrollsora) 15 hely-csoportban: `naplok/ZSOLTAR_UJRAELLENORZES_helyek.tsv`.

## 4. Hatás (M0.3–4)

**Érintett, vagyis a régi kivonatsoron álló állítás (5 hely, két motívum):**

- **HAMART-001, régi forrásréteg (3).** `Bun_…_kereszthivatkozas_naplo.md` 88. sor (3/c tábla: „Zsolt 53:1 (LXX-számozás) διεφθάρησαν G1311”) és 272. sor (11. lépés: „Zsolt 14:1, 53:1 — `LXX_kivonat_Zsoltarok.tsv`”). Ehhez jön a `Bun_…_tematikus.md` 281. sora („LXX-egyeztetés … Zsolt 14:1; 53:2 … `LXX_kivonat_Zsoltarok.tsv`”). A görög alak és a Strong-szám a helyes versen is ugyanaz: Károli Zsolt 53:2 = LXX 52:2, διεφθάρησαν G1311. A hiba a versazonosításban (53:1, „LXX-számozás”) és a forrás-megnevezésben van. Várható ítélet: két módosul, egy megáll. A lelet (Z08, H7843 Hif'íl) héber, nem érintett.
- **TEREMT-002, adatréteg (2).** `adat/auditok.tsv` 160. és 163. sor (B4, Zsolt 80:6 és 80:7, `forras=LXX_kivonat_Zsoltarok.tsv`): mindkét sor a következő vers görögjét naplózta. Ezek a meglévő sorok nem írhatók át. M2: új `lxx-hid` sor. A jelölt elutasítása (`jeloltek.tsv` 327) héber kritériumon áll, ezért nem változik.

**Nem érintett (10 csoport):** a döntést héber kritérium vagy más adat hordozza, vagy csak hivatkozásról van szó. Ide tartozik a TEREMT-001 (Zsolt 36:7, 42:8, 77:17: H8415 TAHOT-scan; a helyes LXX ἄβυσσος G0012-t ad, de a forrás erről nem állít semmit, és ez nem pótlandó), a KIRALY-001 és a HODIT-001 (LD079, LD063 már `LXX_OS`-en), az ISTENTISZT-001 jelölt Zsolt 89:21 (Z06, várhatóan megáll) és a pilot Thayer-hivatkozásai (Z15).

**Az ISTENTISZT-001 állításainak mai helye:**

| Réteg | Hol | Zsoltár-LXX-állítás | Érintett? |
|---|---|---|---|
| migrált forrás | `motivumok/ISTENTISZT-001.md` 192–200. sor („a 22 ÓSZ-igehely közül 18-ban ἐπικαλέομαι”; Zsolt 116:17 tagmondat-hiány) | Zsolt 116:4, 116:13, 116:17, 105:1, 79:6 | nem: egyik vers sem `zsoltar_eltolas`/`csak_regi_vers` (116:17 azonos, 79:6 `nagy_eltero`, a többi `strong_eltero`) |
| adat | `elofordulasok.tsv` (5 zsoltársor), `lxx_dontesek.tsv` LD004 (Zsolt 116:17, `LXX_OS`), `jeloltek.tsv` 556 (Zsolt 89:21) | a fenti, valamint 89:21 | csak a 89:21 eltolt; a kritérium héber (Z06) |
| archív | `archivum/ISTENTISZT-001/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` 85–100. sor (15/17-számítás, a Zsolt 116:4 G4506→G1941 javítás a régi kivonatban) | Zsolt 116:4, 116:17 | nem szűrt; az archív fájl nem szerkeszthető |

A régi `tematikus_lezart/Segitsegul_hivni_az_Urat_*.md` két fájl már nem létezik. A brief `ir` mezőjének két Segitsegul-útja ezért holt.

**A többi motívum** (HAMART-001, TEREMT-002 stb.) a 2. lépcsőig a régi rétegben marad. Az érintett HAMART-001-állítások javítása tehát a `tematikus_lezart/`-ban történik, formai javításként (DT247 (1.) mintájára: a 2. lépcső bájtra viszi tovább). A `motivumok/HAMART-001.md` nem érintett (Z07).

## 5. ⛔ Nyitott kérdések (a döntés a szülő sessioné / a felhasználóé)

**(a) Hatókör és `ir`.** Javaslat: `ir: [adat/auditok.tsv, tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md, tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md, naplok/ZSOLTAR_UJRAELLENORZES_*]`. A két Segitsegul-út kikerül. Ok: a fájlok archiválva vannak, és az ISTENTISZT-001-nél nincs érintett állítás. A `motivumok/ISTENTISZT-001.md` nem kerül be.
- Opciók: 1. a javaslat · 2. a Segitsegul-utak cseréje a `motivumok/ISTENTISZT-001.md`-re (szükségtelen, és ütközne a #11 PR #420-szal) · 3. az `ir` változatlan (holt utak maradnak; a CI E27 hivatkozás-ellenőrzése jelezheti).

**(b) A javítás formája a kézi forrásban.** Javaslat: csere `【NAPLO: … javítva, F55】` jelöléssel (a brief javaslata). A Z01 táblasor helyesen: „Zsolt 53:2 (LXX 52:2) | διεφθάρησαν | G1311”. A Z02 és a Z03 forrás-megnevezése `LXX_OS/psalms-lxx.tsv` lesz, az új proveniencia-sorral. Alternatíva: csak jelölés a régi szöveg mellett.

**(c) Az `adat/auditok.tsv` írásának ideje.** A #11 PR #420 is írja az `adat/auditok.tsv`-t. Opciók: 1. az M1 most fut, az M2 audit-sorai a PR #420 merge-e után kerülnek be (javaslat, nincs ütközés) · 2. hozzáfűzés most (merge-ütközés lehet, bár csak hozzáfűzés) · 3. a futások a `--naplo F55` útján a `naplok/F55_lekerdezesek.tsv`-be kerülnek, az `auditok.tsv` érintetlen (eltér a brieftől). Az új sorok: `lxx-hid "Zsolt 80:6"`/`"Zsolt 80:7"` `--naplo TEREMT-002 --lepes B4`, valamint `"Zsolt 53:2"` és `"Zsolt 14:1"` `--naplo HAMART-001 --lepes adhoc` (a lépéskódot az M1 pontosítja).

**(d) A hatókörön kívül, csak jelölve:**
- A `Konnyu_ellenorzes_4_lezart_tanulmany.md` (28–29., 47–48., 197., 228., 321. sor) a Zsolt 42:8-at és 88:11-et „NEM ELLENŐRIZHETŐ — KONKORDANCIA-RÉS” jelöléssel viszi. Ez a régi TAHOT-hiányra utal, nem LXX-állítás. A TAHOT ma fejezetszinten teljes (F85), tehát az állítás elavult. Lehetséges új feladat a `/befogad` útján.
- A szülő session háttér-szövege a „TAHOT F85 előtti kulcsairól” beszél. A brief tárgya viszont a régi **LXX**-kivonat. Az F85 átkulcsolása a Zsoltárok Károli–Strong táblapárját nem változtatta (`naplok/F85_jelentes.md` 192. sor: a régi és az új pipeline a Zsoltárokra azonos). Egyetlen `bizonytalan` zsoltársor maradt: Zsolt 77:11 (39. sor). TAHOT-irányú bővítést ezért nem javaslok.
- A generált oldalak (`lexikon/HAMART-001_*`) LXX-táblasora (Zsolt 53:2 / LXX 52:2, `LXX_OS`) már a helyes adatot mutatja. A `modszertan` rés másolata (TUDOMANYOS 1144., TORZSCIKK 1059. sor) viszont jelölés nélkül nevezi meg a régi kivonatot (l. a 7. pontot). A #36-ra várnak, a #55 nem írja őket. *(Pontosítva: ELLENOR 2. eltérés, F55.11.)*

## 6. A ⛔ döntései és az M1 (2026-10-19)

**Döntés** (orkesztrátor, a felhasználó felhatalmazásával): DT255 (az `ir`-ből kikerül a két Segitsegul-út), DT256 (csere `【NAPLO: … javítva, F55】` jelöléssel, a régi szám látható), DT257 (az M2 audit-sorai a PR #420 merge-e után). A `Konnyu_ellenorzes_4_…` elavult TAHOT-állításai: N-F55a (`NYITOTT_FELADATOK.md`).

**M1 ítéletek** (`naplok/ZSOLTAR_UJRAELLENORZES_helyek.tsv`, `itelet_M1` oszlop): **módosul 4** (Z01, Z02: javítva, F55.5; Z04, Z05: audit-nyom, az új sor az M2-ben), **megáll 2** (Z03: jelölve, F55.5; Z06: nem írva), **visszavonandó 0**, nem érintett 9 csoport. Minősítés-, jelölt- vagy ★-változás nincs, `DONTESEK.md`-tétel ezért nem kell.

**Hátra (az F55.9 előtti állapot; az M2 azóta kész, l. a 7. pontot):** az M2 (az `adat/auditok.tsv` új `lxx-hid` sorai: Zsolt 80:6, 80:7 `--naplo TEREMT-002 --lepes B4`; Zsolt 14:1, 53:2 `--naplo HAMART-001`) a PR #420 merge-e után; utána az M3.

*F55.8 (2026-10-19): a Bun-tanulmány F55-jelölése a `modszertan` rés elé került (a 6. pont címe alá), mert a résen belül az E1 11. szabálya (rés-forrás egyezés) a #36 újragenerálásáig bukott. A tartalom változatlan.*

## 7. Az M2 és a független ellenőrzés (2026-10-19)

- **M2 (F55.9):** két új `lxx-hid` audit-sor (`TEREMT-002 B4`, Zsolt 80:6 n=11, 80:7 n=13, `LXX_OS`), a PR #420 merge-e után; a 225 meglévő sor bájtra azonos. A HAMART-001 futásai nem kerültek a táblába: a motívumnak nincs auditsora, és a SEMA 2.9 commit-szabálya (DT103) szerint egy motívum auditsorai csak a teljes lefedés után commitolandók *(indok pontosítva, l. a 8. pontot)*. Ez eltér a DT257 szövegétől; eldöntve: DT258 (a tényindokot l. a 8. pontban).
- **Független ellenőrzés:** `naplok/ELLENOR_ZSOLTAR_UJRAELLENORZES.md`, ELTÉRÉS 6. Mechanikusan javítva (F55.11): 4. (N-F55a: Jóel 3:5/2:32), 5. (fejléc, „Hátra”), 6. (Z03 sorszám 281 → 283), és a 2. tételből az 5(d) állítás pontosítása. Tartalmi (azóta eldöntve: DT258–f, F55.12): 1. (HAMART-001 audit-sorok vs. DT103), 2. (a jelölés a rés előtt, ezért a #36 renderébe nem kerül át), 3. (Z02/Z03 forrás-megnevezése: történeti név + jelölés, nem csere).

## 8. A 2. ellenőrzési kör (2026-10-19)

`naplok/ELLENOR_ZSOLTAR_UJRAELLENORZES_2.md`: az 1. kör 6 eltéréséből 4–6. javítva, 1–3. döntéssel lezárva; új ELTÉRÉS 3. Javítva (F55.14): 2. (a brief `kovetkezo` mezője, döntésnaplója és ez az állapotjelölés), 3. (N-F55a: „három tétel”, a 46. sor).

**Tartalmi (1.), eldöntve: (a), F55.15:** a DT258 tényindoka („a részleges első auditsor a DT103 / `ellenoriz.py` 8. szabálya szerint SÉRTÉST ad”) a kód szerint nem áll: a HAMART-001 a `RETROAKTIV_IDK` tagja (`eszkozok/ellenoriz.py` 65–68.), a hiányzó datasetje KÉZI jelentést kap, nem SÉRTÉST (311–312. sor; a végrehajtó session saját olvasással megerősítette). A SEMA 2.9 commit-szabálya („egy motívum auditsorai csak a teljes lefedés után commitolandók”, DT103) ettől függetlenül áll. Opciók: (a) a döntés marad, az indok a SEMA 2.9 commit-szabályára javul (javaslat: a szabály szövege nem tesz kivételt a retroaktív ID-kre); (b) a két HAMART-001 sor most bekerül (`--naplo HAMART-001 --lepes B4`), CI-hiba nélkül, de a DT103 commit-szabályával szemben; az N-F55b lezárul.
