# 3/b. módszertan retroaktív próbafuttatása — jelentés

*Próbafuttatás dátuma: 2026.08.27. Branch: `3b-ujraellenorzes-proba`. Ez a fájl NEM módosítja a `genezis/*.md` study-fájlokat — kizárólag a kétlépcsős (szó-szintű + vers-szintű) motívum-felismerési módszertan retroaktív alkalmazásának hatását dokumentálja a 4. ponton ("Kapcsolódó igehelyek").*

---

## 0. Módszertani emlékeztető

A `sablonok/PaRDeS_gyorsreferencia.md` "Motívum-felismerés módszertana" négy forrásból gyűjt jelöltet:
- 🔤 [Strong] — LEXIKAI (azonos szó, TAHOT_kivonat.tsv globális előfordulás)
- 📖 [Károli-KH] — EDITORIÁLIS/TEMATIKUS, erősség-jelzés nélkül
- 📚 [TSK] — EDITORIÁLIS/TEMATIKUS, Votes≥15 szűréssel
- 🧠 [Claude-tudás] — adatforrás nélküli saját javaslat

Minden jelölt: ✅ valódi/releváns, ❌ hamis, 🔶 rokon de eltérő szerkezetű/kategóriájú.
**Lexikai vs. tematikus fegyelem:** [Strong]-nál a ✅ azonos szót állít. [Károli-KH]/[TSK]-nál a ✅ CSAK tematikus kapcsolatot igazol — lexikai rokonságot csak Strong-számmal alátámasztva szabad hozzáállítani.

---

## STUDY A — 1Móz 1:1

### 1. lépcső eredménye (már elvégezve, itt csak összegezve)

Teljes tartalmi szókészlet: **5 szó** (a vers rendkívül rövid).

| Strong | Szótő | Globális előford. | 1. lépcső eredmény |
|---|---|---|---|
| H7225 | *bereshít* | 51 | HATÁRESET — a küszöb fölött, de a "30-50, tágabban" elv alapján megtartható 2. lépcsőre |
| H1254 | *bará* | 52 | HATÁRESET — ua. |
| H0430 | *elohím* | 2603 | KIESIK (túl gyakori a szó-szintű ritkaság-elvhez) |
| H8064 | *samájim* | 420 | KIESIK |
| H0776 | *árec* | 2501 | KIESIK |

**Vers-szintű jelöltek (1Móz 1:1, 1 vers):** Károli-KH 8 sor, TSK (Votes≥15) 65 sor, 4 db átfedéssel (Zsolt 33:6, Zsid 11:3, ApCsel 14:15, ApCsel 17:24) → **69 egyedi vers-szintű jelölt**.

**Az első fontos megfigyelés itt már látszik:** a szó-szintű szűrésen 3 az 5 legfontosabb teológiai szó (Elohim, samájim, árec) egyszerűen KIESIK — túl gyakoriak ahhoz, hogy a "ritkaság indokolja a bevonást" logika alapján továbbjussanak —, miközben pont EZEKHEZ a szavakhoz/fogalmakhoz létezik a legtöbb és legerősebb vers-szintű (TSK/Károli-KH) találat. A szó-szintű "lexikai ritkaság" és a vers-szintű "tematikus fontosság" tehát két EGYMÁSTÓL FÜGGETLEN tengelyt mér — egyik sem helyettesíti a másikat.

### 2. lépcső — tartalmi minősítés (Top 20+ TSK Votes szerint + minden Károli-KH tétel)

