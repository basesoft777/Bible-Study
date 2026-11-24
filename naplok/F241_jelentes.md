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

## F241.3 — Lapszöveg-kapuk a modellre (N243 (3), HN-17, N-F239b)

*Végrehajtó: `claude-opus-5-5` (kért: `opus`, egyezik) · 2026-11-23/24. A döntésfájlba beírva: D9 (2026-11-23, a GK-27 tárgya), D10–D12 (az integrátor éjjeli üzenete szerint, szó szerint).*

**Felmérés (a munka előtt).** Az ISTENTISZT-001 és a HAMART-001 lapját az új generátor repón kívülre generálta; rajtuk és a 9 commitolt lapon a mai kapuk:
- Az `ellenoriz.py`, az E38 (`allitas_adat.py --minden --szigoru`) és az E39 (`kovetelmeny_kapu.py HAMART-001 --szigoru`) az új lapokon (ideiglenesen a `lexikon/` helyén, commit nélkül, utána visszaállítva) összeomlás nélkül fut; szakaszszámra kötött szabályt bennük nem találtam (a 28. a `GENERÁLT` jelölőkön, a 35. a szám nélküli Kolofon/Jelmagyarázat címen, a 25. a `proza_1a`-n át mér). A többlet-SÉRTÉS (11., 32., 40.) tartalmi lelet, nem kapuhiba (l. lent).
- **Vak pontok az `olvasoi_kapu.py`-ban** (a szakaszt a számozott címből azonosította): az idézet-ellenőrzés (IDEZET) csak az „1/a” alcímet ismerte — az új szerkezetű lapon (a commitolt HAMART-001-en is) 0 blokkot látott (most 49, illetve 20); az LXX-összesítés csak a „3. LXX”-et (**HN-17**; az új lapon 5.) — `None` volt; a szint-összevetés (SZINT_ALATT) az arany lappal a teljes címen kulcsolt, ezért a két szakaszrend közt nem illeszkedett; az Irodalom-kivételek a „8. Irodalom”/„12. Irodalom” literálon álltak. A `proza_1a.py` a „#### 2.1.” számot égette be.

**Megvalósítás (technikai döntések, DT920).**
- Új modul: `eszkozok/lapgen/lapszakasz.py` — a címsor szakaszazonosítója a lapmodell szerint: az azonosító a szakaszrendé (`szakaszok.py`), a cím a B66 `cim.<azonosító>` sora (alrész: `cim.elofordulasok.szoveg`); a régi generátor lapjainak csak ott létező szakasza (6/b. Alkalmazás) a `REGI_CIMEK` táblában. A szám és a „*(kézi)*” jelölés nem része a kulcsnak. Mind a 9 commitolt és a 2 új lap minden `##` címe és az igehely-szöveg alcíme azonosítóra képződik.
- `olvasoi_kapu.py`: a `Sor` az `az`/`alaz` mezőt kapja (a `tagol` tölti); minden szakaszfüggő ellenőrzés az azonosítón dönt (IDEZET, KIVONAT_SZAM LXX-része, ZAROJEL, FUNKCIO_URES, KOLOFON, MEGHATAROZAS, a kizárt szakaszok, az Irodalom-kivételek, SZINT_ALATT, MINTA). A régi lapon a régi mérce megmarad (az Irodalom ANGOL- és DOI-kivétele továbbra is csak a régi, illetve csak az új szerkezeten él, mint eddig). `proza_1a.py`: az igehely-szöveg címét az azonosító adja.
- **N-F239b:** a 12. Irodalom felsoroláselemében az `adat/vitatott_forrasok.tsv` műcíme (`*cím*`) és megjelenési adata bibliográfiai adat, nem olvasói szöveg (a forrás-tábla szerint, nem általános kivétel): az ANGOL, az ANGOL_SOR és a MUNKASZO nem méri; ugyanaz a szó a címen kívül, vagy a táblában nem szereplő címben továbbra is BUKÁS.

