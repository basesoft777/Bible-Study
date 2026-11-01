ELTÉRÉS: 6 tétel

# ELLENOR_F120: független ellenőrzés

Brief: `F120_BSB_SQLITE_KEZI_MT_BRIEF.md` (DT-F120a, átmeneti út, 1. lépés: (c) kihagyó őrrel) · tartomány: `9cf0e43a..2b80c0b3` (F120.1–F120.4) · ellenőr: claude-opus-5-5 (`fuggetlen-ellenor`)

*Mentési megjegyzés (végrehajtó, F120.5): az ellenőr szerepköre fájlt nem írhat, ezért a jelentését a végrehajtó mentette el változtatás nélkül. A javítókör (F120.6) eredménye a fájl végén, külön szakaszban áll.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | tényleges: claude-opus-5-5, kért: opus. A diffben nincs `modell` mező (`git diff --numstat 9cf0e43a..HEAD -- adat konkordancia`: üres). |
| E4 / DT3 / lista 4: sorszám-Δ | OK | – | A `git diff --numstat 9cf0e43a..HEAD -- adat konkordancia` kimenete üres. Az `adat/` és a `konkordancia/` minden `.tsv`-jének Δ-ja 0, bájtra változatlan; nincs új vagy törölt tábla, bontási napló nem kell. |
| lista 1: törölt sorok | OK | – | `git diff --numstat 9cf0e43a..HEAD`: törlés csak a kódban és a doksiban van. `sqlite_epit.py` −28 (a `kezi_mt_or`/`VersmegfKeziMt` és a régi Strong-ág), `teszt_sqlite_epit.py` −53 (`kezi_mt_or_kihagy`, `KeziMtOr`, két kihagyás), brief −2, `NYITOTT` −1 (az N-F117a sora bővített változatra cserélve). Adatsor nem törlődött. |
| lista 2: kulcslefedettség | OK | `konkordancia/Karoli_versmegfeleltetes.tsv` | A Grep `^[^\t#]*\t[^\t]*\t[^\t]+\tKEZI\t` 200 találatot ad, ez egyezik az `F120_meres.md:19` értékével. A Hós 2-ben az MT 2:1–3 nincs `mt_kk`-ban (Grep `^Hós …\t(2:[1-3]\|…)\t`: csak a 2:19–22 sorok jönnek) → a BSB 2:1–3 azonossággal képez. |
| lista 3: nulla-diff hatóköre | OK | – | A nulla-diff az `adat/`-ra és a `konkordancia/`-ra vonatkozik. Nem vonatkozik a generált `pardes.db`-re: a `bsb` tábla a manifestben 277 817 sor, a napló szerinti próbában 275 042; a `vers_szamozas` és a `normalizalas_jelentes` is változik. A `eszkozok/olvaso_szerver/manifest_pardes_db.tsv:8,43,75` az élő újraépítéskor újrakészítendő (`frissesseg.py --manifest-keszit`). |
| lista 5 / ⛔ 3.2 | OK | `DONTESEK.md` (a DT-F120a sora) | Az F120.2 a döntési tétellel megállt. A F120.3 a felhasználó szó szerinti válaszát idézi („Igen, átmeneti”), helyőrzővel (`DT-F120a`, `N-F120a`). |
| ⛔ 3.5 | OK | – | A `BSB_Strongs.tsv` nem változott (l. E4). A 3.3 és a 3.5 nem e kör tárgya. |
| D: DT-F120a | OK | `eszkozok/sqlite_epit.py:184-208, 819-829` | A kód a döntést követi: a nem igazolt és az ütköző vers kimarad, jelentéssorral, más Károli-versre nem kerül. |
| D: fejezet_eltolasok-szignatúra | OK | – | Nem alkalmazható, a `bsb_import.py` nincs a diffben. |
| 3.4 küszöb | OK | `sqlite_epit.py:66,85` · `fj2/bsb_import.py:207-208` | A `len(t&b)/len(t)` mellett `<= 0.5` esetén kimarad; ez pontosan a `bsb_import.versillesztes` `hanyad > 0.5` feltételének tükre (azonos irány: \|T∩B\|/\|T\|). |
| 3.4 Strong-szűrés BSB = TAHOT | OK | `sqlite_epit.py:572-584` ↔ `809-817` | Mindkét oldal azonos: `strong_normalizal` (ValueError esetén elem nélkül), a `grammatikai_strongok.tsv` és a H9001–H9049 kizárva, `+` lánc elemenként. A TAHOT-oldal csak `nyelv=='H'` (az ÓSZ-ben helyes). A `self.grammatikai` a `_eredeti_tokenek`-ben áll be, ez a `_bsb_szamozas` előtt fut (`:489` < `:493`). |
| 3.4 ütközés | OK | `sqlite_epit.py:200-203` | A küszöbön átjutott versek közül, ha több esik egy Károli-versre, mind kimarad. „Azonosság + táblapár” sor így nem kerülhet be (E2, második fele, kódszinten). |
| 3.4 minta mód | OK | `sqlite_epit.py:585, 792-818` | Az `ot_vers_strongok` a `_benne` előtt épül, a `versek` minden BSB-sorból, tehát a `kihagy` minta módban is a teljes adatból számol, és azonos a teljes módéval. A `_benne` csak az írást szűri. |
| 3.4 „Strong-szám nem normalizálható” | OK | `sqlite_epit.py:837-838` | Kódszinten szűkült: a kihagyott versek soraira már nem jelent. A mai adaton ennek nincs hatása. Grep a `BSB_Strongs.tsv`-n, 3. mező → 0 (két mintával). A jelentés száma tehát régen és most is 0. |
| 3.4 `vers_szamozas` mellékhatás | ELTÉRÉS | `sqlite_epit.py:827-833, 858-861` | A `szamozas_vers` már csak a megmaradt BSB-versekből töltődik. Ahol minden jelölt kimaradt (pl. Hós 2:1–3), a `vers_szamozas.szamozas` korábbi értéke `nincs_adat`-ra vált. Ezt sem az `F120_meres.md`, sem a DT-F120a, sem az N-F117a nem említi. Darabszám: NEM ELLENŐRIZHETŐ (építés kellene). |
| 3.4 jelentéssor kulcsa | ELTÉRÉS (enyhe) | `sqlite_epit.py:820-821` | A kihagyott vers a `normalizalas_jelentes` nyers mezőjébe BSB-kulcsként, de magyar könyvnévvel kerül (`'Hós 2:1'`). Ugyanebbe az oszlopba a „nincs ilyen Károli-vers” sor Károli-kulcsot ír, így a kettő összetéveszthető. A STEP-alak (`Hos.2.1`) egyértelmű volna. |
| 3.4 / E3 kivezetés | OK | – | A `Grep kezi_mt_or\|VersmegfKeziMt` a `*.py` fájlokban egyetlen találatot ad, a `teszt_sqlite_epit.py:273`-at, és ez a hiány-teszt maga. A `kezi_mt_or_kihagy` 0 találat. |
| 3.4 `KeziMtOr` → fixtúra | ELTÉRÉS | `teszt_sqlite_epit.py:227-274` | A brief fixtúrát kér arra, hogy a `KEZI` + mt sor a helyes Károli-versre képez. A `BsbOr` viszont csak a `bsb_bizonytalan`-t teszteli kézi halmazokkal. Az `mt_kk` út (pl. MT Jób 17:2 → Károli 17:1) a `_bsb_szamozas`-on át nincs tesztelve, és név szerinti eset az `Integracio`-ban sincs. |
| teszt: Hós 2 fixtúra | ELTÉRÉS (enyhe) | `teszt_sqlite_epit.py:246-250` | A fixtúra azt modellezi, hogy a BSB 2:4 igazolja a Károli Hós 2:1-et. A valós adatban nem így van: a Károli Hós 2:1 tartalma (H7378, H517, H802, …) a BSB **2:2**-é. A BSB 2:4 (H7355, H1121, H2183) nem egyezik, és a fixtúra BSB 2:4-halmaza (H559, H251, H5971) valójában a BSB 2:1-é. A teszt logikája érvényes, a megjegyzés és a „minta” félrevezető. |
| negatív próba | OK (kódszinten) | `teszt_sqlite_epit.py:351-357` | Ha az őr hívását visszaveszik, a `kihagy > 0` állítás piros lesz. Az első állítás is piros: a minta tartalmazza a Jóel 2:32-t (`elofordulasok.tsv`: ISTENTISZT-001), a BSB-ben `Jol.2.32` és `Jol.3.5` is megvan, azonossággal és `mt_tabla`-val ugyanarra a versre, tehát 2 különböző `step_nyers` keletkezne. Futtatással NEM ELLENŐRIZHETŐ (a szerep tiltja). |
| tesztfutás (3.4, E3 „zöld”) | NEM ELLENŐRIZHETŐ | – | A `python -m unittest` nincs a megengedett parancsok között. A F120.3 commit-üzenete 1 FAIL-t ír (`Negativ.test_baseline_a_masolaton_zold`). Ez nem az a FAIL, amelyet a brief várt (`test_mai_adat_zold`), és F120-naplóban nem szerepel. |
| E1 | – | – | A 3.3-hoz tartozik, nem e kör tárgya. |
| E2 | NEM ELLENŐRIZHETŐ (kódszinten OK) | `naplok/F120_meres.md:131-139` | A 0 ütközés a próba-db-n mért; a db nincs a repóban. Szúrópróba Greppel: a BSB `Jol.2.28` Strongjai egyeznek a TAHOT `Jóel 2:28`-cal; a `Jol.3.1` a táblapáron át a 2:28-ra esne, és nem egyezik → kimarad. Ez egyezik a napló 7. pontjával. |
| E3 | OK / NEM ELLENŐRIZHETŐ | – | A grep-rész OK, a „zöld” futás nem ellenőrizhető. |
| E5 | – | – | Az importhoz tartozik, nem e kör tárgya. Megjegyzés: az őr a `pardes.db`-ből egy Zsoltár-verset ejt ki (Zsolt 145:13, 0,50). |
| E6 | NEM ELLENŐRIZHETŐ | `naplok/F120_meres.md:127-141` | A napló szerint a próba Windowson, a repón kívül futott, kilépési kód 0, 90 tábla. Az „építési napló” csak összegzés; a SQL-szkript a scratchpadben van, a lekérdezések viszont a naplóban állnak. |
| E7 / proveniencia | ELTÉRÉS | `NYITOTT_FELADATOK.md` (N-F117a, „RÉSZBEN”) · `DONTESEK.md` (DT-F120a) | Az N-F117a kiegészítése („mért: 248 vers, 0 ütközés”) saját proveniencia-sor nélkül áll. A DT-F120a proveniencia-sora csak a `forras=naplok/F120_meres.py`-t nevezi meg, a 248/0 viszont a `F120_or_meres.py`-ból és a próbaépítésből jön. |
| meres: 0. pont | OK | `F120_meres.md:19` | 200 sor, Grep-pel reprodukálva. |
| meres: 1. pont (1Sám 21 sor) | OK | `F120_meres.md:35` | KK-MT-max 1 (csak az `1Sám 20:43 → 21:1` sor), TAHOT-max 15. |
| meres: 3–5. és 6. számai | NEM ELLENŐRIZHETŐ | `F120_meres.md:60-119` | A futtatás nem megengedett. Kódolvasás: az `or_meres` szabálya azonos a `bsb_bizonytalan`-éval. A 6. pont fejezetlistája összeadva 248, ez egyezik. Csv-modul és írás nincs. |
| meres: 4. pont következtetése | OK (szúrópróba) | `F120_meres.md:81-83` | A Hós 2:1 tartalma a BSB 2:2-é, a Jóel 2:28-é a BSB 2:28-é. |
| meres: 6. pont következtetése | ELTÉRÉS | `F120_meres.md:119` ↔ `:138` | „a helyes sor mindenütt megmarad” a Hós 2:1–3-ra nem igaz: ott egyik jelölt sem helyes. Az azonossággal érkező BSB 2:1–3 és a táblapárral érkező BSB 2:4–6 egyaránt kimarad, a helyes BSB 2:2–4 pedig azonossággal rossz versre esik, és szintén kimarad. A Károli Hós 2:1–3 így BSB-adat nélkül marad. |
| A1 | OK | `F120_meres.md:23, 95` | A kódolvasás `scope=manual`. |
| A2 | ELTÉRÉS (enyhe) | `NYITOTT_FELADATOK.md` (N-F120a (2)) | A nyitott tétel valóban nyitott (a 4Móz 13:1, Jób 39:1 a táblában nincs, a `lekerdez.py karoli` visszaadja; proveniencia: `scope=range:4Móz 13:1 \| forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv \| n=0 \| ts=2026-11-01T12:01Z`; `scope=range:Jób 39:1 \| … \| n=1 \| ts=2026-11-01T12:01Z`). A 9 versből 5 (Jób 39:1–3, Préd 9:1–2) azonban már a meglévő **N-F117d**, és az N-F120a erre nem hivatkozik. Az N-F117a „RÉSZBEN” állapota helytálló. |
| A3–A5 | – | – | Nem alkalmazható. |
| A6 (E12–E15) | OK | – | A `futtat.py` szerint mindegyik 0 találat. |
| CI | OK | – | `python eszkozok/ellenorzes/futtat.py --valtozott … --diff-alap 9cf0e43a --diff-fej HEAD`: HIBA nincs. Az E25 (4) és az E27 (40) a diffen kívüli fájlokra jelez. Az E30 FIGYELMEZTETÉS („fele” → „felé”) hamis pozitív. |
| Tanulmány-ellenőrzés | – | – | A diffben nincs tanulmányfájl. |

