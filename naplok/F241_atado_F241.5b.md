# F241 átadó — F241.5b, 2. menet (1) kész → 3. menet: a D16 (a)–(d) és a ⛔ (4)

*2026-11-24 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/f241a-kiadasi-ut` (A szelet), PR #841 · a döntések: `naplok/F241_dontesek.md` (D1–D16); előbb azt olvasd. A menet jelentése: `naplok/F241_jelentes.md`, „F241.5b — 2. menet, (1)”.*

## Állapot

- **Kész (D16 sorrend (1), a D15 szerint):** az olvasói-indoklás tábla (B76, `adat/olvasoi_indoklasok.tsv`, SEMA 2.74, `lapgen/bemenet/olvasoi_indok.py`) kapuval; a szakszólista egy helyen (`lapgen/szokincs.py`, az `olvasoi_kapu.MINTA_SZAKSZO` innen olvas); a 3. szakasz kettőzött kereszthivatkozás-táblája helyett hivatkozó mondat (`k3.kh_masutt`, `dontes=var`); a B56 két megjegyzése és a `kiadasok.tsv` szava helyben; a B56 a szókincs-kapu alatt. ISTENTISZT-001: MINTA 91 → 1. HAMART-001 regresszió `--teljes`, hash-őrrel: RENDBEN. Tesztek: `futtat.py kizart kereszthiv bemenet vaz festek kapuk olvasoi_indok regresszio` (a `kapuk` B5-mintapéldája javítva, l. a jelentést).
- **A D17 (szűkített tiltólista, névazonosság-kapu) a kódban** (`lapgen/szokincs.py`); a lapok szövegét nem változtatja (a két lap minta-mérése a D17 után: ISTENTISZT-001 1, HAMART-001 0), a kapu a valódi adaton átmegy (`teszt_olvasoi_indok`). **Hátra van az (1) rész-PR-jához (`claude/f241-5b-1`):** a lapgen-sor „szabad” jele után (az integrátor döntése: előbb a #821, majd az A1 session) az ISTENTISZT-001 és a HAMART-001 újragenerálása a D17-es kóddal, a HAMART-001 regressziója `--teljes`, utána merge-kérés az integrátornak.
- **Nyitva, gazdát kér (a jelentésben):** a BDB „arab,;” (1 MINTA) — a fájljait (`forditasok.tsv`, `bdb_szakasz_hu.tsv`) a #821 ága írja; a #821 merge-e után.
- **Az `ellenoriz` 11. szabálya:** az F241.7 első lépése (változatlanul, l. az előző átadó és a jelentés).

## Következő (D16 sorrend)

1. **(2) (a)** B66 `kolofon.ertek.kriterium` → „A lap elején áll ([{cim}](#{horgony})).” (a paraméterek maradnak; a cella a Kolofon táblájában). **(b)** B65 `irod_adat` két sora (`naplok/F123_teljesseg_<ID>.tsv`, `…_blokkok.tsv`): „Lap teljesség-mérése” → „A szócikk teljességmérése”, `eredet` → `uj`. Mindkettő a mérce B65/B66 hash-sorát és a HAMART-001 engedélysorait érinti (Irodalom, Kolofon): a `naplok/F218_elteres_engedely.tsv`-ben a S9C-N178-IROD / S9C-N178-KOLOFON stb. sorai.
2. **(2) (c) LISTA_NEVELO a cella típusából.** A kapu ma a Markdown-szövegen fut (`olvasoi_kapu.ell_lista_nevelo`), ott a cella típusa nem látszik; a lapmodellben igen (`fo.lap_keszit(...).nezetek['TUDOMANYOS']` sorainak `tartomanyok`: `(k, v, Fajta)`; `Fajta.IDEZET`, `PROZA` = kézi, `SABLON`). Javasolt technikai út: a szabály (a `NEVELO_ELEM_RX`) marad az `olvasoi_kapu`-ban, egy helyen; a lapgen a lapmodellen futtatja (a cella első karakterének fajtája IDEZET vagy PROZA → nem méri), generáláskor GK-kapuként; a Markdown-ágon az új generátor lapján (az F241.7 után a `lexikon/`-ban) a szövegkapu ugyanezt csak akkor tudja, ha a típus a lapmodellből jön — ezt a 11. szabály átkötésével együtt érdemes eldönteni (az ellenoriz a lapgen lapjára). A 9 ISTENTISZT-hely: 6 Kulcsszó (Károli-idézet), 3 Funkció (B03/B46 `funkcio`, kézi), 1 Kolofon (a), amelyet az (a) javít.
3. **(3) a két szakszó (D16 (d), a D17 szerint):** a „lánc”, a „szónézet” és a „lap” nem tiltott szó; a csere ott marad, ahol a szó jelentése más, mint a lapon bevezetett név (a motívumtól független sablonsorban „lánc” → „a motívum szava”; „szónézet” → az olvasó saját neve a szó nézetére, `eszkozok/olvaso_szerver/konfig/feliratok.tsv` / a névtábla sora; „lap” → „szócikk”). A kapu névazonosságot mér (`lapgen/szokincs.py` `MASODIK_NEV`), nem tilt; a tiltólista (`SZAKSZO`) a D17 (1) hat szava, nem bővül. A 45 `ok_cella`-másolat megszűnik (a B56 az egy forrás). A sorok listája: `side-session-notes/local_5140778b…/F241.5b_szokincs_munkalista.tsv`.
4. **(4) ⛔ a sablontábla többi sora:** az új szövegek soronként, egyben az integrátornak (`local_5140778b-1529-4b72-b4a8-b9b5a4c06e6c`, SendMessage), a `k3.kh_masutt` mondatával együtt (`dontes=var`, D15 (2)); várni a válaszra. A szókincs-kapu (statikus teszt a B65/B66 minden során, D12) és a névtábla-identitás kapu a javítással egy commitban.
5. Minden lépés után: célzott tesztek, az ISTENTISZT-001 mérése (`olvasoi_kapu.lap_meres`), a HAMART-001 regressziója; a mérce hash-sora és engedélysorai külön commitban. Hasznos segédek a menetből (a jegyzetmappában nincsenek, újraírhatók): a regresszió `--reszletes` diff-fájlából párosított (régi, új) hash-ek → engedélysorok; a referencia-tábla sorainak újraszámolása a `regresszio._olvas` normalizálásával.

## Munkarend (az integrátor, 2026-11-24, a szerkesztő „Igen, így” szavával)

- Az F241.5b négy része egyenként külön PR: kész rész → saját ág (`claude/f241-5b-<n>`) a `f241a-kiadasi-ut` aktuális fejéből (az A1, `claude/f241-a1` merge-e után a main-ből), PR a main-be, merge-kérés az integrátornak. A #841 ágát (`claude/f241a-kiadasi-ut`) is ugyanezzel a fejjel viszed tovább.
- Új hibaosztály nem bővíti a részt: egy sorban az integrátornak, ő ad gazdát.

## Szabályok (változatlanul)

- Helyi ág: `git checkout -B <helyi> origin/claude/f241a-kiadasi-ut` (az `f241a-helyi` és az `f241a-helyi-2` név más worktree-ben foglalt lehet); push: `git push origin HEAD:claude/f241a-kiadasi-ut`.
- Egyszerre egy lapgen-futás; előtte `python.exe`-lista; más session folyamatát soha nem állítod le.
- Célzott tesztek (`futtat.py <név>`), a hosszú kör háttérben (a `kizart … regresszio` kör kb. 12 perc); a HAMART-001 regressziója: `PARDES_DATUM=2026-11-13 general.py --cel lexikon2 --id HAMART-001 --kimenet <repón kívül>`, `regresszio.py --id HAMART-001 --uj <kimenet>/lexikon --teljes`.
- Kontextus-plafon kb. 150 ezer token; lépéshatáron átadó.
