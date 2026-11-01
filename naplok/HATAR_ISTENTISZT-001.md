# HATAR_ISTENTISZT-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum ISTENTISZT-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=ISTENTISZT-001 | ts=2026-10-29T15:36Z | bemenet=adat/elofordulasok.tsv@5c626f5332,adat/motivumok.tsv@857a6e31c8,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** ISTENTISZT-001 — Segítségül hívni az Úr nevét · hordozó: `formulaikus` · fölérendelt fogalom: istentisztelet/imádság általában (bármely invokációs forma, a קָרָא בְשֵׁם (kárá besém) formulán kívül) · beépített sor: 33 (33 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), ISTENTISZT-001 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (33 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | ISTENTISZT-001 versei | másik versei | közös | közös/ISTENTISZT-001 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ALVIL-001 | 33 | 73 | 0 | 0% | 0% | 3, 4 |
| ANTROP-001 | 33 | 8 | 0 | 0% | 0% | nincs |
| HAMART-001 | 33 | 77 | 0 | 0% | 0% | 5 |
| HODIT-001 | 33 | 33 | 0 | 0% | 0% | nincs |
| KIRALY-001 | 33 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 33 | 11 | 0 | 0% | 0% | nincs |
| TEREMT-001 | 33 | 45 | 0 | 0% | 0% | nincs |
| TEREMT-002 | 33 | 3 | 0 | 0% | 0% | nincs |

### 2. Negatív kritérium a beépített sorokon

Módszer: a #150 `jelolt_eloszures.vizsgal` próbája a **beépített** sorokra: a motívum gerinc-kombinációi (`elofordulasok.tsv` `strong`, nyelvtani Strongok nélkül) közül legalább egy teljesen megvan-e a sor versének Strong-halmazában (TAHOT+TAGNT). Hordozó: `formulaikus`.

Összesítés: 33 beépített sor; gerinc-kombináció megvan: 33; **kérdés (hiányzik): 0**; nem ellenőrizhető (nincs szövegadat / nincs kombináció): 0.

**0 kérdés.** Mind a 33 ellenőrizhető beépített sor versében megvan legalább egy gerinc-kombináció.

## Modelles rész

<!-- MODELLES-KEZDET -->
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
<!-- MODELLES-VEGE -->
