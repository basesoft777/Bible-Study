# RENDER_R0_jelentes.md — R0 felmérés

*2026.09.23 · a RENDER_BRIEF.md v2 R0 szakaszának lezáró jelentése*

## 1. §0 újramérés (R0.1)

A brief §0 táblájának minden sorát újramértem. A brief v1 elleni önálló ellenőrzés
(l. a chat előzménye) egy blokkoló eltérést talált: a 0.13 sor mögötti törzscikk-pilot
artifact hiányzott a repóból (`git log --all` egyetlen branch-en sem talált
`*torzscikk*` fájlt). Ez a RENDER_BRIEF.md v2-ben megoldódott: a felhasználó beemelte a
`motivumlog/lexikon_pilot/ISTENTISZT-001_TORZSCIKK.md`, `_dontesnaplo.md` és
`torzscikk_pilot.py` fájlokat (`R0: törzscikk-pilot beemelése` commit).

| # | Mérés | Brief várt érték | Mért érték | Eredmény |
|---|---|---|---|---|
| 0.1 | `main` = `origin/main` | `2eea2c2` | `2eea2c2` (a brief-commit előtt) | egyezik |
| 0.2 | `ellenoriz.py` összesítő | RENDBEN 8 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 1, kód 0 | ugyanez | egyezik |
| 0.3 | `general.py --cel lexikon --ellenoriz` | 8/8 „változatlan lenne" | 8/8 | egyezik |
| 0.4 | lexikonoldalak | 8, mind 10 generált blokkal | 8, mind 10 | egyezik |
| 0.5 | kézi szöveg a blokkokon kívül | ISTENTISZT-001: 37 222; a többi 7: 995–1 033 | ISTENTISZT-001: 37 222; a többi 995–1 033 | egyezik — **csak blokkhatár-pontos (regex a markerekre) méréssel**; egy naiv soronkénti számlálás 9 karakterrel tévedett a két szélső esetnél (l. R0.2 munkalap módszertani megjegyzése) |
| 0.6 | a 7 helyőrzős oldal 6–7. szakaszának régi helyőrző-szerkezete | `### PaRDeS keretrendszer`, `### Módszertani napló`, `### Nyitott kérdések és séma-korlátok` | igazolva mind a 7 oldalon | egyezik. **Melléklelet:** a 2/b rés is régi helyőrző-fejlécet visel a 7 oldalon (`### 2/b *(kézi, ha van)*`), szemben az ISTENTISZT-001 `### 2/b. Kiegészítő szótári adatok *(kézi)*` fejlécével — ezt a brief a 0.6-ban nem nevesíti külön, de a G2/D4 indoklásába (a 7 oldal régi helyőrző-szerkezete nulla-diffet ad) beletartozik |
| 0.7 | `lexikon_hivatkozasok.tsv` | 24 sor; Thayer 14/BDB 4/TBESG 4/TBESH 1/LSJ 1; `forditas_hu` 11 | ugyanez | egyezik |
| 0.8 | `forditas_ubs.tsv` | 20 sor; `definicio_hu` 20; `glosszak_hu` 20 | ugyanez | egyezik |
| 0.9 | `motivumok/*.md` | 8 fájl, nem tartalmazzák a lexikonoldal kézi szövegét | 8 fájl; mintavételes ellenőrzés (ISTENTISZT-001 Kivonat-rés első 200 karaktere) nem található a naplóban | egyezik |
| 0.10 | kiejtés-pár a kézi szövegben (blockquote nélkül) | görög 50, héber 49, mind ISTENTISZT-001-ben | ugyanez | egyezik |
| 0.11 | tudományos átírás-gyanú a generált blokkokban (becslés) | 859 | saját becslés: 936 (l. R0.4 pontosítás lent) | **nem megállási ok** (a brief maga jelöli becslésnek); mindkét módszer az R0.4-ben |
| 0.12 | nyers SQLite | `MCGED.lexicon` 10 666 sor; `TBESH.lexicon` 9 888 sor | ugyanez | egyezik |
| 0.13 | törzscikk-pilot (ISTENTISZT-001) | 32 igehely (22/10) · 25 kapcsolat · 22 LXX-sor · 106 kereszthivatkozás · 0 üzemeltetési elem | a beemelt `stat.txt`-ből: `igehely=32` (`igehely_osz=22` ⇒ ÚSZ 10), `kapcsolat=25`, `lxx_sor=22`, `kereszthivatkozas_talalat=106`; a végső kimenetben `grep -ic üzemeltet` = 0 | egyezik. A `torzscikk_pilot.py`-t újrafuttattam a mai `lexikon/ISTENTISZT-001_TUDOMANYOS.md`-ből `/tmp`-be — a nyers kimenet CRLF-fel tért vissza (Windows Python szöveges írási mód), de `\r` eltávolítása után **bájtra azonos** a beemelt fájllal (`cmp` exit 0) |

**Következtetés:** a §0 tábla — a 0.13 pilot-beemelés után — teljes egészében megerősítve. Nincs blokkoló eltérés.

