# TSK-versszám felmérés — a TSK KJV-kulcsa Károli-kulcsként

*Felmérés, javítás nélkül · 2026-10-17 · modell: claude-opus-5-5 · alap: `main` @ c57a9041 · ág: `claude/admiring-fermat-bcf235`*
*Kiváltó ok: a #9 (SZOTAR S2, PR #381) S2.8 ⛔ kapuja. A diff-osztályozó az ALVIL-001-ben 14 „ismeretlen” sort talált, ebből 11 TSK-jelölt a Préd 9:12 (Károli) helyes verséhez tartozik.*

Mérőszkript: `eszkozok/tsk_versszam_felmeres.py`. Csak olvas, a részletes TSV-t a repón kívülre írja. Futtatás: `python eszkozok/tsk_versszam_felmeres.py`.

## 0. Összefoglaló

**A hiba valós és rendszerszintű.** A `konkordancia/TSK_kereszthivatkozasok.tsv` mindkét kulcsa KJV-számozású (`Igehely` és `Kapcsolódó igehely`), a könyvnév viszont magyar. **Egyik fogyasztó sem vált át**, mind Károli-kulcsként használja:

| Fogyasztó | Hely | Használat |
|---|---|---|
| `eszkozok/lexikon_general.py` | `tsk_index()`, `blokk_kereszthivatkozasok()` (main: 1221., 1257. sor) | `tsk_index().get(igehely)`: a lexikon kereszthivatkozás-blokkja |
| `eszkozok/lekerdez.py` | `cmd_tsk()` (main: ~531. sor) | `r["Igehely"] == scope_adat_igehely(igehely)`, a `lekerdez.py tsk` CLI |
| `eszkozok/nem_vizsgalt.py` | `tsk_kor()` (main: ~443. sor) | a lelet-lap TSK-köre (a csillag = lexikai kör − TSK-kör) |
| `eszkozok/sqlite_epit.py` | `_kereszthivatkozasok()` (main: ~678. sor) | a `pardes.db` `tsk` táblája (olvasó-szerver) |
| `eszkozok/olvaso_pilot/adat.py` | 168–171. sor | a pilot-olvasó TSK-oszlopa |

A hiba két oldalon jelentkezik:
- **Forrásoldal:** a Károli-vers a vele azonos számú KJV-vers TSK-sorait kapja, a saját sorai pedig elmaradnak.
- **Céloldal:** a megjelenített „Kapcsolódó igehely” KJV-szám, Károli-hivatkozásként olvasva más versre mutat.

## A. Teljes TSK

| Mérés | Érték |
|---|---|
| TSK-sor összesen | 432 949 |
| ÓSZ-forrású sor | 288 620 |
| ÓSZ-forráskulcs (egyedi vers) | 21 587 |
| ebből Károli-kulcsként olvasva más vagy nem létező Károli-versre esik | **1 502 kulcs, 23 150 sor** (8,0%) |
| ÓSZ-célú sor | 272 174 |
| ebből legalább egy célverse eltérő számozású | **23 540 sor** |
| Károli-vers, amelynek KJV-kulcsa eltér, vagy nincs KJV-párja (`Karoli_versmegfeleltetes.tsv`) | 1 339 / 22 931 |

`proveniencia: scope=TSK-teljes | forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv | n=432949 | ts=2026-10-17`

Az eltérés zöme a Zsoltárok könyvében jelentkezik: a feliratos zsoltároknál a Károli az MT-számozást követi (felirat = 1. vers), ezért ott +1/+2 az eltolódás. Kisebb blokkok: Préd, Jóel, Mal, Hós, 4Móz 13, Jób 39–41 és a KEZI-osztályú sorok.

## B. Az `adat/elofordulasok.tsv` igehelyei

| Mérés | Érték |
|---|---|
| sor / tartomány-sor | 259 / 17 |
| egyedi vers (kibontva) | 311 |
| azonos Károli- és KJV-kulcs (ÓSZ) | 206 |
| ÚSZ (a megfeleltetés nem fedi; azonosság feltételezve, l. 4. pont) | 87 |
| **eltérő kulcs** | **18 vers, 6 motívumban** |

