# RENDER_R08_jelentes.md — R0.8 kiegészítő felmérés

*2026.09.23 · a RENDER_BRIEF.md v3 R0.8 szakaszának lezáró jelentése*

## 1. §0 újramérés (R0.8.1)

| # | Mérés | Brief várt érték | Mért érték | Eredmény |
|---|---|---|---|---|
| 0.1 | `main` = `origin/main` | az imént készült commit (RENDER_BRIEF.md v3 + SZOTAR_BRIEF.md v1) | `main` = `6a87818` (a két v3/v1-commit után); `origin/main` = `d0a5aa1` (a két új commit még nincs pusholva) | **lásd megjegyzés** |
| 0.2 | `ellenoriz.py` összesítő | RENDBEN 8 · SÉRTÉS 0 · KÉZI 3 · JELENTÉS 1, kód 0 | ugyanez (RENDBEN 8, SÉRTÉS 0, KÉZI 3, JELENTÉS 1, kilépőkód 0) | egyezik |
| 0.3 | `general.py --cel lexikon --ellenoriz` | 8/8 „változatlan lenne" | 8/8 | egyezik |
| 0.4 | lexikonoldalak | 8 (`lexikon/*_TUDOMANYOS.md`), mind 10 generált blokkal | 8 fájl megvan | egyezik |

**Megjegyzés a 0.1-hez:** a brief 15. sora ("Push csak külön kérésre") és a `CLAUDE.md` ("push csak kérésre") szerint a két R0.8-commit (`RENDER_BRIEF.md v3` = `87f42f8`, `SZOTAR_BRIEF.md v1` = `6a87818`) nem lett pusholva — ez szándékos, nem eltérés. `origin/main` (`d0a5aa1`) a `main` őse (nincs divergencia, nincs force-push-igény, nincs idegen commit `origin`-on), csak 2 committal le van maradva. Ez pontosan ugyanaz a mintázat, mint a `RENDER_R0_jelentes.md` 0.1 sorában (`2eea2c2` — "a brief-commit előtt"), ezért **nem blokkoló eltérés**, de a R0.8.1 "ÁLLJ MEG, ha bármi eltér" utasítása szó szerint véve teljesülne egy eltéréssel — jelezve, folytattam.

**Következtetés:** nincs blokkoló eltérés.

## 2. Szakasz-leltár (R0.8.2)

`naplok/RENDER_R08_szakaszok.tsv` — 111 sor (8 tanulmány összesen, motívumonként 8–20 fejléc, `#`/`##`/`###` szinten), oszlopok: `id`, `fajl`, `fejlec_szint`, `fejlec`, `bajtmeret_a_kovetkezo_fejlecig`. A blokkhatár a következő fejlécig (bármely szintig) tart.

Szerkezeti megfigyelés: a 8 tanulmány **nem egységes** a `4_PaRDeS_tematikus_sablon.md` verziói szerint (v12/v14 keveredik, l. az egyes tanulmányok alcímsorai), és a "Minőségi kapu" / "6. Napló-frissítés" sorrendje **motívumonként eltér** — négy tanulmányban (TEREMT, ALVIL, MENNY, HODIT) a Minőségi kapu az 5. és a 6. szakasz közé, illetve a 6. után ékelődik, nem egységes helyen.

## 3. Megfeleltetési javaslat (R0.8.3)

`naplok/RENDER_R08_megfeleltetes.tsv` — 56 sor (8 × 7), oszlopok: `id`, `res`, `fejlec`, `tanulmany_szakaszok`, `hiany`, `megjegyzes`.

**Összesítő `hiany`-eloszlás résenként:**

| Rés | hiany=igen | hiany=nem | Megjegyzés |
|---|---|---|---|
| `kivonat` | 8/8 | 0 | a hipotézis szerint helyesen — G10 új szakaszt hoz létre |
| `2b` | 6/8 | 2/8 | csak TEREMT-001-nél (2/b+2/c) és ALVIL-001-nél (2/b) van meglévő fejléc |
| `miert_fontos` | 0/8 | 8/8 | a "2. Eredeti nyelvi összevetés" fejléc mind a 8 tanulmányban megvan |
| `minosites` | 8/8 | 0 | **egyetlen tanulmányban sincs** önálló "kereszthivatkozások minősítése" fejléc |
| `alatamasztas` | 7/8 | 1/8 | csak ISTENTISZT-001-nél van "1/b. Kapcsolatok" fejléc |
| `ertelmezes` | 0/8 | 8/8 | a "3. A PaRDeS keretrendszer" fejléc mind a 8-nál megvan; ⚠️ Vitatott pontok alcím csak MENNY-001, HODIT-001, HAMART-001-nél |
| `modszertan` | 1/8 | 7/8 | ANTROP-001-nél hiányzik a "0. Forrás-összegyűjtés" szakasz ÉS a Minőségi kapu fejléc is |

