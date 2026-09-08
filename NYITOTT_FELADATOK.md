Nyitott feladatok
Ez a fájl a projekt aktuális, karbantartott feladatlistája. Átadási dokumentum kérésekor frissítendő: a lezárt tételek áthelyezendők a "Lezárva" szakaszba (dátummal), az újonnan felmerülő tételek felveendők a megfelelő szakaszba.
Utolsó frissítés: 2026.09.08

Nagy, tartalmi döntést igénylő tételek

1. `biblemate-agentic-workspace` (eliranwong) mélyebb, rendszeres integrációja — a `morphology.sqlite` (teljes, vers-soronkénti héber/görög morfológiai adatbázis, Google Drive-on, file ID `11QfpwEd5fjdDglPiqzygLNN99AVz2mw5`), a `cross-reference.sqlite`, és a `search_retriever.py` közül mi érné meg ténylegesen beépíteni a saját workflow-ba. A licenc-státusza tisztázva (UniqueBible/GPLv3 az adatbázisokra, a workspace maga license nélkül — l. Lezárva), de a rendszeres integrációról nincs döntés.
2. Melkizedek-study v12-audit befejezése — a `Melkizedek_tematikus_v2.md` draft (Melkizedek személye + királyi papság rendje, két új lelettel: 2Móz 19:6 és Zak 6:13/BDB H3548 "priest-king") elkészült, de hiányzik belőle a kötelező "3. A PaRDeS keretrendszer" szakasz (a Quality Gate Q1 kritériuma szerint) — a felhasználó ezt "stop"-tal megállította, mielőtt commitolva lett volna. A draft és a hozzá tartozó Code-prompt (`Code_prompt_melkizedek_v12_audit.md`) csak lokálisan létezik (`/mnt/user-data/outputs/`), a repóban a `Melkizedek_tematikus.md` változatlan, eredeti (v1) formájában van.
3. Publikálási terv — hosszú megbeszélés a magyar nyelvű lexikon-anyag nyilvános közzétételéről. Végkövetkeztetés: van értelme, "kutatási napló"/"motívum-jegyzetek" címmel, TUDOMÁNYOS mélységi szinten (nem hígítva), a meglévő Netlify/Hugo-munkamódszerrel. Licenc-újraellenőrzés szükséges nyilvános közzétételre. Egyetlen konkrét lépés sem indult el.
4. "Én vagyok" tematikus motívum-jelölt (ÚJ, 2026.09.08, chat-kutatás — még sehol nincs repóban dokumentálva) — 2Móz 3:14 (אֶהְיֶה אֲשֶׁר אֶהְיֶה ⇒ LXX ἐγώ εἰμι ὁ ὤν) és az Ézsaiás "Ani Hu" klaszter (אֲנִי הוּא) mint LXX-híd Jézus ἐγώ εἰμι-mondásaihoz Jánosnál. Pozíció-alapú TAHOT/TAGNT-ellenőrzéssel megerősítve: 6 valódi ÓSZ Ani Hu-hely (Ézs 41:4, 43:10, 43:13, 46:4, 48:12, 52:6 — a kezdeti 20 jelöltből 14 hamis találatnak bizonyult), 8 abszolút ÚSZ ἐγώ εἰμι-mondás Jánosnál (4:26, 6:20, 8:24, 8:28, 8:58, 13:19, 18:5, 18:6, 18:8), 7 predikátumos ἐγώ εἰμι-mondás (6:35 kenyér, 8:12 világosság, 10:7/9 ajtó, 10:11/14 jó pásztor, 11:25 feltámadás/élet, 14:6 út/igazság/élet, 15:1/5 szőlőtő). Kiemelt lelet: Jer 2:21 (זֶרַע אֱמֶת, "igaz mag") mint lehetséges lexikai/fordítási gyökér a Ján 15:1 ἀληθινή ("igazi") jelzőjéhez — a hét predikátumos kép közül ez az egyetlen lexikai szintű, a többi hat tematikus/kép-szintű. Formális PaRDeS-feldolgozás (négyforrásos audit, sablon szerinti tanulmány) még nem indult el.

