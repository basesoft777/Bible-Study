# HATAR_HAMART-001.md — motívum-határ ellenőrzés (F151, #151)

*A „Gépi rész” generált (`python eszkozok/motivum_hatar.py --motivum HAMART-001`, determinisztikus; újrafuttatáskor felülíródik); a „Modelles rész” jelölői közötti tartalom megmarad. Minden pont **kérdés** a felhasználóhoz, nem javítás; adatot, motívumfájlt, lapot ez a fájl nem módosít.*

*(proveniencia: scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv (azonossag_tipusa, negativ_kriterium) + motivum_kapcsolatok.tsv | forras=motivum_hatar.py (jelolt_eloszures.vizsgal; szerep_karoli.vers_strongok: TAHOT+TAGNT; lexikon_general.igehely_lista) | motivum=HAMART-001 | ts=2026-11-08T15:08Z | bemenet=adat/elofordulasok.tsv@dfb0de82a1,adat/motivumok.tsv@e1d84722b1,adat/motivum_kapcsolatok.tsv@a5c617b93b,adat/grammatikai_strongok.tsv@1cc1be084e,konkordancia/TAHOT_kivonat.tsv@a337d3c858,konkordancia/TAGNT_kivonat.tsv@d3ae4ed4a2,konkordancia/Karoli_1908.tsv@cba0ca127a)*

**Motívum:** HAMART-001 — A bűn következményeinek gyűrűzése — átok, föld és romlás · hordozó: `strukturális` · fölérendelt fogalom: a bűn és következményei általában, a genezisi lánc szavai és szerkezete nélkül · beépített sor: 48 (56 vers)

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


*Második vélemény a mai adaton (60 beépített sor, 86 vers; a 2026-11-02/03-i, 52 soros állapotra írt K1 és a felhasználói besorolása ezzel felülírva; az akkori döntés nyoma a fájl git-történetében: f4061848). Bemenet: csak a motívum azonosítója; a készítő session összefoglalóját nem vettem figyelembe. A gépi rész két eredményét (részhalmaz: 0 kérdés; negatív kritérium: strukturális hordozón nem fut) nem ismétlem. Minden pont kérdés a felhasználóhoz, nem javítás; új igehelyet nem javaslok, nem döntök.*

**10 kérdés.** (1. kérdés = következetlen határ; 2. kérdés = hígulás a fölérendelt fogalom felé.)

**K1 — A Jer 51:25 beépítve áll a romlás-ige fizikai jelentésénél, miközben a Jer 51:20 ugyanezt az igét ugyanarra a Babilonra „fizikai pusztítás” indokkal zárja ki.**
- `adat/elofordulasok.tsv:243` — Jer 51:25, `gerinc_elem`=H7843, `jelentes_szam`=„Hif'íl 1”; `adat/jeloltek.tsv:810`: „a hely nem a katonai pusztítás általános esete (az elutasítva), hanem egy birodalom vádja, amely az egész földet rontotta meg”.
- `adat/jeloltek.tsv:480` — Jer 51:20, elutasítva: „Fizikai pusztítás (épületek, országok, szőlő), nem erkölcsi megromlás”; `adat/jeloltek.tsv:735` (összesítő sor, 112 vers): „katonai vagy fizikai pusztítás, egy nép vagy ház bűne, az egyetemes romlás szerkezete nélkül. A Jer 51:25 nem tagja a csoportnak: saját sorban, beépítve áll.”
- Miért kérdés (1.): az 1Móz 6:12 és a Zsolt 14:1/53:2 a sor saját adata szerint „Hif'íl 2” (erkölcsi), a Jer 51:25 „Hif'íl 1” (fizikai), vagyis a beépített sor a BDB-jelentés szerint az elutasított csoport oldalán áll; a különbség csak az „egész föld” tárgy, amelyet a kizárási indok nem nevez határnak.

