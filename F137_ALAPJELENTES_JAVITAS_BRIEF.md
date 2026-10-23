---
feladat: 137
cim: A szó-lap alapjelentésének javítása — a „LORD” hiba a forrásban, a visszaesési sorrend, a BDB-kinyerő a sikertelen sorokra, aranymintával
kod: ALAPJELENTES_JAVITAS
tipus: feladat
fazis: 1
modell: opus
allapot: nem_indult
ad: a szó-lap alapjelentése magyar vagy forrásjelölt Károli-alak minden olyan Strong-számnál, ahol ma az angol Strong-szótár (benne a hibás „LORD”) áll; a TAHOT_kivonat és a Strong_szotar istenneves sorai a glosszát hordozzák; a mai 638 jó alapjelentés változatlan
kovetkezo: "A /kovetkezo a #134 zárása után indíthatja (M0 ⛔: terv)"
munka: adat
olvas: [konkordancia/_nyers/tbesh/TBESH_konszolidalt.tsv, konkordancia/TIPNR_kivonat.tsv, adat/forditasok.tsv]
ir: [konkordancia/TAHOT_kivonat.tsv, konkordancia/Strong_szotar.tsv, konkordancia/TAHOT_TAGNT_README.md, eszkozok/alapjelentes_istennev_javit.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/bdb_szelet.py, eszkozok/olvaso_szerver/teszt_alapjelentes.py, eszkozok/olvaso_szerver/teszt_alapjelentes_arany.tsv, adat/alapjelentes_kezi.tsv]
fugg: [134]
nem_fugg: [27]
---

# F137_ALAPJELENTES_JAVITAS_BRIEF.md — A szó-lap alapjelentésének javítása

*FELADATOK #137 · Modell: opus · v1 · 2026.10.23*

## 1. Cél

A szó-lap fejlécének „Alapjelentés” sora (`blokkok.alapjelentes`) ma két hibát hordoz:

1. **A „LORD” hiba a forrásban.** Az Elohim (H0430) alapjelentéseként „LORD” áll (angolul, a JHVH szokásos fordításával). A lánc: a szó-lap a magyar BDB-ből nem kap alapjelentést → visszaesik a `strong_szotar.jelentes` mezőre → a `konkordancia/Strong_szotar.tsv` „Jelentés” oszlopa „LORD” → ugyanez a `konkordancia/TAHOT_kivonat.tsv` „Rövid jelentés” oszlopában (az Elohim 2 385 előfordulásánál „LORD”, 216-nál „gods”). A TAHOT-konverzió dokumentált szabálya (`TAHOT_TAGNT_README.md`, 5. pont) a STEPBible `Expanded Strong tags` glosszájából a `»` jel **utáni** részt veszi; a STEPBible az istenneveket a „LORD” személyhez köti (TBESH, H0410: „Another name of ye.ho.vah ("LORD" H3068G)”), a H0430 TBESH-glosszája „God”. Érintett Strong-számok (a `Strong_szotar.tsv` „Jelentés” = „LORD”): **H0136, H0410, H0430, H3050, H3068, H5251** (נֵס „zászló”, a „JHVH-nisszi” névből), **H5943, H5945, H5946, H7706**. *A nyers TAHOT-sort a befogadó session nem látta (a nyers fájl helyben nincs); a `»`-mechanizmus következtetés a szabályból, a TBESH-ből és a tíz egybevágó esetből — az M0 a nyers forráson igazolja.* A `Strong_szotar.tsv` előállító szkriptje nincs a repóban (2026-08-24, „deduplikált”); hogy a „Jelentés” oszlop a TAHOT-ból jön, az a kiejtés formájából (`'E.lo.Him`) és az egyező értékekből következik — az M0 ezt is igazolja.
2. **A magyar BDB-kinyerő 36 sornál nem ad alapjelentést.** Mérés (befogadó session, 2026-10-23; `scope=adat/forditasok.tsv BDB-sorok + eszkozok/olvaso_szerver/bdb_szelet.py | forras=helyi-futtatas | ts=2026-10-23`): 674 magyar BDB-sorból 367 változtatás nélkül, 271 gépi tisztítással ad magyar alapjelentést, **36 nem** (5,3%). A 36 négy fajtája: (a) a fej csak szófaj (H0430 „hímnemű többes számú főnév” — a BDB-ben valóban nincs címszó-jelentés, az angolban sem); (b) a jelentés ott van, de a `^` forrásjelölő miatt elutasítva (H0801 „…^Józs 13:14 tűzzel bemutatott áldozat”, H1847, H2077, H2256); (c) héber szóval kezdődő fej (H0589 „אֲנִי, névmás … én”); (d) tulajdonnév vagy számozott első pont (H0087, H0389).

