# F102 — a BDB-szeletelő javítása (napló)

*FELADATOK #102 · brief: `F102_BDB_SZELETELO_JAVITAS_BRIEF.md` · ág: `claude/f102-bdb-szeleto-javitas` · modell: claude-opus-5-5
(a brief `modell: opus` mezőjével egyezik) · indulás: 2026-11-09.*

## 0. Egyeztetett eltérés (az orkesztrátor döntése, 2026-11-09)

A brief 1c. szakaszának **szűkített** hatóköre érvényes, nem a 2. Hatókör teljes listája. A #102-nek marad: (a) az igehely → szakasz
hozzárendelés a szakasztáblán (`adat/bdb_szakaszok.tsv`, 2.30), előbb mérve; (b) öröklés (M092); (c) sigla-szűrés (H2623, H4912, a hét
`sigla_igazolt`, M223-típus); (d) M130 (magányos „II.”); (e) a korpusz-eltérés osztályozása; (f) DT382 (B) javaslatként; (g) a H1004 hamis
folytatás, regressziós teszttel; (h) új vak mérés (⛔ 3.5). A HAMART-001 két esete (H2403, H7451): csak rétegmérés, javítás csak az `ir`-ben.

## 1. Kiinduló állapot (a main-en, `b92d4dc5`; az ág első commitja csak a brief fejléce)

| mérés | eredmény | proveniencia |
|---|---|---|
| a 2.29 újragenerálása `--ts 2026-10-28 --ellenoriz` | **ELTÉR** — a törzs bájtra azonos (162 054 sor, 0 mezőeltérés); csak a `# forras:` sor `bdb_forras_javitas.tsv@` hash-e avult el (f7217021b034 → 834be5c1ee6e: a 2.31 azóta `heber_sorrend`, `atiras`, `zarojel` sorokat kapott, amelyeket a 2.29 nem olvas). A `teszt_bdb_vers_jelentes` `test_bajtra_azonos` ezért a main-en piros volt; az ág első újragenerálása rendbe teszi | scope=adat/bdb_vers_jelentes.tsv | forras=bdb_vers_jelentes.py --ellenoriz + eseti diff (sor kulcs: strong+poz+nyers) | ts=2026-11-09 |
| seed-101, a mai táblával (`m2_minta_osszevet.py --mai-tabla`) | véletlen 200: könyv/vers 197, jelentéspont **184** (92,0%), előtagként 185; szűrés: véletlen 197/200, szűrt 22/25, bizonytalan 13/25 | scope=seed-101 (naplok/BDB_SZELETELO_M2_minta_seed101_kulcs.tsv + kitoltott_A/B) | forras=eszkozok/olvaso_szerver/m2_minta_osszevet.py --mai-tabla | ts=2026-11-09 |
| aranyminta (`bdb_szelet_m0.py --arany`) | 32 szócikk; hibás szócikk EN 7, HU 23; szerkezeti eltérés EN 52, HU 220; cím-eltérés 0 | scope=adat/bdb_aranyminta.tsv | forras=eszkozok/olvaso_pilot/bdb_szelet_m0.py --arany | ts=2026-11-09 |
| szakasztábla (`szerkezet_osszevet.py --arany --seed101 --korpusz`) | arany 411/425 (96,7%), `forras_hiba` nélkül 411/416; seed-101 9/13 (9/10); korpusz 137 885 / 161 242 egyezik (85,5%): `jelentes_elter` 6 486, `csak_resz` 4 686, `torzs_elter` 3 978, `alpont_elter` 2 627, `szeletelo_fej_tabla_tagolt` 2 415, `nem_talalt` 1 779, `tabla_fej_szeletelo_tagolt` 1 386 | scope=adat/bdb_szakaszok.tsv × adat/bdb_vers_jelentes.tsv | forras=eszkozok/bdb_jelolt/szerkezet_osszevet.py --arany --seed101 --korpusz | ts=2026-11-09 |

Megjegyzés az aranyminta számaihoz: a brief 4. pontja „EN 7/32, HU 4/14; 71/72”-t ír; a mai futás HU-része 32 szócikkre fut (a magyar
oldal azóta bővült), ezért a mérce az **előtte/utána azonos szkripttel** mért szám, nem a brief régi HU-száma.

## 2. (a) A szakasztábla mint a jelentéspont forrása — mérés az átállás előtt

**Mit olvas ma a kinyerő:** a `bdb_vers_jelentes.py` a `BDB_teljes_unabridged.tsv` sima szövegét és a `bdb_szelet.py` szeletelőjét
(`szeletel`, `csomopont_savok`, `szakasz_savok`, `jelentespont`); a 2.30 szakasztáblát **nem** olvassa. Az átállás tehát nem történt meg.
(A lexikongenerátor a 2.29 útvonalát a 2.30-hoz illeszti: `lexikon_general.py` `gerinc_utvonal_vag`, `bdb_vers_szocikk`, `_bdb_sor_utvonal`.)

**Próba (eseti szkript, a repón kívül):** a 2.29 minden sorához a 2.30 sora a `szerkezet_osszevet.py --korpusz` kurzoros keresésével
(a `nyers` a Strong tábla-szövegében, sorrendben); az útvonal a 2.29 alakjára hozva (`.A` és a zárójeles szint elhagyva, három szint,
`cim`/`fej` → `fej`, tagolatlan Strongnál `tagolatlan`); a seed-101 kulcsában csak az `utvonal` cserélve (a `szakasz`/`resz` a 2.29-é:
a 2.30 homonima-száma a címsorban áll, a `szakasz`/`resz` oszlopai más szemantikájúak — H3063: a tábla `szakasz` I/II, a vak lap `resz` I).
Hozzárendelés: 159 991 sor; a seed-101 kulcsában 4 sor nem rendelhető (kurzor-csúszás, pl. M238).

| | jelentéspont (véletlen 200) | hibás helyek |
|---|---:|---|
| mai szeletelő | **184** | M028, M043, M140, M146, M236, M243, M238 (szeletelő-hiba); M102, M117, M162 (`forras_hiba`); M130, M203 (fő tagolás); M008, M011, M029, M031 (formátum / kulcs-ellentmondás) |
| szakasztábla útvonala | **184** | megszűnik: M028, M043, M140, M146, M236, M243; **új hiba**: M004, M057, M080, M154, M184, M237 |

proveniencia: scope=seed-101 véletlen 200 | forras=eseti szkript (tabla_kulcs.py: szerkezet_osszevet.tabla_strongonkent + kurzoros keresés) + m2_minta_osszevet.py | ts=2026-11-09

**A tábla új hibái a tábla saját bontásából jönnek** (forrással igazolva, a 2.30 sorai):
- M057 H4994: a 12. sor (`-/4/b`) a „c. אִםנָֿא, especially …” szöveget is hordozza — a héber szóval folytatódó bekezdésen belüli betűfej kimaradt;
- M154 H2471: „d. of מַצָּה burnt …” — ugyanígy (a `-/2/c` sorban);
- M004 H3588: a 18. sor `-/2/-` fejét a „(see Dr N.B.)” zárójeles hivatkozás „2”-je adja (hamis fej), a valódi 3. jelentés megszakad;
- M184 H9004: a „(see היה II. 2 c)” kereszthivatkozás `II. 2` hamis fej (a 8. sor);
- M237 H1004: a „-9 בֵּיתעֲבָדִים” felsorolás után hamis `2` fej (5. sor);
- M080 H5920: a hely a 2.30 jelölő nélküli bekezdésében (`-/-/-`), a vak lap és a szeletelő `-/a` (III. rész).

