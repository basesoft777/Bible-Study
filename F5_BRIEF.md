# F5 brief — sablon-frissítés (`4_PaRDeS_tematikus_sablon.md`)

*Készítette: chat-menet (Opus 5), 2026-09-15, **v1** (első kiadás). Kiindulási állapot: `main` = `origin/main` = **`f425331`** (F0–F4 lezárva).*
*Végrehajtás: Claude Code, a repó gyökeréből, egy menetben. A chat-menet nem hajtja végre — ez a brief a bemenete.*
*Előzmény: `ATALAKITASI_TERV.md.md` 6. szakasz, F5. A három F4-en kívüli nyitott tétel (HODIT-001 témája, HAMART-001 betöltése, `Karoli_Strong_kivonat.tsv` forrás-ütközése) ettől a fázistól független, és ez a brief nem nyúl hozzájuk.*

---

## 0. Miért tér el ez a brief a terv F5-szakaszától

A terv öt tételt sorol fel. Az `f425331`-en mérve **kettő elavult**, és van egy **harmadik, a tervben nem szereplő ütközés**, amely nélkül a sablon az F4 után tiltott műveletre utasít.

**Egy — sorszám.** A terv az F5.1-nél „a 123. sort” nevezi meg. A kétértelmű mondat ma a **130. sorban** áll. Ez a brief ezért szöveg-horgonnyal hivatkozik, nem sorszámmal.

**Kettő — az F5.5 már teljesült.** A terv szerint a v15 magyarítási szabály „ma csak az opus-ágon él”. A `main` sablonjában viszont már benne van: a v15 fejléc-bejegyzésben és a 130. sor végén is. A `bun-gyuruzese-20260911-opus` ág és a `main` között a `sablonok/` alatt **nincs eltérés**. Az F5.5 ezért ellenőrzéssé szűkül.

**Három — a Lezárási checklist generált blokkok kézi szerkesztését írja elő.** Az F4 élesítette a motívumnapló négy blokkját, az index és a `NYITOTT_FELADATOK.md` blokkját. A `CLAUDE.md` („Rétegek”) szerint ezeket kézzel szerkeszteni tilos. A sablon Lezárási checklistjének 2., 3., 5., 6. és 8. lépése viszont éppen ezeket írja át kézzel. Ugyanide tartozik két apróbb elavulás: a 9. lépés a napló fejléc-changelogjára mutat, holott az F0.6 külön fájlba szervezte ki; a sablon pedig háromszor „LEZÁRVA”-t ír, holott az F3.1 óta háromértékű státusz van. Ez az **F5.6** új tétel — külön commitban, hogy elvethető legyen.

**Mellékes lelet.** A Minőségi kapu bevezetője „öt ellenőrzés”-t mond, a záró mondata „mind a hat kritérium”-ot, a lista pedig Q1–Q6, azaz hat tétel. Az F5.4 ezt úgyis érinti, mert új kritériumot vesz fel.

---

## 1. Mért kiindulási állapot *(`f425331`)*

### 1.1 A sablon

- Verzió: **v15** (2026.09.11), a fájl 428 sor.
- Az 1. pont táblázata hét oszlopos: `Igehely | Kapcsolódás | PaRDeS-szint, ahol felmerült | Strong-szám(ok) | BDB-entry-id | Sense-szám | Jelentés-szöveg (BDB eredeti + magyar)`.
- A kétértelmű mondat a 130. sorban kezdődik: *„Az utolsó négy oszlop opcionális kitöltésű (nem minden előfordulásnál áll rendelkezésre BDB-adat), de ha…”*
- Minőségi kapu: Q1–Q6, a bevezető „öt”-öt mond.
- Lezárási checklist: 12 lépés. „LEZÁRVA” a 209., 261. és 335. sorban fordul elő.
- A `general.py` 697. sora a sablon „Kötelező napló” bekezdésére hivatkozik. Ezt a bekezdést az F5 nem érintheti (K9).

### 1.2 Verzió-címkék a lezárt tanulmányokban

