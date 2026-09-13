# Átadási dokumentum — 2026.09.10–11. munkamenet

**Projekt:** PaRDeS bibliai motívum-kutatás (`basesoft777/Bible-Study`)
**Készült:** 2026.09.11
**Előző átadás:** `Atadasi_dokumentum_2026_09_10.md`

---

## 1. Áttekintés — mi történt ebben a munkamenetben

Két, egymástól jól elkülönülő szakasz:

**A) Retroaktív checklist- és sablon-megfelelőségi kör** (2026.09.10)
Hat, korábban lezárt tematikus study átvizsgálása és hozzáigazítása a
`4_PaRDeS_tematikus_sablon.md` v14-es előírásaihoz, plusz két valódi
lexikai kutatás és egy fájl-összevonás.

**B) Modell-összehasonlító teszt** (2026.09.11)
Egy új, még feldolgozatlan motívum ("bűn következményeinek gyűrűzése",
`[ID: HAMART-001]`) párhuzamos feldolgozása Sonnet 5 és Opus 5
modellel, azonos prompttal, külön branch-eken.

---

## 2. Lezárt szálak — `main`-en

Mind a következők **mergelve vannak a `main`-be**, független
`codeload`-ellenőrzéssel validálva:

### 2.1 Melkizedek (`[ID: KIRALY-001]`)
- Motívumnapló mind a négy szekciója frissítve (Tematikus áttekintés,
  Kulcsszó-index, Kulcsszavak részletesen, Könyv szerinti index).
- Index fájl #8 sora frissítve; changelog v53.
- `1Moz_14_bovitett.md`-be 📎-visszahivatkozás pótolva.
- STEPBible-sor kiegészítve (G0934, G2406).
- **A study saját, belső "Lezárási checklist"-je** (12 pont) frissítve
  — korábban elavultan `[ ]` állapotban állt, holott minden elkészült.

### 2.2 Segítségül hívni az Úr nevét (`[ID: ISTENTISZT-001]`)
- Zak 13:9 táblázatosítva, hat új ÚSZ-igehely (1Kor 1:2, 2Tim 2:22,
  1Pét 1:17, ApCsel 9:14, 9:21, 22:16), D-minta explicit kizárva.
- Motívumnapló + index frissítve; changelog v54.

### 2.3 Rafaim (`[ID: HODIT-001]`) és Isten fiai/Nefilim/Gibborim (`[ID: MENNY-001]`)
- v14-compliance: "0. Forrás-összegyűjtés", Minőségi kapu (Q1-Q6).
- Kölcsönös, explicit elhatárolás mindkét fájl saját szövegében.
- 📎-visszahivatkozások pótolva (`1Moz_14_bovitett.md`,
  `1Moz_6v1-8_bovitett.md`).
- **Valódi lexikai kutatás** (helyi `TAHOT_kivonat.tsv`): 3 új
  H7497-igehely (Józs 15:8, 17:15, 18:16), H7496/H7497 Strong-szám
  szerinti megoszlás tisztázva.
- **Igehely-hiba javítva mindenhol:** 4Móz 13:33 → **13:34** (a
  נְפִלִים szó ténylegesen a 34. versben áll) — 2 körben, mert az első
  javítás 2 előfordulást kihagyott.

### 2.4 Tehóm/Abüsszosz (`[ID: TEREMT-001]`) és Hádész/Seól (`[ID: ALVIL-001]`)
- **Hádész/seól kiszervezve önálló fájlba** (`Hadesz_Seol_tematikus.md`)
  — a napló mindig is külön ID-ként tartotta nyilván, csak praktikus
  okból élt közös fájlban.
- **Tehóm-komplexum összevonva:** a
  `Tehom_Abusszosz_Hadesz_Tartarosz_tematikus.md` **törölve**,
  tartalma a `Tehom_tematikus.md`-be olvasztva (a görög ábüσσος-anyagnak
  sosem volt önálló ID-ja).
- **Valódi lexikai kutatás:** H8415 teljes ÓSZ-scan (35 előfordulás,
  3 új: Zsolt 36:7, 77:17, Jón 2:6); G0012 teljes ÚSZ-scan (9, nincs új);
  H7585 teljes ÓSZ-scan (64 egyedi vers, 63 új); G0086 teljes ÚSZ-scan
  (10, nincs új — Strong-szám javítva G86 → G0086).
- **Kiemelt lelet:** Hós 13:14 → Pál 1Kor 15:55-ben idézi/parafrazálja.
- Changelog v55; index és napló szinkronban.

---

## 3. Nyitott szálak — ELDÖNTETLEN, döntést igényel

### 3.1 ⚠️ Két branch, ugyanarra a motívumra — melyik menjen `main`-be?

A "bűn következményeinek gyűrűzése" (`[ID: HAMART-001]`) motívumról
**két teljes feldolgozás létezik**, egyik sincs mergelve:

