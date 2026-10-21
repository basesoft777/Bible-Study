---
feladat: 128
cim: A BDB szakaszonkénti fordításának előkészítése — bemenet, promptváltozat, szakasz-kapu, tárolási kulcs (DT181 (b))
kod: BDB_SZAKASZ_ELOKESZITES
tipus: feladat
fazis: 1
modell: opus
allapot: lezarva
pr: 456
lezarva_osszegzes: "a szakaszonkénti BDB-fordítás eszközlánca kész (bemenet-előállító, prompt v5, 14. szakasz-kapu, szakaszkulcs, közös összefűző, olvasók átállítása); DT285–g; ellenőrzés ELTÉRÉS: 2 → 1 javítókör → TISZTA; a teszt_bont 2 main-beli bukása külön tervezet (beerkezo/Fnn_BDB_FEJLEC_DT_BRIEF.md)"
ag: claude/f128-bdb-szakasz-elokeszites-a2fc2f
ad: a #38 a következő adagtól szakaszonként fordíthat — a bemenet-előállító, a prompt v5, a szakasz-kapu és a forditasok.tsv szakaszkulcsa kész és tesztelt, modellhívásos fordítás nélkül
kovetkezo: "Te: merge a felhasználótól (PR #456); a beerkezo/Fnn_BDB_FEJLEC_DT_BRIEF.md befogadása /befogad-dal"
olvas: [F38_BDB_FORDITAS_BRIEF.md, DONTESEK.md, adat/SEMA.md, adat/bdb_szakaszok.tsv, adat/bdb_forras_javitas.tsv, adat/bdb_szakasz_hu.tsv, adat/forditasok.tsv, adat/terminologia.tsv, eszkozok/emeles.py, eszkozok/forditas_kapuk.py, eszkozok/bdb_adatblokk.py, eszkozok/bdb_jelolt/nezet_general.py, eszkozok/bdb_jelolt/hu_illeszt.py, forditas/prompt_v4.md, naplok/F107_BDB_JELOLT_SZOVEG_naplo.md, naplok/BDB_FORDITAS_sorrend.tsv, konkordancia/BDB_teljes_unabridged.tsv]
ir: [eszkozok/emeles.py, eszkozok/forditas_kapuk.py, eszkozok/teszt_forditas_kapuk.py, eszkozok/ellenoriz.py, eszkozok/teszt_ellenoriz_13.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/bdb_adatblokk.py, eszkozok/teszt_bdb_adatblokk.py, eszkozok/bdb_jelolt/hu_illeszt.py, eszkozok/bdb_jelolt/teszt_bont.py, eszkozok/bdb_jelolt/szakasz_bemenet.py, eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py, forditas/prompt_v5.md, adat/SEMA.md, adat/bdb_szakasz_hu.tsv, naplok/F128_BDB_SZAKASZ_ELOKESZITES_naplo.md, DONTESEK.md, NYITOTT_FELADATOK.md, F38_BDB_FORDITAS_BRIEF.md]
fugg: [107]
nem_fugg: [27, 38]
---

# A BDB szakaszonkénti fordításának előkészítése (BDB_SZAKASZ_ELOKESZITES)

*v1 · 2026.10.20 · tervezet a #38 ⛔ Mj döntéséből (DT181 (b), DT269 (1); felhasználó, 2026-10-20). Írta a #38 döntésrögzítő menete
(`claude/f38-mj-dontes`); befogadás a `/befogad`-dal.*

## Miért

A #38 eddig a `BDB_teljes_unabridged.tsv` sima szövegét fordította Strongonként egy darabban (`jelentes_szam = teljes`). A szöveg
nem hordozza a jelentéspontok határát, ezért a magyar sem; a #107 utólagos illesztése 98 Strong 606 szakaszán elakadt (N-F107b).
A DT181 (b) szerint a következő adagtól a fordító **szakaszonként** kapja a szöveget az `adat/bdb_szakaszok.tsv`-ből (kulcs `strong` +
`sorszam`), és a szakaszhatár változatlan tokenként megy át. A DT269 (1) szerint a bemenet a nyers szöveg a `hivatkozas`
javításokkal, **pe/mem csere nélkül** (`nezet_general.py` `--pe-mem` nélküli logikája).

Ez a feladat az eszközláncot készíti elő. **Fordítás nem indul:** a menet modellhívással fordítást nem készít, az
`adat/forditasok.tsv`-t nem írja. A kapukat a kész fordításokon (`adat/bdb_szakasz_hu.tsv` `illeszkedik` sorai) és szintetikus
eseteken teszteli.

## Lépések

### M0 — felmérés és ⛔ tervezési döntések (csak olvas)

Mérje fel, és a `DONTESEK.md`-be helyőrzős tételként (`DT285` …) vigye a felhasználó elé, opciókkal és javaslattal:

