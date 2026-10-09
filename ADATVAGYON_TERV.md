# PaRDeS adatvagyon-architektúra: Károli–Strong, kereső, MCP (tervjegyzet)

## Kiindulási állapot és mi változott a repóban (2026-10-04)

**Kiindulási állapot:** FELADATOK.md v1.3 (a generált blokkok 2026-10-09-i állapota), `main` `78844919` (a #264 merge-e), 2026-10-09 — a #52 TERV\_SZINKRON 3. futásának viszonyítási pontja (`naplok/F52_TERV_SZINKRON_naplo.md`); a 2. futás kiindulása a `7dd0183` volt (a #218 merge-e `a25c7a0` után, 2026-10-06); az 1. futás kiindulása a `8e8f771` (#171) volt (PR #172, merge `de9c464`, 2026-10-04), előzménye a `117bafc` (#26 EGYFORRAS_NAPLO; #32 KONTEXTUS kész; DT-F33e–j; #46 kész). Az alábbi szakaszok a 2026-10-02/03-i repóállapotra íródtak; ahol a mai állapot felülírja őket, azt **itt** rögzítem, és a szakasz szövegében a hamissá vált állítást a #52 cseréli (v14, v15). Ami nincs ebben a listában, az változatlanul érvényes.

| mi változott a repóban | mit ír felül a tervben |
| --- | --- |
| **DT-F33f:** a STEPBible „Please do not redistribute it yourself" mondata kérés, nem licencfeltétel; a hatályos forrás az upstream README, **CC BY 4.0**. **DT-F33e:** a Károli 1908 (`Karoli_1908`, `Karoli_KH`) közkincs, kiadói nyilatkozat nélkül. **DT-F33g:** BDB, Thayer, Nave közkincs. **DT-F33h:** a SECE public domain, nem GPL (a playbook GPL-sora nem igazolódott). **DT-F33i:** a SECE_G LN/GK mezői nem kerülnek a renderbe. SEMA: az LSJ tisztázott, CC BY-SA 4.0. | A 0. szakasz 4. pontja, a 2. szakasz és a 17.1 első sora **elavult**: a böngészőben futó adatbázis (1. út) nem esik ki a STEPBible miatt; a `pardes.db` terjeszthetőségét a benne lévő források módja dönti el (DT-F33j). A hosting-döntés nyitott, a backend-út már nem kényszer. Marad viszont a **DT-F33j:** két kimeneti változat, **kereskedelmi / nem kereskedelmi** (N-F33b) — a 17.1 „licenc-szűrője" nem tisztazott/tisztazatlan, hanem a `licencek.tsv` `kereskedelmi` oszlopa szerint szűr. Az ok négy nem kereskedelmi vagy tisztázatlan forrás: a három ETCBC-eredetű héber modul (CC BY-NC 4.0), a MCGED (Mounce, csak nem kereskedelmi), az LSJ-alapú LXX.lexicon (CC BY-SA, share-alike a kiadásra is) és a SECE_G LN/GK mezői (jogosultság nem igazolt). Nem kereskedelmi módban minden forrás megy megjelöléssel — ez az első olvasói kiadás; kereskedelmi módban csak a `kereskedelmi=igen` források, tisztázott pótlással (héber morfológia a TAHOT/TAGNT-ból, LN az UBS SDGNT-ből). A kutatói oldalt (MCP, `lekerdez.py`) nem szűri. Súlya: a licenc a kutatást nem korlátozza; egy oszlop a `licencek.tsv`-ben és egy módparaméter a renderben, amit a publikáláskor kapcsolsz (nyilvános nézet: forrásmegjelölés és share-alike; bevétel: a négy forrás kiesik, pótlás belép; adatkészlet-kiadás: a saját rétegek szabadok). Az architektúrát nem a licenc dönti el — a 0. szakasz 4. pontja ennél erősebben fogalmaz, ennyire értendő. A #44 Károli-licencsora ezzel lezárt. |
| **D34–D41 bent a FELADATOK-ban** (#26 merge-elve): motívumonként egy kézi forrás, minden nézet generált; a törzscikk a #11-ben megszűnik; D36 három mélységi szint; D40 olvasói felület statikus HTML, később PWA. **DT-F26a névhasználat:** a „tematikus tanulmány" neve mostantól **motívumcikk** (a `motivumok/[ID].md`-ből generált nézet); a „tanulmány" az igeszakasz-tanulmány (kézi forrás). | A 16. és 18.2 szakasz állításai igazolódtak. A docban a „tematikus tanulmány" mindenütt **motívumcikk**-ként olvasandó; a 4., 5., 20. szakasz „Tanulmány" doboza = motívumcikk + igeszakasz-tanulmány. |
| **#32 KONTEXTUS kész**, négy szabály (MUNKAMENET, CLAUDE.md): az értelmező réteg egy kézben, egy modellel (**DT-F32b: Opus**); a `motivumok/[ID].md` próza-elsőbbségű — a SEMA a kinyerést írja le, nem a dokumentum szerkezetét; aki motívumba ír, az egészet olvassa; a #23 M1 a #12a próza-próba után. A brief fejléce `munka: adat / ertelmezo / folyamat`. | A 9., 13., 14. szakasz eszközei és a 21. workflow lépcsői `munka: adat` vagy `folyamat` feladatok — ezekre a Sonnet és a csomagmód áll. A 22. szakasz „a SEMA a kinyerést írja le" elve ezzel egyezik: a vers-lap/szó-lap/motívum-lap render a markerekből nyer, nem mezőkből. Író MCP-eszköz motívumfájlra sosem (K1). |
| **Sorszámok:** a repóban már van #48 KJV_REGI_KIVEZETES, #49 FOLYTATAS (merge-elve), #50 CI_JAVITO_KOR, **#51 KONZISZTENCIA** (döntések átvezetésének gépi ellenőrzése). | A MUNKATERV javasolt #47–#55 sorszámai ütköztek ezekkel; a felhasználó döntése (DT-F52a, 2026-10-04) szerint a MUNKATERV és a VIBE\_GUIDE a FELADATOK számaihoz igazodik: a még be nem fogadott tervezett feladatok a kódjukkal szerepelnek (`SQLITE_EPIT`, `OLVASOI_KONKORDANCIA` …), számot a `/befogad` ad; a `#nn` alak mindhárom tervdokumentumban FELADATOK-szám. A #51 pontosan a tervdokumentumok elavulását őrzi — a szinkron ritmusát ő adja, nem a chat. |
| **Státuszok (2026-10-09):** #22 ⛔ megállt (kész: 1–5Móz, Józs, Zsolt, Ézs, Jer, 1–2Krón, Ezsd, Ez; hátra a Jób — előfeltételei teljesültek, #83, #84 — és a Péld, DT57); #43 ✅ (PR #167; DT-F43: 86 sor: 24 egyezik, 3 eltér, 46 nincs adat; a bridge nem független második forrás, csak tájékoztató réteg); #42 ✅ (PR #176), #44 ✅ (PR #205), #30 ✅ (PR #206), #51 ✅ (PR #192), #53 ✅, #57 ✅ (PR #209), #58 ✅ (PR #208), #56 ✅ (PR #218), #46 ✅, #37 ✅ (PR #240), #40 ✅ (PR #242), #64 ✅ (PR #247), #66 ✅ (PR #227), #68 ✅ (PR #244), #77 ✅ (PR #249), #78 ✅ (PR #254, #256), #82 ✅ (PR #250), #83 ✅ (PR #260), #84 ✅ (PR #262); #23 M0 és M1 kész (DT84 🟡); #38 ▶ (6 adag kész; a 7. adag (86%) indulhat, a 8. adagtól a Károli-lefedettségi küszöb dönt, DT56; a #56 adatblokkjával, DT-F38i 🟢); #9 a #23-tól is függ (a #78 kész); #11 a #9 és #23-tól, első lépcső ISTENTISZT-001 (a #78 vázával rekonstruálva). N29 lezárva, az ASV nem jön (D7). | A 15., 16. szakasz és a 21. workflow 1. lépcsője ennek megfelelően értendő; a 26-os pont (LXX-híd ★) a DT-F43 (a) szerint tájékoztató réteg, a bizonyosság a DT23 szerint. |
| **2026-10-04 óta eldöntve (2. futás):** **DT-M1** 🟢 — az olvasói konkordancia motívum nélkül a #25 előtt: a #25 kettéválik (#25a = OLVASOI\_KONKORDANCIA, függ SQLITE\_EPIT; #25b motívumos nézet, függ #11, #12, #23; a kettéválasztás külön `/befogad`); **DT-M2** 🟢 új `AZONOSITAS_MODJA` érték: `szó-szintű-gépi`; **DT-M3** 🟢 az `auditok.lepes` a kutatási lépés kódja, lépésen kívül `adhoc`, a csatorna a proveniencia-sorban (#61); **DT-M7** 🟢 az MCP-szerver feltételes (előbb a #61); **DT-M8** 🟢 a TERV\_BEFOGAD külön brief nélkül záródik; **DT-F42d, DT-F42g** — a `KJV_Strongs_teljes` Strong-címkéi `tisztazatlan`, a licenc-címke egyetlen forrása a `licencek.tsv` `cimke` oszlopa; **DT-F42f** — az LXX\_kivonat kivezetve; **DT31–DT34** — a `karoli_bible_hu` elvetve (DT31), az openbible 4 sora `hianyzik` + JELÖLT (DT33), az import külön feladat (DT34). Számot kapott tervezett feladatok: #56 (BDB\_ADATBLOKK), #62 (STRONG\_NORMALIZAL), #63 (JELOLTEK\_RETRO), #65 (KAROLI\_ELLENORZES); új feladatok: #54, #55, #59, #60, #61, #64, #66. | A 0., 9., 13., 15., 16., 17.1, 19., 21., 22.2 és 22.4 szakasz ennek megfelelően értendő; ahol a törzs ezt felülírja, a v15 sor jelöli. |
| **2026-10-08 (TERV-INTEGRÁCIÓ, DT74–g):** a terv → feladat irány átvezetve: SQLITE\_EPIT = #79, OLVASOI\_KONKORDANCIA = #76 (#25a, `fazis: 1`, a #79 után), szerepmátrix-váz = #78 (a lexikonoldal szótári szakasza a 18.5 szerint; az ISTENTISZT-001 aranyminta rekonstrukciója), BDB-adatblokk-pótlás a teljes #22 után = #80 (újrafordítás nélkül; a DT54/DT56 pontosítása), Károli-ujjlenyomat (1.4) = #81; SZPA-audit feltételes (a profilfájl repóba kerülése után); DT-M4, M5, M6 🟢; a #38 6. adagja kész (DT52), a 7. adag (86%) indulhat, a 8. adagtól a DT56 küszöbe dönt; a #22-ben a Zsoltárok kész (PR #239), a további sorrend DT54/DT57; a BDB-gyökcsoport-felmérés lefutott (N53). | Ahol a törzs ennek ellentmond (0., 13., 15., 16., 19., 21.), ez a sor az irányadó; a 19. teendőlistája jelölve. |
| **2026-10-09 (#52 3. futás):** #78 ✅ (szerepmátrix-váz; DT80–DT83: `ÜRES-BLOKK` / `ÜRES-NYELV` jelölő, „adatosítva, nincs bekötve” állapot, 13–14. szerep a `szotar_szerepek.tsv`-ben `javaslat`-tal), #77 ✅ (DT73: a #22 hátralévő könyvei API-n, Batch, `high`), #82 ✅ (DT79: terv → feladat gépi őr; az ADATVAGYON 21. a jelölt táblák közül kimarad), #83 ✅ (DT85) és #84 ✅ (DT86: a Jób 41 TAHOT-sorai pótolva; CLAUDE.md TAHOT-mondat; N55 és N-F34b lezárva), #23 M1 kész (DT84 🟡); a #22-ben a Zsoltárok, Ézsaiás, Jeremiás, 1–2Krónika, Ezsdrás és Ezékiel kész (DT57, DT70–DT72); az ATALAKITASI\_TERV 10. N1, N2, N5 lezárva (DT87–DT89). | A 0. (3. pont), 16. (ábra, állapotfrissítés), 17.2 (Adat-tár sor), 18.1 (ATALAKITASI 4.7 sor), 18.4 (N-F34b sor), 18.5, 19., 21. (5. lépcső), 22.5 (TAHOT-sor) a v17-ben cserélve; ahol a törzs ennek ellentmond, ez a sor az irányadó. |
| **MUNKAMENET:** a ⛔-nál a döntést a `DONTES_KERDES_SABLON.md` szerint kell előkészíteni, erősebb modell (Opus) külön sessionben vagy a chatben. | A 14. és 21. szakasz ⛔-jai ezt a sablont követik. |

**Javaslat (licenc és saját réteg, 2026-10-04)** — a szintézis szabad, a mezők öröklik a forrás licencét, a határ a proveniencia:

1. **A proveniencia a licenc hordozója, mezőszinten.** A renderben minden blokk a `licencek.tsv` `dataset` kulcsával jön; a mód (nem kereskedelmi / kereskedelmi) blokkonként dönt (N-F33b). Az OLVASOI\_KONKORDANCIA elfogadási pontja: minden blokk alatt forrás és licenc, nincs blokk dataset-kulcs nélkül.
2. **Idézési szabály a saját prózára — DT-tétel** (study-rules / CLAUDE.md): a motívumcikk és a napló szócikket csak közkincs vagy CC BY forrásból idéz szó szerint (BDB, Thayer, TAHOT-glossza, Károli 1908); NC- és SA-forrásra (MCGED, LSJ, UBS, BHSA) hivatkozik, de nem másol. Így a saját réteg tiszta marad vegyes mezők mellett is.
3. **A saját réteg licence — DT-tétel.** A `licencek.tsv` `projekt_adat` sora kimondja, milyen licenccel adható ki a Károli–Strong párosítás, a fordítások és a napló-döntések; javaslat: CC BY 4.0 az adatra, a prózára külön. Enélkül a 0.2 „saját szellemi tulajdon" oszlopa nem fordítható kiadássá.
4. **Az első kiadás nem kereskedelmi, teljes, jelölt.** Az OLVASOI\_KONKORDANCIA nem épít kereskedelmi módot, csak a mezőszintű jelölést; a kereskedelmi mód később átbillentett kapcsoló, jogásszal.

Nem jogi vélemény.

A sorrend a továbbiakban: ez a doc a repóba költözött `ADATVAGYON_TERV.md`-ként (`ab73f7b`, 2026-10-04), és onnantól a repó a hatályos példány; a chat-doc csak átnézésre.

## 0. Összegzés — a terv állása 2026-10-03

A tervjegyzet a repó meglévő terveinek kibontása, nem új rendszer. Ami a 18 szakasz átnézéséből a repó fájljaival (FELADATOK, DONTESEK, CLAUDE, MUNKAMENET, NYITOTT\_FELADATOK, ATALAKITASI\_TERV, SEMA, F23/F25) összevetve megáll:

1. **Egy adat, három nézet.** A CLAUDE.md fő szabálya („a kereszthivatkozás adat, a tanulmány és a lexikon nézet") a projekt értelmezésében egy lánc, nem három egyenrangú nézet: a tanulmány detektálja a motívumot → a lexikon hordozza a teljes apparátust (adat, napló, döntések, üzemeltetői üzenetek) → minden olvasói nézet a lexikon adatára készül. A mélységi szintek (D36) ezt a láncot képezik le: belső = üzemeltetői réteg, apparátus = napló és döntés, olvasói = a publikus nézet. Az olvasói felület így nem harmadik, hanem a lánc végén álló nézet ugyanarra az `adat/`-ra. A vers-lap, szó-lap és motívum-lap az F23 (D34) *olvasói nézetei*, `olvasoi` / `apparatus` / `belso` mélységgel; a `belso` (nyitott jelöltek, napló nyers indoklása) a publikus buildből kimarad — a lelet-lap munkalistája csak Code-ban él.
2. **A kutatói lekérdező létezik: `eszkozok/lekerdez.py`.** Az MCP (feltételes, DT-M7) az ATALAKITASI\_TERV 11.7 szerint ennek vékony burka, legfeljebb 8 eszközzel, proveniencia-sorral és kötelező `auditok.tsv`-sorral minden hívásnál. A `sqlite_epit.py` a kutatói oldalon nem előfeltétel; az olvasói felületnek és a nagy fájloknak kell.
3. **A Károli–Strong (#22) a terv alapja, és már kész: 1–5Mózes, Józsué, a Zsoltárok, Ézsaiás, Jeremiás, 1–2Krónika, Ezsdrás és Ezékiel (⛔ a következő könyv döntéséig: a Jób és a Péld, DT57).** Az 1.1–1.4 haszon (ellenőrzés, variancia-térkép, magyar frázis, ujjlenyomat) ebből indul; az ATALAKITASI\_TERV 4.7 („teljes strongozás nem cél") elavult.
4. **A publikálás licenc-kérdés, de nem akadály (DT-F33e–j).** A STEPBible-származékok CC BY 4.0 alatt, attribúcióval terjeszthetők (DT-F33f: a „Please do not redistribute" kérés, nem licencfeltétel) → a böngészőben futó adatbázis nem esik ki, a hosting-út (böngészős, cPanel vagy serverless) nyitott, nem kényszer; a nyers fájlok a repóban maradnak (DT-F33a). A Károli 1908, a BDB, a Thayer, a Nave és a SECE közkincs (DT-F33e, g, h), ezért a Károli kiadói nyilatkozata nem előfeltétel. A kiadás két módban megy (DT-F33j, N-F33b): nem kereskedelmi (minden forrás, jelöléssel) és kereskedelmi (csak a `licencek.tsv` `kereskedelmi=igen` forrásai; kiesik a három ETCBC-eredetű héber modul és az MCGED (`kereskedelmi=nem`), az LSJ-alapú LXX.lexicon (`tisztazatlan`) és a SECE_G LN/GK mezője (DT-F33i, j; N-F33b)); a nyilvános nézet a `kereskedelmi` oszlop szerint szűr. A Bible-Discovery Károli kizárva. Jogász a kereskedelmi döntéskor (ATALAKITASI\_TERV 12).
5. **A séma fő kockázata a versszámozás.** A KK `igehely_kjv` nem megbízható, a TAHOT számozása vegyes (N17, N46, N-F41a/d): a vers-lap kulcsa Károli-számozás, minden más forrás a KK-n át kötve, `szamozas` jelzővel, interpoláció nélkül. A Strong-normalizálás az N37 szerinti egységes függvény.
6. **A BDB-fordításnál (#38; a 6. adag a #56 adatblokkjával, DT-F38i 🟢) nem MCP, hanem build-lépés.** A 12.1 adatlekérés előre számolt blokkként az adagfájlban; az adagok közötti következetesség a már létező `terminologia.tsv`-vel (SEMA 2.15). Szócikkenként drágább, helyes szócikkenként olcsóbb.
7. **Függések.** A lexikonoldal-illesztés a #9/#10, a motívum-séma a #23, a renderelés a #11, az olvasói felület a #25 dolga; ez a tervjegyzet a #25 és #23 bemenete. Most, függés nélkül mehet: az adatréteg importja (Strong, Károli–Strong, TSK, lexikon), az 1.1 ellenőrzés (#65); az MCP olvasó eszközei feltételesek (DT-M7: előbb a #61 LEKERDEZ\_NAPLO); a három kézi 0. lépés (#43, #44) 2026-10-04-re kész.
8. **Ez a doc csak a repóban hat.** Claude Code nem látja a claude.ai-t (playbook): Markdown-exportja a repó gyökerébe (kész: `ab73f7b`), és a #25/#23 brief `olvas:` listájába (kész, DT-M8 (a); a #11 csonk `olvas:` sorában is bent van, DT-M8 (d)).

A részletek és a forrás-hivatkozások a 16–18. szakaszban; a döntésnapló a 19.-ben.

**0.1 A keret: három cél, egy adat**

Motívum-kereszthivatkozási rendszer (a módszer; ez termeli az egyetlen máshol nem létező adatot: a döntést indoklással) · olvasói nézet (próba és termék egyszerre: 11.5 és D46) · a közben felépített adatvagyon hasznosítása (a melléktermék, ami önállóan is áll). A 26 pont ebben rendeződik: 7–12, 21–26 csak a motívumrétegből válaszolható; 17 és a lap-típusok az olvasói nézet; 1–6, 13–16, 18–20 motívum nélkül is áll.

**0.2 Az adatvagyon az 1. fázis végén — úgy gondolva, mintha kész volna**

Az 1. fázis (adatréteg) függő tételei: #22 Károli–Strong (teljes Biblia), #38 BDB magyarul (8 090 szócikk), #7 Thayer magyarul, #43 LXX-híd ellenőrzés, #44 nyílt Károli 1908 + openbible.info licenc, #46 BDB könyvfeloldás, #23 motívum-séma. Ha ezek készen állnak, az adat így néz ki:

| réteg | az 1. fázis végén | saját szellemi tulajdon? | terjeszthető? |
| --- | --- | --- | --- |
| Károli-szöveg | 1908-as revízió, nyílt forrásból, licenc idézve (#44) | nem (közkincs) | igen |
| Károli–Strong | a Károli minden szava eredeti szóval és Strong-számmal, bizonyossági jelöléssel, az egész Biblián (#22) | **igen** — a párosítás a projekt munkája | igen, ha a párosítás nem STEPBible-adat másolata; a bemenet (TAHOT) is CC BY 4.0 alatt, attribúcióval terjeszthető (DT-F33f), a kimenet (saját link-tábla) a projekté — jogász erősítse meg |
| héber szótár | a teljes BDB magyarul, javított igehelyekkel, Károli-szóalak-oszloppal (#38, #46, 12.1) | **igen** — a fordítás; a BDB maga közkincs | igen |
| görög szótár | a teljes Thayer magyarul (#7); a lexikoni Strongok Opus-emeléssel | **igen** | igen (a Thayer közkincs) |
| kiejtés | héber és görög kiejtés-jelöltek szabálytáblával (S1) | **igen** | igen |
| versszámozás | KK: Károli ↔ MT ↔ LXX ↔ KJV, kézzel ellenőrizve, eltolódások jelölve | **igen** | igen (TVTMS-eredetű rész: STEPBible) |
| LXX-híd | héber → görög Strong a LXX-en át, versszinten (LXX\_OS, Macula) és lexémaszinten (lxx\_bridge, #43), döntésekkel | részben (a döntés igen) | a Macula CC BY, a lxx\_bridge CC BY |
| kereszthivatkozások | TSK, Nave, openbible.info (rangsorral), Károli-KH | nem | igen (PD / CC BY) |
| motívum-réteg | motívumok, előfordulások, kapcsolatok, jelöltek, napló-döntések, PaRDeS-szint (#23 séma) | **igen** — ez csak itt létezik | igen |

Ami ebből következik:

1. **Az adatvagyon a projekt saját termékének nagyobb része, nem a tanulmány.** A fenti kilencből hat saját szellemi tulajdon, és egyik sem függ a motívumoktól. Együtt: **az első nyílt, magyar Strong-konkordáns bibliatanulmányozó adatkészlet** — Károli-szöveg szavanként Stronggal, teljes magyar BDB és Thayer a Károli tényleges szóhasználatával, kiejtéssel, versszámozás-kulccsal. Magyarul ma egyetlen zárt program (Biblia-Felfedező / Bible-Discovery) ad Strong-párosított Károlit: az ÚSZ-e kész és lektorált, az ÓSZ-e könyvenként készül; a szó-szintű párosítás fizetős modul, a Strong\_HU szótár zárt. Nyílt licencű magyar Strong-párosítás vagy magyar BDB/Thayer nem került elő (2026-10-03, nem kimerítő keresés). De a lényeg nem ez: a három réteg — konkordancia, értelmezési réteg (motívum, PaRDeS-szint, LXX-híd döntésekkel), és a kettő közti indokolt kapcsolat (★ lelet, napló) — \*\*együtt sehol nem létezik, zártan sem\*\*. A különbség fajtabeli, nem fokozati.
2. **A terjesztési kérdés kettéválik.** A bemeneti STEPBible-fájlok CC BY 4.0 alatt, attribúcióval terjeszthetők (DT-F33f: a „do not redistribute" kérés, nem licencfeltétel), a nyers fájlok a repóban maradnak (DT-F33a); a projekt *saját* kimenete (párosítás, fordítás, döntés) a sajátja, licencét külön DT-tétel mondja ki (fent, javaslat 3.). A szétválasztás így nem STEPBible kontra saját, hanem kereskedelmi kontra nem kereskedelmi (DT-F33j): a `licencek.tsv` `kereskedelmi` oszlopa szerint a kereskedelmi módból a `nem` és a `tisztazatlan` források mezői esnek ki (N-F33b). Ez a 17.1 licenc-szűrőjének tényleges tartalma — és jogászi megerősítést kér a Károli–Strong kimenet státuszáról.
3. **A 26 pont fele kész adaton áll.** Az 1–6, 13–16, 18–20 pont az 1. fázis végén teljes adattal fut, motívum nélkül: szó-lap, variancia-térkép, magyar frázis-keresés, konkordancia. Ez az olvasói felület első, motívum nélküli kiadása lehet — a #25 előtt (DT-M1 🟢, 2026-10-06: a #25 kettéválik, ez a #25a), mert nem függ a #23-tól és a #11-től.
4. **A hasznosítás négy iránya**, mind ugyanabból az adatból: (a) olvasói konkordancia és szó-lap (#25a); (b) fordítói eszköz — SZPA-profil B/C üzemmód, variancia-térkép, terminológia (10. szakasz); (c) kutatói MCP a saját és külső kutatónak (9. szakasz; feltételes, DT-M7); (d) licencelhető adatkészlet — a saját rétegek CC BY alatt, ami visszahat a projekt hitelességére (idézhető forrás lesz).
5. **A motívum-réteg ezután nem az alap, hanem a csúcs.** Amit a tanulmányok évek alatt termelnek (★ leletek, döntések, PaRDeS-szint), az erre a kész konkordanciára ül, és attól lesz egyedi, hogy az alatta lévő adat teljes és ellenőrzött. A sorrend tehát: 1. fázis végig → olvasói konkordancia (motívum nélkül) → motívum-réteg ráépítve (#23, #11, #25b).

**0.3 Kereszthivatkozás a Károlin — mi van, mi nincs**

| réteg | mi | hol | természete |
| --- | --- | --- | --- |
| a Károli saját hivatkozásai | a margón öröklött utalások | `konkordancia/Karoli_kereszthivatkozasok.tsv` (HunKar OSIS), `lekerdez.py karoli` | egyenetlen, helyenként hibás (N22: az Ézs 34:11 lista az Ézs 40:11 másolata) |
| idegen rendszerek a Károlira illesztve | TSK, Nave (basokant), openbible.info (#44) — zártan: a Biblia-Felfedező Nave-alapú rendszere | `TSK_kereszthivatkozasok.tsv`, `Nave_basokant.tsv`, `kapcsolatok.tsv` forrás-oszlopa | versszintű, ezért nyelvfüggetlen: bármely fordításra ráül; a kérdés a versszámozás, amit a KK old meg (zsoltárfeliratok, eltolódások) |
| **ami sehol nincs** | Károli-szóalakhoz kötött, Strong-alapú, indokolt kapcsolat: lexikai / tematikus / fordítói (LXX-híd) minősítéssel, napló-döntéssel | `kapcsolatok.tsv` + napló + Károli–Strong | nem a hagyomány versszámain, hanem a párosításon áll; a 12-es lap a különbséget mutatja: amit a margó, a TSK és a Nave egyike sem jelez, de a szó igen |

A fenti rendszerek mind azt mondják, *mi* kapcsolódik; egyik sem mondja, *miért*, és egyik sem tudja, hogy egy kapcsolat lexikai, tematikus vagy fordítói. Ez a projekt saját rétege.

Oct 2, 2026 · @basesoft

## 1. A Károli–Strong négy közvetlen haszna

Az 1–5Mózes Károli–Strong párosítás elkészültével (FELADATOK #22, 2026-10-03; az eredeti terv 1Mózesre szólt) négy dolog indítható azonnal; az 1. és 2. egy Code-futásban, a 3. a meglévő script módosítása, a 4. a 2–3. kimenetét csomagolja.

**1.1 Visszamenőleges ellenőrzés a kész 1Mózes-tanulmányokon**

Eddig a tematikus táblák Strong-száma a TAHOT-kivonatból, a Károli-idézet fejből vagy a zárt forrásból jött; gépi kapcsolat nem volt a kettő között. Ez a „memória vs. lekérdezés" szabály Károli-oldali lezárása.

1. Code végigmegy minden tematikus tanulmány táblázatán, amelynek motívuma a Genezisben nyílik (a 8 lexikonoldalas motívum + az 1Móz 1–16 bővített tanulmányok; a pontos lista greppel: `1Móz` igehely a 7-oszlopos táblában).
2. Minden sorból: versszám + Strong-szám + idézett magyar szó.
3. Összevetés a Károli–Strong fájl ugyanazon versével.
4. Három eredmény: egyezik / nem egyezik (más Strong a szó mellett) / a szó nincs ott (más Károli-változat).

Kimenet: eltéréslista (fájl, sor, állítás, Károli–Strong szerinti érték). Nulla eltérés is érték: bizonyítottan tiszta Genezis-alap.

**1.2 Fordítási variancia-térkép**

Két tábla a Károli–Strong fájlból:

| irány | példa | mire jó |
| --- | --- | --- |
| Strong → magyar szavak | H6754 → „kép", „ábrázat", „bálvány" | Károli elrejt egy motívumszót más magyar szó mögé |
| magyar szó → Strong-számok | „kép" → H6754, H8544, H4541 | hamis párhuzam kiszűrése (azonos magyar szó, más gyök) |

Kimenet: motívumonként magyar szólista; figyelmeztetőlista a több gyököt takaró magyar szavakról. Ez a harmadik kapcsolódási út a TSK (tematikus) és a TAHOT (lexikai) mellett.

**1.3 Magyar nyelvű frázis-keresés**

A kalibrált pozicionális script (szórend mindkét irányban, névmás-kibontás) a Károli–Strong fájlon, az 1.2 magyar szólistájával. Két találathalmaz, három kategória:

- mindkettőben megvan → biztos találat
- csak héberben → Károli másképp fordította; a magyar olvasó nem látja a párhuzamot — tanulmányba illő lelet
- csak magyarban → Károli egybemosott két héber kifejezést — figyelmeztetés

**1.4 Motívum-index 1Mózesből előre** *(feladat: #81 KAROLI\_UJJLENYOMAT, DT77 (16))*

Minden kész motívumhoz egy „Károli-ujjlenyomat": Strong-készlet, magyar szavak (1.2), frázis-minta (1.3), 1Mózes-találatok. Új könyv Károli–Strongja után Code minden ujjlenyomatot ráfuttat; könyvenként jelentés: motívum → új előfordulások → TSK-ban is / csak lexikai. Így minden új könyv automatikusan visszahat a kész tanulmányokra.

```
1.1 ellenőrzés → tiszta Genezis-alap
1.2 variancia-térkép → magyar szólisták motívumonként
1.3 frázis-keresés → magyar vs. héber találatok
1.4 ujjlenyomat → minden új könyvnél automatikus jelentés
```

## 2. Olvasói kimenet: HTML, tipográfia, keresés

A választható tipográfia/színséma és a keresés nem ugyanazt a kérdést dönti el. A tipográfia HTML-ben triviális: CSS-változók, egy kapcsoló, a választás a böngészőben megmarad. A keresésnél a kérdés nem az, hogy HTML-e, hanem hogy hol él az adat lekérdezéskor.

| út | hogyan | mit ad | mit nem |
| --- | --- | --- | --- |
| Statikus oldal + böngészőben futó SQLite (sqlite-wasm) | a TSV-k egy SQLite-fájlban, szerver nélkül, Netlify-on | minden lekérdezés, néhány tíz MB-ig jól | a tartalom védelme — minden letölthető |
| Kis backend (serverless vagy cPanel) | ugyanaz az SQLite egy lekérdező script mögött; a böngésző csak a találatot kapja | adatvédelem, fizetős réteg később | üzemeltetés (minimális) |
| App (UniqueBible-alapon) | offline, saját kereső | erős kereső, offline | platformfüggő, a legtöbb munka |

A DT-F33f (2026-10-04) szerint a STEPBible-származék CC BY 4.0 alatt terjeszthető, így az 1. út sem esik ki; a választást a kereskedelmi/nem kereskedelmi kimenet (DT-F33j) és az offline-igény dönti el, nem a licenc. Mindhárom ugyanabból az SQLite-adatbázisból dolgozik. Az adatvagyon egy fájlba rendezése a sémával (vers, token, Strong, Károli-szó, motívum, kapcsolat, lexikon) bármelyik felületnél kell, és nem dönt el semmit korán. A felület-kérdés csak a védelem és az offline-igény függvénye. Előbb a keresési követelménylista (4. szakasz), abból a séma, abból az SQLite.

## 3. Serverless működés (Netlify)

Nincs saját szerver: a lekérdező function csak kérésre fut, az ingyenes keret (125 ezer hívás/hó) bőven elég.

**Felállás**

1. Statikus oldalak — a renderelt HTML Netlify-ra, mint most.
2. Egy SQLite-fájl az adatvagyonból generálva; nem kerül ki a böngészőbe.
3. Egy Netlify Function (Node/Python), a deploy-csomagban az SQLite-tal; bemenet a keresés paraméterei (`strong=H6754`, `szo=kép`, `frazis=…`), kimenet JSON.
4. Keresőmező az oldalon, pár sor JS: kérés a function-nek, a JSON listává renderelve.

```
olvasó beír → oldal JS → /api/kereses?strong=H6754
                              ↓
            Function megnyitja az SQLite-ot, SQL, ~50 sor JSON
                              ↓
            oldal kirajzolja (Károli-vers + Strong + motívum-link)
```

**Védelem:** az adat csak a function-ben; a böngésző egy lekérdezés válaszát látja. Belépés (Netlify Identity vagy saját token) egyetlen `if` a function elején.

**Korlátok**

- Olvasási adatbázis: minden adatváltozás deploy (nálad amúgy is így van).
- Csomagméret: a function zip-je \~50 MB tömörítve (kicsomagolva \~250 MB) — az SQLite 2–3× tömörödik, a teljes adatvagyon 30–60 MB zip körül, vagyis a határon. Kiút: Cloudflare Workers + D1 (adatbázis külön tárolóban, 10 GB-ig), vagy az SQLite külön fájlként (Netlify Blobs), amit a function indításkor olvas. A kód mindhárom esetben ugyanaz; dönteni csak a mért fájlméret után.
- Hidegindítás: első kérés 1–2 mp, utána gyors.

**Mi kell a repóban:** `eszkozok/sqlite_epit.py` (TSV-kből adatbázis), `netlify/functions/kereses.py` vagy `.js`, a renderelt oldalakban keresőmező + \~40 sor JS. A Python-eszközök és a TSV-rétegek változatlanok; ez egy rájuk épülő kimeneti réteg.

## 4. Egyesített keresési követelménylista (26 pont)

A mintaképek illusztrációk, nem lekérdezett adatok. A 18–26. pont az 5–6. szakasz metszeteiből került a saját rétegéhez.

**Szó / Strong (TAHOT, TAGNT, Károli–Strong, Strong\_szotar)**

| # | kérdés | mintakép |
| --- | --- | --- |
| 1 | Strong → összes vers | `H6754 célem · 17 hely` — 1Móz 1:26 „a mi képünkre", 5:3 „az ő ábrázatjára" ← Károli másképp (18) |
| 2 | magyar szó → Strong-lista | `„kép" → H6754 (14) · H8544 (6) · H4541 (3) · G1504 (9)` |
| 3 | Strong → Károli-szóalakok | `H6754 „kép" 11 · „ábrázat" 3 · „bálvány" 2 · „árnyék" 1` |
| 4 | két Strong egy versben | `H8414 + H0922 → 1Móz 1:2 · Jer 4:23 · Ézs 34:11 (3 vers)` |
| 5 | frázis magyarul és héberül | `héber: 11 vers · Károli: 9 · csak héber: 1Kir 18:24, Jóel 2:32` |
| 6 | gyök és származékok | `H6754 ◀ gyök צלם · rokon H6757 (halál árnyéka)` |
| 18 | Károli-rejtett kapcsolat (új) | motívum-lapon blokk: „ábrázat" 1Móz 5:3 · „bálvány" 4Móz 33:52 · „árnyék" Zsolt 39:7 — ⚠ a magyar szövegben a párhuzam nem látszik |
| 19 | hamis magyar párhuzam (új) | vers-lapon a szó mellett: ⚠ „kép" Károlinál 3 más gyökre is (H8544, H4541, H6459) — nem ugyanaz a szó |
| 20 | Károli-változat eltérés (új, ha mindkét változat strongozva) | `1908: „ábrázatjára" · modern: „hasonlatosságára" · H1823 ↕` |

**Motívum (motivumok, elofordulasok, kapcsolatok)**

| # | kérdés | mintakép |
| --- | --- | --- |
| 7 | vers → motívumok | `1Móz 1:26 ⭐ Isten képmása (ANTROP-001) Peshat, fő előfordulás · Uralom Remez` |
| 8 | motívum → előfordulások könyvenként | `9 fő előfordulás / 23 igehely-sor · 1Mózes 4 · Zsoltárok 2 · Róma 1 …` |
| 9 | vers → kapcsolatok indoklással | `1Móz 1:26 ↔ 9:6 lexikai + TSK · beépítve · „a vérontás tilalma ugyanaz a צֶלֶם"` |
| 10 | könyv → itt nyíló motívumok | `2Mózes · 3 motívum nyílik itt` (publikálási egység) |
| 21 | motívum-metszet (új) | `↔ ezen a versen 2 motívum találkozik: Isten képmása × Bűn gyűrűzése (1Móz 9:6)` |
| 22 | PaRDeS négy mélység (új) | vers-lapon négy sáv: Peshat ▌… (ANTROP) · Remez ▌… (HAMART) · Drash ▌— · Sod ▌— ; az üres sáv is információ |
| 23 | ritka együttállás → motívum-jelölt (új, belső) | `H2617 + H0571 ~11 vers · nincs motívum [jelölt felvétele]` |

**Kereszthivatkozás (TSK + napló)**

| # | kérdés | mintakép |
| --- | --- | --- |
| 11 | TSK + státusz | `1Móz 1:26 · TSK 14 · beépítve 9 · elutasítva 3 · nyitott 2` |
| 12 | csak lexikai (★) — a projekt lelete | külön lap, 5. szakasz |
| 24 | jelentés-réteg eltolódás (◆, a 12-es szűrője, új) | `◆ Zsolt 39:7 BDB 3. („árnyék") ≠ 1Móz 1:26 BDB 1.` |
| 25 | elutasított hagyomány — a 12-es tükre (új) | `Zsolt 8:5 TSK kapcsolja → elutasítva „dicsőség-motívum, nem צֶלֶם"` |

**Lexikon (a szerepmátrix szerint, l. 18.5: TBESG/H, Thayer, BDB, Louw–Nida/SDBH (CC BY-SA), LXX-híd, kiejtés, Nave; a Macula UBS-mezői a DT7 szerint kizárva)**

| # | kérdés | mintakép |
| --- | --- | --- |
| 13 | szócikk magyarul, motívum-tartomány kiemelve | `BDB H6754: 1. képmás ◀ ebben a motívumban · 2. bálványkép · 3. árnyék ◆` |
| 14 | LXX-híd | `H6754 ──LXX──▶ εἰκών G1504 ──ÚSZ──▶ Róm 8:29 · Kol 1:15 · 2Kor 4:4` |
| 26 | LXX-híd mint lelet (★ nyelvhatáron át, új) | `Kol 1:15 TSK: nem ★ · 2Kor 4:4 TSK: nem ★ · Róm 8:29 TSK: igen` |
| 15 | kiejtés | `צֶלֶם célem · εἰκών eikón` |

**Szöveg és navigáció**

| # | kérdés | mintakép |
| --- | --- | --- |
| 16 | szabadszavas keresés a tanulmányokban (FTS) | `„árnyék" → ANTROP-001 tematikus 4. szakasz · HAMART-001 napló` |
| 17 | vers-lap — minden egy képernyőn | 5. szakasz |

**Jelzések — a felület aláírása**

| jel | jelentés | pont |
| --- | --- | --- |
| ★ | a hagyomány nem jelzi | 12, 26 |
| ◆ | másik jelentés-réteg | 24 |
| ⚠ | a magyar szöveg félrevezet | 18, 19 |
| ↔ | motívumok találkoznak | 21 |
| ↕ | Károli-változatok eltérnek | 20 |
| ▌ | PaRDeS-sáv | 22 |

**Hol laknak a három lap-típuson**

| lap | blokkok |
| --- | --- |
| vers-lap | 1, 6, 7, 9, 11, 13–16, 19–22, 24–26 |
| motívum-lap | 8, 12, 18, 21, 24, 25, 26 |
| szó-lap | 1, 2, 3, 6, 13, 14, 18, 19 |
| belső munkalap | 23, a „nyitott / még nem vizsgált" szűrők |

## 5. A két kiemelt lap: 12-es (lelet-lap) és 17-es (vers-lap)

A 17 pontból a 12-es az, ami csak ennek a projektnek az adatából válaszolható meg; a 17-es az olvasó belépési pontja, amin a többi kattintással elérhető.

**5.1 A 12-es: csak lexikai kapcsolat, amit a hagyomány nem jelez**

Két kört vetünk össze: a lexikai kört (ugyanaz a Strong, ugyanabban a motívumban — a projekt gépi keresése) és a hagyományos kört (TSK, a 19. századi kézi kereszthivatkozás-gyűjtemény). A 12-es a különbség.

```
vers X-hez:
  A = összes vers, ahol a motívum Strong-készlete előfordul
  B = összes vers, amit a TSK X-hez kapcsol
  12-es = A − B
```

| kategória | mit jelent |
| --- | --- |
| A és B is | a hagyomány és a szó is kapcsolja — biztos |
| csak B | a hagyomány gondolati kapcsolata, más szóval |
| csak A (★) | a projekt saját lelete |

Példa: a צֶלֶם (H6754) a Zsolt 39:7-ben és 73:20-ban „árnyék, puszta kép" értelemben áll; a TSK ezeket az 1Móz 1:26-hoz nem kapcsolja, a tanulmány már beépítette. Minden ★ sor mellé a napló döntése kerül: beépítve / elutasítva / nyitott, indoklással — a naplóval együtt ez a projekt tényleges hozzáadott értéke, nem puszta gépi lista. Csak itt válaszolható meg, mert a Strong-keresés és a TSK sok helyen van, de a motívumonként átnézett, indokolt döntés minden találatról csak a PaRDeS naplóiban.

```
┌─ Isten képmása · lexikai leletek ──────────────────────┐
│ Strong-készlet: H6754 צֶלֶם · H1823 דְּמוּת               │
│ TSK 1Móz 1:26-hoz: 14 · lexikai találat: 23             │
│ ★ csak lexikai (TSK nem jelzi): 11                      │
├─ ★ csak lexikai ────────────────────────────────────────┤
│ Zsolt 39:7   H6754  „mint egy árnyék jár az ember"      │
│   beépítve · Remez ◆ „BDB 3. jelentés: a képmás          │
│   ellenpontja"                       [vers-lap] [napló]  │
│ Zsolt 73:20  H6754  beépítve · Remez ◆                   │
│ 1Sám 6:5    H6754  elutasítva · „kultikus tárgy"         │
│ Ez 23:14    H6754  nyitott · döntésre vár                │
│ … (+7) · még nem vizsgált: 0                             │
├─ lexikai + TSK (egyezik) ── 12 tétel, összecsukva ──────┤
├─ csak TSK (hagyomány, más szóval) ── 3 tétel ───────────┤
├─ Összesítés ────────────────────────────────────────────┤
│ 11 lelet → 6 beépítve · 3 elutasítva · 2 nyitott         │
└──────────────────────────────────────────────────────────┘
```

Második használata befelé: munkalista — `státusz = nyitott` szűrővel. A nem feldolgozott Strong-találatokra külön státusz: *még nem vizsgált* — ne keveredjen a „nyitott"-tal; ez dönti el, mennyire hiteles a lap.

**5.2 A 17-es: vers-lap**

Egy igehely → minden, amit a projekt tud róla, egy képernyőn. Nem új lekérdezés, hanem a többi összeszerelve. Az olvasó így olvas Bibliát: egy versnél áll, és onnan akar tovább. Három lap-típus — vers, szó, motívum — és az egész adatvagyon bejárható.

```
┌─ 1Móz 1:26 ───────────────────────────────────────┐
│ Károli-szöveg, a Strong-szavak kattinthatók      │
│ (1908-as / modern változat kapcsoló)              │
├─ Szavak ──────────────────────────────────────────┤
│ képünkre  H6754 צֶלֶם  célem   [szócikk] [előford.]│
│   ⚠ „kép" 3 más gyökre is                         │
│ hasonlatosságunkra H1823 דְּמוּת demút             │
├─ Motívumok ───────────────────────────────────────┤
│ ⭐ Isten képmása (ANTROP-001)   Peshat  fő előford.│
│    Uralom a teremtés felett     Remez              │
│    ↔ 2 motívum találkozik                          │
├─ Négy mélység ────────────────────────────────────┤
│ Peshat ▌…  Remez ▌…  Drash ▌—  Sod ▌—              │
├─ Kapcsolatok ─────────────────────────────────────┤
│ 1Móz 5:3   lexikai + TSK   beépítve                │
│ Zsolt 39:7 csak lexikai ★◆ beépítve                │
│ Kol 1:15   tematikus       beépítve   LXX εἰκών → │
├─ TSK ─────────────────────────────────────────────┤
│ 14 kapcsolat → 9 beépítve, 3 elutasítva, 2 nyitott│
├─ Szócikkek ───────────────────────────────────────┤
│ BDB H6754 (magyar, motívum-tartomány kiemelve)    │
│ LXX: εἰκών G1504 → Róm 8:29, Kol 1:15, 2Kor 4:4   │
├─ Tanulmány ───────────────────────────────────────┤
│ → ANTROP-001 tematikus, 3. szakasz                │
└───────────────────────────────────────────────────┘
```

| blokk | lekérdezés |
| --- | --- |
| Károli-szöveg + kattintható szavak | 1, 20 |
| Szavak | 6, 15, 19 |
| Motívumok, négy mélység | 7, 21, 22 |
| Kapcsolatok | 9, 12, 24 |
| TSK | 11, 25 |
| Szócikkek, LXX | 13, 14, 26 |
| Tanulmány-link | 16 |

Nem kell új adat: egy sablon, amit a function versenként tölt ki (nyolc SQL egy kérésre, vagy előre összerakott nézet). Statikus változatban minden versre előre renderelt oldal (31 ezer vers, belefér).

## 6. További értékes metszetek (A–I)

Az adatvagyon rétegei — Strong, Károli-fordítás, TSK, napló, LXX-híd, szótár-jelentések, PaRDeS-szint, motívum — páronként is adnak olyan különbségeket, amit máshol nem kapni. Ezek a 4. szakasz 18–26. pontjai; itt a lekérdezés és a mintakép.

|  | metszet | lekérdezés | hol | pont |
| --- | --- | --- | --- | --- |
| A | Károli-rejtett kapcsolat — ugyanaz a Strong, más magyar szó | motívum Strong-készlete → versek, ahol a Károli-szó eltér a fő szóalaktól | motívum-lap | 18 |
| B | hamis magyar párhuzam — ugyanaz a magyar szó, más gyök | magyar szó → több Strong a motívum-környezetben | vers-lap, szó mellett | 19 |
| C | LXX-híd mint ÓSZ→ÚSZ kapocs — a fordító szóválasztása köt, a TSK nem jelzi | héber Strong → LXX görög → ÚSZ-előfordulás, TSK-val összevetve | motívum-lap | 26 |
| D | jelentés-réteg eltolódás — ugyanaz a Strong, másik BDB-jelentés | motívum Strong → versek, ahol a napló másik BDB-jelentést rendelt | a 12-es lap sorjelölése ◆ | 24 |
| E | ritka együttállás — két Strong, kevés közös vers | Strong-páronként közös vers-szám, építéskor számolva | belső munkalap | 23 |
| F | motívum-metszet — két feldolgozott motívum egy versen | `elofordulasok` önmagával joinolva versre | vers- és motívum-lap | 21 |
| G | PaRDeS-szint szerinti olvasat — egy vers négy mélysége | vers → motívumok × szint | vers-lap | 22 |
| H | elutasított hagyomány — a TSK kapcsol, a projekt elutasította | napló `elutasítva`, forrás TSK | a 12-es lap tükörblokkja | 25 |
| I | Károli-változat eltérés — 1908 vs. modern más szóval | csak ha mindkét változat strongozva | vers-lap, a szöveg alatt | 20 |

**Mintaképek** (illusztrációk)

```
A) ┌─ Isten képmása · Károli másképp fordítja ──────────┐
   │ „ábrázat"  1Móz 5:3    „az ő ábrázatjára"            │
   │ „bálvány"  4Móz 33:52  „bálványképeiket"             │
   │ „árnyék"   Zsolt 39:7  „mint egy árnyék"             │
   │ ⚠ a magyar szövegben a párhuzam nem látszik          │
   └───────────────────────────────────────────────────────┘

B) │ képünkre  H6754                                       │
   │  ⚠ „kép" Károlinál 3 más gyökre is: H8544, H4541,    │
   │    H6459 — nem ugyanaz a szó.           [részletek]   │

C) ┌─ Isten képmása · az ÚSZ-be a Septuagintán át ──────┐
   │ H6754 צֶלֶם ──LXX──▶ εἰκών G1504                       │
   │ Kol 1:15  „a láthatatlan Isten képe"   TSK: nem ★     │
   │ 2Kor 4:4  „aki az Isten képe"          TSK: nem ★     │
   │ Róm 8:29  „Fia ábrázatához"            TSK: igen      │
   │ ★ a kapcsolat a fordító szóválasztásán át             │
   └────────────────────────────────────────────────────────┘

D) │ Zsolt 39:7   H6754   beépítve · Remez                  │
   │   ◆ BDB 3. jelentés („árnyék") — nem az 1. („képmás"), │
   │     mint 1Móz 1:26-ban.                                │

E) ┌─ Ritka Strong-párok · még nincs motívum ───────────┐
   │ H8414 + H0922   3 vers   → TEREMT-002 ✔              │
   │ H6754 + H1823   3 vers   → ANTROP-001 ✔              │
   │ H2617 + H0571  ~11 vers  → nincs motívum  [jelölt]   │
   └───────────────────────────────────────────────────────┘

F) │ ↔ metszéspont: Isten képmása × Bűn gyűrűzése (1Móz 9:6)│

G) ┌─ 1Móz 9:6 · négy mélység ───────────────────────────┐
   │ Peshat  ▌Vérontás tilalma — a képmás miatt   (ANTROP) │
   │ Remez   ▌Bűn gyűrűzése: Káin → özönvíz → itt (HAMART) │
   │ Drash   ▌—                                            │
   │ Sod     ▌—                                            │
   └───────────────────────────────────────────────────────┘

H) ┌─ Isten képmása · ahol nem követjük a TSK-t ─────────┐
   │ Zsolt 8:5  elutasítva „dicsőség-motívum, nem צֶלֶם"    │
   │ Ef 4:24    elutasítva „κτίζω; εἰκών nem szerepel"      │
   │ Jak 3:9    beépítve tematikusként „ὁμοίωσις, a hídon" │
   └────────────────────────────────────────────────────────┘

I) │ 1908:   „az ő ábrázatjára"        H1823               │
   │ modern: „a maga hasonlatosságára" H1823               │
   │ ↕ fordítás-változás ugyanarra a szóra                 │
```

**Rangsor az egyediség szerint**

|  | mi kell hozzá, ami máshol nincs |
| --- | --- |
| 12, H | napló-döntések |
| G, F | motívum + PaRDeS-besorolás |
| C, D | LXX-híd + jelentés-hozzárendelés a naplóból |
| A, B, I | Károli–Strong (készül) |
| E | semmi egyedi, de motívum-jelöltet termel |

A 12, H, G, F ugyanabból az egy táblából válaszolható: a naplók adatosított formájából — ez a következő lépés, egyszerre négy kiemelt funkció alapja. Az A és B a Károli–Strong első valódi olvasói haszna, napló-adat nélkül: amint 1Mózes Károli–Strongja megvan, futtatható.

## 7. Elég-e az SQLite?

Igen, mind a 26 pontra.

**Méret:** teljes Biblia \~31 ezer vers, \~600–700 ezer Strong-címkés token, TSK \~600 ezer link, szócikkek, naplósorok — indexekkel 50–150 MB (becslés). Olvasási lekérdezés ebből milliszekundum.

| művelet | pontok | SQLite-ban |
| --- | --- | --- |
| join + szűrés | 1–4, 6–11, 13–15, 18–22, 25 | sima SQL, indexekkel azonnali |
| halmazkülönbség (A − B) | 12, 24, 26 | `EXCEPT` vagy `LEFT JOIN … IS NULL`, egy lekérdezés |
| teljes szöveg | 16 | beépített FTS5, magyar szótövezés nélkül is használható |

**Két pont előkészítést igényel**

- 5 (frázis-keresés): pozíció-oszlop a token-táblában (`vers, sorszám, strong, karoli_szo`); az „X után legfeljebb N tokenre Y" self-join a sorszámra. A kalibrált script logikája (szórend mindkét irányban, névmás-kibontás) a Python-oldalon marad, az eredmény táblába írva.
- 23 (ritka együttállás): az összes Strong-pár közös verseinek számolása kérésenként drága; egyszer, építéskor, `strong_parok(a, b, n)` táblába.

Általános elv: ami számítás, az építéskor fut Pythonban; a lekérdező csak kész táblákat olvas. A napló-adatosítás ugyanígy build-lépés.

**Mikor nem elég már**

- ha az olvasók írnak (jegyzet, kedvenc) több felhasználóval egyszerre → Postgres vagy Cloudflare D1
- ha jelentés-alapú („hasonló értelmű versek") keresés kell → vektor-index, külön eszköz
- több száz MB fölött még megy, csak a Netlify-csomagméret korlátoz (3. szakasz), nem az SQLite

A mostani körben egyik sem áll fenn. Az SQLite marad, és bármelyik felület-út ugyanezt a fájlt viszi.

## 8. Hosting: Netlify Function vs. cPanel

Ha van cPanel-tárhely, az egész (HTML + API + SQLite) menjen oda — a legkevesebb mozgó alkatrész a három út közül. A tárhely dönti el, hogy PHP vagy Python a lekérdező.

| szempont | Netlify Function | cPanel |
| --- | --- | --- |
| csomagméret-korlát | \~50 MB tömörítve (becslés) | nincs — az SQLite 1 GB is lehet |
| hidegindítás | 1–2 mp az első kérésnél | nincs, mindig fut |
| adat védelme | a function csomagjában | a webgyökér fölött — még jobb |
| frissítés | deploy | egy fájl feltöltése (FTP vagy cPanel Git) |
| költség | ingyenes keret | évi néhány ezer Ft; meglévő tárhelyen 0 |
| belépés / fizetős réteg | Netlify Identity | PHP session vagy saját token |
| statikus oldalak helye | Netlify CDN | ugyanaz a tárhely (magyar olvasótábornak nem számít) |

**cPanel felállás**

| elem | hely | megjegyzés |
| --- | --- | --- |
| renderelt HTML | `public_html/` | változatlan |
| SQLite adatbázis | `~/adat/pardes.db` (a `public_html` fölött) | kívülről nem elérhető, csak a script olvassa |
| lekérdező script | `public_html/api/kereses.php` | PHP PDO sqlite beépített; vagy Python Passenger („Setup Python App"), ha a tárhely adja |
| keresőmező JS | a renderelt oldalakban | ugyanaz, csak `/api/kereses.php?strong=…` címre hív |
| építő script | helyben vagy Claude Code-ban (Python) | elkészíti a `pardes.db`-t; egy fájlként megy fel |

Hátrány: a statikus oldalak sem a Netlify CDN-en lesznek. HTML Netlify-on + API cPanelen lehetséges, de két hely és CORS — nem éri meg.

Ugyanez a táblázat Excelben: `hosting_osszehasonlitas.xlsx` (három lap, döntésnaplóval).

## 9. Saját MCP-szerver és AI-réteg

**Állapot (DT-M7, 2026-10-05): az MCP-szerver feltételes.** Kikerül a MUNKATERV 3. hullámából; akkor készül, ha a chatből való adathozzáférés ténylegesen hiányzik, vagy repó nélkül dolgozó munkatárs lesz. Előbb a `lekerdez.py` automatikus naplózása (#61), amely a DT-M3 szerint a `lepes` mezőbe a kutatási lépés kódját (lépésen kívül `adhoc`-ot), a proveniencia-sorba a csatornát írja. A szakasz többi része az MCP tervezett alakját írja le arra az esetre, ha elindul.

Az MCP-szerver és egy saját AI-modell nem oldja meg a lekérdezéseket — az SQLite oldja meg; ők azt döntik el, ki és hogyan fér hozzá. Három réteg ugyanazon az adaton:

```
                    ┌──────────────┐
                    │  pardes.db   │   ← az adat
                    └──────┬───────┘
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
   kereses.php        MCP-szerver        AI-réteg
   (olvasó)           (te, Claude)       (olvasó, nyelvi)
   SQL, ingyen        SQL eszközként     NL → SQL → magyarázat
```

| réteg | kinek | mibe kerül | mit ad |
| --- | --- | --- | --- |
| lekérdező (PHP/function) | névtelen olvasó | semmibe kérésenként | a 26 pont előre megírt SQL-ként |
| MCP-szerver | te, Claude Code, subagentek | modell-token kérésenként | a meglévő CLI eszközzé csomagolva (l. 17.2): `lekerdez.py gerinc / scan / kollokacio / igealak / lxx-hid / tsk / karoli`, `jelolt.py`, `gate.py`, `ellenoriz.py`, `emeles.py lista`; új csak a 26 pontból hiányzó (vers-lap, lelet-lap, Károli-szóalakok), ahol a `lekerdez.py` új alparancsa az eszköz, nem külön SQL; minden hívás proveniencia-sorral és `auditok.tsv`-sorral |
| AI-réteg (később) | olvasó, aki nem tud Strong-számot | modell-token → bejelentkezett/fizető olvasónak | természetes nyelv → lekérdezés → találat + magyarázat; jelentés-alapú keresés embeddinggel |

**Miért kell az MCP, ha a prompt már adatból kér választ.** A chatben a szabálynak ma csak a tiltó fele működik: fejből nem mondok igehelyet, de a repó TSV-ihez nem férek hozzá, így a válasz „greppeld le". Az MCP a „ne tippelj"-t „nézd meg"-re fordítja. Code-ban a különbség a költség: egy hívás egy sor eredménnyel, nem egy többmegás TSV a kontextusban; és a 26 lekérdezés egyszer van megírva.

**Tényleges többlet (DT-M7 szerint újravizsgálva, 2026-10-05)**

1. Nyomon követhetőség: minden hívás automatikusan naplózható — a tanulmány állításai mögé a bizonyíték kerül, nem csak a forrás neve. Ez MCP nélkül is elérhető: a `lekerdez.py --naplo` (#61 LEKERDEZ\_NAPLO, DT-M3) maga írja az `auditok.tsv`-sort.
2. Strukturált hívás: az eszköz paraméterezett, a válasz proveniencia-sort hordoz.
3. Munkatárs repó nélkül: lektor vagy társszerző chatből kérdezi az adatot — csak hostolva, VPS-költséggel.

**Nem MCP-előny (DT-M7):** a modellfüggetlenség, a commit előtti kapu és az adat-integritás tesztje — ezek MCP nélkül is megvalósíthatók (CLI-parancsok, hook, az építő tesztjei). Az olvasói AI-réteg spekulatív: nem „már kész", külön döntést kér.

**Mire nem jó:** nem olvasónak (nincs MCP-kliense, token-költség); nem forrás (semmit nem ad az adatvagyonhoz); első körben nem ír (naplóba írás csak ha bevált).

**Hol fut:** \~100 sor Python (FastMCP) a `sqlite_epit.py` után. Claude Code-ból helyben, nulla üzemeltetés. claude.ai-connectorként hostolt HTTPS-végpont kell — ezt a cPanel-tárhely jellemzően nem tudja; kis VPS vagy Fly.io-szerű hely. Ezért Code-ban kezdeni, hostolni csak ha a chat-használat tényleg hiányzik.

**A kereskedelmi kérdés:** egy „kérdezd a PaRDeS-t" chat a 26 lekérdezés fölött eladható funkció, az SQL-kereső önmagában kevésbé — de csak akkor hiteles, ha minden válasz alatt ott a tényleges igehely-lista az adatbázisból.

## 10. Az SZPA fordítói profil hasznosítása

A profil (`SZPA_FORDITOI_PROFIL_prompt.md` v0.1, Mt 1–4 mintáján) szabályokat rögzít, nem szöveget, ezért a saját adatkincre alkalmazható — három helyen közvetlenül, egy helyen fordítva.

| hol | hogyan | hatás |
| --- | --- | --- |
| szótár-réteg (B üzemmód) | a `Strong_szotar` / BDB-fordítás magyar megfelelője mellé második oszlop: SZPA-stratégia szerinti megfelelő, a profil 7. pontjának jelölésével | szó-lapon: „Károli: ország · szó szerint: uralom \[SZPA-B\]" — a 18-as pont ellenpárja. Korlát: a profil görög; héberre csak az LXX-hídon át, `[F]` szinten |
| lektorálás (C üzemmód) | az 1.2 tiltólista és az 1.1 kötött párok gépi ellenőrzése a tanulmányok prózáján és a BDB-fordítás magyar szövegén; kimenet a profil C-táblázata | tudjuk, hol használ a projekt saját szövege egyházi műszót jelöletlenül — egy futás a meglévő lektor-scriptben |
| munkafordítás (A üzemmód) | csak a 18-as és 5-ös pontnál: ahol Károli elrejti a párhuzamot, egy sor szó szerinti visszaadás a profil szerint, jelölve | kimondja, amit eddig prózában kellett magyarázni |
| fordítva: Károli-profil | az 1.2 variancia-térkép (Strong → Károli-szóalakok, előfordulás-számmal) maga a Károli konkordancia-táblája; kötött/nem kötött megkülönböztetés számmal | ugyanaz a sablon, B/V/F helyett előfordulás-arány; a két profil egymás mellett = fordítási variancia két fordítóra |

**Két óvatosság**

- Az SZPA szóválasztásai felekezeti hagyományt hordoznak (szellem, alámerít, uralom). A projekt olvasója Károlit olvas; alapértelmezett megfelelőként elcsúszna a regiszter. Ezért jelölt alternatíva-réteg, nem alap — ahogy a profil az 1.4-et kezeli.
- A `[B]` szabályok csak Mt 1–4-en biztosak. A szótár-rétegbe csak az kerülhet `[B]`-ként, amit a második minta (Róm 1–4, Jn 1) is igazol; addig minden `[V]`.

Első lépés: a lektorálási audit — script + lista, egy futás, és megmutatja, mennyit érint a kérdés a kész szövegben.

## 11. Külső MCP-k és az openbible.info

A `nirajagarwal/bible-mcp` bekötése az adatvagyont nem gazdagítja, a munkafolyamatot átmenetileg igen; egy forrásjelölt kerül elő belőle.

| mi | gazdagodás |
| --- | --- |
| bible-mcp mint connector | 0 adat: ami használható, megvan (MACULA, BDB, Abbott-Smith, Strong); ami nincs (versemap, idézetgráf, embeddingek) NC, tilos. Kényelem a saját MCP-ig; utána nincs feladata |
| openbible.info kereszthivatkozások (CC BY, \~345 ezer, közösségi szavazással) | 1 új réteg a kapcsolatokhoz, rangsorral; közvetlenül onnan, nem az MCP-n át; `datasetek.tsv`-be, F44 licencellenőrzéssel |
| mctx.ai Bible Study, Macaroon, Doxa, Bible Glide | 0 |

**Hatás a 12-es lapra:** a „hagyomány" tengely kettéválik. Egy ★ találat mellé: openbible.info jelzi-e, hány szavazattal. Ha igen, a lelet nem egyedi, csak a TSK-ból hiányzik; ha ott sincs, a projekt tényleg egyedül látja. A „honnan jött" tengely a `jeloltek.forras_kereses` mezője (SEMA 2.4), amely új értéket kap (`openbible …`); a `kapcsolatok` séma érintetlen (l. 22.1).

|  | TSK | openbible.info |
| --- | --- | --- |
| eredet | 19. századi kézi gyűjtés | közösségi szavazás, 2000-es évek |
| méret | \~600 ezer | \~345 ezer |
| rangsor | nincs | van (szavazatszám) |
| licenc | PD | CC BY |

A bible-mcp bekötését a saját MCP-szerver utánra halasztani; ha az megvan, a külső feleslegessé válik.

## 12. Adatlekérő promptok

Két rendszerprompt az MCP-eszközökre (amíg nincs MCP: ugyanezek a lekérések egy Python-függvény, ami a TSV-kből állítja össze a Markdown-blokkot). Mindkettő csak adatot gyűjt — nem fordít, nem értelmez, fejből nem pótol; üres eszköz-válasz = „—".

**12.1 Szócikk-adatlekérés — a BDB-fordító agentnek**

Ma a fordító agent a BDB angol szócikkét kapja, és a magyar megfelelőt a szótári jelentésből választja. Eszközzel a megfelelő Károli tényleges, súlyozott gyakorlatából jön, a példák Károli-idézetek — a Károli-stílust az adat adja, nem a modell. Ezért nem a futó #38-at megállítani, hanem a teljes Károli–Strong után egy javító menetet tervezni, amely minden kész szócikkhez beírja a Károli-oszlopot.

```markdown
# Szócikk-adatlekérés — rendszerprompt · v0.1 · 2026-10-02

## Szerep
Adatlekérő vagy. Egy Strong-számhoz összegyűjtöd a projekt saját adatából,
amit a fordító agentnek tudnia kell, mielőtt a BDB-szócikket magyarítja.
Nem fordítasz, nem értelmezel, nem egészítesz ki emlékezetből. Ha egy
eszköz nem ad vissza semmit, azt üresnek jelölöd, nem pótolod.

## Bemenet
- `strong`: pl. H2617
- `lemma`: pl. חֶסֶד (ellenőrzéshez)

## Lekérések (sorrendben, mind kötelező)
1. `karoli_valtozatok(strong)` → magyar szóalak + előfordulás-szám, csökkenő;
   mellé a `lefedettség` mező: mely könyvek strongozottak.
2. `strong_elofordulasok(strong, szoalak=<minden szóalak az 1.-ből>, minta=3)`
   → szóalakonként legfeljebb 3 vers: igehely + Károli-szöveg, a szó kiemelve.
3. `vers_motivumai(ref)` a 2. minden igehelyére → motívum-id + PaRDeS-szint | „—".
4. `lxx_hid(strong)` → görög Strong + lemma + ÚSZ-előfordulások száma | „—".
5. `szocikk(strong)` → meglévő magyar lexikonoldal/szócikk | „—".
6. `naplo_jelentesek(strong)` → naplóban rögzített BDB-jelentésréteg-
   hozzárendelések (vers → BDB-jelentés száma) | „—".

## Kimenet (pontosan ez a szerkezet)
### <strong> <lemma>
**Lefedettség:** <könyvlista; ha nem teljes: „RÉSZLEGES — az arányok csak
a lefedett könyvekre érvényesek">
**Károli-szóalakok** | szóalak | db | példák (igehely „idézet") |
**Motívum-kapcsolat** | igehely | motívum | szint |
**LXX-híd:** <G-szám lemma, ÚSZ-előfordulás: n> | —
**Meglévő magyar szócikk:** <szöveg> | —
**Naplóban rögzített jelentés-hozzárendelés:** <vers → BDB n.> | —

## Szabályok
- Minden szám és idézet eszköz-kimenetből. Fejből semmi.
- Károli-idézet szó szerint, a vizsgált szó **félkövér**.
- Részleges lefedettségnél az első sor: „A Károli-arányok Genezis-mintából
  származnak."
- Ha két eszköz ellentmond, mindkettőt közlöd, egy sorban jelzed. Nem döntesz.
- Kimenet után nincs összefoglaló, javaslat, kommentár.
```

A fordító agent promptjába egy sor: „A magyar megfelelőt és a példaverseket az adatlekérés táblájából veszed; ahol a BDB-jelentéshez nincs Károli-szóalak, ezt `[NINCS KÁROLI-ALAK]` jelöli."

**12.2 Vers-lap adatlekérés — a 17-es lap adatforrása**

Itt az igehely a belépő, ezért a Strong-szintű lekérések a vers minden Strongjára futnak. A kimenet egy az egyben a vers-lap sablonjának adata; a renderelő (PHP/function) ugyanezt a kilenc lekérdezést futtatja, csak HTML-t rajzol belőle.

```markdown
# Vers-lap adatlekérés — rendszerprompt · v0.1 · 2026-10-02

## Szerep
Adatlekérő vagy. Egy igehelyhez összegyűjtöd a projekt saját adatából
mindent, ami a vers-lapra kerül. Nem értelmezel, nem fordítasz, nem
egészítesz ki emlékezetből. Üres eszköz-válasz = „—", nem pótlás.

## Bemenet
- `ref`: igehely projekt-formában, pl. 1Móz 1:26
- `valtozat`: `1908` | `modern` (alapértelmezés: 1908)

## Lekérések (sorrendben, mind kötelező)
1. `karoli_vers(ref, valtozat)` → szöveg; tokenenként sorszám, Károli-szóalak,
   Strong, lemma, kiejtés. Nem strongozott vers: szöveg + „NEM STRONGOZOTT".
2. `karoli_vers(ref, <másik változat>)` → csak szöveg, az eltérő tokenek (↕).
3. `vers_motivumai(ref)` → motívum-id, cím, PaRDeS-szint, fő előfordulás (⭐).
4. `kapcsolatok(ref)` → kapcsolt igehelyek: forrás (lexikai | TSK | mindkettő |
   tematikus), közös Strong, napló-státusz (beépítve | elutasítva | nyitott |
   még nem vizsgált), indoklás első 60 karaktere, LXX-híd jelzés.
5. `tsk(ref)` → TSK-kapcsolatok száma, státuszonként.
6. `szocikk(strong)` az 1. minden Strongjára → van-e magyar szócikk; a napló
   ehhez a vershez rendelt BDB-jelentésszáma | „—".
7. `lxx_hid(strong)` az 1. minden Strongjára → görög Strong + lemma + ≤3 ÚSZ-hely.
8. `magyar_szo_strongok(szoalak)` az 1. minden szóalakjára → hány más Strong
   áll ugyanezen magyar szó mögött (⚠ ha > 0).
9. `tanulmany_hivatkozas(ref)` → tanulmány-azonosító + szakasz.

## Kimenet (pontosan ez a szerkezet)
### <ref> (<valtozat>)
**Szöveg:** <vers; strongozott szó után [Hnnnn]; ↕ szavaknál lábjegyzet
„<másik változat>: <szóalak>">
**Szavak** | # | szóalak | Strong | lemma | kiejtés | ⚠ más gyök | szócikk | LXX |
**Motívumok** | motívum | cím | szint | fő | — több motívumnál utolsó sor
„↔ <n> motívum találkozik"
**Négy mélység** | Peshat | Remez | Drash | Sod | (motívum-id vagy —)
**Kapcsolatok** (mindkettő → csak lexikai ★ → tematikus → csak TSK)
| igehely | forrás | Strong | státusz | indoklás | jel | — ★ csak lexikai,
◆ másik BDB-jelentés, LXX ha hídon át
**TSK:** <n> → <b> beépítve · <e> elutasítva · <ny> nyitott · <nv> még nem vizsgált
**Szócikkek:** Strongonként: van/nincs; ehhez a vershez rendelt BDB-jelentés | —
**LXX:** <H → G lemma → ÚSZ-helyek> | —
**Tanulmány:** <id, szakasz> | —

## Szabályok
- Minden adat eszköz-kimenetből; igehelyet, Strongot, idézetet fejből soha.
- Károli-szöveg betűhíven, a változat megjelölésével.
- Ha a 4. és 5. száma nem egyezik: „ELTÉRÉS: <n> TSK-sor nincs a kapcsolatok
  táblában" — nem javítod.
- A „még nem vizsgált" nem olvasztható a „nyitott"-ba.
- Kimenet után nincs összefoglaló, javaslat, kommentár.
```

## 13. Az MCP a BDB-fordításnál (#38)

A chatben ma is adatból dolgozom, de úgy, hogy a teljes fájlt lehúzom GitHubról és greppelek benne. Ez nem tud táblákat összekapcsolni, nagy fájlt (TAHOT, 349 ezer soros KJV) kezelni, és minden menetben újraírja a lekérdezést. Az MCP a grep rendezett formája: egyszer megírt, tesztelt lekérdezések bármelyik menetből.

A #38-nál a legtöbbet adja, mert a fordítás 13 adagban fut, és minden adag elölről kezdi:

|  | ma | MCP-vel |
| --- | --- | --- |
| terminológiai következetesség adagok között | a 9. adag nem tudja, mit döntött a 3. a rokon gyöknél | `kesz_megfelelok(gyök)` — a már lefordított rokon szócikkek magyar választásai |
| Károli-megfelelő | modell-stílus (a Sonnet közelebb a Károlihoz, de ingadozik) | `karoli_valtozatok(strong)` — súlyozott gyakoriság, modellfüggetlen, indokolható |
| példaversek | a BDB angol helyeit a modell maga fordítja magyarra | `strong_elofordulasok(strong, szóalak, minta=3)` — valódi Károli-versek betűhíven |
| a kész rétegek | nincsenek a szócikkben | `lxx_hid` (#43 kimenete), bdb\_roots rokonsor, motívum-tagság, meglévő lexikonoldal — egy-egy hívás |
| ellenőrzés commit előtt | az ellenőr is olvasással dolgozik | `ellenoriz_szocikk(strong)` — minden idézett igehelyben ott a Strong, a megfelelő szerepel Károlinál, a rokon szócikkek nem mondanak ellent |

A #38 nem áll meg emiatt: a 6. adag a #56 BDB\_ADATBLOKK adatblokkjával indul (DT-F38i 🟢), a javító menet (teljes Károli–Strong után) az 1–5. adagon pótol. Az adagok közötti következetesség MCP nélkül is megoldható a már létező (SEMA 2.15) `terminologia.tsv`-vel, amit minden adag olvas — ez a futó #38-nak azonnal segít.

**Tokenköltség.** Az adatblokk szócikkenként 400–800 tokennel növeli a bemenetet (8 090 szócikknél 3–6 millió, becslés), és minden eszközhívás külön kör. Megtérülés: elmaradó javító menetek (terminológiai eltérés az M1-nél újrafordítást jelent), kevesebb kitalált idézet, célzottabb kontextus a lexikonoldal vagy TSV-részlet helyett. Szócikkenként drágább, helyes szócikkenként olcsóbb. Ezért a #38-nál a 12.1 lekérések **build-lépésként** futnak (Python előre számolja a blokkot, és az adagfájlban a BDB-szócikk elé fűzi), nem MCP-hívásként: ugyanaz az adat, nulla hívás-overhead, szabott méret. Az MCP az ad hoc kutatói kérdésé; a tömeges fordításé a build.

## 14. Visszaírás az adatba

Lehetséges, de nem az SQLite-ba: a `pardes.db` építési melléktermék, az igazság forrása a repó TSV-je. Az író eszköz a forrásfájlt módosítja (sor hozzáfűzése), git-commitot tesz egy ágra, és újraépíti az adatbázist — ugyanaz, amit Code ma kézzel tesz, egy hívásban. A PR-review és a `fuggetlen-ellenor` nem esik ki.

| írható | nem írható |
| --- | --- |
| `terminologia.tsv` — fordítói döntés (Strong, magyar megfelelő, indok, adag) | TAHOT/TAGNT, Károli–Strong, TSK — forrásadat, csak építő script írja |
| napló-döntés (`dontes_rogzit`: motívum, vers, státusz, indok) | `lxx_dontesek.tsv` és más lezárt döntéstáblák — csak felhasználói döntés után, külön menet |
| motívum-jelölt felvétele (23-as pont) | `DONTESEK.md` — a DT-sor mindig a felhasználóé |

Három feltétel: minden írás proveniencia-oszloppal (modell/menet, mikor, melyik brief — a repó `proveniencia` konvenciója); csak hozzáfűzés, felülírás nem (javítás új sor „felülírja: #n" jelzéssel); író eszköz csak Code-ban, helyben — hostolt végponton írási jog nem.

Sorrend: első kör csak olvasó. A `terminologia_rogzit` lehet az első író eszköz (a #38 miatt, és egy TSV-sor hozzáfűzése a legkisebb kockázat); ha bevált, `dontes_rogzit`.

## 15. A HF-forrásáttekintés (2026-10-02) hozama a tervhez

A „Bible models on Hugging Face" chat (50 kör) nyomán három feladat jött létre, és mind a felhasználó kézi 0. lépésére várt, mert a HF és az openbible.info a cloud proxyról nem elérhető; a három fájl 2026-10-04-re bent van (F43.0, F44.0, F44.1):

| feladat | kézi 0. lépés | hová |
| --- | --- | --- |
| #43 LXX\_BRIDGE (✅ kész, PR #167; DT-F43 ✅) | `lxx_bridge` tábla + licencsor | `adat/kulso/lxx_bridge.tsv`, `adat/kulso/LICENC.md` — bent (F43.0) |
| #44 LICENC\_UTOKOVETES (✅ kész, PR #205) | a `k-mktr/karoli_bible_hu` kártya licence + README szó szerint — a Károli-rész a DT-F33e-vel tárgytalan (közkincs) | `adat/kulso/karoli_bible_hu_LICENC.txt` — bent (F44.0) |
| #44 | az openbible.info licencnyilatkozata szó szerint | `adat/kulso/openbible_crossrefs_LICENC.txt` — bent (F44.1) |

Nyitott kérdés: a #38 5 adaga kész; az M0 5. pontja (BDB-gyökcsoport-felmérés, az F38-kiegészítés) a 6. adag menetének elején fut (FELADATOK #38), a #38 naplójából ellenőrizendő.

**Ami a tervjegyzetet érinti**

1. **Nyílt Károli-szöveg = publikálási feltétel.** A Bible-Discovery Károli zárt; az olvasói felület (vers-lap kattintható Stronggal) csak nyílt törzsszöveggel publikálható. A Károli 1908 szövege közkincs (DT-F33e), kiadói nyilatkozat nélkül: a `karoli_bible_hu` licencellenőrzése nem előfeltétel, a #44 Károli-része tárgytalan; a `karoli_bible_hu` elvetve (DT31: a kártya az 1590-es vizsolyi kiadás, nincs `license` mező).
2. **`lxx_bridge` = a 26-os pont forrása.** A „LXX-híd mint lelet ★" a #43 kimenetére épül (héber → görög Strong, előfordulás-számmal).
3. **bdb\_roots / OpenScriptures LexicalIndex = a 6-os pont forrása.** Ha az M0-felmérés többletet mutat a TWOT-hoz képest, a szó-lap „rokon szavak" blokkja onnan tölthető.
4. **bible-mcp döntés összehangolása.** Az F44 5.(d) a connector-használatot döntési javaslatként tartalmazza; a 11. szakasz halasztást javasol a saját MCP utánra. A (d)-nél: „elvetés egyelőre, saját MCP után újra".
5. **TVTMS** már a KK-ban (F01 G2) — a NuBerea nem kell, lezárt.

## 16. Függések a FELADATOK.md szerint (2026-10-03)

A lexikonoldal-blokkok táblára illesztése és a motívum-séma nem ennek a tervnek a része: a FELADATOK.md már kiosztott feladatai, saját függésekkel.

```
#23 MOTIVUM_FORRAS (szintjelölés a SEMA-ban)  M0 és M1 kész, DT84 🟡 · függ #32 (kész), #78 (kész)
   └─ #11 MIGRACIO (egy forrásból renderelés)   függ #9, #23, #52* · a #12a (#64) kész
         └─ #25b (a #25 motívumos fele; statikus HTML, Netlify, mélységi szintek)  függ #11, #12, #23
#25a = #76 OLVASOI_KONKORDANCIA (= 1–6, 13–16, 18–20. pont, motívum nélkül)  függ #44 (kész), #79 SQLITE_EPIT (← #62) — DT-M1; a #25 kettéválasztása megtörtént
#9 SZOTAR S2 (adat a 8 lexikonoldalon)  függ #5, #6 (kész), #23, #78 (kész), #52*, #80*
   └─ #10 LEXIKON_LEZARAS  függ #8 (kész), #9, #11, #52*
#36 LEXIKON_UJRAGEN  függ #9*, #28, #34, #35 (kész), #38*, #52*, #80* (a #42 kész)
```

*(A függések a 2026-10-09-i FELADATOK szerint frissítve, #52 3. futás.)*

**Következmények a tervjegyzetre**

1. **A #25 már létezik.** A 2., 3. és 8. szakasz (olvasói kimenet, serverless, cPanel) nem új feladat, hanem a `F25_OLVASOI_HTML_BRIEF.md` bemenete. A #25 ma „statikus HTML Netlify-on"; a DT-M1 (🟢, 2026-10-06) szerint kettéválik: a konkordancia (#25a) hosting-döntése a #25a briefje előtt dől el (⛔ hosting), a motívumos nézeté (#25b) a #11 első lépcsője után. A doc ehhez kötődik, nem mellé.
2. **A séma-illesztés két részre válik.**

| mikor | mi | pontok |
| --- | --- | --- |
| most, #23-tól függetlenül | adatréteg: Strong, Károli–Strong, TSK, lexikon-TSV-k importja SQLite-ba a meglévő `adat/SEMA.md` szerint; az MCP olvasó eszközei és a #38 build-blokkja ezen áll | 1–6, 13–16, 18–20, 23 |
| #23 után | motívum, előfordulás, PaRDeS-szint, napló-tábla — a szintjelölés a SEMA-ban ott születik, előre nem írunk rá sémát | 7–12, 21–22, 24–26 |

3. **A lexikonoldal = szó-lap** elv marad, de a leképezést a #9/#10 végzi; itt csak annyi rögzül, hogy a #38 szócikkei és a szó-lap ugyanabból a táblából töltenek.

**Állapotfrissítés a FELADATOK.md-ből (2026-10-09):** a Károli–Strong (#22) kész: 1–5Mózes és Józsué (3Móz–Józs csak Sonnet, DT-F22c), a Zsoltárok (PR #239), Ézsaiás és Jeremiás (API-n, Batch, `high`, DT73; PR #249), 1–2Krónika (PR #253, #255), Ezsdrás és Ezékiel (PR #259); ⛔ megállt: a hátralévő Jób (előfeltételei teljesültek, #83, #84) és Péld (DT57); a #38 ▶ fut: 6 adag kész, a 7. adag (86%) indulhat, a 8. adagtól a DT56 küszöbe dönt (a #56 adatblokkjával, DT-F38i 🟢). Az 1. és a 13. szakasz ennek megfelelően értendő.

## 17. Ütközések és pontosítások: DONTESEK.md, CLAUDE.md, MUNKAMENET.md (2026-10-03)

**17.1 DONTESEK.md**

| tétel | mit mond | hatás a tervre |
| --- | --- | --- |
| DT-F33a, DT-F33f, DT-F24 | A STEPBible-fájlok fejlécének „Please do not redistribute it yourself" mondata (TAHOT, TAGNT, TBESH, TBESG, TVTMS) a DT-F33f szerint kérés, nem jognyilatkozat; a hatályos licenc az upstream README: CC BY 4.0, a TBESH „Meaning” oszlopával együtt; jogi súlya jogász elé a kereskedelmi döntéskor | **A 2. szakasz 1. útja (böngészőben futó SQLite) nem esik ki**: a STEPBible-származék CC BY 4.0 alatt, attribúcióval terjeszthető, tehát nem ő zárja ki a letölthető `pardes.db`-t; az adatbázis terjeszthetőségét a benne lévő források módja dönti el (DT-F33j: kereskedelmi módban csak a `kereskedelmi=igen` források); a nyers fájlok a repóban maradnak (DT-F33a). A hosting-utat a kereskedelmi/nem kereskedelmi mód (DT-F33j) és az offline-igény dönti el; a cPanel „adat a webgyökér fölött” érve opció, nem feltétel. |
| DT-F24, DT-F33c–j | 46 sor a `licencek.tsv`-ben (2026-10-06): 26 `tisztazott`, 8 `kozkincs`, 12 `tisztazatlan` (köztük KJV\_ASV\_Strongs, Karoli\_Strong\_kivonat, LXX\_kivonat, KJV\_Strongs\_teljes (a Strong-címkék, DT-F42d), Heber\_ETCBC\_modulok, LXX\_lexicon, projekt\_adat); `kereskedelmi`: 33 `igen`, 2 `nem` (MCGED, Heber\_ETCBC\_modulok), 1 `feltetelesen` (tW\_szocikkek), 10 `tisztazatlan` *(scope=adat/licencek.tsv, 46 adatsor \| forras=az `allapot` és a `kereskedelmi` oszlop számlálása `split('\t')`-bal, F52 2. futás (`naplok/F52_TERV_SZINKRON_naplo.md` 2.4) \| ts=2026-10-06)* | A 26 pont nem mind publikálható kereskedelmi módban. Minden táblához `licenc_allapot` és `kereskedelmi` a `licencek.tsv`-ből (ahogy a #42 a generátorra előírja); az olvasói lekérdező a módnak megfelelő oszlopra szűr (DT-F33j, N-F33b). A kutatói MCP-t nem korlátozza. |
| DT7 (a) | Az UBS-mezők (SDBH, lexdomain, Louw-Nida) licenc miatt kimaradtak | A Macula UBS-mezői kizárva; a külön importált Louw–Nida és SDBH (CC BY-SA 4.0) a szerepmátrix 4., 5., 9. szerepében adatosítva marad — a ShareAlike terjesztési feltétel a licenc-szűrőben (l. 18.5). |
| DT23 | „Biztos" = két független forrás; független csak a Macula szó-szintű illesztése és az `LXX_OS` | A 26-os pont (LXX-híd mint lelet) a #43 kimenetére épül; a #43 (a) szerint a bridge nem független forrás — a ★ a bridge-ből tájékoztató réteg, a bizonyosság a DT23 szerint. |
| D46 | A teljes szótár gépi fordítása halasztva, amíg nincs böngésző felhasználó (#25 vagy kereskedelmi kiadás) | A szó-lap (13. pont) a nem lexikoni Strongoknál angol szócikket mutat; az olvasói felület terve maga a D46 feloldó feltétele. |
| D50 | A lexikonba csak a motívumhoz illeszkedő jelentéstartomány kerül | A 13. pont ezzel egyezik; a szó-lap teljes szócikke más nézet (szótár ≠ lexikon) — a kettő megkülönböztetendő. |
| DT-F22a | A párosításnak bizonyossági jelölése van (`magas`); 1Móz `kezi` 0 | Az 1.1 ellenőrzés csak `magas` linkre számítson egyezést; `alacsony` link eltérésénél nem a tanulmány a gyanús. |
| DT-F33b | Van `eszkozok/lekerdez.py` (`cmd_lxx_hid`), `lxx_osszevetes.py` | Az MCP ezekre ül rá (l. 17.2). |
| DT-F38e/i, DT-F22c | Sonnet-út, DT-F38i 🟢 (a 6. adag a #56-tal); 3Móztól csak Sonnet | egyezik a 16. szakasszal |

**17.2 CLAUDE.md és MUNKAMENET.md**

A legnagyobb korrekció: **a kutatói lekérdező már létezik.** A hét lépéses protokoll determinisztikus lépései CLI-parancsok — `eszkozok/lekerdez.py` (`gerinc`, `scan`, `kollokacio`, `igealak`, `lxx-hid`, `tsk`, `karoli`), `jelolt.py`, `gate.py`, `kuszob.py`, `ellenoriz.py`, `emeles.py`; a `lexikai-scan` subagent (haiku) kizárólag ezeket futtatja. Ezért a 9. szakasz MCP-eszközlistája a `lekerdez.py` parancsainak csomagolása, nem új SQL; a `sqlite_epit.py` a kutatói oldalon nem előfeltétel (a `lekerdez.py` TSV-t olvas), csak ott kell, ahol a sebesség vagy a nagy fájl indokolja, és az olvasói felületnek.

| forrás | szabály | hatás a tervre |
| --- | --- | --- |
| CLAUDE.md fő szabály | „a kereszthivatkozás adat, a tanulmány és a lexikon pedig ennek az adatnak a nézete" | Az olvasói felület a harmadik nézet ugyanarra az adatra — a terv elve ugyanez. |
| Három szabály, 1. | Proveniencia minden lekérdezés mellé (`scope=… \| forras=… \| ts=…`); minden futás sora az `adat/auditok.tsv`-be, 0 találatnál is (MUNKAMENET A5, B2, B4) | Az MCP-eszköz kimenete proveniencia-sort hordoz; az `auditok.tsv`-be írás nem opcionális író eszköz, hanem minden kutatói hívás kötelező mellékhatása. A 14. szakasz „első kör csak olvasó" = olvasó + auditsor. |
| Három szabály, 2. | Nincs közvetlen út: keresési találat → `jeloltek.tsv` döntéssel, soha nem study-sor | A 14. szakasz „motívum-jelölt felvétele" csak a `jeloltek.tsv`-be írhat, a `motivumok`/`elofordulasok` táblába nem. |
| Rétegek | `adat/*.tsv` kanonikus; a kimenet generált, kézzel nem szerkeszthető | A `pardes.db` kimenet-réteg; a vers-lap/szó-lap renderelés a `general.py --cel` új céljai (a #25-ben), nem külön rendszer. |
| Adat-tár | `TAHOT_kivonat.tsv`: fejezet-szinten teljes (a Jób 41 pótolva, F84, DT86; maradó korlát: a Jób 40 kulcsai MT-számozásúak, CLAUDE.md „Adat-tár”); három dataset STEPBible-igehelyalakot (`Gen.1.1`) használ, `Konyv_normalizalo_tabla.tsv` konvertál; nyers adat soha a fő szál kontextusába | Az építő script igehely-normalizálása kötelező; az MCP-eszközök csak kivonatot adnak (`minta=3`) — a 12. szakasz promptjai így vannak. |
| Shell, TSV | héber/görög/magyar kód csak fájlból; `csv` modul tilos, `split('\t')` | két sor az építő és a szerver briefjébe |
| MUNKAMENET C0, D48; CI E19 | Opus-emelés a lexikon Strongjaira | A szó-lap „szócikk magyarul" blokkja a `forditasok.tsv` `opus`/`kezi` sorából tölt; a többi angol (D46). |
| Git | egy session = egy feladat, `/befogad`, `F<nn>_<NEV>_BRIEF.md`, commit UTF-8 fájlból | az MCP- és építő-brief formája |

Elavultság a CLAUDE.md-ben: „KJV/ASV\_Strongs csak Genezis, Exodus, Példabeszédek" — az F19 óta a KJV teljes (349 308 sor); a brief ne erre építsen. *(Javítva a #52 2. futásában, DT-M8 (c); a #48 a régi fájlok kivezetésekor a végleges állapotra igazítja.)*

## 18. NYITOTT\_FELADATOK.md, ATALAKITASI\_TERV.md, SEMA.md, playbook, F23/F25 (2026-10-03)

**18.1 A terv már részben megvan a repóban**

| hol | mit mond | hatás |
| --- | --- | --- |
| ATALAKITASI\_TERV 11.7 „Saját MCP-szerver" | a `lekerdez.py` MCP-burokként a chatből is elérhető; a proveniencia protokollszinten kikényszeríthető (`scope`, `forras`, `n`, `ts` mindig a strukturált válaszban); **hat-nyolc eszköznél többre ne bomoljon**, mert az eszközdefiníciók minden menetben kontextust fogyasztanak; sorrend: előbb `lekerdez.py`, az MCP vékony burok, csak ha a chatből is kell | A 9. és 17.2 szakasz ezzel egyezik — a tervjegyzet a 11.7 kibontása. A 9. szakasz eszközlistája **legfeljebb 8 eszköz**: a `lekerdez.py` alparancsai egy `lekerdez(parancs, …)` eszközben, külön csak a vers-lap, lelet-lap, Károli-szóalak, ellenőrzés. |
| ATALAKITASI\_TERV 11.5 | a lexikon publikálási formája: generált statikus oldal az `adat/` táblákból — „a legerősebb adatminőségi próba" (rossz kapcsolat = rossz link, azonnal látszik) | Az olvasói felület (2., 8. szakasz, #25) nem csak termék, hanem adatminőségi próba; a 11.5 ezt már kimondta. |
| ATALAKITASI\_TERV 4.7 | „A Károli 31 ezer versének teljes strongozása nem cél" — a join tanulmányvezérelt melléktermék | **Elavult**: a #22 (F22) könyvenként teljes strongozást végez, kész: 1–5Móz, Józs, Zsolt, Ézs, Jer, 1–2Krón, Ezsd, Ez. A 4.7 elve (a `karoli_szo` a `jeloltek.tsv` minősítési sorában) marad; a teljes Károli–Strong új réteg mellette. Az ATALAKITASI\_TERV-ben jelölve (DT-M8 (b), #52 2. futás). |
| ATALAKITASI\_TERV 12 | a szerzői jogi kérdés nincs megoldva; publikálásnál szakjogász | egyezik a 17.1 nyitott tételével |
| playbook 1. | „Claude Code nem látja a claude.ai memóriát, csak a repó fájljait" | **Ez a tervjegyzet csak akkor hat, ha a repóban van**: Markdown-exportja a repó gyökerébe (pl. `ADATVAGYON_TERV.md`), és a #25/#23 brief `olvas:` listájába. |
| playbook 2. licenc-tábla | Biblia-Felfedező (Zsidó Miklós) felfüggesztve/elutasítva; GPL 3.0 nem építhető be | A Bible-Discovery Károli kizárása (11., 17.1) ezzel egyezik — a repó régóta tudja. |
| playbook 3. | kis minta (3–10 tétel) jóváhagyás előtt | az építő script és az MCP briefje: minta-futás a 8 lexikonoldalas motívumon, csak utána teljes |

**18.2 F23 (MOTIVUM\_FORRAS) és F25 (OLVASOI\_HTML)**

- **D34, „B" út:** motívumonként egyetlen kézi forrás (`motivumok/[ID].md` + adattáblák); a tematikus tanulmány, a lexikonoldal és minden olvasói nézet ebből generálódik **állítható mélységgel: `olvasoi` / `apparatus` / `belso`**; a törzscikk megszűnik. A `belso` szint buildkor kimarad, nem rejtjük el (F25 D36/D40).
- Hatás a három lap-típusra: a vers-lap, szó-lap, motívum-lap az F23 értelmében *olvasói nézet*, és minden blokkja szintet kap. A lelet-lap (12-es) ★ és ◆ sorai `apparatus`; a „nyitott / még nem vizsgált" munkalista és a napló-indoklás nyers szövege `belso` — **a publikus buildből kimarad**. A 14. szakasz belső munkalapja tehát csak Code-ban él.
- F25 kiindulása a 2026.09.27-i három HTML-minta (G1941 olvasói nézet, H7121 BDB-nézet, szigorú hű / természetes hű) és a `motivumlog/kereszthivatkozas_pilot/` HTML-pilotjai — ezek a szó-lap első vázlatai; a modul-export (MyBible/e-Sword) későbbi opció.
- A #23 `nem_fugg: [22]` — a motívum-séma nem vár a Károli–Strongra; a 16. szakasz kétrészes illesztése ezzel egyezik.

**18.3 SEMA.md — ami már létezik**

| SEMA | tábla | hatás |
| --- | --- | --- |
| 1.1 `IGEHELY`, 1.2 `STRONG`, 1.5 `PROVENIENCIA` | közös típusok | az építő script típusai innen, nem újak |
| 2.9 `auditok.tsv` | lekérdezés-napló | az MCP kötelező mellékhatása (17.2) |
| 2.14 `forditasok.tsv` | fordítási gyorsítótár (`opus`/`sonnet`/`kezi`) | a szó-lap „szócikk magyarul" forrása |
| 2.15 `terminologia.tsv` | **már létezik** (F05 S2, D26) | a 13. szakasz nem új fájlt javasol, hanem ezt bővíti; a `terminologia_rogzit` ide ír |
| 2.19 `licencek.tsv` | licenc-leltár | a nyilvános nézet szűrője (17.1) |
| 2.20 `adat/karoli_strong/parok_<könyv>.tsv`, `szavak_<könyv>.tsv` | Károli–Strong könyvenként | a 18–20. pont és a 12.1 lekérés forrása |

**18.4 NYITOTT\_FELADATOK — ami a tervet érinti**

| tétel | mit mond | hatás |
| --- | --- | --- |
| 1. (biblemate `morphology.sqlite`) | a `ClauseID` tagmondat-szintű csoportosítást ad, pontosabb a formula-motívumoknál, mint a szórend-heurisztika (Deut 32:3 kizárásánál már segített) | az 5. pont (frázis-keresés) jelöltje; licenc ellenőrizendő a playbook 2. szerint |
| N37 | nincs egységes Strong-normalizáló függvény (`1d`); N21: nullázatlan `H922` | az építő script normalizálása **ez a függvény**, nem újabb ad hoc; a 3. és 17.2 szakasz normalizálási igénye ide fut; megoldja a #62 STRONG\_NORMALIZAL |
| N17, N46, N-F41a, N-F41d | versszámozás: a KK `igehely_kjv` nem megbízható; a `TAHOT_kivonat` számozása vegyes (KJV/MT); 44 KK-vers eltolódás-gyanús | **a vers-lap igehely-kulcsa Károli-számozás, és minden más forrást (TAHOT, BSB, LXX\_OS, TSK) a KK-n át kell kötni; `szamozas` jelző a vers-táblában; ahol a KK üres vagy gyanús, a vers-lap ezt mutatja, nem interpolál** — ez a séma legnagyobb kockázata |
| N-F34b | a „TAHOT\_kivonat nem teljes" állítás elavult, a hiány kicsi — lezárva (F84, 2026-10-09: a Jób 41 pótolva) | a 17.2 Adat-tár sora ennek megfelelően értendő |
| N13 | `jelolt.py` túltermel gyakori Strongokon (H1121, H0430, H2416) | a 23. pont (ritka együttállás) gyakorisági küszöböt kap; a ★ lelet-lapon a gyakori Strongok zajt adnának |
| N32, N33 | a commitolt lexikonoldalak elavultak; a CI nem futtatja a `general.py`-t | a szó-lap/vers-lap generátor is CI-futást igényel, különben ugyanez ismétlődik |
| N26 | a shell-szabály gépi kényszerítése (hook) | az MCP-szerver mint hook-pont: ha az eszköz fut, nincs inline bash |

**18.5 Szótári szerepmátrix = a szó-lap sémája**

Az `adat/szotar_szerepek.tsv` (SEMA 2.13) 13 szerep × 2 nyelv (26 sor; az 1–10. és a 12. a lenti táblában, a 13–14. `javaslat` állapotú, DT-M4, DT76 (9)) statikus táblája megmondja, melyik szótári forrás felel egy kérdéstípusra, és adatosítva van-e. A szó-lap (4–5. szakasz, 13–15. pont) nem új szerkezet, hanem ennek a mátrixnak a renderelése egy Strong-számra; a blokkok sorrendje és töltöttsége innen jön, nem a tervjegyzetből.

| # | szerep | görög | héber | állapot |
| --- | --- | --- | --- | --- |
| 1 | Alapjelentés | TBESG | TBESH | adatosítva |
| 2 | Mélységi szócikk | Thayer | BDB | adatosítva |
| 3 | Teológiai szócikk | nincs (Cremer kivezetve, D16) | Girdlestone elvetve; TWOT-szám hivatkozásként | nincs |
| 4 | Jelentésszerkezet, szemantikai mező | UBS DNTG (Louw–Nida) | SDBH | adatosítva |
| 5 | Tömör jelentés, előfordulás | UBS glossza + Mounce | UBS DBH glossza | görög igen, héber nem |
| 6 | LXX-híd | az ÚSZ-szó LXX-háttere (`lekerdez.py lxx-hid`) | versenkénti LXX-döntés (`lxx_dontesek.tsv`) | adatosítva |
| 7 | Megfelelők a másik nyelven | SECE | SECE | nincs adatosítva |
| 8 | Nyelvi háttér | LSJ | BDB-etimológia | görög igen |
| 9 | Versenkénti jelentés | UBS + KJV szószintű híd | UBS + BSB + KJV híd | görög igen, héber nem |
| 10 | Kiejtés (magyaros) | szabálytábla | OSHL-jelöltek, kézi | nincs adatosítva |
| 12 | Tematikus index | Nave | Nave | javaslat |

**Igazítás a tervjegyzetben**

- A 4. szakasz lexikon-rétege és a 13–15. pont a mátrix szerepeire képeződik: 13 → 1–2 (+3, ha lesz), 14 → 6, 15 → 10; a „jelentésszerkezet" (4) és a „versenkénti jelentés" (9) a szó-lapon külön blokk, amit a 4. szakasz eddig nem nevezett meg.
- Az `allapot` oszlop a szó-lap töltöttségének forrása: `adatosítva` → blokk; `nincs forrás` → a blokk nincs; a „memória vs. lekérdezés" szabály a renderben: az üres blokk gépi jelölője `<!-- ÜRES-BLOKK: szerep | állapot -->` + látható zárójeles sor (DT80, B változat), és csak a `nincs adatosítva` / `javaslat` állapotú szerepnél jelenik meg; az `adatosítva` szerepnél hivatkozás kell (S4), nem üres blokk (DT80); az 5., 6. és 7. szerep hivatkozás a 2/b-re és a 3. szakaszra (DT81 (1)), a 7. szerep (SECE) „l. 2/b” (DT82 (c)); az `adatosítva` szerep, amelyhez a `lexikon_hivatkozasok.tsv`-ben nincs bekötött sor, harmadik állapota „adatosítva, nincs bekötve”, mutatóval a #9-re (DT82 (a)); a héber 1. szerepnél (TBESH marad a forrás, `adatosítva`) a H7121 jelölt üres blokk, mutatója a BDB 2.c (DT-F42a), a H8034 „adatosítva, nincs bekötve”, mutatója a #9 (DT83); token nélküli nyelvnél egy mondat marad és a gépi jelölő `<!-- ÜRES-NYELV: <nyelv> | nincs Strong-token -->` (DT82 (b)); a TWOT-, domén- és kiejtés-sor a saját szerepe alá költözik (3., 4., 10.; DT81).
- **A 17.1 DT7-sora pontosítva:** a DT7 a *Macula* UBS-mezőit zárta ki licenc miatt; a külön importált Louw–Nida (UBS DNTG) és SDBH a mátrix 4., 5. és 9. szerepében adatosítva van, CC BY-SA 4.0 alatt. A CC BY-SA ShareAlike-feltétele terjesztési kérdés: az olvasói nézet ezeket a blokkokat csak azonos licencű kiadásban adhatja — a 17.1 licenc-szűrője ezt is kezeli. A 4. szakasz címsorából az UBS kizárása visszavonva.

**Javaslat: 13. szerep — Károli-megfelelők** *(DT-M4 🟢 2026-10-08: felvétel `javaslat` állapottal; a szerepmátrix-váz #78 ✅ felvette a `szotar_szerepek.tsv`-be, F78.3)*

A Károli–Strong (#22) olyan szerepet hoz, ami a mátrixban nincs: a Strong-szám Károli-szóalakjai gyakorisággal és példaversekkel (a 12.1 lekérés 1–2. pontja), mindkét nyelven, forrás `adat/karoli_strong/szavak_<könyv>.tsv`, állapot `javaslat`, amíg a #22 nem teljes. Ugyanide, külön mezőként: a SZPA konkordáns alternatíva (10. szakasz, B üzemmód), `[SZPA-B/V/F]` jelöléssel. A sor felvéve a SEMA 2.13-ba és a `szotar_szerepek.tsv`-be (`javaslat`, DT-M4, F78.3); az `adatosítva` állapotra váltás a #22 lezárásakor vagy a BDB-adatblokk pótlásakor (#80).

**Javaslat: 14. szerep — Károli-rejtett és hamis párhuzam (18–19. pont)**

A 13. szerepből származtatva: ugyanaz a Strong más magyar szóval, és ugyanaz a magyar szó más Strong mögött — a szó-lap ⚠-blokkja. Nem új forrás, hanem a 13. szerep két lekérdezése; a mátrixban azért külön sor, mert a render külön blokként mutatja.

## 19. Mi hiányzik még, és döntésnapló

A napló gépi alakja a `jeloltek.tsv` (SEMA 2.4) — a tényleges munka a 8 retroaktív motívum sorainak feltöltése és a származtatott „még nem vizsgált" státusz (l. 22.1); a többi meglévő táblákból megy.

| pont | hiányzó adat |
| --- | --- |
| 12, 24, 25, 11 státusz | naplók adatosítása — egy tábla: `motívum · vers · forrás (lexikai/TSK/mindkettő) · döntés · PaRDeS-szint · indoklás · dátum`; a Markdown-naplók (`naplok/[motívum]_kereszthivatkozas_naplo.md`) döntései táblába emelve, build-lépésként |
| 18, 19, 5 magyar fele | Károli–Strong (⛔ megállt; kész: 1–5Móz, Józs, Zsolt, Ézs, Jer, 1–2Krón, Ezsd, Ez; hátra a Jób és a Péld) |
| 20 | mindkét Károli-változat strongozva |
| 26 | LXX-híd + TSK összevetés (adat megvan, lekérdezés új) |
| 21, 22, 23, a többi | semmi — meglévő táblák |

**Kivetkező lépések**

- [ ] Code-brief az 1.1 ellenőrzésre (bemenet: grep a Genezis-igehelyes tematikus táblákra; kimenet: eltéréslista) — a brief megvan: #65 KAROLI\_ELLENORZES (nem_indult)
- [ ] 1.2 variancia-térkép ugyanabban a futásban
- [ ] napló-adatosítás brief (a 12/24/25/11 alapja) — a 8 retroaktív motívumra: #63 JELOLTEK\_RETRO (nem_indult)
- [ ] `eszkozok/sqlite_epit.py` séma a 26 pontból — brief kell: #79 SQLITE\_EPIT (csonk, DT77 (12))
- [ ] tárhely-döntés (cPanel PHP vagy Python / Netlify) a mért `pardes.db` méret után — ⛔ a #76 briefje előtt (hosting)

* [ ] MCP-szerver Code-ban (FastMCP, a `sqlite_epit.py` után; a 12. szakasz eszköznevei) — feltételes (DT-M7); előbb a #61 LEKERDEZ\_NAPLO
* [ ] SZPA-audit (C üzemmód) a tanulmányok prózáján és a BDB-fordításon — **feltételes** (DT77 (13)): előbb a `SZPA_FORDITOI_PROFIL_prompt.md` a repóba, a befogadás a 6. lépcsőben
* [x] openbible.info felvétele a `datasetek.tsv`-be, F44 licencellenőrzés — kész (#44 ✅, PR #205): 4 sor `hianyzik` + „JELÖLT, NEM IMPORTÁLT” (DT33); az import külön feladat (DT34)
* [ ] BDB javító menet a teljes Károli–Strong után (Károli-oszlop minden szócikkhez) — brief kell: #80 BDB\_KAROLI\_POTLAS (csonk) (adatblokk-pótlás újrafordítás nélkül, DT77 (15))
* [x] a három kézi 0. lépés (#43 lxx\_bridge.tsv + LICENC.md; #44 karoli\_bible\_hu\_LICENC.txt, openbible\_crossrefs\_LICENC.txt) — bent (F43.0, F44.0, F44.1); a #43 és a #44 kész
* [x] ellenőrizni a #38 naplójában, hogy az M0 5. pont (BDB-gyökcsoport-felmérés) lefutott-e — lefutott (`naplok/BDB_FORDITAS_gyokcsoportok.tsv`, DT52 (c), N53) — a 6. adag menetének elején fut
* [x] terminologia.tsv a #38 további adagjainak (adagok közötti következetesség, MCP nélkül is) — a #38 briefjének `olvas:` listájában bent (`adat/terminologia.tsv`)
* [x] a nyílt Károli 1908 licencének tisztázása (#44) — tárgytalan: a szöveg közkincs (DT-F33e), nem előfeltétel
* [x] a tervjegyzet Markdown-exportja a repó gyökerébe (ADATVAGYON\_TERV.md) — bent (`ab73f7b`, 2026-10-04)
* [x] az ADATVAGYON\_TERV.md a #25/#23 brief olvas: listájába — bent (DT-M8 (a)); a #11 csonk `olvas:` sorában is bent (DT-M8 (d))
* [x] ATALAKITASI\_TERV 4.7 jelölése elavultként (a #22 teljes strongozást végez) — kész (#52 2. futás, DT-M8 (b))
* [ ] a vers-tábla igehely-kulcsa és a szamozas jelző: KK-alapú kötés minden forráshoz (N17, N46, N-F41a/d) — brief kell: #79 SQLITE\_EPIT (a briefjében)

**Döntésnapló**

| dátum | döntés / változás | státusz |
| --- | --- | --- |
| 2026-10-02 | A Károli–Strong 1Mózes-részének négy hasznosítása (1.1–1.4), javasolt sorrend 1.1 → 1.2 | javaslat |
| 2026-10-02 | Olvasói keresés: az adatvagyon egy SQLite-fájlban, felülettől függetlenül; a felület (statikus / serverless / cPanel / app) a védelem és offline-igény függvénye | javaslat |
| 2026-10-02 | 26 pontos keresési követelménylista; kiemelt a 12-es (lelet-lap) és a 17-es (vers-lap); új metszetek 18–26 | tervezet |
| 2026-10-02 | SQLite elegendő mind a 26 pontra; az 5. és 23. építéskor előszámolva | megállapítás |
| 2026-10-02 | Hosting: ha van cPanel-tárhely, minden oda; a lekérdező PHP vagy Python a tárhely szerint | nyitott — tárhely nem választott |
| 2026-10-02 | Számértékek (MB, mp, hívás/hó, token-szám) becslések, nem mért adatok | megjegyzés |
| 2026-10-02 | v2: 9–12. szakasz hozzáadva (MCP és AI-réteg, SZPA-profil, külső MCP-k és openbible.info, két adatlekérő prompt); a záró szakasz 13-ra számozva | kiegészítés |
| 2026-10-02 | MCP-szerver: olvasó eszközök, Code-ban indul, hostolás csak ha a chat-használat hiányzik; külső bible-mcp bekötése a saját MCP utánra halasztva | javaslat |
| 2026-10-02 | SZPA-profil: jelölt alternatíva-réteg, nem alapértelmezett megfelelő; \[B\] csak második mintával igazolva | javaslat |
| 2026-10-02 | openbible.info kereszthivatkozás forrásjelölt; a kapcsolatok forrás oszlopa harmadik értéket kap (közösségi) | tervezet |
| 2026-10-02 | BDB-fordítás (#38) nem áll meg az adatlekérésért; javító menet a teljes Károli–Strong után | javaslat |
| 2026-10-03 | v3: 13–15. szakasz hozzáadva (MCP a #38-nál, visszaírás szabályai, a HF-forrásáttekintés hozama); a záró szakasz 16-ra számozva | kiegészítés |
| 2026-10-03 | Visszaírás: a forrás-TSV-be hozzáfűzéssel, proveniencia-oszloppal, csak Code-ban; az SQLite nem írható; első író eszköz a terminologia\_rogzit | javaslat |
| 2026-10-03 | A nyílt Károli 1908 (karoli\_bible\_hu) licencellenőrzése az olvasói felület publikálási előfeltétele; a Bible-Discovery Károli kizárva | megállapítás — lezárva (v15): a Károli 1908 közkincs (DT-F33e), a `karoli_bible_hu` elvetve (DT31); a Bible-Discovery Károli kizárása marad |
| 2026-10-03 | bible-mcp: az F44 5.(d) döntésnél elvetés egyelőre, saját MCP után újra | javaslat |
| 2026-10-03 | A #38-nál a 12.1 lekérések build-lépésként (előre számolt blokk az adagfájlban), nem MCP-hívásként; tokenköltség-becslés a 13. szakaszban | javaslat |
| 2026-10-03 | v4: 16. szakasz (függések a FELADATOK.md szerint); a 2–3–8. szakasz a #25 OLVASOI\_HTML bemenete; a séma-illesztés kettéválik (adatréteg most, motívum/napló a #23 után); állapotfrissítés: Károli–Strong 1–5Móz kész, #38 ⛔ DT-F38i | kiegészítés |
| 2026-10-03 | v5: 17. szakasz (ütközések a DONTESEK/CLAUDE/MUNKAMENET-tel); a 2. szakasz 1. útja (böngészőben futó SQLite) a DT-F33a miatt kizárva; az UBS a 4. szakaszból törölve; a 9. szakasz MCP-eszközei a lekerdez.py-ra ülnek, nem új SQL; az auditok.tsv-sor minden kutatói hívás kötelező mellékhatása | kiegészítés |
| 2026-10-03 | Az olvasói felület adatvédelme a DT-F33a terjesztési kérdésén áll; a #25 briefje előtt tisztázandó (jogász a kereskedelmi döntéskor) | lezárva (v14): a DT-F33f/j szerint a terjesztés nem akadály, a kereskedelmi/nem kereskedelmi mód dönt; jogász a kereskedelmi döntéskor |
| 2026-10-03 | v6: 18. szakasz (NYITOTT\_FELADATOK, ATALAKITASI\_TERV 11.5/11.7/4.7, SEMA, playbook, F23/F25). Az MCP legfeljebb 8 eszköz (11.7); a három lap-típus az F23 mélységi szintjeit kapja, a belső munkalista buildből kimarad; a terminologia.tsv már létezik (SEMA 2.15); a vers-lap kulcsa KK-alapú | kiegészítés |
| 2026-10-03 | v7: 0. szakasz — nyolc pontos összegzés a repó-fájlokkal való összevetés eredményéről | kiegészítés |
| 2026-10-03 | v8: 0.1 keret (három cél, egy adat) és 0.2 az adatvagyon az 1. fázis végén — kilenc réteg, saját tulajdon és terjeszthetőség; javaslat: olvasói konkordancia motívum nélkül a #25 előtt; a Károli–Strong kimenet terjesztési státusza jogászi kérdés | javaslat |
| 2026-10-03 | v9: 18.5 szótári szerepmátrix = a szó-lap sémája; a 4. szakasz és a 17.1 DT7-sora igazítva (Macula UBS-mezők kizárva, a külön Louw–Nida/SDBH CC BY-SA adatosítva marad); javaslat a 13. (Károli-megfelelők + SZPA) és 14. (rejtett/hamis párhuzam) szerepre a SEMA 2.13-ban | javaslat — DT-tétel a SEMA 2.13 bővítésére |
| 2026-10-03 | v10: 20. szakasz — rendszer-séma ábra (források → adat → eszközök → nézetek; a Károli–Strong, a motívum-réteg és az olvasói felület kiemelve) | kiegészítés |
| 2026-10-03 | v11: 20. ábra igazítva (szótár-réteg, tanulmány, lexikonoldal is saját; a Nézetek sáv az F23 B út szerint); 21. szakasz — elkészítési workflow hat lépcsőben; a 4. lépcső (olvasói konkordancia motívum nélkül) nem vár az 5.-re — DT-tétel a FELADATOK sorrendjére | javaslat |
| 2026-10-03 | v12: 22. szakasz — a SEMA.md teljes figyelembevétele. Három korrekció: a napló gépi alakja a jeloltek.tsv (nem új tábla; a hiány a 8 retroaktív motívum és a származtatott „még nem vizsgált”); a forrás-tengely a jeloltek.forras_kereses, nem a kapcsolatok (két tengely már ütközik); a szamozas értékkészlet a BSB 7. oszlopáé. 26 pont → tábla illesztés; az 1.7 AZONOSITAS_MODJA elavult a #22 miatt; auditok.lepes új MCP-érték kell; az integritási szabályok az építő tesztjei | kiegészítés — két DT-tétel (1.7 szövege; auditok.lepes) |
| 2026-10-04 | v13: „Kiindulási állapot és mi változott a repóban” szakasz a doc elején (merge 117bafc): DT-F33e–j licenc-fordulat (az 1. út nem esik ki; kereskedelmi/nem kereskedelmi szűrő), D34–D41 és DT-F26a (motívumcikk), #32 KONTEXTUS (DT-F32b Opus), sorszám-ütközés (#48–#51 foglalt), státuszok (#22 ⛔, #43 ▶, #46 ✅); a 2. szakasz licenc-mondata cserélve. A doc a repóba költözik, onnantól az md a hatályos | kiegészítés — utolsó chat-oldali verzió |
| 2026-10-04 | v14 (#52 TERV\_SZINKRON, 1. futás; kiindulás: merge `8e8f771`): a DT-F33e–j a törzsben is átvezetve — 0.2 (Károli–Strong sor, 2. pont), 0.4, 15., 16., 17.1 (két sor), 19. (nyitott sor lezárva, teendőlista), 21. (0., 1., 3., 4. lépcső); státuszok: #22 ⛔, #43 ▶, #44 Károli-rész tárgytalan, #46 ✅, #32 ✅; függések a FELADATOK szerint (#9, #10, #11, #23, #36); sorszámok: a MUNKATERV tervezett feladatai kódnévvel (DT-F52a). Ellenőr 1. kör (JAVÍTANDÓ, 15 tétel) javítva F52.5-ben: DT-F43 (a), #22 Józs, `pardes.db` megfogalmazás, MCGED, 0. szakasz, proveniencia. Napló: `naplok/F52_TERV_SZINKRON_naplo.md` | szinkron |
| 2026-10-06 | v15 (#52 TERV\_SZINKRON, 2. futás; kiindulás: FELADATOK v1.3, `main` `69da794`): DT-M1 🟢 (a #25 kettéválik: #25a/#25b — 0.2, 16., 21.), DT-M2 🟢 (`szó-szintű-gépi` — 22.2), DT-M3 🟢 (`adhoc`, csatorna a proveniencia-sorban — 22.4), DT-M7 🟢 (az MCP feltételes — 0., 9., 19., 21.), DT-M8 🟢 (a TERV\_BEFOGAD külön brief nélkül: az `olvas:`-teendő és az ATALAKITASI\_TERV 4.7 jelölése kész, a CLAUDE.md KJV-sora javítva — 17.2, 18.1, 19.); státuszok: #22 (Józs PR mergelve, következő a Bírák), #42, #43, #44, #30, #51, #53, #57, #58 ✅, #38 ▶ (6. adag a #56-tal, DT-F38i 🟢); a 17.1 licenc-összesítés 46 sorra (26/8/12; DT-F42d, DT-F42g); 15. (DT31: `karoli_bible_hu` elvetve); új feladatok: #54, #55, #56, #59, #60, #61, #62, #63, #64, #65, #66. Napló: `naplok/F52_TERV_SZINKRON_naplo.md` | szinkron |
| 2026-10-08 | v16 (TERV-INTEGRÁCIÓ, DT74–g): a terv → feladat irány átvezetve (a „Kiindulási állapot” 2026-10-08-i sora): #76, #78, #79, #80, #81; SZPA-audit feltételes; DT-M4, M5, M6 🟢; a 19. teendőlista jelölve; 1.4 → #81; 18.5 → #78. Napló: `naplok/TERV_INTEGRACIO_leltar.md` | integráció |
| 2026-10-09 | v17 (#52 TERV\_SZINKRON, 3. futás; kiindulás: FELADATOK v1.3, `main` `78844919`; viszonyítási pont a 2. futás `7dd0183`; KONZISZTENCIA\_20261009 1.16): kiindulási állapot sor és „Státuszok” sor a 2026-10-09-i állapotra (#22 kész könyvei, DT57; #37, #40, #64, #66, #68, #77, #78, #82–#84 ✅; #23 M1, DT84 🟡); új sor a 2026-10-09-i változásokról (DT73, DT79–DT89); 0. (3. pont), 16. (ábra, állapotfrissítés), 17.2 (Adat-tár sor), 18.1 (ATALAKITASI 4.7 sor), 18.4 (N-F34b sor), 18.5 (13 szerep, `ÜRES-BLOKK`/„adatosítva, nincs bekötve”, a 13. szerep felvéve), 19. (Károli–Strong sor, négy teendő-jelölés), 21. (5. lépcső sorrendje; a 6. lépcső feltételes jelölése, terv → feladat 3b), 22.5 (TAHOT-sor) a mai állapotra. Napló: `naplok/F52_TERV_SZINKRON_naplo.md` 3. futás | szinkron |

## 20. Rendszer-séma

&#91;embedded content: rendszer-séma · 4 réteg, 16 egység\]

A négy sáv fentről lefelé: a források licence dönti el, mi mehet tovább; az `adat/` a kanonikus igazság (a kiemelt három — Károli–Strong, szótár-réteg (a magyar BDB/Thayer-fordítás, kiejtés, KK) és motívum-réteg — a projekt saját szellemi tulajdona); az eszközök minden lekérdezést provenienciával adnak; a nézetek generáltak, mélységi szinttel — a tanulmány, a lexikonoldal és az olvasói felület maga a kereszthivatkozási lexikon, ugyanúgy saját szellemi tulajdon, mint az adat, amiből készül; a kék keret ezt jelöli mindkét sávban. Az olvasói felület a harmadik nézet ugyanarra az adatra. Írás csak felfelé, az `adat/`-ba, DONTESEK-tétellel — a nézet soha nem szerkeszthető.

## 21. Elkészítési workflow

Hat lépcső, a 16. szakasz függései és a 0.2 sorrendje szerint (1. fázis végig → olvasói konkordancia motívum nélkül → motívum-réteg ráepítve). Minden lépcső egy vagy több brief a repó szabályai szerint (`/befogad`, egy session = egy feladat, kis minta a teljes futás előtt, `fuggetlen-ellenor`, draft PR). Az ⛔ a felhasználói megállás.

| # | lépcső | mit csinál | kimenet | függ | ki |
| --- | --- | --- | --- | --- | --- |
| 0 | kézi előfeltételek — **kész (2026-10-04)** | a három 0. lépés: `lxx_bridge.tsv` + `LICENC.md` (#43), `karoli_bible_hu_LICENC.txt` (a Károli-rész a DT-F33e-vel tárgytalan), `openbible_crossrefs_LICENC.txt` (#44); a tervjegyzet exportja `ADATVAGYON_TERV.md`-ként a repóba (`ab73f7b`) | a #43 és a #44 kész; Code látja a tervet | — | felhasználó |
| 1 | adatréteg lezárása (1. fázis) | #22 Károli–Strong könyvenként végig; #38 BDB adagok (a 6. adagtól a #56 adatblokkjával, DT-F38i 🟢; `terminologia.tsv` minden adagnak); #43, #44, #46 kész; #7 Thayer a D46 feloldásakor | teljes Károli–Strong, magyar BDB, licenc-tiszta leltár, LXX-híd ellenőrizve | 0 | Code (Sonnet), felhasználó a megállásoknál |
| 2 | ellenőrzés és variancia | 1.1 ellenőrzés (#65 KAROLI\_ELLENORZES: tanulmány-táblák vs. Károli–Strong, csak `magas` link); 1.2 variancia-térkép; N37 egységes Strong-normalizáló (#62, a lépcső elején) | eltéréslista; motívumonként Károli-szólista; `strong_normalizal()` | 1 (könyvenként, nem kell a teljes) | Code, egy brief |
| 3 | eszközök | `sqlite_epit.py` (SEMA-típusok, KK-alapú vers-kulcs, `szamozas`, `licenc_allapot` és `kereskedelmi` oszlop, `strong_parok`, frázis-pozíció); MCP-burok a `lekerdez.py`-ra, ≤ 8 eszköz, proveniencia + `auditok.tsv`-sor (feltételes, DT-M7; előbb a #61); a #38 build-blokkja (12.1) már a #56-ban, az SQLITE\_EPIT-től függetlenül | `pardes.db` (nem commit), `.mcp.json`, adatblokk-generátor | 2 | Code, egy brief (építő; az MCP feltételes) |
| 4 | olvasói konkordancia — motívum nélkül (#25a, DT-M1 🟢) | a 26-ból az 1–6, 13–16, 18–20 pont; szó-lap a szerepmátrix (18.5) szerint, vers-lap KK-kulccsal; `general.py --cel verslap / szolap`; hosting-út a mód szerint (böngészős SQLite, cPanel vagy serverless — DT-F33f/j), a `kereskedelmi` oszlop szerinti szűrővel; nyílt Károli-szöveg (közkincs, DT-F33e) | első publikus kiadás: kereshető magyar Strong-konkordancia, nem kereskedelmi módban | 3, DT-F33j (a #44 kész) | Code; felhasználó a hosting-döntésnél ⛔ |
| 5 | motívum-réteg | #78 ✅ (szerepmátrix-váz) → #23 (séma, mélységi szintek; M1 kész, DT84 🟡) → #9 (szótári adatréteg) → #11 (egy forrásból renderelés) → #10 (lexikonoldal-lezárás) → napló-adatosítás → #25b (motívum-lap, lelet-lap ★, 7–12, 21–26. pont) | a kereszthivatkozási lexikon mint harmadik nézet | 4, #37 | Code (Opus a #23-nál), felhasználó A4/B5 ⛔ |
| 6 | hasznosítás — **feltételes** (a 4–5. lépcső után, a felhasználó döntésére; feladat a döntéskor nyílik, `/befogad`; a SZPA-audit: DT77 (13)) | SZPA-audit (10.); fordítói eszköz; licencelt adatkészlet (saját rétegek CC BY); AI-réteg és kereskedelmi döntés jogásszal | a 0.2 négy iránya | 4–5 | felhasználó dönt, Code végez |

**Három szabály a lépcsőkre**

1. A 4. lépcső nem vár az 5.-re: a konkordancia motívum nélkül is kiadható, és ez a D46 feloldó feltétele. Ez eltért a FELADATOK.md addigi sorrendjétől (#25 a #11/#23 mögött); a DT-M1 🟢 (2026-10-06) eldöntötte: a #25 kettéválik.
2. Egyik lépcső sem ír az `adat/`-ba a briefen kívül; a `pardes.db` és minden nézet generált. Visszaírás csak a 14. szakasz szabályaival.
3. Minden lépcső első futása kis mintán (a 8 lexikonoldalas motívum, ill. 1Mózes), ⛔ után teljes.

```
0 kézi előfeltételek ─▶ 1 adatréteg (1. fázis) ─▶ 2 ellenőrzés, variancia ─▶ 3 eszközök
                                                                              │
                                      ┌───────────────────────────────────────┘
                                      ▼
                         4 olvasói konkordancia (motívum nélkül)  ─▶ 5 motívum-réteg  ─▶ 6 hasznosítás
```

## 22. A SEMA.md teljes figyelembevétele — pontonkénti illesztés (2026-10-03)

A teljes `adat/SEMA.md` (1. közös típusok, 2.1–2.20 táblák, 3. integritási szabályok, 4. nyitott tételek) átolvasása után öt dolog derül ki, amit a terv eddig rosszul vagy hiányosan mondott.

**22.1 Három korrekció a tervjegyzetben**

| mit mondott a terv | mit mond a SEMA | javítás |
| --- | --- | --- |
| „A naplók adatosítása az egyetlen tényleges új munka" (19., 21. szakasz) | **A napló gépi alakja már létezik: 2.4 `jeloltek.tsv`** — `forras_kereses` (`scan H7497` / `TSK 1Móz 6:4` / `Károli-KH`), `dontes` (`beépítve` \| `elutasítva` \| `nyitva`), kötelező `indoklas`, `karoli_szo` + `azonositas_modja` + `megbizhatosag` (Károli-triplet), `datum`. Az `elofordulasok` csak innen, `beépítve`-vel léptethető elő (3. szabály 2.) | A 12-es lelet-lap forrása a `jeloltek` + `elofordulasok` + `auditok`, nem új tábla. A tényleges hiány: a 8 retroaktív (F3/N14) motívum `jeloltek`-sorainak visszamenőleges feltöltése, és a „még nem vizsgált" státusz, ami nem a `dontes` értéke, hanem **származtatott**: az `auditok` szerint lefutott scan találata, amelyhez nincs `jeloltek`-sor. |
| „a `kapcsolatok` forrás oszlopa harmadik értéket kap: lexikai / TSK / közösségi" (11., 17.1) | A 2.3 `kapcsolatok.tipus` a PaRDeS-tengely (`Előkép` \| `Párhuzam` \| `Beteljesedés` \| `Kontraszt` \| `Variáns`); a pilot „Típus" (`LEXIKAI`/`NARRATÍV`/`STRUKTURÁLIS`/`TEMATIKUS`) egy másik, feloldatlan tengely (4. szakasz) | **Nem a `kapcsolatok`-ba.** A „honnan jött" tengely a `jeloltek.forras_kereses` mezője; az openbible.info forrásként ott kap új értéket (`openbible 1Móz 6:4`), a `kapcsolatok` séma érintetlen. Harmadik tengelyt a 2.3-ra tenni a 4. szakasz névütközését súlyosbítaná. |
| `szamozas` jelző a vers-táblában, új oszlop (18.4) | A 2.6 `BSB_Strongs` 7. oszlopa (`Számozás`: `mt` \| `ellenorizetlen` \| `kjv`) már ezt a fogalmat hordozza, versszintű WLC-összevetéssel, dokumentált paraméterekkel | Az építő script **ezt az értékkészletet** veszi át, nem újat vezet be; a vers-lap „szamozas" jelzője a BSB-oszlop és a KK eltolódás-gyanús 44 verse (N46) uniója. |

**22.2 Egy elavult SEMA-tétel, amit a #22 ír felül**

1.7 `AZONOSITAS_MODJA`: „a projektnek nincs szó-szintű Strong-taggelt Károlija, és nem is lesz (zárt licenc)" — a 227 join-sor mind `tartalom-alapú`. A Károli–Strong (#22, 2.20 `parok_<könyv>.tsv`) pontosan a `szó-szintű-gépi` értéket teszi elérhetővé (DT-M2 🟢, 2026-10-05: új érték, hogy a modell-kimenet jelölt legyen; a `szó-szintű-tagged` esetleges kiadói taggelésnek marad). Következmény: az 1.1 ellenőrzés nem csak eltéréslistát ad, hanem **a `jeloltek`/`elofordulasok` Károli-tripletjét frissíti**: ahol a `parok` `magas` linkje egyezik a `karoli_szo`-val, az `azonositas_modja` `tartalom-alapú` → `szó-szintű-gépi`, a `megbizhatosag` a `parok` bizonyosságából. Az 1.7 szövegének és a DONTESEK 8. szakaszának módosítása a DT-M2-vel eldőlt; a triplet-frissítés az 1.1 brief (#65) része.

**22.3 A 26 pont → SEMA-tábla illesztés**

| pont | tábla / mező | állapot |
| --- | --- | --- |
| 1, 3, 18, 19, 20 | 2.20 `parok_<könyv>` (`strong`, `karoli_szo`, bizonyosság); `szavak_<könyv>` | van, könyvenként bővül |
| 2 | 2.20 `szavak` fordított indexe | származtatott |
| 4 | TAHOT/TAGNT-kivonat + 2.7 `grammatikai_strongok` szűrő | van; a `TILTOLISTA` hat tétele sosem szűrhető |
| 5 | `lekerdez.py kollokacio`; a formula a 2.2 `gerinc_elem` kollokáció-pár alakjában (`al+pané`) | van; biblemate `ClauseID` jelölt |
| 6 | 2.5 `lexikon_hivatkozasok` (`szotar`, `entry_id`), bdb_roots | részben |
| 7, 22 | 2.2 `elofordulasok.pardes_szint`, `fo_elofordulas` (csoportkulcs → ⭐), 2.1 `motivumok.pardes_szint` | van |
| 8 | 2.2 `elofordulasok` × 2.1 `motivumok` | van |
| 9 | 2.3 `kapcsolatok` (`tipus`, `bizonyossag`, `funkcio`) + 2.4 `jeloltek.indoklas` | van; a két tengely külön |
| 10 | 2.1 `motivumok.forras_study`, `statusz` (háromértékű) | van |
| 11, 25 | 2.4 `jeloltek` (`forras_kereses` = `TSK …`, `dontes`, `indoklas`) | van |
| 12 | `jeloltek.forras_kereses` ∈ {`scan`, `kollokacio`} ∖ {`TSK`, `Károli-KH`} + `dontes`; „még nem vizsgált" = `auditok` scan − `jeloltek` | **van, új tábla nélkül**; a 8 retroaktív motívum hiányos |
| 13 | 2.5 `lexikon_hivatkozasok` + 2.14 `forditasok` (`forditas_hu` renderidőben), D50 tartomány = az `elofordulasok.jelentes_szam`-hoz kötött sorok | van |
| 14, 26 | 2.11 `lxx_dontesek` (`bizonyossag` `biztos` \| `valoszinu` \| `nyitott` \| `nem_alkalmazhato`), `lekerdez.py lxx-hid`, #43 bridge | van; a generátor csak `biztos`-t mutat — a 26-os ★ ugyanezt a szűrőt követi |
| 15 | 2.16–2.18 kiejtés-táblák, 2.17 `kiejtes_kivetelek` az egyetlen héber forrás | van |
| 16 | FTS a `motivumok/[ID].md` + tanulmányok fölött | új (építés) |
| 17 | összeszerelés; a 2.12 `res_forras` render-elve (a rés törzse a tanulmányban él) a vers-lapra is | sablon |
| 21 | 2.2 `elofordulasok` önjoin igehelyre; 3. szabály 7. (`gate.py` ütközés/részhalmaz) | van |
| 23 | Strong-párok a 2.7 stopword-szűrővel; N13 küszöb | építés |
| 24 | 2.2 `elofordulasok.jelentes_szam` (union: szám \| binyan \| `teljes` tilos) ≠ a motívum fő előfordulásának `jelentes_szam`-a | **van** — a ◆ egy join, nem napló-olvasás |

**22.4 Amit az építő script és az MCP a SEMA-ból kötelezően visz**

- Közös típusok: 1.1 `IGEHELY` magyar kanonikus alak (három dataset STEPBible-pontozott, `Konyv_normalizalo_tabla` konvertál; normalizálás nélkül néma nem-találat); 1.2 `STRONG` négyjegyű nullázott, `+` több számnál; 1.5 `PROVENIENCIA` kötelező kulcsai és `scope` értékkészlete (`TAHOT-teljes`, nem `OT-full`, a 4. szakasz szerint); 1.8 `IGAZOLAS` külön mező, nem proveniencia-kulcs.
- 2.9 `auditok.lepes` zárt: `A5` \| `B2` \| `B3` \| `B4`. **Egy ad hoc hívás egyikbe sem fér** — DT-M3 🟢 (2026-10-05): a `lepes` a kutatási lépés kódját kapja (bármely csatornán), a lépésen kívüli lekérdezés új értéke `adhoc`; a csatorna (`csatorna=cli`, később esetleg `mcp`) a proveniencia-sorba kerül; alkalmazás: #61.
- 3. integritási szabályok mint teszt-sor az építésnél: hivatkozási épség (1.), nincs közvetlen út (2.), proveniencia-kényszer (3.), horgony-kényszer (4.), Károli-triplet (5.), gate-kényszer (6.), dataset-lefedettség (8.) — a `sqlite_epit.py` ezeket futtatja, és sértésnél megáll; az MCP író eszközei csak a `jeloltek`-be írnak (2. szabály).
- 2.6 `datasetek.tsv` `allapot` és a CC BY-SA következmény (SDBH/SDGNT származék azonos licenc) — a `licenc_allapot` szűrő forrása a 2.19-cel együtt.

**22.5 A SEMA 4. szakaszának nyitott tételei a tervben**

| SEMA 4. | hatás |
| --- | --- |
| TAHOT: fejezet-szinten teljes (a Jób 40:1–5 nem hiányzik, a Jób 41 pótolva, F84, DT86); maradó korlát: a Jób 40 kulcsai MT-számozásúak (TAHOT 40:(n+5) = Károli 40:n); a `scope` `TAHOT-teljes` | a Jób 40-nél a vers-lap a `szamozas` jelzővel köt, interpoláció nélkül (6. kockázat a MUNKATERV-ben; N-F41g); a 17.2 sor ennek megfelelő |
| `kapcsolatok.tipus` névütközés a pilot-TSV-vel | l. 22.1 — nem tetézzük harmadik tengellyel |
| SDBH ~90%, gyakori szavak hiányoznak | a szó-lap 4. szerep (jelentésszerkezet) üres cellája nem negatív lelet — jelölve |
| `keretszo` lista (34) nem teljes | az 5. pont frázis-keresését érinti; a `grammatikai_strongok` mellett külön lista |
