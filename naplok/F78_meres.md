# F78 — Szerepmátrix-váz: mérés

*FELADATOK #78 · `F78_SZEREPMATRIX_VAZ_BRIEF.md` · ág: `claude/f78-szerepmatrix-vaz` · Modell: sonnet*

## M0 — a mai 2. szakasz összevetése a szerepmátrixszal

`scope=lexikon/ISTENTISZT-001_TUDOMANYOS.md 342–549. sor (2. Szótári háttér + 2/b + Miért fontos) + adat/szotar_szerepek.tsv (22 sor) + adat/lexikon_hivatkozasok.tsv + lexikon_general.py (lexikon_hivatkozasok_ehhez, oshl_twot_ehhez, domen_talalatok, lemma_kiejtes, rokon_szavak_strongok) | forras=manual (olvasás és összevetés; a darabszámok a generátor saját függvényeiből, scratchpad-szkript) | ts=2026-10-08`

### 1. A mai szerkezet

A 2. szakasz (generált blokk `lexikon#ISTENTISZT-001#szocikkek`, 344–460. sor) a mátrixtól függetlenül épül:

```
Strong (tokenenként)            ← _epit_szotar_alszakasz(strong)
  fejléc: lemma (kiejtés)       (10. szerep, részben)
  TWOT sor                      (héber 3., csak a szám)
  Szemantikai domén sor         (4. szerep)
  forrásonként: TBESG / Thayer / BDB / LSJ   (1., 2., 8. szerep, jelentésszámonként)
Rokon szavak (G0994, G2564)     ← ugyanaz az alszakasz egy szinttel lejjebb
```

A kézi 2/b (462–533. sor) és a „Miért fontos” (535–549. sor) a generált blokkon kívül áll.

### 2. Szerepenként: hol áll ma (ISTENTISZT-001)

| # | Szerep | Görög (G1941, rokon: G0994, G2564) | Héber (H7121, H8034) |
|---|---|---|---|
| 1 | Alapjelentés | **megvan**: TBESG-alszakasz Strongonként (G1941 1., 2. jelentés; G0994, G2564 részlet) | **hiányzik**: TBESH-szócikk nincs a blokkban (csak a Strong-fejlécben a TBESH-lemma/licenckulcs; `lexikon_hivatkozasok.tsv`-ben 0 TBESH-sor) |
| 2 | Mélységi szócikk | **megvan**: Thayer (G1941 teljes; G0994 rokon) | **megvan**: BDB (H7121 2.c és 3.; H8034 részlet) |
| 3 | Teológiai szócikk | nincs adatosítva — nincs | nincs adatosítva — csak a **TWOT-szám** áll (H7121: 2063; H8034: 2405), hivatkozásként a Strong-fejlécben |
| 4 | Jelentésszerkezet, szemantikai mező | **Strong szerinti** „Szemantikai domén” sor (SDGNT; G1941: 4 domén); a 2/b-ben SECE-domének kézzel | **Strong szerinti** „Szemantikai domén” sor (SDBH; H7121: 13, H8034: 5 domén) |
| 5 | Tömör jelentés, előfordulás | csak a **2/b** vegyes blokkban (MCGED-táblázat, kézi) | nincs adatosítva — nincs |
| 6 | LXX-híd | a **3. szakaszban** (nem a 2.-ban) | a **3. szakaszban** |
| 7 | Megfelelők a másik nyelven | csak a **2/b**-ben (SECE héber-lista, kézi) | csak a **2/b**-ben (SECE görög-lista, kézi) |
| 8 | Nyelvi háttér | LSJ csak a rokon G2564-nél (generált részlet); a G1941 LSJ-je csak átirányít (2/b-ben kézzel jelezve) | nincs adatosítva (a „√ unknown” a BDB-szövegben és a 2/b-ben kézi megjegyzés) |
| 9 | Versenkénti jelentés | **hiányzik** | **hiányzik** |
| 10 | Kiejtés (magyaros) | **részleges**: a Strong-fejléc `lemma (átírás)` és a 🇭🇺 sorok kiejtés-glosszái | **részleges**: ugyanígy; kiejtés-kivételtábla szerinti adat nincs a blokkban |
| 12 | Tematikus index (Nave) | **hiányzik** (`javaslat`) | **hiányzik** (`javaslat`) |
| 13–14 | (Károli-megfelelők + SZPA; rejtett/hamis párhuzam) | a mátrixban nincs sor | a mátrixban nincs sor |

