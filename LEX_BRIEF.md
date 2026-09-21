# LEX_BRIEF.md — v1

HAMART-001 lexikon-generálás (C1) + ISTENTISZT-001 pilot átemelése (C2/C3 első példány) + N15 felvétele

## 0. Kiindulás — mérve, `9a7bd6a` (2026.09.21)

- `lexikon/`: 7 vegyes fájl (HAMART-001 nincs), mindegyikben 6 „Kézzel írandó" helyőrző.
- `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` (60 943 bájt) és `_OLVASHATO.md` (4 612 bájt): a pilot kézi szövegei.
- `adat/`: HAMART-001 = 52 `elofordulasok`-sor, 0 `kapcsolatok`-sor; a `lexikon_hivatkozasok.tsv` csak G1941, H3548, H7121 kulcsokat tartalmaz.
- A `general.py` TS-je a mai dátum, de meglévő fájlnál a blokk-fejléc nem frissül (N7), így egy kézi szöveget tartalmazó fájl újrafuttatása „változatlan"-t ad. Ez mérve van.

## 1. A feladat

Rövid, gépies lépések egy menetben:
(a) a HAMART-001 lexikon-oldalának generálása az éles `lexikon/` alá (C1);
(b) az ISTENTISZT-001 pilot kézi szövegeinek átemelése a `lexikon/ISTENTISZT-001_TUDOMANYOS.md` kézi szakaszaiba, és az OLVASHATÓ változat áthelyezése. Ez lesz az első teljes lexikon-oldal (C1+C2+C3);
(c) az N15 (LXX-kivonat licenc-tisztázása) felvétele a nyitott listába.

## 2. G-döntések — jóváhagyva (2026.09.21)

- **G1:** a HAMART-001 C1 csak `--id HAMART-001`-gyel fut. A többi 7 fájl nem változhat.
- **G2:** a HAMART-001 üres vagy vékony blokkjait (2. szakasz jelentés nélkül, 5. szakasz 0 sor) ez a menet nem pótolja. A hiányt a zárójelentés rögzíti.
- **G3:** a `generalt_proba/lexikon/` nem kap HAMART-001-et. Az éles fájl a cél.
- **G4:** az átemelés **szó szerinti**. Csak ez a három változtatás megengedett:
  (1) a pilot szakaszszámaira mutató belső hivatkozásokat az új számozáshoz kell igazítani;
  (2) a pilot szakaszcímei alcímmé válhatnak;
  (3) a generált blokkokkal ütköző tényállítás (szám, igehely, reláció) szövege nem módosul, hanem a sor végére `⚠ ELTÉRÉS: …` megjegyzés kerül, és a tétel a jelentésbe megy.
- **G5:** a pilot **adat-jellegű** részei nem jönnek át: szó szerinti BDB/TBESG/Thayer/LSJ/MCGED/SECE idézetek, előfordulás-lista, LXX- és TSK-nyers adat, kapcsolat-tábla. Ezeket a generált réteg fedi (licenc-jelöléssel), átemelésük duplikáció és licenc-kockázat lenne. Csak az értelmező szöveg jön át.
- **G6:** a pilot mappa érintetlen marad (archív forrás). Az `_OLVASHATO.md` **másolatként** kerül a `lexikon/ISTENTISZT-001_OLVASHATO.md`-be. A pilot `_TUDOMANYOS.md` nem törlődik.
- **G7:** a 7. szakasz (ÚJ FELISMERÉS) üres marad. A pilotban nincs így jelölt szöveg, és a menet nem emel át semmit ide saját ítélet alapján.

## 3. Mi NEM a hatókör

- A másik 7 motívum (köztük a HAMART-001) C2/C3 kézi része. Ez a célvonal-döntés (terv N8/N9) után jön.
- `lexikon_hivatkozasok.tsv` vagy `kapcsolatok.tsv` bővítése.
- N7 (fejléc-befagyás), N11, N13.
- Az N15 érdemi munkája (forráscsere, OpenScriptorium-próba). A LEX.5 csak felveszi a tételt.
- Push. Csak külön kérésre.

## 4. Tételek

### LEX.0 — kiindulás *(nem commitol)*
`git status` tiszta (a `LEX_BRIEF.md` commitja után), HEAD a brief-commit, szülője `9a7bd6a` (ha újabb, jelezd). A 0. pont számainak visszamérése.

