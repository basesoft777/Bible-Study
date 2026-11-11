ELTÉRÉS: 11 tétel

# ELLENOR_F182 — F182_HAMART_JAVITO_BRIEF.md · `4a11b4a1..6a97d83c`

*Base: `git merge-base origin/main HEAD` = `4a11b4a1`; head: `6a97d83c`. Saját commitok: `git log --no-merges --first-parent 4a11b4a1..HEAD` → 46 db (F182.0–F182.45). Diff: `git diff origin/main...HEAD` (76 fájl, +7439/−1713). Ellenőr: claude-opus-5-5 (`fuggetlen-ellenor`). Eltérés a szereptől: a megengedett parancsokon kívül néhány csak olvasó parancsot futtatott (`git show`, `head`, és a `git diff` kimenetén `grep`/`awk`/`sort` szűrőket). A CI kimenetét a scratchpadbe irányította. Fájlt nem módosított. A jelentést a fő szál (orkesztráló session, claude-opus-5-5) írta ki az ellenőr válaszából szó szerint, mert az ellenőrnek nincs fájlíró eszköze.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | Tényleges: claude-opus-5-5; kért (subagent `model`): opus. A 46 commit mindegyikén `Co-Authored-By: Claude Opus 5.5`. A modell-mezők: `elofordulasok` „claude-opus-5-5”; `forditasok` +70 sor „claude-sonnet-5-5”. A subagent tényleges modellje innen NEM ELLENŐRIZHETŐ. |
| H0–H1, K1–K6 | OK | `dontesek/uj/hamart-javito.md:1-4` | K2: `lekerdez.py kollokacio H2555 H4390` → 8 vers; `… H2555 H8085` → 4; `… H2555 H4393` → 1 (Ez 12:19); `scan H2555` → n=59. 13 bent, 46 kint: egyezik. K6: `scan G1093 --szakasz "Zsid 6:7-8"` → Zsid 6:7; `scan G2937 --szakasz "Róm 8:20-21"` → 8:20, 8:21. K1/K4: `elofordulasok` −1 sor (1Móz 4:2-3), 5 sor proveniencia DT747. |
| H2 / F16 kapcsolatok | OK (számok) | `adat/kapcsolatok.tsv` | `git diff … adat/kapcsolatok.tsv`: +56/−0. Párhuzam 43, Kontraszt 7, Variáns 6; magas 26, közepes 30; mind Remez. A jelöltnapló: 103 sor, ebből 56 beépítve. Szúrópróba: `lekerdez.py tsk "1Móz 4:11"` → 1Móz 3,14 Votes=3; `tsk "1Móz 3:16"` → 1Móz 4,7 Votes=10; `tsk "1Móz 3:17"` → 1Móz 5,29 Votes=12. Mind egyezik a sorok indoklásával. |
| H2 / 6. szabály (jeloltek-út) | **ELTÉRÉS #10** | `adat/kapcsolatok.tsv` (proveniencia `forras=naplok/F182_kapcsolat_jeloltek.tsv`) | A brief F16-ja kéri: „a jelöltek útján (CLAUDE.md 2. szabály)”. A 103 kapcsolat-jelölt nem az `adat/jeloltek.tsv`-n ment át, hanem a `naplok/` alatti jelöltnaplón. Dokumentált (N153), de nincs döntés. |
| H3 / hatókör | OK (egyeztetett) | `naplok/F182_jelentes.md:129,210` | F1, F3–F21, H4 (b), H5 és N-F178a/b a befagyasztás miatt elhalasztva, kimondva. |
| H4 (a) MUNKASZO | OK | `eszkozok/olvasoi_kapu.py:484-500` | Grep a lap látható soraira: próba/javaslat/ellenőrzendő/függőben/nincs bekötve/kutatói jelölés/azonosításra vár/gerinc/orkesztrátor/felhasználó → 0. |
| H6 | ez a jelentés | — | — |
| A02 | OK | `lexikon/HAMART-001_TUDOMANYOS.md:5-15` | Az azonosító tábla a lap elején, „Rövid cím”, Státusz: „nincs kiadva — feldolgozás alatt”. |
| A03 | OK | `…TUDOMANYOS.md:229` | „47 helyből 23”, „Az Újszövetségben 6 hely”. Grep `^HAMART-001\t1Móz ` → 23; ÚSZ-könyvek → 6; összesen 47. |
| A04 | OK | `…:1271,1285` | חַטָּאת (chattát). |
| A05 / A06 / B08 | **ELTÉRÉS #8** | `…:744-753, 775-776, 788-790, 888, 890, 987-988` (és a Minősítés ismétlése: 3000-3009, 3034-3035, 3049-3051) | Az indoklásban írás áll kiejtés nélkül: (חוֹחַ, בָּאְשָׁה), (ἄκανθα + τρίβολος), (לִפְנֵי), (קֵץ); a CI E13 ezt 79 JELENTÉS-sel jelzi. Más sorra hivatkozik: „az Ez 28:16 / Mik 6:12 / Róm 8:21 **sorának** folytatása” (4 sor). Munkajavaslat áll a szövegben: „önálló motívum-jelöltként érdemes lehet külön vizsgálatra” (3 sor). Az A05/A06 „teljesül” jelölése így nem áll. |
| A07 | OK, dokumentált kivétellel | `…:123,131` | „1.1. Mit keresünk”, „1.2. Hol kerestünk”: N155 nyitott döntési pont. Grep `-tunk/-ünk/-juk…` a látható szövegben → csak ez a két cím és Károli-idézetek. |
| A08 | **ELTÉRÉS #5** | `…:1247-1261` | 15 lábjegyzetben (k256–k270): „…kereszthivatkozás-naplójában **(7. rész)**, utólagos betöltés”. A `NYERS_JEL` regexe (`olvasoi_kapu.py:512`) csak a `\(\d+/[a-z]\. rész\)` alakot fogja, a teszt (`teszt_kesz_lap_hamart.py:77`) csak a „(4/b. rész)” és a „(4/c. rész)” alakot. |
| A09 / A26 | **ELTÉRÉS #7** | `…:92` | „4.6 **lXX**-híd”, „4.13 **károli**-megfelelők”: kisbetűsítési hiba a látható Jelmagyarázatban. |
| A10–A12 | OK | `…:1304-1318, 2181-2203` | A 4.4 doménnevei egyeznek a forrással: `lekerdez.py domen H2555` → Ferocious/Wrong/Unsafe/Objects/Impact = Vad, kegyetlen; Helytelenség; Veszély; Tárgyak; Ütközés. A `forditasok` új sorai: SDBH 31, SDGNT 11, tW 25, TBESG 3. |
| A13 / A16 / A20 | OK (mintavétel) | `…:2699` | 7 + 27 + 12 = 46 vers; az összesítő sor 7/27/11 + 1 (szamozas_elteres) = 46. |
| A15 | OK | `…:2402-2449, 2518` | A rokon nyelvi tábla a 4.8-ban, a 4.11-ből hivatkozás. |
| A17 | OK („részben”, nyíltan) | N147 | — |
| A18 / 5. pont: BDB-pontosság | OK | — | Grep `94[,.]0|99[,.]4|pontosság` a lapon → 0. Az `olvaso_szerver/blokkok.py:1476`: a BDB-dobozban nem áll; a `_pontossag_html` sehol nincs meghívva (csak teszt hívja). A 99,4 sehol nem fordul elő. |
| A19 | **ELTÉRÉS #4** | `…:2707` vs `…:2510` | Az 5. szakasz 1Móz 3:17 sorában a héber kulcsszó הָֽאֲדָמָה (háadámá), a görög megfelelő ἐπικατάρατος, a jelölés „egyező”. `lekerdez.py lxx-hid "1Móz 3:17"` → G1944 ἐπικατάρατος és G1093 γῆ; a 4.11 szerint az adámá párja γῆ. Rossz párosítás, a main-en is így volt; a lapon látható, és a 7 „egyező” egyike. |
| A21 / B04 | OK | `adat/res_forras.tsv` (−1), `archivum/HAMART-001/HAMART-001_alkalmazas_regi.md:1` | Az Alkalmazás nincs a lapon; ARCHÍV fejléc; a Kolofon szerzőségi mondata (`…:3541`) a mai szakasznevekkel. |
| A22 | OK (mintavétel) | — | — |
| A23 / B14 | OK | `lexikon/HAMART-001_KIZARASOK.md:5-7` | 887 + 577 + 41 + 1 = 1 506; a 25 egyedi ok összege 236; 1 742 + 54 = 1 796. A lap `:682` sora szerint 1 612 + 99 + 31 = 1 742. |
| A24 / 3. pont (4.13) | OK a számokra; **ELTÉRÉS #9** az olvasói egyezésre | `…:2553, 2557-2583` | Az `elofordulasok.tsv`-ben H2555-ös HAMART-sor 12, H0127-es 10. A karoli_szo mezők szerint 9 „erőszak”-családú szó (Ez 7:23, 8:17, 28:16, 1Móz 6:13, Sof 1:9, Ézs 60:18, Jer 6:7, 51:46, Hab 1:2). A 47 hely és a 27 szótári alak egyezik. Viszont a próza szerint „12 helyéből 9 helyen „erőszak”, a lista szerint „**erőszak** (2)”; az „**megroml**” nem szó (részben N149). |
| A24 / 3. pont (4.14) | **ELTÉRÉS #3** | `…:2589, 2619-2652`; `eszkozok/szerep_karoli.py:339-344` | A `sajat = {s['igehely'] …}` a tartomány-kulcsot („Gal 3:13-14”) nem bontja versekre. Emiatt 6 motívumvers a „motívumon kívüli” hamis párhuzamok közé került: Ézs 24:5, 24:6, Hós 4:1, 4:3, Gal 3:13, Zsid 6:7. `lekerdez.py karoli` mind a hatnál „föld” vagy „Átkozott” szót ad. A 2 318 / 2 331 / „99% nem a motívumhoz tartozik” állítás ezért hibás. A rejtett párhuzam (1Móz 12:3) és a „nem mérhető” korlát rendben, asszociatív kitöltés nincs. |
| A25 | OK | `…:1297` | — |
| B07–B10, B13, B15 | OK (a végrehajtás nyoma) | `sablonok/*`, `…:3563-3595` | A Kolofon forrásonként egy sor, „Fájl” oszlop nélkül. |
| 4. pont: nyers jel, napló-utalás | **ELTÉRÉS #6** | `…:1148, 1263, 3430` („csatorna=cli”); `:2743, 2752` („szamozas_elteres”); `:2943` („(forras_kereses: …)”) | A látható szövegben nyers mezőnevek, ill. -értékek állnak. A `NYERS_JELEK` lista (`olvasoi_kapu.py:505-521`) egyiket sem fogja. |
| 4. pont: `<!-- eredeti -->` a nyílt magban | OK | `nyilt_mag/` | Grep `eredeti:|csatorna=|\(\d+\. rész\)|§` a `nyilt_mag/` alatt → 0. A `KIZARASOK.md` látható szövegében a tiltott szavakra 0 találat. |
| 4. pont: elavult DT | OK | — | A lapon DT199, DT564, DT683, DT685–687 áll; a DT-F182 helyőrző csak HTML-megjegyzésben. |
| 1. pont: régi lapok | OK | `lexikon/` | `git diff --stat origin/main...HEAD -- lexikon/`: csak a `HAMART-001_TUDOMANYOS.md` és a `HAMART-001_KIZARASOK.md` változott; a 8 régi TUDOMANYOS és a 4 TORZSCIKK változatlan. Az E28 a négy régi migrált lapra (ISTENTISZT, ALVIL, TEREMT-002, ANTROP) nem jelez. |
| 6. pont: `csv` | OK | — | `git diff … '*.py' | grep 'import csv|csv.reader…'` → 0. |
| 6. pont: végleges DT/N az ágon | OK | `dontesek/uj/`, `nyitott/uj/` | Csak DT744–o és N153–j. A `DONTESEK.md`-ben csak a fej „Állapot” sora módosult (meglévő sor). |
| 6. pont: DT28 | OK (mintavétel) | `motivumok/HAMART-001.md` | Szkript nem írt adatot a forrásba. A forrásprózát kézzel javították, az adatsorokat (`elofordulasok`, `jeloltek`) szkript írta. |
| 6. pont: dokumentációs következetesség | **ELTÉRÉS #11** | `dontesek/uj/hamart-javito.md:13`; `adat/SEMA.md` (2.12); `nyitott/uj/hamart-javito.md:4` | A DT756 szerint a SEMA 2.12 „a felhasználó jóváhagyásával igazítandó”, mégis módosult (F182.38). A DT753 szerint az N154 „lezárható”, mégis nyitottként áll. |
| 7. pont: kapuk | NEM ELLENŐRIZHETŐ (futtatás) | `eszkozok/teszt_kesz_lap_hamart.py:204-225` | A tesztek kódja szerint a NYERS_JEL, MI_HANG, NEVELO és KOV_ISM kapunak van rontott mintás tesztje; a MUNKASZO-é `teszt_olvasoi_kapu.py`-ban, a LYUK-é `teszt_nyilt_mag.py`-ban, a 42. szabályé `teszt_forditas_vedelem.py:48`-ban van. A 43. szabálynak nincs rontott mintás tesztje (JELENTÉS-szint). A 4–6. ELTÉRÉS szerint a NYERS_JEL nem fog minden belső jelet. |
| 8. pont: `ellenoriz.py`, `teszt_futtat.py --gyors` | NEM ELLENŐRIZHETŐ | — | A szerepben nem futtatható parancsok. |
| 3. CI-jelentés | **ELTÉRÉS #1, #2** | lent | `python eszkozok/ellenorzes/futtat.py --valtozott <git diff --name-only origin/main...HEAD> --diff-alap 4a11b4a1 --diff-fej 6a97d83c --minta 12` → exit=1. **E28 HIBA 4** (#1); **E5 HIBA 2** (#2); **E16 HIBA 1**: az `ellenoriz.py`-t érintő PR címe „[ELLENŐRZŐ]” előtagot kér; helyben üres PR-címmel fut, ezért NEM ELLENŐRIZHETŐ. JELENTÉS-szint: E12 499, E13 79, E27 43, E30 9 ékezet nélküli commit-szó, E32 13 (régi helyőrzők az `emeles.py`-ban), E34 41, E36 1. A végrehajtó jelentése a CI-t nem futtatta (`F182_jelentes.md:121, 201`), ezért ezt nem állította. |
| A1 (memória vs. lekérdezés) | OK (mintavétel) | `…:3446` | A vitatott pont prózája `scope=manual` provenienciájú, „ellenőrzött lekérdezés nélkül” jelöléssel. Az „első olvasat” mondatát a lekérdezés igazolja: `scan H0779 --szakasz "1Móz 9:1-50:26"` → 9:25, 12:3, 27:29, 49:7; n=4. |
| A2 (nyitott tételek) | OK, egy kivétellel (#11) | `nyitott/uj/hamart-javito.md` | N146: `lekerdez.py karoli "Péld 57:1"`, `"Jób 14:23"`, `"1Sám 3:26"` → „Nincs Károli-szöveg”, tehát valóban nyitott. N147, g és i a lap szerint is nyitott. |
| A3 | OK | `…:27, 198` | Négy „tematikus, nem lexikai” sor, címkézve. |
| A4 (Sod) | OK | `…:3436` | A Sod az alsóbb rétegekből levezethető. A 8:21 qalal: `scan H7043 --szakasz "1Móz 8:21"` → 1; `scan H0779 --szakasz "1Móz 8:21"` → 0. A Jel 22:3: `scan G2652 --szakasz "Jel 22:3"` → 1. Az áldás (12:3) a Remezben és a Drashban áll. |
| A5 | nem érintett | — | Nevesített tanító nincs. |
| A6 (E12–E15) | lásd #8 | — | Az E13 79 találata tartalmilag az A06/B08 sérülése; az E12 a megszokott jelentés, az E14 és az E15 0. |
| Lista 1: kiszűrt/törölt sorok | OK | — | `elofordulasok` −1 (K1: 1Móz 4:2-3); `res_forras` −1 (HAMART `alkalmazas`). `jeloltek` 80 módosított, mind HAMART-001 (4: K1/K5/K6, 5: K4, 71: A05/A06). `elutasitasi_okok` 2 minta. `forditasok` 1 módosított (G0086: N-F121c → N64). `bdb_vers_jelentes` 1 sor + fejléc (DT749). |
| Lista 2: kulcstartomány | OK | — | A motívum 15 Strongja mind a 4. szakaszban; `scan H6093` → 3 (mind a láncban); `scan H0127` → 211 (a lap szerint is 211); `scan H0779` → 52. |
| Lista 3: „nulla-diff” hatóköre | OK | — | A régi lapok bájtra változatlanok: a commitolt fájlokra és az E28 négy régi migrált lapjára igazolt. A 8 régi lap generátoros újrafuttatása NEM ELLENŐRIZHETŐ. |
| Lista 4: táblasor-Δ | OK (bontás van) | — | `adat/`: auditok **+154** (HAMART-001 A5 proveniencia; F182.2), forditasok **+70** (tW cím 25, SDBH 31, SDGNT 11, TBESG 3; F182.4, .34, .44), kapcsolatok **+56**, nyilt_angol +7, nyilt_kodkonyv +1, funkcio_kapcsolok +1, elofordulasok −1, res_forras −1, jeloltek 0, elutasitasi_okok 0, bdb_vers_jelentes 0. `konkordancia/`: nincs változás. |
| Lista 5: ⛔ pontok | nincs ilyen | `F182_HAMART_JAVITO_BRIEF.md` | A briefben nincs ⛔ pont. |

**ELTÉRÉS-ek súlyossági sorrendben** (m = mechanikus, t = tartalmi):
1. (m) **E28 HIBA**: a 47 sorra váltás után négy generált nézet régi maradt: `motivumlog/PaRDeS_motivumok.md:27` és `:494` (48 → 47, 251 → 250), `Lezart_tematikus_tanulmanyok_index.md:19`, `NYITOTT_FELADATOK.md:947` (251/537 → 250/538). A CI elbukik.
2. (m) **E5 HIBA**: a „## 10. Alkalmazás” cím és a `KESZ_LAP_KOVETELMENY.md` 66 sora jelölés nélkül törlődött. Egyik commit-üzenetben sincs „TÖRLÉS-SZÁNDÉKOS:”.
3. (m) **4.14**: 6 motívumvers áll a „motívumon kívüli” hamis párhuzamok között (tartomány-kulcs, `szerep_karoli.py:339`). Az A24 „teljesül” jelölése nem áll.
4. (m) **5. szakasz, 1Móz 3:17**: adámá ↔ ἐπικατάρατος „egyező”; ellentmond a 4.11-nek (main-ről örökölt, látható hiba).
5. (m) **„(7. rész)” napló-utalás** 15 lábjegyzetben; a kapu nem fogja.
6. (m) **Nyers jelek a látható szövegben**: csatorna=cli (3 sor), szamozas_elteres (2 sor), forras_kereses (1 sor).
7. (m) **Jelmagyarázat**: „lXX-híd”, „károli-megfelelők”.
8. (m) **Indoklások**: írás kiejtés nélkül, „sorának”-hivatkozás, munkajavaslat; ezért az A05/A06 „teljesül” jelölése nem áll.
9. (m) **4.13**: a próza szerint 9 hely „erőszak”, a listában „erőszak (2)”; a „megroml” nem szó (részben N149).
10. (t) **Kapcsolat-jelöltek** a `naplok/` alatt, nem a `jeloltek.tsv`-n (CLAUDE.md 2. szabály; N153 nyitott, döntés kell).
11. (t) **DT756 és SEMA 2.12**, illetve **DT753 és N154** dokumentációs ellentmondása.
