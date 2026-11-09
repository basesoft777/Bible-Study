# HATAR_ALVIL-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum ALVIL-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=ALVIL-001 | ts=2026-11-08T15:08Z | bemenet=adat/elofordulasok.tsv@dfb0de82a1,adat/motivumok.tsv@e1d84722b1,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** ALVIL-001 — Hádész (Seol) — a halottak birodalma · hordozó: `lexikai` · fölérendelt fogalom: a halál és a túlvilág általában, a halottak birodalmának megnevezése nélkül · beépített sor: 74 (75 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), ALVIL-001 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (75 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | ALVIL-001 versei | másik versei | közös | közös/ALVIL-001 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ANTROP-001 | 75 | 11 | 0 | 0% | 0% | nincs |
| HAMART-001 | 75 | 56 | 0 | 0% | 0% | nincs |
| HODIT-001 | 75 | 33 | 2 | 3% | 6% | nincs |
| ISTENTISZT-001 | 75 | 22 | 0 | 0% | 0% | 3, 4 |
| KIRALY-001 | 75 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 75 | 11 | 0 | 0% | 0% | nincs |
| TEREMT-001 | 75 | 45 | 1 | 1% | 2% | nincs |
| TEREMT-002 | 75 | 3 | 0 | 0% | 0% | nincs |

### 2. Negatív kritérium a beépített sorokon

**a hordozó lexikai: a gépi negatív-kritérium próba nem fut.** A hordozó (`azonossag_tipusa`) = `lexikai` (`adat/motivumok.tsv:6`). A #150 szókapcsolat-próbája csak formulaikus hordozón dönt (`naplok/JELOLT_ELOSZURES_naplo.md`; a lexikai kiterjesztés az N-F150a). A negatív kritérium itt tartalmi, nem gépi: a modelles résznek (ha lesz) kérdése, nem ennek a szakasznak.

## Modelles rész

<!-- MODELLES-KEZDET -->

*Független második vélemény (hatar-ellenor), bemenet: csak az azonosító. A gépi rész eredményét (részhalmaz, gerinc-kombináció) nem ismétli. Minden pont kérdés a felhasználóhoz, nem javítás.*

**2 kérdés.** Mind kérdés a felhasználóhoz, nem javítás; egyik sem új igehely-javaslat. A hígulás-vizsgálat üres (lent, *Nem kérdés*).

**K1 — Következetlen határ (1. kérdés): az Mt 16:18 tartalmi okból kizárt, a Luk 10:15 / Mt 11:23 ugyanazzal a jellemzéssel beépített, a hordozó pedig lexikai.**
(a) Az Mt 16:18 tartalmi okból van elutasítva („nem a halál/feltámadás-tipológia, külön motívum”), miközben a Luk 10:15 / Mt 11:23 beépítve áll, holott a forrás ugyanezt mondja róluk — a hordozó pedig `lexikai`, és a negatív kritérium csak a lexémát kéri, amely az Mt 16:18-ban megvan.
(b) `adat/jeloltek.tsv:346` (Mt 16:18, elutasítva): „ekkleziológiai kontextus (az egyház legyőzhetetlensége), tartalmilag nem kapcsolódik a jelen tanulmány tárgyához (halál/feltámadás-tipológia) — külön motívumként kezelendő, ha sorra kerül” ↔ `motivumok/ALVIL-001.md:54` a beépített Luk 10:15 / Mt 11:23-ról (`adat/elofordulasok.tsv:143`, `:144`): „tehát nem a jelen tanulmány fő ívéhez (Krisztus legyőzi a halált) kapcsolódik, hanem egy **másik, önálló bibliai mintázathoz** (a gőg isteni megalázása). Jelzésre érdemes, de a fő tipológiai ívbe nem illesztendő bele.” A kritérium: `adat/motivumok.tsv:6` — „az igehelynek a שְׁאוֹל (seól) gyököt (ÚSZ-ben az LXX-közvetített ᾍδης (hadész) megfelelőjét) kell tartalmaznia”; saját mérés (TAGNT): `konkordancia/TAGNT_kivonat.tsv:9750` — „Mt 16:18	G0086	ᾅδου … NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz”.
(c) Ugyanaz az indok („nem a fő tipológiai ív, önálló mintázat”) egyszer kizár, egyszer beenged; a TAGNT 10 G0086-verséből 9 beépített, az egyetlen kizárt a Mt 16:18 — a határ itt nem a kimondott (lexikai) kritérium szerint fut.

