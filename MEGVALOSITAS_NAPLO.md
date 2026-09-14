# Megvalósítási napló — F0-F3 fázis

**Készült:** 2026.09.13 (F0-F1) · frissítve 2026.09.14 (F2, F3.0, F3.1, F3.2, F3.3, F3.4)
**Forrás terv:** `ATALAKITASI_TERV.md.md`, 6. szakasz
**Fázisok:** F0 — Blokkolók feloldása (8 tétel) · F1 — Séma és belépési pont (6 tétel) ·
F2 — Lekérdező CLI · F3 — Retroaktív betöltés (F3.0 előfeltétel-ellenőrzés, F3.1 könnyű
csoport, F3.2 nehéz csoport, F3.3 gate.py első futtatása, F3.4 Károli-Strong
join — mind az öt lépés lefutott)
**Munkamenet:** Claude Code

---

# I. rész — F0 fázis (Blokkolók feloldása)

---

## Elkészült tételek

### F0.1 — HAMART-001 merge-döntés végrehajtva ✅

`git merge --no-ff bun-gyuruzese-20260911-opus` a `main`-be (commit `c28b49e`). Az opus-ág
kerül be — bővebb hatókör (teljes ÓSZ/ÚSZ scan, lexikai gerincre bontva, 46 táblázat-sor,
7 dataset), szemben a sonnet-ág Gen 1-11-re szűkített, tévesen "teljes"-nek címkézett
scanjével. Az opus-ág már tartalmazta a `bun-gyuruzese-20260911-sonnet` branch nélkül is
elvégzett B) táblázat BDB-javítást (3.2-es nyitott tétel) — ez a merge-döntéssel együtt
automatikusan lezárult.

A `bun-gyuruzese-20260911-opus` és `bun-gyuruzese-20260911-sonnet` branch-ek **nem lettek
törölve** — megmaradnak összehasonlítási referenciának, ahogy az `Atadasi_dokumentum_2026_09_11.md`
3.1. szakaszának egyik felvetett opciója javasolta.

### F0.2 — Sonnet tanítói szakaszának átemelése, parafrazálva ✅

A sonnet-ágon talált **Derek Prince**-forrás (*Blessing or Curse: You Can Choose*) — amely
a study 3-4. fejezetbeli átok-láncára (1Móz 3-4) explicit, névvel idézett tanítói forrást ad —
átkerült a mergelt `Bun_kovetkezmenyeinek_gyuruzese_tematikus.md`-be, **parafrazálva**, a
sonnet-ág kb. 65 szavas szó szerinti idézete nélkül (l. `ATALAKITASI_TERV.md.md` 4.4. szakasz
szerzői jogi megkötése). A bővített kánoni hatókörre (5Móz 27-28, Jer, Ez, Zsolt 74, Róm 8,
Zsid 6, Jel 11/19 stb.) a gap-jelzés megmaradt, mert Prince dedikált anyaga nem terjed idáig.
Frissítve: a study Q5-pontja, a `Lezart_tematikus_tanulmanyok_index.md` #8 sora (F0.4 utáni
számozással), és a `PaRDeS_motivumok.md` HAMART-001 bejegyzése. (Commit `47fb269`.)

### F0.3 — 4Móz 13:33 → 13:34 javítás az indexben ✅

A study-fájlokban (`Rafaim_tematikus.md`, `Isten_fiai_Nefilim_Gibborim_tematikus.md`) ez a
javítás már 2026.09.10-én megtörtént — csak a `Lezart_tematikus_tanulmanyok_index.md` #5
sora (a Rafeusok-tétel) maradt le róla. Javítva. (Commit `47fb269`.)

### F0.4 — Index hiányzó #2 sora / számozás rendezése ✅

