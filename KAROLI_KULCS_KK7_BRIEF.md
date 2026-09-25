# KAROLI_KULCS_KK7_BRIEF.md — Károli-kulcs javító menet: tartalmi próba, a H2-eltolás hibájának javítása

*v1 — 2026.09.25 · a `claude/karoli-kulcs-35158` ág (`bcd88e9`, KK4–KK6) chat-ellenőrzése után ·
jóváhagyásra: a §0 számai és a §2 G-döntései*

**Cél.** A KK4–KK5 által **újonnan** kitöltött Károli-kulcsok egy része egy verssel el van
csúszva. A menet (1) tartalmi próbát épít és lefuttat minden újonnan kitöltött fejezetre,
(2) kijavítja a hibás eltolás okát az importerben, adatvezérelt fejezetdöntésekkel,
(3) újragenerál és újramér. **Alapszabály: az üres kulcs jobb, mint a hibás.**

**Előfeltétel:** nincs. A KK-ágon folytatódik.

**Futás: cloud** (a kreditből), ugyanazon az ágon: `claude/karoli-kulcs-35158`.
**Modell:** Sonnet. **Push:** csak erre az ágra; a `main`-re soha.

**Nincs benne:** a törzscikkek regenerálása (a `main`-en is elavultak, a NYITOTT 5b tétele, a
SZOTAR 2. menete hozza helyre); a 87 függő LXX-hely eldöntése; közös fájl írása
(`NYITOTT_FELADATOK.md`, changelogok, más briefek).

---

## 0. Kiindulás *(chat-ellenőrzés a `bcd88e9` tarballján, 2026.09.25; a KK7.0 újraméri)*

| # | Mérés | Érték |
|---|---|---|
| 0.1 | Ág HEAD / `main` HEAD | `bcd88e9` / `72b200c` (az FJ merge-e) |
| 0.2 | `LXX_OS` szósorok a KK előtti állapothoz (`a6783e4`) képest | korábban kitöltött és változatlan 460 808 · **megváltozott 0** · újonnan kitöltött **14 198** · üres maradt 141 867 · eltűnt 0 |
| 0.3 | Lexikon „Egyezés” a KK6 után | egyező 127 · függőben 89 · szamozas_elteres 9 · eltérő 3 · nincs LXX_OS-könyv 5 · LXX-minusz 1 |
| 0.4 | Tartalmi próba (chat): az újonnan kitöltött, mérhető fejezetek | 27 fejezet; **10-ben a ±1 versre tolt megfeleltetés illeszkedik jobban** |
| 0.5 | A 10 gyanús fejezet (erős jel: r(választott) ≈ 0 vagy negatív, r(−1) ≥ 0,74) | 4Móz 6 · 1Kir 22 · Józs 10 · Józs 13 · 1Sám 18 · 1Sám 20 · Ézs 56 · Ézs 63; gyenge jel: 1Sám 17, Jer 48 |
| 0.6 | Szövegszintű megerősítés | LXX Ézs 63:1 (τίς οὗτος ὁ παραγινόμενος ἐξ Εδωμ) → Károli 63:2 a helyes 63:1 helyett; LXX Ézs 63:12 (Mózes jobbja) → Károli 63:13; LXX 4Móz 6:4 (a szőlőtő terméke) → Károli 6:5; LXX 1Sám 20:8 → Károli 20:9 |
| 0.7 | A kulcstábla ezeken a helyeken | **identitás** (`Ézs 63:1 ↔ 63:1`, `4Móz 6:4 ↔ 6:4`, `1Sám 20:8 ↔ 20:8`) — a hiba nem a táblában, hanem az importer láncában van |
| 0.8 | `eszkozok/ellenoriz.py` | az ágon RENDBEN 9 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2; a `main`-en (`72b200c`) RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2 |