| Forrás | Igehely | Votes | Minősítés | Indoklás |
|---|---|---|---|---|
| 📚+📖 | Ján 1:1, Ján 1:3 | 304 | ✅ | Explicit "kezdetben" szó-visszhang (görög *en arché* = héber *bereshít*), Krisztus mint teremtő Ige — jelenleg is Remez-idézet |
| 📚+📖 | Zsid 11:3 | 238 | ✅ | Direkt exegetikai levezetés Gen 1:1-ből ("láthatatlanból"), jelenleg is Drash-idézet |
| 📚 | Ézs 45:18 | 200 | ✅ | "Nem hiába formálta, hanem lakásra alkotta" — Isten mint egyedüli, célra teremtő — Peshat-erősítő, jelenleg NEM szerepel |
| 📚 | Jel 4:11 | 165 | ✅ | "Te teremtettél mindent, és a te akaratodért vannak és teremttettek" — liturgikus megerősítés, Peshat/Sod határán |
| 📚 | Zsid 1:10 | 158 | ✅ | "Te Uram, kezdetben alapítottad a földet" — Zsolt 102:25 idézete, DE itt a Fiúra alkalmazva → közvetlen Sod/krisztológiai párhuzam Kol 1:16-17-hez, jelenleg NEM szerepel |
| 📚 | Ézs 42:5 | 134 | 🔶 | Isten mint az egek/föld teremtője, de a kontextus (szolga-ének) más tematikus keretbe ágyazza — rokon, nem elsődleges |
| 📚+📖 | Kol 1:16, Kol 1:17 | 133 | ✅ | Jelenleg is Sod-idézet, a legmagasabb Votes-ú Sod-jelölt |
| 📚 | 2Móz 20:11 | 127 | ✅ | Szombat-parancs alapja, direkt Gen 1:1 hivatkozás (hat nap), de tematikailag inkább a Study B (7. nap) 3/b pontjához illik jobban, mint Study A-hoz |
| 📚 | Jób 38:4 | 123 | ✅ | "Hol voltál, mikor a föld alapjait vetettem" — erős Peshat-párhuzam (Isten szuverén, egyedüli teremtő), jelenleg NEM szerepel, önmagában erősebb "kihívó" hangvétele van, mint Zsolt 33:6-nak |
| 📚 | ApCsel 17:24 | 113 | ✅ | "Az Isten, a ki teremtette a világot és mindazt, a mi abban van" — Peshat-erősítő, jelenleg NEM szerepel |
| 📚 | 2Pét 3:5 | 86 | 🔶 | Isten szava általi teremtés — rokon a Zsid 11:3 Drash-gondolattal, de nem ad hozzá újat |
| 📚 | Neh 9:6 | 83 | ✅ | "Te, te vagy egyedül az Úr... te teremtetted az eget" — erős Peshat-párhuzam, hasonló Zsolt 33:6-hoz, csoportosítható vele |
| 📚 | Ézs 44:24 | 79 | ✅ | "...a ki EGYEDÜL feszítem ki az egeket" — az "egyedüli teremtő" motívumra a jelenlegi Zsolt 33:6-nál explicitebb szóhasználat |
| 📚+📖 | Jer 32:17, Jer 51:15 | 73/72 | 🔶 | Isten ereje általi teremtés — rokon, de nem ad új réteget |
| 📚 | Zsolt 33:9 | 72 | ✅ | Ugyanaz a zsoltár, mint a jelenleg idézett 33:6, közvetlen szomszédos vers ("Mert ő szólt és meglett") — csoportosítható a már meglévő idézettel |
| 📚 | Péld 3:19 | 68 | ✅ | Bölcsesség mint teremtő-eszköz — Sod-rokon (előkép a Logosz/Bölcsesség-krisztológiához) |
| 📚 | Jel 14:7 | 66 | 🔶 | Liturgikus felszólítás az imádásra — rokon, nem ad új tartalmi réteget |
| 📚 | Zsolt 115:15, Zsolt 136:5 | 63/62 | 🔶 | Áldás-formula ill. bölcsesség-himnusz — rokon a meglévőkkel |
| 📚+📖 | ApCsel 14:15 | 62 | ✅ | "Élő Isten, ki teremtette a mennyet, a földet, a tengert" — Peshat-erősítő |
| 📚 | Péld 8:22, Péld 8:30 | 59/59 | ✅ | Bölcsesség mint az "első" Isten mellett, a teremtés "kezdetén" — erős Sod/Remez-jelölt, a Logosz-motívum ószövetségi előképe |
| 📖 | Gen 2,4-2,5 | (nincs Votes) | ✅ | A "második teremtéstörténet" bevezetője, közvetlen szerkezeti folytatás — inkább Study B-hez tartozik tematikailag |
| 📖 | Zsolt 89:12, Zsolt 136:5 | (nincs Votes) | 🔶 | Isten hatalmának himnikus dicsérete, rokon de nem ad újat |
| 📖 | Jób 33:4 | (nincs Votes) | ✅ | "Az Istennek Lelke teremtett engem" — inkább Study B (1:2 *ruach elohím*) témájához illik, itt 🔶 |
| 🧠 [Claude-tudás] | 2Makk 7:28 | — | ✅ | Klasszikus *creatio ex nihilo* deuterokanonikus szöveghely, amit a study 3. pontja már meg is említ (Drash, Vitatott pont 2) — a 4. pontban azonban NEM szerepel önálló idézetként, holott a Levenson-vitához közvetlenül kapcsolódna |
| 🧠 [Claude-tudás] | Zsolt 90:2 | 46 (TSK is hozza, alacsonyabb Votes) | ✅ | "Minekelőtte hegyek lettek..." — Isten időn-túlisága, közvetlen Sod-párhuzam a jelenlegi "idő teremtése" gondolathoz |

