---
feladat: 203
cim: A Thayer-lánc, a fordítási lista és a Feed 9. kapujának hibajavítása (generátor-hibaleltár C7, C8, B6, B4)
kod: THAYER_FORDITAS
tipus: feladat
fazis: folyamat
modell: opus
munka: folyamat
allapot: megallt
ag: claude/f203-thayer-forditas
pr: 704
ad: a Thayer-bontó mért, nem javított fej-alesetei (K1d, K2c, K2d) és a G0027 nem bibliai hivatkozása javítva, az átkulcsolás általános móddal; a fordítási lista csak a lapon ténylegesen fordítatlan egységet listázza, és nem ír a repóba; a Feed 9. kapuja a DT665 kivételét blokkszintű lapdiffel ismeri; a C8 fordítási része becsléssel, döntésre
kovetkezo: "Folytatás (orkesztrátori ütemezés, 2026-11-11, (c) út): a #704 áll, amíg a HAMART-001 1. kiadása (#699, #696) a main-re nem kerül; akkor az orkesztrátor szól, és ez a session behozza a main-t, mind az 5 migrált lapot újragenerálja (general.py --cel lexikon --id … --ir), és ellenőrzi az E28 zöldjét (a HAMART változása generált blokk-változás, a következő kiadás változásjegyzékébe, F168). Addig: független ellenőrzés és javítókör. Döntésre vár: DT-F203a, N-F203a; N-F203c az olvasó-fázisé"
olvas: [CLAUDE.md, NYITOTT_FELADATOK.md, adat/SEMA.md, naplok/F186_jelentes.md, eszkozok/thayer_jelolt/, eszkozok/glossza_lexikon_forditas.py, eszkozok/szakasz_cimke_levezet.py, eszkozok/muhely_allapot.py, adat/lap_atnezesek.tsv]
ir: [eszkozok/thayer_jelolt/bont.py, eszkozok/thayer_jelolt/vers_jelentes.py, eszkozok/thayer_jelolt/forditas_atkulcsol.py, eszkozok/thayer_jelolt/teszt_bont.py, eszkozok/thayer_jelolt/teszt_vers_jelentes.py, eszkozok/thayer_jelolt/teszt_forditas_atkulcsol.py, eszkozok/thayer_jelolt/teszt_lanc.py, adat/thayer_szakaszok.tsv, adat/thayer_vers_jelentes.tsv, adat/thayer_forras_javitas.tsv, adat/forditasok.tsv, adat/SEMA.md, eszkozok/glossza_lexikon_forditas.py, eszkozok/teszt_glossza_lexikon_forditas.py, eszkozok/glossza_api_koteg.py, eszkozok/teszt_glossza_api_koteg.py, eszkozok/szakasz_cimke_levezet.py, eszkozok/muhely_allapot.py, eszkozok/lapdiff_blokk.py, eszkozok/teszt_lapdiff_blokk.py, NYITOTT_FELADATOK.md, naplok/F203_jelentes.md, dontesek/uj/f203-thayer-forditas.md, nyitott/uj/f203-thayer-forditas.md]
fugg: []
nem_fugg: [121, 123, 156, 161, 178]
---

# F203 — A Thayer-lánc, a fordítási lista és a Feed 9. kapujának hibajavítása

*Orkesztrátori feladat (2026-11-11), a generátor-hibaleltár (`GENERATOR_HIBALELTAR_2026-11-11.md`) C7, C8, B6, B4 tétele. A
HAMART-001 lezárása után új lap nem készül: a generátor és a folyamat hibái javulnak, hogy a lapkészítés bármikor folytatható
legyen. Gyökérok-szabály: második előfordulásnál gépi védelem.*

## Határok

- Nem írja: `eszkozok/lexikon_general.py`, `olvasoi_kapu.py`, `olvasoi_kovetkeztetes.py`, `allitas_adat.py`, `ellenoriz.py`,
  `karoli_kh_epseg.py`, `visszhang/*`, a motívum-adattáblák, `lexikon/*` (a #182 és a későbbi generátor-kör); `bdb_jelolt/*` és a
  BDB-adat (F202); `szamkiosztas` (F201).
- A lexikonlapok nem generálódnak újra (a HAMART-001 kiadás alatt áll): a várható lapváltozás repón kívüli próbával mérve.
- Új döntés és nyitott tétel csak helyőrzővel: `dontesek/uj/f203-thayer-forditas.md`, `nyitott/uj/f203-thayer-forditas.md`.

## Tételek

| Tétel | Forrás | Mit | Kész, ha |
|---|---|---|---|
| F203.1 | C7: N124, N125, N126 | a Thayer-bontó K1d, K2c, K2d alesete; a G0027 nem bibliai hivatkozása; az átkulcsolás általános módja (a harmadik egyedi átkulcsolás helyett) | az aranymintán nincs visszaesés, a javított osztályok az arany értéken; a korpusz változása átnézve; a táblák `--ellenoriz` azonos; a fordítássorok átkulcsolva |
| F203.2 | B6: N-F12e | a fordítási lista csak a lapon ténylegesen fordítatlan egységet listázza; `--kimenet` mellett nem ír a repóba; a render kihagyásánál megáll; a `szakasz_cimke_levezet.py ellenoriz` sem ír a repóba `--ki` nélkül | előtte–utána szám a HAMART-001-en; teszt |
| F203.3 | B4: N-F184a | a Feed 9. kapuja a DT665 (b) feltételét blokkszintű lapdiffel ellenőrzi | teszt; a mai lapokon mérve |
| F203.4 | C8: N87, N-F131v, N88 | a fordítási hiányok becslése; a `{L:…}` jelölés | becslés és kérdés a fordítási költségről (⛔), a nem költséges rész javítva vagy indoklással nyitva |
| F203.5 | — | jelentés, tesztek, draft PR | `python eszkozok/teszt_futtat.py --gyors` és a saját tesztek zöldek; előtte–utána számok a jelentésben |

A N123 (K3, záró szinonima-jegyzet) a lapgenerátort (`lexikon_general.py`) és a #187 kártyáját érinti (új `utvonal`-érték): ebben a
csomagban nem írható, indoklással nyitva marad. A K1e és a K5 (a „visszaugró betű” mechanizmusa) az F186-ban mérten valódi fejeket
nyelt el; mérve, indoklással nyitva.

⛔ A C8 fordítási munkája költséget jelent: előbb becslés, és a felhasználó (az orkesztrátoron át) dönt (memória: „Fordítás: keret
és menet”).
