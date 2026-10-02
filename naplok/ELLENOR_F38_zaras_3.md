# Független ellenőrzés: F38 BDB_FORDITAS, zárómenet 3. kör (DT-F38g)

*A `fuggetlen-ellenor` ügynök (a8a27a79df5af3f77) jelentése; fájlt nem írhatott, a szöveget a fő session mentette át, a táblázatok tömörítve. A 2. kör jelentése: `ELLENOR_F38_zaras_2.md`.*

- **Brief:** `E:\Letöltések\F38_zaras_DT-F38g.md`
- **Tartomány:** `2aceb70..659ee79` (082c77a = F38.278, 659ee79 = F38.279)
- **Bash-korlát:** csak `git diff`/`git log`, `lekerdez.py`, `futtat.py`; a teszteket és az `ellenoriz.py`-t nem futtatta (NEM ELLENŐRIZHETŐ).
- **Összesített eredmény: ELTÉRÉS, 7 tétel**

## Eltérések súlyosság szerint

1. **E5 HIBA (CI):** a `ELLENOR_F38_zaras_2.md` „## Kezelés (a fő session megjegyzése)” címsorát átnevezték, ez törölt címsornak számít `TÖRLÉS-SZÁNDÉKOS:` jelölés nélkül (`futtat.py --valtozott <8 fájl> --diff-alap 2aceb70 --diff-fej 659ee79`). Minden más ellenőrzés (E2–E16, E19) 0 találat. A napló a CI állapotát nem rögzíti.
2. **DT-F38g „✅ alkalmazva” (`DONTESEK.md:52`):** a sor három nyitott tételt tartalmaz: a `FORRAS_VERS_OCR` **jóváhagyásra** vár, a H7451 és a H4390 tartalmi kétség. A `NYITOTT_FELADATOK.md`, `FELADATOK.md`, `F38_BDB_FORDITAS_BRIEF.md` fájlokban nincs döntésre váró tételként rögzítve.
3. **`FORRAS_VERS_OCR` (`forditas_kapuk.py:53-57, 587-598`):** a hatóköre helyes (csak a `2_versszam` forrásparaméterére hat, a `Gen 33:816t` egyetlen helyen áll: `BDB_teljes_unabridged.tsv:3976`, H4264), de nincs rá egységteszt és negatív hatóköri teszt, csak közvetett lefedés (`teszt_bdb_zaras.py:83-89`).
4. **Kezelés, 3. tétel (`ELLENOR_F38_zaras_2.md:73`):** commit-azonosító helyett „a 3. kör commitja” áll; helyesen 659ee79 / F38.279.
5. **A1 / proveniencia:** a napló H4264-sora `lekerdez.py karoli "1Móz 33:8"` eredményre hivatkozik `scope=… | forras=… | ts=…` sor nélkül (CLAUDE.md 1. szabály). Az állítást az ellenőr saját futtatása igazolta (`scope=range:1Móz 33:8 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=0 | ts=2026-10-02T16:37Z`; `1Móz 33:81`: „Nincs Károli-szöveg ehhez”).
6. **`BDB_FORDITAS_zaras3.py:49-50, 116-119` nem idempotens:** a H5674 `uj` értéke tartalmazza a `regi`-t, ezért egy második `--ir` futás „a Szellemről a Szellemről” szöveget írna. A tesztben (`if regi not in uj`) ez kezelve van, a szkriptben nincs.
7. **Brief-fejléc:** az `F38_BDB_FORDITAS_BRIEF.md` utolsó módosítása 7c70f88 (F38.276), a 3. kör nem frissítette (CLAUDE.md: minden menet a saját briefje fejlécét frissíti).

**Megítélésre, nem eltérés:**
- H5674: a végrehajtó „a Szellemről”-t írt a brief „az Úr Szelleme” alakja helyett (a BDB-ben „az Úr” nincs).
- H7451: a brief szabályának betűje szerint („ahol a BDB maga mondja »divine spirit«”) nagybetű járna (`BDB_teljes_unabridged.tsv:6966`: „of the divine spirit as producing an ecstatic state”); ez ütközik a DT-F38f 3. „rossz szellem kisbetűs” szabályával. Nyitva hagyni védhető.

## Pontonkénti eredmények (OK, ha nincs jelölve)

