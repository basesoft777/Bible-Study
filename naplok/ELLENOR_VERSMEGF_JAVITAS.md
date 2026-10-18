# Független ellenőrzés: F117_VERSMEGF_JAVITAS_BRIEF.md · 89b30c2e..c584e577

*A `fuggetlen-ellenor` subagent jelentése (modell: `claude-opus-5-5`, kért: `opus`). Az ellenőr szerepe nem enged fájlírást, ezért a jelentést az orkesztrátor írta ide változtatás nélkül; az orkesztrátor saját kiegészítése a fájl végén, külön szakaszban áll.*

ELTÉRÉS: 8 tétel. Ítélet: eltérésekkel; merge előtt 1 hiba javítandó.

## Eltérések súlyosság szerint

1. **Hiba — a CI E27-je bukik, 2 HIBA.** Az új N-F117a sor (`NYITOTT_FELADATOK.md:137`) két nem létező útra hivatkozik: `f17/macula_futtat.py` és `fj2/bsb_import.py`. A helyes út `eszkozok/f17/…` és `eszkozok/fj2/…`.
   - Parancs: `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 89b30c2e..HEAD) --diff-alap 89b30c2e --diff-fej HEAD --minta 100`
   - Eredmény: `E27 (HIBA: 2, JELENTES: 40)`. A többi E27/E25 találat a base-en is megvan.
   - CI-jelentés nem volt, ezért annak összevetése NEM ELLENŐRIZHETŐ.

2. **Figyelmeztetés — 5 tábla-lyuk az A–D′ halmazon kívül, N-tétel nélkül.** A Préd 9:1, 9:2 és a Jób 39:1–3 Károli-versnek nincs sora a táblában (Grep `^(Préd 9:\d+|Jób 39:\d+)\t`).
   - A tartalom szerint a Károli Préd 9:1 a KJV `Ecc.8.16`, a Jób 39:1 a KJV `Job.38.39` (`lekerdez.py karoli "Préd 9:1"` / `"Jób 39:1"`).
   - `lekerdez.py tsk "Jób 39:1"` és `tsk "Préd 9:1"`: „nincs KJV-pár”, n=0 (`ts=2026-10-18T17:09Z`).
   - Elvesző TSK-forrássor: 38 (Grep count `^(Jób 38:(39|40|41)|Préd 8:1[67])\t`).
   - Az `F117_javitas_jelentes.md:74` szerint „új tételt kell nyitni”, de a `NYITOTT_FELADATOK.md`-ben nincs ilyen tétel.
   - A `teszt_tsk_kulcs.test_mt_tartalek_negativ` a hibás állapotot rögzíti elvárásként.

3. **Figyelmeztetés — a javító bemenet generátora nem futtatható újra.** A `naplok/F117_javitas_bemenet_general.py:57-83,108` az `elozo:` értéket a MOSTANI (már javított) táblából olvassa, és őr nélkül felülírja a `konkordancia/Karoli_versmegfeleltetes_javitas.tsv`-t.
   - HEAD-en újrafuttatva mind a 346 sor önhivatkozó `elozo:…|szoveg_osszevetes_f117` megjegyzést kapna, a `potolt: nincs_sor` jelölések pedig elvesznének.
   - Javítási irány: a base-táblát (`89b30c2e`) olvassa, vagy álljon le, ha a táblában már F117-sor van.

4. **Figyelmeztetés — az E7 licenc-megnevezése hiányzik.** Grep `Public Domain|CC BY|licenc` a `naplok/F117_*` fájlokon: 0 találat. A README új szakasza sem nevez meg licencet. Csak a változatlan táblafejléc (`:2`) említi a CC BY 4.0-t. A zárójelentésben pótolandó.

5. **Megjegyzés — a mintanapló számai nem reprodukálhatók.** A `F117_minta.md` és a `F117_minta_kuszob.py` a `naplok/F117_szoveg_osszevetes.tsv`-re hivatkozik, ezt azonban a teljes futás felülírta (n=483).
   - A DT205 mintaszámai (20/13/8 a 64-ből; min. 0,57) a HEAD-ről nem jönnek ki újra, csak a 33abc45a-ról.
   - Ezt a commitot egyik fájl sem rögzíti.

