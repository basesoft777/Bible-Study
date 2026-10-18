# Harmadik független újraellenőrzés — `F09_SZOTAR_S2_BRIEF.md` (#9)

*Ág: `claude/f09-szotar-s2`, HEAD `fb2e2a2a`; javító tartomány `88c8fc9e..fb2e2a2a` (F9.J15–J27); merge-base `0d7e9dec`. Ellenőr: `fuggetlen-ellenor`, `claude-opus-5-5` (kért: `opus`). Az ellenőr nem írt a repóba; a jelentést az orkesztrátor mentette ide tartalmi változtatás nélkül, rövidítve. Eredmény: **ELTÉRÉS, 5 tétel**.*

## Eltérések súlyossági sorrendben

1. **A párosítás táblasornál csak igehelyre is párt ad, és ezzel tartalomvesztést takarhat el** (DT191, `eszkozok/render_diff_osztalyoz.py`). A táblasor kulcsa `('sor', szakasz, első cella, Strong-halmaz)` (`:652`); a törzscikk „1. Igehelyek…” táblájában nincs Strong-oszlop, így a kulcs gyakorlatilag szakasz + igehely (a menet saját mintája: `naplok/SZOTAR_S2_parositas_minta.md:14`). Ellentmond a `naplok/SZOTAR_S2_zaras.md:9` (b) mondatának és a DT191 „teljes kulcs” meghatározásának. Pár esetén a törölt sor a hozzáadott kategóriáját kapja, túlélés-próba nélkül (`:797`); a kulcson kívüli cellákat senki nem veti össze. Ugyanígy: a `tetel` kulcs (`:655`, az érték szövege nincs benne), a `leiro`/`osszesites`/`jelmagyarazat` kulcs (`:658-662`, csak a szakasz), és az (1) lépés (`:765-766`). A teszt ezt el is fogadja (`eszkozok/teszt_render_diff_osztalyoz.py:255-263`: cellacsere → `elavult_adat`). A mostani adaton 12 kézzel visszafejtett párnál (word-diff a 16 fájlon) **nem talált ténylegesen eltakart veszteséget**; a tényleges párlistát nem látta.
2. **A zárójelentés 4a pontjának számai nem egyeznek a TSV-vel** (`naplok/SZOTAR_S2_zaras.md:10`): „8 motívum × 2” forditas_ubs-sor helyett 7 × 2 = 14 (ISTENTISZT-001-nek nincs); „16 LXX-sor” helyett a bontás 13-at ad; „BDB-forrássor (3 sor)” valójában 2 BDB + 1 LSJ. A TSV maga helyes (14/2/3/10/3 = 32).
3. **A TSK-lábnyom 11 → 13 bővítéséről nincs felhasználói döntési nyom.** A kód (`render_diff_osztalyoz.py:366`) és a brief K10 (`:153`) 13-at tart; a `DONTESEK.md:266` még „csak a név szerint felsorolt 11 sor”; az `NYITOTT_FELADATOK.md:132` (N-F09g) 11-et sorol, az Ézs 38:18 nélkül; a kódkomment (`:365`) önellentmondó. Adattal indokolt: `lekerdez.py tsk "Préd 9:10"` → `Ézs 38,18 Votes=15` (`scope=range:Préd 9:10 | forras=TSK_kereszthivatkozasok.tsv | n=49 | ts=2026-10-17T20:35Z`).
4. **A brief K10 elavult** (`F09_SZOTAR_S2_BRIEF.md:153`): „`ATKULCSOLT_SOROK`: 3 sor”, a kódban 27 (`:335-361`); a K10 „ismeretlen 0”-t ír elő, a 32 elfogadott sor csak a DT-F09g-ben szerepel.
5. **A felhasználói besorolás egy újrafuttatással elveszhet** (`render_diff_osztalyoz.py:895-897, 903`): az osztályozó a `*_ismeretlen.tsv`-t háromoszlopos fejléccel felülírja (a `felhasznaloi_besorolas` oszlop és a megjegyzések eltűnnek), és a 32 sor nincs beírva az osztályozóba, ezért újrafuttatáskor kilépési kód 2. Csoportszinten a `DONTESEK.md:266` és a zárójelentés megőrzi; soronként csak a verziózott TSV.

