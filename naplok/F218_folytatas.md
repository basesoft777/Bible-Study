# F218a — folytatási fájl

*Kézi munkanapló (a brief 9. pontja szerint minden commitban frissül). Ebből indul a következő session; a régi generátorból visszafejtett mondatszabályok is itt állnak.*

Ág: `claude/f218-generator-uj-a` · Brief: `F218_GENERATOR_UJ_A_BRIEF.md` · Alap: main `37f087cc`.

## Állás

| Tétel | Állapot | Megjegyzés |
|---|---|---|
| F218.0 | kész | modell-ellenőrzés, függések, keretmérés |
| F218.1 | kész, két halasztott résszel | referencia (bájtra azonos, 46,5 s), szimbólumtérkép, bemenet-hashek, alapmérés: `naplok/F218_jelentes.md`. **Halasztva:** a leltár `kovetelmeny` oszlopa (brief 7.4; a heti keret nullázása után, sonnet); a T3 oszlop és az alias-sorok (l. „Nyitott kérdések”) |
| F218.2 (T) | kész | típusok és szerződések; GK-01, 02, 05, 08a–c, 12, 23, 29, 30 zöld (69 teszt) |
| F218.3 | következik | tesztváz |
| F218.4 (S1) | nem indult | 2. Előfordulások + 2.1 |
| F218.5 (S2) | nem indult | 1. Döntési út + KIZARASOK |
| F218.6–F218.13 | nem indult | |

## Következő lépés

1. F218.3: `eszkozok/lapgen/tesztek/teszt_vaz.py` — a 7. pont még meg nem írt követelményei név + docstring + `skip` alakban; a HN-szövegminták.
2. F218.4 (S1): a „2. Előfordulások” és a „2.1” szakasz. A régi kód helye és az utófeldolgozó lánc: `naplok/F218_jelentes.md` „F218.1 — szimbólumtérkép” 2/a (i). A sorrend: bemeneti függvények (B03, B07, B08, B09, B10/B12/B13 kiejtés, B14, B16, B17–B21 a „Jelentés (a szó)” oszlophoz, B32–B34 UBS, B63 könyvrend, B01 licenc) → `szamitas/elofordulas.py` → sablonmondatok → `megjelenites/md/elofordulas.py` → `bekotes.py` → regresszió.

## Hogyan futtatható

- Tesztek: `python eszkozok/lapgen/tesztek/futtat.py` (minden), `… futtat.py szoveg szerkezet` (megnevezett fájlok).
- Új lap: `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon2 --id HAMART-001 --kimenet <repón kívüli könyvtár>`; a fájlok a `<kimenet>/lexikon/` alá kerülnek.
- Regresszió: `python eszkozok/lapgen/regresszio.py --id HAMART-001 --uj <kimenet>/lexikon --reszletes <fájl>`.
- Festékpróba: `python eszkozok/lapgen/festek.py --id HAMART-001 --id ISTENTISZT-001`.
- A régi generátor egyezése: `PARDES_DATUM=2026-11-13 python eszkozok/general.py --cel lexikon --id HAMART-001 --kimenet <ideiglenes>`, majd `cmp` a `git show HEAD:lexikon/HAMART-001_TUDOMANYOS.md` tartalmával (a munkafa CRLF-es, a blob LF-es).

## Tervezési döntések (F218.2)

