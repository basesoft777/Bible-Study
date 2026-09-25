# KAROLI_KULCS_BRIEF.md — Károli-versmegfeleltetés: a `szamozas_elteres` valódi oka és javítása

*v1.1 — 2026.09.25 · jóváhagyásra: a §0b számai, a G2 módosítása és a G9–G11 · új: KK1b-menet a
KK4 előtt (a KK 1. menet jelentésének felülvizsgálatából)*

**Cél.** A `konkordancia/LXX_OS/*.tsv` `igehely_karoli` oszlopa 20 346 szósorban (≈1 000 versben)
üres, `karoli_ok=szamozas_elteres` címkével; ebből ered a 8 lexikonoldal 15 `szamozas_elteres`
sora. A menet (1) okonként besorolja az üres sorokat, (2) Károli-kulcsú versmegfeleltető táblát
készít a KJV- és az MT-számozáshoz, (3) jóváhagyás után javítja az importert, újragenerál és újramér.

**Előfeltétel:** nincs. A `main`-ről indul; a `claude/peaceful-rubin-39uuzs` (FORRASJELOLTEK
1. menet) ágat nem érinti és nem vár rá.

**Futás: cloud.** **Modell:** Sonnet; a KK2 kézi fejezeteihez Opus, ha a „egyik sem” osztály
10 fejezetnél több. **Push:** csak a saját ágra, tételenként; a `main`-re soha.

**Szerkezet.** 1. menet: KK0–KK3, mérés és táblatervezet ⛔ (lefutott, ág: `claude/karoli-kulcs-35158`)
→ **1b menet: KK1b-1…KK1b-5, pótlás és ütköztetés ⛔** → jóváhagyás után 2. menet: KK4–KK6,
élesítés és újragenerálás ⛔.

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

## 0b. Az 1. menet eredménye és hiányai *(chat-ellenőrzés a `claude/karoli-kulcs-35158` tarballján, 2026.09.25; a KK1b-1 újraméri)*

| # | Mérés | Érték |
|---|---|---|
| 0b.1 | `naplok/KAROLI_KK1_fejezetosztaly.tsv` | 896 fejezet, 36 könyv (KJV 786 · MT 84 · KEZI 13 · EGYIK_SEM 13) |
| 0b.2 | Hiányzó ószövetségi könyvek | Ezsdrás (10), Nehémiás (13), Eszter (10) — 33 fejezet; 929 − 896 = 33 |
| 0b.3 | KK3 hatásbecslés alapja | 985 mért vers, „38 nem-Zsoltár könyv”; a Zsoltárok nem mérve; a „~686 (67,6%)” a teljes 1 015-re **arányosítás** |
| 0b.4 | K4 a jelentésben | „RENDBEN, korláttal”: a 10%-os mintapróba helyett 27+1 tételes kézi minta |
| 0b.5 | `konkordancia/LXX_versificacios_terkep.tsv` | 5 426 sor + fejléc, 35 könyv; oszlopok: `Karoli_igehely · Heber_vers · Latin_vers · Gorog_LXX_vers · Elteres_tipusa · Karoli_egyezik_hol`; Renumber 5 091 · Concatenation/Merge 335 |
| 0b.6 | ua., `Karoli_egyezik_hol` | Heber 1 503 · EGYIK_SEM 1 233 · Heber,Latin 1 211 · Latin,Gorog 463 · Latin 361 · ELLENORZESRE_VAR 267 · Heber,Gorog 216 · Heber,Latin,Gorog 165 · egyéb a maradék |
| 0b.7 | ua., a KK-menet használta-e | nem (0 hivatkozás a `naplok/KAROLI_*` fájlokban) |
| 0b.8 | Ellentmondás-minta | a térkép: Károli Jón 2:3 → Héber Jon.2:4, `EGYIK_SEM`; tartalmi kontroll (§0.8): Károli Jón 2:3 = MT 2:3 = LXX 2:3 |
| 0b.9 | A térkép kiejtésének oka | `LXX_OS/README.md` 2. szakasz: a `Gorog_LXX_vers` oszlop a studybible.info saját számozására épül (LEXV2_1 v4); a Károli–Héber–Latin oszlopokat ez nem érinti |

