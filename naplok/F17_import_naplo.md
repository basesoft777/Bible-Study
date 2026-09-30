# F17 — Macula-import naplója (héber és görög)

*FELADATOK #17 · N31 · brief: `F17_MACULA_IMPORT_BRIEF.md` · ág: `claude/macula-import` · 2026.09.30*
*Proveniencia: scope=teljes import | forras=Clear-Bible/macula-hebrew@47db250b…, Clear-Bible/macula-greek@8423afe4… | ts=2026-09-30*

A számokat a `naplok/F17_import_stat.json` adja (a `eszkozok/f17/macula_futtat.py` kimenete); az F06-os
összevetés számai a PR #75 mérési fájljaiból (`naplok/F06_macula_*.tsv`) valók.

## 1. Forrás, licenc, verzió

| | Héber | Görög |
|---|---|---|
| Repó | `https://github.com/Clear-Bible/macula-hebrew` | `https://github.com/Clear-Bible/macula-greek` |
| Verzió | commit `47db250bd55d0d8577f2a94fba114ef16c35b23c` (azonos az F06 mérésével) | commit `8423afe47b9e8f24b7772e808af45c7159a6fe7e` |
| Bemenet | `WLC/lowfat/NN-Kod-FFF-lowfat.xml`, 929 fájl (a 930. `macula-hebrew-lowfat.xml` az egész Biblia összevont fájlja; nem olvasva, nehogy kétszer számoljon) | `Nestle1904/tsv/macula-greek-Nestle1904.tsv`, `SBLGNT/tsv/macula-greek-SBLGNT.tsv` |
| Licenc | CC BY 4.0 © Biblica, Inc (`LICENSE.md` 3. sor) | CC BY 4.0 © Biblica, Inc (`LICENSE.md` 3. sor) |
| Kimenet | `konkordancia/Macula_heber.tsv`: **475 911 sor** (= a lowfat `<w>` elemek száma; morféma-szint) | `konkordancia/Macula_gorog.tsv`: **275 520 sor** (N1904 137 779 + SBLGNT 137 741; szó-szint) |

### Licenc-összevetés (brief 1. lépés) — nincs ütközés, ezért nincs ⛔

