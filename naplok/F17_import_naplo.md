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
2. **`KEZI` osztályú sornál, ha az `igehely_mt` üres, az `igehely_kjv` az irányadó** (`kk_mod=kk_kjv`; a KJV- és az MT-számozás
   ezekben a könyvekben azonos). *Javítás (F17.4):* az első kötés csak az `igehely_mt`-t olvasta, ezért a KEZI-osztályú
   Károli-versek (291 KK-sor: 189 `kezi`, 101 `kezi_identitas_javitas`, 1 `kezi_tobbforrasu_osszevonas`; 4Móz 13, Jób 39–40,
   Préd 2/9/10/12 stb.) identitást kaptak; az `igehely_kjv` alapján 283 Károli-vers kötése lett `kk_kjv`. Igazolás a `lekerdez.py karoli`-val: Károli `4Móz 13:34` (óriások) = KK szerint 13:33;
   Károli `Préd 9:10` (fehér ruha) = KJV/MT 9:8. Az import ezután 4Móz 13:34 → MT 13:33, Préd 9:10 → MT 9:8;
3. `LXX_versificacios_terkep.tsv` `Heber_vers` oszlopa (`kk_mod=terkep`), de **az `EGYIK_SEM` sorokat nem használom**:
   ezeknél a Károli-számozás egyik hagyománnyal sem egyezik, és a `Heber_vers` nem megbízható (példa: `1Móz 37:1` →
   `Gen.36:44`, ami nem létezik); az `ELLENORZESRE_VAR` sor `javaslat`;
4. különben identitás, ha a Károli-vers a KK-táblában szerepel (`kk_mod=identitas`); az `EGYIK_SEM` terkep-sorú versek
   identitása `javaslat:terkep_egyik_sem_identitas` (85 Károli-vers).

Egy MT-vers több Károli-verset is kaphat (összevonás), ekkor a `karoli` mező `;`-vel elválasztott.

Károli-vers a kötés forrása szerint: `identitas` 17 243, `identitas_terkep_egyik_sem` 85, `kk_mt` 1 713, `kk_kjv` 283,
`terkep` 3 701. **Ütközés a KK és a terkep között:** 1 160 Károli-versnél eltér (legtöbb a Zsolt, 1Sám 24, Ézs 9, 1Kir 22,
Jón 2); a KK az irányadó, nem döntöttem, az `utkozesek` listát a `macula_kk.karoli_mt_terkep()` adja vissza.

**Az `allapot` oszlop jelentése (F17.4):** `rendben` csak akkor, ha a KK-kötés igazolt (`identitas`, `kk_mt`, `kk_kjv`, `terkep`
javaslat-ok nélkül) **és** a Strong-illesztés `igen`. Minden más `javaslat:<ok>` (a KK-oldali ok: `nincs_karoli_vers`,
`terkep_ellenorzesre_var`, `terkep_egyik_sem_identitas` …; a Strong-oldali ok `strong_<ok>`, pl. `strong_funkcio_kod`),
a brief 2. lépése szerint („ahol a Strong-szám vagy a KK-vers nem illeszthető, `javaslat`”). A csak-KK bontás a
`naplok/F17_import_stat.json` `heber.allapot_csak_kk` mezőjében van.

| Héber sor | db |
|---|---|
| `allapot=rendben` | 294 329 |
| `allapot=javaslat` (összesen) | 181 582 |
| ebből csak a KK-kötés miatt (`allapot_csak_kk`, Strong-tól függetlenül) | 5 797 |
| MT-vers a Maculában / ebből Károli-megfelelővel | 23 213 / 23 004 (209 MT-vers nincs Károli-párja) |
| Károli-vers a KK/terkep szerint / ebből Macula nélkül | 23 025 / 16 |
| Károli-vers KK-osztály nélkül (EGYIK_SEM fejezet) | 179 |

