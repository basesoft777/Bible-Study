# Specifikációs melléklet: a nulláról írt lapgenerátor (`lexikon_general.py` utódja)

*Alap: a main pillanatképe (63f3f126), a szeletenkénti térkép (lg_1 … lg_9000), a cáfoló ellenőrzés és a hiánykereső. Csak olvasás készült, a kód nem futott.*

**Jelölések a melléklet egészében:**
- **M1–M17**: a cáfoló ellenőrzés által megerősített kockázat. Csak ez számít hibának.
- **C**: cáfolt állítás.
- **H1–H13**: a hiánykereső lelete.
- **E**: a térkép állítja, de a cáfoló menetben nem szerepelt. Ahol a melléklet írója a forrást grep-pel megnézte, ott a sorszám ellenőrzött, az állítás súlya viszont még nincs mérve.

A cáfoló ellenőrzés bemenete a 18. tételnél (`BDB_ARAMI_ELSO`, 3284) megszakadt. Az lg_1300 … lg_9000 szeletek megerősítései nem érkeztek meg, csak a cáfolt tételek.

---

## 1. Összefoglaló

- **A régi generátor mérete.** `eszkozok/lexikon_general.py` 10 051 sor. Mellette kb. 20 segédmodul fut: `szerep_karoli`, `szerep_nave`, `szerep_kizart`, `olvasoi_kovetkeztetes`, `olvasoi_utofeldolg`, `tablajegyzet`, `kiejtes_szoveg`, `nyilt_mag_export`, `bdb_tagolas`, `bdb_rovidites`, `bdb_vj_szabaly`, `karoli_kh_szuro`, `lap_befagyasztas`, `ubs_hozzarendeles`, `lxx_os_import`, `heber_kiejtes`, `szotari_glossza`, `olvaso_szerver/bdb_szelet`, és a törzscikkhez a `torzscikk_general`.
- **Bemenetek.** A jegyzék (2. pont) 64 bemenetet sorol fel, ezek kb. 75 fájlt vagy táblát jelentenek.
- **Kockázatok.** 17 megerősített kockázat (mind az lg_1 szeletből), 29 cáfolt állítás, 13 hiánykereső-lelet. A többi szelet állításai cáfoló ellenőrzés nélkül maradtak (E).
- **Két szerkezet egy kódban.** Az `UJ_LAPSZERKEZET = {'HAMART-001'}` (7099) kb. 80 ágat vezérel. A három F212-kapu csak az új ágon fut (9999–10001). Az ISTENTISZT-001 a régi ágon generálódik, kapu nélkül.
- **Fő tanulság.** A hozzáférési pont ma nem kötelező: ugyanazt az adatot több út olvassa, eltérő szabállyal.
  - TAHOT: 3 út.
  - `BDB_teljes_unabridged`: 3 út.
  - `LXX_OS`: 3 út.
  - `glosszak_heber_hu`: 3 út.
  - TBESH-lemma: 2 út.
  - `lxx_dontesek`: 2 út.

  A lap utólagos szövegcserével javítja a saját kimenetét, és a forrásmegjelölés nem a ténylegesen olvasott fájlból jön. Az újraírás feltétele, hogy minden bemenet egyetlen ponton, kapuval lépjen be, és a kódban ne maradjon motívumazonosító.

---

## 2. Bemeneti jegyzék-tervezet

**Módok:** K = közvetlen fájlolvasás, P = hozzáférési ponton át, M = segédmodulon át. Sorszám mindig `lexikon_general.py`, ha nincs más jelölve.