| | `bun-gyuruzese-20260911-sonnet` | `bun-gyuruzese-20260911-opus` |
|---|---|---|
| Hatókör | a napló szerinti 4 szakasz | lexikai gerincre bontva, kánoni ívvé kiterjesztve |
| Táblázat-sorok | 4 | ~46 (20 genezisi + 18 ÓSZ-kánoni + 8 ÚSZ) |
| Scan-hatókör | ⚠️ **Gen 1-11-re szűkítve** ("teljes"-nek címkézve) | teljes ÓSZ + teljes ÚSZ |
| Használt datasetek | 3 | 7 |
| Kutatási technikák | szemmel olvasott gerinc-azonosítás | halmazmetszet, kollokáció-keresés, LXX-híd |
| 5:29 / 8:21 / 9:25 / 12:3 | elutasítva / nyitva hagyva (a napló utasítására) | beépítve (lexikai bizonyíték alapján) |
| Named teacher | ✅ Derek Prince, valódi `web_search`-csel | ❌ explicit gap, eljárási indoklással |

**Chat-Claude javaslata volt** (nem elfogadva, nem végrehajtva):
az Opus-verzió a merge-alap, két kiegészítéssel — (a) a TSK-szavazatszám
javítása, (b) a Sonnet named-teacher szakaszának átemelése.

**Eldöntetlen:** melyik menjen, kell-e ötvözés, kell-e a Sonnet-ágat
megtartani összehasonlítási referenciának.

### 3.2 ⚠️ Futásban lévő, még nem ellenőrzött Code-prompt

`Code_prompt_B_tablazat_BDB_javitas_magyaritas_2026_09_11.md` —
a B) táblázat 7 hibás BDB-cellájának javítása (idézet-töredék helyett
valódi szócikk-szöveg), 17 sor magyarítása, Ézs 24:5-6 cella pótlása.
**Állapot:** átadva a Code-nak, a push/ellenőrzés még nem történt meg.

### 3.3 ⚠️ Károli-KH jelölt, felhasználói döntésre vár

`1Móz 6:2` → **Máté 24:38 / Lukács 17:27** (Károli-kereszthivatkozás).
Tartalmilag nem az "Isten fiai kiléte" kérdéshez tartozik, hanem az
"úgy lesz, mint Noé napjaiban" eszkatológiai-ítéleti analógiához.
**Eldöntetlen:** (a) jegyzetként bekerüljön-e valamelyik study-ba,
(b) önálló motívumként érdemes-e feldolgozni, (c) maradjon-e figyelmen
kívül. A `Isten_fiai_Nefilim_Gibborim_kereszthivatkozas_naplo.md`
rögzíti mint nyitott tételt.

### 3.4 ⚠️ Rafaim — 12 alacsony szavazatú TSK-jelölt, nem minősítve

5Móz 1:4, 3:20, 3:22, 2:23; Józs 13:19, 13:31; Jer 48:1, 48:23;
Zsolt 105:23, 105:27, 106:22, 78:51; 1Krón 4:40 — mind Óg/Básán,
ill. "Khám földje" tematikus szomszédság, **nem** H7497-előfordulás.
Egyedi minősítést igényelnének. A `Rafaim_kereszthivatkozas_naplo.md`
rögzíti őket.

### 3.5 ⚠️ Tehóm vs. Tehóm-kiterjesztés — tartalmi duplikáció (most már tárgytalan?)

A korábbi két fájl ugyanazt a három igehelyet (1Móz 1:2, 7:11, 8:2)
egymástól függetlenül, külön PaRDeS-kifejtéssel dolgozta fel. Az
összevonással ez megszűnt, **de**: a projekt más helyein (pl.
Melkizedek mélyelemzés + tematikus páros) ugyanez a tudatos
duplikáció-minta él ("minden study önmagában is olvasható legyen").
**Eldöntetlen:** marad-e ez általános elvként, vagy máshol is
érdemes-e összevonni.

### 3.6 ⚠️ Isten fiai — "shem, név szerzése mint lázadás" (6:4 ↔ 11:4)

A study 6. pontja explicit nyitva hagyja: felvétele a naplóba mint új,
előre jelzett motívum **külön jóváhagyást igényel**. Változatlanul
nyitva.

### 3.7 ⚠️ Segítségül hívni — két, régebbi nyitott tétel

(a) A `Karoli_Strong_kivonat.tsv` join-tábla bővítése.
(b) A NAPLO-jelölés egységesítése a study meglévő szövegtörzsében.
Egyik sem érintve ebben a munkamenetben; a study szövege továbbra is
"még nem történt meg"-ként jelöli — ez **igaz állítás**, ellenőrizve.

### 3.8 ⚠️ Sense-szám mező nem-numerikus értékei — indoklás nélkül

Több táblázat-sorban a "Sense-szám" oszlopban nem szám áll, hanem
igealak-jelölés ("Qal pass. ptc.", "Nif'ál", "Pi'él") — mert a BDB az
igegyököket binyan szerint tagolja, nem számozott sense-ekkel. Ez
ésszerű adaptáció, de **eltér a sablon literál példájától ("1") és
nincs sehol indokolva**. Eldöntetlen: kell-e módszertani jegyzet
a sablonba vagy a study-kba.

