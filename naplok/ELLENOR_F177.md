ELTÉRÉS: 2 tétel

# ELLENŐR — F177_KAROLI_KH_MEK_BRIEF.md · 55fa1573..e709614e (ág: claude/karoli-kh-mek)

*A jelentést a `fuggetlen-ellenor` subagent adta (friss kontextus, saját modell: claude-opus-5-5). Fájlíró eszköz híján nem tudta lemezre írni; a szövegét az orkesztrátor rögzítette változatlanul. Az orkesztrátor kiegészítése a fájl végén, külön szakaszban áll.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | Az ellenőr kért modellje `opus`, a sajátja `claude-opus-5-5`. A végrehajtó a jelentés szerint `claude-sonnet-5-5`; mind a 7 commit trailere „Claude Sonnet 5.5” (`git log --format='%h %an%n%B' 55fa1573..e709614e`). Az új táblákban nincs `modell` oszlop. |
| F177.0 #176 a main-ben | OK | — | `git log --oneline --grep='^F176' 55fa1573`: az f81a2d73 (a PR #649 merge-e) a base-ben van. |
| F177.1 kivonat, sorszám | OK | `konkordancia/Karoli_KH_MEK.tsv` | Grep-számlálás `^[A-Za-z0-9]+\.\d+\.\d+\t`: 29 987 sor. Üres `kapcsolodo` 3 sor (3906, 5762, 6066: `1 Sám. 12,.`, `2 Kir. 12,.`, `2 Kir. 21,.`). |
| F177.1 aliasok, versszerkezet | OK | `konkordancia/Karoli_KH_MEK_konyvaliasok.tsv:2-69`, `..._versszerkezet.tsv` | Aliasok: 67 `mek` sor (66 STEP-kód, plusz a `Neh.` duplikátum) és 1 `karoli_1908` sor (`Sir`→`Lam`). Versszerkezet: a numstat 1190 sor, fejléc nélkül 1189 fejezet. |
| F177.1 nyers fájl, SHA-256 | NEM ELLENŐRIZHETŐ | `konkordancia/Karoli_KH_MEK_README.md:16` | Letöltés nélkül nem mérhető (a `curl` kívül esik az ellenőr szerepén). L. az orkesztrátor kiegészítését. |
| F177.2 hibas_hivatkozas, MEK-elírás nincs javítva | OK | `Karoli_KH_javitott.tsv:35163, 35165, 1930` | Az `Exo.6.20→Exo.26.59` és a `Deu.7.15→Gen.15.26` jelölt, `hibas_hivatkozas=…` jelöléssel. A `Deu.21.23→Gal.2.13` csak_mek, és nincs Gal 3:13-ra javítva; a HunKar-ban azon a versen csak a `Jos.10.27` áll. Grep `hibas_hivatkozas=`: 161 sor, ebből csak_mek 117, kiesik 22, egyező 22. A „142 különböző vers” NEM ELLENŐRIZHETŐ. |
| F177.2 TSK-támogatás az egyoldalú sorokon | **ELTÉRÉS** | `eszkozok/karoli_kh_mek.py:421-423` | A brief előírja: „TSK-támogatás … az eltérő és az egyoldalú sorokra”. A `kiesik` sor (csak a HunKar-ban van) egyoldalú, mégsem kap `tsk=` jelölést. Grep `\tkiesik\t[^\t]*\t[^\t]*tsk=`: **0 / 11 027**. Az eltero_lista sorok mind a 44-en (22 `tsk=igen`), a csak_mek sorok mind a 2 797-en (2 018 `tsk=igen`) kapnak jelölést. |
| F177.2 versellenőrzés alapja (DT-F177c) | **ELTÉRÉS** | `dontesek/uj/karoli-kh-mek.md:3`; `naplok/F177_jelentes.md:16,51`; README 4. | (1) A végrehajtó eltért a brieftől (a `Karoli_1908.tsv` helyett unió), 🟡 döntéssel, megállás nélkül. Ez nem az egyeztetett eltérés, hanem a brief ⛔4 határesete. (2) Az indoklás („a `Karoli_1908.tsv` KJV-számozású”) a lekérdezés szerint téves. `lekerdez.py karoli "4Móz 29:39"`: két vers egyben (a KJV-ben 29:39 és 29:40). `"Róm 3:30"`: 3:30 és 3:31 egyben. `"1Kor 3:22"`: 3:22 és 3:23 egyben. `"Ján 1:51"`: két vers egyben; `"Ján 1:52"`: „Nincs Károli-szöveg”. A KJV ezeket külön versként adja, tehát ez versösszevonás, nem KJV-számozás. Maga az unió tartalmilag indokolható, a 14+2 versszám a versszerkezettel egyezik (Num 29 40, Jhn 1 52, Isa 4 5, Zec 9 16). |
| Jób 24 / Zsolt 102 / Zak 11 sorrendi versszám | OK | `Karoli_KH_javitott.tsv:7460-7471, 9923-9938, 19796-19819` | A versszerkezetben 25, 29 és 17 vers áll. A `lekerdez.py karoli` szerint a `Jób 24:25`, a `Zsolt 102:29` és a `Zak 11:17` létezik, a `Jób 24:26`, a `Zsolt 102:30` és a `Zak 11:18` nem. Tartalmi szúrópróba: Jób 24:2 („A határokat odább tolják”)→5Móz 19:14 megerősített; Zak 11:12 („harmincz ezüst”)→Mt 26:15 megerősített. A Jób 24 és a Zsolt 102 minden HunKar-sora megerősített. |
| F177.3 háromszintű tábla, minden HunKar-sor egyszer | OK (darabszám és kód alapján) | `Karoli_KH_javitott.tsv` | Grep: megerositett/HunKar+MEK 21 314, kiesik/HunKar 11 027, eltero_lista 44, egyezik-hibás 22. Összesen **32 407**, ami egyenlő a `Karoli_kereszthivatkozasok.tsv` 32 408 sorával, a fejlécsor nélkül. Csak_mek 2 797, összes sor 35 204. A kulcsonkénti multihalmaz-egyezést az ellenőr csak a kódból (az `osszevet` HunKar-soronként egy kimenő sort ad) és a `teszt_karoli_kh_mek.py:178` tesztből látta; a tesztet nem futtatta. |
| F177.3 szintdefiníció | OK, megjegyzéssel | `adat/SEMA.md` 2.54 | A besorolás sorszintű: eltérő listájú versen az egyező HunKar-sor is megerősített. A brief szövege ebben kétértelmű, a SEMA „sorszinten” rögzíti. Korlát: a MEK a tartományt két végponttal adja, ezért a végpontpár egyik fele csak_mek lehet (pl. a `Jhn.1.46` versen a Jer.33.14 megerősített, a Jer.33.15 jelölt). Ez dokumentált (N-F177b, README). |
| F177.3 szűrő, fogyasztók (`ir`-en kívül) | OK | `eszkozok/karoli_kh_szuro.py`, `lekerdez.py:572-586`, `sqlite_epit.py:740-742`, `olvaso_pilot/adat.py:195-198`, `olvaso_mockup/nav_kinyer.py:45` | A `git diff` szerint mind a négy fogyasztó a `gyanus_forrasok()`-ról az `elfogad(forras, cel)`-ra váltott. Indokolt: a régi API megmaradt, így a brief követelménye („a megerősített jut át”) nélkülük nem érvényesülne. A jelentés 1. pontja közli. |
| Kizárt: `lexikon_general.py`, lapok | OK | `eszkozok/lexikon_general.py:4131` | `git diff --stat`: sem a `lexikon/`, sem a `lexikon_general.py`, sem az `olvasoi_kapu.py` nem változott. A `kh_index` továbbra is a `karoli_kh_epseg.gyanus_forrasok()`-t hívja; ez az N-F177a. |
| F177.4 karantén archív | OK | `Karoli_kereszthivatkozasok_gyanus.tsv` | `git diff --word-diff=porcelain`: 5 078 `ts=` csere és 1 ARCHÍV fejlécsor, más nem változott. A generátor docstringje megkapta a megjegyzést. |
| TSV, `csv` modul | OK | — | Grep `import csv\|csv\.` a 8 érintett .py fájlban: 0 találat. Olvasás `split('\t')`-tel, írás `'\t'.join`-nal (`karoli_kh_mek.py:54-74`). |
| Licenc, nyílt mag | OK | `adat/licencek.tsv` (+2 sor), `nyilt_mag/forrasok_es_licencek.tsv:+2` | A nyílt magba csak a két „kizárva / tisztázatlan” licencsor és az újraszámolt hash került, MEK-adat nem. Megjegyzés: a `sqlite_epit`/`lekerdez` kiválasztása mostantól MEK-eredetű (melyik HunKar-sor megerősített). Ezt a brief F177.3 írja elő, és a DT-F177b (b) változata fedi; a döntés a felhasználóé. |
| Helyőrzők | OK | `dontesek/uj/karoli-kh-mek.md`, `nyitott/uj/karoli-kh-mek.md` | Az ágnév szerinti fájlnév helyes, a jelölések DT-F177a–c és N-F177a–b, új végleges DT/N szám nincs. A `futtat.py` E31/E32/E33-ja 0 találat. |
| A1 memória vs. lekérdezés | OK | `naplok/F177_jelentes.md:55` | A „valószínűleg 4Móz 26:59” feltételezésként van jelölve, és nem került adatba. |
| A2 nyitott/lezárt | OK | `NYITOTT_FELADATOK.md:62-63` | Az N-F156a lezárt. Az N-F156c érdemi része (`kh_index`) nincs kész, de kifejezetten az N-F177a-ba került. A számok (66 = 44 + 22) egyeznek a grep-pel. |
| A3–A6 | nem alkalmazható | — | Nincs tanulmány és nincs tanító. E12–E15: 0 találat. A tanulmány-ellenőrzés (F37 T4) nem indul. |
| A jelentés versszintű számai (11 396, 4 773, 1 905, 1 438, 32, 13 171; 317 / 7 654 / 3 373) | NEM ELLENŐRIZHETŐ | `naplok/F177_jelentes.md:20-43` | A megengedett parancsokkal csak sorszintű számlálás lehetséges, és az lefutott. A versszintű halmazműveletet az ellenőr nem tudta elvégezni. |
| `ellenoriz.py` SÉRTÉS (HAMART-001) és `teszt_sqlite_epit` 3 FAIL + 1 ERROR már a base-en | NEM ELLENŐRIZHETŐ | — | Egyik sem futtatható az ellenőr szerepében. Közvetett jel: a diff nem érinti a `lexikon/` könyvtárat és a `res_forras.tsv`-t. A `sqlite_epit.py` viszont változott, ezért a teszteredmény azonossága nem vezethető le. L. az orkesztrátor kiegészítését. |
| CI (`futtat.py`) | OK | — | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 55fa1573..e709614e) --diff-alap 55fa1573 --diff-fej e709614e`. HIBA 0; E8, E27-hiba, E32, E35: 0. JELENTÉS: E25 3, E27 48, E30 1 (`jelolt`, 59a18d7d), E34 41. Egyezik a jelentés 9. pontjával. |
| Lista 1: kiszűrt sorok | OK | — | Lapra/indexbe nem jut: kiesik 11 027, HunKar-jelölt 66 (eltero 44, egyező-hibás 22). Csak_mek jelölt 2 797 (TSK-val 2 018, nélküle 779; hibás 117). Megerősített 21 314. |
| Lista 2: kulcstartomány | OK | — | 66 STEP-könyv (alias) és 1 189 fejezet, a versösszeg 31 170 (README, tesztkonstans). |
| Lista 3: nulla-diff hatóköre | OK | — | Nem változott a `Karoli_kereszthivatkozasok.tsv`, a `lexikon/`, a `lexikon_general.py` és az `olvasoi_kapu.py`. A gyanús táblában csak a `ts=` és 1 fejléc változott, az adatmezők nem. |
| Lista 4: táblák Δ (fejléc nélkül) | OK | — | `git diff --numstat`: `adat/datasetek.tsv` +2; `adat/licencek.tsv` +2; `Karoli_KH_MEK.tsv` új, +29 987; `Karoli_KH_MEK_konyvaliasok.tsv` új, +68; `Karoli_KH_MEK_versszerkezet.tsv` új, +1 189; `Karoli_KH_javitott.tsv` új, +35 204; `Karoli_kereszthivatkozasok_gyanus.tsv` 0 (+1 megjegyzéssor). Bontás: jelentés 2. pont és README 6. pont (szintek), aliasok 67 + 1, versszerkezet fejezetenként, MEK 29 984 értelmezhető + 3 nem. |
| Lista 5: ⛔ pontok | ⛔1, ⛔2, ⛔3 OK; ⛔4: l. a DT-F177c sort | — | ⛔3: a 77,1% az ellenőr eszközeivel nem mérhető (versszintű szám). ⛔4: kézi KH-javítás nincs, a jelölt sorok eldöntetlenek. |

## Az ELTÉRÉS-ek súlyosság szerint

1. **F177.2:** a TSK-támogatás hiányzik mind a 11 027 `kiesik` (egyoldalú) sorról. Pont ezekből a sorokból lehetne kiszűrni a valódi, de a MEK-ből hiányzó HunKar-KH-t (az 1 905 nem gyanús vers).
2. **DT-F177c:** a végrehajtó a brieftől eltérő versellenőrzési alapot (unió) megállás nélkül alkalmazta, és az indoklás („a `Karoli_1908` KJV-számozású”) téves: a valódi ok a versösszevonás (4Móz 29:39, Róm 3:30, 1Kor 3:22, Ján 1:51).

## Megjegyzések (nem ELTÉRÉS)

- A 3 „értelmezhetetlen” MEK-sor (`1 Sám. 12,.`, `2 Kir. 12,.`, `2 Kir. 21,.`) mindhárom esetben a HunKar-tartomány második végpontjának tűnik (16:11–12, 23:11–12, 25:18–21), ezért 3 HunKar-sor eltero_lista jelölt lett. A találgatás tilalma szerint ez helyes, de a „versszám hiányzik” leírás ezt az összefüggést nem említi.
- A `teszt_karoli_kh_mek.py:101` fixture az „1. 2.” esetet összevont versként modellezi, a valós adat viszont nem ilyen.
- Az N-F177b „4Móz 28:68” és a jelentés „4Móz 28:1–68” alakja eltér.
- A javított táblában a végrehajtó csak a végpont-összeférést teszteli, a tartomány-szomszédságot nem.

## Az orkesztrátor kiegészítése (2026-11-09; nem az ellenőr megállapítása)

Két NEM ELLENŐRIZHETŐ pontot az orkesztrátor saját méréssel pótolt:

- **SHA-256:** `https://mek.oszk.hu/00100/00161/00161.rtf`, újra letöltve a repón kívülre (2026-11-09): `92130f2ae669402c38d2a0e13027fef86acd2fbd66d9a78b9b6d7a9800a7473a`. Egyezik a `Karoli_KH_MEK_README.md:16` értékével.
- **Az `ellenoriz.py` a base-en** (`55fa1573`, külön worktree, a repón kívül): `RENDBEN: 26 | SÉRTÉS: 1 | KÉZI: 2 | JELENTÉS: 14`, a SÉRTÉS a „11. Rés-forrás egyezés” szabályé. Ugyanaz, mint a fejen, tehát nem az F177 okozta.
- A `teszt_sqlite_epit.py` alapállapotát az orkesztrátor nem mérte; nyitva marad a javítókörre.
