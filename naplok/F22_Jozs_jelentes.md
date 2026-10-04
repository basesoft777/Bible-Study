# F22_Jozs_jelentes.md — Károli–Strong párosítás: Józsué (csak Sonnet)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py`, `sonnet_koteg.py`, `egyesit.py`, `f22_elemzes.py`, `versbeosztas.py`, `get_usage`). Ág: `claude/f22-jozs` a `main`-ből (a PR #160 merge-e után). Módszer: `prompt_v3` változatlanul, Sonnet (`vegrehajto-sonnet` subagentek, kötegenként egy, sorban), **a C (Gemini) kimarad** (DT-F22c: lezárva, rossz mérés esetén újranyitható; D12). Munka a külön worktree-ben (`../wt-f22-jozs`).*

## 1. Menet

- **Jóváhagyás (2026.10.04, chat: „mehet a Józsué”)**, a jóváhagyási naplóban (`naplok/F22_versbeosztas_jovahagyas.md`): a detektor szerint a Józs tiszta (`naplok/F22_versbeosztas.md`: 658 Károli-vers, 658 eredeti vers, 24 fejezet, eltolt/K-hiány/E-hiány 0), a listában nincs sora; a `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve. Kézi 1:2 beolvasztás **nincs**.
- **Minta:** 658 vers, 66 köteg (10 vers/köteg, az utolsó 8), `--var 658` egyezik; eredeti nélküli Károli-vers nincs.
- **Hash (K3):** a `prompt_v3` hash-ét a `sonnet_koteg.py prompt` minden köteg előtt ellenőrizte (hiba nélkül; a 66 prompt a menet elején készült el).
- **Keret a `get_usage` szerint** (heti „all models”): a menet elején **9%**, a végén **13%** → **4 százalékpont** a 658 versre. A 85%-os megállási küszöb és a 70%-os indítási feltétel messze alatta. A fogyás a session közbeni más munkát is tartalmazza (felső becslés: az 5Móz ellenőri köre és javítása ugyanebben a sessionben futott, a Józs-menet előtt). Az 5 órás ablak 0%-ról 27%-ra ment.
- **Eljárási megjegyzés:** az 53. köteg subagentje a 2. próbálkozás előtti javításhoz segédszkriptet írt az `f22/_munka/_fix_k053.py` útvonalra (a megbízásán túl; a `f22/_munka/` nem verziózott). A mentett válasz a kapun átment; a köteg-sor formátuma a többivel azonos.

## 2. Szkriptkimenet

```
Sonnet: 66 köteg, 658 vers; kapuhiba első próbára 0.9% (6/658); végleg 0.0% (0/658)
C: 0 köteg, 0 vers
```

Az első próbára elbukott versek kötegenként: 6. (Józs 3:14), 8. (4:18), 11. (6:9), 13. (7:1), 18. (8:24), 53. (20:9) — mind a 2. próbálkozásra átment (a `Jozs.jsonl` `probalkozas: 2` versei; a szám a `f22_statisztika.py`-é).

`egyesit.py --konyv Józs`: `parok_Jozs.tsv` 15 023 sor (mind `alacsony`, `S`), `szavak_Jozs.tsv` 30 405 sor (mind `alacsony`), átnézési sor 0 vers. A szavak bontása: hu 14 668 (12 155 `parositva`, 2 513 `betoldas`), er 15 737 (13 822 `parositva`, 1 915 `forditatlan`); az er szám = a `TAHOT_kivonat.tsv` `^Józs` sorainak száma (15 737). `egyesit.py --ellenoriz --konyv Józs`: „rendben” (minden Károli- és eredeti token pontosan egyszer szerepel, a `strong` a TAHOT-ból levezethető); az újraépítés bájtra azonos (a két tábla SHA-256-ja egyezik). Az 1–5Móz táblái változatlanok; `git diff f21p/` üres.

## 3. Ellenőrzés a könyvön (`f22_elemzes.py --konyv Józs`)

- **Arányok:** `magas` 0,0% (0/15 023 link; 0/30 405 token), `alacsony` 100%, `kezi` 0 — egy modell fut, nincs egyezés; nem minőségi mutató (mint a 3–5Mózesnél). A „gyanús fejezet” jelzés minden fejezetre ezért formális, nem eltolódás-jel (az eltolódást a detektor adja: a Józsuéra 0).
- **Régi arany:** 5 hármas a könyvben, mind megtalálható; mért érték 100,0% (5/5); nagyon kis minta, nem minősít pontosságot. A `magas` linkekre n.é. (nincs).
- **Eltérés-típusok:** 0 (nincs második modell).
- A zárt összevetés (`zart_osszevet.py --konyv Józs --bemenet <fájl>`) a felhasználóé.

## 4. Nyitott

- A bizonyosság-jelölés a C-futással pótolható (DT-F22c: rossz mérés esetén újranyitható).
- A következő könyv indítása a felhasználó döntése (⛔ 2.). Jób előtt: döntés az 1:2 / 2:1 versösszevonás támogatásáról (34 K-hiány); Ézs 9:17–20 megfeleltetése hamis.