| Fájl | Címke | Hol áll | §1 táblázat oszlopszáma |
|---|---|---|---|
| `Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` | v14 szerint | fejléc | 7 |
| `Hadesz_Seol_tematikus.md` | v14 szerint | fejléc + Minőségi kapu címsor | **3** |
| `Tehom_tematikus.md` | v14 szerint | fejléc + Minőségi kapu címsor | **3** |
| `Melkizedek_tematikus.md` | v12 szerint | fejléc + Lezárási checklist címsor | 6 |
| `Isten_fiai_Nefilim_Gibborim_tematikus.md` | v14 szerint | csak Minőségi kapu címsor | 3 |
| `Rafaim_tematikus.md` | v14 szerint | csak Minőségi kapu címsor | 3 |
| `Pneuma_pszukhe_megkulonboztetes_tematikus.md` | — | — | 3 |
| `Segitsegul_hivni_az_Urat_tematikus.md` | — | — | 6 |

A terv F5.2-es indoka ezzel igazolt: a Hádész és a Tehóm fejlécben állítja a v14-et, miközben háromoszlopos a táblázata. Az Isten fiai és a Rafaim esete más: ott a címke csak a Minőségi kapu címsorában áll, tehát csak a kapura vonatkozó állítás. Az F5.2 szabálya ezt a különbséget rögzíti.

### 1.3 A Lezárási checklist és az élesített generált blokkok

| Lépés | Mit ír elő ma | Az érintett tartalom ma | Ütközik? |
|---|---|---|---|
| 2 | a Tematikus áttekintés jelölése „✅ LEZÁRVA”-ra | `naplo#attekintes` blokk | **igen** |
| 3 | a Kulcsszó-index előfordulás-száma | `naplo#kulcsszo_index` blokk | **igen** |
| 4 | a Kulcsszavak részletesen bejegyzés | nem generált; archív másolata a `motivumok/[ID].md`-ben | nem (l. N3) |
| 5 | a Könyv szerinti index | `naplo#konyv_index` blokk | **igen** |
| 6 | az áthelyezés a ⭐ küszöbből | `naplo#kuszob` blokk | **igen** |
| 7 | az Előrejelzett motívumok | nem generált | nem |
| 8 | új sor a `Lezart_tematikus_tanulmanyok_index.md`-ben | `index` blokk | **igen** |
| 9 | a motívumlog fejléc-changelogja | a changelog ma `motivumlog/PaRDeS_motivumok_CHANGELOG.md` | elavult hivatkozás |

A kereszthivatkozás-naplók (G5) és a study 1. pontja (G6) renderelője elkészült, de **nincs élesítve**. Ezek tehát ma még kézzel írt tartalmak, az F5 sem kezeli őket generáltként.

### 1.4 Az eszközréteg, amelyre a checklist hivatkozhat

- `eszkozok/lekerdez.py` alparancsai: `gerinc`, `scan` (`--szakasz` opcióval), `kollokacio`, `igealak`, `lxx-hid`, `tsk`, `karoli`, `domen`.
- A `domen` ma **nem ad eredményt**: az `adat/datasetek.tsv` szerint az SDBH és az SDGNT állapota `hianyzik`, és a parancs ezt ki is írja.
- Az `adat/datasetek.tsv` tartja a 4.3-as mátrixot tanulmány-típusonként. A `study_tipus = tematikus` csoportban 17 sor van, benne a `Karoli_Strong_kivonat` `oroklott` / `generalt_nezet` jelöléssel.

---

## 2. Mit kell csinálni

Minden tétel **egyetlen fájlt** érint: `sablonok/4_PaRDeS_tematikus_sablon.md`. Más fájl nem változik (K10).

A sablon verziója **v16** lesz. A fejléc-bejegyzést az első tartalmi commit (F5.1) hozza létre, a további tételek pedig ugyanahhoz a bejegyzéshez fűzik a saját tagmondatukat. Az F5 így egyetlen verzióugrás, a commit-történet viszont tételenként olvasható marad.

### Tétel F5.0 — előfeltétel-mérés *(nincs commit)*

Mérd újra az 1.1–1.4 pont minden állítását. Ha bármelyik eltér — más a sorszám, más a státusz, van új generált blokk, változott a `lekerdez.py` parancslistája —, **állj meg, és jelentsd az eltérést**, mielőtt írnál. A brief szövegei ezekre a tényekre épülnek.

### Tétel F5.1 — az 1. pont oszlop-szabálya

