---
feladat: 51
cim: Dokumentum-konzisztencia: döntések átvezetésének gépi és ügynöki ellenőrzése
kod: KONZISZTENCIA
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: lezarva
ag: claude/konzisztencia
ad: egy új CI-szabály jelzi, ha egy döntés érintett fájlja még a döntés előtti állapotot írja, vagy a továbbvivő feladata régóta áll; egy naponta, helyi gépen futó ügynök a fogalmi ellentmondásokat jelentésbe gyűjti
kovetkezo: "lezárva; a PR #192 mergelve 2026-10-05; a CI-lépésnév külön tétel (/befogad)"
olvas: [CLAUDE.md, MUNKAMENET.md, RENDER_BRIEF.md, adat/SEMA.md, sablonok/, "F*_BRIEF.md", eszkozok/ellenorzes/, .github/workflows/ellenorzes.yml]
ir: [adat/dontes_hatas.tsv, adat/SEMA.md, eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/futtat.py, eszkozok/ellenorzes/tesztek/, .claude/commands/konzisztencia.md, naplok/KONZISZTENCIA_naplo.md, naplok/konzisztencia/KONZISZTENCIA_20261005.md]
fugg: []
pr: 192
lezarva_osszegzes: E25 CI-szabály + dontes_hatas.tsv (D34, 3 sor) + /konzisztencia parancs; napi helyi ütemezés (konzisztencia-napi) jóváhagyva; merge előtt [ELLENŐRZŐ]-jóváhagyás
helyi_gep: nem
---

# F51_KONZISZTENCIA_BRIEF.md — Döntések átvezetésének ellenőrzése

*FELADATOK #51 · Modell: sonnet · v1 · 2026.10.04*
*v1.1 · 2026.10.05 · Egyeztetett eltérés: a K5 napi (nem heti) futást ír; a „heti” szó a 29. és 87. sorban a v1 szövege.*

## 1. Cél

