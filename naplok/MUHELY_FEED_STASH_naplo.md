# MUHELY_FEED_STASH_naplo.md — F156 (FELADATOK #156)

*Modell-ellenőrzés: kért `sonnet`, tényleges `claude-sonnet-5-5` — egyezik. Futás: 2026-11-01, alap-commit `3a2dbd51`.*

## M0 — a „kész”-kritérium az ISTENTISZT-001 aranymintán

Minden mérő csak olvasva futott; a nulla-diff próba repón kívüli ideiglenes könyvtárba generált. Eredmény pontonként:

| # | kapu | állapot | érték | mérő (proveniencia) |
|---|---|---|---|---|
| 1 | `ellenoriz.py` 1–21: 0 HIBA | **zöld** | 18 RENDBEN, 0 SÉRTÉS; JELENTÉS/KÉZI látszik (nem blokkol) | `scope=motivum:ISTENTISZT-001 \| forras=ellenoriz.py \| ts=2026-11-01` |
| 2 | `futtat.py` E2–E29: 0 hiba a motívum fájljain | **zöld** | 0 HIBA, 500 jelentés (E12 348, E13 107, E27 41, E25 4) | `forras=ellenorzes/futtat.py --valtozott motivumok/ISTENTISZT-001.md lexikon/ISTENTISZT-001_TUDOMANYOS.md` |
| 3 | egyforrású, nulla-diff | **zöld** | `motivumok/ISTENTISZT-001.md` megvan; `general.py --cel lexikon --id ISTENTISZT-001` a lap `ts=` dátumával (`PARDES_DATUM=2026-10-29`) bájtra egyezik (CR-normalizálva) | `forras=general.py (nulla-diff)` |
| 4 | nincs `dontes=nyitva` jelölt | **piros** | 6 nyitva: Ézs 41:25 (F110 szűrő, B osztály) és 5 motívumközi sor (Zsolt 116:4, 1Móz 4:26, Róm 10:12–14; DT280) | `forras=jeloltek.tsv` |
| 5 | `motivum_hatar`: 0 nyitott kérdés | **piros** | gépi rész 0, modelles rész 5 kérdés (K1–K5, `naplok/HATAR_ISTENTISZT-001.md`) | `forras=motivum_hatar.py` |
| 6 | olvasói blokk 100%, kiejtés-hiány 0, „(fordításra vár)” 0 | **piros** | blokk 98/98 fedett (51 bevezetővel, 0 HIÁNY), fordításra vár 0, **kiejtés-hiány 3** (a Jelmagyarázat `י׳`, `ק׳`, `שׁ׳` jelei, generált rész, jóváhagyott héber alak nélkül) | `forras=OLVASOI_blokk_teljesseg_meres.py + kiejtes_szoveg.py` |
| 7 | 0 nyitott lektori kérdés | **nincs mérő** | a lektor-felület tárolója (`naplok/LEKTOR_<ID>.tsv`) nem létezik (DT-F156c) | — |
| 8 | nincs nyitott 🟡 DT / ⛔ feladat | **piros** | 4 megállt feladat (#121, #131, #146, #152) és hozzájuk 🟡 DT-k | `forras=feladatok.py + DONTESEK.md` |

**Összesítés: 3/8 zöld.** Az ISTENTISZT-001 a kritérium szerint **nem kész**, noha a `motivumok.tsv` `statusz`-a `publikálható` (v3).

### Mérés közben megállapított tények

- **Az `ellenoriz.py` kimenetéből a motívumonkénti bontás csak részben vezethető le:** a szakaszok verdiktje globális, motívum csak a 8/c, 18, 19 szakasz soraiban szerepel névvel. Ezért a kapu így számol: SÉRTÉS-szakasz, amely a motívum nevét tartalmazza → piros; SÉRTÉS-szakasz, amelyben egyetlen motívum sem szerepel → minden motívum piros (globális). Ma 0 SÉRTÉS van, tehát minden motívum zöld.
- **A `futtat.py --valtozott` motívumonként levezethető** (a motívum fájljain), 1–4 perc motívumonként; a teljes futás ~20 perc.
- **A 3. kapu nulla-diffje** csak úgy egyezik, ha a generálás a lapban álló `ts=` dátumot kapja (`PARDES_DATUM`); különben a 19 GENERÁLT-KEZDET sor `ts` mezője tér el.
- **A 8. kapu a briefek `ir` mezőjéből köti a feladatot a motívumhoz** (az `ir` tartalmazza a motívum azonosítóját). Az ISTENTISZT-001-re ez 11 feladat, ebből 4 `megallt`. Kérdés a felhasználónak, hogy a „megállt” állapot mindig ⛔-nak számít-e (DT-F156b (c)).

## Teendő-lehetőségek az ISTENTISZT-001-en (⛔ DT-F156b)

Nem zöld: 4., 5., 6., 8. kapu; a 7. nincs mérő. A kapuk kétféleképpen rendezhetők: a lap vagy a forrás javul (kiejtés-jelek, a határ K1–K5 megválaszolása, a megállt feladatok #152/#131/#146/#121), vagy a kritérium pontosodik:

- **4. kapu:** a motívumközi (F127 B2, DT280) nyitva sorok is blokkolnak-e, vagy csak a saját motívum jelöltjei?
- **5. kapu:** a „modelles rész” kérdései mikor számítanak lezártnak (nincs jelölő a megválaszoltságra)?
- **6. kapu:** a Jelmagyarázat gépi jelei (`י׳` stb.) kiejtés-kötelesek-e.
- **8. kapu:** a `megallt` feladat és a 🟡 DT mindig blokkoló-e, vagy csak a motívum tartalmát érintő?

## Futás minden motívumon (lépés 2)

9 motívum, **0 kész (8/8)**, 19/72 zöld kapu. A `motivumok.tsv` 8 motívumot `publikálható`-nak jelöl, a kritérium szerint egy sem kész: az **eltérés-lista** mind a 8 `publikálható` motívumra (KIRALY-001, ISTENTISZT-001, TEREMT-001, ALVIL-001, MENNY-001, ANTROP-001, HODIT-001, HAMART-001); a TEREMT-002 `feldolgozás alatt` (4/8).

| motívum | zöld | zöld kapuk |
|---|---|---|
| KIRALY-001 | 1/8 | 1 |
| ISTENTISZT-001 | 3/8 | 1, 2, 3 |
| TEREMT-001 | 2/8 | 1, 4 |
| ALVIL-001 | 4/8 | 1, 2, 3, 4 |
| MENNY-001 | 1/8 | 1 |
| ANTROP-001 | 1/8 | 1 |
| HODIT-001 | 1/8 | 1 |
| HAMART-001 | 2/8 | 1, 5 |
| TEREMT-002 | 4/8 | 1, 2, 4, 8 |

Megjegyzések:

- **3. kapu:** csak az ISTENTISZT-001 és az ALVIL-001 nulla-diffes. A többi publikálható motívumnál az újragenerálás 994–3628 sorban tér el a committolt laptól (migrációra vár, #123), a TEREMT-002-nek nincs lexikon-lapja.
- **2. kapu:** a régi motívumoknál 1–17 HIBA áll (a `--valtozott` mód diff nélkül a motívum fájljainak minden találatát HIBA-ként számolja); az ISTENTISZT-001, az ALVIL-001 és a TEREMT-002 0 HIBA.
- **5. kapu:** „nincs mérő” a `naplok/HATAR_<ID>.md` nélküli motívumokon (csak az ISTENTISZT-001 és a HAMART-001 van meg).

## A két réteg átnézése (⛔)

- A nyilvános JSON fehérlistás: csak `id`, cím, téma, PaRDeS-szint, állásfokozat, kapuk (sorszám, név, állapot), számlálók, a Stash-mezők. **Nem kerül bele:** jelölt-indoklás, a határ-kérdések szövege, a DT-k kérdésszövege, a hibaszövegek, a PR-ok, a negatív kritérium és a fölérendelt fogalom (utóbbi kettő a brief 3.4 szerint a Stash-leírás része, de adattábla-tartalom; **DT-F156e** kérdés: bekerüljön-e a nyilvános Stash-be). A belső réteg a jelölteket és a határ-kérdéseket csak jelölővel/igehellyel hivatkozza (szöveg nélkül).
- A teszt (`eszkozok/teszt_muhely_allapot.py`) ellenőrzi a fehérlistát és azt, hogy hiányzó mérő nem zöld.

## Frissítés menete

```bash
python eszkozok/muhely_allapot.py            # ~20 perc; --motivum ID ... szűkít, --nincs-gh kihagyja a PR-lekérést
python eszkozok/teszt_muhely_allapot.py
```

A kimenet a `generalt/muhely/` (három JSON, GENERÁLT fejléccel); a Dashboard-artifact a nyilvános JSON-ból levezetett táblákat tölti (frissítést egy session végez kérésre).

## Dashboard

A Dashboard-artifact privát; hivatkozása a PR leírásában és a jelentésben áll. A belső fül **hibaszövegeket** tartalmaz: a hivatkozást megosztani csak a belső fül nélküli változat publikálása után szabad.

## Olvasói megfogalmazás a nyilvános rétegben (⛔ DT-F156f — jóváhagyásra vár)

*Az orkesztrátor kérése nyomán (a felhasználó: a Feed üzenetei az olvasónak értelmezhetetlenek). Ez a tábla **javaslat**: a generátor és a Dashboard addig nem változik. A nyilvános rétegben nem szerepel belső szó (gerinc, eszköz- és szabálynév, DT-szám, `nincs_mero`); a belső réteg megtartja a technikai nevet az olvasói szöveg mellett. Az `N` a mérőből jövő szám.*

### A nyolc kapu

| # | belső név | olvasói név | zöld | piros | nincs mérő |
|---|---|---|---|---|---|
| 1 | `ellenoriz.py` 1–21 | Az adatok összhangja | Az adattáblák egymásnak megfelelnek, ellentmondás nincs. | Az adatokban ellentmondás van, javítás alatt. | Az adatellenőrzés még nem futott. |
| 2 | CI E2–E29 | A szövegek ellenőrzése | A lap szövegei hibátlanul átmentek az ellenőrzésen. | Az ellenőrzés N hibát talált a szövegekben. | Az ellenőrzés még nem futott. |
| 3 | egyforrású, nulla-diff | Egy szerkesztett forrásból épül | A lap egyetlen szerkesztett forrásból készül, és újraépítve ugyanaz. | A lap még átállításra vár az új szerkesztési rendre. | A lap még nincs egy forrásba rendezve. |
| 4 | `dontes=nyitva` jelölt | Eldöntendő igehelyek | Minden vizsgált igehelyről döntöttünk. | N igehely vizsgálata folyamatban van. | – |
| 5 | `motivum_hatar` | A motívum határa | A motívum határáról szóló kérdések megválaszoltak. | N kérdés van nyitva arról, mi tartozik a motívumhoz. | A határ vizsgálata még nem készült el. |
| 6 | olvasói blokk, kiejtés, fordítás | Olvasható lap | A lap minden része magyarázattal, kiejtéssel és fordítással áll. | A lapon N kiejtés hiányzik, M rész fordításra vár. | – |
| 7 | lektori kérdések | Lektori átolvasás | A lektor minden kérdése lezárult. | N lektori kérdés vár válaszra. | A lektori átolvasás még nem indult el. |
| 8 | nyitott DT / ⛔ feladat | Függő munka | Nincs a motívumot érintő megoldatlan kérdés vagy megállt munka. | N kapcsolódó munka vagy kérdés vár megoldásra. | – |

### Az állapotok (a kapu jelzése)

| belső | olvasói szöveg |
|---|---|
| `zold` | rendben |
| `piros` | munka van hátra |
| `nincs_mero` | még nem vizsgáltuk |
| `hiba` | az ellenőrzés nem futott le, újra próbáljuk |

### Az állásfokozatok

| belső | olvasói szöveg |
|---|---|
| jelölt | Felmerült: igehelyeket gyűjtünk hozzá |
| feldolgozás | Feldolgozás alatt |
| ellenőrzés | Ellenőrzés alatt: a lap megvan, a kapuk egy része még nem teljesül |
| lezárt (stash) | Kész, megjelenésre vár |
| kötetben | Megjelent a kötetben |
| `kotet: null` („nincs kötet-adat”) | Kötetbe még nincs beosztva |

### A heti történés

| belső esemény | olvasói szöveg |
|---|---|
| `jelölt-döntés: beépítve` | N igehely bekerült a motívumba |
| `jelölt-döntés: elutasítva` | N igehelyet kizártunk, mert nem illik a motívum határába |
| `állapot: publikálható (v3)` | A motívum lapja új változatot kapott (3. változat) |

### A motívumonkénti mondat

Minta: `N_előfordulás igehely feldolgozva, M vizsgálat alatt, K kizárva; a nyolc ellenőrzési lépésből Z teljesül.` Ha M = 0: „…, nincs vizsgálat alatt álló igehely, …”; ha K = 0, a „kizárva” tag elmarad. Az előfordulás-szám az `elofordulasok.tsv` sorai (ÓSZ+ÚSZ), M a nyitott jelöltek, K az elutasítottak.

| motívum | mondat a mai adatból |
|---|---|
| KIRALY-001 | 9 igehely feldolgozva, 1 vizsgálat alatt, 13 kizárva; a nyolc ellenőrzési lépésből 1 teljesül. |
| ISTENTISZT-001 | 35 igehely feldolgozva, 6 vizsgálat alatt, 92 kizárva; a nyolc ellenőrzési lépésből 3 teljesül. |
| TEREMT-001 | 42 igehely feldolgozva, nincs vizsgálat alatt álló igehely, 2 kizárva; a nyolc ellenőrzési lépésből 2 teljesül. |
| ALVIL-001 | 72 igehely feldolgozva, nincs vizsgálat alatt álló igehely, 5 kizárva; a nyolc ellenőrzési lépésből 4 teljesül. |
| MENNY-001 | 9 igehely feldolgozva, 2 vizsgálat alatt, 1 kizárva; a nyolc ellenőrzési lépésből 1 teljesül. |
| ANTROP-001 | 8 igehely feldolgozva, 3 vizsgálat alatt; a nyolc ellenőrzési lépésből 1 teljesül. |
| HODIT-001 | 33 igehely feldolgozva, 14 vizsgálat alatt, 4 kizárva; a nyolc ellenőrzési lépésből 1 teljesül. |
| HAMART-001 | 52 igehely feldolgozva, 8 vizsgálat alatt, 163 kizárva; a nyolc ellenőrzési lépésből 2 teljesül. |
| TEREMT-002 | 3 igehely feldolgozva, nincs vizsgálat alatt álló igehely, 63 kizárva; a nyolc ellenőrzési lépésből 4 teljesül. |

*Megjegyzés a számokhoz: a „feldolgozva” szám itt a beépített jelöltek száma (az `elofordulasok.tsv` sorainál a motívumközi sorok miatt kettővel kevesebb lehet, pl. ISTENTISZT-001: 35 beépített, 33 előfordulás-sor); a jóváhagyáskor kell eldönteni, melyik szám kerüljön az olvasói mondatba. A táblában a beépített jelöltek száma áll.*

### DT-F156f ✅ eldöntve

A felhasználó jóváhagyta (az orkesztrátor továbbításában, 2026-11-01): **„Igen, így”** — a „Jóváhagyod a Feed olvasói szövegeit, az előfordulások számával a mondatban?” kérdésre. A jóváhagyott változat e tábla két módosítással: (1) az 1. kapu olvasói neve „Az adatok összhangja”; (2) a 3. kapu piros szövege „A lap még átállításra vár az új szerkesztési rendre.” (a sorszám a belső rétegben marad). A „feldolgozva” szám az **előfordulás-sorok száma** (`elofordulasok.tsv`), nem a beépített jelölteké; a fenti mintamondatok ezért a jóváhagyás előtti (beépített-számú) szövegek, a valós mondat a `feed_nyilvanos.json` `olvasoi_mondat` mezőjében áll. Beírva a generátorba (F156.4): a nyilvános réteg kapuinál `olvasoi_nev`, `olvasoi_allapot`, `olvasoi_szoveg`, `szin` (a gépi állapotkód és a belső kapunév nem megy át); a motívumnál `olvasoi_mondat` és olvasói állásfokozat; a heti történésnél `olvasoi_esemeny`; a Stash-nél `kotet_olvasoi`. A #559 (ISTENTISZT-001: 22 előfordulás) merge-e után a számok változnak: a kimenetet újra kell futtatni.

## Arculat (DT-F156g ✅ eldöntve)

A felhasználó kérése: „kapjon modernebb színvilágot és tipót”. Három változat készült próba-artifactként (A. Olvasó, B. Termék, C. Műhely; tokenek: a megosztott jegyzetmappa `KOZOS_TOKENEK.md`), a felhasználó választása (az orkesztrátor továbbításában): **az A változat** („a”) — Source Serif 4 (cím) + IBM Plex Sans (szöveg) + IBM Plex Mono (adat), hűvös papír, mély kék kiemelés, világos és sötét mód. A #157 lektor-felület ugyanezeket a tokeneket használja (`--papir`, `--lap`, `--tinta`, `--halvany`, `--vonal`, `--kiemel(-hatter)`, `--elfogad(-hatter)`, `--elvet(-hatter)`, `--figyel(-hatter)`). A Dashboardra alkalmazva az olvasói szövegek beépítése után (F156.5).

## Frissített állapot (2026-11-02, a #559 és a lektori tároló után)

Az 5. és a 7. kapu a `naplok/LEKTOR_<ID>.tsv`-ből számol (megválaszolt = zárt; a határ modelles K-kérdései, amelyek ott megválaszoltak, nem nyitottak — ez a DT-F156b határ-kérdését érinti: az ISTENTISZT-001 5. kapuja zöld). **ISTENTISZT-001: 5/8 zöld** (szabályok, CI, egyforrású, határ, lektor); piros: eldöntendő igehelyek (4), olvasható lap (3 kiejtés-hiány), függő munka (9). 9 motívumból továbbra is 0 kész. Az olvasói mondat: „22 igehely feldolgozva, 4 vizsgálat alatt, 105 kizárva; a nyolc ellenőrzési lépésből 5 teljesül.” A korábbi M0-tábla a 2026-11-01-i állapotot mutatja.

## Dashboard-arculat (A. Olvasó, a Dashboard-típuson belül)

A betűk (Source Serif 4, IBM Plex Sans, IBM Plex Mono; OFL, a `eszkozok/olvaso_szerver/statikus/fonts/` fájljaiból, latin + latin-ext) a Dashboard `files/*.css` dokumentumaiban `data:` URL-lel állnak, az oldal saját osztályain az A-tokenek (világos/sötét), a háttér az A „papír”; a típus kerete a típusé. A `dash/look` az A-értékeket tartalékként hordozza. A privát oldalt renderelni nem tudtam (bejelentkezés kell), a típus `check` dokumentuma csak megnyitás után jön létre.

## A Dashboard forrása a repóban (újraépíthetőség)

A Dashboard (`https://claude.ai/artifact/S5LqyrUsFN8RXHXLrURnpk`) oldala nem generálódik, kézzel írt: a forrás az `eszkozok/muhely_felulet/` alatt van (a `generalt/` a kimenet rétege, kézzel írt fájl nem kerül oda; README-vel), hogy a következő frissítés ne írja felül a javításokat.

- `index.html`: az oldal (`files/index.html` a Dashboardban); a téma a `data-mode` ősből olvasódik (`.sotet` osztály), az A-tokenek saját osztályokon.
- `look.json`: a `dash/look` (az A értékei tartalékként).
- `adat_laposit.py`: a `feed_*.json`-ból a Dashboard öt adatfájlja (motivumok, kapuk, stash, tortenes, belso_kapuk).
- `betu_css.py`: az öt betű-CSS (`files/*.css`, data: URL) az olvasó-szerver OFL betűfájljaiból.

Frissítés: `muhely_allapot.py` → `adat_laposit.py <könyvtár>` → a fájlok feltöltése az artifact asset-tárába → a `datasets/*` dokumentumok `source.url`-jének cseréje; az oldal vagy a betű-CSS változásakor a `files/` dokumentumok írása (`{"text": …}`).

## DT-F156h ✅ eldöntve — a Feed mindig világos

A felhasználó (az orkesztrátor továbbításában, 2026-11-02): **„Igen, mindig világos”** — a Feed a témától függetlenül mindig az A világos változatát mutatja (papír `#f6f6f3`, lap `#ffffff`, kiemelés `#1f5f7a`), sötét módban is. A sötét A-készlet és a `.sotet` kapcsolás kikerült az `eszkozok/muhely_felulet/index.html`-ből (a DT-F156g téma-olvasása megszűnt); az `.mh` `color-scheme: light`. A `dash/look` sötét halmaza a típus kereténél marad.

## DT-F156b ✅ eldöntve — a kritérium pontosítása az ISTENTISZT-001 M0 után

A felhasználó (az orkesztrátor javaslataira, 2026-11-02): **„Igen, mind”**, három pontban. Alkalmazva a `muhely_allapot.py`-ban (teszttel):

- **(a) 4. kapu:** a motívumközi jelölt (`jelolt_tipus=motivumkozi`) nyitva maradhat, nem blokkol (tájékoztatásként látszik a belső rétegben); csak a motívum saját előfordulás-jelöltje blokkol. A motívumonkénti „vizsgálat alatt” szám is csak a blokkolókat számolja.
- **(b) 6. kapu:** a generált Jelmagyarázat szótári rövidítései (pl. `י׳`, `ק׳`, `שׁ׳`) nem kiejtés-kötelesek; a mérés a Jelmagyarázat szakaszt kihagyja, a prózában álló héber/görög szavak kötelesek maradnak.
- **(c) 8. kapu:** csak az a megállt vagy döntésre váró feladat blokkol, amelynek `ir` listájában a motívum valamelyik fájlja áll (`motivumok/<ID>.md`, `lexikon/<ID>_…`, `motivumlog/<ID>…`), ÉS a briefjének valamelyik ⛔ pontja a motívumról szól; a többi tájékoztatásként látszik. A DT-F156e (a negatív kritérium a nyilvános Stash-ben) halasztva marad.

## A 7. kapu és a következő kiadás (2026-11-02)

A felhasználó: az ISTENTISZT-001 „ettől független lezárható / a lektori átnézés eredménye egy új kiadás”. A `/kiadas` lektori kérdései (`forras=lektor`) ezért a következő kiadáshoz tartoznak: a 7. kapu nem számolja őket blokkolónak, a Feed „2. kiadáshoz: N kérdés” jelöléssel mutatja (belső és nyilvános rétegben is, a kapu olvasói szövegében). A határ- és lefedettségi kérdések (`forras=hatar`, `proza_lefedettseg`) blokkolók maradnak. A #561 merge-e után a DT-F156b alkalmazása (F156.10) ide, erre az ágra került át.

## DT-F156i ✅ eldöntve — a `/kiadas` kimenetéből jövő kérdések a 2. kiadáshoz tartoznak

A felhasználó (az orkesztrátor továbbításában, 2026-11-02): **„Igen, mindkettő”** — a két lefedettségi kérdés (Ézs 41:25, közben elutasítva; 1Móz 4:26 → Sof 3:9, a lezárásnál a 2. kiadásba sorolva) is a 2. kiadáshoz tartozik. Általános szabály: a `/kiadas` kimenetéből jövő kérdések (`forras=lektor` és `forras=proza_lefedettseg`) a következő kiadás bemenetei, a 7. kaput nem blokkolják, „2. kiadáshoz: N kérdés”-ként látszanak; a határ-kérdések (`forras=hatar`) blokkolók maradnak. Alkalmazva a `masodik_kiadas`-ban, teszttel.

## DT-F156j ✅ eldöntve — olvasói előnézet, a nyilvános réteg csak előrehaladást mutat

A felhasználó (az orkesztrátor továbbításában, 2026-11-02): önálló olvasói előnézet a Feedből és a Stash-ből („a feed / stash olvasó előnézet”), és a feltétele: **„ott nem kell látszani hogy megakadt valami”**. (Ugyanekkor visszavonta a kiadás szerinti bontást a Feedből: az a lektori felületre való; a Dashboardból és a generátorból kivettem.)

- **Nyilvános réteg (JSON, Dashboard „nyilvános” fül, előnézet): csak előrehaladás.** Állapotlánc (melyik fokon áll: kész / aktuális / következő), feldolgozott igehelyek, a teljesült lépések (csak a teljesültek, név szerint), heti történés (új igehely, új változat, kizárt igehely „indoklással”), a Stash leírása és statja. **Nem szerepel:** piros kapu, „munka van hátra”, „nincs mérő”, megállt/függő feladat, hibaszám, nyitott jelölt vagy döntés, „vizsgálat alatt”, a lektori kérdések száma. A zöld lépések szövege is akadályt nem említő szóval készült.
- **Belső réteg és Dashboard belső füle:** minden kapu, a „Mi van hátra”, a hibaszövegek, a proveniencia.
- **Teszt:** a nyilvános kimenet fehérlistás, csak teljesült lépést hordoz, és egyetlen szövege sem tartalmaz akadályt, hibát vagy nyitott munkát jelző szót (`TILTOTT_SZAVAK`).
- **Előnézet:** `eszkozok/muhely_felulet/olvaso_elonezet.py` → sima HTML-artifact, A. Olvasó arculat, mindig világos, a generált JSON-ból.

## DT-F156e ✅ eldöntve — a nyilvános Stash-leírásban a negatív kritérium és a fölérendelt fogalom

A felhasználó (az orkesztrátor továbbításában, 2026-11-02): **„Igen, mindkettő”** — a nyilvános Stash leírásában szerepel a motívum negatív kritériuma és fölérendelt fogalma (a `motivumok.tsv`-ből, ahogy a jóváhagyott terv eredetileg is a Stash leírásába sorolta). A prémium tartalom (lapszöveg, adattáblák) továbbra sem nyilvános. A `FEHERLISTA_STASH` bővült a `negativ_kriterium` és `folerendelt_fogalom` mezővel (csak a kész, 8/8 motívumoknál jelennek meg), teszttel; az olvasói előnézet a Stash-t kártyákon mutatja („Ide nem tartozik”), a Dashboard Stash-táblája két új oszloppal.
