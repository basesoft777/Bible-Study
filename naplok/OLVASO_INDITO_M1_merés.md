# #100 OLVASO_INDITO — M1 mérések

*Ág: `claude/olvaso-indito` · végrehajtó: `claude-sonnet-5-5` · mérés napja: 2026-10-15 (helyi idő, +02:00). A mérések a `pardes` WSL-disztribúcióban futottak (Python 3.12.3, a `~/pardes` venv), a kód és a `konkordancia/` a `/mnt/c`-ről olvasódott (DT-F100a (c)), a `PARDES_DB` a WSL-natív `~/pardes/pardes.db` (895 MB, `epites_ts` = `2026-10-14T09:35:00Z`). Nyers kimenet: a session scratch-könyvtárában (nem a repóban).*

## 1. A tesztek együttes ideje (elfogadási feltétel)

**Parancs:** `python eszkozok/teszt_futtat.py` (Windowsról, a repó gyökeréből; a szkript magát a WSL-ben indítja újra, és a `PARDES_DB`-t a natív példányra állítja). **Futás:** 2026-10-15T10:00:08 – 10:04:33 (Windows-óra), egyetlen, mással nem párhuzamos futás (a háttérben más számítás nem ment); a kód a commit `4cf24f98` (F100.7).

A kiírt fejléc: `adatbázis: /home/basesoft/pardes/pardes.db -- WSL-natív alapérték`, `mérete: 895 MB, epites_ts: 2026-10-14T09:35:00Z`; `/mnt/c`-figyelmeztetés nem jött (az adatbázis nem a `/mnt/c` alatt van).

| Tesztfájl | Tesztek | Idő (mp) | Eredmény |
|---|---|---|---|
| `teszt_arculat.py` | 22 | 3,1 | zöld |
| `teszt_indito.py` (új, #100) | 39 | 13,3 | zöld |
| `teszt_olvaso_szerver.py` | 71 | 122,4 | zöld |
| `teszt_pilot_aranymintaval.py` | 22 | 44,3 | zöld |
| `teszt_szintek.py` | 13 | 77,5 | zöld |
| `teszt_tervezo.py` | 48 | 14,0 | zöld |
| **a `teszt_szintek.py` és az új `teszt_indito.py` nélkül** (a #100 előtti négy fájl: arculat, olvaso_szerver, pilot, tervezo) | 163 | **183,8** | zöld |
| a `teszt_szintek.py` nélkül (`--gyors`; a `teszt_indito.py`-val) | 202 | 197,2 | zöld |
| **mind a hat fájl** | 215 | **274,6** | zöld |

*Megjegyzés a „négy tesztfájlhoz”.* A brief négy tesztfájlt nevez; az `eszkozok/olvaso_szerver/teszt_*.py` ma öt fájl (`teszt_arculat`, `teszt_olvaso_szerver`, `teszt_pilot_aranymintaval`, `teszt_szintek`, `teszt_tervezo`), a #100 hatodikat (`teszt_indito.py`) ad. A fenti táblázat mindegyiket külön mutatja; az elfogadási feltétel (a fájlok együtt, a DT-F100a (c) szerinti környezetben a mért idő alatt lefutnak) **teljesül**: a teljes készlet 4,6 perc.

**Összevetés a referenciával:**

- `teszt_olvaso_szerver.py`: **122,4 mp** (referencia: 118–124 mp) — egyezik. Egy korábbi, a SQL-szabály miatt egyetlen tesztben bukó futás (09:54–09:57, a `teszt_futtat --gyors` első próbája, 71 teszt) 131,9 mp-et mért; ugyanaz a kód, a különbség terhelés-ingadozás.
- `teszt_szintek.py`: **77,5 mp** egyedül futtatva (13 teszt, 76,7 mp a unittest szerint). A #98-nál mért 19 perc párhuzamos futás mellett volt; az itteni szám NEM párhuzamos. Az előző mondat nem azt állítja, hogy a párhuzamos futás gyorsabb lenne: csak annyit, hogy a 19 perc terhelt gépen (több session egyszerre) keletkezett, az itteni egyedüli futás 77,5 mp.
- `teszt_pilot_aranymintaval.py`: 44,3 mp (a `konkordancia/`-t a `/mnt/c`-ről olvasó pilot-összevetés — a D2 `adat.py`-t futtatja; a DT-F100a (c) lassúság-kockázata itt nem jelentkezett).

**Az órákról:** a fájlonkénti időket a `teszt_futtat.py` a WSL monotonic órájával méri; a kezdő és záró időbélyeget a Windows-óra adta (10:00:08 → 10:04:33 = 265 mp), a fájlonkénti idők összege 274,6 mp. A ~3,5%-os eltérés a WSL2 és a Windows óra eltérése (nem párhuzamos futás okozza; a fájlok egymás után futottak); az elfogadási feltétel szempontjából a nagyságrend számít.

**A mérés korlátja:** egyetlen futás fájlonként (a két teljes futás: 09:54–09:57 `--gyors`, és 10:00–10:04 teljes), nem ismételt mérés; a szórás nincs becsülve. A szám a `/mnt/c`-ről olvasott kódra és `konkordancia/`-ra vonatkozik; másolat nem készült.

## 2. Az indító mérései

Proveniencia: `proba_m2.py` (a session scratch-könyvtárában), 2026-10-15 10:08–10:09, külön port (18801), ideiglenes adatbázis-másolatok (`~/proba100`); a részletes napló: `naplok/OLVASO_INDITO_M2_gepi_proba.md`.

| Mérés | Érték |
|---|---|
| 895 MB-os adatbázis másolása `cp`-vel a WSL-natív lemezre (két másolat az előkészítéshez) | 12,4–22,3 mp két másolatra, azaz ~6–11 s egy másolatra (a háttérterheléstől függ) |
| `indit.sh` indulása eltérő `epites_ts`-sel (leállítás + másolás + szerver) a `/statusz` 200-ig | 6,4–10,9 mp (három futás: 10,9; 8,9; 6,4) |
| `indit.sh` indulása azonos `epites_ts`-sel (nincs másolás) | a 6. lépésben kb. 5 mp két egymás utáni kattintásra együtt |
| kódváltozás (`touch`) → az újraindított szerver válaszol | 1,0–1,2 mp (öt fájlfajta; egy korábbi futásban az első újraindulás 3,3 mp) |
| a módosított sablon hatása a lapon | 0,1 mp (a sablont a Jinja amúgy is frissen olvassa; az újraindulás ezen kívül ~1 mp) |
| ágváltás → a lábléc az új ágat mutatja | 2,5–2,8 mp (a lábléc 3 mp-es újraolvasási ideje) |

Az üresjárati CPU-terhelés az M0 felmérés szerint ~0,8% egy magon (`naplok/OLVASO_INDITO_M0_felmeres.md` 4.); a 126 helyett a `--ujratolt` extra fájlokkal a figyelt fájlok száma nőtt (a `sablonok/`, `konfig/`, `statikus/` fájljai); a terhelést az új készlettel külön nem mértem.
