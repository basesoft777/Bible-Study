# Független ellenőrzés: ISTENTISZT-001 olvasói forma (DT-F131t; brief-fájl nincs)

Tartomány: d5916f40..c6340e30 (5 commit). Ellenőr: `fuggetlen-ellenor` subagent, `claude-opus-5-5` (kért: `opus`).
A jelentést az ellenőr a válaszában adta (fájlíró eszköze nem volt); a végrehajtó mentette változatlan tartalommal.
A futás közben a munkakönyvtárban már a következő kör (DT-F131w, DT-F131x) nem commitolt változásai is álltak; a
megállapítások a HEAD-re (c6340e30) vonatkoznak.

ELTÉRÉS: 7 tétel

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | – | `claude-opus-5-5` = `opus`; a diffben nincs `modell` mező |
| A: 2. szerep = gerinc | OK | `lexikon/ISTENTISZT-001_TUDOMANYOS.md:600,706` | „Jelentéstartomány (szótári gerinc)” 0 találat; mindkét nyelven a „#### 2. Mélységi szócikk” alatt áll a Thayer- és a BDB-gerinc |
| A: 7. mutató törölve | OK | `:676,943` | `kézi SECE\|#70` 0 találat a `lexikon/`-ban |
| A: görög 8. → rokon | OK | `:682` | „LSJ-szócikk a rokon szavaknál (alább): G2564”; a G2564 LSJ-részlete: `:1096` |
| B: Mit mutat, lefedettség | OK | 34 sor | 11 generált szakasz + 23 szerep-blokk = 34; a hatókör-mondatok nem változtak. Megjegyzés: a 2/b., a Minősítés, az Alátámasztás és a Rokon szavak nem kapott bevezetőt |
| B/(4): fájlnév, szerepkód | OK | – | `Mit mutat.*(\.tsv\|\.py\|\.md\|G\d\b\|DT\|N-F\|#\d\|\[ID)` → 0 találat |
| B/(4): igaz-e az adatra | **ELTÉRÉS** | `:858,864` | A héber 6. bevezető a héber szó görög visszaadásáról szól, a H8034 sor viszont a קָרָא→G1941 egyezését számolja (a sor `strong` mezőjéből) |
| B/(4) | **ELTÉRÉS** | `:649,637,850` | Az 5. szerep bevezetője szerint a blokk megmondja, „hányszor fordul elő”; a blokk csak a szónézetre mutat. A 3. szerep „rövid teológiai szócikket” ígér, de csak mutatót ad |
| C: 1/b. csoportok és számok | OK | `:353–357` | 18+42+23+10 = 93 = 92 elutasított + 1 nyitott; az okok összege 92; „egyéb 1 (Zsolt 99:6)”; a `jeloltek.tsv` nem változott |
| C: okok besorolása | **ELTÉRÉS** | `:444–449`; `adat/elutasitasi_okok.tsv:7` | A 6 K3_jogi sor (ApCsel 25:11, 12, 21, 25; 26:32; 28:19) a 30-as („passzív … megnevezés jellegű”) mintára illeszkedik az 50-es „jogi fellebbezés” előtt |
| C: proveniencia lábjegyzetben | OK | `eszkozok/szerep_kizart.py:161` | |
| D/(2): LSJ-állítás | OK | `konkordancia/LSJ_teljes.tsv:1942` | a G1941 sor csonk; ékezetfüggetlen és HTML-entitásos keresés: önálló ἐπικαλέω-szócikk nincs (5 522 G-sor) |
| D/(3): 6. szerep | OK | `:657` ↔ `:1197–1221` | 19 egyező, 3 eltérő (Ézs 12:4, 2Móz 33:19, 34:5), 1 LXX-minusz (Zsolt 116:17) |
| D/(3): 9. szerep | **ELTÉRÉS** (alacsony) | `:688` ↔ `:99–108` | 10/10 stimmel, de az 1Pét 1:17 cellája két „(jelölt, nem egyértelmű)” jelentést hoz |
| D: héber 9. | **ELTÉRÉS** (alacsony) | `:955–957` | a HEAD-en csak szónézet-mutató |
| D/(6): 7. szerep párosítás | OK (megjegyzéssel) | `:667–674,882–941` | a két kétértelmű pár jelölve; a SECE_G G1941 a „קָרָא”-t kétszer adja |
| D/(6) | **ELTÉRÉS** (alacsony) | `:894` | a διαῤῥήσσω kiejtése „diarrégnümi” (a TBESG G1284 lemmájából), nem a kiírt alakból |
| D: „fordításra vár” | OK | `:882–941` | 55 görög szó, mind jelölve |
| (5) blokk_lxx bájt-azonosság | OK (közvetett) | `:1191` | a 3. szakaszban csak a „Mit mutat” hunk |
| (7) TSV | OK | – | `split('\t')`; nincs `csv` |
| (7) helyőrzők | OK (megjegyzéssel) | – | címsorban és `eszkozok/`-ban 0; a `DT-F131t` az `adat/elutasitasi_okok.tsv` proveniencia-mezőjében áll |
| (7) CRLF | OK | – | DONTESEK 488/488, NYITOTT 976/976, SEMA 1931/1931 |
| (7) commit-üzenet | **ELTÉRÉS** (alacsony) | – | az üzenetek „ISTENTISZT-001 arany, …”-val kezdődnek, tétel-azonosító (`F131.x:`) nélkül |
| (8) tesztek | NEM ELLENŐRIZHETŐ | – | szerepkorlát |
| CI-jelentés | NEM ELLENŐRIZHETŐ | – | a saját futás E28 HIBA-ja a nem commitolt munkakönyvtárból jött |

## A végrehajtó válasza

Döntés: DT-F131x.

1. Javítva: a „jogi fellebbezés” minta sorrendje 25 (a 30 elé); teszt: `teszt_szerep_kizart` (SEMA 2.43).
2. Javítva: a héber 6. sor és bevezető kimondja, hogy a motívum görög szavának egyezését méri.
3. Javítva: a 3. és az 5. szerep bevezetője a hivatkozást is megnevezi.
4. Javítva: a 9. szerep egyértelmű / jelölt / hozzárendelés nélküli bontásban számol.
5. Javítva: a héber 9. a gerinc-lapon mondat a sorszámmal és a szónézet linkjével.
6. Javítva: a kiírt görög alak, ha nem a TBESG-lemma, a saját gépi kiejtését kapja.
7. Nem javítva: a commit-üzenet előtagja a #131 utómunka-menetek (DT-F131s) közös gyakorlata („ISTENTISZT-001 arany, …”).
