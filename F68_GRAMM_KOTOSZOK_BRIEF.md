---
feladat: 68
cim: Okhatározói és következtető kötőszók a nyelvtani Strong-listán, hatásméréssel
kod: GRAMM_KOTOSZOK
tipus: feladat
fazis: folyamat
modell: sonnet
munka: adat
allapot: lezarva
pr: https://github.com/basesoft777/Bible-Study/pull/244
lezarva_osszegzes: "A nyelvtani listára 7 kötőszó került (H3282, H0176, H3863, H3884, H6435, H0432, H3860); H3651 HATARESET, H6118 elutasítva, 4 halasztva (DT67). A gerinc-metszet változatlan, a H3282 LXX-nézete bővült."
ag: claude/gramm-kotoszok
ad: a H3282 (ja’an), H6118 (‘ekev), H3651 (lākēn) — és a felvételi kritérium szerint hasonló kötőszók — elbírálása a HEBER_KEZI listán át, a gerinc-metszetre és az F56 LXX-szűrésre gyakorolt hatás mérésével
kovetkezo: "—"
olvas: [eszkozok/grammatikai_strongok_general.py, adat/grammatikai_strongok.tsv, konkordancia/Strong_szotar.tsv, konkordancia/TAHOT_kivonat.tsv, adat/SEMA.md, eszkozok/bdb_adatblokk.py, eszkozok/lekerdez.py, adat/kulso/lxx_bridge.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv, naplok/F56_zaras.md, naplok/BDB_ADATBLOKK_M0.md]
ir: [eszkozok/grammatikai_strongok_general.py, adat/grammatikai_strongok.tsv, eszkozok/f4_0c_korut_ellenoriz.py, eszkozok/teszt_bdb_adatblokk.py, naplok/GRAMM_KOTOSZOK_*.md]
fugg: []
nem_fugg: [61, 62, 63, 65]
---

# F68_GRAMM_KOTOSZOK_BRIEF.md — Okhatározói és következtető kötőszók a nyelvtani Strong-listán

*FELADATOK #68 · Modell: sonnet · v1 · 2026.10.06 · forrás: `naplok/F56_zaras.md` „Nyitott javaslatok” (a); `naplok/BDB_ADATBLOKK_M0.md` 3. szakasz (a H3282 nyitott kérdése)*

## 1. Cél

Az `adat/grammatikai_strongok.tsv` két helyen szűr: a gerinc-metszetben (`lekerdez.py gerinc`) és a #56 BDB-adatblokkjának LXX-szakaszában (`bdb_adatblokk.py`, ha a héber szó nem nyelvtani, a görög nyelvtani találatok kimaradnak). Az F56 mintájában a H3282 (ja’an, „mert”) nincs a listán, ezért nála a G3754 ὅτι és a G1223 διά kimarad az LXX-párok közül, holott éppen ezek a valódi megfelelői. Az F56-ban a felhasználó úgy döntött, hogy a lista ott érintetlen marad. A kérdés ezért ide került: a H3282, a H6118, a H3651, és a felvételi kritérium szerint hozzájuk hasonló szavak felkerüljenek-e a `HEBER_KEZI` listára.

A feladat nem a felvételt dönti el, hanem előkészíti: jelöltlistát, kritérium-vizsgálatot és hatásmérést ad, a felvételről a felhasználó dönt (⛔ M0 után). A felvétel csak a generátoron át történik, a tábla kézi szerkesztése tilos.

## 2. Hatókör

**Benne van:**
- a három megnevezett Strong és a `Strong_szotar.tsv` szerint `kötőszó` szófajú, a listán még nem szereplő héber Strongok átnézése a generátor kritériuma szerint („a szó önmagában nem hordoz tartalmi jegyet”);
- hatásmérés a felvétel előtt és után: a gerinc-metszet és az F56 LXX-szűrés változása;
- jóváhagyás után a `HEBER_KEZI` bővítése tételes indoklással, a tábla újragenerálása.

