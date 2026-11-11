# F182 — HAMART_JAVITO, 1. fázis: jelentés

*Ág: `claude/hamart-javito` (az `origin/main` 2cddb0d7-ről). Végrehajtó: claude-opus-5-5 (modell-ellenőrzés: a brief `modell: opus` mezőjével egyezik). Dátum: 2026-11-10. A fordítási lépés subagentje: claude-sonnet-5-5. Ez a jelentés nem minősíti a munkát ellenőrzöttnek; az ellenőrzés a `fuggetlen-ellenor` dolga.*

## Egyeztetett eltérés

- **Két fázis, most csak az 1.** Az orkesztrátor jelzése, a felhasználó 2026-11-10-i jóváhagyásával („mehet”). Az 1. fázis a HAMART-001 saját forrását (`motivumok/HAMART-001.md`) és adatsorait írja: határkérdések, kapcsolat-sorok, prózajavítás a forrásban, a Thayertől független fordításpótlás. Generátor, kapu, sablon és a `lexikon/` alatti lap nem változott; a lap nem generálódott újra.
- **A brief menetrendjétől eltérően** a H0 előfeltétele (#102–#105, #180 a main-ben) és a H1 (Fable-határ-ellenőrzés) nem e fázis feltétele: a határ-ellenőrzés a PR #668-ban kész volt (48 sorra), a kérdéseit (K1–K6) ez a fázis dönti el.
- **Pontosítás (orkesztrátor, menet közben):** a 2. fázis Thayer-előfeltétele a #186 (THAYER_JELENTESPONT_97, mérés és javítás) és a #187 (THAYER_KARTYA, a kétrétegű görög kártya a `lexikon_general.py`-ban; a #182 2. fázisa előtt fut, mert ugyanazt a generátort írja). A `fugg` mező nem változott.
- **Az `ir`-listán kívül írt fájlok:** `adat/elutasitasi_okok.tsv` (a HAMART saját 112-es mintája, egy alternatívával bővítve; DT-F182a), `adat/auditok.tsv` (a lekérdezések proveniencia-sorai, MUNKAMENET A5), `adat/forditasok.tsv` (a 4. lépés kimenete, a #161 lánca szerint), `adat/nyilt_kodkonyv.tsv` (egy zárt érték; a CI E35 miatt, l. 5. pont), a menet szkriptjei és a jelöltnapló a `naplok/` alatt (`F182_hatar.py`, `F182_kapcsolat.py`, `F182_kapcsolat_dontes.py`, `F182_kapcsolat_jeloltek.tsv`, `F182_proza_adat.py`), valamint a helyőrzős döntések és nyitott tételek fájljai (`dontesek/uj/hamart-javito.md`, `nyitott/uj/hamart-javito.md`).

## Elvégzett tételek

| Tétel | Commit | Idő (commit) | Lényeg |
|---|---|---|---|
| F182.0 | 6337bdba | 07:42 | fejléc: `allapot: fut`, `ag: claude/hamart-javito` |
| F182.1 | ab258f05 | 07:53 | határ: K1, K5, K6 átvezetve; K2, K3 lezárt; K4 a felhasználóé (eldőlt: F182.7) |
| F182.2 | dbdbb45e | 08:09 | kapcsolatok (F16): 103 jelölt, 56 kapcsolat-sor |
| F182.3 | 7a54418d | 08:14 | próza a forrásban: F2, F24 (a)(b), a határkör következményei |
| F182.4 | 7eb3e62c | 08:17 | TBESG-glossza: G1944, G2671, G5356 |
| F182.5 | ad7f3ee2 | 08:35 | a nyílt mag újragenerálása (CI E35), a négy új indoklás angol párja, egy kódkönyv-sor |
| F182.6 | fffe83c2 | 08:50 | jelentés, a brief fejléce: `allapot: megallt` |
| F182.7 | (ez a commit) | — | K4 alkalmazása: DT-F182d (A); a HAMART határa lezárt (F26) |

### 1. Határkérdések (`naplok/HATAR_HAMART-001.md`, 48 sor)

Minden kérdésnél előbb megnéztem, van-e rá szerkesztői döntés (`DONTESEK.md`, `jeloltek.tsv` `dontes_ref`).

| K | Előzmény | Sors | Hogyan |
|---|---|---|---|
| K1 (1Móz 4:2-3 ↔ 9:20, „földmívelő”) | nincs | **eldöntve: DT-F182a** — az 1Móz 4:2-3 kint | A negatív kritérium kizárja a „föld mint talaj” általános használatot, és megköveteli az átok kimondását, ismétlését vagy megfordítását. Mért jegy (TAHOT, 1Móz 1–9 minden H0127-verse): az 1Móz 2:5, 4:2-3 és 9:20 a földet művelés vagy foglalkozás megnevezésében hozza, átok nélkül; a bent álló 11 adámá-vers mind ítéletet mond ki vagy hajt végre. Azonos jegy, azonos sors: mindhárom kint. A 9:20 indoklása ugyanarra a szövegre igazodott. `elofordulasok.tsv` 48 → 47 sor, 56 → 54 vers. |
| K2 (Ez 12:19 bent ↔ Hab 2:8, 2:17 kint) | DT683 (B), DT685 (K3) | **lezárt** | Következetesség mérve (TAHOT, minden chámász-vers): a 13 vers, amelyben a chámász mellett a ml'-tő (ige vagy a melóá főnév) vagy a sámá áll, mind bent; a 46 szópár nélküli mind kint. Az Ez 12:19 a ml'-tő egyetlen főnévi esete. Adat nem változott. |
| K3 (Gal 3:13-14) | N116, DT686, DT687 | **lezárt, nem nyitottam újra** | A lap a sort „Határeset: a kapcsolat az áldás-mondaton át” funkcióval és a „Határesetek” listán (közepes) mutatja; olvasható. Megjegyzés: a felhasználó „tematikus kapcsolat”-nak nevezte, az adat „határeset”-nek (a G1944 a versben áll, ezért nem „tematikus, nem lexikai” sor). |
| K4 (Ez 28:16, Mik 6:12, Sof 1:9: a szópár a föld nélkül) | nincs | **lezárt: DT-F182d (A), a felhasználó döntése** (2026-11-10, az orkesztrátor továbbításában: „a”) | A szópár (málé + chámász, illetve sámá + chámász) önmagában elég: a formula az 1Móz 6:11-13 szava, maga utal vissza. A sorok maradnak. Az öt vers (Ez 28:16, Mik 6:12, Sof 1:9, Jer 6:7, Hab 1:2) indoklása (`jeloltek.tsv`) és 1/a prózája (`elofordulasok.tsv`) ezt kimondja (`naplok/F182_k4.py`, összevetéssel). A sámá-soroknál pontosítva: az 1Móz 6:11 és 6:13-ban a chámász a málé igével áll (TAHOT: H2555 + H4390), a sámá nem; ott az indoklás azt mondja, hogy az erőszak szava az 1Móz 6:11-13 szava, a „hallatszik az erőszak” pedig a lánc szópárja. A nyílt mag és az öt indoklás angol párja frissítve (Sonnet; két helyen a „voice of the earth” félrefordítást „word for the earth”-re javítottam: `claude-sonnet-5-5; javítás: claude-opus-5-5`); a nyílt mag kapuja 0 BUKÁS. |
| K5 (1Móz 6:5 ↔ Jer 17:9 „jetzer”) | DT683 (E), DT685 (K8) | **lezárt; az indoklás frissítve: DT-F182b** | A sor marad. Az elavult indoklás (a kivezetett רַע szóra épült) helyett: a vers a 6:7 ítéletének indoka ugyanabban az elbeszélésben, és a bent álló 8:21 ugyanezt az indokot mondja ki; a Jer 17:9, Jer 4:14, Mt 15:19, Mk 7:21-23 a lánc elbeszélésén kívül áll. |
| K6 (Gal 3:14, Zsid 6:7 a tartományban ↔ Róm 8:20 kint) | DT686 (Gal), DT685 (K10, Róm) | **Gal és Róm lezárt; Zsid: DT-F182c** | Szabály a két lezárt döntéssel összhangban: a tartomány addig tart, ameddig a hely állításához szükséges rész áll. A Zsid 6:8 igenévi mondatának alanya (γῆ) a 6:7-ben van (TAGNT; Károli: „A mely pedig …”), a Róm 8:21 maga hordozza az alanyt (κτίσις) és a φθορά szót. Csak a Zsid 6:7-8 indoklása változott. |

Írás: `naplok/F182_hatar.py` (soronkénti összevetés az eredetivel; csak a megnevezett mezők változhattak). `ellenoriz.py`: 0 SÉRTÉS. A 39. szabály jelzi, hogy a határ-ellenőrzés modelles része a 48 soros állapotra készült (ma: 47). **A HAMART határa lezárt (F26): nem lesz újabb modelles határ-kör**; a 39. szabály JELENTÉS-e ezért ismert, elfogadott eltérés (a K1–K6 döntései: ez a jelentés és a `dontesek/uj/hamart-javito.md`).

### 2. Kapcsolatok (F16)

A HAMART-001-nek eddig 0 sora volt az `adat/kapcsolatok.tsv`-ben.

- **Jelöltek** (`naplok/F182_kapcsolat.py`): a 47 sor 54 versére a TSK és a Károli-KH (`lekerdez.py tsk` / `karoli`, MUNKAMENET A5; 154 proveniencia-sor az `adat/auditok.tsv`-ben, 0 találatnál is), a lap 1/a prózájának igehely-hivatkozásai (`manual`) és a tematikus sorok `gerinc_elem`-je. **103 jelölt pár**; mindegyik mellett a mért bizonyíték: közös lánc-szó és lánc-szópár (TAHOT/TAGNT), a nyelvközi párokon LXX-híd és görög szócsalád (`lekerdez.py lxx-hid`), és a szó szerint visszatérő, nem köznapi szavak.
- **Döntés** (`naplok/F182_kapcsolat_dontes.py`, DT-F182e): a bizonyosság a mért bizonyítékból, szabály szerint (a szabály a szkript docstringjében és a DT-ben); a típus és a funkció kézi. **56 sor beépítve** (26 magas, 30 közepes; Párhuzam 43, Kontraszt 7, Variáns 6; PaRDeS-szint Remez), **47 elutasítva** indokkal: 30 közös bizonyíték nélkül (csak tematikus rokonság), 8 küszöb alatt (egy szó, 1–2 TSK-szavazat), 9 redundáns (két nem genezisi hely ugyanazzal a szópárral, amely mindkettőt a genezisi forrásvershez köti). A döntés és az indok jelöltenként: `naplok/F182_kapcsolat_jeloltek.tsv`.
- A lánc fő ívei a táblában: 1Móz 3:17 → 4:10-11 (Variáns), → 5:29, → 8:21 (Kontraszt), → 5Móz 28:18; 6:11 → 6:13 és az ezékieli „megtelt erőszakkal” helyek; 6:12 → 6:13 (Variáns, tükörítélet); 6:5 → 8:21 (Kontraszt); 6:17 → 9:11 (Kontraszt); 1Móz 3:18 → Hós 10:8, Zsid 6:7-8; 12:3 → Gal 3:13-14 (közepes, határeset).
- A meglévő 32 kapcsolat-sor bájtra változatlan (a szkript összeveti).
- **N-F182a:** a `jeloltek.tsv`-ben nincs igehely-pár jelöltfajta (SEMA 2.3 „a küszöb alatti sor a jeloltek.tsv-ben marad” ↔ 2.4 `jelolt_tipus`: csak `elofordulas`, `motivumkozi`); a jelöltnapló ezért a `naplok/` alatt áll.
- A K4 az (A)-ra dőlt: az Ez 28:16, a Jer 6:7 és a Hab 1:2 kapcsolat-sora marad (a Mik 6:12 és a Sof 1:9 a redundancia-szabály miatt nem kapott sort).

### 3. Próza a forrásban

A `motivumok/HAMART-001.md` egészét és a 47 sor 1/a prózáját elolvastam, mielőtt belenyúltam.

- **F2:** az 1Móz 7:23 1/a prózája a teljes Károli-tagmondatot idézi („csak Noé marada meg, és azok a kik vele valának a bárkában”), a funkció: „csak Noé és a vele lévők maradnak meg a bárkában” (`adat/elofordulasok.tsv`, `naplok/F182_proza_adat.py`).
- **F24 (a):** a „három, egymástól független keresés” helyett a valós viszony áll: a keresések közös szavakból indulnak, ezért az egybeesésük nem független megerősítés. A „független határ-ellenőrzés” címe is tárgyszerű lett („A határ második ellenőrzése”).
- **F24 (b):** a Sod-zárás a motívum saját leletéből áll: a lap egyik helye sem vonja vissza az átok igéjét ugyanazzal az igével (az 1Móz 8:21-ben qalal áll, a Jel 22:3-ban κατάθεμα); a lánc az áldás szavával ér véget (1Móz 12:3). A lapok közötti sablonmondat („A motívum legmélyebb rétege ezért az a remény …”) kikerült.
- **A határkör következményei:** 47 hely, 54 vers, 23 genezisi sor; a tartomány szabálya a „Tartományok” bekezdésben; az 1Móz 4:2-3 kikerült a Peshat-mondatból és a H0127 szótári bekezdéséből; a határ második köre a Módszertanban; a forrás NAPLO-blokkja rögzíti a menetet.
- A Károli-idézetek gépi összevetése (minden „…” idézet a `Karoli_1908.tsv`-ben): a „fáradságos munka” a Károli-alakra javult („fáradságos munkával”); más eltérés nincs (a „Proveniencia”/NAPLO-blokk és a fogalmi idézőjelek nem Károli-idézetek).
- A leletlista többi forrásszintű tétele **generátort vagy kaput is érint**, ezért a 2. fázis listáján áll (F17 az `alkalmazas` rés kivezetésével együtt; F4 indoklás-javítása az `elutasitasi_okok.tsv` mintáival és az új kapuval együtt).

### 4. Fordításpótlás (Thayer nélkül)

- A #161 lánca (`eszkozok/glossza_api_koteg.py`, prompt glossza v2), mérés nélkül: `lista` → a három TBESG-egység → `szaraz` (1 kérés) → `prompt` → general-purpose subagent, **claude-sonnet-5-5**, a kérés szó szerint → `bevesz` → `kapuz` (3/3 átment, mankó-jelzés 0) → `rogzit` → `beir`.
- `adat/forditasok.tsv`: 3 új sor — G1944 ἐπικατάρατος: „átkozott”; G2671 κατάρα: „átok”; G5356 φθορά: „megromlás” (`allapot` sonnet).
- Mellékhatás, visszaállítva: a `glossza_lexikon_forditas.py lista` a `naplok/F121_GLOSSZA_FORDITAS_lista.tsv`-t is átírja; nem része a menetnek, a változást visszaállítottam.
- **Vár (a #186/#187 után):** a Thayer-sorok (G1311, G2671, G5351, G5356 elavult; G3077), és a G3077 (λύπη) TBESG-glosszája.

### 5. A nyílt mag (a CI E35 szabálya miatt)

Az `adat/*.tsv` változásával a commitolt `nyilt_mag/` az újragenerált exporttal bájtazonos kell legyen (E35, HIBA), ezért a nyílt mag ebben a fázisban újragenerálódott (`python eszkozok/nyilt_mag_export.py`; a `nyilt_mag/*` a brief `ir`-listáján áll).
- `adat/nyilt_kodkonyv.tsv`: egy új zárt érték a `kapcsolatok.tsv` / `forras_megnevezes` oszlophoz („a projekt saját mérése és naplója”, a `motivum_kapcsolatok.tsv` azonos sorának angol címkéjével). Nélküle az export megállt az 56 új kapcsolat-sornál.
- `adat/nyilt_angol.tsv`: a négy megváltozott HAMART-indoklás (1Móz 4:2-3, 1Móz 6:5, 1Móz 9:20, Zsid 6:7-8) angol párja; general-purpose subagent, claude-sonnet-5-5, `nyilt_mag_angol.py betolt`. A nyílt mag kapuja (`nyilt_mag_kapu.py`) előtte 3 BUKÁS (elavult fordítás), utána **0 BUKÁS**, 19 FIGYELMEZTETÉS (a meglévő jellegűek).
- A kapcsolat-sorok `funkcio` és `indoklas` mezője a nyílt mag szabad szöveges oszlopai között nem szerepel, ezért angol párjuk nem kell.

## Nyitott kérdések a felhasználóhoz

1. **K4 (DT-F182d): eldőlt, (A)** (a felhasználó, 2026-11-10: „a”). Nyitva marad egy szerkesztői javaslat: a negatív kritérium második mondatának pontosítása („… vagy a lánc szópárja, amely maga az 1Móz 6:11-13 szava”); a `motivumok.tsv` szövegét ez a fázis nem írta át.
2. **K1 (DT-F182a, tájékoztatás):** az 1Móz 4:2-3 kivételét a negatív kritériumból vezettem le. A HAMART határa lezárt (F26); ha a szerkesztő mégis a (b)-t választaná, a `naplok/F182_hatar.py` visszafordítható.
3. **N-F182a:** a kapcsolat-jelölt helye: új `jelolt_tipus`, vagy a `naplok/` alatti jelöltnapló a rögzített út.

## A 2. fázis listája (tétel → érintett fájl → előfeltétel)

*A 2. fázis a generátort, a kapukat és a lapot írja. Közös feltétele: a #104 a main-en (`lexikon_general.py` és kapuk) és a #187 a main-en (ugyanazt a generátort írja). A sorhalmaz végleges (K4 eldőlt, a határ lezárt: F26). A lap újragenerálása az utolsó lépés.*

| Tétel | Érintett fájl | Előfeltétel |
|---|---|---|
| F1 — a 2. szakasz összegző következtetése (súlypont, szövetség-arány) | `eszkozok/olvasoi_kovetkeztetes.py`, `eszkozok/teszt_olvasoi_kovetkeztetes.py`, `sablonok/6_*` | #104, #187 |
| F3 — a kizárások teljes listája mellékletlapon; a blokk-tagok az adatrétegbe; a 1 717 ↔ 1 754 számeltérés mérése | `eszkozok/lexikon_general.py`, új adattábla + `adat/SEMA.md`, `nyilt_mag/*` | #104, #187 |
| F4 — az indoklás-mezők névelője és átírása (héber/görög írás + zárójeles kiejtés); a kapu; az angol nyílt mag újrafordítása | `adat/jeloltek.tsv`, `adat/elutasitasi_okok.tsv` (a minták az indoklás szövegére illeszkednek), `eszkozok/olvasoi_kapu.py` + teszt, `adat/nyilt_angol.tsv` | #104 (kapu); az adatjavítás a kapuval együtt, hogy a minták és a szöveg egy lépésben változzanak |
| F5 — a görög tokenek bekötése a szótári hivatkozástáblába; az üres-blokk olvasói mondata | `adat/lexikon_hivatkozasok.tsv`, `eszkozok/lexikon_general.py` | #104, #187 (a TBESG-glossza az 1. fázisban kész) |
| F6 — a 4.3 tW-címek magyarul, slug nélkül | `eszkozok/lexikon_general.py`, `eszkozok/olvasoi_kapu.py` | #104, #187 |
| F7 — a 4.9 összegzése (héber és görög), kis elemszámnál következtetés nélkül; a 4.9 tömörítése egy táblázatba (F25) | `eszkozok/olvasoi_kovetkeztetes.py` + teszt, `sablonok/6_*` | #104, #187 |
| F8 — a „Héber/Görög szavak” bevezető mondata írással és kiejtéssel | `eszkozok/lexikon_general.py` | #104, #187 |
| F9 — a H2403 BDB-szakaszhatára; az „ellenőrzendő” szakasz nem renderel; BDB-rövidítések a Jelmagyarázatba | BDB-adattáblák, `eszkozok/lexikon_general.py` | #105, #185 |
| F10 — a BDB-blokkok megjelenítése (ismétlődő bevezető, glosszás csukott címek, belső azonosítók, nyers fej) | `eszkozok/lexikon_general.py`, BDB-adat | #104 (a kártya), #105, #185 |
| F11 — a 4.6 LXX-összegző mondata | `eszkozok/lexikon_general.py` (`lxx_olvasoi*`) | #104, #187 |
| F12 — a 4.7 SECE-mondat (hibás, ismétlődő következtetés) és a kapu | `eszkozok/lexikon_general.py`, `eszkozok/olvasoi_kapu.py` | #104, #187 |
| F13 — a rokon nyelvi tábla a 4.8-ba (a DT639 módosítása) | `eszkozok/lexikon_general.py`, `eszkozok/visszhang/megfelelo_kinyer.py`, `sablonok/6_*` | #104, #187 |
| F14 — 4.13 Károli-megfelelők, 4.14 rejtett/hamis párhuzam (új generátor-rész) | `eszkozok/szerep_karoli.py` + teszt, `adat/szotar_szerepek.tsv` | #104, #187; a #172 döntése (a párosítás mért pontossága) |
| F15 — az 5. szakasz LXX-forrása a gépi társítás; a kapu | `eszkozok/lexikon_general.py`, `adat/visszhang_megfelelok.tsv` | #104, #187 |
| F16 (b) — az üres Kapcsolatok-szakasz egy mondata (a HAMART-on már nem üres) | `eszkozok/lexikon_general.py` | #104 |
| F17 — az `alkalmazas` rés kivezetése; a forrás 5. pontja archívumba | `eszkozok/lexikon_general.py`, `adat/res_forras.tsv`, `motivumok/HAMART-001.md`, `archivum/HAMART-001/`, `sablonok/6_*`, `9_*`, `10_*`, `CLAUDE.md`, `MUNKAMENET.md` | #104 |
| F18 — az azonosító tábla a lap elejére; a státusz a kiadási állapotból | `eszkozok/lexikon_general.py`, `sablonok/6_*` | #104 |
| F19 — a HAMART BDB-hozzárendeléseinek laponkénti ellenőrzése | BDB-adat | #185 (97% után a LEXIKON_PROGRAM szerint okafogyott); ha nem, a #104 után |
| F20 — a közel-keleti határ mondata a Módszertanba | `eszkozok/lexikon_general.py`, `sablonok/6_*` | #104 |
| F21 — a Thayer-sorok (G1311, G2671, G5351, G5356 elavult; G3077) és a G3077 TBESG-glosszája | `adat/forditasok.tsv` | #186, #187 |
| Görög 4.2 (a kétrétegű kártya) | `eszkozok/lexikon_general.py` | #186, #187 |
| F22 — munkaszó- és szakaszszám-kapu | `eszkozok/olvasoi_kapu.py`, `eszkozok/ellenoriz.py` + tesztek | #104; a #184 szabálylistája |
| F24 (c) — nyers proveniencia-sor, „↳ Alpont:” címke, a „tematikus, nem lexikai” címke olvasói alakja; az U3-sablon tiltásai (a „független” szó közös bemenetnél, az ismétlődő zárómondat) | `eszkozok/lexikon_general.py`, `eszkozok/olvasoi_kapu.py`, `sablonok/10_*` | #104 |
| F25 maradéka — a 2. táblázat „(nincs címke: 1.b)” cellája, a lábjegyzetek olvasói nyelve, a kártya bekapcsolása | `eszkozok/lexikon_general.py` | #104, #105, #185 |
| N-F178a/b, N108 (a csukott cím glosszája) | `eszkozok/lexikon_general.py` | #104 |
| H4 — jelölő-kapu a `/kiadas` előtt; előfeltétel-térkép a MUNKAMENET-ben | `eszkozok/olvasoi_kapu.py` / `eszkozok/ellenoriz.py`, `MUNKAMENET.md` | #104 |
| H5 — a #38 záró ellenőrzésének hiánya ismert korlátként a Kolofonban | `eszkozok/lexikon_general.py` | #104 |
| A nyílt mag frissítése a 2. fázis adatváltozásaival (az 1. fázisé kész: F182.5); az F4-javítás után az indoklások angol párja újrafordul | `nyilt_mag/*`, `adat/nyilt_angol.tsv` | a 2. fázis adatváltozásaival együtt (E35) |
| A lap újragenerálása, saját renderelt átnézés, független ellenőr (H6) | `lexikon/HAMART-001_TUDOMANYOS.md` | a fenti tételek; #104, #105, #185, #186, #187 |

## Ellenőrzés a menet végén

- `python eszkozok/ellenoriz.py` (az F182.7 után): **1 SÉRTÉS**, a 11. szabály („Rés-forrás egyezés”): a lap négy rése (`kivonat`, `miert_fontos`, `ertelmezes`, `modszertan`) eltér a forrástól, mert az F182.3 a `motivumok/HAMART-001.md` prózáját javította, a lap viszont az 1. fázisban nem generálódhatott újra (a `lexikon/` alatt semmit nem írtam). Az F182.1–F182.2 utáni futás még 0 SÉRTÉS volt; az F182.3 után nem futtattam újra, ezért ez csak most derült ki. **Döntés kell (orkesztrátor):** (a) a lap újragenerálása már most (a lexikonlap-tilalom alóli kivétel, csak a rések frissülnek); (b) a CI-hiba vállalása a 2. fázisig (a PR addig nem mergelhető); (c) a forrás prózajavításának visszavétele a 2. fázisig. Javaslat: (b), mert a PR úgyis a 2. fázissal együtt zárul, és a lap a 2. fázisban egyszer generálódik újra. A 39. szabály JELENTÉS-e a lezárt határ ismert eltérése (F26).
- `python eszkozok/nyilt_mag_kapu.py`: 0 BUKÁS. A CI-futtató (`eszkozok/ellenorzes/futtat.py`) helyben: az F182.2 utáni futás egyetlen hibát adott (a kódkönyv hiányzó zárt értéke, az F182.5 javította); a teljes ágra indított futás 25 perc után időtúllépéssel megállt, eredmény nélkül. A teljes CI a GitHubon fut a push után.

## 2. fázis (2026-11-11)

*Végrehajtó: claude-opus-5-5 (modell-ellenőrzés: a brief `modell: opus` mezőjével egyezik). Az orkesztrátor 07:42-kor indította; a session 07:42:46-kor kezdett. A fordítási lépés subagentje: claude-sonnet-5-5 (saját kiírt modellneve). Ez a jelentés nem minősíti a munkát ellenőrzöttnek; az ellenőrzés a `fuggetlen-ellenor` dolga.*

### Egyeztetett eltérés és hatókör

- **Hatókör: az orkesztrátor 2026-11-11-i döntései (1–7. tétel)**, nem az 1. fázis végén álló teljes 2. fázis-lista. Az F1, F3–F21, F24 (c) (1), H4 (b), H5 és N-F178a/b e menetben nem készült el (az orkesztrátor menet közben befagyasztotta a hatókört: új tétel nincs, a HAMART lapon látható hiba javítandó). Ezekből a lapon látható hibát javítottam (F182.21, F182.23: az F25 maradékának „(nincs címke: 1.b)” cellája, a hamis „nem található” kutatói megjegyzés, a törött felsorolás).
- **A main beolvasztása:** az origin/main közben a `f66f0fcc`-ig (számkiosztás) lépett; azt olvasztottam be (a `2597e341` utódja). Az `adat/jeloltek.tsv` és az `adat/elofordulasok.tsv` ütközése: a main a közös ős óta csak számot osztott, ezért a sorok az ág szerint, a main végleges számaival maradtak (a helyőrzők a main szamkiosztas-leképezése szerint cserélve); a nyílt mag generált fájljai a main szerint, majd újragenerálva (F182.22).
- **`.claude/agents/hatar-ellenor.md` (F26 (b)): nem írtam.** A fájl Claude-konfiguráció; ügynöki üzenet nem hagyhatja jóvá a módosítását. A szabály kanonikus helye (a `9_` sablon „hét szabály” 2. pontja) kész; az ügynökfájl egysoros hivatkozása a felhasználó jóváhagyásával vehető fel.

### Tételek (mi kész, hogyan)

| Tétel | Commit | Generátor / kapu / teszt |
|---|---|---|
| F33 — a tagolás a szakasztáblából, egy forrásból | F182.10 | új közös modul `eszkozok/bdb_tagolas.py` (a kártya `bdb_gerinc_szocikkek`-je delegál, kimenete bájtra azonos; az olvasó `_bdb_bontas`-a a szakasztábla fáját mutatja, a szeletelő csak a fej szövegét elemzi); a kártya fán kívüli pontja „nem azonosítható” (`fan_kivuli_pontok`); teszt: `teszt_bdb_tagolas.py` (a HAMART minden 2.29-pontja a fában, a kártya és az olvasó ugyanaz a fa, repó-szintű regresszióőr: 440 fán kívüli, 5 368 nem egyértelmű pont; N-F182b, N-F182c) |
| N-F185c (N141) | — | a könyvnév nélküli hely `orokles_hibas` okkódja a kártyán és az olvasóban gyenge jelölés (`bdb_vj_szabaly`, a #185 kódja); a HAMART lapon nincs ilyen pont |
| F25 — a kapcsolók | F182.11 | `KETRETEGU_BDB_KARTYA` = {HAMART-001}; a `BDB_BETU_JAVIT` motívumhalmaz (egy hely), = {HAMART-001}; a régi lapok kikapcsolva; teszt: `teszt_szotari_gerinc` |
| 6. tétel — a `ketes` jelentéspontok | F182.12 | egyetlen kétes pont állt a lapon (l. lent); `jp_kezi` a `JELENTESPONT_KEZI`-ben; 2.29 újragenerálva azonos `--ts`-sel (csak a fejléc kód-hash-e és a sor változott); DT-F182f |
| F22 (a)(b), H4 (a), F24 (a)(c), F35 | F182.13 | `olvasoi_kapu.MUNKASZO` (a lista egy helyen: `MUNKASZAVAK`; új szerkezetű lapon BUKÁS, régin FIGYELMEZTETÉS) és `SZAKASZ_HIV`; a generátor új szerkezetű olvasói átírása (`UJ_OLVASOI_MUNKASZO`, a régi lapok szövege változatlan; DT-F182h); U3-sablon tilalmai; SEMA 3.11 újragenerálva; a mért BDB-pontosság a SEMA 2.29-ben (módszertan), a lapon és az olvasóban nem; „tematikus, nem lexikai” címke marad (DT-F182g); tesztek: `MunkaszoSzakaszHiv`, `HamartLapMunkaszo` (a rontott másolat jelez) |
| F27 — elavult DT nem kerül lapra | F182.13 | jelölés a `DONTESEK.md` fejében (⛔ + `**FELÜLÍRVA → DT<n>**` / `**VISSZAVONVA**` / `**OKAFOGYOTT**`; DT-F182i), olvasó: `eszkozok/dontes_allapot.py`; a generátor a felülíró döntés dátumát írja (`ervenyes_dontes`); a 21. szabály SÉRTÉS érvénytelen DT-re; teszt: `teszt_dontes_allapot.py` (a rontott állapot jelez). A meglévő 79 szöveges „felülírt/elavult” előfordulást nem minősítettem át (tartalmi döntés) |
| F26 — a határ-kör lezárása | F182.14 | a szabály a `9_` sablon 2. pontjában; `ellenoriz.py` HATÁRDÖNTÉS-jel (DT/N nélküli ujjlenyomat, a számkiosztásnak ellenáll), a `--hatar-ujjlenyomat` kiírja a sablonját; a HAMART jele a modelles rész végén (DT-F182a–d, DT683, DT685–DT687); a 39. szabály a HAMART-ra friss; teszt: `teszt_muhely_allapot.TesztHatarFrissesseg` |
| F28 — a nyílt mag lyukai | F182.15 | a feloldatlan DT olvasói mondatrészre íródik („egy korábbi szerkesztői döntés”, raggal), a határ-ellenőrzés jegyzőkönyve „határ-ellenőrzés”, a `gerinc_elem` ragos alakja „motívumszava”, az egymondatos vágás zárójelen kívül; `nyilt_mag_kapu` LYUK (BUKÁS); teszt: `teszt_nyilt_mag.F28Lyuk` |
| F29/F34 — N137, N139 | F182.16, .16b | N137: a kártya csukott vázlatsora „…”-re végződik, ha a szakasz folytatódik; N139: a közös glossza-szabály a forrás-besorolás, a „+ <héber> <nyelvtani>:” és a héber kifejezés előtagot levágja (H2403 1.f „a pap engesztelést szerez valakiért”, H7451 6. „rosszabb”, 8. „gonosz tervet kigondolni”); N138 = F33; teszt: `F182Glossza` |
| F31 — fordítás-pótlás | F182.17 | a lista a `forditasok.tsv` `allapot`-ából: a HAMART 15 Strongjára minden Thayer-szakasz, TBESG-glossza és BDB-szakasz érvényes fordítással áll — fordítandó 0, a subagent nem futott (a G3077 nem a HAMART Strongja); közös őr: `eszkozok/forditas_vedelem.py` (érvényes, azonos forrású sor nem fordul újra; a TBESG-, Thayer- és BDB-lánc beíró lépése hívja); 42. szabály (a lapon szereplő Strong érvényes fordítása a lapon áll; új szerkezetű lapon SÉRTÉS); teszt: `teszt_forditas_vedelem.py` |
| F32 — Károli-versszámozás | F182.18, .19 | a kártya kutatói rétegében a BDB-szöveg hivatkozása a 2.29 átkulcsolt sorai szerint Károli-számmal, az eredeti jelölésével („5Móz 29:21 (héber számozás: 29:20)”), könyv- és fejezet-örökléssel; a Károliban nem létező versre mutató hivatkozás átirányítás nélkül, gyenge jelöléssel (orkesztrátori keret); egy parser (`szotari_hivatkozasok`) a megjelenítéshez és a 43. szabályhoz (JELENTÉS); a HAMART lapon 21 átszámozott, 8 jelölt hivatkozás (N-F182e); teszt: `F182KaroliSzamozas`. A Thayer-tábla a HAMART görög szavain számeltérést nem rögzít |
| 7. tétel — a lap újragenerálása | F182.20, .21, .23 | `general.py --cel lexikon --id HAMART-001 --ir`; a 27. szabály mintája az olvasható szócikkfejet is felismeri (a kártya bekapcsolásával előjött téves SÉRTÉS); látható hibák javítva a generátorban (l. lent) |
| A nyílt mag (E35) | F182.22 | újragenerálva; 39 szöveg (45 cella) angol párja a meglévő láncon (claude-sonnet-5-5); állapot: 1039 cella, hiányzó 0, elavult 0; kapu 0 BUKÁS |
| Látható hibák a lapon (befagyasztás 1. pont) | F182.21, .23, .24 | a Jelentés cella hiányjelei, a hamis „nem található” megjegyzés, a „- 2.” felsorolás; **A01**: az Alátámasztás „nincs rögzített kapcsolat” hamis mondata (a rögzített hiány-mondat csak adat híján áll; a rés az 56 kapcsolat-sorból renderel; teszt: `ResTorzsAdatAg`) |
| Olvasó: literális SQL | F182.25 | `TestSzabalyok.test_nincs_osszefuzott_sql` |
| A04 — H2403 lemma-változat | F182.26 | a motívum szövegéhez illesztett TBESH-változat (חַטָּאת, chattát); csak új szerkezetű lapon |
| A main beolvasztása (#683) | F182.27 | ütközés nélkül; a `sablonok/KESZ_LAP_KOVETELMENY.md` ezután az elsődleges |

### A `ketes` jelentéspontok sorsa (egyenként)

A bekapcsolt kártyán a lap egyetlen kétes pontot mutatott:

| Szó | Hely | Pont | Ok | Sors |
|---|---|---|---|---|
| H7451 רַע (ra) | 1Móz 6:5 | első szócikk, 10.c („gonosz (a szív gondolatairól)”) | `ketes:jp_tanu_elter` (a szeletelő mint tanú más pontot adott) | **igazolva** — a DictBDB szövege: „c. of thoughts, יֵצֶר Gen 6:5; 8:21 (J), …” (a 2.30 BDB8032 15. sora, `-/10/c`); `jp_kezi` tétel a `JELENTESPONT_KEZI`-ben, a sor `biztos` (DT-F182f) |

A H7451 1Móz 6:5 `fej`-sora (2.29, poz 175 és 6238) nem jelenik meg pontként (a kártya a fejet elhagyja, ha a versnek más pontja is van). Gyenge jelölés a lapon ezután nem maradt.

### A lapdiff ellenőrzése (origin/main → ág; `lexikon/HAMART-001_TUDOMANYOS.md`: +740 / −330 sor)

- **DT-hivatkozások:** a lapon DT199, DT564, DT683, DT685, DT686, DT687 áll (látható alakban „szerkesztői döntés, <dátum>”) — mind érvényes a `DONTESEK.md` szerint (`dontes_allapot`: 0 érvénytelen); a 21. szabály (iv) 0 lelet. A DT-F182d helyőrző csak HTML-megjegyzésben (eredeti proveniencia-sor) áll; a 21. szabály (i) ágon JELENTÉS, a számkiosztás a merge után cseréli.
- **Munkaszavak:** a látható szövegben 0 (MUNKASZO kapu). Előtte a próbalapon: „üres blokk: javaslat” 2, „kutatói jelölés … ellenőrzendő” 1, „függőben” 19, „azonosításra vár” 8, „nincs bekötve” 1, „audit” 15, „token” 9 — a generátor új szerkezetű olvasói átírása kezeli. „gerinc”, „orkesztrátor”, „felhasználó” a látható szövegben nincs (BELSO kapu); „felhasználó” csak HTML-megjegyzésben.
- **Számok:** 47 hely, 54 vers (Kivonat, 1. tábla, Döntési út összeadás — a 40. szabály szerint egyezik); az „1 756 verset” a 3. szakasz számlálása (az F3 1 717 ↔ 1 754 eltérés-mérése nem e menet tétele).
- **Látható hibák a renderelt lapon (saját átnézés), generátorban javítva:** (1) a 2. tábla Jelentés cellája „*(nincs címke: 1.b)*” / „*(nincs hozzárendelés)*” → „Isten ellen · 1.b”, „a szócikk egésze — fájdalom, fáradság”, Strong nélküli sornál „—”; (2) a H2555 kutatói megjegyzése a tagolatlan szócikk pontjait hamisan „az útvonal nincs a szakasztáblában”-nak mondta → elmarad; (3) a kártya nem félkövér „- 2. …” sora üres felsorolásjelként, beágyazott listaként renderelt → „2\.”. Tesztek: `F182LathatoHibak`.
- **Maradt (nem hamis állítás, FIGYELMEZTETÉS):** „*(nincs görög szó)*” a Jel 22:3 tematikus sor UBS-cellájában (igaz állítás); KIVONAT_SZAM 2 (téves: „47 hely 54 versben”); a 8 nem létező Károli-versre mutató szótári hivatkozás gyenge jelöléssel (N-F182e).

### Mérési sorok

*Modell: claude-opus-5-5 (a fordításnál claude-sonnet-5-5); effort: nem látható; a keret %-a előtte és utána: nem látható. Idő: a commitok ideje (`git log`), a kezdés a session indulása.*

| Lépés | Kezdés | Vége | Idő |
|---|---|---|---|
| merge, modell-ellenőrzés, fejléc (F182.8–.9) | 07:42 | 07:45 | 3 perc |
| bemenet és állapot olvasása, felmérés | 07:45 | 07:50 | 5 perc |
| F33 (közös modul, kártya, olvasó, teszt) | 07:50 | 08:02 | 12 perc |
| F25 kapcsolók | 08:02 | 08:05 | 3 perc |
| 6. tétel (ketes pont) | 08:05 | 08:07 | 2 perc |
| F22/H4/F24c/F27/F35 (kapuk, átírás, döntés-érvényesség) | 08:07 | 08:19 | 12 perc |
| F26 | 08:19 | 08:22 | 3 perc |
| F28 | 08:22 | 08:27 | 5 perc |
| F29/F34 (N137, N139) | 08:27 | 08:32 | 5 perc |
| F31 | 08:32 | 08:40 | 8 perc |
| F32 (az orkesztrátori kerettel együtt) | 08:40 | 08:48 | 8 perc |
| a lap újragenerálása, 27. szabály, látható hibák (F182.20–.21) | 08:48 | 08:56 | 8 perc |
| nyílt mag + angol pár (subagent: kb. 1 perc) | 08:56 | 09:00 | 4 perc |
| lapnézet, saját átnézés, a törött felsorolás javítása (F182.23) | 09:00 | 09:05 | 5 perc |
| teljes tesztkör, `ellenoriz.py`, olvasó-tesztek friss adatbázison, jelentés, push | 09:05 | 09:35 | 30 perc (benne az alapvonal-futás, az adatbázis-építés és a két késői lapjavítás: F182.24–.26) |

### Tesztek és `ellenoriz.py`

- **`python eszkozok/ellenoriz.py`** (a lap újragenerálása után): kilépési kód 0 — **0 SÉRTÉS**, RENDBEN 26, JELENTÉS 17, KÉZI 2. A **11. szabály RENDBEN**: az 1. fázis után fennmaradt rés-forrás SÉRTÉS a lap újragenerálásával megszűnt. A 21. szabály JELENTÉS (ág: a DT-F182d helyőrző a lap HTML-megjegyzésében), a 39. JELENTÉS (más motívumok üres modelles része; a HAMART friss a határdöntés-jellel), a 42. JELENTÉS (régi lapok), a 43. JELENTÉS (HAMART: 8 szótári hivatkozás, N-F182e).
- **Olvasói kapu (HAMART-001):** 0 BUKÁS. **Nyílt mag kapu:** 0 BUKÁS.
- **Windows-tesztkör** (`eszkozok/teszt_*.py`, 79 modul, modulonként `python -m unittest`): a bukó modulokat tesztnevenként összevetettem az `origin/main` alapvonalával (külön worktree, ugyanazok a modulok). **Csak az ágon bukik:** `teszt_ellenoriz_vedokorlat.ValodiAdat.test_20_21_a_repon` és `teszt_nyilt_mag.Pozitiv.test_nincs_nyitva_sor_es_nincs_feloldatlan_dt` — mindkettő a DT-F182 helyőrzők ági állapota (a 21. szabály „main” módban SÉRTÉS-nek veszi a helyőrzőt; az export feloldatlan DT-t jelez); a merge utáni számkiosztás megszünteti. A többi bukás (bdb_adatblokk, bdb_zaras, general_ellenorzo, general_kinyeres, jelolt_eloszures, lektor_kerdesek, lexikon_adatres, olvasoi_kapu Arany.G7, render_diff_osztalyoz, szakasz_cimke_levezet, szerep_karoli, szerep_nave, szerepmatrix, glossza_api_koteg, thayer_api_koteg, emeles relpath, szotari_gerinc 6) az alapvonalon is bukik. Az e menetben írt tesztek mind zöldek (`teszt_bdb_tagolas`, `teszt_dontes_allapot`, `teszt_forditas_vedelem`, `MunkaszoSzakaszHiv`, `HamartLapMunkaszo`, `F28Lyuk`, `TesztHatarFrissesseg`, `F182Glossza`, `F182KaroliSzamozas`, `F182LathatoHibak`, `ResTorzsAdatAg`).
- **Olvasó-tesztek** (`teszt_olvaso_szerver.py`, a munkafa kódjával, WSL-venv, a munkafa adatából épített friss `pardes.db` — a `~/pardes` klón régi, ezért a `teszt_futtat.py` helyett közvetlenül): 111 teszt, 3 bukás → az SQL-szabálysértés javítva (F182.25), a BDB-tesztek (TestSzabalyok, TestF104BdbJeloles, TestF104Egysegek, TestBdbMagyarOsszefuzo: 23) OK; a két `TestD2PilotEgyezes` (1Móz 1:25, Zsolt 22) a görög Thayer-szócikk meglétén bukik (a friss adatbázis frissebb Thayer-adata a pilothoz képest), nem a BDB-módosításon.
- **A CI-futtató** (`eszkozok/ellenorzes/futtat.py --teljes`) helyben nem futott (az 1. fázisban 25 perc után időtúllépés); a teljes CI a push után a GitHubon fut.

### Lapnézet

`C:\Users\bases\AppData\Local\Temp\claude\256fc271ccf0bd2c\02da030a-5490-4ba6-b1c8-245010c77469\scratchpad\HAMART-001_lapnezet.html` — az `epit_nezet.py` (`C:\Users\bases\pardes_eszkozok\`) kimenete a HEAD lapjából; utólag: HAMART-001 cím (az eszköz az ISTENTISZT-001 feliratát hordozza), `<meta charset="utf-8">`, világos téma rögzítve (`data-theme="light"`). A fejsáv „PARDES MOTÍVUMLEXIKON · ARANY LAP” felirata az eszközé (nem a lapé). Saját átnézés: Kivonat, 2. tábla, a 4.2 kártyák (H2403, H2555, H7451, H0423 apparátusa, G1311), a „A motívum helyein” sorok.

### Nyitott és elhalasztott tételek

- Új nyitott tételek (`nyitott/uj/hamart-javito.md`): **N-F182b** (a sorbelső fej nem csomópont a fában; 440 pont repó-szinten, HAMART: 0), **N-F182c** (két szócikk azonos 2.29-címkével: az olvasó nem dönt a hely szerint; 5 368 sor, HAMART: 172, mind H7451), **N-F182d** („független megerősítés” mondat a TSK ↔ Károli-KH viszonyáról, tartalmi kérdés), **N-F182e** (8 nem létező Károli-versre mutató szótári hivatkozás; a Lam → „Sir” `karoli_vers`).
- Elhalasztva (a hatókör szerint): F1, F3–F21 (a látható hibákon túl), F24 (c) (1) kapuja (a nyers proveniencia-sor), H4 (b) előfeltétel-térkép, H5, N-F178a/b; az `.claude/agents/hatar-ellenor.md` hivatkozása (felhasználói jóváhagyás).
- Előzetes tesztbukások (nem e menetből): `teszt_szotari_gerinc` 6 (a #187 jelentésének listája), `teszt_olvasoi_kapu` Arany.test_G7, `teszt_glossza_api_koteg` TeljesUt (a valódi táblára épülő adatfüggő eset: az érvényes UBS-sor már létezik; az őr nélkül is SystemExit), `teszt_thayer_api_koteg` BUt (G4151 kérésterv: 4 csoport 3 helyett), `teszt_nyilt_mag` `test_nincs_nyitva_sor_es_nincs_feloldatlan_dt` (a DT-F182 helyőrzők ágon feloldatlanok; a számkiosztás után zöld).

## 3. menet (2026-11-11): a kész lap követelménylistájának HAMART-tételei

*Végrehajtó: claude-opus-5-5 (modell-ellenőrzés: a brief `modell: opus` mezőjével egyezik). Kezdés: 09:43. A fordítási lépés subagentje: claude-sonnet-5-5 (saját kiírt modellneve). Hatókör: a `sablonok/KESZ_LAP_KOVETELMENY.md` (a) listájának nyitott HAMART-tételei (A02, A03, A05–A17, A19–A26; az A27 a #183-é) és a (b) lista #182-t érintő döntései (DT-F182j, DT-F182k), az orkesztrátor menet közbeni lelete (a KH-lábjegyzet napló-utalása) és a befagyasztás 1. pontja (a lapon látható hiba). A lap a végén generálódott újra (F182.39); a saját átnézés két apró látható hibája után még kétszer (F182.40, F182.41). Ez a jelentés nem minősíti a munkát ellenőrzöttnek.*

### A/B állapottábla (tétel → állapot → commit)

| Tétel | Állapot | Commit |
|---|---|---|
| A01 | teljesül (2. fázis) | F182.24 |
| A02 | teljesül — azonosító tábla a lap elején, olvasói mezőnevek, státusz a kiadási állapotból (az Irodalomban is) | F182.30 |
| A03 | teljesül — a 2. szakasz következtetése: súlypont + szövetség-arány | F182.30 |
| A04 | teljesül (2. fázis) | F182.26, F182.29 |
| A05 | teljesül — az indoklás nem hivatkozik más sorra, a tanulmányra, a naplóra | F182.33 |
| A06 | teljesül — névelő, írás + zárójeles kiejtés (71 + 4 indoklás); kapu: NEVELO | F182.33, F182.38 |
| A07 | teljesül, kivétellel — a Kivonat, a 3. szakasz és a Döntési út bevezetője, a Módszertan harmadik személyben; a sablon v4 kötelező „1.2 Hol kerestünk” alcíme marad (K33 ↔ K12 ütközés, N-F182g, döntési pont); kapu: MI_HANG | F182.30, F182.36, F182.38 |
| A08 | teljesül — a lábjegyzet olvasói alakja; a KH-lábjegyzet napló-utalása (186 + 69 sor) és nyers jele nélkül; kapu: NYERS_JEL | F182.30, F182.38 |
| A09 | teljesül — a 4. szakasz szólistái írással és kiejtéssel; a pontrendszer a Jelmagyarázatban | F182.30 |
| A10 | teljesül — a görög 4.1 a TBESG rövid jelentéséből | F182.34 |
| A11 | teljesül — a 4.3 tW-címek magyarul, azonosító nélkül, a forrás egyszer | F182.34 |
| A12 | teljesül — a 4.4 doménnevek magyarul | F182.34 |
| A13 | teljesül — a 4.6 szavanként egy mondat, kis elemszámnál következtetés nélkül | F182.30 |
| A14 | teljesül — a 4.7 egy mondata, következtetés csak a SECE-párnál; kapu: KOV_ISM | F182.30, F182.38 |
| A15 | teljesül — a rokon nyelvi tábla a 4.8-ban, „2. szerep”, nyelvtani alak, „késői héber” nélkül (DT-F182l) | F182.32 |
| A16 | teljesül — a 4.9 csoportosított mondata, a kivételek igehellyel | F182.30 |
| A17 | **részben** — a két csukott cím glosszája és a `_226` / nyers BDB-fej kész; a szócikkhatár-hibák (K56) nem (adat: a `bdb_szakasz_hu.tsv` illesztő lánca, N-F182f) | F182.35 |
| A18 | teljesül (fordítva értendő: mért BDB-pontosság nincs a lapon) | 2. fázis |
| A19 | teljesül — az 5. szakasz és a 4.11 egy forrásból; kapu: eltérésnél a generálás megáll | F182.30 |
| A20 | teljesül — a 4.6 és az 5. szakasz versben mér | F182.30 |
| A21 | teljesül — az Alkalmazás lekerül, a forrás szövege archívumban; a Kolofon szerzőségi mondata a mai szakasznevekkel (DT-F182m) | F182.30, F182.36, F182.37 |
| A22 | teljesül — egységes kiejtés az indoklásokban; a rokon nyelvi alak más szó (az ATIRAS_VALT ott nem mér) | F182.33, F182.38 |
| A23 | teljesül — `lexikon/HAMART-001_KIZARASOK.md`, kapuval; lelet: 14 kétszer számolt vers (DT-F182n) | F182.31 |
| A24 | teljesül — 4.13 és 4.14 adatból, szavanként mérve (DT-F182o) | F182.30, F182.40 |
| A25 | teljesül — az áttekintő tábla LXX-oszlopának lábjegyzete a 4.11-hez méri | F182.31 |
| A26 | teljesül — a Jelmagyarázat két lektori aprósága | F182.30 |
| A27 | nem e menet tétele (#183) | — |
| B04 | végrehajtva (sablon 6 v4, sablon 9, sablon 10; a CLAUDE.md mondata felhasználói jóváhagyással, N-F182h) | F182.30, F182.36, F182.37 |
| B07 | végrehajtva (l. A07) | F182.30, F182.36, F182.38 |
| B08 | végrehajtva (indoklások; sablon 6 „Kiejtés formája”) | F182.33, F182.37 |
| B09 | végrehajtva — a generátor a licenctábla szerint jelölt (SECE közkincs, MCGED tisztázott); a sablon bekezdése igazítva | F182.37 |
| B10 | végrehajtva — Kolofon forrásonként egy sor, „Fájl” oszlop nélkül, olvasói névvel | F182.30, F182.37, F182.41 |
| B13 | végrehajtva (l. A15) | F182.32, F182.37 |
| B14, B15 | végrehajtva (A23; A02; A24) | F182.30, F182.31 |

### A 4.13 és a 4.14 eredménye

- **4.13 Károli-megfelelők:** a motívum 47 helyén a Károli 27 szótári alakot használ; szavanként (legalább 3 hely): a חָמָס (chámász) 12 helyéből 9-ben „erőszak”, az אֲדָמָה (adámá) 10-ből 10-ben „föld”, az אָרַר (árar) 4-ből 3-ban „átkoz” (ezek magyarul is követhetők), a שָׁחַת (sáchat) 7-ből legfeljebb 2-ben ugyanaz („elvesztés”; váltakozó). A többi 11 szó 3 helynél kevesebben áll: következtetés nélkül.
- **4.14 Rejtett / hamis párhuzam:** a 14. szerep szabálya (a szó helyeinek legalább felében álló szótári alak) a 15 szóból kettőnek ad kulcsszót: adámá „föld”, árar „átkoz”. A többinél a lap kimondja, hogy a módszerrel nem mérhető (asszociatív kitöltés nincs). Rejtett párhuzam: 1 hely (1Móz 12:3 „megátkozom”, igekötős alak). Hamis párhuzam: 2 318 Károli-vers; a Károli–Strong párosítás szerint a „föld” mögött leggyakrabban az אֶרֶץ (erec) áll (1 957 vers), az „átkoz” mögött a קָלַל (kálal) (9 vers). Következtetés: a magyar szókeresés 2 331 találatának 99%-a nem a motívumé. A lista könyvenként, igehellyel, csukva; jelölt belőle nem lett (CLAUDE.md 2. szabály). A formula-motívumra szabott „A motívum kulcsszavai” blokk az új lapon nem áll (DT-F182o). A TSK/Károli-KH negatív párjai és a `kizaras_csoportok.tsv` nem kellettek: a meglévő Károli-építő (a #22 párosítás) adatot adott.

### Látható hibák (a lapon, a generátorban javítva)

1. A KH- és a minősítés-lábjegyzetek napló-utalása („napló: … (4/b. rész)”, 186 + 69 sor), nyers indoklása és belső keresési jele (`halo=`, `blokk=`, „lanc ±1”, „csalad H…”) — az orkesztrátor lelete (F182.30). A `<!-- eredeti: … -->` megjegyzés sem a nyílt magba, sem a renderelt lapnézetbe nem jut ki (a nyílt mag exportja a lapot nem olvassa; a lapnézet szövegében 0 „eredeti:”).
2. A Döntési út és a 3. szakasz számai 14 verset kétszer számoltak (1 520 → 1 506 csoportos, 1 810 → 1 796 megvizsgált vers; DT-F182n) — a melléklet kapujának lelete (F182.31).
3. A 4.13–4.14 meglévő építőjének hamis mondatai a több szóval hordozott motívumon (DT-F182o) (F182.30).
4. Az 1.5 „a 11. szakaszban (Módszertan …)” hivatkozása az Alkalmazás nélküli lapon a 10. szakaszra (F182.38).
5. A dőlt forrássorok „Proveniencia:” mezőneve (F182.38); a Kolofon „adat/karoli_strong” nyers útvonala (F182.41, a lapnézet átnézésének lelete).

### Tesztek, kapuk, regresszió

- `teszt_kesz_lap_hamart.py`: 27 teszt, OK (lap, melléklet + rontott csoport, generátor, OK-szövegek, a négy új kapu rontott mintán és a régi lapon).
- Olvasói kapu, HAMART-001: **0 BUKÁS**, 16 FIGYELMEZTETÉS (ANGOL_SOR 7: licencsor vagy `title`; MOTIVUM_ID 6; KIVONAT_SZAM 2: hamis riasztás; HIANYJEL 1: „(nincs görög szó)”, igaz állítás). A 3. menet előtti lap mint rontott minta: 84 BUKÁS.
- `ellenoriz.py`: **0 SÉRTÉS**, RENDBEN 26, JELENTÉS 17, KÉZI 2 (a 11. szabály a kivezetett résre és az új lap utómunkájára igazítva; a 43. szabály hatóköre a 4.13 előtt; a 27. szabály 4 HAMART-jelentése: N-F182f; a 21. szabály a DT-F182 helyőrzőket jelzi).
- Nyílt mag kapu: 0 BUKÁS; angol pár: 1 039 cella, hiányzó 0, elavult 0.
- Régi lapok: a 8 régi lap generált kimenete a menet előtti kód (e1080b2a, külön munkafa) kimenetével bájtra azonos.
- A Windows-tesztkör és a `teszt_futtat.py --gyors` eredménye: a „Tesztkör” alszakaszban.

### Tesztkör (3. menet)

- **`python eszkozok/teszt_futtat.py --gyors`** (WSL): a `teszt_visszhang_kapu.py` a 4.8-ba költözött rokon nyelvi tábla miatt bukott (az arany minta a 4.11-ből olvasta), javítva (F182.43): 22 teszt, OK. A többi bukás (`teszt_bdb_vers_jelentes` CsoportOszlop, `teszt_olvaso_szerver` TestF104BdbJeloles és TestLapok, `teszt_pilot_aranymintaval` DT_F76f, DT_F76g) tesztnevenként azonos a menet előtti kód (e1080b2a, külön munkafa) futásával: a WSL-adatbázis állapotához kötött, nem e menet változása.
- **Windows-kör** (`eszkozok/teszt_*.py`, 80 modul, modulonként), tesztnevenként összevetve az alapvonallal (ugyanazok a modulok a menet előtti munkafán): **csak az ágon bukott** a `teszt_strong_util` (a „—” kulcsú doménsorok, javítva: F182.44, utána OK), és három modul a meghajtó-eltérés miatt (`teszt_emeles` 4, `teszt_general_kinyeres` 4, `teszt_render_diff_osztalyoz` 1: „path is on mount 'C:', start on mount 'E:'” — a munkafa az E:-n, a teszt ideiglenes könyvtára a C:-n; az alapvonal-munkafa a C:-n állt, ott nem jön elő; a 2. fázis jelentése ugyanezt az E:-s alapvonalon is mérte). A többi bukó modul (bdb_adatblokk, bdb_psi_javit, bdb_zaras, ellenoriz_vedokorlat, forditas_kapuk, general_ellenorzo, jelolt_eloszures, lektor_kerdesek, lexikon_adatres, nyilt_mag, olvasoi_kapu, szakasz_cimke_levezet, szerep_karoli, szerep_nave, szerepmatrix, szotari_gerinc) tesztnevenként azonos az alapvonallal.
- `ellenoriz.py` (a végső állapoton): 0 SÉRTÉS, RENDBEN 26, JELENTÉS 17, KÉZI 2. Nyílt mag: naprakész (az export a commitolt állapottal azonos).

### Mérési sorok

*Modell: claude-opus-5-5 (a fordításnál claude-sonnet-5-5); effort: nem látható; a keret %-a előtte és utána: nem látható. Idő: a commitok ideje.*

| Lépés | Kezdés | Vége | Idő |
|---|---|---|---|
| modell-ellenőrzés, bemenet, felmérés | 09:43 | 09:55 | 12 perc |
| generátor-tételek (A02–A26 nagy része, KH-lábjegyzet) | 09:55 | 10:11 | 16 perc (F182.30) |
| melléklet + kapu, kettőzött versek (A23, A25) | 10:11 | 10:18 | 7 perc |
| A15 | 10:18 | 10:20 | 2 perc |
| indoklás-adat, nyílt mag, címfordítás (Sonnet subagent: kb. 1 perc) | 10:20 | 10:31 | 11 perc |
| A17 | 10:31 | 10:36 | 5 perc |
| forrás (A07, A21), sablonok, döntések | 10:36 | 10:39 | 3 perc |
| kapuk, tesztek, a lap újragenerálása | 10:39 | 10:46 | 7 perc |
| `ellenoriz.py`, regresszió, lapnézet és saját átnézés, javítások | 10:46 | 10:54 | 8 perc |
| követelménylista, jelentés, tesztkör (alapvonal-összevetéssel), két tesztlelet javítása, push | 10:54 | 11:19 | 25 perc |

### Lapnézet

`C:\Users\bases\AppData\Local\Temp\claude\256fc271ccf0bd2c\02da030a-5490-4ba6-b1c8-245010c77469\scratchpad\HAMART-001_lapnezet.html` — az `epit_nezet.py` kimenete a HEAD lapjából; utólag: cím, charset, világos téma (`data-theme="light"`), a fejsáv fájlneve HAMART-001-re (N-F182j). Saját átnézés a renderelt nézetben: azonosító tábla, Tartalomjegyzék, 4.6, 4.13, 4.14, Kolofon, a Döntési út melléklet-linkjei (29), nyers jel 0.

### Döntési pontok a felhasználónak

1. **N-F182g:** a sablon 6 v4 kötelező alcíme („1.1 Mit keresünk · 1.2 Hol kerestünk”) ütközik a B07/K12 harmadik személyű szabályával. Javaslat: „1.1 Mit keres a lap · 1.2 Hol keresett” (a generált bevezető már így szól).
2. **N-F182h:** a CLAUDE.md „kilenc rés” mondata az `alkalmazas` kivezetésével (DT-F182m) — a CLAUDE.md-t a végrehajtó nem írja.
3. **A17 / N-F182f:** a BDB-szócikkhatár javítása a BDB-lánc adatfeladata; lapszinten (kézi folttal) nem javítható. Javaslat: a #185-lánc saját tételeként az 1. kiadás előtt, vagy a 2. kiadásra.

### Új nyitott tételek

N-F182f (BDB-szócikkhatár), N-F182g (K33 ↔ K12 alcím), N-F182h (az `alkalmazas` kivezetésének maradéka), N-F182i (a 14. szerep szócsalád-összevonása), N-F182j (a lapnézet-eszköz feliratai) — `nyitott/uj/hamart-javito.md`.

## Javítókör (2026-11-11): a független ellenőrzés (`naplok/ELLENOR_F182.md`, 11 tétel) után

*Végrehajtó: claude-opus-5-5 (modell-ellenőrzés: a brief `modell: opus` mezőjével egyezik). Kezdés: 11:38. A fordítási lépés subagentje: claude-sonnet-5-5 (saját kiírt modellneve). Hatókör: az orkesztrátor 13 tétele, menet közben kiegészítve az ELLENOR #10 és #11 felhasználói döntésével (2026-11-11, „mehet”). Az egyetlen javítókör; utána nincs újabb. Ez a jelentés nem minősíti a munkát ellenőrzöttnek.*

### Tételenként

| # | Tétel | Javítva? | Commit | Hogyan / miért nem teljesen |
|---|---|---|---|---|
| 1 | E28 HIBA (4 generált nézet) | igen | F182.47 | `general.py --cel naplo/index/nyitott --ir`: a motívumnapló két blokkja, a lezárt tanulmányok indexe, a NYITOTT_FELADATOK nyitott-blokkja (48 → 47, 251 → 250, 537 → 538); kézi szerkesztés nincs. CI: E28 0 HIBA. |
| 2 | E5 HIBA (szándékos törlés) | igen | F182.47 | Az E5 a PR összes commit-üzenetében sor eleji „TÖRLÉS-SZÁNDÉKOS:” jelölést vár; az F182.47 üzenete ezt hordozza, a két törlés (a „## 10. Alkalmazás” cím, a `KESZ_LAP_KOVETELMENY.md` 66 sorcseréje) megnevezésével. CI: E5 0 HIBA. |
| 3 | 4.14 tartomány-kulcs | igen | F182.49 | `szerep_karoli.hamis_parhuzamok`: a `sajat` halmaz a meglévő `szerep_kizart.versek` szabályával bont. Teszt: `test_hamis_tartomany_kulcs` (a régi kódon bukik). A lapon: hamis párhuzam 2 318 → 2 312 vers (az Ézs 24:5, 24:6, Hós 4:1, 4:3, Gal 3:13, Zsid 6:7 kikerült), a következtetés „a 2325 találat 99%-a nem a motívumhoz tartozik”. |
| 4 | 1Móz 3:17 LXX-párosítás | igen | F182.50 | `lxx_osszevetes`: az új szerkezetű lapon az „egyező” görög szó a kulcsszó saját 4.11-párja; a kapu (`lxx_egyforras_ellenoriz`) a kulcsszó Strongjához mér. Teszt: `test_lxx_sajat_par_1moz_3_17` (a régi párosítás mint rontott minta jelez). Egyező 7 → 6, eltérő 27 → 28, 15% → 13%; a 4.6 adámá-mondata is követi. |
| 5 | „(7. rész)” napló-utalás | igen | F182.51 | Az olvasói átírás minden `(\d+(/[a-z])?\. rész)` alakot elhagy, a fájl „§N” jele sem lesz „(N. rész)”; a NYERS_JEL kapu mindet fogja. Teszt: a rontott minták között a „(7. rész)”. |
| 6 | Nyers jelek | igen | F182.51 | `csatorna=cli` törölve, `szamozas_elteres` → „versszámozás miatt nem párosítva”, „(forras_kereses: …)” → „(a keresés forrása: …)”; mind a `NYERS_JELEK`-ben; tesztek: `test_nyers_jel`, `test_olvasoi_atiras_nyers_jelek`. |
| 7 | Jelmagyarázat kisbetűsítése | igen | F182.52 | `kisbetus_kezdes`: mozaikszó (≥ 2 nagybetű) és tulajdonnév (`KISBETU_TULAJDONNEV`) változatlan; „4.6 LXX-híd”, „4.13 Károli-megfelelők”. Teszt: `test_jelmagyarazat_kisbetu`. |
| 8 | Indoklások (A05/A06/B08) | igen, egy korláttal | F182.53, F182.57 | Adat szkripttel, összevetéssel (`naplok/F182_indoklas_javitokor.py`): 48 `jeloltek.tsv`-indoklás, 1 `elofordulasok.tsv`-próza (Jel 22:3), az elutasítási ok 123-as mintája. Kiejtés a generátor szabályából (`lemma_kiejtes`, `heber_gepi`); a „… sorának folytatása” helyett „a szomszédos vers, az … folytatása”; a munkajavaslat ki, a javaslat N-F182l. Kapu: új INDOKLAS (BUKÁS, új szerkezet). **Korlát:** az E13 a HAMART-ra nem vihető 0-ra: a találatok nagyobb része a 4. szakasz BDB-szövegének héber töredéke („ק׳”, „הִ”), ahol kiejtés nem követelmény; ezért az indoklásokra a külön kapu áll. A nyílt mag és 21 szöveg (48 cella) angol párja frissítve (Sonnet, átnézve). |
| 9 | 4.13 „erőszak (2)” / „megroml” | igen (a HAMART-on látható részt) | F182.54 | Egy szabály, egy hely: `szerep_karoli.szocsalad`; a lista és a próza szócsaládonként („erőszak” 9 = a próza 9/12-e; 27 → 23 szó). „megroml” → „megromlik”: kivétel a `hibrid.py`-ban, a generált szótárialak-tábla az eredeti `--ts`-sel újraépítve (5 sor + fejléc-hash). A többi nem szótári alak („színe”, „fájdalma”, „ragadománnyal”, „elveszessek”, „megrontott”) a tábla közös sorain áll, a 14. szerep teljes Károli-keresésén át más lapokat is érinthet: N-F182i kiegészítve. |
| 10 | Alcím (N-F182g, A07) | igen | F182.55 | „1.1 A keresés tárgya · 1.2 A keresés forrásai” a sablon 6 v4-ben, a K33-ban és a generátorban; a MI_HANG kivétele megszűnt. DT-F182p; az N-F182g lezárva. A sablon 9-ben az alcím nem áll. |
| 11 | BDB szócikkhatár (A17/K56) | igen a HAMART-on | F182.56 | A `bdb_szakasz_hu.tsv` generált, ezért a tételek a generátor kézi szótárában (`hu_illeszt.SZOCIKKHATAR_KEZI`, a `JELENTESPONT_KEZI` mintája; `scope=manual`, a forrás idézetével; ha a horgony nem pontosan egyszer áll, a generálás megáll). Részleges újragenerálás (`--strong H2403,H7451 --ts 2026-11-10`): 6 sor + fejléc. A 27. szabály a HAMART-on 0. DT-F182q; az illesztő általános javítása az N-F182f-ben marad. |
| 12 | CLAUDE.md réslista | igen | F182.48 | „nyolc rés”, az `alkalmazas` a felsorolásból ki, egy mondat a kivezetésről (DT-F182m). Más nem változott. |
| 13 | N-F182d lezárása | igen | F182.48 | A DT-F182j alapján lezárva; a SEMA 2.12-höz a javítókör nem nyúlt. |
| ELLENOR #10 | kapcsolat-jelöltnapló | igen (dokumentáció) | F182.48 | DT-F182r (a felhasználó szavával), N-F182a lezárva, N-F182k új (sémabővítés és átköltöztetés a generátor-körben). A CLAUDE.md nem változott. |
| ELLENOR #11 | DT-F182m és SEMA 2.12 | igen (dokumentáció) | F182.48 | A DT-F182m-ben a felhasználó jóváhagyása („mehet”); a SEMA 2.12 marad. |

A végén: a lap egyszer újragenerálva (F182.58; a melléklet nem változott); a CI két új jelzése (E32, E37), a követelménylista állapota és a brief fejléce (F182.59); ez a jelentés (F182.60).

### Saját átnézés (renderelt lapnézet)

`C:\Users\bases\AppData\Local\Temp\claude\256fc271ccf0bd2c\02da030a-5490-4ba6-b1c8-245010c77469\scratchpad\HAMART-001_lapnezet.html` (az `epit_nezet.py` kimenete a HEAD lapjából; utómunka: cím, charset, világos téma, a fejsáv és a lábsor HAMART-001-re, N-F182j). A böngészőben (helyi HTTP-szerverről) ellenőrizve: világos téma; az 1.1–1.2 új alcíme; a Jelmagyarázat „4.6 LXX-híd”; a 4.13 „23 … (szócsaládonként)”, „erőszak (9)”, „megromlik”; az 5. szakasz 1Móz 3:17 sora „γῆ (gé) · eltérő · gépi társítás”; a Jób 31:40-csoport „(חוֹחַ (chóach) és בָּאְשָׁה (bosá))”; az Ez 7:6 indoklása munkajavaslat nélkül; a BDB9520, BDB8033, BDB8034 feje a saját magyar szövegével, a „szócikkhatáron át” megjegyzés 0. A látható szövegben 0: „(N. rész)”, `csatorna=`, `szamozas_elteres`, `forras_kereses`, „eredeti:”, „Mit keresünk / Hol kerestünk”, „lXX”, „sorának folytatása”, „érdemes lehet”.

### Ellenőrzők és tesztek

- **CI-futtató** (`python eszkozok/ellenorzes/futtat.py --valtozott <git diff --name-only merge-base..HEAD> --diff-alap <merge-base> --diff-fej HEAD --commit-uzenet-fajl <a PR commit-üzenetei>`, a CI workflow szerint): a javítókör előtt E28 HIBA 4, E5 HIBA 2, E16 HIBA 1. Az első javított futás két új HIBA-t mutatott (E32: a `DT-F182q` helyőrző a `hu_illeszt.py` string-literáljában; E37: a SEMA 3.11 generált kapulistája az új INDOKLAS kapu nélkül), mindkettő javítva (F182.59). A végső futás (HEAD `9c33c27e`): **HIBA csak az E16** (a PR-cím „[ELLENŐRZŐ]” előtagja; helyben üres PR-címmel fut), E28 0 („5 migrált nézet”), E5 0. JELENTÉS-szint: E12 569, E13 75 (előtte 79), E25 3, E27 43, E30 9, E32 13 (régi helyőrzők az `emeles.py`-ban), E34 41, E36 1.
- **`python eszkozok/ellenoriz.py`** (végső állapot): **0 SÉRTÉS**, RENDBEN 26, JELENTÉS 17, KÉZI 2. A 26. szabály (a `bdb_szakasz_hu.tsv` = a generátor kimenete) RENDBEN; a 27. szabály 2 jelentése az ALVIL-001-é és az ISTENTISZT-001-é (a HAMART-001-é 0).
- **`python eszkozok/teszt_futtat.py --gyors`** (WSL, `~/pardes/pardes.db`, építés 2026-11-02): 10 modulból 7 zöld; bukott a `teszt_bdb_vers_jelentes` (CsoportOszlop), a `teszt_olvaso_szerver` (TestF104BdbJeloles.test_kattinthato_helyek, TestLapok.test_bdb_jelentesszerkezet_jeloloi_a_szocikkbol) és a `teszt_pilot_aranymintaval` (DT_F76f, DT_F76g) — tesztnevenként ugyanaz, mint a 3. menet alapvonala (a WSL-adatbázis állapotához kötött).
- **Windows, az érintett modulok** (a javítókör előtti HEAD, `1e0da664`, külön munkafán futtatott alapvonallal tesztnevenként összevetve): `teszt_kesz_lap_hamart` 34 teszt, OK (köztük az új tesztek); `teszt_forditas_vedelem` OK; a `teszt_olvasoi_kapu` (Arany.test_G7_dt_a_prozaban), a `teszt_szerep_karoli` (ValodiAdat: 3), a `teszt_nyilt_mag` (Pozitiv.test_nincs_nyitva_sor_es_nincs_feloldatlan_dt) és a `teszt_lexikon_adatres` (KolofonKiadas.test_igazi_tabla_istentiszt) bukásai az alapvonalon is ugyanazok; új bukás nincs.
- **Nyílt mag:** `nyilt_mag_kapu.py` 0 BUKÁS; angol pár 1 039 cella, hiányzó 0, elavult 0.
- **Régi lapok:** a CI E28-a 0 (a négy régi migrált lap a generátor mai kimenetével bájtra egyezik); a `lexikon/` alatt csak a `HAMART-001_TUDOMANYOS.md` változott.

### Mérési sorok

*Modell: claude-opus-5-5 (a fordításnál claude-sonnet-5-5); effort: nem látható; a keret %-a: nem látható. Idő: a commitok ideje.*

| Lépés | Kezdés | Vége | Idő |
|---|---|---|---|
| modell-ellenőrzés, bemenet, CI-alapállapot | 11:38 | 11:42 | 4 perc |
| E28, E5 (F182.47) | 11:40 | 11:42 | 2 perc |
| CLAUDE.md, DT-F182r, nyitott-tételek (F182.48) | 11:42 | 11:43 | 1 perc |
| 4.14, 5. szakasz, nyers jelek, Jelmagyarázat (F182.49–52) | 11:43 | 11:49 | 6 perc |
| indoklás-adat, INDOKLAS kapu (F182.53) | 11:49 | 11:55 | 6 perc |
| 4.13, szótárialak-kivétel (F182.54) | 11:55 | 11:58 | 3 perc |
| alcímek, DT-F182p (F182.55) | 11:58 | 11:59 | 1 perc |
| BDB szócikkhatár, DT-F182q (F182.56) | 11:59 | 12:03 | 4 perc |
| nyílt mag, angol pár (Sonnet subagent: kb. 30 mp) (F182.57) | 12:03 | 12:06 | 3 perc |
| lap újragenerálása, lapdiff (F182.58) | 12:06 | 12:08 | 2 perc |
| lapnézet, saját átnézés | 12:08 | 12:12 | 4 perc |
| CI, `ellenoriz.py`, tesztek, alapvonal; E32/E37 (F182.59) | 12:12 | 12:37 | 25 perc (ebből kb. 20 perc várakozás a közös ellenőrzési zárra) |
| jelentés, push | 12:37 | 12:40 | 3 perc |

### Nyitott pontok

- **N-F182f:** az illesztő lánc általános szócikkhatár-szabálya (az ALVIL-001 és az ISTENTISZT-001 egy-egy 27. szabály-jelentése; utána a kézi tételek kivezethetők).
- **N-F182i:** a 14. szerep szócsalád-összevonása és a szótárialak-tábla maradék nem szótári alakjai (a HAMART-on látható: „színe”, „fájdalma”, „ragadománnyal”, „elveszessek”, „megrontott”).
- **N-F182k:** a `jeloltek.tsv` sémabővítése és a 103 kapcsolat-jelölt átköltöztetése (generátor-kör).
- **N-F182l:** a „vég elérkezett” formula mint lehetséges önálló motívum (nem a #182-é).
- **E13:** a HAMART-on a BDB-szöveg héber töredékei miatt JELENTÉS marad (FIGYELMEZTETÉS-szint).
- Az olvasó-szerver adatbázisa (`pardes.db`) a szótárialak-tábla és a `bdb_szakasz_hu.tsv` változását a saját újraépítésével kapja meg.
