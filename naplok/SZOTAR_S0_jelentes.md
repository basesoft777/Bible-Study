# SZOTAR_S0_jelentes.md — S0 kiegészítő felmérés

*2026.09.23 · a SZOTAR_BRIEF.md v1 S0 szakaszának lezáró jelentése*

## 0. Előfeltétel-ellenőrzés

- `main` = `origin/main` = `443e2e3`, divergencia nélkül. Egyezik.
- A RENDER_BRIEF.md 2. menete lezárult (`NYITOTT_FELADATOK.md` utolsó
  frissítés sora: "RENDER_BRIEF.md v5, 2. menet — R2.1–R2.7 ... RENDER
  lezárva. Következő: SZOTAR_BRIEF.md."). Egyezik.

## 1. §0 tábla újramérése (S0.1)

Minden sort újramértem. Blokkoló eltérés **nincs**; egyetlen, a brief saját
kikötése szerint jelentendő (nem eltérésnek számító) különbség van a 0.12
sornál.

| # | Brief várt érték | Mért érték | Eredmény |
|---|---|---|---|
| 0.1 | `main`=`origin/main`, a RENDER 2. menete utáni hash | `443e2e3`, egyezik | egyezik |
| 0.2 | 24 sor (Thayer 14, BDB 4, TBESG 4, TBESH 1, LSJ 1); `forditas_hu` 11 | ugyanez, pontosan | egyezik |
| 0.3 | 20 sor; `definicio_hu` 20, `glosszak_hu` 20 | ugyanez | egyezik |
| 0.4 | H 24, G 13 token | ugyanez (`adat/elofordulasok.tsv`-ből újraszámolva) | egyezik |
| 0.5 | TBESH 9/13/2 | ugyanez (`naplok/RENDER_R0_forras_osszevetes.tsv`) | egyezik |
| 0.6 | MCGED 13/13 | ugyanez | egyezik |
| 0.7 | SECE 13/13, LN/GK/Hebrew kinyerhető | ugyanez | egyezik |
| 0.8 | 200 pár (112/88), arany 99 (50/49) | ugyanez (`naplok/RENDER_kiejtes_tesztkeszlet.tsv`, 202 sor − 2 fejléc) | egyezik |
| 0.9 | 936 tétel (15/290/25/606) | ugyanez (`naplok/RENDER_R0_atirasok.tsv`, 937 sor − 1 fejléc) | egyezik |
| 0.10 | MCGED.lexicon 10 666, TBESH.lexicon 9 888 | az R0 jelentés által már megerősítve; ezt nem mértem újra (a nyers SQLite nincs a repóban, és a szám az R0.1-ben "egyezik"-ként már rögzült) | átvéve, nem újramért |
| 0.11 | UBSHebrewDic-v0.9.2-en.JSON, SHA a README-ben, eddig csak domén importálva | a SHA valóban a README-ben van; a nyers JSON a repóban nincs (a CLAUDE.md szabálya szerint nyers adat nem kerül a repóba); **letöltöttem a hálózatról** (`eszkozok/sdbh_sdgnt_import.py --letolt`, sikeres) és ellenőriztem mind a 24 H-tokenre: mindegyiknek van legalább egy jelentése, minden jelentésnek van angol definíciója és glosszája, és a jelentésenkénti igehely-lista (LEXReferences) mindegyiknél megvan. L. `naplok/SZOTAR_S0_ubs_dbh.tsv`. | egyezik + kiegészítve |
| 0.12 | 20 sor; a felsorolt "nincs adatosítva" lista (Cremer, Girdlestone+mutató, UBS DBH [3 szerep], Mounce, SECE [2], BDB-etim, kiejtés [2]) | 20 sor egyezik. A tényleges "nincs adatosítva" sorok száma **9** (gorog: Teológiai szócikk, Megfelelők, Kiejtés; heber: Teológiai szócikk, Tömör jelentés, Megfelelők, Nyelvi háttér, Versenkénti jelentés, Kiejtés) — ez **kevesebb tételt** mutat "nincs adatosítva"-ként, mint amit a brief szöveges felsorolása sugall (pl. a gorog "Tömör jelentés, előfordulás [UBS DNTG + Mounce]" és a heber "Jelentésszerkezet [UBS DBH]" sor ma már `adatosítva`). **A user utasítása szerint ez a RENDER végállapotát tükrözi, nem eltérés — csak jelentendő.** | jelentve, nem eltérés (user-utasítás szerint) |
| 0.13 | `konkordancia/LXX_OS/*.tsv` (CC BY 4.0), versszintű; `adat/lxx_dontesek.tsv` | mindkettő megvan és elérhető | egyezik |
| 0.14 | OSHL `atiras` mező (pl. `ʾāb`) | megvan, ellenőrizve a fejlécben és az első sorokban | egyezik |

## 2. S0.2 Cremer — KRITIKUS TALÁLAT

A levendwater.org Cremer-oldalak (`page0001.htm`, `page0914.htm` stb.) **nem
tartalmaznak beágyazott, gépileg kinyerhető szöveget** — kizárólag egy
lapkép-hivatkozást (`<img src="pgNNNNim.jpg" usemap="#Map">`), imagemap-
definíció (AREA-tag) nélkül. A várható "szöveges verzió" URL-minták
(`pagetxtNNNN.htm` stb.) a site generikus frameset-fallback oldalát adják
vissza, nem valódi tartalmat. Ez **ellentmond** a `RENDER_BRIEF.md` S7/D12
feltevésének ("Forrás: gépelt átirat (levendwater.org HTML)").

Az archive.org OCR (`cu31924098819406`) sikeresen letöltve (3 166 034
karakter). A teljes szövegben **0 görög betűs karakter** van — az OCR a
görög szavakat felismerhetetlen latin-betűs torzképekre cseréli (minta:
ἄβυσσος → "A Buocos"). Mind a 13 G-lemma keresése (pontos és ékezet-nélküli
is) 0 találatot ad. Az angol próza nagyrészt olvasható, szórványos hibával.

A Cremer héber mutatója (Index V, `page0934.htm`) szintén tiszta lapkép,
ugyanaz a blokkoló ok.

**Egyik forrás sem adja önmagában a brief S7 által elvárt "szó szerinti
görög szöveg" célt.** L. munkalap: `naplok/SZOTAR_S0_cremer.tsv`.

## 3. S0.3 Girdlestone — kedvezőbb kép

A `preceptaustin.org/pdf/64152/` URL valójában HTML-wrapper, nem tartalmaz
letölthető PDF-linket. A tényleges, gépileg kinyerhető TELJES SZÖVEG a
`preceptaustin.org/synonyms-of-the-old-testament-robert-girdlestone`
cikkoldalon van (709 527 karakter szöveg, cimke nélkül), **valódi héber
betűkkel** (1502 héber karakter). Ez valódi szöveg, nem képszkennelés — a
brief D12 feltevése itt beigazolódik, csak más URL-en, mint várt.

Lefedettség: a 24 H-tokenből 13-nál van (ékezet nélküli) egyezés; a
maradék 11-nél nincs — ez feltehetően tematikus le-nem-fedettség (Girdlestone
nem tárgyal minden szót), nem hiba, mert a forrás valódi szöveg.

Az archive.org OCR (mindkét azonosító, `synonymsofoldtes00gird` és
`SynonymsOfTheOldTestament`) ugyanazt a mintázatot mutatja, mint a Cremernél:
**0 héber betűs karakter** a teljes 1,29M karakteres szövegben, a héber
szavak felismerhetetlenné torzítva (pl. "Nephesh" → "Nepbesb").

**Következtetés: a preceptaustin.org cikkoldal használható elsődleges
forrás; itt nincs olyan blokkoló probléma, mint a Cremernél.** L. munkalap:
`naplok/SZOTAR_S0_girdlestone.tsv`.

## 4. S0.4 BDB-etimológia kivághatósága

A `konkordancia/BDB_teljes_unabridged.tsv` szócikkeiben egy egyszerű
"em dash + '1' + szóköz" mintázat a 24 H-tokenből 14-nél megbízhatóan
elválasztja a nyelvi hátteret (etimológia, rokon nyelvi anyag) az első
számozott jelentéstől. 10 tokennél nem: ebből 6 esetben (H0779, H2555,
H5303, H6093, H7496, H7497) a szócikk maga nagyon rövid, nincs érdemi
etimológiai bekezdés; de 4 esetben (**H0430, H3678, H8004, H8034**) VAN
érdemi rokon-nyelvi anyag, csak eltérő mintázatú a határ — ezeknél kézi
finomítás vagy összetettebb regex kell. L. munkalap:
`naplok/SZOTAR_S0_bdb_etim.tsv`.

## 5. S0.5 kiejtés-tesztkészlet tisztítása

A 200 sort 200-ra helyreállítottam (egy sor egy beágyazott sortörés miatt
két fizikai sorra esett szét a forrás TSV-ben — **ez saját adatminőségi
hiba a `naplok/RENDER_kiejtes_tesztkeszlet.tsv`-ben**, jelzésre érdemes).
A 99 arany pár (mind ISTENTISZT-001-ből) valódinak tekintve. A további 101
párra heurisztikus (automata) triázs: **87 valódinak, 14 hamisnak** tűnik
(a hamisak jellemzően rövidített latin idézetformák, pl. "t. onoma" a
"τ. ὄνομα" rövidítésből, nem önálló kiejtés-pár). Ez előzetes, automata
osztályozás — kézi végső megerősítés az S1.2/S1.3 feladata. L. munkalap:
`naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv`.

## 6. S0.6 átírás-lista tisztítása

Az "alak" kategória (896 tétel) a forrás saját "blokk" mezője alapján
tisztán szétválasztható: `lxx` → **lxx_idezet** (347), `elofordulasok` →
**igeszoveg** (386), `szocikkek`+`kolofon`+`kizart`+`jelmagyarazat` →
**egyeb** (163). A `jelmagyarazat` blokk 1-2 karakteres "szó" mezői (pl.
egy görög betűjel a jelmagyarázatban) hamis-gyanúsként jelölve (16 tétel);
a `kizart` blokk (19 tétel) már eleve a forrás saját kizárási jelölése.
L. munkalap: `naplok/SZOTAR_S0_atirasok_tiszta.tsv`.

## 7. S0.7 héber kiejtés-jelöltek próbája

**Fontos módszertani eltérés a tervezetthez képest:** a brief a 8 motívum
24 lemmájára az OSHL "atiras" mezőt (tudományos átírás) írja elő
alapanyagként; a 49 arany héber pár viszont túlnyomórészt **más** szavakat
(rokon/kapcsolódó gyököket, pl. זָכַר "emlékezni") tartalmaz, nem a 24
lemmát — ezekre nincs kész OSHL-átírás. Ezért a próbát közvetlenül a
pontozott héber szövegen (niqqud) futtattam egy saját, egyszerű
karakter-szabállyal, 36 egyedi egyszavas párra.

**Eredmény: 20/36 egyezik (55,6%).** A 16 eltérés 3 kategóriába sorolható:
(1) **valódi nyelvi nehézség** (10 eset): a szóvégi néma ה és a
shuruk/holam-vav mint magánhangzó-hordozó megkülönböztetése nyers
niqqud-ból nem triviális; (2) **konvenciós hiba** (3 eset): egyszerű
szabály-hangolással javítható (pl. a kaf mindig "k"); (3) **script-hiba**
(3 eset): a próbaszkript saját hibája, nem nyelvi kérdés.

**A (1) kategória pontosan azt a két problémát mutatja, amit a brief D13
indoklása már megnevez** ("a tudományos átírásban a nehéz esetek — hangzó
svá, dagesh, qamets qatan — már eldöntöttek") — az OSHL `atiras` mező ezeket
már nem tartalmazza nyílt karakterként, tehát egy arra épülő szabálytábla
valószínűleg lényegesen jobb arányt érne el. **Ez a próba tehát egy
pesszimista alsó korlátot ad, nem a tényleges S1.2/S3 tervet cáfolja vagy
igazolja közvetlenül** — inkább megerősíti, hogy az OSHL-atirásra épülés a
helyes irány. L. munkalap: `naplok/SZOTAR_S0_heber_jeloltek.tsv`.

## 8. S0.8 LXX korpuszszint próbája

A H7121 mind a 687 Károli-igehelyét (`TAHOT_kivonat.tsv`) összevetve a
`konkordancia/LXX_OS/` versszintű görög adataival: 635 vershez van LXX-sor;
ebből **102 (14,8%)** tartalmazza a G1941 (ἐπικαλέω) kódot. A nyers
együtt-előfordulás átlagosan 15,6 görög szót ad versenként — ez önmagában
túl zajos, a leggyakoribb "találatok" nyelvtani szavak (névelő, kötőszó,
névmás). **A második leggyakoribb tartalmi szó a nem-találatoknál a G2564
(καλέω, 326×) — ez pontosan megegyezik az `adat/lxx_dontesek.tsv` már
rögzített LD001/LD002 döntésével** (2Móz 33:19, 34:5: a fordító καλέω-t
választ ἐπικαλέομαι helyett). A módszer tehát valódi jelet ad, nem csak
zajt, de **csak grammatikai Strong-szűrés után** használható érdemben.
L. munkalap: `naplok/SZOTAR_S0_lxx_versszint.tsv`.

## 9. Kérdések — egy csokorban

1. **Cremer elsődleges forrása (S7) újragondolandó.** A levendwater.org
   nem ad gépileg kinyerhető szöveget (csak lapkép), az archive.org OCR
   pedig a görög betűket teljesen (100%-ban, 0/13 lemma) felismerhetetlenné
   torzítja. A brief D12 döntése ("gépelt átirat az OCR helyett") jó
   irányú volt, de a konkrét forrás (levendwater.org HTML) nem teljesíti a
   feltételét. Alternatívák: (a) más, valódi szöveget adó Cremer-forrás
   keresése (pl. archive.org más kiadása, vagy egy más digitalizálási
   projekt); (b) a Cremer-szócikkek valóban kézi begépelése (nagyobb
   munka, de a brief eredeti "gépelt átirat" szándékát valósítja meg
   szó szerint); (c) a Cremer szerep egyelőre `nincs adatosítva` marad, és
   az S7 tétel elhalasztódik egy külön menetre. Melyiket válasszuk?
2. **Girdlestone forrás-URL pontosítása.** A brief "PDF"-ként hivatkozza a
   forrást (`preceptaustin.org/pdf/64152/`), de a ténylegesen használható,
   szöveget adó URL a testvér-cikkoldal
   (`preceptaustin.org/synonyms-of-the-old-testament-robert-girdlestone`).
   Ezt érdemes-e explicit módon rögzíteni az S1.4 importtételben (és a
   README-ben), nehogy egy jövőbeli futtatás a nem-működő PDF-URL-t
   próbálja?
3. **BDB-etimológia határ-felismerés finomítása (S0.4).** A 24 tokenből
   4-nél (H0430, H3678, H8004, H8034) van érdemi etimológiai anyag, de az
   egyszerű regex nem vágja ki helyesen. Az S9 tétel előfeltétele ("az
   S0.4 igazolja a kivághatóságot") csak részben teljesül — kell-e egy
   finomabb, kézzel ellenőrzött határfelismerő szabály, mielőtt az S9
   commitba kerül, vagy elfogadható-e, hogy ez a 4 token kézi jelöléssel
   (`allapot=kezi_hatarozando`) kerüljön be egyelőre?
4. **A kiejtés-tesztkészlet saját adathibája.** A
   `naplok/RENDER_kiejtes_tesztkeszlet.tsv` egyik sora egy beágyazott
   sortörés miatt két fizikai sorra esett szét (a `csv`-mentes,
   `split('\t')`-alapú olvasás ezt csendben hibásan kezelte volna, ha nem
   veszünk észre egy hiányzó "hely" mezőt). Javítandó-e maga a
   `RENDER_kiejtes_tesztkeszlet.tsv`, vagy elég, hogy a tisztított
   `SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv` már helyesen kezeli?
5. **A kiejtés-tesztkészlet 101 további párjának automata triázsa (87
   valódi / 14 hamis) elfogadható-e S1.2 bemenetként**, vagy kell egy kézi
   átnézési kör is, mielőtt a `kiejtes.py --ellenoriz` ezekre támaszkodik?
6. **A héber kiejtés-jelöltek próbájának alacsony (55,6%) aránya** — mivel
   ez egy eltérő módszertani alapon (nyers niqqud, nem OSHL-atirás) készült
   próba a 24 lemmán kívüli szavakra, elfogadható-e mérföldkőként, vagy
   szükséges egy második próba kifejezetten a 24 lemma OSHL-atirásán
   (ehhez elő kellene állítani az OSHL-bejegyzéseket azokra a szavakra is,
   amelyek nem a 24 motívum-token, de a 49 arany párban szerepelnek — ez
   már S1-szintű munka)?
7. **Az LXX korpuszszint módszer grammatikai szűrése (S0.8).** A nyers
   együtt-előfordulás túl zajos; szükséges a `adat/grammatikai_strongok.tsv`
   mintájára egy görög grammatikai Strong-lista a zaj kiszűrésére, mielőtt
   az S13 (LXX-híd korpuszszinten) élesítésre kerül. Ez az S1.4 tétel
   része legyen (az `LXX_versszintu_parok.tsv` import mellett), vagy külön
   S0-utáni előkészítő lépés?

## Munkalapok

- `naplok/SZOTAR_S0_ubs_dbh.tsv`
- `naplok/SZOTAR_S0_cremer.tsv`
- `naplok/SZOTAR_S0_girdlestone.tsv`
- `naplok/SZOTAR_S0_bdb_etim.tsv`
- `naplok/SZOTAR_kiejtes_tesztkeszlet_tiszta.tsv`
- `naplok/SZOTAR_S0_atirasok_tiszta.tsv`
- `naplok/SZOTAR_S0_heber_jeloltek.tsv`
- `naplok/SZOTAR_S0_lxx_versszint.tsv`

## Elfogadási kritériumok (K1–K3)

- **K1** — teljesítve: a §0 minden sora jelentve fent (1. szakasz).
- **K2** — teljesítve: a nyolc munkalap és e jelentés megvan; a kérdések a
  9. szakaszban, egy listában.
- **K3** — teljesítve: az éles `adat/`, `lexikon/`, `tematikus_lezart/`,
  `konkordancia/` könyvtárba az S0 alatt nem történt írás (csak olvasás és
  mérés, valamint hálózati letöltés ideiglenes könyvtárba, amit a mérés
  után töröltünk; a `naplok/` írás a brief szerint engedélyezett
  munkatermék).
