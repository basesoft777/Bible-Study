# KAROLI_KULCS_KK75_BRIEF.md — KK7.5: az 1Sám 20/21 határának javítása, utána merge

*v1 — 2026.09.25 · jóváhagyásra: a §2 G-döntései · a KK7 független ellenőrzéséből (`d9056a5`)*

**Cél.** A KK7 után egyetlen ismert hibás hozzárendelés maradt, a „hibás helyett üres” szabály
(KK7 G1) sérül. A menet ezt adatvezérelten javítja, és a teljes korpuszon megnézi, van-e még
ilyen eset. Utána, a jóváhagyásod után, a KK-ág a `main`-be kerül.

**Előfeltétel:** nincs. **Futás:** cloud, ugyanazon az ágon: `claude/karoli-kulcs-35158`.
**Modell:** Sonnet. **Push:** csak erre az ágra; a `main`-re csak a §7 merge-prompt után.

**Nincs benne:** a `ts=` soronkénti churn megszüntetése (külön NYITOTT-tétel); a törzscikkek
regenerálása; a KK7 döntéseinek újranyitása.

---

## 0. Kiindulás *(független ellenőrzés a `d9056a5` tarballján; a KK7.5.0 újraméri)*

| LXX-vers | Görög szöveg (eleje) | Most | Helyesen |
|---|---|---|---|
| 1Sám 20:41 | καὶ ὡς εἰσῆλθεν τὸ παιδάριον | `1Sám 20:41` | `1Sám 20:41` ✓ |
| 1Sám 20:42 | καὶ εἶπεν Ιωναθαν πορεύου εἰς εἰρήνην | üres (`szamozas_elteres`) | `1Sám 20:42` |
| 1Sám 21:1 | καὶ ἀνέστη Δαυιδ καὶ ἀπῆλθεν | **`1Sám 20:42` — hibás** | `1Sám 20:43` |
| 1Sám 21:2 | καὶ ἔρχεται Δαυιδ εἰς Νομβα | `1Sám 21:1` ✓ | `1Sám 21:1` |

A Károli a fejezet zárómondatát külön versként (20:43) számozza. A döntéstábla
(`naplok/KAROLI_KK7_fejezet_dontes.tsv`) az 1Sám 20-ra `elfogad`, `-1` korrekciót ad, ez a
fejezethatáron átnyúló versre rossz célt eredményez. Motívum-igehelyet nem érint.

---

## 1. Mércék

- A 0. pont négy verse a „Helyesen” oszlop szerint áll.
- **Korpuszszintű keresés** (fájlba írt szkript): minden, a KK során újonnan kitöltött kulcsra
  (a) két különböző LXX-vers ugyanarra a Károli-versre mutat; (b) a hozzárendelés fejezethatárt
  lép át; (c) egy elfogadott fejezetben Károli-vers marad ki a sorozatból. Minden találat
  vagy javítva a 2. pont szerint, vagy üresre állítva, indokkal.
- Nem-regresszió: a KK előtt kitöltött 460 808 szósor kulcsa változatlan; a KK7 10 419 új
  kulcsa közül csak a §1 találatai változnak.
- Próbakő: az Ézs 63:13 továbbra is „egyező”; a lexikon-fixpont (8 motívum, `--id`-vel) 0 eltérés.

---

## 2. G-döntések

| # | Döntés |
|---|---|
| G1 | A javítás adatvezérelt: új versszintű felülbírálási tábla (`lxx_igehely` → `karoli_igehely`, `indok`), amelyet az importer a fejezetdöntés **előtt** alkalmaz. Kódban könyv- vagy versspecifikus ág nincs. |
| G2 | Az importer éles bemenetei kikerülnek a `naplok/` alól: a KK7 fejezetdöntés-táblája és az új felülbírálási tábla a `konkordancia/LXX_OS/` alá kerül (`karoli_fejezet_dontes.tsv`, `karoli_vers_felulbiralas.tsv`), generált-fejléccel és forrásmegjelöléssel. A `naplok/KAROLI_KK7_fejezet_dontes.tsv` naplóként marad. |
| G3 | Amit a §1 keresése talál, de a helyes cél nem bizonyítható a görög és a Károli-szöveg összevetésével, az üres lesz (KK7 G1). |
| G4 | Közös fájlt a menet nem ír; a jelentés a saját ágán marad. |

