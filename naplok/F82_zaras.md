# F82 TERV_FELADAT_OR — zárójelentés

*FELADATOK #82 · M1–M3 · 2026.10.08 · ág: `claude/f82-terv-feladat-or` · modell: sonnet · a saját munkámat nem minősítem ellenőrzöttnek (a `fuggetlen-ellenor` az orkesztrátoré)*

## Mi készült

- **Döntés:** DT79 (helyőrző, 🟢): jelölőpár `oszlop=` attribútummal; jelölt táblák: ATALAKITASI 13.4 és MUNKATERV 4. (felhasználó, 2026-10-08, chat). Felmérés: `naplok/F82_M0.md`.
- **Szabály (M1):** `eszkozok/feladatok.py` `terv_mutato_hibak()`, az `ellenoriz` hibalistájába kötve (így fut az E18-ban és a `/kovetkezo` 1. lépésében). Jelölő: `<!-- TERVELEM-MUTATO [oszlop=a,b] -->` … `<!-- /TERVELEM-MUTATO -->`, külön sorban. A vizsgált cellák összefűzött szövegében legalább egy: létező `#nn`; brief-`kod` (az `\_` → `_` visszaalakítás után); létező DT-/D-tétel (`DONTESEK.md`, `FELADATOK.md`); `elavult` / `feltételes` / `lezárva`. Hiba: `fájl:sor`, a sor első cellája, a vizsgált szöveg. Külön hiba: hiányzó záró jelölő, záró jelölő nyitó nélkül, nincs tábla a jelölőpár között, ismeretlen `oszlop=`. A `csv` modul nincs használva; a terv-fájlok CRLF-je kezelve.
- **Tesztek:** `TervMutatoTest` (12 teszt) az `eszkozok/teszt_feladatok.py`-ban: jó sor `#nn`-nel; `kod`-dal (`SQLITE\_EPIT`); `feltételes`/`elavult`/`lezárva`; DT-hivatkozás (létező és nem létező); nem létező `#99` → HIBA a pontos sorral; jelölőn kívüli `#205` és `SECE_H` → nem számít; hiányzó záró jelölő → HIBA; záró nyitó nélkül; jelölőpár tábla nélkül; többoszlopos `oszlop=#,név`; ismeretlen oszlop; CRLF; és a valódi repó 0 találata.
- **Jelölők (M2):** ATALAKITASI 13.4 (`oszlop=feladat`, a formátum leírása a bevezető mondatban) és MUNKATERV 4. (`oszlop=#,név`); a táblák tartalma nem módosult, új feladat nem született. A MUNKATERV 4a és az ADATVAGYON 21. kimarad (DT79).

## Ellenőrzés (saját futtatás, `manual`: a menet maga futtatta, nem független ellenőrzés)

| Parancs | Eredmény |
|---|---|
| `python eszkozok/feladatok.py ellenoriz` | 102 brief, 0 hiba, 0 figyelmeztetés |
| `python eszkozok/feladatok.py ellenoriz --pr-alap origin/main` | 0 hiba |
| `python eszkozok/teszt_feladatok.py` | 111 teszt, OK |
| `python eszkozok/ellenoriz.py` | SÉRTÉS 0 (RENDBEN 11, KÉZI 2, JELENTÉS 3), exit 0 |
| `python eszkozok/ellenorzes/futtat.py --teljes` | exit 0 |
| negatív próba (ideiglenes másolat, a 13.4 egyik sora `#78 …` → szöveg) | `HIBA ATALAKITASI_TERV.md.md:1003 terv-mutató: …` |

## Nyitva az orkesztrátornak / felhasználónak

- A `.claude/commands/kovetkezo.md` 16. sorában a „(az őrt a #82 vezeti be)” szöveg törölhető, ha a #82 merge-elt (a brief 3. pontja szerint nem a #82 `ir`-je, ezért nem nyúltam hozzá).
- A MUNKATERV 4a „Tervezett” táblájában a `SZPA_AUDIT` sor jelölés nélküli (nem jelölt tábla, ezért nem hiba); a #52 hatóköre.
- A `fuggetlen-ellenor` futtatása és a merge a felhasználóé / az orkesztrátoré.
