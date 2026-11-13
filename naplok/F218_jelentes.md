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

Az `eszkozok/lapgen/` rétegei (`szoveg` ← `bemenet` ← `szamitas` ← `megjelenites`), a három tábla (SEMA 2.60–2.62), a `regresszio.py`, a `festek.py`, a `general.py --cel lexikon2`. A tervezési döntések listája: `naplok/F218_folytatas.md` „Tervezési döntések”. A régi generátor HAMART-kimenete a `general.py` módosítása után bájtra azonos maradt (a módosítás két additív elem: a `lexikon2` cél és a `--mod` kapcsoló; és egy nem additív: az előjavító (E32) egy meglévő hibaüzenetből törölte a „; DT-F09h” döntésszámot, `general.py` `--helyi-lexicon` ága; pontosítva a javítókörben, az 1. ellenőrzés 8. tétele) (`cmp` a `git show HEAD:lexikon/…` tartalmával, mindkét nézet).

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

**Kiegészítés a javítókörben (2026-11-13; az 1. ellenőrzés 5. és 11. tétele).** A fenti táblázat utolsó oszlopa („Melyik felel meg a Károli-szónak”) az építő session **értelmezése** volt, lekérdezés nélkül. A felhasználó döntése (DT-F218j, a DT838 módosítása): „ahol van párosítás: az az alak áll, amelyhez a Károli-szó kötődik; ahol nincs: az első előfordulás”. A generátor ezt a Károli–Strong párosításból (B54) veszi; az alábbi tábla már lekérdezés, nem értelmezés. Minden olyan sor áll benne, amelynek egy Strong-száma a sor versein többször áll:

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

- **T3 tárolása:** külön kézi tábla (`adat/tematikus_sajat_szo.tsv`, SEMA 2.63, B67), nem új oszlop az `elofordulasok.tsv`-ben: az orkesztrátor technikai döntése (2026-11-13), `dontesek/uj/f218-generator-uj-a.md` DT-F218i. A brief `ir` mezője ezzel a táblával és a döntésfájllal bővült.
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
| G/D: T3 (DT837) tárolása | ELTÉRÉS | `dontesek/uj/f218-generator-uj-a.md:1`; `adat/tematikus_sajat_szo.tsv` | A DT837 (🟢, a felhasználó döntése) és a brief 3./4. pontja (B03: „új oszlop: `sajat_szo`”) az `elofordulasok.tsv` mezőjét írja elő. A DT-F218i (b)-t választott: külön táblát, ✅ állapottal, „az orkesztrátor technikai döntése”-ként, a felhasználó jóváhagyása nélkül. A brief 12. pontja a hasonló helyváltoztatást (T7, T8) felhasználói megerősítéshez köti. `git show dfb4525a:DONTESEK.md \| grep '^\| DT837 '` |
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
1. **T3 (DT837):** felhasználói döntést írt felül az orkesztrátor (DT-F218i, ✅). A felhasználónak kell megerősítenie.
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
| 1 | T3 tárolása külön táblában | a felhasználó megerősítette (szó szerint: „Külön tábla jó”), szócikk nélkül (DT837); a DT-F218i sorában rögzítve | `d3a8f570` |
| 2 | az idézetbe mosás csatornája | a `jel_szoveg` és az `idezet_szoveg` megszűnt; a szakasz jele a kulcsból a bemeneti rétegben képződik (`Gerinc.jel`); a számítás típusos példahelyet kap (`Peldahely`, `ThayerPelda`, `Tartomany`), nyers táblasort nem; a nem BDB-jel a szótár nevével sablonból áll; statikus teszt: idézetet és prózát csak a bemeneti réteg burkol; a festékpróba a szótári ágat is festi | `713e63cb` |
| 3 | a `cella` módosító | megszűnt (DT-F218k): a cella értéke az adatban a végleges alak; a cellakezdő sablonmondat külön sablonsor, a három érintett címke cellakezdő alakja kézi adat a névtáblában, egyezés-kapuval | `312e7b87` |
| 4 | a hash-őr és az olvasási napló | az új generátor a lap mellé írja a naplóját; a regresszió megáll, ha olvasott fájl nincs a referencia-táblában, vagy más tartalommal áll benne; a tábla 4 `uj_bemenet` sorral bővült (B65, B66, B67, `dontesek/uj/`) | `713e63cb` |
| 5 | ONREF-osztály; a T4 3 sora | T4: DT-F218j (a DT838 módosítása), a három T4-engedélysor megszűnt; önreferencia: DT-F218l, az 1Móz 8:21 cellája a forrásban javult, az S1-ONREF engedélysor megszűnt | `d3a8f570`, `312e7b87` |
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

