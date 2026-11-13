# F218a — folytatási fájl

*Kézi munkanapló (a brief 9. pontja szerint minden commitban frissül). Ebből indul a következő session; a régi generátorból visszafejtett mondatszabályok is itt állnak.*

Ág: `claude/f218-generator-uj-a` · PR: #729 (vázlat) · Brief: `F218_GENERATOR_UJ_A_BRIEF.md` · Alap: main `37f087cc`.

## Állás

| Tétel | Állapot | Megjegyzés |
|---|---|---|
| F218.0 | kész | modell-ellenőrzés, függések, keretmérés |
| F218.1 | kész, két halasztott résszel | referencia (bájtra azonos, 46,5 s), szimbólumtérkép, bemenet-hashek, alapmérés: `naplok/F218_jelentes.md`. **Halasztva:** a leltár `kovetelmeny` oszlopa (brief 7.4; a heti keret nullázása után, sonnet); az alias-sorok (GK-17) az S5 előttre |
| F218.2 (T) | kész | típusok és szerződések; GK-01, 02, 05, 08a–c, 12, 23, 29, 30 zöld |
| F218.4 (S1) | **kész: a szakasz-diff 0 az engedélyeken kívül** | „2. Előfordulások” + „2.1”: 437 sorból 432 bájtra egyezik, 5 engedélysor; festékpróba 0 szivárgás. Az S1 tesztjei (`teszt_elofordulas.py`): GK-13, GK-14, GK-17, GK-25, HN-01, HN-16, a sablonmódosítók, a jegyzet-összevonás |
| F218.3 | kész | tesztváz (`teszt_vaz.py`): 35 követelmény név + docstring + `skip` alakban, a szelet megnevezésével; a HN-03 a felhasználó döntésére vár; a mutációs próba (GK-26) az S9-ben. A tesztek állása: 121 teszt, 86 zöld, 35 kihagyva |
| ⛔ az S1 után | **ELTÉRÉS (11 tétel)**; megállt | 1. független ellenőrzés (`fuggetlen-ellenor`, opus) és a felhasználó első átnézése: a lista a `naplok/F218_jelentes.md` „Amit a felhasználónak látnia kell az S1 után” pontja |
| Javítókör (1. kör) | **kész** (2026-11-13, a 2. session) | az 1. ellenőrzés 11 tételéből 9 javítva, a 6. (halasztások) változatlan, az önreferencia három párja nyitva (DT-F218l); részletek: `naplok/F218_jelentes.md` „Javítókör az 1. ellenőrzés után”. Az S1 engedélysorai 5-ről 1-re csökkentek (S1-FORRAS). Az újraellenőrzés az S2 végi célzott ellenőrzéssel együtt fut |
| 2. ellenőrzés (célzott, a javítókörre) | **ELTÉRÉS: 4 tétel** | `naplok/F218_jelentes.md` „Független ellenőrzés — 2. ellenőrzés”; a besorolást az orkesztrátor hozta (1a, 2, 3, 4 mechanikus; 1b döntés: DT-F218m) |
| Javítókör (2. kör) | **kész** (2026-11-13, a 3. session) | mind a 4 tétel javítva: `naplok/F218_jelentes.md` „A 2. ellenőrzés javítóköre”. Új: B68 (a jegyzék saját sora), 2 sablonmondat (`e2.jel.szocikkel`, `e2.jel.szocikk_sorszam`; `dontes=var`), DT-F218m. Az újraellenőrzés az S2 végi célzott ellenőrzéssel együtt fut |
| DT-F218l (önreferencia) | **kész, ✅** (2026-11-13, a 3. session) | a három nyitott pár 8 cellája a forrásban javult, a jóváhagyott lap szavával („a vizsgálat”, „ez a vizsgálat”, „a listán”; nem egységesen „szócikk”: l. a jelentés „DT-F218l: az önreferencia a forrásban” szakaszát). A nyílt mag követi (kódkönyv-kulcs, a fordítástár hash-e, újraexport); az angol szöveg nem változott. Az S2-ONREF-1 és -2 engedélysor megszűnt. A fájlok az `ir`-en kívül esnek (a bővítés függési kört adna: a felhasználó döntése) |
| F218.5 (S2), első fele | **kész** | a vizsgálat közös modellje kapukkal és a kizárt versek melléklete: 431 sorból 421 egyezik, 10 engedélysor, engedély nélküli diff-sor 0; festékpróba 0; 144 teszt |
| F218.5 (S2), második fele | **kész: a szakasz-diff 0 az engedélyeken kívül** | „1. Döntési út” (1.1–1.5): 110 sorból 94 egyezik, 16 engedélysor két előre megszámolt osztályban (1 blokkfejléc, 15 funkció-magyarázat kezdőbetűje); festékpróba 0; 167 teszt (134 zöld, 33 váz). Az ISTENTISZT-lap szakasza generálódik, a kapuk zöldek |
| 3. ellenőrzés (célzott, az S2-re és a 2. javítókörre) | **ELTÉRÉS: 2 tétel** | `fuggetlen-ellenor` (`claude-opus-5-5`); a többi pont rendben, a számok egyeznek. A két tétel: (1) a típusjelölő előtagú hordozó elem (`referencia:`, `idézet:`, `formula:`; a MENNY-001-en él) kézi névként, „szópár” címmel kerülne a lapra, kapu nélkül; (2) a festékpróba nem látja a horgonyba kerülő, kisbetűsített jelzőszót. A jelentés és a besorolási javaslat (mindkettő mechanikus) a `naplok/F218_jelentes.md` végén; egyeztetésre vár, javítás még nem történt |
| F218.6 (S3) – F218.13 | nem indult | a következő: „4. Szótári háttér”, `high` |

