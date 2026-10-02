# F35 M0 — felmérés (csak olvasás)

## „Sir” = Siralmak (migrálandó vagy döntésre váró)
| Hely | Tartalom | Javaslat |
|---|---|---|
| adat/jeloltek.tsv:329 | TEREMT-002 `Sir 2:8` (elutasítva) | M2: JSir 2:8 |
| genezis/1Moz_10v1-11v32_bovitett.md:121 | „Sir 3:52,4:18” | M2: JSir 3:52,4:18 |
| adat/auditok.tsv:169–171 | proveniencia-scope `range:Sir 2:8` | ⛔ M1: maradjon (F28.32 elfogadja, tesztelt) |
| motivumlog/PaRDeS_motivumok.md:142,330,382,579 | „Sir 3:52,4:18” (kézi sorok; a briefben nem `ir`) | ⛔ M1: bevonás? (javaslat: igen, a fájl nem generált sorain) |

## „Sir” egyéb (NEM migrálandó)
- Kód/teszt (lekerdez.py, teszt_lekerdez_sir.py, normalizal.py, macula_kozos.py ALIAS stb.): az adattáblák belső Sir-kulcsa, szándékos.
- forditasok.tsv:72, 73, 84, 91 és lexikon_hivatkozasok.tsv: BDB/Thayer-idézet („Ecclus … Sir 30:11”, Bölcs-hivatkozás): Sirák fia, marad.
- motivumlog/PaRDeS_motivumok_CHANGELOG.md:152: történeti napló, marad.
- Terminologia.tsv 53–55: a szabály maga.
- Sirák fiára vonatkozó előfordulás a forrásrétegben: nincs.

## Szentlélek / Isten Lelke (9 + 3 hely)
| Hely | Alak | Besorolás |
|---|---|---|
| genezis/1Moz_8v1-22:144, 194, 204 | Szentlélek | CSERE (3 hely) → „Szent Szellem” (204: „Szent Szellem-”, a mondat végén szerkezet marad) |
| genezis/1Moz_1v2-2v3:93 | Isten Lelke | MARAD: Károli-idézet |
| genezis/1Moz_1v2-2v3:95 | Isten Lelke | MARAD: a Károli-alakot idézi/bírálja |
| genezis/1Moz_3v7-24:267 | Szentlélek | MARAD: a szabály idézi a tiltott alakot |
| lexikon/ANTROP-001_TORZSCIKK.md:96, 100; TEREMT-001_TORZSCIKK.md:88 | Isten Lelke(nek) | MARAD: Károli-idézet, a fájl generált (nem szerkeszthető) |
| lexikon/ANTROP-001_TUDOMANYOS.md:71,108; TEREMT-001_TUDOMANYOS.md:159 | Isten Lelke(nek) | MARAD: GENERÁLT, Károli-idézet; a forrás nem javítandó, mert idézet |

Következmény: a 9+3 helyből 3 valódi csere; a többi idézet vagy generált.
