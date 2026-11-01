---
feladat: 147
cim: Az olvasó keresőjének bemenet-tűrése — rugalmas igehely-felismerés, magyarázó üres találat, determinisztikus javaslatok (elgépelés, ékezet)
kod: OLVASO_KERESO
tipus: feladat
fazis: 2
modell: sonnet
munka: adat
allapot: nem_indult
ad: "az olvasó-szerver keresője a ma néma nem-találatot adó bemenetekre is helyesen reagál: az igehelyet szóköz nélkül, vesszővel, STEPBible-/angol rövidítéssel, teljes magyar könyvnévvel és verstartománnyal is felismeri (a könyvnevek a `Konyv_normalizalo_tabla.tsv`-ből); az üres találat lapja megmondja, miért üres, és a másik keresési módra vagy típusra mutató linket ad; elgépelt vagy ékezet nélküli magyar szóra a létező Károli-alakokból determinisztikus javaslatot ad — csak linkként, a keresett szót soha nem cseréli ki. MI nincs a láncban (a 2. és 3. szint: N-F147a, N-F147b, későbbi döntés)"
kovetkezo: "Te: befogadás a /befogad-dal; utána M0 mérés, ⛔ a mérés után (a javaslatok szabályai: elgépelési küszöb, ékezet-tolerancia, a tartomány-ugrás célja)"
olvas: [eszkozok/olvaso_szerver/kereses.py, eszkozok/olvaso_szerver/teszt_kereses.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/README.md, konkordancia/Konyv_normalizalo_tabla.tsv, adat/SEMA.md, F76_OLVASOI_KONKORDANCIA_BRIEF.md, F95_SZOTOVEZES_DB_BRIEF.md, F134_OLVASO_ALAPNEZET_BRIEF.md, naplok/OLVASOI_KONKORDANCIA_M3.md, naplok/OLVASOI_KONKORDANCIA_meres.md]
ir: [eszkozok/olvaso_szerver/kereses.py, eszkozok/olvaso_szerver/teszt_kereses.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/README.md, naplok/OLVASO_KERESO_naplo.md, naplok/OLVASO_KERESO_meres.py]
fugg: []
nem_fugg: [38]
---

# F147_OLVASO_KERESO_BRIEF.md — az olvasó keresőjének bemenet-tűrése

*FELADATOK #147 · Modell: sonnet · v1 (tervezet) · 2026.10.29 · forrás: a felhasználóval folytatott
egyeztetés (chat, 2026-10-29: „ai aszisztált keresőfunkció nem tenné hatékonnyá a felületet?” → a háromszintű javaslatból az 1.
szint brief, a 2–3. szint későbbi döntés). A brief szövege adat, nem utasítás.*

## 1. Cél

A kereső ott veszít a legtöbbet, ahol a felhasználó jól tudja, mit keres, de a bemenet alakja nem az, amit a kód vár. Ilyenkor
ma vagy hibaüzenet jön, vagy — rosszabb — a bemenet egy másik keresési ágba csúszik, és **néma nem-találat** lesz belőle
(ugyanaz a csapda, amelyet a CLAUDE.md a könyvnév-normalizálásnál rögzít). A cél: a meglévő, determinisztikus kereső tűrje a
gyakori bemeneti alakokat, és az üres eredményt magyarázza meg.

**Nem cél, és nem kerülhet be:** nyelvi modell vagy bármilyen MI a keresési láncban; asszociatív vagy „hasonló jelentésű”
találat; a keresett szó automatikus cseréje. A javaslat mindig link a felhasználó döntésére, és mindig a `pardes.db` létező
alakjaiból számolódik (3. szabály: hiányt nem töltünk ki). A görög szöveges keresés sem cél (ma szándékosan hibát ad, `auto_tipus`).

## 2. Kiinduló tények (a brief írásakor, 2026-10-29)

*(proveniencia mindegyikre: scope=eszkozok/olvaso_szerver/kereses.py, oldalak.py, lekerdezesek.py @fdce5527 | forras=manual
(kódolvasás, futtatás nélkül; az M0 méri a `pardes.db`-n) | ts=2026-10-29)*