Kisebb, korábbról nyitva maradt tételek

* `Karoli_Strong_kivonat.tsv` bővítése az új igehelyekkel
* A/B/C tipológia + 1Kir 18:24 kontraszt felvétele a `Bibliai_Motivumlexikon_tervezesi_naplo.md`-be
* 3 ÚSZ study első audit (Róm 8:10, Zsid 4:12, 1Thessz 5:23)
* Gen 3:10/3:11 H5903 join-sorok
* בָּרַךְ (H1288) korrekciós Code-prompt újbóli jóváhagyása
* 7 további tematikus study v12-compliance (nagy, több körös munka) — a Quality Gate (Q1-Q5) most már explicit követelményként vonatkozik rájuk, ha bármelyiket lezárjátok/átdolgozzátok
* Tehóm (27) és Seól (63) jelölt-listái — valószínűleg nem hiányosság, nincs explicit döntés
* `4_PaRDeS_tematikus_sablon.md` Q4 pontosítása — a Q4 valójában a `6_` sablonnál (lexikon-oldal) történt esetre hivatkozik, nem a tematikus study-kra; pontosítható vagy hagyható, nincs döntés
* Nevesített tanítói szakasz pótlása az ISTENTISZT-001 pilotban (`motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md`) — döntés megvan: "halvány, tematikus, nem bizonyító erejű" jelöléssel, változtatás nélkül átvehető a `Segitsegul_hivni_az_Urat_tematikus.md` Alkalmazás-szakaszából; csak a végrehajtás hiányzik

Lezárva

2026.09.08 (chat-ellenőrzés):

* `lexikon-oldal-minosegi-kapu-2026-09-07` branch merge-státusza megerősítve — friss `codeload`-tarball ellenőrzés a `main`-en igazolta, hogy mindkét Quality Gate ténylegesen bekerült (`4_PaRDeS_tematikus_sablon.md` Q1-Q5, 176-220. sor; `6_PaRDeS_lexikon_oldal_sablon.md` L1/L3/L4/L5, 222-256. sor) — a korábbi bizonytalanság ("nem kapott explicit megerősítést") tárgytalan

2026.09.07 (második folytatás):