## 2. Hatókör

**Benne van**

1. **Visszaesési sorrend** (`blokkok.alapjelentes`): magyar BDB → a **Károli leggyakoribb szótári alakja** (a meglévő szótövezéssel, DT130; forrásjelöléssel, pl. „Isten (Károli)”) → a **TBESH glosszája** (angol) → az angol Strong-szótár. A blokk-szintű kiadási és hozzáférési szűrés (a mai `magyar_ok` / `angol_ok`) minden ágra érvényes; tiltott forrás nem olvasható és nem szivárog. Mért kiinduló adat a szó-lap „Károli-alakok” blokkjából: H0430 „isten” 777, H0589 „én” 742, H0801 „tűzáldozat…”.
2. **Az istenneves sorok javítása az adatrétegben**: a `TAHOT_kivonat.tsv` „Rövid jelentés” és a `Strong_szotar.tsv` „Jelentés” oszlopa a 10 érintett Strong-számnál a glosszát hordozza (a `»` előtti rész vagy a TBESH-glossza — ⛔ M0). Új szkript (`eszkozok/alapjelentes_istennev_javit.py`), sor-szintű összevetéssel (CLAUDE.md, TSV-olvasás); a `TAHOT_TAGNT_README.md` 5. pontja a szabály kivételével bővül. Más oszlop és más sor nem változik.
3. **A BDB-kinyerő javítása csak a 36 sikertelen sorra**: előbb a mai 638 jó eredmény aranymintaként rögzítve (`teszt_alapjelentes_arany.tsv`: Strong, szöveg, tisztított), és a teszt bukik, ha bármelyik megváltozik; utána célzott szabályok a (b)–(d) fajtára.
4. **Kézi kivételtábla** (`adat/alapjelentes_kezi.tsv`, `manual` proveniencia, SEMA-szakasz): a maradék, ahol sem a BDB, sem a Károli-alak nem ad értelmes alapjelentést. Üres tábla is elfogadható kimenet.
5. A `pardes.db` újraépítése a meglévő építővel (`sqlite_epit.py`, csak futtatás) és a szó-lap mérése.

**Nincs benne**

- A BDB-fordítás (`adat/forditasok.tsv`) tartalmának módosítása.
- A TAHOT_kivonat többi sorának vagy oszlopának átírása; teljes TAHOT-újragenerálás.
- A szó-lap más blokkjai (a „Strong-szótár” blokk a javított adatot mutatja, a kódja nem változik).
- Licenc-módosítás; ha az M0 szerint a `Strong_szotar` licencsora (ma openscriptures) a tábla valódi forrását nem fedi, az N-tétel, nem javítás.

*A fejléc függései (befogadás, 2026-10-23):* `fugg: [134]`, mert a #134 az ágán a `blokkok.py`-t is írja (DT-F134j). `nem_fugg: [27]`: a #27 Thayer-sorokat ír az `adat/forditasok.tsv`-be; ez a feladat csak a BDB-sorokat olvassa, és az aranyminta a mai állapotot rögzíti (a levezetett függés a #27 ↔ #38 ↔ #137 kört adta). Az `olvas` szándékosan szűk: a szerver kódját (`lekerdezesek.py`, `oldalak.py`, `_szo_panel.html`), az `sqlite_epit.py`-t, a `SEMA.md`-t és a `licencek.tsv`-t a menet olvassa, de felsorolva függési kört adtak a konkordancia-táblák olvasóival (`KOR 22 27 38 48 101 102 103 104 120 122 137`); az `adat/SEMA.md` új szakaszát (a kézi tábla) a menet az M0 tervében jelzi, és ha a fejléc `ir`-je bővül, az új befogadás.

## 3. Lépések (⛔ a kötelező megállások)

- **M0 — igazolás és terv ⛔.** (1) A nyers STEPBible TAHOT-fájl a `TAHOT_TAGNT_README.md` szerinti forrásból (Gen–Deu fájl): az Elohim, az Él és a נֵס `Expanded Strong tags` mezője szó szerint, proveniencia-sorral; igazolja vagy cáfolja a `»`-mechanizmust. (2) A `Strong_szotar.tsv` „Jelentés” oszlopának eredete (TAHOT-egyezés mérése a teljes táblán). (3) A javítási forrás eldöntése a 10 sorra (`»` előtti glossza vagy TBESH) — **DT-F137a**. (4) A Károli-visszaesés pontos szabálya (szótári alak, nagybetű, több egyenlő gyakoriságú alak) — **DT-F137b**. Megállás: terv a felhasználónak.
- **M1 — aranyminta.** A mai 638 eredmény rögzítése; a teszt zöld a változtatás előtt.
- **M2 — adatjavítás.** A 10 Strong-szám sorai a két táblában; sor-szintű összevetés, napló (`naplok/ALAPJELENTES_JAVITAS_adat.md`).
- **M3 — kód.** A visszaesési sorrend és a kinyerő célzott szabályai; a kézi tábla betöltése. Az aranyminta zöld marad.
- **M4 — mérés ⛔.** A 674 sor újramérése (magyar / Károli / TBESH / Strong / kézi megoszlás), a 36 sor egyenként (előtte–utána), képernyőkép a H0430, H0410, H0801, H0589 szó-lapjáról. Megállás: jelentés.
- **M5 — tesztek és zárás.** `python eszkozok/teszt_futtat.py` (WSL-natív `pardes.db`), független ellenőr, zárójelentés.

