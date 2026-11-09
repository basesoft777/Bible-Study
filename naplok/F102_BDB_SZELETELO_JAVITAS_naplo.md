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
