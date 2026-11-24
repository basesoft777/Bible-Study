---
feladat: 241
cim: A lapgenerátor újraírása, 3. rész — átállás az új lapgenerátorra (218c)
kod: GENERATOR_UJ_C
tipus: feladat
fazis: folyamat
modell: opus
sav: CONTENT
munka: folyamat
allapot: fut
ag: claude/f241a-kiadasi-ut
pr: 841
ad: a lexikonlapokat az új lapgenerátor (eszkozok/lapgen/) adja ki: az ISTENTISZT-001 2. kiadása és a HAMART-001 új generátoros kiadása megvan, a kiadás mód a jóváhagyás frissességét a kézi rések és az adat hash-éből méri, a lapszövegre kereső kapuk a lapmodellen dolgoznak, a TEREMT-001 generátoroldalról kiadható, a régi generátor (lexikon_general) egy kiadásnyi visszaút után archívumban van
kovetkezo: "Folytatás: F241.4 (licenckapu, N223) az A szelet ágán (claude/f241a-kiadasi-ut); az F241.0–F241.3 kész, a D9–D12 a döntésfájlban (D11: új lépés F241.5b), átadó: naplok/F241_atado_F241.3.md"
olvas: ["tematikus_lezart/HAMART-001*", "tematikus_lezart/naplok/HAMART-001*", "tematikus_lezart/ISTENTISZT-001*", "tematikus_lezart/naplok/ISTENTISZT-001*", eszkozok/lapgen/, eszkozok/lexikon_general.py, eszkozok/general.py, adat/, konkordancia/, motivumok/HAMART-001.md, motivumok/ISTENTISZT-001.md, motivumok/TEREMT-001.md, "motivumok/naplok/HAMART-001*", "motivumok/naplok/ISTENTISZT-001*", lexikon/HAMART-001_TUDOMANYOS.md, lexikon/HAMART-001_KIZARASOK.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, naplok/F218_jelentes.md, naplok/F218_folytatas.md, naplok/HIBA_MECHANIZMUSOK.md, .claude/commands/kiadas.md]
ir: [eszkozok/lapgen/, eszkozok/lexikon_general.py, eszkozok/general.py, eszkozok/torzscikk_general.py, eszkozok/nyilt_mag_export.py, eszkozok/olvasoi_kapu.py, eszkozok/ellenoriz.py, eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/allitas_adat.py, eszkozok/generalt_nezetek.py, eszkozok/feladatok.py, eszkozok/f127_res_eles.py, eszkozok/glossza_lexikon_forditas.py, eszkozok/jelolt_eloszures.py, eszkozok/kiejtes_szoveg.py, eszkozok/lap_javit_proba.py, eszkozok/lektor_kerdesek.py, eszkozok/lexikon_v2_migracio.py, eszkozok/motivum_hatar.py, eszkozok/render_diff_osztalyoz.py, eszkozok/szakasz_cimke_levezet.py, eszkozok/tsk_versszam_felmeres.py, eszkozok/visszhang/megfelelo_kinyer.py, eszkozok/olvaso_szerver/teszt_olvasoi_merce.py, eszkozok/olvaso_szerver/teszt_visszhang_kapu.py, eszkozok/teszt_bdb_tagolas.py, eszkozok/teszt_dontes_allapot.py, eszkozok/teszt_ellenoriz_11.py, eszkozok/teszt_ellenoriz_31.py, eszkozok/teszt_ellenoriz_35.py, eszkozok/teszt_ellenoriz_vedokorlat.py, eszkozok/teszt_f194_szopar.py, eszkozok/teszt_f212_cs3.py, eszkozok/teszt_feladatok.py, eszkozok/teszt_futtat.py, eszkozok/teszt_gorog_rovid_jelentes.py, eszkozok/teszt_gyokerok_kapuk.py, eszkozok/teszt_hatastortenet.py, eszkozok/teszt_kesz_lap_hamart.py, eszkozok/teszt_lexikon_adatres.py, eszkozok/teszt_olvasoi_kapu.py, eszkozok/teszt_sablon_javitokor.py, eszkozok/teszt_szerepmatrix.py, eszkozok/teszt_szotari_gerinc.py, eszkozok/bdb_jelolt/hu_illeszt.py, eszkozok/lxx_versszintu_import.py, eszkozok/thayer_jelolt/vers_jelentes.py, .github/workflows/feladatok.yml, .github/workflows/ellenorzes.yml, adat/bdb_szakasz_hu.tsv, adat/bdb_vers_jelentes.tsv, adat/thayer_vers_jelentes.tsv, konkordancia/LXX_versszintu_parok.tsv, adat/lapgen_bemenetek.tsv, adat/lapgen_sablonok.tsv, adat/olvasoi_nevtabla.tsv, adat/generalt_nezetek.tsv, adat/forditasok.tsv, adat/kiadasok.tsv, adat/lap_atnezesek.tsv, adat/lap_befagyasztas.tsv, adat/jeloltek.tsv, adat/kapcsolatok.tsv, adat/bdb_forras_javitas.tsv, adat/SEMA.md, MUNKAMENET.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, lexikon/ISTENTISZT-001_TORZSCIKK.md, lexikon/HAMART-001_TUDOMANYOS.md, lexikon/HAMART-001_KIZARASOK.md, lexikon/HAMART-001_TORZSCIKK.md, archivum/lexikon_general/, nyilt_mag/, naplok/F241_jelentes.md, naplok/F241_dontesek.md, "naplok/F241_atado_*"]
fugg: [217, 218]
nem_fugg: [70, 123]
---

