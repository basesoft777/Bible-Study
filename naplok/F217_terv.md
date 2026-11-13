# F217 — leltár és terv (a ⛔ előtti rész)

*FELADATOK #217 · `F217_GENERALAS_MAINEN_BRIEF.md` 2. pont 1–2. és a megvalósítás terve · végrehajtó: claude-opus-5-5 (kért: opus) · 2026-11-13 · alap: `cf68d0a9` (main)*

**Hatókör.** Ez a menet csak olvasott és mért. Generátorhoz, workflow-hoz és az E28-hoz nem nyúlt, mert a #709 (`claude/istentiszt-uj-cikk-992f57`, nyitott) még írja az `eszkozok/lexikon_general.py`-t és a lexikonfájlokat. A megvalósítás (3. pont) a #709 mergelése után indul, és az orkesztrátor átnézése után.

**Alap.** A bemeneti oldal a generátor-térkép specifikációja (`GENERATOR_TERKEP_SPEC_2026-11-13.md`, a megosztott jegyzetmappában), annak 2. pontja (B01–B64) és O2 kérdése. A bemeneteket ez a terv nem térképezi fel újra, csak hivatkozik rájuk. Ez a leltár a **kimenetekről** szól.

---

## 1. Leltár: generált kimenetek

### 1.1 Mit commitolnak ma az ágak (mérés)

Az utolsó 60 mergelt PR közül hány írta az ágán a generált útvonalat. A mérés az ág saját változásait nézi (`git diff <merge>^1...<merge>^2`, merge-bázistól), így a main-ről elmaradt fájlok nem számítanak bele.
*Proveniencia: `scope=git log origin/main --merges --first-parent -60 (2026-11-09 … 2026-11-13) | forras=cf68d0a9 | ts=2026-11-13`.*

| Útvonal | PR-ok (60-ból) | Megjegyzés |
|---|---|---|
| `nyilt_mag/` | 13 | export; az E35 kényszeríti a PR-ba |
| `lexikon/<ID>_TUDOMANYOS.md` | 13 | az E28 kényszeríti a PR-ba |
| `NYITOTT_FELADATOK.md` | 11 | egy része kézi sor, egy része a `nyitott` marker-blokk |
| `adat/bdb_vers_jelentes.tsv` | 7 | generált adat-pillanatkép, a lap **bemenete** (B19) |
| `lexikon/<ID>_KIZARASOK.md` | 3 | csak HAMART-001 (új szerkezet) |
| `motivumlog/PaRDeS_motivumok.md` | 3 | `naplo` marker-blokkok |
| `adat/bdb_szakasz_hu.tsv` | 3 | adat-pillanatkép, bemenet (B18) |
| `DONTESEK.md` | 3 | kézi sor (állapotváltás); nem generált nézet |
| `adat/thayer_vers_jelentes.tsv` | 2 | adat-pillanatkép, bemenet (B21) |
| `Lezart_tematikus_tanulmanyok_index.md` | 2 | `index` marker-blokk |
| `nyilt_karoli_strong/`, `nyilt_karoli_modern/` | 1–1 | kiadási csomag (Zenodo), saját exporttal |
| `naplok/F123_teljesseg_*`, `naplok/ALLITAS_HAMART-001.md`, `generalt/muhely/` | 1–1 | mérés-pillanatkép, napló, műhely-feed |

A `FELADATOK.md` generált blokkját, a `FELADATTERKEP.html`-t, a `GERINC_TERKEP`-et és az `ELOSZURES_*`-t ma már a main-en futó Action (`feladatok.yml`, F201) írja. Ezeket az ágak nem commitolják; a PR-ban a régi ág elmaradása látszik csak eltérésként.

**A torlódás forrása tehát három nézetcsoport:** a lexikonlap (TUDOMANYOS + KIZARASOK), a nyílt mag, és a három marker-blokkos nézet (napló, index, nyitott). Ezeket ma az E28 és az E35 a PR-ba kényszeríti, ezért a következő merge után minden más ágon elavulnak.

### 1.2 Nézetenként: író parancs, determinizmus, kapuk

