# HATAR_TEREMT-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum TEREMT-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=TEREMT-001 | ts=2026-11-16T14:07Z | bemenet=adat/elofordulasok.tsv@9bc79289d1,adat/motivumok.tsv@2f73593719,adat/motivum_kapcsolatok.tsv@11ca35ce25,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** TEREMT-001 — Tehóm (תְּהוֹם) — Abüsszosz (ἄβυσσος): a mélység motívuma · hordozó: `lexikai` · fölérendelt fogalom: „vízi/kozmikus káosz-képzetek általában, a תְּהוֹם (tehóm) / ἄβυσσος (abüsszosz) lexémán kívül” · beépített sor: 42 (45 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), TEREMT-001 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (45 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | TEREMT-001 versei | másik versei | közös | közös/TEREMT-001 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ALVIL-001 | 45 | 75 | 1 | 2% | 1% | nincs |
| ANTROP-001 | 45 | 11 | 0 | 0% | 0% | nincs |
| HAMART-001 | 45 | 56 | 0 | 0% | 0% | nincs |
| HODIT-001 | 45 | 33 | 0 | 0% | 0% | nincs |
| ISTENTISZT-001 | 45 | 20 | 0 | 0% | 0% | nincs |
| KIRALY-001 | 45 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 45 | 11 | 0 | 0% | 0% | nincs |
| TEREMT-002 | 45 | 3 | 1 | 2% | 33% | nincs |

### 2. Negatív kritérium a beépített sorokon

**a hordozó lexikai: a gépi negatív-kritérium próba nem fut.** A hordozó (`azonossag_tipusa`) = `lexikai` (`adat/motivumok.tsv:5`). A #150 szókapcsolat-próbája csak formulaikus hordozón dönt (`naplok/JELOLT_ELOSZURES_naplo.md`; a lexikai kiterjesztés az N-F150a). A negatív kritérium itt tartalmi, nem gépi: a modelles résznek (ha lesz) kérdése, nem ennek a szakasznak.

## Modelles rész

<!-- MODELLES-KEZDET -->
*Második vélemény a mai adaton (42 beépített sor, 45 vers; az ág `claude/nervous-kare-9d2361`, 65753e88). Bemenet: a motívum azonosítója és a hívó határeset-listája (igehelyek, ítélet nélkül). Modell: `claude-sonnet-5-5` (kért: `sonnet`). Minden pont kérdés, nem javítás. A válaszok: `naplok/F239_hatar.md` 6. pont.*

**Negatív próba a megadott határeseteken.** Mindkét változat a TAHOT-ra (H8415) és a TAGNT-re (G0012) futott, a `naplok/F239_U1_TEREMT-001_lxx_g0012.tsv` az LXX-oldalt adja.
- **Szűk változat** (csak a héber H8415 vagy az ÚSZ G0012; ez az érvényes kritérium): kiesik az Ézs 44:27, Jób 41:31, Jób 36:16, Zsolt 71:21, Jób 42:8, Mik 7:19, Jón 2:4, Neh 9:11, 2Pét 2:4, Jel 21:1. Bent marad a többi: 2Móz 15:5 és 15:8, 1Móz 49:25, Péld 8:27 és 8:28, Jób 41:32, Zsolt 71:20, Jón 2:6, Ez 31:15, 1Móz 1:2, Róm 10:7, Luk 8:31, Jel 20:1 és 20:3. A Jel 20:2-ben nincs G0012, a Jel 20:1–3 sorral van bent.
- **Tág változat** (az LXX ἄβυσσος is számít): bejön az Ézs 44:27, Jób 41:31, Jób 36:16 és Zsolt 71:21, a többi nem változik.
- **Károli-látható változat** (a lexéma a magyar szövegben is felismerhető): a Jób 41:32 („a tenger megőszült”) kiesne. A szomszéd, elutasított Jób 41:31 (Károli: „örvényeid”, „mélységébe”) és a bent lévő Jón 2:6 („mély ár”) a magyar szövegben nem különböztethető meg a bent lévő Károli-alakoktól. A határ ezeknél csak a héber szón múlik.

Összesen 5 kérdés.

**K1 (következetlen határ): ugyanaz a minta, a Róm 10:7-nél más a döntés, mint a K2 négy versénél.**
(a) A K2 elutasítja azt a helyet, ahol a görög ἄβυσσος nem a tehómot fordítja. A Róm 10:7 ἄβυσσος-a ugyanilyen helyettesítés: Pál az 5Móz 30:13 „tengeren túl”-ját cseréli ἄβυσσος-ra, és ez a sor bent van. Az indok csak az, hogy az ÚSZ-nek nincs héber eredetije.
(b) `adat/jeloltek.tsv:961` (Zsolt 71:21, Septuaginta-többlet); `adat/jeloltek.tsv:92` (Róm 10:7: „ki száll le az abüsszoszba?”); `naplok/F239_hatar.md:43` (B5).
(c) A „görög szó dönt az ÚSZ-ben” és a „nem fordítás-tanúra épít” egy mércével mérve a Róm 10:7-et is érinti-e? A motívum `negativ_kriterium`-ának „LXX-közvetített ἄβυσσος” szövege a Róm 10:7-re és a Luk 8:31-re nem illik, mert az LXX-ben ott nincs ἄβυσσος.

