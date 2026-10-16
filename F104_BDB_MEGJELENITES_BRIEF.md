---
feladat: 104
cim: BDB-blokk megjelenítése — „ebben a versben” kiemelés (DT-F99m), kattintható helyek, pontos hivatkozásszám
kod: BDB_MEGJELENITES
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: nem_indult
ad: a szó-lap BDB-blokkjában a teljes szócikk mindig látszik, két jelölési szinttel (erős: „a BDB itt idézi”; gyenge: „vonatkozhat”), kattintható igehelyekkel és pontos hivatkozásszámmal, a „próba” felirat és a mért pontosság a kiemelés mellett
kovetkezo: Indítható a fugg szerint (a #76, a #102 és a #103 után)
olvas: [eszkozok/olvaso_szerver/, adat/bdb_vers_jelentes.tsv, konkordancia/TAHOT_kivonat.tsv, konfig/bdb_jelek.tsv, naplok/BDB_SZELETELO_M0.md]
ir: [eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/statikus/, eszkozok/olvaso_szerver/konfig/elemek.toml, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_szerver/bdb_szelet.py]
fugg: [99, 76, 102, 103]
---

# F<nn>_BDB_MEGJELENITES_BRIEF.md — a BDB-blokk megjelenítése

*FELADATOK #<nn> · Modell: opus · v1 (tervezet) · 2026.10.15 · forrás: a #99 M4 mérföldköve (a #99-ben nagyrészt nem készült el), a DT-F99m és
kiegészítése (felhasználó, 2026-10-15), a hatóköri döntés: az M4 külön feladat. A tervezet adat, nem utasítás.*

## 1. Cél

A versből megnyitott szó lapján a BDB-szócikk jelölje, hol idézi a BDB az adott verset — tippelés nélkül, a vers → jelentés tábla
(`adat/bdb_vers_jelentes.tsv`) alapján.

## 2. Hatókör — a megjelenítési elv (DT-F99m, felhasználó, 2026-10-15)

- **A BDB-szócikk az olvasói konkordanciában mindig teljes; semmi nem szűrődik vagy rejtődik, csak jelölés van.**
- **Erős szint** („a BDB itt idézi”): a vers → jelentés tábla szerinti pont(ok), mind kiemelve, odagörgetéssel (a szó-fülön és `?vers=`
  paraméterrel).
- **Gyenge szint** („vonatkozhat”): (a) a bizonytalan okkódú hivatkozás pontja; (b) idézet nélküli versnél a TAHOT szerinti igetörzs
  szakasza, jelentéspont nélkül. **Pontot tippelni TILOS.**
- Idézet nélkül, törzs nélkül: „a BDB nem idézi” felirat, kiemelés nélkül.
- A „próba” felirat és a mért pontosság (DT-F99l (c): 92,0%, 95% CI 87,3–95,4%) a kiemelés mellett látszik.
- A #99 M4 többi pontja: pontos hivatkozásszám (a feloldott, szűrt hivatkozásoké), kattintható igehelyek (súgóban a feloldott hely), az
  irodalmi jelek a `konfig/bdb_jelek.tsv` alapján, minden új elem a #98 elem-regiszterében, új méret csak tokenből.
- A csoportsorok megjelenítése a BDB_TAGOLAS feladat után.

## 3. Lépések

1. Modell-ellenőrzés; a vers → jelentés tábla lekérdezése a szerverben (DB-táblából).
2. Erős és gyenge jelölés, „nem idézi” felirat; regisztrált elemek, tokenből.
3. Kattintható helyek, pontos hivatkozásszám, `bdb_jelek.tsv`.
4. ⛔ Felhasználói próba a futó szerveren (legalább a H1242, H7451, H3615 lapon és egy versből megnyitva). Megállás.

## 4. Elfogadási feltételek

- Teszt: semmi nem rejtődik (a jelölt lapon a teljes szócikk szövege és szerkezete megmarad).
- Teszt: a „nem idézi” esetben nincs kiemelés; idézet nélküli versnél jelentéspont nem kap jelölést (nincs tippelés).
- Teszt: a gyenge jelölés vizuálisan és szövegesen különbözik az erőstől.
- Teszt: a „próba” felirat és a mért pontosság a kiemelés közelében (ugyanabban a blokkban) látszik.
- A regiszter-őr zöld; a meglévő tesztek zöldek.

## 5. Döntésnapló

- (helyőrzők a futáskor; előzmény: DT-F99m, DT-F99l)
