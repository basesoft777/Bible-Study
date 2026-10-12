# F64 M0 — TEREMT-002 próza-próba: bemenetek és ⛔

*FELADATOK #64 · `F64_TEREMT002_PROZA_PROBA_BRIEF.md` 3. szakasz, M0 · ág `claude/f64-teremt002-proza-proba` · 2026.10.08*

Az M0 csak olvas és mér: adattábla, `lexikon/`, `tematikus_lezart/`, `motivumok/` nem változott; próza nem készült. A próbafuttatások a repón kívüli ideiglenes könyvtárba mentek (CLAUDE.md, `generalt_proba/`-szabály). A számok saját lekérdezésből származnak (`split('\t')`, a mérőszkript a session scratchpadjában, nem a repóban); minden szám mellett a proveniencia-sor.

---

## 1. A #23 M0 kimenete

**Jóváhagyás.** A #23 M0 ⛔ döntése a `DONTESEK.md` DT66 tétele (🟢; felhasználó, chat, 2026.10.07): (a) a `javaslat` besorolások elfogadva öt kivétellel; (b) a `sablonszabaly` negyedik B_helye-érték; (c) aktiválási feltétel: ⭐ küszöb VAGY van lezárt tematikus forrás; (d) a #23 M1 csak a #12a (#64) után indulhat. A felhasználó a #23 M0 jóváhagyását ebben a sessionben (2026.10.08) kifejezetten megerősítette; a DT66 átvezetése a leképezésben megtörtént (F23.14). **A ⛔ feltétel („ha a #23 M0 nem futott vagy nincs jóváhagyva”) nem áll fenn — a feladat indulhat.**

**A leképezés megvan:** `naplok/MOTIVUM_FORRAS_lekepezes.tsv`, 77 adatsor, oszlopok: `szakasz, sablon, ma_hol_el, B_helye, szint, aktivalas, megjegyzes, forras_parancs`.
`scope=naplok/MOTIVUM_FORRAS_lekepezes.tsv | forras=a fájl teljes olvasása | n=77 | ts=2026-10-08`

**A tematikus sablon (4_tematikus) sorai — kivonat** (a 6. és 8. sablon sorai a 2–3. pontban, ahol a prózát érintik):

| Szakasz | B_helye | szint | aktiválás | TEREMT-002-n |
|---|---|---|---|---|
| Kivonat | `kezi_forras` | olvasoi | mindig | **aktív** — az érvelés nyitánya |
| 0. Forrás-összegyűjtés | `adat` | belso | feltételes: örökölt motívum | **inaktív** (natív; a leképezés szó szerint: „natív motívumnál (TEREMT-002) üres”) |
| 1. Friss keresés P1–P7 | `adat` | belso | mindig | adatból (T1–T2: `auditok`, `jeloltek`); a P2 mező-hipotézis indoklása próza |
| 1. Előfordulások — 7 oszlopos tábla | `adat` | apparatus | mindig | generált nézet (`elofordulasok.tsv`) |
| Logikai kötőszó szerinti bontás | `kezi_forras` | apparatus | feltételes: tartományos sor | **inaktív** (a 3 sor mind egy vers) |
| 2. Eredeti nyelvi összevetés | `kezi_forras` | apparatus | mindig | **aktív**; a szótári idézet adat (l. 5. pont: BDB-mezők üresek) |
| 2/b. Kiegészítő szótári adatok | `adat` | apparatus | feltételes | **inaktív** (nincs `lexikon_hivatkozasok` sor) |
| 3. PaRDeS — Peshat / Remez / Drash / Sod | `kezi_forras` | olvasoi | ⭐ küszöb VAGY lezárt tematikus forrás | **aktív**: a ⭐ küszöb teljesül (3 különböző `fo_elofordulas`, l. 5. pont) |
| 3. ⚠️ Vitatott pontok | `kezi_forras` | olvasoi | feltételes: tudományosan vitatott | a próza dönti el (ha nincs, nem üres címmel) |
| 4. Kapcsolódás a kutatási sablonhoz | `kezi_forras` | apparatus | feltételes | a próza dönti el; ha nincs, kimarad |
| 5. Alkalmazás és tanítványság | `kezi_forras` | olvasoi | ⭐ VAGY lezárt forrás | **aktív** |
| 5. Nevesített tanítói egyezés | `kezi_forras` | olvasoi | feltételes: lefutott a 7. lépés | **inaktív** (a 7. lépés nincs a hatókörben); hivatkozó hiánymondat kell (l. 3. pont L5) |
| 6. Napló-frissítés (státusz) | `adat` | belso | mindig | adat (`motivumok.tsv statusz`), nem próza |
| 【NAPLO】 blokkok | `kezi_forras` | belso | feltételes | kivétel (DT66 a/1): kézi, de mindig `belso` |
| Minőségi kapu (Q1–Q7) | `adat` | belso | mindig | az eredmény adat; a próza nem írja be |
| Verzió-címke | `adat` | belso | mindig | `motivumok.tsv` |
| Mikor használandó; Lezárási checklist; Terminológiai szabályok; Konfliktuskezelés | `sablonszabaly` | — | nem dokumentumszakasz | szabályként alkalmazandó, nem írandó |
| Tartalmi visszaírás bővített tanulmányokba | `generalt` | apparatus | feltételes | **inaktív** (a 3 igehelynek nincs saját bővített tanulmánya; `felmerult_tanulmany` üres) |