6. **Megjegyzés — a „két skip” egy egész osztályt fed.** A `@unittest.skip` a teljes `Integracio` osztályon áll; a végrehajtó mérése szerint ez 35 skip (`F117_meres.md:84`). Dokumentált és jóváhagyott, de nagyobb, mint amit a „két teszt” sugall. A `KeziMtOr.test_kezi_ures_mt_mt_es_kjv_nem_all_le` minden kivételt elnyel (`except Exception: pass`).

7. **Megjegyzés — a DT204–f sorok állapota elavult.** Mind a hat sor „🟢 eldöntve, alkalmazásra vár”, holott alkalmazva vannak. Az a, c, d, e, f döntések „az orkesztrátor közvetítésével” kerültek be; közvetlen felhasználói megfogalmazás csak a b-nél van (a279b9fb). A felhasználói jóváhagyás NEM ELLENŐRIZHETŐ.

8. **Megjegyzés — a modul halmaz-őre tautologikus.** A `versmegf_javitas.javit()` (103–121. sor) őre nem bukhat el, mert az `uj` a `regi`-ből és a `jav`-ból épül. Negatív teszt nincs rá, és az üres sorokat szó nélkül elhagyja. A „0 sor változott a halmazon kívül” tényleges bizonyítéka a git-diff (l. lent).

## Rendben (OK)

- **E1 — a diff csak a generátor és a bemenete változását tükrözi.** `git diff -U0 89b30c2e..HEAD -- konkordancia/Karoli_versmegfeleltetes.tsv`: +347/−82, azaz 1 fejléc-jegyzet, 82 felülírt és 264 pótolt sor, mind `szoveg_osszevetes_f117` forrással. A `# GENERÁLT` fejléc megvan, más hunk nincs. A KK4 diffje csak az import és a print.
  - NEM ELLENŐRIZHETŐ (az ellenőr számára): a kétszeri futás bájtazonossága és a `6890db3c…dbb58` sha256.
- **E2 — mind a 13 fejezet teljes.** A versszám fejezetenként azonos a `Karoli_1908.tsv` és a tábla között (Grep count): 36, 37, 33, 22, 15, 10, 15, 23, 27, 19, 10, 6, 11, összesen 264 = A 261 + C 3.
  - B-osztály: Préd 9:21 = KJV `Ecc.10.1`, Jób 39:34 = KJV `Job.40.1`.
  - C-osztály: Dán 3:31 = KJV `Dan.4.1`.
- **E3 — szúrópróba 22 versen** (`lekerdez.py karoli` + Grep a `KJV_Strongs_teljes.tsv`-n), mind egyezik a táblával:
  - Hós 14:1 = 13:16, Jón 2:1 = 1:17, Jón 2:3 = 2:2, Jón 2:6 = 2:5;
  - Ézs 3:1 = 2:22, Ézs 64:1 = 64:1(+2);
  - 1Sám 24:1 = 23:29, 1Sám 24:2 = 24:1, 1Sám 20:43 = 20:42b;
  - 1Kir 22:43–44 = 22:43, 22:45 = 22:44, 22:46 = 22:45, 22:50 = 22:49, 22:54 = 22:53;
  - Én 6:1 = 6:4, Én 6:10 = 6:13;
  - Hós 2:1 = 2:2, Jób 17:1 = 17:2, Jób 17:12 = 17:13.
  - Proveniencia: `scope=range:<vers> | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | ts=2026-10-18T17:04Z`.
- **E3 — a kivétellista üres:** `NINCS_PAR_KIVETEL = frozenset()`.
- **E3 — a teszt-elvárások nem a kimenetből másoltak**, az ellenőr saját szöveg-összevetésével egyeznek. Kivétel: a Jób 39:34 MT-értéke a táblából jön.
  - A `test_f117_referencia_teljes` ugyanabból a forrásból (`F117_itelet.tsv`) ellenőriz, amelyből a tábla készült. Ez a lánc hűségét méri, nem a pár helyességét.
  - NEM ELLENŐRIZHETŐ (az ellenőr számára), hogy a tesztek zöldek.
