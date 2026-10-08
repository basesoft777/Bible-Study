# F83_Job_versbeosztas_jelentes.md — Jób 38–42 Károli–héber versmegfeleltetés előkészítése

*Feladat: FELADATOK #83 (`F83_JOB_VERSBEOSZTAS_BRIEF.md`), ág: `claude/f83-job-versbeosztas`. A menet csak olvasott; a kanonikus táblákat (`f22/versmegfeleltetes_kezi.tsv`, `f22/versosszevonas.tsv`, `naplok/F22_versbeosztas_jovahagyas.md`) nem írta — azok a ⛔ jóváhagyás után jönnek.*

*Egyeztetett keret (a felhasználó, az orkesztrátoron át): az 1. ellenőrzés forrása a `konkordancia/Macula_heber_Job.tsv` (MT/WLC), letöltés nincs; az N-F41g külön tétel marad (l. 4. szakasz).*

*A lekérdező szkriptek a repón kívül futottak (scratchpad: `f83_ellenor.py`, `f83_javaslat.py`), `split('\t')`-tel; a TSV-kre nem írtak.*

## 0. Összefoglalás

| | Eredmény |
|---|---|
| 1. ellenőrzés | A héber Jób 40:25–41:26 **megvan** a Macula-ban (34 vers, 229 szó). A `TAHOT_kivonat.tsv`-ben a Károli 41. fejezet kulcsán **0 sor** van; a 34 vers TAHOT-szavai (332 sor) a `TAHOT_kivonat_nyitott_esetek.tsv`-ben állnak, `ADATMINOSEGI_GYANU` státusszal. A hiba tehát valóban a kulcsgenerátorban van, nem a nyers adatban — és a gyanú-jelölés **hibás versszámokon** alapul (l. 3.). |
| 2. ellenőrzés | A Jób 42:2–9 (és az egész 42. fejezet, 17 vers) **nem hiányzik**: mind a 17 Károli-kulcson van TAHOT-adat, és a Macula-karoli oszlop is `identitas`. A brief 2. feltevése a repó adatával nem igazolható; továbbgyűrűzés nincs. |
| 3. ellenőrzés | A Károli 38–42 versszáma **38 / 38 / 19 / 34 / 17**, nem a briefben (és a kulcsgenerátor megjegyzésében) szereplő 40 = 28, 41 = 25. Összesen 146 vers, pontosan annyi, mint az MT 38–42-ben (41 / 30 / 32 / 26 / 17). |
| **Új lelet** | A `TAHOT_kivonat.tsv` Jób 40. fejezete **MT-kulcsos** (kulcsok 40:6–24), nem Károli-kulcsos: a TAHOT „Jób 40:n” = MT 40:n = Károli 40:(n−5). A Károli-kulcs szerinti azonosítás (és a detektor implicit identitás-párja) itt 5 verssel eltolt tartalmat adna. |
| Javaslat (2.) | 146 Károli-vers ↔ 146 MT-vers, **mind 1:1**; 1:2 és 2:1 eset **nincs**. Öt szegmens, négy határ-eltolással. |

## 1. ellenőrzés — a héber Jób 40:25–41:26 a Macula-ban és a TAHOT_kivonat-ban

`scope=Jób 40:25–41:26, versenkénti szó- és morfémaszám; TAHOT_kivonat Károli-kulcs Jób 38–42; TAHOT_kivonat_nyitott_esetek Job.* sorok | forras=konkordancia/Macula_heber_Job.tsv (Macula-hebrew commit 47db250, CC BY 4.0), konkordancia/TAHOT_kivonat.tsv, konkordancia/TAHOT_kivonat_nyitott_esetek.tsv | ts=2026-10-08T17:28:12Z`

**Macula (MT/WLC):** a 40:25–41:26 szakasz mind a 34 verse megvan, összesen **229 szó** (versenként 5–10 szó; a szó = az `xml_id` utolsó számjegy nélküli része, a morféma-sorok összevonva). A Macula saját `karoli` oszlopa a szakaszt `terkep` / `javaslat:terkep_ellenorzesre_var` jelöléssel a Károli 41:1–34-re képezi (MT 40:25 → Károli 41:1 … MT 41:26 → Károli 41:34).