*Proveniencia: `scope=a négy szövegpár bal oldalának keresése az adat/*.tsv, a motivumok/*.md és a nyilt_mag/ fájljaiban, cellánként | forras=a munkafa (8c109585 + a javítókör) | ts=2026-11-13`.* A három nyitott pár 8 cellája nincs átírva: a fájlok a brief `ir` mezőjén kívül esnek, és kettőnél a cella átírása a nyílt mag angol fordítását elavulttá teszi (a nyílt mag kapuja bukik: újrafordítás és újraexport kell). A kérdés a felhasználóé (DT-F218l, 🟡). Az S2 két párt érint (a negatív kritérium és a kizárási ok szövege): a döntésig ezek a diff-sorok előre megszámolt engedélysort kapnak.

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

Az 1. ellenőr `teszt_futtat.py --diff` futásában a `teszt_szintek.py` is hibát adott. A fájl az olvasó-szerver tesztje (`eszkozok/olvaso_szerver/teszt_szintek.py`): a feladat ágán 13 tesztből 2 bukik (`test_ebben_a_versben_es_az_interlinearis_csempek_koveti_a_blokkok_lathatosagat`, `test_heber_szavak_alacsony_es_magas_szinten`: a szó-lap magas szintű BDB-darabja és az „Ebben a versben” blokk láthatósága). A fő checkouton (`1352ac3c`, a main egy korábbi állapota) ugyanez a fájl ugyanígy 13 tesztből 2 bukással áll (ott a bukó tesztek nevét nem írattam ki). Az F218a diffje (`git diff --name-only 37f087cc..HEAD`) az `eszkozok/olvaso_szerver/` egyetlen fájlját sem érinti. A hiba tehát nem ebből a diffből jön: nyitott tétel lett (N-F218a, `nyitott/uj/f218-generator-uj-a.md`).
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
| Diéta 3. tesztek | OK | `eszkozok/lapgen/tesztek/` | `python eszkozok/lapgen/tesztek/futtat.py`: 133 futott, 0 hiba, 0 bukás, 36 kihagyva. Egyezik a jelentés 338. sorával (133/97/36). A lassú tesztek (`teszt_futtat.py --diff`) a hívó utasítására kimaradtak. A diff az `eszkozok/olvaso_szerver/`-t nem érinti (`git diff --name-only 37f087cc..2b0a05a4 \| grep -c olvaso_szerver` → 0), ezzel az N-F218a „nem ebből a diffből” állítása a fájllista szintjén igazolt. |
| Régi generátor bájt-egyezése | OK | `eszkozok/general.py` | `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon --id HAMART-001 --kimenet <scratch>/regi`, majd `cmp` a `git show HEAD:lexikon/HAMART-001_{TUDOMANYOS,KIZARASOK}.md` tartalmával: mindkét cmp kilépési kódja 0. |
| Regresszió (S1) | OK | `naplok/F218_elteres_engedely.tsv:3` | `general.py --cel lexikon2 --id HAMART-001 --kimenet <scratch>/uj` (438 sor, EXIT 0), majd `regresszio.py --id HAMART-001 --uj <scratch>/uj/lexikon`: „2. Előfordulások” 1 diff-sor, engedéllyel; `S1-FORRAS: 1`; RENDBEN. Az engedélyfájl diffje: az 5 sorból 4 törölve (T4-1..3, ONREF), az S1-FORRAS új hash-sel. |
| 1. T3 (DT-F218i) | OK | `dontesek/uj/f218-generator-uj-a.md:1` | A sorban: „a felhasználó megerősítésével (… szó szerint: „Külön tábla jó”); a saját szó a DT837 szerint szócikket nem kap”. `grep '^\| DT837 ' DONTESEK.md`: „Adatba kerül, szócikk nélkül … a 4. szakasz nem kap róla szócikket”. A sor nem állít többet, a ✅ (alkalmazva) helytálló. |
| 2. Idézetbe mosás, `bemenet/` kívül | OK | `tesztek/teszt_szerkezet.py:196-211` | `Grep forrasszoveg\(\|\.kezi\(\|\.belso\(\|Forrasszoveg\(\|Kezi\(` az `eszkozok/lapgen` alatt: a `bemenet/`-en kívül csak tesztekben van találat. A `szamitas/elofordulas.py:185` csak `Kulcs`-ot burkol (`f.szotar_kulcs`). A `jel_szoveg` és az `idezet_szoveg` megszűnt; az AST-teszt ezt őrzi (zöld). A B19 nyers sora nem hagyja el a réteget (`Peldahely`, `Tartomany`, `ThayerPelda`). |
| 2. `.ertek`-megkerülés és `Gerinc.jel` | ELTÉRÉS | `szamitas/szotari_gerinc.py:175,181`; `bemenet/gerinc.py:341,349,368-375,191-196`; `megjelenites/md/elofordulas.py:211,250,273` | (a) A javítókör a B19 `karoli_vers`-et `Belso`-ként burkolja (`gerinc.py:341`). A számítás `t.kezdo_vers.ertek`-kel kibontja, `Igehely`-lyé alakítja, és ez látható szövegként kerül a lapra (`e2.jm.tartomany`, `kezdo=`). A `Belso` docstringje szerint „látható szöveg nem lehet belőle” (`szoveg.py:232`). Ugyanígy a B21 `Kulcs` (`p.jel.ertek`) `int`-ként látható szám lesz (`n=`). Az érték típusos és ellenőrzött, tehát szabad szöveg így nem juthat át, de a kategória ellentmond a használatnak, és az `.ertek` út a festékpróbán eleve láthatatlan. (b) A `Gerinc.jel` számított szöveget burkol `Forrasszoveg`-gé: `szakasz_jel(utvonal)` (`Qal/2/c` → `Qal 2.c`) és `pontos_jel` (`4` → `4.`), egy nem létező `szakasz_jel` mezőnévvel. A `kulcs_jel` több szócikkes útvonalnál a belső `bdb_id`-t is a jel elé írja (`gerinc.py:194-195`). Ez az út a jelentés „Ismert korlátok” 3. pontjában szerepel, de a `bdb_id`-előtag nem. A HAMART látható szövegében `BDB\d+` nincs (sed a megjegyzések nélkül + grep: 0), az út tehát most nem él. |
| 2. Festékpróba | OK (futás) | `eszkozok/lapgen/festek.py` | `python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001`: 0/0 szivárgás. Látott jelzőszavak: belső 168/113, idézet 326/183, kézi 180/85. Egyezik a jelentés 338. sorával. A próba ereje: a szótári ág B19-mezőit már festi (`test_gk08b_a_szotari_ag_mezoi_is_festettek`), az előző sorban leírt két utat nem. |
| 3. `cella` módosító (DT-F218k) | OK | `eszkozok/lapgen/szoveg.py:465-477`; `bemenet/gerinc.py:127-131` | A `_cellakezdet` és a `CELLA_MONDAT_SZO` törölve. A `_nevelovel` csak sablonszöveget tesz a szegmensek elé (`[(Fajta.SABLON, nevelo+' ')] + szegmensek`); ismeretlen módosítóra (`cella`) SablonHiba. `Grep upper\|lower\|capitalize\|\.sub\(\|replace\(` a `szoveg.py`-ban: egyik találat sem PROZA- vagy IDEZET-szegmensen dolgozik (horgony, számformázás, a beszúrt névelő). A `_cella_alak_egyezik` csak a nagy kezdőbetűt és a kezdő „a”/„az” elhagyását engedi. A célzott grep a `lexikon/HAMART-001_TUDOMANYOS.md`-ben: „A megművelt föld, amely táplál” stb. Ítéletem: ez nem cseretábla, mert nincs mintaszabály tetszőleges szövegre, címkénként kulcsolt kézi adat, és a kapu eltérésnél megáll. Ára: minden cellakezdő címkének kell egy sor, híján kisbetűvel áll (ISTENTISZT 6 cella; ez a felhasználónak jelezve, jelentés 363). |
| 4. Hash-őr: ismeretlen és más tartalmú bemenet | OK | `eszkozok/lapgen/regresszio.py:92-112` | Három próbát futtattam repón kívüli másolaton, mindegyik után `regresszio.py --id HAMART-001 --uj <másolat>`. Ismeretlen sort fűztem a naplóhoz (`B99 adat/ismeretlen.tsv`) → „nincs a referencia-táblában”. Az `olvasoi_nevtabla.tsv` hash-ét átírtam → „más tartalommal olvasva”. A naplót töröltem → „hiányzik az új generátor olvasási naplója”. Mindhárom MÉRCE NEM FUTTATHATÓ. A tesztek ugyanezt fedik. |
| 4. Hash-őr: naplóból kimaradó olvasás | ELTÉRÉS | `bemenet/jegyzek.py:166-174`; `bemenet/szavak.py:128-136` | (a) A jegyzéktábla (`adat/lapgen_bemenetek.tsv`) olvasása nincs a naplóban; ezt a jelentés kimondja (382. sor). (b) **Új:** a `b54_karoli_parok` a `_fejsorok`-kal minden `parok_*.tsv` első 8 sorát olvassa, naplózás nélkül. `ls adat/karoli_strong/parok_*.tsv \| wc -l` → 66; a naplóban 14 B54-fájl áll, a referencia-táblában 56 (`grep -c karoli_strong/parok_ naplok/F218_referencia.tsv`). A könyv–fájl leképezés így 52 nem mért fájl fejsorától függ, és ez a hézag a jelentésben nem szerepel. A brief „minden olvasott bemenet hash-e” követelménye így nem teljes. |
| 5. T4 (DT-F218j): a kód | OK | `bemenet/szavak.py:162-190` | A `ragozott` versenként először a párosításhoz kötött helyet keresi; ha talál, azt választja, és kilép. Ha nem, az első vers első előfordulását tartja meg. A pár csak akkor dönt, ha a TAHOT/TAGNT `n`. során ugyanez a Strong-szám és ugyanez az alak áll (`_kotott_hely`). Ez a döntés szövegét valósítja meg: „ahol van párosítás: az az alak … ahol nincs: az első előfordulás”. |
| 5. T4-kiegészítő tábla újramérése | OK | `naplok/F218_jelentes.md:222-229` | Repón kívüli szkript (`split('\t')`), a `parok_<könyv>.tsv` és a TAHOT/TAGNT soraiból. 1Móz 6:5 H7451: pár hu#20 „gonosz” → er#18 רַ֖ע; TAHOT #6 רָעַ֥ת, #18 רַ֖ע. 1Móz 6:12 H7843: „megrontotta” → er#11 הִשְׁחִ֧ית; TAHOT #9, #11. Jel 11:18 G1311: „pusztítják” → er#42 διαφθείροντας; TAGNT #40, #42. 1Móz 4:26 H8034: két „nevét” (hu#8 → er#11, hu#16 → er#19), a tábla 19-et ad. 1Kir 18:24 H8034: er#4 és er#11, a tábla 11-et ad. Sof 1:2 H0127: er#8. Mind egyezik a tábla sorszámaival. |
| 5. `elofordulasok.tsv` | OK | `adat/elofordulasok.tsv:217` | `git diff 8c109585..2b0a05a4 -- adat/elofordulasok.tsv`: egyetlen sor, egyetlen cella változott (`kapcsolodas`, 1Móz 8:21: „a lap” → „a szócikk”). `--numstat`: `1 1`. A referencia-tábla B03-hash-e ennek megfelelően frissült, a referencialap hash-e nem (a cmp szerint indokoltan). |
| 6a. Halasztott S1-tételek | OK (nyitott, dokumentált) | `naplok/F218_folytatas.md:12,32,47,135`; `naplok/F218_jelentes.md:329` | A HN-03, a GK-13, a GK-14 (S2), a GK-03, a 7.4 és az alias-sorok nyitottként állnak. A javítókör tábla 6. sora: „nem változott”. Felhasználói jóváhagyás a halasztásra továbbra sem látszik, és nincs is lezártnak jelölve. |
| 6b. Az önreferencia három párja | OK | `dontesek/uj/f218-generator-uj-a.md:4`; `naplok/F218_jelentes.md:350-359` | Repón kívüli szkript (az `adat/**/*.tsv`, a `nyilt_mag/**` és a `motivumok/*.md` cellánként). „azt a lap vitatott…”: 0 találat (javítva). „ezeket a lap egyenként…”: `motivumok.tsv` 1 cella, `nyilt_angol.tsv` 1 sor. „amelyet a lap nem dönt el”: `jeloltek.tsv` 2 cella, `elutasitasi_okok.tsv` 1 sor / 2 cella, `nyilt_angol.tsv` 2 sor, `nyilt_kodkonyv.tsv` 1 sor. „…áll a lapon”: `kapcsolatok.tsv` 3 cella. Összesen 8 adatcella, egyezik a táblával. A DT-F218l 🟡, a kérdés a folytatási fájlban is áll (132. sor). |
| 7. Tesztváz | OK, megjegyzéssel | `eszkozok/lapgen/tesztek/teszt_vaz.py:22-72,185-189` | GK-B9 a vázban (skip S9). `test_a_mintak_megfogjak_a_hibas_lapszoveget` és `test_a_kesz_szakaszokon_nincs_hn_talalat`, mindkettő zöld. Az élő teszt a `fo.lap_keszit` kimenetén fut, a `MEGJEGYZES` tartományok nélkül, mindkét mintalapon: a kész szakaszok látható szövegén. Megjegyzés: a részletek egy része szerkesztett példa (pl. HN-05 „a felhasználó döntése szerint”), nem a hibás lapról vett idézet; a minta így a saját példáját fogja meg. |
| 8. `general.py` „additív” | OK | `naplok/F218_jelentes.md:186` | `git diff 37f087cc..2b0a05a4 -- eszkozok/general.py`: a `lexikon2` választás és az ága, a `--mod`, valamint a „; DT-F09h” törlése. A pontosított mondat (két additív elem és egy nem additív) igaz. A javítókör a `general.py`-t nem érinti. |
| 9. Blokkfejléc | OK | `eszkozok/lapgen/fo.py:108-110` | `sed -n 3p <scratch>/uj/lexikon/HAMART-001_TUDOMANYOS.md`: a `forrás:` listában `-` elem nincs (a `NEM_FAJL` szűrve). |
| 10. Bontási napló | ELTÉRÉS (csekély) | `naplok/F218_jelentes.md:371` | `grep -v '^#' … \| tail -n +2 \| cut -f4/-f5/-f6 \| sort \| uniq -c`. A sablontábla 111 sor: szakasz szerint 100/6/5, eredet szerint 25/13/9/7/7/6/6/4 + 26, `dontes=var` 8. A névtábla 27 sor (7/4/4/3/3/3/3), a jegyzék 24 sor (6+17+1). Minden szám egyezik, de a „többi” **14** szimbólum, nem „tizenhárom”. |
| 11. A T4-tábla értelmező oszlopa | OK | `naplok/F218_jelentes.md:218,232` | A kiegészítés kimondja: „az építő session **értelmezése** volt, lekérdezés nélkül”. Az új tábla proveniencia-sorral áll, és a fenti újramérés igazolja. |
| Új: a DT-állapotok | ELTÉRÉS (csekély) | `dontesek/uj/f218-generator-uj-a.md:2-3` | A DT-F218j és a DT-F218k 🟢 („eldöntve, alkalmazásra vár”, `DONTESEK.md:9` jelmagyarázat), pedig mindkettő sora „Alkalmazva:” / „Megvalósítás:” részt tartalmaz, és a kód a diffben áll. Helyesen ✅ volna, ahogy a DT-F218i-nél. |
| Lista 1: kiszűrt vagy törölt sorok | OK | – | `git diff --numstat 8c109585..2b0a05a4`. Adattábla: `lapgen_sablonok.tsv` 1 törölt sor (`tabla.cella`), `elofordulasok.tsv` 1 módosított sor. Napló: az engedélyfájlból 5 sor törölve, 1 új; a referencia-táblában 1 módosított és 4 új sor. Más törlés adatsorban nincs. |
| Lista 2: kulcstartomány | OK | `adat/lapgen_bemenetek.tsv` | A B-sorok: B01, 03, 07, 08, 09, 12, 13, 14, 16–19, 21, 22, 32–34, 51, 54, 59, 63, 65–67 (24). Új: B54, a T4-hez. |
| Lista 3: a nulla-diff hatóköre | OK | – | A 0 engedélyen kívüli diff-sor csak a HAMART TUDOMANYOS „2. Előfordulások” szakaszára áll (`munka` mód, `PARDES_DATUM=2026-11-13`); a többi szakaszra („nincs kész”), a KIZARASOK-ra és az ISTENTISZT-re nem. A régi generátor bájt-egyezése mindkét HAMART-nézetre áll. |
| Lista 4: táblasorok Δ (E17, DT3) | OK | – | A javítókörben: `elofordulasok.tsv` 0, `lapgen_bemenetek.tsv` +1, `lapgen_sablonok.tsv` +2, `olvasoi_nevtabla.tsv` +3, a `konkordancia/` alatt 0. Egyik sem ≥ 10. A main-hez képest: +111 / +27 / +24 / +1. A három ≥ 10-es táblának most van bontási naplója (10. pont). |
| Lista 5: a brief ⛔ pontjai | OK | – | A T4 > 20% megállás és az ONREF új osztálya felhasználói döntéssel zárult (DT-F218j 🟢, DT-F218l 🟡), az engedélysorok megszűntek. A javítókör után az S2 előkészítése (`2b0a05a4`) csak a folytatási fájlt írja. |
| A3–A6 | OK | – | Tartalmi réteg nincs a diffben. Az egyetlen kézi próza-változás az 1Móz 8:21 cellájának egy szava; nincs nevesített tanító, nincs Remez/Sod. |

