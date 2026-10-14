# Zárójelentés — #76 OLVASOI_KONKORDANCIA, 1. menet (M0 és M1)

*Állapot: a feladat NEM kész, `allapot: megallt`. Ez a menet az M0 (terv) és az M1 (helyi környezet) lépéseit fedi; az M2–M7 hátravan. Ág: `claude/olvasoi-konkordancia` (F76.0–F76.8).*

- **M0:** terv és hat döntés (DT146 🟢, 2026-10-14): Flask, alak ∪ szótári alak, frázis a `token_karoli`-ból, `pardes_nezet` süti csak váltáskor, `systemd-run` korlát a disztribúción belül, helyben a teljes db authorizerrel, nyilvános célgépen szűrt példány. A terv: `naplok/OLVASOI_KONKORDANCIA_M0.md`.
- **M1:** `pardes` WSL-disztribúció (Ubuntu 24.04, `E:\WSL\pardes`), Python 3.12 uv-vel, `pardes.db` a disztribúció saját lemezén, korlátozott indítás (`/statusz` 200). Az M1 zárónaplója az M0 fájl 4.3 szakaszában van. A mért méretek ott állnak (`ext4.vhdx` 2,73 GiB az M1 végén).
- **Szótövező aranyminta 3.12-n:** hibrid v2 súlyozva 99,1%, bájtra azonos a Windowson rögzítettel.
- **Független ellenőr:** `naplok/ELLENOR_F76.md`, 8 eltérés. Javítva: E2, E4–E8. **Nyitott: E1 és E3.**
- **E1 (K4 frissesség) NYITOTT:** a D5 három táblát eltérőnek mért (`vers_szamozas`, `lxx_versszam`, `nave_vers`): a `Karoli_versmegfeleltetes.tsv` (F91.10) és a `LXX_versificacios_terkep.tsv` (F91.12) az építés (`epites_ts=2026-10-13T18:10:45Z`) után módosult. A `pardes.db` a #91 előtti állapot. Újraépítés kell az M5 előtt (`eszkozok/sqlite_epit.py`); ez kívül esik az `ir` mezőn.
- **E3 NYITOTT:** az F79/F92/F95 építő-tesztek nem futottak 3.12-n (a ritka klónban nincs `konkordancia/`); a 3.12 az aranyminta alapján véglegesedett, ez az M0-ban kimondva.
- **Egyeztetett eltérések a briefhez:** Python 3.12 (3.11 helyett), `E:\WSL\pardes` (`D:\WSL\pardes` helyett), frázis-keresés a `token_karoli`-ból.
- **Nyitott döntés a felhasználónak:** ki, mikor és melyik ágon építi újra a `pardes.db`-t. Addig az M2 mehet, de a Zsolt-lapok és a Nave/LXX-versszám blokkok a régi számozást mutatnák.
- **Nem történt meg:** merge, M5–M7, a rootfs letöltési méretének mérése (utólag nem mérhető).
- **Következő:** M2 (alkalmazás), külön `/kovetkezo`-val, ugyanezen az ágon.

# Zárójelentés — #76 OLVASOI_KONKORDANCIA, 2. menet (M2: alkalmazás)

*Állapot: a feladat NEM kész (M3–M7 hátra), `allapot: megallt`; az M2 kész. Ág: `claude/olvasoi-konkordancia-m2` (F76.10–F76.20). Részletes napló: `naplok/OLVASOI_KONKORDANCIA_M0.md` 4.4.*