- **Három konstruktor:** `proza(kezi)`, `sablon(sor, **p)`, `idezet(forrasszoveg)`. Az `idezet` egyetlen argumentumot kap: a forrást (B-azonosító) és a helyet maga a `Forrasszoveg` érték hordozza, így a kettő nem térhet el a szövegtől (a brief `idezet(forras, hely, szoveg)` alakjának szigorítása).
- **A `Lathato` nem `str`:** nincs rajta szövegművelet, `str()`/formázás kivételt dob; szöveggé csak a `kiiras()` alakítja, amelyet csak a `megjelenites/md/iro.py` hív (statikus teszt).
- **Burkolók a bemeneti rétegből:** `Kezi` → `proza`; `Forrasszoveg` → `idezet`; `Belso`, `Kulcs`, `Utvonal` → csak `Proveniencia` vagy (kulcsnál) névtábla. A burkolót csak a `bemenet/` hozhatja létre.
- **Nyilvános azonosító-típusok** (a brief felsorolásán túl): `Strong`, `MotivumId`, `Horgony` az `Igehely` mellett. Megjeleníthetők, mert szigorú alakjuk (regex) miatt szabad szöveget nem hordozhatnak. Sablonparaméter-típusok: `szam`, `tizedes(n)`, `nev(típus)`, `igehely`, `strong`, `motivum`, `horgony`, `datum`, `lathato`, `lista(elemtípus)`.
- **Sablonmondat:** `{nev}`; `{nev|a}` / `{nev|A}` határozott névelőt tesz elé (a/az; számnál a kiejtés szerint); listánál `{elemek|; }`, illetve `{elemek|, | és }`. A mondatban Markdown-jelölés állhat. A megjelenítő saját literálja csak szerkezeti jelölés (`Jel`, zárt készlet az író modulban).
- **Fajta-térkép:** az író minden kiírt sorhoz tartományokat ad (próza / sablon / idézet / megjegyzés / jelölés); ezt használja a festékpróba, és ezt fogja használni az alakosztály-kapu (GK-24).
- **Festés:** a burkoló `szoveg` alakja festett futásban jelzőszót hordoz (`ZZQ<B-azonosító>_<mező>ZZ`); az `ertek` (a számítás kulcsa) változatlan. Belső jelzőszó csak megjegyzésben állhat, kézi csak prózában, idézeté csak idézetben.
- **Blokkjelölő:** a lapon `general.py --cel lexikon#…` áll (a termék célneve), nem `lexikon2`.
- **Hash:** sorvég-normalizált tartalomból (`\r\n` → `\n`), a bemeneti rétegben és a regresszióban is; Windowson a munkafa CRLF-es.
- **`ts=`:** `PARDES_DATUM`-ból vagy a `--datum` paraméterből; nélkülük `ts=b:<12 jegy>` az olvasási napló hash-éből.
- **Jegyzék:** a sor a bemeneti függvénnyel együtt kerül a táblába (statikus teszt: sor ↔ `b<nn>_…` függvény, egy az egyhez). Több fájlos bemenetnél az `utvonal` `;`-vel sorol fel.
- **Regresszió:** szakasz = 2. szintű címsor; a diff soronkénti (`difflib`, azonos hosszú csereblokk soronként párosítva); az engedélyfájl `regi`/`uj` oszlopa `sor` kötésnél a sor sha256-ának első 16 jegye, `minta` kötésnél regex és csere. Részleges lapnál a még nem kész szakasz „nincs kész”, és az engedélysora nem számít.

## Nyitott kérdések

- **T3 (`sajat_szo` oszlop):** az `ellenoriz.py` 16. szabálya és a `betolt.py` pontos fejlécet vár az `elofordulasok.tsv`-n; új oszlophoz mindkettő módosítása kell (kívül esik a brief `ir` mezőjén). Kérdés elküldve az orkesztrátornak (2026-11-13); a válaszig az oszlop nem íródik. A további érintett fájlok listája: `naplok/F218_jelentes.md` 5/b.
- **Alias-sorok (GK-17, B63):** az F218.1 vizsgálata szerint a normalizáló tábla 4. oszlopát több eszköz olvassa (`normalizal.py`, `proza_allitas.py`, `sqlite_epit.py`, `thayer_api_koteg.py`, `olvasoi_utofeldolg.py`), új alias náluk viselkedést változtatna; a tábla ezért nem módosult. A két `KH_KONYV_JAVIT` sor (`Eféz`, `Siral`) az S5-nél (6. Kereszthivatkozások) kell; az `EXTRA_KONYV` kb. 45 eleme az utófeldolgozó csere része, amely az új generátorban megszűnik. Döntés az S5 előtt kell.
- **A CI nem futtatja a `lapgen/tesztek`-et:** a `.github/workflows/ellenorzes.yml` és a `push_elott.py` névvel sorolja a tesztfájlokat, mindkettő a brief `ir` mezőjén kívül esik. A 218a alatt a tesztek helyben futnak, minden commit előtt; a bekötés a 218c N-tételébe kerül.
- **Függések:** a `feladatok.py fuggesek` a 194 és a 212 tétellel is `KIZAR` sort ad (közös fájl), ezek a brief `nem_fugg` indoklásában nem szerepelnek (l. a jelentés F218.0 szakaszát).

