---
feladat: 186
cim: A Thayer-hozzárendelés (vers → jelentéspont) mérése és javítása 97% fölé, vak méréssel igazolva
kod: THAYER_JELENTESPONT_97
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: megallt
ag: claude/f186-thayer-jelentespont-97
ad: a vers → Thayer-jelentéspont hozzárendelés vak méréssel mérve (seed-201), hibaosztályonként javítva, és új vak mérésen (seed-202) ≥ 97%, előre rögzített kapuval; a megváltozott Thayer-szakaszkulcsok tételes listája a jelentésben
kovetkezo: "Te: /elteres 186"
olvas: [eszkozok/thayer_jelolt/, F132_THAYER_SZAKASZ_BRIEF.md, F185_BDB_JELENTESPONT_97_BRIEF.md, naplok/BDB_SZELETELO_M2_seed101_iteletek.md]
ir: [eszkozok/thayer_jelolt/bont.py, eszkozok/thayer_jelolt/vers_jelentes.py, eszkozok/thayer_jelolt/teszt_bont.py, eszkozok/thayer_jelolt/teszt_vers_jelentes.py, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, adat/thayer_forras_javitas.tsv, adat/thayer_aranyminta.tsv, adat/SEMA.md, naplok/F186_jelentes.md, naplok/ELLENOR_F186.md, adat/forditasok.tsv, eszkozok/thayer_jelolt/teszt_lanc.py, eszkozok/thayer_jelolt/forras_javit.py, eszkozok/thayer_jelolt/forditas_atkulcsol.py, eszkozok/thayer_jelolt/teszt_forditas_atkulcsol.py, eszkozok/ellenoriz.py, eszkozok/teszt_ellenoriz_13.py, naplok/F132_THAYER_SZAKASZ_munka.tsv, dontesek/uj/f186-thayer-jelentespont-97.md, nyitott/uj/f186-thayer-jelentespont-97.md, naplok/F186_zaras.md]
fugg: []
---

> **Felosztás (befogadás, 2026-11-10, orkesztrátori jóváhagyással).** Ez a brief a lenti tervezet **T0–T4 és T6** tétele. A **T5** (a kétrétegű kártya Thayer-ága) és a T4-ből a „szó-lapra a mért szám” rész a **#187**-é (`F187_THAYER_KARTYA_BRIEF.md`, `fugg: [104, 186]`); a `fugg: [104]` ezért itt nem áll.
>
> **Előfeltétel/hatás (orkesztrátori döntés, 2026-11-10).** A #7 (THAYER_ELES) a `adat/thayer_szakaszok.tsv`-t olvassa, és szakaszonként fordít. A #7 következő fordítási adagja csak a #186 merge-e után indulhat. A #186 a jelentésében (`naplok/F186_jelentes.md`) **tételesen felsorolja, mely Thayer-szakaszkulcsok változtak**; az érintett fordítássorok a meglévő mechanizmussal `elavult` állapotba kerülnek, kézi átírás nincs. (A #153 és a #158 is olvassa a táblát: automatikus FUGGES.)

# Brief-tervezet — A Thayer jelentéspont-hozzárendelés a BDB szintjére: mérés, javítás ≥ 97%, kétrétegű olvasói kártya (THAYER_JELENTESPONT)

*Orkesztrátori tervezet, 2026-11-10. A felhasználó kérése: „csináljuk meg a thayer szeletelőjét is”. Befogadásra (`/befogad`, külön sessionben). A cél, hogy a görög oldal (Thayer) ugyanazt a szintet érje el, amit a héber (BDB) a #102–#105, #185 láncban: mért, ≥ 97%-os vers → jelentéspont hozzárendelés, és olvasóbarát kétrétegű megjelenítés a lexikonlap 4.2-es szakaszában.*

