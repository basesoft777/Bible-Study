# OSHL lexikális index — TWOT-szám és BDB-azonosító

## Forrás

- **Repó:** `openscriptures/HebrewLexicon` (https://github.com/openscriptures/HebrewLexicon)
- **Commit:** `21c9add13bc727d3a951361778e97e3ff7afd1ce`
- **Fájl és SHA-256:**

| Fájl | SHA-256 |
|---|---|
| `LexicalIndex.xml` | `8f7a605c58899d2f44430149c143c00903976e1e91232476677972a69e5bc85f` |

**Reprodukáló parancs:**

```bash
python eszkozok/oshl_index_import.py --letolt
```

## Licenc és forrásmegjelölés

**CC BY 4.0.** A `readme.md` (Open Scriptures Hebrew Bible Project) szerinti
forrásmegjelölés: „Open Scriptures Hebrew Bible Project”. **A TWOT-szám
hivatkozási jellegű** — a `<xref twot="…">` attribútum csak a *Theological
Wordbook of the Old Testament* szócikkszámára mutat, a TWOT szövegét nem
tartalmazza és nem írja át. **A TWOT-szöveg nem kerül a repóba** (l.
`F6_BRIEF.md` tervezési napló 14. pontja, D7).

## Fájl és oszlopok

Fejléc: `strong strong_eredeti twot bdb_id nyelv oshl_id lemma atiras szofaj def_en`

**A sor egysége `entry × xref`** — egy `<entry>`-nek elvileg pontosan egy
`<xref>`-je van a forrásban, de a kivonat `<xref>`-enként ír sort, ha ez
mégsem állna.

- `strong` — `H` + a `strong` attribútum 4 jegyre nullával kitöltött alakja,
  ha az attribútum csak számjegyekből áll; egyébként `—` (a forrásban a
  `strong` attribútum néha betűvel kezdődő kód, pl. összetett vagy
  bizonytalan azonosítású szócikkeknél).
- `strong_eredeti` — a `strong` attribútum, ahogy a forrásban áll, `—` ha
  hiányzik.
- `twot`, `bdb_id` — a `twot`, illetve `bdb` attribútum, ahogy áll, `—` ha
  hiányzik.
- `nyelv` — a `<part xml:lang="…">` alapján: `heb` → `heber`, `arc` →
  `arameus`.
- `oshl_id` — az `<entry id>` attribútuma (a forrás belső, BDB-oldalszám
  szerinti rendezési kulcsa).
- `lemma`, `szofaj`, `def_en` — a `<w>`, `<pos>`, `<def>` elem szövege
  (`itertext()`, `\s+` → egy szóköz, `strip()`).
- `atiras` — a `<w xlit>` attribútuma.

Hiányzó vagy üres szöveg minden mezőben `—`. A tábla `sorted()`-tel
rendezett, UTF-8, `\n` sorvég.

## Mért értékek

| Tétel | Érték |
|---|---|
| adatsor (fejléc nélkül) | 10 221 |
| SHA-256 a `#`-sorok nélkül | `f5b9e02fbf8ba707eaaecccccbc5512176cc5c3c9b29c81e22a983b30b4eeef3` |
| `strong = —` | 930 |
| `twot = —` | 2 918 |
| `strong ≠ —` és `twot ≠ —` | 6 640 |
| `nyelv = arameus` | 789 |
| különböző `strong` (`—` nélkül) | 8 673 |

Mintasorok (`strong` → `twot`, `bdb_id`): `H0001` → `4a`, `a.ae.ab`; `H3548`
→ `959a`, `k.as.ab`; `H7121` → `2063`, `s.cy.aa`; `H8034` → `2405`,
`v.dv.ab`.

## Ismert korlátok

- **A `strong` hiánya 930 sorban.** A forrás `strong` attribútuma ezekben a
  sorokban vagy nincs jelen, vagy betűvel kezdődő (nem tisztán numerikus)
  kód — ez utóbbi esetben a `strong_eredeti` megőrzi az eredeti alakot, a
  `strong` oszlop `—`.
- **419 Strong-számhoz több (nem üres) TWOT-szám tartozik**, homográfok miatt (a
  forrás ugyanazt a Strong-kódot több, eltérő eredetű gyökhöz is rendeli).
  A kivonat ilyenkor a Strong-számhoz tartozó összes `(twot, bdb_id)` párt
  külön sorban tartja.
- **A TWOT-szöveg nem része a kivonatnak** — csak a hivatkozási szám. A
  TWOT tartalmi felhasználásához külön, jogtiszta forrás szükséges (l.
  `Rendszerfejlesztesi_playbook.md` 2. pont).
