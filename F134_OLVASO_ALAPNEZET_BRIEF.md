---
feladat: 134
cim: Olvasófelület — a Károli-szöveg az alapnézet, a szó és a vers részletei egyetlen lapon (kis képernyőn alsó lap, nagyon oldalblokk)
kod: OLVASO_ALAPNEZET
tipus: feladat
fazis: 1
modell: opus
allapot: fut
ag: claude/olvaso-alapnezet
ad: az olvasó-szerver a mockup 9. változata szerint működik — kis képernyőn csak a Károli-szöveg, a navigáció és a részletek felugró lapon; nagy képernyőn állandó oldalblokk, kijelölés nélkül rövid útmutatóval (DT-F134l); világos alaptéma; mérve 375/768/1280 px-en és valódi telefonon
kovetkezo: "Folytatás: M3 (arculat) — az M2 kész (naplok/OLVASO_ALAPNEZET_M2.md)"
munka: folyamat
olvas: [F76_OLVASOI_KONKORDANCIA_BRIEF.md, F98_TERVEZO_MOD_BRIEF.md, naplok/OLVASOI_KONKORDANCIA_pilot_osszevetes.md, naplok/OLVASOI_KONKORDANCIA_meres.md, naplok/TERVEZO_MOD_zaras.md]
ir: [eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/statikus/, eszkozok/olvaso_szerver/konfig/arculat.json, eszkozok/olvaso_szerver/konfig/elemek.toml, eszkozok/olvaso_szerver/arculat.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_szerver/teszt_arculat.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/regiszter_or.py, eszkozok/olvaso_szerver/export.py, eszkozok/olvaso_szerver/konfig/szerver.toml, eszkozok/olvaso_szerver/teszt_tervezo.py, eszkozok/olvaso_szerver/teszt_pilot_aranymintaval.py, eszkozok/olvaso_szerver/teszt_kereses.py, eszkozok/olvaso_szerver/teszt_indito.py, eszkozok/olvaso_szerver/m4_meres.py, eszkozok/olvaso_szerver/README.md, "naplok/OLVASO_ALAPNEZET_*.md"]
fugg: [76]
---

# F134_OLVASO_ALAPNEZET_BRIEF.md — Olvasófelület: a Károli-szöveg az alapnézet

*FELADATOK #134 · Modell: opus · v1 · 2026.10.22*

## 1. Cél

Az olvasó-szerver (`eszkozok/olvaso_szerver/`) elrendezése a felhasználó 2026-10-22-i döntései (DT292–e) és a jóváhagyott, telefonon kipróbált mockup szerint:

- **Minta (vizuális mérce):** a mockup 9. változata, „Csak szöveg olvasó” — https://claude.ai/artifact/ExAeE1TKsNfuEMutErqsuA. Az Alap mockup és a többi változat: https://claude.ai/artifact/Scybm5aoGkc7N4Q3EYgm3r (a változat-sáv linkjeivel). A mockupot a menet csak olvassa (Artifact `read`); a mockup-kereteket nem írja át, a stílusukat és elemeiket viszi át a szerverre.
- **Elv:** az alapnézet a Károli-szöveg, és semmi más. Minden más (navigáció, jelölések, forrás, vers- és szórészletek) erre épülő réteg; kis képernyőn csak felugró elemként jelenik meg.

## 2. Hatókör

**Benne van**

