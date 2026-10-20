---
feladat: 129
cim: A magyar BDB kiadása — rend, licenc, egységesítés, apparátus, generált kiadási nézet
kod: BDB_KIADAS
tipus: feladat
fazis: 2
munka: adat
modell: opus
allapot: nem_indult
ad: a magyar BDB kiadható alakban, generált nézetként az adatból (web, PDF, EPUB): gyök szerinti vagy Strong-rendben, Strong-mutatóval, magyar szómutatóval, rövidítésjegyzékkel és előszóval; a javítások az adatrétegben, a licenc a kiadás előtt rendezve; előtte egy próbakötet a kész szócikkekből
kovetkezo: "Te: az M0 ⛔ döntései (DT-F129a–e); a próbakötet (M1–M4) a #128 után indulhat, a teljes kiadás (M6) csak a #38 lezárása után"
olvas: [adat/forditasok.tsv, adat/terminologia.tsv, adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_forras_javitas.tsv, adat/bdb_vers_jelentes.tsv, adat/licencek.tsv, adat/SEMA.md, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_teljes_unabridged_README.md, konkordancia/OSHL_lexikalis_index.tsv, konkordancia/OSHL_lexikalis_index_README.md, konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/Karoli_1908.tsv, naplok/BDB_FORDITAS_gyokcsoportok.tsv, naplok/BDB_FORDITAS_naplo.md, naplok/BDB_FORDITAS_sorrend.tsv, naplok/F107_BDB_JELOLT_SZOVEG_naplo.md, eszkozok/bdb_jelolt/nezet_general.py, eszkozok/forditas_kapuk.py, eszkozok/normalizal.py, F38_BDB_FORDITAS_BRIEF.md, F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md, Rendszerfejlesztesi_playbook.md, LICENSE]
ir: [eszkozok/bdb_kiadas/, kiadas/bdb_hu/, adat/bdb_hu_javitas.tsv, adat/bdb_hu_szomutato.tsv, adat/SEMA.md, adat/licencek.tsv, naplok/F129_BDB_KIADAS_naplo.md, naplok/F129_BDB_KIADAS_lektor_minta.tsv]
fugg: [128]
nem_fugg: [7, 27, 36, 38, 67, 121]
---

# A magyar BDB kiadása (BDB_KIADAS)

*FELADATOK #129 (várható szám; a végleges a `/befogad`-nál dől el) · Modell: opus · v1 · 2026.10.20 · tervezet a
DT272 (2026-10-20) utáni chat-kérdésből („hogyan szerkeszthető egybe a magyar BDB kiadása”); a chatben javasolt irányról
a felhasználó még nem döntött, a döntéseket az M0 ⛔ viszi elé. Befogadás a `/befogad`-dal.*

## 1. Cél

A DT272 (felhasználó, 2026-10-20) szerint a BDB és a Thayer fordítása biztos, és a motívumblokk szótári gerince lesz. A magyar BDB
ezért nemcsak a motívumlap forrása, hanem önálló mű is: ez a feladat **kiadható alakra szerkeszti**.

Az alapelv a rendszer fő szabályából jön (`CLAUDE.md`; DT28): **a kiadás generált nézet az adatból.** Az adat a
`adat/forditasok.tsv` BDB-sora (és a szakaszonkénti útvonalon a #128 kulcsa), a szakasztábla (`adat/bdb_szakaszok.tsv`, SEMA 2.30) és a
javítótáblák. Ami a kiadásban hibás, az az adatban javul, és a kiadás újragenerálódik. A kiadási fájlt (HTML, PDF, EPUB) kézzel szerkeszteni
tilos; a fejlécében `GENERÁLT:` jelölés áll.

A feladat két részből áll:

- **próbakötet** a már kész szócikkekből (M1–M4): a rend, a tördelés, a javítási kör és az apparátus próbája, a teljes #38 előtt (ha a
  DT-F129d így dönt);
- **teljes kiadás** (M6), miután a #38 mind a 8 090 szócikket lefordította, és nincs angolul maradt szócikk.

## 2. Hatókör

