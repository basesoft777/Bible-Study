# F40 zárás — a hivatkozás-ellenőrző (E27) eredménye a main-en

*Állapot: az F40 ágon mért, a main tartalmával megegyező feladatkövető-fájlokon (`futtat.py --teljes`, minden találat JELENTES). A javítás nem ennek a menetnek a dolga (H4), a lista a takarítási ponthoz tartozik.*

## Eredmény

- A zöld/piros: PR-on a HIBA csak a diff által hozzáadott/módosított soron áll (D8); a main jelenlegi állapotán a szabály **zöld** (0 HIBA), a régi sorok JELENTES-ek.
- A teljes beolvasás 33 találatot ad: 2 ág, 2 commit, 27 fájl/könyvtár a `FELADATOK.md` / `NYITOTT_FELADATOK.md` soraiban, és 2 `olvas`-mező egy-egy briefben.
- Valószínű téves jelzés (nem repó-út, hanem adatkészlet-belső rövidítés): `base/display/`, `base/text-only/`, `base/hebrew-tsv/`, `text-only/`, `hebrew-tsv/` (NYITOTT_FELADATOK.md:612, 614). Ezeket a takarítás vagy kiveszi a backtickből, vagy a szabályba kivétel kerül.
- A `FELADATOK.md:20` `claude/f38-adag7` még nem létező, jövőbeli ág (a folytatás tervezett ága): a nyitott sorban HIBA lenne, ha a PR érinti azt a sort.

## Talált hivatkozások (fájl:sor — hivatkozás)

- `FELADATOK.md:20` — a hivatkozott ág nem létezik a távoli repóban: `claude/f38-adag7`.
- `FELADATOK.md:72` — a hivatkozott ág nem létezik a távoli repóban: `claude/forditas-pilot-brief-3afbbf`.
- `NYITOTT_FELADATOK.md:12` — a hivatkozott fájl/könyvtár nem létezik: `forditas_ubs.tsv`.
- `NYITOTT_FELADATOK.md:26` — a hivatkozott fájl/könyvtár nem létezik: `morphology_retriever.py`.
- `NYITOTT_FELADATOK.md:26` — a hivatkozott fájl/könyvtár nem létezik: `search_retriever.py`.
- `NYITOTT_FELADATOK.md:56` — a hivatkozott commit nem létezik: `47db250`.
- `NYITOTT_FELADATOK.md:63` — a hivatkozott fájl/könyvtár nem létezik: `Tehom_Abusszosz_Hadesz_Tartarosz_tematikus.md`.
- `NYITOTT_FELADATOK.md:114` — a hivatkozott fájl/könyvtár nem létezik: `adat/tanulmanyok.tsv`.
- `NYITOTT_FELADATOK.md:168` — a hivatkozott fájl/könyvtár nem létezik: `LXX_kivonat_README.md`.
- `NYITOTT_FELADATOK.md:190` — a hivatkozott fájl/könyvtár nem létezik: `LXX_kivonat_Genezis.tsv`.
- `NYITOTT_FELADATOK.md:219` — a hivatkozott fájl/könyvtár nem létezik: `_OLVASHATO.md`.
- `NYITOTT_FELADATOK.md:229` — a hivatkozott fájl/könyvtár nem létezik: `LXX_kivonat_Zsoltarok.tsv`.
- `NYITOTT_FELADATOK.md:237` — a hivatkozott fájl/könyvtár nem létezik: `LXX_kivonat_Zsoltarok.tsv`.
- `NYITOTT_FELADATOK.md:269` — a hivatkozott fájl/könyvtár nem létezik: `tematikus_lezart/naplok/Pneuma_pszukhe_megkulonboztetes_kereszthivatkozas_naplo.md`.
- `NYITOTT_FELADATOK.md:420` — a hivatkozott fájl/könyvtár nem létezik: `eszkozok/strong_util.py`.
- `NYITOTT_FELADATOK.md:461` — a hivatkozott fájl/könyvtár nem létezik: `TBESH_konszolidalt.tsv`.
- `NYITOTT_FELADATOK.md:526` — a hivatkozott fájl/könyvtár nem létezik: `kezi.tsv`.
- `NYITOTT_FELADATOK.md:612` — a hivatkozott fájl/könyvtár nem létezik: `base/display/`.
- `NYITOTT_FELADATOK.md:612` — a hivatkozott fájl/könyvtár nem létezik: `base/text-only/`.
- `NYITOTT_FELADATOK.md:612` — a hivatkozott fájl/könyvtár nem létezik: `base/hebrew-tsv/`.
- `NYITOTT_FELADATOK.md:612` — a hivatkozott fájl/könyvtár nem létezik: `text-only/`.
- `NYITOTT_FELADATOK.md:612` — a hivatkozott fájl/könyvtár nem létezik: `hebrew-tsv/`.
- `NYITOTT_FELADATOK.md:614` — a hivatkozott fájl/könyvtár nem létezik: `base/display/`.
- `NYITOTT_FELADATOK.md:614` — a hivatkozott fájl/könyvtár nem létezik: `base/text-only/`.
- `NYITOTT_FELADATOK.md:616` — a hivatkozott fájl/könyvtár nem létezik: `beerkezo/F66b_BDB_ARAM_BEEMELES_BRIEF_TERVEZET.md`.
- `NYITOTT_FELADATOK.md:692` — a hivatkozott fájl/könyvtár nem létezik: `main_frissit.py`.
- `NYITOTT_FELADATOK.md:717` — a hivatkozott commit nem létezik: `a4a2c05`.
- `NYITOTT_FELADATOK.md:720` — a hivatkozott fájl/könyvtár nem létezik: `forditas_ubs.tsv`.
- `NYITOTT_FELADATOK.md:723` — a hivatkozott fájl/könyvtár nem létezik: `forditas_ubs.tsv`.
- `NYITOTT_FELADATOK.md:776` — a hivatkozott fájl/könyvtár nem létezik: `Code_prompt_melkizedek_v12_audit.md`.
- `NYITOTT_FELADATOK.md:810` — a hivatkozott fájl/könyvtár nem létezik: `Atadasi_dokumentum_2026_09_07_TELJES.md`.
- `F46_BDB_KONYVFELOLDAS_BRIEF.md:14` — az `olvas` mezőben hivatkozott fájl nem létezik: `beerkezo/BDB_KONYVFELOLDASI_AUDIT.md` (lehet, hogy egy függő feladat állítja elő).
- `F64_TEREMT002_PROZA_PROBA_BRIEF.md:12` — az `olvas` mezőben hivatkozott fájl nem létezik: `naplok/MOTIVUM_FORRAS_lekepezes.tsv` (lehet, hogy egy függő feladat állítja elő).
