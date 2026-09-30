# ELLENOR_F21P.md — F21_KAROLI_STRONG_PILOT_BRIEF.md · `origin/main...claude/f21-pilot` — 1. kör

*A `fuggetlen-ellenor` jelentése, a fájlba az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze). Ellenőrzött fej: `ac6fb49`. Merge-base b4b2e66; saját változtatások: 38 F21.* commit; bot-commitok: 3 (12283d4, 0b3e240, d71c691). Ítélet: **NEM TISZTA** (hiba: nincs; figyelmeztetés: 7; megjegyzés: 3). A szkriptek újrafuttatása, a bájtazonosság és az sha256 a szerepkorlát miatt nem volt ellenőrizhető (l. lent).*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| P-K1 minta | OK | `f21p/minta.tsv:2-201` | 200 vers. R1 = 1Móz 40 + 2Móz 30 + Péld 30, R2 25, R3 25, R4 25 evangélium + 25 levél. 1Móz-versek `regi_arany_sor>0`: 24/40 (≥20). A régi hármasok összege 32. A 13 mintabeli Zsolt-vers egyike sincs a `f21p/sorrend_eltero_versek.tsv` 57 versében. |
| P-K1 sorrend-ellenőrzés | OK | `f21p/sorrend_ellenorzes.md` | `git log` 8c15123 (F21.1). A fájl létezik, az 57 eltérő vers listázva. |
| P-K2 Opus-arany, szúrópróba | OK | `DONTESEK.md` DT19 | Az arany (78767be, 11:58) az első trigger (75496f0, 12:35) előtt készült. Szúrópróba: 5/193 = 2,59% ≤ 3%, a felhasználó elfogadta. |
| P-K3 futások | OK (egyeztetett eltérés: F4 nem futott, PD8) | `f21p/futasnaplo.tsv` | F1, F2, F3, F5, F6, F3V2 sorai megvannak; `kapuhiba_db`, `probalkozas`, `finish_reason` naplózva. |
| P-K4 minden mérőszám összeállításonként és rétegenként a jelentésben | **ELTÉRÉS** (figyelmeztetés) | `naplok/F21P_jelentes.md:43,55-62` | A jelentésből hiányzik: A–B egyezés (uniós arány), pontosság bizonyossági szintenként (`kozepes`/`alacsony`), A és B pontossága rétegenként, A/B kapuhiba rétegenként. Ezek csak a `naplok/F21P_meres_v1.md:58-64`-ben és a `meres_eredmeny.tsv`-ben vannak. A brief P6 szerint a jelentésbe kellenek. |
| P-K5 költségvetítés | **ELTÉRÉS** (figyelmeztetés) | `f21p/koltseg_vetites.tsv:34-53`; jelentés :114 | A brief P5.6 szerint a bootstrap a *verseken* fut, a megvalósítás a *kötegeken* (DT21 f nyitott, nincs jóváhagyva). Ellenőrzés: mintán belül 0,001% (közel tautologikus), leave-one-out −0,149%, mindkettő ≤ 10%. Versszám 14006+3712+5486+7954 = 31158. Kötegek 1401+372+549+796 = 3118. M kézzel a naplóból: F3 0,257251/0,198567 = 1,2955; F3V2 0,256731/0,214964 = 1,1943; egyezik. Az A+B+C vetítés elmaradása egyeztetett eltérés (PD8), nem a DT21 alapján. |
| P-K6 összköltség ≤ 3 USD | OK | `f21p/futasnaplo.tsv` | Futásonként: F1 0,132718; F2 0,017725; F3 0,257251; F5 0,060663; F6 0,009506; F3V2 0,256731. Összesen **0,734594 USD**. A kumulatív oszlop a futáshatárokon egyezik. Megjegyzés: 2 F2-sor (47, 51) `finish_reason=error`, `koltseg_usd=0`, 492/292 kimeneti tokennel; ha ezeket számlázták, a költség alulbecsült (elhanyagolható). |
| P-K7 javaslat, döntési tétel | OK | `DONTESEK.md` DT21 | DT21 🟡 nyitva, opciók 1–3. A szabályból adódó „a teljes futás nem indul” a jelentés :176 sorában szerepel. |
| Döntési szabály alkalmazása („mi bukott el”) | **ELTÉRÉS** (figyelmeztetés) | brief :14; jelentés :22 | A `lezarva_osszegzes` és a (b) pont szerint „az A/B kapuhibája bukott”. A kapuhiba nem tartozik az öt rögzített feltétel közé (brief :133-139), tehát feltételként nem bukhat el. Az A+B régi arany (A∩B) 60% (3/5) viszont mért bukás, a (b) mégsem nevezi meg. |
| A+B+C állítása | **ELTÉRÉS** (figyelmeztetés) | jelentés :9, :17; brief :14 | Az öt feltételből A+B+C-re egy sem mért (F4 nem futott). A táblában „nem felel meg (nem mérhető)” áll, a vezető mondat és a `lezarva_osszegzes` „egyik összeállítás sem felel meg”, az A+B+C külön említése nélkül. A pontos állítás: „nem mért (PD8)”. A :176 sor ezt helyesen mondja. |
| Régi arany 30/30 | **ELTÉRÉS** (figyelmeztetés) | jelentés :15, :51; `f21p/c_regi_arany_besorolas.tsv:3,7`; `f21p/regi_arany_hibas.tsv` | A két „hibás” hármas éppen a C két nem-egyezése (F21.11 c_diff), a futás utáni PD9-cel kizárva. Kizárás nélkül 93,8% (30/32) < 95%, kizárással 100%: a kizárás a küszöb átlépését fordítja meg. Az (a) tábla csak a kizárásos számot hozza. Az 1Móz 13:4 a besorolásban „vitatható”, a `hibas.tsv`-ben „hibás”. `lekerdez.py kollokacio H5315 H2416` → 61 vers, 1Móz 6:17 nincs köztük; `kollokacio H7307 H2416` → 1Móz 6:17 benne; `kollokacio H7121 H3068` → 1Móz 13:4 benne, vagyis a H3068 a versben van, a hozzárendelés értelmezés kérdése. Döntésre nincs hatása (a C a PD6 szerint nem minősíthető). |
| PD6: „megfelelt” egymodelles összeállításon | OK | `naplok/F21P_meres_v2.md:5`; jelentés :13-15 | Grep `megfelel` a `naplok/F21P_*`, `f21p/*` és `DONTESEK` fájlokban: egymodelles összeállításhoz sehol nincs „megfelelt”. |
| PD10: korrigált = „Opus-besorolás, nem mérés” | OK (megjegyzés) | `naplok/F21P_C_diff.md:21` | Mindenhol jelölve. A `C_diff.md:21` fejléce csak „kézi besorolás alapján”, a :19 sor viszont „NEM mérés”. |
| Jelentés számai vs. generált TSV | OK | jelentés :32-41, :59-62, :142-145 | Kézzel számolva: 989/1051 = 94,1; 990/1051 = 94,2; 1020/1051 = 97,1; 990/1061 = 93,3; 1020/1090 = 93,6; a rétegösszegek egyeznek. Kapuhiba a naplóból: A 152 első / 82 végleg, B 106/82, F3 30/1, F3V2 19/0. Egyezik a `meres_eredmeny.tsv:213-263`-mal. Kereszt-konzisztencia: F3 × v2 többlet 71 + hiány 61 = 132, a `koltseg_vetites.tsv:70` szerint 132/60; F3V2 70 + 31 = 101, egyezik. |
| `lezarva_osszegzes` „42 USD (90%: 38–47)” | **ELTÉRÉS** (megjegyzés) | brief :14 vs. jelentés :15 | Az [38–47] az F3 intervalluma (37,78–47,03). Az (a) tábla az F3V2 [37,95–46,15] értékét hozza, ami kerekítve 38–46. A forrás-futás nincs megnevezve. |
| Szkriptek újrafuttatása, bájtazonosság; jsonl-visszaszámolás | NEM ELLENŐRIZHETŐ | — | A szerepkorlát szerint nem futtatható. |
| Proveniencia (1. szabály) | **ELTÉRÉS** (figyelmeztetés) | `f21p/koltseg_vetites.tsv:1`, `f21p/ingadozas.tsv:1`, `f21p/meres_v2_eredmeny.tsv:1`, `naplok/F21P_jelentes.md:3`, `naplok/F21P_C_diff*.md:3`, `naplok/F21P_arany_v2_diff.md:3` | Grep `GENERÁLT`: teljes `scope\|forras\|ts` csak a `meres_eredmeny.tsv`-ben és a `F21P_meres_v1.md`-ben van. A többiből hiányzik a `ts`, egyes fájlokból a `scope` vagy a `forras` is. |
| `adat/`, `konkordancia/`, FELADATOK, NYITOTT | OK | — | `git diff --numstat origin/main...HEAD -- adat konkordancia FELADATOK.md NYITOTT_FELADATOK.md` → 0 sor. |
| csv-modul, wrapper, normalizálás | OK | `eszkozok/karoli_strong/*.py` | `csv` használat: 0 találat. `reconfigure(encoding='utf-8')`: 18/18 fájl, az `import sys` után. `Konyv_normalizalo`: `tokenek.py:38,72,81`. |
| Kulcs-grep | OK | teljes worktree | 0 találat. |
| CI (saját futtatás) | **ELTÉRÉS** (figyelmeztetés, feltételes) | `.github/workflows/f21p_pilot.yml` | `eszkozok/ellenorzes/futtat.py --esemeny pull_request` → E2–E15: 0, **E16 HIBA: 1** (workflow-t érint, a PR-cím nem „[ELLENŐRZŐ]” előtagú). `--pr-cim "[ELLENŐRZŐ] F21: …"`-mal nincs találat. CI-jelentést nem kapott, az összevetés NEM ELLENŐRIZHETŐ. |
| Arany v1 érintetlen | OK | `f21p/arany_opus.jsonl` | 78767be (60+), azután csak 5d1a413 (F21.6, 4/4 sor: Mk 2:10, Mk 2:23, Jak 3:4, Jak 3:8), a futás előtt. |
| Arany v2 | OK; hash: NEM ELLENŐRIZHETŐ | `f21p/arany_opus_v2.jsonl` | v1–v2 diff: 2/2 sor, 2Móz 25:8 és 2Móz 26:13. A v2 utolsó módosítása 5d3e762, ez megelőzi a befagyasztó 6aca6c5 commitot. Az sha256 (06a00738…) nem számolható a megengedett parancsokkal. |
| Workflow | OK | `.github/workflows/f21p_pilot.yml:38-124` | Felül `contents: read`, `write` csak a `futtatas` jobnál. Push csak `HEAD:refs/heads/claude/f21-pilot`, ref-ellenőrzéssel, csak `f21p/` alá staged. A kulcs csak a :85 soron szerepel. |
| Actions-commitok | OK | — | 12283d4, 0b3e240, d71c691: csak `f21p/futasnaplo.tsv` és `f21p/valaszok/*.jsonl`. |
| Merge ac6fb49: DT-átszámozás, F18 sorai | OK (megjegyzés) | `DONTESEK.md` | DT19–DT21 felvéve, a DT5 (F18) változatlan. A DT18 sor tartalma azonos, de elveszett a fájlvégi újsor. A jelentés és a `jelentes_f21p.py` DT-hivatkozásai konzisztensen átírva. |
| F22 fejléc (más feladat) | NEM ELLENŐRIZHETŐ (a hívó szerint egyeztetett) | `F22_KAROLI_STRONG_BRIEF.md:8,10` | `allapot: dontesre_var`, új `kovetkezo`. A felhasználói utasítás nincs a repóban, a DT21 nem említi. |
| Gondolkodási mód (Keretek) | **ELTÉRÉS** (megjegyzés) | `futasnaplo.tsv` `gondolkodas_mod`; `futtat.py:31-32,130` | A brief szerint „mindhárom modellnél ugyanaz”, a valóságban A/B `kikapcsolva`, C `kotelezo_effort=minimal`. A kódban dokumentált, döntési tétel nincs róla. Az F1–F6 `gondolkodas_token=0` nem mérés: a token olvasása csak az F21.10-től él (2acaea7). A költség helyes, mert a `cost` mezőből jön. |
| Commit-üzenetek ékezete (CLAUDE.md) | **ELTÉRÉS** (megjegyzés) | — | 75496f0 „koteg … eles ut proba”, 6d94610 „futas … nelkul”, ac6fb49 „beolvasztasa”. |
| A1 memória vs. lekérdezés | OK | — | Az Opus-arany, a (c)-besorolás és a korrigált érték jelölt. Az 1Móz 13:4 „hibás” minősítése értelmezés. |
| A2 nyitott tételek | OK | DT21 a–h | A NYITOTT_FELADATOK-ot az ág nem érintette. |
| A3, A4, A5 | n.é. | — | Nem tanulmány, nincs párhuzam, PaRDeS vagy nevesített tanító. |
| A6 E12–E15 | OK | — | A saját CI-futásban 0 találat. |
| Ellenőrzőlista 1: törölt sorok | OK | — | Törlés > 0: DONTESEK 1 (DT18 újsor), F21 brief 3 (`allapot`, `kovetkezo`, a vegyes példa a P2-nél, a futás előtt), F22 2 (fejléc). Kiszűrt adatsor nincs. |
| Ellenőrzőlista 2: kulcstartomány | OK | — | Versek rétegenként 31158; a 61 eredeti nélküli vers (6+42+4+9) megjelölve. |
| Ellenőrzőlista 3: „nulla-diff” hatóköre | OK | — | Az `adat/`, `konkordancia/`, `FELADATOK.md`, `NYITOTT_FELADATOK.md` nulla-diffje csak ezekre a fájlokra vonatkozik. |
| Ellenőrzőlista 4: adattábla-sorszám (E17) | n.é. | — | `adat/*.tsv` nem változott. |
| Ellenőrzőlista 5: brief ⛔ (P2) | OK | — | 0459572 12:02 „megallt”, c91adfb 12:14 a döntések átvezetése, első trigger 12:35. |

