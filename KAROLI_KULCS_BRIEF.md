# KAROLI_KULCS_BRIEF.md — Károli-versmegfeleltetés: a `szamozas_elteres` valódi oka és javítása

*v1 — 2026.09.25 · jóváhagyásra: a §0 számai és a §2 G-döntései · a FORRASJELOLTEK 1. menetének
(FJ2) felülvizsgálatából*

**Cél.** A `konkordancia/LXX_OS/*.tsv` `igehely_karoli` oszlopa 20 346 szósorban (≈1 000 versben)
üres, `karoli_ok=szamozas_elteres` címkével; ebből ered a 8 lexikonoldal 15 `szamozas_elteres`
sora. A menet (1) okonként besorolja az üres sorokat, (2) Károli-kulcsú versmegfeleltető táblát
készít a KJV- és az MT-számozáshoz, (3) jóváhagyás után javítja az importert, újragenerál és újramér.

**Előfeltétel:** nincs. A `main`-ről indul; a `claude/peaceful-rubin-39uuzs` (FORRASJELOLTEK
1. menet) ágat nem érinti és nem vár rá.

**Futás: cloud.** **Modell:** Sonnet; a KK2 kézi fejezeteihez Opus, ha a „egyik sem” osztály
10 fejezetnél több. **Push:** csak a saját ágra, tételenként; a `main`-re soha.

**Szerkezet.** 1. menet: KK0–KK3, mérés és táblatervezet ⛔ → jóváhagyás után 2. menet:
KK4–KK6, élesítés és újragenerálás ⛔.

**Nincs benne:** a lexikon 3. szakaszának kézi szerkesztése (generált réteg); a 87 függő hely
eldöntése (`LEXIKON_LEZARAS_BRIEF.md` 4c); a teljes KJV/ASV-import (külön brief); közös fájl
írása (`NYITOTT_FELADATOK.md`, changelogok, más briefek).

---

## 0. Kiindulás *(chat-mérés a `claude/peaceful-rubin-39uuzs` tarballján, 2026.09.25; a KK0 a `main`-en újraméri, eltérésnél jelentsd és folytasd)*

| # | Mérés | Érték |
|---|---|---|
| 0.1 | `LXX_OS/*.tsv`, `karoli_ok` szósor-szinten | üres (kitöltött) 441 718 · `nincs_karoli_konyv` 133 229 · `szamozas_elteres` 20 346 · `zsolt_felirat_eltolas` 14 065 · `kezi_eltolas_tabla` 5 025 · `nincs_mt_parositas` 2 490 |
| 0.2 | `szamozas_elteres` versszinten | 1 015 LXX-vers, 112 fejezet, 16 fájl; ebből `psalms-lxx.tsv` 63 fejezet |
| 0.3 | A lexikon 15 `szamozas_elteres` sora | l. FJ2 tábla: Jób 17:13, 17:16, 38:7, 38:16, 38:30 · Józs 12:4, 13:12, 15:8, 17:15, 18:16 · Hós 13:14 · Ézs 63:13 · Jón 2:3, 2:6 · Jer 51:46 |
| 0.4 | `job-lxx.tsv`, `joshua-vaticanus-b.tsv` fejezetei | 42/42 és 24/24 megvan — **nincs hiányzó fejezet** |
| 0.5 | `KEZI_ELTOLASOK['Job']` (`lxx_kivonat_fetch_v2.py`) | `job_38_41_eltolas(38, 1..38)` → `None`; `(38, 39)` → `(39, 1)` |
| 0.6 | `job-lxx.tsv` `szamozas_elteres` fejezetei | 38: 431 · 37: 289 · 17: 176 szósor |
| 0.7 | Károli–KJV versszám, mintafejezetek | Jób 17: 15/16 · Jób 37: 23/24 · Jób 38: 38/41 · Jón 2: 11/10 · Hós 13: 15/16 · Ézs 64: 11/12 |
| 0.8 | Tartalmi kontroll | Károli Jón 2:3 („a Seol”) = LXX 2:3 = KJV 2:2 · Károli Jób 17:10 („Napjaim elmulának”) = KJV 17:11 |
| 0.9 | `eszkozok/ellenoriz.py` | RENDBEN 9 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2 (FORRASJELOLTEK §0.7) |