Egyezik a #64 mérés 7. szakaszával (`naplok/TEREMT002_PROZA_PROBA_meres.md`): a 9., 12., 13. hiányzik; az 5. és 7. a 2/b vegyes blokkban; a 4. Strong szerinti; a héber 3.-ból a TWOT-szám; a 10. részleges. Két pontosítás ehhez: **(a)** a héber 1. (TBESH) is hiányzik a blokk szövegéből; **(b)** a 6. szerep a 3. szakaszba van kihelyezve, nem a 2.-ban áll.

Megjegyzés: a mátrixban a 11. sorszám nincs kiosztva; az 1–10 és 12 sor a mai tábla (11 szerep × 2 = 22 sor, a brief 22 → 26 számítása egyezik: +2 szerep × 2 nyelv).

### 3. TEREMT-002 (második minta)

| Elem | Mérés |
|---|---|
| Strong-tokenek | H0922, H8414 (3 előfordulás-sor) |
| `lexikon_hivatkozasok.tsv` | **0 sor** mindkét tokenre (BDB-bekötés hiányzik, #64 mérés 4.) |
| TWOT / domén / lemma-kiejtés | megvan: H0922 TWOT 205a, 1 domén; H8414 TWOT 2494a, 2 domén |
| Rokon szavak | 0 |
| `res_forras.tsv` | **nincs sora** → a `lexikon_general.run()` mai szabálya szerint `KIHAGYVA`; a `lexikon/TEREMT-002_TUDOMANYOS.md` nem létezik |

Következmény az M3-ra: a TEREMT-002 teljes lexikonoldala nem renderelhető (az a #12b), a szótári rész viszont a `blokk_szocikkek` közvetlen hívásával, a `res_forras`-kapu megkerülése nélkül előállítható `generalt_proba/`-ba, kizárólag a 2. szakaszra. A szerepek legnagyobb része itt üres blokk lesz — ez a váz-render legerősebb próbája.

### 4. Érinti-e a blokk-átrendezés a `blokk_szocikkek` belső szerkezetét?

**Igen.** A mai render Strong-szám → forrás (→ jelentésszám) hierarchiájú, és a Strong-alszakasz fejlécében keveredik három szerep (kiejtés 10., TWOT 3., domén 4.), a forrás-alszakaszokban három másik (1., 2., 8.). A szerep-sorrendű render a hierarchiát **megfordítja** (nyelv → szerep → Strong → forrás/jelentésszám), tehát:

1. a `_epit_szotar_alszakasz()` (lexikon_general.py 679–734. sor) nem maradhat egyben: a TWOT/domén/kiejtés-fejléc és a forrásonkénti jelentés-hivatkozások külön szerepekhez rendelendők, a függvényt szerepenkénti építőkre kell bontani;
2. a `blokk_szocikkek()` (752–798. sor) Strong-ciklusa és a „Rokon szavak” alcsoport szerepe újragondolandó (a rokon szó melyik szerep alá kerüljön: a szerep alatt Strongonként, vagy külön alcsoportban);
3. az alszakasz-címek (`#### TBESG G1941 — 1. jelentés` stb.) mélysége és az `anchor`-ok eltolódnak; a lexikonoldalon belüli és a `_TORZSCIKK`-ből, valamint a gyorsreferenciából jövő hivatkozások (ha vannak) ellenőrzendők;
4. a blokk `forras`/`licenc` fejléc-listája (`fajl_licenc_kulcsok`) a szerep-építőkből gyűlik, nem változhat tartalmában (G3: fájl–licenc párok) — ezt a teszt rögzítse.

Ezért a brief szerinti **⛔ megállás érvényes**.

### 5. Javasolt szűkített hatókör (a felhasználó dönt)

A forrásonkénti belső render **változatlan marad**; csak a 2. szakasz külső váza változik:

- **S1.** A `_epit_szotar_alszakasz` kimenetét nem bontjuk szét, hanem a *meglévő forrás-alszakaszokat* (TBESG, Thayer, BDB, LSJ — már most önálló, jelentésszámos `####` blokkok) szerep alá csoportosítjuk: szerep-fejléc (`### 1. Alapjelentés — TBESG`) a nyelv szerinti sorrendben, alatta Strongonként a változatlan forrás-blokkok.
- **S2.** A Strong-fejléc `lemma (kiejtés)` + TWOT + domén sorai a Strong-szintű összefoglalóba (a 10., 3. és 4. szerep sorai) kerülnek, a mai szövegük változatlanul, de a megfelelő szerep fejléce alatt is feltüntetve (referenciaként), nem kettőzve a szöveget [egyeztetendő: lásd lent].
- **S3.** Az adat nélküli szerep (`nincs adatosítva`, `javaslat`, vagy az adott tokenhez nincs sor) **explicit üres blokk** (DT-F78a jelölésével), adatosítás és szöveg-kitöltés nélkül.
- **S4.** A 5., 7. (2/b) és 6. (3. szakasz) szerep a váz-blokkban **hivatkozásként** jelenik meg („l. 2/b”, „l. 3. szakasz”), nem mozgatjuk át; a kézi 2/b és a LXX-blokk érintetlen.
- **S5.** A „Rokon szavak” külön alcsoport marad a váz végén (a szerepek után), belső szerkezete változatlan.

Ez a szűkítés a #36 `lexikon_general.py`-ra épülő munkáját nem zavarja (a `_epit_szotar_alszakasz` és a `blokk_szocikkek` belseje nem változik, csak egy új csomagoló réteg kerül köréjük), és a teljes átépítés (szerep-építőkre bontás) a #9-re halasztható, amikor az adatosítás indul.

**Nyitott pont a döntéshez:** S2 szerint a TWOT/domén/kiejtés sor a Strong-fejlécben marad *és* a szerep alatt hivatkozásként szerepel, vagy a Strong-fejlécből a szerep alá költözik (ez már belső szerkezetet érint). A javaslat az előbbi (nincs szövegkettőzés: a szerep-blokk csak a kereszthivatkozást és a töltöttséget mutatja).

### 6. A #64 mérés 7. szakaszának két pontosítása

1. **Héber 1. szerep (Alapjelentés, TBESH):** a blokk szövegéből hiányzik; a Strong-fejlécben csak a TBESH-lemma és a licenckulcs áll. `adat/lexikon_hivatkozasok.tsv`-ben **0 TBESH-sor** van (`scope=adat/lexikon_hivatkozasok.tsv, szotar=TBESH | forras=manual (szkript, lexikon_hivatkozasok_ehhez) | ts=2026-10-08`).
2. **6. szerep (LXX-híd):** nem a 2., hanem a **3. szakaszban** áll (`lexikon#ISTENTISZT-001#lxx`); a 2. szakaszban csak hivatkozás kell rá (S4).

### 7. Döntések (felhasználó, 2026-10-08, chat)

- **DT-F78b:** szűkített hatókör (S1–S5). A TWOT-, domén- és kiejtés-sor a saját szerepe alá költözik (3., 4., 10.), nem marad a Strong-fejlécben hivatkozással (az S2 pont eredeti "referencia" változata így módosul).
- **DT-F78a:** B változat: gépi `<!-- ÜRES-BLOKK: szerep | állapot -->` jelölő + látható zárójeles sor. Üres blokk csak a `nincs adatosítva` / `javaslat` állapotú szerepeknél; az `adatosítva` szerepnél (görög 5., 8., 9.) hivatkozás kell (S4), nem üres blokk.

### 8. M1 – a mátrix-bővítés

`adat/szotar_szerepek.tsv`: 22 → 26 sor (13. „Károli-megfelelők (+ SZPA)” és 14. „Rejtett / hamis párhuzam”, mindkét nyelven, `javaslat`); a már meglévő 24 sor (fejléc + 22 adatsor + komment) bájtra változatlan (előtag-ellenőrzéssel igazolva, `csv` nélkül). `adat/SEMA.md` 2.13: „13 szerep × 2 nyelv = 26 sor”. A `torzscikk_general.py` kódja nem változott: az 5. szakasz a táblából épül, a próbarenderben a 13–14. szerep megjelenik a szerep-táblában és a lefedettségi mátrixban (`nincs adatosítva` cellákkal). `scope=adat/szotar_szerepek.tsv | forras=manual (szkript, előtag-egyezés) | ts=2026-10-08`

### 9. M2 – a váz

- `_epit_szotar_alszakasz` → `_szotar_reszek` (Strong-szócikk szétbontva: fejléc/kiejtés, TWOT, domén, forrásblokkok). A régi egybeépített kimenet **bájtra azonos** maradt a refaktor után (az ISTENTISZT-001 `szocikkek` blokk a ts nélkül 19 451 = 19 451 karakter, egyezik), a rokon szavak (S5) ezt használják változatlanul.
- `szerep_vaz()`: nyelv szerint (görög, héber), azon belül a tábla sorrendjében; a mindkét nyelven azonos (szerep, forrás, állapot) sorok (12–14.) a „Nyelvfüggetlen szerepek” alatt, egyszer.
- A TWOT (héber 3.), a domén (4.) és a kiejtés (10.) a saját szerepe alatt áll; a forrásblokkok (`##### TBESG G1941 — …`) belső szövege változatlan, egy fejlécszinttel mélyebben.
- Üres blokk (DT-F78a B): `<!-- ÜRES-BLOKK: szerep | állapot -->` + látható zárójeles sor. A `nincs adatosítva` / `javaslat` szerep mindig kapja; részadat (TWOT, kiejtés-lemma) esetén a sor kimondja, hogy csak hivatkozás/részadat áll.
- S4 hivatkozás az `adatosítva` szerepeknél, ahol a tartalom máshol él: görög 5. (2/b, kézi), 6. és héber 6. (3. szakasz), görög 8. (nincs LSJ-sor a tokenekhez), görög 9. (az 1. szakasz UBS-jelentés oszlopa).
- Szerephez nem rendelt szótár (`SZEREP_SZOTAR`) `ValueError`: nincs néma elhagyás. A licenc-állapot nem romlik (`tisztazatlan`: nem), a szerepmátrix projekt-adatként a blokk forrásai között szerepel.
- `eszkozok/teszt_szerepmatrix.py`: 13 teszt zöld; `feladatok.py ellenoriz` 0 hiba; `ellenorzes/tesztek` 153 teszt zöld.

**Értelmezői bővítés (jelzem, nem a DT-F78a betűje):** a héber 1. (TBESH) szerep a táblában `adatosítva`, de a `lexikon_hivatkozasok.tsv`-ben 0 TBESH-sor van. Itt nem hivatkozást, hanem jelölt üres blokkot ad a render (`ÜRES-BLOKK: Alapjelentés | adatosítva, nincs bekötve`), mert a hiányt elhallgatni a 3. szabályt sértené, hivatkozni pedig nincs hová. Ugyanez áll a TEREMT-002 héber 1–2. szerepére. Kérdés a felhasználónak: elfogadja-e ezt a harmadik állapotértéket, vagy a TBESH-sor állapota a táblában `nincs adatosítva`-ra javítandó (a `torzscikk` lefedettségi mátrixa is „TBESH”-t mutat a H7121/H8034 alatt, ami a jelenlegi adattal nem igaz).

### 10. M3 – próbarender és töltöttség

Kimenet (csak `generalt_proba/`, az éles `lexikon/` változatlan, `git status` igazolja):
- `generalt_proba/F78_szerepmatrix_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md` és `…_TORZSCIKK.md` (`general.py --cel lexikon|torzscikk --id ISTENTISZT-001 --kimenet generalt_proba/F78_szerepmatrix_proba`; a meglévő `generalt_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md` régi próbafájl a `res_blokkok_alkalmaz` határjelölőin elbukik, ezért nem azt írtam felül);
- `generalt_proba/TEREMT-002_szotari_proba/TEREMT-002_2_SZOTARI_HATTER.md` (csak a 2. szakasz, a `blokk_szocikkek` közvetlen hívásával; a TEREMT-002 teljes lexikonoldala a #12b, a `res_forras.tsv`-kapu miatt nem renderelhető).

`scope=generalt_proba/F78_szerepmatrix_proba + generalt_proba/TEREMT-002_szotari_proba | forras=general.py / lexikon_general.blokk_szocikkek, szkript | ts=2026-10-08`

| # | Szerep | ISTENTISZT-001 görög | ISTENTISZT-001 héber | TEREMT-002 héber |
|---|---|---|---|---|
| 1 | Alapjelentés | töltött (TBESG, 2 jelentés) | jelölt üres blokk tokenenként: H7121 mutató a BDB 2.c-re (DT-F42a), H8034 `adatosítva, nincs bekötve` (#9) | **üres** (adatosítva, nincs bekötve; a #9 a BDB-t köti be) |
| 2 | Mélységi szócikk | töltött (Thayer) | töltött (BDB, 3 blokk) | **üres** (adatosítva, nincs bekötve) |
| 3 | Teológiai szócikk | **üres** (nincs adatosítva) | részleges: TWOT-szám + üres blokk | részleges: TWOT-szám + üres blokk |
| 4 | Jelentésszerkezet | töltött (SDGNT-domén) | töltött (SDBH-domén) | töltött (SDBH-domén) |
| 5 | Tömör jelentés | hivatkozás (2/b, kézi) | **üres** (nincs adatosítva) | **üres** (nincs adatosítva) |
| 6 | LXX-híd | hivatkozás (3. szakasz) | hivatkozás (3. szakasz) | hivatkozás (3. szakasz) |
| 7 | Megfelelők | hivatkozás (2/b, kézi; DT-F78c 3.) | hivatkozás (2/b, kézi) | hivatkozás (2/b — a TEREMT-002 oldala még nincs, lógó) |
| 8 | Nyelvi háttér | hivatkozás (nincs LSJ-sor a tokenhez) | **üres** (nincs adatosítva) | **üres** |
| 9 | Versenkénti jelentés | hivatkozás (1. szakasz UBS-oszlop) | **üres** (nincs adatosítva) | **üres** |
| 10 | Kiejtés | részleges: lemma (átírás) + üres blokk | részleges + üres blokk | részleges + üres blokk |
| 12–14 | Nave; Károli+SZPA; rejtett/hamis | **üres** (javaslat) | ugyanaz (közös blokk) | ugyanaz |

Összesítés: ISTENTISZT-001-en a görög szerepek közül 3 töltött (1., 2., 4.) és 4 hivatkozásos (5., 6., 8., 9.), a héberek közül 2 töltött (2., 4.) , 1 hivatkozásos (6.) és 1 jelölt üres, mutatókkal (1.); a többi explicit üres vagy részleges. A #64 mérés 7. szakaszának korlátja (a mérce hiánya a szerepmátrixra) ezzel megszűnik: a 2. szakasz a mátrix minden szerepét mutatja, a hiány látszik, kitöltetlen szerepen sehol nincs gyenge vagy asszociatív anyag. A mérce kiterjesztése (a TEREMT-002-nél a H8414/H0922 BDB-bekötés hiánya, `lexikon_hivatkozasok.tsv` 0 sor) a #9/#12b dolga marad.

### 11. Javítókör a DT-F78c és az ellenőr után (2026-10-08)

- **Állapotnév:** `adatosítva, nincs bekötve` (nem „nincs sor”), a szöveg a #9-re mutat (ISTENTISZT-001 héber 1. és TEREMT-002 héber 1–2. szerep; a próbafájlok újragenerálva).
- **Token nélküli nyelv:** egy mondat + gépi `<!-- ÜRES-NYELV: gorog | nincs Strong-token -->` (a nyelv kódjával).
- **7. szerep (SECE):** „l. 2/b” hivatkozás, nincs ÜRES-BLOKK (`SZEREP_KEZI_2B`, görög és héber).
- **SEMA 2.13** `javaslat` leírás a 13–14. szerepre kiegészítve.
- **Lógó hivatkozás:** a `TEREMT-002_2_SZOTARI_HATTER.md` fejléksora jelzi, hogy a „l. 3. szakaszt / 2/b / 1. szakasz” hivatkozások a leendő lexikonoldalra mutatnak (#12b), jelenleg lógnak.
- **Tesztek:** 16 teszt zöld; új lefedettség: héber `adatosítva` szerepek (2., 4., 6.) nem kapnak hamis ÜRES-BLOKK-ot; a hivatkozási célok léteznek (sablon-szakaszok, az `UBS-jelentés` oszlop a `blokk_elofordulasok` fejlécében); a forrásszöveg (`> `) csak a forrás-szerepekben fordulhat elő, minden más szerepre ellenőrizve; `ÜRES-NYELV` jelölő; a 7. szerep hivatkozás.
- **„Bájtra azonos” igazolás:** a `_epit_szotar_alszakasz` régi (`b7be700~1`) és új változata a repó mind a 41 Strong-számára (motívum-tokenek + rokon szavak), 0 és 1 szinteltolással (82 összevetés): a kimenet UTF-8 bájtjai, a visszatérési jelzők és a licenc-mellékhatások azonosak; SHA-256 mindkét oldalon `3d4979e217b69ec7f1a1064a9a145a4d3d591258b3e35c87bfd9de244d7ab2e1`. (`scope=git b7be700~1:eszkozok/lexikon_general.py vs a munkafa | forras=manual (szkript) | ts=2026-10-08`.) A korábbi „19 451 = 19 451 karakter” állítás ezzel felváltva.
- **N-F78a** (helyőrző, `NYITOTT_FELADATOK.md`): a `torzscikk_general.py --kimenet` az éles `lexikon/`-ból olvas, ezért a próba-törzscikk nulla-diffje nem áll (#36, #11).

### 12. Egyeztetett eltérés a briefhez (a zárójelentés bemenete)

A brief hatóköre a DT-F78c (a) szerint kivételesen bővül: az ISTENTISZT-001-hez két héber TBESH-sor (H7121H „call by”, H8034 „name … the Name”) bekötése, jelölt-soron át, majd a `lexikon_hivatkozasok.tsv`-be; minden más bekötés a #9-é. Az `ir` mező ennek megfelelően kiegészült (`adat/jeloltek.tsv`, `adat/lexikon_hivatkozasok.tsv`).

**A TBESH-bekötés NEM történt meg (két akadály); a felhasználó a negyedik utat választotta: l. a 13. szakaszt (a DT-F42a érvényben marad, a héber 1. szerep a meglévő BDB-sorokra hivatkozik).**
1. **Ütközés a DT-F42a-val** (felhasználó, 2026-10-05, 🟢): a TBESH H7121 „részlet” sorát kifejezetten *törölni* kellett a `lexikon_hivatkozasok.tsv`-ből és a `forditasok.tsv`-ből, a lexikonoldal és a kézi 2/b szakasz BDB-alapra íródott át (Online Bible-eredetű szöveg kiváltása). A TBESH.txt 7. mezője („Meaning”) Online Bible-eredetű; a mostani kérés ezt a sort visszahozná (a H8034 TBESH-sora ugyanígy Online Bible-eredetű Meaning-szöveg). A DT-F33f ugyan `tisztazott`-ra emelte a licencet, de a DT-F42a a kiváltásról döntött. Nem tudom, hogy a felhasználó a DT-F78c (a) jóváhagyásakor ezt mérlegelte-e.
2. **A `jeloltek.tsv` séma (SEMA 2.4):** a kulcs `id` + `igehely`, az `igehely` kötelező `IGEHELY` típus; szótárszócikknek nincs igehelye, így a jelölt-sor sémasértés nélkül nem írható. A precedens (F6.3, `f6_3_lexikon_hivatkozasok_toltes.py`) szótári sort jelölt nélkül, szó szerinti részsztring-ellenőrzéssel kötött be.

Opciók a felhasználónak: **(1)** a bekötés a DT-F42a felülírásával, a `jeloltek.tsv` kihagyásával (döntés + indoklás a `DONTESEK.md`-ben, mint az F6.3-nál; a két sor a TBESH-ból szó szerinti kivonattal, `forditasok.tsv`-sor nélkül → „Fordítás függőben”); **(2)** a bekötés a #9-re marad, az ISTENTISZT-001 héber 1. szerepe `adatosítva, nincs bekötve` (a mai állapot), ami a #78 aranymintájánál látható hiány; **(3)** a héber 1. sor állapota `nincs adatosítva`-ra javul az adatrétegben. Javaslat: (2) vagy (1) a DT-F42a-döntés újranyitásával; a (3) az adatréteg külön lépése.

### 13. A negyedik út (felhasználó, 2026-10-08) — a 14. szakasz felülírja, a tartalma historikus

**Ág: köthető.** A héber 1. szerepnél (ISTENTISZT-001) a meglévő, közkincs BDB-sorokra hivatkozik a render: `BDB H7121` (2.c., 3. jelentés) és `BDB H8034` (részlet) a `lexikon_hivatkozasok.tsv`-ből, „meglévő BDB-sor (DT-F42a kiváltás)” megjegyzéssel, a 2. szerepnél álló szöveg felé mutatva. Új adatsor és `jeloltek.tsv`-sor nincs; a `szotar_szerepek.tsv` forrás-oszlopa (TBESH) érintetlen (a módosítás külön döntés: DT-F78d). A Strong_szotar-ra nem volt szükség (a BDB-sorok megvannak; a Strong_szotar CC BY 4.0, de új forrást vezetne a szerepbe — opció a DT-F78d 3. pontjában), SDBH/KJV/BSB nem használva.

`scope=adat/lexikon_hivatkozasok.tsv (szotar=BDB, strong=H7121,H8034), split('\t') | forras=manual (olvasás, a render saját függvényei) | ts=2026-10-08`

Hatás: az `adatosítva, nincs bekötve` állapot az ISTENTISZT-001-nél nem jelenik meg; a TEREMT-002 héber 1–2. szerepén igen (nincs BDB-sora: a #9-nek **a BDB-t kell bekötnie, nem a TBESH-t**, l. DT-F78d).

### 14. A DT-F78d lezárása (felhasználó, 2026-10-08, chat) — ez felülírja a 12–13. szakasz TBESH-ra vonatkozó állításait

A TBESH licence tisztázott (DT-F33f, `adat/licencek.tsv`: `tisztazott`, CC BY 4.0); a DT-F42a csak a H7121 „részlet” sorát váltotta ki BDB-vel, a TBESH egészét nem zárta ki. A `szotar_szerepek.tsv` héber 1. sora VÁLTOZATLAN (TBESH, `adatosítva`).

- A „DT-F42a miatt kizárt / nem kerülhet vissza a TBESH-szöveg” jellegű mondatok (12–13. szakasz, korábbi jelentések) ezzel javítva: a DT-F42a egyetlen sor (H7121 „részlet”) kiváltása volt.
- A bekötés (H8034 TBESH-sora és a szótári sor jelölt-folyamata) NEM a #78-ban történik, hanem a #9-ben; adatot (`lexikon_hivatkozasok.tsv`, `jeloltek.tsv`) a #78 nem írt.
- **Render (ISTENTISZT-001 héber 1. szerep):** H7121 = jelölt üres blokk, mutató: „a H7121 alapjelentését a BDB 2.c adja (DT-F42a)” (a 2. szerepnél a BDB 2.c és 3 változatlan); H8034 = `adatosítva, nincs bekötve`, mutató a #9-re. A BDB-hivatkozás a H8034-nél megszűnt. TEREMT-002 héber 1–2.: változatlanul `adatosítva, nincs bekötve`, a #9 köti be.
- Kód: `SZEREP_TOKEN_MUTATO` és `_token_ures_blokkok` (`lexikon_general.py`; a korábbi `SZEREP_KIVALTO` megszűnt). Tesztek: 16 OK. Próbarenderek újragenerálva (`generalt_proba/F78_szerepmatrix_proba`, `generalt_proba/TEREMT-002_szotari_proba`); az éles `lexikon/` változatlan.

### 15. Állapot

M0–M3 kész, a javítókör és a DT-F78d lezárása kész. Következik: az ellenőr újrafuttatása (orkesztrátor).
