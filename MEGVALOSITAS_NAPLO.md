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

**183 sor.** A fájl **generált**, nem kézzel írt: `eszkozok/grammatikai_strongok_general.py`
állítja elő a `TAHOT_kivonat.tsv` + `Strong_szotar.tsv` párosból, plusz két gondozott
listából, amelyek a szkript forrásában élnek. Determinisztikus — újrafuttatva bitre azonos
(a timestamp-sor kivételével), ellenőrizve.

| kategória | sor | kizárás |
|---|---|---|
| `affixum` (H9xxx prefixum/szuffixum/névmási elem) | 44 | `mindig` |
| `funkcioszo` (a Strong-szótár szófaji mezője szerint) | 93 | `mindig` |
| `keretszo` (elbeszélői keretszavak) | 34 | **`jelzes`** |
| `kivetel` (motívum-hordozó, nagy gyakoriságú) | 12 | **`soha`** |

⚠️ **Eltérés a tervtől — indokolt.** A terv 1.A táblázata a fájlt egyetlen `Strong`
kulccsal írja le, tehát puszta kizárási listaként. **Ez a megvalósításnál kevésnek
bizonyult**, ezért a `kizaras` mező **háromértékű**. Az indok nem elméleti — két
dokumentált ellenpélda a projekt saját anyagából:

- **H8085 (*sámá*, „hallani")** elbeszélői keretszó, **de** a *sámá + chámász* kollokáció
  egyik tagja, amelynek négy találata **az F2 elfogadási tesztje**.
- **H1121 (*bén*, „fiú")** szintén keretszó, **de** a *bené ha-elohim* szerkezet hordozója,
  azaz a MENNY-001 lexikai magja.

Ha ezek némán kiesnének, a szűrő nem zajt távolítana el, hanem **leletet**. Ezért a
keretszavak `jelzes` értéket kapnak: megjelennek, megjelölve, és explicit döntést kérnek.
A `kivetel` kategória pedig azért kell, mert a védett szavak nagy gyakoriságúak
(H3068 *JHVH* 6 528, H0430 *Elohim* 2 603, H8034 *sém* 864) — egy későbbi, gyakoriság-alapú
listabővítés különben **be is söpörné őket**.

**Kalibrációs teszt — a HAMART-001 eset, gépileg újrafuttatva.** A terv 4.1 pontja szerint
a metszet 23 közös Strong-számot adott, amelyből egyetlen tartalmi szó maradt (*adamá*).
A metszetet újraszámoltam (1Móz 3 ∩ 4 ∩ 6:1-8 ∩ 6:9-22) — **pontosan 23**, egyezik a
tervvel. Átengedve a szűrőn:

| | |
|---|---|
| metszet | **23** |
| `mindig` — automatikusan kiszűrve | 12 |
| `jelzes` — keretszóként megjelölve | 8 |
| **gerinc-jelölt** | **3** |

A három: **H0127** *adamá* (a tanulmány saját lelete, fennmarad), **H0430** *Elohim*
(`kivetel`, szándékosan védve), **H3205** *jalad* („nemzeni") — utóbbi egyik listán sincs,
és ez helyes: a nemzetség-táblázatokban keretszó, de az 1Móz 3:16-ban a motívum magja.
**23 → 3, azaz 87% zajszűrés a lelet elvesztése nélkül.** Ez a fájl elfogadási tesztje;
a szkript módosítása után újra kell futtatni.

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
| szűrő-kalibráció ugyanazon az eseten | **23 → 3, a lelet megmarad** |
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
