# HATAR_ISTENTISZT-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum ISTENTISZT-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=ISTENTISZT-001 | ts=2026-11-11T12:20Z | bemenet=adat/elofordulasok.tsv@3a8723df5b,adat/motivumok.tsv@e1d84722b1,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** ISTENTISZT-001 — Segítségül hívni az Úr nevét · hordozó: `formulaikus` · fölérendelt fogalom: „istentisztelet/imádság általában (bármely invokációs forma, a קָרָא בְשֵׁם (kárá besém) formulán kívül)” · beépített sor: 20 (20 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), ISTENTISZT-001 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (20 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | ISTENTISZT-001 versei | másik versei | közös | közös/ISTENTISZT-001 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ALVIL-001 | 20 | 75 | 0 | 0% | 0% | 3, 4 |
| ANTROP-001 | 20 | 11 | 0 | 0% | 0% | nincs |
| HAMART-001 | 20 | 54 | 0 | 0% | 0% | 5 |
| HODIT-001 | 20 | 33 | 0 | 0% | 0% | nincs |
| KIRALY-001 | 20 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 20 | 11 | 0 | 0% | 0% | nincs |
| TEREMT-001 | 20 | 45 | 0 | 0% | 0% | nincs |
| TEREMT-002 | 20 | 3 | 0 | 0% | 0% | nincs |

### 2. Negatív kritérium a beépített sorokon

Módszer: a #150 `jelolt_eloszures.vizsgal` próbája a **beépített** sorokra: a motívum gerinc-kombinációi (`elofordulasok.tsv` `strong`, nyelvtani Strongok nélkül) közül legalább egy teljesen megvan-e a sor versének Strong-halmazában (TAHOT+TAGNT). Hordozó: `formulaikus`.

Összesítés: 20 beépített sor; gerinc-kombináció megvan: 20; **kérdés (hiányzik): 0**; nem ellenőrizhető (nincs szövegadat / nincs kombináció): 0.

**0 kérdés.** Mind a 20 ellenőrizhető beépített sor versében megvan legalább egy gerinc-kombináció.

## Modelles rész

<!-- MODELLES-KEZDET -->

<!-- SORÁLLAPOT: n=22 ujj=c2824be30ed7 -->

### Első kör — 2026-11-01, a 33 soros adaton (K1–K5; a felhasználói besorolás a DT476/DT478-ban átvezetve)


Modell-ellenőrzés: kért `fable`, tényleges `claude-fable-5-1` — egyezik. Bemenet: csak a motívum azonosítója; a motívum sora (`adat/motivumok.tsv:4`), a `motivumok/ISTENTISZT-001.md`, a `jeloltek.tsv` 133 ISTENTISZT-001-sora (35 beépítve, 92 elutasítva, 6 nyitva), az `elofordulasok.tsv` 33 sora, az `elutasitasi_okok.tsv`, a fenti Gépi rész; a Strong-tokenek saját lekérdezéssel (TAGNT/TAHOT, `split('\t')`). A nyitva sorokról nem döntök, csak ahol a kérdéshez tartoznak, ott hivatkozom rájuk.

**5 kérdés.** Mind kérdés a felhasználóhoz, nem javítás; egyik sem új igehely-javaslat.

