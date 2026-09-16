# SDBH-import brief — szemantikai domének (SDBH + SDGNT)

*Készítette: chat-menet (Opus 5), 2026-09-15, **v2** (v1: első kiadás; v2: az 1. menet lefutott, a független ellenőrzés egy adat-rést és két kisebb hibát talált — §1.5 —, ezeket a 2. menet SDBH.1a–SDBH.5a tételei zárják). Kiindulási állapot: `main` = `origin/main` = **`a94b9f9`** (F0–F5 lezárva); az 1. menet után **`6fe0d1e`**.*
*Végrehajtás: Claude Code, a repó gyökeréből, két menetben, Sonneten (a 2. az SDBH.1a–SDBH.5a). A chat-menet nem hajtja végre — ez a brief a bemenete.*
*Előzmény: `ATALAKITASI_TERV.md.md` 4.3 („Új dataset: SDBH”), D17, D18, N11; `F5_BRIEF.md` v2 N7. Felhasználói döntés (2026-09-15): önálló, rövid menet az F5 után és az F6 előtt; az SDGNT ugyanebben a menetben; a repóba csak kivonat kerül, rögzített forrás-verzióval; a licenc-publikálási döntés (N11) az F6 brief előfeltétele marad.*

---

## 0. Miért tér el ez a brief a terv 4.3 pontjától

A számokat 2026-09-15-én, ebben a chat-menetben futtatott mérés adja, a rögzített UBS-commiton (§1.2) és az `a94b9f9`-en. Négy eltérés van.

**Egy — a domén jelentés-szintű, nem szó-szintű.** A terv „Strong → doménje” alakban írja le a join-t. Az SDBH-ban viszont a domén a jelentés-egységen (`LEXMeaning`) ül: a `kalal` (H7043) 11 doménben szerepel (Agile, Shape, Shame, Curse…), mert minden jelentése máshová esik. Strong-szintű join-nal a mező-tágítás minden jelentés doméntársait egybeöntené. A kivonat sora ezért `Strong × jelentés × domén`.

**Kettő — a terv két száma pontatlan.** A „381 domén” egy üres kódot is számol: 208 jelentés-egység `DomainCode=""` értékkel áll a forrásban. A valódi héber doménkód **380**. A „8 976 Strong-kód” helyett **8 975** a különböző, nem üres érték, és ebben öt érvénytelen is van (§1.3). A „Curse” domén „10 szava” helyes, de 10 *bejegyzés* és 11 Strong-kód: a H0421 és a H0422 egy bejegyzésben áll. *(A chat-menet a jóváhagyáskor „381 ✔”-t írt; ez tévedés volt, a brief a javított értékkel dolgozik.)*

**Három — a harmadik használat (szakasz-profil) kimarad.** Versenkénti hivatkozás-táblát kívánna: 260 813 héber és 130 923 görög hivatkozást, héber versszámozással és könyvkód-leképezéssel. Ez nem rövid menet. Az F6-nak a Strong → domén kapcsolat kell, a profil nem (l. N1).

**Négy — az `F5_BRIEF.md` N7 állítása csak részben igaz.** Szerinte az import után a sablont nem kell módosítani. A P2 első mondata azonban jelen idejű tényt állít („ma nem ad eredményt”), és ez az import után hamissá válik. A mondat ráadásul gépi domén-hivatkozást tilt, amíg áll. Ezért van egy külön, elvethető tétel (SDBH.6).

---

## 1. Mért kiindulási állapot

### 1.1 A repó *(`a94b9f9`)*

- `adat/datasetek.tsv`: 8 SDBH/SDGNT sor (4 study-típus × 2), mindegyik `fajl` üres, `kotelezoseg=ajanlott`, `allapot=hianyzik`.
- `eszkozok/lekerdez.py`: a `cmd_domen` a `datasetek.tsv` SDBH-sorának `allapot`-ját nézi; ha nem `elerheto`, üzenetet ír a stderr-re és 2-es kóddal kilép. Ha `elerheto`, akkor is 2-vel lép ki („a domén-lekérdezés logikája még nincs implementálva”). A parser súgója: *„szemantikai domén (SDBH/SDGNT) — előfeltétel hiányzik”*.
- `CLAUDE.md` „Adat-tár”: *„**SDBH / SDGNT** (szemantikai domének) **még nincs importálva**.”* és *„`konkordancia/` — 387 MB, 17 dataset”*.
- `adat/SEMA.md` 2.6: a `hianyzik` pont az SDBH/SDGNT hiányát írja le; utána *„Licenc-következmény, amit a `konkordancia/README.md`-nek rögzítenie kell:”*. A 4. szakasz felsorolásában: *„**Az SDBH/SDGNT hiánya** (l. 2.6)”*.
- `NYITOTT_FELADATOK.md`: a *„**ÚJ (F1.6) — SDBH / SDGNT import.**”* tétel a generált blokkon **kívül** áll (a blokk a `<!-- GENERÁLT-KEZDET: general.py --cel nyitott` sorral kezdődik, utána).
- `sablonok/4_PaRDeS_tematikus_sablon.md` v16, P2: *„A `lekerdez.py domen` ma nem ad eredményt, mert az `adat/datasetek.tsv` szerint az SDBH/SDGNT állapota `hianyzik`. Amíg ez így áll, gépi doménre hivatkozni nem lehet.”*
- `konkordancia/` alatt nincs SDBH-, SDGNT- vagy UBS-fájl. A `konkordancia/README.md` a KJV/ASV-forrásokról szól, `## Licenc / eredet` szakasszal.

### 1.2 A forrás *(rögzítve)*

| | |
|---|---|
| Repó | `ubsicap/ubs-open-license` |
| Commit | `3a6edd8212df2e1189037ad39687726990c80d56` |
| Letöltés | `https://codeload.github.com/ubsicap/ubs-open-license/tar.gz/3a6edd8212df2e1189037ad39687726990c80d56` (~87 MB) |
| Licenc | CC BY-SA 4.0 (`dictionaries/hebrew/LICENSE.md`, `dictionaries/greek/LICENSE.md`) |

| Fájl (a tarballban `ubs-open-license-<commit>/dictionaries/…`) | SHA-256 |
|---|---|
| `hebrew/JSON/UBSHebrewDic-v0.9.2-en.JSON` | `1686a25dd31dc9afb7b932927e160070667c73caedad11aa7e4482c21f800e8e` |
| `hebrew/JSON/UBSHebrewDicLexicalDomains-v0.9.2-en.JSON` | `fbc862b2c46966cf7f3bf19c2f3e79a7391c34f8c737e1979fa5178ac603d0df` |
| `greek/JSON/UBSGreekNTDic-v1.1-en.JSON` | `d84bb9077a43fa4a4f7e571fe2ffa460fa655d7b78439b366281ce527fd56893` |
| `greek/JSON/UBSGreekNTDicLexicalDomains-v1.1-en.JSON` | `a816a6bb2bdbdd7df6f46f771b5ddb1b9c019d73c3f0147e5a5cead5cfef8b4b` |

### 1.3 A forrás szerkezete és hibái

