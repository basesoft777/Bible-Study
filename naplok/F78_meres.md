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

### 6. Állapot

M0 kész. **⛔ Megállás** (brief M0 vége és a blokk-átrendezés miatt): a felhasználó dönt, hogy a teljes átépítés vagy a szűkített hatókör (S1–S5) érvényes. Az M1 (mátrix-bővítés) a hatókör-döntéstől független, de a brief szerint az M0 végén megállunk.
