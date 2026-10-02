# Független ellenőrzés: F38 BDB_FORDITAS, zárómenet 2. kör (DT-F38f)

*A `fuggetlen-ellenor` ügynök (ac739289b8e98661d) jelentése; fájlt nem írhatott, a szöveget a fő session mentette át. Szerkesztés nélkül, a táblázatok tömörítve.*

- **Brief:** `E:\Letöltések\F38_zaras_DT-F38f.md` (KOZVETLEN_FUTTATAS blokk)
- **Tartomány:** `1f22841..278b33a` (F38.272–F38.274); ezen felül a `8a8dac9` merge (csak a DONTESEK.md és a brief konfliktusfeloldása) és a `7c70f88` (\x01 eltávolítása)
- **Repó:** worktree, HEAD `7c70f88`
- **Bash-korlát:** csak `git diff`/`git log`, `lekerdez.py`, `futtat.py` futott; a teszteket és az `ellenoriz.py`-t nem futtatta, ezek NEM ELLENŐRIZHETŐ eredményt kaptak.
- **Összesített eredmény: ELTÉRÉS, 6 tétel**

## Eltérések súlyosság szerint

1. **D5, H3772** (`adat/forditasok.tsv:255`, közepes): a kézi RV-csere kitörölte a „fordítják” állítmányt. Forrás: „Isa 57:8 is usually rendered as RV made for thee …”; fordítás: „… Ézs 57:8 helyet rendszerint az RV made for thee a covenant with them,”. Az „is … rendered as” nem glossza, magyarul kellett volna maradnia; a mondat csonka.
2. **D3, H5674 indoklása** (`naplok/BDB_FORDITAS_naplo.md:2375`; `BDB_FORDITAS_szellem.py`, közepes): az indoklás szerint az 1Kir 22:24 „rossz/hazug szellem, nem Isten Szelleme”. A forrás H7307 9a pontja viszont kifejezetten: „= י ׳רוּחַ 1Kin 22:24 2Chr 18:23”, vagyis a 9. pontba sorolja. (`lekerdez.py karoli "1Kir 22:24"` → „Eltávozott volna én tőlem az Úrnak lelke”; `scope=range:1Kir 22:24 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | ts=2026-10-02T14:16Z`.) A „kétséges, marad” eredmény védhető (a 4Móz 5:14, 30 a 3g pontban áll, egy frázisban), de az indoklás ellentmond a forrásnak.
3. **D3, a Szellem-tábla „végleges állapota”** (`naplo.md:2358-2359`, megítélésre): a tábla a szabályt mondja ki („a 9. pont nagybetűs, az emberi szellem kisbetűs”), mégis nagybetűsként szerepel a H7307 **4c** (Gen 6:3; a forrás 4. pontja az élőlény szelleme, nem a 9.) és a **3d** (Jób 32:18, „Di Bu divine spirit”; a forrás a 3. pontba sorolja). Ezek F38.268-as javítások, a 2. kör nem vizsgálta őket újra a szabály szerint, a tábla mégis „végleges”-nek nevezi őket.
4. **D5, H4397** (`forditasok.tsv:304`, alacsony; a végrehajtó jelezte): forrás „(angel of RV too specific)”, fordítás „(az angyal RV too specific)”. A szabály betűje teljesül, a célja nem: az RV saját szava („angel”) fordult le, angolul a BDB megjegyzése („too specific”) maradt; a magyar mondat szerkezete sérült.
5. **D4, H4264** (`naplo.md:2397`, alacsony): az indoklás szerint „verszám-táblázat híján gépileg nem dönthető”. `lekerdez.py karoli "1Móz 33:81"` → „Nincs Károli-szöveg ehhez”; `… "1Móz 33:8"` → „Mire való ez az egész sereg…” (`ts=2026-10-02T14:16Z`). A repó adatával eldönthető: `1Móz 33:8, összesen 16-szor`.
6. **D1, H2403** (`forditasok.tsv:88`, alacsony): kézi RV-javítás, a `megjegyzes` mégis „F38.274: DT-F38f (1) — gépi szabályok a #28 soron” jelölést kapott; a javítási listán `igen (kézi, DT-F38f 5)` áll, ebből nem derül ki, hogy #28-as sor. Ok: `zaras2.py:158` minden #28-as változásra a `JELOLES_28` szöveget írja.

## Pontonkénti eredmények (OK, ha nincs jelölve)