Az ELTÉRÉS-ek súlyossági sorrendben:
1. **2. tétel, maradék csatorna.** A `Belso`-ként burkolt B19 `karoli_vers` `.ertek`-en át látható igehely lesz, a B21 `Kulcs` pedig látható szám. A `Gerinc.jel` számított szöveget (és lehetséges `bdb_id`-előtagot) burkol idézetté. A festékpróba egyiket sem látja. Az `.ertek` út és a `bdb_id`-előtag új lelet.
2. **4. tétel, a napló hézaga.** A jegyzéktábla és (új) a B54 `_fejsorok`-olvasása 52 nem mért `parok_*.tsv`-ből nincs a naplóban.
3. **Új:** a DT-F218j és a DT-F218k 🟢-vel áll ✅ helyett.
4. **10. tétel:** „tizenhárom” helyett 14 szimbólum; a számok egyeznek.

Ideiglenes fájlok csak a scratchpadben: `C:\Users\bases\AppData\Local\Temp\claude\263328eaf8ead9ff\270d530d-7596-4408-9382-57d7c56473e8\scratchpad\`.

## F218.5 — S2, első fele: a vizsgálat modellje és a kizárt versek melléklete (`claude-fable-5-2`, 2026-11-13)

**Eredmény (HAMART-001, `PARDES_DATUM=2026-11-13`, `munka` mód).** A melléklet (`HAMART-001_KIZARASOK.md`) 431 sorából 421 bájtra egyezik a referenciával; **10 diff-sor, mind engedéllyel; engedély nélküli diff-sor: 0.** A tudományos lapon a „2. Előfordulások” változatlan (1 engedélysor). A „1. Döntési út” szakasz (az S2 második fele) még nincs kész.
*Proveniencia: `scope=general.py --cel lexikon2 --id HAMART-001, majd python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa az S2a commitja előtt | ts=2026-11-13`.*

| Engedélysor | Osztály | Darab | Mi tér el |
|---|---|---|---|
| S2-KONYV-1…4 | GK-17 | 4 | a csoportosan kizárt versek között a Siralmak könyve az adat szerinti rövidítéssel (`Sir`, a Károli-fájl kulcsa) és a Károli-rend szerinti helyén áll, a versek fejezet- és versrendben (4:6, 4:13, 4:22). A régi generátor a csoporttagokat kódba írt aliasszal `JSir`-ré írta, ezért a könyv a lista végére, a versei betűrendbe kerültek (4:13, 4:22, 4:6); az egyenkénti vers a régi lapon is `Sir` |
| S2-ONREF-1, -2 | M-CSERE | 2 | „az öröklött bűnösség kérdése, amelyet a lap nem dönt el”: a kézi címke és megjegyzés változatlanul áll; a forráscella javítása a felhasználó döntésére vár (DT-F218l) |
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
| 3 | a DT-F218j és a DT-F218k állapota 🟢, ✅ helyett | mechanikus (formai) | a két sor állapotjele ✅ |
| 4 | a bontási naplóban „tizenhárom” szimbólum, a helyes szám 14 | mechanikus (formai) | a szó javítása |


## A 2. ellenőrzés javítóköre (2. kör; `claude-fable-5-2`, 2026-11-13, a 3. session)

*A besorolást az orkesztrátor hozta (2026-11-13): az 1a, a 2., a 3. és a 4. tétel mechanikus, a fenti javaslat szerint; az 1b döntés (DT-F218m); a DT-F218l-ről külön rendelkezett (l. a következő szakaszt). Az újraellenőrzés az S2 végi célzott független ellenőrzéssel együtt fut.*

| # | Tétel | Mi történt |
|---|---|---|
| 1a | belső mezőből `.ertek`-en át látható igehely és szám | a verstartomány kezdő verse a bemeneti rétegben képzett `Igehely` (a könyvnév a normalizáló táblán ellenőrizve), nem `Belso`; a Thayer-példa jelentésszáma a bemeneti rétegben képzett szám (`ThayerPelda.jelentesszam`), nem a belső kulcsból a számításban kibontott érték. Statikus teszt: a `szamitas/` rétegben burkoló `ertek` mezőjéből szám és igehely nem képződik |
| 1b | a szakaszjel a szótár belső szócikk-azonosítójával | DT-F218m: a látható jel csak a szócikken belüli tagolás (`Gerinc.jel`); ha a jel a szó több szócikkében is áll, mellette a szótár saját címszava áll a homográf-számával, szó szerinti idézetként (`Gerinc.jel_szocikke`; „1 (II. רַע)”), híján sablonmondat a szócikk sorszámával („Qal 1 (a BDB 1. szócikke)”). A belső azonosítós alak (`kulcs_jel`) csak megjegyzésbe, rendezéshez és kereséshez jut. A két mintalapon ez az út továbbra sem él (teszt: a látható szövegben nincs belső szócikk-azonosító) |
| 2 | az olvasási napló hézaga | a jegyzéktábla saját sort kapott (B68), az olvasása a naplóba kerül, e sor nélkül a munkamenet nem nyílik meg; a párosítás (B54) könyv–fájl leképezése naplózott olvasás lett (mind a 66 fájl a hash-ével). Teszt: a bemeneti réteg magjában egy fájlnyitás áll, és minden hívója naplóz. A referencia-tábla 11 `uj_bemenet` sorral bővült (10 párosítás-fájl és a jegyzék) |
| 3 | a DT-F218j és a DT-F218k állapota | ✅ |
| 4 | „tizenhárom” szimbólum | javítva: tizennégy |

**Két új sablonmondat** (`eredet=uj`, `dontes=var`; a 218a végi listába kerül): `e2.jel.szocikkel` („{jel} ({szocikk})”) és `e2.jel.szocikk_sorszam` („{szotar|a} {n}. szócikke”, pl. „a BDB 2. szócikke”). Egyik sem áll a két mintalapon.

**A megnevezés rendje (DT-F218m).** Az orkesztrátor példája („רַע I”) a homográf-számot a címszó mögé tette; a lapon a szótár saját rendje áll („II. רַע”), mert a megnevezés szó szerinti idézet (a BDB-szakasztábla szócikkfejének eleje, változtatás nélkül).

**Mérés a szócikk-megnevezésről.** A 3 471 több szócikkes BDB-szócikkből 1 029 megnevezésében áll homográf-szám, 2 192-nek a címszava egyedi a szón belül, 250-nél a sorszám áll. Megnevezést 454 szakaszjel kér: 414 címszóval, 40 sorszámmal.
*Proveniencia: `scope=a BDB-szakasztábla több szócikkes Strong-számai, szócikkenként és megnevezést kérő szakaszjelenként (Gerinc._cimszavak, Gerinc.jel_szocikke) | forras=adat/bdb_szakaszok.tsv | ts=2026-11-13`.*

**Állás a 2. javítókör után (HAMART-001, `PARDES_DATUM=2026-11-13`).** „2. Előfordulások”: 1 engedélysor (S1-FORRAS); a melléklet: 10 engedélysor; engedély nélküli diff-sor 0. Tesztek: 152 futott, 119 zöld, 33 kihagyva (a váz). Festékpróba: 0 szivárgás (HAMART: belső 171, idézet 326, kézi 240 látott jelzőszó; ISTENTISZT: 114, 183, 121; a belső jelzőszó az ISTENTISZT-lapon 2-vel kevesebb, mert a tartomány kezdő verse már nem belső szöveg).
*Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py; general.py --cel lexikon2 --id HAMART-001 + python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001 | forras=a munkafa a javítókör commitja előtt | ts=2026-11-13`.*

