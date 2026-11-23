# F241 — jelentés (218c: átállás az új lapgenerátorra)

*FELADATOK #241 · brief: `F241_GENERATOR_UJ_C_BRIEF.md` · döntések: `naplok/F241_dontesek.md` · BRIEF_SABLON „Jelentés”.*

## F241.0 — Indítás (2026-11-23)

*scope=F241.0 | forras=gh pr view 809/810/820; git (origin/main a3405522); feladatok.py fuggesek; grep a lexikon_general importjaira | ts=2026-11-23*

**Modell-ellenőrzés.** A session `claude-opus-5-5`, a brief `modell` mezője `opus`: egyezik.

**Előfeltételek.**

| Feltétel | Állapot | Forrás |
|---|---|---|
| #809 (F218a) a main-en | MERGED, `3c327ac6`, 2026-11-23 11:11 UTC | `gh pr view 809` |
| #810 (F231, olvasó egyben) a main-en | MERGED, `a3405522`, 2026-11-23 18:27 UTC | `gh pr view 810` |
| #839 (a brief befogadása) a main-en | `7cdcba5a` | `git log origin/main` |
| az integrátor jele | megvan | `naplok/F241_dontesek.md` D8 |

Az A szelet ága: `claude/f241a-kiadasi-ut`, az `origin/main` `a3405522`-ből.

**A #820 N-tételei (bemenet, brief 6. pont).** A PR #820 (`claude/nervous-kare-9d2361`, nyitott, fej `e9e2a136`) `nyitott/uj/nervous-kare-9d2361.md` fájljában két tétel áll:
- **N-F239a**: a 3. szakasz arány-mondata a legfeljebb 10-szeres arányra (`lapgen/megjelenites/md/kizart.py`, `konfig.KIZART_ATLAG_HATAR`) → F241.8.
- **N-F239b**: az olvasói kapu a szakirodalmi mű eredeti angol címét `ANGOL`- és `MUNKASZO`-bukásnak olvassa (`olvasoi_kapu.py`) → F241.3.

**N-F239c még nincs fent.** A #820 U5-csomagja (az átadó `naplok/F239_atado_U4b.md` 2. (c) pontja szerint) a 3/b generált tételeit (M-CSERE, M-NYERS, M-RÁRAKÓDÁS …) mechanizmusonként egy N-tételbe gyűjti, a következő betűvel. Amikor megjelenik, az F241.8 bemenete; addig helyőrző.

**Függések** (`feladatok.py fuggesek`, a main `a3405522`-n): `KOR` nincs. `FUGGES 241 217`, `241 218` (kézi). A 241-et várja (levezetve): #7, #10, #75, #81, #86, #106, #123, #129, #133, #138, #153, #154, #156, #157, #205, #229, #231, #234, #236, #237. Kizárás (közös írt fájl): #7, #122, #123, #133, #153, #154, #157, #171, #205, #231 (`eszkozok/olvaso_szerver/teszt_olvasoi_merce.py`), #237 (`eszkozok/lapgen/`). A fejléc függései nem változtak.

**Megfigyelés:** a #231 briefje a main-en a #810 merge-e után is `allapot: fut`, ezért a #231 a kizárás-listán áll. Az F241 nem javítja (más feladat fejléce), az integrátornak jelezve.

**A `lexikon_general` fogyasztóinak leltára** (import vagy hívás; a `naplok/` és az `eszkozok/lapgen/` nélkül): **40 fájl**, mind benne az `ir`-ben, ezért az F241.0 ⛔-je (a lista bővebb, mint az `ir`) nem áll fenn:

