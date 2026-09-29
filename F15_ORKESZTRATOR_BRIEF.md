# F15_ORKESZTRATOR_BRIEF.md — a munkafolyamat orkesztrátor-parancsa

*v1.3 · 2026.09.29 · FELADATOK #15 (új feladat, a chat jóváhagyásával) · Modell: sonnet · Függ: — (bármikor futhat, az 1. fázistól független)*

*Repóbeli másolat (F14.5): a szám #14 → #15 (a `main`-en a #14 az FP2, DT4 döntés), a naplónevek `orkesztrator-15`; az ág neve marad `claude/orkesztrator-14`. A `/kovetkezo` 1. lépése kiegészült az elavult DONTESEK-tételek jelzésével; a `vegrehajto-*` fájlok önállóak (nem hivatkoznak a brief pontszámaira). A D-számozás a repóban D8–D13 (l. FELADATOK.md). Az élő szöveg a `.claude/`-ben van.*

## 0. Nyitó prompt (ezt másold a Code-ba, a brieffel együtt)

> Olvasd be a csatolt `F15_ORKESZTRATOR_BRIEF.md`-t, a `FELADATOK.md`-t és a `CLAUDE.md`-t. Hajtsd végre a brief 3. pontját a main-ből nyitott új ágon (`claude/orkesztrator-14`). A 2. pont tiltásai kötelezők. A végén a brief 6. pontja szerint zárj.

## 1. Cél

A felhasználó ne közvetítsen kézzel a chat és a Code között, és ne neki kelljen összeállítania a következő lépést. Ezt egy Claude Code-parancs (`/kovetkezo`) készíti elő: a `FELADATOK.md`-ből javaslatot tesz a következő végrehajtható feladatra, és **a felhasználóval egyezteti, mielőtt bármit elindítana**. Csak kifejezett „mehet” után futtatja a briefje szerint, ellenőrizteti, és döntési pontnál megáll. A nyitott döntések egyetlen fájlba (`DONTESEK.md`) kerülnek; a chat csak ezt kapja.

Nem cél: teljes autonómia. A parancs nem mergel, nem hoz tartalmi döntést, és egy session egy feladatot végez.

## 2. Tiltások

- Nem mergel, nem töröl ágat, nem módosít más feladatsort, mint amit a brief megenged.
- Meglévő címsor szövegét nem módosítja (a CI E5 szabálya törlésnek venné); a változás a címsor alá kerül.
- A `FELADATOK.md` D1–D5 döntéssorait nem írja át, csak újakat fűz hozzá.
- A `fuggetlen-ellenor` meglévő tartalmát nem törli, csak kiegészíti.

## 3. Elkészítendő fájlok

### 3.1 `.claude/commands/kovetkezo.md` — az orkesztrátor

A parancs szövege az alábbi (a frontmatter szintaxisát a futó Claude Code verzióhoz igazítsd, lásd 3.5):

