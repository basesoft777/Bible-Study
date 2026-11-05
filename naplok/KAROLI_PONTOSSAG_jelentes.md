# KAROLI_PONTOSSAG_jelentes.md — a Károli–héber/görög szópárosítás pontosságmérése (F172)

*FELADATOK #172 · `F172_KAROLI_PONTOSSAG_BRIEF.md` · 2026-11-05 · a futtató session és az ellenőr modellje: `claude-opus-5-5` (a futásnaplók szerint, nem Sonnet és nem gemini) · független ellenőrzés: `naplok/ELLENOR_F172.md` (9 eltérés, mind átvezetve, l. 10.)*

A mért állapot: `adat/karoli_strong/` @ git `aa61de89` (a keret és a minta), változatlan (`git diff aa61de89 -- adat/` üres). A TAHOT/TAGNT a futáskori commit állapota. Minden szám mellett a forrásfájl, amelynek első sora a proveniencia (`scope=… | forras=… | ts=…`).

## 1. Összefoglaló

| | Becslés | 95% | Forrás |
|---|---|---|---|
| **Súlyozott egyezés a vak Opus-ellenőrrel**, minden pár (1 600 pár, 8 réteg) | **95,06%** | 93,81–96,32 | `f172/meres_eredmeny.tsv` |
| ebből ÓSZ / ÚSZ | 94,50% / 97,07% | 92,95–96,05 / 95,55–98,59 | ugyanott |
| tartalmi szó / morféma (H9001–H9049) | 96,44% / 90,74% | 95,20–97,69 / 87,18–94,29 | ugyanott |
| **Külső összevetés** (Bible-Discovery, 8 fejezet), fő-szó párok (n = 2 663), **tisztán a forrás szerint** | **98,72%** | 98,22–99,08 | `f172/kulso/kulso_eredmeny.tsv` |
| ugyanott, háromutas ítélettel (gépi pár · forrás · vak Opus, DT624) | 99,81% | 99,56–99,92 | ugyanott |
| Kalibráció a régi arannyal: vak ellenőr / gépi pár | 96,79% / 97,06% | 94,48–98,16 / 94,81–98,35 | `f172/meres_eredmeny.tsv` |

A számok nem ugyanazt mérik. A külső forrás szavanként **egy fő Strong-számot** jelöl, a ragban, elöljáróban, névelőben álló mellékszót nem; a külső szám ezért csak a fő-szó párokra érvényes. Tisztán a forrás szerint (a forrás minden eltérését a mi hibánknak számolva) a fő-szó egyezés 98,72%; a 34 eltérés háromutas ítélete után 5 marad a mi hibánk (DT624), a fő-szó pontosság így 99,81%. A teljes párkészletre (mellékszavak, morfémák) csak a vak Opus-egyezés áll rendelkezésre: 95,06%. Ez a pontosság alsó becslése, **ha** a közös (gépi = Opus) hiba elhanyagolható; ezt a külső összevetés csak a fő-szó párokon méri (5. pont: a 8 fejezetbe eső 29 tartalmi Opus-egyezés között a forrás közös hibát nem jelzett).

**Nyitás (DT623)**: a párosítás nyílt adatként közölhető, mert a pontossága **mérve és dokumentálva van** — kapcsolattípusonként és rétegenként, konfidencia-intervallummal; a „javaslat” állapot és a `bizonyossag` megmarad, az ismert hibák nyitott tételként állnak (7. pont). A nyitás nem küszöb teljesülésén alapul; a küszöbök a 2. kiadás előre rögzített minőségi céljai.

## 2. Keret és minta

- Keret: 598 715 pársor, 66 könyv (`f172/keret.tsv`). Rétegek és súlyok: Mózes `magas` (S+C) 52 844 (8,83%) · Mózes `alacsony` 69 690 (11,64%) · történeti 160 447 (26,80%) · költői 65 358 (10,92%) · próféták 118 446 (19,78%) · evangéliumok+ApCsel 79 223 (13,23%) · levelek 44 018 (7,35%) · Jelenések 8 689 (1,45%).
- Kimaradt (leíró): a `kezi` (fuggoben) tokenek 1 588, 45 versben. A teljesen `kezi` verseknek (N-F22e) nincs pársoruk; a részben `kezi` versek (1:2 beolvasztás, pl. Péld 11:31) többi párja a keretben marad (a `kezi` tokenhez pár nem tartozik) — pontosítás a brief 2.3 szövegéhez, a mintában ilyen vers nem szerepel.
- Morféma-pár (H9001–H9049): 157 163 — az ÓSZ-párok (466 785) **33,7%-a**, az összes pár 26,3%-a (DT622 (m1): a mintában arányosan; a mintában 339/1 000 ÓSZ-pár).
- Minta: rétegenként 200 egyszerű véletlen pár, mag `20261105` (`eszkozok/karoli_strong/pontossag_minta.py`, `f172/minta.tsv`); a determinizmust a `teszt_pontossag.py` igazolja.