- A Macula CC BY 4.0. A repóba felvétel megengedett, feltétele az attribúció („MACULA Hebrew/Greek Linguistic Datasets,
  available at https://github.com/Clear-Bible/…”). Ez a két konkordancia-fájl fejlécében (`forras=… | licenc=…`) áll.
- A repó saját licencrendszerét az F24 (#24) rendezi; a CC BY (nem SA, nem NC) nem szab feltételt a repó licencére.
- **Kivétel, amit nem importáltam: az UBS-től „Used with permission” származó mezők.** A `macula-hebrew/LICENSE.md` 21. sora
  és a `macula-greek/LICENSE.md` 3. pontja szerint a szemantikai domének és szójelentés-adatok (héber `sdbh`, `lexdomain`,
  `coredomain`, `contextualdomain`, `sensenumber`; görög `domain`, `ln`) a Semantic Dictionary of Biblical Hebrew / MARBLE
  forrásból jönnek, engedéllyel, **nem CC BY**. Ezek a mezők **nem kerültek be** — így nincs licencütközés. (A repóban az
  SDBH/SDGNT a `konkordancia/SDBH_SDGNT_README.md` szerint már CC BY-SA 4.0 forrásból van; az F06 jelentés 4. pontja szerint
  a Macula-oldali SDBH-engedély külön tisztázandó, ha a domének kellenének. Ezt a döntést nem hoztam meg: l. DT-F17.)
- A görög `gloss` a Berean Interlinear (közkincs 2023.04.30 óta), az `english` a Cherith Glosses (CC BY 4.0). Ezek bekerültek.

## 2. Mit importáltam (oszlopok)

Héber (`Macula_heber.tsv`): `xml_id`, `ref` (Macula/MT-számozás, `GEN 1:1!1`), `karoli`, `kk_mod`, `allapot`, `szo`, `lemma`,
`strong`, `strong_x` (a Macula `strongnumberx` nyers értéke), `strong_illesztes`, `morf`, `szofaj`, `gloss`, `gorog_lxx`,
`gorog_strong`. Görög (`Macula_gorog.tsv`): `kiadas` (N1904 | SBLGNT), `xml_id`, `ref`, `karoli`, `kk_mod`, `allapot`, `szo`,
`lemma`, `strong`, `strong_x`, `strong_illesztes`, `morf`, `szofaj`, `gloss`, `english`.

**Nem importált** (mérethatár vagy nem kell; javaslat: később külön, ha kell): héber `mandarin`, `transliteration`, `english`
(a `gloss` megvan), `frame`, `participantref`, `subjref`, `after`, nyelvtani jegyek (`gender`, `number`, `person`, `stem`,
`state`) — a `morf` kód hordozza; görög `mandarin`, `after`, `normalized`, nyelvtani jegyek, `frame`, `subjref`, `referent`, `role`.

**Fájlméret:** `Macula_heber.tsv` ≈ 65 millió bájt (~62 MiB; a repó eddigi legnagyobb tábla 26 MB). A GitHub 50 MB fölött
figyelmeztet, 100 MB fölött tilt. Javaslat a DT-F17 (e) pontjában.

## 3. A Károli-kulcshoz (KK) kötés

A Macula héber MT-számozású (WLC), a Károli-szöveg fejezetenként KJV- vagy MT-számozású. Az illesztés Károli-verstől indul,
és megfordul (`eszkozok/f17/macula_kk.py`); a Károli-versek halmaza a `Karoli_1908.tsv`. Sorrend:

1. `Karoli_versmegfeleltetes.tsv` `igehely_mt` oszlopa, ha ki van töltve (`kk_mod=kk_mt`; tartalmilag ellenőrzött);
2. **`KEZI` osztályú sornál, ha az `igehely_mt` üres, az `igehely_kjv` (több forrású összevonásnál a megjegyzés `raw=A;raw=B`
   listája) a KJV-számozás — de csak ott irányadó MT-nek (`kk_mod=kk_kjv`), ahol a KJV = MT azonosság igazolt.** *Javítás (F17.5):*
   az F17.4 a KJV-t mindenhol MT-nek vette; ez **Dán 4-re hamis** (a 3. fejezet KJV 30 / MT 33 vers, ezért KJV 4:4 = MT 4:1;
   Károli `Dán 4:1` „Én Nabukodonozor békében valék” = KJV 4:4 = MT 4:1, nem MT 4:4). Az igazolás fejezetenként
   (`naplok/F17_kezi_fejezetek.tsv`): a KJV-fejezet versszáma (`KAROLI_KK1b_fejezetosztaly.tsv` `kjv_max`) és a Macula MT-fejezet
   tényleges versszáma; a kötés akkor igazolt, ha az **előző fejezet** KJV- és MT-versszáma azonos (nincs fejezet eleji eltolódás),
   és a vers mindkét oldalon létezik. (Kumulált összeget nem használtam: a KK1b `kjv_max`-a a 4Móz 6-ra 26, a KJV-ben 27 a vers,
   így az összeg hamis eltolódást mutatna.) Eredmény a KEZI-fejezetekre: a 13 fejezet közül **12 igazolt** (4Móz 12, 13;
   Jób 38, 39, 40; Préd 1, 2, 8, 9, 10, 11, 12), **1 nem igazolt: Dán 4** (34 KEZI-sor, előző fejezet különbsége −3) →
   `javaslat:kk_kjv_mt_nem_igazolt`, **nincs MT-megfelelő** (a Károli Dán 4 ↔ MT 4 illesztetlen; a −3 eltolás számítható lenne,
   de nem igazolt, ezért nem alkalmaztam). Igazolt sorok: 249 Károli-vers `kk_kjv`. Példák a `lekerdez.py karoli`-val:
   `4Móz 13:34` (óriások) → MT 13:33; `Préd 9:10` (fehér ruha) → MT 9:8; `Jób 40:1` („Ekkor szóla az Úr Jóbnak”) → KJV/MT 40:6;
   a `Préd 2:26` (`raw=2:25;raw=2:26`) → MT 2:25 **és** 2:26 (a Károli-vers két MT-verset foglal magába);
3. **hiányzó vagy üres KEZI-sorú Károli-vers interpolációja** (`kk_mod=kezi_interpolalt`, `javaslat:kezi_interpolalt`): ha a
   Károli-vers nincs a KK-ban (vagy KEZI-sora üres igehelyű), és a következő Károli-vers (akár a következő fejezet első verse)
   igazolt `kk_kjv`-horgony vagy már interpolált, akkor az MT-megfelelője a horgony MT-versének megelőző MT-verse. Példák:
   Károli `Jób 39:1–3` = MT 38:39–41 (a Károli 39:1–3 nincs a KK-ban), Károli `Jób 39:34–38` = MT 40:1–5, `4Móz 13:1` = MT 12:16;
   a lánc visszafelé továbbmegy (Károli Jób 37–38, Préd 2:1, 9:1–2, 9:21–23, 12:1–2). Összesen 40 Károli-vers;
   **ez következtetés, ezért `javaslat`**, nem KK-igazolás;
4. `LXX_versificacios_terkep.tsv` `Heber_vers` oszlopa (`kk_mod=terkep`), de **az `EGYIK_SEM` sorokat nem használom**:
   ezeknél a Károli-számozás egyik hagyománnyal sem egyezik, és a `Heber_vers` nem megbízható (példa: `1Móz 37:1` →
   `Gen.36:44`, ami nem létezik); az `ELLENORZESRE_VAR` sor `javaslat`;
5. különben identitás, ha a Károli-vers a KK-táblában szerepel (`kk_mod=identitas`); az `EGYIK_SEM` terkep-sorú versek
   identitása `javaslat:terkep_egyik_sem_identitas` (85 Károli-vers).

**Tekintély-szabály (F17.5):** az az MT-vers, amelyet a KK (`kk_mt`, igazolt `kk_kjv`) vagy az interpoláció igényel, **nem köthető
más Károli-versre a terkep/identitás útján** (a terkep-kötés visszavonva, `javaslat:mt_vers_kk_val_foglalt`). Példa: a terkep a
Károli `Jób 39:1`-et az MT 39:1-hez és a `4Móz 13:1`-et az MT 13:1-hez kötötte (tévesen: MT 38:39, ill. MT 12:16), ezért az MT 39:1
és MT 13:1 két Károli-verset kapott (`karoli` = `Jób 39:1;Jób 39:4`, 24 `rendben` sor). Most az MT 39:1 → csak Károli `Jób 39:4`,
az MT 38:39–41 → Károli `Jób 39:1–3`, az MT 12:16 → Károli `4Móz 13:1`.

Egy MT-vers több Károli-verset is kaphat (összevonás, pl. `Neh 7:68;Neh 7:69`), ekkor a `karoli` mező `;`-vel elválasztott.

Károli-vers a kötés forrása szerint: `identitas` 17 243, `identitas_terkep_egyik_sem` 85, `kk_mt` 1 713, `kk_kjv` 249,
`kk_kjv_nem_igazolt` 34, `kezi_interpolalt` 40, `terkep` 3 701. **Ütközés a KK `igehely_mt` és a terkep között:** 1 048
Károli-versnél eltér (legtöbb a Zsolt, 1Sám 24, Ézs 9, 1Kir 22, Jón 2); a KK az irányadó, nem döntöttem, az `utkozesek` listát a
`macula_kk.karoli_mt_terkep()` adja vissza.

**Az `allapot` oszlop jelentése (F17.4):** `rendben` csak akkor, ha a KK-kötés igazolt (`identitas`, `kk_mt`, igazolt `kk_kjv`, `terkep`
javaslat-ok nélkül) **és** a Strong-illesztés `igen`. Minden más `javaslat:<ok>` (a KK-oldali ok: `nincs_karoli_vers`,
`terkep_ellenorzesre_var`, `terkep_egyik_sem_identitas`, `kezi_interpolalt`, `mt_vers_kk_val_foglalt` …; a Strong-oldali ok
`strong_<ok>`, pl. `strong_funkcio_kod`), a brief 2. lépése szerint („ahol a Strong-szám vagy a KK-vers nem illeszthető, `javaslat`”).
A csak-KK bontás a `naplok/F17_import_stat.json` `heber.allapot_csak_kk` mezőjében van.

| Héber sor | db |
|---|---|
| `allapot=rendben` | 293 808 |
| `allapot=javaslat` (összesen) | 182 103 |
| ebből csak a KK-kötés miatt (`allapot_csak_kk`, Strong-tól függetlenül) | 6 705 |
| MT-vers a Maculában / ebből Károli-megfelelővel | 23 213 / 23 014 (199 MT-vers nincs Károli-párja; ebből Dán 34 a 4. fejezetben) |
| Károli-vers a KK/terkep szerint / ebből Macula nélkül | 23 025 / 39 |
| Károli-vers KK-osztály nélkül (EGYIK_SEM fejezet) | 151 |

A KK-osztály nélküli 151 Károli-vers és a párjuk nélküli MT-versek (pl. 2Móz 35–36, Dán 1, 3, Jób 17) a 13 `EGYIK_SEM` fejezetből
adódnak (`F01_KAROLI_KULCS_BRIEF.md`: a KK ezeket szándékosan nem osztályozza). Ezek `naplok/F17_illesztetlen.tsv`-ben vannak,
`javaslat` jelöléssel; az interpolációt kivéve (3. pont) nem találgattam.

**Görög (ÚSZ):** identitás a Károli-versekkel; a 8 sorú `Verzifikacios_elteres_tabla.tsv` az egyetlen kivétel-forrás
(`kk_mod=verzifikacios_tabla`, `javaslat`). N1904: 137 704 `rendben` / 75 `javaslat` sor; SBLGNT: 137 699 / 42.
Macula-vers Károli nélkül: N1904 4, SBLGNT 3 (pl. `Róm 3:31`, `Róm 8:39`, `1Kor 3:23`, `Mk 16:99`); Károli-vers Macula nélkül:
N1904 15, SBLGNT 18 (a szövegkritikai kihagyások: `Mt 17:21`, `Mt 18:11`, `Mk 9:44`, `ApCsel 8:37` stb.).

## 4. A Strong-számhoz kötés — és egy csapda

**A Macula héber `strongnumberx` értéke nem mindig Strong-szám.** A betűs kód (pl. `0871a`, `2050b`, `1886a`) a funkció-morfémáknál
(elő-/utótagok, kötőszó, névelő, ragok) Macula-azonosító, nem Strong-szám: `0871a` a `bə-` előtag (`in`), míg a
`Strong_szotar.tsv` `H0871`-e az „Atharim” helynév. Ha a számjegyeket vakon `H####`-vá alakítom, az első futásban 176 219
betűs sorban lett volna hamis Strong-egyezés.

Szabály (`macula_import.strong_feldolgoz`, F17.4-es szigorítással):

| `strong_illesztes` | Jelentés | Héber sor |
|---|---|---|
| `igen` | tiszta szám, a `Strong_szotar.tsv`-ben szerepel → `strong=H####` | 297 981 |
| `javaslat:betu_alap` | betűs kód + tartalmi szófaj (főnév, ige, melléknév, határozószó, névmás), egyetlen kód, és a szám családja sehol sem funkció-morféma → az alapszám; a betűs változat nincs feloldva | 5 790 |
| `javaslat:funkcio_kod` | betűs kód + funkció-morféma, vagy olyan számcsalád, amelynek valamely eleme elő-/utótag/kötőszó (pl. `1886a/c/d`) → **`strong` üres**, a `strong_x` őrzi a nyers kódot | 170 429 |
| `javaslat:funkcio_kod\|tobbes` | `\|`-jelű többes kód egy elemen és valamelyik rész nem Strong (pl. Zak 2:13 `5921\|3963a`; Bír 9:41 `1886a\|0725`; 1Krón 2:52 `1886a\|7204a`) → **`strong` üres** (nem találgatok) | 5 |
| `javaslat:nincs_strong` | nincs vagy 0 (pl. tulajdonnév-részletek) | 1 706 |

Javítás (F17.4): a független ellenőr szerint az első verzió `H1886`-ot (a `1886a/1886d` névelő-/ragkódok alapszámát, ami a
Strong-szótárban Dothan) adott néhány sorra (Bír 13:14, Bír 9:41, 1Krón 2:52), és a Zak 2:13 két `tobbes` sora `H5921`-et
kapott. A szabály most a számcsaládra és a többes kódra is kiterjed, így ezek `strong` mezője üres.

A funkció-morfémák STEP-megfelelője a 9000-es sáv (`H9001`…); a leképezésük nem a feladat tárgya (DT-F17 (b)).
Görög: 137 777 / 137 739 sor `igen` (N1904 / SBLGNT), a maradék 2-2 sor `nincs_strong` (`Ἀρνεί`, a 0 Strong).
Az összetett görög Strong (`1417+3461`) a SEMA 1.2 szerint `G1417+G3461`. A `naplok/F17_illesztetlen.tsv` a Strong-oldali
illeszthetetlent Strong-kódonként összesítve tartalmazza (1 016 sor).

## 5. A #8 ellenőrző száma (brief 3. lépés) — **eltér az F06-tól**

A 87 függő hely (a `naplok/FORRAS_FJ1_lxx_jeloltek.tsv` sorai) a `naplok/F17_87_hely.tsv`-ben: a Károli-számozású igehelyet a KK
alapján MT-versre váltottam (`igehely_mt`, KEZI osztálynál `igehely_kjv`), majd a Macula szavai között a `heber_strong`
(számjegy-egyezés), ennek híján a szóalak alapján kerestem.

| Állapot | F17 (javított KK-kötéssel) | F17 első verzió (hibás: `igehely_kjv` nélkül) | F06 (PR #75, számozás-átalakítás nélkül) |
|---|---|---|---|
| **LXX_MEGFELELO** | **38** | 39 | 39 |
| HEBER_SZO_GOROG_NELKUL | 40 | 38 | 38 |
| HEBER_SZO_NINCS_A_VERSBEN | 9 | 8 | 8 |
| NINCS_VERS | 0 | 2 | 2 |

**A szám 39-ről 38-ra változott, három sor tér el az F06-tól (`egyezik_f06 = nem`):**
- `4Móz 13:34` (HODIT-001 és MENNY-001): F06/első verzió `NINCS_VERS`; most MT 13:33 → `HEBER_SZO_GOROG_NELKUL` (a szó megvan,
  görög Strong nincs rendelve);
- `Préd 9:10` (ALVIL-001): F06/első verzió `LXX_MEGFELELO` (`ἅδη`); most MT 9:8 → `HEBER_SZO_NINCS_A_VERSBEN`.

**F17.5 újraszámolás** (Dán 4 kizárása, a terkep-kötés visszavonása, a több-raw és az interpolált sorok kezelése után): az eredmény változatlan, **38 / 40 / 9 / 0**, az F06-tól eltérő 3 sor ugyanaz. A három sor fejezete igazolt (4Móz 13, Préd 9), tehát a szám a KEZI-igazolásra nem érzékeny.

Az F17.4-es napló azt állította, hogy „mind a 87 helyen azonos a Károli- és az MT-számozás”; **ez hamis volt** — a
KK `igehely_kjv` oszlopát nem olvastam. A korábbi 87/87 egyezés az F06-tal **közös módszerhiba** volt: sem az F06 (számozás-
átalakítás nélkül), sem az első F17 (csak `igehely_mt`) nem tekintette a KEZI-számozást.

**Új lelet a Préd 9:10-ről (a #8-nak):** a munkalap `heber_kulcsszo` értéke `שְׁאוֹל`, és a Macula szerint ez a szó MT `Préd 9:10`-ben
van (Károli-számozásban `Préd 9:12`, a KK szerint), nem MT 9:8-ban. Vagyis a munkalap `Préd 9:10` igehelye valószínűleg
**nem Károli-, hanem KJV/MT-számozású**. Ha ez így van, a sor helyes kötése MT 9:10 → LXX-megfelelő `ἅδη`, és a
munkalap igehelyeinek számozási alapja (Károli vs. KJV/MT) sor-szinten ellenőrizendő. Nem döntöttem el; a `DT-F17` (g) pontja.

A 38 sor továbbra is **javaslat, kézi megerősítést igényel** (az F06 szerint a Macula szó-szintű illesztése 78,3%).
A fájl `allapot` oszlopa a gépi keresés kimenete (nem döntés); a `kk_mod` `:`-os utótagja a KK-kötés bizonytalanságát jelzi.

## 6. Illeszthetetlen sorok (brief 2. lépés)

`naplok/F17_illesztetlen.tsv`: 1 445 adatsor, minden `allapot=javaslat` (D19).

| Típus | Héber | Görög N1904 | Görög SBLGNT |
|---|---|---|---|
| `macula_vers_nincs_karoli` | 199 | 4 | 3 |
| `karoli_vers_nincs_macula` | 190 | 15 | 18 |
| `strong_nem_illesztheto` (Strong-kódonként) | 1 014 | 1 | 1 |

## 7. Szerepmátrix és datasetek

- **`adat/szotar_szerepek.tsv`: nem módosítottam** (az F17.3-ban felvett `heber 11` és `gorog 11` sort F17.4 visszavonta): a SEMA 2.13
  10 szerep × 2 nyelv = 20 sort rögzít (sorrend 1–10); a Macula-szerep felvétele SEMA-bővítést igényel, a döntés a
  felhasználóé (DT-F17 (f)).
- **`adat/datasetek.tsv`:** felvéve a `Macula_heber` és a `Macula_gorog` (mindkettő `ajanlott`, `elerheto`, négy study-típusra:
  +8 sor). A SEMA 2.6 „17 dataset × 4 = 68 sor” száma nem frissült (SEMA-módosítás kívül esik a hatókörön); a #16 ága is bővíti a
  táblát, rebase-nél mindkét oldal sorai maradnak.

## 8. Ismert korlátok

- A KK–terkep ütközés 1 048 Károli-versnél; a KK irányadó, nem verifikáltam tartalmilag (nincs szó-szintű Károli–héber illesztés).
- 85 Károli-vers identitása (`javaslat:terkep_egyik_sem_identitas`) feltevés.
- A Macula `greek`/`greekstrong` (LXX-megfelelő) szó-szintű, gépi; az FJ1 78,3%-osnak mérte (átvett szám).
- A TAHOT_kivonat és a Macula közti verslista-eltérések oka (F06 5. pont) továbbra sincs vizsgálva.