## Az 1. független ellenőrzés után: ELTÉRÉS, 11 tétel

A jelentés változtatás nélkül: `naplok/F218_jelentes.md` „Független ellenőrzés — 1. ellenőrzés”. **A javítókör lezajlott** (2. session, 2026-11-13): az eredmény tételenként a jelentés „Javítókör az 1. ellenőrzés után” szakaszában áll. Az alábbi tábla az építő session eredeti javaslata (történeti); a döntéseket az orkesztrátor hozta a felhasználótól: T3 megerősítve („Külön tábla jó”), T4 módosítva (DT-F218j), a `cella` módosító megszűnt (DT-F218k), az önreferencia a forrásban javul (DT-F218l), a 7 új sablonmondat jóváhagyva („Igen, mind jó”).

| # | Eltérés | Javasolt besorolás | Teendő |
|---|---|---|---|
| 1 | T3 (DT837) tárolása külön táblában, felhasználói megerősítés nélkül | döntés (a felhasználóé) | az orkesztrátor viszi a felhasználóhoz: külön tábla (DT-F218i) vagy az `elofordulasok.tsv` oszlopa; a megerősítésig a DT-F218i állapota nem ✅ |
| 2 | Az idézetbe mosás csatornája: a `gerinc.jel_szoveg` és az `idezet_szoveg` a számításból kapott szöveget burkolja; a B16–B22 nyers sorai festetlenül jutnak a számításba | mechanikus | a szakaszjel két alakja (cella, próza) és a példahely mezői a `bemenet/gerinc.py`-ban, betöltéskor kapjanak burkolót (a jel a kulcsból a bemeneti rétegen belül képződjön); a számítás típusos példahely-objektumot kapjon, nyers szótársort ne; a két általános burkoló metódus megszűnik; a festékpróba ezután a szótári ágat is fedi |
| 3 | A `cella` módosító prózát és idézetet ír át, szemben a 6-os sablon új szabályával („változatlanul”) | döntés + tervezés | két út: (a) a szabály szövege kimondott kivételt kap a cellakezdő alakra (tipográfiai átalakítás a sablon-konstruktorban, teszttel), a felhasználó jóváhagyásával; (b) a címkék cellakezdő alakja adatba kerül (a címketábla javítása), és a módosító csak sablonszövegre hat. Ugyanide tartozik az önreferencia („a lap”) kezelése: a kettő legyen következetes |
| 4 | A bemenet-hash őr nem veti össze az olvasási naplót a referencia-táblával; a B67 és a `dontesek/uj/*.md` nincs a táblában | mechanikus | a `regresszio.py` kapja meg az új generátor olvasási naplóját (a `fo.lap_keszit` eredményéből vagy a kimenet mellé írt naplófájlból), és bukjon, ha olvasott bemenet nincs a `F218_referencia.tsv`-ben; a tábla bővítése az új generátor bemeneteivel (külön commit, okkal) |
| 5 | Az S1-ONREF osztály előzetes darabszám nélkül, látható visszalépéssel; a T4 osztály 3 a rögzített 2 helyett | döntés (a felhasználóé) | a jelentés „Amit a felhasználónak látnia kell az S1 után” 1. és 2. pontja; a döntés után az engedélysorok igazítása |
| 6 | Az S1 hatóköréből halasztott tételek: HN-03, GK-13 (lemma), GK-14 (összevont versek), GK-03 (B18/B19/B21), 7.4, alias-sorok | részben döntés, részben mechanikus | a halasztást az orkesztrátor hagyja jóvá, vagy a javítókör pótolja; a GK-03 frissességi kapu a B18/B19/B21-re pótolható az S1-ben is |
| 7 | Tesztváz: hiányzik a GK-B9, a HN-szövegminták és a leltárleírások | mechanikus | GK-B9 a vázba (a tartalmát a `test_gk29_…` már méri); a HN-esetekhez lapszöveg-részlet mint tesztadat; a cím nélküli tételek leírása a 7.4 után |
| 8 | `general.py:1925`: az előjavító (E32) egy régi üzenetből törölte a „; DT-F09h” részt; a jelentés „additív”-nak mondja | mechanikus | a jelentés mondatának pontosítása (additív módosítás és egy E32-előjavítás); a régi generátor kimenete ettől bájtra azonos maradt |
| 9 | GK-07: `-` elem a blokkfejléc forráslistájában (a B13 szabálymodul útvonala) | mechanikus | a `fo._forrasok` a nem fájl-bemenetet hagyja ki (vagy a modul nevét írja); utána az S1-FORRAS engedélysor hash-e frissül |
| 10 | A 10 sornál nagyobb új táblákhoz nincs bontási napló | mechanikus | a három tábla sorainak bontása a jelentésbe (sablon: `eredet` szerint; névtábla: típus szerint; jegyzék: szeletenként) |
| 11 | A T4-táblázat „melyik felel meg a Károli-szónak” oszlopa jelöletlen értelmezés | mechanikus | értelmezésként jelölni, vagy a Károli–Strong párosítás lekérdezésével alátámasztani, proveniencia-sorral |

