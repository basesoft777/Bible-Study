# KAROLI_PONTOSSAG_jelentes.md — a Károli–héber/görög szópárosítás pontosságmérése (F172)

*FELADATOK #172 · `F172_KAROLI_PONTOSSAG_BRIEF.md` · 2026-11-05 · a futtató session és az ellenőr modellje: `claude-opus-5-5` (a futásnaplók szerint, nem Sonnet és nem gemini)*

A mért állapot: `adat/karoli_strong/` @ git `aa61de89` (a keret és a minta), változatlan (`git diff aa61de89 -- adat/` üres). A TAHOT/TAGNT a futáskori commit állapota. Minden szám mellett a forrásfájl, amelynek első sora a proveniencia (`scope=… | forras=… | ts=…`).

## 1. Összefoglaló

| | Becslés | 95% | Forrás |
|---|---|---|---|
| **Súlyozott egyezés a vak Opus-ellenőrrel**, minden pár (1 600 pár, 8 réteg) | **95,06%** | 93,81–96,32 | `f172/meres_eredmeny.tsv` |
| ebből ÓSZ / ÚSZ | 94,50% / 97,07% | 92,95–96,05 / 95,55–98,59 | ugyanott |
| tartalmi szó / morféma (H9001–H9049) | 96,44% / 90,74% | 95,20–97,69 / 87,18–94,29 | ugyanott |
| **Külső összevetés** (Bible-Discovery, 8 fejezet), a forrás által Strong-számmal jelölt szavak tartalmi párjai | **99,83–99,90%** | 99,59–99,96 | `f172/kulso/kulso_eredmeny.tsv` |
| Kalibráció a régi arannyal: vak ellenőr / gépi pár | 96,79% / 97,06% | 94,48–98,16 / 94,81–98,35 | `f172/meres_eredmeny.tsv` |

A két szám nem ugyanazt méri. A külső forrás szavanként **egy fő Strong-számot** jelöl, a ragban, elöljáróban, névelőben álló mellékszót nem; a fő-szó kapcsolat így szinte hibátlan (3 hiba 2 860 ellenőrzött párból). Az Opus-eltérések zöme éppen a mellékszavakon áll („egység határa”: 37/72), amelyet a külső forrás nem ellenőrizhet. A **mért pontosság tehát kapcsolattípusonként**: fő-szó kapcsolat ≈ 99,8% (külső), a teljes párkészlet ≈ 95,1% (vak Opus, konzervatív alsó becslés; ha az „egység határa” eseteket konvenciónak vesszük, 97,45% [96,52–98,38]).

**Nyitás (DT-F172b): mehet** — a 7. pont küszöbjavaslata mindhárom feltételben teljesül.

## 2. Keret és minta

- Keret: 598 715 pársor, 66 könyv (`f172/keret.tsv`). Rétegek és súlyok: Mózes `magas` (S+C) 52 844 (8,83%) · Mózes `alacsony` 69 690 (11,64%) · történeti 160 447 (26,80%) · költői 65 358 (10,92%) · próféták 118 446 (19,78%) · evangéliumok+ApCsel 79 223 (13,23%) · levelek 44 018 (7,35%) · Jelenések 8 689 (1,45%).
- Kimaradt (leíró): a `kezi` (fuggoben) tokenek 1 588, 45 versben; a párosítatlan tokenek (`betoldas`/`forditatlan`) könyvcsoportonként a `f172/keret.tsv`-ben.
- Morféma-pár (H9001–H9049): 157 163, az ÓSZ-párok 26%-a (DT-F172a (m1): a mintában arányosan, a jelentés külön is közli).
- Minta: rétegenként 200 egyszerű véletlen pár, mag `20261105` (`eszkozok/karoli_strong/pontossag_minta.py`, `f172/minta.tsv`); a determinizmust a `teszt_pontossag.py` igazolja.

## 3. A vak ellenőrzés

