# /lap-javit HAMART-001 — gépi versellenőrzés az egybeírt prózán

*2026-11-11 · a felhasználó döntése (az orkesztrátor továbbításában): „mehet az egybeírás”, gépi versellenőrzéssel. Tárgy: a kézi forrás (`motivumok/HAMART-001.md`) négy egybeírt értelmező rése (kivonat, miert_fontos, ertelmezes, modszertan).*

## 1. Gépies rész (szkript)

- `naplok/HAMART_lapjavit_versellenorzes.py`:
  - mondatonként kigyűjti az igehely-hivatkozásokat: 71 mondat, 174 hivatkozás;
  - összeveti a „…” idézetet a közvetlenül utána hivatkozott Károli-verssel (betűhíven);
  - ellenőrzi, hogy a mondatban megnevezett héber vagy görög szó (árar, adámá, erec, chámász, sáchat, qalal, kéc, málé, sámá …) Strong-száma legalább egy hivatkozott versben áll-e (TAHOT, TAGNT; kulcs: a Károli-vers);
  - ellenőrzi, hogy a vers létezik-e.
- Első futás: 7 eltérés. Ebből 2 javítva:
  - az 1Móz 6:12 „útja” helyett betűhív idézet: „megrontotta vala az ő útát”;
  - az 1Móz 6:13, 6:17 „elveszti” helyett: „elvesztem őket”, „elveszessek”.
- Maradt 5, mind átnézve, mind téves riasztás:
  - „a föld színe” fogalom-idézet, a BDB jelentéscímkéje, nem versidézet;
  - a sámá a 6:11-nél azért nincs, mert a mondat éppen azt mondja ki, hogy a Genezisben nem áll;
  - az árar az 1Móz 8:21-nél azért nincs, mert a mondat azt mondja ki, hogy ott nem az árar áll;
  - a Róm 8:21-es mondat árar/qalal szava az 1Móz 8:21-re vonatkozik (a Vitatott pontok kérdése).

## 2. Második kéz (Sonnet-subagent, `claude-sonnet-5-5`, a versszöveggel és a TAHOT/TAGNT-sorokkal)

Ellenőrzött mondat: 71, eltérés: 12. A javított mondatok a forrásban és a változáslistában jelölve.

| # | Hely | Eltérés | Javítás |
|---|---|---|---|
| 6 | Kivonat | a Jer 51:46-ban nem az erőszak, hanem az erőszakról szóló hír hallatszik | „háromféleképpen: maga az erőszak hallatszik (Jer 6:7), az erőszakról szóló hír hallatszik (Jer 51:46), vagy a miatta kiáltó szó nem talál meghallgatásra (Hab 1:2)” |
| 8 | Kivonat | a Sof 1:2-3 nem „ismétli” a felsorolást (hal és más is áll benne), és az 1Móz 6:7 nem volt hivatkozva | „az özönvíz előtti ítélet felsorolásából az embert, a barmot és az ég madarait hozza vissza (1Móz 6:7)” |
| 11 | Miért fontos, árar | az „egyetlen hely tér el” hatóköre félreérthető (a 12:3 is más igealak) | „A törzs egyetlen helyen más: Lámek mondatában …” |
| 17 | Miért fontos, iccávón | a 3:16-ban a viselősség fájdalma | „a viselősség fájdalmát (1Móz 3:16)” |
| 24 | Miért fontos, görög | a „földjét” alak nincs a versben | „a Jel 11:18-ban álló »földet«” |
| 39 | Értelmezés, Remez | a tövis és bogáncs genezisi helye nem volt hivatkozva | „(1Móz 3:18)” |
| 41 | Értelmezés, Remez | a Jel 19:2 és az 1Móz 6:11 azonossága csak a Septuagintán át áll | „ugyanazzal a görög igével (φθείρω, ftheiró) szól, amellyel a görög Ószövetség az 1Móz 6:11 mondatát fordítja” |
| 44 | Értelmezés, Remez ÚSZ | a Genezis-vers nem volt hivatkozva | „(1Móz 3:17-18)” |
| 46 | Értelmezés, Remez ÚSZ | a két helyen két különböző görög ige áll | „a romlás szócsaládjának igéjével” |
| 48 | Értelmezés, Drash | következtetés, amelyet a vers nem mond | nem javítva: a Drash a lap kimondott olvasata („A lap olvasata három tételben”), a következtetés oda tartozik (lektor 30.) |
| 64 | Módszertan, TR | a STEPBible TR-adata κατάθεμα | mindkét forrás megnevezve: a kritikai kiadások és a STEPBible TR-adata κατάθεμα, a Thayer címszava a Textus Receptus egy kiadásának κατανάθεμα alakja (`adat/thayer_szakaszok.tsv` G2652) |
| 71 | Módszertan, Nyitott 4. | az „átok feltételes” olvasat a Gal 5:3-ra hivatkozott, amely kötelezettségről szól | „a törvény cselekedeteiből valókra szól (Gal 3:10), és aki körülmetélkedik, »köteles az egész törvényt megtartani« (Gal 5:3)” |

Versszöveg alapján nem ellenőrizhető (a második kéz szerint is):
- a szótári felosztások (BDB, Thayer);
- a keresések számai (577, 42, „tizenegy hely”), ezek a forrás proveniencia-soraiból jönnek;
- a forráskritikai mondat (Carr).
