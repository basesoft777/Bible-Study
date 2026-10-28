# F123 X.A — az ALVIL-001 adat-előkészítése (munkafájl)

*#123 MIGRACIO2 · 2b. 1. lépés (`munka: adat`) · ág: `claude/f123-alvil-adat` · modell: claude-opus-5-5 · 2026-10-28*

*Döntés nélküli munkafájl: jelentéstartományt nem választ, prózát nem ír, motívumfájlt (`motivumok/`, `tematikus_lezart/`, `lexikon/`) és adattáblát (`adat/*.tsv`) nem ír (2b). A teljes sorok a mellékelt TSV-kben állnak, minden sor mellett a lekérdezés proveniencia-sorával; ez a fájl összegzés. A lekérdezések naplója: `naplok/F123_lekerdezesek.tsv` (`lekerdez.py --naplo F123`). Munkaszkript: `naplok/F123_adat_keszito.py` (alparancsok: `f108`, `szotar`, `proza`, `seol`).*

*Hatókör (DT-F123b, A út): most csak az X.A fut; a szétválasztás (M1–M5), a `motivumok/ALVIL-001.md` forrás és a lexikongenerálás a #131 merge-e után (N-F11d).*

## 1. A törzs összevetése a #108 eltérés-táblájával (2c)

**A törzs nincs újra levezetve** (2c): a meglévő `adat/elofordulasok.tsv` és `adat/jeloltek.tsv` ALVIL-001-sorai vannak összevetve a `naplok/F108_ujrascan_elteresek.tsv` (2026-10-17) ALVIL-001-soraival, és a motívum két Strongjára (H7585, G0086; az `elofordulasok.tsv` `strong` / `gerinc_elem` oszlopa: 64 + 8 sor) a mai TAHOT/TAGNT-en lefutott a scan.

