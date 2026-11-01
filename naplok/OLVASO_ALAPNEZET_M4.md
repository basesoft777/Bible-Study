# OLVASO_ALAPNEZET — M4: mérés (#134) ⛔

*Végrehajtói mérés (`claude-opus-5-5`), nem független ellenőrzés. Ág: `claude/olvaso-alapnezet`, a main beolvasztása után (`9e7e0f98`, F134.15). A brief M4 lépése: a 6. szakasz táblázatának megismétlése, képernyőképek, vizuális összevetés; a felhasználó kérésére a #60 pilothoz is, blokkonként.*

Proveniencia: `scope=olvaso_szerver 127.0.0.1:8799 @9e7e0f98 (belso kiadás, kutato szint, sablon_verzio f134-m3l; WSL pardes, PARDES_DB=~/pardes/pardes.db, epites_ts 2026-10-14T09:35:00Z) + #60 pilot (eszkozok/olvaso_pilot adat.py + epit.py --szakasz "1Móz 1:1-2:3", ezen az ágon építve, a repón kívül) + mockup 9. változat (Artifact ExAeE1TKsNfuEMutErqsuA, verzió 1792660119-3840, Artifact read, helyben renderelve) | forras=bongeszo-meres (headless Chrome, DevTools-protokoll; naplok/OLVASO_ALAPNEZET_M4/m4_bongeszo_meres.py) | ts=2026-11-01`

## 0. Összefoglaló

- **A 6. szakasz minden „törik” sora javult, kettő kivétellel** (E7): a részletek lapja 375 és 768 px-en a képernyő felénél nyílik (422 / 532 px; a kiinduló állapot 3 874 / 34 277 px), az első vers 146 px-nél kezdődik (640 px volt), az oldal vízszintes túlfolyása mindenhol 0. **Nem javult:** (1) a lapon belül a széles táblák kilógnak (375 px-en 118 px, a 920 px-es oldalblokkban 93–123 px; a lap vízszintesen görget, a jobb oszlop levágva látszik); (2) szómódban a lap maga görget, benne két 340 px-es `.gordul` doboz (görgetés a görgetésben). Mindkettő ugyanígy áll a 9. változatban is (a mockup a szerver blokkjait mutatja). Döntés: DT-F134p, DT-F134q (6. szakasz).
- **A 9. változathoz mérve** a geometria szinte azonos: a lap teteje 375 px-en 422 / 422 px, 768 px-en 532 / 532 px; az oldalblokk 920 px-en 400 / 400 px, 1280 px-en 584 / 578 px széles. A szándékos eltérések (DT-F134l, -m, -n, -o) a képeken látszanak, új eltérés három (5. szakasz).
- **A #60 pilothoz mérve** a szerkezeti különbség a lényeg: a pilot 900 px alatt a teljes részletek-panelt a szöveg alá teszi (375 px-en 5 047 px-nél), kattintásra odagörget, és a kattintott vers eltűnik a képről; a szerveren a lap a vers alatt nyílik, a vers látható marad. Valódi telefonon a pilot asztali elrendezésben, kicsinyítve jelenik meg (nincs `viewport` meta), a szerver a saját mobil elrendezésével. Blokkonként: 4. szakasz.
- **Tesztek:** a beolvasztás után 8 piros teszt, mind a main-en is piros ugyanazzal az adatbázissal (7. szakasz) — a beolvasztásból nem ered hiba, javítás nem kellett.
- **Nem futott:** a valódi telefonos próba (a felhasználóé, lépések: 8. szakasz); a téma (E5) és a szó↔vers váltás (E4) újramérése (az M1–M3 mérte, a kód azóta csak a beolvasztással változott).

## 1. Módszer