1. **Tárolási kulcs.** (a) szakaszonkénti sorok az `adat/forditasok.tsv`-ben (`jelentes_szam` = a szakasz azonosítója, pl. `sz<sorszam>`;
   `forras_hash` a szakasz szövegéé), a Strong teljes szövege nézet; (b) egy `teljes` sor Strongonként, benne a szakaszhatár
   gépi tokenként (pl. `⟦12⟧`), amelyet minden olvasó levesz; (c) egyéb. Mérje: hány olvasója van a `jelentes_szam = teljes`
   BDB-soroknak (render, `lexikon_general.py`, `olvaso_szerver`, kapuk, CI E-szabályok), és mit kell átállítani opciónként.
2. **A `forras_hash` alapja.** Az új bemenet nem a TSV szövege (a nyers nézet 446 kész sor hash-ét változtatná, DT231 (2)). Mi a
   hash tárgya, és hogyan marad összevethető a 674 kész Strong a TSV-cseréig?
3. **A darabolás egysége.** Egy hívás = egy Strong összes szakasza (tokenekkel), vagy szakaszcsoport a 20 000 karakter fölötti
   szócikkeknél (a #28 G4151/H1121 mintája)? A fordító a szakaszok egymásutánját lássa (kontextus), ne egyenként kapja.
4. **A nem `egyezik` illesztésű Strongok** (`reszleges` 94, `sikertelen` 15, `csonk` 35, a táblán kívüli 9; SEMA 2.30): ezek
   bemenete honnan jön (a TSV-ből `teljes`-ként, a régi módon), és hol jelölődik?
5. **A 98 elakadó Strong (N-F107b)** újrafordítása: a meglévő `teljes` sor sorsa (felváltódik / archív `megjegyzes`), és a sorrendbe
   illesztésük (a 7. adag elején vagy a gyakorisági helyükön).

**⛔ M0:** a felhasználó dönt az 1–5. pontról. A döntésig nincs kódírás.

### M1 — bemenet-előállító

`eszkozok/bdb_jelolt/szakasz_bemenet.py`: Strongonként a szakasztábla sorai (`jel` + `szoveg`) a `hivatkozas` / `javitva` javításokkal,
pe/mem csere nélkül, a határokon a tokennel; determinisztikus, `--ellenoriz`-zel. Teszt: `teszt_szakasz_bemenet.py` — a tokenek nélküli
kimenet Strongonként egyezik a `nezet_general.py` (`--pe-mem` nélküli) nézetével; 0 pe/mem csere.

### M2 — prompt v5 és `emeles.py`

`forditas/prompt_v5.md` a v4-ből: a szakasztoken változatlan átvitelének szabálya és egy példa; minden más szabály változatlan
(Károli-tábla, terminológia, kötelező alakok, adatblokk). Az `emeles.py` új (vagy kapcsolós) ága a szakaszonkénti bemenettel; a régi
`teljes` útvonal változatlanul működik (a 674 kész sor és a nem `egyezik` Strongok miatt). A rögzítés az M0 1. pontja szerinti kulccsal.

### M3 — szakasz-kapu

Új kapu a `eszkozok/forditas_kapuk.py`-ban: a fordításban a tokenek száma és sorrendje egyezik a bemenetével, nincs új vagy hiányzó
token, a tokenek közti szakasz nem üres. A régi `9_tagolas` kapu szakaszon belül fut tovább. Tesztek: szintetikus esetek (hiányzó,
duplázott, felcserélt token, üres szakasz) és a `bdb_szakasz_hu.tsv` `illeszkedik` soraiból összerakott tokenes magyar szövegek
(ezeken a kapunak 0 hibát kell adnia).

### M4 — száraz próba és zárás

1. Száraz próba 3 Strongon (egy rövid, egy több törzses, egy N-F107b-s): a prompt összeáll, a kapu a kész magyar szakaszokon zöld;
   **modellhívás nincs**. Kimenet a naplóba (`naplok/F128_BDB_SZAKASZ_ELOKESZITES_naplo.md`), a prompt a repón kívülre.
2. `adat/SEMA.md` 2.14 a döntött kulccsal; a `F38_BDB_FORDITAS_BRIEF.md` „Lépések” szakaszához rövid hivatkozás a szakaszonkénti
   útvonalra (a #38 fejlécéhez nem nyúl).
3. Független ellenőr, draft PR.

## Nem cél

- Fordítás (a #38-é); a `adat/forditasok.tsv` írása.
- A pe/mem csere és a `BDB_teljes_unabridged.tsv` cseréje (DT231 (d) külön feladata; DT269 (1)).
- A #67 kapuja (`bdb_igehely_javitas` összevetés) — ugyanazt a két fájlt írja, a sorrend a befogadáskor dől el.
