# T1.1 — TEREMT-002 (תֹהוּ וָבֹהוּ) lekérdezés-összefoglaló

*TEREMT002_KUTATAS_BRIEF.md T1.1 · 2026.09.25 · ág: `teremt002-t1`*

**Előállítás:** `python eszkozok/t1_teremt002_munkalap.py --nyers <repón kívül> --ir`
(221 `lekerdez.py`-futás, egy menetben, `ts=2026-09-25T11:02Z`–`11:05Z`).
Minden futás proveniencia-sora szó szerint: `T1_TEREMT002_auditok_munkalap.tsv`
(221 sor + 1 „nem alkalmazható” sor). Jelöltek: `T1_TEREMT002_jeloltek_munkalap.tsv`
(66 sor, mind `nyitva`). Nem-jelölt találatok: `T1_TEREMT002_masodrendu_talalatok.tsv`
(983 igehely). Az `adat/` érintetlen (G3).

> **Hatókör-fenntartás.** A `TAHOT-teljes` scope a kivonat egészére vonatkozik, nem az ÓSZ
> kánonjára: a kivonatból hiányzik legalább 1Móz 32, Zsolt 88/89/140/142, Jóel 3 (CLAUDE.md,
> „Adat-tár”). Minden alábbi „teljes” szám ennyivel gyengébb.

---

## 1. Gerinc-metszet (1. lépés, B2)

`gerinc "1Móz 1:2" "Jer 4:23" "Ézs 34:11"` — a három vers 14 / 13 / 16 egyedi Strong-száma;
szűretlen metszet 3, ebből a grammatikai szűrő kiveszi a `H9002`-t (kötőszó *wᵉ-*).

**Gerinc: `H0922` (*bohu*) + `H8414` (*tohu*).** Más közös tartalmi Strong nincs.

`scope=range:1Móz 1:2+Jer 4:23+Ézs 34:11 | forras=TAHOT_kivonat.tsv | n=2 | ts=2026-09-25T11:02Z`

## 2. Szemantikai mező-hipotézis (2. lépés, B3 — generatív, Opus)

*Értelmezés, nem lekérdezés-eredmény. A domén-futás támasz (l. 2.2), nem helyettesítő.*

### 2.1 Mező-szavak

A hipotézis két irányt választ szét, mert a *tohu* maga is kettéágazik (l. 2.2): a
**pusztaság / formátlanság** (a motívum mezeje) és a **semmiség / hiábavalóság** (a
fölérendelt fogalom felé húzó ág). A mező-szavakat a gerinccel kollokáltattam (4. lépés),
hogy kiderüljön, melyik ágon állnak.

| Strong | Szó | Ág | Indok (egy mondat) | Kollokáció H8414-gyel |
|---|---|---|---|---|
| H0216 | אוֹר *ór*, „világosság” | pusztaság | A Jer 4:23 a teremtés első napjának visszavonását a világosság hiányával mondja ki. | 1 — Jer 4:23 |
| H6957 | קַו *kav*, „mérőkötél” | pusztaság | Az Ézs 34:11 „a *tohu* mérőkötele” az építő mérést rombolásra fordítja (vö. 2Kir 21:13, Sir 2:8). | 1 — Ézs 34:11 |
| H0068 | אֶבֶן *even*, „kő” | pusztaság | Ugyanabban a képben a *bohu* köveivel pár (függőón). | 1 — Ézs 34:11 |
| H4057 | מִדְבָּר *midbár*, „puszta” | pusztaság | A *tohu* térbeli, sivatagi jelentésének kísérője. | 1 — 5Móz 32:10 |
| H8077 | שְׁמָמָה *semámá*, „pusztulás” | pusztaság | A Jer 4:27 és a prófétai ítélet-nyelv sztereotip pusztulás-szava. | **0** |
| H0950 | בּוּקָה *buká*, „üresség” | pusztaság | Hangzásbeli párképzés, mint a *tohu wa-bohu* (Náh 2:10: *buká u-mᵉvuká*). | **0** |
| H4003 | מְבוּקָה *mᵉvuká*, „üresség” | pusztaság | A H0950 párja ugyanabban a versben. | (H0950+H4003: 1 — Náh 2:10) |
| H1238 | בָּקַק *bákak*, „kiüresít” (ige) | pusztaság | Az Ézs 24:1 „kiüresíti a földet” a 24:10 *qirjat-tohu*-jának közvetlen kerete. | **0** (H0922-vel is 0) |
| H0657 | אֶפֶס *efesz*, „semmi” | semmiség | Az Ézs 40:17 a *tohu*-t a népek semmisségére alkalmazza. | 2 — Ézs 40:17, 41:29 |
| H0205 | אָוֶן *áven*, „álnokság, semmiség” | semmiség | A bálvány-polémiában a *tohu* párja. | 2 — Ézs 41:29, 59:4 |
| H7385 | רִיק *rík*, „hiábavaló” | semmiség | Az Ébed Jahve panaszában a *tohu* párja. | 1 — Ézs 49:4 |
| H1892 | הֶבֶל *hevel*, „pára, hiábavalóság” | semmiség | Ugyanott, a hiábavaló fáradozás harmadik szava. | 1 — Ézs 49:4 |

