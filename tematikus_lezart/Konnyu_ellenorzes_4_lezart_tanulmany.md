# Könnyű, feltáró ellenőrzés — 4 lezárt tematikus tanulmány (Tehóm, Segítségül hívni az Úr nevét, Rafeusok/óriás-népek, Hádész) — v1

*v1 — 2026.08.25. A `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` 8. szakaszának nyitott pontja
("A négy már lezárt tematikus tanulmány visszamenőleges STEPBible-ellenőrzése") alapján, a 7.2-es
tematikus workflow szerint, a `genezis/Konnyu_ellenorzes_1-16_osszesito_v2.md` mintájára.*

**FONTOS — ez a fájl kizárólag feltáró jellegű.** Egyetlen tanulmányfájl vagy motívumlog-bejegyzés
sem lett módosítva. A join-tábla-építés (Károli-Strong) ennek a futásnak NEM része.

**Fájlhely-megjegyzés:** a feladatkiírás `tematikus/Konnyu_ellenorzes_4_lezart_tanulmany.md` útvonalat
adott meg, de a projektben nincs önálló `tematikus/` könyvtár — a négy vizsgált tanulmány a
`tematikus_lezart/` mappában van. A `genezis/`-beli precedenst követve (az összesítő a forrás-mappában
készült) ez a fájl is a `tematikus_lezart/` mappába került.

---

## ⚠️ Kritikus módszertani előfeltétel — a `TAHOT_kivonat.tsv` LEFEDETTSÉGI RÉSE

Mielőtt a találatokat értékelnénk: a `TAHOT_TAGNT_README.md` szerint a kivonat "39 ószövetségi könyv,
21 178 egyedi igehely" — ez **nem a teljes 23 145 verses maszoréta szöveg**. Ellenőrzés közben
konkrét hiányok is megerősítést nyertek:

- **1Móz 32 teljes fejezete hiányzik** a kivonatból (Gen.1–31, 33–50 megvan, 32 nem).
- **Több zsoltár-fejezet hiányzik**, köztük **Zsolt 88, 89, 140, 142** — összesen 88 zsoltárfejezet
  van jelen a 150-ből (62 hiányzik).
- **Jóel 3. fejezete hiányzik** (csak 1–2 van meg).

**Következmény erre a feladatra nézve:** a Rafeusok-tanulmány saját táblázata Zsolt 88:11-et idézi,
a Hádész/Abüsszosz-komplexum tanulmány Zsolt 42:8-at — **ezek egyike sem ellenőrizhető** a jelenlegi
kivonatból, mert a teljes fejezet hiányzik belőle (nem arról van szó, hogy a szó nem szerepel a
versben — a vers maga nincs a kivonatban). Hasonlóan, a "Segítségül hívni" tanulmány Jóel 3:5/2:32
hivatkozása sem ellenőrizhető. Ezeket lent **"NEM ELLENŐRIZHETŐ — KONKORDANCIA-RÉS"**-ként jelölöm,
külön a valódi "ÚJ ELŐFORDULÁS TALÁLVA" kategóriától.

Ez egy önálló, a jelen feladat keretein túlmutató adatminőségi kérdés — **nem a négy tanulmány hibája**,
hanem a `TAHOT_kivonat.tsv` generálásának egy eddig nem dokumentált hiányossága. Javasolt külön nyitott
pontként felvenni a döntési fájlba (l. a changelog-bejegyzést lent).

---

## Összesítő táblázat

| Tanulmány | Kulcs Strong-szám(ok) | Tanulmányban szereplő igehelyek | Teljes egyezés? | Új előfordulás száma | Rokon gyökű jelölt száma | Konkordancia-rés miatt nem ellenőrizhető |
|---|---|---|---|---|---|---|
| **Tehóm** (`Tehom_tematikus.md`) | H8415 | 6 (1Móz 1:2, 7:11, 8:2, 49:25; 2Móz 15:5, 15:8) | ❌ Nem | **24** | **1** | 0 |
| **Segítségül hívni az Úr nevét** (`Segitsegul_hivni_az_Urat_tematikus.md`) | H7121+H8034 (+H3068/H0136), G1941 | 5 táblázatos (1Móz 4:26, 12:8, 13:4, 21:33, 26:25) + ~10 névvel idézett kánoni kitekintés-vers | ❌ Nem (de a kánoni kitekintésben név szerint idézett versek mind megerősítve) | **65 ÓSZ + 29 ÚSZ = 94** (⚠️ lásd módszertani megjegyzés — zajos keresés) | Nem releváns (túl gyakori gyök) | 2 (Jóel 3:5/2:32) |
| **Rafeusok/óriás-népek** (`Rafaim_tematikus.md`) | H7497 (+H7496) | 24 (H7497) + 7 (H7496) = 31 igehely | ❌ Nem | **6** | **3** | 1 (Zsolt 88:11) |
| **Hádész** (+ Tehóm/Abüsszosz/Tartarosz-komplexum, `Tehom_Abusszosz_Hadesz_Tartarosz_tematikus.md`) | H8415, H7585, G0012, G0086, G5020 | ld. a fájl 1. pontjának 17 sora | ❌ Nem (a hádész/seól-ágon jelentős eltérés) | **75** | 1 (H8415-ös, dup. a Tehóm-tanulmánnyal) + görög gyök-adat nem ellenőrizhető | 1 (Zsolt 42:8) |
| **Összesen** | — | — | **0/4 teljes egyezés** | **199** | **5** (+ 1 dup) | **4** |

