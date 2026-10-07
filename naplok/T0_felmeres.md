# T0 — felmérés (F37 TANULMANY_ELLENORZES)

*2026.10.07 · `claude/tanulmany-ellenorzes` · csak olvasó lépés; a mérő szkriptek a repón kívül futottak (scratchpad), a számok forrása a lent megnevezett fájl. Proveniencia: `scope=T0 felmérés | forras=a sorokban megnevezett fájlok | ts=2026-10-07` (mért, nem lekérdező CLI-ből).*

## Eredmény a ⛔ pontokra

| ⛔ feltétel | Lelet | Megállás? |
|---|---|---|
| nincs Strong-jelölt eredeti szöveg | van: héber (TAHOT, Macula-héber), görög ÚSZ (TAGNT, Macula-görög), görög LXX (LXX_OS) — l. 6. pont | nem |
| az SzPA kötelező szakasz a Tanulmány sablonban | nem szakasz: két említés a 2. pont kiválasztási kritériumában és a formai szabályok között — l. 8. pont | nem |
| a T0 mégis alap tanulmányt talál | nincs: a repóban csak `_bovitett.md` tanulmány van, a git-történetben (minden ág, A/D szűrő) sincs törölt `*_alap.md` | nem |

## 1. Sablonfájlok

| Sablon | Fájl | Megjegyzés |
|---|---|---|
| Tanulmány sablon (eddig: bővített) | `sablonok/2_PaRDeS_bovitett_sablon.md` (v19, 297 sor) | a T1 itt nevezi át; a fájlnév marad (sok hivatkozás, a `datasetek.tsv` `bovitett` study_tipus kulcsa) |
| alap sablon | `sablonok/1_PaRDeS_alap_sablon.md` (77 sor) | a T1 elavultnak jelöli, nem törli |

A Tanulmány sablon `##` szakaszai (az E20 ebből olvas): `0. Sorozat-kontextus` *(feltételes)*, `1. Alapkérdések`, `1/b. Idővonal / térkép` *(feltételes)*, `2. Eredeti nyelvi szöveg`, `3. PaRDeS keretrendszer`, `4. Kapcsolódó igehelyek`, `5. Rabbinikus és patrisztikus hangok`, `6. Kiegészítő szempontok`, `7. Lexikai audit — módszertani napló` *(feltételes)*; plusz két számozatlan, minden sablonra érvényes szabályszakasz (`Terminológiai és formai szabályok`, `Konfliktuskezelés`), amely nem tanulmányszakasz.

## 2. Tanulmányfájlok (23, mind bővített)

- `genezis/` (20): `1Moz_1v1`, `1Moz_1v2-2v3`, `1Moz_2v4-7`, `1Moz_2v8-25`, `1Moz_3v1-6`, `1Moz_3v7-24`, `1Moz_4v1-24`, `1Moz_4v25-5v32`, `1Moz_6v1-8`, `1Moz_6v9-22`, `1Moz_7v1-24`, `1Moz_8v1-22`, `1Moz_9v1-17`, `1Moz_9v18-29`, `1Moz_10v1-11v32`, `1Moz_12v1-20`, `1Moz_13v1-18`, `1Moz_14`, `1Moz_15`, `1Moz_16` — mind `_bovitett.md`.
- `ujszovetseg/` (3): `1Thessz_5v23`, `Rom_8v10`, `Zsid_4v12` — mind `_bovitett.md`.
- Kereszthivatkozás-napló csak kettőhöz van: `genezis/naplok/1Moz_1v1_…`, `genezis/naplok/1Moz_1v2-2v3_…`.
- Nem tanulmány, bár a könyvtárban áll: `genezis/Konnyu_ellenorzes_1-16_osszesito*.md` (összesítők).
- Alap tanulmány: **nincs** (`git ls-files | grep _alap` → csak a sablon; `git log --all --diff-filter=AD --name-only` → nincs törölt `*_alap.md`).

Szakasz-felmérés: mind a 23 tanulmány tartalmazza a sablon 1–6. szakaszát; a 7. (feltételes) a 3 ÚSZ-tanulmányból hiányzik. Sablonon kívüli `##` szakaszok 13 tanulmányban: önellenőrzés (11×, ebből 7 „Formai önellenőrzés”), „Terminológiai és formai szabályok” (2×), „Javasolt / Motívum-napló frissítés” (2×), „Kiegészítés (2026.08.01)”, „Következő lépés”, „Javasolt következő igeszakasz”, „Belső önellenőrzés”, „3/d. Későbbi protestáns hagyomány” (tartalmi), „⚠️ Megjegyzés — …”, és egy második, „Bővített PaRDeS tanulmány” című `##` (1Moz_10v1-11v32).

