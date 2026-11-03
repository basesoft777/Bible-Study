# F161 GLOSSZA_LANC — menetnapló

*Modell: claude-opus-5-5 (a brief `modell` mezője: opus). Ág: `claude/glossza-lanc-1a9f9f`. 2026-11-03.*

## 1. A #121 feloldója

A `glossza_lexikon_forditas.py lista` a nem UBS szótárakra nem hívta a 13. szabály feloldóját (`tovabbi_forras`), ezért
az ANTROP-001 21 TBESG-egysége `nincs_forras` volt. Új közös `forras_szoveg(sor)`; a `lista` ezt hívja.

*proveniencia: scope=`glossza_lexikon_forditas.py lista --id ANTROP-001` a #608 ágának állapotán (c332f160, repón kívüli
munkafa), a javítás előtt és után | forras=konkordancia/TBESG.txt, UBS_DNTG_jelentesek.tsv, UBS_DBH_jelentesek.tsv,
adat/forditasok.tsv | ts=2026-11-03*

| `szotar` | előtte | utána |
|---|---|---|
| UBS_DNTG | 30 hianyzik | 30 hianyzik |
| UBS_DBH | 3 hianyzik | 3 hianyzik |
| TBESG | 21 nincs_forras | **21 hianyzik** |
| Thayer | 6 nincs_forras | 6 nincs_forras (szakaszsor; a Thayer-lánc dolga) |
| BDB | 1 nincs_forras | 1 nincs_forras (szakaszsor; a BDB-lánc dolga) |

A main-en (az ANTROP-001 régi lapja) ugyanígy feloldódik a TBESH 6, a tW 11, az MCGED 2 és a BDB nyelvi háttér 2
egysége is (N-F161b); ezeket a lánc nem veszi fel.

## 2. `szaraz` az ANTROP-001 54 egységén

*proveniencia: scope=`glossza_api_koteg.py szaraz --lista <a fenti lista> --munka <jegyzetmappa>/glossza_antrop`, a #608
állapotán | forras=a fenti lista, adat/terminologia.tsv (v5), adat/karoli_strong/, adat/forditasok.tsv | ts=2026-11-03*

- 54 egység (UBS DNTG 30, UBS DBH 3, TBESG 21), 3 kérés (20 + 20 + 14 egység; azonos Strong egy kérésben).
- Forrás 1 213 karakter; a három prompt 30 630 karakter.
- Becslés (manual, mérés nélkül): bemenet ~13 100 token, kimenet ~18 900 token; ~0,11 USD Batch-áron, cache nélkül.
- A kérések a session jegyzetmappájában (`glossza_antrop/keresek.jsonl`), repón kívül; a `bekuld` nem futott.

## 3. A lánc próbája (5 glossza, prompt v1) — felváltva

Az első menetben (a hatókör-módosítás előtt) 5 glossza ment a v1 prompttal egy Sonnet subagenten át: 5/5 átment. Az
eredményt nem írtuk be; a 4. pont éles futása ugyanezeket az egységeket a v2 prompttal újra fordította.

## 4. Az éles futás: a 9 lexikonlap hiányzó UBS- és TBESG-glosszái

