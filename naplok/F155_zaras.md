# F155 zárónapló (THAYER_ELAVULT_HIVATKOZAS)

**Mi készült el.** A `eszkozok/thayer_jelolt/forditas.py:219` a régi `teljes` sor megjegyzésébe ezentúl a végleges `DT329`-et írja, nem a `DT-F132c` helyőrzőt. Ezt a `Lanc.test_beir_opus_regi_elavul` teszt ellenőrzi. Az `adat/forditasok.tsv` 7 `elavult` Thayer-sorában (G1311, G2671, G5010, G5356, G0012, G5351, G0086) a megjegyzés-mezőben `DT-F132c` → `DT329`. Mindez a DT-F155a (a) szerint történt; a felhasználó döntése: „(a) Csere DT329-re”, 2026-11-02.

**Mért eredmények.**
- `grep -c "DT-F132c" adat/forditasok.tsv`: 7 → 0. A diff pontosan 7 sort érint, csak a `megjegyzes` mezőt, a táblasor-Δ 0.
- `teszt_lanc.py`: 40 tesztből 39 zöld. Egyetlen bukás az ismert N66, a sigla-teszt.
- `ellenoriz.py`: SÉRTÉS 0. `feladatok.py ellenoriz`: 177 brief, 0 hiba.

**Egyeztetett eltérés.** A felhasználó kérésére („#155 és a teszt”, 2026-11-02) a `teszt_lanc.py` G1941-gerinc állítása 10-ről 6-ra változott. Ok: a DT476 / F152.14 szándékosan vette ki az ISTENTISZT-001-ből a Róm 10:12, 10:14, 2Tim 2:22 és 1Pét 1:17 helyeket.

**Javítókör (/elteres, 2/2).**
- ELLENOR_F155 (3 tétel):
  - 1.: a merge-ből visszajött `DT-F157d` duplikátum törölve (F155.6).
  - 2.: a brief döntésnaplója kitöltve (F155.7).
  - 3.: téves; válasz: `ELLENOR_F155_1_valasz.md`, a `BRIEF_SABLON.md:54` alapján.
- ELLENOR_F155_2 (1 tétel): a válaszfájl neve javítva (F155.11).
- ELLENOR_F155_3: TISZTA.

**Nyitott (hatókörön kívül).**
- A `forditas.py` docstringjében és a 211., 216. sor hibaüzenetében még a `DT-F132c` áll. Az E32 ezt JELENTÉS-ként jelzi; a javítás a 70 literálos javaslathoz tartozik (F141).
- A `szolista.py` és a `teszt_lanc.py` megjegyzéseiben is van még `DT-F132c`.
- Az N66 sigla-teszt továbbra is piros.