---

## Módszertani megjegyzés a "94" és "75" számokhoz — miért ilyen magas

A Tehóm- és Rafeusok-tanulmányoknál a kulcsszó **egyetlen, ritka, jól körülhatárolt Strong-szám**
(H8415, H7497) — a grep-találati lista eleve szűk és célzott, pontosan úgy, ahogy a döntési fájl
7.2 pontja leírja ("néhány, legfeljebb egy-két tucat jelölt").

A **"Segítségül hívni" és a "Hádész/Seól"** esetében ez **nem áll**, és ezt explicit jelezni kell:

- **קָרָא בְשֵׁם** nem egyetlen Strong-szám, hanem két, külön-külön **rendkívül gyakori** szó
  (H7121 "hívni", 692 előfordulás; H8034 "név", 788 előfordulás) kombinációja. A jelen ellenőrzés
  a két szó **együttes előfordulását**, Isten nevére (H3068/H0136) szűkítve kereste egy versen belül
  — ez KÖZELÍTŐ módszer, nem azonos a tanulmány saját, szűkebb, tartalmi-idiomatikus szűrésével
  ("az Úr nevét segítségül hívni" mint rögzült formula). A találatok jó része **nyilvánvalóan más
  jelentésű** felszíni egybeesés (pl. Gen 2:19 — Ádám állatokat nevez el; Gen 29:32-35, 30:24 —
  gyermeknevek adása; Jdg 13:24 — Sámson elnevezése; Jer 20:3 — Pashúr átnevezése) — **ezeket a
  módszertan szerint NEM értékeltem tartalmilag**, csak jelöltem, de a felhasználónak érdemes tudnia,
  hogy ez a lista jóval zajosabb, mint a másik három tanulmányé.
- **שְׁאוֹל (seól, H7585)** hasonlóan gyakori (47 előfordulás), és a Hádész-tanulmány maga is csak egy
  **szűk, messiási-tipológiai ívet** követ (Zsolt 16:10 → ApCsel 2:27,31 → Luk 16:23 → Jel 1:18 →
  Jel 20:13-14), nem az összes ószövetségi "seól"-előfordulást. A 46 új jelölt túlnyomó része a szó
  **általános, köznapi ("a sír/halál birodalma") használata** Jóbban, Zsoltárokban, Példabeszédekben,
  Ézsaiásban stb. — ez **nem feltétlenül tartozik** a tanulmány szűken vett tárgyához, de a módszertan
  előírása szerint jelölni kellett.

**Javaslat a következő lépéshez (nem e feladat része, csak jelzés):** mielőtt bármelyik listát emberi
döntésre bocsátanánk, érdemes lenne először eldönteni, hogy a "Segítségül hívni" és "Seól" tanulmányok
tárgya *szándékosan* szűk-e (egy konkrét formula/ív), vagy *bővítendő* teljes lexikai mezővé — ez a
90+ tételes listák hasznosságát alapvetően befolyásolja.

---

## Részletes szakasz — tanulmányonként

### 1. Tehóm (`Tehom_tematikus.md`) — Strong: H8415 (תְּהוֹם)

**Tanulmányban szereplő 6 igehely:** Gen.1.2, Gen.7.11, Gen.8.2, Gen.49.25, Exo.15.5, Exo.15.8