| MT | szó | MT | szó | MT | szó | MT | szó |
|---|---|---|---|---|---|---|---|
| 40:25 | 6 | 41:1 | 7 | 41:10 | 6 | 41:19 | 6 |
| 40:26 | 6 | 41:2 | 8 | 41:11 | 6 | 41:20 | 9 |
| 40:27 | 7 | 41:3 | 8 | 41:12 | 6 | 41:21 | 6 |
| 40:28 | 6 | 41:4 | 7 | 41:13 | 6 | 41:22 | 7 |
| 40:29 | 6 | 41:5 | 8 | 41:14 | 6 | 41:23 | 8 |
| 40:30 | 6 | 41:6 | 7 | 41:15 | 7 | 41:24 | 6 |
| 40:31 | 6 | 41:7 | 6 | 41:16 | 7 | 41:25 | 7 |
| 40:32 | 7 | 41:8 | 7 | 41:17 | 5 | 41:26 | 10 |
| | | 41:9 | 6 | 41:18 | 7 | | |

**TAHOT_kivonat.tsv (Károli-kulcs):** Jób 41:* kulcson **0 sor**; a Jób 40 kulcsai csak **40:6–40:24** (19 kulcs, 198 sor), 40:25 feletti kulcs nincs.

**TAHOT_kivonat_nyitott_esetek.tsv:** 332 Jób-sor, mind `ADATMINOSEGI_GYANU` státuszú, 34 versnyi párban: elsődleges (angol) `Job.41.1`–`Job.41.34` ↔ másodlagos (héber) `Job.40.25`–`Job.41.26` (83 sor a 40. fejezeti, 249 a 41. fejezeti héber versekre). A 34 pár Strong-halmaza a Macula azonos MT-versével Jaccard 0,71–1,00 (medián 0,86; H9xxx elöljárók nélkül), tehát a nyers TAHOT-tartalom a teljes szakaszra **megvan és helyes**, csak nem került kulcsra.

**Ok (a kulcsgenerátorban):** `eszkozok/tahot_karoli_kulcs_generalas.py`, `DONTES_FELULBIRALAS[("Job", (40, 41))] = ADATMINOSEGI_GYANU`, indoklása: „a Karoli tenyleges 40. (28v) es 41. (25v) fejezet-hossza” egyik hipotézissel sem egyezik. A 3. ellenőrzés szerint a Károli 40 = **19**, 41 = **34** vers; az elsődleges (angol) 41. fejezet hossza (34) tehát **egyezik** a Károli 41-gyel. A gyanú-jelölés hibás számokon alapult; a 41. fejezetre az `ELSODLEGES` döntés helyes kulcsot adott volna (Job.41.n → Jób 41:n), ezt a 2. szakasz tartalmi összevetése is megerősíti.

## 2. ellenőrzés — Jób 42:2–9

`scope=Jób 42:1–17 versenként: Károli-vers megléte, TAHOT_kivonat sorszám, Macula szószám és karoli-oszlop | forras=konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/Macula_heber_Job.tsv, eszkozok/tahot_karoli_kulcs_generalas.py | ts=2026-10-08T17:28:12Z`

| vers | Károli | TAHOT sor | Macula szó | | vers | Károli | TAHOT sor | Macula szó |
|---|---|---|---|---|---|---|---|---|
| 42:1 | van | 7 | 5 | | 42:10 | van | 22 | 15 |
| 42:2 | van | 10 | 8 | | 42:11 | van | 54 | 33 |
| 42:3 | van | 18 | 14 | | 42:12 | van | 28 | 20 |
| 42:4 | van | 10 | 6 | | 42:13 | van | 9 | 6 |
| 42:5 | van | 11 | 6 | | 42:14 | van | 17 | 11 |
| 42:6 | van | 9 | 7 | | 42:15 | van | 23 | 14 |
| 42:7 | van | 39 | 26 | | 42:16 | van | 21 | 15 |
| 42:8 | van | 49 | 33 | | 42:17 | van | 7 | 5 |
| 42:9 | van | 26 | 17 | | | | | |