**K1 — Következetlen határ (1. kérdés): az „ὄνομα nélkül nem a formula” indok az ÚSZ-oldalon csak egy sorra lett alkalmazva.**
(a) Az ApCsel 7:59 azért elutasított, mert a versben nincs ὄνομα, az 1Pét 1:17 viszont ugyanilyen (ὄνομα nélküli, és a tárgy nem is a név, hanem „Atya”) szerkezettel beépített.
(b) `adat/jeloltek.tsv:598` (ApCsel 7:59, elutasítva): „nincs ὄνομα — invokáció a קָרָא בְשֵׁם / ἐπικαλέομαι τὸ ὄνομα formulán kívül (motivumok.tsv, fölérendelt fogalom)” ↔ `adat/jeloltek.tsv:46` (1Pét 1:17, beépítve): „»…ha Atyának hívjátok őt…« — az invokáció »Atya« megszólításra alkalmazva; a görög ige azonos, a Károli nem tartja meg a »segítségül« szót”. Saját mérés (TAGNT): az 1Pét 1:17 Strong-sora G3962 (πατέρα) + G1941, G3686 (ὄνομα) nincs; az ApCsel 7:59-ben G1941 van, G3686 nincs — a két vers a formula szempontjából azonos állapotú.
(c) Ha az ὄνομα hiánya a fölérendelt fogalom felé tolja a sort (ApCsel 7:59), akkor az 1Pét 1:17 is ott áll; ha nem, az ApCsel 7:59 indoklása nem a határ indoka. (Az ÚSZ-oldali gerinc a `gerinc_elem` szerint csak G1941, tehát a Gépi rész 2. pontja ezt nem látja.)

**K2 — Következetlen határ (1. kérdés): a „név nélküli segítségül hívás” mint elutasítási ok csak a héber oldalon működik.**
(a) Hat ószövetségi sor „név nélküli” (שֵׁם nélküli) hívásként elutasított, miközben három újszövetségi, ugyanúgy név nélküli hívás beépített.
(b) `adat/jeloltek.tsv:535` (Zsolt 50:15, elutasítva): „név nélküli segítségül hívás (H7121, שֵׁם nélkül): rokon igei használat, nem a formula, NEM a motívum része” (azonos indokkal: 536 Zsolt 91:15, 537 Jer 29:12, 538 Ézs 58:9, 539 Ézs 65:24, 540 Zsolt 86:5) ↔ `adat/jeloltek.tsv:45` (2Tim 2:22, beépítve): „»…azokkal egyetembe, a kik segítségül hívják az Urat tiszta szívből« — a segítségül hívás mint közösségválasztási kritérium”; ugyanígy `:278` (Róm 10:12, „a kik őt segítségül hívják”) és `:43` (Róm 10:14, „Mimódon hívják segítségül, a kiben nem hittek?”). Saját mérés (TAGNT): 2Tim 2:22 ἐπικαλουμένων τὸν κύριον, Róm 10:12 ἐπικαλουμένους αὐτόν, Róm 10:14 ἐπικαλέσωνται εἰς ὃν — G3686 egyikben sincs; a Zsolt 86:5 (לְכָל קֹרְאֶיךָ, „mindazoknak, akik hívnak téged”) szerkezetileg a Róm 10:12 párja.
(c) A hordozó `formulaikus`; a formula a név. Ha a név hiánya a héber oldalon kizár, a görög oldalon miért nem — vagy a határ nyelvenként más, és ezt ki kell mondani?

**K3 — Következetlen határ (1. kérdés): a Zsolt 99:6-ot a בְּ hiánya zárta ki, a beépített görög sorokon viszont a בְּ-nek nincs megfelelője, és a Zsolt 99:6-ban a név ott van.**
(a) A Zsolt 99:6 — Károli: „az ő nevét segítségül hívókkal egybe, segítségül hívják vala az Urat” — a negatív kritérium (קָרָא + בְּ) szerint elutasított, miközben a Róm 10:12 („a kik őt segítségül hívják”, בְּ-analógia és név nélkül) beépített.
(b) `adat/jeloltek.tsv:639` (Zsolt 99:6, elutasítva): „a בְּ (H9003) az igenév előtt áll (»azok között, akik hívják«), a név (H8034 + 3. sz. birtokos rag) az igenév birtokos szerkezetében … kárá + בְּ + név szerkezet nincs” ↔ `adat/jeloltek.tsv:278` (Róm 10:12, beépítve): „»…a kik őt segítségül hívják« — a 10:13-as Jóel-idézet közvetlen bevezetése”. Saját mérés (TAHOT): Zsolt 99:6 H7121 + H8034 (קֹרְאֵי שְׁמוֹ) és H7121 + H0413 + H3068 (קֹרִאים אֶל־יְהוָה), tárgy Isten neve / Isten, alany ember, meghallgatással (H6030); a Róm 10:12-ben G1941 + G0846, név nélkül.
(c) A negatív kritérium a `motivumok.tsv:4`-ben csak héber szerkezettel van megfogalmazva (קָרָא + בְּ); a görög oldalon ennek nincs leképezése (a gerinc G1941 egyedül). Így a héber oldal szigorúbb (בְּ + שֵׁם kell), a görög enyhébb (puszta ige elég). Ez szándékolt kettős mérce, vagy a kritérium görög felét kell megírni? (A döntés a `jeloltek.tsv:639` szerint felhasználói, 2026-10-29; a kérdés ettől függetlenül a határ egységességéről szól.)

