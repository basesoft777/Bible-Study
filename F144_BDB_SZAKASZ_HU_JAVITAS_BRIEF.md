---
feladat: 144
cim: A magyar BDB szakaszillesztésének javítása — a „csak a jelölő” sorok (H0001 és társai), a szövegközi szám- és törzsnév-említés kizárása az illesztőben, újragenerálás és újramérés (BDB_SZAKASZ_HU_JAVITAS)
kod: BDB_SZAKASZ_HU_JAVITAS
tipus: feladat
fazis: 1
modell: opus
allapot: nem_indult
ad: az adat/bdb_szakasz_hu.tsv-ben nincs olyan `illeszkedik` sor, amelynek magyar szövege csak a jelölő, kivéve a soronként igazolt szerkezeti eseteket; a hu_illeszt.py a szövegközi szám- és törzsnév-említést nem köti jelölőhöz; az újragenerált tábla kategória-eloszlása mérve, a B-kör (≈70 szócikk) szúrópróbával átnézve
kovetkezo: "/kovetkezo (M0 ⛔: a 20 szócikk soronkénti átnézése és a javítási szabály)"
munka: folyamat
olvas: [naplok/BDB_SZAKASZ_HU_JELOLO_JELENTES.md, naplok/F107_BDB_JELOLT_SZOVEG_naplo.md, F107_BDB_JELOLT_SZOVEG_BRIEF.md, adat/bdb_szakaszok.tsv, adat/forditasok.tsv, konkordancia/BDB_teljes_unabridged.tsv, eszkozok/bdb_jelolt/bont.py, eszkozok/bdb_jelolt/szakasz_bemenet.py]
ir: [eszkozok/bdb_jelolt/hu_illeszt.py, eszkozok/bdb_jelolt/teszt_hu_illeszt.py, adat/bdb_szakasz_hu.tsv, naplok/BDB_SZAKASZ_HU_JAVITAS_naplo.md]
fugg: []
nem_fugg: [27, 38]
---

# F144_BDB_SZAKASZ_HU_JAVITAS_BRIEF.md — A magyar BDB szakaszillesztésének javítása

*FELADATOK #144 · Modell: opus · v1 · 2026.10.25*

## 1. Cél