A determinizmust két mérés igazolja, mindkettő a repón kívüli ideiglenes könyvtárba írt:
- `PARDES_DATUM=2026-11-12 general.py --cel lexikon --id HAMART-001` → a TUDOMANYOS és a KIZARASOK LF-re normálva **bájtra azonos** a commitolttal (51 s).
- `nyilt_mag_export.py --kimenet <tmp>` → `diff -rq` **0 eltérés** (11 s).
- Ugyanez más dátummal (`2026-11-05`): az eltérés **csak** a `ts=` és a „generálva:” dátum.

*Proveniencia: `scope=general.py --cel lexikon --id HAMART-001; nyilt_mag_export.py | forras=d9df4490 (= cf68d0a9 + fejléc) | ts=2026-11-13`.*

| Nézet | Író parancs | Determinizmus | Kapu, amely nézi |
|---|---|---|---|
| `lexikon/<ID>_TUDOMANYOS.md` (aktív: HAMART-001, ISTENTISZT-001) | `general.py --cel lexikon [--id ID] --ir` → `lexikon_general.run` | a bemenet és a `PARDES_DATUM` függvénye; dátum nélkül a mai nap (GK-B9) | **E28** (az `e28_migralt_nezetek.tsv` sorai: nulláról generált = commitolt, és helyben frissítő = nulláról generált); **E29** (kiadható kimenet tisztasága, ugyanaz a lista); **E35** kiváltója (`lexikon/*_TUDOMANYOS.md`); **E38** (`allitas_adat.py --minden`, a lemezen lévő lapot olvassa); **E39** (`kovetelmeny_kapu.py HAMART-001`, a lemezen lévő lapot olvassa); a generátor belső kapui (teljesség, `lxx_egyezes`, `hely_egyseg`, melléklet; csak új szerkezeten, l. térkép H8) |
| `lexikon/<ID>_KIZARASOK.md` (HAMART-001) | ugyanaz a hívás | ugyanaz („generálva: <dátum>” sor) | E38 (melléklet-rész); generátor `MellekletHiba` |
| `lexikon/<ID>_TORZSCIKK.md` | `general.py --cel torzscikk` → `torzscikk_general` (a TUDOMANYOS-t olvassa vissza) | a TUDOMANYOS-tól függ | E28 nem (nincs a listán); ma mind a 4 TORZSCIKK befagyasztott motívumé |
| `motivumlog/PaRDeS_motivumok.md` (`naplo#…`, 4 blokk) | `general.py --cel naplo --ir` | a törzs determinisztikus; a fejléc-marker `ts=` dátumfüggő, az E28 csak a törzset veti össze | E28 (1. ág, marker-blokkok) |
| `Lezart_tematikus_tanulmanyok_index.md` (`index`) | `general.py --cel index --ir` | ugyanaz | E28 |
| `NYITOTT_FELADATOK.md` (`nyitott` blokk) | `general.py --cel nyitott --ir` | ugyanaz | E28 |
| `nyilt_mag/` (30 fájl) | `nyilt_mag_export.py` | determinisztikus (mérve) | **E35** (kiváltó: `adat/*.tsv`, az export, `lexikon/*_TUDOMANYOS.md`) |
| `FELADATOK.md` (generált blokk), `FELADATTERKEP.html`, `feladatterkep.json` | `feladatok.py general`, `feladatterkep.py` | determinisztikus | E18 (a PR nem módosíthatja a generált blokkot); **már Action írja** |
| `naplok/GERINC_TERKEP.{tsv,md}`, `naplok/ELOSZURES_*.tsv` | `gerinc_terkep.py`, `jelolt_eloszures.py` | időbélyeg a git-ből (`gerinc_terkep.py:238`) | **már Action írja** (`feladatok.yml`, útvonal-kiváltóval) |
| `generalt/muhely/*.json` | `muhely_allapot.py` | **nem determinisztikus** (`datetime.now()`, `gh pr list`, mai dátum: 74., 687. sor) | nincs |