**K2 — A Mal 3:11 a föld termésének megóvását a tized szövetségi rendjében mondja ki, amit a negatív kritérium és az 1Kir 8:34-35 kizárása a motívumon kívülre tesz.**
- `adat/elofordulasok.tsv:247` — Mal 3:11, `gerinc_elem`=H7843, `jelentes_szam`=„Hif'íl 1”, `funkcio`: „megfordítás — a föld termését többé nem rontja meg a kártevő”; `adat/jeloltek.tsv:668`: „a 3:9 átka (arar) után az Úr megígéri, hogy a kártevő »nem veszti el földetek gyümölcsét«”.
- `adat/jeloltek.tsv:657` — 1Kir 8:34-35, elutasítva: „a vétek miatt a nép fogságba kerül a földről, vagy elmarad az eső, és a megtérés után visszakapja. Ez a szövetségi átok rendje, mint a korábban elutasított 5Móz 28:23-24 és 3Móz 26:20 helyeken; a szöveg a Genezisre nem utal vissza.” — és `adat/jeloltek.tsv:471` — Mal 3:9, elutasítva: „Az arar itt rituális, jogi vagy indulati átok-kimondás … prófétai feddés”.
- Miért kérdés (1. és 2.): a beépítés indoka a Mal 3:9 átkára épül, amelyet ugyanez a tábla kizár; a Mal 3:11 termés-ígérete a „bűn és következményei” fölérendelt fogalom szövetségi alakja (`adat/motivumok.tsv:10`: „az sem, amely a föld elvesztését csak a szövetségi rendben mondja ki”), a Genezisre való visszautalást az indoklás nem nevezi meg.

**K3 — A Hab 2:8, a Hab 2:17 és a Jón 3:8 a chámász szón egyedül, kollokáció nélkül áll bent, miközben 39 más chámász-vers pontosan a kollokáció hiánya miatt van kizárva.**
- `adat/elofordulasok.tsv:238`, `:239`, `:240` — Hab 2:8, Hab 2:17, Jón 3:8, `gerinc_elem`=H2555 (nem málé+chámász, nem sámá+chámász); `adat/jeloltek.tsv:258`: „az erőszak visszatér elkövetőjére: a gyűrűzés mint megtorlási elv, explicit kimondva”; `:260`: „az egyetlen hely, ahol egy nép a chámász-ból megtérve elkerüli a már kimondott pusztulást”.
- `adat/jeloltek.tsv:417` — Zsolt 11:5, elutasítva: „chámász általános használatban, kollokáció nélkül”; `adat/jeloltek.tsv:734` (összesítő sor, 36 vers): „a חָמָס (chámász, erőszak) szava áll bennük, általános használatban: a »megtelt erőszakkal« és a »hallatszik az erőszak« szókapcsolata nélkül, a láncra való visszautalás nélkül.”
- Miért kérdés (1. és 2.): a TAHOT szerint a Hab 2:8 és 2:17 versében H2555 és H0776 áll, a „megtelt”/„hallatszik” ige nem (a Jón 3:8-ban csak H2555); a beépítés indoka („megtorlási elv”, „megtérés”) a fölérendelt fogalom (a bűn következményei általában), nem a lánc szópárja.

**K4 — A Jer 17:5 egyéni „Átkozott az, a ki…” formulája bent áll, a Jer 11:3 és a Zsolt 119:21 ugyanilyen formulája „prófétai feddés” indokkal kint.**
- `adat/elofordulasok.tsv:227` — Jer 17:5, `funkcio`: „formula egyénre — az átok a bizalom rossz irányára szól”; `adat/jeloltek.tsv:249`: „a próféta az átok-formulát egyéni bizalmi döntésre alkalmazza”.
- `adat/jeloltek.tsv:462` — Jer 11:3 („Átkozott mindenki, a ki meg nem hallja e szövetségnek igéit”, `konkordancia/Karoli_1908.tsv`), elutasítva: „Az arar itt rituális, jogi vagy indulati átok-kimondás (… eskü, önátok, prófétai feddés) — nincs meg a következmény-terjedés szerkezete … A arar önmagában nem a motívum, csak annak egyik eszköze; a motívum a arar + adamá együttállásán és a fokozási soron áll”; ugyanez az indok a `:472` Zsolt 119:21 soron.
- Miért kérdés (1. és 2.): a Jer 17:5-ben sem adamá, sem fokozási sor nincs, az indoklás a láncra való visszautalást nem nevezi meg; a Jer 11:3 ráadásul az 5Móz 27:26 formulája, amelyet a Gal 3:10 beépített sora idéz (`adat/jeloltek.tsv:268`).

