# Kereszthivatkozás-keresési napló — 1Móz 1:1

*Hivatalossá téve: 2026.08.27. Forrás: `ideiglenes/3b_ujraellenorzes_proba_jelentes.md`
(STUDY A szakasz) és `ideiglenes/kombinalt_kereses_proba_jelentes.md` (Study A
szakasz), a `3b-ujraellenorzes-proba` branch próbafuttatásai — ez a fájl a két
próbajelentés Study A-ra vonatkozó tartalmát egyesíti a
`2_PaRDeS_bovitett_sablon.md` v11 4. pontjában előírt kötelező napló-szerkezet
szerint. A napló NEM módosítja a `1Moz_1v1_bovitett.md` study-fájlt — kizárólag
dokumentálja a keresési/minősítési folyamatot.*

---

## 1. Vizsgált kulcsszavak

A vers rendkívül rövid — teljes tartalmi szókészlete **5 szó**:

| Strong | Szótő | Globális előfordulás | 1. lépcső (szó-szintű ritkasági küszöb) eredménye |
|---|---|---|---|
| H7225 | *bereshít* | 51 | HATÁRESET — a küszöb fölött, de a "30-50, tágabban" elv alapján megtartható a 2. lépcsőre |
| H1254 | *bará* | 52 | HATÁRESET — ua. |
| H0430 | *elohím* | 2603 | KIESIK (túl gyakori a szó-szintű ritkaság-elvhez) |
| H8064 | *samájim* | 420 | KIESIK |
| H0776 | *árec* | 2501 | KIESIK |

**Mind az 5 szó egyetlen versben (1:1) fordul elő**, ezért — a
`PaRDeS_gyorsreferencia.md` "Motívum-felismerés módszertana" FIGYELEM-bekezdése
szerint — minden párjuk/hármasuk jogosult a **kombinált Strong-keresésre** is,
függetlenül attól, hogy önmagukban kiestek vagy határesetek voltak.

---

## 2. Nyers találatok forrásonként

### 🔤 Strong — szó-szintű
Ld. fenti táblázat (globális előfordulás-számok).

### 🔤 Strong — kombinált (2+ Strong-szám együttes előfordulása)

| Kombináció | Egyedi találatok (globális) | Minősítésre került? |
|---|---|---|
| **H0430+H1254** (Elohím+bará) — *validációs eset* | 12 | igen (teljes körűen) |
| **H0430+H8064+H0776** (Elohím+samájim+árec, a teljes 1:1-es hármas) | 32 | igen (teljes körűen) |
| H0430+H8064 (Elohím+samájim) | 73 | nem — nem szelektív (ld. 5. pont) |
| H0430+H0776 (Elohím+árec) | 305 | nem — nem szelektív |
| H8064+H0776 (samájim+árec) | 180 | nem — nem szelektív |

*Validáció: a `comm -12 idx/H0430.txt idx/H1254.txt` lekérdezés pontosan a
megadott 12 verset adta vissza (1Móz 1:1, 1:21, 1:27, 2:3, 2:4, 5Móz 4:32, Ez
28:13, Zsolt 51:12, Ámós 4:13, Ézs 40:28, Ézs 45:18) — teljes egyezés a chat-
felület korábbi manuális futtatásával (2603 önálló H0430 + 52 önálló H1254 → 12
együttes előfordulás). A mechanikus módszertan (verzió-alapú indexfájlok +
`comm -12` metszet a teljes `TAHOT_kivonat.tsv`-n) ezzel megerősítve.*

### 📖 Károli-KH + 📚 TSK — vers-szintű (1Móz 1:1, 1 vers)

Károli-KH: 8 sor. TSK (Votes≥15): 65 sor. 4 db átfedés (Zsolt 33:6, Zsid 11:3,
ApCsel 14:15, ApCsel 17:24) → **69 egyedi vers-szintű jelölt**. A ténylegesen
tartalmilag átolvasott és minősített részhalmaz (Top 20+ Votes szerint +
minden Károli-KH tétel) a 3. pont táblázatában szerepel.