**Következtetés:** a térkép ellenőrzött sorai (tartalmilag egyeztetett, pl. Ez 20/21, 1Móz 32)
lezárt döntések; az ellenőrizetlen sorokban (`EGYIK_SEM`, `ELLENORZESRE_VAR`) a `Karoli_igehely`
a 0b.8 szerint az angol számozást hordozhatja. A térkép tehát nem vehető át vakon, de a kulcstábla
kötelező ütközés-ellenőrzője.

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
- **Ütköztetés a térképpel (KK1b-3):** a tervezet minden sora, amelyhez a
  `LXX_versificacios_terkep.tsv`-ben van `Karoli_igehely` sor, egy osztályt kap: `EGYEZIK`
  (a tervezet `igehely_mt`-je = `Heber_vers`) · `UTKOZIK_ELLENORZOTT` (eltér, és a térkép sora
  tartalmilag egyeztetett) · `UTKOZIK_ELLENORIZETLEN` (eltér, a térkép sora `EGYIK_SEM` vagy
  `ELLENORZESRE_VAR`). `UTKOZIK_ELLENORZOTT` sor a tervezetben nem maradhat: vagy a tervezet
  javul, vagy horgonnyal bizonyított, miért téves a térkép.
- **A K4 mintapróba horgonya:** a Károli-vers és a jelölt MT-vers között a `TAHOT_kivonat.tsv`
  tulajdonnév- (TIPNR) vagy számnév-Strongja; KJV-szöveg nem kell hozzá.
- **Siker (KK6):** a `szamozas_elteres` szósorok száma a 0.1-hez képest legalább 90%-kal
  csökken; a lexikon 15 sorából mindegyik új besorolást kap indokkal.

Szám csak lefuttatott, fájlba írt szkriptből jöhet; a szkript neve a munkalap fejlécében.

---

## 2. G-döntések

| # | Döntés |
|---|---|
| G1 | Az 1. menet csak `naplok/KAROLI_KK*` fájlokba és a `konkordancia/_nyers/` (gitignore) alá ír. |
| G2 | Az MT↔angol kulcs forrása a STEPBible TVTMS (`STEPBible-Data`, commit rögzítve); a verse_pairs.jsonl marad az LXX↔KJV kulcs. **v1.1:** a repó saját, TVTMS-alapú `konkordancia/LXX_versificacios_terkep.tsv`-je a Károli–Héber–Latin oszlopaival kötelező jelöltlista és ütközés-ellenőrző; a `Gorog_LXX_vers` oszlopa nem használható (0b.9). Új, nem GitHub-os forrás nem kell. |
| G3 | A kulcstábla neve és helye (2. menet): `konkordancia/Karoli_versmegfeleltetes.tsv`, oszlopok: `igehely_karoli · igehely_kjv · igehely_mt · osztaly · forras · megjegyzes`; generált fejléccel és proveniencia-sorral. |
| G4 | Az importer javítása a `resolve_karoli`-ban: (1) kézi függvény `None`-ja a lefedett fejezetben identitás, nem továbblépés; (2) új ág: ha a fejezet a kulcstáblában szerepel, onnan olvas, és elsőbbséget kap a versszám-őrrel szemben. A versszám-őr megmarad a tábla által nem fedett fejezetekre. |
| G5 | Az `EGYIK_SEM` fejezetek soronkénti megfeleltetése csak tartalmi egyeztetéssel készülhet, soronkénti horgony-megjegyzéssel (a `job_38_41_eltolas` docstringje a minta); bizonytalan sor üres marad, `karoli_ok=szamozas_elteres`, nem találunk ki megfeleltetést. |
| G6 | A lexikon 3. szakasza csak a saját generátorából frissül (CLAUDE.md, kimenet réteg). Ha a Józs-sorok oka H4, az a generátor LXX-szövegválasztásának kérdése: javaslat, nem javítás ebben a menetben. |
| G7 | A FORRASJELOLTEK FJ2-fájljait a menet nem írja át; a KK1 jelentése külön szakaszban sorolja fel, melyik FJ2-állítást cáfolja vagy erősíti meg, mérésre hivatkozva. |
| G8 | A kulcstábla a teljes KJV/ASV-import (3b) importkulcsa is lesz; ezért a Károli–KJV oldal a 39 ószövetségi könyv minden fejezetére készül, nem csak az LXX-érintett fejezetekre. |
| G9 | A KK1b csak a `naplok/KAROLI_KK1b_*` fájlokba ír; a `LXX_versificacios_terkep.tsv`-t nem módosítja. A térkép javítandó sorai javaslatként kerülnek a jelentésbe (`naplok/KAROLI_KK1b_terkep_javaslat.tsv`). |
| G10 | Hatásszám csak teljes mérésből: arányosítás, extrapoláció tilos (G2 v1 „becslés nem”). Ami nem mérhető, az „nem mért”, okkal. |
| G11 | A K-feltétel állapota csak RENDBEN vagy NEM TELJESÜL lehet; a „RENDBEN, korláttal” nem elfogadható. A nem teljesülő feltétel mellé ok és pótlási javaslat kerül. |

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