| Mérés | Eredmény |
|---|---|
| `elofordulasok.tsv` ALVIL-001-sorok (ma / F108) | 72 / 72 — a kulcs (igehely + strong) mind egyezik; **új vagy eltűnt sor: 0** |
| `jeloltek.tsv` ALVIL-001-sorok (ma / F108) | 74 / 74 — **új, eltűnt vagy döntést váltott sor: 0** |
| F108-osztály, E-sorok | 57 `rendben`, 15 `zsoltar_55` (mind a 15: „mert osztaly: rendben”, azaz a `zsoltar_55` csak a #55-re utaló osztályozás, a kulcs rendben) |
| F108-osztály, J-sorok | 59 `nincs_strong` (TSK/frázis/kézi forrás, kulcs nem ellenőrizhető), 15 `zsoltar_55` |
| mai scan H7585 | 64 igehely (66 szó-előfordulás); 64 E-ben, 0 csak J-ben, **0 új**; E-sor, amelyet a scan nem ad: 0 |
| mai scan G0086 | 10 igehely; 9 E-vers, 1 csak J-ben (Mt 16:18, `elutasítva` — meglévő döntés, nem változás), **0 új**; E-sor, amelyet a scan nem ad: 0 |
| #110 szűrő | **nem alkalmazandó:** a szűrő az F108 tág gerinc-Strongjainak új helyeire szól (`F110_SZURO_PILOT_ISTENTISZT_BRIEF.md`); az ALVIL-001 két Strongja szűk (64, 10), és új hely nincs |

**Eredmény: eltérés nincs.** Gerinc-elemet érintő változás (Strong be/ki) nincs, ⛔ nem keletkezik; az értelmező menetnek a törzsben nincs mihez nyúlnia (a #109 mintájára csak eltérésnél kellene).

Részletes sorok: `naplok/F123_adat_ALVIL-001_f108_osszevetes.tsv` (146 kulcs-sor + 1 `ujrascan` csak-J sor).

Proveniencia:

- `scope=ALVIL-001: adat/elofordulasok.tsv (72 sor) + adat/jeloltek.tsv (74 sor) × naplok/F108_ujrascan_elteresek.tsv (146 sor) | forras=split('\t'), ág claude/f123-alvil-adat | ts=2026-10-28T15:10Z`
- `scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H7585 | n=64 | ts=2026-10-28T15:10Z | csatorna=cli`
- `scope=TAGNT-teljes | forras=TAGNT_kivonat.tsv | strong=G0086 | n=10 | ts=2026-10-28T15:10Z | csatorna=cli`

## 2. Szótári sorok, hiányzó fordítások, szerepenkénti nyers kínálat (2b)

A motívum Strongjai az `elofordulasok.tsv` szerint: **H7585** (64 sor) és **G0086** (8 sor). Rokon szavak (pl. a felmérés kísérő szavai) itt nincsenek gyűjtve: a szótári kínálat a gerinc-Strongokra szól; a kísérő szavak a 3. szakaszban, mért tényként.

**Szótári sorok:** 87 sor, `naplok/F123_adat_ALVIL-001_szotar.tsv` (forrás, kulcs, hossz, SHA-1-előtag, 160 karakteres kivonat, a generátor szerinti `forditasok.tsv`-kulcs és annak állapota, proveniencia). A teljes szövegek a forrásfájlokban maradnak; a kivonat csak azonosításra szolgál.

**Szerepenkénti nyers kínálat** (`adat/szotar_szerepek.tsv`, 13 szerep × 2 nyelv): `naplok/F123_adat_ALVIL-001_szerepkinalat.tsv`. Mind a 26 szerephez van sor; üres szerep nincs. Három szerep nem szótári forrás, hanem jelölt állapot: 10. kiejtés (héber: jóváhagyott kivétel-sor nincs, a render a STEP-átírást adja; görög: render-időben számolt), 12. Nave (nem Strong-kulcsú: a motívum 73 versére illesztve), 14. rejtett/hamis párhuzam (a 13. szerepből render-időben származtatott, itt nem gyűjtve). Jelentéstartomány nincs kiválasztva (az a 2. lépés D50-döntése).

**Hiányzó fordítások — 13 kulcs** (`naplok/F123_adat_ALVIL-001_forditas_hiany.tsv`; a kulcsok a `lexikon_general.py` `forditas_ehhez` hívásai szerint; **a `forditasok.tsv`-be nincs írva**, a pótlás külön adatfeladat, 2b):

| Szótár | Strong | Kulcs (entry_id / jelentes_szam / mező) | Szerep |
|---|---|---|---|
| TBESH | H7585 | H7585 / teljes / forditas_hu | héber 1 |
| BDB | H7585 | H7585 / nyelvi_hatter / forditas_hu (a határ `gepi`) | héber 8 |
| UBS_DBH | H7585 | 007131001001000 / — / definicio_hu | héber 4 |
| UBS_DBH | H7585 | 007131001001000 / — / glosszak_hu | héber 5 |
| tW_szocikkek | H7585 | kt/hades, kt/hell / — / forditas_hu (a tW-cikk első Strongja H7585; a görög oldal ugyanezt a két kulcsot kérné) | héber/görög 3 |
| tW_szocikkek | H0875 | other/pit / — / forditas_hu (a cikk H7585-öt is felsorol) | héber 3 |
| tW_szocikkek | H1430 | other/tomb / — / forditas_hu (a cikk H7585-öt is felsorol) | héber 3 |
| TBESG | G0086 | G0086 / teljes / forditas_hu | görög 1 |
| UBS_DNTG | G0086 | 000086001003000 / 12.50 / definicio_hu, glosszak_hu | görög 4–5 |
| MCGED | G0086 | G50087 / — / glosszak_hu | görög 5 |
| LSJ | G0086 | G0086 / teljes / forditas_hu | görög 8 |

Megvan: BDB H7585 `teljes` (`kezi`), Thayer G0086 sz1–sz4 (`sonnet`; a `teljes` sor `elavult`), UBS_DNTG G0086 1.19 és 23.108 (`kezi`), `glosszak_heber_hu.tsv` H7585.

**A #131-re tartozó megfigyelés (nem hiány):** a BDB H7585-nek 11 szakasza van (`adat/bdb_szakaszok.tsv`), `sz<n>` fordítási sora egy sincs; a DT290 (3) szerint a `kezi` `teljes` sor az érvényes, amíg a szakaszsorok nem mind `kezi`-k. A szakasztáblára álló render (#131) ezen a Strongon tehát a `teljes` sort kapja; ezt az értelmező menet a #131 merge-e után ellenőrzi.

Proveniencia: minden sor saját proveniencia-mezővel (a `szotar`/`szerepkinalat`/`forditas_hiany` TSV utolsó oszlopa); a futás: `scope=ALVIL-001 Strongjai (H7585, G0086) × adat/szotar_szerepek.tsv | forras=naplok/F123_adat_keszito.py szotar | ts=2026-10-28T15:12Z`

## 3. Felmérő lekérdezés (2d. 1.) — `eszkozok/motivum_felmeres.py`

Az eszköz a #123 első motívumánál készült (2d. 1.), motívumfüggetlen (`python eszkozok/motivum_felmeres.py <ID> --ki naplok/F123_felmeres_<ID>`). Kimenet: `naplok/F123_felmeres_ALVIL-001.md` (összegzés, paraméterek, proveniencia) és három TSV, **teljes egészében az értelmező menet elé** (2c, „A tengely”). **Mért tény, nem állítás:** a szomszédos motívum és a közös szókészlet csak jelöltként mehet tovább (`jeloltek.tsv`, 2. szabály), a közös szókészlet nem bizonyít idézést.

**Adatforrás-eltérés a brieftől:** a brief „friss `pardes.db`”-t ír; a repó `pardes.db`-je (a fő checkoutban) 2026-10-14-i építés, régebbi az ág tábláinál. Az eszköz ezért a kanonikus TSV-kből olvas (`adat/elofordulasok.tsv`, `adat/motivumok.tsv`, `konkordancia/TAHOT_kivonat.tsv`, `TAGNT_kivonat.tsv`, `adat/grammatikai_strongok.tsv`, a `lekerdez.py` betöltőivel), így építés nélkül az ág aktuális adatán fut. Ugyanazok a táblák kerülnek a `pardes.db`-be (DT28).

| Blokk | Eredmény | Fájl |
|---|---|---|
| (a) kísérő szavak | 377 Strong a motívum 73 versében (ebből 2 a saját gerinc: H7585, G0086); 56 grammatikai Strong kizárva | `naplok/F123_felmeres_ALVIL-001_kiserok.tsv` |
| (b) szomszédos motívumok, azonos fejezet | 10 fejezet×motívum pár, 4 motívum: HODIT-001 4 (Jób 26, Péld 9, Zsolt 88, Ézs 14), TEREMT-001 3 (Ez 31, Jel 20, Jón 2), ISTENTISZT-001 2 (ApCsel 2, Zsolt 116), HAMART-001 1 (Hab 2); közös vers: Ez 31 (TEREMT-001), Péld 9:18 és Ézs 14:9 (HODIT-001) | `naplok/F123_felmeres_ALVIL-001_szomszedok.tsv` |
| (c) válasz-szavak ±3 vers (H6030, H8085, G0191, G1522, G0611) | 24 találat 20 motívumversnél: H8085 12, H6030 6, G0191 5, G0611 1 | `naplok/F123_felmeres_ALVIL-001_valasz.tsv` |

A (b) két ISTENTISZT-001-párja (Zsolt 116:3 ↔ 116:4; ApCsel 2:27, 31 ↔ 2:21) a 2e. 3. pont két háló-jelöltje; a `jeloltek.tsv`-be írásuk az értelmező menet dolga (döntéssel), most nem került be.

A (c) válasz-szavainak listája a felmérés példája („felel/meghall”) szerinti paraméter (`--valasz`), nem mező-hipotézis; a (c) a fejezethatáron nem lép át.

Proveniencia: a `naplok/F123_felmeres_ALVIL-001.md` három sora (ts=2026-10-28T15:13Z) és minden TSV-sor utolsó mezője.
