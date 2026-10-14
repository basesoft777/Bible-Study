# Független ellenőrzés — F95_SZOTOVEZES_DB_BRIEF.md · 0f5990f5..3b7d9d27 (claude/f95-szotovezes-db)

*Ellenőr modellje: claude-opus-5-5 (kért: opus, egyezik). Az ellenőr nem tudott fájlt írni, a jelentést az orkesztrátor mentette el az ellenőr jelentéséből, tartalmilag összevonva.*

**Összegzés:** ELTÉRÉS: 3 tétel, mind dokumentációs vagy folyamati. A betöltött adatban, a kódban és a K1–K4 tartalmában hibát nem találtak.

| pont | eredmény | indok |
|---|---|---|
| 0 modell | OK | a menet `modell` mezői (`claude-sonnet-5-5`) egyeznek a 8 commit trailerével |
| K1 | OK | 66 824 adatsor, 0 `simplemma` sor, a `szoto_tablak` licencsor megvan; a *alak* sor (fájl 12188.) nem vész el fejlécként |
| K2 | OK, a DB-szám nem ellenőrizhető | 99,7789% (483 748/484 820); kötőjeles táblával 99,9988%; az 1 072 nem illeszkedő token osztályozva, a szúrópróba verseken az osztálypéldák valósak |
| K3 / D5 | OK | `D5_TOVABBI` lista, a `frissesseg()` az új három táblán fut; a D4 mérését nem érinti |
| K4 | OK | az (a) mód és a kereső tábla legfeljebb 20,6 ms (hideg); az időket az ellenőr nem futtatta újra |
| K5 | NEM ELLENŐRIZHETŐ | a 61 teszt darabszáma stimmel; a futtatás nem megengedett parancs az ellenőrnek |
| (c) mód 173–874 ms | OK | a zárójelentés a #76 felé ismert korlátként rögzíti |
| `tablameret()` javítás | OK | a UNIQUE INDEX az `x` sémába irányul; a mért hatás konzisztens |
| DT141 (1)–(4) | OK | a kód megfelel a jóváhagyott döntésnek |
| DT141 jóváhagyás | nem ellenőrizhető a repóból | a sorrend rendben: ⛔ megállás `1e6c6b1a`, jóváhagyás `81c38b34`, építés csak utána |
| Egyeztetett eltérés (#22) | OK | `adat/karoli_strong` és `adat/szoto` diffje üres, a `szavak_*.tsv` nem változott |
| L1–L4 | OK | adatsor nem törlődött; minden `adat/**/*.tsv` Δ = 0 |
| CI (saját futás) | OK | `futtat.py` rc=0; az E25/E27 találatok a diffen kívüli fájlokra vonatkoznak |

## ELTÉRÉSEK (súlyossági sorrendben)

1. `naplok/SZOTOVEZES_DB_zaras.md:5`, `naplok/SZOTOVEZES_DB_M0.md:96` és az a5384877 commit „15 próbapont megegyezik”-et ír, a próbanapló szerint viszont 9/9. A zárójelentésben téves szám áll.
2. `adat/SEMA.md:1167`: a gyakori lemmák (c) idejét „120–870 ms”-nak írja, a mért érték 173–874 ms (a 120 egy tartalmas lemmáé).
3. `F95_SZOTOVEZES_DB_BRIEF.md:16`: az `ir` mezőből hiányzik a `DONTESEK.md`, a `naplok/SQLITE_EPIT_integritas.md` és a `naplok/SQLITE_EPIT_proba_teljes.md`.

**Megjegyzés (teszt):** a `test_f95_kotojeles_segedtabla` `COUNT(DISTINCT igehely||sorszam)` elválasztó nélkül fűz; most nincs hatása.

**Nem igazolt:** a K5 tesztek futtatása, a DB-beli számok saját lekérdezéssel, a CI-jelentés (nem érkezett bemenet).
