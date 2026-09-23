# Döntésnapló — ISTENTISZT-001 kereszthivatkozási törzscikk, pilot v1

*2026.09.23 · bemenet: `lexikon/ISTENTISZT-001_TUDOMANYOS.md` (a `main` 2026.09.23-i állapota, codeload) · eszköz: `torzscikk_pilot.py`*

## Döntések

| # | Döntés | Indoklás |
|---|---|---|
| D1 | Formátum: Markdown. Áttekintő táblák, alattuk a teljes szövegek. | A repó Markdown-alapú; a HTML (lenyitható cellák) a pilot után dönthető el. |
| D2 | Pilot-rövidítés: a törzscikk a lexikonoldalból renderel. | A kézi rétegek még a lexikonoldalon élnek. Éles változatban a bemenet a belső adatmodell és a forrásréteg (l. N1). |
| D3 | Kereszthivatkozás-központú felépítés: igehelyenként egy blokkban a Károli-szöveg, a megjegyzés, a funkció, a kulcsszó, a Strong és szótári jelentés, az UBS-jelentés, az LXX-döntés, a kapcsolatok és a kereszthivatkozások. | A lexikonoldal 1., 3., 4. és 5. szakaszának versenkénti adatai így egy helyen olvashatók. |
| D4 | Az 1. szakasz eleji tábla csak navigáció (igehely, funkció, PaRDeS-szint, megbízhatóság). | Minden más adat a versblokkban áll, nem ismétlődik. |
| D5 | A kapcsolatok a versnél mindkét irányban (→ kimenő, ← bejövő), linkkel; a teljes tábla, az ábra és az alátámasztás a 2. szakaszban. | A vers felől és a hálózat felől is olvasható. |
| D6 | Szótári háttér szerepkör-mátrix szerint. Görög szó: alapjelentés (TBESG) → mélységi szócikk (Thayer) → szemantikai mező (SDGNT, Louw–Nida) → előfordulás (Mounce) → héber megfelelők (SECE) → klasszikus háttér (LSJ) → jelentősége. Héber szó: alapjelentés (BDB) → jelentés-lista (TBESH) → szemantikai mező (SDBH) → görög megfelelők (SECE) → jelentősége. | Minden szónál azonos sorrend; hiányzó szerep nem jelenik meg. |
| D7 | Duplikátumok egyszer: az LSJ G2564 és a TBESH H7121 részlete a 2. és a 2/b szakaszban is szerepelt; a generált változat maradt. | A szerepkör-mátrix célja az ismétlés megszüntetése. |
| D8 | A „Miért fontos" és „Jelentősége" bekezdések az érintett szóhoz kerültek; a „Kiemelt módszertani jelentőség" új címe „A három ige együtt". | A jelentőség a szó mellett olvasható. |
| D9 | Eltávolított üzemeltetési elemek: l. a Mérések táblát, továbbá a kolofon fájltáblája, az adatforrás-lista, 3 üzemeltetői törzsmező (forrás-study, kereszthivatkozás-napló, sablon-megfelelőség), a TBESH SQLite-megjegyzés, a „nyers, gépileg olvasható adat" bekezdés, a 2/b bevezetője és a Funkció-jelmagyarázat SEMA-hivatkozása. | A felhasználó szabálya: napló- és üzemeltetési bejegyzés nincs a törzscikkben. |
| D10 | Kiejtés: a szó-fejlécekben és az LXX-táblában a tudományos átírás magyarosra cserélve (epikaleō → epikaleó, kaleō → kaleó, boaō → boaó, qa.ra → kárá, shem → sém), 52 helyen. | Rögzített konvenció. A kulcsszó-cellák STEP-átírása (pl. k.Ro') változatlan, l. N4. |
| D11 | A kézi szövegben 5 szakaszhivatkozás a törzscikk számozására átírva (2/b → 5.; a 2. szakasz generált része → 5.; 1–4. → 1–5.; 3. → 4.; „UBS-oszlop" → „UBS-jelentés"). | A lexikonoldal számozása itt nem érvényes. |
| D12 | Lábléc: hivatkozás, a szótárak licenccel, fájlútvonal nélkül; pótolva a Károli, a SECE és a Mounce szó szerinti megjelölése. | A Mounce kötelező megjelölést ír elő; a SECE és a Mounce a lexikonoldal 8. szakaszából hiányzik (l. N5). |
| D13 | A TSK- és Károli-kereszthivatkozások listából egysoros felsorolásba, „(Votes: n)" → „(n)". | Tömörebb, tartalomvesztés nélkül (106 = 106). |

## Mérések

| Mérés | Lexikonoldal | Törzscikk |
|---|---|---|
| Sorok | 1 345 | 1 285 |
| Méret (bájt) | 116 854 | 105 335 |
| Igehelyek (ÓSZ / ÚSZ) | 32 (22 / 10) | 32 (22 / 10) |
| Károli-szöveg | 32 | 32 |
| Kapcsolatok | 25 | 25 |
| LXX-sorok | 22 | 22 |
| Kereszthivatkozás-találatok | 106 | 106 |
| Szavak (fő + rokon) | 3 + 2 | 3 + 2 |
| GENERÁLT-marker | 20 | 0 |
| Hatókör-szöveg („Ez a blokk…") | 10 | 0 |
| Proveniencia-lábjegyzet és -jel | 32 + 32 | 0 |
| NAPLO-blokk | 15 | 0 |
| „(kézi)" címke | 8 | 0 |
| Forrásfájl-sor a szócikkek alatt | 11 | 0 |
| Fájlhivatkozás a kézi prózában (6–7. szakasz) | 7 | 7 (l. N2) |

## Nyitott kérdések a pilotból

| # | Kérdés |
|---|---|
| N1 | **Előfeltétel az éles renderhez:** a kézi rétegek (kivonat, értelmezés, minősítés, alátámasztás, jelentőség-bekezdések, 7. szakasz) a forrásrétegbe költöznek, és mindkét render onnan olvas. |
| N2 | 7 fájlhivatkozás maradt a kézi prózában (6. és 7. szakasz, pl. `Bibliai_Motivumlexikon_tervezesi_naplo.md`). Átírni a forrásban, vagy a render cserélje le? |
| N3 | 3 NAPLO-blokk tartalmi megjegyzés volt: a Típus-mező névütközése a kapcsolat-TSV-ben; a tematikus study 15 → 22 frissítésének igénye; a Variáns-kategória döntése. A törzscikkből kikerültek, a lexikonoldalon megmaradtak. Átkerüljenek-e nyitott kérdésként a 7. szakaszba? |
| N4 | A kulcsszó-cellák és az LXX-tábla héber alakjainak kiejtése STEP-átírás (k.Ro', i.yik.Ra'); ez a kiejtés-generátor (SZ1) feladata. |
| N5 | A lexikonoldal 8. szakaszából hiányzik a SECE és a Mounce, pedig a 2/b használja őket; a Mounce megjelölése kötelező. Ez a lexikonoldalon is javítandó. |
| N6 | A G0994-megjegyzés a forrásban elavult („a 2. szakasz nem ad hozzá szócikket"), pedig a Rokon szavak alblokk óta ad. A törzscikkben átírva (D11), a lexikonoldalon javítandó. |
| N7 | Ha egy kereszthivatkozás célja maga is a motívum igehelye, linkeljen a versblokkra (a pilot nem linkel). |
| N8 | HTML-változat lenyitható szócikkekkel (D1). |