### 🧠 Claude-tudás
- 2Makk 7:28 (a study 3. pontja már megemlíti Drash-szinten, de a 4. pontban
  nem szerepel önálló idézetként)
- Zsolt 90:2 (TSK is hozza, alacsonyabb Votes-szal, mint a fenti táblázat
  küszöbe)

---

## 3. Tartalmi minősítés — MINDEN vizsgált jelölt

### 3/a — Vers-szintű (Károli-KH/TSK, Top 20+ Votes + minden Károli-KH tétel)

| Forrás | Igehely | Votes | Minősítés | Indoklás |
|---|---|---|---|---|
| 📚+📖 | Ján 1:1, Ján 1:3 | 304 | ✅ | Explicit "kezdetben" szó-visszhang (görög *en arché* = héber *bereshít*), Krisztus mint teremtő Ige |
| 📚+📖 | Zsid 11:3 | 238 | ✅ | Direkt exegetikai levezetés Gen 1:1-ből ("láthatatlanból") |
| 📚 | Ézs 45:18 | 200 | ✅ | "Nem hiába formálta, hanem lakásra alkotta" — Peshat-erősítő |
| 📚 | Jel 4:11 | 165 | ✅ | "Te teremtettél mindent..." — liturgikus megerősítés, Peshat/Sod határán |
| 📚 | Zsid 1:10 | 158 | ✅ | Zsolt 102:25 idézete a Fiúra alkalmazva → Sod/krisztológiai párhuzam |
| 📚 | Ézs 42:5 | 134 | 🔶 | Isten mint teremtő, de a kontextus (szolga-ének) más tematikus keretbe ágyazza |
| 📚+📖 | Kol 1:16, Kol 1:17 | 133 | ✅ | Legmagasabb Votes-ú Sod-jelölt |
| 📚 | 2Móz 20:11 | 127 | ✅ | Szombat-parancs alapja, de tematikailag inkább Study B-hez illik |
| 📚 | Jób 38:4 | 123 | ✅ | Erős Peshat-párhuzam (Isten szuverén, egyedüli teremtő) |
| 📚 | ApCsel 17:24 | 113 | ✅ | Peshat-erősítő |
| 📚 | 2Pét 3:5 | 86 | 🔶 | Isten szava általi teremtés — rokon a Zsid 11:3 gondolattal, nem ad új réteget |
| 📚 | Neh 9:6 | 83 | ✅ | Erős Peshat-párhuzam, csoportosítható Zsolt 33:6-tal |
| 📚 | Ézs 44:24 | 79 | ✅ | Az "egyedüli teremtő" motívumra explicitebb szóhasználat, mint Zsolt 33:6 |
| 📚+📖 | Jer 32:17, Jer 51:15 | 73/72 | 🔶 | Isten ereje általi teremtés — rokon, nem ad új réteget |
| 📚 | Zsolt 33:9 | 72 | ✅ | Ugyanaz a zsoltár, mint a jelenleg idézett 33:6, szomszédos vers |
| 📚 | Péld 3:19 | 68 | ✅ | Bölcsesség mint teremtő-eszköz — Sod-rokon |
| 📚 | Jel 14:7 | 66 | 🔶 | Liturgikus felszólítás, nem ad új tartalmi réteget |
| 📚 | Zsolt 115:15, Zsolt 136:5 | 63/62 | 🔶 | Áldás-formula / bölcsesség-himnusz — rokon a meglévőkkel |
| 📚+📖 | ApCsel 14:15 | 62 | ✅ | Peshat-erősítő |
| 📚 | Péld 8:22, Péld 8:30 | 59/59 | ✅ | Erős Sod/Remez-jelölt, Logosz-motívum ószövetségi előképe |
| 📖 | 1Móz 2:4-2:5 | (nincs Votes) | ✅ | Közvetlen szerkezeti folytatás — inkább Study B-hez tartozik tematikailag |
| 📖 | Zsolt 89:12, Zsolt 136:5 | (nincs Votes) | 🔶 | Himnikus dicséret, rokon de nem ad újat |
| 📖 | Jób 33:4 | (nincs Votes) | 🔶 | Inkább Study B (1:2 *ruach elohím*) témájához illik |
| 🧠 | 2Makk 7:28 | — | ✅ | Klasszikus *creatio ex nihilo* deuterokanonikus szöveghely — a 4. pontban NEM szerepel önálló idézetként |
| 🧠 | Zsolt 90:2 | 46 (TSK is hozza) | ✅ | Isten időn-túlisága, közvetlen Sod-párhuzam |

