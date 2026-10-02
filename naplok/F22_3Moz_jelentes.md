# F22_3Moz_jelentes.md — Károli–Strong párosítás: 3Mózes (csak Sonnet)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py`, `sonnet_koteg.py`, `egyesit.py`, `f22_elemzes.py`, `versbeosztas.py`). Ág: `claude/f22-2moz` (PR #114). Módszer: `prompt_v3` változatlanul, Sonnet (`vegrehajto-sonnet` subagentek, kötegenként egy, sorban), **a C (Gemini) kimarad** (felhasználói döntés, DT-F22c nyitva). Munka a külön worktree-ben (`../Bible-Study-f22`).*

## 1. Menet

- **Megfeleltetés:** a 3Móz a `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` listán (2Móz, 3Móz); a detektor szerint a 3Móz tiszta (27 fejezet, 0 jelzett fejezet, 0 eltolt pár, 0 hiány), a lista nem tartalmaz 3Móz-sort, tehát a bemenet a nyers kulcs.
- **Minta:** 859 vers, 86 köteg (10 vers/köteg), `--var 859` egyezik, eredeti nélküli vers nincs.
- **Csak-Sonnet támogatás:** az `egyesit.py` a C-fájl hiányát nem hibának veszi; minden link `alacsony`, `forras: S` (a brief szabálya: egy modell, nincs egyezés); a proveniencia-sor `ts=manual` (nincs C futásnapló, a subagent-futásnak nincs lekérdezés-időbélyege).
- **Hash (K3):** a `prompt_v3` hash-ét a `sonnet_koteg.py prompt` minden köteg előtt ellenőrizte (hiba nélkül), és a menet végén is: `prompt_hash_hiba()` → `None` (nincs eltérés); `git diff f21p/` üres.
- **Keret a /usage szerint** (heti „all models”): a menet elején **52%**, a végén **63%** → **11 százalékpont** (egész százalékos kerekítéssel 10–12) a 859 versre; az 5 órás ablak 10%-ról 100%-ra ment (a menet közben elfogyott, a kimaradt rész után nullázódott). A 30%-os menetkeret alatt maradt. A mért fogyás a menet közbeni más munkát (a session többi része) is tartalmazza, ezért felső becslés.

## 2. Szkriptkimenet

```
Sonnet: 86 köteg, 859 vers; kapuhiba első próbára 0.9% (8/859); végleg 0.0% (0/859)
```

`egyesit.py --konyv 3Móz`: `parok_3Moz.tsv` 18 347 sor (mind `alacsony`, `S`), `szavak_3Moz.tsv` 36 655 sor (mind `alacsony`), átnézési sor 0 vers. `egyesit.py --ellenoriz`: „rendben” (minden Károli- és eredeti token pontosan egyszer; a `strong` a TAHOT-ból levezethető); az újraépítés bájtra azonos. Az 1Móz és a 2Móz táblái változatlanok.

## 3. Amit a szám jelent és amit nem

- A `magas` arány **0%** nem minőségi mutató, hanem a módszer következménye: egy modell, nincs egyezés. Az `f22_elemzes.py` „gyanús fejezetek” sora ezért mind a 27 fejezetet jelzi (a `magas` arány < 70%), ez itt nem eltolódás-jel; az eltolódást a detektor mondja ki (0 jelzés).
- A régi arany (`Karoli_Strong_kivonat.tsv`) a 3Mózesből **0 hármast** tartalmaz, így nincs aranyra mért egyezés; a kereszttábla (DT-F22c) a 3Mózesre nem képezhető (nincs második modell).
- Az eltérés-típusok táblája (4.3) üres: nincs C-oldal.
- **Pontosság nincs mérve.** A Sonnet pilot-pontossága (97,3%, KJV-támponttal, Gen/Exo/Pro) a 3Mózesre nem igazolt; ehhez a felhasználó helyi zárt összevetése kell (`zart_osszevet.py --konyv 3Móz --bemenet <fájl>`; a kimenet csak összesített szám, a `magas` sor üres, mert nincs `magas` link).

## 4. Nyitott

1. A 3Móz csak-Sonnet jellege: a bizonyosság-jelölés (`magas`) a későbbi C-futással pótolható (a C-futás a `f22/futtatas.txt` triggerrel indítható, a kész kötegeket kihagyja); ez a DT-F22c döntésén múlik.
2. A következő könyv előtt a jelzett fejezetek kézi jóváhagyása (első: **4Móz 30**); az **Ézs 9:17–20** megfeleltetése hamis (a lista más könyvekre javaslat, a futtató csak a jóváhagyott könyvekre alkalmazza).
3. Az ellenőri kör: `naplok/ELLENOR_F22_3Moz.md`.
