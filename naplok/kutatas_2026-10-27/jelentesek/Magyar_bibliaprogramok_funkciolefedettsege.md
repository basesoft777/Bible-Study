# Magyar bibliaprogramok funkciólefedettsége

*2026-10-27, átdolgozva. Források: három kutatási jegyzet (`research_notes/Magyar bibliaprogramok funkciólefedettsége/alkalmazasok.md`, `weboldalak.md`, `kiegeszites.md`).*

**Jelek:** ✅ van · ◐ részben · ❌ nincs · ? nem ellenőrizhető. A projekt oszlopa a repó állapota (terv = még nincs kész).

**Bizonyosság:** a jel jelöletlenül a letöltött oldalon, kódon vagy adaton látott állapot. **[S]** = csak keresőkivonat. **[P21]** = M. Pintér (2021) leírása, a 2021-es állapotról. **[F]** = a projekt tulajdonosának saját használati tapasztalata (2026-10-27).

| Funkció | Biblia-Felfedező | szentiras.eu | szentiras.hu | YouVersion | AndBible | Logos | szeroczei | EBO (KRE) | Bibliatársulat Szómutató | parallelbible.nytud.hu | **Projekt** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Magyar fordítások | ✅ kb. 18 (RÚF nélkül); a Strong-os HUN 2026-ban modernizált Károli | ✅ 7 | ✅ 12 szöveg | ✅ 6 | ✅ 5 SWORD-modul (Károli 1908, UF, RÚF, KNB, IMIT) | ◐ 1 (karakterhibás) | ✅ sok régi | ✅ 19 + 7 idegen [P21] | ❌ nem szövegolvasó; „bármely fordításhoz” | ✅ 14, kódexektől a 2014-es MBT-ig (betűhű + normalizált) | ◐ Károli 1908 |
| Strong a magyar szövegben, szószinten | ✅ zárt, fizetős modul [F]; ÓSZ teljessége vitatott | ◐ csak a görög szövegben, magyar glosszával | ❌ | ❌ | ❌ (egy magyar SWORD-modulban sincs Strong-szűrő) | ❌ | ◐ versszinten | ? | ❌ (az ÚSZ-sorszám valószínűleg Strong-szám, az ÓSZ-é saját) | ❌ | ✅ (9 ÚSZ-könyv még párosítatlan) |
| Interlineáris | ? | ✅ görög ÚSZ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ párhuzamos, nem szószintű [P21] | ❌ | ❌ csak versszintű párhuzam | ✅ |
| Héber szöveg | ? | ❌ | ✅ | ❌ | ? | ❌ | ❌ | ✅ 1 héber [P21] | ◐ héber/arámi címszójegyzék | ❌ | ✅ |
| Héber szótár magyarul | ◐ egyszerű szótár, nem BDB; fizetős modul [F] | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ terv [P21] | ✅ Babits: Ószövetségi Szómutató (zárt, ingyenes online) | ❌ | ◐ BDB-fordítás folyamatban |
| Görög szótár magyarul | ◐ egyszerű szótár; fizetős modul [F] | ✅ MI-generált, CC BY-SA | ❌ | ❌ | ❌ | ❌ | ❌ 2026-ban angol (P21 szerint magyar is volt) | ❌ terv [P21] | ✅ Balázs: Újszövetségi Szómutató (zárt, ingyenes online) | ❌ | ◐ Thayer-fordítás folyamatban |
| Konkordancia eredeti szó szerint | ✅ (kivonat) | ◐ görög ÚSZ | ❌ | ❌ | ❌ | ❌ | ◐ versszint, angol definíció | ❌ 2021-ben nincs kereső; 2022: terv | ◐ magyar szó → héber/görög címszó; a szócikkben igehelyek (teljesség ?) | ❌ csak igehelyre keres | ✅ |
| LXX + héber–görög kapcsolat | ? | ❌ | ◐ LXX-szöveg, kapcsolat nélkül | ❌ | ❌ | ❌ | ❌ | ? (1 görög szöveg, kiléte ?) | ❌ | ❌ | ✅ LXX-híd, 90 döntés |
| Kereszthivatkozás | ✅ Nave-alapú | ❌ | ? | ❌ | ✅ TSK; HunKar: Károli-margó | ? | ❌ | ? | ❌ | ❌ | ✅ TSK, Nave, OpenBible, Károli-margó |
| Versszámozás-kulcs Károli↔MT↔LXX↔KJV | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ? (belső alvers-szinkron [P21]) | ❌ | ◐ csak versszintű magyar↔KJV↔finn igazítás | ✅ |
| Motívum- vagy fogalomszócikk | ❌ | ◐ MI-kommentár versenként | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ (napi kalauzok) [P21] | ❌ lexikai szócikk | ❌ | ✅ motívumlexikon |
| Döntésnapló, proveniencia | ❌ | ◐ ellenőrzöttségi szint; a szócikk modellneve a kódban | ❌ | ❌ | ❌ | ❌ | ❌ | ◐ a fejlesztést tanulmánykötet dokumentálja [P21] | ❌ | ◐ korpuszleírás (Simon–Kalivoda 2020) | ✅ |
| Nyílt licenc, API | ❌ | ✅ CC BY-SA (saját anyag), kód AGPL-3.0, REST API, MCP; tömeges dump nincs | ❌ | ❌ | ✅ GPL (app); HunKar PD, a többi modul jogvédett | ❌ | ❌ | ? | ❌ „minden letöltés tilos” | ✅ TSV a GitHubon, CC BY-SA 4.0 (3 modern fordítás nélkül) | ◐ CC BY terv |
| DOI, idézhetőség | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ◐ tanulmányok idézhetők, adat-DOI nincs | ❌ | ◐ idézendő cikk, DOI nélkül | ◐ terv |
| Offline | ✅ | ? | ✅ app | ◐ | ✅ | ✅ | ❌ | ? | ❌ | ◐ TSV letölthető | ◐ PWA terv |
| Ár | alap ingyenes; modulok 1 290–19 990 Ft | ingyenes | ingyenes | ingyenes | ingyenes | 13,99 USD/modul | ingyenes | ingyenes? | ingyenes (feltétel-elfogadással, belépéssel) | ingyenes | ingyenes (terv) |
| Elterjedtség | Play 1 M+, 4,9★ | ? | app 10 E+ | 100 M+ (globális) | 500 E+ | ? | ? | ? (projekt lezárva 2024.04 [S]) | ? | ? | — |

