# HATAR_ALVIL-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum ALVIL-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=ALVIL-001 | ts=2026-11-08T15:08Z | bemenet=adat/elofordulasok.tsv@dfb0de82a1,adat/motivumok.tsv@e1d84722b1,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** ALVIL-001 — Hádész (Seol) — a halottak birodalma · hordozó: `lexikai` · fölérendelt fogalom: „a halál és a túlvilág általában, a halottak birodalmának megnevezése nélkül” · beépített sor: 74 (75 vers)

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

<!-- SORÁLLAPOT: n=74 ujj=460c69bb3460 -->

*Független második vélemény (hatar-ellenor), bemenet: csak az azonosító. A gépi rész eredményét (részhalmaz, gerinc-kombináció) nem ismétli. Minden pont kérdés a felhasználóhoz, nem javítás. Ez a rész a 2026-11-02-i modelles részt váltja: annak két kérdése (Mt 16:18, 1Kor 15:55) a mai adatban nem áll fenn — mindkét hely beépített (`adat/jeloltek.tsv:345`, `:346`), és a negatív kritérium (`adat/motivumok.tsv:6`) a Károli alapszövegét (TR) nevezi mércének.*

**1 kérdés.** Kérdés a felhasználóhoz, nem javítás; nem új igehely-javaslat. A következetlen-határ vizsgálat üres (lent, *Nem kérdés*).

**K1 — Hígulás (2. kérdés): az Ézs 7:11 az egyetlen beépített hely, ahol a héber alak nem a seól névszói alakja, és a Septuaginta meg a Károli is „mélység”-et olvas — a hely a lexémán vagy a „mélység” értelmén keresztül tartozik ide?**
(a) A kimondott kritérium szerint a versben a héber szövegben a שְׁאוֹל (seól) szónak kell állnia; az Ézs 7:11-ben a TAHOT H7585-címkét ad egy olyan alakra, amely a 66 H7585-sor közül egyedül nem she.'ol / she.'o.la alakú, miközben a két fordítás (LXX, Károli) ugyanitt nem a halottak birodalmát, hanem a mélységet olvassa.
(b) `konkordancia/TAHOT_kivonat.tsv:324856` — „Ézs 7:11	H7585	שְׁאָ֔לָה	she.'A.lah	שְׁאוֹל	Hell	[as] Sheol” (előtte `:324855` — „הַעְמֵ֣ק … be deep	make deep”); `konkordancia/Karoli_1908.tsv:17858` — „Kérj jelt magadnak az Úrtól, a te Istenedtől, kérj a mélységben vagy fent a magasban!”; `naplok/F123_ALVIL2_lxx_hid.tsv:58` — „Ézs 7:11	seól → más”; `adat/elofordulasok.tsv:119` (beépítve) — „karoli_szo=a mélységben … megbizhatosag=közepes”, kapcsolodas: „A héber szöveg itt a Seolt nevezi meg”. A kritérium: `adat/motivumok.tsv:6` — „A versben a héber szövegben a שְׁאוֹל (seól) … szó áll; … Ahol a Károli sírt, koporsót, poklot vagy mélységet ír, de az eredetiben más szó áll …, az nem tartozik ide”. Az adat a beépítés mellett szól: a TAHOT H7585-öt ad, és a BDB a szócikk fejében ezt az alakot a seól alá sorolja (`naplok/F123_adat_ALVIL-001_szotar.tsv:42` — „H7585. sheol שְׁאָ֫לָה Isa 7:11 see שְׁאוֺל 1 below”).
(c) A határ itt a Strong-címkén és a szótári besoroláson múlik, nem az alakon: a Károli-szó („mélységben”) épp az, amelyet a kritérium máshol kizáró jelnek vesz, és a Septuaginta sem hoz ᾍδης-t. A kérdés: elég-e a Strong/BDB-besorolás, vagy a lap jelölje a helyet úgy, ahogy a kritérium az 1Kor 15:55 eltérését jelöli (a sor `közepes` megbízhatósága erre utal, de a forrás nem mondja ki).

*Nem kérdés (ellenőrizve):*
- **Következetlen határ (1. kérdés): 0 kérdés.** 74 beépített és 36 elutasított sor (`adat/jeloltek.tsv:98–169, 345–346` ill. `:694–729`), átfedés nincs. Mind a 36 elutasítás egy indokon áll („a versben a seól, illetve a hádész szava nem áll”, öt indok-osztály: `adat/elutasitasi_okok.tsv` 4–8. sor), és egyetlen elutasított igehely sem áll a TAHOT H7585- vagy a TAGNT G0086-listáján (saját mérés: elutasított ∩ TAHOT/TAGNT = ∅); a beépített sorok indoklása sehol nem egyezik elutasítottéval. A TR-mérce két oldala összhangban: az 1Kor 15:55 bent (Károli „Pokol!”, `konkordancia/Karoli_1908.tsv:28830`; a TAGNT második θάνατε-ja TR és Byz nélkül, `konkordancia/TAGNT_kivonat.tsv:99823`), az ApCsel 2:24 kint (θανάτου TR+Byz címkével, `:67915`; Károli „a halál fájdalmait”, `Karoli_1908.tsv:27034`). Két megjegyzés, nem határkérdés: a `jeloltek.tsv:714` „a ᾅδου csak szövegváltozat” állítása a TAGNT-ból nem olvasható ki (a TAGNT TR-en kívüli változatot nem rögzít), a döntést nem érinti; a Jób 38:17 a forrásban a nyolc LXX-többlet közt áll (`motivumok/ALVIL-001.md:147`), az adatban a „szótári összevető” osztályban (`jeloltek.tsv:704`) — mindkét helyen kint.
- **Hígulás a többi 73 soron: 0 kérdés.** A 64 ÓSZ-sor (`gerinc_elem`=H7585) a TAHOT 64 H7585-igehelye, két irányban eltérés nélkül; a 9 ÚSZ-sor 10 verse (Jel 20:13–14 egy sor) a TAGNT 10 G0086-verse, eltérés nélkül; az 1Kor 15:55 a kimondott TR-kivétel szerint, a lapon jelölve (a TAGNT-ban G0086 nincs ezen a versen, a `gerinc_elem`=G0086 tehát a TR-ből, nem a repó Strong-adatából áll). A hasonlat- és mérték-használatok (Én 8:6; Péld 27:20; 30:16; Hab 2:5; Jób 11:8) a lexikai hordozón nem hígulás. Üres eredmény, nem negatív lelet.

(proveniencia: scope=adat/motivumok.tsv:6, motivumok/ALVIL-001.md, adat/jeloltek.tsv (ALVIL-001 sorai: 98–169, 345–346, 694–729; motívumközi 681–682), adat/elutasitasi_okok.tsv, adat/elofordulasok.tsv:73–146, naplok/HATAR_ALVIL-001.md (Gépi rész), konkordancia/TAHOT_kivonat.tsv (H7585-szűrés; Ézs 7:11 teljes vers), konkordancia/TAGNT_kivonat.tsv (G0086-szűrés; 1Kor 15:55, ApCsel 2:24), konkordancia/Karoli_1908.tsv (Ézs 7:11, 1Kor 15:55, ApCsel 2:24), adat/bdb_vers_jelentes.tsv (Ézs 7:11), naplok/F123_ALVIL2_lxx_hid.tsv:58, naplok/F123_adat_ALVIL-001_szotar.tsv:42, naplok/F123_teljesseg_ALVIL-001.md:73 | forras=modell:claude-fable-5-1 | ts=2026-11-09T19:22Z)
<!-- MODELLES-VEGE -->
