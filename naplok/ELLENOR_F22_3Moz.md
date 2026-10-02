# ELLENOR_F22_3Moz.md

*A `fuggetlen-ellenor` ügynök jelentése (a hatókör: `759d7d1..685cf0d`, worktree `Bible-Study-f22`), tömörítve a tételekre; az ügynök szerepköre csak olvasó volt (szkriptet nem futtathatott: `egyesit.py --ellenoriz`, bájtazonos újraépítés), a fájlt az orkesztrátor mentette. A „Kezelés” szakasz az orkesztrátoré.*

**Minősítés: ELTÉRÉS: 6 tétel.**

## Rendben (OK)

- **K1:** 859 vers hu- és er-sorral; 86 köteg, folytonos, mind `ok`; er-sorok 18 571 = a TAHOT 3Móz tokenjei; az er-strongok a TAHOT sorrendjében (szúrópróba: 3Móz 1:1 er 1..14 = TAHOT 55773–55786. sor); hu-tokenenkénti lefedettség és a levezethetőség gépi ellenőrzése az ügynöknek **nem ellenőrizhető** (az orkesztrátor oldalán `egyesit.py --ellenoriz`: rendben).
- **Csak-Sonnet:** minden link/szósor `alacsony`/`S` (18 347 / 36 655), `magas`/`kezi`/`fuggoben` 0; nincs C-jsonl (soha nem létezett); a proveniencia-sor `ts=manual`, `forras` helyes.
- **prompt_v3 változatlan** (`git diff f21p/` üres); a subagent-válaszok `forras: subagent`.
- **1Móz/2Móz nem változott** (táblák, jsonl, minta, átnézés a 27c8fa0-hoz képest); az `egyesit.py` módosítása kódolvasás szerint nem hat rájuk (létező C-fájlnál a régi ág).
- **Jelentés számai:** kapuhiba 8/859 (köteg 12, 21, 33, 42, 44, 50 (2 vers), 81), 18 347 link, 36 655 szósor, 0 átnézés; a detektor 3Móz-sora 0/0/0/0 (27 fejezet, d = 0); régi arany 0 hármas (kontroll: Gen/Exo 200); a „gyanús fejezet” magyarázat helyes; szúrópróba a 3Móz 6:1/6:8-on (Károli és TAHOT azonos tartalmú).
- **Jóváhagyott lista:** `tokenek.py:55` `('2Móz', '3Móz')`, más könyv nincs; a `versmegfeleltetes.tsv`-ben nincs 3Móz-sor.
- **Brief fejléc:** `allapot: dontesre_var`, `kovetkezo` „Te:”-vel; a `FELADATOK.md` nem módosult (E18 miatt a szöveg a brief `kovetkezo` mezőjén keresztül kerül oda).
- **Kulcs-grep, zárt licencű adat:** tiszta. **A6:** E12–E15 0. **L1–L3:** adatsor-törlés 0, kulcstartomány teljes (859/859, álkulcs nincs), nulla-diff igazolva.
- **Nem ellenőrizhető (ügynök):** a /usage-mérés (52%→63%), a PR-frissítés, a CI-egyezés.

## Eltérések és Kezelés

| # | Eltérés | Kezelés (az orkesztrátor) |
|---|---|---|
| 1 | `adat/SEMA.md:917` (és 909/914/930): a jóváhagyott lista „2Móz” ellentmond a `tokenek.py:55`-nek; a `ts` és az `alacsony` meghatározása nem fedi a csak-Sonnet könyvet | **Javítva** (SEMA 2.20: jóváhagyott 2Móz, 3Móz; „csak-Sonnet könyv” bekezdés: nincs C-fájl, minden `alacsony`/`S`, `ts=manual`, a „gyanús fejezetek” sor nem eltolódás-jel). |
| 2 | `adat/datasetek.tsv:89–96`: a „jelenleg 1Móz és 2Móz” elavult, a „két modell” a 3Mózesre nem igaz | **Javítva** (3Móz felvéve, csak-Sonnet jelzéssel; a 3Móz-jelentés hivatkozva). |
| 3 | A D2-től eltérő csak-Sonnet döntés nincs rögzítve a brief döntés-/verziónaplójában | **Javítva:** D9 (DT-F22c helyőrző) és v2.3 a briefben; a `DONTESEK.md`-be a számot a main-Action adja a merge után. |
| 4 | K3: a hash-ellenőrzés eredménye hiányzik a jelentésből | **Javítva:** a jelentés 1. szakasza: `prompt_hash_hiba()` → `None` a menet végén, minden köteg előtt a `prompt` parancs ellenőrizte. |
| 5 | A brief `ir:` mezőjéből 7 érintett fájl hiányzik | **Javítva** (a 3Móz-táblák, minta, jsonl, átnézés, jelentés, ellenőri jelentés, `f22_statisztika.py`). |
| 6 | A brief `kovetkezo` mezője elavult („a jelentés még hátra”) | **Javítva.** |
| — | Látens: csak-Sonnet könyvben a javító-fájl meglétekor a nem létező `c/…_javito.jsonl` is bekerülne a forráslistába (`egyesit.py:276–277`) | **Nyitva, nem aktív** (a 3Mózesnek nincs javító menete); a proveniencia-sor csak létező fájlt nevez meg, a hiba csak ilyen vegyes esetben jelentkezne. |
| — | Megjegyzés: az ág le van maradva a `main`-től (licencek.tsv: Karoli_1908 „tisztázatlan”; `SEMA.md` main-oldali változás) | A `main` beolvasztása a PR-frissítéskor történik; a licencstátusz-átvezetés a merge-hez tartozik. |

A javítások utáni **második, független kör nem készült.**
