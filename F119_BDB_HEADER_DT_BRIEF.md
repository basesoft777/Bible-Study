---
feladat: 119
cim: A bdb_vers_jelentes.py fejléc-sorának DT-hivatkozásai a végleges számokra; a bukó teszt_bdb_vers_jelentes.test_bajtra_azonos javítása
kod: BDB_HEADER_DT
tipus: feladat
fazis: 1
munka: adat
modell: sonnet
allapot: fut
ag: claude/f119-bdb-header-dt
ad: az `adat/bdb_vers_jelentes.tsv` újragenerálva a javított generátorral (csak a 2. sor / a kód-hash változik), a `teszt_bdb_vers_jelentes.Ujrageneralas.test_bajtra_azonos` zöld a `python eszkozok/teszt_futtat.py` teljes futásán, más teszt eredménye nem változik
kovetkezo: a /kovetkezo indítja
olvas: [eszkozok/olvaso_szerver/bdb_vers_jelentes.py, eszkozok/olvaso_szerver/teszt_bdb_vers_jelentes.py, eszkozok/szamkiosztas.py, naplok/ELLENOR_F115.md, adat/SEMA.md]
ir: [eszkozok/olvaso_szerver/bdb_vers_jelentes.py, adat/bdb_vers_jelentes.tsv]
fugg: []
nem_fugg: [76, 102, 103, 104, 105, 106, 107, 115]
---
# F119_BDB_HEADER_DT_BRIEF.md — a bukó `test_bajtra_azonos` javítása

*FELADATOK #119 · Modell: sonnet · v1 · 2026.10.18 · előzmény: #99 (F99, a generátor), #115 (ELLENOR_F115 G7)*

## 1. Mért állapot (main, `8965b53f`, 2026.10.18)

A `teszt_bdb_vers_jelentes.Ujrageneralas.test_bajtra_azonos` (`eszkozok/olvaso_szerver/teszt_bdb_vers_jelentes.py:272`) a tábla 2. sorából kiolvassa a `--ts` értéket (`2026-10-16`), újragenerál (`V.general(ts)`, `V.kiir(...)`), és **bájtra** összeveti a meglévő `adat/bdb_vers_jelentes.tsv`-val.

