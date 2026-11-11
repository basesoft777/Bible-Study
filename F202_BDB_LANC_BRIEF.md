---
feladat: 202
cim: A BDB illesztő láncának és forrásadatának javítása a nyitott tételek alapján (C1, C2, C4, C5)
kod: BDB_LANC
tipus: feladat
fazis: folyamat
modell: opus
allapot: megallt
ad: a BDB-lánc (2.30 szakasztábla, 2.31 forrásjavítás, 2.32 magyar illesztés, 2.29 szeletelő-hivatkozások) ismétlődő hibái gyökérok-szinten javítva, minden javított osztályra gépi védelem (teszt vagy kapu), mért előtte–utána számokkal; a lexikonlapok nincsenek újragenerálva, a hatás mérve
kovetkezo: "Te: a draft PR áttekintése; a merge az orkesztrátoré, a HAMART-001 /kiadas után; az ALVIL-001 újragenerálása előtt az N-F202e (generátor); döntés: DT-F202a"
munka: adat
olvas: [CLAUDE.md, adat/SEMA.md, NYITOTT_FELADATOK.md, eszkozok/bdb_jelolt/bont.py, eszkozok/bdb_jelolt/hu_illeszt.py, eszkozok/bdb_jelolt/forras_javit.py, eszkozok/olvaso_szerver/bdb_szelet.py]
ir: [F202_BDB_LANC_BRIEF.md, eszkozok/bdb_jelolt/bont.py, eszkozok/bdb_jelolt/hu_illeszt.py, eszkozok/bdb_jelolt/forras_javit.py, eszkozok/bdb_jelolt/teszt_bont.py, eszkozok/bdb_jelolt/teszt_hu_illeszt.py, eszkozok/olvaso_szerver/bdb_szelet.py, eszkozok/olvaso_szerver/bdb_vers_jelentes.py, eszkozok/olvaso_szerver/teszt_bdb_vers_jelentes.py, adat/bdb_szakaszok.tsv, adat/bdb_szakasz_hu.tsv, adat/bdb_forras_javitas.tsv, adat/bdb_igehely_javitas.tsv, adat/bdb_vers_jelentes.tsv, adat/SEMA.md, naplok/F202_jelentes.md, NYITOTT_FELADATOK.md, dontesek/uj/epic-spence-e4ece9.md, nyitott/uj/epic-spence-e4ece9.md]
fugg: [185, 197]
nem_fugg: [182]
---

# F202_BDB_LANC_BRIEF.md — A BDB-lánc javítása (C1, C2, C4, C5)

*FELADATOK #202 · Modell: opus · v1 · 2026.11.11*

*Az orkesztrátor indította, külön sessionben, saját ágon (`claude/epic-spence-e4ece9`); befogadás nélkül. Forrás: a
generátor-hibaleltár (2026-11-11) C1, C2, C4, C5 sora és a hozzájuk tartozó N-tételek. Az ütemezés szerint a HAMART-001
lezárása után nem készül új lap; a generátor és a lánc hibái javulnak, hogy a lapkészítés bármikor folytatható legyen.*

## 1. Cél és tételek

| Tétel | N-tételek | Hely |
|---|---|---|
| C1 — a magyar BDB-szöveg szócikkhatár-hibája (a jelölő nélküli szócikkfej magyar szövege az előző szócikkben marad) | N147, N100, K56 | `bdb_jelolt/hu_illeszt.py`, `adat/bdb_szakasz_hu.tsv` |
| C2 — a szakasztábla (2.30) hibái: „1 — bűn” alatt a bűnáldozat; fej-felismerési osztályok; nem szomszédos azonos útvonal; homonima-, rész- és számhibák | N99, N103, N109, N113, N142 (a N125, N126 Thayer-tétel: a `thayer_*` az F203-é) | `bdb_jelolt/bont.py`, `olvaso_szerver/bdb_szelet.py`, `adat/bdb_szakaszok.tsv` |
| C4 — BDB-forrásszöveg-hibák: Abdiás-vers fejezetszámmal, 2Krón 10:20/26, Zoar/H6920, pe/mem OCR | N101, N102, N104, N120–N122 | `adat/bdb_forras_javitas.tsv`, `adat/bdb_igehely_javitas.tsv`, `bdb_jelolt/forras_javit.py` |
| C5 — a könyvnév nélküli és a nem létező fejezetű könyv utáni hely feloldása | N141 | `olvaso_szerver/bdb_szelet.py` (`hivatkozasok`) |

Gyökérok-szabály: második előfordulásnál nem példányjavítás, hanem szabály és gépi védelem (teszt vagy kapu).

## 2. Lépések

1. Előtte-mérés (minden tételre szám, a mérő szkript a repón kívül; az eredmény a jelentésben).
2. Tételenként: a szabály a lánc megfelelő pontján; a tábla újragenerálva; teszt vagy kapu; utána-mérés.
3. Hatásmérés: a lexikonlapok generált kimenete egy repón kívüli próbakönyvtárban, a mai és a javított adattal; hány lapon, hány
   blokkban változna. **A lapokat a repóban nem generálja újra** (a HAMART-001 kiadás alatt áll).
4. Jelentés (`naplok/F202_jelentes.md`), az igazolt N-tételek lezárása, draft PR a `main`-be.

## 3. Határok

Nem nyúl: `eszkozok/lexikon_general.py`, `olvasoi_kapu.py`, `olvasoi_kovetkeztetes.py`, `allitas_adat.py`, `karoli_kh_epseg.py`,
`eszkozok/visszhang/*`, `adat/elofordulasok.tsv`, `jeloltek.tsv`, `kapcsolatok.tsv`, `motivumok.tsv`, `lexikon/*` (a #182 és a
későbbi generátor-kör írja); `glossza_lexikon_forditas.py`, `thayer_*` (az F203 írja). Az `adat/forditasok.tsv`-t nem írja.

## 4. Gépi kapu (G)

- G1: `python eszkozok/bdb_jelolt/bont.py --ellenoriz`, `hu_illeszt.py --ellenoriz`, `forras_javit.py --ellenoriz` és a
  `bdb_vers_jelentes.py --ellenoriz` a commitolt táblákkal bájtra azonos (a saját `--ts`-ükkel).
- G2: `python eszkozok/teszt_futtat.py --gyors` zöld; a `bdb_jelolt` saját tesztjei (`teszt_bont.py`, `teszt_hu_illeszt.py`,
  `teszt_szakasz_bemenet.py`) zöldek.
- G3: minden javított hibaosztályra teszt (szabály-szinten szintetikus esettel és a valódi táblán felső korláttal).
- G4: a `lexikon/` és a tiltott fájlok a base-hez képest változatlanok (`git diff --stat origin/main -- …`).

## 5. Döntések és nyitott tételek

Helyőrzővel: `dontesek/uj/epic-spence-e4ece9.md`, `nyitott/uj/epic-spence-e4ece9.md`. Végleges számot a `szamkiosztas` Action ad.
