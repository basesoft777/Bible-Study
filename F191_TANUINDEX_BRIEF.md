---
feladat: 191
cim: Tanúindex a visszhang-réteghez (egyházatyai és rabbinikus, szöveg nélkül)
kod: TANUINDEX
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: fut
ad: metaadat-szintű, helyi tanúindex (egyházatyák: HCF; rabbinikus: Sefaria links), amelyből a #183 a 9. „Hatástörténet” szakasz tanúrétegét webes keresés nélkül építheti
kovetkezo: "Folytatás: a független ellenőrzés és a draft PR; a merge a felhasználóé"
munka: adat
olvas: [CLAUDE.md, Rendszerfejlesztesi_playbook.md, konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, adat/elofordulasok.tsv]
ir: [nyilt_mag/, eszkozok/tanu_index.py, eszkozok/teszt_tanu_index.py, konkordancia/Tanu_atyak_index.tsv, konkordancia/Tanu_atyak_mu.tsv, konkordancia/Tanu_rabbinikus_index.tsv, konkordancia/Tanu_index_README.md, adat/datasetek.tsv, adat/licencek.tsv, nyitott/uj/tanuindex-8ed546.md, dontesek/uj/tanuindex-8ed546.md, naplok/F191_jelentes.md]
fugg: []
nem_fugg: [38, 123, 146, 182]
---

# F191_TANUINDEX_BRIEF.md — Tanúindex a visszhang-réteghez

*FELADATOK #191 · Modell: sonnet · v1 · 2026.11.11*

*Az orkesztrátor indította, külön sessionben, a szabályos úthoz, ugyanezen az ágon; befogadás nélkül. A felhasználó jóváhagyása (2026-11-11), szó szerint.
A kérdés: „Letöltés: a HCF Commentaries-Database SQLite-ja (github.com/HistoricalChristianFaith, kb. 176 MB) és a Sefaria links CSV-k (Sefaria-Export, kb. 0,7 GB),
előtte a licencük ellenőrzésével. A nyers fájlok a repón kívül maradnak, a repóba csak a szűrt index kerül. Mehet?” A válasz: „mehet”.*

## 1. Cél

A #183 a HAMART-001 lap 9. szakaszát („Hatástörténet: ókori fordítások és értelmezők”) építi; a tanúréteg (egyházatyák, rabbinikus) ma motívumonként webes keresést
igényelne. Ez a feladat helyi, szöveg nélküli indexet ad, minden későbbi lapra újrahasznosíthatón.

## 2. Hatókör

**Benne van:** HCF `commentaries.sqlite` és Sefaria links CSV letöltése a repón kívülre (`D:\pardes_tanu\`), a licencek ellenőrzése előtte; a kinyerő szkript és tesztje; a két
index, a dataset- és licencsor, a README; HAMART-minta.
**Nincs benne:** `eszkozok/visszhang/`, `konkordancia/VISSZHANG_README.md` (a #183 írja; javasolt mutató-sor: „A tanúréteg helyi indexe: `konkordancia/Tanu_index_README.md`,
lekérdezés `python eszkozok/tanu_index.py keres \"<igehely>\"`”); Sefaria-szöveg, CCEL-szöveg, idézetszöveg; Glossa Ordinaria; új licencdöntés.

## 3. Lépések és mért eredmény

1. Modell-ellenőrzés (`claude-sonnet-5-5` = a kért); felmérés, playbook 2. pont.
2. **Licenc.** HCF: a `LICENSE` „PUBLIC DOMAIN DEDICATION” a metaadatra, a „FAIR USE NOTICE” az idézetekre → csak metaadat. Sefaria links: a fejlesztői oldal „Links License” szakasza
   „CC-BY” (a verzió nincs megadva; a szerkesztő CC BY-ként elfogadta, DT740, N-F191c lezárva); a `LICENSE.md` csak a szövegekről szól. Mindkét nyers fájl letöltve (HCF 176 242 688 bájt, Sefaria 18 CSV
   ~680 MB), sha256 a README-ben.
3. **Index.** `Tanu_atyak_index.tsv` + `Tanu_atyak_mu.tsv` (97 572 sor, 9,5 MB; a teljes kanon), `Tanu_rabbinikus_index.tsv` (5 259 sor, 0,5 MB; a teljes Tanakh 24 MB lenne → első körben csak a
   lexikonmotívumok 289 versével átfedő sorok, N-F191a). A rabbinikus kategóriák: Midrash, Talmud, Mishnah, Tosefta, Targum.
4. **Szkript és teszt:** `eszkozok/tanu_index.py` (`epit-atyak`, `epit-rabb`, `keres`, `minta`), `eszkozok/teszt_tanu_index.py` (22 teszt, zöld).
5. Egy független ellenőrzés, legfeljebb egy javítókör; jelentés (`naplok/F191_jelentes.md`), draft PR.

## 4. Elfogadási feltételek

- A repóba nem kerül idézet- vagy Sefaria-szöveg (teszt: `test_atyak_szoveg_nelkul`, a fejlécek és a mezőhossz-vizsgálat).
- Minden index fejléce: forrás-URL, sha256, licenc, proveniencia (`scope=… | forras=… | ts=…`); `datasetek.tsv` és `licencek.tsv` sor.
- A HAMART-minta (1Móz 3:17, 4:7, 4:11, 6:5, 6:11) a jelentésben; az atyai pontos darabszámok egyeznek a felmérés kézi mérésével (8/4/2/2/1).

## 5. Döntésnapló

DT740 (🟢): a Sefaria links CC BY-ként elfogadva (a letöltést a felhasználó jóváhagyta). Nyitott: N-F191a (rabbinikus hatókör), N-F191b (UT-átvezetés), N-F191c (lezárva, DT740), N-F191d (középkori kommentárok).