**A lassú tesztek.** Az ellenőr `teszt_futtat.py --diff` futása a `teszt_visszhang_kapu.py`-ban 2 bukást adott (a régi generátor 4.11 blokkja). A fő checkout (`1352ac3c`, a main egy korábbi állapota) ugyanezzel a 2 bukással áll (`python eszkozok/teszt_futtat.py --fajl teszt_visszhang_kapu`: 22 teszt, 2 bukás), tehát a hiba nem ebből a diffből jön. A `teszt_szintek.py` hibáját nem vizsgáltam.
*Proveniencia: `scope=python eszkozok/teszt_futtat.py --fajl teszt_visszhang_kapu | forras=1352ac3c (a fő checkout) | ts=2026-11-13`.*

## Következő lépés

**Az S2 (F218.5) kész.** A 3. session a 2. ellenőrzés javítókörét, a DT-F218l forrásjavítását és az S2 második felét végezte el; a kontextusa a végén kb. 60%. **Az xhigh eddig tartott:** az S3-tól a brief szerint `high`.

1. **A 3. ellenőrzés javítóköre (2 tétel).** A besorolási javaslat a `naplok/F218_jelentes.md` végén áll (mindkettő mechanikus); az orkesztrátor egyeztetése után javítandó, az S3 előtt. (1) A hordozó elem fajtája zárt készlet a bemeneti rétegben (`bemenet/elofordulas.py` `gerinc_reszek`): ismeretlen előtag (`referencia:`, `idézet:`, `formula:`) `BemenetHiba`; teszt a MENNY-001 soraira. (2) A festékpróba (`festek.py`) kis- és nagybetűtől függetlenül keressen; a horgony saját tartományfajta, ahol a kézi és az idézett szöveg jelzőszava megengedett, a belsőé nem; a kivétel egy mondata a 6-os sablon alapszabály-szakaszába. Ez a 218a harmadik ellenőrzése volt (a brief kettőt írt elő: az S1 után és az S9-ben; a 2. és a 3. a javítókörök és az S2 célzott ellenőrzése); az újraellenőrzése az S3 végi ellenőrzéssel együtt futhat.
2. **F218.6 (S3): „4. Szótári háttér”** (Áttekintés, 4.1–4.10 BDB/Thayer-kártya, 4.12 Nave, 4.13/4.14), új Fable-sessionben, `high`. Előtte modell-ellenőrzés és `get_usage` (a küszöb 99% heti; 70% kontextus fölött zárás). A szelet nagy: két-három commitra bontva (4.1–4.5 · 4.6–4.10 · 4.11–4.14). Első lépés: a referencia-szakasz (991–2350. sor) szerkezetének kiírása rövidítve, és a régi kód szimbólumonkénti olvasása (a jelentés szimbólumtérképe, 2/b).

### Az S3 előtt eldöntendő (a felhasználóhoz, az orkesztrátoron át)

1. **Az egyenként elutasított versek „saját indoka” (a 3. szakaszhoz, S3 után is ráér, de a „3. Kizárt és vizsgált helyek” előtt kell).** A régi kód a `jeloltek.tsv` `indoklas` mezőjét (belső szabad szöveg) regexekkel tisztítva írta ki. Az új generátor belső szövegből cserével olvasói szöveget nem készít: az indoklás kézi prózának minősül-e (akkor változatlanul áll, és a forrásban javul), vagy külön olvasói mező kell.
2. **Alias-sorok (GK-17, B63)** az S5 előtt (`Sir` / `JSir`).
3. **HN-03** (a hatókör-sor zárójeles forráslistája): a mai jóváhagyott szöveg áll.

### Amit az S3 az S2-ből örököl