Mérés (Windows-Python, a tesztfüggvény lépései ugyanazzal a `--ts`-sel): 160 620 sor mindkét oldalon, **pontosan 1 sor tér el: a 2. (a `# forras:` fejlécsor)**; a 3. sortól az adatsorok bájtra azonosak. Az eltérés **nem hash**: a BDB-, Macula- (39 fájl, `cd5307d181c7`), versmegfeleltetés-, Károli-, F85-, OSHL-, Strong-, TAHOT- és kód-hash is egyezik (a #115 PR által frissített Macula-hash már jó). Az eltérés a **döntésszámok szövege**:

| | a generátor `kiir()` (`bdb_vers_jelentes.py:266-270`) | a tábla 2. sora |
|---|---|---|
| ma | `DT-F99n`, `DT-F99h`, `DT-F99g`, `DT-F99a`, `DT-F99i`, `DT-F99j`, `DT-F99k` | `DT179`, `DT173`, `DT172`, `DT166`, `DT174`, `DT175`, `DT176` |

**Ok:** a `szamkiosztas` Action (`eszkozok/szamkiosztas.py`) a helyőrzőket csak `*.md` és `*.tsv` fájlokban cseréli (`szamkiosztas.py:106,121`). A tábla fejlécében a számok véglegesedtek (`0d7e9dec`), a generátor `.py` fájljának string-literáljaiban a `DT-F99*` helyőrzők maradtak. A tábla tehát egy olyan fejlécet hordoz, amit a generátor már nem tud előállítani. A hiba a `main`-en a `szamkiosztas` óta áll fenn; a #114 zárójelentése (`naplok/TSK_VERSSZAM_zaras.md:22`) már „DT-F99n/DT179 számozás”-ként rögzítette, a #115 ELLENOR_F115 G7 pontja a Macula-hash-t is említi, az pedig a #115 PR-ban már rendbe jött.

## 2. Javítás helye

A **generátor** a hibás, nem a teszt (a teszt elvárása — bájtra azonos újragenerálás — helyes). Teendő:

1. `eszkozok/olvaso_szerver/bdb_vers_jelentes.py`, `kiir()` (a 266-270. sor körül): a fejlécben kiírt `DT-F99a/g/h/i/j/k/n` → `DT166/172/173/174/175/176/179` (a leképezés a `0d7e9dec` szamkiosztas-commitból; a sorrend és a szöveg a táblában álló szerint). A kód többi része és a kommentek tartalmilag nem változnak (kommentekben a helyőrző maradhat, nem kerül a kimenetbe; ⛔ ha a végrehajtó mégis kommenteket is átír, a diffet külön jelzi).
2. Az `adat/bdb_vers_jelentes.tsv` újragenerálása **`--ts 2026-10-16`-tal** (a ts a tábla sorainak proveniencia-mezőjében áll, nem változhat), a CLI-ből: `python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts 2026-10-16`. A kód módosult, ezért a `kód: …@` hash a 2. sorban új értéket kap: ez várt.
3. Ellenőrzés a kiírás előtt és után: a `git diff --stat adat/bdb_vers_jelentes.tsv` **csak a 2. sort** érintse (1 sor ki, 1 be); ha adatsor változik, megállás és jelzés (nem várt: a kimenet a 3. sortól már azonos).

Alternatíva, amit **nem** javaslunk: a tábla fejlécének kézi visszaírása `DT-F99*`-ra (a tábla `GENERÁLT`, kézzel nem szerkeszthető, és a `szamkiosztas` a következő futásnál újra megbontaná), vagy a teszt fejlécsor-kivételezése (a bájt-teszt lényege, hogy a fejlécet is védi: ELLENOR_F99 3.).

## 3. Hatókör

**Benne:** a fenti két fájl; futtatás a `python eszkozok/teszt_futtat.py` hívással (WSL, `~/pardes/pardes.db`).

**Nincs benne:** a #76 (`olvaso_szerver/` többi fájlja), a #107 (`bdb_jelolt/`, `adat/bdb_*` további táblái), a #115, #117, #118, #11, #111 fájljai. **Átfedés-jelzés:** a `eszkozok/olvaso_szerver/` és az `adat/bdb_*` név a #76-tal, illetve a #107-tel rokon terület; a brief csak a fenti két konkrét fájlt írja. Ha a végrehajtáskor akár a generátort, akár a táblát az ottani ág is módosítja, a végrehajtó megáll és jelez.

**Rendszerszintű észrevétel (külön N-tétel, nem e feladat része):** a `szamkiosztas` nem nyúl `.py`-hoz, így minden generátor, amely `DT-F…` helyőrzőt ír a kimenetébe, ugyanígy megbukik. A végrehajtó csak jelzi (N-F119a helyőrzővel); a gyógymód (generátor ne tartalmazzon helyőrzőt, vagy a `szamkiosztas` bővítése) tartalmi döntés.

## 4. Elfogadási feltételek

- **G1.** `python eszkozok/teszt_futtat.py` (teljes) ezen a teszten (`teszt_bdb_vers_jelentes`, minden teszt) zöld.
- **G2.** Más teszt eredménye nem változik: a futás előtti és utáni FAIL/OK-szám összevetve (a #76 M3 mért alapja: 276 OK, 1 FAIL → 277 OK, 0 FAIL, ha közben más ág nem módosít).
- **G3.** `git diff` a két fájlra: a generátorban csak a fejléc-literálok (és a várt egyéb sorok, ha a végrehajtó kommenteket is érint, jelezve); a táblában csak a 2. sor.
- **G4.** `python eszkozok/olvaso_szerver/bdb_vers_jelentes.py --ts 2026-10-16 --ellenoriz` kimenete „bájtra azonos”.
- **G5.** `python eszkozok/feladatok.py ellenoriz` 0 hiba.

## 5. Megállási pontok

Nincs tartalmi döntés. Megállás: ha a G3 szerint adatsor is változik; ha a teszt a javítás után sem zöld (a mért ok egyetlen sor, tehát más ok kell); ha a #76/#107 ága a két fájlt közben módosította.
