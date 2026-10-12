ELTÉRÉS: 6 tétel

# Független ellenőrzés — F37_TANULMANY_ELLENORZES_BRIEF.md

*A jelentést a `fuggetlen-ellenor` írta (2026.10.07). Az ügynöknek nincs fájlíró eszköze, ezért a szöveget az orkesztrátor mentette el, változatlanul. Az orkesztrátor kiegészítése a végén, külön szakaszban áll.*

Tartomány: megadott `666ab03ab17eaee9ac848ca6930f41160f2bab41..b6ce4bc68cdb461ffd29f47a85261a593e2eddff`. Ténylegesen ellenőrizve: `af1ad8b..b6ce4bc` (a valódi merge-base az `origin/main`-nel, l. B0).

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| B0 bemenet: base | ELTÉRÉS | — | `git log --oneline b6ce4bc..main` → üres; `git log --oneline main..b6ce4bc` → 15 commit, köztük `#237`, `#238` merge és `7419c7d szamkiosztas`; `git log origin/main..b6ce4bc` → 8 commit (F37.0–F37.7). A helyi `main` (666ab03) elavult, a merge-base `af1ad8b`. Az `origin/main` közben előrébb jár (#239, 07fcb39), és a `DONTESEK.md`-t, az `adat/SEMA.md`-t és a `CLAUDE.md`-t is módosítja (`git diff --stat af1ad8b..origin/main`). |
| CI (3.) megadott base-zel | (tájékoztató) | — | `futtat.py --valtozott <666ab03..head fájljai> --diff-alap 666ab03… --diff-fej b6ce4bc…` → EXIT=1; E5 HIBA 4, E16 HIBA 1, E26 HIBA 6 (DT55–57: a main `szamkiosztas` commitjából, nem F37). Ok: a rossz base. |
| CI (3.) valódi base-zel, PR-cím nélkül | OK (várt) | — | `futtat.py --valtozott <af1ad8b..head> --diff-alap af1ad8b --diff-fej b6ce4bc` → EXIT=1: E5 HIBA 3 (törölt címsor, mert commit-üzenet nem volt átadva), E16 HIBA 1 (PR-cím). |
| CI (3.) úgy, ahogy a workflow futtatja | OK | — | ugyanez + `--pr-cim "[ELLENŐRZŐ] F37" --commit-uzenet "$(git log af1ad8b..b6ce4bc --format=%B)"` → EXIT=0; minden HIBA 0 (E2 JELENTÉS 1, E9 JELENTÉS 8, E25 JELENTÉS 3). A `TÖRLÉS-SZÁNDÉKOS:` jelölés az f25faa6 üzenetében áll; a workflow a merge-base-t használja (`ellenorzes.yml:42`). |
| CI teljes mód | OK (jelentés) | — | `futtat.py --teljes` → EXIT=0; E20 JELENTÉS 48, mind helyi, nem verziózott `.claude/worktrees/*/tematikus_lezart/Konnyu_ellenorzes_4_lezart_tanulmany.md` fájlon (a `tanulmany_fajl_e` könyvtár-kizárása `startswith`, a beágyazott útra nem hat). CI-ben nincs worktree. |
| Elfogadás: CI zöld + szabály-tesztek | NEM ELLENŐRIZHETŐ | `ellenorzes.yml:130-142` | A `test_szabalyok.py` és a `test_tanulmany.py` futtatása nem megengedett parancs (D6), nem futott. A workflow mostantól mindkettőre bukik. |
| Elfogadás: pozitív és negatív teszt szabályonként | OK (statikus) | `tesztek/test_tanulmany.py:65-221` | E20: 3 pozitív és 3 negatív; E13: 2 és 6 (+1 FIGYELMEZTETÉS-szint); E8: 1 és 2; E9: 1 és 2; E12: 1 és 2. `git diff af1ad8b..b6ce4bc -- …test_tanulmany.py \| grep -c "^+    def test_"` → 29. |
| Jelentett eltérés: F37.3 „28 teszt” | OK (pontos) | ea552f7 | ugyanez a grep `af1ad8b..ea552f7`-re → 27; az üzenet 28-at ír (`git log -1 --format=%B ea552f7`). |
| Jelentett eltérés: `ir`-listán kívüli átírás | ELTÉRÉS | `naplok/TANULMANY_ELLENORZES_utofeladat.md:55` | A lista szerint `4_`, `5_`, gyorsreferencia, tanítói lista. A `git diff --numstat af1ad8b..b6ce4bc` szerint azonban a `sablonok/Javasolt_sablon_kiegeszites_BDB_arnyalat.md` is változott (6+/6−), és ez nincs sem az `ir` listán, sem a jelentett eltérések között. |
| Jelentett eltérés: inline Python/`sed` magyar szöveggel | NEM ELLENŐRIZHETŐ | — | A git-történetből nem látszik, a session naplóját nem kapom meg. |
| Jelentett eltérés: FELADATOK.md nem szerkesztve (D25) | ELTÉRÉS (dokumentálás) | brief T6 1. pont, `FELADATOK.md:192` | A D25 létezik és indokolja (`FELADATOK.md:192`), a fájl valóban nem változott. A brief T6 „Frissítsd a FELADATOK.md saját sorát” pontja viszont teljesítetlen, és ez a repóban sehol nincs rögzítve: `git diff af1ad8b..b6ce4bc \| grep D25` → nincs; az utófeladat eltéréslistájában sem szerepel. |
| „Bővített sablon” élő hivatkozás | OK (értelmezéssel) | `sablonok/3_…:3`, `4_…:82,84`, `5_…:7,9`, `Javasolt_…:35` | Grep `[Bb]ővített sablon` → a sablonokban csak verziótörténeti (changelog) sorok maradtak. A többi találat lezárt (`F8_BRIEF.md`, archív, changelog), tanulmány (`genezis/1Moz_1v2-2v3`), tematikus_lezart, napló, illetve a brief saját szövege. Más ügynökdefinícióban és aktív briefben nincs. Mellékes: a T0 (`T0_felmeres.md:73`) a `3_` sablont az átnevezendők közé sorolja, de nem változott, és ezt semmi nem magyarázza. |
| Új kód: TSV-olvasás | OK | `tanulmany_ellenorzes.py:62-75, 170-172` | `split('\t')`; a `csv` modul egyik új fájlban sincs importálva (Grep `csv` a két új .py-ban → 0). |
| Új kód: UTF-8 wrapper | OK | `tanulmany_audit.py:16-26`, `tanulmany_ellenorzes.py:30-42`, `test_tanulmany.py:16-23` | A wrapper az stdlib-importok után áll; a helyi modulok (`kozos`, `szabalyok`) a `sys.path` beállítása után jönnek, ugyanúgy, mint a meglévő `futtat.py`-ban. |
| `.claude/agents/fuggetlen-ellenor.md` csak hozzáfűzés | OK | `:81-152` | `git diff --numstat af1ad8b..b6ce4bc` → 72+/0−; a DT-F37b-pontosítás az új szakaszon belül van. |
| Ügynökdefiníció: a „Csak olvas” állítás | ELTÉRÉS (alacsony) | `fuggetlen-ellenor.md:97-98`, `tanulmany_ellenorzes.py:439-452` | A definíció a segédszkriptet „csak olvas”-nak mondja, és megengedett parancsként adja. A szkriptnek viszont van fájlt író `--kimenet` kapcsolója; a docstring ezt kivételként jelzi, a definíció nem. |
| Végleges DT/N szám az ágon | OK | — | `git diff af1ad8b..b6ce4bc \| grep "^+" \| grep -oE "\b(DT\|N)[0-9]+\b"` → csak `DT3` (meglévő hivatkozás). E26 = 0 (fenti futás). Helyőrzők: DT61/b, DT-F37-10/11. |
| 4 Strong-ELTÉRÉS (T5 audit) | OK (igazolva) | `naplok/TANULMANY_AUDIT_ugynok.md:51-54` | `lekerdez.py scan H5375 --szakasz "1Móz 14"` n=0; `scan H7311 --szakasz "1Móz 14:22"` n=1; `scan H1892 --szakasz "1Móz 4"` n=0; `scan H1893 --szakasz "1Móz 4:2"` n=1 (2 szó); `scan H5315 --szakasz "1Móz 6"` n=0 és `"1Móz 6:17"` n=0 (a versben H7307 n=1, H2416 n=1); `scan H0853 --szakasz "1Móz 1:1"` n=1 (2 szó). Proveniencia: `scope=range:… \| forras=TAHOT_kivonat.tsv \| strong=… \| n=… \| ts=2026-10-07T09:39–40Z`. A tanulmánysorok egyeznek: `1Moz_14:62`, `1Moz_4v1-24:57`, `1Moz_6v9-22:51`, `1Moz_1v1:57`. |
| T5: Jób 38:41 verzifikáció | OK | `TANULMANY_AUDIT_ugynok.md:87` | `lekerdez.py karoli "Jób 38:41"` → „Nincs Károli-szöveg”; `karoli "Jób 39:3"` → „Ki szerez a hollónak eledelt…” (`forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv`). |
| T3 gépi audit egyezése | OK | `naplok/TANULMANY_AUDIT.md:13-19` | `futtat.py --valtozott genezis/*_bovitett.md ujszovetseg/*_bovitett.md` → E13 206, E8 32, E12 195, E20 0, E9 0; egyezik a jelentéssel (összesen 433, mint az F37.3 üzenetében). |
| T3 audit proveniencia | ELTÉRÉS (alacsony) | `naplok/TANULMANY_AUDIT.md:5` | „commit `f25faa6`”, de a generátor (`tanulmany_audit.py`) csak az ea552f7-ben került be (`git diff --stat af1ad8b..f25faa6` nem tartalmazza). A megnevezett commitból a jelentés nem reprodukálható. |
| T3 kötelező mód minden tanulmányra (E13/E12 hatókör) | ELTÉRÉS (közepes) | `eszkozok/ellenorzes/szabalyok.py:684-691, 818`; `kozos.py` `tanulmany_fajl_e` | A `tanulmany_fajl_e` bármely könyvtárban elfogad `*_bovitett.md`/`*_tanulmany.md` fájlt (a teszt maga: `zsoltarok/Zsolt_23_tanulmany.md` → True, `test_tanulmany.py:57`). Az E13 (tanulmányon HIBA) és az E12 viszont előbb az `E12_E13_HATOKOR`-t nézi (`genezis/`, `ujszovetseg/`, …). Egy új könyvtárba írt tanulmányon az E20/E8/E9 lefut, az E13 HIBA és az E12 csendben nem. Ezt teszt nem fedi. |
| D: DT-F37-1..11 | OK | brief:123-133 | DT-F37-1/2/5: kód és utófeladat ennek megfelelő; -3: a workflow jelentés-mód lépése nem bukik (`ellenorzes.yml:119-128`), a kötelező mód D8 szerinti; -6: az E20 a sablonból olvas (`szabalyok.py` `tanulmany_sablon_szakaszai`, teszt `test_pozitiv_a_lista_a_sablonbol_jon_dt_f37_6`); -8: E20 új, E21–E24 bővítés; -9: T2 elhagyva, a `T2_alap_osszevetes.md` nem készült; -10/11 = DT61/b. A felhasználói döntés ténye (chat) a repóból NEM ELLENŐRIZHETŐ. |
| Elfogadás: két auditjelentés | OK | `naplok/TANULMANY_AUDIT.md`, `naplok/TANULMANY_AUDIT_ugynok.md` | `git diff --numstat`: 597 és 536 sor, új fájlok. |
| Elfogadás: nincs alap tanulmány | OK (részben ellenőrizhető) | `naplok/T0_felmeres.md:11,28` | A diffben nincs `_alap` tanulmány; az `--all` története a megengedett parancsokkal nem lett újrafuttatva. |
| A1 memória vs. lekérdezés | OK | `T0_felmeres.md:3`, `TANULMANY_AUDIT_ugynok.md:10` | A T0 „mért, nem lekérdező CLI-ből”, a 4–5. pont `manual`. T0-szúrópróba: `scan H3290 --szakasz "1Móz 32"` n=16; `scan H0430 --szakasz "Zsolt 88"` n=1; `scan H3068 --szakasz "Jóel 3"` n=7; `scan H0834 --szakasz "Jób 41"` n=0. Egyezik a T0 6. pontjával. |
| A2 nyitott tételek a friss repó szerint | ELTÉRÉS | `naplok/TANULMANY_ELLENORZES_utofeladat.md:50`; `T0_felmeres.md:97` | A „CLAUDE.md TAHOT-hiánylista elavult — külön /befogad-tétel” nem nyitott: az `origin/main` DT58-a (07fcb39) már javította (`git diff af1ad8b..origin/main -- CLAUDE.md`: „Jób 40:1–5 és a Jób 41”). A `NYITOTT_FELADATOK.md` az F37 diffben nem változott. |
| A3 tematikus/lexikai címke | OK (tárgytalan) | — | A diff új tanulmányt vagy párhuzam-állítást nem hoz. |
| A4 Remez/Sod | OK (tárgytalan) | — | Nincs új tanulmány; a T5 Sod-leletei (`TANULMANY_AUDIT_ugynok.md:71-83`) `manual` ítéletek, saját olvasással nem ismételtem meg. |
| A5 nevesített tanító | OK (tárgytalan) | — | A `PaRDeS_tanitok_lista.md` csak a sablonnév cseréjével változott (1/1 sor). |
| A6 E12–E15 | OK | — | A változott fájlokon E12/E13/E14/E15 = 0 (fenti futás). |
| CL1 törölt sorok | OK | — | `git diff --numstat af1ad8b..b6ce4bc`: 52 törölt sor, mind módosítás. T1-átnevezés 26 (ATAL 1, Join 3, MUNKAMENET 3, SEMA 2, sablon1 2, sablon2 2, sablon4 2, sablon5 1, Javasolt 6, gyorsref 3, tanítók 1); kód 22 (szabalyok 17, futtat 2, workflow 3); brief-fejléc 4. Fájltörlés nincs (`--diff-filter=D` → üres). |
| CL2 kulcstartomány | OK | — | E-számok: E20 új, E21–E24 szabad (`szabalyok.py` E26-megjegyzés); a Strong-szúrópróbák fent. |
| CL3 nulla-diff hatóköre | OK | — | Tanulmányfájl (`genezis/`, `ujszovetseg/`), `adat/*.tsv` és `konkordancia/` nem változott (name-only lista). Nem vonatkozik: a sablonokra, a dokumentációra és a CI-kódra. |
| CL4 adattábla Δ (E17/DT3) | OK | — | `git diff --numstat af1ad8b..b6ce4bc -- '*.tsv'` → üres; `666ab03..b6ce4bc` → üres. Minden `adat/`, `konkordancia/` .tsv Δ = 0, bontási napló nem kell. Az `origin/main` új táblái (pl. `parok_Zsolt.tsv` +32 191) nem az ág változásai. |
| CL5 a brief ⛔ pontjai | OK | `T0_felmeres.md:7-11`; `DONTESEK.md` DT61/b | A T0 három ⛔ feltétele nem teljesült, ezt dokumentálták. A T5 ⛔ → DT61/b, döntés előtt megállt (0d63bb1 „döntésre vár”, c213ac6 „eldöntve”). |
| ⛔ (tanulmány-ellenőrzés) | — | — | Nem él: a diff nem hoz tanulmányfájlt. |

## Az eltérések súlyossági sorrendben

1. **E12/E13 hatókör-rés.** A genezis/ és ujszovetseg/ (és a többi régi hatókörkönyvtár) kívül írt tanulmányon az E13 tanulmány-HIBA és az E12 nem fut, pedig a `tanulmany_fajl_e` tanulmánynak ismeri el (`szabalyok.py:684-691, 818`).
2. **Elavult base, ág a main mögött.** A megadott base nem a merge-base; az ág nincs a friss `origin/main`-re hozva (#239: átfedés a `DONTESEK.md`-ben és az `adat/SEMA.md`-ben). Emiatt az utófeladat egyik „nyitott” tétele már lezárt (A2).
3. **Jelentetlen `ir`-en kívüli fájl:** `sablonok/Javasolt_sablon_kiegeszites_BDB_arnyalat.md`.
4. **A T6 FELADATOK-pontja teljesítetlen,** a D25-indoklás a repóban nincs rögzítve.
5. **`TANULMANY_AUDIT.md`:** a proveniencia olyan commitot nevez meg, amelyben a generátor még nincs benne.
6. **Ügynökdefiníció:** a segédszkriptet „csak olvas”-nak mondja, de a szkriptnek fájlt író `--kimenet` kapcsolója is van.

Nem ellenőrizhető: a két tesztfájl futása (a D6 miatt nem futtattam), az inline Python/`sed` eltérés, és a chatben hozott felhasználói döntések ténye.

---

## Orkesztrátori kiegészítés (2026.10.07)

- **Szabály-tesztek** (az ellenőr ezeket nem futtathatta): `python eszkozok/ellenorzes/tesztek/test_szabalyok.py` → 74 teszt, OK; `python eszkozok/ellenorzes/tesztek/test_tanulmany.py` → 29 teszt, OK.
- **A B0 oka:** az ellenőrnek átadott base-t az orkesztrátor a frissítetlen helyi `main`-ből számolta. A helyes merge-base az `af1ad8b`. Az `origin/main` 10 committal jár előrébb (07fcb39-ig).
