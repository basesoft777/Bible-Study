# 10. PaRDeS U3-prompt sablon — a motívum teljes prózája nulláról, egy kézből

**Állapot: v1.2 (F206, 2026-11-11: „Állítás a versről — írás közben”, a HAMART-001 lektori körének hibaosztályai, gyökérok: `naplok/F206_jelentes.md`). v1.1: F193, 2026-11-11 (a lap új számozása — 9. Hatástörténet, 10. Értelmezés, 11. Módszertan és nyitott kérdések, DT766; J2–J4; hang és alcím, DT768). v1: F178.3, 2026-11-08.** A HAMART-001 mint arany (a felhasználó: „a hamart lesz az új arany / fontos hogy most már visszaesés ne legyen innen”) prózai menetének promptja. Minden új cikknél ez a prompt indítja az U3-at (`MUNKAMENET.md` C-w); 2. kiadásnál, ha a próza újraíródik, szintén. A forma szabályai a `sablonok/9_PaRDeS_motivum_forras_sablon.md` 4. pontjában állnak („Az 1/a igehelyenkénti prózája”, „Az új cikk öt szabálya”, „A HAMART-001 mint arany: a lezárás hét szabálya”); ez a fájl a session bemenete. A próza **mondatszintű** szabályai („Olvasói szöveg”, „Állítás a versről”) itt állnak, egy helyen (F184, DT793); a forma és a szerkezet kérdésében ellentmondásnál a 9-es sablon az irányadó.

*Használat: a `[…]` helyőrzőket a session indítója tölti ki; a prompt többi része szó szerint megy. A session modellje `opus` (értelmező próza, egy kéz: CLAUDE.md, KONTEXTUS K1).*

---

## A prompt

Te a `[ID]` motívum (`[cím]`) teljes prózáját írod meg **nulláról, egy kézből**: a `motivumok/[ID].md` minden kézi szakaszát, egyetlen sessionben. Régi tanulmányból, régi lapból, archívumból mondatot nem viszel át; ha a régi szövegben jó lelet áll, az adatból igazolod, és a saját mondatodban mondod ki.

**Előfeltétel — ellenőrizd, mielőtt egy mondatot írnál:**

1. A határ kész és nem a te döntésed (U2/U3 szétválasztás): a `jeloltek.tsv` motívumsorai döntöttek (`nyitva` 0), a `naplok/HATAR_[ID].md` modelles része friss (`python eszkozok/ellenoriz.py --hatar-ujjlenyomat [ID]` jele egyezik a modelles rész első sorával). Ha nem friss, vagy ebben a sessionben határdöntést hoztál, **állj meg**: a próza a határkör után jön.
2. A modell-ellenőrzés (CLAUDE.md): a saját modellneved a `kiadasok.tsv` / `res_forras.tsv` `proza_modell` mezőjébe kerül, a környezetedből véve.
3. A 9. Hatástörténet adata kész: a visszhang 1 és 2 kinyerő sorai két kézzel ellenőrizve (`MUNKAMENET.md` C-vh), a lap újragenerálva. Ha nem, **állj meg**: a próza a 9. után jön.

**Bemenet** (célzottan olvasd, ne egészben):

- `adat/motivumok.tsv` `[ID]` sora: `negativ_kriterium`, `folerendelt_fogalom`, `azonossag_tipusa`;
- `adat/elofordulasok.tsv` `[ID]` sorai: `igehely`, `karoli_szo`, `gerinc_elem`, `funkcio`, `kapcsolodas`, `jelentes_szam`;
- `adat/jeloltek.tsv` `[ID]` elutasított sorai (az okok, nem egyenként);
- az U1 kivonata: `naplok/F123_alapanyag_[ID].md` (vagy a motívum saját U1-fájlja);
- a lap generált része (`lexikon/[ID]_TUDOMANYOS.md`) csak a számokért (Döntési út, 2. és 3. szakasz) és a 9. Hatástörténet soraiért.

**Amit írsz, sorrendben:**