- Mindkét szótár JSON-lista. Bejegyzés: `MainId`, `Lemma`, `StrongCodes` (lista), `BaseForms[].LEXMeanings[]`. Jelentés-egység: `LEXID`, `LEXEntryCode`, `LEXDomains[]`, `LEXSubDomains[]`, `LEXSenses[]` (`LanguageCode`, `Glosses`), `LEXReferences[]`.
- **SDBH:** 7 932 bejegyzés, 16 224 jelentés-egység. A `LEXSubDomains` mindenütt üres; a doménkód hierarchikus, hármas csoportokban (`002003002008`). 234 jelentés-egységnek nincs valódi doménje (27 üres lista, 207 csak üres kóddal).
- **SDGNT:** 5 507 bejegyzés, 9 178 jelentés-egység. A `LEXDomains` a 93 Louw–Nida főcsoport, a `LEXSubDomains` 645 alcsoport; a `LEXEntryCode` a Louw–Nida szám (`33.471`).
- **Strong-formátum:** `H0001`, `A0002` (arámi), `G0001`; kisbetűs utótag lehet (`H2256b`, `G0001a`); `+`-os összevonás hat SDBH-bejegyzésben (`H0410+H1285` stb.).
- **Hibás `StrongCodes`-értékek (SDBH):** háromszor a szerző neve (`Reinier de Blois`), kétszer előtag nélküli szám (`2062`, `6859`); 26 üres sztring. Érvényes Strong-kód nélküli bejegyzés: SDBH 35 (a négy, csak hibás értéket viselőt is beleértve), SDGNT 110.
- **Arámi kódok:** 372 bejegyzés visel csak `A`-kódot; ezek mögött 375 utótagos `A`-kód és **367 különböző normalizált kód** áll. *(v2: az egység megnevezve, l. §1.5 L3.)* Az `A####` → `H####` leképezéssel mind a 367 kód megtalálható a `TAHOT_kivonat.tsv`-ben; 362 kód kizárólag a Dán, Ezsd, Jer 10 és 1Móz 31 fejezetekben (könyv-, illetve fejezetszintű szűrés). Öt Strong-szám héber szóra is ki van osztva: `H1529`, `H2269`, `H5613`, `H6211`, `H8412`. Ez Strong-homográf, nem leképezési hiba.

### 1.4 Elvárt értékek *(a §2 szabályainak referencia-futtatásából)*

| Tétel | SDBH | SDGNT |
|---|---|---|
| adatsor (fejléc nélkül) | **22 280** | **9 075** |
| különböző `strong` | 8 557 | 5 312 |
| különböző `strong_kod` | 8 935 | 5 397 |
| különböző `entry_id` | 7 862 | 5 397 |
| különböző `lexid` | 16 219 | 9 067 |
| különböző `domen_kod` (`—` nélkül) | 380 | 668 |
| `domen_kod = —` sor | 344 | 21 |
| `osszetett ≠ —` sor | 12 | 0 |
| `nyelv = arameus` sor / különböző `strong_kod` | 2 086 / 647 | — |
| doménfa-sor | 411 | 738 |
| anomália-sor *(v2)* | **75** (35 `strong_nelkul` + 5 `ervenytelen_kod` + 35 `jelentes_nelkul`) | 110 `strong_nelkul` |

*Az SDBH hibás anomália-sorai: 35 `strong_nelkul` + 5 `ervenytelen_kod` = 40 sor, 36 különböző bejegyzés. A négy csak hibás kódot viselő bejegyzés mindkét típusban szerepel. (v2) Ehhez jön 35 `jelentes_nelkul` sor, 35 további bejegyzés (§2.4).*

**Forrás-leltár** *(v2)*: minden forrásbejegyzés pontosan egy helyen áll.

| | forrás | a kivonatban (`entry_id`) | `strong_nelkul` | `jelentes_nelkul` |
|---|---|---|---|---|
| SDBH | 7 932 | 7 862 | 35 | 35 |
| SDGNT | 5 507 | 5 397 | 110 | 0 |

| Kimeneti fájl | Sor (fejléc nélkül) | SHA-256 a `#`-sorok nélkül |
|---|---|---|
| `konkordancia/SDBH_domenek.tsv` | 22 280 | `678160daa869dc81ef8d5b7743d4e4be533d8933409805bc45158bef5debd709` |
| `konkordancia/SDGNT_domenek.tsv` | 9 075 | `800ae82baebdcc4ca9951fcfff8b861d98f4d6da5b9aec3917c2316395c0c097` |
| `konkordancia/SDBH_SDGNT_domenfa.tsv` | 1 149 | `88319a86cb313242b08abecc282f891353668f1862d918b54a8e9ec77efef991` |
| `konkordancia/SDBH_SDGNT_anomaliak.tsv` *(v2)* | **185** | `2c45f330c1f76af0b66a001498e1379c45c74b7249be1cfb9137f476c27839a2` *(v1: 150 sor, `ab69a616…`)* |

**Lefedettség** *(a kivonat `strong` oszlopa a kivonatok lexikai Strong-kódjaihoz mérve; a héber oldalon a `H9xxx` nélkül)*:

| | Strong-kód | Token |
|---|---|---|
| `TAHOT_kivonat.tsv` | 8 421 / 8 502 (99,0%) | 259 162 / 299 370 (86,6%) |
| `TAGNT_kivonat.tsv` | 5 252 / 5 410 (97,1%) | 130 159 / 141 489 (92,0%) |

A héber token-rés oka: gyakori szavak hiányoznak, köztük `H1961` (lenni), `H5414` (adni), `H6440` (arc), `H5921`, `H0413`, `H3605`, `H3588`. **A `domen` üres eredménye ezért nem negatív lelet.**

### 1.5 Az 1. menet mért eredménye *(v2; független ellenőrzés, `6fe0d1e`)*

Commitok: `a92916f` (SDBH.1), `9c9ba5c` (SDBH.2), `9aa094a` (SDBH.3), `4474cab` (SDBH.4), `1fd5aa6` (SDBH.5), `6fe0d1e` (SDBH.6); push `a94b9f9..6fe0d1e`. A brief v1 nem került a repóba.

Friss klónon megerősítve: a négy kimeneti fájl SHA-256-ja; a hat commit fájllistája (= §5); a `datasetek.tsv` 8 cserélt sora, a `hianyzik` csak a fejléc-kommentben; a K11 és a K13 grep-je; a `domen H0779 H7043` és a `domen H6093 H0779` helyi futtatással; a két ©-mondat.

**A független ellenőrzés három rést talált, amelyet egyik K-kritérium sem fogott meg:**

| # | Hol | Mi a hiba | Kinek a hibája |
|---|---|---|---|
| L1 | §2 szabályai | **35 SDBH-bejegyzésnek van érvényes Strong-kódja, de nincs jelentés-egysége** (a szótár felvette, még nem elemezte). Sort nem ad, anomáliának sem számít: csendben kiesik. A `domen A0116` (*’edajin*, „akkor”, 57 TAHOT-előfordulás) „nincs SDBH-bejegyzés”-t ír, holott a bejegyzés létezik. Az elemzetlenek között gyakori szó is van: `H0518` (*’im*, 1 069), `H1931` (*hú’*, 1 876). Öt esetben a kód egy másik, elemzett bejegyzésen keresztül ad sort (`H0001`, `H0791`, `H5933`, `H8213b`, valamint utótag nélkül a `H2669`), és az elemzetlen homonim a kimenetben láthatatlan. | **brief**: a §1.4 7 862-es értéke a kiesést már tartalmazta (7 932 − 35 − 35), és minden számláló a kivonatot mérte, egyik sem a forrás egészét |
| L2 | `eszkozok/sdbh_sdgnt_import.py`, anomália-írás | a sorok halmazba gyűlnek (`all_anoms = {…}`), a §2.4 „nincs deduplikálás” szabálya ellenére. Ma nincs hatása (az SHA egyezett), de két azonos anomália-sor egybeolvadna. | végrehajtás |
| L3 | §1.3 arámi pont | a „367 kód” egysége nem volt megnevezve. A chat-mérés normalizált kódot számolt, az `ellenoriz.py` bejegyzést. A kivonatban 367 csak-arámi bejegyzés van (a 372-ből 5 elemzetlen kiesett, L1), mögöttük 362 kód; a két 367 véletlenül egyezik. Mindkét ellenőrzés érvényes, csak mást mér. | **brief** |

Az L1 adat-rés, az L2 és az L3 nem. Mind a 2. menetben javul; a v1 commitok nem íródnak át (D21).

---

## 2. Kimeneti szabályok

Minden szabály determinisztikus; két futás byte-azonos kimenetet ad.

### 2.1 Fájlformátum

UTF-8, BOM nélkül, sorvég `\n` (Windowson is: `newline='\n'`). Mezőelválasztó tab. Írás `'\t'.join()`, a `csv` modul tilos (`CLAUDE.md`). A `—` karakter U+2014. Minden fájl három `#`-sorral kezdődik, utána a fejléc:

```
# GENERÁLT: eszkozok/sdbh_sdgnt_import.py — kézzel nem szerkesztendő.
# forras: ubsicap/ubs-open-license @ 3a6edd8212df2e1189037ad39687726990c80d56 | <forrásfájl(ok) neve> sha256=<…>
# licenc: CC BY-SA 4.0 — © United Bible Societies; forrásmegjelölés: konkordancia/SDBH_SDGNT_README.md
```

Időbélyeg nem kerül a fájlba (determinizmus). Az SHA-256 ellenőrzés a `#`-sorok elhagyásával kapott byte-sorozatra vonatkozik.

**Szöveg-tisztítás** (`lemma`, `entry_kod`, `domen`, minden glossza, `nyers_ertek`, `cimke`, `leiras`): a `[\t\r\n]+` futamok egy szóközre cserélődnek, majd `strip()`. A referencia-futtatásban 2 mező változott így.

### 2.2 `SDBH_domenek.tsv` és `SDGNT_domenek.tsv`

Fejléc: `strong	strong_kod	osszetett	nyelv	szotar	entry_id	lemma	lexid	entry_kod	domen_kod	domen	glossza	hivatkozas_n`

1. **Strong-kódok.** A `StrongCodes` minden elemére: az üres sztring kimarad (megszámolva). Minden elemet `+` mentén részekre vágunk. Érvényes rész: `^([HAG])(\d{4})([a-f]?)$`.
   - `strong` = `H` + a négy számjegy (`H` és `A` előtagnál), illetve `G` + a négy számjegy.
   - `strong_kod` = a rész, ahogy áll (`H2256b`, `A0002`).
   - `osszetett` = a teljes elem, ha `+` van benne (`H1237+H0205a`), különben `—`.
   - `nyelv` = `heber` / `arameus` / `gorog` az előtag szerint.
   - Érvénytelen rész → anomália-sor (`ervenytelen_kod`, `nyers_ertek` = a teljes elem). Ha a bejegyzésnek egyetlen érvényes része sincs → anomália-sor (`strong_nelkul`, `nyers_ertek` = `json.dumps(StrongCodes, ensure_ascii=False)`), és a bejegyzés nem ad adatsort.
2. **Jelentés-egységek.** Minden `BaseForms[].LEXMeanings[]` elemre: `lexid` = `LEXID`; `entry_kod` = `LEXEntryCode`, vagy `—`, ha üres/null; `glossza` = az `en` nyelvű `LEXSenses` összes glosszája, sorrendtartó duplikátum-szűréssel, `; `-vel, vagy `—`; `hivatkozas_n` = `len(LEXReferences)` (null → 0).
3. **Domén.** SDBH: a `LEXDomains` nem üres kódú elemei. SDGNT: a `LEXSubDomains` nem üres kódú elemei, és csak ha ilyen nincs, a `LEXDomains` elemei. Ha egyik sincs: egy sor `domen_kod = —`, `domen = —` értékkel.
4. **Sor** = érvényes Strong-rész × jelentés-egység × domén. Azonos sorok egyszer szerepelnek.
5. **Rendezés:** a teljes sor mint sztring-mezők tuple-je, Python `sorted()`.

### 2.3 `SDBH_SDGNT_domenfa.tsv`

Fejléc: `szotar	kod	szint	szulo_kod	cimke	leiras`. Forrás: a két `LexicalDomains` JSON minden eleme. `szint` = `Level`; `szulo_kod` = a kód utolsó három jegy nélkül, vagy `—`, ha a kód háromjegyű; `cimke`/`leiras` = az `en` lokalizáció `Label`/`Description` mezője (üres leírás → `—`). Rendezés: tuple, `sorted()`. **Minden `szulo_kod` létezik a saját szótára kódjai között**, és a kivonatok minden `domen_kod`-ja (a `—` kivételével) szerepel a fában.

### 2.4 `SDBH_SDGNT_anomaliak.tsv`

Fejléc: `szotar	entry_id	lemma	tipus	nyers_ertek	allapot`. Az `allapot` a `strong_nelkul` és az `ervenytelen_kod` sorban `AZONOSITVA, NEM JAVITVA`. Nincs deduplikálás — *(v2)* a sorok listában gyűlnek, nem halmazban; rendezés tuple, `sorted()`.

*(v2)* **Harmadik típus: `jelentes_nelkul`.** A bejegyzésnek van legalább egy érvényes Strong-része (§2.2/1), de a `BaseForms[].LEXMeanings[]` együttvéve üres. `nyers_ertek` = `json.dumps(StrongCodes, ensure_ascii=False)`, `allapot` = `FORRASBAN_BEFEJEZETLEN`. Ez nem forráshiba: a szótár felvette a szót, de még nem elemezte. A `strong_nelkul` bejegyzés nem kaphat `jelentes_nelkul` sort (a két típus kizárja egymást). **Egyik anomália sincs kijavítva vagy kitalált előtaggal pótolva** (a `2062` nem lesz `H2062`).

---

## 3. Tételek

### Tétel SDBH.0 — előfeltétel-mérés *(nincs commit)*

Mérd újra az 1.1 minden állítását. Ha bármi eltér, **állj meg, és jelentsd**, mielőtt írnál.

### Tétel SDBH.1 — import-szkript, kivonatok, ellenőrző szkript

**a) `eszkozok/sdbh_sdgnt_import.py`**, a `CLAUDE.md` szerinti UTF-8 őrrel.

- `--letolt`: a §1.2 URL-ről `urllib`-bel letölti a tarballt egy `tempfile.mkdtemp()` könyvtárba (**a repón kívülre**), `tarfile`-lal csak a négy JSON-t bontja ki, és ellenőrzi a négy SHA-256-ot. Eltérésnél 2-es kóddal kilép, és nem ír semmit.
- `--forras <könyvtár>`: már kibontott `dictionaries/` szülőkönyvtárból dolgozik, ugyanazzal az SHA-ellenőrzéssel.
- `--minta`: nem ír fájlt. Kiírja a `H0779`, `H6093`, `A0002` és `G2671` adatsorait, a `H1237+H0205a` összetett kód sorait, a `H7043` különböző doménjeinek számát, és az öt `ervenytelen_kod` anomáliát.
- Kapcsoló nélkül a négy fájlt írja a `konkordancia/` alá, a §2 szerint.

**Megállási pont — minta.** Futtasd `--letolt --minta` módban. Ha a kiírt értékek egyeznek a §3.5 táblázat H0779/H6093/G2671 soraival, a `H7043` doménszáma 11, és az öt anomália a §1.3 szerinti, **folytatható**: a minta a brief jóváhagyott számaival egyezik. Bármi eltérésnél állj meg, és idézd a kimenetet.

**b)** Teljes futtatás, majd **`eszkozok/sdbh_sdgnt_ellenoriz.py`** megírása és futtatása. A szkript csak a repó fájljait olvassa (`split('\t')`), és kritériumonként `OK`/`HIBA` sort ír:

- a §1.4 mindkét táblázatának minden értéke, a négy SHA-256-tal;
- minden adatsor mezőszáma a fejlécével azonos;
- a doménfa-integritás (§2.3 két állítása);
- az arámi ellenőrzés (§1.3: 367 / 367 megtalálható, 362 kizárólagos, az öt homográf pontosan a felsorolt);
- a lefedettség (§1.4 alsó táblázat, a négy számpár).

Kilépési kód: 0, ha minden `OK`; különben 1.

**c)** Futtasd kétszer egymás után az importot, és ellenőrizd, hogy a négy fájl byte-azonos (K3).

### Tétel SDBH.2 — forrás- és licenc-dokumentáció

**a) Új fájl: `konkordancia/SDBH_SDGNT_README.md`.** A `TBESH_TBESG_README.md` szerkezetét kövesse. Kötelező szakaszok:

1. *Forrás* — repó, commit, a négy fájl neve és SHA-256-ja, verziók (SDBH v0.9.2, SDGNT v1.1), a reprodukáló parancs (`python eszkozok/sdbh_sdgnt_import.py --letolt`).
2. *Licenc és forrásmegjelölés* — CC BY-SA 4.0. **A két szótár `dictionaries/hebrew/README.md`, illetve `dictionaries/greek/README.md` fájljának zárójeles ©-mondatát szó szerint másold ide** — ez a licenc által megkövetelt forrásmegjelölés. Utána magyarul: a származékos adat, beleértve a motívumlexikon domén-hivatkozásait, ugyanilyen licenc alá esik; a publikálási döntés nyitott (terv N11).
3. *Fájlok és oszlopok* — a négy fájl, a §2 szabályainak rövid leírása, a jelentés-szintű sor indokával (`kalal`, 11 domén).
4. *Mért értékek* — a §1.4 két táblázata.
5. *Ismert korlátok* — kb. 90%-os lefedettség és a hiányzó gyakori szavak (üres eredmény ≠ negatív lelet); a Strong-homográfok; az anomália-fájl; a `LEXReferences` nincs importálva (héber versszámozás, l. N1); a terv D18-a (a domén támasz, nem a mező-hipotézis helyettesítője; az `itzávón` doménje Spasm, nem Curse).

**b) `konkordancia/README.md`** — a fájl végére új szakasz:

> ## CC BY-SA 4.0 licencű datasetek — SDBH, SDGNT
>
> A `SDBH_domenek.tsv`, a `SDGNT_domenek.tsv`, a `SDBH_SDGNT_domenfa.tsv` és a `SDBH_SDGNT_anomaliak.tsv` a United Bible Societies nyílt szótáraiból származik, **CC BY-SA 4.0** licenc alatt. A forrásmegjelölés kötelező, és a belőlük származó adat — beleértve a motívumlexikon domén-hivatkozásait — **ugyanilyen licenc alá esik**. Ez eltér a mappa többi, közkincs vagy CC BY 4.0 licencű forrásától. Forrás-commit, ellenőrző összegek és a pontos forrásmegjelölés: `SDBH_SDGNT_README.md`.

**c) `konkordancia/Validacios_naplo.md`** — új, dátumozott bejegyzés a meglévők formájában: mit (SDBH/SDGNT import), mivel vetettük össze (a brief §1.4 referencia-értékei, a `TAHOT_kivonat.tsv` arámi ellenőrzése, a lefedettség), eredmény kritériumonként, módosított fájlok, **„Lezárva.”** — vagy a nyitott eltérések listája.

### Tétel SDBH.3 — adatmátrix és belépési dokumentáció

**a) `adat/datasetek.tsv`** — a 8 SDBH/SDGNT sorban a `kotelezoseg` marad; a többi mező:

| Mező | SDBH | SDGNT |
|---|---|---|
| `fajl` | `konkordancia/SDBH_domenek.tsv` | `konkordancia/SDGNT_domenek.tsv` |
| `feltetel` | `a 4.1 2. lépéséhez (szemantikai mező); támasz, nem helyettesítés (terv D18)` | `görög oldali szemantikai mező; támasz, nem helyettesítés (terv D18)` |
| `allapot` | `elerheto` | `elerheto` |
| `megjegyzes` | `UBS SDBH v0.9.2, CC BY-SA 4.0; jelentés-szintű domén; az ÓSZ szókincsének kb. 90%-a — hiányzó bejegyzés nem negatív lelet (TAHOT: 99,0% Strong, 86,6% token; hiányzik pl. H1961, H5414, H6440); l. konkordancia/SDBH_SDGNT_README.md` | `UBS SDGNT v1.1 (Louw–Nida alapú), CC BY-SA 4.0; jelentés-szintű domén, alcsoport-szinten; TAGNT: 97,1% Strong, 92,0% token; a SECE_G Louw–Nida kódjával átfed; l. konkordancia/SDBH_SDGNT_README.md` |

Írás előtt és után vesd össze a sorokat: **csak ez a 8 sor változhat**, és azokban csak ez a négy mező (minta: `eszkozok/igazolas_migracio.py`).

**b) `adat/SEMA.md` 2.6.** A ``- `hianyzik` — az **SDBH és az SDGNT importja nem történt meg**.`` kezdetű pont (a `korlatos` pont előtti sorig) helyett:

> - `hianyzik` — jelenleg egyetlen sor sem viseli. Az SDBH és az SDGNT volt ilyen; importjuk 2026.09-ben megtörtént (`konkordancia/SDBH_SDGNT_README.md`). Az érték az értékkészletben marad a még nem importált datasetek számára.

A ``*Licenc-következmény, amit a `konkordancia/README.md`-nek rögzítenie kell:*`` szövegrész helyett: ``*Licenc-következmény, rögzítve a `konkordancia/README.md` licenc-szakaszában és a `konkordancia/SDBH_SDGNT_README.md`-ben:*``. A mondat többi része marad.

**c) `adat/SEMA.md` 4.** A ``- **Az SDBH/SDGNT hiánya** (l. 2.6) — az F2 `domen` parancsának előfeltétele.`` sor helyett:

> - **Az SDBH lefedettsége** (l. 2.6) — kb. 90%; gyakori szavak is hiányoznak (pl. H1961, H5414, H6440), ezért a `domen` üres eredménye nem negatív lelet.

**d) `CLAUDE.md`.** A `- **SDBH / SDGNT** (szemantikai domének) **még nincs importálva**.` sor helyett:

> - **SDBH / SDGNT** (szemantikai domének, **CC BY-SA 4.0**) az ÓSZ szókincsének kb. 90%-át fedik — **üres `domen`-eredmény nem negatív lelet**, és a domén támasz, nem a mező-hipotézis helyettesítője.

A `387 MB` értéket írd át a `konkordancia/` mért méretére (egész MB, Pythonnal mérve, a `.git` nélkül). A „17 dataset” marad: a két dataset eddig is a mátrixban volt.

### Tétel SDBH.4 — a `domen` parancs

`eszkozok/lekerdez.py`, `cmd_domen` és a parser. A többi parancs **nem változik** (K9).

**Előfeltétel.** A lekérdezett nyelv datasetje (`H` → SDBH, `G` → SDGNT) `allapot`-ja az `adat/datasetek.tsv`-ben `elerheto`. Ha nem, a mai üzenet és a 2-es kilépési kód marad. Az olvasás a meglévő `read_tsv_skip_comments`-szel történik.

**`domen <Strong>` — mező-tágítás.**
- Bemenet `H####` / `G####`: minden sor, ahol `strong` egyezik. Bemenet utótaggal (`H2256b`) vagy `A####`: minden sor, ahol `strong_kod` egyezik.
- Kimenet jelentés-egységenként: `strong_kod`, `nyelv`, `lemma`, `lexid`, `glossza`, a doménkód és -címke (`—` esetén „domén nélkül”).
- Utána doménenként (kód szerint rendezve) egy `## <domen_kod> <domen> (<n> Strong)` fejléc, alatta a doméntársak: a doménben előforduló többi különböző `strong` (a lekérdezett nélkül), rendezve, `glossza`-mintával.
- Ha nincs sor: `# domen <Strong> — nincs <SDBH|SDGNT>-bejegyzés (a szótár nem teljes: hiányzó bejegyzés nem negatív lelet)`, kilépési kód 0.

**`domen <Strong_A> <Strong_B>` — elhatárolás.** A két bemenet doménkód-halmazának metszete (`—` nélkül), doménenként mindkét oldal érintett `lexid`-jével és glosszájával. Üres metszet: `# nincs közös domén`, kilépési kód 0.

**Vegyes nyelv** (`H` és `G` együtt) vagy háromnál több argumentum: hibaüzenet a stderr-re, kilépési kód 1.

**Proveniencia** — utolsó sor, a többi parancs formájában:

```
proveniencia: scope=SDBH-v0.9.2 | forras=SDBH_domenek.tsv | strong=H0779 | n=2 | ts=2026-09-15T12:00Z
proveniencia: scope=SDBH-v0.9.2 | forras=SDBH_domenek.tsv | strong=H0779+H7043 | n=1 | ts=…
```