- **Szerver:** `alkalmazas.py --port 8799 --kiadas belso` a WSL `pardes` disztribúcióban, a munkafa kódjával, `PARDES_DB=~/pardes/pardes.db` (WSL-natív; `epites_ts` 2026-10-14). Előbb `/szint/kutato` (süti), mint a 6. szakasz mérésében. A felhasználó 8765-ös példányához nem nyúltam.
- **Pilot:** `adat.py` + `epit.py --szakasz "1Móz 1:1-2:3"` ezen az ágon, kimenet a session scratchpadjában (a repón kívül); `file://`-ból nyitva. A pilot hatóköre csak 1Móz 1–25 / Zsolt 22, ezért a pilot-összevetés oldala az 1Móz 1 (a 6. szakasz oldala is ez: 1Móz 1:3, H0216).
- **Mockup:** a 9. változat HTML-je Artifact `read`-del, helyben renderelve (a Google Fonts betűi a hálóról töltődtek). Oldala az Ez 37, ezért a szerver az Ez 37-en is mérve (a 12. versre koppintva).
- **Böngésző:** headless Chrome a DevTools-protokollon, saját stdlib-kliens (`naplok/OLVASO_ALAPNEZET_M4/m4_bongeszo_meres.py`; playwright nincs a gépen, csomagot nem telepítettem). Szélességek: 375×812, 768×1024, 920×900, 1280×900 asztali emulációval (a 6. szakasz módszere), külön **telefon-emuláció** 375×812-n (mobil nézetablak, érintés-események). `prefers-color-scheme: light`, `prefers-reduced-motion: reduce` (az átmenetek nem zavarják a mérést). Kattintás valódi egér-, illetve érintés-eseménnyel az elem koordinátáján; 1,8 s várakozás a töredék betöltésére. Mérés: `getBoundingClientRect`, `scrollWidth`, a látható `fixed`/`sticky` elemek, a lapon belüli görgetődobozok és kilógó táblák, a 24 px-nél kisebb érintési célok. Nyers eredmény: `naplok/OLVASO_ALAPNEZET_M4/meres.json` (56 jelenet), a részletek-lapok blokkcímei: `blokkcimek.json`.
- **A mockup korlátja:** a mockup a szöveget és a blokkokat árnyék-DOM-ban (Shadow DOM) rajzolja; a mérőkód ezt bejárja a helyzet-adatokhoz, a táblák és az érintési célok számolása viszont csak a felső DOM-ot látja, ezért ezeket a mockupra nem közlöm.

## 2. A 6. szakasz táblázata, megismételve

Oldal: 1Móz 1, a 3. vers H0216-os szavára (szómód) vagy versszámára (versmód) koppintva. Az „új” oszlopban a szerver, zárójelben a 9. változat (Ez 37:12) és a #60 pilot ugyanazon a szélességen.

| Lelet | Kiinduló (2026-10-22) | Új, 375 px | Új, 768 px | Új, 920 px | Új, 1280 px | Ítélet |
|---|---|---|---|---|---|---|
| A részletek teteje, szómód (Olvasópult → olvasó) | 3 874 / 2 727 / 284 px (375 / 768 / 1280) | **422 px** a nézetablakban, alsó lap (mockup 422; pilot 5 047 px a dokumentumban, kattintásra odagörget) | **532 px** (mockup 532; pilot 3 223) | 86 px, oldalblokk (mockup 126; pilot 600) | 86 px (mockup 126; pilot 600) | javult |
| Ugyanez, interlineáris réteg | 34 277 / 22 281 / 284 px | **422 px** | **532 px** | 82 px | 82 px | javult |
| Görgetődoboz a görgetett oldalon (`.gordul` 340 px) | igen / igen / ragadós | a lap görget, benne **2 × `.gordul` 340 px** (szómód) | ugyanígy | ugyanígy | ugyanígy | **nem javult** (DT-F134q) |
| Az első vers kezdete | 640 / 495 / 454 px | **146 px** (mockup 132; pilot 1 160) | 112 px (mockup 105; pilot 688) | 202 px (mockup 220; pilot 635) | 202 px (mockup 220; pilot 635) | javult (E1 ≤ 200 px) |
| A fejléc magassága | 210 / 132 / 91 px | 49 px, ragadós egysoros sáv (mockup: nincs, a navigáció alsó lapon; pilot 262, nem ragadós) | 49 px (mockup: nincs; pilot 169) | 74 px (mockup 69 + 37 px változat-sáv; pilot 116) | 74 px (ugyanígy) | javult; a sáv a DT-F134n szerint tartós |
| A munkaasztal verslistája | 732 / 800 px / 180 px-es oszlop | — | — | — | — | kikerült (DT-F134g) |
| Vízszintes túlfolyás, oldal | 109 px (375) | **0** | 0 | 0 | 0 | javult |
| Vízszintes túlfolyás a részletek lapján | — (az oldal folyt túl) | szómód 118 px, versmód 41 px (Ez 37:12: 147; mockup Ez 37:12: 143) | 0 | szómód 93 px, versmód 17 px (Ez 37:12: 123; mockup: 118) | 0 | **nem javult**, áthelyeződött (DT-F134p) |
| Kilógó táblák a lapban | igen (375) | szómód 2 (`szo.ubs_dbh` 473 px, `szo.oshl` 468 px), versmód 3 (`vers.eredeti`, `vers.macula_morf`, `vers.ubs`) | 0 | szómód 2, versmód 1–3 | 0 | **nem javult** (DT-F134p) |
| 24 px-nél kisebb érintési cél | 45 / 323 (375), 56 / 429 (768) | 53 / 555, nyitott lappal 91 / 608 (pilot 50 / 436) | 52 / 555 | 121 / 627 | 121 / 627 | arányában javult (13,9% → 9,5% 375 px-en); nem célzott javítás |

