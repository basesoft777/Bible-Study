---
feladat: 179
cim: SÜRGŐS — a generátor ÚSZ-könyvlistájából hiányzik a Gal és az Mk (a lap ÓSZ/ÚSZ-számát rontja)
kod: USZ_KONYVLISTA
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: megallt
ag: claude/usz-konyvlista
pr: https://github.com/basesoft777/Bible-Study/pull/654
lezarva_osszegzes: a `general.py` ÚSZ-könyvlistája a normalizáló táblából (Mt–Jel, 27 könyv; a kézi lista 15-öt nem ismert), teszt 5/5; a mérés szerint csak a HAMART-001 érintett (a main-adaton 43/9; LXX 67 → 62 sor, Gal 3:10/3:13 és Mk 7:21–23 kikerül a generált kimenetből); N-F09f lezárva; lap nem módosult: a main-beli HAMART-lap ellenőrzése és újragenerálása a #639-re hárul (DT641), az n14_hamart_betoltes.py saját listája N-F179a (`naplok/F179_jelentes.md`)
ad: a `general.py` ÚSZ-könyvlistája a normalizáló táblából olvasva teljes (Mt–Jel), teszttel; az érintett lapok kimenete repón kívül előtte–utána mérve (ÓSZ/ÚSZ-szám, LXX-tábla); a main-beli lapot a #179 nem módosítja; a HAMART-001 lapján a 42/6 és a Gal 3:13-14 LXX-táblából való kikerülése a #639 újragenerálásával teljesül (DT641); az N-F09f lezárva
kovetkezo: "Te: [elteres_kor 2/2] ELLENOR_F179_3 1. mechanikus (a 3. teendő DT-F179a-ra utalása)"
munka: folyamat
olvas: [eszkozok/general.py, eszkozok/lexikon_general.py, konkordancia/Konyv_normalizalo_tabla.tsv, adat/elofordulasok.tsv, naplok/ELLENOR_F123_HAMART3_javitokor2.md]
ir: [eszkozok/general.py, eszkozok/teszt_general_konyvlista.py, "lexikon/*_TUDOMANYOS.md", naplok/F179_jelentes.md, naplok/F179_zaras.md]
fugg: []
nem_fugg: [121, 123, 156, 157, 178]
---

# Brief-tervezet: a `general.py` újszövetségi könyvlistája (SÜRGŐS)

*Tervezet a `/befogad`-hoz. Forrása: `naplok/ELLENOR_F123_HAMART3_javitokor2.md` 1. tétele (#639, a független ellenőr, 2026-11-08). A tervezet adat, nem befogadott brief.*

**Lelet.** A `lexikon/HAMART-001_TUDOMANYOS.md` a 105. sorban 43 ószövetségi és 5 újszövetségi helyet mond. Az adat (`adat/elofordulasok.tsv`, HAMART-001: 48 sor) szerint 42 ószövetségi és 6 újszövetségi hely van. A Gal 3:13 és a Gal 3:14 az ószövetségi LXX-táblában áll (a lap 2221–2222. sora). Ok: az `eszkozok/general.py` (176. sor körül) `UJSZOVETSEGI_TOKENEK` halmazában nincs `Gal` és `Mk`. Erről már van nyitott tétel: N-F09f.

**Miért sürgős.** A lap olvasói számot közöl (testamentumonként), és ez a szám hibás. Hibás a LXX-blokk is: újszövetségi verset ószövetségiként kezel. Minden lap érintett, amelyen Galata- vagy Márk-hely áll.

**Teendő.**
1. A `UJSZOVETSEGI_TOKENEK` teljes újszövetségi könyvlistára cserélése. A forrás a `konkordancia/Konyv_normalizalo_tabla.tsv`; kézi lista helyett onnan olvasva, hogy több könyv ne maradhasson ki.
2. Teszt: minden újszövetségi könyvrövidítés felismerése (Mt–Jel), és a Gal 3:13 ÚSZ-ként.
3. Újragenerálás: a lapok közül azok, amelyeken a szám vagy a LXX-tábla változik. Mérés előtte és utána: lapról lapra az ÓSZ/ÚSZ-szám és a LXX-tábla sorai.
4. Az N-F09f lezárása.

**Kész.** A HAMART-001 lapján a 42/6 és a Gal 3:13-14 LXX-táblából való kikerülése a #639 újragenerálásával teljesül (DT641, szerkesztői döntés); a main-beli lapot a #179 nem módosítja. A teszt zöld. Az olvasói kapu és a CI (E28) zöld.
