# ELLENOR_F22_Neh — F22_KAROLI_STRONG_BRIEF.md (D31, v2.25), `ae6ee24d..9fc32dd3`

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-neh`; commitok: `41f6581e`, `c7e4ab8d`, `c7998b75` (a main beolvasztása), `9fc32dd3`.*

ELTÉRÉS: 3 tétel

## Igazolt (saját lekérdezéssel)

- **406/406 vers:** a `Karoli_1908.tsv` `^Neh ` sorai 406; a `minta_Neh.tsv` 406 + fejléc; a k41 `igehely_db`-je 6.
- **parok_Neh 8 027:** 8 029 sor = 1 proveniencia + 1 fejléc + 8 027 `alacsony / S`; a fejezettábla összege 8 027.
- **szavak_Neh 16 169:** hu 7 725 (6 326 `parositva`, 1 399 `betoldas`), er 8 444 (7 491 `parositva`, 953 `forditatlan`); er = a `TAHOT_kivonat.tsv` `^Neh ` sorai (8 444); `fuggoben`/`kezi` 0.
- **Kapuhiba 36/406 → 0:** 1. kör k2 1, k4 1, k6 1, k10 9, k11 1, k12 1, k31 1, k32 10, k34 1, k35 10 = 36; a javító kör 10 sora mind 0; a `sonnet/Neh.jsonl`-ben 0 `kapuhiba`.
- **Költség:** 1. kör 2,167389, 2. kör 0,280320, összesen 2,447709 USD; tokenek 435 544 / 346 369 és 127 205 / 30 623; plafon 4,5066; versenként 0,00603. Kumulatív 59,629227 + 6,251993 + 2,447709 = 68,328929 USD.
- **A main beolvasztása:** a `batchek` (2), a `futasnaplo` (51) és a jóváhagyási napló (1) csak hozzáadás; a `tokenek.py` tuple-jében az `'1Kir'` megmaradt, mellé került a `'Neh'`; az 1Kir sorai érintetlenek. Adattáblából 0 adatsor törlődött.
- **K9:** `adat/SEMA.md` 2.20 és a `datasetek.tsv` 8 sora bővítve.
- **Szúrópróba (lekerdez.py scan):** H5166 és H2446 (Neh 1:1), H3588 (Neh 10:39): 3/3 egyezik a táblákkal.
- **Prompt-hash:** mind az 51 sor `84f12ca7aafb`. **Kulcs-grep:** 0 találat. **D15:** nincs párhuzamos futás. **D9:** a proveniencia `scope=manual … csak Sonnet`. **Jóváhagyás sorrendje:** a jóváhagyó commit (11:34:26Z) a batch (11:34:43Z) előtt van.
- **CI-eszköz (`eszkozok/ellenorzes/futtat.py`):** exit 0; E2–E16, E19, E20, E26: 0; E25: 3 és E27: 32, repószintű, nem e diffből; az E27 maradék 29 tétele a kimenetben csonkolt.

## ELTÉRÉS

1. **`f22/api_termeles/futasnaplo.tsv`, `futo_osszeg_usd`:** a Neh-sorok értéke (59,70 → 62,08) az 1Kir nélkül számolt, ezért az oszlop nem monoton, és az utolsó sor 62,0769, a valós összeg 68,3289. Egy keretőr 6,25 USD-vel alábecsülhet. Átírás csak a felhasználó jóváhagyásával (DT72); a jelentés 1. szakasza jelzi.
2. **`adat/datasetek.tsv` 89, 92, 95, 98:** a `Karoli_Strong_parok` sorok jelentéslistájából hiányzott a `naplok/F22_Neh_jelentes.md`.
3. **`F22_KAROLI_STRONG_BRIEF.md:12`, `kovetkezo`:** ellenőri jelentésre hivatkozott, amely az ellenőri kör előtt nem létezett.

## Nem ellenőrizhető a szerepkörből

`egyesit.py --ellenoriz` és a K7 újraépítés (a fő session futása: „rendben”), a BDB-mérés 479 / 96 értéke (a mérés kimenete nincs a repóban), a chatben adott jóváhagyás („mehet a Nehémiás”, 2026.10.11), a hu oldal tokenszáma a `tokenek.py` tokenizálásával.