**Lelet:** a pusztaság-ág kísérőszavai *verson belül* csak a három magversben és az 5Móz
32:10-ben állnak a *tohu* mellett; a sztereotip pusztulás-szókincs (H8077, H0950, H1238)
egyetlen *tohu*-versben sem fordul elő. A semmiség-ág szavai kizárólag Ézsaiás 40–59
bálvány- és panaszszövegeiben kollokálnak.

### 2.2 Domén-támasz (SDBH)

- `domen H8414 H0922` — **1 közös domén: `002002002006 Non-Exist`** (*tohu*: „waste;
  desolation; chaos”; *bohu*: „emptiness; wasteland”).
- `domen H8414` — **két jelentés-egység**: `…001001000` Non-Exist, **11** hivatkozás;
  `…001002000` Worthless („nothing; useless; worthless; in vain”), **9** hivatkozás
  (összesen 20 = a scan 20 szó-előfordulása).
- `domen H0922` — egyetlen jelentés-egység, Non-Exist.

A *bohu* tehát csak a pusztaság-ágon él; a *tohu* SDBH szerint közel fele-fele arányban
oszlik. Az igehelyenkénti SDBH-besorolás a repóban nincs meg (a `SDBH_domenek.tsv` csak
a hivatkozás-számot tárolja), ezért a 3. pont ág-besorolása **értelmezés** (`manual`).

## 3. Lépésenkénti találatszám

| # | Lépés | Futás | Találat |
|---|---|---|---|
| 1 | `gerinc` | 1 | 2 Strong (H0922, H8414) |
| 2 | `domen` (B3-támasz) | 3 | 1 közös domén; H8414: 2 jelentés-egység |
| 3 | `scan H8414` | 1 | **19 vers, 20 szó-előfordulás** (1Sám 12:21-ben kétszer) |
| 3 | `scan H0922` | 1 | **3 vers** |
| 4 | `kollokacio H8414 H0922` | 1 | **3 vers: 1Móz 1:2, Jer 4:23, Ézs 34:11** |
| 4 | mező-kollokációk | 13 | l. 2.1 (4 nulla) |
| 5 | `igealak` — gerinc | 0 + 1 sor | **nem alkalmazható**: H8414 és H0922 főnév (`scope=manual` sor az auditban) |
| 5 | `igealak H1238` — mező igei tagja | 1 | 9 alak, 7 vers (Hós 10:1 homonim: „buján tenyészik” — kiesik) |
| 6 | `lxx-hid` | 19 + 39 | l. 5. pont |
| — | `tsk` | 19 + 52 | a 3 magversre 45 célpont |
| — | `karoli` | 19 + 52 | a 3 magversre 7 KH-célpont (ebből 5 adathiba-gyanús, l. 6.) |

*(A „+” utáni szám a jelöltté lett 47 kereszthivatkozás-célpontra futott lekérdezés —
52 vers, az `lxx-hid` ebből a 39 ÓSZ-versre; a tartomány-célpontok — `Zsolt 80:6-7`, `Ez 34:12-16` — versenként futottak, mert a
`lekerdez.py` tartományt nem fogad.)*

## 4. A 0.4 hipotézis mérése (K8)

**MEGERŐSÍTVE.** A napló állítása — a H8414 + H0922 pár a teljes ÓSZ-ben 3 igehelyen:
1Móz 1:2, Jer 4:23, Ézs 34:11 — a `kollokacio` szerint pontosan igaz (TAHOT-teljes +
TAGNT-teljes hatókörön, l. a fenntartást). Sőt erősebb: a *bohu* **csak** ebben a három
versben fordul elő, tehát a pár nem csupán „együtt” ritka — a *bohu* önállóan nem létezik.

`scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H8414+H0922 | n=3 | ts=2026-09-25T11:02Z`

## 5. LXX-híd (6. lépés)

A LXX a *tohu*-t **nem fordítja egységesen**, és a párt sem:

| Igehely | LXX (a *tohu* / a pár helyén) |
|---|---|
| 1Móz 1:2 | ἀόρατος καὶ ἀκατασκεύαστος |
| Jer 4:23 | οὐθέν (a pár egyetlen szóval) |
| Ézs 34:11 | σπαρτίον γεωμετρίας ἐρήμου (a *bohu*-kő elmarad) |
| 5Móz 32:10; Ézs 24:10 | ἔρημος / ἐρημόω |
| Zsolt 107:40 | ἄβατος |
| Ézs 45:18; 49:4; 59:4 | κενός / κενῶς |
| Ézs 44:9; 45:19 | μάταιος |
| 1Sám 12:21; Jób 26:7; Ézs 40:17, 23 | οὐθέν / οὐδέν |
| Ézs 41:29 | μάτην |

**Következmény:** nincs olyan görög lexéma, amelyen az ÚSZ felé lexikai híd állna. A
`lxx-hid` által listázott ÚSZ-előfordulások (pl. G0517 ἀόρατος → Kol 1:15, Róm 1:20)
a „láthatatlan Isten” jelentésben állnak, nem a teremtés-visszavonásban — zaj. A TSK
ÚSZ-célpontjai (Mt 24:29, Mk 13:24-25, Luk 21:25-26, ApCsel 2:19-20, Jel 18, Jel 20:11)
kozmikus elsötétülés-, illetve Babilon-bukás-szövegek, **lexikai horgony nélkül**. A
napló „ÓSZ↔ÓSZ (belső)” besorolását a lekérdezés alátámasztja.

## 6. Jelölt-halmaz és anomáliák

**66 jelölt** (`nyitva`, G4):

| Típus | n | gerinc_elem-javaslat (G5) |
|---|---|---|
| a pár (kollokáció) | 3 | `tohu+bohu` |
| önálló *tohu* | 16 | `tohu` |
| önálló *bohu* | 0 | — (a *bohu* csak a párban él) |
| a magversek TSK-célpontjai | 40 | nincs lexikai horgony — a T2.1 dönt |
| a magversek Károli-KH-célpontjai | 7 | nincs lexikai horgony — a T2.1 dönt |

A 16 önálló *tohu* közül 3 a magversek TSK-célpontja is (Jób 26:7, Ézs 45:18 ← 1Móz 1:2;
Ézs 24:10 ← Ézs 34:11); a magversek közül a Jer 4:23 és az 1Móz 1:2 kölcsönösen egymásé.

**Nem jelölt, de rögzített:** 983 másodrendű találat (a 16 nem-mag *tohu*-vers és a 47
kereszthivatkozás-jelölt TSK/KH-célpontjai, az `igealak H1238` versei, a mező-kollokációk
jelölt-halmazon kívüli verse). Rekurzió nincs; jelöltté léptetésük gate-kérdés.

**Anomáliák (nem javítva — közös fájlok, §1):**

1. **`Karoli_kereszthivatkozasok.tsv`: az `Isa.34.11` KH-listája betűre azonos az
   `Isa.40.11`-ével** (Ézs 66:12, Ez 34:12-16, Ján 10:11, 1Móz 33:13, 4Móz 11:12 — a
   pásztor-kép). Az `Ézs 34:11`-re valószínűleg hibás a lista; a `Karoli_adatminosegi_anomaliak.tsv`
   nem tartalmazza. Az öt jelölt `indoklas`-a ADATHIBA-GYANÚ jelzést kapott.
2. A `lekerdez.py` `lxx-hid` / `tsk` / `karoli` parancsa tartományt nem fogad
   (`ValueError: nem elemezhető igehely`); a generátor versenként futtat.
3. A domén-futás a B3 támasza, az `auditok.tsv` `lepes` mezőjének zárt készlete
   (`A5 | B2 | B4`, SEMA 2.9) viszont nem ismer B3-at. A munkalapon `B3` áll (3 sor) —
   gate-kérdés.