- A 42:2–9 **nem hiányzik** a `TAHOT_kivonat`-ból (8 vers, 172 sor). A TAHOT- és a Macula-Strongsor 42:1–17-ben 15 versben azonos, a 42:12 és 42:14 kisebb Strong-eltérés (nem eltolás). A Macula `karoli` oszlopa 42:1–15-re `identitas`, 42:16–17-re `terkep`, mind `rendben`.
- A kulcsgenerátorban a 42. fejezetnek nincs külön kezelése (a `DONTES_FELULBIRALAS` csak a (40, 41) csoportot érinti), az `ADATMINOSEGI_GYANU`-sorok között 42-es elsődleges vagy másodlagos kulcs nincs.
- A detektor (`naplok/F22_versbeosztas.md`, Jób 42: 17/17, r = 0,95) és a gépi lista (`f22/versmegfeleltetes.tsv`: Jób 42-sor nincs) ugyanezt mutatja.
- **Következtetés:** a 42:2–9 hiánya a repó adatával nem igazolható; sem önálló hiba, sem a 41. fejezet továbbgyűrűzése nincs. A feltevés forrása a repóban nem található (a „42:2–9” csak a briefben szerepel); valószínűleg egy korábbi, a mostani `TAHOT_kivonat` előtti állapotra vagy más táblára vonatkozott — ez **értelmezés**, nem lekérdezett tény.

## 3. ellenőrzés — a Károli 38–42 versszámai, összevetve az MT-vel és az F22-vel

`scope=Jób 38–42 fejezethosszak (versdarab és legnagyobb versszám) három táblában + az F22 gépi lista Jób-sorai | forras=konkordancia/Karoli_1908.tsv, konkordancia/Macula_heber_Job.tsv, konkordancia/TAHOT_kivonat.tsv, f22/versmegfeleltetes.tsv, naplok/F22_versbeosztas.md | ts=2026-10-08T17:28:12Z`

| fejezet | Károli_1908 (közvetlen) | Macula MT | TAHOT_kivonat kulcsok | F22 napló: Károli / eredeti / K-hiány |
|---|---|---|---|---|
| 38 | 38 (1–38) | 41 | 38 (1–38) | 38 / 38 / 0 |
| 39 | 38 (1–38) | 30 | 38 (1–38) | 38 / 38 / 0 |
| 40 | **19** (1–19) | 32 | 19 (**6–24**) | 19 / 19 / 8 |
| 41 | **34** (1–34) | 26 | 0 | 34 / 0 / 26 |
| 42 | 17 (1–17) | 17 | 17 (1–17) | 17 / 17 / 0 |
| össz. | **146** | **146** | 112 | |

- A Károli-forrás versszámai **38 / 38 / 19 / 34 / 17**. A brief (és a kulcsgenerátor megjegyzése) szerinti „40 = 28, 41 = 25” **nem igaz**; a F22-napló Károli-oszlopa viszont helyes.
- A Károli 39 elején az MT 38:39–41 (oroszlán, holló), a végén az MT 40:1–5 (az Úr első felszólítása és Jób első válasza) áll; a Károli 40 az MT 40:6–24, a Károli 41 az MT 40:25–41:26.
- **TAHOT_kivonat Jób 38–39:** Károli-kulcsos és helyes (a 38:8, 12, 15, 29, 35 és néhány 39-es vers kisebb Strong-eltérése nem eltolás) — a TAHOT „39:1–3” Strongsora az MT 38:39–41-gyel, a „39:34–38” az MT 40:1–5-tel egyezik (lekérdezés: Strongsor-azonosság a Macula-versekkel).
- **TAHOT_kivonat Jób 40: MT-kulcsos.** A TAHOT „40:n” (n = 6–24) Strong-halmaza az MT 40:n-nel Jaccard 0,62–0,90, az MT 40:(n−5)-tel 0,00–0,06 (egy kivétel: a TAHOT 40:6 a formulaazonosság miatt az MT 40:1-gyel is 0,62). A Károli 40:1 („Ekkor szóla az Úr Jóbnak a forgószélből”) tartalma = MT 40:6 („and he answered Yahweh Job from a tempest”) = TAHOT-kulcs 40:6. A kulcsok tehát a Károli 40:(n−5)-nek felelnek meg.
- **Az F22 gépi lista Jób 40–41 sorai használhatatlanok:** 34 `nincs_eredeti` sor (Károli 40:1–5, 40:13, 40:16, 40:19 és 26 sor a 41-ből: 41:1–4, 6, 9, 10, 13–22, 24–26, 28–33). A többi Károli 40-es versre a detektor implicit identitás-párt ad (Károli 40:n ↔ TAHOT 40:n), ami 5 verssel eltolt tartalom; a 41-ből 8 vers (41:5, 7, 8, 11, 12, 23, 27, 34) nem szerepel a listában — a detektor ezeket valószínűleg a TAHOT 40-es kulcsaihoz párosította, magányos, a `MIN_SZEGMENS` alatti eltolásként (értelmezés a detektor docstringje alapján, nem lekérdezés). A detektor a hosszeltérésre épít, a kulcshibát nem látja.

