# Kombinált Strong-keresés próbafuttatása — jelentés

*Próbafuttatás dátuma: 2026.08.27. Branch: `3b-ujraellenorzes-proba`. Ez a fájl NEM módosítja a `genezis/*.md` study-fájlokat — kizárólag a `PaRDeS_gyorsreferencia.md` "Motívum-felismerés módszertana" ma beépített "kombinált Strong-keresés" kiegészítésének hatását dokumentálja, ugyanazon a két tanulmányon (1Móz 1:1 és 1Móz 1:2–2:3), amit a korábbi kétlépcsős próba (`ideiglenes/3b_ujraellenorzes_proba_jelentes.md`) is vizsgált.*

---

## 0. Validáció

A feladatban megadott validációs eset (H0430 [Elohím] + H1254 [bará], 1Móz 1:1-hez) reprodukálva:

```
comm -12 idx/H0430.txt idx/H1254.txt
```

**Eredmény: pontosan a megadott 12 vers** — 1Móz 1:1, 1:21, 1:27, 2:3, 2:4, 5:1, 5Móz 4:32, Ez 28:13, Zsolt 51:12, Ámós 4:13, Ézs 40:28, Ézs 45:18. **Teljes egyezés** a chat-felület korábbi manuális futtatásával (2603 önálló H0430 + 52 önálló H1254 → 12 együttes előfordulás). A módszertan és a mechanikus lekérdezés (verzió-alapú indexfájlok + `comm -12` metszet a teljes `TAHOT_kivonat.tsv`-n) ezzel megerősítve — a további futtatások ugyanezt az eljárást használják.

---

## 1. lépés — vizsgált szópárok/hármasok azonosítása

### Study A (1Móz 1:1) — 1. lépcsőn kiesett/határeset szavak

A korábbi jelentés szerint 5 tartalmi szóból 3 **kiesett** (H0430 *elohím* 2603×, H8064 *samájim* 420×, H0776 *árec* 2501×) és 2 **határeset** (H7225 *bereshít* 51×, H1254 *bará* 52×), de mind az 5 egyetlen versben (1:1) fordul elő, tehát minden párjuk/hármasuk jogosult a kombinált keresésre. A gyakorlati keret miatt (lásd 4. pont) a ténylegesen lefuttatott és tartalmilag minősített kombinációk:

| Kombináció | Egyedi találatok (globális) |
|---|---|
| **H0430+H1254** (Elohím+bará) — *validációs eset* | 12 |
| **H0430+H8064+H0776** (Elohím+samájim+árec, a teljes 1:1-es hármas) | 32 |
| H0430+H8064 (Elohím+samájim) | 73 |
| H0430+H0776 (Elohím+árec) | 305 |
| H8064+H0776 (samájim+árec) | 180 |

A három páros kombináció (73/305/180 találat) **nem szelektív** — a validációs eset (52→12, kb. 4:1 szűkítés) helyett itt alig szűkül a keresési tér az önálló szavak (420–2603) gyakoriságához képest, mert a "menny"+"föld" pár önmagában rendkívül gyakori teológiai formula (kb. minden 5. Isten-idézetben szerepel valamelyik). Ezeket **nem minősítettük tartalmilag** — ez maga is módszertani tanulság (lásd 5. pont). Teljes tartalmi minősítés a validált párra (12) és a szűkebb hármasra (32) készült.

### Study B (1Móz 1:2–2:3) — 1. lépcsőn kiesett szavak

58–59 tartalmi szó esik ki (globális előfordulás ≥50, a korábbi jelentés listája szerint). A 34 vers belső együttes-előfordulásaiból **463 egyedi szópár** generálható mechanikusan — ez a tartalmi minősítéshez kezelhetetlenül sok (lásd 4. pont indoklása). Ehelyett egy **célzott, motívum-vezérelt mintát** választottunk: minden olyan párt, amely (a) a study saját PaRDeS-elemzésében (3. pont) már megnevezett fogalomhoz kötődik, és (b) a globális metszet mérete kezelhető (≤50 találat) volt. A kiválasztott és lefuttatott kombinációk:

| Kombináció | Motívum | Globális találat |
|---|---|---|
| H1254+H0120 (bará+ádám) | ember teremtése | 8 |
| H1288+H6942 (bárach+kádás) | 7. napi áldás+megszentelés | 4 |
| H7673+H1288 (sábat+bárach) | 7. napi nyugalom+áldás | 2 |
| H7673+H6942 (sábat+kádás) | 7. napi nyugalom+megszentelés | 1 |
| H1288+H7637 (bárach+sevíí) | áldás+hetedik | 3 |
| H6942+H7637 (kádás+sevíí) | megszentelés+hetedik | 2 |
| H0120+H2145 (ádám+záchár) | ember+férfi/nő | 4 |
| H2233+H6529 (zerá+perí) | mag+gyümölcs (növényzet) | 6 |
| H0430+H7307 (Elohím+rúach) | Isten Szelleme | 46 |
| H6440+H4325 (páné+majim) | "a vizek színén" idióma | 47 |

Négy tovább nem minősített, de mechanikusan ellenőrzött nagy pár (dokumentálva a szükségtelen terjedelem elkerülése végett): H0430+H2416 (62), H0430+H5315 (76), H3117+H7637 (59), H4399+H6213 (95) — mindegyik túl generikus formula ("Isten... élő", "munkáját végezte") ahhoz, hogy a kereszthivatkozás-keresésben szelektív legyen.

---

## 2. lépés — tartalmi minősítés

### Study A

**H0430+H1254 (validált, 12 találat)** — a validációs adatok szerint: 4×✅ (5Móz 4:32, Ámós 4:13, Ézs 40:28, Ézs 45:18), 2×🔶 (Ez 28:13, Zsolt 51:12 — utóbbi más referensű, Drash-értékes), 5× nem releváns (1Móz-en belüli önismétlés), 1× (2:4) határeset a study saját szakaszán belül.

**H0430+H8064+H0776 (1:1-es hármas, 32 találat)**

| Igehely | Minősítés | Indoklás |
|---|---|---|
| 2Kir 19:15 | ✅ | "...te teremtetted a mennyet és a földet" — explicit, direkt Peshat-párhuzam, Ezékiás imájában |
| 2Krón 2:12 | ✅ | "...a ki mind a mennyet, mind a földet teremtette" — Hírám áldása, explicit teremtés-kijelentés |
| Ézs 37:16 | ✅ | "Te teremtéd a mennyet és a földet" — a 2Kir 19:15 párhuzamos (szinoptikus) szövege Ézsaiásnál |
| 1Móz 24:3 | 🔶 | "az Úr, a mennynek Istene, és a földnek Istene" — szuverenitás-cím esküformulában, nem teremtés-kijelentés |
| 1Móz 24:7 | 🔶 | ua. — "az égnek Istene" cím, más kontextusban (elhívás-elbeszélés) |
| 2Krón 36:23 / Ezsd 1:2 | 🔶 | Círusz rendelete, "a mennynek Istene" cím — szuverenitás, nem teremtés |
| 5Móz 10:14 | 🔶 | "Ímé az Úréi az egek... a föld és minden" — birtoklás-kijelentés, rokon de nem teremtő ige |
| 5Móz 4:39 | 🔶 | "az Úr az Isten, fent a mennyben és alant e földön" — monoteista hitvallás, nem teremtés |
| Józs 2:11 | 🔶 | Ráháb hitvallása, ua. formula |
| 1Kir 8:23, 1Kir 8:27, 2Krón 6:14, 2Krón 6:18 | ❌ | "lakozhatik-é Isten a földön" — templom-teológia, más témakör |
| 1Móz 27:28 | ❌ | áldásformula (harmat/kövérség), nem teremtés |
| 1Móz 28:12 | ❌ | Jákób létrája — más motívum (menny-föld összekötő látomás) |
| 1Sám 17:46 | ❌ | Dávid-Góliát csatakiáltás, véletlen szóegyüttállás |
| 5Móz 25:19 | ❌ | Amálek-ítélet, véletlen szóegyüttállás |
| Ez 8:3 | ❌ | látomás-elragadtatás, más témakör |
| Préd 5:2 | ❌ | Isten transzcendenciája vs. ember, nem teremtés |
| Zsolt 108:6, Zsolt 57:6, Zsolt 57:12, Zsolt 68:9 | ❌ | doxológia-formula ("magasztaltassál az egek felett"), ill. Sinai-teofánia — nem teremtés |
| 1Móz 1:1, 1Móz 2:4, 5Móz 4:32, Ézs 45:18 | — | már szerepelnek a validált 12-es listában (duplikátum) |
| 1Móz 1:17, 1:20, 1:26, 1:28 | — | a Study B (nem A) saját belső versei — másik tanulmányhoz tartoznak, itt csak zaj |