## Megállási küszöb

A brief megállási szabálya: az építő session indulásakor mért maradék heti keret felének elfogyásáig az S1 szakasz-diffje legyen 0. Induló érték: heti 83% → a küszöb **91,5%** (heti, minden modell). Ha ezt eléri a keret, és az S1 diffje nem 0: megállás és jelzés.

## Mérőszámok

| Pont | Dátum (UTC) | Heti · minden modell | Heti · Fable | 5 órás | Megjegyzés |
|---|---|---|---|---|---|
| F218.0 (indulás) | 2026-11-13 09:05 | 83% | 15% | 19% | `get_usage`; nullázás: 2026-11-14 14:00 UTC |
| F218.2 után | 2026-11-13 09:35 | 85% | 20% | 38% | az F218.1 (sonnet) és az F218.2 együtt 2 százalékpont |

Diff-görbe (engedélyen kívüli diff-sorok szakaszonként, commitonként):

| Commit | 2. Előfordulások (437 sor) | Megjegyzés |
|---|---|---|
| F218.4 (1) | 76 | az összegző mondat, a hatókör-sor és a 2.1 pont (kb. 355 sor) bájtra egyezik; hátra van a tábla (51 sor), a 17 jegyzet, a közös forrásmegjelölés, az UBS-magyarázat és a blokkfejléc forráslistája |

Festékpróba (F218.4 (1)): HAMART-001 0 szivárgás (látott jelzőszavak: belső 5, idézet 58, kézi 98); ISTENTISZT-001 0 szivárgás (belső 5, idézet 22, kézi 40).

Az F218.1 alapmérés számai (a várt eltérés-osztályokhoz): `naplok/F218_jelentes.md` „F218.1 — alapmérés”. Kiemelve: T4 a HAMART-on 2 sor (1Móz 6:5 H7451, 1Móz 6:12 H7843); HN-15: 2; HN-03: 10; HN-01: 6 a 23 jegyzetből; N178: 0 érintett Strong; elavult fordítás: 5 sor (Thayer).

## Nyitott diff-sorok szakaszonként

Még nincs mérés.

## A régi generátorból visszafejtett szabályok

- A régi generátor a lapot nyers blokkokból építi, majd tíz utófeldolgozó lépésben írja át (címcsere → olvasói átírás → névelő-levétel → kiejtés-pótlás → Strong/BDB/könyvnév/idézőjel → lábjegyzet a tábla alá → közös forrásmegjelölés). A lánc és a 2. szakaszt érintő lépések táblája: `naplok/F218_jelentes.md` „F218.1 — szimbólumtérkép”.
- A tábla alatti jegyzet (`- <span class="lj-szam" id="j-2-5">2.5</span>…`) a régi `[^n]` lábjegyzetekből lesz: az azonos látható szövegű jegyzetek egy sorba vonódnak össze, és a sor végén minden eredeti lábjegyzet `<!-- eredeti: [^n]: … -->` megjegyzésként áll.

## Session-váltások, kompaktálások

- 1. session (2026-11-13): az indulás `claude-opus-5-5` modellen modell-eltérés miatt megállt; a felhasználó a sessiont `claude-fable-5-2`-re állította, a munka innen indul. Kompaktálás eddig: 0.
