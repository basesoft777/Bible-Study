Nyitott feladatok
Ez a fájl a projekt aktuális, karbantartott feladatlistája. Átadási dokumentum kérésekor frissítendő: a lezárt tételek áthelyezendők a "Lezárva" szakaszba (dátummal), az újonnan felmerülő tételek felveendők a megfelelő szakaszba.
Utolsó frissítés: 2026.09.07
Nagy, tartalmi döntést igénylő tételek

1. `biblemate-agentic-workspace` (eliranwong) mélyebb, rendszeres integrációja — a `morphology.sqlite` (teljes, vers-soronkénti héber/görög morfológiai adatbázis, Google Drive-on, file ID `11QfpwEd5fjdDglPiqzygLNN99AVz2mw5`), a `cross-reference.sqlite`, és a `search_retriever.py` közül mi érné meg ténylegesen beépíteni a saját workflow-ba. A licenc-státusza NINCS tisztázva (csak egyszeri, ideiglenes felhasználás történt eddig, l. Lezárva). Nincs döntés.

Kisebb, korábbról nyitva maradt tételek

* `Karoli_Strong_kivonat.tsv` bővítése az új igehelyekkel
* A/B/C tipológia + 1Kir 18:24 kontraszt felvétele a `Bibliai_Motivumlexikon_tervezesi_naplo.md`-be
* 3 ÚSZ study első audit (Róm 8:10, Zsid 4:12, 1Thessz 5:23)
* Gen 3:10/3:11 H5903 join-sorok
* בָּרַךְ (H1288) korrekciós Code-prompt újbóli jóváhagyása
* 7 további tematikus study v12-compliance (nagy, több körös munka)
* Tehóm (27) és Seól (63) jelölt-listái — valószínűleg nem hiányosság, nincs explicit döntés

Lezárva
2026.09.07 (folytatólagos szakasz):

* BDB "16t" kérdés véglegesen lezárva — három egymástól független módszerrel (TAHOT pozíció-alapú frázis-scan, laza vers-szintű co-occurrence a `morphology.sqlite`-on, ClauseID- alapú szintaktikai scan ugyanazon adatbázison) sem került elő új, valódi igehely; a jelölt Deut 32:3 maga a BDB szerint más szócikk-pontba (3.b "kihirdetni") tartozik, nem a mi 2.c "invokálni" pontunkba
* Licenc-tisztázás lezárva 4 lexikonra: Thayer és BDB (közkincs), LSJ (Perseus, nyíltan újrafelhasznált), SECE (csak közkincs Strong- szöveg + funkcionális számkódok) — mind feldolgozható; MCGED (Mounce, 1993, copyright) — kizárva a rendszeres feldolgozásból
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