- **Egy rövid jelentés-út** (`bemenet/motivum.py` `rovid_jelentes`): a 4. szakasz Áttekintése és a szócikkfej ugyanezt használja (GK-16); magyar jelentés híján kimondott hiány, az angol „fordításra vár” alak a 4. szakasz szelete (GK-15).
- **A szótári alak és kiejtés** (`Kiejtes.szotari(strong, versek)`): a lemma-változat a motívum versei szerint (GK-13). A 4. szakasz szócikkcíme ebből jön; a pontozatlan héber alak kiejtése itt már megvan (az S1-ben kimondott hibával megálló ág a ragozott alaké).
- **HTML a sablonmondatban.** A lenyíló blokk jelölése (`<details>`, `<summary>`, `<p>`, `<ul>`, `<li>`, `<em>`, `<a href>`) a sablonmondat része; a blokkba kerülő kézi szöveg és idézet a `vizsgalat.html_ben` kapun megy át (`<`, `>`, `&` nem állhat benne; a generátor nem kódol át).
- **Cellakezdő alak:** sablonsorként, illetve névtábla-sorként (`halo_leiras`), ahogy a lapon áll; átírás nincs (DT-F218k).
- **A mellékletre és a lapon belülre mutató horgony** a cél címsorából, illetve az igehelyből képződik (`cim_horgony`, `Igehely.horgony`); teszt ellenőrzi, hogy minden link létező célra mutat.
- **Az engedélyfájl írása.** A `regresszio.py` részletes diffje csak az engedély nélküli sorokat adja: új osztály felvételéhez a szelet engedélysorait előbb ki kell venni a fájlból, a regressziót futtatni, majd `engedely_ir.py <diff> naplok/F218_elteres_engedely.tsv <jegyzetmappa>/F218_eszkozok/osztaly_s2.py` (az osztályfájl szigorú: a funkció-osztály csak akkor ad engedélyt, ha a sor egyetlen eltérése a kezdőbetű). Az S3-hoz új osztályfájl kell (`MEGTART`: minden korábbi azonosító).
- **Referencia-tábla.** Új táblasor vagy új bemenet után: `referencia_frissit.py --naplo <kimenet>/lexikon/<ID>_olvasasi_naplo.tsv` mindkét mintalapra, és `--frissit adat/lapgen_sablonok.tsv adat/olvasoi_nevtabla.tsv adat/lapgen_bemenetek.tsv dontesek/uj/f218-generator-uj-a.md`.
- **Magyar szöveget tartalmazó szkript:** a Write eszközzel fájlba, és úgy futtatva (a heredoc elromlik rajta).

### A régi generátorból visszafejtett szabályok (S2, Döntési út)

- **1.1.** A negatív kritérium a „Nem tartozik ide” szavaknál válik ketté; a második rész végére a fölérendelt fogalom kerül („A motívumon kívül eső tágabb kör: … .”). A régi `olvasoi_indok` tisztítása a HAMART-szövegen az önreferencián kívül semmit nem változtatott.
- **1.2.** A lánc szavai: a `gerinc_elem` `+`-szal tagolt részei közül a Strong-számok, a héber szavak elöl, azon belül Strong-szám szerint; `lemma (kiejtés), rövid jelentés`, a jelentés csak ha van magyar. A tábla sorai a teljesség-mérés keresései az első előfordulásuk rendjében; az ajánlás-sor csak ha a szám nem 0.
- **1.3.** A csoportos ok alatt legfeljebb öt példa: a csoportos (összesítő) jelölt-sorok igehelyei a döntésnapló rendjében, a Károli-szöveggel. Az egyenkénti ok versei a döntésnapló rendjében (a melléklet ugyanezeket a Károli versrendjében adja). Az okok rendje: versszám szerint csökkenő, azon belül a címke betűrendje.
- **1.4.** Csoportosítás a `gerinc_elem` szerint, a tábla (nem a kánon) rendjében; minden `tematikus:` kezdetű elem egy csoport. A csoport neve: Strong-részeknél `lemma (kiejtés)` ` + `-szal, egyetlen szónál ` — rövid jelentés`; nem Strong részeknél „szópár: a + b” (a részek kézi nevek). A megoszlás: „N hely: x a Genezisben, y az Ószövetség többi könyvében és z az Újszövetségben”, egy helynél „Egy hely, a Genezisben”.
- **1.5.** Határeset: a nem magas megbízhatóságú sorok, a tábla rendjében, a megbízhatóság nevével. A nyitott kérdések: az `ertelmezes` rés „Vitatott pontok” félkövér címei, majd a `modszertan` rés „Nyitott kérdések” számozott címei, mindegyikhez az első mondat.

### A felhasználó megállási küszöbe

**Érvényes szabály (a felhasználó, az orkesztrátoron át, 2026-11-13, szó szerint): „99 % az új szabály”.** A megállási küszöb a heti keret („Weekly · all models”) 99%-a; elérésekor ugyanúgy zöld állapotban zárás (commit, folytatási fájl, push) és jelzés. A 70%-os kontextus-szabály változatlan. Az alábbi bekezdés a korábbi, 96%-os szabályt rögzíti (felülírva).