---

## 3. Tételek

- **KK7.5.0 — Kiindulás.** A §0 újramérése. `naplok/KAROLI_KK75_kiindulas.md`.
- **KK7.5.1 — Korpuszszintű keresés.** A §1 (a)–(c) keresése →
  `naplok/KAROLI_KK75_hatarkereses.tsv` (LXX-vers, most, javasolt, típus, bizonyíték).
- **KK7.5.2 — Javítás.** A G1 táblája, a G2 áthelyezés, az importer módosítása; újragenerálás
  (`lxx_os_import.py`, ugyanazzal a helyi lxx-morph klónnal és sha256-igazolással, mint a KK5-ben),
  majd `general.py --cel lexikon --id X --ir` a 8 motívumra.
- **KK7.5.3 — Újramérés és jelentés ⛔.** A §1 mércéi; a lexikon Egyezés-bontása előtte–utána.
  `naplok/KAROLI_KK75_jelentes.md`. Push az ágra. ÁLLJ, jelentés a chatbe.

Commit tételenként: `KK7.5.<n>: <rövid leírás>`.

---

## 4. Elfogadási feltételek

| # | Feltétel |
|---|---|
| K1 | a KK előtti 460 808 kulcs változatlan; 0 eltűnt sor |
| K2 | a §0 négy verse helyes; a §1 keresése után 0 nyitott (a)/(b)/(c) találat |
| K3 | az importer nem olvas a `naplok/` alól (grep) |
| K4 | az Ézs 63:13 „egyező”; a lexikon-fixpont 8/8 motívumon 0 eltérés |
| K5 | `ellenoriz.py`: RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2 |
| K6 | nincs `csv` modul; héber/görög szöveg csak fájlba írt szkriptből (CLAUDE.md, Shell) |

---

## 5. Döntésnapló

| Verzió | Dátum | Változás |
|---|---|---|
| v1 | 2026.09.25 | Az 1Sám 20:42 / 21:1 hiba javítása versszintű felülbírálási táblával (G1), korpuszszintű határkereséssel (§1); az importer éles bemenetei a `konkordancia/LXX_OS/` alá (G2). |

---

## 6. Nyitó prompt — KK7.5 (a futó cloud sessionbe, a `claude/karoli-kulcs-35158` ágon; a briefet csatold)

```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
(elvárt: claude/karoli-kulcs-35158, d9056a5)
1. A csatolt KAROLI_KULCS_KK75_BRIEF.md-t mentsd a repó gyökerébe, változtatás nélkül.
   Commit: "KK7.5: KAROLI_KULCS_KK75_BRIEF.md v1".
2. Hajtsd végre a KK7.5.0–KK7.5.3 tételeket a brief §3 szerint, a §1 mércéivel és a §2 döntéseivel.
   Tételenként külön commit.
3. A végén ellenőrizd a §4 K1–K6-ot, és pushold az ágat. A main-re ne pushold.
ÁLLJ a KK7.5.3 után: jelentés a chatbe (commitlista, a határkeresés találatai, K1–K6).
```

## 7. Merge-prompt (csak a KK7.5 független ellenőrzése és a jóváhagyásod után)

```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
1. git fetch origin; git checkout main; git pull --ff-only origin main
2. git merge --no-ff origin/claude/karoli-kulcs-35158 -m "Merge: KAROLI_KULCS (KK0–KK7.5) — Károli-versmegfeleltetés és LXX_OS-újragenerálás"
   Ütközésnél ÁLLJ, ne oldd fel magadtól: jelentsd a fájlokat.
3. Ellenőrzés a merge után: eszkozok/ellenoriz.py (RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2);
   general.py --cel lexikon --id X --ellenoriz a 8 motívumra (0 eltérés).
4. git push origin main. Jelentés: a merge-commit hash-e és a két ellenőrzés eredménye.
```
