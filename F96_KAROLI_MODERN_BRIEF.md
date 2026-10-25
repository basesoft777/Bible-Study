---
feladat: 96
cim: Modernizált Károli-szövegréteg — helyesírás és igealak, szókincs és szórend nélkül, az 1908-as szövegből generálva (DT128)
kod: KAROLI_MODERN
tipus: feladat
fazis: 1
modell: opus
munka: adat
allapot: megallt
ag: ccr-a680d019-39s73e
ad: a Károli 1908 modernizált szövegrétege (helyesírás + igealak; szórend, szókincs, írásjel, betoldás-jelölés változatlan), szabályalapú szavankénti cserével (a #94 szótári alak- és regies_jegy-táblájából, Hunspell csak fejlesztési mérce, DT301), LLM csak a szabállyal le nem fedett maradékra; minden token hordozza az 1908-as token vers-kulcsát és sorszámát (a Strong a #22 párosításából token-kulcson illeszthető, a réteg nem tárol Strongot, DT-F96f), a kieső segédigei vala jelölve; generált tábla az 1908-as szöveg mellett, nem helyette; két lépcső (helyesírás, majd igeragozás és vala), felhasználó által ellenőrzött mintán mérve, a token-felhasználással együtt
kovetkezo: "Te: [elteres_kor 2/2] ELLENOR_F96_3 1. mechanikus (a napló 15.6 megállás-mutatója); DT-F96v (a #96 lezárása)"
olvas: [adat/szoto/, konkordancia/Karoli_1908.tsv, "adat/karoli_strong/*", adat/SEMA.md, adat/licencek.tsv, DONTESEK.md]
ir: [eszkozok/karoli_modern/, adat/karoli_modern/, naplok/KAROLI_MODERN_meres.md, naplok/ELLENOR_F96.md, adat/SEMA.md, adat/licencek.tsv, DONTESEK.md, F137_KAROLI_MODERN_DB_BRIEF.md]
fugg: [94]
nem_fugg: [22]
---

# F96_KAROLI_MODERN_BRIEF.md — Modernizált Károli-szövegréteg (KAROLI_MODERN)

*FELADATOK #96 · Modell: opus · v2.2 · 2026.10.25 (csonk kitöltése; a `/befogad` hozta létre; v1.1: a DT301 átvezetve; v1.2: a DT-F96d/e/f átvezetve — K3, K4b, DT-F96b, .1/.2; v1.3: a DT-F96o átvezetve — K3b, .3; v1.4: a .3 kimenete két táblában, karoli_modern.tsv + karoli_modern_versek.tsv, napló 6.; v1.5: a független ellenőr ELTÉRÉS-einek javítása, DT-F96p, az `ir` lista kiegészítve, napló 7.; v1.6: a DT-F96q alkalmazva — régies-szken, opus-futás, az `ek_E1_T3` szabály, a lefedettséget mérő minta; DT-F96r, napló 10.; v1.7: a DT-F96r 2. opciója — a 4. kör, a minta2 újramérése; DT-F96s, napló 11.; v1.8: a DT-F96s 3. opciója — a jelöltként maradt alakok köre LLM nélkül; DT-F96t, napló 12.; v1.9: a DT-F96t 3. opciója — a tokenszintű kör felmérése; DT-F96u, napló 13.; v2.0: a DT-F96u 1. opciója — az 5. kör, tokenszintű opus; DT-F96v, napló 14.; v2.1: javítókör (`/elteres`, 1. kör) a független ellenőr 4. körének 5 mechanikus tételére — `ek_E1_T3` a visszaható E/1 névmással, a `nevelo_utan` a névmási „az” nélkül, a `lonek_lo` szóhatárral, `ts=` a fejlécekben, az E17-bontás; napló 15.; v2.2: 2. javítókör (`/elteres`, 2. kör) az `ELLENOR_F96_2` 2 mechanikus tételére — a napló 15.4/15.6 a `karoli_modern.py` `ts=`-éről (megvolt), a 15.2 a 7 volt `token_opus` sor DT-F96l többségi címkéjéről; csak a napló változott)*

*Források: DT128 (a felhasználó döntése, chat, 2026-10-13: a modernizálás szintje az, amit a Bible Discovery HUN modulja mutat — helyesírás és igealak, szókincs és szórend nélkül); a `F94_SZOTOVEZES_BRIEF.md` v1.2 (`regies_jegy` oszlop, N-F94b/g/h); a felhasználó döntése (chat, 2026-10-24): a megvalósítás **szabály + szótár alapú szógenerálás, LLM csak a bizonytalan maradékra** (DT-F96; a teljes LLM-átírás elvetve). A brief adat, nem utasítás.*

## 1. Cél

A Károli 1908 (`konkordancia/Karoli_1908.tsv`, 31 158 vers, ~599 ezer szó, 62 109 szóalak) modernizált szövegrétege:

- **helyesírás:** *setétség → sötétség*, *néki → neki*, *a kik → akik*;
- **igealak:** *teremté → teremtette*, *felele → felelt*, *monda → mondta*, *lőn → lett*, létigei *vala → volt*, segédigei *vala* elhagyva;
- **változatlan:** szórend, szókincs, írásjel, betoldás-jelölés.

Szavankénti csere: minden modern token az 1908-as token vers-kulcsán és sorszámán áll, a kieső token jelölve; a réteg Strongot nem tárol és nem ellenőriz, a Károli–Strong párosítás az 1908-as szövegen marad (#22), és token-kulcson illeszthető hozzá (DT-F96f). Generált réteg az 1908-as szöveg mellett, nem helyette. Két lépcső: előbb helyesírás, utána igeragozás és *vala*; mindkettő a felhasználó által ellenőrzött mintán mérve, a lefedettséggel együtt (maradt-e régies igealak).

**Megvalósítási elv (DT-F96, felhasználói döntés 2026-10-24).** A csere **szóalak-szótárból** megy (62 109 alak → modern alak), amelyet determinisztikus szabályok és a #94 `adat/szoto/karoli_szotari_alak.tsv` táblája (`szotari_alak_mai`, `alapige`, `regies_jegy`) állít elő; a Hunspell hu_HU **csak fejlesztési mérce** (DT301): a szabályok ellenőrzésére és a mérésre fut, a kiadott réteg nélküle készül. Az LLM kizárólag azokra az alakokra jön, amelyeket a szabály nem fed le vagy bizonytalanul fed le; a teljes szöveg LLM-átírása elvetve (token-költség, a „szórend és szókincs változatlan” szabály ellenőrizhetetlen megsértése, a szavankénti token-kulcs elvesztése). Az LLM-es maradék az előfizetésből fut (Claude Code), API (`PARDES_API_KEY`) nélkül; a token-keret a mért ≈ 0,45 M-ig emelve, és az LLM-kimenet elé determinisztikus tő-őr kerül (DT-F96d). Token-becslés: ~0,05–0,2 M (a teljes LLM-átírásé ~3–3,5 M); a tényleges érték a .0 mintán mérendő.

## 2. Hatókör

**Benne van**
- A szabálykészlet a helyesírási és igealak-cserére, forrásolt szabályokkal (`szabaly_forras`), a #94 `regies_jegy` értékkészletére építve.
- A szóalak → modern alak szótár (generált tábla), az LLM-es maradék javaslatai külön jelölt sorokként (`modszer`).
- A modernizált szövegtábla `adat/karoli_modern/` alatt, token-soronként, az 1908-as token vers-kulcsával és sorszámával (DT-F96f: Strong nélkül, token-kulcson illeszthető).
- Mérés felhasználó által ellenőrzött mintán: pontosság, a maradék régies igealakok aránya, és a **token-felhasználás** (a becslés ellenőrzése).

**Nincs benne**
- A Bible Discovery (SQL Uniform Kft., © 2026) KG/HUN szövege és Strong-rétege: nem használható adatként, csak a megfigyelt módszer leírása (DT128).
- Szókincs- és szórendváltoztatás, fordítási revízió.
- A Hunspell vagy más külső szótár beemelése a kiadott rétegbe vagy a szóalak-szótárba (DT301: a Hunspell csak fejlesztési mérce; más külső szótár csak új licencdöntéssel).
- A `pardes.db`-be töltés (a #76 vers-lapjának kapcsolójához): külön csonk, a `sqlite_epit.py` miatt a #92 után (N-F96a).

## 3. Lépések (⛔ a kötelező megállások)

### .0 — előkészítés és token-mérés
1. Modell-ellenőrzés (CLAUDE.md); a #94 kimenetének olvasása: `adat/szoto/karoli_szotari_alak.tsv`, `regies_jegy` értékkészlet (`adat/SEMA.md`).
2. Fedettségi mérés: a 62 109 alakból hányra ad a #94 tábla egyértelmű modern alakot, hányra kell szabály, hányra bizonytalan (LLM-jelölt). A keletkező szótár-lista és az LLM-jelöltek darabszáma a `naplok/KAROLI_MODERN_meres.md`-be.
3. Token-becslés ellenőrzése ~200 alakos mintán (tényleges felhasznált token, proveniencia-sorral); ha a teljes maradékra számolt érték meghaladja a 0,2 M-ot, megállás és jelzés. ⛔ A felhasználó dönt.

### .1 — helyesírási lépcső
1. Szabályok (*ly/j*, *cz → c*, *ö/ő*, *néki → neki*, *reá → rá* (DT-F96e b), *a kik → akik* különírt vonatkozó névmás, N-F94f) generátora `eszkozok/karoli_modern/` alatt; kódolási őr, `split('\t')` / `'\t'.join()`, `csv` modul nélkül, abszolút útvonal nélkül.
2. Hunspell hu_HU (DT301): csak fejlesztési mérce. Használat előtt a licenc szó szerinti idézettel, URL-lel (commit-hash) és lekérési dátummal a `naplok/KAROLI_MODERN_meres.md`-be (playbook 2. pont); a Hunspell-ítélet a szabály ellenőrzését szolgálja, a kimeneti táblába nem kerül Hunspellből származó alak. Ahol sem korpusz, sem Hunspell nem támasztja alá a szabályt: `modell_ellenorizetlen`.
3. Mintavétel (rögzített magú, ~100–120 mondat/vers), a felhasználó soronként ellenőrzi (`ellenorzes` oszlopot ő tölti); a mérés csak a `felhasznalo` sorokon. A mintában a *-jék* felszólító E/3 (DT-F96e d) is szerepel, mindkét alakkal: ott dönt a felhasználó. A K1 küszöbét a felhasználó itt rögzíti, a mérés előtt. ⛔
4. A DT-F96e (a) szerint a nem helyesírási lemmaváltások (*e → ez*, *oh → ó*, *férfiú → férfi*, *leány → lány*, az önálló *kik/mely*) nem változnak.

### .2 — igealak lépcső és *vala*
1. Igealak-csere a `regies_jegy` alapján (*mult.targyas.E3*, *mult.alanyi.E3*, *mult.T3*, *hatarozoi_igenev* … ; a *-ván/-vén → -va/-ve* a DT-F96e c szerint igen); a ritka alakok jegye ~6% hibás (N-F94h), ezért a ritka alakokon az LLM-es ellenőrzés a bizonytalan jelölt, nem automatikus csere. Az LLM-kimenet elé tő-őr (DT-F96d): ami nem hordozza az igető, illetve a szótári alak mai alakjának betűsorát, az `bizonytalan`, felhasználói sorba.
2. Létigei *vala → volt*, segédigei *vala* elhagyva: a kieső token jelölve (a token-kulcs megmarad, így a #22 Strong-párosítása továbbra is illeszthető, DT-F96f).
3. Mintavétel és felhasználói ellenőrzés a .1 szerint ⛔; a lefedettség (maradt-e régies igealak) kiírva.

### .3 — kimenet
- `adat/karoli_modern/karoli_modern.tsv` (token-soronként) és `adat/karoli_modern/karoli_modern_versek.tsv` (a modern vers-szöveg; a két tábla közös vers-kulccsal, a méret miatt, napló 6.) (a vers-kulccsal és a modern vers-szöveggel együtt; DT-F96b, `# GENERÁLT: …` fejléccel: a szabálykészlet és a bemeneti táblák sha256-ja, a mérés hivatkozása); kézzel nem szerkesztendő, a javítás a szabályban vagy a kivételtáblában történik.
- a K3b igazolása (a #22 Strongos tokenjeinek kulcs-lefedettsége, DT-F96o), naplózva;
- `adat/SEMA.md` új szakasza; a licenc-sor az `adat/licencek.tsv`-be (a modernizált réteg a közkincs 1908-as szövegből származik, DT116/DT128).

## 4. Elfogadási feltételek

- **K1.** A modernizált réteg a felhasználó által ellenőrzött mintán a megállapított küszöb felett (a küszöböt a .1 ⛔ rögzíti a mérés előtt, nem utólag).
- **K2.** A szórend, szókincs, írásjel és betoldás-jelölés változatlan: gépi összevetés az 1908-as szöveggel (tokenszám és sorrend a kieső tokenek jelölésével egyező).
- **K3.** (DT-F96f) Minden modern token az 1908-as token vers-kulcsán és sorszámán áll (a `tokenek.py` `tokenizal` sorszámozása, amelyen a #22 `hu_sorszam`-a is áll), így a Strong token-kulcson illeszthető; a réteg Strongot nem tárol és nem ellenőriz; a kieső tokenek jelölve, számuk naplózva.
- **K3b.** (DT-F96o) A Strong nem változik: a .3 generátora igazolja, hogy a #22 párosítás minden Strongos 1908-as tokenjének kulcsa szerepel a modern táblában (a kieső sorokkal együtt); hiányzó kulcsnál megáll. A kieső token sora megmarad, és `kieso_gazda` oszlopában a gazdaszó sorszámát hordozza (az összevont „a”-é a névmás, a segédigei *vala*-é az ige).
- **K4.** A token-felhasználás a naplóban, a becsléssel (0,05–0,2 M) összevetve.
- **K4b.** (DT-F96b, DT-F96f) A kimeneti tábla keresésre alkalmas: token-szinten (vers-kulcs, token-sorszám, 1908-as alak, modern alak, kieső-jelölés); Strong-oszlop nincs, a Strong a token-kulcson illeszthető a #22 párosításából.
- **K5.** Bible Discovery-adat nincs a repóban; abszolút útvonal nincs; `csv` modul nincs; CI zöld; a független ellenőr eltérés nélkül zár.

## 5. Döntésnapló

- **DT128** 🟢 — a modernizálás szintje (helyesírás + igealak, szókincs és szórend nélkül); a teljes szöveg a `DONTESEK.md`-ben.
- **DT-F96** 🟢 (helyőrző) — a megvalósítás szabály + szótár alapú szógenerálás, LLM csak a bizonytalan maradékra; a teljes LLM-átírás elvetve. *(felhasználó, chat, 2026-10-24; a token-becslés alapja: 599 ezer szó, 62 109 szóalak, ~3,78 M karakter)*
- **N-F94b** — a Hunspell hu_HU licencdöntés; lezárva a DT-F96c-vel (csak fejlesztési mérce).
- **DT301** 🟢 (helyőrző) — a Hunspell hu_HU csak fejlesztési mérce (a DT139 mintájára), a kiadott modernizált réteg nélküle készül. *(felhasználó, chat, 2026-10-24)*
- **DT-F96b** 🟢 (helyőrző) — a keresés a modernizált szövegrétegben is keressen (a szótári alakos kereséssel egyesítve), nem csak az alakszótárban. *(felhasználó, chat, 2026-10-24)* Következmény: a réteg táblája keresésre alkalmas sémájú (vers-kulcs, token-sorszám, modern alak; a Strong a DT-F96f szerint nem tárolt, token-kulcson illeszthető), hogy a `pardes.db`-be töltés és a `kereses.py` bővítése külön csonkban (N-F96a) ráépülhessen; maga a betöltés és a keresőbővítés nem a #96 `ir` listájában van.
- **DT-F96d** 🟢 (helyőrző) — a .0/3 ⛔: a mért token-felhasználás (≈ 0,44 M a teljes LLM-jelölt maradékra) a 0,2 M-os küszöb felett; **eldöntve** (felhasználó, chat, 2026-10-24): a keret emelhető (≈ 0,45 M), az LLM-es maradék az előfizetésből fut (Claude Code), API nélkül; tő-őr kötelező az LLM-kimenet elé. Mérés: `naplok/KAROLI_MODERN_meres.md` 2.
- **DT-F96e** 🟢 (helyőrző) — a modernizálás határa; **eldöntve** (felhasználó, chat, 2026-10-24): (a) a nem helyesírási lemmaváltások (*e → ez*, *férfiú → férfi*, *leány → lány*) maradnak; (b) *reá → rá*: igen (.1); (c) *-ván/-vén → -va/-ve*: igen (.2); (d) a *-jék* felszólító E/3 marad (felhasználó, 2026-10-24; a mintán eltérő ítélet felülírja).
- **DT-F96f** 🟢 (helyőrző) — a modernizált réteg nem tárol és nem ellenőriz Strongot; minden sora hordozza az 1908-as token vers-kulcsát és sorszámát, így a #22 Strong-párosítása token-kulcson illeszthető (felhasználó, chat, 2026-10-24). Átvezetve: 1. szakasz, 2. szakasz, .2/2, K3, K4b, DT-F96b.
- **DT-F96g** 🟢 (helyőrző) — a birtokos T/3 *-jok/-jök → -juk/-jük*; **eldöntve** (felhasználó, chat, 2026-10-24): a *j*-s változat (212 alak, 714 token) a .1 szabálya, a *j* nélküli marad; a mintán eltérő ítélet felülírja; alkalmazva (`jok` szabály, 714 token); `DONTESEK.md`, napló 4.7, 4.8.1.
- **DT-F96h** 🟢 (helyőrző) — a K1 küszöbe; **eldöntve** (felhasználó, chat, 2026-10-24): változásszinten ≥ 98% helyes csere a mintán és külön a `helyesiras_ami_ellenorzes.tsv` 102 szövegváltozó során, a `valtozatlan` réteg 0 kihagyással; a `jek`/`jok` A/B és a bizonytalan „a mi” nem hiba; `DONTESEK.md`, napló 4.7. Mérve: teljesül (minta 230/230, ami-ellenőrzés 101/102; modell-ellenőrzés, a felhasználó elfogadta), napló 4.8.3.
- **DT-F96j** 🟢 (helyőrző) — a *nék-* család (*néked, nékem, nékik, nékünk, néktek*; 3 919 token) a `neki` szabályban; **eldöntve** (felhasználó, chat, 2026-10-24: „Mehet”), alkalmazva; `DONTESEK.md`, napló 4.9.
- **DT-F96k** 🟢 (helyőrző) — (a) a felszólító *-jál/-jél* marad; (b) a kötőhangzós régi múlt automatikus csere (felhasználó, „Mehet”); napló 5.7.
- **DT-F96l** 🟢 (helyőrző) — 2. opció: a három forrásból kettő egyező, tő-őrös jelölt cserél (felhasználó, „Mehet”); napló 5.7.
- **DT-F96m** 🟢 (helyőrző) — a token-keret túllépése elfogadva; a keret a teljes számítással mérve, minden további LLM-futás előtt jóváhagyás (felhasználó, „Mehet”); napló 5.4.
- **DT-F96n** 🟢 (helyőrző) — a K1: a minta automatikus cseréi ≥ 98%, `valtozatlan` 0; a bizonytalanok külön; modell-ellenőrzés (felhasználó, „Mehet”); mérve: 99,1%; napló 5.7.
- **DT-F96o** 🟢 (helyőrző) — a Strong nem változik: a DT-F96f marad; a kieső token sora megmarad, a gazdaszó kulcsával (`kieso_gazda`); a .3 igazolja a #22 Strongos tokenjeinek kulcs-lefedettségét (K3b); a kieső, csak magán Strongot hordozó 294 token (257 összevont „a”, főleg H0834; 37 segédigei *vala*, H1961) Strongját a kereső a gazdaszóhoz köti (#137). *(felhasználó, chat, 2026-10-24: „Mehet”; napló 5.2)*
- **DT-F96p** 🟢 (helyőrző) — a *j* nélküli birtokos T/3 *-ök → -ük*, ahol a tő többese *-ek* (*szívök → szívük*, *velök → velük*), plusz a *nemök*; a múlt idejű T/2 ige kizárva (felhasználó, „Mehet”, 2026-10-25); napló 7.
- **DT-F96q** 🟢 (helyőrző) — a 3. kör maradéka: régies-szken (`regies_szken.py`), egyetlen vak opus-futás (1 516 kérdés, 595 232 token), csere a szabály és az opus egyezésével, tő-őrrel; az `ek_E1_T3` mondatszakaszra szűkítve; új K1-minta (`igealak_minta2.tsv`) a lefedettséggel (felhasználó, „Mehet a javaslattal”, 2026-10-25); napló 10.
- **DT-F96r** 🟢 (helyőrző) — a lefedettség a 3. kör után 92,7%; **eldöntve** (felhasználó, „2”, 2026-10-25): még egy kör — a 4. kör (`regies_szken.py --kor 4`, 485 kérdés, opus, 282 897 token; 184 token csere, 16 *vala*), a minta2 újramérve: 96,9%; napló 11.
- **DT-F96s** 🟢 (helyőrző) — a 4. kör után; **eldöntve** (felhasználó, „3”, 2026-10-25): további kör a jelöltként maradt alakokra, LLM nélkül — a nem tanúsított szabály-jelölt helyett a korpuszban álló opus-alak, a .1 cseréje a szavazatokon, az alanyi–tárgyas pár; 70 token, a minta2 véletlen rétegén 99,0%; napló 12.
- **DT-F96t** 🟢 (helyőrző) — a jelölt-kör után; **eldöntve** (felhasználó, „3”, 2026-10-25): további kör tokenszintű LLM-kérdéssel, a keret külön jóváhagyással (DT-F96u); napló 13.
- **DT-F96u** 🟢 (helyőrző) — a tokenszintű kör; **eldöntve** (felhasználó, „1”, 2026-10-25): 370 kérdés, teljes verssel, vak opus (285 418 token); 205 token csere, 106 jelölt marad; napló 14.
- **DT-F96v** 🟡 (helyőrző) — az 5. kör után: javaslat a független ellenőr újrafuttatása friss véletlen mintával, majd a #96 lezárása; `DONTESEK.md`, napló 14.4.
- **N-F96c** (helyőrző) — a .1 szabályai által nem fedett egyedi régi írásmódok (*irígy, akképen, husvét, bölcseség, nyilásának, hizelkedő, sujts*, *nékie*) és az összetételben álló *-jok* (*atyjokfiai*): korpusz-szintű számuk nem mért; napló 4.8.4.
- **N-F96d** (helyőrző; a DT-F96q-val nagyrészt megoldva: 420 alak, 690 token; maradék: napló 10.6) — a fedettségi mérés `valtozatlan` osztályában maradt régies igealak-osztályok: E/3 tárgyas *-á/-é* (kb. 180 alak: *megnyergelé, körülmetélé, állatá*), E/2 tárgyas *-ád/-éd* (kb. 55: *adád, rakád*), T/3 alanyi *-ának/-ének* (*gyűlének, akadának, foganának*), a maradék E/1 *-ám/-ém* (kb. 69 alak: *imádkozám, evém, megérkezém*), *levék, jövénk*; a lefedettség-számláló ezeket nem látja (ellenőr 3. kör, 1. és 3. tétel; napló 9.).
- **N-F96e** (helyőrző; a DT-F96q-val megoldva: 71 *vala* kiesik; maradék 3 pár, napló 10.6) — a *vala* előtti ragtalan E/3 jelen (*sátoroz, táncol, szakadoz, felkél, sántít* … vala → *volt*, legalább 14 token) és az igei régmúlt (*alkotott, formált, megszünt* … vala → *volt*, kb. 25) maradéka; az 1Krón 12:2 közös *vala*-ja (ellenőr 3. kör, 2. tétel).
- **N-F96f** (helyőrző; részben megoldva: a mondatszakasz-szabály és az `E1_MINDIG_VEG` 17 tokent javított, napló 10.4; a visszaható E/1 névmás (*magamnak* …) mellett T/3-ra fordított 4 token (Préd 2:5 ×2, 2:6, 2:9; ELLENOR_F96 4. kör, 1.) a javítókörben javítva, napló 15.1; ismert, nyitott maradék: 3 E/1 helyen T/3 maradt, 1Móz 39:15 *kezdék*, Dán 7:16 *kérék*, Ez 22:30 *keresék*, napló 10.4; az `ek_E1_T3` heurisztika a 694 tokenes osztály egészén nem igazolt) — az `ek_E1_T3` heurisztika: a *felelék* E/1 helyen T/3-ra (*felelték*, 8 token), az *eljövék → eljötték* nem létező alak; az LLM-jelölt itt jobb (ellenőr 3. kör, 4. tétel).
- **N-F96g** (helyőrző; megoldva: `igealak_minta2.tsv`, a kihagyás is számít, napló 10.6) — a K1 mérési eljárása: a minta változatlanul maradt régies alakja (G051 *rakád*, a 2. körben G050 *mondám*) nem számított kihagyásnak; a K1 csak a cserék pontosságát méri, a lefedettséget nem (ellenőr 3. kör, 5. tétel).
- **DT-F96i** 🟢 (helyőrző) — a puszta „a mi” birtokos/vonatkozó támpontjai (B1/B2 *-nk* birtokos, V1–V4); **eldöntve** (felhasználó, chat, 2026-10-24, „Mehet a javaslat”): a kiadott .1-ben (bizonytalan 298 → 7, 93 hibás összevonás visszavonva); a 109 szöveget változtató vagy bizonytalan token külön felhasználói ellenőrzésre (`adat/karoli_modern/helyesiras_ami_ellenorzes.tsv`), a K1 erre is vonatkozik; napló 4.6.
- **N-F96b** (helyőrző) — a #94 `regies_jegy` értékkészletéből hiányzik a tárgyas T/3 (*mondák, adák*), és megfigyelt táblahibák (*vévén*, *kivűl*); a modernizálás saját szabállyal kezeli (napló 1.2).
- **N-F96a** (helyőrző) — a modernizált réteg `pardes.db`-be töltése és a keresőbe kötése (`eszkozok/sqlite_epit.py`, `eszkozok/olvaso_szerver/kereses.py`) külön csonk-feladat, a #96 és a #92 után; a DT-F96b miatt kötelező, nem elhagyható. A csonk: #137 (KAROLI_MODERN_DB), a felhasználó jóváhagyásával befogadva (2026-10-24).
