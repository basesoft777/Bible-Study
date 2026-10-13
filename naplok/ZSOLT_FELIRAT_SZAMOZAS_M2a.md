# ZSOLT_FELIRAT_SZAMOZAS_M2a.md — az A-oldali M2: a `Karoli_versmegfeleltetes.tsv` javítása (F91)

*Végrehajtó: claude-sonnet-5-5. Eszköz: `eszkozok/f91_versmegf_javit.py` (idempotens; `--ir` nélkül csak mér). Mért adat.*

Proveniencia: `scope=Zsolt 1–150 | forras=konkordancia/LXX_OS/psalms-lxx.tsv | ts=2026-10-13` · `scope=Zsolt 1–150 | forras=konkordancia/Karoli_1908.tsv + konkordancia/KJV_Strongs_teljes.tsv | ts=2026-10-13` · `scope=Zsolt 1–150 | forras=konkordancia/Karoli_versmegfeleltetes.tsv | ts=2026-10-13`

## 1. A1: a tábla javítása

Szabály (DT-F91a): a feliratos zsoltárokban az `igehely_kjv` az LXX_OS Károli-kulcsú etalon KJV-értéke (v > d); v ≤ d: üres, megjegyzés `felirat` (d = 1) vagy `felirat 2 vers` (Zsolt 51, 52, 54, 60). Az érintett zsoltárok: 62 (d > 0: 58 × d = 1, 4 × d = 2) + Zsolt 13 (kivétel, az etalon szerint) = **63**. A javított soroknál `forras = lxx_os_etalon_f91`; az `osztaly` és az `igehely_mt` változatlan. A fájl fejlécébe egy `# F91 javítás …` jegyzetsor került.

| | előtte | utána |
|---|---|---|
| eltérés az LXX_OS etalonnal (63 zsoltár) | 1 055 vers | **0** |
| ebből Zsolt 22 | 32 (mind a 32 Károli-vers: a felirat + 31 tartalmi vers) | **0** |
| módosult adatsor | | **1 055** (63 zsoltár) |
| nem komment sorok száma (az oszlopnév-sorral) | 22 932 | 22 932 (Δ = 0) |

- A módosult sorokból felirat-vers (üres KJV, `felirat` megjegyzés): 67 (59 × 1 + 4 × 2, benne Zsolt 13:1); a többi tartalmi vers `igehely_kjv`-je javult.
- Védőellenőrzés a szkriptben: minden nem érintett sor (a 63 zsoltáron kívül, és a fejléc) bájtra azonos az eredetivel; az oszlopszám minden sorban 6; a `git diff` kizárólag `Zsolt …` sorokat és a jegyzetsort mutatja.
- A d-szabály (`c:(v−d)`) mint ellenőrzés: **1 eltérés**, Zsolt 13:6, ahol az etalon `13:5;13:6` (a KJV a 13:5-öt két versre bontja), a d-szabály `13:5`. Ez a DT-F91a által rögzített kivétel; a mező az etalon pontosvesszős alakját viszi.
- Zsolt 13:1: az etalonban a KJV-értéke `13:1` (üres `karoli_ok`), de az etalon-d = 1, ezért felirat-versként üres KJV + `felirat` lett (mint a többi feliratos zsoltár első verse).
- **Figyelem:** a tábla fejléce szerint generált (`naplok/KAROLI_KK4_tabla_veglegesit.py`). A KK4-generátor újrafuttatása ezt a javítást visszavonná; a javítás az `eszkozok/f91_versmegf_javit.py` újrafuttatásával visszaállítható.

## 2. DT3 bontási napló

A DT3 küszöbe |Δ sorszám| ≥ 10 táblánként. Az A tábla sorainak száma nem változik (Δ = 0), tehát bontási napló nem kötelező; a módosult sorok száma fent áll (1 055 sor, 63 zsoltár).

## 3. N2: a Nave `karoli_allapot` / `igehely_karoli` oszlopa — **NEM újragenerálva, megállás**

A generátor az `eszkozok/nave_import.py` (a `nave_bontas.py` csak a vers-szintű bontás közös szabálya, az oszlopot nem állítja). Az oszlopok a `Karoli_versmegfeleltetes.tsv` `igehely_kjv` oszlopából jönnek (`beolvas_versmegf`). A hatást ideiglenes könyvtárba generálva mértem (a repó `Nave_basokant.tsv`-jéhez nem nyúltam): a régi és az új A tábla ugyanazzal a generátorral és forrással:

- módosuló sor: **2 039**, mind Zsolt, **63 fejezet**;
- 2 036 sor `azonos` → `eltero` (a `karoli_allapot` és az `igehely_karoli` változik) — megegyezik a DT-F91a becslésével (2 036);
- **3 sor `azonos` → `nincs_a_tablaban`** (a DT +3 sort `eltero`-nek várt a Zsolt 13-ban): oka, hogy a `beolvas_versmegf` a `13:5;13:6` értéket egy kulcsként indexeli, így a KJV 13:5 és 13:6 hivatkozás nem találja.

Miért állok meg a futtatás előtt (nem triviális):
1. A helyi `konkordancia/_nyers/nave/nave.txt` sha256-ja `9f028dbb…`, a repó `Nave_basokant.tsv` fejlécében rögzített `560dcb1a…`: a forrás nem azonos (valószínűleg sorvég/ekódolás-eltérés, nem vizsgáltam).
2. A generátor még a **régi** A táblával sem reprodukálja a repó Nave-fájlját: ~247 sor eltér az A-változástól függetlenül (pl. `JSir 3:33` vs `Sir 3:33`). Egy éles újragenerálás ezért az F91-en kívüli változásokat is behozna.
Javaslat az orkesztrátornak: (a) a `nave_import.py` `beolvas_versmegf`-jét a `;`-os értékre felkészíteni (a Zsolt 13:6 miatt), (b) a forrás-sha és a drift okát külön tételben tisztázni, és csak ezután újragenerálni; vagy (c) a Nave-sorokat csak a 2 036 + 3 sorra célzottan frissíteni (ez generátor-módosítás, tilos kézzel).

## 4. Tesztek

Az A táblát közvetlenül ellenőrző teszt a repóban nincs (az `eszkozok/ellenoriz.py` a SEMA 3. szakaszát és tanulmányfájlokat vizsgálja, a `konkordancia/Karoli_versmegfeleltetes.tsv`-t nem). A `eszkozok/teszt_sqlite_epit.py` a B-oldal (`sqlite_epit.py`, `lxx_versszam`) hatókörébe tartozik, nem futtattam. Futtatott ellenőrzés: a szkript beépített etalon-összevetése (UTÁNA: 0 eltérés, Zsolt 22: 0), az oszlopszám-ellenőrzés (0 hibás sor), az idempotencia (második futás: 0 módosuló sor).

## 5. Ami nem tartozik ide (B-oldal, érintetlen)

`LXX_versificacios_terkep.tsv` átnevezése/átkulcsolása, `sqlite_epit.py`, `teszt_sqlite_epit.py`, `f92_db_igazolas.py`, `macula_kk.py` hatásmérés. A fogyasztók közül a `Karoli_versmegfeleltetes.tsv` `igehely_kjv`-jét olvassák: `karoli_strong/tokenek.py` (+ `elopar_kjv.py`), `f17/macula_kk.py`, `olvaso_pilot/adat.py`, `fj2/bsb_import.py`, `nave_import.py`; hatásukat a B-oldali M2 mérje.