- Ellenőr: Opus (`claude-opus-5-5`, minden köteg `modell` mezője), előfizetésből, subagentekben (DT-F172a (u1)). Nem a párosítás modelljeinek egyike (Sonnet, gemini-3.8-flash).
- Vakság: az ellenőr a vers Károli-szövegét és a TAHOT/TAGNT szavait kapta (a #22 bemenet-formája, KJV nélkül), és a **cél Károli-szóhoz maga jelölte** az eredeti szavakat; a gépi pár nem látszott. Szabályok: a `f21p/prompt_v3.md` A–L pontjai, változatlanul (`f172/ellenor/utasitas.md`).
- 72 köteg, 1 791 vers, 2 315 cél (minta + régi arany), mind átment a kapun (`pontossag_ellenor.py --kapu`). Egy javítás: a 70. kötegben egy nem kért szó jelölése gépileg elhagyva (a fájl `javitas` mezője), a mérést nem érinti.
- A pár **helyes**, ha a gépi pár eredeti tokenje az ellenőr halmazában van.
- **Kalibráció** (a régi arany, `konkordancia/Karoli_Strong_kivonat.tsv`, 383 hármasból 374 mérhető, 9 kimaradt: a kifejezés nincs a versben / nincs vers): az ellenőr 96,79% (362/374), a gépi pár 97,06% (363/374); a `f21p/regi_arany_hibas.tsv` 3 mérhető sora nélkül 97,57% / 97,84%. Az ellenőr tehát nem megbízhatóbb a párosításnál: az egyezés vele a pontosság **alsó** becslése (az eltérés egy része az ellenőr hibája).

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

A súlyozott becslés rétegzett (a rétegek pársúlyával), a CI normál közelítésű. A `magas` (két modell egyezése) réteg 99,0%-a a kétmodelles párosítás hasznát mutatja: a csak-Sonnet Mózes-réteg (92,0%) ugyanazon könyvekből 7 ponttal gyengébb.

**Hibatípusok** (72 eltérés): egység határa 37 (tartalmi 20, morféma 17) · rossz szó a versben 17 (12 / 5) · fölös pár 16 (12 / 4) · azonos lexéma, más előfordulás 2 (morféma). Az „egység határa” zöme egy szomszédos héber előtag vagy névelő hozzákötése a szóhoz a szabályokkal ellentétben (pl. `וַ` a „méne” mellett az I szabály ellenére, `הַ` a „folyó” mellett az A szabály ellenére). Hiányzó pár (leíró, nem a pontosság része): 18 célnál jelölt az ellenőr a gépinél több tokent.

## 5. Külső összevetés (Bible-Discovery)

**Forrás**: Bible-Discovery (Biblia-Felfedező), Strong-számos Károli (HUN) modul, **a program szerinti régies változat** (a felhasználó közlése, az orkesztrátoron át). Zárt, fizetős modul: csak mérésre; a bemásolt szöveg a repón kívül maradt, a repóba csak a saját párjaink osztálya és az összesítés került (`f172/kulso/osszevetes.tsv`, `fejezet_osszesites.tsv`, `elteres_itelet.tsv`, `kulso_eredmeny.tsv`; DT32-elv, DT-F172a).

**Egység**: rétegenként egy teljes fejezet (a felhasználó: „max egy teljes rész tudok másolni”, „8 fejezet”): 3Móz 3, 1Móz 7, 2Kir 10, Péld 3, Ez 43, ApCsel 12, Róm 1, Jel 19 (`f172/kulso/fejezetek.tsv`). A fejezetek klaszterek (rétegenként a legtöbb célpárt tartalmazó, azonos számozású, 15–40 verses), nem véletlen mintaelemek: a CI alulbecsüli a bizonytalanságot.

**Kiadás és számozás**: mind a 217 vers megvan a forrásban, többlet és hiány nélkül (a versszámozás 8/8 fejezetben azonos). A szöveg és a `Karoli_1908.tsv` szóalak-összevetése (4 388 Károli-szó): azonos 4 054 (92,4%) · helyesírás 19 · összevonás („a mely” ↔ „amely”) 168 · más alak 135 · nem igazítható 12. Ez a két kiadás különbsége, nem párosítási hiba; a szóalak az összevetésben csak igazítási támasz, a kulcs a szó helye és a Strong-szám.

**Formátum** (az elemző, `pontossag_kulso.py --osszevet`): a szó UTÁN álló számcsoport; a 0, az igealak-kód (héber > 8674, görög > 5624) és a 8675-ös Ketiv/Qere-kód eldobva; a sorvégi `*( … )` megjegyzés figyelmen kívül; a `[ ]` betoldásjel elhagyva; az ÚSZ-könyvnév („Apcs”) a Károli-rövidítésre kulcsolva.

**Osztályok** (3 388 tartalmi pár; *forras=f172/kulso/kulso_eredmeny.tsv*):

| osztály | db | jelentés |
|---|---|---|
| egyezik | 2 580 | a pár Strongja a forrás szavának Strongja |
| másodlagos | 197 | a forrás a szó fő Strongját adja, és az egyezik egy másik gépi párral; ez a pár a rag/elöljáró mellékszava (H5921 47, G0846 33, H0413 24, G3588 23, …) — a forrás nem ellenőrzi |
| számozás (konvenció) | 49 | ugyanaz a lexéma a két Strong-rendszerben más számon (héber: H1980/H3212, H7122/H7125; görög: a KJV-Strong alakszámai a névmásra, εἰμί-re, οὗτος-ra, valamint οἶδα 1492 / TAGNT G6063) |
| eltér — a forrás hibája | 29 | a vak Opus a gépi tokent jelöli, a forrásét nem (zömmel eltolt Strong, pl. 1Móz 7:20, 2Kir 10:5) |
| eltér — vitatható | 2 | 2Kir 10:15 „é”, Róm 1:12 „Azaz” |
| eltér — **a mi hibánk** | **3** | Péld 3:18 „Életnek” ↔ „fája” (felcserélt pár, 2 pár), Ez 43:13 „közsinget” |
| a forrásban nincs Strong | 522 | nem ellenőrizhető (ha, akár, a mely, mind, különírt igekötő, névmások) |
| szövegforma | 6 | a szó nem igazítható a forrás szövegéhez |

A háromutas ítélet (gépi pár · forrás · vak Opus, `f172/ellenor/valasz/kulso_*.json`) szabálya: az Opus a forrás Strongját jelöli, a gépit nem → a mi hibánk; fordítva → a forrás hibája; mindkettő vagy egyik sem → vitatható. Ez **javaslat**; a vitatható esetek a felhasználóé (6. pont).

Pontosság a forrás által Strong-számmal jelölt szavak párjain (n = 2 860, a másodlagos is): **99,83%** (a vitatható is hiba) – **99,90%** (nem az), Wilson 95% 99,59–99,96. Csak a fő-szó kapcsolatokon (a másodlagos nélkül, n = 2 663): 99,81–99,89%. ÓSZ 99,73–99,80% (n = 1 504), ÚSZ 99,93–100% (n = 1 356). Szószinten (a forrás Strong-halmaza része-e a gépi partnerhalmaznak): 2 452 / 2 525 = 97,11%; a különbség a forrás hibái és a konvenció részleges esetei.

**Az Opus-eltérések lefedése**: a 72 minta-eltérésből 9 esik a 8 fejezetbe (8 tartalmi, 1 morféma). Sorsuk: másodlagos 5 (a forrás nem ellenőrzi: 3Móz 3:10, 2Kir 10:25, ApCsel 12:17, Jel 19:2, Jel 19:3) · a forrás a gépi párt igazolja 1 (Róm 1:12 „egymás” → ἐν; az Opus tévedett) · a forrás az Opust igazolja 1 (Péld 3:18 „Életnek” → a mi hibánk) · a forrásban nincs Strong 1 (Ez 43:19) · morféma 1 (1Móz 7:15). A többi 63 eltérés becslése az Opus-ítéleten és a régi arany kalibrációján nyugszik. A minta Opus-egyezéseiből 31 pár esik a fejezetekbe (ebből 2 morféma): 22 egyezik, 5 a forrásban nincs, 1 szövegforma, 1 eltér (ApCsel 12:17 „ki”, a háromutas ítélet szerint a forrás hibája) — közös (gépi + Opus) hibát a forrás nem jelzett.

## 6. Kétes esetek a felhasználónak

1. **2Kir 10:15 „é”** (Károli 23. szó): a gépi pár H3426 (יֵשׁ), az Opus a kérdő partikulát (הֲ, H9008), a forrás egy harmadik szót jelöl. A kérdő „-é” a יֵשׁ-hez vagy a kérdő partikulához tartozik?
2. **Róm 1:12 „Azaz”** (1. szó): a gépi párok G3778, G1161, G1510 (τοῦτο δέ ἐστιν); a G3778 és a G1510 a forrás alakszámaival konvenció szerint egyezik, a G1161 (δέ) nem, és az Opus sem a δέ-t jelöli. A „δέ” a kapcsolás része legyen-e?
3. **A „mi hibánk” hármas megerősítése**: Péld 3:18 (az „Életnek” H6086 ← helyesen H2416; a „fája” H2416 ← helyesen H6086) és Ez 43:13 „közsinget” (H2948 ← a forrás és az Opus szerint H0520). A javítás nem ennek a feladatnak a része (N-F172a).

## 7. Végső becslés és nyitási küszöb (DT-F172b)

**Becslés**:
- fő-szó kapcsolat (lexikai pár): ≈ **99,8%** (külső, 8 fejezet, 2 663–2 860 pár; klaszter-minta, a CI szűkebb a valósnál);
- a teljes párkészlet, a mellékszavakkal és a morfémákkal: **95,1%** [93,8–96,3] (vak Opus, konzervatív alsó becslés); felső tájékoztató 97,5% (az „egység határa” konvenciónak véve);
- morféma-párok: 90,7% [87,2–94,3] (csak Opus; a külső forrás nem ellenőrzi).

**Küszöbjavaslat a nyitáshoz**: a párosítás nyílt adatként közölhető (CC BY 4.0, TAHOT/TAGNT-attribúció), ha (1) a külső fő-szó pontosság 95%-os alsó széle ≥ 98% — **teljesül** (99,59%); (2) a vak ellenőrrel mért súlyozott egyezés alsó széle ≥ 93%, és egyetlen réteg pontbecslése sem 90% alatti — **teljesül** (93,81%; a legkisebb 92,0%); (3) a közlés a pontosságot kapcsolattípusonként (fő-szó / mellékszó / morféma) és rétegenként közli, a `bizonyossag` és a „javaslat” állapot megmarad, és a talált rendszerhibák (N-F172a–b) nyitott tételként állnak — **a közlés feltétele**. **A mért pontosság alapján a nyitás mehet.**

## 8. Korlátok

- Az Opus-egyezés nem arany: a kalibráció szerint az ellenőr a régi aranyon nem jobb a párosításnál. Az egyezés alsó becslés; a közös hibát csak a külső összevetés (és csak a fő-szavakon) becsli.
- A külső forrás a mellékszó-, a névelő- és a morféma-kapcsolatot nem jelöli: ezekre csak az Opus-szám érvényes. A forrás Strong-jelölése 522/3 388 tartalmi páron hiányzik (15%).
- A 8 fejezet klaszter (rétegenként egy), nem véletlen minta; a fejezetek kiválasztása a célpárok szerint történt.
- A recall nem cél: a hiányzó párok csak leíró számok (18 a mintában; 43 a fejezetekben a forrás Strongos szaván, nálunk tartalmi pár nélkül).
- A régi arany 383 hármasa csak részben fedi a rétegeket (könyvenként 0–17), és 9 hármasa nem mérhető.

## 9. Nyitott tételek (`nyitott/uj/goofy-turing-b0eb00.md`)

- **N-F172a**: a 3 talált párhiba javítása (Péld 3:18 felcserélt pár, Ez 43:13 „közsinget”), a #22 javító menetében.
- **N-F172b**: az „egység határa” rendszerhiba (a szabályokkal ellentétesen a szóhoz kötött `ve-`/névelő/elöljáró) generátorszintű vizsgálata: szabályalapú utófeldolgozás az `egyesit.py`-ban, CI-kapuval, nem laponkénti folttal.
- **N-F172c**: a morféma-párok külön ellenőrzése (a külső forrás nem fedi; 90,7%).