**1b menet** *(ugyanazon az ágon: `claude/karoli-kulcs-35158`; az 1. menet fájljait nem írja felül, újakat hoz létre)*

- **KK1b-1 — A §0b újramérése.** 0b.1–0b.9 szkripttel. `naplok/KAROLI_KK1b_kiindulas.md`.
- **KK1b-2 — Hiányzó könyvek és a Zsoltárok.** (a) Ezsdrás, Nehémiás, Eszter fejezetosztálya a
  KK1 módszerével (a LXX_OS-ben: `2-esdras.tsv`, `esther-greek.tsv`; a kánoni szakaszok
  megfeleltetése a `verse_pairs.jsonl` `mt_book`-ja szerint; a görög Eszter-többletek
  `nincs_karoli_konyv`/`nincs_mt_parositas` maradnak). (b) A 150 zsoltár fejezetosztálya és
  a Zsoltár-sorok ok-besorolása (H1–H5), a `zsolt_felirat_eltolas` ágat is beleértve.
  Kimenet: a teljes, 929 fejezetes osztálytábla `naplok/KAROLI_KK1b_fejezetosztaly.tsv`,
  és az ok-besorolás kiegészítése `naplok/KAROLI_KK1b_ok_besorolas.tsv`.
- **KK1b-3 — Ütköztetés a térképpel.** A KK2-tervezet és a KK1b-2 új sorai a §1 ütköztetési
  mércéje szerint. `UTKOZIK_ELLENORZOTT`: javítás a tervezetben, vagy horgonyos bizonyítás.
  `UTKOZIK_ELLENORIZETLEN`: horgonyos döntés soronként, a 0b.8 mintájára. A térkép javítandó
  sorai: G9. Kimenet: `naplok/KAROLI_KK1b_kulcstabla_tervezet.tsv` (a G3 oszlopaival, új
  `terkep_utkozes` oszloppal), `naplok/KAROLI_KK1b_utkozes.tsv`.
- **KK1b-4 — K4 mintapróba.** 10%-os véletlen minta (seed rögzítve) a `KJV` és `MT` osztályú
  fejezetekből, fejezetenként az első és az utolsó vers, TAHOT-horgonnyal (§1). Minden
  mintatétel sorban: Károli-igehely, jelölt MT-igehely, horgony-Strong, egyezik/nem.
  `naplok/KAROLI_KK1b_mintaproba.tsv`.
- **KK1b-5 — Hatás újraszámolása ⛔.** A KK3 szkriptje a KK1b-tervezettel, a teljes 1 015
  (vagy újramért) versen, Zsoltárokkal; a 15 lexikon-sor újra; K1–K6 a G11 szerint.
  `naplok/KAROLI_KK1b_hatas.md`. **ÁLLJ, jelentés a chatbe.**

**2. menet** *(csak a KK1b-5 jóváhagyása után; a nyitó prompt külön kéri)*

- **KK4 — Élesítés.** `konkordancia/Karoli_versmegfeleltetes.tsv` a jóváhagyott KK1b-tervezetből;
  `eszkozok/lxx_os_import.py` a G4 szerint; `konkordancia/LXX_OS/README.md` 2. szakasza
  az új algoritmussal.
- **KK5 — Újragenerálás.** `lxx_os_import.py --forras <lxx-morph klón a rögzített commiton>`
  (a hálózati letöltés helyett); majd a lexikon saját generátora. Minden generált fájl
  fejléce érintetlen formában.
- **KK6 — Újramérés és jelentés ⛔.** A §0.1–0.3 újra; a 15 sor új besorolása; a lexikon
  „Egyezés”-bontása előtte/utána; `ellenoriz.py`. `naplok/KAROLI_KK6_jelentes.md`.
  **ÁLLJ, jelentés a chatbe.**

Commit tételenként: `KK<n>: <rövid leírás>` (az 1b menetben `KK1b-<n>: …`).

---

## 4. Elfogadási feltételek