**K4 — Hígulás (2. kérdés) és következetlen határ (1. kérdés): a 2Móz 33:19 / 34:5 (B-minta: Isten kihirdeti saját nevét) beépített, holott a motívum saját tipológiája és a BDB sem invokációnak olvassa, és a C-mintát ugyanazzal az érvvel (alany Isten) zárta ki.**
(a) A két B-sor a negatív kritérium invokáló mintájának („[valaki] hívja segítségül [Isten nevét]”) nem felel meg — Isten a saját nevét kiáltja ki (BDB 3. „proclaim”, nem 2.c) —, mégis `beépítve`, `funkcio` „❓ be nem sorolható”.
(b) `adat/jeloltek.tsv:55` (2Móz 33:19, beépítve): „Isten maga jelenti ki Mózesnek: »kihirdetem előtted az Úr nevét« — nem az ember hívja segítségül Isten nevét, hanem Isten mondja ki a sajátját” (ugyanígy `:56`, 2Móz 34:5; `adat/elofordulasok.tsv:40–41` `jelentes_szam`=3, `funkcio`=„❓ be nem sorolható — a szereplők szerepe felcserélődik …”) ↔ `adat/jeloltek.tsv:620` (Ézs 43:1, elutasítva): „C-minta: Isten szólít néven egy embert (alany: Isten, tárgy: ember neve), nem a motívum A-mintája (alany: ember, tárgy: Isten neve); a קָרָא + שֵׁם szerkezet közös, a motívumhoz nem tartozik” (azonos indokkal: 621, 622). Saját mérés (TAHOT): 2Móz 33:19 וְקָרָאתִי בְשֵׁם יְהוָה, 34:5 וַיִּקְרָא בְשֵׁם יְהוָה (H7121 + H9003 + H8034 + H3068): a felszíni szerkezet A-mintájú, az alany Isten.
(c) A B-sorokat csak a felszíni קָרָא בְּשֵׁם szerkezet tartja a motívumban, az invokáció (a motívum funkciója) hiányzik — ez a hígulás tipikus útja a `formulaikus` hordozónál: forma igen, funkció nem. Kérdés: a motívum határa a *forma* (akkor a B-sorok benn vannak, de a C-minta kizárása felszíni-szerkezeti alapon nem indokolt) vagy az *invokáció* (akkor a B-sorok határon kívüli, kapcsolódó anyag, pl. `motivum_kapcsolatok` vagy a motívumfájl kitekintése)? Érintett nyitva sor (nem döntök róla): `adat/jeloltek.tsv:630` Ézs 41:25 (יִקְרָא בִשְׁמִי, Károli „hirdeti nevemet”) — ugyanaz a „kihirdet” olvasat, mint a B-sorokon, és nyitva áll, míg a B-sorok beépítettek.

