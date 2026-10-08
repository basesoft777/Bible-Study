---
feladat: 63
cim: A 8 régi motívum jelölt-sorainak pótlása a naplókból, és a „még nem vizsgált” lista
kod: JELOLTEK_RETRO
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: nem_indult
ad: a 8 retroaktív (F3/N14) motívum vizsgált, de a jeloltek.tsv-ből hiányzó jelöltjei a naplókból pótolva, mindegyik dontes és indoklas mezővel (ahol a napló nem mond döntést: nyitva, explicit jelöléssel); egy generátor (eszkozok/nem_vizsgalt.py) adja a „még nem vizsgált” listát (auditok-scan − jeloltek); az ANTROP-001 lelet-lapjának (12-es) első teljes adatfutása
kovetkezo: /kovetkezo; ⛔ az M0 után (forrás-leképezés és hiánymérés), és az M2 ANTROP-001 mintája után; a #11 előtti befagyasztás nem érinti (adatréteg, DT74 (3))
olvas: [adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/auditok.tsv, adat/motivumok.tsv, adat/SEMA.md, tematikus_lezart/, motivumlog/, melyelemzesek/, genezis/, eszkozok/jelolt.py, eszkozok/lekerdez.py]
ir: [adat/jeloltek.tsv, eszkozok/nem_vizsgalt.py, eszkozok/teszt_nem_vizsgalt.py]
fugg: []
nem_fugg: [55, 61, 65]
---

# F63_JELOLTEK_RETRO_BRIEF.md — A 8 régi motívum jelölt-sorainak pótlása

*FELADATOK #63 · Modell: sonnet · v1 · 2026.10.05 · forrás: `MUNKATERV.md` 4. szakasz (JELOLTEK_RETRO, 1. hullám), `ADATVAGYON_TERV.md` 5. szakasz (12-es lelet-lap), `adat/SEMA.md` 2.4*

## 1. Cél

A CLAUDE.md 2. szabálya szerint minden jelölt a `adat/jeloltek.tsv`-n megy át, döntéssel és indoklással — így látszik, mit vizsgált a kutatás és mit vetett el, nem csak az, amit elfogadott. A 8 régi motívum (ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, ISTENTISZT-001, KIRALY-001, MENNY-001, TEREMT-001) a szabály előtt készült, és utólag (F3, N14) került a táblákba.

**Állapot a befogadáskor (2026.10.05, sorszám):**

| motívum | jeloltek | elofordulasok |
|---|---|---|
| ALVIL-001 | 72 | 72 |
| HAMART-001 | 52 | 52 |
| TEREMT-001 | 41 | 41 |
| ISTENTISZT-001 | 32 | 32 |
| KIRALY-001 | 9 | 9 |
| ANTROP-001 | 9 | 8 |
| MENNY-001 | 11 | 9 |
| HODIT-001 | 50 | 33 |
| *TEREMT-002 (natív, összevetésül)* | *66* | *3* |

A régi motívumoknál a két szám többnyire egyezik: a `jeloltek.tsv` lényegében csak a beépített sorokat tartalmazza, az elutasított és vizsgált jelöltek a naplókban élnek. Ez a befogadáskori olvasat; a tényleges hiányt az M0 méri.

A feladat a hiányzó sorokat adatként pótolja, és megépíti a „még nem vizsgált” listát, amely a 12-es lelet-lap (★ = a projekt saját lexikai lelete, amelyet a TSK nem jelez) alapja.

## 2. Hatókör

**Benne van:**
- a 8 motívum hiányzó `jeloltek.tsv`-sorai a dokumentált forrásokból (kereszthivatkozás-naplók, tematikus tanulmányok, `motivumlog/`, mélyelemzések), soronként `forras_kereses`, `dontes`, `indoklas`, `datum` mezővel (SEMA 2.4);
- `eszkozok/nem_vizsgalt.py`: motívumonként a „még nem vizsgált” lista = az `auditok.tsv` scan-lekérdezéseinek találatai − a `jeloltek.tsv` igehelyei; a lekérdezéseket a `lekerdez.py` futtatja újra, a saját proveniencia-sorával;
- az ANTROP-001 lelet-lapjának adatfutása (12-es: lexikai kör − TSK-kör), jelentésként.