A 130. sor elején álló mondatot (horgony: *„Az utolsó négy oszlop opcionális kitöltésű (nem minden előfordulásnál áll rendelkezésre BDB-adat), de ha a 0. pont gyűjtése vagy a friss keresés során előkerül, itt rögzítendő,”*) cseréld erre:

> **Mind a hét oszlop kötelezően jelen van.** Az utolsó négy oszlop (Strong-szám(ok), BDB-entry-id, Sense-szám, Jelentés-szöveg) cellája üresen maradhat — ilyenkor `—` áll benne, mert nem minden előfordulásnál áll rendelkezésre BDB-adat —, de **az oszlop nem hagyható el**, és nem vonható össze másik oszloppal. Ha az adat a 0. pont gyűjtése vagy a friss keresés során előkerül, itt rögzítendő,

A bekezdés további része (*„**külön oszlopokban** — a `Bibliai_Motivumlexikon_tervezesi_naplo.md`…”* és a v15-ös magyarítási mondatok) **szó szerint marad**. A táblázat fejlécsora nem változik.

A szabály nem visszamenőleges. A v15-ös előzményhez igazodva a v16 bejegyzés ezt ki is mondja: új vagy szerkesztés alatt álló study-nál kötelező, a lezártakat nem kell átírni.

### Tétel F5.2 — a verzió-címke szabálya

A Minőségi kapu szakasz vége után, a `### Lezárási checklist` címsor elé kerül egy új alszakasz:

> ### Verzió-címke („v‹N› szerint”)
>
> A „`4_PaRDeS_tematikus_sablon.md` v‹N› szerint” megjelölés **tanúsítás, nem dátum**. Csak akkor írható fel vagy át, ha a megfelelőségi ellenőrzés a v‹N› **minden szakaszára** lefutott. Részleges kör esetén a címke: `v‹N› részleges (érintett: …)`, a zárójelben a ténylegesen ellenőrzött szakaszokkal.
>
> A címke hatóköre az a szerkezeti egység, amely viseli. A study fejlécében az egész study-ra vonatkozik; a Minőségi kapu vagy a Lezárási checklist címsorában csak arra a kapura, illetve listára.
>
> Régebbi címke nem írható át újabbra ellenőrzés nélkül. A régi címke akkor is igaz marad, ha a sablon azóta újabb verzióra lépett.
>
> *(A szabályt megalapozó konkrét eset: 2026.09.15-én a `Tehom_tematikus.md` és a `Hadesz_Seol_tematikus.md` fejléce „v14 szerint”-et állított, miközben az 1. pont táblázata háromoszlopos volt, a v14 pedig hetet ír elő.)*

A Lezárási checklist végére új, **13.** lépés kerül: *„**13. Verzió-címke** — a study fejlécének és a kapu-címsoroknak a címkéje a »Verzió-címke« alszakasz szerint.”*

A lezárt study-k címkéit ez a tétel **nem** írja át (l. §5 és N1).

### Tétel F5.3 — a hétlépéses protokoll checklistként

Az 1. pont `### Friss, teljes körű keresés` alszakaszának első bekezdése után, a „**Kötelező napló:**” bekezdés elé kerül:

> **Kutatási protokoll — hét lépés, kötött sorrendben.** A determinisztikus lépések az `eszkozok/lekerdez.py` parancsaival futnak. Minden futás saját proveniencia-sort ír ki (`scope=… | forras=… | ts=…`), és ez a sor szó szerint a kereszthivatkozás-naplóba kerül. Ahol nem futott lekérdezés, ott az állítás értelmezésként jelölendő.
>
> - [ ] **P1. Gerinc-metszet** — `python eszkozok/lekerdez.py gerinc "<szakasz>" "<szakasz>" …`. A levezetést **akkor is dokumentálni kell, ha az eredmény üres vagy triviális.** Az üres metszet maga is lelet: a motívum szerkezeti, nem lexikai, ezért a P2 a szemantikai mező szerint építi fel a gerincet.
> - [ ] **P2. Szemantikai mező-hipotézis** — generatív lépés, nincs parancsa. A mező szavai a naplóba kerülnek. A `lekerdez.py domen` ma nem ad eredményt, mert az `adat/datasetek.tsv` szerint az SDBH/SDGNT állapota `hianyzik`. Amíg ez így áll, gépi doménre hivatkozni nem lehet.
> - [ ] **P3. Teljes scan** — `python eszkozok/lekerdez.py scan <Strong>` minden mező-szóra. A `--szakasz` szűkítéssel futott scan eredménye nem nevezhető „teljes”-nek; a proveniencia `scope` mezője ezt gépileg mutatja.
> - [ ] **P4. Kollokáció** — `python eszkozok/lekerdez.py kollokacio <Strong_A> <Strong_B>`.
> - [ ] **P5. Igealak-szintű ellenőrzés** — `python eszkozok/lekerdez.py igealak <Strong>`.
> - [ ] **P6. LXX-híd** — `python eszkozok/lekerdez.py lxx-hid "<igehely>"`; kötelező, ha a study bármely ÚSZ-sort állít (l. Q7).
> - [ ] **P7. Nevesített tanító** — önálló menet, saját fájl, az 5. pont „Nevesített tanítói egyezés-keresés módszere” szerint.
>
> A Q2-es négyforrásos audit támogató parancsai: `lekerdez.py tsk "<igehely>"` és `lekerdez.py karoli "<igehely>"`.

A „Friss, teljes körű keresés” meglévő első bekezdése, amely a `PaRDeS_gyorsreferencia.md` négyforrásos módszertanára utal, **marad**. A protokoll kiegészíti, nem váltja ki; a gyorsreferencia összehangolása nem F5-feladat (§5).

### Tétel F5.4 — a dataset-mátrix a Minőségi kapuban

**a) Új kritérium** a Q6 után:

> - [ ] **Q7. Dataset-lefedettség indokolt és ellenőrizhető** — az `adat/datasetek.tsv` `study_tipus = tematikus` sorai szerint. A mátrixot ez a tábla tartja; a sablon szándékosan nem másolja.
>   - `mindig`: a lefutás proveniencia-sorral dokumentált.
>   - `felteteles`: vagy a lefutás dokumentált, vagy egy mondat rögzíti, hogy a feltétel nem áll fenn (pl. „a study nem állít ÚSZ-sort” → TAGNT és LXX nem kötelező).
>   - `ajanlott`: a használat vagy a kihagyás jelölve. `allapot = hianyzik` esetén a kihagyás nem bukás, de a study nem hivatkozhat a datasetre.
>   - `korlatos` állapot (KJV/ASV Strongs): a lefedett könyveken kívül nem épülhet rá „teljes” állítás.
>   - `oroklott`: olvasható, a study nem írja.
>
>   A kapu elbukik, ha egy `mindig` sor nyom nélkül marad, vagy ha egy `felteteles` sor feltétele fennáll, de nincs lefutás.

**b) Számjavítás:** a bevezető „ez az öt ellenőrzés” → „ez a hét ellenőrzés”; a záró „Ha mind a hat kritérium teljesül” → „Ha mind a hét kritérium teljesül”.

A Q2 szövege nem változik. A Q2 a négy „mindig” forrás auditjának *dátumát és minősítő sorait* kéri, a Q7 a *teljes mátrix indokoltságát*.

### Tétel F5.5 — a v15 átvezetésének ellenőrzése *(várhatóan nincs commit)*

```bash
git fetch origin bun-gyuruzese-20260911-opus
git diff --stat main origin/bun-gyuruzese-20260911-opus -- sablonok/
```

Ha a kimenet üres, a tétel teljesült: a zárójelentés egy mondatban rögzíti, commit nincs. Ha nem üres, **ne vezess át semmit**. Listázd az eltérő fájlokat és hunkokat, és állj meg; az átvezetésről a chat-menet dönt.

### Tétel F5.6 — a Lezárási checklist és a 6. pont összehangolása a generált réteggel

A lépések **sorszáma nem változik**, mert a sablon korábbi changelog-bejegyzései sorszámmal hivatkoznak rájuk (pl. „12. pont”). A megszűnő lépések helyén rövid jelölés marad.