Görögnél `scope=SDGNT-v1.1 | forras=SDGNT_domenek.tsv`. Az `n` egy argumentumnál a lekérdezett kód különböző doménkódjainak száma, kettőnél a közös doménkódok száma; a `—` egyiknél sem számít. A `scope` szándékosan verziót és nem „teljes”-t mond, mert a szótár nem teljes.

**Súgó:** `szemantikai domén (SDBH/SDGNT) — mező-tágítás 1 Stronggal, elhatárolás 2-vel`. A docstring 3. használatot („szakasz-profil”) nem ígér.

### 3.5 A `domen` elvárt eredményei *(a referencia-kivonaton mérve)*

| Parancs | Elvárt |
|---|---|
| `domen H0779` | `n=2`: `002001001024` Impact, `002003002008` Curse; a Curse-társak: H0421, H0422, H0423, H2194, H3994, H6895, H7043, H7045, H7621, H8381 |
| `domen H7043` | `n=11` |
| `domen H0779 H7043` | `n=1`: `002003002008` Curse |
| `domen H6093` | `n=1`: `002001001055` Spasm; társak: H2256, H2342, H6089, H6735, H6736 |
| `domen H6093 H0779` | `# nincs közös domén`, `n=0`, kilépési kód 0 |
| `domen G2671` | `n=1`: `033055` Bless, Curse; társak: G0331, G0332, G0685, G1944, G2127, G2129, G2652, G2653, G2672 |
| `domen G2127 G2672` | `n=1`: `033055` |
| `domen H1961` | „nincs SDBH-bejegyzés”, `n=0`, kilépési kód 0 |
| `domen H2256` | négy `strong_kod`: H2256a, H2256b, H2256c, H2256d |
| `domen H2256b` | csak a H2256b sorai |
| `domen H0779 G2671` | kilépési kód 1 |

*A H6093 ↔ H0779 sor a terv D18-ának gépi tanúja: az `itzávón` és az `arar` között nincs közös domén.*

### Tétel SDBH.5 — nyitott tétel lezárása

`NYITOTT_FELADATOK.md`, a generált blokkon **kívül**. A `* **ÚJ (F1.6) — SDBH / SDGNT import.**` kezdetű pont (egyetlen sor) helyett:

> * ~~**ÚJ (F1.6) — SDBH / SDGNT import.**~~ **LEZÁRVA 2026.09.‹nap› → SDBH.1–SDBH.4.** Kivonat a `konkordancia/SDBH_domenek.tsv`-ben és a `SDGNT_domenek.tsv`-ben, jelentés-szintű doménnel; a `lekerdez.py domen` mező-tágítást és elhatárolást ad. Forrás és licenc: `konkordancia/SDBH_SDGNT_README.md`. Nyitva maradt: a szakasz-profil (versenkénti hivatkozás-tábla), a forrás 150 anomália-sora (`SDBH_SDGNT_anomaliak.tsv`), és a CC BY-SA 4.0 publikálási következménye (terv N11) — ez az F6 brief előfeltétele.

A `‹nap›` a commit napja.

### Tétel SDBH.6 — a P2 mondata állapotfüggetlen *(külön commit, elvethető)*

`sablonok/4_PaRDeS_tematikus_sablon.md`. A horgony (a P2 során belül):

```
A `lekerdez.py domen` ma nem ad eredményt, mert az `adat/datasetek.tsv` szerint az SDBH/SDGNT állapota `hianyzik`. Amíg ez így áll, gépi doménre hivatkozni nem lehet.
```

Helyette:

```
A `lekerdez.py domen <Strong> [<Strong>]` gépi támaszt ad (doméntársak, illetve közös domén), ha az `adat/datasetek.tsv` szerint az SDBH/SDGNT `elerheto`; ellenkező esetben gépi doménre hivatkozni nem lehet. A domén **nem helyettesíti** a mező-hipotézist: a mező megválasztása emberi döntés, és a domén-lekérdezés üres vagy szűk eredménye nem negatív lelet.
```

A P2 sor eleje (`- [ ] **P2. Szemantikai mező-hipotézis** — generatív lépés, nincs parancsa. A mező szavai a naplóba kerülnek.`) szó szerint marad. *(A „nincs parancsa” igaz marad: a mező-hipotézisnek nincs parancsa, a `domen` csak támasz.)*

A fájl 3. sora elé, a v16 bejegyzés elé új bekezdés:

```
*v17 — 2026.09.‹nap› (SDBH.6: a P2 domén-mondata állapotfüggetlenné vált — az SDBH/SDGNT import után a `domen` a `datasetek.tsv` állapota szerint ad eredményt; a domén támasz, nem a mező-hipotézis helyettesítője. Tartalmi követelmény nem változott; a „v16 szerint” címkék érvényesek maradnak.)*

```

### Tételek a 2. menetben *(v2)*

Kiindulás: `main` = `origin/main` = `6fe0d1e`. A `SDBH_domenek.tsv`, a `SDGNT_domenek.tsv` és a `SDBH_SDGNT_domenfa.tsv` **nem változhat** (K17).

#### Tétel SDBH.1a — elemzetlen bejegyzések, forrás-leltár

**a) `eszkozok/sdbh_sdgnt_import.py`.** A §2.4 v2 szabálya szerint `jelentes_nelkul` sorokat ír. Az anomáliák listában gyűlnek, és a sorokhoz típusonként rendelődik az `allapot` (L2).

**b) `eszkozok/sdbh_sdgnt_ellenoriz.py`** — módosul, illetve bővül:

- a §1.4 anomália-értékei (185 sor, SDBH 75, `jelentes_nelkul` 35, SDGNT 110) és az új SHA-256;
- `allapot` típusonként: `jelentes_nelkul` → `FORRASBAN_BEFEJEZETLEN`, a másik kettő → `AZONOSITVA, NEM JAVITVA`;
- **forrás-leltár:** szótáranként a kivonat `entry_id`-halmaza, a `strong_nelkul` és a `jelentes_nelkul` `entry_id`-halmaza páronként diszjunkt, és az uniójuk mérete 7 932, illetve 5 507 (a §1.4 leltártáblája);
- **az arámi ellenőrzés két egysége (L3):**
  - a meglévő bejegyzés-alapú sorok címkéje: „a kivonatban csak arámi bejegyzés”;
  - új sor: a kivonat csak-arámi bejegyzéseinek és a csak `A`-kódot viselő `jelentes_nelkul` bejegyzéseknek együtt 372 bejegyzés, mögöttük 367 különböző normalizált kód.

Futtasd az importot `--letolt` móddal kétszer (K3), majd az ellenőrzőt.

#### Tétel SDBH.2a — dokumentáció

**`konkordancia/SDBH_SDGNT_README.md`**, három helyen:

1. A fájl-táblázat ``| `SDBH_SDGNT_anomaliak.tsv` | 150 |`` sora → `185`.
2. A Mért értékek `| anomália-sor | 40 (35 …` sora → a §1.4 v2 sora (a `*(v2)*` jelölés nélkül), és a táblázat után a forrás-leltár táblája.
3. Az „Ismert korlátok” `**Az anomália-fájl**` kezdetű pontja (három sor) helyett:

> - **Az anomália-fájl** (`SDBH_SDGNT_anomaliak.tsv`) 185 sora két fajta tételt tart. **150 sor javítatlan forráshiba** (`AZONOSITVA, NEM JAVITVA`): szerzőnév a Strong-mezőben, előtag nélküli szám, Strong-kód nélküli bejegyzés. **35 sor elemzetlen bejegyzés** (`jelentes_nelkul`, `FORRASBAN_BEFEJEZETLEN`): a szótár felvette a szót, de jelentés-egységet és domént még nem rendelt hozzá — köztük gyakori szavak, pl. `A0116` (*’edajin*, „akkor”), `H0518` (*’im*, „ha”), `H1931` (*hú’*, „ő”). A `domen` ezeket külön jelzi. L. a döntésnaplót a `SDBH_IMPORT_BRIEF.md`-ben.
> - **Az arámi ellenőrzés egysége.** 372 forrásbejegyzés visel csak `A`-kódot; ebből 367 van a kivonatban (5 elemzetlen), a 372 mögött pedig 367 különböző normalizált kód. A két 367 véletlenül egyezik; az `sdbh_sdgnt_ellenoriz.py` mindkét egységet külön ellenőrzi.

