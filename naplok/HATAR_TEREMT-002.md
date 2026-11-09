# HATAR_TEREMT-002.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum TEREMT-002`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=TEREMT-002 | ts=2026-11-08T15:08Z | bemenet=adat/elofordulasok.tsv@dfb0de82a1,adat/motivumok.tsv@e1d84722b1,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** TEREMT-002 — Tohu va-vohu (תֹהוּ וָבֹהוּ, tóhú vávóhú) — a föld kietlen és puszta állapota a teremtéskor és az ítéletkor · hordozó: `formulaikus` · fölérendelt fogalom: az isteni ítélet mint pusztulás / kozmikus felbomlás általában (prófétai pusztulás-, elsötétülés- és romhalmaz-képek), a תֹהוּ וָבֹהוּ (tohu va-vohu) páron kív… · beépített sor: 3 (3 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), TEREMT-002 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (3 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | TEREMT-002 versei | másik versei | közös | közös/TEREMT-002 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ALVIL-001 | 3 | 75 | 0 | 0% | 0% | nincs |
| ANTROP-001 | 3 | 11 | 0 | 0% | 0% | nincs |
| HAMART-001 | 3 | 56 | 0 | 0% | 0% | nincs |
| HODIT-001 | 3 | 33 | 0 | 0% | 0% | nincs |
| ISTENTISZT-001 | 3 | 22 | 0 | 0% | 0% | nincs |
| KIRALY-001 | 3 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 3 | 11 | 0 | 0% | 0% | nincs |
| TEREMT-001 | 3 | 45 | 1 | 33% | 2% | nincs |

### 2. Negatív kritérium a beépített sorokon

Módszer: a #150 `jelolt_eloszures.vizsgal` próbája a **beépített** sorokra: a motívum gerinc-kombinációi (`elofordulasok.tsv` `strong`, nyelvtani Strongok nélkül) közül legalább egy teljesen megvan-e a sor versének Strong-halmazában (TAHOT+TAGNT). Hordozó: `formulaikus`.

Összesítés: 3 beépített sor; gerinc-kombináció megvan: 3; **kérdés (hiányzik): 0**; nem ellenőrizhető (nincs szövegadat / nincs kombináció): 0.

**0 kérdés.** Mind a 3 ellenőrizhető beépített sor versében megvan legalább egy gerinc-kombináció.

## Modelles rész

<!-- MODELLES-KEZDET -->

*Független második vélemény (hatar-ellenor), bemenet: csak az azonosító. A gépi rész eredményét (részhalmaz, gerinc-kombináció) nem ismétli. Minden pont kérdés a felhasználóhoz, nem javítás.*

*A futás (`claude-fable-5-1`) a felhasználó kifejezett jóváhagyásával, kreditből (usage credits) történt: „Igen, mehet” (2026-11-02, az orkesztrátornak; DT-F151b: „Igen, indítsd”).*

**2 kérdés.** Mind kérdés a felhasználóhoz, nem javítás; egyik sem új igehely-javaslat. A következetlen-határ vizsgálat a motívum saját jelölt-sorain üres (lent, *Nem kérdés*); a két kérdés a hordozó és a kritérium viszonyát, illetve egy másik motívum sorának TEREMT-002-re tett állítását érinti.

**K1 — Hígulás (2. kérdés): az Ézs 34:11-ben a pár nem formulaként áll, hanem két külön birtokos szerkezetben; a hordozó `formulaikus`, a kritérium viszont csak egy-versen-belüli együttállást kér.**
(a) A motívum neve és hordozója a תֹהוּ וָבֹהוּ formula (a két szó a *va-* kötőszóval közvetlenül egymás mellett, ahogy az 1Móz 1:2-ben és a Jer 4:23-ban), a negatív kritérium azonban csak azt kéri, hogy H8414 és H0922 „egy versben” álljon — az Ézs 34:11-ben a két szó két külön szerkezet (קַו־תֹהוּ, אַבְנֵי־בֹהוּ) birtokosa, a kötőszó a két mérőeszközt köti, nem a két szót.
(b) `adat/motivumok.tsv:11` (hordozó és kritérium): „formulaikus … az igehelynek a תֹהוּ וָבֹהוּ (tohu va-vohu) szópárt kell tartalmaznia (H8414 + H0922 egy versben)” ↔ `motivumok/TEREMT-002.md:67` a beépített Ézs 34:11-ről (`adat/elofordulasok.tsv:251`): „Az Ézs 34:11-ben a pár szétválik: mindkét tagja egy-egy mérőeszköz birtokos szerkezetében (status constructus) áll”; saját mérés (TAHOT): `konkordancia/TAHOT_kivonat.tsv:334107–334111` — „Ézs 34:11	H6957	קַֽו … a measuring-line of” / „H8414	תֹ֖הוּ” / „H0068	אַבְנֵי … stones of” / „H0922	בֹֽהוּ”, szemben az 1Móz 1:2 (`:17`, `:19`) és a Jer 4:23 (`:349082`, `:349084`) közvetlen egymás mellett álló párjával.
(c) Ha a hordozó valóban a formula (a kötött szópár), az Ézs 34:11 a lexikai együttálláson és a fölérendelt fogalmon (ítélet mint pusztulás: Edom romhalmaz-képe) keresztül tartozik ide, nem a formulán — ha viszont a kritérium kollokációs (egy vers), akkor a hordozó megnevezése (`formulaikus`) pontatlan; a kettő közül melyik a határ, a felhasználó döntése, a három beépített sor közül ez az egyetlen, ahol a kettő eltérő eredményt ad.