## 4. Átfedés az N-F41g-vel (nem zárja le)

Az N-F41g (`NYITOTT_FELADATOK.md`) a `BSB_Strongs.tsv` Jób 38–41 `Igehely`-ét hozná MT/WLC-számozásra, gépi táblából. Ugyanazt a három határ-eltolást érinti (MT 38:39–41, 40:1–5, 40:25–41:26), de **más tábla, más célszámozás** (BSB → MT; itt Károli → MT). A 2. szakasz Károli↔MT leképezése és a DT-F41b-ben rögzített Macula-leképezés (KJV 41:1–8 = MT 40:25–32, 41:9–34 = MT 41:1–26) a 41. fejezetben egybeesik, mert ott a Károli = KJV. A 38–40. fejezetben a Károli **nem** KJV-számozású (a KJV 38 = 41, 39 = 30, 40 = 24 vers), tehát a két leképezés ott eltér. Az N-F41g külön tétel marad (egyeztetett döntés).

## 5. Megfeleltetési JAVASLAT — Károli → MT, Jób 38–42 (nem jóváhagyott)

`scope=Jób 38–42, 146 Károli-vers ↔ 146 MT-vers: lefedés, Macula-karoli oszlop, szószám-korreláció (d = −1, 0, +1), Strong-Jaccard a TAHOT-kulcsokon és a nyitott eseteken, határ-versek glosszái | forras=konkordancia/Karoli_1908.tsv, konkordancia/Macula_heber_Job.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAHOT_kivonat_nyitott_esetek.tsv | ts=2026-10-08`

**⛔ Ez javaslat, a felhasználó jóváhagyására vár.** A `f22/versmegfeleltetes_kezi.tsv`, a `f22/versosszevonas.tsv` és a `naplok/F22_versbeosztas_jovahagyas.md` nem változott.

### 5.1 Szegmensek

| Károli | MT (Macula/WLC) | viszony | versek | tartalmi horgony (rövid) |
|---|---|---|---|---|
| 38:1–38 | 38:1–38 | 1:1, azonos szám | 38 | — |
| 39:1–3 | 38:39–41 | 1:1, fejezethatár-eltolás | 3 | K 39:1 „prédát a nőstény oroszlánnak” = MT 38:39 „hunt prey for a lion”; K 39:3 „a hollónak eledelt” = MT 38:41 „for the raven food” |
| 39:4–33 | 39:1–30 | 1:1, −3 eltolás | 30 | K 39:4 „kőszáli zergék ellésének idejét” = MT 39:1 „bringing forth of mountain goats”; K 39:33 „Fiai vért szívnak” = MT 39:30 „its young ones drink blood” |
| 39:34–38 | 40:1–5 | 1:1, fejezethatár-eltolás | 5 | K 39:34 „Szóla továbbá az Úr Jóbnak” = MT 40:1; K 39:38 „Egyszer szóltam … kétszer” = MT 40:5 „one time I have spoken … two times” |
| 40:1–19 | 40:6–24 | 1:1, +5 eltolás | 19 | K 40:1 „az Úr … a forgószélből” = MT 40:6 „from a tempest”; K 40:6 „Öntsd ki haragodnak tüzét” = MT 40:11 „scatter the furies of your anger”; K 40:19 „átfúrhatják-é az orrát” = MT 40:24 „pierce a nose” |
| 41:1–8 | 40:25–32 | 1:1, fejezethatár-eltolás | 8 | K 41:1 „leviáthánt horoggal … nyelvét kötéllel” = MT 40:25 „Leviathan with a fish hook … cord … tongue”; K 41:8 „a harczot nem ismételed” = MT 40:32 „remember the battle, do not repeat” |
| 41:9–34 | 41:1–26 | 1:1, −8 eltolás | 26 | K 41:9 „reménykedése csalárd” = MT 41:1 „hope … proved a lie”; K 41:34 „király minden ragadozó felett” = MT 41:26 „king over all the sons of pride” |
| 42:1–17 | 42:1–17 | 1:1, azonos szám | 17 | — |
| **össz.** | | **146 × 1:1; 1:2 = 0; 2:1 = 0** | **146** | |

### 5.2 Támasz (lekérdezés)

