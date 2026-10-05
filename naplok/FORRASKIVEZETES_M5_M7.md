# FORRASKIVEZETES M5 és M7 — az LXX_kivonat kivezetése és a render-diff

*Brief: `F42_FORRASKIVEZETES_BRIEF.md` · ág: `claude/forraskivezetes` · 2026-10-05. Mérések: `manual` (saját mérőszkriptek és `eszkozok/lxx_osszevetes.py`), ahol nem `lekerdez.py`-kimenet.*

## M5 — az LXX_kivonat kivezetése (DT-F42f)

**(f1) 2 Esdras és görög Eszter.** `lxx_os_import.py`: `karoli_esdras_eszter()` (2 Esdras 1–10 = Ezsd, 11–23 = Neh; a Károli-kulcs az `igehely_kjv` oszlopból és a `Karoli_versmegfeleltetes.tsv`-ből; fejezethatár-eltolódásnál a KJV-hivatkozás a mérvadó, pl. 2 Esdras 13:33–37 = Neh 4:1–5, 20:1 = Neh 9:38), `karoli_ok=versmegfeleltetes_tabla`. Letöltés nélkül: `python eszkozok/lxx_os_import.py --ujrabesorol` (ugyanaz a függvény, mint a teljes importban). Az Eszter-betoldások és az 1 Esdras kulcs nélkül maradtak.

| Könyv | Károli-vers | LXX_OS-kulcsolt | Nem kulcsolt (a görög forrás nem tartalmazza) |
|---|---|---|---|
| Ezsd | 280 | 280 | — |
| Neh | 406 | 392 | 3:7, 4:6, 11:16, 11:20–21, 11:28–29, 11:32–35, 12:4–6 |
| Eszt | 167 | 163 | 1:1, 4:6, 9:5, 9:30 |

Idegen (Károlinál nem létező) kulcs nincs. Az `lxx-hid` a nem kulcsolt versekre explicit üres eredményt ad (pl. `Neh 3:7`, n=0), nem tölt ki.

**(f2) Elsődleges változat** (`ELSODLEGES_SLUG`, a `LXX_OS/README.md`-ben rögzítve): Józs `joshua-vaticanus-b`, Bír `judges`, Dán `daniel-theodotion`; a másik változat megmaradt. Következmény a HODIT-001 oldal Józs-soraira: 5 sor `szamozas_elteres` → `kutatói azonosítás függőben` (a Vaticanus-fájl kulcsolja a verseket).

**(f3) Teljes eltéréslista:** `naplok/FORRASKIVEZETES_M5_eltereslista.tsv` (18 450 nem azonos vers; előállítás: `eszkozok/lxx_osszevetes.py`, a törlés előtt futott). 22 627 régi vers: azonos 4 433, `strong_eltero` (Jaccard ≥ 0,8) 12 766, `nagy_eltero` 4 186, `zsoltar_eltolas` 739, csak a régiben 503, csak az újban 256.
- **Zsoltár-eltolás (JAVÍTÁS):** a régi zsoltár-kivonat egy verssel eltolt (pl. régi „Zsolt 22:2” = Károli 22:3 tartalma); az átállás ezt javítja (NYITOTT N17 lezárva).
- **Strong-konvenció (jelölve, nem javítva):** a leggyakoribb azonos szóalakú párok régi → új: G3364 → G3756 (4 835), G1065 → G1093 (2 563), G3165 → G3361 (2 098), G2036 → G3004 (1 344), üres → G3004 (2 094); a régi Strong nélküli szavakra (G2474 → üres 2 381, G3739 → üres 1 333) az új GreekWordList nem ad Strongot.
- **Csak a régiben (503 vers, az `lxx-hid` n=0):** Jób 78, Zsolt 66, Jer 59, Hós 57, Péld 50, 2Móz 46, 1Sám 34, Dán 30, Én 28, Józs 27, Ézs 24, Jón 2, 4Móz 1, 1Kir 1.
- **A régi kivonatra épülő állítások (tartalmi kérdés, nem javítva):** `adat/auditok.tsv` TEREMT-002 B4 sorai (Zsolt 107:40, 104:30, 33:6, 80:6, 80:7; 32., 82., 85., 160., 163. sor) és a másolat `naplok/T1_TEREMT002_auditok_munkalap.tsv`; `tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md` (Zsolt 14:1, 53:1); `tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` (92. sor); `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` (370. sor).

**Mintavételes `lxx-hid` (új, `LXX_OS`):** 1Móz 1:1 n=10 (azonos Strong-halmaz); 2Móz 33:19 n=28; Zsolt 22:2 n=21 (LXX 21:2); Sir 2:8 n=24. A `teszt_lekerdez_sir.py` rögzített n-jei (lxx-hid 24, tsk 15, karoli 1, gerinc 38, scan 10) változatlanok, a teszt zöld.

