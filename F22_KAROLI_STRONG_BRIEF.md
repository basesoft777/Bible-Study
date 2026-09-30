---
feladat: 22
cim: Károli–Strong párosítás a teljes Bibliára
kod: F22
tipus: feladat
fazis: 1
modell: sonnet
allapot: dontesre_var
ad: a Károli 1908 minden szavához Strong-szám bizonyossággal (két tábla, KJV-támponttal)
kovetkezo: Te: a pilot (#21) nem felel meg; döntés: marad, módosított céllal indul, vagy elhalasztva (l. DT21, naplok/F21P_jelentes.md)
olvas: [konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_Strong_kivonat.tsv]
ir: [konkordancia/Karoli_Strong_OSZ.tsv, konkordancia/Karoli_Strong_USZ.tsv, adat/karoli_strong_kezi.tsv, adat/datasetek.tsv, adat/SEMA.md, eszkozok/karoli_strong/, f22/, .github/workflows/f22_parositas.yml]
fugg: [21]
---
# F22_KAROLI_STRONG_BRIEF.md — Károli–Strong párosítás a teljes Bibliára

*FELADATOK #22 · v1 · 2026.09.30 · Modell: sonnet (szkript és adatmunka) · aranyminta: opus (`vegrehajto-opus`) · Külső modellek (OpenRouter): `google/gemini-3.1-flash-lite` (A), `deepseek/deepseek-v4-flash` (B), döntőbíró `google/gemini-3.8-flash` (C, csak eltérésnél) · Ág: `claude/f22-karoli-strong` · Két menet, köztük egy ⛔ megállás*

## Mit ad, ha kész

A Károli 1908 minden szava mellett ott lesz, melyik héber vagy görög szót fordítja, a Strong-számmal és egy bizonyossági értékkel együtt. Az eredeti szöveg minden szavánál az is látszik, hogy Károli lefordította-e, és ha igen, melyik magyar szóval.

Ebből lesz:

- magyar szóból induló keresés (pl. „föld” → *erec* vagy *adáma*);
- fordítási térkép (egy Strong-számot Károli hányféleképpen és hol fordít);
- frázismotívumok gépi ellenőrzése a magyar szövegen;
- a tanulmányok és az `elofordulasok.tsv` `karoli_szo` mezőjének gépi ellenőrzése (néma hiányok, rossz Strong-szám);
- a lexikonoldalak Károli-kulcsszó oszlopának gépi alapja;
- a leendő olvasói felület alapja (szóra bökve megnyílik a szócikk).

## Előzmény és viszony a meglévő adathoz

- A módszer ugyanaz, mint a `Join_tabla_folyamat_magyarazat.md`-ben leírt tanulmányvezérelt párosításé: **a Strong-szám mindig a TAHOT/TAGNT-ből jön, a modell csak párosít**, angol támponttal. Az új elem, hogy minden vers minden szava sorra kerül, és a bizonyosságot két független modell egyezése adja.
- A `konkordancia/Karoli_Strong_kivonat.tsv` (383 sor) **nem változik**: az `adat/datasetek.tsv` szerint az `elofordulasok.tsv`-ből generált nézet, a motívumok kulcsszavait tartalmazza. Ebben a feladatban **aranymintaként** szolgál, az új teljes tábla pedig ellenőrzi.
- Licenc: a Károli 1908 közkincs, a TAHOT/TAGNT CC BY 4.0, a KJV (eBible.org) közkincs. Mindhárom kiadható külső modellnek.
- Versmegfeleltetés: a `TAHOT_kivonat.tsv` és a `TAGNT_kivonat.tsv` `Igehely` mezője már Károli-natív (`1Móz 1:1`). A KJV-verset a `Karoli_versmegfeleltetes.tsv` `igehely_kjv` oszlopa adja.

## Kiinduló számok (lekérdezve 2026.09.30, `main` = `634d567`)

| Adat | Érték |
|---|---|
| Károli-versek (`Karoli_1908.tsv`) | 31 158 |
| Károli-szavak (`\w+` szerint) | kb. 599 000, átlag 19,2 / vers |
| TAHOT-szósorok / versek | 468 968 / 23 179 |
| ebből nyelvtani előtagkód (H9xxx) | 169 598 |
| TAGNT-szósorok / versek | 141 746 / 7 948 |
| ebből TR-t tartalmazó sor | 137 220 |
| Károli-vers TAHOT/TAGNT-párja nélkül | 61 |
| TAHOT/TAGNT-vers Károli-párja nélkül | 30 |
| Meglévő arany sorok (`Karoli_Strong_kivonat.tsv`) | 383 |
| `elofordulasok.tsv` sorai (`karoli_szo` mezővel) | 260 |

A 0. lépés ezeket újra lekérdezi. Eltérés esetén a friss szám érvényes, és a jelentésbe kerül.

## Munkamegosztás

| Lépés | Ki végzi |
|---|---|
| Előkészítő szkriptek, kapuk, építő szkript, jelentés | Code (sonnet) |
| Aranyminta 100 versre | Code, `vegrehajto-opus` subagent |
| Aranyminta szúrópróbája (20 vers) | te, a ⛔ pontnál |
| Párosítás (pilot és teljes futás) | A és B modell a GitHub Actionsben, C csak az eltérő versekre |
| Ellenőrzés | CI és `fuggetlen-ellenor` |
| Alacsony bizonyosságú sorok átnézése | te, később, a `naplok/F22_atnezes.tsv` alapján; a merge nem vár rá |

## Keretek

- **A modell nem ír Strong-számot.** A kimenet csak sorszámpárokat tartalmaz (magyar szó sorszáma → eredeti szó sorszáma). A Strong-számot az építő szkript teszi be a TAHOT/TAGNT-ből. Ha a válaszban Strong-szám formájú karakterlánc van, a kapu elutasítja.
- **Számadat** (arány, darabszám, költség) csak szkriptkimenetből kerülhet a jelentésbe.
- **Kulcs:** `OPENROUTER_API_KEY` repo-secret, csak az Actions job `env`-jében. Soha nem kerül fájlba, naplóba vagy commitba; commit előtt kulcs-grep.
- **HTTP-kliens:** az `eszkozok/fordit.py` `_valodi_http_kuldo` függvényét használd újra (importálva vagy közös modulba kiemelve). Új klienst ne írj.
- **Költségplafon:** pilot legfeljebb **3 USD**, teljes futás legfeljebb **60 USD** (G6). A futásnapló alapján minden köteg előtt ellenőrizd; elérésekor állj meg tiszta ponton.
- **Nincs darabolás versen belül.** Egy vers mindig egészben megy a modellhez.
- **Folytathatóság:** a már megválaszolt versek nem futnak újra. A nyers válaszok versenként mentődnek.
- **A kézi javítás a forrásrétegben történik**, mezőkulcsos felülíró táblában (`igehely` + `k_poz`), soha nem a generált táblában.
- Minden lépés után commit és push a távoli ágra.

## 1. menet — előkészítés, aranyminta, pilot

### 22.0 Felmérés és előkészítés

1. Kérdezd le újra a „Kiinduló számok” táblát, és rögzítsd a `naplok/F22_felmeres.md`-ben.
2. **A 61 + 30 versmegfeleltetési maradék:** listázd ki, és osztályozd őket (összevont vers, osztott vers, TAHOT/Károli fejezethatár, Károliban hiányzó vers). Az összevont és osztott eseteknél a modell a verspárt együtt kapja meg. Ami nem osztályozható, `kezi` jelölést kap, és a pilotból kimarad.
3. **Sorrend-ellenőrzés:** ellenőrizd, hogy a TAHOT/TAGNT sorok egy versen belül a szórendben állnak (a nyers fájl `#01, #02…` sorszámával, `konkordancia/TAHOT_TAGNT_README.md`). Ha igen, a versen belüli sorszám a sorrendből származtatható. Ha nem, állj meg és jelezd.
4. **Károli-tokenizálás:** determinisztikus függvény (`eszkozok/karoli_strong/tokenek.py`): token = Unicode betű- és számjegysorozat, az írásjel nem token. Ugyanaz a függvény dolgozik a promptnál, a kapunál és az építésnél. Egységteszt a 383 arany sor szavaira: mindegyik szó megtalálható az adott vers tokenjei között. Ha nem, listázd.
5. **KJV-import (N29):** az eBible.org `eng-kjv_usfm.zip` szó-szintű Strong-címkéiből `konkordancia/KJV_Strongs_teljes.tsv` (a meglévő `KJV_Strongs_*.tsv` oszlopaival: `Igehely | Szósorszám | Strong-szám | Angol szó | Morfológiai kód`), Strong nullázva. A letöltés az Actionsben fut (a cloud proxy blokkolhat). Proveniencia-fejléc: URL, sha256, dátum. Ellenőrzés: a meglévő 1Móz/2Móz/Péld táblákkal soronkénti egyezés, az eltérések száma a jelentésbe. *(A #19 végzi, ha a #21 pilot az import mellett dönt.)*
6. **Az arany sorok előkészítése:** a `Karoli_Strong_kivonat.tsv` sorait `(igehely, Károli-szó, Strong)` hármassá alakítsd a Károli-natív igehellyel és nullázott Strong-számmal, csak memóriában, a fájl módosítása nélkül. Az ismert eltéréseket (N21, F4.0d szófaj-drift) nem kell javítani, mert a szófaj- és gyökoszlop az aranymintában nem játszik szerepet.

### 22.1 Prompt és kapu

**A modell bemenete versenként:**

```
VERS: 1Móz 1:1
KÁROLI (számozott szavak): 1 Kezdetben | 2 teremté | 3 Isten | 4 az | 5 eget | 6 és | 7 a | 8 földet
EREDETI (számozott szavak): 1 בְּ H9003 [in] | 2 רֵאשִׁית H7225 [beginning] | 3 בָּרָא H1254 [he created] | ...
KJV-TÁMPONT: In the beginning{H7225} God{H430} created{H1254} the heaven{H8064} and{H853} the earth{H776}
```

- Az eredeti szavaknál: sorszám, ragozott alak, Strong-szám, angol tükörfordítás (a TAHOT/TAGNT `Angol tükörfordítás` oszlopa). A Strong-szám a bemenetben tájékoztató, a kimenetben tilos.
- ÚSZ-ben a nem TR-es sorok `[nem TR]` jelölést kapnak; ezekre a várt válasz „nincs fordítva”.
- A prompt 10 verset kér egy hívásban (G5); az utasításrész a kötegen belül közös.

**A modell kimenete (JSON):**

```json
{"vers":"1Móz 1:1","parok":[[1,[1,2]],[2,[3]],[3,[4]],[5,[5]],[6,[7]],[8,[8]]],
 "betoldas":[4,7],"forditatlan":[6]}
```

- `parok`: magyar sorszám → egy vagy több eredeti sorszám. Egy eredeti szó több magyar szóhoz is tartozhat.
- **Nyelvtani előtagok (H9xxx):** ha a magyarban raggal vagy névutóval jelenik meg, ahhoz a magyar szóhoz tartozik, amelyiken a rag áll (a *Kezdetben* → H9003 + H7225). Ha a magyarban nincs nyoma, `forditatlan`.
- `betoldas`: magyar szó eredeti megfelelő nélkül (névelő, segédige, Károli betoldása).
- `forditatlan`: eredeti szó magyar megfelelő nélkül (pl. a tárgyjelölő אֵת, H0853).

**Gépi kapu (`eszkozok/karoli_strong/kapu.py`), versenként:**

1. érvényes JSON, a `vers` mező egyezik;
2. minden hivatkozott sorszám létezik;
3. minden Károli-token pontosan egyszer szerepel (`parok` bal oldalán vagy a `betoldas`-ban);
4. minden eredeti token szerepel legalább egyszer (`parok` jobb oldalán vagy a `forditatlan`-ban);
5. nincs `[HG]\d{3,4}` minta a válaszban.

Hibás válasz esetén egy újrakérés a hibaüzenettel. Ha másodszor is hibás, a vers „kapuhiba” jelölést kap, és a C modellhez megy.

### 22.2 Aranyminta
*Helyette a #21.*

1. **Pilotminta: 300 vers**, rögzített véletlenmaggal, rétegzetten: 60 ÓSZ-próza, 60 költészet (Zsolt, Jób, Péld, Én), 60 próféta, 60 evangélium + ApCsel, 60 levél + Jel. A 383 arany sor verseinek legalább fele benne van. A minta: `f22/pilot_minta.tsv`.
2. **Opus-arany:** a pilotminta 100 versére (minden rétegből 20) a `vegrehajto-opus` teljes, szó-szintű párosítást készít ugyanabban a JSON-formában, a modellekétől függetlenül, a modellválaszok ismerete nélkül. Kimenet: `f22/arany_opus.jsonl`.
3. **A régi arany:** a 22.0/6 hármasai, a pilotminta verseire szűrve.

### 22.3 Pilot futtatása (Actions)
*Helyette a #21.*

- Workflow: `.github/workflows/f22_parositas.yml`, indítás push-ra, ha az `f22/futtatas.txt` változik. Paraméter: `--minta pilot` vagy `--konyv <könyv>`.
- Az A és a B modell a 300 versen, egymástól függetlenül. Utána a C modell csak azokon a verseken, ahol A és B link-szinten eltér, vagy ahol kapuhiba volt; C látja A és B válaszát, és egyik mellett dönt, vagy saját választ ad.
- A nyers válaszok helye: `f22/valaszok/<modell>/<könyv>.jsonl.gz`.

### 22.4 Mérés és ⛔ megállás
*Helyette a #21.*

A `eszkozok/karoli_strong/meres.py` kiszámolja, a `naplok/F22_pilot_jelentes.md` rögzíti:

| Mérőszám | Definíció |
|---|---|
| A–B egyezés | az azonos `(k_poz, e_poz)` linkek aránya a két modell linkjeinek uniójához |
| Pontosság az Opus-aranyhoz | a végleges (bizonyossággal ellátott) linkek közül hány van az aranyban, bizonyossági szintenként külön |
| Lefedettség az Opus-aranyhoz | az arany linkjeiből hány van a végleges kimenetben |
| Régi arany egyezés | a 383-as hármasok közül hány egyezik (azonos vers, azonos Károli-szó, a Strong-szám a linkelt eredeti szavak között) |
| Kapuhiba-arány | modellenként, első és második próbálkozás után |
| Bizonyossági eloszlás | magas / közepes / alacsony arány |
| Költség | USD/vers modellenként, a futásnaplóból, és a teljes Bibliára vetítve |
| Átnézési sor várható mérete | a 22.7 szabályai szerint, a teljes Bibliára vetítve |

**⛔ Állj meg.** Nyiss tételt a `DONTESEK.md`-ben a mérőszámokkal, és kérd:

1. a küszöb teljesülésének elfogadását (G7), vagy a prompt/modell módosítását és a pilot megismétlését;
2. a 20 versből álló szúrópróbát az Opus-aranyon (a 100-ból rétegenként 4, a szkript választja): a felhasználó jelzi, ha az arany hibás. Ha a hibás arany-linkek aránya 3% fölött van, az arany javítása után a mérés újrafut;
3. a teljes futás költségplafonjának megerősítését.

A menet zárása: ellenőr, push, draft PR (a pilot kimenetei nem kerülnek az `adat/` és a `konkordancia/` könyvtárba).

## 2. menet — teljes futás, építés, zárás

Csak a ⛔ pont „mehet” döntése után.

### 22.5 Teljes futás

- Az Actions mátrix könyvenként fut (66 job, egyszerre legfeljebb 6), a pilot promptjával és modelljeivel.
- A pilotban már megválaszolt versek nem futnak újra.
- A költségplafont a futásnapló alapján minden köteg előtt ellenőrzi. Elérésekor megáll, és a zárójelentésben „Folytatási pont” szerepel.

### 22.6 Építés

`eszkozok/karoli_strong/epit.py` a nyers válaszokból és a felülíró táblából építi:

**`konkordancia/Karoli_Strong_OSZ.tsv` és `konkordancia/Karoli_Strong_USZ.tsv`** (a méret miatt két fájl), GENERÁLT-fejléccel és proveniencia-sorral:

| Oszlop | Tartalom |
|---|---|
| `igehely` | Károli-natív (`1Móz 1:1`) |
| `k_poz` | a Károli-szó sorszáma a versben; üres, ha `forditatlan` |
| `k_alak` | a Károli-szó alakja |
| `e_poz` | az eredeti szó sorszáma a versben; üres, ha `betoldas` |
| `strong` | a TAHOT/TAGNT-ből, nullázva |
| `e_alak` | az eredeti ragozott alak |
| `kapcsolat` | `1:1`, `1:n`, `n:1`, `n:m`, `betoldas`, `forditatlan` |
| `bizonyossag` | `magas`, `kozepes`, `alacsony` |
| `dontes` | `egyezes`, `dontobiro`, `kezi` |

Bizonyossági szabály (G4):

- **magas:** A és B ugyanazt a linket adta, és a KJV-támpont nem mond ellent (ahol a KJV ugyanazt a Strong-számot más angol szóhoz köti, mint amit a Károli-szó jelent, a sor legfeljebb `kozepes`);
- **kozepes:** a döntőbíró (C) A vagy B egyikével egyezett;
- **alacsony:** hármas eltérés, vagy a vers kapuhibás maradt; a C válasza kerül be.

**`adat/karoli_strong_kezi.tsv`** (felülíró tábla, kezdetben üres, csak fejléccel): `igehely | k_poz | e_poz | kapcsolat | indok | datum`. Az `epit.py` utoljára alkalmazza, `dontes=kezi`, `bizonyossag=magas`.

Regisztráció: új sorok az `adat/datasetek.tsv`-ben, új szakasz az `adat/SEMA.md`-ben (a következő szabad 2.x szám), `CLAUDE.md` hivatkozó sor.

### 22.7 Ellenőrzések és átnézési sor

1. **Lefedettség:** minden Károli-token és minden eredeti token szerepel a táblában. Hiány esetén a menet nem zárható.
2. **Új `ellenoriz.py` szabály:** minden `elofordulasok.tsv`-sorra ellenőrzi, hogy a `karoli_szo` az adott versben ugyanahhoz a Strong-számhoz kapcsolódik-e a teljes táblában. Eltérésnél **jelez, nem bukik** (a döntés tartalmi).
3. **`naplok/F22_atnezes.tsv`** (a felhasználónak, később):
   - minden eltérés a régi arannyal és az `elofordulasok.tsv`-vel;
   - minden `alacsony` sor az `elofordulasok.tsv` igehelyein;
   - 1%-os rögzített magú véletlenminta az `alacsony` sorokból.

   A többi `alacsony` sor a táblában marad a jelölésével; a felhasználás során a bizonyosság látszik.
4. **Összesítő:** `naplok/F22_jelentes.md` a teljes futás mérőszámaival (bizonyossági eloszlás könyvenként, költség, kapuhibák, átnézési sor mérete).

### 22.8 Zárás

`fuggetlen-ellenor` (`naplok/ELLENOR_F22.md`), push, draft PR, a `FELADATOK.md` #22 sorának frissítése. A záró összefoglaló első sora a PR linkje és a CI állapota.

## Döntések (jóváhagyásra)

| # | Döntés | Javaslat | Elvetett alternatíva |
|---|---|---|---|
| G1 | Hatókör | teljes Biblia, minden vers minden szava | csak a motívumok igehelyei (gyorsabb, de a D1 miatt később újra kellene futtatni) |
| G2 | Módszer | külső LLM-párosítás, a modell csak sorszámot ad | statisztikai szóillesztés (fast_align + magyar lemmatizáló): Károli szabad fordításain rosszul teljesít, és a 09.14-i becslés szerint 30–45 óra fejlesztés |
| G3 | Modellek | A = Gemini 3.1 Flash Lite, B = DeepSeek V4 Flash, C = Gemini 3.8 Flash csak az eltéréseken | MiniMax M3 döntőbírónak (az FP2-ben kitalált tartalmat írt); Claude-session mint párosító (drága, és elviszi a Code-keretet) |
| G4 | Bizonyosság | két modell egyezése + KJV-ellentmondás lefelé húz | a modell saját bizonyossági becslése (nem mérhető, nem megbízható) |
| G5 | Kötegméret | 10 vers / hívás | versenként egy hívás (az utasításrész tokenje tízszeres) |
| G6 | Költségplafon | pilot 3 USD, teljes futás 60 USD | plafon nélkül |
| G7 | Pilot-küszöb | a `magas` linkek pontossága az Opus-aranyhoz ≥ 98%, az összes link lefedettsége ≥ 95%, a régi arany egyezése ≥ 95%. **A küszöb mérés előtt rögzített, mérés után nem változik** | egyetlen összesített pontosság (elfedi, hogy a `magas` jelölés megbízható-e) |
| G8 | Aranyminta | Opus 100 vers + a 383 régi sor + 20 vers felhasználói szúrópróba | 200 vers teljes kézi arany (kb. 3 800 link kézi munkája) |
| G9 | KJV | az eBible.org teljes KJV importja ennek a feladatnak a 0. lépése (N29 lezárul) | külön importfeladat; BSB mint támpont (csak az 1Mózes mért, a teljes lefedettség nem ismert) |
| G10 | Kézi átnézés | csak a 22.7/3 sor; a merge nem vár rá | minden `alacsony` sor átnézése a merge előtt (a pilot előtt a mérete nem ismert, a teljes feladatot blokkolná) |
| G11 | A régi kivonat | változatlan marad, generált nézet; az új tábla ellenőrzi | a régi kivonat kiváltása az új táblával (a motívum-kulcsszó kiválasztása tartalmi döntés, nem a teljes tábla dolga) |

## Költségbecslés (a pilot pontosítja)

Levezetés, hogy a pilot után ugyanígy újraszámolható legyen:

- bemenet versenként kb. 530 token (eredeti szavak kb. 200, Károli kb. 80, KJV kb. 100, az utasítás 10 versre elosztva kb. 150);
- kimenet versenként kb. 150 token;
- 31 158 vers modellenként: kb. 16,5 M bemeneti és 4,7 M kimeneti token;
- a döntőbíró a versek azon részén fut, ahol A és B eltér; ennek aránya a pilotból derül ki.

A díjat a `fp2/koltsegbecsles.py` modelláraiból kell számolni, a pilot mért token/vers értékével. Ha a vetített költség a 60 USD-t meghaladja, a ⛔ pontnál ez döntési kérdés.

## Kész, ha

- **K1** A „Kiinduló számok” újra lekérdezve, a 61 + 30 maradék osztályozva.
- **K2** A KJV-import kész, az 1Móz/2Móz/Péld táblákkal összevetve.
- **K3** A pilot mérőszámai a jelentésben, a G7 küszöb teljesül vagy a felhasználó döntött.
- **K4** A két tábla lefedi az összes Károli-tokent és eredeti tokent.
- **K5** Egyetlen sorban sincs a modell által írt Strong-szám (minden `strong` a TAHOT/TAGNT-ből levezethető, gépi ellenőrzéssel).
- **K6** Az `ellenoriz.py` új szabálya fut, és jelzi az `elofordulasok.tsv`-eltéréseket.
- **K7** `naplok/F22_atnezes.tsv` elkészült.
- **K8** A költség a plafon alatt, a futásnapló alapján.
- **K9** Kulcs-grep tiszta, a nyers válaszok commitolva, az újraépítés (`epit.py`) API-hívás nélkül ugyanazt a táblát adja.
- **K10** `ELLENOR_F22.md` TISZTA, CI zöld.

<!-- KOZVETLEN_FUTTATAS -->
## Nyitó prompt (a Code-sessionhöz, `/kovetkezo` után)

> A feladat: FELADATOK #22, Károli–Strong párosítás a teljes Bibliára. A brief: `F22_KAROLI_STRONG_BRIEF.md` a repó gyökerében. Az 1. menetet futtasd (22.0–22.4), a 22.4 ⛔ pontján állj meg, és a döntési tételt a `DONTESEK.md`-be írd. Ág: `claude/f22-karoli-strong`. Minden lépés után commit és push. A menet végén `fuggetlen-ellenor`, push, draft PR, a `FELADATOK.md` #22 sorának frissítése.
<!-- /KOZVETLEN_FUTTATAS -->

## A FELADATOK.md-be kerülő sor (az 1. menet első commitjában)

| # | Feladat | Mit ad, ha kész | Állapot | Függ ettől | Következő lépés | Hol |
|---|---|---|---|---|---|---|
| 22 | Károli–Strong párosítás a teljes Bibliára | minden Károli-szóhoz Strong-szám bizonyossággal; magyar oldali keresés, fordítási térkép, a Károli-kulcsszó oszlop gépi alapja | ⬜ nem futott | — (#7-tel párhuzamosan futhat) | 1. menet: előkészítés, aranyminta, pilot ⛔ | `F22_KAROLI_STRONG_BRIEF.md` |

A #9 „Függ ettől” oszlopába kerül: #22.

Döntésnapló-sor:

| D14 | A Károli–Strong párosítás a teljes Bibliára külső modellekkel, az adatfázisban (#22); a #9 függ tőle | a lexikonoldalak Károli-oszlopa és a magyar oldali keresés erre épül; ha a render előtte készül, újra kell renderelni (D1) | csak a motívumok igehelyei; a tanulmányvezérelt, kumulatív join-tábla folytatása |

## Döntésnapló (a brief verziói)

| Verzió | Dátum | Változás | Indok |
|---|---|---|---|
| v1 | 2026.09.30 | első változat: teljes Biblia, két külső modell + döntőbíró, a modell csak sorszámot ad, Opus-arany + régi arany, KJV-import a 0. lépésben, pilot ⛔, két menet | a felhasználó kérése (teljes feldolgozás, kevés lépés); a korábbi tanulmányvezérelt módszer skálázása |