**ELTÉRÉS-ek súlyossági sorrendben:**
1. `F120_meres.md:119`: a „helyes sor mindenütt megmarad” állítás a Hós 2:1–3-ra hamis; a három vers BSB-adat nélkül marad, és ez a DT-F120a és az N-F117a összegzéséből sem derül ki.
2. `vers_szamozas` mellékhatás: a kihagyott verseknél a `szamozas` `nincs_adat`-ra vált; nincs dokumentálva, a darabszám nincs mérve.
3. Brief 3.4: a `KEZI` + mt leképezésre nincs fixtúrás `_bsb_szamozas`-teszt.
4. E7: az N-F117a „RÉSZBEN” mérési számai proveniencia-sor nélkül állnak, a DT-F120a forrásmezője hiányos.
5. A2: az N-F120a (2) részben átfed az N-F117d-vel, hivatkozás nélkül.
6. Enyhe: a Hós 2 tesztfixtúra megjegyzése ellentmond a valós adatnak; a jelentéssor BSB-kulcsa a Károli-kulcsokkal összetéveszthető.

*Nyitva maradt (szerepkorlát): a célzott tesztfutás és a mérőszkriptek újrafuttatása; ezért NEM ELLENŐRIZHETŐ az E2, az E6, a tesztek „zöld” állapota és a mérés 3–6. pontjának számai.*