```markdown
---
description: A FELADATOK.md következő végrehajtható feladatának futtatása, ellenőrzéssel, döntési pontnál megállva
model: sonnet
---

Te vagy a PaRDeS orkesztrátora. Egy session = egy feladat.
Az 1–5. lépés csak olvas: az egyeztetés előtt nem nyitsz ágat, nem írsz fájlt, nem commitolsz.

1. BEOLVASÁS: `git fetch`; olvasd be a main `FELADATOK.md`, `DONTESEK.md` és `CLAUDE.md` fájlját.
2. ELDÖNTÖTT TÉTELEK: ha a `DONTESEK.md`-ben van „eldöntve”, de „alkalmazásra vár” állapotú tétel, az a feladat az első jelölt.
3. JELÖLT KIVÁLASZTÁSA, ebben a sorrendben:
   - csak az 1. fázis sorai, amíg az 1. fázis minden sora nincs ✅;
   - állapot ⬜ vagy ⏸, és a „Következő lépés” NEM „Te:” kezdetű;
   - minden „Függ ettől” feladat ✅ (a main-ben);
   - nincs rá nyitott tétel a `DONTESEK.md`-ben;
   - elsőbbség: a kritikus út sorrendje, utána a táblázat sorrendje.
   Helyi gépet igénylő feladatot (pl. #6) nem indítasz: jelzed, és továbblépsz.
4. ELŐFELTÉTELEK: a feladat briefje a repóban van (`F<nn>_*_BRIEF.md`; ha még régi néven van, a „Hol” oszlop szerint keresd), és a fejlécében van `Modell:` sor
   (`sonnet` | `opus` | `haiku` | `külső:<név>`). Ha bármelyik hiányzik: nyiss tételt a
   `DONTESEK.md`-ben („brief kell” / „modell nincs megadva”) — de csak az 5. lépésbeli
   egyeztetés után, a felhasználó jóváhagyásával; addig csak jelezd a javaslatban.
5. EGYEZTETÉS (kötelező, soha nem hagyod ki):
   a) Javaslat, legfeljebb 10 sorban: a javasolt feladat és miért ez; brief; modell; ág;
      a brief ⛔ pontjai; hiányzó előfeltétel; legfeljebb 2 alternatív jelölt; a kihagyott
      feladatok és az okuk egy sorban.
   b) Várj. A felhasználó kérdezhet, más feladatot választhat, szűkítheti vagy módosíthatja
      a hatókört, vagy leállíthatja a menetet. Kérdésre válaszolj, módosításnál írd ki az
      új tervet, és várj újra.
   c) Csak a kifejezett „mehet” (vagy egyértelmű igen a végső tervre) indítja a 6. lépést.
      Hallgatás, kétértelmű válasz vagy témaváltás nem jóváhagyás.
   d) Ha a felhasználó a briefben rögzítettől eltérő hatókört kér, azt a zárójelentésben
      „Egyeztetett eltérés” címen rögzítsd.
6. VÉGREHAJTÁS: új ág a main-ből (`claude/<feladat-slug>`). A munkát a brief modelljének
   megfelelő végrehajtó subagent végzi (`vegrehajto-sonnet` / `vegrehajto-opus` / `vegrehajto-haiku`).
   `külső:<név>` esetén a `vegrehajto-sonnet` a briefben megadott szkripttel futtatja a
   külső modellt; Claude-dal nem helyettesíti. Gyakran commitolj.
7. ⛔ PONT: ha a brief kötelező megállást ír elő, vagy tartalmi döntés kell: tétel a
   `DONTESEK.md`-be (kérdés, opciók, javaslat, hivatkozás a naplóra), commit, push, állj meg.
8. KERETKIMERÜLÉS: ha a használati keret fogy, tiszta ponton commitolj, a zárójelentésbe írd a
   „Folytatási pont” szakaszt, és állj meg. A következő `/kovetkezo` onnan folytatja.
9. ELLENŐRZÉS: futtasd a `fuggetlen-ellenor` subagentet; jelentése: `naplok/ELLENOR_<feladat>.md`.
10. ZÁRÁS (CLAUDE.md menetzárás): zárójelentés `naplok/<feladat>_zaras.md` (≤20 sor),
    a `FELADATOK.md` saját sorának frissítése, push, draft PR a main-be.
    A felhasználónak adott válasz első sora: PR-link + CI-állapot; utána legfeljebb 5 sor.
11. SOHA: merge, ágtörlés, más feladatsor módosítása, új feladat felvétele, tartalmi döntés.
```

### 3.2 Végrehajtó subagentek — `.claude/agents/vegrehajto-*.md`

Három, tartalmilag azonos fájl, csak a modell tér el (`sonnet`, `opus`, `haiku`). Szerep: a kapott brief végrehajtása, a brief ⛔ pontjain megállás, gyakori commit. Ha a futó Claude Code subagent-hívásonként megengedi a modell megadását, elég egy `vegrehajto.md`; ezt jelezd a zárójelentésben.

### 3.3 `fuggetlen-ellenor` kiegészítése

- Modell: `opus` (a frontmatterben rögzítve).
- A meglévő tartalom alá új szakasz, „Kötelező ellenőrzőlista”:
  1. Kiszűrt vagy törölt sorok kategóriákra bontva, darabszámmal.
  2. Kulcstartomány-lefedettség (pl. Strong-alapszámok hiánya a várt tartományban).
  3. A „nulla-diff” pontos hatóköre: mire vonatkozik, mire nem.
  4. Adattábla sorszámának változása a main-hez képest; ha nagyobb a küszöbnél (lásd E17 a `DONTESEK.md`-ben), van-e bontási napló.
  5. A brief ⛔ pontjait a végrehajtó tényleg betartotta-e.
- A jelentés első sora: `TISZTA` vagy `ELTÉRÉS: <n> tétel`.

### 3.4 `DONTESEK.md` — a döntési sor (a repó gyökerében)

Sablon:

```markdown
# DONTESEK.md — nyitott döntések sora

*A chat csak ezt a fájlt kapja. Egy tétel = egy döntés. Az orkesztrátor nyit tételt, a felhasználó (a chattel) dönt, az orkesztrátor alkalmazza.*

Állapot: 🟡 nyitott · 🟢 eldöntve, alkalmazásra vár · ✅ alkalmazva

| # | Feladat | Kérdés | Opciók | Javaslat | Állapot | Döntés | Napló |
|---|---|---|---|---|---|---|---|
```

