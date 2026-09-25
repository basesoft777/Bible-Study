# FORRASJELOLTEK_BRIEF.md — forrásjelöltek bevizsgálása: MT–LXX-illesztés, versszámozás, teljes KJV/ASV, BSB, Nave

*v1 — 2026.09.25 · jóváhagyásra: a §2 G-döntései és a §0 számai · a 2026.09.25-i munkaterv C briefje (3a–3e)*

**Cél.** Öt forrásjelöltről mérés alapján eldönteni, hogy beválik-e, és mire: (3a) szószintű
MT–LXX-illesztés a 87 függő LXX-helyhez és az S13-hoz; (3e) a 15 számozás-eltérés oka és a
versszámozási kulcs; (3b) teljes bibliás, Strong-címkés KJV/ASV a Károli-rokonsági hídhoz,
a BSB kiegészítőként; (3c) tiszta Nave-adatforrás. **Az 1. menet csak felmér, nem importál.**

**Előfeltétel:** nincs. A menet semmit nem akaszt meg, és semmire nem vár.

**Futás: cloud** (a kreditből). **Modell:** Sonnet. **Push:** csak a saját ágra, a menet végén;
a `main`-re soha.

**Szerkezet.** 1. menet: FJ0–FJ5, felmérés, jelentés ⛔ → a döntések után 2. menet: import
(brief v2).

**Nincs benne:** import a `konkordancia/`-ba (a `_nyers/` kivételével), bármilyen írás az
`adat/`, `lexikon/`, `tematikus_lezart/`, `motivumok/` alá; a 87 hely eldöntése (az a
`LEXIKON_LEZARAS_BRIEF.md` 4c-je); a SZOTAR S13 élesítése.

---

## 0. Kiindulás *(az FJ0 újraméri; eltérésnél jelentsd, és folytasd)*

| # | Mérés | Érték |
|---|---|---|
| 0.1 | `main` | `a6783e4` (a `szotar-v1-1` merge-e) |
| 0.2 | A 8 `lexikon/*_TUDOMANYOS.md` 3. szakasza, „Egyezés” oszlop | egyező 123 · kutatói azonosítás függőben 87 · szamozas_elteres 15 · eltérő 3 · nincs LXX_OS-könyv 5 · LXX-minusz 1 |
| 0.3 | `adat/lxx_dontesek.tsv` | 4 sor (LD001–LD004), mind ISTENTISZT-001 |
| 0.4 | `konkordancia/KJV_Strongs_*.tsv`, `ASV_Strongs_*.tsv` | 6 fájl (1Móz, 2Móz, Péld), a studybible.info oldalairól (`konkordancia/README.md`) |
| 0.5 | `konkordancia/LXX_OS/` versmegfeleltetés | `verse_pairs.jsonl`, TVTMS-alapú, ~99,57% (a forrás saját auditja, `LXX_OS/README.md`) |
| 0.6 | SZOTAR S0.8 (versszintű együtt-előfordulás) | H7121 × G1941: 102/635 vers (14,8%); grammatikai szűrés nélkül zajos (`naplok/SZOTAR_S0_jelentes.md` 8. pont) |
| 0.7 | `eszkozok/ellenoriz.py` | RENDBEN 9 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 2 |

---

## 1. Mércék

**A 3a aranykészletei** (az FJ1 ezekből számol):
- **A:** a 0.2 123 „egyező” sora: ismert héber token ↔ görög lemma pár.
- **B:** az LD001–LD004 kutatói döntés.
- **C:** a 3 „eltérő” sor, csak jelentésre.

**A 3a küszöbei:**
- **beválik:** az A-n ≥ 95% egyezés és a B-n 4/4 → a 87 hely előtöltésére és az S13 szószintű változatára javasolható;
- **feltétellel:** 90–95%, vagy a B-n 3/4 → csak jelöltként, kézi megerősítéssel;
- **nem:** < 90% → a D14 marad (versszintű).

