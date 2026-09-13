# Megvalósítási napló — F0-F1 fázis

**Készült:** 2026.09.13
**Forrás terv:** `ATALAKITASI_TERV.md.md`, 6. szakasz
**Fázisok:** F0 — Blokkolók feloldása (8 tétel) · F1 — Séma és belépési pont (6 tétel)
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

#### Kalibráció — és amit megmutat

A HAMART-001 metszetét gépileg újraszámoltam (1Móz 3 ∩ 4 ∩ 6:1-8 ∩ 6:9-22):
**pontosan 23**, egyezik a terv 4.1 pontjával. A szűrőn átengedve:

| | |
|---|---|
| metszet | **23** |
| kiszűrve (7 `H9xxx` + `H0853` + `H0834`) | **9** |
| **marad** | **14** |

*Összevetés:* az első, 183 soros változat ugyanezen az eseten 23 → 3-at adott (87%
zajszűrés); a mostani 23 → 14 (39%). A különbséget a most kihagyott keretszó-kategória
teszi ki.

⚠️ **A megmaradó 14 nem mind tartalmi szó — ez a lista ismert hiánya.** Három közülük
tiszta funkciószó, pontosan olyan, mint a három felvett kézi tétel, csak szabadon álló
alakban: **`H0413`** (אֶל, „felé"), **`H5921`** (עַל, „-on, fölött"), **`H3588`**
(כִּי, „mert, hogy"). A `H9xxx` a *prefixált* elöljárókat fedi le (בְּ, לְ, מִן, כְּ),
a *szabadon álló* héber elöljárókat és kötőszókat viszont senki — miközben a görög oldal
12 elöljárót és 6 kötőszót tételesen felsorol. **Az aszimmetria nem elvi, hanem a kézi
lista terjedelméből adódik; felhasználói döntést igényel, hogy bővüljön-e.**

A maradék tizenegy tartalmi vagy keretszó, köztük a tanulmány saját lelete (`H0127`
*adamá*), valamint `H0430` *Elohim* és `H3205` *jalad* — ezek helyesen maradnak benn.

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
| szűrő-kalibráció ugyanazon az eseten | **23 → 14, a lelet megmarad** (l. F1.4) |
| TILTOLISTA-őrző élesben (H3068 beszúrása) | **hibával leáll, kilépési kód 1** |
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
