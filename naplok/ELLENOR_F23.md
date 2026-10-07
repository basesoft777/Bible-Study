# ELLENOR_F23 — F23_MOTIVUM_FORRAS_BRIEF.md (M0)

*Ág: claude/f23-motivum-forras, origin/main..HEAD (63cda5e..1d4772b). Az ellenőr (`fuggetlen-ellenor`) jelentése; a fájlba az orkesztrátor írta át, mert az ellenőrnek nincs fájlíró eszköze. Az ellenőr nem futtathatta a `MOTIVUM_FORRAS_M0.py`-t, a számokat Grep-pel mérte újra.*

**Eredmény: ELTÉRÉS, 8 tétel.** Tartalmi fájl nem változott (nulla-diff az adat/, konkordancia/, tematikus_lezart/, motivumok/, lexikon/, genezis/, sablonok/, eszkozok/, motivumlog/ és CLAUDE.md körben). Az M1 nem indult el, a ⛔ megállás megtörtént.

## Eltérések (súlyosság szerint csökkenően)

1. **M0/1 leképezés nem teljes:** 10 sablonszakasznak nincs sora a `MOTIVUM_FORRAS_lekepezes.tsv`-ben. A 6. sablonból 6 (Mikor használandó; Kimenet: KÉT fájl; Közös terminológiai szabályok; Fájlnév-konvenció; Konfliktuskezelés; Minőségi kapu), a 8.-ból 4 (Mikor és hogyan készül; Amit a törzscikk kihagy; Ellenőrzés; Kiejtés). A 4. sablon azonos jellegű szabályblokkjai kaptak sort.
2. **10 `kezi_forras` sor** (lekepezes.tsv:2,4,16,19,21,26,27,56,60,68) megjegyzése nem rögzíti az „összefüggő érvelés része, nem önálló mező” jelölést; köztük nem érvelés-szakaszok is (NAPLO-blokk, Forrásréteg-fejléc, Mikor használandó, Terminológiai szabályok): lehetséges besorolási hiba.
3. **M0/4–5 hatókör:** a mérés csak a `tematikus_lezart/*.md` gyökerét nézi; a `tematikus_lezart/naplok/` 7 kereszthivatkozás-naplója kimaradt, a szűkítést sem a napló, sem a DT nem rögzíti.
4. **„rés: modszertan” sor** (lekepezes.tsv:68): B_helye `kezi_forras`, a megjegyzés szerint adat- és kézi részre válik, de a `szetvalasztando` jelölés hiányzik (DT28).
5. **DT-F23a szám-keverés** (DONTESEK.md:141): „272 gyanús sor (dátum 179, fájlnév 273, …)” — a zárójeles számok találatok, nem sorok.
6. **DT-F23a nem sorolja fel** a `javaslat` besorolásokat, csak a darabszámot és a TSV-re mutat (alacsony).
7. **Oszlopnév:** `lefedettseg_5gram` (M0.py:216), a módszer viszont 3-gram.
8. **`ir`-en kívüli fájl:** `naplok/MOTIVUM_FORRAS_M0.py` és `naplok/F23_zaras.md` (a végrehajtó maga dokumentálta; alacsony).

## OK (saját újramérés)

- Leképezés-számok: kézi 26 / adat 13 / generált 28; olvasói 21 / apparátus 29 / belső 17; `javaslat` 19, `szetvalasztando` 16 — egyezik a DT-F23a-val.
- Törzscikk-egyediség: 363 sor, `nem_besorolt` 0 (heurisztikus regex-besorolás: az „üres eredmény” erre érvényes, nem kézi átnézésre).
- Párosítás 8:1 egyezik az `adat/motivumok.tsv`-vel; NAPLO-blokkok 81 (72 + 9), fájlonként egyezik; átfedés 175 pár (3/6/39/127).
- ⭐-küszöb lelet (D37): KIRALY, MENNY, HODIT = 1; ISTENTISZT = 5 — egyezik a DT-vel.
- ⛔ M0 utáni megállás, DT-F32a: nincs `sablonok/9_*`, SEMA-módosítás; `allapot: megallt`.
- E2–E16, E19, E20, E26: 0; HIBA-szintű jelzés nincs. E25 3 jelzés (diffen kívül), E27 33 jelentés (csonkolt).

## Nem ellenőrizhető

- A „3418 vizsgált egység” csak a szkript stdout-jában van, fájl nincs mögötte.
- A CI-jelentéssel való egyezés (nem volt CI-jelentés).