## Eltérések súlyossági sorrendben

1. **Régi arany.** A futás utáni kizárás (PD9) a C régi arany eredményét 93,8%-ról (95% alatt) 100%-ra emeli. Az (a) tábla csak a kizárásos számot mutatja.
2. **A+B+C.** A vezető mondat és a `lezarva_osszegzes` „nem felel meg”-et állít. Mivel az öt feltételből egy sem mért, a pontos állítás „nem mért (PD8)”.
3. **Kapuhiba mint feltétel.** A kapuhiba „bukott”-ként szerepel, pedig nem tartozik az öt feltétel közé. Az A+B régi arany bukását viszont a (b) nem nevezi meg.
4. **P-K4.** A jelentés nem tartalmaz minden mérőszámot rétegenként és összeállításonként.
5. **Proveniencia.** A generált kimenetek többségéből hiányzik a `ts`, néhol a `scope` vagy a `forras` is.
6. **P5.6.** A bootstrap egysége a köteg a vers helyett. Nyitott tétel (DT21 f), nincs jóváhagyva.
7. **E16.** A PR csak „[ELLENŐRZŐ]” előtagú címmel lesz zöld.
8. Megjegyzés: a `lezarva_osszegzes` [38–47] intervalluma az F3-ból jön, az (a) tábla az F3V2-t idézi.
9. Megjegyzés: a gondolkodási mód eltér a modellek között; az F1–F6 gondolkodási tokenje nem mérés.
10. Megjegyzés: három commit-üzenet ékezet nélküli.

**NEM TISZTA**