- **Elkészült:** Flask-alkalmazás (`eszkozok/olvaso_szerver/`), Flasktól független `oldalak.py`, 40 blokk-azonosító (a pilot 39 blokkja, a 9. kettéválasztva), három nézet (az Interlineáris `token_par` pozíció szerint), `pardes_nezet` süti csak nézetváltáskor, konfigurációs hozzáférés, kiadási kapcsoló authorizerrel, `/pardes.db` → 404, `/statusz`, gunicorn gthread 1×4, `telepit.sh` (az indítás az ellenőrzés sikeréhez kötött).
- **Tesztek (végrehajtói futás, nem független ellenőri):** `teszt_olvaso_szerver.py`, 61 teszt, OK, 63,9 s, Python 3.12.3 (`pardes` WSL); parancs és proveniencia: M0 4.4.
- **E1 lezárva:** a `pardes.db` újraépült (F97, `epites_ts=2026-10-14T09:35:00Z`), D5 eltérő tábla nincs, `frissesseg.py` ÉP. **E3 lezárva:** `naplok/PARDES_DB_UJRAEPIT_zaras.md` 6. és 9. szakasz (64 építő-teszt, 3.12.3); az itteni E3-mal azonos tárgy.
- **DT-F76d eldöntve (a):** a D2 egyetlen eltérése (`gorog_szo:usz_elofordulas`, 27 és 11 lap: a „+” Strong-láncok) elfogadva, a `token_strong` a helyes; a brief K1 a kivételt kimondja, a D2-teszt csak ezt az okot engedi át; a szó-lapon bontás látszik („54, ebből 25 láncelemként”). A DT133 külön, nyitott.
- **Jelleg-átírás a pilot szerint (M0 3.4; régi → új):** `vers.versszamozas` gépi → forrásadat; `vers.lxx_versszam` gépi → forrásadat; `szo.usz` gépi → forrásadat; `vers.bsb` forrásadat → forrásadat + gépi; `vers.kjv` forrásadat → forrásadat + gépi; `vers.nave` gépi → forrásadat + gépi; `vers.tipnr` gépi → forrásadat + gépi; `szo.tbesh` forrásadat → forrásadat + gépi. Más blokk jellege nem változott; a `szo.magyar_gorog` (nincs pilot-cím) modell-kimenet marad.
- **Ellenőri tételek (`ELLENOR_F76_M2.md`):** 1. D2/K1: döntve (DT-F76d), brief átírva; 2. szövegoszlop jelleg- és forrássor: javítva; 3. D2-teszt `ok` mező: javítva; 4. jelleg-összevetés a pilottal: javítva (teszt); 5. telepit.sh és .gitignore: javítva; 6. ismeretlen blokk-azonosító: javítva; 7. DT-helyőrző: felvéve. Az újrafutó független ellenőrzés az orkesztrátoré.
- **Egyeztetett eltérések:** BDB gépi apparátus-bontása nincs átírva; a fordított proxy nincs kiválasztva; a kereső (M3) nincs, csak gyorsugrás; a Nave a `nave_vers`-ből jön (a pilot `bovites.py` marad, `ir` kívül).
- **Nyitott:** N-F76d (BDB-bontás; Caddy vs nginx, javaslat Caddy; `NYITOTT_FELADATOK.md`); DT133 (a `scan`-javítás és a korábbi görög ÚSZ-scanek felmérése) nyitott, nem módosult; M4 mérés a korláttal.
- **Nem történt meg:** M3, M4, merge, PR, M5–M7; a `pr` és `lezarva_osszegzes` mező üres.
- **Következő:** M3 (keresés), külön `/kovetkezo`-val; ⛔ M5, ⛔ M6, ⛔ M7.

# Zárójelentés — #76 OLVASOI_KONKORDANCIA, 3. menet (M2b: a #60 pilot kirajzolt blokk-készletének pótlása)

*Állapot: `allapot: megallt`; az M2 „kész” állítása függőben a DT-F76e–i döntéséig. Ág: `claude/olvasoi-konkordancia-m2b` (F76.23–F76.27). Részletek és tábla: `naplok/OLVASOI_KONKORDANCIA_pilot_osszevetes.md`.*

- **Ok:** a felhasználó szerint a szerver nem egyezik a #60 pilottal. Mérés (pilot újraépítve a repón kívül, böngészőben kirajzolva, szerver Flask test_client-tel, 1Móz 1:1–2:3 és Zsolt 22): az észrevételek **igazoltak**, két ponton árnyalva (a magyar BDB megvan nyersen; a motívum-blokk megvan, összevonva). Az M0 3.4 „39 blokkja” a *mért adatblokkok* listája, nem a kirajzolt blokkoké (N-F76g).
- **Pótolva (döntés nélkül):** írásjeles Károli-szöveg mindhárom nézetben; fejléc-számlálók és „Hogyan olvasd”; héber és LXX szócsempék, BSB/KJV csempék; „Ebben a versben” a szó-lapon (vers-kontextussal); LXX versszintű együttelőfordulás; fejezet-szintű Nave; adatréteg-blokk háromra bontva; „57 feldolgozott könyv” jelzés. Regiszter: 46 blokk-azonosító.
- **Döntésre vár (DT-F76e–i, ⛔ a pótlás a döntésig nem készül):** e) folyó szöveg vs versenkénti sor; f) magyar alapjelentés vs angol Strong-glossza; g) a magyar BDB bontása és forrása (N-F76d (1)); h) „LXX többlet és számozási eltérés”: a két forrástábla nincs a `pardes.db`-ben; i) aláhúzás-kapcsoló és témaváltó. Kisebb formai eltérések: N-F76h.
- **Tesztek (végrehajtói futás, nem független ellenőri):** új `teszt_pilot_aranymintaval.py`: 19 teszt, 14 zöld + 5 `expectedFailure` (a döntésre váró hiányok, nem zöldre állítva); `teszt_olvaso_szerver.py`: 62 teszt, OK. Python 3.12.3, `pardes` WSL-disztribúció; parancs és proveniencia: az összevetés 7. szakasza.
- **A futó szerver** (8765) az M2 kódjával indult; újraindítás kell (a Flask-szerver nem tölti újra a kódot, és gyorsítótáraz).
- **Nem történt meg:** a döntésre váró pótlások, M3, M4, merge, PR, M5–M7; az `ir` mezőn kívül csak a `NYITOTT_FELADATOK.md` (N-F76f–h), a `DONTESEK.md` (DT-F76e–i) és a brief fejléce változott.
- **Következő:** a DT-F76e–i döntése és a felhasználó vizuális összevetése; utána M3 (keresés), külön `/kovetkezo`-val; ⛔ M5, ⛔ M6, ⛔ M7.