A szómód lapjának 422 px-es teteje a nézetablak 52%-a (betekintés kb. félig, a brief 2.3 szerint); a kattintott vers (1Móz 1:3: 323–388 px) a lap fölött látszik minden mért 900 px alatti szélességen, az Ez 37:12-n is (görgetés után 80–241 px). Telefon-emulációval a szerver számai a 375 px-es asztali emulációéval azonosak.

**A kilógó tábla képe:** `naplok/OLVASO_ALAPNEZET_M4/szerver_1moz1_vers_375_kilogo_tabla.png` — a lap teljes nézetben, az „Eredeti szavak (TAHOT / TAGNT)” tábla „Angol tükörfordítás” oszlopa a jobb szélen levágva; a lap vízszintesen elhúzható.

## 3. Elfogadási feltételek

| | Állapot (M4) |
|---|---|
| **E1** | teljesül: 375 px-en az első vers 146 px-nél (a ragadós sáv 49 px); az oldal vízszintes túlfolyása 0 mind az 56 jelenetben |
| **E2** | teljesül: a lap 375 px-en 422, 768 px-en 532 px-nél nyílik (szó- és versmód, interlineáris réteg is); a koppintott vers a lap fölött |
| **E3** | teljesül: 920 / 1280 px-en az oldalblokk ragadós (86 px), kijelölés nélkül útmutató, a fejezet forrása és a számlálók (kép: `szerver_ez37_ures_920.png`, `_1280.png`) |
| **E4** | M4-ben nem mértem újra (M1–M3 mérte) |
| **E5** | M4-ben nem mértem újra (M3 mérte, 2. szakasz); a mérés világos rendszertémával futott, a lap világos |
| **E6** | a beolvasztás nem okozott új piros tesztet (7. szakasz) |
| **E7** | két „törik” sor nem javult (görgetődoboz, kilógó táblák): DT-F134p, DT-F134q |

## 4. Összevetés a #60 pilottal, blokkonként

Képek: `pilot_1moz1_*` és `szerver_1moz1_*` (375 / 768 / 920 / 1280 px, valamint `_telefon`). A tartalmi blokkok (a szó- és vers-lap adatai) a #76 összevetése szerint (`naplok/OLVASOI_KONKORDANCIA_pilot_osszevetes.md` 2. és 8. szakasz) változatlanok; itt az elrendezés és a látvány a mérce.

### 4.1 Oldal-szint

| Blokk | Pilot | Szerver (új) | Eltérés |
|---|---|---|---|
| Oldalfej | cím + alcím + számláló-címkék + téma-gombok, nem ragadós, 116–262 px | egysoros ragadós sáv (könyvválasztó, ‹ ›, Aa, Strong, ⚙, ⌕), 49 px; 900 px-től fejléc + kánon-sáv, 74 px | a szerver kisebb és ragadós; a pilot címe és alcíme nincs |
| Számláló-címkék (34 vers, szó-lapok, BDB magyarul, Károli–Strong) | a fejlécben | az oldalblokk üres állapotában (900 px-től), 900 px alatt a „Forrás és számlálók” hivatkozás mögött | áthelyezve (DT-F134l) |
| „Hogyan olvasd ezt az oldalt?” | nyitott `details` a szöveg fölött (a szöveg 375 px-en 1 160 px-nél kezdődik) | az oldalblokk üres állapotában; 900 px alatt a lap „Forrás és számlálók” nézetében | áthelyezve; a szöveg ettől kezdődik 146 px-nél |
| Károli-szöveg | folyó szöveg, nagy fejezetszám-iniciálé | versenként új sor (DT-F134o: az Aa-ban folyóra váltható), fejezetcím h1 | elrendezési döntés (DT148, DT-F134o) |
| Kapcsolt szavak jelölése | jelölőnégyzet a szöveg fölött | „Strong számok” chip a sávban | áthelyezve (DT-F134o) |
| Téma-váltó | három gomb a fejlécben, alap „Rendszer” | a ⚙ menüben, alap „Világos” | DT295, DT-F134i |
| A kattintott szó kiemelése | a szó minden előfordulása kitöltött háttérrel (`aktiv`) | **csak a vers** kap halvány hátteret, a szó nem | **új lelet**: a szerveren nincs szó-kiemelés (5. szakasz, c) |
| Telefon (valódi mobil nézetablak) | nincs `viewport` meta: 980 px-es asztali elrendezés kicsinyítve, a szöveg és a panel egymás mellett, olvashatatlanul kicsi (`pilot_1moz1_ures_375_telefon.png`) | saját mobil elrendezés, azonos a 375 px-es méréssel (`szerver_1moz1_szo_375_telefon.png`) | a szerver javára |

