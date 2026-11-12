# F194 — az ISTENTISZT-001 új cikkének menetnaplója (1. fázis, adat)

*#194 ISTENTISZT_UJ_CIKK · claude-opus-5-5 · a mérés: `naplok/F194_meres.md`*

## F194.1 — határ (2026-11-12)

A felhasználó döntései a második kör K6–K8 kérdésére (2026-11-11), és az orkesztrátoré a K7-re: DT-F194a–d (`dontesek/uj/istentiszt-uj-cikk-992f57.md`). Átvezetés: `naplok/F194_hatar_jeloltek.py`.
- 22 → 20 előfordulás (ÓSZ 16, ÚSZ 4): az ApCsel 9:14 és 9:21 elutasítva. A rájuk mutató két `kapcsolatok.tsv`-sor kikerült: Róm 10:13 → ApCsel 9:14 és ApCsel 9:14 → ApCsel 9:21.
- **A negatív kritérium új szövege — még nem az `adat/motivumok.tsv`-ben.** Az orkesztrátor kérése (2026-11-12): a #699 minden sorhoz új `meghatarozas` oszlopot ad, a sor módosítása ütközne; az F194.1-beli átírás az F194.5-ben visszaállítva. A #699 merge-e és a main behozása után ez a szöveg kerül a `negativ_kriterium` mezőbe (DT-F194a–c):

  > Az igehelyen a קָרָא (kárá, hív) igét a בְּשֵׁם (besém, „a nevén”) követi, és a név után az Úr neve, a יְהוָה (Jahve) áll: aktív, invokáló szerkezet („[valaki] segítségül hívja az Úr nevét”). Nem tartozik ide, ahol a név helyén névmási rag áll („nevemet”, „nevedet”, „nevét”: Zak 13:9, Zsolt 105:1, Jer 10:25, Ézs 43:1, 45:3), vagy más név (Ézs 44:5). Az Újszövetségben az ἐπικαλέω (epikaleó) mellett a névnek, az ὄνομα (onoma) szónak és az Úr megnevezésének kell állnia; a puszta „nevedet”, „ezt a nevet” (ApCsel 9:14, 21) és a név nélküli segítségül hívás (2Tim 2:22, Róm 10:12, 14) a fölérendelt fogalomhoz tartozik. A mérce a Károli alapszövege, a Textus Receptus (ApCsel 22:16). Kivétel: a kontrasztként megtartott 1Kir 18:25–26, ahol a név után אֱלֹהֵיכֶם (elóhéchem, „a ti istenteknek”), illetve הַבַּעַל (habbaal, „a Baálnak”) áll. A szenvedő (passzív) נִקְרָא … עַל (nikrá … al) szerkezet (birtoklás, hovatartozás, nem invokáció) kizárja a besorolást, még ha ugyanazt a két gyököt használja is (2Sám 6:2, Jer 7:10–14, 5Móz 28:10; az Újszövetségben a Zsid 11:16). Az „invokáló” marad; a 2Móz 33:19 és 34:5 nem kivétel; a tetragramma mindenütt Jahve.
- A 131 `elofordulas`-jelölt indoklása olvasói mondat (K47, K48, K04, K06). Az átírás előtt 94 sor sértette a kapu-szabályokat; utána a 142 sorból csak a 7 `motivumkozi` sor. Ezekhez a menet nem nyúlt: a kapcsolat-lépés a CS3 után jön (N-F194a).
- A `HATÁRDÖNTÉS`-jel a határnapló modelles részében; a 39. szabály friss, új modelles határkör nem indul.

**A próza-lépésnek átadva:** a 2Móz 33:19 és 34:5 `kapcsolodas` és `funkcio` mezője ma is a régi „Isten mondja ki a sajátját” / „❓ be nem sorolható … B-eset” szöveg. A DT-F194b szerint ez tilos. A mező a próza (U3) lépésében íródik újra, a többi 18 sor kerek prózájával együtt (K43). A mostani menet a prózához nem nyúlt.

## F194.2 — teljesség-mérés és LXX-híd (2026-11-12)