*proveniencia: scope=`glossza_lexikon_forditas.py lista --id <ID>` mind a 9 `lexikon/*_TUDOMANYOS.md` lapra (8 a main
állapotán, 2910ae69 + ez az ág; az ANTROP-001 a #608 állapotán, c332f160; repón kívüli render), egyesítve, azonos kulcs
egyszer | forras=konkordancia/UBS_DNTG_jelentesek.tsv, UBS_DBH_jelentesek.tsv, TBESG.txt; adat/forditasok.tsv | ts=2026-11-03*

| motívum | UBS DNTG | UBS DBH | TBESG | összesen |
|---|---|---|---|---|
| ALVIL-001 | 0 | 0 | 0 | 0 |
| ANTROP-001 (#608) | 30 | 3 | 21 | 54 |
| HAMART-001 | 16 | 88 | 72 | 176 |
| HODIT-001 | 0 | 14 | 1 | 15 |
| ISTENTISZT-001 | 0 | 0 | 0 | 0 |
| KIRALY-001 | 6 | 26 | 5 | 37 |
| MENNY-001 | 0 | 50 | 35 | 85 |
| TEREMT-001 | 0 | 4 | 1 | 5 |
| TEREMT-002 | 0 | 0 | 0 | 0 |
| **egyesítve** | **52** | **183** | **131** | **366** (a 400-as küszöb alatt) |

Mezők: UBS glossza 134, UBS definíció 101 (DBH 90, DNTG 11), TBESG rövid 131. A definíciók miatt a prompt v2-t kapott
(egyetlen kiegészítő szabály: a UBS-jelek `=`, `≈`, `◄`, `►` és a `{L:…<SDBH:…>}` jelölés változatlan, „szó szerint: …;
innen:”), a futás előtt rögzítve; a v1 szövege változatlan.

*proveniencia: scope=`glossza_api_koteg.py szaraz → prompt → (subagent) → bevesz → kapuz → javit → rogzit → beir`, munkakönyvtár a
session jegyzetmappájában (`glossza_9lap/`) | forras=a 23 kérés (`keresek.jsonl`, 238 807 karakter), a subagentek válaszai,
adat/terminologia.tsv (v5) | ts=2026-11-03*

- **`szaraz`:** 366 egység, 23 kérés (kérésenként 4–20 egység), forrás 15 252 karakter, prompt 238 807 karakter. A Batch-becslés
  (manual) ~0,74 USD lenne; az API nem futott.
- **Fordítás:** kérésenként egy `general-purpose` subagent (`model: sonnet`; mind a 24 futás saját bevallása szerint
  `claude-sonnet-5-5`). A subagent a `prompt` paranccsal kiírt user-szöveget fájlból olvasta be szó szerint, a JSON-választ
  fájlba írta; ez a futtatási utasítás a kérésen kívül állt. Eltérés az API-tól: a Claude Code alap rendszerutasítása,
  effort és max_tokens nem állítható (a sorok megjegyzése ezt rögzíti). Mérés és költségnapló nincs.
- **`kapuz`:** 1. kör 365/366; az e321 (TBESG G2836 `belly/womb/stomach`) a G1 elemszám-kapun bukott (a perjeles elemet
  „;”-vel bontotta); a javító kör (`G021-p2`, egy egység) után **366/366**. Kétszer bukott: 0.
- **Mankó-jelzés 5** (szójegyzéki ütközés), kézzel átnézve, mind homonímia: G5591 79.5 *human* → emberi (a tábla: ember);
  H7043 *light; fast* → könnyű; sebes (a tábla: fény, böjt); H7043 *to lighten* → könnyebbé tenni; H7043 *to shake* →
  megrázni; G2100 *to please* → tetszeni. A `beir` `--jelzes-atnezve`-vel futott.
- **`beir`:** 366 új sor az `adat/forditasok.tsv`-ben, a tábla rendje szerinti helyre (31 helyen), 0 törölt vagy cserélt
  sor; a tábla vége (ahová a #608 fűz) változatlan. A #608 csak Thayer-kulcsot ír, a #609 a táblát nem érinti: kulcsütközés
  nincs. A 13. szabály (`ellenoriz.szabaly13_forditasi_gyorsitotar`): RENDBEN.
- **Lapok:** az ISTENTISZT-001 és az ALVIL-001 újragenerálása (repón kívül) a mostani lappal tartalmilag azonos (sorvég nélkül
  0 eltérő sor): a két kiadott lapon nincs hiányzó UBS/TBESG-egység, ezért a lapfájl nem változik. Feed 6. kapu (`muhely_allapot.kriterium_6`):
  ISTENTISZT-001 zöld, „fordításra vár” 0 (előtte is 0); ALVIL-001 zöld, 0 (előtte is 0). Olvasói kapu: a két lap
  BUKÁS-számai nem változtak (a lap nem változott). A másik hét lapot ez a PR nem generálja újra.

### C0 szúrópróba

| szótár, kulcs, mező | forrás | fordítás |
|---|---|---|
| UBS DNTG G0540 10.15 definíció | a person for whom there is no record of a male parent or who has never had a male parent or whose father has died | olyan személy, akiről nincs feljegyzés, hogy lett volna férfi szülője, vagy akinek soha nem volt férfi szülője, vagy akinek az apja meghalt |
| UBS DBH H0127 definíció | = fortified town; ◄ territory of {L:Naphtali<SDBH:נַפְתָּלִי>} | = megerősített város; ◄ {L:Naphtali<SDBH:נַפְתָּלִי>} területe |
| UBS DBH H1121 definíció | literally: children of a town, region, nation; hence: = people, animals, or products that are inhabitants of or originating from a place, town, region, or nation, ◄ as if they were the offspring of that place | szó szerint: város, vidék, nemzet gyermekei; innen: = emberek, állatok vagy termékek, amelyek egy hely, város, vidék vagy nemzet lakói vagy onnan származnak, ◄ mintha annak a helynek az utódai lennének |
| UBS DBH H5315 glossza | living creature; living soul | élőlény; élő lélek |
| TBESG G2836 rövid | belly/womb/stomach | has/méh/gyomor (a javító kör után) |

## 5. TBESH-ellenőrzés (fordítás nélkül)

*proveniencia: scope=a 9 lap #121-listájának TBESH-sorai, összevetve az `adat/glosszak_heber_hu.tsv`-vel (11 677 sor) és a
`forditasok.tsv` TBESH-soraival | forras=a fenti listák | ts=2026-11-03*

22 egyedi kulcs (23 lap-sor). **Kulcseltérés egy sincs**: a lapok a teljes TBESH-szócikk fordítását keresik
(`TBESH|<Strong>|<Strong>|teljes|forditas_hu`), a `glosszak_heber_hu.tsv` viszont csak a rövid glosszát adja (más kulcson
sincs teljes fordítás; a `forditasok.tsv`-ben 1 TBESH-sor van, más Strongra). Mind a 22 valóban hiányzik (N-F161c).

| lap(ok) | a lap keresett kulcsa | glosszak_heber_hu (strong, entry_id → glossza_hu) | forditasok.tsv más TBESH-kulcson | ítélet |
|---|---|---|---|---|
| HAMART-001 | `TBESH|H0127|H0127|teljes|forditas_hu` | H0127 H0127G → föld: talaj | — | valóban hiányzik (a teljes szócikk) |
| MENNY-001 | `TBESH|H0430|H0430|teljes|forditas_hu` | H0430 H0430G → Isten | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H0779|H0779|teljes|forditas_hu` | H0779 H0779 → megátkozni | — | valóban hiányzik (a teljes szócikk) |
| MENNY-001 | `TBESH|H1121a|H1121a|teljes|forditas_hu` | H1121 H1121A → fiú: gyermek (+7) | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H2403a|H2403a|teljes|forditas_hu` | H2403 H2403A → bűn (+3) | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H2403b|H2403b|teljes|forditas_hu` | H2403 H2403A → bűn (+3) | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H2555|H2555|teljes|forditas_hu` | H2555 H2555 → erőszak | — | valóban hiányzik (a teljes szócikk) |
| KIRALY-001 | `TBESH|H3548|H3548|teljes|forditas_hu` | H3548 H3548 → pap | — | valóban hiányzik (a teljes szócikk) |
| KIRALY-001 | `TBESH|H3678|H3678|teljes|forditas_hu` | H3678 H3678G → trón | — | valóban hiányzik (a teljes szócikk) |
| KIRALY-001 | `TBESH|H4467|H4467|teljes|forditas_hu` | H4467 H4467 → királyság | — | valóban hiányzik (a teljes szócikk) |
| HODIT-001, MENNY-001 | `TBESH|H5303|H5303|teljes|forditas_hu` | H5303 H5303 → nefilek | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H6093|H6093|teljes|forditas_hu` | H6093 H6093 → fáradság | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H6975|H6975|teljes|forditas_hu` | H6975 H6975 → tövis | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H7043|H7043|teljes|forditas_hu` | H7043 H7043 → könnyűnek lenni | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H7451a|H7451a|teljes|forditas_hu` | H7451 H7451C → nyomorúság: kár (+4) | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H7451b|H7451b|teljes|forditas_hu` | H7451 H7451C → nyomorúság: kár (+4) | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H7451c|H7451c|teljes|forditas_hu` | H7451 H7451C → nyomorúság: kár (+4) | — | valóban hiányzik (a teljes szócikk) |
| HODIT-001 | `TBESH|H7496|H7496|teljes|forditas_hu` | H7496 H7496 → árny | — | valóban hiányzik (a teljes szócikk) |
| HAMART-001 | `TBESH|H7843|H7843|teljes|forditas_hu` | H7843 H7843 → elpusztítani, megrontani | — | valóban hiányzik (a teljes szócikk) |
| KIRALY-001 | `TBESH|H8004|H8004|teljes|forditas_hu` | H8004 H8004 → Sálem | — | valóban hiányzik (a teljes szócikk) |
| ISTENTISZT-001 | `TBESH|H8034|H8034|teljes|forditas_hu` | H8034 H8034 → név | — | valóban hiányzik (a teljes szócikk) |
| TEREMT-001 | `TBESH|H8415|H8415|teljes|forditas_hu` | H8415 H8415 → mélység | — | valóban hiányzik (a teljes szócikk) |

## 6. Tesztek

`python eszkozok/teszt_glossza_api_koteg.py`: 21 teszt, OK. `python eszkozok/teszt_glossza_lexikon_forditas.py`: 16 teszt, OK.

## 7. Független ellenőrzés

Az F161.0–F161.4 tartományon (`fuggetlen-ellenor`): ELTÉRÉS 6 — mind javítva az F161.7-ben (tulajdonnév és „gerinc” hamis
pozitív, TBESG `rovid`-szűrés, a 2. kör bájtra azonossága, a „jóváhagyott” címke, üres korábbi válasz). Az F161.5–F161.9
második ellenőrzése: ELTÉRÉS 6; javítva az F161.11-ben (4 kisbetűs tulajdonnév, a G1944 001900 definíciója a kezi sor szavával, egy helyesírási hiba — 6 sor kézzel, a megjegyzésben jelölve; a v2 verziónapló-bejegyzése), nyitott: N-F161d. Mindkét kör: `naplok/ELLENOR_F161.md`.
