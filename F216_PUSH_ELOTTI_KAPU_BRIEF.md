---
feladat: 216
cim: Helyi kapu push előtt — a CI bukó lépései helyben, egy szkriptben
kod: PUSH_ELOTTI_KAPU
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: nem_indult
ad: egy `eszkozok/push_elott.py` szkript, amely helyben ugyanazt futtatja, amit a CI bukó lépései, így a HIBA a push előtt kiderül, nem a CI-ben; a CI ugyanezt hívja, és a HIBA-sorokat a logba is kiírja
kovetkezo: "Indítás a #715 (F212) mergelése után, mert az F212 is írja az `.github/workflows/ellenorzes.yml`-t (E38–E39 lépés); Te: /kovetkezo"
munka: folyamat
olvas: [eszkozok/ellenorzes/futtat.py]
ir: [eszkozok/push_elott.py, eszkozok/teszt_push_elott.py, .github/workflows/ellenorzes.yml, .claude/commands/kovetkezo.md, .claude/commands/kiadas.md, .claude/commands/lap-javit.md]
fugg: []
---

# F216_PUSH_ELOTTI_KAPU_BRIEF.md — Helyi kapu push előtt

*FELADATOK #216 · Modell: sonnet · v1 · 2026.11.12 · forrás: a felhasználó jóváhagyása (2026-11-12, „Igen, mindkettőt”), az orkesztrátor feladatleírása*

## 1. Cél

A piros CI-körök megszüntetése. Ma a session pushol, és csak a CI-ből derül ki a HIBA; egy kör kb. 4 perc CI és egy session-kör (példa: #715, run 43277531095). A cél, hogy ugyanaz az ellenőrzés helyben, push előtt lefusson.

## 2. Tartalom

1. **Szkript:** `eszkozok/push_elott.py`. Helyben pontosan azt futtatja, amit a `.github/workflows/ellenorzes.yml` bukó lépései: E1; E2–E39 (`eszkozok/ellenorzes/futtat.py` a változott fájlokkal, `--diff-alap origin/main`); a szabály-tesztek; `feladatok.py ellenoriz` és tesztjei. Kimenet: HIBA-sorok és kilépési kód.
2. **Egyezés a CI-vel:** a CI ugyanezt a szkriptet hívja, vagy egy kapu ellenőrzi, hogy a szkript és a workflow lépéslistája egyezik. Ne térhessen el egymástól a kettő.
3. **Napló:** a CI a HIBA-sorokat a logba is kiírja, ne csak a lépés-összefoglalóba és a PR-kommentbe.
4. **Parancsfájlok:** `.claude/commands/kovetkezo.md` (a push előtti lépés), `kiadas.md` 6. lépés, `lap-javit.md`: push csak akkor, ha a `push_elott.py` 0 HIBA-val fut. Egy szabály, egy hely: a szabály szövege egy helyen áll, a többi csak hivatkozik. A parancsfájlok módosítását a felhasználó ezzel a jóváhagyással engedélyezte.

## 3. Hatókör

`ir`: l. a fejléc. Egy teszt (`eszkozok/teszt_push_elott.py`) a szkriptre. Az ellenőrzések (E1–E39) tartalmához nem nyúl.

## 4. Kész, ha

- a szkript a mai main-en 0 HIBA-t ad;
- egy szándékosan rontott próbán HIBA-t ad;
- a CI zöld.

## 5. Időzítés

A #715 (F212) mergelése után indul, mert az F212 is írja az `.github/workflows/ellenorzes.yml`-t (E38–E39 lépés). Az F217 (GENERALAS_MAINEN) ettől függ, mert mindkettő a workflow-t írja.