A `motivumok/[ID].md`-blokkok sorai: a ⭐-bekezdés értelmező mondatai (TEREMT-002: „teremtés visszavonása”) `kezi_forras olvasoi` anyag a Kivonathoz / 3. szakaszhoz; a Tematikus áttekintés és a Kulcsszó-index archív, `generalt belso`; a Forrásréteg-fejléc dőlt proveniencia-bekezdésének célja NAPLO-blokk (`belso`, DT66 a/3). A „teremtés-visszavonás” kifejezés rendezése a T3 prózájára vár (N25).

**Következmény a prózára:** a kézi próza helye az aktív `kezi_forras` sorok: Kivonat, 2. Eredeti nyelvi összevetés (értelmezés), 3. PaRDeS (négy szint + esetleges Vitatott pontok), 5. Alkalmazás, 7. Nyitott kérdések (a 6. sablon `modszertan` résének kézi része), valamint a 4. szakasz, ha van tárgya. Ezek együtt egy összefüggő érvelést adnak (K1/2), nem önálló mezőket.

## 2. A próza helye

**Javaslat (a briefé, és ezt támogatom):** a próza a `motivumok/TEREMT-002.md`-be kerül, a tematikus sablon szakaszsorrendjével; külön `tematikus_lezart/` fájl nem készül.

Indok:
- a D34 és a CLAUDE.md átmeneti bekezdése szerint motívumonként egy kézi forrás a cél, és a motívumcikk generált nézet; a leképezés minden prózai sort `kezi_forras`-nak sorol, a forrás pedig a `motivumok/[ID].md`;
- a TEREMT-002 natív egyforrású (DT66 (3): „nincs tematikus tanulmánya”); a `motivumok/TEREMT-002.md` proveniencia-bekezdése és a `TEREMT002_KUTATAS_BRIEF.md` (14. sor) is ezt rögzíti: „a próza a T3-ban közvetlenül a forrásrétegbe kerül”;
- egy második kézi forrás a DT28 kétirányúságát hozná vissza, amelyet épp a #11 migráció bont le;
- a próba célja a #23 M1 forrássablonjának mérése: ha a próza nem a B-forrásban születik, a próba nem méri azt, amit kell.

**Alternatíva:** külön tanulmányfájl (`tematikus_lezart/Tohu_va_vohu_tematikus.md` jellegű), a DT-F32a „a tematikus tanulmány prózája” szövegének szó szerinti olvasata. Előny: a mai `lexikon_general.py` rés-mechanizmusa (`RÉS-KEZDET`/`VÉGE` a tanulmányban, `res_forras.tsv` `tanulmany` forrással) ezt ismeri. Ár: második kézi forrás, a #11-ben migrálandó; és a rés-útvonalhoz `res_forras.tsv`-sor kellene, amit a brief kizár (2. szakasz, „Nincs benne”). Ezért a próbarenderen az alternatíva sem nyer.

