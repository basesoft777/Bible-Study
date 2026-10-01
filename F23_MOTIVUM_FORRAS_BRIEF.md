---
feladat: 23
cim: Egyforrású motívumdokumentum: forrássablon és mélységi szintek (terv)
kod: MOTIVUM_FORRAS
tipus: feladat
fazis: 1
modell: opus
allapot: nem_indult
ad: a B szerkezet terve mérésekkel: szakasz-leképezés, forrássablon-tervezet, szintjelölés a SEMA-ban, CI-szabályok leírása; renderelés és fájlmozgatás nélkül
kovetkezo: /kovetkezo; ⛔ az M0 felmérés után
olvas: [sablonok/, tematikus_lezart/, motivumok/, lexikon/, genezis/, adat/SEMA.md, adat/res_forras.tsv, eszkozok/general.py, CLAUDE.md, ATALAKITASI_TERV.md.md]
ir: [sablonok/9_PaRDeS_motivum_forras_sablon.md, adat/SEMA.md]
fugg: []
nem_fugg: [22]
---

# F<nn>_MOTIVUM_FORRAS_BRIEF.md — Egyforrású motívumdokumentum: forrássablon és mélységi szintek (terv)

*FELADATOK #<nn> · Modell: opus · v1 · 2026.09.30 · döntések: D34–D39 (a naplózó brief rögzíti; a számok a befogadáskor a következő szabad D-számtól csúszhatnak)*

## 1. Cél

A 2026.09.30-i döntés (D34, „B” út): motívumonként **egyetlen kézi forrás** legyen (`motivumok/[ID].md` + adattáblák). A tematikus sablon adja a szerkezetét. A tematikus tanulmány, a lexikonoldal és minden olvasói nézet ebből **generálódik**, állítható mélységgel. A törzscikk megszűnik.

Ez a feladat csak **tervez és mér**. Semmit nem renderel, nem mozgat, és nem ír át meglévő tanulmányt vagy lexikonoldalt. Ezért fér bele a D1 szerinti 1. fázisba: metaadat és séma, amely nem függ a késői forrásoktól. Az eredményére a #9, a #12 és a #11 épít.

## 2. Hatókör

**Benne van:** az M0 felmérés (csak olvas); a forrássablon tervezete; a szintjelölés szabálya a `adat/SEMA.md`-ben; két CI-szabály **leírása** (nem implementálása); a két pilot bemenetének leírása.