- **Három háló, az új ÚSZ-feltétellel** (`naplok/F194_teljesseg_meres.py`): 0 olyan döntés nélküli vers, amelyben a formula áll. Az ApCsel 22:16 a kritikai szövegen nem teljesíti a görög feltételt (αὐτοῦ), a Textus Receptuson igen; marad (DT-F194a).
- **LXX-híd** (`naplok/F194_lxx_hid_scan.py`, a 6. lépés): a LXX-ben 67 versben áll ἐπικαλέω + ὄνομα. Ebből 40 döntés nélküli; 23-at az F123-as összesítő sorok fednek. A maradék 17-ben a héberben nincs קָרָא (kárá). Ezek a `jeloltek.tsv`-n át, elutasítva kerültek be (`naplok/F194_lxx_jeloltek.py`):
  - 1 összesítő sor 14 versre (szenvedő szerkezet, a hely viseli a nevet; blokk=`lxx_szenvedo_hely`);
  - 2Sám 20:1 és 2Krón 28:15: megnevezés;
  - Zsolt 75:2: a héberben „neved közel van”.
- **Lelet a mérőfüggvényről:** a `teljesseg_meres.allapot` az összesítő sor tagjai közül csak az elsőt látja döntöttnek, a többit ELTÉRÉS-nek. A LXX-hídnál ezért kellett a blokkfájllal szűrni. A hiba nem a menet tárgya (N-F194b).

## F194.3 — a 15 nyitott lektori tétel besorolása (2. kiadás bemenete)

Forrás: `naplok/LEKTOR_ISTENTISZT-001.tsv`, `lektor:ISTENTISZT-001:1–15`, mind `nyitva`, `kiadas=2`, claude-fable-5-1, 2026-11-02, az 1. kiadás prózáján. A fájl generált: a válasz a felületről és az átvezetésből jön, ez a menet nem írja. A besorolás azt mondja meg, melyik lépés viszi a tételt.

| # | Hely | A gond röviden | Besorolás | Ki viszi |
|---|---|---|---|---|
| 1 | Lefedettség | A kapcsolat 1Móz 4:26 → Sof 3:9 nincs a prózában | próza + kapcsolat | U3 (a Kivonat és a 7. szakasz). A kapcsolat-sor felülvizsgálata a CS3 utáni kapcsolat-lépésé |
| 2 | Lefedettség | Az Ézs 41:25 „nyitva” | **adat: kész** | 2026-11-02 óta elutasítva (DT478, „Igen, mind”); az F194.1 olvasói indoklást adott. Lezárható: „az adat eldöntötte” |
| 3 | Kivonat | „a pátriárkák oltárépítéséhez kötődik”: túláltalánosítás | próza | U3. Adat: oltár a 12:8, 13:4, 26:25-ben; a 4:26-ban nincs, a 21:33-ban tamariszkuszfa |
| 4 | Kivonat | A kritérium a 1Kir 18:25–26 kivétele nélkül | próza (adat kész) | A kritériumszöveg a kivételt kimondja (F194.1); a Kivonat 3. bekezdése név szerint (K27): U3 |
| 5 | Kivonat | „önmegnevezés” (ApCsel 9:14, 21) | **adat: okafogyott** + próza | A két hely kikerült (DT-F194a). Az 1Kor 1:2-nél az U3 csak adattal alátámasztottat mondhat |
| 6 | Kivonat | „6 újszövetségi”, öt megnevezve | próza (adat kész) | Ma 4 ÚSZ-hely (1Kor 1:2, ApCsel 2:21, 22:16, Róm 10:13); a Kivonat számai az adatból: U3 (K26) |
| 7 | Kivonat | „formulaikus azonosság”: belső szó | próza | U3 (K04) |
| 8 | Kivonat | 【NAPLO】 a Kivonat résében | próza | U3: az új prózában nincs NAPLO (K13, CI E29) |
| 9 | Módszertan | Ellentmondó állapotok (2Móz 33:19/34:5 „be nem sorolható”) | **adat: eldöntve** + próza | DT-F194b: nem kivétel, azonos héber szerkezet. A `funkcio` mező és a Módszertan: U3 |
| 10 | Módszertan | Számozás („5.” 1–4. nélkül), üres hivatkozások | próza | U3 (K84, K45) |
| 11 | Módszertan | Belső szakszók (Q3-fegyelem, study, A-hely …) | próza | U3 (K04; kapu: MUNKASZO) |
| 12 | Módszertan | A BDB 2.c bekezdés csak kizárt helyekről szól | próza | U3: a kizárt helyek a 3. szakaszban és a mellékletben állnak; a Módszertanban legfeljebb egy mondat |
| 13 | Módszertan | Két egymást kizáró ÓSZ-szám (16 / 22) | **adat: kész** + próza | Ma 16 ÓSZ, 4 ÚSZ, 20 hely; az U3 csak a lap adatából számol (K20) |
| 14 | Módszertan | Törött mondat két NAPLO-blokkal | próza | U3 |
| 15 | 4. Kapcsolódás | A „pünkösdi/karizmatikus hangsúly” állítását nem támasztja alá adat | próza | U3: a tanítói rész kivezetve (DT643), az állítás nem kerül a lapra (K67f) |