**Munkahipotézisek (a KK1 igazolja vagy cáfolja, soronként):**
- **H1 — importer-hiba.** Ahol a kézi eltolásfüggvény a változatlan szakaszra `None`-t ad,
  a `resolve_karoli` továbblép a fejezetszintű versszám-őrre, az pedig elutasítja az egész
  fejezetet (Jób 38:1–38; valószínűleg a többi `KEZI_ELTOLASOK`-fejezet is).
- **H2 — a Károli több könyvben az MT-számozást követi**, nem a KJV-t (Jónás, Hóseás 13–14,
  valószínűleg Joel, Malakiás, Ézs 63–64). Ezt a mai algoritmus nem ismeri.
- **H3 — valódi Károli-sajátosság** (sem KJV, sem MT): pl. Jób 17, Jób 37.
- **H4 — lexikonoldali kiválasztás.** A Józs-soroknál a lexikon a rövid A-szöveget
  (`joshua.tsv`, 3 fejezet) nézheti a B-szöveg helyett; a `joshua-vaticanus-b.tsv`-ben
  a Józs 12:4, 15:8, 17:15, 18:16 Károli-igehelye ki van töltve.
- **H5 — valódi LXX-eltérés:** Jer 51:46 (a LXX Jeremiás más fejezetrendje).

**Az FJ2 három megállapítása ennek alapján nem tartható** (a KK1 dönt): a „hiányzó fejezetek”
(0.4); a Jón 2:3 → LXX 2:4 javaslat (0.8 szerint a Károli 2:3 az LXX 2:3); és a „Károli-kulcsú
tábla nem szükséges” következtetés, amely csak 1Móz, 2Móz, Péld könyvekre támaszkodott (0.2).

---

## 1. Mércék

- **Fejezetosztály (KK1):** minden ószövetségi Károli-fejezet pontosan egy osztályba kerül:
  `KJV` (versszám és kezdő-/zárósor egyezik a KJV-vel) · `MT` (egyezik a TAHOT-tal) ·
  `KEZI` (van `KEZI_ELTOLASOK`-függvény) · `EGYIK_SEM`.
- **Tartalmi próba:** a `KJV`/`MT` osztályú fejezetek 10%-os véletlen mintáján (seed rögzítve,
  fejezetenként az első és az utolsó vers) a Károli-vers és a jelölt KJV/MT-vers tulajdonnév-
  vagy számnév-horgonya egyezik; minta-egyezés < 98% → az osztályozás nem fogadható el.
- **A kulcstábla érvényessége (KK3):** minden érintett Károli-vers legfeljebb egy sorban
  szerepel; fejezeten belül monoton; az MT-oldal a TAHOT-ban, a KJV-oldal a `verse_pairs.jsonl`
  `mt_refs`-ében létezik; minden sor forrása megnevezve (`tvtms` · `kezi` · `szamlalas`).
- **Siker (KK6):** a `szamozas_elteres` szósorok száma a 0.1-hez képest legalább 90%-kal
  csökken; a lexikon 15 sorából mindegyik új besorolást kap indokkal.

Szám csak lefuttatott, fájlba írt szkriptből jöhet; a szkript neve a munkalap fejlécében.

---

## 2. G-döntések