**Teljes körű TAHOT-grep eredménye (30 igehely):** Amo.7.4 · Deu.8.7 · Deu.33.13 · Exo.15.5 · Exo.15.8
· Ezk.26.19 · Ezk.31.4 · Ezk.31.15 · Gen.1.2 · Gen.7.11 · Gen.8.2 · Gen.49.25 · Hab.3.10 · Isa.51.10 ·
Isa.63.13 · Job.28.14 · Job.38.16 · Job.38.30 · Pro.3.20 · Pro.8.24 · Pro.8.27 · Pro.8.28 · Psa.33.7 ·
Psa.71.20 · Psa.78.15 · Psa.104.6 · Psa.106.9 · Psa.107.26 · Psa.135.6 · Psa.148.7

**ÚJ ELŐFORDULÁS TALÁLVA (24):** Amo.7.4 (Ámós 7,4) · Deu.8.7 (5Móz 8,7) · Deu.33.13 (5Móz 33,13) ·
Ezk.26.19 (Ezék 26,19) · Ezk.31.4 (Ezék 31,4) · Ezk.31.15 (Ezék 31,15) · Hab.3.10 (Hab 3,10) ·
Isa.51.10 (Ésa 51,10) · Isa.63.13 (Ésa 63,13) · Job.28.14 (Jób 28,14) · Job.38.16 (Jób 38,16) ·
Job.38.30 (Jób 38,30) · Pro.3.20 (Péld 3,20) · Pro.8.24 (Péld 8,24) · Pro.8.27 (Péld 8,27) ·
Pro.8.28 (Péld 8,28) · Psa.33.7 (Zsolt 33,7) · Psa.71.20 (Zsolt 71,20) · Psa.78.15 (Zsolt 78,15) ·
Psa.104.6 (Zsolt 104,6) · Psa.106.9 (Zsolt 106,9) · Psa.107.26 (Zsolt 107,26) · Psa.135.6 (Zsolt 135,6)
· Psa.148.7 (Zsolt 148,7)

*Megjegyzés:* a tanulmány saját "Konkordancia-megjegyzés"-e (1. pont) már jelezte, hogy a *tehóm*
kb. 27-szer fordul elő az ÓSZ-ban, "elsősorban Zsoltárok, Jób, Ézsaiás, Ezékiel" — ez az általános
becslés (27 ≈ a most talált 30) **összhangban van** a jelen kereséssel, de a tanulmány **egyenként
nem katalogizálta és nem értékelte** ezeket a verseket — ezért formálisan "ÚJ ELŐFORDULÁS TALÁLVA".

**ROKON GYÖKŰ JELÖLT (1):** **H4103 מְהוּמָה** (*mehumáh*, "zűrzavar, pánik") — ugyanabból a H1949
gyökből (a "zúgó hang" jelentésmezőből), mint H8415. Tematikus kapcsolódás gyenge/közvetett (a
"zajos, rendezetlen" alapjelentés köti össze a "mélység" és a "zűrzavar" szót), emberi mérlegelésre
érdemes, de nem erős jelölt.

---

### 2. Segítségül hívni az Úr nevét (`Segitsegul_hivni_az_Urat_tematikus.md`) — Strong: H7121+H8034 (ÓSZ), G1941 (ÚSZ)

**Tanulmányban szereplő igehelyek:**
- Táblázatos (5): Gen.4.26, Gen.12.8, Gen.13.4, Gen.21.33, Gen.26.25
- Kánoni kitekintésben név szerint idézve (nem táblázatban, de a szövegben tárgyalva): 1Ki.18.24-26,
  2Ki.5.11, Psa.116.4, Psa.116.13, Psa.116.17, Zep.3.9, Zec.13.9, Jóel 3:5/2:32 (nem ellenőrizhető),
  Act.2.21, Rom.10.13

**Megerősítés:** a fenti, szövegben név szerint idézett ÓSZ-i/ÚSZ-i versek **mindegyike megjelenik**
a H7121+H8034(+H3068/H0136) ill. G1941 grep-találati listában (kivéve Jóel — konkordancia-rés) —
ez validálja a tanulmány saját kitekintését.

**NEM ELLENŐRIZHETŐ — KONKORDANCIA-RÉS (2):** Jóel 3:5 (MT) / 2:32 — a TAHOT-kivonatból Jóel 3.
fejezete teljesen hiányzik.

