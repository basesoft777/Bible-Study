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