**Nincs benne:**
- új tartalmi ítélet: ahol a forrás nem mond egyértelmű döntést, a sor `dontes = nyitva`, `indoklas` = „nincs dokumentált döntés (forrás: …)”. **A hiány nem tölthető ki gyenge vagy asszociatív indoklással** (CLAUDE.md 3. szabály); a `nyitva` sorok elbírálása külön, értelmező feladat;
- `elofordulasok.tsv`-sor felvétele vagy törlése (a 2. szabály: találatból nincs közvetlen út);
- motívumfájl írása (`motivumok/`, `tematikus_lezart/`, `motivumlog/`) és generált kimenet írása (`lexikon/`; a DT28 szerint nem motívumfájl, de kézzel nem írható);
- a TEREMT-002 (natív, a jelöltjei megvannak);
- a lelet-lap renderelése vagy publikálása (az OLVASOI_KONKORDANCIA dolga) és a többi 7 motívum lelet-futása (az M2 minta után, ha a felhasználó kéri, ugyanebben a feladatban vagy külön).

## 3. Lépések

### M0 — Forrás-leképezés, hiánymérés és ⛔

Jelentés: `naplok/JELOLTEK_RETRO_M0.md`.
1. Motívumonként a döntéseket hordozó források listája (melyik napló, tanulmány, `motivumlog/` fájl), és hogy van-e kereszthivatkozás-naplója (SEMA 2.4.1: négy napló hiányzik).
2. Motívumonként: a forrásokban vizsgált igehelyek száma, ebből hány van már a `jeloltek.tsv`-ben, és hány hiányzik; a hiányzók közül hánynál mond a forrás egyértelmű döntést és indoklást.
3. Az `auditok.tsv` scan-sorai motívumonként: futtatható-e belőlük a „még nem vizsgált” lista (a proveniencia-sor elég-e a lekérdezés megismétléséhez).
4. Az írás módja: a `jelolt.py` írja-e a sorokat, vagy egy egyszeri, összevetéssel ellenőrzött hozzáfűzés (minta: `eszkozok/igazolas_migracio.py`; `split('\t')` / `'\t'.join()`, a `csv` modul tilos).

**⛔ Megállás:** a felhasználó elfogadja a forrás-leképezést, a hiányszámokat és az írás módját.

### M1 — Pótlás

- Motívumonként külön commit (`F63.<n>: <ID> jelölt-sorok pótlása`), csak hozzáfűzés; meglévő sor nem változik.
- Minden új sor `forras_kereses` mezője megnevezi a forrásfájlt és helyet; `datum` a pótlás napja.
- A `nyitva` sorok száma motívumonként a naplóba kerül.

### M2 — „Még nem vizsgált” lista és az ANTROP-001 minta, ⛔

- `nem_vizsgalt.py` + `teszt_nem_vizsgalt.py` (ideiglenes táblamásolaton).
- ANTROP-001: a „még nem vizsgált” lista és a lelet-lap adata (`naplok/JELOLTEK_RETRO_lelet_ANTROP.md`): minden ★ sor mellett `dontes` + `indoklas` a `jeloltek.tsv`-ből, vagy explicit „még nem vizsgált”.

**⛔ Megállás:** a felhasználó átnézi az ANTROP-001 mintát; dönt, hogy a többi 7 motívum lelet-futása ebben a feladatban fut-e.

### M3 — Zárás

`naplok/JELOLTEK_RETRO_zaras.md` (≤20 sor: motívumonként pótolt / `nyitva` / még nem vizsgált), `fuggetlen-ellenor` (`naplok/ELLENOR_JELOLTEK_RETRO.md`, szúrópróba: 10 pótolt sor visszakeresése a forrásban), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Minden új `jeloltek.tsv`-sor forrása visszakereshető; elutasított sornál az `indoklas` a forrásból jön, nem új ítélet.
- **K2.** Nincs kitalált döntés: a dokumentálatlan esetek `nyitva`, explicit jelöléssel.
- **K3.** Meglévő sor nem változott; az `elofordulasok.tsv` érintetlen; az `ellenoriz.py` és a CI zöld.
- **K4.** ANTROP-001: minden ★ sor mellett `dontes` + `indoklas`, vagy explicit „még nem vizsgált” jelölés (a munkaterv kis mintája: 0 jelöletlen sor).
- **K5.** A független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | A dokumentálatlan döntés `nyitva` értéket kap, nem új zárt értéket (a SEMA 2.4 meglévő listája elég). | befogadás |
| v1 | 2026-10-05 | `munka: adat`: a feladat dokumentált döntéseket visz át, motívumfájlt nem ír; az elbírálás külön értelmező feladat. | befogadás, KONTEXTUS K1 |
