---
feladat: 59
cim: Olvasói szószedet — jóváhagyott, szerkesztői magyarázó tábla az olvasói nézethez
kod: SZOSZEDET
tipus: feladat
fazis: 2
modell: opus
munka: ertelmezo
allapot: nem_indult
ad: egy repóban tárolt, tételenként jóváhagyott magyarázó tábla (adat/szoszedet.tsv) az olvasói nézet szakszavaihoz és blokkjaihoz; minden sor „szerkesztői szöveg” jelölésű, forrás- vagy hivatkozásmezővel, és csak a felhasználó jóváhagyása után jelenhet meg
kovetkezo: /kovetkezo; ⛔ a tervezet után (tételenkénti jóváhagyás)
olvas: [adat/SEMA.md, adat/datasetek.tsv, adat/licencek.tsv, ADATVAGYON_TERV.md, MUNKATERV.md]
ir: [adat/szoszedet.tsv, adat/SEMA.md]
fugg: [58]
nem_fugg: [52]
---

# F59_SZOSZEDET_BRIEF.md — Olvasói szószedet

*FELADATOK #59 · Modell: opus · v1 · 2026.10.05 · forrás: az olvasói pilot (1Móz 1:1–2:3) tapasztalata, felhasználói döntés 2026-10-05*

## 1. Cél

Az olvasói nézetnek szüksége van rövid magyarázatokra (pl. Strong-szám, Septuaginta, törzs, ketiv/qere, szemantikai domén, az adatblokkok jelentése). A pilotban ezeket emlékezetből írt szöveg adta, ezért kikerültek: a pilot csak adatot mutathat. A feladat ezt a réteget **adatként** hozza létre: egy szerkesztői táblát, amelynek minden sorát a felhasználó tételenként jóváhagyja, és amely a lapon is „szerkesztői szöveg”-ként jelölve jelenik meg.

Ez nem lekérdezés-eredmény, hanem jóváhagyott szerkesztői réteg (CLAUDE.md 3. szabály: ami nem a repó adatából jön, az értelmezés; itt az értelmezés jelölten és jóváhagyva kerül a repóba).

## 2. Hatókör

**Benne van:**
- a tábla sémája (SEMA);
- a tételjegyzék: a pilot blokkjai és szakszavai, valamint a #58 jelkulcsának nyelvtani megnevezései (törzsek, igealakok, állapotok);
- tervezet, tételenkénti jóváhagyás, rögzítés.

**Nincs benne:**
- a megjelenítés (az olvasói nézet feladata);
- motívum- vagy igehely-értelmezés: a szószedet csak fogalmakat és adatblokkokat magyaráz, bibliai szöveget nem értelmez.

## 3. Lépések

### M0 — Séma és tételjegyzék

- `adat/szoszedet.tsv` javasolt oszlopai: `kulcs`, `cim`, `szoveg`, `tipus` (`fogalom` / `adatblokk` / `nyelvtan`), `hivatkozas` (adatkészlet, fájl vagy szakirodalom, ha van), `allapot` (`javaslat` / `jovahagyott` / `elvetett`), `jovahagyas_datum`, `modell`.
- A tételjegyzék: a pilot blokkcímei, a lábjegyzetek szakszavai, a #58 jelkulcsának magyar megnevezései. A nyelvtani tételek a #58 tábláján állnak; ezért függ tőle a feladat.
- SEMA-szakasz; a `szoveg` mező szabálya: rövid (≤ 3 mondat), köznyelvi, és nem állít a repó adatával ellentétes tényt. Ha tényt állít (pl. évszám, keletkezés), a `hivatkozas` mezőben forrás áll, vagy a tétel `javaslat` marad.

### M1 — Tervezet és ⛔

- Minden tételhez egy tervezetsor, `allapot: javaslat`, a `modell` mezőben a tényleges modellnév.
- **⛔ Megállás:** a felhasználó tételenként dönt (`jovahagyott` / `elvetett` / javítással jóváhagyott). Csak a `jovahagyott` sor jelenhet meg az olvasói nézetben.

### M2 — Rögzítés és zárás

- A döntések átvezetése a táblán, `jovahagyas_datum`-mal.
- `naplok/SZOSZEDET_zaras.md` (≤20 sor), `fuggetlen-ellenor` (`naplok/ELLENOR_SZOSZEDET.md`), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- **K1.** Minden sor `allapot`-tal és `modell`-lel; a `jovahagyott` sorok jóváhagyási dátummal.
- **K2.** A ténymegállapítást tartalmazó soroknál van `hivatkozas`, vagy a sor nem `jovahagyott`.
- **K3.** A tábla nem értelmez bibliai szöveget, csak fogalmat és adatblokkot magyaráz.
- **K4.** A CI zöld; a független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

| Verzió | Dátum | Döntés | Forrás |
|---|---|---|---|
| v1 | 2026-10-05 | Az olvasói magyarázat szerkesztői rétegként, adatként és jóváhagyva kerül a repóba; jóváhagyás nélkül nem jelenik meg. | felhasználó |
| v1 | 2026-10-05 | 2. fázis: az olvasói nézethez tartozik; függ a #58 jelkulcstól (a nyelvtani tételek miatt). | befogadás |
| v1 | 2026-10-05 | `nem_fugg: [52]`: a tervdokumentum olvasása kontextus, nem adatfüggés. | kontextus-olvasás |
