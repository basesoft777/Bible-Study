# HATAR_HAMART-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum HAMART-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=HAMART-001 | ts=2026-11-08T15:08Z | bemenet=adat/elofordulasok.tsv@dfb0de82a1,adat/motivumok.tsv@e1d84722b1,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** HAMART-001 — A bűn következményeinek gyűrűzése — átok, föld és romlás · hordozó: `strukturális` · fölérendelt fogalom: „a bűn és következményei általában, a genezisi lánc szavai és szerkezete nélkül” · beépített sor: 48 (56 vers)

## Gépi rész

### 1. Részhalmaz-vizsgálat (CLAUDE.md „Új motívum-ID”, 4. kérdés)

Módszer: a beépített igehelyek (`elofordulasok.tsv`) versekre bontva (tartomány = minden vers), HAMART-001 összes beépített versét minden más motívuméval összevetve, mindkét irányban. Kérdés: A ⊆ B, vagy |A ∩ B| / |A| ≥ 80% (A = az ellenőrzött oldal, B = a másik oldal; a fordított irányt külön vizsgálja).

**0 kérdés.** Egyik másik motívummal sem áll fenn részhalmaz-viszony vagy ≥80% átfedés (56 beépített vers vetve össze minden más motívum halmazával). Üres eredmény: nem negatív lelet a fogalmi átfedésre, csak az igehely-halmazra.

Az összevetés teljes táblája (nem kérdés; a küszöb alatti sorok is látszanak):

| másik motívum | HAMART-001 versei | másik versei | közös | közös/HAMART-001 | közös/másik | meglévő kapcsolat (`motivum_kapcsolatok.tsv` sora) |
|---|---|---|---|---|---|---|
| ALVIL-001 | 56 | 75 | 0 | 0% | 0% | nincs |
| ANTROP-001 | 56 | 11 | 0 | 0% | 0% | nincs |
| HODIT-001 | 56 | 33 | 0 | 0% | 0% | nincs |
| ISTENTISZT-001 | 56 | 22 | 0 | 0% | 0% | 5 |
| KIRALY-001 | 56 | 38 | 0 | 0% | 0% | nincs |
| MENNY-001 | 56 | 11 | 0 | 0% | 0% | nincs |
| TEREMT-001 | 56 | 45 | 0 | 0% | 0% | nincs |
| TEREMT-002 | 56 | 3 | 0 | 0% | 0% | nincs |

### 2. Negatív kritérium a beépített sorokon

**a hordozó strukturális: a gépi negatív-kritérium próba nem fut.** A hordozó (`azonossag_tipusa`) = `strukturális` (`adat/motivumok.tsv:10`). A #150 szókapcsolat-próbája csak formulaikus hordozón dönt (`naplok/JELOLT_ELOSZURES_naplo.md`; a lexikai kiterjesztés az N-F150a). A negatív kritérium itt tartalmi, nem gépi: a modelles résznek (ha lesz) kérdése, nem ennek a szakasznak.

## Modelles rész

<!-- MODELLES-KEZDET -->

<!-- SORÁLLAPOT: n=48 ujj=c477c896b6bd -->


*Második vélemény a mai adaton (48 beépített sor, 56 vers). Bemenet: csak a motívum azonosítója; a készítő sessionök összefoglalóit és a korábbi Modelles rész döntéseit nem vettem figyelembe, a határt az adatból olvastam ki. A 2026-11-08-i, 60 soros állapotra írt K1–K10 ezzel felülírva; nyoma a fájl git-történetében (3ba995c0, 6f42447a). A gépi rész két eredményét (részhalmaz: 0 kérdés; negatív kritérium: strukturális hordozón nem fut) nem ismétlem. Minden pont kérdés a felhasználóhoz, nem javítás; új igehelyet nem javaslok, nem döntök.*

**6 kérdés.** (1. kérdés = következetlen határ; 2. kérdés = hígulás a fölérendelt fogalom felé.)

