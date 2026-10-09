---
feladat: 22
kod: F22
cim: "Károli–Strong párosítás könyvenként (1–2Móz: Sonnet + Gemini; a 3Móztól csak Sonnet, DT-F22c); első könyv: 1Mózes"
tipus: feladat
fazis: 1
modell: sonnet
allapot: megallt
ag: claude/peaceful-meitner-1vzy4m
ad: "Az 1Mózes minden Károli-szavához az eredeti szó és a Strong-szám, bizonyossági jelöléssel (magas = a két modell egyezik)"
kovetkezo: "Te: az 1Sámuel kész (API, DT73 (a); jelentés: `naplok/F22_1Sam_jelentes.md`; tiszta versbeosztás; végleges kapuhiba 0); a Péld, a Bír, a Jób, az Eszt és a 2Sám a main-en (PR #266, #267); ⛔ 2.: a független ellenőr (`naplok/ELLENOR_F22_1Sam.md`), a szúrópróba elmarad (DT70); kézi átnézés: 2Sám 23:16, Jób 16:22, 36:33, Péld 11:31, korábbról 1Krón 19:2, Ézs 9:20, 64:1, Zsolt 119:94, 144:15, 145:1 (a felhasználóé); a régi arany `Job.17.13` hármasa kulcshibás (javaslat: `f21p/regi_arany_hibas.tsv`, külön tétel); PR, ready és merge (a felhasználóé). A következő könyv a felhasználó döntése: a BDB-mérés (2026.10.09) szerinti tiszta jelöltek 1Kir, Neh, 2Kir; a Dán (37 detektorsor) előtt versbeosztás-döntés kell; **párhuzamos futás csak kifejezett jóváhagyással indulhat (D15, DT60)**."
fugg: [21]
nem_fugg: [48]
olvas: [f21p/prompt_v3.md, f21p/prompt_v3.sha256, eszkozok/karoli_strong/tokenek.py, eszkozok/karoli_strong/kapu.py, eszkozok/karoli_strong/futtat.py, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_Strong_kivonat.tsv, f21p/regi_arany_hibas.tsv, naplok/F21P_jelentes.md]
ir: [naplok/F22_1Sam_jelentes.md, naplok/ELLENOR_F22_1Sam.md, naplok/F22_1Sam_atnezes.tsv, adat/karoli_strong/parok_1Sam.tsv, adat/karoli_strong/szavak_1Sam.tsv, f22/minta_1Sam.tsv, f22/valaszok/sonnet/1Sam.jsonl, f22/api_termeles/high/1Sam.jsonl, naplok/F22_2Sam_jelentes.md, naplok/ELLENOR_F22_2Sam.md, naplok/F22_2Sam_atnezes.tsv, adat/karoli_strong/parok_2Sam.tsv, adat/karoli_strong/szavak_2Sam.tsv, f22/minta_2Sam.tsv, f22/valaszok/sonnet/2Sam.jsonl, f22/api_termeles/high/2Sam.jsonl, naplok/F22_Eszt_jelentes.md, naplok/ELLENOR_F22_Eszt.md, naplok/F22_Eszt_atnezes.tsv, adat/karoli_strong/parok_Eszt.tsv, adat/karoli_strong/szavak_Eszt.tsv, f22/minta_Eszt.tsv, f22/valaszok/sonnet/Eszt.jsonl, f22/api_termeles/high/Eszt.jsonl, naplok/F22_Job_jelentes.md, naplok/ELLENOR_F22_Job.md, naplok/F22_Job_atnezes.tsv, adat/karoli_strong/parok_Job.tsv, adat/karoli_strong/szavak_Job.tsv, f22/minta_Job.tsv, f22/valaszok/sonnet/Job.jsonl, f22/api_termeles/high/Job.jsonl, naplok/F22_versbeosztas.md, naplok/F22_Bir_jelentes.md, naplok/ELLENOR_F22_Bir.md, naplok/F22_Bir_atnezes.tsv, adat/karoli_strong/parok_Bir.tsv, adat/karoli_strong/szavak_Bir.tsv, f22/minta_Bir.tsv, f22/valaszok/sonnet/Bir.jsonl, f22/api_termeles/high/Bir.jsonl, naplok/F22_Peld_jelentes.md, naplok/ELLENOR_F22_Peld.md, naplok/F22_Peld_atnezes.tsv, adat/karoli_strong/parok_Peld.tsv, adat/karoli_strong/szavak_Peld.tsv, f22/minta_Peld.tsv, f22/valaszok/sonnet/Peld.jsonl, f22/api_termeles/high/Peld.jsonl, naplok/F22_Ez_jelentes.md, naplok/ELLENOR_F22_Ez.md, naplok/F22_Ez_atnezes.tsv, adat/karoli_strong/parok_Ez.tsv, adat/karoli_strong/szavak_Ez.tsv, f22/minta_Ez.tsv, f22/valaszok/sonnet/Ez.jsonl, f22/api_termeles/high/Ez.jsonl, naplok/F22_Ezsd_jelentes.md, naplok/ELLENOR_F22_Ezsd.md, naplok/F22_Ezsd_atnezes.tsv, adat/karoli_strong/parok_Ezsd.tsv, adat/karoli_strong/szavak_Ezsd.tsv, f22/minta_Ezsd.tsv, f22/valaszok/sonnet/Ezsd.jsonl, f22/api_termeles/high/Ezsd.jsonl, naplok/F22_2Kron_jelentes.md, naplok/ELLENOR_F22_2Kron.md, naplok/F22_2Kron_atnezes.tsv, adat/karoli_strong/parok_2Kron.tsv, adat/karoli_strong/szavak_2Kron.tsv, f22/minta_2Kron.tsv, f22/valaszok/sonnet/2Kron.jsonl, f22/api_termeles/high/2Kron.jsonl, naplok/F22_1Kron_jelentes.md, naplok/ELLENOR_F22_1Kron.md, naplok/F22_1Kron_atnezes.tsv, adat/karoli_strong/parok_1Kron.tsv, adat/karoli_strong/szavak_1Kron.tsv, f22/minta_1Kron.tsv, f22/valaszok/sonnet/1Kron.jsonl, f22/api_termeles/high/1Kron.jsonl, naplok/F22_Jer_jelentes.md, naplok/ELLENOR_F22_Jer.md, naplok/F22_Jer_atnezes.tsv, adat/karoli_strong/parok_Jer.tsv, adat/karoli_strong/szavak_Jer.tsv, f22/minta_Jer.tsv, f22/valaszok/sonnet/Jer.jsonl, f22/api_termeles/high/Jer.jsonl, naplok/F22_Ezs_jelentes.md, naplok/ELLENOR_F22_Ezs.md, naplok/F22_Ezs_atnezes.tsv, f22/api_termeles/futasnaplo.tsv, f22/api_termeles/batchek.tsv, f22/api_termeles/javitando.txt, f22/api_termeles/high/Ezs.jsonl, f22/api_termeles/high/_munka, adat/datasetek.tsv, adat/SEMA.md, adat/karoli_strong/parok_Ezs.tsv, adat/karoli_strong/szavak_Ezs.tsv, f22/minta_Ezs.tsv, f22/valaszok/sonnet/Ezs.jsonl, f22/versmegfeleltetes_kezi.tsv, naplok/F22_Jozs_atnezes.tsv, naplok/F22_Jozs_jelentes.md, naplok/ELLENOR_F22_Jozs.md, adat/karoli_strong/parok_Jozs.tsv, adat/karoli_strong/szavak_Jozs.tsv, f22/minta_Jozs.tsv, f22/valaszok/sonnet/Jozs.jsonl, naplok/F22_versbeosztas_jovahagyas.md, naplok/ELLENOR_F22_5Moz.md, eszkozok/karoli_strong/futtat.py, eszkozok/karoli_strong/sonnet_koteg.py, eszkozok/karoli_strong/egyesit.py, eszkozok/karoli_strong/zart_osszevet.py, eszkozok/karoli_strong/f22_c_futtat.py, eszkozok/karoli_strong/eredeti_nelkuli_lista.py, naplok/F22_nincs_parja_versek.tsv, adat/karoli_strong/parok_5Moz.tsv, adat/karoli_strong/szavak_5Moz.tsv, f22/minta_5Moz.tsv, f22/valaszok/sonnet/5Moz.jsonl, naplok/F22_5Moz_atnezes.tsv, naplok/F22_5Moz_jelentes.md, adat/karoli_strong/parok_4Moz.tsv, adat/karoli_strong/szavak_4Moz.tsv, f22/minta_4Moz.tsv, f22/valaszok/sonnet/4Moz.jsonl, naplok/F22_4Moz_atnezes.tsv, naplok/F22_4Moz_jelentes.md, naplok/ELLENOR_F22_4Moz.md, f22/versosszevonas.tsv, naplok/F22_versbeosztas_jovahagyas.md, adat/karoli_strong/parok_3Moz.tsv, adat/karoli_strong/szavak_3Moz.tsv, f22/minta_3Moz.tsv, f22/valaszok/sonnet/3Moz.jsonl, naplok/F22_3Moz_atnezes.tsv, naplok/F22_3Moz_jelentes.md, naplok/ELLENOR_F22_3Moz.md, eszkozok/karoli_strong/f22_statisztika.py, naplok/F22_2Moz_jelentes.md, naplok/F22_2Moz_atnezes.tsv, f22/minta_2Moz.tsv, f22/valaszok/sonnet/2Moz.jsonl, f22/valaszok/c/2Moz.jsonl, f22/elvetett, f22/minta_2Moz_javito.tsv, f22/valaszok/sonnet/2Moz_javito.jsonl, f22/valaszok/c/2Moz_javito.jsonl, f22/versmegfeleltetes.tsv, naplok/F22_versbeosztas.md, naplok/ELLENOR_F22_2Moz_2.md, eszkozok/karoli_strong/versbeosztas.py, eszkozok/karoli_strong/tokenek.py, eszkozok/karoli_strong/f22_elemzes.py, naplok/ELLENOR_F22_2Moz.md, adat/karoli_strong/parok_2Moz.tsv, adat/karoli_strong/szavak_2Moz.tsv, eszkozok/karoli_strong/f22_arany_kereszt.py, eszkozok/karoli_strong/futtat.py, eszkozok/karoli_strong/egyesit.py, .github/workflows/f22_parositas.yml, f22/futtatas.txt, f22/valaszok/sonnet/1Moz.jsonl, f22/valaszok/c/1Moz.jsonl, f22/futasnaplo.tsv, adat/karoli_strong/parok_1Moz.tsv, adat/karoli_strong/szavak_1Moz.tsv, adat/datasetek.tsv, adat/SEMA.md, naplok/F22_1Moz_jelentes.md, naplok/ELLENOR_F22_1Moz.md, adat/karoli_strong/parok_Zsolt.tsv, adat/karoli_strong/szavak_Zsolt.tsv, f22/minta_Zsolt.tsv, f22/valaszok/sonnet/Zsolt.jsonl, naplok/F22_Zsolt_atnezes.tsv, naplok/F22_Zsolt_elokeszites.md, naplok/F22_Zsolt_elofutas.md, naplok/F22_Zsolt_jelentes.md, naplok/ELLENOR_F22_Zsolt.md]
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
- A próféták és az Újszövetség sajátosságai (a prófétáknál 10 verses kötegek, DT71 (a); TR-kezelés): a megfelelő könyveknél.

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
| D9 | **DT-F22c (helyőrző) — a 3Móz csak Sonnettel** (felhasználói döntés, 2026.10.02): a C (Gemini) a 3Mózesnél kimarad; minden link `alacsony`, `forras: S`; a tábla proveniencia-sora `ts=manual`; a Gemini-döntés (DT-F22c) lezárva (✅; l. a `DONTESEK.md` DT-F22c sorát) | költség és keret: csak a Sonnet fogy; a bizonyosság-jelölés a C-futással pótolható | a két modell a 3Mózesre is (D2) |
| D10 | a 4Móz csak Sonnettel (DT-F22c lezárva, mint a 3Móz); a 4Móz 29:39 utolsó mondata = TAHOT 30:1: kézi 1:2 beolvasztás, `kezi` (nem `betoldas`); `f22/versosszevonas.tsv`; heti keret 85%-nál megállás a köteg végén (felhasználói döntés, 2026.10.02) | az 1:2 támogatás a párosításban nincs; a kézi jóváhagyás naplózva | 1:2 támogatás most (a Jób-döntésig halasztva) |
| D11 | az 5Móz csak Sonnettel (DT-F22c lezárva); a detektor szerint tiszta (959/959, K-hiány 0, E-hiány 0), nincs kézi beolvasztás; heti keret 85%-nál megállás a köteg végén (felhasználói döntés, 2026.10.02) | ugyanaz a menet, mint a 3–4Mózesnél; a heti keret a menet elején 76% (a 70%-os szabály felett, a felhasználó tudatos jóváhagyásával) | várás a heti keret nullázódására |
| D12 | a Józs csak Sonnettel (DT-F22c lezárva); a detektor szerint tiszta (658/658 vers, 24 fejezet, K-hiány 0, E-hiány 0), nincs kézi beolvasztás; heti keret 85%-nál megállás a köteg végén (felhasználói döntés, 2026.10.04, chat: „mehet a Józsué”) | ugyanaz a menet, mint a 3–5Mózesnél; a heti keret a menet elején 9% | két modell (D2) |
| D13 | **DT54** — a Józsué után a Zsoltárok következik, utána a kanonikus sorrend (Bír, …) (felhasználói döntés, 2026-10-07, (b)); a #38 7. adagja nem vár rá | a #38 BDB-adatblokkjának Károli-szakasza csak a kész könyvekből él; a 7. adagban a NINCS/kevés szócikkek előfordulása Zsolt 741 / Bír 187, a hátralévő sorban Zsolt 3 172 / Bír 1 029 (`naplok/F22_DT54_zsoltarok_javaslat.md`) | (a) marad a Bírák; (c) nyereség szerinti sorrend Ézs-sel kezdve; (d) a 7. adag vár |
| D14 | a Zsolt csak Sonnettel (DT-F22c lezárva); a detektor szerint tiszta (2527/2527 vers, 150 fejezet, K-hiány 0, E-hiány 0), nincs kézi beolvasztás; a versbeosztás jóváhagyása és a szúrópróba módja (a Zsolt 51:1–10-re szűkítve): DT58, DT59 (felhasználó, 2026-10-07); előfutás 12 köteg, utána a teljes futás (heti keret 85%-nál megállás a köteg végén); jelentés: `naplok/F22_Zsolt_jelentes.md`; a CLAUDE.md elavult TAHOT-hiány sora javítva (Jób 40:1–5 és Jób 41 hiányzik) | a felhasználó döntései (DT58, DT59) és a Józs-menet precedense (D12) | a teljes futás a szúrópróba előtt (a felhasználó a Zsolt 51:1–10-re szűkítette a mintát); a C (Gemini) kimarad (DT-F22c) |
| D15 | a Zsolt-menet párhuzamos futását a felhasználó utólag elfogadta (DT60, 2026-10-07); **az elv érvényben marad: párhuzamos futás csak kifejezett jóváhagyással indulhat**, alapértelmezés a „kötegenként egy subagent, sorban” | a kötegek függetlenek, de a keretmérés és a hibakezelés párhuzamosan nem tiszta; a jóváhagyás a futás előtt kell, nem utólag | a párhuzamos futás alapértelmezetté tétele |
| D16 | az Ézs csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a), DT57); a detektor Ézs 9 és 64 hibáját kézi megfeleltetés javítja (`f22/versmegfeleltetes_kezi.tsv`), két 2:1 beolvasztással (Ézs 9:20, 64:1 → átnézés); költség 7,08 USD; jelentés: `naplok/F22_Ezs_jelentes.md` | a felhasználó döntései (DT73 (a), DT57, versbeosztás-jóváhagyás 2026.10.08) | subagentes futás (a keretet terheli) |
| D17 | a Jer csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a), DT57); a detektor szerint tiszta (1364/1364 vers, 52 fejezet), nincs kézi javítás és beolvasztás; könyvplafon 15,14 USD (F77.11), költség 9,06 USD; jelentés: `naplok/F22_Jer_jelentes.md` | a felhasználó döntései (DT73 (a), DT57, versbeosztás-jóváhagyás 2026.10.08: „mehet”) | subagentes futás (a keretet terheli) |
| D18 | **DT70** — a 22.6 független szúrópróba az Ézstől kezdve elmarad (felhasználó, 2026-10-08: „nem csinálok próbát”); a `zart_osszevet.py` megmarad, a döntés újranyitható | a minőség jelzője a kapu, az `--ellenoriz` és a független ellenőri kör | könyvenkénti szúrópróba (22.6) |
| D19 | **DT71 (a)** — a prófétai könyveknél (Ez, kispróféták, Dán) is 10 verses kötegek; az Ézs és a Jer 10 verses futása utólag elfogadva (a 22.1.3 és a DT-F21g (3) 5 verses előírása erre a menetre nem érvényes). **DT72**: az Ézs futásnapló-sorainak átcímkézése (F77.11) utólag elfogadva; futásnapló csak kifejezett jóváhagyással írható át (felhasználó, 2026-10-08) | a Jer-ellenőr 1. és 2. eltérése (`naplok/ELLENOR_F22_Jer.md`) | (a) 10 verses kötegek a prófétáknál is; a napló visszaállítása |
| D20 | az 1Krón csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a), DT57 (1)); a detektor szerint tiszta (942/942 vers, 29 fejezet), nincs kézi javítás és beolvasztás; könyvplafon 10,46 USD, költség 4,56 USD; kapuhiba első próbára 70/942 (ebből 50 öt formátumhibás kötegben), végleg 1 (1Krón 19:2, átnézési sor); jelentés: `naplok/F22_1Kron_jelentes.md` | a felhasználó döntései (DT73 (a), DT57 (1), versbeosztás-jóváhagyás 2026.10.08: „mehet”) | subagentes futás (a keretet terheli) |
| D21 | a 2Krón csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a), DT57 (1)); a detektor szerint tiszta (822/822 vers, 36 fejezet), nincs kézi javítás és beolvasztás; könyvplafon 9,12 USD, költség 6,32 USD (versenként 0,0077, a plafon alapja 0,0074 fölött); kapuhiba első próbára 14/822, végleg 0; jelentés: `naplok/F22_2Kron_jelentes.md` | a felhasználó döntései (DT73 (a), DT57 (1), versbeosztás-jóváhagyás 2026.10.08: „mehet a 2 krónika”) | subagentes futás (a keretet terheli) |
| D22 | az Ezsd csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a), DT57 (1)); a detektor szerint tiszta (280/280 vers, 10 fejezet), nincs kézi javítás és beolvasztás; könyvplafon 3,11 USD, költség 1,64 USD (versenként 0,0059); kapuhiba első próbára 16/280 (ebből 10 egy formátumhibás kötegben, k009), végleg 0; jelentés: `naplok/F22_Ezsd_jelentes.md` | a felhasználó döntései (DT73 (a), DT57 (1), versbeosztás-jóváhagyás 2026.10.08: „mehet az ezsdrás”) | subagentes futás (a keretet terheli) |
| D23 | az Ez csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a)), 10 verses kötegekkel (DT71 (a)); a DT57 (1) sorrendjéből a Jób elé hozva (a Jób versmegfeleltetése nyitott); a detektor szerint tiszta (1273/1273 vers), nincs kézi javítás és beolvasztás; könyvplafon 14,13 USD, költség 7,80 USD (versenként 0,0061); kapuhiba első próbára 32/1273 (ebből 10 egy formátumhibás kötegben, k088), végleg 0; régi arany 8/8; jelentés: `naplok/F22_Ez_jelentes.md` | a felhasználó döntései (DT73 (a), versbeosztás-jóváhagyás és sorrend 2026.10.08: „menjen ezékiel”) | a DT57 (1) sorrendje szerint előbb a Jób |
| D24 | a Péld csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a)), 10 verses kötegekkel; a Jób helyett (a Jób versbeosztás-javaslata után, felhasználó 2026.10.09: „menjen helyette a példabeszédek”); a detektor hibáját kézi megfeleltetés javítja (Károli 12:n → TAHOT 12:(n+1)), egy 2:1 beolvasztással (Péld 11:31 hu 15–30 = TAHOT 12:1 → átnézés); könyvplafon 10,15 USD, költség 2,61 USD (versenként 0,0029); kapuhiba első próbára 56/914 (ebből 44 öt formátumhibás kötegben), végleg 0; régi arany 16/16; jelentés: `naplok/F22_Peld_jelentes.md` | a felhasználó döntései (DT73 (a), versbeosztás-jóváhagyás 2026.10.09) | előbb a Jób (41. fejezet nélkül vagy az N-F83a után) |
| D25 | a Bír csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a)), 10 verses kötegekkel; a BDB-haszon mérése (2026.10.09) szerint a tiszta versbeosztású könyvek közül; a detektor szerint tiszta (618/618 vers), nincs kézi javítás és beolvasztás; könyvplafon 6,86 USD, költség 4,39 USD (versenként 0,0071); kapuhiba első próbára 13/618, végleg 0; régi arany a könyvben nincs; jelentés: `naplok/F22_Bir_jelentes.md` | a felhasználó döntése (chat, 2026.10.09: „mehet a birák”) | Eszt (a 7. adagnak többet ad, de kisebb könyv) |
| D26 | a Jób csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a)), egy menetben (1068 vers, a Jób 41 a #84 óta a TAHOT_kivonatban); a detektor a #84 után újragenerálva; kézi megfeleltetés: Károli 17:n → TAHOT 17:(n+1), 37:n → 37:(n+1), két 2:1 beolvasztással (16:22 hu 14–21 = TAHOT 17:1, 36:33 hu 13–21 = TAHOT 37:1 → átnézés), a #83 40. fejezeti sorai maradnak (DT85); könyvplafon 11,85 USD, költség 3,61 USD (versenként 0,0034); kapuhiba első próbára 103/1068 (ebből 60 hat formátumhibás kötegben), végleg 0; régi arany 13/14 (az eltérő hármas a régi arany kulcshibája); jelentés: `naplok/F22_Job_jelentes.md` | a felhasználó döntése (chat, 2026.10.09: „Mehet a Jób, egy menetben. Jóváhagyom”) | a Jób 41 nélkül, az N55 előtt |
| D27 | az Eszt csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a)), 10 verses kötegekkel; a BDB-haszon mérése (2026.10.09) szerint a 7. adag maradékára ez hat a legtöbbet (148); a detektor szerint tiszta (167/167 vers), nincs kézi javítás és beolvasztás; könyvplafon 1,85 USD, költség 1,36 USD (versenként 0,0082); kapuhiba első próbára 3/167, végleg 0; régi arany a könyvben nincs; jelentés: `naplok/F22_Eszt_jelentes.md` | a felhasználó döntése (chat, 2026.10.09: „mehet az eszter”) | 2Sám (a hátralévő sornak többet ad) |
| D28 | a 2Sám csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a)), 10 verses kötegekkel; a BDB-haszon mérése (2026.10.09) szerint a tiszta könyvek közül a legtöbbet adja a hátralévő sornak (577 / 86); a detektor szerint tiszta (695/695 vers), nincs kézi javítás és beolvasztás; könyvplafon 7,71 USD, költség 5,04 USD (versenként 0,0073); kapuhiba első próbára 28/695, végleg 1 (2Sám 23:16, átnézési sor); régi arany 8/8; jelentés: `naplok/F22_2Sam_jelentes.md` | a felhasználó döntése (chat, 2026.10.09: „mehet”) | 1Sám (nagyobb, a mérésben kevesebb) |
| D29 | az 1Sám csak Sonnettel, a Message Batches API-n (`effort=high`, DT73 (a)), 10 verses kötegekkel; a BDB-haszon mérése (2026.10.09) szerint a 2Sám után (524 / 86); a detektor szerint tiszta (811/811 vers; az 1Sám 20:43 a TAHOT-kulcsban már Károli-kulcsú), nincs kézi javítás és beolvasztás; könyvplafon 9,00 USD, költség 6,15 USD (versenként 0,0076); kapuhiba első próbára 30/811 (ebből 10 egy formátumhibás kötegben, k013), végleg 0; régi arany 1/1; jelentés: `naplok/F22_1Sam_jelentes.md` | a felhasználó döntése (chat, 2026.10.09: „menjen 1sámuel”) | 1Kir (a mérésben hasonló, több NINCS-szócikk) |