**Regresszió** (a 9 commitolt lap + a 2 új lap, a módosítás előtt és után, minden találat és a `proza_1a` blokkjai): egyetlen eltérés, a várt: a HAMART-001 Carr-műcímének ANGOL_SOR-figyelmeztetése eltűnt (mindkét lapváltozaton). A most aktív ellenőrzések (IDEZET 49/20 blokk, LXX-összesítés, SZINT kulcsai) az új lapokon új találatot nem adnak.

**Teszt.** `teszt_olvasoi_kapu.py` `ModellSzakasz` (4): azonosító régi és új címre; HN-17 (az 5. LXX összesítése mér, KIVONAT_SZAM jelez); IDEZET a „2.1.” blokkon (jó: 0, rossz: BUKÁS); N-F239b (táblabeli cím: 0 ANGOL/MUNKASZO; címen kívül és ismeretlen címben BUKÁS). A fogyasztók tesztjei: l. a commit üzenetét.

**A brief határán belül javítva (az F241.1 hibája, külön commit `57ba097f`).** A `lapgen/tesztek/teszt_szerkezet.py` három bukása (GK-01: `'lexikon/'` literál; GK-08a: szöveg-összefűzés és a Kolofon-modell bemeneti típusú mezője) az F241.1 óta: a `Frissesseg`/`Jovahagyas` a `lapgen/ertekek.py`-ba költözött (a bemenet re-exportálja), a kapu üzenete a `_KAPU_OK` táblából. `futtat.py szerkezet kolofon`: 34/34.

**Tartalmi leletek az új generátoros lapokon (nem a kapu hibája; az F241.5b/F241.7 bemenete).** ISTENTISZT-001 (új): 103 BUKÁS — MINTA 91 (a „jelölt” és a „fölérendelt fogalom” szakszó a kizárt helyek indoklásában; a forrásuk a `jeloltek.tsv` kézi indoklása, a régi generátor regex-cserével elfedte), LISTA_NEVELO 9, KONYV 2 („Zef”), MUNKASZO 1 („Lap teljesség-mérése” az Irodalom adatforrás-listájában); HAMART-001 (új): 2 BUKÁS (MUNKASZO 1, ugyanaz; LISTA_NEVELO 1: a Kolofon „a lap elején áll” értéke, `kolofon.ertek.kriterium` sablonsor). Az `ellenoriz.py` 11. szabálya a HAMART-001 új lapján: a `minosites` és az `alatamasztas` rés eltér a tábla + tanulmány szerint elvárttól. Ezeket az F241.5b (sablon/névtábla, D11–D12) és az F241.7 (3/b) méri újra; a kapuk most már mindkét szakaszrenden mérnek.

**Lapgen-futás:** kettő (az ISTENTISZT-001 és a HAMART-001 repón kívüli generálása a felméréshez, egy folyamatban, egymás után), előtte a `python.exe`-lista: 6 kis folyamat (14–26 MB), lapgen-méretű nem.

*Proveniencia: `scope=lapgen.fo.lap_keszit (ISTENTISZT-001, HAMART-001, munka mód) + olvasoi_kapu.lap_meres + proza_1a.blokkok a 9 commitolt és a 2 új lapon, előtte/utána; ellenoriz.py; kovetelmeny_kapu.py HAMART-001 --szigoru; allitas_adat.py --minden --szigoru; futtat.py szerkezet kolofon | forras=a munkafa | ts=2026-11-24`.*

