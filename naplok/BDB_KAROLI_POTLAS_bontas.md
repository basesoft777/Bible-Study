# BDB_KAROLI_POTLAS_bontas.md — E17/DT3 bontási napló (F80.7–F80.12)

*FELADATOK #80 · 2026-10-12 · ág: claude/f80-karoli-potlas · a main-hez képest.*

**Új tábla: `adat/bdb_karoli.tsv`** (a main-en nincs): Δ = +62 526 adatsor (a `#` fájlszintű sor és a fejlécsor nélkül). Generált (`python eszkozok/bdb_adatblokk.py --karoli-epit`).

| Kategória | Sor | Megjegyzés |
|---|---|---|
| `tipus=szocikk` | 674 | szócikkenként egy sor (a `forditasok.tsv` kész BDB-szócikkei: `teljes`, `forditas_hu`; sonnet 648, opus 20, kezi 6); `[NINCS KÁROLI-ALAK]` jelzés: 0 |
| `tipus=alak` | 61 852 | szócikkenként egy sor minden különböző kisbetűs Károli-szóalakra; `pelda_versek` hivatkozás (legfeljebb 3 vers), szöveg nincs |
| **összesen** | **62 526** | = 674 + 61 852 |

Más adat/konkordancia-tábla sorszáma nem változott; az `adat/forditasok.tsv` bájtra változatlan (sha256 `f01130a1…2081` az építés előtt és után).

**A F80.7–F80.12 javítás hatása az új tábla soraira** (az előző változathoz képest, ugyanaz a 62 526 sor): a sorszám azonos; a `pelda_versek` 5 550 `alak` soron változott (kanonikus könyvsorrend); a `magas`/`alacsony`/`tahot_elofordulas`/`par_db` mező 0 soron; a `proveniencia` mind a 62 526 soron kitöltve (az `alak` soroké = a szócikk soráé), a fájl 12,3 MB.

**Mellékhatás az adatblokkra (#38):** a `bdb_adatblokk.parok_konyvek()` a #38 adatblokkjának 2. szakaszát (példaversek) is táplálja; az új BDB-adagok blokkjában a példaversek a `Konyv_normalizalo_tabla.tsv` sorrendjében, nem fájlnév szerint választódnak (az 1–5Móz és Józs után Bír, Ruth, 1Sám, … és nem 1Krón, 1Kir, …). Az 1. szakasz egy sora is pontosabb: „a TAHOT-ban %d előfordulás; a Károli–Strong párosításban %d link (egy előfordulásra több link is eshet)” (előtte: „ebből %d kapott Károli-párt”, ami téves volt). A már lefordított szócikkek szövege nem változik. Jelzés: `NYITOTT_FELADATOK.md` `N-F80a`.