A 2026.10.04-i chat kiinduló esete: a D34 (F23/F26, 2026.09.30: motívumonként egyetlen kézi forrás, a tematikus tanulmány és a lexikonoldal generált, a törzscikk megszűnik) csak két briefben él. A `CLAUDE.md` rétegtáblája, a `RENDER_BRIEF.md` G1/G7 pontja és a `MUNKAMENET.md` C1 sora a régi rendet írja. A továbbvivő feladat (#26) befogadva, de ⬜, és ezt semmi nem jelezte. Mellékleletként a D34 szám kétszer foglalt: az `adat/SEMA.md` 2.18 a D34–D37-et a szótári kiejtés-döntésekre használja.

A meglévő ellenőrzések (CI E2–E19, `fuggetlen-ellenor`, `/dontes`) egyike sem nézi, hogy egy döntés eljutott-e minden érintett dokumentumba. A feladat két réteget ad:

1. **Gépi szabály (CI):** determinisztikus, minden PR-en lefut, olcsó. Csak azt fogja meg, amit egy táblában előre leírtunk.
2. **Időzített ügynök (helyi, heti):** a táblában nem szereplő, fogalmi ellentmondásokat is keresi (pl. a „tanulmány” szó kettős jelentése az F37 és a D34 között). Csak jelent, nem javít.

## 2. Hatókör

**Benne van:**
- új adattábla: `adat/dontes_hatas.tsv` + SEMA-szakasz;
- új CI-szabály (az utolsó foglalt E-szám után; a #37 az E20–E24-et tervezi, ezért itt **E25**-ként jelölve, a végleges szám az implementáláskor a `szabalyok.py` és a #37 állapota szerint);
- a tábla induló sorai a kiinduló esetből (D34) és a döntésforrásokban talált, ellenőrizhető további döntésekből;
- `.claude/commands/konzisztencia.md`: az ügynök utasítása;
- a helyi ütemezett feladat **terve** (a létrehozás a felhasználó jóváhagyásával, K5).

**Nincs benne:**
- a talált ellentmondások javítása (pl. a `CLAUDE.md` átírása) — az a #26, a #11 és a #37 dolga, vagy új feladat a `/befogad`-on át;
- a D-számozás egységesítése (a D34-ütközés csak jelentésbe kerül, javaslattal);
- felhős futtatás.

## 3. Lépések

### K0 — felmérés (csak olvas)
Gyűjtsd össze, hol élnek ma döntések: `DONTESEK.md`, a briefek „Döntésnapló” táblái (`D<nn>`, `DT-F<nn>-<n>`, `G<nn>`), a `FELADATOK.md` döntésnaplója, `DONTESEK_INDEX.tsv`. Rögzítsd a `naplok/KONZISZTENCIA_naplo.md`-be: forrásonként az azonosító-formát és a sorszámot. **Listázd az ütköző azonosítókat** (pl. D34: F05/SEMA 2.18 kontra F23/F26).

### K1 — `adat/dontes_hatas.tsv` + SEMA
Javasolt oszlopok (a végleges forma a SEMA-szakaszban):

| oszlop | tartalom |
|---|---|
| `dontes_forras` | a döntést rögzítő fájl és azonosító, pl. `F26_EGYFORRAS_NAPLO_BRIEF.md#D34` (a fájl része a kulcsnak, mert a D-számok ütköznek) |
| `datum` | a döntés napja |
| `erintett_fajl` | az a fájl, amelynek a döntést tükröznie kell |
| `tilos_minta` | regex: a döntés előtti állapot; ha a fájlban áll, és nincs mellette `atmeneti_jeloles`, találat |
| `atmeneti_jeloles` | regex: ha a fájlban megvan, a `tilos_minta` találat csak JELENTES (pl. `Átmenet \(D34\)`) |
| `tovabbvivo_feladat` | a `FELADATOK.md` száma, amely a döntést átvezeti (üres, ha nincs) |
| `megjegyzes` | szabad szöveg |

A TSV olvasása/írása `split('\t')` / `'\t'.join()`, a `CLAUDE.md` TSV-szabálya szerint.

### K2 — induló sorok
- D34: `CLAUDE.md` (rétegtábla, törzscikk generált kimenetként), `RENDER_BRIEF.md` (G1, G7), `MUNKAMENET.md` (C1, 139. sor körül) — `tovabbvivo_feladat` 26, illetve 11.
- További sorok csak olyan döntésre, amelynek a régi állapota **regexszel egyértelműen** felismerhető. Ami nem az, az az ügynök dolga (K4), nem a tábláé.

⛔ **Megállás a K2 után:** a sorlista (döntés, fájl, minta) a felhasználó elé kerül jóváhagyásra, mielőtt a szabály élesedik. Ok: a túl tág minta hamis riasztást ad minden PR-en.

### K3 — CI-szabály (E25)
- (a) `tilos_minta` találat az `erintett_fajl`-ban, `atmeneti_jeloles` nélkül → **FIGYELMEZTETES**;
- (b) a `tovabbvivo_feladat` állapota ⬜ / `nem_indult`, és a `datum` óta több mint **14 nap** telt el → **FIGYELMEZTETES**;
- (c) a tábla hivatkozott fájlja vagy azonosítója nem létezik → **HIBA** (a tábla nem avulhat el csendben).
- Fájlszintű szabály (`SZ.FAJLSZINTU_SZABALYOK`), mert a találat nem egy diff-sorhoz kötődik. Tesztek a `tesztek/` alá, a meglévő minta szerint. `--teljes` módban nulla HIBA a jelenlegi `main`-en.

### K4 — `.claude/commands/konzisztencia.md`
Az ügynök utasítása. Csak olvas, egyetlen fájlt ír: `naplok/konzisztencia/KONZISZTENCIA_<ééééhhnn>.md`.
- Beolvassa a döntésforrásokat (K0 listája) és a belépési dokumentumokat (`CLAUDE.md`, `MUNKAMENET.md`, `RENDER_BRIEF.md`, `adat/SEMA.md` fejezetcímei, `sablonok/`), a `CLAUDE.md` „Ezt olvasd, ezt ne” szabályai szerint (az archívumot és a changelogokat nem).
- Lefuttatja az E25-öt `--teljes` módban, és a kimenetét beemeli.
- Keresi: (1) döntés, amely egy belépési dokumentumnak ellentmond, és nincs a `dontes_hatas.tsv`-ben; (2) ütköző döntés-azonosítók; (3) ugyanaz a szó két jelentésben (pl. „tanulmány”); (4) 14 napnál régebben ⬜ továbbvivő feladat; (5) *(2026-10-08, DT-F52g (19))* tervelem feladat vagy brief-tartalom nélkül: a három terv (`ATALAKITASI_TERV.md.md`, `MUNKATERV.md`, `ADATVAGYON_TERV.md`) — ezek a beolvasott döntésforrások közé tartoznak — feladatként, lépcsőként, teendőként vagy döntésként megnevezett eleme, amely nincs FELADATOK-sorban, briefben vagy DONTESEK-tételben, és nincs „elavult”/„feltételes” jelölése.
- Minden találat: idézet mindkét helyről (fájl:sor), egy mondat arról, miért ütközik, és javaslat: `dontes_hatas.tsv`-sor, `/befogad`-jelölt vagy `DONTESEK.md`-tétel. **Javítást nem végez, nem commitol, nem pushol.**
- Ha nincs találat, a jelentés ezt mondja ki (üres eredmény elfogadható kimenet).
- Az előző jelentéshez képest csak az új találatokat emeli ki az elején.

### K5 — helyi ütemezés (terv)
A naplóba: heti egy futás (javasolt: hétfő 9:00), helyi ütemezett feladatként, amely csak akkor fut, ha a gép be van kapcsolva; a kimaradt futás pótlódik a következő bekapcsoláskor. Modell: sonnet. Jelentés kész → értesítés.

⛔ **Megállás a K5 után:** az ütemezett feladat létrehozása a felhasználó jóváhagyásával, külön lépésben.

## 4. Elfogadási feltételek
- `python eszkozok/ellenorzes/futtat.py --teljes` lefut, az E25 a jelenlegi `main`-en legalább a D34 `CLAUDE.md`-sorát jelzi (amíg a #26 nem futott le), HIBA-szintű találat nincs.
- Az E25 tesztjei zöldek; a CI zöld.
- A `/konzisztencia` kézi próbafutása elkészíti az első jelentést, és abban szerepel a kiinduló eset (D34 ↔ `CLAUDE.md`), a D34-számütközés és a „tanulmány” kettős jelentése.
- `python eszkozok/feladatok.py ellenoriz` = 0.

## 5. Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| DT-F51-1 | Két réteg: gépi szabály + ügynök | a gépi szabály biztos, de csak az előre leírtat fogja; az ügynök szélesebb, de tévedhet | csak az egyik |
| DT-F51-2 | Az ügynök helyben fut, ha a gép be van kapcsolva | felhasználói döntés (2026.10.04) | felhős ütemezés |
| DT-F51-3 | Az ügynök csak jelent, nem javít és nem commitol | a javítás tartalmi döntés, az a felhasználóé (`CLAUDE.md`: döntésnél megállás) | önjavító ügynök |
| DT-F51-4 | Az E25 (a) és (b) ága FIGYELMEZTETES, csak a (c) HIBA | a régi állapot átmeneti időszakban jogos lehet; a hibás tábla viszont nem | minden ág HIBA |
| DT-F51-5 | A tábla kulcsa fájl + azonosító | a D-számok ütköznek (D34) | csak azonosító |
| DT-F51-6 | A jelentés helye `.claude/konzisztencia/` (gitignore-olt, helyi), nem `naplok/konzisztencia/`; az előző jelentést mindkét helyen keresi | felhasználói döntés (2026.10.05): a napi rutin commitolatlan jelentése a verziózott mappában megakasztaná a worktree frissítését; a kézi `/konzisztencia` és a rutin ugyanoda ír | jelentés a `naplok/` alá, futás előtti törléssel |

| v | dátum | változás |
|---|---|---|
| v1 | 2026.10.04 | első változat a chatben (kiinduló eset: D34 ↔ `CLAUDE.md` / `RENDER_BRIEF.md` / `MUNKAMENET.md`) |
| v2 | 2026.10.05 | DT-F51-6: a jelentés helye `.claude/konzisztencia/`; a 3. pont `naplok/konzisztencia/` útvonala ennek a döntésnek a régi állapota |
| v3 | 2026.10.08 | DT-F52g (19) (TERV-INTEGRÁCIÓ, kemény zár 2. rétege): a `/konzisztencia` 5. kategóriája (tervelem feladat vagy brief-tartalom nélkül); a három tervdokumentum a beolvasott döntésforrások közé kerül. Ok: a #51 négy kategóriája csak a döntés → dokumentum irányt nézte, a terveket nem olvasta, ezért a terv → feladat rés nem jelzett (`naplok/TERV_INTEGRACIO_leltar.md`). |