### 3/b — Kombinált Strong-keresés: H0430+H1254 (validált, 12 találat)

4×✅ (5Móz 4:32, Ámós 4:13, Ézs 40:28, Ézs 45:18), 2×🔶 (Ez 28:13, Zsolt 51:12 —
utóbbi más referensű, Drash-értékes), 5× nem releváns (1Móz-en belüli
önismétlés: 1:1, 1:21, 1:27, 2:3), 1× (2:4) határeset a study saját szakaszán
belül.

### 3/c — Kombinált Strong-keresés: H0430+H8064+H0776 (1:1-es hármas, 32 találat)

| Igehely | Minősítés | Indoklás |
|---|---|---|
| 2Kir 19:15 | ✅ | "...te teremtetted a mennyet és a földet" — explicit, direkt Peshat-párhuzam |
| 2Krón 2:12 | ✅ | "...a ki mind a mennyet, mind a földet teremtette" |
| Ézs 37:16 | ✅ | A 2Kir 19:15 szinoptikus párhuzama |
| 1Móz 24:3 | 🔶 | Szuverenitás-cím esküformulában, nem teremtés-kijelentés |
| 1Móz 24:7 | 🔶 | ua., más kontextusban |
| 2Krón 36:23 / Ezsd 1:2 | 🔶 | Círusz rendelete, szuverenitás-cím, nem teremtés |
| 5Móz 10:14 | 🔶 | Birtoklás-kijelentés, rokon de nem teremtő ige |
| 5Móz 4:39 | 🔶 | Monoteista hitvallás, nem teremtés |
| Józs 2:11 | 🔶 | Ráháb hitvallása, ua. formula |
| 1Kir 8:23, 1Kir 8:27, 2Krón 6:14, 2Krón 6:18 | ❌ | Templom-teológia, más témakör |
| 1Móz 27:28 | ❌ | Áldásformula, nem teremtés |
| 1Móz 28:12 | ❌ | Jákób létrája — más motívum |
| 1Sám 17:46 | ❌ | Véletlen szóegyüttállás |
| 5Móz 25:19 | ❌ | Véletlen szóegyüttállás |
| Ez 8:3 | ❌ | Más témakör |
| Préd 5:2 | ❌ | Isten transzcendenciája vs. ember, nem teremtés |
| Zsolt 108:6, Zsolt 57:6, Zsolt 57:12, Zsolt 68:9 | ❌ | Doxológia-formula / Sinai-teofánia — nem teremtés |
| 1Móz 1:1, 1Móz 2:4, 5Móz 4:32, Ézs 45:18 | — | duplikátum (már szerepel a validált 12-es listában) |
| 1Móz 1:17, 1:20, 1:26, 1:28 | — | a Study B (nem A) saját belső versei, itt csak zaj |

---

## 4. Végső döntés

A study **4. pontja jelenleg (2026.08.27-i állapot)** a következő négy idézetet
tartalmazza: **Zsolt 33:6** (Peshat), **Ján 1:1-3** (Remez), **Zsid 11:3**
(Drash), **Kol 1:16-17** (Sod).