**K1 — Az 1Móz 4:2-3 „Kain pedig földmívelő” mondata a föld szaván bent áll, az 1Móz 9:20 „Noé pedig földmívelő kezde lenni” mondata ugyanazzal a szóval „semleges, narratív adamá-használat” indokkal kint.**
- `adat/elofordulasok.tsv:206` — 1Móz 4:2-3, `gerinc_elem`=H0127, `funkcio`: „láncszem — az átkozott föld a következő nemzedéken; a testvéri viszály színtere”; `adat/jeloltek.tsv:230`: „Kain "földmívelő", és a földből hozza áldozatát: az átkozott föld a testvéri konfliktus színtere”.
- `adat/jeloltek.tsv:514` — 1Móz 9:20, elutasítva: „semleges, narratív adamá-használat, nem az átok-szerkezetben (napló 4/c, H0127 sor: genezisen belüli határeset)”. TAHOT: 1Móz 4:2 H5647+H0127 (óvéd adámá), 1Móz 9:20 H0376+H0127 (ís há-adámá); a Károli mindkettőt „földmívelő”-nek fordítja.
- Miért kérdés (1.): mindkét vers elbeszélő foglalkozás-megnevezés az átok szava nélkül, és a 4:2-3 beépítési indoka („az átkozott föld … színtere”) a versen kívüli összekötés, amelyet az indoklás a 9:20-nál nem mérlegel — a két sor közti határ nincs kimondva.

**K2 — Az Ez 12:19 a chámász szón, a „megtelt” ige nélkül bent áll, a Hab 2:8 és a Hab 2:17 ugyanezzel a szóval és ugyanazzal a föld + lakói szerkezettel „a szókapcsolat nélkül” indokkal kint.**
- `adat/elofordulasok.tsv:229` — Ez 12:19, `gerinc_elem`=H2555 (nem málé+chámász); `adat/jeloltek.tsv:664`: „A héber vers együtt hozza az erőszak (chámász, a Károliban »álnokság«), a föld (adamá) és a teljesség (melóá, a »megtelt« igének tövéből; a Károliban »bőség«) szavát, vagyis az 1Móz 6:11-13 szerkezetét.”
- `adat/jeloltek.tsv:258` — Hab 2:8, elutasítva: „A chámász szava itt a megtorlás elveként áll, a »megtelt erőszakkal« és a »hallatszik az erőszak« szókapcsolata nélkül, mint a csoportosan kizárt chámász-versekben.” (ugyanez `:259`, Hab 2:17). TAHOT: Ez 12:19 H2555 + H0127 („admat Jiszráél”) + H0776 + H4393 (melóá, főnév) + H3427, a H4390 ige nincs benne; Hab 2:8 és 2:17: H2555 + H0776 + H3427 („chámász erec … vechol jósvé váh”).
- Miért kérdés (1.): a gépi málé+chámász kollokáció (8 vers) az Ez 12:19-et nem tartalmazza, az adamá itt az „Izráel földje” országnév-szerkezetben áll (a kritérium a „föld mint ország” használatot kizárja), így a bent és a kint között egyedül a melóá főnév tő-érve áll, amelyet a Hab-soroknál az indoklás nem mérlegel.

**K3 — A Gal 3:13-14 beépítési indoka az 5Móz 21:23-ra épül („az átok és a föld együtt áll”), miközben az 5Móz 21:23 átok-szava a qelálá (H7045), amelyet a motívum saját kizárásai „nem a motívum szava”-ként kezelnek, és a vers maga csak blokk-kizárásban szerepel.**
- `adat/jeloltek.tsv:269` — Gal 3:13-14, beépítve: „Pál az 5Móz 21:23 átok-mondatát idézi, amelyben az átok és a föld együtt áll, a lánc görög átok-szavával (ἐπικατάρατος, epikataratosz); a kapcsolatot a 3:14 áldás-mondata adja, amely az 1Móz 12:3 ígéretét veszi fel.”
- `adat/jeloltek.tsv:742` — összesítő sor (13 vers): „a Károli »átok«-csoport szava (átok) ezekben a versekben a H7045 szót fordítja; a motívum saját szava a versekben nem áll.”; `adat/jeloltek.tsv:731` — a qalal 71 verse: „nem a negatív kritérium lexémája”; `adat/jeloltek.tsv:268` — Gal 3:10, elutasítva: „Pál az 5Móz 27:26 átok-mondatát idézi; az átok a tóra megszegőjére szól, a szövetség rendjében, a föld szava nélkül”. TAHOT 5Móz 21:23: H7045 (qilelat) + H0127 (admátekhá); `naplok/F123_teljesseg_HAMART-001.tsv:575`, `:1506`: a vers ELTÉRÉS-ként a H0127- és a Károli „átkozott”-hálóban, beépítés nélkül.
- Miért kérdés (1. és 2.): a Gal 3:10 forrásversében (5Móz 27:26) a lánc igéje (árar) áll, és a hely kint van; a Gal 3:13 forrásversében a kivezetett qalal-tő áll, és a hely bent van — a bent-állás így az áldás-mondaton és a „szövetség átka” fölérendelt fogalmán át áll, amit a sor maga „határeset”-nek jelöl.