**K2 (következetlen határ): ugyanazon a fejezeten belül a magyar szövegben azonos szókészletű helyek ellentétes döntést kaptak.**
(a) Jób 41:31 (elutasítva) és 41:32 (beépítve) egy leírásban áll, mindkettőben a Leviatán nyomában kavargó víz van. Ugyanígy a Jón 2:4 (elutasítva) és a Jón 2:6 (beépítve). A különbség kizárólag a héber szó (מְצוֹלָה, illetve tehóm).
(b) `adat/jeloltek.tsv:948` (a mecólá-összesítő sor); `adat/jeloltek.tsv:616` (Jób 41:32: „a Károli-szóalak nem azonosítja a lexémát, a TAHOT igen”).
(c) A határ itt nem a Károli-olvasó számára látható, hanem a héber szó. Ellenőrizhető-e ez a lap Károli-szövegéből? Az olvasói oldalon nincs jelzés.

**K3 (következetlen határ, nyomon követhetőség): három megadott határeset nem kapott saját sort.**
(a) A Mik 7:19, a Jón 2:4 és a Neh 9:11 csak a Jób 41:31 tízverses összesítő során belül elutasított; saját soruk nincs (H8415 és G0012 egyikben sincs). A Jón 2:6 saját soron bent van.
(b) `naplok/F239_U1_TEREMT-001_teljesseg_blokkok.tsv:88–90`; `adat/jeloltek.tsv:948` indoklása csak a Jób 41:31-re mond LXX-megállapítást.
(c) A többi vers LXX-állapota nincs kimondva, pedig az összesítő sor az ő döntésüket is hordozza.

**K4 (hígulás): a Jel 20:2 beépített vers a hordozó szó nélkül.**
(a) A 45 beépített vers a `Jel 20:1-3` tartomány-sor miatt a 20:2-t is tartalmazza; ebben a TAGNT szerint nincs G0012.
(b) `adat/elofordulasok.tsv:70`; `naplok/F239_hatar.md:23`, `:41` (B3).
(c) A „egyik sor sem csak a fölérendelt fogalmon át tartozik ide” állítás verssel számolva nem teljesen igaz: a 20:2 tagságát a tartomány-forma okozza, nem a lexéma.

**K5 (hígulás): a lexikai motívum sorainak többsége „tartalom-alapú” bizonyítékú.**
(a) A 42 beépített sorból 36-nál az `elofordulasok.tsv` `azonositas_modja` mezője „tartalom-alapú”, csak hat „szó-szintű-gépi” (1Móz 1:2, 7:11, 8:2, 49:25, 2Móz 15:5, 15:8).
(b) `adat/elofordulasok.tsv:44` (Zsolt 71:20), `:63` (Jón 2:6), `:252` (Jób 41:32).
(c) A lexikai kritérium és a „tartalom-alapú” címke ellentmond-e egymásnak, vagy a címke a retroaktív betöltés öröksége?

*(proveniencia: scope=adat/motivumok.tsv:5, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/elutasitasi_okok.tsv, naplok/HATAR_TEREMT-001.md, naplok/F239_hatar.md, naplok/ERVNAPLO_TEREMT-001.md, naplok/F239_U1_TEREMT-001_lxx_g0012.tsv, naplok/F239_U1_TEREMT-001_teljesseg_blokkok.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv | forras=modell:claude-sonnet-5-5 (hatar-ellenor) | ts=2026-11-23T12:48Z)*
*A határ lezárt: a fenti kérdések (K1–K5) és a szerkesztő kilenc kérdésének döntései a `jeloltek.tsv`-n és az adattáblákon át (F239.3, F239.7); a sorállapot a döntés állapota. Új modelles kör csak új, nem a határdöntésből eredő sor-változásnál.*

*A jel frissítve a próza után (F239 U3, 2026-11-23): az előfordulás-sorokban csak határon kívüli mező változott (funkcio, jelentes_szam, kapcsolodas, karoli_szo, lexikon_entry_id, lexikon_szotar, proveniencia; `naplok/F239_U3_hatarjel_frissit.py`); az igehelyek és a döntések azonosak.*

<!-- HATÁRDÖNTÉS: n=43 ujjd=0a017634e94d | DT-F239a, DT-F239b, DT-F239c, DT-F239d -->

<!-- MODELLES-VEGE -->
