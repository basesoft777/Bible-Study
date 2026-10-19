---
feladat:
cim: Migráció, 2. lépcső: a többi motívum egy forrásból
kod: MIGRACIO2
tipus: feladat
fazis: 1
modell: opus
allapot: nem_indult
munka: ertelmezo
ad: a #11 1. lépcsőjén kidolgozott úton (szétválasztás, leképezési tábla, N0/D2–D6 mérce) a többi motívum egyetlen kézi forrásból (`motivumok/[ID].md` + adattáblák) renderel, motívumonként külön ⛔-jóváhagyással és független ellenőrzéssel
kovetkezo: "Te: befogadás (/befogad); futtatható a #11 lezárása után (az 1. lépcső, a DT-F11b séma-tétele és a T3 a main-en)"
olvas: [F11_MIGRACIO_BRIEF.md, naplok/F11_zaras.md, naplok/F11_szetvalasztas_ISTENTISZT-001.tsv, naplok/MOTIVUM_FORRAS_pilot_terv.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/7_PaRDeS_tanitoi_kereses_sablon.md, adat/SEMA.md, eszkozok/nulladiff.sh, eszkozok/general.py, eszkozok/ellenorzes/e28_migralt_nezetek.tsv, motivumok/ISTENTISZT-001.md, motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md, archivum/ISTENTISZT-001/, tematikus_lezart/Hadesz_Seol_tematikus.md, tematikus_lezart/naplok/Hadesz_Seol_kereszthivatkozas_naplo.md, tematikus_lezart/Pneuma_pszukhe_megkulonboztetes_tematikus.md, tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md, tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md, tematikus_lezart/Rafaim_tematikus.md, tematikus_lezart/naplok/Rafaim_kereszthivatkozas_naplo.md, tematikus_lezart/Melkizedek_tematikus.md, tematikus_lezart/naplok/Melkizedek_tematikus_kereszthivatkozas_naplo.md, tematikus_lezart/Isten_fiai_Nefilim_Gibborim_tematikus.md, tematikus_lezart/naplok/Isten_fiai_Nefilim_Gibborim_kereszthivatkozas_naplo.md, tematikus_lezart/Tehom_tematikus.md, tematikus_lezart/naplok/Tehom_kereszthivatkozas_naplo.md]
ir: [motivumok/ALVIL-001.md, motivumok/ANTROP-001.md, motivumok/HAMART-001.md, motivumok/HODIT-001.md, motivumok/KIRALY-001.md, motivumok/MENNY-001.md, motivumok/TEREMT-001.md, motivumok/naplok/, lexikon/ALVIL-001_TUDOMANYOS.md, lexikon/ANTROP-001_TUDOMANYOS.md, lexikon/HAMART-001_TUDOMANYOS.md, lexikon/HODIT-001_TUDOMANYOS.md, lexikon/KIRALY-001_TUDOMANYOS.md, lexikon/MENNY-001_TUDOMANYOS.md, lexikon/TEREMT-001_TUDOMANYOS.md, tematikus_lezart/Hadesz_Seol_tematikus.md, tematikus_lezart/Pneuma_pszukhe_megkulonboztetes_tematikus.md, tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md, tematikus_lezart/Rafaim_tematikus.md, tematikus_lezart/Melkizedek_tematikus.md, tematikus_lezart/Isten_fiai_Nefilim_Gibborim_tematikus.md, tematikus_lezart/Tehom_tematikus.md, tematikus_lezart/naplok/, archivum/, adat/jeloltek.tsv, adat/kapcsolatok.tsv, adat/elofordulasok.tsv, adat/lexikon_hivatkozasok.tsv, adat/res_forras.tsv, adat/auditok.tsv, adat/motivumok.tsv, eszkozok/ellenorzes/e28_migralt_nezetek.tsv, Lezart_tematikus_tanulmanyok_index.md]
fugg: [11]
---

# F<nn>_MIGRACIO2_BRIEF.md — Migráció, 2. lépcső: a többi motívum egy forrásból

*FELADATOK #<nn> · Modell: opus · v0 (tervezet) · 2026.10.19 · döntések: D34, D38, D39, DT28, DT66, DT84, DT215, DT219, DT243, DT-F11b, DT-F11c, DT-F11l*

