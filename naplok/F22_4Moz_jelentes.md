# F22_4Moz_jelentes.md — Károli–Strong párosítás: 4Mózes (csak Sonnet)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py`, `sonnet_koteg.py`, `egyesit.py`, `f22_elemzes.py`, `versbeosztas.py`) és a menet végi ellenőrző szkriptből (l. 3.). Ág: `claude/f22-4moz` (a PR #114 ágára épül: a 4Móz-menet eszközei — detektor, megfeleltetés, csak-Sonnet ág — még nincsenek a `main`-en). Módszer: `prompt_v3` változatlanul, Sonnet (`vegrehajto-sonnet` subagentek, kötegenként egy, sorban), **a C (Gemini) kimarad** (DT-F22c nyitva). Munka a külön worktree-ben (`../Bible-Study-f22`).*

## 1. Menet

- **Kézi jóváhagyás (2026.10.02, chat), a jóváhagyási naplóban** (`naplok/F22_versbeosztas_jovahagyas.md`): a 4Móz 30 lista helyes (Károli 30:n → TAHOT 30:(n+1), n = 1–16); a TAHOT 30:1 tartalma a Károli 29:39 utolsó mondata (beolvasztás, 1:2). 1:2 támogatás a párosításban nincs, ezért a TAHOT 30:1 és a Károli 29:39 utolsó mondatának szavai (hu 25–38) **`kezi`**, nem `betoldas`, hivatkozással a TAHOT 30:1-re.
- **Megvalósítás:** a 4Móz a `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` listán (2Móz, 3Móz, 4Móz; a 4Mózesre csak a lista 30. fejezeti sorai érvényesek); a kézi beolvasztás az `f22/versosszevonas.tsv`-ben (kézzel írt, a detektor nem írja felül); a `tokenek._versmegfeleltet` a TAHOT 30:1-et nem teszi gazdátlanná (nincs `4Móz 30:1001` ál-azonosító); az egyesítő a 29:39 hu 25–38 és a TAHOT 30:1 tokenjeit `kezi`-ben viszi (az `er` sorok a 29:39 saját eredeti szavai (1–30) után 31–43 sorszámmal), a modell-válaszból a 25–38 tokenek linkjeit kiszűri; átnézési sor hivatkozással.
- **Minta:** 1 287 vers, 129 köteg (10 vers/köteg), `--var 1287` egyezik; a megfeleltetés után eredeti nélküli Károli-vers nincs.
- **Hash (K3):** a `prompt_v3` hash-ét a `sonnet_koteg.py prompt` minden köteg előtt ellenőrizte (hiba nélkül); `git diff f21p/` üres.
- **Keret a /usage szerint** (heti „all models”): a menet elején **65%**, a végén **74%** → **9 százalékpont** (egész százalékos kerekítéssel 8–10) az 1 287 versre; **az 85%-os megállási küszöböt nem érte el**, a menet nem szakadt meg. A fogyás a session közbeni más munkát is tartalmazza (felső becslés). Az 5 órás ablak a menet alatt 16%-ról 92%-ra ment.

## 2. Szkriptkimenet

```
Sonnet: 129 köteg, 1287 vers; kapuhiba első próbára 0.9% (12/1287); végleg 0.0% (0/1287)
```

`egyesit.py --konyv 4Móz`: `parok_4Moz.tsv` 24 695 sor (mind `alacsony`, `S`), `szavak_4Moz.tsv` 49 211 sor (alacsony 49 184, `kezi` 27: 14 hu + 13 er), átnézési sor 1 vers (4Móz 29:39, hivatkozással a TAHOT 30:1-re). `egyesit.py --ellenoriz`: „rendben” (minden Károli- és eredeti token — a beolvasztott TAHOT 30:1 tokenjeit is beleértve — pontosan egyszer szerepel, a `strong` a TAHOT-ból levezethető); az újraépítés bájtra azonos. Az 1–3Móz táblái változatlanok.

## 3. A négy kért ellenőrzés (szkriptkimenet)

| # | ellenőrzés | eredmény |
|---|---|---|
| 1 | a 30. fejezet minden verse a megfeleltetett TAHOT-verssel párosodott | **igen**, mind a 16 vers: a Károli 30:n bemeneti eredeti szavai megegyeznek a TAHOT 30:(n+1) szavaival, az `er` sorok száma egyezik, minden versben van párosított hu-token (15, 24, 15, … db), `kezi` a 30. fejezetben 0 |
| 2 | a 29:39 vége `kezi`, nem `betoldas` | **igen**: hu 25–38 (14 sor) mind `fuggoben` / `kezi`, `betoldas` 0, a `parok` táblában 0 sor a 29:39 hu ≥ 25 tokenjeire; a hu 1–24: 17 `parositva`, 7 `betoldas` (a vers többi része normálisan párosított); az `er` 31–43 (13 sor = a TAHOT 30:1 tokenjei) `fuggoben` / `kezi`, a strongjaik a TAHOT 30:1-ével egyeznek |
| 3 | nincs 30:1001 ál-azonosító | **igen**: a `4Móz 30:1001` nem fordul elő sem a 4Móz-táblákban, sem a jsonl-ben, sem a mintában, sem az átnézési fájlban, és az `ered` kulcsai között sincs |
| 4 | a jóváhagyás naplózva | `naplok/F22_versbeosztas_jovahagyas.md` (4Móz 30 sor, a Jób függő pontja is) |

## 4. A számok jelentése és nyitott kérdések

- A `magas` arány **0%**: egy modell fut, nincs egyezés; nem minőségi mutató (a 3Mózeshez hasonlóan). Az `f22_elemzes.py` „gyanús fejezet” sora ezért minden fejezetet jelez (nem eltolódás-jel; az eltolódást a detektor adja: a 4Mózesre 1 jelzett fejezet, a 30., kezelve).
- A régi arany a 4Mózesre 3 hármast ad, mindhárom egyezik (100,0%, 3/3); ez nagyon kis minta, és a 3Mózeshez hasonlóan nem minősít pontosságot. A zárt összevetés (`zart_osszevet.py --konyv 4Móz --bemenet <fájl>`) a felhasználóé.
- **Nyitott:** a bizonyosság-jelölés a C-futással pótolható (DT-F22c); **1:2 / 2:1 versösszevonás támogatásáról döntés a Jób jóváhagyása előtt (34 K-hiány)**; következő könyv előtt a jelzett fejezetek kézi jóváhagyása; Ézs 9:17–20 megfeleltetése hamis.
- **PR:** draft, a #114 ágára épül (base: `claude/f22-2moz`), mert a `main` még nem tartalmazza a #114 eszközeit; a #114 merge-e után a PR a `main`-re állítható.
