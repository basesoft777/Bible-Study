# FORRAS_FJ3_kjv_bsb.md — 3b: teljes KJV/ASV, majd BSB

*FJ3 — FORRASJELOLTEK_BRIEF.md §3, G5 sorrendje szerint (előbb KJV/ASV, a BSB
kiegészítőként).*

## 1. Teljes bibliás, szószintű, Strong-címkés KJV/ASV — NEM ELÉRHETŐ ebből a
sessionből

A meglévő `KJV_Strongs_*.tsv`/`ASV_Strongs_*.tsv` (1Móz, 2Móz, Péld) forrása a
`konkordancia/README.md` szerint `studybible.info` oldalankénti HTML-lekérése.
**Ez a domain a session hálózati proxy-szabályzata szerint blokkolva van**
(`curl`: `CONNECT tunnel failed, response 403`; a `WebFetch` eszköz explicit
`EGRESS_BLOCKED` hibát ad `studybible.info`-ra) — tehát a meglévő módszerrel a
teljes 66 könyv **ebben a sessionben nem folytatható**.

**Alternatív, git-klónozható forrás keresése** (a brief eBible.org USFM-jelöltje
és egyéb GitHub-repók):
- **eBible.org** közvetlen web-elérése szintén blokkolt (`CONNECT tunnel failed,
  response 403`) — a KJV/ASV USFM/USFX csomagjai csak weben töltődnek le, git
  repóként nincsenek közzétéve.
- **STEPBible-Data** (`github.com/STEPBible/STEPBible-Data`, teljes klón,
  482 MB) **tételesen átnézve**: a `Tagged-Bibles/` mappa csak Arab Biblia
  (`TTAraSVD`) és ESV (`TTESV`, **CC BY-NC** — nem-kereskedelmi, tehát a D17
  szerint eleve kizárt) szó-szintű táblákat tartalmaz. **Nincs benne teljes,
  szó-szintű KJV vagy ASV.** A stepbible.org weboldal maga kínál egy
  "KJV (1769) with Strongs Numbers and Morphology" nézetet, de ez a webes
  felület adata, nem git-repóban tárolt fájl — nem D17-kompatibilis forrás.
- **crizin/bible-db** (`github.com/crizin/bible-db`, MIT kód / PD+CC BY adat):
  teljes 66 könyv KJV-szöveg megvan (`data/kjv/kjv.jsonl`), de **csak
  vers-szintű** (`{"text": "In the beginning God created..."}`), nincs
  szó-Strong illesztés az angol szövegre — a héber/görög oldalon van Strong,
  az angolon nincs. **Nem alkalmas.**
- Egyéb próbált nevek (`bsbible/bsb-usfm`, `openbible/bsb`, `kylerainer/BSB`,
  `bereanbible/bsb`) nem léteznek ilyen néven.

**Verdikt (KJV/ASV):** ebben a menetben **nem importálható** — sem a meglévő
módszer (studybible.info scraping) nem folytatható a hálózati korlátozás
miatt, sem git-klónozható alternatíva nem került elő szó-szintű Strong-
illesztéssel. **Javaslat:** vagy (a) egy jövőbeli session kérje a
`studybible.info` proxy-engedélyezését, és folytassa ugyanazzal a
lapon-kénti letöltő módszerrel, vagy (b) a SWORD "KJV+strongs" modul
feldolgozása (nem ellenőrzött ebben a menetben, külön SWORD-parszolót
igényelne). Egyik sem 2. menetre kész jelölt.

## 2. BSB (Berean Standard Bible) — kiegészítőként, G5 szerint

- **URL:** `github.com/BSB-publishing/bsb-data-output` · **commit:**
  `e1b254cef86d0e65b1a5d1a94b8b112d0f296a2c` (a repó saját `VERSION.json`-ja
  szerint az adatot építő `bsb2usfm` forrás sha-ja: `3c13b1892e9f37c53ca7d75b531bd1336a874a13`,
  a Hebrew morfológia forrása `openscriptures/morphhb` `3d15126fb1ef74867fc1434be1942e837932691f`)
- **Szerkezet:** `base/display/<KÖNYV>/<KÖNYV><fejezet>.json` — **szó/frázis-
  szintű** angol szöveg, mindegyik span Strong-számmal párosítva, pl.
  `["created","H1254"]`. **Mind a 66 könyv megvan** (1190 fejezet-fájl).
  Emellett `base/index-cc-by/` héber szó-szintű morfológiai index (lemma,
  morfológiai kód, Strong), `base/english-concordance/` szó→vers index.
