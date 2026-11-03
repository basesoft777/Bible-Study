# F161 GLOSSZA_LANC — menetnapló

*Modell: claude-opus-5-5 (a brief `modell` mezője: opus). Ág: `claude/glossza-lanc-1a9f9f`. 2026-11-03.*

## 1. A #121 feloldója

A `glossza_lexikon_forditas.py lista` a nem UBS szótárakra nem hívta a 13. szabály feloldóját (`tovabbi_forras`), ezért
az ANTROP-001 21 TBESG-egysége `nincs_forras` volt. Új közös `forras_szoveg(sor)`; a `lista` ezt hívja.

*proveniencia: scope=`glossza_lexikon_forditas.py lista --id ANTROP-001` a #608 ágának állapotán (c332f160, repón kívüli
munkafa), a javítás előtt és után | forras=konkordancia/TBESG.txt, UBS_DNTG_jelentesek.tsv, UBS_DBH_jelentesek.tsv,
adat/forditasok.tsv | ts=2026-11-03*

| `szotar` | előtte | utána |
|---|---|---|
| UBS_DNTG | 30 hianyzik | 30 hianyzik |
| UBS_DBH | 3 hianyzik | 3 hianyzik |
| TBESG | 21 nincs_forras | **21 hianyzik** |
| Thayer | 6 nincs_forras | 6 nincs_forras (szakaszsor; a Thayer-lánc dolga) |
| BDB | 1 nincs_forras | 1 nincs_forras (szakaszsor; a BDB-lánc dolga) |

A main-en (az ANTROP-001 régi lapja) ugyanígy feloldódik a TBESH 6, a tW 11, az MCGED 2 és a BDB nyelvi háttér 2
egysége is (N-F161b); ezeket a lánc nem veszi fel.

## 2. `szaraz` az ANTROP-001 54 egységén

*proveniencia: scope=`glossza_api_koteg.py szaraz --lista <a fenti lista> --munka <jegyzetmappa>/glossza_antrop`, a #608
állapotán | forras=a fenti lista, adat/terminologia.tsv (v5), adat/karoli_strong/, adat/forditasok.tsv | ts=2026-11-03*

- 54 egység (UBS DNTG 30, UBS DBH 3, TBESG 21), 3 kérés (20 + 20 + 14 egység; azonos Strong egy kérésben).
- Forrás 1 213 karakter; a három prompt 30 630 karakter.
- Becslés (manual, mérés nélkül): bemenet ~13 100 token, kimenet ~18 900 token; ~0,11 USD Batch-áron, cache nélkül.
- A kérések a session jegyzetmappájában (`glossza_antrop/keresek.jsonl`), repón kívül; a `bekuld` nem futott.

## 3. Próba: 5 glossza előfizetői subagenttel

Egy külön munkakönyvtár, az 54-ből 5 jellemző egység (glosszaelem-lánc, zárójeles pontosítás, igei glossza
`one's`-szal, héber, TBESG névelővel), egy kérés (`G001-p1`, 6 408 karakter). A `general-purpose` subagent
(`claude-sonnet-5-5`, saját bevallása szerint) a `prompt` paranccsal kiírt user-szöveget kapta szó szerint, és a JSON-t
fájlba írta; a válasz a `bevesz`-szel került be, utána `kapuz` és `rogzit` (a munkakönyvtárba). **A `beir` nem futott.**

*proveniencia: scope=`glossza_api_koteg.py bevesz / kapuz / rogzit --munka <jegyzetmappa>/glossza_proba5` | forras=a
subagent válasza (`G001-p1_valasz.json`), a kapuk: forditas_kapuk.kapuk_futtat + G1–G4 | ts=2026-11-03*

**Kapueredmény: 5/5 átment, javító kör nem kellett, mankó-jelzés 0.** A 6. hosszarány-kapu háromszor JELZÉS (nem gátol;
a rövid glosszán nem értelmezhető).

| # | szótár, kulcs | forrás (angol) | fordítás | mankó (szójegyzék · Károli) |
|---|---|---|---|---|
| e001 | UBS DNTG G4151 12.37 | demon; evil spirit | démon; gonosz szellem | egyezik · egyezik (szel) |
| e002 | UBS DNTG G4152 12.21 | spiritual; from the Spirit (in reference to such matters as gifts, benefits, teachings, blessings, and religious songs) | szellemi; a Szellemtől származó (olyan dolgokra vonatkozóan, mint az ajándékok, jótétemények, tanítások, áldások és vallásos énekek) | egyezik · egyezik (aján) |
| e003 | UBS DNTG G5590 25.280 | to experience anguish; to be tormented in one’s heart | gyötrelmet átélni; szívében gyötrődni | nincs adat · egyezik (szív) |
| e004 | UBS DBH H5315 004880001004000 | living creature; living soul | élőlény; élő lélek | nincs adat · egyezik (léle) |
| e005 | TBESG G0444 rövid | a human | ember | nincs adat · egyezik (embe) |

A rögzített sor mintája (`rogzitett.tsv`, a `forditasok.tsv` sémája): `allapot` = sonnet, `modell` = claude-sonnet-5-5,
`megjegyzes` = „F161 (glossza-lánc, prompt glossza v1, G001-p1, subagent): kapuk átmentek; terminológia v5 |
scope=UBS_DNTG G4151 004054001003000 12.37 glosszak_hu | forras=konkordancia/UBS_DNTG_jelentesek.tsv | ts=2026-11-03”.

## 4. Tesztek

`python eszkozok/teszt_glossza_api_koteg.py`: 18 teszt, OK (a `szaraz` kétszer bájtra azonos, a `bekuld` a fájl kéréseit
küldi, plafon nélkül és eltérő kérésnél megáll; a kapuk: angol maradék, funkciószó, helyőrző, elemszám, belső jel,
egyenes idézőjel, terminológia; a teljes út bevesz → kapuz → javit → rogzit → beir egy másolaton: a meglévő sorok bájtra
változatlanok, `kezi` védett, hash-eltérésnél megáll). `python eszkozok/teszt_glossza_lexikon_forditas.py`: 16 teszt, OK.

## 5. Az 54 fordításának menete (az ANTROP-001 sessionjének, e PR merge-e után, a #608 ágán)

```
python eszkozok/glossza_lexikon_forditas.py lista --id ANTROP-001 --kimenet <repón kívül>/render
python eszkozok/glossza_api_koteg.py szaraz --lista naplok/F121_GLOSSZA_FORDITAS_lista.tsv --munka <repón kívül>/glossza
python eszkozok/glossza_api_koteg.py prompt --munka <…> --cid G001-p1 --ki <…>/G001-p1_prompt.txt   # G002, G003 ugyanígy
#   subagent (Sonnet): a prompt-fájl szó szerint → JSON-válasz fájlba
python eszkozok/glossza_api_koteg.py bevesz --munka <…> --cid G001-p1 --valasz <…>/G001-p1_valasz.json --modell <tényleges modellnév>
python eszkozok/glossza_api_koteg.py kapuz --munka <…>
python eszkozok/glossza_api_koteg.py javit --munka <…>      # ha van bukott; a p2 kérések ugyanígy: prompt → subagent → bevesz → kapuz
python eszkozok/glossza_api_koteg.py rogzit --munka <…>
python eszkozok/glossza_api_koteg.py beir --munka <…> [--jelzes-atnezve]
```

API-úton a `prompt`/`bevesz` helyett `bekuld --plafon <USD>` → `allapot` → `begyujt` (a plafon a felhasználóé).