**Nem nézet, ezért a jegyzék G-sorai között nem szerepel** (bemenetként B-sor, vagy kimarad):
- **Generált adat-pillanatkép, a lap bemenete:** `adat/bdb_szakasz_hu.tsv` (B18), `bdb_vers_jelentes.tsv` (B19), `thayer_vers_jelentes.tsv` (B21), `naplok/F123_teljesseg_<ID>*.tsv` (B05/B06; író: `teljesseg_meres.py`). Ezek az ágon maradnak. A védelmük a frissességi kapu (térkép GK-03), nem az Action. Ha ezeket is a main-en generálnánk, a lap bemenete merge után változna.
- **Kiadási csomag:** `nyilt_karoli_strong/`, `nyilt_karoli_modern/` (`karoli_strong_export.py`, `karoli_modern_export.py`). Kiadáskor készülnek, nem merge-enként.
- **Napló, jelentés:** `naplok/ALLITAS_<ID>.md` (`proza_allitas.py`), a többi `naplok/` jelentés. Ezek mérés-pillanatképek.

### 1.3 Ami már ma is a main-en generál

A `feladatok.yml` (F201) a main-re érkező minden push után **egy futásban, egy commitban** fut le (`pardes-feladatok` App-token, `concurrency: feladatok-frissites`, `pull --rebase`). Lépései:
1. számkiosztás;
2. **csak kiosztás után** a `szamkiosztas_ujragen.py`, amely a három marker-blokkot, az `e28_migralt_nezetek.tsv` minden lapját (a lap saját `ts=` dátumával) és a nyílt magot generálja újra;
3. `FELADATOK.md` és feladattérkép;
4. GERINC_TERKEP és ELOSZURES, útvonal-kiváltóval;
5. egy gépi commit.

**Következmény a tervre:** az F217 Action-je nem új mechanizmus, hanem ennek a 2. lépésnek az általánosítása. A feltétel „csak kiosztás után” helyett „mindig” lesz, a lista pedig az `e28_migralt_nezetek.tsv` helyett a jegyzék. A `szamkiosztas_ujragen.py` ennek a kezdeti, kézzel kódolt változata.

### 1.4 Megőrzés: befagyasztott és kiadott lapok

- **Befagyasztott** (`adat/lap_befagyasztas.tsv`, DT816): KIRALY-001, TEREMT-001, ALVIL-001, MENNY-001, ANTROP-001, HODIT-001, TEREMT-002. A generátor kihagyja őket (`lexikon_general.py:9962`, „BEFAGYASZTVA”), és az E28 sem veti össze őket (`szabalyok.py:2239`). Ez ma is véd.
- **Kiadott** (`adat/kiadasok.tsv`): ISTENTISZT-001 (1. kiadás), HAMART-001 (2. kiadás). A befagyasztott ALVIL-001 és ANTROP-001 is kiadott. A két nem befagyasztott kiadott lapnál ma semmi nem tiltja, hogy egy adatváltozás után a generátor csendben új szöveget adjon. Ma ezt az E28 PR-beli kényszere teszi láthatóvá; az F217 után ezt a szerepet egy külön kapu veszi át (3.4).

### 1.5 Költség

A becsült költség a CI-ban (a mérésből, ×1,7 biztonsági szorzóval):
- egy aktív lap generálása kb. 50 s; az E28 ma lapnként kétszer generál (nulláról és helyben), két aktív lapnál ez kb. 200 s;
- a nyílt mag kb. 11 s;
- a teljes újragenerálás az Action-ben 2 aktív lapra kb. 2–3 perc, ×1,7-del kb. 5 perc.

Minden új, nem befagyasztott cikk lapnként kb. +50 s-ot ad (a PR-ban a helyben ág miatt +100 s-ot).

---

## 2. A jegyzék formátuma (`adat/generalt_nezetek.tsv`) — az O2 válasza

**Egy tábla köti össze a bemeneti jegyzéket és a kimeneteket.** Két sorfajtája van: a `tipus` mező `bemenet` (B-sor, a térkép 2. pontja) vagy `kimenet` (G-sor). A kimenet `bemenetek` mezője B-azonosítókra hivatkozik. A gépi kapu a hivatkozási épséget nézi: minden hivatkozott B-azonosító létezik.

**Oszlopok** (TSV, `split('\t')`, az első sor a fejléc; `#` kezdetű megjegyzéssor a fejléc előtt állhat, mint a `kiadasok.tsv`-ben):