**K4 — Az Ez 28:16, a Mik 6:12 és a Sof 1:9 a „megtelt erőszakkal” szópáron áll bent, de a megtelt dolog egyikben sem a föld (egy fejedelem belseje, a gazdagok, egy ház), és az indoklásuk a kritérium második feltételét (az erőszakkal megtelt föld kimondása vagy ismétlése) nem nevezi meg.**
- `adat/jeloltek.tsv:254` — Ez 28:16: „a kollokáció Tírusz fejedelmére”; `:256` — Mik 6:12: „a kollokáció Izráel gazdagjaira”; `:257` — Sof 1:9: „a kollokáció az úr házának megtöltésére”. TAHOT: Ez 28:16 H4390 + H8432 (tókh) + H2555; Mik 6:12 H4390 + H2555 (alany: a gazdagok); Sof 1:9 H4390 + H1004 (bét) + H2555; H0127 vagy H0776 egyikben sincs.
- `adat/motivumok.tsv:10` — negatív kritérium: „vagy a lánc szópárja (tövis és bogáncs; megtelt erőszakkal; hallatszik az erőszak), és a hely ezen a szón át az 1Móz 3–9 láncára utal vissza: az átkot a földön, a föld romlását, az erőszakkal megtelt földet vagy a föld színéről való eltörlést mondja ki, ismétli vagy fordítja meg.”
- Miért kérdés (2.): ha a szópár önmagában elég, a határ a kollokáció és nem a kritérium második mondata; ha nem elég, a három sor csak az erőszak mint bűn tágabb fogalmán át tartozik ide — a kettő közül az indoklás egyiket sem mondja ki.

**K5 — Az 1Móz 6:5 tematikus sorként bent áll, miközben a Jer 17:9, a Jer 4:14 és a Mt 15:19 / Mk 7:21-23 a „jetzer — a szív romlott hajlama” másik motívum tárgyaként kint, holott a jécer szó (H3336) éppen az 1Móz 6:5-ben áll.**
- `adat/elofordulasok.tsv:212` — 1Móz 6:5, `gerinc_elem`=„tematikus:1Móz 6:5”; `adat/jeloltek.tsv:236`: „רָעָה / רַע … — a diagnózis kiterjesztése: a gonoszság nem tettekben, hanem a szív minden gondolat-alkotásában”.
- `adat/jeloltek.tsv:347` — Jer 17:9, elutasítva: „a szív romlottsága a "jetzer — a szív romlott hajlama" motívum tárgya, amely a naplóban önálló tételként szerepel. Kereszt-motívum szennyeződés elkerülése (Q4)”; `:273` — Mt 15:19, elutasítva: „Ugyanaz a másik motívum, mint a Jer 17:9-nél: a szív romlott hajlama. A lánc egyetlen szava sem áll a versben, és az 1Móz 6:5, amelyre utal, maga is tematikus sor.” TAHOT 1Móz 6:5: H3336 (jécer) + H4284 + H3820 + H7451; a H7451 a lánc szavai közül kikerült (`adat/jeloltek.tsv:730`).
- Miért kérdés (1. és 2.): a sor jeloltek-indoklása a kivezetett רַע (ra) szón áll, a mai hordozó csak a név szerinti tematikus jelölés, és a Jer 17:9 kizárási indoka (a szív hajlama önálló motívum, Q4) szó szerint erre a versre is illik.