## 4. Elfogadási feltételek

- **E1** A mai 638 magyar alapjelentés karakterre azonos (aranyminta-teszt).
- **E2** A 10 istenneves Strong-szám egyikénél sem áll „LORD” sem a szó-lap alapjelentésében, sem a „Strong-szótár” blokkban; a H0430-nál magyar vagy Károli-alapú alapjelentés áll (a DT-F137b szerint).
- **E3** A 36 sikertelen sor mindegyike magyar BDB-, Károli-, kézi vagy (indokolt esetben) TBESH-alapjelentést kap; angol Strong-visszaesés csak indoklással marad.
- **E4** A forrásjelölés látszik: a nem magyar BDB-ből jövő alapjelentés megmondja a forrását (`lang` és felirat).
- **E5** A tiltott forrás (kiadás, hozzáférési szint) egyik ágon sem olvasható (a `teszt_szintek.py` megfelelő esetei zöldek).
- **E6** A két konkordancia-táblában csak a 10 Strong-szám érintett oszlopa változik (sor-szintű diff a naplóban).

## 5. Döntésnapló

- **DT-F137a** 🟡 — a 10 istenneves sor javítási forrása: (a) a STEPBible-glossza `»` előtti része · (b) a TBESH-glossza · (c) mindkettő, eltérésnél ⛔. Javaslat: az M0 nyers adata alapján.
- **DT-F137b** 🟡 — a Károli-visszaesés szabálya: (a) a leggyakoribb szótári alak, nagy kezdőbetű a tulajdonnév/istennév jelleg szerint, „(Károli)” jelöléssel · (b) a két leggyakoribb szótári alak · (c) csak ha a leggyakoribb alak a párok legalább X%-a. Javaslat: az M0 mérése alapján.

## 6. Kiinduló mérés (2026-10-23, a befogadó session)

*Proveniencia: `scope=adat/forditasok.tsv (674 BDB-sor) + eszkozok/olvaso_szerver/bdb_szelet.py | forras=helyi-futtatas | ts=2026-10-23`; a szó-lap adatai: `scope=olvaso_szerver 127.0.0.1:8765 /r/szo/<Strong> | forras=bongeszo-meres | ts=2026-10-23`.*

| Eredmény | db |
|---|---|
| magyar alapjelentés, változtatás nélkül | 367 |
| magyar alapjelentés, gépi tisztítással | 271 |
| nincs magyar alapjelentés → angol Strong-szótár | 36 |

Tanulság a befogadó session próbájából (a repón kívül): egy általános előtisztítás (a `^` forrásjelölő a tapadt igehellyel és a vezető héber szó levágása minden sorra) a 36-ból 8-at javított, de **több mint 150 eddig jó sort rontott el** (pl. H3027 „kéz” → „nőnemű főnév és gyakran máshol”, H5971 „nép” → „_1840 hímnemű főnév”). Ezért a kinyerő javítása csak aranymintával és csak a sikertelen sorokra célzottan mehet.

Érintett istenneves sorok a `Strong_szotar.tsv`-ben (Strong | szótő | szófaj | Jelentés): H0136 אֲדֹנָי főnév | LORD · H0410 אֵל főnév | LORD · H0430 אֱלֹהִים főnév | LORD · H3050 יָהּ tulajdonnév | LORD · H3068 יהוה tulajdonnév | LORD · H5251 נֵס főnév | LORD · H5943 עִלַּי melléknév | LORD · H5945 עֶלְיוֹן főnév/melléknév | LORD · H5946 עֶלְיוֹן melléknév | LORD · H7706 שַׁדַּי főnév | LORD. A TAHOT_kivonat-ban a H0430 rövid jelentése: LORD 2 385, gods 216, God 1, Gibeath-elohim 1; a H0410-é: LORD 210, god 29, God 1, El-berith 1.
