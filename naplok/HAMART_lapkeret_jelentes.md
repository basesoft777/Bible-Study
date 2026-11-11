# HAMART-001 lapkeret — a lap eleje és a Kolofon (F182.67): jelentés

*Ág: `claude/hamart-lapkeret` (az `origin/main` 3565fe5f-ről). Végrehajtó: claude-opus-5-5. Dátum: 2026-11-11. Kiindulás: a felhasználó jelzése a HAMART lap elejéről és végéről, az orkesztrátor továbbításában; még a `/kiadas` előtt, generátorszinten. Ez a jelentés nem minősíti a munkát ellenőrzöttnek.*

## Mi változott (csak az új szerkezetű lapon, `uj_szerkezet`; a régi lapok kimenete változatlan)

1. **A lap eleje — egyszerűsített kolofon** (DT-F182s; a felhasználó: „a motívum megfogalmazása / negatív elhatárolás / fölérendelt fogalom ahogy a régiben volt — a legvégén a teljes”). A cím alatt: **A motívum.** (a teljes cím) · **Negatív elhatárolás.** (a negatív kritérium) · **Fölérendelt fogalom** (egy mondatos magyarázattal) · mutató a Kolofonra. A „régi” forma keresése: a git-történetben prózai változat nem volt; a régi törzscikkben és az első lexikonlapon („0. Metaadatok”) a lap ELEJÉN kulcs–érték tábla állt, benne a negatív kritériummal és a fölérendelt fogalommal (ELLENOR_HAMART_lapkeret 2.: az első változat „a Kolofon táblájában állt” állítása hamis volt). Ezért a három mező olvasói alakban áll, a szövegük a motívumtábla adata (`lexikon_general.egyszerusitett_kolofon`).
2. **A Kolofon táblája — a teljes azonosító adat:** ID, rövid cím, teljes cím, téma, PaRDeS-szint, státusz (a kiadási állapotból), azonosság típusa, negatív kritérium, fölérendelt fogalom; utána a sablon-megfelelőség és a kiadás sorai. A „Kézi forrás” és a „Kereszthivatkozás-napló” belső sora kikerült.
3. **A Kolofon licencei** (`olvasoi_licencek`, a forrástáblában és a 12. Irodalom „Adatforrások” listájában): a nyílt adatmagban (CC BY 4.0) kiadott saját adat — a motívumtábla, az előfordulás-tábla, a jelöltek döntésnaplója, a kapcsolat-tábla, a motívumközi kapcsolatok, az elutasítási okok (`nyilt_mag_export.py` forrásai) — „CC BY 4.0 (a nyílt adatmagban)”; a Károli–Strong párosítás CC BY 4.0 (DT623, `Karoli_Strong_parok`); a fordítástábla: „a forrásszöveg közkincs; a magyar fordítás: minden jog fenntartva”. A nyílt magba nem kerülő saját táblák (pl. a Károli-szavak szótári alakjai, a versmegfeleltetés, az LXX-döntések táblája) licence „minden jog fenntartva” marad — ez igaz.
4. **Módszertani elvek:** a bekezdés eddig egy link-címet hordozott („[A módszer Hays hét kritériumának tükrében](…)”), amely olvasóként kitöltetlen helyőrzőnek látszott. Helyette saját szavas próza a közlemény (`kozlemeny/HAYS_LEKEPEZES.md`) táblája szerint: mit fed a módszer Hays hét kérdéséből, mit részben, mit nem; a közlemény címe idézőjelben, link-szintaxis nélkül.

**A szerző neve, a lexikon címe és a kanonikus cím:** az F182.67-ben még helyőrző volt; a felhasználó értékeivel az F182.68 vezette át (l. lent).

## Ellenőrzés (helyben)

- `ellenoriz.py`: 0 SÉRTÉS (27 RENDBEN). Olvasói kapu (HAMART-001): 0 BUKÁS.
- `teszt_kesz_lap_hamart` 36/36 (az A02-teszt az új formára; új: a saját adat licence, a Módszertani elvek prózája), `teszt_hatastortenet` OK, `teszt_gyokerok_kapuk` OK, `teszt_olvasoi_kapu` 68/69 (az `Arany.G7` az alapvonalon is bukik).
- A lexikon/ alatt csak a HAMART-001 lapja változott.

## F182.68 — az idézés adatai, egy idézési forma, nyers helyőrző nélkül (a felhasználó döntései, 2026-11-11; DT-F182t)