**ÚJ ELŐFORDULÁS TALÁLVA — ÓSZ, H7121+H8034+H3068/H0136 együttes előfordulása (65, ⚠️ zajos, ld. fenti
módszertani megjegyzés):**
1Ch.13.6 (1Krón 13,6) · 1Ch.16.8 (1Krón 16,8) · 1Ki.13.2 (1Kir 13,2) · 1Sa.1.20 (1Sám 1,20) ·
1Sa.7.12 (1Sám 7,12) · 2Ch.20.26 (2Krón 20,26) · 2Sa.5.20 (2Sám 5,20) · 2Sa.6.2 (2Sám 6,2) ·
2Sa.12.24 (2Sám 12,24) · 2Sa.12.25 (2Sám 12,25) · Amo.5.8 (Ámós 5,8) · Amo.9.6 (Ámós 9,6) ·
Amo.9.12 (Ámós 9,12) · Dan.9.19 (Dán 9,19) · Deu.28.10 (5Móz 28,10) · Deu.32.3 (5Móz 32,3) ·
Exo.17.7 (2Móz 17,7) · Exo.17.15 (2Móz 17,15) · Exo.33.19 (2Móz 33,19) · Exo.34.5 (2Móz 34,5) ·
Exo.35.30 (2Móz 35,30) · Gen.2.19 (1Móz 2,19) · Gen.5.29 (1Móz 5,29) · Gen.11.9 (1Móz 11,9) ·
Gen.16.11 (1Móz 16,11) · Gen.16.13 (1Móz 16,13) · Gen.22.14 (1Móz 22,14) · Gen.29.32 (1Móz 29,32) ·
Gen.29.33 (1Móz 29,33) · Gen.29.35 (1Móz 29,35) · Gen.30.24 (1Móz 30,24) · Hos.1.4 (Hós 1,4) ·
Isa.7.14 (Ésa 7,14) · Isa.8.3 (Ésa 8,3) · Isa.12.4 (Ésa 12,4) · Isa.43.1 (Ésa 43,1) ·
Isa.44.5 (Ésa 44,5) · Isa.45.3 (Ésa 45,3) · Isa.48.1 (Ésa 48,1) · Isa.48.2 (Ésa 48,2) ·
Isa.49.1 (Ésa 49,1) · Isa.54.5 (Ésa 54,5) · Isa.62.2 (Ésa 62,2) · Isa.65.15 (Ésa 65,15) ·
Jdg.2.5 (Bír 2,5) · Jdg.13.24 (Bír 13,24) · Jer.3.17 (Jer 3,17) · Jer.7.11 (Jer 7,11) ·
Jer.7.30 (Jer 7,30) · Jer.11.16 (Jer 11,16) · Jer.14.9 (Jer 14,9) · Jer.15.16 (Jer 15,16) ·
Jer.20.3 (Jer 20,3) · Jer.23.6 (Jer 23,6) · Jer.25.29 (Jer 25,29) · Jer.44.26 (Jer 44,26) ·
Jos.5.9 (Józs 5,9) · Jos.7.26 (Józs 7,26) · Lam.3.55 (JSir 3,55) · Mic.6.9 (Mik 6,9) ·
Num.11.3 (4Móz 11,3) · Num.21.3 (4Móz 21,3) · Psa.99.6 (Zsolt 99,6) · Psa.105.1 (Zsolt 105,1) ·
Rut.4.11 (Ruth 4,11) · Rut.4.14 (Ruth 4,14)

**ÚJ ELŐFORDULÁS TALÁLVA — ÚSZ, G1941 (29, ⚠️ szintén zajos — a görög ige "nevet adni/nevezni" és
"[Caesarhoz] fellebbezni" jelentésben is előfordul, nem csak "segítségül hívni" értelemben):**
1Co.1.2 (1Kor 1,2) · 1Pe.1.17 (1Pét 1,17) · 2Co.1.23 (2Kor 1,23) · 2Ti.2.22 (2Tim 2,22) ·
Act.1.23 (Csel 1,23) · Act.4.36 (Csel 4,36) · Act.7.59 (Csel 7,59) · Act.9.14 (Csel 9,14) ·
Act.9.21 (Csel 9,21) · Act.10.5 (Csel 10,5) · Act.10.18 (Csel 10,18) · Act.10.32 (Csel 10,32) ·
Act.11.13 (Csel 11,13) · Act.12.12 (Csel 12,12) · Act.12.25 (Csel 12,25) · Act.15.17 (Csel 15,17) ·
Act.22.16 (Csel 22,16) · Act.25.11 (Csel 25,11) · Act.25.12 (Csel 25,12) · Act.25.21 (Csel 25,21) ·
Act.25.25 (Csel 25,25) · Act.26.32 (Csel 26,32) · Act.28.19 (Csel 28,19) · Heb.11.16 (Zsid 11,16) ·
Jas.2.7 (Jak 2,7) · Mat.10.3 (Máté 10,3) · Mat.10.25 (Máté 10,25) · Rom.10.12 (Róm 10,12) ·
Rom.10.14 (Róm 10,14)

