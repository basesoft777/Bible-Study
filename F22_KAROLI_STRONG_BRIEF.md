---
feladat: 22
kod: F22
cim: "Károli–Strong párosítás könyvenként, két modellel (Sonnet + Gemini); első könyv: 1Mózes"
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ag: claude/f22-2moz
ad: "Az 1Mózes minden Károli-szavához az eredeti szó és a Strong-szám, bizonyossági jelöléssel (magas = a két modell egyezik)"
kovetkezo: "Te: a következő könyvek ütemezése (Leviticustól, csak Sonnet)"
fugg: [21]
olvas: [f21p/prompt_v3.md, f21p/prompt_v3.sha256, eszkozok/karoli_strong/tokenek.py, eszkozok/karoli_strong/kapu.py, eszkozok/karoli_strong/futtat.py, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_Strong_kivonat.tsv, f21p/regi_arany_hibas.tsv, naplok/F21P_jelentes.md]
ir: [eszkozok/karoli_strong/futtat.py, eszkozok/karoli_strong/sonnet_koteg.py, eszkozok/karoli_strong/egyesit.py, eszkozok/karoli_strong/zart_osszevet.py, eszkozok/karoli_strong/f22_c_futtat.py, eszkozok/karoli_strong/eredeti_nelkuli_lista.py, naplok/F22_nincs_parja_versek.tsv, adat/karoli_strong/parok_3Moz.tsv, adat/karoli_strong/szavak_3Moz.tsv, f22/minta_3Moz.tsv, f22/valaszok/sonnet/3Moz.jsonl, naplok/F22_3Moz_atnezes.tsv, naplok/F22_3Moz_jelentes.md, naplok/ELLENOR_F22_3Moz.md, eszkozok/karoli_strong/f22_statisztika.py, naplok/F22_2Moz_jelentes.md, naplok/F22_2Moz_atnezes.tsv, f22/minta_2Moz.tsv, f22/valaszok/sonnet/2Moz.jsonl, f22/valaszok/c/2Moz.jsonl, f22/elvetett, f22/minta_2Moz_javito.tsv, f22/valaszok/sonnet/2Moz_javito.jsonl, f22/valaszok/c/2Moz_javito.jsonl, f22/versmegfeleltetes.tsv, naplok/F22_versbeosztas.md, naplok/ELLENOR_F22_2Moz_2.md, eszkozok/karoli_strong/versbeosztas.py, eszkozok/karoli_strong/tokenek.py, eszkozok/karoli_strong/f22_elemzes.py, naplok/ELLENOR_F22_2Moz.md, adat/karoli_strong/parok_2Moz.tsv, adat/karoli_strong/szavak_2Moz.tsv, eszkozok/karoli_strong/f22_arany_kereszt.py, eszkozok/karoli_strong/futtat.py, eszkozok/karoli_strong/egyesit.py, .github/workflows/f22_parositas.yml, f22/futtatas.txt, f22/valaszok/sonnet/1Moz.jsonl, f22/valaszok/c/1Moz.jsonl, f22/futasnaplo.tsv, adat/karoli_strong/parok_1Moz.tsv, adat/karoli_strong/szavak_1Moz.tsv, adat/datasetek.tsv, adat/SEMA.md, naplok/F22_1Moz_jelentes.md, naplok/ELLENOR_F22_1Moz.md]
---

# F22_KAROLI_STRONG_BRIEF.md — Károli–Strong párosítás könyvenként (Sonnet + Gemini)

*FELADATOK #22 · v2 · 2026.10.01 · a v1-et (külső modellpár, a teljes Biblia egy menetben) teljesen felváltja · alap: a #21 pilot eredménye (`naplok/F21P_jelentes.md`) · ág: `claude/f22-1moz` · egy menet egy könyv, két kötelező megállással*

## Mit ad, ha kész

Az 1Mózes (1 533 vers) minden Károli-szavához a megfelelő eredeti (héber) szót és annak Strong-számát, vagy azt, hogy a szó Károli betoldása. Minden eredeti szóhoz azt, hogy Károli lefordította-e. Minden link bizonyossági jelölést kap. Ez az első könyv; a többi könyv ugyanezzel a brieffel fut, a könyv paraméter cseréjével.