`eszkozok/ellenoriz.py`, `eszkozok/ellenorzes/allitas_adat.py`, `eszkozok/f127_res_eles.py`, `eszkozok/feladatok.py`, `eszkozok/general.py`, `eszkozok/glossza_lexikon_forditas.py`, `eszkozok/jelolt_eloszures.py`, `eszkozok/kiejtes_szoveg.py`, `eszkozok/lap_javit_proba.py`, `eszkozok/lektor_kerdesek.py`, `eszkozok/lexikon_v2_migracio.py`, `eszkozok/motivum_hatar.py`, `eszkozok/nyilt_mag_export.py`, `eszkozok/olvaso_szerver/teszt_olvasoi_merce.py`, `eszkozok/olvaso_szerver/teszt_visszhang_kapu.py`, `eszkozok/olvasoi_kapu.py`, `eszkozok/render_diff_osztalyoz.py`, `eszkozok/szakasz_cimke_levezet.py`, `eszkozok/torzscikk_general.py`, `eszkozok/tsk_versszam_felmeres.py`, `eszkozok/visszhang/megfelelo_kinyer.py`, valamint 19 teszt: `eszkozok/teszt_bdb_tagolas.py`, `teszt_dontes_allapot.py`, `teszt_ellenoriz_11.py`, `teszt_ellenoriz_31.py`, `teszt_ellenoriz_35.py`, `teszt_ellenoriz_vedokorlat.py`, `teszt_f194_szopar.py`, `teszt_f212_cs3.py`, `teszt_feladatok.py`, `teszt_futtat.py`, `teszt_gorog_rovid_jelentes.py`, `teszt_gyokerok_kapuk.py`, `teszt_hatastortenet.py`, `teszt_kesz_lap_hamart.py`, `teszt_lexikon_adatres.py`, `teszt_olvasoi_kapu.py`, `teszt_sablon_javitokor.py`, `teszt_szerepmatrix.py`, `teszt_szotari_gerinc.py`.

A Workflow-fájlok (`.github/workflows/*.yml`) a `lexikon_general`-t név szerint nem hívják, csak a `general.py --cel lexikon`-t (F241.2).

**Szöveges említések** (nem import; az archiválás nem változtatja őket, mert történeti hivatkozások, a régi fájl az `archivum/lexikon_general/` alatt elérhető marad):
- a `lapgen/` három helye (`bemenet/nyelvi_hatter.py`, `konfig.py` megjegyzés; `tesztek/teszt_regresszio.py` útvonal-literál egy érintettség-tesztben, ez az F241.13-ban átírandó);
- `konkordancia/README.md`, `konkordancia/VISSZHANG_README.md`, `adat/SEMA.md`, `MUNKAMENET.md`, `sablonok/6_PaRDeS_lexikon_oldal_sablon.md`, valamint hét `adat/*.tsv` proveniencia- vagy forrásmezője (`kiejtes_szabalyok`, `lap_javitasok`, `lapgen_bemenetek`, `lapgen_sablonok`, `licencek`, `olvasoi_nevtabla`, `tematikus_sajat_szo`);
- a `CLAUDE.md`: csak a szerkesztő szavára (brief 2. pont);
- 24 brief `olvas` mezője: ezeket az áthelyezés commitja frissíti (`CLAUDE.md` „Git”, E27), mert a szabály előírja;
- a `naplok/` 15 régi mérőszkriptje importálja: napló, nem fogyasztó; az archiválás után nem futtathatók (brief 2. pont).

**Lapgen-futás:** az F241.0-ban nem volt. Indításkor egy `python.exe` futott (PID 21132, 14 MB, nem lapgen-méret).

## F241.1 — Kiadás mód és frissesség (N221; DT933 (1); GK-27, T9)

*Végrehajtó: `claude-opus-5-5` (kért: `opus`, egyezik) · 2026-11-23.*