1. **Kivonat (4 bekezdés).**
   - 1. bekezdés: a lánc vagy a motívum menete a kulcshelyeken, **és a fordulópontja**: hol fordul meg, áll meg vagy vált irányt. A fordulópont adatból igazolt — a beépített sorok `funkcio`-ja, a szó, az igealak —, nem feltevés. Ha két hely között „feszültséget” vagy „ellentmondást” mondanál, nézd meg a két vers szavát: ha más szó vagy más alany áll, a feszültség nem az adaté. *(Tanulság: HAMART-001, 1Móz 8:21 ↔ 9:25.)*
   - 2. bekezdés: a számok a lap adatából (helyek, versek, könyvek, ÓSZ/ÚSZ) és a későbbi helyek csoportjai.
   - 3. bekezdés: a két kötelező határ-elem — a negatív kritérium szó szerint ellenőrizhetően (mely alak tartozik ide, mely nem), az ÚSZ-mérce (a Károli alapszövege, a Textus Receptus), és strukturális/fogalmi hordozónál: a lista keresési módszer eredménye.
   - 4. bekezdés: a fölérendelt fogalom („nem a … általában, hanem …”), a név szerinti tematikus kivételek.
2. **1/a — minden igehely**: a `kapcsolodas` **kerek mondat** (alany, állítmány; idézet csak a fölötte álló Károli-vers szó szerinti része, „…”-ben), alatta a „Funkció:” sor (`címke — magyarázat`, a motívumbeli szerep). Töredék súlyos hiba.
3. **10. Értelmezés** (PaRDeS-keret, vitatott pontok) és **11. Módszertan és nyitott kérdések**: a 9-es sablon 4. pontja szerint, „Az értelmező szakaszok kötelező elemei” mind a négy pontjával — az Értelmezés eleje olvasói magyarázat a négy szintről, az állítások alatt a mért adat forrássora (J3); a Vitatott pontok mindkét olvasatot adatból igazolt érvvel mondják, és kimondják: „a lap a kérdést nem dönti el” (J4); a Módszertanban „A határ második ellenőrzése” bekezdés (J2), próza, nem táblázat. A nyitott kérdés tartalmi, a séma-korlát és az adatállapot `【NAPLO】`. **Alkalmazás-szakasz nincs** (F17, B04, DT756: a felhasználó, 2026-11-10: „nincs is alkalmazás”) — nem írod, és más szakaszba sem viszed át.
4. **Nave-döntések** (U3b, ha még nincs): az `adat/tematikus_temak.tsv`-be, indokkal; üres Nave-blokkal a lap nem adható ki.

**A 9. Hatástörténet: ókori fordítások és értelmezők** generált (a visszhang 1 és 2 kinyerő tábláiból, `MUNKAMENET.md` C-vh), és a próza előtt kész; a próza nem ír helyette, és nem állít
róla többet, mint amit a blokk alapvonala és a tanúsorok mondanak (a 6-os sablon „A 9. Hatástörténet szabályai” és „A 4.11 visszhang-blokk szabályai”): a fordítók „hallották”
a láncot mondat csak ott állhat, ahol a blokk kiemelt következtetése (két héber szó egyesítése, szokatlan választás) ezt
alátámasztja; egyházatyai vagy rabbinikus tanúra csak a 9. sora alapján hivatkozol, szöveget nem idézel belőle.

**Olvasói szöveg — mindenütt:**