**K5 — Az 1Móz 12:3 „a ki téged átkoz, megátkozom azt” formulája bent áll, a szó szerinti ismétlései (1Móz 27:29, 4Móz 24:9) kint.**
- `adat/jeloltek.tsv:246` — 1Móz 12:3, beépítve: „a lánc megfordítása: ugyanaz az ige (arar) és ugyanaz a főnév (adamá), de most az áldás keretében”.
- `adat/jeloltek.tsv:444` — 1Móz 27:29 („Átkozott, a ki téged átkoz, és a ki téged áld, legyen áldott”), elutasítva: „áldás-átok formula pátriárkai áldásban … nincs meg a következmény-terjedés szerkezete”; ugyanez a `:454` 4Móz 24:9 soron („ki átkoz téged, átkozott lészen”).
- Miért kérdés (1.): ha a 12:3-at a megfordítás (átok az áldás keretében) teszi láncelemmé, ugyanez a megfordítás a 27:29-ben és a 24:9-ben is áll; ha az adamá, akkor az indoklás „megfordítás” fele nem a határ.

**K6 — Az 1Móz 9:25 Noé pátriárkai átka egy leszármazottra bent áll, az 1Móz 49:7 Jákób pátriárkai átka a leszármazottakra „pátriárkai áldásban” indokkal kint.**
- `adat/jeloltek.tsv:245` — 1Móz 9:25, beépítve: „az átok-lánc az özönvíz után azonnal újraindul, immár egy leszármazottra”.
- `adat/jeloltek.tsv:445` — 1Móz 49:7 („Átkozott haragjok, mert erőszakos … eloszlatom őket Jákóbban”), elutasítva: „Az arar itt rituális, jogi vagy indulati átok-kimondás (áldás-átok formula pátriárkai áldásban …)”.
- Miért kérdés (1.): a két hely ugyanaz a beszédhelyzet (apa átka fiára vagy unokájára, adamá nélkül); a határ itt csak a fejezetszám (1Móz 3–9), amelyet az indoklás nem mond ki.

**K7 — Az 5Móz 27:15-26 és 28:16-19 szövetségi átkai bent állnak, miközben a negatív kritérium a szövetségi rendet kizárja, és az 5Móz 28:20-24 kizárása csak az arar hiányát nevezi meg.**
- `adat/elofordulasok.tsv:226` — 5Móz 28:16-19, `funkcio`: „törvényi formula — négy átok az áldások tükörképeként; a föld termése is alá esik”; `adat/jeloltek.tsv:248`: „Négy אָרוּר (árúr) a szövetségszegés következményeiként, a 28:3-6 négy בָּרוּךְ (bárúkh) tükörképeként”.
- `adat/motivumok.tsv:10` — negatív kritérium: „és az sem, amely a föld elvesztését csak a szövetségi rendben mondja ki”; `adat/jeloltek.tsv:405` — 5Móz 28:23, elutasítva: „Szövetségi átok-szakaszok, amelyek nem az arar igét használják”.
- Miért kérdés (2.): a beépített sorok indoklása a láncra való visszautalást (átok a földön, föld romlása) nem nevezi meg, csak a szót és a formula-jelleget; a szomszédos versek határa így az arar lexéma, nem a kritérium második feltétele (visszautalás), ami a fölérendelt fogalom (szövetségi átok általában) felé nyit.

**K8 — A Mt 15:19 és a Mk 7:21-23 tematikus sorként a szív gonosz gondolataira utal vissza, miközben a Jer 17:9 és a Préd 7:29 ugyanezt a szív-diagnózist más motívumhoz sorolva vagy „antropológiai általánosításként” zárja ki.**
- `adat/elofordulasok.tsv:257` — Mt 15:19, `gerinc_elem`=„tematikus:1Móz 6:5”; `adat/jeloltek.tsv:273`: „»a szívből származnak a gonosz gondolatok« — a 1Móz 6:5 szív-diagnózisának újszövetségi megismétlése ⇒ tematikus, nem lexikai”.
- `adat/jeloltek.tsv:347` — Jer 17:9 („Csalárdabb a szív mindennél, és gonosz az”), elutasítva: „a szív romlottsága a »jetzer — a szív romlott hajlama« motívum tárgya … Kereszt-motívum szennyeződés elkerülése (Q4)”; `:349` — Préd 7:29: „Antropológiai általánosítás az emberi szívről; nem a következmény-terjedésről”.
- Miért kérdés (1. és 2.): a Mt/Mk sor célpontja (1Móz 6:5) maga is tematikus sor (`adat/elofordulasok.tsv:212`; a H7451 a 2026-11-03-i döntés óta nem gerinc-elem), így a két evangéliumi hely a lánc egyetlen szavát és szerkezetét sem hordozza, csak a „bűn általában” fölérendelt fogalmat; a Jer 17:9 kizárási indoka (a szív romlott hajlama önálló motívum) szó szerint rájuk is illik.