**A fogyasztók tesztjei** (a commit előtt): `teszt_olvasoi_kapu.py` 80/80 (az új `ModellSzakasz` segédje eleinte egy meglévő `uj_lap` nevű függvényt fedett el: átnevezve `modell_lap`-ra); `teszt_f194_szopar.py` 19/19; `teszt_kesz_lap_hamart.py` 66/66; `teszt_gyokerok_kapuk.py` 27/27; `teszt_ellenoriz_32.py` 8/8; `teszt_f212_cs3.py` 24/24; `ellenorzes/tesztek/test_szabalyok.py` 282, 26 hiba — mind az E27-teszteké, környezeti (`ValueError: path is on mount 'E:', start on mount 'C:'`: a teszt ideiglenes könyvtára más meghajtón van, mint ez a worktree; a CI-ben nem áll elő). `teszt_muhely_allapot.py` 35-ből 1 bukás: `test_hamart_a_valos_adaton_hatardontessel_lezart` (a HAMART-001 határ-frissessége „elavult”, a teszt „friss”-t vár) — **nem ettől az ágtól**: az `ellenoriz.hatar_frissesseg` és a bemenetei (`adat/jeloltek.tsv`, `naplok/HATAR_HAMART-001.md`) azonosak az `origin/main`-nel; **nem javítottam** (a motívum határát érinti: a szerkesztőé), az integrátornak jelezve.

## F241.4 — Licenckapu (N223; D13, D14)

*2026-11-24 · `claude-opus-5-5` (kért: `opus`, egyezik) · a D13 (az F241.3 leletei az F241.5b bemenete) és a D14 (a halmaz és a kapu formája) a döntésfájlban.*

**Mérés (⛔ előtt).** Az új generátor `lap_keszit`-je munka módban, a Kolofon bemenetén (a számozott szakaszok valódi olvasásai, GK-07), a származtatott táblák bemenetei (F212) és a külső források. A lapra adatot adó, nem üres `kotelezo_megjeloles`-ű, a régi halmazon kívüli források: TAGNT, Karoli_Strong_parok, TAGNT_valtozatok, SDBH/SDGNT (a mondatuk már a lapon állt); TBESH/TBESG, LXX_OS, Strong_szotar, SBLGNT_apparatus, Macula_heber, Karoli_KH_javitott (mindkét lapon, új mondattal); Tanu_rabbinikus_index (Sefaria) és Chain_Lineage_Browser (csak a HAMART-001-en). A TEREMT-001 ezen az ágon nem generálódik (a B47 forrása a #820 ágán van), ezért nem mértem. A lista az integrátornak ment; a döntés: D14.

**Kapu** (`lapgen/szamitas/kolofon.py`: `licenc_meres`, `licenc_hianyok`, a `kapu` első lépése, minden módban; a modell `licenc_hiany` mezője). (1) Mondatszint: a lap adatát adó minden forrás (a számozott szakaszok forráslistára kerülő bemenetei, a több forrású bemenet társai — `konfig.LICENC_TARS`: B10 → TBESG, B31 → SDGNT —, a származtatott táblák bemenetei és a külső források) nem üres megjelölésének minden mondata a Kolofonban áll, idézetként vagy a forrás saját mondatával (LSJ, OSHL/TWOT, tW). (2) Név: minden ilyen forrást a forrástábla megnevez; a tisztázatlan licencűt (ma a Chain Lineage) a licencállapot mondatával (GK-28); a tisztázatlan licencű forrás mezője leírás, ezért a mondat-kapu nem méri (D14 (c)). A GK-28 eddig csak a forrástábla licencalakját adta, a lap szintjén nem mérte; ez most a kapu része.

**A halmaz** (`konfig.KOLOFON_MEGJELOLES`, D14 (b)): + TBESH, TBESG, Strong_szotar, LXX_OS, SBLGNT_apparatus, Macula_heber, Karoli_KH_javitott, Tanu_rabbinikus_index. A megjelölés a lap adatát adó források szerint áll (eddig: csak a jegyzék `licenc_kulcs`-a szerint, a külső és a társ-forrás kimaradt).

**Technikai döntés: a mondathatár.** A `kotelezo_megjeloles` mező mondatokra bontása a „.; ” mellett a „); ” határon is (`bemenet/alap.py`): a TBESH/TBESG mezője „… (CC BY 4.0); Refer others …” alakú, így a STEPBible-mondat a TAHOT-éval azonos, és a lapon egyszer áll. A „); ” más mezőben csak a lapra nem kerülő Versifikacios_tablak és simplemma soron fordul elő.