**Összegzés:** a 15 tételből 2 adat-oldalon kész (2, 13), 1 okafogyott (5), 1 eldöntve (9); ezek prózai része is az U3-é. A többi 11 tisztán próza: az U3 nulláról írt szövege kezeli, a HAMART mércéjén (K04, K09, K13, K20, K26, K27, K45, K84). Nyitott lektori tétel nem marad a próza nélkül; a lektor-felületen a 2, 5, 9 és 13 „adat” válasszal zárható, a többi az U3 után.

**A mérés korlátja (a felhasználóval, 2026-11-11):** az ISTENTISZT 2. kiadás, a határa nagyrészt ismert. Ezért a lektori tételek száma nem általánosítható egy új motívumra. A folyamat összevetésére viszont jó (az 1. és a 2. kiadás ugyanazt a tartalmat dolgozza fel).

## F194.4 — Nave-blokk (K68)

A 20 versen a jelöltképzés (2 vers és 1%-os küszöb) öt kiválasztott témát ad: REVIVALS (4 vers), OBLIGATION, IDOL, GLORY, SEEKERS (2–2). A blokk tehát nem üres. A kiválasztott PRAYERLESSNESS (0 vers: a Jer 10:25 és a Zsolt 79:6 kívül esik), PENITENT (1 vers) és TESTIMONY (2/261, 1% alatt) a 2. kiadás határán nem jelölt. A döntés (DT424) nem változik, csak az indok: a 8 kiválasztott téma indoka versekkel áll (`naplok/F194_nave_indok.py`).

## F194.5 — a `motivumok.tsv` és a fordítás (2026-11-12)