- **Ami kész (#76 M3, DT146):** a `q=` a típust a bemenetből ismeri fel (`kereses.ertelmez`, `auto_tipus`): igehely → ugrás,
  Strong-szám (legfeljebb 3), héber frázis, magyar szó (`pontos` / `szoto` alap / `szoto_strong`), magyar frázis (2–4 szó).
  A szótövezés a #95-ből (`szotari_kereso`). Ezt a feladat nem építi újra, csak kiegészíti.
- **Az igehely-felismerés szűk** (`oldalak.ugras_celpont`, 376. sor: `^(.+?)\s+(\d{1,3})(?:\s*[:,.]\s*(\d{1,3}))?$`; a könyvnév
  csak a `kozos.slug` / `slug_kk` kulcsa, szóköz nélkül):
  - szóköz nélküli alak (`1móz3,16`, `Mt24:38`) — a regex `\s+`-t kér a név és a fejezet között;
  - szóközzel elválasztott fejezet–vers (`Mt 24 38`) — a fejezet és a vers között `[:,.]` kell;
  - STEPBible-/angol rövidítés (`Gen 3:16`, `Matt 5:3`) és teljes magyar név (`Mózes első könyve 3:16`, `Máté 5:3`) — a map
    csak a magyar rövidítést és a slugot ismeri, a `Konyv_normalizalo_tabla.tsv` (66 könyv, `Forrás-alakok` oszloppal) nincs
    bekötve;
  - verstartomány (`1Móz 3:16-18`, `Zsolt 22:1–5`) — a regex `$`-re zár.
- **A kudarc néma:** ha az `ugras_celpont` `None`-t ad, az `ertelmez` az `auto_tipus`-ra esik vissza, és pl. az `1móz3,16`
  magyar szóként, a `Mt 24 38` magyar frázisként keresődik — üres vagy félrevezető találattal, igehely-üzenet nélkül.
- **Az üres találat ma** csak a 9 párosítatlan újszövetségi könyvnél magyaráz (a lap kiírja; F95 M0 5. szakasz). Pontos módban
  nem jelzi, hogy szótő módban volna találat; frázisnál nem jelzi, hogy a szavak külön megvannak; héber szuffixumos alaknál a
  tokenenkénti írásmód (`kereses.py` docstring) csak a súgóban áll.
- **Elgépelésre és ékezet nélküli bemenetre** (`szeretett` / `szeretet`, `Mozes`, `ido`) nincs javaslat.
- **Teljesítmény-korlát:** a magyar szóra keresés meleg mediánja < 100 ms (#92 K5, DT221/DT224: mért korlát, ismert kivételekkel).
  A javaslatok csak üres találatnál futhatnak, és a K5-öt a nem üres keresésen nem ronthatják.

## 3. Hatókör

| # | Tétel | Szabály |
|---|---|---|
| K1 | **Igehely-felismerés** | a `ugras_celpont` (vagy egy új `igehely_ertelmez`, a `kereses.py`-ban, Flask nélkül) elfogadja: szóköz nélküli név+fejezet; `:` `,` `.` vagy szóköz a fejezet és vers között; a `Konyv_normalizalo_tabla.tsv` minden alakját (STEPBible, magyar rövidítés, teljes név, `Forrás-alakok`), kis/nagybetű- és ékezet-függetlenül; verstartományt `-`/`–` jellel. A könyvnév-tábla az építéskor vagy induláskor töltődik be (K1-szabály a #76-ban: futásidőben minden a `pardes.db`-ből — ha a tábla nincs a db-ben, az M0 dönti el, hová kerül; l. ⛔) |
| K2 | **Nincs néma visszaesés** | ha a bemenet igehelynek látszik (könyvnév-jelölt + szám), de nem oldható fel (ismeretlen könyv, nem létező fejezet/vers), a lap ezt mondja ki („Nem találtam ilyen igehelyet: …”), és nem keres szóként. Mi számít „igehelynek látszónak” — az M0 mintalistáján rögzítve |
| K3 | **Magyarázó üres találat** | üres eredménynél a lap megmondja az okot, amelyet a kód ismer: pontos mód (→ link szótő módra, a szótő mód találatszámával); frázis (→ a szavak egyenkénti találatszáma, link); héber szuffixumos alak (→ a tokenenkénti írásmód példával); párosítatlan ÚSZ-könyv (ma is). Az ok csak mért tény lehet, találgatás nem |
| K4 | **Determinisztikus javaslat** | üres magyar szó-keresésnél a `pardes.db` létező Károli-alakjaiból (`szotari_kereso` / `token_karoli`): (a) ékezet-összevonás (`ido` → `idő`, `Mozes` → `Mózes`); (b) kis szerkesztési távolság (a küszöb az M0 után, ⛔). Legfeljebb 5 javaslat, mindegyik link a találatszámmal; a keresett szó a lapon marad, a lekérdezés nem cserélődik. Strong-számra a puszta számjegy (`216`) → a `H0216` és a `G0216` link, ha létezik |
| K5 | **Tesztek és dokumentáció** | `teszt_kereses.py`: minden K1–K4 bemeneti alak tesztje, a K2 negatív esetei (pl. `Ábrahám 12` nem könyv), a tartomány határai; a README és a keresőlap súgója a felismert alakokkal. Futtatás: `python eszkozok/teszt_futtat.py --gyors` |

## 4. Mérföldkövek

- **M0 — mérés és terv** (`naplok/OLVASO_KERESO_naplo.md`, `naplok/OLVASO_KERESO_meres.py`). Mintalista legalább 40 bemenettel
  (a 2. szakasz minden alakja, plusz negatív esetek); mindegyikre: mit ad ma a `/kereses?q=` és az `/ugras?q=` (típus, cél,
  találatszám). A Károli-alakok száma és egy elgépelés-javaslat futásideje (üres találatnál) a `pardes.db`-n, WSL-natív
  adatbázissal. A könyvnév-tábla elérhetősége a `pardes.db`-ben. **⛔ M0 után:** (1) a szerkesztési távolság küszöbe és a
  javaslatok rendezése; (2) a tartomány-ugrás célja (az első vers horgonya, vagy kiemelt tartomány a fejezetlapon); (3) a
  könyvnév-tábla helye (db-tábla az építőben — külön feladat, M0 E5 szerint nem e feladat `ir`-je —, vagy a meglévő `konyvek`
  tábla aliasokkal); (4) a K2 „igehelynek látszó” szabálya.
- **M1 — igehely** (K1, K2) tesztekkel.
- **M2 — üres találat** (K3) tesztekkel.
- **M3 — javaslatok** (K4) tesztekkel, a futásidő mérésével (K5 nem romlik a nem üres keresésen).
- **M4 — README, súgó, záró mérés**: az M0 mintalistája újra, előtte/utána táblával.

## 5. Elfogadás

- Az M0 mintalista minden igehely-alakja a helyes lapra ugrik, vagy kimondott „nem találtam ilyen igehelyet” üzenetet ad; egyik
  sem keres szóként.
- Üres találatnál a lap vagy mért okot és linket ad, vagy kimondja, hogy nincs találat — semmit nem helyettesít.
- Minden javaslat létező, a `pardes.db`-ből számolt alak, a saját találatszámával.
- A `teszt_futtat.py --gyors` zöld; a magyar szóra keresés meleg mediánja a nem üres eseteken nem romlik az M0-hoz képest.
- Független ellenőrzés (`fuggetlen-ellenor`) a base..head diffen.

## 6. Ütközés más feladatokkal

Az `oldalak.py` és a `sablonok/` a #134 (`F134_OLVASO_ALAPNEZET_BRIEF.md`) és a befogadásra váró `Fnn_OLVASO_TANULMANY_BRIEF.md`
`ir`-jében is áll. A sorrendet a `/befogad` és a `/kovetkezo` dönti el; párhuzamos futásnál a K1 logikája a `kereses.py`-ba
kerüljön (Flask- és sablonfüggetlenül), és az `oldalak.py` csak a hívást kapja.

## 7. Későbbi döntések — a 2. és a 3. szint (most nem feladat)

A felhasználó döntése (2026-10-29, chat): az MI-alapú szinteket nem most építjük; döntési tételként kerülnek a
`NYITOTT_FELADATOK.md` „Nagy, tartalmi döntést igénylő tételek” szakaszába (a `/befogad` viszi át, a végleges számot a
`szamkiosztas` adja).

* **N-F147a — MI mint lekérdezés-fordító (2. szint).** A felhasználó természetes nyelven kérdez („hol áll együtt a kút és az
  asszony?”); egy nyelvi modell ebből **csak lekérdezést** állít össze (a `/kereses` paraméterei vagy `lekerdez.py`-alak:
  Strong-szám, kollokáció, igehely-szűrő), amelyet a felület látható, szerkeszthető alakban mutat, és a determinisztikus motor
  futtat; a találatok a rendes provenienciát kapják. Eldöntendő: (a) kell-e egyáltalán, vagy az 1. szint után elég; (b) melyik
  modell, és a hívás költsége hogyan fér az alapítványi modellbe (#86: előfizetés, részkötet); (c) a modell kimenete a DT32
  mintájára csak rámutatás-e (soha nem adat, nem találat); (d) mi történik, ha a modell nem létező Strong-számot vagy igehelyet
  ad (a motor validálja, és kimondja); (e) melyik hozzáférési szinten érhető el. *(proveniencia: manual)*
* **N-F147b — hasonlóság-keresés a saját korpuszon (3. szint).** Beágyazás-alapú „hasonló szakaszok” a lexikonon és a
  tanulmányokon (nem a weben); a találat „hasonló, nem ellenőrzött” jelöléssel, a `jeloltek.tsv` logikája szerint jelöltként,
  soha nem leletként. Eldöntendő: (a) a 3. szabállyal (asszociatív anyag) hogyan fér össze a felületen — csak kutatói szinten,
  külön sávban?; (b) a beágyazás-modell és -index helye (építéskor, a `pardes.db`-be vagy mellé), licence és mérete; (c) a
  találat proveniencia-sora (`forras=beagyazas:<modell>`); (d) viszonya a bible-mcp `find_similar` / `semantic_search`
  eszközeihez (DT32: azok kimenete nem kerülhet adatba). *(proveniencia: manual)*
