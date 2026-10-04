# F22_5Moz_jelentes.md — Károli–Strong párosítás: 5Mózes (csak Sonnet)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py`, `sonnet_koteg.py`, `egyesit.py`, `f22_elemzes.py`, `versbeosztas.py`, `get_usage`). Ág: `claude/f22-5moz` (a `claude/f22-4moz` ágra épül, mert a #131 még nincs a `main`-en). Módszer: `prompt_v3` változatlanul, Sonnet (`vegrehajto-sonnet` subagentek, kötegenként egy, sorban), **a C (Gemini) kimarad** (DT-F22c: lezárva, rossz mérés esetén újranyitható). Munka a külön worktree-ben (`../Bible-Study-f22`).*

## 1. Menet

- **Jóváhagyás (2026.10.02, chat: „5Mózes mehet”)**, a jóváhagyási naplóban (`naplok/F22_versbeosztas_jovahagyas.md`): a detektor szerint az 5Móz tiszta (`naplok/F22_versbeosztas.md`: 959 Károli-vers, 959 eredeti vers, 34 fejezet, eltolt/K-hiány/E-hiány 0), a listában nincs sora; a `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve. Kézi 1:2 beolvasztás **nincs**.
- **Minta:** 959 vers, 96 köteg (10 vers/köteg, az utolsó 9), `--var 959` egyezik; eredeti nélküli Károli-vers nincs.
- **Hash (K3):** a `prompt_v3` hash-ét a `sonnet_koteg.py prompt` minden köteg előtt ellenőrizte (hiba nélkül).
- **Keret a `get_usage` szerint** (heti „all models”): a menet elején **76%**, a végén **84%** → **8 százalékpont** a 959 versre. Az **85%-os megállási küszöböt nem érte el**, a menet nem szakadt meg. **A 70%-os indítási feltételt (a #22-jegyzet) a menet elején megsértette** (76%), a felhasználó tudatosan jóváhagyta („1”). A fogyás a session közbeni más munkát is tartalmazza (felső becslés). Az 5 órás ablak 9%-ról 74%-ra ment.

## 2. Szkriptkimenet

```
Sonnet: 96 köteg, 959 vers; kapuhiba első próbára 1.4% (13/959); végleg 0.0% (0/959)
C: 0 köteg, 0 vers
```

`egyesit.py --konyv 5Móz`: `parok_5Moz.tsv` 23 392 sor (mind `alacsony`, `S`), `szavak_5Moz.tsv` 45 447 sor (mind `alacsony`), átnézési sor 0 vers. `egyesit.py --ellenoriz`: „rendben” (minden Károli- és eredeti token pontosan egyszer szerepel, a `strong` a TAHOT-ból levezethető); az újraépítés bájtra azonos (a két tábla SHA-256-ja egyezik). Az 1–4Móz táblái változatlanok; `git diff f21p/` üres.

## 3. Ellenőrzés a könyvön (`f22_elemzes.py --konyv 5Móz`)

- **Arányok:** `magas` 0,0% (0/23 392 link; 0/45 447 token), `alacsony` 100%, `kezi` 0 — egy modell fut, nincs egyezés; nem minőségi mutató (mint a 3–4Mózesnél). A „gyanús fejezet” jelzés minden fejezetre ezért formális, nem eltolódás-jel (az eltolódást a detektor adja: az 5Mózesre 0).
- **Régi arany:** 7 hármas a könyvben, mind megtalálható; mért érték 100,0% (7/7); nagyon kis minta, nem minősít pontosságot. A `magas` linkekre n.é. (nincs).
- **Eltérés-típusok:** 0 (nincs második modell).
- A zárt összevetés (`zart_osszevet.py --konyv 5Móz --bemenet <fájl>`) a felhasználóé.

## 4. Nyitott

- A bizonyosság-jelölés a C-futással pótolható (DT-F22c: rossz mérés esetén újranyitható).
- 1:2 / 2:1 versösszevonás támogatásáról döntés a Jób jóváhagyása előtt (34 K-hiány); a jelzett fejezetek kézi jóváhagyása könyvenként; Ézs 9:17–20 megfeleltetése hamis.
- ~~**PR:** a `claude/f22-5moz` ág a `claude/f22-4moz`-ra épül (a #131 ágára); a PR a #114 és a #131 merge-e után a `main`-re állítható. Push és PR **nem készült** (a felhasználó kérésére marad).~~ *Lezárva (2026.10.04):* a 4–5Móz a PR #139-cel a `main`-ben; a merge előtt elmaradt független ellenőri kör utólag pótolva (`naplok/ELLENOR_F22_5Moz.md`, `claude/f22-5moz-ellenor`, PR #160).
