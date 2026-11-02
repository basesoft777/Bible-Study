# Az 1/a igehelyenkénti prózájának hiánya — mérés, ok, kapu (2026-11-02)

*Megbízás: az orkesztrátor (`local_20eed447-…`), a felhasználó 2026-11-02-i jelzése nyomán, szó szerint (rövidítve): „volt kerek proza, amiket most csinálunk nincs vagy töredékek”; „mindig volt próza — ez most elmaradt — ez súlyos hiba”. Mérce: az arany lap (ISTENTISZT-001), 1Móz 4:26. Modell: `claude-opus-5-5`. A próza megírása nem része ennek a menetnek (⛔, K1).*

## 1. Mérés

Mérő: `python eszkozok/proza_1a.py --reszletes` (a generált lapot méri, nem az adatot; `scope=lexikon/*_TUDOMANYOS.md 1/a | forras=eszkozok/proza_1a.py | ts=2026-11-02`).

Szabály: igehelyenként (a) **próza** — a Károli-szöveg alatti sor(ok); *töredék*, ha az idézőjeles és zárójeles betéten, valamint a héber/görög szón kívül 7-nél kevesebb magyar szó áll benne (az arany lap legrövidebb kerek prózája, az ApCsel 22:16, pontosan 7); (b) **„Funkció:” sor** — *töredék*, ha 3-nál kevesebb szó. Arany szintű az igehely, ha mindkettő megvan.

| motívum | igehely | próza kerek | töredék | hiányzik | Funkció van | töredék | hiányzik | arany szint |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ALVIL-001 | 72 | 8 | 64 | 0 | 0 | 0 | 72 | 0 |
| ANTROP-001 | 8 | 7 | 1 | 0 | 0 | 0 | 8 | 0 |
| HAMART-001 | 52 | 43 | 9 | 0 | 0 | 0 | 52 | 0 |
| HODIT-001 | 33 | 4 | 29 | 0 | 0 | 0 | 33 | 0 |
| ISTENTISZT-001 | 22 | 22 | 0 | 0 | 18 | 0 | 4 | 18 |
| KIRALY-001 | 9 | 7 | 2 | 0 | 1 | 0 | 8 | 1 |
| MENNY-001 | 9 | 6 | 3 | 0 | 0 | 0 | 9 | 0 |
| TEREMT-001 | 41 | 7 | 34 | 0 | 0 | 0 | 41 | 0 |
| TEREMT-002 | 3 | 2 | 1 | 0 | 0 | 0 | 3 | 0 |
| **összesen** | **249** | **106** | **143** | **0** | **19** | **0** | **230** | **19** |

**Lelet:** a 249 igehelyből 19 arany szintű (18 az ISTENTISZT-001-en, 1 a KIRALY-001-en). A „Funkció:” sor a többi hét motívum egyetlen igehelyén sincs ott; a próza 143 helyen töredék. Hiányzó próza (üres sor) nincs: minden helyen áll valami, csak a nagyobb része címke vagy idézet-foszlány. A felhasználó által idézett mind a nyolc ALVIL-001-hely (1Móz 37:35, 42:38, 44:29, 4Móz 16:33, 5Móz 32:22, 1Sám 2:6, 2Sám 22:6, 1Kir 2:6) töredéknek mérődik, és az 1Kir 2:9 („ua. — Simei”) is (teszt: `eszkozok/teszt_proza_1a.py`).

*A határeset:* a mérő szószámot mér, nem mondattant. A „élve alászállás a Seolba — Kóré lázadása, csodás ítélet” (4Móz 16:30) kereknek mérődik, mert 8 szó; mondatnak az arany lap 1Móz 12:8-a sem teljesebb („Ábrám, Bétel-Ai között — oltárépítés + segítségül hívás első összekapcsolása.”). A kerek próza tehát a mérő szerint *alsó korlát*, nem minőségi ítélet.

### Honnan generálódik