| Igehely | Végső döntés | Indoklás |
|---|---|---|
| Zsolt 33:6 | ✅ BEKERÜLT (Peshat) | Megerősítve — bár "csak" 51 Votes-ú TSK-jelölt, a study saját választása marad; erősebb Votes-ú alternatíva is van (ld. lent) |
| Ján 1:1-3 | ✅ BEKERÜLT (Remez) | A legmagasabb Votes-ú (304) jelölt az egész listán — a módszer is ezt igazolja legerősebbnek |
| Zsid 11:3 | ✅ BEKERÜLT (Drash) | 2. legmagasabb Votes (238) — erősen indokolt választás |
| Kol 1:16-17 | ✅ BEKERÜLT (Sod) | Magas Votes (133), a study saját választása marad |
| Ézs 44:24 | ✅, de NEM került be | Erősebb/pontosabb "egyedüli teremtő" szóhasználat, mint Zsolt 33:6, de a szintenkénti 1-2-es limit miatt csak kiegészítésként javasolt, nem csere |
| Jób 38:4 | ✅, de NEM került be | ua. — Peshat-alternatíva, limit miatt kimaradt |
| Neh 9:6 | ✅, de NEM került be | ua. — Peshat-alternatíva, limit miatt kimaradt |
| Zsid 1:10 | ✅, de NEM került be | Erősebb/kiegészítő Sod-jelölt (Votes 158 > Kol 1:16-17 133), de a study Kol 1:16-17-et tartja meg elsődlegesként |
| 2Makk 7:28 | ✅, de NEM került be | A 3. pontban (Drash, Vitatott pont) már megemlítve, de a 4. pontból (önálló idézetként) hiányzik — dokumentált hiány, nem elutasítás |
| Zsolt 90:2 | ✅, de NEM került be | Sod-párhuzam ("idő teremtése"), a limit miatt nem szerepel |
| 2Móz 20:11 | ✅, de NEM került be | Tematikailag inkább a Study B 3/b (7. nap) pontjához illik |
| 1Móz 2:4-2:5 | ✅, de NEM került be | Inkább Study B-hez tartozik tematikailag |
| 2Kir 19:15, 2Krón 2:12, Ézs 37:16 | ✅ (kombinált keresés), de NEM kerültek be | Nettó új Peshat-jelöltek a kombinált hármas-keresésből, eddig egyik lépcsőn sem szerepeltek — a study még nem frissült ezekkel |
| 5Móz 4:32, Ámós 4:13, Ézs 40:28 | ✅ (kombinált keresés, validált pár), de NEM kerültek be | ua. — nettó új Peshat-jelöltek, a study még nem frissült |
| Ézs 45:18 | ✅ mindkét forráson (validált pár ÉS 2. lépcsős TSK, 200 Votes) — de NEM önálló idézetként a 4. pontban | Erős, kettős megerősítésű jelölt, jelenleg mégsem szerepel a study 4. pontjában önálló idézetként |
| A többi 🔶/❌ jelölt (Ézs 42:5, 2Pét 3:5, Jer 32:17/51:15, Jel 14:7, Zsolt 115:15/136:5, Zsolt 89:12, Jób 33:4, 1Móz 24:3/24:7, 2Krón 36:23/Ezsd 1:2, 5Móz 10:14, 5Móz 4:39, Józs 2:11, Ez 28:13, Zsolt 51:12, és a teljes ❌ lista a 3/c táblázatban) | ❌/🔶 — NEM releváns v. csak rokon | Ld. indoklás a 3. pont táblázataiban |

**Az 5. pont (Rabbinikus és patrisztikus hangok)** jelenleg nem hivatkozik
2Makk 7:28-ra sem — bár a 3. pont Sod/Vitatott pont szakasza tárgyalja a
*creatio ex nihilo* vitát (Levenson vs. patrisztikus konszenzus), a
deuterokanonikus szöveghely önálló forrásidézetként nincs beépítve.

---

## 5. Rövid összegzés

- **Vizsgált kulcsszó:** 5 (mind az 5 jogosult volt kombinált keresésre is a
  vers rövidsége miatt)
- **Vers-szintű (Károli-KH/TSK) jelölt, tartalmilag minősítve:** 25 sor (kb.
  30 egyedi igehely, csoportosított sorokkal) — ebből **19 ✅**, **6 🔶**, **0 ❌**
  (a Top 20+ Votes szűrés eleve kiszűrte a leggyengébb jelölteket)
