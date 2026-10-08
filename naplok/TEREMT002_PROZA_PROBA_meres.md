# F64 M3 — TEREMT-002 próza-próba: mérés ⛔

*FELADATOK #64 · `F64_TEREMT002_PROZA_PROBA_BRIEF.md` 3. szakasz, M3 · ág `claude/f64-teremt002-proza-proba` · 2026.10.08 · mérce: DT-F64a (2) — L1–L7 + a DT2 két rés-szabálya*

**Mérés tárgya.** Forrásproza: `motivumok/TEREMT-002.md` (`0e36220` F64.5, `28ffd04` F64.8). Próbarender: `generalt_proba/TEREMT-002_proza_proba/` (`0f42ca9` F64.9). LXX-munkajegyzet: `naplok/TEREMT002_PROZA_PROBA_lxx_friss.md` (`ccd4b1d` F64.6).

Ez az író saját mérése, nem független ellenőrzés; a független ellenőr (M4) és a K1/4 (b) kimondása a felhasználóé.

**Számok** (saját szkript, `split('\t')`, a scratchpadban; a forrás-fájl az F64.18 utáni állapotban; frissítve F64.19):
`scope=motivumok/TEREMT-002.md | forras=manual (szöveg-számlálás: lábjegyzet, jelölő, NAPLO) | ts=2026-10-08`

| Mérőszám | Érték |
|---|---|
| proveniencia-lábjegyzet (definíció) / hivatkozás | 39 / 94; mind definiált és hivatkozott (F64.15 előtt 32 / 74, F64.18 előtt 39 / 87) |
| ebből friss `lekerdez.py`-futás | 27 (gerinc 1, kollokacio 8, scan 2, domen 2, lxx-hid 3, karoli 11; a P2 hét kollokáció-futása az F64.15-ben) |
| sorkivonat `split('\t')`-tel (nem `lekerdez.py`) | 5 (TAHOT 1, BDB 2, `forditasok.tsv` 2) |
| adattábla-olvasás / `manual` (T1-naplók) | 4 / 3 |
| `【NAPLO】` blokk | 13 (F64.12 előtt 10, F64.15 előtt 12) |
| `SZINT` / `INAKTÍV` / `ADAT-NÉZET` jelölő | 6 / 5 / 4 (sor eleji jelölő; a 7. sori NAPLO említését nem számolva — F64.16, ellenőri 9. pont) |
| archív blokk karakterre azonos | igen (3 blokk) |
| `【NAPLO` a próbarenderben | 0 |

## 1. Próbarender (M2)

`python eszkozok/general.py --cel <cél> --id TEREMT-002 --kimenet generalt_proba/TEREMT-002_proza_proba`, mind a hét célra; a generátor nem módosult, az éles fixpont (`--ellenoriz` naplo/index/nyitott) 0.

| Cél | Kimenet | Mi renderelődött | A prózából? |
|---|---|---|---|
| `naplo` | `motivumlog/PaRDeS_motivumok.md` | 4 marker-blokk (áttekintés, küszöb, kulcsszó-index, könyv-index) | **nem** — a `kuszob` blokk helyőrzőt ír: „a bekezdés-próza a G2 után a `motivumok/TEREMT-002.md`-ből fűződik ide” |
| `index` | `Lezart_tematikus_tanulmanyok_index.md` | a TEREMT-002 nem szerepel (nincs lezárt tanulmány) | — |
| `naplok` | `tematikus_lezart/naplok/TEREMT-002_kereszthivatkozas_naplo_GENERALT.md` + `naplok/F4_naplo_hianylista.tsv` | 66 jelölt, döntéssel és indoklással; kulcsszó csak `tohu+bohu` | **nem** — „Strong-lista és named-teacher gap-jelzés … a forrásrétegben él” |
| `study` | `tematikus_lezart/TEREMT-002_1_pont_GENERALT.md` | 1. pont, 7 oszlop, 3 sor; a BDB-oszlopok „—” | — |
| `nyitott` | `NYITOTT_FELADATOK.md` | a TEREMT-002 1 sorral | — |
| `lexikon` | — | **KIHAGYVA**: nincs `res_forras.tsv`-sor | — |
| `torzscikk` | — | **KIHAGYVA**: nincs lexikonoldal | — |