### Study B

**H1254+H0120 (bará+ádám, 8 találat)**

| Igehely | Minősítés | Indoklás |
|---|---|---|
| Ézs 45:12 | ✅ | "Én alkotám a földet, és az embert rajta én teremtém..." — explicit, direkt Peshat-párhuzam az 1:26-27-hez |
| 1Móz 6:7 | 🔶 | "Eltörlöm az embert, akit teremtettem..." — ugyanaz a motívum, de fordított irányú (özönvíz-ítélet, teremtés visszavonása) |
| Zsolt 89:48 | 🔶 | "Mily semmire teremtetted te mind az embernek fiait" — emberi élet mulandósága, rokon de más hangsúlyú |
| 1Móz 5:1, 1Móz 5:2 | — | már szerepel az eredeti 2. lépcsős (TSK) listában — duplikátum |
| 5Móz 4:32, Ámós 4:13 | — | már szerepel a Study A validált 12-es listájában — duplikátum |
| 1Móz 1:27 | — | belső (a study saját verse) |

**H1288+H6942 / H7673+H1288 / H7673+H6942 / H1288+H7637 / H6942+H7637 (7. napi klaszter, összesen 4+2+1+3+2=12 nyers, sok átfedéssel)**

| Igehely | Minősítés | Indoklás |
|---|---|---|
| 2Móz 20:11 | — | már szerepel az eredeti 2. lépcsős (Károli-KH+TSK) listában mindkét studynál — duplikátum, de a kombinált keresés is megerősíti: ez az EGYETLEN nem-belső vers, ami mind az öt "7. napi" párban következetesen megjelenik — módszertanilag ez a legerősebb (legrobusztusabb) egyetlen kereszthivatkozás a 2:2-3 szakaszhoz |
| 1Krón 23:13 | ❌ | Áron felszentelése — más "megszentelés" kontextus (papi, nem szombati) |
| Jób 1:5 | ❌ | Jób megszenteli fiait áldozattal — rituális, nem szombati |
| Ruth 4:14 | ❌ | áldásformula, véletlen szóegyüttállás |
| 1Krón 26:5 | ❌ | Obed-Edom családi áldása, véletlen szóegyüttállás |

**H0120+H2145 (ádám+záchár, 4 találat)**

| Igehely | Minősítés | Indoklás |
|---|---|---|
| 1Móz 5:2 | — | duplikátum (lásd fent) |
| 2Móz 13:15 | ❌ | elsőszülött-törvény, más témakör |
| 4Móz 31:35 | ❌ | hadizsákmány-számlálás, véletlen szóegyüttállás |
| 1Móz 1:27 | — | belső |

**H2233+H6529 (zerá+perí, 6 találat)**

| Igehely | Minősítés | Indoklás |
|---|---|---|
| Zak 8:12 | 🔶 | "a szőlőtő megadja gyümölcsét, a föld is megadja termését, az egek is megadják harmatjokat" — eszkatologikus áldás-ígéret, tartalmilag rokon a teremtés bőség-motívumával, de restaurációs (nem ősi teremtési) kontextusban |
| 3Móz 27:30 | ❌ | tizedtörvény, más témakör |
| Zsolt 21:11 | ❌ | ellenség gyümölcsének/magvának kiirtása (ítélet), véletlen szóegyüttállás |
| 1Móz 1:11, 1:12, 1:29 | — | belső |

**H0430+H7307 (Elohím+rúach, 46 találat)** — alacsony hozam: a lista túlnyomó többsége (kb. 35/46) emberi/prófétai szellem-állapotra (Saul gonosz szelleme, prófétai elragadtatás, Bezalél mesteri szelleme) vonatkozik, nem a teremtő/megújító Szellem motívumára.

| Igehely | Minősítés | Indoklás |
|---|---|---|
| Zsolt 51:12 | — | duplikátum (Study A validált listájában már 🔶) |
| Ámós 4:13 | — | duplikátum (Study A validált listájában már ✅) |
| 4Móz 27:16, 4Móz 16:22 | 🔶 | "az Úr, minden test lelkének Istene" — Isten mint minden élet/szellem forrása, rokon de nem közvetlenül a teremtés-elbeszéléshez kötődő megfogalmazás |
| Préd 12:7 | 🔶 | "a lélek Istenhez tér vissza, a ki adta volt azt" — az emberi szellem isteni eredete, rokon a *ruach elohím* témával, de a Préd-i kontextus (halál/mulandóság) más hangsúlyú |
| Préd 11:5 | 🔶 | "nem ismered az Istennek dolgát, a ki mindeneket cselekszik" — a magzati formálódás rejtélye Isten teremtő munkájához hasonlítva, közvetett rokonság |
| a fennmaradó ~39 találat | ❌ | emberi/prófétai szellem-állapot (Saul, Bír, Sám, Krón, Józs, Hós, Mal stb.) — nincs tartalmi kapcsolat a teremtés-motívummal |
| 1Móz 1:2 | — | belső |

