# F240 (LXXBDB) — jelentés

*proveniencia: scope=F240 L1–L6 | forras=a független ellenőr (fuggetlen-ellenor) jelentése a 424f077b..cc05bc0e diffen + a javítókör (0e822ba8, af6efead) | ts=2026-11-24*

**Brief:** `F240_LXX_BDB_ADATJAVITAS_BRIEF.md` · **döntések:** `naplok/F240_dontesek.md` (D1–D15) · **mérés:** `naplok/LXXBDB_meres.md` ·
**PR:** #821 · **modell:** claude-opus-5-5 (a brief `opus`) · **ellenőrzési szint:** teljes, egy javítókör.

## A független ellenőr eltérései és a javítókör

| # | Súly | Eltérés (röviden) | Kimenet |
|---|---|---|---|
| 1 | BLOKKOLÓ | CI piros: a PR címe nem `[ELLENŐRZŐ]`; `N249` helyőrző string-literálban; HAMART-001; egy szabály-teszt | **javítva:** a cím `[ELLENŐRZŐ] …`; a literálok számfüggetlenek; a HAMART-001 a 2. sor szerint; a szabály-teszt (`test_push_ures_cimmel_nem_piros`) a PR-cím miatt bukott |
| 2 | BLOKKOLÓ | a kiadott HAMART-001 egy száma változna (H7843 „13 hely”) | **javítva:** lapjavító sor (`adat/lap_javitasok.tsv`, D15, a szerkesztő: „mehet”); „13 → 14 hely” és „Hiph'il 1 (54 → 53 hivatkozás)” — ugyanannak az áthelyezésnek (Ézs 36:10) a két oldala; a lapot a main-en az Action generálja újra |
| 3 | KÖZEPES | a `bridge_sorok` 1–2 darabos, hamis új párt hoz (H1241 „marha” → πρωΐ) | **javítva:** új pár csak a forrás küszöbével (a teljes javított darabszám ≥ 3); a legkisebb darabszám 3 |
| 4 | KÖZEPES | a `Sir 1:5` ἀγόμεναι (G0033) javítatlan | **javítva** (javítósor), és teljességi próba a versillesztéstől függetlenül (`marado_hibas`; a 44. kapu része) |
| 5 | KÖZEPES | 14 hamis fejléc (rossz könyvfeloldás) tétel nélkül | **gazdája van:** D11–D13 — F240.L7, saját PR a #821 merge-e után, OpenScriptures BDB-XML elsődleges tanúval |
| 6 | KÖZEPES | a 44(b) kapu nem fogta volna meg a ténylegesen előfordult nyers olvasást | **javítva:** útvonal-literál és oszlopindex (`r[14]`) is; a segéd importja csak hívással ment fel; teszt: a régi `olvaso_pilot/adat.py` bukik |
| 7 | KÖZEPES | a 48. kapu nem a brief L5.3(b)-je; a 44–48-ra nincs teszt | **javítva:** a generátor a várttól > 600 karakterre választott helyet `ketes:jp_tavol`-ként jelöli (ez a L5.3(b) mérése a generátoron belül: a táblapozíció és az angol pozíció eltérése), 19 sor, plafon 19; tesztek: `eszkozok/teszt_gyokerok_kapuk.py` (`LxxStrongKapuk`, `BdbKonyvkettoKapu`, `VersJelentesKapu`; áladattal: a javítás előtt bukik, utána átmegy), a CI futtatja |
| 8 | APRÓ/KÖZEPES | `bdb_forras_javitas.tsv`: 15 „nem azonosított” sor, elveszett F46-attribúció | **javítva:** a tiszta törlés hivatkozás-kulcsa; az F240 L3 forrásként (`forras_javit.f240_index`); „nem azonosított” sor 0; a H2742 és a H3856 az F46-ot is megtartja |
| 9 | APRÓ | az N-F240a-ban nincs átvezetve a mért 3 370 / 35 | **javítva** |
| 10 | APRÓ | rokon lemmák `konvencio` ítélettel (δῆλος/δήλωσις, ἁρπαγμός/ἅρπαγμα, κόσμιος/κόσμιον) | **javítva** a meglévő DT957 szerint: „megfelelő nélkül”, jelölve (6 javítósor, 16 token) |
| 11 | APRÓ | naplószámok (89/87; 141 vs. 130), `--naplo` a docstringben | **javítva:** 90/88; „141 a javítás előtt, 126 utána”; `--ir` |
| 12 | APRÓ | a `grammatikai_strongok.tsv` fejléce `n=31`; két régi indok ellentmond | **javítva:** `alakszam=34`; a G3165 és a G4771 indoka |

A „NEM ELLENŐRIZHETŐ” pontok (a kapuk futtatása, a tesztsor a saját adatbázison) a javítókörben: a 44–48. kapu
áladatos tesztje zöld (35/35 a `teszt_gyokerok_kapuk.py`-ban); az olvasó gyors tesztsora a saját, az ágból épített
adatbázison zöld (a `teszt_blokkfej` a három szándékos változás kivételsorával, `merce/blokkfej_kivetel.tsv`).

## Saját próba

- Próba-adatbázis a repón kívül (`sqlite_epit.py --mod teljes`), előnézet a 8776-os porton: H0430 „c.” fejléce
  „angyalok”, a szöveg „angyalok Zsolt 97:7”, az LXX-sor „θεός 4 · 1 megfelelő nélkül” (μου nélkül, 8 hivatkozás); H1242
  „πρωΐ 14 · 5 megfelelő nélkül” (φωσφόρος nélkül); H8415 1. jelentése 14 hely (ἄβυσσος).

## A brief határán túl talált, nem javított hiba

- `eszkozok/olvaso_szerver/bdb_vers_jelentes.py` 214. sor: a `_HIVATKOZAS` mintában `\b` helyett nyers visszatörlés-karakter
  (U+0008) áll (a main-en is), ezért a könyvneves ág soha nem illeszkedik. A javítás a vers → jelentés tábla újragenerálását
  vonja maga után, ezért nem gépies apró javítás; az integrátornak jelezve, gazdát kér.

## Technikai döntések (DT920)

- A `bdb_vers_jelentes.tsv` a régi `--ts 2026-11-10`-zel generálva (a 162 ezer soros proveniencia-diff elkerülésére); a
  változást a fejléc kód-hash-e és a commit rögzíti.
- A `bdb_forras_javitas.tsv` az eredeti `--ts` kapcsolókkal generálva (a fejlécben rögzített futás szerint).
- Az L5.3(b) mérése a generátoron belül (`jp_tavol`), nem a kész táblából (a tábla nem hordozza a táblapozíciót).