## A módszer röviden

Két modell párosít egymástól függetlenül, ugyanazzal a prompttal (`f21p/prompt_v3.md`, befagyasztva):

| | Sonnet | Gemini („C”) |
|---|---|---|
| Hol fut | ebben a Claude Code-sessionben, subagentekkel | GitHub Actions, OpenRouter (`google/gemini-3.8-flash`) |
| Fizetés | a Max-keret | az `OPENROUTER_API_KEY`, kb. 2 USD az 1Mózesre |
| Mért pontosság a pilotban | 97,3% | 95,3% |

Ahol a két modell ugyanazt a linket adja, az `magas` (a pilotban 98,7% pontos). Ahol eltérnek, a Sonnet változata kerül a táblába `alacsony` jelöléssel. A Strong-számot egyik modell sem írja: a szkript veszi a TAHOT-ból a linkelt eredeti szó sorszáma alapján.

## Keretek

- **A modell nem ír Strong-számot**, csak sorszámpárokat (a pilot 5. kapupontja érvényes).
- **A két modell nem látja egymás válaszát.** A Sonnet-subagent nem olvassa az `f22/valaszok/c/` könyvtárat, és fordítva.
- **A prompt nem változik.** A futás előtt a `prompt_v3.sha256` ellenőrzése; eltérésnél megállás.
- **A session egyedül fut**, más Code-session közben nem dolgozik (a keretmérés így tiszta).
- **Számadat** csak szkriptkimenetből kerülhet a jelentésbe.
- **Kulcs:** csak az Actions job `env`-jében; commit előtt kulcs-grep.
- **A zárt licencű Károli–Strong forrás** adata nem kerülhet a repóba, és nem lehet a szótár vagy a párosítás forrása. Csak helyi összevetésre szolgál, és a repóba csak összesített szám mehet.
- **Számkiosztás:** az ágon csak helyőrző (`DT-F22`, `N-F22`), a végleges számot merge után a main-Action adja.

## Lépések

### 22.1 Előkészítés

1. Ág: `claude/f22-1moz` a `main`-ből.
2. `f22/minta_1Moz.tsv`: az 1Mózes összes verse a `Karoli_1908.tsv`-ből, a `tokenek.py` tokenizálásával. Ellenőrzés: 1 533 vers; ha eltér, megállás és jelentés.
3. Kötegek: 10 vers, a könyv sorrendjében (154 köteg). Paraméter: `koteg_meret`; a prófétáknál majd 5.
4. `eszkozok/karoli_strong/sonnet_koteg.py`: egy köteg promptjának előállítása (a `prompt_v3` + a kötegek bemenete, ugyanúgy, mint a `futtat.py`-ban), és a subagent válaszának beolvasása, kapuellenőrzése és mentése az `f22/valaszok/sonnet/1Moz.jsonl`-be. Hibás válasznál egy újrakérés a kapu hibaüzenetével; másodszor `kapuhiba`.
5. `.github/workflows/f22_parositas.yml`: a pilot workflow mintájára (a `futtat.py` újrahasználva), `--konyv 1Moz`, `prompt_v3`, a C beállításai a pilot szerint (minimális gondolkodás). Indítás push-ra, ha az `f22/futtatas.txt` változik. Plafon: **4,00 USD**, megállási küszöb 3,90.

### 22.2 Próbaszakasz: 1Móz 1–5 (138 vers, 14 köteg)

1. A futás előtt jegyezd fel a `/usage` állását (a heti keret %-a).
2. Sonnet: a 14 köteg `vegrehajto-sonnet` subagentekkel, kötegenként egy subagent, sorban.
3. C: trigger az `f22/futtatas.txt`-ben, csak az 1Móz 1–5 kötegeire.
4. A futás után jegyezd fel újra a `/usage` állását.
5. Jelentés (`naplok/F22_1Moz_jelentes.md`, 1. szakasz): kapuhiba első próbára és végleg (mindkét modell), a C költsége, a `/usage` fogyása, és vetítés a teljes 1Mózesre (×1 533/138).

**⛔ 1. megállás**, ha bármelyik teljesül:
- az 1Mózesre vetített keretfogyás a heti keret **30%-a** fölött van;
- a Sonnet végleges kapuhibája 5% fölött van;
- a C költségének vetítése 3,90 USD fölött van.

