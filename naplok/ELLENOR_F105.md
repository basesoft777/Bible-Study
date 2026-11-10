ELTÉRÉS: 7 tétel

# ELLENOR_F105 — `F105_BDB_SZOREND_BRIEF.md` · `b2317a2e..ac56f668`

*A merge-base az `origin/main`. Az `origin/main` közben `75b04e6a`-ra lépett; ez egyetlen `szamkiosztas` commit.*

*Ellenőr: a `fuggetlen-ellenor` subagent, `claude-opus-5-5`. A jelentést az orkesztráló session írta fájlba, szó szerint az ellenőr válaszából, mert az ellenőrnek nincs fájlíró eszköze. A Bash-köre a `git diff`/`git log`/`lekerdez.py`/`futtat.py` hívásokra korlátozódik. Ugyanezért a teszteket, a `--ellenoriz`-t és az összevető szkriptet nem futtatta: ezek NEM ELLENŐRIZHETŐ sorok, és a javítókörben futnak.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | A végrehajtó tényleges modellje `claude-opus-5-5`, a kért `opus`. Mind a 11 commitban `Co-Authored-By: Claude Opus 5.5` áll. |
| 0 modell (kitöltők) | NEM ELLENŐRIZHETŐ | `naplok/F105_naplo.md:198` | A két vak kitöltő tényleges modellnevét a napló nem rögzíti, csak annyit ír: „Opus-kitöltő”. |
| Elfogadás: a forrás bájtra változatlan | OK | – | `git diff --numstat origin/main HEAD -- konkordancia/ lexikon/` → 0 sor. |
| Elfogadás: a gépi arány és a minta a naplóban | OK | `naplok/F105_naplo.md:177-218` | Az aritmetika stimmel: 10 483/12 308 = 85,17%; 12 287/12 308 = 99,83%; 12 287+20+1 = 12 308; 1 825 = 1 748+69+6+2. Az újramérés futtatása NEM ELLENŐRIZHETŐ. |
| Elfogadás: a meglévő tesztek zöldek | NEM ELLENŐRIZHETŐ | – | A `teszt_futtat.py --gyors` és a `teszt_bdb_rovidites.py` kívül esik az ellenőr Bash-körén. A `teszt_szotari_gerinc` 6 hibájának base-beli megléte sem igazolt. |
| DT-F105a (a) | OK (egyeztetett eltérés) | `dontesek/uj/f105-bdb-szorend.md:1` | Az olvasót a diff nem érinti. A szabály a javítótáblában és a `bdb_rovidites`-ben él. |
| ⛔ minta: két vak kitöltő | OK (egyeztetett eltérés) | `naplok/F105_vak_kitolto_{1,2}.tsv` | Kézi összevetés mind az 50 soron: 50/50, a két kitöltő között 0 eltérés. A Wilson-alsó korlát n/(n+z²): 0,929 és 0,927. |
| ⛔ betartása: bevezetés a jóváhagyás után | OK, megjegyzéssel | – | Az F105.7–9 commitok (tábla és megjelenítés) a vak eredmény commitja (F105.10) előtt készültek. Mind az ágon maradtak: merge és lapgenerálás nem volt. |
| ⛔ hatókör: a maqqéf-szabály | **ELTÉRÉS** | `eszkozok/bdb_rovidites.py:197-262` | A vak minta mindkét alakból kiszedte a maqqéfet, ezért a rafe-maqqéf szabály kézi minta nélkül került a megjelenítésbe. A felső becslés 113 hibás eset 2 668 eldönthetőből. Ismert hibás kimenet: `אֶתֿכֹּל` → `אֶ־תכֹּל` (`F105_naplo.md:174`). |
| Javítótábla: a meglévő `javitva` sorok | OK | `adat/bdb_forras_javitas.tsv` | Törölt sorok: 2 fejléc, 1 778 `jelolt_marad`, 2 `valodi_sorrend`, **0 `javitva`**. Új sorok: 2 fejléc, 1 846 `javitva` (próbával), 2 `javitva/manual`. A törölt kulcsok mind visszajönnek, a 68 új kulcs egyedi. |
| Javítótábla: `--ellenoriz` | NEM ELLENŐRIZHETŐ | – | Kívül esik az ellenőr Bash-körén. |
| Javítótábla: kód-hash | **ELTÉRÉS** | `eszkozok/bdb_jelolt/forras_javit.py:69-75` | A `kod_hash()` csak a `forras_javit.py`-t és a `heber_sorrend.py`-t fedi. Az új próba viszont a `bdb_szelet.lapit`-ot is használja, ezért ha a `bdb_szelet.py` változik, a tábla változhat úgy, hogy a fejléc nem jelzi. |
| A hivatkozott-vers-próba logikája | OK | `eszkozok/bdb_jelolt/heber_sorrend.py:192-301` | A DT445 `minta` változatlan. A `helyes` ítélet csak akkor születik, ha a vers a jelöltet illeszti, a forrásalakot pedig nem. Az átfedés ártalmatlan, mert a csere pozíció szerint, egy menetben fut (`bdb_rovidites.py:271-287`). |
| A két kézi sor (ütközés) | OK | `forras_javit.py:181-188`, `naplok/F105_utkozes.tsv` | `lekerdez.py scan` a Péld 17:18-on és a 3Móz 16:4-en → n=1 (`scope=range:… \| forras=TAHOT_kivonat.tsv \| ts=2026-11-10T12:41Z`). |
| A rafe-maqqéf szabály (kód) | OK | `bdb_rovidites.py:219-262` | Kézi nyomkövetés: a kimenet egyezik a tesztek elvárásával. A szabály idempotens. |
| `bdb_vers_jelentes.tsv` hash (kör) | OK (szerkezet) | `adat/bdb_vers_jelentes.tsv:2`, `forras_javit.py:57-66` | Egyetlen fejlécsor változott. A kör megtört, van fixpont. A hash-értékek kiszámítása NEM ELLENŐRIZHETŐ. |
| SEMA 2.31 | OK | `adat/SEMA.md:1387, 1398, 1400, 1403` | Grep-számlálás a táblán: 43 572 / 36 320 / 16 824 / 222 / 19 274. Egyezik a SEMA-val. |
| `lexikon/` érintetlen, `KETRETEGU_BDB_KARTYA` | OK | `eszkozok/lexikon_general.py:3302` | A `lexikon/` diffje 0, a kapcsoló értéke `frozenset()`. |
| Lexikon-nézetek a CI szerint (E28) | **ELTÉRÉS** | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:743` és még 4 | `futtat.py` E28: 5 HIBA, a commitolt nézet eltér az újragenerálttól. Az ISTENTISZT-001 eltérése bizonyosan az F105-ből jön (H7121). A másik 4 (pl. ALVIL-001:1043, TEREMT-002:358) oka nem látszik. A DT-F105a „most nem generálódnak újra” mondata ezt a piros kaput nem kezeli. |
| Helyőrző string-literálban (E32) | **ELTÉRÉS** | `eszkozok/bdb_jelolt/forras_javit.py:217` | A `DT-F105a` a `prov_vers` literálban áll, és ugyanez a szöveg áll az 1 846 táblasor `proveniencia` mezőjében is. A `szamkiosztas` ezt nem cseréli, ezért merge után a tábla, a generátor és a `--ellenoriz` szétcsúszhat. |
| A napló belső ellentmondásai | **ELTÉRÉS** | `naplok/F105_naplo.md:3-4, 136-137, 97, 103` | A fejléc szerint „az adat, a megjelenítés … nem változott”, pedig a 6. szakasz szerint változott. A 136–137. sor szerint a jóváhagyás nyitott, a 7. szakasz szerint teljesült. Az 5. táblában a 17. sor (Hós 14:8) Macula-oszlopa üres, a 23. sor (Ézs 3:3) az MT 3:3-at adja a Károli 3:3 helyett. A vak mintában (`F105_vak_minta.md:186`) a vers helyes. |
| A brief `ir` mezője | **ELTÉRÉS** | `F105_BDB_SZOREND_BRIEF.md:14` | Hiányzik belőle: `naplok/F105_vak_minta.md`, `F105_vak_kulcs.tsv`, `F105_vak_kitolto_{1,2}.tsv`, `F105_vak_osszevet.py`, `nyitott/uj/f105-bdb-szorend.md`. |
| Commit-üzenetek (E30) | **ELTÉRÉS** (enyhe) | `d724e487`, `97410ec1` | „versen” helyesen „versén”. A `javitva` jelzés téves riasztás (állapot-azonosító). |
| Vak eljárás: árulkodó jel | OK, egy kivétellel | `naplok/F105_vak_minta.md:35` | Strong, állapot és geres nincs a fájlban. Az egyetlen jel: a 4. tétel A-alakjában maqqéf áll. Ezt a napló jelzi, és a 4. tétel nélküli számot is közli. |
| Vak eljárás: a kulcs elérhetősége | NEM ELLENŐRIZHETŐ | `naplok/F105_naplo.md:79-130` | A helyreállított alak a kitöltés alatt a repóban állt (az 5. tábla, `0ad712f3`). A kitöltők utasítása megtiltotta a megnyitását, és mindkét kitöltő indoka versalapú. |
| Vak eljárás: hatókör | OK, megjegyzéssel | – | 49 tétel `javitva` sorként áll a táblában. A 25. tétel (H4725, 3Móz 10:17) nem: a H4725-nek 0 sora van. A minta a mérés 1 823 jelöltjét fedi, nem a bevezetett 1 848 sort. |
| N-F105a valóban nyitott (A2) | OK | `nyitott/uj/f105-bdb-szorend.md:1` | A csere alak szerint történik (`bdb_rovidites.py:276-284`). |
| A1 | OK | – | Minden számállítás mellett szkript és proveniencia áll. |
| A3, A4, A5 | nem alkalmazható | – | – |
| A6 / E12–E15 | OK | – | `futtat.py`: 0 találat. |
| CI | NEM ELLENŐRIZHETŐ (részben) | – | Saját `futtat.py --valtozott …` futás: HIBA E28 5, E32 1. Figyelmeztetés: E25 3, E27 43, E30 5, E34 41, E36 1. Az E25/E27/E34/E36 a diffen kívülre mutat. |

**ELTÉRÉS-ek, súlyossági sorrendben:**
1. E32 HIBA: a `DT-F105a` helyőrző a `forras_javit.py:217` literáljában és az 1 846 táblasor provenienciájában.
2. E28 HIBA: 5 lexikon-nézet eltér az újragenerálttól, ebből legalább egy bizonyosan az F105 miatt.
3. A rafe-maqqéf szabály ⛔ kézi minta nélkül került a megjelenítésbe, és van ismert hibás kimenete.
4. A `kod_hash` nem fedi a `bdb_szelet.py`-t.
5. A napló belső ellentmondásai (a fejléc, a 6. szakasz eleje, az 5. tábla 17. és 23. sora).
6. A brief `ir` mezője hiányos.
7. E30: ékezetlen szó a commit-üzenetekben.

**A javítókörben futtatandó:**
- `python eszkozok/teszt_futtat.py --gyors`
- `python eszkozok/teszt_bdb_rovidites.py`
- `python eszkozok/bdb_jelolt/forras_javit.py --ellenoriz`
- `python naplok/F105_vak_osszevet.py`
- a base-en: `teszt_szotari_gerinc`