A sortörés a környezethez igazodik.

**`konkordancia/Validacios_naplo.md`** — új, dátumozott bejegyzés az SDBH-bejegyzés után: mit (SDBH.1a — elemzetlen bejegyzések, forrás-leltár), mivel (a brief v2 §1.4 leltártáblája, K15–K18), eredmény kritériumonként, módosított fájlok, **„Lezárva.”**

#### Tétel SDBH.4a — a `domen` jelzi az elemzetlen bejegyzést

`eszkozok/lekerdez.py`, csak a `cmd_domen` és a hozzá tartozó segédfüggvények.

- A parancs a kivonat mellett mindig beolvassa a `konkordancia/SDBH_SDGNT_anomaliak.tsv` saját szótárhoz tartozó `jelentes_nelkul` sorait. A `nyers_ertek` JSON-listájából ugyanazzal a szabállyal (`+` mentén vágva, §2.2/1) kinyeri az érvényes részeket, és ugyanazzal az illesztéssel veti össze, mint a kivonat sorait: utótag nélküli `H####`/`G####` bemenetnél a normalizált kódon, utótagos vagy `A####` bemenetnél a részen, ahogy áll.
- **Ha van illeszkedő elemzetlen bejegyzés**, közvetlenül a `# domen …` fejlécsor után (elhatárolásnál argumentumonként, az eredmény előtt) bejegyzésenként egy sor, majd egy záró sor:

```
# figyelem: elemzetlen SDBH-bejegyzés illeszkedik — <entry_id> <lemma> <nyers_ertek>
# (a forrásban szerepel, de jelentés-elemzés és domén nélkül: SDBH_SDGNT_anomaliak.tsv, jelentes_nelkul — nem negatív lelet)
```

- Ha nincs elemzett sor, de van elemzetlen bejegyzés, a fejlécsor: `# domen <Strong> — nincs elemzett SDBH-bejegyzés`. Ha egyik sincs, a mai „nincs SDBH-bejegyzés” sor marad.
- Az `n` definíciója nem változik: az elemzetlen bejegyzés nem ad domént.
- A proveniencia `forras` mezője mindig mindkét olvasott fájlt nevezi meg: `forras=SDBH_domenek.tsv+SDBH_SDGNT_anomaliak.tsv` (görögnél `SDGNT_domenek.tsv+SDBH_SDGNT_anomaliak.tsv`).

#### 3.6 A `domen` elvárt eredményei a 2. menet után

| Parancs | Elvárt |
|---|---|
| `domen A0116` | fejléc: „nincs elemzett SDBH-bejegyzés”; 1 figyelmeztetés (`000120000000000`); `n=0`, kilépési kód 0 |
| `domen H0116` | ugyanaz (normalizált illesztés) |
| `domen H1931` | fejléc: „nincs elemzett SDBH-bejegyzés”; 2 figyelmeztetés (`001778000000000`, `001803000000000`); `n=0` |
| `domen H0001` | `n=9`; 1 figyelmeztetés (`000043000000000`) |
| `domen H8213b` | `n=5`; 1 figyelmeztetés (`007587000000000`) |
| `domen A0116 H0779` | figyelmeztetés az `A0116`-ra; `# nincs közös domén`; `n=0` |
| `domen H1961` | változatlan: „nincs SDBH-bejegyzés”, figyelmeztetés nélkül |
| a §3.5 mind a 11 parancsa | az `n=` és a kilépési kód változatlan; figyelmeztetés egyiknél sem jelenik meg |

#### Tétel SDBH.5a — nyitott tétel pontosítása

`NYITOTT_FELADATOK.md`, a generált blokkon kívül, az SDBH-tétel sorában:
- `→ SDBH.1–SDBH.4.` → `→ SDBH.1–SDBH.4, javítás: SDBH.1a, SDBH.2a, SDBH.4a.`
- ``a forrás 150 anomália-sora (`SDBH_SDGNT_anomaliak.tsv`)`` → ``a forrás 150 hibás anomália-sora és 35 elemzetlen bejegyzése (`SDBH_SDGNT_anomaliak.tsv`)``

---

## 4. Elfogadási kritériumok

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K1 | A forrás a rögzített | az import a négy SHA-256-ot ellenőrzi; hibás hash-sel 2-es kóddal, írás nélkül lép ki |
| K2 | A kivonatok a §1.4 szerint | `python eszkozok/sdbh_sdgnt_ellenoriz.py` kilépési kódja 0, minden sora `OK` |
| K3 | Determinizmus | két egymás utáni import után a négy fájl byte-azonos |
| K4 | Nincs adat a repón kívülről | `git status --porcelain` csak a §5 commitjaiban felsorolt fájlokat mutatja; nincs JSON, tarball vagy ideiglenes könyvtár a repóban |
| K5 | Nincs `csv` modul | `grep -n "import csv\|csv\." eszkozok/sdbh_sdgnt_import.py eszkozok/sdbh_sdgnt_ellenoriz.py` = 0 találat |
| K6 | A mátrix csak a 8 sorban változott | a `git diff adat/datasetek.tsv` pontosan 8 sort cserél; a `hianyzik` érték egyetlen adatsor `allapot` mezőjében sem szerepel (a `#` fejléc-kommentben maradhat) |
| K7 | A `domen` a §3.5 szerint | mind a 11 parancs; az `n=` és a kilépési kód szó szerint, a társ-listák halmazként |
| K8 | A proveniencia-sor formája | minden `domen`-futás utolsó sora `proveniencia: scope=` kezdetű, és tartalmaz `forras=`, `strong=`, `n=`, `ts=` mezőt |
| K9 | A többi parancs érintetlen | a `gerinc`, `scan`, `kollokacio`, `igealak`, `lxx-hid`, `tsk`, `karoli` `--help` kilépési kódja 0; a `git diff eszkozok/lekerdez.py` csak a `cmd_domen` függvényt, a `domen` parser-blokkot és a modul docstringjének `domen`-re vonatkozó részét érinti |
| K10 | Licenc-dokumentáció | a `konkordancia/SDBH_SDGNT_README.md` mind az öt szakaszt tartalmazza; a két ©-mondat karakterre egyezik a forrás README-kkel; `grep -c "CC BY-SA 4.0" konkordancia/README.md` ≥ 1 |
| K11 | Belépési dokumentáció | `grep -c "még nincs importálva" CLAUDE.md` = 0; `grep -c "Az SDBH/SDGNT hiánya" adat/SEMA.md` = 0 |
| K12 | Nyitott tétel lezárva | az F1.6 tétel áthúzva, `LEZÁRVA`; a `GENERÁLT-KEZDET` és a `GENERÁLT-VÉGE` közötti rész a `git diff`-ben nem változik |
| K13 | SDBH.6 | `grep -c "ma nem ad eredményt" sablonok/4_PaRDeS_tematikus_sablon.md` = 0; `grep -c "^\*v17 — " …` = 1; a diff csak a P2 sort és az új v17 bekezdést érinti |
| K14 | Tétel-szintű commitok | minden `SDBH.*` commitra: `git show --name-only --format= <hash>` pontosan a §5-ben felsorolt fájlokat adja |
| K15 | *(v2)* Az anomália-fájl a §1.4 v2 szerint | 185 sor, az új SHA-256; típusonkénti darabszám és `allapot` az `ellenoriz.py` szerint `OK` |
| K16 | *(v2)* Forrás-leltár | az `ellenoriz.py` leltár-sorai `OK`: szótáranként diszjunkt halmazok, unió = 7 932 / 5 507 |
| K17 | *(v2)* A kivonat és a doménfa nem változott | a `SDBH_domenek.tsv`, a `SDGNT_domenek.tsv` és a `SDBH_SDGNT_domenfa.tsv` SHA-256-ja a §1.4 v1 értéke; a `git diff 6fe0d1e -- <a három fájl>` üres |
| K18 | *(v2)* A `domen` a §3.6 szerint | a §3.6 minden sora; a §3.5 regresszió |
| K19 | *(v2)* Nincs halmaz az anomália-gyűjtésben | a zárójelentés idézi az anomáliákat gyűjtő és író sorokat; K3 és K4 újra |
| K20 | *(v2)* Dokumentáció | `grep -c "150 sora" konkordancia/SDBH_SDGNT_README.md` = 0; `grep -c "jelentes_nelkul"` ≥ 1 a README-ben; `grep -c "150 anomália-sora" NYITOTT_FELADATOK.md` = 0; K12 újra |
| K21 | *(v2)* A 2. menet commitjai | az `SDBH.1a`, `SDBH.2a`, `SDBH.4a`, `SDBH.5a` commit fájllistája a §5 szerint |