---

## Javítókör (F120.6, végrehajtó)

| # | ELTÉRÉS | javítás |
|---|---|---|
| 1 | Hós 2:1–3 állítás | `F120_meres.md` 6.: az állítás pontosítva (Hós 2-ben egyik jelölt sem helyes, mind kimarad); a DT-F120a és az N-F117a megnevezi a BSB-adat nélkül maradó verseket. |
| 2 | `vers_szamozas` | mérve (`F120_or_meres.py`): 237 Károli-vers marad BSB-adat nélkül, `vers_szamozas.szamozas` = `nincs_adat`; fejezetenként a napló 6. szakaszában; a próba-db `vers_szamozas` eloszlása a 7. szakaszban. |
| 3 | fixtúrás teszt | `BsbOr.test_bsb_szamozas_fixturan_kezi_mt_par_es_kihagyas`: a `_bsb_szamozas` fixtúrán (Károli Jób 17:1 = MT 17:2, `KEZI`): a táblapár a helyes versre képez, az azonossággal érkező BSB 17:1 kimarad, jelentéssor STEP-kulccsal, `vers_szamozas` ellenőrizve. Negatív próba (az őr kikapcsolva): PIROS. |
| 4 | E7 | proveniencia-sor az N-F117a kiegészítésénél és a DT-F120a-ban (`F120_or_meres.py` + próbaépítés). |
| 5 | A2 | az N-F120a (2) hivatkozik az N-F117d-re. |
| 6 | enyhe | a fixtúra Jób 17-es valós mintára cserélve (a Hós 2-es megjegyzés javítva); a jelentéssor nyers mezője STEP-alakú BSB-kulcs (`Job.17.1`). |

Tesztek a javítás után: l. a F120.6 commit-üzenetét és a `naplok/F120_meres.md` 8. szakaszát.
