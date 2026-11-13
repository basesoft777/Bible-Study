# ELLENOR_F194_2 — független ellenőrzés, a #194 2. fázisa (efefb910..2ae45dae)

*A `fuggetlen-ellenor` subagent (claude-opus-5-5) jelentése; a fájlt a menet keze mentette a subagent válaszából (a subagent nem írta ki), tartalmi változtatás nélkül. 2026-11-12.*

**ELTÉRÉS: 10 tétel**

Brief: `F194_ISTENTISZT_UJ_CIKK_BRIEF.md` · tartomány: `efefb910..2ae45dae` (F194.19–F194.30). Ellenőrzési szint: `teljes` (`python eszkozok/feladatok.py szint 194` → „teljes, 2 kör”). A saját változtatások: `5f6ac740..HEAD`; a main-behozás (5f6ac740) összevont diffje (`git show --cc`) csak generált nézetekben old fel ütközést.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | Tényleges: `claude-opus-5-5`, kért: `opus`. Mind a 12 commit `Co-Authored-By: Claude Opus 5.5`. |
| 0 modell-mezők | ELTÉRÉS | `naplok/F194_teljesseg_ISTENTISZT-001.md:4, :52` | Az F194.20 újrafuttatás felülírta a fejlécet („#123 MIGRACIO2 · ág `claude/relaxed-raman-0562d4` · modell: claude-sonnet-5-5”), a „2. kiadás listája (20 vers)” helyére „Az 1. kiadás listája (22 vers)” került. |
| G1 proveniencia | OK | `motivumok/ISTENTISZT-001.md:27–152` | Az értelmező rések alatt proveniencia-sor; az `elofordulasok.tsv` 20 sorában `scope=manual \| forras=F194 … U3 (claude-opus-5-5 …)`. |
| G2 TSV | OK | `naplok/F194_proza_1a.py`, `F194_kapcsolat_szoveg.py` | `split('\t')`, `'\t'.join`, írás előtti összevetés. |
| Brief: G3, „Ne nyúlj”, `ir`, fejléc | ELTÉRÉS | `F194_ISTENTISZT_UJ_CIKK_BRIEF.md` | A „Ne nyúlj” lista és a G3 szövege az 1. fázisé, az orkesztrátor 2. fázisbeli jóváhagyása nincs rögzítve; az `ir`-ből hiányzik `eszkozok/tablajegyzet.py`, `kiejtes_szoveg.py`, `olvasoi_kapu.py`, `bdb_rovidites.py`, `lexikon/HAMART-001_TUDOMANYOS.md`, `adat/lap_javitasok.tsv`, `adat/kiadasok.tsv`, `archivum/ISTENTISZT-001/` és 6 tesztfájl; a fejléc (`allapot: megallt`, `kovetkezo`, cím) az 1. fázisé. |
| Brief „Mérés (kötelező)” | ELTÉRÉS | `naplok/F194_meres.md` | A 2. fázis (F194.19–30) egy lépést sem vett fel. |
| D1 | OK | – | Egy javítókör (F194.30); ez a független ellenőrzés. |
| DT832 | OK | `dontesek/uj/istentiszt-uj-cikk-992f57.md` | `feladatok.py ellenoriz` → 0 hiba. |
| DT833, 9. szakasz ÓSZ-tábla | ELTÉRÉS | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:1541`; `eszkozok/lexikon_general.py:8907` | (1) A Targum-cella hat versre (1Kir 18:24–26, 2Kir 5:11, Jóel 2:32, Sof 3:9) „nincs Targum-forrás”-t ír, holott az adatban van Jonatan-alak, csak ellenőrizetlen (N181): „nincs ellenőrzött adat” járna. (2) Az LXX-cella az 1Kir 18:24-hez csak a βοάω-t írja „más szó”-ként, pedig a sor `βοάω · ἐπικαλέω`; a próza 13 ἐπικαλέω-versnek számolja. |
| (a) HAMART-001 | OK | `lexikon/HAMART-001_TUDOMANYOS.md` | `git diff --word-diff 1352ac3c..HEAD`: pontosan három csere (kétszer `(JHVH)`→`(Jahve)`, egyszer `שחת (s-ch-t)`→`שחת`); a `lap_javitasok.tsv:83` sora megvan. |
| (b) a generátor hatóköre | ELTÉRÉS | `eszkozok/olvasoi_kapu.py:885-900` | A `PONTOZATLAN_HEBER` kivétel minden lap minden „szó (kiejtés)” párjára hat, nem csak a rokon nyelvi táblára (a generátoroldali `kiejtes_szoveg._bejar` csak a „rokon nyelvek” szakaszra szűkít); példa: `ISTENTISZT-001_TUDOMANYOS.md:1169` „קרא (kárá)” (Thayer-szöveg). |
| 4.8 rokon nyelvek | ELTÉRÉS | `ISTENTISZT-001_TUDOMANYOS.md:1045-1051`; `lexikon_general.py:8581, 9811` | A 7 bdb-sorból 3 jelenik meg; a föníciai, nabateus és palmürai sor kimarad, mert a `ROKON_NYELVEK` listában nincs; a bevezető mondat a táblában nem szereplő nyelveket sorol. |
| (c) próza, mintavétel | OK | `adat/elofordulasok.tsv`, `motivumok/ISTENTISZT-001.md` | `lekerdez.py karoli` 11 versre: az idézetek egyeznek; `scan`-ellenőrzések (H0430, H5769, H0410, H1168, H7121, G1063, G3686), `lxx-hid` (Jóel 2:32, 1Móz 4:26), az ApCsel 22:16 apparátusa, a Thayer G1941, a Targum 5/7 mind egyezik. |
| (c) lektor javítókör | ELTÉRÉS | `ISTENTISZT-001_TUDOMANYOS.md:1419, 1492, 1493` (`adat/kapcsolatok.tsv`) | A lektor 5. tétele csak a próza oldalán javult: a kapcsolat-sor szerint a 2Kir 5:11 „parafrazált … nincs szó szerinti egyezés”, holott a TAHOT szerint H7121, H8034, H3068 áll; a blokk három idézete nem Károli-szöveg („az Úr, az ő Istene nevét”, „segítségül hívják mindnyájan”, „segítségül hívni az Úr nevét”). |
| 1. kiadás lektori naplója | ELTÉRÉS | `naplok/KIADAS_ISTENTISZT-001_lektor.md` | Az F194.30 felülírta az 1. kiadás 15 kérdését (archív másolat nélkül); a fájlra a `DONTESEK.md:520`, a `NYITOTT_FELADATOK.md:995` (N-F152c) és a `naplok/LEKTOR_FELULET_naplo.md:133` a régi tartalom szerint hivatkozik. |
| (d) bdb +7 sor | OK | `adat/visszhang_megfelelok.tsv:192–198` | `modell=claude-sonnet-5-5`, `ellenorzes=claude-opus-5-5 …`; a sorok egyeznek a BDB fejsorával. Az 1. kör 4 javítandó tétele csak a commit-üzenetben szerepel. |
| (e) kapuk | OK | – | olvasói kapu 0 BUKÁS (29 FIGY); `proza_1a` 20/20; `proza_allitas` ELTÉR 0; `feladatok.py ellenoriz` 0 hiba; `teszt_f194_szopar` 10 OK. |
| A6 / olvasói kapu, HAMART-mérce | ELTÉRÉS | `ISTENTISZT-001_TUDOMANYOS.md:199, 1580, 1586, 1596, 1598, 1612` | ONREF 14, HIANYJEL 1 (a HAMART-on 0 és 0): kétszer „A lap a kérdést nem dönti el”, egyszer „Ez a lap olvasata”, kétszer „Forrás: a lap munkaanyaga”; a 2.1 táblában „H8034: *(nincs hozzárendelés)*”. |
| Tesztek, változott kód | ELTÉRÉS | `eszkozok/teszt_olvasoi_kapu.py:399`; `eszkozok/teszt_szotari_gerinc.py` | `teszt_olvasoi_kapu.py`: 1 FAIL (`Arany.test_G7_dt_a_prozaban`; `ARANY='ISTENTISZT-001'`, a DT476-hiba az újraírt lapon nincs meg). `teszt_szotari_gerinc.py`: 12 FAIL + 1 ERROR (a main-en 10); az ISTENTISZT régi adataira épülő tesztek nincsenek átkötve. |
| Lassú olvasószerver-tesztek | NEM ELLENŐRIZHETŐ | – | `teszt_futtat.py --diff efefb910`: 14 fájl zöld; `teszt_visszhang_kapu` 2 FAIL (régi HAMART-szöveget vár, a main lapján sincs meg); `teszt_szintek` 2 FAIL (a közös natív adatbázison, a diff nem érinti). |
| 3. CI | NEM ELLENŐRIZHETŐ | – | A HEAD-re nincs futás; saját futás (`--diff-alap 1352ac3c`): E5/E16/E26 0, E28 0, E29 0, E35 HIBA 4 (ismert, a nyílt mag). |
| A1–A5 | OK | – | A Thayer-állítás igazolva; az értelmezés jelölt; az N-F194c lezárása megalapozott; 16 kapcsolat-sor (13/3); a Remez leíró, a Sod levezethető; a képviselők repóforrások. |
| (f) commitok, döntések | OK | – | Tételazonosító, magyar üzenet; új tétel csak helyőrzővel; a `DONTESEK.md` és a `NYITOTT_FELADATOK.md` nem változott. |
| Ell. 1–5 | OK | – | A törlések jelölve (`TÖRLÉS-SZÁNDÉKOS:`); a kulcstartomány; a HAMART nulla-diffje az F194.22-re (utána 3 sor); a sorszám-Δ magyarázott; a ⛔ pontokon nincs jogosulatlan írás. |

**Az eltérések súlyossági sorrendben:**
1. A 9. Hatástörténet ószövetségi táblázata: hat vers „nincs Targum-forrás” (valójában ellenőrizetlen); az 1Kir 18:24 LXX-cellájából hiányzik az ἐπικαλέω.
2. A kapcsolat-indoklás blokkja ellentmond a TAHOT-nak (2Kir 5:11), és három nem Károli-idézetet hoz.
3. Az 1. kiadás lektori kérdéslistája archiválás nélkül felülíródott.
4. A brief nincs a 2. fázishoz igazítva.
5. A kötelező mérés a 2. fázisból hiányzik.
6. A 4.8 rokon nyelvi táblából kimarad a föníciai, nabateus és palmürai sor; a bevezető mondat nem szereplő nyelveket sorol.
7. Az olvasói kapu figyelmeztetései a HAMART-mércéhez képest: ONREF 14, HIANYJEL 1.
8. A teljesség-mérés leírásában hamis a modell- és ágmező, és hibás a „22 vers” mondat.
9. Két teszt bukik a változott kódra.
10. A `PONTOZATLAN_HEBER` kapu-kivétel tágabb a döntésnél.