**Nem renderelt** (a teljes próza, szakaszonként): Kivonat; 1. pont P1–P7 (belso); 2. Eredeti nyelvi összevetés (a BDB-idézettel); 3. PaRDeS (Peshat, Remez, Drash, Sod, Vitatott pontok); 5. Alkalmazás; 7. Nyitott kérdések; Proveniencia-sorok; a 13 NAPLO-blokk és a 3 archív blokk. A mai `general.py` a `motivumok/[ID].md`-ből semmit nem olvas (M0 4. pont: a `forrasreteg_beolvaszthato_szakaszok()` hívatlan).

## 2. A mérce pontonként

| Pont | Forrásproza | Próbarender |
|---|---|---|
| **L1** szerkezeti teljesség | **teljesül** (átfordítva) | **nem** |
| **L2** napló-jelölés kötelező | **teljesül** (F64.12) | **részben** |
| **L3** lexikai vs. tematikus | **teljesül** | **részben** |
| **L4** kereszt-motívum szennyeződés | **teljesül** | **teljesül** |
| **L5** nevesített tanítói szakasz | **teljesül** (hiányjelzéssel) | nem alkalmazható |
| **L6** a)–f) fegyelem | **teljesül** | **részben** |
| **L7** PaRDeS-rétegfegyelem | **teljesül** | nem alkalmazható |
| **DT2/1** minden rés kitöltött vagy explicit hiány | **teljesül** | **részben** |
| **DT2/2** adatból generált rész `adat`-forrás-jelölésű | **teljesül** | **teljesül** |

**L1.** *Forrás:* a 13-szakaszos TUDOMÁNYOS-lista a lapra szól (M0 3. pont); átfordítva a tematikus sablon aktív `kezi_forras` szakaszai mind jelen vannak (Kivonat, 2., 3. a négy réteggel és a Vitatott pontokkal, 5., 7.), az inaktívak `INAKTÍV`-jelölővel, üres cím nélkül, az `adat` szakaszok `ADAT-NÉZET`-jelölővel. *Render:* lexikonoldal nincs, a 13 szakasz nem ellenőrizhető; a próza egyetlen szakasza sem jelenik meg.

**L2.** *Forrás:* **teljesül (F64.12).** Minden dátum-, eredet-, döntés- és folyamat-megjegyzés NAPLO-blokkban áll, prózai mondatba ágyazva nem. Az F64.12 a 7. pont és a P3 hat folyamat-/állapotmondatát (rögzítés a #12b-nél, gépi fordítás és forrásfájl, scan-hatókör, „önálló menet”, a régi kifejezés más fájlokban) két új NAPLO-blokkba emelte; a tartalmi mondatban csak a hiány ténye maradt („explicit hiány”). *Az F64.12 előtti ítélet (részben) indoka:*  a 7. pont (Nyitott kérdések) tételei természetüknél fogva adatállapotot írnak le tartalmi mondatban („fordítói döntésként nincs rögzítve”, „magyar fordítása gépi”), és a P1–P7 (belso) egy mondata a TAHOT-rés hatását írja („ennyivel gyengíti a »teljes« jelzőt”). A sablon nem mondja meg, hogy a módszertan-/nyitott-kérdés-rés ilyen állapotmondatai tartalomnak vagy naplónak számítanak — #23 M1-kérdés. *Render:* 0 NAPLO; a `kuszob` blokk helyőrző-sora („a bekezdés-próza a G2 után … fűződik ide”) folyamatjelzés a nyilvános nézetben.

**L3.** *Forrás:* az Ézs 45:18 és az Ézs 24:10 „a formula szempontjából tematikus, nem lexikai” jelölést kap (a versben a *tohu* áll, a pár nem), a 2Kir 21:13 / JSir 2:8 mérőkötél-képe „tematikus, nem lexikai”. *Render:* a kapcsolat-nézet nem renderelődik (a lexikonoldal hiányzik), a kereszthivatkozás-napló az elutasítást indoklással hozza, de a „tematikus, nem lexikai” címke nem jelenik meg.

**L4.** *Forrás:* a TEREMT-001-gyel közös 1Móz 1:2-n az elhatárolás explicit (3. pont Remez, „Elhatárolás”); a *tehóm*-mondatrész a Peshatból kikerült; az LXX ἀβύσσου (G0012) kifejezetten kizárva. A régi „teremtés-visszavonás” kifejezés (N25) csak az archív blokkokban és egy idéző nyitott-kérdés tételben áll. *Render:* csak TEREMT-002-adat.

**L5.** *Forrás:* a 7. lépés nem futott; a hiány az 5. pont INAKTÍV-jelölőjében, egy NAPLO-ban és a 7. pont 6. tételében explicit (Q5-alak). *Render:* lap nincs.

**L6 a)–f).** *Forrás:* (a) tartalmi mondatban/cellában dátum nincs; a ts-ek a proveniencia-lábjegyzetekben (ISTENTISZT-001-minta) és a NAPLO-kban állnak; (b) „Forrás:” sor nincs; (c) első személyű ellenőrzési állítás nincs; (d) minden NAPLO előtt üres sor; (e) blockquote csak héber szöveg, a magyar Károli-fordítás utána normál bekezdés; (f) „mi”-hang nincs (a szkript egyetlen találata a „mi a tét” kérdőszó). *Render:* részben, l. L2 (helyőrző-sor).