**Adat** (D14 (d)): az `adat/licencek.tsv` Karoli_KH_javitott sorának `kotelezo_megjeloles` mezőjéből a „— udvariassági forrásmegjelölés” megjegyzés a `megjegyzes` oszlopba került (split/join, egy sor, a többi bájtra azonos). A mérce B01 hash-sora (`naplok/F218_referencia.tsv`) külön commitban frissült (a brief 8.1 pontja).

**Hatás a lapokon:** a Kolofon generált blokkjában 9 új megjelölés-mondat (a HAMART-001-en; az ISTENTISZT-001-en 8, a Sefaria nélkül); a DT933 (1) szerint változásjegyzék-sor, új nézés nem. A regresszió (HAMART-001, `--teljes`): 9 látható és 9 üres új sor engedélysorral (`S8D-LICENC-1…9`, `S8D-LICENC-URES`); utána RENDBEN, engedély nélküli diff-sor 0; `hash_or_kapu`: RENDBEN, 210 sor.

**Teszt** (`teszt_kolofon.py`, `Licenckapu` + `Istentiszt.test_n223_licenckapu`): a mérce független számlálással a táblákból; a lap minden kötelező mondatot hordoz, a kapu átmegy; hiányzó idézet → a forrást nevezi, a kapu megáll, a sablonos LSJ nem hiány; a forrástábla nélküli forrás és a licencállapot-mondat nélküli tisztázatlan forrás hiány; a mondathatár. A régi `Megjeloles` teszt a külső és a társ-forrásokra bővült. `futtat.py kolofon szerkezet`: 40/40; `futtat.py szerkezet kapuk bemenet szoveg`: 71, a szerkezet két bukását (GK-08a: szabad `str` mező a modellben, `.join` a számításban) a kapu átszervezése javította. A teljes `futtat.py` a 30 perces időkorlátba ütközött (a részhalmazok zöldek).

**Lapgen-futás:** a mérés két generálása, a tesztek és egy HAMART-001 repón kívüli generálás a regresszióhoz; egy alkalommal egy másik session push előtti lapgen-futását (`general.py --cel lexikon --id HAMART-001`) megvártam.

*Proveniencia: `scope=lapgen.fo.lap_keszit (ISTENTISZT-001, HAMART-001, munka mód) a Kolofon bemenetén; futtat.py kolofon szerkezet kapuk bemenet szoveg; PARDES_DATUM=2026-11-13 general.py --cel lexikon2 --id HAMART-001; regresszio.py --id HAMART-001 --teljes; hash_or_kapu.py | forras=a munkafa a commit előtt | ts=2026-11-24`.*

## F241.5 — Az ISTENTISZT-001 hiányzó fordításai (N244)

*2026-11-24 · `claude-opus-5-5` (kért: `opus`, egyezik).*

**Mérés.** Az új generátoros ISTENTISZT-001 lapon 34 „fordításra vár” jel (a 35. találat a 2. szakasz magyarázó mondata, nem jel): a 4.3 (Teológiai szócikk) 12 tW-címe és a 4.4 (Szemantikai domén) 22 doménneve a G1941, a H7121 és a H8034 szónál. A kulcsok a generátor saját bemenetéből (`b29_tw`, `b31_domenek`; a tW-cím kulcsa a cikk első Strongja + `tw_id`, a doméné a szó Strongja + `domen_kod`): 32 egyedi sor (a `kt/call-speakloudly` és az `other/renown` cím két szónál is áll), egyik sem volt a táblában. Azonos forrásszövegű (`forras_hash`) meglévő fordítás egy volt: „Names of People” → „Személynevek” (SDBH, más Strongnál); átvéve.

