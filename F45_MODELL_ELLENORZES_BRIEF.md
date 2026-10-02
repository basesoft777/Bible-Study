---
feladat: 45
cim: Modell-ellenőrzés minden brief futtatásának elején
kod: MODELL_ELLENORZES
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: nem_indult
ad: minden brief-futtatás (közvetlen és /kovetkezo útján, subagenttel vagy anélkül) az elején ellenőrzi, hogy a ténylegesen futó modell egyezik-e a brief fejlécének `modell` mezőjével, eltérésnél nem dolgozik; az adattáblák `modell` mezőjébe mindig a tényleges modellnév kerül
kovetkezo: végrehajtás a /befogad után
olvas: [CLAUDE.md, BRIEF_SABLON.md, .claude/commands/kovetkezo.md, .claude/commands/befogad.md, .claude/agents/, adat/SEMA.md]
ir: [CLAUDE.md, BRIEF_SABLON.md, .claude/commands/kovetkezo.md, .claude/agents/vegrehajto-opus.md, .claude/agents/vegrehajto-sonnet.md, .claude/agents/vegrehajto-haiku.md, .claude/agents/fuggetlen-ellenor.md]
fugg: []
---

# Fxx_MODELL_ELLENORZES_BRIEF.md — Modell-ellenőrzés minden brief futtatásának elején

*FELADATOK #45 · Modell: sonnet · v1 · 2026.10.02*

## 1. Cél

A BDB-fordítás (#38) briefjének fejlécében `modell: opus` állt, a menet mégis Sonnet-sessionben futott. A fejléc mezője ugyanis csak jelölés, a session modelljét nem állítja. Közben a 269 lefordított sor `modell=claude-opus-5-5` címkét kapott, mert a menet a briefből másolta. Ez a feladat két szabályt vezet be:

1. **Minden brief futtatásának első lépése a modell-ellenőrzés.** Ez minden útra érvényes: közvetlen futtatás (KOZVETLEN_FUTTATAS), `/kovetkezo`, végrehajtó subagent, független ellenőr. A végrehajtó kiírja a saját tényleges modellnevét (pl. `claude-opus-5-5`), és összeveti a brief `modell` mezőjével. Ha eltér, semmilyen munkát nem végez, nem ír és nem commitol. Jelzi az eltérést: „A brief `opus`-t kér, a session `<tényleges név>`; új session kell a kért modellel.”, és megáll.
2. **A `modell` mező az adattáblákban mindig a tényleges modellnév**, amelyet a végrehajtó a saját környezetéből vesz. A briefből vagy korábbi sorból másolni tilos.

## 2. Hatókör

**Benne van:** a `CLAUDE.md`, a `BRIEF_SABLON.md`, a `/kovetkezo` és a végrehajtó/ellenőr subagent-fájlok szabályszövege.
**Nincs benne:** a #38 hibás modellcímkéinek javítása (az a #38 saját menetében történik), CI-szabály.

## 3. Lépések

1. **Modell-ellenőrzés** (ennek a menetnek is ez az első lépése, az 1. cél szerint: a brief `sonnet`-et kér).
2. **`CLAUDE.md`:** új szakasz a „Három szabály, amit soha ne sérts” után, „Modell-ellenőrzés — minden brief futtatásakor” címmel, az 1. cél két szabályával. A meglévő címsorok szövege nem változik.
3. **`BRIEF_SABLON.md`:** a „Nyitó prompt” mintájának első mondata legyen: „Első lépésként írd ki a saját tényleges modellnevedet, és vesd össze a fejléc `modell` mezőjével; eltérésnél ne dolgozz, jelezd, és állj meg.” A `modell` mező táblázatsorához kerüljön egy mondat: „a session modelljét nem állítja, a futtató ellenőrzi”.
4. **`.claude/commands/kovetkezo.md`:** a 6. (VÉGREHAJTÁS) és 6b. lépésben a végrehajtó subagent első teendője a modell-ellenőrzés. Ha a brief subagent nélküli futást ír elő (pl. a #38 D7-es döntése), a session modelljét kell a brief `modell` mezőjével összevetni, és eltérésnél az 5. lépésbeli egyeztetésen jelezni, hogy új session kell.
5. **`.claude/agents/vegrehajto-*.md` és `fuggetlen-ellenor.md`:** a feladatleírás első pontja a modell-ellenőrzés. A független ellenőr ezen felül a zárójelentésében ellenőrizze, hogy a menet által írt `modell` mezők a tényleges modellt mutatják-e.
6. Menetzárás a szokott rendben: `fuggetlen-ellenor`, a jelentés a `naplok/ELLENOR_MODELL_ELLENORZES.md` fájlba, push, draft PR. A záró összefoglaló első sora a PR linkje és a CI állapota.

## 4. Elfogadási feltételek

- A szabály mind az öt helyen (CLAUDE.md, sablon, /kovetkezo, végrehajtó-fájlok, ellenőr) szerepel, egybehangzó szöveggel.
- A menet naplójában az első bejegyzés a saját modell-ellenőrzése.
- Meglévő címsor szövege nem változott.

## 5. Döntésnapló

| # | Döntés | Indok | Elvetett |
|---|---|---|---|
| D1 | Modell-ellenőrzés minden brief futtatásakor, eltérésnél munka nélküli megállás | a #38 Sonneten futott `modell: opus` brieffel, 269 sor hamis címkével (felhasználói döntés, 2026.10.02) | csak a #38-ra szóló ellenőrzés |
| D2 | Az adattáblák `modell` mezője a tényleges modellnév, briefből másolni tilos | a #38 hibás címkéi a briefből másolódtak | — |
| D3 | A szabály öt helyre kerül, nem csak a CLAUDE.md-be | a közvetlen futtatás és a subagent-út más-más fájlt olvas | csak CLAUDE.md |

<!-- KOZVETLEN_FUTTATAS -->
## 0. Nyitó prompt

> Első lépésként írd ki a saját tényleges modellnevedet, és vesd össze a fejléc `modell` mezőjével (`sonnet`). Ha eltér, ne dolgozz, jelezd, és állj meg. Ha egyezik: olvasd be a csatolt briefet, és hajtsd végre a 3. szakasz lépéseit új ágon a `main`-ből; minden lépés után commit és push ugyanarra az ágra.
<!-- /KOZVETLEN_FUTTATAS -->
