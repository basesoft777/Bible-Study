# THAYER_API_KOTEG — napló

*FELADATOK #158 · brief: `F158_THAYER_API_KOTEG_BRIEF.md` · ág: `claude/f158-thayer-api-koteg-559bd1`*
*Végrehajtó modell: `claude-sonnet-5-5` (a brief `modell: sonnet` mezőjével egyezik, modell-ellenőrzés 2026-11-02).*
*Valódi Batch-beküldés és hálózati hívás nem történt; az `adat/forditasok.tsv` és a `forditas/thayer_api/` érintetlen.*

## 1. Felmérés — mi importálható változtatás nélkül, mi új

| Elem | Honnan | Hogyan |
|---|---|---|
| REST-hívó, kulcs (`PARDES_API_KEY`), `tsv_olvas`, `tsv_hozzaad`, `eredmeny_sorok`, `uzenet_szoveg` | `karoli_strong/api_koteg.py` | import (`AK.`) |
| `koltseg`, `jsonl_olvas/hozzaad`, `json_valasz`, `javito_uzenet`, `modell_allapot`, `kerelem_params`, `max_tokens_kerelemre`, ár- és fejléc-konstansok | `bdb_api_koteg.py` | import (`B.`), tiszta segédek |
| `forras`, `prompt_epit`, `utofeldolgoz` (javítóréteg + `kapuk_futtat_thayer`: `14_szakasz`, `15_tiltott`, `16_sigla`), `szakasz_sorok`, `beir` | `thayer_jelolt/forditas.py` | import (`F.`), változtatás nélkül |
| `helyorzo_bont`, `helyorzo_visszaallit`, `HELYORZO`, `kotelezo_alakok_szoveg`, `darab_info_szoveg`, `kisnagybetu_naplo`, `tsv_ir` | `emeles.py` | import (`E.`) |
| `szakaszok`, `csoportok`, `tokenes`, `nezet`, `tabla_olvas` | `thayer_jelolt/thayer_bemenet.py` | import (`TB.`) |
| `allapot` (a `kesz` / `nincs_szakaszos` / `hianyos` / `elavult_hash` szabály), `thayer_sorok` | `thayer_jelolt/szolista.py` | import; a `szolista.lista` **nem** használható: csak a motívumok gerincszavait listázza |

**Új a kötegelőben:** (a) a teljes Thayer listája (`teljes_lista`: a `thayer_szakaszok.tsv` összes Strongja); (b) a helyőrzős prompt:
a `forditas.prompt_epit` a forrást helyőrző nélkül teszi a promptba (a Code-os úton a `_szakasz_hely.txt` adta a helyőrzős
alakot), ezért a `helyorzos_prompt` a kész prompt `Forrás (Thayer, angol):` és `## Kimenet` közötti részét a csoport
`helyorzo_bont` alakjára cseréli (előbb ellenőrzi, hogy a cserélt rész pontosan a csoport tokenes szövege) — a `forditas.py`
módosítása nélkül; (c) a csoportonkénti helyőrző-számozás (1-től, csoportonként) és visszaállítás; (d) a Thayer saját
`custom_id`-mintája (csak `G…`; a BDB-é a `H…`-t is elfogadja); (e) a plafon alapértéke 0, a `bekuld` és a `javit` csak
`--plafon USD`-vel indul. Amit **nem** vettem át a `bdb_api_koteg.py`-ból: a B-út (több Strong egy kérésben), a prompt-cache
(a BDB-n is ki volt kapcsolva), a 13./14. adag összevonása, a `teljes`-úti ág (a Thayerben minden Strongnak van szakaszsora).

A #132 eszközei, az `emeles.py`, a `bdb_api_koteg.py`, az `api_koteg.py` és a `prompt_v5_1.md` bájtra változatlanok
(`git status`: tracked fájl nem változott, csak két új fájl van). Nem kellett megállni, DONTESEK-tétel nem született.

## 2. Alparancsok (`eszkozok/thayer_api_koteg.py`)

`lista`, `szaraz`, `bekuld`, `allapot`, `begyujt`, `kapuz`, `javit`, `rogzit`, `beir`, `--onteszt`. A `--strongok FÁJL` (soronként egy
Strong) adja az adag listáját; `--munka PATH` felülírja a `forditas/thayer_api/adag<N>/` mappát. A `rogzit` a válasz `model`
mezőjét írja a `modell` oszlopba (`modell_allapot`), a `jelentes_szam = sz<n>`, `forras_hash` = a szakasz SHA-1-e
(`forditas.szakasz_sorok`); a kétszer bukottak a `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`-be mennek (fejléc: a
meglévővel azonos), a futás megy tovább. A `beir` a `forditas.beir`-t hívja.

