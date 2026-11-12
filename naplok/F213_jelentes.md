# F213 — Szótári nézet az olvasóban: jelentés

*FELADATOK #213 · `F213_SZOTARI_NEZET_BRIEF.md` · modell: claude-opus-5-5 · ág: `claude/f213-szotari-nezet-a55839`*

## 1. A menet szakaszai

### F213.0 — brief; az F104 beolvad (2026-11-12)
A brief a `BRIEF_SABLON.md` szerint; az F104 (PR #671, a main-en) lezárva, a hátralévő felhasználói próba és a nyitott pont ide olvadt.

### Mockup a design-vásznon (2026-11-12)
Új „Szótári nézet” oldal (https://claude.ai/artifact/Hq87CVsbpZCy4GCBFDedth), öt saját keret: H0216 szónézet (1Móz 1:3-ból), H0127 szónézet, H0127 motívumlap-nézet (HAMART-001), jelek és szabályok, szófej (alapjelentés, glossza, versszintű sor). Valódi adat: `adat/bdb_szakaszok.tsv`, `adat/bdb_szakasz_hu.tsv` (a szerver javítási láncán át), `adat/bdb_vers_jelentes.tsv`, `adat/szotar_szakasz_cimke.tsv`, `adat/elofordulasok.tsv`, `konkordancia/Macula_heber_*.tsv`. *(proveniencia: scope=H0216, H0127, H1242 | forras=a fenti táblák, scratchpad-szkriptek | ts=2026-11-12)* A felhasználó jóváhagyta („mehet”, az orkesztrátoron át).

### F213.1–F213.3 — hatókör-bővítés és döntés
- F213.1: a szófej és a szópanel magyar bekötése (az orkesztrátor feladatleírása, a felhasználó: „Igen, az F213”).
- F213.2: a görög fej bekötése az F213-ba (orkesztrátori döntés).
- F213.3: DT-F213a — az alapjelentés elsődleges forrása a magyar glossza (a felhasználó: „Igen, B (glossza)”).

### F213.4 — a szerver
- **Szókártya** (`blokkok._r_bdb_apparatus`, `bdb_szokartya.py`): fej (alapjelentés, csukva az alakok és a rokon nyelvek), a jelentések rendje (a motívum jelentései jelölve), jelentésenként glossza (`szotari_glossza.olvasoi_glossza`, közös a 4.2 kártyájával), használati sorok (szerkezet → magyarázat → helyek), csukott „Apparátus és szövegkritika” és „Angol eredeti”, LXX-pár (Macula, névelő nélkül), „még N hely”, nézetkapcsoló (`?nezet=`, localStorage). Az F104 jelölése (DT178) változatlan szabállyal. Kikerült az elavult „gépi szeletelés; hibás határ előfordulhat” címke és a szeletenkénti forrássor; a régi vázlat-, jelentéscím- és csoportsor-renderer holt kódja törölve (170 sor), a regiszterből 12 régi elem, a CSS-ből 34 szabály.
- **Alapjelentés** (DT-F213a): magyar glossza → magyar BDB-fejsor (a nemi tanú igehelye nem vág, csak szófaj nem fogadható el) → angol; a görög fejben a magyar TBESG-glossza. Strong-szótár és „Ebben a versben”: magyar elöl, az angol mellette; a versszintű UBS magyarul, ahol van. A szűrés blokkszintű (`K.glossza_ok`, `K.ubs_hu_ok`, `K.szotar_ok`).
- **Bekötési audit** (orkesztrátor): TBESG, LSJ, SDBH/SDGNT, tW, TBESH, Nave magyarul, ahol van (`q.forditas_bejegyzesek`, `q.glosszak_heber_hu_angol`, `q.nave_tema_hu`); a „modell-kimenet” jelleg adatfüggő (`jelleg_fn`).

**Mérés — alapjelentés** (`naplok/F213_alapjelentes_meres.py`) *(proveniencia: scope=strong_szotar H+G (14347) | forras=naplok/F213_alapjelentes_meres.py, pardes.db 2026-11-12T15:51:52Z | ts=2026-11-12)*:

| | előtte | utána |
|---|---|---|
| héber (8718) | magyar BDB 6591 · csak szófaj 647 · angol 1475 · nincs 5 | magyar glossza 8718 |
| görög (5629) | angol 5603 · nincs 26 | magyar glossza 269 · angol 5334 · nincs 26 |

Javul: héber 2127, görög 269 (a „csak szófaj” küszöb javítása után mérve; az első mérés a rövid szót, pl. „kő”, is szófajnak vette: 2190); angol marad: héber 0, görög 5334 (N-F213c).

**Mérés — bekötési audit** (`naplok/F213_bekotes_meres.py`) *(proveniencia: scope=pardes.db forditasok, nave_tema_hu, glosszak_heber_hu | forras=naplok/F213_bekotes_meres.py, pardes.db 2026-11-12T15:51:52Z | ts=2026-11-12)*: TBESH-glossza 8176 / 9345 Strong; SDBH-domén 3647 / 8557; SDGNT-domén 123 / 5312; TBESG-glossza 269 / 10 847 (szócikk 4); LSJ 2; tW-cikk 29 / 598; TBESH-szócikk 1; Nave 23 téma (1506 vers).

### F213.5 — a main beolvasztása (#718, #719)

## 2. Független ellenőrzés

(a push és a felhasználói átnézés után, ha az orkesztrátor kéri)

## Zárás

- Tesztek: l. a push előtti kapufutás (a CI a pusholt sha-val).
- A main-ről örökölt piros: `teszt_szintek.py` `test_ebben_a_versben_es_az_interlinearis_csempek_koveti_a_blokkok_lathatosagat` és `test_heber_szavak_alacsony_es_magas_szinten` (azonos sorral és állítással a main-en is: 9d2e04e4 előtti állapot, mérve 2026-11-12), `teszt_visszhang_kapu.py` 2 teszt.
- Döntés: DT-F213a (🟢), DT-F213b (🟡, a böngészős átnézés dönt). Nyitott: N-F213a (pe/mem a maqqef után), N-F213c (a görög glosszák fordítása).
- ⛔ merge előtt a felhasználó böngészős átnézése a `192.168.1.172:9765` címen.