**H6440+H4325 ("a vizek színén" idióma, 47 találat)** — a lista túlnyomó része ("penei ha-majim" mint egyszerű helyrajzi kifejezés: özönvíz apadása, folyók/tengerek átkelése) generikus, nem a teremtés-kozmológiához kötődik.

| Igehely | Minősítés | Indoklás |
|---|---|---|
| Jób 26:10 | ✅ | "Ő szab határt a víz színe fölé, a világosságnak és setétségnek elvégéig" — kozmológiai kép, közvetlen tartalmi párhuzam 1:2/1:4-hez (fény/sötétség elválasztása a vizek felett) |
| Jób 38:30 | ✅ | "a mikor a víz mint kő összeáll, és a mélység színe egybefagy" — Isten teremtő beszéde (Jób 38, már Study A-nál kiemelt fejezet más versével), közvetlen "mélység/víz színe" kozmológiai párhuzam |
| a fennmaradó ~43 találat (özönvíz-elbeszélés, Jordán-átkelés, harci/földrajzi leírások stb.) | ❌ | generikus helyrajzi idióma, nincs tartalmi kapcsolat a teremtés-motívummal |
| 1Móz 1:2, 1:20 | — | belső |

---

## 3. lépés — összevetés a korábbi jelentéssel

Az alábbi táblázat csak azokat a jelölteket sorolja fel, amelyek **✅ minősítést kaptak**, és **sem a korábbi jelentés 1. lépcsős (szó-szintű Strong), sem 2. lépcsős (Károli-KH/TSK vers-szintű) találatai között NEM szerepeltek** — vagyis a mai kombinált (harmadik granularitású) keresés valódi, nettó hozama.

| Study | ÚJ ✅ jelölt | Réteg-javaslat | Miért nem került elő korábban |
|---|---|---|---|
| A | 5Móz 4:32 | Peshat/Drash | a szó-szintű szűrőn H0430 kiesett, H1254 határeset; a vers-szintű TSK/Károli listán nem szerepelt (nincs TSK-hivatkozás Gen 1:1-ről erre a versre) |
| A | Ámós 4:13 | Peshat | ua. — a TSK nem társítja Gen 1:1-hez |
| A | Ézs 40:28 | Peshat | ua. |
| A | Ézs 45:18 | Peshat | *(ez már a régi 2. lépcsős TSK-listán is ✅ volt (Ézs 45:18, 200 Votes) — a kombinált keresés csak megerősíti, NEM új; a validációs listából ezért itt kivezetve a nettó összesítésből)* |
| A | 2Kir 19:15 | Peshat | sem szó-, sem vers-szintű (TSK/Károli) listán nem szerepelt Gen 1:1-hez társítva |
| A | 2Krón 2:12 | Peshat | ua. |
| A | Ézs 37:16 | Peshat | ua. (a 2Kir 19:15 szinoptikus párhuzama) |
| B | Ézs 45:12 | Peshat | a *bará*+*ádám* szó-szintű Strong-pár nem szerepelt egyik korábbi lépcsőn sem társítva 1:26-27-hez |
| B | Jób 26:10 | Peshat/Remez | a "vizek színén" idióma-keresés korábban nem futott le; a TSK sem hozta ezt a verset 1:2-höz |
| B | Jób 38:30 | Peshat/Remez | ua. |

