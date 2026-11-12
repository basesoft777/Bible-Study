# F216 — Helyi kapu push előtt (`eszkozok/push_elott.py`)

*Modell: claude-sonnet-5-5 · 2026-11-12 · alap: `origin/main` (63f3f126) · ág: `claude/push-elotti-kapu` · PR: #724*

## 1. Menet

- `eszkozok/push_elott.py`: a CI bukó lépései helyben (E1; E2–E39 `--diff-alap` a merge-base-zel; E38/E39 `--szigoru`; szabály-tesztek; E18 és tesztjei). Kilépési kód 0 = 0 HIBA. `--lepes <szöveg>`: részleges újrafutás javítás után (nem kapu); `--pr-cim`: az E16-hoz (alap: a nyitott PR címe, `gh`).
- Egyezés a CI-vel: `push_elott.py --ci-egyezes` lépés a workflow-ban (és a `teszt_push_elott.py`, K12): a lépéslista és a workflow `python eszkozok/…` hívásai, valamint az állandó argumentumú hívások szövege egyezik; eltérésnél a CI itt bukik.
- Napló: az E2–E39 HIBA-sorai (`grep`), az E1 jelentése és az E38/E39 jelentés bukáskor a logba is kerül; `--minta 50`.
- A szabály egy helye: `.claude/commands/kovetkezo.md` 6. lépés, „PUSH ELŐTT”; a `kiadas.md` 6. lépése és a `lap-javit.md` 6. pontja hivatkozik rá.
- Ideiglenes könyvtár a repó meghajtóján (Windows): a `test_szabalyok.py` a repó gyökeréhez relatív útvonalat képez, és C:-s `%TEMP%` mellett E:-s worktree-n `ValueError`-ral bukott.

## 2. Mérések

- A mai main-en (a fej `b760a1f4`-et követő commitokkal) a teljes futás: 0 HIBA (E2–E39 83 mp, E1 86 mp, E39 80 mp, E38 27 mp, `test_szabalyok.py` 228 mp, E18 47 mp, feladatok-tesztek 48 mp; összesen kb. 7 perc). A háttérben indítandó.
- Rontott próba: érvénytelen `modell` a brief fejlécében → `push_elott.py --lepes E18`: `HIBA … modell érvénytelen: 'ismeretlen'`, kilépési kód 1. Egy valódi hiba is kiderült: a workflow módosítása miatt a PR címe `[ELLENŐRZŐ]` előtagú kell legyen (E16); a kapu ezt a push előtt jelezte.
- CI a pusholt `fd89bda0`-n: futás 43320932305, success (mindkét job).

## Független ellenőrzés — 1. ellenőrzés

(Az `fuggetlen-ellenor` válasza, változtatás nélkül; a futás a `fd89bda0` head-re.)

ELTÉRÉS: 3 tétel

1. **Az egyezés-kapu megkerülhető** (`eszkozok/push_elott.py:89-120`): a dinamikus hívások (`futtat.py`, `ellenoriz.py`, `feladatok.py`) argumentumait nem veti össze; a nem `python eszkozok/` alakú hívásokat nem látja; a bukás szemantikáját (`|| true`, `continue-on-error`, hiányzó `K<n>` a feltételben) nem nézi; a kikommentelt egyezés-lépés is átmegy.
2. **A helyi kapu más fán fut, mint a CI** (`push_elott.py:196-207`): a CI a `refs/pull/N/merge` fán, a helyi kapu az ág HEAD-jén; nem jelez, ha az ág le van maradva az `origin/main`-hez képest, így a „pontosan azt futtatja” túlállítás.
3. **Ellentmondás és félreolvasható mondat a parancsfájlokban:** a `lap-javit.md:119` („csak ez, kb. 2–5 perc”) ütközik a `:121` teljes kapujával; a `kovetkezo.md:68` „egyetlen helye” mondata félreolvasható (mintha a `/kiadas` lenne a szabály helye).

Rendben: G/2.1 (lépéslista), G/2.3 (napló, megjegyzéssel: a logsor nem tartalmazza az E-számot), 3. hatókör, CI zöld a head-re, A1–A6, ⛔ nincs. Nem ellenőrizhető: a teljes helyi futás ismétlése (nem futtatta újra).

## Zárás

Állapot: az 1. ellenőrzés ELTÉRÉS-t jelzett (3 tétel), a menet a 9. lépés szerint megáll; a javítókör külön sessionben: `/elteres F216`. A kapu működik és a CI zöld a pusholt sha-n, a hátralévő tételek az egyezés-kapu szigorítása (dinamikus argumentumok, kikommentelés), az elmaradt-ág figyelmeztetés (merge-base ≠ `origin/main` csúcsa) és két parancsfájl-mondat.
