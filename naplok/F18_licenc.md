# F18 — Nave-import: licenc-ellenőrzés (1. lépés) — ⛔ megállás

*Ág: `claude/nave-import` · 2026.09.30 · a számok forrása: `naplok/F06_nave.tsv`, `naplok/F06_forras_jelentes.md` (PR #75), újraellenőrizve friss klónon.*

## Forrás és verzió

| Forrás | Commit | Licenc-hely | Licenc |
|---|---|---|---|
| `theonize/bible_database` | `0df2f9928358926f94a6d0db5e823a3a73280339` | `LICENSE` 1–2. sor | GNU GPL v3 (29 June 2007). A `README.md` („Database of open-source Bible texts and topical and cross references”) a Nave-eredetet nem nevezi meg. |
| `basokant/nave` | `4f35c7d4ffd4933f4db1b9d5182db90dc04bd235` | nincs LICENSE-fájl; `README.md` | Csak a README állítja: a mű (Nave, 1897) „in the public domain”. A repó adatfájljaira (`data/parsed-nave.json`, lekaparás) külön licenc nincs. |
| `elcafe7/lex` | — | — | Nem importáljuk (a brief szerint). |

## Ütközés

- A repó (`basesoft777/Bible-Study`) **nyilvános**, és nincs LICENSE-fájlja (`gh repo view`: `licenseInfo: null`).
- `Rendszerfejlesztesi_playbook.md` 2. pont, licenc-táblázat: a GPL 3.0 forrás **„NEM építendő be publikus repóba — copyleft-kockázat, más licencű adatokkal ütközhet”**. A theonize importja (32 253 sor + 92 609 reláció a `konkordancia/`-ba) ezt a szabályt közvetlenül sértené.
- A repóban már van share-alike adat (SDBH/SDGNT, CC BY-SA 4.0); a GPLv3-mal való keverés külön jogi kérdés (F24, D41).
- A Nave-tartalom közkincs (1897), de a theonize szerkezete/feldolgozása GPLv3 alatt áll; a licenclánc (ki vitte át és milyen jogcímen) dokumentálatlan.

**Döntés: ⛔ megállás.** Az import (2. lépés) és az eredet-ellenőrzés (3. lépés) nem indult; adat/ és konkordancia/ nem változott. A Gemini-költség 0 USD.

## Döntési opciók az orkesztrátornak

1. **Nem importáljuk a theonize-t**; a `basokant/nave` (közkincs-állítás, lekaparás) az egyetlen import-jelölt. Hátrány: a téma↔vers reláció számát nem mértük (JSON belső szerkezete), 5322 elem a 4980 témával szemben; saját parszolás kell. *Javaslat.*
2. A theonize importja **csak helyi, nem verziózott** elemzéshez (az eredet-ellenőrzés a basokant ellen), a repóba nem kerül be; csak a mérőszámok. Jogilag óvatosabb, de a kimenet (témák) nem lenne a repóban.
3. A repó GPLv3 alá helyezése (vagy jogi tisztázás, F24) után teljes import. Nem javasolt a kereskedelmi/nyilvános cél (D41) miatt.

## Nyitott

- Az FJ4-hez képesti számeltérés (32254/4951/92610 vs. 32253/4980/92609) oka tisztázatlan (F06: a mostani mérés az irányadó); a friss klón `Topics.csv`/`TopicIndex.csv` sorszámai az F06-tal egyeznek-e, itt nem mértük újra.
- Folytatási pont: a döntés után a 2. lépés (import) vagy, az 1. opciónál, a basokant parszolása.
