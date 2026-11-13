---
feladat: 217
cim: Generált nézetek a main-en, Actionnel — jegyzék és újragenerálás
kod: GENERALAS_MAINEN
tipus: feladat
fazis: folyamat
modell: opus
allapot: megallt
ag: claude/f217-generalas-mainen-f752cc
ad: a generált nézeteket nem az ágak commitolják, hanem egy Action generálja újra a main-en egy jegyzék (`adat/generalt_nezetek.tsv`) szerint; a párhuzamos PR-ok nem várnak egymásra a generált fájlok miatt; a jegyzék a bemeneti jegyzék első lépése
kovetkezo: "Te: a #709 mergelve; indulás a heti reset után (2026-11-14 14:00 UTC), orkesztrátori döntés (keret); a terv átnézése kész (O1–O6 elfogadva, két kiegészítés; naplok/F217_terv.md 5.); a megvalósítás (F217.2–) az orkesztrátor jelzésére"
munka: folyamat
olvas: [adat/SEMA.md, adat/lap_befagyasztas.tsv, eszkozok/szamkiosztas.py]
ir: [adat/generalt_nezetek.tsv, adat/SEMA.md, .github/workflows/generalt_nezetek.yml, .github/workflows/ellenorzes.yml, .claude/commands/kiadas.md, eszkozok/generalt_nezetek.py, eszkozok/teszt_generalt_nezetek.py]
fugg: [216]
---

# F217_GENERALAS_MAINEN_BRIEF.md — Generált nézetek a main-en, Actionnel

*FELADATOK #217 · Modell: opus · v1 · 2026.11.12 · forrás: a felhasználó jóváhagyása (2026-11-12, „Igen, mindkettőt”), az orkesztrátor feladatleírása*

## 1. Cél

A párhuzamos PR-ok ne várjanak egymásra a generált fájlok miatt. Ma minden ág commitolja a generált nézeteket is: `lexikon/*_TUDOMANYOS.md`, `lexikon/*_TORZSCIKK.md`, `nyilt_mag/`, napló- és nyitott-nézetek, `generalt/`. Ezért egy merge után a többi ágnak be kell hoznia a main-t, újra kell generálnia, és újra kell futnia a CI-nek. Példa: a #710 csak emiatt vár a #715-re.

## 2. Tartalom

1. **Leltár:** mely generált fájlokat commitolják ma az ágak, melyik generátor írja őket, és determinisztikus-e a kimenet (nincs benne modell-hívás).
2. **Jegyzék:** `adat/generalt_nezetek.tsv` (cél, parancs, bemenetek, kimenet), a `adat/SEMA.md`-ben dokumentálva. Ez egyben a bemeneti jegyzék első lépése (a nyitott „bemeneti jegyzék és zárási fogyasztó-ellenőrzés” tétel).
3. **Action:** a main-re érkező push után (a `szamkiosztas` és a `feladatok` Action mintájára) a jegyzék szerint újragenerál, és egy commitban visszaír.
4. **PR-ban:** a generált fájl változása nem kötelező. Az E28 (generált nézet egyezése) ehhez igazodik. A kapuk (E29, E38, E39, teljesség-kapu) viszont a PR-ban egy ideiglenes generáláson futnak, így a hiba továbbra is merge előtt derül ki.
5. **Kivételek:** a befagyasztott lapok (`adat/lap_befagyasztas.tsv`) és a kiadott lapváltozat nem generálódik újra csendben. A kiadás menetét (`kiadas.md`) ehhez igazítani.
6. **Átnézés:** a PR a renderelt lapot ideiglenes kimenetként mutatja, a repón kívül.

## 3. Megállás

⛔ A leltár (1.) és a terv után megállás: az orkesztrátor nézi át (nem a felhasználó). Utána megvalósítás.

## 4. Megkötések

- Időzítés: a #715 (F212, CS3) és a #710 (F208) mergelése UTÁN indul, mert azok generált fájlokat írnak; és az F216 (PUSH_ELOTTI_KAPU) után, mert mindkettő az `.github/workflows/ellenorzes.yml`-t írja.
- A generátor nulláról való újraírása később jön; a jegyzék úgy készüljön, hogy az új generátor csak a jegyzék sorát cserélje.
- Új adattábla: `adat/SEMA.md` bejegyzés és gépi kapu a séma szerint.