**L7.** *Forrás:* a Drash a lakhatóság-célt (Ézs 45:18) „(Remez-szintű kiegészítés, l. 3. pont, Remez: Ézs 45:18)” kereszthivatkozással veszi át; a TSK-szavazatok és a kapcsolat-típusok (Kontraszt/Párhuzam) csak a Remezben állnak. Az F64.15/F64.18 óta a Vitatott pontok a `kapcsolatok.tsv` irányára nem hivatkozik bizonyítékként (a :132 NAPLO szerint az irány nem szöveg-adat); a Remez, a Drash és az Alkalmazás olvasatfüggő mondatai feltételes jelölést kaptak. A Vitatott pontok nem PaRDeS-réteg; a határ a sablonban nincs kimondva.

**DT2/1.** *Forrás:* minden sablonszakasz vagy kitöltött, vagy `INAKTÍV`/`ADAT-NÉZET`-jelölésű, és minden tartalmi hiány NAPLO-ban explicit (vitatott pont képviselői, nevesített tanító, BDB-mezők, Ézs 34:11 Károli-KH). *Render:* a lexikon-rések nem jönnek létre (kihagyott cél), a küszöb-blokkban helyőrző áll.

**DT2/2.** *Forrás:* az `ADAT-NÉZET`-jelölők megnevezik a táblát és a célt. *Render:* minden blokk `GENERÁLT-KEZDET … | forrás: …` fejlécű.

## 3. A #23 M1-nek

**Szakaszonként** (kézi = a forrásban próza; adat = táblából generálható; hiány = a sablonból hiányzott):

| Szakasz | Hogyan működött | Megjegyzés |
|---|---|---|
| Kivonat | kézi | két bekezdés, 10 lábjegyzet-hivatkozás; számai (3 vers, 19/16 *tohu*-vers) lekérdezésből — adatból is generálhatók volnának |
| 0. Forrás-összegyűjtés | inaktív | natív motívum; a jelölő elég |
| 1. P1–P7 | kézi (belso) a P2-n, a többi adatból megismételve | a P1/P3–P6 eredményei a próza és az `auditok.tsv` között duplikálódnak; generált nézet lehetne, a P2 indoklása maradjon kézi |
| 1. tábla | adat | renderelhető (`study`), BDB-oszlopok „—” |
| Logikai kötőszó | inaktív | |
| 2. Eredeti nyelvi összevetés | kézi + szótári idézet | a héber alakok és a kiejtés TAHOT-ból; a BDB-idézet és a magyar fordítás a szótárfájlból — a leképezés szerint `adat` (`lexikon_hivatkozasok`), itt mégis a prózába került, mert a bekötés hiányzik; mezőhatár itt kellene |
| 2/b | inaktív | |
| 3. Peshat/Remez/Drash/Sod | kézi | a próza-elsőbbség itt működött a legjobban: az igeidézetek lábjegyzettel, mezőhatár nélkül |
| 3. ⚠️ Vitatott pontok | kézi, értelmezői aktiválással | az aktiválási feltétel („tudományosan vitatott”) a prózaíróra bízott — l. 5. szakasz |
| 4. Kutatási sablon | inaktív, értelmezői döntéssel | l. 5. szakasz |
| 5. Alkalmazás | kézi | |
| 5. Nevesített tanító | inaktív + hiánymondat | a hiánymondat helye (NAPLO vagy tartalom) nem egyértelmű; most mindkettő |
| 6. Napló-frissítés | adat | jelölő |
| 7. Nyitott kérdések | kézi (apparatus) | **a tematikus sablonból hiányzik**; a lexikonoldal `modszertan` résének kézi része |
| Proveniencia-sorok | kézi | **a sablonból hiányzik**; lábjegyzet-alak (ISTENTISZT-001) |
| Archív blokkok | belso | a sablon nem ismeri; a #11 dönt a sorsukról |

