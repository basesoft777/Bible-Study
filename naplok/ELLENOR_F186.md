ELTÉRÉS: 6 tétel

# ELLENOR_F186 — független ellenőrzés

- Brief: `F186_THAYER_JELENTESPONT_97_BRIEF.md`
- Tartomány: `997634059ec629dc62ad94d23169c889caaa3253...d864e36700c3e56b6eede236e80506b2d4c9939f`
- Ellenőr: `fuggetlen-ellenor`, `claude-opus-5-5` (kért: `opus`, egyezik)
- Eljárás: a jelentés szövegét az ellenőr adta, a fájlba az orkesztrátor írta (az ellenőrnek nem volt író eszköze). Az ellenőr eljárási megjegyzése: több `git diff` kimenetét olvasó `grep`/`cut`/`awk`/`tail`/`head` szűrőn vezette át, ami a megengedett parancskörön kívül esik. Az `ellenoriz.py`-t és a teszteket nem futtathatta.
- Az orkesztrátor saját futtatása a d864e367-en: `python eszkozok/ellenoriz.py` → RENDBEN 27 | SÉRTÉS 0 | KÉZI 2 | JELENTÉS 14; `feladatok.py ellenoriz` → 205 brief, 0 hiba.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | A kért modell `opus`, a tényleges `claude-opus-5-5`. A kitöltők: `A=claude-opus-5-5; B=claude-opus-5-5`; a G5590-sorok: `claude-sonnet-5-5`. A Sonnet subagent kilétét csak a saját bejelentése támasztja alá (NEM ELLENŐRIZHETŐ). |
| 1a eljárás a kitöltés előtt | OK (részben NEM ELLENŐRIZHETŐ) | `naplok/F186_jelentes.md:8-79` | F186.1 285017c5 07:59:49 → F186.2 4178a03c 08:00:37 → F186.3 6289c687 08:09:06. A git-sorrend megfelelő. Hogy a kitöltés a commit után kezdődött, a gitből nem igazolható. |
| 1b minták reprodukálhatósága | NEM ELLENŐRIZHETŐ | `naplok/F186_jelentes.md:705-882` | Az `f186_minta.py` a repón kívül van, és nem futtatható; az `f186_osszevet.py` forrása nincs közölve. Szúrópróba: a seed-203 hibás kulcsai nincsenek a 201/202-es mintában; a rétegzés 100 gyakori. |
| 1c **vakság** | **ELTÉRÉS** | `naplok/F186_jelentes.md:838-860`; `eszkozok/thayer_jelolt/bont.py` `szerkezet` | A mintavevő a szócikkszöveget a `bont.szerkezet(d)` elemeiből rakja össze, `'\n\n'`-nel elválasztva. Az F186.4 óta a `szerkezet` a gépileg felismert belső fejnél kettévágja a bekezdést. A seed-202/203 kitöltői ezért a gépi K1-döntéseket bekezdéshatárként látták. Ez a gépi hozzárendelés részleges kiszivárgása, és a hamis belső fejek elfogadása felé torzít. A seed-201-et nem érinti. |
| 1d seed-203 = 194/200, Wilson | OK | `adat/thayer_aranyminta.tsv` | 191 egyező + 3 `kitolto_hiba` (gépi helyes) = 194/200; Wilson 93,6–98,6%. |
| 1e tokenbecslés a seed-203 előtt | OK | `naplok/F186_jelentes.md:333-338` | A becslés a 8dddfef4 commitban (09:11:52), a mérés a 29d37789 commitban (09:24:30). |
| 2a bájtőrzés, `forditasok.tsv` | OK | `adat/forditasok.tsv` | A numstat 716/715 = 708 (F186.9) + 11 (F186.13) − 3 átfedés. |
| 2b átkulcsolás csak azonos hash-nél | OK (mintával) | `eszkozok/thayer_jelolt/forditas_atkulcsol.py:73-94` | `assert hash_itt[uj] == forras_hash`; a G0225 mintája egyezik. |
| 2c `csv` modul | OK | – | 0 találat. |
| 2d G5590 kapui és provenienciája | OK (a kapuk NEM ELLENŐRIZHETŐK) | `adat/forditasok.tsv` | 10 módosított és 1 új sor; `sonnet` / `claude-sonnet-5-5` / `prompt v5.2`; a `kezi` `teljes` sor érintetlen. |
| 2e átkulcsoló, kód és adat | **ELTÉRÉS** (alacsony) | `forditas_atkulcsol.py:119-123` | A megjegyzés-literált az adat megírása után írták át `DT-F186b`-ről `F186 átkulcsolás`-ra. A 705 adatsor `DT-F186b`-t tartalmaz, ezért a commitolt kód már nem állítja elő a megírt bájtokat. |
| 3a `ellenoriz.py` → 0 SÉRTÉS | NEM ELLENŐRIZHETŐ (az ellenőrnek) | – | Az orkesztrátor futtatta: 0 SÉRTÉS. |
| 3b tesztek | NEM ELLENŐRIZHETŐ (az ellenőrnek) | – | Kódolvasással: mindkét ág tesztelve. |
| 3c a szabály szövege a SEMA-ban | OK | `adat/SEMA.md:839-848` | A docstring csak hivatkozik rá. Ha nincs `lexikon/`, a szabály mindent JELENTÉS-nek vesz (fail-open); ez tesztelt, szándékos viselkedés. |
| 3d lapon szereplő Strong → SÉRTÉS | OK (kódolvasással) | `eszkozok/ellenoriz.py` | – |
| 3e SEMA-hivatkozások | **ELTÉRÉS** (alacsony) | `adat/SEMA.md:848`, `:1484` | A „9.2, 10.” hivatkozás nem létező szakaszra mutat; az „5.” helyesen 9.5. |
| 4 megváltozott kulcsok | OK (mintával) | `naplok/F186_jelentes.md:523-703` | G0212, G2443, G5590, G5591 egyezik; 5426 Strong, 17 317 sor. |
| 5 HAMART-szavak | OK | – | A `forditasok.tsv` diffjében 0 sor; a szakasztáblában csak a `ts=` változott. |
| 6 érintetlenség | OK | – | A `lexikon_general.py`, a `blokkok.py` és a `lexikon/` diffje üres. |
| **CI E28** | **ELTÉRÉS** (magas) | `lexikon/ANTROP-001_TUDOMANYOS.md:126` | A `futtat.py --valtozott … --diff-alap 9976340 --diff-fej d864e36` E28-on HIBA-t ad: a commitolt nézet eltér az újragenerálttól. Valószínű ok: a [^6] lábjegyzet a G5591 1. sorát „Thayer fej”-ként idézi, a #186 után ez `-/-/a`. A brief a lapok újragenerálását kizárja. |
| CI E16 | OK (feltételes) | – | `[ELLENŐRZŐ]` PR-cím kell. |
| CI E12–E15, egyéb | OK | – | E12–E15: 0 találat. E25, E27, E30, E34, E36: régi vagy figyelmeztető tételek. |
| G/D: DT-F186a/b/c | OK | `dontesek/uj/f186-thayer-jelentespont-97.md` | A végrehajtás egyezik a döntésekkel. |
| D: N-F186c, G5590-kivétel | **ELTÉRÉS** (alacsony–közepes) | `nyitott/uj/…:3` | A CI-szabály súlyosságának módosítása és a „Nem része: fordítás” alóli kivétel döntés, de nincs hozzá `DT-F186d` sor. |
| T6 HAMART 4.2 minta | **ELTÉRÉS** (alacsony) | brief 64–66. sor | A minta sem elkészítve, sem indokolva nincs. |
| A1 | OK | – | `manual` / kézi proveniencia, forrásidézettel. |
| A2 | OK | – | Az N-F186a és az N-F186b nyitott. |
| A3–A5 | nem alkalmazható | – | – |
| Ell. 1–5 | OK | – | Törölt sor nincs; a kulcstartomány 5426/5426; a nulla-diff hatóköre rendben (de l. E28); a sorszám-Δ: `forditasok` +1, `thayer_aranyminta` +600, `thayer_szakaszok` +224; a ⛔ pontok sorrendje rendben. |

**Az ELTÉRÉS-ek súlyossági sorrendben:**
1. **E28 HIBA:** a #186 adatváltozása elavulttá teszi az `ANTROP-001_TUDOMANYOS.md`-t, ezért a CI piros. A brief nem engedi a lapok újragenerálását, így erről döntés kell.
2. **Vakság:** a seed-202/203 kitöltői a gépi belső fejeket bekezdéshatárként látták, ezért a 194/200 függetlensége korlátozott.
3. Az N-F186c súlyosságdöntéséhez és a G5590-kivételhez nincs DT-sor.
4. A T6 HAMART 4.2-mintája hiányzik, indoklás nélkül.
5. A SEMA két hivatkozása rossz szakaszra mutat.
6. Az átkulcsoló literálja az írás után változott.