### LEX.1 — HAMART-001 lexikon-oldal (C1)
1. `python eszkozok/general.py --cel lexikon --id HAMART-001 --ellenoriz` → „új fájl lenne".
2. `python eszkozok/general.py --cel lexikon --id HAMART-001 --ir`.
3. A `git status` csak az új `lexikon/HAMART-001_TUDOMANYOS.md`-t mutathatja.

### LEX.2 — ISTENTISZT-001 kézi szakaszai (C2)
A pilotból a vegyes fájl hat kézi helyére. A pilot sorszámai csak tájékozódásul szolgálnak (v1-es mérés), a címek alapján kell azonosítani:

| Cél (vegyes fájl) | Forrás (pilot) |
|---|---|
| 1/b PaRDeS keretrendszer | „PaRDeS keretrendszer — a motívum egészére alkalmazva" (~74–172) |
| Miért fontos ez a lelet | a G1941 és a G0994 „Miért fontos ez a lelet" bekezdése (~242, ~287) és a „Kiemelt módszertani jelentőség" bekezdés (~309), Strong-számos alcímmel. A G0994-hez írj megjegyzést, hogy generált szócikke jelenleg nincs. |
| Minősítés | a 6. szakasz (TSK/Károli-KH) minősítő sorai (független megerősítés / új találat / nem releváns), a nyers találatok nélkül |
| Alátámasztás | „A kapcsolatok alátámasztása" (~488–522) |
| 6. Módszertani napló | a 8. és 8/b szakasz, a „D — negyedik minta" alszakasszal (~523–625) |
| 8. Nyitott kérdések | a 9. szakasz (~626–vége) |

A „Kézzel írandó" helyőrzők törlődnek. A markeres (`GENERÁLT-KEZDET/VÉGE`) blokkokhoz nem szabad hozzányúlni.

### LEX.3 — OLVASHATÓ változat (C3)
Másold a `motivumlog/lexikon_pilot/ISTENTISZT-001_OLVASHATO.md`-t a `lexikon/ISTENTISZT-001_OLVASHATO.md`-be. A tényállításait vesd össze a generált blokkokkal (G4/3 szabály). A pilot és a `motivumok.tsv` címe eltér („Névbe vetett segítségül hívás" ↔ „Segítségül hívni az Úr nevét"). A címet ne módosítsd, de írd bele a jelentésbe.

### LEX.4 — runbook
A `MUNKAMENET.md` C3-sorában a „ma egyetlen `_OLVASHATO.md` sem létezik" helyett ez álljon: az első (ISTENTISZT-001) átemelve a pilotból, a többi a célvonal-döntéstől függ.