### Study A — összevetés a jelenlegi 4. ponttal

| Jelenlegi idézet | Réteg | Minősítés a módszer szerint | Kategória |
|---|---|---|---|
| Zsolt 33:6 | Peshat | ✅ mindkét forrásban, de "csak" 51 Votes, több erősebb Peshat-jelölt is van (Ézs 44:24 "egyedül", Jób 38:4, Neh 9:6) | (a) megegyezik, DE (c) erősebbel bővíthető |
| Ján 1:1-3 | Remez | ✅ legmagasabb Votes (304) az egész listán | (a) megegyezik — a módszer szerint is ez a legerősebb jelölt |
| Zsid 11:3 | Drash | ✅ 2. legmagasabb Votes (238) | (a) megegyezik — erősen indokolt választás |
| Kol 1:16-17 | Sod | ✅ magas Votes (133), de Zsid 1:10 (158 Votes) egy még közvetlenebb "Fiú mint teremtő alany" szöveghely | (a) megegyezik, DE (b)/(c) Zsid 1:10-zel kiegészíthető/erősíthető |

**Nem talált "gyengülne" esetet Study A-ban** — mind a 4 jelenlegi idézet ✅ minősítést kap, és mindegyik a saját rétegének egyik legmagasabb Votes-ú jelöltje. A módszer tehát UTÓLAG IGAZOLJA a már meglévő választásokat, de talál **2 db új (b) jelöltet** (Ézs 44:24/Jób 38:4/Neh 9:6 mint erősebb Peshat-alternatíva/kiegészítés; Zsid 1:10 mint erősebb/kiegészítő Sod-jelölt), plusz egy 🧠-forrású hiányt (2Makk 7:28, ami a 3. pontban már szóba került, de a 4. pontból kimaradt).

### Study A — javaslat

**Érdemes-e frissíteni:** Igen, KIEGÉSZÍTÉS formájában — nem csere, mert a jelenlegi 4 idézet a módszer szerint is helytálló.
- **Peshat:** Ézs 44:24 hozzáadása vagy Zsolt 33:6 melletti másodikként említése ("egyedül" szóhasználat pontosabban illik az "Isten mint EGYEDÜLI teremtő" témamondathoz, mint a Zsolt 33:6 "szavára lettek" fókusza).
- **Sod:** Zsid 1:10 megemlítése a Kol 1:16-17 mellett, mint további, direkt ószövetségi idézetre (Zsolt 102:25) épülő krisztológiai megerősítés.
- **Kiegészítő infó a 3/c vagy Sod-hoz:** 2Makk 7:28 mint a *creatio ex nihilo* vita (Levenson vs. patrisztika) klasszikus deuterokanonikus háttere, önálló idézetként is, nem csak említésként.

---

## STUDY B — 1Móz 1:2 – 2:3

### 1. lépcső eredménye (már elvégezve, itt összegezve)

Teljes tartalmi szókészlet: **93 egyedi Strong-szám** (a nyers 118 tételből 24 grammatikai elem + 1 duplikátum kizárva).

Küszöb (globális előfordulás < 50): **35 szó ÁTMEGY** a 2. lépcsőre, **58 szó KIESIK**.