| Oszlop | B-sor | G-sor | Érték |
|---|---|---|---|
| `id` | ✔ | ✔ | `^B\d{2,3}$` / `^G\d{2,3}$`; nem újrahasznosítható; a térkép B01–B64 számai változatlanok, az új bemenet B65-től kap számot |
| `tipus` | `bemenet` | `kimenet` | |
| `utvonal` | ✔ | ✔ | repó-relatív út vagy glob (`*`). Motívumhelyőrző: `<ID>`. Marker-blokk: `fájl#blokk` (pl. `NYITOTT_FELADATOK.md#nyitott`). Könyvtár: `/` a végén. Modul (B13, B61, B62): `modul:eszkozok/heber_kiejtes.py` |
| `leiras` | ✔ | ✔ | mit ad a lapnak (B), illetve milyen nézet (G) |
| `parancs` | – | ✔ | a teljes parancssor, `{gyoker}` helyőrzővel a kimeneti gyökérre (a main-en a repó, a PR-ban és átnézéskor ideiglenes könyvtár). Pl. `python eszkozok/general.py --cel lexikon --kimenet {gyoker}`. **Az új generátor csak ezt a mezőt cseréli** (brief 4. pont) |
| `bemenetek` | – | ✔ | B-azonosítók `;`-vel; tartomány `B01..B59`; kizárás `!B60` |
| `utana` | – | ✔ | G-azonosítók, amelyek előtte futnak (pl. TORZSCIKK a TUDOMANYOS után, nyílt mag a lap után) |
| `orzes` | – | ✔ | `szabad` / `befagyasztas` (a `lap_befagyasztas.tsv` ID-jét kihagyja) / `kiadas` (a kiadott lap tartalmi változása csak új kiadással, 3.4) |
| `determinizmus` | – | ✔ | `det` / `det:PARDES_DATUM` / `nemdet` |
| `kapuk` | – | ✔ | a nézetet olvasó kapuk, `;`-vel (pl. `E28;E29;E35;E38;E39`) |
| `gazda` | – | ✔ | `action` (a main-en az Action írja; az ág nem commitolja) / `ag` (az ág commitolja, az Action nem nyúl hozzá) |
| `allapot` | ✔ | ✔ | `aktiv` / `kimarad` (az ok a `leiras`-ban) |
| `hozzaferesi_pont` | ✔ | – | a térkép „helyes hozzáférési pont” oszlopa (az újraírás célja; ma dokumentáció) |
| `kockazat` | ✔ | – | M/H/E jelölés a térképből, `;`-vel |
| `forras` | ✔ | ✔ | proveniencia: a térkép pontja, vagy `manual` |

Az üres mezőben `-` áll, nem üres string, a `SEMA.md` szokása szerint.

**Kezdő G-sorok** (a B-sorok a térkép 2. pontjának 64 sora, változatlan számmal; a nem-lexikon nézetek bemenetei B65-től):