**ROKON GYÖKŰ JELÖLT:** nem releváns — H7121 és H8034 mindkettő túl gyakori/produktív gyök ahhoz,
hogy a `Strong_szotar.tsv` "rokon gyök" mezője érdemi, szűkített jelöltlistát adjon.

---

### 3. Rafeusok/óriás-népek (`Rafaim_tematikus.md`) — Strong: H7497 (רְפָאִים, "Rephaim/Rapha" névként), H7496 (רְפָאִים, "árnyak" költői értelemben)

**Tanulmányban szereplő igehelyek (a táblázat sorai szerint, tartományokkal):** Gen.14.5, Gen.15.20,
Deu.2.10-11, Deu.2.20-21, Deu.3.11, Deu.3.13, Jos.12.4, Jos.13.12, 2Sa.21.15-22, 1Ch.20.4-8,
Job.26.5, Psa.88.11 (⚠️ nem ellenőrizhető), Pro.2.18, Pro.9.18, Pro.21.16, Isa.14.9, Isa.26.14,
Isa.26.19 (+ Gen.6.4 és Num.13.33 — más lexéma, nefilim/gibborim, nem H7497/H7496)

**Teljes körű TAHOT-grep — H7497 (24 igehely):** 1Ch.11.15 · 1Ch.14.9 · 1Ch.20.4 · 1Ch.20.6 ·
1Ch.20.8 · 2Sa.5.18 · 2Sa.5.22 · 2Sa.21.16 · 2Sa.21.18 · 2Sa.21.20 · 2Sa.21.22 · 2Sa.23.13 ·
Deu.2.11 · Deu.2.20 · Deu.3.11 · Deu.3.13 · Gen.14.5 · Gen.15.20 · Isa.17.5 · Jos.12.4 · Jos.13.12
· Jos.15.8 · Jos.17.15 · Jos.18.16

**Teljes körű TAHOT-grep — H7496 (7 igehely):** Isa.14.9 · Isa.26.14 · Isa.26.19 · Job.26.5 ·
Pro.2.18 · Pro.9.18 · Pro.21.16 — **ez a 7 pontosan egyezik** a tanulmány táblázatával (TELJES
EGYEZÉS a H7496-os/költői ágon).

**ÚJ ELŐFORDULÁS TALÁLVA (6, mind a H7497-es "Refáim-völgy" földrajzi kifejezésből, amit a tanulmány
nem tárgyal):**
- **2Sám 5:18** — "a Refáim völgyében" (filiszteus csata Dávid ellen)
- **2Sám 5:22** — ugyanaz a helyszín, második ütközet
- **2Sám 23:13** — Dávid három vitézének éve, "a Refáim völgyében" táborozó filiszteusok
- **1Krón 11:15** — a 2Sám 23:13 párhuzamos helye
- **1Krón 14:9** — a 2Sám 5:18/22 párhuzamos helye
- **Ézsaiás 17:5** — aratási hasonlat, "mint mikor ki a Refáim völgyében kalászt szed"

*Megjegyzés:* ezek mind ugyanazt a H7497 Strong-számot viselik, mint a tanulmányban már tárgyalt
"Refáim mint népnév" előfordulások, de egy **más funkcióban** — helynévi jelzőként ("Refáim-völgy"),
nem népnévként vagy "óriás" jelentésben. A tanulmány 2. pontja explicit tárgyalja a szó két
jelentésmezőjét (prózai "nép" vs. költői "árnyak") — ez a hatodik, helynévi használat egy **harmadik,
eddig nem tárgyalt kategória**, tartalmi értékelésre váró jelölt.

**NEM ELLENŐRIZHETŐ — KONKORDANCIA-RÉS (1):** Zsolt 88:11 — a Zsolt 88 fejezet teljesen hiányzik a
`TAHOT_kivonat.tsv`-ből.

