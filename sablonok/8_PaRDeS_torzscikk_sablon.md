# 8. Kereszthivatkozási törzscikk sablon (RENDER_BRIEF.md G7)

*v1 — 2026.09.23 (RENDER v4, 1. menet) — a `motivumlog/lexikon_pilot/ISTENTISZT-001_TORZSCIKK.md`
pilot általánosítása mind a 8 motívumra. A pilot D1–D5, D7–D11, D13 döntése
érvényes marad; a D6-ot (régi szerepkör-mátrix) a G6/G7 váltja fel.*

**Kimenet nyelve:** magyar

---

## Mikor és hogyan készül

A törzscikk **nem önálló kutatás** — "render a renderből": a generátor
(`eszkozok/torzscikk_general.py`, `python eszkozok/general.py --cel torzscikk
--ir`) a már megírt lexikonoldalt (`lexikon/[ID]_TUDOMANYOS.md`) olvassa
vissza, és a kereszthivatkozás-fókuszú olvasói nézetét állítja elő
(`lexikon/[ID]_TORZSCIKK.md`). Nem tartalmaz olyan adatot, ami a
lexikonoldalon ne szerepelne; a sorrend és a hangsúly más (a
kereszthivatkozások és a kapcsolatok kerülnek előre, a szótári szócikkek egy
tömör mátrixra egyszerűsödnek).

**Előfeltétel:** a motívumnak legyen `lexikon/[ID]_TUDOMANYOS.md` lexikonoldala
(azaz `elofordulasok.tsv`-ben legalább egy sora).

---

## Szerkezet

1. **Törzsadat-kártya** — ID, cím, UI-címke, téma, azonosság-típus,
   PaRDeS-szint, státusz, igehelyszám (ÓSZ/ÚSZ bontásban), kapcsolatszám, a
   motívum saját Strong-tokenjei ("Fő szavak"), negatív kritérium, fölérendelt
   fogalom — a lexikonoldal Kolofonjából és 1. szakaszából.
2. **Kivonat** — a lexikonoldal kézi Kivonat-résének törzse (helyőrzőnél
   üres, l. lent).
3. **1. Igehelyek és kereszthivatkozások** — a lexikonoldal 1. és 4.
   szakaszának összefésülése: minden igehelynél a Károli-szöveg, a
   kulcsszó/UBS-jelentés, az esetleges LXX-sor, a kapcsolat-nyilak és a
   TSK/Károli-KH találatok együtt. Utána: "Kizárt és vizsgált helyek" (a
   lexikonoldal 1/b. szakasza).
4. **2. Kapcsolatok** — a lexikonoldal 5. szakasza (tábla + Mermaid-ábra) és
   az "Alátámasztás" kézi rés.
5. **3. A kereszthivatkozások minősítése** — a "Minősítés" kézi rés törzse
   változatlanul.
6. **4. LXX-fordítói döntések** — a lexikonoldal 3. szakaszának tömör
   változata (Egyezés-oszlopig, Forrás-oszlop nélkül).
7. **5. Szótári háttér — szerepek és lefedettség** — **G7 szerint ÚJ, nem a
   pilot öröksége**: két mátrix, nem szócikk-próza.
   - **Szerepek** — `adat/szotar_szerepek.tsv` (G6), 10 szerep × 2 nyelv,
     melyik forrás felel meg ma (vagy célként) egy adott kérdéstípusnak.
   - **Lefedettség szavanként** — a motívum saját Strong-tokenjei × a 10
     szerep; a cella értéke forrás-hivatkozás (ha a szerep ma adatosítva),
     `kézi (2/b)` (ha a 2/b kézi rés lefedi — ma csak ISTENTISZT-001-nél,
     a "Megfelelők a másik nyelven" szerepen), vagy `nincs adatosítva`.
8. **6. Értelmezés** / **7. Módszertan és nyitott kérdések** — a megfelelő
   kézi rés törzse változatlanul.
9. **Jelmagyarázat** — közös szöveg, a Funkció-sor a motívum saját
   tanulmányára mutat (nem a lexikonoldal generált szövegére).
10. **Források és licenc** — a Kolofon szűkítve: csak a törzscikkben
    ténylegesen idézett szótárak/adatok (D12/G7) — ha az 5. szakasz nem idéz
    egy forrást (pl. SECE, Mounce, LSJ — ma nincs adatosítva vagy a mátrix
    nem idézi szó szerint), a lábléc sem sorolja fel.

---

## Amit a törzscikk kihagy

- **`<!-- GENERÁLT-KEZDET/VÉGE -->` és `<!-- RÉS-KEZDET/VÉGE -->` markerek**,
  a hatókör-sorok, a forrás-sorok, a lábjegyzet-jelek.
- **`【NAPLO: …】` blokkok** — belső, üzemeltetési feljegyzések, nem az
  olvasónak szólnak.
- **Helyőrző kézi rész** (`*Kézzel írandó…*`, RENDER_BRIEF.md G7) — amíg egy
  rés `forras=lap` és a lexikonoldalon még helyőrző áll, a törzscikk
  megfelelő szakasza üres marad, nem a helyőrző szövegét mutatja.
- **Üzemeltetési bekezdések** — pl. a nyers, gépi adatfájlra mutató
  megjegyzések (`*(A nyers, gépileg…*`).

---

## Ellenőrzés

- `grep -c` a törzscikkben: `GENERÁLT` 0, `【NAPLO` 0, `proveniencia:` 0,
  `Kézzel írandó` 0, `üzemeltet` (kis/nagybetű-független) 0.
- Az ISTENTISZT-001 törzscikke a pilottól **csak** az 5. szakaszban és a
  láblécben térhet el (RENDER_BRIEF.md D18, K9) — a diff nyoma:
  `naplok/RENDER_R1_pilot_diff.tsv`.

---

## Kiejtés — tudatos korlát

A törzscikk a lexikonoldalról öröklött, SBL-stílusú átírásokat (pl.
*epikaleō*) NEM alakítja át magyaros kiejtésre — ez a RENDER_BRIEF.md
hatályán kívül esik (l. "Nincs benne": kiejtés és átírás), a
`SZOTAR_BRIEF.md` S3 tétele oldja meg. A pilot néhány, ISTENTISZT-001-nél
ismert javítást (pl. *epikaleō* → *epikaleó*) megőriz (`torzscikk_general.py`
`KIEJT` táblája), de ez nem általános megoldás.