A `2. Eredeti nyelvi összevetés` (`miert_fontos`) és a `3. A PaRDeS keretrendszer` (`ertelmezes`) hipotézis **minden tanulmányban megerősítve** (fejléc-szinten). A `minosites` hipotézis (kereszthivatkozások minősítése) **egyetlen tanulmányban sem** igazolódott — ez a legnagyobb eltérés a brief kiinduló hipotéziséhez képest, és minden motívumra érinti (l. kérdések).

## 4. Elavult számok (R0.8.4)

`naplok/RENDER_R08_szamok.tsv` — 17 sor, oszlopok: `id`, `tanulmany`, `sor`, `szoveg`, `tanulmany_ertek`, `adat_ertek`, `hatokor`, `megjegyzes`.

A regex-alapú kandidátumkeresés (`\d+` + igehely/előfordulás/kapcsolat/vers/találat szókörnyezet) 36 sort adott; ebből a valódi számadatot hordozó 17-et tételesen összevetettem az `adat/*.tsv` mai értékeivel (`naplok/RENDER_R08_adat_alapszamok.tsv` — a motívumonkénti összes/ÓSZ/ÚSZ igehelyszám és a kapcsolat-sorszám az `adat/elofordulasok.tsv` és az `adat/kapcsolatok.tsv` mai állapotából).

**Eredmény: nem találtam olyan esetet, ahol a tanulmány prózája a motívum jelenlegi, összesített (`id`-szintű) igehely- vagy kapcsolatszámával ellentmondana az adatnak.** Két konkrét egyezés-igazolás:
- ISTENTISZT-001: 32 igehely (22 ÓSZ / 10 ÚSZ), 25 kapcsolat — a tanulmány LXX-hídelemzésének belső számai (15/17, 31=6+1+24) ezzel konzisztensek, csak szűkebb hatókörűek (a formula LXX-megfelelése, ill. a teljes G1941-korpusz-scan, nem a motívum 32-es alapszáma).
- TEREMT-001: a H8415 teljes ÓSZ-scan "34 egyedi vers" állítása **pontosan** egyezik az `adat/elofordulasok.tsv` 34 ÓSZ-sorával.

A talált 17 sor túlnyomó többsége **más hatókörű szám** (egy adott Strong-szám/lemma teljes ÓSZ- vagy ÚSZ-korpuszbeli előfordulása, nem a motívum szűkített halmaza — pl. HAMART-001 `adamá` 211 igehelye a köznyelvi szó teljes ÓSZ-előfordulása, szemben a motívum 52-es végösszegével), vagy **dátumozott történeti/verziótörténeti utalás** (pl. ALVIL-001 "4→6", ANTROP-001 "ötödik előfordulás felvéve" 2026.08.22-i bejegyzésként, HODIT-001 "1 előfordulásnál tart" a küszöb-esemény leírásaként) — ezek a maguk idejében helyesek voltak, és nem a mai állapotra vonatkozó (ezért nem elavult) állítások.

**Módszertani korlát:** a regex-keresés csak a hét fő kulcsszó (igehely, előfordulás, kapcsolat, vers, találat) közvetlen szám-szomszédságára szűrt; nem zárható ki, hogy van olyan elavult szám, amely más szóval (pl. "db", "tétel", "sor") vagy szám nélkül, szövegesen (pl. "mindhárom") szerepel. Az `1. Előfordulások összegyűjtése` szakaszok elején egyik tanulmány sem tartalmaz explicit "N igehely összesen" nyitómondatot — a táblázat sorai maguk az adat, külön összegző számállítás nélkül, ezért ott nincs mit összevetni.

## 5. ISTENTISZT-001 visszaírási terv (R0.8.5)

`naplok/RENDER_R08_visszairas.tsv` — 7 sor (a 7 rés), oszlopok: `res`, `fejlec`, `hatas`, `erintett_tanulmany_szakasz`, `megjegyzes`.

| Rés | Hatás | Érintett szakasz |
|---|---|---|
| `kivonat` | új | (a tanulmány elejére, G8/G10 szerint) |
| `2b` | új | nincs jelenlegi megfelelő; javasolt hely a 2. és a 3. szakasz között |
| `miert_fontos` | felváltás | 2. Eredeti nyelvi összevetés |
| `minosites` | új | nincs jelenlegi megfelelő; javasolt hely az 1. szakasz után |
| `alatamasztas` | felváltás | 1/b. Kapcsolatok |
| `ertelmezes` | felváltás | 3. A PaRDeS keretrendszer |
| `modszertan` | felváltás, HÁROM cél-szakasz | 0. Forrás-összegyűjtés + 6. Napló-frissítés + Minőségi kapu |

A 7 résből **3 "tiszta" felváltás** (miert_fontos, alatamasztas, ertelmezes), **2 új szakasz** (kivonat, minosites — nincs mit felváltani), **1 új szakasz bizonytalan elhelyezéssel** (2b), és **1 többcélú felváltás** (modszertan — egy rés, három lehetséges célszakasz), amely tényleges döntést igényel jóváhagyás előtt.