Ha egyik sem teljesül, a jelentés után **megállás nélkül** folytatódik a 22.3.

### 22.3 A könyv többi része: 1Móz 6–50 (1 395 vers, 140 köteg)

1. Ugyanaz, mint a 22.2: Sonnet a Code-ban, C az Actionsben.
2. Ha a heti keret fogyása (a `/usage` szerint) a futás közben eléri a **30%-ot a menet kezdetéhez képest**, a session a kötegek között megáll, commitol, és jelzi, honnan kell folytatni. A következő héten ugyanebből a briefből folytatható (a már kész kötegeket kihagyja).
3. A futás újraindítható: a már mentett kötegeket mindkét oldal kihagyja.

### 22.4 Egyesítés és táblák

`eszkozok/karoli_strong/egyesit.py` (API nélkül, determinisztikus):

**`adat/karoli_strong/parok_1Moz.tsv`**, linkenként egy sor:

| Oszlop | Tartalom |
|---|---|
| `vers` | pl. `1Móz 1:1` |
| `hu_sorszam`, `hu_szo` | a Károli-token |
| `er_sorszam`, `er_szo` | az eredeti token (TAHOT) |
| `strong` | a TAHOT-ból, a szkript veszi |
| `bizonyossag` | `magas` / `alacsony` / `kezi` |
| `forras` | `S+C` (egyezés) / `S` (csak Sonnet) / `C` (csak C) |

**`adat/karoli_strong/szavak_1Moz.tsv`**, tokenenként egy sor: minden Károli-token és minden eredeti token állapota (`parositva` / `betoldas` / `forditatlan`), bizonyossággal.

**Bizonyossági szabály:**
- `magas`: mindkét modell ugyanazt a linket adta, vagy ugyanazt a `betoldas`/`forditatlan` döntést hozta.
- `alacsony`: a két modell eltér; a Sonnet változata kerül a táblába, `forras: S`.
- Ha csak az egyik modell ment át a kapun: annak változata, `alacsony`, `forras: S` vagy `C`.
- `kezi`: mindkét modell kapuhibás; a vers az átnézési sorba kerül (`naplok/F22_1Moz_atnezes.tsv`), linkek nélkül.

**Lefedettségi ellenőrzés:** minden Károli-token és minden eredeti token pontosan egyszer szerepel a `szavak_1Moz.tsv`-ben; a `strong` oszlop minden értéke levezethető a TAHOT-ból (gépi ellenőrzés).

### 22.5 Ellenőrzés a könyvön

A jelentés 2. szakasza, csak szkriptkimenetből:

1. **Arányok:** `magas`, `alacsony`, `kezi` aránya (linkek és szavak szerint), fejezetenként is.
2. **Régi arany:** a `Karoli_Strong_kivonat.tsv` 1Mózes-sorainak egyezése (halmazként, az összetett Strongot bontva), külön a `magas` linkekre. Az `f21p/regi_arany_hibas.tsv` sorai csak tájékoztatásul kizárva; a mért érték a kizárás nélküli.
3. **A 20 leggyakoribb eltérés-típus** az `alacsony` linkekből (melyik magyar szó, melyik két Strong-jelölt), mintapéldával.

### 22.6 Független szúrópróba (a felhasználó végzi, helyben)

1. `eszkozok/karoli_strong/zart_osszevet.py`: beolvas egy **repón kívüli** szövegfájlt (a zárt licencű forrásból kimásolt versek, soronként egy vers, inline Strong-számokkal), és összeveti a `parok_1Moz.tsv`-vel:
   - versszinten: a Strong-számok halmaza versenként;
   - szószinten: ahol a magyar szó betűre egyezik;
   - a vesszővel kapcsolt pár második tagja (pl. `5647, 8799` → `8799`) igealak-kód, eldobandó; héberben a 8674 fölötti számok is.
2. A kimenet csak összesített szám (egyezés %, n), külön a `magas` és az `alacsony` linkekre. Versenkénti tartalom nem kerülhet a repóba, és a bemeneti fájl útvonala ne legyen beégetve (parancssori paraméter).
3. A szkript a menetben elkészül és mintaadaton tesztelve van; a felhasználó a saját gépén futtatja, és az összesítést bemásolja a jelentésbe.