**K6 — Formai: a Gal 3:14 és a Zsid 6:7 a lánc szava nélkül a beépített tartomány része, a Róm 8:20 ugyanilyen helyzetben külön elutasított sor „folytatás” indokkal.**
- `adat/jeloltek.tsv:813` — Róm 8:20, elutasítva: „A hely a Róm 8:21 sorának folytatása: a teremtett világ »hiábavalóság alá vettetett«; a romlás szava (φθορά) a 8:21-ben áll, és az a motívumban van.”; `motivumok/HAMART-001.md:31`: „a Róm 8:20-22 érveléséből csak a 8:21, amelyben a romlás szava áll. A szomszédos versek saját sorban, elutasítva szerepelnek.”
- `adat/elofordulasok.tsv:243` — Gal 3:13-14 egy sorban, `adat/jeloltek.tsv:269`: „a kapcsolatot a 3:14 áldás-mondata adja”; `adat/elofordulasok.tsv:244` — Zsid 6:7-8 egy sorban, `adat/jeloltek.tsv:388` (Jer 12:13 kizárása): „ezt kizárólag a Zsid 6:8 hozza”; `motivumok/HAMART-001.md:31`: „Hét sor több verset fog össze, mert a hely egy összefüggő mondatban vagy szakaszban áll”. TAGNT: Gal 3:14, Zsid 6:7 és Róm 8:20 egyikében sincs a lánc görög szava (G1944, G2671, G5351, G5356, G1311, G0173, G5146); a Gal 3:13-ban G1944+G2671, a Zsid 6:8-ban G0173+G2671+G5146, a Róm 8:21-ben G5356 áll.
- Miért kérdés (1.): a „tartomány csak addig, ahol a lánc szava áll” szabály a Róm 8:20-22-n és az 5Móz 28:16-19-en érvényesül, a Gal 3:13-14-en és a Zsid 6:7-8-on nem, és a fájl „egy mondat” elve a Róm 8:20-21-re nincs megvizsgálva.

*Nem kérdés (összevetve, a határ következetes): az 1Móz 3:14 (Isten átka a kígyóra, a lánc első kimondása) az 1Móz 9:25 (Noé emberi átka) kizárásával szemben; az 1Móz 12:3 és az 5Móz 28:18 (árar + adámá egy versben) az 1Móz 27:29, 4Móz 24:9, 5Móz 27:15-26, 28:16-17, 28:19 (árar a föld szava nélkül) kizárásával szemben; a Zsolt 14:1 / 53:2 „egyetemes” hifíl sorok a „szövetséges nép” sáchat-kizárásokkal (5Móz 4:25, Bír 2:19, Sof 3:7, Hós 9:9, 5Móz 9:26-27) szemben; a „föld színéről” fordulat (1Móz 7:4, 7:23, Sof 1:2-3 bent; 1Kir 13:34, 14:15-16, 2Kir 17:22-23 kint) az egyetemes felsorolás határán; a négy sámá+chámász sor; a Hós 10:8 szópárja; a romlandó test és a sír-enyészet (1Kor 15, ApCsel 2 és 13, 1Pét 1) kizárása a Róm 8:21-gyel szemben; az Ez 28:17 és a Mik 6:13 „folytatás” kizárása a Róm 8:20/22-vel összhangban.*

(proveniencia: scope=adat/motivumok.tsv:10 (azonossag_tipusa, negativ_kriterium, folerendelt_fogalom), motivumok/HAMART-001.md (Kivonat, 1., 2., 7. szakasz), adat/jeloltek.tsv (HAMART-001: 335 sor, 48 beépítve, 287 elutasítva), adat/elutasitasi_okok.tsv (HAMART-001 minták), adat/elofordulasok.tsv (HAMART-001: 48 sor, gerinc_elem, jelentes_szam, funkcio), adat/motivum_kapcsolatok.tsv (HAMART-001: 1 sor), naplok/HATAR_HAMART-001.md Gépi rész, naplok/F123_teljesseg_HAMART-001.tsv (5Móz 21:23 sorai), konkordancia/TAHOT_kivonat.tsv (1Móz 4:2, 9:20, 6:5, 8:21, Ez 12:19, 28:16, Hab 1:2, 2:8, 2:17, Jón 3:8, 5Móz 21:23, Mik 6:12, Sof 1:9, Zsolt 74:20, Jer 51:46), konkordancia/TAGNT_kivonat.tsv (Gal 3:13-14, Zsid 6:7-8, Róm 8:20-21), konkordancia/Karoli_1908.tsv (ugyanezek a versek), git log (HATAR_HAMART-001.md, a három adattábla) | forras=modell:claude-fable-5-1 (split(tab), olvasó lekérdezés) | ts=2026-11-09T19:23Z)
*A határ lezárt (F26): a fenti kérdések (K1–K6) döntései a `jeloltek.tsv`-n át, DT-hivatkozással; a sorállapot a döntés állapota. Új modelles kör csak új, nem a határdöntésből eredő sor-változás után.*

<!-- HATÁRDÖNTÉS: n=47 ujjd=a8fdcc3a1b63 | DT744, DT745, DT746, DT747, DT683, DT685, DT686, DT687 -->

<!-- MODELLES-VEGE -->