### 4.2 A részletek helye és működése

| Blokk | Pilot | Szerver (új) | Eltérés |
|---|---|---|---|
| Panel 900 px alatt | statikus panel a szöveg alatt (375 px: 5 047 px, 8 557 px magas); kattintásra a böngésző odagörget, a vers kikerül a képből (−3 758 px) | alsó lap 422 / 532 px-nél, a vers fölötte marad; teljes nézet a ⤢ gombbal | a szerver javára (E2) |
| Panel 900 px-től | ragadós panel a szöveg mellett, 600 px-nél kezdődik (a fejléc és az útmutató alatt), 876 px magas | ragadós oldalblokk 86 px-nél, 576–810 px magas | a szerver feljebb kezd |
| Fülek | Szó · Vers részletei · Bezárás × | versmódban Vers · Kereszthiv. · Témák · Motívum; szómódban fül nincs, a fejsorban „A vers: 1Móz 1:3 →” és ✕ | más szerkezet (DT293) |
| Görgetés | a panel egészében görget, belső görgetődoboz nincs | a lap görget; szómódban benne 2 × `.gordul` 340 px | a pilot javára (DT-F134q) |
| Táblák | a pilot csempékkel és listákkal dolgozik, táblázat a panelen nincs (0) | 7 (szómód) / 12 (versmód) táblázat, ebből 375 px-en 2–3 kilóg | a pilot javára (DT-F134p) |

### 4.3 Szó-lap (H0216, 1Móz 1:3) — blokksorrend

