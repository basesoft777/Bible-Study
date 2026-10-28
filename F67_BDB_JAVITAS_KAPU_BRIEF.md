---
feladat: 67
cim: A javított BDB-hivatkozás kapuja — a fordító Y-ja és a javítótábla összevetése
kod: BDB_JAVITAS_KAPU
tipus: feladat
fazis: folyamat
munka: folyamat
modell: sonnet
allapot: megallt
ag: ccr-f67-bdb-javitas-kapu
ad: egy kapu az eszkozok/forditas_kapuk.py-ban, amely a fordítás [BDB: X] / Y hivatkozását összeveti az adat/bdb_igehely_javitas.tsv javitott_hivatkozas értékével, tesztekkel
kovetkezo: "Te: független ellenőrzés (naplok/ELLENOR_F67.md), utána push és PR"
olvas: [adat/bdb_igehely_javitas.tsv, adat/SEMA.md, adat/forditasok.tsv, adat/bdb_szakaszok.tsv, eszkozok/forditas_kapuk.py, eszkozok/emeles.py, eszkozok/bdb_adatblokk.py, eszkozok/bdb_atvezet_m5.py, forditas/prompt_v4.md, F56_BDB_ADATBLOKK_BRIEF.md, F38_BDB_FORDITAS_BRIEF.md, konkordancia/Konyv_normalizalo_tabla.tsv]
ir: [eszkozok/forditas_kapuk.py, eszkozok/teszt_forditas_kapuk.py, eszkozok/emeles.py, eszkozok/teszt_emeles.py]
fugg: [56]
nem_fugg: [27, 38, 121]
---

# F67_BDB_JAVITAS_KAPU_BRIEF.md — A javított BDB-hivatkozás kapuja

*FELADATOK #67 · Modell: sonnet · v1 · 2026.10.28 · a csonk (2026-10-06, a #56 zárójavaslataiból) kitöltése; DT55: a #38 9. adagja előtt*

## 1. Cél

A `konkordancia/BDB_teljes_unabridged.tsv` néhány hivatkozásának fejezetszáma nem létezik (pl. `Eccl 17:10`). A javítás az `adat/bdb_igehely_javitas.tsv`-ben él (SEMA 2.23). A fordító a `javitva` sorokat az adatblokk 6. szakaszából kapja, és a prompt v4.2 szerint `Y [BDB: X]` alakkal írja (Y a helyes, X a forrás alakja Károli-rövidítéssel).

Ma ezt semmi nem ellenőrzi. A 13. kapu az `[BDB: …]` tartalmát kihagyja, a többi kapu a `Y [BDB: X]` → `X` visszaállított szöveget látja. Ha a fordító a jelölést elhagyja, rossz Y-t ír, vagy olyan hivatkozást jelöl, amely `jelolt_marad`, az hiba nélkül átmegy.

A cél egy gátoló kapu, a `17_bdb_javitas`, amely a fordítás jelöléseit a javítótáblához méri. Ezt a #38 a 9. adagtól használja (a 9. adagban két `javitva` Strong van: H5377 és H0479; a H2597 a 11. adagban).

## 2. Hatókör

**Benne van:**
- az új kapu függvénye az `eszkozok/forditas_kapuk.py`-ban, a `GATOLO` listában;
- a `kapuk_futtat` és a `kapuk_futtat_szakaszos` új, opcionális `strong=None` paramétere;
- az `eszkozok/emeles.py` BDB-hívásai (`utofeldolgoz_szakasz`, és a teljes soros út, ha ott a Strong ismert) átadják a Strongot;
- tesztek (`teszt_forditas_kapuk.py`, szükség esetén `teszt_emeles.py`);
- regressziós futtatás a meglévő BDB-sorokon, napló a `naplok/BDB_JAVITAS_KAPU_*` alá.

