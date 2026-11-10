---
feladat: 187
cim: A Thayer-blokk kétrétegű olvasói kártyája a #104 mechanizmusával, a mért pontossággal a szó-lapon
kod: THAYER_KARTYA
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: fut
ag: claude/f187-thayer-kartya
ad: a lexikonlap görög 4.2-je és a szó-lap Thayer-blokkja kétrétegű (olvasói réteg glosszás jelentésfával és „A motívum helyein” listával; kutatói apparátus <details>-ben), a #104 kapcsolójával, jelölőjével és HIBA-kapujával; a #186 mért pontossága a szó-lapon CI-vel; a lapok nem generálódnak újra
kovetkezo: "A #104 és a #186 merge-e után. KIZAR a lexikon_general.py-n a #182-vel (és a #123/#178/#183-mal), a számsorrend a #182-t tenné előre; a #187 → #182 sorrendet az orkesztrátor vezeti: a #182 2. fázisa a #187 után indul (2026-11-10)"
olvas: [adat/thayer_vers_jelentes.tsv, adat/thayer_szakaszok.tsv, F104_BDB_MEGJELENITES_BRIEF.md, F186_THAYER_JELENTESPONT_97_BRIEF.md]
ir: [eszkozok/lexikon_general.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/konfig/thayer_pontossag.toml, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_pilot/adat.py, eszkozok/teszt_thayer_api_koteg.py, eszkozok/olvasoi_kapu.py, eszkozok/teszt_olvasoi_kapu.py, eszkozok/teszt_szotari_gerinc.py, adat/SEMA.md, nyitott/uj/f187-thayer-kartya.md, naplok/F187_jelentes.md, naplok/ELLENOR_F187.md]
fugg: [104, 186]
---

> **Felosztás (befogadás, 2026-11-10, orkesztrátori jóváhagyással).** Ez a brief a THAYER_SZELETELO-tervezet (2026-11-10) **T5** tétele, a T4-ből a „szó-lapra a mért szám” rész és a T6 zárása. A T0–T4 a **#186** (`F186_THAYER_JELENTESPONT_97_BRIEF.md`); a teljes tervezet ott olvasható. Az alábbi szöveg a tervezetből szó szerint átvett rész.

# Brief-tervezet — A Thayer jelentéspont-hozzárendelés a BDB szintjére: mérés, javítás ≥ 97%, kétrétegű olvasói kártya (THAYER_JELENTESPONT)

*Orkesztrátori tervezet, 2026-11-10. A felhasználó kérése: „csináljuk meg a thayer szeletelőjét is”. Befogadásra (`/befogad`, külön sessionben). A cél, hogy a görög oldal (Thayer) ugyanazt a szintet érje el, amit a héber (BDB) a #102–#105, #185 láncban: mért, ≥ 97%-os vers → jelentéspont hozzárendelés, és olvasóbarát kétrétegű megjelenítés a lexikonlap 4.2-es szakaszában.*

## Kiindulás
- **#132 (lezárva):** `adat/thayer_szakaszok.tsv` (17 093 szakasz, 5 426 Strong), `adat/thayer_vers_jelentes.tsv` (63 953 sor), javítótábla 15 Strongra. **Pontosságmérés nincs**, a zárójelentés csak teszteket és kapukat említ.
- **BDB-minta, ehhez kell igazodni:**
  - seed-101/102 vak mérés, véletlen 200 vers, két független Opus-kitöltő, kapu ≥ 97%;
  - hibaosztályok: fejfelismerés, törzsfejléc, könyvnév nélküli hely, forráshiba;
  - DT-F102d/g, #185.
- **#104:** a kétrétegű BDB-kártya (olvasói réteg: jelentésfa glosszákkal, „A motívum helyein”, glosszás csukott cím; apparátus: `<details>` + gépi jelölő, „Szótári apparátus”), egyetlen helyen definiált kapcsolóval. A HAMART görög 4.2 mintája még a régi formában van (pl. „2 – 2.a (2 szakasz)”, glossza nélküli „2.b” cím, a fejben görög nyers alakjegyzék).


## Tételek
- **T0:** modell-ellenőrzés; a #104 és a #186 a main-en. *(befogadói kiegészítés)*
- **T4 — új vak mérés (seed-202):** friss minta, kapu ≥ 97%. Ha teljesül, a szó-lapra a mért szám kerül CI-vel.  *(itt: csak a szó-lapra kerülő mért szám, CI-vel; a mérés a #186-é)*
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