**⛔ 2. megállás:** a jelentés és az ellenőri kör után, merge előtt. A felhasználó dönt a 2Mózes indításáról.

### 22.7 Zárás

1. `fuggetlen-ellenor`, jelentés: `naplok/ELLENOR_F22_1Moz.md`.
2. Push, draft PR a `main`-be. A záró összefoglaló első sora a PR linkje és a CI állapota.
3. A `FELADATOK.md` #22 sorát nem kézzel írod; a brief fejlécének `allapot` mezője adja.

## Kész, ha

- **K1** Az 1Mózes 1 533 verse feldolgozva; a `szavak_1Moz.tsv` minden Károli- és eredeti tokent pontosan egyszer tartalmaz.
- **K2** A `strong` oszlop minden értéke a TAHOT-ból levezethető (gépi ellenőrzés), modell által írt Strong-szám nincs.
- **K3** A `prompt_v3` hash-e a futás elején és végén egyezik.
- **K4** A jelentés tartalmazza: kapuhiba, `magas`/`alacsony`/`kezi` arány, régi arany egyezés, a C költsége, a `/usage` fogyása.
- **K5** A C költsége a 4,00 USD-s plafon alatt, a futásnapló szerint.
- **K6** A `zart_osszevet.py` mintaadaton tesztelve; a repóban nincs a zárt forrásból származó versenkénti adat.
- **K7** Az újraépítés (`egyesit.py`) API-hívás nélkül ugyanazt a két táblát adja.
- **K8** `ELLENOR_F22_1Moz.md` TISZTA, CI zöld.
- **K9** A két új tábla bejegyezve az `adat/datasetek.tsv`-be és az `adat/SEMA.md`-be.

## Mi nincs benne

- A szkriptes előpárosítás (szótár, tövesítés): a 2Mózestől kerülhet be, külön döntéssel, az 1Mózes `magas` linkjeiből építve.
- A KJV a promptban: a pilot szerint nem igazolt (a zsoltár-eltolódás javítása után újramérhető).
- A próféták és az Újszövetség sajátosságai (5 verses kötegek, TR-kezelés): a megfelelő könyveknél.

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | Könyvenként, az 1Mózessel kezdve | a projekt könyvenként halad; a keret szétterül, minden könyv után mérhető | a teljes Biblia egy menetben (v1) |
| D2 | Sonnet a Code-ban + Gemini (C) az Actionsben | a pilotban a pár `magas` pontossága 98,7%; a Sonnet a Max-keretből fut, készpénzben csak a C kerül pénzbe (kb. 42 USD a teljes Bibliára) | A+B olcsó modellek (elbuktak); Sonnet API-n (kb. 416 USD a párral); C egyedül (bizonyosság nélkül) |
| D3 | Eltérésnél a Sonnet változata, `alacsony` jelöléssel | a Sonnet a pontosabb (97,3% vs. 95,3%); az eltérések kb. 11–12%-át kézzel átnézni nem reális | döntőbíró modell; teljes kézi átnézés |
| D4 | Keretszabály: a menet legfeljebb a heti keret 30%-át használja | más munkának is maradjon keret; a becslés szerint az 1Mózes kb. 2–9% | nincs korlát |
| D5 | Próbaszakasz az 1Móz 1–5-ön, megállási feltételekkel | a Sonnet a pilotban a kimenet 82%-át gondolkodásra fordította, a valódi keretigény csak mérhető | külön 20 verses keretmérés (a felhasználó nem kért több mérést) |
| D6 | A zárt licencű forrás csak helyi összevetésre | licenc; a repóba csak összesített szám mehet | szótárforrásként vagy aranyként használni |
| D7 | A prompt a `prompt_v3`, befagyasztva | a pilotban mérve; a változtatás új mérést igényelne | v4 a pilot nyitott kérdéseivel |
| D8 | **DT-F22d (helyőrző)** — C-költségplafon könyvenként: a könyv versszáma × (2,27 / 1533) × 1,5 USD, de legalább 1,00 USD (2Móz: 2,69 USD); a futtató csak az adott könyv naplósorait összegzi. Külön összesített felső korlát a teljes #22-re: 60 USD a teljes naplóra, elérésekor megáll. A korábbi 4,00 USD az 1Mózesre szólt; a naplóösszeg az egész naplót számolta, ezért a 2Móz 106. kötegénél megállt (felhasználói döntés, 2026.10.01) | a költségvédelem maradjon, de ne a könyvek összegét korlátozza; az 1Móz mért költsége az alap | a 4,00 USD az összesített naplóra (a 2Móz nem fejezhető be) |
| D9 | **DT-F22c (helyőrző) — a 3Móz csak Sonnettel** (felhasználói döntés, 2026.10.02): a C (Gemini) a 3Mózesnél kimarad; minden link `alacsony`, `forras: S`; a tábla proveniencia-sora `ts=manual`; a Gemini-döntés (DT-F22c) nyitva | költség és keret: csak a Sonnet fogy; a bizonyosság-jelölés a C-futással pótolható | a két modell a 3Mózesre is (D2) |