### LEX.5 — N15 felvétele a nyitott listába
A `NYITOTT_FELADATOK.md`-ben az N14 blokk („L. `N14_BRIEF.md`, `N14.0`–`N14.4` commitok.") után, a „## Migrálva a döntési fájl 8. szakaszából" fejléc elé, egy üres sorral elválasztva, szó szerint:

```
- **N15 — Az LXX-kivonat licenc-tisztázása.** *(ÚJ, LEX, 2026.09.21)*
  A `konkordancia/LXX_kivonat_*.tsv` (39 könyv) a studybible.info
  LXX_WH + ABP oldalaiból készült, licencnyilatkozat nélkül (l.
  `LXX_kivonat_README.md` „Licenc-státusz — explicit gap"); az F6
  licenc-térképén ez az egyetlen `tisztazatlan` forrás, és minden
  lexikon-oldal 3. szakaszát (LXX-híd) érinti. Belső használatra nem
  akadály (N11/N3: a lexikon belső), a publikálási döntésnek viszont
  elzáró tétele. Két út: (a) a studybible.info üzemeltetőjének
  megkeresése; (b) forráscsere azonos oszlopformátummal. A (b) jelöltje
  az OpenScriptorium/lxx-morph (egy harmadik projekt leírása szerint
  CC BY 4.0, Rahlfs 1935 alapszöveg, Morpheus-morfológia) — az eredeti
  repó licence még ellenőrizendő; lemmát ad, nem Strong-számot, ezért
  lemma→Strong megfeleltetés kell (jelölt: Open Scriptures Septuagint
  Project, CC BY 4.0). Nem jelölt: Eliran Wong LXX-Rahlfs-1935 és a
  CenterBLC/LXX (CATSS-alapú, CC BY-NC-SA 4.0, felhasználói
  nyilatkozathoz kötött). Alternatíva, ha elérhetővé válik: a STEPBible
  TAGOT (l. a lenti figyelő tételt). Első lépés: az eredeti repó
  licencének ellenőrzése és egy könyv (Genezis) összevetése a mostani
  kivonattal.
```

A `MUNKAMENET.md` „Mi hiányzik az üzemmenetből ma" szakaszában a nyitott tételek felsorolása egészüljön ki az N15-tel.

## 5. Várt számok — jóváhagyva (2026.09.21)

| Mérés | Várt |
|---|---|
| `lexikon/HAMART-001_TUDOMANYOS.md` mérete | ≈ 30 KB (a próbában 29 996 bájt) |
| HAMART-001 1. szakasz | 52 sor, ebből 42 lexikon-jelentéssel |
| HAMART-001 2. szakasz | 14 Strong-fej, 0 jelentés-hivatkozás |
| HAMART-001 3. szakasz (LXX) | 5 görög token, 46 ÓSZ igehely, 6 találat |
| HAMART-001 4. szakasz (TSK/KH) | 30 igehely találattal, 138 találat |
| HAMART-001 5. szakasz | 0 sor |
| HAMART-001 „Kézzel írandó" | 6 |
| HAMART-001 tisztázatlan licenc érintett | igen |
| ISTENTISZT-001 „Kézzel írandó" az LEX.2 után | 0 |
| Módosult a többi 6 `lexikon/*_TUDOMANYOS.md` | 0 |

## 6. Elfogadási kritériumok

- **K1:** az LEX.1 után a `git diff --stat` csak az új HAMART-001 fájlt mutatja. A számok az 5. pont szerintiek.
- **K2:** az LEX.2 után a `general.py --cel lexikon --id ISTENTISZT-001 --ir` futása „változatlan"-t jelez (a kézi szöveg túléli az újragenerálást), és utána a `git diff` üres.
- **K3:** az ISTENTISZT-001 fájl markeres blokkjai bájtra azonosak a kiindulással: `git diff` csak marker-blokkon kívüli sorokat mutat.
- **K4:** a pilot-mappa változatlan (`git diff --stat motivumlog/lexikon_pilot/` üres).
- **K5:** a G5 szerint tiltott adat-rész nem került át. Ellenőrzés: a vegyes fájlban a GENERÁLT-blokkokon kívül nincs szó szerinti szótár-idézet.
- **K6:** az `eszkozok/ellenoriz.py` összesítője nem romlik a kiinduláshoz képest.
- **K7:** a zárójelentés felsorolja az összes `⚠ ELTÉRÉS` tételt, a címeltérést és a HAMART-001 vékony blokkjait.
- **K8:** az N15 blokk szó szerint a megadott helyen áll a `NYITOTT_FELADATOK.md`-ben, és a `MUNKAMENET.md` nyitott felsorolása tartalmazza. A `general.py --cel nyitott --ellenoriz` nem jelez eltérést a generált blokkban.

## 7. Commitok *(push csak külön kérésre)*

1. `LEX_BRIEF.md v1`
2. `LEX.1: HAMART-001 lexikon-oldal (C1, --id HAMART-001)`
3. `LEX.2: ISTENTISZT-001 kézi szakaszai a pilotból (C2)`
4. `LEX.3: ISTENTISZT-001 OLVASHATÓ változat (C3, pilot-másolat)`
5. `LEX.4: MUNKAMENET C3-sor frissítése`
6. `LEX.5: N15 (LXX-kivonat licenc-tisztázása) a nyitott listába`

## 8. Nyitó prompt *(Sonnet)*

> Olvasd el a `LEX_BRIEF.md`-t és a `CLAUDE.md`-t. Hajtsd végre a LEX.0–LEX.5 tételeket egy menetben, a 2. pont G-döntései szerint. Az átemelés szó szerinti, saját fogalmazás nem kerülhet bele. Minden tétel után mérd az 5. pont számait. Ha bármelyik eltér, állj meg és jelezd, ne javítsd. Commitolj a 7. pont szerint, pusholni ne pusholj. A végén adj zárójelentést a K1–K8 szerint.

## Döntésnapló

| Verzió | Dátum | Döntés |
|---|---|---|
| v1 | 2026.09.21 | Két lépés egy menetben (HAMART-001 C1, ISTENTISZT-001 pilot-átemelés), Sonnet, emberi megállás nélkül (gépies munka); G1–G7 és az 5. pont számai jóváhagyva; a C2 tömeges megírása a célvonal-döntés (N8/N9) utánra halasztva |
| v1 (commit előtt kiegészítve) | 2026.09.21 | N15 felvétele LEX.5 tételként ugyanebben a menetben; a forráscsere nem hatókör; jelölt OpenScriptorium/lxx-morph (licenc ellenőrizendő), kizárva a CATSS-alapú források |