- a lelettel kezdesz (számok, a szavak kiejtéssel, példahely), és szabály szerinti következtetéssel zársz;
- harmadik személyben írsz: „mi”-hang, olvasót megszólító mondat és első személyű ellenőrzési állítás („megnéztük”, „vizsgáltuk”) nincs; ha alcímet írsz, névszói alakú (6-os sablon „Alcím és hang”, DT768);
- minden héber, arámi és görög szó mellett a magyaros kiejtés (a lapon egy szónak egy kiejtése van);
- belső szó nem kerül a szövegbe: döntés-azonosító, feladatszám, fájlnév, „gerinc”, „szerep”, „orkesztrátor”, „felhasználó” (a döntés olvasói neve „szerkesztői döntés”); a kutatás belső neve („hígul”, „séma-korlát”, „Strong-keresés”, „mintakeresés”, „láncvers”, „Peshat-mag”, „alapvonal”, „cella”), a készítés menete (modell emelte ki, más kéz ellenőrizte) és a munka állapota („még nem történt meg”) sem: a keresést a tárgyával nevezed meg, a hiányt a szóról mondod (F206). *Rossz:* „A Strong-keresés 577 versében … egy mintakeresés is átnézte” *Jó:* „A szókeresés verseiből 577-ben a lánc négy szava (a bűn, a föld, a romlás és az erőszak) … egy célzott együttállás-keresés is átnézte”;
- a beépítés indoka szerkezeti jegy (lánc, visszautalás, szókapcsolat), nem a szó puszta egyezése;
- „független” csak akkor, ha a két forrásnak nincs közös bemenete: a motívum keresései közös szavakból (Strong-listából) indulnak, ezért egybeesésük „egybeesés, nem független megerősítés” (F24 (a); a kapu: `olvasoi_kapu.MUNKASZAVAK`);
- a zárómondat (Sod és minden szakasz vége) a motívum saját leletéből áll; más lap zárómondata, a lapok közötti sablonmondat („A motívum legmélyebb rétege ezért … az a remény”) tilos (F24 (b));
- munkaszó és munkajelölő nem kerül a szövegbe („próba”, „javaslat”, „ellenőrzendő”, „függőben”, „audit”, „token” — a teljes lista: `olvasoi_kapu.MUNKASZAVAK`);
- hiányt nem töltesz ki asszociatív anyaggal: ha nincs adat, kimondod (CLAUDE.md 3. szabály).

**Állítás a versről — írás közben** (F206; ugyanezeket a hibaosztályokat találta a HAMART-001 lektora és az újraírt prózán a második kéz: `naplok/F206_jelentes.md`). Minden versre hivatkozó mondatnál, megíráskor:

1. **A vers azt mondja, amit a mondat neki tulajdonít:** a vers alanya, tárgya, megszólítottja; két tagmondatát nem vonod össze; nem teszel hozzá szót (ítélet, vér, vádló); a név a Károli alakjában; minden versállítás mellett az igehely.
   *Rossz* (Jer 6:7): „A város úgy őrzi gonoszságát, mint a kút a vizét, és az erőszak hangja Isten előtt szüntelen; az ítélet ennek a hangnak felel.” *Jó:* „A vers két dolgot mond külön: a városban erőszak és önkény hallatszik, Isten előtt pedig szüntelen »betegség és vereség« van.”
2. **A magyar szó mögött a vers saját héber/görög szava áll** (TAHOT/TAGNT); ahol nem a lánc szava (erec az adámá helyett, más görög ige, azonosság csak a Septuagintán át), kimondod. „Más szóval” csak ellenőrzés után.
   *Rossz:* „…és végül az ítélet tárgya (1Móz 6:13).” *Jó:* „…és végül az ítélet tárgya (1Móz 6:13); az utolsó lépésnél a héber szó változik, az 1Móz 6:11-13 »földje« az erec, nem a lánc szava, így a hordozó jelentésében folytatódik, szavában nem.”
3. **Kizárólagos szó csak lekérdezéssel** („először”, „egyetlen”, „mindig”, „minden”, teljesnek ható felsorolás), proveniencia-sorral; különben az összevetést mondod ki.
   *Rossz:* „Ábrám elhívásában pedig az átok szava először áll az áldás keretében (1Móz 12:3).” *Jó:* „Ábrám elhívásában pedig az átok igéje Isten áldás-ígéretének egy mondatában áll (1Móz 12:3); Noé szavában az átok és az áldás még két külön kimondás (1Móz 9:25-26).”
4. **A hatókör a csoport minden tagjára igaz;** a kivételt (tematikus hely) megnevezed; a szám mellett a számlálás köre (mely szavak, melyik keresés); egy versből következetesség nem mondható.
   *Rossz:* „A motívum hat újszövetségi helyén a motívum szava a Textus Receptusban és a kritikai kiadásokban ugyanott áll.” *Jó:* „A motívum öt lexikai újszövetségi helyén a lánc szava … ugyanott áll. A hatodik, a Jel 22:3, tematikus hely, a lánc szava nélkül; …”