**A 3b küszöbe:** a teljes KJV-jelölt Strong-halmaza versenként ≥ 98%-ban egyezik a meglévő
`KJV_Strongs_Genesis.tsv`-vel az 1Mózes mind az 1 533 versén.

**Minden forrásnál kötelező:** licenc a forrás saját LICENSE- vagy README-szövegéből szó
szerint idézve; URL; rögzített commit vagy verzió; sha256. A D17 szerint csak a repóban
tárolható és onnan renderelhető forrás javasolható importra.

---

## 2. G-döntések

| # | Döntés |
|---|---|
| G1 | Az 1. menet csak felmér: ír a `naplok/FORRAS_FJ*` fájlokba és a `konkordancia/_nyers/` alá (gitignore), máshová nem. |
| G2 | Az 1. pont mércéi és küszöbei kötelezők; szám csak lefuttatott szkriptből jöhet, becslés nem. |
| G3 | A 3a mindkét jelöltet méri: CenterBLC/MT-LXX és Macula Hebrew (a korábbi, 2026.09.23-i megállapítás szerint szószintű MT→LXX-illesztést hordoz; ellenőrizendő). Ha mindkettő beválik, a magasabb A-egyezésű a javasolt. A Macula Greek licencét külön kell ellenőrizni. |
| G4 | A 87 helyre adott jelöltek csak munkalapba kerülnek (`naplok/FORRAS_FJ1_lxx_jeloltek.tsv`), az `adat/`-ba nem (CLAUDE.md 2. szabály). A döntés a 4c-é. |
| G5 | A 3b sorrendje: előbb teljes bibliás, Strong-címkés KJV (és ha van, ASV), a Károli-rokonsági híd miatt; a BSB csak kiegészítő, lefedettségi tartalék (munkaterv M4). |
| G6 | A mai KJV/ASV-fájlok Strong-címkézési rétegének licencét is fel kell mérni (a studybible.info nyilatkozata); a szöveg közkincs, a címkézés licence nincs rögzítve. |
| G7 | Közös fájlt a menet nem ír (`NYITOTT_FELADATOK.md`, changelogok, más briefek döntésnaplói); a jelentés a saját ágán marad. |
| G8 | A NYITOTT 1. tételéhez (`morphology.sqlite` `ClauseID`) az FJ1 csak javaslatot ad: lefedi-e a Macula tagmondat-tagolása ugyanezt a célt. |

---

## 3. Tételek

- **FJ0 — Hozzáférés és kiindulás.** A §0 számainak újramérése. Minden forrás elérhetőségének
  mérése a sessionből (GitHub-repók, egyéb letöltőhelyek): elérhető / nem elérhető, a hibaüzenettel.
  Nem elérhető forrásnál jelöld, és folytasd a többivel. `naplok/FORRAS_FJ0_hozzaferes.md`.

- **FJ1 — 3a: MT–LXX-illesztés.** Mindkét jelölt letöltése a `_nyers/` alá; licenc, szerkezet,
  lefedettség (könyvek, versek, szavak). Az illesztés alkalmazása az A/B/C aranykészletre:
  egyezési arány, eltéréslista. A 87 függő helyre jelölt-munkalap: igehely, héber token,
  javasolt görög lemma és Strong, forrás, bizonyosság. Az S13-ra: a szószintű illesztés
  kiváltja-e a versszintű együtt-előfordulást. `naplok/FORRAS_FJ1_mtlxx_macula.md`,
  `naplok/FORRAS_FJ1_arany.tsv`, `naplok/FORRAS_FJ1_lxx_jeloltek.tsv`.

- **FJ2 — 3e: versszámozás.** A 15 `szamozas_elteres` sor egyenkénti besorolása az
  `LXX_OS` `verse_pairs.jsonl` (TVTMS) és a `LXX_versificacios_terkep.tsv` alapján:
  (a) a megfeleltetés megoldja → javasolt LXX-igehely; (b) valódi LXX-eltérés (minusz,
  átrendezés) → kutatói kérdés. Ezen túl: a Károli- és a KJV-versállomány eltérésének mérése
  1Móz, 2Móz, Péld könyvekben, a 3b importkulcsának tervezéséhez. Javaslat: kell-e külön
  Károli-kulcsú számozási tábla. `naplok/FORRAS_FJ2_szamozas.tsv`.

