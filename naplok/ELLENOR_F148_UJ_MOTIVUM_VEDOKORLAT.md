# ELLENŐR — F148_UJ_MOTIVUM_VEDOKORLAT_BRIEF.md · `63c7b344..c052cd14`

*A `fuggetlen-ellenor` jelentése (modell: `claude-opus-5-5`, kért: `opus`). Az ellenőrnek nem volt fájlíró joga, ezért a jelentést a végrehajtó mentette el, változtatás nélkül; a végén a végrehajtó javításai (F148.8) külön szakaszban.*

```
ELTÉRÉS: 5 tétel
```

(A merge-base egyezik az `origin/main` csúcsával, `63c7b344`. Az ellenőrzés közben a HEAD az F148.7-re lépett, ez csak a naplót bővítette.)

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | `naplok/F148_UJ_MOTIVUM_VEDOKORLAT_naplo.md:7` | Az ellenőr `claude-opus-5-5`, a kért `opus`. A napló a tényleges modellt írja. Adattábla-`modell` mezőt a menet nem írt. |
| Elf. 1 (render bájtra azonos) | NEM ELLENŐRIZHETŐ | `eszkozok/lexikon_general.py:2496,2530` | A `general.py --kimenet` és a worktree-létrehozás kívül esik a megengedett parancsokon. Kódolvasásból: előtte `gerinc_aktiv` = {ISTENTISZT, ALVIL}, utána = minden, ami nincs a `kivetel` sorok között {ANTROP, HAMART, HODIT, KIRALY, MENNY, TEREMT-001, TEREMT-002}. A 9 motívum (`adat/motivumok.tsv` 3–11. sora) mindegyikén azonos az eredmény. A régi konstanst `eszkozok/` alatt más nem olvassa (Grep `SZOTARI_GERINC_MOTIVUMOK`). A lapok száma 8 TUDOMANYOS és 6 TORZSCIKK (Glob), tehát a napló 6-os korrekciója helyes. |
| Elf. 2 (új motívum kapcsolósor nélkül) | OK (kódolvasásból) | `eszkozok/teszt_szotari_gerinc.py:270-291` | `UJTESZT-001`: kapcsolósor nélkül megjelenik a „Jelentés (a szó)” oszlop, kivétellistán nem. A tesztet nem futtattam. |
| Elf. 3 / 18. szabály | OK (logika) | `eszkozok/ellenoriz.py` 18. szabály | Kivétellistán nem fut. A leképezés a generátor `kutatoi_szakasz`-a. Ha nincs mire leképezni, vagy nincs címkesor, SÉRTÉS. Pozitív és negatív teszt van. |
| Elf. 3 / 19. szabály | OK (logika) | `ellenoriz.py` 19. szabály | Gerincen SÉRTÉS, kivétellistán JELENTÉS darabszámmal. A DT438 (3)+(1) szerint a `tagolatlan` csak tagolatlan, egy-Strongos BDB-entry-n fogadható el. |
| Elf. 3 / 20. szabály, 1Kir 18:25–26 | OK | `ellenoriz.py` (JELENTES_HU_TILTOTT); `teszt_ellenoriz_vedokorlat.py:178-185` | Grep `^ISTENTISZT-001\t1Kir 18:2[56]\t.*Baál nevével` az `adat/elofordulasok.tsv`-ben: 2 találat. A „Baál nevével” sem a 6 kódbeli mintára, sem a `tiltott_fordulatok.tsv` 3 mintájára (3–5. sor) nem illik. |
| Elf. 3 / 21. (iv), N9999 | OK | `teszt_ellenoriz_vedokorlat.py:211-220` | A kitalált N9999-et és a kitalált DT-hivatkozást (négy kilences) jelzi, a létezőt nem. A repón: a lapok DT-hivatkozásai (272, 277, 280, 283, 373, 381, 382, 393, 414) mind `\| DTn \|` sorok a `DONTESEK.md`-ben (Grep). Az N-hivatkozás csak N59 (`**N59`, NYITOTT:74). Helyőrző, „a(z)” és „Kézzel írandó” a `lexikon/` alatt nincs (Grep: 0). |
| 21. (iv) N-létezés mintája | **ELTÉRÉS** (alacsony, látens) | `ellenoriz.py` `_letezo_tetelek`; `NYITOTT_FELADATOK.md:849` | A minta `\*\*N(\d+)\b`, a lezárt tétel viszont `* N62 —` alakú, csillagos kiemelés nélkül. Ha egy lap lezárt N-tételt idéz, hamis SÉRTÉS lesz belőle. A teszt fixture-je (`**N62`) nem a valódi formát használja. Ma nincs hatása. |
| DT440 súlyosság | OK | `ellenoriz.py` 21. szabály, `main_agon` | Az (i) pont ágon JELENTÉS, main-en SÉRTÉS. A (ii) és (iv) gerincen mindig SÉRTÉS. Kivétellistás lapon minden JELENTÉS. CI-ben `pull_request` esetén ág-állapotként fut. |
| Elf. 6 (kivétellista egy helyen) | OK | `adat/funkcio_kapcsolok.tsv:9-15`; `szerep_karoli.py:70-74`; `ellenoriz.py` `gerinc_kivetelek` | A generátor és az `ellenoriz.py` ugyanazt a `SZK.kapcsolo_kivetelek`-et hívja, ezt teszt is ellenőrzi (`assertIs(E.SZK, SZK)`). A brief „import, nem másolat” formáját a DT437 (4) adatsorra cserélte. |
| Elf. 4 (SÉRTÉS 0, E1 zöld) — ismert (A) | OK (a napló helyesen kimondja) | napló:131, 164, 175 | Grep `\tJ3\t` a `naplok/F148_levezetes_ALVIL-001.tsv`-ben: 59. Az `adat/elofordulasok.tsv` diffje üres. A 18. és 19. szabály így 59–59 SÉRTÉS-t ad. A napló szerint a merge feltétele a kitöltés. Pontosítás: az E1 lépés (`.github/workflows/ellenorzes.yml:95-105, 160`) a PR-en is fut, tehát a PR CI-je is piros lesz, nem csak a main. Az `ellenoriz.py`-t nem futtattam. |
| Elf. 5 / regresszió | OK | `naplok/F148_levezetes_ISTENTISZT-001.tsv` (33 sor, mind `igen`); `..._ALVIL-001.tsv` (13 kitöltött sor, mind `igen`) | A fájlok olvasásával ellenőrizve. A Jób 17:12-n és a Zsolt 88:4-en J1 és J2 jelzés áll (a BDB példahelye -/2/b, ill. -/3/b), ezek a `naplok/F123_cimke_javaslat_ALVIL-001.md` és az `F123_M1_ALVIL-001.md` szerint ismert kutatói kérdések. Az F148-napló 3. szakasza nem említi őket. |
| Elf. 5 / hat jelzéstípus | OK (kódolvasásból) | `eszkozok/teszt_szakasz_cimke_levezet.py:71-129` | A J1–J6 mindegyikére van teszt, a J7-re is. Nem futtattam. |
| `--ir` | OK | `szakasz_cimke_levezet.py:315-359`; teszt 159-180 | Meglévő címkét nem ír felül. Létező kulcsra `uj_sor` esetén megáll, nem üres kulcs pótlásakor megáll. Írás előtt és után összevet. A `--ir` nem futott: a `szotar_szakasz_cimke.tsv` diffje üres. |
| `--ir` és a 17. szabály | **ELTÉRÉS** (alacsony) | `szakasz_cimke_levezet.py:172-175` és `ellenoriz.py:1098-1102` | Az eszköz a `lexikon_hivatkozasok.tsv`-kulcsot csak TBESG-nél nézi. A 17. szabály BDB-n és Thayeren is megköveteli. Egy jelzés nélküli gépi `uj_sor` így 17. szabály szerinti SÉRTÉS-t okozhat. |
| Csak létező útvonal | OK | `szakasz_cimke_levezet.py:136-141, 179-181` | A jelöltek kizárólag a `bdb_sz`/`th_sz` útvonalaiból jönnek, különben J4. |
| Binyan-szűkítés | OK | `:182-191` | Csak akkor szűkít, ha a binyan és a jelölt is egyértelmű, különben J2. Az `o` (Polel) nincs leképezve, ilyenkor J2 jön: óvatos irány. |
| Kulcsolás a versmegfeleltetésen át (1Móz 4:26, Ézs 64:6) | OK | `Macula_heber_Ezsaias.tsv:24436` (`ISA 64:6!2`, karoli `Ézs 64:7`, `Vqrmsa`); `Karoli_versmegfeleltetes.tsv:23071` (`Ézs 64:6` → MT `64:6`) | `lekerdez.py scan H7121 --szakasz "Ézs 64:6"` → 1 igehely (`scope=range:Ézs 64:6 \| forras=TAHOT_kivonat.tsv \| strong=H7121 \| n=1 \| ts=2026-11-01T08:44Z`). `scan H7121 --szakasz "1Móz 4:26"` → 2 szó-előfordulás, n=1. Mindkettő Qal/2/c. |
| Kulcsolás, ha a táblában nincs MT | **ELTÉRÉS** (közepes, látens) | `szakasz_cimke_levezet.py:117-123` (`mt = _versmegf().get(karoli) or cv`) | Ahol a táblában nincs MT (Grep: 21 005 KJV osztályú sor), a kód a Károli-féle fejezet:verset MT-ként használja. Repóadat szerint ez hibás: `Karoli_versmegfeleltetes.tsv:16987` `Mik 5:1`, MT üres. A Macula `MIC 4:14!1` sorának karoli oszlopa `Mik 5:1`, a `MIC 5:1!1` soráé `Mik 5:2`. `lekerdez.py karoli "Mik 5:2"` → „De te, Efratának Bethleheme …”. A kód tehát Károli Mik 5:1-hez az MT 5:1 (= Károli 5:2) morfológiáját veszi. Ugyanez a helyzet a Zak 2:1-nél (`ZEC 2:1!1` → `Zak 1:18`). Az ISTENTISZT- és ALVIL-regressziót ez nem érinti, de új motívumon a binyan rossz versből jöhet, és a `--ir` jelzés nélkül írhat. Az N-F148b csak a Macula `karoli` oszlopát nevezi elavultnak, ezt az esetet nem fedi le. |
| N-F148a / mérőszkript | **ELTÉRÉS** (közepes) | `naplok/F148_meres.py:54`; `NYITOTT_FELADATOK.md` (N-F148a); napló:185 | A szkript a 54. sorban az F148.1-ben megszüntetett `LG.SZOTARI_GERINC_MOTIVUMOK`-ot olvassa (Grep: a `lexikon_general.py`-ban nincs definíció és `__getattr__` sem). A HEAD-en ezért `--forditas` előtt (149. sor) AttributeError-ral leáll. Az N-F148a és a #125-javaslat mégis erre a parancsra utal átmeneti JELENTÉS-ként. A napló „Mellékhatás” bekezdése csak a `F131_dbh_meres.py`-t sorolja fel. |
| (iii) — ismert | OK (a napló helyesen mondja ki) | napló:132; N-F148a | Nem gépi, nyitott tétel, a mért 4/0 és 1/0 aránnyal. |
| Commit-granularitás | **ELTÉRÉS** (alacsony, dokumentált) | commit `7648fb39` | A brief 2. lépése tételenkénti commitot kér, a négy szabály egy commitban van. A napló:140 és a commit-üzenet ezt indokolja. |
| Elf. 7 / „nulla diff” hatóköre | OK | — | `git diff --stat 63c7b344..HEAD -- lexikon adat/elofordulasok.tsv MUNKAMENET.md` üres, ugyanígy a `szotar_szakasz_cimke.tsv` és a `tiltott_fordulatok.tsv` diffje. A hatókör a forrásfájlokra vonatkozik. A renderelt kimenet bájtazonosságára nem, az NEM ELLENŐRIZHETŐ (Elf. 1). |
| Elf. 8 (csv, wrapper) | OK | `szakasz_cimke_levezet.py:29-41`; a tesztek 22-27. sora; `F148_meres.py:6-15` | Grep `^import csv\|csv\.` → 0. A wrapper az importok után áll. |
| Tesztek (6 db) | NEM ELLENŐRIZHETŐ | — | A futtatás kívül esik a megengedett parancsokon. A napló:164-171 szerint 26/17/61/47/6/70 OK, ezt nem igazoltam. |
| CI-jelentés | OK | — | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 63c7b344..HEAD) --diff-alap 63c7b344 --diff-fej HEAD --pr-cim "[ELLENŐRZŐ] F148: …" --esemeny pull_request`: E2–E32 0 HIBA. JELENTÉS: E25 4, E27 40, E30 2 (`karoli`, `szamkiosztas` ékezet nélkül a commit-üzenetben). Ez egyezik a napló 0 HIBA állításával. Az E1 nem része a `futtat.py`-nak. |
| ⛔ pontok | OK / NEM ELLENŐRIZHETŐ | DONTESEK DT437–d | 0.1: `git log origin/main --grep="pull request #513"` → `f711291d`. A 0. ⛔ megállás külön commit (`c0cfb53a`), a döntések utána jöttek (`b414ae72`). A felhasználó chates idézete NEM ELLENŐRIZHETŐ. Az ALVIL nem került kivétellistára, a szabály nem lazult. A `--ir` nem futott. A merge nem történt meg. |
| Kiszűrt/törölt sorok | OK | `git diff --numstat` | 15 törölt sor, mind módosítás, adatsor-törlés nincs: brief-fejléc 3, SEMA 5, `funkcio_kapcsolok` megjegyzéssor 1, `lexikon_general` 2, `teszt_szerepmatrix` 3, `teszt_szotari_gerinc` 1. |
| Kulcstartomány-lefedettség | OK | `adat/funkcio_kapcsolok.tsv` | A 9 motívum-id mindegyikének egyértelmű állapota van: 2 `aktiv`, 7 `kivetel`. |
| TSV Δ (E17, DT3) | OK | — | `adat/funkcio_kapcsolok.tsv` 5 → 12, Δ +7. Minden más `adat/` és `konkordancia/` alatti `.tsv` Δ 0. Egyik sem éri el a ≥10 küszöböt, bontási napló nem kell. |
| A1 / A3 / A5 / A6 | NEM ALKALMAZHATÓ | — | Nincs tanulmány, párhuzam, tanító, és az E12–E15 nem adott találatot. |
| A2 | OK | NYITOTT N-F148a/b | Mindkét tétel nyitott a repó szerint. Az N-F148a tartalmát lásd fent. |
| A4 | NEM ALKALMAZHATÓ | — | Nincs tanulmányfájl a diffben. |

**ELTÉRÉS-ek súlyossági sorrendben**
1. Közepes: a `F148_meres.py:54` a megszűnt konstanst olvassa, ezért az N-F148a átmeneti JELENTÉS-parancsa a HEAD-en leáll.
2. Közepes, látens: a `MaculaKaroli.get` MT nélküli tartalékága hibás, ahol a Károli és az MT számozása eltér (Mik 5:1, Zak 2:1). A binyan rossz versből jöhet.
3. Alacsony: a `--ir` BDB- és Thayer-sornál nem nézi a `lexikon_hivatkozasok.tsv`-kulcsot, ezért 17. szabály szerinti SÉRTÉS-t írhat.
4. Alacsony: a 21. (iv) N-mintája nem látja a lezárt, kiemelés nélküli N-tételeket.
5. Alacsony, dokumentált: a négy szabály egy commitban van.

**Az 5 kért pont verdiktje**
1. **Render-bájtazonosság: NEM ELLENŐRIZHETŐ.** A szerepkorlát miatt nem futtattam. Kódolvasásból a 9 motívum mindegyikén ekvivalens a régivel.
2. **18–21. szabály: OK.** A súlyosság a DT440 szerinti, a kivétellista egy helyen van, közös függvényen át. A „Baál nevével” nem jelzett, az N9999 jelzett. Egy alacsony súlyú látens rés van a (iv) N-mintájában.
3. **`szakasz_cimke_levezet.py`: részben OK.** Csak létező útvonalat ad, a regresszió 33/33 és 13/13, a hat jelzéstípusnak van tesztje, a `--ir` nem ír felül. Az 1Móz 4:26 és az Ézs 64:6 helyes. A tartalékág MT nélküli versnél hibás (közepes), és a `--ir` nem ellenőrzi a 17. szabály kulcsát (alacsony).
4. **CLAUDE.md-szabályok: OK.** Nincs `csv` modul, a wrapper az importok után áll, a `lexikon/`, az `adat/elofordulasok.tsv` és a `MUNKAMENET.md` nem változott.
5. **Tesztek: NEM ELLENŐRIZHETŐ.** Nem futtattam őket.

---

## A végrehajtó javításai (F148.8, 2026-11-01)

| ELTÉRÉS | javítás | igazolás |
|---|---|---|
| 1. `F148_meres.py:54` | a gerinces kör `LG.gerinc_aktiv`-ból | `python naplok/F148_meres.py` a 0.3-on át lefut: `['ALVIL-001', 'ISTENTISZT-001']` |
| 2. MT nélküli tartalékág | `MaculaKaroli.get`: ahol a versmegfeleltetés nem ad MT-t, a Károli fejezet:vers csak akkor MT, ha a Macula saját `karoli` oszlopa is ugyanazt a verset adja; különben nincs morfológia → J2 | `teszt_szakasz_cimke_levezet.py` `test_macula_mt_nelkuli_vers`, `test_valodi_mik_5_1`; a regresszió változatlan (33/33, 13/13) |
| 3. `--ir` és a 17. szabály | írás csak létező `lexikon_hivatkozasok.tsv`-kulcsra; különben J8 | `test_ellenoriz_teendok` (kulcs nélkül J8, kulccsal `uj_sor`/`kulcs_potlas`) |
| 4. lezárt N-tétel | a létező N-tételek közé a `* N<n> —` (lezárt) alak is | `teszt_ellenoriz_vedokorlat.py` `test_nem_letezo_n_sertes_letezo_nem` (N63 lezárt alakban, nem jelzett) |
| 5. commit-granularitás | dokumentált eltérés, nem javítva | napló 2. szakasz |

A render-bájtazonosságot (Elf. 1) és a teszteket a végrehajtó futtatta: 14/14 lap `cmp`-azonos (napló 1.), a tesztek a napló 5. szakasza szerint. A PR E1-lépése is piros lesz (⛔ A), nem csak a main: a napló 5. szakasza ezt pontosítja.