**Javasolt fejléc [javaslat]:**
- `tipus: feladat`, `fazis: folyamat`, `modell: opus`, `munka: folyamat`
- `fugg: [104]` — a lapgenerátor 4.2-es része közös a #104-gyel, a kétrétegű kártya és a kapcsoló onnan jön
- `nem_fugg`: a #105 és a #185 BDB-oldali, a befogadó vezesse le a fájlütközést
- `olvas` / `ir`: a befogadó vezesse le. Fő fájlok:
  - `eszkozok/thayer_jelolt/bont.py`, `eszkozok/thayer_jelolt/vers_jelentes.py` és a tesztjeik
  - `adat/thayer_szakaszok.tsv`, `adat/thayer_vers_jelentes.tsv`, `adat/thayer_forras_javitas.tsv`
  - új aranyminta-tábla (`adat/thayer_aranyminta.tsv`)
  - `eszkozok/lexikon_general.py` (a görög 4.2, a #104 kártyájának Thayer-ága)
  - `eszkozok/olvaso_szerver/blokkok.py` (a mért pontosság)
  - `adat/SEMA.md`, `naplok/F<nn>_jelentes.md`

## Kiindulás
- **#132 (lezárva):** `adat/thayer_szakaszok.tsv` (17 093 szakasz, 5 426 Strong), `adat/thayer_vers_jelentes.tsv` (63 953 sor), javítótábla 15 Strongra. **Pontosságmérés nincs**, a zárójelentés csak teszteket és kapukat említ.
- **BDB-minta, ehhez kell igazodni:**
  - seed-101/102 vak mérés, véletlen 200 vers, két független Opus-kitöltő, kapu ≥ 97%;
  - hibaosztályok: fejfelismerés, törzsfejléc, könyvnév nélküli hely, forráshiba;
  - DT-F102d/g, #185.
- **#104:** a kétrétegű BDB-kártya (olvasói réteg: jelentésfa glosszákkal, „A motívum helyein”, glosszás csukott cím; apparátus: `<details>` + gépi jelölő, „Szótári apparátus”), egyetlen helyen definiált kapcsolóval. A HAMART görög 4.2 mintája még a régi formában van (pl. „2 – 2.a (2 szakasz)”, glossza nélküli „2.b” cím, a fejben görög nyers alakjegyzék).

## Tételek
- **T0:** modell-ellenőrzés; a #104 a main-en.
- **T1 — vak mérés (seed-201):**
  - véletlen 200 Thayer-idézett ÚSZ-vers, rétegezve gyakori és ritka Strongra;
  - két független Opus-kitöltő; aki dönt, nem ellenőriz;
  - az eljárás és a kapu előre rögzítve: nyers szám, Wilson-CI, könyv/vers és jelentéspont külön.
  - **A mérés megelőzi a javítást.**
- **T2 — szabályjavítás hibaosztályonként:** csak a mért hibákra, a BDB-osztályok mintájára; minden osztály tesztje a seed-201 eseteivel. Forráshiba a `thayer_forras_javitas.tsv`-be, tételesen.
- **T3 — kétes esetek:** csak akkor, ha a T2 után a mérés 97% alatt marad.
  - gépi jelölés: `biztos` / `ketes`;
  - a kétes esetekre modelles döntés két kézzel, provenienciával;
  - ellenőrizetlen sor nem renderel;
  - előtte költségbecslés, orkesztrátori jóváhagyással.
- **T4 — új vak mérés (seed-202):** friss minta, kapu ≥ 97%. Ha teljesül, a szó-lapra a mért szám kerül CI-vel.
- **T5 — a kétrétegű kártya Thayer-ága:** a #104 mechanizmusával (ugyanaz a kapcsoló, a jelölő és a HIBA-kapu az olvasói rétegre).
  - olvasói réteg: jelentésfa magyar glosszákkal, „A motívum helyein: vers → jelentés”, glosszás csukott cím;
  - kutatói réteg: a görög alakjegyzék, a klasszikus párhuzamok (Platón, Xenophón …) és a teljes igehely-lista.
  - Glossza nélküli szakasznál a magyar meghatározás áll, vagy ez: „a szótár csak alakot/párhuzamot közöl”.
- **T6:** jelentés, független ellenőr, draft PR.
  - A lapokat nem generálja újra: a HAMART-on a #182 kapcsolja be.
  - Minta a HAMART görög 4.2-éről, ideiglenes könyvtárban.

## Nem része
- a Thayer magyar fordítása (#7 / #142 / #153);
- a BDB-oldal;
- a lapok újragenerálása.

## Előfeltétel-térkép
- A **#104** merge-e kell a T5-höz; a T1–T4 csak a Thayer-fájlokat írja, ezért előbb is indulhat. Ha a befogadó a `fugg`-ot T5-re szűkíteni tudja, a mérés azonnal mehet.
- A **#182 (HAMART)** görög 4.2-je erre épül, ezért ez a #182 előtt fusson le.