A felhasználó (az orkesztrátoron át, 2026-11-13, szó szerint): „megállási köszüb 96% legyen”. Minden commit előtt `get_usage`. Ha a heti keret („Weekly · all models”) eléri a 96%-ot: az épp futó lépés zöld állapotban lezárul (commit, folytatási fájl, push), megállás, a pontos százalék jelzése az orkesztrátornak. Új szelet 96% fölött nem indul. Ez a brief megállási szabálya mellett érvényes.

## Hogyan futtatható

- Tesztek: `python eszkozok/lapgen/tesztek/futtat.py` (minden), `… futtat.py szoveg szerkezet` (megnevezett fájlok).
- Új lap: `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon2 --id HAMART-001 --kimenet <repón kívüli könyvtár>`; a fájlok a `<kimenet>/lexikon/` alá kerülnek.
- Regresszió: `python eszkozok/lapgen/regresszio.py --id HAMART-001 --uj <kimenet>/lexikon --reszletes <fájl>`.
- Festékpróba: `python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001`.
- A régi generátor egyezése: `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon --id HAMART-001 --kimenet <ideiglenes>`, majd `cmp` a `git show HEAD:lexikon/HAMART-001_TUDOMANYOS.md` tartalmával (a munkafa CRLF-es, a blob LF-es).
- Push előtt: `python eszkozok/push_elott.py --pr-cim "F218: a lapgenerátor újraírása, 1. rész — építés a regresszióig"` (kb. 7 perc, a háttérben), csak 0 HIBA-val.
- Táblasor hozzáadása: magyar szöveget tartalmazó kódot heredocból futtatni tilos (és el is romlik); a sorokat Python-fájlba kell írni, és úgy futtatni.

## Tervezési döntések

- **Három konstruktor:** `proza(kezi)`, `sablon(sor, **p)`, `idezet(forrasszoveg)`. Az `idezet` egyetlen argumentumot kap: a forrást (B-azonosító) és a helyet maga a `Forrasszoveg` érték hordozza (a brief `idezet(forras, hely, szoveg)` alakjának szigorítása).
- **A `Lathato` nem `str`:** nincs rajta szövegművelet, `str()`/formázás kivételt dob; szöveggé csak a `kiiras()` alakítja, amelyet csak a `megjelenites/md/iro.py` hív (statikus teszt).
- **Burkolók a bemeneti rétegből:** `Kezi` → `proza`; `Forrasszoveg` → `idezet`; `Belso`, `Kulcs`, `Utvonal` → csak `Proveniencia` vagy (kulcsnál) névtábla. A burkolót csak a `bemenet/` hozhatja létre.
- **Nyilvános azonosító-típusok** (a brief felsorolásán túl): `Strong`, `MotivumId`, `Horgony` az `Igehely` mellett; szigorú alakjuk miatt megjeleníthetők.
- **Sablonmondat:** `{nev}`; skalárnál `{nev|a}` / `{nev|A}` névelőt tesz elé (a/az; számnál a kiejtés szerint), `{nev|a:masik}` a névelőt a megnevezett másik paraméter szövege szerint választja (pl. a görög szó kiejtése); a `cella` módosító megszűnt (DT-F218k); listánál `{elemek|; }`, illetve `{elemek|, | és }`. A mondatban Markdown-jelölés állhat. A megjelenítő saját literálja csak szerkezeti jelölés (`Jel`, zárt készlet az író modulban).
- **Fajta-térkép:** az író minden kiírt sorhoz tartományokat ad (próza / sablon / idézet / megjegyzés / jelölés); ezt használja a festékpróba, és ezt fogja használni az alakosztály-kapu (GK-24).
- **Festés:** a burkoló `szoveg` alakja festett futásban jelzőszót hordoz (`ZZQ<B-azonosító>_<mező>ZZ`); az `ertek` változatlan. Belső jelzőszó csak megjegyzésben állhat, kézi csak prózában, idézeté csak idézetben.
- **Blokkjelölő:** a lapon `general.py --cel lexikon#…` áll (a termék célneve), nem `lexikon2`.
- **Hash:** sorvég-normalizált tartalomból (`\r\n` → `\n`), a bemeneti rétegben és a regresszióban is.
- **`ts=`:** `PARDES_DATUM`-ból vagy a `--datum` paraméterből; nélkülük `ts=b:<12 jegy>` az olvasási napló hash-éből.
- **Jegyzék:** a sor a bemeneti függvénnyel együtt kerül a táblába (statikus teszt: sor ↔ `b<nn>_…` függvény, egy az egyhez). Több fájlos bemenetnél az `utvonal` `;`-vel sorol fel; nem fájl-bemenet (szabálymodul) útvonala `-`.
- **Regresszió:** szakasz = 2. szintű címsor; soronkénti diff; az engedélyfájl `regi`/`uj` oszlopa `sor` kötésnél a sor sha256-ának első 16 jegye. Részleges lapnál a még nem kész szakasz „nincs kész”, és az engedélysora nem számít.
- **A megjegyzések is bájtra egyeznek:** a régi lap `<!-- eredeti: … -->` megjegyzéseit az új generátor `Proveniencia`-ként, ugyanabból a szerkezetből állítja elő, mint a látható mondatot (két párhuzamos megjelenítés, nem egymásból képzett szöveg).
- **A szótári gerinc megosztása:** a forrás szerkezetének feloldása (melyik példahely melyik szócikké, szakaszjel, címke, glossza) a `bemenet/gerinc.py`; a döntés (melyik címke áll a soron, és miért) a `szamitas/szotari_gerinc.py`, szerkezetként (`Indok` fajtával); a mondat a megjelenítőben, a sablontáblából.
- **Újrahasznosított régi segédmodulok** (tiszta függvények, az útvonalat a jegyzékből kapják): `heber_kiejtes`, `kiejtes`, `bdb_tagolas`, `bdb_rovidites`, `szotari_glossza`. A `lexikon_general.py`-ból az új kód semmit nem importál.
- **T3:** a tematikus hely saját szava külön kézi táblában (`adat/tematikus_sajat_szo.tsv`, B67, SEMA 2.63; DT-F218i), nem az `elofordulasok.tsv` új oszlopában.