## Döntésnapló (a brief verziói)

| Verzió | Dátum | Változás | Indok |
|---|---|---|---|
| v1 | 2026.09.30 | első változat: teljes Biblia, három külső modell (A, B, döntőbíró C), Opus-arany, KJV-import, pilot ⛔ | a felhasználó kérése (teljes feldolgozás) |
| v2 | 2026.10.01 | v1 (három külső modell, a teljes Biblia) felváltva v2-vel, a #21 pilot eredménye alapján | a pilot mért pontossága: Sonnet 97,3%, Gemini 95,3%, a pár `magas` linkjei 98,7% |
| v2.3 | 2026.10.02 | a 3Móz menete csak Sonnettel (D9, DT-F22c helyőrző); a `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve a 3Mózessel; a csak-Sonnet ág az egyesítőben | a felhasználó utasítása a #114 ágán |
| v2.2 | 2026.10.01 | versbeosztás-detektor (`versbeosztas.py`, `f22/versmegfeleltetes.tsv`, `naplok/F22_versbeosztas.md`): a futtató a megfeleltetett eredeti verset kapja, ahol nincs megfeleltetés, ott `kezi`; a 2Móz 35:36–36:37 javító menete (`2Móz_javito`); a 3Móz csak a detektor eredményének jóváhagyása után indul | a felhasználó utasítása a PR #114 merge előtt |
| v2.1 | 2026.10.01 | a 2Móz menete: D8 (DT-F22d helyőrző: könyvenkénti C-költségplafon + 60 USD összesített korlát), a Károli-kulcs szerinti páratlan versek `kezi` kezelése, `f22/kezi_versek_<könyv>.tsv` (versszámozás-eltolódás) | a 2Móz C-futása a 106. kötegnél az összesített plafonba ütközött; a 2Móz 35:36–36:37 eltolódása (ellenőri kör) |

<!-- KOZVETLEN_FUTTATAS -->
## Nyitó prompt (Code-session)

> A feladat: FELADATOK #22, Károli–Strong párosítás, első könyv: 1Mózes. A brief: `F22_KAROLI_STRONG_BRIEF.md` a repó gyökerében (v2, a v1-et teljesen felváltja). Ez a session egyedül fut, más Code-munka közben nincs.
>
> Ág: `claude/f22-1moz` a `main`-ből. Futtasd a 22.1–22.7 lépéseket. A 22.2 után az ⛔ 1. megállás feltételeit ellenőrizd: ha egyik sem teljesül, jelentés után megállás nélkül folytasd a 22.3-mal. A 22.3 alatt figyeld a `/usage`-t: a menet kezdetéhez képest 30% fogyásnál a kötegek között állj meg, commitolj, és jelezd, honnan kell folytatni. A 22.7 után az ⛔ 2. megállás: jelentés, ellenőri kör, draft PR, és várj a döntésemre.
>
> A Sonnet-kötegeket `vegrehajto-sonnet` subagentek végzik, kötegenként egy, és nem látják a C válaszait. A C-t az Actions futtatja. Minden lépés után commit és push. Számot csak szkriptkimenetből írj a jelentésbe.
<!-- KOZVETLEN_FUTTATAS -->