`proveniencia: scope=elofordulasok.tsv (311 vers) | forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv | n=18 | ts=2026-10-17`

A 18 eltérő versen a TSK-hatás:

| | ma kapott sor | helyes sor | rossz versről | elmarad |
|---|---|---|---|---|
| minden Votes | 264 | 355 | 263 | 354 |
| Votes ≥ 15 (a lexikonblokk küszöbe) | 10 | 18 | **10** | **18** |

Hét versen látszik a hatás a ≥ 15 küszöbön:

| Károli-vers | Motívum | KJV-kulcs | ma kapott sorok valójában ennek a Károli-versnek | rossz ≥15 | elmarad ≥15 |
|---|---|---|---|---|---|
| Préd 9:12 | ALVIL-001 | Préd 9:10 | Préd 9:14 | 0 | **12** (a #9 osztályozója 11-et látott) (Kol 3:23, Mt 6:33, Ef 5:16, Jer 29:13, 1Kor 9:24, Préd 11:6, 2Krón 31:20–21 …) |
| Zsolt 18:6 | ALVIL-001 | Zsolt 18:5 | Zsolt 18:7 | **6** (Zsolt 50:15, 2Sám 22:7, Zsolt 34:15, 130:1–2, 120:1) | 0 |
| Zsolt 6:6 | ALVIL-001 | Zsolt 6:5 | Zsolt 6:7 | 0 | **5** (Préd 9:10, Zsolt 115:17, 30:9, 88:10, 88:12) |
| Zsolt 36:7 | TEREMT-001 | Zsolt 36:6 | Zsolt 36:8 | **4** (Zsolt 86:5, Ruth 2:12, Zsolt 91:4, 1Ján 3:1) | 0 |
| Zsolt 42:8 | TEREMT-001 | Zsolt 42:7 | Zsolt 42:9 | 0 | 1 (Jón 2:3) |

A további 11 eltérő vers (4Móz 13:34; Zsolt 30:4, 31:18, 49:15–16, 53:2, 55:16, 76:3, 77:17, 88:4, 88:11, 89:49, 9:18) ≥ 15-ön sem ma, sem helyesen nem ad találatot. Minden Votes-értéken azonban ezeknél is teljes a csere: például a Zsolt 31:18-nál 33 sor marad el. Ez a `nem_vizsgalt.py` minden Votes-értéket használó TSK-körét érinti.

Motívumonként (eltérő vers / rossz ≥15 / elmarad ≥15): ALVIL-001 11 / 6 / 17 · TEREMT-001 3 / 4 / 1 · HODIT-001 2 / 0 / 0 · MENNY-001 1 / 0 / 0 · HAMART-001 1 / 0 / 0 · KIRALY-001 1 / 0 / 0.

**A generált kimenetben is látszik** (main, `lexikon/ALVIL-001_TUDOMANYOS.md` 844. sor): a `#### Zsolt 18:6` alatt a KJV 18:6 („In my distress I called”) TSK-sorai állnak, holott a Károli 18:6 a Seol köteleiről szól (= KJV 18:5). Ugyanígy a `lexikon/TEREMT-001_TUDOMANYOS.md` 549. sora: a Zsolt 36:7 alatt a KJV 36:7 szárny-képe szerepel. A main lexikonja még a régi `Préd 9:10` kulcson áll, ezért ott a Seol-vers TSK-ja véletlenül helyes. Az F87.3 átkulcsolása (Préd 9:10 → 9:12) után az újragenerálás veszíti el. Ezt látta a #9.

### B2. Mellékes lelet: a tartomány-igehely nem kap TSK-t

A `lexikon_general.tsk_index()` pontos kulcsra keres, ezért a 17 tartomány-igehely (pl. `1Móz 14:18-20`) semmit nem talál. 7 ilyen sor verseire volna ≥ 15 TSK-találat. Ez nem versszám-hiba, de ugyanazt a függvényt érinti.

### B3. Céloldal

A motívum-versek mai ≥ 15 TSK-találata 341 cél. Ebből **19** eltérő számozású versre mutat, például: `Zsolt 16:10 → Zsolt 49:15` (Károli: 49:16), `1Móz 2:7 → Préd 12:7` (Károli: 12:9), `1Móz 6:4 → 4Móz 13:33` (Károli: 13:34), `Zak 13:9 → Hós 2:23` (a KJV Hós 2:23-nak nincs azonos számú Károli-párja).

`proveniencia: scope=elofordulasok.tsv versei, Votes>=15 | forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv | n=341 | ts=2026-10-17`

## C. `adat/jeloltek.tsv`: került-e rossz TSK-jelölt adatba?

**A `beépítve` döntésű sorok között nincs rossz kulcsú TSK-jelölt.** A 236 TSK-eredetű jelöltből 10 esik eltérő számozású versre. A Károli-szöveg összevetése szerint ezek három csoportba esnek:

| Sor | Döntés | Lelet |
|---|---|---|
| KIRALY-001 Zsolt 76:3 | beépítve | **helyes Károli-kulcs**: a Károli 76:3 „hajléka van Sálemben”, az indoklás is ezt idézi |
| HAMART-001 Préd 9:3 (TSK 1Móz 6:5) | elutasítva | **KJV-kulcs, átváltás nélkül**: az indoklás („emberi szívről”) a Károli 9:5-re illik |
| HAMART-001 Préd 2:11, 2:17, 2:22, 2:23 (TSK 1Móz 3:17) | elutasítva | **KJV-kulcs**: a fáradság- és gyűlölet-tartalom a Károli 2:12, 2:18, 2:23, 2:24-ben áll |
| HAMART-001 Zsolt 140:11, Zsolt 55:9 (TSK 1Móz 6:11) | elutasítva | **KJV-kulcs**: a chámász („erőszak”) a Károli 140:12-ben és 55:10-ben áll |
| ISTENTISZT-001 Zsolt 89:21, 89:22 | elutasítva | nem TSK-cél (az ApCsel 9:14 TSK-sorai között nincs); Károli-KH-eredetű, nem érintett |

`proveniencia: scope=jeloltek.tsv TSK-eredetű sorai | forras=jeloltek.tsv+Karoli_versmegfeleltetes.tsv+Karoli_1908.tsv | n=236 | ts=2026-10-17`

**7 elutasított HAMART-001-jelölt KJV-kulcson áll.** A döntés tartalmilag a valódi (KJV) versre vonatkozik, a kulcs viszont más Károli-versre mutat. Adatba nem jutott, de a napló-nyom hamis: az `igehely` mező szerint egy olyan Károli-verset utasítottunk el, amelyet senki nem vizsgált. A forrásuk a `Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md` §4/b (2026-10-11).

Az `elofordulasok.tsv` egyetlen TSK-említésű sora (ISTENTISZT-001 Róm 10:12) ÚSZ-vers, nem érintett.

## 4. Korlátok

- **ÚSZ: nem mért.** A `Karoli_versmegfeleltetes.tsv` csak az ÓSZ-t fedi (39 könyv). Az ÚSZ-ben a Károli és a KJV ismert helyeken eltérhet (pl. 2Kor 13:12–14, 3Ján 14–15, Róm 16 vége, Jel 12:18/13:1). Ezeket a szkript azonosnak veszi, tehát az ÚSZ-adat alsó becslés (0).
- **Nincs KJV-pár** (pl. zsoltárfelirat, Préd 9:21–23 `kezi_identitas_javitas` üres KJV-vel): a szkript eltérőnek számolja, „helyes” TSK nélkül.
- **Fejezethatáron átnyúló tartomány:** a kibontás bővít (c1-ben a 200. versig), a nem létező versek a kulcsoknál kiesnek. Az érintett sorok száma kicsi.
- A C-csoport osztályozását Károli-szöveg-összevetéssel végeztem, kézzel, 10 soron (`scope=manual`).
