# F178 — a lexikon ág lezárása: menetjelentés (1. lépés: csak a HAMART-001)

*Végrehajtó: claude-opus-5-5 (a brief `modell`: opus; egyezik). Ág: `claude/lexikon-ag-lezaras`. Dátum: 2026-11-08.*

## Egyeztetett eltérések

1. **Formai függés.** A fejléc szerinti `fugg: [123, 176]` formailag nem teljesül (a #123 a többi motívum miatt `megallt`, a #179 fejléce a merge után nem frissült); a tartalmi előfeltétel teljesül (PR #639, #649, #654 a main-ben). A felhasználó a futást jóváhagyta („Mehet”). A #123 és a #179 fejléce érintetlen.
2. **Előbb csak a HAMART-001** (a felhasználó: „Előbb csak a hamart”). Az új szerkezet a `lexikon_general.UJ_LAPSZERKEZET` halmazán (ma: HAMART-001) áll; a többi lap és a `nyilt_mag/` nincs újragenerálva, generálásuk bájtra változatlan (E28: 5 migrált nézet, 0 eltérés). A nyílt mag exportja és kapuja megváltozott, próbaexport a repón kívül.
3. **Megálló.** A felhasználó a HAMART-001-et csak a visszhang 2. fázisa után, teljes lapként nézi át („Én csak a teljes lapot nézem”); a megálló az orkesztrátori átnézés.

## Tételek

| Tétel | Állapot | Mit változtatott |
|---|---|---|
| F178.0 | kész | modell-ellenőrzés; a #639 Nave- és gépi őr-munkája megvan (F123.HAMART3.24: NAVE_ANGOL; .25: 37., 38. szabály), hiányzó rész nincs |
| F178.1 | kész | `ellenoriz.py` 39. szabály (határ-frissesség, SORÁLLAPOT-jel: a motívumsorok rendezett SHA-256-ja; JELENTÉS), Feed 5. kritérium piros nem friss modelles résznél (HIBA: a lap nem adható ki), `--hatar-ujjlenyomat`; MUNKAMENET C-h |
| F178.2 | kész | U2/U3 szétválasztás: 9-es sablon v2 (hét szabály), MUNKAMENET C-w |
| F178.3 | kész | 10-es U3-prompt sablon; 9-es sablon v2; 6-os sablon v4; `ellenoriz.py` 40. szabály (regressziós HIBA-kapuk), 41. szabály (közlemény, JELENTÉS) |
| F178.4 | kész a HAMART-001-en; ⛔ DT-F178b nyitva | Döntési út, folyamatos számozás 1–12 (4.1–4.14), tanítói rész nélkül, áttekintő tábla, belső jel olvasói formára (a nyers proveniencia HTML-megjegyzésben), olvasói kapu kivétel nélkül az új szerkezetű lapon; B9 kivezetve, 7-es sablon ARCHÍV |
| F178.5 | kész a HAMART-001-en | `adat/visszhang_megfelelok.tsv` (SEMA 2.53, 74 sor), `megfelelo_kinyer.py`, arámi kiejtés (A1), a 4.11 blokk alapvonallal (DT-F178d), BDB-háttér szűkítve |
| F178.6 | kész (a lapon és az exportban; a `nyilt_mag/` nincs újragenerálva) | SZERKESZTOI_CSERE (magyar, angol), SZERKESZTO-kapu; a lapon „felhasználó” BUKÁS az új szerkezetben |
| F178.7 | kész az exportban | [A LEXIKON CÍME] a nyílt mag címében és fejlécében |
| F178.8 | kész (a #639 elvégezte) | a HAMART-001-en NAVE_ANGOL 0 |
| F178.9 | a HAMART-001-en kész; a többi lap elmarad (4. eltérés) | a HAMART-001 orkesztrátori átnézése a megálló |

## Kapuk a HAMART-001-en (utolsó futás)

- `olvasoi_kapu.py HAMART-001`: `## HAMART-001: 0 BUKÁS, 26 FIGYELMEZTETÉS` (kivétel nélküli mérés)
- `ellenoriz.py`: kilépési kód 0, SÉRTÉS 0; 40. szabály: a HAMART-001 átmegy, a 8 régi szerkezetű lap JELENTÉS (2. kiadás tétele)
- `proza_1a.py HAMART-001`: 48/48 arany szint
- `megfelelo_kinyer.py ellenoriz`: 74 sor, 0 hiba

## A 2. kiadásra / a következő körre átadott tételek

- **Határ-frissesség (39.):** ALVIL-001 (72 → 74 sor), HAMART-001 (60 → 48 sor) elavult; ANTROP-001, ISTENTISZT-001, TEREMT-002 jel nélküli. A modelles rész újrafuttatása a felhasználó jóváhagyásával (C-h); a `hatar-ellenor` ügynök utasítása a SORÁLLAPOT-jelre nem a #178 írása.
- **Regressziós kapuk (40.):** a régi szerkezetű lapokon a Döntési út hiányzik; HODIT, KIRALY, MENNY, TEREMT-001, TEREMT-002: olvasói kapu BUKÁS, nem kerek próza, üres Nave-blokk.
- **Közlemény (41.):** `kozlemeny/MI_NYILATKOZAT.md` 2 előfordulás.
- **Visszhang:** két kézi sor ellenőrizetlen (kinyerő = ellenőr): LXX 1Móz 8:21 ἔργα, asszír qalâlu; a görög rövid jelentések (G1944, G2671, G5356) fordításra várnak.
- **Adatlelet:** a H6093 és a H1863 helyi BDB-szócikke megvan (a Sefaria-lekérdezés bdb_szócikk=0).
- **Előzőleg is bukó tesztek (nem e menet okozta):** `teszt_olvasoi_kapu.py` Arany.test_G7 (DT476), `teszt_nyilt_mag.py` (feloldatlan DT-F123h), `olvaso_szerver/teszt_bdb_vers_jelentes.py` (bemeneti hash).

## Helyőrzős döntések (`dontesek/uj/lexikon-ag-lezaras.md`)

- **DT-F178b** (⛔): a `tanitoi` rés sorsa — (a) kivezetés, (b) az adatrétegben marad, a lapon nem áll, (c) a visszhang tanúrétegévé alakul; javaslat: (b) most, (a) a többi lap körével.
- **DT-F178c**: a lapszerkezet levezetett részletei (4.11 visszhang, 10. Alkalmazás, az 1.4/1.5 gépi tartalma).
- **DT-F178d** (🟢, „Mehet”): a visszhang következtetési szabálya (alapvonal, 80% / 40%).
- **DT-F178e** (🟢): a visszhang-szabályok átvihetősége (sablon, C-vh, VISSZHANG kapu, arany-minta teszt).

## Kiegészítés (2026-11-08, a menet végén)

### További egyeztetett eltérés

4. **A második szakasz elmarad** (a felhasználó: „Ne a régi hibákkal írjuk újra a többi lapot. Minden menjen át a teljes folyamaton”). A #178 a HAMART-001 lapjával, a generátorral, a sablonokkal (6, 9, 10), a MUNKAMENET-tel, a kapukkal és a tesztekkel zárul; a többi lexikonlap és a `nyilt_mag/` nincs újragenerálva, és a #178-ban nem is lesz. A brief `ad` mezője ennyivel szűkül: „minden lexikonlap az új lapszerkezettel” helyett „a HAMART-001 lapja az új lapszerkezettel; a generátor, a sablonok és a kapuk minden új vagy lezárandó lapra készen” — a többi lap motívumonként, a teljes folyamaton (határ, próza, kinyerés két kézzel, visszhang 2. fázis, kapuk, felhasználói átnézés), külön feladatokban.

### CI-őr a generált lapok frissességére

Van: az **E28** (`eszkozok/ellenorzes/szabalyok.py` `e28_generalt_nezet_egyezes`, HIBA) az `e28_migralt_nezetek.tsv` öt lapját (ISTENTISZT-001, ALVIL-001, TEREMT-002, ANTROP-001, HAMART-001) a repón kívül újragenerálja, és bájtra összeveti a commitolt lappal. **Nem bukik:** az új szerkezet és minden F178-generátorváltozás az `UJ_LAPSZERKEZET` halmazára (ma: HAMART-001) szűkül, a többi lap generálása bájtra változatlan. A legutóbbi futás (`python eszkozok/ellenorzes/futtat.py --teljes`) sorai: `## E28 (0 talalat)`, `- E28: 5 migrált nézet`, kilépési kód 0. A többi lap tehát nem igényel generátor-verzió jelölést; ha egy későbbi generátorváltozás a halmazon kívüli lapot is érintené, az E28 azonnal jelez. Javaslat erre az esetre (a döntés az orkesztrátoré): az `UJ_LAPSZERKEZET` halmaz maradjon a lapszerkezet-verzió jelölője (a motívum a halmazba kerül, amikor a teljes folyamaton átment), ne vezessünk be külön verziómezőt.

### Melyik szabály hol él

| Szabály | Sablon | Kapu | Teszt |
|---|---|---|---|
| Lapszerkezet 1–12, Döntési út, tanítói rész nélkül | 6-os sablon v4, „Az új lapszerkezet…” | 40. szabály (összeadás, döntés nélküli vers 0) | `teszt_olvasoi_kapu.py` UjSzerkezet |
| Olvasói kapu kivétel nélkül, „felhasználó” | 6-os sablon v4 | olvasói kapu (új szerkezetnél) | UjSzerkezet (4 teszt) |
| Kerek 2.1 + „Funkció:”, Nave nem üres | 9-es sablon v2, 6-os v4 | 40. szabály, 25. szabály | `teszt_proza_1a.py` |
| Határ-frissesség | 9-es v2, MUNKAMENET C-h | 39. szabály, Feed 5. kritérium | `teszt_muhely_allapot.py` TesztHatarFrissesseg (5) |
| U2/U3 szétválasztás, U3 nulláról | 9-es v2 1. és 7. szabály, 10-es prompt, MUNKAMENET C-w | — (menetszabály) | — |
| Szerkesztői döntés | 6-os v4 | olvasói kapu BELSO; nyílt mag SZERKESZTO; 41. szabály (közlemény) | `teszt_nyilt_mag.py` TesztSzerkesztoi (3) |
| Visszhang 4.11, 1–8. | 6-os sablon „A 4.11 visszhang-blokk szabályai”; 10-es prompt; MUNKAMENET C-vh | olvasói kapu VISSZHANG V1–V6 | `olvaso_szerver/teszt_visszhang_kapu.py` (9; arany minta + 6 rontott másolat) |
| Kinyerő tábla, két kéz | SEMA 2.53; MUNKAMENET C-vh | `megfelelo_kinyer.py ellenoriz` | — |
| Arámi kiejtés | — | — | `teszt_heber_kiejtes.py` test_a1 |

### Egy új motívumnál melyik lépés gondoskodik a visszhangról

A **C-vh** (MUNKAMENET): a Targum- és a Vulgata-megfelelőt modell emeli ki, egy másik kéz ellenőrzi (`megfelelo_kinyer.py beolvas … --ellenor`), a LXX-oszlop és az alapvonal gépi (`… lxx`), a BDB rokon nyelvi háttér ugyanitt; a lapot a generátor állítja elő (C1), a VISSZHANG kapu (C-o) védi. A próza (C-w, 10-es prompt) a blokk után jön, és nem állít többet nála. A meglévő lapoknál ez a motívumonkénti lezárás (#10) lépése.

### DT-F178b — a felhasználóhoz (röviden)

A `tanitoi` rés sorsa: (a) kivezetés az adatrétegből (a `res_forras.tsv` sorai, nyolc rés, a CLAUDE.md mondata, a tanítói fájlok archívumba); (b) a rés az adatrétegben marad, a lapon nem áll; (c) a visszhang tanúrétegévé alakul (2. fázis). **Ajánlás: (b) most** (visszafordítható, adatot nem érint, a régi lapok nem törnek el), **(a) akkor, amikor az utolsó lap is átment a teljes folyamaton**; a (c) a 2. fázis saját döntése.