## 6. Kérdések — egy csokorban

1. **A `minosites` rés hipotézise (mind a 8 tanulmányra) nem igazolódott.** Egyetlen tanulmányban sincs önálló "kereszthivatkozások minősítése" fejléc. Az R1.2/R1.3 (1. menet) számára ez azt jelenti, hogy mind a 8 motívumnál **új szakaszt** kell nyitni a tanulmányban (a 7 helyőrzős oldalnál egyelőre `forras=lap` marad — G12 —, de a struktúra-kérdés ugyanaz lesz a 2. menetben). Hova kerüljön ez a nyolcszori új szakasz — egységes pozíció (pl. mindig az "1. Előfordulások összegyűjtése" után) kell-e definiálni a `res_forras.tsv`-ben?

2. **ISTENTISZT-001 `2b` rés — hova kerüljön az új szakasz a tanulmányban**, és **teljes egyben menjen-e be az 1. menetben**, tudva, hogy a `SZOTAR_BRIEF.md` S12-je (2. menet, a SZOTAR briefben) ezt utólag szét fogja bontani (a jelentőség-bekezdések átkerülnek a `miert_fontos` alá)? Ha igen, ez azt jelenti, hogy az 1. menetben egy olyan tartalom kerül be, amit a SZOTAR-menet később módosít — ez összhangban van-e a "nulla-diff" elvvel a RENDER 2. menetének végén (amikor a `res_forras.tsv` `lap`→`tanulmany` vált), vagy a `2b` betoldását célszerűbb-e a RENDER 2. menetére halasztani?

3. **ISTENTISZT-001 `modszertan` rés — egy résre három célszakasz.** A lex. oldal 7. szakasza (8263 bájt) egyetlen tömb, a hipotézis viszont a "0. Forrás-összegyűjtés", "6. Napló-frissítés" és "Minőségi kapu" hármasát jelöli meg forrásként/célként. Melyik konkrét megoldást hagyjuk jóvá: (a) a rés egészét egyetlen célszakaszba (javaslat: "6. Napló-frissítés", mert ez a legközelebbi tematikus párja) írjuk vissza, a másik kettőt (0., Minőségi kapu) a study saját, változatlan szövegével hagyva; vagy (b) a rés tartalmát a visszaírás előtt manuálisan szét kell bontani a három szakasz között? A G13 szerint "a study-frissítésről szóló blokk a 2. menetben lezárul" — a jelenlegi 3 NAPLO-blokk közül melyik ez tételesen, azonosítást igényel a R1.2 előtt.

4. **A Minőségi kapu / 6. szakasz sorrendje négy tanulmányban nem egységes** (TEREMT-001, ALVIL-001, MENNY-001, HODIT-001 — a Minőségi kapu hol az 5. után/6. elé, hol a 6. után/Önellenőrzés után ékelődik). Ez nem blokkolja a `modszertan` rés összeállítását (G2 szerint "több tanulmány-szakaszból is állhat, dokumentum-sorrendben, egy üres sorral összefűzve"), de jelzem, mert a `render_resek_kivag.py`-nak (R1.1/R1.3) fejléc-mintára, nem pozícióra kell illesztenie ezt a három komponenst.

5. **A `0.1 (main=origin/main)` mérés szó szerinti értelmezése** (a §0 táblázat "az imént készült commit" oszlopa) minden brief-nyitó commit után eltérést fog mutatni, amíg push nem történik — ez a mintázat már a `RENDER_R0_jelentes.md`-ben is megjelent (2eea2c2 esetén). Érdemes-e a brief §0 tábláját pontosítani úgy, hogy a mérce "origin/main a main őse (nincs divergencia)" legyen, nem a szó szerinti egyenlőség, hogy a jövőbeli nyitó promptok ne generáljanak félreérthető "ÁLLJ MEG" helyzetet minden brief-commit után?

## Munkalapok

- `naplok/RENDER_R08_szakaszok.tsv`
- `naplok/RENDER_R08_megfeleltetes.tsv`
- `naplok/RENDER_R08_szamok.tsv` (+ segédfájl: `naplok/RENDER_R08_adat_alapszamok.tsv`, `naplok/RENDER_R08_szamok_nyers.tsv`)
- `naplok/RENDER_R08_visszairas.tsv`

## Elfogadási kritériumok

- **K4** — teljesítve: a négy munkalap és e jelentés megvan; a kérdések a 6. szakaszban, egy listában.
- **K5** — teljesítve: az R0.8 alatt az éles `adat/`, `lexikon/`, `motivumok/`, `tematikus_lezart/` könyvtárba nem történt írás (csak olvasás és mérés; a `naplok/` írás a brief szerint engedélyezett munkatermék).