- **Kombinált Strong-keresésű jelölt, tartalmilag minősítve:** 12 (H0430+H1254)
  + 32 (H0430+H8064+H0776) = 44 nyers találat — ebből kb. **9 ✅**, **8 🔶**,
  **~18 ❌**, a maradék duplikátum/belső vers
- **Beépítési arány:** a study 4. pontjában **4 idézet szerepel**, mindegyik
  ✅ minősítést kapott és a saját rétegének egyik legerősebb Votes-ú jelöltje —
  a módszer tehát UTÓLAG IGAZOLJA a meglévő választásokat, de **9 db nettó
  ÚJ ✅ jelöltet** (amit sem a szó-, sem a korábbi vers-szintű keresés nem
  hozott elő) és további **~15 db ✅/🔶 kiegészítő/alternatív jelöltet**
  azonosított, amelyek a szintenkénti 1-2-es limit miatt (vagy mert a study
  még nem frissült velük) jelenleg nem szerepelnek a 4. pontban.
- **Javasolt, de még nem végrehajtott frissítés:** Ézs 44:24/Jób 38:4/Neh 9:6
  (Peshat-kiegészítés), Zsid 1:10 (Sod-kiegészítés), 2Makk 7:28 (önálló Drash-
  idézetként), 2Kir 19:15/2Krón 2:12/Ézs 37:16/5Móz 4:32/Ámós 4:13/Ézs 40:28
  (kombinált keresésből nyert nettó új Peshat-jelöltek).

---

## 6. LXX-hidas audit-kiegészítés (2026.09.02)

*A `LXX_kivonat_Genezis.tsv` (LXX-fázis3 pilot) elkészülte után elvégzett,
első valódi tartalmi audit a fenti ✅-minősítéseken — nem új keresés, hanem
a MEGLÉVŐ minősítések lexikai alátámasztásának/cáfolatának ellenőrzése.*

**✅ Megerősítve, valódi lexikai alap (nem csak tematikus):**
- **Ján 1:1** ↔ 1Móz 1:1 (LXX): közös szó **ἀρχή** (G0746), TBESG 1. jelentés
  ("beginning, origin") mindkét helyen — a study Remez-idézete lexikailag is
  alátámasztott, nem csak tematikus visszhang.
- **Zsid 1:10** ↔ 1Móz 1:1 (LXX): ugyanez a szó, ugyanez a jelentés (κατ'
  ἀρχάς) — eddig nem szerepelt a study 4. pontjában, érdemes megfontolni
  Remez-kiegészítőként.

**❌ KIZÁRVA — hamis pozitív, dokumentált figyelmeztetésként:**
- **Kol 1:16** (ἀρχαὶ) és 1Móz 1:1 (LXX ἀρχή) — **azonos Strong-szám
  (G0746), de eltérő jelentésárnyalat**: Kol 1:16-ban a TBESG szerint 3.
  jelentés ("sovereignty, principality, rule" — a TAGNT saját angol
  tükörfordítása is "rulers"), NEM az 1. jelentés ("beginning"). **Ha valaha
  lexikai érvvel akarnánk alátámasztani a Kol 1:16-17 Sod-idézetet, ez a
  konkrét szó-egyezés NEM használható fel** — a study jelenlegi, tartalmi
  ("mindenek Krisztus által teremtettek") indoklása érintetlen marad, csak
  ez az egy lehetséges kiegészítő lexikai érv esik ki.

**Vizsgált, de LXX-adat hiánya miatt nem ellenőrizhető:** a többi ✅-minősített
NT-jelölt (Zsid 11:3, Jel 4:11, Kol 1:17, ApCsel 17:24, ApCsel 14:15) csak
generikus (θεός/γῆ/οὐρανός/ἐν, mind >200 előfordulású) közös szót mutatott —
ezek a napló eredeti, tematikus minősítése alapján maradnak érvényben,
lexikai megerősítés vagy cáfolat nélkül.
