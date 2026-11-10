# F105 — a BDB héber idézeteinek szórendje: mérés, gépi egyezés, 50-es minta (FELADATOK #105)

*2026-11-10. Modell: `claude-opus-5-5`. Ág: `claude/f105-bdb-szorend`. Csak mérés és minta: a forrás, az adat, a
megjelenítés és a lexikon nem változott. Mérőszkript: `naplok/F105_meres.py` (kb. 10 mp), minta: `naplok/F105_minta.py`.*

*proveniencia: scope=BDB_teljes_unabridged.tsv minden szócikkének többszavas héber futama (29 469) | forras=naplok/F105_meres.py@49a9f39bea4a;
konkordancia/BDB_teljes_unabridged.tsv@d4b15b2faea6, konkordancia/TAHOT_kivonat.tsv@4c876f570aad, adat/bdb_vers_jelentes.tsv@17a27594fd5e,
adat/bdb_forras_javitas.tsv@834be5c1ee6e, eszkozok/bdb_rovidites.py@64c639fe67b0, eszkozok/olvaso_szerver/bdb_szelet.py@180ed181fb02 | ts=2026-11-10*

## 1. Kiinduló lelet: a brief tárgyának nagy része a DT445 óta él

A brief (v1, 2026-10-15) óta a szórend-javítás elkészült és élesben van: a DT445 (N-F131y, 2026-11-01;
`naplok/BDB_HEBER_SORREND_meres.md`) a javítótáblán (`adat/bdb_forras_javitas.tsv`, `heber_sorrend`: `javitva` 14 976,
`valodi_sorrend` 224, `jelolt_marad` 21 052) és a megjelenítésben (`eszkozok/bdb_rovidites.heber_sorrend_javit`, amelyet az
olvasó `blokkok._rovidites` és a lexikon-generátor is hív). A gépi ellenőrzés ott **bármely** TAHOT-versen futott; a brief
módszere, a **hivatkozott** vers (`adat/bdb_vers_jelentes.tsv`), új. Nincs megoldva: a `jelolt_marad` tételek, és a
rafe mint maqqéf-pótló (U+05BF; az N-F131y szerint „külön mérendő”).

## 2. Mérés (a brief 1. lépése)

**Módszer.** Futam: a szeletelő `lapit` alakjában legalább két, szóközzel tagolt héber token. A futamot akkor tekintem
TAHOT-tal ellenőrizhetőnek, ha közvetlenül (legfeljebb írásjel, zárójel, „&c.” után) hivatkozás követi, amelynek a
vers → jelentés táblában Károli-verse van, és nincs kiszűrve. Próba a vers TAHOT-vázfolyamán (mássalhangzók, végbetű
alapbetűre, pe/mem egybevéve; teljes szó = betűi, rövidítés = betűi + legfeljebb 8 betű rés, ellipszis legfeljebb 60).
Három alakot vetek össze: **F** a forrás, **M** a mai megjelenítés (DT445 csere), **R** a lexikon nélküli R_hib (geres
nélkül a tokenek megfordítása, geresnél a DT445 `r_str`-je, `eszkozok/bdb_jelolt/heber_sorrend.py`).

| Mi | Szám |
|---|---:|
| többszavas héber futam | **29 469** |
| — geres nélkül / geresszel | 19 242 / 10 227 |
| — rafe-maqqéffel egybeírt tokennel | 2 891 |
| DT445 szerint: `javitva` / `valodi_sorrend` / `jelolt_marad` / részleges / nincs sora | 14 744 / 216 / 11 437 / 139 / 2 933 |
| **TAHOT-tal ellenőrizhető** (hivatkozott, nem kiszűrt vers követi) | **17 953 (60,9%)** |
| — kevés anyag (nincs egy teljes szó és még egy egység) | 135 |
| — a vers nem dönt (sem F, sem R nem illeszkedik: nem szó szerinti idézet, plene/defektív írás, osztott rövidítés) | 5 510 |
| — **eldönthető** | **12 308** |

## 3. Gépi egyezés a hivatkozott versen (a brief 2. lépésének mérése)

