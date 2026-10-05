# ELLENOR_F51.md — F51_KONZISZTENCIA_BRIEF.md · `fuggetlen-ellenor`, 2026-10-05

*Tartomány: origin/main..2bd7339 (F51.0–F51.7). A jelentést az ellenőr adta vissza (nem volt fájlíró eszköze); a fájlt az orkesztrátor írta, az ellenőr szövegének tartalmával, tömörítve. Az ellenőr nem futtathatta a teszteket és a `feladatok.py ellenoriz`-t; ezeket az orkesztrátor futtatta (lent).*

**Eredmény: ELTÉRÉS, 6 tétel.** Minden más pont OK.

## Eltérések és kezelésük

| # | Eltérés | Kezelés |
|---|---|---|
| 1 | **E16 HIBA** a `--valtozott` futásban: az ellenőrzőt érintő PR címe `[ELLENŐRZŐ]` előtagú kell legyen, és külön felhasználói jóváhagyást kér (F02, D5) | A PR címe `[ELLENŐRZŐ]`-előtagú; a merge előtti külön jóváhagyás a felhasználóé (⛔, a zárójelentésben) |
| 2 | A `/konzisztencia` parancsot nem a parancs futtatta: az első jelentés kézi utánzat | Nyitva; az első valódi futás a `konzisztencia-napi` feladat első futása (a parancs csak a merge után él a `main`-en) |
| 3 | A jelentés számellentmondása (6 kontra 5 találat; RENDER_BRIEF) | Javítva (5; a RENDER_BRIEF archív, nem találat) |
| 4 | A napló „mind az öt sor” szövege elavult (a tábla 3 soros) | Javítva |
| 5 | A brief `ad:` és K5 heti futást ír, nincs verziósor a napi eltérésről | `ad:` napira átírva, v1.1 verziósor; a „heti” szó a 29. és 87. sorban a v1 szövege marad |
| 6 | Pontatlan fájl:sor (FELADATOK 189→191, SEMA 811→812) | Javítva |

Megjegyzés (kis súlyú): a jelentés proveniencia-sora `forras=manual`, miközben futtat.py-kimenetet is idéz; a „CLAUDE.md:35 … a globálisat értik” sor értelmezés.

## Az orkesztrátor saját futtatásai (az ellenőr NEM ELLENŐRIZHETŐ tételei)

- `python -m unittest eszkozok.ellenorzes.tesztek.test_szabalyok` → 74 teszt, OK.
- `python eszkozok/feladatok.py ellenoriz` → 83 brief, 0 hiba, 3 figyelmeztetés (F09, F36, F37: nem a #51-é).
- A K2/K5 chatbeli jóváhagyás és a `konzisztencia-napi` feladat léte gitből nem igazolható; a feladat a felhasználó gépén jött létre jóváhagyással (2026-10-05).
- A (b) ág 2026-10-15-től 3 FIGYELMEZTETES-t ad minden PR-en, ha a #11 akkor is `brief_kell` (várható).
