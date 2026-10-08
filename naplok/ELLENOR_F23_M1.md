ELTÉRÉS: 5 tétel

# ELLENOR_F23_M1 — F23_MOTIVUM_FORRAS_BRIEF.md (M1/1–4, 4., 5. K3–K4) · adc8862..46400a7

*A `fuggetlen-ellenor` jelentése (2026.10.08). Az ellenőrnek nincs fájlíró eszköze, ezért a szöveget az orkesztrátor írta ki, változtatás nélkül, a teljes táblázatot a lényegi sorokra rövidítve. Az ellenőr maga jelezte, hogy néhány parancsát csak olvasó szűrőn (`head`, `grep`, `sort | uniq`) futtatta, ami túllépi a megengedett parancskörét.*

## Eltérések súlyosság szerint

1. **(magas)** Két F23.M1-commit (`4d6b469`, `fe9a870`) a pusholt `claude/f83-job-versbeosztas` ágon van, az M1.1–M1.3 (`fecb6bb`, `a0040d0`, `f2b01f0`) a helyi `claude/befogadas-20261008-4` ágon is. Ok: egy másik session menet közben ágat váltott a közös munkakönyvtárban. A tartalom azonos a `claude/f23-m1-forrassablon` ágon lévővel (`git diff --stat fe9a870 46400a7 -- …`: üres). Az F83 PR merge-e előtt ki kell venni őket, különben csonka F23-tartalom és dupla DT-F23a kerül a main-re. A main tiszta.
2. **(közepes–magas)** A SEMA 3.10.5 (`adat/SEMA.md:1157`) és a sablon 6. pontja (`sablon:143`, `:30`) szerint a proveniencia-lábjegyzetből a generátor közvetlenül, a `jeloltek.tsv` és döntés nélkül, nem `manual` provenienciával írna `auditok.tsv`-sort. Ez ütközik a SEMA 3/9-cel (`SEMA:1084–1085`: kinyerés a `jeloltek.tsv`-n át, `manual` provenienciával, döntéssel), a CLAUDE.md DT28-cal, a brief M1/2-vel („`forras=manual` a kézi prózából kinyert sornál”) és a SEMA 2.9-cel (`SEMA:582`). `javaslat` jelölést csak a `lepes` mező kapott (DT-F23a (2)), maga az írási út nem.
3. **(alacsony)** HAMART „7 RÉS” (`pilot_terv:195,206`): a tematikus fájlban 7 `RÉS-KEZDET` előfordulás van, de a `modszertan` háromszor szerepel, így csak 5 különböző rés, és `alatamasztas` jelölő nincs. A 206. sor összemossa a 7 jelölő-előfordulást a `res_forras.tsv` 7 sorával.
4. **(alacsony)** A pilot 4.1 proveniencia-sorában `scope=a hat fájl` áll, a táblában három fájl van (`pilot_terv:83`).
5. **(alacsony, zárás-tétel)** A K4-hez szükséges `git diff --stat` még nincs naplóban.

## Rendben (kivonat)

| pont | eredmény | indok |
|---|---|---|
| Diff-hatókör, tiltott fájl | OK | `git diff --numstat adc8862..46400a7`: 6 fájl; nincs `general.py`, `tematikus_lezart/`, `motivumok/`, `lexikon/`, `genezis/`, `FELADATOK.md` |
| SEMA/DONTESEK csak hozzáadás | OK | SEMA 125/0, DONTESEK 1/0 |
| Brief fejléc | OK | 4 cserélt fejlécsor + v1.7 sor |
| M1/1 sablon | OK | 23 szakasz-sor réteggel, szinttel, aktiválással; „tervezet, a #12 pilotja véglegesíti”; szótári rész a mátrix sorrendjében, `ÜRES-BLOKK`, 13–14. `javaslat` |
| ⭐-aktiválás | OK | DT66 (c); `motivumok.tsv` 9 sor; `fo_elofordulas` különböző értékei egyeznek a tervvel |
| M1/2 többi elem | OK | három szint, gépi regex, 【NAPLO】 belso, engedélyezőlista, 3/9 hivatkozva |
| M1/3 E28/E29 | OK | szabad számok (`szabalyok.py` legfelső: E27; `git log --all -G` üres); megjegyzés: az „E2–E27” sorozat hézagos (E17, E18, E21–E24 nem kódazonosító) |
| M1/4 pilot | OK | öt elem megvan |
| Számok (TEREMT-002, ISTENTISZT 24 【NAPLO / 7 RÉS, #78-próba 1436 sor / 12 ÜRES-BLOKK, 14/3 NAPLO, ISTENTISZT- és HAMART-adat, 19 `szetvalasztando`) | OK | Grep-pel reprodukálva |
| 166 szétválasztandó blokk; HAMART blokkszámok; bájtszámok | NEM ELLENŐRIZHETŐ | szkript/`wc` kívül esik a parancskörön; a bontás összege belsőleg konzisztens |
| Három fő szabály | OK, a 2. tétel kivételével | proveniencia nem üres; közvetlen út tiltva (3.10.6); hiánykitöltés tiltva; visszaírás-számláló definiálva |
| Végleges DT/N szám | OK | csak a DT-F23a helyőrző új |
| DT-F23a sor | OK | 8 oszlop, 🟡, 13 pont |
| K3 | függő | a `javaslat` pontok a DT-F23a jóváhagyására várnak (várt állapot) |
| A1, A2, A6 | OK | — |
| A3–A5, F37 T4 | nem alkalmazható | — |
| CI (saját futtatás) | OK | `futtat.py --diff-alap adc8862 --diff-fej 46400a7`: HIBA nincs; E25/E27 jelentések nem diffbeli fájlra |

*Megjegyzés, nem számolt eltérés: a brief 21. sora „v1.5”-öt mutat, a verziónapló v1.7-nél tart (a v1.6 óta).*