**K2 — Következetlen határ (1. kérdés, motívumközi): a HAMART-001 egy jelölt-sora a Jer 4:28-at a TEREMT-002 tagjaként utasítja el, a TEREMT-002 adatában a Jer 4:28 nem szerepel, és a versben a pár sincs meg.**
(a) A HAMART-001 két elutasított sora (Jer 4:23, Jer 4:28) azonos indoklással a TEREMT-002-re hivatkozik mint a hely motívumára; a Jer 4:23-ra ez igaz, a Jer 4:28-ra nem: a TEREMT-002-nek sem jelölt-, sem előfordulás-sora nincs rá, és a vers nem tartalmazza a H8414+H0922 párt.
(b) `adat/jeloltek.tsv:442` (HAMART-001, Jer 4:28, elutasítva): „A Jer 4:23 a naplóban már rögzített "תהו/בהו — teremtés-visszavonás" motívum ([ID: TEREMT-002]) tagja — kereszt-motívum szennyeződés elkerülése (Q4)” ↔ a TEREMT-002 saját sorai: `adat/jeloltek.tsv:279–344` (66 sor, Jer 4:28 nincs köztük), `adat/elofordulasok.tsv:249–251` (1Móz 1:2, Jer 4:23, Ézs 34:11); saját mérés (TAHOT): a Jer 4:28 soraiban H8414/H0922 találat: 0. A sor a motívumot a régi névvel („teremtés-visszavonás”) idézi, amelyet a forrás nyitott kérdése kivezetettnek jelöl: `motivumok/TEREMT-002.md:215` — „A motívum nem a teremtés visszavonását állítja, hanem a föld visszarendeződését”.
(c) A TEREMT-002 határa innen nézve helyes (a Jer 4:28 kint van), de egy másik motívum adata a TEREMT-002 nevében tart kint egy helyet, amelyet a TEREMT-002 kritériuma nem fed — a Jer 4:28 így egyik motívumban sincs megvizsgálva a saját kritériumán; hogy ez a HAMART-001 soránál javítandó-e, vagy a TEREMT-002 jelölt-táblájába kell egy elutasított sor, a felhasználó döntése.

*Nem kérdés (következetlen határ a motívum saját sorain, 1. kérdés — ellenőrizve, 0 kérdés):* a 66 TEREMT-002 jelölt-sorból (`adat/jeloltek.tsv:279–344`) a 3 beépített mind kollokáció-találat (`forras_kereses`: „kollokacio H8414+H0922”), a 63 elutasított közül 58 indoklása „negatív kritérium: nincs H8414+H0922 pár …”, 5 „adathiba: az Isa.34.11 lista az Isa.40.11 másolata”; egyetlen elutasított sorban sincs meg a pár, egyetlen beépített sor indoklása sem azonos egy elutasítottéval. Az Ézs 45:18 és az Ézs 24:10 elutasított, és kapcsolat-sorként (`adat/kapcsolatok.tsv:33–34`) él tovább — ez a kimondott kritériummal összhangban van (a végpont nem előfordulás). Az `elutasitasi_okok.tsv` mintái közül a 10-es („nincs .* a versben”) illeszkedik az elutasítások egy részére, a TEREMT-002-nek saját mintája nincs — ez besorolási, nem határ-kérdés.

(proveniencia: scope=adat/motivumok.tsv:11, motivumok/TEREMT-002.md, adat/jeloltek.tsv (TEREMT-002 sorai: 279–344; motívumközi 441–442), adat/elutasitasi_okok.tsv, adat/elofordulasok.tsv:249–251, adat/kapcsolatok.tsv:30–34, naplok/HATAR_TEREMT-002.md (Gépi rész), konkordancia/TAHOT_kivonat.tsv (1Móz 1:2, Jer 4:23, Jer 4:28, Ézs 34:11 sorai, H8414/H0922/H6957/H0068-szűrés) | forras=modell:claude-fable-5-1 | ts=2026-11-02T13:20Z)
<!-- MODELLES-VEGE -->