**K2 — Következetlen határ (1. kérdés, adat vs. forrás): az 1Kor 15:55 szövegkritikai okból kizárt, a beépített Hós 13:14 sor és a kivonat fő íve viszont erre a helyre épít.**
(a) Az 1Kor 15:55 szövegkritikai okból elutasított, de a beépített Hós 13:14 sor és a forrás kivonata épp az 1Kor 15:55-ös idézetre mint a motívum „legfontosabb lelet”-ére épít; a negatív kritérium nem mondja ki, melyik görög szöveg (kritikai vagy Károli/TR) a mérce.
(b) `adat/jeloltek.tsv:345` (1Kor 15:55, elutasítva): „a kritikai szövegkiadás mindkét tagmondatban θάνατος-t hoz; a TR/Byzantinus-alapú Károli-olvasat eltérése szövegkritikai kérdés, nem a jelen scan tárgya” ↔ `adat/elofordulasok.tsv:133` (Hós 13:14, beépítve): „"Hol van a te veszedelmed, oh Seol?" — Pál idézi 1Kor 15:55-ben, ⭐ kiemelt lelet”; `motivumok/ALVIL-001.md:13`: „A legfontosabb lelet Hós 13:14, amelyet Pál explicit idéz/parafrazál 1Kor 15:55-ben”. Saját mérés (TAGNT): az 1Kor 15:55 sorai közt nincs G0086; a második θάνατε kiadásjelzése „NA28+NA27+Tyn+SBL+WH+Treg” (TR és Byz nélkül), tehát az elutasítás az adatból igazolt, a Károli „Pokol” a TR-olvasat.
(c) A határ az ÚSZ-ben a kritikai szöveg szerint fut (1Kor 15:55 kint), a motívum fő íve viszont a kint hagyott helyre támaszkodik; a kettő egyszerre áll az adatban és a forrásban.

*Nem kérdés (hígulás, 2. kérdés — ellenőrizve, 0 kérdés):* mind a 72 beépített sor hordozza a lexémát: a 64 ÓSZ-sor (`gerinc_elem`=H7585) mindegyike a TAHOT 64 H7585-igehelyének egyike (66 szóelőfordulás; beépített-de-TAHOT-hiányos: 0, TAHOT-de-nem-beépített: 0); a 8 ÚSZ-sor 9 verse (Jel 20:13-14 két vers) mind a TAGNT G0086-sorai közt áll. A fölérendelt fogalmon („a halál/túlvilág fogalma általában, a lexémán kívül”) keresztül egyetlen beépített sor sem tartozik ide. A Seol nélküli, elutasított három hely (`adat/jeloltek.tsv:640–642`) a kimondott kritériummal összhangban van kint. Üres eredmény, nem negatív lelet a tartalmi szóródásra (pl. Én 8:6, Hab 2:5, Péld 30:16 hasonlatként használja a Seolt) — ez a lexikai hordozón nem hígulás.

(proveniencia: scope=adat/motivumok.tsv:6, motivumok/ALVIL-001.md, adat/jeloltek.tsv (ALVIL-001 sorai: 98–169, 345–346, 640–642; motívumközi 632–633), adat/elutasitasi_okok.tsv, adat/elofordulasok.tsv:73–144, naplok/HATAR_ALVIL-001.md (Gépi rész), konkordancia/TAHOT_kivonat.tsv (H7585-szűrés), konkordancia/TAGNT_kivonat.tsv (G0086-szűrés, 1Kor 15:55) | forras=modell:claude-fable-5-1 | ts=2026-11-02T11:03Z)
<!-- MODELLES-VEGE -->