- **Lefedés:** a leképezés 146 Károli-versből 146 különböző MT-versbe visz; lefedetlen MT-vers nincs, nem létező MT-cél nincs.
- **Macula `karoli` oszlop:** mind a 146 MT-versnél ugyanazt a Károli-verset nevezi, mint a javaslat (0 eltérés); többes (`;`) Károli-hozzárendelés a 38–42-ben nincs. A Macula a 38:39–41 és 40:1–5 szakaszt `kezi_interpolalt`, a 40:25–41:26-ot `terkep` / `javaslat:terkep_ellenorzesre_var` jelöléssel adja — a javaslat ezeket a fenti horgonyokkal igazolja.
- **Szószám-korreláció** (Károli-szó vs. MT-szó, szegmensenként): d = 0-nál 0,39 (38), 0,45 (39), 0,46 (40), 0,47 (41), 0,96 (42); a ±1 eltolás mindenütt rosszabb (38: +1 → 0,01; 40: −1 → −0,30, +1 → 0,03). A költői fejezetek alacsony abszolút értéke a műfajjal jár (rövid, párhuzamos stichoszok), nem eltolódás.
- **Strong-Jaccard:** a TAHOT „40:n” kulcs az MT 40:n-nel 0,62–0,90 (tehát a Károli 40:(n−5)-tel egyezik); a nyitott esetek 34 párja az MT 40:25–41:26-tal 0,71–1,00.
- **Hosszarány:** a Károli/MT szóarány mediánja 1,57; egyetlen kiugró pár (> 1,6 × medián) a K 40:3 → MT 40:8 (2,83), tartalmilag egyezik („semmivé teheted-é … igazságomat; kárhoztathatsz-é” = „will you annul my justice, will you condemn me”) — a Károli bővebb fordítása, nem összevonás.

### 5.3 Kétes helyek

- **Nincs** olyan Károli-vers, amely két MT-vers tartalmát hordozná, és olyan MT-vers sem, amely két Károli-versre oszlana: a négy fejezethatár-eltolás (38/39, 39/40, 40/41 kétszer) tiszta versszám-átvitel. Ezért a Jóbnál **nem kell 1:2 / 2:1 versösszevonás** — a DT-F83a javaslata ezen alapul.
- A K 39:36 („És szóla Jób az Úrnak, és monda”) Strong-szinten a MT 40:3 mellett a 42:1-gyel is azonos (formula); a sorrend egyértelművé teszi (MT 40:3).
- A K 40:1 / MT 40:6 bevezető formula az MT 40:1-gyel is hasonló (Jaccard 0,62); a „forgószélből” / „from a tempest” csak az MT 40:6-ban áll.

### 5.4 Teljes lista (Károli → MT)

