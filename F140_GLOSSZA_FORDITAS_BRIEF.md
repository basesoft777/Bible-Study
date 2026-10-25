---
feladat: 140
cim: A héber szavak rövid magyar jelentése — a TBESH-glossza fordítása mind a 8 718 héber Strongra, a szó-lap kiemelt jelentés-sorának forrásaként (GLOSSZA_FORDITAS)
kod: GLOSSZA_FORDITAS
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ag: ccr-636782ad-lysuoh
ad: minden héber Strong-számhoz (8 718) rövid magyar jelentés egy új adattáblában (adat/glosszak_heber_hu.tsv, allapot=sonnet, modell = a ténylegesen futó modell; a pardes.db-be az sqlite_epit.py általános adat/*.tsv-betöltője hozza), a TBESH glosszájából fordítva, a lemma és a definíció eleje mint kontextus mellett; kapukkal ellenőrizve; a 300 leggyakoribb szóra kézi átnézési lista
kovetkezo: "Folytatás: M1 — 11 586/11 677 sor kész (81 köteg); következő: python eszkozok/glossza_forditas.py --koteg <fajl> --csak-bemenet, fordítás, --rogzit <valasz> --modell <tényleges modellnév>; l. naplok/GLOSSZA_FORDITAS_M1_naplo.md Folytatási pont és Tanácsok a folytatáshoz"
munka: adat
olvas: [konkordancia/TBESH.txt, konkordancia/TBESH_TBESG_README.md, konkordancia/Strong_szotar.tsv, konkordancia/TAHOT_kivonat.tsv, adat/terminologia.tsv, eszkozok/forditas_kapuk.py, eszkozok/emeles.py]
ir: [adat/glosszak_heber_hu.tsv, adat/SEMA.md, eszkozok/glossza_forditas.py, eszkozok/teszt_glossza_forditas.py, naplok/GLOSSZA_FORDITAS_elakad.tsv, naplok/GLOSSZA_FORDITAS_atnezes.tsv, naplok/GLOSSZA_FORDITAS_zaras.md]
fugg: []
nem_fugg: [38, 138]
---

# F140_GLOSSZA_FORDITAS_BRIEF.md — A héber szavak rövid magyar jelentése

*FELADATOK #140 · Modell: sonnet · v1 · 2026.10.25*

## 1. Cél

A szó-lap kiemelt jelentés-sora (a #139 fejléce) ma a lefordított BDB-szócikk elejéből gépileg kivágott szöveget mutatja (`bdb_szelet.alap_jelentes`, DT-F76f), ennek híján az angol Strong-szótár szavát (innen a „LORD” hiba, #138). A kivágás a 7a adag 85 szócikkéből 13-nál hibás (`scope=adat/forditasok.tsv, 7a adag 85 Strong + eszkozok/olvaso_szerver/bdb_szelet.py | forras=helyi-futtatas | ts=2026-10-25`), és csak a már lefordított BDB-szócikkekre ad bármit.

A DT-F140a döntése szerint a kiemelt jelentés forrása a **TBESH rövid glosszájának (7. oszlop) magyar fordítása** lesz. A TBESH a helyes glosszát adja ott is, ahol a `Strong_szotar.tsv` hibás (H0430: TBESH „God”, Strong_szotar „LORD”).

Előmérés a befogadáskor (`scope=konkordancia/TBESH.txt H-sorai, konkordancia/Strong_szotar.tsv H-sorai | forras=helyi-futtatas | ts=2026-10-25`):

- a TBESH 11 682 héber sora 8 723 alapszámra esik (a kulcs első öt karaktere; a homonimák betűjellel, pl. `H2763a` „to devote/destroy”, `H2763b` „to slash”); a `Strong_szotar.tsv` mind a 8 718 héber Strongjának van TBESH-sora;
- 7 331 alapszámnak egy sora van, 1 392-nek több (homonima, vagy a névhez kapcsolt alsor, pl. H0430G „God”, H0430H „(LORD)-Elohe”, H0430I „(Gibeath)-elohim”);
- a glossza összesen 62 920 karakter (alapszámonként az első sor), 88 119 karakter minden sorral; a definíció első 200 karaktere mint kontextus kb. 907 000 karakter bemenet.

## 2. Hatókör

**Benne van:**

- az alapszám → fordítandó TBESH-sor(ok) szabálya (M0): melyik sor a fő glossza; a homonimák (`a`/`b`) mind kapnak fordítást, saját `entry_id`-val; a névhez kapcsolt alsorok (`= a Part of`, `= a Name of` kapcsolattal) nem fő glosszák [javaslat: kimaradnak, vagy külön jelölve];
- saját adattábla: `adat/glosszak_heber_hu.tsv` (kulcs: `strong` + `entry_id`, ahol az `entry_id` a TBESH kiterjesztett azonosítója; mezők [javaslat]: `strong`, `entry_id`, `glossza_en`, `forras_hash`, `glossza_hu`, `allapot`, `modell`, `datum`, `megjegyzes`), SEMA-bejegyzéssel. A `forditasok.tsv` helyett azért külön tábla, mert azt a #38 (BDB-fordítás) folyamatosan írja: a közös fájl kizárná a párhuzamos futást (KIZAR #27, #38), és 11 feladatot tenne a #140-től függővé (DT-F140a (e)). A pardes.db-be az `sqlite_epit.py` `_adat_tablak` általános betöltője minden `adat/*.tsv`-t betölt, tehát az építőhöz nem kell nyúlni; ha a licencjelölés (a TBESH CC BY 4.0, a fordítás származtatott mű) az `ADAT_LICENC` bejegyzését kívánja, az M0 ⛔ pontja jelzi, és az `sqlite_epit.py`-módosítás külön kerül a felhasználó elé;
- a fordító szkript (`eszkozok/glossza_forditas.py`): kötegelt, újraindítható, a `forras_hash` a TBESH-glossza SHA-1-e; a prompt bemenete szavanként a héber lemma, az átírás, a szófaj, a glossza és a definíció első ~200 karaktere, a köteg elején a projekt terminológiája (`adat/terminologia.tsv`); a kimenet egy rövid magyar jelentés (legfeljebb ~5 szó, több értelem pontosvesszővel), szófaj nélkül, főnévnél alanyesetben, igénél főnévi igenévvel;
- tulajdonnév: a magyar (Károli-hagyományú) névalak, pl. H7346 „Roboám”; istennév: a Károli-szóhasználat szerint (H3068 „az ÚR”, H0430 „Isten”);
- kapuk (gépi, minden soron; saját kapukészlet, az `eszkozok/forditas_kapuk.py` csak minta, nem közös kód: a #38 futás közben módosíthatja, ezért `nem_fugg: [38]`): nem üres; nincs benne héber vagy görög betű; nincs angol szó (szótár-alapú ellenőrzés, kivétel-listával); hossz-korlát; a `forras_hash` egyezik;
- **DT-F140b szerint igazítva (2026-10-25, a felhasználó döntése):** mind a 11 677 TBESH-sor fordul, `kapcsolat` és `fo` oszloppal (K1 (B)); a `fo` a `TAHOT_kivonat.tsv` „Rövid jelentés” oszlopának Strongonkénti többségi értékével egyező glosszájú sor (K2), az istenneves Strongoknál a K5-lista; a TAHOT-oszlop csak a kiválasztásban számít, szöveg nem kerül át; az M1-et a session végzi kötegenként (K7 (a)), a `modell` mezőbe a ténylegesen futó modell neve kerül; az `ADAT_LICENC`-bejegyzés (K8) külön kisfeladat, a tábla main-re kerülése előtt.
- a 300 leggyakoribb héber Strong (a `TAHOT_kivonat.tsv` előfordulásszáma szerint) kézi átnézési listája a `naplok/GLOSSZA_FORDITAS_atnezes.tsv`-be; a hibás sort a felhasználó `kezi` sorral írja felül.

**Nincs benne:**

- a szó-lap megjelenítése és a forrás-sorrend kódja (kézi > glossza-fordítás > BDB-kivágás): az a #139;
- a görög szavak (TBESG): külön feladat, ha ez beválik;
- a `Strong_szotar.tsv` és a `TAHOT_kivonat.tsv` „LORD”-javítása: a #138 (szűkített hatókörrel, DT-F140a (c)). A #140 e két fájlból csak a Strong-kulcsot, a szófajt és az előfordulásszámot olvassa, a #138 által javított „Jelentés”/„Rövid jelentés” oszlopot nem; ezért `nem_fugg: [138]`.

## 3. Lépések

**M0 — mérés és minta.** ⛔ A sor-választási szabály (fő glossza, homonima, alsor) mért darabszámokkal; a kulcsséma; a prompt; próba 30 szón (vegyesen: gyakori ige, főnév, melléknév, partikula, tulajdonnév, istennév, homonima: köztük H0430, H3068, H5945, H2763, H1581, H7346, H0853); a 30 eredmény a `naplok/GLOSSZA_FORDITAS_M0.md`-be. Megállás: a felhasználó jóváhagyja a mintát és a szabályokat.

**M1 — teljes futás.** Kötegenként; minden köteg után kapuk; a kapun elbukó sor újrafordul, a második bukás után `naplok/GLOSSZA_FORDITAS_elakad.tsv`-be kerül, nem az adattáblába. Folytatásnál a tábla írása előtt a meglévő sorok változatlanságának összevetése (minta: `eszkozok/igazolas_migracio.py`); `ellenoriz.py` 0 sértés.

**M2 — átnézési lista és zárás.** A 300 leggyakoribb szó listája; zárójelentés (darabszám, kapuhibák, elakadók, a modell tényleges neve) a `naplok/GLOSSZA_FORDITAS_zaras.md`-be. ⛔ a felhasználó átnézi a listát.

## 4. Elfogadási feltételek

- A 8 718 héber Strongból mindegyiknek van legalább egy sora az `adat/glosszak_heber_hu.tsv`-ben, vagy az elakadó-listában szerepel indoklással.
- Minden sor átment a kapukon; `ellenoriz.py` 0 sértés; az `adat/forditasok.tsv` érintetlen.
- A `modell` mezőben a ténylegesen futó modell neve áll (CLAUDE.md, modell-ellenőrzés).
- A szkript második futása a kész sorokat nem fordítja újra (a `forras_hash` szerint).

## 5. Döntésnapló

- **DT-F140a** (2026-10-25, a felhasználó, chat; a tétel a `DONTESEK.md`-ben): a kiemelt jelentés forrása és sorrendje; a modell; a #138 szűkítése; a #139 függése; a saját tábla (e).
- **DT-F140b** (2026-10-25, a felhasználó, chat; a tétel a `DONTESEK.md`-ben): K1 (B), K2 (a) módosított `fo`-szabállyal, K3 (a), K4 (a), K5 kibővített istennév-lista, K6, K7 (a), K8 külön kisfeladat, K9 (a), K10 50/6. Az M1 ezek szerint fut.