Következtetés: az átállás a seed-101-en **nem javít** (184 = 184), csak kicseréli a hibahalmazt; a tábla hibái a `bont.py` (#107) fej-
felismerésében vannak, amely nem a #102 `ir`-je. Ez tartalmi döntés (DT-F102d, l. 8.).

## 3. (g) A H1004 hamis folytatás (F102.1)

`bdb_szelet.hivatkozasok`: a vers-folytatás („, N”) tartomány nélkül sem indulhat egy kiírt hivatkozás kezdetén (a DT382 (A) tartomány
utáni ellenőrzése most mindkét ágon fut). Hatás a teljes táblán: **−1 sor** (H1004 sorszam 286, `, 2` → hamis 2Krón 10:2), más mező nem
változik. Regressziós teszt: `test_folytatas_nem_indul_kiirt_hivatkozas_elejen`, `test_h1004_nincs_hamis_folytatas`.
*(proveniencia: scope=adat/bdb_vers_jelentes.tsv, teljes | forras=eseti diff (tabla_diff.py: bdb_vers_jelentes.general a main táblájával szemben) | ts=2026-11-09)*
Mellékmegfigyelés (nem a #102 hatóköre): ugyanott a „2 Chronicles 10:20”, „10:26” `nem_letezo_vers` (a 2Krón 10-ben 19 vers; a forrás valószínűleg 1Kir 12:20, 26).

## 4. (b) Öröklés az egyfejezetes könyv után (F102.1)

`bdb_szelet.hivatkozasok`: ha az örökölt könyv egyfejezetes (`EGYFEJEZETES_KONYV`: Abd, Filem, 2Ján, 3Ján, Júd) és a könyv nélküli hely
fejezete nem 1, az egyfejezetes könyv előtti könyv öröklődik, okkód `orokles_egyfejezetes`. Az első változat (kapu nélkül) 25 sort oldott
fel; a TAHOT ebből 15-öt igazolt. A 10 nem igazolt: H6215 (6 sor) és H0343 (3 sor) **Abdiás-versek**, amelyeket a TSV-szöveg hamis
fejezetszámmal ír („Obadiah 6, עֵשָׂו בֵּית 49:18 …” — a BDB-ben Ob 18, 8, 9, 19, 21; „Obadiah 13 … 46:12; 46:14 … 46:15” — Ob 12, 14, 15);
H4530 (1 sor) helyes könyv (2Móz 12:4), de Targum-hely (a szó arámi glossza). Ezért a generátor (`bdb_vers_jelentes.general`) a DT-F99k
mintájára **TAHOT-kapuval** fogad el: a Károli-vers (híján az azonos számú vers) hordozza-e a Strong-számot; ha nem, a sor marad
`orokles_hibas` (könyv és vers nélkül, bizonytalan). Eredmény: **15 sor** oldódik fel (mind TAHOT-igazolt), köztük a seed-101 M092
(H0669 „31:1” → 2Krón 31:1). *(proveniencia: scope=adat/bdb_vers_jelentes.tsv okkod=orokles_egyfejezetes | forras=eseti szkript tahot_ell.py (TAHOT_kivonat.tsv, Igehely = Károli-vers) | ts=2026-11-09)*
A TSV Abdiás-fejezetszám-hibája (9 sor) forrás-/konverziós hiba, nem a szeletelőé: N-F102c.

Csoportzárás (F102.1): tábla `--ts 2026-11-09` (kilépési kód 0, mtime változott, `--ellenoriz` bájtra azonos); aranyminta változatlan
(az összesítő bájtra azonos); `teszt_bdb_vers_jelentes` 35/35; `teszt_futtat --gyors` 11 fájl zöld (322 mp).

## 5. (d) A magányos „II.” — M130 (F102.2)

Mérés a teljes BDB-n (eseti szkript `magany_ii.py`: „II.” kisbetűs vagy zárójeles folytatással, „I.” nélküli szócikkben, kereszthivatkozás
és héber szó után nem): **21 jelölt**, ebből 20 arab igetörzs a nyelvi háttérben („Arabic II. prolongavit, IV. …”), 1 valódi fő tagolás
(H8478 „Ezek 47:1b II. as preposition”). A szabály ezért szűk: `bdb_szelet._tagolas` — ha nincs legalább kételemű római sor, a magányos
„II.” akkor fő tagolás, ha szófaj-fej követi („as preposition|conjunction|adverb|substantive|noun|adjective”), a szócikkben nincs „I.”, és
pontosan egy ilyen van. Hatás: csak a H8478 — 214 sor `resz` → `II`, 25 sor `utvonal` `-/1` → `fej` (a „II. as preposition; so construct,
and with suffix …” alaktani bevezetője; a 2.30 ugyanezt `II -/-/-`-ként bontja). M130 (poz 3485, Hab 3:16): `resz` II, `-/2/a` — a vak
lap szerint. *(proveniencia: scope=adat/bdb_vers_jelentes.tsv, teljes | forras=eseti diff (tabla_diff.py) + magany_ii.py | ts=2026-11-09)*

## 6. (c) Szűrés (F102.2)

**(c1) A nem bibliai jelölőről öröklődő könyv** (ELLENOR_F99 12.: H2623 „116:15” + Zsolt 149:1, 5, 9; H4912 „1:1”). `hivatkozasok`: a
`nem_bibliai`-t öröklő könyv nélküli hely megkapja a jelölő előtti utolsó bibliai könyvet (`alt_konyv`); a generátor TAHOT-igazolással
fogadja el (okkód `orokles_nem_bibliai_utan`, nem szűrt), különben marad `nem_bibliai` (szűrt). Hatás: **10 sor** — H2623 116:15, 149:1,
149:5, 149:9 (Zsolt); H4912 1:1 (2×), 1:6 (Péld); H0966 1:4 (Bír, „Error in 1:4-5”); H7073 1:13 (Bír, „GFM 1:13ff.”: Moore kommentárja a
Bír 1:13-hoz — a vers a szót hordozza); H7350 20:18 (2Móz, „Gi 20:15; 20:18”). A H2623 „7:13” (1Makk) szűrt marad (a TAHOT nem igazolja).
Forrással átnézve: mind a 10 bibliai hely.
**(c2) M223-típus** (ELLENOR_F99 9.; a `bdb_szelet.py` megjegyzése ezt a javítási feladatra hagyta): a `sigla_kozel` nem áll, ha a sigla és a
hely között záró zárójel van („Josh 23:7 (R^D), compare Hosea 2:19”). Hatás: **224 sor okkódja** — 200 `sigla_igazolt` → üres (eddig is
bibliai), **24** `sigla_kozel` (szűrt, a TAHOT nem igazolta) → bibliai. A 24 forrással átnézve: mind bibliai idézet (nem kommentár-hely),
a TAHOT-igazolás főleg az arámi Strongoknál (Dán) hiányzott (H0002, H0321, H0744, H3860, H4429, H4576, H5750, H8128 …). Az M223 maga a
main-en már `sigla_igazolt` volt (az F85-ös Károli-kulcs óta: Hós 2:19 MT → Károli 2:16), most okkód nélküli.
*(proveniencia: scope=adat/bdb_vers_jelentes.tsv, teljes | forras=eseti diff (tabla_diff.py) + kornyezet.py (BDB_teljes_unabridged.tsv, lapított) | ts=2026-11-09)*
**(c3) A hét `sigla_igazolt` eltérés** (M054, M065, M147, M149, M191, M198, M230): mind tapadt vagy közvetlen szerző-sigla („see Di^Lev 7:30”,
„compare Dr^Amos 2:2”, „COT^Gen 10:22”, „Dr^Deut 2:11”, „(Baer^Josh 1:7)”, „Du^Isa 29:3 thinks …”, „: Dr^1Sam 14:18)”); a TAHOT a versben
hordozza a szót (DT176 → bibliai), a két vak kitöltő mind a 7-et kommentár-helynek ítélte. Ez a DT176 finomítása, tartalmi döntés:
**DT-F102e** (javaslat, nem alkalmazva).

Csoportzárás (F102.2): tábla `--ts 2026-11-09` (kilépési kód 0, mtime-őr, `--ellenoriz` bájtra azonos); aranyminta összesítő változatlan;
`teszt_bdb_vers_jelentes` 38/38. A `test_kozvetlen_szerzo_sigla_tapadt` három elvárása az M223-szabály szerint módosult (a „(MI^10) Jer 48:1”,
„(Kö^ii.l,74) Jer 6:13”, „(both R^D), Jer 6:24” most bibliai).

## 7. (e) A korpusz-eltérés osztályozása (F102.3)

Javítás után: `szerkezet_osszevet.py --korpusz` 161 275 nem szűrt hivatkozás, egyezik 138 046 (**85,6%**, előtte 85,5%); `jelentes_elter` 6 486,
`csak_resz` 4 556, `torzs_elter` 3 978, `alpont_elter` 2 602, `szeletelo_fej_tabla_tagolt` 2 441, `nem_talalt` 1 778, `tabla_fej_szeletelo_tagolt`
1 388. *(proveniencia: scope=adat/bdb_szakaszok.tsv × adat/bdb_vers_jelentes.tsv (F102.2) | forras=eszkozok/bdb_jelolt/szerkezet_osszevet.py --korpusz --lista 100000 | ts=2026-11-09)*

**Minták szerint** (a számok N-re normálva; a leggyakoribb párok osztályonként):
- `csak_resz`: a két réteg római-szint szemantikája tér el — a 2.29 `resz`-e (DT174, a szócikk fő tagolása) a 2.30-ban sokszor `szakasz` (homonima)
  vagy üres, és fordítva („szeletelő II -/N ↔ tábla - -/N/-” 553, „I -/N ↔ -” 303, „- ↔ tábla II” 257). Rendszerszintű, nem soronkénti hiba: a 2.30
  homonima-száma a címsorban áll, nem oszlopban.
- `torzs_elter`: törzshatár-eltérés („Hiph'il/N ↔ Qal/N” 164; „-/N ↔ Qal/N” 154: a szeletelő a törzsnév nélküli első törzset nem nevezi meg —
  M162-típus; „Qal/- ↔ Niph'al” 117).
- `jelentes_elter`: számozás-elcsúszás azonos alakkal („-/N ↔ -/N/-” 796; betűvel osztályonként 300 körül) — hamis vagy kimaradt számfej mindkét
  oldalon (gyakoriságszám, zárójeles jelölő a szeletelőben; kereszthivatkozás a táblában).
- `alpont_elter`: „-/N/a ↔ -/N/-” 237, „Pi'el/- ↔ Pi'el/N” 113: kimaradt vagy hamis betű-/számfej.
- `szeletelo_fej_tabla_tagolt` / `tabla_fej_szeletelo_tagolt`: a fej-határ (a szeletelőben tagolatlan, a táblában számozott: 504; a táblában fej, a
  szeletelőben `-/N`: 580).
- `nem_talalt` (1 778): a hivatkozás a 2.30 szövegében nem található (a két szövegréteg eltérése: a TSV F34/F46 hivatkozás-javításai, pe/mem).

**Melyik a helyes — vak kitöltéssel ítélt minta** (az egyetlen ítélt mérés a soronkénti igazságról; eseti szkript `elteres_itelt.py`, a kitöltés a mérce):

| minta | mindkettő jó | csak a szeletelő jó | csak a tábla jó | mindkettő rossz, eltérő | mindkettő rossz, azonos |
|---|---:|---:|---:|---:|---:|
| seed-101 | 179 | 6 | 6 | 3 (M031, M117, M162) | 6 |
| seed-100 | 184 | 8 | 0 | 1 (M101) | 7 |

*(proveniencia: scope=seed-100, seed-101 véletlen 200 | forras=eseti szkript elteres_itelt.py (m2_minta_osszevet.bont/fo) + kitoltott_A/B | ts=2026-11-09)*
Következtetés: a 14,4% eltérés két nagyjából egyforma hibaforrás összege; az ítélt mintán az eltérő sorok fele-fele arányban oszlanak (a
seed-100-on a szeletelő javára, amelyre a szeletelő hangolódott). A soronkénti osztályozás a teljes korpuszon ítélet nélkül nem automatizálható;
a döntés a seed-102-n (DT-F102d (C)).

## 8. Döntési pontok (⛔ 3.1, 3.3; F102.3)

- **3.1 (DT-F102d)**: hogy a hibák egy része a szövegrétegben keletkezik, azt az 1a./1c. és a #107 már igazolta (a 2.30 a jelölt szövegréteg, DT225); a
  #102 kérdése most az, hogy a 2.29 jelentéspontja melyik rétegből jöjjön. Javaslat: (C), mérés a seed-102-n.
- **3.3 (DT-F102a)**: a 2.30-ban a formátum már bővült (DT190 🟡); a 2.29 formátuma és az összevetés szabálya nyitott — javaslat (a). Az **M029**
  okafogyott (a 2.29 ma is homonima-szakaszként adja, a 2.30 is, DT229 (a) (2)); külön DT-F102b nem nyílt; a seed-102 vak lap fejléce a (3a) pontban
  kimondja.
- **DT382 (B) (DT-F102f)**: javaslat (A), a DT382 🟢 megerősítése.
- **DT-F102e**: a hét `sigla_igazolt`, javaslat (B).

## 9. ⛔ 3.5 — az újramérés előkészítése (F102.3)

- Vak munkalap és kulcs, **seed 102**: `naplok/BDB_SZELETELO_M2_minta_seed102_vak.tsv` (250 sor), `naplok/BDB_SZELETELO_M2_minta_seed102_kulcs.tsv`
  (réteg: véletlen 200, szűrt 25, bizonytalan 25); `python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --minta 102`, a tábla F102.2 állapotán. A vak
  lap fejléce a (3a) ponttal bővült (M029-típus, DT229 (a) (2)).
- A kapu következménye: DT-F102c (javaslat (a): nyers szám, a kitöltés ELŐTT rögzítve).
- **Kitöltés**: két független, friss kontextusú **modell**-kitöltő (mint a seed-99/100/101-nél): `_A` M001–M125, `_B` M126–M250, egyenként
  **125 elem**; a vak lapot és a BDB TSV-t látják, a kulcsot nem. Kimenet: `naplok/BDB_SZELETELO_M2_seed102_kitoltott_A.tsv`, `_B.tsv` (a seed-101
  oszlopaival: `azon strong konyv_mt karoli_vers jelentespont resz szures megjegyzes`). A vak kitöltést az orkesztrátor indítja, nem a #102 menete.
- Összevetés a kitöltés után: `m2_minta_osszevet.py --kulcs …seed102_kulcs.tsv --kitoltott …_A.tsv …_B.tsv` (szeletelő), és ugyanez `--szakasztabla`-val
  (a 2.30 útvonala) — a DT-F102d (C) szerint; ha a DT-F102a (a), az összevetés szabályát a kitöltés előtt kell beírni.

## 10. A seed-101 hibaosztályai előtte / utána (kötelező mérés)

Mindkét oszlop ugyanazzal a szkripttel: `python eszkozok/olvaso_szerver/m2_minta_osszevet.py --kulcs naplok/BDB_SZELETELO_M2_minta_seed101_kulcs.tsv
--kitoltott …_A.tsv …_B.tsv --mai-tabla`; előtte a main táblája (`b92d4dc5`), utána az ág táblája (F102.2; az F102.3 csak a fejléc kód-hash-ét írja).
*(proveniencia: scope=seed-101 (250 sor) | forras=eszkozok/olvaso_szerver/m2_minta_osszevet.py --mai-tabla | ts=2026-11-09)*

| mutató | előtte | utána |
|---|---:|---:|
| jelentéspont, véletlen 200 | 184 (92,0%) | **185** (92,5%) |
| előtagként helyes | 185 | 186 |
| könyv/vers, véletlen 200 | 197 | 197 |
| szűrés egyezése: véletlen / szűrt / bizonytalan | 197 / 22 / 13 | 197 / **24** / 13 |

| hely | osztály | előtte | utána |
|---|---|---|---|
| M028, M043 | gyakoriságszámos jelölő | hibás | hibás (a 2.30 megoldja; DT-F102d) |
| M146, M243 | zárójeles jelölő | hibás | hibás (a 2.30 megoldja) |
| M140 | OCR / fejléc-glossza | hibás | hibás (a 2.30 megoldja) |
| M236 | laza „2. a.” | hibás | hibás (a 2.30 megoldja) |
| M102, M117, M162 | `forras_hiba` (2.31 kézi sor) | hibás | hibás (forráshiba; egyik réteg sem oldja) |
| M031 | törzsfejléc „Hiph`il A./B.” | hibás | hibás (a 2.30 `Hiph'il.B/2`; formátum: DT-F102a) |
| M203 | fő tagolás (H3068, angol „II.”) | hibás | hibás (a 2.30 `resz` II; a 2.29 `resz`-e nem) |
| M238 | jelöletlen alcímszó | hibás | hibás (a 2.30 helyes, de a kurzoros illesztés nem találja) |
| **M130** | magányos „II.” | hibás | **helyes** (`II -/2/a`) |
| **M092** | öröklés egyfejezetes könyv után | `orokles_hibas` (könyv nélkül) | **2Krón 31:1** (a jóváhagyott ítélet szerint; TAHOT-igazolt) |
| **M001** (H2623 116:15) | nem bibliai jelölőről öröklés | szűrt (`nem_bibliai`) | **bibliai, Zsolt 116:15** (+ 149:1, 5, 9) |
| **M159** (H4912 1:1) | ugyanaz | szűrt | **bibliai, Péld 1:1** (+ 1:1, 1:6) |
| M223 (H8034 Hos 2:19) | lezárt megjegyzés utáni sigla | bibliai (`sigla_igazolt`, a main-en már) | bibliai, okkód nélkül |
| M054, M065, M147, M149, M191, M198, M230 | a hét `sigla_igazolt` | bibliai (a kitöltés: kommentár-hely) | változatlan — DT-F102e |
| M008, M011, M029 | kulcs-ellentmondás (formátum, homonima) | eltérés | eltérés — DT-F102a |

A 13 jóváhagyott szeletelő-hibából 1 javult a szeletelőben (M130); 6-ot a 2.30 útvonala javítana (DT-F102d); 3 forráshiba; 3 marad (M031, M203,
M238 — mindhárom a 2.30-ban helyes vagy formátumkérdés). Öröklés: 1/1; szűrés: a 2 igazolt hamis pozitív (4 + 3 sor) 2/2; M223 1/1. A szűrés
„bizonytalan” rétegének egyezése 13 maradt: az M051 (17:9, `orokles_egyfejezetes` → 1Kir 17:9) most egyezik, az M092 most nem, mert a kitöltő
„bizonytalan”-t írt — a jóváhagyott ítélet szerint viszont a 2Krón 31:1 a helyes.
Az aranyminta mindhárom csoport után változatlan (a `bdb_szelet_m0.py --arany` összesítője bájtra azonos: EN hibás szócikk 7/32, szerkezeti eltérés
52; HU 23/32, 220).

## 11. A HAMART-001 két esete — rétegmérés (csak mérés; javítás nincs, a lap nem generálódott újra)

- **H2403 (chattát)** → **(i) a 2.30** (`bdb_szakaszok.tsv` BDB2699 `sorszam` 13: a „see 1 above” hamis `1` fej; a 14–16. sor `-/1/a–c` a
  `-/4/a–c` helyett) + **(iii) a generátor** (`lexikon_general.py` `bdb_gerinc_szocikkek()`: a nem szomszédos azonos `(bdb_id, utvonal)` kulcsok
  összevonása; a 13. sor `horgonnyal` kategóriája → `HORGONNYAL_JELOLES`). A 2.29 helyes (Lev 23:19 `-/4`, Lev 4:24 `-/4/a` …). → **N-F102a**.
- **H7451 (ra)** → **(iii) a magyar illesztés** (`bdb_szakasz_hu.tsv`: a BDB8033 és a BDB8034 `fej` sora `jelolo_nelkul`, szöveg nélkül; a „II. רַע …”
  fej a BDB8032 10.d magyar szövegének végén áll; a H7451 fordítása nem szakaszonkénti). A 2.30 szócikkhatára helyes, a 2.29 nem érintett. → **N-F102b**.
*(proveniencia: scope=H2403, H7451 | forras=adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv, lexikon/HAMART-001_TUDOMANYOS.md (1687., 1801. sor), eszkozok/lexikon_general.py | ts=2026-11-09)*

## 12. DT190-érintettség

A #102 a DT190-et (a 2.30 útvonal-formátuma mint kanonikus kulcs) **nem dönti el**, hanem **feltételezi** a mai állapotát: a 2.29 formátuma nem
változott, a `--szakasztabla` mérés a 2.30 útvonalát a 2.29 alakjára hozza (a csoport- és a zárójeles szint nélkül). Ha a DT-F102a (b) vagy a
DT-F102d (B) választódik, az a DT190-et érinti (a 2.29 a 2.30 kulcsát venné át).

## 13. A döntések alkalmazása (F102.4)

Orkesztrátori döntés (local_c8cc3610, a felhasználó felhatalmazásával), 2026-11-09, mind a javaslat szerint: DT-F102a (a), DT-F102c (a), DT-F102d (C),
DT-F102e (B), DT-F102f (A).

- **DT-F102a (a)** — `m2_minta_osszevet.py` `fo()`: a fő mutató a zárójeles szint mellett az egyetlen nagybetűs csoportszegmenst (`A`–`H`) és a görög
  betűs szegmenst is elhagyja; az előtag-mutató változatlan. A seed-102 kitöltése ELŐTT rögzítve. Hatás a seed-101-en (tájékoztató, a korábbi
  számok e szabály előtt készültek): jelentéspont 185 → **187** (M008, M011 most egyezik). *(proveniencia: scope=seed-101 véletlen 200 | forras=m2_minta_osszevet.py --mai-tabla | ts=2026-11-09)*
- **DT-F102c (a)** — a kapu: a seed-102 NYERS mért száma dönt, az ítélet előtt kiszámolva, a fenti összevetési szabállyal: könyv/vers ≥ 99% ÉS
  jelentéspont ≥ 97% a 200 véletlen soron → a „próba” jelölés lekerül, a `blokkok.py` `BDB_MERT_PONTOSSAG` az új nyers szám és 95%-os CI; különben a
  „próba” marad, a lapon az új nyers szám és CI, a további javítás külön feladat, a #102-ben nincs több mérési kör. A 3.6 ítélete csak osztályoz.
- **DT-F102d (C)** — a seed-102-n mindkét kulcs mérve ugyanazzal a kitöltéssel (szeletelő és `--szakasztabla`); a magasabb jelentéspont-szám dönt,
  döntetlennél marad a szeletelő; a 2.30-ra állás csak a `bont.py` hibaosztályainak (N-F102e) javítása után.
- **DT-F102e (B)** — `bdb_vers_jelentes.py` `SIGLA_MINDIG_SZURT`: a `sigla_tapadt` és a `sigla_lista` mindig szűrt; a TAHOT-kapu csak a `sigla_kozel`-é.
  Hatás a teljes táblán: **192 sor** `sigla_igazolt` → szűrt (`okkod`, `szurt`, `mt_vers`, `karoli_vers`, `vers_feloldas`), más mező nem.
  *(proveniencia: scope=adat/bdb_vers_jelentes.tsv, teljes | forras=eseti diff (tabla_diff.py) az F102.3 táblájával szemben | ts=2026-11-09)*
- **DT-F102f (A)** — nincs tartomány-kibontás; a DT382 döntése érvényes.

**A seed-102 kulcsa:** a `--minta 102` újrafuttatása a megváltozott rétegkészletek (a „bizonytalan” réteg a `sigla_igazolt` sorokat is húzza) miatt
**más mintát húzna** — ezért nem futott újra. A meglévő kulcs soraiba (ugyanazok az azonosítók, `strong` + `poz`) a mai 2.29 értékei kerültek
(eseti szkript `kulcs_frissit.py`; a kulcs első sora ezt kimondja): **10 sor változott**, mind a „bizonytalan” rétegben (M031, M122, M157, M162,
M185, M191, M197, M212, M213, M215: `sigla_igazolt` → `sigla_tapadt`, szűrt); a véletlen 200-ból egy sem. A vak munkalap bájtra változatlan.

**A kitöltés utáni összevetés** (a repó gyökeréből):
- szeletelő: `python eszkozok/olvaso_szerver/m2_minta_osszevet.py --kulcs naplok/BDB_SZELETELO_M2_minta_seed102_kulcs.tsv --kitoltott naplok/BDB_SZELETELO_M2_seed102_kitoltott_A.tsv naplok/BDB_SZELETELO_M2_seed102_kitoltott_B.tsv`
- szakasztábla: ugyanez `--szakasztabla` kapcsolóval.

Csoportzárás (F102.4): tábla `--ts 2026-11-09` (kilépési kód 0, mtime-őr, `--ellenoriz` bájtra azonos); aranyminta, `teszt_bdb_vers_jelentes`,
`teszt_futtat --gyors`: l. a commit-üzenetet.

## 14. A seed-102 vak kitöltése és nyers összevetése (F102.5)

**Kitöltés** (az orkesztrátor indította, 2026-11-09): két független, friss kontextusú Opus-kitöltő; `naplok/BDB_SZELETELO_M2_seed102_kitoltott_A.tsv`
(M001–M125) és `_B.tsv` (M126–M250), változtatás nélkül mentve (az orkesztrátor `cmp`-vel igazolta). **Eltérés a brieftől és a döntéstől:** a kitöltők
a munkalap felén és a `konkordancia/BDB_teljes_unabridged.tsv`-n kívül a `karoli_vers` oszlophoz a `konkordancia/Karoli_1908.tsv`-t és a
`konkordancia/Konyv_normalizalo_tabla.tsv`-t is látták (a brief és a DT-F102c csak a BDB-t nevezte). A jelentéspontot és a szűrést ez nem érinti; a
Károli-oszlopot az összevetés nem bírálja.

**Nyers összevetés — szeletelő (2.29)** *(proveniencia: scope=seed-102 | forras=m2_minta_osszevet.py | ts=2026-11-09)*:

```
# M2 minta-összevetés: kulcs=naplok/BDB_SZELETELO_M2_minta_seed102_kulcs.tsv; kitöltött: naplok/BDB_SZELETELO_M2_seed102_kitoltott_A.tsv, naplok/BDB_SZELETELO_M2_seed102_kitoltott_B.tsv
veletlen	200
konyv_vers_egyezik	199
jelentespont_egyezik	183
jelentespont_elotagkent_helyes	183
VERS	M091	H2370	2:41	kulcs: Ezsd 2:41	kitoltott: Dán 2:41
JP	M003	H2505	kulcs: I  Niph'al/3	kitoltott: I Pi`el/1	
JP	M009	H5674	kulcs:   Hithpa'el/2/a	kitoltott: Hiph`il/2/a	
JP	M011	H3254	kulcs:   Niph'al/2	kitoltott: Hiph`il	
JP	M016	H2161	kulcs:   -/2/b	kitoltott: Qal/2/b	
JP	M027	H7323	kulcs:   Hiph'il/1	kitoltott: Qal/1	
JP	M034	H2490	kulcs: III  Hiph'il/-/b	kitoltott: III Hiph`il/2	
JP	M036	H3318	kulcs:   fej	kitoltott: Qal/1/h	
JP	M042	H5066	kulcs:   Qal/-	kitoltott: Qal/1	
JP	M050	H2063	kulcs:   -/3/i	kitoltott: -/6/g	
JP	M052	H9003	kulcs: I r:III -/5	kitoltott: -/5 r:III	
JP	M058	H3651	kulcs: I  -/3/f	kitoltott: tagolatlan	
JP	M143	H1980	kulcs:   Qal/-/a	kitoltott: Qal	
JP	M205	H5595	kulcs:   Qal/-	kitoltott: Qal/2	
JP	M208	H7617	kulcs:   Qal/-	kitoltott: Qal/2	
JP	M223	H7812	kulcs:   Hiph'il/1/b	kitoltott: Hithpa`lel/1/b	
JP	M233	H7812	kulcs:   Hiph'il/2/c	kitoltott: Hithpa`lel/2/c	
JP	M249	H2076	kulcs:   Pi'el/-	kitoltott: Pi`el/2	
szures_veletlen	200	egyezik 197
SZ	M015	Gen 10:4	kulcs: bibliai 	kitoltott: alhivatkozas: Dillmann-kommentár (Di Gen 10:4)
SZ	M214	Deut 4:25	kulcs: bibliai 	kitoltott: bizonytalan: Driver-hivatkozás (Dr^Intr 191) után áll, lehet Driver Deut-komment
SZ	M248	Cant 7:1	kulcs: kiszurt sigla_kozel	kitoltott: bibliai
szures_szurt	25	egyezik 23
SZ	M156	33:25	kulcs: kiszurt sigla_kozel	kitoltott: bibliai
SZ	M188	Jer 31:23	kulcs: kiszurt sigla_kozel	kitoltott: bibliai
szures_bizonytalan	25	egyezik 21
SZ	M039	15:15	kulcs: bizonytalan orokles_hibas	kitoltott: bibliai
SZ	M060	13:10	kulcs: kiszurt sigla_kozel	kitoltott: bibliai
SZ	M127	17:20	kulcs: bizonytalan orokles_hibas	kitoltott: bibliai
SZ	M196	30:14	kulcs: bizonytalan orokles_hibas	kitoltott: bibliai
```

**Nyers összevetés — szakasztábla (2.30 útvonal)** *(proveniencia: scope=seed-102 | forras=m2_minta_osszevet.py --szakasztabla | ts=2026-11-09)*:

```
# szakasztábla-útvonal: a nem szűrt kulcssorokból 1 nem rendelhető a 2.30-hoz (ott a 2.29 útvonala áll)
# M2 minta-összevetés: kulcs=naplok/BDB_SZELETELO_M2_minta_seed102_kulcs.tsv; kitöltött: naplok/BDB_SZELETELO_M2_seed102_kitoltott_A.tsv, naplok/BDB_SZELETELO_M2_seed102_kitoltott_B.tsv
veletlen	200
konyv_vers_egyezik	199
jelentespont_egyezik	184
jelentespont_elotagkent_helyes	185
VERS	M091	H2370	2:41	kulcs: Ezsd 2:41	kitoltott: Dán 2:41
JP	M002	H2388	kulcs:   Pi'el/6/c	kitoltott: Hiph`il/6/c	
JP	M018	H2534	kulcs:   -/2/-	kitoltott: -/2/c	előtagként helyes
JP	M036	H3318	kulcs:   -/1/h	kitoltott: Qal/1/h	
JP	M042	H5066	kulcs:   Qal/-/-	kitoltott: Qal/1	
JP	M052	H9003	kulcs: I r:III -/5/-	kitoltott: -/5 r:III	
JP	M056	H3452	kulcs:   -/-/a	kitoltott: -/b	
JP	M058	H3651	kulcs: I  fej	kitoltott: tagolatlan	
JP	M143	H1980	kulcs:   Qal/-/a	kitoltott: Qal	
JP	M194	H3452	kulcs:   -/-/a	kitoltott: -/b	
JP	M198	H3117	kulcs:   -/3/e	kitoltott: -/2/e	
JP	M201	H3117	kulcs:   -/3/e	kitoltott: -/2/e	
JP	M221	H2388	kulcs:   Pi'el/6/a	kitoltott: Hiph`il/6/a	
JP	M223	H7812	kulcs:   Hiph'il/1/b	kitoltott: Hithpa`lel/1/b	
JP	M226	H5676	kulcs: I  -/-/-	kitoltott: I -/1/B	
JP	M233	H7812	kulcs:   Hiph'il/2/c	kitoltott: Hithpa`lel/2/c	
JP	M242	H5973	kulcs: h:מעם  -/5/a	kitoltott: -/a	
szures_veletlen	200	egyezik 197
SZ	M015	Gen 10:4	kulcs: bibliai 	kitoltott: alhivatkozas: Dillmann-kommentár (Di Gen 10:4)
SZ	M214	Deut 4:25	kulcs: bibliai 	kitoltott: bizonytalan: Driver-hivatkozás (Dr^Intr 191) után áll, lehet Driver Deut-komment
SZ	M248	Cant 7:1	kulcs: kiszurt sigla_kozel	kitoltott: bibliai
szures_szurt	25	egyezik 23
SZ	M156	33:25	kulcs: kiszurt sigla_kozel	kitoltott: bibliai
SZ	M188	Jer 31:23	kulcs: kiszurt sigla_kozel	kitoltott: bibliai
szures_bizonytalan	25	egyezik 21
SZ	M039	15:15	kulcs: bizonytalan orokles_hibas	kitoltott: bibliai
SZ	M060	13:10	kulcs: kiszurt sigla_kozel	kitoltott: bibliai
SZ	M127	17:20	kulcs: bizonytalan orokles_hibas	kitoltott: bibliai
SZ	M196	30:14	kulcs: bizonytalan orokles_hibas	kitoltott: bibliai
```

Nyers számok (a DT-F102c (a) kapuja ezekre vonatkozik): szeletelő — könyv/vers 199/200 (99,5%), jelentéspont **183/200 (91,5%)**; szakasztábla —
könyv/vers 199/200, jelentéspont **184/200 (92,0%)**.

## 15. ⛔ 3.6 — a seed-102 ítéleti táblája (F102.6; jóváhagyásra; külön fájl: `naplok/BDB_SZELETELO_M2_seed102_iteletek.md`)

*Kézi ítélet a forrásszöveg alapján (`konkordancia/BDB_teljes_unabridged.tsv`, a Strong sora, a szeletelő „lapított” alakjában; a `poz` a
hivatkozás helye), a seed-101 mintájára (`naplok/BDB_SZELETELO_M2_seed101_iteletek.md`). Kategóriák: **szeletelő-hiba** (a 2.29 kulcsa hibás),
**szakasztábla-hiba** (a `--szakasztabla` kulcs útvonala hibás), **kitöltő-hiba** (csak a forrással bizonyítva), **kulcs-ellentmondás**,
**`forras_hiba`**. Mérés: kulcs `naplok/BDB_SZELETELO_M2_minta_seed102_kulcs.tsv` (F102.4), kitöltések `naplok/BDB_SZELETELO_M2_seed102_kitoltott_A.tsv`
és `_B.tsv` (F102.5), összevetés `m2_minta_osszevet.py` és `--szakasztabla` (`naplok/F102_BDB_SZELETELO_JAVITAS_naplo.md` 14.). A kapu
következménye az ítélet ELŐTT rögzítve: DT-F102c (a) (nyers szám); a forrás választása: DT-F102d (C). Proveniencia: `scope=seed-102 vak minta |
forras=BDB_teljes_unabridged.tsv (lapított; eseti szkript itel_dump.py, szakasz_ki.py) + m2_minta_osszevet.py [--szakasztabla] | ts=2026-11-09`;
az ítélet értelmezés (manual), nem gépi eredmény.*

**A törzsnév-írásmód ellenőrzése** (az orkesztrátor kérésére): az összevető a backticket aposztrófra normálja (`normal()`), és a törzs-eltérések
(M003, M009, M011, M027, M223, M233, M249) mind valódi törzs- vagy számeltérések (Niph'al ↔ Pi'el, Hithpa'el ↔ Hiph'il, Hiph'il ↔ Hithpa'lel,
Pi'el/- ↔ Pi'el/2), egyik sem az írásmódból jön. Az összevetőnek itt nincs hibája.

### 1. Összesítő

| | szeletelő (2.29) | szakasztábla (2.30 útvonal) |
|---|---:|---:|
| nyers jelentéspont, véletlen 200 | **183** (91,5%; 95% CI 86,7–95,0%) | **184** (92,0%; 87,3–95,4%) |
| eltérés | 17 | 16 |
| ebből saját hiba (szeletelő-, ill. szakasztábla-hiba) | 15 | 13 (+ 1 szeletelő-hiba a 2.29-ből átvett `szakasz`-ban: M058) |
| kitöltő-hiba | 1 (M052) | 1 (M052) |
| `forras_hiba` | 1 (M036) | 1 (M036) |
| kulcs-ellentmondás | 0 | 0 |
| **ítélet utáni** (csak tájékoztató) | **185** (92,5%; 87,9–95,7%) | **186** (93,0%; 88,5–96,1%) |
| könyv/vers, véletlen 200 | 199 (99,5%; 97,2–100%); az 1 eltérés `forras_hiba` (M091) → ítélet után 200 | ugyanaz |

**A kapu (DT-F102c (a), nyers szám):** könyv/vers 99,5% ≥ 99% teljesül, **jelentéspont 91,5% < 97% nem teljesül** → a „próba” jelölés marad; a
szó-lapon (`blokkok.py` `BDB_MERT_PONTOSSAG`) az új nyers szám és CI áll; a további javítás külön feladat, a #102-ben nincs több mérési kör.
**A forrás (DT-F102d (C)):** a nyers jelentéspont szakasztábla 184 > szeletelő 183 → **a szakasztábla nyer** (egy találattal; ítélet után is
+1, 186 ↔ 185). A (C) szerint a 2.29 átállása a 2.30-ra **csak a `bont.py` hibaosztályainak (N-F102e) javítása után**; a különbség (1/200) a
mérési szóráson belül van (a két CI szinte azonos).

### 2. Jelentéspont — soronkénti ítélet

Jelölés: SZ = a szeletelő kulcsa, T = a szakasztábla kulcsa, K = a kitöltés. A helyes érték a forrás szerint.

| azon | Strong | SZ | T | K | forrásidézet (a hely környezete) | ítélet SZ | ítélet T | ok |
|---|---|---|---|---|---|---|---|---|
| M002 | H2388 | `Hiph'il/6/c` | `Pi'el/6/c` | `Hiph`il/6/c` | „6 … a. … b. have or keep hold of … c. hold up … Dan 11:1 (\|\| מָעוֺז), 11:6” | — | **szakasztábla-hiba** | a 6. pont a Hiph`il-é (a BDB חזק Hiph. 6 „take or keep hold”); a tábla a Hiph`il fejet nem látja |
| M221 | H2388 | `Hiph'il/6/a` | `Pi'el/6/a` | `Hiph`il/6/a` | „laying hold of wisdom Prov 3:18 … Job 2:3, 9; 27:6; Jer 8:5. b. have or keep hold” | — | **szakasztábla-hiba** | mint M002 |
| M003 | H2505 | `I Niph'al/3` | `Pi'el/1` | `I Pi`el/1` | „(see above Niph`al) … Imperative חַלֵּק … — 1 divide, apportion: food … 1Chr 16:3” | **szeletelő-hiba** | — | a „see above Niph`al” visszautalás hamis törzsfej; a hely a Pi`el 1. pontja |
| M009 | H5674 | `Hithpa'el/2/a` | `Hiph'il/2/a` | `Hiph`il/2/a` | „— Hithpa`el see [עָבַר] below Hiph`il Perfect … 2. a. … Neh 8:15. b. let pass through” | **szeletelő-hiba** | — | a „Hithpa`el see … below” kereszthivatkozás hamis törzsfej, a rögtön utána álló Hiph`il elvész |
| M011 | H3254 | `Niph'al/2` | `Hiph'il/-` | `Hiph`il` | „Hiph`il172Perfect הֹסִיף 2Kin 24:7” | **szeletelő-hiba** | — | a gyakoriságszámhoz tapadt „Hiph`il172” törzsfejet a szeletelő nem ismeri fel; a hely a Hiph`il alaktani feje |
| M016 | H2161 | `-/2/b` | `Qal/2/b` | `Qal/2/b` | „b. of evil purpose … absolute Prov 30:32 … **the text of Prov 30:32 is questioned” | **szeletelő-hiba** | — | a szócikk igei, a Qal fej (poz 195) elveszett; a lábjegyzet a Qal 2.b-hez tartozik |
| M018 | H2534 | `-/2/c` | `-/2/-` | `-/2/c` | „Vbs. used with חֵמָה … 2. c.: הֵשִׁיב turn away wrath … arises עלה 2Chr 36:16” | — | **szakasztábla-hiba** | a függelék „2. c.:” címkéje alatt; a tábla csak a 2-ig jut (előtagként helyes) |
| M027 | H7323 | `Hiph'il/1` | `Qal/1` | `Qal/1` | „(… compare Hiph`il below); … אֵת person accompare Jer 12:5” | **szeletelő-hiba** | — | a „compare Hiph`il below” kereszthivatkozás hamis törzsfej |
| M034 | H2490 | `III Hiph'il/-/b` | `III Hiph'il/2` | `III Hiph`il/2` | „Hiph`il 1. a. … b. … 2 begin, Perfect הֵחֵל … with Infinitive (ל) begin to … 2Chr 3:1-2, 29:17” | **szeletelő-hiba** | — | a „2 begin,” jelentésfej elvész, a hely az 1.b-be csúszik |
| M036 | H3318 | `fej` | `-/1/h` | `Qal/1/h` | „h. … with idea of unfolding, growth Job 8:16; 14:2; 31:40” | **`forras_hiba`** | **`forras_hiba`** | a H3318 „Qal” neve mindkét nyers forrásból hiányzik (a seed-101 M162 hibaosztálya; 2.31 kézi sor); a jelentés (1.h) a táblában helyes |
| M042 | H5066 | `Qal/-` | `Qal/-` | `Qal/1` | „— draw or come near, 1 human subject: followed by אֶלֿ person … Exod 19:15” | **szeletelő-hiba** | **szakasztábla-hiba** | a fej-glossza utáni „1” jelentésfejet egyik sem ismeri fel |
| M050 | H2063 | `-/3/i` | `-/6/g` | `-/6/g` | „6 … f. זֶה עַל on this account … g. זֶה עִם in spite of this Neh 5:18” | **szeletelő-hiba** | — | a hely a 6.g-ben áll; a szeletelő a 3.i-nél ragad |
| M052 | H9003 | `I r:III -/5` | `I r:III -/5` | `-/5 r:III` | „ב בּ ב,, Bêth, 2nd letter; … I. בְּ, preposition” | — | — | **kitöltő-hiba**: a címszó előtt a forrás „I.”-t ír; a vak lap (1) szabálya szerint a fő címszónál is írandó |
| M056 | H3452 | `-/-/b` | `-/-/a` | `-/b` | „b. without article, a waste or wilderness … Psa 68:8; 78:40; 106:14” | — | **szakasztábla-hiba** | a hely a b.-ben áll; a tábla a b. fejet nem bontja |
| M194 | H3452 | `-/-/b` | `-/-/a` | `-/b` | „b. without article … with reference to returning exiles Isa 43:19-20” | — | **szakasztábla-hiba** | mint M056 |
| M058 | H3651 | `I -/3/f` | `I fej` | `tagolatlan` | „IV. כֵּן see II. כנן. p. 467, below adverb thus … Dan 2:24 …, 2:25; 4:11” | **szeletelő-hiba** | **szeletelő-hiba** (a 2.29-ből átvett `szakasz` I) | a szócikk végi jelöletlen arámi כֵּן címszó tagolatlan; a szeletelő az I. 3.f-be teszi, a `--szakasztabla` útvonala (`fej`) helyes, de a `szakasz` I a 2.29-é |
| M143 | H1980 | `Qal/-/a` | `Qal/-/a` | `Qal` | „Imperative rarely a. הֲלוֺךְ Prov 13:20 (Kt.; Qr הֹלֵךְ” | **szeletelő-hiba** | **szakasztábla-hiba** | az „a.” az alaktani felsorolás (Imperative-alakok) betűje, nem jelentés-alpont — *kérdéses* (l. 4.) |
| M198 | H3117 | `-/2/e` | `-/3/e` | `-/2/e` | „(see Zech 14:7 below 3 below) d. day as defined by evening … e. day of month … Exod 12:10” | — | **szakasztábla-hiba** | a „below 3 below” visszautalás hamis „3” fej (a H2403 „see 1 above” osztálya) |
| M201 | H3117 | `-/2/e` | `-/3/e` | `-/2/e` | ugyanott: „… Exod 12:10; 2Kin 25:1, 3; Ezek 1:1-2” | — | **szakasztábla-hiba** | mint M198 |
| M205 | H5595 | `Qal/-` | `Qal/2` | `Qal/2` | „2 transitive: Imperfect … suffix לִסְמּוֺתָהּ Psa 40:15” | **szeletelő-hiba** | — | a „2 transitive:” jelentésfej elvész |
| M208 | H7617 | `Qal/-` | `Qal/2` | `Qal/2` | „2 with accusative of congnate meaning … 2Chr 28:5, 11” | **szeletelő-hiba** | — | mint M205 |
| M223 | H7812 | `Hiph'il/1/b` | `Hiph'il/1/b` | `Hithpa`lel/1/b` | „Hithpa`lel_170 (Ges^§ 75kk) Perfect … b. with ל … Isa 60:14” | **szeletelő-hiba** | **szakasztábla-hiba** | a „Hithpa`lel” törzset (gyakoriságszámmal) egyik sem ismeri fel; a hely a Hithpa`lel 1.b-je |
| M233 | H7812 | `Hiph'il/2/c` | `Hiph'il/2/c` | `Hithpa`lel/2/c` | „c. with לְ only: 1Sam 1:28” | **szeletelő-hiba** | **szakasztábla-hiba** | mint M223 |
| M226 | H5676 | `I -/1` | `I -/-/-` | `I -/1/B` | „1 … B. West Jordan … + יָ֫מָּה Josh 5:1” | — | **szakasztábla-hiba** | a hely az 1. pont B. csoportjában; a nagybetűs szintet a DT-F102a (a) szerint a fő mutató elhagyja, a tábla viszont az „1”-et is elveszti |
| M242 | H5973 | `h:מעם -/-/a` | `-/5/a` | `-/a` | „(a jelöletlen מֵעִם címszó) … after שׁאל to ask … Isa 7:11” | — | **szakasztábla-hiba** | a jelöletlen מֵעִם alcímszó saját a.-ja; a tábla az עִם 5.a-jába vonja |
| M249 | H2076 | `Pi'el/-` | `Pi'el/2` | `Pi`el/2` | „but 2 elsewhere of sacrifice to other deities … Hab 1:16” | **szeletelő-hiba** | — | a mondat belsejében álló „2” jelentésfej elvész |

Szeletelő-hiba 15: M003, M009, M011, M016, M027, M034, M042, M050, M058, M143, M205, M208, M223, M233, M249. Szakasztábla-hiba 13: M002, M018,
M042, M056, M143, M194, M198, M201, M221, M223, M226, M233, M242 (+ M058 a 2.29-ből átvett `szakasz`-szal).
**Okcsoportok** — szeletelő: kereszthivatkozásból hamis törzsfej (M003, M009, M027), gyakoriságszámhoz tapadt törzsnév (M011, M223, M233), mondat
belsejében álló vagy fej-glossza utáni jelentésfej (M034, M042, M205, M208, M249), elveszett törzsfej (M016), elcsúszott számozás (M050),
jelöletlen alcímszó (M058), alaktani betű (M143). Szakasztábla: elveszett törzsfej (M002, M221 Hiph`il; M223, M233 Hithpa`lel), visszautalásból
hamis fej (M198, M201), kimaradt betűfej (M056, M194), durvább szint (M018, M042, M226), alcímszó (M242), alaktani betű (M143).

### 3. Könyv/vers és szűrés (a jelentéspont-mércén kívül)

| azon | forrásidézet | ítélet |
|---|---|---|
| M091 H2370 (VERS) | „3 usually behold in dream or vision …, Ezra 4:20, accusative of thing 2:41” | **`forras_hiba`**: a forrás „Ezra 4:20”-at ír a Dán 4:20 helyett (a 4:14 valóban Ezsdrás); a 2:41 ezt a hibás könyvet örökli (Ezsd 2:41); a helyes Dán 2:41 — a kitöltés szerint |
| M015 H0473 (véletlen) | „Italy, … compare ᵑ7 … Ezek, Di Gen 10:4; Carthage = Elissa” | **szeletelő-hiba** (szűrés): „Di Gen 10:4” = Dillmann kommentárja a helyhez (`^` nélküli szerző-sigla, a szeletelő nem ismeri fel); a DT-F102e (B) szerint szűrendő |
| M214 H3707 (véletlen) | „— The phrase is characteristic of D …; see Dr^Intr 191; Deut 4:25 Holz^eini. Hexateuch 287” | **kitöltő-hiba** — *kérdéses*: a „Dr^Intr 191;” lezárt hivatkozás után a Deut 4:25 a kifejezés fent már idézett bibliai helye (a 2.b-ben), nem Driver lapszáma |
| M248 H4266 (véletlen) | „site unknown, see Di^Gn; הַמַּחֲנָ֑יִם כִּמְחֹלַת Cant 7:1 is put here by Ew Hi Öttli” | **szeletelő-hiba** (szűrés): bibliai idézet (Én 7:1); a `sigla_kozel` szűrte, mert a TAHOT nem igazolta |
| M156 H2022 (szűrt) | „but Ezek 18:6, 15 read perhaps הַדָּם for הרים compare RS^K 310 & 33:25” | **szeletelő-hiba** (szűrés): a 33:25 (Ez 33:25) bibliai hely, nem a sigla része |
| M188 H6994 (szűrt) | „(ה)ק ׳הר Isa 11:9 6t. Isa^2; Isa^3; Jer 31:23” | **szeletelő-hiba** (szűrés): az „Isa^2; Isa^3;” könyvrész-jel (Deutero-/Trito-Ézsaiás), nem kommentár; a Jer 31:23 bibliai |
| M039 H1121 (bizonytalan) | „1Chr 9:18; … 12:27; Nehemiah 10:40; הַלֵּוִי בְּנֵי 15:15; 24:30” | **szeletelő-hiba** — *kérdéses*: a közbeékelt Nehemiásnak nincs 15. fejezete; a helyes 1Krón 15:15 (a szeletelő `orokles_hibas`-t ad, a szabály szerint bizonytalan) |
| M127 H5203 (bizonytalan) | „1Sam 30:16 …; … Hosea 12:15 …; leave in charge of … sheep 17:20, 28; baggage 17:22” | **szeletelő-hiba** — *kérdéses*: mint M039 (1Sám 17:20) |
| M196 H1736 (bizonytalan) | „noun masculine^Gen 30:14 … 30:14; Cant 7:14; construct דּוּדָאֵי 30:14 3t.” | **szeletelő-hiba** — *kérdéses*: mint M039 (1Móz 30:14) |
| M060 H6920 (bizonytalan) | „— Σηλωρ, ᵐ5^L Σιλωρ, but 13:10; Jer 48:34 Ζογορ(α)” | **kulcs-ellentmondás** — *kérdéses*: a forrás könyvnév nélkül írja a 13:10-et (a LXX-alak helye, valószínűleg 1Móz 13:10); a kulcs könyv híján szűrt, a kitöltés bibliai — a szabály nem dönti el |

Szűrés, ítélet után: véletlen 197 → 199 kitöltő-hiba nélkül (M214), a szeletelő 2 hibája (M015, M248) marad; szűrt 23/25 (M156, M188 szeletelő-hiba);
bizonytalan 21/25 (M039, M127, M196 szeletelő-hiba — a közbeékelt, nem létező fejezetű könyv átugrása, az F102 (b) szabályának kiterjesztése
lenne —, M060 kulcs-ellentmondás).

### 4. Kérdéses (nem egyértelmű) tételek

- **M143** H1980: az „Imperative rarely a. הֲלוֺךְ” „a.”-ja alaktani felsorolás vagy szerkezeti alpont? Az ítélet: alaktani (mindkét kulcs hibás).
- **M018** H2534: a „Vbs. used with חֵמָה … 2. c.:” függelék címkéje jelentéspont-e; az ítélet a kulcsot és a kitöltést fogadja el (a tábla durvább).
- **M036** H3318: `forras_hiba` (a „Qal” név hiányzik) vagy szeletelő-hiba — a seed-101 M162 ítélete szeletelő-hiba volt, a #107 1c. `forras_hiba`-nak vette; itt az 1c. szerint.
- **M091** H2370: a forrás „Ezra 4:20”-a könyvnév-hiba (Dán) — a TAHOT itt nem dönt (az arámi Strong a kivonatban nem illeszkedik: 0 találat mindkét versre).
- **M214** H3707: a „Dr^Intr 191; Deut 4:25” Deut 4:25-je bibliai visszautalás (az ítélet) vagy Driver kommentár-helye.
- **M039, M127, M196**: a közbeékelt könyv utáni, abban nem létező fejezetű hely a korábbi könyvet folytatja-e — a mai szabály (bizonytalan) szándékosan óvatos.
- **M060** H6920: a könyvnév nélküli „13:10” (LXX-alak helye) — a forrás nem nevezi meg a könyvet.

## 16. A ⛔ 3.6 jóváhagyása és a 7. lépés (F102.7)

**Orkesztrátori döntés** (local_c8cc3610, a felhasználó felhatalmazásával, 2026-11-09):
- **DT-F102d: (ii)** — a szeletelő marad; az átállás a 2.30-ra az N-F102e javítása után, újraméréssel. Pontosítás a döntési sorban: a (C) a szóráson
  túli különbségre értendő; azon belül a szeletelő marad.
- **Az ítéleti tábla jóváhagyva**, a kérdéses tételekre: M143 kulcs-hiba (nem számít a szeletelő ellen); M018 a mérésből kizárva; M036 és a seed-101
  M162 `forras_hiba`; M091 `forras_hiba`; M214 bibliai (kitöltő-hiba marad); M039, M127, M196: a mai óvatos szabály marad; M060: saját hiba (a
  könyvnév nélküli hely a szócikkben utoljára megnevezett könyvre oldódik, ha egyértelmű; kódváltozás nincs, l. N-F102f).
- **A kapu**: a „próba” jelölés marad, a szó-lapon az új nyers szám CI-vel.

**Ítélet utáni számok, jóváhagyva** (tájékoztató; a nyers szám a kapu, nem változik) *(proveniencia: scope=seed-102 véletlen 200 | forras=naplok/BDB_SZELETELO_M2_seed102_iteletek.md (manual ítélet) + m2_minta_osszevet.py [--szakasztabla] | ts=2026-11-09)*:

| | nyers | ítélet utáni (M018 kizárva, n = 199) | megmaradó saját hiba |
|---|---:|---:|---:|
| seed-102, szeletelő | 183 / 200 (91,5%; CI 86,7–95,0%) | **185 / 199 (93,0%)** | 14 |
| seed-102, szakasztábla | 184 / 200 (92,0%; CI 87,3–95,4%) | **187 / 199 (94,0%)** | 12 (11 + M058 átvett `szakasz`) |

Javítások a nyers számhoz képest: M052 kitöltő-hiba, M036 `forras_hiba`, M143 kulcs-hiba (mindkét kulcsnál +1-1); az M018 kizárva (a szeletelőnél
helyes volt, a táblánál hibás). Szűrés: M060 most szeletelő-hiba (szűrés); M039, M127, M196 nem hiba (a szabály szándékosan óvatos).

**Seed-101 újraszámolva** (a M162 a mai, 1c. szabály szerint `forras_hiba`): a #99 ítéletének állapotán (a F99.25-ös kulcs, 184 nyers) a szeletelő-hibák
13 → **12**, az ítélet utáni szám 187 → **188 / 200 (94,0%)**. A mai tábla állapotán (F102.4, DT-F102a összevetési szabály; nyers 187 / 200) a
megmaradó eltérések: M028, M043, M140, M146, M236, M243, M031, M203, M238 szeletelő-hiba (9), M102, M117, M162 (az 1c. szerint mind `forras_hiba`;
az orkesztrátor a M162-t nevezte meg), M029 (a DT-F102a szerint okafogyott: a kulcs `II` szakasza helyes) → ítélet után **191 / 200 (95,5%)**, ha az
1c. mindhárom `forras_hiba`-ját alkalmazzuk; csak a M162-vel 189 / 200. *(proveniencia: scope=seed-101 | forras=m2_minta_osszevet.py --mai-tabla + naplok/BDB_SZELETELO_M2_seed101_iteletek.md | ts=2026-11-09)*

**7. lépés**: `eszkozok/olvaso_szerver/blokkok.py` `BDB_MERT_PONTOSSAG` → „2026-11-09: 91,5% (95%-os konfidencia-intervallum: 86,7–95,0%)” (a seed-102
nyers száma, a szeletelő); teszt: `teszt_olvaso_szerver.py` `test_bdb_proba_es_mert_pontossag` (91,5%, 86,7–95,0%; a régi 92,0% és az ítélet utáni
93,0% nem áll a lapon). A „próba” jelölés marad.

## 17. A teljes tesztkör (F102.8)

`python eszkozok/teszt_futtat.py` (teljes, a lassú `teszt_szintek.py`-val; WSL, `~/pardes/pardes.db`, az F102.7 állapotán): **11 fájl zöld, 1 hibás** —
`teszt_arculat` 27, `teszt_bdb_vers_jelentes` 38, `teszt_indito` 39, `teszt_kereses` 36, `teszt_megfelelo_kinyer` 27, `teszt_olvaso_szerver` 91 (2 kihagyva),
`teszt_pilot_aranymintaval` 22, `teszt_tanulmany_oldal` 17, `teszt_tervezo` 49, `teszt_ubs_dbh` 6, `teszt_visszhang_kapu` 22 OK; `teszt_szintek` 13 tesztből
**1 FAIL**: `test_heber_szavak_alacsony_es_magas_szinten` (H0120: a `forditasok` adatbeli „H120. adam אָדָם_560 hímnemű f” darab nincs a lapon, mert
a lap a héber szó után U+200E jelet ír: „אָדָם\u200e_560”). **Nem az ág hibája:** ugyanez a teszt a main-en (`e72ef053`, ideiglenes leválasztott
munkafán, ugyanazzal az adatbázissal) ugyanígy bukik; az ág nem érinti sem a renderelést, sem a `forditasok` adatot. → N-F102g.
`python eszkozok/feladatok.py ellenoriz`: 198 brief, 0 hiba, 0 figyelmeztetés.
*(proveniencia: scope=teljes tesztkör | forras=eszkozok/teszt_futtat.py, eszkozok/feladatok.py ellenoriz | ts=2026-11-09)*

## 18. Javítókör 1/2 — ELLENOR_F102 1., 2., 5. (F102.10)

*Az orkesztrátor besorolása és döntései (local_c8cc3610, 2026-11-09) a `naplok/ELLENOR_F102.md` öt tételére.*

- **1. A DT-F102d utólagos átírása — őszintén:** a DT-F102d (C) („a magasabb jelentéspont-szám dönt, döntetlennél a szeletelő”) a seed-102 kitöltése
  ELŐTT rögzült (F102.4). Az eredmény szerint a szakasztábla nyert volna (nyers 184 : 183). Az F102.7-ben a (C) „pontosításaként” beírt „a (C) a szóráson
  túli különbségre értendő” mondat nem a szabály értelmezése volt, hanem az előre rögzített szabály utólagos átírása az eredmény ismeretében. Ezt most
  nyíltan **utólagos eltérésként** rögzítjük (DT-F102g): az orkesztrátor az eredmény ismeretében tért el a (C)-től (ii), mert a különbség (1/200) a
  szóráson belül van; a DT-F102d sorából a pontosítás visszavonva, helyette a DT-F102g-re hivatkozik.
- **2. A brief 4.1 elfogadási feltétele a szeletelőn nem teljesült:** a seed-101 13 szeletelő-hibájából az élő 2.29-ben csak az M130 javult. Egyeztetett
  eltérés (orkesztrátori döntés): a 2.30 által megoldott hat hiba — M028, M043, M140, M146, M236, M243 — tételesen az N-F102e-hez (a szakasztáblára
  való átálláshoz) került; a zárójelentés ezt „nem teljesült, áthelyezve” formában mondja ki. (A többi: M102, M117 az 1c. szerint `forras_hiba`;
  M162 szeletelő-hiba, l. 19.; M031, M203, M238 a 2.30-ban helyes vagy formátumkérdés, szintén a szeletelőben él.)
- **5. A ⛔ 3.1 sorrendje:** az F102.1–F102.2 javítása (H1004 folytatás, öröklés, szűrés, M130) a ⛔ 3.1 megállási javaslata (F102.3, DT-F102d) előtt
  készült; tartalmilag független a rétegválasztástól (hivatkozás-feloldás és a szeletelő fő tagolása, amely mindkét rétegválasztás mellett a 2.29-ben
  marad), de a brief szerint a 2. lépés előtt meg kellett volna állni.

## 19. Javítókör 1/2 — ELLENOR_F102 3.: M036 és M162 szeletelő-hiba (F102.11)

Az orkesztrátor visszavonta a ⛔ 3.6 erre vonatkozó ítéletét (local_c8cc3610, 2026-11-09): a seed-102 **M036** és a seed-101 **M162** (mindkettő H3318)
**szeletelő-hiba**, nem `forras_hiba` — a forrásban van „1 … a. … h.” számozás, csak a „Qal” név hiányzik; a szeletelő a 7947. karakternél (M036) is
`fej`-et ad. A 16. szakasz ezzel ellentétes állítása (M036, M162 `forras_hiba`) és az ott közölt ítélet utáni számok érvényüket vesztik.

**A szakasztábla-kulcson (mérve):** a 2.30 a M036 helyét `-/1/h`-nak adja (`adat/bdb_szakaszok.tsv` H3318 12. sor, `point` „h.”), a vak kitöltés
`Qal/1/h`; a „Qal” nevet a 2.30 nem hordozza, csak a 2.31 `jelolo_hianyzik` kézi sora (H3318 sorszam 3 → `Qal/1`) pótolná. A `--szakasztabla` kulcs a
nyers 2.30-at olvassa, ezért ott is eltérés: **szakasztábla-hiba** (a javítótáblával helyes volna).
*(proveniencia: scope=H3318 | forras=adat/bdb_szakaszok.tsv + adat/bdb_forras_javitas.tsv (grep) + m2_minta_osszevet.py --szakasztabla | ts=2026-11-09)*

**Javított ítélet utáni számok** (tájékoztató; a nyers kapu változatlan: szeletelő 183/200):

| | nyers | ítélet utáni, javítva | maradó saját hiba |
|---|---:|---:|---:|
| seed-102, szeletelő | 183 / 200 | **184 / 199 (92,5%)** | 15 |
| seed-102, szakasztábla | 184 / 200 | **186 / 199 (93,5%)** | 12 (+ M058 átvett `szakasz`) = 13 |
| seed-101, a #99 kulcsán (F99.25; M162 szeletelő-hiba, mint a #99 ítéletében) | 184 / 200 | **187 / 200 (93,5%)** | 13 |
| seed-101, a mai táblán (F102.4; DT-F102a; M029 okafogyott) | 187 / 200 | **188 / 200 (94,0%)**; ha az 1c. szerint az M102 és az M117 `forras_hiba`: 190 / 200 | 12, ill. 10 |

A seed-101 ítéleti fájlja (`naplok/BDB_SZELETELO_M2_seed101_iteletek.md`, #99) az M162-t eleve szeletelő-hibának ítélte (45. sor), és a #102 nem írta
át: nincs mit igazítani (a fájl nincs a #102 `ir`-jében; csak itt jelölve).
*(proveniencia: scope=seed-101, seed-102 | forras=m2_minta_osszevet.py --mai-tabla, [--szakasztabla] + naplok/BDB_SZELETELO_M2_seed10{1,2}_iteletek.md (manual ítélet) | ts=2026-11-09)*

## 20. Javítókör 1/2 — ELLENOR_F102 4.: az M091 indoklása (F102.12)

A 15. szakasz (és a ⛔ 3.6 ítéleti fájl) állítása — „a TAHOT itt nem dönt (az arámi Strong a kivonatban nem illeszkedik: 0 találat mindkét versre)” —
**hamis és proveniencia nélküli volt** (egy `grep` a Strong-szám rossz alakjával, nem a projekt lekérdezése; a CLAUDE.md 1. és 3. szabályának
megsértése). A lekérdezés:

- `python eszkozok/lekerdez.py scan H2370 --szakasz "Dán 2:41"` → 1 igehely, 2 szó-előfordulás
  *(proveniencia: scope=range:Dán 2:41 | forras=TAHOT_kivonat.tsv | strong=H2370 | n=1 | ts=2026-11-09T17:15Z)*
- `python eszkozok/lekerdez.py scan H2370 --szakasz "Ezsd 2:41"` → 0 igehely
  *(proveniencia: scope=range:Ezsd 2:41 | forras=TAHOT_kivonat.tsv | strong=H2370 | n=0 | ts=2026-11-09T17:15Z)*

A TAHOT tehát dönt: a hely Dán 2:41, a forrás „Ezra 4:20”-a könyvnév-hiba; az ítélet (`forras_hiba`) nem változik, csak az indoklása.

## 21. Javítókör 2/2 — ELLENOR_F102_2 1.: az M036 szakasztábla-oldala `forras_hiba` (F102.17)

Az ELLENOR_F102 3. orkesztrátori döntése (M036 és M162 szeletelő-hiba) **csak a szeletelő-oldalra szólt**; a 19. szakasz ezt a szakasztábla-kulcsra is
kiterjesztette, ami túllépés volt. Visszaállítva: a szakasztábla-oldalon az M036 **`forras_hiba`** — a 2.30 a hely számozását hordozza (`-/1/h`, H3318
12. sor), csak a forrásban hiányzó „Qal” törzsnevet nem; ezt a 2.31 `jelolo_hianyzik` kézi sora pótolja (H3318 sorszam 3 → `Qal/1`), ez az 1c.
`forras_hiba` osztálya. A szeletelő-oldal marad szeletelő-hiba (a szeletelő a számozást sem látja: `fej`).

**Ellenőrző számolás (szakasztábla-kulcs, seed-102):** nyers 184 / 200 egyezés; az M018 kizárva (a táblánál eltérés volt) → 184 / 199; javítás a
nyershez: M052 (kitöltő-hiba) +1, M036 (`forras_hiba`) +1, M143 (kulcs-hiba) +1 → **187 / 199 (94,0%)**. A maradék 12 eltérés: 11 szakasztábla-hiba
(M002, M042, M056, M194, M198, M201, M221, M223, M226, M233, M242) + M058 (a 2.29-ből átvett `szakasz`); 187 + 12 = 199. A szeletelő: nyers 183 → az
M018 kizárva (ott egyezett) 182 / 199; + M052, + M143 → **184 / 199 (92,5%)**; maradék 15 szeletelő-hiba (M003, M009, M011, M016, M027, M034, M036,
M042, M050, M058, M205, M208, M223, M233, M249); 184 + 15 = 199.
*(proveniencia: scope=seed-102 véletlen 200 | forras=m2_minta_osszevet.py [--szakasztabla] + naplok/BDB_SZELETELO_M2_seed102_iteletek.md (manual ítélet) | ts=2026-11-09)*

## 22. Javítókör 2/2 — ELLENOR_F102_2 3.: a brief 4.1 nem teljesült helyei, mind nyitott tételben (F102.19)

A brief 4.1 elfogadási feltétele (a seed-101 13 szeletelő-hibája a táblában a jóváhagyott ítélet szerint, teszttel) **10 helyen nem teljesült**:
M028, M043, M140, M146, M236, M243, M203, M238 → **N-F102e** (a 2.30 megoldja; a szakasztáblára való átállással zárul); M031, M162 → **N-F102h** (a
szeletelő törzsfejléc-osztálya). Az M102 és az M117 `forras_hiba` (1c.); az **M130 javult** (F102.2). Orkesztrátori döntés (local_c8cc3610, 2026-11-09):
mind a tíz nyitott tételben áll; a zárójelentésnek ki kell mondania: „nem teljesült, áthelyezve”.