**Nincs benne:**
- a javítótábla újraépítése vagy módosítása (generált, a #56 eszköze írja);
- fordítás, adatsor módosítása (`adat/forditasok.tsv` nem változik);
- a Thayer-lánc (`thayer_kapuk.py`); a kapu Thayerre és Strong nélküli hívásra nem fut;
- a többi hívó (`naplok/BDB_FORDITAS_*.py`, `teszt_bdb_zaras.py`) átírása: ezek Strong nélkül hívnak, a kapu ott `RENDBEN` „nem alkalmazható” eredményt ad, a viselkedésük nem változik.

## 3. Lépések

**M0. Modell-ellenőrzés** (CLAUDE.md). Ág: a `main`-ről nyitott saját ág.

**M1. A kapu** (`17_bdb_javitas`, csak `szotar == 'BDB'` és megadott `strong` esetén). Bemenete a nyers fordítás (a `bdb_jeloles_vissza` előtti), a forrás és a Strong (`H5377`, `H0479` stb.; a homográf-betűs kulcsra, pl. `H0090a`, a táblában `Strong_padded` áll). A javítótábla sorai a Strong kulcsán:

1. **Hiányzó vagy rossz javítás:** minden `javitva` sorra, ahányszor a forrásban a `forras_hivatkozas` előfordul (könyvnévvel, határolva: `Ezra 16:8` nem találat a `Ezra 16:80`-ban), annyiszor kell a fordításban `Y [BDB: X]` alaknak állnia, ahol Y = `javitott_hivatkozas`, X = a forrás-hivatkozás Károli-rövidítéses alakja (a `bdb_adatblokk.regi_alak` szerint, pl. `Ezsd 16:8`). Hiány, eltérő Y, vagy X jelölés nélkül (csupaszon) → `SERTES`.
2. **Jogosulatlan jelölés:** minden `[BDB: X]` a fordításban egy `javitva` sorhoz tartozik, egyező Y-nal. Ami `jelolt_marad` sorhoz vagy a táblában nem szereplő X-hez tartozik → `SERTES` (a `jelolt_marad` hivatkozás a forrás alakjában marad, SEMA 2.23).
3. Ha a Strongnak nincs sora a táblában, és a fordításban nincs `[BDB:` → `RENDBEN`.

A részlet a hibás hivatkozásokat nevezi (`hiányzik: Abd 1:7 [BDB: Abd 3:7]`; `jogosulatlan: …`).

A könyvnév-leképezés a meglévő táblából jöjjön (`konkordancia/Konyv_normalizalo_tabla.tsv`, ahogy a `bdb_adatblokk.konyv_minta`). **Körkörös importot ne vezess be:** a `bdb_adatblokk.py` már importálja a `forditas_kapuk`-at. A javítótáblát a kapu maga olvassa (`split('\t')`, a `#`-sor és a fejléc kihagyásával), egyszer, gyorsítótárazva.

**M2. Bekötés.** `kapuk_futtat(szotar, forras, forditas, bizonytalan=(), strong=None)` és `kapuk_futtat_szakaszos(..., strong=None)`. A szakaszos változat a tokenek nélküli szövegen futtatja a kaput. Az `emeles.py` BDB-útjai a Strongot átadják; a `--kapu-felulir` mechanizmus (DT-F38s) a 17. kapura is működik. A meglévő hívók paraméter nélkül változatlanul futnak.

**M3. Tesztek.** Legalább: a H7223 `Eccl 17:10` → `Préd 7:10 [BDB: Préd 17:10]` `RENDBEN`; jelölés hiánya, rossz Y, csupasz X, `jelolt_marad` hivatkozás jelölése, ismeretlen X jelölése → `SERTES`; Strong nélküli hívás és Thayer → a kapu nem gátol; többszöri előfordulás; szakaszos hívás. A teljes `teszt_forditas_kapuk.py` és `teszt_emeles.py` zöld.

**M4. Regresszió és mérés.** A kaput lefuttatod minden BDB-soron az `adat/forditasok.tsv`-ben (a teljes és a szakaszos sorokon, a forrás az `emeles.py` szerinti), a Strong megadásával. Várt eredmény: a 4 már jelölt szócikk (H5002, H5046, H4427, H7223) `RENDBEN`, máshol nincs `SERTES`. Külön sor a H6297-re (DT-F38t (5)). A szkript és az eredmény: `naplok/BDB_JAVITAS_KAPU_regresszio.py` és `naplok/BDB_JAVITAS_KAPU_naplo.md` (szócikkenként, proveniencia-sorral).

⛔ **M4-megállás:** ha a regresszió bármely meglévő soron `SERTES`-t ad, a sort nem javítod (adatot ez a feladat nem ír); a listát a naplóba írod, és megállsz. Hogy kapuhiba vagy fordítási hiba, és mi legyen vele, a felhasználó dönti el (helyőrzős `DT-F67a`).

**M5. Zárás.** A `F38_BDB_FORDITAS_BRIEF.md` fejlécét ez a feladat nem írja; a #38 9. adagjának menete teszi a saját `fugg` mezőjébe a 67-et (a csonk kovetkezo-ja szerint). Tételenként commit (`F67.<n>: …`), UTF-8 fájlból.

## 4. Elfogadási feltételek

- A `17_bdb_javitas` a `GATOLO` listában van, és a fenti esetekben gátol.
- Strong nélküli és Thayer-hívásnál a kapusor eredménye bájtra azonos a mostanival (teszttel igazolva).
- `python eszkozok/teszt_forditas_kapuk.py`, `python eszkozok/teszt_emeles.py`, `python eszkozok/bdb_jelolt/teszt_szakasz_bemenet.py` zöld.
- A regresszió naplózva, 0 `SERTES`, vagy a ⛔ M4 szerinti megállás.
- `adat/` és `konkordancia/` bájtra változatlan.

## 5. Döntésnapló

- DT55 (b): a kapu a #38 9. adagja előtt készül el.
- A kapu sorszáma 17, mert a 16. (`16_sigla`) a Thayer-láncé (`thayer_kapuk.py`).
- (M4 ⛔ esetén) `DT-F67a` helyőrzővel.