| Lépés | Új szöveg (lényeg) |
|---|---|
| **2** | **Adatréteg frissítve** — a minősített jelöltek a `adat/jeloltek.tsv`-ben; a `dontes=beépítve` sorok előléptetve az `adat/elofordulasok.tsv`-be; a motívum `statusz` / `statusz_verzio` / `statusz_datum` mezője az `adat/motivumok.tsv`-ben, az `adat/SEMA.md` 2.1–2.2 szerint. Lezáráskor a státusz `publikálható`. |
| **3** | **Generált blokkok újragenerálva** — `python eszkozok/general.py --cel naplo`, `--cel index`, `--cel nyitott`, és a diff soronként átnézve. A motívumnapló Tematikus áttekintés, ⭐ Emlékeztető küszöb, Kulcsszó-index és Könyv szerinti index blokkja, valamint a `Lezart_tematikus_tanulmanyok_index.md` és a `NYITOTT_FELADATOK.md` generált blokkja **kézzel nem szerkeszthető** (`CLAUDE.md`, Rétegek). Ha a generált érték hibás, a tábla javul, nem a blokk. |
| 4 | a „Motívumlog 3. szekció (Részletes kulcsszó-magyarázatok)” megnevezés helyett a tényleges címsor: „Kulcsszavak részletesen”; a tartalom egyébként változatlan |
| **5** | *(megszűnt — a Könyv szerinti index generált blokk, a 3. lépés fedi)* |
| **6** | *(megszűnt — az ⭐ Emlékeztető küszöb generált blokk, a státusz alapján a 3. lépés fedi)* |
| 7 | a „Motívumlog 6. szekció” megnevezés helyett a tényleges címsor: „Előrejelzett, konkrét igehelyen megerősítendő motívumok”; a tartalom változatlan |
| **8** | *(megszűnt — az index generált blokk, a 3. lépés fedi)* |
| **9** | a „Motívumlog fejléc-changelog” helyett: `motivumlog/PaRDeS_motivumok_CHANGELOG.md` |
| 11 | kiegészül: „…a `lekerdez.py` proveniencia-soraival (l. P1–P6)” |

**A 6. pont és a Minőségi kapu:**

- A 6. pont első bekezdése („lezárt/önállóan feldolgozott témaként kell megjelölni”) → a státusz az `adat/motivumok.tsv`-ben `publikálható`-ra áll, a napló jelölése ebből generálódik.
- Az „**Index-frissítés:**” bekezdés → az index generált, a Lezárási checklist 3. lépése frissíti.
- A 209. sor „✅ LEZÁRVA státuszú” → „`publikálható` vagy `véglegesített` státuszú”.
- A 261. sor „LEZÁRVA jelölnénk” → „`publikálható` státuszra állítanánk”.
- A 335. sor „✅ LEZÁRVA-ra” a 2. lépés átírásával megszűnik.

A Lezárási checklist **1. lépése** (`/mnt/user-data/outputs/` útvonal) és a **12. lépés** nem változik (l. N2).

---

## 3. Elfogadási kritériumok

Mind gépileg ellenőrizhető a munkapéldányon.

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K1 | A régi mondat eltűnt, az új bekerült | `grep -c "opcionális kitöltésű" sablonok/4_PaRDeS_tematikus_sablon.md` = 0; `grep -c "Mind a hét oszlop kötelezően jelen van"` = 1 |
| K2 | Az 1. pont fejlécsora és a v15 magyarítási mondatai változatlanok | a `git diff` ezeket a sorokat nem érinti |
| K3 | A verzió-címke alszakasz és a 13. lépés jelen van | `grep -c "### Verzió-címke"` = 1; `grep -c "13. Verzió-címke"` = 1 |
| K4 | A protokoll minden hivatkozott parancsa létezik | `python eszkozok/lekerdez.py <parancs> --help` kilépési kódja 0 mind a hét parancsra (`gerinc`, `scan`, `kollokacio`, `igealak`, `lxx-hid`, `tsk`, `karoli`) |
| K5 | A Minőségi kapu számai egyeznek | a Q-tételek száma = 7, és a szöveg „hét ellenőrzés” / „mind a hét kritérium”; `grep -c "öt ellenőrzés"` = 0 |
| K6 | A Q7 nem másolja a mátrixot | a sablonban nincs dataset-táblázat; az `adat/datasetek.tsv` hivatkozás jelen van |
| K7 | Egyik checklist-lépés sem ír elő generált blokkba írást | a 2–9. lépésben nem szerepel „frissítve” / „áthelyezve” / „új sor” generált szakaszra vonatkoztatva; a 3. lépés a `general.py`-t nevezi meg |
| K8 | A „LEZÁRVA” címke eltűnt a sablonból | `grep -c "LEZÁRVA"` = 0 — ezért a v16 fejléc-bejegyzés sem idézi a szót, hanem „a régi kétértékű címke” néven hivatkozik rá |
| K9 | A `general.py` által hivatkozott „Kötelező napló” bekezdés érintetlen | a `git diff` a bekezdést nem érinti |
| K10 | Csak a sablon változott | `git diff --name-only f425331..HEAD` = `sablonok/4_PaRDeS_tematikus_sablon.md` |
| K11 | A v16 fejléc-bejegyzés minden tartalmi tételt megnevez | F5.1, F5.2, F5.3, F5.4, F5.6 mind szerepel; a visszamenőleges hatály kizárása kimondva |