**Fordítás** (`adat/forditasok.tsv`, 32 új sor, csak hozzáfűzés: `allapot=opus`, `modell=claude-opus-5-5`, `datum=2026.11.24`, `terminologia_verzio=v5`, a `megjegyzes`-ben a forrásszöveg; `forras_hash` = a forrásszöveg SHA-1-e). A meglévő tW-cím- és doménfordítások formája szerint: a tW-cím kisbetűs szólista, a doménnév nagybetűs főnév vagy melléknév. Nyelvközi egység: a görög (SDGNT 033009) és a héber (SDBH 002004002010) „Name” egyaránt „Név”; a „proclaim” a declare- és a preach-címben egyaránt „hirdet”; a „renown” és a „reputation” „hírnév”; a „call”/„cry out” „hív”/„kiált”. A terminológiatáblában (v1–v5) ezekre nincs kötött szó. Meglévő, kiadott fordítást nem írtam át (a brief ⛔ feltétele nem állt elő).

**Ellenőrzés.** Az ISTENTISZT-001 új generátoros lapja: 0 „fordításra vár” jel, 0 elavult jel. `ellenoriz.py`: 13. szabály JELENTÉS (a 158 elavult sor és a Thayer-szakaszok, mind a meglévő állapot), SÉRTÉS 0. A mérce B14 hash-sora (`naplok/F218_referencia.tsv`) külön commitban; utána a HAMART-001 regressziója (`--teljes`): RENDBEN, engedély nélküli diff-sor 0 (a HAMART-001 lapja nem használja az új sorokat).

**Hatás:** az ISTENTISZT-001 4.3 és 4.4 pontja (generált blokk) magyarul; a D9 szerint változásjegyzék-sor, új nézés nem.

*Proveniencia: `scope=general.py --cel lexikon2 --id ISTENTISZT-001 (előtte/utána); lapgen.bemenet.szotari b29_tw, b31_domenek; ellenoriz.py; PARDES_DATUM=2026-11-13 general.py --cel lexikon2 --id HAMART-001; regresszio.py --id HAMART-001 --teljes | forras=a munkafa a commit előtt | ts=2026-11-24`.*

## F241.5b — 1. menet: a 91 MINTA-hely mérése, KONYV, a HAMART-001 mérése, a D11-kapuk munkalistája

*2026-11-24 · `claude-opus-5-5` (kért: `opus`, egyezik) · alap: `6bdff88e`.*

**A 91 MINTA-hely forrása (D13 (c), ⛔ az integrátorhoz, válaszra vár).** Öt forrás: 87 hely a `jeloltek.tsv` `indoklas` mezője a 3. szakasz (43) és a 6. szakasz Minősítés-táblája (44) Indok oszlopában — mögöttük 10 egyedi szöveg („… került a jelöltek közé” 37 sorban, „… a fölérendelt fogalomhoz tartozik” 6 sorban); 2 hely az `elutasitasi_okok.tsv` `megjegyzes` mezője (1. Döntési út); 1 hely BDB-szöveg (4.2, a kiesett nem héber írású szó utáni „,;”); 1 hely a `kiadasok.tsv` leírása („jelölt alakban” = megjelölve). Mellék-lelet: a 61 kereszthivatkozásos sor a 3. és a 6. szakaszban is teljes táblában áll. A javaslat (külön olvasói-indoklás tábla hash-kulccsal; a kettőzés megszüntetése; helyben javítás a B56-ban és a kiadástörténetben) és a mérés: `side-session-notes/local_5140778b…/F241.5b_MINTA91_meres.md`.

**KONYV (kész, `51bd1fa1`).** A „Zef 3:9” a döntésnapló `forras_kereses` mezőjéből jön (a Károli-KH forrásverse); a lapgen eddig „úgy, ahogy az adatban” tette ki (N195). Javítás: a normalizáló tábla meglévő `Forrás-alakok` oszlopa (a Sof sorban `Zef`), a B63-modul olvassa, a `kereszthiv._igehely` a tábla rövidítésére cserél, ismeretlen könyvnév BemenetHiba (a kódban alias nincs, GK-17). A tábla hash-ét rögzítő `adat/thayer_vers_jelentes.tsv` újragenerálva (`vers_jelentes.py --ts 2026-11-11`): csak a fejléc változott. A mérce B63/B21 hash-sora: `e7d93251`. Az ISTENTISZT-001 lapján előtte/utána: a KONYV-találat 2 → 0, a diff a 4 „Sof 3:9” sor és a blokkok `ts=b:` hash-e.

