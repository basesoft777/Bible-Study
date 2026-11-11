---
feladat: 189
cim: A /kovetkezo alapesete subagent nélküli végrehajtás, és a CLAUDE.md karcsúsítása
kod: KOVETKEZO_KARCSU
tipus: feladat
fazis: folyamat
modell: opus
allapot: lezarva
ag: claude/teher-kovetkezo-claude-4e1093
pr: 682
ad: a brief egyszer olvasódik (a session hajtja végre, ha a modellje egyezik a briefével), és a minden kérésben betöltődő CLAUDE.md csak szabályokat tartalmaz, a magyarázat a CSAPDAK.md-be kerül
kovetkezo: "Te: a PR #682 átnézése és merge"
munka: folyamat
olvas: [CLAUDE.md, MUNKAMENET.md, BRIEF_SABLON.md]
ir: [.claude/commands/kovetkezo.md, .claude/commands/elteres.md, .claude/agents/vegrehajto-haiku.md, .claude/agents/vegrehajto-opus.md, .claude/agents/vegrehajto-sonnet.md, CLAUDE.md, CSAPDAK.md, MUNKAMENET.md, eszkozok/feladatok.py]
fugg: []
lezarva_osszegzes: a /kovetkezo és a /elteres alapesete a subagent nélküli végrehajtás (DT736); a CLAUDE.md 18 KB-ról 14 KB-ra karcsúsodott, a magyarázat a CSAPDAK.md-ben
---

# F189_KOVETKEZO_KARCSU_BRIEF.md — A /kovetkezo alapesete subagent nélküli végrehajtás, és a CLAUDE.md karcsúsítása

*FELADATOK #189 · Modell: opus · v1 · 2026.11.11*

*Az orkesztrátor indította, külön sessionben. A felhasználó jóváhagyása (2026-11-11): „csináljuk meg”, „csináljuk”, „menjen párhuzamosan”. A brief a szabályos úthoz készült, ugyanezen az ágon; befogadás nélkül, mert a feladatot a felhasználó közvetlenül hagyta jóvá.*

## 1. Cél

A heti keret terhének csökkentése két ponton (mért adat: a felhasználó 7 napos használati képe):

- **A)** A keret 86%-a subagent-nehéz sessionökből jött, ebből a `vegrehajto-opus` 21%. Ma egy feladatot két kontextus olvas végig: előbb a `/kovetkezo` sessionje, aztán a végrehajtó subagent.
- **B)** A `CLAUDE.md` 17 KB, és minden kérésben betöltődik; a mért „always on” teher 14%.

## 2. Hatókör

**Benne van:**
- A) A `/kovetkezo` 6. lépése: ha a session tényleges modellje egyezik a brief `modell` mezőjével, a session maga hajtja végre a briefet, subagent nélkül. Végrehajtó subagent három esetben marad: (1) eltérő modell, ha a felhasználó nem kér új sessiont; (2) csomagmód; (3) `külső:<név>` brief (változatlanul). A `fuggetlen-ellenor` változatlanul subagent; a takarékos szabály is marad (egy független ellenőrzés, legfeljebb egy javítókör). Ugyanez a `/elteres` 4. lépésében. Igazítva: a `CLAUDE.md` „Modell-ellenőrzés” szakasza, a `MUNKAMENET.md` szereposztása, a `vegrehajto-*.md` leírása.
- B) A `CLAUDE.md` hosszú magyarázatai (TSV/csv-csapda, shell, TAHOT, commit-üzenet indoklása, olvasó-szerver tesztjei) egy új fájlba kerülnek: `CSAPDAK.md`. A `CLAUDE.md`-ben a szabály marad, egy-két sorban, hivatkozással. A szakaszcímek megmaradnak, mert kódból és briefekből hivatkoznak rájuk (E27, E36).
- A `CSAPDAK.md` a `feladatok.py` könnyített ellenőrzési listájára kerül, mert a `CLAUDE.md` tartalmát viszi tovább (dokumentáció).

**Nincs benne:** a lexikon, az `adat/` és a generátor; a `.claude/commands/kovetkezo.md` frontmatterjének `model` sora (a modell-ellenőrzés a 6. lépés elején, a ténylegesen futó modellel történik, így nem függ tőle).

## 3. Lépések

1. A brief, `allapot: fut`.
2. A) átírás: `kovetkezo.md`, `elteres.md`, `CLAUDE.md` „Modell-ellenőrzés”, `MUNKAMENET.md`, `vegrehajto-*.md`.
3. B) átírás: `CLAUDE.md` → `CSAPDAK.md`; hivatkozások; szabálylista-összevetés a jelentésbe.
4. Helyi E-ellenőrzés és `python eszkozok/teszt_futtat.py --gyors`.
5. Egy független ellenőrzés, legfeljebb egy javítókör.
6. Jelentés (`naplok/F189_jelentes.md`), draft PR.

## 4. Elfogadási feltételek

- Szabály nem vész el, és nem gyengül; a régi és az új `CLAUDE.md` szabálylistája tételesen össze van vetve a jelentésben.
- A `CLAUDE.md` mérete előtte és utána a jelentésben.
- A helyi E-ellenőrzés és a gyors tesztek zöldek.

## 5. Döntésnapló

- DT736 (🟢, a felhasználó jóváhagyásával, l. a fejléc alatti idézetet; `dontesek/uj/teher-kovetkezo-claude-4e1093.md`): a `/kovetkezo` és a `/elteres` alapesete a subagent nélküli végrehajtás.