`eszkozok/lexikon_general.py` (1/a-blokk, a `tetelek_1a` ciklus): igehelyenként a Károli-szöveg, utána **az `adat/elofordulasok.tsv` `kapcsolodas` mezője** (változatlanul), majd `Funkció: <x>`, ahol `x` **a `funkcio` mező „ — ” utáni része**. Ha a `funkcio` üres, vagy nincs benne „ — ”, a „Funkció:” sor elmarad (a teljes érték csak a fenti táblázat „Funkció (a motívumban)” oszlopába kerül, a „ — ” előtti címkével). A `motivumok/[ID].md` kézi prózája nem kerül az 1/a-ba.

A `funkcio` mező állapota az adatban:

| motívum | `funkcio` üres | csak címke (nincs „ — ”) | címke — magyarázat |
|---|---:|---:|---:|
| ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, MENNY-001, TEREMT-001 | mind (216) | 0 | 0 |
| ISTENTISZT-001 | 0 | 4 | 18 |
| KIRALY-001 | 0 | 8 | 1 |
| TEREMT-002 | 0 | 3 (`címke: magyarázat`, kettősponttal) | 0 |

## 2. Ok — a teljes lánc

**Igehelyenkénti kerek próza ezeknél a helyeknél sosem volt; az adatrétegben semmi nem veszett el.**

1. **Az adattábla története** (`git log -- adat/elofordulasok.tsv`, minden commit motívumonkénti mérése): a `kapcsolodas` átlagos hossza a betöltés óta lényegében állandó (ALVIL-001: 39 karakter az F3.2-ben, 2026-09-14, és ma is 40; TEREMT-001: 66 → 72; HODIT-001: 44 → 53); a `funkcio` a hat motívumon az első betöltés óta üres. Egyetlen commit sem rövidítette a mezőt, és egyik sem ürítette a `funkcio`-t. A CSV-idézőjel-csapda (CLAUDE.md „TSV-olvasás”) itt nem okozott kárt: az idézőjelek a mezőben épek (pl. 1Móz 37:35).
2. **A betöltés forrása:** a sorok a tematikus tanulmányok táblázatából jöttek (F3.1/F3.2, N14.2, T2.2 — retroaktív betöltés). Az ISTENTISZT-001 forrás-tanulmánya (`Segitsegul_hivni_az_Urat_tematikus.md`) táblázatában igehelyenként külön leírás és külön funkció-oszlop állt („🌱 alap-előfordulás — …”); ezért lett arany lap. A többi tanulmány táblázata csak egy rövid megjegyzés-oszlopot adott, funkció nélkül — ezt vette át a `kapcsolodas`.
3. **Ahol volt próza, és hova lett:** az ALVIL-001 és a TEREMT-001 tanulmányában a táblázat előtt **csoportos próza** állt (a 2/b. „Kiterjesztés”: egy-egy bekezdés néhány igehely csoportjáról, pl. „Személyes gyász … 1Móz 37:35; 42:38; 44:29,31 — mind ugyanaz a formula, apai gyász József/Benjámin miatt.”). A `5efba149` commit (2026-09-10, „Hadesz_Seol + Tehom: »2/b« prózai kiterjesztések táblázatra alakítva (sablon-megfelelőség)”) ezeket igehelyenkénti táblázatsorokra bontotta: a csoportmondat az első sorba került rövidítve, a többi sor „ua. — …” lett. Innen jön a „Benjámin miatti félelem”, a „Júda közbenjárása” és a „ua. — Simei”. A teljes csoportos szöveg a `git show 5efba149^:tematikus_lezart/Hadesz_Seol_tematikus.md` és `…Tehom_tematikus.md` alatt olvasható; a régi törzscikk (`archivum/ALVIL-001/ALVIL-001_torzscikk_regi.md`) már ugyanazokat a töredékeket mutatta.
4. **HODIT-001:** a `Rafaim_tematikus.md` tartomány-sorait (pl. „5Móz 2:10-11”) a betöltés versenként bontotta; a második vers „ua. — folytatás” lett (16 „ua.” sor).
5. **A generátor:** a „ — ” nélküli `funkcio` nem kerül az 1/a-ba. Ez a TEREMT-002 mindhárom helyén (`prototípus: a föld teremtés előtti, rendezetlen állapota …`) kerek funkció-mondatot rejt el, a KIRALY-001 8 és az ISTENTISZT-001 4 helyén címkét.
6. **Miért nem vette észre senki:** a Feed 6. kapuja az olvasói blokkok bevezetőjét, a kiejtést és a fordítást méri; a `ellenoriz.py` 23. szabálya a `motivumok/[ID].md` kézi prózáját; igehelyenkénti mérés nem volt. A felhasználói élmény („mindig volt próza”) az arany lapból jön, amelynek forrása eleve más szerkezetű volt.

