# B4 — a helyben frissítő és a nulláról generáló út egyezése (lexikonlap)

*2026-11-03 · modell: claude-opus-5-5 · ág: `claude/b4-general-egyezes` · alap: `410e59fa` (a #611 merge-e)*

## 1. A kiinduló folt

A `lexikon/TEREMT-002_TUDOMANYOS.md`-ből két üres sort kétszer is kézzel töröltek (`4c792511`, 1A.11; `c07c2517`, SABLON.6). A helyben futtatott `python eszkozok/general.py --cel lexikon --id TEREMT-002 --ir` két üres sort tett a `res_labjegyzet` blokk elé, az E28 újragenerálása (`--kimenet`, üres könyvtárba) nem (`naplok/1A_PROZA_jelentes.md` 7. szakasz). A generált lapot kézzel szerkeszteni tilos; a hibát a generátorban kell javítani.

## 2. Mérés (javítás előtt)

Eszköz: `eszkozok/lexikon_ket_ut_meres.py`. Lapként négy generálás, mind a repón kívüli ideiglenes könyvtárba, `PARDES_DATUM` = a commitolt lap első `ts=` dátuma. A helyben frissítő út bemenete: (a) a nulláról generált lap, (b) a commitolt (LF-es) blob, (c) a blob CRLF-es példánya. A (c) a `core.autocrlf=true` munkapéldány esete, ezt látja a `--ir`.

| Lap | helyben(a) | helyben(b) | helyben(c) | helyben(c), LF-re normalizálva |
|---|---|---|---|---|
| ALVIL-001, ANTROP-001, HAMART-001, HODIT-001, ISTENTISZT-001, KIRALY-001, MENNY-001, TEREMT-001 | egyezik | egyezik | **eltér** (a 3. sortól CR marad a sorvégen) | egyezik |
| TEREMT-002 | egyezik | egyezik | **eltér** | **eltér: 891. sor, +2 üres sor a `res_labjegyzet` előtt** (1011 → 1013 sor) |

Tehát a két út LF-es bemeneten mind a 9 lapon bájtra egyezik. Az eltérés oka a **munkapéldány CRLF-je**:

- A `lexikon_general.run()` a meglévő lapot `newline=''`-vel, normalizálás nélkül olvasta be.
- A `res_labjegyzetek_alkalmaz` a régi blokkot kivágva `'\n\n'`-t keres a záró jelölő után. CRLF-nél ott `'\r\n\r\n'` áll, ezért a két üres sor bent maradt, és az új blokk elé került. Az eltérés csak ott jön elő, ahol a lapon `res_labjegyzet` blokk van; ma ez egyedül a TEREMT-002.
- A kimenetet a generátor `newline='\n'`-nel írta. A megmaradt CR-ek így vegyes sorvéget adtak, amelyet a git commitkor LF-re simított. A tartalmi különbség, a két üres sor, viszont commitba került.

A `_generalt_fejlec_alkalmaz` korábbi CRLF-kezelése (F11 M4, DT-F11h Á7) ugyanennek a hibának egy másik tünetét foltozta, csak a fejlécnél.

## 3. Javítás (generátor)

`eszkozok/lexikon_general.py` `run()`: a meglévő lapot a `general.eles_fajl_beolvas` olvassa be, LF-re normalizálva. A `general.py` többi helyben író célja is ugyanígy olvas. A kimenet LF-es marad, ahogy eddig.

Mérés a javítás után: mind a 9 lapon mind a négy összevetés egyezik (36/36). A nulláról generáló út nem változott, ezért **egyetlen commitolt lap sem változik**, laptartalom nincs a diffben.

## 4. Kapu

Az **E28** (`eszkozok/ellenorzes/szabalyok.py`, `_e28_helyben_ag`) a migrált nézeteken (`e28_migralt_nezetek.tsv`: ISTENTISZT-001, ALVIL-001, TEREMT-002) mostantól a helyben frissítő utat is lefuttatja: bemenete a commitolt blob CRLF-es példánya, és bájtra a nulláról generálthoz méri. Eltérésnél HIBA, a javítási útmutatás: „a generátorban …, nem a lapon”. Ára migrált nézetenként egy további generálás.

Tesztek (`eszkozok/ellenorzes/tesztek/test_szabalyok.py`, `E28Teszt`):

- pozitív: a helyben ág CRLF-es bemenetet kap, egyező kimenetnél zöld;
- negatív: két plusz üres sor (a TEREMT-002 esete) piros;
- negatív: CRLF-es kimenet piros.

A nem migrált 6 lapon a kétféle út egyezését a kapu nem őrzi. Ezeken a `python eszkozok/lexikon_ket_ut_meres.py` méri; a kilépési kód 1, ha a két út eltér.
