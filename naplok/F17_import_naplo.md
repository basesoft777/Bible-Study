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

**Fájlméret:** `Macula_heber.tsv` ≈ 61,5 MB (a repó eddigi legnagyobb tábla 26 MB). A GitHub 50 MB fölött figyelmeztet,
100 MB fölött tilt. Javaslat a DT-F17-ben.

## 3. A Károli-kulcshoz (KK) kötés

A Macula héber MT-számozású (WLC), a Károli-szöveg fejezetenként KJV- vagy MT-számozású. Az illesztés Károli-verstől indul,
és megfordul (`eszkozok/f17/macula_kk.py`); a Károli-versek halmaza a `Karoli_1908.tsv`. Sorrend:

1. `Karoli_versmegfeleltetes.tsv` `igehely_mt` oszlopa, ha ki van töltve (`kk_mod=kk_mt`; tartalmilag ellenőrzött);
2. `LXX_versificacios_terkep.tsv` `Heber_vers` oszlopa (`kk_mod=terkep`), de **az `EGYIK_SEM` sorokat nem használom**:
   ezeknél a Károli-számozás egyik hagyománnyal sem egyezik, és a `Heber_vers` nem megbízható (példa: `1Móz 37:1` →
   `Gen.36:44`, ami nem létezik); az `ELLENORZESRE_VAR` sor `javaslat`;
3. különben identitás, ha a Károli-vers a KK-táblában szerepel (`kk_mod=identitas`); az `EGYIK_SEM` terkep-sorú versek
   identitása `javaslat:terkep_egyik_sem_identitas` (119 Károli-vers, 2751+20 héber sor).

Egy MT-vers több Károli-verset is kaphat (összevonás), ekkor a `karoli` mező `;`-vel elválasztott.

**Ütközés a KK és a terkep között:** 1048 Károli-versnél a KK `igehely_mt` és a terkep `Heber_vers` eltér (legtöbb a Zsolt,
1Sám 24, Ézs 9, 1Kir 22, Jón 2). Ott a KK az irányadó (nem döntöttem; a `naplok/` alatt nincs külön lista, a szkript
`macula_kk.karoli_mt_terkep()` visszaadja az `utkozesek` listát).

| Héber eredmény | sor |
|---|---|
| `allapot=rendben` | 469 028 |
| `allapot=javaslat` (ebből 3777 `nincs_karoli_vers`) | 6 883 |
| MT-vers a Maculában / ebből Károli-megfelelővel | 23 213 / 23 003 (210 MT-vers nincs Károli-párja) |
| Károli-vers a KK/terkep szerint / ebből Macula nélkül | 23 025 / 21 |
| Károli-vers KK-osztály nélkül (EGYIK_SEM fejezet) | 179 |

A KK-osztály nélküli 179 Károli-vers és a párjuk nélküli MT-versek (pl. 2Móz 35–36, Dán 1, 3) a 13 `EGYIK_SEM` fejezetből
adódnak (`F01_KAROLI_KULCS_BRIEF.md`: a KK ezeket szándékosan nem osztályozza). Ezek `naplok/F17_illesztetlen.tsv`-ben vannak,
`javaslat` jelöléssel; **nem találgattam**.

**Görög (ÚSZ):** identitás a Károli-versekkel; a 8 sorú `Verzifikacios_elteres_tabla.tsv` az egyetlen kivétel-forrás
(`kk_mod=verzifikacios_tabla`, `javaslat`). N1904: 137 706 `rendben` / 73 `javaslat` sor; SBLGNT: 137 701 / 40.
Macula-vers Károli nélkül: N1904 4, SBLGNT 3 (pl. `Róm 3:31`, `Róm 8:39`, `1Kor 3:23`, `Mk 16:99`); Károli-vers Macula nélkül:
N1904 15, SBLGNT 18 (a szövegkritikai kihagyások: `Mt 17:21`, `Mt 18:11`, `Mk 9:44`, `ApCsel 8:37` stb.).

## 4. A Strong-számhoz kötés — és egy csapda

**A Macula héber `strongnumberx` értéke nem mindig Strong-szám.** A betűs kód (pl. `0871a`, `2050b`, `1886a`) a funkció-morfémáknál
(elő-/utótagok, kötőszó, névelő, ragok) Macula-azonosító, nem Strong-szám: `0871a` a `bə-` előtag (`in`), míg a
`Strong_szotar.tsv` `H0871`-e az „Atharim” helynév. Ha a számjegyeket blindra `H####`-vá alakítom, **az első futásban 176 219 betűs sorban hamis
Strong-egyezést** kaptam volna (az első futásban így is lett; az `Atharim` a `be-` előtagra).