- **Károli 38:** 38:1→38:1 · 38:2→38:2 · 38:3→38:3 · 38:4→38:4 · 38:5→38:5 · 38:6→38:6 · 38:7→38:7 · 38:8→38:8 · 38:9→38:9 · 38:10→38:10 · 38:11→38:11 · 38:12→38:12 · 38:13→38:13 · 38:14→38:14 · 38:15→38:15 · 38:16→38:16 · 38:17→38:17 · 38:18→38:18 · 38:19→38:19 · 38:20→38:20 · 38:21→38:21 · 38:22→38:22 · 38:23→38:23 · 38:24→38:24 · 38:25→38:25 · 38:26→38:26 · 38:27→38:27 · 38:28→38:28 · 38:29→38:29 · 38:30→38:30 · 38:31→38:31 · 38:32→38:32 · 38:33→38:33 · 38:34→38:34 · 38:35→38:35 · 38:36→38:36 · 38:37→38:37 · 38:38→38:38
- **Károli 39:** 39:1→38:39 · 39:2→38:40 · 39:3→38:41 · 39:4→39:1 · 39:5→39:2 · 39:6→39:3 · 39:7→39:4 · 39:8→39:5 · 39:9→39:6 · 39:10→39:7 · 39:11→39:8 · 39:12→39:9 · 39:13→39:10 · 39:14→39:11 · 39:15→39:12 · 39:16→39:13 · 39:17→39:14 · 39:18→39:15 · 39:19→39:16 · 39:20→39:17 · 39:21→39:18 · 39:22→39:19 · 39:23→39:20 · 39:24→39:21 · 39:25→39:22 · 39:26→39:23 · 39:27→39:24 · 39:28→39:25 · 39:29→39:26 · 39:30→39:27 · 39:31→39:28 · 39:32→39:29 · 39:33→39:30 · 39:34→40:1 · 39:35→40:2 · 39:36→40:3 · 39:37→40:4 · 39:38→40:5
- **Károli 40:** 40:1→40:6 · 40:2→40:7 · 40:3→40:8 · 40:4→40:9 · 40:5→40:10 · 40:6→40:11 · 40:7→40:12 · 40:8→40:13 · 40:9→40:14 · 40:10→40:15 · 40:11→40:16 · 40:12→40:17 · 40:13→40:18 · 40:14→40:19 · 40:15→40:20 · 40:16→40:21 · 40:17→40:22 · 40:18→40:23 · 40:19→40:24
- **Károli 41:** 41:1→40:25 · 41:2→40:26 · 41:3→40:27 · 41:4→40:28 · 41:5→40:29 · 41:6→40:30 · 41:7→40:31 · 41:8→40:32 · 41:9→41:1 · 41:10→41:2 · 41:11→41:3 · 41:12→41:4 · 41:13→41:5 · 41:14→41:6 · 41:15→41:7 · 41:16→41:8 · 41:17→41:9 · 41:18→41:10 · 41:19→41:11 · 41:20→41:12 · 41:21→41:13 · 41:22→41:14 · 41:23→41:15 · 41:24→41:16 · 41:25→41:17 · 41:26→41:18 · 41:27→41:19 · 41:28→41:20 · 41:29→41:21 · 41:30→41:22 · 41:31→41:23 · 41:32→41:24 · 41:33→41:25 · 41:34→41:26
- **Károli 42:** 42:1→42:1 · 42:2→42:2 · 42:3→42:3 · 42:4→42:4 · 42:5→42:5 · 42:6→42:6 · 42:7→42:7 · 42:8→42:8 · 42:9→42:9 · 42:10→42:10 · 42:11→42:11 · 42:12→42:12 · 42:13→42:13 · 42:14→42:14 · 42:15→42:15 · 42:16→42:16 · 42:17→42:17

### 5.5 Következmény a futtatóra (javaslat, nem végrehajtva)

A F22 futtató az eredeti verset a `TAHOT_kivonat` kulcsán keresi (`eredeti` = TAHOT-kulcs), nem MT-számon. A TAHOT-kulcsok a 38, 39 és 42. fejezetben Károli-számozásúak, a 40-ben MT-számozásúak, a 41-ben hiányoznak. A jóváhagyás után ezért:

1. **Károli 38, 39, 42** (93 vers): identitás a TAHOT-kulccsal — kézi sor nem kell.
2. **Károli 40:1–19** → TAHOT-kulcs **40:6–24** (`eltolt`, 19 sor a `f22/versmegfeleltetes_kezi.tsv`-be; a detektor 8 hibás Jób 40-es `nincs_eredeti` sorát kiváltja).
3. **Károli 41:1–34**: a `TAHOT_kivonat`-ban nincs adat. Ez **nem versbeosztás-kérdés, hanem adatforrás-kérdés**, és a kézi táblával nem oldható meg. Lehetőségek (döntést igényel, a DT-F83a mellett): (a) a kulcsgenerátor `DONTES_FELULBIRALAS[("Job", (40, 41))]` javítása (a hibás 28/25 indoklás helyett `ELSODLEGES` a 41-re), és a 332 sor visszakerül a `TAHOT_kivonat`-ba Jób 41:1–34 kulccsal — ez a `konkordancia/` táblát írja, külön feladat; (b) a 41. fejezet eredetije a Macula-ból (MT 40:25–41:26) — a futtató forrását érinti, külön feladat; (c) a Jób 41 a #22-ben `kezi` marad, amíg (a) vagy (b) el nem készül. Javaslat: (a), mert a nyers adat megvan és a Strong-egyezés igazolja.

## 6. Jóváhagyás és végrehajtás (F83.5–F83.7)

**Jóváhagyás:** a felhasználó (chat, 2026.10.08, „1 igen 2 igen”, az orkesztrátoron át) elfogadta (a) az 5. szakasz megfeleltetési javaslatát és (b) a DT-F83a (1) opcióját: 1:2 / 2:1 összevonás-támogatás nem kell, a megfeleltetés kézi táblával megy.

### 6.1 Mi került a `f22/versmegfeleltetes_kezi.tsv`-be és mi nem (F83.5)