**K5 — Hígulás (2. kérdés): az 1Kir 18:25–26 tárgya nem Isten neve, hanem „a ti istenteknek” / „a Baálnak” neve.**
(a) A negatív kritérium tárgyat is nevez („[Isten nevét]”), és a C-minta kizárása a tárgyra épült („tárgy: ember neve”); az 1Kir 18:25–26 tárgya hamis isten neve, mégis beépített.
(b) `adat/jeloltek.tsv:35` (1Kir 18:26, beépítve): „A Baál-próféták ismétlődő, sikertelen invokációja — a formula kudarca a kontraszt kiteljesedése” (ugyanígy `:34`, 1Kir 18:25: „hívjátok segítségül a ti istenetek nevét”) ↔ `adat/jeloltek.tsv:620` (Ézs 43:1, elutasítva): „… nem a motívum A-mintája (alany: ember, tárgy: Isten neve); a קָרָא + שֵׁם szerkezet közös, a motívumhoz nem tartozik”. Saját mérés (TAHOT, 1Kir 18:24): וּקְרָאתֶם בְּשֵׁם אֱלֹהֵיכֶם (H7121 + H9003 + H8034 + H0430) ↔ וַאֲנִי אֶקְרָא בְשֵׁם יְהוָה — a két fél szerkezete azonos, a tárgy más. A motívumfájl ezt a két sort az A-sorban tartja („ebből 2 a Kármel-próbán hamis isten nevével”, `motivumok/ISTENTISZT-001.md:446`).
(c) A kérdés nem a két vers fontossága (a kontraszt a motívum értelmezéséhez tartozik), hanem a határ: ha a tárgy („Isten neve”) a kritérium része, a 18:25–26 csak a fölérendelt fogalmon („bármely invokációs forma”) keresztül tartozik ide; ha a tárgy nem része a kritériumnak, a C-minta kizárásának tárgyra épülő fele nem indok. Melyik?

*Nem kérdés (ellenőrizve, rendben):* a 35 beépített `jeloltek`-sor = 33 `elofordulas` + 2 `motivumkozi` (`:633`, `:635`); a D-minta héber (623–629) és görög (596–615 K1_passziv) kizárása egységes; a jogi fellebbezés (606–611) és az esküformás tanúhívás (595) kizárásának nincs beépített párja; a tagadó forma (Jer 10:25, Zsolt 79:6, Ézs 64:6) következetes.

(proveniencia: scope=adat/motivumok.tsv:4 + adat/jeloltek.tsv (id=ISTENTISZT-001, 133 sor) + adat/elofordulasok.tsv (id=ISTENTISZT-001, 33 sor) + adat/elutasitasi_okok.tsv + adat/motivum_kapcsolatok.tsv + motivumok/ISTENTISZT-001.md + naplok/HATAR_ISTENTISZT-001.md (Gépi rész) + konkordancia/TAGNT_kivonat.tsv, TAHOT_kivonat.tsv (range: Róm 10:12–14, 1Kor 1:2, 2Tim 2:22, 1Pét 1:17, ApCsel 2:21, 7:59, 9:14, 9:21, 22:16, 2Kor 1:23; 2Móz 33:19, 34:5, Ézs 12:4, 41:25, 58:9, 65:24, Zsolt 50:15, 86:5, 91:15, 99:6, 105:1, Jer 29:12, 1Kir 18:24; split('\t')) | forras=modell:claude-fable-5-1 | ts=2026-11-01T11:16Z)

**Felhasználói besorolás** *(nem a modell írta; 2026-11-01, DT476)*

- K1: az 1Pét 1:17 kerüljön ki.
- K2: a név nélküli görög sorok kerüljenek ki (2Tim 2:22, Róm 10:12, Róm 10:14).
- K3: marad így, a döntésem áll (Zsolt 99:6 kint marad).
- K4: az elhatárolás a *besém* után álló JHVH (H3068): a 2Móz 33:19 és 34:5 teljesíti (`vekárati besém JHVH`, `vájikrá besém JHVH`), az Ézs 43:1 és 45:3 (*besimchá*, „a te neveden”) és a 44:5 (*besém Jaakóv*) nem.
- K5: az 1Kir 18:25–26 kontrasztként marad; a lapon jelezni kell, hogy a *sém* után nem JHVH áll, hanem *Elohím* (18:25: *elohéchem*) illetve *ha-Báal* (18:26).