| Pilot | Szerver (új) | Eltérés |
|---|---|---|
| Szó adatai (héber): nagy héber alak, Alapjelentés „fény”, 3 számláló-csempe (121 / 21 / 123) | a lap fejsora (H0216 אוֹר, „fény”) + a lap élén nagy héber alak, „ALAPJELENTÉS fény”; „Strong-szótár” tábla; „Előfordulás, könyvek száma” mondatban (121, 21) | az alapjelentés magyarul megvan (a #76-ban még hiányzott); a számlálók szövegként, csempe nélkül |
| Ebben a versben (1Móz 1:3) | Ebben a versben (Károli itt „világosság”, alak, LXX φῶς G5457, UBS) | megvan, azonos sorrendben (a „Károli-alakok” előtt) |
| Így fordítja Károli | Károli-alakok és bizonyosság | megvan |
| BDB apparátusokra bontva (Címszó … Jelentésszerkezet, 11 jelentéspont) | ugyanaz, ugyanazzal a 11 ponttal; többlet: Jelmagyarázat | megvan |
| Görög megfelelő, SDBH, SECE, OSHL, TBESH, tW | megvan | megvan |
| — | többlet: BDB angol, BDB magyar (nyers), UBS DBH, Rokon szavak (OSHL), Nyelvtani szűrés | a #76 ismert többlete; a két nyers BDB-blokk adja a `.gordul` dobozokat |

### 4.4 Vers-lap (1Móz 1:3) — blokksorrend

| Pilot | Szerver (új, „Vers” fül) | Eltérés |
|---|---|---|
| Versszámozás (a panel élén) | LXX-versszám + Versszámozás (MT / KJV), a fül közepén | ismert (V1) |
| Károli-szöveg, Héber szöveg (csempék), Septuaginta (csempék) | ugyanígy, a fül élén | megvan |
| Kereszthivatkozások (TSK), Károli-kereszthivatkozások | a „Kereszthiv.” fülön | fülre bontva (DT293) |
| Témák (Nave), Tulajdonnevek (TIPNR) | a „Témák” fülön | fülre bontva |
| Motívumadat, Igehely-kapcsolatok | a „Motívum” fülön | fülre bontva |
| Angol szó (BSB, KJV), LXX-döntések, LXX együttelőfordulás („1 héber szó, 4 pár”), LXX többlet | megvan, a „Vers” fülön | megvan |
| — | többlet táblázatok: Károli–Strong, Eredeti szavak, Macula, héber–görög párosítás, LXX_OS, igealak-feloldás, UBS | a #76 ismert többlete; ezek a kilógó táblák |

## 5. Vizuális összevetés a 9. változattal

Képpárok: `szerver_ez37_vers_<sz>.png` ↔ `mockup9_ez37_vers_<sz>.png` (375 / 768 / 920 / 1280), `szerver_ez37_ures_<sz>.png` ↔ `mockup9_ez37_ures_<sz>.png` (920 / 1280), telefon: `mockup9_ez37_vers_375_telefon.png`.

**Azonos:** a színek, a betűk, a lap alakja (lekerekített felső sarkok, fogó, árnyék), a lap helye (422 / 532 px), a fejsor (igehely + a vers eleje, ⤢, ✕), a fülsor aláhúzott aktív füllel, a kiemelt vers halvány zöld háttere, a kánon-sáv műfajszínei, a 900 px-es oldalblokk szélessége (400 px), a pontozott aláhúzás.

**Szándékos eltérés (döntéssel):** nincs „Másolás forrással” (DT-F134m); üres állapotban útmutató a fejezet-kalauz helyett (DT-F134l); 900 px alatt ragadós egysoros sáv a fejezetcímre koppintós navigáció és a tájoló pirula helyett (DT-F134n); versenként új sor és kitöltött szélesség a 60ch-s folyó szöveg helyett, „Strong számok” chip a sávban (DT-F134o); a „Legutóbb” a fejléc 2. sorában, nem alsó sávban (M2); a mockup jelölő chipjei (kereszthivatkozás, motívum, témák) és a szövegbeli ↗-kereszthivatkozás-jelek más változatok újdonságai, a hatókörön kívül.

**Új, döntés nélküli eltérés (M4 lelet):**

- **(a)** a mockup fülei számlálót mutatnak („Kereszthiv. 17”, „Témák 9”), a szerveréi nem;
- **(b)** a szerver szövegoszlopa fölött „← 36. fejezet · Ezékiel könyve · 38. fejezet →” hivatkozássor áll (a mockupban nincs; a sáv ‹ › gombjai ugyanezt adják);
- **(c)** a kattintott szó nem kap kiemelést (a pilotban kitöltött háttér, a mockup szómódját a mérés nem képezte le).

Ezek kis, elrendezési pontok; a felhasználó döntheti el, kellenek-e (a M5 előtt javítókörben, vagy külön tételben).

## 6. Nyitott döntések (⛔)

- **DT-F134p** — a részletek lapjának széles táblái (375 px-en és a 920 px-es oldalblokkban kilógnak; a lap vízszintesen görget, a jobb oszlop levágva). (a) a táblák saját, vízszintesen görgethető burkolóba (`overflow-x: auto`), a lap maga nem görget vízszintesen · (b) tördelés: a tábla a lap szélességére (`table-layout`, `overflow-wrap`), a hosszú oszlopok több sorba · (c) marad, ahogy a mockupban. **Javaslat: (a)** — a tartalom változatlan, csak CSS; a 9. változat ugyanígy törik, tehát a mockuptól ez sem tér el látványban.
- **DT-F134q** — szómódban a lapon belüli két 340 px-es `.gordul` doboz (BDB angol, BDB magyar nyers): görgetés a görgetésben, kis képernyőn különösen. (a) a lapban a `.gordul` magasságkorlátja feloldva (a lap maga görget) · (b) a két nyers BDB-blokk alapból csukott `details` · (c) marad. **Javaslat: (a)**, csak a részletek lapján belül (a nem-fejezet lapokon a korlát marad).

Mindkettő a brief `ir` mezőjén belüli CSS-változás, blokktartalom nem változik. Az 5. szakasz (a)–(c) pontja nem igényel külön DT-tételt, ha a felhasználó egyszerűen jelzi, melyik kell.

## 7. Tesztek

`python eszkozok/teszt_futtat.py --gyors` a beolvasztás után; adatbázis: `/home/basesoft/pardes/pardes.db` (WSL-natív, 895 MB, `epites_ts` 2026-10-14T09:35:00Z).

| Fájl | Ág (`9e7e0f98`) | Main (`9cf0e43a`, ugyanazzal a DB-vel) |
|---|---|---|
| `teszt_arculat.py`, `teszt_indito.py`, `teszt_kereses.py`, `teszt_tervezo.py` (49), `teszt_ubs_dbh.py` (6) | zöld | — (nem futtattam: zöldek) |
| `teszt_olvaso_szerver.py` | 92 teszt, 2 piros (`test_1moz_1_25`, `test_zsolt_22`), 1 kihagyott | 80 teszt, ugyanaz a 2 piros, 1 kihagyott |
| `teszt_bdb_vers_jelentes.py` | 31 teszt, 1 piros (`test_bajtra_azonos`) | ugyanaz |
| `teszt_pilot_aranymintaval.py` | 22 teszt, 5 piros (`test_DT_F76f_…`, `test_DT_F76g_…`, `test_heber_csempe_…`, `test_magyar_tartalom_…`, `test_szamlalok_…`) | ugyanaz az 5 |

**A piros lista az ágon és a main-en tételesen azonos (8 / 8);** a hibák szövege adat-eltérésre mutat (pl. a pilot a TSV-kből `συναχθήτω`-t, a DB `συναξθήτω`-t ad; a BDB-magyar számláló 96 a pilotban, 61 a DB-ben): a WSL-natív `pardes.db` 2026-10-14-i, a main TSV-i azóta változtak. Ez nem a mi águnkból ered; nem javítottam (a DB újraépítése a #120 / az indító dolga). Az M3 alapja 289 teszt volt 4 ismert pirossal; a különbség az új main-tesztekből és a régi DB-ből jön.

## 8. Valódi telefonos próba (a felhasználó végzi)

1. A szerver indítása a WSL-ben, a hálón elérhetően: `wsl -d pardes -e bash -lc 'cd /mnt/c/Users/bases/Desktop/wt-olvaso-alapnezet && PARDES_DB=$HOME/pardes/pardes.db /home/basesoft/pardes/eszkozok/olvaso_szerver/.venv/bin/python eszkozok/olvaso_szerver/alkalmazas.py --host 0.0.0.0 --port 9765 --kiadas belso'` (a tervező mentése továbbra is csak helyi kérésre ír).
2. Ha a WSL NAT-módban fut (nem „mirrored”), rendszergazdai PowerShellben: `wsl -d pardes -e hostname -I` → a WSL IP; `netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=9765 connectaddress=<WSL IP> connectport=9765`.
3. Tűzfal: `New-NetFirewallRule -DisplayName "PaRDeS olvaso 9765" -Direction Inbound -Protocol TCP -LocalPort 9765 -Action Allow -Profile Private`.
4. Telefonon (ugyanazon a Wi-Fi-n): `http://<a gép IP-je>:9765/1Moz/1`, majd `/Ez/37`.
5. **Mit kell nézni:** (a) a sáv egy sorban marad-e (a 375 px-es mérésben 3 px a tartalék; nagyobb rendszerbetűvel törhet); (b) versszámra és szóra koppintva a lap a képernyő felénél nyílik-e, a vers fölötte látszik-e; (c) a lap felhúzása teljes nézetre, lehúzása vissza és zárásra — a mozgás folyamatos-e (headlessben nem mérhető); (d) a lapon a széles táblák (DT-F134p) és a BDB-dobozok (DT-F134q) hogyan görgetnek ujjal; (e) a ⌕ mögötti kereső, a kánon-sáv és a „Legutóbb”; (f) a ⚙ téma-választás újratöltés után megmarad-e.
6. A végén: `netsh interface portproxy delete v4tov4 listenaddress=0.0.0.0 listenport=9765` és a tűzfalszabály törlése, ha nem kell tovább.

## 9. Ami nem futott le, korlátok

- Valódi telefon (8. szakasz) — nem futott; a telefon-emuláció (mobil nézetablak, érintés) igen.
- Mozgás: az átmeneteket a mérés kikapcsolta (`prefers-reduced-motion`); a húzás nem mérve.
- A mockup tábla- és érintésicél-számai (árnyék-DOM), lásd 1. szakasz.
- A szerver friss DB nélkül: a lapok tartalma a 2026-10-14-i `pardes.db`-ből; az elrendezés mérését ez nem érinti.
- Képek: válogatás (27 db) a `naplok/OLVASO_ALAPNEZET_M4/` alatt; a többi jelenet csak a `meres.json`-ban.