## 3. Gépi kapu

- `eszkozok/proza_1a.py` — a mérő (modul + parancssor).
- `eszkozok/ellenoriz.py` **24. szabály** („Az 1/a igehelyenkénti prózája (arany lap)”) — ma **JELENTÉS**, nem gátol; motívumonként: hány igehely nem arany szintű, ebből próza töredék/hiányzik, Funkció töredék/hiányzik. Mostani kimenet: JELENTÉS, 9 motívum, 230 igehely.
- `eszkozok/teszt_proza_1a.py` — 10 teszt (arany lap kerek; a felhasználó kilenc töredéke; héber/zárójel nem számít; HTML-megjegyzés nem próza; az 1/a határa; a 24. szabály RENDBEN/JELENTÉS/KÉZI).
- **A Feed (`muhely_allapot.py`) nem változott.** A beemelés a 6. kapuba (és ezzel a szint) döntés: **DT-F1Aa**.

## 4. Motívumonként: mi állítható vissza gépileg, mennyi új próza kell

„Új próza” = a 7 szónál rövidebb `kapcsolodas` kiegészítése, „új Funkció” = a hiányzó funkció-mondat. Egyik sem írható gépileg: igehelyenkénti értelmező próza (K1, egy kéz, Opus).

| motívum | gépileg visszaállítható | új próza | új Funkció | anyag a próza-menethez |
|---|---|---:|---:|---|
| ALVIL-001 | — (igehelyenkénti próza sosem volt) | 64 | 72 | a csoportos 2/b-próza: `5efba149^:tematikus_lezart/Hadesz_Seol_tematikus.md` (8 csoport + Hós 13:14) |
| TEREMT-001 | — | 34 | 41 | `5efba149^:tematikus_lezart/Tehom_tematikus.md` 2/b; *mellékesen: a Jób 41:32 adatsor a lap 1/a-jából hiányzik* |
| HODIT-001 | — (16 „ua.” sor a tartomány-sor első verséből örökölhet, de az olvasónak az is ismétlés) | 29 | 33 | `tematikus_lezart/Rafaim_tematikus.md` táblázata |
| HAMART-001 | — | 9 | 52 | `Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` |
| MENNY-001 | — | 3 | 9 | `Isten_fiai_Nefilim_Gibborim_tematikus.md` |
| ANTROP-001 | — | 1 | 8 | `Pneuma_pszukhe_megkulonboztetes_tematikus.md` |
| KIRALY-001 | **8 Funkció-sor** a meglévő címkéből (DT-F1Ab) — 6 mérődne „van”-nak, 2 töredék („krisztológiai betöltés”) | 2 | 8 (a címkék kiegészítése) | `Melkizedek_tematikus.md` |
| ISTENTISZT-001 | **4 Funkció-sor** a meglévő címkéből (DT-F1Ab), pl. „ismétlődés, személyes könyörgésben” | 0 | 4 (ha a címke nem elég) | — |
| TEREMT-002 | **3 kerek Funkció-sor** (DT-F1Ab) | 1 (Jer 4:23) | 0 | — |
| **összesen** | **15 Funkció-sor** (ebből 3 kerek mondat) | **143** | **227** | |

## 5. Döntések (⛔)

- **DT-F1Aa** — a 24. szabály szintje és a Feed. Javaslat: **(b)**, l. `DONTESEK.md`.
- **DT-F1Ab** — a generátor a „ — ” nélküli `funkcio`-t is írja ki az 1/a-ban. Javaslat: **(a)**, l. `DONTESEK.md`.
- Az új próza menete: **N-F1Aa** (`NYITOTT_FELADATOK.md`).