`scope=a kézi tábla Jób-sorai + a futtató szimulációja (tokenek.versmegfeleltetes(jovahagyott={'Jób'}), tokenek._versmegfeleltet a nyers TAHOT-kulcsokon) | forras=f22/versmegfeleltetes_kezi.tsv, f22/versmegfeleltetes.tsv, konkordancia/TAHOT_kivonat.tsv, eszkozok/karoli_strong/tokenek.py | ts=2026-10-08`

A futtató az `eredeti` oszlopban a **nyers `TAHOT_kivonat`-kulcsot** várja, nem MT-számot. Kézi sor ezért csak ott kell, ahol a TAHOT-kulcs eltér a Károli-kulcstól:

| Károli | TAHOT-kulcs | kézi sor | indoklás |
|---|---|---|---|
| 38:1–38 | 38:1–38 | **nincs** | a TAHOT 38-as kulcsa Károli-számozású (MT 38:1–38), identitás |
| 39:1–38 | 39:1–38 | **nincs** | a TAHOT 39-es kulcsa már Károli-számozású (a 39:1–3 = MT 38:39–41, a 39:34–38 = MT 40:1–5 tartalommal; 3. szakasz), identitás |
| 40:1–19 | 40:6–24 | **19 `eltolt` sor** | a TAHOT 40-es kulcsa MT-számozású; a kézi sor a detektor 8 hibás `nincs_eredeti` sorát (40:1–5, 13, 16, 19) is kiváltja |
| 41:1–34 | — | **nincs** | a `TAHOT_kivonat`-ban nincs Jób 41-kulcs; a detektor 26 `nincs_eredeti` sora és a kulcs hiánya együtt azt adja, hogy mind a 34 vers eredeti nélkül marad. Kézi `nincs_eredeti` sort szándékosan nem vettem fel: a kulcsgenerátor javítása után (Jób 41:n = Károli 41:n) a kézi sor felülírná a helyes identitást |
| 42:1–17 | 42:1–17 | **nincs** | identitás |

**Szimuláció (a futtató függvényeivel, a táblák írása nélkül):** leképezett Károli-kulcsok 38 / 38 / 19 / 0 / 17; a Károli 40:1 = nyers TAHOT 40:6, a 40:19 = nyers 40:24; a Jób 38–42 tokenszáma nyers/leképezett 1344 / 1344 (nem veszett el, nem duplázódott); gazdátlan (+1000) kulcs a 38–42-ben nincs.

**Hatókörön kívül, de a Jób felvételekor élesedik:** a detektor Jób 17 és 37 sorai (`eltolt` / `nincs_karoli`, 17:10–15, 37:21–23) a jóváhagyással együtt hatályba lépnek, és a szimulációban két gazdátlan kulcsot adnak (`Jób 17:1010`, `Jób 37:1021`). Ezeket a #83 nem vizsgálta; a #22 Jób-menetének kell átnéznie.

**Kötöttség:** a 19 kézi sor a mostani `TAHOT_kivonat` Jób 40-kulcsaihoz kötött. Ha a kulcsgenerátor javítása a Jób 40-et is átkulcsolja Károli-számozásra, ezeket a sorokat törölni kell.

### 6.2 Nyitott tétel — javaslat (N-F83a helyőrző, nem felvéve)

A `NYITOTT_FELADATOK.md` nincs a brief `ir` mezőjében, ezért nem írtam bele. **Javasolt tétel (N-F83a):** a `eszkozok/tahot_karoli_kulcs_generalas.py` `DONTES_FELULBIRALAS[("Job", (40, 41))]` javítása — a hibás „40 = 28, 41 = 25” indoklás helyett `ELSODLEGES` a 41. fejezetre —, és a `TAHOT_kivonat_nyitott_esetek.tsv` 332 Jób-sorának visszavétele a `TAHOT_kivonat.tsv`-be Jób 41:1–34 kulccsal, majd a detektor újrafuttatása. **A Jób 41 futtatása addig nem lehetséges** (34 vers eredeti nélkül).

### 6.3 A futtató jóváhagyott listája

A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT`-hoz ez a menet nem nyúlt (nincs az `ir`-ben). A Jób felvétele a #22 Jób-menetének első lépése, a Jób 41 hiányára tekintettel: vagy a N-F83a után, vagy a Jób 41 kizárásával / `kezi` kezelésével.
