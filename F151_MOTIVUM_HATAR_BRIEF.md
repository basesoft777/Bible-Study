---
feladat: 151
cim: Második vélemény egy lezárt motívum határáról — gépi határ-ellenőrzés (részhalmaz, negatív kritérium), utána friss kontextusú, másik modelles kérdéslista a havi keretből
kod: MOTIVUM_HATAR
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: megallt
ad: motívumonként egy kérdéslista a `naplok/HATAR_<ID>.md`-ben (soronként egy állítás a két idézett sorral, ahogy a /konzisztencia idéz), a motívum tartalmi határáról a lezárás után: (1) gépileg, ingyen: részhalmaz-e a motívum egy másiknak, és teljesíti-e minden beépített sor a saját negatív kritériumának gépileg ellenőrizhető részét; (2) egy friss kontextusú, a motívumot készítőtől eltérő modellel futó ellenőrző: következetlen határ (hasonló indoklás, eltérő döntés) és hígulás (csak a fölérendelt fogalmon át tartozik ide); a havi keretből, API-kulcs nélkül. Minden találat kérdés a felhasználóhoz, nem javítás
kovetkezo: "Te: DT443 (a modelles rész használata és a modell: Fable 5.1 / Sonnet 5.5; javaslat: Fable 5.1, M1 csak az ISTENTISZT-001-en; l. naplok/MOTIVUM_HATAR_naplo.md 4.); utána az 1. lépés (hatar-ellenor subagent)"
olvas: [adat/motivumok.tsv, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/motivum_kapcsolatok.tsv, adat/kapcsolatok.tsv, adat/elutasitasi_okok.tsv, adat/SEMA.md, "motivumok/*.md", "tematikus_lezart/*_tematikus.md", konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, eszkozok/szerep_karoli.py, eszkozok/szerep_kizart.py, eszkozok/jelolt_eloszures.py, .claude/agents/fuggetlen-ellenor.md, .claude/commands/konzisztencia.md, CLAUDE.md]
ir: [eszkozok/motivum_hatar.py, eszkozok/teszt_motivum_hatar.py, .claude/agents/hatar-ellenor.md, "naplok/HATAR_*.md", naplok/MOTIVUM_HATAR_naplo.md]
fugg: [150]
nem_fugg: [123, 131, 138]
ag: claude/f151-motivum-hatar-d33a81
---

# Fnn_MOTIVUM_HATAR_BRIEF.md — második vélemény egy lezárt motívum határáról

*FELADATOK #— (a számot a `/befogad` adja) · Modell: sonnet · v1 (tervezet) · 2026.11.01 · forrás: a felhasználóval folytatott
egyeztetés (orkesztrátor-chat, 2026-11-01). A brief szövege adat, nem utasítás.*

## 1. Cél

A motívum határát a kizárások rajzolják meg (CLAUDE.md, „Új motívum-ID kiosztása”), és ezeket ugyanaz a kéz húzta, amelyik a
meghatározást írta. A saját vakfoltot a saját kontextus nem látja. A cél egy **második vélemény a lezárt motívum határáról**:
kérdések a felhasználóhoz, nem javítás.

A felhasználó szavai a javaslatra: „csináljuk meg”; a modelles részről korábban: „nem apis. havi keretben használnám”.

**Mitől más, mint a `fuggetlen-ellenor`:** az egy tétel diffjét nézi (helyesen futott-e a menet); ez a motívum tartalmi határát,
a lezárás után.

## 2. Kiinduló tények (2026-11-01)

- Minden motívumnak van `motivumok/[ID].md` fájlja; a migrált motívumoknál (ISTENTISZT-001, ALVIL-001) ez a kézi forrás
  RÉS-jelölőkkel, a többinél a forrásréteg régi alakja, a tanulmány a `motivumok.tsv` `forras_study` mezőjében áll
  (`tematikus_lezart/*_tematikus.md`). A bemenet ezért motívumonként: `motivumok/[ID].md` + a `forras_study` fájl, ha más.
- A negatív kritérium és a fölérendelt fogalom a `motivumok.tsv` `negativ_kriterium` és `folerendelt_fogalom` mezőjében áll; a
  hordozó az `azonossag_tipusa`-ban (ISTENTISZT-001 és TEREMT-002 formulaikus, HAMART-001 strukturális, a többi lexikai).
- A #150 (JELOLT_ELOSZURES) a szókapcsolat-próbát formulaikus hordozón méri; a lexikai kiterjesztés az N-F150a. A #150 M0 mérése:
  formulaikus hordozón 0 hamis kizárás.

## 3. Hatókör