| id | utvonal | parancs (röviden) | bemenetek | utana | orzes | determinizmus | gazda | allapot |
|---|---|---|---|---|---|---|---|---|
| G01 | `lexikon/<ID>_TUDOMANYOS.md` | `general.py --cel lexikon` | `B01..B64;!B60` | – | `kiadas;befagyasztas` | `det:PARDES_DATUM` | `action` | `aktiv` |
| G02 | `lexikon/<ID>_KIZARASOK.md` | (a G01 hívása állítja elő) | `B03;B04;B05;B06;B07;B56;B62` | – | `kiadas;befagyasztas` | `det:PARDES_DATUM` | `action` | `aktiv` |
| G03 | `lexikon/<ID>_TORZSCIKK.md` | `general.py --cel torzscikk` | `G01` (a lap; térkép GK-20) | G01 | `befagyasztas` | `det:PARDES_DATUM` | `action` | `kimarad` (mind a 4 befagyasztott) |
| G04 | `motivumlog/PaRDeS_motivumok.md#naplo` | `general.py --cel naplo` | B02;B03;B04;B63 | – | `szabad` | `det` (törzs) | `action` | `aktiv` |
| G05 | `Lezart_tematikus_tanulmanyok_index.md#index` | `general.py --cel index` | ugyanaz | – | `szabad` | `det` (törzs) | `action` | `aktiv` |
| G06 | `NYITOTT_FELADATOK.md#nyitott` | `general.py --cel nyitott` | ugyanaz | – | `szabad` | `det` (törzs) | `action` | `aktiv` |
| G07 | `nyilt_mag/` | `nyilt_mag_export.py --kimenet {gyoker}/nyilt_mag` | `adat/*` táblák (B65…), G01 | G01 | `szabad` | `det` | `action` | `aktiv` |
| G08 | `FELADATOK.md#…`, `FELADATTERKEP.html`, `feladatterkep.json` | `feladatok.py general`; `feladatterkep.py` | `F*_BRIEF.md` (B-sor) | – | `szabad` | `det` | `action` | `aktiv` (ma is) |
| G09 | `naplok/GERINC_TERKEP.{tsv,md}` | `gerinc_terkep.py --kimenet {gyoker}/naplok` | (a `feladatok.yml` GERINC-regexe) | – | `szabad` | `det` | `action` | `aktiv` (ma is) |
| G10 | `naplok/ELOSZURES_*.tsv` | `jelolt_eloszures.py` | (az ELOSZ-regex) | – | `szabad` | `det` | `action` | `aktiv` (ma is) |
| G11 | `generalt/muhely/*.json` | `muhely_allapot.py` | – | G01 | `szabad` | `nemdet` | `ag` | `kimarad` (3.6) |

A G08–G10 sorai új működést nem hoznak. Azért kerülnek a jegyzékbe, hogy minden main-en generált nézet egy helyen álljon, és a G01 bemenetei között ne legyen rejtett nézet.

**Az `e28_migralt_nezetek.tsv` sorsa.** A jegyzék G01/G02 sora a mai lista utódja; a lista oszlopai (`id`, `fajl`, `cel`, `melyseg`) a jegyzékből és a `motivumok.tsv`-ből származtathatók. A régi lista nem marad párhuzamos forrásként (memória: „javítás új fájlként”). Minden fogyasztóját egy commitban kell átkötni, és a régi listát a kapunak tiltania kell. A fogyasztók:
- `eszkozok/ellenorzes/szabalyok.py` (E28, E29);
- `szamkiosztas_ujragen.py`;
- `torzscikk_general.py`;
- `lexikon_ket_ut_meres.py`;
- `teszt_torzscikk_migralt.py`;
- `ellenorzes/tesztek/test_szabalyok.py`.

A `datum` oszlopa ma senkinek nem bemenet: az E28 a lap `ts=`-éből olvas.

---

## 3. Terv (a ⛔ után, a #709 mergelése után)

A tételek sorrendben; mindegyik külön commit, tétel-azonosítóval.

**F217.2 — a jegyzék.** Az `adat/generalt_nezetek.tsv` a 2. pont szerint, a B-sorok a térkép 2. pontjából, `forras` mezővel. Mellé a `SEMA.md` bejegyzése és a gépi kapu:
- oszlopok, `tipus` szerinti kötelező mezők;
- id-formátum;
- hivatkozási épség;
- `utana`-körmentesség;
- `gazda=action` sor `parancs`-a futtatható szkriptre mutat.

A kapu a `futtat.py` új szabálya, helyőrző számmal; a SEMA 3.11 kapulistája generált.

**F217.3 — `eszkozok/generalt_nezetek.py`.** A jegyzék végrehajtója, a `szamkiosztas_ujragen.py` utódja; a régi szkript vékony hívássá válik, vagy archívumba megy. Módjai:
- `--lista`: a sorrend kiírása;
- `--ir`: a main-en, a repóba ír;
- `--gyoker DIR`: ideiglenes gyökér, a PR-ban és átnézéskor;
- `--jelentes`: mely nézet változott, és melyik őrzött nézet változna.

Az `utana` szerinti topologikus sorrendben fut. A `nemdet` és a `gazda=ag` sort nem futtatja. Hiba esetén nem nulla kóddal lép ki, és nem ír félig (előbb ideiglenes gyökérbe generál, csak siker után másol).