## 2. Rés-leltár (R0.2)

`naplok/RENDER_R0_resek.tsv` — 56 sor (8 oldal × 7 rés): fájl, rés-név, bájtméret,
helyőrző-e, fejlécsor szövege. Réseken és vázon kívül eső szöveg: **0** (a várt szám
szerint). A hét rés mindegyikét a saját fejlécsora azonosítja (`## Kivonat`, `### 2/b`,
`### Miért fontos ez a lelet`, `### Minősítés`, `### Alátámasztás`, `## 6. Értelmezés`,
`## 7. Módszertan és nyitott kérdések`), a rés vége a következő rés-fejléc, generált
marker vagy `## `-szintű váz-fejléc.

**Módszertani megjegyzés (a 0.5-nél tapasztalt hiba nyomán):** a blokkhatárokat
(GENERÁLT-KEZDET/VÉGE) **nem soronkénti**, hanem teljes szöveges regex-illesztéssel kell
azonosítani. Egy soronkénti feldolgozás a marker-sorokat kihagyja a számolásból, de a
hozzájuk tartozó sortörést máshogy kezeli, mint a blokkhatáron belüli/kívüli szöveg
összefésülése — ez 9 karakteres eltérést okozott két oldalon (ISTENTISZT-001, HODIT-001)
az első próbálkozásban. A javított, blokkhatár-pontos módszer bájtra egyezett a brief
0.5 számaival.

## 3. Kiejtés-tesztkészlet (R0.3)

`naplok/RENDER_kiejtes_tesztkeszlet.tsv` — 200 pár (görög 112, héber 88), oszlopok:
`nyelv`, `szo`, `kiejtes`, `hely`. Forrás szerinti bontás:
- lexikonoldalak kézi szövege (generált blokkon és blockquote-on kívül): 99 pár
  (görög 50, héber 49) — pontosan a brief 0.10 száma, mind ISTENTISZT-001-ben.
- `adat/lexikon_hivatkozasok.tsv` `forditas_hu` mezője: a BDB/TBESH szócikk-fordítások
  szabad szövegében rejlő párok.
- `adat/forditas_ubs.tsv` `definicio_hu` és `glosszak_hu` mezői.

A minta zajos (a regex `(...)` mintát keres görög/héber betű után, ami néha egy egész
mondatot fog be, nem csak egy szót) — élesítéskor (`kiejtes.py`) ez tisztítást igényel;
az R0-szinten leltárnak elég.

## 4. Átírás-leltár a generált blokkokban (R0.4)

`naplok/RENDER_R0_atirasok.tsv` — soronként: fájl, blokk-azonosító (`elofordulasok`,
`szocikkek`, `lxx`, `kereszthivatkozasok` stb.), nyelv, típus (`lemma`/`alak`), Strong
(csak lemmánál), szó, átirat.

| Nyelv | Típus | Darabszám |
|---|---|---|
| görög | lemma (`### G#### — szó (átirat)` fejléc) | 15 |
| görög | alak (egyéb átirat a blokkban) | 290 |
| héber | lemma | 25 |
| héber | alak | 606 |
| **összesen** | | **936** |

**Ez pontosítja a 0.11 becslést:** a brief 859-es száma és a saját 936-os becslésem
közül a **936 a blokkhatár-pontos, teljes leltár** — ugyanazzal a blockquote-kizárási
szabállyal mérve, mint a 0.10/0.5. A 859 valószínűleg egy szűkebb mintavétellel vagy
más blockquote-kezeléssel készült. **Az R2.1 elvárt diffje ebből a 936-os számból
induljon ki**, nem a 859-ből.

Módszertani korlát: a `lemma`/`alak` szétválasztás egy fejléc-mintára
(`^#{3,5} [HG]\d+ — szó (átirat)$`) épül; ez megbízhatóan azonosítja a szócikk-fejléceket,
de az `alak` kategórián belül nem különbözteti meg pl. az LXX-idézetet a kereszthivatkozás
igeszövegétől — ez az R1.6/R2.1 tényleges `kiejtes.py`-jának finomabb elemzést igényel.

## 5. Forrás-összevetés (R0.5)

`naplok/RENDER_R0_forras_osszevetes.tsv`. A 8 motívum `elofordulasok.tsv`-jéből 24 egyedi
H-token és 13 egyedi G-token adódik.