*(proveniencia: scope=TAHOT_kivonat.tsv (2Móz 33:19, 34:5, 34:6; Ézs 43:1, 44:5, 45:3; 1Kir 18:24–26) | forras=manual: a felhasználó döntései a chatben | ts=2026-11-01)*

### Második kör — 2026-11-09, a mai (22 soros) adaton

Modell-ellenőrzés: kért `fable`, tényleges `claude-fable-5-1` — egyezik. Bemenet: csak a motívum azonosítója. Olvasva: `adat/motivumok.tsv:4` (`azonossag_tipusa`=formulaikus, `negativ_kriterium`, `folerendelt_fogalom`), a `motivumok/ISTENTISZT-001.md` egésze, a `jeloltek.tsv` 138 ISTENTISZT-001-sora (`split('\t')`; 24 beépítve = 22 `elofordulas` + 2 `motivumkozi`, 111 elutasítva, 3 nyitva), az `elofordulasok.tsv` 22 sora (`gerinc_elem`: 16× H7121+H8034, 6× G1941), az `elutasitasi_okok.tsv`, a fenti Gépi rész, a `naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv` `besem_JHVH_nelkul` blokkja; a Strong-tokenek saját lekérdezéssel (TAGNT/TAHOT). Az első kör K1–K5 kérdését és a felhasználói besorolást (DT476, DT478) tényként nem vettem át: a határt újra az adatból olvastam ki; ahol az adat a döntést már tükrözi (1Pét 1:17, 2Tim 2:22, Róm 10:12, 14 kint; a hét névmási ragos hely kint; Zsolt 99:6 kint; 1Kir 18:25–26 kivételként bent), azt nem kérdezem újra.

**2 kérdés az 1. kérdéshez (következetlen határ), 0 kérdés a 2. kérdéshez (hígulás), 1 szövegfeszültség-kérdés a kritérium és egy beépített sor indoklása között.** Mind kérdés a felhasználóhoz, nem javítás; egyik sem új igehely-javaslat.