**LISTA_NEVELO, MUNKASZO (mérve, a javítás új szöveget kér: ⛔ az integrátorhoz).** A 9 ISTENTISZT-hely: 6 a 2.1 tábla Kulcsszó oszlopa (Károli-szavak, a jóváhagyott régi lapon is így), 3 a Funkció cella (B03/B46 `funkcio`, kézi kifejezés); a 10. és a HAMART-001 egyetlen LISTA_NEVELO-ja: B66 `kolofon.ertek.kriterium` („a lap elején áll”). A MUNKASZO mindkét lapon: B65 `irod_adat` „Lap teljesség-mérése” (B05/B06).

**A HAMART-001 és az `ellenoriz` 11. szabálya (D13 (e)).** A HAMART-001 új lapja: BUKÁS 2 (a fenti MUNKASZO és LISTA_NEVELO). A 11. szabály a lapon álló `minosites`/`alatamasztas` rést a régi generátor (`lexikon_general.res_torzs`) szövegével veti össze: a 99 vizsgált hely mindkét változatban azonos, soronként azonos tartalommal; az eltérés megfogalmazás, forráslista és a proveniencia-sor olvasói alakja. Tartalmi veszteség nincs. A szabály a régi generátor fogyasztója: az új generátor lapján (F241.7-től a `lexikon/`-ban) minden résen SÉRTÉST adna. **Gazdája: az F241.7 első lépése** (átkötés: az új generátoron a rés-forrás egyezést a GK-07, a GK-27 és a `regresszio.py` méri). A HAMART-001 regressziója (`--teljes`) a KONYV-javítás után: RENDBEN, engedély nélküli diff-sor 0.

**A D11 (1) kapuinak munkalistája** (`side-session-notes/local_5140778b…/F241.5b_szokincs_munkalista.tsv`): a próbalista (a MINTA- és a MUNKASZO-kapu mintái + a forrásmérés belső szavai) a B66-ban 99, a B65-ben 16 sort talál (160 találat; „lánc” 86, „szónézet” 16); a névtábla-identitás 77 sor (45 `ok_cella`-másolat). A kapuk a javítással együtt kerülnek be (különben a teszt bukik); a szakszavak olvasói megfelelője ⛔ az integrátornál.

**A brief határán túl javítva:** `konkordancia/Konyv_normalizalo_tabla.tsv` (egy cella, a Sof sor `Forrás-alakok` mezője; gépies, a tábla meglévő oszlopa) és a mérce `naplok/F218_referencia.tsv` hash-sorai.

**Lapgen-futás:** három, egymás után (ISTENTISZT-001 előtte, HAMART-001, ISTENTISZT-001 utána), előtte a `python.exe`-lista (3 folyamat, a legnagyobb 296 MB, lapgen-méretű nem). Tesztek: `futtat.py kereszthiv` 18/18.

*Proveniencia: `scope=general.py --cel lexikon2 --id ISTENTISZT-001 / HAMART-001 (repón kívül) → olvasoi_kapu.lap_meres; ellenoriz.res_elvart_es_tenyleges (HAMART-001 minosites, alatamasztas); a B65/B66 minden során a próbalista; regresszio.py --id HAMART-001 --teljes | forras=a munkafa (6bdff88e → e7d93251) | ts=2026-11-24`.*

## F241.5b — 2. menet, (1): a 91 MINTA-hely a D15 szerint

*2026-11-24 · `claude-opus-5-5` (kért: `opus`, egyezik) · alap: `99ff3d6a`.*

