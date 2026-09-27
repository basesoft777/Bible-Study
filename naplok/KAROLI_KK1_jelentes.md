# KAROLI_KK1_jelentes.md — ok-besorolás

*KK1 — KAROLI_KULCS_BRIEF.md §3 szerint. Szkriptek:
`naplok/KAROLI_KK1_fejezetosztaly_general.py` (39 ószövetségi könyv minden
fejezete, osztályba sorolva), `naplok/KAROLI_KK1_ok_besorolas.py` (a
`szamozas_elteres` versek okonkénti bontása). Kimenet:
`naplok/KAROLI_KK1_fejezetosztaly.tsv`, `naplok/KAROLI_KK1_15sor.tsv`,
`naplok/KAROLI_KK1_ok_besorolas_reszletek.tsv`.*

## (a) 39 ószövetségi könyv, minden fejezet — osztályba sorolva

`karoli_max` = `Karoli_1908.tsv` (az `Karoli_ures_helyorzo_sorok.tsv` törölt
sorai nélkül); `kjv_max` = `verse_pairs.jsonl` `mt_refs` (KJV-számozás);
`mt_max` = `TAHOT_kivonat.tsv`.

| Osztály | Fejezetek száma | Arány |
|---|---|---|
| **KJV** (Károli = KJV) | 786 | 87,7% |
| **MT** (Károli = MT, KJV-től eltér) | 84 | 9,4% |
| **KEZI** (van aktív `KEZI_ELTOLASOK`-szakasz a fejezetben) | 13 | 1,5% |
| **EGYIK_SEM** | 13 | 1,5% |
| **Összesen** | 896 | 100% |

**A 13 `EGYIK_SEM` fejezet** (mindegyik kézi, tartalmi egyeztetést igényel,
G5 szerint):

| Könyv | Fejezet | Károli | KJV | MT |
|---|---|---|---|---|
| 2Móz | 35 | 36 | 35 | 35 |
| 2Móz | 36 | 37 | 38 | 38 |
| Jób | 17 | 15 | 16 | 16 |
| Jób | 37 | 23 | 24 | 24 |
| Péld | 12 | 27 | 28 | 28 |
| Én | 5 | 19 | 16 | 16 |
| Én | 6 | 10 | 13 | 13 |
| Ézs | 4 | 5 | 6 | 6 |
| Ézs | 64 | 11 | 12 | 12 |
| Dán | 3 | 33 | 30 | 30 |
| Hós | 2 | 22 | 23 | 23 |
| Hós | 13 | 15 | 16 | 16 |
| Hós | 14 | 10 | 9 | 9 |

Ezek jellemzően fejezethatár-eltolások (a Hós 13/14 és Ézs 63/64 pár a
klasszikus "az utolsó MT-vers a KJV-ben már a következő fejezet 1. verse"
mintázat), amit sem a tiszta KJV-, sem a tiszta MT-egyezés nem old meg —
verssoronkénti tartalmi egyeztetés kell (2. menetre halasztva, G5).

**Tartalmi próba** (a §1 mérce szerinti minta, a full KJV-szöveg
hiánya miatt — l. FORRASJELOLTEK FJ3 — az angol KJV helyett a LXX görög
szövegen és a TAHOT héber tükörfordításon végezve, a `LXX_OS/README.md` 2.
szakaszának már meglévő 27 mintasorával együtt): a KK0 0.8 pontban
ellenőrzött Jón 2:3 (Károli = raw LXX, nem az eltolt cél) és a
`LXX_OS/README.md`-ben dokumentált 27 minta (100%-os egyezés) alapján a
KJV/MT-osztályozás megbízhatónak tekinthető. **Korlátozás, amit a K4
elfogadási feltételnél figyelembe kell venni:** a §1 által kért, teljes
angol KJV-szövegen végzett, 10%-os véletlen mintavételes, ≥98%-os próba
**nem végezhető el ebben a menetben**, mert a teljes KJV-szöveg nem
elérhető (FORRASJELOLTEK FJ3: `studybible.info` proxy-blokkolt, nincs
alternatív teljes KJV-forrás). A fenti, kisebb, de valódi mintaellenőrzés
(27+1 tartalmi egyezés) ezt helyettesíti — ez K4 alá esik, l. lent.

## (b) Az 1 015 (itt mérve: 985, 97%-os lefedettséggel — l. korlátozás lent)
érintett LXX-vers okonkénti bontása

| Ok | Verssorok | Arány |
|---|---|---|
| **H2** — Károli MT-számozást követ, az importer nem ismeri | 573 | 58,2% |
| **H3** — egyéb Károli-sajátosság (`EGYIK_SEM` fejezet) | 223 | 22,6% |
| **H5** — valódi vers-tartalmi LXX-eltérés (a fejezet egyébként KJV-osztályú) | 96 | 9,7% |
| **H1** — importer-hiba (`KEZI_ELTOLASOK` `None`-ja tévesen a fejezet-őrre esik) | 93 | 9,4% |
| **Összesen mérve** | 985 | 97,0% a 1015-ből |

**Korlátozás:** a szkript 39 könyv 38 LXX_OS-fájlját dolgozza fel (a
`psalms-lxx.tsv`-t kihagyva — a Zsoltárok saját, már külön kezelt
cím-eltolás-logikával rendelkeznek, `zsolt_felirat_eltolas`, és a 63
zsoltár-fejezetnyi `szamozas_elteres` sor egy külön, komplexebb
napirendi pont, amit a KK2 kulcstábla-tervezetnek külön kell kezelnie —
ebben a jelentésben nem bontottuk H1–H5-re, mert a Zsoltárok saját
cím-eltolás-algoritmusa más logikájú, mint a sima fejezet-max-egyezés).
Emiatt 985/1015 (97,0%) a mért lefedettség; a fennmaradó 30 vers a
Zsoltárokból jön.