---

## 5. Commit és push

Tétel-szintű commitok, magyar üzenettel, UTF-8 fájlból (`git -c i18n.commitEncoding=UTF-8 commit -F commit_uzenet.txt`):

| Commit-üzenet | Fájlok |
|---|---|
| `SDBH.1: SDBH/SDGNT import — import-szkript, jelentés-szintű domén-kivonatok, doménfa, anomália-lista, ellenőrző szkript` | `eszkozok/sdbh_sdgnt_import.py`, `eszkozok/sdbh_sdgnt_ellenoriz.py`, `konkordancia/SDBH_domenek.tsv`, `konkordancia/SDGNT_domenek.tsv`, `konkordancia/SDBH_SDGNT_domenfa.tsv`, `konkordancia/SDBH_SDGNT_anomaliak.tsv` |
| `SDBH.2: SDBH/SDGNT — forrás- és licenc-README, validációs naplóbejegyzés` | `konkordancia/SDBH_SDGNT_README.md`, `konkordancia/README.md`, `konkordancia/Validacios_naplo.md` |
| `SDBH.3: datasetek.tsv — SDBH/SDGNT elérhető; SEMA.md és CLAUDE.md átvezetve` | `adat/datasetek.tsv`, `adat/SEMA.md`, `CLAUDE.md` |
| `SDBH.4: lekerdez.py domen — mező-tágítás és elhatárolás az SDBH/SDGNT kivonatokon` | `eszkozok/lekerdez.py` |
| `SDBH.5: NYITOTT_FELADATOK.md — az SDBH/SDGNT import tétele lezárva` | `NYITOTT_FELADATOK.md` |
| `SDBH.6: tematikus sablon v17 — a P2 domén-mondata állapotfüggetlen` | `sablonok/4_PaRDeS_tematikus_sablon.md` |
| *(v2)* `SDBH.1a: SDBH/SDGNT import — 35 elemzetlen bejegyzés az anomália-fájlba, forrás-leltár ellenőrzés` | `eszkozok/sdbh_sdgnt_import.py`, `eszkozok/sdbh_sdgnt_ellenoriz.py`, `konkordancia/SDBH_SDGNT_anomaliak.tsv` |
| *(v2)* `SDBH.2a: SDBH/SDGNT README — elemzetlen bejegyzések, arámi egység; validációs naplóbejegyzés` | `konkordancia/SDBH_SDGNT_README.md`, `konkordancia/Validacios_naplo.md` |
| *(v2)* `SDBH.4a: lekerdez.py domen — figyelmeztetés elemzetlen bejegyzésre` | `eszkozok/lekerdez.py` |
| *(v2)* `SDBH.5a: NYITOTT_FELADATOK.md — az SDBH-tétel elemzetlen bejegyzésekkel pontosítva` | `NYITOTT_FELADATOK.md` |

A brief saját commitja tétel-azonosító nélkül megy, a 2. menet végén (`SDBH_IMPORT_BRIEF.md v2: az 1. menet független ellenőrzése (§1.5), SDBH.1a–SDBH.5a`), és nem tartozik a K14 és a K21 alá. Az SDBH.0 nem commitol. **Push csak külön kérésre.**

---

## 6. Amit ez a brief szándékosan nem kér

- **A szakasz-profilt** és a `LEXReferences` importját (l. N1).
- **Az anomáliák javítását** — sem kitalált előtaggal, sem kézzel (l. N2).
- **A `lexikon_hivatkozasok.tsv` feltöltését.** Az F6 dolga; a kivonat `szotar`, `entry_id` és `lexid` mezője ehhez illeszkedik (`SEMA.md` 2.5).
- **A terv 4.3 számainak javítását** (l. N5).
- **A `general.py` bármely módosítását** és bármely study vagy motívumnapló érintését.
- **A spanyol, francia, portugál és kínai lokalizációt.** Csak az `en` fájlok kellenek.

---

## 7. Futtatás és modellválasztás

**Két menet, Sonnet.** *(v2: az 1. menet lefutott, `6fe0d1e`; a 2. menet az SDBH.1a–SDBH.5a.)* Migrációs menet (terv D11), soronkénti tartalmi ítélet nélkül. A szabályok és az elvárt értékek a briefben készen állnak.

**Megállási pontok:** az SDBH.0 után, ha bármi eltér; SHA-eltérésnél; a mintánál, ha eltér a §3.5-től; minden commit előtt a hozzá tartozó K-kritériumok; bármely szöveg-horgonynál, ha nem pontosan egy helyen illeszkedik.

### 7.1 Az 1. menet nyitó promptja *(lefutott, `6fe0d1e`)*

```
Olvasd el a CLAUDE.md-t, majd az SDBH_IMPORT_BRIEF.md-t teljes egészében.

0. SDBH.0: main = origin/main = a94b9f9? Mérd újra a brief 1.1 pontját.
   Ha bármi eltér, állj meg és jelentsd — ne írj semmit.
1. SDBH.1: írd meg az eszkozok/sdbh_sdgnt_import.py-t a §2 szabályai szerint.
   Futtasd: --letolt --minta. Ha egyezik a §3.5 megfelelő soraival és a §1.3
   anomáliáival, folytasd; ha nem, állj meg és idézd a kimenetet.
   Teljes futtatás, majd írd meg és futtasd az eszkozok/sdbh_sdgnt_ellenoriz.py-t.
   Futtasd az importot még egyszer (K3). K1–K5, commit.
2. SDBH.2: README-k és validációs naplóbejegyzés. K10, commit.
3. SDBH.3: datasetek.tsv (8 sor, soronkénti összevetéssel), SEMA.md, CLAUDE.md.
   K6, K11, commit.
4. SDBH.4: lekerdez.py domen. Futtasd a §3.5 mind a 11 parancsát.
   K7, K8, K9, commit.
5. SDBH.5: NYITOTT_FELADATOK.md. K12, commit.
6. SDBH.6: sablon P2 + v17 bekezdés. K13, commit.
7. K14 minden SDBH-commitra.

Héber vagy görög karaktert tartalmazó kódot csak fájlból futtass.
Push nincs. A végén zárójelentés: commit-hash-ek, K1–K14 kritériumonként,
az ellenoriz.py teljes kimenete, a §3.5 parancsainak proveniencia-sorai,
és minden eltérés, amit menet közben találtál.
```

### 7.2 A 2. menet nyitó promptja *(v2)*