A KK-osztály nélküli 179 Károli-vers és a párjuk nélküli MT-versek (pl. 2Móz 35–36, Dán 3) a 13 `EGYIK_SEM` fejezetből
adódnak (`F01_KAROLI_KULCS_BRIEF.md`: a KK ezeket szándékosan nem osztályozza). Ezek `naplok/F17_illesztetlen.tsv`-ben vannak,
`javaslat` jelöléssel; **nem találgattam**.

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

Az előző verzió naplója azt állította, hogy „mind a 87 helyen azonos a Károli- és az MT-számozás”; **ez hamis volt** — a
KK `igehely_kjv` oszlopát nem olvastam. A korábbi 87/87 egyezés az F06-tal **közös módszerhiba** volt: sem az F06 (számozás-
átalakítás nélkül), sem az első F17 (csak `igehely_mt`) nem tekintette a KEZI-számozást.

**Új lelet a Préd 9:10-ről (a #8-nak):** a munkalap `heber_kulcsszo` értéke `שְׁאוֹל`, és a Macula szerint ez a szó MT `Préd 9:10`-ben
van (Károli-számozásban `Préd 9:12`, a KK szerint), nem MT 9:8-ban. Vagyis a munkalap `Préd 9:10` igehelye valószínűleg
**nem Károli-, hanem KJV/MT-számozású**. Ha ez így van, a sor helyes kötése MT 9:10 → LXX-megfelelő `ἅδη`, és a
munkalap igehelyeinek számozási alapja (Károli vs. KJV/MT) sor-szinten ellenőrizendő. Nem döntöttem el; a `DT-F17` (g) pontja.

A 38 sor továbbra is **javaslat, kézi megerősítést igényel** (az F06 szerint a Macula szó-szintű illesztése 78,3%).
A fájl `allapot` oszlopa a gépi keresés kimenete (nem döntés); a `kk_mod` `:`-os utótagja a KK-kötés bizonytalanságát jelzi.

## 6. Illeszthetetlen sorok (brief 2. lépés)

`naplok/F17_illesztetlen.tsv`: 1 460 adatsor, minden `allapot=javaslat` (D19).

| Típus | Héber | Görög N1904 | Görög SBLGNT |
|---|---|---|---|
| `macula_vers_nincs_karoli` | 209 | 4 | 3 |
| `karoli_vers_nincs_macula` | 195 | 15 | 18 |
| `strong_nem_illesztheto` (Strong-kódonként) | 1 014 | 1 | 1 |

## 7. Szerepmátrix és datasetek

- **`adat/szotar_szerepek.tsv`: nem módosítottam** (az F17.3-ban felvett `heber 11` és `gorog 11` sort F17.4 visszavonta): a SEMA 2.13
  10 szerep × 2 nyelv = 20 sort rögzít (sorrend 1–10); a Macula-szerep felvétele SEMA-bővítést igényel, a döntés a
  felhasználóé (DT-F17 (f)).
- **`adat/datasetek.tsv`:** felvéve a `Macula_heber` és a `Macula_gorog` (mindkettő `ajanlott`, `elerheto`, négy study-típusra:
  +8 sor). A SEMA 2.6 „17 dataset × 4 = 68 sor” száma nem frissült (SEMA-módosítás kívül esik a hatókörön); a #16 ága is bővíti a
  táblát, rebase-nél mindkét oldal sorai maradnak.

## 8. Ismert korlátok

- A KK–terkep ütközés 1 160 Károli-versnél; a KK irányadó, nem verifikáltam tartalmilag (nincs szó-szintű Károli–héber illesztés).
- 85 Károli-vers identitása (`javaslat:terkep_egyik_sem_identitas`) feltevés.
- A Macula `greek`/`greekstrong` (LXX-megfelelő) szó-szintű, gépi; az FJ1 78,3%-osnak mérte (átvett szám).
- A TAHOT_kivonat és a Macula közti verslista-eltérések oka (F06 5. pont) továbbra sincs vizsgálva.