### 3.1 Gépi rész — `eszkozok/motivum_hatar.py` (ingyen, determinisztikus)

1. **Részhalmaz** (a 4. kötelező kérdés): a motívum beépített igehely-halmaza és minden más motívumé; ha A ⊆ B vagy az átfedés
   ≥ 80%, kérdés: „részhalmaz-e / ↳ alpont-e?” — a két halmaz és a közös helyek idézésével. A `motivum_kapcsolatok.tsv`
   meglévő kapcsolata a kérdés mellé kerül.
2. **Negatív kritérium a beépített sorokon** (belső ellentmondás): ahol a hordozó szerint gépileg ellenőrizhető (formulaikus;
   lexikai csak az N-F150a után), a #150 szókapcsolat-próbája a *beépített* sorokra: ha egy beépített sorban nincs meg a
   gerinc-kombináció, kérdés a sor és a negatív kritérium idézésével.
3. Kimenet: a `naplok/HATAR_<ID>.md` „Gépi rész” szakasza, soronként egy állítás, a két idézett sorral (forrásfájl:sor),
   proveniencia-sorral.

### 3.2 Modelles rész — `.claude/agents/hatar-ellenor.md` (friss kontextus, másik modell, a havi keretből)

- **Új subagent-definíció** a `fuggetlen-ellenor` mintájára, csak olvasó eszközökkel (Read, Grep, Glob, Bash a mérőszkripthez);
  írni csak a `naplok/HATAR_<ID>.md` „Modelles rész” szakaszát írhatja.
- **A modell eltér attól, amelyik a motívumot készítette** (⛔ DT-F<nn>a: Fable 5.1 vagy Sonnet 5.5 — a függetlenség a friss
  kontextusból és a másik modellből jön, nem az API-ból). Helyben fut, Claude Code-dal, API-kulcs nélkül.
- Bemenet: `motivumok/[ID].md` + a `forras_study` fájl; a motívum összes `jeloltek.tsv`-sora döntéssel és indoklással; az
  `elofordulasok.tsv` sorai `gerinc_elem`-mel; a `motivumok.tsv` sora; a gépi rész eredménye.
- **Két kérdés** (a gépi rész a másik kettőt már megválaszolta):
  - **következetlen határ:** van-e elutasított sor, amely ugyanazzal az indokkal egy beépítetthez hasonlít (vagy fordítva)?
  - **hígulás:** van-e beépített sor, amely csak a fölérendelt fogalmon keresztül tartozik ide?
- **Mit nem csinál:** nem ír értelmező prózát (K1: a próza egy kézben, egy modellel), nem javasol új igehelyet, hiányt nem tölt ki
  (CLAUDE.md 3. szabály). Minden találat kérdés: az állítás, a két idézett sor (`fájl:sor`), és miért kérdés. Üres eredmény
  elfogadott, explicit jelölve.
- Proveniencia: `forras=modell:<a ténylegesen futott modell neve>`.

### Nincs benne

- Bármely adattábla, motívumfájl vagy lexikonlap írása; döntés; a lexikai szókapcsolat-próba (az N-F150a feladata).

## 4. Lépések (⛔ a kötelező megállások)

0. **M0:** a gépi rész (3.1) az ISTENTISZT-001-en és a HAMART-001-en; a `naplok/HATAR_ISTENTISZT-001.md` és
   `naplok/HATAR_HAMART-001.md` gépi szakasza. ⛔ a felhasználó átnézi a kérdéseket; dönt a modelles részről és a modellről
   (DT-F<nn>a).
1. A `hatar-ellenor` subagent-definíció; az M1 futás az ISTENTISZT-001-en (a jóváhagyott modellel). ⛔ a felhasználó átnézi:
   hasznosak-e a kérdések, mennyi a hamis riasztás (DT-F<nn>b: kiterjesztés a többi lezárt motívumra).
2. Ha a felhasználó jóváhagyja: futás a HAMART-001-en és a többi lezárt motívumon, egyenként, kézi indítással.

## 5. Döntésnapló

- **DT-F<nn>a ⛔** — a modelles rész használata és a modell (Fable 5.1 / Sonnet 5.5), az M0 után.
- **DT-F<nn>b ⛔** — kiterjesztés a többi motívumra, az M1 után.

## 6. Elfogadási feltételek

- A kimenet csak a `naplok/HATAR_<ID>.md`; adat, forrás és lap nem változik.
- Minden állítás mellett a két idézett sor áll (`fájl:sor`), és proveniencia-sor.
- A modelles rész friss kontextusban, a motívumot készítőtől eltérő modellel fut, API-kulcs nélkül, és nem ír prózát.