## A régi generátorból visszafejtett szabályok (S1)

- **Lánc.** A régi lap nyers blokkokból épül, majd tíz utófeldolgozó lépés írja át (címcsere → olvasói átírás → névelő-levétel → kiejtés-pótlás → Strong/BDB/könyvnév/idézőjel → lábjegyzet a tábla alá → közös forrásmegjelölés → önreferencia-csere). A lánc táblája: `naplok/F218_jelentes.md` „F218.1 — szimbólumtérkép”. A közbenső állapotok mérésére a régi generátor függvényei burkolhatók (repón kívüli szkripttel), így látszik, melyik lépés mit változtat egy szakaszon.
- **Cellakezdet (`nevelo_le`).** Minden tábla- és listaelem: ha kisbetűs „a ”/„az ” névelővel kezdődik, és utána hatnál kevesebb szó áll, a névelő elmarad, és az elem nagy kezdőbetűt kap („a szócikk egésze — fájdalom” → „Szócikk egésze — fájdalom”); hat vagy több szónál a névelő marad, nagy kezdőbetűvel („a megművelt föld, amely táplál · 1” → „A megművelt…”). A szószám a cella egészére értendő (a szakaszjel és a „·” is szó). Az új generátorban **nincs** ilyen átírás (DT-F218k): a cella elején álló sablonmondat külön sablonsor, a kézi címke cellakezdő alakja a névtábla `cimke_cella` sora; más kézi szöveg és az idézet szó szerint áll.
- **Kulcsszó-cella.** `Károli-szó — alak (kiejtés)`; több Strongnál az alakok „; ”-vel. Héberül a teljes szó (előtag + tő + toldalék a szöveg soraiból, `heber_kiejtes.teljes_szo`) és a gépi kiejtése; görögül a ragozott alak és a magyaros átírása. A záró írásjel (`,.;·`) lemarad az alakról. A régi az utolsó előfordulást vette (a szótárindex felülírása miatt); az új (DT-F218j) azt, amelyhez a sor Károli-szava a párosításban (B54) kötődik, párosítás híján az elsőt.
- **Jelentés-cella.** Címkével: `címke · jel`; címke nélkül, BDB-jellel: `a szakasz olvasói glosszája · jel`; jel nélküli héber szónál, ha a szócikk tagolatlan: `a szócikk egésze — a fej glosszája`; különben `*(nincs címke: jel)*`, illetve `*(nincs hozzárendelés)*`. Több szónál `H…: …; H…: …`. A nem BDB-jel a szótár nevével áll („Thayer 1”, „Thayer fej”).
- **A címke elsőbbsége.** Ha a BDB maga idézi a verset, és az útja a szerkesztői hozzárendelés alá esik, a finomabb út címkéje áll; ha a szerkesztői út esik a példa alá, a szerkesztői; ha egyik sem, a futás megáll. Ha a Strong többször áll a versben, a versszintű BDB-példa nem kerül a szóra. Több útvonalú példánál a szerkesztői hozzárendelés dönt, ha pontosan egy esik alá.
- **Jegyzet (egyszavas sor).** `Igazolás; a jelentés: indok.` Az igazolás: „A héber szöveg (TAHOT) igazolja” / „Újszövetségi hely: a szó a görög szövegben áll” (hatókörön kívül, újszövetségi sor) / „A héber szöveg-igazolás itt nem alkalmazható” / „Szövegigazolás nélkül”. Az indok az első indok fajtája szerint: BDB-példa → „a BDB a(z) X szakaszban maga idézi a helyet” (a puszta szám ponttal: „az 1.”); más szakaszban is → „a BDB a helyet a(z) X is idézi”; szerkesztői hozzárendelés → „a BDB X szakasza” / „a Thayer szócikkfeje”; tagolatlan → „a szócikk egésze (a szótár nem tagolja számozott jelentésekre)”. A tematikus sor jegyzete egyetlen mondat, igazolás nélkül.
- **Jegyzet (többszavas, szópáros sor).** Mondatonként: az igazolás, majd szavanként `H…: rövid mondat` (a cella tartalmát nem ismétli); a „nincs hozzárendelés” szóról nem szól mondat.
- **Összevonás.** Az azonos látható mondatú jegyzet egyszer áll; a szám az első hivatkozás sorrendje; a sor jelentés- és megbízhatóság-cellája is hivatkozik rá (a tematikus sornál csak az utóbbi). Az összevont sor végén minden eredeti lábjegyzet `<!-- eredeti: [^n]: proveniencia: … | igazolas: … | jelentés-címke: … -->` megjegyzésként áll.
- **Közös forrásmegjelölés.** A legalább két jegyzetben álló `scope=… | forras=… | ts=…` hármas jelet kap (‹E1›, ‹E2› …, gyakoriság, majd szöveg szerint); a tábla alatt egy megjegyzéspár áll: `<!-- közös forrásmegjelölés: … -->` (olvasói alak: „forrás: kézi szerkesztés, dátum”) és `<!-- eredeti: … -->`.
- **UBS-cella.** Újszövetségi sor: a görög UBS-szótár versre hivatkozott jelentései, `glossza [ⓘ](/szo/Strong)`, több jelentésnél vagy tartománynál `*(lehetséges, nem egyértelmű)*`. Ószövetségi sor: a héber UBS-szótár a Károli-vers masszoréta megfelelőjén; eltérő versnél `*(MT: vers)*`. A glossza a fordítástáblából (`glosszak_hu`), híján az angol `*(fordításra vár)*` jelöléssel.
- **Önreferencia-csere.** A régi kód nyolc rögzített szövegpárral cserélte a „lap” szót (`tablajegyzet.ONREF_CSERE`), adatcellákban is; az új generátor prózát nem ír át. A négy adatcella-párból egy a forrásban javult (1Móz 8:21), három nyitva (DT-F218l; a mérés a jelentésben). A négy közös generátormondat-pár (Tartalom, Jelmagyarázat, Kolofon, Idézés) az új sablontáblába már a javított szöveggel kerül.