---

## 4. Commit és push

Tétel-szintű commitok, magyar üzenettel, UTF-8 fájlból (`git -c i18n.commitEncoding=UTF-8 commit -F commit_uzenet.txt`), a `CLAUDE.md` szerint:

```
F5.1: tematikus sablon v16 — az 1. pont hét oszlopa kötelező, a cella lehet „—"
F5.2: tematikus sablon — verzió-címke szabály + 13. checklist-lépés
F5.3: tematikus sablon — hétlépéses kutatási protokoll (P1–P7) az 1. pontban
F5.4: tematikus sablon — Q7 dataset-lefedettség, a kapu számai javítva
F5.6: tematikus sablon — Lezárási checklist és 6. pont a generált réteghez igazítva
```

Az F5.0 és az F5.5 nem commitol, ha nincs eltérés. **Push csak külön kérésre.**

---

## 5. Amit ez a brief szándékosan nem kér

- **A lezárt study-k verzió-címkéinek átírását.** A Hádész, a Tehóm és a többi fájl a forrásréteg része; az átcímkézés tartalmi ítélet (l. N1).
- **A `PaRDeS_gyorsreferencia.md`, a `2_PaRDeS_bovitett_sablon.md` és a `6_PaRDeS_lexikon_oldal_sablon.md` összehangolását.** A terv F5-je a tematikus sablont nevezi meg.
- **Dataset-lefedettséget ellenőrző eszközt.** A terv szerint ez gépileg ellenőrizhető; az eszköz megírása viszont kód, nem sablon-munka (l. N5).
- **Az SDBH/SDGNT importját** — külön nyitott tétel.
- **A G5/G6 élesítését** és a `general.py` bármely módosítását.
- **Az F4 három nyitott tételét** (HODIT-001 és MENNY-001 témája, HAMART-001 betöltése, `Karoli_Strong_kivonat.tsv`).
- **A `CLAUDE.md` két eltérésének javítását** — csak jelentendő (l. N4).

---

## 6. Futtatás és modellválasztás

**Egy menet, Sonnet.** A terv D11-e szerint a migrációs menetek Sonneten futnak, és az F5 nem tartalmaz soronkénti tartalmi ítéletet. A szövegek a briefben készen állnak, a végrehajtás beillesztés és ellenőrzés.

**Megállási pontok:** az F5.0 után, ha bármi eltér; az F5.5-nél, ha az ág eltér; minden commit előtt a hozzá tartozó K-kritériumok.

### 6.1 A menet nyitó promptja

```
Olvasd el a CLAUDE.md-t, majd az F5_BRIEF.md-t teljes egészében.

1. F5.0: mérd újra a brief 1.1–1.4 pontjának minden állítását a mai main-en.
   Ha bármi eltér, állj meg és jelentsd — ne írj semmit.
2. F5.1 → F5.2 → F5.3 → F5.4: a briefben megadott szövegeket illeszd be a
   megadott horgonyokhoz, szó szerint. A v16 fejléc-bejegyzést az F5.1 hozza
   létre, a többi tétel ehhez fűzi a saját tagmondatát. Minden tétel után
   futtasd a rá vonatkozó K-kritériumokat, és külön commitolj (UTF-8 fájlból).
3. F5.5: futtasd a két git-parancsot. Üres diff esetén egy mondat a
   zárójelentésbe, commit nincs. Nem üres diff esetén listázd, és állj meg.
4. F5.6: a brief táblázata szerint írd át a Lezárási checklistet és a
   6. pont érintett bekezdéseit. A sorszámok maradnak. Utána K7, K8, K9, K10, K11.

Push nincs. A végén zárójelentés: commit-hash-ek, K1–K11 eredménye
kritériumonként, és minden eltérés, amit menet közben találtál.
```