## Megjegyzések a 32 elfogadott sorhoz

- Az LSJ-sor nem formátum-, hanem licencverzió-változás (CC BY-SA 3.0 → 4.0; `adat/licencek.tsv:12`); a próba kézi rése még 3.0-t ír (`generalt_proba/F09_szotar_s2_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md:1261`, míg `:1174`, `:1980` 4.0).
- Az 5 HODIT-001 `szamozas_elteres` helyőrző nem „feloldódott”, hanem `kutatói azonosítás függőben` lett (`HODIT-001_TORZSCIKK.md:171-222`: Józs 12:4, 13:12, 15:8, 18:16 …).

## Rendben

- **TBESH-alszócikkek:** nincs hamis TBESH-„nem tárgyalja”; 4 szúrópróba egyezik a `TBESH.txt`-tel (H2403a `:3270`, H7451c `:10085/10087`, H1121a `:1558-1565`, H2416a–e `:3289-3293`); az `N:` alszócikkek kimaradnak (a pontos sor `N:` esetén is bekerül, pl. H5303 — a motívum tokenje, helyes); H7497: „csak tulajdonnév-alszócikk: H7497a, H7497b” (`HODIT-001_TUDOMANYOS.md:372`, `HODIT-001_TORZSCIKK.md:608`).
- **TAHOT-ág:** igazolva, hogy a `TAHOT_kivonat.tsv` Strong-oszlopa betűutótag nélküli (`H\d{4}[A-Za-z]` 0 találat; `lekerdez.py scan H2403B` elutasítja). A `Szótő` oszlop lemma szerinti szűkítést lehetővé tenne — ez nem a kért ág.
- **Párosítás:** kizárólagos és szakaszon belüli; a `TSK`/`Károli-KH` sornál a csak-igehely nem pár; `ISMERT_HIBA_TSK_VERSSZAM` 13 sor, csak törölt irány; `ATKULCSOLT_SOROK` 27, csak ALVIL-001, csak törölt, csak a 3 régi kulcs.
- **A 32 sor:** 14/2/3/10/3 soronként megszámolva, és az élessel és a próbával összevetve (a fenti megjegyzésekkel).
- **Szúrópróba:** rétegzett (10 + 5 + 5), a horgonyok 5 tételnél word-diffel és a 98f22fc6-tal igazolva.
- **`--helyi-lexicon`:** `realpath` + `normcase`, a repó gyökere és minden alútja tiltott (`general.py:1067-1079`).
- **`ir`:** a J15–J27 30 fájljából az `ir`-en kívül csak koordinációs fájlok.
- **Elavult állítások:** a `zaras.md:8-9, 13-15`, az `NYITOTT:120` (320, Grep-pel igazolva) és a brief `kovetkezo` mezője rendben.
- **Héber 9:** a jelző visszakerült; K13 = 0. **K13b:** a `lexikon/` változatlan.
- **CI:** `futtat.py` a teljes PR-diffre `[ELLENŐRZŐ]` címmel: exit 0, HIBA 0 (E25: 6, E27: 35 JELENTÉS).
- **E17:** a J15–J27-ben csak az `adat/szotar_szerepek.tsv` változott (Δ0, 1 sor).

## Nem ellenőrizhető (az ellenőr parancskörén kívül)

Az osztályozó újrafuttatása (a tényleges párlista); a diff TSV az F9.J18 óta nem számolódott újra, pedig az F9.J23 33 sort módosított (`híd` → `híd, teljes Biblia`); a tesztek, a tiszta klón, a `k9_egyedites`, az `ellenoriz.py` és a `feladatok.py ellenoriz` futtatása.