## 3. Tesztek

`python eszkozok/teszt_thayer_api_koteg.py` — 13 teszt, hálózat és kulcs nélkül: **OK**. Lefedik: a `custom_id` oda-vissza
bontását; a prompt bájtazonosságát a `forditas.prompt_epit` kimenetével (a helyőrzős forrásrész visszaállítása után; G1941);
a helyőrző-körút betűhűségét (G1941, G4151 – utóbbi 3 csoport); a G1941 kész sonnet fordításából képzett hamis Batch-válasz
átmenetét a `kapuz`-on (`kesz`, `vegleges` = az eredeti szöveg) és a `rogzit` (ideiglenes munkatáblába) 7 sorát: `forras_hash`,
`jelentes_szam`, `forditas_hu` a meglévő sorokkal azonos; a modellnevet a válaszból (`opus` esetén `opus`); a kapuhiba →
`javitando` → kétszer bukott → `bukottak.tsv` utat; a `javit` plafon-ellenőrzését; a `begyujt` hamis batch-ből (újrafuttatásnál
nincs duplikátum); a `lista` lefedettségét (5 426 Strong, a G1941 `kesz`); a 0 plafonú `bekuld` nem hív hálózatot.

Zárási tesztek (a diff tracked fájlt nem érint, ezért a lenti bukások **nem e feladat okozta**, a brief ismert N66-ján kívül
a környezetfüggő adat-ellenőrzések; nem javítottam őket, hatókörön kívül):
`thayer_jelolt/teszt_lanc.py` 40 teszt, 1 bukás (`Sigla.test_tabla_determinisztikus_es_kezi_vedett`, ez az ismert N66);
`teszt_bont.py` 24 teszt, 2 bukás (`test_ellenoriz`, `test_forras_javit_ellenoriz`: a `bont.py --ellenoriz` és a `forras_javit.py`
ellenőrzése 1-et ad vissza — „javítás nem alkalmazható: 0”, „lyuk: 15; javitva: 15”, azaz a kimenet rendben, a kilépési kód nem);
`teszt_vers_jelentes.py` 11 teszt, 1 bukás (`test_ellenoriz`, hasonlóan: a kimenet rendben, a kilépési kód 1);
`python eszkozok/feladatok.py ellenoriz`: 178 brief, 0 hiba, 0 figyelmeztetés.
*Ezek a bukások az ág alapállapotán (tracked fájl nem változott) is fennállnak; külön vizsgálatra érdemesek (javaslat: külön tétel), a #158 nem függ tőlük.*

## 4. A teljes Thayer futási listája (`lista`, 2026-11-02)

*(proveniencia: `scope=adat/thayer_szakaszok.tsv, adat/forditasok.tsv (szotar=Thayer) | forras=eszkozok/thayer_api_koteg.py lista (szolista.allapot) @a #158 ág | ts=2026-11-02`)*

