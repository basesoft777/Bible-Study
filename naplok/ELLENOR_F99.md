# ELLENŐR — #99 BDB_SZELETELO

*A `fuggetlen-ellenor` subagent jelentése (claude-opus-5-5, a kért `opus`); az ellenőrnek nincs író eszköze, a jelentést az orkesztrátor mentette. Tartomány: `origin/main..HEAD` = `f44ff8dc..32b20b9e`, 32 commit (F99.0–F99.31). A helyi `main` elavult, ezért nem azt használta. Csak olvasott; a tesztek, az `ellenoriz.py`, a `feladatok.py ellenoriz`, a `bdb_szelet_m0.py --arany` és a `regiszter_or.py` futtatása nem fért a szerepébe (NEM ELLENŐRIZHETŐ).*

**Eredmény: ELTÉRÉS, 10 tétel.**

## Mérföldkövek
A brief-fejléc, a napló 0. pontja és a zárás-tervezet egybehangzóan nem késznek mondja az M3-at, az M4 nagy részét, az M5-öt és az M6-ot; a diff is ezt mutatja (nincs `bdb_magyarazat_proba.tsv`, `terminologia.tsv`-/`konfig/bdb_jelek.tsv`-változás, „ebben a versben”, kattintható hely, csoportsor). Kész: M0, M1, M2 (a mérce nélkül), az M4-ből a DT168 és a DT177 felirata. Az elfogadási feltételek közül nem teljesült: aranyminta 0 eltérés; jelentéspont ≥97% (92,0%, DT177 (c)).

## ELTÉRÉS-ek súlyossági sorrendben
1. **Rendszeres Károli-kulcs-hiba, kb. 541 sor** a DT173 (b) után is: Ézs 3 (+1, 180 sor), Hós 2 (−1, 164), 1Krón 12 (+1, 78), Ézs 64 (−1, 65), 5Móz 5 (+3, 54). Az Ézs 3 igazolva: `lekerdez.py karoli "Ézs 3:1"` → MT 2:22 szövege; `scan H0113 --szakasz "Ézs 3"` → csak 3:2, a tábla viszont MT 3:1 → Károli 3:1 (`azonos_f85`). Nem szerepel nyitott tételként, a `datasetek.tsv`-megjegyzésben sem; a javítási brief-tervezet a Károli-kulcsot kizárja (`beerkezo/…:119-120`).
2. **A szűrés hamis pozitív/negatív aránya nincs kiszámolva és elbírálva a seed-101-en** (elfogadási feltétel). Igazolt hamis pozitívok: H2623 „116:15” (és a 149:1/5/9, 4 sor; `scan H2623 --szakasz "Zsolt 116"/"Zsolt 149"`), H4912 „1:1” (`scan H4912 --szakasz "Péld 1"` → 1:1), H8034 „Hosea 2:19” (M223, `sigla_kozel`). Hét `sigla_igazolt` eltérés (M054, M065, M147, M149, M191, M198, M230) nincs elbírálva.
3. **A „bájtra újragenerálható” állítás platformfüggő:** a fejléc kód-hash-e a munkafa fájlbájtjainak sha256-ja; a `.gitattributes` a `*.py`-ra nem ír elő LF-et, a repó `core.autocrlf=true`-val megy (`bdb_szelet.py` 877/877 sor CRLF); egy LF-es klónon más a hash, a `--ellenoriz` „ELTÉR”-t adhat. A bájt-teszt csak `os.name=='nt'` vagy `PARDES_LASSU` mellett fut.
4. **A fejléc proveniencia-sora hiányos (DT172, SEMA 2.29):** a `Macula_heber_*`, az `F85_macula_elvetve.tsv`, az `OSHL_lexikalis_index.tsv` hash nélkül áll, a `Strong_szotar.tsv` nincs felsorolva; a kód-hash kihagyja a `bdb_konyv_javit.py`-t és a `normalizal.py`-t (LEK, LANCTORO, TOBBERTELMU).
5. **A teszt rögzíti az ismert hibát:** `eszkozok/olvaso_pilot/teszt_olvaso_pilot.py:666` a H3027-re `1(ab) 2 3(abcde)…`-t vár „az aranyminta szerint”; az aranyminta (`adat/bdb_aranyminta.tsv:466-476`) `-/1/a`…`-/1/e` alpontot rögzít és a hibát kimondja.
6. **Az OSHL (CC BY) hiányzik az `ADAT_LICENC`-ből** (`eszkozok/sqlite_epit.py:391-394`): a `bdb_id` oszlop OSHL-adat; a TAHOT is dönt (szűrés, Károli-kulcs).
7. **A DT167 (4) időzítése a #38-hoz nincs bekötve** (a `terminologia.tsv` nem változott; a `F38_BDB_FORDITAS_BRIEF.md`-ben és a `dontes_hatas.tsv`-ben nincs F99-hivatkozás): ha a #99 az M3 nélkül zárul, a kötés elárvul.
8. **Hiányzó nyitott tételek:** az N-F99a és N-F99b nincs a `NYITOTT_FELADATOK.md`-ben (csak az N-F99c); az M027 (Neh 7:68, legalább 3 sor: H2543, H1581 is, `tobb_karoli_vers`) és a maradék Károli-eltolás sem.
9. **Téves megjegyzés:** `eszkozok/olvaso_szerver/bdb_szelet.py:750-758`: a megjegyzés szerint lezáró zárójel/pontosvessző/gondolatjel után a hely bibliai; a kód `sigla_kozel`-t ad, ha a lista nem illeszkedik (a DT176 miatt a TAHOT dönt); a teszt (`teszt_bdb_vers_jelentes.py:74-75`) ezt rögzíti. Az M223 hamis pozitívja ebből jön.
10. **Hiányos `ir` lista:** a brief `ir`-jéből hiányzik a `naplok/ELLENOR_F99_minta.md` (F99.5).