---

## Döntésnapló

| # | Döntés | Indok |
|---|---|---|
| D1 | Szöveg-horgony a sorszám helyett | A terv „123. sor”-a már elcsúszott (ma 130.); egy horgony nem csúszik el. |
| D2 | Az F5.5 ellenőrzéssé szűkül | A v15 szabály a `main`-en van, a `sablonok/` alatt nincs eltérés az opus-ágtól (mérve `f425331`-en). |
| D3 | Új tétel: F5.6 | Enélkül a sablon a `CLAUDE.md` által tiltott kézi szerkesztést írja elő öt lépésben. Külön commit, tehát elvethető. |
| D4 | Az F5.6 megtartja a lépések sorszámát | A sablon régebbi changelog-bejegyzései sorszámmal hivatkoznak; az átszámozás csendben elavítaná őket. |
| D5 | A Q7 az `adat/datasetek.tsv`-re hivatkozik, nem másolja | Egy igazságforrás: a mátrix a táblában már karbantartott, egy másolat driftelne. |
| D6 | Az F5.1 és az F5.2 nem visszamenőleges | A v15 előzményét követi; a lezárt study-k átírása tartalmi ítélet. |
| D7 | Egyetlen v16 verzióugrás, tételenként bővülő bejegyzéssel | Egy fázis, egy menet; a commit-történet ettől még tételenként olvasható. |
| D8 | Lezáráskor a státusz `publikálható` | `SEMA.md` 2.1.1: a kapuzott, de újranyitható tanulmány értéke; a `véglegesített` külön döntés. |
| D9 | Egy menet, Sonnet | D11 (terv); nincs soronkénti tartalmi ítélet. |

### Nyitott, a briefben szándékosan el nem döntött kérdések

- **N1 — A lezárt study-k címkéi.** A Hádész és a Tehóm fejléce „v14 szerint”-et állít háromoszlopos táblázattal. Mi történjen: átcímkézés `v14 részleges (érintett: …)`-ra, a táblázat hétoszloposra bővítése (a G6 élesítésével ez generálható volna), vagy semmi? Felhasználói döntés.
- **N2 — A Lezárási checklist 1. lépése.** A `/mnt/user-data/outputs/` a chat-korszak útvonala; a tanulmányíró menetek ma Claude Code-ban, a repóban futnak. Átírandó-e `tematikus_lezart/`-ra?
- **N3 — A „Kulcsszavak részletesen” kanonikus helye.** A napló szakasza nem generált, a `motivumok/[ID].md` archív másolatot tart belőle. A terv 1.C szerint ez a szakasz a forrásrétegből olvad be. Amíg ez nincs élesítve, a 4. lépés a naplót szerkeszti — ez rendben van-e?
- **N4 — A `CLAUDE.md` két eltérése.** A forrásréteg útvonala a `CLAUDE.md`-ben `motivumlog/[ID].md`, a valóságban `motivumok/[ID].md` (G0 döntés). A generált jelölést `# GENERÁLT: …` formában írja le, a valóságban `<!-- GENERÁLT-KEZDET: … -->`. Mindkettő egysoros javítás, de nem sablon-munka.
- **N5 — A dataset-lefedettség gépi ellenőrzése.** Melyik fázisba kerüljön az eszköz (F6 előtt, vagy az F7 üzemmenet része)?
- **N6 — A G6 fejléc eltérése.** A `general.py` study-renderelője az utolsó oszlopot „Jelentés-szöveg (EN + HU)” néven írja, a sablon „Jelentés-szöveg (BDB eredeti + magyar)” néven. A G6 nincs élesítve, tehát ma nincs kár, de az élesítés előtt egyeztetendő; javaslat: a generátor igazodjon a sablonhoz.