**Fő tanulságok:**
1. **Renderút nincs.** A B-szerkezethez a generátornak olvasnia kell a forrásprózát, szintszűréssel (`olvasoi` / `apparatus` / `belso`); ma a próza 100%-a „nem renderelt”. Ez a #23 M1 legfontosabb bemenete.
2. **A jelölők ideiglenes alakja** (`<!-- SZINT: … -->` a következő jelölőig, `<!-- INAKTÍV: ok -->`, `<!-- ADAT-NÉZET: forrás | cél -->`) írás közben kezelhető volt. A szint hatóköre (jelölőtől jelölőig, vagy címsorig) azonban nincs kimondva, és a NAPLO-blokkok `belso` szintje implicit (az `olvasoi` szakaszon belül is). Javaslat: a forrássablon mondja ki mindkettőt.
3. **Próza-elsőbbség (K1/2).** Az érvelés (3., 5. pont) mezőhatár nélkül, lábjegyzetes provenienciával jól működött. Mezőhatár három helyen hiányzott: a szótári idézet (BDB/fordítás → `lexikon_hivatkozasok`), az LXX-megfelelők (→ `lxx_dontesek`) és az adatból számolt számok (a prózában ismételt n-értékek elcsúszhatnak a táblától). Javaslat: „adatból számolt érték”-jelölő, amelyet a generátor ellenőrizhet.
4. **Sablonrés:** a tematikus sablonból hiányzik a Nyitott kérdések / Módszertan szakasz és a Proveniencia-szakasz; a Vitatott pontok és a 4. pont aktiválási feltétele értelmezői ítélet, gépi feltétel nélkül.

## 4. A #12b-nek