**Eredmény.** Az ISTENTISZT-001 új lapján a MINTA 91 → 1; a maradék a BDB „arab,;” (l. lent). A HAMART-001 regressziója `--teljes`, hash-őrrel: RENDBEN (0 engedély nélküli sor).

**(1) Olvasói-indoklás tábla (B76, `adat/olvasoi_indoklasok.tsv`, SEMA 2.74).** 10 sor (az ISTENTISZT-001 10 egyedi indoklása), kulcs: a lapra kerülő indoklás-szöveg SHA-1-e (12 jegy). A mondatok a D15 (1) szerint, minimális cserével: a „A hely kereszthivatkozás nyomán került a jelöltek közé.” zárómondat elmarad (37 sor; a „Nincs meg a formula a versben: …” rész marad); „a fölérendelt fogalomhoz tartozik” → „a tágabb körbe tartozik” (7 szöveg); „az invokáló szerkezet” → „a segítségül hívó szerkezet” (Zsolt 99:6); a „Jogi fellebbezés:” címke elmarad (ApCsel 25–28, 6 sor). A `jeloltek.tsv` érintetlen. A lapgen (`bemenet/olvasoi_indok.py`) a 3. (`vizsgalt.py`) és a 6. szakasz (`kereszthiv.py`) Indok cellájában az olvasói alakot teszi ki (Kezi, B76 `olvasoi_indoklas`); a cellakezdő ok elhagyását (`ok_ismetles`) a lapra kerülő szövegen méri.
- **Kapuk (betöltéskor, a D17 szerint):** szókincs-kapu az olvasói alakon (`lapgen/szokincs.py`): a szűkített tiltólista (`SZAKSZO`: gerinc, token, proveniencia, kutatói hozzárendelés, „Szövegigazolás nélkül”, jelölt) és a névazonosság (`MASODIK_NEV`: egy fogalom második neve hiba — „fölérendelt fogalom” a lapon bevezetett „tágabb kör” helyett, „invokáló szerkezet” a „segítségül hívó szerkezet” helyett); a „tágabb kör” név a sablontábla `fej.tagabb` sorából jön, más „tágabb …” alak hiba; árva hash (a motívum egyik élő indoklására sem mutat) hiba. A D15 cseréinek indoka így a névazonosság (D17 (2)).
- **Technikai döntés (a D15 „ha … nincs olvasói alakja, a generálás megáll” olvasata):** olvasói alak nélkül az indoklás akkor áll a lapon, ha átmegy a szókincs-kapun; ha nem, a generálás megáll az (azonosító, igehely, hash) megnevezésével. Indok: a tiszta indoklás olvasói alakja betűre ugyanaz volna (a HAMART-001-nél több száz sor), a kapu ugyanazt méri. Ha az integrátor minden lapra kerülő indoklásra kézi sort kér, a `lapra` egy sora változik.
- **Egy szólista:** az `olvasoi_kapu.MINTA_SZAKSZO` a `lapgen.szokincs.SZAKSZO` (teszt őrzi); a lap minta-ellenőrzése a második nevet „egy fogalom második neve” üzenettel jelzi (a régi f194-minta így is hibát ad). A szűkítés után az ISTENTISZT-001 MINTA-értéke 1, a HAMART-001-é 0 (újramérve).
- **Jóváhagyás tárgya:** a B76 a `konfig.JOVAHAGYAS_BEMENETEK`-ben (motívumra kulcsolt kézi adat). A lenyomat táblánál ezentúl csak akkor veszi a fejlécet, ha a motívumnak van sora (`jovahagyas._motivum_resz`): így az új tábla nem avultatja el a sor nélküli HAMART-001 jóváhagyását. Az ISTENTISZT-001 lenyomata változik (B76, B56) — az F241.7 nézése ezt fedi.