### 3.9 ⚠️ Modellhasználati stratégia

Felmerült (nem eldöntve) az Opus/Sonnet megosztás rögzítése:
- **Opus** — tervező/kutató szerep (új study nulláról, mélyelemzés,
  lexikai feltárás, sablon-értelmezés, önaudit).
- **Sonnet** — végrehajtó szerep (Code-promptok futtatása,
  string-cserék, commit/push, mechanikus validáció).
Aktuális árazás (2026.09): Opus 5 = $5/$25, Sonnet 5 = $3/$15,
Haiku 4.5 = $1/$5 (input/output, millió token). **Eldöntetlen**, hogy
ez rögzüljön-e munkamódszerként.

### 3.10 ⚠️ Szerzői jogi státusz

Felmerült, nem lezárt kérdés. Rögzített tények: az Anthropic ToS
átruházza a kimenetre vonatkozó jogait a felhasználóra ("all our
right, title, and interest, **if any**"), de ez nem dönti el, hogy a
mű szerzői jogi védelem alatt áll-e harmadik féllel szemben.
EU/magyar jogban az emberi szellemi alkotás követelménye miatt az
AI-közreműködéssel készült művek státusza aktívan fejlődő terület.
A forrásanyagok (BDB, bibliai szöveg, TSK) közkincsek.
**Ha publikálás/kereskedelmi felhasználás merül fel: szakjogászi
konzultáció indokolt.**

---

## 4. Módszertani tanulságok — rögzítve a `method-learnings.md`-ben

Három új szabály került be ebben a munkamenetben, mind valós
incidens nyomán:

1. **Memória vs. lekérdezés.** Minden állítás két kategória egyikébe
   tartozik, és a szövegnek meg kell mondania, melyikbe: (a)
   adatbázis-tény (előfordulás-szám, Strong-kód, kereszthivatkozás-lista)
   — **kizárólag** az adott munkamenetben ténylegesen lefuttatott
   lekérdezésből; (b) értelmezés/szakirodalmi ismeret — jöhet
   memóriából, de jelölni kell. *Incidens: egy "🔍 STEPBible-ellenőrizve"
   sor bekerült a study-ba anélkül, hogy a lekérdezés valaha lefutott
   volna.*

2. **Sablon vs. precedens.** Egy meglévő fájl szerkezeti mintájának
   átvétele **nem** bizonyítja a sablon-megfelelőséget — mindig a
   sablon élő szövegét kell ellenőrizni. *Incidens: prózai
   csoportosítás került két fájlba, egy régebbi, nem-compliant fájl
   mintájára, holott a sablon explicit "MINDEN találat a táblázatba"
   szabályt ír elő.*

3. **Kötelező kereszthivatkozás-napló.** Minden valódi, teljes körű
   keresés után kötelező a `naplok/[motívum]_kereszthivatkozas_naplo.md`
   fájl, **minden** jelölt minősítésével (a bekerülteket és az
   elutasítottakat/nyitva hagyottakat is). *Incidens: négy valódi
   keresés futott, egyikhez sem készült napló — az elutasított
   jelöltek csak a chat-történetben léteztek.*

**Negyedik, felmerült de nem rögzített tanulság:** ha egy friss
lexikai lekérdezés ellentmond a motívumnapló korábbi besorolási
döntésének, azt **kötelező felvetni** — nem szabad némán követni a
naplót. (Ez az Opus/Sonnet különbség egyik gyökere volt az 5:29-nél.)
**Eldöntetlen:** bekerüljön-e a `method-learnings.md`-be.

---

## 5. Sablon-változás

**`4_PaRDeS_tematikus_sablon.md` v15 (2026.09.11):** a táblázat
"Jelentés-szöveg" oszlopa mostantól az angol BDB-szöveg **mellett
magyar fordítást is** tartalmaz, `"angol" — magyarul: "fordítás"`
formátumban. A korábbi elv (csak angol a táblázatban, magyarítás a
prózában) hatályát vesztette. Visszamenőleg nem kötelező a lezárt
study-kat frissíteni, de szerkesztés alatt állónál igen.

---

## 6. Javasolt következő lépések

1. **Dönteni a 3.1-ről** (melyik HAMART-001 branch) — ez blokkolja a
   motívum lezárását.
2. **Ellenőrizni a 3.2-t** (futásban lévő B) táblázat-javítás).
3. Eldönteni, hogy a 3.3-3.8 nyitott tételek közül melyik érdemel
   önálló munkamenetet.
4. Ha a 3.9 (modellhasználati megosztás) rögzül, érdemes a
   `method-learnings.md`-be vagy egy külön workflow-dokumentumba írni.

---

*Az ebben a dokumentumban szereplő minden állítás vagy friss
`codeload`-ellenőrzésből, vagy a helyi konkordancia-fájlok közvetlen
lekérdezéséből származik. Ahol egy állítás nem ellenőrzött (3.2 —
futásban lévő prompt), az explicit jelölve van.*