**Járulékos megfigyelés (nem döntés):** a mai forrásfájl három archív blokkot hordoz (Tematikus áttekintés, ⭐-bekezdés, Kulcsszó-index). A javaslat szerint a próza ezek mellé kerül; az archív blokkok sorsa (#11) nem az M1 dolga. A `general.py` csak az allowlistben (`BEOLVASZTHATO_SZAKASZOK`) felsorolt fejléceket olvashatná — l. 4. pont.

## 3. A mérce alkalmazhatósága

**A mérce forrása.** A brief és a `F32_KONTEXTUS_BRIEF.md` (76. sor), `F23_MOTIVUM_FORRAS_BRIEF.md` (62. sor), `MUNKAMENET.md` (138–139. sor) „L1–L5 a #10 szerint”-et ír; a #10 mércéje viszont a DT2 (🟢, felhasználó, 2026.10.06): **a lexikonoldal-sablon Minőségi kapuja, L1, L3–L6, plusz: minden rés kitöltött vagy explicit hiány-/`adat`-jelölésű; L2 és L7 nincs.** A kapu (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md` 387–434. sor) L1, L3, L4, L5, L6 pontot tartalmaz; az „L1–L7” a chatben maradt #10-briefből jött (DT2). A két megfogalmazás tehát az L6-ban tér el: az „L1–L5” szövegben az L6 is benne van-e. Javaslat: az L6 benne van (a DT2 ezt mondja, és a #10 ezzel dolgozik).

**Honnan a rés.** A lexikonkapu a tematikus sablon Q-kapujából adaptált (a sablon szövege szerint), és a számozás megfeleltethető: L1↔Q1, L3↔Q3, L4↔Q4, L5↔Q5, L6↔Q6. A kihagyott két pont: **Q2 (négyforrásos audit nyoma dokumentált)** és **Q7 (dataset-lefedettség indokolt és ellenőrizhető)** — mindkettő a forrás-rétegre szól, nem a lapra, ezért esett ki a lexikonkapuból. A prózapróba viszont épp a forrást méri.

**Alkalmazhatóság pontonként:**

| Pont | A forrásban álló prózára (`motivumok/TEREMT-002.md`) | A próbarenderre (`generalt_proba/TEREMT-002_proza_proba/`) |
|---|---|---|
| **L1** Szerkezeti teljesség (13 TUDOMÁNYOS-szakasz + OLVASHATÓ 7) | **nem alkalmazható szó szerint**: a szakaszlista a TUDOMÁNYOS lapra szól; az OLVASHATÓ változat 2026.09.21 óta megszűnt. Átfordítva: a tematikus sablon aktív `kezi_forras` szakaszai (1. pont, „Következmény”) mind jelen vannak, és az inaktívak nem üres címmel, hanem hiányjelöléssel/kihagyással kezeltek (Q1 + D37/DT66 c) | **részben**: lexikonoldal nem renderelhető (4. pont), tehát a 13-as lista nem ellenőrizhető; a renderelt adatnézetekre (1. tábla, napló, kereszthivatkozás-napló) szakaszonként „renderelt / nem renderelt” ítélet adható |
| **L3** Lexikai vs. tematikus szétválasztva | **alkalmazható** (= Q3): pl. Ézs 45:18, Ézs 24:10 (önálló *tohu*, kapcsolat-sor, nem előfordulás) csak „tematikus, nem lexikai” jelöléssel | alkalmazható a renderelt kapcsolat-/jelölt-nézetre |
| **L4** Kereszt-motívum szennyeződés kizárva | **alkalmazható** (= Q4): kiemelten a TEREMT-001-gyel közös 1Móz 1:2 (funkció-különbség a gate-ben dokumentált) és a HAMART-001-naplóbeli régi kifejezés (N25) | alkalmazható |
| **L5** Nevesített tanítói szakasz | **alkalmazható Q5-ként**: a 7. lépés kívül esik, ezért a próza explicit hiánymondattal zárja (DT66 a/2: hivatkozás a 7. lépés saját fájljára, ha lesz) | nem alkalmazható (nincs lap) |
| **L6** Napló-/formázási-/hangnem-fegyelem (a–g) | **alkalmazható** (= Q6); az (f) „mi-hangú mondat a TUDOMÁNYOS változatban” a forrás `olvasoi` szintjére is értelmezendő | alkalmazható a renderelt fájlokra; a nyilvános nézetben 0 `【NAPLO` (M1/3 előképe) |
| *(L2 — nincs)* | ↔ **Q2** négyforrásos audit nyoma: a TEREMT-002-n az adatban dokumentált (`auditok.tsv` A5/B2/B3/B4, 222 sor; `jeloltek.tsv` 66 sor, mind minősítve) — ellenőrizhető | ↔ a generált kereszthivatkozás-napló adja |
| *(L7 — nincs)* | ↔ **Q7** dataset-lefedettség (`adat/datasetek.tsv`, `study_tipus = tematikus`) | — |

**Kiegészítő mérce, amely a briefből következik, nem a kapuból:** a DT2 „minden rés kitöltött vagy explicit hiány-/`adat`-jelölésű” fele a prózára így fordítható: minden aktív `kezi_forras` szakasz kitöltött, vagy explicit hiányjelölésű (CLAUDE.md 3. szabály). Ez a K2 elfogadási feltétellel egybeesik.

**Javaslat az L2/L7 résre:** az L2 és az L7 helyén a **Q2 és Q7 forrás-oldali megfelelője** kerüljön a próba mércéjébe, *mérési pontként, nem a DT2-mérce bővítéseként* (a #10 mércéje változatlan marad). Indok: a próba forrást mér, és a két pont pontosan az, amit a lexikonkapu a forrásra bízott. Alternatívák: (2) szó szerint a DT2: L1, L3–L6, a rés üres marad, és a Q2/Q7 nem mérődik; (3) a teljes Q1–Q7 a mérce (a forrás tematikus jellege miatt), az L-pontok csak a próbarenderre.

## 4. A jelenlegi generátor képessége

Futtatva: `python eszkozok/general.py --cel <cél> --id TEREMT-002 --kimenet <repón kívüli scratchpad>` mind a hét célra; a munkafa utána tiszta (`git status`: nincs változás).
`scope=--id TEREMT-002, célok: naplo,index,naplok,study,nyitott,lexikon,torzscikk | forras=eszkozok/general.py (adat/motivumok.tsv, elofordulasok.tsv, jeloltek.tsv) | ts=2026-10-08`

| Cél | Eredmény a TEREMT-002-re | Prózát olvas a `motivumok/`-ból? |
|---|---|---|
| `naplo` | renderel: 4 marker-blokk (attekintes, kuszob, kulcsszo_index, konyv_index) | **nem** — a `kuszob` blokk csak helyőrzőt ír: „a bekezdés-próza a G2 után a `motivumok/TEREMT-002.md`-ből fűződik ide” |
| `index` | renderel; a TEREMT-002 nem szerepel (nincs lezárt tanulmány) | — |
| `naplok` | renderel: `TEREMT-002_kereszthivatkozas_naplo_GENERALT.md` (66 jelölt; 3 beépítve, 63 elutasítva, 0 nyitva) | **nem** — a záró mondat: a Strong-lista és a tanítói gap-jelzés „a forrásrétegben … él — innen nem vezethető le” |
| `study` | renderel: `TEREMT-002_1_pont_GENERALT.md`, a 7 oszlopos 1. tábla, 3 sor; a BDB-oszlopok „—” | — |
| `nyitott` | renderel (a TEREMT-002 1 sorral) | — |
| `lexikon` | **KIHAGYVA**: „nincs egyetlen `res_forras.tsv` sora sem” | — |
| `torzscikk` | **KIHAGYVA**: nincs lexikonoldal | — |

**Lelet:** a `forrasreteg_beolvaszthato_szakaszok()` függvény (allowlist: „Kulcsszavak részletesen”, ⭐-bekezdés) definiálva van, de **egyetlen hívása sincs** az `eszkozok/*.py`-ban (`grep`). A mai generátor tehát **semmilyen prózát nem renderel a `motivumok/[ID].md`-ből**; a lexikonoldal-rések pedig csak `res_forras.tsv`-sorral (tanulmány-útvonal vagy `adat` mondat) töltődnének, amely a TEREMT-002-nek nincs, és a brief szerint nem is kaphat.

**Következmény az M2-re (generátor nem módosul):** a `generalt_proba/TEREMT-002_proza_proba/` alá a fenti öt adatnézet renderelhető (napló-blokkok, kereszthivatkozás-napló, 1. tábla, nyitott-sor); **a teljes próza „nem renderelt”** jelölést kap a mérési jelentésben, szakaszonként. Ez maga is #23 M1-bemenet: a B-szerkezethez kell a forrás-próza renderútja (szintjelöléssel), amely ma nincs. A `--cel naplo/index/nyitott --ellenoriz` fixpontot a próbafuttatás nem érinti (nem `--ir`).

*Mellékmegfigyelés:* az `index` cél `--id` szűkítéssel is kiírja a „HIÁNYZÓ ZÁRT ID (K8): HAMART-001” figyelmeztetést — ismert (F3/K9), a TEREMT-002-t nem érinti.

## 5. Az adat-alap

| Tábla | TEREMT-002 sor | Kivonat | Proveniencia |
|---|---|---|---|
| `motivumok.tsv` | 1 | `statusz` = feldolgozás alatt (v1, 2026.09.25); `azonossag_tipusa` = formulaikus; `pardes_szint` = Remez; `negativ_kriterium` = H8414 + H0922 egy versben; `forras_study`, `sablon_verzio` üres | `scope=id=TEREMT-002 | forras=adat/motivumok.tsv | n=1 | ts=2026-10-08` |
| `elofordulasok.tsv` | 3 (az összes 259-ből) | 1Móz 1:2 (Peshat), Jer 4:23 (Remez), Ézs 34:11 (Remez); `strong` H8414+H0922, `gerinc_elem` tohu+bohu mindháromnál; 3 különböző `fo_elofordulas` → ⭐ küszöb teljesül; BDB-mezők (`lexikon_entry_id`, `jelentes_*`) üresek; `felmerult_tanulmany` üres | `scope=id=TEREMT-002 | forras=adat/elofordulasok.tsv | n=3 | ts=2026-10-08` |
| `jeloltek.tsv` | 66 (342-ből) | 3 beépítve, 63 elutasítva, 0 nyitva; forrás: scan H8414 13, TSK-célpontok, Károli-KH | `scope=id=TEREMT-002 | forras=adat/jeloltek.tsv | n=66 | ts=2026-10-08` |
| `kapcsolatok.tsv` | 5 (39-ből) | 1Móz 1:2→Jer 4:23 Kontraszt (magas); 1Móz 1:2→Ézs 34:11 Kontraszt (magas); Jer 4:23→Ézs 34:11 Párhuzam (közepes); 1Móz 1:2→Ézs 45:18 Kontraszt (közepes); Ézs 24:10→Ézs 34:11 Párhuzam (alacsony); mind Remez | `scope=id=TEREMT-002 | forras=adat/kapcsolatok.tsv | n=5 | ts=2026-10-08` |
| `auditok.tsv` | 222 (a tábla mind a 222 sora TEREMT-002) | A5 142, B2 1, B3 3, B4 76; ebből 58 B4-sor `lxx-hid` (forrás: régi `LXX_kivonat_*.tsv`) | `scope=id=TEREMT-002 | forras=adat/auditok.tsv | n=222 | ts=2026-10-08` |
| `res_forras.tsv` | 0 | a lexikonoldal-réteg nem indult (#12b) | `scope=id=TEREMT-002 | forras=adat/res_forras.tsv | n=0 | ts=2026-10-08` |
| `lxx_dontesek.tsv` | 0 | a #12b tárgya | `scope=id=TEREMT-002 | forras=adat/lxx_dontesek.tsv | n=0 | ts=2026-10-08` |
| `lexikon_hivatkozasok.tsv` | 0 (H8414/H0922 sem) | a 2. szakasz szótári idézetéhez nincs adatsor | `scope=strong=H8414,H0922 | forras=adat/lexikon_hivatkozasok.tsv | n=0 | ts=2026-10-08` |

**A T1–T2 naplók és a kapcsolódó tételek nyitott pontjai** (a próza szempontjából):

1. **LXX-alap — a legfontosabb (új összefüggés).** A TEREMT-002 mind az 58 `lxx-hid` audit-sora a 2026.09.25-i, azóta kivezetett `LXX_kivonat_*.tsv`-ből származik (#42, F42.M5; a mai `lxx-hid` az `LXX_OS`-ből olvas). Az összevetés (`naplok/FORRASKIVEZETES_M5_eltereslista.tsv`) mindhárom előfordulás-versnél eltérést mutat: 1Móz 1:2 `strong_eltero`, Ézs 34:11 `strong_eltero`, Jer 4:23 `nagy_eltero`; az öt zsoltár-sor (Zsolt 107:40, 104:30, 33:6, 80:6, 80:7) a régi zsoltár-kivonat egyverses eltolására épül (N17 „tartalmi kérdés, nem javítva”). A brief M1-szabálya („LXX-állítás csak a meglévő `lxx-hid` lekérdezés proveniencia-sorával”) ezért kivezetett forrásra mutató proveniencia-sort írna elő. → döntési kérdés (DT69).
2. **N22** — a `Karoli_kereszthivatkozasok.tsv` `Isa.34.11` listája az `Isa.40.11` másolata; az öt érintett jelölt „adathiba” indokkal elutasítva; az Ézs 34:11 valódi Károli-KH célpontjai nincsenek felmérve. A prózában explicit hiány.
3. **N25** — a „teremtés-visszavonás” kifejezés rendezése a T3 prózájában (a cím a gate óta „a föld kietlen és puszta állapota a teremtéskor és az ítéletkor”).
4. **N20 / N21** — `Pshat`/`Peshat` (SEMA vs. adat) és a `Karoli_Strong_kivonat` Gen.1.2 nullázatlan `H922`-je: a prózát nem blokkolja, a hivatkozott Strong-alak `H0922`.
5. **TAHOT-lefedettség** — a T1-scan hatókör-fenntartása (1Móz 32, Zsolt 88/89/140/142, Jóel 3 hiányzik) a CLAUDE.md szerint részben elavult (ezeket az F2 2026.09.14-én pótolta); a fennmaradó ismert hiány a Jób 40:1–5 és a Jób 41. A próza „teljes körű” állítása ezzel a fenntartással írandó; a TEREMT-002 3 versét nem érinti.
6. **Gate-hagyaték** — a B változat három verse (Ézs 45:18, Ézs 24:10, Jób 26:7) nem előfordulás; a gate szerint az Ézs 45:18 a prózában Kontrasztként megjelenhet előfordulás-sor nélkül (ez `kapcsolatok.tsv`-sorként már bent van).
7. **2. szakasz szótári alapja** — a három előfordulás-sor BDB-mezői üresek és nincs `lexikon_hivatkozasok`-sor; a szótári idézet csak futtatott lekérdezés proveniencia-sorával kerülhet a prózába, különben explicit hiány. Adattábla nem bővül (brief 2. szakasz).
8. **7. lépés** — nem futott; a próza hiánymondattal zár (L5/Q5).

---

## ⛔ Megállás — döntési kérdések

A `DONTESEK.md` DT68 és DT69 tételei.

- **DT68 (1) — a próza helye:** javaslat: a `motivumok/TEREMT-002.md` (egy kézi forrás), alternatíva: külön tematikus tanulmányfájl.
- **DT68 (2) — a mérce:** javaslat: a DT2-mérce (L1, L3–L6 + rés-/hiányjelölés), az L1 átfordítva a tematikus sablon aktív szakaszaira; az L2/L7 helyén a Q2 és Q7 forrás-oldali megfelelője mérési pontként. Alternatívák: szó szerint L1, L3–L6 (a rés üres); vagy a teljes Q1–Q7 a forrásra, L-pontok a próbarenderre.
- **DT69 — az LXX-alap:** l. 5. pont, 1. tétel.
