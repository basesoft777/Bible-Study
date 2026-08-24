# Konkordancia — KJV-Strongs és ASV-Strongs (Példabeszédek)

Ez a mappa a PaRDeS-projekt Strong-számmal ellátott angol híd-forrásait tartalmazza,
szavankénti bontásban, a `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` döntési fájl
4.8 és 4.9 pontjában rögzített módszertan szerint.

## Fájlok

| Fájl | Tartalom | Sorok (fejléc nélkül) |
|---|---|---|
| `KJV_Strongs_Proverbs.tsv` | KJV (King James Version) + Strong-számok + morfológiai kódok, Példabeszédek 1-31 | 5945 |
| `ASV_Strongs_Proverbs.tsv` | ASV (American Standard Version, 1901) + Strong-számok, Példabeszédek 1-31 | 5872 |

## Oszlopok

**KJV_Strongs_Proverbs.tsv:**
```
Igehely | Szósorszám | Strong-szám | Angol szó | Morfológiai kód
```

**ASV_Strongs_Proverbs.tsv:**
```
Igehely | Szósorszám | Strong-szám | Angol szó
```
(Az ASV-forrás nem tartalmaz morfológiai kódot.)

- **Igehely:** pl. `Proverbs 23:7`
- **Szósorszám:** a szó sorszáma a versen belül (1-től indul)
- **Strong-szám:** héber Strong-szám (H-szám), mert a Példabeszédek ószövetségi könyv
- **Angol szó:** a ragozott angol szóalak, pontosan ahogy a forrás megjeleníti (a szomszédos írásjelek — vessző, kettőspont — a szóhoz tartozó span részeként jelennek meg a forrásban, ezért változatlanul megmaradtak)
- **Morfológiai kód (csak KJV-nél):** a forrásban szögletes zárójelben jelzett igei/névszói alakinformáció (pl. `[H8798]`); ha egy szóhoz több morfológiai jelölés is tartozik (pl. Kethiv/Qere-változat), szóközzel elválasztva, egy cellában szerepelnek (pl. `[H8686] [H8675]`)

## Forrás

- **KJV_Strongs minta-URL:** `https://studybible.info/KJV_Strongs/Proverbs%20{N}` (N = 1-31)
- **ASV_Strongs minta-URL:** `https://studybible.info/ASV_Strongs/Proverbs%20{N}` (N = 1-31)
- **Letöltés dátuma:** 2026-08-24
- **Letöltő/feldolgozó módszer:** oldalankénti HTML-letöltés (`fetch`), majd szavankénti kinyerés a forrás `<span class="unit">` szerkezetéből (Strong-szám-hivatkozás + angol szórész; a `[H####]` formátumú, zárójeles hivatkozások morfológiai kódként lettek a megelőző szóhoz rendelve, nem önálló szóként számolva)

## Licenc / eredet

- **Alapszöveg (KJV, ASV):** közkincs (public domain). A KJV brit "Crown copyright"-szabálya kizárólag a kereskedelmi nyomtatásra vonatkozik az Egyesült Királyságban; nem-kereskedelmi/kutatási felhasználásra és a világ többi részén szabadon felhasználható.
- **Héber Strong-számok (KJV-Strongs):** Bible Foundation (bf.org).
- **Görög Strong-számok (KJV-Strongs, ÚSZ-hez, itt nem releváns):** CrossWire KJV2003 projekt.
- **ASV Strong-taggelés:** a "Cross Word Project" (Wade Maxfield) munkája — a KJV-Strongs taggelésétől független forrás, ami valódi kereszt-ellenőrzést tesz lehetővé.

A pontos hivatkozásokért és a módszertani indoklásért lásd a döntési fájl
[PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md](../PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md)
4.8 (KJV-hidas módszer) és 4.9 (ASV kereszt-ellenőrzés) pontját.

## Validáció

A generált Péld 23:7 adat egyezést mutat a döntési fájl 4.8-as pontjában rögzített,
korábban kézzel ellenőrzött referenciával:

```
számítgatja = H8176 [H8804]
magában     = H5315
egyél       = H398  [H8798]
igyál       = H8354 [H8798]
mondja      = H559  [H8799]
akarattal   = H3820
```

Mind a hat szó (Strong-szám és morfológiai kód) számjegyre pontosan egyezik — a validáció
sikeres volt.