**(2) A kettőzött tábla egyszer (D15 (2)).** A 3. szakasz TSK- és Károli-csoporttáblája helyett egy mondat: „A kereszthivatkozásból vizsgált 61 sor (TSK-ajánlás 19 és Károli-kereszthivatkozás 42) a [6. Kereszthivatkozások](#6-kereszthivatkozások) szakaszban, a Minősítés táblájában áll.” (új sablonsor `k3.kh_masutt`, `dontes=var`: a ⛔ (4) csomagjában megy az integrátorhoz). A csoportok számai („A jelölés forrása” sor, a szakasz kapuja) változatlanok; a jegyzetek belső sorszáma és a közös forrásmegjelölés csak a kiírt sorokból számol. **A HAMART-001 arany lapjához mérve:** a szakaszrend azonos (a 3. és a 6. szakasz mindkét lapon áll, a régi arany lapon is kettőzve: 99 sor) — a javítás a HAMART-001 új lapját is érinti (a 3. szakaszból 99 sor kiesik, egy mondat belép): lapszerkezet-változás, az **F241.10 változáslistájába** kerül. Teszt: a 3. szakasz kereszthivatkozásos sorai pontosan a 6. szakasz elutasított és nyitott sorai (mindkét mintalapon), és a 3. szakaszban nincs csoporttábla, a hivatkozó mondat egyszer áll.

**(3) Helyben (D15 (3), (5)).** `elutasitasi_okok.tsv`: „(a fölérendelt fogalom felé)” → „(a tágabb kör felé)”, „nem az invokáló szerkezetben áll” → „nem a segítségül hívó szerkezetben áll”; a B56 `cimke`/`megjegyzes` minden sora a szókincs-kapu alatt (betöltéskor). `kiadasok.tsv` (ISTENTISZT-001, 1. kiadás): „jelölt alakban áll” → „megjelölve áll”. Mindkettő split/join, az eredetivel összevetve.

**(4) BDB „arab,;” — nem javítottam, gazdát kér.** A forrás a fordított BDB-szöveg (`adat/forditasok.tsv`, `adat/bdb_szakasz_hu.tsv`): a fordításból a nem héber írású (etióp, arab) szó kiesett, az írásjel maradt. Ezt a két fájlt most a #821 (F240, `lxx-bdb-adatjavitas`) ága írja; két ág nem írhat egy fájlba. Javaslat: a #821 merge-e után a 218c javítja (a `bdb_jelolt/forras_javit.py` szabályával), vagy a #821 kapja. A `forditasok.tsv`-ben 117 „,; ” jel áll, ebből a kiesett szó utáni árva jel külön mérendő.

**Változáslista az F241.7-hez (ISTENTISZT-001):** a 10 olvasói indoklás; a 3. szakasz hivatkozó mondata a 61 soros tábla helyett; a B56 két megjegyzése; a Kolofon kiadástörténetének „megjelölve” szava. **Az F241.10-hez (HAMART-001):** a 3. szakasz hivatkozó mondata a 99 soros tábla helyett.

**Mérce:** `naplok/F218_referencia.tsv` (B56, B48 `kiadasok.tsv`, B66, B68 hash-sora; új B76 sor) és `naplok/F218_elteres_engedely.tsv` (S9A-D15-T001…T089, S9A-D15-MONDAT, S9A-D15-J01…J09; a S9A-FORRAS, S5-FORRAS, S5-RES-FORRAS, S5-PROV új hash-e; az ISM3-URES-REGI 1 → 2; a S9A-KIEJTES törölve: a sora a kiesett táblában állt).

**Lapgen-futás:** három, egymás után (ISTENTISZT-001 előtte és utána, HAMART-001), előtte a `python.exe`-lista (két másik session BDB-szkriptje, lapgen-méretű nem).

*Proveniencia: `scope=general.py --cel lexikon2 --id ISTENTISZT-001 / HAMART-001 (repón kívül) → olvasoi_kapu.lap_meres; regresszio.py --id HAMART-001 --teljes | forras=a munkafa (99ff3d6a + a menet változásai) | ts=2026-11-24`.*