**K6 — Következetlen határ (1. kérdés): a „besém után névmási rag, nem JHVH” kizáró ok a héber oldalon hét helyet zárt ki, a görög oldalon ugyanez a szerkezet (ὄνομά σου, ὄνομα τοῦτο) két beépített soron áll.**
(a) Az Ézs 64:6 („nevedet”, *bismchá*, 2. személyű rag, a megszólított Isten) azért elutasított, mert a *besém* után nem JHVH, hanem névmási rag áll; az ApCsel 9:14 („a te nevedet”, τὸ ὄνομά σου, 2. személyű névmás, a megszólított Úr) ugyanilyen szerkezettel beépített, és az ApCsel 9:21 („ezt a nevet”, τὸ ὄνομα τοῦτο) is név szerinti megnevezés nélkül.
(b) `adat/jeloltek.tsv:680` (Ézs 64:6, elutasítva): „a besém után nem a JHVH (H3068) szó áll, hanem névmási rag (bismchá, „nevedet”)” — ugyanezzel az indokkal `:53` (Jer 10:25), `:54` (Zsolt 79:6), `:50`/`:51`/`:52` (Zsolt 105:1, 1Krón 16:8, Ézs 12:4: *bismó*), `:38` (Zak 13:9: *bismí*) ↔ `adat/jeloltek.tsv:47` (ApCsel 9:14, beépítve): „»…mindazokat…, kik a te nevedet segítségül hívják« — Saul üldözési célpontjainak leírása” és `:48` (ApCsel 9:21, beépítve): „»…a kik ezt a nevet hívják segítségül« — az ApCsel 9:14-es leírás közvetlen megismétlése”. Saját mérés: TAHOT Ézs 64:6 = H0369 אֵין + H7121 קוֹרֵא + H9003 בְ + H8034 שִׁמְ + H9021 ךָ (`konkordancia/TAHOT_kivonat.tsv:464020–464024`); TAGNT ApCsel 9:14 = G1941 ἐπικαλουμένους + G3686 ὄνομά + G4771 σου (`konkordancia/TAGNT_kivonat.tsv:72773–72776`), ApCsel 9:21 = G1941 + G3686 ὄνομα + G3778 τοῦτο (`:72912–72915`); κύριος (G2962) egyik ApCsel-versben sincs, a másik négy görög helyen van (ApCsel 2:21, Róm 10:13: ὄνομα κυρίου; 1Kor 1:2: ὄνομα τοῦ κυρίου ἡμῶν Ἰησοῦ Χριστοῦ; ApCsel 22:16: a TAGNT alapszövegében αὐτοῦ, NA-jelöléssel, TR-token nélkül — a Károli „az Úrnak nevét” a TR-t követi).
(c) A `motivumok.tsv:4` negatív kritériuma a héber oldalon a *besém* utáni JHVH szót kéri (névmási rag kizár: DT478), a görög oldalon csak az ὄνομα meglétét (DT476 K2); a két fél így nem ugyanazt a jegyet méri: a héber a név *kimondását*, a görög a név *szavának* jelenlétét. Kérdés: szándékolt-e, hogy a görög oldalon a névmással vagy mutató névmással álló „név” elég (akkor a héber névmási ragos helyek kizárása a formula más szintjén áll, és ezt a kritériumnak ki kell mondania), vagy a görög oldalon is a megnevezett Úr (κύριος / Ἰησοῦς) kell a név után (akkor az ApCsel 9:14 és 9:21 ugyanazon az alapon áll, mint az Ézs 64:6)? Az ApCsel 22:16-nál külön: a TR-alapú Károli és a TAGNT alapszövege két különböző jegyet mutat (κυρίου ↔ αὐτοῦ); az ALVIL-001 kritériuma ilyen esetben a Károli alapszövegét (TR) nevezi irányadónak (`motivumok.tsv:6`), itt ez nincs kimondva.

**K7 — Következetlen határ (1. kérdés): az összesítő elutasító sor az *elóhím*-ot kizáró jegyként nevezi meg, miközben a *besém* + *elóhím* szerkezet az adatban csak beépített soron áll (1Kir 18:25).**
(a) A `besem_JHVH_nelkul` összesítő sor indoklása szerint a *besém* után álló „névmási rag, más név vagy az elóhím” kizár; az 1Kir 18:25 beépített sorának indoklása ugyanezt a jegyet (*elohéchem*) nevezi meg, kivételként.
(b) `adat/jeloltek.tsv:693` (2Móz 31:2, elutasítva, összesítő sor 12 versre): „a kárá és a besém egy szerkezetben áll, de a név után nem az Úr neve, a JHVH áll, hanem névmási rag, más név vagy az elóhím” ↔ `adat/jeloltek.tsv:34` (1Kir 18:25, beépítve): „a besém után nem JHVH áll, hanem elohéchem („a ti isteneteknek”)” (és `:35`, 1Kir 18:26: „ha-Báal”). Saját mérés: a blokk 12 verse (`naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv`, `besem_JHVH_nelkul`: 1Krón 6:65, 2Móz 31:2, 2Móz 35:30, 4Móz 32:38, 4Móz 32:42, Eszt 2:14, Józs 21:9, Zsolt 49:12, Ézs 43:7, Ézs 45:4, Ézs 48:1, Ézs 65:1) között egy sincs, ahol a *besém* után אֱלֹהִים (H0430) állna; a קָרָא + בְּ + שֵׁם + H0430 lánc a motívum vizsgált helyei közül a TAHOT szerint az 1Kir 18:24-ben (`TAHOT_kivonat.tsv:202412–202415`, Illés felszólítása) és az 1Kir 18:25-ben (`:202466–202469`) áll — mindkettő beépített.
(c) A kivétel a `motivumok.tsv:4` kritériumában szerepel („Kivétel: a kontrasztként megtartott 1Kir 18:25–26”), az összesítő sor indoklásában nem; így a két szöveg ugyanazt a jegyet ellentétes irányban használja, és az összesítő sor egy olyan kizáró jegyet nevez meg, amelyet a blokk 12 verse közül egy sem hordoz. Kérdés: az „vagy az elóhím” az összesítő sorban a határ része (akkor a kivételt ott is ki kell mondani), vagy egy nem előforduló eset maradványa?