## 3. CI-szabályok helye, utolsó E-szám

| Szabály | Hely |
|---|---|
| E1 (SEMA §3, Q1, Q7) | `eszkozok/ellenoriz.py --study` (a workflow külön lépése) |
| E2–E16, E19, E25, E26 | `eszkozok/ellenorzes/szabalyok.py`, futtató: `eszkozok/ellenorzes/futtat.py`, tesztek: `eszkozok/ellenorzes/tesztek/test_szabalyok.py` |
| E17 | csak név (DT3 sorszám-változás küszöb, a `fuggetlen-ellenor` 4. ellenőrzőpontja), nincs kódja |
| E18 | `eszkozok/feladatok.py ellenoriz` (külön job) |
| workflow | `.github/workflows/ellenorzes.yml` |

**Utolsó használt E-szám: E26.** Az E20–E24 a `szabalyok.py` E26-os megjegyzése szerint erre a feladatra foglalt (F40 H5, F51 is így számolt), tehát az új szabály(ok) az E20-tól kaphatnak számot.

### A tervezett szabályok összevetése a meglévőkkel (DT-F37-8: átfedésnél bővítés)

| Terv | Meglévő | Átfedés | Javaslat (a T3 ezt hajtja végre) |
|---|---|---|---|
| E20 szakaszlista a sablonból | E1/Q1 (`ellenoriz.py`): `## 1.`–`## 6.` beégetve, csak a `motivumok.tsv` `forras_study` fájljain (tematikus); E6: tematikus „0. Forrás-összegyűjtés” | részleges (cél azonos, fájlkör és listaforrás más; a Q1 beégetett listája ellentmond a DT-F37-6-nak, a `ellenoriz.py` a `ir` listán kívül esik) | **új szabály: E20**, tanulmányfájlokra, a sablonból olvasott listával |
| E21 kiejtés | E13 (FIGYELMEZTETES; csak a sor első héber/görög futamát nézi; a táblázat következő cellájában és a `, *átírás*` alakban álló kiejtést nem ismeri fel) | teljes | **E13 bővítése:** a sor minden futama; elfogadott alakok bővítése; tanulmányfájlon HIBA, máshol FIGYELMEZTETES marad |
| E22 versformátum | E8 (HIBA, minden `.md`): `1 Móz`, `1. Móz`, `ApCsel.`, `2. Sám` stb. | teljes, de rés van: az `1 Mózes 3:1` (a `\bMóz\b` nem illeszkedik a `Mózes`-re), az `1Mózes 12:1` és a STEPBible-alak (`Gen.12.7`) átmegy | **E8 bővítése** tanulmányfájlon: `\d ?Mózes \d+:` és a STEPBible-alak (`Gen.12.7`) is tiltott; más fájlon nem, mert ott a STEPBible-alak adatformátumként legitim (CLAUDE.md, briefek) |
| E23 „sense” | E9 (HIBA, minden `.md`; kizárja a blockquote-ot és az idézőjeles szöveget) | teljes; rés: a tanulmányban a blockquote a 🔗 kereszthivatkozás-blokk, benne magyar magyarázó sorral | **E9 bővítése:** tanulmányfájlon a blockquote nem kizárt (az idézőjeles szöveg igen) |
| E24 `【NAPLO】` | E12 (FIGYELMEZTETES, a `【NAPLO】` blokkon kívüli prózai proveniencia: dátum, `.tsv`/`.md`, „audit során”, „visszaírva”, „felismerve”, „l. N. pont”) | teljes (ugyanaz a kérdés: naplójellegű szöveg a blokkon kívül) | **E12 bővítése**, FIGYELMEZTETES marad (a felismerés bizonytalan) |

### Az E24 (→ E12) felismerésének javaslata

Mérés a 23 tanulmányon: `【NAPLO】` blokk 1 fájlban (`1Moz_4v1-24`), egyetlen helyen; az E12 meglévő mintái 172 sort jeleznek 23 fájlban. A naplójellegű szöveg három típusa jelenik meg:
1. **verziósor a fejlécben** (`*v4 — 2026.09.03 (…)*`) — a dátum-minta már elkapja;
2. **sablonon kívüli napló-szakasz** (`## Formai önellenőrzés (elvégezve)`, `## Motívum-napló frissítés`, `## Kiegészítés (2026.08.01)`, `## Következő lépés …`) — ma semmi nem jelzi;
3. **folyamatleíró mondat a prózában** („retroaktív ellenőrzés”, „Code-prompt”, „visszamenőleges pótlás”, „commit”).