## Döntésnapló (a brief verziói)

| Verzió | Dátum | Változás | Indok |
|---|---|---|---|
| v1 | 2026.09.30 | első változat: teljes Biblia, három külső modell (A, B, döntőbíró C), Opus-arany, KJV-import, pilot ⛔ | a felhasználó kérése (teljes feldolgozás) |
| v2 | 2026.10.01 | v1 (három külső modell, a teljes Biblia) felváltva v2-vel, a #21 pilot eredménye alapján | a pilot mért pontossága: Sonnet 97,3%, Gemini 95,3%, a pár `magas` linkjei 98,7% |
| v2.23 | 2026.10.09 | az 1Sám menete csak Sonnettel, a Message Batches API-n (D29); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve az 1Sámuellel | a felhasználó döntése |
| v2.22 | 2026.10.09 | a 2Sám menete csak Sonnettel, a Message Batches API-n (D28); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve a 2Sámuellel | a felhasználó döntése |
| v2.21 | 2026.10.09 | az Eszt menete csak Sonnettel, a Message Batches API-n (D27); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve az Eszterrel | a felhasználó döntése |
| v2.20 | 2026.10.09 | a Jób menete csak Sonnettel, a Message Batches API-n (D26), a detektor újragenerálásával, kézi versmegfeleltetéssel és két 2:1 beolvasztással; `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve a Jóbbal | a felhasználó döntése |
| v2.19 | 2026.10.09 | a Bír menete csak Sonnettel, a Message Batches API-n (D25); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve a Bírákkal | a felhasználó döntése |
| v2.18 | 2026.10.09 | a Péld menete csak Sonnettel, a Message Batches API-n (D24), kézi versmegfeleltetéssel és egy 2:1 beolvasztással; `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve a Példabeszédekkel; `ag`: `claude/peaceful-meitner-1vzy4m` | a felhasználó döntései |
| v2.17 | 2026.10.08 | az Ez menete csak Sonnettel, a Message Batches API-n (D23), a Jób elé hozva; `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve az Ezékiellel; `ag`: `claude/f22-ez` | a felhasználó döntései |
| v2.16 | 2026.10.08 | az Ezsd menete csak Sonnettel, a Message Batches API-n (D22); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve az Ezsdrással; `ag`: `claude/f22-ezsd` | a felhasználó döntései |
| v2.15 | 2026.10.08 | a 2Krón menete csak Sonnettel, a Message Batches API-n (D21); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve a 2Krónikával; `ag`: `claude/f22-2kron` | a felhasználó döntései |
| v2.14 | 2026.10.08 | az 1Krón menete csak Sonnettel, a Message Batches API-n (D20); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve az 1Krónikával | a felhasználó döntései |
| v2.13 | 2026.10.08 | D19 (DT71 (a), DT72): prófétai kötegméret 10 (az 5 verses előírás helyett); a futásnapló átcímkézése elfogadva; a Jer-ellenőr köre | a felhasználó döntései |
| v2.12 | 2026.10.08 | D18 (DT70): a 22.6 szúrópróba az Ézstől elmarad | a felhasználó döntése |
| v2.11 | 2026.10.08 | a Jer menete csak Sonnettel, a Message Batches API-n (D17); könyvenkénti plafon (F77.11); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve a Jeremiással | a felhasználó döntései |
| v2.10 | 2026.10.08 | az Ézs menete csak Sonnettel, a Message Batches API-n (D16, DT73 (a), DT57); kézi versmegfeleltetés (`f22/versmegfeleltetes_kezi.tsv`) és két 2:1 beolvasztás; `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve az Ézzsel | a felhasználó döntései |
| v2.9 | 2026.10.07 | D15: a párhuzamos futás csak kifejezett jóváhagyással (DT60); a Zsolt-menet párhuzamos futása utólag elfogadva | a felhasználó döntése |
| v2.8 | 2026.10.07 | a Zsolt menete csak Sonnettel (D14); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve a Zsolttal; DT58/g | a felhasználó utasítása |
| v2.7 | 2026.10.07 | a következő könyv a Zsoltárok (D13, DT54); a `kovetkezo` frissítve | a felhasználó döntése |
| v2.6 | 2026.10.04 | a Józs menete csak Sonnettel (D12); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve a Józsuéval | a felhasználó utasítása |
| v2.5 | 2026.10.02 | az 5Móz menete csak Sonnettel (D11); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve az 5Mózessel | a felhasználó utasítása |
| v2.4 | 2026.10.02 | a 4Móz menete csak Sonnettel (D10); kézi 1:2 beolvasztás (`f22/versosszevonas.tsv`); jóváhagyási napló | a felhasználó utasítása |
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
