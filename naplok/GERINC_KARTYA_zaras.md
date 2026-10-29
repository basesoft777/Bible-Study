# GERINC_KARTYA_zaras.md — #124 zárójelentés

*Modell: `claude-sonnet-5-5` (a brief `sonnet`). Ág: `claude/f124-gerinc-kartya-8a0cef`, alap: `origin/main` 0e607b2f. Napló: `naplok/GERINC_KARTYA_naplo.md`.*

## Mi készült

| Tétel | Fájl | Tartalom |
|---|---|---|
| F124.0 | `naplok/GERINC_KARTYA_naplo.md` | 0. mérés: gerinc-elemek, #110 szűrő, fájlnevek, `jelolt.py` alap; DT-F124a helyőrző |
| F124.1 | `eszkozok/gerinc_szuro.py`, `teszt_gerinc_szuro.py` | a DT283 szabály importálható alakban; a valós adaton az `F110_szuro_szimulacio.tsv` mind a 189 sorát reprodukálja |
| F124.2 | `eszkozok/gerinc_kartya.py`, `teszt_gerinc_kartya.py` | kártya (kollokáció, állapot, szűrő, `szuretlen_tag`, melléklet, proveniencia 0 találatnál is), `--osszevet`, `--ir` |
| F124.3 | `eszkozok/gerinc_terkep.py`, `teszt_gerinc_terkep.py` | prioritási térkép, fájlnév-alapú vers-pontos lefedettség, idempotens kimenet |
| F124.4 | `.github/workflows/gerinc_terkep.yml` | commit a `main`-re a `feladatok.yml` mintájára |

Döntés: DT-F124a (✅ alkalmazva; a felhasználó szava: „minden legyen teljes”, az orkesztrátor üzenetében idézve). A DT-F124d nem kellett; a DT-F124b (előminősítés) nyitva, kimarad.

## Az elfogadási feltételek

| Feltétel | Állapot |
|---|---|
| Kártya-sor: id, igehely, Strong, `gerinc_elem`, állapot; proveniencia 0 találatnál is | ✔ (`teszt_gerinc_kartya` `Kartya`, `Egyezes`) |
| A kártya a `jelolt.py` minden sorát tartalmazza | ✔ 5 szakaszon azonos halmaz |
| Összevetés mindkét listája, üresen is explicit | ✔ szintetikus teszt; valós adaton a `kulcsszavak.tsv` üres → „nem végezhető el” |
| Tág Strong szűretlen sora nem a `jeloltek.tsv`-be, nem a sűrűségbe | ✔ (`Ir`, `Szamitas`) |
| Alapfutásban nem ír táblát; `--ir` csak `új`, `nyitva`, sorösszevetéssel | ✔; az `elofordulasok.tsv` hash-e a teszt előtt-után azonos |
| Térkép bajtra azonos, `# GENERÁLT` fejléc | ✔ (`ValosAdat`) |
| MUNKAMENET és 2_ sablon csak jóváhagyott szöveggel | ✔ nem módosult; a szöveg a naplóban, jóváhagyásra |
| `feladatok.py ellenoriz` 0 hiba; tesztek zöldek | lásd lent |

## Tételesen nem teljesített / nyitott (a naplo 8. pontja)

1. A workflow éles próbája (`workflow_dispatch`) a merge után a felhasználó lépése; a `naplok/GERINC_TERKEP.*` az ágon nincs, az Action írja.
2. A tág Strongok szűrője csak az ISTENTISZT-001-re van (a többi motívum 71–100 % `szuretlen_tag`).
3. A `kulcsszavak.tsv` üres, az `--osszevet` valós adaton nem kapott tartalmat.
4. A `melyelemzesek/` többszakaszos fájlneve nem értelmezhető (Zsolt 110:4, Zsid 5–7 feldolgozatlannak számít).
5. N-F124a (kártya-fájl helye), N-F124c (#81-összekötés): nyitva.
6. A `--ir` az `egy_tag` sorokat is írja, ha nem tág az összetett gerinc-elem (a brief szerint).
7. A 2.3 szöveg (MUNKAMENET A3b/A3c, 2_ sablon v22): ⛔ jóváhagyásra vár, az átírás a #125.
8. A brief `paths:` listáját a tanulmánymappákkal bővítettem (a lefedettség bemenete).

## Ellenőrzés

Lásd a PR-t és a `naplok/ELLENOR_F124.md`-t.
