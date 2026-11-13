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