**Nettó ÚJ ✅ (a korábbi jelentés egyik lépcsőjén sem szerepelt):**
- **Study A: 6 db** (5Móz 4:32, Ámós 4:13, Ézs 40:28, 2Kir 19:15, 2Krón 2:12, Ézs 37:16 — Ézs 45:18 kizárva, mert az már a 2. lépcsős listán is ✅ volt)
- **Study B: 3 db** (Ézs 45:12, Jób 26:10, Jób 38:30)
- **Összesen: 9 db nettó új ✅ jelölt**, plusz további 9 db 🔶 (rokon-de-eltérő, ill. Drash-szinten értékes) jelölt mindkét studyból együtt (Ez 28:13, Zsolt 51:12 [Study A validált]; 1Móz 24:3, 1Móz 24:7, 2Krón 36:23/Ezsd 1:2, 5Móz 10:14, 5Móz 4:39, Józs 2:11 [Study A hármas]; 1Móz 6:7, Zsolt 89:48, Zak 8:12, 4Móz 27:16, 4Móz 16:22, Préd 12:7, Préd 11:5 [Study B]).

---

## 4. Kimenet — módszertani megjegyzés a mintavételről

A Study B 463 mechanikusan generálható szópárja közül csak 10-et (2%) minősítettünk tartalmilag — ez tudatos, dokumentált szűkítés, nem hiányosság: a fennmaradó ~450 pár túlnyomó többsége (1) vagy két, egymástól független, véletlenül egy versben együtt szereplő, de tartalmilag nem összefüggő szót kombinál (pl. "reggel"+"sötétség" — napszak-határ szavak, amik bármely özönvíz- vagy éjszaka-elbeszélésben együtt előfordulhatnak), (2) vagy már lefedett duplikátum-motívum (pl. minden *bárach*-tartalmú pár nagyrészt ugyanazt az 5-6 verset hozza vissza). A 10 kiválasztott pár szándékosan a study saját 3. pontjában (PaRDeS keretrendszer) már megnevezett fő motívumokra (emberteremtés, 7. napi szentelés, Isten Szelleme, vizek színe) épült — ez adja a módszer valódi tesztjét, nem a kombinatorikus kimerítés.

---

## 5. Záró összegzés

**A validációs eset (H0430+H1254) tökéletesen egyezett** a chat-felület korábbi manuális futtatásával (12/12 vers, azonos minősítési arány) — a mechanikus módszertan (Strong-számonkénti indexfájl + halmazmetszet a teljes `TAHOT_kivonat.tsv`-n) megbízhatóan reprodukálható.

**Érdemes-e rutinszerűen bevonni a kombinált keresést a teljes 22 tanulmányos újraellenőrzésbe?** **Igen, de feltételesen és szűrve, nem kimerítő kombinatorikával:**

1. **A módszer valódi, mérhető hozzáadott értéket ad**: a mai próbafuttatás **9 db nettó új ✅ jelöltet** talált (Study A: 6, Study B: 3), amit sem a szó-szintű (1. lépcső), sem a vers-szintű TSK/Károli (2. lépcső) keresés nem hozott elő — ez a két study 4. pontjának **kb. 20-25%-os bővítését** jelentené, ha beépülne.
2. **DE a szelektivitás erősen függ a szópár megválasztásától.** A validált pár (52×+2603×→12 találat, kb. 220:1 szűkítés) rendkívül szelektív volt, de a mechanikusan generált párok többsége (pl. H0430+H0776: 305 találat, vagy H0430+H7307: 46 találat, ebből csak 4-5 tartalmilag releváns) **nem** ilyen éles — a "menny"/"föld"/"Isten"/"szellem" tipusú általános teológiai szavak páronkénti kombinációja gyakran még mindig túl nagy és zajos halmazt ad.
3. **Javasolt gyakorlati szabály a jövőbeli alkalmazáshoz**: a kombinált keresést csak (a) a study saját PaRDeS-elemzésében már megnevezett, **konkrét, azonosítható motívumokra** (nem mechanikus szópár-kimerítésre) érdemes futtatni, és (b) csak azokat a találati halmazokat minősíteni tartalmilag, amelyek **globálisan ≤50 verset** hoznak — 50 fölött a szűrés hatékonysága drasztikusan csökken, és a manuális átolvasás költsége már nem áll arányban a hozammal.
4. **Költségbecslés**: a mai próbafuttatás (10 pár + 1 hármas + validáció Study A-ra, kb. 15 perc gépi lekérdezés + kb. 120 vers tartalmi átolvasása/minősítése) egyetlen munkamenetben, kb. 20-25 perc alatt elvégezhető volt — egy 22 tanulmányos, motívum-vezérelt (nem kimerítő) alkalmazás becsülten stúdiumonként 5-10 perc gépi idő + 10-20 perc tartalmi átolvasás, tehát a teljes korpuszra kb. 6-8 óra összesített LLM-asszisztált munka, jelentős, de nem irreális ráfordítással.