| # | Döntés |
|---|---|
| G1 | Az 1. menet csak `naplok/KAROLI_KK*` fájlokba és a `konkordancia/_nyers/` (gitignore) alá ír. |
| G2 | Az MT↔angol kulcs forrása a STEPBible TVTMS (`STEPBible-Data`, commit rögzítve); a verse_pairs.jsonl marad az LXX↔KJV kulcs. Új, nem GitHub-os forrás nem kell. |
| G3 | A kulcstábla neve és helye (2. menet): `konkordancia/Karoli_versmegfeleltetes.tsv`, oszlopok: `igehely_karoli · igehely_kjv · igehely_mt · osztaly · forras · megjegyzes`; generált fejléccel és proveniencia-sorral. |
| G4 | Az importer javítása a `resolve_karoli`-ban: (1) kézi függvény `None`-ja a lefedett fejezetben identitás, nem továbblépés; (2) új ág: ha a fejezet a kulcstáblában szerepel, onnan olvas, és elsőbbséget kap a versszám-őrrel szemben. A versszám-őr megmarad a tábla által nem fedett fejezetekre. |
| G5 | Az `EGYIK_SEM` fejezetek soronkénti megfeleltetése csak tartalmi egyeztetéssel készülhet, soronkénti horgony-megjegyzéssel (a `job_38_41_eltolas` docstringje a minta); bizonytalan sor üres marad, `karoli_ok=szamozas_elteres`, nem találunk ki megfeleltetést. |
| G6 | A lexikon 3. szakasza csak a saját generátorából frissül (CLAUDE.md, kimenet réteg). Ha a Józs-sorok oka H4, az a generátor LXX-szövegválasztásának kérdése: javaslat, nem javítás ebben a menetben. |
| G7 | A FORRASJELOLTEK FJ2-fájljait a menet nem írja át; a KK1 jelentése külön szakaszban sorolja fel, melyik FJ2-állítást cáfolja vagy erősíti meg, mérésre hivatkozva. |
| G8 | A kulcstábla a teljes KJV/ASV-import (3b) importkulcsa is lesz; ezért a Károli–KJV oldal a 39 ószövetségi könyv minden fejezetére készül, nem csak az LXX-érintett fejezetekre. |

---

## 3. Tételek

**1. menet**

- **KK0 — Kiindulás.** A §0 számainak újramérése a `main`-en (0.1–0.9), szkripttel.
  `naplok/KAROLI_KK0_kiindulas.md`.

- **KK1 — Ok-besorolás.** (a) A 39 ószövetségi könyv minden fejezetének versszáma három
  oszlopban: Károli (`Karoli_1908.tsv`, a `Karoli_ures_helyorzo_sorok.tsv` törölt sorai
  nélkül) · KJV (`verse_pairs.jsonl` `mt_refs`) · MT (`TAHOT_kivonat.tsv`); fejezetosztály
  az 1. pont szerint, tartalmi mintapróbával. (b) Az 1 015 érintett vers okonként: H1–H5
  vagy egyéb. (c) A lexikon 15 sora egyenként: ok, helyes Károli- és LXX-igehely, bizonyítékkal
  (horgonyszó mindkét oldalon). (d) Az FJ2-állítások felülvizsgálata (G7).
  `naplok/KAROLI_KK1_fejezetosztaly.tsv`, `naplok/KAROLI_KK1_15sor.tsv`,
  `naplok/KAROLI_KK1_jelentes.md`.

- **KK2 — Kulcstábla-tervezet.** `KJV` osztály: identitás. `MT` osztály: Károli = MT, a KJV
  a TVTMS-ből. `KEZI` osztály: a meglévő függvények kimenete, `None` = identitás a lefedett
  fejezetben. `EGYIK_SEM`: tartalmi egyeztetés G5 szerint. A §1 érvényességi próbái lefutnak.
  `naplok/KAROLI_KK2_kulcstabla_tervezet.tsv` (a G3 oszlopaival).

- **KK3 — Hatásbecslés ⛔.** Az importer módosítása nélkül, a tervezet alapján szkripttel:
  hány `szamozas_elteres` szósor/vers töltődne ki; mi lesz a lexikon 15 sorával; változna-e
  a 123/87/3/5/1 bontás (csak előrejelzés, a lexikont nem generálja). `naplok/KAROLI_KK3_hatas.md`.
  **ÁLLJ, jelentés a chatbe.**

**2. menet** *(csak a KK3 jóváhagyása után; a nyitó prompt külön kéri)*