**F217.3a — a dátumszabály (GK-B9).** A generálás először a commitolt lap `ts=`-ével fut. Ha a kimenet a dátumsorokon kívül nem változik, a lap marad (nincs commit). Ha változik, a HEAD commit dátumával (UTC) fut újra, így az újrafuttatás is ugyanazt adja.

**F217.4 — `eszkozok/teszt_generalt_nezetek.py`.** Tesztesetek:
- jegyzék-kapu, pozitív és negatív esetekkel;
- sorrend;
- befagyasztott ID kimarad;
- kiadott lap változása;
- idempotencia (két futás, nincs diff);
- dátumszabály;
- a régi lista tiltása.

**F217.5 — az Action.** Ajánlás: a `feladatok.yml` 2. lépése bővül: a feltétel „csak kiosztás után” helyett „mindig”, a hívás `generalt_nezetek.py --ir`. Indoklás: az F201 egy futás, egy commit elve (DT-F201c), a meglévő `concurrency` csoport, és hogy két bot ne versengjen a main-ért. A brief `.github/workflows/generalt_nezetek.yml`-t ír; ez eltérés, l. O1.

Az újragenerálás után, a commit előtt az E29, E38 és E39 lefut a friss nézeten. Ha bukik, nincs commit, a futás piros, és a main-őr (`/kovetkezo` 1. lépés) jelzi. Ez a két PR közti szemantikus ütközés hálója: mindkét PR külön zöld volt, az együttesük nem.

**F217.6 — a PR-ellenőrzés (`ellenorzes.yml`, `szabalyok.py`, `futtat.py`).**

A gépi kapuk előtt egy új lépés fut: `generalt_nezetek.py --ir` a runner munkapéldányán. Ez nem commitol; a kapuk a friss nézetet látják. Ez a brief 2. pont 4. szerinti „ideiglenes generálás”. Kapunként:
- **E28 a PR-ban:**
  - (1) a generátor hiba nélkül lefut: HIBA;
  - (2) a helyben frissítő út egyezik a nulláról generálttal: HIBA, marad;
  - (3) a commitolt blob egyezik az újragenerálttal: **jelentés**, nem HIBA („a main-en az Action frissíti”);
  - (4) **új:** őrzött (kiadott) lap tartalma változna új kiadás nélkül: HIBA (3.4).
- **E35 a PR-ban:** ugyanígy jelentés, a nyílt mag a main-en frissül.
- **E29, E38, E39:** változatlan szigor, de a friss nézeten futnak, nem a commitolton. Így a hiba továbbra is merge előtt derül ki.
- **A main-en** (`push`) a nem bot szereplő futásában az E28/E35 (3) jelentés, mert a merge commit nézete még a régi. A bot commitjának futásában HIBA. Így nincs átmeneti piros a merge commiton, és a végállapot mérve van.

**F217.6a — átmenet: generált fájl a PR-ban.** Ha egy PR mégis módosít `gazda=action` kimenetet, az ütközést okoz. Ajánlás: először FIGYELMEZTETÉS („felesleges, az Action írja”), és az első sikeres Action-újragenerálás után HIBA. Kivétel a bot. Lásd O4.

**F217.7 — a kiadás menete (`.claude/commands/kiadas.md`).** Az 5. lépés `general.py --cel naplo/nyitott --ir` és `nyilt_mag_export.py` sora kikerül. A kiadás PR-ja a `kiadasok.tsv` sort és a forrást hozza; a lapot és a nyílt magot az Action generálja. A helyi `push_elott.py` E28/E35-öt a PR-szabály szerint kell értelmeznie. Ez az F216 fájlja, nincs a brief `ir`-jében, l. O5.

**F217.8 — átnézés a repón kívül.** A PR-ban az ideiglenesen generált lexikonlapok és a main-hez mért diffjük CI-artefaktként tölthetők le (`actions/upload-artifact`). A repóba nem kerülnek. A `/kiadas` és a `/lap-javit` „renderelt lapot megnyitni” lépése helyben `generalt_nezetek.py --gyoker <tmp>`-vel ugyanezt adja.

### 3.4 A kiadott lap szabálya (brief 2. pont 5.)

