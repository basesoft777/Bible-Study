# Független ellenőrzés: F30 (SZAMOZAS)

*A jelentést a `fuggetlen-ellenor` ügynök állította össze (tartomány `bd39b91..9309b72`, ág `claude/szamozas`); a fájlba az orkesztrátor írta át, mert az ügynöknek nem volt Write eszköze, és nem commitolhat. Verdikt: **ELTÉRÉS, 6 tétel.** Az ügynök teljes táblája (parancsokkal) a session transcriptjében van; itt az eredmények összefoglalva.*

## Eredmény
- **Különfeltétel (a felhasználó döntése): az `ir` listán kívüli diff kizárólag DT18→DT29 csere** — OK. Az 5 fájl (F18 brief, `adat/SEMA.md`, `adat/datasetek.tsv`, `naplok/F18_import_naplo.md`, `naplok/F18_zaras.md`) tokenszinten, szóközt is számolva pontosan 2+2+4+3+3 `DT18→DT29` cserét tartalmaz. Formális kivétel: az F30 brief saját fejléce.
- **Örökölt helyőrzők kimaradnak:** OK (99/99: 70 DT + 29 N; a DT-F30a és N-F30a nincs a listában). Következő szám DT30 / N47: OK.
- **E26:** piros végleges számra (7 HIBA jelölés nélkül, kilépés 1), zöld helyőrzőre, és `SZÁMKIOSZTÁS-SZÁNDÉKOS` jelöléssel (0 HIBA) — OK.
- **DT-F30a 🟢 (1. opció), ⛔ megállás megtörtént, `commit_uzenet.txt` nincs a végső fán, az `ir` bővítés rögzítve (N-F30a 5., zárás a)**: OK.
- **D1–D5, SZ.0, SZ.5, A3–A6, 1–5. lista:** OK (E12–E15: 0 találat; táblasor-Δ 0; tartalomvesztés nincs).
- **NEM ELLENŐRIZHETŐ** az ügynök eszközeivel: a tesztek futtatása (a CI csak a `teszt_feladatok.py`-t futtatja, a 10 új teszt nincs a CI-ben), a `--proba` 138 fájl / 2237 csere száma, a GitHub-oldali Action-futás, a SZ.6 próba tiltásának ténye, a 200+ távoli ág átnézése, a közös `concurrency`-csoport (`feladatok-frissites`) hatása gyors egymásutáni merge-eknél.

## Eltérések súlyossági sorrendben és állapotuk
1. **(közepes)** Az F30 brief a `KIZART` halmazban van, a `lezarva_osszegzes`-ben álló DT-F30a/N-F30a ezért nem kapna számot, és az újragenerált FELADATOK.md-ben lógó helyőrző maradna. — **Javítva:** a `lezarva_osszegzes` helyőrző-tokenek nélkül, szövegesen hivatkozik a döntésre.
2. **(alacsony–közepes)** A `SZÁMKIOSZTÁS-SZÁNDÉKOS` jelölés a teljes PR-re kikapcsolja az E26-ot (a később rákerülő commitokra is), tágabban a brief SZ.3-nál. — **Nyitott, tervezési döntés a felhasználóé.**
3. **(alacsony)** A DT29 sorban a mechanikus csere a korábbi DT18-döntés szövegét is átírta („az azonosító DT29 marad”), ami már nem igaz. — **Javítva (a felhasználó kérésére):** a két történeti állítás („az új DT-szám DT18”, „az azonosító DT18 marad”) visszaállt DT18-ra; az új azonosítót a sor elején álló megjegyzés adja.
4. **(alacsony)** A napló „jelölés nélkül 3 HIBA” állítása elavult (7 a végső fejen). — **Javítva.**
5. **(alacsony)** Az N-F30a (4) és (5) pontja nem nyitott feladat, és a pontok sorrendje hibás. — **Nyitott, kis javítás.**
6. **(formális)** Az F30 brieffejléc az `ir`-en kívül esik, de a diffje nem DT18→DT29 csere (a CLAUDE.md konvenciója szerint minden menet a saját brieffejlécét frissíti). — **Elfogadott.**

A PR címének ékezetes `[ELLENŐRZŐ]` előtagúnak kell lennie (E16): az ASCII `[ELLENORZO]` E16 HIBÁT ad.
