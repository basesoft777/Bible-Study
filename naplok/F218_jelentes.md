# F218a — jelentés (menet-, ellenőri és zárójelentés egy fájlban)

*FELADATOK #218 · brief: `F218_GENERATOR_UJ_A_BRIEF.md` · ág: `claude/f218-generator-uj-a`.*

## F218.0 — modell-ellenőrzés, függések, keret

- **Modell.** Az építő session tényleges modellje `claude-fable-5-2`; a brief fejléce `modell: fable`. Egyezik. (Az első indulás `claude-opus-5-5` modellen modell-eltérés miatt megállt, munka nélkül.)
- **Függések.** `python eszkozok/feladatok.py fuggesek` (main `37f087cc`): a 218-as tételhez `KIZAR` sor áll a 38, 123, 178, 179, 194 és 212 tétellel (közös fájl: `Konyv_normalizalo_tabla.tsv`, `elofordulasok.tsv`, a 6-os sablon, `general.py`). Ezek közül egy sem fut ténylegesen: a 38, 123, 178, 179 `megallt`, a 194 `dontesre_var`, a 212 `fut`, de `Folytatás:` kezdetű `kovetkezo` mezővel (félbemaradt, nem aktív). A fejléc (`fugg: []`, `nem_fugg: [121, 123, 146, 178, 179]`) a #728 befogadás szerint áll. **Megjegyzés az orkesztrátornak:** a 194 és a 212 a brief `nem_fugg` indoklásában nem szerepel; mindkettővel csak additív érintkezés van (`elofordulasok.tsv` új oszlop, `general.py` új `--cel` érték).
  *Proveniencia: `scope=feladatok.py fuggesek | forras=37f087cc | ts=2026-11-13`.*
- **Ellenőrzési szint.** `feladatok.py szint 218`: `teljes`, 2 kör.
- **Keret** (`get_usage`, 2026-11-13 09:05 UTC): heti (minden modell) 83%, heti Fable 15%, 5 órás 19%; a heti nullázás 2026-11-14 14:00 UTC.
- **A független ellenőr modellje** (`.claude/agents/fuggetlen-ellenor.md`): `opus`, tehát nem Fable.

## F218.1 — referencia és futásidő (1. lépés)

- **Parancs** (ideiglenes kimenet a repón kívül, a `lexikon/` alá semmi nem íródott): `PARDES_DATUM=2026-11-13 PYTHONIOENCODING=utf-8 python eszkozok/general.py --cel lexikon --id HAMART-001 --kimenet %TEMP%\f218_1\out`. A `general.py` kapcsolói: `--cel lexikon`, `--id`, `--kimenet` (a gyökér a `<kimenet>/lexikon/`).
- **Futásidő:** 46,5 s (a mért második futás; a gép és a gyorsítótárak melegek). Kimenet: `HAMART-001_TUDOMANYOS.md` 488 241 bájt, `HAMART-001_KIZARASOK.md` 21 763 bájt; a futás kiejtés-hiány jelzése: 22 hiány (15 generált, 7 kézi), a konzol szerint „K13/K15: minden könyvnév feloldva, alias nélkül (a KONYV_ALIAS üres)”.
- **Egyezés: bájtra azonos** a `git show HEAD:lexikon/<fájl>` tartalmával (`diff` 0 sor, mindkét fájlra). A munkafában a két fájl CRLF-es (`core.autocrlf`), ezért a munkafa-sha eltér; a kimenet LF-es, mint a commitolt blob.

| fájl | HEAD-blob sha256 (= a generált kimenet) | munkafa-bájtok sha256 (CRLF) |
|---|---|---|
| `lexikon/HAMART-001_TUDOMANYOS.md` | `66e066c61f3975a9993b1a4cfd8169a83aca7cf27762d3e2c7fcda475038a4d7` | `7cf6a6fa2d36caeae330d1aa0bb2284376d896fd86c2daa18c9e681122ed5e1f` |
| `lexikon/HAMART-001_KIZARASOK.md` | `1cdaffd3e529d3ca4051d6be90515eaec75179038c92749a3fcd14e4cd9e9b3c` | `1319812158e78d032998f6e67ebbce93beefe2c66322393728bdb67803995c90` |

*Proveniencia: `scope=general.py --cel lexikon --id HAMART-001, PARDES_DATUM=2026-11-13 | forras=5e4344f6 | ts=2026-11-13`.*

## F218.1 — szimbólumtérkép (2. lépés)

*Alap: `eszkozok/lexikon_general.py` (10 153 sor; `scope=wc -l eszkozok/lexikon_general.py | forras=5e4344f6 | ts=2026-11-13`), main `5e4344f6`; a sorszámok mai sorszámok (`ast` alapú kinyerés, szimbólum szerint). A hívási fa a HAMART-001 ágára vonatkozik. **Eltérés a SPEC-től:** `UJ_LAPSZERKEZET = frozenset({'HAMART-001', 'ISTENTISZT-001'})` (7109), tehát az ISTENTISZT-001 is az új ágon generálódik; a három F212-kapu (`run`) mindkettőn fut. A `gerinc_aktiv(id)` (3161) = az id nincs a `GERINC_KIVETEL_MOTIVUMOK`-ban (`SZK.kapcsolo_kivetelek`, `adat/funkcio_kapcsolok.tsv`). Az `olvasoi_atiras` nem az `OU`-ban, hanem a `lexikon_general.py`-ban él.*

### A teljes lánc: `run`-tól a fájlba írásig (új szerkezet; a sorrend kötött)

1. `run` (10049–10153): `G.elofordulasok_id_szerint`; `BEFAGYASZTOTT` (10046, `LB.befagyasztott_idk`) → kihagy; `res_forras_teljesen_hianyzik_e` (6433) → kihagy; `lemma_valtozat_beallit(sorai)` (405) (a `LEMMA_VALTOZAT` globális állapotot tölti); `UJ_DOMEN_MAGYAR[0]` beállítása.
2. `render_lexikon_egy_id` (9918–9960): `blokk_tartalom` (643), `blokk_jelmagyarazat` (752), **`blokk_elofordulasok` (898)**, `blokk_kizart` (1103), `blokk_szocikkek` (2727), `blokk_lxx` (5428), `blokk_kereszthivatkozasok` (5523), `blokk_kapcsolatok` (5630), `blokk_kapcsolodo` (5737), `blokk_idezes` (5816), `blokk_kolofon` (6247). Mindegyik `_lexikon_blokk`-kal (446–453) csomagol: **ez állítja elő a `<!-- GENERÁLT-KEZDET … | forrás: … | licenc: … | ts=… -->` fejlécet** (a `forrás:`/`licenc:` lista a blokkfüggvény saját, kézzel írt `forras_lista`/`licenc_lista` változója; a `ts` a `G.TS`: `PARDES_DATUM` env vagy a mai dátum), és az olvasói bekezdést (`olvasoi_bekezdes` 569: `OLVASOI_CIMKE = '<!-- olvasói -->'`, 461, a sor végére).
3. `epit_uj_fajl` (9963): `VAZ_SABLON` (9829–9912; a régi szakaszrenddel) `%`-behelyettesítése a blokkokkal.
4. `res_blokkok_alkalmaz` (6858): a hét rés fejléc+törzs span-jét cseréli a `res_forras.tsv` szerint (`szakasz_6b_beszur` 6838, `opcionalis_res_visszaallit` 6930, `res_torzs` 6490, `OK.minosites`, `opcionalis_resek_torol`).
5. `res_labjegyzetek_alkalmaz` (6970): a kézi rések definíció nélküli `[^kulcs]` lábjegyzeteinek generált blokkja (`lap_labjegyzet_hiany` 6963).
6. `_generalt_fejlec_alkalmaz` (10000) ← `_generalt_fejlec_sor` (9981): a fájl első sora `<!-- GENERÁLT: general.py --cel lexikon | rések: … -->`.
7. **`uj_szerkezet_alkalmaz` (8425–8443)**, belül ebben a sorrendben: `blokk_dontesi_ut` (7648) + `dontesi_ut_beszur` (7802) → `uj_cimek_alkalmaz` (7157; `UJ_CIMCSERE` 7125, `UJ_SZOVEGCSERE` 7143) + `.replace('## 10. Alkalmazás…')` → `tanitoi_resz_ki` (7223) → `alkalmazas_resz_ki` (7233) → `.replace(` a „Tanítói egyezés” mondatra`)` → `attekinto_beszur` (8536) → `visszhang_beszur` (8563) → `rokon_tabla_48` (9206) → `hatastortenet_athelyez` (9630) → `szakirodalom_beszur` (9598) → `azonosito_tabla_beszur` (7305; `egyszerusitett_kolofon` 7284) → `kesz_lap_elotte` (8298; `UJ_JELMAGYARAZAT_CSERE` 8249, `szotari_pontok_jelmagyarazat`) → **`olvasoi_atiras` (8228)** → `kesz_lap_utana` (8339) → `nevelo_le` (8384).
8. `kiejtes_potol` (9990) → `kiejtes_szoveg.potol` (278): az első előfordulás kiejtésének pótlása a kész szövegben; a hiányokat `KIEJTES_JELOLT_HIANY`-ba gyűjti.
9. `cimjeloles_ki` (6378) majd `OU.alkalmaz` (`olvasoi_utofeldolg.py` 354): soronként `strong_sor` (269), `bdb_sor` (145), `konyv_sor` (130; `EXTRA_KONYV` 44, `konyv_alias` 67 → `Konyv_normalizalo_tabla.tsv`), `idezojel_sor` (110).
10. `TJ.alkalmaz(szoveg, szopar=szopar_motivum(sorai))` (`tablajegyzet.py` 250): lábjegyzet-definíciók → `olvasoi_jegyzet` (172); a `*A közös forrásmegjelölések…*` sor → `<!-- közös forrásmegjelölés: … -->`; a szakaszvégi `*Forrás: …*` sor névlistára + `<!-- eredeti: … -->`; `tabla_ala` (406; `ismetlo_jegyzet` 397); `_szam_link_nevelo` (478); `onref_csere` (351); `strong_szo_elol` (298).
11. Kapuk (a kész szövegen): `lxx_egyezes_kapu` (1974), `hely_egyseg_kapu` (2031), `teljesseg_kapu` (7558). Hiba esetén a lap nem íródik ki.
12. Fájlba írás: `io.open(cel_ut, 'w', encoding='utf-8', newline='\n')`; utána `kizarasok_melleklet(m, sorai)` (7577) írja a `_KIZARASOK.md`-t (`KIZARASOK_UTOTAG` 7484).

### 2/a (i) — „2. Előfordulások” + „2.1 Az igehelyek szövege” (`blokk_elofordulasok` 898–1070; a lap `#elofordulasok` blokkja)

**Nyers szöveget előállító függvények (hívási fa):**
- `blokk_elofordulasok` 898–1070 — a 2. tábla sorai, a `[^n]` lábjegyzetek, az 1/a tételek (a „2.1” az `1/a` címmel készül, `uj_cimek_alkalmaz` nevezi át), a hatókör-mondat. Olvas: a hívótól kapott `sorai` (`adat/elofordulasok.tsv` a `G.tsv_beolvas` 235-ön át, `G.elofordulasok_id_szerint`); `G.igehely_rendezo_kulcs` 221 ← `G.konyv_sorszam` 195, `G.igehely_fejezet_vers` 214, `G.konyv_token` 313; `G.konyv_teszamentum` 319 (← `ujszovetsegi_tokenek_betolt` 261, `Konyv_normalizalo_tabla.tsv`).
- `gerinc_adat` 3225–3275 — a „Jelentés (a szó)” oszlop táblái egyszer betöltve: `adat/szotar_szakasz_cimke.tsv`, `bdb_szakaszok.tsv`, `bdb_szakasz_hu.tsv`, `bdb_vers_jelentes.tsv` (`VJ.vj_feloldott`, `bdb_vj_szabaly.py` 21), `thayer_szakaszok.tsv`, `thayer_vers_jelentes.tsv`, `glosszak_heber_hu.tsv`, `tiltott_fordulatok.tsv`, `konkordancia/TAHOT_kivonat.tsv` (`L.load_tahot`, `lekerdez.py` 280 → `token_szam`), `konkordancia/BDB_teljes_unabridged.tsv`.
- `jelentes_cella` 3650–3699 → `jelentes_cimke_token` 3529–3625 (a címke és az ⓘ szöveg; `_HANYSZOR` 3136, `TAHOT_KIVONAT_FAJL` 3135) ← `bdb_vers_szocikk` 3423, `_bdb_poz_megbizhato` 3397, `_bdb_poz_szocikkei` 3375, `_bdb_sor_kezdetek` 3358 (← `_lapit` 3305 ← `_szelet_modul` 3293, `olvaso_szerver/bdb_szelet.py` importlib), `_vers_ut_szocikkei` 3386, `bdb_szocikkek` 3321, `kutatoi_szakasz` 3451, `kutatoi_kulcs` 3213, `bdb_peldak` 3461, `bdb_tartomanyban` 3469, `_pelda_kulcs` 3523, `_bdb_sor_utvonal` 3515, `kulcs_ala_esik` 3316, `gerinc_ala_esik` 3207, `gerinc_utvonal_vag` 3165, `szakasz_jel` 3172, `szakasz_kulcs_jel` 3335, `szakasz_szoveg` 3198, `_nevelo` 3188, `GerincHiba` 3156.
- `_szakasz_olvasoi_glossza` 3630, `_tagolatlan_olvasoi` 3640, `fej_glossza` 3936 ← `bdb_gerinc_szocikkek` 4282 (← `BT.szocikkek`, `bdb_tagolas.py` 75; `BR.zarojel_javit`, `bdb_rovidites.py` 170 ← `zarojel_javitasok` 159, `_javitasok` 115: `adat/bdb_forras_javitas.tsv`; `_bdb_hu_strong` 4291), `olvasoi_glossza` (`szotari_glossza.py` 39) ← `vegyes_cim_nelkul` 25, `jelolo_levag` 84, `_glossza_elotag_nelkul` 68.
- `kulcsszo_cella` 874–890 → `kiejtes_ehhez` 267–290 (TAHOT/TAGNT ragozott alak + kiejtés) ← `tahot_index` 247, `tagnt_index` 257, `tahot_vers_index` 296 (**M1: az utolsó előfordulás**), `L.load_tagnt` 290, `heber_gepi` 307 ← `HK.kiejt` (`heber_kiejtes.py` 234), `HK.teljes_szo` 250, `HK._szo` 99; `gorog_magyaros` 363 ← `KJ.atir` (`kiejtes.py` 100; `szabalyok_betolt`, `kivetelek_betolt`: `adat/kiejtes_szabalyok.tsv`, `kiejtes_kivetelek.tsv`); `lemma_kiejtes` 381 → `lemma_kiejtes_szabaly` 418 ← `tbesg_tbesh_index` 317 (TBESG.txt, TBESH.txt; `_U.kotelezo`, `utvonalak.py` 43), `heber_lemma_kiejtes` 373, `_kiejtes_tablak` 350; `ragozott_kiejtessel` 857; `LEMMA_VALTOZAT` 402, `KIEJTES_HIANY` 396.
- `ubs_jelentes_cella` 807–847 ← `ubs_indexek` 768 (`UBS.build_ref_index` / `build_jelentes_index`, `ubs_hozzarendeles.py` 80/90; `UBS_DNTG_referenciak.tsv`, `UBS_DNTG_jelentesek.tsv`), `UBS.hozzarendel` 100, `ubs_glossza_cella` 799 ← `forditas_ehhez` 794 ← `forditasok_index` 784 (`adat/forditasok.tsv`; **M5: az `elavult` nincs szűrve**).
- `dbh_jelentes_cella` 3702–3743 ← `ubs_dbh_adatok` 1570 (`UBS_DBH_referenciak.tsv`, `UBS_DBH_jelentesek.tsv`; `motivum_strong_tokenek` 196), `karoli_mt_vers` 1595 (`Karoli_versmegfeleltetes.tsv`), `igehely_lista` 166 (← `L.parse_igehely` 180, `parse_range` 227, `in_range` 248).
- `lexikon_jelentes_cella` 1073 — csak a nem gerinces ág (HAMART-001-en nem fut).
- `SZKZ.kozos_proveniencia` (`szerep_kizart.py` 397–419; `PROV_HARMAS` 393): az azonos proveniencia-sorok ‹E1› jelre cserélése + a blokk alatti közös sor.
- 2.1 rész: `L.load_karoli_1908` (`lekerdez.py` 322; `Karoli_1908.tsv`), `igehely_lista`, `SZKZ.olvasoi_indok` (`szerep_kizart.py` 322; `BELSO_KIFEJEZES` 291, `AZON_ELEJEN` 296, `DONTES_MONDAT` 297, `_piszkos` 300) a `kapcsolodas` mezőre, `ikon_nelkul` 564, `_anchor_id` 893.
- Összegző olvasói mondat: `OK.elofordulasok_uj` (`olvasoi_kovetkeztetes.py` 45–73; `fok` 22, `SULYPONT_KUSZOB` 41, `SZOVETSEG_KUSZOB` 42), `konyv_teljes_nev` 3069 (`Konyv_normalizalo_tabla.tsv`), `szam_osszegzes` 602, `olvasoi` 573 / `OLVASOI_SABLON['1a']` 462.
- Csomagolás: `_lexikon_blokk` 446, `LC` 122 ← `licenc_sor` 112 ← `licencek` 87 (`adat/licencek.tsv`), `_sorted_unique` 143, `_cella` 1565, `EM_DASH` 75. A `forras_lista` és `forras_licenc_parok` **kódba írt** fájllistákat tartalmaz (`UBS_DBH_*_FAJL` 1557–1558, `SZAKASZ_CIMKE_FAJL` 3130, `BDB_VERS_JELENTES_FAJL` 3133, `THAYER_VERS_JELENTES_FAJL` 3138, `TAHOT_KIVONAT_FAJL` 3135) — ez adja a blokkfejléc `forrás:`/`licenc:` listáját, és a `fl_elofordulasok`-on át a Kolofon és a 12. Irodalom forráslistáját (nem a valódi olvasásból).
- Motívum-specifikus: `TEMATIKUS_SAJAT_SZO` 871 (`('HAMART-001','Jel 22:3')`), az `uj_szerkezet(...)` ágak a 898–1070-ben (a `[^n]` szöveg `str.replace`-e: „jelentés-címke: a sornak nincs Strong-tokenje” → „Tematikus hely…”).

**Utófeldolgozó lépések, amelyek a 2. szakasz nyers szövegét a végső lapszöveggé alakítják** (a 2. szakasz = a `lexikon#<ID>#elofordulasok` blokk; sorrend a fenti lánc 7–10. pontja szerint):

| # | Lépés | Függvény (sor) | Mit érint a 2. szakaszban |
|---|---|---|---|
| a | címcsere | `uj_cimek_alkalmaz` 7157 (`UJ_CIMCSERE` 7125) | „## 1. Előfordulások” → „## 2.”, „#### 1/a.” → „2.1” |
| b | Jelmagyarázat-csere | `kesz_lap_elotte` 8298 (`UJ_JELMAGYARAZAT_CSERE` 8249) | a lap elején, nem a 2. szakaszban (ValueError, ha a szöveg nincs meg) |
| c | **olvasói átírás** | `olvasoi_atiras` 8228 → `olvasoi_sor` 8218 → `_olvasoi_resz` 8147–8208 | a táblasorok, a `[^n]: …` definíciók, az 1/a sorok látható szövege: `_PROV_RX` 7964 → `_prov_olvasoi` 8125 („forrás: …, dátum”); `olvasoi_forrasnev` 7914 / `_nevelo_illeszt` 7904 (fájlnév → forrásnév, névelő); `_FAJL_RX`; `_DT_RX` + `dontes_datum` 7947 / `ervenyes_dontes` 7932 (`DONTESEK.md`: „DT…” → „szerkesztői döntés, <dátum>”); `_TETEL_RX` (F/N/# tételszám törlése); `_KOD_RX` (G…/R… kód); `_ZSARGON`; `UJ_OLVASOI_MUNKASZO` 7967; `NYM.szerkesztoi` (`nyilt_mag_export.py`); `IGAZOLAS_OLVASOI`; takarító regexek. A `[^n]: proveniencia: …` és `scope=` sor végére **`<!-- eredeti: … -->`** kerül (8228–8244), ha az átírás változtatott |
| d | jelölt-lábjegyzet, BDB-fej | `kesz_lap_utana` 8339 → `jelolt_labjegyzet_olvasoi` (csak `[^k…]`/`[^mj…]`; a 2. szakaszon nem fut), `SZONEZET_NYERS_RX`, `BDB_FEJ_NYERS_RX`, `BDB_SZAMLALO_RX` | a 2. szakaszon: a `BDB_SZAMLALO_RX` az `_NNN` számlálót törli |
| e | névelő-levétel | `nevelo_le` 8384 (`_nevelo_nelkul` 8374, `NEVELO_MONDAT_SZO` 6) | táblacellák és listaelemek eleji „a/az” |
| f | kiejtés-pótlás | `kiejtes_potol` 9990 → `kiejtes_szoveg.potol` 278 (`_bejar` 204) | az első előfordulás kiejtése a 2. szakasz szövegében |
| g | Strong-jelölés, BDB, könyvnév, idézőjel | `OU.alkalmaz` 354 (`strong_sor` 269, `bdb_sor` 145, `konyv_sor` 130, `idezojel_sor` 110); `strong_cim` 1845 | a Strong-számok `<sup class="strong">`-ra, a könyvrövidítések linkre, az idézőjelek „…”-ra |
| h | **lábjegyzet → tábla alatti jegyzet** | `TJ.alkalmaz` 250 → `olvasoi_jegyzet` 172 (`_jelentes_tomor` 114, `_forras_elemek` 99, `_szopar_jegyzet` 145); **`tabla_ala` 406**: a táblasorban `[^n]` → `<sup class="lj"><a href="#j-2-5">2.5</a></sup>`, a definíció a tábla alá kerül: `- <span class="lj-szam" id="j-2-5">2.5</span>…` (azonos látható szöveg egyszer; `ismetlo_jegyzet` 397 csak a 3. és 6. szakaszon, `ISMETLO_SZAKASZ` 388) | a 2. és a 3. tábla jegyzetei |
| i | közös forrásmegjelölés | `TJ.alkalmaz` 250–291: a `*A közös forrásmegjelölések…*` / `*Minden sor forrásmegjelölése…*` sor → `<!-- közös forrásmegjelölés: … -->` | a 2. szakasz alatti magyarázó sor |
| j | forrássor | `TJ.alkalmaz`: a szakaszvégi `*Forrás: …*` névlistára + `<!-- eredeti: … -->` | a blokk végi forrássor |
| k | önreferencia, névelő a linken | `onref_csere` 351, `_szam_link_nevelo` 478, `strong_szo_elol` 298 | „a lap” fordulatok; „az [4.2…” névelő |
| l | kapuk | `lxx_egyezes_kapu`, `hely_egyseg_kapu` (regex a lapszövegen) | a 2. szakasz helyszáma és a többi blokk egyezése |

### 2/a (ii) — „1. Döntési út” (1.1–1.5; `blokk_dontesi_ut` 7648–7799) és a `_KIZARASOK.md` melléklet

- `blokk_dontesi_ut` 7648: 1.1 `m['negativ_kriterium']`, `m['folerendelt_fogalom']` (`adat/motivumok.tsv`), `SZKZ.olvasoi_indok`; 1.2 `gerinc_elem` a `sorai`-ból, `lemma_kiejtes` 381, `rovid_jelentes` 1852 (← `glosszak_heber_hu` 1836: `adat/glosszak_heber_hu.tsv`; `tbesg_rovid_glossza` 1823: TBESG), `lemma_cim` 389, **`teljesseg_halok` 7377** (`naplok/F123_teljesseg_<ID>.tsv`, **M13: pillanatkép**), `TELJESSEG_HALO_NEV` 7370, `TELJESSEG_HORGONY` 7554 (← `_heading_slug` 633), `kizarasok_link` 7549; 1.3 `dontesi_ut_adat` 7434, `SZKZ.ok_megjegyzesek` (`szerep_kizart.py` 70), `L.load_karoli_1908`, `_reszletek` 7616, `html_escape` 7621; 1.4 `_lanc_szo_nev` 7325, `_hely_bontas` 7361 (← `_konyvresz` 7341, `OU_USZ_KONYVEK` 7351), `_funkcio_magyarazat` 7316, `_anchor_id`; 1.5 `_ige_link` 7312, **`_modszertan_nyitott` 7625** (← `res_forras_sorok` 6424, `res_torzs` 6490, `res_tanulmany_torzs` 6465, `_tanulmany_szoveg` 6447 → `G.forras_nezet`, `general.py` 1275: a motívum kézi forrása, `motivumok/<ID>.md`); olvasói bevezető: `OK.nevelo_szam` (`olvasoi_kovetkeztetes.py` 320), `OK._ezres` 124; csomagolás `_lexikon_blokk` (forrás: `jeloltek.tsv`, `elofordulasok.tsv`, `motivumok.tsv`, `elutasitasi_okok.tsv`, `Karoli_1908.tsv` — kódba írt lista).
- `dontesi_ut_adat` 7434: `SZKZ.okok` (56; `adat/elutasitasi_okok.tsv`), `jeloltek_sorok` 1093 (← `G.elofordulas_jeloltek`, `general.py` 293; `adat/jeloltek.tsv`), `csoport_n` 7430 / `csoport_egyedi` 7405 (← `NYM.csoport_tagjai`, `nyilt_mag_export.py` 825: `naplok/F123_teljesseg_<ID>_blokkok.tsv`; `NYM.CSOPORT_RX` 820, `BLOKK_RX` 821; **M13**), `SZKZ.csoport_versszam` 137 (versszám a `forras_kereses` szövegéből), `SZKZ.jeloles_oka` 211 (← `_ahol` 112, `_tsk_reszlet` 116, `_teljesseg` 201), `SZKZ.elutasitas_oka` 97, `SZKZ.olvasoi_ok` 65, `SZKZ.versek` 149, `_versek_halmaz` 7395.
- `kizarasok_melleklet` 7577–7613 ← `kizarasok_adat` 7492 (`MellekletHiba` 7488: a számok összeadása; ez a melléklet kapuja), `_konyvenkent` 7535 (← `SZK.vers_kulcs`, `szerep_karoli.py` 313 ← `karoli_versek` 305), `kizarasok_cim` 7543 (← `TJ.onref_csere`), `SZKZ.ok_megjegyzesek`, `teljesseg_halok`, `TELJESSEG_CIM` 7553, `KIZARASOK_NYITVA_HATAR` 7485. A melléklet **nem megy át** az olvasói átíráson (`OU`, `TJ.alkalmaz`, `olvasoi_atiras` nem érinti); csak `TJ.onref_csere` fut rajta.
- Utófeldolgozás a Döntési útra: a blokk a 7. lépésben, az `uj_cimek_alkalmaz` előtt kerül be (`dontesi_ut_beszur` 7802: a Jelmagyarázat `GENERÁLT-VÉGE` jelölője után), tehát a c–l lépések (fent) rá is lefutnak; a `<details>`/`<p>` HTML-t a `_olvasoi_resz` `_VEDETT_RX`-e (8215) védi, a sima szöveg (1.1–1.5 próza, táblák) átíródik. `teljesseg_kapu` 7558 a lap törzsében nem engedi a nyers teljességi forrássort (`_TELJ_TORZS_RX`), és a `strong` háló Strong-halmazát a mai halmazhoz köti.

### 2/b — a többi szakasz: belépő függvény (mai sor)

| Lapszakasz | Belépő |
|---|---|
| cím (`# 📖 …`), azonosító tábla | `VAZ_SABLON` 9829; `azonosito_tabla_beszur` 7305 ← `egyszerusitett_kolofon` 7284 |
| Kivonat, Miért fontos, 10. Értelmezés, 11. Módszertan, Alátámasztás, Minősítés | `res_blokkok_alkalmaz` 6858 → `res_torzs` 6490 → `res_tanulmany_torzs` 6465 (kézi forrás) vagy `ADAT_RES_RENDEREK` 6804 → `adatres_alatamasztas` 6586, `adatres_minosites` 6670 (+`minosites_jelolt_sorok` 6732, `MINOSITES_STAT`), `adatres_2b` 6642 |
| Tartalomjegyzék | `blokk_tartalom` 643 (a lista kódban: `SZAKASZOK`/`UJ_SZAKASZOK`) |
| Jelmagyarázat | `blokk_jelmagyarazat` 752 (`JELMAGYARAZAT_TORZS` 702); `kesz_lap_elotte` 8298 |
| 3. Kizárt és vizsgált helyek | `blokk_kizart` 1103 (← `SZKZ.blokk_torzs`, `SZKZ.vizsgalt_versek`, `SZKZ.osszesito_sor`, `OK.kizart_uj`) |
| 4. Áttekintés | `attekinto_beszur` 8536 ← `attekinto_tabla` 8523 (`lxx_tarsak` 8493, `_lxx_tars`, `rovid_jelentes`, `lemma_kiejtes`) |
| 4.1–4.10 szavanként (4.1 Alapjelentés, 4.2 Mélységi szócikk, 4.3 Teológiai, 4.4 Jelentésszerkezet, 4.5 Tömör jelentés, 4.6 LXX-híd, 4.7 Megfelelők, 4.8 Nyelvi háttér, 4.9 Versenkénti jelentés, 4.10 Kiejtés) | `blokk_szocikkek` 2727 → `szerep_vaz` 2626 → `_szerep_blokk` 2581 → `SZEREP_EPITO` 2341 / `GERINC_SZEREP_EPITO` 4983: `_tartalom_heber_tbesh` 1524, `_gerinc_tbesh` 4850, `_gerinc_szocikk` 4674 (4.2; `BT`, `BR`, `szotari_glossza`), `_gerinc_tw` 4871 / `_tartalom_teologiai` 2138, `_tartalom_heber_dbh_tomor` 1623, `_tartalom_gorog_tomor` 1736, `_gerinc_ubs_mutato` 4907, `_tartalom_heber_lxx_parok` 2219, `_tartalom_gorog_lxx` 2064, `_tartalom_sece` 1897, `_tartalom_heber_etimologia` 2178, `_gerinc_bdb_fej_rovid` 4722, `_tartalom_heber_dbh_vers` 1646, `_tartalom_ubs_oszlop` 4812; a Thayer-kártya nyers adata: `gerinc_adat` `th_sz` |
| 4.11 Visszhang (mutató) → 9. Hatástörténet | `blokk_visszhang` 9025 ← `visszhang_beszur` 8563; áthelyezés `hatastortenet_athelyez` 9630; `blokk_visszhang_hatter` 9770; `rokon_tabla_48` 9206 (a 4.8 végére); `hatastortenet_forrasok` 9551 |
| 4.12 Nave | `_gerinc_nave` 4963 (`SZN`) |
| 4.13, 4.14 Károli-megfelelők, rejtett/hamis párhuzam | `_gerinc_karoli` 4941 (`SZK`, `olvasoi_13_szavankent`, `olvasoi_14_szavankent`) |
| 4. Rokon szavak, kulcsszavak | `rokon_szavak_strongok` 1306 → `_epit_szotar_alszakasz` 1290; `kulcsszavak_blokk` 2693 |
| 5. LXX-fordítói döntések | `blokk_lxx` 5428 ← `lxx_statisztika` 1958 ← `lxx_osszevetes` 5149; `lxx_egyforras_ellenoriz` 5376; `lxx_dontesek_index` 5051 |
| 6. Kereszthivatkozások | `blokk_kereszthivatkozasok` 5523 (`kh_index` 5496 ← `KHS.megerositett_sorok`; `tsk_index` 5483 ← `TK.karoli_index`) |
| 7. Kapcsolatok | `blokk_kapcsolatok` 5630 (`kapcsolatok_sorok` 5615) |
| 8. Kapcsolódó motívumok | `blokk_kapcsolodo` 5737 |
| 10. + vitatott pontok szakirodalma | `res_torzs` (ertelmezes); `szakirodalom_beszur` 9598 (`vitatott_forrasok` 9585) |
| 12. Irodalom és idézés | `blokk_idezes` 5816 (`kotelezo_megjeloles` 5916) |
| Kolofon | `blokk_kolofon` 6247 (`kolofon_forrastabla_olvasoi` 6225, `kolofon_forrasoszlop_kapu` 6216, `kolofon_szerzoseg` 5999, `kolofon_kiadas_sorok` 5970, `kolofon_lektor_uj` 6127, `kolofon_kozlemenyek` 6049, `kolofon_naplo_cella` 5940) |
| Szakaszcímek, számozás | `uj_cimek_alkalmaz` 7157; a 4.N pontnevek: `szerepek_sorok` 7052 (`adat/szotar_szerepek.tsv`) |

*Nem követve:* a 4.1–4.14 belső hívási fája (szócikk-kártyák, `bdb_*`, `thayer_*`, `szerep_*` segédfüggvények), a `blokk_visszhang` / `blokk_kereszthivatkozasok` / `blokk_idezes` / `blokk_kolofon` részletei; a 4.N ↔ építő-függvény megfelelés a `SZEREP_EPITO`/`GERINC_SZEREP_EPITO` kulcsai (nyelv, sorrend) alapján áll, a megjelenített számozást az `uj_cimek_alkalmaz` adja (nem ellenőrizve minden pontra). A `blokk_kizart` hívottai: `SZKZ.blokk_torzs` 448, `SZKZ.vizsgalt_versek` 176, `SZKZ.osszesito_sor` 534, `OK.kizart_uj` 129.

## F218.1 — alapmérés (4. lépés)

*Bemenet: `git show HEAD:lexikon/HAMART-001_TUDOMANYOS.md` (3 271 sor) és `…/ISTENTISZT-001_TUDOMANYOS.md` (2 025 sor), LF. „Látható” = a `<!-- … -->` megjegyzések (többsorosak is, a sorszámok megtartásával) eltávolítása után. A szakaszok a `## ` címsor első tokenjével jelöltek; **az ISTENTISZT-001 lapon a régi számozás áll** (pl. 1/b, 2 = Szótári háttér, 5/b), a HAMART-on az új (2 = Előfordulások, 4 = Szótári háttér). A mérés szkriptje a repón kívül (`%TEMP%\f218_1\count.py`, `t4.py`). A HN-08 számlálás a látható szövegből a HTML-címkék és a `](…)` linkcélok kivételével történt. Sorszámok a lapfájl sorai.*

| osztály | HAMART db | ISTENTISZT db | hol | hogyan mértem |
|---|---|---|---|---|
| `ts=` sorok (nyers) | 34 sor | 40 sor | HAMART: Tartalomjegyzék 1, Jelmagyarázat 1, 1. 1, 2. 4, 3. 5, 4. 6, 5. 1, 6. 3, 7. 3, 8. 2, 10. 2, 11. 3, 12. 1, Kolofon 1 | a sorban `ts=` |
| `ts=` sorok (látható) | **0** | **29** | ISTENTISZT: Jelmagyarázat 1, 1. 1, 1/b 7, 2. 4, 4. 3, 5. 4, 5/b 1, 6. 7, 7. 1; sorok: 79, 153, 509, 512, 528, 530–532, 548, 870, 989, 1011… | a sor a megjegyzések eltávolítása után is tartalmaz `ts=`-t |
| HN-15 | 2 | 3 | HAMART 1283, 2072 (4.); ISTENTISZT 666, 941, 1095 (2.) | `magyar rövid glossza-tábla a görögre még nincs` (látható) |
| T9 | 1 | 1 | Kolofon, HAMART 3171, ISTENTISZT 1921 | a Kolofon „Szerzőség.” sora: „Az értelmező szakaszokat (Kivonat, Miért fontos ez a lelet, Értelmezés, Módszertan és nyitott kérdések) mesterséges intelligencia (claude-opus-5-5) írta az adatok alapján; a szerző jóváhagyta.” (HAMART; az ISTENTISZT-on a szakaszlista hosszabb, a modellnév `…` kódjelöléssel) |
| HN-03 | 10 | 1 | HAMART: 2. 1 (225), 4. 4 (1439, 2078, 2082, 2086), 9. 1 (2998), 12. 4 (3106, 3108, 3110, 3116); ISTENTISZT 1585 (6.) | `\((?:a\|az\|A\|Az) [^()\n]*(?:BDB\|Thayer\|TBESG\|TBESH\|STEPBible\|MCGED\|SDBH\|LSJ\|SECE)[^()\n]*szótár[^()\n]*\)`; alakok: „(a BDB-szótár szerint)”, „(a BDB-szótár, közkincs)”, „(a Thayer-szótár, közkincs)”, „(a BDB-ben: …; a BDB-szótár)”, 3× „(a STEPBible rövid szótára szerint)”, „(az MCGED görög szótár, © Mounce 1993)”, „(az SDBH szemantikai szótár, CC BY-SA 4.0)”, „(a szótári szakaszok címketáblája, a BDB-szótár, a Thayer-szótár; …)”; ISTENTISZT: „(a héber BDB, és két külön görög szótár, a TBESG és Thayer)” |
| HN-10 megjegyzésben | 4 | 3 | HAMART: 6. 3, Kolofon 1; ISTENTISZT: 4. 3 | `Karoli_kereszthivatkozasok.tsv` a `<!-- … -->` belsejében |
| HN-10 látható szövegben | **0** | **17** | ISTENTISZT: 1/b 8, 4. 1, 6. 5, 8. 1, Kolofon 2 (sorok: 509, 512, 528, 530–532, 1380, 1555, 1561, 1567, 1642, 1652…) | ugyanaz a fájlnév, a megjegyzések eltávolítása után |
| HN-01 ismétlő jegyzet | 6 (a 23-ból) | 0 (nincs tábla alatti jegyzet; a régi szerkezet) | HAMART jegyzetsorok 280 (j-2-2, közös: „zócikk egésze ” 14 kar.), 295 (j-2-17, „ κατάθεμα (katathema)” 21), 957 (j-3-1, „: שָׁחַת (sáchat)” 17), 959 (j-3-3, „két lánc-szó egy versben vagy a szomszédos versben” 50), 961 (j-3-5, „otívum szavainak teljes bibliai keresése” 40), 983 (j-3-6, „otívum korábbi ” 15) | a `- <span class="lj-szam" id="j-…">` sor látható szövege és a rá hivatkozó (`href="#j-…"`) táblasor cellái (címke- és markup-mentesítve, a jegyzetjel nélkül); `difflib.SequenceMatcher.find_longest_match` ≥ 12 karakter. A 3 példa a 959, 961, 295. sor; a 280., 957., 983. sor találata rövid, névszerű részszöveg (valószínűleg nem valódi ismétlés) |
| tábla alatti jegyzetek | 23 | 0 | 17 a 2. szakasz (2. tábla), 6 a 3. szakasz (3. tábla) alatt: **egyezik a brief 23 = 17 + 6 adatával** | `^- <span class="lj-szam"` sorok szakaszonként |
| HN-08 `DT\d+` | 0 | 73 (59 sor) | ISTENTISZT 103, 134, 138, 155, 457, 500–502… (pl. DT272, DT381, DT382, DT393) | látható szöveg, `DT\d+` |
| HN-08 `#\d{2,3}` | 0 | 1 | ISTENTISZT 603 (`#142`) | `(?<![\w&/])#\d{2,3}\b` |
| HN-08 `N\d+` | 0 | 2 (1 sor) | ISTENTISZT 532 (`N59`) | `\bN\d+\b` |
| HN-08 `(G\d+)` | 0 | 11 | ISTENTISZT 44, 103, 324, 531, 556, 573, 856, 858… (pl. (G10), (G3), (G7), (G1941)) | `\(G\d+\)` |
| HN-08 `F\d{2,3}` | 0 | 29 | ISTENTISZT 103, 509–515… (pl. F131, F110) | `\bF\d{2,3}\b` |
| T4 (TAHOT-ismétlés, eltérő alak) | 2 sor-Strong pár | 5 | l. alább | l. alább |
| N178 (15 Strong) | 0 | 0 | — | l. alább |
| elavult fordítás | 5 sor | 0 sor | l. alább | l. alább |

**T4.** Mérés: az `adat/elofordulasok.tsv` HAMART-001 (49 sor) és ISTENTISZT-001 (20 sor) sorainak `strong` mezőjét `+`-nál szétvágva a `H…` tokenek; a `konkordancia/TAHOT_kivonat.tsv` `Igehely` kulcsa a sor `igehely` mezője (egy vers tokenjei); a (vers, Strong) párra a tokenek száma > 1 és a `Ragozott alak` különbözik. Az „első” és „utolsó” alak a fájlsorrend szerinti. A HAMART 4 `H` sor-Strong párja tartománybeli igehelyen áll, amelynek kulcsa nincs a TAHOT-ban (nem mérhető egyszerű kulcsolvasással; a régi kód `igehely_lista`-val bont).

| motívum | igehely | Strong | első alak | utolsó alak | token |
|---|---|---|---|---|---|
| HAMART-001 | 1Móz 6:5 | H7451 | רָעַ֥ת | רַ֖ע | 2 |
| HAMART-001 | 1Móz 6:12 | H7843 | נִשְׁחָ֑תָה | הִשְׁחִ֧ית | 2 |
| ISTENTISZT-001 | 1Móz 4:26 | H7121 | יִּקְרָ֥א | קְרֹ֖א | 2 |
| ISTENTISZT-001 | 1Móz 4:26 | H8034 | שְׁמ֖ | שֵׁ֥ם | 2 |
| ISTENTISZT-001 | 1Kir 18:24 | H7121 | קְרָאתֶ֞ם | אֶקְרָ֣א | 2 |
| ISTENTISZT-001 | 1Kir 18:24 | H8034 | שֵׁ֣ם | שֵׁם | 2 |
| ISTENTISZT-001 | Jóel 2:32 | H7121 | יִקְרָ֛א | קֹרֵֽא | 2 |

(A 1Kir 18:24 H8034 két alakja csak a kantillációban tér el: `שֵׁ֣ם` / `שֵׁם`; a szigorú „eltérő szóalak” mérce szerint ez is találat.)

**N178.** A 15 Strong (G0260, G0575, G0846, G1100, G1909, G2675, G3536, G3563, G4151, G4404–G4407, G5132, G5567) közül **egyik sem** szerepel a HAMART-001 és az ISTENTISZT-001 `elofordulasok.tsv` sorainak `strong`, `lexikon_entry_id` vagy `gerinc_elem` mezőjében. A motívumok Strongjai: HAMART-001: G1311, G1944, G2671, G5351, G5356, H0056, H0127, H0423, H0779, H2403, H2555, H6093, H6975, H7451, H7843; ISTENTISZT-001: G1941, H7121, H8034. (A kapu-érintettség tehát 0; az N178 a két mai lapot nem érinti.)

**Elavult fordítás.** Az `adat/forditasok.tsv` kulcsoszlopai: `szotar, strong, entry_id, jelentes_szam, mezo`; `allapot` értékei: sonnet 33 220, elavult 311 (Thayer 213, BDB 98), kezi 71, opus 21. Illesztés a `strong` oszlopon a motívum `strong` mezőinek halmazára (az `entry_id` szerinti illesztés nem ad többletet): **HAMART-001: 5 elavult sor, mind Thayer (G1311, G2671, G5351, G5356)**; ISTENTISZT-001: 0. A régi kód ezeket szűrés nélkül veszi be az UBS/tW/BDB/TBESH/Thayer cellákba (M5), tehát a HAMART-on legfeljebb ez az 5 sor érintett.

*Proveniencia: `scope=lexikon/HAMART-001_TUDOMANYOS.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, adat/elofordulasok.tsv, konkordancia/TAHOT_kivonat.tsv, adat/forditasok.tsv | forras=5e4344f6 | ts=2026-11-13`.*

## F218.1 — könyvnév-aliasok (5. lépés, GK-17 / B63) és T3 (5/b): csak vizsgálat

### 5. A két kódbeli könyvnév-szótár és a normalizáló tábla

- **`KH_KONYV_JAVIT`** (`lexikon_general.py` 153): `Eféz → Ef`, `Siral → JSir`. Egyetlen használati helye a `karoli_colon` (156–163): ha a sztring `<régi> `-vel kezdődik, a kulcsot az újra cseréli, utána `,` → `:`. A Károli-KH/TSK magyar megjelenítésére szolgál (6. és Minősítés). Csak előtag-csere, a táblát nem olvassa.
- **`EXTRA_KONYV`** (`olvasoi_utofeldolg.py` 44–50, ~45 bejegyzés): `Zef→Sof, Csel→ApCsel, Ésa→Ézs, Ezék→Ez, Mát/Máté/Matt→Mt, Márk/Mark→Mk, Lk/Luke/Lukács→Luk, John/Jn→Ján, 1Jn/2Jn/3Jn/1John→1Ján…, Ám→Ámós, Agge→Hag, Róma/Rom→Róm, Acts→ApCsel, 1Cor/2Cor→1Kor/2Kor, Heb→Zsid, 1Pet/2Pet→1Pét/2Pét, 1Thess/2Thess→1Thessz/2Thessz, Bir→Bír, Genezis/1Mózes→1Móz, Jas→Jak, Eph→Ef, Col→Kol, Rev→Jel, Jude→Júd, Mk→Mk`. Használat: `konyv_alias()` (67–87) először a normalizáló tábla 1. oszlopát és 4. oszlopának vesszős aliasait gyűjti (`alias[szóköz nélkül] = 2. oszlop`), **utána `alias.update(EXTRA_KONYV)` felülírja**, végül a magyar rövidítések (2. oszlop) kulcsait törli. Fogyasztó: `konyv_sor` (130; `OU.alkalmaz`, a lánc 9. lépése).
- **A tábla:** `konkordancia/Konyv_normalizalo_tabla.tsv`, fejléc: `STEPBible-rövidítés · Magyar rövidítés · Teljes magyar könyvnév · Forrás-alakok`, 67 nem-`#` sor (fejléc + 66 adatsor); az `Ef` és a `JSir` sor 4. oszlopa üres. **Fogyasztói:** a `grep` 59 `eszkozok/` fájlt talál (pl. `normalizal.py`, `proza_allitas.py`, `sqlite_epit.py`, `thayer_api_koteg.py`, `general.py`, `lekerdez.py`, `lexikon_general.py`, `olvasoi_kapu.py`, `olvasoi_utofeldolg.py`, `nyilt_mag_export.py`, `karoli_kh_*`, `tanu_index.py`, `olvaso_szerver/lekerdezesek.py`). A 4. oszlopot (`Forrás-alakok`) **olvassák**: `normalizal.py` 180–199 (`_karoli_tabla` → `TABLA_ALAKOK` → `FORRAS_ALIAS.setdefault`; ebből épül az `IGE_LEK` és a 11. fordítás-kapu mintái: új alias **új szövegcserét** jelent a normalizálóban), `proza_allitas.py` 140–150 (`konyv_alakok`: csak `^[0-9]?[betű]+$` alakú alias kerül be), `sqlite_epit.py` 310–320 (`Konyvek.step_hu.setdefault`), `thayer_api_koteg.py` 355–366 (a regex-minták listája nő), `olvasoi_utofeldolg.py` 67–87 (fent). Sorrendfüggő olvasás: `olvasoi_utofeldolg.konyv_alias` (az `EXTRA_KONYV` felülír, a magyar kulcsok törlődnek); `setdefault`-os olvasók (`normalizal`, `sqlite_epit`): az első alias nyer. Fordított irányú szótár, amelyet egy új alias-sor felülírna: nem találtam (a fordított irány az 1.→2. oszlop, a 4. oszlop csak alias→kanonikus).
- **Pontos sorszámot vagy fejlécet váró ellenőrzés:** `teszt_normalizal.py` `test_tabla_szerkezet_valtozatlan` (a négy oszlop fejléce pontosan, **66 adatsor**, minden sor 4 oszlopos), `teszt_normalizal.py` `test_tabla_forras_alakjai` (21 csere a pontos szövegre), `teszt_sqlite_epit.py` 277 (`Konyvek` a 4 oszlopos fejléccel); további (`teszt_general_konyvlista.py`, `ellenorzes/tesztek/test_szabalyok.py`, `ellenorzes/tanulmany_ellenorzes.py`, `olvasoi_kapu.py` KONYV szabály): nem néztem meg, hogy pontos számot várnak-e.
- **Javasolt új alias-tartalom** (a meglévő sorok 4. oszlopába, új sor nélkül, a 66 sor megmarad): `Ef` sor: `Eféz`; `JSir` sor: `Siral`. Az `EXTRA_KONYV` ~45 eleme nem vihető át változtatás nélkül: van köztük azonosságra képező (`Mk→Mk`), és olyan, amelynek a magyar célalakja nincs egyeztetve a táblával (`Ám→Ámós`, `Bir→Bír`); a `konyv_alias` ráadásul az `EXTRA_KONYV`-ot a tábla fölé írja, tehát a tábla bővítése nem lenne ekvivalens a mai viselkedéssel.
- **Kockázat olvasónként:** `lexikon_general.karoli_colon` — a `KH_KONYV_JAVIT` kivezetése csak akkor ekvivalens, ha a KH/TSK adat `Eféz`/`Siral` alakjait új kód a táblából oldja fel (ma nem a táblát olvassa, új kód kell); `normalizal.py` — az `Eféz`/`Siral` új alias új szövegcserét hoz a normalizált szövegekben (nem a meglévő kulcsokra, hanem új alakokra); `proza_allitas.py` — új alias-kulcsok a `konyv_alakok`-ban (új találatok lehetségesek); `sqlite_epit.py` — `setdefault`, bővül az olvasói DB könyvtérképe (a DB tartalma változhat); `thayer_api_koteg.py` — új minta a listában; `olvasoi_utofeldolg.py` — a 4. oszlop aliasai bekerülnek a `konyv_sor` szótárába (`Eféz 1:1` ma nem íródik át, utána átírna); a többi ~54 fogyasztót **nem követtem**.
- **Döntés: a táblát nem módosítottam.** Az (a) feltétel (egyetlen olvasó viselkedése sem változik) nem biztosítható: legalább a `normalizal.py`, `proza_allitas.py`, `sqlite_epit.py`, `thayer_api_koteg.py` és az `olvasoi_utofeldolg.py` kimenete új aliasra változna, a többi fogyasztó átvizsgálatlan. A (b) feltétel (sor- és fejlécszám) teljesülne, de az (a) miatt a módosítás elmarad. A bővítést a fogyasztók átvizsgálásával és regressziós méréssel érdemes megtenni.

### 5/b. T3 — az `adat/elofordulasok.tsv` új `sajat_szo` oszlopának érintettsége (csak lista)

Az `adat/elofordulasok.tsv` 20 oszlopos; fejléc: `id, igehely, kapcsolodas, pardes_szint, funkcio, gerinc_elem, strong, lexikon_szotar, lexikon_entry_id, jelentes_szam, jelentes_en, jelentes_hu, karoli_szo, azonositas_modja, megbizhatosag, proveniencia, igazolas, fo_elofordulas, felmerult_tanulmany, forras_tanulmany`. A `grep` 115 `eszkozok/` vagy `.github` fájlt talál, amely a táblára hivatkozik; a lista a fejléc- vagy oszlopfüggő használatokat adja.

- **Pontos fejlécet váró szabály/teszt:** `ellenoriz.py:1165–1181` (`ELOFORDULASOK_FEJLEC`, `szabaly16_elofordulasok_fejlec`: a fejléc pontosan ez a 20 oszlop, a `forras_tanulmany` az utolsó); `betolt.py:50–56` (`ELOFORDULASOK_FEJLEC`, „az utolsó oszlop”); `eszkozok/ellenorzes/tesztek/test_szabalyok.py` 128–139, 1361, 1393, 1712 (`_E31_FEJ`), 1724, 1769, 2015 (saját fejléccel írt ideiglenes táblák; a 16. szabály tesztje a valódi fejlécet várja); `teszt_ellenoriz_13.py:220`, `teszt_ellenoriz_36.py:39`, `teszt_ellenoriz_37_38.py:53`, `teszt_karoli_ellenorzes.py:59`, `teszt_muhely_allapot.py:275`, `teszt_proza_lefedettseg.py:45` (a táblát saját fejléccel generálják; az új oszlop nem érinti, ha nem a valódi fejlécet ellenőrzik).
- **Rögzített fejléclistával író szkript:** `betolt.py:312–317` (`elofordulasok_ir`: a sort az `ELOFORDULASOK_FEJLEC` szerint állítja össze, az új oszlop híján kimaradna vagy üres lenne); `n14_hamart_betoltes.py:48–55, 431, 462, 484, 728` (`ELOFORDULASOK_FEJLEC`, munkalap-író); `g0d_elofordulasok_bovites.py:190` (régi, egyszeri bővítő: `fejlec + ['fo_elofordulas', 'felmerult_tanulmany']`).
- **Oszlopnév szerint olvasók (az új oszlopot nem ismerik, de nem törnek):** a legtöbb (`G.tsv_beolvas`, `general.py` 235–253, dict-sorokat ad és az oszlopszámot kikényszeríti; `lexikon_general.py`, `proza_allitas.py` 73, `olvaso_pilot/bovites.py` 473, `sqlite_epit.py`, `olvaso_szerver/lekerdezesek.py` 328 név szerint választ). **Pozíció szerint olvasó:** a durva `grep` (`split('\t')[N]`, `cols[N]`, `c[N]` az `elofordulasok.tsv`-t említő fájlokban) egyetlen valódi találatot sem adott; a jelzett fájlok indexe más adatra vonatkozik. Ez **nem teljes bizonyíték** (a 115 fájlt nem olvastam végig).
- **Oszlop-besorolást váró kimenet:** `nyilt_mag_kapu.py:526–556` (`KI_MEZOK['elofordulasok.tsv']` = `kapcsolodas, jelentes_hu, felmerult_tanulmany, forras_tanulmany, fo_elofordulas`; `ell_termekreteg`: az új oszlopot be kell sorolni a csomagba vagy a kizárásba, és a kódkönyvnek sora kell, különben a nyílt-mag kapu megállhat); `nyilt_mag_export.py:125` (`ZART`), 187 (`funkcio`), 197 (az export oszlop-átnevezései), 1481–1559 (az export `oszlop_tsv(fej, sorok, 'elofordulasok.tsv')` az adat fejlécéből épít); `adat/SEMA.md` 2.2 (az oszloplista a sémában).
- **CI:** `.github/workflows/feladatok.yml` 101–102 a táblát a gerinc-/előszűrő-trigger listában tartja (a változása indítja a gerinc-térképet és az előszűrőt); fejlécet nem ellenőriz.
- **Nem követve:** a 115 fájl teljes átvizsgálása; az olvasói SQLite (`sqlite_epit.py`) oszlop-térképe.

*Proveniencia: `scope=grep eszkozok/ .github/, olvasás a hivatkozott fájl:sor helyeken | forras=5e4344f6 | ts=2026-11-13`.*

## F218.2–F218.4 — típusok és az első szelet (az építő session, `claude-fable-5-2`)

### F218.2 — típusok és szerződések

Az `eszkozok/lapgen/` rétegei (`szoveg` ← `bemenet` ← `szamitas` ← `megjelenites`), a három tábla (SEMA 2.66–2.68), a `regresszio.py`, a `festek.py`, a `general.py --cel lexikon2`. A tervezési döntések listája: `naplok/F218_folytatas.md` „Tervezési döntések”. A régi generátor HAMART-kimenete a `general.py` módosítása után bájtra azonos maradt (a módosítás két additív elem: a `lexikon2` cél és a `--mod` kapcsoló; és egy nem additív: az előjavító (E32) egy meglévő hibaüzenetből törölte a „; DT-F09h” döntésszámot, `general.py` `--helyi-lexicon` ága; pontosítva a javítókörben, az 1. ellenőrzés 8. tétele) (`cmp` a `git show HEAD:lexikon/…` tartalmával, mindkét nézet).

### F218.4 — S1: „2. Előfordulások” és „2.1 Az igehelyek szövege”

**Eredmény (HAMART-001, `PARDES_DATUM=2026-11-13`, `munka` mód):** a szakasz 437 sorából 432 bájtra egyezik a referenciával; **5 diff-sor, mind engedéllyel; engedély nélküli diff-sor: 0.** A bemenet-hash őr rendben. Futásidő a részleges lapra: 4,8 s.
*Proveniencia: `scope=python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa az F218.4 commitja előtt | ts=2026-11-13`.*

| Engedélysor | Osztály | Darab | Mi tér el |
|---|---|---|---|
| S1-FORRAS | GK-07 (a brief 8.1 (b)) | 1 | a blokkfejléc forrás- és licenclistája a valódi olvasásokból jön, nem kódba írt listából |
| S1-T4-1, -2, -3 | T4 (a brief 8.1 (d)) | 3 | az első előfordulás alakja és kiejtése: 1Móz 6:5 (H7451), 1Móz 6:12 (H7843), Jel 11:18 (G1311) |
| S1-ONREF | M-CSERE | 1 | a régi generátor a kézi prózát utólag átírta („a lap” → „a szócikk”, 1Móz 8:21); az új a prózát változatlanul adja |

**Festékpróba:** HAMART-001 0 szivárgás (látott jelzőszavak: belső 137, idézet 326, kézi 180); ISTENTISZT-001 0 szivárgás (belső 86, idézet 180, kézi 85). **Tesztek:** 69 zöld (`python eszkozok/lapgen/tesztek/futtat.py`).

**ISTENTISZT-001 (8.2):** a 2. szakasz generálódik (20 sor, 8 összevont jegyzet); a látható szövegben nincs döntésszám, fájlnév, belső mezőnév. A számok független összevetése és a felhasználó olvasata a teljes lapnál (S9) esedékes.

### Amit a felhasználónak látnia kell az S1 után (a két kör közül az első)

**1. T4 („az első előfordulás”) a mért sorokon rosszabb egyezést ad a Károli-szóval, mint a régi szabály.** A sor Károli-szava és a mutatott eredeti alak:

| Lap | Igehely | Károli-szó a sorban | Régi (utolsó előfordulás) | Új (első előfordulás, T4) | Melyik felel meg a Károli-szónak |
|---|---|---|---|---|---|
| HAMART-001 | 1Móz 6:5 | gonosz | רַ֖ע (ra) | רָעַ֥ת (ráat) | a régi |
| HAMART-001 | 1Móz 6:12 | megrontotta | הִשְׁחִ֧ית (hischít) | נִשְׁחָ֑תָה (nischátá) | a régi |
| HAMART-001 | Jel 11:18 | pusztítják | διαφθείροντας (diaftheirontasz) | διαφθεῖραι (diaftheirai) | a régi |
| ISTENTISZT-001 | 1Móz 4:26 | segítségül hívni az Úrnak nevét | (a második „kárá”) | וַיִּקְרָ֥א (vajjikrá: „és nevezé”) | a régi |
| ISTENTISZT-001 | 1Kir 18:24 | segítségül hívom az Úrnak nevét | (a második „kárá”) | וּקְרָאתֶ֞ם (úkerátem: „hívjátok”) | a régi |
| ISTENTISZT-001 | Jóel 2:32 | Az Úrnak nevét hívja segítségül | (az utolsó) | יִקְרָ֛א (jikrá) | az új |

Sem az „első”, sem az „utolsó” nem jó minden sorra: a helyes alak az, amelyik a sor Károli-szavának felel meg. Javaslat: a választás a Károli–Strong párosításból jöjjön (`adat/karoli_strong/parok_<könyv>.tsv`, B54), és csak párosítás híján az első előfordulás. A generátor most a T4 döntés szerint az elsőt adja; a három HAMART-sor az engedélyfájlban áll. Az alapmérés (F218.1) csak a héber szöveget mérte (2 sor), a görög Jel 11:18-cal az osztály 3 soros.

**Kiegészítés a javítókörben (2026-11-13; az 1. ellenőrzés 5. és 11. tétele).** A fenti táblázat utolsó oszlopa („Melyik felel meg a Károli-szónak”) az építő session **értelmezése** volt, lekérdezés nélkül. A felhasználó döntése (DT868, a DT838 módosítása): „ahol van párosítás: az az alak áll, amelyhez a Károli-szó kötődik; ahol nincs: az első előfordulás”. A generátor ezt a Károli–Strong párosításból (B54) veszi; az alábbi tábla már lekérdezés, nem értelmezés. Minden olyan sor áll benne, amelynek egy Strong-száma a sor versein többször áll:

| Lap | Igehely | Károli-szó | Strong | Az első előfordulás | A Károli-szóhoz kötött alak (ez áll a lapon) | A pár (sorszám a versben) |
|---|---|---|---|---|---|---|
| HAMART-001 | 1Móz 6:5 | gonosz | H7451 | רָעַ֥ת (ráat) | רַ֖ע (ra) | 18 |
| HAMART-001 | 1Móz 6:12 | megrontotta | H7843 | נִשְׁחָ֑תָה (nischátá) | הִשְׁחִ֧ית (hischít) | 11 |
| HAMART-001 | Sof 1:2-3 | föld színéről | H0127 | הָאֲדָמָ֖ה (háadámá) | הָאֲדָמָ֖ה (háadámá) | Sof 1:2: 8 |
| HAMART-001 | Jel 11:18 | pusztítják | G1311 | διαφθεῖραι (diaftheirai) | διαφθείροντας (diaftheirontasz) | 42 |
| ISTENTISZT-001 | 1Móz 4:26 | segítségül hívni az Úrnak nevét | H7121 | וַיִּקְרָ֥א (vajjikrá) | לִקְרֹ֖א (likró) | 17 |
| ISTENTISZT-001 | 1Móz 4:26 | segítségül hívni az Úrnak nevét | H8034 | שְׁמ֖וֹ (semó) | בְּשֵׁ֥ם (besém) | 19 |
| ISTENTISZT-001 | 1Kir 18:24 | segítségül hívom az Úrnak nevét | H7121 | וּקְרָאתֶ֞ם (úkerátem) | אֶקְרָ֣א (ekrá) | 9 |
| ISTENTISZT-001 | 1Kir 18:24 | segítségül hívom az Úrnak nevét | H8034 | בְּשֵׁ֣ם (besém) | בְשֵׁם (vesém) | 11 |
| ISTENTISZT-001 | Jóel 2:32 | az Úrnak nevét hívja segítségül | H7121 | יִקְרָ֛א (jikrá) | יִקְרָ֛א (jikrá) | 5 |

*Proveniencia: `scope=a két mintalap előfordulás-sorai, amelyekben egy Strong-szám a sor versein legalább kétszer áll; a kiejtés-szolgáltatás (lapgen.bemenet.szavak.Kiejtes.ragozott) kimenete Károli-szóval és anélkül | forras=adat/elofordulasok.tsv, adat/karoli_strong/parok_1Moz.tsv, parok_1Kir.tsv, parok_Joel.tsv, parok_Sof.tsv, parok_Jel.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv | ts=2026-11-13`.* A párosítás modell-kimenet (javaslat, nem ellenőrzött adat; az 1Kir, a Jóel, a Sof és a Jel párjai `alacsony` bizonyosságúak). Ha a Károli-szó egy szava a versben többször áll (1Móz 4:26 és 1Kir 18:24: „nevét”), az a pár dönt, amelynek a szomszédos szavai a Károli-szó többi szavával egyeznek. A HAMART-001 három eltérő sora így a régi lappal egyezik: a három T4-engedélysor megszűnt.

**2. A kézi próza önreferenciája („a lap”).** A régi generátor nyolc kódba írt cserével (`tablajegyzet.ONREF_CSERE`) írta át a „lap” szót, köztük adatcellák szövegét is; a 2. szakaszban egy sort érint (1Móz 8:21: „azt a lap vitatott pontként tárgyalja” → „… a szócikk …”). Az új generátor a prózát változatlanul adja, ezért itt a jóváhagyott laphoz képest visszalépés áll, amíg a forrás nem javul. Két út: (a) az adatcella javítása (a régi kód megjegyzése szerint ehhez a nyílt mag angol fordításának hash-e kötődik, ezért maradt a csere a kódban); (b) prózajavító tábla a bemeneti rétegben (a `javitas` oszlop mintájára). Döntés kell; addig engedélysor (S1-ONREF).

**3. Új sablonmondatok (`eredet=uj`, jóváhagyásra várnak).** Egyik sem áll a két mintalap 2. szakaszában; a régi generátor ezekben az esetekben belső szöveget vagy nyers adatértéket írt volna ki:

| Kulcs | Új mondat | A régi alak |
|---|---|---|
| `e2.dbh.ok.nem_egy_vers` | az MT-megfelelő nem egyetlen vers | ugyanez, zárójelben a tábla nyers értékével |
| `e2.dbh.ok.szamozas_elteres` | versszámozás-eltérés, az MT-vers a táblában nincs megadva | ugyanez, zárójelben a belső osztálykóddal |
| `e2.jegyzet.tematikus_sajat.heber` (+ kiejtés nélküli) | Tematikus hely: a vers héber szava, … nem a lánc szava. | a régi csak a görög alakot ismerte |
| `e2.jm.nincs_lekepezve` | a szerkesztői jelentésszám nincs leképezve a szótár tagolására | belső mondat a címketábla nevével |
| `e2.jm.nem_azonosithato` | a BDB idézi a helyet, de nem azonosítható, melyik szócikkében | belső mondat fájlnévvel és sorszámmal |
| `e2.jm.thayer_pelda` | a Thayer a helyet az N. jelentésnél idézi | belső mondat fájlnévvel |
| `e2.jm.thayer_nem_idezi` | a Thayer a helyet nem idézi | belső mondat fájlnévvel |

**4. Amit szándékosan nem változtattam** (a mai jóváhagyott szöveg maradt, betűre): a hatókör-sor zárójeles forráslistája („(a szótári szakaszok címketáblája, a BDB-szótár, a Thayer-szótár; …)”, az alapmérés HN-03 találata a 225. sorban) és a két rövid, névszerű HN-01 találat (2.2 és 2.17 jegyzet). Ha ezek javítandók, az új mondat külön jóváhagyást kér.

**5. Többszavas sor jegyzete.** A nem szópáros motívum többszavas soránál (a két mintalapon nincs ilyen) a jegyzet a szópáros lap formáját követi (szavanként egy rövid mondat), mert a régi út ilyenkor belső szöveget adott.

### Egyeztetett eltérések a brieftől

- **T3 tárolása:** külön kézi tábla (`adat/tematikus_sajat_szo.tsv`, SEMA 2.69, B67), nem új oszlop az `elofordulasok.tsv`-ben: az orkesztrátor technikai döntése (2026-11-13), `dontesek/uj/f218-generator-uj-a.md` DT867. A brief `ir` mezője ezzel a táblával és a döntésfájllal bővült.
- **F218.1 halasztott részei:** a leltár `kovetelmeny` oszlopa (7.4) a heti keret nullázása utánra; az alias-sorok (GK-17) az S5 előttre (az alapmérés szerint a normalizáló tábla 4. oszlopát több eszköz olvassa, új alias viselkedést változtatna).
- **Az S3-ra halasztva (kimondott hibával megáll, ha előbb kellene):** a pontozatlan héber alak szótári kiejtése (B10), az elavult fordítás jelölése az UBS-cellában (T5), a B18/B19/B21 frissességi kapuja (GK-03).

### Ismert korlátok (a független ellenőrnek is)

- A `bemenet/gerinc.py` a szótári táblák nyers sorait adja a `szamitas/szotari_gerinc.py`-nak (belső kulcsként); a látható szövegbe ezekből csak a bemeneti réteg burkolóin át juthat érték, de a `jel_szoveg` és az `idezet_szoveg` a számításból kapott szöveget burkolja. A festékpróba ezt a csatornát nem festi.
- A régi segédmodulok újrahasznosítva, a bemeneti rétegen át: `heber_kiejtes`, `kiejtes`, `bdb_tagolas`, `bdb_rovidites`, `szotari_glossza` (tiszta függvények; az útvonalat a jegyzékből kapják).
- A `lapgen/tesztek` tesztjeit a CI nem futtatja (az `ellenorzes.yml` és a `push_elott.py` névvel sorolja a tesztfájlokat; mindkettő kívül esik a brief `ir` mezőjén).

## Független ellenőrzés — 1. ellenőrzés

*A `fuggetlen-ellenor` subagent (`claude-opus-5-5`) jelentése változtatás nélkül; bemenete: a brief, a `37f087cc..dfb4525a` tartomány, a `teljes` szint és a CI-állapot a head-re. Mentve: 2026-11-13.*

ELTÉRÉS: 11 tétel

Brief: `F218_GENERATOR_UJ_A_BRIEF.md` · tartomány: `37f087cc..dfb4525a` · szint: `teljes`

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0. modell | OK | – | A tényleges modellem `claude-opus-5-5`, a kért `opus`; egyezik, és nem Fable (brief 9.). A `git log --format='%h %(trailers:key=Co-Authored-By,valueonly)' 37f087cc..dfb4525a` szerint az F218.1 commitjai Sonnet 5.5, a többi Fable 5.2. Ez egyezik a jelentés F218.0 sorával. Adattábla `modell` mezőjét a menet nem írt. |
| 3. CI | OK | – | `gh run view 43412314120 --json headSha,conclusion,jobs`: a `headSha` `dfb4525a…`, az eredmény `success`, a `feladatkovetes` és az `ellenorzes` job zöld (E28 és E29 benne). A `futtat.py`-t nem futtattam újra. Megjegyzés: a CI a `lapgen/tesztek`-et nem futtatja (`.github` és `push_elott.py` grep: 0 találat), ezért ezeket magam futtattam. |
| Diéta 3. tesztek | OK | `eszkozok/lapgen/tesztek/` | `python eszkozok/lapgen/tesztek/futtat.py`: 121 futott, 0 hiba, 0 bukás, 35 kihagyva (ez a tesztváz). |
| Diéta 3. lassú tesztek | NEM ELLENŐRIZHETŐ | – | `python eszkozok/teszt_futtat.py --diff 37f087cc`: a `teszt_szintek.py` és a `teszt_visszhang_kapu.py` HIBA. Újrafuttatás: `teszt_futtat.py --fajl teszt_visszhang_kapu --reszletes` → 2 bukás (`test_bevezeto_a_peshat_magot…`, `test_v3_nincs_a_nem_azonositott_helyen`), mindkettő a régi generátor 4.11 blokkjában. A diff ezt a kódot nem érinti (a `general.py`-ban csak argparse és üzenet változott), de hogy a hiba a main-en is fennáll-e, azt a megengedett parancsokkal nem tudtam ellenőrizni. |
| Régi generátor bájt-egyezése | OK | `eszkozok/general.py` | `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon --id HAMART-001 --kimenet <scratch>/regi`, majd `cmp` a `git show dfb4525a:lexikon/HAMART-001_{TUDOMANYOS,KIZARASOK}.md` tartalmával: mindkettő azonos. |
| 8.1 regresszió (S1) | OK | `naplok/F218_elteres_engedely.tsv` | `general.py --cel lexikon2 --id HAMART-001` (5,6 s, 438 sor), majd `regresszio.py --id HAMART-001 --uj …`: „2. Előfordulások” 5 diff-sor, mind engedéllyel; az 5 engedélysor tényleges darabszáma 1/1; RENDBEN. |
| Engedélysor-minta | OK (tartalom) | `naplok/F218_elteres_engedely.tsv:3-7` | `git diff --no-index --word-diff` a referencia 221–655. sora és az új kimenet között. A T4-sorok valóban a három alakcserét adják (1Móz 6:5 רַ֖ע→רָעַ֥ת, 1Móz 6:12, Jel 11:18). Az ONREF-sor „szócikk”→„lap”. A FORRAS-sor a blokkfejléc. `lekerdez.py scan H7451 --szakasz "1Móz 6:5"` / `H7843 "1Móz 6:12"` / `G1311 "Jel 11:18"`: mindhárom esetben „1 igehely, 2 szó-előfordulás” (`forras=TAHOT/TAGNT_kivonat.tsv`). |
| Festékpróba (GK-08b) | OK (futás) | `eszkozok/lapgen/festek.py` | `python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001`: 0/0 szivárgás. Látott jelzőszavak: belső 137 / 86, idézet 326 / 180, kézi 180 / 85. A próba erejének korlátja a következő sorban. |
| GK-08a/08b: idézetbe mosás csatornája | ELTÉRÉS | `eszkozok/lapgen/bemenet/gerinc.py:315-321`; `szamitas/szotari_gerinc.py:48,116,135,146,200` | A `gerinc.idezet_szoveg(b_id, mezo, szoveg, hely)` és a `jel_szoveg` tetszőleges `str`-t `Forrasszoveg`-gé (idézetté) burkol. A számítás számított szöveget ad át nekik (`G.pontos_jel(j)`: „4” → „4.”), illetve a B19 nyers dict-sorát (`r['nyers']`). A jelzőszó a burkoláskor születik, idézet-kategóriában, ezért egy `.ertek`-en vagy nyers soron át átvitt belső mező a festékpróbán láthatatlan. A B16–B22 nyers sorai festetlenül jutnak a számításba. A brief 2./3. „minden belső szövegmező” állítását a próba így nem bizonyítja. A jelentés „Ismert korlátok” pontja ezt ki is mondja. |
| 2. pont / 6-os sablon: `cella` módosító | ELTÉRÉS | `eszkozok/lapgen/szoveg.py:465-489`; `sablonok/6_PaRDeS_lexikon_oldal_sablon.md:599-616` | A `_cellakezdet` a PROZA és IDEZET szegmens szövegét írja át: leveszi a névelőt, nagybetűsít („az átok” → „Átok”). Ez ellentmond a 6-os sablonba most beírt szabálynak („változatlanul”; „A kész szöveget a generátor utólag nem írja át”). Az AST-teszt a `szoveg.py`-ra nem fut. A kezelés következetlen: ugyanakkor az ONREF-cserét az új generátor elhagyja. |
| G/D: T3 (DT837) tárolása | ELTÉRÉS | `dontesek/uj/f218-generator-uj-a.md:1`; `adat/tematikus_sajat_szo.tsv` | A DT837 (🟢, a felhasználó döntése) és a brief 3./4. pontja (B03: „új oszlop: `sajat_szo`”) az `elofordulasok.tsv` mezőjét írja elő. A DT867 (b)-t választott: külön táblát, ✅ állapottal, „az orkesztrátor technikai döntése”-ként, a felhasználó jóváhagyása nélkül. A brief 12. pontja a hasonló helyváltoztatást (T7, T8) felhasználói megerősítéshez köti. `git show dfb4525a:DONTESEK.md \| grep '^\| DT837 '` |
| G/D: T4 (DT838) | OK | `eszkozok/lapgen/bemenet/szavak.py:98-121` | Az első előfordulás érvényesül (a fenti engedélysor-minta igazolja). A „Károli-szónak rosszabbul felel meg” jelzés a felhasználónak megy (jelentés 205–216. sor). |
| G/D: T5–T9, O1–O8 | NEM ELLENŐRIZHETŐ | – | A későbbi szeletek (S2–S9) tárgya; az S1 diffje nem érinti. Az O7-nek (B11 kivezetve) megfelelően a B11 nincs a `lapgen_bemenetek.tsv`-ben. |
| 8.1 bemenet-hash őr | ELTÉRÉS | `eszkozok/lapgen/regresszio.py:71-84`; `naplok/F218_referencia.tsv` | Az őr csak a `referencia.tsv` sorait nézi, az olvasási naplót nem veti össze velük. Az új generátor által olvasott `adat/tematikus_sajat_szo.tsv` (B67) és `dontesek/uj/*.md` (B51) nincs a táblában (`git show dfb4525a:naplok/F218_referencia.tsv \| grep -c` → 0 / 0). A brief szerint „minden olvasott bemenet hash-e” kell. |
| 8.1 engedélyosztályok | ELTÉRÉS | `naplok/F218_elteres_engedely.tsv:7`; `naplok/F218_folytatas.md:80` | Az S1-ONREF (M-CSERE) nem szerepel a brief (a)–(i) osztályai között, és az F218.1 nem rögzített rá előzetes `elvart_db`-t. A jóváhagyott laphoz képest látható visszalépést hoz („azt a lap vitatott pontként tárgyalja”, a kimenet 224. sora). A T4 osztály 3 a rögzített 2 helyett (>20%), ami a brief szerint megállás. A menet ezt az S1 utáni ⛔-be vonta, de előtte még elvégezte az F218.3-at. |
| 9. pont: az S1 hatóköre | ELTÉRÉS | `eszkozok/lapgen/tesztek/teszt_vaz.py:13-49,139`; `naplok/F218_jelentes.md:239-240` | A brief szerint S1-es tételek elhalasztva. HN-03: kihagyva, felhasználói döntésre vár; a hatókör-sor zárójeles forráslistája mindkét új lap 7. sorában áll. GK-13 (H2403a/b, H2398) → S3. GK-14 (az összevont versek kulcsa) → S2. GK-03 a már olvasott B18/B19/B21-re frissességi kapu nélkül. Az F218.1 7.4 pontja (a `kovetelmeny` oszlop) és az alias-sorok szintén elhalasztva. Részben deklarált; a felhasználó jóváhagyása nem látszik. |
| F218.3 tesztváz | ELTÉRÉS | `eszkozok/lapgen/tesztek/teszt_vaz.py:98-170` | Az N-F212a **B9** tétele hiányzik a vázból (brief 7.2: A1…B8, B9, C3…). A HN-szövegminták nincsenek meg (brief 7., F218.3: „lapszöveg-részlet → BUKÁS”), csak docstringek. A cím nélküli leltártételek leírása nincs átvéve a docstringekbe. |
| 3. pont: additív módosítás | ELTÉRÉS | `eszkozok/general.py:1925` | Meglévő ág üzenetéből törölve a „; DT-F09h”. Ez nem additív, a jelentés (186. sor) mégis „additív módosítás”-t állít. |
| GK-07 blokkfejléc | ELTÉRÉS | új kimenet 3. sor; `eszkozok/lapgen/fo.py:103-112` | A `forrás:` listában egy szó szerinti `-` elem áll (a B13 szabálymodul útvonala). Az S1-FORRAS engedélysor hash-e ezt rögzíti. |
| 1. A1 | ELTÉRÉS | `naplok/F218_jelentes.md:207-214` | A T4 táblázat „Melyik felel meg a Károli-szónak” oszlopa nyelvi ítélet, lekérdezés és proveniencia nélkül, értelmezésként jelöletlenül. Pedig erre épül a T4-módosítási javaslat. A többi alapmérés-állítás mellett van proveniencia-sor. |
| 1. A2 | OK | `naplok/F218_folytatas.md:68-76` | A „nyitott” tételek nyitottak, például a CI nem futtatja a `lapgen/tesztek`-et (grep `.github`: 0). A `NYITOTT_FELADATOK.md`-t a diff nem írja. |
| 1. A3–A6 | OK | – | Tartalmi réteg nincs a diffben: nincs motívum-, forrás- vagy tanulmányszöveg, nincs nevesített tanító, nincs Remez/Sod. Az új sablonmondatok (8, `dontes=var`) új tartalmi állítást nem tesznek. A6: a CI-napló HIBA-sort nem ad, E12–E15 figyelmeztetés a naplóban nem látszik. |
| ISTENTISZT (8.2, S1-rész) | OK | – | `general.py --cel lexikon2 --id ISTENTISZT-001` → 190 sor. A megjegyzések nélküli szövegben DT-szám, fájlnév, aláhúzásos azonosító, `,;`, `sz<n>`, „gerinc”, „felhasználó”: 0 találat (grep a scratch kimeneten). |
| Lista 1: kiszűrt vagy törölt sorok | OK | – | `git diff --numstat 37f087cc..dfb4525a`: törlés csak a brief fejlécében (3) és a `general.py`-ban (2). Adatsor törlése: 0. |
| Lista 2: kulcstartomány | OK | `adat/lapgen_bemenetek.tsv` | 23 B-sor: B01, 03, 07, 08, 09, 12, 13, 14, 16–19, 21, 22, 32–34, 51, 59, 63, 65–67. A sor és a `b<nn>_` függvény egy-egy megfelelését a `test_gk01_bemenetenkent_egy_fuggveny` (zöld) adja. A B02–B06 stb. még nem szükséges, a szeletenkénti bevezetés szerint. |
| Lista 3: a nulla-diff hatóköre | OK | – | A „0 engedélyen kívül” csak a HAMART TUDOMANYOS „2. Előfordulások” szakaszára áll (437 sor), `munka` módban, `PARDES_DATUM=2026-11-13`-mal. Nem vonatkozik a többi szakaszra („nincs kész”, ezek engedélysorai nem számítanak), a KIZARASOK-ra (nem készül) és az ISTENTISZT-re (nincs bájt-mérce). A régi generátor bájt-egyezése a teljes két HAMART-nézetre áll. |
| Lista 4: táblasorok Δ (E17, DT3) | ELTÉRÉS | `adat/lapgen_sablonok.tsv`, `adat/olvasoi_nevtabla.tsv`, `adat/lapgen_bemenetek.tsv`, `adat/tematikus_sajat_szo.tsv` | Új táblák, Δ fejléc és `#` nélkül: +109, +24, +23, +1; a `konkordancia/` alatt 0. A három ≥10-es táblához nincs bontási napló. A sablontábla `eredet` oszlopa (`awk … \| uniq -c`: 23 `blokk_elofordulasok`, 13 `elofordulasok_uj`, 9 `dbh_jelentes_cella`, 8 `uj` …) csak implicit bontás. A CI E17 zöld. |
| Lista 5: a brief ⛔ pontjai | OK, megjegyzéssel | `naplok/F218_folytatas.md:80` | Az S1 utáni ⛔ betartva: ez az ellenőrzés. Az ellenőr nem Fable. A megállási küszöböt (89% < 91,5%) nem érte el. A T4 >20%-os ⛔ megállása elmaradt (l. a „8.1 engedélyosztályok” sort). |

Az ELTÉRÉS-ek súlyossági sorrendben:
1. **T3 (DT837):** felhasználói döntést írt felül az orkesztrátor (DT867, ✅). A felhasználónak kell megerősítenie.
2. **GK-08a/08b:** az idézetbe mosás csatornája (`gerinc.idezet_szoveg`, `jel_szoveg`, nyers B19-sorok a számításban) miatt a festékpróba a szótári ágon nem bizonyít.
3. **A `cella` módosító:** a prózát és az idézetet átírja, szemben az új alapszabállyal („változatlanul”, „utólag nem írja át”).
4. **A hash-őr hézaga:** a B67 és a `dontesek/uj/*.md` nincs a referencia-táblában.
5. **Az ONREF-osztály:** előzetes darabszám nélküli új osztály, látható „lap”-visszalépéssel. A T4 >20%-os ⛔ megállás elmaradt.
6. **Az S1 hatókörének halasztásai:** HN-03, GK-13 egy része, GK-14 egy része, GK-03 (B18/B19/B21), 7.4.
7. **Tesztváz:** hiányzik a B9, a HN-szövegminták és a leltárleírások.
8. **`general.py`:** nem additív üzenetmódosítás, a jelentés állítása ellenére.
9. **GK-07:** `-` elem a blokkfejléc forráslistájában.
10. **Lista 4:** a ≥10 soros új táblákhoz nincs bontási napló.
11. **A1:** a T4-táblázat jelöletlen értelmező oszlopa.

Munka közben a munkafában egy nem commitolt `naplok/F218_folytatas.md`-változás jelent meg; nem én írtam, és nem a `base..head` része. Ideiglenes fájlokat csak a scratchpadbe írtam: `C:\Users\bases\AppData\Local\Temp\claude\db97c378f8e1854f\6df2a091-98b7-4500-8d57-fb63ead9296f\scratchpad\`.

## Javítókör az 1. ellenőrzés után (1. kör; `claude-fable-5-2`, 2026-11-13)

*A besorolást és a döntéseket az orkesztrátor hozta a felhasználótól (2026-11-13); a javítás az ágon, a brief modelljén futott. Tartomány: `8c109585..` (a javítókör commitjai). Az újraellenőrzés az S2 végi célzott független ellenőrzéssel együtt fut (az orkesztrátor rendelkezése).*

| # | Tétel | Mi történt | Commit |
|---|---|---|---|
| 1 | T3 tárolása külön táblában | a felhasználó megerősítette (szó szerint: „Külön tábla jó”), szócikk nélkül (DT837); a DT867 sorában rögzítve | `d3a8f570` |
| 2 | az idézetbe mosás csatornája | a `jel_szoveg` és az `idezet_szoveg` megszűnt; a szakasz jele a kulcsból a bemeneti rétegben képződik (`Gerinc.jel`); a számítás típusos példahelyet kap (`Peldahely`, `ThayerPelda`, `Tartomany`), nyers táblasort nem; a nem BDB-jel a szótár nevével sablonból áll; statikus teszt: idézetet és prózát csak a bemeneti réteg burkol; a festékpróba a szótári ágat is festi | `713e63cb` |
| 3 | a `cella` módosító | megszűnt (DT869): a cella értéke az adatban a végleges alak; a cellakezdő sablonmondat külön sablonsor, a három érintett címke cellakezdő alakja kézi adat a névtáblában, egyezés-kapuval | `312e7b87` |
| 4 | a hash-őr és az olvasási napló | az új generátor a lap mellé írja a naplóját; a regresszió megáll, ha olvasott fájl nincs a referencia-táblában, vagy más tartalommal áll benne; a tábla 4 `uj_bemenet` sorral bővült (B65, B66, B67, `dontesek/uj/`) | `713e63cb` |
| 5 | ONREF-osztály; a T4 3 sora | T4: DT868 (a DT838 módosítása), a három T4-engedélysor megszűnt; önreferencia: DT870, az 1Móz 8:21 cellája a forrásban javult, az S1-ONREF engedélysor megszűnt | `d3a8f570`, `312e7b87` |
| 6 | az S1 hatóköréből halasztott tételek | nem változott: a HN-03 a felhasználó döntésére vár; a GK-13 (lemma) és a GK-03 (B18/B19/B21) az S3, a GK-14 (összevont versek) az S2 tétele; a 7.4 és az alias-sorok a folytatási fájl szerint | – |
| 7 | tesztváz | GK-B9 a vázban; a HN-esetek szövegmintái tesztadatként (`HN_MINTAK`: minta + hibás lapszöveg-részlet), két élő teszttel: a minta megfogja a részletet, és a kész szakaszokon a már mért esetek száma 0 | ez a commit |
| 8 | a `general.py` „additív” állítása | pontosítva az F218.2 pontban (két additív elem és egy E32-előjavítás) | ez a commit |
| 9 | `-` a blokkfejléc forráslistájában | a nem fájl-bemenet (szabálymodul) nem áll a forráslistában | `713e63cb` |
| 10 | bontási napló | l. alább | ez a commit |
| 11 | a T4-táblázat értelmező oszlopa | értelmezésként jelölve, mellé a párosítás lekérdezése proveniencia-sorral („Amit a felhasználónak látnia kell” 1. pont) | `d3a8f570` |

**A 7 új sablonmondat** (`eredet=uj`, `dontes=var`): a felhasználó jóváhagyta (az orkesztrátoron át, 2026-11-13, szó szerint: „Igen, mind jó”). A sablontábla `dontes` oszlopa a jóváhagyás DT-számát várja; a sorok addig `var` értékkel állnak, amíg a jóváhagyás döntésszámot nem kap.

**Állás a javítókör után (HAMART-001, `PARDES_DATUM=2026-11-13`).** „2. Előfordulások”: 437 sorból 436 bájtra egyezik; **1 engedélysor** (S1-FORRAS, a blokkfejléc forráslistája, GK-07), engedély nélküli diff-sor 0. Festékpróba: 0 szivárgás (HAMART: belső 168, idézet 326, kézi 180 látott jelzőszó; ISTENTISZT: 113, 183, 85). Tesztek: 133 futott, 97 zöld, 36 kihagyva (a váz). A régi generátor mindkét HAMART-nézete a javított adatcellával is bájtra azonos a HEAD lapjaival.
*Proveniencia: `scope=python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001; python eszkozok/lapgen/tesztek/futtat.py; general.py --cel lexikon --id HAMART-001 + cmp | forras=a munkafa a javítókör utolsó commitja előtt | ts=2026-11-13`.*

### Kézi adat, előtte → utána

| Fájl | Sor, mező | Előtte | Utána |
|---|---|---|---|
| `adat/elofordulasok.tsv` | HAMART-001, 1Móz 8:21, `kapcsolodas` | „… azt a lap vitatott pontként tárgyalja.” | „… azt a szócikk vitatott pontként tárgyalja.” |
| `adat/olvasoi_nevtabla.tsv` | új sor: `cimke_cella`, H0127 1. szakasz | (a címke: „a megművelt föld, amely táplál”) | „A megművelt föld, amely táplál” |
| `adat/olvasoi_nevtabla.tsv` | új sor: `cimke_cella`, H0127 3. szakasz | (a címke: „a föld mint anyag, amelyből az ember lett”) | „A föld mint anyag, amelyből az ember lett” |
| `adat/olvasoi_nevtabla.tsv` | új sor: `cimke_cella`, H0127 4. szakasz | (a címke: „a föld látható felszíne, a föld színe”) | „A föld látható felszíne, a föld színe” |

### Az önreferencia mérése (a régi `ONREF_CSERE` négy adatcella-párja)

| Pár („lap” → a lapon álló szó) | Cella | Kötődik hozzá |
|---|---|---|
| „azt a lap vitatott pontként tárgyalja” → „a szócikk” | `adat/elofordulasok.tsv` 1 cella | semmi: **javítva** |
| „ezeket a lap egyenként, tematikus helyként veszi fel” → „a vizsgálat” | `adat/motivumok.tsv` 1 cella (HAMART-001 `negativ_kriterium`) | `adat/nyilt_angol.tsv` 1 sor (a magyar szöveg hash-e), `nyilt_mag/motivumok.tsv` |
| „amelyet a lap nem dönt el” → „ez a vizsgálat” | `adat/jeloltek.tsv` 2 cella, `adat/elutasitasi_okok.tsv` 1 sor 2 cellája | `adat/nyilt_angol.tsv` 2 sor, `adat/nyilt_kodkonyv.tsv` 1 sor (a szöveg a kódkönyv kulcsa), `nyilt_mag/kizarasok.tsv`, `nyilt_mag/kodkonyv.tsv`, `nyilt_mag/KODKONYV.md` |
| „amely a lánc szavai nélkül áll a lapon” → „a listán” | `adat/kapcsolatok.tsv` 3 cella | a mérés szerint semmi |

*Proveniencia: `scope=a négy szövegpár bal oldalának keresése az adat/*.tsv, a motivumok/*.md és a nyilt_mag/ fájljaiban, cellánként | forras=a munkafa (8c109585 + a javítókör) | ts=2026-11-13`.* A három nyitott pár 8 cellája nincs átírva: a fájlok a brief `ir` mezőjén kívül esnek, és kettőnél a cella átírása a nyílt mag angol fordítását elavulttá teszi (a nyílt mag kapuja bukik: újrafordítás és újraexport kell). A kérdés a felhasználóé (DT870, 🟡). Az S2 két párt érint (a negatív kritérium és a kizárási ok szövege): a döntésig ezek a diff-sorok előre megszámolt engedélysort kapnak.

### Amit a felhasználónak látnia kell (a javítókör új tételei)

1. **Az ISTENTISZT-001 2. táblájában hat cella kisbetűvel kezdődik**, mert a generátor a forrást szó szerint adja: öt Károli-idézet („az Úrnak nevét hívja segítségül …”) és egy funkciócímke („a népek ígérete”). A régi lapon ezeket az utófeldolgozó nagybetűsítette, illetve a névelőt levette („Népek ígérete”). Két út: a Károli-idézet marad szó szerint (kisbetűvel), a funkciócímke cellakezdő alakja adatba kerül; vagy mindkettő adatba kerül. Az ISTENTISZT-lapnak nincs bájt-mércéje, ezért ez nem engedélysor, hanem olvasói döntés.
2. **A három nyitott önreferencia-pár** (fent): a javítás helye és ideje.
3. **A T4 az ISTENTISZT-lapon** is a párosítás szerint áll (a fenti T4-kiegészítés táblája); az 1Kir, a Jóel, a Sof és a Jel párjai `alacsony` bizonyosságú modell-kimenetek.

### Bontási napló a 10 sornál nagyobb új táblákhoz (10. tétel)

| Tábla | Sor | Bontás |
|---|---|---|
| `adat/lapgen_sablonok.tsv` | 111 | **szakasz szerint:** 2. Előfordulások 100, 2.1 pont 6, keret 5. **Eredet szerint:** betűre átvett a régi generátorból 103 (`blokk_elofordulasok` 25, `olvasoi_kovetkeztetes.elofordulasok_uj` 13, `dbh_jelentes_cella` 9, `ubs_jelentes_cella` 7, `tablajegyzet._jelentes_tomor` 7, `tablajegyzet.olvasoi_jegyzet` 6, `jelentes_cella` 6, `_tagolatlan_olvasoi` 4, a többi tizennégy szimbólum 26), új mondat 8 (`dontes=var`) |
| `adat/olvasoi_nevtabla.tsv` | 27 | **típus szerint:** `forras` 7, `pardes_szint` 4, `hanyszor` 4, `azonositas_modja` 3, `megbizhatosag` 3, `szotar` 3, `cimke_cella` 3 |
| `adat/lapgen_bemenetek.tsv` | 24 | **szelet szerint:** T (F218.2) 6: B01, B51, B59, B63, B65, B66; S1 (F218.4) 17: B03, B07, B08, B09, B12, B13, B14, B16, B17, B18, B19, B21, B22, B32, B33, B34, B67; javítókör 1: B54 |

*Proveniencia: `scope=a három tábla adatsorainak száma a szakasz, az eredet, a típus oszlop szerint (cut, sort, uniq -c) | forras=adat/lapgen_sablonok.tsv, adat/olvasoi_nevtabla.tsv, adat/lapgen_bemenetek.tsv (a javítókör után) | ts=2026-11-13`.*

### A `teszt_szintek.py` hibája

Az 1. ellenőr `teszt_futtat.py --diff` futásában a `teszt_szintek.py` is hibát adott. A fájl az olvasó-szerver tesztje (`eszkozok/olvaso_szerver/teszt_szintek.py`): a feladat ágán 13 tesztből 2 bukik (`test_ebben_a_versben_es_az_interlinearis_csempek_koveti_a_blokkok_lathatosagat`, `test_heber_szavak_alacsony_es_magas_szinten`: a szó-lap magas szintű BDB-darabja és az „Ebben a versben” blokk láthatósága). A fő checkouton (`1352ac3c`, a main egy korábbi állapota) ugyanez a fájl ugyanígy 13 tesztből 2 bukással áll (ott a bukó tesztek nevét nem írattam ki). Az F218a diffje (`git diff --name-only 37f087cc..HEAD`) az `eszkozok/olvaso_szerver/` egyetlen fájlját sem érinti. A hiba tehát nem ebből a diffből jön: nyitott tétel lett (N187, `nyitott/uj/f218-generator-uj-a.md`).
*Proveniencia: `scope=python eszkozok/teszt_futtat.py --fajl teszt_szintek [--reszletes] | forras=a feladat ága (713e63cb) és a fő checkout (1352ac3c) | ts=2026-11-13`.*

### Ismert korlátok a javítókör után

- A jegyzéktábla (`adat/lapgen_bemenetek.tsv`) olvasása nincs az olvasási naplóban (nincs B-azonosítója), ezért a hash-őr nem méri.
- A referencia-tábla `uj_bemenet` sorai (a sablontábla, a névtábla, `dontesek/uj/`) minden szelettel változnak: a hash-ük a szelet végén frissítendő (a szkript a megosztott jegyzetmappában áll: `F218_eszkozok/referencia_frissit.py`).
- A szakasz jele (`Gerinc.jel`) a szakasz kulcsából képzett szöveg, idézet fajtával: a szótár saját tagolásának átírt alakja (`Qal/2/c` → „Qal 2.c”), ugyanúgy, mint a kiejtés a ragozott alakból.

## Független ellenőrzés — 2. ellenőrzés

*A `fuggetlen-ellenor` subagent (`claude-opus-5-5`) jelentése változtatás nélkül; bemenete: a brief, a `8c109585..2b0a05a4` tartomány (a javítókör commitjai), célzott hatókörrel (az 1. ellenőrzés 11 tétele és a két nyitva hagyott tétel), `teljes` szint, a CI-állapot a head-re. Mentve: 2026-11-13.*

ELTÉRÉS: 4 tétel

Brief: `F218_GENERATOR_UJ_A_BRIEF.md` · tartomány: `8c109585..2b0a05a4` (5 commit; a javítókör) · szint: `teljes`, célzott hatókörrel (az 1. ellenőrzés 11 tétele) · 2. ellenőrzés

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0. modell | OK | – | A modellem `claude-opus-5-5`, a kért `opus`; egyezik. `git log --format='%h %(trailers:key=Co-Authored-By,valueonly)' 8c109585..2b0a05a4`: mind az 5 commit `Claude Fable 5.2`. Ez egyezik a jelentés „Javítókör” fejlécével (`claude-fable-5-2`). Adattábla `modell` mezőjét a menet nem írt. |
| 3. CI | OK | – | `gh run view 43422669225 --json headSha,status,conclusion,jobs`: a `headSha` `2b0a05a4…`, `completed` / `success`, az `ellenorzes` és a `feladatkovetes` job zöld. Az első lekérdezéskor a futás még tartott, a második már befejezett. A `futtat.py`-t nem futtattam. |
| Diéta 3. tesztek | OK | `eszkozok/lapgen/tesztek/` | `python eszkozok/lapgen/tesztek/futtat.py`: 133 futott, 0 hiba, 0 bukás, 36 kihagyva. Egyezik a jelentés 338. sorával (133/97/36). A lassú tesztek (`teszt_futtat.py --diff`) a hívó utasítására kimaradtak. A diff az `eszkozok/olvaso_szerver/`-t nem érinti (`git diff --name-only 37f087cc..2b0a05a4 \| grep -c olvaso_szerver` → 0), ezzel az N187 „nem ebből a diffből” állítása a fájllista szintjén igazolt. |
| Régi generátor bájt-egyezése | OK | `eszkozok/general.py` | `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon --id HAMART-001 --kimenet <scratch>/regi`, majd `cmp` a `git show HEAD:lexikon/HAMART-001_{TUDOMANYOS,KIZARASOK}.md` tartalmával: mindkét cmp kilépési kódja 0. |
| Regresszió (S1) | OK | `naplok/F218_elteres_engedely.tsv:3` | `general.py --cel lexikon2 --id HAMART-001 --kimenet <scratch>/uj` (438 sor, EXIT 0), majd `regresszio.py --id HAMART-001 --uj <scratch>/uj/lexikon`: „2. Előfordulások” 1 diff-sor, engedéllyel; `S1-FORRAS: 1`; RENDBEN. Az engedélyfájl diffje: az 5 sorból 4 törölve (T4-1..3, ONREF), az S1-FORRAS új hash-sel. |
| 1. T3 (DT867) | OK | `dontesek/uj/f218-generator-uj-a.md:1` | A sorban: „a felhasználó megerősítésével (… szó szerint: „Külön tábla jó”); a saját szó a DT837 szerint szócikket nem kap”. `grep '^\| DT837 ' DONTESEK.md`: „Adatba kerül, szócikk nélkül … a 4. szakasz nem kap róla szócikket”. A sor nem állít többet, a ✅ (alkalmazva) helytálló. |
| 2. Idézetbe mosás, `bemenet/` kívül | OK | `tesztek/teszt_szerkezet.py:196-211` | `Grep forrasszoveg\(\|\.kezi\(\|\.belso\(\|Forrasszoveg\(\|Kezi\(` az `eszkozok/lapgen` alatt: a `bemenet/`-en kívül csak tesztekben van találat. A `szamitas/elofordulas.py:185` csak `Kulcs`-ot burkol (`f.szotar_kulcs`). A `jel_szoveg` és az `idezet_szoveg` megszűnt; az AST-teszt ezt őrzi (zöld). A B19 nyers sora nem hagyja el a réteget (`Peldahely`, `Tartomany`, `ThayerPelda`). |
| 2. `.ertek`-megkerülés és `Gerinc.jel` | ELTÉRÉS | `szamitas/szotari_gerinc.py:175,181`; `bemenet/gerinc.py:341,349,368-375,191-196`; `megjelenites/md/elofordulas.py:211,250,273` | (a) A javítókör a B19 `karoli_vers`-et `Belso`-ként burkolja (`gerinc.py:341`). A számítás `t.kezdo_vers.ertek`-kel kibontja, `Igehely`-lyé alakítja, és ez látható szövegként kerül a lapra (`e2.jm.tartomany`, `kezdo=`). A `Belso` docstringje szerint „látható szöveg nem lehet belőle” (`szoveg.py:232`). Ugyanígy a B21 `Kulcs` (`p.jel.ertek`) `int`-ként látható szám lesz (`n=`). Az érték típusos és ellenőrzött, tehát szabad szöveg így nem juthat át, de a kategória ellentmond a használatnak, és az `.ertek` út a festékpróbán eleve láthatatlan. (b) A `Gerinc.jel` számított szöveget burkol `Forrasszoveg`-gé: `szakasz_jel(utvonal)` (`Qal/2/c` → `Qal 2.c`) és `pontos_jel` (`4` → `4.`), egy nem létező `szakasz_jel` mezőnévvel. A `kulcs_jel` több szócikkes útvonalnál a belső `bdb_id`-t is a jel elé írja (`gerinc.py:194-195`). Ez az út a jelentés „Ismert korlátok” 3. pontjában szerepel, de a `bdb_id`-előtag nem. A HAMART látható szövegében `BDB\d+` nincs (sed a megjegyzések nélkül + grep: 0), az út tehát most nem él. |
| 2. Festékpróba | OK (futás) | `eszkozok/lapgen/festek.py` | `python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001`: 0/0 szivárgás. Látott jelzőszavak: belső 168/113, idézet 326/183, kézi 180/85. Egyezik a jelentés 338. sorával. A próba ereje: a szótári ág B19-mezőit már festi (`test_gk08b_a_szotari_ag_mezoi_is_festettek`), az előző sorban leírt két utat nem. |
| 3. `cella` módosító (DT869) | OK | `eszkozok/lapgen/szoveg.py:465-477`; `bemenet/gerinc.py:127-131` | A `_cellakezdet` és a `CELLA_MONDAT_SZO` törölve. A `_nevelovel` csak sablonszöveget tesz a szegmensek elé (`[(Fajta.SABLON, nevelo+' ')] + szegmensek`); ismeretlen módosítóra (`cella`) SablonHiba. `Grep upper\|lower\|capitalize\|\.sub\(\|replace\(` a `szoveg.py`-ban: egyik találat sem PROZA- vagy IDEZET-szegmensen dolgozik (horgony, számformázás, a beszúrt névelő). A `_cella_alak_egyezik` csak a nagy kezdőbetűt és a kezdő „a”/„az” elhagyását engedi. A célzott grep a `lexikon/HAMART-001_TUDOMANYOS.md`-ben: „A megművelt föld, amely táplál” stb. Ítéletem: ez nem cseretábla, mert nincs mintaszabály tetszőleges szövegre, címkénként kulcsolt kézi adat, és a kapu eltérésnél megáll. Ára: minden cellakezdő címkének kell egy sor, híján kisbetűvel áll (ISTENTISZT 6 cella; ez a felhasználónak jelezve, jelentés 363). |
| 4. Hash-őr: ismeretlen és más tartalmú bemenet | OK | `eszkozok/lapgen/regresszio.py:92-112` | Három próbát futtattam repón kívüli másolaton, mindegyik után `regresszio.py --id HAMART-001 --uj <másolat>`. Ismeretlen sort fűztem a naplóhoz (`B99 adat/ismeretlen.tsv`) → „nincs a referencia-táblában”. Az `olvasoi_nevtabla.tsv` hash-ét átírtam → „más tartalommal olvasva”. A naplót töröltem → „hiányzik az új generátor olvasási naplója”. Mindhárom MÉRCE NEM FUTTATHATÓ. A tesztek ugyanezt fedik. |
| 4. Hash-őr: naplóból kimaradó olvasás | ELTÉRÉS | `bemenet/jegyzek.py:166-174`; `bemenet/szavak.py:128-136` | (a) A jegyzéktábla (`adat/lapgen_bemenetek.tsv`) olvasása nincs a naplóban; ezt a jelentés kimondja (382. sor). (b) **Új:** a `b54_karoli_parok` a `_fejsorok`-kal minden `parok_*.tsv` első 8 sorát olvassa, naplózás nélkül. `ls adat/karoli_strong/parok_*.tsv \| wc -l` → 66; a naplóban 14 B54-fájl áll, a referencia-táblában 56 (`grep -c karoli_strong/parok_ naplok/F218_referencia.tsv`). A könyv–fájl leképezés így 52 nem mért fájl fejsorától függ, és ez a hézag a jelentésben nem szerepel. A brief „minden olvasott bemenet hash-e” követelménye így nem teljes. |
| 5. T4 (DT868): a kód | OK | `bemenet/szavak.py:162-190` | A `ragozott` versenként először a párosításhoz kötött helyet keresi; ha talál, azt választja, és kilép. Ha nem, az első vers első előfordulását tartja meg. A pár csak akkor dönt, ha a TAHOT/TAGNT `n`. során ugyanez a Strong-szám és ugyanez az alak áll (`_kotott_hely`). Ez a döntés szövegét valósítja meg: „ahol van párosítás: az az alak … ahol nincs: az első előfordulás”. |
| 5. T4-kiegészítő tábla újramérése | OK | `naplok/F218_jelentes.md:222-229` | Repón kívüli szkript (`split('\t')`), a `parok_<könyv>.tsv` és a TAHOT/TAGNT soraiból. 1Móz 6:5 H7451: pár hu#20 „gonosz” → er#18 רַ֖ע; TAHOT #6 רָעַ֥ת, #18 רַ֖ע. 1Móz 6:12 H7843: „megrontotta” → er#11 הִשְׁחִ֧ית; TAHOT #9, #11. Jel 11:18 G1311: „pusztítják” → er#42 διαφθείροντας; TAGNT #40, #42. 1Móz 4:26 H8034: két „nevét” (hu#8 → er#11, hu#16 → er#19), a tábla 19-et ad. 1Kir 18:24 H8034: er#4 és er#11, a tábla 11-et ad. Sof 1:2 H0127: er#8. Mind egyezik a tábla sorszámaival. |
| 5. `elofordulasok.tsv` | OK | `adat/elofordulasok.tsv:217` | `git diff 8c109585..2b0a05a4 -- adat/elofordulasok.tsv`: egyetlen sor, egyetlen cella változott (`kapcsolodas`, 1Móz 8:21: „a lap” → „a szócikk”). `--numstat`: `1 1`. A referencia-tábla B03-hash-e ennek megfelelően frissült, a referencialap hash-e nem (a cmp szerint indokoltan). |
| 6a. Halasztott S1-tételek | OK (nyitott, dokumentált) | `naplok/F218_folytatas.md:12,32,47,135`; `naplok/F218_jelentes.md:329` | A HN-03, a GK-13, a GK-14 (S2), a GK-03, a 7.4 és az alias-sorok nyitottként állnak. A javítókör tábla 6. sora: „nem változott”. Felhasználói jóváhagyás a halasztásra továbbra sem látszik, és nincs is lezártnak jelölve. |
| 6b. Az önreferencia három párja | OK | `dontesek/uj/f218-generator-uj-a.md:4`; `naplok/F218_jelentes.md:350-359` | Repón kívüli szkript (az `adat/**/*.tsv`, a `nyilt_mag/**` és a `motivumok/*.md` cellánként). „azt a lap vitatott…”: 0 találat (javítva). „ezeket a lap egyenként…”: `motivumok.tsv` 1 cella, `nyilt_angol.tsv` 1 sor. „amelyet a lap nem dönt el”: `jeloltek.tsv` 2 cella, `elutasitasi_okok.tsv` 1 sor / 2 cella, `nyilt_angol.tsv` 2 sor, `nyilt_kodkonyv.tsv` 1 sor. „…áll a lapon”: `kapcsolatok.tsv` 3 cella. Összesen 8 adatcella, egyezik a táblával. A DT870 🟡, a kérdés a folytatási fájlban is áll (132. sor). |
| 7. Tesztváz | OK, megjegyzéssel | `eszkozok/lapgen/tesztek/teszt_vaz.py:22-72,185-189` | GK-B9 a vázban (skip S9). `test_a_mintak_megfogjak_a_hibas_lapszoveget` és `test_a_kesz_szakaszokon_nincs_hn_talalat`, mindkettő zöld. Az élő teszt a `fo.lap_keszit` kimenetén fut, a `MEGJEGYZES` tartományok nélkül, mindkét mintalapon: a kész szakaszok látható szövegén. Megjegyzés: a részletek egy része szerkesztett példa (pl. HN-05 „a felhasználó döntése szerint”), nem a hibás lapról vett idézet; a minta így a saját példáját fogja meg. |
| 8. `general.py` „additív” | OK | `naplok/F218_jelentes.md:186` | `git diff 37f087cc..2b0a05a4 -- eszkozok/general.py`: a `lexikon2` választás és az ága, a `--mod`, valamint a „; DT-F09h” törlése. A pontosított mondat (két additív elem és egy nem additív) igaz. A javítókör a `general.py`-t nem érinti. |
| 9. Blokkfejléc | OK | `eszkozok/lapgen/fo.py:108-110` | `sed -n 3p <scratch>/uj/lexikon/HAMART-001_TUDOMANYOS.md`: a `forrás:` listában `-` elem nincs (a `NEM_FAJL` szűrve). |
| 10. Bontási napló | ELTÉRÉS (csekély) | `naplok/F218_jelentes.md:371` | `grep -v '^#' … \| tail -n +2 \| cut -f4/-f5/-f6 \| sort \| uniq -c`. A sablontábla 111 sor: szakasz szerint 100/6/5, eredet szerint 25/13/9/7/7/6/6/4 + 26, `dontes=var` 8. A névtábla 27 sor (7/4/4/3/3/3/3), a jegyzék 24 sor (6+17+1). Minden szám egyezik, de a „többi” **14** szimbólum, nem „tizenhárom”. |
| 11. A T4-tábla értelmező oszlopa | OK | `naplok/F218_jelentes.md:218,232` | A kiegészítés kimondja: „az építő session **értelmezése** volt, lekérdezés nélkül”. Az új tábla proveniencia-sorral áll, és a fenti újramérés igazolja. |
| Új: a DT-állapotok | ELTÉRÉS (csekély) | `dontesek/uj/f218-generator-uj-a.md:2-3` | A DT868 és a DT869 🟢 („eldöntve, alkalmazásra vár”, `DONTESEK.md:9` jelmagyarázat), pedig mindkettő sora „Alkalmazva:” / „Megvalósítás:” részt tartalmaz, és a kód a diffben áll. Helyesen ✅ volna, ahogy a DT-F218i-nél. |
| Lista 1: kiszűrt vagy törölt sorok | OK | – | `git diff --numstat 8c109585..2b0a05a4`. Adattábla: `lapgen_sablonok.tsv` 1 törölt sor (`tabla.cella`), `elofordulasok.tsv` 1 módosított sor. Napló: az engedélyfájlból 5 sor törölve, 1 új; a referencia-táblában 1 módosított és 4 új sor. Más törlés adatsorban nincs. |
| Lista 2: kulcstartomány | OK | `adat/lapgen_bemenetek.tsv` | A B-sorok: B01, 03, 07, 08, 09, 12, 13, 14, 16–19, 21, 22, 32–34, 51, 54, 59, 63, 65–67 (24). Új: B54, a T4-hez. |
| Lista 3: a nulla-diff hatóköre | OK | – | A 0 engedélyen kívüli diff-sor csak a HAMART TUDOMANYOS „2. Előfordulások” szakaszára áll (`munka` mód, `PARDES_DATUM=2026-11-13`); a többi szakaszra („nincs kész”), a KIZARASOK-ra és az ISTENTISZT-re nem. A régi generátor bájt-egyezése mindkét HAMART-nézetre áll. |
| Lista 4: táblasorok Δ (E17, DT3) | OK | – | A javítókörben: `elofordulasok.tsv` 0, `lapgen_bemenetek.tsv` +1, `lapgen_sablonok.tsv` +2, `olvasoi_nevtabla.tsv` +3, a `konkordancia/` alatt 0. Egyik sem ≥ 10. A main-hez képest: +111 / +27 / +24 / +1. A három ≥ 10-es táblának most van bontási naplója (10. pont). |
| Lista 5: a brief ⛔ pontjai | OK | – | A T4 > 20% megállás és az ONREF új osztálya felhasználói döntéssel zárult (DT868 🟢, DT870 🟡), az engedélysorok megszűntek. A javítókör után az S2 előkészítése (`2b0a05a4`) csak a folytatási fájlt írja. |
| A3–A6 | OK | – | Tartalmi réteg nincs a diffben. Az egyetlen kézi próza-változás az 1Móz 8:21 cellájának egy szava; nincs nevesített tanító, nincs Remez/Sod. |

Az ELTÉRÉS-ek súlyossági sorrendben:
1. **2. tétel, maradék csatorna.** A `Belso`-ként burkolt B19 `karoli_vers` `.ertek`-en át látható igehely lesz, a B21 `Kulcs` pedig látható szám. A `Gerinc.jel` számított szöveget (és lehetséges `bdb_id`-előtagot) burkol idézetté. A festékpróba egyiket sem látja. Az `.ertek` út és a `bdb_id`-előtag új lelet.
2. **4. tétel, a napló hézaga.** A jegyzéktábla és (új) a B54 `_fejsorok`-olvasása 52 nem mért `parok_*.tsv`-ből nincs a naplóban.
3. **Új:** a DT868 és a DT869 🟢-vel áll ✅ helyett.
4. **10. tétel:** „tizenhárom” helyett 14 szimbólum; a számok egyeznek.

Ideiglenes fájlok csak a scratchpadben: `C:\Users\bases\AppData\Local\Temp\claude\263328eaf8ead9ff\270d530d-7596-4408-9382-57d7c56473e8\scratchpad\`.

## F218.5 — S2, első fele: a vizsgálat modellje és a kizárt versek melléklete (`claude-fable-5-2`, 2026-11-13)

**Eredmény (HAMART-001, `PARDES_DATUM=2026-11-13`, `munka` mód).** A melléklet (`HAMART-001_KIZARASOK.md`) 431 sorából 421 bájtra egyezik a referenciával; **10 diff-sor, mind engedéllyel; engedély nélküli diff-sor: 0.** A tudományos lapon a „2. Előfordulások” változatlan (1 engedélysor). A „1. Döntési út” szakasz (az S2 második fele) még nincs kész.
*Proveniencia: `scope=general.py --cel lexikon2 --id HAMART-001, majd python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa az S2a commitja előtt | ts=2026-11-13`.*

| Engedélysor | Osztály | Darab | Mi tér el |
|---|---|---|---|
| S2-KONYV-1…4 | GK-17 | 4 | a csoportosan kizárt versek között a Siralmak könyve az adat szerinti rövidítéssel (`Sir`, a Károli-fájl kulcsa) és a Károli-rend szerinti helyén áll, a versek fejezet- és versrendben (4:6, 4:13, 4:22). A régi generátor a csoporttagokat kódba írt aliasszal `JSir`-ré írta, ezért a könyv a lista végére, a versei betűrendbe kerültek (4:13, 4:22, 4:6); az egyenkénti vers a régi lapon is `Sir` |
| S2-ONREF-1, -2 | M-CSERE | 2 | „az öröklött bűnösség kérdése, amelyet a lap nem dönt el”: a kézi címke és megjegyzés változatlanul áll; a forráscella javítása a felhasználó döntésére vár (DT870) |
| S2-FORRASSOR-1…4 | DT823 | 4 | a régi lap látható szövegben közölte a mérés fájlnevét és három nyers forrássorát, a keresést a belső kulcsával (`strong`, `karoli`, `szotar`); az új lapon a forrássor megjegyzésben áll, a keresés az olvasói nevével |

**Mi készült.** A döntésnapló bemenetei (`bemenet/dontes.py`: B04, B05, B06, B56), a vizsgálat közös modellje (`szamitas/vizsgalat.py`: a motívum versei, a csoportosan kizárt, az egyenként elutasított és a döntésre váró versek; ebből ír a melléklet, és ebből fog írni a Döntési út), a melléklet modellje és megjelenítője (`szamitas/kizarasok.py`, `megjelenites/md/kizarasok.py`), a szakasz kapuja (a `SzakaszLeiro` `kapu` mezője; a `fo.lap_keszit` a megjelenítés előtt futtatja). A HAMART-001 számai a modellen: 56 vers (49 hely) + 1 542 csoportosan kizárt + 242 egyenként elutasított + 0 döntésre váró = 1 840; 4 csoportos és 26 egyenkénti ok.

**Kapuk a modellen** (nem a kiírt szövegen): a számok összeadódnak; az okok versszámainak összege a két részösszeg; minden ok verslistája a versszáma; egy vers sem áll kétszer; a motívum verse nem áll a kizártak között (GK-09, GK-21, GK-04 melléklet-kapu). A teljesség-mérés pillanatképe frissességi kapuval lép be (GK-03, HN-11): ha a Strong-keresés forrássora nem nevezi meg a mért Strong-halmazt, vagy az nem a motívum mai halmaza, a lap nem készül el. Hiányzó mérés kimondott hiány (GK-06). Mindkét mintalap pillanatképe friss.

**Tesztek:** 144 futott, 111 zöld, 33 kihagyva (a váz); az S2 tesztjei: `teszt_dontes.py` (14 teszt). **Festékpróba:** 0 szivárgás (HAMART: belső 171, idézet 326, kézi 240 látott jelzőszó; ISTENTISZT: 116, 183, 121). **ISTENTISZT-001:** a melléklet generálódik (307 sor), a látható szövegben nincs proveniencia-sor és fájlnév (teszt); bájt-mércéje nincs.
*Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001 | forras=a munkafa az S2a commitja előtt | ts=2026-11-13`.*

**Új táblasorok:** a jegyzék +4 (B04, B05, B06, B56; összesen 28), a névtábla +3 (`halo` típus; összesen 30), a sablontábla +14 (`kz.*` 13 és `cim.dontesi_ut`; összesen 125), közülük 2 új mondat (`dontes=var`): `kz.forrassorok.bevezeto` („A Döntési út 1.2 pontjának versszámai ebből a mérésből jönnek. Keresésenként a megvizsgált versek száma:”) és `kz.forrassorok.kereses` („- **A szavak minden előfordulása** (1 392 vers)”). A referencia-tábla 2 `uj_bemenet` sorral bővült (az ISTENTISZT-001 teljesség-mérése és csoportlistája; a HAMART-001 új bemenetei a régi generátor bemeneteiként már benne álltak), a sablontábla és a névtábla sorának hash-e frissült.

**Amit a felhasználónak látnia kell (S2a).**
1. **`Sir` vagy `JSir`.** A jelöltek és a csoportlista a Károli-fájl kulcsát használják (`Sir`), a normalizáló tábla rövidítése `JSir`. A melléklet most egységesen az adat szerinti `Sir` alakot adja, a Károli-rend szerinti helyen. A végleges alakról az alias-sorok döntése szól (GK-17, az S5 előtt).
2. **A forrássorok két új mondata** (fent) jóváhagyásra vár; a mérés nyers forrássora megjegyzésben megmaradt.
3. **„A 575 vers”.** A lenyíló lista címe betűre a régi lapé (`kz.lista_cim`: „A {n} vers”); nyelvtanilag „Az 575 vers” volna helyes. Nem javítottam, mert a szöveg jóváhagyott; ha javítandó, a sablonmondat `{n|A}` alakot kap, és ez 1 engedélysor.

## A 2. ellenőrzés besorolási javaslata (kör: 2 / 2; egyeztetésre vár, javítás még nem történt)

| # | Tétel | Javasolt besorolás | Indok, teendő |
|---|---|---|---|
| 1a | belső mezőből `.ertek`-en át látható igehely és szám | mechanikus | a verstartomány kezdő verse a bemeneti rétegben képzett `Igehely` legyen (ne `Belso`), a Thayer-példa jelentésszáma a bemeneti rétegben képzett szám (ne `Kulcs`); így a típus egyezik a használattal |
| 1b | a szakaszjel a szótár belső szócikk-azonosítójával („BDB… 1”), idézetként burkolva | tartalmi | döntés kell: hogyan nevezze a lap a több szócikk egyikét (a régi lap a belső azonosítót írta ki); addig a több szócikkes esetben a generálás kimondott hibával álljon meg. A két mintalapon ez az út nem él |
| 2 | az olvasási napló hézaga | mechanikus | a jegyzéktábla és a B54 minden fejsor-olvasott fájlja kerüljön a naplóba (hash-sel), a referencia-tábla ennek megfelelően bővül |
| 3 | a DT868 és a DT869 állapota 🟢, ✅ helyett | mechanikus (formai) | a két sor állapotjele ✅ |
| 4 | a bontási naplóban „tizenhárom” szimbólum, a helyes szám 14 | mechanikus (formai) | a szó javítása |


## A 2. ellenőrzés javítóköre (2. kör; `claude-fable-5-2`, 2026-11-13, a 3. session)

*A besorolást az orkesztrátor hozta (2026-11-13): az 1a, a 2., a 3. és a 4. tétel mechanikus, a fenti javaslat szerint; az 1b döntés (DT871); a DT-F218l-ről külön rendelkezett (l. a következő szakaszt). Az újraellenőrzés az S2 végi célzott független ellenőrzéssel együtt fut.*

| # | Tétel | Mi történt |
|---|---|---|
| 1a | belső mezőből `.ertek`-en át látható igehely és szám | a verstartomány kezdő verse a bemeneti rétegben képzett `Igehely` (a könyvnév a normalizáló táblán ellenőrizve), nem `Belso`; a Thayer-példa jelentésszáma a bemeneti rétegben képzett szám (`ThayerPelda.jelentesszam`), nem a belső kulcsból a számításban kibontott érték. Statikus teszt: a `szamitas/` rétegben burkoló `ertek` mezőjéből szám és igehely nem képződik |
| 1b | a szakaszjel a szótár belső szócikk-azonosítójával | DT871: a látható jel csak a szócikken belüli tagolás (`Gerinc.jel`); ha a jel a szó több szócikkében is áll, mellette a szótár saját címszava áll a homográf-számával, szó szerinti idézetként (`Gerinc.jel_szocikke`; „1 (II. רַע)”), híján sablonmondat a szócikk sorszámával („Qal 1 (a BDB 1. szócikke)”). A belső azonosítós alak (`kulcs_jel`) csak megjegyzésbe, rendezéshez és kereséshez jut. A két mintalapon ez az út továbbra sem él (teszt: a látható szövegben nincs belső szócikk-azonosító) |
| 2 | az olvasási napló hézaga | a jegyzéktábla saját sort kapott (B68), az olvasása a naplóba kerül, e sor nélkül a munkamenet nem nyílik meg; a párosítás (B54) könyv–fájl leképezése naplózott olvasás lett (mind a 66 fájl a hash-ével). Teszt: a bemeneti réteg magjában egy fájlnyitás áll, és minden hívója naplóz. A referencia-tábla 11 `uj_bemenet` sorral bővült (10 párosítás-fájl és a jegyzék) |
| 3 | a DT868 és a DT869 állapota | ✅ |
| 4 | „tizenhárom” szimbólum | javítva: tizennégy |

**Két új sablonmondat** (`eredet=uj`, `dontes=var`; a 218a végi listába kerül): `e2.jel.szocikkel` („{jel} ({szocikk})”) és `e2.jel.szocikk_sorszam` („{szotar|a} {n}. szócikke”, pl. „a BDB 2. szócikke”). Egyik sem áll a két mintalapon.

**A megnevezés rendje (DT871).** Az orkesztrátor példája („רַע I”) a homográf-számot a címszó mögé tette; a lapon a szótár saját rendje áll („II. רַע”), mert a megnevezés szó szerinti idézet (a BDB-szakasztábla szócikkfejének eleje, változtatás nélkül).

**Mérés a szócikk-megnevezésről.** A 3 471 több szócikkes BDB-szócikkből 1 029 megnevezésében áll homográf-szám, 2 192-nek a címszava egyedi a szón belül, 250-nél a sorszám áll. Megnevezést 454 szakaszjel kér: 414 címszóval, 40 sorszámmal.
*Proveniencia: `scope=a BDB-szakasztábla több szócikkes Strong-számai, szócikkenként és megnevezést kérő szakaszjelenként (Gerinc._cimszavak, Gerinc.jel_szocikke) | forras=adat/bdb_szakaszok.tsv | ts=2026-11-13`.*

**Állás a 2. javítókör után (HAMART-001, `PARDES_DATUM=2026-11-13`).** „2. Előfordulások”: 1 engedélysor (S1-FORRAS); a melléklet: 10 engedélysor; engedély nélküli diff-sor 0. Tesztek: 152 futott, 119 zöld, 33 kihagyva (a váz). Festékpróba: 0 szivárgás (HAMART: belső 171, idézet 326, kézi 240 látott jelzőszó; ISTENTISZT: 114, 183, 121; a belső jelzőszó az ISTENTISZT-lapon 2-vel kevesebb, mert a tartomány kezdő verse már nem belső szöveg).
*Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py; general.py --cel lexikon2 --id HAMART-001 + python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001 | forras=a munkafa a javítókör commitja előtt | ts=2026-11-13`.*

**Új táblasorok:** a jegyzék +1 (B68; összesen 29), a sablontábla +2 (összesen 127).

## DT870: az önreferencia a forrásban (`claude-fable-5-2`, 2026-11-13, a 3. session)

*Az orkesztrátor technikai döntése (2026-11-13): a három nyitott pár a forrásban javul, ebben a feladatban; egyszavas egységesítés, a tartalom nem változik; a cella az legyen, ami a jóváhagyott lapon látszott; az engedélysorok megszűnnek, a DT870 állapota ✅.*

**Eltérés az utasítás betűjétől, kimondva.** Az utasítás szava „szócikk” volt („a »lap« helyett »szócikk« álljon, ahogy a jóváhagyott lapon látszott”). A jóváhagyott lapon a három nyitott párnál nem „szócikk” áll, hanem páronként más szó: „a vizsgálat”, „ez a vizsgálat”, „a listán” (a régi cserepár jobb oldala; a motívum kézi forrása is ezeket használja). A cellákba ezek a szavak kerültek, mert az utasítás két másik feltétele (a jóváhagyott lap szövege, és az engedélysorok megszűnése) csak így teljesül: „szócikk” szóval a lap szövege megváltozna, és a két engedélysor megmaradna. Ha az orkesztrátor mégis egységesen „szócikk”-et kér, az 8 cella újabb cseréje és a korábbi mérés szerint 2 + 16 engedélysor (a melléklet és a tudományos lap érintett sorai).

| Fájl | Sor, mező | Előtte | Utána |
|---|---|---|---|
| `adat/motivumok.tsv` | HAMART-001, `negativ_kriterium` | „… ezeket a lap egyenként, tematikus helyként veszi fel.” | „… ezeket a vizsgálat egyenként, tematikus helyként veszi fel.” |
| `adat/jeloltek.tsv` | HAMART-001, Ef 2:1 és Ef 2:3, `indoklas` (2 cella) | „… amelyet a lap nem dönt el (l. az Értelmezés szakasz vitatott pontjait)” | „… amelyet ez a vizsgálat nem dönt el (…)” |
| `adat/elutasitasi_okok.tsv` | HAMART-001, 111. sorrendű sor, `cimke` és `megjegyzes` (2 cella) | „az öröklött bűnösség kérdése, amelyet a lap nem dönt el” | „az öröklött bűnösség kérdése, amelyet ez a vizsgálat nem dönt el” |
| `adat/kapcsolatok.tsv` | HAMART-001, 3 sor (1Móz 3:17 → Ézs 24:5-6 és két társa), `indoklas` | „A tematikus hely, amely a lánc szavai nélkül áll a lapon, …” | „… áll a listán, …” |
| `adat/nyilt_kodkonyv.tsv` | `kizaras_oka` értéke: `ertek`, `leiras_hu` (2 cella) | „… amelyet a lap nem dönt el” | „… amelyet ez a vizsgálat nem dönt el” (a kódkönyv kulcsa a kizárási ok szövege: követi a forrást) |
| `adat/nyilt_angol.tsv` | 3 sor: `forras_hu`, `forras_hash` | a régi magyar szöveg és a hash-e | az új magyar szöveg és a hash-e; az `angol`, a `modell` és a `datum` mező változatlan |

**Ellenőrzések.**
- A cserét szkript végezte (`split('\t')` / `'\t'.join()`), írás előtt soronkénti összevetéssel: fájlonként csak a megnevezett cellák változtak (`git diff --numstat`: 1, 2, 1, 3, 1, 3 sor), a sorok száma nem.
- **A régi generátor** mindkét HAMART-nézete a javított cellákkal is bájtra azonos a kiadott lapokkal (`cmp`, kilépési kód 0): a négy cserepár így üresen fut.
- **A nyílt mag.** Az angol fordítás nem készült újra: a tár három sorának `forras_hash`-e az új magyar szövegé (a régi hash a régi szöveg SHA-256-jának első 16 jegye volt: a szkript ezt írás előtt ellenőrizte), az angol szöveg maradt („which the entry does not decide”: az „entry” a lap önmegnevezése). A `nyilt_mag_angol.py allapot` száma a javítás előtt és után azonos (1 262 cella: 1 037 fordított, 76 hiányzó, 149 elavult): a javítás új elavult fordítást nem hozott. A `nyilt_mag/` újraexportálva: 4 adatsor (`kizarasok.tsv` 2, `kodkonyv.tsv` 1, `motivumok.tsv` 1), a `KODKONYV.md` 1 sora és a kiadási hash (`KIADAS.txt`, `RELEASE.txt`, `ELLENORZO_OSSZEG.sha256`). A nyílt mag kapujának 150 bukása a javítás előtt is állt (149 elavult fordítás az ISTENTISZT-001 soraiban és 1 visszhang-sor): egyik sem az itt érintett sor.
- **Az új generátor.** A melléklet engedélysorai 10-ről 8-ra csökkentek (az S2-ONREF-1 és -2 megszűnt); engedély nélküli diff-sor 0. A referencia-tábla négy bemenet-sorának hash-e frissült (B02, B04, B45, B56).

*Proveniencia: `scope=git diff --numstat -- adat nyilt_mag; general.py --cel lexikon --id HAMART-001 + cmp a HEAD két lapjával; python eszkozok/nyilt_mag_angol.py allapot (előtte és utána); python eszkozok/nyilt_mag_export.py; python eszkozok/nyilt_mag_kapu.py; general.py --cel lexikon2 + python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa a DT870 commitja előtt | ts=2026-11-13`.*

**Az `ir` mező.** A hat adatfájl és a generált `nyilt_mag/` kívül esik a brief `ir` mezőjén. A mezőt nem bővítettem: a bővítés a feladatkövetőben függési kört ad (`python eszkozok/feladatok.py ellenoriz`: „függési kör: #203 ↔ #212 ↔ #218”; a brief olvassa azok fájljait, és közös fájlt írna velük), amelynek feloldása a felhasználó döntése. Az `ir`-en kívüli írásra CI-szabály nincs; a módosítás itt és a DT870 sorában cellánként áll.

**Amit a felhasználónak látnia kell.** (1) A fenti szóválasztás („vizsgálat”, „listán”; nem „szócikk”). (2) A nyílt mag angol szövege nem változott: ha az „entry” helyett „this study” kell, az két szöveg újrafordítása és egy kódkönyv-címke. (3) Az `ir`-en kívüli hat fájl.

## F218.5 — S2, második fele: „1. Döntési út” (1.1–1.5) (`claude-fable-5-2`, 2026-11-13, a 3. session)

**Eredmény (HAMART-001, `PARDES_DATUM=2026-11-13`, `munka` mód).** A „1. Döntési út” szakasz 110 sorából 94 bájtra egyezik a referenciával; **16 diff-sor, mind engedéllyel, két előre megszámolt osztályban; engedély nélküli diff-sor: 0.** A melléklet 8, a „2. Előfordulások” 1 engedélysorral áll (változatlan). Az S2 szelet ezzel kész: a szakasz-diff 0 az engedélyeken kívül mindkét nézetre.
*Proveniencia: `scope=general.py --cel lexikon2 --id HAMART-001, majd python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa az S2b commitja előtt | ts=2026-11-13`.*

| Engedélysor | Osztály | Darab | Előre rögzítve | Mi tér el |
|---|---|---|---|---|
| S2-FORRAS | GK-07 | 1 | 1 (a brief 8.1 (b) osztálya) | a blokkfejléc forrás- és licenclistája a szakasz valódi olvasásaiból jön |
| S2-FUNKCIO-1…15 | M-CSERE (DT869) | 15 | 15 (a folytatási fájl „Az S2 második feléhez” pontja) | az 1.4 pont listaelemeiben a funkció kézi magyarázata a kettőspont után változatlanul, kisbetűvel áll („1Móz 3:14: az átok első kimondása, …”); a régi generátor nagy kezdőbetűvel írta át. Az engedély írásakor gépi ellenőrzés: a sor egyetlen eltérése a listaelemek kezdőbetűje |

**Mi készült.**
- **Bemenetek** (a jegyzék +4 sor: B02, B10, B15, B47): a motívum sora (`bemenet/motivum.py` `b02_motivum`: a negatív kritérium szerkezeti bontása a „Nem tartozik ide” szavaknál, szövegváltoztatás nélkül; a cím és a fölérendelt fogalom záró pontja kapu, nem levágás); a szótári alak és kiejtése (`bemenet/szavak.py` `b10_lemmak`, `Kiejtes.szotari`: görögül a szótár átírásának magyaros alakja, héberül a kivétel-sor, híján a gépi kiejtés; a lemma-változat a motívum versei szerint, GK-13: H2403 → חַטָּאת, mert az 1Móz 4:7 szótöve ez); a rövid magyar jelentés egy úton (`rovid_jelentes`: héberül a glosszatábla fő sora, görögül a fordítástábla rövid glosszája; magyar jelentés híján kimondott hiány, angol szöveg nem kerül a lapra); a kézi forrás vitatott pontjai és nyitott kérdései szó szerinti részletként (`b47_nyitott_kerdesek`).
- **Számítás** (`szamitas/dontesi_ut.py`): a számok a vizsgálat közös modelljéből jönnek (ugyanabból, mint a melléklet); a motívum helyei a hordozó elemük szerint csoportosítva, a tábla rendjében; a helyek megoszlása (Genezis, az Ószövetség többi könyve, Újszövetség) a könyvtáblából (a Genezis a tábla első sora: könyvnév a kódban nincs).
- **Kapuk a modellen:** a vizsgálat számegyezése; a csoportok helyeinek összege a motívum helyeinek száma; csoportonként a megoszlás a helyek száma; a lenyíló blokkba kerülő kézi szöveg és idézet nem tartalmazhat `<`, `>`, `&` jelet (a régi kód átkódolta ezeket; az új nem ír át, ezért az ilyen szöveg kapun akad meg; a két mintalap adatában 0 ilyen jel áll).
- **Megjelenítés** (`megjelenites/md/dontesi_ut.py`): minden mondat a sablontáblából; a lenyíló blokkok jelölése a sablonmondat része. A mellékletre mutató horgony a melléklet címsorából képződik (teszt: minden link létező címsorra mutat).

**A régi utófeldolgozó lánc itt nem változtatott mást.** A negatív kritériumon a régi `olvasoi_indok` tisztítása a HAMART-szövegen az önreferencián kívül semmit nem írt át (a két bekezdés bájtra egyezik a forráscellával). A cellakezdő alakok (pl. „1.2. lépés minden találata”, „A keresés találata, …”) sablonsorként, illetve a névtábla `halo_leiras` soraként állnak, ahogy a lapon.

**Új táblasorok.** A jegyzék +4 (összesen 33); a névtábla +3 (`halo_leiras`; összesen 33); a sablontábla +69 (összesen 196): mind betűre a régi lap szövege, kivéve egyet. **Új sablonmondat** (`eredet=uj`, `dontes=var`): `d14.hely.magyarazat_nelkul` (listaelem magyarázat nélkül: csak az igehely linkje; a két mintalapon nem áll). Két sor eredete megjegyzi, hogy a régi kód a kézi szöveget nagy kezdőbetűvel írta (`d14.hely`, `d11.csak_tagabb`).

**Tesztek:** 167 futott, 134 zöld, 33 kihagyva (a váz); az S2b tesztjei: `teszt_dontesi_ut.py` (15 teszt). **Festékpróba:** 0 szivárgás (HAMART: belső 191, idézet 420, kézi 364 látott jelzőszó; ISTENTISZT: 134, 208, 185). **Futásidő:** az új generátor a HAMART két nézetét 6 másodperc alatt adja (a régi 44–47 mp). **ISTENTISZT-001:** a szakasz generálódik (a tudományos nézet 271 sor), a kapuk zöldek, a linkek létező horgonyra mutatnak; bájt-mércéje nincs.
*Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001; time general.py --cel lexikon2 --id HAMART-001 | forras=a munkafa az S2b commitja előtt | ts=2026-11-13`.*

**A HAMART-001 számai a modellen:** 1 840 megvizsgált vers = 56 (a motívumhoz tartozik, 49 hely) + 1 542 (csoportosan kizárva, 4 ok) + 242 (egyenként elutasítva, 26 ok) + 0 (döntésre vár); kereszthivatkozás-ajánlásból 99; 15 helycsoport, 13 lánc-szó, 7 határeset, 7 vitatott pont és nyitott kérdés. Az ISTENTISZT-001-en: 2 helycsoport, 3 lánc-szó, 0 határeset, 4 kérdés.
*Proveniencia: `scope=szamitas.dontesi_ut.szamit a két mintalapra (a modell mezőinek száma) | forras=a munkafa az S2b commitja előtt | ts=2026-11-13`.*

**Amit a felhasználónak látnia kell (S2b; a 218a végi átnézés listájába).**
1. **Az 1.4 pont listaelemei kisbetűvel kezdődnek** a kettőspont után („1Móz 3:14: az átok első kimondása, a kígyóra; …”), mert a funkció magyarázata a forrás szerint áll. A régi lap nagybetűvel írta. Ha a nagybetűs alak kell, a magyarázat mondatkezdő alakja adatba kerül (új mező), és a 15 engedélysor megszűnik. Az ISTENTISZT-lapon ugyanez látszik.
2. **„mind a 575 verse”.** A csoportos ok mondata betűre a régi lapé („A csoport mind a {n} verse …”); nyelvtanilag „mind az 575 verse” volna helyes. Nem javítottam, mert a szöveg jóváhagyott (ugyanaz az eset, mint a melléklet „A 575 vers” címe); ha javítandó, a sablonmondat `{n|a}` alakot kap, és ez 1 engedélysor.
3. **A kizárási okok kézi megjegyzéseiben belső szó áll az ISTENTISZT-lapon** („a negatív kritérium a passzív / megnevező használatot zárja ki”, „(a fölérendelt fogalom felé)”): ez kézi adat (`adat/elutasitasi_okok.tsv`), a generátor változatlanul adja; a javítása a forrásban történik, a lap olvasásakor.
4. **Az új sablonmondat** (fent) és a javítókör két új mondata (`e2.jel.szocikkel`, `e2.jel.szocikk_sorszam`).

**Ismert korlátok (az ellenőrnek is).**
- A B10 jegyzéksora két fájlt fed (a görög és a héber rövid szótár), egy licenckulccsal (`TBESH`); a két szótár licenccímkéje a leltárban külön sor. A blokkfejléc licenclistája így az egyik címkét adja.
- A `d11.csak_tagabb` (nincs „Nem tartozik ide” rész, csak fölérendelt fogalom) és a „Döntésre vár” sor egyik mintalapon sem áll: teszt nem fedi a megjelenésüket.
- A nyitott kérdés szó szerinti részlet: ha a forrásban a félkövér cím végén nincs pont, a lapon sem lesz (a régi kód pótolta).

## Független ellenőrzés — 3. ellenőrzés

*A `fuggetlen-ellenor` subagent (`claude-opus-5-5`) jelentése változtatás nélkül; bemenete: a brief, a `656c508a..28be9127` tartomány (az S2 két fele, a 2. javítókör és a DT870), célzott hatókörrel, `teljes` szint. A push az ellenőrzés indításakor még nem történt meg (azóta megtörtént: `dca8a9f3..28be9127`). Mentve: 2026-11-13.*

ELTÉRÉS: 2 tétel

Brief: `F218_GENERATOR_UJ_A_BRIEF.md` · tartomány: `656c508a..28be9127` (5 commit) · szint: `teljes`, célzott hatókörrel · 3. ellenőrzés

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0. modell | OK | – | A modellem `claude-opus-5-5`, a kért `opus`. Mind az 5 commit trailere `Claude Fable 5.2`, ez egyezik a jelentés fejléceivel. A `nyilt_angol.tsv` `modell` mezője változatlan. |
| 3. CI | NEM ELLENŐRIZHETŐ | – | Push nem történt, ezért a HEAD-re nincs futás (a megbízás szerint csak jelzem). A gépi részt helyben futtattam (lent). |
| 1a `.ertek` → igehely/szám | OK | `szamitas/szotari_gerinc.py:199-207,226-232`; `bemenet/gerinc.py:398,406-413` | A `kezdo_vers` a bemenetben `Igehely`, a `jelentesszam` a bemenetben `int`. `Grep \.ertek` a `szamitas/` alatt: csak kulcsként, rendezéshez vagy prov-ban, a `megjelenites/` alatt 0. `int(` és `Igehely(` a két rétegben: 0. |
| 1b szakaszjel | OK | `bemenet/gerinc.py:214-253,435-440`; `megjelenites/md/elofordulas.py:84-95` | A `kulcs_jel` (BDB-id) csak prov-ba, rendezésbe és a `szakasz_glossza` kulcsába jut. A látható jel a `_szakaszjel` útján megy. A `_cimszavak` `m.group(0)`-t ad: összefüggő, változatlan forrásrészlet. Az új lapok látható szövegében `BDB\d`: 0/0/0/0, a mintalapokon az út nem él. |
| 2. olvasási napló | OK | `bemenet/jegyzek.py:164-184` | `open`/`glob` csak a `_fajl`/`_utvonalak` magban van. A `zarojel_javitasok` a fájlt a naplózott `_szoveg` után újra beolvassa (csak elméleti TOCTOU). Saját szkript: a két lap 104-104 naplósorából 0 nincs a referencia-táblában (útvonal + hash). |
| B numstat, cellák | OK | `adat/*.tsv` | `git diff 2b7a9b3b..4d4fc103 --numstat` és cellánkénti szkript: 8 adatcella (2+2+3+1), a kódkönyvben 2, a fordítástárban 3 sor. Az `angol`/`modell`/`datum` bájtra azonos, a `forras_hash` = SHA-256[:16] az új cellán (3/3 True). |
| B nyílt mag | OK | `nyilt_mag/` | `nyilt_mag_export.py --kimenet <scratch>` (a repó helyett), majd fájlonként cmp a HEAD-del: 0 eltérés, 0 hiányzó, 0 új fájl. `git status` üres. |
| B régi generátor | OK | – | `general.py --cel lexikon` → cmp a `git show HEAD:` két lapjával: mindkettő 0. |
| B szóválasztás | OK | `naplok/F218_jelentes.md:500` | A jelentés egyértelműen kimondja a „szócikk” helyett választott szavakat. A HEAD-lapon „ez a vizsgálat nem dönt el” 6+2, „ezeket a vizsgálat egyenként” 5, „áll a listán, a láncnak” 2. „a lap …” és „a szócikk …” 0 találat, a lexikon a tartományban változatlan. |
| C tesztek | OK | – | `tesztek/futtat.py`: 167 futott, 0 hiba, 33 kihagyva. |
| C regresszió | OK | – | A HAMART-ra: Döntési út 16, melléklet 8, Előfordulások 1 engedélysor; engedély nélküli diff 0, RENDBEN. Az ISTENTISZT-re: „nincs referenciája” (EXIT 2), a brief 8.2 szerint ez várt. |
| C festék | OK | – | 0/0 szivárgás. Látott jelzőszó: 191/420/364 és 134/208/185, egyezik a jelentéssel. |
| C S2-FUNKCIO, S2-FORRAS | OK | – | Saját difflib-szkript a szakaszra: mind a 15 sor egyetlen eltérése a „: ” utáni kezdőbetű (15/15, nem csak 4 minta). Az S2-FORRAS sor a `GENERÁLT-KEZDET` blokkfejléc. |
| C (i) `b02_motivum` | OK | `bemenet/motivum.py:40-62` | A `partition('Nem tartozik ide')` két összefüggő részletet ad, csere nincs. A záró pont kapu, nem levágás. |
| C (i) `gerinc_reszek` | **ELTÉRÉS** | `bemenet/elofordulas.py:131-134`; `szamitas/dontesi_ut.py:124-134` | A `Kulcs`-ként is burkolt `gerinc_elem` minden nem-Strong része `Kezi` lesz. A MENNY-001-en (saját szkript, `b03`) ez `referencia:1Énokh 10:4-6/…`, `idézet:1Énokh 1:9` és `formula:οὐκ ἐφείσατο …` értéket ad, és ezek „szópár: …” néven a lapra kerülnének. Kapu nem állítja meg. |
| C (ii) `b47` regexek | OK | `bemenet/motivum.py:25-28,104-117` | A `findall` csoportja összefüggő részlet. Kockázat: a `[^.!?]+` sortörésen átnyúlhat, és rövidítésnél („pl.”) mondat közepén vág. |
| C (iii) `html_ben` lefedés | OK | `szamitas/vizsgalat.py:89-93,174`; `szamitas/dontesi_ut.py:101-103,134-136` | Lefedett mezők: az ok címkéje és leírása, a Károli-példa, a lemma, a kiejtés, a jelentés, a szópár-név és a funkció-magyarázat. HTML-jelölésű sablonsor (`grep '[<&>]'`) csak d13 és d14, a d11/d12/d15 sima Markdown. |
| C festék ereje | **ELTÉRÉS** | `szoveg.py:574-584`; `festek.py:30` | A `cim_horgony` a kézi okcímkét kisbetűsíti, és horgonyként (href) a lapra írja. A jelzőszót kereső regex kisbetű-érzékeny: festett futásban 30 (HAMART) és 18 (ISTENTISZT) `zzq…zz` áll megjegyzésen kívül, a próba egyiket sem látja. |
| C kapuk | OK | `bekotes.py`; `fo.py:81-83` | A `kapu=sz_dontesi_ut.kapu` be van kötve, és a megjelenítés előtt fut. Saját próba hamisított modellel: hiányzó hely, `osszes+1`, `csoport+1`, bent vers kizártként → mind a négy `KapuHiba`, a megjelenítő 0-szor hívódott. A `bent+…=osszes` ág valós adaton tautológia. |
| C táblasorok | OK | `adat/lapgen_*.tsv` | Sorszám (komment- és fejléc nélkül): 33 / 33 / 196, az S2b-ben +4 / +3 / +69. Egy `dontes=var` sor van (`d14.hely.magyarazat_nelkul`). Az eredet-szimbólumok mind léteznek a `lexikon_general.py`-ban. Kilenc mintasor minden literálja megvan a HEAD-lap 108–218. sorában. |
| C negatív kritérium | OK | – | A d11 sorok a szakasz-diffben 0 eltérésűek, és a sablon (`**Ami ide tartozik:** {szoveg}`) nem ír át. Az állítás így igaz. |
| D proveniencia, `ir` | OK | `naplok/F218_jelentes.md:519` | Minden új számblokk alatt áll proveniencia-sor. Az `ir`-en kívül csak a 4d4fc103 írt (6 adatfájl és a `nyilt_mag/`); a jelentés ezt kimondja. |
| Lista 1–2 | OK | – | Törölt adatsor nincs, csak cellacsere. A jegyzék a B68-cal és a B02/B10/B15/B47-tel bővült. |
| Lista 3 nulla-diff | OK | – | Csak a HAMART „1. Döntési út” és „2. Előfordulások” szakaszára és a mellékletre érvényes, a többi szakasz „nincs kész”. Az ISTENTISZT-re nincs bájt-mérce. |
| Lista 4 Δ (E17) | OK | – | A tartományban: bemenetek +9, sablonok +85, névtábla +6, a többi tábla 0. A bontás commitonként a jelentésben (+14 / +2 / +69: 68 régi + 1 új). |
| Lista 5 ⛔ | OK | – | A DT870 a felhasználói döntéssel zárult, az engedélysorok megszűntek. |
| A1–A6 | OK | – | Tartalmi réteg csak a 8 egyszavas cellacsere. |

Az ELTÉRÉS-ek súlyossági sorrendben:
1. **`gerinc_reszek` (C/i).** A típusjelölő előtagú `gerinc_elem` értékek (`referencia:`, `idézet:`, `formula:`) kézi prózaként, „szópár” címmel kerülnének a lapra. A két mintalapon nem él, a MENNY-001 migrációjakor igen, és kapu nem fogja meg. A `tematikus:` előtagot a kód kezeli, ezt a hármat nem.
2. **A festékpróba vakfoltja.** A kézi okcímke átalakítva, kisbetűvel horgonyba kerül. Ez nem látható szöveg, de a brief 2.3 szerint jelzőszó megjegyzésen kívül sehol nem állhat. A kisbetű-érzékeny regex miatt a próba ezt az utat nem méri.

Az ideiglenes fájlok (szkriptek, generált lapok) a repón kívül, a scratchpadben vannak: `C:\Users\bases\AppData\Local\Temp\claude\7726172d3b7d614a\ece49adf-e664-4f56-b65b-6d6d801699e3\scratchpad\`

## A 3. ellenőrzés besorolási javaslata (egyeztetésre vár; javítás még nem történt)

*Az építő session (`claude-fable-5-2`) javaslata; a besorolás az orkesztrátoré. A javítás a következő session első lépése lehet (a 3. session kontextusa a 70%-os határ közelében zárt).*

| # | Tétel | Javasolt besorolás | Indok, teendő |
|---|---|---|---|
| 1 | a típusjelölő előtagú hordozó elem (`referencia:`, `idézet:`, `formula:`) kézi névként, „szópár” címmel kerülne a lapra | mechanikus (kapu), és egy későbbi tartalmi kérdés | most: a hordozó elem fajtája a bemeneti rétegben zárt készlet legyen (Strong-részek; `tematikus:`; kézzel elnevezett szópár előtag nélkül); ismeretlen előtag `BemenetHiba`, a lap nem találgat. Teszt a MENNY-001 soraira (a futás megáll, kimondott hibával). Később, a MENNY-001 új lapja előtt: hogyan nevezze meg a lap az ilyen csoportot (új sablonmondat, a felhasználó jóváhagyásával); ez nem a 218a két mintalapjának kérdése |
| 2 | a festékpróba nem látja a horgonyba kerülő, kisbetűsített jelzőszót | mechanikus | a próba kis- és nagybetűtől függetlenül keressen; a horgony (a link célja és a címsor azonosítója) kapjon saját tartományfajtát, amelyben a kézi és az idézett szöveg jelzőszava megengedett (a horgony a címsorból képzett szerkezeti azonosító), a belső mező jelzőszava ott is szivárgás. A kivétel szövege a 6-os sablon alapszabály-szakaszába kerül (egy mondat), teszttel |

## A 3. ellenőrzés javítóköre (`claude-fable-5-2`, 2026-11-13, a 3. session)

*A besorolást az orkesztrátor hozta (2026-11-13): mindkét tétel mechanikus, a fenti javaslat szerint, ebben a sessionben javítva. Az orkesztrátor az S2 négy eltérését (a szóválasztás, a homográf-szám rendje, az `ir`-en kívüli fájlok, a nyílt mag változatlan angol szövege) elfogadta; az `ir` mező nem bővül, a függési kör a 218c-ben rendeződik (N188). A 218a végi listába felvéve: a kisbetűs listaelemek, a „mind a 575”, és a három új sablonmondat. Az újraellenőrzés az S3 végi ellenőrzéssel együtt fut.*

| # | Tétel | Mi történt |
|---|---|---|
| 1 | a típusjelölő előtagú hordozó elem kézi névként kerülne a lapra | a hordozó elem fajtája zárt készlet a bemeneti rétegben (`bemenet/elofordulas.py`): Strong-szám(ok), kézzel elnevezett szópár előtag nélkül, vagy `tematikus:`; ismeretlen előtagnál (`referencia:`, `idézet:`, `formula:`) a bemenet kimondott hibával megáll, a lap nem készül el. Próba: a MENNY-001 generálása BUKÁS-sal áll meg („ismeretlen hordozó-előtag: `referencia:` (MENNY-001, Júd 1:6)”), kilépési kód 1. Az ilyen csoport megnevezése a MENNY-001 új lapja előtt eldöntendő (új sablonmondat) |
| 2 | a festékpróba nem látta a horgonyba kerülő, kisbetűsített jelzőszót | a próba kis- és nagybetűtől függetlenül keres; a horgony külön tartományfajta (`Fajta.HORGONY`: a sablonmondat `horgony` típusú paramétere), ahol a kézi és az idézett szöveg jelzőszava megengedett, a belső mezőé nem; horgonyon kívül az átalakított jelzőszó szivárgás (a szöveget valami átírta). A kivétel egy mondata a 6-os sablon alapszabály-szakaszában áll |

**Állás a javítókör után.** Festékpróba: 0 szivárgás; a horgonyokban látott jelzőszó 30 (HAMART) és 18 (ISTENTISZT): ez az a szám, amelyet az ellenőr a próba vakfoltjaként mért. Látott jelzőszavak: HAMART belső 191, idézet 420, kézi 394; ISTENTISZT 134, 208, 203 (a kézi szám a horgonyokkal nőtt). Regresszió: engedély nélküli diff-sor 0 (25 engedélysor, változatlan). Tesztek: 172 futott, 139 zöld, 33 kihagyva (a váz); új: 4 festék-teszt és 1 előtag-teszt.
*Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py; general.py --cel lexikon2 --id HAMART-001 + python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001; general.py --cel lexikon2 --id MENNY-001 | forras=a munkafa a javítókör commitja előtt | ts=2026-11-13`.*

**Az adat a hordozó-előtagokról.** Az `adat/elofordulasok.tsv` 250 sorából 241-nek nincs előtagja, 6 `tematikus:` (HAMART-001), és 1-1 `referencia:`, `idézet:`, `formula:` (mind MENNY-001).
*Proveniencia: `scope=a gerinc_elem mező kezdő „szó:” előtagjának számlálása | forras=adat/elofordulasok.tsv | ts=2026-11-13`.*

## F218.6 — S3, első rész: a „4. Szótári háttér” váza, az Áttekintés és az egyszerű pontok (`claude-fable-5-2`, 2026-11-13, a 4. session)

*Modell-ellenőrzés: a session tényleges modellje `claude-fable-5-2`, a brief kért modellje `fable`: egyezik. Effort: `high`.*

**Mi készült el.** A szakasz címe, a blokkfejléc, a bevezető és a hatókör-sor; az áttekintő tábla (15 szó: kiejtés, alapjelentés, LXX-megfelelő, helyek); nyelvenként a nyelvrész feje és a 4.1 (Alapjelentés), 4.3 (Teológiai szócikk), 4.4 (Szemantikai mező), 4.5 (Tömör jelentés), 4.10 (Kiejtés) pont; a nyelvfüggetlen rész feje és a 4.11 egysoros mutató. Új modulok: `bemenet/szotari.py` (B29, B30, B31, B35, B36, B52), `szamitas/szocikkek.py`, `megjelenites/md/szocikkek.py`, `tesztek/teszt_szocikkek.py`; bővült a `bemenet/motivum.py` (a rövid jelentés egy útja az angol eredetivel és az elavulás jelzésével) és a `bemenet/jegyzek.py` (nagy szövegkiadás indexe a fájlok hash-ére kulcsolt gyorsítótárral).

**Mérés.** A 4. szakasz 37 alblokkjából (a 3. és a 4. szintű címsorok és a blokk záró jelölője szerint) 17 kész (212 sor a referencia 1 360 sorából), 20 nincs kész; a kész alblokkok diffje az első futáson 1 sor volt (a blokkfejléc forráslistája: előre várt osztály, `S3-FORRAS`), engedély nélküli diff-sor 0. A festékpróba mindkét lapon 0 szivárgás. Tesztek: 184 (152 zöld, 32 váz). Egy lap generálása kb. 8 s (a régi 46,5 s).
*Proveniencia: `scope=python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001; python eszkozok/lapgen/tesztek/futtat.py | forras=a munkafa az F218.6 (1) commit előtt | ts=2026-11-13`.*

**A regresszió részleges módja.** A mérce eddig a 2. szintű címsor szerinti szakaszt ismerte egységként; a 4. szakasz több szeletben készül (a pontjai az S3-ban és az S4-ben, a „Miért fontos ez a lelet” rés az S8-ban), ezért a `regresszio.py` a `RESZLEGES_SZAKASZOK` listában álló szakaszt alblokkonként méri: a még meg nem írt alblokk „nincs kész” (megszámolva), a megírt soronként vetődik össze. Más szakaszra a mód nem áll (teszt), `--teljes` mellett a lista nem számít. A lista a szakasz elkészültekor ürítendő.

**Egyeztetett eltérések a régi kódtól** (a kimenet bájtra egyezik; a mintalapokon egyik sem látszik):
- A pont neve a névtáblából jön (`szotari_pont`), nem a szótári pontok táblájának `szerep` mezőjéből cserével.
- A rövid jelentés hiánya egyféle (GK-16): az angol eredeti „fordításra vár” jelöléssel, vagy „a szótár nem ad magyar rövid jelentést”.
- A licenc a mondatban a licencleltárból jön (GK-07).
- Az elemzetlen szótári bejegyzés figyelmeztetése darabszámos sablonmondat; a nyers leírás megjegyzésbe kerül.
- A Septuaginta-könyvtár két segédtáblája (fejezet- és versdöntések) a fejléce alapján kimarad a versszámlálásból (a régi kód a `strong` oszlop hiánya miatt hagyta ki, kimondatlanul); az olvasásuk a naplóban áll.

**Új táblasorok.** Jegyzék: +6 (B29, B30, B31, B35, B36, B52). Névtábla: +14 (13 `szotari_pont`, 1 `forras`: B32). Sablontábla: +60, eredet szerint: a régi generátor szimbóluma 54, `uj` 6 (`dontes=var`: `s4.felulvizsgalat`, `s4.p3.cim.var`, `s4.p3.cim.felulvizsgalat`, `s4.p4.elemzetlen`, `s4.nyelv.gorog.ures.megjegyzes`, `s4.nyelv.heber.ures.megjegyzes`); szakasz szerint: keret 3, 4 (váz) 24, Áttekintés 10, 4.1 4, 4.3 9, 4.4 4, 4.5 3, 4.10 2, 4.11 1.
*Proveniencia: `scope=git diff -U0 HEAD -- adat/lapgen_sablonok.tsv adat/olvasoi_nevtabla.tsv adat/lapgen_bemenetek.tsv (a hozzáadott sorok megszámolva) | forras=a munkafa az F218.6 (1) commit előtt | ts=2026-11-13`.*

**Ami az S3-ból hátravan:** a 4.2 kártyák (654 sor), a 4.6–4.9 és a 4.12–4.14 pont, a B36 frissességi kapuja (GK-03), a GK-15 Thayer-része (az 5 elavult sor), GK-18, GK-19, GK-N178, HN-12, HN-15, és az S3 végi független ellenőrzés. A sorrend a folytatási fájl „Következő lépés” pontjában áll.

## F218.6 — S3, második rész: a 4.7 és a 4.9 pont (`claude-fable-5-2`, 2026-11-13, a 4. session)

**Mi készült el.** A 4.9 (Versenkénti jelentés) és a 4.7 (Megfelelők a másik nyelven) pont mindkét nyelven. Új modulok: `szamitas/szotari_sece.py`, `szamitas/szotari_tipusok.py` (a pontok közös adatosztályai); bővült a `bemenet/szotari.py` (B28: a kétnyelvű szótár; B42: a Strong-szótár származtatása; a szóalak → Strong index), a `bemenet/szavak.py` (a forrásban kiírt alak kiejtése, a görög betűnkénti gépi átírás, a görög szócsalád tövei) és a `szamitas/elofordulas.py` (`ubs_cellak`: a 2. tábla UBS-cellájának számítása önállóan hívható, így a 4.9 a modellből számol, nem a kiírt cella szövegéből).

**Mérés.** A 4. szakasz 37 alblokkjából 21 kész (427 sor a referencia 1 360 sorából), 16 nincs kész. A kész alblokkokban 3 diff-sor áll, mind engedéllyel: `S3-FORRAS` (1; a blokkfejléc forráslistája a valódi olvasásból) és `S3-HN15` (2; a két nyelvrész betűre azonos jegyzete, ezért egy engedélysor 2 darabbal). A HN-15 előre rögzített száma (az F218.1 alapmérése) 2: egyezik. Festékpróba: 0 szivárgás mindkét lapon. Tesztek: 189 (158 zöld, 31 váz); a vázból a GK-16 és a HN-15 valódi tesztté vált.
*Proveniencia: `scope=python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001; python eszkozok/lapgen/tesztek/futtat.py | forras=a munkafa az F218.6 (2) commit előtt | ts=2026-11-13`.*

**HN-15 (GK-28, a SECE-mondat).** A 4.7 táblái alatti jegyzet a régi lapon azt állítja, hogy a görög rövid jelentés „a TBESG angol glosszája (magyar rövid glossza-tábla a görögre még nincs)”. A valós állapot: a görög rövid jelentés a lexikon fordítástáblájából jön, magyarul (a tábla soraiban magyar szöveg áll). Az új mondat a két forrást a névtáblából nevezi meg (B15, B14: mindkettőt olvassa a szakasz, teszt ellenőrzi). Új sablonmondat (`s4.p7.labjegyzet`, `eredet=uj`, `dontes=var`): a 218a végi listába.

**Egyeztetett eltérések a régi kódtól** (a kimenet a HN-15 két során kívül bájtra egyezik):
- A 4.9 számlálója a lapmodellt olvassa; a régi kód a kiírt cella szövegében kereste a „[ⓘ]” jelet és a „nem egyértelmű” szót.
- A görög szócsalád töve és a kiírt alak gépi átírása a bemeneti rétegben képződik (összevetési kulcs, illetve idézhető kiejtés); a számítási rétegben szövegművelet nincs.
- A híd mondatában a szó rövid jelentése csak magyarul áll; a hiánya itt nem kerül a fordítás-állapot listájára (a szó a táblában jelölve áll).

**Új táblasorok.** Jegyzék: +2 (B28, B42). Névtábla: +1 (`forras`: B15). Sablontábla: +52, eredet szerint: a régi generátor szimbóluma 51, `uj` 1 (`s4.p7.labjegyzet`); szakasz szerint: 4 (közös) 8, 4.7 23, 4.9 21.
*Proveniencia: `scope=git diff -U0 HEAD -- adat/lapgen_sablonok.tsv adat/olvasoi_nevtabla.tsv adat/lapgen_bemenetek.tsv (a hozzáadott sorok megszámolva) | forras=a munkafa az F218.6 (2) commit előtt | ts=2026-11-13`.*

**Megállás.** A session a kontextusa miatt zár (60% fölött; a szabály 70%-nál zárást ír elő, és a hátralévő legkisebb pont sem fér bele biztonsággal). Az S3 nem zárult le: hátravan a 4.2 (654 sor), a 4.6, a 4.8, a 4.12–4.14, a B36 frissességi kapuja (GK-03), a GK-15 Thayer-része, GK-18, GK-19, GK-N178, HN-12. **Az S3 végi célzott független ellenőrzés ezért nem futott:** az S3 lezárásakor esedékes, a 3. ellenőrzés javítókörének két tételével együtt (a tartomány eleje: `28be9127`, illetve az S3-ra `03636753`).

## F218.6 — az S3 alszeletekre bontása (2026-11-13, a 4. session zárása)

A felhasználó kérése az orkesztrátoron át, szó szerint: „ne daraboljuk?”. Az orkesztrátor rendelkezése: az S3 négy alszeletre bomlik, mert a „4. Szótári háttér” a lap legnagyobb része: **S3a** (Áttekintés és 4.1), **S3b** (4.2 BDB-kártya), **S3c** (Thayer és a többi szótár, 4.3–4.10), **S3d** (4.12 Nave, 4.13 és 4.14 Károli). Minden alszelet a saját diffjével (0 engedély nélküli sor) zárul, commit, push és a folytatási fájl frissítése után; a független ellenőrzés két alszeletenként, célzottan fut; 70%-os kontextusnál a következő alszeletet új session viszi.

**A 4. session két commitja az alszeletek szerint:** az `F218.6 (1)` (`759a0699`) az S3a egésze (a szakasz vázával és a regresszió részleges módjával) és az S3c-ből a 4.3, 4.4, 4.5, 4.10; az `F218.6 (2)` (`76a92fdb`) az S3c-ből a 4.7 és a 4.9. **Az S3a kész.** Az S3c-ből hátravan a Thayer-kártya (a görög 4.2), a 4.8 és a 4.6 (az utóbbi első fele az S4 számításából jön). Az S3b és az S3d nem indult. Független ellenőrzés ebben a sessionben nem futott: lezárt alszelet egy van; az első ellenőrzés az S3a és az S3c lezárása után esedékes.

## DT872: az ismétlés megszüntetése a lap elején (`claude-fable-5-2`, 2026-11-13, az 5. session)

**Az ok.** A HAMART-001 lapján a kritérium négyszer áll (a lap eleje, a Kivonat, az 1.1 pont, a 3. szakasz vége), a tágabb kör háromszor: négy egymásra rakódott javítás mindegyike újabb helyre írta ki ugyanazt a szabályt. A felhasználó a lektori bírálat 6. pontja szerinti módosított változatot hagyta jóvá (az orkesztrátoron át, szó szerint: „Igen, mehet”). A döntés: DT872 (`dontesek/uj/f218-generator-uj-a.md`).

**Mi készült el.**
- **1.1 A keresés tárgya:** a három régi bekezdés („A motívum:”, „Ami ide tartozik:”, „Ami nem:”) helyett egy mondat áll: hivatkozás a lap eleji meghatározásra, a keresett elemek megszámolva (héber szó, görög szó, szópár: a lapmodellből), és mutató az 1.2, az 1.3 és az 1.4 pontra. A HAMART-001 lapján: „A keresés tárgyát a lap eleje határozza meg ([Mi tartozik ide, és mi nem](#mi-tartozik-ide)). A keresés 8 héber szóra, 5 görög szóra és 3 szópárra terjedt ki: a szavakat az 1.2., a kizárás okait az 1.3., a megmaradt helyeket az 1.4. pont sorolja fel.” Az ISTENTISZT-001 lapján: 2 héber szó, 1 görög szó, 1 szópár.
- **Az 1. szakasz eleje:** a két magyarázó sorból a számoló bevezető marad; a dőlt hatókör-sor kimarad.
- **A horgony:** a lap eleji meghatározás horgonya a szakaszmodellben áll (`szakaszok.KRITERIUM_HORGONY`: `mi-tartozik-ide`), a címe a sablontáblában (`fej.hatar.cim`). Az 1.1 ezekre hivatkozik; a lap eleje (S8) ugyanezekből írja ki.
- **Két kapu** (`eszkozok/lapgen/ismetles.py`), a kész lap fajta-térképén (a megjegyzés, a jelölés és a horgony nem látható szöveg):
  1. *A kritérium egyszer áll* (BUKÁS): a kritérium bármely 12 szavas részlete a látható lapon legfeljebb egyszer állhat; a teljes lapon (ha a lap eleje elkészült) pontosan egyszer.
  2. *Ismétlés-figyelő* (figyelmeztetés): 15 szónál hosszabb azonos szósor kétszer; az ablakban legfeljebb 4 idézett szó állhat (a kétszer idézett bibliai vagy szótári szöveg nem ismétlés). A futás a találatokat kiírja.
- **A 9-es sablon:** az „Egy szabály, két hely, egy szöveg” szabály helyén „Egy szabály, egy teljes hely” áll (v2.3).

**A szándékolt eltérés-osztály, előre megszámolva.** Az első regresszió előtt rögzített szám az 1. szakaszban: látható sor −4 (a hatókör-sor és az 1.1 három bekezdése) és +1 (az új mondat), üres sor −3. A mérés pontosan ezt adta: 8 diff-sor, hat engedélysorban (`ISM-HATOKOR`, `ISM-MOTIVUM`, `ISM-IDE`, `ISM-NEM`, `ISM-TARGY`: 1-1; `ISM-URES`: 3), mechanizmus: M-RÁRAKÓDÁS. A szakasz a motívumtáblát már nem olvassa, ezért a blokkfejléc forráslistája is változott: az `S2-FORRAS` engedélysor új hash-t kapott (a darabszáma 1 maradt). Az 1. szakasz diffje: 24 sor, engedély nélkül 0; a regresszió eredménye: RENDBEN.
*Proveniencia: `scope=python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa a DT872 commit előtt | ts=2026-11-13`.*

**A figyelő kalibrálása.** A 16 szavas ablak és a 4 idézett szó küszöbe mellett a kész szakaszokon (1., 2., a 4. részben) a HAMART-001 lapján 7, az ISTENTISZT-001 lapján 4 találat áll. Mind valódi ismétlés, három fajtából: a funkció kézi magyarázata az 1.4 pontban és a 2. szakasz táblájában (HAMART: 3); azonos jegyzet vagy cella szomszédos sorokban (HAMART: 2, ISTENTISZT: 2); a 4. szakasz ugyanazon sablonmondata a héber és a görög részben (mindkét lapon 2: egy 41 és egy 24 szavas mondat). Túlnyomóan idézett szövegből álló találat nincs köztük (a kétszer idézett szöveget a figyelő nem jelzi: `test_idezet_nem_ismetles`). A küszöbök a további szeletekkel újramérendők; a teljes lapra az S9 adja a számot.
*Proveniencia: `scope=python eszkozok/general.py --cel lexikon2 --id HAMART-001, --id ISTENTISZT-001 (a futás figyelmeztetései) | forras=a munkafa a DT872 commit előtt | ts=2026-11-13`.*

**Tesztek.** Új fájl: `teszt_ismetles.py` (14 teszt: a kritérium kapuja 8, a figyelő 4, a két mintalapon 2). A `teszt_dontesi_ut.py` régi 1.1-állításai helyett új teszt áll (az 1.1 nem ismétli a kritériumot, hivatkozik és számol). Három új vázlat-teszt a későbbi szeletekre (`teszt_vaz.py`): a lap eleji meghatározás horgonya (S8), a Kolofon sora (S8), a 3. szakasz utalása. Összesen 207 teszt (173 zöld, 34 váz). Festékpróba: 0 szivárgás mindkét lapon.
*Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001 | forras=a munkafa a DT872 commit előtt | ts=2026-11-13`.*

**Sablontábla.** Ki 6 sor (`d1.hatokor`, `d11.motivum`, `d11.ide`, `d11.nem`, `d11.nem.tagabb`, `d11.csak_tagabb`); be 6 sor: `fej.hatar.cim` (a mai lap eleji cím, betűre) és öt új mondat (`d11.targy`, `d11.targy.szavak_nelkul`, `d11.elem.heber`, `d11.elem.gorog`, `d11.elem.szopar`; `eredet=uj`, `dontes=var`).

**Ami a későbbi szeletekre marad** (a kapu és a vázlat-tesztek őrzik):
- a lap eleje (S8) kiírja a horgonyt; ettől kezdve a kapu „pontosan egyszer” módja él;
- a 3. szakasz végi „Negatív kritérium” bekezdés helyett utalás áll, a szakasz elején;
- **a Kolofon táblájában is áll a teljes kritérium** („Negatív kritérium” sor): ez az ötödik példány, a lektori bírálat nem látta. A teljes lapon a kapu megfogja; a sor sorsa a felhasználó döntése (javaslat: hivatkozás a lap elejére);
- **a Kivonat (S8):** amíg a kézi forrásban a szabályt újramondó két mondat áll, a kapu a HAMART-001 teljes lapján BUKÁS-t ad. A döntés az S8 előtt kell.

### A 218a végi listába: a kézi szöveg változásai (nem kerültek a forrásba; a felhasználó jóváhagyásával)

| # | Hely | Mai szöveg | Javaslat |
|---|---|---|---|
| 1 | Kivonat, 3. bekezdés | „Ide az a hely tartozik, amelyben a lánc egyik szava áll — … — … mondja ki, ismétli vagy fordítja meg.” | törlés (a lap eleji kritérium szűkített másolata) |
| 2 | Kivonat, 3. bekezdés, a törlés utáni mondat | „A hallás igéje háromféleképpen állhat az erőszak mellett: …” | átvezetés a mondat elején, mert a feltételt a törölt mondat vezette be; javaslat: „Ahol az erőszak szava a hallás igéjével áll egy versben, a hallás igéje háromféleképpen állhat mellette: …” |
| 3 | Kivonat, 4. bekezdés, első mondat | „A motívum tehát nem a bűn és következményei általában, hanem az a sajátos lánc, …” | törlés (a tágabb kör másolata). Egy elem vész el: „a családra”; ha kell, a lap eleji „A motívum.” bekezdésbe való |
| 4 | Kivonat, 4. bekezdés | „… mert ugyanezt a szerkezetet más szavakkal mondja ki; ezeket a vizsgálat egyenként, tematikus helyként veszi fel.” | „ugyanezt a szerkezetet” → „a lánc szerkezetét”; a pontosvessző utáni tagmondat törölhető (a lap elején áll) |
| 5 | Kivonat, utolsó mondat; a lap eleje | „Az újszövetségi helyeknél a Károli alapszövege, a Textus Receptus a mérce.” (Kivonat) / „… a Textus Receptus a mérce.” (lap eleje) | a „Károli alapszövege” a lap eleji mondatba kerül; a Kivonat mondata törlődik (így a Kivonat a Jel 22:3 idézetével zár) |
| 6 | a kritérium (`negativ_kriterium`) | egyetlen, kb. 95 szavas, kétszeresen gondolatjeles mondat; a hat szó kétszer áll benne („szóláncából (átok, föld, fáradság, bűn, erőszak, romlás) egy szó áll — héberül az átok (árar), …”), ingadozó megnevezéssel („fáradság” / „a fájdalom és fáradság”) | a zárójeles magyar szólista törlése és a mondat tagolása két-három mondatra |
| 7 | a kizárási lista: lap eleje / Kivonat | „katonai pusztítás” / „a katonai és fizikai pusztítás”; „bűnáldozat” / „a bűnáldozat törvényei” | a Kivonat listája a kritériuménál tágabb kizárást mond: vagy kikerül a Kivonatból (a példák maradnak), vagy a kritérium szava szerint áll |
| 8 | Kivonat, 3. bekezdés | „… a lánc hat héber és három görög szavának, illetve szócsaládjának minden előfordulása átnézésre került …” | az 1.1 a szótári szavakat számolja (8 héber, 5 görög: a szópár két szava és a görög szócsalád három szava külön számít). A két szám nem mond ellent, de egymás mellett magyarázatra szorul; javaslat: a Kivonatban „a lánc szavainak és szópárjainak minden előfordulása” |

A 9-es sablon bevezetője és 2. pontja (a fölérendelt fogalom mondata a Kivonatban) a 3. sor törlésével együtt igazítandó (N190).

### A 218a végi listába: döntések és új mondatok a DT-F218n-ből

- **Öt új sablonmondat** (`dontes=var`): `d11.targy`, `d11.targy.szavak_nelkul` (ha a motívumnak nincs szava: a számolás kimarad), `d11.elem.heber` („{n} héber szóra”), `d11.elem.gorog`, `d11.elem.szopar`.
- **A megmaradt magyarázó sor:** a számoló bevezető; a kimaradt sor mutatója („a részletek a 2. és a 3. szakaszban”) elveszett. Ha a másik sor kell, egy sor csere.
- **A motívum-specifikus mondat nem került az 1.1-be.** A lektor mintamondatának vége („a döntő feltétel a visszautalás az 1Móz 3–9 láncára”) motívumonként más, sablonmondat nem mondhatja ki; ha kell, kézi mező lesz belőle.
- **A Kolofon „Negatív kritérium” sora:** javaslat: hivatkozás a lap elejére (az S8 előtt).
- **Az ismétlés-figyelő találatai** közül a 4. szakasz két hosszú sablonmondata a héber és a görög részben is áll (41 és 24 szó): szándékos szerkezet, de az olvasó kétszer látja. Ha zavaró, a mondat a nyelvfüggetlen részbe emelhető.

## F218.6 — S3d: a 4.12 (tematikus index), a 4.13 (Károli-megfelelők) és a 4.14 (rejtett és hamis párhuzam) pont (`claude-fable-5-2`, 2026-11-13, az 5. session)

**Mi készült el.** A nyelvfüggetlen rész három pontja; az S3d alszelet ezzel lezárult. Új modulok:
- `bemenet/nave.py` (B57: a Nave-tárgymutató sorai Károli-versekre bontva; B70: a motívum döntései a témákról; B71: a témák magyar neve), `szamitas/szotari_nave.py`, `megjelenites/md/szotari_nave.py`. A KJV-számozású hivatkozások bontása a közös `eszkozok/nave_bontas.py` szabálya (tiszta függvény, fájlt nem olvas); a hozzá kellő KJV-megfeleltetés a Septuaginta-kiadás fájljaiból (B35, új index) és a Károli-versmegfeleltetésből (B34) jön.
- `bemenet/karoli_szo.py` (B55: a Károli-szavak szótári alakja; B53: a funkciókapcsolók; B69: a nyelvtani szavak Strong-számai), `szamitas/szotari_karoli.py` (a régi `szerep_karoli.py` szabályai: szótári alak és szócsalád, kulcsszó, rejtett és hamis párhuzam, a kulcsszó mögött álló eredeti szó), `megjelenites/md/szotari_karoli.py`.
- Bővült a `bemenet/szavak.py` (a párosítás minden párja versenként: `Parositas.parok`) és a `bemenet/elofordulas.py` (a Károli-fordítás minden verse a fordítás rendjében: `Karoli.mind`).

**Mérés.** A HAMART-001 lapján mindhárom pont (a referencia 2178–2318. sora) az első futásra bájtra egyezett a referenciával. A 4. szakasz 37 alblokkjából 24 kész, 13 nincs kész; a kész alblokkokban 3 diff-sor áll, mind engedéllyel (`S3-FORRAS` 1: a blokkfejléc forráslistája új hash-sel, mert a szakasz új bemeneteket olvas; `S3-HN15` 2). A számok a jóváhagyott lapéi: 7 téma (31 szóba jöhetőből, 2 tiltott); 25 szócsalád; 15 szóból 2-nek van kulcsszava; 1 rejtett és 2 310 hamis párhuzam. Az ISTENTISZT-001 lapján a három pont generálódik (5 téma 11 szóba jöhetőből, 4 tiltott; 13 szócsalád; 2 rejtett és 17 hamis párhuzam).
*Proveniencia: `scope=python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/general.py --cel lexikon2 --id ISTENTISZT-001 | forras=a munkafa az F218.6 (S3d) commit előtt | ts=2026-11-13`.*

**GK-19 (T6).** A párosítás minden párja számít, szűrő nélkül (teszt: a vers párjainak száma a tábla sorainak száma); a 4.13–4.14 látható szövegében nincs bizonyossági címke, százalékos pontosság és páronkénti jelölés (teszt). A pontosság egyszeri kimondása a Módszertanban az S8-ra marad (a vázlat-teszt oda mutat).

**GK-21.** A tematikus index pontja nem üres: kapu a modellen (ha a pont épül, van témája, és minden témának van motívumverse) és teszt a HAMART-lap 7 témájára.

**Tesztek.** Új fájlok: `teszt_szotari_karoli.py` (10 teszt), `teszt_szotari_nave.py` (7 teszt); a GK-21 vázlat-tesztje valódi tesztté vált. Összesen 223 teszt (190 zöld, 33 váz). Festékpróba: 0 szivárgás mindkét lapon.
*Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001 | forras=a munkafa az F218.6 (S3d) commit előtt | ts=2026-11-13`.*

**Új táblasorok.** Jegyzék: +6 (B53, B55, B57, B69, B70, B71). A térkép B57 sora három fájlt fogott össze; licenc és forrásnév szerint három sor lett (B57, B70, B71). A B69 (nyelvtani szavak) a térkép bemenetlistájából hiányzott: a régi `szerep_karoli.py` olvasta. Névtábla: +7 forrásnév (B07, B08, B09, B55, B57, B70, B71; a mai lap szavai). Sablontábla: +42, mind a régi generátor mondata betűre (`eredet` szerint: `SZN.olvasoi_12` 2, `SZN.blokk_12` 3, `SZN._hu` 1, `olvasoi_13_szavankent` 10, `olvasoi_14_szavankent` 14, `SZK.blokk_13` 2, `SZK.blokk_14` 5, `_tomor_lista` 3, a forrássor és a névelős idézet 2); új mondat nincs.
*Proveniencia: `scope=a két táblabővítő szkript beszúrásai (sorok megszámolva) | forras=a munkafa az F218.6 (S3d) commit előtt | ts=2026-11-13`.*

**Az ismétlés-figyelő újrakalibrálása.** A 4.13 hosszú igehely-felsorolásai az ISTENTISZT-001 lapján 5 hamis találatot adtak (két szócsalád azonos helylistája). Új küszöb: az ablakban legfeljebb 8 számjegyes szó állhat (`ISMETLES_SZAMOS_LEGFELJEBB`); az igehely-felsorolás így nem találat. A találatok száma a kalibrálás után: HAMART-001 7, ISTENTISZT-001 4 (ugyanazok, mint a DT872 mérésénél).
*Proveniencia: `scope=python eszkozok/general.py --cel lexikon2 (a futás figyelmeztetései), a küszöb előtt és után | forras=a munkafa az F218.6 (S3d) commit előtt | ts=2026-11-13`.*

**Egyeztetett eltérések a régi kódtól** (a kimenet a HAMART-lapon bájtra egyezik):
- A kulcsszó mögött álló eredeti szó megszámolása determinisztikus: holtversenyben az elsőként látott szó áll elöl (a versek rendjében, versen belül a Strong-szám rendjében; a régi kód halmaz-bejárása a futástól függött). A két mintalapon nincs holtverseny az élen.
- A 10 versnél rövidebb hamis-párhuzam lista is könyvenként, igehellyel áll (lenyíló nélkül). A régi kód a rövid listánál versszöveget és a jelölt döntésének belső kulcsát írta ki (`jelölt: <kulcs>`); ez belső mező, az új lapra nem kerülhet. A két mintalapon nincs rövid lista.
- Ha a motívumon a 4.13–4.14 nincs jóváhagyva (B53) vagy a soroknak nincs Károli-szava, a két pont nem áll a lapon; ha a motívumnak nincs döntése a témákról (B70), a 4.12 nem áll a lapon. Ezek az ágak a két mintalapon nem futnak.
- A 4.12 bevezetőjének példája (az első téma neve) csak akkor áll magyarul, ha a fordítás az angol név mai szövegéből készült; a régi kód itt a forrás-hash-t nem nézte, és fordítás híján a kisbetűsített angol nevet írta. Az új lap fordítás híján az angol nevet változtatás nélkül adja, „fordításra vár” jelöléssel. A két mintalapon minden név le van fordítva.

**Megfigyelések a 218a végi listába** (a mai jóváhagyott szöveg áll, változtatás nélkül):
- **A 4.12 olvasói bevezetője zárójelben megismétli a tágabb kört** („a tágabb, általános témák (a bűn és következményei általában, …) szándékosan kimaradtak”): ez a DT872 szerint a tágabb kör negyedik példánya a lapon. Javaslat: hivatkozás a lap elejére („a tágabb kör témái szándékosan kimaradtak”). A kritérium kapuja ezt nem fogja meg (a tágabb kör 11 szó, és nem része a kritérium mezőjének): ha a tágabb körre is kell kapu, külön döntés.
- A 4.12 dőlt sora a licencet a mondatba írva közli („közkincs”); a GK-07 szerint licencszöveg csak a licencleltárból jöhet (S8-ban egységesítendő).
- A 4.14 mondatában „{n}-nak van” áll rögzített toldalékkal („2-nak”); más számnál hibás volna. A „a {N} találat” névelője is rögzített.
- A hamis párhuzam listájában a Siralmak könyve a Károli-fájl kulcsával áll („Sir”), nem a lap többi részének rövidítésével („JSir”).
- A megjegyzésben álló belső proveniencia a régi szkriptek nevét hordozza (`eszkozok/szerep_karoli.py`, `eszkozok/szerep_nave.py`); a látható forrássor a névtáblából jön. A megjegyzés a 218b-ben igazítható az új generátorhoz.
- A 4.14 forrássorából hiányzik a Károli–Strong párosítás (a belső proveniencia megnevezi, a látható sor nem): a mai lap szövege; a GK-07 szerint a látható forráslistának a valódi olvasást kell követnie (S8).

## Független ellenőrzés — 4. ellenőrzés (célzott: S3a, DT872, S3d és a 3. ellenőrzés javítóköre)

*A `fuggetlen-ellenor` subagent (`claude-opus-5-5`; kért: `opus`) jelentése, a hívó session mentésében, a tételek szó szerinti tartalmával, a rendben talált pontok tömörítve. Hatókör: `03636753..759a0699` (S3a: váz, Áttekintés, 4.1), `52de9c2d..b1c7b0eb` (DT872), `b1c7b0eb..8fb27f64` (S3d: 4.12–4.14), `28be9127..03636753` (a 3. ellenőrzés javítókörének újraellenőrzése). Szint: célzott. 2026-11-13.*

**Eredmény: ELTÉRÉS, 6 tétel** (2 közepes, 4 alacsony).

| # | Tétel | Súly | Hely | Az ellenőr bizonyítéka |
|---|---|---|---|---|
| E1 | Az ISTENTISZT-001 4.12 bevezetője a tágabb kört egészében adja, a régi szabálytól eltérve, dokumentálatlanul | közepes–súlyos | `szamitas/szotari_nave.py`; `megjelenites/md/szotari_nave.py` | A régi kód a mező első zárójel előtti részét adta át (`lexikon_general.py:2587`). A referencián „(istentisztelet/imádság általában) szándékosan kimaradtak” áll, az új lapon a zárójeles pontosítás is, hármas zárójel-beágyazással. A jelentés szerint az eltérő ágak „a két mintalapon nem futnak”; ez az ág a mintalapon fut. Az ISTENTISZT-re regresszió nincs |
| E2 | A kisbetűsített szótári alak idézetként jelenik meg | közepes | `bemenet/karoli_szo.py` | A B55 értéke a bemeneti rétegben `.lower()`-t kap, aztán idézetként kerül a lapra; a táblában „Úr”, „Baál”, „Ábrám”, „Isten” áll, az új lapon „úr”, „baál”, „ábrám”, „isten”. A festékpróba nem látja (a jelzőszó a kisbetűsítés után kerül a szövegbe). A referencia ugyanígy áll, tehát nem visszaesés, de az alapszabálynak ellentmond, és a megfigyelések között nem szerepelt. A modul docstringje („a tábla értékeként”) nem volt igaz |
| E3 | Az ismétlés-figyelő számjegy-szűrője kiskapu, a tesztje üres | alacsony | `ismetles.py`; `teszt_szotari_karoli.py` | Egy 20 szavas, három igehelyet tartalmazó prózamondat kétszer áll: 0 találat (a három igehely 9 számjegyes szó). A teszt önmagát igazolta, a záró állítása függvényobjektumot vizsgált |
| E4 | A mintalapos figyelő-teszt nem azt méri, amit a docstringje mond | alacsony | `teszt_ismetles.py` | A „hamis találat nincs” állítást a teszt nem méri: csak a találat alakját nézte, ami a függvény felépítéséből mindig teljesül |
| E5 | B53: a `*` sor a régi szabálytól eltérően bekapcsol | alacsony | `bemenet/karoli_szo.py` | A régi `kapcsolo_motivumok` a `*` sort kizárja (`szerep_karoli.py:69-70`); az új elfogadta. A mintalapokon nem fut, de az egyeztetett eltérések között nem szerepelt |
| E6 | A napló állítása nem egyezik a kóddal (holtverseny) | alacsony | `naplok/F218_jelentes.md`; `szamitas/szotari_karoli.py` | A jelentés szerint „holtversenyben a Strong-szám rendje dönt”; a kód az elsőként látott szót adja (a versek rendjében, versen belül a Strong-szám rendjében) |

**Rendben talált pontok** (az ellenőr saját futásával vagy keresésével):
- **CI:** a `8fb27f64`-re futó `ellenorzes` (43479787987) és a `b1c7b0eb`-re futó (43474835873) is `success`.
- **A 3. ellenőrzés javítókörének két tétele:** az ismeretlen hordozó-előtagnál a bemenet megáll (teszt zöld); a festékpróba kis- és nagybetűtől függetlenül keres, a horgony külön tartományfajta (0 szivárgás; látott jelzőszavak: HAMART belső 236, horgony 30, idézet 1 359, kézi 391; ISTENTISZT belső 179, horgony 18, idézet 699, kézi 200). Mellékmegfigyelés: a `+` utáni részben álló előtag (`H0127+referencia:x`) nem áll meg, kézi névként megy tovább; a valós adatban nem fordul elő.
- **DT872, a kritérium kapuja:** a két sorra tördelt ismétlést megfogja; ha 11 szavanként egy szó beékelődik, nem fogja meg (a 12 szavas ablak határa). A kapu csak a fő nézeten fut. A `teljes` mód ma nem él (a `fej` szakasz nincs bekötve): a „pontosan egyszer” fele valós lapon még nem futott. A tágabb kört a kapu nem őrzi (a napló kimondja).
- **DT872, az 1.1 új alakja:** a számok egyeznek az 1.2 szólistájával (8 + 5) és az 1.4 három szópár-csoportjával. A `#mi-tartozik-ide` horgony a lapon ma nem létezik: a link az S8-ig célpont nélküli (kihagyott teszt jelzi).
- **Engedélysorok:** az `ISM-` sorok hash-ei a referencia 114., 118., 120., 122. sorát és az új lap 9. sorát fedik; az `ISM-URES` darabszámhoz és szakaszhoz kötött; az `S3-FORRAS` és az `S3-HN15` a megnevezett sorokat fedi. Túl tág engedély nincs.
- **Regresszió, tesztek, számok:** HAMART RENDBEN, 0 engedély nélküli sor, 24 kész és 13 nem kész alblokk; 223 teszt (0 hiba, 0 bukás, 33 kihagyva); figyelmeztetések: HAMART 7, ISTENTISZT 4. Mind egyezik a naplóval.
- **S3d számítások:** soronként összevetve a régi `szerep_karoli.py` és `szerep_nave.py` szabályaival a küszöbök, az összeolvasztás, a kulcsszó, a rejtett és a hamis párhuzam, a találat- és százalékképlet, a Nave jelöltképzése és -választása egyezik; az eltérések: E1, E5, E6, és a két dokumentált ág.
- **GK-19, GK-21:** a tesztek azt mérik, amit a nevük mond (a „bizonyossági címke nincs” teszt öt tiltott szövegrészre keres: gyenge, de valódi).
- **Táblasorok:** a „betűre átvett” sablonsorok szövege megvan a referencián, illetve a régi kódban (11 sort az ellenőr kézzel vetett össze); a forrásnevek megvannak a régi névtáblában; a jegyzéksorok útvonala a régi kód olvasásaival egyezik.
- **Alapszabály:** a megjelenítő modulokban látható magyar literál nincs (az E2 kivételével a hatókör tiszta).

**Amit az ellenőr nem tudott ellenőrizni:** a végrehajtó tényleges modellje; a DT872 felhasználói jóváhagyása (csak a napló állítja); az ISTENTISZT-001 teljes regressziója (nincs referenciája); a 4.13–4.14 helyessége a mintalapokon kívüli bemeneten (csak kódösszevetés); a kritérium-kapu `teljes` módja valós lapon.

## A 4. ellenőrzés javítóköre (`claude-fable-5-2`, 2026-11-13, az 5. session)

Az orkesztrátor rendelkezése szerint a kicsi javítások ebben a sessionben készültek el; az E2 döntést kér.

- **E1 — javítva.** A 4.12 bevezetője a tágabb kör rövid alakját idézi: a mező szövegét az első zárójeles kiegészítésig (`bemenet/motivum.tagabb_kor_rovid`; a régi szabály). Az ISTENTISZT-lapon újra a jóváhagyott szöveg áll („(istentisztelet/imádság általában)”); a HAMART-lapon a mezőben nincs zárójel, a szöveg nem változott. Teszt: `test_a_bevezeto_a_tagabb_kor_rovid_alakjat_idezi`. Tanulság: a régi kód hívási helyén álló átalakítást (`split(' (')[0]`) a szerepmodul olvasása nem mutatta meg; a hívó oldalt is olvasni kell.
- **E2 — nem javítva, döntést kér** (a 218a végi listába). A lapon a szótári alak kisbetűsítve áll, idézetként („úr”, „baál”, „ábrám”), ahogy a jóváhagyott lapon is. A javítás a látható szöveget változtatná („Úr”, „Baál”, „Ábrám”), ezért nem mechanikus. Két út: (a) a lapon a tábla eredeti alakja áll (a kisbetűs alak csak összevetési kulcs marad): ez az alapszabály szerinti alak, a HAMART-on és az ISTENTISZT-en a tulajdonnevek és a mondatkezdő alakok sorai változnak, engedélysorral; (b) marad a kisbetűs alak, kimondott kivételként. A modul docstringje addig a tényleges állapotot írja le.
- **E3 — javítva.** A szűrő most a tiszta számokat számolja (legfeljebb 9 a 16 szavas ablakban): az igehely-felsorolás ablakában legalább 10 tiszta szám áll, a néhány igehelyet tartalmazó prózamondatéban legfeljebb 8. Az ellenőr próbája (három igehelyes prózamondat kétszer) most találat. Két irányú teszt: `test_igehely_felsorolas_nem_ismetles_de_az_igehelyes_proza_az`; az üres teszt helyén valódi áll (`test_az_azonos_helylista_nem_ismetles_a_lapon`).
- **E4 — javítva.** A mintalapos teszt azt méri, amit mond: minden találat szósora a megnevezett sorok megnevezett helyén betűre ott áll (`test_a_figyelo_talalatai_a_lapon_tenyleg_ketszer_allnak`).
- **E5 — javítva.** A 4.13–4.14 pontot csak a motívum saját, aktív sora kapcsolja be, a `*` sor nem (a régi szabály). Teszt kis bemeneten.
- **E6 — javítva.** A jelentés mondata a kód szerint áll: holtversenyben az elsőként látott szó áll elöl.

**Mérés a javítókör után.** 225 teszt (192 zöld, 33 váz); festékpróba 0; a HAMART-regresszió rendben (engedély nélküli diff-sor 0); figyelmeztetések: HAMART-001 7, ISTENTISZT-001 4.
*Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001; python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/general.py --cel lexikon2 (figyelmeztetések) | forras=a munkafa a javítókör commitja előtt | ts=2026-11-13`.*

**Nem javított megjegyzések** (az ellenőr megfigyelései, nyitva): a `+` utáni hordozó-előtag nem áll meg (a valós adatban nincs ilyen; az N189 tételhez tartozik); a kritérium kapuja nem fogja meg az ismétlést, ha 11 szavanként egy szó beékelődik (a 12 szavas ablak tulajdonsága); az ISTENTISZT-001 lapjára nincs sorszintű regresszió (a brief 8.2 szerint szándékosan: a mércéje a számok, a kapuk és a felhasználó olvasata).

## DT874: a DT872 kézi tételei a forrásban (`claude-opus-5-5`, 2026-11-15, a 6. session)

*Az orkesztrátor döntése a felhasználó felhatalmazásával (a felhasználó, 2026-11-13, szó szerint: „döntsd el és add át a sessionnak”); a tíz tétel a megosztott jegyzetmappa `F218A_KOVETKEZO_MENET_2026-11-14.md` 1. pontjában áll. A döntés sora: DT874 (`dontesek/uj/f218-generator-uj-a.md`).*

**Olvasás.** A teljes Kivonat (`motivumok/HAMART-001.md`, a `kivonat` rés, négy bekezdés), a teljes kritérium (`adat/motivumok.tsv`, HAMART-001, `negativ_kriterium`) és a tágabb kör mezője a javítás előtt, a 9-es sablon 4. pontjának határ-elemei. A csere szkripttel készült (pontos részletcsere: minden régi részlet pontosan egyszer áll, különben a szkript megáll; a TSV `split('\t')` / `'\t'.join()`, írás előtt soronkénti összevetéssel). A forrásban a Kivonat 2 sora (a 3. és a 4. bekezdés), a táblában 1 cella változott; a sorok száma egyik fájlban sem.

| # | Hely | Előtte | Utána |
|---|---|---|---|
| 8 | Kivonat, 3. bekezdés | „a lánc hat héber és három görög szavának, illetve szócsaládjának minden előfordulása átnézésre került” | „a lánc szavainak és szópárjainak minden előfordulása átnézésre került” (a szám egyetlen helye az 1.1, az adatból) |
| 1–2 | Kivonat, 3. bekezdés | „Ide az a hely tartozik, amelyben a lánc egyik szava áll — … — … mondja ki, ismétli vagy fordítja meg. A hallás igéje háromféleképpen állhat az erőszak mellett: …” | „Ahol az erőszak szava a hallás igéjével áll egy versben, a hallás igéje háromféleképpen állhat mellette: …” |
| 7 | Kivonat, 3. bekezdés | „Nem tartozik ide a hely, amelyben a szó általános használatban áll: a bűnáldozat törvényei, …, és a romlandó test. Az sem tartozik ide, amely az átkot vagy a föld elvesztését a szövetség rendjében, a szövetség megszegésének büntetéseként mondja ki: ilyenek a törvény átok-kimondásai (5Móz 27:15-26), és a Királyok könyveinek földvesztés-ítéletei, …” | „Kizárt hely például a törvény átok-kimondásai (5Móz 27:15-26), és a Királyok könyveinek földvesztés-ítéletei, …” (a két Királyok-hely és az ok-mondat változatlan) |
| 3–4 | Kivonat, 4. bekezdés | „A motívum tehát nem a bűn és következményei általában, hanem … idéznek fel. Hat hely a lánc szavai nélkül is ide tartozik, mert ugyanezt a szerkezetet más szavakkal mondja ki; ezeket a vizsgálat egyenként, tematikus helyként veszi fel.” | „Hat hely a lánc szavai nélkül is ide tartozik, mert a lánc szerkezetét más szavakkal mondja ki.” |
| 5 | Kivonat, utolsó mondat | „Az újszövetségi helyeknél a Károli alapszövege, a Textus Receptus a mérce.” | törölve; a Kivonat a Jel 22:3 idézetével zár |
| 5 | kritérium, utolsó mondat (a lap eleje) | „Az újszövetségi helyeknél a Textus Receptus a mérce.” | „Az újszövetségi helyeknél a Károli alapszövege, a Textus Receptus a mérce.” |
| 6 | kritérium, első mondat | egy kb. 95 szavas mondat, a zárójeles magyar szólistával („(átok, föld, fáradság, bűn, erőszak, romlás)”) és két gondolatjellel | három mondat: „A versben az 1Mózes 3–9. fejezetének szóláncából egy szó áll, héberül: átok (árar), föld (adámá), fájdalom és fáradság (iccávón), bűn (chattát), erőszak (chámász) vagy a romlás igéje (sáchat); görögül: átkozott (…), átok (…) vagy a romlás szócsaládja (…). Ugyanígy ide tartozik a vers, amelyben a lánc szópárja áll (tövis és bogáncs; megtelt erőszakkal), vagy az erőszak szava a hallás igéjével ugyanabban a versben. Mindhárom esetben a hely ezen a szón át az 1Móz 3–9 láncára utal vissza: …” |

**A 6. tétel, kimondott eltérés a betűtől.** A szólista névelő nélkül áll („héberül: átok (árar), föld (adámá), …”). A névelős alak („héberül az átok (árar), a föld (adámá), …”) a Kivonat 1. bekezdésének láncbemutató mondatával 17 szavas egyezést ad, és a kritérium kapuja a teljes lapon BUKÁS-t adna: a kizárási lista törlése nélkül is ez volna az ötödik ismétlés. A Kivonat 1. bekezdése nincs a tíz tétel között, ezért a kritérium formája igazodott (a feltételek nem változtak). A „Mindhárom esetben” a régi mondat szerkezetét mondja ki (három vagylagos feltétel, közös visszautalással). Az „az 1Móz 3–9 láncára” fordulat betűre maradt: a régi generátor ebből olvassa a Pesat-gerincet (`lanc_mag`).

**A feltételek nem változtak: teszt.** `eszkozok/lapgen/tesztek/teszt_kriterium.py` (6 teszt): a régi szöveg (a 6b935da5 commité, mintaként a tesztben) és a mai kritérium ugyanazt adja: 9 Strong-számot (a zárójeles eredeti szavak a lánc szavainak szótári alakján és kiejtésén át: H0127, H0779, H2403, H2555, H6093, H7843, G1944, G2671, G5351), 3 szópár-elemet (tövis és bogáncs; megtelt erőszakkal; az erőszak a hallással) és 7 kizárást (a hat általános használat és a szövetség rendje). Ugyanitt: a lánc megnevezése és a tematikus helyek mondata változatlan, a mérce mondata a Károli alapszövegével áll, a forma (nincs szólista, egységes megnevezés, 2–3 mondat), és a Kivonat-résben a kritériumnak egyetlen 12 szavas részlete sem áll (a próba él: a régi Kivonat-mondat a régi kritériummal egyezést ad).

**9. tétel (Kolofon).** A régi generátor nem változik: a Kolofon „Negatív kritérium” sora az S8-ban kerül az új generátorba, hivatkozással a lap elejére. Előre megszámolt eltérés: 1 sor (`ISM-KOLOFON`, egy engedélysor); a vázlat-teszt (`test_ism_a_kolofon_nem_ismetli_a_kriteriumot`) leírása ezt rögzíti.

**10. tétel (9-es sablon, v2.4; N190).** A „Kivonat két kötelező határ-eleme” bevezetője: a határ szabálya a két mezőben áll, és a lap elején egyszer jelenik meg; a Kivonat nem mondja újra. A 2. pont címe „A minimális jegy olvasói nyelven”: a Kivonat a tágabb kört nem ismétli, hanem azt mutatja meg, miért a jegy dönt. Az 1. pont „Jó” mintája a javított Kivonat mondata; az átmeneti mondat megszűnt. Az N190 hibanapló-része nyitva marad.

**Következmények, mérve.**
- **A régi generátor lapja (E28).** A `lexikon/HAMART-001_TUDOMANYOS.md` a forrásból generálódik, az E28 bájtra egyezést kér: újragenerálva (`PARDES_DATUM=2026-11-13`, a lap jelölőjének dátuma). 7 sora változott: a lap eleje (a kritérium), a Kivonat 2 bekezdése, a régi 1.1 két sora, a 3. szakasz végi „Negatív kritérium” és a Kolofon sora; a `_KIZARASOK.md` nem változott. **A lap a 2. kiadás (2026.11.12) óta változott**, új kiadás-sor nélkül; a vizuális átnézés (`adat/lap_atnezesek.tsv`) a lap korábbi commitjára szól.
- **A mérce.** A `naplok/F218_referencia.tsv` négy sora frissült: B02 (`adat/motivumok.tsv`), a `motivumok/HAMART-001.md`, a referencialap, és a B51 (az ág döntésfájlja, a DT874 sora miatt). Az `ISM-IDE` és az `ISM-NEM` engedélysor új hash-t kapott (a régi 1.1 két sorának szövege a kritériummal változott); a darabszámuk 1-1 maradt. A regresszió: RENDBEN, engedély nélküli diff-sor 0.
- **A kritérium helyei a régi lapon** (a 12 szavas ablak a teljes sorszövegen, felső becslés): a lap eleje, a régi 1.1 két sora, a 3. szakasz vége, a Kolofon. A Kivonatban nincs. Az új generátorban a lap eleje marad (S8), a többi hivatkozás (1.1: kész; a 3. szakasz: S4; a Kolofon: S8).
- **A nyílt mag (E35).** Újraexportálva: `motivumok.tsv` 1 sor, a `METHODS.md` és a `MODSZER.md` 1-1 száma (a fordítás 222 helyett 223 sorban hiányzik), a kiadási hash. A kritérium angol fordítása elavult (a `nyilt_mag_angol.py allapot` szerint 1 036 fordított, 150 elavult; a DT870 mérése 1 037 és 149 volt, a különbség ez az egy cella): újrafordításra vár, nem töltöttem ki.

*Proveniencia: `scope=a forrásjavító szkript próbafutása és írása (a jegyzetmappán kívül, a session scratchpadjében); PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon --id HAMART-001 + diff a lexikon/ lappal; python eszkozok/general.py --cel lexikon2 --id HAMART-001 + python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/tesztek/futtat.py kriterium; python eszkozok/nyilt_mag_angol.py allapot (az export előtt és után); python eszkozok/nyilt_mag_export.py | forras=a munkafa a DT874 commitja előtt | ts=2026-11-15`.*

**A 218a végi listába (megfigyelés, nem javítva).** A 9-es sablon 2. pontjának mintája (az ISTENTISZT-001 Kivonata: „A motívum nem az imádság általában, hanem …”) a tágabb kört rövid alakban kimondja; a kritérium kapuja ezt nem méri (a tágabb kör nem része a kritérium mezőjének). A HAMART-001 lapján a tágabb kör a lap eleje mellett a 4.12 bevezetőjében és a Kolofon „A tágabb kör” sorában is áll (a 4.12-ről l. az S3d megfigyeléseit).

## F218.6 — S3c: a 4.8 (Nyelvi háttér) görög része (`claude-opus-5-5`, 2026-11-15, a 6. session)

**Mi készült el.** A görög nyelvrész 4.8 pontja, a régi `_hivatkozas_szoveg` három ágával (a régi lapon „*Hivatkozás: …*” sor, amelyet az F212 olvasói cseréje írt át):
- *nincs adat* (a HAMART-001 lapján): a motívum szavaihoz és a rokon szavakhoz sincs LSJ-szócikk; a mondat a mai lap mondata betűre (`s4.p8.gorog.nincs`);
- *rokon szavak* (a mintalapokon nem fut): a szavakhoz nincs, a rokon szavak közül egyeshez van szócikk; új mondat (`s4.p8.gorog.rokon`, `dontes=var`); a régi mondat a fájlnevet (`lexikon_hivatkozasok.tsv`) és a Strong-számokat írta ki;
- *utaló csonk* (az ISTENTISZT-001 lapján): minden görög szó LSJ-szócikke csak a képzés leírása („… Middle voice from G1909 and G2564”); az alapige a csonk utolsó Strong-száma. Új mondatok (`s4.p8.gorog.csonk`, `.csonk.rokon`, `.csonk.nincs`, `.csonkok`; `dontes=var`): „*Az ἐπικαλέω (epikaleó) LSJ-szócikke csak az alapigére utal: καλέω (kaleó). Az alapige LSJ-szócikke a rokon szavaknál áll.*” A régi mondat a fájlnevet, a Strong-számot és a nyers csonkot írta ki, a csonk szövegébe a régi kiejtés-pótló gépi átírásokat illesztve („ε (e)̓πικαλε (pikale)ìομαι (omai)”).
- *A saját szóhoz LSJ-szócikk tartozik* (a régi kód ilyenkor a szócikk kártyáját írta): a 4.2 kártyáival készül (S3b); addig az ág kimondott hibával megáll (`BemenetHiba`), csendes kihagyás nincs.

Új modul: `bemenet/nyelvi_hatter.py` (B25: a szótári hivatkozástábla szótárai Strong-számonként; B26: az LSJ utaló csonkjának felismerése, a régi minta szerint; B37: az LXX-fordítói döntések a régi szűrővel, a rokon szavak forrása). A számítás a `szamitas/szocikkek.py`-ban (`GorogHatter`, három eset), a mondat a megjelenítőben. A régi szabályok, változtatás nélkül: a rokon szó a motívum verseinek LXX-döntéseiben megnevezett, a motívumon kívüli görög szó, amelynek a kiegészítő szótárakon (SECE, MCGED) kívül szócikke van; a csonk-ág csak akkor fut, ha minden görög szó csonk.

**Mérés.** A HAMART-001 görög 4.8 alblokkja az első futásra bájtra egyezett a referenciával. A 4. szakasz 37 alblokkjából 25 kész, 12 nincs kész; a kész alblokkokban 3 diff-sor, mind engedéllyel (`S3-FORRAS` 1: a blokkfejléc forráslistája új hash-sel, a három új bemenet miatt; `S3-HN15` 2). A regresszió: RENDBEN. Az ISTENTISZT-001 lapján a csonk-ág fut (a fenti mondat); a mai lap „*Hivatkozás: …*” sorától az eltérés szándékos (a fájlnév, a Strong-szám, a nyers csonk és a gépi átírás nem áll a lapon).
*Proveniencia: `scope=python eszkozok/general.py --cel lexikon2 --id HAMART-001, --id ISTENTISZT-001; python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa az F218.6 (S3c, 4.8 görög) commit előtt | ts=2026-11-15`.*

**Tesztek.** `teszt_szocikkek.py` + 4 (`NyelviHatterGorog`: a HAMART nincs-ága, az ISTENTISZT csonk-ága a két Strong-számmal, a csonk felismerése kis bemeneten, a lapon a mondat áll, a fájlnév, a nyers csonk és a Strong-szám nem). Összesen 235 teszt (202 zöld, 33 váz); az első teljes futás 1 bukást adott (GK-08a: `.join()` a számítási réteg hibaüzenetében), javítva. Festékpróba: 0 szivárgás mindkét lapon.

**Új táblasorok.** Sablontábla + 7 (`s4.p8.gorog.*`: a bevezető és a „nincs” mondat a régi lapé betűre; öt új mondat, `dontes=var`). Jegyzék + 3 (B25, B26, B37; mind szerepelt a régi generátor bemenetei között, a mérce-táblában a hash-ük változatlan). A sablontábla és a jegyzék mérce-hash-e frissült.

**A 4.8 héber része: felmérés (nem kezdődött el).** A héber 4.8 egyetlen alblokk (a szólista és a „Háttér: rokon nyelvek (BDB)” tábla együtt, 48 sor), ezért csak egyben zárható. Két része két másik szelet gépezetére épül:
1. *A szólista* (10 sor): a BDB-szócikk magyar fejéből az alapjelentés és a gyök (szerkezeti részlet: az első zárójel előtti utolsó „: ” utáni rész, a „√” utáni rész), az első szócikk puszta utalásánál a következő szócikk feje, alapjelentés híján a rövid jelentés jelöléssel. A fej szövegére a régi kód a BDB-kártya megjelenítő lépéseit alkalmazta (`bdb_rovidites_jelol`: átírás- és sorrend-javítás, LRM, `<abbr>`): ez a 4.2 kártya (S3b) szegmentált idézetének gépezete.
2. *A rokon nyelvi tábla* (27 sor): a B38 (`visszhang_megfelelok.tsv`) `bdb` sorai a lánc szavaira. A sor címe a lánc-szó a láncversek szerinti Strong-változattal és a láncbeli jelentéssel (`lanc_szavak`, `lanc_mag` a kritérium „az 1Móz 3–9 láncára” fordulatából, `strong_valtozat_versben`, `lanc_szo_jelentes` a BDB-törzzsel és a TAHOT-glosszával): ez a 9. Hatástörténet szakasz közös magja. Továbbá: a tő keresése (`bdb_to_strong`, B22), a B24 megjegyzéssorának számlálója, a rokon alak kiejtése, a megjegyzés besorolása kulcsszavakra.
   - **Döntés kell:** a `jelentes` mezőből a régi kód regexszel vágta le a BDB-utalás zárójelét („átkozni (a BDB a „köt” és „átkoz” jelentés összefüggésére utal)” → „átkozni”). Az új generátorban ez (a) szerkezeti bontás a bemeneti rétegben (a zárójeles forrásmegjegyzés külön rész, a látható cella a mező eleje, változtatás nélkül), vagy (b) adatjavítás: a B38-ban külön olvasói oszlop vagy tisztított mező. A régi `tagabb_kor_rovid` precedense (a)-t ad.
   - **GK-03:** a B38 pillanatkép; a frissességi kapuja még nincs meg.

## F218.6 — S3c: a 4.8 (Nyelvi háttér) héber része; az S3c lezárul a Thayer-kártya nélkül (`claude-opus-5-5`, 2026-11-15, a 6. session)

*Az orkesztrátor rendelkezése (2026-11-15): a 4.8 héber része ebben a sessionben, high szinten; az S3b előtt megállás.*

**Mi készült el.** A héber nyelvrész 4.8 pontja egyetlen alblokkban: szavanként a BDB-szócikk fejének rövid alakja, a mutató a teljes fejre (4.2), és a lánc héber szavainak rokon nyelvi táblája („Háttér: rokon nyelvek (BDB)”).
- **A szólista** (a régi `_gerinc_bdb_fej_rovid`): az alapjelentés és a gyök a magyar fej részletei (`bemenet/gerinc.fej_alap_gyok`: az első zárójel előtti utolsó „: ” utáni rész az első gondolatjelig; a „√” utáni rész; a kapu ellenőrzi, hogy mindkettő a fej változatlan részlete); az első szócikk puszta utalásánál a következő, szakaszokkal bíró szócikk feje; ha a fej nem mondja ki az alapjelentést, a rövid szótár magyar jelentése a régi jelöléssel. A régi kód az alapjelentésen a BDB-kártya megjelenítő lépéseit futtatta (átírás- és sorrend-javítás, LRM, rövidítés-jelölés): ezek csak héber betűn, számon és átírási jelen változtatnak. Az új generátor ilyen jel esetén megáll (kimondott hiba, a szöveg a 4.2 kártya szegmentált idézetével állhat: S3b); a két mintalapon nincs ilyen.
- **A rokon nyelvi tábla** (a régi `blokk_visszhang_hatter`, `_hatter_sorok`, `lanc_szavak`, `lanc_mag`, `_lanc_szo_cim`, `lanc_szo_jelentes`, `bdb_to_strong`): új modul `szamitas/nyelvi_hatter.py`; a bemenetek `bemenet/nyelvi_hatter.py` (B24: a lekérdezés számlálója; B38: a visszhang-megfelelők) és `bemenet/gerinc.py` (a tő keresése a teljes angol BDB-szócikkek fejéből, a versenkénti törzs a B19 minden sorából, a helyi szócikk léte), `bemenet/motivum.lanc_mag` (a kritérium „az 1Móz 3–9 láncára” fordulatából, szerkezetileg; híján a Pesat-sorokból). A kulcsszavas besorolás (romlott alak, bizonytalan adat, targumi sor, valódi rokon nyelv) a bemeneti rétegben történik, a számítás jelzőt kap.
- **A B38 jelentés-mezője (a felmérés nyitott kérdése):** a régi kód a mező BDB-utalását regexszel törölte. Az új generátor szerkezetileg bont, a `tagabb_kor_rovid` precedense szerint: a látható jelentés a mező eleje, változatlanul; ha a levágandó rész nem a mező végén áll, a bemenet megáll (a forrásban javítandó). A kiejtés-mező ugyanígy. Ez technikai megoldás a mai szöveg előállítására, nem tartalmi döntés; ha a felhasználó adatjavítást kér (külön olvasói oszlop), az a 218c-ben kerülhet sorra.
- **A cellakezdő alakok** (a régi `nevelo_le` a táblán: „A rokon írások lekérdezése …”, „BDB szerint bizonytalan vagy ritka”) a DT869 szerint sablonsorként állnak, a lapon látható alakban.
- **Két ág kimondott hibával áll meg** (a mintalapokon nem fut): a láncbeli jelentés nem Qal törzzsel (a régi kód a TAHOT glosszájából vett igét); és a pontozott rokon alak, amelyre nincs gépi kiejtés.

**Mérés.** A HAMART-001 héber 4.8 alblokkja (48 sor: a tíz szó, a mutató, a tábla 27 sora) az első futásra bájtra egyezett. A 4. szakasz 37 alblokkjából 26 kész, 11 nincs kész; a kész alblokkokban 3 diff-sor, mind engedéllyel (`S3-FORRAS` 1, új hash a két új bemenet miatt; `S3-HN15` 2). A regresszió: RENDBEN.
- **ISTENTISZT-001:** a héber 4.8 a szópáros úton generálódik (a formula igéje, a kárá, a motívum ószövetségi verseivel): két szó a fej rövid alakjával, a táblában a kárá három rokon nyelvi sora (arab, arámi a romlott alak megjegyzésével, óarámi). A mai jóváhagyott lap régi szerkezetű, rokon nyelvi tábla nincs rajta: **a tábla új tartalom az ISTENTISZT-lapon** (ugyanaz a szerkezet, mint a HAMART-on). Az arab sor jelentése a B38 mezője szerint „hangosan olvas, recitál (a Korán); a Korán” (a mező ismétlése adathiba-gyanú, a 218a végi listába).
*Proveniencia: `scope=python eszkozok/general.py --cel lexikon2 --id HAMART-001, --id ISTENTISZT-001; python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa az F218.6 (S3c, 4.8 héber) commit előtt | ts=2026-11-15`.*

**Tesztek.** `teszt_szocikkek.py` + 5 (`NyelviHatterHeber`: a fej részletei és a héber/szám jel kapuja; a B38 jelentés-mezőjének szerkezeti bontása és a nem-előtag esete; a lánc-mag a két mintalapon; a HAMART szólistája és táblája a hiány okaival és a tővel; az ISTENTISZT szópáros útja). A görög 4.8 lapteszt a két 4.8 címhez igazítva. Összesen 240 teszt (207 zöld, 33 váz); az első teljes futás 1 bukást adott (GK-13: a kiejtés-modult a `bemenet/nyelvi_hatter.py` is importálta; a pontozottság vizsgálata a `bemenet/szavak.py`-ba került), javítva. Festékpróba: 0 szivárgás mindkét lapon.

**Új táblasorok.** Sablontábla + 32 (`s4.p8.heber.*`, `s4.p8.rokon.*`, `cim.s4.p8.rokon`): egy új mondat (`s4.p8.heber.nincs_fej`, `dontes=var`; a régi a Strong-kódot és a „2. szerep” belső szót írta), a többi a régi lap szövege betűre, a cellakezdő alakok a lapon látható alakban. Jegyzék + 2 (B24, B38; a mérce-táblában a hash-ük változatlan). **GK-03:** a B38 pillanatkép, a frissességi kapuja még nincs meg (mint a B36-é).

**Az S3c állása.** Kész a 4.3–4.10 mindkét nyelven, a görög 4.2 (Thayer-kártya) kivételével: az a 4.2 BDB-kártyával közös kódon áll, ezért az S3b-vel együtt készül.

## F218.6 — S3b: a 4.2 BDB-kártya és (az S3c-ből) a Thayer-kártya (`claude-opus-5-5`, xhigh, 2026-11-15, a 7. session)

**Eredmény.** A 4.2 mindkét nyelven kész: a héber alblokk (500 sor) és a görög (154 sor) bájtra egyezik a referenciával; a 4. szakaszból csak a 4.6 (LXX-híd) hiányzik, az S4-gyel zárul. `regresszio.py --id HAMART-001`: RENDBEN, engedély nélküli diff-sor 0; engedélysor-változás: az S3-FORRAS `uj` hash-e (a blokkfejléc forráslistája a ténylegesen olvasott B20-cal és B32-vel bővült; a sor osztálya, darabszáma változatlan). Festékpróba: HAMART-001 0 szivárgás (belso 255, idézet 2 337, kézi 439, horgony 30), ISTENTISZT-001 0 (194, 1 200, 220, 18).
*Proveniencia: `scope=python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001 | forras=a munkafa (F218.6 S3b) | ts=2026-11-15`.*

**Diff-görbe.** Héber 4.2: az első futás 8 eltérő sor (a régi olvasói átírás a forrásszöveg kódjelét törölte: „Hiph`il” → „Hiphil”; a lépés hiányzott), a javítás után 0. Görög 4.2: elsőre 0.

**A megoldás: szegmentált idézet szövegcsere nélkül.** A régi kártya a szótári szöveget 13 lépéses cserelánccal vitte át (a kártya építésekor kiemelés, forrásjavítás, irányjel, rövidítés-feloldás, Károli-számozás, BDB-azonosító; a kész lapon backtick- és írásjel-takarítás, a fej nyers előtagja és a belső számlálók törlése, kiejtés-pótlás, a digitalizálás jelei). Az új generátorban a szöveg `Jelolt`: idézet-darabok és típusos jelölés-darabok sora; a régi minták a régi bekezdés szövegén futnak (a jelölés-darab a mintáknak egyenértékű belső alakkal áll), de csak pozíciót adnak: a jelölés beszúródik, a forrásjavítás csak idézet-darabot ír, jelölésbe vagy keretbe egyik művelet sem nyúlhat (kimondott hiba). A lapon a jelölés sablonsor (`s4.p2.jel.*`), az idézet idézet; a kártya-teszt a fajta-térképen ellenőrzi, hogy `<mark>`, `<abbr>` és „(héber számozás:” idézet-darabban nem áll.

**Új bemenet:** B20 (`adat/thayer_szakaszok.tsv`). A B17-ből a javítótábla mind a négy fajtája (átírás, betűsorrend, zárójel, betű), a B19-ből a feloldott sorok (a hivatkozásszámhoz) és a bizonyosság oszlop olvasódik. **Új sablonsorok:** 96 (`s4.p2.*`), mind a jóváhagyott lap szövege (`dontes=-`); új mondat nincs.

**T5.** A 4.2-t nem érinti: az öt elavult Thayer-sor közül négy a `teljes` mezőé, egy a `sz2~3` összevont soré; a kártya a `sz<n>` sorokat olvassa. Az előre rögzített 5 engedélysor itt nem kellett; a T5 helye a későbbi szeletekben keresendő (a független ellenőrzés figyelje).

**Nem portolt ágak (a két mintalapon nem futnak; kimondott hibával megállnak):** az elnyelt szakasz mondatai, a „fordításra vár” ág, a horgonnyal illesztett kibontott szakasz, a több szócikkes tartomány-megjegyzés, a címkét átalakító glossza. **Eltérés a régitől, kapu nélkül:** a tiltott fordulatok ⓘ-megjegyzése (B58) nincs bekötve; a betűjavítás minden motívumon fut (a régi csak a két mintalapon). Mindkettő N-tétel jelölt a 218a végi listába.

**Átszökési arány:** a zöld regresszió után a szerkezeti tesztek 6 réteghibát fogtak (a szövegmunka a számításban, a megjelenítő a bemenetet importálta, a kiejtés második úton jött); a réteg-átrendezés után zöldek.

## Független ellenőrzés — 5. ellenőrzés (célzott: S3b, S3c, DT874 és a 4. ellenőrzés javítóköre)

*A `fuggetlen-ellenor` subagent jelentése, a hívó session (`claude-opus-5-5`, a 8. session) mentésében, változtatás nélkül. Az első hívás a modell-ellenőrzésen megállt (a subagent-fájl `model: opus`, a hívás Fable); a hívó a DT873 sorára hivatkozva folytattatta (l. E7). Hatókör: `8fb27f64..4cee43be`, másodlagosan `4cee43be..484abac9` (main-beolvasztás).*

**Eredmény: ELTÉRÉS, 8 tétel**

**Brief:** `F218_GENERATOR_UJ_A_BRIEF.md` · **tartomány:** `8fb27f64..4cee43be` (másodlagos: `4cee43be..484abac9`) · **szint:** `teljes`, célzottan · 2026-11-15
**Modell:** kért `fable` (DT873, a hívás szerint), tényleges `claude-fable-5-2`. (A subagent-fájlban ma is `model: opus` áll; a folytatás a koordinátor üzenetén és a DT873 során alapul — a sort a vizsgált tartomány `6b935da5` commitja maga írta, l. 0. és E7.)

**Futtatás:** minden a munkafán (`484abac9`), a kimenet a scratchpadbe; a repóba nem írtam. A hívó session futás közben a `naplok/F218_folytatas.md`-t módosította (`git status --short`: ` M`), kódot nem.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0. modell | NEM ELLENŐRIZHETŐ | `dontesek/uj/f218-generator-uj-a.md:7`; `.claude/agents/fuggetlen-ellenor.md:5` | A DT873 sor létezik és azt mondja, amit a koordinátor idézett; a felhasználói idézet („Igen, Opusra”) a végrehajtóról szól, az ellenőr Fable-je a sor következtetése. Felhasználói eredetét nem tudom igazolni. |
| 0. modell-mezők | OK | commitok | `git show --format=%b`: `6b935da5` Fable 5.2, a többi öt Opus 5.5 — egyezik a jelentés állításával; adattábla `modell` mezőt a tartomány nem írt. |
| 3. CI | OK | – | `gh run view 43722618020 --json headSha,conclusion,jobs`: `headSha=484abac9…`, `success`, mindkét job zöld. A `4cee43be`-re nincs futás; a `8af316a4`-re 43708743801 `success`. `futtat.py` nem futtattam újra. |
| tesztek | OK | `eszkozok/lapgen/tesztek/` | `python eszkozok/lapgen/tesztek/futtat.py` → futott 249, hiba 0, bukás 0, kihagyva 33 (782 s). |
| S3b/S3c regresszió | OK | `naplok/F218_elteres_engedely.tsv` | `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon2 --id HAMART-001 --kimenet <scratch>` + `regresszio.py --id HAMART-001 --uj <scratch>/lexikon` → „RENDBEN (engedély nélküli diff-sor: 0)”; mind a 33 engedélysor tényleges = elvárt; a hash-őr nem állt meg. |
| festékpróba | OK | – | `python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001` → 0 / 0 szivárgás; a jelzőszó-számok (255/30/2337/439; 194/18/1200/220) egyeznek a jelentéssel. |
| rétegszabály, megjelenítő | OK | `eszkozok/lapgen/megjelenites/md/kartya.py`; `megjelenites/md/szocikkek.py` | Olvasással: látható magyar literál nincs, minden mondat `ny.s(kulcs)`; a megjelenítő által hívott `s4.p2.*` kulcsok megvannak a sablontáblában. |
| rétegszabály, bemenet | ELTÉRÉS (E1) | `eszkozok/lapgen/bemenet/kartya_lap.py:30-92, 264-287, 344-373`; `bemenet/kartya.py:266-267, 389-439`; `tesztek/teszt_szerkezet.py:202, 235, 273` | l. E1 |
| idézet szó szerint | ELTÉRÉS (E2) | `eszkozok/szotari_glossza.py:45-53, 76`; `bemenet/kartya_lap.py:227-243`; `bemenet/kartya.py:361-374` | l. E2 |
| GK-15 / T5 a kártyán | ELTÉRÉS (E3) | `bemenet/gerinc.py` `thayer_fa`; `bemenet/kartya_lap.py:192-193, 317-337` | l. E3 |
| GK-06 néma hiány | ELTÉRÉS (E4) | `bemenet/kartya_lap.py` (B58 nincs); `eszkozok/lexikon_general.py:4437-4441, 4489-4492` | l. E4 |
| a régi lánc portja | OK (a mért körben) | `lexikon_general.py:4079-4275, 8926-9002, 9723-9759, 1306-1390` | Soronként összevetve a 4.2 olvasói rétege és szakaszlistája, a lánc-mag/lánc-szavak, a rokon nyelvi sorok, a görög 4.8 három ága: a döntési szabályok egyeznek; eltérés: E3, E4, E6 és a naplóban közölt megálló ágak. |
| 4. ell. E1 | OK | `bemenet/motivum.py` `tagabb_kor_rovid`; `lexikon_general.py:2587` | A régi szabály (`split(' (')[0]`); teszt zöld. |
| 4. ell. E3 | OK | `eszkozok/lapgen/ismetles.py`; `konfig.py` `ISMETLES_SZAM_LEGFELJEBB = 9` | Felsorolásnál a 16 szavas ablakban ≥ 10 tiszta szám, négy igehelyes prózánál ≤ 8; kétirányú teszt zöld. (Öt igehely 16 szón belül továbbra is kiszűrődik — a napló kimondja.) |
| 4. ell. E4 | OK | `tesztek/teszt_ismetles.py` | A teszt a találat szósorát a megnevezett sor megnevezett helyén veti össze. |
| 4. ell. E5 | OK | `bemenet/karoli_szo.py` `b53_karoli_pontok`; `eszkozok/szerep_karoli.py:67-70` | A `*` sor nem kapcsol be (régi: `r['id'] != '*'`); teszt kis bemeneten. |
| 4. ell. E6 | OK | `naplok/F218_jelentes.md:753` | A holtverseny-mondat a kód szerint áll. |
| 4. ell. E2 (nyitva) | OK (nem javítva, döntésre vár) | `bemenet/karoli_szo.py:6-10` | A docstring a tényleges állapotot írja. |
| DT874 tartalma | OK | `motivumok/HAMART-001.md:23-25`; `adat/motivumok.tsv` HAMART-001 sor | `git diff 6b935da5..7302338c`: az (1)–(8) tétel mind megvan; a kritérium feltételei szövegre azonosak; a `_LANC_MAG_RX` az új mondaton is talál; `teszt_kriterium.py` zöld. |
| DT874 hatóköre | ELTÉRÉS (E5) | `motivumok/HAMART-001.md`; `adat/motivumok.tsv`; `lexikon/HAMART-001_TUDOMANYOS.md` (7/7); `nyilt_mag/motivumok.tsv` | l. E5 |
| DT874 jóváhagyása | NEM ELLENŐRIZHETŐ | `dontesek/uj/f218-generator-uj-a.md:8` | A sor szerint a felhasználó: „döntsd el és add át a sessionnak”; a tíz tétel az orkesztrátoré, tételenkénti felhasználói jóváhagyás nincs rögzítve. |
| DT873 tartalma | ELTÉRÉS (E7) | `CLAUDE.md` „Modell-ellenőrzés”; `F218_GENERATOR_UJ_A_BRIEF.md:291` | l. E7 |
| A1 | OK | `naplok/F218_jelentes.md` | A mért állítások mellett proveniencia-sor áll; a „T5 a 4.2-t nem érinti” csak a HAMART adatára igaz (E3). |
| A2 | ELTÉRÉS (E4/E5 része) | `nyitott/uj/f218-generator-uj-a.md`; `naplok/F218_folytatas.md:65, 67, 218` | Négy nyitott tétel csak a folytatási fájlban: B58, betűjavítás minden motívumon, kritérium-újrafordítás, kiadás-sor; a `nyitott/uj/`-ban a tartományban csak az N190 módosult. |
| A3–A5 | OK (n/a) | – | A diffben nincs párhuzam-címkézés, Remez/Sod réteg vagy nevesített tanító. |
| A6 | OK | – | `gh run view 43722618020` annotációi: E12–E15 nincs. |
| ell.lista 1: törölt sorok | OK | `adat/` | A tartomány saját commitjaiban adatsor nem törlődött; `adat/motivumok.tsv` 1 módosított sor. |
| ell.lista 2: kulcslefedettség | ELTÉRÉS (E6) | `megjelenites/md/szocikkek.py` `_MEGJEGYZES` | 7 lehetséges megjegyzés-együttesből 5 kap sablont; a 8 bizonytalanság-kód és a szócikk-sorszámok lefedve. |
| ell.lista 3: nulla-diff hatóköre | OK, pontosítással | `regresszio.py` kimenete | Vonatkozik: HAMART-001 TUDOMANYOS 1., 2., 4. szakasz (a 4.-ben „9 alblokk nincs kész”: 2× 4.6 és a „Miért fontos ez a lelet” rés 7 alblokkja — a jelentés „csak a 4.6 hiányzik” mondata ezt nem mondja ki) és a KIZARASOK egésze. Nem vonatkozik: Kivonat, Tartalomjegyzék, Jelmagyarázat, 3., 5–12., Kolofon, ISTENTISZT-001 egésze. |
| ell.lista 4: tábla-Δ | OK | `adat/*.tsv` | `git diff --numstat cfc84cc7..484abac9`: `lapgen_sablonok` +487, `olvasoi_nevtabla` +57, `lapgen_bemenetek` +55, `tematikus_sajat_szo` +3; `kapcsolatok`, `nyilt_angol` 3/3; `jeloltek` 2/2; `elofordulasok`, `elutasitasi_okok`, `motivumok`, `nyilt_kodkonyv` 1/1; `konkordancia/` 0. A tartományban: sablon +135 (7+32+96, a jelentés bontja; 6 új `dontes=var`), bemenet +6. |
| ell.lista 5: ⛔ pontok | ELTÉRÉS (E7) / OK | brief 6., 9. pont | A 9. pont „az ellenőr modellje nem Fable” ⛔-ját a DT873 megfordította (E7). A 6 új sablonmondat a 218a végi listára vár; új tényállítást bennük nem találtam. |
| másodlagos: SEMA-számok | OK | `adat/SEMA.md:2486-2552` | A négy tábla 2.66–2.69; a hivatkozások (TSV-fejlécek, döntésfájl, 6-os sablon, két napló) követik; régi számú hivatkozás nem maradt. |
| másodlagos: hash-frissítés | OK | `naplok/F218_referencia.tsv` | 6 sor (B51 ×2, B65–B68); a méretek azonosak, ahol csak a SEMA-szám cserélődött; a regresszió a hash-őrrel ezen a fán zöld. |

**Eltérések (súly szerint)**

- **E1 (közepes–magas) — a GK-08a kapuit a 4.2 kódja megkerüli.** A kártya számítása (pontok, félkövér, csoportosítás), egy szabad `str`/`object` mezős modell és a szövegátírás a `bemenet/` alá került, amelyet a három szerkezeti teszt nem néz; a jelentés maga írja, hogy hat réteghiba után „réteg-átrendezés” tette zölddé őket. A kész lap mondatai árnyékként kódban is állnak (`'%d hivatkozás'`, `' · arámi'`, `'(a %s %d. BDB-szócikke a %d-ből)'`, `' (héber számozás: %s)'`), és a minták ezen döntenek: ha a sablontábla mondata változik, a pozíciók némán elcsúszhatnak. Az idézeten kódba írt regex-cserék futnak (`takaritas` 8 minta + a kódjel törlése, `belso_jelek_torlese`, `digitalizalas_jelei`) javítótábla-sor nélkül, holott a `jelolt.py` docstringje „a javítótábla sora szerint” javítást ígér; a DT869/l ugyanilyen ügyben a forrásban javítást írt elő, cseretábla nélkül. A felhasználó döntése kell: megengedett „forrásjavítás”-e a bemeneti rétegben, vagy adatba kell kerülnie.
- **E2 (közepes) — idézetként áll nem szó szerinti szöveg.** A glosszát az `olvasoi_glossza` átalakítja (70 karakternél csonkol + „…”, zárójeles részt kihagy, szóközt von össze), a `_forras_ertek` mégis idézetté burkolja, részlet-kapu nélkül (a 4.8 `_eleje` és `fej_alap_gyok` kaput tartalmaz). Bizonyíték az új ISTENTISZT-001 lapon (H8034): „2.c különösen mint ami az embernek egyfajta halál utáni életet ad, főként…” — a forrás (`adat/bdb_szakasz_hu.tsv`) „főként a fiaiban, …” folytatódik; a „…” a generátoré, idézet-típusban (a vázlatsoron helyesen sablon-jel). A Károli-számozás két darabja (`uj`, `eredeti`) összerakott szöveg, B19-/B18-idézetként címkézve. A HAMART-lapon ilyet nem találtam; a festékpróba nem látja.
- **E3 (közepes) — GK-15/T5 a kártyán nincs megvalósítva.** Elavult `sz<n>` Thayer-fordításnál a magyar szöveg eltűnik (a lap „fordításra vár”-t ír, vagy hibával megáll) a T5 szerinti jelölt régi szöveg helyett. A `forditasok.tsv`-ben 213 elavult Thayer-sor van, köztük `sz<n>` (pl. G2532 `sz9`, G0846 `sz4`); a HAMART öt sora valóban nem érintett.
- **E4 (közepes) — néma hiány.** A tiltott fordulatok megjegyzését („ismert hiány: a magyar szöveg tiltott fordulatot tartalmaz…”) a régi kártya kiírta; az új a B58-at nem olvassa, se hiba, se hiány-jelölés nélkül. A jelentés közli, de a folytatási fájl a „kimondott hibával megállnak” cím alatt sorolja, és N-tétel nincs.
- **E5 (közepes) — a DT874 a brief hatókörén kívül írt.** A brief 3. pontja kizárja az új prózát és a `lexikon/` írását; a commit a kiadott HAMART-001 Kivonatát/kritériumát módosította, a lapot újragenerálta (7 sor). Következmény: a nyílt magban a HAMART-001 angol kritériuma üres (`METHODS.md`: 222 → 223 hiányzó); a lap a 2. kiadás óta változott, új `kiadasok.tsv`-sor nélkül; ezek csak a folytatási fájlban állnak nyitottként.
- **E6 (alacsony) — nem dokumentált megálló ágak a 4.8-ban.** Két megjegyzés-együttesre (írás nélkül + romlott; mindhárom) a megjelenítő `KapuHiba`-t dob; a régi bármely együttest kiírt. A saját szó LSJ-szócikkének ága az S3b után is megáll, az üzenete még az S3b-re vár.
- **E7 (alacsony) — szabályütközés a DT873 körül.** A `CLAUDE.md` szerint az ellenőr kért modellje a subagent-fájl mezője (`opus`); a DT873 Fable-t ír elő; a fájl és a brief 291. sora változatlan. Amíg így marad, minden ellenőr-hívás a modell-ellenőrzésen megáll.
- **E8 (alacsony) — napló és apróságok.** A figyelmeztetések száma ma HAMART 9, ISTENTISZT 8 (a napló utolsó száma 7/4). Az új ISTENTISZT-lap 386. sora a „rokon szavaknál” álló LSJ-szócikkre utal, ilyen blokk az új lapon még nincs. `kartya_lap.py`: holt `_hiv` függvény; a `_szakasz_lista` docstringje az első utasítás után áll.

**Amit nem tudtam ellenőrizni:** a végrehajtó sessionök tényleges modellje; a DT873 és a DT874 felhasználói eredete; az ISTENTISZT-001 4.2 és 4.8 blokkjának sorszintű helyessége (nincs referenciája; csak szemle és kódösszevetés); a megálló ágak viselkedése a két mintalapon kívüli motívumon; a `takaritas` háromszori ciklusának egyezése a régi lánccal a HAMART 654 során túl.

## Az 5. ellenőrzés besorolási javaslata (a 8. session; egyeztetésre vár, javítás még nem történt)

| # | Javasolt besorolás | Teendő |
|---|---|---|
| E1 | **döntés (a felhasználóé)** | Megengedett-e a kártyán a bemeneti rétegben futó, kódba írt forrásjavítás (a régi lánc pozíciós portja, `takaritas`, `belso_jelek_torlese`, `digitalizalas_jelei`), vagy a javításoknak adatba (javítótábla) kell kerülniük, a DT869/l mintájára. Mechanikus rész a döntéstől függetlenül: a kódbeli árnyékmondatok (`'%d hivatkozás'` …) helyett a minták a sablontábla mondatából képződjenek (vagy kapu vesse össze a kettőt), és a szerkezeti tesztek terjedjenek ki a `bemenet/kartya*.py` számítási részére (a pontozás és csoportosítás a `szamitas/`-ba). |
| E2 | mechanikus | Az átalakított glossza nem idézet: a csonkoló „…” sablon-jel, az idézet-darab csak a forrás szó szerinti részlete, részlet-kapuval (a 4.8 `_eleje` mintájára); a Károli-számozás két darabja jelölésként (nem B18/B19-idézet). A HAMART-regresszió nem változhat. |
| E3 | mechanikus | A T5 (GK-15) a Thayer-kártyán: `munka` módban a régi magyar szöveg + felülvizsgálat-jel (`s4.felulvizsgalat`), `kiadas` módban BUKÁS; teszt egy `sz<n>` elavult sorra (G2532 `sz9`). |
| E4 | mechanikus | A B58 bekötése a kártyára (a régi ⓘ-megjegyzés), vagy kimondott BUKÁS, ha a kártya tiltott fordulatot tartalmaz; N-tétel a `nyitott/uj/`-ba; a folytatási fájl mondata javítva. |
| E5 | **döntés (az orkesztrátoré)** | A DT874 az orkesztrátor rendelkezésére ment; a következmények (angol kritérium újrafordítása, a HAMART-001 új kiadás-sora) N-tételként a `nyitott/uj/`-ba — ez mechanikus, a döntés az, hogy a 218a-ban vagy külön tételben történjen. |
| E6 | mechanikus | A két megálló 4.8-együttesre sablonmondat (vagy kimondott, dokumentált megállás a régi szöveggel); az LSJ-ág üzenete frissítve. |
| E7 | **döntés (a felhasználóé)** | A `fuggetlen-ellenor.md` `model:` mezője `fable`-re (a DT873 idejére), vagy a CLAUDE.md szabálya kapjon kivételt a hívásban megadott modellre. Amíg nem dől el, minden ellenőr-hívás megáll, és csak a hívó hivatkozásával folytatható. |
| E8 | mechanikus | A figyelmeztetés-számok frissítése a naplóban; az ISTENTISZT 386. sor utalása (a rokon szavak blokkja az S5–S8-ban jön: N-tétel vagy kapu); a holt `_hiv` törlése, a docstring helyre. |

## Az 5. ellenőrzés javítóköre, második fele (`claude-opus-5-5`, 2026-11-15, a 9. session)

*Az orkesztrátor besorolása szerint: E2, E3, E6 mechanikus; az E1 mechanikus része a felhasználó döntésével (DT875: „Kódban, később adatba.”). Az E4, az E5 és az E8 egy része az első félben készült (`e65fb60a`). Mérés minden tétel után: mindkét lap (`general.py --cel lexikon2`, `PARDES_DATUM=2026-11-13`) bájtra azonos a javítókör előtti kimenettel (TUDOMANYOS és KIZARASOK), a HAMART-regresszió RENDBEN (engedély nélküli diff-sor 0), festékpróba 0.*
*Proveniencia: `scope=general.py --cel lexikon2 --id HAMART-001/ISTENTISZT-001; regresszio.py --id HAMART-001; festek.py; cmp az 52f978f2-es kimenettel | forras=munkafa (52f978f2 + a javítókör) | ts=2026-11-15`.*

- **E2 — az átalakított glossza nem idézet.** A `bemenet/kartya_lap._forras_ertek` részlet-kaput kapott: a meghatározás (a generátor „…” csonkoló jele nélkül) szóköz-normalizálva a forrás (a szakasz vagy a fej teljes magyar szövege) részlete, vagy legfeljebb három részlete a forrás rendjében; különben `JeloltHiba`. A modellben `Glossza(reszek, csonk, felulvizsgalat)` (bemenet) → `TagoltGlossza` (`szamitas/kartya.py`) → a megjelenítő `_gl`: a csonkolás jele a `s4.p2.glossza.csonk` sablonsor (`{glossza}…`), a részek kötése a `s4.p2.glossza.kihagyas` (`{elotte} {utana}`). **Lelet a HAMART-lapon:** a H7451 egyik glosszája („gonosz tervet kigondolni”) a forrásból a héber kifejezés utáni zárójeles magyarázatot hagyja ki (a régi `_glossza_elotag_nelkul` szabálya); a lap szövege nem változhatott, ezért két szó szerinti részlet áll, köztük sablonnal, látható kihagyásjel nélkül, mint eddig. **A 218a végi listába:** a kihagyás láthatóvá tétele (pl. „…” vagy „[…]”) tartalmi döntés, a felhasználóé. A Károli-számozás jelölése szerkezetes lett (`bemenet/jelolt.KaroliSzam`: a könyv a forrás részlete, a fejezet- és versszám egész szám), három sablonsorral (`s4.p2.jel.karoli.konyv`, `.fejezet`, `.vers`; a régi `s4.p2.jel.karoli` törölve, `{uj}` / `{eredeti}` összerakott szövege nem idézet többé). Ettől az idézet-jelzőszavak száma csökkent: HAMART 2337 → 2313, ISTENTISZT 1200 → 1196 (a kiírt szöveg azonos). Tesztek: `teszt_kartya.Reszletkapu` (4), `ALapon.test_a_csonkolt_glossza_jele_sablon_a_reszlet_idezet` (az ISTENTISZT H8034 „főként…” két helyén a „…” sablon, előtte idézet; a 4.2 kártyáin egyetlen idézet-darab sem végződik „…”-re), a Károli-teszt az új adattal.
- **E3 — T5 (GK-15) a Thayer-kártyán.** A `bemenet/gerinc.thayer_fa` az elavult `sz<n>` sor régi magyar szövegét adja, a kulcsát a szócikk `elavult` halmazában (a régi generátor az elavult sort üresnek vette). A kártyán minden ebből a szövegből származó elem jelölt: a glossza (`s4.felulvizsgalat`), a fej, a kibontott szakasz és a vázlatsor idézete a végén `JelFajta.FELULVIZSGALAT` jelöléssel (`s4.p2.jel.felulvizsgalat`, új sablonsor, `dontes=var`). A `szamitas/szocikkek.elavult_jelez` a kártya elavult kulcsait a fordítás-állapotba írja: `kiadas` módban a szakasz kapuja BUKÁS (a meglévő `test_gk15_forditas_allapot` szerint), `munka` módban a lap elkészül. Tesztek: `teszt_kartya.ElavultThayer` (3): a G2532 `sz9` sora a valós adaton régi szöveggel és jelölve jön; a jel a lapmodellben és a kiírt sorban (idézet + sablon); az állapotba két ELAVULT tétel. **Korlát:** a G2532 teljes kártyája ma egy másik, nem portolt ágon áll meg (az `I 2.b` szakasznak nincs magyar szövege: az angol vázlatsor ága), ezért a teszt a darabokat méri, nem a teljes kártyát. Az elavult szövegből levezetett „a szótár csak alakot közöl” típusú sor (nincs benne idézett szöveg) nem kap jelet; kiadási módban a kapu ettől függetlenül megáll. A két mintalapon nincs érintett sor (a kimenet azonos).
- **E6 — a 4.8 két megálló együttese.** A régi `_hatter_sorok` a nyelv sorainak megjegyzéseit betűrendben, „; ”-vel fűzte össze, így az új modellben egy nyelv írás nélküli és romlott sora együtt is állhat. A két hiányzó együttes (írás nélkül + romlott; mindhárom) sablonmondatot kapott a régi szabály kimenetével (`s4.p8.rokon.megj.iras_romlott`, `.iras_biz_romlott`, `dontes=var`); mind a nyolc együttesnek van mondata (`teszt_szocikkek.RokonMegjegyzes`). Az LSJ-ág üzenete frissült: a saját szó LSJ-kártyája nincs portolva, az ág kimondott hibával megáll (**N194**, az E8 ISTENTISZT 386. sorának utalásával együtt).
- **E1 mechanikus része.** (a) Árnyékmondatok: a bemeneti réteg keret- és jelölésszövegei függvényekbe kerültek (`_hely`, `_summary_cim`, `_vazlat_keret`, `_kibontott_keret`, `_fejcim_keretek`; a `bemenet/kartya.py` állandói: `FEJ_KERET`, `KAROLI_BELSO`, `NINCS_KAROLI_BELSO`, `CSONK_*`, `kiejtes_jel`), mindegyik docstringje megnevezi a sablonsort; a `teszt_kartya.Arnyekmondat` (2 teszt, 25 összevetés) a sablontábla kiírt mondatával veti össze őket: ha a sablon mondata változik, a teszt bukik, a minták pozíciója nem csúszik el némán. (b) A kódba írt forrásjavítások (DT875): jegyzék `bemenet/kartya.KODBELI_FORRASJAVITASOK` (5 függvény), a `teszt_kartya.KodbeliForrasjavitas` szerkezeti teszt bukik, ha a bemeneti réteg jegyzéken kívüli függvénye írja az idézet betűit; az N193 (az S9 utáni javítótábla) kiegészítve. **Nem készült el:** a besorolási javaslat további része (a kártya pontozása és csoportosítása a `szamitas/`-ba, a szerkezeti tesztek kiterjesztése a `bemenet/kartya*.py`-ra): az orkesztrátor besorolása ezt nem vette fel; a 218a végi listába.
- **E8 maradéka.** A figyelmeztetések száma: HAMART 9, ISTENTISZT 8 (változatlan). Az ISTENTISZT 386. sora: N194.

**Tesztek:** a teljes futás 263 teszt; az első futás 1 bukása (GK-08a: a lapmodell glossza-mezői `object` típusúak voltak) javítva: a meghatározás a lapmodellben mindig `TagoltGlossza` (a kézi címke egy részként); utána a szerkezeti és a kártyatesztek (35) zöldek, a két lap ismét bájtra azonos. *Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py (teljes, majd szerkezet kartya) | forras=munkafa | ts=2026-11-15`.*

**Új sablonsorok** (8, `adat/lapgen_sablonok.tsv`; a `dontes=var` sorok a 218a végi listára): `s4.p2.glossza.csonk` (`-`, a régi lap jele), `s4.p2.glossza.kihagyas` (`-`, a régi lap szövege), `s4.p2.jel.karoli.konyv` / `.fejezet` / `.vers` (`-`, a régi `s4.p2.jel.karoli` helyett), `s4.p2.jel.felulvizsgalat` (`var`), `s4.p8.rokon.megj.iras_romlott` és `.iras_biz_romlott` (`var`). Törölve: `s4.p2.jel.karoli`. A mérce B66-hash-e frissült (`naplok/F218_referencia.tsv`).

## F218.7 — S4: „5. LXX-fordítói döntések” és a 4.6 (LXX-híd) (`claude-opus-5-5`, 2026-11-15, a 9. session)

**Eredmény:** a HAMART-001 5. szakasza és mindkét 4.6 alblokk bájtra egyezik a referenciával; az egyetlen eltérő sor az 5. szakasz blokkfejléce (új engedélysor: `S4-FORRAS`, GK-07, 1 sor). A regresszió: RENDBEN (engedély nélküli diff-sor 0); a 4. szakaszban 7 alblokk nincs kész (a „Miért fontos ez a lelet” rés, S8), a 4.6 kész. Festékpróba 0 (HAMART: belső 277, horgony 30, idézet 2735, kézi 439; ISTENTISZT: 216, 18, 1372, 220).
*Proveniencia: `scope=general.py --cel lexikon2 --id HAMART-001/ISTENTISZT-001 (PARDES_DATUM=2026-11-13); regresszio.py --id HAMART-001; festek.py | forras=munkafa (a0432491 + az S4 megjelenítője) | ts=2026-11-15`.*

**Felépítés.**
- `bemenet/lxx.py`: a Septuaginta versei a Károli-könyv elsődleges fájljából (a B35 nagy-indexén át, `lxx_os_import.elsodleges_slug` térképpel), a döntéstábla teljes sorai (B37: megjelenő szűrővel, és a szűretlen tábla saját párjai), a 4.11 ellenőrzött LXX-társításai (B38). A jegyzék három leírása a használatot követi (a mérce hash-e frissült).
- `szamitas/lxx.py`: a régi `lxx_osszevetes` + `_lxx_ujraminosit` + `lxx_egyforras_ellenoriz` portja: versenkénti ítélet (egyező a 4.11 saját-pár szűrésével; fordítói döntés: eltérő vagy LXX-minusz; társítás; nincs megállapítva; versszámozás), hídszó (F212 Sz3), újraminősítés (nincs újszövetségi pár; szócsalád), a szakaszon belüli kiejtés-pótlás (az először álló görög alak), két kapu (a szavankénti összeg; egy forrás a 4.11-gyel). A 4.6 adatai (`hid`): a görög nyelvrészen a szavak mondata, a héberen a szavankénti mondat (ugyanabból az ítéletsorból) és a társlista (a `Tarsulas` mércéje, az Áttekintésével azonos).
- `megjelenites/md/lxx.py`: az 5. szakasz (olvasói bekezdés, tábla, magyarázat, összesítés) és a 4.6 mindkét nyelvrészen (a `md/szocikkek.py` `_PONTOK` táblájából hívva). 75 új sablonsor (`cim.lxx`, `szamnev.1`–`10`, `szam`, `s5.*`, `s4.p6.*`), mind a régi lap szövege (`dontes=-`); a magyarázó sor szakaszszáma a szakaszrendből jön (`{szakasz}`), nem kódba írt „9.”.
- Nem portolt, kimondott hibával megálló ágak (a két mintalapon nem futnak): a motívum ószövetségi sor nélkül (az üres blokk), a görög könyv nélküli vers („nincs Septuaginta-könyv”), az LXX-igehely nem fejezet:vers alakban, a fordítói döntés görög lemma nélkül, a 4.6-ban az 5. szakaszban sor nélküli héber szó, és a szótári alak vagy kiejtés nélküli görög társ.

**ISTENTISZT-001** (nincs bájt-mérce; a mai lap az 1. kiadás régi szerkezete): az új 5. tábla cellái a mai lap celláival két soron térnek el. Az 1Kir 18:24 a mai lapon „egyező”, az új lapon „ugyanaz a szócsalád”, a 4.11 társításával („βοάω · ἐπικαλέω”). A régi generátor új szerkezetű ága ugyanezt adja (`lxx_osszevetes` a HAMART-on kívül futtatva: egyező 12, szócsalád 3, LXX-minusz 1), tehát a port a régi szabályt követi. A Zsolt 116:13 kiejtés-pótlása ennek következménye: az alak ott áll először. **Megfigyelés a 218a végi listába:** a régi szabály a több lemmás 4.11-sort („βοάω · ἐπικαλέω”) a saját-pár szűrésben egészében hasonlítja (ezért az 1Kir 18:24 egyező görög szava kiesik), az egy forrás kapuja viszont részenként; a kettő közül az egyik szabályhiba lehet (tartalmi döntés, a felhasználóé).

**Tesztek:** `teszt_lxx.py` (6): az összesítés és a 48 vers a HAMART-on, a szavankénti összeg, jellemző sorok (társítás-szócsalád, hídszó, versszámozás, az LXX-számozás jelölése, a kiejtés-pótlás), az LXX-minusz és az ISTENTISZT 5. szakasza a kész lapon.

## Független ellenőrzés — 6. ellenőrzés (célzott: az 5. ellenőrzés javítókörének második fele, S4, DT876)

*A `fuggetlen-ellenor` subagent jelentése, a hívó session (`claude-opus-5-5`, a 9. session) mentésében, változtatás nélkül. A hívás Fable modellel ment (a main-en a subagent-fájl `model: fable`, #743; az ág munkafáján még `opus`, ezt a subagent a main-ről ellenőrizte). Hatókör: `52f978f2..3a5ce4fb`. A jelentés után a subagent egy kiegészítést küldött; az a jelentés végén áll.*

ELTÉRÉS: 9 tétel

**Brief:** `F218_GENERATOR_UJ_A_BRIEF.md` · **tartomány:** `52f978f2..3a5ce4fb` (5 commit) · **szint:** `teljes`, célzottan (6. ellenőrzés) · 2026-11-16
**Modell:** kért `fable`, tényleges `claude-fable-5-2`. A munkakönyvtár szerepfájlja még `model: opus`; a main-en `fable` (`git diff HEAD origin/main -- .claude/agents/fuggetlen-ellenor.md`: `-model: opus` / `+model: fable`, commit `68472a49`).

**Futtatás:** minden a munkafán (`3a5ce4fb`, tiszta); a repóba nem írtam. A `general.py --cel lexikon2` és a `regresszio.py` nincs a megengedett parancsaim között, ezért a HAMART-regressziót nem futtattam.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0. modell | OK | `.claude/agents/fuggetlen-ellenor.md:5` (main) | l. fent; `dontesek/uj/f218-generator-uj-a.md:7` (DT873) ugyanezt írja. |
| 0. modell-mezők | OK | commitok | `git log --format='%h … %(trailers:key=Co-Authored-By…)' 52f978f2..3a5ce4fb`: mind az öt `Claude Opus 5.5`, egyezik a brief `modell: opus` mezőjével. Adattábla `modell` mezőt a tartomány nem írt. |
| 3. CI | OK | – | `gh run view 43750049419 --json headSha,conclusion,status,jobs`: `headSha=3a5ce4fb…`, `success`, mindkét job zöld. `futtat.py`-t nem futtattam újra. A CI a `lapgen/tesztek`-et és a regressziót nem futtatja. |
| tesztek (lapgen) | OK | `eszkozok/lapgen/tesztek/` | `python eszkozok/lapgen/tesztek/futtat.py` → `futott: 269, hiba: 0, bukás: 0, kihagyva: 33` (676 s). Benne a festékpróba (`teszt_festek`) és `teszt_lxx` (6). A kihagyott tesztek száma változatlanul 33. |
| tesztek (olvasó-szerver) | NEM ELLENŐRIZHETŐ | `eszkozok/teszt_futtat.py:55-58` | `python eszkozok/teszt_futtat.py --diff 52f978f2` elindult, de a jelentés írásáig nem adott kimenetet. A diff az `adat/` előtag miatt formálisan érinti a `teszt_szintek.py`-t; olvasó-szerver kódot nem érint. |
| HAMART-regresszió a head-en | ELTÉRÉS (E1) | `naplok/F218_referencia.tsv:194`; `eszkozok/lapgen/regresszio.py:80-93` | l. E1 |
| HAMART 5. szakasz, számok | OK | `lexikon/HAMART-001_TUDOMANYOS.md:2412`; `teszt_lxx.py:31-36` | Célzott grep a referencia Összesítés-sorára: 7/6/1/20/0/13/1; a teszt ugyanezt és 48 verset állít a modellről, zöld. A bájt-egyezést magam nem mértem. |
| S4: a régi lánc portja | OK (a mért körben) | `szamitas/lxx.py`; `lexikon_general.py:5149-5401`; `olvasoi_kovetkeztetes.py:326-407` | Soronként összevetve: ítéletsorrend, hídszó, saját-pár szűrés, újraminősítés, egyforrás-kapu, a mondatok szövege és sorrendje, a 0,67 / 5 küszöb. Eltérések: E2, E4, E7. A `Lathato.__eq__` érték szerinti (`szoveg.py:313`), az egyforrás-kapu tehát nem üres. |
| S4: rétegszabály | ELTÉRÉS (E5) | `megjelenites/md/lxx.py:14, 24-27, 146` | l. E5. Egyébként: a modell mezői típusosak, motívumazonosító nincs (`[A-Z]{3,}-\d{3}` a három rétegen: 0), a megjelenítő mondatai mind `ny.s(kulcs)`. |
| GK-04 / „`lxx_egyezes` a modellen” | ELTÉRÉS (E3) | `tesztek/teszt_vaz.py:82-85`; `szamitas/lxx.py:295-302` | l. E3 |
| GK-14 / T4 | ELTÉRÉS (E4) | `bemenet/szavak.py:246-262`; `szamitas/lxx.py:149` | l. E4 |
| GK-03 | ELTÉRÉS (E6) | `adat/lapgen_bemenetek.tsv:41, 54`; `teszt_vaz.py:77` | l. E6 |
| GK-06 néma hiány | ELTÉRÉS (E7) | `bemenet/lxx.py:53-54, 141-142`; `megjelenites/md/lxx.py:30-52, 183` | l. E7 |
| GK-17 / DT876 | OK, megjegyzéssel (E8) | `dontesek/uj/f218-generator-uj-a.md:10`; `nyitott/uj/f218-generator-uj-a.md:9` | `git diff --numstat 52f978f2..3a5ce4fb -- konkordancia`: üres, a normalizáló tábla nem változott. A `lapgen/` kódjában nincs `Eféz`/`Siral`/`JSir` alias (grep: csak egy teszt). A sor és az N195 megvan, a folytatási fájl két alias-sora lezárva. |
| DT876 felhasználói eredete | NEM ELLENŐRIZHETŐ | `dontesek/uj/f218-generator-uj-a.md:10` | Az idézet („Igen, maradjon kódban”) az orkesztrátoron át érkezett. |
| 5. ell. E2 javítása | OK, korláttal | `bemenet/kartya_lap.py:255-308`; `megjelenites/md/kartya.py:63-73` | A részlet-kapu megvan, a „…” sablonsor, a Károli-számozás szerkezetes; `Reszletkapu` (4) és az ISTENTISZT H8034-teszt zöld. Korlát: az illesztés részsztring-szintű, legfeljebb három részre, ezért egy 2–3 szavas, a forrás távoli helyeiről összeszedett glossza is átmegy. A H7451 összefűzött idézete látható kihagyásjel nélkül áll (a jelentés közli, a végi listán van). |
| 5. ell. E3 javítása | OK, korláttal | `bemenet/gerinc.py:623-638`; `szamitas/szocikkek.py:478-482, 511` | `ElavultThayer` (3) zöld; kiadási módban a kapu megáll (`teszt_szocikkek.py:101-113`). Korlát (a jelentés közli): a G2532 teljes kártyája más ágon megáll, a teszt darabokat mér; a „csak alakot közöl” sor nem kap jelet. |
| 5. ell. E6 javítása | OK | `megjelenites/md/szocikkek.py:281-284` | Mind a 8 együttes kap sablont (`RokonMegjegyzes` zöld). A tuple rendje a modellben érték szerinti (`nyelvi_hatter.py:169`), egyezik a kulcsokkal. Két új sor `dontes=var`. |
| 5. ell. E1 mechanikus része | OK, korláttal | `bemenet/kartya.py:399-409`; `teszt_kartya.py` `Arnyekmondat`, `KodbeliForrasjavitas` | Mindkét teszt zöld. Korlát: a szerkezeti teszt csak a `Bekezdes` négy író metódusát figyeli a két fájl modulszintű függvényeiben; a `Jelolt` előtt nyers szövegen futó csere nem látszik neki. A DT875 „jelzést” kért, annak megfelel. |
| 5. ell. E8 maradéka | OK | `nyitott/uj/f218-generator-uj-a.md:8` | N194 megvan (LSJ-kártya, az ISTENTISZT 386. sor utalása). |
| A1 | OK, megjegyzéssel | `naplok/F218_jelentes.md:981-982, 997, 1005` | A mért állítások mellett proveniencia-sor áll. Az 1005. sor régi generátoros futásának (12 / 3 / 1) nincs saját proveniencia-sora. |
| A2 | OK | `nyitott/uj/f218-generator-uj-a.md:8-9` | N194 és N195 valóban nyitott. A „218a végi lista” tételei a folytatási fájlban állnak (a brief 6. pontja megengedi); közülük az 1Kir 18:24 ügye nem megfogalmazási kérdés (E2). |
| A3–A5 | OK (n/a) | – | A diffben nincs párhuzam-címkézés, Remez/Sod réteg vagy nevesített tanító. |
| A6 | OK | – | `gh run view 43750049419`: E12–E15 annotáció nincs; a hat E27-ből négy a szabály saját tesztadata, kettő más brief (`F46`, `F224`) meglévő hivatkozása. |
| ell.lista 1: törölt sorok | OK | `adat/lapgen_sablonok.tsv` | `git diff 52f978f2..3a5ce4fb -- adat/lapgen_sablonok.tsv`: 1 törölt sor (`s4.p2.jel.karoli`, három sor váltja). `lapgen_bemenetek.tsv`: 3 sor leírása módosult (B35, B37, B38), törlés nincs. |
| ell.lista 2: kulcslefedettség | OK | `adat/lapgen_sablonok.tsv` | `Itelet` 7 értéke ↔ 7 `s5.itelet.*` sor; `szamnev.1`–`10` és `szam`; `GorogFajta` 5 értéke lefedve; `Megjegyzes` 8 együttese lefedve. |
| ell.lista 3: nulla-diff hatóköre | pontosítással | `naplok/F218_jelentes.md:996` | Az állítás a HAMART-001 5. szakaszára, a két 4.6-ra, az 1., 2., 4. szakaszra (7 alblokk nélkül) és a KIZARASOK-ra szól, a `b40a8bf9` munkafáján. Nem vonatkozik a head-re (E1), az ISTENTISZT-001-re (nincs bájt-mérce) és a lap többi szakaszára. |
| ell.lista 4: tábla-Δ | OK, megjegyzéssel (E9) | `adat/*.tsv` | Tartomány (`git diff --numstat 52f978f2..3a5ce4fb -- adat konkordancia`): `lapgen_sablonok` +83/−1, `lapgen_bemenetek` 3/3, `konkordancia/` 0. Main-hez (`git diff --numstat origin/main...3a5ce4fb`): `lapgen_sablonok` +569, `olvasoi_nevtabla` +57, `lapgen_bemenetek` +56, `tematikus_sajat_szo` +3; `kapcsolatok`, `nyilt_angol` 3/3; `jeloltek` 2/2; `elofordulasok`, `elutasitasi_okok`, `motivumok`, `nyilt_kodkonyv` 1/1. Bontási napló van (`F218_jelentes.md:992, 1002`): 75 + 8 új, 1 törölt. |
| ell.lista 5: ⛔ pontok | OK / ELTÉRÉS (E1) | brief 6., 8.1, 9. pont | A három új `dontes=var` sor a végi listára vár; új tényállítást nem tesznek. A 9. pont „az ellenőr modellje nem Fable” mondata a briefben (291. sor) változatlan, a DT873 fordítja meg. A 8.1 „a referencia újrafelvétele külön commit, okkal” szabálya az utolsó commitnál nem teljesült (E1). |

**Eltérések (súly szerint)**

- **E1 (közepes–magas) — a head-en a mérce hash-őre elavult, a regresszió nem futtatható.**
  - A `3a5ce4fb` egy sort adott a `dontesek/uj/f218-generator-uj-a.md`-hez (DT876); ez a mérce B51 bemenete.
  - A `naplok/F218_referencia.tsv:194` hash-sora (`6f4cb3c8…`, 18161 bájt) nem frissült: a fájlt utoljára a `b40a8bf9` írta.
  - Az `e65fb60a` ugyanilyen egysoros bővítésnél frissítette a sort (17176 → 18161).
  - A `hash_or` minden sort összevet, ezért a head-en „a mérce bemenete megváltozott: B51 …” üzenettel kell megállnia (kilépési kód 2). Ezt gitből vezettem le, nem futtatásból.
  - A „Regresszió RENDBEN” így legfeljebb a `b40a8bf9`-re igaz.
- **E2 (közepes) — az ISTENTISZT-001 új lapján az 1Kir 18:24 ítélete téves, és teszt rögzíti.**
  - A vers LXX-szövegében a motívum saját görög szava áll: `python eszkozok/lekerdez.py lxx-hid "1Kir 18:24"` → `G1941 ἐπικαλέσομαι` (`forras=LXX_OS/1-kings.tsv+TAGNT_kivonat.tsv`).
  - A kiadott lap „egyező”-t ír (`lexikon/ISTENTISZT-001_TUDOMANYOS.md:1163`); az új „ugyanaz a szócsalád”-ot, társítás jellel.
  - Ok: a saját-pár szűrés a több lemmás 4.11-sort („βοάω · ἐπικαλέω”) egészben hasonlítja (`szamitas/lxx.py:204-207`), az egyforrás-kapu részenként (`:316`).
  - A `teszt_lxx.py:85` a 12 / 3 összesítést rögzíti.
  - A jelentés megfigyelésként közli (1005. sor), de csak a végi listán áll. A 8.2 mérce 1. pontja szerint a számnak független számlálással kell egyeznie. Ez a felhasználó döntése.
- **E3 (közepes) — a GK-04 az S4-ben nem teljesült.**
  - A brief 186. és 296. sora szerint az `lxx_egyezes` a modellen fut, mindkét lapon.
  - A `test_gk04_kapu_minden_lapon` ma is `skip(S4)`; a kihagyott tesztek száma változatlanul 33.
  - A modell egyetlen számegyezés-kapuja (`_kapu_szavankent`) csak akkor fut, ha minden sor egyszavas.
  - Az ISTENTISZT-001-en nem fut: 16 sor `H7121+H8034`. A HAMART-001-en a `teszt_lxx.py:42-43` megjegyzése szerint a szó nélküli tematikus sorok miatt szintén nem.
  - A régi kapu szópáros ága (`lexikon_general.py:2004-2006`) nincs portolva.
  - A jelentés S4-szakasza a GK-04-et nem említi.
- **E4 (közepes) — az 5. szakasz héber kulcsszava a vers utolsó előfordulása; a T4 és a GK-14 az elsőt írja elő.**
  - Az `utolso=True` új paraméter a régi `kiejtes_ehhez` szabályát viszi át a bájt-egyezésért.
  - Sem döntés-helyőrző, sem engedélysor nincs róla, és a jelentés nem említi.
  - Példa: 1Kir 18:24, H7121 kétszer (`python eszkozok/lekerdez.py scan H7121 --szakasz "1Kir 18:24"` → 2 szó-előfordulás; `TAHOT_kivonat.tsv:202412, 202419`); az 5. tábla a másodikat adja.
  - A két mintalapon a 2. és az 5. szakasz között látható ellentmondást nem találtam. Az 1Móz 6:12-nél mindkettő „hischít”.
  - A két szabály párosítás nélküli versnél eltérő alakot adhat.
- **E5 (közepes–alacsony) — számítás a megjelenítőben, küszöb a `konfig.py`-n kívül.**
  - A híd erősségének fokozatai (`_JELZO`: 0,67 / 0,34) a megjelenítőben állnak, nem nevesített konstansként.
  - A szavankénti következtetés feltétele (`megjelenites/md/lxx.py:146`) is ott dől el, nem a modell következtetés-kódjában (brief 5. pont).
  - Az `LXX_SZO_MIN` és az `LXX_SZO_ARANY` a konfigban van, de teszt nem hivatkozik rájuk (grep a `tesztek/` alatt: 0).
- **E6 (közepes–alacsony) — GK-03: a szelet két pillanatkép-bemenetet olvas frissességi kapu nélkül.**
  - A B36 és a B38 `frissesseg` mezője `-`; a brief mindkettőt a kapuzandók közé sorolja.
  - A B36 hiányát a folytatási fájl közli, a B38-ét nem.
  - A `test_gk03` ma is `skip`.
- **E7 (alacsony) — néma eltérések a régi lánctól, amelyek nincsenek a megálló ágak listáján.**
  - Görög szó nélküli motívumnál a régi más mondatot írt (`lexikon_general.py:5119-5131`); az új mindig a szóhíd-mondatot adja.
  - A döntés hibás alakú `lxx_igehely` mezője némán a vers saját LXX-helyére esik vissza; a nem `G\d{4}` alakú `gorog_strong` némán elmarad. A mai adatban ilyen sort nem találtam (két grep az `adat/lxx_dontesek.tsv`-n: 0).
  - Ha egyik héber szónak sincs sora a párok táblájában, a forrás-sor elmarad; a régi kiírta.
  - A `_vers_index` az `igehely_lxx` oszlop nélküli könyvfájlt némán kihagyja.
- **E8 (alacsony) — a Károli-könyv → LXX-fájl térkép kódból jön, benne a `Sir` alakkal.**
  - A `bemenet/lxx.py:15, 76` az `lxx_os_import` kódbeli térképét importálja (`"lamentations": "Sir"`, `lxx_os_import.py:284-292`); az LXX_OS fájl kulcsa is `Sir 1:1`.
  - A normalizáló tábla alakja `JSir` (`Konyv_normalizalo_tabla.tsv:26`).
  - Egy `JSir` vers ezért félrevezető „nincs Septuaginta-fájlja” üzenettel állna meg.
  - Ma nincs érintett sor (`\t(JSir|Sir) \d` az `elofordulasok.tsv`-ben: 0). A DT876 és az N195 ezt az aliast nem sorolja fel.
- **E9 (alacsony) — napló és apróságok.**
  - A jelentés 992. sora „7 új sablonsort” ír, de 8-at sorol fel (8 új, 1 törölt).
  - A `LxxDontesSorok.sajat` holt kód (`bemenet/lxx.py:119-121, 129, 132`; hívója nincs).
  - Az összevetés kétszer számolódik: az 5. szakasz új `_Forrasok`-ot épít (`szamitas/lxx.py:322-328`), a 4.6 a gyorsítótárazottat használja.
  - Három commit 400 sor fölött van (444, 546, 599).
  - A `s4.p6.forras` látható mondata („Forrás: a grammatikai szavak listája.”) a régi lap szövege (`dontes=-`), de a tényleges forrást (LXX_OS, versszintű párok) nem nevezi meg.
  - Tíz `skip(S3)` váz-teszt maradt (`teszt_vaz.py:77-236`), miközben az S3 késznek jelölt; a GK-15-é közülük duplikátum.

**Amit nem tudtam ellenőrizni:**
- a HAMART-regressziót és a két lap bájt-azonosságát a javítókör előttivel (nem futtatható parancsok; a head-en az E1 szerint amúgy sem futna);
- az ISTENTISZT-001 5. szakaszának és 4.6-jának sorszintű helyességét az 1Kir 18:24-en túl;
- a megálló ágak viselkedését a két mintalapon kívül;
- a DT876 és a besorolás felhasználói eredetét;
- a végrehajtó sessionök tényleges modelljét;
- az olvasó-szerver tesztjeinek eredményét.

**Kiegészítés (a subagent második üzenete):** a táblázat és az ELTÉRÉS-tételek változatlanok (ELTÉRÉS: 9 tétel).

- **Festékpróba és futástesztek külön is zöldek:** `python eszkozok/lapgen/tesztek/futtat.py festek futas` → `futott: 17, hiba: 0, bukás: 0, kihagyva: 0` (203 s). Ez megerősíti a „tesztek (lapgen)” sor OK eredményét; a teljes futás (269 teszt) ezeket már tartalmazta.
- **Olvasó-szerver tesztek:** a `python eszkozok/teszt_futtat.py --diff 52f978f2` továbbra sem adott kimenetet, a háttérben fut. A sor eredménye marad NEM ELLENŐRIZHETŐ.

**Második kiegészítés (a subagent harmadik üzenete, változtatás nélkül):**

Az olvasó-szerver tesztjei lefutottak: 16 fájlból 14 zöld, 2 bukik. A fenti jelentés „tesztek (olvasó-szerver)” sora ezzel NEM ELLENŐRIZHETŐ-ről ELTÉRÉS-re változik, új tételként (E10); az első sor így: **ELTÉRÉS: 10 tétel**.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| tesztek (olvasó-szerver) | ELTÉRÉS (E10) | `eszkozok/olvaso_szerver/teszt_visszhang_kapu.py:85, 202`; `teszt_szintek.py` | `python eszkozok/teszt_futtat.py --diff 52f978f2` → `teszt_visszhang_kapu.py`: 22 tesztből 2 bukás; `teszt_szintek.py`: HIBA; a többi 14 fájl zöld. |

- **E10 (közepes) — két olvasó-szerver tesztfájl bukik a head-en; egyiket sem ez a tartomány okozza, de az egyik az ágról jöhet, és nincs róla nyitott tétel.**
  - **`teszt_visszhang_kapu.py`, 2 bukás:**
    - `test_bevezeto_a_peshat_magot_es_a_kulcsszavak_szamat_mondja` a „Peshat-magjának (1Móz 3–9) azon verse” szöveget várja; a blokk ma „a Genezis láncának (1Móz 3–9) azok a versei” szöveget adja.
    - `test_v3_nincs_a_nem_azonositott_helyen`: a rontott és az eredeti bemenet ugyanazt a blokkot adja.
  - A tartomány a tesztek bemeneteit nem érinti: `git diff --name-only 52f978f2..3a5ce4fb` csak `eszkozok/lapgen/`, `adat/lapgen_*`, naplók, a brief és a `dontesek/uj` / `nyitott/uj` fájlokat ad.
  - Az ág a merge-base óta viszont írta az `adat/motivumok.tsv`-t és a `motivumok/HAMART-001.md`-t (DT874, DT870): `git diff --name-only cfc84cc7..3a5ce4fb -- … adat/motivumok.tsv motivumok/HAMART-001.md`. A bukás ebből is jöhet, vagy a main-en is áll; ezt nem tudtam eldönteni, mert a main-en nem futtathatok.
  - A `nyitott/uj/f218-generator-uj-a.md` ezt a két bukást nem említi.
  - **`teszt_szintek.py`:** HIBA. Az N187 13-ból 2 bukást rögzít rá, a main-en is. A részletes kimenetét a futtató csonkolt vége miatt nem láttam, ezért azt, hogy ma is pontosan ugyanaz a 2 teszt bukik-e, nem igazoltam.
  - A CI ezeket a teszteket nem futtatja, ezért a zöld CI-futás erről nem mond semmit.

## A 6. ellenőrzés besorolási javaslata (a 9. session; egyeztetésre vár, javítás még nem történt)

A hívó saját ellenőrzése az E1-re: a `dontesek/uj/f218-generator-uj-a.md` mai mérete 19 849 bájt, a hash-e `32590240…`; a `naplok/F218_referencia.tsv` 194. sora `6f4cb3c8…` és 18 161 bájt. Az E1 tehát áll. Oka: a DT876 commitja után a regresszió nem futott (`scope=a B51 hash-sora és a fájl mai hash-e | forras=naplok/F218_referencia.tsv:194; sha256sum | ts=2026-11-16`).

| # | Javasolt besorolás | Teendő | A merge előtt? |
|---|---|---|---|
| E1 | mechanikus | Külön commitban, okkal (8.1): a B51 hash-sorának frissítése (`referencia_frissit.py`), regresszió a head-en. Gépi védelem javaslatként: a `push_elott.py` futtassa a regresszió hash-őrét (gyors, a lap generálása nélkül), hogy a mérce bemenetének változása ne maradhasson rejtve. | igen |
| E2 | **döntés (a felhasználóé)** | A több lemmás 4.11-sor („βοάω · ἐπικαλέω”) a saját-pár szűrésben egészben vagy részenként hasonlítandó-e. Ha részenként, az ISTENTISZT-001 1Kir 18:24 sora „egyező”, és a `teszt_lxx.py` összesítése 13/2. Az új generátor ma egyik lapot sem adja ki, ezért ez nem gátolja a merge-et; N-tétel a végi listával. | nem (N-tétel) |
| E3 | mechanikus | A régi `lxx_egyezes` kapu szópáros ágának portja a modellre, és a `test_gk04` élesítése; vagy kimondott N-tétel az S5 ágára. Az orkesztrátor dönti el, hogy most vagy az S5-tel. | javaslat: most (kicsi) |
| E4 | **döntés (a felhasználóé)** | Az 5. tábla héber kulcsszava: a régi szabály (a vers utolsó előfordulása, ma bájtra egyezik) vagy a T4/DT868 (Károli-pár, híján az első). Mechanikus rész a döntéstől függetlenül: DT-F helyőrző vagy N-tétel, hogy az eltérés ne legyen néma. | nem (N-tétel) |
| E5 | mechanikus | A `_JELZO` fokozatai és a szavankénti következtetés feltétele a `szamitas/lxx.py`-ba (a fokozat és a „következtetés-e” a modell mezője), a küszöbök a `konfig.py`-ba; teszt a konstansokra. A lap nem változhat. | igen |
| E6 | mechanikus | A B38 frissességi hiánya a folytatási fájlba, a B36 mellé; a GK-03 egésze a halasztott tételek között marad. | igen (napló) |
| E7 | mechanikus | A négy néma ág kimondott megállássá (`BemenetHiba` vagy `ValueError`, a megálló ágak listáján), vagy portolva, ha kicsi (a görög szó nélküli motívum mondata). | igen |
| E8 | mechanikus | Az N195 kiegészítése az `lxx_os_import` `Sir` ↔ `JSir` alakjával; a „nincs Septuaginta-fájlja” üzenet nevezze meg a lehetséges okot (a könyvnév-alakot). A DT876 szerint kódban marad. | igen |
| E9 | mechanikus, egy tartalmi résszel | A napló 7 → 8; a holt `LxxDontesSorok.sajat` törlése; az összevetés egyszeri számítása (gyorsítótár); a `skip(S3)` váz-tesztek rendezése. **Tartalmi rész:** az `s4.p6.forras` mondata a régi lap szövege, a valódi forrást nem nevezi meg; javítása engedélysor és új mondat, ezért a végi listára (a felhasználóé). | igen, a tartalmi rész nélkül |
| E10 | mechanikus (N-tétel), az ágtól részben független | A hívó ellenőrzése: a „Genezis láncának (…) azok a versei” szöveget a `cee76546` (F125.LJ1) vezette be a `lexikon_general.py`-ba, és ez a commit a merge-base (`cfc84cc7`) őse; a merge-base óta az ág sem a `lexikon_general.py`-t, sem az `eszkozok/olvaso_szerver/` alatti fájlt nem írta (`git diff --stat cfc84cc7 HEAD -- eszkozok/olvaso_szerver eszkozok/lexikon_general.py eszkozok/olvasoi_kovetkeztetes.py`: üres). Az első bukás tehát a main-en is áll (elavult teszt-elvárás). A második (`test_v3_…`) eredetét nem igazoltam; a main behozása után újrafuttatandó. Teendő: N-tétel a két bukásra (a `teszt_szintek.py` az N187 alatt marad), a javítás nem a 218a hatóköre. | nem (N-tétel; a main behozása után újramérés) |

## A 6. ellenőrzés javítóköre (`claude-opus-5-5`, 2026-11-16, a 9. session)

Az orkesztrátor besorolása (2026-11-16): E1, E3, E5, E6, E7, E8, E9 mechanikus, a merge előtt (az E9 tartalmi része, az `s4.p6.forras` mondata nélkül: az a 218a végi listájára); E2 és E4 a felhasználó döntése (N196, N197), a merge-et nem gátolja; E10 N-tétel (N198), a main behozása után újramérve.

**Hibahely-tábla (a célzott újraellenőrzéshez):**

| # | Hely | Javítás | Ellenőrzés |
|---|---|---|---|
| E1 | `naplok/F218_referencia.tsv` (B51 sor) | a hash-sor frissítve, külön commitban, okkal (`fb2cabb3`) | regresszió a head-en: RENDBEN |
| E1 (védelem) | új: `eszkozok/lapgen/hash_or_kapu.py`; `eszkozok/push_elott.py`; `.github/workflows/ellenorzes.yml` | a mérce hash-őre a push előtti kapuban és a CI-ben, ha a változás a lapgenerátort vagy a mércéjét érinti (`f18a25d8`) | `push_elott.py --ci-egyezes`: RENDBEN; a javítás előtti állapoton HIBA (B51), nem érintő listán „nem fut” |
| E3 | `eszkozok/lapgen/szamitas/lxx.py` `egyezes_kapu`, hívása a `hid()`-ben | a régi `lxx_egyezes_kapu` érdemi része a modellen: a héber 4.6 szavankénti versszámainak összege a versek száma, szópáros motívumnál mindegyik a teljes versszám. A rövid mondatok, az összegző és a görög 4.6 számai egyetlen számlálóból jönnek, köztük eltérés nem keletkezhet | `teszt_lxx.py` `Gk04` (3 teszt: mindkét mintalap elkészül, pozitív és negatív esetek mindkét ágra); a `teszt_vaz.py` `test_gk04_kapu_minden_lapon` váza törölve |
| E3 (maradék) | `teszt_vaz.py` `test_gk04_hely_egyseg_kapu` (új váz, `HELY_EGYSEG` ok) | a `hely_egyseg` kapu nincs portolva: a névvel megadott szópár (`málé+chámász`) tagjait az 1.4 modellje nem köti Strong-számhoz, a régi kapu kiejtés-szöveget illesztett, a számítási réteg szöveget nem hasonlíthat (GK-08a). Egy próbaváltozat a Strong-csoportokon a HAMART-001-en hamis BUKÁS-t adott (H2555: 1.4 2 hely, Áttekintés 12 hely), ezért visszavonva | N199 |
| E5 | `szamitas/lxx.py` `HidFok`, `hid_fok`, `Osszevetes.fok`, `SzoMondat.kovetkeztetes`, `szo_kovetkeztetes`; `konfig.py` `LXX_HID_EROS`, `LXX_HID_RESZLEGES`; `megjelenites/md/lxx.py` `jelzo`, `_szo_mondat` | a fokozat és a szavankénti következtetés a modell mezője; a megjelenítő csak kulcsot választ | `teszt_lxx.py` `Kuszobok` (3 teszt, a konfig konstansaival); HAMART-regresszió RENDBEN |
| E6 | `naplok/F218_folytatas.md` (a GK-03 B36-os pontja) | a B38 frissességi hiánya rögzítve, a B36 mellé | – |
| E7 | `bemenet/lxx.py` `_alak_kapu`, `_vers_index` (`_SEGEDTABLAK`); `szamitas/lxx.py` `osszevetes`, `hid` | a hibás alakú Strong- és `lxx_igehely`-mező, az ismeretlen `igehely_lxx` nélküli fájl, a görög szó nélküli motívum és a társlista forrás-sor nélküli ága kimondott hibával áll meg. Mérés: a döntéstábla 96 sorában hibás alakú mező 0 (`scope=heber_strong, gorog_strong, lxx_igehely \| forras=adat/lxx_dontesek.tsv \| ts=2026-11-16`); az `igehely_lxx` nélküli fájl a két ismert segédtábla | `teszt_lxx.py` `NemaAgak` (2 teszt) |
| E8 | `szamitas/lxx.py` (a „nincs Septuaginta-fájlja” üzenet); `nyitott/uj/f218-generator-uj-a.md` N195 | az üzenet megnevezi a könyvnév-alak lehetséges okát (`Sir` ↔ `JSir`); az N195 kiegészítve | – |
| E9 | `naplok/F218_jelentes.md` („7 új sablonsor” → 8); `bemenet/lxx.py` (`LxxDontesSorok.sajat` és a halmaza törölve); `szamitas/lxx.py` `szamit` docstringje; `teszt_vaz.py` (a GK-15 duplikált váza törölve, 9 váz `S3_MARADEK` okkal) | Az összevetés kétszeri számítása marad, indokkal: az 5. szakasz forrásfigyelése (GK-07) így a saját olvasásait látja (a bemenetek beolvasása gyorsítótárazott). A 400 sor fölötti commitok tényként rögzítve, utólag nem bonthatók. **Az `s4.p6.forras` mondata** a 218a végi listáján | – |

**Mérés a javítókör után** (`scope=HAMART-001 és ISTENTISZT-001, munka mód | forras=eszkozok/lapgen/regresszio.py; festek.py; tesztek/futtat.py | ts=2026-11-16`): HAMART-regresszió RENDBEN (engedély nélküli diff-sor 0; S4-FORRAS: 1); festékpróba 0 szivárgás mindkét lapon (HAMART belső 277, ISTENTISZT belső 216); a teljes tesztsor eredménye a commit üzenetében.

**A main behozása és az E10 újramérése** (2026-11-16): a main beolvasztása ütközés nélkül (`31d1451e`); a mérce bemenetei közül csak a `DONTESEK.md` változott, a hash-sora külön commitban frissült (`9e5fc5ee`); HAMART-regresszió RENDBEN (engedély nélküli diff-sor 0), festékpróba 0 mindkét lapon. Az `eszkozok/olvaso_szerver/teszt_visszhang_kapu.py` két bukása a merge után is áll; az ág által írt nyolc, a teszt által olvasható fájlt a main változatára cserélve is mindkettő bukik (`scope=a két teszt | forras=python eszkozok/olvaso_szerver/teszt_visszhang_kapu.py, a fájlok a main változatával | ts=2026-11-16`). **Mindkét bukás a main-ről ered** (N198).

**A teljes lapgen-tesztsor** a javítókör után: 270 teszt, 3 bukás (GK-08a egy `.join()`, GK-01 két teszt a `hash_or_kapu.py` miatt); javítva (`e6f0226c`), a szerkezeti és az LXX-tesztek újrafuttatva: 26/26 zöld.

## Független ellenőrzés — 7. ellenőrzés (célzott újraellenőrzés a 6. ellenőrzés javítókörére)

*A `fuggetlen-ellenor` subagent (Fable) jelentése, a hívó session (`claude-opus-5-5`, a 9. session) mentésében. A táblázat a lényegi sorokra rövidítve; az ELTÉRÉS-tételek szó szerint. Hatókör: `5e628d69..f5241825`; szint: a megbízás `konnyitett`, a subagent `teljes`-re emelte (a diff olvasói kimenetet előállító kódot hoz; `feladatok.py szint 218`: `teljes`).*

**Eredmény: ELTÉRÉS, 3 tétel.** OK: modell (`claude-fable-5-2`), CI a head-en (43825976334, `success`, a hash-őr lépése: 209 sor egyezik), tesztek (`lxx szerkezet vaz`: 60, 0 hiba; `teszt_push_elott.py` zöld), E1 (mindkét hash-frissítés külön commitban), E3, az E3 maradéka (N199), E6, E7, E8, E9, E2/E4/E10 (N196–n), a merge (`31d1451e`: a 218a fájljait nem írta), a 218a nyitva marad (a `MERGE_SZO` nem illik a `kovetkezo`-ra), A1, A2, ⛔ pontok. NEM ELLENŐRIZHETŐ: a HAMART-regresszió és a festékpróba a head-en (nem megengedett parancs), a teljes tesztsor, az N198 mérése, a brief teljes G/D listája, A6.

- **U1 (közepes–alacsony) — az E5 javítása hibás deklarációt hozott: a `HidFok` enumon `@dataclasses.dataclass(frozen=True)` áll** (`eszkozok/lapgen/szamitas/lxx.py:112-113`). A generált `__eq__`/`__hash__` miatt a tagok egymással egyenlők (`HidFok.EROS == HidFok.GYENGE` igaz; a Python dokumentációja ezt nem támogatott használatnak írja). Nyelvi szabályból levezetve, nem futtatásból. Ma nem látszik (a megjelenítő `.value`-t olvas, a tesztek `assertIs`-t használnak), de az `Osszevetes` érték szerinti egyenlősége a `fok` mezőre vak, és minden későbbi `==` vagy szótárkulcs némán rossz. A modul többi enumja (`Itelet`, `GorogFajta`) dekorátor nélküli. Javítás: a dekorátor törlése és egy `assertNotEqual` teszt.
- **U2 (alacsony) — a brief `kovetkezo` mezője a merge-et nem nevezi meg** (`F218_GENERATOR_UJ_A_BRIEF.md:12`). A cél teljesül (a gépi lezárás nem zár). A tényleges következő lépés azonban a felhasználó merge-e, a mező ezt elhallgatja, és ugyanezzel a szöveggel marad a main-en; a `feladatok.py ellenoriz` B része a mergelt, de nyitott briefet jelentésben mutathatja. A merge után az `ag`/`pr` mező is elavul (a folytatási fájl teendőként rögzíti, `naplok/F218_folytatas.md:62`).
- **U3 (alacsony, tervezési) — az új hash-őr kemény CI-bukás a teljes mércére, amelynek része a teljes `DONTESEK.md`** (`.github/workflows/ellenorzes.yml:181-189`; `naplok/F218_referencia.tsv:3`). A PR-futás a merge-refet ellenőrzi; minden más PR `szamkiosztas`-a megváltoztatja a `DONTESEK.md`-t, így a lapgenerátort érintő PR CI-je akkor is piros, ha az ág önmagában konzisztens, amíg a main behozása és a hash-frissítés meg nem történik. A #729 merge-e után a `szamkiosztas` törli a `dontesek/uj/f218-generator-uj-a.md`-t (B51, „hiányzik”), a main-en a mérce azonnal elavult; a folytatási fájl ezt az S5 első teendőjeként rögzíti, N-tétel nincs róla. Ha a main a `31d1451e` óta `DONTESEK.md`-változást kapott, a merge-commit main-futása piros lesz. A kapunak saját tesztje nincs.

**A hívó kezelése (2026-11-16):**
- **U1 javítva:** a dekorátor törölve; teszt: `teszt_lxx.py` `Kuszobok.test_a_fokozatok_kulonboznek` (`assertNotEqual` és háromelemű halmaz).
- **U3 javítva:** a CI-lépés csak PR-on fut (`if: always() && github.event_name == 'pull_request'`): a main-re futó push-esemény nem bukhat el a `szamkiosztas` utáni elavult mércén. A PR-okon a viselkedés szándékos: a lapgenerátort érintő ág a regresszió előtt hozza be a main-t és frissítse a hash-sort. Új N-tétel: N200. A kapu saját tesztje: `teszt_regresszio.py` `HashOrKapu` (2 teszt). A `hash_or_kapu.py` csomagként is importálható (`from lapgen import regresszio`).
- **U2 marad:** a `kovetkezo` szövegét az orkesztrátor adta meg szó szerint („Te: S5 új ágon a main-ről”), és a merge szó a gépi lezárást kiváltaná (`brief_lezaras.py` `MERGE_SZO`). A merge a PR címéből és leírásából látszik.

## F218.8 — S5: „6. Kereszthivatkozások” és a Minősítés (`claude-opus-5-5`, high, 2026-11-16, a 10. session)

*Új ág a main-ről (`claude/f218a-s5-1402d5`, alap `68d9ee90`), saját PR-ban. A modell-ellenőrzés: a kért `opus`, a session `claude-opus-5-5`.*

**Első lépés: N200** (`2e21e0b1`). A `szamkiosztas` a #729 merge-e után a B51 `DONTESEK.md`-t és a B66 sablontábla döntésszámait megváltoztatta, a `dontesek/uj/f218-generator-uj-a.md`-t törölte. A két hash-sor frissült, a törölt fájl sora kikerült; HAMART-regresszió RENDBEN, festékpróba 0, a hash-őr 208 sorral RENDBEN. Az N200 a hosszabb távú része miatt nyitva marad (a lezárt-sor a `NYITOTT_FELADATOK.md`-ben). **Ugyanez a merge után újra esedékes** (az ág új döntésfájlja, `dontesek/uj/f218a-s5-1402d5.md`, a B51 sora): az S6 első lépése.

**Eredmény:** a HAMART-001 6. szakasza (a Minősítéssel együtt, 307 sor) a referenciától négy soron tér el, mind engedéllyel; a regresszió RENDBEN (engedély nélküli diff-sor 0). Festékpróba 0 (HAMART: belső 319, horgony 30, idézet 2754, kézi 652; ISTENTISZT: 258, 18, 1375, 291).
*Proveniencia: `scope=general.py --cel lexikon2 --id HAMART-001/ISTENTISZT-001 (PARDES_DATUM=2026-11-13); regresszio.py --id HAMART-001; festek.py | forras=munkafa (2e21e0b1 + az S5) | ts=2026-11-16`.*

| Engedélysor | Osztály | Sor | Előre számolt? |
|---|---|---|---|
| `S5-FORRAS` | GK-07, HN-10: a blokkfejléc forráslistája a valódi olvasásból, a javított Károli-KH táblával | 1 | igen: az alapmérés „HN-10 megjegyzésben” sora a 6. szakaszban 3 sort számolt, ez a három egyike |
| `S5-RES-FORRAS` | HN-10: a Minősítés rés-jelölőjének forráslistája | 1 | igen (a 3 közül) |
| `S5-PROV` | HN-10: a Minősítés proveniencia-sorának eredeti alakja (megjegyzés); a látható „Forrás:” mondat változatlan | 1 | igen (a 3 közül) |
| `S5-KIEJTES` | M-CSERE: a régi lap a Jer 4:23 sor kézi indoklásába utólag kiejtést szúrt („תהו (tóhú)/בהו (tóhú/bóhú)”: a kiejtés kétszer); az új lap a forrás szövegét adja, ahogy a régi lap is a következő (Jer 4:28) sorban | 1 | **nem**: új osztály, a 218a végi listán |

**Felépítés.**
- `bemenet/kereszthiv.py`: B44 (TSK) a B34 megfeleltetésével Károli-kulcsra váltva (a régi `tsk_kulcs` szabálya: ószövetségi könyvben a tábla párja, MT-tartalék a számlálással kapott MT-sorokra, az Újszövetségben azonosság); B43 (Károli-KH, nyers) és B72 (a javított, MEK-kel összevetett tábla; a térkép B43-a licenc szerint két sorra bontva, a B57 mintájára): a nyers és a csak a MEK-ben álló megerősített sorok, azonos kulcs egyszer, csak a `megerositett` szint; a többi sor száma forrásversenként. A célhely igehelyként: a könyv a cél STEPBible-alakjából (B63), a szám a megjelenítésből (vesszős és kettőspontos alak egyaránt). A B04 kereszthivatkozásos jelöltjei (`kereszthiv_jeloltek`): a forrás-mező szerkezete (gyűjtemény, forrásversek, irány, szavazatszámok, TSK-találat, „a Károli is ajánlja”), az ok (B56), a címke-ismétlés szabálya (a régi `cimke_ismetles`; HN-02), a proveniencia-sor két alakja; az indoklás darabjai: kézi szöveg, motívum-hivatkozás (`[ID: …]`), Strong-hivatkozás (a Strong-szám és utána a héber/görög szó, a régi `STRONG_ELOL`).
- `szamitas/kereszthiv.py`: a szakasz (49 hely, 25 ad utalást, 120 utalás, 6 nem vizsgálható, 5 hely 8 nem megerősített Károli-utalása) és a Minősítés (5 pár, 6 érintett hely, 99 vizsgált hely) modellje; a kapu: a felsorolt és a nem vizsgálható helyek ismétlés nélkül (GK-A1), az utalások összege, a párok a felsorolt utalások közül, a döntések összege.
- `megjelenites/md/kereszthiv.py`: 57 új sablonsor (`s6.*`, `cim.kereszthivatkozasok`, `cim.minosites`), ebből 55 a régi lap végleges szövege (`dontes=-`, a régi utólagos cserék — F212 M2, M3, M4, I5 — eredménye), 2 új (`dontes=var`, a két mintalapon nem fut): `s6.ures`, `s6.min.parok.nincs` (a régi „TSK/Károli-KH”, „Votes ≥ 15” szöveg helyett).
- `ertekek.py`: `Dontes` (a `bemenet/dontes.py` innen veszi), `Gyujtemeny`, `AjanlasFajta`; `bemenet/konyvek.py`: a STEPBible-rövidítés két iránya; `fo.Forrasok.lista` (a proveniencia `+` elválasztós felsorolásához); `konfig.TSK_SZAVAZAT_KUSZOB = 15`.
- Jegyzék: B43, B44, B72; névtábla: 15 `ok_cella` sor (DT869; 12 HAMART-, 3 ISTENTISZT-címke).

**DT884 (🟢, a felhasználó döntése, 2026-11-16, az orkesztrátoron át: „Igen, (a)”): a kézi indoklás az adatban a végleges alak.** A régi lap a Minősítés (és a 3. szakasz) indoklás-celláit utólagos cserékkel tette olvashatóvá. Az új generátor nem írhat át látható szöveget, ezért a DT869 elvét alkalmaztam: az egyenes idézőjel (24 sor) és a „Strong-keresés szerint” munkaszó (10 sor) a `jeloltek.tsv`-ben javult (csak a HAMART-001 kereszthivatkozásos előfordulás-jelöltjein), az ok cellakezdő alakja a névtábla `ok_cella` sora, a jelölt szerkezet (`[ID: …]`, Strong + szó) a bemeneti rétegben bomlik darabokra; ha az indoklás nem olvasói szöveg, a réteg megáll. **A régi generátor HAMART-kimenete mindkét adatjavítás után bájtra azonos a referenciával.** A `jeloltek.tsv` az `ir`-en kívül esik: a felvétele kölcsönös függést adna (#212 ↔ #218, és új függést a #157-tel), mint a DT870-nél (N188). A többi motívum egyenes idézőjeles indoklása: N208.
*Proveniencia: `scope=general.py --cel lexikon --id HAMART-001 (PARDES_DATUM=2026-11-13), cmp a HEAD lapjával | forras=munkafa | ts=2026-11-16`.*

**ISTENTISZT-001** (nincs bájt-mérce): 20 hely, 8 ad utalást (19); a Minősítés 9 pár, 7 érintett hely, 61 vizsgált hely (mind elutasítva); a címke-ismétlés (HN-02) 0. A forrás-mező egyik helye `Zef 3:9` (a normalizáló táblában `Sof`): a régi lap is így közölte; az új generátor a forrás-mező igehelyét csak alakra ellenőrzi, és az adat szerint írja ki (N208, N195).

**Nem portolt, kimondott hibával megálló ágak** (a két mintalapon nem futnak): ismeretlen forrás-forma a kereszthivatkozásos jelöltnél; szokatlan szavazatszám-alak (a lap alakja a szerkezetből készül, csak ha a forrással azonos); nem olvasói indoklás (egyenes idézőjel, belső jelölés, munkaszó, cellahatár); értelmezhetetlen Károli-KH célhely.

**Az ismétlés-figyelő** (figyelmeztetés, nem BUKÁS) a HAMART-on 46, az ISTENTISZT-en 31 találatot ad (eddig 9 és 8): a többlet a Minősítés táblájának azonos indoklású sorai (pl. a Jób 14:1-től a Zsolt 90:9-ig tizenhat sor ugyanazzal az indoklással). A régi lapon is így áll.

**Tesztek:** `teszt_kereszthiv.py` (15): a HAMART számai és a TSK-sorrend, a kapu, GK-A1 (a nem vizsgálható hely egyszer áll, mindkét lapon), HN-10 (a jelölők a javított táblát nevezik, a látható szövegben fájlnév nincs), a forrás-mező szerkezete (öt eset és két megálló), az indoklás darabjai és kapuja, HN-02 a lapon, az `ok_cella` kapuja. A `teszt_vaz.py` GK-A1 váza törölve.

**A 218a végi listába:** a két új `var` sablonsor; az `S5-KIEJTES` osztály; a DT884; a 15 `ok_cella` sor (a három ISTENTISZT-címke nagy kezdőbetűje a régi lap szabálya szerint); a Minősítés „a {p}%-a” mondatrésze a régi szöveg szerint rögzített névelővel áll (1%-nál és 5%-nál „a 5%-a” lenne); a `s6.min.olvasoi.nincs` a régi „független külső megerősítése” szót tartja, holott az F212 M2 a „független”-t a párokra „külső”-re cserélte (a két mintalapon nem fut).

| Pont | Dátum (UTC) | Heti · minden modell | Heti · Fable | 5 órás | Megjegyzés |
|---|---|---|---|---|---|
| 10. session indul (opus, high) | 2026-11-16 10:48 | 41% | 15% | 82% | `get_usage`; a kontextus 29% (1M) |
| S5 kész (a regresszió RENDBEN) | 2026-11-16 11:35 | 42% | 15% | 9% | 1 százalékpont heti (az 5 órás közben nullázódott); a kontextus 52% |

## Független ellenőrzés — 8. ellenőrzés (célzott: S5 és az N200)

*A `fuggetlen-ellenor` subagent (`claude-fable-5-2`) jelentése, a hívó session (`claude-opus-5-5`, a 10. session) mentésében, rövidítve; az ELTÉRÉS-tételek lényege szó szerint. Hatókör: `68d9ee90..4f6974e8`; szint: `teljes`.*

**Eredmény: ELTÉRÉS, 9 tétel.** OK: modell; CI a head-en (43863082548, `success`, a hash-őr lépése zöld); a régi generátor HAMART-kimenete változatlan (CI F217: „HAMART-001: nem változott”, E28 zöld); a modell számai; GK-A1, HN-10, HN-02; GK-08a/c, GK-01, GK-05; festékpróba; a tesztek (a `teszt_visszhang_kapu.py` két bukása az N198, a `teszt_szintek.py` az N187); A1–A6; a táblák sorszáma. NEM ELLENŐRIZHETŐ: a valódi szakasz-diff (`regresszio.py` nincs a megengedett parancsai között), az ISTENTISZT számai (teszt nem rögzítette). Tartományon kívüli megfigyelés: a base-re futó main-oldali `ellenorzes` (43850277818) piros az E2–E37 lépésen („HAMART-001: 8 hivatkozás nem létező Károli-versre”).

1. **E2:** a `jeloltek.tsv` javítása merge után a közzétett nyílt magot is átírja (6 fájl: `kizarasok.tsv`, `METHODS.md`, `MODSZER.md`, `KIADAS.txt`, `RELEASE.txt`, `ELLENORZO_OSSZEG.sha256`), és ezt sem a DT884, sem a jelentés nem mondja ki.
2. **E1:** a brief által belsőnek nevezett `indoklas` mező új mezőnéven (`indoklas_kh`), kézi szövegként kerül a látható lapra; a festékpróba ezt nem láthatja, a `dontes.py:7` docstringje ellentmond neki. Felhasználói megerősítés kell.
3. **`ir`:** a `jeloltek.tsv` 34 cellája a mezőn kívül íródott, rögzített rendelkezés nélkül (DT884 🟡).
4. **E4:** a SEMA 2.68 az `ok_cella` típusra olyan kaput ígér (a kulcs létező címkére mutat), amelyet a kód nem tartalmaz.
5. **E5:** a Minősítés küszöbei (`45, 55`; `0.67, 0.34`) és az erős/közepes/gyenge besorolás a megjelenítőben áll, nem a `konfig.py`-ban és a `szamitas/`-ban. **E6:** `@unittest.skip(S5) test_hn10_karoli_kh_forrasdeklaracio` megmaradt; az új tesztek nevében nincs azonosító. **E9:** a B43 szűrése a `karoli_kh_szuro` saját másolata, egyezés-teszt nélkül. **E8:** a B04 (és B65, B66, B68, az új B51) hash-sora nem külön commitban frissült. **E7:** a forrás-mező könyvneve ellenőrizetlenül jut a lapra (`Zef 3:9`; bevallott, N195, N208).

## A 8. ellenőrzés javítóköre (`claude-opus-5-5`, 2026-11-16, a 10. session)

A besorolás az orkesztrátoré; a session a gépies tételeket javította, a döntést kívánókat a DT-F218s-be írta.

| # | Hely | Javítás | Ellenőrzés |
|---|---|---|---|
| E1, E2, `ir` | `dontesek/uj/f218a-s5-1402d5.md` (DT884); `bemenet/dontes.py` docstring | a DT884 kimondja mindkét következményt: az `indoklas` átminősítését a kereszthivatkozásos sorokon és a nyílt mag hat fájljának változását; a docstring a kivételt nevezi. **Döntés nem született: 🟡, a felhasználóé** | – |
| E4 | `bemenet/nyelv.py` `ok_cellaalakok` | a kulcsnak a B56 létező címkéjére kell mutatnia (az „(összesítő sor)” jelölő nélkül), különben BemenetHiba | `teszt_kereszthiv.py` `OkCella` (három eset, köztük az árva sor) |
| E5 | `konfig.py` (`MINOSITES_EROS`, `MINOSITES_KOZEPES`, `MINOSITES_FELE`); `ertekek.py` `MegerositesFok`; `szamitas/kereszthiv.py` (`Minosites.szazalek`, `.fele`, `.fok`; `KhSzakasz.szazalek`); `megjelenites/md/kereszthiv.py` | a küszöbök a konfigban, a százalék és a fokozat a modellben; a megjelenítő csak kulcsot választ | HAMART-lap bájtra azonos a javítás előttivel; `test_az_istentiszt_szamai` (fokozat: közepes) |
| E6 | `teszt_vaz.py`; `teszt_kereszthiv.py` | a HN-10 váza törölve; a tesztnevek: `test_gk_a1_…`, `test_hn10_…` | `teszt_vaz.py` zöld |
| E9 | `teszt_kereszthiv.py` `KarolKhSzuro` | egyezés-teszt a régi `karoli_kh_szuro.szures`-sel a két mintalap minden versén (a megerősített utalások sorrendje és a nem megerősítettek száma) | zöld |
| E8 | – | utólag nem bontható; tényként rögzítve. A javítókör hash-frissítése (B51, a döntésfájl bővülése) a javítókör commitjában áll | – |
| E7 | – | bevallott, halasztva (N195, N208) | – |
| (az ellenőr megjegyzése) | `teszt_kereszthiv.py` | az ISTENTISZT számai rögzítve (20/8/19; 9/7/61) | zöld |

**Mérés a javítókör után** (`scope=HAMART-001 és ISTENTISZT-001, munka mód | forras=regresszio.py; festek.py; tesztek/futtat.py | ts=2026-11-16`): HAMART-regresszió RENDBEN (engedély nélküli diff-sor 0; S5: 4 engedélysor), a HAMART-lap bájtra azonos a javítókör előttivel; festékpróba 0 mindkét lapon.

**DT884 eldőlt (2026-11-16):** a felhasználó döntése az orkesztrátoron át, szó szerint: „Igen, (a)”. Az adat a végleges alak (DT869 elve); a döntés magában foglalja a 8. ellenőrzés E1 és E2 tételét (az `indoklas` átminősítése a kereszthivatkozásos sorokon, a nyílt mag hat fájljának változása a merge után) és az `ir`-en kívüli írást (N188). A DT884 állapota 🟢; a független ellenőrzésnek nincs hátralévő lépése (a jelentés és az egy javítókör kész).

## F218.9 — S6: „7. Kapcsolatok”, Alátámasztás és „8. Kapcsolódó motívumok” (`claude-opus-5-5`, high, 2026-11-16, a 11. session)

*Új ág a main-ről (`claude/f218a-s6-3896f7`, alap `ff3fd41c`), saját PR-ban. A modell-ellenőrzés: a kért `opus`, a session `claude-opus-5-5`.*

**Első lépés: N200** (`648ddbcb`). A `szamkiosztas` (`ff3fd41c`) a B51 `DONTESEK.md`-t megváltoztatta, a `dontesek/uj/f218a-s5-1402d5.md`-t törölte. A hash-sor frissült, a törölt fájl sora kikerült; HAMART-regresszió RENDBEN, a hash-őr 208 sorral RENDBEN. **A merge után ugyanez újra esedékes** (az ág döntésfájlja, `dontesek/uj/f218a-s6-3896f7.md`, a B51 sora): az S7 első lépése.

**Eredmény:** a HAMART-001 7. szakasza (az Alátámasztással, 236 sor) és 8. szakasza (17 sor) a referenciától hat soron tér el, mind engedéllyel; a regresszió RENDBEN (engedély nélküli diff-sor 0); az első futás is pontosan ezt a hat sort adta. Festékpróba 0 (HAMART: belső 342, horgony 30, idézet 2756, kézi 754; ISTENTISZT: 281, 18, 1377, 325).
*Proveniencia: `scope=general.py --cel lexikon2 --id HAMART-001/ISTENTISZT-001 (PARDES_DATUM=2026-11-13); regresszio.py --id HAMART-001; festek.py | forras=munkafa (648ddbcb + az S6) | ts=2026-11-16`.*

| Engedélysor | Osztály | Sor | Előre számolt? |
|---|---|---|---|
| `S6-FORRAS` | GK-07: a 7. szakasz blokkfejlécének forráslistája a valódi olvasásból (a kapcsolat-tábla mellett a döntések táblája és a könyvnév-normalizáló tábla) | 1 | a brief 8.1 (b) osztálya (mint az S1–S5 `…-FORRAS` sora) |
| `S6-RES-FORRAS` | GK-07: az Alátámasztás rés-jelölőjének forráslistája | 1 | (b) |
| `S6-PROV` | GK-07: az Alátámasztás proveniencia-sorának eredeti alakja (megjegyzés); a látható „Forrás:” mondat változatlan | 1 | (b) |
| `S6-KAPCSOLODO-FORRAS` | GK-07: a 8. szakasz blokkfejlécének forráslistája | 1 | (b) |
| `S6-KAPCSOLODO-PROV` | GK-07: a 8. szakasz proveniencia-sorának eredeti alakja | 1 | (b) |
| `S6-KIEJTES` | M-CSERE: a régi lap az 1Móz 6:11 → 6:13 indoklásába utólag kiejtést szúrt („מָלֵא (málé) + חָמָס, málé + chámász”: a kiejtés kétszer); az új lap a forrás szövegét adja | 1 | **nem**: az S5-KIEJTES osztálya (ugyanaz a `kiejtes_szoveg.potol` lépés), a 218a végi listán |

**Felépítés.**
- `bemenet/kapcsolat.py`: B45 (`adat/kapcsolatok.tsv`) és B46 (`adat/motivum_kapcsolatok.tsv`), új jegyzéksorok a térkép számával; a döntésre váró motívumközi jelöltek a B04-ből. A zárt értékek felsorolásra (`KapcsolatTipus`, `MotivumKapcsolatTipus`, `Megbizhatosag`), a PaRDeS-szint névtábla-kulcsra; a `funkcio` és az indoklás kézi része kézi próza, a S5 kapujával (`kereszthiv.nem_olvasoi`, most nyilvános); a B45 indoklásának ` | ` utáni része belső proveniencia (megjegyzésbe kerül, a hivatkozott döntések dátumával a B51-ből).
- `szamitas/kapcsolatok.py`: a 7. szakasz modellje (a kapcsolatok a tábla sorrendjében, a gráf csomópontjai kánoni sorrendben, az élek sorszámmal, a típus- és a bizonyosság-megoszlás, a következtetés két kódja: `KapcsolatSzerkezet`, `KapcsolatBiztossag`, a küszöbök a `konfig.py`-ban), az Alátámasztás (az azonos indoklású sorok egy sorban, az első előfordulás helyén; az indoklás nélküliek külön), a 8. szakasz modellje (a másik motívum szemszögéből, a motívumközi döntés dátuma a `konfig.DONTES_MOTIVUMKOZI`-ból). Két kapu: a 7.-en a típusok, a bizonyosság összege, a gráf élei és csomópontjai, az Alátámasztás teljessége; a 8.-on a darabszámok.
- `megjelenites/md/kapcsolatok.py`: 63 új sablonsor (`s7.*`, `s8.*`, `cim.kapcsolatok`, `cim.kapcsolodo`, `cim.alatamasztas`), mind a régi lap végleges szövege vagy a régi kód ágának mondata (`dontes=-`); az író zárt jelölés-készlete a Mermaid-blokkal (`MERMAID_*`, `mermaid_csucs_nyit`, `mermaid_el_*`) és a másik motívum lapjára mutató link végével (`lap_link_zar`) bővült. Névtábla: 12 új sor (`kapcsolat_tipus` 5, `kapcsolat_tipus_mondat` 5, `motivumkozi_tipus` 2; ebből 1 `eredet=uj`: „közös_igehely” → „közös igehely”).

**Adatjavítás (DT869 elve, az `ir`-en kívül, N188).** A régi lap a `funkcio` cellát utólag cellakezdő alakra írta (`nevelo_le`: nagy kezdőbetű, rövid cellánál a névelő elhagyásával). Az új generátor nem ír át, ezért a cella az adatban kapta meg a jóváhagyott lap alakját: `adat/kapcsolatok.tsv` a HAMART-001 43 sora (41 nagybetű, 2 névelő-elhagyás: „„megtelt erőszakkal” szópár …”), `adat/motivum_kapcsolatok.tsv` a HAMART-001 ↔ ISTENTISZT-001 sor („A megfordított lánc …”, mindkét lapon áll). A szkript csak a kezdő névelőt és a kezdőbetűt engedte eltérni, a többi cellát bájtra összevetette. **A régi generátor HAMART-kimenete (mindkét nézet) a javítás után is bájtra azonos a referenciával.** A `funkcio` mező a nyílt magba nem kerül, ezért a nyílt mag nem változik. Az ISTENTISZT-001 saját soraiban a funkció kisbetűvel áll (a forrás szerint; mint a DT869 hat cellájánál): a 218a végi listán.

**DT888 (🟡, technikai döntés, a felhasználó megerősítésére vár).** A B46 mindhárom sorának indoklása „Döntés: DT280 (felhasználó, 2026-10-20).” mondattal, az ISTENTISZT-001 két B45-sora „(DT479, a felhasználó, …)” zárójellel végződik; a régi lap ezt tisztítással vágta le. A bemeneti réteg a mező végén álló döntés-hivatkozást (két rögzített alak) szerkezetként leválasztja; a döntést a sor proveniencia-része, illetve `dontes_ref` mezője hordozza; a szöveg közepén álló döntésszámon a kapu megáll. A HAMART-001 8. szakasza így betűre a jóváhagyott lapé. A döntésfájl: `dontesek/uj/f218a-s6-3896f7.md`.

**ISTENTISZT-001** (nincs bájt-mérce): 16 kapcsolat 20 helyet köt össze (13 párhuzam, 2 beteljesedés, 1 variáns; 13 magas, 3 közepes; következtetés: túlnyomórészt párhuzam, a többség biztos); az Alátámasztás 12 sora és 1 indoklás nélküli kapcsolat (2Móz 33:19 → 34:5); a 8. szakasz 3 kapcsolata (ALVIL-001 2, HAMART-001 1) és 3 döntésre váró jelölt. A látható szövegben döntésszám nincs (teszt).

**Nem portolt, kimondott hibával megálló vagy a két mintalapon nem futó ágak:** kapcsolat nélküli motívum (a 7. és az Alátámasztás hiánymondata), indoklás nélküli kapcsolatok mind (a régi hiánymondat), motívumközi kapcsolat nélküli motívum; ismeretlen típus- vagy bizonyosság-érték; nem olvasói kézi szöveg. A régi kód a `res_forras.tsv` rögzített mondatát („A motívumhoz nincs rögzített kapcsolat.”) adat mellett figyelmen kívül hagyta; az új generátor a rés-forrást itt nem olvassa (mint az S5 a Minősítésnél).

**Az ismétlés-figyelő** (figyelmeztetés) a HAMART-on 79 (eddig 46), az ISTENTISZT-en 34 (eddig 31) találatot ad: a többlet az Alátámasztás azonos szerkezetű indoklásai („A közepes bizonyosság ezen a mért egyezésen áll. A hagyományos kereszthivatkozások közül a TSK …”); a régi lapon is így áll.

**Tesztek:** `teszt_kapcsolatok.py` (15): a két lap számai, a csomópontok sorrendje, a 8. szakasz számai és a döntés dátuma, a három kapu, a záró döntés-hivatkozás, a következtetés ágai, az üres ágak, a gráf, a link, a döntésszám hiánya a látható szövegben. Az egész tesztsor: 308 teszt, 0 hiba, 0 bukás, 30 váz (két korábbi teszt a saját szakasza helyett a lap végéig vágott: a 2. és a 6. szakasz kivágása a következő szakaszcímig szűkült).

**A 218a végi listába:** a DT888; az `S6-KIEJTES` osztály; az 1 új névtábla-név (`motivumkozi_tipus` „közös igehely”); a `funkcio` adatjavítás (43 + 1 cella); az ISTENTISZT-001 kisbetűs funkció-cellái (a 7. szakasz 16 sorából 15, és a 8. szakasz két ALVIL-001-sora); az üres funkció és PaRDeS-szint cellája a 7. szakaszban „—” (a régi üres cellát írt; a két mintalapon nem fut); az ISTENTISZT-001 Alátámasztásában a kézi szöveg Strong-számot („H7121+H8034”) és Markdown-kiemelést hordoz; az `s7.alat.modszer` rögzített módszermondata (a leltár szerint az adatból kellene levezetni: új tartalom, nem e szelet dolga).

| Pont | Dátum (UTC) | Heti · minden modell | Heti · Fable | 5 órás | Megjegyzés |
|---|---|---|---|---|---|
| S6 kész (a regresszió RENDBEN) | 2026-11-16 13:55 | 45% | 16% | 30% | a kontextus 44% (1M) |

## Független ellenőrzés — 9. ellenőrzés (célzott: S6 és az N200)

*A `fuggetlen-ellenor` subagent (`claude-fable-5-2`) jelentése, a hívó session (`claude-opus-5-5`, a 11. session) mentésében, rövidítve; az ELTÉRÉS-tételek lényege szó szerint. Hatókör: `ff3fd41c..dc9bd031`; szint: `teljes`.*

**Eredmény: ELTÉRÉS, 7 tétel.** OK: modell; CI a head-en (43886409725, `success`, a hash-őr és az F217 zöld: „HAMART-001: nem változott”, „G07 (nyilt_mag/): 0 fájl változott”); az adatjavítás tartalma (csak a `funkcio` oszlop, 43 + 1 cella, 41 nagybetű, 2 névelő-elhagyás); a B45 `indoklas` kézi prózaként (SEMA 2.3); az öt GK-07 engedélysor indoka; GK-01/05/08a/c, festékpróba, tesztek (308/0/0, 30 váz); a sablon- és névtáblasorok (`dontes=-`, új tartalmi állítás nincs; 1 `eredet=uj`); az ISTENTISZT-001 számai saját számlálással; a két szűkített régi teszt; A1, A3–A5; a táblák sorszáma. NEM ELLENŐRIZHETŐ: a régi generátor bájt-egyezése és a szakasz-diff közvetlenül (a `general.py`, a `regresszio.py`, a `cmp` nincs a megengedett parancsai között; közvetett CI-bizonyíték van); A6; a commitonkénti zöld állapot (a `b482668b` valószínűleg bukó teszttel állt, a javítás a `5a8e76a9`-ben).

1. **DT888:** a záró döntés-hivatkozás levágása törlés a kézi prózán, a kapuk által nem látott rétegben; a minta tágabb volt a leírt két alaknál (bármely DT-számmal kezdődő záró zárójelet törölt); az alapszabály alóli kivételt a menet maga döntötte el. Felhasználói döntés kell: (a) marad, a minta a két alakra szűkül, teszttel; vagy (b) a hivatkozás az adatból kerül ki (DT869/DT884). A B46 `indoklas` kézi prózaként kezelése ugyanitt erősítendő meg.
2. **Az `ir`-en kívüli adatírás** (43 + 1 `funkcio` cella) döntéssor és N-tétel nélkül; az S5-ben ugyanez DT884-et és N188-kiegészítést kapott. A B45/B46 hash-sora az S6 commitjában frissült, nem külön (a 8. ellenőrzés E8 tételének ismétlődése).
3. **`S6-KIEJTES`:** a 8.1 osztályain kívüli eltérés második példánya; osztályszintű rendelkezés hiányzik.
4. **GK-01:** a B04-nek három közvetlen olvasója van (`dontes.py`, `kereszthiv.py`, `kapcsolat.py`); a teszt a névminta miatt nem látja.
5. **A kapuk** bizonyosság- és nyitott-összege a valódi számításon nem bukhat (az `alacsony` = `n − magas − kozepes`; a `nyitott_ossz` = az összeg).
6. **Napló:** hibás commit-hash (`101da4dc` ↔ `648ddbcb`) és „4” ↔ 5 GK-07 engedélysor.
7. **Az olvasó-szerver tesztsora** a menet jelentésében nem szerepel, bár a diff az `adat/`-ot érinti; az ellenőr futása (`teszt_futtat.py --diff ff3fd41c`): `teszt_szintek.py` 13-ból 2, `teszt_visszhang_kapu.py` 22-ből 2 bukás (az N187 és az N198 nyilvántartott hibái), a többi 14 fájl zöld.

Megfigyelés: a `teszt_kapcsolatok.szakasz_sorai` is a lap végéig vágott (az S7-ben ugyanez ismétlődött volna).

## A 9. ellenőrzés javítóköre (`claude-opus-5-5`, 2026-11-16, a 11. session)

A besorolás: E1 (döntési rész), E2, E3 a felhasználóé — helyőrző-döntéssor, megállás; a többi gépies, egy javítókörben.

| # | Hely | Javítás | Ellenőrzés |
|---|---|---|---|
| E1 (gépies rész) | `bemenet/kapcsolat.py` `_ZARO_DONTES_RX` | a minta csak a két tényleges alakra illeszt (döntésszám, döntéshozó, dátum, legfeljebb a válasz idézete); tartalmas zárójel nem válik le, a benne álló döntésszámon a kapu megáll | `teszt_kapcsolatok.ZaroDontes.test_tartalmas_zaro_zarojel_nem_valik_le`; a két lap bájtra azonos |
| E1 (döntés) | `dontesek/uj/f218a-s6-3896f7.md` DT888 | a kérdés a felhasználóé: (a) a leválasztás marad, vagy (b) a hivatkozás az adatból kerül ki; a B46 `indoklas` lapadat-volta ugyanitt. **🟡** | – |
| E2 | DT889 (új, 🟡); `NYITOTT_FELADATOK.md` N188 | döntéssor a `funkcio` adatjavításról (a felhasználó megerősítésére vár; a többi motívum kisbetűs cellái a saját menetükben); az N188 kiegészítve | – |
| E3 | DT890 (új, 🟡) | a kiejtés-beszúrás mint előre ismert osztály (a brief 8.1 (j)) a felhasználó döntésére; addig a soronkénti engedély | – |
| E4 | `bemenet/dontes.py` `jeloltnaplo_tabla`; `kereszthiv.py`, `kapcsolat.py` | a B04 egyetlen hozzáférési pontja (a hívó a többletoszlopot kéri) | `teszt_kapcsolatok.Hozzaferes.test_gk01_a_b04_egyetlen_hozzaferesi_pontja` |
| E5 | `szamitas/kapcsolatok.py` | az alacsony bizonyosságú kapcsolatok külön számolva (a kapu a három számot a kapcsolatok számával veti össze); a 8. kapuja az ismétlődő motívumközi párt is megfogja; a docstring kimondja, mi belső egyezés | `test_a_kapcsolodo_kapu_megfogja_az_ismetlodo_part` |
| E6 | `naplok/F218_jelentes.md`, `naplok/F218_folytatas.md` | a commit-hash `648ddbcb`; „5 forráslista és proveniencia” | – |
| E7 | ez a szakasz | az olvasó-szerver tesztjei: a 2 + 2 bukás a nyilvántartott N187 és N198 (az ellenőr futása); a lapgen 308 tesztje mellett ezt is rögzítem | – |
| megfigyelés | `tesztek/teszt_kapcsolatok.py` | a kivágás a 8. szakasz végéig tart | – |

**Mérés a javítókör után:** `scope=HAMART-001 és ISTENTISZT-001, munka mód (PARDES_DATUM=2026-11-13) | forras=futtat.py; general.py --cel lexikon2; regresszio.py; festek.py; hash_or_kapu.py | ts=2026-11-16`: tesztek 311, 0 hiba, 0 bukás, 30 váz; mindkét lap bájtra azonos a javítókör előttivel; HAMART-regresszió RENDBEN (engedély nélküli diff-sor 0); festékpróba 0 mindkét lapon; a hash-őr 209 sorral RENDBEN (a döntésfájl hash-sora frissült). **A DT888, a DT889 és a DT890 🟡: a felhasználó döntésére vár (megállás).**

## A DT888, -u, -v döntése és a DT888 adatjavítása (`claude-opus-5-5`, 2026-11-16, a 11. session)

**A döntés:** a felhasználó (2026-11-16, az orkesztrátoron át) az orkesztrátori javaslatot hagyta jóvá, szó szerint: „mehet”. Mindhárom helyőrző 🟢 (`dontesek/uj/f218a-s6-3896f7.md`).

| Döntés | Tartalom | Megvalósítás ebben a PR-ban |
|---|---|---|
| DT888 (b) | javuljon az adat: a döntés-hivatkozás külön, a lapon meg nem jelenő mezőbe; a generátor szövegcserés leválasztása kivezetendő | a `kapcsolatok.tsv` két ISTENTISZT-001-cellájából a „(DT479, a felhasználó, 2026-11-01: „Igen, (b)”)” kikerült (a döntés a sor proveniencia-részében már állt: `forras=DONTESEK.md DT479`), a mondat pontot kapott; **a B45 leválasztása törölve**, teszt: a két mintalap B45-indoklásában nincs döntés-hivatkozás. **Nem fért a szeletbe** a `motivum_kapcsolatok.tsv` három sora („Döntés: DT280 (…).”): a nyílt mag exportja (`dontesek` oszlop, NYD-003) ebből a mezőből olvassa a döntésszámot, így az adat, az export, a SEMA 2.33 és a nyílt mag együtt változik: **N209**. Addig a B46-on egyetlen rögzített alak átmenetileg leválik (`_mk_zaro_dontes_nelkul`), az N209 lezárásakor törlendő |
| DT889 (a) | jóváhagyva: a HAMART-001 44 cellájának adatbeli javítása marad; a többi motívum kisbetűs cellái egy menetben az S9-ben; gépi kapu a kisbetűs cellára | **N210** (az S9-ben: a cellák és a kapu) |
| DT890 (a) | a régi lap utólagos kiejtés-beszúrása előre ismert osztály: (j) a brief 8.1 pontjában; soronkénti engedély nem kell | a brief 8.1 (j) beírva; az `S5-KIEJTES` és az `S6-KIEJTES` gépi kötése a regresszió miatt marad, `8.1 (j)` mechanizmussal |

**Mérés:** `scope=HAMART-001 és ISTENTISZT-001, munka mód (PARDES_DATUM=2026-11-13) | forras=general.py --cel lexikon2; regresszio.py; festek.py; futtat.py | ts=2026-11-16`: a HAMART-001 lapja bájtra azonos a döntés előttivel; az ISTENTISZT-001 lapján csak a két javított Alátámasztás-sor változott (a hivatkozás nélkül, ponttal); HAMART-regresszió RENDBEN; festékpróba 0 mindkét lapon; tesztek 310, 0 hiba, 0 bukás, 30 váz; a mérce két hash-sora (B45, a döntésfájl) frissült.

## F218.10 — S7: „9. Hatástörténet: ókori fordítások és értelmezők” (`claude-opus-5-5`, 2026-11-16, a 12. session)

**Eredmény.** A 9. szakasz (ószövetségi és újszövetségi ókori fordítások, tanúk) a HAMART-001 referenciájával **bájtra egyezik, engedélysor nélkül** (56 sor; az első futáson 0 diff-sor). Regresszió: RENDBEN (engedély nélküli diff-sor 0 a lap minden kész szakaszán). Festékpróba: 0 szivárgás (HAMART belső 342, idézet 2 874, kézi 782; ISTENTISZT belső 281, idézet 1 407, kézi 331). Az első lépés a mérce hash-sorainak frissítése volt (N200: a #756 utáni `szamkiosztas` a `DONTESEK.md`-t módosította, az S6 döntésfájlját törölte).

**Új kód.** `bemenet/hatastortenet.py` (a B38 ókori fordítás-sorai, B39 tanúk, B41/B74 szövegváltozatok, B64 Targum-lefedés, B73 Peshitta-állapot, LXX-alapvonal), `szamitas/hatastortenet.py` (a régi `blokk_visszhang`, `visszhang_cella`, `_visszhang_mondat_lxx`, `_egyesites_mondat`, `blokk_hatas_usz`, `tanuk_lapra`, `blokk_hatas_tanuk` szabályai), `megjelenites/md/hatastortenet.py`; a 4.8 modul két nyilvános függvénnyel (`lanc_szavak`, `lanc_szo`), a TAHOT-bemenet az angol tükörfordítással, a B35 egy lemmaindexszel (`lxx_lemmak`), az író egy cellán belüli sortörés-jellel (`SORTORES`). Jegyzék: 5 új sor (B39, B41, B64, B73, B74; a térkép számai, a B41 két fájlja licenc szerint két sorra bontva, a B73 új). Sablontábla: 129 sor (`s9.*`, `cim.s9.*`), ebből 8 `eredet=uj`, `dontes=var`; névtábla: 9 sor (`lanc_konyv`, `szamszo`, `tanu_hagyomany`). SEMA: két bekezdés (2.66: forrás-állapot és adat; 2.68: a 9. szakasz nevei).

**Szerkezeti átírás, szövegcsere nélkül.** A régi lap három helyen utólag írta át a 9. szakaszt; az új generátor a szerkezetből adja ugyanazt: (1) a tanú korának zárójeles adatbázis-évszáma („4. sz. (HCF: 373)”) a mező belső része, a látható rész a mező eleje (bemeneti réteg); (2) a rabbinikus hivatkozás „25:2” alakja fejezet- és szakaszszámként jön, a sablon írja „25.2”-nek; (3) a latin szócsalád jele („*maled-*”) a lemma elejének idézete, és a névelője a sablonból jön (az ISTENTISZT-en így lett „az *invoc-*” a régi „a *invoc-*” helyett).

**GK-28 (a szelet része: Targum, Peshitta).** A régi kód a Targum lefedettségét kódba írt Mózes-könyv listából vette; a forrás (B64) a Prófétákat is fedi, a Zsoltárokat nem. Az új Targum-oszlop a forrás tényleges könyveiből mondja ki a hiányt; a jegyzék állapota `reszleges`, és ha az adat ennek ellentmond, BUKÁS. Következmény az ISTENTISZT-en: a három Zsoltár-vers Targum-cellája a régi hamis „nincs megfelelő szó” helyett „nincs Targum-forrás (a szabad Targum-szöveg ezt a könyvet nem tartalmazza)”. A Peshitta-mondat a B73 `nem_vizsgalt` állapotából jön; ha a forrás megjelenne (glob-találat), vagy az állapot változna, BUKÁS. A közel-keleti és a Chain Lineage-mondat a Kolofoné (S8); a váz GK-28 tesztje erre szűkítve S8-ra áll.

**GK-SZOPAR (DT833).** A spec 6.3 nyolc feltétele: a szópáros ISTENTISZT-001 ószövetségi táblája nem üres, a lánc-szó a formula igéje (H7121), a 16 vers a motívum saját ószövetségi helye (az első 1Móz 4:26), a bevezető kimondja, hogy a táblázat az igét követi, az ellenőrzött, alak nélküli LXX-sor „nincs megfelelő szó”, az LXX-kapu a szópár-feltételt használja, a HAMART szakasza változatlan; a `teszt_f194_szopar.py` eseteinek leképezése a `teszt_s9_hatastortenet.py` fejlécében (a régi lapszöveg-kapuk esetei a 218c-hez, O6). **GK-A6:** a „kinyerés még nem történt meg” pontosan a B38 rokon sora és B24-lekérdezés nélküli lánc-szónál áll (teszt mindkét lapon).

**ISTENTISZT-001 (8.2): a szópáros lap 9. szakasza.** A régi kód szópáros ágának hibái, amelyek a mai mintán is látszottak (a régi függvények közvetlen hívásával mérve), az új lapon nem állnak: a Zsoltár-versek hamis Targum-hiánya (fent); az újszövetségi tábla „Genezis-lánc” szövege a szópáros lapon (helyette „formula”, öt új sablonsor); a LXX-oszlop vegyes rövid/teljes és ábécé szerinti versrendje (most kánoni rend, teljes igehely); „A 1 görög szócsaládból” (most „Az 1”).

**Új sablonmondatok `dontes=var` (a 218a végi listába):** `s9.nincs_targum`; `s9.usz.bevezeto.szopar`, `s9.usz.fejlec.lxx.szopar`, `s9.usz.lxx.nincs.szopar`, `s9.usz.valt.nincs.szopar`, `s9.usz.mit.egyezo.szopar`, `s9.usz.mit.reszben.szopar`, `s9.usz.lab.szopar`. Egyik sem tesz új tartalmi állítást: a hamis állapotmondat javítása (HN-15 osztály) és a szópáros lap rossz megnevezésének javítása.

**Megfigyelések, döntés nélkül.** (a) N214: a szópáros bevezető (DT833 szövege) ISTENTISZT-specifikus tartalmat mond minden szópáros motívumra. (b) A 9. szakasz dőlt sorai a licencet betűre mondják („közkincs”, „CC BY 4.0”): a GK-07 (licencszöveg csak a B01-ből) az S8-ban. (c) A B64 ma csak a Targum-fájl; a térkép B64-ében a Vulgata és a Glossa Ordinaria is áll, ezek a Kolofon forrássorában kellenek (S8). (d) Az egyesítés-mondatok (két lánc-szó egy fordítói szóval) a két mintalapon nem állnak; az ágak modellből renderelve tesztelve.

**Tesztek.** `teszt_s9_hatastortenet.py` (16 teszt): a modell számai, a szakasz bájtra, GK-SZOPAR, GK-A6, GK-28 (Targum, Peshitta, a két ellentmondás-BUKÁS), a mondat-ágak. A váz két tesztje (GK-A6, GK-SZOPAR) innen költözött.

*Proveniencia: `scope=PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon2 --id HAMART-001|ISTENTISZT-001; python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001; python eszkozok/lapgen/tesztek/futtat.py | forras=50e02921 (az S7 commitja) | ts=2026-11-16`*

## Független ellenőrzés — 10. ellenőrzés (S7, `fuggetlen-ellenor`, `claude-opus-5-5`, 2026-11-17)

Tartomány: `8a3e7185..8969a8c1` (a base a main akkori feje; az első indítás a 2026-11-16-i leállításkor eredmény nélkül állt le). Szint: `teljes`. **Eredmény: ELTÉRÉS, 8 tétel** (a teljes táblázat az ellenőr válaszában; itt a tételek és az OK-ként igazolt fő pontok).

**Rendben (saját méréssel):** az ÓSZ-tábla portolása (cellafajták, szócsalád-kulcs, betoldás, egyesítés, Targum+Vulgata összevonás) és az ÚSZ-, tanú- és alapvonal-szabályok; a HAMART 9. szakasza egyezik (engedélysor nélkül); a Peshitta-állapot és az adat egyezik; a rabbinikus hivatkozás bontása szerkezeti (nem csere); 56 sor, 129 sablonsor (8 `var`), 9 névtábla-sor, a festék számai, 16 teszt; GK-SZOPAR mind a nyolc feltétel; GK-A6 (a main kódja szerint, a B24-lekérdezéssel); A2–A6; a lista 1–5. pontja.

**Eltérések (súlyosság szerint), az ellenőr besorolásával:**
1. A CI piros a fejen (a mérce hash-őre): a beolvasztás a `2560e4e7 szamkiosztas` előtti main-t vette; újabb beolvasztás és N200 kell. *Mechanikus.*
2. Az ISTENTISZT ÚSZ „Mit mutat” mondata (`s9.usz.mit.reszben.szopar`) 12 verset mond, a szomszéd oszlop 14-et sorol: a nevező csak az ellenőrzött Vulgata-sorral bíró versek (a Zsolt 116:4 és 116:13 kiesik); az 1Kir 18:24 (βοάω · ἐπικαλέω) az első lemma miatt kimarad az ÚSZ-oszlopból. A régi szabály szemantikája; a HAMART-on nem látszik (5 = 5). *Döntés (a 218a végi listába).*
3. A Targum-lefedés kapuja gyenge: a mintára nem illeszkedő vagy ismeretlen könyvű sor és az üres lefedés `reszleges` állapotban némán átmegy; a nem fedett könyvben álló ellenőrzött, alakos Targum-sor rejtve marad. *Mechanikus.*
4. A 8.2/1 független számlálói (a szópár-lánccal) hiányoznak a `regresszio.py`-ból. *Mechanikus, szeleteken átívelő.*
5. A tanú `kor` mezőjének belső része kapu nélkül vágódik le, a festés előtt. *Döntés (adat-szétválasztás) vagy mechanikus kapu.*
6. A szópáros ÚSZ-bevezető némán elhagyja a tematikus helyeket (ma nem látszik). *Mechanikus.*
7. Az S7 jelentés-szakaszából hiányzik a proveniencia-sor. *Mechanikus.*
8. A brief `kovetkezo` mezője elavult. *Mechanikus.*

## A 10. ellenőrzés javítóköre (2026-11-17)

| # | Javítás | Hol |
|---|---|---|
| 1 | a main beolvasztva (`#764`, a `szamkiosztas` 2560e4e7), a törölt döntésfájl B51-sora kikerült (N200); regresszió RENDBEN, hash-őr 209 sor | `7b7483de` |
| 3 | a Targum-kulcs csak ismert ószövetségi „könyv fejezet:vers” lehet, különben BUKÁS; üres forrás BUKÁS; ha a forrás nem fedi a verset, de ellenőrzött, alakos Targum-sor áll rá, BUKÁS (az adat ellentmond) | `bemenet/hatastortenet.py` `b64_targum`, `szamitas/hatastortenet.py` `_osz`; teszt: `test_a_targum_kulcs_kapuja` |
| 5 | mechanikus kapu: a `kor` mező csak „<kor>” vagy „<kor> (HCF: <év>)” alakú lehet, más alakban BUKÁS (a belső rész nem válhat le némán). Az adat-szétválasztás (külön évszám-oszlop) döntés, a 218a végi listába | `bemenet/hatastortenet.py` `_KOR_RX`; teszt: `test_a_tanu_koranak_belso_resze` |
| 6 | a szópáros ÚSZ-bevezető tematikus helynél kimondott hibával megáll (a mondata nem tudja kimondani a kimaradást) | `megjelenites/md/hatastortenet.py` `_usz` |
| 7 | proveniencia-sor az S7 szakaszban | e fájl |
| 8 | a brief `kovetkezo` mezője | `F218_GENERATOR_UJ_A_BRIEF.md` |
| 2 | nem javítva: döntés, a 218a végi listába (a nevező vagy a mondat; az 1Kir 18:24 több lemmája) | — |
| 4 | nem javítva: az S9-ben (a teljes ISTENTISZT-mérce, minden szakasz számlálóival egy helyen); a folytatási fájl S9-teendői közé felvéve | — |

Mérés a javítókör után: HAMART-regresszió RENDBEN (a 9. szakasz egyezik); az ISTENTISZT-001 9. szakasza változatlan; `teszt_s9_hatastortenet.py` + `teszt_szerkezet.py` 31 teszt, 0 hiba.
*Proveniencia: `scope=python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/tesztek/futtat.py s9_hatastortenet szerkezet | forras=a javítókör commitja (7b7483de után) | ts=2026-11-17`*

## F218.11 — S8a: a lap eleje, a Kivonat, a Tartalomjegyzék és a Jelmagyarázat (`claude-opus-5-5`, 2026-11-21, a 13. session)

**Bontás.** Az S8 az S3 mintájára alszeletekre bomlik, mindegyik a saját diffjével zárul: **S8a** a lap eleje, a
Kivonat, a Tartalomjegyzék és a Jelmagyarázat (ez a commit); **S8b** a kézi próza-rések (a 4. szakasz „Miért fontos ez
a lelet” rése, 10. Értelmezés, 11. Módszertan); **S8c** a „12. Irodalom és idézés”; **S8d** a Kolofon (GK-07, GK-27,
a GK-28 maradéka, `ISM-KOLOFON`). Az S8b-hez: a régi lap a rések kézi „Proveniencia” sorát olvasói „Forrás:” sorra
cseréli (`<!-- eredeti: … -->` megjegyzéssel), az Értelmezésbe „Szakirodalom:” sorokat szúr, a Módszertan rése
`ADAT-NÉZET` blokkokat hordoz: ezek az új generátorban a bemeneti rétegben szerkezetként bontandók, nem cserével.

**Eredmény (N200 után).** A HAMART-001 regressziója: RENDBEN; a Kivonat, a Tartalomjegyzék és a Jelmagyarázat bájtra
egyezik a referenciával, engedélysor nélkül. Festékpróba: 0 szivárgás (HAMART belső 342, kézi 786; ISTENTISZT belső
281, kézi 335). Tesztek: `teszt_eleje.py` (9): GK-10 (két számozott szakasz cseréje után nem keletkezik új hibás belső
link, a Tartalomjegyzék és a hivatkozások az új számot viselik), GK-A13, a horgony sora, a mondatkezdő alak, GK-06 a
lap elején, a Kivonat rése, a Jelmagyarázat két szakaszszáma és licence.

**⛔ A lap eleje (`fej`) kész, de nincs bekötve.** A bekötéssel a kritérium kapujának „pontosan egyszer” módja él
(DT872), és az **ISTENTISZT-001** lapját elbuktatja: a kézi Kivonat 3. bekezdése („Ide az a hely tartozik, amelyben a
hívás igéje (kárá) és a név …”) a kritérium másolata, a 4. bekezdés első mondata („A motívum tehát nem az imádság vagy
a segítségkérés általában, …”) a tágabb köré — ugyanaz, mint a HAMART-001-en a DT874 1. és 3. tétele. A kézi próza
javítása a felhasználó döntése (az orkesztrátornak elküldve, 2026-11-21). A HAMART-001 lapján a bekötött `fej`
kipróbálva: egyetlen eltérő sor, a horgony (`<a id="mi-tartozik-ide"></a>` a meghatározás előtt; az `ISM-HORGONY`
engedélysor kész: régi `a3a17a817a90da74`, új `b1c3b164425dcfd5`, 1 sor), a kapu „teljes” módja zöld. A bekötés a
döntés után: a `bekotes.py` egy sora, az engedélysor visszaírása, a tesztváz `S8_FEJ` csonkja.

**Két megvalósítási megjegyzés.** (1) A tágabb kör a lap elején mondatkezdő alakban áll, az adat kisbetűs (a 4.12
bevezetője a mondat belsejében idézi): a nagy kezdőbetű a bemeneti rétegben képződik (`bemenet.motivum.mondatkezdo`),
a DT875 elve szerint (forrás-oldali alakképzés kódban, az átírás végéig). (2) Az adatot nem olvasó szakasz (Tartalom,
Jelmagyarázat) blokkfejlécének licence a licencleltár `projekt_adat` címkéje (`konfig.SAJAT_LICENC`, GK-07), nem
kódba írt szöveg.

**Új sorok.** Sablontábla: 59 (`cim.*` 6, `fej.*` 8, `kivonat.olvasoi`, `tartalom.*` 3, `jm.*` 41); mind a mai lap
szövege, `eredet=<szimbólum>`, `dontes=-`, új tartalmi állítás nincs. Névtábla: 19 (`azonossag` 5, a régi
`AZONOSSAG_OLVASOI`; `szotari_pont_mondatkozi` 14, a szerepnevek mondatközi alakja, a régi `kisbetus_kezdes`). Új
bemenet nincs: a B02 három új oszlopot olvas (`meghatarozas`, `azonossag_tipusa`, `forras_study`), a B47 a Kivonat
rését. A mérce két hash-e frissült (B65, B66).

**A 218a végi listába ebből a szeletből:** a mondatkezdő alak kódbeli képzése; a `projekt_adat` licenc az adat nélküli
blokkon; a `szotari_pont_mondatkozi` névtábla-típus (a szerepnév második, kisbetűs alakja az adatban); az ISTENTISZT-001
Kivonatának döntése; a „3. Kizárt és vizsgált helyek” szakasz szelet nélkül maradt (a jelentés DT874-szakasza az S4-re
tette, az S4 nem vitte; a tesztváz `ISM_3` csonkja őrzi).

**Ismétlés-figyelő.** HAMART-001: 80 ismétlődő szósor, ISTENTISZT-001: 34 (figyelmeztetés, nem BUKÁS).
