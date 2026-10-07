# Nyitott feladatok
Ez a fájl a projekt aktuális, karbantartott feladatlistája. Átadási dokumentum kérésekor frissítendő: a lezárt tételek áthelyezendők a "Lezárva" szakaszba (dátummal), az újonnan felmerülő tételek felveendők a megfelelő szakaszba.
Utolsó frissítés: 2026.10.05 (F53 utótétel — N-F53c, N-F53e, N-F53f a Lezárva szakaszba); előtte 2026.10.05 (F53 utótétel — N-F53a és N-F53b a Lezárva szakaszba); előtte 2026.10.05 (F53_FELADATTERKEP_BRIEF.md, FT.2 ⛔ válasz — N-F53a, N-F53b, N-F53c, N-F53d új; FT.4 — N-F53e új; FT.5 ⛔ — N-F53f új; ELLENOR_F53 — N-F53e, N-F53f kiegészítve); előtte 2026.10.04 (F43_LXX_BRIDGE_BRIEF.md, F43.8 — N29 a Lezárva szakaszba, D7: az ASV-t nem importáljuk); előtte 2026.10.03 (F46_BDB_KONYVFELOLDAS_BRIEF.md, F46.15 — N-F46a: 16 visszaállított sor, 779 sor; előtte F46.13 — N-F46a számozás eldöntve, N-F46b új; előtte F46.7 — N-F34 és N-F34c a Lezárva szakaszba, N-F46a új: a BDB könyvfeloldási kézi lista); előtte 2026.10.02 (F41_BSB_UJRAMERES_BRIEF.md, F41.15 — N-F41d/g/h az `ellenorizetlen` pontos jelentése és a Jób 40:1/3/6 szerint; N-F41e és N-F41f a Lezárva szakaszba; előtte F41.12 — N-F41b, N-F41d, N-F41g, N-F41h a szigorított versszintű `Számozás` szerint; előtte F41.10 — N-F41e, N-F41g, N-F41h a versszintű `Számozás` (mt/kjv/ellenorizetlen) szerint; előtte F41.7 — N-F41g, N-F41h új; N-F41e elvégezve; N-F41d, N-F41b pontosítva; előtte: N-F41a, N-F41b, N-F41d, N-F41e, N-F41f új, N-F41c felvéve és lezárva.)

Korábbi frissítés: 2026.09.29 (F05_SZOTAR_BRIEF.md v1.10, S1 javítókör (F05b) —
N39–N44 új: héber `s`/`ś` átírás, H2403 lemma-választás, `spirantize()`
geminációs hiba, `alap_strong` lemma-választási szabály (a `#9`
előfeltétele), CI E5-jelölés globális hatóköre, commit-fegyelem.)

Korábbi frissítés: 2026.09.28 (F05_SZOTAR_BRIEF.md v1.7, S1.5 — N38 felvéve és
lezárva ugyanabban a menetben: az `ellenoriz.py` 10. szabálya a megszűnt
`forditas_ubs.tsv`-t olvasta, HIBA-val állt le S1.1 óta; javítva, és a
13–14. szabály bevezetve, S1.5.)

Korábbi frissítés: 2026.09.28 (F05_SZOTAR_BRIEF.md v1.7, S1.4 — N35–N37 új: a
MCGED `y`-ág validálatlansága, a gold-készlet 12 csonkolt sora, nincs
egységes Strong-normalizáló függvény.)

Korábbi frissítés: 2026.09.28 (F05_SZOTAR_BRIEF.md v1.4, D30 — N32, N33 új: a
commitolt render-kimenet elavultsága és a CI generátor-lefedettsége.)

Korábbi frissítés: 2026.09.23 (RENDER_BRIEF.md v5, 2. menet — R2.1–R2.7: a rések tartalommal, kivonatok, `forras=lap` megszűnt, diff-osztályozó — RENDER lezárva. **Következő: `F05_SZOTAR_BRIEF.md`.**)

## Nagy, tartalmi döntést igénylő tételek

1. `biblemate-agentic-workspace` (eliranwong) `morphology.sqlite` — konkrét, szűkített haszon azonosítva (2026.09.08, a `morphology_retriever.py` forráskód-elemzéséből): a tábla `ClauseID` mezője **tagmondat-szintű** csoportosítást ad, amivel a formula-motívum-kutatás (pl. "segítségül hívni", "Ani Hu") pontosabbá tehető, mint a jelenlegi, csak szórendet néző pozíció-alapú heurisztika — ez már egyszer, kézzel bevetve segített kizárni a Deut 32:3 jelöltet a BDB "16t" lezárásnál. A `Translation`/`Gloss`/angol Biblia-táblák (NET/BSB/KJV) nem jelentenek pluszt a saját TSV-k mellett. Nyitott döntés: megéri-e a technikai integráció (Google Drive-fájl elérés, file ID `11QfpwEd5fjdDglPiqzygLNN99AVz2mw5`, script-adaptálás) költsége a `ClauseID`-scan rendszeresítéséért — licenc nem akadály (UniqueBible/GPLv3, l. Lezárva). A `cross-reference.sqlite` és a `search_retriever.py` haszna továbbra sincs vizsgálva. **Kapcsolódó, de külön szál (2026.09.10):** ugyanennek az eliranwong-ökoszisztémának egy másik ága (UniqueBible mint megjelenítő alkalmazás, BibleMate AI mint kutatás-gyorsító ügynök) megvizsgálva a Károliba épített kereszthivatkozás kapcsán — l. 2. tétel és a `Bibliai_Motivumlexikon_tervezesi_naplo.md` 17. pontja. Konklúzió: az UniqueBible kifutó rendszer (a fejlesztő saját szavai szerint a BibleMate AI az utódja), és a kereszthivatkozás-funkciója zárt, előre csomagolt adatkészletekhez kötött — nem old meg semmit a mi konkrét megjelenítési kérdésünkből.

   *FJ1 javaslat (2026.09.25, G8):* a Macula Hebrew `<wg class="cl">` tagmondat-csoportjai
   funkcionálisan lefedik a `ClauseID` célját; a `morphology.sqlite` Google Drive-integrációja
   ezzel elkerülhető. Döntésre vár.
2. Publikálási terv — hosszú megbeszélés a magyar nyelvű lexikon-anyag nyilvános közzétételéről. Végkövetkeztetés: van értelme, "kutatási napló"/"motívum-jegyzetek" címmel, TUDOMÁNYOS mélységi szinten (nem hígítva). Licenc-újraellenőrzés szükséges nyilvános közzétételre. **A motívum-alapú kereszthivatkozási réteg** (minden előfordulási igehelyről elérhető a teljes lexikon-cikk/kapcsolati háló, nem csak egy címke) 2026.09.10-re jelentősen előrehaladt: **KAPCSOLATOK Típus-mező v1** lezárt (Előkép/Párhuzam/Beteljesedés/Kontraszt/Variáns); **megjelenítési döntés meghozva** (`Bibliai_Motivumlexikon_tervezesi_naplo.md` 18. szakasz) — induló megoldásként egyszerű, típus nélküli link minden megjelölt versen, nem típusonként színezett popup; **három kézzel épített HTML-pilóta** elkészült és a repóba emelve (`motivumlog/kereszthivatkozas_pilot/`: `01_demo_2_vers.html`, `02_teljes_pilota_29_vers.html` — mind a 29 igehely, valódi Károli-szöveggel, az egyszerűsített döntés szerint —, `03_floating_ui_pilota.html` — a gazdagabb, típusonként színezett popup-verzió próbája `@floating-ui/dom` könyvtárral, összehasonlításra). **A `naszut` projekt Hugo-alapú munkamódszerére való korábbi hivatkozás tévesnek bizonyult** — a `naszut` nem Hugót használ, sima statikus HTML-t Netlify drag-and-drop-pal; egy tényleges Hugo-alapú build ezért nulláról épülne. Technikai kutatás lezárva: Kubernetes Docsy `glossary_tooltip` shortcode-pár, SermonIndex.net auto-linkelő minta, BibleUp (nem használt a pilótákban, csak referenciaként vizsgálva), Floating UI (ténylegesen használva a 03-as pilótában). **Még mindig nyitva:** a lexikon-cikkek tényleges célformátuma a kereszthivatkozás másik végén (nyers markdown vs. Netlify/Hugo-oldal vagy UniqueBible-modul), és maga a tényleges build (Hugo-projekt-inicializálás) — ez továbbra is külön munkamenetet igénylő lépés, amit a mai pilóták nem helyettesítenek, csak előkészítenek.
3. "Én vagyok" tematikus motívum-jelölt (2026.09.08, chat-kutatás — még sehol nincs repóban dokumentálva) — 2Móz 3:14 (אֶהְיֶה אֲשֶׁר אֶהְיֶה ⇒ LXX ἐγώ εἰμι ὁ ὤν) és az Ézsaiás "Ani Hu" klaszter (אֲנִי הוּא) mint LXX-híd Jézus ἐγώ εἰμι-mondásaihoz Jánosnál. Pozíció-alapú TAHOT/TAGNT-ellenőrzéssel megerősítve: 6 valódi ÓSZ Ani Hu-hely (Ézs 41:4, 43:10, 43:13, 46:4, 48:12, 52:6 — a kezdeti 20 jelöltből 14 hamis találatnak bizonyult), 8 abszolút ÚSZ ἐγώ εἰμι-mondás Jánosnál (4:26, 6:20, 8:24, 8:28, 8:58, 13:19, 18:5, 18:6, 18:8), 7 predikátumos ἐγώ εἰμι-mondás (6:35 kenyér, 8:12 világosság, 10:7/9 ajtó, 10:11/14 jó pásztor, 11:25 feltámadás/élet, 14:6 út/igazság/élet, 15:1/5 szőlőtő). Kiemelt lelet: Jer 2:21 (זֶרַע אֱמֶת, "igaz mag") mint lehetséges lexikai/fordítási gyökér a Ján 15:1 ἀληθινή ("igazi") jelzőjéhez — a hét predikátumos kép közül ez az egyetlen lexikai szintű, a többi hat tematikus/kép-szintű. Formális PaRDeS-feldolgozás (négyforrásos audit, sablon szerinti tanulmány) még nem indult el.
4. Olvasói szint — FEJLESZTÉS LEÁLLÍTVA (2026.09.08, l. `motivumlog/Olvasoi_szint_tervezesi_naplo.md` 10. pontja). Egy teljes cikken (ISTENTISZT-001) végzett pilot (6 fokozat, 4 tengely, típus-tudatos finomítás) a `olvasoi-szint-pilot-2026-09-08` branch-en van, NEM mergelve a main-be. Leállítás oka: a publikálási terv (l. 2. tétel), ami ezt indokolná, még csak megbeszélés szintjén áll. Nyitott kérdések (l. napló 10. pont): a 4 tengely függetlensége nincs bizonyítva; a script-koncepció valószínűleg sosem lesz tisztán mechanikus; az általánosíthatóság más szövegtípuson nincs tesztelve. Csak akkor veendő elő újra, ha a publikálási terv ténylegesen elindul.

5. Szótári szerepmátrix — utómunka a 2026.09.25-i döntések után (`F05_SZOTAR_BRIEF.md` v1.1, D16–D17):
   - (a) Licencoszlop a `szotar_szerepek.tsv`-be (forrásonként licenc és a repóban tárolható tartalom) — nyitott javaslat.
   - (b) A 8 törzscikk 5. szakasza a `szotar_szerepek.tsv` v1.1-es módosítása után még a régi forrásneveket mutatja („Cremer (1895)”, „+ Cremer héber mutatója”); a SZOTAR 2. menetének regenerálása hozza helyre.
6. Forrásjelöltek a GitHub-szemléből — **felvéve** (2026.09.25, a felhasználó döntése): vizsgálat, és ha beválik, import, sorrendben (jcuenod/awesome-bible-data és 11 további link alapján):
   - **BSB interlineáris** (BSB-publishing; a Berean Standard Bible 2023 óta közkincs): szószintű, Strong-számozott, teljes bibliás angol híd — a `konkordancia/` KJV/ASV-hídja ma csak 1Móz, 2Móz és Péld.
   - **Macula Hebrew/Greek** (Clear-Bible): mondattani fák, tagmondatszintű tagolás — összevetendő az 1. tétel `morphology.sqlite` `ClauseID`-jával a formulamotívum-kereséshez; licenc ellenőrizendő.
   - **CenterBLC/MT-LXX**: README nélküli Text-Fabric adathalmaz, a neve szerint MT–LXX megfeleltetés — tartalma ellenőrizendő, az S13 (LXX versszintű párok) jelöltje lehet.
   - **Nave's Topical Bible** (1897, közkincs) mint második tematikus forrás a TSK mellé: tiszta adatforrás kiválasztandó (a basokant/nave weboldalról kapar; theonize/bible_database, elcafe7/lex SQLite dokumentálatlan).
   - Nem hoz újat: openscriptures (Strong, OSHB, BDB már megvan; a GreekResources legfeljebb a LXX_OS keresztellenőrzésére), CenterBLC/LXX (a LXX_OS mellett már döntöttünk), unfoldingWord UGL (Abbott-Smith CC BY-SA, az átdolgozás nem készült el), GITenberg 40935 (Green zsebszótára), mrgreekgeek (Brenton angol LXX, Abbott-Smith-kereső), elcafe7 (aggregátor, ESV jogvédett), theonize (Theographic-fork), biblelexicon (Android-app), topics/open-source-bible (témaoldal).
   - **Az FJ 1. menet eredménye (2026.09.25, `FORRASJELOLTEK_BRIEF.md` v1, `naplok/FORRAS_jelentes.md`):**
     CenterBLC/MT-LXX 78,9% és Macula Hebrew 78,3% az aranykészleten — mindkettő a 90%-os küszöb alatt,
     a D14 marad (versszintű S13); a CenterBLC-nek nincs licence, a Macula Hebrew CC BY 4.0. A 87 függő
     LXX-helyre 58 gépi jelölt készült (`naplok/FORRAS_FJ1_lxx_jeloltek.tsv`), küszöb alatti forrásból,
     ezért csak tájékoztató. BSB (`bsb-data-output`, CC0, 66 könyv): N30 lezárva, a BSB importálva: 31 ÓSZ-könyv, l. `konkordancia/README.md`.
     Nave: `theonize/bible_database` feltétellel (GPLv3, a Nave-tartalom licenclánca tisztázatlan),
     `elcafe7/lex` gyengébb. Nyitott utómunka: N27–N31.

## Kisebb, korábbról nyitva maradt tételek

* **ÚJ (F72, 2026.10.07) — N-F72a: a `bdb_strong_potlas.py --alias` őrizze meg az arámi alias-sorokat.** A szkript a `BDB_strong_alias.tsv`-t és a `BDB_strong_alias_elvetett.tsv`-t nulláról újraírja, ezért letörölné az F72-ben beemelt 164 arámi alias-sort (`nyelv=aram`, proveniencia `eszkozok/bdb_aram_beemeles.py --m2`). Javaslat: az `--alias` fűzze hozzá az ilyen sorokat az újragenerált táblához, vagy az arámi sorok generálása kerüljön egy közös szkriptbe; addig a `BDB_teljes_unabridged_README.md` figyelmeztetése érvényes. (A számot a main-Action osztja ki.)

