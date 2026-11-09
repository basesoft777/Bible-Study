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
| F178.4 | kész a HAMART-001-en; ⛔ DT643 nyitva | Döntési út, folyamatos számozás 1–12 (4.1–4.14), tanítói rész nélkül, áttekintő tábla, belső jel olvasói formára (a nyers proveniencia HTML-megjegyzésben), olvasói kapu kivétel nélkül az új szerkezetű lapon; B9 kivezetve, 7-es sablon ARCHÍV |
| F178.5 | kész a HAMART-001-en | `adat/visszhang_megfelelok.tsv` (SEMA 2.53; f46b10b7: 74 sor, bb3020eb: 82 sor — a „74” a végállapotra elavult volt, ELLENOR_F178 6.; a javítókör után 127 sor, l. „Bontási napló”), `megfelelo_kinyer.py`, arámi kiejtés (A1), a 4.11 blokk alapvonallal (DT645), BDB-háttér szűkítve |
| F178.6 | kész (a lapon és az exportban; a `nyilt_mag/` nincs újragenerálva) | SZERKESZTOI_CSERE (magyar, angol), SZERKESZTO-kapu; a lapon „felhasználó” BUKÁS az új szerkezetben |
| F178.7 | kész az exportban | [A LEXIKON CÍME] a nyílt mag címében és fejlécében |
| F178.8 | kész (a #639 elvégezte) | a HAMART-001-en NAVE_ANGOL 0 |
| F178.9 | a HAMART-001-en kész; a többi lap elmarad (4. eltérés) | a HAMART-001 orkesztrátori átnézése a megálló |

## Kapuk a HAMART-001-en (utolsó futás)

- `olvasoi_kapu.py HAMART-001`: `## HAMART-001: 0 BUKÁS, 26 FIGYELMEZTETÉS` (kivétel nélküli mérés)
- `ellenoriz.py`: kilépési kód 0, SÉRTÉS 0; 40. szabály: a HAMART-001 átmegy, a 8 régi szerkezetű lap JELENTÉS (2. kiadás tétele)
- `proza_1a.py HAMART-001`: 48/48 arany szint
- `megfelelo_kinyer.py ellenoriz`: 82 sor, 0 hiba (az első menet végén; a javítókör után: l. „Bontási napló”)

## A 2. kiadásra / a következő körre átadott tételek

- **Határ-frissesség (39.):** ALVIL-001 (72 → 74 sor), HAMART-001 (60 → 48 sor) elavult; ANTROP-001, ISTENTISZT-001, TEREMT-002 jel nélküli. A modelles rész újrafuttatása a felhasználó jóváhagyásával (C-h); a `hatar-ellenor` ügynök utasítása a SORÁLLAPOT-jelre nem a #178 írása.
- **Regressziós kapuk (40.):** a régi szerkezetű lapokon a Döntési út hiányzik; HODIT, KIRALY, MENNY, TEREMT-001, TEREMT-002: olvasói kapu BUKÁS, nem kerek próza, üres Nave-blokk.
- **Közlemény (41.):** `kozlemeny/MI_NYILATKOZAT.md` 2 előfordulás.
- **Visszhang:** két kézi sor ellenőrizetlen (kinyerő = ellenőr): LXX 1Móz 8:21 ἔργα, asszír qalâlu; a görög rövid jelentések közül fordításra vár (mérve: `lexikon_general.rovid_jelentes`, a motívum görög szavai és a kinyerő tábla LXX-lemmái): G1944 ἐπικατάρατος, G2041 ἔργον, G2671 κατάρα, G3077 λύπη, G5356 φθορά — az első listából a G3077 és a G2041 kimaradt (ELLENOR_F178 6.).
- **Adatlelet:** a H6093 és a H1863 helyi BDB-szócikke megvan (a Sefaria-lekérdezés bdb_szócikk=0).
- **Előzőleg is bukó tesztek (nem e menet okozta):** `teszt_olvasoi_kapu.py` Arany.test_G7 (DT476), `teszt_nyilt_mag.py` (feloldatlan DT-F123h), `olvaso_szerver/teszt_bdb_vers_jelentes.py` (bemeneti hash).

## Helyőrzős döntések (`dontesek/uj/lexikon-ag-lezaras.md`)

- **DT643** (⛔): a `tanitoi` rés sorsa — (a) kivezetés, (b) az adatrétegben marad, a lapon nem áll, (c) a visszhang tanúrétegévé alakul; javaslat: (b) most, (a) a többi lap körével.
- **DT644**: a lapszerkezet levezetett részletei (4.11 visszhang, 10. Alkalmazás, az 1.4/1.5 gépi tartalma).
- **DT645** (🟢, „Mehet”): a visszhang következtetési szabálya (alapvonal, 80% / 40%).
- **DT646** (🟢): a visszhang-szabályok átvihetősége (sablon, C-vh, VISSZHANG kapu, arany-minta teszt).

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
| Visszhang 4.11, 1–8. | 6-os sablon „A 4.11 visszhang-blokk szabályai”; 10-es prompt; MUNKAMENET C-vh | olvasói kapu VISSZHANG V1–V7 (V7: az alapvonal-mondat sávja és számai) | `olvaso_szerver/teszt_visszhang_kapu.py` (18; arany minta 2, rontott másolat és szintetikus tábla V1–V7 9, gépi szabály 3, a lánc a motívumadatból 4) |
| Kinyerő tábla, két kéz | SEMA 2.53; MUNKAMENET C-vh | `megfelelo_kinyer.py ellenoriz` | `olvaso_szerver/teszt_megfelelo_kinyer.py` (21; az `ellenorzes` mező, a szórend szerinti LXX-kiosztás, a szócsalád) |
| Arámi kiejtés | — | — | `teszt_heber_kiejtes.py` test_a1 |

### Egy új motívumnál melyik lépés gondoskodik a visszhangról

A **C-vh** (MUNKAMENET): a Targum- és a Vulgata-megfelelőt modell emeli ki, egy másik kéz ellenőrzi (`megfelelo_kinyer.py beolvas … --ellenor`), a LXX-oszlop és az alapvonal gépi (`… lxx`), a BDB rokon nyelvi háttér ugyanitt; a lapot a generátor állítja elő (C1), a VISSZHANG kapu (C-o) védi. A próza (C-w, 10-es prompt) a blokk után jön, és nem állít többet nála. A meglévő lapoknál ez a motívumonkénti lezárás (#10) lépése.

### DT643 — a felhasználóhoz (röviden)

A `tanitoi` rés sorsa: (a) kivezetés az adatrétegből (a `res_forras.tsv` sorai, nyolc rés, a CLAUDE.md mondata, a tanítói fájlok archívumba); (b) a rés az adatrétegben marad, a lapon nem áll; (c) a visszhang tanúrétegévé alakul (2. fázis). **Ajánlás: (b) most** (visszafordítható, adatot nem érint, a régi lapok nem törnek el), **(a) akkor, amikor az utolsó lap is átment a teljes folyamaton**; a (c) a 2. fázis saját döntése.

## Javítókör az orkesztrátori átnézés után (bb3020eb)

A 4.11 hat pontja generátor-szinten javítva (l. a commit üzenetét); a HAMART-001 újragenerálva: olvasói kapu `0 BUKÁS, 25 FIGYELMEZTETÉS`; `ellenoriz.py` kilépési kód 0; `teszt_visszhang_kapu.py` 13/13. Új kapuszabály: VISSZHANG V7 (az alapvonal-mondat sávja); V6 tagmondat-szintű, cellán belül is. A javítókör közben a saját átnézés egy további hibát talált és javított: a forrásnév-átírás regexe a könyvtár-előtagot csak az első alternatívára tette (az Irodalomban „a lap adattáblája” állt „a BDB-szótár” helyett), és az ismétlődő forrásnév most egyszer áll.

### Az olvasói kapu 25 FIGYELMEZTETÉS-e (egyik sem akadályozza a kiadást)

| Azonosító | Db | Mi |
|---|---|---|
| KIVONAT_SZAM | 2 | a Kivonat „56 vers” és „négy hely” száma nem a tábla helyszáma (versszám, illetve a tematikus kivételek száma — helyes, a mérő a táblával veti össze) |
| HIANYJEL | 3 | „(nincs hozzárendelés)” az iccávón (2.) és „(nincs címke: 1.b)” a chattát jelentés-cellájában; „nincs a szakasztáblában” a 4.2 egy BDB-útvonalánál — adathiány, a 2. kiadás tétele |
| ANGOL_SOR | 7 | szótár- és licencnevek (UBS DNTG/DBH, BDB teljes címe, tW-licencmondat) és egy Nave-alcím `title`-je — tulajdonnevek és licencszöveg |
| MOTIVUM_ID | 5 | TEREMT-002 (kétszer, a jelöltindoklásban), ISTENTISZT-001 (kapcsolat-összegzés), HAMART-001 (a Kolofon „ID” és „Hogyan idézd” sora) — link nélküli azonosító |
| ATIRAS_VALT | 4 | „adamá”, „arar” a jelöltindoklásokban (adat), „chamasz” a 4.2-ben, „adama” az arab rokon alak kiejtése — a héber adámától eltérő szó vagy régi indoklás |
| SZINT_ALATT | 4 | üres szótári pontok (4.1 görög, 4.13, 4.14: „javaslat”), a 7. Kapcsolatok „még nincs ilyen” mondata |

## DT643 végrehajtása — ⛔ megállva

A felhasználó döntése („Kivezetjük”) a `dontesek/uj/lexikon-ag-lezaras.md`-ben 🟢. **A végrehajtás nem történt meg**, mert a régi lapokat érintené:

- a `res_forras.tsv` `tanitoi` sorainak törlése után a régi szerkezetű generálás a rés-határt nem találja (`_BOUNDARY_SLOTS` → `ValueError: hiányzó res_forras.tsv sor`), a szakasz kiesése után pedig a 8 régi lap kimenete változik: ALVIL-001 −6 sor, ANTROP-001 −6, ISTENTISZT-001 −32, TEREMT-002 −31, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001 −4–4 sor (a „### Tanítói egyezés” szakasz);
- az E28 a négy migrált lapon (ISTENTISZT-001, ALVIL-001, TEREMT-002, ANTROP-001) bukna;
- a két tanítói forrásfájl (`motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md`, `motivumok/naplok/TEREMT-002_tanitoi_kereses.md`) a régi lapok résforrása; archiválásuk ugyanígy a régi lapokat változtatná; rájuk mutat a `NYITOTT_FELADATOK.md` és kilenc brief `olvas` mezője.

**Javaslat (a döntés az orkesztrátoré):** lépcsős kivezetés. Most csak a HAMART-001 `tanitoi` sora törlődik (az egyetlen új szerkezetű lap; kimenete nem változik), a generátor a rést csak a sorral rendelkező motívumnál keresi. A többi motívum sora és tanítói fájlja (`archivum/<ID>/`, ARCHÍV fejléccel, a hivatkozásokkal együtt) a motívum teljes folyamatának lapgenerálásával egy commitban kerül ki; a CLAUDE.md és a SEMA „kilenc rés” mondata addig „kilenc rés, a `tanitoi` kivezetés alatt (DT643)”, az utolsó lappal „nyolc rés”. A `CLAUDE.md` és az `archivum/` érintése az `ir` mezőn kívüli: egyeztetett eltérésként jelzem, amikor megtörténik.

## DT643 végrehajtva — lépcsős kivezetés (2026-11-08)

Orkesztrátori döntés a „Kivezetjük” módjáról: a HAMART-001 `tanitoi` sora törölve az `adat/res_forras.tsv`-ből (a lap kimenete nem változott: „változatlan, 546606 bájt”); a generátor sor nélkül a rést kivezetettnek veszi (`res_kivezetett`, a régi címhatár a váz literál fejlécével); az `ellenoriz.py` 11. szabálya a hiányzó `tanitoi` sort nem kéri. A CLAUDE.md és a SEMA 2.12 mondata: „kilenc rés, a `tanitoi` kivezetés alatt (DT643)”. A többi motívum sora és tanítói fájlja a saját teljes folyamatának lapgenerálásával egy commitban kerül ki (MUNKAMENET C5). Egyeztetett eltérés: a `CLAUDE.md` és az `adat/res_forras.tsv` az `ir` mezőn kívül.

## Bontási napló: `adat/visszhang_megfelelok.tsv` (ELLENOR_F178 6.)

A tábla a #178 új fájlja (a `9af7cecf` alapon nincs). Sorszám a mért tábla szerint (`python eszkozok/visszhang/megfelelo_kinyer.py ellenoriz`; bontás: forrás × kinyerés × az `ellenorzes` mező):

| forrás | kinyerés | állapot | 46c234c7 (első menet vége) | javítókör 1/2 után |
|---|---|---|---|---|
| targum | modell | ellenőrzött | 17 | 32 |
| vulgata | modell | ellenőrzött | 17 | 32 |
| lxx | gepi | ellenőrzött | 16 | 27 |
| lxx | gepi | ellenőrizetlen | 0 | 4 |
| lxx | kezi | ellenőrizetlen | 1 | 1 |
| bdb | modell | ellenőrzött | 30 | 21 |
| bdb | modell | ellenőrizetlen | 0 | 9 |
| bdb | kezi | ellenőrizetlen | 1 | 1 |
| **összesen** | | | **82** | **127** |

- Forrásonként: targum 17 → 32, vulgata 17 → 32, lxx 17 → 32, bdb 31 → 31. A Targum és a Vulgata 17 sorából 16 a lánc-szavak sora, 1 a 8:21 betoldás-sora (H2403).
- A változás (+45): a motívumadatból levezetett lánc (DT648) 15 hiányzó (lánc-szó, láncvers) párja — Targum +15, Vulgata +15 (kinyerő `claude-sonnet-5-5`, ellenőr `claude-opus-5-5`), LXX +15 gépi (11 egyértelmű; 4 nem egyértelmű, ellenőrizetlen: H0127 1Móz 3:23, 4:2, 4:12; H7843 9:15).
- A bdb ellenőrzött 30 → 21: a meglévő sorok `ellenorzes`-e az új szabállyal íródott újra (ELLENOR_F178 4.: a kézi átnézés csak az átnézés-bemenetből, `naplok/F178_visszhang_atnezes.tsv`). Nincs átnézve: a kálal (H7043) 8 modell-sora — nem lánc-szó, nem renderel — és a H6087 targumi arámi sora (az ellenőr korábbi pontosítása; nem rokon nyelv, nem renderel).
- Bemenetek (mind commitolva): `naplok/F178_kinyert_uj.tsv` (a Sonnet-kinyerés, változatlanul), `naplok/F178_kinyert_ujraolvas.tsv` (a beolvasás bemenete), `naplok/F178_visszhang_atnezes.tsv` (85 átnézett sor), `naplok/F178_lemma_megerosites.tsv` (9 megerősítés, `claude-sonnet-5-5`).
- A lapon nem renderel (127-ből): ellenőrizetlen 15 (lxx 5, bdb 10); a lánc-szón kívüli kálal (H7043) Targum-, Vulgata- és LXX-sora 3; a nem rokon nyelvi bdb sor (újhéber, targumi arámi, Sirák) és a tartalom nélküli sor a háttér-szabály szerint.

## Javítókör 1/2 (`naplok/ELLENOR_F178.md`, 2026-11-08)

*Végrehajtó: claude-opus-5-5 (kért: opus). A Targum/Vulgata-kinyerő és a lemma-megerősítő: claude-sonnet-5-5. Alap: 383bfe38.*

| ELLENOR | Tétel | Állapot |
|---|---|---|
| 1. E35 / nyílt mag (DT647) | F178.11, F178.12 | kész: a diff csak szóhasználat + ellenőrzőösszeg (20 fájl, 73/73 sor); E35 0 |
| 2. a lánc a motívumadatból (DT648) | F178.11, .15, .16, .22, .23 | kész: lánc-szó a kulcsszó (gerinc-elem), láncvers mindig a genezisi mag (1Móz 3–9) verse, ahol áll; 30 új Targum/Vulgata-sor két kézzel, 15 LXX gépi (4 nem egyértelmű, ellenőrizetlen) |
| 3. lemma-egységesítés második kézzel | F178.16 | kész: 9/9 megerősítve (claude-sonnet-5-5) |
| 4. `ellenorzes` mező, üres alak | F178.13, .16 | kész: kód + 15 teszt; a meglévő sorok újra átnézve (85 átnézett sor) |
| 5. alapvonal-mondat | F178.17 | kész: „a láncon kívüli N versből x versben (y%)”; sablon, V7 |
| 6. bontási napló | F178.18 | kész („Bontási napló”) |
| 7. λύπαις ki a 3:16-ból | F178.14 (+ .15) | kész: héber szórend szerinti kiosztás |
| 8. `ir` mező | F178.19 | kész |
| 9. sablon v4, `ad` | F178.20 | kész |
| 10. V1–V7 | F178.21 | kész |

**A javítókör saját lelete (generátor-szinten javítva, F178.15):** a görög szócsalád-tő az előtagos alak elejét („κατ”) is tőnek vette, így minden κατα-szó egy családba esett (a 6:17 és a 9:11 LXX-sorába a κατακλυσμός is bekerült); csak a 4.11 használja.

**Nyitott (a következő körre):** a LXX négy nem egyértelmű sora (H0127 1Móz 3:23, 4:2, 4:12; H7843 9:15) modell-kinyerésre vár (a `megfelelo_kinyer.py lxx` a modell-LXX-sort ma nem őrzi meg, ehhez kódváltozás kell); a chattát (H2403) rokon nyelvi háttere nincs kinyerve; az 1Móz 3:19 LXX-sorában a második γῆ a עָפָר megfelelője (a szórend-szabály a rövid jelentés eltérése miatt nem bontja).

**E5 (törölt címsor):** a HAMART-001 régi „1/b”, „5/b”, „6/b” címsorai az F178.4 átszámozásával (a felhasználó: „Számozzuk is át / ne legyen b/ alszekció”) szándékosan szűntek meg; a jelölés a javítókör záró commitjában áll.

**Kapuk (a javítókör végén):** olvasói kapu `## HAMART-001: 0 BUKÁS, 25 FIGYELMEZTETÉS`; `teszt_futtat.py --gyors`: minden fájl ZÖLD, kivéve a korábban is bukó `teszt_bdb_vers_jelentes.py`-t (bemeneti hash); `feladatok.py ellenoriz`: `197 brief, 0 hiba, 0 figyelmeztetés`; CI: E28 0, E35 0, E16 HIBA 1 (a PR-cím nem ismert).

## Javítókör 2/2 (`naplok/ELLENOR_F178_2.md`, 2026-11-08)

*Végrehajtó és átnéző: claude-opus-5-5 (kért: opus). Alap: e6b303a9 (az ELLENOR_F178_2 rögzítése). A felhasználó jóváhagyása: „Mehet” (2026-11-08).*

| ELLENOR_F178_2 | Tétel | Állapot |
|---|---|---|
| 1. a láncvers meghatározása; a gerinc az adatból | F178.26 | kész: a láncvers a motívum Pesat-gerincének azon verse, ahol a kulcsszó a héberben áll (a motívum saját verse). A gerinc (`lanc_mag`): a negatív kritérium megnevezése, különben a Pesat-sorok (`pardes_szint` ∋ Peshat) fejezet-tartománya az első Pesat-sor könyvében, Pesat-sor nélkül nincs lánc; a „teljes 1Mózes” tartalék megszűnt. A HAMART-001 4.11 táblája nem változott; a bevezető „a lánc 6 kulcsszava … (az 1.2 teljes szólistája ennél bővebb)”, „Peshat-magjának (1Móz 3–9)”. Teszt: Ez 7–12 gerincű szintetikus motívum. SEMA 2.53, MUNKAMENET C-vh, 6-os sablon 0. pont, DT648 |
| 2. az átnézés soronkénti ítélete | F178.27 | kész: 85 sor érdemi indokkal, 82 `jo`, 3 `elvet` (Vulgata 4:12 eam; H6087 újhéber II. szócikk; H7843 Tell el-Amarna jelentés). A bdb-sor átnézési kulcsa a nyelvvel és a jelentéssel (eddig a H6087 4 és a H2554 2 alak nélküli sora egy kulcson állt). Kapu: `atnezes_ellenoriz` (indok nélküli sor, kettőzött kulcs, sablonmondat), teszttel. „Második kéz (nem az ellenőr; lehet a kinyerő)” a MUNKAMENET C-vh-ban, a SEMA 2.53-ban és a kódban |
| 3. H2403 lemmaalak | F178.28 | kész a 4.11-ben és a BDB-háttérben: `strong_valtozat_versben` (TAHOT-szótő ↔ TBESH-változat), 1Móz 4:7 → H2403b חַטָּאת (chattát), teszttel; 6-os sablon 1. pont |

**Eltérés az utasítástól (1. tétel, jelezve):** a Pesat-sorok fejezet-tartománya a HAMART-001-en 1Móz 3–7 lenne (a 8:21, 9:11, 9:15 és az 5:29 sora `Remez`), vagyis önmagában megváltoztatná a 4.11-et (sáchat 6 → 4 láncvers, a 8:21 kiesne). Az adatban nincs olyan mező, amely a 3–9 gerincet közvetlenül jelölné. Ezért a sorrend: a negatív kritérium megnevezése (motívumadat, `motivumok.tsv`) előbb, a Pesat-sorok tartománya csak megnevezés híján. A lapon a „gerinc” szó nem állhat (olvasói kapu, BELSO), ezért a lap „Peshat-mag”-ot és „a lánc 6 kulcsszava”-t mond; a „gerinc-elem” és a „Pesat-gerinc” csak a belső dokumentumokban áll.

**A tábla változása (E17/DT3):** `adat/visszhang_megfelelok.tsv` 127 sor, Δ 0; 3 sor `ellenorzes`-e kiürült (vulgata 1: H0127 1Móz 4:12; bdb 2: H6087 újhéber „formába nyújt”, H7843 Tell el-Amarna). A bontási napló számai ennyivel módosulnak: vulgata ellenőrzött −1, bdb ellenőrzött 21 → 19. A HAMART-001 lapja: a 4.11 adámá-sorában „4:12 nincs ellenőrzött adat” (eddig „*is*”), a háttér-táblából a Tell el-Amarna sor kikerült, a chattát címe „חַטָּאת (chattát)”.

**Nyitott (a következő körre):**
- Vulgata 1Móz 4:12: a helyes rögzítés alak nélküli sor („nincs megfelelő szó”, mint a 4:2), ez új kinyerés és új átnézés.
- H7843 Tell el-Amarna: a jelentés javítása („leborul, elterül (? országról)”), utána újra átnézendő.
- Targum 8:21 betoldás: a sor igaz, de a betoldott szó a חוֹבָא, nem a 4:7 חֶטְאָא-ja; a lap „a lánc szavát (bűn)” mondata a jelentésbeli, nem a szó szerinti egyezést mondja ki — a mondat pontosítása generátor-kérdés.
- H2403 lemmaalak a lap többi blokkjában (1.2 szólista, 4. szótári háttér fejléce és áttekintő táblája, SECE, UBS, 5.): az általános `lemma_kiejtes` az alapváltozatot (H2403a חַטָּאָה) adja; a javítás a régi lapokat is érintené (E28), ezért a hatókörön kívül maradt.
- A korábbi kör nyitott pontjai (a LXX négy nem egyértelmű sora, a chattát rokon nyelvi háttere, a 3:19 γῆ) változatlanul nyitottak.

**Kapuk (a javítókör 2/2 végén):** olvasói kapu `## HAMART-001: 0 BUKÁS, 25 FIGYELMEZTETÉS`; `teszt_futtat.py --gyors`: minden fájl zöld, kivéve a korábban is bukó `teszt_bdb_vers_jelentes.py`-t (`test_bajtra_azonos`, bemeneti hash: `adat/bdb_forras_javitas.tsv`, e kör nem érintette); `feladatok.py ellenoriz`: `197 brief, 0 hiba, 0 figyelmeztetés`; `ellenoriz.py`: `RENDBEN: 27 | SÉRTÉS: 0 | KÉZI: 2 | JELENTÉS: 14`; `megfelelo_kinyer.py ellenoriz`: `127 sor, 0 hiba`; CI (`--diff-alap 9af7cecf --diff-fej HEAD`, commit-üzenet nélkül): E28 0 („5 migrált nézet”), E35 0, E5 HIBA 5 (a törölt „1/b”, „5/b”, „6/b” címsorok; a `TÖRLÉS-SZÁNDÉKOS:` jelölés a 7aaafed4 üzenetében áll, a PR-Action átadja), E16 HIBA 1 (üres PR-cím).