- A `motivumok.tsv` ISTENTISZT-sora visszaállítva (az orkesztrátor kérése: a #699 új `meghatarozas` oszlopa miatt sorütközés lenne); a kritérium új szövege az F194.1 pontjában áll, a #699 merge-e után kerül a táblába.
- **Fordítás (C-y):** a `glossza_lexikon_forditas.py lista --id ISTENTISZT-001` öt hiányzó egységet ad. A négy görög rövid glosszát (G1510, G2250, G3004, G3956) a #704 (`claude/f203-thayer-forditas`, nyitott PR) már tartalmazza: itt nincs mit fordítani. A H8034 teljes TBESH-szócikke a felhasználó döntése szerint nem fordul (N87, az olvasó-fázis kérdése; az új lap a kulcsot nem kéri). Az `emeles.py lista` 18 fordítandó teljes szócikke közül egy sem ISTENTISZT-001-é.
- **Lelet (a generátoré, nem a menet tárgya):** az `ellenoriz.py` 42. szabálya szerint a G1941 Thayer sz3 érvényes fordítása nem áll az ISTENTISZT lapján: a bekötés a generátorban; a lap újragenerálásakor (2. fázis) újramérendő.

## F194.6 — a meghatározás (`motivumok.tsv` `meghatarozas`)

A HAMART-001 mintájára (F125.LJ7, DT-F125j): mi a motívum, mi hordozza, mit foglal magában. **A felhasználó jóváhagyta, 2026-11-12** (az orkesztrátoron át: „Jóváhagyom”; DT-F194e). A `motivumok.tsv`-be a #699 merge-e és a main behozása után kerül, az F194.1 kritérium-szövegével együtt.

> Az Úr nevének segítségül hívása a Bibliában rögzült formula: a héberben קָרָא בְּשֵׁם יְהוָה (kárá besém Jahve), „segítségül hívni az Úr nevét”. Énós nemzedékében hangzik el először (1Móz 4:26), a pátriárkák oltárainál ismétlődik, a Kármel-próbán a Baál nevének hívásával áll szemben, Jóel próféciájában a megmenekülés ígérete (Jóel 2:32); az Újszövetség ezt az ígéretet idézi (ApCsel 2:21, Róm 10:13), és a gyülekezet Jézus Krisztus nevét hívja segítségül (1Kor 1:2). A motívum ezt a formulát foglalja magában ott, ahol a név után az Úr neve áll; az imádság és a segítségül hívás általában nem tartozik ide.

*A motívum mai 20 helyének lefedése: 1Móz 4:26, 12:8, 13:4, 21:33, 26:25 (Énós, pátriárkák); 1Kir 18:24–26 (Kármel); 2Móz 33:19, 34:5, 2Kir 5:11, Zsolt 116:4, 13, 17, Sof 3:9 (a mondat nem nevezi meg, a formula része); Jóel 2:32; ApCsel 2:21, 22:16, Róm 10:13, 1Kor 1:2.*

## F194.7 — visszhang: megfelelők és tanúk (K65–K67a; 2026-11-12)

- **Első kéz (claude-opus-5-5):** `naplok/F194_megfelelok_kinyeres.py` → `naplok/F194_megfelelok_kinyert.tsv` (36 sor: a H7121 Targum- és Vulgata-megfelelője a 16 ószövetségi versben, a G1941 Vulgata-megfelelője a 4 újszövetségiben); `naplok/F194_tanuk_kinyert.tsv` (2 tanú a HCF-szövegből: Órigenész a Róm 10:13-nál, görög; Szent Jeromos a Jóel 2:32-nél, latin; a névalak a HAMART-001 táblasorához igazítva).
- **Második kéz (claude-sonnet-5-5, független subagent):** `naplok/F194_megfelelok_atnezes.tsv`, `naplok/F194_tanuk_atnezes.tsv`. Első kör: 35 + 1 jó, 2 elvetve — a Targum 1Kir 18:25 megjegyzése (a Targum a nevet megtartja, csak az „isteneitek” helyén áll „bálványaitok”) és az Órigenész-mondat („Énósig vezeti vissza”: túlzás; Órigenész a segítségül hívást az Írás kiemelkedő alakjainak jegyeként mutatja be, Énós és a Zsolt 99:6 Mózes, Áron, Sámuel). **Egy javítókör:** a két sort a kinyerő javította, a második kéz mindkettőt jónak ítélte.
- **Beolvasás:** `megfelelo_kinyer.py beolvas … --ellenor claude-sonnet-5-5` → `adat/visszhang_megfelelok.tsv` +36 sor; ebből 9 gépileg ellenőrizetlen (nem renderel), noha a második kéz jónak ítélte: a hat Jonatan-Targum sor (1Kir 18:24–26, 2Kir 5:11, Sof 3:9, Jóel 2:32; a kinyerő csak az Onkelost olvassa) és a három Zsolt 116 Vulgata-sor (a forrás kulcsa Zsolt 114:4, 115:4, 115:8) — N-F194d. A Zsolt 116 Targum-sorai alak nélkül, a hiány kimondva (a `Targum_PD` nem tartalmazza a Zsoltárokat). `tanu_kinyer.py beolvas` → `adat/visszhang_tanuk.tsv` +2 sor, mindkettő ellenőrzött. `megfelelo_kinyer.py lxx --motivum ISTENTISZT-001` → +20 sor; ebből 2 egyértelmű (2Móz 33:19 καλέσω, 34:5 ἐκάλεσεν), 18 alak nélküli, ellenőrizetlen — N-F194e. `ellenoriz`: mindkét tábla 0 hiba.
- **A második kéz megfigyelése:** a Rufinus-féle latin szöveg (HCF „From Latin”) Órigenésznél: a hagyomány a szerzőé (görög), a HAMART-001 Órigenész-sorával egyezően.
- **A lapon:** a 4.11 lánca a szópáros gerinc miatt ma üres lenne (N-F194c); a megfelelők a generátor-kör után renderelnek.