A `orzes=kiadas` sor ID-je kiadott, ha van sora a `kiadasok.tsv`-ben. Ha az újragenerált lap tartalma eltér a commitolttól (a dátumsorokon kívül), a változás csak két esetben mehet át:
- (a) a PR új `kiadasok.tsv` sort hoz ugyanarra az ID-ra (új kiadás, a `/kiadas` menete);
- (b) a diff kizárólag számkiosztás: a `DT-F<nn>[a-z]` → `DT<n>` csere és az ebből feloldott dátum. Ez a `feladatok.yml` saját lépése (F201, DT-F201a); egy normalizált összevetés dönti el (a DT-tokenek helyőrzőre cserélve egyezik).

Minden más eltérés:
- a PR-ban HIBA (E28 (4));
- a main-en az Action nem írja ki a lapot, a futás piros, az üzenet megnevezi a lapot és a `/kiadas`, illetve `/lap-javit` utat.

Így a kiadott lap nem változik csendben. A befagyasztott lap a mai módon kimarad.

### 3.5 Kockázatok

1. **Két PR szemantikus ütközése.** Mindkettő zöld, az együttesük nem. Háló: a kapuk az Action-ben a commit előtt (F217.5). A main-őr jelzi. A javítás külön PR.
2. **CI-idő.** Az E28 ma is generál; a PR-lépés egyszer generál, és a kapuk ezt használják. A helyben-ág (E28 (2)) lapnként +50 s. Ha a cikkek száma nő, a PR-ban a változott bemenetek szerinti szűkítés jöhet (a `bemenetek` mező erre is jó). Mivel a G01 szinte minden adatból olvas, ma nem érdemes.
3. **A #709 hatása.** A #709 a `lexikon_general.py`-t és az ISTENTISZT-001 lapot írja (térkép T1: új szerkezet?). A megvalósítás előtt a determinizmus-mérést (1.2) az ISTENTISZT-001-en is meg kell ismételni a merge utáni main-en.
4. **Python-verzió.** A CI 3.11, a helyi mérés 3.14. A determinizmus-mérést a CI is futtassa (a teszt része).
5. **Átmeneti időszak.** A nyitott ágakon commitolt generált fájlok a merge-nél ütközhetnek a bot commitjával. Az első Action-futás után a régi ágaknak egyszer be kell hozniuk a main-t; ez az utolsó ilyen kör.

### 3.6 Kimarad (indoklással)

- **`generalt/muhely/`** (G11, `nemdet`): a kimenet időtől és a GitHub-állapottól függ, merge-enként nem reprodukálható. Ajánlás: ütemezett futás vagy kézi indítás, és az ágak ne commitolják. Ez külön feladat, mert a műhely-feed fogyasztóit érinti.
- **Adat-pillanatképek** (B05, B06, B18, B19, B21): bemenetek, az ágon maradnak, a védelmük a frissességi kapu (térkép GK-03, a generátor újraírása).
- **Kiadási csomagok** (`nyilt_karoli_*`): kiadáskor készülnek.

---

## 4. Nyitott kérdések (technikai, az orkesztrátornak)

- **O1 — a workflow helye.** Ajánlás: a `feladatok.yml` meglévő 2. lépése (egy futás, egy commit), új `generalt_nezetek.yml` helyett. Ehhez a `feladatok.yml` bekerül az `ir`-be, a `generalt_nezetek.yml` kikerül.
- **O2 — a jegyzék formája** (a térkép O2-je). Ajánlás: egy tábla `tipus` mezővel (2. pont); a B-azonosító `^B\d{2,3}$`, a térkép számai változatlanok. Alternatíva: két tábla (`generalt_nezetek.tsv` és `generalt_bemenetek.tsv`), de ez az `ir`-t bővíti.
- **O3 — a dátumszabály** (F217.3a). Ajánlás: a régi `ts`, változásnál a HEAD commit dátuma.
- **O4 — generált fájl a PR-ban.** Ajánlás: FIGYELMEZTETÉS, majd az első sikeres Action-futás után HIBA.
- **O5 — az `ir` bővítése.** A terv a brief `ir`-jén kívül ezeket érinti:
  - `.github/workflows/feladatok.yml`;
  - `eszkozok/szamkiosztas_ujragen.py`;
  - `eszkozok/ellenorzes/szabalyok.py`, `futtat.py`, `tesztek/test_szabalyok.py`;
  - `eszkozok/ellenorzes/e28_migralt_nezetek.tsv` és fogyasztói: `torzscikk_general.py`, `lexikon_ket_ut_meres.py`, `teszt_torzscikk_migralt.py`;
  - `eszkozok/push_elott.py` (F216);
  - `.claude/commands/lap-javit.md`;
  - `MUNKAMENET.md` (A7, B7, C1: „`--ir` és commit”).

  Ajánlás: a brief fejlécének `ir`-je ezekkel bővüljön a megvalósítás első commitjában, az átnézés jóváhagyásával. A `kizar`-ütközést a `feladatok.py fuggesek` a bővítés után méri.