**Legfontosabb megállapítás:** a domináns ok **H2** (58%) — a jelenlegi
`resolve_karoli` egyáltalán nem ismeri a "Károli MT-számozást követ" esetet,
csak KJV-egyezést és a Zsoltár-cím-eltolást vizsgálja. Ez sokkal nagyobb
hatású hiba, mint amit az FJ2 feltételezett.

## (c) A lexikon 15 sora — egyenként

l. `naplok/KAROLI_KK1_15sor.tsv`. Összegzés:

| Ok | Sorok száma | Sorok |
|---|---|---|
| H1 (importer-hiba, KEZI) | 3 | Jób 38:7, 38:16, 38:30 |
| H2 (Károli MT-számozás) | 4 | Józs 13:12, Ézs 63:13, Jón 2:3, Jón 2:6 |
| H3 (egyéb, kézi egyeztetés) | 3 | Jób 17:13, 17:16, Hós 13:14 |
| **H4 (lexikonoldali forrásválasztás — ÚJ, az FJ2-ben H4-ként feltételezett, most megerősítve)** | 4 | Józs 12:4, 15:8, 17:15, 18:16 |
| H5 (valódi LXX-eltérés) | 1 | Jer 51:46 |

**H4 megerősítve, konkrét bizonyítékkal:** a `konkordancia/LXX_OS/joshua-vaticanus-b.tsv`
mind a 4 érintett Józsué-versnél (12:4, 15:8, 17:15, 18:16) **már ki van
töltve** helyes `igehely_karoli`-val (`karoli_ok` üres) — pl. a 12:4 sora
`Józs 12:4`-et ad, tartalmilag egyezik is ("Ωγ βασιλεὺς τῆς Βασαν" =
"Ógnak, a Básán királyának", már a `LXX_OS/README.md` 27 mintájában is
szerepel). A `joshua.tsv` (Alexandrinus A-szöveg) viszont **csak 3
fejezetet fed** (15, 18, 19), a 12. és 13. fejezetet egyáltalán nem — ha a
lexikonoldal-generátor ezt a hiányos fájlt nézi elsődlegesen (vagy nem
esik vissza a B-szövegre, amikor az A-szöveg nem ad találatot), pontosan a
megfigyelt hibát kapja. **Ez nem forrásjelölt-kérdés (G6 szerint javaslat,
nem javítás ebben a menetben) — a generátor LXX-forrás-választási
logikájának felülvizsgálatát igényli.**

## (d) FJ2-felülvizsgálat (G7)

A FORRASJELOLTEK-menet FJ2-jelentése (`naplok/FORRAS_FJ2_szamozas.md` a
`claude/peaceful-rubin-39uuzs` ágon) **három ponton nem tartható**, a KK0/KK1
mérései alapján:

1. **"13/15 sor a repó saját `LXX_OS`-kivonatolási hézaga, nem valódi
   eltérés"** — **RÉSZBEN CÁFOLVA.** A `job-lxx.tsv` és `joshua-vaticanus-b.tsv`
   ténylegesen **teljes** (42/42, 24/24 fejezet, KK0 0.4) — nincs
   "kivonatolási hézag" a fájlokban. Az FJ2 tévesen azonosította hézagnak
   azt, hogy az `igehely_karoli` oszlop üres ezekben a sorokban (mert a
   `karoli_ok=szamozas_elteres`) — ez nem hiányzó adat, hanem a
   Károli-megfeleltető algoritmus (`resolve_karoli`) valódi, dokumentált
   korlátja (H1/H2/H3/H4/H5, l. fent).
2. **"Jón 2:3 → LXX 2:4, Jón 2:6 → LXX 2:7"** — **CÁFOLVA.** A KK0 0.8
   közvetlen tartalmi ellenőrzése szerint a Károli Jón 2:3 szó szerint a
   **nem eltolt** (raw) LXX Jonah 2:3-mal egyezik, nem a `verse_pairs.jsonl`
   TVTMS-térkép szerinti 2:4-gyel. Az FJ2 a `verse_pairs.jsonl`-t közvetlenül,
   MT→KJV irányban használta fel Károli-célként — ez pontosan az a hiba,
   amit a `LXX_OS/README.md` 2. szakasza explicit tilt ("A `verse_pairs.jsonl`
   `mt_refs` mezője csak az `igehely_kjv` oszlopba kerül... **nem forrása**
   az `igehely_karoli`-nak"). A helyes cél Jón 2:3 → LXX 2:3 (identitás,
   mert Károli itt MT-számozást követ, l. H2).
3. **"Károli-kulcsú tábla nem szükséges (2 eltérés/3660 vers)"** —
   **CÁFOLVA, méretaránytévesztés.** Az FJ2 csak 1Móz/2Móz/Péld könyvekre
   nézte a Károli–KJV eltérést (ahol tényleg minimális, 1–2 vers/könyv). A
   most feltárt 985+ érintett vers (39 könyv egészén) — és ebből 573+223=796
   olyan, amit a KEZI-táblák és a KJV-only logika **soha nem tud kezelni**
   MT- vagy tartalmi-egyeztetés nélkül — világosan mutatja, hogy egy
   teljes ószövetségi Károli-kulcstábla (G8 szerint is) szükséges, és ez
   éppen a G8 indoka (a 3b import-kulcsaként is szolgál majd).

**Nem cáfolt FJ2-megállapítás:** Jer 51:46 valódi LXX-eltérés (H5) — ez
megerősítve, változatlan.