**TBESH.txt vs TBESH.lexicon (24 H-token):** mindegyik token mindkét forrásban megvan.
Tartalmi összevetés (karakterszám-becsléssel): 9 tokennél a `.txt` bővebb, 13-nál a
`.lexicon` bővebb, 2-nél nagyjából egyenlő. **Nincs olyan token, ahol az egyik forrás
teljesen hiányozna a másikhoz képest** — de a `.lexicon`-ra való egyszerű átállás (a G12
javaslat "marad a TBESH.txt" alternatívájával szemben) **tartalmat veszítene** azon a
9 tokenen, ahol a `.txt` bővebb (pl. H5315 — `nefes` — 4061 vs 666 karakter, H7121 maga a
motívum-token 2267 vs 699 karakter). **Ez ellentmond a G12 feltételének** („ha az R0.5
összevetése nem talál tartalomvesztést") — l. a kérdések közt.

**MCGED lefedettség (13 G-token):** mind a 13 token pontosan 1 sorral szerepel a
`MCGED.lexicon`-ban — teljes lefedettség.

**SECE L–N és megfelelő-lista (13 G-token):** mind a 13 token megvan a
`SECE_G_teljes.tsv`-ben, és a `Teljes_szocikk` mező strukturáltan tartalmazza az
`LN: ...` (Louw-Nida domén-kódok, vesszős lista), a `GK: ...` (Goodrick-Kohlenberger
megfelelő-szám) és egy `Hebrew: ...` (héber megfelelő-lista) almezőt — mindhárom
gépileg kinyerhető egyszerű mintaillesztéssel.

## 6. Volumen a fordítási pipeline-hoz (R0.6)

`naplok/RENDER_R0_volumen.tsv`:

| Forrás | Sor | Karakter |
|---|---|---|
| Thayer | 5 427 | 4 509 565 |
| BDB | 8 091 | 6 429 306 |
| TBESG | 11 105 | 4 302 344 |
| UBS (jelentések) | 9 079 | 2 923 253 |
| UBS (referenciák) | 130 952 | 6 469 355 |
| SDBH | 22 284 | 2 389 365 |
| SDGNT | 9 079 | 1 193 069 |

Ez a teljes kivonatok mérete, nem csak a 8 motívumra eső szeletük — a fordítási
pipeline (kizárt tétel, l. brief „Nincs benne") tervezéséhez ez a felső korlát.

## 7. Kérdések — egy csokorban

1. **G12 feltétele nem teljesül tisztán.** A TBESH-összevetés (R0.5) szerint 9 a 24
   H-tokenből olyan, ahol a `.txt` bővebb tartalmat hordoz, mint a `.lexicon`
   (pl. H5315 *nefes*: 4061 vs 666 karakter). A G12 „ha nem talál tartalomvesztést"
   feltétele szó szerint véve nem teljesül. Kérdés: a G12 mégis érvényben marad-e
   (mert a `.lexicon` strukturáltabb és a motívum-token maga — pl. H7121 — nem veszít
   érdemben), vagy a `TBESH_konszolidalt.tsv`-nek (R2.2) mindkét forrást egyesítenie
   kell (unió, nem csere)?
2. **A 0.11 becslés két száma.** A brief 859-et, a saját blokkhatár-pontos leltár
   (R0.4) 936-ot ad. Melyik legyen az R2.1 elvárt diffjének mércéje — a 936 (l. §4
   fenti indoklás), vagy kell egy harmadik, szűkebb definíció (pl. csak a `lemma`
   kategória, 15+25=40)?
3. **A 2/b rés régi fejléce a 7 helyőrzős oldalon.** A `### 2/b *(kézi, ha van)*`
   fejléc eltér az ISTENTISZT-001 `### 2/b. Kiegészítő szótári adatok *(kézi)*`
   fejlécétől. A G2/D4 szerint ez a nulla-diff szempontjából nem probléma (a rés a
   fejléccel együtt tárolódik szó szerint), de az R1.1 forrásréteg-kivágásnál
   (`render_resek_kivag.py`) tudnia kell mindkét fejléc-variánst felismerni — ezt
   érdemes-e a brief R1.1-es tételébe explicit megjegyzésként felvenni?
4. **A kiejtés-tesztkészlet zajossága.** A 200 pár regex-alapú kinyeréssel készült,
   és több hamis találatot tartalmaz (pl. teljes tagmondatok a zárójelben, ha a minta
   egy hosszabb magyarázatot fog be, nem egy szót). Az 1. menet R1.6-jában
   (`kiejtes.py --ellenoriz`) ez a nyers tesztkészlet-e a bemenet, vagy előbb kézi
   tisztítást igényel egy szűkebb, csak a valódi kiejtés-párokat tartalmazó
   változatra?

## Munkalapok

- `naplok/RENDER_R0_resek.tsv`
- `naplok/RENDER_kiejtes_tesztkeszlet.tsv`
- `naplok/RENDER_R0_atirasok.tsv`
- `naplok/RENDER_R0_forras_osszevetes.tsv`
- `naplok/RENDER_R0_volumen.tsv`

## Elfogadási kritériumok (K1–K3)

- **K1** — teljesítve: a §0 minden sora jelentve fent (1. szakasz).
- **K2** — teljesítve: az öt munkalap és e jelentés megvan; a kérdések a 7. szakaszban,
  egy listában.
- **K3** — teljesítve: az éles `adat/`, `lexikon/`, `motivumok/` könyvtárba az R0 alatt
  nem történt írás (csak olvasás és mérés; a `naplok/` és a felhasználó által kért
  `motivumlog/lexikon_pilot/` írás a brief szerint engedélyezett munkatermék).