**Átállt olvasók:** `lekerdez.py` (`lxx-hid`), `lxx_bridge_egyezes.py` (csak a `lefedettseg` oszlop változik: `OS+kivonat` → `csak_OS`, 86 sor; egyéb oszlop nem), `lexikon_general.py` (`karoli_to_primary_slug`), `kockazat_szures_18_tanulmany.py`; `adat/datasetek.tsv` 4 sora `LXX_OS`-re mutat; `licencek.tsv` `LXX_kivonat` sora KIVEZETVE megjegyzést kapott (állapot változatlan). Törölve: 39 `LXX_kivonat_*.tsv`, a README, `lxx_kivonat_fetch.py`, `lxx_kivonat_fetch_v2.py` (a `KEZI_ELTOLASOK` az `lxx_os_import.py`-ba költözött).

## M7 — render-diff és elfogadási ellenőrzés

Módszer: `general.py --cel lexikon` és `--cel torzscikk` az `origin/main` állapotával és az ág állapotával, ugyanazon a napon, ideiglenes könyvtárba (a `generalt_proba/` nem módosult).

- **Törzscikkek (8):** a main-állapot és az ág-állapot renderje között 0 eltérés. **De** a commitolt `lexikon/*_TORZSCIKK.md` oldalak a #42-től függetlenül mind elavultak a mai adathoz képest (a friss render 65–326 sorban tér el oldalanként), ezért a `lexikon/ISTENTISZT-001_TORZSCIKK.md` még „CC BY-SA 3.0”-t ír az LSJ-ra; ennek felzárkóztatása a #36 (LEXIKON_UJRAGEN) dolga, a #42 nem renderelte újra (független ellenőr K8).
- **Táblák sorszám-változása (DT3, E17; fejlécsorok és kommentek nélkül, `git diff --numstat origin/main HEAD`):** `LXX_kivonat_*.tsv` (39 tábla) összesen −469 932 adatsor (kivezetés, az eltéréslista verzió szerint bont); `TBESH_konszolidalt.tsv` −9 838 (a `_nyers/tbesh/` alá költözött, generálható); `adat/lexikon_hivatkozasok.tsv` −1 és `adat/forditasok.tsv` −1 (TBESH H7121 `részlet`, DT-F42a); `datasetek.tsv`, `licencek.tsv` ±0; `LXX_OS/2-esdras.tsv`, `esther-greek.tsv` ±0 adatsor.
- **Lexikonoldalak:** ALVIL, ANTROP, HAMART, KIRALY, MENNY, TEREMT, ISTENTISZT: a N9-átállás (`cimke`) önmagában bájtazonos renderrel jár. ISTENTISZT-001 és HODIT-001 változik.
- **ISTENTISZT-001 (az élő oldal újrarenderelve, F42.8): 63 osztályozott sor, nem várt: 0.**
  - M4 szerinti tartalomcsere: a TBESH H7121 blokk és a TBESH-konszolidáció bekezdés, BDB-alapú szakasz (20 sor);
  - várt licencjelölés-változás: LSJ CC BY-SA 3.0 → 4.0 (11 sor);
  - korábbi adatváltozás felzárkózása (felhasználó jóváhagyta, 2026-10-05): ts-ek, `forditas_ubs.tsv` → `forditasok.tsv` forrásnév, BDB 2.c/3 és G994 fordítássor (32 sor).
- **HODIT-001: az élő oldal NEM lett újrarenderelve.** A #42 hatása (f2, Józs 5 sor) a scratch-diffben látszik, de az élő oldal a #42-től független, nagyobb elavulást is hordoz (pl. LXX-döntések „kutatói azonosítás függőben” → „eltérő” sorok, az F8 óta), amelynek felzárkóztatása a `#36` (LEXIKON_UJRAGEN) feladata; a #42 nem hagyja jóvá helyette.
- **K ellenőrzés:** K1 (szűkítve, DT-F42e): `git ls-files` nem tartalmaz `TBESH.lexicon`-t, `TBESH_konszolidalt.tsv`-t, `LXX_kivonat`-ot; a `TBESH.txt` marad. K2: friss checkoutban a `forras_letolt.py --ellenoriz` rendben (CRLF-munkafánál is, LF-normalizált sha256), a generátor fut. K3: hiányzó `TBESH.txt` / `TBESH.lexicon` esetén minden olvasó a letöltőre / helyreállításra mutató `FileNotFoundError`-t ad. K5: 23 `forrasfajl`, 0 nem létező. K6: nyilvános rétegben Online Bible-szöveg csak a jóváhagyott kivételekben (pilot-/próba-példányok, `generalt_proba/`, `naplok/EMELES_elso_adag.md`, a TBESH.txt maga, DT-F33f). K7: nincs licenc-konstans, hiányzó sor `SystemExit`. K9: a `KJV_Strongs_teljes` sor `tisztazatlan`, a `kjv.conf` szó szerint idézve.
- **`futtat.py` (CI-ekvivalens, a PR változott fájljaira):** E5 HIBA 7 a törölt `LXX_kivonat_README.md` címsorai miatt: a `TÖRLÉS-SZÁNDÉKOS:` jelölés a F42.13 commit üzenetében van; az E11 a lexikonoldal 366. során JELENTÉS (nem HIBA; a felhasználó tudomásul vette).