## OK pontok (rövid)
Tábla séma és sorszám (160 616 sor, 15 mező, nem üres `utvonal`, `konyv_feloldas`/`vers_feloldas` értékkészleten belül); proveniencia minden soron, `manual` 0; `csv` modul-tilalom (0 találat); SEMA 2.29/`datasetek.tsv` (4 sor, „korlatos”, 92,0% [87,3–95,4%]); CLAUDE.md 2. szabály (a `jeloltek.tsv`, `elofordulasok.tsv`, motívumfájlok érintetlenek); a `FORRAS_HIBA` lista saját lekérdezéssel igazolva (H1802 → Móz 2:16/19, H7804 → Dán 3:15); DT168 (a pilot csak betöltő); a szó-lap felirata (92,0%, a 93,5% csak a tesztben `assertNotIn`); M1 gyökcsalád (main 2643, sub 4368, single 574); DT166/h/i/j/k számai (`sigla_igazolt` 484; szűrt 531 = 330+112+86+3); a seed-100 nem lett zöldre javítva; a vak minta vak; a brief-fejléc (`dontesre_var`); a brief-tervezet nem befogadott; E12–E15: 0 találat; a ⛔ pontoknál minden megállás megvolt; táblánkénti Δ egyezik a naplóval.

## NEM ELLENŐRIZHETŐ
DT170 felhasználói átnézése (a H1242, H0776, H7451, H3615, H0559 átnézésének nincs nyoma; 51 `modell_ellenorizetlen` sor); az aranyminta-számok (EN 7/32, HU 4/14); a tesztek, az `ellenoriz.py`, a `feladatok.py ellenoriz`, a `regiszter_or.py`; a fejléc-hash helyessége; a vak kitöltők modellje (a Co-Authored-By: 28 commit Opus, 4 Sonnet: F99.5, F99.15, F99.20, F99.26 az orkesztrátor mentései/összevetései).

*Megjegyzés: a DT177 kapuja az ítélet előtt rögzült, de a 184/200 nyers szám ismeretében; a küszöbök ezt látva születtek.* A merge-ről a felhasználó dönt.