| pont | eredmény | indok |
|---|---|---|
| Brief 0 (Sonnet) | OK | mindkét commit trailere `Claude Sonnet 5.5` |
| (1) H3772 (`forditasok.tsv:255`) | OK | „helyet rendszerint így fordítják: RV made for thee a covenant with them,” |
| (2) H5674 1Kir 22:24 (`:177`) | OK (megítélésre) | `{+a Szellemről+}`; forrás `:5314`, 9a `:6834`; Károli: „…az Úrnak lelke…” (`scope=range:1Kir 22:24 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | n=1 | ts=2026-10-02T16:37Z`) |
| H5674 táblaindoklás | OK | régi áthúzva, az új a 9a-ra hivatkozik |
| (4) H4397 (`:304`) | OK | „(az RV angel szava túl szűk)” |
| (5) H4264 (`:301`) | OK | „33:8, összesen 16-szor”; listáról és a teszt `marad` halmazából kivéve |
| (6) H2403 (`:88`) | OK | megjegyzés: kézi javítás (RV/AV-glossza); a „(1)” címke (5)-re javult |
| DT-F38g új sor, régi megmaradt (`DONTESEK.md:52`) | OK | +1/−0 |
| 4c nagybetűs, 3d Elihu kisbetűs | OK | forrás `:6834`: „God's spirit: Gen 6:3”, „Job 32:18 (Du breath; Di Bu divine spirit…)”; Elihu szellemére nincs külön magyar szó |
| teljes Szellem-tábla újranézve | OK | a H5650, H7307, H7451, H5307 helyei mind a táblában; a H2451 és H5012 helyei nincsenek a `forditasok.tsv`-ben |
| H7451 és H4390 a listán | OK (megítélésre) | indoklással, „tartalmi kétség” jelöléssel |
| `FORRAS_VERS_OCR` hatóköre | OK | l. 3. eltérés |
| teszt a kapubővítésre | **ELTÉRÉS** | l. 3. eltérés |
| `allapot`/`modell`, törölt sor | OK | numstat 5/5; csak `forditas_hu` és `megjegyzes` változott |
| javítási lista +4 (`zaras_javitasok.tsv:447-450`) | OK | H3772, H5674, H4397, H4264 `igen (kézi, DT-F38g N)`; a H2403 csak megjegyzés, nem szerepel |
| „Kezelés”, javítva: <commit> | **ELTÉRÉS** | l. 4. eltérés |
| CI-jelentés (saját futtatás) | **ELTÉRÉS** | l. 1. eltérés |
| tesztek, `ellenoriz.py`, kapuk a 269 soron | NEM ELLENŐRIZHETŐ | Bash-korlát |
| DT-F38g állapota / A2 | **ELTÉRÉS** | l. 2. eltérés |
| A1 / proveniencia | **ELTÉRÉS** | l. 5. eltérés |
| Brief-fejléc | **ELTÉRÉS** (alacsony) | l. 7. eltérés |
| `zaras3.py` újrafuttathatósága | **ELTÉRÉS** (alacsony) | l. 6. eltérés |
| A3–A5 | nem alkalmazható | nincs tanulmányszöveg, PaRDeS-réteg, tanító |
| A6 (E12–E15) | OK | 0 találat |
| CL1 (törölt/módosított sorok) | OK | `forditasok.tsv` 5 módosult, 0 törlés; lista +4; `DONTESEK.md` +1; napló +89/−6 (a 6 sor a 2. köri táblák helyben javított sora; a 3d és 4c régi indoklása jelölés nélkül íródott felül, „(DT-F38g 3)” hivatkozással) |
| CL2 (lefedettség) | OK | a Szellem-ellenőrzés minden `BDB`/`teljes` soron fut; 14 nagybetűs hely = `SZELLEM_KOVETELT` 14 eleme |
| CL3 (nulla-diff hatóköre) | OK | `allapot`, `modell`, kulcs, dátum, verzió változatlan |
| CL4 (E17/DT3) | OK | `forditasok.tsv` +251/−8 a mainhez, Δ = +243; a tartományban 5/5, Δ = 0 |
| CL5 (⛔ pontok) | OK | nincs ⛔ |

## Kezelés

Állapot: nyitott; a gépies tételeket (1, 3, 4, 5, 6, 7) a következő commit kezeli. A 2. tétel, a H5674 szövegezése, a H7451, H4390 kétségek és a `FORRAS_VERS_OCR` jóváhagyása a felhasználó döntésére vár.
