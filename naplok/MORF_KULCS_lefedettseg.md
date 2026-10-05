# MORF_KULCS lefedettség (eszkozok/morf_feloldas.py --lefedettseg)

*proveniencia: scope=konkordancia/Macula_heber_*.tsv (morf oszlop) + adat/morf_kulcs_heber.tsv + adat/morf_nyelv_aramai.tsv | forras=a fenti táblák (OSHB-jelkulcs, Macula lowfat lang) | ts=2026-10-05*

- Szó (morféma) összesen: 475911; különböző kód: 747; (kód, nyelv) pár: 892; arámi szó: 7549; az arámi-táblázat morf-értéke a Macula-táblától eltér: 0 szón.

## 1. A szó tényleges nyelvével ((kód, nyelv) pár)

| állapot | pár | szó |
|---|---|---|
| teljes | 874 | 473228 |
| helykitoltovel | 18 | 2683 |
| reszleges | 0 | 0 |
| ismeretlen | 0 | 0 |

A `helykitoltovel` állapot: minden jel a táblából feloldva, de legalább egy pozíció a forrás szerinti `x` (ismeretlen vagy szükségtelen érték). Nem teljes feloldás, külön számolva.

Ebből `x` helykitöltőt tartalmaz (a forrás szerint „ismeretlen vagy szükségtelen érték”): 18 pár, 2683 szó.

Részlegesen vagy nem feloldott párok:

| kód | nyelv | szó | kimenet |
|---|---|---|---|
| `Pdxms` | H | 1190 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: hímnem; szám: egyes szám |
| `Pdxcp` | H | 755 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: közös (ige); szám: többes szám |
| `Pdxfs` | H | 611 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: nőnem; szám: egyes szám |
| `Pdxms` | A | 51 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: hímnem; szám: egyes szám |
| `Pdxfs` | A | 13 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: nőnem; szám: egyes szám |
| `Pdxmp` | A | 12 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: hímnem; szám: többes szám |
| `Pfxcs` | A | 8 | névmás; típus: határozatlan; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: közös (ige); szám: egyes szám |
| `Pdxcp` | A | 7 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: közös (ige); szám: többes szám |
| `Nxxxa` | A | 7 | főnév; típus: ismeretlen vagy szükségtelen érték helykitöltője; nem: ismeretlen vagy szükségtelen érték helykitöltője; szám: ismeretlen vagy szükségtelen érték helykitöltője; állapot: abszolút |
| `Pdxcs` | A | 7 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: közös (ige); szám: egyes szám |
| `Pfxbs` | A | 5 | névmás; típus: határozatlan; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: mindkettő (főnév); szám: egyes szám |
| `Pdxcs` | H | 4 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: közös (ige); szám: egyes szám |
| `Prxcs` | A | 4 | névmás; típus: vonatkozó; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: közös (ige); szám: egyes szám |
| `Pdxbp` | A | 3 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: mindkettő (főnév); szám: többes szám |
| `Pdxmp` | H | 3 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: hímnem; szám: többes szám |
| `Pdxbs` | A | 1 | névmás; típus: mutató; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: mindkettő (főnév); szám: egyes szám |
| `Pixbs` | A | 1 | névmás; típus: kérdő; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: mindkettő (főnév); szám: egyes szám |
| `Pixcs` | A | 1 | névmás; típus: kérdő; személy: ismeretlen vagy szükségtelen érték helykitöltője; nem: közös (ige); szám: egyes szám |

## 2. Nyelv nélkül (csak a kód)

| állapot | kód | szó |
|---|---|---|
| teljes | 734 | 473228 |
| helykitoltovel | 13 | 2683 |
| reszleges | 0 | 0 |
| ismeretlen | 0 | 0 |

Kétértelmű (a törzs jele mindkét nyelvben szerepel, más megnevezéssel): 377 kód, 68668 szó; ebből tényleg arámi szó: 1014. Nyelv nélkül ezek mindkét olvasatot kapják, `[nyelv ismeretlen]` jelzéssel.

## 3. A héber olvasatban nem teljesen feloldott kódok (az M0 nem illeszkedő kódjai és az x-helykitöltősök)

| kód | héber olvasat | szó héberként | szó arámiként | arámi olvasat |
|---|---|---|---|---|
| `Pdxms` | helykitoltovel | 1190 | 51 | helykitoltovel |
| `Pdxcp` | helykitoltovel | 755 | 7 | helykitoltovel |
| `Pdxfs` | helykitoltovel | 611 | 13 | helykitoltovel |
| `Pdxmp` | helykitoltovel | 3 | 12 | helykitoltovel |
| `Pdxcs` | helykitoltovel | 4 | 7 | helykitoltovel |
| `Pfxcs` | helykitoltovel | 0 | 8 | helykitoltovel |
| `Nxxxa` | helykitoltovel | 0 | 7 | helykitoltovel |
| `Vec` | reszleges | 0 | 5 | teljes |
| `Pfxbs` | helykitoltovel | 0 | 5 | helykitoltovel |
| `Varmsa` | reszleges | 0 | 5 | teljes |
| `Vep3ms` | reszleges | 0 | 4 | teljes |
| `Prxcs` | helykitoltovel | 0 | 4 | helykitoltovel |
| `Varmpa` | reszleges | 0 | 3 | teljes |
| `Vei3ms` | reszleges | 0 | 3 | teljes |
| `Varfsa` | reszleges | 0 | 3 | teljes |
| `Vai3mp` | reszleges | 0 | 3 | teljes |
| `Pdxbp` | helykitoltovel | 0 | 3 | helykitoltovel |
| `Vai2ms` | reszleges | 0 | 2 | teljes |
| `Vep3mp` | reszleges | 0 | 2 | teljes |
| `Vai3ms` | reszleges | 0 | 2 | teljes |
| `Vai3fs` | reszleges | 0 | 2 | teljes |
| `Vav2ms` | reszleges | 0 | 1 | teljes |
| `Vap3ms` | reszleges | 0 | 1 | teljes |
| `Pdxbs` | helykitoltovel | 0 | 1 | helykitoltovel |
| `Vermsa` | reszleges | 0 | 1 | teljes |
| `Varfpa` | reszleges | 0 | 1 | teljes |
| `Vssmpa` | reszleges | 0 | 1 | teljes |
| `Vav2mp` | reszleges | 0 | 1 | teljes |
| `Pixbs` | helykitoltovel | 0 | 1 | helykitoltovel |
| `Pixcs` | helykitoltovel | 0 | 1 | helykitoltovel |