Javaslat: az E12 tanulmányfájlon a 2. és 3. típus mintáit is jelezze (címsor: önellenőrzés / napló-frissítés / kiegészítés / következő lépés; próza: retroaktív, visszamenőleges, Code-prompt, commit). Mivel a 3. típus határa bizonytalan (a „retroaktív” tartalmi szó is lehet), a szabály **csak figyelmeztet**.

## 4. A `fuggetlen-ellenor` ügynök definíciója

`.claude/agents/fuggetlen-ellenor.md` (80 sor). Szerkezet: bemenet, szerep, Bash-korlát (`git diff`, `git log`, `lekerdez.py`, `futtat.py`), kimenet `naplok/ELLENOR_<tétel>.md`, kötelező ellenőrzőlista 1–5. Tanulmány-ellenőrző szakasza nincs. A #45 (`F45_MODELL_ELLENORZES_BRIEF.md`) is ezt a fájlt írja; a T4 csak új, önálló szakaszt ad hozzá, a meglévő szakaszokat nem érinti.

## 5. A „Bővített” szó élő előfordulásai

`git ls-files` (a `konkordancia/` és minden `naplok/` könyvtár nélkül), kis-nagybetű függetlenül: **307 előfordulás, 100 fájlban.** Ennek nagy része nem a sablon neve, hanem a tanulmánytípus („bővített tanulmány”), a fájlnév-utótag (`_bovitett`) vagy a köznyelvi „bővített” (bővítve). Csoportok:

| Csoport | Fájlok | Sors a T1-ben |
|---|---|---|
| a **„Bővített sablon”** név (template-név) élő fájlban | `sablonok/2_…` (cím, 207. sor), `sablonok/1_…` (2), `sablonok/3_…`, `sablonok/4_…` (4), `sablonok/5_…` (3), `sablonok/PaRDeS_gyorsreferencia.md` (2), `sablonok/PaRDeS_tanitok_lista.md`, `sablonok/Javasolt_sablon_kiegeszites_BDB_arnyalat.md` (7), `Join_tabla_folyamat_magyarazat.md` (3), `adat/SEMA.md` (548), `ATALAKITASI_TERV.md.md` (591) | átnevezés „Tanulmány sablon”-ra |
| lezárt brief | `F8_BRIEF.md` (lezarva), `F05`, `F26`, `F4_GENERATOR` (lezarva) | marad (lezárt dokumentum) |
| archívum, changelog | `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md`, `…_join_adatcsatorna.md`, `PaRDeS_dontesek_CHANGELOG.md`, `motivumlog/PaRDeS_motivumok_CHANGELOG.md` | marad |
| tanulmány, lezárt tematikus, mélyelemzés | `genezis/`, `ujszovetseg/`, `tematikus_lezart/`, `melyelemzesek/` | marad: a régi tanulmányok javítása nem tartozik ide (a T6 utófeladata) |
| generált | `lexikon/`, `generalt_proba/`, `motivumlog/lexikon_pilot/`, `FELADATTERKEP.html`, `feladatterkep.json` | marad (kézzel nem szerkeszthető) |
| tanulmánytípus („bővített tanulmány”) és adatkulcs (`bovitett`) | `MUNKAMENET.md`, `adat/SEMA.md` 556, `ATALAKITASI_TERV.md.md` (25), `adat/elofordulasok.tsv`, `adat/forditasok.tsv`, `eszkozok/*.py`, `NYITOTT_FELADATOK.md`, `DONTESEK.md`, `ADATVAGYON_TERV.md`, `GitHub_feltoltesi_workflow.md` | marad: nem a sablon neve; az adatkulcs átnevezése adatmigráció lenne |
| napló jellegű kézi fájl | `motivumlog/Bibliai_Motivumlexikon_tervezesi_naplo.md`, `sablonok/Kockazat_szures_riport_2026-09-03.md`, `MEGVALOSITAS_NAPLO.md` | marad (lezárt napló, ill. keltezett jelentés) |

*Megjegyzés:* a sablonok közül a `3_`, `4_`, `5_`, `PaRDeS_gyorsreferencia.md`, `PaRDeS_tanitok_lista.md` és a `Javasolt_sablon_kiegeszites_BDB_arnyalat.md` nincs a brief `ir` listáján, de a T1 a „sablonfájl” kategóriát nevezi meg, és az elfogadási feltétel („a név élő hivatkozásban nem fordul elő”) enélkül nem teljesül; ezért a T1 ezeket is átírja, csak a sablon nevét érintő helyeken (a jelentésben jelezve).

## 6. Strong-jelölt eredeti szöveg a repóban