* **ÚJ (2026.10.05, olvasói prototípus) — a `konkordancia/Macula_heber_*.tsv` `gorog_lxx` oszlopában a χ és a ξ betű rendszeresen fel van cserélve.** Példák (1Móz 1): `ἀρξῇ` → helyesen `ἀρχῇ`, `χηρά` → `ξηρά`, `χύλον` → `ξύλον`, `ψυξὴν` → `ψυχὴν`, `αὐχάνεσθε` → `αὐξάνεσθε`; az 1Móz 1:1–2:3 szakaszban 34 szóalak, az LXX_OS (Rahlfs) szóalakjával összevetve. Kiterjedés a teljes táblán (`manual` mérés): a nem üres `gorog_lxx` sorokból 7 681 tartalmaz χ-t és 12 275 ξ-t; jellemző tövek: `ψυξ` 688 / `ψυχ` 5, `ἀρξ` 250 / `ἀρχ` 3, `χηρ` 99 / `ξηρ` 16 — a csere tehát szinte teljes. *(proveniencia: scope=konkordancia/Macula_heber_*.tsv (gorog_lxx) | forras=manual | ts=2026-10-05)* A `gorog_strong` oszlop nem érintett, ezért a Strong-számokon dolgozó feldolgozás (a #43 LXX-ellenőrzés, a `lxx_bridge`, a #54) nem sérül; minden olyan hely viszont hibás görög szóalakot mutat vagy idéz, amely a `gorog_lxx` oszlopot szövegként használja. Az F17 importja (`eszkozok/f17/macula_futtat.py`) a `greek` mezőt változtatás nélkül veszi át, ezért a hiba vagy a Clear-Bible/macula-hebrew forrásban van, vagy a beolvasáskor keletkezett. **Teendő:** (1) összevetés az eredeti macula-hebrew fájllal (commit `47db250`) néhány ismert helyen; (2) ha a forrás hibás: jelzés a forrásnak, és nálunk javítás egy csere-lépéssel az importban, a csere szabályának naplózásával; ha az import hibás: az import javítása és a táblák újragenerálása; (3) addig a megjelenítés a görög szóalakot az `LXX_OS`-ből vegye, a Maculából csak a párosítást (az olvasói prototípus már így dolgozik).

* **ÚJ (F42 utótétel, 2026.10.05) — a HODIT-001 élő lexikonoldala és mind a 8 törzscikk elavult a mai adathoz képest → #36 (LEXIKON_UJRAGEN).** A #42 (PR #176) M7 render-diffje szerint a HODIT-001 oldalon a #42 hatása csak 5 Józs-sor (elsődleges szövegváltozat: `joshua-vaticanus-b`), mögötte nagyobb, az F8 óta felgyűlt elavulás áll (LXX-döntések „kutatói azonosítás függőben” → „eltérő”); a 8 `lexikon/*_TORZSCIKK.md` oldalanként 65–326 sorban tér el (az ISTENTISZT-001 törzscikk még LSJ „CC BY-SA 3.0”-t ír). A felzárkóztatás a #36 dolga; a #42 nem hagyta jóvá helyette. Forrás: `naplok/FORRASKIVEZETES_M5_M7.md` (M7), `naplok/FORRASKIVEZETES_zaras.md`.

* **ÚJ (F4.0e, 2026.09.15) — a `Lezart_tematikus_tanulmanyok_index.md` #2 sora (ALVIL-001) hiányos.** A `fo_elofordulas` mező G0/d kitöltésekor kiderült: a napló saját ⭐-szakasza (`PaRDeS_motivumok.md`, `[ID: ALVIL-001]` bejegyzés) 6 tagot sorol fel — Zsolt 16:10⇒ApCsel 2:27,31, Luk 16:23, **Jel 1:18**, Jel 6:8, Luk 10:15/Mát 11:23, Jel 20:13-14 —, miközben az index #2 sora csak 5-öt nevez meg (a Jel 1:18 hiányzik belőle), a "6 előfordulás" számot mégis helyesen tartja. A napló ⭐-szakasza az irányadó; az index sora pótlandó a Jel 1:18-cal.
* **ÚJ (F4.0d, 2026.09.14) — `Karoli_Strong_kivonat.tsv` drift: a két utolsó oszlop (Szófaj, Gyök/Származtatás) elavult a mai `Strong_szotar.tsv`-hez képest** (HEAD 46 105 bájt vs. friss futás 45 659 — mérve `eszkozok/merge_karoli_szofaj.py`-jal, olvasás-only, **nem futtatva élesben**). Oszloponkénti bontás: 32 sor érintett összesen; ebből 7 sorban tér el a Szófaj, 32 sorban a Gyök/Származtatás; 14 mezőben üresből lett kitöltött a friss `Strong_szotar.tsv` szerint (fordítva, kitöltöttből üresbe, 0 eset); a héber kombináló-jelek puszta sorrend-eltérése (NFD-azonos, karaktersorrend más) 0 esetben magyarázza az eltérést — minden eltérés tartalmi. Újragenerálás **NINCS** — a Szófaj oszlop study-bemenet, ez külön döntés.
* 3 ÚSZ study első audit (Róm 8:10, Zsid 4:12, 1Thessz 5:23) — a három bővített tanulmányfájl már létezik (2026.07.28/07.30 óta), de a négyforrásos audit még nem futott le rajtuk
* **5 további tematikus study v12-compliance** — a 7 meglévő tematikus study közül eddig 2 kapta meg a Q1-Q5 Minőségi kaput (Melkizedek — 2026.09.09; Segítségül hívni — már 2026.09.08 óta). Az 5 még hátralévő: `Isten_fiai_Nefilim_Gibborim_tematikus.md`, `Rafaim_tematikus.md`, `Tehom_Abusszosz_Hadesz_Tartarosz_tematikus.md`, `Tehom_tematikus.md`, `Pneuma_pszukhe_megkulonboztetes_tematikus.md`
* 5 küszöbön-túli, még meg sem írt motívum (l. `PaRDeS_motivumok.md` ⭐ szakasz) — ANTROP-002 (uralom-megbízás), ANTROP-003 (Isten képmása), TEREMT-002 (תהו/בהו mint ítélet-nyelvezet), ISTENTISZT-002 (oltárépítés), SZOVETS-001 (brít első előfordulása) — mindegyik felhasználói jóváhagyásra vár. *(Javítva N14, 2026.09.21: a HAMART-001 tévesen szerepelt itt — lezárt study-ja van, a hiánya betöltési, l. N14.)*
* Tehóm/Seól (H8415/H7585) — ⏹ **JAVÍTVA (F1.6 ellenőrzés, 2026.09.13): ez a tétel elavult volt.** A korábbi szöveg azt állította, hogy „a Seól-motívum jelölt-listája továbbra is valóban nyitott; egy teljes, friss H7585-scan szükséges" — **a scan azóta lefutott**: a `Hadesz_Seol_tematikus.md` v2 (2026.09.10) 66 nyers szóelőfordulást / 64 egyedi verset vizsgált, **64 beépítve**, Hós 13:14 kiemelt leletként; naplózva a `tematikus_lezart/naplok/Hadesz_Seol_kereszthivatkozas_naplo.md`-ben. A Tehóm-ág változatlanul gyakorlatilag lezárt (24/24 jelölt beépítve, v47-es kör, 2026.08.25). **Ami ténylegesen marad:** (a) egy gyors megerősítő újra-scan mindkét gyökre friss adaton, (b) a Tehóm-gyök rokon gyökű jelöltje, H4103 (*mehumáh*, „zűrzavar, pánik") — egyedi minősítés nélkül.
* Nevesített tanítói szakasz pótlása az ISTENTISZT-001 pilotban (`motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md`) — döntés megvan: "halvány, tematikus, nem bizonyító erejű" jelöléssel, változtatás nélkül átvehető a `Segitsegul_hivni_az_Urat_tematikus.md` Alkalmazás-szakaszából; csak a végrehajtás hiányzik
* **ÚJ (2026.09.10) — más tematikus study-k TSK-auditjának újra-átnézése a Q2-szabály fényében.** A Melkizedek-study 1Pét 2:9-es hiánya (l. Lezárva) azért derült ki, mert a TSK a nyers találatok között megtalálta, de sosem került át a minősítő táblázatba — ez strukturális hiba volt, nem egyedi eset. A `4_PaRDeS_tematikus_sablon.md` Q2 pontja mostantól kötelezővé teszi minden TSK-jelölt egyedi minősítését, de ez csak a jövőbeli study-kra vonatkozik automatikusan — a meglévő 7 tematikus study egyikén sem lett systematikusan újra átnézve, van-e hasonlóan kiesett, korábban megtalált de sosem minősített TSK-jelölt.
* **ÚJ (F4-0, 2026.09.14) — 10 `eszkozok/*.py`-nak nincs sem `argparse`-a, sem `if __name__ == "__main__":` őre** (mérve: `f3_1_betoltes.py`, `f3_2_betoltes.py`, `f3_4_ellenoriz.py`, `f3_4_elokeszites.py`, `f3_4_gorog_ellenoriz.py`, `f3_4_join_potlas.py`, `f3_4_munkalap_general.py`, `f3_4_nema_nemtalalat.py`, `f3_4_zaro_ellenoriz.py`, `merge_karoli_szofaj.py`) — ezekben a teljes törzs lefut bármilyen közvetlen `python szkript.py` hívásra, argumentumtól függetlenül; egy `--help` sem súgót ír, hanem végrehajtja a szkriptet. Ebből **8 modulszinten fájlt is ír** (mind, `f3_4_gorog_ellenoriz.py` és `f3_4_zaro_ellenoriz.py` kivételével) — bármely véletlen hívás (pl. egy jövőbeli füstteszt) csendben felülírhatja/duplikálhatja a kanonikus táblákat. Dokumentált eset: az F4-0 E tétel `--help`-alapú ellenőrzése ténylegesen kiváltotta ezt a `f3_1_betoltes.py`-nál és a `f3_2_betoltes.py`-nál (l. `F4_BRIEF.md` E/2-E/3, helyreállítva). Nem az F4-0 része — külön tétel.
* **ÚJ (F4-0, 2026.09.14) — négy `eszkozok/*.py` sorokra bontáskor nem strippeli a `\r`-t** (mérve: `elofordulas_szamlalo.py`, `f3_4_zaro_ellenoriz.py`, `frazis_kereses_pozicio_alapon.py`, `tahot_zarojeles_phaseA_kivonat.py`) — mindegyik `line.rstrip("\n")` (vagy `.rstrip('\n')`) alakot használ, ami CRLF-sorvégű bemeneten a `\r`-t a sor VÉGÉN hagyja, és az a `split('\t')` utáni utolsó mezőbe kerül be szennyeződésként (néma, mert a `\r` nem látható). Jelenleg nincs élő kár, mert az `adat/*.tsv` és a `konkordancia/*.tsv` táblák LF-tisztán tartottak (l. `F4_BRIEF.md` E11), de az `f3_4_zaro_ellenoriz.py` éppen az `adat/elofordulasok.tsv`-t olvassa így — ha az a tábla valaha CRLF-re vált (mint az F4.0a menetben egyszer, véletlenül, most helyreállítva), a szkript némán szennyezett utolsó mezőket lát. Javítás: `rstrip("\n")` helyett `rstrip("\n").rstrip("\r")` vagy `rstrip("\r\n")` mindegyikben — nem az F4-0 része, külön tétel.
* A lexikon-oldal KAPCSOLATOK-diagram és a TSV "Típus" oszlopa közötti névütközés (l. `ISTENTISZT-001_TUDOMANYOS.md` 7. pont NAPLO-ja, 2026.09.09) — a `Motivum_kapcsolatok_PILOT.tsv` "Típus" oszlopa (LEXIKAI/NARRATÍV/STRUKTURÁLIS/TEMATIKUS) egy MÁSIK tengely, mint a diagram PaRDeS Típus-mezője (Előkép/Párhuzam/Beteljesedés/Kontraszt/Variáns); a TSV-ben nincs önálló oszlop a PaRDeS Típus-mezőre — nyitott kérdés marad, nem oldódott meg. **Az `adat/kapcsolatok.tsv` a PaRDeS-tengelyt viszi (l. `adat/SEMA.md` 2.3); a szétválasztás az F3 betöltés feladata.**
* **ÚJ (F6, 2026.09.20) — jelentés-hivatkozások kitöltése öt adatszegény motívumra és 33 görög sorra.** Az ALVIL-001, ANTROP-001, HODIT-001, MENNY-001, TEREMT-001 héber Strong-tokenjeire és mind a 33 görög előfordulás-sorra nincs `lexikon_hivatkozasok.tsv` bejegyzés (BDB, illetve TBESG forrásból); a munkalista a generált `lexikon/*_TUDOMANYOS.md` "Nincs jelentés-hivatkozás" soraiból áll össze — külön, tartalmi Opus-menet (F6_BRIEF.md N1).
* **ÚJ (F6, 2026.09.20) — a `jelentes_szam` három union-sértő értéke.** Az `elofordulasok.tsv`-ben `2.c (tagadva)` (×2) és `2.c (rokon)` (×1) igehelyi megjegyzést hordoz jelentés-szám helyett — eldöntendő, hogy a `kapcsolodas` mezőbe, új mezőbe, vagy a `jelentes_hu`-ba kerüljön (F6_BRIEF.md N2).
* **ÚJ (F6, 2026.09.20) — Formula és Kapcsolódó motívum mező hiánya a `motivumok.tsv`-ben.** A lexikon-sablon 0. szakasza kéri mindkettőt, a táblában nincs mezőjük — eldöntendő, hogy új mezőként felvételre kerüljenek, vagy maradjanak kézi szövegként a lexikon-oldalon (F6_BRIEF.md N3).
* **ÚJ (F6, 2026.09.20) — a tisztázatlan licencű források (LXX-kivonat, MCGED) kockázata.** *(SZŰKÍTVE — F7.1, 2026.09.20: a korábban idesorolt három forrás az F6.5b óta tisztázott — l. alább, N5.)* A D9 döntés szerint idézhetők, `tisztazatlan` jelöléssel a generált lexikon-rétegben; az MCGED (Mounce) valószínűleg védett kereskedelmi mű — publikálás vagy megkeresés esetén a `tisztazatlan` jelölésű blokkok az elsők, amelyeket jogilag át kell nézni (F6_BRIEF.md N4).
* ~~**ÚJ (F6, 2026.09.20) — a Thayer digitalizált forrásának jogtisztázása.**~~ **LEZÁRVA (F7.1, 2026.09.20) → F6.5b, `3099114`.** A Thayer `tisztazatlan` licenc-jelölése `közkincs`-re cserélve a generátorban (F6_BRIEF.md N5). *(A besorolás a szerző forrásoldaláról való, l. §1.6 fenntartása — nem a letöltött fájlokhoz csatolt licencszövegből.)*
* **ÚJ (F6, 2026.09.20) — a KIRALY-001 `G0813` tokenje téves.** A `TAGNT_kivonat.tsv` szerint helyesen `G0540` volna (l. fent, F3.4-es tétel); a generált lexikon-szócikk ezt a hibát a mai `motivumok.tsv`/`elofordulasok.tsv` állapot szerint továbbviszi — felhasználói megerősítésre vár (F6_BRIEF.md N6).

- **N7 — A marker-fejléc befagyása meglévő fájlon.** *(ÚJ, F6 zárás után,
  2026.09.20)* A megosztott `G.blokk_beilleszt` (`eszkozok/general.py`) csak a
  marker-pár közötti törzset cseréli, a kezdő marker fejlécét soha — így a
  fejlécmezők (pl. `licenc:`) meglévő fájlon némán befagynak. Az F6.5a ezt csak
  a lexikon célra kerülte meg (`_blokk_beilleszt_fejleccel`, `lexikon_general.py`);
  a `naplo`/`index`/`nyitott`/`motivumok` célokon ma azért nem látszik, mert a
  fejlécükben a `ts=`-en kívül nincs érdemi adat. Amint bármelyikébe metaadat
  kerül, ugyanez a néma nem-frissülés jön vissza. Eldöntendő: a fejléces
  beillesztés váltsa-e ki a megosztott függvényt (a K7/K8 byte-azonossági
  garanciák újramérésével), vagy maradjon célonkénti.

- **N8 — A `general.py` main() cél-kivételei.** *(ÚJ, F6 zárás után, 2026.09.20)*
  Az F6.5 után három helyen `cel != 'lexikon'` kivétel ágaztatja a main()-t
  (egyfájlos `CEL_FAJL`-ág, „nem élesíthető” üzenet, `vegso_kod`). A minta a
  következő könyvtáras célnál megismétlődne. Eldöntendő: cél-képesség leíró
  (egyfájlos/könyvtáras, élesíthető, saját jelentés) váltsa-e ki mindhármat.

- **N9 — A licenc-besorolás kettős forrása. LEZÁRVA (F42.7, 2026.10.05; DT-F42g).** *(ÚJ, F6 zárás után, 2026.09.20)*
  Az F6.5b után a besorolás két helyen áll: a `lexikon_general.py`
  licenc-konstansában és a `TISZTAZATLAN_SZOTARAK` halmazban (ez utóbbi most
  üres, magyarázó kommenttel). Egy új, tisztázatlan licencű forrásnál a kettő
  szétcsúszhat. Javaslat: a halmaz származzon a konstansból
  (`{f for f, l in LICENC.items() if l == 'tisztazatlan'}`), vagy szűnjön meg.

- **N10 — A „sorozat-tábla" (terv A7) nincs definiálva. LEZÁRVA (F8.2,
  2026.09.21).** *(ÚJ, F7 után, 2026.09.20)* Az `ATALAKITASI_TERV.md.md` 7.
  pontja az A7 lépésnél „motívumnapló, index, sorozat-tábla újragenerálása"-t
  ír elő, de a „sorozat-tábla" fogalma a tervben sehol máshol nincs
  definiálva, és nincs hozzá implementáció (`eszkozok/`-ban nincs rá utaló
  szkript). **Definíció (F8_BRIEF.md G1):** a sorozat-tábla = a napló
  „Feldolgozott igeszakaszok listája" (`motivumlog/PaRDeS_motivumok.md`),
  kézzel karbantartva. A generálás önálló tétel, l. N11.

- **N11 — A sorozat-tábla generálása.** *(ÚJ, F8.2, 2026.09.21)* Az N10
  lezárása a sorozat-táblát a napló „Feldolgozott igeszakaszok listája"
  szakaszaként azonosította, kézi karbantartással. Eldöntendő, generálandó-e
  a jövőben egy új `adat/tanulmanyok.tsv`-ből (a 24 sor migrálásával) — ez
  volt az F8_BRIEF.md G1 elvetett alternatívája. A „Fő kulcsszavak" oszlopot
  generálás esetén is a kutató írná; a generálás nyeresége a 0. pont
  aktiválási feltételének gépi ellenőrizhetősége volna.

- **N12 — A SEMA §3/8 és a retroaktív sorok. LEZÁRVA (N12, 2026.09.21).**
  *(ÚJ, F8.10, 2026.09.21)* Mind a 201 `elofordulasok`-sor `scope=manual`
  (F3-betöltés), ezért az `ellenoriz.py` 8. szabálya (dataset-lefedettség)
  mind a 7 motívumra sértett — a régi illesztés emellett részsztring-alapú
  volt, tehát a `karoli` parancs `+`-szal összefűzött forrása soha nem
  illeszkedett a Karoli_KH-ra. **Megoldás (N12_BRIEF.md G1–G4):** a 8.
  szabály motívumszintűvé vált, új `adat/auditok.tsv` nyom-táblával (0
  találatos lekérdezés is nyom); a `forras` érték `+` mentén bontva, PONTOS
  fájlnév-egyezéssel illeszt; a BDB (nincs lekérdező parancs) és a 7
  retroaktív motívum hiányzó datasetjei (zárt lista) KÉZI jelentést kapnak,
  nem SÉRTÉST. Eredmény: a 8. szabály ma KÉZI (0 gépileg ellenőrizhető
  motívum) a korábbi SÉRTÉS (35) helyett; az első új motívumnál gépi zöld
  vagy piros. L. `N12_BRIEF.md`, `N12.1`–`N12.3` commitok.

- **N13 — A `jelolt.py` túltermelése gyakori Strongokon.** *(ÚJ, F8.10,
  2026.09.21)* Az 1Móz 7:1-24 szakaszra `jelolt.py` 10 „új jelölt" sort ad,
  főleg H1121, H0430 (MENNY-001) és H2416 (ANTROP-001) gyakori Strongokon.
  Eldöntendő: gyakorisági küszöb, kollokáció-pár megkövetelése a többstrongos
  motívumoknál, vagy a MENNY-001 `azonossag_tipusa` felülvizsgálata. A
  GENERÁLT blokk nem módosul.

- **N14 — A HAMART-001 betöltése az `adat/`-ba. LEZÁRVA (N14, 2026.09.21).**
  *(ÚJ, N12 után, 2026.09.21)* A HAMART-001-nek lezárt study-ja volt
  (`tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md`) és
  kereszthivatkozás-naplója, de az `adat/`-ban egyetlen sora sem volt: a
  terv F3-köre (7 lezárt study + ISTENTISZT-001 lexikon) a 2026.09.13-i
  állapotot rögzítette, amikor a study még két ágon, mergeletlenül állt;
  az F0.1-es merge (`c28b49e`) után a kört senki nem bővítette.
  **Megoldás (N14_BRIEF.md G1–G6):** a study 1. pontjának A/B/C táblázata
  retroaktív betöltéssel, `scope=manual` provenienciával, `eszkozok/
  n14_hamart_betoltes.py`-n és a `betolt.py beepit` F8-átjárón át 52
  `elofordulasok`-sorra bomlott (a 46 study-sorból G3 szerint 3 vesszős/
  perjeles összevonás szétbontva); a `gerinc_elem` a study saját
  BDB-horgonyát követi (G2), kollokációnál a SEMA 2.2 pár-alakját
  (`málé+chámász`, `sámá+chámász`); a `fo_elofordulas` a napló négy
  szakasz-megnevezése (G4). A SEMA §3/8 (b) útja: a HAMART-001 az
  `ellenoriz.RETROAKTIV_IDK` zárt listájára került (7 → 8 ID) — a study
  2026.09.11-i megírásakor a `lekerdez.py` még nem létezett (F2:
  2026.09.14), tehát valódi lekérdezés utólagos gyártása lett volna a
  proveniencia. A napló három kézi HAMART-001-szövege és az index kézi
  „betöltetlen tanulmány" szakasza a forrásrétegbe költözött
  (`motivumok/HAMART-001.md`, F4.4 mintája), karakterre azonosan. Eredmény:
  `ellenoriz.py` 6·0·3·1, kód 0, 8/c KÉZI (8); a `general.py --cel naplo/
  index --ir` fixponton ZÖLD; `gate.py` nem talált új HAMART-001-ütközést.
  L. `N14_BRIEF.md`, `N14.0`–`N14.4` commitok.