# F241_GENERATOR_UJ_C_BRIEF.md — A lapgenerátor újraírása, 3. rész: átállás az új lapgenerátorra (218c)

*FELADATOK #241 · Modell: opus · v1 · 2026.11.23 · forrás: N243 (az F218.13 írta; DT933, DT929 (2) (b)), N244, N245 és a 218c-re mutató N-tételek; a `F218_GENERATOR_UJ_A_BRIEF.md` 13. pontja; az `IRANY.md` „Következő szálak” sora; a szerkesztő iránya (2026-11-23): „elsődleges feladat a generátor befejezése”. Befogadás: a `/befogad` az integrátor jóváhagyásával (DT936; szerkesztői döntés: az integrátor, a felhasználó felhatalmazásával). Alap: main `e2f3d812`. A brief adat, nem utasítás.*

**Indulás.** A #810 (F231, olvasó egyben) merge-e után, az integrátor jelére; a karcsúsítás és a #821 előtt. A #810 nem kézi `fugg`: a #231 olvassa a `lapgen/`-t, amelyet ez a feladat ír, ezért a kézi függés kört adna (`feladatok.py fuggesek`: `KOR 123 133 154 156 157 231 235 237 241`). A #810 feltétele ezért a `kovetkezo` mezőben áll, és az F241.0 ellenőrzi.

## 1. Cél