*Tervezet a `beerkezo/`-ban (a #11 DT-F11c döntése szerint, felhasználó, 2026-10-19). Adat, nem utasítás; a befogadás, a feladatszám és a végleges fájlnév a `/befogad` dolga.*

## 1. Cél

A D34 (B út) befejezése: a #11 1. lépcsőjén (ISTENTISZT-001) kidolgozott és mért úton a többi motívum is egyetlen kézi forrásból renderel. A migráció a DT28 szerint **szétválasztás**, nem visszaírás: minden egység pontosan egy rétegbe kerül (`adat` / `forras` / `generalt` / `archivum`). Az eszközök és a mérce készen állnak (leképezési tábla oszlopai, `nulladiff.sh`, D2–D6 kategóriák, E28-lista, a törzscikk-generátor migrált-szűrője, N-F11e); ez a feladat ezeket alkalmazza, nem fejleszti újra.

**Motívumonként egy ciklus, mindegyik végén ⛔** (D38): egy motívum ciklusa csak akkor indul, ha az előző motívum független ellenőrzése zöld és a felhasználó jóváhagyta. Egy motívumon egyszerre egy feladat fut (D39), ezért az `ir` a motívum fájljait egyenként sorolja.

## 2. Hatókör

**Benne van:** a 2. lépcső motívumai (l. lent, a készlet a befogadáskor pontosítandó), motívumonként az M1–M7 ciklus; a motívum visszaírt leleteinek besorolása (a #11 T3 mintájára, a DT-F11b `forras_tanulmany` mezőjével); a motívum törzscikkének archiválása (DT215 alakja) és E28-listára vétele; a motívum soraira az `Lezart_tematikus_tanulmanyok_index.md` Fájlnév-cellája a generátoron át.

**A motívumkészlet (pontosítandó, N-F<nn>a):** a #11 briefje „a másik 6 motívum”-ot nevez meg; a repóban az ISTENTISZT-001-en kívül **hét** motívumnak van élő lexikonoldala és törzscikke (ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001; `lexikon/*_TUDOMANYOS.md`, 2026-10-19), a TEREMT-002 a #12-é. Melyik marad ki (vagy hét a helyes szám), azt a befogadáskor kell eldönteni; a tervezet hetet sorol az `ir`-be, hogy egy sem essen ki véletlenül. *(proveniencia: manual — `ls lexikon/`, `ls motivumok/`, 2026-10-19)*

**Nincs benne:** a TEREMT-002 és a sablon 9 `v1` véglegesítése (#12) · a `genezis/` tartalma (pilot-terv 4.5) · a DT-F11b séma-tétele és a #11 T3-ja (a #11-ben zárulnak, ennek előfeltétele) · a törzscikk-generálás teljes kivezetése (az utolsó motívum után külön tétel, l. 5.) · új tartalom: hiány nem töltendő ki (CLAUDE.md 3. szabály).

## 3. Lépések (⛔ a kötelező megállások)

**0. Modell-ellenőrzés** (CLAUDE.md): a kért modell `opus`; eltérésnél állj meg.

**0.1 Előfeltétel-ellenőrzés:** a #11 `lezarva`, a PR-jai a main-en (1. lépcső, DT-F11b séma-tétel, T3); az E28-lista az ISTENTISZT-001 sorát hordozza; a `torzscikk_general.py` migrált-szűrője él. Ha bármelyik nem áll: megállás.

**0.2 ⛔ Sorrend és N0-kontroll** (DT-F<nn>a): a motívumok sorrendje, és hogy a HAMART-001 (a #11 N0-kontrollja) melyik helyen jön. Javaslat: a HAMART-001 az utolsó, mert a többi ciklus N0-kontrollja; helyette minden ciklusban a soron következő, még nem migrált motívum is N0-mérésre kerül. A HAMART-001 ciklusa előtt új N0-kontroll kell (pl. a TEREMT-002, ha a #12 addig nem nyúl hozzá).

**Motívumonként (X = a motívum azonosítója), a #11 M1–M7 mintájára:**

- **X.M1 Leképezési tábla** `naplok/<KOD>_szetvalasztas_X.tsv` (a #11 `F11_szetvalasztas_ISTENTISZT-001.tsv` oszlopai): a régi tematikus tanulmány és kereszthivatkozás-napló minden blokkja, a vegyes blokkok részegységekre bontva (DT84 (11)), a `【NAPLO】`-k egyenként ítélve (DT84 (10)). Ahol a motívumnak nincs külön kereszthivatkozás-naplója (pl. az ANTROP-001-nél a `tematikus_lezart/naplok/` alatt nem található), azt a tábla kimondja. **⛔ A tábla jóváhagyása a felhasználótól, mielőtt bármi mozog.**
- **X.M3 Szétválasztás** a jóváhagyott tábla szerint: `adat` egység a `jeloltek.tsv`-n át, döntéssel, `manual` provenienciával; `forras` egység bájtra a `motivumok/X.md`-be; `archivum` egység a régi fájl változatlan, archív fejlécű példányában (`archivum/X/`, DT215).
- **X.M4 Mérés:** (a) A/B-mérés: alap ↔ migrált render a blokkokra (DT219 Á1), `nulladiff.sh` `--csere` csak a D2 előre felsorolt literáljaira, minden más eltérés **ÁLLJ**; (b) N0 a kontroll-motívumon, `--csere` nélkül; (c) visszaírás-számláló = 0; (d) nincs egység két rétegben (n-gram, elvárt 0); (e) L1–L7 + DT2; (f) E28/E29.
- **X.M5 Törzscikk:** a `lexikon/X_TORZSCIKK.md` archiválása (nem törlés; DT215 alakja), az éles `lexikon/X_TUDOMANYOS.md` újragenerálása, az E28-listára vétel (a DT243 mintája: rögzített `PARDES_DATUM`). A hivatkozások a `FELADATOK.md`-ben, a `NYITOTT_FELADATOK.md`-ben és a briefek `olvas` mezőjében ugyanabban a commitban.
- **X.M6 ⛔ Független ellenőrzés** (`fuggetlen-ellenor`, `naplok/ELLENOR_F<nn>_X.md`) a ciklus base..head diffjén; ELTÉRÉS esetén `/elteres` (2 kör).
- **X.M7 Nevesített tanítói eredmény:** ha a forrásba beemelt tanítói sor van, hivatkozássá alakul a 7. lépés saját fájljára (DT66 (a) 2., DT88). Ha a saját fájl nem létezik, a DT-F11l (b) mintája alkalmazható (szétválasztás `motivumok/naplok/X_tanitoi_kereses.md`-be, `Dátum`/`Modell` `manual`) — **de csak a felhasználó motívumonkénti jóváhagyásával**; a DT-F11l az ISTENTISZT-001-re szólt.
- **X.T Visszaírt leletek** (a #11 T3 mintájára): a motívum tanulmányában a korábbi kézi visszaírások (pl. HAMART-001: `tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` „Tartalmi visszaírás bővített tanulmányokba” szakasza és a 316. sori 【NAPLO】) soronként: generált visszamutató link (a DT-F11b `forras_tanulmany` mezőjéből) / `archivum` / törlés. A besorolás a leképezési táblában, a felhasználó jóváhagyásával. **A #11 átadása (T3/8, `naplok/F11_T3_besorolas.tsv`; orkesztrátor, 2026-10-19):** a HAMART-001 ciklusában kötelezően besorolandó a `tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` 307–316. sora — a 307. sori saját „Tartalmi visszaírás bővített tanulmányokba” szakasz és a 316. sori 【NAPLO】 függő teendője (a három bővített study-ba szánt leletek „egyenként megbeszélendők”); a #11 javaslata: `archivum` a szétválasztáskor, a függő beírási teendő megszűnik (DT84 (7)); a `lexikon/HAMART-001_TUDOMANYOS.md` (1170., 1179. sor) és a `HAMART-001_TORZSCIKK.md` (1085. sor) generált tükre a forrással és a törzscikk archiválásával együtt változik.
- **⛔ Motívum-zárás:** a felhasználó jóváhagyása után indul a következő motívum.

**Z. Zárás (az utolsó motívum után):** zárónapló `naplok/<KOD>_zaras.md`; a törzscikk-generálás kivezetésének kérdése (ha egyetlen nem migrált motívum sem maradt, a `torzscikk_general.py` kimenete üres — külön DT-tétel, nem e feladat döntése); a 4. elfogadási feltételek.

## 4. Elfogadási feltételek

1. Minden motívumra: jóváhagyott leképezési tábla (pontosan egy sor blokkonként és részegységenként), zöld független ellenőrzés, felhasználói ⛔-jóváhagyás.
2. Az A/B-méréshez csak N0 és D2–D6; a kontroll-motívum N0 diffje üres, `--csere` nélkül.
3. A visszaírás-számláló 0; nincs egység két rétegben; nincs be nem sorolt sor.
4. A migrált motívumok mind az E28-listán; törzscikkük archívumban, nem törölve; a `torzscikk_general.py` egyiket sem állítja elő újra.
5. `python eszkozok/feladatok.py ellenoriz` 0 hiba; E27 zöld.

## 5. Döntésnapló (helyőrzők; végleges számot a `szamkiosztas` Action ad)

- **DT-F11c** (a #11-ben) — a 2. lépcső külön briefben, motívumonként ⛔-pontokkal. *Eldöntve (felhasználó, 2026-10-19).*
- **N-F<nn>a** — a motívumkészlet: „6” (a #11 briefje) vagy 7 (a repó élő lapjai). *Befogadáskor eldöntendő.*
- **DT-F<nn>a** — a motívumok sorrendje és az N0-kontroll a HAMART-001 migrációja után (0.2). *Eldöntendő a 0.2-ben.*