| ID | Bemenet | Mit ad a lapnak | Helyes hozzáférési pont (új) | Régi olvasás | Kockázat |
|---|---|---|---|---|---|
| B01 | `adat/licencek.tsv` | minden forrás- és licencsor, Kolofon, Irodalom | `licencek()` az egyetlen licencforrás, minden licencmondat innen jön | 92 K; mellette kódba írt licencszövegek: 132, 462, 5770–5906, 9075, 9346 | H5, E |
| B02 | `adat/motivumok.tsv` | azonosító, negatív kritérium, lánc | motívum-sor egy ponton | 559 K; a lánc szabad szövegből regexszel (8893) | E |
| B03 | `adat/elofordulasok.tsv` | 2. szakasz, minden számítás | a motívum sorai egyszer, szűrve | a hívó adja (898); 1577 a teljes táblát olvassa (DBH-halmaz); 6571 újraolvas | E |
| B04 | `adat/jeloltek.tsv` | 1. Döntési út, 3. Kizárt, Minősítés, 8. „döntésre vár” | `jeloltek()` | 1097 K, 5690 K; versszám a `forras_kereses` szövegéből (`szerep_kizart.py:116–122`) | **M13** |
| B05 | `naplok/F123_teljesseg_<ID>.tsv` | 1.2 versszámai, melléklet | mérés a mai Strong-halmazon, vagy pillanatkép + kapu minden hálóra | 7370 K; hiányzó fájlnál `[]`; a kapu (7548) csak a `strong` hálót nézi | E (grep-pel látva) |
| B06 | `naplok/F123_teljesseg_<ID>_blokkok.tsv` | csoportos kizárás taglistája, melléklet | ugyanaz a mérés, kapuval | `nyilt_mag_export.py:837` M | H9 |
| B07 | `konkordancia/Karoli_1908.tsv` | 2.1 versszöveg, Döntési út példái, „van-e ilyen vers” | `L.load_karoli_1908` + `f22/versosszevonas.tsv` | 177 P; 4612 K (`karoli_versek`, összevonás nincs bekötve) | E |
| B08 | `konkordancia/TAHOT_kivonat.tsv` | kiejtés, `token_szam`, lánc, LXX-alapvonal | `L.load_tahot` + versösszevonás + explicit ismétlés-szabály | 247/296 P; 283 `max(k)`; 3262 P; 8675 K (oszlopnév szerint); 8812/8945 P | **M1**, E (8675) |
| B09 | `konkordancia/TAGNT_kivonat.tsv` | görög alak, kiejtés, ÚSZ-tábla szótöve | `L.load_tagnt` | 261 P; 9170 K (oszlopindex) | H3 |
| B10 | `TBESG.txt`, `TBESH.txt` | lemma, átírás, rövid angol glossza, 4.1 | `tbesg_tbesh_index` + `LEMMA_VALTOZAT` minden lapra | 317–344 K; 1829 K (`cols[6]`); 3095 megkerüli a `LEMMA_VALTOZAT`-ot; `kiejtes_szoveg.py:28–72` K | **M2**, H6 |
| B11 | `_nyers/tbesh/TBESH_konszolidalt.tsv` | 4.1 (kapcsolóval) | kivezetni, vagy verziózott táblába tenni | 1438 M, kapcsoló 1411 | E |
| B12 | `adat/kiejtes_szabalyok.tsv`, `kiejtes_kivetelek.tsv` | kiejtés | egy kiejtés-szolgáltatás | 356 M; `kiejtes_szoveg.py:29` K (második út) | H6 |
| B13 | `heber_kiejtes` (gépi szabály, DT-F131y) | héber kiejtés | ugyanez, jelölve | 284–285, 307, 863 M | **M4** (gépi szabály, nem régi bekötés) |
| B14 | `adat/forditasok.tsv` | minden magyar fordítás és glossza | `forditas_ehhez` + `allapot`-szűrő | 784–796 K; az `elavult` sort csak a 4314 szűri | **M5** |
| B15 | `adat/glosszak_heber_hu.tsv` | 4.1 rövid jelentés, Áttekintés, lánc-szó jelentése | egy glossza-pont | 1841 K, 3255 K, 8789 K (az angol `to X` egyezés szerint) | **M10** |
| B16 | `adat/szotar_szakasz_cimke.tsv` | 2. „Jelentés (a szó)”, 4.2 | P | 3231 | – |
| B17 | `adat/bdb_szakaszok.tsv` + `bdb_forras_javitas.tsv` | 4.2 BDB-kártya | `bdb_tagolas.szocikkek` + `bdb_rovidites` (zárójel- és betűjavítás minden lapra) | 3234 K → 4283 BT; a betűjavítás csak a HAMART-001-en (4548) | C (nyers olvasás), E (betűjavítás) |
| B18 | `adat/bdb_szakasz_hu.tsv` | 4.2 magyar szöveg | `hu_illeszt` + frissességi kapu (`kapu_elteresek`) betöltéskor | 3237 K; a kapu csak az `ellenoriz.py` 26. szabálya | **M6** |
| B19 | `adat/bdb_vers_jelentes.tsv` | 4.2 példahely, hivatkozásszám, törzs | `bdb_vj_szabaly.vj_feloldott` (közös a szerverrel) | 3240 K (két index, két szűrés); 8769 K | **M7** (alacsony) |
| B20 | `adat/thayer_szakaszok.tsv` + `thayer_forras_javitas` | 4.2 Thayer-kártya | `thayer_jelolt/thayer_bemenet.szakaszok(strong)` | 3248 K → 3919, 4305–4316, 4268 (nyers angol a lapon) | **M8** (N178) |
| B21 | `adat/thayer_vers_jelentes.tsv` | Thayer-példahely, „nem idézi” mondat (3665) | P + frissességi kapu a `bont.py` bemeneteire | 3251 K | **M9** |
| B22 | `konkordancia/BDB_teljes_unabridged.tsv` | `poz`-koordináta, helyi szócikk megléte, igei tő | egy pont, a `poz` és a TSV egy verzióhoz kötve | 3266 K; 8594 K (gyorsítótár nélkül); 9591 K (regex, betűjavítás nélkül) | **M11**, E, H4 |
| B23 | `konkordancia/BDB_etimologia_kezi_hatarok.tsv` | 4.8 nyelvi háttér | P | 2170 K | C |
| B24 | `konkordancia/BDB_rokon_irasok.tsv` | 4.8 rokon nyelvek | lekérdezés-eredmény tábla, dátummal | 8582 K (kommentsorból regexszel) | E |
| B25 | `adat/lexikon_hivatkozasok.tsv` | 2/b, 4.x forrásblokkok, licenc-gyűjtés | csak a szakasztáblás úton; licenc a ténylegesen megjelenő sorból | 1169 K; 1270–1271 licenc-mellékhatás; 1274–1281 nyers `szoveg_en` | **M12** |
| B26 | `konkordancia/LSJ_teljes.tsv` | 4.8 görög csonk | P | 1389 K (csonk-regex 1380) | E |
| B27 | `konkordancia/MCGED_teljes.tsv` | 4.5, 2/b | P | 1728 K | – |
| B28 | `SECE_G/H_teljes.tsv` | 4.7 | P | 1780 K (regex a szócikk szövegén) | E |
| B29 | `tW_szocikkek.tsv` | 4.3 | P | 2104 K | – |
| B30 | `OSHL_lexikalis_index.tsv` | TWOT-szám | P | 1158 K | – |
| B31 | SDBH/SDGNT domének + anomáliák | 4.4 | `L.load_*` | 1193, 1205 P | – |
| B32 | `UBS_DNTG_*` | 2. UBS-oszlop, 4.5, 4.9 | `ubs_hozzarendeles` | 771, 1711 M | – |
| B33 | `UBS_DBH_*` | ÓSZ UBS-cella, 4.5, 4.9 | `ubs_dbh_adatok` a motívum tokenjeire | 1582/1587 K; a token-halmaz az egész `elofordulasok.tsv`-ből (1577) | E |
| B34 | `Karoli_versmegfeleltetes.tsv` | DBH MT-vers | `karoli_mt_vers` | 1602 K | – |
| B35 | `konkordancia/LXX_OS/*.tsv` | 5. LXX, Dice-nevező, alapvonal-lemma, Nave KJV-kulcs | `lxx_os_import` egy ponton | 5020 K, 8441 K, 8647 K, `szerep_nave.py:72–89` K | E, H11 |
| B36 | `LXX_versszintu_parok.tsv` | 4.6, Áttekintés LXX-társ, alapvonal | P + frissességi kapu | 2206 K | E |
| B37 | `adat/lxx_dontesek.tsv` | 5. LXX eltérő / minusz | `lxx_dontesek_index`, egy szűrővel | 5151 P (szűrt), 5160 K (szűretlen) | E |
| B38 | `adat/visszhang_megfelelok.tsv` | 9. ÓSZ-tábla, 4.8 rokon nyelvek, 5. egyforrás-kapu | `visszhang_sorok` | 8598 K (hiányzó fájlnál `[]`), 5368 P | E |
| B39 | `adat/visszhang_tanuk.tsv` | 9. tanúréteg | P; hiányzó fájl = hiba | 9362 K, néma `[]` | H1 |
| B40 | `adat/vitatott_forrasok.tsv` | 10. vitatott pontok, 12. Irodalom | P | 9492 K, néma `[]` | H1 |
| B41 | `TAGNT_valtozatok.tsv`, `SBLGNT_apparatus.tsv` | 9. ÚSZ szövegváltozat | P | 9212–9213 K (regex a jegyzeten) | H1 |
| B42 | `konkordancia/Strong_szotar.tsv` | 9. ÚSZ szócsalád | `STRONG_SZOTAR_TSV` (69. sor), P | 9188 K (`c[4]` regex) | H2 |
| B43 | Károli-KH (nyers + MEK) | 6. Kereszthivatkozások, Minősítés | `karoli_kh_szuro.megerositett_sorok`; az elvetett-szám a szűrő nyilvános API-jából | 5498 P, de 5501 `KHS._nyers_sorok()`; a deklaráció nyers fájlnevet ad (5588, 5596, 6780) | E (grep-pel látva); C (a 315-ös állítás) |
| B44 | `TSK_kereszthivatkozasok.tsv` | 6., Minősítés | `L.load_tsk` + `tsk_kulcs` | 5481 P; a `Votes ≥ 15` kódban (5537, 6676) | E |
| B45 | `adat/kapcsolatok.tsv` | 7., Alátámasztás | P | 5611 | – |
| B46 | `adat/motivum_kapcsolatok.tsv` | 8. | P; hiányzó fájl = hiba | 5684 K, néma `[]` | E |
| B47 | `adat/res_forras.tsv` + kézi forrásfájlok | rések | P | 6420; 6443 K; 6983 K (mélységszűrő nélkül) | E |
| B48 | `adat/kiadasok.tsv`, `lap_atnezesek.tsv`, `lap_javitasok.tsv` | Kolofon | P | 5959, 6006, 6108 K (régi és új szűrő) | E |
| B49 | `naplok/KIADAS_<ID>_lektor.md` | Kolofon „Modell-lektor” sora | adattábla, nem napló | 6137 K (regex a napló szövegén) | E |
| B50 | `adat/kozel_keleti_hatar.tsv` | Kolofon hatókör | P | 6036 K | E |
| B51 | `DONTESEK.md` + `dontes_allapot` | olvasói dátum, érvényes döntés | `dontes_allapot` | 7937 K (regex); 7924 M | E; C (7924) |
| B52 | `adat/szotar_szerepek.tsv` | 4. váz, Jelmagyarázat | P | 2626, 7048, 8270 (a 8271 a „11”-et kézzel írja) | E |
| B53 | `adat/funkcio_kapcsolok.tsv` | gerinc, 4.13/4.14 | P, futásidőben | 3124, 4934 M (importkor kiértékelve) | E |
| B54 | `adat/karoli_strong/parok_<könyv>.tsv` | 4.13/4.14, kulcsszavak | P + bizonyossági szűrő | `szerep_karoli.py:201–223` K, néma üres | H10 |
| B55 | `adat/szoto/karoli_szotari_alak.tsv` | kulcsszavak | P | SZK; a deklaráció (2711) független a valódi olvasástól | E |
| B56 | `adat/elutasitasi_okok.tsv` | 3., Döntési út okai | SZKZ | M | C |
| B57 | `tematikus_temak.tsv`, `Nave_basokant.tsv`, `nave_tema_hu.tsv` | 4.12 Nave | SZN | 4965 M | E |
| B58 | `adat/tiltott_fordulatok.tsv` | 4.2 ⓘ | P | 3258 | – |
| B59 | `adat/lap_befagyasztas.tsv` | generálódik-e a lap | P, futásidőben | 9945 (importkor) | H13 |
| B60 | `lexikon/<ID>_TUDOMANYOS.md` (a meglévő lap) | régi ág: a markereken kívüli szöveg | **nem lehet bemenet** | 10004–10017 (`frissit_meglevo_fajlt`) | H7 (a 9988-as állapot-összevetés C) |
| B61 | `olvaso_szerver/bdb_szelet.py` | `_lapit` | közös számítási modul, jelölt függéssel | 3295 M (importlib) | E |
| B62 | `nyilt_mag_export` (`csoport_tagjai`, `szerkesztoi`) | csoport-taglista, „szerkesztői döntés” | bemeneti réteg, körkörös függés nélkül | 7400, 8146 | E |
| B63 | `konkordancia/Konyv_normalizalo_tabla.tsv` | könyvnév, ÚSZ-könyvlista | P; minden normalizálás innen | 3070 K, 7344 K (sorrendfüggő); `KH_KONYV_JAVIT` 153; `olvasoi_utofeldolg.py:42–63` `EXTRA_KONYV` | **M17**, H12 |
| B64 | `Targum_PD`, `Vulgata_Clementina`, `Glossa_Ordinaria` | Kolofon és Irodalom forrássora | csak a ténylegesen olvasott fájl | 9456–9479 (mindig deklarálva) | H5 |