- **E4 — az A–D′ halmazon kívül 0 sor változott.**
  - A 82 törölt sor mind B/D/D′: 1Kir 22:43–54 (12), 1Sám 20:43 (1), 1Sám 24:1–23 (23), Jób 39:34–38 (5), Jón 2:1–11 (11), Préd 9:21–23 (3), Ézs 3:1–27 (27).
  - Osztályszámok (Grep count): KJV 104, MT 68, KEZI + kitöltött mt 174; 23 195 adatsor.
  - M1/M5 szúrópróba (`lekerdez.py tsk` és a nyers TSK Grep count): Jón 2:6 n=4, Jón 2:3 n=26, Hós 13:14 n=29, Jób 17:12 + 17:15 = 25 (11 + 14), egyezik.
  - NEM ELLENŐRIZHETŐ: az M3 a `tsk_kulcs` szintjén.
- **E5 — a Jón 2:6 0 sora helyes.** A KJV Jón 2:5 négy TSK-sorának Votes-értéke 5, 7, 11, 11 (Grep `^Jón 2:5\t`), a generátor szűrője pedig `>= 15` (`lexikon_general.py:1953`). Az E5 szövege ennél a versnél szó szerint nem teljesíthető; ez a brief pontatlansága, nem a menet hibája.
  - A Jón 2:3 a 22/22/21-es sorokat kapja, a Zsolt 42:8 célja `Jón 2,4 Votes=15`.
- **E6 — az adatfájlok érintetlenek.** `git diff --name-status` az `adat`, `konkordancia`, `lexikon`, `motivumok`, `archivum`, `lexikon_general.py`, `general.py` és `FELADATOK.md` útvonalakra: csak a tábla, a javító TSV és a `konkordancia/README.md` változott.
- **Írási kör a brief `ir` mezőjén kívül:**
  - `sqlite_epit.py`: csak a `VersmegfKeziMt` osztály, a `kezi_mt_or()` és egyetlen hívás (+20 sor).
  - `teszt_sqlite_epit.py`: csak a `KeziMtOr` és a 2 skip (+40 sor).
  - A README- és a NYITOTT-változás egyeztetett eltérés.
- **Helyőrzők:** a DT204–f helyőrzők, 8 cellásak, a cellán belüli `|` escapelve. Az N-F117a/b/c helyőrző, és valóban nyitott.
- **⛔ pontok:** mindegyik külön megállás-commit, a döntés utána jön.
- **Proveniencia:** a javító TSV fejléce és mind a 346 sora tartalmaz `scope=…` mezőt (assert kényszeríti).

## Ellenőrzőlista

- **Törölt sorok:** 82, mind felülírás (B 8 / D 67 / D′ 7), nettó törlés 0.
- **Sorszám-változás a base-hez:**
  - `Karoli_versmegfeleltetes.tsv`: 22 931 → 23 195, +264. Bontási napló: `F117_javitas_jelentes.md:27-37`.
  - `Karoli_versmegfeleltetes_javitas.tsv`: új tábla, +346 (KJV 104 / MT 68 / KEZI 174).
  - Minden más `adat/` és `konkordancia/` tábla: Δ 0.
- **A „nulla-diff” hatóköre:** csak a tábla sorai, kulcs szerint. Nem terjed ki a fogyasztók kimenetére (N-F117a) és a `tsk_kulcs` KJV→Károli irányára (M3: 350 kulcs változott).
- Tanulmányfájl nincs a diffben; ⛔ DÖNTÉS KELL nincs.

## Az orkesztrátor kiegészítése (nem az ellenőr megállapítása)

A két, az ellenőr számára nem ellenőrizhető pontot az orkesztrátor lefuttatta (2026-10-18, a `c584e577` HEAD-en):

- **E1, bájtazonosság:** `KK4_KIMENET=<scratchpad>/kk4_{1,2}.tsv python naplok/KAROLI_KK4_tabla_veglegesit.py` kétszer, a repón kívülre: mindkét kimenet sha256-ja `6890db3c…`, és egyezik a repóbeli `konkordancia/Karoli_versmegfeleltetes.tsv`-vel. `scope=kk4_ketszeri_futas | forras=naplok/KAROLI_KK4_tabla_veglegesit.py | n=2 | ts=2026-10-18`
- **Tesztek:** `python eszkozok/teszt_tsk_kulcs.py` → 15/15 OK; `python eszkozok/teszt_versmegf_javitas.py` → 16/16 OK. `scope=unittest | forras=eszkozok/teszt_tsk_kulcs.py, eszkozok/teszt_versmegf_javitas.py | n=31 | ts=2026-10-18`

## Újraellenőrzés (2153f4ff..942006ae)

