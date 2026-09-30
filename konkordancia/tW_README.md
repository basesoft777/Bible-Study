# `tW_szocikkek.tsv` — unfoldingWord Translation Words (F05_SZOTAR_BRIEF.md S14, D20)

*Elfogadva mindkét nyelven S0b.2-ben (`naplok/SZOTAR_S0b_jelentes.md` 4. szakasz);
teljes import S1.4-ben.*

## Forrás

- **Repó:** `git.door43.org/unfoldingWord/en_tw`
- **Tag:** `v91`
- **Commit:** `ff5b3852c27c3a0d01b109e482eb26047dcd20e2`
- **Tarball:** `https://git.door43.org/unfoldingWord/en_tw/archive/v91.tar.gz`
- **SHA-256 (tarball):** `1d2b32da85b97ef4eac5965e40b4952673cdec89a2573d01427342a719bb15be`

**Reprodukáló parancs:**

```bash
python eszkozok/tw_import.py --letolt
```

## Licenc — szó szerint (`LICENSE.md`)

> *unfoldingWord® Translation Words*
>
> *Copyright © 2026 by unfoldingWord*
>
> This work is made available under the Creative Commons Attribution-ShareAlike 4.0
> International License. To view a copy of this license, visit
> [https://creativecommons.org/licenses/by-sa/4.0/](https://creativecommons.org/licenses/by-sa/4.0/)
> or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
>
> unfoldingWord® is a registered trademark of unfoldingWord. Use of the unfoldingWord
> name or logo requires the written permission of unfoldingWord. Under the terms of the
> CC BY-SA license, you may copy and redistribute this unmodified work as long as you
> keep the unfoldingWord® trademark intact. If you modify a copy or translate this work,
> thereby creating a derivative work, you must remove the unfoldingWord® trademark.
>
> On the derivative work, you must indicate what changes you have made and attribute the
> work as follows: "The original work by unfoldingWord is available from
> [unfoldingword.org/utw](https://www.unfoldingword.org/utw)". You must also make your
> derivative work available under the same license (CC BY-SA).
>
> If you would like to notify unfoldingWord regarding your translation of this work,
> please contact us at [unfoldingword.org/contact/](https://www.unfoldingword.org/contact/).

**Következmény a projektre:** a `tW_szocikkek.tsv` és minden belőle vezetett
adat **CC BY-SA 4.0** alatt áll (ShareAlike öröklődik, mint az UBS-eknél,
D17-nek megfelelően). A generált lexikonoldalakon **tilos** az
unfoldingWord® védjegyet feltüntetni (a szöveg maga származékos munka —
akár a magyar fordítással, akár anélkül); a forrásmegjelölés **szó
szerint** a fenti "The original work by unfoldingWord is available from
unfoldingword.org/utw" mondat.

## Fájl

**Generált** (`eszkozok/tw_import.py`, kézzel nem szerkesztendő). Fejléc:
`tw_id kategoria cim strong szoveg forras_commit`.

| Mező | Leírás |
|---|---|
| `tw_id` | `kt/<fájlnév>` vagy `other/<fájlnév>` (a forrás `bible/kt/`, `bible/other/` alkönyvtára + a `.md` fájl alapneve, kiterjesztés nélkül). |
| `kategoria` | `kt` (kulcsfogalmak) \| `other`. |
| `cim` | A szócikk `# ...` szintű címsora. |
| `strong` | A „Word Data” szakasz `* Strong's: ...` sorából kinyert, **normalizált** (4 jegyű, nullázott) Strong-kódok listája, `+`-jellel elválasztva. A héber kódok a forrásban is 4 jegyűek; a görög kódok **5 jegyűek** (4 jegyű alapszám + záró "jelentés-változat" számjegy, l. `naplok/SZOTAR_S0b_tw.tsv` (a) pontja) — a normalizálás az 5. számjegyet levágja. Üres, ha a szócikk nem hivatkozik Strong-kódra (16 ilyen a 598-ból). |
| `szoveg` | A teljes markdown-szöveg, `\n`-nel escapelt sortörésekkel és szóközzé cserélt tab-karakterekkel (a TSV egy fizikai sor marad). |
| `forras_commit` | A fenti commit-hash, minden soron azonos. |

**Mért érték (2026.09.28):** 598 sor (190 `kt`, 408 `other`). Lefedettség a
D28 hatókör 26 héber / 13 görög tokenjén: **héber 21/26**, hiányzik
`H0922` (*bohu* — maga a T2.2 új tokenje), `H6093`, `H7496`, `H8004`,
`H8415`; **görög 10/13**, hiányzik `G0282`, `G0813`, `G5010` — pontosan
egyezik az S0b.2 méréssel (`naplok/SZOTAR_S0b_jelentes.md`).

## Ismert korlát

**A Strong-kód normalizálása feltételezi, hogy minden görög kód pontosan
5 jegyű** (a forrásban megfigyelt minta). Ha egy jövőbeli tW-kiadásban
ettől eltérő hosszúságú kód jelenne meg, a `normalize_strong()` hibásan
vágná le — a szkript ezt NEM ellenőrzi le mechanikusan (nincs asszertálás
a bemeneti hosszra). Egy korábbi verzió (a leadó zérók levágásával a
regexben) ezt a hibát ténylegesen el is követte 2 tokenre (`G0012` →
tévesen `G0120`) — javítva, a teljes lefedettségi számot az S0b.2
jelentéssel összevetve ellenőriztem.