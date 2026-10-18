ELTÉRÉS: 2 tétel

# ELLENOR_F11_S — F11_MIGRACIO_BRIEF.md, S-tétel (S1 + S2)

Tartomány: `ca52ee58..0d9f1b89` (a `ca52ee58` = `origin/main`; a `0d9f1b89` = `origin/claude/f11-migracio`). Ellenőr: `claude-opus-5-5` (`fuggetlen-ellenor`).

*Mentési megjegyzés: az ellenőr szerepköre nem ír fájlt és nem futtat a `git diff`/`git log`/`lekerdez.py`/`futtat.py` körön kívüli parancsot; a jelentés szövegét az orkesztrátor mentette ide változatlanul, a „NEM ELLENŐRIZHETŐ” pontok pótló futtatása a végén, külön szakaszban áll.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | A tényleges modell `claude-opus-5-5`, a kért `opus`. A diff nem ír `modell` mezőt: a `kapcsolatok.tsv`-nek nincs ilyen oszlopa, napló nem változott. A commitok `Co-Authored-By: Claude Opus 5.5` sora a végrehajtó modelljét a git-ből nem igazolja: NEM ELLENŐRIZHETŐ, de nincs ellentmondás. |
| Commitok, tétel-azonosító, ékezet (7) | OK | — | `git log ca52ee58..0d9f1b89`: 4 commit, `F11.0`, `F11.S1`, `F11.S2`, `F11.S2`. Mind magyar, ékezetes, a végén Co-Authored-By. Az S1 (`d0baba60`: SEMA + tábla) és az S2 (`d05e52ef`: eszközök) külön commit (`git diff --numstat <c>~1 <c>`), így a 4. szakasz 1. pontjának „külön állnak” feltétele teljesül. |
| Csak `ir`-fájl (6) | OK | — | `git diff --numstat ca52ee58..0d9f1b89`: `F11_MIGRACIO_BRIEF.md` (a saját brief fejléce, CLAUDE.md szerint megengedett), `adat/SEMA.md`, `adat/kapcsolatok.tsv`, `eszkozok/ellenoriz.py`, `eszkozok/f3_1_betoltes.py`, `eszkozok/sqlite_epit.py`. Mind az `ir`-ben van (`F11_MIGRACIO_BRIEF.md:14`). |
| S1 / (1) régi 7 oszlop bájtra változatlan | OK | `adat/kapcsolatok.tsv:2-41` | `git diff ca52ee58..0d9f1b89 --word-diff=porcelain --word-diff-regex='[^\n]' -- adat/kapcsolatok.tsv`: karakterszinten soronként csak a sorvégi `+\tindoklas` (fejléc) és `+\t` (39 adatsor) a hozzáadás, törlés egy sincs. A komment-sor (1.) változatlan. Grep a head-fájlon: `^[^\t#][^\t]*(\t[^\t]*){7}$` → 40 sor (fejléc + 39 adatsor, pontosan 8 mező). `\t$` → 39 sor (az `indoklas` mindenhol üres). `(\t[^\t]*){8,}$\| $\|\r` → 0 (nincs 9+ mező, sorvégi szóköz, CR). A diffben nincs „\ No newline”, tehát a záró újsor megvan. |
| S1 meglévő sorok száma | OK | `adat/kapcsolatok.tsv` | Grep-számlálás: `\tISTENTISZT-001\t` = 25, `\tKIRALY-001\t` = 9, `\tTEREMT-002\t` = 5, összesen 39. Egyezik a brief S1 (25) és a commit-üzenet értékével. |
| S1 csv-mentes írás | NEM ELLENŐRIZHETŐ | — | Az író szkript a repón kívül futott, a diffben nincs. Az eredmény (lásd fent) megfelel a `split('\t')`/`'\t'.join()` írásnak, és nincs benne idézőjel-duplázás. |
| (2) SEMA 2.3 ↔ DT183 | OK | `adat/SEMA.md:305` | A diffben az új `indoklas` sor: szabad szöveg, nem kötelező, az utolsó oszlop, a meglévő sorokon üres. A `DONTESEK.md:258` (DT183, „a.”) is ezt írja: SEMA 2.3, a tábla fejléce, üres érték a meglévő sorokon, a #11 első tételeként. A sor a brief S1 szövegével is egyezik. |
| (2) SEMA 3.10.7 1. ↔ DT183 | OK | `adat/SEMA.md:1413-1414` | Az „Átvezetve (#11 S1, DT183 a)” kiegészítés a döntés „a.” opciójával egyezik. Új DT/N számot vagy helyőrzőt a diff nem hoz (`git diff`). |
| (3) olvasók/írók: lista | OK | `eszkozok/` | Grep `kapcsolatok` az `eszkozok/` alatt: 26 fájl. A pozicionális vagy rögzített oszlopszámú kezelés csak az `f3_1_betoltes.py`-ban volt (`assert len == 7`), és ez javítva lett (`:369`, `:385`). Név szerinti vagy prefix-pozíciós kezelés: `lexikon_general.py:2000-2026` (`G.tsv_beolvas`, `r['…']`, az `indoklas` nem renderelődik), `zaro2_kiejtes_potlas.py:115-156` (fejléc-index), `olvaso_pilot/bovites.py:481-487` (`r[0..6]`, `len(r)>6`), `olvaso_szerver/lekerdezesek.py:309` (explicit SELECT), `sqlite_epit.py:218, 475, 1182` (név szerint; rögzített DDL-oszloplista nincs: grep `pardes_szint\|indoklas` → csak a 236. sor). A `G.tsv_beolvas` (`general.py:247-248`) eltérő oszlopszámnál `ValueError`-t dob, tehát a 8 oszlop egységessége kikényszerített. |
| (3) `t2_2_teremt002_atvezetes.py` KeyError elérhetetlen | OK, pontosítással | `eszkozok/t2_2_teremt002_atvezetes.py:95-96, 141-142, 147` | A `:147` (`k[f] for f in kfej`, a `kfej` most 8 elemű, a javaslat-munkalap 7 oszlopos) valóban `KeyError: 'indoklas'`-t adna. A futás azonban a mai adaton korábban megáll. (a) Elsőként a `:95-96` őrnél („már minősített jelölt”): grep `adat/jeloltek.tsv`-n `^TEREMT-002\t` = 66 sor, és `^TEREMT-002\t[^\t]*\t[^\t]*\tnyitva\t` = 0 (a `dontes` a 4. oszlop, `jeloltek.tsv:2`). (b) Ha erre nem kerülne sor, a `:141-142` őr is megállítaná: a `naplok/T2_TEREMT002_kapcsolatok_javaslat.tsv:3-7` mind az 5 kulcsa megvan a `kapcsolatok.tsv`-ben (a diff 5 TEREMT-002 sora). A végrehajtó állítása tehát igaz, csak az első megállító őr nem az, amelyet megnevez. |
| (3) `olvaso_mockup/kinyer.py` „kimenete változatlan” | ELTÉRÉS (alacsony) | `eszkozok/olvaso_mockup/kinyer.py:19, 25-27, 37` | Az `olvas()` `dict(zip(fej, m))`-et ad, így a JSON-kimenet minden `kap` sora új `"indoklas": ""` kulcsot kap, és a `print(kap[0])` is megváltozik. A `d05e52ef` commit-üzenetének „a kimenetük változatlan” állítása erre a fájlra nem igaz. Hiba nem keletkezik, a fájl az `ir`-en kívül van, és a cél is helyes. Javítás nem kell, csak az állítás téves. |
| (4) nulla-diff, saját futtatás | NEM ELLENŐRIZHETŐ | — | A `bash eszkozok/nulladiff.sh` a megengedett parancskörön kívül esik, nem futtattam. Közvetett igazolás: a commit-üzenetben szereplő fej (`a464450c`, „WIP on …: d0baba60”) és a `d05e52ef` fája azonos. `git diff --stat a464450c d05e52ef`: üres. `git diff --stat d05e52ef 0d9f1b89`: csak a `F11_MIGRACIO_BRIEF.md` (1/1). Statikusan: a generátorok (`lexikon_general.py`, `general.py`) az `indoklas`-t nem olvassák (grep), a `torzscikk_general.py` pedig a lexikonoldalból dolgozik. |
| (4) a nulla-diff pontos hatóköre | OK (leírás) | `eszkozok/nulladiff.sh:42-50, 195` | `diff -r` a két oldal teljes generált `lexikon/` könyvtárán (`*_TUDOMANYOS.md` + `*_TORZSCIKK.md`), benne a HAMART-001 és az ISTENTISZT-001. Nem terjed ki: a `pardes.db`/SQLite-ra, az olvasó-szerverre, az `olvaso_mockup`/`olvaso_pilot` kimeneteire és a `naplok/`-ra. |
| (5) `ellenoriz.py` 0 hiba, a 15. szabály negatív próbája | NEM ELLENŐRIZHETŐ | `eszkozok/ellenoriz.py:741-755, 893` | Az `ellenoriz.py` futtatása a megengedett körön kívül esik. Statikusan: a `szabaly15_kapcsolatok_fejlec` a fejlécet a 8 elemű `KAPCSOLATOK_FEJLEC`-hez méri. A base-beli 7 oszlopos táblán ez szükségképpen SÉRTÉS, a head-en (`kapcsolatok.tsv:2`, lásd fent) RENDBEN. A `sqlite_epit.py:236` is meghívja. |
| (5) `feladatok.py ellenoriz` 0 hiba | NEM ELLENŐRIZHETŐ | — | A megengedett körön kívül esik. A `futtat.py` E27-je (hivatkozás) csak JELENTES/FIGYELMEZTETES szintű, és a diff fájljait nem érinti (lásd lent). |
| CI: `futtat.py --valtozott` | ELTÉRÉS (közepes) | `eszkozok/ellenoriz.py:0` | `python eszkozok/ellenorzes/futtat.py --valtozott F11_MIGRACIO_BRIEF.md adat/SEMA.md adat/kapcsolatok.tsv eszkozok/ellenoriz.py eszkozok/f3_1_betoltes.py eszkozok/sqlite_epit.py --diff-alap ca52ee58 --diff-fej 0d9f1b89` → EXIT=1. **E16 HIBA: 1**: „a PR erinti az ellenorzot (eszkozok/ellenoriz.py), de a cim nem "[ELLENŐRZŐ]" elotagu”. A szabály a `szabalyok.py:951-958`-ban van, és a `ellenorzes.yml:153-161` a HIBA-n bukik. A PR-t `[ELLENŐRZŐ]` előtagú címmel kell nyitni, különben a CI piros. Ezt sem a brief, sem a `kovetkezo` mező nem jelzi. Ezen kívül: E2–E15, E19, E20, E26 0 találat. E25: 3 JELENTES/FIGYELMEZTETES (CLAUDE.md, MUNKAMENET.md, nem a diff fájljai). E27: 40 JELENTES/FIGYELMEZTETES (FELADATOK.md ághivatkozások, nem a diffből). |
| CI: `futtat.py --teljes` | OK | — | `python eszkozok/ellenorzes/futtat.py --teljes --diff-alap ca52ee58 --diff-fej 0d9f1b89` → EXIT=0. Csak JELENTES szintű találatok, mind a diffen kívüli fájlokban (E2 7, E6 1, E8 32, E9 84, E11 9, E12 1876, E13 796, E25 3, E27 40). Az E1-et (`ellenoriz.py`) a `futtat.py` nem futtatja (`ellenorzes.yml:95-105`), lásd az (5) sort. |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | — | A bemenetben CI-jelentést nem kaptam, ezért nincs mivel összevetni. A saját futtatás eredménye a fenti két sorban áll. |
| Ellenőrzőlista 1: kiszűrt/törölt sorok | OK | `adat/kapcsolatok.tsv` | `git diff --numstat`: 40/40 a `kapcsolatok.tsv`-ben. Mind a 40 cserélt sor (fejléc 1 + adatsor 39), a karakter-diff szerint csak hozzáfűzéssel. Valódi törlés: 0, kiszűrt sor: 0. Más adattábla nem változott. |
| Ellenőrzőlista 2: kulcstartomány | OK | `adat/kapcsolatok.tsv` | Motívum-ID-k szerint 25 + 9 + 5 = 39 kulcs (grep), a diff előtt és után ugyanannyi. Strong-tartomány a diffben nincs. |
| Ellenőrzőlista 3: a nulla-diff hatóköre | lásd a (4) sort | — | A generált `lexikon/` igen, a DB, az olvasó és a naplók nem. |
| Ellenőrzőlista 4: sorszám-Δ (E17, DT3) | OK | — | `git diff --numstat ca52ee58..0d9f1b89`: az `adat/` és a `konkordancia/` alatt csak az `adat/kapcsolatok.tsv` változott, a fejlécsor nélkül 39 → 39, Δ = 0. Minden más `adat/*.tsv` és `konkordancia/*.tsv`: Δ = 0 (nincs a diffben). A küszöböt (±10) egyik sem éri el, bontási napló nem kell. Tájékoztatásul: az `eszkozok/olvaso_szerver/manifest_pardes_db.tsv:18` (`kapcsolatok 39 d2fafe8c…`) a `pardes.db` hash-másolata. A következő DB-újraépítéskor a `kapcsolatok` hash-e megváltozik (új oszlop), ez a DB-újraépítő feladaté, nem az S-é. |
| Ellenőrzőlista 5: ⛔ pontok | OK | `F11_MIGRACIO_BRIEF.md:12, 48, 52` | Az S3 ⛔ előtt a végrehajtó megállt (`kovetkezo: S3 ⛔ …, utána M1`). M-tételhez tartozó fájl (`naplok/F11_szetvalasztas_*`, `motivumok/ISTENTISZT-001.md`, sablonok) nincs a diffben. |
| Brief 4. szakasz 1. pont | NEM ELLENŐRIZHETŐ (S3 maga) | — | A feltétel az S3 zöld eredménye, ezt e jelentés dönti el. Lásd az első sort. |
| Brief 4. szakasz 6. pont (S-re) | NEM ELLENŐRIZHETŐ | — | A `feladatok.py` futtatása a megengedett körön kívül esik. Az E27 HIBA-mentes. |
| Brief D-pontok (DT215/b/c) | OK (nem esedékes) | `F11_MIGRACIO_BRIEF.md:78-80` | Az M3, a T3 és az M6 előtt esedékesek, az S-tétel nem érinti őket. A diff nem hoz helyőrzőt. |
| A1–A6 | nem alkalmazható | — | A diff értelmező prózát, tanulmányt, NYITOTT_FELADATOK-ot vagy nevesített tanítót nem érint. |
| Tanulmány-ellenőrzés (F37 T4) | nem alkalmazható | — | A diffben nincs `*_bovitett.md` vagy `*_tanulmany.md`. |

ELTÉRÉS-ek súlyossági sorrendben:

1. (közepes) E16 HIBA. A diff módosítja az `eszkozok/ellenoriz.py`-t, ezért a PR címének `[ELLENŐRZŐ]` előtaggal kell kezdődnie, különben az `ellenorzes.yml` CI bukik.
2. (alacsony) A `d05e52ef` commit-üzenete szerint az `olvaso_mockup/kinyer.py` kimenete változatlan. Valójában a JSON `kap` sorai új `indoklas` kulcsot kapnak. Hibát nem okoz, csak az állítás téves.

Pontosítás, nem ELTÉRÉS: a `t2_2` `KeyError`-ját a mai adaton elsőként a `:95-96` őr előzi meg, nem a `:141-142` őr. A végrehajtó a `:141-142` őrt nevezi meg, de az is megállítaná a futást.

Ítélet: **ELTÉRÉS** (2 tétel, lásd fent). A merge-ről a felhasználó dönt.

## Orkesztrátori pótló futtatás (a „NEM ELLENŐRIZHETŐ” pontokra)

Futtatta az orkesztrátor (`claude-opus-5-5`), 2026-10-18, a `claude/f11-migracio` ágon, fej `0d9f1b89`, tiszta munkafa:

| parancs | eredmény |
|---|---|
| `bash eszkozok/nulladiff.sh ca52ee58 2026-10-18` (`--csere` nélkül) | EXIT=0, „nulladiff: RENDBEN -- a ket oldal generalt lexikon/ konyvtara azonos” (a HAMART-001 és az ISTENTISZT-001 benne) |
| `python eszkozok/ellenoriz.py` | EXIT=0; RENDBEN: 12, SÉRTÉS: 0, KÉZI: 2, JELENTÉS: 3 |
| `python eszkozok/feladatok.py ellenoriz` | EXIT=0; 135 brief, 0 hiba, 0 figyelmeztetés |

A 15. szabály negatív próbáját az orkesztrátor nem ismételte meg (a végrehajtó jelentése szerint a 7 oszlopos táblán SÉRTÉS; az ellenőr statikus elemzése ugyanezt adja).

Az ELTÉRÉS-ek kezelése: (1) a PR címe `[ELLENŐRZŐ]` előtaggal nyílik; (2) a téves commit-üzenet-állítást ez a jelentés rögzíti, a pusholt commit nem íródik át. Kódjavítás egyikhez sem kell.
