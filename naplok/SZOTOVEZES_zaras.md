# SZOTOVEZES (#94) — zárójelentés (újraellenőrzésre kész, a lezárás előtt)

*2026-10-13 · ág: `claude/f94-szotovezes` · modell: claude-opus-5-5 · részletek: `naplok/SZOTOVEZES_meres.md` (1–17. szakasz) · ellenőri jelentés: `naplok/ELLENOR_F94.md` (7 eltérés, javítva: 17. szakasz)*

- **Eredmény:** a Károli minden írásmódjának szótári alakja: `adat/szoto/karoli_szotari_alak.tsv` (66 824 sor, generált, determinisztikus), a **C+K hibriddel, simplemma nélkül** (DT-F94e; a simplemma csak fejlesztési mérce). Hibrid v3 újra befagyasztva az ellenőr után (`hibrid.py` sha256 `7dc76b42…`); a K tábla 400 sora és a 4. minta 113 sora a felhasználó által ellenőrzött.
- **Mérés a 4. mintán, C+K:** a független mérés (15. szakasz) M1 súlyozva 98,5% (a K-alakok nélküli döntő halmazon 94,6%, alakonként 60%), M2 (c) 98,40% (K nélküli lemmákon 98,02%). Az ellenőr utáni v3-mal (**a minta erre nem teljesen független**, 17.5): 98,6% / 95,0% / 63%, M2 (c) 98,40% / 98,03%.
- **Keresési mód (a #76/#92 felé):** a mért pontosság a **(c) módra** (szótári alak VAGY Strong) érvényes; tisztán szótári alakra keresve (a) a K nélküli lemmákon 91,8%, és a ritka alakokon alakonként gyengébb (N-F94g). A tábla `# allapot:` sora is kimondja.
- **K1** teljesül · **K2** teljesül (bitre) · **K3** teljesül a C+K-ra (M2 (c) a küszöb határán) · **K4** teljesül a DT-F94d szerinti számmal (30 + 1 manual, nem 34) · **K5** teljesül, a független újraellenőrzés hátra van · **K6** teljesül a kiadott C+K-n is (előtte 93 / 200 nem ige, utána 0; az ellenőr 26 névszói sora jegy nélküli).
- **Ismert hibák a kiadott C+K-ban** (kézi kivétellel nem javítva): *Melkié → Melkié*, *atyámnak → atyám*, *meggyarapodnak → meggyarapod*; további korlátok: napló 11.6, 16.4, 17.6 (pl. *-ám/-ém* E/1 tárgyas, *leheletének*, *atyafiaival*).
- **Döntések:** DT130, DT-F94a–e 🟢. **Nyitott:** N-F94a (különálló igekötő), N-F94b (külső szótár, licencdöntés), N-F94c (*jó*, 1Móz 1:4, H2895), N-F94d (hátravetett igekötő), N-F94f (különírt vonatkozó névmás), N-F94g (a C+K ritka alakjai). N-F94e lezárva.
- **Következő:** független újraellenőrzés, majd lezárás (PR); a `pardes.db`-oszlop a #95.