- **Licenc (szó szerint, `README.md` + `LICENSE-CC-BY.md`):**
  - `base/display/` — **CC0 (Public Domain)**, attribúció nem kötelező.
  - `base/index-cc-by/` — **CC BY 4.0**, mert héber morfológiát tartalmaz
    (Open Scriptures Hebrew Bible-ből): *"Hebrew morphology data from Open
    Scriptures Hebrew Bible (OSHB) … licensed under CC BY 4.0."*
  - `base/concordance/` — CC0.
  Tehát pontosan az, amire a 3b-nek szüksége van (`base/display/`), **CC0**,
  a legkevésbé korlátozó licenc a menetben vizsgált öt forrás közül.
- **sha256** (minta, `base/display/GEN/GEN1.json`):
  `0da2a437898feb7584080182226b535e80fc01a71ed8eb90516ba37361e9ff8a`

## 3. BSB Strong-halmaz összevetés a TAHOT-tal, mintán (1Móz 1:1–5, K4: szkript
`naplok/FORRAS_FJ3_bsb_tahot_minta.py`, kimenet `naplok/FORRAS_FJ3_bsb_minta.tsv`)

| Igehely | Halmaz-egyezés (Jaccard) |
|---|---|
| 1Móz 1:1 | 67% |
| 1Móz 1:2 | 86% |
| 1Móz 1:3 | 80% |
| 1Móz 1:4 | 62% |
| 1Móz 1:5 | 77% |

**Az eltérés fő oka nem tartalmi, hanem konvencionális:** a `TAHOT_kivonat.tsv`
a STEPBible-féle **kiterjesztett Strong-számozást** használja, ami a héber
prefixumokat/toldalékokat (kötőszó `וְ`, elöljárók, névelő) **külön
"9000-es sorozatú" pszeudo-Strong-kóddal** listázza (`H9001` = "és", `H9003`
= "ban/ben" stb.) — ezek nem szerepelnek sem a klasszikus Strong-
számozásban, sem a BSB adatban (ott a prefixum a tő szavához tapad). Ha a
9000-es sorozatot kiszűrjük, a **tartalmi Strong-szavak egyezése lényegében
teljes** (1Móz 1:2-ben pl. a TAHOT 19 tokenjéből 6 a 9000-es sorozat, a
maradék 13 mind megvan a BSB 14 tokenje között). Egy valódi eltérés van:
1Móz 1:4-ben a TAHOT `H2895`-öt ad a טוֹב szóra, a BSB (és a standard
Strong-számozás) `H2896`-ot — ez feltehetően a TAHOT saját, nem-standard
tövesítési döntése, nem BSB-hiba.

## 4. Verdikt

| Forrás | Javaslat | Indok |
|---|---|---|
| Teljes KJV/ASV (studybible.info-alapú) | **nem importálható ebben a menetben** | a domain a proxy-szabályzat szerint blokkolva, nincs git-klónozható alternatíva szó-szintű Strong-illesztéssel |
| BSB (`bsb-data-output`, `base/display/`) | **import javasolt, feltétel nélkül** | CC0, teljes 66 könyv, szó-szintű Strong-illesztés, jól dokumentált forrás-lánc (OSHB commit rögzítve), a mintaellenőrzés a konvenciós eltérésen kívül tartalmi egyezést mutat |

A G5 által elvárt sorrend ("előbb KJV, a BSB csak kiegészítő") ebben a
menetben **megfordul a valóságban**: a KJV-oldal elérhetetlensége miatt a
BSB az egyetlen ténylegesen importálható 3b-jelölt. Ez nem változtatja meg,
hogy a Károli-rokonsági híd célja (ami a KJV/ASV mellett szólt) BSB-vel nem
old meg — ezt a 2. menet előtt jelezni kell a döntéshozónak.

## 5. G6 — a meglévő KJV/ASV-fájlok címkézési licence

A `studybible.info` oldal saját licencnyilatkozata **ebből a sessionből nem
volt elérhető** (a domain blokkolva, l. fent), tehát szó szerinti idézése
nem lehetséges. A `konkordancia/README.md` már rögzíti a jelenleg ismert
eredetet: a héber Strong-taggelés a Bible Foundation (bf.org) munkája, az
ASV-taggelés a "Cross Word Project" (Wade Maxfield) munkája — de ezek
**másodkézből dokumentált** állítások, nem a studybible.info saját
szövegéből idézve. **Ez a hézag megmarad**, amíg egy jövőbeli session el
nem éri a domaint.