**Benne van:** a kiadás rendjének, licencének és igehely-formájának döntése; a szerkesztői egységesítés mérése és a javítások az adatba;
a kiadás előtti forrásjavítások átvétele (pe/mem, ψ-maradék, hivatkozás-javítások) a kiadási nézetbe; az apparátus (előszó, rövidítésjegyzék,
Strong-mutató, magyar szómutató); a kiadás generátora (web, PDF, EPUB) és a próbakötet.

**Nincs benne:**

- fordítás: új szócikk vagy újrafordítás a #38-é (a 98 elakadó Strong, N-F107b, is ott fordul újra);
- a szakaszonkénti fordítás eszközlánca (#128);
- a `konkordancia/BDB_teljes_unabridged.tsv` cseréje a nézetre (DT231 (d) külön feladata) — ez a feladat a TSV-t nem írja;
- a Thayer kiadása (ha kell, saját feladat ugyanezzel a mintával);
- a motívumlap és a lexikon (#36, #121, #127): ezek a fordítást a saját nézetükben olvassák, a kiadás nem az ő forrásuk;
- a kiadás nyilvános közzététele, feltöltése vagy terjesztése: az a felhasználó külön lépése, a licenc rendezése után.

## 3. Kiinduló állapot (mérve)

*Proveniencia: scope=adat/forditasok.tsv BDB-sorai; adat/terminologia.tsv; adat/bdb_vers_jelentes.tsv (szurt≠1); konkordancia/BDB_teljes_unabridged.tsv
| forras=egyszeri, csak olvasó számláló szkript a repón kívül (split('\t'), a `#` sorok kihagyva) | ts=2026-10-20 16:48.*

| | Érték |
|---|---|
| BDB-szócikk a forrásban (`BDB_teljes_unabridged.tsv` adatsor) | 8 099 (a #38 8 090-et számol; a 9 JSON-kulcs nélküli sor, F57/F72, SEMA 2.30) |
| kész magyar szócikk (`jelentes_szam = teljes`) | **674 Strong**, 2 899 919 karakter magyar szöveg |
| ebből a #28 (Opus) | 26 (`kezi` 6, `opus` 20), `terminologia_verzio = v1` |
| ebből a #38 (Sonnet) | 648 (`sonnet`, `claude-sonnet-5-5`), `terminologia_verzio = v3` |
| nem `teljes` BDB-sor (jelentéspont-szintű, #28-előzmény) | 4 (`kezi`, `v1`) |
| `(fordításra vár)` a BDB-sorokban | 0 |
| a terminológia verziói a táblában | v1 13 sor, v2 3, v3 55 |
| BDB-igehely (nem szűrt) | 160 088; ebből **9 351 (5,8%)** Károli-verse eltér az MT-verstől, 774-nek nincs Károli-verse (`nem_letezo_vers` 485, `nincs_karoli` 201, egyéb) |
| BDB-gyökcsoport (OSHL `bdb_id` első két tagja) | 7 990 héber Strongon mérve, 2 275 gyökcsoport (`naplok/BDB_FORDITAS_naplo.md`, M0 5. pont; `naplok/BDB_FORDITAS_gyokcsoportok.tsv`) |

A terminológia tehát **két verzióval** készült (v1: a #28 26 szócikke; v3: a #38), a fordítás két modellel (Opus, Sonnet) és két prompttal
(a #28 prompt v4-e mindkettőnél; a #128 után a v5 jön). Az egységesítés (M2) ennek az eltérésnek a mérése és javítása.

## 4. Lépések (⛔ a kötelező megállások)

### M0 — felmérés és ⛔ döntések (csak olvas)

Az első lépés a modell-ellenőrzés (`CLAUDE.md`). Utána a menet felméri az alábbiakat, és a `DONTESEK.md`-be helyőrzős tételként
(`DT-F129a` …) viszi a felhasználó elé, opciókkal és javaslattal. A döntésig kódírás nincs.

#### ⛔ DT-F129a — a kiadás rendje és a gyökcsoport forrása

**Kérdés.** Milyen rendben álljanak a szócikkek?

- **(a) gyök szerinti főrend, ahogy az eredeti BDB** (gyök, alatta a származékai), **Strong-mutatóval** a kötet végén. A rend kulcsa az
  OSHL `bdb_id` (pl. `a.ac.aa`: első két tagja a gyökcsoport, a teljes az eredeti BDB-sorrend). Forrás: `openscriptures/HebrewLexicon`
  `LexicalIndex.xml`, commit `21c9add1`, **CC BY 4.0**, a repóban kivonatként (`konkordancia/OSHL_lexikalis_index.tsv`, `adat/licencek.tsv`
  OSHL sor); a kiadásban kötelező a megjelölés: „Open Scriptures Hebrew Bible Project”. A `BDB.lexicon` `BDB<n>` azonosítója (a
  szakasztábla `bdb_id`-je) **nem** lehet a rend kulcsa a kiadásban: a lexikon licence tisztázatlan (`lexikonok_nyers` sor), és a DT225 (c)
  szerint csak azonosítót és szerkezeti metaadatot ad, belső használatra.
- **(b) Strong-sorrend** (H0001 → H8674), gyökmutatóval vagy anélkül. Egyszerű, a Strong-számmal kereső olvasónak kényelmes, de a BDB
  szerkezetét (a gyök alá rendelt származékok, a kereszthivatkozó „see” sorok) szétszedi.
- **(c) kettős kimenet:** a nyomtatott/PDF kötet gyökrendben, a web Strong-sorrendben, kölcsönös mutatóval (ugyanabból az adatból két nézet).

**Mérendő az M0-ban:** hány kész és hány összes Strong kap OSHL `bdb_id`-t; hány Strong több `bdb_id`-n osztozik (egy Strong több
szócikkben — SEMA 2.30 `szocikk_resze` 30), és hány `bdb_id` több Strongon (az eredeti BDB egy szócikke több Strong); ezek hová kerülnek a
gyökrendben; a `bdb_id` nélküli Strongok (az OSHL-index `etym_tipus = —` sorai) helye.

**Javaslat: (a).** A BDB mint mű gyökrendű; a magyar kiadás ettől a fordítás hűségében is függ (a szócikkek egymásra hivatkoznak a gyökön
belül). A rend kulcsa a CC BY 4.0 OSHL-index, megjelöléssel; a Strong-mutató a hiányt pótolja. A DT52 (c) / N53 (a gyökcsoport mint „rokon
szavak” adat) ettől független marad: itt a gyökcsoport csak rendező kulcs, nem új szócikk-adat.

#### ⛔ DT-F129b — licenc a kiadás előtt

**A helyzet** (`adat/licencek.tsv` BDB sor; DT-F33g; DT225 (i)): a BDB (1906) **szövege a mű kora miatt közkincs**. A digitalizálási réteg
(Tim Morton / Bible Analyzer átirata, Stephen Ku és társai hivatkozás-elemzése, Eliran Wong javítása és formázása; `eliranwong/unabridged-BDB-Hebrew-lexicon`
@ `6e8326c6`, `DictBDB.json`) licence **tisztázatlan**: a README „Public domain document” mondata a digitális kiadás készítőjének
besorolása, nem a jogtulajdonos licencnyilatkozata a saját formázási rétegére, és a repóban LICENSE-fájl nincs (F33/DT-F33c). A sor már
rögzíti: „a kiadás előtt az eliranwong-repó LICENSE-ét idézni kell”. Ehhez jön: a repó saját adatrétege (benne az `adat/forditasok.tsv`, a
magyar fordítás) a `LICENSE` szerint „minden jog fenntartva” (`projekt_adat` sor, DT131).

**Kérdés.** Mi kell a kiadás előtt, és milyen licenccel jelenik meg a magyar szöveg?

- **(a) nyilatkozat kérése:** Eliran Wongtól (és rajta át Tim Mortontól / a Bible Analyzertől) írásos, projektre szóló nyilatkozat a
  digitális rétegről; a válasz szó szerint a `licencek.tsv`-be (playbook 2. pont: „© védett, engedély nélkül/bizonytalan → felfüggesztve”).
- **(b) a közkincs műre támaszkodó kiadás igazolással:** szúrópróbás összevetés a nyomtatott 1906-os kiadás nyilvános szkennelt példányával
  (pl. 50 szócikk, rétegzett minta), hogy a fordítás tárgya a mű szövege, nem a digitális réteg saját hozzáadása; a digitális réteg saját
  elemei (pl. a `_N` gyakoriságszám-jelölés, a hivatkozás-normalizálás, a formázás) a kiadásból kimaradnak vagy saját alakban jelennek
  meg. A mérés a naplóba, proveniencia-sorral.
- **(c) a kiadás belső marad**, amíg az (a) vagy a (b) nem zárul: a próbakötet készülhet, közzététel nincs.

**Alkérdés — a magyar szöveg licence:** (1) „minden jog fenntartva” (a `LICENSE` mai állása) · (2) nyílt licenc (pl. CC BY 4.0 vagy
CC BY-SA 4.0) a kiadásra · (3) később dönt. Ha a kiadás OSHL-adatot használ (DT-F129a (a)), a CC BY 4.0 megjelölése minden opcióban kötelező.

**Javaslat: (c) most, párhuzamosan (a) és (b);** a teljes kiadás (M6) közzététele csak (a) vagy (b) lezárása után. Az alkérdés a
felhasználóé, javaslat nélkül (a projekt licencpolitikája, DT116/DT131).

#### ⛔ DT-F129c — az igehely-forma a kiadásban

**A helyzet.** A BDB az MT számozását követi; a magyar olvasó a Károlit üti fel. A `adat/bdb_vers_jelentes.tsv` (SEMA 2.29) minden
hivatkozásra megadja az `mt_vers`-t és a `karoli_vers`-t; a mért eltérés 9 351 / 160 088 hely (5,8%), Károli-vers nélkül 774 (l. 3.).
**Mérendő az M0-ban:** a magyar fordítás szövegében ma milyen alakban állnak az igehelyek (magyar könyvrövidítés + MT-vers, ahogy a
forrás, vagy már átkulcsolva), és a `bdb_vers_jelentes.tsv` sorai a magyar szöveg igehelyeihez egyértelműen illeszthetők-e
(`strong` + `sorszam`, a `poz` az angol szövegben áll).

- **(a) Károli-hely elöl, eltérésnél az MT zárójelben:** „Zsolt 51:3 (MT 51:4)”; ahol nincs Károli-vers, az MT-vers áll, jelölve
  („MT 3:24, Károliban nincs”). A forrás a `karoli_vers`; a `vers_feloldas = atkulcsolt_bizonytalan` sorok külön listán, a kiadásban az
  MT-alak.
- **(b) MT-hely (ahogy a BDB), az előszóban magyarázattal**, és egy átszámozási táblázat a függelékben.
- **(c) MT-hely, eltérésnél a Károli zárójelben:** „Zsolt 51:4 (K 51:3)”.

**Javaslat: (a)** — a kiadás magyar olvasónak készül, az eltérés kis arányú, és az MT-alak nem vész el. A csere a generátorban történik
(nézet), a `forditasok.tsv` szövegét nem írja át.

#### ⛔ DT-F129d — próbakötet a teljes #38 előtt

**Kérdés.** Készüljön-e próbakötet a kész szócikkekből (`forditasok.tsv` `teljes` BDB-sorai: ma 674), mielőtt a #38 végigér?

- **(a) igen, a teljes 674-ből** (2,9 millió karakter; kb. a teljes BDB 8%-a): a generátor, a tördelés, a javítási kör és az apparátus
  teljes próbája.
- **(b) igen, egy szűkebb, gyökrendben összefüggő szeletből:** a kész szócikkek közül azok a gyökcsoportok, amelyeknek minden tagja kész
  (az M0 méri, hány ilyen van), plusz a DT272 arany motívumának szavai (H7121, H8034) — így a gyökrend próbája hézag nélküli.
- **(c) nem;** a kiadás a #38 lezárása után egyben készül.

**Javaslat: (b), majd (a)** — a gyökrend hézagos szeleteken nem ítélhető meg, a teljes 674 viszont a javítási kör (M3) mérésére kell. A
próbakötet nem nyilvános (DT-F129b).

#### ⛔ DT-F129e — hová kerül a szerkesztői javítás

**A helyzet.** A javítás az adatba megy (DT28), de az `adat/forditasok.tsv`-t a #38 írja, adagonként; egy közben beírt szerkesztői javítás
ütközne vele, és a `forras_hash`-hez kötött soron nem látszana, mi a fordítás és mi a javítás.

- **(a) külön javítótábla** (`adat/bdb_hu_javitas.tsv`, új SEMA-szakasz; a `bdb_forras_javitas.tsv`, 2.31, mintájára): kulcs `strong` +
  szakasz (a #128 döntött kulcsa szerint) + előfordulás, `eredeti` / `javitott` alak, `osztaly` (terminológia, rövidítés, törzsnév,
  helyesírás, félrefordítás), `indok`, `proveniencia`; a kiadási nézet a fordítás + a javítótábla. A #38 nem érintett.
- **(b) közvetlenül az `adat/forditasok.tsv`-be,** a #38 megállási pontjain, egyeztetve (a sor `allapot`-ja `kezi`-re vált, a `megjegyzes`
  rögzíti).

**Javaslat: (a)** — a #38 alatt is fut, visszakereshető, és a gépi és kézi réteg külön marad. A félrefordítás-osztályú javítás (ha a
szakasz értelme hibás) a #38-hoz megy újrafordításra, nem a javítótáblába.

**⛔ M0:** a felhasználó dönt a DT-F129a–e-ről. A menet commitolja a `DONTESEK.md` tételeit és a naplót, és megáll.

### M1 — a kiadási nézet generátora (a próbakötet alapja)

`eszkozok/bdb_kiadas/` (a pontos fájlnevek az M0 után): a bemenet a `forditasok.tsv` BDB-sorai (a #128 szakaszkulcsával és a régi `teljes`
útvonallal is), a szakasztábla, a `bdb_hu_javitas.tsv` (DT-F129e (a) esetén), a `bdb_vers_jelentes.tsv` (DT-F129c) és az OSHL-index
(DT-F129a). Kimenet egy köztes, formátumfüggetlen nézet (szócikkenként: címszó, rend-kulcs, szakaszok, igehelyek), amelyből az M5 a
formátumokat készíti. Determinisztikus, `--ellenoriz`-zel, teszttel; a kimenet első sora `# GENERÁLT: …`, a második a bemenetek és a kód
hash-e (a SEMA 2.29–2.32 mintája).

### M2 — szerkesztői egységesítés (mérés, majd javítás)

1. **Terminológia.** A v1-es (a #28 26 szócikke) és a v3-as szócikkek összevetése a `terminologia.tsv` v3 soraival: hány v1-es szócikk
   használ a v3-tól eltérő alakot (kulcsonként, a `forditas_kapuk.py` 5. kapujának logikájával, futtatva, nem újraírva). A javítás a
   DT-F129e szerint.
2. **Modellstílus.** A #28 (Opus) és a #38 (Sonnet) szócikkei közti rendszeres eltérések (szórend, igeidő, a „vö.” / „ld.” / „lásd”
   típusú rövidítések, a nyelvtani szakszavak) mérése egy rétegzett mintán; amit a terminológia nem fed, az javaslat a
   `terminologia.tsv`-be — jóváhagyással, és **csak a #38 megállási pontján** (F38: „a prompt és a terminológia futás közben nem változik”).
3. **Rövidítések és könyvnevek:** a `Konyv_normalizalo_tabla.tsv` szerint (Siralmak = JSir; a „Sir” csak Sirák fia); a maradék angol
   könyvrövidítés listája.
4. **Törzsnevek** (Qal, Niph'al, Pi'el …): egy alak a teljes kötetben; a mai alakok számlálása, a kanonikus alak a #107 illesztőjének
   kulcsa (`Hithpa'el`, `Pe'al`) vagy a felhasználó döntése.
5. **Lektorálási mintavétel.** Rétegzett minta (hossz, gyakoriság, modell, terminológia-verzió szerint; a méretet az M0 javasolja, pl. 40
   szócikk) a `naplok/F129_BDB_KIADAS_lektor_minta.tsv`-be: Strong, réteg, forrás és fordítás egymás mellett, a lektor ítélete
   (`rendben` / `javitando` / `ujraforditando`) és megjegyzése. A lektor a felhasználó (vagy általa kijelölt személy); a menet nem lektorál
   helyette, csak előkészít és összesít. Az arány (hány szócikket olvasott ember) az előszóba kerül (M4).

**⛔ M2:** a felhasználó jóváhagyja a javítási listát (osztályonként) és a lektorálási mintát; a javítások csak utána kerülnek a táblába.

### M3 — kiadás előtti forrásjavítások a nézetben

A kiadás nem viheti tovább a forrás ismert hibáit. Mindegyik a kiadási nézetben javul (vagy jelölődik), a `forditasok.tsv` és a TSV nem íródik:

1. **pe/mem (N-F107a, DT269 (1)):** a kész magyar szöveg héber idézeteiben a dagesses mem → pe csere a `bdb_forras_javitas.tsv` `pe_mem` /
   `javitva` soraiból. Ha a DT231 (d) TSV-csere-feladata addigra a kész fordításokra is elvégezte, ez a lépés csak ellenőriz (0 maradék).
2. **ψ-maradék (DT-F34b):** a B/R maradék (N-F34) helyei a kiadásban; a nem igazolt helyek jelölve vagy javítva, a N-F34 kézi nézetének
   állása szerint. Mérendő: hány maradék hely esik kész szócikkbe.
3. **Hivatkozás-javítások:** a `bdb_forras_javitas.tsv` `hivatkozas` sorai (F34/F46) és a `kezi` szerkezeti sorai; ellenőrzés, hogy a
   magyar szövegben a javított alak áll.
4. **Elakadó szakaszok (N-F107b):** ha a kiadás szakaszolt (DT-F129a gyökrend és tagolt tördelés), a 98 Strong a #38 újrafordítása előtt
   szakaszhatár nélkül marad; a próbakötetben jelölve, a teljes kiadás előfeltétele a #38-beli újrafordítás.
5. **Konverziós maradványok:** a `_N` tapadt gyakoriságszám (`2_46`, `3_39`) és a „2 145:törzs” (H7626) típusú forráshiba (F38 ⛔ Mj
   lelete): mérés és a kiadási alak (pl. felső index).

Minden lépés eredménye a naplóba, proveniencia-sorral (`scope=… | forras=… | ts=…`).

### M4 — apparátus és próbakötet

1. **Előszó:** a mű és a fordítás története; **a gépi fordítás aránya** (hány szócikk Opus, hány Sonnet, hány `kezi`), **a lektorálás aránya**
   (az M2 5. mintája és az azon túl olvasott szócikkek), a kapuk és a normalizáló szerepe egy bekezdésben; a forrás és a licenc
   (DT-F129b); az igehely-forma (DT-F129c). A számok a generátorból jönnek, nem kézzel írva.
2. **Rövidítésjegyzék:** a `terminologia.tsv` rövidítés-feloldásaiból és a `Konyv_normalizalo_tabla.tsv`-ből generálva.
3. **Strong-mutató:** Strong → címszó → hely a kötetben (DT-F129a (a) esetén kötelező).
4. **Magyar szómutató:** magyar szó → a szócikkek, amelyekben jelentésként áll. **Mérendő előbb:** kinyerhető-e a jelentés-glossza
   determinisztikusan a magyar szövegből (pl. a szakasz első kurzív / félkövér eleme a szakasztábla jelölői szerint), vagy kézi /
   modellkivonás kell; az utóbbi `adat/bdb_hu_szomutato.tsv`-be kerül (új SEMA-szakasz, `manual` vagy modell-proveniencia, a
   `jeloltek.tsv`-útvonal itt nem kell, mert nem study-adat). A DT272 (d) szerint a szómutató a **szóról** szól, nem a motívumról:
   motívumcímke nem kerül bele.
5. **Próbakötet** a DT-F129d szerint, a próbakimenet a repón kívülre vagy a `kiadas/bdb_hu/proba/` alá (az M0 dönti el, a `generalt_proba/`
   szabálya szerint: ami verziózott, nem törölhető).

**⛔ M4:** a felhasználó átnézi a próbakötetet; a visszajelzés javítás az adatban (M2/M3 körön át), nem a kimenetben.

### M5 — kimeneti formátumok (generált nézet)

1. **Web** (statikus HTML, szócikkenként horgonnyal; a meglévő olvasóval — `eszkozok/olvaso_szerver/` — összhangban, de nem annak része).
2. **PDF** (nyomdai tördelés; javaslat az M0-ban: HTML → PDF vagy LaTeX/XeLaTeX/ConTeXt; a választás a héber kezelésén múlik).
3. **EPUB** (EPUB 3, `dir="rtl"` a héber szakaszokon).
4. **Héber szedés:** RTL a vegyes irányú sorokban (bidi-izoláció a héber idézet körül), NFC/NFD egységesen, a nikkud és a kantilláció
   helyes megjelenése; tesztoldal a legnehezebb esetekkel (hosszú héber idézet magyar mondatban, szám a héber mellett).
5. **Betűtípus-licenc:** csak beágyazható, terjeszthető licencű betűtípus (pl. SIL OFL: Ezra SIL, Noto Serif Hebrew; a magyar szövegre
   OFL-es antikva). A választott betűtípus licence a `licencek.tsv`-be kerül, saját sorral. Az SBL Hebrew és hasonló, korlátozott EULA-jú
   betűtípusok csak a licencük ellenőrzése után.

### M6 — teljes kiadás és zárás

**Előfeltétel:** a #38 lezárva (mind a 8 090 szócikk `teljes` vagy szakaszolt magyar sora megvan), és **a kiadásban nincs
`(fordításra vár)` jelölés, sem angolul maradt szócikk** — a generátor ezt ellenőrzi, és piros esetén nem ad kimenetet. Ha a menet
indulásakor ez nem teljesül, a végrehajtó nem indul el, csak jelez (a `fugg` ezért csak a #128-at tartalmazza: a próbakötet a #38 alatt is
futhat; a teljes kiadás kapuja ez a pont).

1. A teljes kötet generálása mindhárom formátumban; az M2–M3 javítási kör a teljes anyagon (a #38 újabb adagjai miatt újramérve).
2. A DT-F129b közzétételi feltételének ellenőrzése; ha nem teljesül, a kiadás belső marad.
3. `adat/SEMA.md` (az új táblák), `adat/licencek.tsv` (betűtípus, a kiadás saját sora), napló, független ellenőr, draft PR.

## 5. Elfogadási feltételek

- A kiadás minden fájlja generált, `GENERÁLT:` fejléccel, és az adatból bájtra újraelőállítható (`--ellenoriz`).
- Kézi javítás csak az adatrétegben (DT-F129e szerinti helyen), proveniencia-sorral; a `forditasok.tsv`-t ez a feladat nem írja (DT-F129e
  (a) esetén), a `BDB_teljes_unabridged.tsv`-t semmiképp.
- A teljes kiadásban 0 `(fordításra vár)`, 0 angol szócikk, 0 maradék pe/mem (a javítótábla `javitva` sorai szerint), a ψ-maradék
  jelölve vagy javítva.
- Az előszó gépi- és lektorálási aránya a generátorból jön, és egyezik a `forditasok.tsv` / a lektori minta számaival.
- A licenc a közzététel előtt a DT-F129b szerint rendezve; a CC BY 4.0 megjelölések (OSHL, ha használt) a kiadásban állnak.
- Minden mérés mellett proveniencia-sor; TSV-olvasás `split('\t')`-vel, a `csv` modul nélkül; héber/magyar szöveget tartalmazó kód fájlból
  fut (`CLAUDE.md`).

## 6. Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | A kiadás generált nézet az adatból; javítás az adatba | DT28: a kereszthivatkozás és a fordítás adat, a kiadás nézet; így a #38 újabb adagjai újragenerálással jönnek be | a kiadás kézzel szerkesztett dokumentumként |
| D2 | Próbakötet és teljes kiadás egy feladatban, a teljes kiadás kapuja az M6 előfeltétele, nem a `fugg` | a próbakötet a #38 alatt is futhat; a `fugg: [38]` ezt blokkolná | két külön feladat (a befogadáskor választható, ha a felhasználó így kéri) |
| D3 | `modell: opus` | szerkesztői döntések, egységesítés és tördelési tervezés egy kézben (KONTEXTUS K1 szelleme); a generátor-kód mechanikus része csomagolható lenne, de a menet egyben marad | `sonnet` (a fordító modellje; a szerkesztő legyen más szem) |
| DT-F129a | 🟡 a kiadás rendje (gyök / Strong / kettős) | l. M0 | — |
| DT-F129b | 🟡 licenc a kiadás előtt, a magyar szöveg licence | l. M0 | — |
| DT-F129c | 🟡 igehely-forma (Károli elöl / MT / MT elöl) | l. M0 | — |
| DT-F129d | 🟡 próbakötet a #38 előtt (igen-teljes / igen-szelet / nem) | l. M0 | — |
| DT-F129e | 🟡 a szerkesztői javítás helye (javítótábla / `forditasok.tsv`) | l. M0 | — |