**Nincs benne:** a `general.py` módosítása; bármely `tematikus_lezart/`, `motivumok/`, `lexikon/` vagy `genezis/` fájl írása; a `CLAUDE.md` rétegtáblájának átírása (az a #11 dolga); a CI-szabályok implementálása (külön ágon, D6); HTML.

## 3. Lépések

### M0 — felmérés (csak olvas) ⛔ utána megállás

Minden számot a menetben ténylegesen futtatott parancs kimenetéből vegyél. Becsült vagy emlékezetből vett szám nem kerülhet a naplóba.

1. **Szakasz-leképezés.** Vedd sorra a `sablonok/4_PaRDeS_tematikus_sablon.md`, a `6_PaRDeS_lexikon_oldal_sablon.md` és a `8_PaRDeS_torzscikk_sablon.md` minden szakaszát, a `motivumok/[ID].md` blokkjait és az `adat/res_forras.tsv` réseit. Kimenet: `naplok/MOTIVUM_FORRAS_lekepezes.tsv`, oszlopok:
   `szakasz` · `sablon` · `ma_hol_el` · `B_helye` (`kezi_forras` / `adat` / `generalt`) · `szint` (`olvasoi` / `apparatus` / `belso`) · `aktivalas` (mindig / feltételes: mi a feltétel) · `megjegyzes`.
   Ha egy szakasz besorolása nem egyértelmű, `javaslat` jelölést kap, és az összesítő tételbe kerül.
2. **Csak a törzscikkben létező tartalom.** Motívumonként vesd össze a `lexikon/[ID]_TORZSCIKK.md`-t a `_TUDOMANYOS.md`-vel és a forrásokkal. Van-e olyan állítás vagy adat, amely csak a törzscikkben szerepel? Kimenet: `naplok/MOTIVUM_FORRAS_torzscikk_egyedi.tsv` (motívum, szakasz, szöveg-kivonat legfeljebb 15 szóban, hol kellene élnie). Az üres eredmény elfogadható, de jelölni kell.
3. **Tematikus tanulmányok és motívumok párosítása.** Melyik `tematikus_lezart/*_tematikus.md` melyik motívum-ID-hez tartozik, melyik motívumnak nincs tematikus tanulmánya, és melyik fájl nem tanulmány (pl. ellenőrző jegyzet)? Kimenet: `naplok/MOTIVUM_FORRAS_parositas.tsv`.
4. **NAPLO-keveredés.** Fájlonként számold meg a `tematikus_lezart/` és a `motivumok/` fájlokban:
   - a `【NAPLO: …】` blokkokat;
   - a gyanús, mondaton belüli proveniencia-szöveget: dátum, fájlnév, „l. X pont”, „felismerve / visszaírva / audit során”.

   Ez a migráció (#11) szintjelölési munkájának becslése. Kimenet: `naplok/MOTIVUM_FORRAS_naplo_keveredes.tsv`.
5. **Átfedés a bővített tanulmányokkal.** Keress szó szerinti vagy közel szó szerinti bekezdés-átfedést a `genezis/*_bovitett.md` és a `tematikus_lezart/` fájlok között. A módszert (pl. 8 szavas n-gram) a naplóban rögzítsd. Ez mutatja, hol kell a forrásnak hivatkoznia másolás helyett (D34). Kimenet: `naplok/MOTIVUM_FORRAS_atfedes.tsv`.
6. **Összesítés és ⛔ megállás.** Egy `DONTESEK.md`-tétel: a `javaslat` jelölésű besorolások, a 2–5. pont fő számai, és a kérdés, hogy mehet-e az M1. Menet közben máshol ne állj meg (D19).

### M1 — terv (a jóváhagyás után)

1. **Forrássablon-tervezet:** `sablonok/9_PaRDeS_motivum_forras_sablon.md`. Szakaszonként:
   - kézi vagy adatból generált;
   - mélységi szint;
   - aktiválási feltétel.

   A tematikus szakaszok a ⭐ küszöb (`COUNT(DISTINCT fo_elofordulas)`) alatt inaktívak (D37), ugyanúgy, ahogy ma a 0. és az 1/b szakasz is feltételes. A sablon fejlécében álljon: „tervezet, a #12 pilotja véglegesíti”. A tematikus sablon v16 szabályai (pl. a BDB-jelentés oszlop magyarul) változatlanul átkerülnek. Ha egy szabály nem fér bele, `javaslat` jelölést kap.
2. **Szintjelölés a `adat/SEMA.md`-ben:** új alfejezet.
   - Három szint: `olvasoi`, `apparatus`, `belso`.
   - A jelölés blokkszintű, és gépileg olvasható. A jelölő alakját te javasold, a meglévő `RÉS-KEZDET` / `GENERÁLT-KEZDET` jelölők mintájára.
   - A `【NAPLO】` mindig `belso`.
   - A nyilvános nézet engedélyezőlistával válogat, a `belso` réteget buildkor kihagyja, nem rejti el (D36).
   - Ide kerül a D35 szabálya is: a generált fájlba kézzel nem írunk.
3. **CI-szabályok leírása** a `naplok/MOTIVUM_FORRAS_ci_terv.md`-ben, a következő szabad E-számmal:
   - (a) az újragenerált nézet bájtazonos a commitolttal;
   - (b) a nyilvános kimenetben nulla `belso` jelölés és nulla `【NAPLO` található.

   Csak leírás. Az implementáció külön ágon megy (D6), a #11 előtt.
4. **Pilot-bemenetek** a `naplok/MOTIVUM_FORRAS_pilot_terv.md`-ben (D38):
   - mit kell tudnia a #12-nek (TEREMT-002, natív);
   - mit kell tudnia a #11 1. lépcsőjének (ISTENTISZT-001, örökölt);
   - milyen nulla-diff vagy elfogadott-diff kategóriákkal mérjük a migrációt.

## 4. Munkaszabályok

1. **Csak olvas az M0-ban.** Egyetlen meglévő tartalmi fájl sem változik a menetben. Írni csak a 3. pontban felsorolt új fájlokat és a `adat/SEMA.md` új alfejezetét lehet.
2. **⛔ megállás csak az M0 után**, és ha egy meglévő tartalmi fájl nem szándékolt módosulását észleled.
3. **A számok a futtatott parancsokból jönnek**, eltérésnél a fájl az irányadó. Ahol nincs mérés, ott „nincs mérés” áll, nem becslés.
4. **Motívumszintű `ir`:** ez a feladat egyetlen motívumfájlt sem ír, ezért más feladattal párhuzamosan futhat. Ütközhet viszont minden olyan feladattal, amely a `adat/SEMA.md`-t írja; a sorrendet a `feladatok.py` dönti el.
5. **Zárás a `/kovetkezo` szerint:** `fuggetlen-ellenor`, zárójelentés, draft PR, a saját fejléc frissítése.

## 5. Kész, ha

- K1: az öt M0-kimenet létezik. Minden sorhoz van forrásparancs a naplóban.
- K2: a `DONTESEK.md`-tétel jóvá van hagyva.
- K3: a forrássablon-tervezet minden szakasza kap szintet és aktiválási feltételt; `javaslat` csak jóváhagyott tételként maradhat.
- K4: a SEMA-alfejezet és a CI-terv kész. Nincs `general.py`-módosítás, és nincs tartalmi fájl a diffben (`git diff --stat` a naplóban).
- K5: a `fuggetlen-ellenor` jelentése `TISZTA`.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.09.30 | első változat a chat D34–D39 döntései alapján | a feladat 1. fázisú (metaadat, nincs render); Opus, mert a besorolás szakmai ítélet; a CI-szabályok itt csak leírva, implementálás D6 szerint külön |
