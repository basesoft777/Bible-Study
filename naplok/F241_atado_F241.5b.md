# F241 átadó — F241.5b, 4. menet: a (2) kész a D20 (1), D21, D22 licencmondataival → következő: a (2) PR, utána a (3), a (4)

*2026-11-24 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · a döntések: `naplok/F241_dontesek.md` (D1–D22); előbb azt olvasd. A menet jelentése: `naplok/F241_jelentes.md`, „F241.5b — 4. menet”.*

## Állapot

- **#855 (`claude/f241-5b-1`):** a main-re igazítva az A1 (#860) után; a diff csak az (1) rész. Fej `14d39d2a` (a TÖRLÉS-SZÁNDÉKOS jelölő commit az átadó két régi címsorára, E5). Merge: az integrátortól, zöld CI után.
- **(2) (`claude/f241-5b-2`):** a D16 (a)–(c) (3. menet) és a 4. menet: D20 (1) — a saját mondatú források (LSJ, OSHL, tW) előírt megjelölése szó szerint a Kolofonban (`{megjeloles}` a három sablonsorban, a megjelenítő e nélkül megáll), a licenckapu `sablonos` kivétele megszűnt; a tW-leltár mezője a LICENSE.md szó szerinti mondata; D21 — az LSJ „[date of access]” helyén 2026-09-07 (az adat letöltése) és a lap saját mondata a letöltési útról; D22 — „átdolgozott változat” az LSJ-előtagban. Mérve (gépsorral): HAMART-001 regresszió `--teljes` RENDBEN (S8D-MEGJ-1 az új LSJ-sorra), `teszt_kolofon` 29/29, ISTENTISZT-001 Kolofon: a három mondat szó szerint, „[date of access]” nincs. **Hátra:** a #855 merge-e után a main behozása, PR („F241.5b (2): Kolofon-mondat, a szócikk teljességmérése, névelő-kapu cellatípus szerint”; első sor: Mérce · Állapot · Következő · Akadály), zöld CI, merge-kérés az integrátornak.
- **(3)** (D18: csak ahol a szó a három lapon félrevezető; D17 névazonosság-kapuval; saját kis PR a (2) után): a lapon-mérés kész — `side-session-notes/local_5140778b…/F241.5b_3_lapon_meres.tsv`: 43 sablonsor (27 „lánc”, 16 „szónézet”), soronként a két lapon (ISTENTISZT-001, HAMART-001) megjelenő darabszám és a mondat. A TEREMT-001 a main-en az új generátorral nem generálható (B47: a kézi forrása a #820-on van), nem mérve — a #820 után pótolni. Következő lépés: soronként eldönteni, hol félrevezető (a „lánc” ott, ahol a lap a motívum szókészletét nem láncként vezeti be; a „szónézet” az olvasó saját feliratára, „szó-lap”), az új szövegeket soronként, egyben ⛔ az integrátornak; a kapu a `szokincs.MASODIK_NEV`-be.
- **(4)** ⛔: a sablontábla három lapon megjelenő sorai, soronként egyben az integrátorhoz; a többi N-F241a.
- Nyitott licenckérdés nincs (D22 lezárta); a #858 két új hibaosztálya (894 nem-LSJ pótszöveg, téves Strong→szócikk hozzárendelés) külön sessioné.

## Szabályok

- A lapgen-futás és a lapgent rejtő teszt (`teszt_regresszio`, `teszt_kolofon`, `teszt_kapuk`) a gépsorral: `python eszkozok/gepsor.py futtat --leiras "…" -- <parancs>` (#861). Más session folyamatát soha nem állítod le.
- Hasznos segédek (a scratchpadben, újraírhatók): `meres3.py` (in-process lapkészítés, a `lapgen.bemenet.nyelv` modul `sablon` függvényének burkolásával a használt sablonkulcsok számlálása — a modult `importlib.import_module`-lal kell venni, mert a `lapgen.bemenet.nyelv` név a csomagban függvény); `futas.py` (general.py `--cel lexikon2` repón kívülre → `regresszio.py --teljes --reszletes`); engedélysor-hash csere a `--reszletes` kimenetből; a referencia hash-sorai: sha256 a CRLF→LF normalizált bájtokon.
- A brief fejlécét (`kovetkezo`) a menet frissíti; kontextus-plafon kb. 150 ezer token.
