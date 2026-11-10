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
| K2 (Ez 12:19 bent ↔ Hab 2:8, 2:17 kint) | DT-F123ha (B), DT-F123hc (K3) | **lezárt** | Következetesség mérve (TAHOT, minden chámász-vers): a 13 vers, amelyben a chámász mellett a ml'-tő (ige vagy a melóá főnév) vagy a sámá áll, mind bent; a 46 szópár nélküli mind kint. Az Ez 12:19 a ml'-tő egyetlen főnévi esete. Adat nem változott. |
| K3 (Gal 3:13-14) | N-F123hc, DT-F123hd, DT-F123he | **lezárt, nem nyitottam újra** | A lap a sort „Határeset: a kapcsolat az áldás-mondaton át” funkcióval és a „Határesetek” listán (közepes) mutatja; olvasható. Megjegyzés: a felhasználó „tematikus kapcsolat”-nak nevezte, az adat „határeset”-nek (a G1944 a versben áll, ezért nem „tematikus, nem lexikai” sor). |
| K4 (Ez 28:16, Mik 6:12, Sof 1:9: a szópár a föld nélkül) | nincs | **lezárt: DT-F182d (A), a felhasználó döntése** (2026-11-10, az orkesztrátor továbbításában: „a”) | A szópár (málé + chámász, illetve sámá + chámász) önmagában elég: a formula az 1Móz 6:11-13 szava, maga utal vissza. A sorok maradnak. Az öt vers (Ez 28:16, Mik 6:12, Sof 1:9, Jer 6:7, Hab 1:2) indoklása (`jeloltek.tsv`) és 1/a prózája (`elofordulasok.tsv`) ezt kimondja (`naplok/F182_k4.py`, összevetéssel). A sámá-soroknál pontosítva: az 1Móz 6:11 és 6:13-ban a chámász a málé igével áll (TAHOT: H2555 + H4390), a sámá nem; ott az indoklás azt mondja, hogy az erőszak szava az 1Móz 6:11-13 szava, a „hallatszik az erőszak” pedig a lánc szópárja. A nyílt mag és az öt indoklás angol párja frissítve (Sonnet; két helyen a „voice of the earth” félrefordítást „word for the earth”-re javítottam: `claude-sonnet-5-5; javítás: claude-opus-5-5`); a nyílt mag kapuja 0 BUKÁS. |
| K5 (1Móz 6:5 ↔ Jer 17:9 „jetzer”) | DT-F123ha (E), DT-F123hc (K8) | **lezárt; az indoklás frissítve: DT-F182b** | A sor marad. Az elavult indoklás (a kivezetett רַע szóra épült) helyett: a vers a 6:7 ítéletének indoka ugyanabban az elbeszélésben, és a bent álló 8:21 ugyanezt az indokot mondja ki; a Jer 17:9, Jer 4:14, Mt 15:19, Mk 7:21-23 a lánc elbeszélésén kívül áll. |
| K6 (Gal 3:14, Zsid 6:7 a tartományban ↔ Róm 8:20 kint) | DT-F123hd (Gal), DT-F123hc (K10, Róm) | **Gal és Róm lezárt; Zsid: DT-F182c** | Szabály a két lezárt döntéssel összhangban: a tartomány addig tart, ameddig a hely állításához szükséges rész áll. A Zsid 6:8 igenévi mondatának alanya (γῆ) a 6:7-ben van (TAGNT; Károli: „A mely pedig …”), a Róm 8:21 maga hordozza az alanyt (κτίσις) és a φθορά szót. Csak a Zsid 6:7-8 indoklása változott. |

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
| F13 — a rokon nyelvi tábla a 4.8-ba (a DT-F178a módosítása) | `eszkozok/lexikon_general.py`, `eszkozok/visszhang/megfelelo_kinyer.py`, `sablonok/6_*` | #104, #187 |
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
| N-F178a/b, N-F103b (a csukott cím glosszája) | `eszkozok/lexikon_general.py` | #104 |
| H4 — jelölő-kapu a `/kiadas` előtt; előfeltétel-térkép a MUNKAMENET-ben | `eszkozok/olvasoi_kapu.py` / `eszkozok/ellenoriz.py`, `MUNKAMENET.md` | #104 |
| H5 — a #38 záró ellenőrzésének hiánya ismert korlátként a Kolofonban | `eszkozok/lexikon_general.py` | #104 |
| A nyílt mag frissítése a 2. fázis adatváltozásaival (az 1. fázisé kész: F182.5); az F4-javítás után az indoklások angol párja újrafordul | `nyilt_mag/*`, `adat/nyilt_angol.tsv` | a 2. fázis adatváltozásaival együtt (E35) |
| A lap újragenerálása, saját renderelt átnézés, független ellenőr (H6) | `lexikon/HAMART-001_TUDOMANYOS.md` | a fenti tételek; #104, #105, #185, #186, #187 |

## Ellenőrzés a menet végén

- `python eszkozok/ellenoriz.py` (az F182.7 után): **1 SÉRTÉS**, a 11. szabály („Rés-forrás egyezés”): a lap négy rése (`kivonat`, `miert_fontos`, `ertelmezes`, `modszertan`) eltér a forrástól, mert az F182.3 a `motivumok/HAMART-001.md` prózáját javította, a lap viszont az 1. fázisban nem generálódhatott újra (a `lexikon/` alatt semmit nem írtam). Az F182.1–F182.2 utáni futás még 0 SÉRTÉS volt; az F182.3 után nem futtattam újra, ezért ez csak most derült ki. **Döntés kell (orkesztrátor):** (a) a lap újragenerálása már most (a lexikonlap-tilalom alóli kivétel, csak a rések frissülnek); (b) a CI-hiba vállalása a 2. fázisig (a PR addig nem mergelhető); (c) a forrás prózajavításának visszavétele a 2. fázisig. Javaslat: (b), mert a PR úgyis a 2. fázissal együtt zárul, és a lap a 2. fázisban egyszer generálódik újra. A 39. szabály JELENTÉS-e a lezárt határ ismert eltérése (F26).
- `python eszkozok/nyilt_mag_kapu.py`: 0 BUKÁS. A CI-futtató (`eszkozok/ellenorzes/futtat.py`) helyben: az F182.2 utáni futás egyetlen hibát adott (a kódkönyv hiányzó zárt értéke, az F182.5 javította); a teljes ágra indított futás 25 perc után időtúllépéssel megállt, eredmény nélkül. A teljes CI a GitHubon fut a push után.
