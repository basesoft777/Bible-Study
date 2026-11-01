ELTÉRÉS: 8 tétel

# ELLENOR_F38_adag13 — F38_BDB_FORDITAS_BRIEF.md, 13–14. adag (sorrend 5671–8073), PR 556

*A `fuggetlen-ellenor` subagent jelentése, az orkesztrátori menet által mentve (az ellenőrnek nem volt fájlíró eszköze). Itt a jelentés összefoglaló része áll (a verdikt-sor, a kulcs-eredmények, az ELTÉRÉS-ek); a soronkénti táblázat részletei a javítókör bontási-napló szakaszában (6.) és a commitokban követhetők. Merge-ítéletet a jelentés szándékosan nem tartalmaz.*

- **Tartomány:** `18d0dcb9..7a072233` (F38.454–F38.466), ág: `claude/f38-adag13-api-bc60bb`. Az ellenőr modellje `claude-opus-5-5` (kért: `opus`).
- **OK:** modell-mezők (6400 új sor: `sonnet` / `claude-sonnet-5-5`, futásnapló 567/567), tábla-Δ (csak `adat/forditasok.tsv` +6400 / 0 törlés; `kezi` sor érintetlen), Strong-határ a B-úton (75 + 1878 + 450 = 2403; szakaszszám-próbák egyeznek; kimaradt `⟦n⟧` 0; üres `forditas_hu` 0), kapu-felülbírálás H2202, H2954, H1306 (hamis pozitív, hű), hűség/terminológia minták (H0019, H6008, H5951, H8640, H4984 48 szakasz), Szent Szellem-szabály, költségszámok (23,220054 USD, 567 kérés), kulcs-grep (üres), DT-F38y/DT-F38u forma, brief-fejléc, ⛔ M1/Mz/Mj nem érintett.
- **NEM ELLENŐRIZHETŐ az ellenőr számára:** a teljes halmazkülönbség, a `teszt_bdb_api_koteg.py` és az `ellenoriz.py` futtatása, a 65/65 Károli-pár, a 571 310 karakteres nevező.

## Az ELTÉRÉS-ek súlyossági sorrendben

1. **Plafon:** a DT-F38y és a brief szerint 15 USD a kemény plafon; a kód 31,67 USD-vel futott (mért költség 23,22 USD). A +20 USD-s emelésről nincs DONTESEK-sor, és a DT-F38y szövege sem módosult.
2. **AV/RV-glossza:** H1761 sz2 „AV RV instrument of music” → „AV RV hangszer” lefordult (D10 (5)); a H2082 határeset. A visszaállító heurisztika ismert korlátja.
3. **Hamis `megjegyzes` a kanonikus táblában:** a H0435 sora azt állítja, hogy a forrásban nincs „Sept.”, pedig van („Aug.—Sept. Neh 6:15”).
4. **Kapuhiba-számok a bontási naplóban:** 54 és 49/54 helyett 51 és 46/51 (a B-próba bukottjai kétszer számolva).
5. **H3901:** a felülbírált fordításból kimaradt egy „de” (but).
6. **Bontási napló, 28. sor:** 6396 helyett 6398 szakaszsor.
7. **Commitüzenetek:** F38.457 „+929” (valójában 931), F38.463 „1941 Strong” (valójában 1878).
8. **F136-fejléc:** egy másik brief fejlécét ez a menet írta át; `lezarva_osszegzes` nincs.

*(A 8. tétel az indító session megbízásából történt; a bontási napló 6. szakasza egyeztetett eltérésként rögzíti.)*