1. **Kis képernyő (900 px alatt):** nincs tartós fejléc és alsó sáv. A navigáció (kereső, könyvválasztó, ‹ ›, Aa, ⚙, kánon-sáv, jelölő chipek, „Legutóbb”; a Fejezet-kalauz gomb a DT-F134l szerint kimarad) a fejezetcímre koppintva felugró lapon nyílik; felfelé görgetésre egy átmeneti tájoló pirula („Ez 37 ▾”) is előhívja.
2. **A részletek lapja — egy komponens, két mód:** versszámra koppintva versmód (fejsor: igehely + a vers eleje; a „Másolás forrással” gomb a DT-F134m szerint nem kerül be; fülek: Vers · Kereszthiv. · Témák · Motívum), szóra koppintva szómód (fejsor: Strong-szám, héber/görög alak, alapjelentés; „A vers: … →”). Váltás a két mód között bezárás nélkül; ‹ az előző tartalomra lép (előzménylánc).
3. **Két alak:** 900 px alatt alulról felugró lap (betekintés kb. a képernyő felééig, felhúzva teljes nézet, lehúzásra vissza, majd zárás; a koppintott vers a lap fölött látható marad); 900 px-től állandó, párhuzamos oldalblokk.
4. **Üres állapot (DT-F134l):** kijelölés nélkül az oldalblokk rövid útmutatót mutat (koppints versszámra a vers, szóra a szó részleteiért), alatta a fejezet forrását és a számlálókat. A fejezet-kalauz (a mockup 5. változata) kimarad; később külön feladat lehet.
5. **Téma:** az alapértelmezett a világos; a sötét a ⚙ menüben választható marad (a Rendszer lehetőség a DT295 szerint).
6. **Arculat:** a színtokenek és a betűk már azonosak a mockupéval (mérve 2026-10-22); új: a kánon-sáv műfajszínei (`--g-tor` … `--g-apok`, világos és sötét érték) az `konfig/arculat.json`-ba; a mockup komponensstílusai (egysoros fejléc nagy képernyőn, 32 px-es ikongombok, pirula-chipek, árnyékos felugró elemek, fülsor) a tokenrendszeren át.
7. **Nézetek helyett rétegek (DT294):** a nézetváltó kikerül; az interlineáris sor az olvasóra kapcsolható réteg. A munkaasztalból nem marad réteg, verslista nincs (DT-F134g). Az állapot és a régi linkek: DT-F134f (a terv: `naplok/OLVASO_ALAPNEZET_M0.md` 4. szakasz).
9. **Kereső (DT-F134k):** a meglévő űrlap a mockup stílusában, kliensoldali javaslattal a könyvnevekre és az igehely-mintára, új végpont nélkül.
8. **Mérés:** a 6. szakasz kiinduló mérésének megismétlése az új állapotra (375 / 768 / 920 / 1280 px), valamint valódi telefonos próba a belső hálón (a portproxy- és tűzfal-lépéseket a felhasználó végzi).

**Nincs benne**