## Nyitott kérdések (a felhasználóhoz, illetve az orkesztrátorhoz)

- **Önreferencia (DT-F218l):** lezárva, ✅ (a forrásban javítva). Nyitva maradt belőle: a szóválasztás megerősítése („vizsgálat” / „listán”, nem „szócikk”), a nyílt mag angol szövege („the entry” maradt), és az `ir`-en kívüli hat fájl (a jelentés „DT-F218l” szakasza).
- **Az 1.4 pont kisbetűs listaelemei** (15 engedélysor): a funkció magyarázata a forrás szerint áll; ha nagybetű kell, a mondatkezdő alak adatba kerül.
- **„mind a 575 verse” / „A 575 vers”:** betűre a régi lap; a helyes névelő 1-1 engedélysor volna.
- **Három új sablonmondat `dontes=var`** az S2-ből (`e2.jel.szocikkel`, `e2.jel.szocikk_sorszam`, `d14.hely.magyarazat_nelkul`) és kettő az S2a-ból: a 218a végi listába.
- **ISTENTISZT-001, hat kisbetűs cellakezdet:** öt Károli-idézet és egy funkciócímke („a népek ígérete”) a forrás szerint, szó szerint áll; a régi lap nagybetűsítette. Olvasói döntés (a jelentés „Javítókör” szakaszának 1. pontja).
- **A 7 új sablonmondat `dontes` mezője:** a felhasználó jóváhagyta („Igen, mind jó”); a mező a jóváhagyás döntésszámát várja, addig `var`.
- **HN-03:** a hatókör-sor zárójeles forráslistája a mai jóváhagyott szöveg; ha javítandó, új mondat kell, jóváhagyással.
- **Alias-sorok (GK-17, B63):** a normalizáló tábla 4. oszlopát több eszköz olvassa; döntés az S5 előtt kell.
- **A CI nem futtatja a `lapgen/tesztek`-et:** a bekötés a 218c N-tételébe kerül.
- **Függések:** a `feladatok.py fuggesek` a 194 és a 212 tétellel is `KIZAR` sort ad (l. a jelentés F218.0 szakaszát).
- **`teszt_szintek.py`:** az olvasó-szerver tesztje 13-ból 2 bukással áll a fő checkouton is; nem ebből a diffből jön (N-F218a, `nyitott/uj/f218-generator-uj-a.md`).

## Megállási küszöb

