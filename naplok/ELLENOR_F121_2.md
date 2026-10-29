# ELLENOR_F121_2 — F121 UBS-csomag · `8e3d71a3..90f19f0f`

*A `fuggetlen-ellenor` (claude-opus-5-5) jelentése, a végrehajtó rögzítette. Verdikt: **ELTÉRÉS: 3 tétel**.*

**OK:** a modell-mezők; a meglévő sorok bájtazonossága (1 csere: 33.131); kulcslefedettség (H7121 19/19, H8034 5/5 lexid, G1941 56.15); a három jóváhagyott javítás pontosan így áll a táblában, a „(valakire) hozni (eseményt)” kapubukása kézi ítélettel a `bukottak.tsv`-ben; a lap diffje csak a 32 UBS-cella és a lábjegyzet, a `(fordításra vár)` 1 db; a „2. Szótári háttér” érintetlen; a szerverkód (H-Strong, paraméteres SQL, jelleg); az `ir` fedi a fájlokat; a CI-szabályok 0 HIBA. NEM ELLENŐRIZHETŐ az ellenőrnek: a SHA-1 újraszámolás (a végrehajtó `ellenoriz.py` 13. szabálya RENDBEN).

| # | Eltérés | Kezelés |
|---|---|---|
| 1 | (közepes) A 44 egységes adag előtt nincs dokumentálva a szójegyzék-gyűjtő (DT240), a visszamenőleges felmérés (DT242), a Károli-adatblokk (E9) futása vagy elengedése; a DT-F121f elengedése a 6 sorra szólt. | **Nyitott — jelezve a felhasználónak.** Tény: egyik sem futott a 44 sorra; a terminológiát a jóváhagyott v4 sorok és a tervezet kézi átnézése (a felhasználó a tervezetet soronként látta és javította) fedte; a Károli-alakokat a 44 szövegben nem külön adatblokk, hanem a lap Károli-sorai (segítségül hívni, kiáltani, nevezni) adták. |
| 2 | (közepes) A `ubs_glossza_cella` minden lapra hat; a többi lap a következő generáláskor változik, erről nincs döntés. | **Dokumentálva** (napló 9.): ez a #36 (a többi lap újragenerálása) hatóköre; e menet más lapot nem írt, a cella-forma a DT393 szerint a generátoré. A többi lap `(fordításra vár)`-ja a saját UBS-csomagjukig marad. |
| 3 | (alacsony) `q.ubs_dbh_szo`: az „első sor” nem determinisztikus. | **Javítva**: `ORDER BY lexid, rowid` (a fájlsorrend = a `dbh_forras_idx` és a hash forrása); a további domének elvesznek, mint a többi UBS-felületen (lexidenként egy sor). |