| Ítélet (az eldönthető 12 308-on) | Szám | Állapot a DT445 szerint |
|---|---:|---|
| M illeszkedik (a mai megjelenítés egyezik a verssel) | **10 483 (85,2%)** | ebből `javitva` 8 369, a többi változatlanul is jó |
| M nem illeszkedik, R igen (**javítható**) | **1 825 (14,8%)** | `jelolt_marad` 1 748, nincs sora 69, részleges 6, `valodi_sorrend` 2 |

- **A DT445 `javitva` cseréit a hivatkozott vers sehol nem cáfolja:** ahol dönt, 8 369 / 8 369 egyezik.
- **A szabály (R) pontossága a forrással szemben**, ahol a vers csak az egyiket illeszti: R helyes 10 194, F helyes 89
  (**99,1%**). A 89-ből 44 a DT445 `valodi_sorrend` sora (ott a forrás marad), 45 `jelolt_marad` / nincs sora / részleges.
  Hivatkozott-vers-vétóval (csak ahol a vers R-t igazolja, F-et nem) ez a 89 nem romlik el.
- **Ütközés** (DT445 `valodi_sorrend`, de a hivatkozott vers R-t igazolja): 2 sor, `naplok/F105_utkozes.tsv`.
- Ha az 1 823 jelöltet (a nem javított `jelolt_marad` / nincs sora / részleges, `F0_M0_R1`) a megjelenítés javítaná, az
  eldönthető futamokon a megjelenítés és a vers egyezése 85,2%-ról 99,98%-ra nőne (a maradék a 2 ütközés). *(Ez a szám a
  jelölt halmaz definíciójából következik; a valódi próbája az 50-es kézi minta, 4. szakasz.)*

**Maqqéf.** A rafe-maqqéf (`מִןהָֿאָרֶץ` = מִן־הָאָרֶץ) a megjelenítésben ma sehol sincs feloldva (a `bdb_rovidites.py`-ban
és a `blokkok.py`-ban nincs rá szabály). 2 891 többszavas futamot érint (az egytokenes alakokkal együtt a DT445 mérése
szerint 5 589 kifejezést). A minta helyreállított alakja a feloldást is mutatja (a rafét hordozó, nem első betű elé U+05BE, a
rafe ki, az előző betű végbetűre).

## 4. Megállás: hatóköri döntés (DT-F105a) és ⛔ 50-es minta

A brief 2. lépése egy új, az olvasóba kötött szabálymodult (`eszkozok/olvaso_szerver/bdb_szoerend.py`) ír elő. A DT445 óta
a szórend szabálya és a csere egy helyen él (javítótábla + `bdb_rovidites`, a lexikonlap és az olvasó közös útja); egy
második, csak az olvasóban futó szabály ugyanazt a futamot kétszer fordíthatná meg, és a lexikonlap eltérne az olvasótól.
Ezért a megvalósítás előtt megálltam: **DT-F105a** (`dontesek/uj/f105-bdb-szorend.md`). A `blokkok.py`, a
`teszt_olvaso_szerver.py` és a `bdb_szoerend.py` nem változott, a `KETRETEGU_BDB_KARTYA` kapcsolóhoz nem nyúltam.

A ⛔ 50-es minta (5. szakasz) a fenti 1 823 jelöltből készült. Bármelyik változat ezeket javítaná újonnan, így a minta
jóváhagyása a döntéstől független.

## 5. ⛔ Az 50-es kézi minta

Seed 105, véletlen 50 az 1 823 jelöltből, Strong és pozíció szerint. „nyers forrás”: a `BDB_teljes_unabridged.tsv` futama;
„helyreállított alak”: a lexikon nélküli R_hib, utána a rafe-maqqéf feloldása (csak itt: a megjelenítés nem változott);
„vers”: a hivatkozás Károli-kulcsa; „a vers héber szövege”: a Macula szavai a Károli-versen (csak olvasásra, a maqqéf nélkül;
a gépi ellenőrzés a TAHOT-on fut). A „kézi ítélet” (helyes / rossz / nem tudom) a független ellenőré vagy a felhasználóé.
Újragenerálás: `python naplok/F105_meres.py --ki <kvt>`, majd `python naplok/F105_minta.py --be <kvt> --ki-md <fájl> --ki-utkozes naplok/F105_utkozes.tsv`.