- **FJ3 — 3b: teljes KJV/ASV, majd BSB.** Teljes bibliás, szószintű, Strong-címkés KJV
  (és ASV) keresése; lehetséges kiindulópont az eBible.org USFM-kiadása (nem ellenőrzött).
  Mérés: licenc (szöveg és címkézés külön), 66 könyv lefedettsége, formátum, és az 1. pont
  szerinti Strong-egyezés. Ugyanez a BSB-re (BSB-publishing), a TAHOT/TAGNT Strong-halmazával
  összevetve, mintán. A G6 licencfelmérése. `naplok/FORRAS_FJ3_kjv_bsb.md`, `.tsv`.

- **FJ4 — 3c: Nave.** Tiszta adatforrás keresése: közkincs alapszöveg (1897), gépileg
  olvasható szerkezet (témakör, altéma, igehelyek), a származás nem jogvédett modern
  kiadás oldaláról. Mérés: témakör- és igehely-darabszám, az igehelyek feldolgozhatósági
  aránya, három témakör mintája. Megvizsgálandó a `basokant/nave` adatforrása, a
  `theonize/bible_database` és az `elcafe7/lex`. `naplok/FORRAS_FJ4_nave.md`.

- **FJ5 — Összesítő jelentés ⛔.** Forrásonként: licenc (idézet), lefedettség, mérés,
  javaslat (import / feltétellel / nem) indokkal; a 2. menet javasolt importlistája.
  `naplok/FORRAS_jelentes.md`. ÁLLJ, jelentés a chatbe.

Commit tételenként: `FJ<n>: <rövid leírás>`.

---

## 4. Elfogadási feltételek

| # | Feltétel |
|---|---|
| K1 | `git diff --stat main..HEAD`: csak `FORRASJELOLTEK_BRIEF.md` és `naplok/FORRAS_*` |
| K2 | `eszkozok/ellenoriz.py`: SÉRTÉS 0 (változatlan a 0.7-hez képest) |
| K3 | minden letöltött forrásnál URL, commit/verzió, sha256, szó szerinti licencidézet |
| K4 | az FJ1 és FJ3 arányai szkriptből számolva, a szkript a munkalap fejlécében megnevezve |
| K5 | az FJ2-ben mind a 15 sor besorolva |
| K6 | nincs `csv` modul; a Strong-számok nullázva (SEMA 1.2); héber/görög szöveg csak fájlba írt szkriptből (CLAUDE.md, Shell) |
| K7 | a jelentésben minden forrásnál javaslat és indok |

---

## 5. Döntésnapló

| Verzió | Dátum | Változás |
|---|---|---|
| v1 | 2026.09.25 | Első változat a munkaterv alapján (M4, M5): csak felmérés; aranykészletek és küszöbök (G2); a 87 hely jelöltjei csak munkalapba (G4); KJV előbb, BSB kiegészítő (G5); a KJV/ASV címkézési licence (G6); közös fájl nem írható (G7). |

---

## 6. Nyitó prompt (cloud session; a briefet csatold)

```
Először írd ki: pwd, git branch --show-current, git log --oneline -1
Olvasd el a CLAUDE.md-t.
1. A csatolt FORRASJELOLTEK_BRIEF.md-t mentsd a repó gyökerébe, változtatás nélkül.
   Commit: "FJ: FORRASJELOLTEK_BRIEF.md v1".
2. Hajtsd végre az FJ0–FJ5 tételeket a brief §3 szerint, a §1 mércéivel és a §2 döntéseivel.
   Tételenként külön commit.
3. A menet végén ellenőrizd a §4 K1–K7-et, majd pushold a saját ágadat. A main-re ne pushold.
ÁLLJ az FJ5 után: jelentés a chatbe (ág neve, commitlista, forrásonkénti javaslat, K1–K7).
```