**ROKON GYÖKŰ JELÖLT (3):** mindhárom a H7495 (רָפָא, "gyógyítani") közös gyökből, amelyből maga a
H7496/H7497 is származik (a `Strong_szotar.tsv` szerint):
- **H8655 תְּרָפִים** (*teráfim*, "házi bálványok/terafim") — **erős tartalmi jelölt**: a tanulmány
  2. pontja maga hivatkozik az ugariti *rāpi'ūma* kutatásra (félig-isteni, tisztelt halott-ősök),
  és a teráfim-kultusz a szakirodalomban (pl. hettita/ugariti ősök-tisztelet kontextusában)
  gyakran éppen ezzel a *rāpi'ūma*-hagyománnyal hozható összefüggésbe — érdemes emberi mérlegelésre.
- **H7504 רָפֶה** ("gyenge, erőtlen") és **H7510 רִפְיוֹן** ("erőtlenség") — gyengébb, de tematikusan
  releváns jelölt: a tanulmány Remez-pontja kifejezetten az "erőtlen árnyak" motívumot elemzi
  (Zsolt 88:11 kontextusában), és ez a két szó ugyanabból a "elernyedni/gyengülni" jelentésmezőből
  (H7503) származik, mint a H7496 "árnyak" jelentés maga.

---

### 4. Hádész (+ Tehóm/Abüsszosz/Tartarosz-komplexum, `Tehom_Abusszosz_Hadesz_Tartarosz_tematikus.md`)