**Ami kiesik — és ez a legfontosabb tanulság:** pont a study legfontosabb teológiai szavai esnek ki a szó-szintű szűrőn: H0430 *elohím* (2603), H1961 *hajá* (3547), H0559 *amár* (5289), H3605 *kol* (5398), H5414 *natán* (7419), H6213 *aszá* (2627), H0776 *árec* (2501), H3117 *jom* (2304), H7200 *raá* (1296), H8147 *sneim* (766), H0259 *echád* (968), H3318 *jacá* (1061). Ezek a szavak minden nyelvi elemzésnek gerincét adják (2. pont táblázatai), de a szó-szintű "lexikai ritkaság" szűrőn automatikusan kiesnek.

**Ami átmegy (35 szó, mind <50 globális előfordulás):** a legritkább, leginkább technikai/egyedi szavak — pl. H1876 *dásá* "sarjadni" (2), H0922 *bohú* "puszta" (3), H7363 *rácháf* "lebegni" (3), H3418 *jerek* "zöld" (6), H4723 *mikvé* "gyűjtőhely" (12), H3533 *kávas* "meghódítani" (14), H8317 *sárac* "nyüzsögni" (14), H6754 *celem* "képmás" (17, HATÁRESET-közeli, de a study egyik LEGFONTOSABB szava), H1823 *demút* "hasonlatosság" (25), H7287 *rádá* "uralkodni" (26), H8415 *tehóm* "mélység" (35), H1254 *bará* (52 — technikailag kiesik, de a Study A elemzésnél már HATÁRESETNEK jelöltük).

**Itt egy második fontos jelenség látszik:** a *celem* (képmás, H6754) — a study egyik legfontosabb Drash/Sod-fogalma — a szó-szintű szűrőn éppen ÁTMEGY (17 előfordulás, ritka), miközben az "elohím"/"bará" a Study A-hoz hasonlóan HATÁRESET vagy kiesik. Vagyis a szó-szintű módszer NEM egyenletesen bünteti a teológiailag fontos szavakat — a *celem*-hez hasonló, valóban ritka, egyedi kulcsszavaknál pontosan a szándékolt módon működik (kiszűri a zajt, megtartja az egyedi jelzőszót), csak az "univerzális" alapszavaknál (Elohim, bará, hajá) esik ki rendszerszinten, mert azok eleve túl gyakoriak bármilyen ritkaság-alapú szűréshez.

**Vers-szintű jelöltek (1Móz 1:2 – 2:3, 34 vers):** Károli-KH 24 sor (16 különböző vers), TSK (Votes≥15) 84 sor (12 különböző vers, kiemelkedő: 1:26=24, 1:3=17, 1:27=14, 1:28=10 találat).

### 2. lépcső — tartalmi minősítés (Top 20+ Votes szerint + minden Károli-KH tétel, csoportosítva ahol indokolt)