| pont | eredmény | indok |
|---|---|---|
| Brief 0 (Sonnet) | OK | mind az 5 commit trailere `Claude Sonnet 5.5`; a napló `claude-sonnet-5-5` |
| Brief 1a (felülírt szöveg) | OK | `DONTESEK.md:49,50`, napló:1685: régi szöveg megmaradt, „Felülírva (2026.10.02) …” jelzéssel, címsor nem változott. A naplóban a jelzés a címsor alatt, a törzs előtt áll („alá” helyett „fölé”): formai kérdés. |
| Brief 1b (243 sor vs. 20ef676) | OK, egy része NEM ELLENŐRIZHETŐ | a 2–6., 10., 11. oszlopban 0 eltérés; 243 sor `opus`→`sonnet` (DT-F38e); `20ef676..8710ca3`: 156 sor szövege tér el, 87 azonos (egyezik a naplóval; HEAD-en 167/76, a 2. kör 11 újabb sort javított). Hogy a 156 mindegyike szerepel a javítási listán, csak szkripttel igazolható. |
| D1 (#28): allapot/modell nem változik | OK | 8 #28 sor: csak a `forditas_hu` és a `megjegyzes` változik |
| D1: 18 gépi + 1 kézi hely | OK | lista: 421 `igen`, 18 `igen (#28, DT-F38f 1)`, 6 `igen (kézi, DT-F38f 5)` |
| D1: H0430 11. kapu | OK (rácsos keresés), kapufutás NEM ELLENŐRIZHETŐ | tapadt könyvjelzés a táblán: 0 találat |
| D1: külön jelölés | **ELTÉRÉS** | l. 6. tétel |
| D2: `KIS_NAGYBETUS_IS` | OK | `forditas_kapuk.py:313-334`: csak a `spirit` kulcs; a `spiritual` nem érintett; teszt: `SzellemKisNagybetu` 5 eset, köztük a `soul→Lélek` SÉRTÉS |
| D2: H5307/H5414/H7760 kivétele kikerült | OK | `spirit` kivétel: 0 találat; maradók: accusative 4, see 2, p. 1, cl. 1, Heb. 1 |
| D3: H1320 Ézs 31:3 → Szellem | OK | forrás H7307 9e: „as vital power, opposed to בָשָׂר: Isa 31:3” |
| D3: H4390 kisbetűs marad | OK | egy frázis („fill with spirit Exod 28:3; 31:3; 35:31”); 6. pont emberi, 9d isteni; indoklással listán |
| D3: H7451 (#28) kisbetűs | OK | Istentől küldött rossz szellem (9a, 1Sám 16:14–16, 23, 18:10, 19:9) |
| D3: H5674 indoklása | **ELTÉRÉS** | l. 2. tétel |
| D3: Szellem-tábla | **ELTÉRÉS** | l. 3. tétel |
| D4: tartományos „N t.” | OK | `normalizal.py:301-335`; `Jer 25:3-4t.`, `Num 7:15-16t.` párhuzamos szerkezetek támasztják; „összesen” a brief példája szerint |
| D4: 39 hely / 30 szócikk | OK | -szor/-szer/-ször mind a 39 helyen hangrendhelyes |
| D4: más gépileg eldönthető hely nem maradt | OK | maradt: H7043 (`§67 t.`), H4264, H4687 |
| D4: H4687 listán | OK | `lekerdez.py scan H4687`: a Zsolt 119:20 nincs a találatok közt, a 119. zsoltárban 22 vers van (`scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H4687 | n=177 | ts=2026-10-02T14:16Z`); listán hagyás indokolt |
| D4: H4264 listán | **ELTÉRÉS** | l. 5. tétel |
| D5: H4150, H2403, H5674, H8033 | OK | forrás és fordítás szó szerint egyezik |
| D5: H3772 | **ELTÉRÉS** | l. 1. tétel |
| D5: H4397 | **ELTÉRÉS** | l. 4. tétel |
| D6: toldalék, D11 | OK | a D11 sor bekerült |
| Brief 3: merge, DONTESEK.md | OK | a main oldaláról 0 sor törlődött |
| Brief 3: merge, F38 brief | OK | a main M0 5. pontja, M1, D-gyok, v1.1-jelzés, `ir: …gyokcsoportok.tsv` megmaradt |
| 7c70f88 | OK | `modell: sonnet^A` → `modell: sonnet` |
| Tesztek, `ellenoriz.py`, kapuk a 269 soron | NEM ELLENŐRIZHETŐ | Bash-korlát; a napló állítása (12/61/63/7/9 OK, 0 SÉRTÉS) nincs igazolva. A `test_28_cimkek_valtozatlanok` csak halmazba tartozást vizsgál, nem a 20ef676-hoz hasonlít. |
| CI-jelentés | NEM ELLENŐRIZHETŐ | saját `futtat.py` a tartományon: E2–E19 0 találat. A teljes PR a beolvasztott main-hez képest (32 fájl): **E16 HIBA 1**, ha a PR címe nem `[ELLENŐRZŐ]` előtagú (forrás: 4d0feb5/F38.265, tartományon kívül). |
| A1 (memória vs. lekérdezés) | NEM ELLENŐRIZHETŐ | a napló „a BDB `Deut 11:13 + 14 t.` alakja” állítása: a forrásban csak `Deut 11:13-14t.` áll; a „+” analógiát a 29 „+ N t.” hely támogatja, de jelöletlen értelmezés. A „+ N t.” máshol `+ 2-szer`, a tartományos alak „összesen”: a két alak eltér. |
| A2 (nyitott tételek) | OK | négy tétel rendeződött; `NYITOTT_FELADATOK.md`-ben nincs F38-as tétel |
| A3–A5 | nem alkalmazható | nincs tanulmányszöveg, PaRDeS-réteg, nevesített tanító |
| A6 (E12–E15) | OK | saját tartományon 0 találat |
| CL1 (törölt sorok) | OK | `forditasok.tsv` 45/45, 0 törölt; 37 F38-as + 8 #28-as módosult |
| CL2 (lefedettség) | OK | 269 `teljes` sor, ebből 243 F38, 26 #28 |
| CL3 (nulla-diff hatóköre) | OK | allapot, modell, kulcs, hash, dátum, verzió változatlan a 45 soron |
| CL4 (E17/DT3) | OK | `forditasok.tsv` +251/−8 a mainhez, **Δ = +243**; `Konyv_normalizalo_tabla.tsv` Δ = 0 |
| CL5 (⛔ pontok) | OK | a brief blokkjában nincs ⛔ |
| CLAUDE.md: TSV, proveniencia | OK | 7 érintett fájlban 0 `csv` használat; a `zaras2.py` írás előtt ellenőriz; a H4264 „nem dönthető” megállapítás lekérdezés nélkül született (l. 5. tétel) |

## Kezelés (a fő session megjegyzése; DT-F38g, 2026.10.02)

A felhasználó DT-F38g döntése szerint, egy körben, a Sonnet végrehajtóval (`claude-sonnet-5-5`). Szkript:
`naplok/BDB_FORDITAS_zaras3.py`; a javítási lista +4 sorral bővült (`igen (kézi, DT-F38g N)`). A részletek:
`naplok/BDB_FORDITAS_naplo.md`, „Zárómenet, 3. kör”.

| # | Eltérés | Kezelés | Állapot |
|---|---|---|---|
| 1 | D5, H3772 | `rendszerint így fordítják: RV made for thee a covenant with them,` — az állítmány vissza, az RV-szó angolul | javítva: 082c77a |
| 2 | D3, H5674 | az 1Kir 22:24 (H7307 9a) nagybetűs: `a Szellemről abszolút használatban és מֵאֵת 1Kir 22:24`; a Szellem-tábla indoklása javítva. Új szó („az Úr”) nem került a szövegbe | javítva: 082c77a (szöveg), a tábla: a naplóban |
| 3 | D3, Szellem-tábla | A szabály pontosítva (kire vonatkozik a szó a kifejezésben). H7307 4c nagybetűs marad (a BDB maga „God's spirit”), a 3d-n csak a „Di Bu: isteni Szellem” nagybetűs, Elihu szelleme kisbetűs. A teljes tábla újranézve szkripttel (14 nagybetűs hely); a szöveg a H5674-en kívül nem változott, a H5650 és a H7307 9 fejléce bekerült a táblába. **Tartalmi kétség, nem döntöttem:** a H7451 (#28; a BDB maga „divine spirit”, a DT-F38f 3 szerint viszont rossz szellem, kisbetűs) és a H4390 (egy frázis, emberi/isteni vegyesen) | javítva: 082c77a (ellenőrző szkript), a tábla és a DT-F38f 3 kiegészítése: a 3. kör commitja; a H7451 és a H4390 nyitott |
| 4 | D5, H4397 | `(az RV angel szava túl szűk)` — az RV saját szava angolul, a BDB megjegyzése („too specific”) fordítva | javítva: 082c77a |
| 5 | D4, H4264 | `1Móz 33:8, összesen 16-szor`; lekerült a listáról. A 2. kapu forrásoldali OCR-javítást kapott (`forditas_kapuk.FORRAS_VERS_OCR`), különben a `33:816` token SÉRTÉS lett volna — **kapuszabály-bővítés, jóváhagyásra** | javítva: 082c77a |
| 6 | D1, H2403 | a `megjegyzes` „kézi javítás” jelölést kap (nem „gépi szabályok a #28 soron”) | javítva: 082c77a |

Ellenőrzés a kör végén: `teszt_bdb_zaras.py` 17, `teszt_forditas_kapuk.py` 61, `teszt_normalizal.py` 63,
`teszt_emeles.py` 7 — OK; `ellenoriz.py` SÉRTÉS 0; a 269 BDB-soron (243 F38 + 26 #28) a gátoló kapuk RENDBEN.
A független ellenőr a 3. kört nem látta; a kör a saját munkát nem minősíti ellenőrzöttnek.
