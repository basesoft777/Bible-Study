# F40 zárás — a hivatkozás-ellenőrző (E27) eredménye a main-en

*Állapot: a DT-F40a/b szerinti javítás után (F40.5–), az F40 ágon mért, a main tartalmával megegyező feladatkövető-fájlokon. A javítás a talált hivatkozásokon nem ennek a menetnek a dolga (H4), a lista a takarítási ponthoz tartozik.*

## Eredmény (a DT-F40a/b utáni köztes állapot — a végleges a „DT-F40c végrehajtása” szakaszban áll; az itt jelzett 2 HIBA és a bukó teszt megszűnt)

- **`futtat.py --teljes`: 0 HIBA** (kilépési kód 0) — de ez a `--teljes` mód szerkezeti tulajdonsága: minden találatot JELENTES-re minősít (D3), tehát a 0 önmagában nem bizonyít. A nyers szint (`SZ.e27_hivatkozas()` közvetlen hívása, diff nélkül) a main mai állapotán: **2 HIBA, 1 FIGYELMEZTETÉS, 30 JELENTES**.
- A 2 HIBA a DT-F40a (b) szabály következménye: az `olvas`-mező hiányzó fájlja mindig HIBA, ha egy `fugg`-beli feladat `ir` mezője nem fedi. Ilyen az `F46_BDB_KONYVFELOLDAS_BRIEF.md:14` (`beerkezo/BDB_KONYVFELOLDASI_AUDIT.md`; az útvonalat az F38 `ir`-je tartalmazza, az F46 `fugg`-je viszont [34]; az F46 lezárt) és az `F64_TEREMT002_PROZA_PROBA_BRIEF.md:12` (`naplok/MOTIVUM_FORRAS_lekepezes.tsv`; az F64 `fugg`-je üres, az útvonal a #23 M0 kimenete, de az F23 `ir`-je nem fedi). **A felhasználói döntés („F46, F64 mostani jelzése figyelmeztetés”) feltevése nem teljesül, ezért a CI a main-en piros lenne: `DT-F40c` (🟡) vár döntésre.** A `test_push_ures_cimmel_nem_piros` (E16EsemenyTest) emiatt bukik: a valódi repón az E27 2 HIBÁJA az összesített jelentést pirossá teszi.
- Az 1 FIGYELMEZTETÉS: `FELADATOK.md:20` `claude/f38-adag7`, a tervezett (még nem létező) ág, nyitott sorban csak figyelmeztetés (DT-F40a (a)); az üzenet a forrás-briefet (`F38_BDB_FORDITAS_BRIEF.md`) nevezi meg.
- A 30 JELENTES a diff-hatókörű helyeken (`NYITOTT_FELADATOK.md`, a `FELADATOK.md` kézi/Kész sorai) lévő régi hivatkozás; a PR-ban nem érintett sorokon nem blokkol. A `NYITOTT_FELADATOK.md:612/614` adatkészlet-belső rövidítései (`base/display/`, `base/text-only/`, `base/hebrew-tsv/`, `text-only/`, `hebrew-tsv/`) a DT-F40a (f) szerint **nem kapnak kódbeli kivételt**: a takarítási pontba mennek (vagy kikerülnek a backtickből).
- Az előző (F40.3) zárólista 33 találata ugyanennyi, de a besorolás változott: az 1 FIGYELMEZTETÉS és a 2 HIBA a DT-F40a miatt.

## Eltérések a briefhez

- **DT-F40b:** a végrehajtó a brief 4. pontjánál (⛔ átfedés az E18-cal) nem állt meg, a D-ág a fejléc-érvényességet is ellenőrizte. A felhasználó döntése: a D-ág csak az `olvas` útvonalait ellenőrzi, a fejléc érvényessége az E18-é. A javítás: `_e27_fejlec_olvas` helyett a hibatűrő `_e27_fejlec_mezo` (hibás fejlécre üres listát ad, nem jelez); a tesztek hibás YAML-re 0 találatot és 0 kilépési kódot várnak.
- **Szabályszám:** E27 (a brief H5 szerinti E25 elavult: az E25 a döntés-átvezetés, az E26 a végleges szám az ágon).
- **Kódbeli kivételek** (a briefben eredetileg nem szerepeltek; most a brief 2. pontja alatt dokumentálva és tesztelve): rövid név bármely azonos nevű fájllal; kiterjesztés nélküli `a/b` csak létező első taggal; `beerkezo/` és `konkordancia/` briefjei kizárva a D-ágból; URL, ág és minta nem útvonal.
- **Tesztek:** a `_kilepes` segéd már a `futtat.py main()` valódi kilépési kódját méri (`--valtozott`, push-esemény, `--diff-alap/--diff-fej`), a brief 3. pontja minden esetére, a „csak chatben” és a hibás YAML esetre is.
- **Teszt-darabszám:** az `E27Teszt` 33 metódus (az előző diffben 16 volt, nem 15). `test_szabalyok.py` összesen 107 teszt (ebből 1 bukik: l. fent), `test_tanulmany.py` 32 OK, `teszt_feladatok.py` 99 OK. `feladatok.py ellenoriz`: 95 brief, 0 hiba.

## Talált hivatkozások (fájl:sor — [szint] hivatkozás)

- `FELADATOK.md:20` — [FIGYELMEZTETES] a hivatkozott ág nem létezik a távoli repóban: `claude/f38-adag7` (nyitott sor: a tervezett ág érvényes). A sor a generált blokkban áll; a javítás a forrás-briefben történik: `F38_BDB_FORDITAS_BRIEF.md`.
- `FELADATOK.md:72` — [JELENTES] a hivatkozott ág nem létezik a távoli repóban: `claude/forditas-pilot-brief-3afbbf`.
- `NYITOTT_FELADATOK.md:12` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `forditas_ubs.tsv`.
- `NYITOTT_FELADATOK.md:26` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `morphology_retriever.py`.
- `NYITOTT_FELADATOK.md:26` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `search_retriever.py`.
- `NYITOTT_FELADATOK.md:56` — [JELENTES] a hivatkozott commit nem létezik: `47db250`.
- `NYITOTT_FELADATOK.md:63` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `Tehom_Abusszosz_Hadesz_Tartarosz_tematikus.md`.
- `NYITOTT_FELADATOK.md:114` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `adat/tanulmanyok.tsv`.
- `NYITOTT_FELADATOK.md:168` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `LXX_kivonat_README.md`.
- `NYITOTT_FELADATOK.md:190` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `LXX_kivonat_Genezis.tsv`.
- `NYITOTT_FELADATOK.md:219` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `_OLVASHATO.md`.
- `NYITOTT_FELADATOK.md:229` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `LXX_kivonat_Zsoltarok.tsv`.
- `NYITOTT_FELADATOK.md:237` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `LXX_kivonat_Zsoltarok.tsv`.
- `NYITOTT_FELADATOK.md:269` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `tematikus_lezart/naplok/Pneuma_pszukhe_megkulonboztetes_kereszthivatkozas_naplo.md`.
- `NYITOTT_FELADATOK.md:420` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `eszkozok/strong_util.py`.
- `NYITOTT_FELADATOK.md:461` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `TBESH_konszolidalt.tsv`.
- `NYITOTT_FELADATOK.md:526` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `kezi.tsv`.
- `NYITOTT_FELADATOK.md:612` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `base/display/`.
- `NYITOTT_FELADATOK.md:612` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `base/text-only/`.
- `NYITOTT_FELADATOK.md:612` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `base/hebrew-tsv/`.
- `NYITOTT_FELADATOK.md:612` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `text-only/`.
- `NYITOTT_FELADATOK.md:612` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `hebrew-tsv/`.
- `NYITOTT_FELADATOK.md:614` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `base/display/`.
- `NYITOTT_FELADATOK.md:614` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `base/text-only/`.
- `NYITOTT_FELADATOK.md:616` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `beerkezo/F66b_BDB_ARAM_BEEMELES_BRIEF_TERVEZET.md`.
- `NYITOTT_FELADATOK.md:692` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `main_frissit.py`.
- `NYITOTT_FELADATOK.md:717` — [JELENTES] a hivatkozott commit nem létezik: `a4a2c05`.
- `NYITOTT_FELADATOK.md:720` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `forditas_ubs.tsv`.
- `NYITOTT_FELADATOK.md:723` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `forditas_ubs.tsv`.
- `NYITOTT_FELADATOK.md:776` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `Code_prompt_melkizedek_v12_audit.md`.
- `NYITOTT_FELADATOK.md:810` — [JELENTES] a hivatkozott fájl/könyvtár nem létezik: `Atadasi_dokumentum_2026_09_07_TELJES.md`.
- `F46_BDB_KONYVFELOLDAS_BRIEF.md:14` — [HIBA] az `olvas` mezőben hivatkozott fájl nem létezik: `beerkezo/BDB_KONYVFELOLDASI_AUDIT.md`, és egyik `fugg`-beli feladat `ir` mezője sem fedi.
- `F64_TEREMT002_PROZA_PROBA_BRIEF.md:12` — [HIBA] az `olvas` mezőben hivatkozott fájl nem létezik: `naplok/MOTIVUM_FORRAS_lekepezes.tsv`, és egyik `fugg`-beli feladat `ir` mezője sem fedi.

## DT-F40c végrehajtása (F40.9–)

- **Döntés (Felhasználó, 2026.10.07):** (a) lezárt brief `olvas`-mezőjében a hiányzó fájl FIGYELMEZTETÉS; (b) nyitott briefnél FIGYELMEZTETÉS, ha bármely nem lezárt feladat `ir`-je fedi (egyezés, könyvtár-előtag, joker), különben HIBA; (c) az F23 `ir`-je az öt M0-kimenettel bővül. Az F64 fejléce nem változott.
- **Kód:** `e27_hivatkozas` D-ága az `allapot` mezőt a terkepből és a vizsgált briefből olvassa; `_e27_brief_terkep` felvette az `allapot`-ot.
- **F23 `ir`-bővítés:** `naplok/MOTIVUM_FORRAS_lekepezes.tsv`, `_torzscikk_egyedi.tsv`, `_parositas.tsv`, `_naplo_keveredes.tsv`, `_atfedes.tsv`; az F23 verziónaplójában v1.4. Az `allapot` és a `fugg` nem változott.
- **Eredmény:** az E27 nyers szintje (`SZ.e27_hivatkozas()`, diff nélkül) a main tartalmán 0 HIBA; a fenti „2 HIBA” (F46, F64) megszűnt. Az F46 FIGYELMEZTETÉS (lezárt), az F64 FIGYELMEZTETÉS (az F23 `ir`-je fedi).
- **Tesztek:** a `test_olvas_hiba_ha_a_fedo_feladat_nincs_a_fuggesek_kozott` a DT-F40c (b) szerint megfordult (nem `fugg`-beli fedés is FIGYELMEZTETÉS); új: lezárt feladat `ir`-je nem fed (HIBA), joker, lezárt brief (FIGYELMEZTETÉS, kilépés 0), fedetlen nyitott brief (HIBA, kilépés 1). A kilépési kódok a `futtat.py main()` valódi kilépési kódjai.

- **Végleges tesztszám (ellenőr 2. kör, mérve):** `E27Teszt` 37 metódus, `test_szabalyok.py` összesen 111 teszt, mind OK (a fenti „33 / 107, 1 bukik” köztes adat). Az F46 és F64 sora a fenti listában a köztes [HIBA] besorolású; végleges: FIGYELMEZTETES.
- **Ellenőrzés:** `naplok/ELLENOR_HIVATKOZAS.md` (1. kör) és `naplok/ELLENOR_HIVATKOZAS_2.md` (2. kör). B-ellenőrzés Actions-tokennel: az első CI-futáson derül ki.