| Forrás | Igehely | Votes | Minősítés | Indoklás |
|---|---|---|---|---|
| 📚 | Jer 4:23 (1:2-höz) | 84 | 🔶 | "Néztem a földet és ímé kietlen és puszta" — SZÓ SZERINTI *tohú vabohú* idézet, de ítélet-kontextusban (a teremtés visszavonása) — erős lexikai kapcsolat (Strong-szinten is igazolható: H8414/H922 mindkettőben), de tartalmilag fordított irányú (ítélet, nem teremtés) → jó jelölt lenne, de figyelmeztető irányjelöléssel (← visszautaló, nem előkép/beteljesedés) |
| 📚 | Mt 19:4 / Mk 10:6 (1:27-hez) | 73/38 | ✅ | Jézus explicit idézi Gen 1:27-et a házasság alapjaként — jelenleg NEM szerepel a 4. pontban, pedig ez a LEGERŐSEBB, direkt újszövetségi idézet az egész study-hoz | 
| 📚 | Kol 3:10, Ef 4:24 (1:26-hoz) | 70/65 | ✅ | "Új ember... Isten képére (*eikón*/*celem* párhuzam) teremtetett" — közvetlen tematikus ÉS részben lexikai (eikón~celem) kapcsolat a *celem*-motívumhoz, jelenleg csak Kol 1:15 szerepel — Kol 3:10/Ef 4:24 az "új teremtés" irányból erősítik ugyanazt a motívumot |
| 📚 | 2Kor 4:6 (1:3-hoz) | 65 | ✅ | "Isten... ragyogást parancsolt a sötétségből" — közvetlen Gen 1:3 idézet, krisztológiai fénnyel — jelenleg NEM szerepel, erős Remez/Sod jelölt |
| 📚 | Zsolt 104:30 (1:2-höz) | 61 | ✅ | Jelenleg is idézve (Remez), a legmagasabb Votes az 1:2-höz kötött jelöltek közül — megerősíti a jelenlegi választást |
| 📚 | Ézs 45:18 (1:2-höz) | 55 | 🔶 | "Nem hiába (*tohú*) teremtette" — lexikai kapcsolat (H8414), de a kontextus (célra teremtés) más hangsúlyú, mint az 1:2 kezdőállapot |
| 📚 | Ján 1:5 (1:3-hoz) | 54 | ✅ | "A világosság a sötétségben fénylik" — közvetlen tematikus párhuzam az első teremtő szóhoz, Logosz-fény motívum |
| 📚 | Zsolt 8:4, Zsolt 8:8 (1:26-hoz) | 43/43 | ✅ | Jelenleg Zsolt 8:5-6 van idézve (Peshat) — ez a szomszédos vers-pár megerősíti, hogy a zsoltár egésze releváns |
| 📚 | Ef 2:10 (1:27-hez) | 43 | 🔶 | "Az Ő alkotása vagyunk" — rokon "új teremtés" gondolat, de görög szava (*poiéma*) nem a *celem*-motívumhoz kötődik közvetlenül |
| 📚 | Zsolt 33:6 (1:2-höz) | 40 | ✅ | Már Study A-ban idézve — itt is releváns (Isten szava/lehelete a teremtésben), de a duplikáció miatt itt 🔶 (már felhasznált motívum) |
| 📚+📖 | 1Móz 9:1/9:7 (1:28-hoz) | 40/34 | ✅ | Nóénak megismételt áldás/megbízás — közvetlen belső bibliai visszhang (← előkép/↔ ismétlés), erős Peshat-párhuzam |
| 📚+📖 | 1Móz 5:1-2 (1:27-hez) | 38/38 | ✅ | A nemzetségtáblázat direkt visszautal Gen 1:27-re — erős belső-bibliai megerősítés |
| 📚 | 1Móz 3:22 (1:26-hoz) | 37 | ✅ | "Ímé az ember olyanná lett, mint mi" — közvetlen visszhangja az 1:26 "alkossunk" többes számának, fontos a Drash-vitához (angyalok/Szentháromság kérdés) |
| 📚 | Zsolt 100:3 (1:26-hoz) | 34 | 🔶 | "Ő alkotott minket" — általános teremtés-hála, nem specifikusan a *celem*-motívumhoz |
| 📚 | 2Kor 3:18 (1:26-hoz) | 33 | ✅ | "Ugyanazon ábrázatra elváltozunk" — a *celem*/*eikón* megújulás-motívum újszövetségi csúcspontja, erős Sod-kiegészítő a Kol 1:15 mellé |
| 📖 | 1Móz 2:21, 2:25 (1:27-hez) | 33/33 | ✅ | Közvetlen szerkezeti folytatás (férfi/nő teremtésének részletezése) — inkább kontextuális, mint önálló kereszthivatkozás |
| 📚 | Zsid 2:6, Zsid 2:9 (1:26-hoz) | 21/21 | ✅ | Zsolt 8 zsidókhoz írt levélbeli krisztológiai értelmezése — közvetlenül összeköti a Peshat (Zsolt 8) és Sod (Krisztus mint tökéletes ember/képmás) rétegeket, jelenleg nincs kihasználva ez az összekötő kapocs |
| 📚 | Zsid 4:4 (2:2-höz) | 20 | ✅ | A jelenlegi 4. pont már MEGEMLÍTI szövegesen ("Zsid 4:4 szó szerint hivatkozik"), de a ténylegesen IDÉZETT vers Zsid 4:9-11 — a TSK a 4:4-et (a direkt idézetet) hozza fel elsőként, nem a 4:9-11-et; érdemes lenne pontosítani, melyik a fő idézet |
| 📖 | 1Kor 11:7 (1:26-hoz) | 21 | 🔶 | "Isten képe és dicsősége" — nemi szerep-vitákba ágyazott, tematikailag rokon de exegetikailag vitatott alkalmazás, óvatosan kezelendő |
| 📖 | Ez 20:12, Mk 2:27 (2:3-hoz) | 15/15 | ✅ | "A szombat az emberért lett" — fontos kiegészítő a hetedik napi nyugalom Drash-témájához, más irányból (rendeltetés) mint a Zsid 4:9-11 |
| 🧠 [Claude-tudás] | Ef 1:4 | — | 🔶 | "Kiválasztott... a világ teremtetése előtt" — rokon, de nem az 1:2-2:3 szakasz specifikus motívumaihoz kötődik, inkább általános teremtés-előtti kiválasztás témája |
| 🧠 [Claude-tudás] | Zsolt 139:14 | 28 (TSK is hozza) | ✅ | "Csodálatosan vagyok alkotva" — a *celem* méltóság-motívum személyes/egyéni alkalmazása, jó kiegészítő az Alkalmazás ponthoz |

### Study B — összevetés a jelenlegi 4. ponttal

| Jelenlegi idézet | Réteg | Minősítés a módszer szerint | Kategória |
|---|---|---|---|
| Zsolt 8:5-6 | Peshat | ✅, de a TSK a szomszédos 8:4/8:8-at hozza (43 Votes) — maga az 5-6 vers nem szerepel önállóan a TSK Votes≥15 listán ezen a szűrésen (a study saját válogatása pontosabb versszakaszt jelöl meg, mint a TSK nyers vers-egység) | (a) megegyezik — a study saját döntése finomabb, mint a TSK granularitása |
| Zsolt 104:30 | Remez | ✅ legmagasabb Votes (61) az 1:2-höz kötött jelöltek közül | (a) megegyezik — erősen indokolt |
| Zsid 4:9-11 | Drash | ✅ tematikailag helyes, de a TSK/Károli konkrétan a Zsid 4:4-et (20 Votes) társítja elsődlegesen 2:2-höz, nem a 4:9-11-et | (a) megegyezik tartalmilag, DE (c) pontosítható: a 4:4 a direkt idézet, a 4:9-11 a kiterjesztés — érdemes mindkettőt jelölni, vagy a 4:4-et elsődlegesként feltüntetni |
| Kol 1:15 | Sod | ✅, de Kol 3:10 (70 Votes) és Ef 4:24 (65 Votes) — mindkettő magasabb Votes-ú — ugyanahhoz a *celem*/*eikón* motívumhoz kapcsolódik, "új ember" irányból | (b) új — Kol 3:10/Ef 4:24 hiányoznak, pedig erősebb Votes-úak; (c) erősebb-nek is tekinthető, mert konkrétabb lexikai kapcsolatot ad (eikón megismétlődik) |