- **N15 — Az LXX-kivonat licenc-tisztázása. LEZÁRVA (LEXV2_2, 2026.09.22).** *(ÚJ, LEX, 2026.09.21)*
  A `konkordancia/LXX_kivonat_*.tsv` (39 könyv) a studybible.info
  LXX_WH + ABP oldalaiból készült, licencnyilatkozat nélkül (l.
  `LXX_kivonat_README.md` „Licenc-státusz — explicit gap"); az F6
  licenc-térképén ez az egyetlen `tisztazatlan` forrás, és minden
  lexikon-oldal 3. szakaszát (LXX-híd) érinti. Belső használatra nem
  akadály (N11/N3: a lexikon belső), a publikálási döntésnek viszont
  elzáró tétele. Két út: (a) a studybible.info üzemeltetőjének
  megkeresése; (b) forráscsere azonos oszlopformátummal — jelölt: az
  Open Scriptorium (openscriptorium.org) Rahlfs-LXX adata. Szöveg:
  Rahlfs 1935, közkincs; szószintű morfológia és lemma: lxx-morph
  (`git.sr.ht/~sethkush/lxx-morph`, CC BY 4.0, megjelöléssel; a szerző
  nem szakértő, a proveniencia megbízhatósági sávval jelölt). A szavak
  `strongs_number` mezője üres, de a közös lemma-tábla Strong-számot
  ad (`/api/v1/lemmas/124` → θεός → `strongs_numbers: ["G2316"]`;
  ellenőrizve mindkét irányban, 2026.09.21: `/lemmas/strong/G2316` →
  egyetlen lemma, id 124). Így a szűrés a mostani logikával mehet:
  motívum-Strong → lemma-id(k) → LXX-szavak, külső híd nélkül; ha egy
  Strong több lemmára mutat, mind bekerül a szűrőbe. A morfológia
  szöveges címke (`noun fem dat sg`), nem tömör kód. Forrás: a teljes
  SQLite-letöltés (`openscriptorium.org/downloads`), nem az API
  (60 kérés/perc). Nem jelölt (CATSS-alapú, felhasználói nyilatkozathoz
  kötött): Eliran Wong LXX-Rahlfs-1935 (CC BY-NC-SA 4.0),
  CenterBLC/LXX, codykingham/catss_lxx. Első lépés: az SQLite
  Strong→lemma joinjával a Genezis újraépítése, és a motívum-tokenek
  találatainak összevetése a mostani `LXX_kivonat_Genezis.tsv`-vel.

  **Állapot (LEXV2_1, 2026.09.22):** az Open Scriptorium-kivonat elkészült
  (`konkordancia/LXX_OS/`), összevetés: `naplok/LEXV2_lxx_osszevetes.tsv`; a
  generátor átállítása a lexikon-oldal v2 (2. menet) része. Az N15 akkor
  zárul, ha a régi kivonat kikerül a generált rétegből. **Pontosítás a fenti
  tervhez képest:** a bulk SQLite végül nem tartalmazott lemma-táblát
  (`words.strongs_number` üres a teljes rahlfs-lxx műre) — a tényleges forrás
  az lxx-morph szavankénti `lemma` mezője + a GreekWordList (Strong), a
  Károli-igehely pedig a meglévő `LXX_versificacios_terkep.tsv` +
  `KEZI_ELTOLASOK` újrafelhasználásával, nem a `verse_pairs.jsonl`
  KJV-számozásával (l. `LEXV2_1_BRIEF.md` döntésnapló v3).

  **Lezárás (LEXV2_2_BRIEF.md, 2026.09.22):** a lexikon-oldal generátora
  (`eszkozok/lexikon_general.py`, V2.4) a 3. szakaszt (LXX-fordítói döntések)
  mostantól kizárólag a `konkordancia/LXX_OS/`-ből építi — a régi
  `LXX_kivonat_*.tsv` teljesen kikerült a generált rétegből (nincs rá
  hivatkozás egyetlen `lexikon/*_TUDOMANYOS.md`-ben sem, ellenőrizve
  szkripttel, K4). A `LXX_OS` licence CC BY 4.0 (lxx-morph + GreekWordList),
  tisztázott — az N15 ezzel lezárva.

- **N16 — Az ISTENTISZT-001 hiányzó ÚSZ-i idézőhelyei. LEZÁRVA (N16, 2026.09.21).** *(ÚJ, LEX.2
  zárójelentése, 2026.09.21)* A Jóel 2:32 szó szerinti ÚSZ-i idézetei
  — ApCsel 2:21 és Róm 10:13 — nincsenek az `elofordulasok.tsv`
  29 ISTENTISZT-001 sora között, noha a Jóel 2:32 sor megjegyzése
  mindkettőt megnevezi. A `kapcsolatok.tsv` Jóel 2:32 → Róm 10:14
  „Beteljesedés" sora „szó szerinti LXX-idézés-lánc (2:32⇒Róm
  10:13⇒10:14)" indoklású, de a lánc középső tagja sorként nem
  létezik, a Róm 10:14 pedig nem idézet, hanem folytatás. A lexikon-
  oldal (`lexikon/ISTENTISZT-001_TUDOMANYOS.md`, `_OLVASHATO.md`) kézi
  szövegében ⚠ ELTÉRÉS jelöli. Eldöntendő: a két sor felvétele
  (proveniencia: a pilot 2026.09.06-i auditja vagy új lekérdezés) és
  a Jóel 2:32 → Róm 10:14 kapcsolat átkötése Róm 10:13-ra. Utána a
  ⚠ ELTÉRÉS jelölések feloldhatók. Kapcsolódó: a módszertani napló
  „15 emberi-invokációs eset" állítása a jelenlegi táblán
  ellenőrizendő (a zárójelentés 27-et becsült, nem mért).

  **Megoldás (N16_BRIEF.md):** a két sor a study kapcsolat-táblája alapján, `scope=manual` provenienciával, `betolt.py beepit` úton betöltve (29 → 31 sor); a Jóel 2:32 → Róm 10:14 kapcsolat a study szerinti három sorra bontva (23 → 25 kapcsolat). A lexikon-oldal ApCsel/Róm 10:13 ⚠ ELTÉRÉS-jelölései feloldva; a pilot szótári anyaga (2–4. szakasz) a 2/b. kézi alszakaszba átemelve. L. `N16.0`–`N16.5` commitok.

- **N17 — A régi `LXX_kivonat_Zsoltarok.tsv` Igehely-címkéi gyanúsan a KJV
  (angol) versszámozást viselhetik Károli helyett, cím-viselő zsoltároknál. LEZÁRVA (F42.M5, 2026.10.05).**
  *Megoldás:* a gyanú igazolódott (a régi zsoltár-kivonat egy verssel eltolt: 739 zsoltárvers egyezik az LXX_OS következő versével, `naplok/FORRASKIVEZETES_M5_eltereslista.tsv`, kategória `zsoltar_eltolas`); a régi kivonat kivezetve, az `lxx-hid` az `LXX_OS`-ből olvas (javítja az eltolást). *Tartalmi kérdés, nem javítva:* a régi kivonatra épült állítások: `adat/auditok.tsv` TEREMT-002 B4 sorai (Zsolt 107:40, 104:30, 33:6, 80:6, 80:7; 32., 82., 85., 160., 163. sor) és a másolat `naplok/T1_TEREMT002_auditok_munkalap.tsv`; `tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md` (LXX-egyeztetés Zsolt 14:1, 53:1), `tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` (92. sor), `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` (370. sor). Ezek újraellenőrzése külön döntés.
  *(ÚJ, LEXV2_1 V1.3a független ellenőrzése, 2026.09.22)* A `LEXV2_1_BRIEF.md`
  V1.3a tétele során kiderült: a `konkordancia/LXX_versificacios_terkep.tsv`
  a studybible.info saját belső oldal-verszámozására épült, ami cím-viselő
  zsoltároknál NEM esik egybe sem az lxx-morph, sem a valódi Károli
  versszámozással. Ennek gyanús tünete a régi kivonatban is megjelenik:
  `LXX_kivonat_Zsoltarok.tsv` „Zsolt 3:2" sora a `πολλοι λεγουσιν τη ψυχη
  μου` („sokan mondják az én lelkem felől") szöveget tartalmazza — ez
  tartalmilag a KJV/angol Zsolt 3:2, míg a valódi Károli 3:2 („Uram!
  mennyire megsokasodtak ellenségeim!") a KJV/angol 3:1-nek felel meg (a
  Károli a zsoltárcímet önálló 1. versnek számozza, az angol hagyomány nem).
  **Nincs megvizsgálva, mekkora a hatóköre** (hány zsoltár-fejezetet érint,
  és érinti-e ez a jelenlegi generált lexikon-oldalak LXX-hídját, amely a
  régi kivonatot használja). Külön menet/brief tárgya: a
  `LXX_versificacios_terkep.tsv` és a `LXX_kivonat_*.tsv` (elsősorban
  Zsoltárok) szisztematikus átvizsgálása, összevetve a
  `LEXV2_1_BRIEF.md` V1.3a algoritmusával (KJV-fejezet-egyezés + Zsoltár
  cím-eltolás), és ha valódi hiba igazolódik, a régi kivonat javítása vagy
  lecserélése az új `konkordancia/LXX_OS/`-re.

  **Szűkítés (LEXV2_2_BRIEF.md, 2026.09.22):** a régi `LXX_kivonat_*.tsv`
  (és a rá épülő `LXX_versificacios_terkep.tsv`) mostantól kizárólag
  archív — a lexikon-generátor (V2.4) a `LXX_OS`-t használja, a régi
  kivonatot semmilyen generált oldal nem olvassa. Az N17 hátralévő
  hatóköre ezért csak a saját magára, archívumként: a Zsoltár-számozási
  gyanú ellenőrzése akkor válik ismét élessé, ha a régi kivonatot valaki
  újra bemenetként használná (jelenleg nincs ilyen felhasználás).

- **N18 — Az ANTROP-001-nek nincs kereszthivatkozás-naplója.** *(ÚJ,
  RENDER_BRIEF.md R2.1, G14, 2026.09.23)* A `minosites` rés forrása a
  motívum kereszthivatkozás-naplójának „Tartalmi minősítés minden
  jelöltre" és „Végső döntés és indoklás" szakasza volna (G14) — a másik
  hat lezárt motívumnak (KIRALY-001, TEREMT-001, ALVIL-001, MENNY-001,
  HODIT-001, HAMART-001) megvan ez a naplója, az ANTROP-001-nek
  (`Pneuma_pszukhe_megkulonboztetes_tematikus.md`) nincs. A lexikonoldal
  `minosites` rése ezért egy explicit hiány-mondatot kapott a
  tanulmányban (*„A kereszthivatkozás-minősítés ennél a motívumnál nem
  készült el."*), jelölők közt. Eldöntendő: készüljön-e utólag napló
  (`tematikus_lezart/naplok/Pneuma_pszukhe_megkulonboztetes_kereszthivatkozas_naplo.md`)
  a többi hathoz hasonló TSK/Károli-audittal, vagy maradjon a hiány
  dokumentálva.

- **N19 — KIRALY-001 kapcsolatainak bizonyossági indoklása (C2).** *(ÚJ,
  RENDER_BRIEF.md R2.2, G16, 2026.09.23)* Az `alatamasztas` rés forrása
  a hat 0-kapcsolatú motívumnál `adat` (G16 alapértelmezés). A
  KIRALY-001-nek van kapcsolata (9 sor, `adat/kapcsolatok.tsv`), ezért
  a G16 egy tanulmány/napló-beli indoklás-forrást várt volna — a
  felhasználói döntés szerint azonban a napló „Végső döntés és
  indoklás" szakasza (a `minosites` rés forrása) tartalmilag nem
  alátámasztás, hanem jelölt-elfogadási indoklás, és nincs olyan kész
  szövegrész, amely kifejezetten a 9 kapcsolatot indokolná. Ezért a
  `res_forras.tsv` KIRALY-001/`alatamasztas` sora is `adat` forrású
  lett, egy a hattól eltérő, a `kapcsolatok.tsv` Funkció oszlopára
  mutató generált mondattal. Eldöntendő: készüljön-e később egy
  önálló, a 9 kapcsolatot ténylegesen indokoló bekezdés a
  `Melkizedek_tematikus_kereszthivatkozas_naplo.md`-be, saját
  `RÉS-KEZDET/VÉGE: alatamasztas` jelöléssel — ez lecserélné a jelenlegi
  `adat`-forrású generált mondatot egy valódi, C2-szintű indoklásra.

- **N20 — SEMA 1.4: `Pshat` vs. az adatban mindenhol `Peshat`.** *(ÚJ,
  TEREMT002_KUTATAS_BRIEF T2.1, 2026.09.25)* A SEMA 1.4 `Pshat`-ot ír elő,
  az `elofordulasok.tsv` minden érintett sora (a TEREMT-002 1Móz 1:2-sorával
  együtt) `Peshat`-ot használ — a SEMA igazítandó az adathoz.

- **N21 — `Karoli_Strong_kivonat.tsv` Gen.1.2: nullázatlan `H922`.** *(ÚJ,
  TEREMT002_KUTATAS_BRIEF T2.1, 2026.09.25)* A sor `H8414+H922`-t visel
  `H8414+H0922` helyett (SEMA 1.2); a 26 nullázatlan régi join-sorról szóló
  F3.4-es tétel (l. „Migrálva…” szakasz) egyik esete, a TEREMT-002-nél
  külön is felszínre került.

- **N22 — `Karoli_kereszthivatkozasok.tsv`: az `Isa.34.11` lista az
  `Isa.40.11` másolata.** *(ÚJ, TEREMT002_KUTATAS_BRIEF T1.1, 2026.09.25)*
  A lista betűre azonos (pásztor-kép: Ézs 66:12, Ez 34:12-16, Ján 10:11,
  1Móz 33:13, 4Móz 11:12) — javítandó, és felveendő a
  `Karoli_adatminosegi_anomaliak.tsv`-be; utána TEREMT-002 pót-scan
  (`lekerdez.py karoli`) az Ézs 34:11 valódi Károli-KH célpontjaira (az öt
  hibás célpont a `jeloltek.tsv`-ben `elutasítva`, „adathiba” indokkal).

- **N23 — `ellenoriz.py`: a zárt `lepes`-készlet ellenőrzése; `MUNKAMENET.md`
  B3.** *(ÚJ, TEREMT002_KUTATAS_BRIEF T1.3, 2026.09.25)* Az `auditok.lepes`
  zárt készletét (`A5 | B2 | B3 | B4`, SEMA 2.9) ma semmi nem ellenőrzi, és a
  `MUNKAMENET.md` B3-sora („kézi”) nem említi a `lekerdez.py domen` futást,
  amely B3-as audit-sort kap.

- **N24 — `general.py`: a többértékű `tema` bontása a napló
  témacsoportosításában.** *(ÚJ, TEREMT002_KUTATAS_BRIEF T2.3, 2026.09.25)*
  A `naplo#attekintes` blokk a `Teremtéstan + Eszkatológia` értéket önálló
  témafejlécként kezeli, ahelyett hogy a motívumot mindkét téma (vagy az
  első) alá sorolná.

- **N25 — a „teremtés-visszavonás” kifejezés rendezése.** *(ÚJ,
  TEREMT002_KUTATAS_BRIEF T1.3, 2026.09.25)* A TEREMT-002 címe a gate-döntés
  óta „a föld kietlen és puszta állapota a teremtéskor és az ítéletkor”; a
  régi kifejezés előfordulásai (listájuk a T1.3 jelentésében: napló „Lásd
  még”, changelog, HAMART-001-napló és -lexikon, a brief, a T1-naplók) a T3
  prózájában rendezendők.

- **N26 — a shell-szabály gépi kényszerítése.** *(ÚJ,
  TEREMT002_KUTATAS_BRIEF T1–T2, 2026.09.25)* A „héber/görög/magyar szöveget
  tartalmazó kód csak fájlból” szabály (CLAUDE.md, Shell) a TEREMT-002
  menetekben kétszer sérült heredocba ágyazott Pythonnal — egy hook (pl. a
  `python -` / `<<` + nem-ASCII minta tiltása) gépivé tehetné.

- **N27 — Nave: a `basokant/nave` létezik.** *(ÚJ, FJ-ellenőrzés, 2026.09.25)* Az FJ4 „nem
  létezik” állítása hibás (a `git ls-remote https://github.com/basokant/nave` a `main` ágat
  visszaadja; a cloud proxy okozhatta). A Nave-forrás felmérése helyi gépről ismétlendő, a
  `basokant/nave` adatforrásával együtt.
  **LEZÁRVA (F18, 2026.09.30, javaslat-állapotban):** DT5 szerint a `basokant/nave` nyers szövege
  importálva saját parszolóval (`konkordancia/Nave_basokant.tsv`, 85 246 sor, 5 322 téma); a `theonize`
  nem került be. Napló: `naplok/F18_import_naplo.md`, `naplok/F18_licenc.md`. Nyitva marad: teljes
  független kiadás-összevetés (letöltés-engedéllyel) — l. DONTESEK DT29.
- **N45 — Nave_basokant: maradék jelöletlen hivatkozás-töredékek.** *(ÚJ, F18 4. ellenőri kör, 2026.09.30)* Jelöletlen, számmal nyilvántartott maradék a `konkordancia/Nave_basokant.tsv`-ben: (a) `REVERENCEGe 35:5` (NAVE-4148): az 1Móz 35:5 nem lett sor, a töredék 153 sor `cimke` mezőjébe öröklődik; (b) 19 könyv nélküli folytató-hivatkozás `</ref>; N:N.` alakban (nyers forrás 20238 ×2, 20494 ×16, 21842), 22 sor `cimke`-je, egyik sem lett sor; (c) SATYR `utotag:34:14.` (Ézs 34:14); (d) 8 `with N` fejezetszám-folytatás (TSV-fájlsor 5263, 30166, 37102, 38336, 38737, 38741, 52628, 73970). Javaslat: külön javító menet; az import addig `javaslat`-állapotú. Napló: `naplok/ELLENOR_F18.md` 4. kör, DT29.

- **N28 — az FJ2 versszámozási következtetései felülírva.** *(ÚJ, FJ-ellenőrzés, 2026.09.25)*
  A `F01_KAROLI_KULCS_BRIEF.md` 0. pontja szerint nem tartható: a Jón 2:3 → LXX 2:4 javaslat, a
  „hiányzó fejezetek” diagnózis és a „Károli-kulcsú tábla nem szükséges” következtetés. Az
  adat megvan, a Károli-kulcs üres (`karoli_ok=szamozas_elteres`). A téma gazdája a KK-menet;
  a `naplok/FORRAS_FJ2_*` fájlok csak történeti érvényűek.

- **N31 — a Macula Hebrew lefedettsége ellenőrizendő.** *(ÚJ, FJ-ellenőrzés, 2026.09.25)* Az
  FJ1 szerint a letöltött Macula Hebrew-ből hiányzik az 1Sám–2Krón. Ez valószínűleg letöltési
  vagy feldolgozási hiba; a küszöb alatti eredményen nem változtat, de bármilyen későbbi
  használat (pl. a G8 tagmondat-tagolás) előtt ellenőrizni kell.
  **LEZÁRVA (F17, 2026.09.30):** a hiány nem valós — az F06 mérése és az F17 importja szerint az
  1Sám–2Krón mind a hat könyve megvan (929 lowfat-fájl, 475 911 morféma-sor, `konkordancia/Macula_heber_*.tsv`, 39 könyvfájl);
  az FJ1 hibája a fájlnév-minta volt (a számjeggyel kezdődő könyvkódot nem illesztette). A Macula–TAHOT
  verslista-eltérések oka (F06) továbbra sincs vizsgálva; l. `naplok/F17_import_naplo.md`.

- **N32 — a commitolt `lexikon/*_TUDOMANYOS.md`/`*_TORZSCIKK.md` elavult a
  KK7.5 (Károli-versszám-javítás) és a D16 (Cremer kivezetve) óta.**
  *(ÚJ, SZOTAR D30 ellenőrzés, 2026.09.28)* A `general.py --cel lexikon
  --ir` és `--cel torzscikk --ir` friss futása (azonos adaton, csak a
  committolt fájlokhoz képest) valódi, nem dátum-jellegű eltérést ad: több
  LXX-sor `szamozas_elteres` → `egyező` vált (pl. Jón 2:3, Jón 2:6, Ézs
  63:13), és a törzscikkek szerepmátrix-sora még mindig `Teológiai szócikk |
  Cremer (1895)`-t mutat a mai `nincs (Cremer kivezetve, SZOTAR D16)` helyett.
  A pótlás a #9 (SZOTAR S2, teljes újragenerálás) feladata — nem önálló
  tétel, csak dokumentálva, hogy az S2 zárásakor ez is bekerül.

- **N33 — a CI (`ellenorzes.yml`) nem futtatja a `general.py`-t, csak az
  `ellenoriz.py` sértés-alapú szabályait (E1) és a diff-alapú E2–E16
  szabályokat.** *(ÚJ, SZOTAR D30 ellenőrzés, 2026.09.28 — javaslat, nincs
  döntés)* Emiatt sem a TEREMT-002 `res_forras.tsv`-hiánya (a `general.py
  --cel lexikon --ir` kivétellel megszakadt volna bármely PR-en, amely ezt
  a fájlt érinti), sem az N32 render-drift nem jelent meg CI-hibaként. Egy
  jövőbeli CI-szabály (pl. `general.py --cel lexikon --ellenoriz` +
  `--cel torzscikk --ellenoriz` futtatása minden PR-en) elkaphatná — ehhez
  a `PARDES_DATUM` rögzítése is kellene, hogy a dátum-mező ne adjon hamis
  pirosat.

- **N35 — a `kiejtes_szabalyok.tsv` `Y`/`y` szabálya (D33, MCGED-konvenció)
  gold-párral még nincs igazolva.** *(ÚJ, SZOTAR S1.4, 2026.09.28)* Az
  `U`/`u` ágat az S1.3 26/26 aranyparja validálta (TAGNT/TBESG-forrás); a
  `Y`/`y` ág csak a `kiejtes.py --onteszt`-tel van ellenőrizve (egyetlen
  kézi példa, `kyrios`→`kürion`... helyesebben `kyrios`→`küriosz`, nem
  gold-készletből). Ha a `konkordancia/MCGED_teljes.tsv` `atirat` mezője
  valaha render-be kerül (S2), előbb egy MCGED-specifikus arany
  párkészletet kell összeállítani (hasonlóan a
  `naplok/SZOTAR_S1_kiejtes_arany_sbl.tsv`-hez) és azzal validálni.

- **N36 — a `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv` 12 görög
  "arany" sora csonkolt (hiányzik az első, ékezetes/lehelet-jeles betű).**
  *(ÚJ, SZOTAR S1.3 ellenőrzés, 2026.09.28)* Pl. `γκαλέω` `ἐγκαλέω`
  helyett, `νομάζω` `ὀνομάζω` helyett — egy korábbi (S0-előtti)
  másolási/kódolási hiba a tesztkészletben, nem az S1.3 vagy S1.4
  bevezetése. A próbát nem érintette (a
  `naplok/SZOTAR_S1_kiejtes_arany_sbl.tsv` a helyreállított alakot
  használja, `megjegyzes` oszloppal jelölve, l. `naplok/
  SZOTAR_S1_kiejtes_jelentes.md` 5. szakasza). **Javaslat, nem döntés:**
  a gold-tábla saját maga javítható lenne, de más menetek (K10, RENDER)
  saját mérési alapja is, ezért csak jelzésnek szánt tétel.