Szabály (`macula_import.strong_feldolgoz`):

| `strong_illesztes` | Jelentés | Héber sor |
|---|---|---|
| `igen` | tiszta szám, a `Strong_szotar.tsv`-ben szerepel → `strong=H####` | 297 981 |
| `javaslat:betu_alap` | betűs kód + tartalmi szófaj (főnév, ige, melléknév, határozószó, névmás) → az alapszám; a betűs változat nincs feloldva | 6 313 (+2 többes) |
| `javaslat:funkcio_kod` | betűs kód + funkció-morféma → **`strong` üres**, a `strong_x` őrzi a nyers kódot | 169 906 (+3 többes) |
| `javaslat:nincs_strong` | nincs vagy 0 (pl. tulajdonnév-részletek) | 1 706 |

A funkció-morfémák STEP-megfelelője a 9000-es sáv (`H9001`…); a leképezésük nem a feladat tárgya (javaslat a DT-F17-ben).
Görög: 137 777 / 137 739 sor `igen` (N1904 / SBLGNT), a maradék 2-2 sor `nincs_strong` (`Ἀρνεί`, a 0 Strong).
Az összetett görög Strong (`1417+3461`) a SEMA 1.2 szerint `G1417+G3461`. A `naplok/F17_illesztetlen.tsv` a Strong-oldali
illeszthetetlent Strong-kódonként összesítve tartalmazza (1016 sor).

## 5. A #8 ellenőrző száma (brief 3. lépés)

A 87 függő hely (a `naplok/FORRAS_FJ1_lxx_jeloltek.tsv` sorai) a `naplok/F17_87_hely.tsv`-ben: a Károli-számozású igehelyet
a KK alapján MT-versre váltottam, majd a Macula szavai között a `heber_strong` (számjegy-egyezés), ennek híján a szóalak
alapján kerestem.

| Állapot | F17 (KK-számozással) | F06 (PR #75, számozás-átalakítás nélkül) |
|---|---|---|
| **LXX_MEGFELELO** | **39** | **39** |
| HEBER_SZO_GOROG_NELKUL | 38 | 38 |
| HEBER_SZO_NINCS_A_VERSBEN | 8 | 8 |
| NINCS_VERS | 2 | 2 |

**Eltérés a 39-hez képest: nincs** (sorról sorra egyezik: `egyezik_f06 = igen` mind a 87 sorban). Ez nem a módszer közös hibája,
hanem adat: a 87 hely mindegyikénél a KK szerint a Károli- és az MT-vers azonos számú (a `igehely_mt` = `igehely_karoli`), tehát a
számozás-átalakítás ezekre nem változtat. A 2 `NINCS_VERS` sor (4Móz 13:34, két motívum) a KK szerint valóban nincs MT-párja
(Károli 4Móz 13:34 nincs a Maculában; F06 N28-magyarázata). A 39 sor továbbra is **javaslat, kézi megerősítést igényel** (az F06
78,3%-os szószintű illesztési mérése szerint).

## 6. Illeszthetetlen sorok (brief 2. lépés)

`naplok/F17_illesztetlen.tsv`: 1466 adatsor, minden `allapot=javaslat` (D19).

| Típus | Héber | Görög N1904 | Görög SBLGNT |
|---|---|---|---|
| `macula_vers_nincs_karoli` | 210 | 4 | 3 |
| `karoli_vers_nincs_macula` | 200 | 15 | 18 |
| `strong_nem_illesztheto` (Strong-kódonként) | 1014 | 1 | 1 |

## 7. Szerepmátrix

`adat/szotar_szerepek.tsv`: két új sor (`heber 11`, `gorog 11`) — a Macula szintaktikai/morfológiai réteg és a szavankénti
LXX-megfelelő. **Eltérés a `adat/SEMA.md` 2.13-tól** (az 1–10 szerepet rögzít): a brief a bejegyzést kéri, a séma-módosítás
nem tartozott a hatókörbe → DT-F17.

## 8. Ismert korlátok

- A KK–terkep ütközés 1048 Károli-versnél; a KK irányadó, nem verifikáltam tartalmilag (nincs szó-szintű Károli–héber illesztés).
- 2751+20 héber sor `javaslat:terkep_egyik_sem_identitas`: az identitás a KK „szám szerint sehol sem egyező” versein feltevés.
- A Macula `greek`/`greekstrong` (LXX-megfelelő) szó-szintű, gépi; az FJ1 78,3%-osnak mérte (átvett szám).
- A TAHOT_kivonat és a Macula közti verslista-eltérések oka (F06 5. pont) továbbra sincs vizsgálva.