Emellett **Mt 19:4/Mk 10:6** (Jézus explicit idézi Gen 1:27-et) egy TISZTÁN ÚJ (b) jelölt, ami jelenleg egyáltalán nincs a 4. pontban, holott a legmagasabb Votes-ú (73) az 1:27-hez kötődő tételek között, és direkt újszövetségi idézet — erősebb bizonyítottságú, mint bármelyik jelenlegi Study B idézet.

**Nem talált "gyengülne" esetet Study B-ben sem** — mind a 4 jelenlegi idézet ✅ marad, de két helyen (Sod-réteg, és a Drash-réteg pontosítása) erős kiegészítési/pontosítási lehetőség adódik, plusz egy teljesen hiányzó, magas Votes-ú Peshat-jelölt (Mt 19:4).

### Study B — javaslat

**Érdemes-e frissíteni:** Igen, ez a study-nál még indokoltabb, mint Study A-nál.
- **Peshat/kiegészítés:** Mt 19:4 (vagy Mk 10:6) hozzáadása — Jézus saját szájából idézett Gen 1:27, ez hiányzik, pedig a legerősebb újszövetségi megerősítés a "férfi és nő" motívumhoz.
- **Sod:** Kol 1:15 mellé (vagy helyette) Kol 3:10 és/vagy Ef 4:24 megfontolása — ezek a *celem*/*eikón*-motívum "megújulás" irányú, magasabb Votes-ú kiegészítései; 2Kor 3:18 is jó harmadik jelölt.
- **Drash pontosítás:** jelezni, hogy a TSK elsődlegesen Zsid 4:4-et (a direkt idézetet) társítja 2:2-höz, a Zsid 4:9-11 pedig ennek eszkatologikus kiterjesztése — mindkettő megtartható, de érdemes a sorrendet/hangsúlyt jelezni.
- **Remez megerősítés:** Zsolt 104:30 marad, de 2Kor 4:6 (65 Votes) jó kiegészítő lehet a "fény/sötétség" (1:3) témához, ha a study bővíteni akarja a Remez réteget külön szakaszra.

---

## Összefoglalás

- **Jelentés-fájl:** `ideiglenes/3b_ujraellenorzes_proba_jelentes.md` (ez a fájl)
- **Durva költségbecslés:** kb. 2 db mechanikus lekérdezés-pár (4 awk parancs) + kb. 90 vers-szintű sor és 35+58 szó-szintű tétel tartalmi átolvasása/minősítése; a próbafuttatás becsült ideje egy ember számára kézzel kb. 3-4 óra alapos munka lenne (Strong-számonkénti előfordulás-ellenőrzés, vers-szintű tartalmi olvasás), gépi/LLM-asszisztált végrehajtással ez egyetlen munkamenetben, kb. 15-20 percnyi tényleges számítási idő és nagyságrendileg 60-90 ezer token felhasználás alatt elvégezhető (a két teljes study beolvasása, a ~150 vers-szintű sor és 93+118 szó-szintű tétel áttekintése és a jelentés megírása dominálja a költséget).
- **Vélemény a kétlépcsős szűrés hatékonyságáról:**
  1. **A szó-szintű (1. lépcső) szűrés nagyon hatékonyan csökkenti a drága, tartalmi 2. lépcső terhét ott, ahol a szókészlet nagy és heterogén** — Study B-nél 93 szóból 58-at (62%-ot) kiszűrt anélkül, hogy bármi releváns elveszett volna a LEXIKAI (Strong-szintű) kereséshez, mert azok a szavak (Elohim, hajá, amár stb.) eleve túl gyakoriak ahhoz, hogy a "ritka szó = erős egyedi kapocs" logika alapján bárhová vezessenek.
  2. **DE ugyanez a szó-szintű szűrés TELJESEN VAK a vers-szintű (editoriális/tematikus) jelöltekre** — pont azoknál a legfontosabb szavaknál (Elohim, bará, celem-hez közeli fogalmak), amelyek a szó-szintű szűrőn kiesnek vagy határesetek, található a legtöbb és legerősebb TSK/Károli-KH vers-szintű találat (pl. Zsid 11:3 238 Votes, Ján 1:1/1:3 304 Votes — mindkettő "Elohim/bará" tematikájú vershez kötődik, miközben maguk a szavak a szó-szintű szűrőn technikailag kiesnek vagy határesetek). **Ez a próbafuttatás legfontosabb módszertani tanulsága: a két granularitás (szó-szintű LEXIKAI vs. vers-szintű TEMATIKUS) egymást kiegészíti, nem helyettesíti — a szó-szintű küszöb csak a [Strong]-forrású lexikai jelölteket szűkíti, a [Károli-KH]/[TSK] vers-szintű jelölteket a teljes verstartományra függetlenül, saját (Votes-alapú) küszöbbel kell kezelni.**
  3. **A tartalmi (nem mechanikus) minősítés ténylegesen talált érdemi hibákat/hiányokat** a jelenlegi 4. pontokban — nem drámai tévedéseket (egyik jelenlegi idézet sem bizonyult ❌-nak vagy erőtlennek), hanem hiányzó, magasabb Votes-ú, egyenrangú vagy erősebb alternatívákat (Study A: Ézs 44:24, Zsid 1:10; Study B: Mt 19:4, Kol 3:10/Ef 4:24) — ami azt mutatja, hogy a módszertan bevezetése előtt is ÉSZSZERŰ, jól megalapozott választások születtek, de a szisztematikus 4-forrásos gyűjtés és Votes-rendezés objektívebb, ellenőrizhetőbb alapot ad, és következetesen talál 1-3 érdemi kiegészítési lehetőséget tanulmányonként.