**K8 — Szövegfeszültség a kritérium és a beépített sor indoklása között (az 1. kérdéshez; a DT476 K4 után maradt): a kritérium „aktív, invokáló szerkezet: »[valaki] hívja segítségül az Úr nevét«” feltételét a 2Móz 33:19 és 34:5 saját indoklása tagadja.**
(a) A `motivumok.tsv:4` negatív kritériuma két jegyet kér egyszerre (invokáló szerkezet; a *besém* után JHVH); a két B-sor a másodikat teljesíti, az elsőt a saját indoklása szerint nem.
(b) `adat/motivumok.tsv:4`: „az igehelynek a קָרָא (kárá) + בְּשֵׁם (besém) + יְהוָה (JHVH) mintát kell mutatnia (aktív, invokáló szerkezet: "[valaki] hívja segítségül az Úr nevét")” ↔ `adat/jeloltek.tsv:55` (2Móz 33:19, beépítve): „nem az ember hívja segítségül Isten nevét, hanem Isten mondja ki a sajátját” (ugyanígy `:56`, 2Móz 34:5; `adat/elofordulasok.tsv:30–31`: `jelentes_szam`=3 „kihirdetni”, `funkcio`=„❓ be nem sorolható”). Az elutasított oldalon az ApCsel 7:59 (`:598`) indoka „invokáció a … formulán kívül”: ott invokáció van formula nélkül, a B-sorokon formula van invokáció nélkül — a kritérium „invokáló” szava csak az elsőt zárja ki.
(c) A DT476 K4 a határt a *besém* utáni JHVH-ra tette, és a B-sorok e szerint bent vannak; a kritérium szövege viszont továbbra is az invokációt is feltételként mondja ki. Kérdés: a kritériumban az „aktív, invokáló szerkezet” leíró jellemzés (akkor a B-sorok rendben vannak, és a mondat nem feltétel), vagy feltétel (akkor a B-sorok a saját indoklásuk szerint nem teljesítik)? Nem döntök; a kérdés csak azt rögzíti, hogy a két szöveg ma nem ugyanazt mondja.

**Hígulás (2. kérdés): 0 kérdés.** Mind a 22 beépített sor a motívum saját szerkezetét hordozza (TAHOT/TAGNT: 16× קָרָא + בְּ + שֵׁם, 6× ἐπικαλέομαι + ὄνομα; a Gépi rész 2. pontjával egyezően), tehát egyik sem a fölérendelt fogalmon („bármely invokációs forma, a קָרָא בְשֵׁם formulán kívül”) keresztül tartozik ide. A két szélső csoport (1Kir 18:25–26: a formula hamis isten nevével; 2Móz 33:19, 34:5: a formula invokáció nélkül) a hígulás fordítottja — forma igen, a cél vagy a funkció tér el —, ezeket a K7 és a K8 mint határkérdést, nem mint hígulást rögzíti. Az üres eredmény nem negatív lelet: a fölérendelt fogalom felé mutató sorok (Zsolt 50:15, 91:15, 86:5, Jer 29:12, Ézs 58:9, 65:24; ApCsel 7:59; 2Tim 2:22, Róm 10:12, 14; 1Pét 1:17) mind elutasítottként állnak az adatban, egységes indokkal.

