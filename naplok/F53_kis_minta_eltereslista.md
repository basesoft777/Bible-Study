# F53 — a kis minta eltéréslistája (FT.2 ⛔)

*Összevetés: a generált lap (`eszkozok/feladatterkep.py`, forrás-bélyeg `2026-10-05`,
commit `9d488a0`) és a mai kézi `FELADATTERKEP.html` (pillanatkép: main `e9b057b`).
A minta a repón kívül van: `C:\Users\bases\AppData\Local\Temp\claude\C--Users-bases-Desktop-Bible-Study\f72912cb-9878-462a-84d5-20e9d5613b43\scratchpad\minta\`
(`FELADATTERKEP.html`, `feladatterkep.json`). A két futás bájtazonos. Az összevetés
gépi (a kézi lap `T`, `RESZ`, `DT`, `WAVES` tömbjei és Mermaid-sorai a
generált JSON-nal), a besorolás kézi.*

**Általános ok.** A kézi lap egy korábbi pillanatkép: azóta kész a #42, #43, #51, felvételt kapott a
#53–#65 (a kézi lap „tervezett” sorai közül a STRONG_NORMALIZAL, JELOLTEK_RETRO,
KAROLI_ELLENORZES, BDB_ADATBLOKK mára #62, #63, #65, #56), a DT-M1–M8 és a DT-F42a–i bekerült a
`DONTESEK.md`-be. Ahol az eltérés csak ebből adódik: **a kézi lap tévedett (elavult)**. Az alábbi
sorok külön jelzik, ahol más az ok.

## Összkép-csempék

| csempe | kézi | generált | besorolás |
|---|---|---|---|
| Megállt | 2 | 2 | azonos szám; a tartalom más: #22 (mindkettő), kézi: #38 → generált: #64 |
| Fut | 2 | 2 | #52 mindkettőben; kézi #43 → generált #53 (a #43 kész) |
| Indítható | 3 | 8 | a kézi lap tévedett (elavult): #42 kész, #44 azóta indítható; új: #57, #58, #60, #62; **#50: l. lent (a generátor téved, forráshiány miatt)** |
| Függésre vár | 9 | 14 | a kézi lap tévedett (elavult): #38 áthelyezve, #54, #55, #56, #59, #61, #63, #65 új |
| Felvehető | 5 | 5 | azonos szám; a tartalom más: kézi 5 `új`, generált: TERV_BEFOGAD, SQLITE_EPIT, MCP_BUROK, OLVASOI_KONKORDANCIA, SZPA_AUDIT |
| Nyitott döntés | 3 | 6 | a kézi lap tévedett (elavult): DT-F38i azóta 🟢; DT-M1, M4, M5, M6 felvéve 🟡 |

## Kártyák

**Csak a kézi lapon** (a generátorban nincs kártya)

| kártya | besorolás |
|---|---|
| #42 FORRASKIVEZETES | a kézi lap tévedett (elavult: lezárva, a main-en is) |
| #43 LXX_BRIDGE | a kézi lap tévedett (elavult: lezárva, a main-en is) |
| #51 KONZISZTENCIA | a kézi lap tévedett (elavult: lezárva, a main-en is) |

**Csak a generátorban**

| kártya | besorolás |
|---|---|
| #53 FELADATTERKEP, #54, #55, #57, #58, #59, #60, #61, #64 | a kézi lap tévedett (elavult: a lap után felvett feladatok) |
| TERV_BEFOGAD (tervezett) | a kézi lap tévedett: a MUNKATERV 4. szakaszának első sora és az 1. hullám eleme, a kézi lap kártyát nem adott neki |

**Mindkettőben, állapot- vagy függéseltérés**

| kártya | eltérés | besorolás |
|---|---|---|
| #38 BDB_FORDITAS | állapot: megállt → függésre vár (brief: `fut`, `Folytatás:`); függ: `#34 ✓` → `#34 (kész), #56*, #57*` | a kézi lap tévedett (elavult: a #38 azóta „Folytatás”-ban áll, és a #56/#57 elé kerül; a `feladatok.py jeloltek` is „vár: #56, #57”-et ad). **Modellezési megjegyzés:** a `fut` + `Folytatás:` állapotot a generátor mint a nem indultat kezeli (vár / indítható), nem mint „Fut (▶)”; l. a kérdéseket |
| #44 LICENC_UTOKOVETES | állapot: függésre vár → indítható; függ: `#42` → `#33 (kész), #42 (kész)` | a kézi lap tévedett (elavult: a #42 azóta kész) |
| #50 CI_JAVITO_KOR | állapot: függésre vár → indítható; függ: `#45` → `—` | **a generátor téved, forrásadat-hiány miatt.** A generátor a FELADATOK.md-vel egyezik (⬜, „Függ ettől: —”), mert a brief fejléce `fugg: []`; a brief „következő lépés” szövege viszont „futtatható a #32 és a #45 lezárása és mergelése után” — a #45 nincs kész. A lap „Indítható”-nak mutatja. A javítás a #50 briefjében lenne (fejléc), nem a generátorban; l. a kérdéseket |
| STRONG_NORMALIZAL | tervezett → indítható | a kézi lap tévedett (elavult: azóta #62, FELADATOK-sor) |
| JELOLTEK_RETRO | tervezett → függésre vár (#62*); függ: `— (adat megvan)` → `#62*` | a kézi lap tévedett (elavult: #63; a levezetett függés a briefekből jön) |
| KAROLI_ELLENORZES | tervezett → függésre vár; függ: `#22, DT-M2` → `#62, #63*` | a kézi lap tévedett (a FELADATOK-sor nyer: a #65 fejléce `fugg: [62, 63]`). **Forrás-ellentmondás:** a MUNKATERV 4. szakasza még „#22 könyvenként, DT-M2”-t ír; a DT-M2 éle a DONTESEK „Feladat” oszlopából megmarad, a #22 éle nem; l. a kérdéseket |
| BDB_ADATBLOKK | tervezett → függésre vár; függ: `#38, DT-F38i` → `#57*` | a kézi lap tévedett (a FELADATOK-sor nyer: #56). **Forrás-ellentmondás:** a MUNKATERV szerint a BDB_ADATBLOKK függ a #38-tól, a briefek szerint a #38 függ a #56-tól (irány megfordul); l. a kérdéseket |
| SQLITE_EPIT, MCP_BUROK, OLVASOI_KONKORDANCIA | halasztott (szürke) → tervezett (lila) | a kézi lap tévedett: a „később” minősítés nem forrásból jött (a MUNKATERV nem jelöl halasztást). **Tartalmi kérdés** a felhasználónak: kell-e halasztott-jelölés, és honnan (l. a kérdéseket) |
| OLVASOI_KONKORDANCIA | függ: + `; hosting ⛔` | nem tartalmi eltérés (a generátor szó szerint adja a MUNKATERV „függ” celláját) |
| #40, #48, #37, #9, #36, #10, #7, #30 | függ: a kézi lap a kész függéseket elhagyta vagy `✓`-val jelölte; a generátor a FELADATOK.md „Függ ettől” szövegét adja (`(kész)`), és a #9, #36, #38 mellé a #56*-ot is | a kézi lap tévedett (rövidített/elavult); a #36-nál a kézi `#42*` azóta kész |

**Mind a 31 kézi kártya „Most:” sora** a kézi lap saját összefoglalója volt; a generátor a brief
`kovetkezo` mezőjét adja (a lapon legfeljebb 220 karakter, a teljes szöveg a kurzor alatt). Nem
eltérés, de az olvashatóságra hat: sok `kovetkezo` gépies („/kovetkezo; ⛔ az M0 után …”).

**Leírás nélküli kártyák** (a TSV-ben nincs sor, a lap „nincs leírás”-t ír, nem pótol): #53, #54, #55, #57, #58, #59, #60, #61,
#64, TERV_BEFOGAD. A TSV három sora kártya nélkül maradt (kész feladatok: FORRASKIVEZETES, KONZISZTENCIA,
LXX_BRIDGE) — a JSON `kartya_tabla.felhasznalatlan` mezőjében látszik.

## Döntések

| lista | kézi | generált | besorolás |
|---|---|---|---|
| Nyitott | DT-F38i, DT2, DT-F41a | DT2, DT-F41a, DT-M1, DT-M4, DT-M5, DT-M6 | a kézi lap tévedett (elavult): DT-F38i 🟢; DT-M1, M4, M5, M6 azóta 🟡 a DONTESEK-ben |
| Eldöntve, alkalmazásra vár | 7 tétel | 22 tétel | a kézi lap tévedett (elavult): új DT-F38d, DT-F38i, DT-F42a–i, DT-M2, DT-M3, DT-M7, DT-M8 |
| Javasolt, még nincs felvéve | DT-M1–M6, „#23 M0” | üres | a kézi lap tévedett: a DT-M1–M6 már a DONTESEK-ben van; a „#23 M0” sem a DONTESEK-ben, sem a MUNKATERV 2. szakaszában nem DT (a kézi lap saját tétele) |
| Ellenőrizendő sor | nincs | DT1, DT3, DT4, DT19 | új kategória (7.3). Mind ✅-jelű, de az oszlopszámuk eltér a táblafejléctől (DT1, DT4: 7 oszlop; DT3, DT19: 10 oszlop, a szabad szövegben `|`), ezért a generátor nem találgat. Nem hiba egyik oldalon sem; a sorok javítása (`\|`) a DONTESEK.md dolga, nem ezé a feladaté |

## Függési térkép

**Csomópontok csak a kézi lapon:** #42, #43, #51 — a kézi lap tévedett (elavult: kész feladatok, a térképen nem szerepelnek).

**Csomópontok csak a generáltban:** #53, #54, #55, #57, #58, #59, #60, #61, #64 (új feladatok) —
a kézi lap tévedett (elavult); TERV_BEFOGAD — a kézi lap tévedett (hiányzott); DT-F38d, DT-M7, DT-M8
(új DT-k), DT-M4, DT-M5 — a kézi lap tévedett (a MUNKATERV „függ” cellája és a DONTESEK szerint van él hozzájuk).
A DT1 először megjelent a térképen (ellenőrizendő sor); ezt javítottam (a generátor téved volt):
az ismeretlen állapotú sor nem rajzolódik nyitott döntésként. A tesztek zöldek.

**Élek:** kézi 39, generált 52, közös 31.

| él (csak a kézin) | besorolás |
|---|---|
| #36→#42, #44→#42 | a kézi lap tévedett (elavult: a #42 kész) |
| #50→#45 | l. #50 fent (a generátor téved, forrásadat-hiány miatt) |
| #51→#37 | a kézi lap tévedett (elavult: a #51 kész) |
| #56→#38, #56→DT-F38i | forrás-ellentmondás (irány): a briefek szerint #38 → #56; a kézi lap a MUNKATERV irányát rajzolta. A generátor a briefet követi; l. a kérdéseket |
| #63→#23 (szaggatott „bemenet”) | a kézi lap többlete: „bemenet”-viszony, a briefekben és a MUNKATERV „függ” oszlopában nincs; a generátor csak függést rajzol |
| #65→#22 | forrás-ellentmondás: a #65 fejléce nem sorolja a #22-t; a MUNKATERV igen. A generátor a briefet követi |

| él (csak a generáltban) | besorolás |
|---|---|
| #54→#62, #55→#54/#63/#65, #59→#58, #61→#54/#62, #63→#62, #65→#62/#63, #56→#57, #38→#57/#56/DT-F38d, #9→#56, #36→#56 | a kézi lap tévedett (elavult: új feladatok és levezetett függések) |
| #36→#7 | a kézi lap tévedett: a saját kártyája is „#7*”-ot ír, az él a térképről hiányzott |
| MCP_BUROK→DT-M5/DT-M7, OLVASOI_KONKORDANCIA→DT-M4, TERV_BEFOGAD→DT-M8 | a kézi lap tévedett: a MUNKATERV „függ” cellája, ill. a DONTESEK „Feladat” oszlopa szerint van él |

## Hullámok

| elem | kézi | generált | besorolás |
|---|---|---|---|
| 0. lépcső | futó (zöld) | kész ✓ | nem tartalmi eltérés (a generátor a „(kész)” szövegből jelzi) |
| TERV_BEFOGAD | függésre vár | tervezett | a kézi lap tévedett: nincs feladat-sora, a forrás nem ad „vár”-állapotot |
| STRONG_NORMALIZAL / JELOLTEK_RETRO / KAROLI_ELLENORZES / BDB_ADATBLOKK | tervezett | indítható / vár / vár / vár | a kézi lap tévedett (elavult: #62, #63, #65, #56) |
| SQLITE_EPIT, MCP_BUROK, OLVASOI_KONKORDANCIA | halasztott | tervezett | l. a halasztott-jelölés kérdését fent |
| a ⛔ szövegek | rövidített | a MUNKATERV 5. szakaszának szó szerinti cellája | nem tartalmi eltérés (átfogalmazás); a generált az aktuális MUNKATERV-et adja |

## Most induló sor

A kézi lap a chat 2026-10-05-i sorrendjét mutatta (STRONG_NORMALIZAL, SZPA_AUDIT, JELOLTEK_RETRO, #30, DT-M2, KAROLI_ELLENORZES,
BDB_ADATBLOKK). A generált: a `feladatok.py jeloltek` jelöltjei — #30, #44, #57, #58 (a brief 8.2 döntése szerint; a
`jeloltek` csak az 1. fázis feladataira fut, így a folyamat-fázisú #45, #50, #62 a „Most induló sor”-ban nem szerepel,
kártyán „Indítható”). Nem eltérés, hanem a döntés következménye.

## Kérdések a felhasználónak (tartalmi döntés — a generátor nem dönt)

1. **#50:** a lap „Indítható”-nak mutatja, de a brief szövege a #45 lezárására vár. Javítás: a #50 briefjének
   `fugg:` mezője (nem ennek a feladatnak a hatóköre) — kérsz-e N-tételt?
2. **MUNKATERV ↔ briefek függési irány** (BDB_ADATBLOKK/#56 ↔ #38; KAROLI_ELLENORZES/#65 ↔ #22): a generátor a briefet követi
   (a brief 3. pontja: a FELADATOK-sor nyer). A MUNKATERV-et a #52 TERV_SZINKRON hozhatná egyre — kérsz-e értesítést?
3. **Halasztott jelölés** a tervezett (még fel nem vett) feladatoknál (SQLITE_EPIT, MCP_BUROK, OLVASOI_KONKORDANCIA): ma nincs forrás.
   Opciók: (a) marad „tervezett” minden; (b) a MUNKATERV 4. szakaszába új oszlop/jelölés (a #52 hatóköre); (c) a TSV-be új oszlop.
   Javaslat: (a), amíg a forrás nem jelöli.
4. **`fut` + `Folytatás:` (#38):** „Fut (▶)” oszlopban vagy várakozóként/indíthatóként jelenjen meg? Ma: mint a nem indult
   (a `jeloltek` logikájával egyezően). Javaslat: így marad.
5. **Leírás nélküli kártyák** (10 db, fent): a szövegeket (`reszletes`, `roviden`) tartalmilag te hagyod jóvá; kérsz-e piszkozatot a TSV-be?

## A felhasználó válasza (2026-10-05) — a minta jóváhagyva, mehet az FT.3

1. **Igen**, két pontosítással: a #50 fejlécébe `fugg: [45]`, és a `kovetkezo:` sorból a #32 is kikerül (a #32 a PR #164-gyel a main-en van) → **N-F53a**. A `DONTESEK.md` javítása külön N-tétel, és a négy sor nem egyformán hibás: a DT3-ban és a DT19-ben fölös `|` → `\|`; a DT1-ben és a DT4-ben a Döntés és a Napló egy cellában áll, ott az elválasztó `|`-t kell beszúrni → **N-F53b**.
2. **Kész, ehhez a feladathoz nem tartozik.** A MUNKATERV a PR #199-cel (DT-M8) a briefekhez igazodott: a #56 függése `SQLITE_EPIT`, a #38 ráépül; a #65-nél a #22 bemenet, és az F65 fejlécében `nem_fugg: [22]` áll. A main az FT.3 előtt behúzva (`5c7abe2`). **Maradék, nem javítva:** a generált lap a #56-nál `#57*`-ot mutat (a FELADATOK-sor szerint), a MUNKATERV `SQLITE_EPIT`-et; a tervezett, fel nem vett SQLITE_EPIT a brief fejlécébe nem írható, így a FELADATOK-sor nyer (a brief 3. pontja).
3. **(a)** — marad „tervezett”.
4. **Igen** — a #38 a „Függésre vár” oszlopban marad.
5. **Igen**, külön tételben, az FT.3 után; a kártyaszöveg csak piszkozat lehet, és csak a felhasználó jóváhagyása után kerülhet a TSV-be → **N-F53d**.

A lap három kisebb hibája külön tételbe megy, nem az FT.3-ba → **N-F53c**: a Markdown nyersen jelenik meg (`*(forrás: …)*`, visszaperjelek a címekben); a térképen a #22 felirata „#22 F22” (a kódnév hiányzik); a „Most induló sor” végén lóg egy `‖`.
