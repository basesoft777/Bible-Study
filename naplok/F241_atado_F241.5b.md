# F241 átadó — F241.5b, 4. menet: a (2) kész a D20 (1), D21, D22 licencmondataival → következő: a (2) PR, utána a (3), a (4)

*2026-11-24 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · a döntések: `naplok/F241_dontesek.md` (D1–D22); előbb azt olvasd. A menet jelentése: `naplok/F241_jelentes.md`, „F241.5b — 4. menet”.*

## Állapot

- **#855 (`claude/f241-5b-1`):** a main-re igazítva az A1 (#860) után; a diff csak az (1) rész. Fej `14d39d2a` (a TÖRLÉS-SZÁNDÉKOS jelölő commit az átadó két régi címsorára, E5). Merge: az integrátortól, zöld CI után.
- **(2) (`claude/f241-5b-2`):** a D16 (a)–(c) (3. menet) és a 4. menet: D20 (1) — a saját mondatú források (LSJ, OSHL, tW) előírt megjelölése szó szerint a Kolofonban (`{megjeloles}` a három sablonsorban, a megjelenítő e nélkül megáll), a licenckapu `sablonos` kivétele megszűnt; a tW-leltár mezője a LICENSE.md szó szerinti mondata; D21 — az LSJ „[date of access]” helyén 2026-09-07 (az adat letöltése) és a lap saját mondata a letöltési útról; D22 — „átdolgozott változat” az LSJ-előtagban. Mérve (gépsorral): HAMART-001 regresszió `--teljes` RENDBEN (S8D-MEGJ-1 az új LSJ-sorra), `teszt_kolofon` 29/29, ISTENTISZT-001 Kolofon: a három mondat szó szerint, „[date of access]” nincs. **Hátra:** a #855 merge-e után a main behozása, PR („F241.5b (2): Kolofon-mondat, a szócikk teljességmérése, névelő-kapu cellatípus szerint”; első sor: Mérce · Állapot · Következő · Akadály), zöld CI, merge-kérés az integrátornak.
- **(3)** (D18: csak ahol a szó a három lapon félrevezető; D17 névazonosság-kapuval; saját kis PR a (2) után): a lapon-mérés kész — `side-session-notes/local_5140778b…/F241.5b_3_lapon_meres.tsv`: 43 sablonsor (27 „lánc”, 16 „szónézet”), soronként a két lapon (ISTENTISZT-001, HAMART-001) megjelenő darabszám és a mondat. A TEREMT-001 a main-en az új generátorral nem generálható (B47: a kézi forrása a #820-on van), nem mérve — a #820 után pótolni. Következő lépés: soronként eldönteni, hol félrevezető (a „lánc” ott, ahol a lap a motívum szókészletét nem láncként vezeti be; a „szónézet” az olvasó saját feliratára, „szó-lap”), az új szövegeket soronként, egyben ⛔ az integrátornak; a kapu a `szokincs.MASODIK_NEV`-be.
- **(4)** ⛔: a sablontábla három lapon megjelenő sorai, soronként egyben az integrátorhoz; a többi N-F241a.
- Nyitott licenckérdés nincs (D22 lezárta); a #858 két új hibaosztálya (894 nem-LSJ pótszöveg, téves Strong→szócikk hozzárendelés) külön sessioné.

## Következő (D16 sorrend)

*Az (1)–(2) kész (#855; a (2) ága, l. „Állapot”). A (3) lapon-mérése kész: `side-session-notes/local_5140778b…/F241.5b_3_lapon_meres.tsv`.*

1. **(3) a két szakszó (D16 (d), a D17 szerint):** a „lánc”, a „szónézet” és a „lap” nem tiltott szó; a csere ott marad, ahol a szó jelentése más, mint a lapon bevezetett név (a motívumtól független sablonsorban „lánc” → „a motívum szava”; „szónézet” → az olvasó saját neve a szó nézetére, `eszkozok/olvaso_szerver/konfig/feliratok.tsv` / a névtábla sora; „lap” → „szócikk”). A kapu névazonosságot mér (`lapgen/szokincs.py` `MASODIK_NEV`), nem tilt; a tiltólista (`SZAKSZO`) a D17 (1) hat szava, nem bővül. A 45 `ok_cella`-másolat megszűnik (a B56 az egy forrás). A sorok listája: `side-session-notes/local_5140778b…/F241.5b_szokincs_munkalista.tsv`.
2. **(4) ⛔ a sablontábla többi sora:** az új szövegek soronként, egyben az integrátornak (`local_5140778b-1529-4b72-b4a8-b9b5a4c06e6c`, SendMessage), a `k3.kh_masutt` mondatával együtt (`dontes=var`, D15 (2)); várni a válaszra. A szókincs-kapu (statikus teszt a B65/B66 minden során, D12) és a névtábla-identitás kapu a javítással egy commitban.
3. Minden lépés után: célzott tesztek, az ISTENTISZT-001 mérése (`olvasoi_kapu.lap_meres`), a HAMART-001 regressziója; a mérce hash-sora és engedélysorai külön commitban. Hasznos segédek a menetből (a jegyzetmappában nincsenek, újraírhatók): a regresszió `--reszletes` diff-fájlából párosított (régi, új) hash-ek → engedélysorok; a referencia-tábla sorainak újraszámolása a `regresszio._olvas` normalizálásával.

## Munkarend (az integrátor, 2026-11-24, a szerkesztő „Igen, így” szavával)

- Az F241.5b négy része egyenként külön PR: kész rész → saját ág (`claude/f241-5b-<n>`) a `f241a-kiadasi-ut` aktuális fejéből (az A1, `claude/f241-a1` merge-e után a main-ből), PR a main-be, merge-kérés az integrátornak. A #841 ágát (`claude/f241a-kiadasi-ut`) is ugyanezzel a fejjel viszed tovább.
- Új hibaosztály nem bővíti a részt: egy sorban az integrátornak, ő ad gazdát.

## Szabályok (változatlanul)

- Helyi ág: `git checkout -B <helyi> origin/claude/f241a-kiadasi-ut` (az `f241a-helyi` és az `f241a-helyi-2` név más worktree-ben foglalt lehet); push: `git push origin HEAD:claude/f241a-kiadasi-ut`.
- Egyszerre egy lapgen-futás: a lapgen-futás és a lapgent rejtő teszt (`teszt_regresszio`, `teszt_kolofon`, `teszt_kapuk`) a gépsorral, `python eszkozok/gepsor.py futtat --leiras "…" -- <parancs>` (#861); más session folyamatát soha nem állítod le.
- Célzott tesztek (`futtat.py <név>`), a hosszú kör háttérben (a `kizart … regresszio` kör kb. 12 perc); a HAMART-001 regressziója: `PARDES_DATUM=2026-11-13 general.py --cel lexikon2 --id HAMART-001 --kimenet <repón kívül>`, `regresszio.py --id HAMART-001 --uj <kimenet>/lexikon --teljes`.
- Kontextus-plafon kb. 150 ezer token; lépéshatáron átadó.
- Hasznos segédek (a scratchpadben, újraírhatók): `meres3.py` (in-process lapkészítés, a `lapgen.bemenet.nyelv` modul `sablon` függvényének burkolásával a használt sablonkulcsok számlálása — a modult `importlib.import_module`-lal kell venni, mert a `lapgen.bemenet.nyelv` név a csomagban függvény); `futas.py` (general.py `--cel lexikon2` repón kívülre → `regresszio.py --teljes --reszletes`); engedélysor-hash csere a `--reszletes` kimenetből; a referencia hash-sorai: sha256 a CRLF→LF normalizált bájtokon.