*A `fuggetlen-ellenor` subagent második jelentése (modell: `claude-opus-5-5`, kért: `opus`), az orkesztrátor írta be; a fájlírást a futtatási környezet nem engedte az ellenőrnek. Ítélet: **eltérésekkel** (2 kis súlyú); a merge előtti hiba (E27) megszűnt.*

| pont | eredmény | indok (az ellenőr saját lekérdezése) |
|---|---|---|
| 1 E27 | megszűnt | `futtat.py --diff-alap 89b30c2e --diff-fej HEAD`: E27 0 HIBA (40 JELENTES, a base-en is), minden szakasz 0 HIBA |
| 2 tábla-lyuk | megszűnt | N-F117d megvan (`NYITOTT_FELADATOK.md:138`); a tábla a javítókörben nem változott; a Préd 9:1–2 / Jób 39:1–3 sor nélkül, 38 TSK-sor (`scope=range:Jób 39:1 \| forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv \| n=0 \| ts=2026-10-18T18:07Z`) |
| 3 bemenet-generátor | megszűnt | `git show 89b30c2e:…` olvasás, `--felulir`-őr |
| 4 licenc | megszűnt | a 7 licenc-cella egyezik az `adat/licencek.tsv`-vel |
| 5 minta-forrás | megszűnt | a napló kimondja a `33abc45a` forrást; a fájl ott jött létre |
| 6 skip | **fennáll, részben (kis súlyú)** | a `KeziMtOr` már csak a várt `FileNotFoundError`-t fogadja; a skip feltételes (csak `VersmegfKeziMt`), de a közös `setUpClass` miatt mind a 34 `Integracio`-teszt kimarad (35 teszt nem fut). A „technikailag nem szűkíthető” túlzó: táblamásolaton (a `Negativ` osztály `modosit()`-mintájára, a 174 sor `igehely_mt`-je kiürítve) szűkíthető volna, módosított adaton. A döntés („a skip a két tesztre szűkítve”) szó szerint nem teljesül — felhasználói jóváhagyás kell |
| 7 DT204–f | megszűnt | mind `✅ alkalmazva`, 8 cella, „a szülő sessionön át érkezett” |
| 8 halmaz-őr | megszűnt | a `halmaz_or()` a kimenetet függetlenül újraolvassa, hat ága elbukhat; a negatív tesztek valódi halmazon kívüli változást visznek be. Maradék: a hiányzó-javítósor- és az oszlopfej-ágra nincs negatív teszt |
| 9 (új) datasetek-állítás | **új, kis súlyú** | a `F117_javitas_jelentes.md:81` szerint mind a 7 dataset `elerheto`; a `KJV_Strongs_teljes`-nek és a `Karoli_versmegfeleltetes`-nek nincs saját sora |
| tiltott fájlok | OK | a javítókör nem érintette a #11 fájljait, az `adat/`-ot, a `FELADATOK.md`-t, a `sqlite_epit.py`-t |

### Az orkesztrátor kiegészítése az újraellenőrzéshez (942006ae HEAD)

- **Tesztek** (az ellenőr számára nem futtathatók): `teszt_tsk_kulcs.py` OK, `teszt_versmegf_javitas.py` OK (19), `teszt_sqlite_epit.py` FAILED (failures=1, skipped=2) — az egyetlen FAIL a main-en is fennálló `Pozitiv.test_mai_adat_zold`, ERROR nincs. `scope=unittest | forras=eszkozok/teszt_*.py | ts=2026-10-18`
- **E1:** a KK4 a refaktorált `versmegf_javitas`-sal kétszer, a repón kívülre futtatva `6890db3c…` — bájtra azonos a commitolt táblával. `scope=kk4_ketszeri_futas | n=2 | ts=2026-10-18`
- **3. pont:** `F117_javitas_bemenet_general.py --kimenet <scratchpad>/jav.tsv` → sha256 `d7534fa6…`, azonos a commitolt javító-TSV-vel.
- **5. pont:** `git show 33abc45a:naplok/F117_szoveg_osszevetes.tsv` + `F117_minta_kuszob.py` → 20 / 13 / 8 a 64-ből, TAHOT-Jaccard min 0,57: egyezik a DT205 mintaszámaival.
- **9. pont:** javítva a `naplok/F117_javitas_jelentes.md` licencszakaszában (F117.9).
- **6. pont:** nyitott; a zárójelentés felhasználói jóváhagyásra váró eltérésként rögzíti.