- **Szerző és cím:** „Demeter Tamás”, „Logosz Lexikon” (`SZERZO_NEV`, `LEXIKON_CIM`).
- **Kanonikus cím:** egyetlen beállítás, `KANONIKUS_ALAP_URL` = https://logoszlexikon.hu; a szócikk állandó címe https://logoszlexikon.hu/HAMART-001, a kiadás változatcíme `…/HAMART-001/<kiadás>` (a kiadáskor). Üres beállításnál: „a lap állandó webcíme az első nyilvános megjelenéskor kerül ide”.
- **DOI:** az adatban nincs (a `CITATION.cff` szerint a nyílt mag Zenodo-közlése után kerül be); a lapon: „a nyílt adatkészlet DOI-ja az első Zenodo-közléskor kerül ide” (`NYILT_ADAT_DOI` üres).
- **Egy idézési forma:** a Kolofon „Hogyan idézd” bekezdése (Demeter Tamás: *Logosz Lexikon*, „<cím>” (<ID>), <kiadás>, <dátum>, <cím>); a 12. Irodalom „Hogyan hivatkozz” listája helyett mutató; a generálás dátuma a Kolofon táblájában (a státusz ott állt).
- **A Kolofon hatókör-mondata** olvasói („motívumtábla” nélkül).
- **Kapu:** olvasói kapu HELYORZO (BUKÁS, csak az új szerkezetű lapon): „<KANONIKUS_FORRAS_URL>”, „[HELYŐRZŐ…]”, „<DOI>”, üres „DOI: .”; teszt a rontott másolattal (`teszt_kesz_lap_hamart.test_idezes_egy_helyen_helyorzo_nelkul`); SEMA 3.11 újragenerálva.
- **Jelzés (hiány):** a „Nyilatkozat a mesterséges intelligencia használatáról” a lapon relatív linkkel a közleményre mutat (`../kozlemeny/MI_NYILATKOZAT.md`); a szöveg nem a lap része, és a nyilvános webcíme még nincs eldöntve (a közlemények kanonikus címe a nyitóoldal-tétel része). A régi lapok és a nyílt mag, a CITATION.cff, a közlemények: nem változtak (külön tétel).

Ellenőrzés: `ellenoriz.py` 0 SÉRTÉS; olvasói kapu 0 BUKÁS; nyílt mag kapu 0 BUKÁS; `teszt_kesz_lap_hamart` 37/37, `teszt_ellenoriz_35` OK, `teszt_gyokerok_kapuk` OK, `teszt_hatastortenet` OK, `teszt_olvasoi_kapu` 68/69 (az `Arany.G7` az alapvonalon is bukik).

## F182.70 — a nyílt mag DOI-ja egy beállításból (a felhasználó, 2026-11-11: Zenodo-feltöltés „még nem volt”)

- `NYILT_MAG_DOI` (üres alapértékkel; a HAMART kiadása utáni Zenodo-közléskor a concept DOI ide kerül). Amíg üres, a „Hogyan idézd” mondata: „A lap adatai (előfordulások, kizárt helyek) nyílt adatkészletként is megjelennek; az adatkészlet DOI-ja az első Zenodo-közléskor kerül ide.”; DOI-val: „… nyílt adatkészletként is elérhetők: DOI: <doi>.”
- Az `ellenoriz.py` 35. szabálya a két alak közös elejét keresi (a régi „… is elérhetők” literál helyett); a HELYORZO-kapu az üres „DOI: .” alakot nem engedi. `ellenoriz.py` 0 SÉRTÉS; `teszt_ellenoriz_35` OK; `teszt_kesz_lap_hamart` OK; olvasói kapu 0 BUKÁS.

## Javítókör (ELLENOR_HAMART_lapkeret, egy kör; F182.72)

| # | Tétel | Javítva |
|---|---|---|
| 1 | a fordítástábla és az előfordulás-tábla licencsora | igen: a fordítástábla „a magyar fordítás: minden jog fenntartva; a lefordított szótárszöveg licence a szótár saját soránál áll” (az UBS-glosszák CC BY-SA 4.0 forrása a saját sorában); az előfordulás-tábla „az adatoszlopok CC BY 4.0, a nyílt adatmagban; az igehelyenkénti magyarázat: minden jog fenntartva” (a nyílt mag a magyarázatot nem adja ki) |
| 2 | a „régi forma” premisszája | a DT-F182s és ez a jelentés helyesbítve (a régi lapokon a lap elején kulcs–érték tábla állt); a forma (bekezdés vagy háromsoros tábla) a felhasználó kérdése, az orkesztrátoron át |
| 3, 6 | generátorszintű teszt rontott bemenettel | igen: `test_olvasoi_licencek_generator`, `test_egyszerusitett_kolofon_az_adatbol` (a `motivumok.tsv`-vel összevetve; üres mezőre „—”) |
| 4 | az A02 leírása | igen |
| 5 | halott kód, elavult megjegyzések | igen: az `azonosito_tabla()` törölve, a megjegyzések az új formára |
| 7 | kettős zárójel | igen: „CC BY 4.0, a nyílt adatmagban” |

Ellenőrzés: `ellenoriz.py` 0 SÉRTÉS; olvasói kapu 0 BUKÁS; `teszt_kesz_lap_hamart` 39/39, `teszt_ellenoriz_35`, `teszt_gyokerok_kapuk`, `teszt_hatastortenet` OK.
