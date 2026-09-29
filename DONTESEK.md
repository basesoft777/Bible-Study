# DONTESEK.md — nyitott döntések sora

*A chat csak ezt a fájlt kapja. Egy tétel = egy döntés. Az orkesztrátor nyit tételt, a felhasználó (a chattel) dönt, az orkesztrátor alkalmazza.*

Állapot: 🟡 nyitott · 🟢 eldöntve, alkalmazásra vár · ✅ alkalmazva

| # | Feladat | Kérdés | Opciók | Javaslat | Állapot | Döntés | Napló |
|---|---|---|---|---|---|---|---|
| DT1 | #7 Thayer-fordítás | „döntés a v3-ról („természetes hű” stílus a promptban) + költség újraszámítása a teljes Thayer_teljes.tsv hosszeloszlásából (a P6 ~30 USD-ja nem vezethető le, naiv skálázással ~62 USD; ELLENOR_FP.md 1. eltérés)” *(forrás: `FELADATOK.md` #7 „Következő lépés”)* | — *(a forrássor nem sorol opciót; az opciókat a `FORDITAS_ELES_THAYER_BRIEF.md` v2 / chat adja)* | — | ✅ | lezárva: a #7 döntése a main-en rögzítve (FP2-D13–D15, `bd4b32f`; #7 sor: `1ef61a3`)
| DT2 | #10 lexikonoldalak lezárása | „döntés az L6 és L7 feltételről. Ide tartozik N18, N19” *(forrás: `FELADATOK.md` #10 „Megjegyzés”)* | — *(a forrássor nem sorol opciót; a brief csak chatben van)* | — | 🟡 | | |
| DT3 | #2 CI (E17) | E17: adattábla sorszámának mekkora változása kívánjon bontási naplót? *(forrás: F15 brief 3.4)* | 1% / 5% / abszolút sorszám | 1% | 🟡 | | |
| DT4 | #14 száma | A `main`-en a `#14` szám már a Thayer-stíluspróbáé (FP2, kész; a #7 „#14 (kész)” függést hivatkozza), az orkesztrátor-feladat sora is `#14` (F14 brief). Melyik számot kapja az orkesztrátor-feladat? *(forrás: az F14.3 merge-konfliktus)* | 1. #15 (sor, brief fájlneve `F15_…`, ág marad) / 2. #14 marad az orkesztrátoré, az FP2 hivatkozásai átírva / 3. más szám | 1 (#15), mert az FP2 hivatkozásai már mainen vannak | ✅ | #15 (F15_ORKESZTRATOR_BRIEF.md; az ág neve marad `claude/orkesztrator-14`)
