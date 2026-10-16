---
feladat: 103
cim: BDB jelentésen belüli tagolás (használati csoportok) és a csoport-bevezetők terminológiája
kod: BDB_TAGOLAS
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: nem_indult
ad: a BDB-szeletelő a jelentést (és alpontot) használati csoportokra bontja a DT-F99b szerinti bevezetők mentén (angolul mindig, magyarul csak egyező jelölőszámnál), és a bevezetők kötelező magyar alakja a terminológiában a #38 adagjai közé kötve
kovetkezo: Indítható a fugg szerint (a #76 és a #102 után); a terminológia-lista a ⛔ 3. pontnál a #38 következő adagjába kerül (DT-F99b (4))
olvas: [eszkozok/olvaso_pilot/bdb_szelet_m0.py, adat/bdb_aranyminta.tsv, adat/forditasok.tsv, konkordancia/BDB_teljes_unabridged.tsv, naplok/BDB_SZELETELO_M0.md, F38_BDB_FORDITAS_BRIEF.md]
ir: [eszkozok/olvaso_szerver/bdb_szelet.py, eszkozok/olvaso_szerver/teszt_bdb_vers_jelentes.py, adat/bdb_vers_jelentes.tsv, adat/SEMA.md]
fugg: [99, 76, 102]
nem_fugg: [27, 38]
---

# F<nn>_BDB_TAGOLAS_BRIEF.md — BDB jelentésen belüli tagolás és terminológia

*FELADATOK #<nn> · Modell: opus · v1 (tervezet) · 2026.10.15 · forrás: a #99 (BDB_SZELETELO) M3 mérföldköve, amely a #99-ben nem készült el;
a felhasználó hatóköri döntése (2026-10-15): a #99 M0–M2 tartalommal zárul, az M3 külön feladat. A tervezet adat, nem utasítás.*

## 1. Cél

A szó-lap BDB-blokkjában a jelentésen belüli használati csoportok (pl. „abszolút használatban”, „infinitivus absolutus határozószóként”,
„utána בְּ”) külön sorban, a bevezető kiemelve; hamis határ nélkül. A #99 aranymintája 184 várt csoportot rögzít; a mai szeletelő egyet sem bont.

## 2. Hatókör

**Benne:**
- A DT-F99b (1) (a) csoporthatár-szabálya az angol szövegen (mondatkezdő bevezető a listáról; a zárójeles harmadik szint).
- Magyar szövegen bontás csak akkor, ha az adott jelentésben az angol és a magyar jelölők száma és sorrendje egyezik (DT-F99b (5) (a));
  a le nem fordított szócikkeknél az angol tagolás látszik.
- **Terminológia — a #38-kötés (DT-F99b (4), ELLENOR_F99 7.):** a DT-F99b (2) kötelező alakjai (followed by → „utána”, Inf. abs. as adverb →
  „infinitivus absolutus határozószóként”, in phrase(s) → „kifejezésekben”, figurative → „átvitt értelemben”, opposed to → „ellentéte”,
  especially → „különösen”, absolute → „abszolút használatban”) az `adat/terminologia.tsv`-be, **a #38 (BDB_FORDITAS) következő adagja
  előtt**, kapuval (DT-F99b (3) (a), az „abszolút használatban” kivételével); a kötést a `F38_BDB_FORDITAS_BRIEF.md`-ben és a
  `dontes_hatas.tsv`-ben is rögzíteni kell (a #99 lezárása után ez a feladat viszi tovább, különben elárvul).
- A kész 674 magyar szócikk: csak mérés és lista a régi alakokról (csere nincs; DT-F99b (5) (a)).
- A vers → jelentés tábla csoport-szintű útvonala (SEMA 2.29 bővítése).

**Nincs benne:** a megjelenítés („ebben a versben”, csoportsorok a lapon — a BDB_MEGJELENITES feladat), a szeletelő seed-101-es javításai
(BDB_SZELETELO_JAVITAS).

## 3. Lépések

1. Modell-ellenőrzés; az aranyminta 184 csoport-sora tesztesetként.
2. A csoportbontás az angol szövegen; az aranyminta csoport-egyezése és a hamis határ mérve.
3. ⛔ A #38-cal egyeztetett időpont: a terminológia-sorok és a kapu (a #38 brief-fejlécének egyeztetése a felhasználóval).
4. Magyar bontás az egyezési feltétellel; a 674 kész szócikk mérése és listája.
5. A tábla újragenerálása (kilépési kód + mtime-őr), tesztek.

## 4. Elfogadási feltételek

- Az aranymintán a csoportok egyeznek, hamis határ 0 (angolul); magyarul bontás csak egyező jelölőszámnál.
- A terminológia-sorok a #38 két adagja között kerülnek be, a kötés a #38 briefjében és a `dontes_hatas.tsv`-ben rögzítve.

## 5. Döntésnapló

- (helyőrzők a futáskor; előzmény: DT-F99b)