A régi úton (egy szócikk egy darabban) lefordított BDB-szócikkek magyar szövegét a `eszkozok/bdb_jelolt/hu_illeszt.py` illeszti a szakasztábla soraihoz (`adat/bdb_szakasz_hu.tsv`, SEMA 2.32; az F107-ben készült, a #107 lezárt). Egy mérés (`naplok/BDB_SZAKASZ_HU_JELOLO_JELENTES.md`, `scope=adat/bdb_szakasz_hu.tsv (674 Strong, 9 664 sor, sha1 2dcfad3cea24) | forras=ad hoc szűrés | ts=2026-10-25`, ág `ccr-84ba79ed-q18w8z`, commit `ac71281`) szerint 26 `illeszkedik` sor magyar szövege gyakorlatilag csak a jelölő (pl. H0001 `-/1/-`: „1.”), a tényleges szöveg a szomszédos sorban áll. Ok: az illesztő a jelölőket számmal, sorrendben keresi, és a szövegközi szám- vagy törzsnév-említéshez (a H0001-nél a forrás „Sabean אב CIS^iv, 1, 37 1. 2 and others” töredékéhez) köti őket; a kategória ilyenkor hamisan `illeszkedik`.

A hiba csak a magyar illesztés rétegében van: a szakasztábla (`bdb_szakaszok.tsv`), a fordítás (`forditasok.tsv`) és az igehely-feloldás (`bdb_vers_jelentes.tsv`) helyes.

**Hatókör a jelentés 26 szócikkéből:** a H1980, H7200, H7725, H7971 (2. szelet, `ff497bd`), valamint a H1129 és H7218 (3. szelet, `cc4bf75`) a #38 N-F107b újrafordításában szakaszonkénti fordítást kapott, a régi soruk `elavult`; ezeknél a szó-lap az új szakaszsorokat használja, ezért kikerülnek. Marad **20** (2026-10-25-i állapot; a #38 újrafordítása még fut, ezért az M0 a futáskor újraméri, melyik szócikk esett ki közben):

| Típus (a jelentés szerint) | Szócikkek |
|---|---|
| (a) szerkezeti, valószínűleg nem hiba | H3499, H4519, H6965, H7130 |
| (b) a jelölő szövegközi említéshez kötődött | H3423, H3603, H5324, H5826, H6299, H7122, H7378, H7650, H7896 |
| (c) fejléc-töredékes vagy bizonytalan | H0001, H2199, H3381, H5027, H5060, H6499, H7043 |

Ehhez jön a tágabb B-kör (≈70 szócikk, 79 sor: `illeszkedik`, jelölővel, 12 karakternél rövidebb szöveg), amelyet a jelentés nem vizsgált.

## 2. Hatókör

**Benne van:** a 20 szócikk soronkénti átnézése (EN szakasz ↔ magyar szöveg ↔ a jelölő helye); a `hu_illeszt.py` jelölőkeresésének javítása (a szövegközi szám-, sorszám- és törzsnév-említés nem jelölő: pl. mondatközi, zárójelen belüli, igehely-részként álló szám; a forrás fejléc-töredékének kezelése); tesztek (`teszt_hu_illeszt.py`: legalább a H0001, egy (b) és egy (a) eset); a tábla újragenerálása (`--ts`), a kategória-eloszlás újramérése az előtte–utána összevetéssel; a B-kör szúrópróbája (legalább 20 szócikk).

**Nincs benne:** a fordítás (`forditasok.tsv`) módosítása — az a #38-é; a szakasztábla (`bdb_szakaszok.tsv`) és az angol bontó (`bont.py`) módosítása; a szakaszonként fordított Strongok (azoknál az illesztés nem kell). A H0001 forrásbeli számtöredéke nem javítandó a forrásban (hűség), csak az illesztő nem köthet hozzá.

**`nem_fugg: [27, 38]`:** a #27 halasztott (D46), és csak a Thayer-sorokat érinti. A #38 a `forditasok.tsv`-t írja (új szakaszsorok, a régi sorok `elavult`-ra állítása), a #144 csak olvassa. A #144 az illesztést a régi (`teljes`) úton fordított, nem `elavult` sorokra végzi; a futás elején rögzíti a `forditasok.tsv` hash-ét, és a zárónaplóban megnevezi, mely Strongok estek ki közben a #38 újrafordítása miatt.

## 3. Lépések

**M0 — átnézés és szabály.** ⛔ Előbb újramérés: a 20 szócikk közül melyik kapott közben szakaszonkénti újrafordítást (`elavult` régi sor), az kiesik. A maradék soronként: a valódi ok, és hogy a javított illesztőnek mit kellene adnia (táblázat a naplóba). A (a) csoportnál annak eldöntése, hogy hiba-e. Javasolt javítási szabály (mit nem tekint jelölőnek), és a várható hatás becslése a teljes táblán (hány sor változik). Megállás: a felhasználó jóváhagyja a szabályt.

**M1 — javítás és tesztek.** A `hu_illeszt.py` a jóváhagyott szabály szerint; `teszt_hu_illeszt.py`; a meglévő `teszt_bont.py` is zöld.

**M2 — újragenerálás és mérés.** `python eszkozok/bdb_jelolt/hu_illeszt.py --ts <nap>`, majd `--ellenoriz`. Előtte–utána: kategória-eloszlás, a megváltozott sorok listája (Strongonként), a 20 szócikk eredménye, a B-kör szúrópróbája. Ha olyan sor változik, amely előtte helyes volt, megállás és jelentés.

**M3 — zárás.** Napló (`naplok/BDB_SZAKASZ_HU_JAVITAS_naplo.md`) proveniencia-sorokkal. ⛔ a felhasználó átnézi a változott sorok mintáját.

## 4. Elfogadási feltételek

- A (közben ki nem esett) szócikkek mindegyikéről a naplóban soronkénti ítélet; a (b) és (c) csoportban a javítás után nincs „csak a jelölő” `illeszkedik` sor, vagy indokolt kivétel van.
- A teljes táblán az A-feltétel (a jelentés 2. pontja) szerinti sorok száma mérve, előtte–utána.
- Nincs olyan változott sor, amely előtte helyes volt (a változott sorok mintája átnézve).
- `teszt_hu_illeszt.py` és `teszt_bont.py` zöld; a `forditasok.tsv`, a `bdb_szakaszok.tsv` és a `bdb_vers_jelentes.tsv` bájtra változatlan.

## 5. Döntésnapló

- Előzmény (2026-10-25, chat, `manual`): a felhasználó jóváhagyta, hogy a jelentésből új feladat legyen, a már újrafordított szócikkek nélkül (a befogadáskor hat: H1980, H7200, H7725, H7971, H1129, H7218).