```
Olvasd el az SDBH_IMPORT_BRIEF.md v2 §1.5 pontját, a §2.4-et és a
„Tételek a 2. menetben” szakaszt.

0. Ellenőrizd: main = origin/main = 6fe0d1e. Ha nem, állj meg.
1. SDBH.1a: import-szkript (jelentes_nelkul, anomáliák listában), majd
   az ellenoriz.py bővítése. Import --letolt kétszer (K3), ellenoriz.py.
   K15, K16, K17, K19. Commit.
2. SDBH.2a: README három helyen + validációs naplóbejegyzés.
   K20 README-része. Commit.
3. SDBH.4a: domen figyelmeztetés. A §3.6 minden sora, a §3.5 regresszió.
   K18. Commit.
4. SDBH.5a: NYITOTT_FELADATOK.md két csere. K20 NYITOTT-része, K12. Commit.
5. K21 a négy commitra. Végül az SDBH_IMPORT_BRIEF.md v2 a gyökérbe,
   saját commit.

Héber vagy görög karaktert tartalmazó kódot csak fájlból futtass.
Push nincs. Zárójelentés: hash-ek, K15–K21 kritériumonként, az
ellenoriz.py teljes kimenete, a §3.6 parancsainak teljes kimenete,
az anomáliákat gyűjtő és író sorok idézve, és minden eltérés.
```

---

## Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | Önálló menet az F5 után, az F6 előtt | Felhasználói döntés (2026-09-15). Az F6 lexikon-generátorának már számolnia kell a doménekkel; így az F6 brief kész adatra épül. |
| D2 | Az SDGNT ugyanebben a menetben | Felhasználói döntés. Azonos séma és parser; a görög oldal külön menetben megduplázná a munkát. |
| D3 | Csak TSV-kivonat a repóban, rögzített commit és SHA-256 mellett | Felhasználói döntés. A nyers JSON 23 MB, és a reprodukáláshoz nem kell; a commit és a hash visszakereshetővé teszi a forrást. |
| D4 | A sor `Strong × jelentés × domén` | Mérés: a H7043 11 doménben szerepel. Strong-szintű join-nal a mező-tágítás minden jelentés doméntársait egybeöntené. |
| D5 | Utótag-levágott `strong` + eredeti `strong_kod` | A TAHOT/TAGNT nem használ betű-utótagot; a join a levágott kódon megy, a homonim bejegyzés az eredetin különíthető el. |
| D6 | `A####` → `H####` | Mérés: 367/367 megtalálható a TAHOT-ban, 362 kizárólag arámi fejezetekben; az öt kivétel Strong-homográf. A `nyelv` oszlop az SDBH oldalán megőrzi a különbséget. |
| D7 | Az összetett (`+`) kód részenként kap sort, `osszetett` jelöléssel | A rész önmagában is kereshető marad, a jelölés pedig mutatja, hogy a domén a kifejezésé, nem a szóé. |
| D8 | Az anomália külön fájlba kerül, javítás nélkül | `CLAUDE.md` 3. szabály: hiány nem tölthető ki kitalált adattal. A `2062` → `H2062` találgatás lenne. Minta: `Karoli_adatminosegi_anomaliak.tsv`. |
| D9 | Görögnél az alcsoport a doménkód, ha van | A 93 Louw–Nida főcsoport túl tág a mező-tágításhoz; az alcsoport (`033055` Bless, Curse) felel meg a héber hierarchikus kód finomságának. A szülő a doménfából kereshető. |
| D10 | `allapot=elerheto`, nem `korlatos` | A `korlatos` a SEMA szerint azt jelenti, hogy máshol az állítás hamis. Itt a hiány nem hamisít, csak nem erősít — ezt a `megjegyzes` és a `domen` kimenete mondja ki. |
| D11 | A `scope` verziót mond (`SDBH-v0.9.2`), nem „teljes”-t | Ugyanaz az elv, mint a `TAHOT-teljes` ↔ `OT-full` megkülönböztetésnél: a címke ne állítson teljességet. |
| D12 | Nincs időbélyeg a generált fájlokban | Byte-azonos újrafuttatás (K3); a forrás-commit és a hash pontosabb proveniencia, mint a futás ideje. |
| D13 | A szakasz-profil kimarad | Versenkénti hivatkozás-táblát kívánna (~390 ezer sor, héber versszámozás); az F6-nak nem előfeltétele. |
| D14 | SDBH.6 külön, elvethető commit, sablon v17 | Az import a P2 első mondatát hamissá teszi, és a mondat tiltja a gépi domén-hivatkozást. Az új mondat állapotfüggetlen, tehát egy későbbi állapotváltás nem avítja el újra. Külön commit, mert sablon-munka. |
| D15 | Elvárt SHA-256 a kimenetre | Kettős megerősítés: a chat-menet referencia-futtatása és a Code független implementációja ugyanarra a byte-sorozatra jut. Eltérésnél a menet megáll, és a számlálók mutatják, hol tér el. |
| D16 | Egy menet, Sonnet | Terv D11: migrációs menet, soronkénti tartalmi ítélet nélkül. *(v2: két menet, l. D21.)* |
| D17 | *(v2)* Az elemzetlen bejegyzés az anomália-fájlba kerül, nem a kivonatba | A kivonat sora jelentés-egységet jelent, elemzetlen bejegyzésnek ilyen nincs. Így a kivonat és az SHA-ja változatlan marad; hogy a lexikon hogyan jelenítse meg a doménnélküli szót, az F6 kérdése. |
| D18 | *(v2)* Külön `allapot`: `FORRASBAN_BEFEJEZETLEN` | Az elemzetlen bejegyzés nem forráshiba; a `AZONOSITVA, NEM JAVITVA` javítandó hibát sugallna. |
| D19 | *(v2)* Új kritérium: forrás-leltár (partíció) | Az L1 azért csúszott át, mert minden számláló a kivonatot mérte. A forrás egészéből induló leltár ezt a hibaosztályt fogja meg: ami sehova sem kerül, az a különbségben látszik. |
| D20 | *(v2)* A `domen` akkor is figyelmeztet, ha van elemzett sor, és a `forras` mindig két fájlt nevez meg | Különben az elemzetlen homonim (`H0001`, `H8213b`) láthatatlan maradna. A proveniencia azt mondja, amit a lekérdezés ténylegesen olvasott. |
| D21 | *(v2)* Javítás külön, `a`-jelű tételekben; a v1 commitok nem íródnak át | Push után vannak; az `F5_BRIEF.md` D12 mintája. A hiba és a javítás a történetben is nyomon követhető. |

### Nyitott, a briefben szándékosan el nem döntött kérdések

- **N1 — Szakasz-profil.** A terv harmadik `domen`-használata. Versenkénti táblát kíván a `LEXReferences`-ből (14 jegyű kód: könyv 3, fejezet 3, vers 3, szó-pozíció 5; a könyvszám a 66 könyves protestáns sorrend, az ÚSZ 040-nel kezdődik), héber versszámozással, a `Konyv_normalizalo_tabla.tsv`-hez illesztve. Mikor, és kell-e egyáltalán?
- **N2 — Az anomáliák sorsa.** 150 hibás sor, köztük a szerzőnév Strong-mezőben *(v2: a 35 elemzetlen bejegyzés nem hiba, ide nem tartozik)*. Jelezni az UBS felé (issue), vagy kézi leképező táblát vezetni, forrás-ellenőrzéssel?
- **N3 — Licenc-publikálás (terv N11).** A CC BY-SA 4.0 miatt a domén-hivatkozást tartalmazó lexikon-kimenet is ShareAlike. Az F6 brief előfeltétele.
- **N4 — SECE_G vagy SDGNT a görög doménhez.** Mindkettő Louw–Nida alapú. A lexikonban melyik legyen a kanonikus hivatkozás (`lexikon_hivatkozasok.szotar`)?
- **N5 — A terv 4.3 számai.** 381 → 380 (+208 üres kódú jelentés), 8 976 → 8 975. Javítandó-e a terv szövege, vagy elég ez a brief és a README?
- **N6 — A Strong-homográfok hatása a `scan`-re.** Az öt kódnál (`H1529`, `H2269`, `H5613`, `H6211`, `H8412`) a TAHOT-scan héber és arámi szót együtt ad vissza. Jelezze-e ezt a `scan`?
- **N7 — Gyakori szavak hiánya.** A `H1961` (lenni) és a `H5414` (adni) teológiailag is terhelt. Ha motívum-gerincen állnak, a P2-nek nincs gépi támasza. Kell-e erre külön figyelmeztetés a sablonban?
