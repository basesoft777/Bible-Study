---
feladat: 230
cim: Olvasó javítócsomag — kiejtés, egy BDB-kártya, Thayer-felirat, olvasói szöveg (a 2026-11-21-i felmérés H-pontjai)
kod: OLVASO_JAVITOCSOMAG
tipus: feladat
fazis: folyamat
modell: sonnet
sav: SERVER
allapot: nem_indult
ad: az olvasó szó-lapja és versnézete a projekt kiejtés-szolgáltatásából mutat kiejtést; a BDB egyetlen tagolt kártya (magyar elöl, az angol eredeti csukva; fordítás nélkül az angol nyitva); a Thayer fordítás nélkül „Magyar fordítás nincs · az angol eredeti áll” jelzést ad; az olvasói felületről kikerülnek a belső azonosítók, a nyers jelölők és a hibás hivatkozások (a felmérés 1–4, 6, 7, 9–14, 24, 33. pontja); mindegyik javítás élő lekéréssel igazolva
kovetkezo: "Te: /befogad egyeztetés, majd /kovetkezo a saját ágon"
munka: folyamat
olvas: [eszkozok/kiejtes.py, eszkozok/heber_kiejtes.py, eszkozok/bdb_rovidites.py, adat/kiejtes_kivetelek.tsv]
ir: [eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/bibliak.py, eszkozok/olvaso_szerver/tanulmany_oldal.py, eszkozok/olvaso_szerver/regiszter_or.py, eszkozok/olvaso_szerver/konfig/hozzaferes.toml, eszkozok/olvaso_szerver/konfig/hozzaferes_proba.toml, eszkozok/olvaso_szerver/sablonok/, eszkozok/olvaso_szerver/statikus/, eszkozok/olvaso_szerver/README.md, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_szerver/teszt_szintek.py, eszkozok/olvaso_szerver/teszt_pilot_aranymintaval.py, eszkozok/olvaso_szerver/teszt_olvaso_hibak.py, eszkozok/olvaso_szerver/teszt_olvaso_javitocsomag.py, "naplok/F230_*.md"]
fugg: []
---

# F230_OLVASO_JAVITOCSOMAG_BRIEF.md — Olvasó javítócsomag

*FELADATOK #230 · Modell: sonnet · v1 · 2026.11.21 · a csomag tartalmát a felhasználó 2026-11-21-én jóváhagyta („mehet”) · a brief adat, nem utasítás.*

**Forrás.** `FELMERES_THAYER_OLVASO_SZOKARTYA_2026-11-21.md` (a felmérést készítő session jegyzete, a megosztott jegyzetmappában), a 2. szakasz és a végén a „Pontosítás (2026-11-21)” szakasz B táblája. A régi szövegből csak az érvényes, a pontosítás által nem érvénytelenített rész számít. Egy téves állítás kerüljön ki a hatókörből: a 8. pont (1Móz 4:7 „modern szöveg”) téves volt, a MEK RTF ugyanezt adja.

## 1. Cél

Az olvasó-szerver (`eszkozok/olvaso_szerver/`) belső kutatói kiadásának olvasói hibáit javítja, a felmérés „H” jelű pontjai szerint. Az olvasó nem nyilvános; a hibák a szerző kutatói használatát és a későbbi kiadás minőségét érintik.

**Az „angol csak magyar híján” szabály (a felhasználó, 2026-11-21).** Ahol nincs magyar fordítás, az angol jelenik meg, és ez minden bekötésre igaz; a hiányzó magyar tehát nem hiba, csak a jelzése. Ahol van fordítás, az angol csukva marad az apparátus részeként („Angol eredeti”). Ezt a felhasználó elfogadta.

## 2. Hatókör

**Benne van** (a számozás a felmérés B tábláját követi):