* Lexikon-adatstruktúra döntés dokumentálva — a Thayer/LSJ/SECE/BDB TSV-k lapos, 3 oszlopos (`Strong_padded | Strong_eredeti | Teljes_szocikk`) struktúrája végleges, tudatos döntés, nem elmaradt granulálás (`motivumlog/Bibliai_Motivumlexikon_tervezesi_naplo.md` 15. pont)
* Reprodukálható lexikon-oldal sablon létrehozva (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`), az ISTENTISZT-001 pilot két fájljából visszafejtve
* Napló-szinkron szabály kiterjesztve — a `PaRDeS_motivumok.md`-vel való szinkron nemcsak kezdeti lezáráskor, hanem utólagos bővítésnél is kötelező, ugyanabban a commit/PR-ben (`sablonok/4_PaRDeS_tematikus_sablon.md`, `PaRDeS_gyorsreferencia.md`)
* PaRDeS-keretrendszer szakasz pótolva az ISTENTISZT-001 pilotban (`ISTENTISZT-001_TUDOMANYOS.md`) — az eredeti pilot hiányossága volt, nem mai hiba; a `6_` sablon kiegészítve egy kötelező "1/b" szakasszal, hogy ez jövőben ne maradjon ki
* Két Quality Gate bevezetve a `biblemate-agentic-workspace` quality-gate *ötletéből* adaptálva, saját szöveggel: `4_PaRDeS_tematikus_sablon.md` Q1-Q5 (a Melkizedek-hiányosság alapján), `6_PaRDeS_lexikon_oldal_sablon.md` L1/L3/L4/L5 (a Zak 6:13/Melkizedek kereszt-motívum-keveredés alapján)
* `biblemate-agentic-workspace` licenc-helyzet tisztázva: UniqueBible (SQLite-adatbázisok forrása) GPLv3; a workspace maga (125 skill, persona-definíciók) license nélküli, "minden jog fenntartva" — adatbázis-lekérdezés jogilag rendben, minta-átvétel (pl. quality-gate ötlete) jogilag tiszta és megtörtént, szó szerinti fájl-átvétel nem történt és nem is javasolt

2026.09.07 (folytatólagos szakasz):

* BDB "16t" kérdés véglegesen lezárva — három egymástól független módszerrel (TAHOT pozíció-alapú frázis-scan, laza vers-szintű co-occurrence a `morphology.sqlite`-on, ClauseID-alapú szintaktikai scan ugyanazon adatbázison) sem került elő új, valódi igehely; a jelölt Deut 32:3 maga a BDB szerint más szócikk-pontba (3.b "kihirdetni") tartozik, nem a mi 2.c "invokálni" pontunkba
* Licenc-tisztázás lezárva 4 lexikonra: Thayer és BDB (közkincs), LSJ (Perseus, nyíltan újrafelhasznált), SECE (csak közkincs Strong-szöveg + funkcionális számkódok) — mind feldolgozható; MCGED (Mounce, 1993, copyright) — kizárva a rendszeres feldolgozásból
* Thayer, LSJ, SECE teljes feldolgozása (PR #53): 4 új TSV (`Thayer_teljes.tsv` 5426 sor, `LSJ_teljes.tsv` 5522 sor, `SECE_H_teljes.tsv` 8674 sor, `SECE_G_teljes.tsv` 5523 sor) + 1 új, újrafelhasználható script (`eszkozok/elofordulas_szamlalo.py` — a kizárt MCGED "Frequency" funkcióját pótolja, a repó saját TAGNT/TAHOT-kivonataiból, licenc-kockázat nélkül)
* Pilot→study visszaírás lezárva — a scope a vártnál kisebb volt: a 4 igehelyből 3 (Zsolt 105:1/1Krón 16:8, Ézs 12:4, Jer 10:25/Zsolt 79:6) már 2026.09.05 óta a study-ban volt; csak Róm 10:14 (TSK-eredetű, 2026.09.06) és az A/B/C tipológia hiányzott ténylegesen — mindkettő beépítve a `Segitsegul_hivni_az_Urat_tematikus.md`-be
* `Karoli_Strong_kivonat.tsv`: Róm 10:14 (G1941) sor pótolva

2026.09.07 (korábbi szakasz):

* 12 SQLite-lexikon + Motívumlexikon-pilot fájlok repóba emelése (PR #48)
* Alapadatok szakasz (repó, branch-lista, raw/codeload URL-minták) a pilot átadási dokumentumban (PR #49)
* Lexikon-rangsor kiegészítés — projekt-szintű SECE/Thayer/MCGED/LSJ rangsor + héber oldal (TBESH-konszolidáció, SECE görög-megfelelő lista) (PR #50)
* LXX-híd 2 tétele lezárva: Zsolt 116:4 Strong-címke javítva (G4506→G1941), Zsolt 116:17 "hiánya" tévhitnek bizonyult (a görög LXX autentikusan nem fordítja a vers második felét) (PR #51)
* TAHOT teljes korpuszos frissscan — nem hozott új igehelyet; a Zsolt 116:4,13,17 hármas kiderült, hogy már 2026.09.05 óta a hivatalos 17 igehelyes listában szerepel

2026.09.05 és korábbi: l. `Atadasi_dokumentum_2026_09_07_TELJES.md` 1–2. pontja (3/b és 3/c terv, ISTENTISZT-001 v12-compliance és motívum-ID átnevezés).