A törölt `Tehom_Abusszosz_Hadesz_Tartarosz_tematikus.md` fájl miatt az index táblázata
1, 3, 4, 5, 6, 7, 8, 9 sorszámmal futott (a #2 hiányzott). Renumberelve folyamatosra
(1-8), a belső kereszthivatkozások (korábbi #3/#5/#7 → új #2/#4/#6) átvezetve. (Commit `47fb269`.)

### F0.5 — Négy hiányzó kereszthivatkozás-napló pótlása ✅

Elkészült mind a négy hiányzó napló, a study-fájlok saját szövegéből (0., 1., 2/b., Q2 pontok,
NAPLO-blokkok) rekonstruálva, minden vizsgált jelölt (beépített/elutasított/nyitva hagyott)
minősítésével:

- `tematikus_lezart/naplok/Rafaim_kereszthivatkozas_naplo.md` — a 12 alacsony szavazatú
  TSK-jelölt (5Móz 1:4 stb.) explicit "nyitva, nem minősítve" jelöléssel rögzítve.
- `tematikus_lezart/naplok/Isten_fiai_Nefilim_Gibborim_kereszthivatkozas_naplo.md` — a
  Károli-KH jelölt (1Móz 6:2 → Mt 24:38/Lk 17:27) szintén nyitva, nem minősítve rögzítve.
- `tematikus_lezart/naplok/Tehom_kereszthivatkozas_naplo.md`
- `tematikus_lezart/naplok/Hadesz_Seol_kereszthivatkozas_naplo.md`

Mind a négy study-fájl "6. Napló-frissítés" szakasza kiegészítve a naplóra mutató
hivatkozással. (Commit `1084ac8`.)

**Fontos korlát, amit a napló maga is jelez:** ezek a fájlok **utólagos rekonstrukciók**,
nem a 2026.09.10-i tényleges kutatási munkamenet élő jegyzetei — a tartalom forrása a
study-fájlok szövege és NAPLO-blokkjai, valamint az `Atadasi_dokumentum_2026_09_11.md`.
Ahol a study nem rögzítette explicit a keresés minden lépését, a napló ezt nem pótolja
utólagos találgatással.

### F0.6 — Két changelog kiszervezése ✅

- `motivumlog/PaRDeS_motivumok.md` verziónkénti története (v1-v56, ~38 KB) →
  `motivumlog/PaRDeS_motivumok_CHANGELOG.md`.
- `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` verziónkénti története (v15-v36, ~23 KB) →
  `PaRDeS_dontesek_CHANGELOG.md`.

A két élő fájl mérete együtt 271 419 bájtról 169 500 bájtra csökkent (~100 KB
megtakarítás, pontosan a terv 8.1-es becslése szerint). (Commit `98b44e6`.)

### F0.7 — Döntési fájl 4. szakaszának kiszervezése ✅

A `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` 4. szakasza (STEPBible↔SzPA join,
~40 KB, a v23-as bejegyzés óta felfüggesztett alrendszer) kiszervezve
`PaRDeS_STEPBible_SzPA_join_adatcsatorna.md`-be. A döntési fájlban a 4. szakasz címe és
egy pointer-bekezdés maradt; a fájlon belüli "4.1", "4.13" stb. kereszthivatkozások
(pl. a 0. szakasz dataset-táblázatában) továbbra is feloldhatók, csak a másik fájlban.
(Commit `98b44e6`.)

### F0.8 — "Teljes beolvasás" szabály cseréje ✅ (ideiglenes)

A `Rendszerfejlesztesi_playbook.md` 29-30. sorának "minden feladat első lépése a döntési
fájl teljes beolvasása" szabálya lecserélve egy szakasz-szintű táblázatra (melyik szakaszt
mikor kell megnyitni). A terv explicit jelzi, hogy ez **ideiglenes** — végleges formáját az
F1 fázis `CLAUDE.md`-je adja majd. (Commit `98b44e6`.)

---

## Nyitva maradt tételek / amit ez a munkamenet NEM végzett el

Ezek nem az F0 fázis részei, de a munka során előkerültek — a teljesség kedvéért rögzítve:

1. **A Rafaim 12 alacsony szavazatú TSK-jelöltje** (5Móz 1:4, 3:20, 3:22, 2:23; Józs 13:19,
   13:31; Jer 48:1, 48:23; Zsolt 105:23, 105:27, 106:22, 78:51; 1Krón 4:40) — a napló
   nyilvántartásba vette, de **egyedi minősítésük nem történt meg**. Ez a `NYITOTT_FELADATOK.md`-be
   vagy egy célzott munkamenetbe való (a terv F1.6 pontja is utal rá).
2. **A Károli-KH jelölt** (1Móz 6:2 → Mt 24:38/Lk 17:27) — nyilvántartásba véve az Isten
   fiai naplóban, de a döntés (bekerüljön-e valamelyik study-ba, önálló motívum legyen-e,
   vagy maradjon figyelmen kívül) **felhasználói döntésre vár**.
3. **Az `Atadasi_dokumentum_2026_09_11.md` 3.5-3.10 szakaszainak nyitott tételei**
   (Tehóm-duplikáció mint elv, "shem — név szerzése" motívum, Segítségül hívni két régi
   tétele, Sense-szám mező indoklása, modellhasználati stratégia, szerzői jogi státusz) —
   ezek az F0 tervben sem szerepeltek, változatlanul nyitottak.
4. **F0.8 véglegesítése** — a playbook-csere csak ideiglenes; a végleges `CLAUDE.md`
   (F1.1) még nem készült el.
5. **A törölt Tehóm-kiterjesztés fájlnév-történetének explicit jelzése** — a `Lezart_tematikus_tanulmanyok_index.md`
   fájlnév-konvenció szakasza nem lett kiegészítve a törölt `Tehom_Abusszosz_Hadesz_Tartarosz_tematikus.md`
   említésével (csak a táblázat #1/#2 sorának jegyzetében szerepel) — kisebb, kozmetikai hiányosság.

**Ami a tervben sem F0 alatt szerepelt, de érdemes tudni:** a két, még nem commitolt fájl a
gyökérben (`ATALAKITASI_TERV.md.md`, `Atadasi_dokumentum_2026_09_11.md`) — ezek a tervezési/
átadási dokumentumok, ez a munkamenet nem git-addolta és nem commitolta őket, mert a
feladat kizárólag az F0 végrehajtására szólt, nem ezek beolvasztására a repóba. Ha a
felhasználó szeretné, ezek külön commit-tal felvehetők.

> ⏹ **Ez a bekezdés azóta elavult (F1, 2026.09.13):** a két fájl — e napló mellett — az
> `e0acc5c` commitban („Átalakítási terv, átadási dokumentum és F0-megvalósítási napló
> felvétele") bekerült a repóba. **A 4. pont is lezárult:** az F0.8 ideiglenes
> playbook-cserét az F1.1 `CLAUDE.md` váltotta fel.

---

## Ellenőrzési nyom

Nyolc F0 tétel, négy tematikus commit a `main`-en (plusz az opus-ág három eredeti commit-ja
a merge-ön keresztül):

```
98b44e6 F0.6-F0.8: két changelog kiszervezése, SzPA-join adatcsatorna kiszervezése, playbook "teljes beolvasás" szabály cseréje
1084ac8 F0.5: négy hiányzó kereszthivatkozás-napló retroaktív pótlása
47fb269 F0.2-F0.4: Sonnet tanítói szakasz átemelése (parafrazálva), 4Móz 13:34 index-javítás, index-számozás rendezése
c28b49e HAMART-001 ("bűn következményeinek gyűrűzése") merge-döntés végrehajtása (F0.1)
```

A `main` jelenleg **nincs push-olva** az `origin`-ra — a felhasználó döntése, mikor és
hogyan kerüljön fel.

---
---

# II. rész — F1 fázis (Séma és belépési pont)

**Végrehajtva:** 2026.09.13, egyetlen menetben
**Terv-hivatkozás:** `ATALAKITASI_TERV.md.md` 6. szakasz, F1 (6 tétel); séma-részletek az
1.A, 4.1, 4.2, 4.3, 4.5, 4.6, 4.7 pontokból

Mind a hat tétel elkészült. Két helyen tértem el a tervtől, mindkettőt indokolva jelzem
(F1.1 méret, F1.4 mezőszerkezet).

---

## Elkészült tételek

### F1.1 — `CLAUDE.md` a repó gyökerébe ✅

A végrehajtó-agent belépési pontja. Ez váltja ki a korábbi „minden Code-feladat első lépése
a teljes `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md` beolvasása" szabályt (96 KB).

Tartalma: réteg-szabályok (ki írja melyik fájlt), a három megsérthetetlen szabály
(proveniencia / nincs közvetlen út / memória vs. lekérdezés), a hétlépéses kutatási menet,
a motívum-gate négy kérdése, a három ismert dataset-korlát, és az igehely-formátum
normalizálási csapdája.

⚠️ **Eltérés a tervtől:** a terv 2-3 KB-ot írt elő, a fájl **5,2 KB** lett. Két tömörítő
kört futtattam (az incidens-leírások átkerültek a `SEMA.md`-be, a hétlépéses táblázat
felsorolássá vált); ennél tovább csak load-bearing tartalom rovására mennék. Viszonyítás:
a kiváltott szabály 96 KB beolvasást írt elő, tehát a megtakarítás ettől együtt is ~95%-os.
**Ha a felhasználó ragaszkodik a 2-3 KB-hoz**, a gate négy kérdése és a hétlépéses menet
kiemelhető külön fájlba — de akkor a leggyakrabban kellő két szabályért plusz olvasás kell.

### F1.2 — `adat/SEMA.md` ✅

22 KB, a hét tábla teljes meződefiníciója típusokkal. Szerkezete: közös típusok (1.) →
táblánkénti mezőtáblák (2.) → integritási szabályok (3.) → amit nem old meg (4.).

Három dolog, amit a séma írása közben **el kellett dönteni**, mert a terv nyitva hagyta:

1. **Igehely-formátum (`SEMA.md` 1.1).** Kiderült, hogy a repóban **két formátum él
   egymás mellett**: a magyar kanonikus (`1Móz 1:1` — TAHOT, TAGNT, TSK, Károli_1908,
   LXX-kivonatok) és a STEPBible-pontozott (`Gen.1.1` — Károli-KH, Károli_Strong_kivonat,
   TIPNR). Az `adat/` réteg a **magyar kanonikus** alakot használja, mert a `lekerdez.py`
   öt determinisztikus lépése mind ilyen datasetet olvas. **Ez az F2-re nézve kötelezettség:**
   a `karoli` és a `tsk` parancs bemenete és kimenete között normalizálási lépés áll
   (`Konyv_normalizalo_tabla.tsv`) — enélkül **néma nem-találat** jön, nem hiba.
2. **A `statusz` mező szerkezete.** A terv egyetlen összetett értéket mutatott
   (`publikálható, v3, 2026.09.10`); a sémában ez **három külön mező**
   (`statusz` / `statusz_verzio` / `statusz_datum`), hogy gépileg szűrhető legyen.
3. **`jelentes_szam` — az átadás 3.8-as tétele lezárva** (`SEMA.md` 2.2.2). A mező típusa
   **union**: numerikus jelentés-szám **vagy** binyan-címke, mert a BDB az igegyököket
   binyan szerint tagolja, nem számozott sense-ekkel. A ma használatban lévő teljes
   értékkészletet megmértem a `tematikus_lezart/` + `genezis/` fájlokon: `Qal pass. ptc.` (6),
   `Pi'él` (2), `Qal impf.` (1), `Nif'ál` (1), `Hif'íl` (1), `Nif'ál / Hif'íl` (1).
   **Az indoklás, ami eddig hiányzott, most rögzítve van** — a sablonba nem kell külön
   módszertani jegyzet, elég erre a szakaszra hivatkoznia.

### F1.3 — Üres TSV-k fejléccel ✅

Öt tábla, kommentsorral és fejléccel: `motivumok.tsv` (13 mező), `elofordulasok.tsv` (15),
`kapcsolatok.tsv` (7), `jeloltek.tsv` (9), `lexikon_hivatkozasok.tsv` (7). A `jeloltek.tsv`
az F1.6-ban feltöltődött 16 sorral, a többi szándékosan üres — az F3 betöltés tölti fel.

### F1.4 — `adat/grammatikai_strongok.tsv` feltöltve ✅

> **Átdolgozva 2026.09.13-án, felhasználói specifikáció szerint.** Az első változat
> 183 soros volt, négy kategóriával és háromértékű `kizaras` mezővel. A specifikáció
> ennél szűkebb és élesebb szerkezetet ír elő; az alábbi a hatályos állapot. Az első
> változat indoklása a `f7c0e67` commitban olvasható.

**78 sor, négy oszlop:** `strong | rovid_jelentes | kategoria | kizaras_oka`.
A fájl **generált**: `eszkozok/grammatikai_strongok_general.py` állítja elő.
Determinisztikus, ellenőrizve.

**Három forrás:**

| Forrás | Sor | Hogyan |
|---|---|---|
| héber gépi alap — a TAHOT `H9xxx` tartománya | **44** | automatikusan kiolvasva, provenienciával |
| héber kézi kiegészítés | **3** | `H0853` tárgyrag, `H0834` vonatkozó névmás, `H3808` tagadószó — soronként indokolva |
| görög tételes lista | **31** | névelő 1, kötőszó 6, elöljáró 12, névmás 6, tagadószó 3, partikula 3 |

A `H9xxx` gépi alap **44 kód, 169 598 előfordulás** — a TAHOT-kivonat 468 968 sorának
36%-a. Ez a fájl legnagyobb hozadéka, és teljes egészében gépi: névelő, kötőszó,
prefixált elöljárók, névmási szuffixumok.

**Lelet — a görög oldalnak nincs gépi alapja.** A héber `H9xxx`-nek **nincs megfelelője**
a TAGNT-ben: a `G9xxx` tartomány ott **nem grammatikai**, hanem hét ritka *lexikai* szó
(συναλλάσσω „sürgetni", ὑπόλειμμα „maradék", ταπεινοφροσύνη, οἰκουργός stb.), egyenként
**egy** előfordulással — kiegészítő Strong-számok az eredeti számozásból kimaradt
szavakhoz. Az ok nyelvi, nem adathiba: a héberben a névelő, a kötőszó és a gyakori
elöljárók *prefixumok*, tehát külön grammatikai kódot kapnak; a görögben ugyanezek
*önálló szavak*, tehát rendes Strong-számon ülnek (`G3588` ὁ, `G2532` καί, `G1722` ἐν).
Ezért a görög oldal tételes lista, soronként indokolva, és a `kizaras_oka` mező ott, ahol
van párja, megnevezi a héber megfelelőt.

*Egy lemmatizálási sajátosság dokumentálva:* a TAGNT a többes számú személyes névmásokat
is az egyes számú kód alá sorolja (`ἡμῶν` a `G3165` alatt), ezért a `G2249` és a `G5210`
**nem kap sort** — a kivonatban nulla előfordulásúak. Ezt a generátor futás közben
jelezte, nem feltételezésből derült ki.

**`TILTOLISTA` — gépi tiltás, nem megjegyzés.** Négy Strong-szám soha nem kerülhet a
táblába: `H3068` (JHVH), `H0559` (*amar*, „mondani"), valamint görög párjaik, `G2316`
(θεός) és `G3004` (λέγω). Ha egy későbbi bővítés bármelyiket felvenné, a **szkript
hibával leáll**. Kipróbálva: `H3068` beszúrására a futás 1-es kilépési kóddal megáll.
Azért kell gépi őrzés, mert e szavak épp a leggyakoribbak közé tartoznak (`H3068` 6 528,
`G3004` 1 357, `G2316` 1 343), tehát egy „szűrjük ki a leggyakoribbakat" típusú bővítés
elsőként söpörné be őket.

**Proveniencia.** A fájl fejléce két proveniencia-sort visel, a `SEMA.md` 1.5
formátumában — külön a gépi héber alapra (`scope=OT-full | tartomany=H9xxx | n=44 |
elofordulas=169598`) és a tételes görög listára (`scope=NT-full |
modszer=teteles-lista | n=31 | elofordulas=65646`). A `modszer=teteles-lista` őszinte
jelölés: a görög sorok emberi döntésből származnak, csak az előfordulásszámuk gépi.

#### A besorolás kritériuma — a második átdolgozás

> **Átdolgozva 2026.09.14-én.** Az első kör a kézi héber listát háromtételesre szűkítette
> (`H0853`, `H0834`, `H3808`), és a kalibráció megmutatta, hogy három tiszta funkciószó
> bennmarad. A felhasználói válasz nem csak a hármat engedélyezte, hanem **a szabályt
> is kimondta**, amiből a hiány következett.

**A kritérium, ami eddig hiányzott:**

> Egy Strong-szám akkor grammatikai, ha a szó **önmagában nem hordoz tartalmi jegyet** —
> függetlenül attól, hogy prefixként vagy szabadon áll. A `H9xxx` tartomány kényelmes
> kiindulás, de **nem definíció**.

A `H9xxx` **ortográfiai határ, nem szemantikai**: a héberben a névelő, a kötőszó és a
gyakori elöljárók prefixumként tapadnak, ezért kaptak külön kódot — de egy elöljáró nem
attól lesz tartalmas, hogy külön szóként írják. Ebből következett, hogy **több ilyen van**,
nem csak a kérdezett három.

**A kézi héber lista 3 → 10 tételre bővült.** Az új hét:

| Strong | Szó | db | Görög párja a listán |
|---|---|---|---|
| `H0413` | אֶל — „felé" | 5 515 | `G1519` (εἰς) |
| `H5921` | עַל — „-on, fölött" | 5 768 | `G1909` (ἐπί) |
| `H3588` | כִּי — „mert, hogy" | 4 482 | `G3754` (ὅτι) |
| `H1931` | הוּא — „ő, az" | 1 876 | `G0846` (αὐτός) |
| `H5704` | עַד — „-ig" | 1 261 | — |
| `H4480` | מִן־ — „-ból" | 1 189 | `G1537` (ἐκ) |
| `H2088` | זֶה — „ez" | 1 180 | `G3778` (οὗτος) |

Mind a hét előfordulásszáma **pontosan egyezett** a megadott értékekkel; ellenőrizve a
TAHOT-on.

**A `H4480` önmagában bizonyítja a kritériumot.** Ugyanaz a héber elöljáró (*min*) két
Strong-számon ül, pusztán az írásmód szerint:

| | Strong | Előfordulás | Hol volt |
|---|---|---|---|
| prefixált (מִ) | `H9006` | **6 383** | a gépi `H9xxx` alapban, kezdettől |
| szabadon álló (מִן־) | `H4480` | **1 189** | sehol, amíg kézzel fel nem vettük |

**Egy független ellenőrző jel is adódott, amit nem kerestem:** a felvett tíz héber tétel
szófaja a `Strong_szotar.tsv`-ben kivétel nélkül `elöljárószó`, `kötőszó` vagy `névmás`,
a szándékosan kihagyottaké viszont `főnév` (`H3605`), illetve `ige` (`H1961`, `H6213`).
A kritérium tehát **gépileg ellenőrizhető**, nem csak kimondott — ez a jövőbeli
bővítéseknél használható kapu.

**A `TILTOLISTA` négyről hatra bővült:** felkerült a `H1961` (*hájá*, „lenni", 3 562) és a
`H6213` (*aszá*, „tenni", 2 628). Indok a felhasználói megjegyzésből: tartalmi igék,
amelyek a teremtés-motívumoknál **gerinc-elemek lehetnek**. Ez ugyanaz a logika, amiért a
`H0559` is tiltólistán van — ezért gépi őrzésbe tettem, nem csak kihagytam. *Ha ez
túlmegy a szándékon, egyetlen sor visszavonja.*

**Új, `HATARESET` rekesz — dokumentált, de inaktív.** A `H3605` (*kol*, „minden", 5 412)
**sem a táblán, sem a tiltólistán nincs**: gyakori és kvantor-szerű, de a teljesség /
kivétel nélküliség motívumszinten releváns lehet. A kérdés így nyitva marad egy későbbi
kör számára, ahogy a felhasználói megjegyzés kérte („vagy ha igen, külön kategóriával és
indoklással").

#### Hatókör rögzítve — stopword-lista, nem globális kizárás

A `SEMA.md` új 2.7.5 pontja kimondja: ez a tábla a **`gerinc` parancs stopword-listája**.
Ha egy elöljáró motívumszinten számít — mint az עַל־פְּנֵי (*al-pené*, „színe fölött",
1Móz 1:2) —, azt a **`kollokacio`** parancs találja meg, amely szópárt keres egy versen
belül, nem a `gerinc`, amely szakaszok közös Strong-halmazát metszi. **A kettő nem
ütközik:** más a bemenetük, más a kérdésük.

Gyakorlati következménye a sémára: ha egy sor elöljárós szerkezeten lóg, a `gerinc_elem`
mezőbe a **kollokáció-pár** kerül (`al+pané`), nem a puszta Strong-szám.

#### Kalibráció — a lista fejlődése ugyanazon az eseten

| Változat | Eredmény | Mi hagyta bent a többletet |
|---|---|---|
| első (keretszavas, 183 sor) | 23 → **3** | — (de keretszavakat is szűrt, ami leletet veszélyeztetett) |
| szűkített (3 kézi tétel, 78 sor) | 23 → **14** | a lista esetenként épült, nem szabály szerint |
| **kritérium-alapú (10 kézi tétel, 85 sor)** | **23 → 11** | — |

| | |
|---|---|
| metszet | **23** |
| kiszűrve — 7 `H9xxx` + `H0853`, `H0834`, `H0413`, `H5921`, `H3588` | **12** |
| **marad — gerinc-jelölt** | **11** (52%) |

**A lényeges eredmény nem a szám, hanem az összetétel: a megmaradó tizenegyből egy sem
funkciószó.** Mind főnév vagy ige — `H0127` *adamá*, `H0430` *Elohim*, `H0559` *amar*,
`H0802` *issá*, `H1121` *bén*, `H1961` *hájá*, `H3205` *jalad*, `H3605` *kol*,
`H3947` *lakach*, `H6213` *aszá*, `H6440` *pané*. A grammatikai osztály ezen a
teszteseten **lezárult**; ami bent maradt, az emberi ítéletet kíván, nem listabővítést.

Ez egyben azt is jelenti, hogy a mostani 52% **nem hasonlítható** az első változat 87%-ához:
az a szám keretszavak kiszűrésével jött ki, amit a mostani szerkezet szándékosan nem tesz.

### F1.5 — `adat/datasetek.tsv` ✅

**68 sor** — 17 dataset × 4 study-típus (`bovitett`, `tematikus`, `melyelemzes`,
`lexikon_oldal`), a terv 4.3 mátrixa kifejtve. Mezők: `kotelezoseg`
(`mindig`/`felteteles`/`ajanlott`/`oroklott`), `feltetel`, `allapot`, `megjegyzes`.

**A lefedettség tényleges felmérése két olyan tételt hozott, amit a mátrix most rögzít:**

- **Az SDBH és az SDGNT `allapot=hianyzik`.** A terv 4.3 pontja új datasetként javasolja
  ezeket (UBS, CC BY-SA 4.0), és a szöveg úgy olvasható, mintha rendelkezésre állnának —
  **a repóban nincsenek** (ellenőrizve: egyetlen SDBH/SDGNT/UBSHebrew fájl sincs).
  **Következmény az F2-re:** a `domen` parancs **nem implementálható**, és az F2 harmadik
  elfogadási tesztje (az `arar`/`kalal` közös „Curse" doménje) **nem futtatható**, amíg az
  import meg nem történik. Felvéve a `NYITOTT_FELADATOK.md`-be.
- **`KJV_ASV_Strongs` `allapot=korlatos`** — csak Genezis, Exodus, Példabeszédek.

### F1.6 — A döntési fájl 8. szakaszának migrálása ✅

A terv tételes újraellenőrzést írt elő, „mert több bejegyzés elavult". **Elvégeztem, és
három elavult állítást találtam** — kettőt a döntési fájlban, egyet a `NYITOTT_FELADATOK.md`-ben.

**Vers-szintű jelöltek → `adat/jeloltek.tsv` (16 sor, mind `dontes=nyitva`):**

| ID | igehelyek | forrás |
|---|---|---|
| `HODIT-001` | 13 alacsony szavazatú TSK-jelölt (5Móz 1:4, 2:23, 3:20, 3:22; Józs 13:19, 13:31; Jer 48:1, 48:23; Zsolt 78:51, 105:23, 105:27, 106:22; 1Krón 4:40) | Rafaim-napló (F0.5) |
| `MENNY-001` | Mt 24:38, Luk 17:27 | Károli-KH jelölt, 1Móz 6:2-ből |
| `ANTROP-001` | Fil 1:27 | döntési fájl 8. szakasz |

**Nem vers-szintű tételek → `NYITOTT_FELADATOK.md`** (új szakasz): TAHOT lefedettségi rés,
Károli-kiadás hitelesítése, Károli-revízió sokféleség, rokon gyökű jelöltek, Példabeszédek/
ApCsel feldolgozás, PAT-döntés, figyelendő STEPBible-adatállományok, SDBH/SDGNT import,
Motívumlexikon-tervezés.

**`DONTESEK_INDEX.tsv`** — a döntési fájl ezzel archívummá vált. 9 szakasz, mindegyiknél
`allapot` (`elo`/`felfuggesztve`/`kiszervezve`/`archiv`) és „mikor nyisd meg". A sorszámok
tájékoztatóak; a stabil horgony a `## <szakasz>.` fejléc.

#### A három elavult állítás — amit az újraellenőrzés talált

1. **„Segítségül hívni — 94 új jelölt" (döntési fájl).** A terv maga is gyanította.
   Megerősítve: a 94-es szám (65 ÓSZ + 29 ÚSZ) a `Konnyu_ellenorzes_4_lezart_tanulmany.md`
   **saját jelzése szerint is zajos keresésből** származott. Azóta jobb módszertanú kör
   futott (2026.09.08): a G1941 mind a 31 ÚSZ-előfordulásának egyenkénti áttekintése és
   H7121+H8034 kombinált teljes ÓSZ-scan (196 nyers találat, a gyermeknévadási formula
   zajként kiszűrve) — a study hat új ÚSZ-igehellyel bővült, a D-mintát dokumentálta és
   kizárta, és megkapta a Q1-Q5 kaput. **Felülírt mérőszám, nem nyitott feladat** —
   nem migrálva, a helyén ⏹-jelöléssel.
2. **„A hádész-komplexum 46 seól-jelöltje továbbra is nyitott" (döntési fájl).** **Elavult:**
   a teljes H7585-scan lefutott — a `Hadesz_Seol_tematikus.md` v2 (2026.09.10) 66 nyers
   szóelőfordulást / **64 egyedi verset** vizsgált, **64 beépítve**, Hós 13:14 kiemelt
   leletként (Pál 1Kor 15:55-ben idézi). Naplózva az F0.5-ben pótolt Hádész-naplóban.
3. **Ugyanez a `NYITOTT_FELADATOK.md`-ben is állt** („a Seól-motívum jelölt-listája
   továbbra is valóban nyitott; egy teljes, friss H7585-scan szükséges") — **javítva**.
   Ami ténylegesen marad: egy megerősítő újra-scan, és a H4103 (*mehumáh*) rokon gyökű
   jelölt minősítése.

**Egy számolási eltérés is előkerült:** a Rafaim-napló „12 alacsony szavazatú TSK-jelöltet"
ír, de **13 igehelyet sorol fel**. A `jeloltek.tsv` a **13 tényleges igehelyet** viszi.

### Ráadás — az F0.8 véglegesítése ✅

Az F0 napló „nyitva maradt" 4. tétele (a playbook-csere ideiglenessége) ezzel lezárult:
a `Rendszerfejlesztesi_playbook.md` 1. pontja most a `CLAUDE.md`-re mint belépési pontra
mutat, a 8. szakasz sora pedig „már nem kell megnyitni" jelölést kapott.

---

## Ellenőrzési nyom

| Ellenőrzés | Eredmény |
|---|---|
| generátor determinisztikus (kétszeri futtatás diffje) | **OK** |
| TSV oszlopszám-integritás (7 `adat/` tábla + index) | **OK, 0 hiba** |
| a `SEMA.md` lefedi-e minden tábla minden mezőjét | **OK, 0 nem dokumentált mező** |
| HAMART-001 metszet újraszámolva a terv 23-as értéke ellen | **23 = 23** |
| szűrő-kalibráció ugyanazon az eseten | **23 → 11, és a maradékban nincs funkciószó** (l. F1.4) |
| TILTOLISTA-őrző élesben (H3068 beszúrása) | **hibával leáll, kilépési kód 1** |
| a 6 tiltólistás + a határeset tényleg kint van-e a táblából | **OK, mind a 7** |
| a 7 új héber tétel tényleg bekerült-e | **OK, mind a 7** |
| `DONTESEK_INDEX.tsv` sorszámai a tényleges fejlécek ellen | javítva (8. szakasz vége 278 → 293) |

---

## Nyitva maradt tételek

**Az F1-en belül: semmi.** Mind a hat tétel elkészült.

Amit az F1 **felszínre hozott**, és a következő fázisoké:

1. **SDBH / SDGNT import — az F2 blokkolója.** Amíg nincs meg, a `domen` parancs nem
   implementálható és a harmadik elfogadási teszt nem futtatható. Az F2 tehát vagy ezzel
   kezdődik, vagy tudatosan kétlépcsős lesz (öt parancs most, `domen` később).
2. **Az igehely-normalizálás az F2 kötelezettsége** — l. F1.2/1. Ez nem kényelmi funkció:
   normalizálás nélkül a `karoli` és a `tsk` parancs néma nem-találatot ad.
3. **A `TAHOT_kivonat.tsv` lefedettségi résének tételes felmérése** — a terv ezt az F2 első
   lépéseként írja elő. Amíg nincs meg, a `scope=OT-full` proveniencia-érték **a kivonat
   teljességét jelenti, nem a kánonét** (így is van dokumentálva a `SEMA.md` 4. pontjában).
4. **A `keretszo` lista nem állítja magáról, hogy teljes** (34 tétel, gyakoriság alapján
   válogatva). Bővítése az F3 betöltés tapasztalatai alapján várható.
5. **A `CLAUDE.md` mérete** (5,2 KB vs. tervezett 2-3 KB) — felhasználói döntés, hogy
   elfogadható-e, l. F1.1.
6. **Az F0-ból változatlanul nyitott tételek:** az `Atadasi_dokumentum_2026_09_11.md`
   3.5-3.7, 3.9-3.10 szakaszai (Tehóm-duplikáció mint elv, „shem — név szerzése" motívum,
   Segítségül hívni két régi tétele, modellhasználati stratégia, szerzői jogi státusz).
   *A 3.8 — a Sense-szám mező indoklása — az F1.2-vel lezárult.*
   Szintén nyitott a törölt Tehóm-kiterjesztés fájlnév-történetének jelzése (kozmetikai).

**A `main` továbbra sincs push-olva** az `origin`-ra. A terv F0-szakasza ezt kifejezetten
ellenőrizendőként jelöli, mert **az F3 retroaktív betöltés a `main` állapotából indul** —
ha a távoli ág a hivatkozási pont, a push az F3 előfeltétele.

---

# III. rész — F2 fázis (Lekérdező CLI)

**Készült:** 2026.09.14
**Forrás terv:** `ATALAKITASI_TERV.md.md` 6. szakasz F2 pontja, 2. pont (eszközréteg), 4.1 (hétlépéses menet)

---

## Elkészült tételek

### F2.0 — A TAHOT_kivonat.tsv lefedettségének tételes felmérése ✅

A terv előírja, hogy ez legyen az F2 első, a CLI-től független lépése. Elkészült
`eszkozok/tahot_lefedettseg_ellenoriz.py`: mind a 39 ószövetségi könyvre, fejezet- és
versszinten ellenőrzi a kivonatot a kánoni fejezetszámok ellen.

**Eredmény — a korábbi tétel elavultnak bizonyult, egy másik, eddig dokumentálatlan hiány
került elő helyette:**

- A `NYITOTT_FELADATOK.md`-ben és a `SEMA.md`-ben rögzített hiány (1Móz 32, Zsolt
  88/89/140/142, Jóel 3) **nem áll fenn** — mind a hat fejezet teljes egészében jelen van.
  Ezt a `TAHOT_TAGNT_README.md` már korábban dokumentálta pótlásként (2026.08.24 utáni
  frissítés), csak a `SEMA.md` és a `NYITOTT_FELADATOK.md` nem lett ezután frissítve —
  ugyanaz a hibaosztály, mint az F1.6-ban talált elavult tételek.
- **Új, eddig nem dokumentált hiány: Jób 40:1-5 és a teljes Jób 41. fejezet hiányzik**
  a kivonatból (0 sor). Valószínű ok: a Jób könyve 40-41. fejezeteinél ismert héber/angol
  versszámozási eltolódás — ezt a forrás STEPBible-fájlban tételesen még ellenőrizni kell,
  ez **nyitva marad**.
- Mindhárom érintett fájl frissítve: `konkordancia/TAHOT_TAGNT_README.md` (a lefedettségi
  bekezdés kiegészítve), `adat/SEMA.md` 4. pont, `NYITOTT_FELADATOK.md` (a tétel `⏹ JAVÍTVA`
  jelöléssel lezárva, az új Jób-hiány rögzítve).
- **Következmény a proveniencia-mezőre:** a `scope` értéke minden `lekerdez.py`-kimenetben
  `TAHOT-teljes` / `TAGNT-teljes` (soha nem `OT-full` / `NT-full`) — ez a terv 9. pontjának
  kockázat-táblázata és a `SEMA.md` 1.5 pontja szerinti, tudatosan konzervatív címke: a
  kivonat egészére vonatkozik, nem a kánon teljességére. Mivel a mérés szerint a kivonat a
  Jób 41. fejezet kivételével valóban teljes, ez a megkülönböztetés a gyakorlatban ma csak
  egyetlen könyvet érint — de a címke marad, mert a garancia nem esetenkénti, hanem elvi.

### F2.1-F2.7 — `eszkozok/lekerdez.py`, hét működő parancs ✅

A terv 2. pontja nyolc parancsot ír elő; hét elkészült és tesztelt, a nyolcadik (`domen`)
a hiányzó SDBH-import miatt csak a hiány jelzéséig jutott (l. Nyitva maradt tételek).

| Parancs | Lépés | Mit csinál |
|---|---|---|
| `gerinc <szakasz> <szakasz> ...` | 1. | N igehely-tartomány közös Strong-halmaza, `grammatikai_strongok.tsv` szűréssel |
| `scan <strong>` | 3. | teljes TAHOT- vagy TAGNT-scan egy Strong-számra, opcionális `--szakasz` szűkítéssel |
| `kollokacio <strong_a> <strong_b>` | 4. | két Strong együttes előfordulása egy versen belül |
| `igealak <strong>` | 5. | egy Strong minden ragozott alakja, kiejtéssel és glosszal — a binyan-döntés emberi marad |
| `lxx-hid <igehely>` | 6. | egy ÓSZ-igehely LXX-görög szavai + azok ÚSZ-előfordulásai (híd-jelöltek) |
| `tsk <igehely>` | A5 | TSK-kereszthivatkozások, Votes szerint csökkenő sorrendben |
| `karoli <igehely>` | A5 | Károli 1908-szöveg + Károli-KH kereszthivatkozások (4.7 — `karoli_szo` hozzárendeléshez) |

Minden parancs az utolsó sorban szó szerint másolható `proveniencia:`-sort ír ki
(`adat/SEMA.md` 1.5 formátuma szerint).

**Igehely-normalizálás** (`parse_igehely`, `to_step`) — a terv szerint az F2 kötelezettsége:
mindkét irányban kezeli a magyar kanonikus alakot (`1Móz 3:16`) és a STEPBible-alakot
(`Gen.3.16`), a `konkordancia/Konyv_normalizalo_tabla.tsv` alapján. Enélkül a `karoli` és a
`tsk` parancs néma nem-találatot adott volna a STEPBible-natív datasetek felé (ez a kockázat
konkrétan a `Karoli_kereszthivatkozasok.tsv`-t érinti, amely `Gen.1.1` alakban tárolja a
kulcsot).

### F2.8 — Elfogadási teszt, mindhárom próba ✅ (a harmadik korlátozottan)

A terv F2 szakasza három elfogadási próbát ír elő:

1. **`scan H6093`** (itzávón) → `1Móz 3:16`, `1Móz 3:17`, `1Móz 5:29` — **egyezik** a terv
   3 igehelyes elvárásával.
2. **`kollokacio H4390 H2555`** (málé + chámász) → **8 vers**, **`kollokacio H8085 H2555`**
   (sámá + chámász) → **4 vers** — mindkettő **pontosan egyezik** a terv elvárt
   számaival, és a versek listája is egyezik a HAMART-001 study alapjával (1Móz 6:11,
   6:13, Ez 7:23/8:17/28:16, Mik 6:12, Sof 1:9, Zsolt 74:20, illetve Hab 1:2, Jer 6:7/51:46,
   Ézs 60:18).
3. **`domen H0779` (arar) / `domen H7043` (kalal)** → **nem futtatható**, mert az SDBH
   import nem történt meg (`adat/datasetek.tsv`: `allapot=hianyzik`). A parancs ezt
   explicit jelzi (kilépési kód 2, hivatkozással a `NYITOTT_FELADATOK.md`-re), **nem
   fabrikál helyettesítő eredményt** — ez szándékos, a terv 4.4/1 elve szerint ("az üres
   eredmény elfogadható kimenet").

**Kalibrációs melléktermék, nem a hivatalos elfogadási teszt része, de megerősítő jel:**
a `gerinc "1Móz 3" "1Móz 4" "1Móz 6:1-8" "1Móz 6:9-22"` a HAMART-001 esetre **pontosan**
a `SEMA.md` 2.7.6 pontjában rögzített számokat és Strong-listát reprodukálja: 23 elemű
szűretlen metszet, 12 kiszűrt grammatikai Strong, 11 megmaradó gerinc-jelölt
(`H0127, H0430, H0559, H0802, H1121, H1961, H3205, H3605, H3947, H6213, H6440`).

---

## Nyitva maradt tételek

1. **`domen` parancs — blokkolva az SDBH/SDGNT importon.** A parancs váza és a
   `datasetek.tsv`-re támaszkodó előfeltétel-ellenőrzés elkészült, de a tényleges
   domén-lekérdezés (StrongCodes join) csak az import után írható meg. Ez a terv 4.3 és a
   `NYITOTT_FELADATOK.md` már korábban rögzített nyitott tétele — az F2 ezen nem lép túl.
2. **Jób 40:1-5 / Jób 41 hiánya a TAHOT_kivonat.tsv-ben** — l. F2.0. A forrás STEPBible-fájl
   tételes ellenőrzése (hipotézis: héber/angol versszámozási eltolódás a 40-41. fejezetnél)
   nem történt meg ebben a menetben.
3. **`igealak` parancs csak adatot szolgáltat, ítéletet nem** — ez szándékos (a terv szerint
   a binyan-csoportosítás emberi döntés), de következmény: a parancs önmagában nem "teszi
   gépesítetté" az 5. lépést a szó szoros értelmében, csak a nyers adathoz jutást gyorsítja.
4. **`ellenoriz.py` még nem készült el** *(⏹ a `gate.py` fele időközben elkészült, l. IV. rész
   F3.3)* — a terv 2. pontja szerint ezek külön eszközök (audit-subagent / hook), nem az F2
   hatóköre; a `lekerdez.py`-nak nincs saját validáló rétege azon túl, amit a parancsok
   kimenete magától nyújt.
5. **A `lxx-hid` parancs nem szűri a Strong-tiltólistát vagy a grammatikai listát** — szándékosan,
   mert a lépés célja a teljes LXX-szókészlet megmutatása egy adott versre, nem egy gerinc-
   metszet. Ha ez gyakorlatban túl zajos, az F5/F6 tapasztalatai alapján érdemes lehet egy
   `--csak-tartalmi` kapcsolót hozzáadni.
6. **A `main` push-a az `origin`-ra továbbra sincs meghatározva** — ugyanaz a nyitott tétel,
   mint az F1 zárásakor (l. II. rész vége).

---

# IV. rész — F3 fázis (Retroaktív betöltés)

**Készült:** 2026.09.14
**Forrás terv:** `ATALAKITASI_TERV.md.md` 6. szakasz F3 pontja, a lépéstábla F3.0-F3.4 sorai

---

## Elkészült tételek

### F3.0 — Előfeltétel-ellenőrzés ✅

A lépés kérdése: érinti-e az F2.0-ban feltárt TAHOT-hiány (Jób 40:1-5 és a teljes Jób 41,
l. III. rész F2.0) bármelyik olyan igehelyet, amelyet az F3 ténylegesen betölt.

**Az F3 betöltési köre** (a terv F3.1-F3.2 sora szerint): a hét lezárt tematikus study —
`Melkizedek_tematikus.md`, `Segitsegul_hivni_az_Urat_tematikus.md` (könnyű csoport),
`Tehom_tematikus.md`, `Hadesz_Seol_tematikus.md`, `Isten_fiai_Nefilim_Gibborim_tematikus.md`,
`Pneuma_pszukhe_megkulonboztetes_tematikus.md`, `Rafaim_tematikus.md` (nehéz csoport) — plusz
az ISTENTISZT-001 lexikon-oldal (`motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md`).

**Ellenőrzés módja:** mind a nyolc fájl (a hét study + a lexikon-oldal), valamint a hozzájuk
tartozó kereszthivatkozás-naplók (`tematikus_lezart/naplok/*.md`) tételes `Jób`-grep-je,
igehely-tartományra szűrve.

**Eredmény: a hiány egyetlen betöltendő igehelyet sem érint.**

A nyolc fájlban előforduló összes Jób-hivatkozás felsorolva: Jób 1:6, 2:1 (Isten fiai/Nefilim),
Jób 3:8 (Bűn gyűrűzése — ez lezárt, de nem a mostani F3.1-F3.2 könnyű/nehéz körbe tartozó
study, l. megjegyzés lent), Jób 5:5, 5:6-7, 5:8 (Melkizedek naplója), Jób 7:9, 11:8, 14:13,
16:18, 17:13, 17:16, 21:13, 21:17, 22:15, 22:17, 24:19, 26:5, 26:6, 28:14, 31:38, 31:40,
33:27, 38:7, 38:16, 38:30. A legmagasabb fejezetszám, ami ténylegesen előfordul, **Jób 38**
(a Tehóm-study "mélység forrásai" sora) — a hiány (40:1-5, 41) fölött marad egy teljes
fejezettel. Egyetlen betöltendő study vagy a lexikon-oldal sem hivatkozik Jób 40-re vagy
41-re.

*Megjegyzés a Bűn-gyűrűzése studyra:* ez az F0-ban már lezárt HAMART-001 study (nem F3.1/F3.2
tárgya), de a teljesség kedvéért ellenőrizve — a kereszthivatkozás-naplójában szereplő Jób-helyek
(3:8, 5:5-7, 16:18, 21:17, 22:15/17, 31:38/40, 33:27) szintén mind 38. fejezet alattiak.

**Következmény:** nincs explicit hiány-jelölésre szoruló sor, a 3. alapszabály (memória vs.
lekérdezés — hiányt gyenge anyaggal kitölteni tilos) ezen a körön belül nem aktiválódik. Az
F3.1-F3.4 ettől függetlenül futtathatók a TAHOT-hiány miatti kockázat nélkül.

**Fennmaradó, de az F3.0 hatókörén kívüli kockázat:** ha egy jövőbeli teljes ÓSZ-scan
(`lekerdez.py scan`) vagy a hat küszöbön túli, még meg nem írt motívum (HAMART-001-en kívüli
öt) valaha Jób 40-41-et érintő Strong-számra fut, a hiány néma nem-találatot fog adni, mert a
`TAHOT_kivonat.tsv` ott 0 sort tartalmaz — ez nem új felismerés, hanem az F2.0-ban rögzített,
még nyitva álló tétel (l. III. rész, Nyitva maradt tételek 2. pont), amit az F3.0 csak
megerősít, nem old fel.

---

### F3.1 — Könnyű csoport ✅

**Készült:** 2026.09.14
**Forrás terv:** `ATALAKITASI_TERV.md.md` 6. szakasz, F3 lépéstábla F3.1 sora

A terv előírja: Melkizedek + Segítségül hívni betöltése, egy menetben a 4.6 gate
visszamenőleges alkalmazásával és a háromértékű státusz bevezetésével. Az ISTENTISZT-001
study↔lexikon egyesítés vizsgálata megerősítette a terv előfeltevését: a `Segitsegul_
hivni_az_Urat_tematikus.md` és a `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md`
igehely-halmaza **valóban pontosan egyezik (29 = 29)** — a lexikon-oldal táblázata a study
1. pontjának szó szerinti átemelése, kiegészítve PaRDeS-szint/funkció-besorolással —, tehát
ez tiszta egyesítés volt, tartalmi ütközés feloldása nélkül.

**Egyszeri, kézi futtatású betöltő szkript:** `eszkozok/f3_1_betoltes.py` — nem a
`betolt.py`/`lekerdez.py` eszköztár része (azok F2/F4 hatókörébe tartoznak), hanem ennek az
F3.1 menetnek a jegyzőkönyve: a sorokat memóriában állítja össze, **minden sort mezőszám
szerint ellenőriz, mielőtt bármit lemezre írna** — így egy elgépelt mezőszám kivétellel áll
le, nem csendes oszlop-eltolással —, és a kulcs-egyediséget (`id`+`igehely`) is ellenőrzi
írás előtt.

**Betöltött adat:**

| Tábla | KIRALY-001 (Melkizedek) | ISTENTISZT-001 (Segítségül hívni) | Összesen |
|---|---|---|---|
| `motivumok.tsv` | 1 sor | 1 sor | 2 |
| `elofordulasok.tsv` | 9 sor | 29 sor | 38 |
| `jeloltek.tsv` (dontes=beépítve) | 9 sor | 29 sor | 38 |
| `kapcsolatok.tsv` | 9 sor | 23 sor | 32 |

**Forrás az `elofordulasok.tsv`-hez:** a Melkizedek-study 1. pontja + a hozzá tartozó
kereszthivatkozás-napló; a Segítségül hívni-study 1. pontja helyett — mivel gazdagabb,
mezőnként (PaRDeS-szint, funkció, Strong, BDB-jelentés) már tagolt forrás — az
ISTENTISZT-001 lexikon-oldal 1. pontjának táblázata, szó szerint átvéve.

**Proveniencia — tudatos döntés, nem mulasztás.** Mindkét motívum kutatása megelőzte a
`lekerdez.py`-t (F2, 2026.09.14), tehát egyetlen sor sem `lekerdez.py`-kimenet. Az
`adat/SEMA.md` 1.5 pontja szerint ez pontosan a `scope=manual` eset — minden sor
`scope=manual | forras=<study fájl> | ts=<a napló szerint dokumentált dátum>` alakú
provenienciát kapott, a study/napló saját 【NAPLO】-dátumait követve soronként (pl. a
Segítségül hívni 2026.09.05-i eredeti 17 sora `ts=2026-09-05`, a 2026.09.08-i G1941-scan
6 új ÚSZ-sora `ts=2026-09-08`). **Ez nem hamis "ellenőrizve" állítás** — a `manual` érték
explicit jelzi, hogy a Minőségi kapu ezt értelmezésként, nem gépi ténymegállapításként
kezelje (l. `SEMA.md` 1.5, a terv legfontosabb egyetlen szabálya).

**`gerinc_elem` retroaktív kitöltése.** Egyik motívum kutatása sem a hétlépéses
`lekerdez.py`-menettel futott (az még nem létezett), de mindkettő dokumentáltan
lexikai/formulai horgonyon áll: ISTENTISZT-001 minden ÓSZ-sora a H7121+H8034 kollokációs
párra, ÚSZ-sorai a G1941-scan-re (a 2Móz 33:19/34:5 kivétellel, amely ugyanabból a
kollokációs scanből ered, csak funkcionálisan másik BDB-sense alá sorolva); KIRALY-001 sorai
H3548-ra (BDB "priest-king" sense), Zsolt 76:3 H8004-re, a Zsid-sorok G5010-re (τάξις). Egy
sor sem maradt horgony nélkül — az integritási ellenőrzés (l. lent) ezt megerősítette.

**4.6 gate — visszamenőleges alkalmazás:**

| Mező | KIRALY-001 | ISTENTISZT-001 |
|---|---|---|
| `azonossag_tipusa` | lexikai | formulaikus |
| `negativ_kriterium` | Melkizedek névszerinti említése VAGY a BDB H3548 "priest-king" sense — a "chieftain" alkategória (Jetró stb.) explicit kizárva | aktív קָרָא+בְּ szerkezet — a passzív נִקְרָא...עַל (D-minta) kizárva |
| `folerendelt_fogalom` | papi és királyi tisztség kombinációja Melkizedekre hivatkozás nélkül | istentisztelet/imádság általában, a formulán kívül |

A negatív kritériumok mindkét esetnél **már a study-kban is dokumentált, ténylegesen
alkalmazott elhatárolásokból** származnak (KIRALY-001: a BDB "chieftain" alkategória
kizárása; ISTENTISZT-001: a D-minta explicit kizárása) — nem új, utólag kitalált szabályok,
csak a study szövegéből a séma mezőibe emelve.

**Háromértékű státusz.** Mindkét motívum `publikálható` (nem `véglegesített`) lett — ez
tudatos, a `SEMA.md` 2.1.1 saját példáinak megfelelő döntés: pontosan ez a két motívum a
dokumentált bizonyíték arra, hogy a régi "LEZÁRVA" címke félrevezető volt (Melkizedek a
08.22-i lezárás után 09.08-09-én bővült, a Segítségül hívni kétszer is, mindkétszer
**szerkesztői döntés** nyomán, nem csak új lexikai bizonyítékra). A `véglegesített` állapot
— ami kizárná az újbóli szerkesztői döntés általi újranyitást — ezért itt nem indokolt.

**Integritás-ellenőrzés (kézzel, az `ellenoriz.py` hiányában — l. F2 nyitva maradt 4. pont):**
lefuttatva mind a négy `SEMA.md` 3. szakasz szerinti szabályra, ami F3.1 hatókörében
értelmezhető — mind a 38 `elofordulasok` sorhoz van `jeloltek` sor `dontes=beépítve`
értékkel (2. szabály), egyetlen `gerinc_elem` és `proveniencia` mező sem üres (3-4.
szabály), és nincs duplikált `id+igehely` kulcs.

---

### F3.2 — Nehéz csoport ✅

**Készült:** 2026.09.14
**Forrás terv:** `ATALAKITASI_TERV.md.md` 6. szakasz, F3 lépéstábla F3.2 sora

A terv előírja: Tehóm, Hádész/Seól, Isten fiai/Nefilim/Gibborim, Pneuma/pszükhé, Rafaim —
**visszakeresés** a `TAHOT_kivonat.tsv`-ből, szkripttel, nem kézzel; a lefedettségi hiányból
eredő néma nem-találat külön kategóriaként jelentendő, nem keverhető a valódi
nem-találattal; könyvnév-normalizálás kötelező.

**A könnyű csoporttal (F3.1) szembeni különbség:** e öt study háromoszlopos táblázata
(`Igehely | Kapcsolódás | PaRDeS-szint`) — a Strong-szám sehol nincs tabellázva, csak a
study prózájában van megnevezve az az egy-két gyök, amelyen az egész motívum áll (Tehóm:
H8415; Seól: H7585; Rafaim: H7497/H7496; Isten fiai: H1121+H0430/H5303). A feladat tehát
nem kinyerés, hanem **visszakeresés**: minden táblázat-sorra ellenőrizni kell, hogy az adott
igehely valóban tartalmazza-e a motívum lexikai horgonyát a `TAHOT_kivonat.tsv`-ben.

**Egyszeri, kézi futtatású szkript:** `eszkozok/f3_2_betoltes.py` — egyetlen áthaladással
beolvassa a `TAHOT_kivonat.tsv` 468 968 sorát (csak a szükséges Strong-kódokra szűrve),
majd minden ÓSZ-sorra három lehetséges kimenetet állapít meg:

| Kimenet | Jelentés | Talált eset |
|---|---|---|
| `IGAZOLVA` | a vers szerepel a kivonatban, és az elvárt Strong-szám(ok) mind jelen vannak | 138 |
| `TAHOT_HIANYOS` | a vers **egyáltalán nem** szerepel a kivonatban — lefedettségi rés, néma nem-találat | 0 |
| `STRONG_HIANYZIK` | a vers szerepel, de az elvárt Strong-szám hiányzik belőle — valódi anomália | 3 |

**A három kategória nem keveredett.** `TAHOT_HIANYOS` nulla esetben fordult elő — ez a
gyakorlatban azt jelenti, hogy a Jób 40:1-5/41-es hiány (F2.0/F3.0) egyetlen ide tartozó
igehelyet sem érintett, és más lefedettségi rés sem került elő. A 3 `STRONG_HIANYZIK` eset
mindegyike ugyanabból a hibaosztályból ered: a study egy **több-verses tartományt**
(`5Móz 2:10-11`, `5Móz 2:20-21`, `2Sám 21:15-22`) idézett egységként, de a per-vers
szétbontás után kiderült, hogy a רְפָאִים szó ténylegesen csak a tartomány egyik tagjában áll
(ellenőrizve: `5Móz 2:11`, `5Móz 2:20`, `2Sám 21:16`/`21:18` — mind `IGAZOLVA`). A három
üres tagot (`5Móz 2:10`, `5Móz 2:21`, `2Sám 21:15`) a szkript **nem** léptette elő
`elofordulasok`-má, hanem a `jeloltek.tsv`-be irányította `dontes=elutasítva` értékkel, a
konkrét hiányzó Strong-szám megnevezésével.

**Egy negyedik, kézi döntést igénylő eset:** `1Móz 14:6` (חֹרִים, "Hórim") a Rafaim-study saját
táblázatában szerepel ("ugyanabban a hadjáratban legyőzött negyedik népcsoport"), de a
חֹרִים szónak **nincs közös gyöke** a רְפָאִים szócsaláddal (más Strong-szám, H2752). Mivel a
HODIT-001 negatív kritériuma (l. lent) kizárólag a רְפָאִים-rokon népneveket engedi be, ez a
sor sem lépett elő — `jeloltek.tsv`-ben maradt, `dontes=nyitva`, indokolással.

**Könyvnév-normalizálás:** nem volt rá szükség — a `TAHOT_kivonat.tsv` már eleve magyar
kanonikus alakban (`1Móz 14:5`) tárolja az igehelyet (l. `adat/SEMA.md` 1.1), ezért a
`Konyv_normalizalo_tabla.tsv` STEPBible↔magyar konverziója ezen a datasetnél nem
alkalmazandó — ez maga is dokumentálandó, mert a terv 1.1 pontja szerint másik három dataset
(`Karoli_kereszthivatkozasok.tsv`, `Karoli_Strong_kivonat.tsv`, `TIPNR_kivonat.tsv`) igenis
STEPBible-alakot használ, tehát a normalizálás-mentesség dataset-specifikus, nem általános.

**Betöltött adat:**

| ID (motívum) | study | `elofordulasok` sor | ebből ÚSZ (Strong a study prózájából, TAHOT-visszakeresés nélkül) |
|---|---|---|---|
| TEREMT-001 (Tehóm) | `Tehom_tematikus.md` | 41 | 7 (G0012, ábüsszosz) |
| ALVIL-001 (Hádész/Seól) | `Hadesz_Seol_tematikus.md` | 72 | 8 (G0086, hádész) |
| MENNY-001 (Isten fiai/Nefilim) | `Isten_fiai_Nefilim_Gibborim_tematikus.md` | 9 | 3 (nem lexikai, l. lent) |
| ANTROP-001 (Pneuma/pszükhé) | `Pneuma_pszukhe_megkulonboztetes_tematikus.md` | 8 | 7 (görög, eleve NT) |
| HODIT-001 (Rafaim) | `Rafaim_tematikus.md` | 33 | 0 |
| **Összesen** | | **163** | |

Mindegyik sorhoz `jeloltek.tsv` sor is készült (`dontes=beépítve`), plusz a 4 elutasított/
nyitva hagyott eset — összesen **167 `jeloltek` sor**.

**A MENNY-001 három ÚSZ-sora (Júd 1:6, Júd 1:14-15, 2Pét 2:4-5) nem lexikai horgonyon áll** —
a study saját szövege explicit kimondja, hogy ezek "tematikus/szerkezeti, NEM közös lexikai
gyök" kapcsolatok. A `gerinc_elem` mező ezért nem Strong-számot, hanem a study saját,
megnevezhető horgonyát kapta (`referencia:1Énokh 10:4-6/…`, `idézet:1Énokh 1:9`,
`formula:οὐκ ἐφείσατο`) — üres `gerinc_elem` egyik sornál sem maradt, de ez a három sor
formálisan más horgony-típusú, mint a motívum lexikai magja.

**`motivumok.tsv` — öt új sor, a 4.6 gate mezőivel és háromértékű státusszal.** A terv F3.2
sora nem írja elő explicit a gate alkalmazását (csak F3.1-nél szerepel), de a
`motivumok.tsv` sémája szerint az `azonossag_tipusa`/`negativ_kriterium`/
`folerendelt_fogalom` **kötelező** mező minden `publikálható`/`véglegesített` motívumnál (l.
`SEMA.md` 3.6. integritási szabály) — ezért mind az öt kapott gate-mezőt, a study-k saját,
már dokumentált elhatárolásaiból építve (pl. HODIT-001 negatív kritériuma pontosan az a
szabály, ami az imént a Hórim-sort kizárta — nem utólag kitalált teszt, hanem a study saját
2. pontjának tétele: "a Refáim szótő teljesen elkülönül a gibborim/nefilim szócsaládtól").
Mind az öt `publikálható` állapotú (nem `véglegesített`) — egyik motívum sem zárult le úgy,
hogy kizárt legyen a jövőbeli, csak szerkesztői szándékból eredő újranyitás.

**Integritás-ellenőrzés (kézzel):** mind a 163 `elofordulasok` sorhoz van `jeloltek` sor
`dontes=beépítve` értékkel, egyetlen `gerinc_elem` vagy `proveniencia` mező sem üres, és
nincs duplikált `id+igehely` kulcs (ellenőrizve a teljes, F3.1+F3.2 utáni táblára).

---

### F3.3 — A `gate.py` első futtatása ✅

**Készült:** 2026.09.14
**Forrás terv:** `ATALAKITASI_TERV.md.md` 6. szakasz, F3 lépéstábla F3.3 sora; 2. pont
(eszközréteg); 4.6 (motívum-gate)

A terv előírja: `gate.py` első futtatása a 14 meglévő ID-n, ütközés- és
részhalmaz-jelentésre — **a jelentés kimenet, nem döntés.**

**A `gate.py` eddig nem létezett** (az F2 nyitva maradt tételei között szerepelt, l. III.
rész). Elkészült `eszkozok/gate.py`: beolvassa az `adat/motivumok.tsv` + `adat/
elofordulasok.tsv` táblákat, és minden motívumpárra két vizsgálatot végez —

1. **ütközés-jelentés:** mely igehelyek szerepelnek egynél több motívum táblájában, és
   mekkora az átfedés motívumpáronként;
2. **részhalmaz-ellenőrzés:** B ⊆ A (B minden előfordulása A-ban is megvan) — a 4.6 gate
   4. kérdésének gépi támasza.

Eredményét Markdown-jelentésbe írja (`--md` kapcsoló); a fájl a `motivumlog/
gate_jelentesek/` alá kerül, generált-jelöléssel (`<!-- GENERÁLT: eszkozok/gate.py -->`),
mert **kimeneti réteg**, nem `adat/` — az `adat/` kizárólag a hét kanonikus táblát tartja,
nem levezetett jelentéseket (l. `CLAUDE.md` rétegtáblázata).

**A 14 helyett 7 ID-n futott — ez a jelentés maga is dokumentálja (4. szakasza).** A
`motivumok.tsv`-ben ma csak az F3.1+F3.2-ben betöltött hét ID van (KIRALY-001,
ISTENTISZT-001, TEREMT-001, ALVIL-001, MENNY-001, ANTROP-001, HODIT-001) — a további hét,
a `motivumlog/PaRDeS_motivumok.md`-ben dokumentált ID (HAMART-001, ANTROP-002, ANTROP-003,
ANTROP-004, ISTENTISZT-002, SZOVETS-001, TEREMT-002) még nincs betöltve az `adat/`
táblákba — ez utóbbiak közül négy még meg sincs írva tematikus study-ként (l.
`NYITOTT_FELADATOK.md`), a HAMART-001-nek pedig van lezárt study-ja
(`Bun_kovetkezmenyeinek_gyuruzese_tematikus.md`), de az a terv F3 betöltési körén (a hét
lezárt study + ISTENTISZT-001 lexikon) kívül esett — betöltése nem volt sem az F3.1, sem az
F3.2 hatóköre. A `gate.py` így most **részleges** képet ad; teljes lefedettséghez a
fennmaradó ID-k betöltése szükséges (nem e lépés feladata).

**Eredmény — `motivumlog/gate_jelentesek/gate_jelentes_F3.3.md`:**

| Ütközés | Osztozó igehelyek | Jelleg |
|---|---|---|
| ALVIL-001 ↔ HODIT-001 | Péld 9:18; Ézs 14:9 | mindkettő a study-k saját szövegében már dokumentált, tudatos együttállás (a seól-motívum mindkét helyen kifejezetten a Refáim-kontextusra hivatkozik) |
| ALVIL-001 ↔ TEREMT-001 | Ez 31:15 | valódi kettős lexikai előfordulás — a vers mindkét szót (שְׁאוֹל **és** תְּהוֹם) tartalmazza, mindkét study 2/b-scanje önállóan, egymástól függetlenül találta meg |
| HODIT-001 ↔ MENNY-001 | 4Móz 13:34 | a `נְפִלִים` szó közös horgony, de a study-k szerint eltérő funkcióval: MENNY-001-nél a nefilim-eredetkérdés, HODIT-001-nél az Anákim-azonosítás — ez a 4.6 gate 3. kérdése szerint (*különbözik-e a funkció?*) éppen a megengedett eset, nem ütközés-hiba |

**Részhalmaz-viszony egy párnál sem került elő** — egyik betöltött motívum sem B ⊆ A
viszonyban áll egy másikkal, tehát a hét betöltött ID közül egyik sem gyanús arra, hogy
valójában egy másik ↳ alpontja legyen.

**A jelentés nem zár le semmit — ez szándékos.** A három ütközés mindegyike a study-k saját,
már korábban is dokumentált tényeire mutat rá (nem új felfedezés), és egyik sem igényel
azonnali szerkesztői beavatkozást: a 4.6 gate 3. kérdése szerint az osztozás önmagában nem
hiba, ha a funkció különbözik — ez mindhárom esetben így van. A jelentés ennek ellenére
rögzíti őket, mert **a gépi megerősítés maga az érték** (eddig ez csak a kutató fejében élt).

---

### F3.4 — A Károli-Strong join visszamenőleges pótlása ✅

**Készült:** 2026.09.14
**Forrás terv:** `ATALAKITASI_TERV.md.md` 4.7 pont, a 6. szakasz F3 lépéstáblájának F3.4
sora, és a 10. szakasz **D24** döntése (a `karoli_szo` minden jelöltnél *megnézendő*, de
csak a beépített sorokon *őrzendő meg*)

A terv ezt a lépést külön, Opus-menetre különíti el, mert **soronkénti, tartalom-alapú
ítélet** — a Károli-szóalak hozzárendelése egy Strong-számhoz nem gépesíthető. A gépesített
rész itt csak az előkészítés (versszöveg-előszedés, könyvnév-normalizálás) és az
utóellenőrzés; az ítélet mind a 191 sornál egyedi, és auditálhatóan rögzítve van az
`eszkozok/f3_4_dontesek.tsv`-ben.

**A hatókör a D24 szerint.** A 4.7 két körben határozza meg a pótlást (a 2026.09.10-i négy
scan minősített találatai; ami a hét lezárt study előfordulás-táblájában szerepel, de a
join-táblában nem). A D24 ezt a `adat/` rétegre fordítja le: a triplet
(`karoli_szo` + `azonositas_modja` + `megbizhatosag`) **kötelező minden beépített
`elofordulasok.tsv`-soron**. A mért kiindulás: a 201 sorból **10-en volt** kitöltve (a már
meglévő join-táblából örökölve az F3.1-ben), **191-en hiányzott** — ez lett az F3.4
tényleges köre.

| Motívum | Hiányzó sor | Gerinc-elem |
|---|---|---|
| ALVIL-001 | 72 | H7585 (64) + G0086 (8) |
| TEREMT-001 | 41 | H8415 (34) + G0012 (7) |
| HODIT-001 | 33 | H7497 (24) + H7496 (8) + H5303 (1) |
| ISTENTISZT-001 | 21 | H7121+H8034 |
| MENNY-001 | 9 | H1121+H0430 (4) + H5303 (2) + 3 nem lexikai horgony |
| ANTROP-001 | 8 | G4151+G5590 (7) + H5315+H2416 (1) |
| KIRALY-001 | 7 | H3548 (2) + H8004 (1) + G5010 (4) |

**A menet négy lépése.**

1. `eszkozok/f3_4_munkalap_general.py` — minden hiányzó sorhoz kiszedi a Károli-versszöveget
   (`Karoli_1908.tsv`), vers-tartományt kibontva. **Könyvnév-normalizálás kötelező:** az
   `elofordulasok.tsv` négy helyen teljes könyvnevet visel (`Jelenések`, `Lukács`, `Máté`,
   `Róma`), a Károli-tábla rövidet (`Jel`, `Luk`, `Mt`, `Róm`) — normalizálás nélkül 17 sor
   **néma nem-találatot** adott volna, nem hibát.
2. `eszkozok/f3_4_nema_nemtalalat.py` — gépi előszűrő: melyik versben **nem** szerepel a
   Strong egyetlen ismert magyar visszaadása sem. Ez a szűrő fogta meg azt a két esetet,
   amelyet kézzel ki lehetett volna tölteni rossz szóval (l. alább).
3. A soronkénti ítélet → `eszkozok/f3_4_dontesek.tsv` (191 sor) és
   `eszkozok/f3_4_extra_join.tsv` (7 sor: egy igehelyhez több Strong, illetve
   vers-tartomány további versei).
4. `eszkozok/f3_4_join_potlas.py` írja mind a három táblát; `eszkozok/f3_4_ellenoriz.py` és
   `eszkozok/f3_4_zaro_ellenoriz.py` ellenőriz.

**Eredmény.**

| Tábla | Változás |
|---|---|
| `adat/elofordulasok.tsv` | 191 sor kapott `karoli_szo` tripletet — **üres már egy sincs** (201/201); 3 sor `strong`-pótlást |
| `adat/jeloltek.tsv` | 201 `beépítve` sor kapta meg a tripletet (SEMA 2.2: innen öröklődik); 25 elcsúszott sor javítva |
| `konkordancia/Karoli_Strong_kivonat.tsv` | **227 → 383 sor** (156 új); 161 → 309 egyedi igehely; 156 → 171 egyedi Strong; 25 → 29 forrás-tanulmány |

A megbízhatóság megoszlása a teljes join-táblán: **370 `magas`, 13 `közepes`** (a kiindulás
222/5 volt). A 13 közepes mindegyike meg van indokolva a `dontesek.tsv` `megjegyzes`
oszlopában — jellemzően ott, ahol Károli nem a szokásos szóval adja vissza a gyököt
(Zsolt 33:7 *a hullámokat*, Zsolt 104:6 *Vízáradattal*, Zsolt 107:26 *a fenékig*,
Hab 3:10 *a víz-ár*, Ézs 12:4 *magasztaljátok az Ő nevét*), vagy ahol a héber maga
kétértelmű (Ézs 7:11 *a mélységben* — a `שְׁאָלָה` szójáték).

**A feltárt hiány mértéke igazolódott.** A 4.7 mérése szerint a `Hadesz_Seol_tematikus.md`
mindössze négy sorral szerepelt forrásként, holott a H7585-scan 63 új verset hozott — az
F3.4 után ez a study **72 join-sort** ad. A 4.7 által név szerint hiányolt hat sor
(Rafaim H7497: Józs 15:8, 17:15, 18:16; Tehóm H8415: Zsolt 36:7, 77:17, Jón 2:6) és a
kiemelt Hádész-lelet (Hós 13:14) mind bekerült.

#### Amit a soronkénti ítélet feltárt — négy lelet

Ezek nem melléktermékek: pontosan az a fajta hiba, amit csak a tételes, tartalom-alapú
végigmenés hoz elő, és amiért a terv külön menetet szánt erre a lépésre.

**(1) Két új Károli-adatminőségi anomália — vers-eltolódás.** A néma-nem-találat szűrő két
sort emelt ki, mindkettő ugyanabból az összeolvadás-hibaosztályból, amelyre a
`Karoli_adatminosegi_anomaliak.tsv` hét `JAVITVA` tétele is épült:

- **Jób 17** — a `Karoli_1908.tsv` 17. fejezete 15 verset tartalmaz 16 helyett, mert a
  `Jób 16:22` sor két verset olvaszt egybe. A szabványos `Jób 17:16` szövege a fájlban
  `Jób 17:15` alatt áll (*„Leszáll az majd a sír üregébe"*).
- **Préd 9** — a fejezet **két** verssel el van tolva: a fájl `Préd 9:1` sora a szabványos
  `Préd 8:16` szövegét hozza, és a szabványos `Préd 9:10` (*„nincs a Seolban"*) a fájlban
  `Préd 9:12` alatt áll.

Mindkettő felvéve a `konkordancia/Karoli_adatminosegi_anomaliak.tsv`-be
`AZONOSITVA, NEM JAVITVA` állapottal — a szétbontás MEK-forrás tételes ellenőrzését
igényli, mint a korábbi javításoknál, és ez az F3.4-en kívül esik. A két érintett join-sor
a **szabványos** igehely alatt, `közepes` megbízhatósággal került be.

*Amiért ez fontos:* eltolódás esetén a naiv kitöltés nem hibát ad, hanem **rossz szót a
helyes igehelyhez** — a Préd 9:10-re *„A te ruháid mindenkor legyenek fejérek"* jött volna
vissza. Ezt nem fegyelem fogta meg, hanem a 2. lépés gépi szűrője.

**(2) Oszlop-eltolódás a `jeloltek.tsv`-ben — az F3.1 betöltő hibája, 25 sor.** A
`karoli_szo` oszlopba az `elofordulasok.tsv` `jelentes_hu` értéke került, és emiatt minden
következő mező eggyel odébb csúszott: `azonositas_modja` ← `karoli_szo`,
`megbizhatosag` ← `azonositas_modja`, `datum` ← `datum` — a `megbizhatosag` értéke pedig
elveszett. Az eltolás-hipotézis mind a 25 soron tételesen igazolódott (nincs kivétel), így
a javítás gépi volt. Példa: a `2Móz 19:6` sor `karoli_szo` mezője
*„egyszerre papok és királyok a nemzetekhez való viszonyukban"* volt *„papok"* helyett.

*Amiért ez F3.4 dolga volt, nem külön köré:* a helyes értéket nem lehet olyan oszlopba
írni, amelyben rossz adat áll. A séma szerint (SEMA 2.2) az `elofordulasok.karoli_szo`
**a `jeloltek` azonos kulcsú sorából öröklődik** — az öröklés forrása volt hibás.

**(3) Három Strong-szám a Zsid 7:3-nál — a study saját hivatkozása téves.** A
`Melkizedek_tematikus.md` táblázata és a kereszthivatkozás-naplója a `G0813/G0282/G0035`
hármast rendeli az *ἀπάτωρ / ἀμήτωρ / ἀγενεαλόγητος* szavakhoz. A `TAGNT_kivonat.tsv`
tételes ellenőrzése szerint az *ἀπάτωr* Strong-száma **G0540**, nem G0813 (a G0813 az
*ἄτακτos*, „rendetlen"), és az `elofordulasok.tsv` `bdb_entry_id` mezője
(`G5010+G0813+G0282`) a G0035-öt egyáltalán nem tartalmazza. A join-táblába ezért a TAGNT
által megerősített hármas került (`Heb.7.3`: G0540 *Apa nélkül*, G0282 *anya nélkül*,
G0035 *nemzetség nélkül való*), a study saját hivatkozása viszont **változatlan maradt** —
javítása tartalmi döntés, nem a join dolga (l. Nyitva maradt tételek).

**(4) A `G4151+G5590` gerinc-elem két ANTROP-001 sornál nem a versben álló szót nevezi
meg.** Az 1Kor 2:14-ben nem a `G5590` (*ψυχή*) áll, hanem a `G5591` melléknév
(*ψυχικός*, Károli: *„Érzéki"*), a 2:15-ben pedig nem a `G4151`, hanem a `G4152`
(*πνευματικός*, Károli: *„A lelki ember"*). A join-sor a ténylegesen a versben álló
Strong-számot kapta.

*Két további, tartalmilag beszédes lelet ugyanebből a csoportból* — ezek nem hibák, hanem
a Pneuma/pszükhé-study saját tézisét erősítő adatok, amelyek eddig nem voltak
adat-szinten rögzítve: a **Zsid 4:12**-ben Károli a `ψυχή`-t *„szív"*-nek adja vissza
(*„a szívnek és léleknek"*), az **1Thessz 5:23**-ban a `πνεῦμα`-t *„valótok"*-nak — az
**1Kor 15:45** viszont **az egyetlen hely, ahol Károli a `πνεῦμα`-t *„szellem"*-nek
fordítja**. A Luk 1:46-47 párhuzamában pedig mindkét görög szó ugyanazt a magyar
*„az én lelkem"* alakot kapja.

#### Két szerkezeti döntés, amelyet a lépés meghozott

**A nem lexikai horgonyú sorok.** Három MENNY-001 sor horgonya nem Strong-szám
(`referencia:1Énokh 10:4-6`, `idézet:1Énokh 1:9`, `formula:οὐκ ἐφείσατο`). A D24 szerint a
`karoli_szo` a beépített sorokon kötelező, a join-tábla viszont Strong-kulcsú. A megoldás
soronként külön:

- **2Pét 2:4-5** — a formula-horgony *mögött* van Strong: a TAGNT szerint az
  *οὐκ ἐφείσατο* hordozó szava a **G5339** (*φείδομαι*). Károli: *„nem kedvezett"* (2:4),
  *„sem kedvezett"* (2:5). Ez tehát **rendes join-sort kapott**, `magas` megbízhatósággal.
- **Júd 1:6 és Júd 1:14-15** — itt nincs szó-szintű megfelelés, csak a horgonyt hordozó
  mondat. A `karoli_szo` ezért a mondatot kapta, `azonositas_modja=kikövetkeztetett`,
  `megbizhatosag=közepes`, és **join-sor nem keletkezett**. A D24 így teljesül (az ítélet
  megszületett és rögzült), a join-tábla Strong-kulcsú szerkezete pedig sértetlen marad.

**Három `strong` nélküli KIRALY-001 sor pótolva.** A Zsid 5:6, 5:10 és 6:20 `gerinc_elem`-e
`G5010` volt, a `strong` oszlop viszont üres — ez az F3.3 zárásának 3. nyitott tétele. A
pótlás nem új állítás, csak átemelés a már kitöltött mezőből, és **az F3.4-nek szüksége
volt rá**: Strong nélkül nincs join-sor. A másik három `strong` nélküli sor (a fenti
MENNY-001 hármas) helyesen maradt üres.

#### Ellenőrzés

Az `eszkozok/f3_4_ellenoriz.py` a döntés-táblát ellenőrzi (fedi-e pontosan a 191 hiányzó
sort, duplikátum nélkül; és a megadott `karoli_szo` ténylegesen szerepel-e a hivatkozott
Károli-versben, a két ismert eltolódást figyelembe véve) — **0 eltérés**. Az
`eszkozok/f3_4_zaro_ellenoriz.py` a három tábla utólagos integritását nézi: nincs üres
`karoli_szo` a beépített sorokon, nincs triplet-töredék, nincs duplikált join-kulcs, minden
új igehely szabályos STEPBible-alakú, a `jeloltek` és az `elofordulasok` `karoli_szo`
mezője **mind a 201 soron egyezik**.

A záró ellenőrzés egyetlen hiba-osztályt jelez, és az **nem az F3.4 sorain van**: 26 régi
join-sor (mind a 182. sor előtt, korábbi genezisi tanulmányokból) nem nullázott
Strong-számot visel (`H430`, `H779`, `H8414+H922`…), ami sérti a SEMA 1.2-t. Változatlanul
hagyva — l. Nyitva maradt tételek.

---

## Nyitva maradt tételek

1. ⏹ **LEZÁRVA (F3.4, 2026.09.14).** A Károli-Strong join visszamenőleges pótlása lefutott:
   191 sor kapott `karoli_szo` tripletet, a join-tábla 227 → 383 sorra nőtt. Az F3 mind az
   öt lépése megvan.
2. **A `gate.py` csak a betöltött hét ID-t látta, nem mind a 14-et.** A további hét ID
   (HAMART-001, ANTROP-002, ANTROP-003, ANTROP-004, ISTENTISZT-002, SZOVETS-001,
   TEREMT-002) nincs betöltve az `adat/` táblákba — ebből négy még meg sincs írva
   tematikus study-ként, a HAMART-001-nek pedig van lezárt study-ja, de az kívül esett a
   terv F3 betöltési körén (a hét lezárt study + ISTENTISZT-001 lexikon). A `gate.py`
   jelentése ezért **részleges** — ha a fennmaradó ID-k valaha betöltésre kerülnek, a
   jelentést újra kell futtatni.
3. **A `gate.py` három talált ütközése (ALVIL-001↔HODIT-001, ALVIL-001↔TEREMT-001,
   HODIT-001↔MENNY-001, l. F3.3) emberi megerősítést nem kapott.** A jelentés kimenet, nem
   döntés — egyik esetet sem zárta le, csak megnevezte és a 4.6 gate keretébe helyezte.
4. **A HODIT-001 negatív kritériuma szerint elutasított `1Móz 14:6` (Hórim) és a 3
   `STRONG_HIANYZIK` eset (`5Móz 2:10`, `5Móz 2:21`, `2Sám 21:15`) emberi felülvizsgálatra
   várnak** — a szkript indoklással a `jeloltek.tsv`-be irányította őket, de a végső döntés
   (véglegesen elutasítva marad-e, vagy a study saját tartomány-idézése frissítendő) emberi
   megerősítést igényel.
5. **A Rafaim/HODIT-001 és a Seól/ALVIL-001 táblák nem kaptak `kapcsolatok.tsv` sort** — az
   F3.2 a terv szövege szerint kizárólag a visszakeresésről szól, a `kapcsolatok` réteg
   (pl. Ézs 14:9 rafaim↔seól együttállása, vagy a Hós 13:14 → 1Kor 15:55 páli idézet)
   kitöltése nem volt e lépés hatóköre — nyitva marad egy későbbi körre.
6. **A Segítségül hívni-study 1Kir 18:24 belső Kontraszt-esete nem került a
   `kapcsolatok.tsv`-be.** Ez nem mulasztás, hanem a séma dokumentált korlátja (l.
   `SEMA.md` 2.3 „Ismert névütközés" doboza): a `forras_igehely`+`cel_igehely` kulcs két
   *különböző* igehelyet feltételez, egy versen belüli kontrasztot (Baál neve vs. YHVH neve,
   ugyanabban a 1Kir 18:24 versben) nem tud natívan ábrázolni. Nyitott kérdés marad a
   `Bibliai_Motivumlexikon_tervezesi_naplo.md` KAPCSOLATOK-fejezete felé.
7. ⏹ **LEZÁRVA (F3.4, 2026.09.14).** A `karoli_szo` korábban csak a már meglévő
   join-sorokból öröklődött (10 sor); az F3.4 után mind a 201 beépített `elofordulasok`-sor
   ki van töltve. A `NYITOTT_FELADATOK.md` „három KIRALY-001 sor `strong` nélkül" tétele
   szintén lezárva: a `G5010` átemelve a `gerinc_elem`-ből, mert Strong nélkül nincs
   join-sor.
8. **A `motivumok.tsv` `sablon_verzio` mezője a study fejlécének saját állítását kapta**
   mind a hét ID-nél, nem egy frissen lefuttatott F5-ös megfelelőségi kör eredményét (az F5
   még nem történt meg). Ha az F5 sablon-frissítés (a terv 123. sorának javítása)
   megtörténik, ez a mező felülvizsgálandó.
9. **A Jób 40-41 STEPBible-forrásfájl tételes ellenőrzése** (a feltételezett héber/angol
   versszámozási eltolódás hipotézise) továbbra sem történt meg — ugyanaz a nyitott tétel,
   mint az F2.0 zárásakor. **Az F3.4 két új eltolódást talált a Károli-oldalon** (Jób 17,
   Préd 9, l. 10. tétel); a kettő független — az egyik a STEPBible-forrás, a másik a
   `Karoli_1908.tsv` hibája —, de ugyanazt a tanulságot hordozzák.

**Az F3.4-ben felmerült új tételek (2026.09.14):**

10. **A `Karoli_1908.tsv` két azonosított, de nem javított vers-eltolódása.** `Jób 17` (egy
    verssel) és `Préd 9` (két verssel) — mindkettő felvéve a
    `konkordancia/Karoli_adatminosegi_anomaliak.tsv`-be `AZONOSITVA, NEM JAVITVA`
    állapottal. A szétbontás MEK-forrás tételes ellenőrzését igényli, mint a korábbi hét
    javított tételnél. **Amíg nincs javítva, minden `Jób 17:*` és `Préd 9:*` hivatkozás
    néma nem-találatot vagy rossz verset ad a Károli-táblán.** A két érintett join-sor
    `közepes` megbízhatósággal került be. *Érdemes megnézni, hány további fejezet érintett:
    az `eszkozok/f3_4_nema_nemtalalat.py` mintája (Strong → ismert magyar visszaadások)
    általánosítható a teljes join-táblára.*
11. **A `Melkizedek_tematikus.md` Zsid 7:3-as Strong-hármasa téves, javítása nyitva.** A
    study táblázata és kereszthivatkozás-naplója `G0813`-at ír *ἀπάτωρ*-ra; a
    `TAGNT_kivonat.tsv` szerint az helyesen **G0540** (a G0813 az *ἄτακτος*). Az
    `elofordulasok.tsv` `bdb_entry_id` mezője (`G5010+G0813+G0282`) ráadásul a `G0035`-öt
    sem tartalmazza. A join-táblába a TAGNT-igazolt hármas került; **a study és az
    `elofordulasok` sor javítása tartalmi döntés, emberi megerősítést kér.**
12. **Az `elofordulasok.tsv` `G4151+G5590` gerinc-eleme két ANTROP-001 sornál pontatlan.**
    Az 1Kor 2:14-ben `G5591` (*ψυχικός*), a 2:15-ben `G4152` (*πνευματικός*) áll — nem a
    főnevek. A join-sorok a versben ténylegesen álló Strong-számot viselik, a `gerinc_elem`
    viszont változatlan maradt. Döntendő: a gerinc-elem a motívum *magját* nevezi-e meg
    (akkor helyes így), vagy a soron ténylegesen álló szót (akkor javítandó).
13. **26 régi join-sor nem nullázott Strong-számot visel** (`H430`, `H779`, `H8414+H922`…),
    ami sérti a `SEMA.md` 1.2-t („a nullázás kötelező — `H779` nem érvényes érték, mert a
    datasetek rendezése így rendezi"). Mind a 26 korábbi genezisi tanulmányokból való,
    egyik sem F3.4-es sor. A javítás mechanikus, de más tanulmányok sorait érinti, és egy
    esetleges `grep H779` hívást elnémítana — ezért **nem az F3.4 végezte el**.
14. **A 3 `elutasítva` és 17 `nyitva` jelölt-sor `karoli_szo` mezője üres.** Ez a D24
    szerint megengedett (a mező csak a beépített sorokon kötelező), és a 4.7 hatókörén is
    kívül esik (az a ténylegesen feldolgozott igehelyekre szól). A D24 első fele viszont
    azt mondja, hogy a Károli-szót **minden** jelöltnél meg kell nézni, mert az ítélethez
    kell — ezeknél a soroknál ez nem történt meg, mert maga az ítélet nyitott.
    Felülvizsgálandó, amikor a 20 sor minősítése megtörténik.
15. **A `kikövetkeztetett` azonosítási mód első két használata felülvizsgálatra ajánlott.**
    A Júd 1:6 és Júd 1:14-15 sor `karoli_szo` mezője nem szóalak, hanem a horgonyt hordozó
    mondat — ez a mező eredeti jelentésének (*„a Károli-szóalak ezen a helyen"*) tágítása.
    Alternatíva volna egy külön mező vagy a mező üresen hagyása; a jelenlegi megoldás a D24
    „minden beépített soron kötelező" felét tartja, a `közepes` megbízhatóság és a
    `kikövetkeztetett` mód pedig greppelhetővé teszi mindkét sort.

---