Ez a tanulmány formálisan a naplóban két külön index-tételt fed le (#2 Tehóm-Abüsszosz-Hádész-
Tartarosz kibővített komplexum; #3 Hádész/seól önálló motívumként) — mindkettő ugyanabban a
fájlban. A jelen ellenőrzés a fájl teljes 1. pontjának mind az öt lexikai ágát átfésülte.

#### 4a. תְּהוֹם (tehóm), H8415 — a fájl saját ágán

**Táblázatban:** Gen.1.2, Gen.7.11, Gen.8.2, Psa.42.8 (⚠️ nem ellenőrizhető), Job.38.16

**Eredmény:** a teljes H8415-lista (l. fent, 30 igehely) mind a 4 ellenőrizhető táblázati tételt
tartalmazza (Gen.1.2, Gen.7.11, Gen.8.2, Job.38.16 ✅) — a fennmaradó **25 verzió "ÚJ ELŐFORDULÁS
TALÁLVA"**, ugyanaz a 24-es lista, mint a #1 Tehóm-tanulmánynál, **plusz** Gen.49.25 és Exo.15.5/15.8
(amelyeket EZ a tanulmány nem tárgyal, csak a különálló `Tehom_tematikus.md`).

**NEM ELLENŐRIZHETŐ — KONKORDANCIA-RÉS (1):** Zsolt 42:8 — a Zsolt 42 fejezet teljesen hiányzik a
`TAHOT_kivonat.tsv`-ből.

#### 4b. ἄβυσσος (abüsszosz), G0012 — TELJES EGYEZÉS

**Táblázatban (9):** Luk.8.31, Rom.10.7, Rev.9.1, Rev.9.2, Rev.9.11, Rev.11.7, Rev.17.8, Rev.20.1,
Rev.20.3

**Teljes körű TAGNT-grep (9):** ugyanez a 9 igehely, egy az egyben. **✅ TELJES EGYEZÉS**, nincs
teendő.

#### 4c. שְׁאוֹל/ᾍδης (seól/hádész), H7585 (ÓSZ) + G0086 (ÚSZ)

**Táblázatban — a hádész-ág:** Psa.16.10 → Act.2.27, Act.2.31 → Luk.16.23 → Rev.1.18 → Rev.20.13,
Rev.20.14 (a formálisan idézett ÓSZ-i alapige csak Psa.16.10)

**Teljes körű TAHOT-grep, H7585 (47 igehely):** 1Ki.2.6 · 1Ki.2.9 · 1Sa.2.6 · 2Sa.22.6 · Amo.9.2 ·
Deu.32.22 · Ecc.9.10 · Ezk.31.15 · Ezk.31.16 · Ezk.31.17 · Ezk.32.21 · Ezk.32.27 · Gen.37.35 ·
Gen.42.38 · Gen.44.29 · Gen.44.31 · Hab.2.5 · Hos.13.14 · Isa.5.14 · Isa.7.11 · Isa.14.9 · Isa.14.11
· Isa.14.15 · Isa.28.15 · Isa.28.18 · Isa.38.10 · Isa.38.18 · Isa.57.9 · Job.7.9 · Job.11.8 ·
Job.14.13 · Job.17.13 · Job.17.16 · Job.21.13 · Job.24.19 · Job.26.6 · Num.16.30 · Num.16.33 ·
Pro.1.12 · Pro.5.5 · Pro.7.27 · Pro.9.18 · Pro.15.11 · Pro.15.24 · Pro.23.14 · Pro.27.20 ·
Pro.30.16 · Psa.16.10 · Psa.86.13 · Psa.116.3 · Psa.139.8 · Psa.141.7 · Sng.8.6

**ÚJ ELŐFORDULÁS TALÁLVA — H7585 (46, ⚠️ ld. a fenti módszertani megjegyzést — a tanulmány szándékosan
csak egy szűk messiási-tipológiai ívet követ, nem a teljes lexikai mezőt):** 1Ki.2.6 (1Kir 2,6) ·
1Ki.2.9 (1Kir 2,9) · 1Sa.2.6 (1Sám 2,6) · 2Sa.22.6 (2Sám 22,6) · Amo.9.2 (Ámós 9,2) ·
Deu.32.22 (5Móz 32,22) · Ecc.9.10 (Préd 9,10) · Ezk.31.15 (Ezék 31,15) · Ezk.31.16 (Ezék 31,16) ·
Ezk.31.17 (Ezék 31,17) · Ezk.32.21 (Ezék 32,21) · Ezk.32.27 (Ezék 32,27) · Gen.37.35 (1Móz 37,35) ·
Gen.42.38 (1Móz 42,38) · Gen.44.29 (1Móz 44,29) · Gen.44.31 (1Móz 44,31) · Hab.2.5 (Hab 2,5) ·
Hos.13.14 (Hós 13,14, kétszer) · Isa.5.14 (Ésa 5,14) · Isa.7.11 (Ésa 7,11) · Isa.14.9 (Ésa 14,9) ·
Isa.14.11 (Ésa 14,11) · Isa.14.15 (Ésa 14,15) · Isa.28.15 (Ésa 28,15) · Isa.28.18 (Ésa 28,18) ·
Isa.38.10 (Ésa 38,10) · Isa.38.18 (Ésa 38,18) · Isa.57.9 (Ésa 57,9) · Job.7.9 (Jób 7,9) ·
Job.11.8 (Jób 11,8) · Job.14.13 (Jób 14,13) · Job.17.13 (Jób 17,13) · Job.17.16 (Jób 17,16) ·
Job.21.13 (Jób 21,13) · Job.24.19 (Jób 24,19) · Job.26.6 (Jób 26,6) · Num.16.30 (4Móz 16,30) ·
Num.16.33 (4Móz 16,33) · Pro.1.12 (Péld 1,12) · Pro.5.5 (Péld 5,5) · Pro.7.27 (Péld 7,27) ·
Pro.9.18 (Péld 9,18) · Pro.15.11 (Péld 15,11) · Pro.15.24 (Péld 15,24) · Pro.23.14 (Péld 23,14) ·
Pro.27.20 (Péld 27,20) · Pro.30.16 (Péld 30,16) · Psa.86.13 (Zsolt 86,13) · Psa.116.3 (Zsolt 116,3) ·
Psa.139.8 (Zsolt 139,8) · Psa.141.7 (Zsolt 141,7) · Sng.8.6 (Én 8,6)

**Teljes körű TAGNT-grep, G0086 (10 igehely):** Act.2.27 · Act.2.31 · Luk.10.15 · Luk.16.23 ·
Mat.11.23 · Mat.16.18 · Rev.1.18 · Rev.6.8 · Rev.20.13 · Rev.20.14

**ÚJ ELŐFORDULÁS TALÁLVA — G0086 (4):** Luk.10.15 (Luk 10,15 — "te, Kapernaum... a hádészig
taszíttatol") · Mat.11.23 (Máté 11,23, párhuzamos hely) · Mat.16.18 (Máté 16,18 — "a hádész kapui
sem vesznek diadalmat rajta") · Rev.6.8 (Jel 6,8 — a sápadt ló lovasát "a hádész" követi)

#### 4d. ταρταρόω (tartaroó), G5020 — TELJES EGYEZÉS

**Táblázatban:** 2Pe.2.4 (egyetlen ÚSZ-i előfordulás)

**Teljes körű TAGNT-grep:** ugyanez az 1 igehely. **✅ TELJES EGYEZÉS**, nincs teendő.

#### Rokon gyökű jelölt — a komplexum egészére

- **H4103 מְהוּמָה** — ugyanaz, mint a #1 Tehóm-tanulmánynál (dublikált jelölt, azonos H8415-ös gyök).
- **Görög oldal (abüsszosz, hádész, tartarosz):** a `Strong_szotar.tsv` ezekre a görög szócikkekre
  "nem önálló Strong-számos szócikk" jelöléssel csak a görög összetételi elemeket adja meg
  (pl. ἄβυσσος = α + βυθος), **valódi gyök/rokonsági adatot nem tartalmaz** — a görög oldali
  "rokon gyökű" ellenőrzés a jelenlegi `Strong_szotar.tsv` struktúrával **nem végezhető el**
  érdemben. Ez maga is egy dokumentálandó korlát (a görög rész a szótár jövőbeli bővítésénél
  érdemes lehet mélyebb gyök-adatot kapni, ha valaha releváns lesz).
- **שְׁאוֹל (seól) gyöke, H7592** ("kérdezni") — a `Strong_szotar.tsv` szerinti származékai (Eshtaol,
  Mishal, Sheal stb.) mind név-/kérés-jelentésűek, **nincs köztük tematikusan releváns, halál/alvilág
  jelentésű rokon** — explicit ellenőrizve, nincs jelölt.

---

## SzPA-lefedettség (4. szakasz, felfüggesztett állapot — csak jelzés)

Mind a négy tanulmány igehelyei kizárólag olyan könyveket érintenek (1Móz, 2Móz, 4Móz, 5Móz, Józs,
Bír, Ruth, 1-2Sám, 1-2Kir, 1-2Krón, Jób, Zsolt, **Péld**, Ézs, Jer, JSir, Ezék, Hós, Ámós, Mik, Sof,
Zak, Dán — és ÚSZ-ben Mát, Luk, Ján, **ApCsel**, Róm, 1-2Kor, 2Tim, Zsid, Jak, 1-2Pét, Jel), amelyek
közül a privát SzPA-adatbázis jelenleg csak **Példabeszédek 1:1-9** és **ApCsel 1:1-4** mintaterjedelmet
fedi le. A jelen ellenőrzés talált Péld-beli (pl. Pro.1.12, Pro.3.20, Pro.5.5 stb.) és ApCsel-beli
(Act.2.21, Act.2.27, Act.2.31 stb.) új jelölteket is, de ezek **egyike sem esik az SzPA-minta jelenlegi
1-9/1-4 verses tartományába** — nincs tényleges SzPA-lefedettség egyik találatnál sem. Az
SzPA-integráció felfüggesztett állapota miatt ennél tovább nem megyek (l. döntési fájl 8. szakasz,
első nyitott pont).

---

## Összefoglalás

- **4 tanulmány ellenőrizve**, mind a négyet a teljes TAHOT/TAGNT-en átfuttatva a saját kulcs
  Strong-számára/számaira.
- **0/4 "TELJES EGYEZÉS"** a tanulmány szintjén (de két önálló lexikai ágon — abüsszosz G0012 és
  tartarosz G5020 — igen: 9/9 és 1/1 pontos egyezés).
- **199 "ÚJ ELŐFORDULÁS TALÁLVA"** összesen (24 Tehóm + 94 Segítségül hívni [65 ÓSZ+29 ÚSZ, ⚠️ zajos
  módszer] + 6 Rafeusok + 75 Hádész-komplexum [25 tehóm-dup + 46 seól + 4 hádész]) — emberi döntésre
  várva, tartalmi értékelés nélkül.
- **5 egyedi "ROKON GYÖKŰ JELÖLT"** (+ 1 duplikált): H4103 (mehumáh, Tehóm-gyök, 2×) · H8655
  (teráfim, erős jelölt) · H7504 + H7510 (gyenge/erőtlenség, Rafeusok-gyök).
- **4 tétel "NEM ELLENŐRIZHETŐ — KONKORDANCIA-RÉS" miatt**: Zsolt 88:11, Zsolt 42:8, Jóel 3:5/2:32
  (kétszer hivatkozva) — mindegyik azért, mert a `TAHOT_kivonat.tsv`-ből a teljes fejezet hiányzik.
- **⚠️ Új, e feladat során felfedezett adatminőségi kérdés**: a `TAHOT_kivonat.tsv` a
  `TAHOT_TAGNT_README.md` saját állítása szerint "39 könyv, teljes ÓSZ", de ténylegesen legalább
  1Móz 32, Zsolt 88/89/140/142 és Jóel 3 fejezetek hiányoznak belőle (150-ből 88 zsoltárfejezet van
  jelen) — ez minden jövőbeli "teljes körű grep" alapú ellenőrzés megbízhatóságát érinti, nem csak
  a jelen négy tanulmányét.