- **N37 — nincs egységes Strong-kód-normalizáló függvény a projektben
  (`#4/1d`).** *(ÚJ, SZOTAR S1.4 ellenőrzés, 2026.09.28, a felhasználó
  kérésére, l. a #4/N21 kapcsán)* A `F04_KARBANTARTAS_BRIEF.md` §3 saját
  `1a`/`1b`/`1c` sorozatának (KB1 = `__main__`-őr+argparse, KB2 =
  CRLF-tűrés, KB3 = `1c`, N21: a `Karoli_Strong_kivonat.tsv` nullázatlan
  Strong-számainak javítása) **logikus folytatása — `1d`**: legalább 7
  önálló Strong-normalizáló implementáció létezik: `eszkozok/
  lxx_kivonat_fetch.py normalize_strong()`, `lxx_osszevetes.py
  normalize_strong()`, `merge_karoli_szofaj.py normalize()`,
  `oshl_index_import.py strong_from_attr()` (mind korábbi), és az S1.4
  négy új szkriptje (`ubs_dbh_import.py`, `mcged_import.py`,
  `lxx_versszintu_import.py`, `tw_import.py`) — mindegyik saját
  logikával. Ugyanaz a hibaosztály, mint az N21: decentralizált
  Strong-kezelés, ahol a padolási/csonkolási hiba könnyen észrevétlen
  marad — pontosan ez történt a `tw_import.py` első verziójával
  (`G00120` → tévesen `G0120`, l. `naplok/SZOTAR_S1_4_jelentes.md` 7.
  szakasza), mielőtt a keresztellenőrzés kifogta. Javaslat: egy közös
  `eszkozok/strong_util.py` (vagy hasonló) modul, amit minden import
  átvesz. **A `#4` (KARBANTARTAS KB0–KB4) már lezárt és mergelt**
  (`b8a418a`, 2026.09.27), ezért ez a tétel nem élesztette újra azt a
  menetet — a `F04_KARBANTARTAS_BRIEF.md` §5 döntésnaplója rögzíti az
  eltérést (miért N-tételként, nem élő KB5-ként fut). Ez a tétel maga NEM
  végzi el a konszolidációt (kívül esik az S1 hatókörén), csak jelzi;
  jövőbeli önálló karbantartás-menet tárgya.

- **N39 — a héber kiejtés-jelölt szabálytáblában nincs szabály a számek
  (`s`, ס) és a szin (`ś`, שׂ) megkülönböztetésére.** *(ÚJ, SZOTAR S1
  javítókör (F05b), 2026.09.29, `naplok/ELLENOR_SZOTAR_S1.md`)* A görög
  szabálytábla `s→sz`-t alkalmaz mindenre, a héber táblában ez a
  megkülönböztetés hiányzik — pl. H3678 (כִּסֵּא) jelöltje „kissé”,
  magyar ejtéssel [kiʃːeː], holott a szó tartalmaz szamek-et. **Felhasználói
  döntés kell:** vezessünk-e be külön `ś`-szabályt (az OSHL-atirásban
  ez `ś` karakterként jelenik meg, ha a forrás egyáltalán megkülönbözteti),
  vagy maradjon az egységes `s`. Nem blokkolja a jelenlegi 26 jóváhagyott
  jelöltet (egyik sem tartalmaz `ś`-t). **Ugyanez a hiány a `w` (vav)
  betűre is fennáll** — nincs külön szabály rá, a `naplok/
  ELLENOR_SZOTAR_S1.md` 1. körének megfigyelése szerint (jelen jelöltek
  egyike sem érintett, de a `w` az OSHL-atirásban is előfordulhat).
- **N40 — a H2403 (חַטָּאָה/חַטָּאת) OSHL-homográf-választása indoklás
  nélküli.** *(ÚJ, SZOTAR S1 javítókör (F05b), 2026.09.29)* A
  `heber_kiejtes_jeloltek.py` a fájl-sorrend szerinti ELSŐ OSHL-sort
  választja (חַטָּאָה, „chattáá”), de a gyakoribb címszó a חַטָּאת (a BDB
  szócikk-feje is ezt adja). **Felhasználói döntés kell**, hogy ez a
  választás maradjon-e, vagy a gyakoriság/BDB-cím alapján váltson.
- **N41 — a `spirantize()` (héber begadkefat-átírás, D34) latens
  geminációs hibája.** *(ÚJ, SZOTAR S1 javítókör (F05b), 2026.09.29)* A
  függvény karakterenként lépked a döntéslistán; egy geminált
  begadkefat-pár (pl. `bb`/`pp`/`kk`) második karaktere tévesen a
  KÖVETKEZŐ ב/כ/פ döntését fogyasztaná el (példa: egy `rabbāb`-ból
  `rabvāb` lenne). A jelenlegi 26 jóváhagyott jelölt között nincs ilyen
  eset, de egy jövőbeli bővítésnél (pl. a #9 render vagy egy új
  motívum-token) hibát okozhat. Javítás: a döntéslista indexelését a
  betű saját pozíciójához kell kötni, nem sorrendi fogyasztáshoz.
- **N42 — nincs rögzített lemma-választási szabály az `alap_strong`
  szerint csoportosuló TBESH-sorokra.** *(ÚJ, SZOTAR S1 javítókör (F05b),
  2026.09.29, `naplok/ELLENOR_SZOTAR_S1.md`)* A betű-utótag-javítás
  (D38) után egy alapszámhoz (pl. H2416) akár öt különböző, saját lemmájú
  betű-utótagos sor is tartozhat. Ma nincs downstream fogyasztó (a
  generátor még nem olvassa a `TBESH_konszolidalt.tsv`-t), de **ez a
  `#9` (SZOTAR S2, render) előfeltétele**: mielőtt a render alapszám
  szerint lemmát/kiejtést jelenítene meg, dönteni kell, melyik
  betű-utótagos sor lemmáját mutassa (vagy mindet, felsorolva).
- **N-F33a — a SECE_G "LN:" (Louw–Nida) és "GK:" mezői ne kerüljenek a renderbe.** *(ÚJ, F33 / DT-F33h, 2026.10.04)* A `konkordancia/SECE_G_teljes.tsv` 5 406 szócikkében "LN:" (Louw–Nida szám, UBS), 5 506-ban "GK:" (Goodrick–Kohlenberger szám) jelölés áll; a modul készítőjének (Eliran Wong) "public domain" nyilatkozata ezekre a hozzáadott leképezésekre külön nem terjed ki, a jogosultságuk nem igazolt (`adat/licencek.tsv` SECE_G sor, `javaslat:`). **A `#9` (SZOTAR S2, render) szabálya:** a SECE_G szócikk-szövegét a render az LN- és GK-jelölések nélkül jeleníti meg (lexikonoldal, törzscikk). Felhasználói döntés (2026.10.04): gépi védelem nem épül, a megjegyzés és ez a tétel elég; a `#9` brief befogadásakor vagy futtatásakor ellenőrizendő. **Tisztázott forrás az LN-hez (felhasználói döntés, 2026.10.04):** ha a renderben Louw–Nida hivatkozás kell, az az UBS-adatból jön, nem a SECE_G-ből: `konkordancia/SDGNT_domenek.tsv` / `UBS_DNTG_*` (`entry_kod` = Louw–Nida hivatkozás, pl. `33.98`; `konkordancia/SDBH_SDGNT_README.md` 149. sor), CC BY-SA 4.0 © United Bible Societies, kötelező forrásmegjelöléssel (a README idézi), share-alike hatása a kimenetre külön jelölendő (SEMA 2.19 1. szabály). Korlát: az UBS-adat nem 1:1 a SECE LN-jével, hiány lehet; üres érték nem negatív lelet (CLAUDE.md). A GK-szám (Goodrick–Kohlenberger) nem kerül a renderbe, pótló tisztázott forrása nincs. **Mérés (DT-F33i, 2026.10.04):** a SECE_G 5 406 LN-es sorából 5 050 (93,4%) LN-kódja teljesen az UBS `entry_kod`-halmazban van, 245 (4,5%) részben, 5 sornál nincs közös kód, 106 sornál (2,0%) a Strongnak nincs UBS-sora; az UBS-adat egyes kódjai betű-utótagosak (`93.4a`) vagy `{N:001}` jelölésűek, ezeket a render az egyeztetéskor normalizálja.
- **N-F33b — a `#9` (SZOTAR S2, render) kereskedelmi módja: a `kereskedelmi=nem` forrásokat kihagyja.** *(ÚJ, F33 / DT-F33j, 2026.10.04)* A kimenetnek két változata lehet: **nem kereskedelmi** (a mostani, bevétel nélküli projekt: minden forrás, megjelöléssel) és **kereskedelmi** (csak azok a források, amelyek a `licencek.tsv` `kereskedelmi` oszlopa szerint `igen` vagy megfelelően `feltetelesen`). A render a `kereskedelmi` oszlopot a `licencek.tsv`-ből olvassa (nem kézi mező-listából); kereskedelmi módban a `kereskedelmi=nem` (MCGED, Heber_ETCBC_modulok) és a `tisztazatlan` forrásokból származó mezők kimaradnak. A kimaradó adatra tisztázott pótlás van: a héber morfológiát és előfordulást a TAHOT/TAGNT (CC BY 4.0), az LN-t az UBS SDGNT (CC BY-SA 4.0, DT-F33i) adja; a CC BY-SA források (LSJ, UBS) kereskedelmi kiadásban is szabadok, de a share-alike a kiadásra is vonatkozik (külön jelölendő). A mező-proveniencia (melyik forrásból jön) a render része. A leltár nem jogi vélemény; kereskedelmi kiadás előtt jogász.
- **N43 — a CI E5-szabály `TÖRLÉS-SZÁNDÉKOS:` jelölése PR-szinten
  globális, nem címsoronkénti.** *(ÚJ, SZOTAR S1 javítókör (F05b),
  2026.09.29)* Egyetlen jelölés a PR összes törölt címsorát felmenti,
  akkor is, ha a PR több, egymástól független szándékos törlést
  tartalmaz. Ez CI-tervezési kérdés (`eszkozok/ellenorzes/szabalyok.py`
  `SZANDEKOS_JELOLES_MINTA`), nem egy konkrét PR hibája — javaslat:
  címsoronkénti vagy fájlonkénti jelölés bevezetése egy jövőbeli
  karbantartás-menetben.
- **N44 — commit-fegyelem: ékezet nélküli commit-üzenetek és WIP-commit
  a SZOTAR S1 menetben (K8).** *(ÚJ, SZOTAR S1 javítókör (F05b),
  2026.09.29, `naplok/ELLENOR_SZOTAR_S1.md`)* A `fuggetlen-ellenor`
  mindkét körben jelezte, hogy a menet commitjai (a `cfa7d0d` WIP-pel
  együtt) ékezet nélküliek — ez sérti a CLAUDE.md `git log --grep`
  kereshetőségi elvét. A menet ezen a ponton már túl van a javításon
  (a git history nem írható át visszamenőleg, l. a projekt szabálya, hogy
  csak új commit készül, nem amend/rebase); a tétel a JÖVŐBELI menetekre
  vonatkozó emlékeztető.
- **N46 — a Károli-kulcs (KK) 44 Károli-verse eltolódás-gyanús, a Macula-
  illesztésben üres `karoli` értékkel.** *(ÚJ, F17 (#17) 3. kör, F17.6,
  `naplok/F17_import_naplo.md`, `naplok/F17_illesztetlen.tsv`, `naplok/ELLENOR_F17.md`)*
  A `LXX_versificacios_terkep.tsv` `EGYIK_SEM` fejezeteinél az identitás
  egy verssel elcsúszott értéket adott volna (pl. `karoli "Préd 5:1"` = MT 4:17,
  `karoli "4Móz 30:1"` = MT 30:2), ezért a `karoli` mező üres, a sor
  `javaslat:terkep_egyik_sem_eltolodas_gyanu`. Érintett: Préd 5:1–20,
  4Móz 30:1–16, Zsolt 13:1–6, 4Móz 26:1, Zak 3:1 (44 Károli-vers; az MT-oldalon
  megfelelő Károli-vers nélkül maradnak). A Károli-kulcs (`konkordancia/
  Karoli_versmegfeleltetes.tsv`) sorait kell rájuk kiegészíteni vagy
  igazolni (KEZI-osztály, fejezetenkénti KJV=MT ellenőrzéssel, mint az
  `naplok/F17_kezi_fejezetek.tsv`-ben). A felvételt a chat jóváhagyta
  (2026.09.30).
- **N-F08a — a Préd 9:10 előfordulás-sor (ALVIL-001) igehelyének javítása
  Préd 9:12-re.** *(ÚJ, F08 (#8), DT23 (c), DT7 (g); `naplok/F08_zaras.md`)*
  A munkalap-igehely MT/KJV-számozású: a Károli Préd 9:10 = MT 9:8 (KK, KEZI),
  a שְׁאוֹל a Károli 9:12-ben (MT 9:10) áll, ahol a Macula ἅδη G0086 és az
  `LXX_OS` ᾅδης egyezik. A javítás az `adat/elofordulasok.tsv` ALVIL-001
  sorát érinti; utána az `adat/lxx_dontesek.tsv` LD008 sora tárgytalan (az
  ALVIL-001 G-tokenje G0086, a 9:12 várhatóan „egyező” lesz, döntési sor
  nélkül). A felvételt a felhasználó a DT23-ban jóváhagyta (2026.09.30).
- **N-F08b — saját címke a `nincs_heber_kulcsszo` sorokra a lexikon-
  generátorban.** *(ÚJ, F08 (#8), DT23 (e); `adat/SEMA.md` 2.11)* Az
  `adat/lxx_dontesek.tsv` 8 `nincs_heber_kulcsszo` / `nem_alkalmazhato` sora
  (ige-tartományú előfordulás-sor kulcsszó nélküli verse, ill. tematikus sor)
  ma „kutatói azonosítás függőben”-ként jelenik meg. A `lexikon_general.py`
  `blokk_lxx` kapjon saját „kulcsszó nincs a versben” címkét (és számlálót),
  a SEMA 2.11 megjelenítési mondata ehhez igazodjon. A felvételt a
  felhasználó a DT23-ban jóváhagyta (2026.09.30).
- **N-F46a — a BDB könyvfeloldási kézi lista (779 sor): kézi döntés.**
  *(ÚJ, F46 (#46), DT-F46 (2) b; `naplok/BDB_KONYVFELOLDAS_kezi.tsv`, `naplok/BDB_KONYVFELOLDAS_naplo.md`)*
  Az F46 gépi cseréje (DT-F46 és kiegészítései) 253 forrás-tokent (250 igehely + 3 névhiba, 197 szócikk) és
  54 fordítás-tokent (39 sor) javított; a többi jelölt szövegkörnyezettel a kézi listán (779 sor): 296 + a
  DT-F46 miatt kézire tett 55 + a kiegészítés 2 szerint visszaállított 16 = 367 sor javaslattal (a 34
  „más könyv érvényes fejezettel” `kozepes`, a 18 >500 előfordulású Strong — köztük a H8034
  `Dan 22:14/22:19` → 5Móz és a H0413 `Deut 37:36` → 1Móz —, a 3 azonos célú H5656-sor), a
  többi javaslat nélkül (több egyenrangú jelölt, nincs igazolt jelölt, láncolt lehetetlen hely 96,
  jelentésszám tapadt 12, H3117 téves névhiba-jelölt). A 13. kapu forrásoldali 63 megmaradt
  jelzése mind ezen a listán áll. Teendő: döntés soronként vagy blokkban (a nyomtatott BDB
  alapján). A kézi lista pozíciói a jelenlegi (F46.14 utáni) forrásra vonatkoznak; a cserenapló
  (`naplok/BDB_KONYVFELOLDAS_csere.tsv`) pozíciói a 3.6 előttire, ezért az `eszkozok/bdb_konyv_javit.py
  --ir --dt-f46` a mostani forráson nem futtatható újra (a pozíció-kapu megáll). A jóváhagyott kézi sorok
  cseréjéhez a szkriptet a `kezi.tsv` pozícióira kell bővíteni (ugyanazzal a mezőkulcsos, pozícióhoz kötött
  cserével és a Károli-létezés + Károli-vers Strong-kapuval, ablak 0); a `--dt-f46-szures` újrafuttatása
  a commitolt állapotot adja (idempotens, F46.17).
  **Számozás (DT-F46 kiegészítés, 2026-10-03, eldöntve):** a forrás MT-számozású marad, a `javasolt_karoli_alak`
  Károli-számozású (H2204, H7871 → 2Sám 19:32; H2938 → 2Sám 19:35; H7138 → 2Sám 19:42; H3940 → Náh 2:4;
  H1932 → Dán 6:26), a fordításba nem került csere. A Károli-vers Strong-kapuja (DT-F46 kiegészítés (2)) a
  pontos Károli-versben 16 már cserélt sort nem igazolt; a DT-F46 kiegészítés 2 szerint ezek visszaálltak a
  forrásban és a fordításban (F46.14), és a kézi listára kerültek (`dt_f46 = kezi`, a TAHOT szerinti szomszédos
  vers a javaslat-oszlopban; lista: `naplok/BDB_KONYVFELOLDAS_naplo.md` F46.14).
  *Helyőrző: a végleges N-számot az Action osztja ki.*
- **N-F46b — a `eszkozok/teszt_bdb_zaras.py` korábbi hibái (2 FAIL + 1 ERROR).**
  *(ÚJ, F46 (#46), DT-F46 kiegészítés (5); `naplok/BDB_KONYVFELOLDAS_naplo.md` 3.6)*
  `test_dtf38g_kezi_javitasok` (FAIL: H5674), `test_szellem_tabla_nagybetus_helyei` (FAIL: H5674 nagybetűs
  `Szellem`), `Zaras3Idempotencia.test_ir_ketszer_futtatva_nem_duplikal` (ERROR). A hiba az F46 előtti
  HEAD-en is fennállt (az F46 változtatásai nélkül ugyanígy bukik), tehát nem az F46 okozta. Teendő: az
  ok felmérése (a H5674 sora és a zárás-szkript idempotencia-tesztje) és javítás, külön menetben.
  *Helyőrző: a végleges N-számot az Action osztja ki.*
- **N47 — a feladatszámból képzett régi DT-számok és az árva helyőrzők.** *(ÚJ, F30 (#30), SZ.0/SZ.4, 2026.10.05)*
  (1) A DT18 (#18 Nave) a feladatszámból képzett hibás szám volt; DT29-re számozva (`DONTESEK.md`). A DT19 sora (`#19 KJV/ASV-import`) szintén a feladatszám alakját viseli, és a régi F21-pilot-kimenetekben a „DT19” az F21 sorára (ma DT-F21h) is utal: ütközés. Átszámozását az F30 nem végezte el (nem a brief tárgya); az orkesztrátor döntse el.
  (2) A lezárt ellenőri jelentések (`naplok/ELLENOR_*.md`) és a `naplok/F16_zaras.md` a DT18-at változatlanul tartalmazza (a DONTESEK-sor megjegyzése jelzi).
  (3) 17 árva helyőrző (hivatkozás definíciós sor nélkül; pl. DT-F16, DT-F17, DT-F22, DT-F28, N-F38a–c): a `szamkiosztas` nem számozza, mert nincs hová; a lezárt döntések helyőrzőinek rendezése nyitott.
  (5) Egyeztetett eltérés (F30): a brief `ir` listája az `eszkozok/ellenorzes/futtat.py`-val, a `eszkozok/ellenorzes/tesztek/test_szamkiosztas.py`-val, az `eszkozok/szamkiosztas_oroklott.txt`-vel és a `naplok/F30_*` fájlokkal bővül (az E26 bekötése, tesztje, az örökölt lista). Az `ir` listán kívül csak a DT18→DT29 csere történt (F18 brief, `adat/SEMA.md`, `adat/datasetek.tsv`, `naplok/F18_*`); a base..head diff ezt igazolja.
  (4) A `szamkiosztas.yml` és az E26 az `eszkozok/ellenorzes/`-t és a `.github/`-ot érinti: a PR címének `[ELLENŐRZŐ]` előtaggal kell kezdődnie (E16).

- **N-F34b — a TAHOT-kivonat „nem teljes” állítás elavult (CLAUDE.md,
  `konkordancia/README.md`); a valódi hiány kicsi.** *(ÚJ, F34 (#34), DT-F34b 3. pont)*
  A `konkordancia/TAHOT_TAGNT_README.md` (195., 316., 320. sor) szerint az 1Móz 32,
  Zsolt 88/89/90/140/142 hiánya már pótolt; az F34 mérése ezt megerősíti
  (Zsolt: 150/150 fejezet, 2527/2527 MT-vers, a Macula-táblához mérve nincs hiányzó
  vers; az egyetlen fejezet-szintű rés: Jób 41; mérés + proveniencia-sor: `python eszkozok/bdb_psi_javit.py --meres-tahot`, `naplok/F34_M2_naplo.md` F34.6/3.). Javítandó: a `CLAUDE.md` „Adat-tár”
  szakasza („TAHOT_kivonat.tsv nem teljes … hiányzik legalább 1Móz 32, Zsolt
  88/89/140/142, Jóel 3”) és a `konkordancia/README.md` ide vonatkozó sora — a
  Jób 41 és az esetleges vers-szintű rések (Jóel 3 külön mérendő) pontos
  hiánylistájával. *Helyőrző: a végleges N-számot az Action osztja ki.*

- **N-F21 — Károli ↔ KJV versmegfeleltetés: zsoltárfeliratok, 1039 ÓSZ-vers, F19-tábla.** *(ÚJ, F21 regressziós mérés, KJV-szabály mérése, 2026.10.01, `naplok/F21P_elopar_kjv.md` 5. pont, `naplok/F21P_kjv_meres.md`; a számot (N-F21) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  A `konkordancia/Karoli_versmegfeleltetes.tsv` `igehely_kjv` oszlopa (főleg az `osztaly=MT` soroknál) az MT-versszámot adja a KJV-szám helyett, ezért a `konkordancia/KJV_Strongs_teljes.tsv` (F19) KJV-támpontja ezeknél a verseknél a rossz KJV-versről jön. A teljes ÓSZ-ben 22 730 KJV-soros versből 1162 gyanús (a vers jól címkézett Strongjainak kevesebb mint fele van a KJV-sorban); ebből 1039-nél a szomszéd KJV-vers illik: Zsolt 915 (a zsoltárfeliratok: pl. Zsolt 18:1 a KJV 18:0-hoz illik), Ézs 42, Préd 24, 1Sám 20, Hós 13, Jón 9, 4Móz 8, 1Kir 6, Dán 2. A Zsolt 6:5, 13:2, 18:1, 18:3, 59:8 az F21 arany 60 versében is szerepel.
  **Érintett:** a versmegfeleltetési tábla, a `tokenek.kjv_tamapont_teljes` (és minden fogyasztója), az F21 F8V3 mérés R2-je (a zsoltárversek KJV-támpontja). **Állapot:** nem javítva (a felhasználó döntése: most ne javítsd). Az F8V3 megismétlése a javítás után jön, külön döntéssel (kb. 0,26 USD). A javítás hatóköre (F19 tábla vs. a megfeleltetési tábla) nyitott.
  *Kapcsolódó nyitott pont (az N-F21 alatt, 2026.10.01, F21 utómunka; az ellenőri 6. kör 13b megjegyzése):* a `futtat.py` helyi éles-hívás tiltásának (`GITHUB_ACTIONS=true` vagy `F21_ELES_HELYI=igen`; a véletlen helyi F8V3-futás után, `naplok/F21_baleset_F8V3.md`) **nincs öntesztje**; ugyanitt: a `meres.py`, `jelentes_f21p.py`, `ingadozas.py` és `szuroproba.py` nem támogat valódi `--onteszt`-et, a futtatásuk követett kimeneteket ír át (a régi kimenetek a main-hez képest 0 diffek, a mellékhatás helyreállt, de a csapda megmaradt).
  *Kapcsolódó (nem tétel):* az ÚSZ-hez nincs Károli → KJV kulcs (a megfeleltetési tábla csak az ÓSZ-t fedi); a felhasználó döntése szerint most nem kell; az F21 jelentésében az R4: „KJV nélkül, nem mérhető”.

- **N-F22a — Névadó versek javítómenete (a „mindkettő” konvenció): a magyarázó szó a saját tövéhez és a név szavaihoz is kötődik.** *(ÚJ, F22 1Móz, DT-F22b 3. pont, 2026.10.01, `naplok/F22_DT-F22b_javaslat.md`; a számot (N-F22a) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  Nem promptszabály, hanem későbbi, külön javítómenet a névadó versekre (1Móz 5:29, 16:11, 16:13 mint kiinduló esetek). Feltétel: a Károli-szöveg kimondja a névadást, és a név a versben áll. **Az 1Móz 16:11 aranyát (H3458, csak a név) ehhez a konvencióhoz kell igazítani**, mert az arany a három esetben nem egységes. A `prompt_v3` változatlan marad.

- **N-F22b — Gemini-újrapróba versszintre szűkítése. LEZÁRVA (elvetve), 2026.10.01.** *(ÚJ, F22 1Móz, felhasználói kérés 2026.10.01; a számot (N-F22b) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  **Lezárás (felhasználó, 2026.10.01):** „Az újrapróba már ma is csak a hibás versekre kér választ. Csak az újrapróba költsége csökkenthető (19%), ez a teljes Biblián néhány USD, nem éri meg a lánc módosítását.”
  „Gemini-újrapróba versszintre szűkítése (csak a hibás versek mennek újra), várható megtakarítás 25–35%. Csak akkor, ha a Gemini a DT-F22c után is marad; legkorábban a Mózes öt könyve után.”
  *Mérési megjegyzés (az `f22/futasnaplo.tsv` 1Móz-adataiból, `scope=manual`, nem a tétel része):* a `futtat.py` újrakérése már ma is csak a hibás versekre kér választ, de az első kérés teljes szövegét és a hibás választ is előzményként küldi; ezért az újrapróba bemenete nagyobb (646 797 token / 62 hívás, kimenet 27 380), mint az elvetett első próbáké (519 833 / 97 193). Az újrapróbák összköltsége 0,4363 USD, a napló 2,2720 USD-jének 19,2%-a; ennyi a megtakarítás elvi felső határa a 1Mózes költségén, tehát a 25–35% a teljes költségre nem érhető el; az elvetett első próbák 0,7543 USD-je (33,2%) a kapuhibás hívások ára, nem az újrapróbáé. A tétel döntésekor ezt a kiindulást kell a várt megtakarítás mellé tenni.
- **N-F17a — a Macula-kötés többi `EGYIK_SEM` fejezetének kézi feloldása.** *(ÚJ, F17 javító menet, DT7 (c), 2026.10.02, `naplok/F17_import_naplo.md` F17.J; a számot (N-F17a) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  A Dán 3–4 identitás-kötése megtörtént; a többi `EGYIK_SEM` osztályú fejezet (2Móz 35–36, Hós 2, 13, 14, Jób 17, 37 stb.) Károli–MT kötése kézi feloldásra vár. Az interpoláció (40 vers) `javaslat` marad.

- **N-F17b — a Macula héber funkció-kódjainak leképezése a STEP 9000-es sávjára. Alacsony prioritás.** *(ÚJ, F17 javító menet, DT7 (b), 2026.10.02; a számot (N-F17b) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  A 170 429 funkció-morféma sor Macula-azonosító (`strong_x`), nem Strong-szám; a leképezés külön feladat.

- **N-F35a — a Macula-generátor Sir/JSir aliasának törlése a #35 lezárása után.** *(ÚJ, F17 javító menet, 2026.10.02; a számot (N-F35a) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  A generátor a régi `Sir` könyvnévtől függött: a Károli-oldali adatok még `Sir`-t, a könyvtábla már `JSir`-t használ. A kétirányú alias az `eszkozok/f17/macula_kozos.py`-ban (`ALIAS`, `kanoni_nev`, `RAW_NEV`) és a használói (`macula_kk.py`, `macula_import.karoli_cimke`) törölhető, ha a Károli-adat átnevezése megtörtént; utána a `Macula_heber_Siralmak.tsv` újragenerálása a `JSir` címkével.

- **N-F41a — a Károli-kulcs (KK) `igehely_kjv` oszlopa nem megbízható KJV-számozás.** *(ÚJ, F41 (#41) 3.1–3.5, `naplok/F41_bsb_megfeleltetes.tsv`, `eszkozok/fj2/bsb_verseltolas_diag.py --f41`; a számot (N-F41a) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  A `konkordancia/Karoli_versmegfeleltetes.tsv` `igehely_kjv` oszlopa a `KJV` osztályú soroknál (20 927 sor) mindig azonos a Károli-hivatkozással, az `MT` osztályúaknál 1561/1713 sorban, a `KEZI` osztályúaknál 93/291 sorban (`scope=manual`: a menet saját összevetése, ts=2026-10-02) — vagyis az oszlop a Károli-hivatkozás másolata, nem független KJV-adat. Példa: `Jón 2:1` → `igehely_kjv=2:1`, holott a Károli Jón 2:1 a KJV 1:17-e (a Strong-illeszkedés szerint a BSB 1:17 = TAHOT 2:1). A BSB (KJV-számozás) → TAHOT_kivonat Strong-illeszkedés ellentmond a kulcsnak: 4Móz 16, 1Sám 22, 1Kir 6, Zsolt 921, Ézs 46, Hós 14, Jón 10 sorban (összehasonlítva a `KJV`/`MT` osztályú sorokat, ahol a BSB-vers szerepel). Javítás: a KK-tábla gazdájának dolga (N46 érinti: Préd 5, 4Móz 30, Zsolt 13); az F41 nem javít.
- **N-F41b — CI-szabály-javaslat: a `BSB_Strongs.tsv` „Angol szó állapota” oszlopának gépi ellenőrzése.** *(ÚJ, F41.4, javaslat; a számot (N-F41b) a main-Action osztja ki)*
  Az `eszkozok/fj2/bsb_import.py` a futása végén ellenőrzi (üres „Angol szó” csak `elhagyva` / `ures_jelzo_nelkul` állapottal; 6 oszlop minden sorban; a darabszámok egyeznek a napló `angol_szo_allapot` sorával), de CI-szabály nem védi a commitolt fájlt. Javaslat: E-szabály, amely a commitolt `BSB_Strongs.tsv`-ben ugyanezt ellenőrzi. Az F41 CI-szabályt nem ír. (F41.7, F41.10, F41.12: a fájl azóta 7 oszlopos; a `Számozás` oszlop értékei `mt` / `kjv` / `ellenorizetlen` (a korábbi `tahot_szamozas` / `kjv_szamozas` megszűnt): az E-szabály ezt is ellenőrizze.)
- **N-F41d — a `TAHOT_kivonat.tsv` versszámozása vegyes: egyes könyvekben KJV-, másokban a masszoréta (Macula/WLC) számozást követi; az F41 `mt_vers` (megfeleltetés) a TAHOT_kivonat számozására illesztett; a `BSB_Strongs.tsv` `Igehely` célszámozása az MT (WLC), a 7. oszlop (`Számozás`) mutatja a WLC-vel való igazoltságot (`ellenorizetlen` = a WLC-vel egyértelműen nem igazolt, nem „TAHOT-hibrid számozás”).** *(ÚJ, F41.1/3.2, `naplok/F41_bsb_megfeleltetes.tsv` fejléc; a számot (N-F41d) a main-Action osztja ki)*
  Mérés (`scope=manual`, a menet saját összevetése, ts=2026-10-02): a TAHOT_kivonat és a `Macula_heber_*.tsv` (MT/WLC) fejezet-maximuma 25 ószövetségi könyvben tér el (TAHOT_kivonat/Macula; pl. 2Sám 18: 33/32 és 19: 43/44; Dán 3: 30/33, 4: 37/34, 5: 31/30, 6: 28/29; 1Kir 4: 34/20, 5: 18/32; Jóel 2: 32/27, 3: 21/5, 4: nincs; Mal 3: 18/24, 4: 6/0; Jób 38: 38/41, 39: 38/30, 40: 24/32, 41: nincs; 4Móz 12: 15/16, 13: 34/33). A D3 („átszámozás MT-re”) ezért pontosabban „átszámozás a TAHOT_kivonat számozására”. A 2Sám 18:33/19:1 és a Dán 3:31–33/5:31 feltevés ezen a számozáson nem eltérés (a BSB és a TAHOT_kivonat azonos számozású), a masszoréta számozáshoz viszonyítva viszont az. Döntendő: a `Igehely` célszámozása legyen-e a TAHOT_kivonaté, a Macula/WLC-é, vagy a Károlié (a három egyenként más). **Eldöntve (felhasználó, 2026.10.02, DT-F41b): a célszámozás MT (WLC), ahogy a D3-ban; a megvalósítás: N-F41g, N-F41h. A `bsb_wlc_versszam_ellenorzes.py` (F41.7; versszintre javítva F41.10, szigorítva F41.12) versenként összeveti az `Igehely`-t a WLC-vel: `naplok/F41_wlc_versszam_ellenorzes.tsv`.**
  *Ide kapcsolódik a Jób 41:* a TAHOT_kivonatban nincs a 41. fejezet (és a 40:25–32 sem), ezért a BSB Jób 41 (34 vers) a KJV-számozást tartja, `kjv` `Számozás`-jelöléssel az F41-ben (a `naplok/F41_bsb_megfeleltetes.tsv` `modell` oszlopában az érték `kjv_szamozas`). A Macula (WLC) szerint a megfeleltetés a kért ismert leképezés (KJV 41:1–8 = MT 40:25–32; 41:9–34 = MT 41:1–26): a BSB-versek 30/34-en részhalmazként illeszkednek (a 4 kivétel egy-egy H4480-címke), a `konkordancia/Macula_heber_Job.tsv` alapján. Átszámozás ezzel külön döntésre vár.
- **N-F41g — a Jób 38–41 `Igehely`-ének MT/WLC-számozásra hozása, csak gépi táblából.** *(ÚJ, F41.7, DT-F41c (a), DT-F41b; a számot (N-F41g) a main-Action osztja ki)*
  A `BSB_Strongs.tsv` Jób 38–41 sorai (890 sor: Jób 38: 296, 39: 208, 40: 163, 41: 223) a BSB/KJV-számozást tartják, sorszintű jelöléssel: a versszintű WLC-összevetés (F41.12 szerint) a Jób 38–39 és a Jób 40 21 verse `mt` (a BSB/KJV-szám = MT), a Jób 41 34 verse (223 sor) `kjv` (tényleges KJV ≠ MT: BSB 41:1–8 = MT 40:25–32, 41:9–34 = MT 41:1–26), a Jób 40:1/3/6 (17 sor) `ellenorizetlen` (F41.15: a `kjv` címke csak ténylegesen KJV ≠ MT versre kerül; a Jób 40:1–24 KJV = MT, de ez a három formulás vers a kritérium szerint nem igazolható, a TAHOT-megfeleltetésük 39:34, 39:36, 40:6). A WLC fejezet-max szerint (Macula: 38: 41, 39: 30, 40: 32, 41: 26 vers; BSB/KJV: 41, 30, 24, 34; `naplok/F41_wlc_versszam_ellenorzes.tsv`) a Jób 40 és 41 számozása eltér, a 38 és 39 fejezet-max azonos — **a versszintű megfeleltetést gépi forrásból kell levezetni** (a TVTMS vagy a WLC (Macula) versszámaiból, Strong-illeszkedéssel, mint a `bsb_import.konyv_megfeleltetes`, `forras` = a WLC Strong-halmazai), **kézi megfeleltetés nélkül**; az orkesztrátortól kapott kézi Jób 40–41 megfeleltetés és a d42b729-ben bevezetett Jób 39:34–38 / 40:25–32 logika nem használható. Kimenet: a Jób 41 (és az esetleg el nem igazolt Jób-sorok) `Számozás`=`kjv` helyett igazolt MT-számozásúak (`mt`), a nulla-diff a többi könyvre.
- **N-F41h — az `ellenorizetlen` Számozású sorok (271 fejezet, 1 477 vers, 17 659 sor) `Igehely`-ének MT/WLC-számozásra hozása.** *(ÚJ, F41.7, átírva F41.10-ben: DT-F41b, DT-F41f; a számot (N-F41h) a main-Action osztja ki)*
  A jelölés elkészült (DT-F41f): a `BSB_Strongs.tsv` 7. oszlopa versszintű WLC-összevetésből `mt` (260 243 sor) / `kjv` (223 sor: Jób 41) / `ellenorizetlen` (17 659 sor; F41.12/F41.15: a szigorított, környezet-egyértelmű kritérium szerint a WLC-vel **egyértelműen nem igazolt**; nagy része formulás/ismétlődő, azonos Strong-halmazú szomszéd versek döntetlenje KJV = MT fejezetekben, ezeknek a száma lehet helyes; a többi hibrid részvers, izolált egyezés, a WLC-ben nincs ilyen vers vagy üres a WLC-halmaz; a Jób 40:1/3/6 is). **Az `ellenorizetlen` nem „TAHOT-hibrid számozás”, és nem állítja, hogy a szám hibás.** A sorok `Igehelye` a megfeleltetés szerinti (TAHOT_kivonat-alapú) szám (`naplok/F41_wlc_versszam_ellenorzes.tsv`, `ellenorizetlen_versek_lista` oszlop; a 271 fejezet listája ott). A feladat a teljes MT-átszámozás: gépi megfeleltetés a WLC-hez az N-F41g módszerével (Strong-illeszkedés, `forras` = a WLC Strong-halmazai), **kézi táblázat nélkül**; az átszámozott sorok `Számozás`-a `mt`. A 4Móz 12/13 átszámozását a felhasználó visszavonta (DT-F41f: WLC szerint KJV = MT), ezért ez a tétel azt már nem érinti.

- ✅ **N-F38a — a `FORRAS_VERS_OCR` kapubővítés jóváhagyása.** *(ÚJ, F38 (#38), DT-F38g (5), LEZÁRVA a DT-F38h szerint (5. adag); a számot (N-F38a) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  Az `eszkozok/forditas_kapuk.py` `FORRAS_VERS_OCR` szótára (`Gen 33:816t.` → `Gen 33:8 16t.`) a 2_versszam kapu forrásparaméterében javítja a H4264 összeforrt OCR-helyét; más kapura és más helyre nem hat (egységteszt: `eszkozok/teszt_forditas_kapuk.py`, `ForrasVersOcr`). Kapuszabály-bővítés: a felhasználó jóváhagyása kell. Opciók: (a) jóváhagy; (b) elvet, és a H4264 kivétellel kezelendő.

- ✅ **N-F38b — a H7451 és a H4390 Szellem-kisbetű/nagybetű kétsége.** *(ÚJ, F38 (#38), DT-F38g (3), tartalmi döntésre vár; a számot (N-F38b) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  H7451 (#28): a BDB maga „divine spirit” (`konkordancia/BDB_teljes_unabridged.tsv:6966`), a DT-F38g (3) betűje szerint nagybetű járna, de a DT-F38f 3. „rossz szellem kisbetűs” szabálya ezzel ütközik. H4390: egy frázis, emberi és isteni értelemben vegyesen. A szöveg jelenleg változatlan.

- ✅ **N-F38c — a H5674 „a Szellemről” szövegezés megítélése. LEZÁRVA a DT-F38h (c) szerint: a `forditasok.tsv` 176. sora ma „a Szellem 1Kir 22:24” (nagybetűs, a BDB 9a besorolásával összhangban); az „a Szellemről” alak a DT-F38g (2) alkalmazása volt, a DT-F38h (c) átfogalmazta.** *(ÚJ, F38 (#38), DT-F38g (2), megítélésre vár; a számot (N-F38c) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  Az 1Kir 22:24-en a végrehajtó „a Szellemről”-t írt; a brief „az Úr Szelleme” alakja új szót vinne be (a BDB-ben „az Úr” nincs). Opciók: (a) marad „a Szellemről”; (b) „az Úr Szelleme” (új szó, külön döntés).

- **N53 — a BDB-gyökcsoport (rokon szavak) hasznosítása külön adatként.** *(ÚJ, F38 (#38), DT52 (c), a felhasználó később dönt; a számot (N53) a F30 helyőrző-szabálya szerint a main-Action osztja ki)*
  A mérés (`naplok/BDB_FORDITAS_naplo.md` M0 5. pont, `naplok/BDB_FORDITAS_gyokcsoportok.tsv`): 7 990 Strong, 71,4% kap BDB-rokon többletet (újramérve). A felhasználó a DT52 (c) szerint a 3. opciót választotta (később dönt), az irány a 2.: ha hasznosítjuk, külön adatként (új tábla vagy mező SEMA-bővítéssel), **nem a fordításban**. A 7. adag nem vár rá; a fordítás szócikkenként megy tovább, a gyökcsoport-adat nem kerül a `forditasok.tsv`-be, amíg a döntés nincs meg. Opciók: (a) külön adat (`adat/` tábla, SEMA-bővítéssel, licencsorral: CC BY 4.0); (b) nem használjuk.

- **N-F53d — kártyaszöveg-piszkozat a 10 leírás nélküli kártyára.** *(ÚJ, F53 (#53), FT.2 ⛔, felhasználói válasz 2026-10-05; az FT.3 után, külön tételben; a számot (N-F53d) a main-Action osztja ki)*
  Érintett: #53, #54, #55, #57, #58, #59, #60, #61, #64, TERV_BEFOGAD (a lap ma „nincs leírás”-t ír). A `reszletes` és `roviden` szöveg **csak piszkozat** lehet (a briefekből, naplóba vagy külön fájlba); az `eszkozok/feladatterkep_kartyak.tsv`-be **csak a felhasználó jóváhagyása után** kerül, `forras` = `kezi-<dátum>`.

- **N48 — Strong-ekvivalencia a BSB-mérésben.** *(ÚJ, F71, felhasználói felvétel 2026-10-06; a számot (N48) a main-Action osztja ki)* A DT6 lezárása (✅) érvényes marad: az elutasított (d) a küszöb **lazítása** volt, ez a tétel viszont a mérés **finomítása**, ezért nem ellentmondás. A `naplok/F41_nem_egyezo_versek.tsv` `cimkezes` sorai (pl. 1Móz 1:4: TAHOT H2895, BSB H2896) azt mutatják, hogy az igehely-szintű egyezés (TAHOT ⊆ BSB) egymásnak megfelelő, de eltérő számú Strong-címkéket is eltérésnek számol. Lépések: (1) Strong-ekvivalencia-tábla összeállítása és **igazolása** (forrással, provenienciával; asszociatív párosítás nem kerülhet bele, 3. szabály); (2) a mérés újrafuttatása **mind a 39 ÓSZ-könyvre**, változatlan 95%-os küszöbbel (D15), az F06-módszer szerinti érték mellett külön oszlopban. A 2Sám, az Ezsd vagy a Dán csak akkor kerül be a `BSB_Strongs.tsv`-be, ha az új módszerrel eléri a 95%-ot; addig a kimaradásuk (DT6 (a)) érvényes.

- **N49 — a BSB display-JSON-ból hiányzó 117 első vers pótlása (DT6 (c)).** *(ÚJ, F71, DT6 (c) továbbvitele, felhasználói döntés 2026-10-06; a számot (N49) a main-Action osztja ki)* A `base/display/` JSON-ból 117 fejezet 1. versének szövege és Strong-címkéi hiányoznak (116 feliratos zsoltár + Zak 12:1; `konkordancia/README.md` „Ismert hiány”). A `base/text-only/` CC0, de csak angol szöveget ad, Strong-címkét nem. Első lépés: a `base/hebrew-tsv/` licencének ellenőrzése (a #33 nem rendezte; a repó README-je/ATTRIBUTION-je csak a `text-only/`-t mondja CC0-nak). Utána: pótlás a `hebrew-tsv/`-ből, vagy — ha a licenc nem igazolható — explicit üres eredmény. A gyökér közös az N-F71a-val (a Zsolt 13 MT 1–2 annak egy esete); a DT6 lezárását nem blokkolja.

- **N50 — a Zsolt 13 MT 1–2 verse (felirat, BSB 13:1) hiányzik a `BSB_Strongs.tsv`-ből.** *(ÚJ, F71, ellenőr: EF1 eltérés; a számot (N50) a main-Action osztja ki)* A #71 csak az MT 3–6-ot importálta (41 sor, `manual`, kézi kivétel): a BSB 13:1 szövege a `base/display/` JSON-ból kiesik (DT6 (c), a README „Ismert hiány”-a, 116 feliratos zsoltár), a felirat pedig a BSB-ben `d`-szintű heading, nem hordoz Strongot, bár a TAHOT szerint az MT 13:1 hordoz (H1732, H4210, H5329). Az üres eredmény explicit, nem töltendő ki (3. szabály). Megoldás: a display-JSON hiányának külön kezelése (pl. a `base/text-only/` állomány), nem a kézi kivétel. Nyitott: a `naplok/F41_wlc_versszam_ellenorzes.tsv` Zsolt 13 sora még `nincs_bsb_sor`; a `naplok/F16_bsb_zsolt_megfeleltetes.tsv` fejléce gépi futtatási parancsot mond a kézzel szerkesztett sorokhoz.

- **N51 — az arámi pótlás beemelése a fő táblába: alias-sorok és 6 szöveges pótlás, majd a #38 sorrendjének újragenerálása.** *(ÚJ, F66 (#66), 2026.10.06; a briefben N52 néven szerepelt; a számot a main-Action osztja ki; a felhasználói döntés ezt rögzítette (2026-10-06, chat); a végrehajtás külön feladat: `beerkezo/F66b_BDB_ARAM_BEEMELES_BRIEF_TERVEZET.md`, befogadásra vár)* A `konkordancia/BDB_aram_potlas.tsv` 170 elfogadott sora (169 `egyertelmu` + 1 `kezi_elfogadott`: H2298 → BDB9285) külön táblában áll; a fő tábla bájtra változatlan. **Duplikáció (mérve, `naplok/BDB_ARAM_POTLAS_duplikacio.md`):** a DictBDB a közös héber–arámi szócikkeket egy sorban adja, ezért a 170 sorból 164 szövege (ujjlenyomat-mérőszám ≥ 0,8) már a fő táblában van, a héber testvérsor végén; 5 részleges, 1 nincs (H6433). **Döntés:** (1) a 164 duplikált sor **nem** kerül be új szövegsorként a `BDB_teljes_unabridged.tsv`-be; a 164 Strong-szám **alias-sorként** kerül be, a héber testvérsorra mutatva, a `BDB_strong_alias.tsv` mintájára (`masodlagos_strong` → `tabla_strong`, `szoveg_hasonlosag` az ujjlenyomat-mérőszámból, a proveniencia a mérés soráról); (2) szöveges pótlásként csak a **6 valódi hiány** (az 5 részleges és a H6433) kerül a fő tábla végére, az `eszkozok/bdb_strong_potlas.py --m2` mintájára, a meglévő sorok bájtra azonosak maradnak; (3) jelölt marad: H0004 (`cimke_reszleges`), H3769, H5013 (`csonk`); (4) a beemelés a #38 7. adagja **előtt** fut, utána a #38 sorrendje újragenerálandó; ez külön feladat. **LEZÁRVA (2026.10.07, F72; helyőrző: DT-F72):** a beemelés elvégezve: 164 alias-sor (a H5839 → H5838 indokolt felülírással, a H2298 → H0259 automatikus egyezéssel; a két korábbi kizárás téves alapon állt, a szöveg mindkét esetben a testvérsor végén van, a `kezi_elfogadott` döntés a szócikk-azonosításról szólt), 6 szöveges pótlás, jelölt marad H0004, H3769, H5013 (`naplok/BDB_ARAM_BEEMELES_zaras.md`). A #38 sorrendjének újragenerálása a `F72` 4. lépése; a #38 7. adagjának `fugg`-bővítése a befogadáskor. **A #38 sorrendje újragenerálva (F72.6):** a 648 soros kész előtag változatlan, +9 sor a hátralékban (6 F72: H1753, H3367, H3848, H6433, H7560, H8065; 3 az F57 óta kimaradt: H0747, H4123, H4725); a H4725 (gyakoriság 401) a 649. sor lett; a hátralék adagbeosztása eltolódott (7425 sor, adagok 7–14), a DT55 „a #38 9. adagja előtt” döntése ennek ellenére érvényes marad: a még fordítatlan `javitva` sorok (H5377, H0479: 9. adag; H2597: 11. adag) az új sorrendben is ugyanott vannak, a 7–8. adagban ilyen sor nincs (`naplok/BDB_ARAM_BEEMELES_zaras.md`).

## Migrálva a döntési fájl 8. szakaszából (F1.6, 2026.09.13)


A `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` 8. szakasza ezzel archívummá vált — belépő: `DONTESEK_INDEX.tsv`. A vers-szintű jelöltek nem ide, hanem az `adat/jeloltek.tsv`-be kerültek (16 sor, mind `dontes=nyitva`): HODIT-001 13 alacsony szavazatú TSK-jelölt, MENNY-001 Mt 24:38 + Luk 17:27, ANTROP-001 Fil 1:27. Az alábbiak a nem vers-szintű tételek:

* **Adatminőség — a `TAHOT_kivonat.tsv` lefedettségi rése — ⏹ JAVÍTVA (F2, 2026.09.14).** A korábbi állítás (1Móz 32, Zsolt 88/89/140/142, Jóel 3 hiánya) elavult volt: az `eszkozok/tahot_lefedettseg_ellenoriz.py` tételes, mind a 39 könyvre kiterjedő ellenőrzése szerint mind a hat fejezet teljes egészében jelen van. **Ami ténylegesen hiányzik:** Jób 40:1-5 és a teljes Jób 41. fejezet — ez korábban nem volt dokumentálva, valószínűleg a Jób 40-41. fejezeteinél ismert héber/angol versszámozási eltolódás miatt (l. `TAHOT_TAGNT_README.md`, tételes forrás-ellenőrzés még nyitva). A `proveniencia` mező `scope` értéke ettől függetlenül `TAHOT-teljes` (nem `OT-full`) — l. `adat/SEMA.md` 1.5 és 4. Az `eszkozok/lekerdez.py` (F2) minden parancsa ezt a címkét írja ki.
* **Károli-kiadás hitelesítése.** A scrollmapper HunKar-adat az 1908-as revideált kiadás — ellenőrizendő, hogy a projekt korábbi tanulmányaiban idézett Károli-szövegek ugyanezzel a kiadással egyeznek-e, mielőtt a strukturált adatbázist visszamenőleg is hitelesítő forrásként használnánk.
* **Károli-revízió sokféleség.** A "Károli" név alatt legalább két, szövegszerűen eltérő kiadás létezik: az 1908-as HunKar (közkincs, ez a publikus dataset) és a Revideált Károli (Veritas Kiadó, 2011 — © védett, **nem közkincs**). Nyitott: ha a felhasználónak van jogszerű hozzáférése a 2011-es szöveghez, érdemes-e külön **privát** datasetként felépíteni összevetés céljából? A publikus `Karoli_1908.tsv` semmiképp nem cserélendő rá.
* **Rokon gyökű jelöltek egyedi minősítése** (a `Konnyu_ellenorzes_4_lezart_tanulmany.md` 5 tétele). HODIT-001 / Rafeusok, mind a H7495 (*ráfá*, "gyógyítani") gyökből: **H8655 תְּרָפִים** (*teráfim*, "házi bálványok") — a jelentés szerint **erős tartalmi jelölt**; **H7504** (*ráfe*, "gyenge") és **H7510** (*rifjón*, "erőtlenség") — gyengébb, tematikus. Továbbá TEREMT-001 / Tehóm-gyök: **H4103** (*mehumáh*). Ezek **lexikai**, nem vers-szintű jelöltek, ezért nem a `jeloltek.tsv`-be valók: előbb scan kell rájuk, és a scan verssorai lesznek jelöltek.
* **Példabeszédek és ApCsel teljes feldolgozása** a két-táblás + join struktúrában — eddig csak minta készült (Péld 1:1-9, ApCsel 1:1-8). *Megjegyzés: az SzPA-integráció felfüggesztése óta ez a tétel részben tárgytalan; a "csak Károli" kétoszlopos forma az érvényes, és a 4.7 kumulatív elv szerint a teljes strongozás nem cél.*
* **Felület-döntés:** készüljön-e szűk hatókörű PAT a privát repóhoz a claude.ai chat-felülethez, vagy a munka véglegesen Claude Code-ra kerül át? *Az átalakítási terv 5. pontja ezt gyakorlatilag eldöntötte (a végrehajtási felület Claude Code), de a privát repó elérése formálisan nyitott.*
* **Figyelendő, még nem elérhető STEPBible-adatállományok:** **TAGOT** (taggelt Septuaginta — ez pótolná a "tudatos idézet vs. véletlen egybeesés" eldöntéséhez hiányzó láncszemet), **TBCWG** (rokon jelentésű szócsoportok — a motívumlog küszöbszámítási elvét segítené), kisebb jelentőségűek: TOTMM/TNTMM, TFBDB.
* ~~**ÚJ (F1.6) — SDBH / SDGNT import.**~~ **LEZÁRVA 2026.09.16 → SDBH.1–SDBH.4, javítás: SDBH.1a, SDBH.2a, SDBH.4a.** Kivonat a `konkordancia/SDBH_domenek.tsv`-ben és a `SDGNT_domenek.tsv`-ben, jelentés-szintű doménnel; a `lekerdez.py domen` mező-tágítást és elhatárolást ad. Forrás és licenc: `konkordancia/SDBH_SDGNT_README.md`. Nyitva maradt: a szakasz-profil (versenkénti hivatkozás-tábla), a forrás 150 hibás anomália-sora és 35 elemzetlen bejegyzése (`SDBH_SDGNT_anomaliak.tsv`), és a CC BY-SA 4.0 publikálási következménye (terv N11) — ez az F6 brief előfeltétele.
* **~~ÚJ (F3.3) — a `scope=manual` és az F4 generátor ütközése.~~ LEZÁRVA 2026.09.14 → D25.** A megoldás nem a `manual` gyengítése, hanem a két tény szétválasztása: a proveniencia visszaállt a kanonikus `scope | forras | ts` alakra, az igazolás pedig önálló `igazolas` oszlopba került (`TAHOT-igazolt` 138 / `TAHOT-hatokoron-kivul` 25 / `nincs` 38). A `strong_vart` eldobva, mert mind a 138 soron azonos volt a `strong` oszloppal. Végrehajtó: `eszkozok/igazolas_migracio.py`; séma: `adat/SEMA.md` 1.8. A SEMA 3.3 kényszere változatlan — `manual` esetén a sor továbbra is értelmezésként jelölendő; az `igazolas` ehhez hozzátesz, nem visszavon.
* ~~**ÚJ (F3.3) — három KIRALY-001 sor `strong` nélkül.**~~ ⏹ **JAVÍTVA (F3.4, 2026.09.14):** a `G5010` átemelve a `gerinc_elem`-ből a `strong` oszlopba mindhárom sornál (Zsid 5:6, 5:10, 6:20) — az F3.4-nek szüksége volt rá, mert Strong nélkül nincs join-sor. A másik három `strong` nélküli sor (MENNY-001) változatlanul helyes: ott a horgony nem lexikai (`referencia:1Énokh 10:4-6`, `idézet:1Énokh 1:9`, `formula:οὐκ ἐφείσατο`) — ezek közül a 2Pét 2:4-5 mégis kapott join-sort, mert a formula mögött a TAGNT szerint van Strong (`G5339`, *pheidomai*).
* **ÚJ (F3.4) — a `Karoli_1908.tsv` két azonosított, de nem javított vers-eltolódása.** `Jób 17` egy verssel (a `Jób 16:22` sor két verset olvaszt egybe), `Préd 9` két verssel el van tolva a szabványos számozáshoz képest. Mindkettő felvéve a `konkordancia/Karoli_adatminosegi_anomaliak.tsv`-be `AZONOSITVA, NEM JAVITVA` állapottal; a szétbontás MEK-forrás tételes ellenőrzését igényli, mint a korábbi hét javított tételnél. **Amíg nincs javítva, minden `Jób 17:*` és `Préd 9:*` hivatkozás néma nem-találatot vagy rossz verset ad a Károli-táblán.** Érdemes az `eszkozok/f3_4_nema_nemtalalat.py` mintáját (Strong → ismert magyar visszaadások halmaza) a teljes join-táblára általánosítani, hogy kiderüljön, hány további fejezet érintett.
* **ÚJ (F3.4) — a `Melkizedek_tematikus.md` Zsid 7:3-as Strong-hármasa téves.** A study táblázata és a kereszthivatkozás-naplója `G0813`-at rendel az *ἀπάτωρ*-hoz; a `TAGNT_kivonat.tsv` szerint az helyesen **G0540** (a `G0813` az *ἄτακτος*, „rendetlen"). Az `adat/elofordulasok.tsv` `bdb_entry_id` mezője (`G5010+G0813+G0282`) ráadásul a `G0035`-öt (*ἀγενεαλόγητος*) sem tartalmazza. A join-táblába az F3.4 a TAGNT-igazolt hármast írta (`Heb.7.3`: G0540/G0282/G0035); **a study és az `elofordulasok` sor javítása tartalmi döntés, felhasználói megerősítést kér.**
* **ÚJ (F3.4) — az `elofordulasok.tsv` `G4151+G5590` gerinc-eleme két ANTROP-001 sornál pontatlan.** Az 1Kor 2:14-ben `G5591` (*ψυχικός*), a 2:15-ben `G4152` (*πνευματικός*) áll — nem a főnevek. Döntendő: a `gerinc_elem` a motívum *magját* nevezi-e meg (akkor helyes így), vagy a soron ténylegesen álló szót (akkor javítandó). A join-sorok a versben álló Strong-számot viselik.
* **ÚJ (F3.4) — 26 régi join-sor nem nullázott Strong-számot visel** (`H430`, `H779`, `H8414+H922`…), ami sérti az `adat/SEMA.md` 1.2-t. Mind a 26 korábbi genezisi tanulmányokból való (a `Karoli_Strong_kivonat.tsv` 182. sora előtt), egyik sem F3.4-es. A javítás mechanikus, de más tanulmányok sorait érinti és egy esetleges `grep H779` hívást elnémítana — ezért az F3.4 nem végezte el.
* **Bibliai Motívumlexikon — koncepcionális tervezés.** Réteges architektúra-vízió (Szöveg → Konkordancia → Lexikon → Motívum → Kapcsolat → Tanulmány), napló: `motivumlog/Bibliai_Motivumlexikon_tervezesi_naplo.md`. *Ez a tétel az `ATALAKITASI_TERV.md.md`-vel implementációs fázisba lépett — az F1 (séma + belépési pont) elkészült; az `adat/` réteg ennek a víziónak az első megvalósult darabja.*

## Adattáblából generált — nyitott jelöltek és motívum-státuszok

<!-- A GENERÁLT BLOKK HELYE: nyitott -->

<!-- GENERÁLT-KEZDET: general.py --cel nyitott | forrás: adat/jeloltek.tsv, adat/motivumok.tsv, adat/elofordulasok.tsv | ts=2026-09-15 -->

*Ez a blokk a `jeloltek.tsv` 17 nyitott (`dontes=nyitva`) sorát fedi 3 motívum-ID-ről, és a `motivumok.tsv` 9 státusz-sorát. A 259 beépítve és 66 elutasítva döntésű jelölt nem tartozik ide. A fájl minden más szakasza kézi, a marker-blokkon kívül marad.*

### Nyitott jelöltek (`adat/jeloltek.tsv`, `dontes=nyitva`)

| # | Motívum-ID | Igehely | Forrás-keresés | Indoklás | Dátum |
|---|---|---|---|---|---|
| 1 | `[ID: ANTROP-001]` | Fil 1:27 | döntési fájl 8. szakasz (migrálva F1.6-ban) | bekerüljön-e ötödik, korporatív jellegű előfordulásként a pneuma/pszükhé tanulmányba; a study jelenlegi szövege NEM említi — ellenőrizve 2026.09.13 | 2026.09.13 |
| 2 | `[ID: HODIT-001]` | 1Móz 14:6 | study 1. pont táblázata (kontextuális sor) | חֹרִים (Hórim) nem a רְפָאִים szócsaládból való — nincs közös gyök H2752 és H7497/H7496 között; a study saját táblázatában szerepel mint "ugyanabban a hadjáratban legyőzött negyedik népcsoport", de a motívum negatív kritériuma (l. adat/motivumok.tsv HODIT-001 sora) kizárja: a rokon népnév önmagában nem elég, lexikai átfedés kell | 2026.09.14 |
| 3 | `[ID: HODIT-001]` | 5Móz 1:4 | TSK, alacsony szavazat | Óg/Básán tematikus szomszédság; nem H7497-előfordulás — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 4 | `[ID: HODIT-001]` | 5Móz 2:23 | TSK, alacsony szavazat | Óg/Básán tematikus szomszédság; nem H7497-előfordulás — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 5 | `[ID: HODIT-001]` | 5Móz 3:20 | TSK, alacsony szavazat | Óg/Básán tematikus szomszédság; nem H7497-előfordulás — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 6 | `[ID: HODIT-001]` | 5Móz 3:22 | TSK, alacsony szavazat | Óg/Básán tematikus szomszédság; nem H7497-előfordulás — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 7 | `[ID: HODIT-001]` | Józs 13:19 | TSK, alacsony szavazat | Básán-terület egyéb említése; tematikus szomszédság — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 8 | `[ID: HODIT-001]` | Józs 13:31 | TSK, alacsony szavazat | Básán-terület egyéb említése; tematikus szomszédság — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 9 | `[ID: HODIT-001]` | 1Krón 4:40 | TSK, alacsony szavazat | tematikus szomszédság, nem lexikai egyezés — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 10 | `[ID: HODIT-001]` | Zsolt 78:51 | TSK, alacsony szavazat | 'Khám földje' tematikus szomszédság — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 11 | `[ID: HODIT-001]` | Zsolt 105:23 | TSK, alacsony szavazat | 'Khám földje' tematikus szomszédság — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 12 | `[ID: HODIT-001]` | Zsolt 105:27 | TSK, alacsony szavazat | 'Khám földje' tematikus szomszédság — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 13 | `[ID: HODIT-001]` | Zsolt 106:22 | TSK, alacsony szavazat | 'Khám földje' tematikus szomszédság — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 14 | `[ID: HODIT-001]` | Jer 48:1 | TSK, alacsony szavazat | Móáb-prófécia, a 'Refáim' szó nélkül — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 15 | `[ID: HODIT-001]` | Jer 48:23 | TSK, alacsony szavazat | Móáb-prófécia, a 'Refáim' szó nélkül — egyedi minősítést igényel, a 2026.09.10-i körben nem történt meg | 2026.09.13 |
| 16 | `[ID: MENNY-001]` | Mt 24:38 | Károli-KH (forrás-vers: 1Móz 6:2) | tartalmilag nem az 'Isten fiai kiléte' kérdéshez, hanem az eszkatológiai-ítéleti 'mint Noé napjaiban' analógiához tartozik; eldöntendő: (a) jegyzet valamelyik study-ba, (b) önálló motívum, (c) figyelmen kívül — FELHASZNÁLÓI DÖNTÉS | 2026.09.13 |
| 17 | `[ID: MENNY-001]` | Luk 17:27 | Károli-KH (forrás-vers: 1Móz 6:2) | tartalmilag nem az 'Isten fiai kiléte' kérdéshez, hanem az eszkatológiai-ítéleti 'mint Noé napjaiban' analógiához tartozik; eldöntendő: (a) jegyzet valamelyik study-ba, (b) önálló motívum, (c) figyelmen kívül — FELHASZNÁLÓI DÖNTÉS | 2026.09.13 |

### Motívum-státuszok (`adat/motivumok.tsv`)

| Motívum | Státusz | Verzió | Státusz dátuma | Fő előfordulás | Nyitott jelölt | Forrás-study |
|---|---|---|---|---|---|---|
| Hádész (Seól) — a halottak birodalma `[ID: ALVIL-001]` | publikálható | v2 | 2026.09.10 | 6 fő / 72 sor | 0 | tematikus_lezart/Hadesz_Seol_tematikus.md |
| Pneuma/pszükhé megkülönböztetés `[ID: ANTROP-001]` | publikálható | v3 | 2026.08.22 | 5 fő / 8 sor | 1 | tematikus_lezart/Pneuma_pszukhe_megkulonboztetes_tematikus.md |
| A bűn következményeinek gyűrűzése — átok, föld és romlás `[ID: HAMART-001]` | publikálható | v1 | 2026.09.11 | 4 fő / 52 sor | 0 | tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md |
| Rafeusok/óriás-népek `[ID: HODIT-001]` | publikálható | v3 | 2026.09.10 | 1 fő / 33 sor | 14 | tematikus_lezart/Rafaim_tematikus.md |
| Segítségül hívni az Úr nevét `[ID: ISTENTISZT-001]` | publikálható | v3 | 2026.09.22 | 5 fő / 32 sor | 0 | tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md;motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md |
| Melkizedek — király-pap rendje, kenyér és bor `[ID: KIRALY-001]` | publikálható | v2 | 2026.09.10 | 1 fő / 9 sor | 0 | tematikus_lezart/Melkizedek_tematikus.md |
| Isten fiai — Nefilim — Gibborim motívum-komplexum `[ID: MENNY-001]` | publikálható | v4 | 2026.09.10 | 1 fő / 9 sor | 2 | tematikus_lezart/Isten_fiai_Nefilim_Gibborim_tematikus.md |
| Tehóm (תְּהוֹם) — Abüsszosz (ἄβυσσος): a mélység motívuma `[ID: TEREMT-001]` | publikálható | v4 | 2026.09.10 | 5 fő / 41 sor | 0 | tematikus_lezart/Tehom_tematikus.md |
| Tohu va-vohu (תֹהוּ וָבֹהוּ) — a föld kietlen és puszta állapota a teremtéskor és az ítéletkor `[ID: TEREMT-002]` | feldolgozás alatt | v1 | 2026.09.25 | 3 fő / 3 sor | 0 | — |

<!-- GENERÁLT-VÉGE: nyitott -->

## Lezárva
### 2026.10.06 (F66_BDB_ARAM_POTLAS_BRIEF.md — N52 felvéve és lezárva):
* N52 — a szúrópróba-kivonat két hibája (csak a `naplok/BDB_ARAM_POTLAS_szurop.md` igehely-kivonatát érintette, a TSV-t nem). **LEZÁRVA (2026.10.06, F66):** (a) a H3542 listáján a Jer 48:47 és a Jer 51:64 héber „compare” hely volt, nem arámi előfordulás; (b) a H3969 listáján az Ezsd 6:17 háromszor állt (nem szűrte az ismétlést). Javítva az `eszkozok/bdb_aram_potlas.py --szurop`-ban (`aram_hely`: csak a bibliai arámi szakaszok; ismétlés nélkül), a napló újragenerálva, teszttel.

### 2026.10.05 (F53_FELADATTERKEP_BRIEF.md utótétel — N-F53c, N-F53e, N-F53f lezárva):
* N-F53c — a generált feladattérkép három megjelenítési hibája. **LEZÁRVA (2026.10.05, PR #204):** a nyers Markdown a lapon `md()`/`plain()` függvénnyel renderel (előbb HTML-escape); a puszta `F\d+` kódú csomópont (#22) felirata a cím eleje; az elválasztó a kártyán belül áll, az utolsón nincs. A #22 valódi kódneve a brief `kod:` mezőjén múlik.
* N-F53e — CI-őr a generált feladattérképre. **LEZÁRVA (2026.10.05, PR #203):** az E18 bővítése a `feladatok.py ellenoriz --pr-alap`-ban (`pr_terkep_ellenorzes`): a `FELADATTERKEP.html` és a `feladatterkep.json` a PR `merge-base..HEAD` diffjében nem szerepelhet. Ezzel a bélyeg egy-commitos késése is megszűnt.
* N-F53f — az FT.5 (artifact `files`-olvasással) és az FT.7. **LEZÁRVA, KIVÁLTVA (2026.10.05; felhasználói döntés):** `chan_…` azonosító nincs, mert a repó nem Claude Code projekt (helyi desktop-munkakönyvtár), így a `files`-olvasás nem valósítható meg. Helyette a `feladatterkep-napi` helyi ütemezett feladat (naponta, a `.claude/worktrees/terkep` worktree-ben `git fetch` + `checkout --detach origin/main`) a main-en lévő generált lapot változatlanul feltölti a https://claude.ai/artifact/Dwnq3JtHgmgPiwDPaUnJzx artifactra, ha a SHA-256 változott; első feltöltés 2026.10.05, bélyeg `677867c`. A brief 4.4 nagyítása a generált lapba került (F53.3, PR #207). Az FT.7 `main_frissit.py`-ja okafogyott; az `origin/main` frissességét a rutin fetch-e adja.

### 2026.10.05 (F53_FELADATTERKEP_BRIEF.md utótétel — N-F53a és N-F53b lezárva):
* N-F53a — a #50 (CI_JAVITO_KOR) fejléce. **LEZÁRVA (2026.10.05; felhasználói döntés, módosítva):** a `fugg: [45]` függési kört adott (#45 ↔ #50: mindkettő a `.claude/commands/kovetkezo.md`-t írja, ezért a rendszer kölcsönös kizárást vezet le), és a brief D4 sora is kizárást ír elő, nem sorrendet. A fejléc `fugg: []` marad; a `kovetkezo:` sor: „nem futhat a #45 (MODELL_ELLENORZES) mellett, mert mindkettő a .claude/commands/kovetkezo.md-t írja (kizárás, D4)”; a #32 (PR #164, main) kikerült belőle. Az F50 brief D5 sora rögzíti. `feladatok.py ellenoriz`: 0 hiba.
* N-F53b — a `DONTESEK.md` DT1, DT3, DT4, DT19 oszlophibája. **LEZÁRVA (2026.10.05):** DT1, DT4: elválasztó `|` a Döntés és a Napló közé; DT3: `\|Δ sorszám\|`; DT19: a proveniencia-sor két `|`-je `\|`. Mind a négy sor 8 cellás; a feladattérkép `ellenőrizendő` listája üres.

### 2026.10.05 (F42_FORRASKIVEZETES_BRIEF.md — N9 lezárva, DT-F42g):
* N9 — a licenc-besorolás kettős forrása. **LEZÁRVA (F42.7, 2026.10.05; felhasználó, DT-F42g):** a `lexikon_general.py` `LICENC`-konstansa és a `TISZTAZATLAN_SZOTARAK` megszűnt; a licenc-állapot és a rövid címke az `adat/licencek.tsv`-ből jön (új, zárt `cimke` oszlop, SEMA 2.19); hiányzó sor vagy üres címke hiba, alapértelmezett érték nincs. Várt render-változás: az LSJ-címke CC BY-SA 3.0 → 4.0 (Perseus nyilatkozata).
  *Proveniencia: scope=adat/licencek.tsv + eszkozok/lexikon_general.py | forras=general.py --cel lexikon (a 7 érintetlen oldal renderje bájtra azonos a változtatás előtti renderrel) | ts=2026-10-05.*

### 2026.10.04 (F43_LXX_BRIDGE_BRIEF.md — N29 lezárva, a brief D7 döntése szerint):
* N29 — a teljes KJV/ASV-forrás keresése (FJ-ellenőrzés, 2026.09.25). **LEZÁRVA (F43, 2026.10.04; felhasználó):** a KJV-ág teljesült az F19-ben (`konkordancia/KJV_Strongs_teljes.tsv`, 349 308 sor, 31 099 címkés vers, Public Domain; állapot: `importált, javaslat`). Az ASV-ág a D7 szerint megszűnik: az ASV-t nem importáljuk (felhasználó, 2026.10.02), mert a szerepmátrix 9. szerepét a KJV tölti be, és az ASV-nek nincs szerepe. Az eBible-ASV forráshibás volt (F19.7, DT19). Ha mégis igény lenne rá, a megnevezett pótlás a luvlylavnder ASV-Strongs (CC0, 31 086 vers). *(F19 (#19), DT19; `F43_LXX_BRIDGE_BRIEF.md` D7; `naplok/ELLENOR_F19.md`)*
  *Proveniencia: scope=konkordancia/KJV_Strongs_teljes.tsv | forras=eszkozok/f19_ellenorzes.py | ts=2026-09-30.*

### 2026.10.03 (F46_BDB_KONYVFELOLDAS_BRIEF.md — N-F34 és N-F34c lezárva, DT-F46 (6)):
* N-F34 — a BDB „ψ”-hiba B/R maradéka (a `naplok/F34_M2_maradek.tsv` 153 sora). **LEZÁRVA (F46.7):** az F46 teljes könyvfeloldási felmérése 141 sort a csere-táblára vett (37 `psi_maradek`, a többi valódi típusa szerint), 12 sor helyesnek bizonyult (a vers létezik, a Strong-próba sikeres); a jóváhagyott sorok a DT-F46 szerint cserélődtek, a többi az N-F46a kézi listáján. *(F34 (#34), DT-F34b/DT-F34c; `naplok/BDB_KONYVFELOLDAS_naplo.md`)*
* N-F34c — nem ψ eredetű könyvfeloldási hibák (Dt→Dan, `Lev 28:17` típus), a Dán 22:14 (H8034) kizárásának felülvizsgálata. **LEZÁRVA (F46.7):** a `Dan c:v` tokenek közül `Dan 4:14` (H2742) → Jóel 4:14 (a Károli-alak MT→Károli átváltva: Jóel 3:14), `Dan 21:15` és `Dan 24:2` (H8478) → 1Móz javaslat a >500 előfordulási szabály miatt kézi; a H8034 `Dan 22:14`/`Dan 22:19` → 5Móz javaslat szintén kézi (>500), ezért a DT-F34c védett sora nem változott; `Lev 28:17` (H0398) kézi (két egyenrangú jelölt). A maradék az N-F46a-ban. *(F34 (#34), DT-F34c 3. pont; F46, DT-F46)*

### 2026.10.02 (F41_BSB_UJRAMERES_BRIEF.md — N-F41c felvéve és lezárva):
* N-F41c — a `bsb_import.py` a `Lam`/`JSir` (F28.9 átnevezés) miatt a Siralmakat néma 0%-os könyvként mérte volna, és kihagyta volna az importból (a TAHOT_kivonat/Károli-kulcs `Sir`-t használ, a könyvtábla `JSir`-t). F41: a mérés a forrás-nevet használja (`forras_nev`), és a szkript hangos hibával leáll, ha egy ószövetségi könyvnek 0 illesztett sora / 0 egyező verse van, vagy a TAHOT_kivonatban nincs ilyen nevű könyv (`eszkozok/fj2/bsb_import.py`; a `Lam` sorok az újraimport után sorról sorra azonosak, `naplok/F41_nulladiff.txt`). A Macula-generátor aliasa külön tétel (N-F35a).
* N-F41e — a BSB-importot leíró dokumentumok az F41 előtti állapotot mutatták. **ELVÉGEZVE (F41.7, a merge előtt): `adat/datasetek.tsv`, `konkordancia/README.md`, `adat/SEMA.md`, `adat/szotar_szerepek.tsv` frissítve (36 ÓSZ-könyv, 278 125 sor, a 6./7. oszlop, a számozás); `adat/licencek.tsv`-ben nincs számadat, nem változott.** *(ÚJ, F41.3, `konkordancia/README.md` BSB_Strongs-szakasz, `adat/SEMA.md`, `adat/datasetek.tsv` BSB-sorok, `adat/licencek.tsv`, a jelen fájl 6. nagy tétele; a számot (N-F41e) a main-Action osztja ki)*
  Az F41 `ir` mezője nem tartalmazza őket, ezért nem frissültek: „31 ÓSZ-könyv” → 36 (új: 1Sám, Préd, Ézs, Hós, Jón; továbbra is kimarad: 2Sám, Ezsd, Dán), az `Igehely` számozása már nemcsak a Zsoltárokban a TAHOT-é (4Móz 29/30; 1Sám 23/24; 1Kir 22; Ézs 9; Hós 11/12; Jón 1/2; a 4Móz 12/13, a Préd 11/12 és az Ézs 2/3 a BSB/KJV-számozás, = WLC, DT-F41f), a Jób 38–41 KJV-számozású, a 6. oszlop (`Angol szó állapota`), a 7. oszlop (`Számozás`: `mt` / `kjv` / `ellenorizetlen`, versszintű WLC-összevetésből), a mellékletek egyes szövegei („a nem-zsoltár könyvek eltolását az import nem javítja”).
* N-F41f — a F41-brief számozási példái hibásak (1Kir 4/5, Jóel 2/3, Neh 3/4). **ELVÉGEZVE (F41.1): a javítás a brief címsora alatti megjegyzésben van.** *(ÚJ, F41.1, megjegyzés)* A brief 2. szakasza ezeket eltolt fejezetként hozta példának; a Strong-illeszkedés szerint a TAHOT_kivonatban a BSB-vel azonos számozásúak (0 eltolt vers); a javítás a brief címsora alatti megjegyzésben van (a címsor változatlan).

### 2026.09.30 (F16_BSB_IMPORT_BRIEF.md — N30 lezárva):
* N30 (BSB-import feltétele: teljes Genezis-összevetés) lezárva: az 1Mózes-mérés az F06-ban (PR #75, 98,83%, 1515/1533 vers), a teljes Biblia mérése és importja az F16-ban (`eszkozok/fj2/bsb_import.py`, `naplok/F16_bsb_lefedettseg.tsv`): 31 ÓSZ-könyv ≥ 95% → importálva (`konkordancia/BSB_Strongs.tsv`, 242 597 sor, CC0, BSB commit `a4a2c05`; a zsoltár-verseltolás javítása után, F16.8); 8 ÓSZ-könyv a küszöb alatt, az ÚSZ szándékosan kimarad (DONTESEK DT6, javaslat). Az 1Mózes újramért értéke azonos az F06-éval.

### 2026.09.28 (F05_SZOTAR_BRIEF.md S1.5 — N38 felvéve és lezárva):
* N38 — az `eszkozok/ellenoriz.py` 10. szabálya (`forditas_ubs.tsv`) az S1.1 óta HIBA-val (kilépési kód 2) állt le minden futtatáskor, észrevétlenül. A `forditas_ubs.tsv` a SZOTAR S1.1-ben megszűnt (`adat/SEMA.md` 2.10, D31, 51-soros `adat/forditasok.tsv`-re költözött), de a 10. szabály (`LEXV2_2 tablak`) a régi fájlnevet feltétel nélkül olvasta be — a hiányzó fájl kivétele az egész szkriptet `HIBA`-val állította le, mielőtt bármi más lefuthatott volna. Mivel az S1.1–S1.4 közben egyetlen menet sem futtatta le az `ellenoriz.py`-t teljes egészében, ez a törés hetekig rejtve maradt volna a következő tényleges futtatásig. Javítva az S1.5-ben (ugyanaz a commit, amely a 13-14. szabályt bevezette): a `forditas_ubs.tsv`-részt a szabály RETIRED-ként kihagyja, ha a fájl hiányzik (a kulcs-/hash-ellenőrzést a 13. szabály veszi át); a `lxx_dontesek.tsv`-rész változatlan. `naplok/SZOTAR_S1_5_ellenoriz_jelentes.md`: RENDBEN 11, SÉRTÉS 0, KÉZI 2, JELENTÉS 3, kilépési kód 0.

### 2026.09.28 (F05_SZOTAR_BRIEF.md S1.1 — N34 lezárva):
* N34 — a megszűnt `forditas_ubs.tsv` `megjegyzes` mezője (4 sor: G1311/88.266, G1944/33.475, G5351/88.266, G5590/9.20) pótolva: az `adat/forditasok.tsv` felvett egy opcionális `megjegyzes` oszlopot (`adat/SEMA.md` 2.14), a 4 sor jegyzete mindkét származó soron (`definicio_hu`, `glosszak_hu`) megőrizve. A `nulladiff.sh 8f5a1eb` a két D31-csere mellett továbbra is üres diffet ad.

### 2026.09.25 (CREMER_OCR_BRIEF.md v3 — lezárva):
* A Cremer teljes szövegének javítása külső modellekkel (O-pipeline) lezárva, D22. Eredmény: a cremuoft-tétel azonosítása (görög betűs OCR), élőfej-alapú leképezés, módszertani tanulságok (D20–D21), ellenőrző csomag (`96c4c5d`). A Cremer a szótári rétegbe sem kerül be (SZOTAR D16).
* Cremer utóélete (korábbi 5. tétel): a Cremer sem szövegként, sem hivatkozásként nem kerül a szótári rétegbe — `F05_SZOTAR_BRIEF.md` D16 (a felhasználó döntése). A korábbi javaslat (oldalhivatkozás archive.org-linkkel; célzott kinyerés és becslése) a git-történetben (`eae2143`).
* Szerepmátrix (korábbi 6. tétel): forrásszabály — csak saját repóban tárolható és onnan renderelhető forrás kerül be (`F05_SZOTAR_BRIEF.md` D17, a felhasználó döntése). Ezért a NIDNTTE/NIDOTTE nem kerül be. A megbeszélés rögzített pontjai (NIDNTTE/NIDOTTE-javaslat és idézési szabálya, a Cremer/Girdlestone-sor átnevezése, licencoszlop, az elvetett alternatív mátrix-javaslat indoklása) szó szerint a git-történetben (`eae2143`, NYITOTT_FELADATOK.md 6. tétel).
* TWOT-szám: marad, a D17 kivételeként (`F05_SZOTAR_BRIEF.md` D17, a felhasználó döntése, 2026.09.25).
* Utómunka: új 5. tétel (licencoszlop, törzscikk-regenerálás).

### 2026.09.23 (RENDER_BRIEF.md v4, 1. menet — R1.1–R1.8):

* **A hét lexikonoldal-rés forrása mostantól a tanulmány, nem a lexikonoldal** (RENDER_BRIEF.md G1–G4) — `adat/res_forras.tsv` (56 sor: ISTENTISZT-001 7 sora `tanulmany`, a többi 49 egyelőre `lap`, változatlanul); `eszkozok/lexikon_general.py` `res_blokkok_alkalmaz()`/`modell_epit()` a fejlécet a táblából, a törzset a tanulmány/napló `<!-- RÉS-KEZDET/VÉGE -->` jelölői közül állítja össze. Nulla-diff igazolva (`git status --porcelain lexikon/*_TUDOMANYOS.md` üres az `--ir` után).
* **ISTENTISZT-001 visszaírás**: a tanulmány (`tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`) és a kereszthivatkozás-napló (`tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md`) megkapta a lexikonoldal hét résének tartalmát, jelölőkkel; a `minosites` a naplóba (G14), a `2b` új szakaszként a "2. Eredeti nyelvi összevetés" után (G15/D22), a `modszertan` csak a "6. Napló-frissítés" szakaszt váltja fel (D23).
* **Törzscikk-generátor** (`eszkozok/torzscikk_general.py`, `general.py --cel torzscikk`) — mind a 8 motívumra `lexikon/[ID]_TORZSCIKK.md`, a lexikonoldalból renderelve (sablon: `sablonok/8_PaRDeS_torzscikk_sablon.md`). Az 5. szakasz a régi pilot-szócikk-dump helyett a G6 szerepmátrixot (`adat/szotar_szerepek.tsv`, 20 sor) és egy szavankénti lefedettségi mátrixot mutat. Az ISTENTISZT-001 törzscikke a pilottól igazoltan csak az 5. szakaszban és a láblécben tér el (`naplok/RENDER_R1_pilot_diff.tsv`).
* `eszkozok/ellenoriz.py` 11–12. szakasz: a `tanulmany`/`adat` forrású rések egyezése a lexikonoldallal (SÉRTÉS eltérésnél), és a `lap` forrású sorok száma (JELENTÉS, ma 49).
* **Nyitva maradt, tudatosan nem javított apróság**: a törzscikk-generátor `KIEJT` táblája (SBL→magyaros kiejtés-javítás) csak az ISTENTISZT-001-nél ismert 5 szót fedi — a többi motívum egyéb szavai nyers, SBL-stílusú átírással jelennek meg a törzscikkben, amíg a `F05_SZOTAR_BRIEF.md` S3 (`kiejtes.py`) nem old meg egy általános átírást. Nem hiba, tudatos hatókör-szűkítés (l. `sablonok/8_PaRDeS_torzscikk_sablon.md`).

### 2026.09.09-10 (chat-munkamenet, harmadik szakasz):

* **ISTENTISZT-001 lexikon-oldal teljes frissítése** — a study 29-igehelyes állapotára hozva (17→29 tétel): Zak 13:9 + 6 ÚSZ-hely (1Kor 1:2, 2Tim 2:22, 1Pét 1:17, ApCsel 9:14, 9:21, 22:16) pótolva, D-minta dokumentálva. Ezen felül ~15 kisebb, review-alapú javítás: tartalom/proveniencia-keveredés (inline dátum-tagek, "Forrás:" sorok, első személyű ellenőrzési állítások mind NAPLO-formába), hiányzó üres sor NAPLO előtt (10+1 hely), csak eredeti nyelvű szöveg blockquote-ban (fordítás normál bekezdésbe), casual "mi"-hangú fogalmazás semlegesítve, PaRDeS-réteg keveredés javítva (Drash/Remez szétválasztva), félrevezető szóhasználat ("társválasztási") pontosítva, üzemeltetői megfogalmazás + elavult "LXX-hiba" állítás javítva, hiányzó kiejtés pótolva.
* **Napló-/formázási-/hangnem-fegyelem szabályok rögzítve** mindkét sablonban — `6_PaRDeS_lexikon_oldal_sablon.md` (L6 kapu-tétel), `4_PaRDeS_tematikus_sablon.md` (Q6 kapu-tétel) — konkrét triggerekkel (inline dátum-tag, "Forrás:" sor, első személyű ellenőrzés, NAPLO üres sor, blockquote-fordítás, casual hangnem, réteg-keveredés), a mai ISTENTISZT-001-es átfésülés tapasztalatai alapján.
* Melkizedek-study: Zsolt 76:3 BDB-hivatkozás pótlása (H8004, a BDB szócikk explicit összeköti Gen 14:18-cal) — a sor korábban üresen, kötőjelekkel szerepelt.
* `Karoli_Strong_kivonat.tsv` bővítése 11 sorral — Melkizedek (2Móz 19:6, Zak 6:13, fejenként 2 Strong-számmal) és Segítségül hívni (Zak 13:9 + 6 ÚSZ-hely).
* Segítségül hívni-study: **KAPCSOLATOK Típus-mező szerint strukturált tábla** hozzáadva (új "1/b" szakasz) — az öt típus rövid meghatározásával és mind a 19 pár-szintű kapcsolat besorolásával; a 2Móz 33:19/34:5 eset itt kapta meg először a Variáns, az 1Kir 18:24 belső kontrasztja a Kontraszt formális jelölést.
* ISTENTISZT-001 lexikon-oldal KAPCSOLATOK szakasza **áttérve a végleges 5 kategóriás Típus-mezőre** — a korábbi laza elnevezések (KÁNONI ÍV, ISMÉTLÉS/VISSZATÉRÉS, ÖRÖKLÉS/MINTAÁTVÉTEL, ESZKATOLÓGIAI KITERJESZTÉS, FORMULA-ÁTVÉTEL, NYITOTT) mind lecserélve; legenda-tábla hozzáadva; a korábbi "be nem sorolható" 2Móz 33:19/34:5-eset most Variáns, az 1Kir 18:24 explicit Kontraszt.
* **NAPLO-jelölés retrospektív egységesítése** — mechanikus grep-alapú szűrés mind a 30 másik tematikus/bővített study-fájlon (inline dátum-tag, "Forrás:" sor, első személyű ellenőrzési állítás, NAPLO üres sor, blockquote-fordítás) — csak egy valódi találat (`1Moz_4v1-24_bovitett.md`, 7. pont), javítva. A korábbi feltételezés ("valószínűleg ugyanazok a hibák ott is előfordulnak") nem igazolódott.
* `4_PaRDeS_tematikus_sablon.md` **Q2 pont kibővítve** — minden TSK-jelölt, ami a study táblázatában még nem szereplő, új igehelyre mutat, saját egyedi ✅/❌ minősítést igényel, nem elég a nyers találatok listájában megemlíteni. A szabályt a Melkizedek-study 1Pét 2:9-es esete alapozta meg (l. alább).
* Melkizedek-study: **1Pét 2:9 pótlása** — szó szerinti LXX-idézés (βασίλειον ἱεράτευμα, azonos G0934+G2406 pár, mint LXX 2Móz 19:6), TSK 22 szavazat, amit a TSK-audit már 2026.09.08-09-én megtalált, de sosem került át a minősítő táblázatba. Jel 1:6 és Jel 5:10 (ugyanabban a TSK-sorban) formálisan minősítve és elutasítva — más görög szavak (βασιλείαν, ἱερεῖς), csak tematikus párhuzam.
* ISTENTISZT-001 lexikon-oldal: **módszertani tisztázó bekezdés** a KAPCSOLATOK-diagram hatóköréről — explicit kimondva, hogy a diagram nem a lexikai formula-egységet ábrázolja (amiben mind a 29 igehely "kapcsolódik" egymáshoz), hanem csak az egyedileg indokolható, formulán túli kapcsolatokat; ezért nem egyetlen csillag-alakzat 1Móz 4:26-ból, hanem több független klaszter.
* Tervezési napló **17. pont kiegészítve**: a `naszut` projekt Hugo-használatára vonatkozó korábbi feltételezés korrigálva (nem Hugót használ); Docsy/SermonIndex/BibleUp/Floating UI technikai kutatás dokumentálva, konkrét technikai vázlattal (JSON adatszerkezet, Hugo partial-kód).
* Tervezési napló **18. szakasz (DÖNTÉS)**: a Károliba épített kereszthivatkozás megjelenítése — induló megoldásként egyszerű, típus nélküli link minden megjelölt versen, nincs típusonként színezett popup; ez lezárja a 17. pont inline jelölés/interakció nyitott kérdéseit induló választásként.
* Tervezési napló **19. szakasz**: a három kereszthivatkozás-pilóta dokumentálva, technikai tanulsággal (Floating UI CDN-nél egyező core/dom verziószám szükséges).
* **Károliba épített kereszthivatkozás — 3 kézzel épített HTML-pilóta a repóba emelve** (`motivumlog/kereszthivatkozas_pilot/`): `01_demo_2_vers.html` (első próba, típusonként színezett), `02_teljes_pilota_29_vers.html` (mind a 29 igehely, egyszerűsített link-megoldás, valódi Károli-szöveggel), `03_floating_ui_pilota.html` (gazdag popup-verzió próbája Floating UI-val, összehasonlításra).

### 2026.09.09 (chat-munkamenet, második szakasz):

* A/B/C tipológia + 1Kir 18:24 kontraszt felvéve nyitott kérdésként a `Bibliai_Motivumlexikon_tervezesi_naplo.md`-be (5. és 6. pont), commit `dbdf711`
* Gen 3:10/3:11 H5903 join-sorok pótolva a `Karoli_Strong_kivonat.tsv`-ben, commit `9612316`
* `4_PaRDeS_tematikus_sablon.md` Q4 pontja pontosítva — eredet-hivatkozás a `6_PaRDeS_lexikon_oldal_sablon.md` L4 pontjára, fejléc v14-re emelve, commit `8e4ec99`
* `NYITOTT_FELADATOK.md` Tehóm/Seól sora korrigálva — elavult jelölt-számok pontosítva, commit `bdedea5`
* KAPCSOLATOK Típus-mező öt kategóriás döntése rögzítve a `Bibliai_Motivumlexikon_tervezesi_naplo.md`-ben (Előkép/Párhuzam/Beteljesedés/Kontraszt/Variáns — Előkép/Párhuzam/Beteljesedés megtartva, Kontraszt és Variáns új; lezárja az 5. és 6. nyitott pontot) — commit-hash a chatben nem lett külön megerősítve, tartalma friss `codeload`-dal ellenőrizve
* Károliba épített kereszthivatkozás megjelenítési ötletelése naplózva a `Bibliai_Motivumlexikon_tervezesi_naplo.md` 17. szakaszában, explicit "NEM döntés" jelöléssel, commit `e408f93`
* בָּרַךְ (H1288) korrekció — ellenőrizve, kiderült, hogy ez már 2026.09.03 óta lezárva volt (`genezis/1Moz_1v2-2v3_bovitett.md` v5) — a nyitott listán tévesen szerepelt, most eltávolítva
* "6 további tematikus study v12-compliance" szám javítva 5-re — kiderült, hogy a Segítségül hívni-study már 2026.09.08 óta megkapta a Q1-Q5 kaput, ez korábban nem lett levonva a számból

### 2026.09.09 (chat-munkamenet, első szakasz):

* Melkizedek-study v1 → v7, teljes v12-compliance — `tematikus_lezart/Melkizedek_tematikus.md`, commit `c1e327a`. Új tartalom: 2Móz 19:6, Zak 6:13, Zsolt 76:3, Zsolt 110:4 részletes eskü-formula/grammatika/legitimáció-levezetés, Zsid 7:20-22 eskü-érv, ἀφωμοιωμένος/μαρτυρούμενος vitatott pont. Táblázat 7 oszlopra igazítva a valódi v13 sablonhoz. Kötelező kereszthivatkozás-napló létrehozva (`tematikus_lezart/naplok/Melkizedek_tematikus_kereszthivatkozas_naplo.md`).
* "Segítségül hívni az Úr nevét" study — soha nem lett kiadva korábban (a repóban 2026.08.17 óta a 17-igehelyes v1 állt, a 24-igehelyes bővítés csak lokálisan létezett) — most pótolva, `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md`, commit `8df6650`.
* ISTENTISZT-001 lexikon TUDOMÁNYOS oldal — tartalom/proveniencia-tisztítás, commit `99f63dc`. Tartalmilag NEM frissítve a study 24-igehelyes állapotára akkor — l. a harmadik szakasz Lezárva-tételét, ahol ez már megtörtént.
* Mondaton belüli tartalom/proveniencia-keveredés — szisztematikus felismerés és javítás a Melkizedek- és a segítségül hívni-studyn: a korábbi NAPLO-jelölés szabály feltételezte, hogy a keveredés mindig mondathatáron fut, de mondaton belül is előfordul — a mondatot ilyenkor ketté kell vágni, a tartalmi mag marad, a proveniencia helyben (nem centralizálva) kerül 【NAPLO】 blokkba.
* "Logikai kötőszó szerinti bontás" — új, kötelező lépés bevezetve mindhárom sablonba (`4_PaRDeS_tematikus_sablon.md` v13, `2_PaRDeS_bovitett_sablon.md` v19, `5_Melyelemzes_prompt_sablon.md` v8, commit `87dcddf`). Konkrét eset motiválta: a Melkizedek-study "Zsid 7:1-28" sora hónapokig lefedettnek számított, miközben a 7:15-19 μαρτυρεῖται-érvelés sosem lett kifejtve.
* TSK-teljes-lista szabály — a `PaRDeS_gyorsreferencia.md`-be építve (v11, commit `5f2068e`), ami mind a három sablon közös hivatkozási pontja. Konkrét eset: a Zsolt 110:4 TSK-listájának legmagasabb szavazatú tétele (Zsid 7:17, 25 szavazat) hónapokig kiaknázatlan maradt, mert csak a top 1-2 találatot néztük meg, nem a teljes, Votes ≥ 15 szűrt listát.
* `Code_prompt_melkizedek_v12_audit.md` elavultnak jelölve — sosem futott le, azóta tartalmilag (v2→v7) és eljárásilag is túlhaladott.

### 2026.09.08 (chat-ellenőrzés):

* `lexikon-oldal-minosegi-kapu-2026-09-07` branch merge-státusza megerősítve — friss `codeload`-tarball ellenőrzés a `main`-en igazolta, hogy mindkét Quality Gate ténylegesen bekerült (`4_PaRDeS_tematikus_sablon.md` Q1-Q5, 176-220. sor; `6_PaRDeS_lexikon_oldal_sablon.md` L1/L3/L4/L5, 222-256. sor) — a korábbi bizonytalanság ("nem kapott explicit megerősítést") tárgytalan
* "Párhuzam" funkció-indoklás pontosítva (Zsolt 105:1, 1Krón 16:8, Ézs 12:4) — a "nem közvetlen narratív folytonosság a genezisi vonallal" megfogalmazás félreérthető volt (mintha a mózesi hagyománnyal ne lenne kapcsolat); pontosítva "formulai/liturgikus örökség a genezisi hagyományból, nem narratív folytonosság"-ra, mindkét érintett fájlban (`Segitsegul_hivni_az_Urat_tematikus.md`, `ISTENTISZT-001_TUDOMANYOS.md`)
* Olvasói szint pilot lezárva és naplózva — l. 4. nagy tétel fent
* Segítségül hívni-study Q1-Q5 Minőségi kapu retroaktívan pótolva, egy hiányzó táblázat-sor (Zak 13:9) és hat új ÚSZ igehely felvéve, D-minta dokumentálva és kizárva

### 2026.09.07 (második folytatás):

* Lexikon-adatstruktúra döntés dokumentálva — a Thayer/LSJ/SECE/BDB TSV-k lapos, 3 oszlopos (`Strong_padded | Strong_eredeti | Teljes_szocikk`) struktúrája végleges, tudatos döntés, nem elmaradt granulálás (`motivumlog/Bibliai_Motivumlexikon_tervezesi_naplo.md` 15. pont)
* Reprodukálható lexikon-oldal sablon létrehozva (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`), az ISTENTISZT-001 pilot két fájljából visszafejtve
* Napló-szinkron szabály kiterjesztve — a `PaRDeS_motivumok.md`-vel való szinkron nemcsak kezdeti lezáráskor, hanem utólagos bővítésnél is kötelező, ugyanabban a commit/PR-ben (`sablonok/4_PaRDeS_tematikus_sablon.md`, `PaRDeS_gyorsreferencia.md`)
* PaRDeS-keretrendszer szakasz pótolva az ISTENTISZT-001 pilotban (`ISTENTISZT-001_TUDOMANYOS.md`) — az eredeti pilot hiányossága volt, nem mai hiba; a `6_` sablon kiegészítve egy kötelező "1/b" szakasszal, hogy ez jövőben ne maradjon ki
* Két Quality Gate bevezetve a `biblemate-agentic-workspace` quality-gate *ötletéből* adaptálva, saját szöveggel: `4_PaRDeS_tematikus_sablon.md` Q1-Q5 (a Melkizedek-hiányosság alapján), `6_PaRDeS_lexikon_oldal_sablon.md` L1/L3/L4/L5 (a Zak 6:13/Melkizedek kereszt-motívum-keveredés alapján)
* `biblemate-agentic-workspace` licenc-helyzet tisztázva: UniqueBible (SQLite-adatbázisok forrása) GPLv3; a workspace maga (125 skill, persona-definíciók) license nélküli, "minden jog fenntartva" — adatbázis-lekérdezés jogilag rendben, minta-átvétel (pl. quality-gate ötlete) jogilag tiszta és megtörtént, szó szerinti fájl-átvétel nem történt és nem is javasolt

### 2026.09.07 (folytatólagos szakasz):

* BDB "16t" kérdés véglegesen lezárva — három egymástól független módszerrel (TAHOT pozíció-alapú frázis-scan, laza vers-szintű co-occurrence a `morphology.sqlite`-on, ClauseID-alapú szintaktikai scan ugyanazon adatbázison) sem került elő új, valódi igehely; a jelölt Deut 32:3 maga a BDB szerint más szócikk-pontba (3.b "kihirdetni") tartozik, nem a mi 2.c "invokálni" pontunkba
* Licenc-tisztázás lezárva 4 lexikonra: Thayer és BDB (közkincs), LSJ (Perseus, nyíltan újrafelhasznált), SECE (csak közkincs Strong-szöveg + funkcionális számkódok) — mind feldolgozható; MCGED (Mounce, 1993, copyright) — kizárva a rendszeres feldolgozásból
* Thayer, LSJ, SECE teljes feldolgozása (PR #53): 4 új TSV (`Thayer_teljes.tsv` 5426 sor, `LSJ_teljes.tsv` 5522 sor, `SECE_H_teljes.tsv` 8674 sor, `SECE_G_teljes.tsv` 5523 sor) + 1 új, újrafelhasználható script (`eszkozok/elofordulas_szamlalo.py` — a kizárt MCGED "Frequency" funkcióját pótolja, a repó saját TAGNT/TAHOT-kivonataiból, licenc-kockázat nélkül)
* Pilot→study visszaírás lezárva — a scope a vártnál kisebb volt: a 4 igehelyből 3 (Zsolt 105:1/1Krón 16:8, Ézs 12:4, Jer 10:25/Zsolt 79:6) már 2026.09.05 óta a study-ban volt; csak Róm 10:14 (TSK-eredetű, 2026.09.06) és az A/B/C tipológia hiányzott ténylegesen — mindkettő beépítve a `Segitsegul_hivni_az_Urat_tematikus.md`-be
* `Karoli_Strong_kivonat.tsv`: Róm 10:14 (G1941) sor pótolva

### 2026.09.07 (korábbi szakasz):

* 12 SQLite-lexikon + Motívumlexikon-pilot fájlok repóba emelése (PR #48)
* Alapadatok szakasz (repó, branch-lista, raw/codeload URL-minták) a pilot átadási dokumentumban (PR #49)
* Lexikon-rangsor kiegészítés — projekt-szintű SECE/Thayer/MCGED/LSJ rangsor + héber oldal (TBESH-konszolidáció, SECE görög-megfelelő lista) (PR #50)
* LXX-híd 2 tétele lezárva: Zsolt 116:4 Strong-címke javítva (G4506→G1941), Zsolt 116:17 "hiánya" tévhitnek bizonyult (a görög LXX autentikusan nem fordítja a vers második felét) (PR #51)
* TAHOT teljes korpuszos frissscan — nem hozott új igehelyet; a Zsolt 116:4,13,17 hármas kiderült, hogy már 2026.09.05 óta a hivatalos 17 igehelyes listában szerepel

2026.09.05 és korábbi: l. `Atadasi_dokumentum_2026_09_07_TELJES.md` 1–2. pontja (3/b és 3/c terv, ISTENTISZT-001 v12-compliance és motívum-ID átnevezés).
