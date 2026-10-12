# ELLENOR_F23_2 — F23_MOTIVUM_FORRAS_BRIEF.md (M0, második kör)

*Ág: claude/f23-motivum-forras, origin/main..HEAD (63cda5e..8b3ef97). A `fuggetlen-ellenor` jelentése; a fájlba az orkesztrátor írta át (az ellenőrnek nincs fájlíró eszköze). Az ellenőr a `MOTIVUM_FORRAS_M0.py`-t nem futtathatta; a számokat a TSV-kből mérte újra.*

**Eredmény: ELTÉRÉS, 3 tétel.** Az első kör 8 eltéréséből 7 megszűnt, 1 részben megmaradt. Tartalmi fájl nem változott; az M1 nem indult; `allapot: megallt`.

## Eltérések

1. **`sablonszabaly` nem következetes** (lekepezes.tsv:24, 46; vö. 48, 52): a 24. sor (Lezárási checklist) saját megjegyzése szerint „eljárás, nem dokumentumszakasz”, a B_helye mégis `adat`; a 46. sor (B) OLVASHATÓ, megszűnt) `generalt`, holott az azonos okafogyott 48. sor (Kimenet: KÉT fájl) `sablonszabaly`. Érinti a DT66 (b) kérdését.
2. **Elavult szám** (lekepezes.tsv:21): „81 blokk”, a javított mérés és a DT66 szerint 87.
3. **`naplok/ELLENOR_F23.md` (és ez a fájl) nincs az `ir` mezőben**, és az `ir` bővítéséről nincs verziónapló-sor (alacsony).

## OK

- Leképezés teljes (6. és 8. sablon minden szakasza, a 7 rés); 77 sor: generalt 28, kezi_forras 21, adat 15, sablonszabaly 13; 33 `javaslat`, 19 `szetvalasztando`.
- „rés: modszertan” `szetvalasztando`; a 21 `kezi_forras` sor rögzíti az „összefüggő érvelés” jelölést vagy indokolja a kivételt (12–15, 17, 18, 40. sorból a „nem önálló mező” szó szerinti fele hiányzik, alacsony).
- NAPLO-blokk, Forrásréteg-fejléc, Mikor használandó, Terminológiai szabályok besorolása védhető, javaslatként.
- Hatókör bővítve a `tematikus_lezart/naplok/`-ra: 25 fájl, 87 NAPLO-blokk, 324 gyanús sor, 176 átfedéspár.
- `lefedettseg_3gram`; DT66: 33 javaslat felsorolva, sor- és találatszám szétválasztva, négy kérdés (a)–(d); az `ir` tartalmazza a M0.py-t és az F23_zaras.md-t.
- Nulla-diff a tartalmi könyvtárakon; E2–E16, E19, E20, E26: 0; HIBA-szintű jelzés nincs. CI-egyezés nem ellenőrizhető (nem volt CI-jelentés).