**Megvalósítás.**
- **Új bemeneti modul** `eszkozok/lapgen/bemenet/jovahagyas.py`: a szerzői jóváhagyás frissessége kiadás módban. A legutóbbi érvényes átnézés-sor (`lap_atnezesek.tsv`, SEMA 2.48: `ki` = `felhasználó`, nem üres `idezet`, a `lap_commit` őse a HEAD-nek) `lap_commit`-ja és a lap (`lexikon/<ID>_TUDOMANYOS.md`) mai utolsó commitja: egyezésnél **FRISS**. Egyezés nélkül a motívum kézi bemeneteinek lenyomata dönt (a jóváhagyott commitban, `git show`, és a munkafán): azonos → **CSAK_GENERALT** (változásjegyzék-sort kér, új nézést nem); eltérő → **ELAVULT** (új nézés). Átnézés-sor nélkül **NINCS_ATNEZES**, a repóban nem álló lapnál **NINCS_LAP**. A git-olvasás nem tartalmi olvasás, nem kerül az olvasási naplóba (a `bemenet/frissesseg.py` mintájára); csak kiadás módban fut.
- **A jóváhagyás tárgya** (`konfig.JOVAHAGYAS_BEMENETEK`, technikai döntés, DT920): a jegyzék azon bemenetei, amelyek a motívum kézi forrását vagy a motívumra kulcsolt kézi adatát hordozzák — B02, B03, B04, B38, B39, B40, B45, B46, B47, B50, B53, B56, B67, B70. A lenyomat a motívum saját fájljából (`motivumok/<ID>.md`) az egészet, a táblákból a fejlécet és azokat a sorokat veszi, amelyeknek valamely cellája pontosan a motívum azonosítója (más motívum sorának változása nem érinti). Nincs benne: a kiadási és átnézési napló (B48), a befagyasztás (B59), a generátor saját táblái (B65, B66, B68), a több motívum közös forrás- és szótári adata (konkordancia, fordítások): ezek változása a generált blokkokat érinti. A halmaz a mérés óvatos oldala: a vitás eset (pl. a B38/B39 visszhang-sorai) inkább új nézést kér.
- **Kapu** (`szamitas/kolofon.py` `kapu`): kiadás módban a kézi résű lap csak FRISS vagy CSAK_GENERALT állapotban megy át; mérés nélkül, NINCS_LAP, NINCS_ATNEZES és ELAVULT esetén BemenetHiba, az okkal. A modell új mezője: `frissesseg`.
- **A mondat** kiadás módban: „a szerző jóváhagyta” (új sablonsor: `kolofon.jovahagyas.friss`, a régi lap szövege; a kapu után áll, ezért nem állíthat hamisat). Munka módban változatlan („a szerző a lap korábbi változatát hagyta jóvá (dátum)”), git nélkül.
- **A változásjegyzék-sor** (CSAK_GENERALT): a kapu nem kéri számon, mert a kiadás sora (`kiadasok.tsv`) a `/kiadas` lépése (F241.7), és a kiadott lap új kiadás nélküli változását az E28 őrzi (F241.2). Technikai döntés: így nincs két őr ugyanarra.

**Teszt** (`teszt_kolofon.py`): `Jovahagyas` — a kapu mind az öt állapotra és a generált lapra; a kiadás módú mondat. Új `Frissesseg` osztály (hamis git-olvasóval, az ISTENTISZT-001 mai átnézés-sorával): egyező `lap_commit` → FRISS; csak a lap változott → CSAK_GENERALT; közös tábla más motívumra eső sorának változása → CSAK_GENERALT; kézi próza (`motivumok/<ID>.md`) változása → ELAVULT; adat (`kapcsolatok.tsv` motívumsora) változása → ELAVULT; lap nélkül és átnézés nélkül; a valódi git-olvasó. `futtat.py kolofon`: 21 teszt, 0 bukás; `bemenet szoveg kapuk`: 58 teszt, 0 bukás (3 kihagyva).

**Mérés a valós repón** (kiadás módú frissesség, a munkafán): ISTENTISZT-001 → **ELAVULT** (átnézés `ee33a860`, 2026.11.04; azóta a kézi forrás és az adat változott — a 2. kiadáshoz új nézés kell, ez az F241.7 ⛔-je); HAMART-001 → **NINCS_ATNEZES** (a `lap_atnezesek.tsv`-ben nincs HAMART-sor; a B szelet HAMART-kiadásához (F241.10) átnézés-sor kell); ALVIL-001 → ELAVULT (befagyasztott, nem generálódik).

**Regresszió.** A sablontábla (B66) új sora miatt a hash-őr megállt; `PARDES_DATUM=2026-11-13 general.py --cel lexikon2 --id HAMART-001` + `regresszio.py --id HAMART-001 --teljes`: **RENDBEN**, engedély nélküli diff-sor 0 (munka módban a lap bájtra változatlan). A B66 hash-sora a `naplok/F218_referencia.tsv`-ben külön commitban frissült (a brief 8.1 pontja); utána `hash_or_kapu`: RENDBEN, 210 sor.

**Lapgen-futás:** egy (a regresszió generálása), előtte a `python.exe`-lista: egy másik session `push_elott --reszleges` / `teszt_futtat` (olvasó-tesztek, 25–27 MB), nem lapgen-futás.

*Proveniencia: `scope=futtat.py kolofon; futtat.py bemenet szoveg kapuk; general.py --cel lexikon2 --id HAMART-001 (PARDES_DATUM=2026-11-13); regresszio.py --id HAMART-001 --teljes; hash_or_kapu.py; jovahagyas.frissesseg (ISTENTISZT-001, HAMART-001, ALVIL-001) | forras=a munkafa a commit előtt | ts=2026-11-23`.*

## F241.2 — Célnév és Action (N243 (2), (4) első fele)

*Végrehajtó: `claude-opus-5-5` (kért: `opus`, egyezik) · 2026-11-23.*

