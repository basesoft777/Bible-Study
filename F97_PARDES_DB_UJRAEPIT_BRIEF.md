---
feladat: 97
cim: A pardes.db újraépítése a #91 utáni TSV-kből — frissesség (D5), 3.12-es építő-tesztek, a pardes disztribúció példányának cseréje
kod: PARDES_DB_UJRAEPIT
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: lezarva
pr: https://github.com/basesoft777/Bible-Study/pull/342
lezarva_osszegzes: "Új pardes.db (73 tábla, D5 0 eltérés, sha256 500183a1…708b), új manifest, a disztribúció példánya cserélve (a felhasználó futtatta; .regi megmaradt), 3.12-es tesztek 64 OK; F76 E1 és E3 lezárva; N-F97a nyitott."
ag: claude/f97-pardes-db-ujraepit
ad: friss pardes.db a main TSV-iből (D5 0 eltérés), új manifest a másolat-épséghez, a pardes disztribúció példánya cserélve (sha256 és másolat-épségi teszt), az F79/F92/F95 építő-tesztek Python 3.12-n; az F76 E1 és E3 lezárása
kovetkezo: "Lezárva; merge a felhasználótól. N-F97a nyitott."
olvas: [eszkozok/sqlite_epit.py, eszkozok/teszt_sqlite_epit.py, eszkozok/olvaso_pilot/db_meres.py, eszkozok/olvaso_szerver/frissesseg.py, naplok/OLVASOI_KONKORDANCIA_M0.md, naplok/ELLENOR_F76.md, naplok/SQLITE_EPIT_meres.md, adat/SEMA.md]
ir: [eszkozok/olvaso_szerver/manifest_pardes_db.tsv, naplok/SQLITE_EPIT_meres.md, naplok/SQLITE_EPIT_integritas.md, naplok/SQLITE_EPIT_proba_teljes.md, naplok/PARDES_DB_UJRAEPIT_zaras.md]
fugg: [91, 95]
nem_fugg: [76, 93]
---

# F97_PARDES_DB_UJRAEPIT_BRIEF.md — A pardes.db újraépítése a #91 utáni TSV-kből

*FELADATOK #97 · Modell: sonnet · v1 · 2026.10.14 · forrás: az F76 1. menetének zárása (`naplok/OLVASOI_KONKORDANCIA_M0.md` 4.3, K4-bekezdés; `naplok/ELLENOR_F76.md` E1, E3), a felhasználó döntése a chatben (2026-10-14): az újraépítés külön feladat, az F76 M2 előtt, a main-ről nyitott ágon.*

## 1. Cél

A `pardes.db` (fő munkamásolat, `epites_ts=2026-10-13T18:10:45Z`) a #91 (feliratos zsoltárok számozása) javításai előtti állapotot tükrözi: a D5 frissességi ellenőrzés három táblára eltérést mért (`vers_szamozas`, `lxx_versszam`, `nave_vers`; forrásuk a `konkordancia/Karoli_versmegfeleltetes.tsv` és a `konkordancia/LXX_versificacios_terkep.tsv`, mindkettő az építés után módosult). A feladat az adatbázis újraépítése a main mai TSV-iből, a frissesség igazolása, és a `pardes` WSL-disztribúció példányának cseréje, hogy az F76 M2 (alkalmazás) már az új számozásra épüljön.

## 2. Hatókör

- **Benne:** újraépítés a meglévő építővel (`eszkozok/sqlite_epit.py`), kódváltoztatás nélkül; a D5 (TSV-frissesség) és a másolat-épség külön igazolása; az F79/F92/F95 építő-tesztek futtatása Python 3.12-n; a disztribúció két maradék munkakönyvtárának törlése.
- **Nincs benne:** az építő vagy a séma módosítása (ha az újraépítéshez kódváltoztatás kellene: ⛔ megállás); az olvasói szerver (F76) bármely része; a #93 (TIPNR token-hiány) — ha az később módosítja az építőt, újabb újraépítés kell, ez nem e feladat dolga.
- **Két külön igazolás (F76 M0 3.8, K4):** (1) **TSV-frissesség** az építés gépén: `eszkozok/olvaso_pilot/db_meres.py` D5, hash-újraszámítással; (2) **másolat-épség** a célgépen: `eszkozok/olvaso_szerver/frissesseg.py` a manifesttel. A manifest az új db `meta` sorából készül (`--manifest-keszit`); ez **nem** frissességi bizonyíték, és a napló nem is nevezheti annak.

## 3. Lépések

1. **M0 (rövid terv):** a 3.12-es tesztfuttatás helye. Windowson a Python 3.14 fut, `uv` nincs; a `pardes` disztribúcióban 3.12 van, de a klón ritka (a `konkordancia/` hiányzik). Két út: (a) a disztribúció a repót a `/mnt/c/...` úton csak olvassa; (b) a ritka klón bővítése. A választás és indoklása a zárónaplóba kerül.
2. **Újraépítés:** `python eszkozok/sqlite_epit.py --mod teljes` (a `--naplo` a `naplok/SQLITE_EPIT_*.md` fájlokat frissíti), a main friss állapotán.
3. **D5:** a `db_meres.py` frissességi szakasza hash-újraszámítással; elvárt eredmény: 0 eltérő tábla. Eltérésnél ⛔ megállás.
4. **Manifest:** `frissesseg.py --db pardes.db --manifest-keszit eszkozok/olvaso_szerver/manifest_pardes_db.tsv`.
5. **⛔ Megállás a disztribúcióba másolás előtt** (a felhasználó jóváhagyása).
6. **Csere a disztribúcióban:** a db átmásolása a `~/pardes/pardes.db` helyére, a sha256 egyezése a forrással, a másolat-épségi teszt (`frissesseg.py` teljes módban, a manifesttel) zöld.
7. **Építő-tesztek 3.12-n:** `eszkozok/teszt_sqlite_epit.py` (az F79, F92 és F95 tesztjei) az 1. lépésben választott módon; az eredmény és a Python-verzió a naplóba.
8. **Takarítás:** a disztribúcióban a `~/probe/` és a `~/szoto_arany/` törlése (a felhasználó a chatben jóváhagyta a feladat felvételével; a törlés előtt a tartalom listázása a naplóba).
9. **Zárónapló:** `naplok/PARDES_DB_UJRAEPIT_zaras.md` — mért számok (méret, táblaszám, `epites_ts`, sha256, idők), proveniencia-sorral; az F76 E1 és E3 lezárásának kimondása.

## 4. Elfogadás

- D5: 0 eltérő tábla, a proveniencia-sor (`scope=… | forras=… | ts=…`) a naplóban.
- A disztribúció példányának sha256-ja egyezik az új fő munkamásolatéval; a másolat-épségi teszt zöld.
- `teszt_sqlite_epit.py` Python 3.12-n hiba nélkül; ha valamelyik teszt nem futtatható, az kifejezetten jelölve, nem zöldként.
- A `feladatok.py ellenoriz` 0 hibát ad.

## 5. Kapcsolódás

#76 (OLVASOI_KONKORDANCIA: a fogyasztó; az M2 erre a feladatra vár), #79 (SQLITE_EPIT), #91 (ZSOLT_FELIRAT_SZAMOZAS: a változás forrása), #92 (PARDES_DB_OLVASOI), #95 (SZOTOVEZES_DB), #93 (nem függés: ha módosítja az építőt, újabb újraépítés kell).

## 6. Döntésnapló

*(üres)*