## 3. A vak ellenőrzés

- Ellenőr: Opus (`claude-opus-5-5`, minden válaszfájl `modell` mezője: 79/79), előfizetésből, subagentekben (DT622 (u1)). Nem a párosítás modelljeinek egyike (Sonnet, gemini-3.8-flash).
- Vakság: az ellenőr a vers Károli-szövegét és a TAHOT/TAGNT szavait kapta (a #22 bemenet-formája, KJV nélkül), és a **cél Károli-szóhoz maga jelölte** az eredeti szavakat; a gépi pár nem látszott. Szabályok: a `f21p/prompt_v3.md` A–L pontjai, változatlanul (`f172/ellenor/utasitas.md`).
- 72 köteg, 1 791 vers, 2 315 cél (minta + régi arany), mind átment a kapun (`pontossag_ellenor.py --kapu`). Egy javítás: a 70. kötegben egy nem kért szó jelölése gépileg elhagyva (a fájl `javitas` mezője), a mérést nem érinti.
- A pár **helyes**, ha a gépi pár eredeti tokenje az ellenőr halmazában van.
- **Kalibráció** (a régi arany, `konkordancia/Karoli_Strong_kivonat.tsv`, 383 hármasból 374 mérhető, 9 kimaradt: a kifejezés nincs a versben / nincs vers): az ellenőr 96,79% (362/374), a gépi pár 97,06% (363/374); a `f21p/regi_arany_hibas.tsv` 3 mérhető sora nélkül 97,57% / 97,84%. Az ellenőr tehát nem megbízhatóbb a párosításnál: az eltérés egy része az ellenőr hibája.

## 4. Rétegenkénti eredmény (egyezés a vak ellenőrrel)

*forras=f172/meres_eredmeny.tsv*

| Réteg | n | helyes | p | Wilson 95% |
|---|---|---|---|---|
| Mózes, `magas` (S+C) | 200 | 198 | 99,00% | 96,43–99,73 |
| Mózes, `alacsony` | 200 | 184 | 92,00% | 87,40–95,02 |
| történeti | 200 | 190 | 95,00% | 91,04–97,26 |
| költői | 200 | 190 | 95,00% | 91,04–97,26 |
| próféták | 200 | 186 | 93,00% | 88,59–95,78 |
| evangéliumok+ApCsel | 200 | 196 | 98,00% | 94,97–99,22 |
| levelek | 200 | 191 | 95,50% | 91,67–97,61 |
| Jelenések | 200 | 193 | 96,50% | 92,95–98,29 |
| **ÓSZ, súlyozott** | 1 000 | 948 | 94,50% | 92,95–96,05 |
| **ÚSZ, súlyozott** | 600 | 580 | 97,07% | 95,55–98,59 |
| **összes, súlyozott** | 1 600 | 1 528 | **95,06%** | 93,81–96,32 |

A súlyozott becslés rétegzett (a rétegek pársúlyával), a CI normál közelítésű. A `magas` réteg (1–2Móz, két modell egyezése) 99,0%, a Mózes `alacsony` réteg 92,0%; a két réteg könyvei azonban nagyrészt eltérnek (az `alacsony` minta 200 párjából 188 a 3–5Mózesből), ezért a különbség nem csak a kétmodelles párosítás hatása, könyv-hatás is lehet.

**Hibatípusok** (72 eltérés; *forras=f172/meres_eredmeny.tsv*, `hibatipus` sorok): szomszédos token 37 (tartalmi 20, morféma 17) · rossz szó a versben 17 (12 / 5) · fölös pár 16 (12 / 4) · azonos lexéma, más előfordulás 2 (0 / 2). A „szomszédos token” helyzeti címke: a gépi pár tokenje az ellenőr halmazának szomszédja. Gyakran egy héber előtag vagy névelő hozzákötése a szóhoz a szabályokkal ellentétben (pl. `וַ` a „méne” mellett az I szabály, `הַ` a „folyó” mellett az A szabály ellenére), de valódi felcserélést (Péld 3:18) és Opus-hibát (Róm 1:12 „egymás”, l. 5.) is takar; a típus tehát nem konvenció. Hiányzó pár (leíró, nem a pontosság része): 18 célnál jelölt az ellenőr a gépinél több tokent.

## 5. Külső összevetés (Bible-Discovery)

**Forrás**: Bible-Discovery (Biblia-Felfedező), Strong-számos Károli (HUN) modul, **a program szerinti régies változat** (a felhasználó közlése, az orkesztrátoron át). Zárt, fizetős modul: csak mérésre; a bemásolt szöveg a repón kívül maradt, a repóba csak a saját párjaink osztálya és az összesítés került (`f172/kulso/osszevetes.tsv`, `fejezet_osszesites.tsv`, `elteres_itelet.tsv`, `kulso_eredmeny.tsv`; DT32-elv, DT622). Egyedi forrás-Strong érték a jelentésbe sem kerül.

**Egység**: rétegenként egy teljes fejezet (a felhasználó: „max egy teljes rész tudok másolni”, „8 fejezet”): 3Móz 3, 1Móz 7, 2Kir 10, Péld 3, Ez 43, ApCsel 12, Róm 1, Jel 19 (`f172/kulso/fejezetek.tsv`). A fejezetek klaszterek (rétegenként a legtöbb célpárt tartalmazó, azonos számozású, 15–40 verses), nem véletlen mintaelemek: a CI alulbecsüli a bizonytalanságot.

**Kiadás és számozás** (*forras=f172/kulso/fejezet_osszesites.tsv*): mind a 217 vers megvan a forrásban, többlet és hiány nélkül (a versszámozás 8/8 fejezetben azonos). A szöveg és a `Karoli_1908.tsv` szóalak-összevetése (4 388 Károli-szó): azonos 4 054 (92,4%) · helyesírás 19 · összevonás („a mely” ↔ „amely”) 168 · más alak 135 · nem igazítható 12. Ez a két kiadás különbsége, nem párosítási hiba; a szóalak az összevetésben csak igazítási támasz, a kulcs a szó helye és a Strong-szám.

**Formátum** (az elemző, `pontossag_kulso.py --osszevet`): a szó UTÁN álló számcsoport; a 0, az igealak-kód (héber > 8674, görög > 5624) és a 8675-ös Ketiv/Qere-kód eldobva; a sorvégi `*( … )` megjegyzés figyelmen kívül; a `[ ]` betoldásjel elhagyva; az ÚSZ-könyvnév („Apcs”) a Károli-rövidítésre kulcsolva.

**Osztályok** (3 388 tartalmi pár; *forras=f172/kulso/kulso_eredmeny.tsv*):

| osztály | db | jelentés |
|---|---|---|
| egyezik | 2 580 | a pár Strongja a forrás szavának Strongja |
| számozás (konvenció) | 49 | ugyanaz a lexéma a két Strong-rendszerben más számon (héber: H1980/H3212, H7122/H7125; görög: a KJV-Strong alakszámai a névmásra, εἰμί-re, οὗτος-ra, valamint οἶδα 1492 / TAGNT G6063; általános számozási tudás, `pontossag_kulso.py` `_KONV_CSOPORT`) |
| eltér — a forrás hibája | 29 | a vak Opus a gépi tokent jelöli, a forrásét nem (zömmel eltolt Strong, pl. 1Móz 7:20, 2Kir 10:5) |
| eltér — **a mi hibánk** | **5** | Péld 3:18 „Életnek” ↔ „fája” (felcserélt pár, 2 pár), Ez 43:13 „közsinget”, 2Kir 10:15 „é”, Róm 1:12 „Azaz” (δέ) — az utóbbi kettő a DT624 döntése |
| másodlagos | 197 | a forrás a szó fő Strongját adja, és az egyezik egy másik gépi párral; ez a pár a rag/elöljáró mellékszava (H5921 47, G0846 33, H0413 24, G3588 23, …) — **a forrás nem ellenőrzi** |
| a forrásban nincs Strong | 522 | nem ellenőrizhető (ha, akár, a mely, mind, különírt igekötő, névmások) |
| szövegforma | 6 | a szó nem igazítható a forrás szövegéhez |

A háromutas ítélet (gépi pár · forrás · vak Opus, `f172/ellenor/valasz/kulso_*.json`) szabálya: az Opus a forrás Strongját jelöli, a gépit nem → a mi hibánk; fordítva → a forrás hibája; mindkettő vagy egyik sem → vitatható. A két vitatható esetet a DT624 döntötte el (mindkettő a mi hibánk); vitatható nem maradt.

**Pontosság a fő-szó párokon** (n_fo = egyezik + konvenció + eltér = 2 663): tisztán a forrás szerint 2 629/2 663 = **98,72%** [98,22–99,08]; háromutas ítélettel (2 663 − 5)/2 663 = **99,81%** [99,56–99,92]. ÓSZ: 98,93% / 99,71% (n = 1 397); ÚSZ: 98,50% / 99,92% (n = 1 266). Szószinten (a forrás Strong-halmaza része-e a gépi partnerhalmaznak): 2 452 / 2 525 = 97,11%; a különbség a forrás hibái és a konvenció részleges esetei. A 197 másodlagos, a 522 Strong nélküli és a 6 szövegforma pár (725, a tartalmi párok 21,4%-a) külsőleg nem ellenőrzött.

**A minta-párok a 8 fejezetben** (*forras=f172/kulso/kulso_eredmeny.tsv*, második blokk): a 72 Opus-eltérésből 9 esik a fejezetekbe (8 tartalmi, 1 morféma). Sorsuk: másodlagos 5 (a forrás nem ellenőrzi: 3Móz 3:10, 2Kir 10:25, ApCsel 12:17, Jel 19:2, Jel 19:3) · a forrás a gépi párt igazolja 1 (Róm 1:12 „egymás” → ἐν; az Opus tévedett) · a forrás az Opust igazolja 1 (Péld 3:18 „Életnek”, a mi hibánk) · a forrásban nincs Strong 1 (Ez 43:19) · morféma 1 (1Móz 7:15). A többi 63 eltérés megítélése csak az Opus-ítéleten és a régi arany kalibrációján nyugszik. A minta 1 528 Opus-egyezéséből 31 esik a fejezetekbe (ebből 2 morféma): 22 egyezik, 5 a forrásban nincs Strong, 1 szövegforma, 1 eltér (ApCsel 12:17 „ki”, a háromutas ítélet szerint a forrás hibája) — a forrás közös (gépi = Opus) hibát nem jelzett; a mérhető esetek száma kicsi (23).

## 6. Kétes esetek — eldöntve (DT624)

Az orkesztrátor a felhasználó felhatalmazásával (2026-11-05):
1. **2Kir 10:15 „é”**: a kérdő „-é” a kérdő partikula (הֲ, H9008), nem a יֵשׁ; a gépi pár (H3426) hiba, a יֵשׁ az „olyan” szóhoz tartozik.
2. **Róm 1:12 „Azaz”**: a magyar szó a τοῦτ' ἔστιν kifejezés; a δέ (G1161) fordítatlan, nem része a párnak; a G3778 és a G1510 igen.
3. **Péld 3:18 és Ez 43:13**: a hiba megerősítve. A Péld 3:18-ban az „Életnek” és a „fája” párja felcserélt (a TAHOT-glossza szerint is); az Ez 43:13 „közsinget” párja az Opus-ítélet szerint más szóra tartozik. A javítás az N-F172a, nem e feladat része.

## 7. Végső becslés, a nyitás indoka (DT623) és a 2. kiadás minőségi célja

**Becslés**:
- fő-szó kapcsolat (lexikai pár): **98,72%** [98,22–99,08] tisztán a forrás szerint; **99,81%** [99,56–99,92] a háromutas ítélettel (8 fejezet, n = 2 663; klaszter-minta, a valós bizonytalanság nagyobb);
- a teljes párkészlet, a mellékszavakkal és a morfémákkal: **95,06%** [93,81–96,32] (vak Opus-egyezés; alsó becslés, ha a közös hiba elhanyagolható);
- morféma-párok: 90,74% [87,18–94,29] (csak Opus; a külső forrás nem ellenőrzi).

**A nyitás indoka (DT623; az orkesztrátor döntése a felhasználó felhatalmazásával, 2026-11-05)**: a párosítás nyílt adatként közölhető (CC BY 4.0, TAHOT/TAGNT-attribúció), mert a pontossága mérve és dokumentálva van — kapcsolattípusonként (fő-szó / mellékszó / morféma) és rétegenként, konfidencia-intervallummal (ez a jelentés); a „javaslat” állapot és a `bizonyossag` mező megmarad, az ismert hibák nyitott tételként állnak (N-F172a–c). A nyitás **nem** egy küszöb teljesülésén alapul: a mérés előtt nem volt rögzített kritérium, és utólag felállított küszöb utólagos kritériumnak látszana.

**Minőségi cél a 2. kiadásra** (előre rögzített kritérium a következő kiadás méréséhez; **az 1. kiadás eredményeinek ismeretében fogalmaztuk meg**, ezért az 1. kiadásra nem alkalmazzuk): (1) a külső fő-szó egyezés tisztán a forrás szerinti 95%-os alsó széle ≥ 98% (az 1. kiadásban 98,22%); (2) a vak ellenőrrel mért súlyozott egyezés alsó széle ≥ 93%, és egyetlen réteg pontbecslése sem 90% alatti (az 1. kiadásban 93,81%, a legkisebb réteg 92,0%); (3) a mérés ugyanezzel a protokollal fut (rétegzett minta, vak ellenőr, független külső forrás), és a közlés kapcsolattípusonként és rétegenként adja meg a pontosságot. A célt az N-F172a–b javítása után új mérés igazolja.

## 8. Korlátok

- Az Opus-egyezés nem arany: a kalibráció szerint az ellenőr a régi aranyon nem jobb a párosításnál. Az egyezés csak akkor alsó becslés, ha a közös hiba elhanyagolható; ezt a külső összevetés csak a fő-szó párokon és kevés (23) mérhető esetben vizsgálta.
- A külső forrás a mellékszó-, a névelő- és a morféma-kapcsolatot nem jelöli: ezekre csak az Opus-szám érvényes. A forrás Strong-jelölése 522/3 388 tartalmi páron hiányzik (15,4%).
- A 8 fejezet klaszter (rétegenként egy), nem véletlen minta; a fejezetek kiválasztása a célpárok szerint történt.
- A háromutas ítélet az Opusra támaszkodik, amelynek a hibája a régi aranyon ~3%.
- A recall nem cél: a hiányzó párok csak leíró számok (18 a mintában; 43 a fejezetekben a forrás Strongos szaván, nálunk tartalmi pár nélkül).
- A régi arany 383 hármasa csak részben fedi a rétegeket (könyvenként 0–17), és 9 hármasa nem mérhető.

## 9. Nyitott tételek (`nyitott/uj/goofy-turing-b0eb00.md`)

- **N-F172a**: az 5 megerősített párhiba javítása (Péld 3:18 felcserélt pár, Ez 43:13 „közsinget”, 2Kir 10:15 „é”, Róm 1:12 „Azaz” δέ), a #22 javító menetében.
- **N-F172b**: a „szomszédos token” eltérések (37/72) átnézése; ahol a gépi pár a szabályokkal (prompt_v3 A, I) ellentétesen köti a szomszédos `ve-`-t, névelőt vagy elöljárót a szóhoz, generátorszintű javítás (szabályalapú utófeldolgozás, CI-kapuval), nem laponkénti folt.
- **N-F172c**: a morféma-párok (az ÓSZ-párok 33,7%-a) független ellenőrzése (a külső forrás nem fedi; Opus szerint 90,7%).

## 10. A független ellenőrzés átvezetése (`naplok/ELLENOR_F172.md`)

1. (4a) A külső főcím a tisztán forrás szerinti fő-szó egyezés (98,72%); a másodlagos párok kikerültek a nevezőből, a háromutas szám mellette áll.
2. (4b) Az „egység határa” címke „szomszédos token” lett (helyzeti címke); a 97,45%-os „konvenciónak véve” érték törölve; az N-F172b szövege átnézést ír elő.
3. (4c) A `magas`/`alacsony` Mózes-réteg ok-okozati állítása törölve (könyv-hatás).
4. A morféma-arány: az ÓSZ-párok 33,7%-a (az összes 26,3%-a), a DT-F172a-ban és az N-F172c-ben is javítva.
5. (4.5) A kétes esetek eldöntve (DT624), a pontosság átszámolva; a nyitás indoka a mért és dokumentált pontosság, nem utólagos küszöb; a küszöbjavaslat a 2. kiadás előre rögzített minőségi céljává vált (7.).
6. (4d) Az Opus-szám alsó becslés volta feltételhez kötve.
7. DT622: egyedi forrás-Strong érték nem áll a jelentésben és az N-F172a-ban.
8. Proveniencia: a hibatípusok tartalmi/morféma bontása a `f172/meres_eredmeny.tsv`-ben, a minta-párok sorsa a `f172/kulso/kulso_eredmeny.tsv`-ben.
9. A részben `kezi` versek párjainak keretbeli helyzete a 2. pontban pontosítva (a mintát nem érinti).
