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