**A hiba valószínű oka (a KK7.2 igazolja vagy cáfolja).** A `resolve_karoli` H2-ága a fejezet
hosszkülönbségéből (`d = karoli_max − kjv_max`) **egyenletes** eltolást alkalmaz a fejezet
minden versére (`uj_vers = kjv_v + d`). Ez csak akkor helyes, ha a többletvers a fejezet
**elején** van (ilyen a zsoltárcím). Ha a többlet a fejezet **végén** vagy **közepén** van,
az eltolás a fejezet minden versét elcsúsztatja. Példa: a Károli 1Sám 20:43 a KJV 20:42
második fele (és az LXX 21:1), vagyis a többlet a fejezet végén van, a 20:1–42 identitás.

**Próbakő:** az Ézs 63:13 (TEREMT-001, *tehóm* / ἄβυσσος) a KK6 után „függőben” lett, pedig
helyes kulccsal „egyező”: az LXX 63:13-ban ott a διὰ τῆς ἀβύσσου.

---

## 1. Mércék

**Tartalmi próba (fejezetenként).** Minden fejezetre, amelyben van újonnan kitöltött kulcs:
- A választott megfeleltetésre és a ±1, ±2 versre tolt változatra kiszámolod a Pearson-
  korrelációt az LXX-vers szószáma és a hozzárendelt Károli-vers szószáma között
  (`LXX_OS` szósorok száma versenként ↔ `Karoli_1908.tsv` szavainak száma).
- **Elfogadás:** a választott megfeleltetés korrelációja a legnagyobb, legalább **0,60**, és
  legalább **0,15**-tel nagyobb a következő legjobbnál.
- **Tulajdonnév-horgony:** ahol van (TIPNR-név a TAHOT-versben és a névalak a Károli-versben,
  a KK1b-4 mintájára), ott ellentmondás esetén a horgony dönt.
- **Nem mérhető fejezet** (kevesebb mint 4 vers, vagy nincs meg minden eltolt vers): csak
  akkor fogadható el, ha a horgony megerősíti; különben üres.

**Nem-regresszió:** a KK előtt kitöltött 460 808 szósor Károli-kulcsa változatlan marad (0.2).

---

## 2. G-döntések

| # | Döntés |
|---|---|
| G1 | **Üres jobb, mint hibás.** Ha egy fejezet nem megy át a §1 próbáján, az újonnan kitöltött kulcsai visszaállnak üresre, `karoli_ok=szamozas_elteres` jelöléssel. |
| G2 | A javítás **adatvezérelt**: a fejezetdöntések (könyv, fejezet, elfogadott eltolás vagy „üres”, a korrelációk, a horgony) generált táblába kerülnek, és az importer ezt olvassa. Heurisztikus új ág a `resolve_karoli`-ban nem elég. |
| G3 | A KK7.0 először a `main`-t (`72b200c`) mergeli az ágba, hogy a végső újragenerálás a `main` mai adatán fusson (a TEREMT-002 adatai is ott vannak). Ütközés nem várható, mert a két oldal nem érint közös fájlt. |
| G4 | A KK6 „javult” besorolásai (Jób 38:16, 38:30, Jón 2:3, 2:6) is átmennek a tartalmi próbán; ami nem megy át, az is G1 szerint üres lesz. |
| G5 | A K-feltételek állapota csak RENDBEN vagy NEM TELJESÜL lehet (a KAROLI_KULCS_BRIEF G11-e). |

---

## 3. Tételek

- **KK7.0 — Kiindulás és a `main` beolvasztása.** `pwd`, ág, HEAD. `git merge origin/main`
  (G3); ütközésnél ÁLLJ. A §0 újramérése a merge után; az `ellenoriz.py` elvárt értéke a
  merge után a `main`-é (RENDBEN 10 · SÉRTÉS 0 · KÉZI 2 · JELENTÉS 2).

- **KK7.1 — Tartalmi próba.** `naplok/KAROLI_KK7_tartalmi_proba.py`: az összes újonnan
  kitöltött fejezetre a §1 szerint. Kimenet: `naplok/KAROLI_KK7_fejezet_dontes.tsv`
  (könyv, fejezet, választott eltolás, r(−2…+2), horgony, döntés: elfogad / üres), és
  összesítő a jelentésbe: hány fejezet ment át, hány lett üres, és mennyi szósor érintett.