- Új adat, új blokk, a blokkok tartalmának módosítása.
- A fejezet-kalauz és a „Másolás forrással” gomb (DT-F134l, DT-F134m).
- A mockup többi változatának (1–4, 6–8) újdonságai, kivéve amit a 9. változat átvett.
- Nyilvános telepítés. A statikus export az új elrendezést kapja ugyanabból a sablonból, a mai viselkedése teszttel őrizve (DT-F134h).
- A Tervező mód (#98) működésének átírása; a Tervező kapcsoló a ⚙ menübe kerül, csak a belső kiadásban.

## 3. Lépések (⛔ a kötelező megállások)

- **M0 — előkészítés ⛔.** A #76 zárásának ellenőrzése a main-en (a `fugg` miatt); a 9. változat és az Alap mockup olvasása (Artifact `read`); a DT294 alkalmazási terve (mi marad a `nezet` sütiből, a `/nezet/<nev>` útvonalból, a DT148 elrendezéseiből). Megállás: terv a felhasználónak.
- **M1 — vázszerkezet.** A részletek-lap komponense (szerveroldalon a meglévő `/r/szo` és `/r/vers` töredékekre építve), a két alak CSS-e és JS-e, a fejsor, az előzménylánc; az üres állapot útmutatója (DT-F134l).
- **M2 — kis képernyő.** Fejléc nélküli olvasó, navigációs lap, tájoló pirula, húzás; a versműveletek a lap fejsorában.
- **M3 — arculat.** Világos alaptéma; `--g-*` tokenek; komponensstílusok. A Tervező mód és az `arculat.json` őrei (#98) zöldek maradnak.
- **M4 — mérés ⛔.** A 6. szakasz táblázatának megismétlése (szkripttel, böngészőben) és képernyőképek a három szélességen, vizuálisan a 9. változathoz mérve; valódi telefon. Megállás: mérési jelentés.
- **M5 — tesztek és zárás.** `python eszkozok/teszt_futtat.py` (WSL-natív `pardes.db`), független ellenőr, zárójelentés.

## 4. Elfogadási feltételek

- **E1** 375 px-en az első vers a fejezetcím alatt kezdődik (mérve: ≤ 200 px a lap tetejétől); nincs tartós sáv; vízszintes túlfolyás 0 minden mért oldalon.
- **E2** Versszámra és szóra koppintva a lap 375 és 768 px-en látható helyen nyílik (a mai állapotban 3 874 / 34 277 px-rel a szöveg alatt); a koppintott vers a betekintő lap fölött látszik.
- **E3** 900 px-től az oldalblokk állandó; kijelölés nélkül a rövid útmutatót, a fejezet forrását és a számlálókat mutatja (DT-F134l).
- **E4** Szó- és versmód között bezárás nélkül lehet váltani, a ‹ az előzőre lép.
- **E5** Alapértelmezett téma: világos; a Rendszer / Világos / Sötét választható, és a választás megmarad (a böngésző helyi tárolójában, DT-F134i).
- **E6** A meglévő tesztek zöldek; a #98 Tervező mód és a hozzáférési szintek (DT129) működése változatlan.
- **E7** A 6. szakasz minden „törik” sora javult, vagy a jelentés indokolja, miért nem.

## 5. Döntésnapló

- **DT292** 🟢 — az alapnézet a Károli-szöveg; kis képernyőn minden más felugró, tartós sáv nélkül (felhasználó, 2026-10-22).
- **DT293** 🟢 — a részletek egyetlen komponensben, szó- és versmóddal; 900 px alatt alsó lap, fölötte állandó oldalblokk; üres állapotban fejezet-kalauz (felhasználó, 2026-10-22; a 9. változat jóváhagyásával, telefonon kipróbálva).
- **DT294** 🟢 — nézetek helyett rétegek: a nézetváltó kikerül; a DT129 (4) „három váltható nézet” és a DT148 ennyiben módosul (felhasználó, 2026-10-22).
- **DT295** 🟢 — az alapértelmezett téma a világos, a sötét választható marad (felhasználó, 2026-10-22).
- **DT296** 🟢 — a szerver új stílusa a mockup világos színsémája és betűkészlete; a `--g-*` műfajszínek az `arculat.json`-ba; a komponensstílusok a mockupból (felhasználó, 2026-10-22).
- **DT-F134f** 🟢 — (b) egyetlen réteg (`il`), `pardes_reteg` süti csak kapcsoláskor, `?reteg=` felülírja; a régi `?nezet=` álnév, a `/nezet/<nev>` 302 (felhasználó, 2026-10-22, M0).
- **DT-F134g** 🟢 — (c) nincs verslista; a munkaasztalból nem marad réteg (felhasználó, 2026-10-22, M0).
- **DT-F134h** 🟢 — (a) a statikus export az új elrendezéssel, ugyanabból a sablonból (felhasználó, 2026-10-22, M0).
- **DT-F134i** 🟢 — (a) a téma a böngésző helyi tárolójában; Rendszer / Világos / Sötét, alap Világos (felhasználó, 2026-10-22, M0).
- **DT-F134j** 🟢 — (a) az `ir` bővül (a `lekerdezesek.py` nélkül) (felhasználó, 2026-10-22, M0).
- **DT-F134k** 🟢 — (b) kliensoldali javaslat könyvnévre és igehelyre (felhasználó, 2026-10-22, M0).
- **DT-F134l** 🟢 — (a) üres állapotban rövid útmutató; a fejezet-kalauz kimarad; a DT293 és az E3 ennyiben módosul (felhasználó, 2026-10-22, M0).
- **DT-F134m** 🟢 — (c) nincs „Másolás forrással” gomb (felhasználó, 2026-10-22, M0).

A tételek teljes szövege a `DONTESEK.md`-ben.

## 6. Kiinduló mérés (2026-10-22, a befogadó session mérése)

*Módszer: a böngészőpanel emulált szélességén, mérőszkripttel (`getBoundingClientRect`, `scrollWidth`) és képernyőképpel; a szerver a WSL-ben, `belso` kiadás, `kutato` szint; oldal: 1Móz 1:3 nyitott szópanellel (H0216). Proveniencia: `scope=olvaso_szerver 127.0.0.1:8765 | forras=bongeszo-meres | ts=2026-10-22`.*

| Lelet | 375 px | 768 px | 1280 px |
|---|---|---|---|
| A szópanel teteje, Olvasópult | 3 874 px | 2 727 px | 284 px (mellette) |
| Ugyanez, Interlineáris | 34 277 px | 22 281 px | 284 px |
| Görgetődoboz a görgetett oldalon (panel 794–1006 px, benne `.gordul` 340 px) | igen | igen | ragadós, működik |
| Az első vers kezdete (Olvasópult / Munkaasztal) | 640 / 1 385 px | 495 / 1 307 px | 454 / 468 px |
| A fejléc magassága | 210 px | 132 px | 91 px |
| A munkaasztal verslistája | 732 px magas, teljes szélesség | 800 px | 180 px-es oszlop |
| A szólap vízszintes túlfolyása (`table.adat`, 484 px) | 109 px | nincs | nincs |
| A panel táblái kilógnak (`table.adat` 400–503 px) | igen | nem | nem |
| 24 px-nél kisebb érintési cél (Olvasópult) | 45 / 323 | 56 / 429 | — |

920 px-en a munkaasztal háromoszlopos (180 + 300 + 361 px; a szöveg 300 px), 899 px-en egyoszlopos: egyetlen lépcső. Az Alap mockup ugyanitt: 375 px-en az első vers 327 px-nél, a ragadós fejléc 159 px, a panel 4 750 px-nél (35 569 px magas, kinyitva), a versszámra koppintás látható hatás nélkül; a 9. változat ezt oldja meg.