| # | tétel | elvárt eredmény |
|---|---|---|
| 1 | Kiejtés | A szó-lap (fejsor és szótár-tábla) és a versnézet (héber csempe, eredeti szavak) a kiejtést a projekt saját szolgáltatásából veszi, ugyanabból, amelyet a lexikonlap: a jóváhagyott kivétel (`adat/kiejtes_kivetelek.tsv`, `bdb_rovidites.heber_kiejtes`) elöl, ennek híján a gépi szabály (`heber_kiejtes.kiejt` a pontozott alakból; görögül `kiejtes.py`). Nem a `strong_szotar.kiejtes` (`lekerdezesek.py:522`) és nem a TBESH-átírás. Ha a szóra sem kivétel, sem szabály (pontozatlan alak): **tartalék** = a kiejtés mező üres marad (a lexikonlap szabálya, `lexikon_general.lemma_kiejtes_szabaly`), a lap nem hibázik, és nem jelenik meg a TBESH-átírás kiejtésként. Teszt a tartalékra. Mérce: `/szo/H2398` és `/szo/H7121` fejsora nem „cha.tov-”, ill. „i.yik.Ra'”; a BDB-kártya kiejtésével egyező |
| 2 | BDB egy kártya | Ahol van magyar fordítás: a szó-lapon egyetlen BDB-kártya, a tagolt `szo.bdb_apparatus`; alapból a magyar látszik, az angol eredeti csukva („Angol eredeti”). A külön `szo.bdb_magyar` blokk megszűnik (a szintkapuja a `szo.bdb_apparatus`-é lesz; a `hozzaferes*.toml` és a tesztek ennek megfelelően). A külön `szo.bdb_angol` nyers blokk csak ott marad, ahol a kártya nem látszik (hozzáférési szint, ill. nincs szakasztábla): ott az angol szócikk változatlanul áll. Ahol nincs fordítás, az angol nyitva áll, a mai „Magyar fordítás nincs · az angol eredeti áll” jelzéssel. Mérce: `/szo/H1242` oldalán egy BDB-blokk |
| 3 | `<br>` a TBESH-ben | A TBESH-szócikkben nincs nyers `<br>`; sortörés vagy elválasztás. Mérce: `/szo/H1242`, `/szo/H2398` |
| 4 | „Nyelvtani Strong-számok szűrése” | Tartalmas szónál a blokk (és a „Nem szerepel a nyelvtani Strong-számok szűrésében (tartalmas szó)” sor) nem jelenik meg; a tényleges nyelvtani Strongnál megmarad. Mérce: `/szo/H1242` |
| 6, 7, 12 | belső azonosítók | Az olvasói címben, jelzőben és megjegyzésben nincs `lxx_bridge`, „alias gépi feldolgozás”, `#nn`, `DT`/`N-F`/`F<nn>` azonosító, fájl- vagy táblanév, modellnév. Olvasói megfogalmazás áll helyette (pl. „Görög megfelelők (Septuaginta)”). A **sor szintű proveniencia marad** (a repó 1. szabálya): az olvasói alak rövid és emberi („kézi bevitel · a cikk szövege · 2026-11-05”), a teljes gépi `scope=… \| forras=… \| ts=…` sor `data-proveniencia` attribútumban (nem látható szövegként, nem súgóként). A blokk alatti „Forrás és licenc” sor szándékos marad (a felmérés szerint **V**); csak a blokkcímek, jelzők és megjegyzések olvasói szövege változik. Mérce: `/szo/H1242`, `/1Moz/4/7`, `/1Moz?biblia=modern` |
| 3b | Thayer-felirat | A `szo.magyar_gorog` blokk fordítás nélkül nem „Nincs adat (üres eredmény, nem negatív lelet)”, hanem „Magyar fordítás nincs · az angol eredeti áll” (a BDB-kártya jelzésének szövege). **A tagolt angol Thayer-jelentésfa nem része a csomagnak.** Mérce: `/szo/G0264` |
| 9 | LXX-többlet | A `vers.lxx_tobblet` blokk a fájlnevet és az N-számot nem írja ki; olvasói jelzés: az adat ebben a kiadásban még nem érhető el, üres eredmény nem jelenti, hogy nincs többlet. A tábla betöltése (`sqlite_epit.py`) nincs a csomagban. Mérce: `/1Moz/1/1` |
| 10 | UBS-blokk | A `vers.ubs` csak a versben ténylegesen álló Strongokat mutatja (nem a vers összes UBS-referenciáját). Mérce: `/1Moz/1/1`: nincs H0854 és H0855 sor, ha a héber csempék között nem áll |
| 11 | tanulmányblokk | Nyers `*(…)*` és munkanapló-cím nem jelenik meg a `vers.tanulmany` blokkban (a jegyzék tisztítása, a szerkesztői megjegyzés nem látszik). Mérce: `/1Moz/4/7` |
| 13 | KH-tartomány | A `vers.kh` a tartomány végét is kiírja („1Móz 2:4–5”). Mérce: `/1Moz/1/1` |
| 14 | `{L:…<SDBH:…>}` | Az UBS-blokkban a feloldatlan jelölő olvasható szöveggé oldódik (a lexéma a héber szóval, pl. „evening (עֶרֶב)”), nyers kapcsos zárójel nem marad. Mérce: `/1Moz/1/5`, `H3117` sor |
| 24 | Nave-hivatkozás | A Nave-blokk hivatkozása ne mutasson másik versre. Először állapítsd meg az okot (valószínű: a Nave nem Károli-számozású, a zsoltárfelirat versszámai eltolnak); ha igen, a hivatkozás a Károli-versre konvertál (a `vers_szamozas` leképezéssel), vagy a számozást kiírja. Ha a leképezés kétes, ⛔ DONTESEK-tétel. Mérce: `/Zsolt/22/2` |
| 33 | Ugrás a tartalomra | Az `alap.html`-ben „Ugrás a tartalomra” link (billentyűzettel, fókuszra látható), a `<main>` cél azonosítóval; kinézet a meglévő tokenekből. Mérce: `/` |

