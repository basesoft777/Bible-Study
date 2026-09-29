# FP2 minta — 30 szócikk

*FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 1. lépés · kiválasztó szkript: `fp2/mintavalaszto.py`
(rögzített seed: 20260926) · kimenet: `fp2/minta.tsv`*

## Összetétel

- **20 szócikk a kor2-ből** (`naplok/FORDITAS_P1_minta.tsv`), változatlanul: E (13) + A (1,
  G1941 arany) + N (3) + V (3). Ezen a Gemini 3.1 Flash Lite és a DeepSeek V4 Flash
  v1→v3 kimenete közvetlenül összevethető.
- **10 új szócikk**, a kor2 20 szócikkének kizárásával, rétegzett minta:
  - **hosszkategóriák** (a `FORDITAS_ELES_THAYER_BRIEF.md` E6 mintájával egyező határok):
    rövid ≤ 300 kar., közepes 300–2000 kar., hosszú > 2000 kar. → 3 rövid, 4 közepes,
    3 hosszú.
  - **teológiailag súlyos szavak** (szerkesztői jelölt-halmaz, *nem* lekérdezés
    eredménye — CLAUDE.md 3. szabálya szerint jelölve): `G0026` (ἀγάπη, szeretet),
    `G2316` (θεός, Isten), `G4102` (πίστις, hit), `G1343` (δικαιοσύνη,
    igazság/megigazulás), `G5485` (χάρις, kegyelem), `G0266` (ἁμαρτία, bűn), `G3341`
    (μετάνοια, megtérés), `G4991` (σωτηρία, üdvösség), `G2222` (ζωή, élet), `G1391`
    (δόξα, dicsőség) — mind a 10 megvan a `Thayer_teljes.tsv`-ben, egyik sincs a kor2
    20 szócikke között. A determinisztikus kiválasztás ezek közül hármat vett fel
    (`G0026`, `G0266`, `G1343` — mindhárom a „hosszú” kategóriába esik, mert ezek a
    Thayer-ben terjedelmes szócikkek), a fennmaradó 7 helyet a hosszkategóriák szerint
    rétegzett, rögzített seed-del kevert listákból töltötte fel.

## A 10 új szócikk

| Strong | Kategória | Hossz (kar.) | Súlyos |
|---|---|---:|---|
| G0026 | hosszú | 4 688 | igen (ἀγάπη) |
| G0266 | hosszú | 5 003 | igen (ἁμαρτία) |
| G1343 | hosszú | 6 741 | igen (δικαιοσύνη) |
| G0993 | közepes | 691 | nem |
| G1106 | közepes | 603 | nem |
| G3687 | közepes | 1 148 | nem |
| G5013 | közepes | 1 835 | nem |
| G2105 | rövid | 267 | nem |
| G3782 | rövid | 274 | nem |
| G5298 | rövid | 258 | nem |

## Ellenőrzés (a szkriptben `assert`-ekkel)

- 30 sor, 30 egyedi Strong.
- Az új 10 egyike sem esik egybe a kor2 20 szócikkével.
- Pontosan 3 rövid + 4 közepes + 3 hosszú az új szócikkek között.
- Legalább 3 teológiailag súlyos szó az új szócikkek között (ténylegesen 3).