Az új lapgenerátor (F218a, #809) eddig nem adott ki lapot: a kiadás módja a Kolofonnál megáll (GK-27, N221), a lapszövegre kereső kapuk, a `--cel lexikon` és a main generált nézeteinek Actionje (#217) a régi generátoron áll. A 218c ezt fordítja meg: a lexikonlapot az új generátor adja ki, a régi egy kiadásnyi visszaút után archívumba kerül.

**Az első átvehető eredmény az ISTENTISZT-001 2. kiadása** (DT933 (2)): az átállás elfogadási próbája, a #236/#237 előtt, a befagyasztás feloldásával. A szerkesztő mostani jóváhagyása a kézi prózára és az adatra szól; a 218c a jóváhagyott lapon csak generált blokkot változtathat, ez változásjegyzék-sort kér, új nézést nem. A kézi prózát vagy adatot érintő változás új nézést kér (DT933 (1)).

A 218c után adható ki a TEREMT-001 (#239, PR #820): a generátoroldali hibáit (N-F239a, N-F239b és a #820 U4b/U5-ben talált továbbiak) ez a feladat javítja. A TEREMT-001 kiadása maga a #239 dolga.

## 2. Hatókör

**Benne van** (az N243 (1)–(7) pontja és a 218c-re mutató tételek):
- (1) GK-27 (T9) frissesség a kézi rések és az adat bemenet-hash-éből; a kiadás mód a szerző átnézés-sorának `lap_commit`-jával (N221; DT933 (1)).
- (2) A #217 jegyzékének G01/G02 sora, a `bemenetek` oszlop (a `lapgen_bemenetek.tsv` B-azonosítói), az E28 és a `feladatok.yml` Action az új generátorral; a `--cel lexikon` az újra mutat.
- (3) A lapszövegre kereső kapuk átírása a lapmodellre (`olvasoi_kapu.py`, az `ellenoriz.py` lapszöveg-szabályai, E38, E39; HN-17: a „3. LXX” előtagú kapu), a fogyasztóikkal egy commitban.
- (4) Visszaút: a régi generátor egy kiadásig `--cel lexikon_regi` néven fut; archiválás csak utána, fogyasztónként, az `archivum/lexikon_general/` alá, `ARCHÍV` fejléccel, a hivatkozások frissítésével (E27).
- (5) GK-20 (a TORZSCIKK a lapmodellből), B62 (a `nyilt_mag_export` körkörös függése), B49 (a lektor-sor a `kiadasok.tsv`-be), O4 (a `fordit.py`/`emeles.py` sorsa, mérés után); a leltár C3 és C9 sora.
- (6) N188, N221, N223, N234, N235, N236 (a 2. pont korlátjával), N241, N242, N244, N245; N-F239a, N-F239b és a #820-ban ezután felvett N-F239c… tételek (bemenet, l. 6. pont).
- (6a) Az ISTENTISZT-001 2. kiadásának `/kiadas`-lépésében a 3/b olvasói átolvasás kötelező, a teljes lapon (DT824; az új generátor szinte minden generált blokkot megváltoztatott).
- (7) A valódi függések rendezése (l. „Függésszámítás”).

**Nincs benne:**
- A 218b (#236) és a B0 (#237): külön tétel. A levezetett függés szerint mindkettő e feladat után jön (a `lapgen/` és a `lapgen_bemenetek.tsv` közös), ez megfelel a DT933-nak.
- A befagyasztott lapok (KIRALY, ALVIL, MENNY, ANTROP, HODIT, TEREMT-002; `adat/lap_befagyasztas.tsv`: „új cikkként, nulláról készül újra”) újragenerálása. Ezek a régi generátor kimenetével, befagyasztva maradnak, és nulláról, az új generátorral készülnek újra (#123). Ezért az N236-ból (a 3. szakasz többi jelölésfajtája) csak az kerül ide, amit a három átálló lap (ISTENTISZT-001, HAMART-001, TEREMT-001) használ; a többi jelölésfajta a nulláról írt cikkek dolga (⛔ B1, l. 7. pont).
- A TEREMT-001 kiadása (#239), új próza, új motívum.
- A `CLAUDE.md` szövege: a `lexikon_general` említése ott csak a szerkesztő szavára változik (Munkamód; a kérés az integrátoron át megy).
- A `naplok/` régi mérőszkriptjei (`naplok/F09_*.py`, `F12_kitoltes.py`, `F123_*.py` …), amelyek a `lexikon_general`-t importálják: napló, nem fogyasztó; az archiválás után nem futtathatók, és ezt a jelentés kimondja.

## 3. Munkarend

- **Modell-ellenőrzés** minden session első lépése (`CLAUDE.md`).
- **Döntésfájl:** `naplok/F241_dontesek.md` (MUNKAMENET „Szereposztás”): az integrátor minden döntése teljes szöveggel, sorszámmal (`D1`, `D2` …); a session a fájl aktuális állapotát hajtja végre, lépéshatáron és commit előtt újraolvassa. A befogadás döntései is ide kerülnek, az F241.0-ban.
- **Kérdések:** a ⛔ pontok és minden tartalmi kérdés `SendMessage`-dzsel az integrátornak (az indító session); technikai kérdésben (megvalósítás, teszt, ágkezelés, sorrend a feladaton belül) a session dönt, és a jelentésbe írja (DT920).
- **Egy lépés = egy kis commit / tétel** (`F241.<n>: …`); a nagy lépés `F241.<n>a`, `b` … alszeletekre bomlik.
- **Szeletek és PR-ok.** Három szelet, mindegyik saját ágon, saját kis draft PR-ral (az F218a S-szeleteinek mintájára): **A** (F241.0–F241.7, a kiadás útja és az ISTENTISZT-001 2. kiadása), **B** (F241.8–F241.12, a TEREMT-001 kiadhatósága, a HAMART-001 kiadása, a teljes kapuforma), **C** (F241.13–F241.15, archiválás és zárás). A PR első sora: Mérce · Állapot · Következő · Akadály. A brief fejlécének `ag`/`pr` mezője az aktuális szeletét viszi; a `lezar` mező szeletenként bővül azokkal az N-tételekkel, amelyeket a szelet PR-ja teljesít (a befogadáskor üres, hogy a befogadó PR merge-e ne zárjon le semmit).
- **Kontextus-plafon (Munkamód 10):** kb. 150–200 ezer token kontextusnál csere vagy tömörítés, a végrehajtó subagenteknél is. Minden lépéshatáron átadó jegyzet: `naplok/F241_atado_<lépés>.md` (állapot, a nyitott ⛔-k, a következő lépés, a döntésfájl hivatkozása).
- **Egyszerre egy lapgen-tesztfutás a gépen** (Munkamód 7; 3–4 GB futásonként): nehéz futás előtt a `python.exe`-folyamatok listája; más session folyamatát soha nem állítod le. A TEREMT-001 (#820) előnézete is lapgen-futás: ütközésnél vársz.
- **Nehéz kör (DT919):** a feladat generátort, adatot és kiadott lapot érint, ezért szeletenként **egy `fuggetlen-ellenor`-futás és legfeljebb egy javítókör**; a teljes `python eszkozok/push_elott.py` minden szelet PR-ja előtt. A jelentés: `naplok/F241_jelentes.md` (BRIEF_SABLON „Jelentés”).
- **Generált hibát a generátorban javítunk, kapuval** (a hiba oka, nem a példány); a `lexikon/` kézzel nem szerkeszthető.
- **Fordítás:** az N244 fordításait a végrehajtó session maga készíti (előfizetés), API-keretet (`forditas/bdb_api`, `forditas/thayer_api`) nem használ; a nyelvközi egység szabályával (a héber és a görög azonos fogalma azonos magyar szóval).

## 4. Lépések (⛔ a kötelező megállások)

### A szelet — a kiadás útja és az ISTENTISZT-001 2. kiadása

- **F241.0 — Indítás.** Modell-ellenőrzés. Előfeltételek, mind igazolva a jelentésben: a #809 és a #810 a main-en; az integrátor jele megvan; a #820 ágának (`claude/nervous-kare-9d2361`) vagy már a main-nek `nyitott/uj/nervous-kare-9d2361.md` / `NYITOTT_FELADATOK.md` fájljából az N-F239a, N-F239b és a további N-F239-tételek beolvasva, listájuk a jelentésben (ha a #820 közben merge-elt, a végleges számukkal). `python eszkozok/feladatok.py fuggesek` a mai állapotra; ha a fejléc függései változtak, a fejléc frissül. A döntésfájl megnyitása a befogadás döntéseivel. A `lexikon_general` fogyasztóinak leltára (import és hívás, a `naplok/` nélkül) a jelentésbe; ha a lista bővebb, mint az `ir`, ⛔ (az `ir` bővítése az integrátor döntése, N188 tanulsága).
- **F241.1 — Kiadás mód és frissesség (N221; DT933 (1); GK-27, T9).** A jóváhagyás frissessége a kézi rések és az adat bemenet-hash-éből (nem a teljes lap bájtjaiból); a kiadás mód a szerző átnézés-sorának `lap_commit`-ját veti össze a lap mai utolsó commitjával, egyezés nélkül BUKÁS. Generált blokk változása → változásjegyzék-sor, nem új nézés; kézi próza vagy adat változása → új nézés. Kapu: `lapgen/szamitas/kolofon.py` `kapu`; teszt: `teszt_kolofon.py` `Jovahagyas` (mindhárom ágra: egyező, csak generált változás, kézi/adat-változás).
- **F241.2 — Célnév és Action (N243 (2), (4) első fele).** A `--cel lexikon` az új generátorra; a régi `--cel lexikon_regi` néven fut a visszaútig. A #217 jegyzékének (`adat/generalt_nezetek.tsv`) G01/G02 sora az új generátorra, a `bemenetek` oszlop B-azonosítókra; az E28 és a `feladatok.yml` az újjal. **Korlát:** a kiadott lap új kiadás nélkül nem változhat (E28); ezért a lap motívumonként, a saját kiadásával egy commitban áll át (a megvalósítás módja technikai, a session dönti el, pl. a jegyzékben motívumonkénti generátor); a befagyasztott lapok érintetlenek. A fogyasztókkal egy commitban.
- **F241.3 — Lapszöveg-kapuk a modellre (N243 (3)).** `olvasoi_kapu.py`, az `ellenoriz.py` lapszöveg-szabályai, E38, E39, HN-17 („3. LXX” előtag): a modellen dolgoznak, a fogyasztóikkal egy commitban. Ide kerül az **N-F239b** is (az olvasói kapu kivétele a „Szakirodalom” sor dőlt, eredeti nyelvű műcímére, a jelölés vagy a forrás-tábla szerint, gépi teszttel), mert ugyanaz a fájl.
- **F241.4 — Licenckapu (N223).** Minden licencleltár-forrás, amelynek adata a lapon látszik, és a `kotelezo_megjeloles` mezője nem üres, szerepel a Kolofon forrásmegjelölésében; kapu és teszt. ⛔ **A megjelölendő halmaz bővítése** (DT911 3. (b): TBESH/TBESG, Strong-szótár, MACULA, SBLGNT-apparátus, javított Károli-KH (MEK) …): a session méréssel listát ad (forrás, licenc, látszik-e a lapon), a bővítést az integrátor dönti el.
- **F241.5 — Az ISTENTISZT-001 hiányzó fordításai (N244).** A 34 „fordításra vár” jel (a 4. szakasz SDBH/UBS-glosszái és doménnevei, a H7121, a H8034 és a G1941 kártyái) pótlása az `adat/forditasok.tsv`-ben (B14), az előfizetésből, a nyelvközi egység szabályával, proveniencia-sorral; utána a lap 0 „fordításra vár” jellel generálódik. ⛔ ha egy fordítás a nyelvközi egység miatt meglévő, kiadott fordítást írna át (az másik lapot is érint).
- **F241.6 — Független ellenőrzés (A szelet).** `fuggetlen-ellenor` az A szelet base..head diffjén, legfeljebb egy javítókör (`/elteres`).
- **F241.7 — Az ISTENTISZT-001 2. kiadása (DT933 (2)).** Generálás az új generátorral a `lexikon/` végleges helyére, kiadás módban; a befagyasztás feloldása (`adat/lap_befagyasztas.tsv`). A `/kiadas ISTENTISZT-001` menete a 2. kiadásra, **a 3/b olvasói átolvasással a teljes lapon** (kötelező, N243 (6a); friss kontextusú olvasó, brief és döntéslista nélkül; a `naplok/HIBA_MECHANIZMUSOK.md` lapot érintő nyitott mechanizmusai mind ellenőrizve). Talált generált hiba: a generátorban javítva, kapuval, célzott újraellenőrzéssel (hibahely-tábla + diff). A lektor-sor a `kiadasok.tsv`-be (B49), a változásjegyzék-sor és a kiadásszám a `kiadasok.tsv`-ből (SEMA 2.46). ⛔ **ha a 3/b vagy a javítás kézi prózát vagy adatot érint:** új nézés kell (DT933 (1)): az integrátoron át a szerkesztőhöz, a hibahely-táblával. ⛔ **a kiadás sora előtt:** az integrátor jóváhagyása (a 3/b eredménye, a változásjegyzék, a nézett commit hash-e). A TORZSCIKK (GK-20) itt még a régi úton készül, ha az F241.11 előtt kell; ezt a jelentés kimondja.

### B szelet — a TEREMT-001 kiadhatósága, a HAMART-001 kiadása, a teljes kapuforma

- **F241.8 — A TEREMT-001 generátorhibái.** **N-F239a** (a 3. szakasz arány-mondata a legfeljebb 10-szeres arányra: nyelvi mondat vagy a mondat elhagyása, a generátorban, gépi kapuval; a `kizart.py` ideiglenes kerülőútja megszűnik) és a #820 U4b/U5-ben talált **N-F239c…** tételek (bemenet; a lista az F241.0-ból). Az **N236**-ból az, amit a TEREMT-001 3. szakasza használ (sablonmondat a régi lap szövege szerint). ⛔ **minden új sablonmondat** (`adat/lapgen_sablonok.tsv`) az integrátor jóváhagyásával (a sablontáblát a szerkesztő hagyja jóvá, F218a 6. pont; az integrátor dönt vagy továbbadja). Ellenőrzés: a TEREMT-001 előnézete kerülőút nélkül generálódik, és a #820 ágán a lapgen-kapuk zöldek (a #820 fájljaihoz nem nyúlsz).
- **F241.9 — A kézi adat csupasz Strong-számai (N235, N242).** A HAMART-001 két csoportos indoklása (N235: „csoportos kizárás (a רַע (ra) és a קָלַל (kálal) csoportjának mintájára)”), a 16 TSK-kizárás-cella (N242 A), az 57 Károli-csoport blokk-sor a generáló szkripttel együtt (N242 B), az ISTENTISZT-001 1Móz 4:26 → 2Móz 33:19 kapcsolat-cellája (N242 D; ⛔ B3 szerint). Minden javított tétel ki az `alakosztaly.ISMERT_CSUPASZ_STRONG`-ból és a `teszt_kapuk._S9C_LELTAR` másolatából; a HAMART-diff új engedélysorai a nézésre mennek.
- **F241.10 — A HAMART-001 új generátoros kiadása.** A HAMART-001 a saját kiadásával egy commitban áll át (F241.2 korlátja). Mivel az F241.9 adatot változtat, ⛔ **új nézés kell** (DT933 (1)): az ágas lap és a hibahely-tábla az integrátoron át a szerkesztőhöz; a kiadás sora csak a nézés után. A `/kiadas` 3/b olvasói átolvasása itt is kötelező (DT824).
- **F241.11 — Teljes kapuforma.** **N234** (GK-04 `hely_egyseg`: a szópár-név → Strong-tagok feloldása a bemeneti rétegben; a `teszt_vaz.py` skipje megszűnik); **N241** (GK-03 teljes forma, mind az öt pont: `hu_illeszt.py` B18, `lxx_versszintu_import.py` B36, `vers_jelentes.py` B21, a B19 jegyzéksorai, a B38 ellenőrzése; a táblák újragenerálása; `teszt_bemenet.Gk03Pillanatkep` bővítése); a leltár **C3, C9** (a `teszt_kapuk.Leltar` skipjeinek feloldása, vagy kimondott „nem portolandó” egy sor indokkal). Ha a táblák újragenerálása kiadott lapot változtat: generált blokk → változásjegyzék-sor; adat → ⛔ nézés. **Ütközés:** a „kis adatjavítás” szál (a görög LXX-párok 88 hamis „hajnalcsillag”-ja, N-F231a) ugyanazt a B36 táblát (`konkordancia/LXX_versszintu_parok.tsv`) írja; a sorrendet az integrátor dönti el (⛔ B4).
- **F241.12 — Törzscikk és nyílt mag (GK-20, B62, O4).** A TORZSCIKK a lapmodellből; a `nyilt_mag_export` körkörös függése feloldva; az O4 (`fordit.py`/`emeles.py`) mérés után: megmarad, átkötve vagy archívumba, egy sor indokkal. Utána a független ellenőrzés (B szelet), legfeljebb egy javítókör.

### C szelet — visszaút lezárása, archiválás, zárás

- **F241.13 — Archiválás (N243 (4)).** Feltétel: az ISTENTISZT-001 2. és a HAMART-001 új kiadása a main-en (ez a „visszaút egy kiadása”). Fogyasztónként, kis commitokban (az F241.0 leltára szerint): a hívott függvények a helyükre (a `lapgen/` vagy saját modul), a teszt átkötve vagy kimondottan kivezetve; végül a `lexikon_general.py` az `archivum/lexikon_general/` alá, `ARCHÍV` fejléccel; a `--cel lexikon_regi` megszűnik; a hivatkozások frissítése ugyanabban a commitban (`FELADATOK.md`, `NYITOTT_FELADATOK.md`, a briefek `olvas` mezője; E27). A `CLAUDE.md` említése: ⛔ az integrátoron át a szerkesztőhöz. A befagyasztott lapok a régi kimenetükkel maradnak, az E28 nem méri őket újra (a `lap_befagyasztas` útja).
- **F241.14 — A régi javító lépés és a függési kör (N245, N188).** N245: a régi generátor kivezetésével a rossz sorrendű `heber_sorrend_javit`-hívás a lapon megszűnik (az olvasóban a #810 javította); igazolás: a 4Móz 16:30 H0127 alakja a kiadott lapokon. A H4480 Ezsd 9:11 („מֶּה”) hiányzó kulcsa a `bdb_forras_javitas.tsv`-be, ha a Biblia igazolja (különben egy sor indokkal elvetve). N188: a #218 `ir`-en kívüli írásainak függési köre a 218c fejlécével rendezve; a jelentés kimondja, hogy a kör megszűnt (`feladatok.py fuggesek`: nincs `KOR` a 241-gyel).
- **F241.15 — Zárás.** Független ellenőrzés (C szelet), legfeljebb egy javítókör; teljes `push_elott`; a jelentés „Zárás” szakasza (mi készült, a kiadások, a lezárt N-tételek, a mérések, a nyitott pontok); a `lezar` mező a teljes listával; a fejléc `allapot`-ja és `kovetkezo`-ja: „Te: a draft PR áttekintése és merge-e”.

## 5. Elfogadási feltételek

1. Az ISTENTISZT-001 2. kiadása a main-en, az új generátorral, 0 „fordításra vár” jellel, a 3/b olvasói átolvasás kérdéslistájával és hibahely-táblájával a jelentésben; a kiadás mód kapuja a `lap_commit`-tal zöld.
2. A HAMART-001 új generátoros kiadása a main-en, a szerkesztő nézése után; a GK-24 ismert eltérés-listája (`ISMERT_CSUPASZ_STRONG`) üres.
3. A `--cel lexikon`, az E28, a `feladatok.yml` és a #217 jegyzék az új generátoron; a lapszöveg-kapuk a modellen; a licenckapu zöld.
4. A TEREMT-001 előnézete kerülőút nélkül generálódik; az N-F239a/b/c… lezárva vagy egy sor indokkal elvetve.
5. A `teszt_vaz.py` GK-04 és a `teszt_kapuk.Leltar` C3/C9 skipje megszűnt, vagy kimondott indokkal áll.
6. A `lexikon_general.py` az `archivum/lexikon_general/` alatt, `ARCHÍV` fejléccel; a fogyasztók átkötve; a `feladatok.py ellenoriz` és a CI zöld.
7. Szeletenként egy független ellenőrzés a jelentésben, legfeljebb egy javítókör; a 218c-re mutató N-tételek mindegyike lezárva, elvetve egy sor indokkal, vagy az integrátor döntésével máshová mutatva.

## 6. Bemenet a #820-ból

A TEREMT-001 3/b átolvasásában (#239, U4b/U5) talált generátorhibák N-tételei a `nyitott/uj/nervous-kare-9d2361.md`-be kerülnek, a PR #820 ágán (`claude/nervous-kare-9d2361`). A befogadáskor fent van: **N-F239a** (a 3. szakasz arány-mondata) és **N-F239b** (az olvasói kapu és a szakirodalmi műcím). A továbbiak helyőrzője: **N-F239c…** (a következő betűk). A befogadás nem vár rájuk; az F241.0 beolvassa őket, és ha generátorhibák, az F241.8-ba kerülnek. Ha egy tétel nem generátorhiba (próza, adat a #239 fájljaiban), az a #239-é marad.

## 7. Döntések a befogadáskor (⛔, az integrátoré)

- **B1 — Az N236 hatóköre.** Javaslat: csak az átálló három lap jelölésfajtái; a többi a befagyasztott motívumok nulláról írt cikkeivel (#123). Az N236 így részben a #123-ra mutat.
- **B2 — `nem_fugg: [70, 123]`.** Az N243 (7) a #70-et és a #123-at valódi függésnek nevezi (a mérce-motívumok forrása). A #70 befagyasztva vár, a #123 megállt, és maga is az új generátort várja; kézi függésként a 241 nem indulhatna. Javaslat: `nem_fugg`, mert a 241 a motívumfájlokat csak olvassa, a jóváhagyott állapotukban; ha közben a #70 vagy a #123 elindulna, a motívumfájlon egyszerre egy feladat fut (D39).
- **B3 — Az N242 D (ISTENTISZT-001, 1Móz 4:26 kapcsolat-cella).** Javaslat: az ISTENTISZT-001 2. kiadásába (F241.7), egysoros célzott nézéssel; különben a 2. kiadás csupasz Strong-számmal jelenik meg, és egy 3. kiadás kell.
- **B4 — A „kis adatjavítás” szál és az F241.11 sorrendje** (közös tábla: `konkordancia/LXX_versszintu_parok.tsv`). Javaslat: a kis adatjavítás előbb, mert a hamis tartalmat javítja; az F241.11 utána generálja újra a táblát.
- **B5 — A #236/#237 sorrendje.** A levezetett függés szerint mindkettő a 241 egészét várja. Javaslat: elfogadni (a `lapgen/` közös, két ág nem ír egy fájlba).

## 8. Döntésnapló

A befogadás és a menet döntései: `naplok/F241_dontesek.md` (sorszám, dátum, kérdés – döntés – indok, a szerkesztő szava, ha van). A `DONTESEK.md`-be menő döntés ezen felül a `dontesek/uj/<ágnév>.md`-be is (helyőrzővel, `DT-F241a` …).

## Függésszámítás (ideiglenes fejléccel, a main `e2f3d812`-n, 2026-11-23)

`python eszkozok/feladatok.py fuggesek --extra <fejléc>`: `KOR` nincs; `FUGGES 241 217 kezi`, `FUGGES 241 218 kezi`. A 241-et váró levezetett függések (a 241 által írt fájlt olvassák): #7, #10, #75, #81, #86, #106, #123, #129, #133, #138, #153, #154, #156, #157, #205, #229, #231, #234, #236, #237 — mind lezárt, nem induló, megállt vagy döntésre váró; a #231 a #810 merge-ével lezárul. A #810-zel kézi függés kört adna (`KOR 123 133 154 156 157 231 235 237 241`), ezért a feltétele a `kovetkezo` mezőben áll. Az N243 (7) további nevei: #212, #178, #181, #203 lezárva (nincs hatásuk), #70 és #123 a B2 szerint: `nem_fugg` nélkül `FUGGES 241 70` (a `motivumok/ISTENTISZT-001.md`) és `KOR 123 156 157 241` adódik. Ellenőrzési szint (`feladatok.py szint`): `teljes`, 2 kör; ez a brief szeletenként legfeljebb egy javítókört enged (takarékos irány).