**Illesztés az F217 jegyzékhez.** Az `adat/generalt_nezetek.tsv` sem a main pillanatképben, sem a git-történetben nem található. A sorok formáját ezért a feladatban megadott négy oszlopra (cél, parancs, bemenetek, kimenet) írom, és ezt a #217-tel egyeztetni kell. A „bemenetek” oszlop a fenti B-azonosítókra hivatkozik, a jegyzék gépi formája pedig ez a táblázat (azonosító → útvonal → hozzáférési pont).

| cél | parancs | bemenetek | kimenet |
|---|---|---|---|
| `lexikon_tudomanyos` | `python eszkozok/general.py --cel lexikon --id <ID>` | B01–B59, B61–B64 (B60 nem) | `lexikon/<ID>_TUDOMANYOS.md` |
| `lexikon_kizarasok` | ugyanaz | B03, B04, B05, B06, B07, B56, B62 | `lexikon/<ID>_KIZARASOK.md` |
| `lexikon_torzscikk` | `torzscikk_general` → a közös lapmodellből | a lapmodell (nem a TUDOMANYOS-fájl) | `lexikon/<ID>_TORZSCIKK.md` |

---

## 3. Lapszakasz → adatforrás → szabály → kapu

A sorrend az új szerkezeté (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md:558`). A „sablon” oszlopban a régi szerkezet sorai (108–329) a tartalmi szabályt adják.

| Lapszakasz | Adatforrás | Szabály (sablon:sor) | Mai kapu | Hiány |
|---|---|---|---|---|
| Cím + egyszerűsített kolofon | B02 | 558 (DT781) | `azonosito_tabla_beszur` ValueError, ha nincs `## Kivonat` (7298) | **nincs tartalmi kapu** |
| Kivonat (rés) | B47 | 108–113; `10_…_U3_proza_prompt_sablon.md` 1. pont | RÉS-marker párkapu (6475); hiányzó `res_forras` sor (6840) | – |
| Tartalomjegyzék | szakaszlista a kódban (612, 7106) | 115–118 | nincs | **a forrás kód, nem adat** |
| Jelmagyarázat | `JELMAGYARAZAT_TORZS` (702); B52 | 120–128 | `kesz_lap_elotte` ValueError (8280, 8283; szövegegyezés) | **a forrás kód**; a kapu szövegmintára épül |
| 1. Döntési út (1.1–1.5) | B04, B03, B05, B06, B56, B07, kézi nyitott kérdések | 558, 560, 562 | `teljesseg_kapu` (7548, csak a `strong` háló); `MellekletHiba` (7482); Jelmagyarázat-jelölő (7796) | **a `karoli`/`szotar` háló és a B06 kapu nélkül**; csak új ágon |
| Melléklet (`_KIZARASOK.md`) | B04, B06 | 558 (F3/B14) | `MellekletHiba` (7482) | B06 frissessége |
| 2. Előfordulások | B03, B07, B08/B09/B10/B13 (kiejtés), B16, B19, B21, B32–B34, B14 | 130–146, 311–313 | `GerincHiba` (3453, 3565, 3597); olvasói kapu; `ellenoriz.py` 40. | **tematikus ág a kódban** (M15, M16) |
| 2.1 Az igehelyek szövege | B07, B03 (`kapcsolodas`, `funkcio`) | 148–154; `9_…` 4. pont | `ellenoriz.py` 25. | – |
| 3. Kizárt és vizsgált helyek | B04, B02, B56 | 156–159 | üresség-mondat (1110) | **frissességi kapu nincs** (M13) |
| 4. Áttekintés | B03, B15/B14/B10, B36, B35 | 558 | `hely_egyseg_kapu` (2027; regex a lapszövegen) | `attekinto_beszur` némán kilép (8517) |
| 4.1–4.10 szótári pontok | B10, B11, B14, B15, B17–B33 | 161–178, 558 | `szerep_vaz` ValueError (2636); `GerincHiba`; `ellenoriz.py` 26. (külső) | **a Thayer-ág javított pont nélkül** (M8); B18 kapu csak külső |
| 4.6 LXX-híd | B35, B36, B37 | 558 | `lxx_egyezes_kapu` (1975; regex a lapszövegen) | két mérce (új 2253, régi 2265) |
| 4.8 + „Háttér: rokon nyelvek” | B23, B24, B22, B38 | 593 (6. pont) | olvasói kapu VISSZHANG V1–V3 | B22 nyers, betűjavítás nélkül (H4) |
| 4.11 mutató | – | 558, 580 (DT766, N-F193a) | – | **szabály nyitott: mutató vagy megszűnik** |
| 4.12 Nave | B57, B35 | 597 („a Nave-blokk nem üres”) | NAVE_ANGOL | – |
| 4.13/4.14 | B03 (`karoli_szo`), B54, B55, B53 | 315 (következtetés) | nincs | **bizonyossági szűrő nincs** (H10) |
| 2/b (opcionális rés) | B25 (MCGED) | 180–183; DT597 | `res_ures_e` (6544; szövegegyezés) | – |
| Miért fontos ez a lelet | kézi | 185–188 | RÉS-kapu | – |
| 5. LXX-fordítói döntések | B35, B37, B38, B08 | 190–202 | `lxx_egyezes_kapu`; `_lxx_ujraminosit` (5347, 5349); `lxx_egyforras_ellenoriz` (5434, csak új ágon) | B37 két szűrővel |
| 6. Kereszthivatkozások | B43, B44 | 204–209 | nincs | **a deklaráció nyers fájlt nevez** |
| Minősítés | B44, B43, B04, B03 | 211–214 | 6892 (render-sorrendfüggő `MINOSITES_STAT`) | – |
| 7. Kapcsolatok | B45 | 216–221 | nincs | – |
| Alátámasztás (adat-rés) | B45 | 223–229 | adat-rés renderelő (6503) | – |
| 8. Kapcsolódó motívumok | B46, B04 | 231–240 | 5/b beszúrás (5759) | B46 hiánya néma |
| 9. Hatástörténet (ÓSZ, ÚSZ, tanúk) | B38–B42, B08, B09, B35, B36 | 572–595 | olvasói kapu VISSZHANG; `teszt_hatastortenet.py`; a generátorban `hatastortenet_athelyez` némán kilép (9540) | **B39/B40 hiánya néma**; a szópár-szabály (DT-F194h) csak ágon |
| 10. Értelmezés + vitatott pontok szakirodalma | kézi forrás + B40 | 242–264, 579, 582 | RÉS-kapu | `szakirodalom_beszur` kapu nélkül |
| 11. Módszertan és nyitott kérdések | kézi | 286–301 | RÉS-kapu | – |
| 12. Irodalom és idézés | B01, gyűjtött fájl–licenc lista, B40 | 303–309 | nincs | **a lista nem a valódi olvasásból épül** (H5) |
| Kolofon | B01, B02, B47–B51 | 317–327 | `kolofon_forrasoszlop_kapu` (6209); `kotelezo_megjeloles` SystemExit (5919); `olvasoi_kapu.ell_kolofon` | a lektor-sor regexszel napló-szövegből (B49) |
| Kiejtés, Strong-szám a prózában | B10, B12, B13 | 311–315, 329 | olvasói kapu BELSO | két kiejtés-út (H6) |
| Regressziós kapuk | – | 597 | `ellenoriz.py` 37–40. | a három F212-kapu csak új ágon (H8) |

---

## 4. Megerősített hibák és régi bekötések

| # | Hiba | Fájl:sor | HAMART-001 | ISTENTISZT-001 |
|---|---|---|---|---|
| M1 | A TAHOT hallgatólagos „utolsó előfordulás” szabálya fájlsorrendfüggő. A Károli-vers kulcs az összevont 9 versnél két TAHOT-verset egyesít. | 247–254, 283 (`max(k)`), 296–304, 3262–3264 → 3548 | érinti, ha ugyanaz a Strong kétszer áll egy versben, vagy összevont versben; nem mérve | ugyanígy, nem mérve |
| M2 | A TBESG/TBESH alap-kulcsa az első előfordulást adja (`setdefault`). A `LEMMA_VALTOZAT` csak új ágon fut; a 3095 megkerüli. | 317–344, 340–342, 418–422, 3095, 9972–9977 | új ágon a változat-szabály fut; a 3095 érintheti | régi ág: a/b Strongnál az első előfordulás; nem ellenőrzött |
| M4 | A héber kiejtés gépi szabály (DT-F131y). Ez nem régi bekötés, de nem jóváhagyott adat. | 284–285, 307, 857–863 | igen (héber kulcsszavas sorok) | igen |
| M5 | A `forditas_ehhez` nem szűri az `elavult` fordítást (csak a 4314). A gyorsítótár folyamatonként egyszer töltődik. | 784–796 | igen (UBS/tW/BDB/TBESH/Thayer/Mounce/TBESG cellák); az elavult sorok száma nem mérve | igen, ugyanígy |
| M6 | A `bdb_szakasz_hu.tsv` generált pillanatkép. A generátor olvasáskor nem ellenőrzi a frissességét, a kapu csak az `ellenoriz.py` 26. szabálya. | 3237 → 4287–4290 | igen (`SZOTARI_GERINC` aktív) | igen (aktív) |
| M7 | A `bdb_vers_jelentes` két indexe eltérő szűrést kap, és nincs a tábla kód-hash-éhez kötve. A szabály közös a szerverrel, a kockázat alacsony. | 3240–3246 | igen (alacsony) | igen (alacsony) |
| M8 | A Thayer-szakasz nyersen jön: a `thayer_forras_javitas` / `thayer_bemenet` nincs bekötve. Fordítás nélkül nyers angol kerül a lapra. | 3248–3249 → 3919, 4305–4316, 4365, 4223–4231, 4268 | igen, ha van görög gerinc-token; nem ellenőrzött | ugyanígy |
| M9 | A `thayer_vers_jelentes` pillanatkép frissességi kapu nélkül. A „nem idézi” állapotmondat (3665) ebből jön. | 3251 → 3665, 3922, 4369 | igen, ha van G-token | igen, ha van G-token |
| M10 | A `glosszak_heber_hu` három párhuzamos közvetlen olvasással jön, eltérő hiány-viselkedéssel (1861 vs. 4855/4860). | 1841, 3255, 8789 | igen | igen |
| M11 | A `BDB_teljes_unabridged` `poz`-koordinátája nincs a TSV verziójához kötve (részben védi a `_bdb_poz_megbizhato`). | 3266, 3301–3303, 3354–3371, 3393–3416 | igen (alacsony) | igen (alacsony) |
| M12 | A `lexikon_hivatkozasok` nyers `szoveg_en` szövege a nem gerinces lapokra kerül, a licenc-gyűjtés minden lapon fut. | 1166–1170, 1270–1271, 1274–1281, 2378–2379 | a törzs nem; a licenc-mellékhatás lehetséges, nem ellenőrzött | ugyanígy |
| M13 | A csoportos kizárás versszáma a `forras_kereses` szövegéből jön, a mai Strong-halmazhoz nincs frissességi kapu. HAMART-on a `_blokkok.tsv` pillanatkép finomítja. | `szerep_kizart.py:116–122`; 1104–1118, 7395–7417, 7437, 7498, 7719 | igen (pillanatkép) | igen (nyers szám) |
| M14 | Motívumra szabott kapcsoló (`UJ_LAPSZERKEZET`): két szerkezet, kb. 80 ág. | 7099, 7102; használat pl. 644, 924, 1063, 1113, 9993, 10034; `ellenorzes/allitas_adat.py:98` | új ág | régi ág |
| M15 | `TEMATIKUS_SAJAT_SZO`: kézi felülírás motívum+igehely kulcson. A `str.replace` a 3690-es szövegre épül, és némán elbukhat. A 4. szakasz nem kap szócikket a G2652-re. | 871, 957–968, 3690 | igen (Jel 22:3) | nem |
| M16 | HAMART-001-re szabott tematikus cellaszövegek. | 942, 967, 975–976 | igen | nem |
| M17 | `KH_KONYV_JAVIT` kódba írt könyvrövidítés-javítás a normalizáló tábla helyett. | 153, 156–163 → 5546, 5549, 6684 | csak Eféz/Siral célhelynél; nem ellenőrzött | ugyanígy |

**4.b Ellenőrzendő tételek.** A forrásban grep-pel látható, de cáfoló ellenőrzés még nem futott rájuk, ezért nem számítanak hibának. A brief véglegesítése előtt egy ellenőrző kör kell.
- 5501 `KHS._nyers_sorok()`, valamint a nyers Károli-KH deklarációja (5588, 5596, 6780).
- 7370 `teljesseg_halok`, illetve 7548 (a kapu csak a `strong` hálót nézi).
- 9999–10001: a kapuk csak az új ágon futnak.
- 10004–10017: a régi lap a bemenet.
- 4548 `BDB_BETU_JAVIT` csak HAMART-on; az olvasó mindig alkalmazza.
- 3885 `KETRETEGU_BDB_KARTYA`.
- 5151/5160: a `lxx_dontesek` két szűrővel.
- 8441/8647 `LXX_OS` kétszer.
- 8594, 9591 `BDB_teljes` (nyers, betűjavítás nélkül).
- 8675 TAHOT közvetlenül.
- 9170 TAGNT oszlopindexszel.
- 9188 `Strong_szotar` (`c[4]`).
- 4612 `Karoli_1908` közvetlenül, összevonás nélkül.
- 1389 LSJ.
- A hiánykereső H1–H13 tételei.

**A cáfolt állítások egy sorban (29):** `bdb_szakaszok` nyers olvasása (3234, kétszer); a 942-es Kivonat-hivatkozás; a 998-as UBS-fedés mondata; `HEBER_NINCS_KIEJTES_JELZO`; `BDB_etimologia_kezi_hatarok`; TBESH forrás-jelző; `TW_SZOVEG_JEL`; DBH-fordítás (3725); `bdb_vers_jelentes` „két párhuzamos szűrés” (3240); TAHOT-normalizálás (3262); `HORGONNYAL_JELOLES`; `_HIV_TOK`; az Összesítés-mondat belső kulcsa; 2/b `szoveg_en` (6766); `elutasitasi_okok` mintaszótár; `ervenyes_dontes` (7924); `OLVASOI_FORRASNEV` (kétszer); `UJ_OLVASOI_MUNKASZO` regex-csere; a meglévő lap 9988-as olvasása; `KIZARASOK_UTOTAG` / fejléc-konvenció; Károli-KH hozzáférési pont (315); `utvonalak` / TBESH-konszolidált; `utvonalak._UZENET` commit-hash; `ellenoriz._teljes_szocikk`; `ellenoriz.szakasz_cimke_hibak`; `kovetelmeny_kapu`; `KOLOFON_KOTELEZO` / `NEM_URES`; `forditas_ubs` 20-as szám és `main_agon`.

---

## 5. Rögzített számok, állapotmondatok, motívum-specifikus ágak

Az új generátorban ezek adatból (A) vagy egy verziózott konfigurációs táblából (K) jönnek. A kódban motívumazonosító, licencszöveg és szakaszszám nem állhat.

| Csoport | Elem | Hely | Új forrás |
|---|---|---|---|
| Motívumkapcsoló | `UJ_LAPSZERKEZET`, `KETRETEGU_BDB_KARTYA`, `BDB_BETU_JAVIT` (mind `{'HAMART-001'}`) | 7099, 3885, 4548 | megszűnik, egy szerkezet (l. 8. pont) |
| Motívum+igehely felülírás | `TEMATIKUS_SAJAT_SZO` | 871 | A: az `elofordulasok.tsv` sora vagy egy kézi felülíró tábla, döntéssel |
| Motívumkapcsoló adatból | `GERINC_KIVETEL_MOTIVUMOK`, `SZEREP_KAROLI_MOTIVUMOK`, `BEFAGYASZTOTT` | 3124, 4934, 9945 | A (marad), de futásidőben olvasva |
| Token-kivétel | `SZEREP_TOKEN_MUTATO` (H7121 → BDB 2.c) | 2403 | A |
| Küszöb | TSK `Votes ≥ 15` (kódban és szövegben) | 5537, 6676, 8000 | K, a szöveg a K-értékből |
| Küszöb | `ALAPVONAL_SZOKASOS` 0.80, `ALAPVONAL_RITKA` 0.40; `LXX_TARS_KUSZOB` 0.05 (a görög ágon literál, 8495) | 8567–8568, 8469 | K, egy helyen |
| Küszöb | `KAROLI_MIN_HELY` 3, `KAROLI_ALLANDO` 0.67, `OLVASOI_13_KUSZOB` | 2882–2883, 2845 | K |
| Küszöb | `LXX_PAROK_TOP` 10, `NEVELO_MONDAT_SZO` 6, `_elso_tagmondat` 90, példák `[:4]` / `[:5]` | 2093, 8350, 3819, 2494, 7721 | K |
| Szűrő-halmaz | `LXX_DONTES_MEGJELENO_BIZONYOSSAG/TIPUS` | 5043–5044 | K |
| Adathalmaz-konstans | `BDB_ARAMI_ELSO = 9264` | 3284 | A (a BDB-adat README-jéből vagy táblából) |
| Állapotmondat | `SECE_LABJEGYZET` („magyar rövid glossza-tábla a görögre még nincs”, ellentmond az 1864-nek) | 1920 | az adatállapotból számolva |
| Állapotmondat | `PESHITTA_MONDAT`, `CHAIN_LINEAGE_LICENC_OLVASOI`, Targum-fedés (`NINCS_TARGUM`), közel-keleti hatókör, Hays-bekezdés | 9143, 9453, 8891, 6083, 6070 | A (forrás-állapot tábla / `licencek.tsv`) |
| Állapotmondat | „fordításra vár” bevezetők, „bekötés később”, „adatosítva, nincs bekötve”, `HORGONNYAL_JELOLES` | 1683, 2326, 2607 | az adat állapotából |
| Licenc/forrás a kódban | `MOUNCE_MEGJELOLES`, `lsj_forrasmegjeloles`, `TW_/TWOT_MEGJELOLES`, `OLVASOI_SABLON` licencnevek, `FAJL_TELJES_NEV`, `ADATFORRAS_FAJLOK`, `KOLOFON_BEMENETEK`, `ADAT_RES_FORRASAI`, 4.11/9. lábjegyzet-licencek | 132, 138, 462, 5770–5906, 6202, 6776, 9075, 9346 | A: `licencek.tsv`; a forráslista a bemeneti réteg olvasási naplójából |
| Személy, kiadás | `SZERZO_NEV`, `LEXIKON_CIM_HU`, `KANONIKUS_ALAP_URL`, `NYILT_MAG_DOI`, `KAROLI_STRONG_DOI` | 677–692 | K (a felhasználó szerint nem végleges) |
| Szakaszszám a szövegben | `SZAKASZOK`/`UJ_SZAKASZOK`, `UJ_CIMCSERE`, `KOLOFON_SZAKASZNEV`, „9. szakasz”, „4.11–4.14”, `#1-előfordulások`, `#5-lxx-…`, „2. szerep” | 612, 7106, 6163, 5402, 8271, 4817, 4735 | a szakaszmodellből generált horgony |
| Döntésszám a lapon | DT379, #142, DT382, DT-F123h, G5, G10, `LXX_OS`, `szamozas_elteres` | 4486, 3503, 1025, 5424, 5443 | nem állhat a lapon; nyers sor HTML-megjegyzésben |
| Szövegmintára épülő kapu vagy csere | `_LXX_OSSZESITES_RX`, `_HELY_14/ATT_RX`, `_TELJ_TORZS_RX`, `UJ_SZOVEGCSERE`, `UJ_JELMAGYARAZAT_CSERE`, `_lxx_ujraminosit` `replace`, `SZERKEZETI_HELYORZOK`, `ALATAMASZTAS_NINCS_KAPCSOLAT`, `BDB_FEJ_NYERS_RX` | 1969, 2011, 7545, 7106, 8277, 5296, 6534, 6566, 8318 | a kapu a lapmodell számain fut, nem a renderelt szövegen |
| Heurisztika | görög tő (3 betű + előtaglista), latin szócsalád (5 betű), BDB-tő képzőlevágás, `ROKON_NYELVEK`, `TORZS_MAGYAR`, `KISBETU_TULAJDONNEV`, `IGAZOLAS_OLVASOI`, `_HALO_OLVASOI` | 5316, 9152, 9615, 8569, 8120, 8073 | K (szabálytábla), teszttel |
| Globális állapot | `LEMMA_VALTOZAT`, `KIEJTES_HIANY`, `KIEJTES_JELOLT_HIANY`, `MINOSITES_STAT`, `KERESZT_OSSZES`, `_kh_elvetett`, kb. 15 folyamat-szintű gyorsítótár | 396–433, 6690, 5498 | megszűnik; a számítás tiszta függvény |
| Holt kód | második `n == 7 and uj` ág (2540), Alátámasztás `else` (6619), `_gerinc_bdb_fej_mutato` (4689, nem bekötött) | – | nem portolandó |

---

## 6. Követelménylista az újraíráshoz

### 6.1 N-F212a (a hibaleltár CS3-maradéka, `NYITOTT_FELADATOK.md:968`)

A pillanatképben csak a tételek rövid címe áll. A teljes leírás a 2026-11-11-i hibaleltárban van, ezért a cím nélküli tételek teljesülési feltétele az újramérés.

| ID | Tétel | Mérhető teljesülés |
|---|---|---|
| GK-A1 | Másolt Károli-KH lista, kihagyó lista | A versenként nem vizsgálható helyek listája egyszer áll a lapon: minden igehely legfeljebb egyszer szerepel a 6. szakaszban és a hatókör-jegyzetben együtt. A lista az adatból jön, nem szövegmásolatból. |
| GK-A6 | Rokon nyelvi tábla: „a kinyerés még nem történt meg” | A mondat pontosan azoknál a lánc-szavaknál áll, amelyeknek nincs `bdb` soruk a B38-ban (gépi lista-összevetés: 0 eltérés). |
| GK-A10 | Csupasz Strong-szám a Szócikkek-bevezetőben | A lapon 0 csupasz, zárójeles Strong-szám (sablon 329; olvasói kapu BELSO = 0 BUKÁS). |
| GK-A11 | (leírás a hibaleltárban) | Újramérve az új generátoron, naplózva, 0 eltérés. |
| GK-A12 | 8 nem létező Károli-vers a BDB-szövegből | BDB-hivatkozásból képzett igehely csak akkor link, ha a vers a B07-ben létezik (a versösszevonással együtt). A 8 eset tesztesetként: 0 nem létező versre mutató link. |
| GK-A13 | A cím frissítése meglévő fájlnál | Ha a `motivumok.tsv` címe megváltozik, újrageneráláskor a lap címe az új. A meglévő lap nem bemenet (GK-12). |
| GK-A14, GK-A15 | (leírás a hibaleltárban) | Újramérve, naplózva, 0 eltérés. |
| GK-B5, GK-B8 | (leírás a hibaleltárban) | Újramérve, naplózva, 0 eltérés. |
| GK-B9 | A `ts=` nem determinisztikus | Két egymás utáni futás azonos bemenettel bájtra azonos kimenetet ad. A `ts` a bemenetek hash-éből vagy explicit paraméterből jön. |
| GK-C3, GK-C9, GK-D3 | (leírás a hibaleltárban) | Újramérve, naplózva, 0 eltérés. |

### 6.2 N-F215a (a mainen N178)

| ID | Tétel | Mérhető teljesülés |
|---|---|---|
| GK-N178 | A Thayer-szöveg a javított forrásból jöjjön (M8). | A 4.2 Thayer-kártya szakaszai és útvonalai a `thayer_jelolt/thayer_bemenet.szakaszok(strong)` kimenetéből jönnek. A 15 érintett Strongon (G0260, G0575, G0846, G1100, G1909, G2675, G3536, G3563, G4151, G4404–G4407, G5132, G5567) a lapra kerülő angol szöveg = a javított szöveg (teszt). Kódban 0 közvetlen `thayer_szakaszok.tsv`/`Thayer_teljes.tsv` olvasás a bemeneti rétegen kívül. Megjegyzés: az N178 `:3021`-es sorhivatkozása elavult; a mai nyers út a 3248. sor. |

### 6.3 DT-F194h (szópár)

A tétel az `istentiszt-uj-cikk-992f57` ágon van (F194.22, commit 7043c4ab), a main pillanatképben nincs. Portolni kell.

| ID | Mérhető teljesülés |
|---|---|
| GK-SZOPAR | Tisztán szópáros motívumon (van `H…+H…` gerinc-elem, és nincs egyes szavas héber) a következők teljesülnek: (1) a 9. szakasz ÓSZ-táblája nem üres; (2) a lánc-szó a formula igéje (a pár első tagja); (3) a láncversek a motívum beépített ÓSZ-versei, Peshat-mag nélkül, a mai adatból; (4) a tábla alatti mondat kimondja, hogy a táblázat a formula igéjét követi; (5) az ellenőrzött, alak nélküli LXX-sor „nincs megfelelő szó”; (6) a `lxx_egyezes_kapu` a `szopar_motivum`-ot használja; (7) a HAMART-001 kimenete bájtra változatlan; (8) a `teszt_f194_szopar.py` `SzoparLanc` zöld. |

### 6.4 Kiegészítő követelmények

| ID | Követelmény | Mérhető teljesülés |
|---|---|---|
| GK-01 | Egy adat, egy hozzáférési pont. | Statikus teszt: `konkordancia/` vagy `adat/` útvonalat csak a bemeneti réteg nyit meg (0 találat máshol). Minden olvasás a jegyzék (2. pont) egy B-azonosítójához kötött. |
| GK-02 | A javított változat kötelező. | B17, B18, B20, B43 csak a javított ponton érhető el. A nyers függvény (`_nyers_sorok`, nyers TSV) a bemeneti rétegen kívül nem hívható (teszt). |
| GK-03 | Pillanatkép csak kapuval lehet bemenet. | B05, B06, B18, B21, B36, B38, B49 minden betöltésnél frissességi kaput futtat (hash vagy a mai Strong-halmaz). Eltérésnél BUKÁS, a lap nem íródik ki. |
| GK-04 | Kapu minden lapon. | `lxx_egyezes`, `hely_egyseg`, `teljesseg` és a melléklet-kapu minden generált lapon fut. Nincs „régi ág” kapu nélkül. |
| GK-05 | Nincs motívumazonosító a kódban. | `grep -E '[A-Z]+-[0-9]{3}'` a generátor kódján 0 találat (tesztek és dokumentáció kivételével). |
| GK-06 | Nincs néma hiány. | Hiányzó kötelező bemenet → BUKÁS. Opcionális bemenet hiánya kimondott hiánymondat az adatállapotból (CLAUDE.md 3. szabály). B39, B40, B46, B35 slug, B59 most néma. |
| GK-07 | A forrásmegjelölés a valódi olvasásból jön. | A Kolofon, a 12. Irodalom és a blokkfejlécek forráslistája = a bemeneti réteg olvasási naplója (halmaz-egyenlőség teszttel). A licencszöveg csak a B01-ből jön. |
| GK-08 | Nincs utólagos szövegcsere. | A `kesz_lap_elotte`, `olvasoi_atiras`, `UJ_SZOVEGCSERE`, `UJ_JELMAGYARAZAT_CSERE`, `_lxx_ujraminosit replace`, `kesz_lap_utana`, `nevelo_le`, `OU.alkalmaz` funkciója a megjelenítő sablonba kerül. 0 olyan lépés, amely renderelt Markdownt regexszel átír. |
| GK-09 | Kapu a modellen, nem a szövegen. | A számegyezés-kapuk a lapmodell számait vetik össze, nem regexszel olvasott lapszöveget. |
| GK-10 | Szakaszszám és horgony a modellből. | Minden „N. szakasz”, „4.x pont”, `#horgony` a szakaszmodellből generált. A szakaszrend módosítása után 0 hibás belső link (linkellenőrző teszt). |
| GK-11 | Nincs globális állapot. | Két motívum generálása fordított sorrendben bájtra azonos kimenetet ad. |
| GK-12 | A generált fájl nem bemenet. | A lap mindig nulláról épül a forrásból és az adatból (a régi `frissit_meglevo_fajlt` út megszűnik). |
| GK-13 | Egy kiejtési út. | A kiejtés (lemma, ragozott, gépi) egy szolgáltatásból jön, a `LEMMA_VALTOZAT`-tal minden lapon. A `kiejtes_szoveg` pótlás ugyanazt a szolgáltatást hívja. Tesztelt eset: H2403a/b. |
| GK-14 | TAHOT-ismétlődés explicit szabállyal (M1). | (vers, Strong) ismétlődésnél a választás szabálya nevesített és tesztelt. Az összevont 9 versnél a kulcs a versösszevonás szerint. |
| GK-15 | Fordítás-állapot (M5). | Az `elavult` állapotú fordítás nem kerül a lapra: helyette angol + „fordításra vár” (vagy a 8. pont szerinti döntés). Teszt egy elavult sorral. |
| GK-16 | Egy glossza-út (M10). | A héber rövid jelentés egy függvényből jön. A hiány egyféle mondatot ad. |
| GK-17 | Könyvnév-normalizálás egy táblából (M17, H12). | `KH_KONYV_JAVIT` és `EXTRA_KONYV` megszűnik, a B63 bővül. 0 kódba írt könyvnév-alias. |
| GK-18 | BDB-betűjavítás minden lapon. | A generátor és az olvasó ugyanazt a javított BDB-szöveget adja (a 4548-as halmaz megszűnik). |
| GK-19 | Károli–Strong párosítás bizonyossággal (H10). | A 4.13/4.14 csak a döntött bizonyossági szint feletti párosítást használja; hiányzó könyvfájl = kimondott hiány. |
| GK-20 | A törzscikk a lapmodellből készül (H11). | A `TORZSCIKK` nem olvassa vissza a `TUDOMANYOS.md`-t. Befagyasztott motívum törzscikke sem generálódik elavult lapból. |
| GK-21 | A HAMART-001 regressziós kapui. | Sablon 597: 0 BUKÁS az olvasói kapun kivétel nélkül; a Döntési út számai összeadódnak; döntés nélküli vers 0; Nave-blokk nem üres; `ellenoriz.py` 37–40. zöld. |
| GK-22 | Az olvasó és a lap számai egyeznek. | Az olvasó-szerver blokkjai és a Markdown ugyanabból a lapmodellből számolnak (7. pont); egy motívumon a két kimenet számai gépi összevetésben azonosak. |

---

## 7. Javasolt felépítés

**Rétegek.** Mindegyik külön csomag, egyirányú függéssel.

1. **`bemenet/`** (az egyetlen hely, amely fájlt nyit)
   - Jegyzékvezérelt: a 2. pont B-azonosítóinak gépi alakja. B-azonosítónként egy függvény.
   - Minden függvény betöltéskor kaput futtat: létezés, fejléc/oszlopnév, a javítótábla alkalmazva, frissesség (hash vagy a mai Strong-halmaz).
   - Kimenete immutábilis adat. Az olvasási napló (B-azonosító, útvonal, hash) a forrásmegjelölés alapja (GK-07).
   - A nyers forrás csak a javító modulon belül érhető el.
2. **`konfig/`**: a küszöbök, szűrő-halmazok, heurisztika-táblák, a kiadási azonosítók (5. pont, K), egy verziózott táblában.
3. **`szamitas/`**: tiszta függvények, motívumazonosító-ág nélkül. Kimenetük a **lapmodell**: szakaszonként a számok, a sorok, a kimondott hiányok és a következtetés-kód (`olvasoi_kovetkeztetes` szabályai). Modulok:
   - előfordulás, kizárás / Döntési út, szótári pontok (gerinc, BDB/Thayer kártya), LXX, kereszthivatkozás, kapcsolat, Hatástörténet (benne a `szopar_motivum`), kolofon.
   - A gépi kapuk (GK-04, GK-09) ezen a rétegen futnak, a modellen.
4. **`megjelenites/md`**: a lapmodellből a `TUDOMANYOS.md`, `KIZARASOK.md` és `TORZSCIKK.md`, sablonokból. Az olvasói szöveg (forrásnév, névelő, táblajegyzet, „szerkesztői döntés”) itt keletkezik, utólagos csere nélkül. Utána az olvasói kapu fut a kész szövegen, csak ellenőrzésre.
5. **`megjelenites/olvaso`**: az olvasó-szerver blokkjai ugyanazt a lapmodellt (vagy a `szamitas/` függvényeit) használják. A ma közös `bdb_vj_szabaly` mintájára minden szabály egy helyen él („egy számítás, két megjelenítés”).

**Regressziós feltétel.**
- A **HAMART-001** új kimenete bájtra egyezik a mai main kimenetével (`general.py --cel lexikon --kimenet <ideiglenes könyvtár a repón kívül>`), kivéve a felsorolt szándékos eltéréseket. Ezeket egy eltérés-engedélyező fájl rögzíti, okkal és követelmény-azonosítóval. Minden más diff BUKÁS.
- Szándékos eltérések:
  - (a) a `ts=` determinisztikus (GK-B9);
  - (b) a Kolofon, a 12. Irodalom és a blokkfejlécek forrásneve a valóban olvasott javított forrást nevezi (Károli-KH, Thayer; GK-07);
  - (c) a Thayer-szöveg a javított forrásból, ha a lap a 15 Strong valamelyikét érinti (GK-N178; előtte mérni);
  - (d) az elavult fordítás szűrése, ha érinti (GK-15);
  - (e) az N-F212a tételek javításai (6.1).
- Az **ISTENTISZT-001** referenciája nyitott (8. pont, T1): a mainen régi szerkezetű, kapu nélküli lap áll, az F194 ágon új szerkezetű, DT-F194h-val. A bájt-egyezés csak az utóbbihoz értelmes.

---

## 8. Nyitott kérdések

### Tartalmi kérdések (a felhasználó dönt)

- **T1.** Mi az ISTENTISZT-001 regressziós referenciája: a mai main régi szerkezetű lapja, vagy az F194 ág új szerkezetű lapja a merge után?
- **T2.** Megszűnik-e a régi szerkezet (minden lap az új szerkezettel generálódik), vagy a nem migrált és a befagyasztott lapoknál megmarad? A sablon (556) szerint a többi lap motívumonként, a teljes folyamaton át követ. A generátor viszont egy szerkezetet kellene tartson (GK-05).
- **T3.** A `TEMATIKUS_SAJAT_SZO` (Jel 22:3 → G2652) adatba kerül-e (az `elofordulasok.tsv` `strong` mezőjébe vagy kézi felülíró táblába), és kapjon-e a 4. szakasz szócikket erre a szóra?
- **T4.** A TAHOT-ismétlődésnél (M1) az utolsó vagy az első előfordulás kiejtése álljon? A választás a kimenetet változtatja.
- **T5.** Elavult fordításnál angol szöveg + „fordításra vár” álljon-e, vagy a régi magyar szöveg jelölve (M5)?
- **T6.** Kell-e bizonyossági küszöb a Károli–Strong párosításra (H10) a 4.13/4.14 következtetéseihez, és mekkora?
- **T7.** A kódban álló állapotmondatok (Peshitta, Chain Lineage licence, közel-keleti hatókör, Hays-bekezdés, Targum-fedés) szövege marad-e, amikor adattáblába költözik?
- **T8.** A szerző neve, a lexikon címe, a kanonikus URL és a DOI-k konfigurációba kerülnek. Ezek értéke a felhasználó döntése; a memória szerint nem véglegesek.

### Technikai kérdések (az orkesztrátor dönt)

- **O1.** A cáfoló ellenőrzés bemenete csonka. Kell egy ellenőrző kör az E-tételekre és a H1–H13-ra a brief véglegesítése előtt (egy ellenőrzés, legfeljebb egy javítókör).
- **O2.** Az `adat/generalt_nezetek.tsv` (F217) sem a mainen, sem a git-történetben nincs. Egyeztetni kell az oszlopformátumot és a B-azonosítók gépi alakját.
- **O3.** A 4.11 helye: egysoros mutató, vagy a pont megszűnik (DT766, N-F193a: „a generátor döntése”)?
- **O4.** A `fordit.py`/`emeles.py` régi egész-szócikkes út él-e, vagy archívumba megy (N178)?
- **O5.** Az olvasó-szerver közös rétege: a szerver a `szamitas/` csomagot importálja, vagy egy generált lapmodell-JSON-t olvas? Ide tartozik a `bdb_szelet.py` szerverfüggés (B61) és a `nyilt_mag_export` körkörös függése (B62) is.
- **O6.** Az `ellenoriz.py` és az `olvasoi_kapu.py` lapszövegre kereső szabályait (pl. 35. szabály, `NYILT_ADAT_MUTATO`, `KOLOFON_KOTELEZO`) a generátorral egy körben kell átírni. Sorrend és ág-terv kell, mert közös fájlokat érint.
- **O7.** A `TBESH_konszolidalt` (B11, `.gitignore`-olt) kivezetése vagy verziózása.
- **O8.** A holt kód (2540, 6619, 4689) nem portolandó. Kell-e ezt külön mérni a HAMART-001 diffjén?