Lefedettség: a Károli 1908 verseihez mérve (`konkordancia/Karoli_1908.tsv`: ÓSZ 23 050 vers, ÚSZ 7 954 vers; a Siralmak könyve a Károliban `Sir`, a normalizáló táblában `JSir`, ezért a 154 verse a mérésből kimaradt).

| Nyelv | Fájl | Versek (Károli-metszet) | Lefedettség | Teljesen hiányzó Károli-fejezet |
|---|---|---|---|---|
| héber | `konkordancia/TAHOT_kivonat.tsv` | 22 998 / 23 050 | 99,8% | Jób 41 (verzifikáció) |
| héber | `konkordancia/Macula_heber_*.tsv` (38 könyvfájl) | 22 877 / 23 050 | 99,2% | 9 (4Móz 30, Hós 13–14, Jób 17, Préd 5, Péld 12, Zsolt 13, Én 5, Ézs 4 — verzifikációs eltolás) |
| görög ÚSZ | `konkordancia/TAGNT_kivonat.tsv` | 7 945 / 7 954 | 99,9% | — |
| görög ÚSZ | `konkordancia/Macula_gorog.tsv` | 7 940 / 7 954 | 99,8% | — |
| görög LXX | `konkordancia/LXX_OS/*.tsv` (61 fájl) | 22 208 / 23 050 | 96,3% | 19 (pl. 2Móz 35–36, Jer 33, Jer 48, Jób 37–38 — LXX-verzifikáció) |

A tanulmány-ellenőrzés (T4 1. pont) elsődleges forrása a **TAHOT** (héber) és a **TAGNT** (görög ÚSZ): ugyanaz a Károli-alakú igehely-kulcs (`1Móz 12:2`), és a `lekerdez.py scan --szakasz` is ezekből olvas.

*Eltérés a `CLAUDE.md`-től (jelentve, nem javítva):* a `CLAUDE.md` szerint a TAHOT-kivonatból hiányzik „legalább 1Móz 32, Zsolt 88/89/140/142, Jóel 3”. A mai fájlban az 1Móz 32 (700 szósor), a Zsolt 88 (223) és a Jóel 3 (414) megvan; teljes fejezet csak a Jób 41 hiányzik. A `CLAUDE.md` állítása elavultnak látszik — utófeladat-jelölt (`CLAUDE.md` „Adat-tár” bekezdés).

## 7. Szótári réteg

| Réteg | Fájl | Kulcsok | Formátum |
|---|---|---|---|
| TBESH (héber, Abridged BDB alapú) | `konkordancia/TBESH.txt` | 9 345 eStrong-kulcs | tab: `eStrong`, `dStrong = …`, `uStrong`, héber alak, átírás, morfológia, glossza, definíció |
| TBESG (görög, Abbott-Smith alapú) | `konkordancia/TBESG.txt` | 10 847 eStrong-kulcs | ugyanígy, görög alakkal |
| leírás | `konkordancia/TBESH_TBESG_README.md` | — | licenc CC BY 4.0; lekérdezés: `grep "^H0001" konkordancia/TBESH.txt` |

## 8. SzPA-előfordulások (az SzPA kivezetve, 2026.10.01)

| Fájl | Hely | Jelleg |
|---|---|---|
| `sablonok/2_PaRDeS_bovitett_sablon.md` | 96. sor: a kiválasztás 2. szempontja „Elmosódás a Károli/SzPA fordításban” | kritérium-szöveg, **nem szakasz** |
| ugyanott | 289. sor: „A Szent Pál Akadémia-fordításból csak rövid idézetek …” | formai szabály, **nem szakasz** |
| ugyanott | 47. sor (v8 changelog): a `PaRDeS_STEPBible_SzPA_…` fájlnév | changelog |
| `CLAUDE.md` | 12. és 16. sor: az archív `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` és a „felfüggesztett SzPA-join dokumentáció” olvasási tilalma | hivatkozás archívumra |
| `MUNKAMENET.md` | — | nincs |
| CI | `szabalyok.py` E15 (SzPA-idézet hossza > 25 szó) | élő szabály egy kivezetett forrásra |

Nem javítva (a brief szerint csak jelentendő). Javaslat a T6 utófeladatához: a két sablonsor és az E15 sorsa.

## 9. Utófeladat-javaslat: `ATALAKITASI_TERV.md.md`

A fájl kiterjesztése dupla (`.md.md`). Nem javítva: a `CLAUDE.md` és több brief ezen a néven hivatkozik rá (a javítás minden hivatkozás egyidejű átírását kívánja), ezért külön utófeladat.
