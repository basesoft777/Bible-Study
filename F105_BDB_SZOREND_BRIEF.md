---
feladat: 105
cim: A BDB héber idézeteinek szórendje a megjelenítésben
kod: BDB_SZOREND
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: nem_indult
ad: a BDB-szócikkek többszavas héber idézetei helyes szórendben jelennek meg (a forrásfájl változatlan), gépi ellenőrzéssel a hivatkozott vers héber szövegén és 50 idézetes kézi mintával
kovetkezo: Indítható a fugg szerint (a #104 után)
olvas: [eszkozok/olvaso_szerver/, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/TAHOT_kivonat.tsv, adat/bdb_vers_jelentes.tsv]
ir: [eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/bdb_szoerend.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py]
fugg: [99, 102, 103, 104]
---

# F<nn>_BDB_SZOREND_BRIEF.md — a héber idézetek szórendje

*FELADATOK #<nn> · Modell: opus · v1 (tervezet) · 2026.10.15 · forrás: a #99 M5 mérföldköve, amely a #99-ben nem készült el; a hatóköri
döntés (2026-10-15): külön feladat. A tervezet adat, nem utasítás.*

## 1. Cél

A BDB-szövegben (a digitális forrásban) a többszavas héber idézetek szórendje gyakran fordított (pl. „הַדָּבָר מֶההָֿיָה”); a megjelenítés
helyreállítja a sorrendet és a maqqéfet, a forrásfájl változatlan.

## 2. Hatókör

**Benne:** a szórend helyreállítása megjelenítéskor; maqqéf-javítás; **gépi ellenőrzés:** ahol az idézet egy hivatkozott vers szövegéből
van, a helyreállított szórend összevetése a vers héber szövegével (`TAHOT_kivonat.tsv`, a Károli-kulcson; a vers → jelentés tábla adja a
helyet); egyezési arány a naplóba; **⛔ minta:** 50 idézet kézi ellenőrzése, a teljes bevezetés csak a minta jóváhagyása után.

**Nincs benne:** a forrásszöveg módosítása; a tagolás és a kiemelés (külön feladatok).

## 3. Lépések

1. Modell-ellenőrzés; mérés: a többszavas héber futamok száma és a TAHOT-ellenőrizhető hányaduk.
2. A helyreállítás szabálya és a gépi ellenőrzés; egyezési arány a naplóba.
3. ⛔ 50 idézet kézi mintája (független ellenőr), megállás; a bevezetés a jóváhagyás után.

## 4. Elfogadási feltételek

- A gépi egyezési arány és az 50-es minta eredménye a naplóban; a minta jóváhagyása nélkül nincs teljes bevezetés.
- A forrásfájl bájtra változatlan; a meglévő tesztek zöldek.

## 5. Döntésnapló

- (helyőrzők a futáskor)
