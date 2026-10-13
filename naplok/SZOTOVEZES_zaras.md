# SZOTOVEZES (#94) — zárójelentés (ellenőrzésre kész, a lezárás előtt)

*2026-10-13 · ág: `claude/f94-szotovezes` · modell: claude-opus-5-5 · részletek: `naplok/SZOTOVEZES_meres.md` (1–16. szakasz)*

- **Eredmény:** a Károli minden írásmódjának szótári alakja: `adat/szoto/karoli_szotari_alak.tsv` (66 824 sor, generált), a **C+K hibriddel, simplemma nélkül** (DT-F94e; a simplemma csak fejlesztési mérce, ODbL-összetevő a kiadott táblában nincs). Hibrid v3 befagyasztva (`hibrid.py` sha256 `74d0ebe5…`), K tábla 400 sor és a 4. minta 113 sora a felhasználó által ellenőrzött.
- **Mérés (4. független minta, utána fejlesztési):** C+K M1 súlyozva 98,5% (a K-alakok nélküli döntő halmazon 94,6%, alakonként 60%); M2 (c) 98,4% (K nélküli lemmákon 98,02%).
- **Keresési mód (fontos a #76/#92 felé):** a mért pontosság a **(c) módra** (szótári alak VAGY Strong) érvényes; tisztán szótári alakra keresve (a) a K nélküli lemmákon 91,8%, a ritka alakokon alakonként gyengébb. A tábla `# allapot:` sora is kimondja.
- **K1** teljesül · **K2** teljesül (bitre) · **K3** teljesül a C+K-ra (M2 (c) a határon) · **K4** teljesül a DT-F94d szerinti számmal (30 + 1 manual, nem 34) · **K5** teljesül, a független ellenőrzés hátra van · **K6** teljesül (74 → 0 nem ige).
- **Döntések:** DT130, DT-F94a–e 🟢. **Nyitott:** N-F94a (különálló igekötő), N-F94b (külső szótár, licencdöntés), N-F94c (*jó* Strongja, 1Móz 1:4), N-F94d (hátravetett igekötő), N-F94e (javítva; a magas hangrendű -ék E/1–T/3 kétértelműsége marad), N-F94f (különírt vonatkozó névmás), N-F94g (a C+K ritka alakjai).
- **Ismert korlátok:** napló 11.6 és 16.4 (pl. *-ám/-ém* E/1 tárgyas, *leheletének*, *atyafiaival*); a `hibrid_v2.py` hash-függő bejárása (nem kiadott).
- **Következő:** független ellenőrzés, majd lezárás (PR); a `pardes.db`-oszlop a #95.