**Nincs benne:**
- a görög oldal (a G-lista tükrözését csak jelezni kell, ha egy felvett héber szó görög párja hiányzik; a bővítése külön döntés);
- a `HATARESET` (H3605) és a `TILTOLISTA` módosítása;
- a BDB-adatblokkok újragenerálása és a már átvezetett fordítások módosítása (ez a #38 menetéé; itt csak a mérés);
- a #56 (b) és (c) javaslata.

## 3. Lépések

**M0 — felmérés (csak olvas, kimenet: `naplok/GRAMM_KOTOSZOK_M0.md`).**
1. Jelöltlista: a három megnevezett Strong, továbbá minden `kötőszó` szófajú héber Strong a `Strong_szotar.tsv`-ből, amely nincs a táblán. Soronként: Strong, szótő, szófaj, jelentés, ÓSZ-gyakoriság (TAHOT; a TAHOT hiányos, l. CLAUDE.md), kategória-javaslat.
2. **Kritérium-eltérés, külön jelölve.** A generátor „ellenőrizhető jele” szerint a kézi tételek szófaja elöljárószó, kötőszó vagy névmás. A `Strong_szotar.tsv` szerint viszont a H6118 `főnév, hímnemű` („consequence”), a H3651 `határozószó` („so”). A H6118 önálló főnévként tartalmi jelentést is hordoz (pl. „jutalom”), a H3651 (lākēn = lə + kēn) pedig a prófétai ítéletformula része („ezért így szól az ÚR”). Mindkettőnél meg kell nézni, hogy a Strong-szám a kötőszói és a tartalmi használatot szétválasztja-e, vagy egy számon fut mindkettő. Ha nem választja szét, a felvételük leletet törölhet: ezt a M0 jelzi, és nem dönti el.
3. Negatív próba: a jelöltek előfordulnak-e `gerinc_elem`-ként vagy `strong` értékként az `elofordulasok.tsv`-ben, a `jeloltek.tsv`-ben és a motívumok gerinc-naplóiban. (A befogadáskor a három megnevezett Strongra 0 találat volt a két táblában; ezt a M0 újra lekérdezi, provenienciával.)
4. Hatásmérés két ponton, a felvétel előtt és után (az utóbbi ideiglenes táblával, a repón kívül):
   - gerinc-metszet: a meglévő gerinc-levezetések közül azok, amelyekben a jelölt a metszetben áll, és a metszet mérete előtte/utána;
   - F56 LXX-szűrés: az érintett BDB-adatblokkok LXX-szakaszának különbsége (mely görög találat kerül be vagy esik ki), legalább a H3282 F56-mintabeli esetén.
5. ⛔ **Megállás.** A felhasználó jelöltenként dönt: felvétel (kategóriával), elutasítás, vagy `HATARESET`. A döntés tétele a `DONTESEK.md`-be kerül (`DT67`, …).

**M1 — felvétel (csak a jóváhagyott tételekkel).**
1. A `HEBER_KEZI` bővítése a generátorban, tételes indoklással (a meglévő tételek mintájára: miért nem hordoz tartalmi jegyet, és van-e görög párja a listán). Ha egy tétel a szófaj-jel alól kivétel, a kritérium-kommentben ezt rögzíteni kell.
2. A tábla újragenerálása; írás előtt és után soronkénti összevetés: csak a jóváhagyott sorok jelenhetnek meg újként, a többi sor bájtra azonos (a `ts` sor kivételével).
3. A hatásmérés megismétlése a valódi táblával; az eredmény egyezzen a M0 ideiglenes mérésével.

**Zárás.** `naplok/GRAMM_KOTOSZOK_zaras.md` (≤15 sor), `fuggetlen-ellenor` (`naplok/ELLENOR_GRAMM_KOTOSZOK.md`), a brief fejléce `lezarva`, push, draft PR.

## 4. Elfogadási feltételek

- A M0 jelöltlistája minden jelöltről ítéletet kér, és a kritérium-eltéréseket (szófaj, tartalmi használat) külön jelöli.
- A tábla csak a generátorból változik; a soronkénti összevetés szerint csak a jóváhagyott sorok újak.
- A `TILTOLISTA`-ellenőrzés lefut, és nem sérül.
- A gerinc-metszetre és az LXX-szűrésre gyakorolt hatás számszerűen dokumentált, előtte/utána; az üres eredmény is rögzítve.
- Minden lekérdezésből származó állítás mellett ott a proveniencia-sor.
- `python eszkozok/feladatok.py ellenoriz` 0 hiba; `python eszkozok/ellenoriz.py` SÉRTÉS 0; a `teszt_bdb_adatblokk.py` zöld (ha egy teszt a felvett Strongtól függően változik, az eltérés indokolva).

## 5. Döntésnapló

- (a M0 kész, `naplok/GRAMM_KOTOSZOK_M0.md`; a jelöltenkénti döntés `DT67` a `DONTESEK.md`-ben eldöntve (🟢), 2026.10.08: 7 felvétel, H3651 HATARESET, H6118 elutasítva, 4 halasztva; az M1 kész, `naplok/GRAMM_KOTOSZOK_zaras.md`)
