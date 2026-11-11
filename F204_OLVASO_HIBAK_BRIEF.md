---
feladat: 204
cim: Az olvasó szerver három nyitott hibája — N-F99a, N117, N118
kod: OLVASO_HIBAK
tipus: feladat
fazis: folyamat
modell: claude-sonnet-5-5
allapot: kesz
ag: claude/unruffled-diffie-bcef47
ad: a tW-blokk Markdownja renderelve, a BDB jelmagyarázat hiányzó jelei felvéve, a `/szo/<strong>?vers=` paraméter átvéve; mindegyikre teszt
kovetkezo: "Te: a draft PR áttekintése; merge-et az orkesztrátor végzi"
munka: folyamat
olvas: [eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/konfig/bdb_jelek.tsv]
ir: [eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/konfig/bdb_jelek.tsv, eszkozok/olvaso_szerver/teszt_olvaso_hibak.py, NYITOTT_FELADATOK.md, F204_OLVASO_HIBAK_BRIEF.md]
fugg: []
nem_fugg: [182, 201, 202, 203]
---

# F204_OLVASO_HIBAK_BRIEF.md — Az olvasó három hibája

*FELADATOK #204 · Modell: claude-sonnet-5-5 · v1 · 2026.11.11*

**Hatókör.** Csak `eszkozok/olvaso_szerver/*` és tesztje; az adat és a generátorok érintetlenek.

## Megoldás
1. **N-F99a.** A `tw_szocikkek.szoveg` a sortörést szó szerinti perjel+n alakban tárolja. Új `blokkok._md_tw`: fejléc (`#`, `##`), `* ` lista, bekezdés, `__`/`**` félkövér, `*` dőlt, hivatkozás csak a szövegével (a `rc://` és `../kt/x.md` cél nem követhető); minden más escape-elt; a blokk címével azonos első `# cím` sor kimarad.
2. **N117.** `konfig/bdb_jelek.tsv`: új csoport `nyelvtani` (*status absolutus/constructus*, *absolutus*, *constructus*), továbbá *SS*, *Wetzst* (csoport `szerző`), `manual` provenienciával. A feloldás a BDB rövidítésjegyzékéből való; a jegyzék a repóban nincs meg, ezért a két szerzőjel feloldása a felhasználói/lektori átnézésre vár. A *Hu* és a *De* szándékosan kimarad (bizonytalan, illetve ütközik a „de” kötőszóval).
3. **N118.** `/szo/<strong>?vers=1Moz/1/5`: a szigorúan ellenőrzött vers-kontextus a `szo_lap` → `szo_torzs(…, ig)` láncon átmegy; közös `vers_kontextus` segéd a `/r/szo` `ig` paraméterével; a gyorsítótár-kulcsban a vers is szerepel.

## Védelem
`eszkozok/olvaso_szerver/teszt_olvaso_hibak.py` (7 teszt): Markdown-renderelő (nyers jel nincs, szerkezet, escape), a H8441 tW-blokk a valódi adatbázison, a H7451 jelmagyarázat (SS, Wetzst, nincs feloldatlan jel), a `?vers=` (jelölés van; vers nélkül, hibás vagy nem szigorú alaknál nincs).