## Mi változott az előző változathoz képest

- **Három új oszlop.**
  - **EBO** (KRE Egyesített Bibliaolvasó): az oldal blokkolt, adatai csak Pintér 2021-es leírásából és keresőkivonatokból származnak.
  - **Bibliatársulat Szómutató Szótár**: héber–magyar (Babits) és görög–magyar (Balázs) szómutató. Ingyenes online, de jogvédett, és a letöltést tiltja.
  - **parallelbible.nytud.hu**: történeti magyar fordítások versszinten igazítva, CC BY-SA TSV-ben.
- **A Biblia-Felfedező szótára egyszerű szótár, nem BDB** (a tulajdonos saját tapasztalata; a keresőkivonat „Óhéber–Magyar BDB” elnevezése félrevezető volt). A szótár és a Strong is fizetős modul. **BDB-szintű héber–magyar lexikon tehát egyik vizsgált eszközben sincs, zártan sem.**
- **Magyar héber szótár online már nem csak a Biblia-Felfedezőben van**: a Bibliatársulat ÓSZ-Szómutatója ingyenes. A mátrixban viszont egyik szótár sem nyílt adat.
- **AndBible**: a CrossWire fő tárában 5 magyar modul van, és egyikben sincs Strong-címke. Strong-taggelt magyar SWORD-modul ma nem létezik.
- **szentiras.eu**: a kód AGPL-3.0 licencű. A görög szószedet CC BY-SA, de kész letölthető fájl nincs, csak szócikkenként API-n és MCP-n érhető el. Az ujszov.szentiras.eu ide irányít át.
- **GitHub**: nyílt, Strong-taggelt vagy szószinten igazított magyar bibliaszöveget nem találtam. Ez negatív lelet, nem kimerítő keresés.

## Ellenőrizetlen pontok

- **Biblia-Felfedező:** az ÓSZ-párosítás mai teljessége, az interlineáris nézet és az LXX-modul továbbra is nyitott. A bolti leírásban egyiknek sincs nyoma. A bible-discovery.com és a mobilbiblia.hu blokkolt. Az iOS-changelog szerint a Strong-os HUN-szöveg kb. 15 ezer helyen modernizált Károli.
- **EBO:** a mai működés, a kereső, a Strong- és szótárfunkció, a licenc és az adat nem ellenőrizhető. Az ebo.kre.hu és a btk.kre.hu blokkolt. Pintér–Márkus (2022) konkordancia-megoldást ígért, ennek sorsa ismeretlen.
- **Szómutató Szótárak:** a szócikkek szerkezete és az igehelylisták teljessége ismeretlen. A használathoz el kellene fogadni a feltételeket, ezt nem tettem meg a felhasználó nevében. Az ÚSZ-sorszám Strong-egyezése következtetés, az ábécé-ugrópontok alapján.
- **szeroczei:** Pintér (2021) szerint a Strong-keresés a lexikon „magyar fordítását” is adta, 2026-ban viszont angol definíciót láttam. Az ellentmondás feloldatlan.
- **Pintér 2021/2022 említett, de most nem elérhető oldalai** (a proxy nem engedte):
  - Árpádffy Károli-konkordanciája (polarhome.com/biblia);
  - biblia.hit.hu;
  - online-biblia.ro;
  - okosbiblia.hu;
  - az ÚRK-konkordancia (ESV-címszavakra, félautomatikus; elkészülte ismeretlen).
- **szentiras.hu:** a keresés és a hivatkozások továbbra is JavaScriptből töltődnek. Pintér leírásai a régi kódra vonatkoznak, amely ma a szentiras.eu-n fut.
- **Elérhetetlen oldalak:** a bibliaonline.hu nem működik, a szit.hu 429-et adott.
- **Tisztázandó licencek:**
  - parallelbible: a README a CC BY 4.0-ra linkel, a LICENSE-fájl viszont CC BY-SA 4.0.
  - `peterpolgar/Biblia-json-xml`: jogvédett fordításokat tartalmaz Unlicense alatt, ezért nem jogtiszta.
