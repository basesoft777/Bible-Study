# F239 átadó — U3b (a próza célzott igazítása a kész 9. Hatástörténethez) → U4 (ellenőrzés)

*2026-11-23 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/nervous-kare-9d2361` (PR #820). A lépések indokkal: `naplok/F239_naplo.md`, „U3b”; az érvekben változó pontok: `naplok/ERVNAPLO_TEREMT-001.md` D3.*

**A célzott ellenőrzés lezárult.** A próza (F239.17) az U1b előtt készült; az U3 átadójának „Nyitott, az U1b után” pontja szerinti összevetés kész, a próza a 9. blokknál és a vitatott pontok szakirodalmánál többet nem állít. A próza ezzel az U4-nek (állítás-ellenőrzés), utána a lektornak átadható; a kiadás továbbra is a 218c-re (N-F239a) és a #240-re (BDB) vár.

## Mi változott (F239.19, F239.20)

| hely | volt | lett | ok |
|---|---|---|---|
| Miért fontos, „A Septuaginta hídja” | 2Móz 15:5: βυθός | 15:5 πόντος („tenger”), 15:8 κύματα („hullámok”); a βυθός a mecólá fordítása; 1Móz 49:25 és Péld 8:27-28: átfogalmazás | U1b kétkezes LXX-sora, az 5. szakasz táblája |
| Remez — az Újszövetség | „a felhozás és a mélység a Zsolt 71:20-ban is” | a hét vers tényként, a merítés nyitott kérdésként, külön mondatban | D2.1; saját lekérdezés n=7 |
| V4 (Róm 10:7) | két zsoltár + három leszállás-vers | hét vers (4 leszállás, 3 felhozás; kettőben a héberben nincs tehóm), a két zsoltár mint a legközelebbi; az elöljáró-eltérés csak a 107:26-ra | D2.1; saját lelet: a 71:20 ἐκ … ἀνάγω szerkezete a Róm 10:7-ével nem ütközik |
| V3 (Tengeri ének) | „A kommentárirodalomban mindkét álláspont képviselt.” | kimarad | ellenőrizetlen alap; a szakirodalom-sor szerint lektorált forrás nem került elő |
| `adat/vitatott_forrasok.tsv` `pont` (3 sor) | az érvnapló kérdés-címe | a forrásprózabeli félkövér cím (SEMA 2.58) | az előnézet a B40-en megállt; csak a kulcs, külön commit |
| érvnapló A3; új D3 | βυθός | πόντος | ugyanaz, mint fent |

Változatlan, indokkal (napló 8–11. pont): a Kivonat (a zárómondat a 9. LXX-alapvonalával és az 5. szakasszal egyezik), a V1 (a Tsumura-sor két álláspontot mutat be), a V2, a Remez „Genezis négy helye” (nem a 9. lánca), az 1/a (fordítókról, recepcióról nem állít). Az atyai tanúkról a próza hallgat.

## Mérve (az előnézeten, repón kívül)

Az előnézet: `python eszkozok/general.py --cel lexikon2 --id TEREMT-001 --kimenet <repón kívül>`, az N-F239a ideiglenes kerülőútjával (a `adat/motivum_kapcsolatok.tsv` `DT-F239a` → `DT9991`; a `lapgen/megjelenites/md/kizart.py` arány-mondatának hibája kikapcsolva), futás után visszaállítva; előtte `python.exe`-lista, egyszerre egy futás. Eredmény: az 1/a 43/43 kerek; az olvasói kapu 8 BUKÁS, mind generált részben, a prózában 0; `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba.

## Talált olvasói hibák, nem a próza hatáskörében (az integrátornak jelentve)

1. **Az 5. LXX-fordítói döntések** a 2Móz 15:5 πόντος szavát G4195-tel, „Pontosz · Pontusz” (földrajzi név) címkével adja; itt „tenger”. Forrása a LXX_OS Strong-hozzárendelése; az `adat/lxx_dontesek.tsv`-ben TEREMT-001 sor nincs.
2. **ATIRAS** (olvasói kapu, 932. sor): az 5. szakasz a κῦμα lemmához a κύματα alak kiejtését („kümata”) írja, a 4. szakasz „küma”-t; a forrás a `visszhang_megfelelok.tsv` 2Móz 15:8 sorának `kiejtes` mezője.
3. **ANGOL + MUNKASZO** (1248. sor): a Bekken-könyv valódi angol címe („A Study of …”) az Irodalomban; a kapu nem ismeri fel a műcímet.
Az U3 öt korábbi bukása (Thayer-zárójel, „jelölt”, „teljesség-mérése”, „ellenőriztük”, „a lap elején áll”) változatlan, generátor-szöveg.

## Az U4 bemenete

Az U3 átadójának U4-listája változatlanul áll (`naplok/F239_atado_U3.md`, „Az U4 bemenete”), két kiegészítéssel: a V4 ténye és nyitott kérdése most a hét versre szól, külön mondatban; a V3-ból a kommentárirodalom-mondat kimaradt. A `proza_1a.py` és az `olvasoi_kapu.py` alapból a befagyasztott régi lapot méri: `--lexikon-konyvtar <előnézet>/lexikon`, illetve `proza_1a.lap_meres('TEREMT-001', gyoker=<előnézet>)`.

## Nyitott döntések

Új tartalmi vagy határkérdés nem merült fel. A kiadás feltételei változatlanok: N-F239a (218c) és a B19 BDB-hiba (#240).