5. **A kapcsolat legfeljebb az adat erejével:** „visszautal”, „visszatér” csak a hely `kapcsolatok.tsv`-sorával; közepes vagy hiányzó sornál a közös szót mondod, függést nem (a beépítés szerkezeti jegye, pl. a szókapcsolat, így is kimondható: az a hely jegye, nem a másik helytől való függés); szakaszra csak az ott ténylegesen álló tárgyalásra utalsz.
   *Rossz* (Jer 6:7, Hab 1:2, közepes sor): „Az erőszak szava az 1Móz 6:11 és 6:13 szava, és a szópár maga utal vissza a láncra.” *Jó* (Jer 6:7): „A lánccal az erőszak szava (chámász) köti össze, az 1Móz 6:11 és 6:13 szava; a »hallatszik« ige a Genezis láncában nem áll, a szókapcsolat a próféták saját fordulata.”
6. **Az olvasat a lap olvasataként áll:** a Peshat csak a vers szavát mondja; következtetés és általános tétel a lap olvasata (Drash), nem a szöveg állítása; szerzőnek csak a forrássora szerinti állítást tulajdonítasz.
   *Rossz:* „…de azt igen, hogy a bűnnek mindig vannak az elkövetőn túli hatásai.” *Jó:* „…a lap helyei azt mutatják, hogy a bűn következményei kiterjednek az elkövetőn túl.”
7. **Az első említés önmagában érthető, a címke a tartalmát mondja;** felosztás, keresés bevezetés nélkül nem áll; felvett és kizárt hely nem keveredik.
   *Rossz:* „a föld a lánc egyetlen szava, amely mind a négy genezisi szakaszban áll (az 1Móz 3., 4., 6:1-8 és 6:9-22).” *Jó:* „a föld a lánc legtöbbször visszatérő szava: a lap genezisi helyei közül 12 versben áll, az 1Móz 3:17-től a 8:21-ig, és Ábrám elhívásában is (1Móz 12:3).”

**Önellenőrzés a commit előtt** (mind fusson le, a kimenet a menetnaplóba):

```
python eszkozok/general.py --cel lexikon --id [ID] --ir
python eszkozok/proza_1a.py [ID] --reszletes
python eszkozok/olvasoi_kapu.py [ID] --reszletes
python eszkozok/ellenoriz.py
```

A mérce: 25. szabály RENDBEN (minden 1/a kerek + „Funkció:”), olvasói kapu 0 BUKÁS, 37–39. szabály a motívumra tiszta, a lap regressziós kapui (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`, „A HAMART-001 regressziós kapui”) zöldek. Ha egy kapu bukik, a forrást javítod (a lapot soha), és újragenerálsz.

**Állítás-ellenőrzés — a próza után, a lektor előtt** (`MUNKAMENET.md` C-a; F200):

```
python eszkozok/proza_allitas.py [ID]
```

A `naplok/ALLITAS_[ID].md` a próza versre hivatkozó állításait (a rések mondatai és a `kapcsolodas` sorai) veti össze a verssel és az adattal.

- **ELTÉR-sor:** a gépi ítélet a vers héber/görög Strong-során, a Károli-szövegen vagy az adaton áll (a szó áll vagy nem áll a versben; a szópár mellett más szó áll; a fordulat két szava nem szomszédos; az idézet nem a Károli szövege; a szám nem egyezik). Minden ELTÉR-sort a forrásban javítasz, és újrafuttatod; a javított mondat a vers saját szövegét mondja (ki/mi az alany, melyik héber szó áll), nem a régit tompítja.
- **⚑ tétel a kézi listán.** Mindet magad nézed át, és a fenti „Állítás a versről” szerint javítod. A jelzés fajtái:
  - a magyar szó más héber szót fordít, vagy a lánc szava nincs a versben (2.);
  - kizárólagos állítás lekérdezés nélkül (3.);
  - hatókör: a csoportban tematikus hely is van (4.);
  - kapcsolat-állítás közepes vagy hiányzó kapcsolat-sorral (5.).
- **A többi kézi tétel** (az állítás, a Károli-vers és a héber/görög sor egymás mellett) az olcsó modell (Sonnet) vagy ember átnézésére megy, a lektor előtt; a kérdés tételenként: azt mondja-e a vers, amit az állítás neki tulajdonít (alany, tárgy, szó, kapcsolat).

A lépés kapu-szintje JELENTÉS: nem bukik, de a lektor csak az ELTÉR-sorok javítása után indul.

**Kimenet:** a `motivumok/[ID].md` (forrásréteg) és a menetnapló; tételenkénti commit, UTF-8 fájlból. A lap a generátor kimenete, kézzel nem szerkeszted.