**Megvalósítás (technikai döntések, DT920).**
- **`--cel lexikon` = az új generátor** (`general.py` → `lapgen.fo.futtat`); a régi generátor `--cel lexikon_regi` néven fut; a `lexikon2` (a 218a próbaneve) az új generátor álneve marad. A `mind` cél a `lexikon_regi`-t futtatja (változatlan viselkedés).
- **Átállás motívumonként** (a brief korlátja: a kiadott lap új kiadás nélkül nem változhat): `general.py` `ATALLT_MOTIVUMOK` (kezdetben üres) és `lexikon_generator()`. A `--cel lexikon --id X` a régi generátort futtatja (visszaút), ha X-nek commitolt lapja van, és X nem állt át; lap nélküli (új) motívumnál és átállt motívumnál az újat. A motívum a saját új generátoros kiadásának commitjában kerül a listára (ISTENTISZT-001: F241.7; HAMART-001: F241.10). **Miért nem „régi lista”:** egy csak a HAMART-001-et tartalmazó visszaút-lista a befagyasztott régi lapokat (ALVIL, ANTROP, KIRALY …) az új generátorral generálná a műhely nulla-diffjében; a fordított lista minden commitolt régi lapot véd.
- **A G01 sora** (`adat/generalt_nezetek.tsv`): a parancs `--cel lexikon … --mod {mod}`; a `generalt_nezetek.lexikon_general` (az egyetlen belépési pont) a kiadott lapot (sora van a `kiadasok.tsv`-ben) kiadás módban, a többit munka módban generálja — a kiadott lap Kolofonja így a „jóváhagyta” mondatot kapja, és a GK-27 kapuja őrzi (F241.1). A régi generátor a `--mod`-ot elfogadja és figyelmen kívül hagyja. A G01 és a G02 `bemenetek` oszlopa már a `lapgen_bemenetek.tsv` B-azonosítóira hivatkozik (`B*`, illetve `B03;B04;B05;B06;B07;B56`; a jegyzék kapuja ellenőrzi): itt változás nem kellett.
- **E28 és `feladatok.yml`:** mindkettő a `lexikon_general()`-on át generál, így a G01-gyel együtt áll át; a workflow-fájl nem változik.
- **Fogyasztók:** a régi generátor belső függvényére épülő két eszköz kifejezetten a régi célra: `glossza_lexikon_forditas.py` (a régi `forditas_ehhez` naplózása), `lap_javit_proba.py` (a memóriában cserélt forrás a régi olvasón át); `adat/SEMA.md` 2.19 (`--cel lexikon_regi --ellenoriz`). Az `ellenoriz.py` javítási megjegyzései (`--cel lexikon --id <ID> --ir`) a visszaút miatt a régi lapra helyesek; az F241.3 nézi újra. A `lexikon_ket_ut_meres.py` a visszaúton változatlanul fut.
- **A brief határán túl javítva** (külön commit, Munkamód 5): `eszkozok/muhely_allapot.py` nulla-diffje a `general.py --cel lexikon` közvetlen hívása helyett az egyetlen belépési pontot (`generalt_nezetek.lexikon_general`) hívja — így az átállt, kiadott lapot kiadás módban generálja (különben az ISTENTISZT-001 2. kiadása után hamis piros jelzést adna).
- **A `lexikon/` végleges helyére írás** (az új generátor ma csak repón kívülre ír): az F241.7-ben, a kiadással.

**Teszt** (`lapgen/tesztek/teszt_futas.py`): `Celnev` — lap nélküli motívum → új generátor (a `--mod` átmegy); commitolt régi lap → régi generátor; átállt motívum → új; `--cel lexikon_regi` → régi. `G01Mod` — a parancs `--cel lexikon` és `{mod}`; a HAMART-001 (kiadott) kiadás, a TEREMT-001 munka módban. `futtat.py futas`: 12 teszt, 0 bukás. `teszt_generalt_nezetek.py`: RENDBEN. `generalt_nezetek.py --ellenoriz`: rendben (11 sor). Végponttól végpontig: `generalt_nezetek.py --gyoker <tmp> --id HAMART-001` → a TUDOMANYOS és a KIZARASOK „nem változott” (a visszaút bájtra a régi lap).

*Proveniencia: `scope=futtat.py futas; teszt_generalt_nezetek.py; generalt_nezetek.py --ellenoriz; generalt_nezetek.py --gyoker <tmp> --id HAMART-001 | forras=a munkafa a commit előtt | ts=2026-11-23`.*