| # | Feltétel |
|---|---|
| K1 | 1. és 1b menet: `git diff --stat main..HEAD` csak `KAROLI_KULCS_BRIEF.md` és `naplok/KAROLI_*`. 2. menet: ezeken felül csak `konkordancia/Karoli_versmegfeleltetes.tsv`, `konkordancia/LXX_OS/*`, `eszkozok/lxx_os_import.py`, `eszkozok/lxx_kivonat_fetch_v2.py` (ha a G4 ott javít), és a lexikon generátorának kimenetei |
| K2 | `eszkozok/ellenoriz.py`: SÉRTÉS 0 |
| K3 | a KK1-ben mind a 15 sor besorolva, horgonyszóval mindkét oldalon; 1b: a 929 fejezet mind osztályozva |
| K4 | a KK1b-tervezet átmegy a §1 érvényességi próbáin; a KK1b-4 mintapróba ≥ 98%; nincs `UTKOZIK_ELLENORZOTT` sor bizonyítás nélkül |
| K5 | minden szám szkriptből, a szkript a munkalap fejlécében; a TVTMS és az lxx-morph commitja rögzítve |
| K6 | nincs `csv` modul; héber/görög szöveg csak fájlba írt szkriptből (CLAUDE.md, Shell) |
| K7 | 2. menet: a `szamozas_elteres` csökkenése ≥ 90%, vagy a hiány okonként megindokolva |
| K8 | minden K-feltétel állapota RENDBEN vagy NEM TELJESÜL (G11); hatásszám csak mérésből (G10) |

---

## 5. Döntésnapló

| Verzió | Dátum | Változás |
|---|---|---|
| v1.1 | 2026.09.25 | A KK 1. menet (ág `claude/karoli-kulcs-35158`) jelentésének chat-ellenőrzése után: 36 könyv 39 helyett (0b.2), a Zsoltárok kimaradt és a hatásszám arányosítás (0b.3), a K4 nem teljesült (0b.4), a repó `LXX_versificacios_terkep.tsv`-je nem került felhasználásra (0b.7). Új §0b; §1 ütköztetési mérce és TAHOT-horgonyos mintapróba; G2 módosítva (a térkép kötelező ellenőrző, a görög oszlop kizárva); új G9–G11; új KK1b-menet a KK4 előtt; K1, K3, K4 pontosítva, új K8. |
| v1 | 2026.09.25 | Első változat. Kiváltó ok: az FJ2 a 15 `szamozas_elteres` sort kivonatolási hézagnak minősítette, de a chat-ellenőrzés szerint a fejezetek megvannak (0.4), az üres Károli-oszlop oka a `resolve_karoli` fejezetszintű versszám-őre (H1), a Károli MT-követése (H2) és valódi Károli-sajátosság (H3). Döntések: TVTMS mint MT-kulcs (G2); kulcstábla a teljes ÓSZ-re, a 3b importkulcsaként is (G8); bizonytalan sor üres marad (G5); a lexikon csak generátorból (G6); az FJ2-fájlok érintetlenek (G7). |

---

## 6. Nyitó prompt — 1b menet (cloud session; a briefet csatold)

```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
Válts a claude/karoli-kulcs-35158 ágra (git fetch; git checkout), és írd ki újra a git log --oneline -1-et.
Olvasd el a CLAUDE.md-t, a konkordancia/LXX_OS/README.md 2. szakaszát és a naplok/KAROLI_KK1_jelentes.md-t.
1. A csatolt KAROLI_KULCS_BRIEF.md v1.1-et írd a repó gyökerében lévő v1 helyére, változtatás nélkül.
   Commit: "KK: KAROLI_KULCS_BRIEF.md v1.1".
2. Hajtsd végre a KK1b-1…KK1b-5 tételeket a brief §3 szerint, a §0b, §1 és a G9–G11 szerint.
   Tételenként külön commit, és minden commit után push erre az ágra. A main-re ne pushold.
3. A KK1b-5 után ellenőrizd a §4 K1–K6 és K8 feltételt; állapot csak RENDBEN vagy NEM TELJESÜL.
ÁLLJ a KK1b-5 után: jelentés a chatbe (commitlista, 929 fejezet osztálybontása, a térkép-ütközések
darabszáma osztályonként, a mintapróba aránya, a mért hatás a Zsoltárokkal, a 15 sor, K1–K8).
A KK4–KK6-ot ebben a sessionben NE kezdd el.
```

## 7. Nyitó prompt — 1. menet (v1, lefutott; archív)

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