Az S1 szakasz-diffje a heti keret 89%-ánál lett 0 (az engedélyeken kívül); a küszöb 91,5% volt. A megállási szabály első feltétele teljesült. A T4 osztály tényleges száma (3) az előre rögzítettől (2) 20%-nál jobban eltér: az ok a mérés hatóköre (csak a héber szöveg), a jelentés kimondja; a ⛔ megállás az S1 után amúgy is esedékes.

## Mérőszámok

| Pont | Dátum (UTC) | Heti · minden modell | Heti · Fable | 5 órás | Megjegyzés |
|---|---|---|---|---|---|
| F218.0 (indulás) | 2026-11-13 09:05 | 83% | 15% | 19% | `get_usage`; nullázás: 2026-11-14 14:00 UTC |
| F218.2 után | 2026-11-13 09:35 | 85% | 20% | 38% | az F218.1 (sonnet) és az F218.2 együtt 2 százalékpont |
| S1 első fele után | 2026-11-13 09:55 | 87% | 22% | 48% | a régi kód olvasása és a 2.1 pont: 2 százalékpont |
| S1 diff 0 | 2026-11-13 10:35 | 89% | 27% | 66% | a tábla, a jelentés-oszlop és a jegyzetek: 2 százalékpont |
| S1 tesztek, push | 2026-11-13 11:00 | 90% | 28% | 71% | a tesztek és a tesztváz: 1 százalékpont; a kontextus 80% |
| Javítókör indul (2. session) | 2026-11-13 11:27 | 91% | 30% | 82% | az orkesztrátor üzenete, a futó sessionök |
| Javítókör kész | 2026-11-13 12:00 | 93% | 35% | 98% | a javítókör (9 tétel, 4 commit): 2 százalékpont heti; a kontextus 45% |
| Újraindítás (a keret nullázva) | 2026-11-13 12:15 | 76% | 0% | 0% | az orkesztrátor üzenete |
| S2 első fele kész | 2026-11-13 | 78% | 4% | 16% | az S2 első fele és a 2. ellenőrzés: 2 százalékpont heti; a kontextus 67% |
| 3. session indul | 2026-11-13 13:35 | 79% | 5% | 20% | modell-eltérés miatt előbb megállt (opus), utána fable |
| 2. javítókör és DT-F218l kész | 2026-11-13 | 81% | 9% | 37% | a javítókör és a forrásjavítás: 2 százalékpont heti; a kontextus 46% |
| S2 kész (a Döntési út diffje 0) | 2026-11-13 | 82% | 12% | 47% | az S2 második fele: 1 százalékpont heti; a kontextus 59% |

Diff-görbe (engedélyen kívüli diff-sorok, commitonként):

| Commit | 2. Előfordulások (437 sor) | Megjegyzés |
|---|---|---|
| F218.4 (1) | 76 | az összegző mondat, a hatókör-sor és a 2.1 pont egyezik |
| F218.4 (2) | 0 (5 engedélysor) | a tábla, a 17 jegyzet, a közös forrásmegjelölés, az UBS-magyarázat |
| Javítókör | 0 (1 engedélysor) | T4 a párosításból (−3), az önreferencia a forrásban (−1); marad a blokkfejléc |
| F218.5 (S2a) | melléklet (431 sor): 0 (10 engedélysor) | az első futás 10 diff-sort adott, mind előre várt osztály |
| F218.5 (DT-F218l) | melléklet: 0 (8 engedélysor) | a két önreferencia-sor megszűnt (a forrás javult) |
| F218.5 (S2b) | 1. Döntési út (110 sor): 0 (16 engedélysor) | az első futás 17 diff-sort adott: 16 előre várt osztály és 1 hiba (a lemma-változat szabálya hiányzott: javítva) |

Festékpróba: HAMART-001 0 szivárgás (belső 191, idézet 420, kézi 364 látott jelzőszó az S2 végén; az S2a után 171, 326, 240); ISTENTISZT-001 0 (134, 208, 185). Mutációs próba: még nincs. Átszökési arány: még nincs mérés (az 1. ellenőrzés és a felhasználó átnézése után).

## Session-váltások, kompaktálások

- 1. session (2026-11-13): az indulás `claude-opus-5-5` modellen modell-eltérés miatt megállt; a felhasználó a sessiont `claude-fable-5-2`-re állította. Egy megszakadás (hitelesítési hiba) az S1 közben, adatvesztés nélkül. Kompaktálás eddig: 0; a kontextus az S1 végén 76%.
- 2. session (2026-11-13, `claude-fable-5-2`, az orkesztrátor indította): a javítókör. Kompaktálás: 0. A kontextus a javítókör végén 45%; az 5 órás keret 98%.
- 3. session (2026-11-13, az orkesztrátor indította): az indulás `claude-opus-5-5` modellen modell-eltérés miatt megállt, munka nélkül; a felhasználó a sessiont `claude-fable-5-2`-re állította (xhigh). A 2. ellenőrzés javítóköre, a DT-F218l és az S2 második fele. Kompaktálás: 0; a kontextus az S2 végén kb. 60%.