- **„Függő (#12b)” LXX-helyek:** 1Móz 1:2 (ἀόρατος καὶ ἀκατασκεύαστος), Jer 4:23 (οὐθέν), Ézs 34:11 (σπαρτίον γεωμετρίας ἐρήμου; a *bohu*-kövek görög megfelelő nélkül); `lxx_dontesek.tsv`-sor nincs. A régi 58 `lxx-hid` audit-sor kivezetett forrásra mutat; a három előfordulás-vers sorai a friss futással újraírandók (`naplok/TEREMT002_PROZA_PROBA_lxx_friss.md`). Az ἀκατασκεύαστος az LXX_OS-ben Strong-szám nélkül áll.
- **BDB-mezők:** a három előfordulás-sor `lexikon_entry_id`, `jelentes_szam`, `jelentes_en`, `jelentes_hu` mezője üres (az 1. tábla „—”); a BDB-szócikk (H8414, H0922) és a gépi fordítás (`forditasok.tsv`, `allapot=opus`) megvan, csak a bekötés hiányzik.
- **`lexikon_hivatkozasok`:** H8414-re és H0922-re 0 sor; a lexikonoldal 2. szakasza (Szótári háttér) erre épül.
- **A lexikonoldalhoz hiányzik még:** `res_forras.tsv`-sorok (a `lexikon` cél ezért hagyja ki); a rések forrásútja a `motivumok/TEREMT-002.md`-ből (a mai rés-mechanizmus tanulmányt vár); a 7. lépés (nevesített tanító); az Ézs 34:11 valódi Károli-kereszthivatkozásai (N22); a TEREMT-001 1Móz 1:2-sorának `funkcio`-ja (az L4-elhatárolás teljességéhez).

## 5. Átnézendő értelmezői döntések

1. **A Vitatott pontok aktívvá tétele.** Az M1 aktívnak vette, és eredetileg a kiinduló-állapot olvasat mellett döntött. A felhasználó (a) döntése (2026-10-08) szerint a szakasz aktív marad, de nem dönt: az F64.15/F64.18 óta mindkét olvasatot (kiinduló-állapot / restitúciós „hézag”) kiegyensúlyozottan mutatja be, a közös, nem különböztető tényeket (a BDB teljes keretezésével) külön blokkban, körkörös érv nélkül; az olvasatfüggő mondatok a próza többi részében feltételes jelölést kaptak (a1). Az olvasatok leírása emlékezetből származó értelmezés (`manual`; a „vala”/„lett” grammatikai kérdés lekérdezéssel nincs alátámasztva); a sablon szerint kötelező nevesített képviselők forrás híján hiányoznak. Alternatíva: a szakasz inaktív, és a kérdés a 7. pontba kerül.
2. **A 4. pont inaktiválása.** Indok: a repó adatában nincs dokumentált pünkösdi/karizmatikus szakirodalmi vonatkozás. Ezt az M1 nem kereste; az inaktiválás a „nincs adat” állapotot rögzíti, nem a „nincs vonatkozás” tényt.
3. **A BDB-fordítás nem független.** A `forditasok.tsv` H8414/H0922 sora `allapot=opus`, `modell=claude-opus-5-5`: ugyanaz a modell fordította, amely a prózát írta. Az idézett magyar szöveg tehát nem független megerősítés, és emberi lektorálása nem történt.

## 6. Kívül eső leletek (tétel nem nyílt)

1. **A BDB-forrás sérült héber idézetei** (`konkordancia/BDB_teljes_unabridged.tsv`, H8414 és H0922): fordított szórend és hibás maqqef-kötés (pl. `קַותֿֿהֹוּ` a קַו־תֹהוּ helyett; `וָבֹהוּ תֹּהוּ`; `בֹהוּ וְאַבְנֵי`). A próza ezekből nem idéz; a `forditasok.tsv` a sérült alakot viszi tovább.
2. **H8414 „49:19”:** a BDB-szócikk az Ézs 49:19-re hivatkozik, a *tohu*-vers viszont az Ézs 49:4 (`scan H8414`, 19 vers). Valószínű forrás- vagy átírási hiba; nem javítva.
3. **Az M0-pontosítás:** az M0 5. pontja mind az öt zsoltár-jelölt régi LXX-sorát az N17-eltolásra épülőnek írta; a `naplok/FORRASKIVEZETES_M5_eltereslista.tsv` szerint ez csak kettőre áll (Zsolt 80:6, 80:7 `zsoltar_eltolas`); a Zsolt 104:30 `strong_eltero`, a Zsolt 107:40 `nagy_eltero`, a Zsolt 33:6 azonos.

## 7. A mérce korlátja (felhasználó, 2026-10-08, chat)

Az aranyminta (ISTENTISZT-001) maga sem tartalmazza a szótári szerepmátrix (`adat/szotar_szerepek.tsv`, SEMA 2.13) minden elemét, és nem a mátrix szerint rendez: a `lexikon/ISTENTISZT-001_TUDOMANYOS.md` 2. szakasza Strong-számonként, azon belül forrásonként halad (TBESG, Thayer, BDB, LSJ), a 4. szerep (szemantikai domén) Strong-számonként a 2. szakaszban áll, az 5. és a 7. szerep csak a 2/b vegyes blokkjában; a héber 3. szerepből csak a TWOT-szám (hivatkozásként) szerepel; a 10. (kiejtés) csak részben (a 🇭🇺 sorokban); a 9. (versenkénti jelentés), a 12. (Nave) és a javasolt 13. (Károli-megfelelők) szerep hiányzik (F64.16, ellenőri 8. pont).
`scope=lexikon/ISTENTISZT-001_TUDOMANYOS.md címsorai + adat/szotar_szerepek.tsv | forras=manual (összevetés) | ts=2026-10-08`

Következmény: ez a mérés a próza értelmező részére érvényes (PaRDeS-rétegek, L1–L7 a forrásprózán); a szerepmátrix szerinti szótári rész **nincs mérve**, mert a mérce erre a részre hiányos. Az ISTENTISZT-001 rekonstrukciója a teljes szerepmátrix szerint külön feladat (befogadásra vár), a #23 M1, a #10 és a #11 mércéje az lesz. A felhasználó a #64 zárását ezzel a korláttal hagyta jóvá.

---

## ⛔ Megállás

A felhasználó átnézi a prózát (`motivumok/TEREMT-002.md`) és ezt a mérést; a K1/4 (b) teljesülését ő mondja ki. Ezután indulhat a #23 M1; az M4 (zárás, független ellenőr, PR) csak ezután.