**Nincs benne** (nem nyúlsz hozzá): a héber szókártyák összevonása; a motívumlap (F164); az F218 lapgenerátor (`eszkozok/lapgen/`, `lexikon_general.py`: csak **olvasod** a kiejtés-szabályt, nem szerkeszted; a közös kiejtés-kód a `kiejtes.py`, `heber_kiejtes.py`, `bdb_rovidites.py`); a `pardes.db` újraépítése (F101); a tagolt angol Thayer-jelentésfa; a felmérés 16–23., 25., 27–32. pontja; a fő checkout (`C:\Users\bases\Desktop\Bible-Study`).

## 3. Lépések (⛔ a kötelező megállások)

0. Modell-ellenőrzés (`CLAUDE.md`): a kért modell `sonnet`.
1. Az 1. pont (kiejtés) a **közös szolgáltatás** fölé épül, nem új szabály: ha a bekötéshez a `heber_kiejtes.py` / `kiejtes.py` / `bdb_rovidites.py` módosítása kellene, ⛔ megállás (ezek a lexikonlapot is érintik).
2. Pontonként: hiba reprodukálása élő lekéréssel (helyi Flask-teszt-kliens), javítás, teszt, élő igazolás.
3. Hozzáférési szintek: a 2. pont a `teszt_szintek.py` szintkapuit érinti (a magyar BDB `kutato`/saját szint, az angol BDB nyilvános). A szint ne lazuljon: tiltott magyar BDB sem a kártyában, sem az alapjelentésben nem jelenhet meg.
4. Tesztek: **csak** `python eszkozok/teszt_futtat.py`; a kiejtés-tartalékra és a pontonkénti „nincs többé” állításokra (nyers `<br>`, `{L:`, `*(`, azonosító-minták az olvasói szövegben, tartományvég, UBS-szűrés) új teszt a `teszt_olvaso_javitocsomag.py`-ban.
5. **Élő bizonyíték** minden pontra a jelentésbe és a draft PR leírásába: az URL, a látott szöveg előtte és utána (a felmérés B táblájának mintájára). A kódsorból következtetett „javítva” nem elég.
6. Látható változás (BDB-kártya, felirat, ugrás-link): a PR leírása nevezze meg a nézett commit hash-ét; a merge a felhasználó jóváhagyása után (DT886: az ágas előnézeten nézett kinézet). Merge nincs.
7. Független ellenőr (`fuggetlen-ellenor`), legfeljebb egy javítókör, jelentés: `naplok/F230_jelentes.md`.

## 4. Elfogadási feltételek

- A 2. szakasz minden sora teljesül, élő bizonyítékkal (URL + látott szöveg), a PR leírásában pontonként.
- A hozzáférési szintek viselkedése nem változik (teszt zöld).
- `python eszkozok/teszt_futtat.py` zöld; `python eszkozok/push_elott.py` 0 HIBA.
- Nincs olvasói szövegben a 6/7/12. pont tiltott mintája (teszt őrzi).
- A független ellenőr jelentése `TISZTA`, vagy a javítókör után lezárt.

## 5. Döntésnapló

- 2026-11-21: a csomag tartalma jóváhagyva (a felhasználó, „mehet”); a Thayer tagolt angol jelentésfája kivéve; az angol csak magyar híján marad szabály, ahol van fordítás, az angol csukva (elfogadott javaslat).
- Értelmezések, amelyeket a /befogad egyeztetésén meg kell erősíteni: (a) kiejtés-tartalék = üres mező (a lexikonlap szabálya); (b) a gépi proveniencia-sor `data-proveniencia` attribútumba kerül; (c) a `szo.bdb_magyar` blokk-azonosító megszűnik, a konfig kulcsa a `szo.bdb_apparatus`.