Kezdő tételek: töltsd fel a `FELADATOK.md` jelenlegi ⏸/⛔ tételeiből és a „Te: döntés …” kezdetű következő lépésekből (szó szerint átvéve, forrássorral). Ezen felül egy új tétel:

- **E17 küszöb** (#2 CI): „Adattábla sorszámának mekkora változása kívánjon bontási naplót?” · Opciók: 1% / 5% / abszolút sorszám · Javaslat: 1% · 🟡

### 3.5 Szintaxis-ellenőrzés

A parancs- és subagent-fájlok frontmatterét (különösen a `model:` mezőt) a futó Claude Code verzió dokumentációja szerint ellenőrizd. Ha valamelyik mező nem támogatott, a legközelebbi működő megoldást válaszd, és írd le a zárójelentésben.

## 4. A `FELADATOK.md` módosításai (v1 → v1.1)

A címsorok szövege változatlan marad.

**4.1 Fejléc** — a verziót v1.1-re, a dátumot 2026.09.28-ra állítsd, és a mondat végére fűzd: „Munkafolyamat: `/kovetkezo` orkesztrátor, döntések a `DONTESEK.md`-ben.”

**4.2 Új sor az 1. fázis táblájába** (a #8 után):

| 15 | Orkesztrátor-parancs (munkafolyamat) | a következő feladatot gép választja és futtatja; a chat csak döntéskor kap jelzést | *(a menet szerint)* | — | *(a menet szerint)* | `F15_ORKESZTRATOR_BRIEF.md` |

**4.3 A „Munkamenet (tokentakarékos)” szakasz törzsének cseréje** (a címsor marad):

```markdown
1. **Indítás és egyeztetés:** új Code-session, `/kovetkezo`. Egy session = egy feladat. A parancs javaslatot tesz a következő végrehajtható feladatra, és veled egyezteti (feladatválasztás, hatókör, modell). Addig semmit nem ír és nem indít; csak a kifejezett „mehet” után futtat.
2. **Egy feladat = egy brief = egy ág.** A brief a repóban van. Neve a feladat kétjegyű számával kezdődik: `F<nn>_<NEV>_BRIEF.md` (pl. `F05_SZOTAR_BRIEF.md`). A fejlécében a feladat száma és a `Modell:` sor (`sonnet` | `opus` | `haiku` | `külső:<név>`). Brief nélkül a feladat nem indul.
3. **Modellkiosztás:** orkesztrátor Sonnet; végrehajtás a brief szerint (szkript- és adatmunka Sonnet, kutatói ítélet Opus, takarítás Haiku, a Thayer-fordítás a rögzített külső modellel); ellenőr mindig Opus.
4. **Ellenőrzés (gépi):** zöld CI és a `fuggetlen-ellenor` jelentése (`naplok/ELLENOR_*.md`) a kötelező ellenőrzőlistával. Második szem a chat helyett: friss Code-session vagy PR-review.
5. **Döntés:** a ⛔ pontok és a hiányzó briefek a `DONTESEK.md`-be kerülnek. A chat csak ezt a fájlt kapja (raw link); rutinszerű „kész” jelentés nem megy a chatbe.
6. **Merge:** te indítod, zöld CI és `TISZTA` ellenőri jelentés mellett a chat nélkül is. A merge-commit a sort ✅-ra állítja, és a „Kész” listába mozgatja.
7. **Keret és hossz:** ha a keret fogy vagy a session hosszú, a parancs tiszta ponton megáll („Folytatási pont” a zárójelentésben); a következő `/kovetkezo` onnan folytatja.
```

**4.3a Takarítás szakasz** — új pont a lista végére:

- A meglévő briefek átnevezése `F<nn>_…_BRIEF.md` formára `git mv`-vel (a történet megmarad), a hivatkozások frissítésével (`FELADATOK.md` „Hol” oszlop, `CLAUDE.md`, más briefek, CI-konfiguráció, szkriptek: `grep -rn "_BRIEF.md"`). Feladathoz nem köthető brief nem kap számot. Modell: haiku.

**4.4 Jelmagyarázat** — új sor: „**DONTESEK.md:** a nyitott döntések sora; 🟡 nyitott · 🟢 eldöntve · ✅ alkalmazva”.

**4.5 Döntésnapló** — új sorok a D5 után:

| D6 | Orkesztrátor igen, de Claude Code-parancsként (`/kovetkezo`), döntési ponton megállva; a D2-t módosítja | a meglévő eszközökre épül (CLAUDE.md, subagentek, CI), az előfizetésen belül fut, egy session egy feladat, így nem hízik | külön ügynök-rendszer (API, karbantartás); teljes autonómia (a ⛔ pontok szakmai döntések, a hibák a kritikus úton halmozódnak) |
| D7 | A chat csak döntéskor kap jelzést, a `DONTESEK.md`-n keresztül | a chat adat nélkül ellenőrizne: drága és gyenge (TBESH-szűrés tanulsága) | minden zárójelentés bemásolása a chatbe |
| D8 | Második szem: `fuggetlen-ellenor` (Opus) kötelező ellenőrzőlistával, szükség esetén friss Code-session | tiszta kontextus, közvetlen adathozzáférés | a chat mint ellenőr; külső session-verziózó eszközök (Agent-Git, agit) |
| D9 | A végrehajtó modellt a brief `Modell:` sora írja elő | a modellválasztás a felhasználónál marad; a költség oda megy, ahol szakmai ítélet kell | az orkesztrátor maga választ |
| D10 | A brief neve a feladat számával kezdődik: `F<nn>_<NEV>_BRIEF.md` | a brief a fájllistában és az orkesztrátor számára is egyértelműen a feladathoz köthető | szám csak a brief fejlécében |
| D11 | Az orkesztrátor futtatás előtt mindig egyeztet: javaslat → kérdés/módosítás → kifejezett „mehet”; az egyeztetésig csak olvas | a feladatválasztás és a hatókör a felhasználó döntése; az automatikus indulás rossz feladatot vagy rossz hatókört futtathat | a parancs automatikusan indul, csak a tervet írja ki |

**4.6 A #2 (CI) sor** — a „Következő lépés” végére: „+ E17 (sorszám-változás küszöb, lásd `DONTESEK.md`)”.

## 5. `CLAUDE.md`

A meglévő menetzárás-szabály alá új sor: „A munkát a `/kovetkezo` parancs indítja. Egy session = egy feladat. Tartalmi döntésnél tétel a `DONTESEK.md`-be, majd megállás. Merge csak a felhasználótól. Új brief neve: `F<nn>_<NEV>_BRIEF.md`.”

## 6. Zárás

1. `fuggetlen-ellenor` futtatása → `naplok/ELLENOR_orkesztrator-15.md`.
2. Zárójelentés → `naplok/orkesztrator-15_zaras.md` (≤20 sor): elkészült fájlok, a 3.5 szintaxis-eltérései, a `DONTESEK.md` kezdő tételeinek száma.
3. Push, draft PR a main-be.
4. Válasz a felhasználónak: első sor PR-link + CI-állapot, utána legfeljebb 5 sor.

**Próbafuttatás a merge után:** új session, `/kovetkezo`. Elvárt eredmény: a parancs kiírja a tervét egy konkrét feladatra, vagy megnevezi, melyik `DONTESEK.md`-tétel blokkolja a kritikus utat.

## 7. Ütközés más ágakkal

A SZOTAR S1 ága (#5) is módosítja a `FELADATOK.md`-t (a saját sorát). Ez az ág más sorokhoz nyúl; merge-kor a #5 sorának a S1 ágon lévő változata marad érvényes.

## Döntésnapló (a brief verziói)

| Verzió | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| v1 | Az orkesztrátor Code-parancs, nem külön rendszer; terv után „mehet” jóváhagyás | a felhasználó kezében marad az indítás, olcsó kapu | indítás jóváhagyás nélkül |
| v1 | Három végrehajtó subagent modellenként, ha a hívásonkénti modellmegadás nem támogatott | a brief `Modell:` sora így biztosan érvényesül | minden a fő session modelljével fut |
| v1 | Az E17 küszöbe nyitott döntésként indul (javaslat: 1%) | a felhasználó még nem erősítette meg | a küszöb rögzítése a briefben |
| v1 | A külső modellel futó feladatnál Claude csak felügyel | a Thayer-fordítás modellje rögzítve van | Claude-dal helyettesítés |
| v1.1 | A fájlnév elején a feladat száma: `F15_ORKESZTRATOR_BRIEF.md` | a brief a fájllistában is a feladathoz köthető legyen | szám csak a fejlécben |
| v1.2 | Az `F<nn>_` névelőtag általános szabály minden briefre; a meglévők átnevezése a takarítási listára kerül | egységes, a számról kereshető briefek | csak az új briefekre |
| v1.3 | Kötelező egyeztetés a futtatás előtt; az egyeztetésig a parancs csak olvas (DONTESEK-tételt is csak jóváhagyással nyit) | a felhasználó előbb megbeszéli a feladatot; ne induljon automatikusan | terv kiírása után azonnali „mehet”-kapu, egyeztetés nélkül |
