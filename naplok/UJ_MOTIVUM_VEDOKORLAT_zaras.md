# UJ_MOTIVUM_VEDOKORLAT_zaras.md — F148 zárójelentés

*Proveniencia: scope=F148 (`F148_UJ_MOTIVUM_VEDOKORLAT_BRIEF.md`, ág `claude/f148-vedokorlat-4b117b`, F148.0–F148.12; PR #535) | forras=`gh pr view 535` (MERGED 2026-11-01T09:44:55Z, merge-commit `15fd0630`, `git merge-base --is-ancestor` → a main-en), `gh pr view 528` (MERGED 2026-11-01T10:30:54Z), `DONTESEK.md` (DT437–DT441 sorai), `naplok/F148_UJ_MOTIVUM_VEDOKORLAT_naplo.md` 0.–8., `adat/funkcio_kapcsolok.tsv`, `NYITOTT_FELADATOK.md` | ts=2026-11-02 | modell: claude-opus-5-5 (a zárás; a végrehajtás modelljét a napló rögzíti)*

A zárás oka: a munka a PR #535-tel 2026-11-01-én bekerült a main-be, de a brief fejléce `dontesre_var` maradt. A zárás csak a fejlécet, ezt a jelentést és az át nem vezetett N-tételeket írja. Lexikont, adatot és kódot nem változtat.

## Mit hozott a #535

- **(a) A gerinc alapból be.** A kivétel adat, nem kódbeli konstans (DT437): a `SZOTARI_GERINC` motívum-sora `kivetel` állapotú az `adat/funkcio_kapcsolok.tsv`-ben (SEMA 2.44). Ma 7 sor: ANTROP-001, HAMART-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001 (a #123 hátralévő hat motívuma) és TEREMT-002 (a #12 adatcommitjáig). Elfogadás: a 8 lexikonlap és a 6 törzscikk a változás előtt és után bájtra azonos (14/14).
- **(b) Négy új szabály az `ellenoriz.py`-ban:** 18. gerinc-Strong címkéje; 19. kötelező `karoli_szo`/`lexikon_szotar`/`lexikon_entry_id`/`jelentes_szam` (kivétellistán JELENTÉS); 20. a `jelentes_hu` a szóról szól (az 1Kir 18:25–26 BDB-szövege nem jelez); 21. a generált lap tisztasága (helyőrző, „a(z)”, nem létező DT/N). A 21. (iii) pontja (fordítatlan egység) nem lett SÉRTÉS-szabály: N-F148a.
- **(c) `eszkozok/szakasz_cimke_levezet.py`:** a szakasz és a címke gépi levezetése a `jelentes_szam`-ból, nyolc jelzéstípussal (J1–J8), `--ir` csak jelzés nélküli sorra. Regresszió: ISTENTISZT-001 33/33, ALVIL-001 72/72.
- **SEMA:** 2.2.2 (`tagolatlan`, DT438), 2.40 (gépi levezetés, DT439), 2.44 (`kivetel`).
- **⛔ A feloldása (DT441):** az ALVIL-001 59 H7585-sorának gépi kitöltése (`naplok/F148_alvil_kitoltes.py`), utána az `ellenoriz.py` SÉRTÉS 0.
- **Ellenőrzés:** független ellenőr (`naplok/ELLENOR_F148_UJ_MOTIVUM_VEDOKORLAT.md`, 5 ELTÉRÉS, az 1–4. javítva, az 5. dokumentált eltérés); tesztek és CI-emuláció a napló 5. szakasza szerint.

## A ⛔ pontok

| Pont | Döntés | Állapot |
|---|---|---|
| 0. — DT437 (a kivétellista helye) | a felhasználó, 2026-11-01 | 🟢 alkalmazva (F148.1) |
| 0. — DT438 (tagolatlan szócikk) | a felhasználó, 2026-11-01 | 🟢 alkalmazva (F148.4) |
| 0. — DT439 (a levezetett címke) | a felhasználó, 2026-11-01 | 🟢 alkalmazva (F148.3) |
| 0. — DT440 (a 21. szabály súlyossága) | a felhasználó, 2026-11-01 | 🟢 alkalmazva (F148.2) |
| ⛔ A — DT441 (az ALVIL-001 59 sora) | a felhasználó, 2026-11-01 („A #148 gépileg”) | 🟢 alkalmazva (F148.11–F148.12) |
| 5. — a merge | a felhasználó | ✅ PR #535, 2026-11-01 |

A `DONTESEK.md`-ben nincs nyitott (🟡) #148-tétel.

**A `kovetkezo` mező feltétele** („a #528 BDB-sorrend PR-ja után az ALVIL-001 újragenerálása kell”) teljesült. A #528 a #535 után mergelt (2026-11-01T10:30:54Z). Az ALVIL-001 lapot utána a #528 (N-F131y.3) és a #152 (F152.4, F152.6) is újragenerálta. A zárás ellenőrzésként újrarenderelte a lapot a main-állapoton, a lap saját generálási napjával (`PARDES_DATUM=2026-10-29 python eszkozok/general.py --cel lexikon --id ALVIL-001 --kimenet <repón kívüli ideiglenes könyvtár>`). Az eredmény a commitolt laptól csak a sorvégben (CRLF) tér el (`diff --strip-trailing-cr`: üres).

**A brief 6. szakasza (javaslat a #125-nek):** a C-x és a C-y lépés a #125-tel bekerült a `MUNKAMENET.md` C) szakaszába; átvezetve.

## Mi maradt N-tételként

| Jel | Tárgy | Állapot |
|---|---|---|
| N-F148a | a fordítatlan egység gépi mérése (21. (iii)) | már a `NYITOTT_FELADATOK.md`-ben (F148.5) |
| N-F148b | a Macula `karoli` oszlopa elavult | már a `NYITOTT_FELADATOK.md`-ben (F148.5) |
| N-F148c | a `kivetel` sor törlése a #123/#12 menetében; a #123 és a #12 briefje nem mondta ki, az `ir`-jükben nem állt a tábla | **új** (zárás) |
| N-F148d | a `naplok/F131_dbh_meres.py` a megszűnt konstanst olvassa | **új** (zárás; a napló 5. szakaszának „Mellékhatás” pontja) |
| N-F148e | azonos útnál redundáns „alá esik” mondat (az ALVIL-001-en 61 lábjegyzet) | **új** (zárás; a napló 8. szakaszának „Megfigyelés” pontja) |

A brief lezárása ezektől nem függ.
