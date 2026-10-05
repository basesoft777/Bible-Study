# KONZISZTENCIA_20261005.md — konzisztencia-jelentés (az első, kézi próbafutás)

*(proveniencia: scope=CLAUDE.md, MUNKAMENET.md, RENDER_BRIEF.md, FELADATOK.md, DONTESEK.md, MUNKATERV.md, F05/F26/F37 briefek, adat/SEMA.md, `python eszkozok/ellenorzes/futtat.py --teljes` | forras=manual (az ügynök-utasítás `.claude/commands/konzisztencia.md` szerint kézzel végigvitt menet, F51 K4) | ts=2026-10-05)*

Ez az **első jelentés**, nincs előző, ezért az „új” szakasz a teljes lista. A jelentés javítást nem végzett; a javaslatok a felhasználó döntésére várnak.

## Új az előző jelentés óta

Nincs előző jelentés: minden találat új (4 kategória, összesen 6 találat; l. alább).

## Összefoglaló

| Kategória | Találat |
|---|---|
| 1. Átvezetetlen döntés | 2 (D34 ↔ `CLAUDE.md`; D34 ↔ `RENDER_BRIEF.md`, `MUNKAMENET.md`) |
| 2. Ütköző azonosítók | 1 (a D-számozás névtér-ütközése; kiemelve a D34) |
| 3. Kettős szóhasználat | 2 („tanulmány”; „törzscikk” vs „motívumcikk”) |
| 4. Régóta álló továbbvivő | 0 (a #11 `brief_kell`, de a D34 5 napos; a határ 2026-10-14) |

## 1. Átvezetetlen döntés

### 1.1 D34 ↔ `CLAUDE.md` rétegtáblája (a kiinduló eset)

- Döntés: `FELADATOK.md:189` / `F26_EGYFORRAS_NAPLO_BRIEF.md:38` — „Motívumonként egy kézi forrás … a motívumcikk (a volt „tematikus tanulmány”), a lexikonoldal és az olvasói nézetek generáltak; a törzscikk a #11-ben megszűnik”.
- Régi állapot: `CLAUDE.md:33` — „**kimenet** — generált | … `lexikon/[ID]_TUDOMANYOS.md`, `lexikon/[ID]_TORZSCIKK.md` | **kézzel szerkeszteni tilos**”; `CLAUDE.md:47` — „A `lexikon/[ID]_TORZSCIKK.md` a lexikonoldalból renderel, önálló forrás nélkül”.
- Miért ütközik: a rétegtábla a törzscikket stabil, generált kimenetként írja, a D34 szerint viszont megszűnik; a „forrás” sor (`CLAUDE.md:32`) a `tematikus_lezart/`-et kézi forrásnak mondja, a D34 szerint a forrás a `motivumok/[ID].md`.
- **Állapot:** a `CLAUDE.md:35` átmeneti jelölést visel („Átmenet (D34) … a #11 lezárásáig érvényes”), tehát **jogos átmenet**, nem hiba. A #26 vitte át; a végleges átírás a #11-é. Gépi jelzés: E25 (JELENTES).
- Javaslat: nincs teendő a `dontes_hatas.tsv`-ben (már benne van, 1. sor). A #11 briefjének tartalmaznia kell a `CLAUDE.md` rétegtábla végleges átírását.

### 1.2 D34 ↔ `MUNKAMENET.md` C1 és a törzscikk-bemutatás

- Régi állapot: `MUNKAMENET.md:67` — „| C1 | lexikon TUDOMÁNYOS szakaszainak + a törzscikk generálása (render) …”; `MUNKAMENET.md:181` — „a **törzscikk** (`lexikon/[ID]_TORZSCIKK.md`, `general.py --cel torzscikk`) a lexikonoldalból renderel”.
- Miért ütközik: a munkamenet-lépés a törzscikk generálását a megszűnő termék állandó lépésének írja; **átmeneti jelölés nincs** a fájlban.
- Javaslat: a #11 átvezeti; addig a gépi szabály FIGYELMEZTETES-t ad (a `dontes_hatas.tsv` 2. és 3. sora). Mérlegelhető egy átmeneti jelölés a `MUNKAMENET.md`-be (külön kis feladat a `/befogad`-on át), hogy a jelzés elnémuljon.

### 1.3 D34 ↔ `RENDER_BRIEF.md` G1 és G7 (kategórián kívül: archív)

- `RENDER_BRIEF.md:69` — „| G1 | Hol élnek a rések? | **A motívum tematikus tanulmányában** …”; `RENDER_BRIEF.md:75` — „| G7 | Törzscikk | `lexikon/[ID]_TORZSCIKK.md` mind a 8 motívumra …”.
- A fájl `tipus: archiv`, `allapot: lezarva`. **Nem találat**: archívumot nem szerkesztünk, a történeti állapot nem hiba (a felhasználó döntése; az E25 a `tipus: archiv` fájlokat általánosan kihagyja). Csak a teljesség kedvéért rögzítve.

## 2. Ütköző azonosítók

### 2.1 A `D<n>` névtér: a D34 (és D1–D42) kétféle jelentéssel

- `F05_SZOTAR_BRIEF.md:356` — „**D34** A héber kiejtés-jelöltekben a begadkefat-spirantizáció …”; `adat/SEMA.md:811` — „### 2.18 … (F05_SZOTAR_BRIEF.md S1.7, D34–D37)”.
- `FELADATOK.md:189` / `F26_EGYFORRAS_NAPLO_BRIEF.md:38` — „| D34 | Motívumonként egy kézi forrás …”.
- Miért ütközik: ugyanaz az azonosító két jelentéssel; a D34–D37, D38–D41 és D42 az F05-ben a brieflokális számozás, a `FELADATOK.md`-ben a globális. Hivatkozás („D34”) fájl nélkül nem egyértelmű; a `CLAUDE.md:35` és a `RENDER_BRIEF`-hivatkozások a globálisat értik, a `SEMA.md` 2.18 a lokálisat.
- Szélesebb kép (K0, `naplok/KONZISZTENCIA_naplo.md`): a számozás **fájlonként újraindul**; az F05 D20–D33-a és minden brief saját D1–D18 tartománya ütközik a `FELADATOK.md` D1–D50-nel.
- A `DT-M1–M6` (`MUNKATERV.md`) és a `DONTESEK.md:94–99` `DT-M1–M6` **nem ütközik**: ugyanazok a döntések (a `DONTESEK.md` rögzíti őket); a `DT-M7–M8` új. A K0 naplóban „ellenőrizendő”-ként szerepelt, ezzel lezárva.
- Javaslat: `DONTESEK.md`-tétel a számozási szabályra (pl. hivatkozáskor mindig `fájl#azonosító`, vagy fájlelőtagos azonosítók); a D-számozás egységesítése az F51 hatókörén kívül van, és a #30 (SZAMOZAS, ⬜) témája is érinti. A `adat/SEMA.md` 2.18 címe pontosítható „F05-D34–D37”-re (külön kis feladat).

## 3. Kettős szóhasználat

### 3.1 „tanulmány”

- `CLAUDE.md:4–5` — „a tanulmányok ennek előállítási folyamata … a kereszthivatkozás adat, a tanulmány és a lexikon pedig ennek az adatnak a nézete”: a **tanulmány itt nézet** (D34 előtti „tematikus tanulmány”).
- `CLAUDE.md:35` — „A „tanulmány” az igeszakasz-tanulmány (kézi forrás), a „motívumcikk” a `motivumok/[ID].md`-ből generált nézet (DT-F26a)”: itt **kézi forrás**.
- `F37_TANULMANY_ELLENORZES_BRIEF.md:25` — „A bővített tanulmány neve mostantól „tanulmány”” (kézi, igeszakasz); `FELADATOK.md:189` (D34): „a tanulmányok (igeszakasz-tanulmányok) önállóak”.
- `MUNKAMENET.md:68` — „a rések megírása **a tanulmányban**”, és `MUNKAMENET.md:111` / `CLAUDE.md:44` — „a motívum tematikus tanulmányából”: itt a **motívumcikk-előd** („tematikus tanulmány”).
- Miért ütközik: a „tanulmány” szó három jelentésben él (igeszakasz-tanulmány, kézi forrás; a motívum tematikus tanulmánya, a D34 szerint generált nézet; a `CLAUDE.md:5` általános „tanulmány = nézet” állítása). A `CLAUDE.md:35` feloldja az átmenetet, de a `CLAUDE.md:5` és `:44`, a `MUNKAMENET.md` és az F37 még nem követi.
- Javaslat: `/befogad`-jelölt: szóhasználati egységesítés (`CLAUDE.md:5`, `:44`, `MUNKAMENET.md:68,111` és az F37 brief), a #11-gyel együtt; addig a `CLAUDE.md:35` az irányadó. Gépi szabályt nem javaslok (nincs egyértelmű regex).

### 3.2 „törzscikk” kontra „motívumcikk”

- `CLAUDE.md:47` — „A `lexikon/[ID]_TORZSCIKK.md` a lexikonoldalból renderel” kontra `CLAUDE.md:35` / D34 — „motívumcikk … a `motivumok/[ID].md`-ből generált nézet; a törzscikk megszűnik”.
- Miért ütközik: a „törzscikk” a ma generált kimenet, a „motívumcikk” a D34 szerinti utód; a két szó különböző termékre mutat, de a dokumentumok néha egymás szinonimájaként használják.
- Javaslat: a #11 definiálja a két fogalmat a `CLAUDE.md`-ben; nincs külön teendő.

## 4. Régóta álló továbbvivő feladat

0 találat. Átnézve: a D34 továbbvivője a #11 (`F11_MIGRACIO_BRIEF.md`, `allapot: brief_kell`). A döntés 2026-09-30-i, a jelentés napján 5 napos; a 14 napos határ **2026-10-14**. A #26 lezárva (`117bafc`, 2026.10.04). Ha a #11 addig nem lép `nem_indult`/`brief_kell` fölé, az E25 (b) ága FIGYELMEZTETES-t ad.

## E25 (gépi réteg) — a `futtat.py --teljes` kimenete

```
## E25 (JELENTES: 3)
- `JELENTES` `CLAUDE.md:33` -- F26_EGYFORRAS_NAPLO_BRIEF.md#D34: a dontes elotti allapot (\[ID\]_TORZSCIKK\.md) 2 helyen -- atmeneti jelolessel
- `JELENTES` `MUNKAMENET.md:67` -- F26_EGYFORRAS_NAPLO_BRIEF.md#D34: a dontes elotti allapot (^\| C1 \| lexikon TUDOMÁNYOS szakaszainak \+ a törzscikk generálása) 1 helyen
- `JELENTES` `MUNKAMENET.md:181` -- F26_EGYFORRAS_NAPLO_BRIEF.md#D34: a dontes elotti allapot (a \*\*törzscikk\*\* \(`lexikon/) 1 helyen
```

(`--teljes` módban minden találat JELENTES; a PR-módban a `MUNKAMENET.md` két sora FIGYELMEZTETES, a `CLAUDE.md` sora JELENTES marad. HIBA-szintű találat nincs.)

## Amit nem vizsgáltam

- A `sablonok/` tartalmát (csak a fájlnevek és a fejlécek szintjén); a `NYITOTT_FELADATOK.md` nagy részét (csak a fejléc); a `genezis/`, `tematikus_lezart/` és `lexikon/` fájlokat.
- A `CLAUDE.md` „`KJV_/ASV_Strongs` csak Genezis, Exodus, Példabeszédek” sorának viszonyát az F19-importhoz (a rendezés az F48-ra vár, függő döntés) és a `sablonok/2_PaRDeS_bovitett_sablon.md:277` `LXX_kivonat_Genezis.tsv` hivatkozását az F42 után: lehetséges jövőbeli, döntéshez kötött `dontes_hatas.tsv`-sorok (KJV/ASV → F19, LXX → F42), most nem vettem fel.
- A `.claude/worktrees/` alatti másolatokat (nem a repó része).

*Futás: a fent idézett fájlok olvasása, `python eszkozok/ellenorzes/futtat.py --teljes`, `python eszkozok/feladatok.py ellenoriz`; az ügynök utasítását (`.claude/commands/konzisztencia.md`) a szerző maga követte kézzel, nem a parancs hívta.*