- **KK7.2 — Az ok igazolása és a javítás.** A 0.6 négy példáján lépésenként mutasd meg, melyik
  ág adja a hibás célt (a fenti hipotézis megerősítése vagy cáfolata). Utána a G2 szerint:
  az importer a KK7.1 döntéstábláját olvassa, a H2-eltolást csak az elfogadott fejezetekben és
  csak az elfogadott eltolással alkalmazza, a többi újonnan kitöltött helyet üresen hagyja.

- **KK7.3 — Újragenerálás.** `lxx_os_import.py` a rögzített lxx-morph commiton (ugyanaz, mint
  a KK5-ben), majd `general.py --cel lexikon --ir`.

- **KK7.4 — Újramérés és jelentés ⛔.**
  - a 0.2 újra: a KK előtti 460 808 kitöltött szósor változatlan;
  - a KK7.1 tartalmi próba újrafuttatva az új állapoton: minden kitöltött új fejezet átmegy;
  - a 0.6 négy példája szövegszinten helyes (vagy üres);
  - az Ézs 63:13 „egyező” (a próbakő);
  - a lexikon „Egyezés”-bontása a KK6 után és most;
  - `general.py --cel lexikon --ellenoriz`: 0 eltérés; `ellenoriz.py`: SÉRTÉS 0.
  `naplok/KAROLI_KK7_jelentes.md`. **ÁLLJ, jelentés a chatbe.**

Commit tételenként: `KK7.<n>: <rövid leírás>`.

---

## 4. Elfogadási feltételek

| # | Feltétel |
|---|---|
| K1 | a KK előtt kitöltött 460 808 szósor kulcsa változatlan; 0 eltűnt sor |
| K2 | minden megmaradt új kulcs olyan fejezetben van, amely átment a §1 próbáján |
| K3 | a 0.6 négy példája helyes vagy üres, egyik sem hibás |
| K4 | az Ézs 63:13 „egyező” |
| K5 | `general.py --cel lexikon --ellenoriz`: 0 eltérés |
| K6 | `ellenoriz.py`: SÉRTÉS 0 |
| K7 | a fejezetdöntések generált táblában, az importer azt olvassa (G2); minden szám szkriptből |
| K8 | `git diff --stat origin/main..HEAD`: csak a KK hatóköre (brief, `eszkozok/lxx_os_import.py`, `konkordancia/Karoli_versmegfeleltetes.tsv`, `konkordancia/LXX_OS/*`, a döntéstábla, `lexikon/*_TUDOMANYOS.md`, `naplok/KAROLI_*`) |

---

## 5. Döntésnapló

| Verzió | Dátum | Változás |
|---|---|---|
| v1 | 2026.09.25 | A KK4–KK6 chat-ellenőrzése után: a régi kulcsokban nincs regresszió, de az új kulcsok egy része egy verssel elcsúszott (10/27 mérhető fejezet, négy szövegszintű példa). Tartalmi próba, adatvezérelt fejezetdöntés, „üres jobb, mint hibás”; a `main` beolvasztása az újragenerálás előtt; az Ézs 63:13 mint próbakő. |

---

## 6. Nyitó prompt (cloud session a `claude/karoli-kulcs-35158` ágon; a briefet csatold)

```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
Olvasd el a CLAUDE.md-t és a csatolt KAROLI_KULCS_KK7_BRIEF.md-t.
1. A briefet mentsd a repó gyökerébe, változtatás nélkül. Commit: "KK7: KAROLI_KULCS_KK7_BRIEF.md v1".
2. Hajtsd végre a KK7.0–KK7.4 tételeket a brief §3 szerint, a §1 mércéivel és a §2 döntéseivel.
   Tételenként külön commit, push csak a claude/karoli-kulcs-35158 ágra. A main-re ne pushold.
ÁLLJ a KK7.4 után: jelentés a chatbe (commitlista, a K1–K8 állapota, az Egyezés-bontás előtte/utána,
a fejezetdöntések összesítője).
```
