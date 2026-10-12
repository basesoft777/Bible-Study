# ELLENOR_BDB_KAROLI_POTLAS_2 — brief: F80_BDB_KAROLI_POTLAS_BRIEF.md (v2)

*Második ellenőrzés, tartomány: origin/main...7acb696c (10 commit); az első: `naplok/ELLENOR_BDB_KAROLI_POTLAS.md`. A `fuggetlen-ellenor` jelentésének tömörített mentése (a szerepköre fájlba írást nem enged). A teszteket és a CI-t az ellenőr nem futtathatta.*

**Eredmény: 5 eltérés; az első jelentés 6 eltéréséből az 1–5. megszűnt, a 6. részben.**

## Rendben (saját lekérdezéssel)
- Példasorrend kanonikus: H2617 `irgalmassága` = „1Sám 20:14;1Krón 16:34;1Krón 16:41”, H0426 `istenek` = „Jer 10:11;Dán 2:11;Dán 3:25”, H3782 `el` = „Jer 31:9;Ez 33:12;Hós 5:5”.
- Proveniencia: 62 526 sor mind nem üres (674 `szocikk` + 61 852 `alak`); az `alak` soré = a szócikk soráé.
- `par_db` = link-darab (H3722: 178 / 102 előfordulás; H4191: 1087 / 840); a `tahot_elofordulas` egyezik a `lekerdez.py scan` eredményével (H1285 284, H5315 754, H1004 2049, H8064 421, H2617 247, H0426 95, H3782 62).
- Visszakeresés új Strongokon (H1285, H5315, H1004): a példák a `parok_*.tsv`-ből előállnak.
- `adat/forditasok.tsv` blob `1060f59d` az `origin/main`-nel azonos (K3).
- `parok_konyvek()`: tábla szerinti sorrend, `ValueError` ismeretlen könyvre; a `PAROK_KONYV_ALIAS` (Sir→JSir) indokolt (a tábla `JSir`-t, az adat `Sir`-t ír).
- Bontási napló, N-F80a helyőrző, ⛔ sorrend: rendben; nincs törölt adatsor.

## Eltérések és kezelésük
1. **Magas: a `teszt_bdb_adatblokk.py` beégetett `43`-at vár a `parok_*.tsv` fájlokra**, a main-en már 54 van (+11 ÚSZ). *Javítva (F80.10): a teszt a könyvtár tényleges fájlszámát veti össze; az ág a main-re rebase-elve.*
2. **Közepes: a jóváhagyott változások nem voltak rögzítve.** *Javítva: DT-F80b (🟢) a `DONTESEK.md`-ben, v3 sor a brief döntésnaplójában.*
3. **Alacsony: a bontási napló számai proveniencia-sor nélkül álltak, a `modell`/`allapot` kategóriák keveredtek.** *Javítva: „opus 26; ebből `allapot=kezi` 6”, proveniencia-sor hozzáadva.*
4. **Alacsony: hivatkozás nem létező F80.10–F80.12 commitokra.** *Javítva: F80.7–F80.9.*
5. **Alacsony: a brief törzsében „v1” állt.** *Javítva: v3.*

## Nem ellenőrizhető az ellenőr szerepköréből
Tesztek és `ellenoriz.py` futtatása (a hívó futtatta: 45 teszt zöld, SÉRTÉS 0, `feladatok.py ellenoriz` 0 hiba); a 12,3 MB és az 5 550 módosult `pelda_versek` sor; CI-jelentés.