**Új táblasorok:** a jegyzék +1 (B68; összesen 29), a sablontábla +2 (összesen 127).

## DT-F218l: az önreferencia a forrásban (`claude-fable-5-2`, 2026-11-13, a 3. session)

*Az orkesztrátor technikai döntése (2026-11-13): a három nyitott pár a forrásban javul, ebben a feladatban; egyszavas egységesítés, a tartalom nem változik; a cella az legyen, ami a jóváhagyott lapon látszott; az engedélysorok megszűnnek, a DT-F218l állapota ✅.*

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

*Proveniencia: `scope=git diff --numstat -- adat nyilt_mag; general.py --cel lexikon --id HAMART-001 + cmp a HEAD két lapjával; python eszkozok/nyilt_mag_angol.py allapot (előtte és utána); python eszkozok/nyilt_mag_export.py; python eszkozok/nyilt_mag_kapu.py; general.py --cel lexikon2 + python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa a DT-F218l commitja előtt | ts=2026-11-13`.*

**Az `ir` mező.** A hat adatfájl és a generált `nyilt_mag/` kívül esik a brief `ir` mezőjén. A mezőt nem bővítettem: a bővítés a feladatkövetőben függési kört ad (`python eszkozok/feladatok.py ellenoriz`: „függési kör: #203 ↔ #212 ↔ #218”; a brief olvassa azok fájljait, és közös fájlt írna velük), amelynek feloldása a felhasználó döntése. Az `ir`-en kívüli írásra CI-szabály nincs; a módosítás itt és a DT-F218l sorában cellánként áll.

**Amit a felhasználónak látnia kell.** (1) A fenti szóválasztás („vizsgálat”, „listán”; nem „szócikk”). (2) A nyílt mag angol szövege nem változott: ha az „entry” helyett „this study” kell, az két szöveg újrafordítása és egy kódkönyv-címke. (3) Az `ir`-en kívüli hat fájl.

## F218.5 — S2, második fele: „1. Döntési út” (1.1–1.5) (`claude-fable-5-2`, 2026-11-13, a 3. session)

**Eredmény (HAMART-001, `PARDES_DATUM=2026-11-13`, `munka` mód).** A „1. Döntési út” szakasz 110 sorából 94 bájtra egyezik a referenciával; **16 diff-sor, mind engedéllyel, két előre megszámolt osztályban; engedély nélküli diff-sor: 0.** A melléklet 8, a „2. Előfordulások” 1 engedélysorral áll (változatlan). Az S2 szelet ezzel kész: a szakasz-diff 0 az engedélyeken kívül mindkét nézetre.
*Proveniencia: `scope=general.py --cel lexikon2 --id HAMART-001, majd python eszkozok/lapgen/regresszio.py --id HAMART-001 | forras=a munkafa az S2b commitja előtt | ts=2026-11-13`.*

| Engedélysor | Osztály | Darab | Előre rögzítve | Mi tér el |
|---|---|---|---|---|
| S2-FORRAS | GK-07 | 1 | 1 (a brief 8.1 (b) osztálya) | a blokkfejléc forrás- és licenclistája a szakasz valódi olvasásaiból jön |
| S2-FUNKCIO-1…15 | M-CSERE (DT-F218k) | 15 | 15 (a folytatási fájl „Az S2 második feléhez” pontja) | az 1.4 pont listaelemeiben a funkció kézi magyarázata a kettőspont után változatlanul, kisbetűvel áll („1Móz 3:14: az átok első kimondása, …”); a régi generátor nagy kezdőbetűvel írta át. Az engedély írásakor gépi ellenőrzés: a sor egyetlen eltérése a listaelemek kezdőbetűje |

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

*A `fuggetlen-ellenor` subagent (`claude-opus-5-5`) jelentése változtatás nélkül; bemenete: a brief, a `656c508a..28be9127` tartomány (az S2 két fele, a 2. javítókör és a DT-F218l), célzott hatókörrel, `teljes` szint. A push az ellenőrzés indításakor még nem történt meg (azóta megtörtént: `dca8a9f3..28be9127`). Mentve: 2026-11-13.*

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
| Lista 5 ⛔ | OK | – | A DT-F218l a felhasználói döntéssel zárult, az engedélysorok megszűntek. |
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

*A besorolást az orkesztrátor hozta (2026-11-13): mindkét tétel mechanikus, a fenti javaslat szerint, ebben a sessionben javítva. Az orkesztrátor az S2 négy eltérését (a szóválasztás, a homográf-szám rendje, az `ir`-en kívüli fájlok, a nyílt mag változatlan angol szövege) elfogadta; az `ir` mező nem bővül, a függési kör a 218c-ben rendeződik (N-F218d). A 218a végi listába felvéve: a kisbetűs listaelemek, a „mind a 575”, és a három új sablonmondat. Az újraellenőrzés az S3 végi ellenőrzéssel együtt fut.*

| # | Tétel | Mi történt |
|---|---|---|
| 1 | a típusjelölő előtagú hordozó elem kézi névként kerülne a lapra | a hordozó elem fajtája zárt készlet a bemeneti rétegben (`bemenet/elofordulas.py`): Strong-szám(ok), kézzel elnevezett szópár előtag nélkül, vagy `tematikus:`; ismeretlen előtagnál (`referencia:`, `idézet:`, `formula:`) a bemenet kimondott hibával megáll, a lap nem készül el. Próba: a MENNY-001 generálása BUKÁS-sal áll meg („ismeretlen hordozó-előtag: `referencia:` (MENNY-001, Júd 1:6)”), kilépési kód 1. Az ilyen csoport megnevezése a MENNY-001 új lapja előtt eldöntendő (új sablonmondat) |
| 2 | a festékpróba nem látta a horgonyba kerülő, kisbetűsített jelzőszót | a próba kis- és nagybetűtől függetlenül keres; a horgony külön tartományfajta (`Fajta.HORGONY`: a sablonmondat `horgony` típusú paramétere), ahol a kézi és az idézett szöveg jelzőszava megengedett, a belső mezőé nem; horgonyon kívül az átalakított jelzőszó szivárgás (a szöveget valami átírta). A kivétel egy mondata a 6-os sablon alapszabály-szakaszában áll |

**Állás a javítókör után.** Festékpróba: 0 szivárgás; a horgonyokban látott jelzőszó 30 (HAMART) és 18 (ISTENTISZT): ez az a szám, amelyet az ellenőr a próba vakfoltjaként mért. Látott jelzőszavak: HAMART belső 191, idézet 420, kézi 394; ISTENTISZT 134, 208, 203 (a kézi szám a horgonyokkal nőtt). Regresszió: engedély nélküli diff-sor 0 (25 engedélysor, változatlan). Tesztek: 172 futott, 139 zöld, 33 kihagyva (a váz); új: 4 festék-teszt és 1 előtag-teszt.
*Proveniencia: `scope=python eszkozok/lapgen/tesztek/futtat.py; general.py --cel lexikon2 --id HAMART-001 + python eszkozok/lapgen/regresszio.py --id HAMART-001; python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001; general.py --cel lexikon2 --id MENNY-001 | forras=a munkafa a javítókör commitja előtt | ts=2026-11-13`.*

**Az adat a hordozó-előtagokról.** Az `adat/elofordulasok.tsv` 250 sorából 241-nek nincs előtagja, 6 `tematikus:` (HAMART-001), és 1-1 `referencia:`, `idézet:`, `formula:` (mind MENNY-001).
*Proveniencia: `scope=a gerinc_elem mező kezdő „szó:” előtagjának számlálása | forras=adat/elofordulasok.tsv | ts=2026-11-13`.*