**K9 — A 2Pét 3:6-7 az özönvíz ítéletét tematikus sorként bent tartja, a 2Pét 2:5 ugyanezt az özönvíz-ítéletet „Noé alakja” indokkal kint.**
- `adat/jeloltek.tsv:275` — 2Pét 3:6-7, beépítve: „az özönvíz-világ elpusztulása és a jelenlegi világ tűzre tartatása — a 1Móz 6:13 ítélet-logikájának eszkatológiai kiterjesztése ⇒ tematikus, nem lexikai”.
- `adat/jeloltek.tsv:435` — 2Pét 2:5 („özönvízzel borítván el az istentelenek világát”), elutasítva: „Noé alakja és az özönvíz-narratíva újszövetségi felidézése; a motívum (az átok/romlás terjedése) nem tárgyuk”.
- Miért kérdés (1.): mindkét hely az özönvizet az istentelenek ítéletének mintájaként idézi, lánc-szó nélkül; az egyiknél ez „ítélet-logika”, a másiknál „Noé alakja”.

**K10 — Formai: a bent lévő sor „folytatása” hol külön elutasított sor, hol a beépített tartomány része.**
- `adat/jeloltek.tsv:665` — Ez 28:17, elutasítva: „A hely az Ez 28:16 sorának folytatása … új láncelem nélkül”; ugyanez a `:667` Mik 6:13 és a `:515` 2Pét 3:10 soron.
- `adat/elofordulasok.tsv:250` — Róm 8:20-22 egy sorban; `motivumok/HAMART-001.md:31`: „A Róm 8:20-22 három verse egy érvelés, amelyben a romlás szava a középső versben (8:21) áll.”
- Miért kérdés (1.): a Róm 8:20 és 8:22 ugyanúgy „folytatás, új láncelem nélkül”, mint az Ez 28:17, de az egyik a beépített vers-számba (86) kerül, a másik elutasított sor; a lapon a határ ettől másnak látszik, mint ami.

*Nem kérdés (összevetve, a határ következetes): a sáchat „szövetséges nép” kizárása (5Móz 4:25, Bír 2:19, Sof 3:7, Hós 9:9, 5Móz 9:26-27) a Zsolt 14:1/53:2 „egyetemes” beépítésével szemben; a „föld színéről” fordulat (1Móz 7:4, 7:23, Sof 1:2-3 bent; 1Kir 13:34, 14:15-16, 2Kir 17:22-23 kint) az egyetemes felsorolás határán; a Hós 10:8 szópárja; a málé+chámász és sámá+chámász sorok; a romlandó test (ApCsel, 1Kor 15) kizárása a Róm 8:20-22-vel szemben.*

(proveniencia: scope=adat/motivumok.tsv:10 (azonossag_tipusa, negativ_kriterium, folerendelt_fogalom), motivumok/HAMART-001.md (1., 2., 7. szakasz), adat/jeloltek.tsv (HAMART-001: 331 sor, 60 beépítve, 271 elutasítva), adat/elutasitasi_okok.tsv (HAMART-001 minták), adat/elofordulasok.tsv (HAMART-001: 60 sor, gerinc_elem, jelentes_szam), naplok/HATAR_HAMART-001.md Gépi rész, konkordancia/Karoli_1908.tsv és konkordancia/TAHOT_kivonat.tsv (a K1–K6 versei, grep) | forras=modell:claude-fable-5-1 (split('\t'), olvasó lekérdezés) | ts=2026-11-08T09:00Z)
<!-- MODELLES-VEGE -->