| | Strong |
|---|---|
| a `thayer_szakaszok.tsv` Strongjai | **5 426** |
| `kihagyva` / `kesz` | **13** (a motívumok gerincszavai közül kész szakaszos fordítás: a #132 M2, a #142 M3) |
| `forditando` / `nincs_szakaszos` | **5 413** |
| `forditando` / `hianyos` | 0 |
| `forditando` / `elavult_hash` | 0 |

Csoportszám szerint: 5 416 Strong 1 csoportos, 6 Strong 3, 3 Strong 4, 1 Strong 6 csoportos (10 többcsoportos Strong); a
fordítandó és a kész Strongok tokenes forrása (a `nezet`) összesen 4 443 391 karakter (a tokenes bemenet a `szaraz` szerint
4 512 785 karakter a 5 452 kérésben, mert a határtokenek is számítanak).

## 5. Száraz futások (`szaraz`, hálózat nélkül, `--munka` a repón kívülre)

*(proveniencia: `scope=lista.tsv mind az 5 426 Strong (a 13 kész is; a minta: a 195 fordítandó) | forras=eszkozok/thayer_api_koteg.py szaraz @a #158 ág | ts=2026-11-02`; a becslések **jelöltek, `manual`**: 2,8 karakter/token a promptra, 0,5 kimeneti token/forráskarakter + 1 500 gondolkodási token/kérés, Batch-ár 1,00 / 5,00 USD/MTok, prompt-cache nélkül, `effort=high`)*

| | mintaadag (a lista első fordítandó Strongjai Strong-szám szerint: G0001–G0200) | a teljes Thayer (mind az 5 426) |
|---|---|---|
| Strong | 195 | 5 426 |
| kérés (csoport) | 195 (0 többcsoportos) | 5 452 (10 többcsoportos Strong) |
| tokenes forrás | 152 964 karakter | 4 512 785 karakter |
| prompt összesen / átlag | 6 662 693 / 34 167 karakter | 189 373 354 / 34 734 karakter |
| bemenet (becslés, manual) | 2,38 M token | 67,63 M token |
| kimenet (becslés, manual) | 0,37 M token | 10,43 M token |
| **költség (becslés, manual, cache nélkül)** | **4,22 USD** | **119,81 USD** |
| csomag (450 kérés/batch) | 1 | 13 |
| `max_tokens` | 16 000–28 028 | 16 000–37 964 |

A mintaadag a brief „kb. 150 000 karakter” méretét a lista első Strongjaiból tölti fel (150 377 karakter a `nezet` szerint;
a gyakorisági sorrend a #27 M0-é). A száraz futás ideje: 5 mp, ill. 83 mp.

**Megfigyelések a #27 M1 számára** (mind becslés/`manual`, mérés nincs):
- A kérésenkénti prompt nagy (átlag ~35 000 karakter): a bemenet a költség ~56%-a (67,6 M token × 1,00 USD), mert minden kérés a
  teljes szabályszöveget, a terminológiát, a Károli-táblát és az adatblokkot hordozza. A prefix a `## Bemenet` elé eső rész
  (G0001: 27 396 / 35 934 karakter, G1941: 35 943 / 54 986), de a kötelező-alak lista Strongonként más, ezért a közös,
  cache-elhető prefix rövidebb, mint ez a szám; a kötegelő a cache-t **nem** kapcsolja be (mint a BDB-n), ezt az első mért
  adag után érdemes újra mérlegelni.
- A tényleges költséget az első adag `futasnaplo.tsv`-je adja; a becslés a BDB mért arányaihoz (0,5 token/karakter) igazodik,
  de a BDB-hez mért karakter/token arányt a Thayer-promptra (angol szöveg, nagy adatblokk) nem mértem — a becslés bizonytalansága
  ebből adódik; az első adag mért értéke váltja.
- A `bekuld` plafonja: a #27 ⛔ M1 felhasználói döntésére vár; a kötegelő alapértéke 0, `--plafon USD` nélkül nem küld.

## 6. Az ellenőri jelentés (`naplok/ELLENOR_F158.md`) tételei és javításuk

1. Köv. 8 — a `rogzit` a munkatáblát `tsv_ir`-rel újraírta, összevetés nélkül → javítva: `munka_ir` (a `#` sorok, a fejléc és a többi
   Strong sora bájtra megmarad, írás előtt ellenőrizve); teszt: `test_rogzit_a_tobbi_sort_bajtra_megtartja`.
2. Köv. 7 — az 1. próbán `kapuhiba` (átmeneti `errored`/`expired`) újrapróba nélkül bukott → javítva: csak a `refusal` végleges, a többi
   `javitando`; a `stop_hibas` nem íródik felül csoportonként; az újrafuttatott `rogzit` nem duplikálja a bukott sorokat;
   tesztek: `test_atmeneti_hiba_javitando_refusal_bukott`, `test_bukott_sor_nem_duplazodik`.
3. Köv. 1 — a git-mentés importja hiányzott → pótolva: `--commit` (a `bekuld`/`begyujt`/`kapuz`/`javit`/`rogzit`/`beir` után
   `api_koteg.git_mentes`; a repón kívüli munkamappát nem commitolja).
4. A napló/docstring pontatlanságai (hatókör-jelölés, 56%, a `G1941a` alak) → javítva.
5. E30 (ékezetek a már pusholt commit-üzenetekben) → a korábbi commitokat nem írtam át; az újak ékezetesek.

## 7. Kész, ha — állapot

- K1 ✅ a kötegelő a brief 3. pontjának alparancsaival; a #132 eszközei, `emeles.py`, `bdb_api_koteg.py`, `api_koteg.py` bájtra változatlanok.
- K2 ✅ a tesztek zöldek, hálózati hívás nélkül.
- K3 ✅ a napló (felmérés, lista, két `szaraz` becslés).
- K4 ✅ az `adat/forditasok.tsv` változatlan; a `forditas/thayer_api/` nem jött létre.
- K5 — az ellenőr első menete 5 eltérést adott (6. szakasz), mind javítva; újraellenőrzés kérésre.