- **O6 — a kiadott lap számkiosztás-kivétele** (3.4 (b)). Elfogadható-e a normalizált összevetés, vagy a számkiosztás után is új kiadás kell? Ajánlás: a kivétel. A DT-szám nem tartalmi változás, és az F201 pont ezért vezette be az újragenerálást.

Tartalmi (felhasználói) kérdés ebben a részben nincs. A kiadott lap szabálya a brief 2. pont 5. megvalósítása.

---

## 5. Az átnézés eredménye (orkesztrátor, 2026-11-13)

Az orkesztrátor (`local_c8cc3610…`, a felhasználó felhatalmazásával: „vidd végig ezeket … orkesztráld”) a tervet elfogadta. A megvalósítás ennek a szakasznak a döntései szerint megy; ahol ez eltér a fenti 1–4. ponttól, ez a szakasz az irányadó.

**Döntések:**
- **O1:** a `feladatok.yml` meglévő 2. lépése bővül (egy futás, egy commit). A `.github/workflows/feladatok.yml` bekerül az `ir`-be, a `generalt_nezetek.yml` kikerül.
- **O2:** egy tábla, `tipus` mezővel; a térkép B-számai változatlanok.
- **O3:** a dátumszabály elfogadva: a régi `ts`, változásnál a HEAD commit dátuma.
- **O4:** elfogadva: FIGYELMEZTETÉS, az első sikeres Action-futás után HIBA.
- **O5:** elfogadva; a bővített `ir` a megvalósítás első commitjában kerül be.
- **O6:** elfogadva: a számkiosztás-kivétel normalizált összevetéssel.

**Sorrend:** a `.claude/commands/kiadas.md`-t egy másik, előbb mergelődő PR is írja (új 3/b. lépés: minta-kapu, olvasói átolvasás, hibanapló; DT-F212f). Az F217.7 csak utána, a main behozásával szerkeszti.

**1. kiegészítés — a 3.4 harmadik kivétele.** A kiadott lap változása akkor is átmehet, ha:
- (c) a PR új `adat/lap_javitasok.tsv`-sort hoz ugyanarra az ID-ra;
- és ez a sor tételesen leírja a változást (javítás kiadás nélkül, `/lap-javit`).

Valós eset: a HAMART-001 a #709-ben a minta-kapu javításaival ilyen sort kap. A kapu tehát három kivételt ismer: (a) új `kiadasok.tsv` sor, (b) számkiosztás-diff, (c) új `lap_javitasok.tsv` sor.

**2. kiegészítés — a #709 döntése** (a felhasználó: „Igen, az újjal”). Az ISTENTISZT-001 lapja befagyasztva marad az 1. kiadás állapotában; a 2. kiadás az újraírt generátorral jön.
- A G01 aktív lapja most **csak a HAMART-001**.
- A 3.5/3. pont ISTENTISZT-mérése elmarad.
- A #709 minta-kapuja (címke-ismétlés, cellát ismétlő jegyzet, forrásnév a mondatban, belső név) a friss nézeten fut, az E29/E38/E39 mellett: bekerül a G01/G02 `kapuk` mezőjébe, és az F217.5 (Action, commit előtt) és az F217.6 (PR, ideiglenes generálás) kapusorába.

**Indítás:** a #709 mergelése után, az orkesztrátor jelzésére. Addig a brief `megallt`.