- **KK4 — Élesítés.** `konkordancia/Karoli_versmegfeleltetes.tsv` a jóváhagyott tervezetből;
  `eszkozok/lxx_os_import.py` a G4 szerint; `konkordancia/LXX_OS/README.md` 2. szakasza
  az új algoritmussal.
- **KK5 — Újragenerálás.** `lxx_os_import.py --forras <lxx-morph klón a rögzített commiton>`
  (a hálózati letöltés helyett); majd a lexikon saját generátora. Minden generált fájl
  fejléce érintetlen formában.
- **KK6 — Újramérés és jelentés ⛔.** A §0.1–0.3 újra; a 15 sor új besorolása; a lexikon
  „Egyezés”-bontása előtte/utána; `ellenoriz.py`. `naplok/KAROLI_KK6_jelentes.md`.
  **ÁLLJ, jelentés a chatbe.**

Commit tételenként: `KK<n>: <rövid leírás>`.

---

## 4. Elfogadási feltételek

| # | Feltétel |
|---|---|
| K1 | 1. menet: `git diff --stat main..HEAD` csak `KAROLI_KULCS_BRIEF.md` és `naplok/KAROLI_*`. 2. menet: ezeken felül csak `konkordancia/Karoli_versmegfeleltetes.tsv`, `konkordancia/LXX_OS/*`, `eszkozok/lxx_os_import.py`, `eszkozok/lxx_kivonat_fetch_v2.py` (ha a G4 ott javít), és a lexikon generátorának kimenetei |
| K2 | `eszkozok/ellenoriz.py`: SÉRTÉS 0 |
| K3 | a KK1-ben mind a 15 sor besorolva, horgonyszóval mindkét oldalon |
| K4 | a KK2 tervezet átmegy a §1 érvényességi próbáin; a mintapróba ≥ 98% |
| K5 | minden szám szkriptből, a szkript a munkalap fejlécében; a TVTMS és az lxx-morph commitja rögzítve |
| K6 | nincs `csv` modul; héber/görög szöveg csak fájlba írt szkriptből (CLAUDE.md, Shell) |
| K7 | 2. menet: a `szamozas_elteres` csökkenése ≥ 90%, vagy a hiány okonként megindokolva |

---

## 5. Döntésnapló

| Verzió | Dátum | Változás |
|---|---|---|
| v1 | 2026.09.25 | Első változat. Kiváltó ok: az FJ2 a 15 `szamozas_elteres` sort kivonatolási hézagnak minősítette, de a chat-ellenőrzés szerint a fejezetek megvannak (0.4), az üres Károli-oszlop oka a `resolve_karoli` fejezetszintű versszám-őre (H1), a Károli MT-követése (H2) és valódi Károli-sajátosság (H3). Döntések: TVTMS mint MT-kulcs (G2); kulcstábla a teljes ÓSZ-re, a 3b importkulcsaként is (G8); bizonytalan sor üres marad (G5); a lexikon csak generátorból (G6); az FJ2-fájlok érintetlenek (G7). |

---

## 6. Nyitó prompt (cloud session; a briefet csatold)

```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
Olvasd el a CLAUDE.md-t és a konkordancia/LXX_OS/README.md 2. szakaszát.
1. A csatolt KAROLI_KULCS_BRIEF.md-t mentsd a repó gyökerébe, változtatás nélkül.
   Commit: "KK: KAROLI_KULCS_BRIEF.md v1".
2. Hajtsd végre a KK0–KK3 tételeket a brief §3 szerint, a §1 mércéivel és a §2 döntéseivel.
   Tételenként külön commit, és minden commit után push a saját ágadra. A main-re ne pushold.
3. A KK3 után ellenőrizd a §4 K1–K6-ot (az 1. menetre vonatkozó részt).
ÁLLJ a KK3 után: jelentés a chatbe (ág neve, commitlista, fejezetosztályok darabszáma,
a 15 sor besorolása, az FJ2-felülvizsgálat, a hatásbecslés, K1–K6).
A KK4–KK6-ot ebben a sessionben NE kezdd el.
```