*Nem kérdés (megjegyzés):* (1) `adat/jeloltek.tsv:533–534` (1Pét 1:6, 1:7, elutasítva) indoklása azt mondja, hogy a Zak 13:9 célhelyei közül „a formulát … Jóel 2:32, ApCsel 2:21 és Róm 10:14 mellett egyedül a Róm 10:12 tartalmazza” — a Róm 10:12 és 10:14 a DT476 K2 óta éppen a formula (ὄνομα) hiánya miatt elutasított, tehát az indoklás előfeltevése elavult; a döntés (elutasítva) ettől nem változik. (2) A görög oldali `gerinc_elem` mind a hat soron G1941 egyedül, az ὄνομα (G3686) nem része; a Gépi rész 2. pontja ezért a görög kritérium név-feltételét nem méri (a név nélküli ApCsel 7:59 is átmenne rajta). (3) A D-minta (`:596–615`, `:672–678`), a jogi fellebbezés (`:606–611`), az esküformás tanúhívás (`:595`), a névadás (`:541–546`) és a név nélküli héber hívás (`:535–540`) kizárása egységes, beépített párja nincs. (4) Az 1Kir 18:24 (`:33`) mindkét felét hordozza (H0430 és H3068 a *sém* után), a sor Illés hívásán áll.

(proveniencia: scope=adat/motivumok.tsv:4,6 + adat/jeloltek.tsv (id=ISTENTISZT-001, 138 sor) + adat/elofordulasok.tsv (id=ISTENTISZT-001, 22 sor) + adat/elutasitasi_okok.tsv + adat/motivum_kapcsolatok.tsv (3 sor) + motivumok/ISTENTISZT-001.md + naplok/HATAR_ISTENTISZT-001.md (Gépi rész) + naplok/F123_teljesseg_ISTENTISZT-001_blokkok.tsv (besem_JHVH_nelkul) + konkordancia/TAGNT_kivonat.tsv (ApCsel 2:21, 9:14, 9:21, 22:16; Róm 10:13; 1Kor 1:2) + konkordancia/TAHOT_kivonat.tsv (1Kir 18:24–26; Ézs 64:6, 65:1; Zsolt 79:6); split('\t') | forras=modell:claude-fable-5-1 | ts=2026-11-09T19:20Z)

**Szerkesztői besorolás, második kör** *(nem a modell írta; 2026-11-11, a #194-ben átvezetve: F194.1)*

- K6: „(A) Kikerül” — a görög oldalon is az Úr megnevezése kell a név után; az ApCsel 9:14 és 9:21 a fölérendelt fogalomhoz kerül (22 → 20). Az ApCsel 22:16 marad (a Károli alapszövege, a Textus Receptus: κυρίου). (DT-F194a)
- K7: a „vagy az elóhím” maradvány, kikerül az összesítő sor indoklásából és az elutasítási ok magyarázatából; saját mérés (TAHOT): a 12 versben a *besém* után sehol nem áll אֱלֹהִים (elóhím). Az orkesztrátor döntése. (DT-F194d)
- K8: az „invokáló” marad a kritériumban; a 2Móz 33:19 és 34:5 kivételjelölés nélkül tartozik ide: „a szavak ugyanazok az forditói döntés hogy ez kihirdetés”. (DT-F194b)
- A tetragramma alakja mindenütt יְהוָה (Jahve): „Igen, mindenhol Jahve”. (DT-F194c)

*(proveniencia: scope=adat/motivumok.tsv (ISTENTISZT-001) + adat/jeloltek.tsv (ISTENTISZT-001, elofordulas) + TAHOT_kivonat.tsv (a besem_JHVH_nelkul blokk 12 verse) | forras=manual: a felhasználó döntései (AskUserQuestion, az orkesztrátoron át) | ts=2026-11-11)*
<!-- HATÁRDÖNTÉS: n=20 ujjd=4460c4ab6a6b | DT-F194a, DT-F194b, DT-F194c, DT-F194d -->
<!-- MODELLES-VEGE -->
