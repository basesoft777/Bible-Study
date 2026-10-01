# F34 M2–M4 — futásnapló és proveniencia

*Ág: `claude/bdb-psi` · eszköz: `eszkozok/bdb_psi_javit.py` · dátum: 2026.10.01 · dontés: DT-F34 (felhasználó, 2026.10.01)*

## Proveniencia

`scope=manual | forras=eszkozok/bdb_psi_javit.py + konkordancia/TAHOT_kivonat.tsv + naplok/F34_M0_lista.tsv | ts=2026-10-01`
A javítás kulcsa: szócikk-id + régi + új token (`naplok/F34_M2_csere.tsv`), nem sorszám.

## 0. pont: parser-javítás nem elérhető

A nyers `DictBDB.json` nincs a repóban (a `konkordancia/_convert_bdb.py` a `%TEMP%`-ből olvasna); a `konkordancia/lexikonok_nyers/BDB.lexicon` más szerkezetű (18 642 tétel, más jelölés), nem ennek a datasetnek a nyers forrása. Ezért az 1–4. pont szerint mezőkulcsos csere a kész TSV-n.

## Szabály és eredmény

- A (fejezet>66 / „Psalm” jelző): javul, ha a szócikk Strong-száma a TAHOT szerint előfordul a Zsolt c:v ±1 versben.
- B/R: javul, ha Zsolt c:v ±1 találat van, és a TAHOT szerint más könyvben ugyanott (c:v ±1) nincs.

| | Javítva (hely) | Maradék (hely) |
|---|---|---|
| A | 85 | 19 |
| B | 57 | 144 |
| R | 2 (köztük H7585 `Ezek 16:10` → `Psa 16:10`) | 15 |
| Összesen | **144 hely, 48 szócikk** | **178 hely, 104 szócikk** |

A maradék oka: 167 kulcsnál a TAHOT-kivonatban nincs Zsolt c:v ±1 találat (a kivonat nem teljes: Zsolt 88/89/140/142 hiányzik, és a Strong-szám nem mindig szerepel az idézett versben), 7-nél más könyvben is van találat (nem egyértelmű), 1 összeolvadt alak (`2Sam 132:1132`). Listája: `naplok/F34_M2_maradek.tsv` — **kézi nézet, nem javítva**. `Dan 22:14` forráshiba, nem hatókör.

## Diff-kapu

Forrás: 144 csere, 48 sor változott; minden változott sorban a `Könyv c:v` helyhivatkozások `<R>`-re cserélve a két szöveg bájtazonos (más eltérés nincs). Sorszám változatlan, a sorvégek megmaradtak. Új SHA-256: `e9ee0b724dcb86f40370734b142d17863fe204c764966911f72b042e0ddf666d`.

## M3 — adat/forditasok.tsv

Csak a helyhivatkozás tokenje változott (a fordítás szövege egyébként bájtazonos; kapu a szkriptben), a `forras_hash` az új forrásból újraszámolva (SHA-1):

| Fájlsor | Szócikk | Állapot | Csere |
|---|---|---|---|
| 78 | H8415 | kezi | Ézs 106:9 → Zsolt 106:9; Ézs 71:20 → Zsolt 71:20 |
| 81 | H7585 | kezi | Ez 16:10 → Zsolt 16:10; Ez 49:16 → Zsolt 49:16 (Ez 73:23, 73:25 marad: a TAHOT nem igazolja) |
| 89 | H0430 | opus | Jób 97:7 → Zsolt 97:7 |

A 84. és 85. sor forrása nem változott (nincs javítható találat), ezért érintetlen. `eszkozok/ellenoriz.py`: 13. szabály (forras_hash) **RENDBEN**, kilépési kód 0.

## M4 — kapu

`eszkozok/teszt_forditas_kapuk.py`: 20 teszt OK (3 új: javított hely nem jelez; hibás ψ-feloldás jelez; a 78. és 89. sor RENDBEN). A 13. kapu a 78. és 89. soron **0**; a 81., 84., 85. soron a jelzés a **maradék miatt** marad (Ez 73; Péld 57–59, 75 és `2Kir 36:10`; Dán 22) — ez a ⛔ kézi nézet.

## F34.5 — DT-F34b alkalmazása (2026.10.01)

1. **A-maradék TAHOT nélkül:** a 19 A-maradékból 15 javítva, ha a vers létezik a Zsolt-fejezetben (versszámozási tábla: `konkordancia/Macula_heber_Zsoltarok.tsv`, MT, 150 fejezet / 2527 vers; `vers_tabla()` az `eszkozok/bdb_psi_javit.py`-ban). Köztük `Ezek 73:23`, `Ezek 73:25` (H7585), `Prov 75:1` (H7843). Marad: `Gen 81:48`, `Josh 82:9`, `1Ki 145:31` (a vers nem létezik a zsoltárban), `2Sam 132:1132` (összeolvadt alak, kézi).
2. **Összesen javítva: 159 hely, 56 szócikk** (A 100, B 57, R 2). **Maradék: 163 hely, 99 szócikk** (A 4, B 144, R 15), `naplok/F34_M2_maradek.tsv`; N-F34 / N-F34b a `NYITOTT_FELADATOK.md`-ben (helyőrző).
3. **forditasok.tsv:** a 81. és 84. sor forrása (H7585, H7843) tovább változott, a sorokat a döntés szerint NEM írtam át. A tárolt `forras_hash` ezért elavult: az `ellenoriz.py` 13. szabálya e két sorra SÉRTÉS (kilépési kód 1). A 78., 89. sor RENDBEN; a 85. sor forrása nem változott.
4. **Újrafuttathatóság:** `python eszkozok/bdb_psi_javit.py --forditas [--ir]` a csere-táblát a lefordított szövegen alkalmazza (csak a helyhivatkozás tokenje, a 81/84/85. sor kihagyva, hash érintetlen); a főfutás idempotens (újrafuttatva 0 csere). Teszt: `python eszkozok/teszt_bdb_psi_javit.py` (6 teszt OK).
5. **Új SHA-256:** `5c176037617813e330eb57e883ab7fd728c19a244c42196668ea712d0f502f14`.
6. **Megfigyelés:** a DT-F34b tételben feltételezett TAHOT-hiány Zsoltárokra nem áll fenn (150/150 fejezet, 2527/2527 vers; a hiányt a `TAHOT_TAGNT_README.md` szerint korábban pótolták; a `CLAUDE.md` állítása elavult) — a 167 elutasítás tehát valódi „nincs a versben” eredmény.
