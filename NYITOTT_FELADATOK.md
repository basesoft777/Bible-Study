Nyitott feladatok
Ez a fájl a projekt aktuális, karbantartott feladatlistája. Minden Claude-chat vagy Code-munkamenet végén frissítendő: a lezárt tételek áthelyezendők a "Lezárva" szakaszba (dátummal), az újonnan felmerülő tételek felveendők a megfelelő szakaszba.
Utolsó frissítés: 2026.09.07
Nagy, tartalmi döntést igénylő tételek

1. Pilot→study visszaírás — a 4 valódi extra igehely (Zsolt 105:1/1Krón 16:8, Ézs 12:4, Jer 10:25/Zsolt 79:6, Róm 10:14) + A/B/C tipológia beépítése a tényleges `Segitsegul_hivni_az_Urat_ tematikus.md`-be, vagy tudatos elhalasztása. Részletek: `motivumlog/lexikon_pilot/Atadasi_dokumentum_Motivumlexikon_ pilot_2026-09-07.md`.
2. 12 SQLite-lexikon tényleges feldolgozása (SECE, Thayer, MCGED, LSJ → TSV) — a rangsor már dokumentálva (`konkordancia/Javasolt_gorog_oldal_erositese.md`, 6. lehetőség), de a munka maga el sem indult. Előfeltétel: a 12 SQLite-fájl licenc-státuszának tisztázása (`konkordancia/lexikonok_nyers/README.md`).
3. `biblemate-agentic-workspace` (eliranwong) mélyebb integrációja — a `morphology.sqlite` (teljes, vers-soronkénti héber/görög morfológiai adatbázis, Google Drive-on, file ID `11QfpwEd5fjdDglPiqzygLNN99AVz2mw5`), a `cross-reference.sqlite`, és a `search_retriever.py` közül mi éri meg ténylegesen beépíteni a saját workflow-ba. Folyamatban: קרא-lexéma teljes scan a morphology.sqlite-on, a BDB "16t" kérdés végleges lezárásához.

Kisebb, korábbról nyitva maradt tételek

* `Karoli_Strong_kivonat.tsv` bővítése az új igehelyekkel
* A/B/C tipológia + 1Kir 18:24 kontraszt felvétele a `Bibliai_Motivumlexikon_tervezesi_naplo.md`-be
* 3 ÚSZ study első audit (Róm 8:10, Zsid 4:12, 1Thessz 5:23)
* Gen 3:10/3:11 H5903 join-sorok
* בָּרַךְ (H1288) korrekciós Code-prompt újbóli jóváhagyása
* 7 további tematikus study v12-compliance (nagy, több körös munka — mind a "Segítségül hívni"-n kívüli lezárt tematikus study ugyanabban a v12-non-compliance állapotban van, mint amiben a "Segítségül hívni" volt 2026.09.05 előtt)
* Tehóm (27) és Seól (63) nagy, ellenőrizetlen jelölt-listái — valószínűleg nem hiányosság a studyk szándékos szűkítése miatt, de nincs explicit döntés

Lezárva
2026.09.07:

* 12 SQLite-lexikon + Motívumlexikon-pilot fájlok repóba emelése (PR #48)
* Alapadatok szakasz (repó, branch-lista, raw/codeload URL-minták) a pilot átadási dokumentumban (PR #49)
* Lexikon-rangsor kiegészítés — projekt-szintű SECE/Thayer/MCGED/LSJ rangsor + héber oldal (TBESH-konszolidáció, SECE görög-megfelelő lista) (PR #50)
* LXX-híd 2 tétele lezárva: Zsolt 116:4 Strong-címke javítva (G4506→G1941), Zsolt 116:17 "hiánya" tévhitnek bizonyult (a görög LXX autentikusan nem fordítja a vers második felét) (PR #51)
* TAHOT teljes korpuszos frissscan — nem hozott új igehelyet; a Zsolt 116:4,13,17 hármas kiderült, hogy már 2026.09.05 óta a hivatalos 17 igehelyes listában szerepel

2026.09.05 és korábbi: l. `Atadasi_dokumentum_2026_09_07_TELJES.md` 1–2. pontja (3/b és 3/c terv, ISTENTISZT-001 v12-compliance és motívum-ID átnevezés).