# PaRDeS-projekt: STEPBible/SzPA integráció és GitHub-architektúra — döntési összefoglaló

*v26 — 2026.08.24 (önellenőrzési mechanizmus és egységes megbízhatósági jelölés bevezetve a Károli-Strong join-tábla építésébe: (1) `konkordancia/Karoli_Strong_kivonat.tsv` oszlopszerkezete bővítve egy 6. "Megbízhatóság" oszloppal ["magas"/"közepes"/"bizonytalan"/"—"]; (2) `konkordancia/Validacios_naplo.md` létrehozva, visszamenőleg rögzítve a három korábbi, chat-munkamenetben elvégzett kézi validáció [Pro.23.1-9, Act.1.1-4, Gen.1.2-4]; (3) új 4.13 alpont — miért a KJV/ASV a kereszt-ellenőrző forrás [nem a STEPBible, ami maga az elsődleges bemenet, körkörös lenne], az 5 lépéses megbízhatósági döntési logika, és a 10. soronkénti mintavételes validáció szabálya; (4) `Join_tabla_lekerdezo_promptok.md` felvéve a repó gyökerébe, újrafelhasználható lekérdező promptokkal a join-tábla állapotának bármikori ellenőrzéséhez)*

*v25 — 2026.08.24 (nyomon követési mechanizmus bevezetve a Károli-Strong join-tábla építésére: (1) `Join_tabla_folyamat_magyarazat.md` felvéve a repó gyökerébe, a kétoszlopos [Strong+Károli] join gyakorlati folyamatát írja le bővített és tematikus sablonnál; (2) `konkordancia/Karoli_Strong_kivonat.tsv` létrehozva üres, fejléces váltként [Igehely | Strong-szám | Károli-szó | Azonosítás módja | Forrás-tanulmány]; (3) `motivumlog/PaRDeS_motivumok.md` "Feldolgozott igeszakaszok" táblázata kiegészítve egy "Károli-Strong sorok" oszloppal, minden meglévő sornál "—" [nincs visszamenőleges becslés]; (4) új 4.12 alpont — 66 könyves join-tábla lefedettségi táblázat, jelenleg minden könyvnél 0%; (5) a 8. szakasz "négy lezárt tematikus tanulmány" nyitott pontja részletes, pipálható checklistre cserélve, könyvenkénti bontásban)*

*v24 — 2026.08.24 (Károli-specifikus kereszthivatkozás-adat legenerálva a teljes Bibliára a krisek/HunKar OSIS-forrásból — `konkordancia/Karoli_kereszthivatkozasok.tsv` [31 168 vers feldolgozva, 19 817 versnek van kereszthivatkozása, 32 407 sor összesen, ~1,1 MB, közkincs]; validálva: Gen.1.1-hez pontosan 8 kereszthivatkozás generálódott, számjegyre egyezve a korábban kézzel ellenőrzött referenciával; az OSIS-forrás saját könyv-kódjai [pl. `Exod`, `Acts`, `Ps`] STEPBible-natívra konvertálva [`Exo`, `Act`, `Psa`] egy 66 elemű, kánoni sorrendű megfeleltető táblával, 0 konverziós hibával; dokumentálva `konkordancia/Karoli_kereszthivatkozasok_README.md`-ben, explicit jelezve, hogy ez csak jelöltlista a 3/b ponthoz, a tartalmi értékelés kézi lépés marad — a 0. szakasz dataset-leltárának 8. sora "Letöltve, generálva (teljes Biblia)" státuszra frissítve)*

*v23 — 2026.08.24 (SzPA-integráció felfüggesztve, bizonytalan időre, felhasználói döntés alapján — a privát repó és a két-táblás SzPA-terv változatlanul érvényes marad, csak az aktív bővítés szünetel; a meglévő minták [Péld 1:1-9, ApCsel 1:1-4] referenciaként megmaradnak; jövőbeli join-tábla-építés ezalatt "csak Károli" [kétoszlopos] formában, publikus repóban készül — a 0. szakasz 3. és 4. sora "(felfüggesztve)" jelzéssel kiegészítve, új nyitott pont felvéve a 8. szakaszba)*

*v22 — 2026.08.24 (a korábban eldöntött, de a sablonfájlokba be nem épített STEPBible-lépések ténylegesen beillesztve három sablonba: `2_PaRDeS_bovitett_sablon.md` v7→v8 [kulcsszó-kiválasztás 6 szempontos kritériumlistája a 2. pontban + kötelező STEPBible TAGNT/TAHOT-ellenőrzés a 3/b pont végén], `4_PaRDeS_tematikus_sablon.md` v3→v4 [kötelező STEPBible-egyezés-ellenőrzés az 1. pont táblázata után + új 11. pont a Lezárási checklistben — előzetesen ellenőrizve, hogy a checklist ténylegesen csak 10 pontos volt, nincs duplikáció], `5_Melyelemzes_prompt_sablon.md` v2→v3 [STEPBible-lekérdezés a 2. pont végén] — a döntési fájl 8. szakaszának megfelelő nyitott pontja lezárva)*

*v21 — 2026.08.24 (két új felismerés: (1) új 4.11 alpont — a projekt saját, tartalom-alapú Károli-Strong párosítási módszere [4.2] első ízben külső, független referenciával ellenőrizve 1Móz 1:3-4-en, 13/14 szó pontos egyezéssel, beleértve két kettős-taggelésű esetet is [„látá" = H0853+H7200; „között...között" szétosztása], az egyetlen eltérés [„jó" = H2896 vs H2895] dokumentált, legitim kettős lehetőségként azonosítva — megerősíti a 4.7-es döntés technikai megbízhatóságát; (2) a 4.7 pont kiegészítve egy másodlagos, szövegszerűen eltérő Károli-revízió azonosításával [„Revideált Károli", Veritas Kiadó 2011, © védett, nem közkincs, karolibiblia.hu] — nyitott pontként rögzítve a 8. szakaszban, mert a jelenlegi publikus Karoli_1908.tsv NEM cserélendő rá jogosultság nélkül)*

*v20 — 2026.08.24 (KJV-Strongs és ASV-Strongs 1Mózes [50 fejezet] letöltve és a publikus repóba generálva, ugyanazzal a validált parszoló-logikával, mint a Példabeszédeknél — `konkordancia/KJV_Strongs_Genesis.tsv` [15098 sor] és `konkordancia/ASV_Strongs_Genesis.tsv` [14917 sor]; validálva Gen.17.5-nél [Ábrám→Ábrahám névváltás verse] a `TIPNR_kivonat.tsv`-vel kereszt-ellenőrizve, H87/H85 mindkét oldalon megjelenik; **igehely-formátum egységesítve mind a négy KJV/ASV-fájlban STEPBible-natívra** [`Gen.1.1`, `Pro.23.7`], felhasználói döntéssel — a két korábbi Példabeszédek-fájl Igehely-oszlopa visszamenőleg konvertálva `Proverbs N:V`-ről `Pro.N.V`-re, minden más adat változatlan; a döntés és indoklás dokumentálva `konkordancia/README.md`-ben — a 0. szakasz dataset-leltárának 5. és 6. sora "Letöltve, validálva (Példabeszédek + 1Mózes)" státuszra frissítve)*

*v19 — 2026.08.24 (három hátralévő publikus dataset legenerálva — `konkordancia/Karoli_1908.tsv` [scrollmapper/HunKar, közkincs, 31 170 vers, validálva: 1Móz 1:1 = "Kezdetben teremté Isten az eget és a földet."]; `konkordancia/TIPNR_kivonat.tsv` [STEPBible-Data CC BY, 35 522 sor, validálva: Ábrahám/H0085 és Ábrám/H0087, ill. Sára/H8283 és Szárai/H8297 külön Strong-számmal és teljes előfordulási listával szerepel]; `konkordancia/Konyv_normalizalo_tabla.tsv` [STEPBible README alapján, mind a 66 könyv, Gen→1Móz és Pro→Péld ellenőrizve; két korpuszbeli ellentmondás — Máté/Mt és Ezék/Ez — felhasználói egyeztetéssel eldöntve: Mt, Ez]; dokumentálva `konkordancia/Karoli_TIPNR_Normalizalo_README.md`-ben — a 0. szakasz dataset-leltárának 2., 10. és 11. sora véglegesített státuszra frissítve)*

*v18 — 2026.08.24 (TAHOT/TAGNT kivonat legenerálva a teljes ÓSZ+ÚSZ-re a STEPBible-Data nyersadatból, publikus repóba — `konkordancia/TAHOT_kivonat.tsv` [283 734 nyers sor → 435 723 sor, 39 könyv, 21 178 igehely] és `konkordancia/TAGNT_kivonat.tsv` [141 720 sor, 27 könyv, 7 948 igehely]; mezőazonosítás dokumentálva `konkordancia/TAHOT_TAGNT_README.md`-ben; validálva mindhárom feladat-referenciával [Gen.1.1 2. szó=H7225/first/beginning; Pro.1.1 1. szó=H4912/"[the] proverbs of"; Heb.4.12 ψυχῆς=G5590/"of soul"/NA28+NA27+Tyn+SBL+WH+Treg+TR+Byz] számjegyre pontos egyezéssel, valamint kereszt-ellenőrizve Pro.23.7-nél a KJV_Strongs_Proverbs.tsv hat Strong-számával — a 0. szakasz dataset-leltárának 1. sora "Letöltve, generálva (teljes ÓSZ+ÚSZ)" státuszra frissítve)*

*v17 — 2026.08.24 (összefésülve a Claude Code által commitolt v16-tal [claude.ai chat munkamenet]: pótolva a hiányzó 4.10 alpont [getbible.net API — megvizsgálva és lezárva, nincs Strong-szám, elsőkézből is megerősítve]; a 4.8/4.9 pontokban a `studybible.info/[KJV_Strongs|ASV_Strongs]/[Könyv]` könyv-szintű forrás lett az elsődleges, felváltva a biblehub.com/kjvs-t mint első helyen említett forrást; rögzítve a repó kisbetűs átnevezése `basesoft777/Bible-Study`-ra. Minden más korábbi tartalom [4.1-4.9, 0. szakasz, 7.1-7.2] már a Claude Code-os v16-ban is jelen volt, nem igényelt módosítást.)*

*v16 — 2026.08.24 (KJV-Strongs és ASV-Strongs teljes Példabeszédek [31 fejezet] letöltve és a publikus repóba generálva — `konkordancia/KJV_Strongs_Proverbs.tsv` [5945 sor] és `konkordancia/ASV_Strongs_Proverbs.tsv` [5872 sor], összesen 11817 adatsor; validálva a 4.8-as pontban rögzített Péld 23:7-es kézi referenciával, hat szóra pontosan egyezik — a 0. szakasz dataset-leltárának 5. és 6. sora "Letöltve, validálva (Példabeszédek)" státuszra frissítve)*

*v15 — 2026.08.23 (új 0. szakasz: összegző dataset-leltár táblázat a fájl elejére, hogy egy új munkamenet azonnal áttekintést kapjon mind a 11 azonosított/tervezett datasetről — hely, státusz, forrás, és a részletes indoklásra mutató hivatkozás — mielőtt a lenti szakaszok részletes tárgyalásába merülne)*

*Ez a fájl híd a claude.ai memóriarendszerében felhalmozott kontextus és a Claude Code / bármely jövőbeli munkamenet között. Célja, hogy egy új munkamenet — akár claude.ai chatben, akár Claude Code-ban — enélkül a beszélgetés-történet nélkül is teljes képet kapjon a meghozott döntésekről és azok indoklásáról.*

---

## 0. Dataset-leltár — gyors áttekintés

*Ez a szakasz csak összegzés; a részletes indoklás és a technikai formátum a lenti szakaszokban található (lásd a hivatkozott pontokat).*

| # | Dataset | Tartalom | Hely | Státusz | Forrás | Részletek |
|---|---|---|---|---|---|---|
| 1 | **TAGNT/TAHOT kivonat** | 8 oszlop: igehely, Strong, alak, kiejtés, szótő, szótári jelentés, angol gloss, kritikai kiadás | Publikus repó | Letöltve, generálva (teljes ÓSZ+ÚSZ) | STEPBible-Data (CC BY) | 2. szakasz |
| 2 | **Karoli_1908.tsv** | Igehely + teljes Károli-vers | Publikus repó | Letöltve, generálva (teljes Biblia, 31 170 vers) | scrollmapper/HunKar (közkincs) | 4.1, 4.7 |
| 3 | **SzPA versek + lábjegyzetek** | 2 tábla könyvenként (Példabeszédek, ApCsel) | Privát repó | Minta kész (1:1-9, 1:1-4), teljes könyv még nem (felfüggesztve) | Saját feltöltés (jogosult tulajdon) | 3. szakasz |
| 4 | **Összekapcsolt (join) táblák** | Strong + Károli + SzPA + azonosítás módja + megbízhatóság | Privát repó | Minta/demó szinten kész, generálás még nem indult (felfüggesztve) | Az 1-3. összefésülése | 4.1-4.2 |
| 5 | **KJV-Strongs** | Híd-forrás, Példabeszédek (31 fej.) + 1Mózes (50 fej.), szavankénti bontásban tárolva | Publikus repó | Letöltve, validálva (Példabeszédek + 1Mózes) | biblehub.com/kjvs, studybible.info/KJV_Strongs (közkincs) | 4.8 |
| 6 | **ASV-Strongs** | Második híd-forrás, Példabeszédek (31 fej.) + 1Mózes (50 fej.), kereszt-ellenőrzésre | Publikus repó | Letöltve, validálva (Példabeszédek + 1Mózes) | studybible.info/ASV_Strongs (közkincs) | 4.9 |
| 7 | **byztxt szövegkritikai variánsok** | Tényleges eltérő szövegváltozatok (nem csak "van/nincs") | Publikus repó | Azonosítva, beépítésre vár | byztxt/byzantine-majority-text (Unlicense) | 4.6 |
| 8 | **Károli-specifikus kereszthivatkozások** | Versenkénti hivatkozás-lista, szentiras.hu eredetű | Publikus repó | Letöltve, generálva (teljes Biblia, 32 407 sor) | krisek/HunKar (SWORD OSIS, közkincs) | 4.6 |
| 9 | **openbible.info kereszthivatkozások** | Szavazat-súlyozott hivatkozás-jelöltek | Publikus repó | Azonosítva, kiegészítő szerepű | scrollmapper (MIT) | 4.6 |
| 10 | **TIPNR névelőfordulások** | Tulajdonnév-alakváltozatok (pl. Ábrám/Ábrahám) | Publikus repó | Letöltve, generálva (teljes Biblia, 35 522 sor) | STEPBible-Data (CC BY) | 8. szakasz |
| 11 | **Könyv-rövidítés normalizáló tábla** | STEPBible angol ↔ magyar igehely-formátum | Publikus repó | Elkészült (mind a 66 könyv) | STEPBible README | 8. szakasz |

**Nem önálló dataset, csak referencia-eszköz** (nem kerül tárolásra nyers adatként):
- TBESH/TBESG/TFLSJ lexikonok — csak átfogalmazva idézhetők
- Biblia-Felfedező — kizárólag kézi ellenőrzésre (4.7-es döntés)
- TAGOT, TBCWG — jövőbeli, még nem elérhető STEPBible-fejlesztések

---

## 1. Architekturális váltás: GitHub mint elsődleges forrás

**Döntés:** a `project_knowledge_search` (Claude Projects szemantikus keresés) helyett a **GitHub-repó** (`basesoft777/Bible-Study`) grep-alapú keresése lesz az elsődleges módszer, minden munkamenet elején repó-klónozással/pull-lal.

**Fontos, gyakorlati megjegyzés:** a repó időközben átköltözött **kisbetűs** `basesoft777/Bible-Study` névre (korábban `Basesoft777/Bible-Study`) — a régi URL jelenleg még átirányít, de érdemes az új, kisbetűs formát használni jövőbeli klónozásnál/hivatkozásnál, nehogy az átirányítás egyszer megszűnjön.

**Indoklás:**
- A `project_knowledge_search` eddig is csak azokra a fájlokra terjedt ki, amiket ténylegesen visszatöltöttünk a Claude Projects-be — ez már eddig is következetlen volt (nem minden tanulmány került vissza)
- A motívumlog (`PaRDeS_motivumok.md`) **teljes fájlként beolvasva** jobb eredményt ad, mint egy szemantikus top-N töredék-keresés — a teljes napló-kontextus értelmezhető, összefüggések felismerhetők
- A grep **kiszámítható**: pontosan tudható, mi van a repóban és mi nem
- **Korlát, amit tudni kell:** egy adott tanulmány *mélyebb tartalmára* (konkrét érvelés, nevesített tanító pontos szövege) a motívumlog önmagában nem ad választ — ehhez a teljes tanulmányfájl szükséges, ami viszont szintén a repóban van, tehát elérhető, csak explicit meg kell nyitni.

**Gyakorlati következmény:** a Claude Projects-feltöltés gyakorlata megszűnhet/opcionálissá válhat; a GitHub lesz az egyetlen "igazságforrás".

---

## 2. STEPBible-integráció (nyilvános adat, nyilvános repó-rész)

**Mi:** STEPBible-Data (Tyndale House, Cambridge), CC BY licenc, TAGNT (görög ÚSZ) + TAHOT (héber ÓSZ).

**Végleges kivonat-formátum (8 oszlop):**
```
Igehely | Strong-szám | Ragozott alak | Kiejtés | Szótő | Rövid jelentés (szótári) | Angol tükörfordítás (kontextuális) | Kritikai kiadások (csak TAGNT-nál)
```
A 7. oszlop (**új**: kontextuális angol tükörfordítás, pl. "proverbs of", "to teach") **különbözik** a 6. oszloptól (szótári alapjelentés, pl. "proverb", "to teach"): míg a 6. oszlop a szó lexikai alapjelentését adja, a 7. oszlop azt mutatja, **hogyan szerepel a szó ténylegesen ebben a versben, ebben a mondatbeli szerepben** — ez teszi lehetővé a **tartalom-alapú (nem pozíció-alapú) párosítást** a magyar SzPA-szöveggel, mert a magyar és héber szórend gyakran jelentősen eltér (lásd a Péld 1:1-4 kísérletet, ahol a pozíció-alapú interpoláció megbukott, de az angol gloss alapú tartalom-keresés minden szónál sikeres párosítást adott).

A 8. oszlop (mely kiadásokban szerepel a szó: NA28, TR, Byz stb.) teszi lehetővé a szövegkritikai ⚠️ pontok automatikus jelzését — ha egy szó nem szerepel minden kiadásban, az valódi eltérés a Károli/TR-hagyomány és a modern kritikai szöveg között.

**Elhelyezés a repóban:**
```
Bible-Study/
├── konkordancia/
│   ├── TAGNT_kivonat.tsv
│   ├── TAHOT_kivonat.tsv
│   └── README.md (forrás, licenc, generálás dátuma)
```
Ez a rész **nyilvános** maradhat (CC BY engedi).

**Alternatív/kiegészítő források, megvizsgálva:**
- **OSHB/morphhb** (CC BY 4.0) — pontosabb morfológia, de nincs kiejtés/jelentés beépítve → csak másodlagos, finom nyelvtani kérdésekhez
- **byztxt/byzantine-majority-text** (Unlicense, a legtisztább licenc) — teljes bizánci alapszöveg, de a STEPBible TAGNT már jelzi a Byz/TR-jelenlétet is → csak akkor kell, ha a teljes bizánci szöveget kell megjeleníteni

**Sablon-integráció (még nem hajtva végre, de eldöntött terv):**
- **Tematikus sablon (4.):** kötelező STEPBible-ellenőrzés az 1. pontban (előfordulás-gyűjtés) + 11. checklist-pont a lezáráskor, ami dokumentálja, milyen paraméterekkel futott az ellenőrzés
- **Bővített sablon (2.):** 3/b pontban a "célzott konkordancia-ellenőrzés" mostantól STEPBible-alapú, nem csak `web_search`
- **Mélyelemzés sablon (5.):** 2. pontban (nyelvi/filológiai összevetés) kötelező STEPBible-adat beépítése a válaszba

**Visszamenőleges felülvizsgálat (még nem indítva el):** a már lezárt 4 tematikus tanulmány (tehóm, segítségül hívni, Rafeusok, hádész) nem STEPBible-lel készült — érdemes lenne visszamenőleg ellenőrizni őket.

---

## 3. SzPA-fordítások integrációja (védett, privát adat, privát repó-rész)

**Jogi alap:** a Szent Pál Akadémia Példabeszédek- és Apostolok Cselekedetei-fordítása **"Minden jog fenntartva"** védelem alatt áll. A felhasználó **legálisan megvásárolt, kereskedelmi példánnyal** rendelkezik mindkettőből — ez megalapozza a magáncélú másolás/feldolgozás elvét, **privát** (nem nyilvános) repóban tárolva.

**Két-táblás struktúra minden feldolgozott könyvhöz:**

*1. tábla — verses szöveg:*
```
Igehely | SzPA-szöveg (teljes vers)
```

*2. tábla — lábjegyzet-szótár:*
```
Igehely | Lj.# | Magyar kifejezés | Eredeti szó | Kiejtés | Jelentés-árnyalatok
```
(Az ApCsel-nél opcionális 7. oszlop: **Típus** — nyelvi/szómagyarázat vs. kontextuális/történeti megjegyzés, mert itt vegyesebbek a lábjegyzetek, mint a Példabeszédeknél.)

**Forrás-minőség, amit tudni kell:**
- **Példabeszédek** (2006, Grüll Tiborné fordítása, Hack Márta lektorálása): tiszta, jó minőségű digitális szöveg, academia.edu-ról (Eszter Csalog publikációi közt) és a felhasználó saját PDF-jéből is elérhető
- **ApCsel 1-14** (2002, Új Exodus XIII/2, Grüll Tibor és Csalog Eszter fordítása): **korábbi, nem a 2023-as végleges kiadás szövege** — a felhasználó saját PDF-je jobb minőségű, mint az academia.edu-s OCR-es verzió, de még ez is tartalmaz kisebb OCR-hibákat

---

## 4. Az összekapcsolás: STEPBible ↔ SzPA join Strong-szám alapján

### 4.1 Háromrétegű adatbázis-architektúra

**1. réteg — Forrás-táblák** (nem módosulnak, csak beolvasásra kerülnek):

*Nyilvános (STEPBible-kivonat, publikus repó-rész):*
```
TAHOT_kivonat.tsv / TAGNT_kivonat.tsv
Igehely | Szósorszám | Strong | Ragozott alak | Kiejtés | Szótő | Szótári jelentés | Angol tükörfordítás | Kritikai kiadás*
```
*(a Kritikai kiadás oszlop csak a TAGNT-nál releváns; a héber ÓSZ-nél nincs ilyen elágazás)*

*Privát (SzPA, privát repó-rész) — két külön tábla könyvenként:*
```
[könyv]_versek.tsv:       Igehely | SzPA-szöveg (teljes vers)
[könyv]_labjegyzetek.tsv: Igehely | Lj# | Magyar kifejezés | Eredeti szó | Kiejtés | Jelentés-árnyalatok
```

*Nyilvános (Károli 1908, publikus repó-rész) — új, negyedik forrás:*
```
Karoli_1908.tsv (vagy könyvenkénti bontásban): Igehely | Károli-szöveg (teljes vers)
```
**Eredet:** `scrollmapper/bible_databases` (GitHub, MIT licenc a repóra, a Károli-forrás önmaga **közkincs**) — "HunKar: Revideált Károli Biblia 1908", strukturált JSON/SQL/CSV formátumban, `{"verse": 1, "text": "Kezdetben teremté Isten az eget és a földet."}` séma szerint. Ez a projekt **elsődleges** fordítása — eddig nem volt hozzá strukturált, gépileg kereshető adat, csak az SzPA (másodlagos, összehasonlító forrás) rendelkezett ilyennel.

**A "más Károli-verzió" kérdés:** ez az **1908-as revideált** kiadás (nem az eredeti 1590-es Vizsolyi Biblia) — a leggyakoribb, online is elterjedt "Károli"-szöveg. Ha a projekt korábbi tanulmányai egy eltérő kiadást idéztek, ez visszamenőleg ellenőrizendő (nyitott pont, lásd 8. szakasz).

**2. réteg — Az összekapcsolt (join) tábla** — ez a tényleges, generált végeredmény, ami *minden* STEPBible-sorhoz (tehát minden szóhoz, nem csak a lábjegyzeteshez) hozzárendel egy sort. **Mostantól háromoszlopos a magyar oldal** (Károli bevonásával, nem csak SzPA):
```
[könyv]_osszekapcsolt.tsv:
Igehely | Szósorszám | Strong | Eredeti szó | Kiejtés | Szótári jelentés | Angol tükörfordítás | Kritikai kiadás |
Károli megfelelés | Károli azonosítás módja | SzPA megfelelés | SzPA azonosítás módja | SzPA lábjegyzet-szöveg
```
**Fontos különbség a két magyar oszlop között:** a Károli-oszlopnál **nincs lábjegyzet-forrás** (a Károli maga nem tartalmaz fordítói jegyzeteket) — tehát a Károli-oszlopnál a hármas állapotból (lásd 4.2) csak kettő fordulhat elő: *tartalom-alapú azonosítás* vagy *nincs önálló megfelelés*, sosem *lábjegyzet-alapú*. Az SzPA-oszlopnál mindhárom állapot érvényes, változatlanul.

**Miért éri meg mindkét magyar fordítást egy sorban tartani:** ez teszi lehetővé, hogy egy jövőbeli tanulmány **közvetlenül összevesse**, hol egyezik és hol tér el a Károli és az SzPA fordítói döntése ugyanahhoz az eredeti szóhoz — ez pontosan az a fajta összevetés, amit korábban (a "Károli-hűség" és a szövegkritikai ⚠️ pontok kapcsán) csak esetenként, kézzel végeztünk.

**3. réteg — Fájlszervezés a privát repóban:**
```
Bible-Study-privat/
├── szpa/
│   ├── peldabeszedek_versek.tsv
│   ├── peldabeszedek_labjegyzetek.tsv
│   ├── apcsel_versek.tsv
│   └── apcsel_labjegyzetek.tsv
```
Bible-Study/  (publikus repó-rész)
├── konkordancia/
│   ├── TAGNT_kivonat.tsv
│   ├── TAHOT_kivonat.tsv
│   └── README.md
├── karoli/
│   ├── Karoli_1908.tsv              ← scrollmapper/bible_databases-ből, közkincs
│   └── README.md (forrás, licenc: MIT [repó] / Public Domain [szöveg], generálás dátuma)

Bible-Study-privat/  (privát repó-rész)
├── szpa/
│   ├── peldabeszedek_versek.tsv
│   ├── peldabeszedek_labjegyzetek.tsv
│   ├── apcsel_versek.tsv
│   └── apcsel_labjegyzetek.tsv
├── osszekapcsolt/
│   ├── peldabeszedek_osszekapcsolt.tsv   ← generált, a 2. réteg (Károli + SzPA együtt)
│   ├── apcsel_osszekapcsolt.tsv
│   └── README.md (mikor generálva, milyen STEPBible-verzióból, generálási módszer)
```

**Miért marad a join-tábla mégis privát a Károli bevonása után is:** bár a Károli-oszlop önmagában közkincs, a **teljes sor** (Károli + SzPA együtt egy táblában) a védett SzPA-adatot is tartalmazza — ezért a teljes összekapcsolt tábla továbbra is a privát repóba kerül. *(Elméletileg készíthető lenne egy külön, csak Károli+STEPBible join, ami tisztán publikus lehetne — ez egy jövőbeli, opcionális bővítés, ha valaha SzPA nélküli, csak Károli-alapú konkordanciára is szükség lenne.)*

**Tárolási hely elve:** mivel az összekapcsolt (join) tábla tartalmazza a védett SzPA-szöveget is, **a teljes join-tábla a privát repóba kerül**, még akkor is, ha az egyik forrás-oldal (STEPBible, most már a Károli is) önmagában nyilvános maradhat.

### 4.2 Az "Azonosítás módja" oszlop — hármas állapot (felváltja a korábbi kétállapotú leírást)

A Péld 1:1-4 és ApCsel 1:1-4 minták alapján kiderült, hogy a "van SzPA-lábjegyzet / nincs" kétállapotú megkülönböztetés **pontatlan** volt — a "nincs lábjegyzet" eset valójában **két, egymástól jól elkülönülő alesetre** bomlik:

| Állapot | Jelentése | Példa |
|---|---|---|
| **lábjegyzet-alapú** | SzPA-fordító saját magyarázata köti hozzá — legmagasabb megbízhatóság | Péld 1:2 "bölcsesség" ↔ חָכְמָה |
| **tartalom-alapú azonosítás** | angol gloss segítségével beazonosítva (jelentés szerint, nem pozíció szerint), de nincs SzPA-kommentár hozzá | Péld 1:1 "Salamonnak" ↔ שְׁלֹמֹה |
| **nincs önálló megfelelés** | funkciószó (névelő, nyomatékosító partikula), aminek nincs önálló magyar szava a fordításban | ApCsel 1:1 τὸν (névelő), μέν (nyomatékosító) |

**Miért fontos a megkülönböztetés:** az első két állapot esetében **van** azonosítható magyar szó a join-táblában (csak eltérő megbízhatósággal), a harmadik esetben viszont **nincs is mit azonosítani** — ezt korábban tévesen ugyanabba a "üres mező" kategóriába soroltuk, mint a lábjegyzet-hiányt, pedig ez két, tartalmilag eltérő helyzet.

**A módszer, ami a tartalom-alapú azonosítást lehetővé teszi:** a 8-oszlopos STEPBible-kivonat 7. oszlopa (kontextuális angol tükörfordítás) horgonyként szolgál ahhoz, hogy — akár kézzel, akár nyelvi modell segítségével — a magyar mondatban **jelentés szerint**, pozíciótól függetlenül megtalálható legyen a megfelelő szó. **Ez nem old fel egy tartalmi hiányt** (a fordítói *magyarázat* hiánya továbbra is explicit jelzve marad) — csak azt teszi lehetővé, hogy a magyar szó *azonosítása* (nem a *magyarázata*) megbízható legyen.

*(Elvetett alternatíva a szó-azonosításra: horgonypont-alapú, pozíció-szerinti interpoláció — kísérlettel igazoltan megbízhatatlan héber szövegnél, mert a héber és a magyar szórend rendszeresen eltér, különösen birtokos szerkezeteknél és célhatározói igéknél [lásd Péld 1:1-4 kísérlet]. Görög szövegnél [ApCsel 1:1-4] a szórend-eltérés kisebb, de az egységesség kedvéért a tartalom-alapú módszer mindkét testamentumnál alkalmazandó.)*

### 4.3 További megfigyelések az ApCsel-mintából

**A) A kritikai kiadás-oszlop "nincs eltérés" eredménye is informatív.** Az ApCsel 1:1-4 mind a 19 vizsgált szavánál minden kiadás (NA28-tól Byz-ig) egyezett — nincs szövegkritikai ⚠️ pont ebben a szakaszban. Ez nem "üres" vagy haszontalan eredmény: megerősíti, hogy a Károli/SzPA és a modern kritikai szövegek **teljesen egyeznek** ezen a szakaszon, ami egy jövőbeli tanulmány szövegkritikai ellenőrzési lépésének (lásd a sablon-módosítások között) pozitív, dokumentálandó eredménye.

**B) Egy SzPA-lábjegyzet néha több görög/héber szóra is vonatkozik.** Az ApCsel 1:2-nél a 3. lábjegyzet ("utasításokat adott az apostoloknak") egyszerre két STEPBible-sorhoz kapcsolódik (`ἐντειλάμενος` + `ἀποστόλοις`). A join-tábla generálásakor ezt jelölni kell (pl. mindkét sor "lábjegyzet-alapú" állapotot kap, azonos lábjegyzet-szöveggel, vagy egy "lásd Lj.X" kereszthivatkozással) — a kapcsolat **nem mindig szigorúan 1:1** arányú.

### 4.4 A generálás korlátja

A **lábjegyzet-alapú sorok** gépiesen, megbízhatóan generálhatók (az SzPA lábjegyzet-tábla és a STEPBible Strong-száma egyértelműen összeköthető). A **tartalom-alapú azonosítás** viszont — ahogy mindkét mintánál is történt — **nem tisztán szkriptelhető**, mert szemantikai felismerést igényel; egy teljes könyv generálásakor ez a réteg **kézi átnézést vagy egy nyelvi modell soronkénti közreműködését** igényli, nem egy egyszeri, automatikus script-futtatást.

### 4.5 Miért éri meg mindezt megépíteni

Ez a join gyakorlatilag **egy egyedi, magyar nyelvű, Strong-számmal ellátott konkordanciát** hoz létre — mostantól nemcsak az SzPA-hoz, hanem a **Károlihoz is**. Ilyen, tudomásunk szerint, jelenleg nyilvánosan nem létezik egyetlen magyar bibliafordításhoz sem. Ez túlmutat egy kényelmi eszközön — önálló, projekt-specifikus erőforrás.

### 4.6 Egyéb, a scrollmapper/bible_databases keresésekor azonosított elemek

**Kereszthivatkozás-adatbázis (openbible.info alapú, szavazat-súlyozott)** — a `cross_references` tábla a repóban minden vershez ad lehetséges kereszthivatkozás-jelölteket, relevancia-szavazatszámmal. **Hasznos segédeszköz** a 3/b pont kereszthivatkozás-kereséséhez: nem helyettesíti a tartalmi mérlegelést, de **kiindulási jelöltlistát** ad, amit utána a szokásos módon (lexikai vs. tematikus elhatárolás, STEPBible-ellenőrzés) kell kiértékelni.

**Károli-specifikus kereszthivatkozás-adat (`krisek/HunKar`, GitHub) — új, valószínűleg jobb elsődleges forrás ugyanerre a célra.** Ez egy önálló SWORD-modul repó (Károli 1908, OSIS XML formátum, forrása a `szentiras.hu/KG`), ami **Strong-számot nem tartalmaz**, de **beépített, versenkénti kereszthivatkozásokat** ad, közvetlenül a magyar Károli-hagyományból:
```xml
<verse osisID="Gen.1.1">Kezdetben teremté Isten az eget és a földet.
  <reference osisRef="Gen.2.4-Gen.2.5">1Móz 2,4-5</reference>
  <reference osisRef="Ps.33.6">Zsolt 33,6</reference>
  <reference osisRef="Acts.14.15">Csel 14,15</reference>
  ...
</verse>
```
**Miért lehet jobb, mint a scrollmapper/openbible.info-adat:** ez **magyar, Károli-specifikus, valószínűleg teológiai szerkesztők által összeállított** hivatkozásrendszer (a `szentiras.hu` mögötti szerkesztőségtől), nem angol nyelvű, crowdsourced szavazat-alapú lista. Közvetlenül a projekt elsődleges forrásához (Károli) kötődik, nem egy másik nyelvű köztes fordításhoz.

**A két kereszthivatkozás-forrás egymáshoz való viszonya — nyitva hagyva, nem eldöntve:** mindkettő **kiindulási jelöltlistaként** szolgálhat a 3/b ponthoz, nem helyettesítik a tartalmi mérlegelést. Lehetséges, hogy a kettő **kiegészíti** egymást (a Károli-specifikus szűkebb, de megbízhatóbb; az openbible.info szélesebb, de vegyesebb minőségű) — ez a kérdés egy jövőbeli, tényleges összevetéssel dönthető el, nem itt, elméletben.

**Strong-taggelt Károli — a mélykutatás megtalálta, de zárt licenc alatt.** A `krisek/HunKar` és a scrollmapper-es Károli-forrás mellett végzett mélyebb kutatás **egyetlen, ténylegesen létező, teljes** Strong-tagelt Károlit azonosított: a **Biblia-Felfedező (Bible-Discovery)** program "Károli Gáspár Biblia – Strong számokkal (HUN)" modulja (Zsidó Miklós fejlesztése, mobilbiblia.hu / bible-discovery.com). Ez **valódi, szó szintű** párosítás (nem csak névleges, mint a scrollmapper KJV esetében), a teljes Bibliára (ÓSZ+ÚSZ) elkészült. **Licenc:** zárt — "A Strong párosítás Zsidó Miklós tulajdona. Minden jog fenntartva… Tilos a Művet… forgalmazni… módosítani… szétbontani illetve visszafejteni." A programon kívüli adatkiemeléshez egyedi engedélykérés szükséges (info@mobilbiblia.hu). Egy Bible-software fórumbeszélgetés (biblesupport.com) megerősíti, hogy a Strong-számok kézi hozzáadása egy fordításhoz **általánosan nehéz, homográf-problémákkal terhelt feladat** — ez a Biblia-Felfedező munkájának valódi szakmai értékét is alátámasztja.

**A döntés (lásd 4.7): a Biblia-Felfedező nem lesz elsődleges adatforrás**, mert a zárt licenc pontosan ugyanabba az akadálytípusba ütközik, mint korábban az ESV/Crossway és az Accordance-eset — használható eszköz, de nem exportálható adat.

**KJV/KJVA/RLT "Strong-taggelt" verziói (scrollmapper) — megvizsgálva, jelenleg NEM használható.** A fordítás neve ("with Strongs Numbers and Morphology") a SWORD-modul eredeti elnevezéséből öröklődött, de a scrollmapper könnyen elérhető JSON-konverziója **ténylegesen nem tartalmazza** a Strong-tageket (ellenőrizve: `{"verse": 1, "text": "In the beginning God created..."}`, tag nélkül). A nyers forrás (`sources/en/KJV/`) elvben tartalmazhatja, de **külön feldolgozást** igényelne, és a forrás licence ott **GPL** (nem egyszerű közkincs) — ez nem oldja meg a korábban azonosított "természetes szórendű, Strong-taggelt angol szöveg" hiányt.

**AndBible fejlesztői terv (2026 Q2/Q3, figyelendő, nem kész eszköz).** Az AndBible nyílt forráskódú Biblia-app dokumentált fejlesztési terve szerint egy **AI-alapú Strong-taggelési pipeline-t** építenek, ami egy referencia-Bibliából (KJV/WEB, közkincs) automatikusan hozzárendel Strong-számokat **bármely más fordításhoz** — koncepcionálisan ez pontosan a projekt saját, kézzel végzett "tartalom-alapú azonosítási" módszerét automatizálná. Nem publikált eszköz, csak fejlesztői útiterv — érdemes később visszatérni rá.

### 4.7 Végleges döntés: a Károli-dataset forrása

**A Károli-dataset elsődleges forrása: a közkincs HunKar-szöveg (scrollmapper), Strong-párosítással a projekt már meglévő, tanulmányvezérelt, tartalom-alapú generálási módszerével** (lásd 4.2, 7.1, 7.2) — **nem** a Biblia-Felfedező.

**Indoklás:**
1. **Azonnal elindítható**, nincs engedélykérésre várás (szemben a Biblia-Felfedezővel, ahol egyedi, elbírálás-függő engedély kellene)
2. **Nulla plusz jogi kockázat** — a HunKar bázisszöveg közkincs
3. **A meglévő infrastruktúrába illeszkedik** — a join-tábla, a kumulatív generálás, a kritériumlista mind eleve erre lett kidolgozva
4. **Konzisztens a Károli sajátosságával:** mivel a Károli-szövegnek nincs lábjegyzet-forrása (szemben az SzPA-val), a Károli-oszlop a hármas állapotból (4.2) mindig csak a *tartalom-alapú azonosítás* vagy a *nincs önálló megfelelés* állapotot veheti fel, sosem a *lábjegyzet-alapút* — ez nem hiányosság, hanem a forrás jellegéből következő, várt korlát

**A Biblia-Felfedező szerepe emiatt referencia-eszközzé alakul, nem adatforrássá:** ha egy saját, tartalom-alapú Károli-Strong párosításnál bizonytalanság merül fel, a Biblia-Felfedező programban (ha hozzáférhető) **kézzel visszaellenőrizhető**, hogy a saját azonosítás egyezik-e a professzionális párosítással — anélkül, hogy azok adatát kiemelnénk vagy másolnánk.

**Utólagos felismerés (4.11-es validáció során): a "Károli" név alatt legalább KÉT, szövegszerűen eltérő revízió létezik, más-más jogi státusszal.** A validáció (lásd 4.11) során kiderült, hogy a felhasználó által megadott külső referencia a jelenlegi 1908-as HunKar-szövegnél **modernebb** alakokat használt egyes verseknél (1Móz 1:2: "volt"/"sötétség"/"lebegett" a HunKar "vala"/"setétség"/"lebeg vala" helyett) — ez egy **másik, "Revideált Károli" néven ismert, 2011-es kiadás (Veritas Kiadó)**, ami **© védett, nem közkincs** (szemben a jelenleg használt 1908-as HunKar-ral). A Biblia-Felfedező program feltehetően ezt a 2011-es revíziót futtatja, nem az 1908-ast — ez magyarázza a referencia eltérő alakjait. **A projekt publikus Károli-datasete (`Karoli_1908.tsv`) emiatt is az 1908-as HunKar-on marad** — a Veritas 2011-es revízió licenc-kockázata miatt nem cserélhető rá jogosultság nélkül. Részletek és nyitott döntés: lásd 8. szakasz.

### 4.8 KJV-hidas módszer — validált, ellenőrzött forrással megerősítve

**A módszer:** a tartalom-alapú azonosításnál (4.2) a nyers STEPBible angol tükörfordítás helyett/mellett a **KJV természetes szórendű, teljes mondatszerkezete** szolgál hídként a héber/görög Strong-szám és a Károli/SzPA-szó között. Ez azért segít, mert a KJV **grammatikai szerkezete** (alany-állítmány-tárgy) explicit jelzést ad ott, ahol a nyers szó-glosszok csak egyenrangú jelentés-listát adnak.

**Demó-eredmény (Péld 23:1-4, vak teszt):** a csak STEPBible-glosszra épülő módszer 9/10 (90%) pontosságot ért el; a KJV-hidas módszer **10/10 (100%)** — a kritikus eset (23:2, "mértékletlen" — H1167 "master of" vs. H5315 "appetite") a KJV *"if thou be **a man given to** appetite"* mondatszerkezete alapján oldódott meg helyesen, mert az egyértelműsítette, melyik héber szó az állítmány.

**Forrás — megtalálva és validálva** *(korábbi "még beszerzendő" jelölés lezárva)*: **valódi, ténylegesen beágyazott** Strong-taggelt KJV-szöveg, **öt egymástól független oldalon** megerősítve (nem egyetlen, bizonytalan forrás):
- **`studybible.info/KJV_Strongs/[Könyv]`** — **elsődleges, ajánlott forrás**: könyv-szintű navigációval (mind a 31 fejezet egy oldalon), morfológiai kóddal kiegészítve — ezzel a formátummal készült el ténylegesen a teljes Példabeszédek-dataset (lásd 0. szakasz, 5-6. sor)
- `biblehub.com/kjvs/` (pl. `biblehub.com/kjvs/proverbs/23.htm`) — másodlagos, ugyanúgy validált
- `godrules.net/library/kjvstrongs/`
- `sacrednamebible.com/kjvstrongs/`
- `bibletruthpublishers.com`

**Eredet:** héber Strong-számok — Bible Foundation (bf.org); görög Strong-számok (ÚSZ) — CrossWire KJV2003 projekt. **Licenc:** az Egyesült Királyságban a KJV szövege "Crown copyright" alatt áll, de ez **csak a kereskedelmi nyomtatásra** vonatkozik ott — a világ többi részén, és nem-kereskedelmi/kutatási célra szabadon használható.

**Független megerősítés a saját adat hitelességére:** a fenti forrásokból lekért Strong-számok **számjegyre pontosan egyeztek** a felhasználó saját, korábban bemutatott Károli-Strong adatával (pl. Péld 23:7: számítgatja=8176/8804, magában=5315, egyél=398/8798, igyál=8354/8798, mondja=559/8799, akarattal=3820 — mind egyezik) — ez megerősíti, hogy a felhasználó saját adata **ugyanerre a szabványos, közkincs KJV-Strong konvencióra** épül.

**SzPA-specifikus szabály — kettős következtetés: alapértelmezett javítás, DE explicit kivétel-lista**

**1. Alapszabály:** a KJV-híd **alapértelmezetten bevezetendő** az SzPA tartalom-alapú azonosításánál is — a legtöbb, teológiailag semleges szónál (ahogy a Károli-demó mutatta) ugyanúgy javítja a pontosságot, mert a KJV természetes mondatszerkezete ugyanazt a grammatikai egyértelműsítést adja, függetlenül attól, melyik magyar fordítást (Károli vagy SzPA) kötjük hozzá.

**2. Kivétel-lista — azok a fogalmak, ahol az SzPA tudatosan, dokumentáltan eltér a hagyományos angol (KJV-szerű) fordítási konvenciótól.** Ezeknél a KJV-hidas eredményt **fokozott gyanakvással**, nem automatikusan kell elfogadni, mert éppen itt állhat a KJV a legtávolabb az SzPA szándékos választásától:

| Fogalom | Hagyományos angol (KJV) | SzPA tudatos választása | Miért kockázatos a KJV-híd itt |
|---|---|---|---|
| βαπτίζω (baptizó) | "baptize" | **"alámerít"** | a KJV át nem fordított, transzliterált szava ("baptize") semmilyen tartalmi/grammatikai támpontot nem ad a magyar "alámerít" igéhez |
| πνεῦμα ἅγιον (pneuma hagion) | "Holy Ghost/Spirit" | **"Szent Szellem"** | a "Ghost" szó a mai angolban már nem hordozza a "szellem" jelentésmezőt, félrevezető párhuzamot adhat |
| ἔθνη (ethné) | "Gentiles" | **"nemzetek"** | a "Gentiles" kulturálisan szűkebb (zsidó szempontból "nem-zsidók"), míg a "nemzetek" tágabb, semlegesebb — a KJV itt egy értelmezési döntést is magával hozna |

**3. A kivétel-lista bővítendő, tanulmányvezérelt alapon:** ez a három tétel a beszélgetésben eddig felmerült, dokumentált esetekre épül — **nem kimerítő lista**. Minden jövőbeli tanulmánynál, ahol az SzPA lábjegyzete kifejezetten jelez egy tudatos, hagyománytól eltérő fordítói döntést (ahogy a projekt korábbi terminológiai szabályai is rögzítik, pl. "Szent Szellem" nem "Szentlélek", "spirituális" nem "misztikus"), az adott szó **automatikusan felkerül** erre a listára, mielőtt a KJV-hidas azonosítást rá alkalmaznánk.

**4. Gyakorlati szabály a join-táblában:** minden SzPA-oszlopos sor, ami a kivétel-listán szereplő Strong-számhoz kapcsolódik, kap egy **"⚠️ KJV-híd óvatossággal kezelendő"** jelölést — ez nem zárja ki a KJV-híd használatát, csak jelzi, hogy az eredményt **kézzel is ellenőrizni kell**, mielőtt a "tartalom-alapú azonosítás" állapotot magas bizonyossággal rögzítjük.

### 4.9 Második validáló forrás: ASV (American Standard Version, 1901) — kereszt-ellenőrzés

**A forrás:** ASV, 1901, közkincs alapszöveg; a Strong-taggelés a "Cross Word Project" (Wade Maxfield) munkája — **független** a KJV-Strongs taggelésétől (Bible Foundation/CrossWire), tehát valódi, nem csak formális második forrás. **Elsődleges, ajánlott elérés:** `studybible.info/ASV_Strongs/[Könyv]` — könyv-szintű belépési pont, mind a 31 fejezet linkjével egy oldalon, ugyanazzal a szerkezettel, mint a KJV-nél. *(Fontos: a `biblehub.com/asv/` **nem** Strong-taggelt — csak sima szöveg; a biblehub.com-on nincs külön "ASV+Strong's" útvonal, ellentétben a KJV-vel.)*

**A módszer bővítése:** a join-tábla "Azonosítás módja" oszlopa (4.2) egy negyedik, finomított állapottal egészül ki, amikor KJV-híd alkalmazva van:

| Alállapot | Jelentés | Megbízhatóság |
|---|---|---|
| KJV + ASV egyezik | két független forrás ugyanoda mutat | legmagasabb |
| csak KJV vagy csak ASV elérhető | egy forrás, nincs kereszt-ellenőrzés | közepes |
| **KJV ≠ ASV eltérés** | a két forrás eltérő angol megfogalmazást ad | **explicit ⚠️ jelzés — kézi ellenőrzés kötelező** |

**Demonstrált eset — Péld 23:1, valódi, a mintában ténylegesen előforduló eltérés:**

| Forrás | Megfogalmazás | H0834 ("that which") értelmezése |
|---|---|---|
| KJV | *"consider diligently **what** is before thee"* | tárgyra utal (étel) |
| ASV | *"consider diligently **him** that is before thee"* | személyre utal (uralkodó) |
| Károli | *"...**ki** van előtted"* | **személyre utaló** vonatkozó névmás |

**A Károli "ki" szava egyértelműen az ASV értelmezésével egyezik, nem a KJV-vel.** Ha csak a KJV szolgált volna hídként, ez tévesen sugallhatta volna, hogy a "ki" valamiért mégis egy tárgyra utaló szerkezetet fordít. Az ASV bevonása **azonnal jelezte** az eltérést, és a helyesebb irányba terelt — ez **konkrét, mérhető bizonyíték** a kereszt-ellenőrzés gyakorlati értékére, nem csak elméleti előny. *(A 23:2-4 verseknél az ASV szó szerint megegyezett a KJV-vel — ott a második forrás csak megerősítést adott, nem új információt, ami várható, hiszen az ASV a KJV/ERV hagyomány folytatása.)*

**A teljes lánc, az eredeti szöveg Strong-adatáig visszavezetve — ez magyarázza meg, honnan ered az eltérés:**

| Réteg | Adat |
|---|---|
| Héber szó (Strong) | אֲשֶׁר (H0834A) |
| Kiejtés | *ásér* |
| STEPBible gloss | *"[that] which"* |
| KJV | *"what"* |
| ASV | *"him"* |
| Károli | *"ki"* |

**Kulcsfelismerés:** a héber *ásér* egy **eredendően semleges vonatkozó névmás**, ami egyaránt vonatkozhat személyre és tárgyra (kb. "aki/ami") — a **STEPBible nyers gloss is ezt a semlegességet tükrözi**, nem dönt személy/tárgy között. A KJV és az ASV fordítói **egymástól függetlenül, külön-külön döntöttek** ebben a kérdésben — a kétértelműség tehát **nem fordítási hiba**, hanem **magának az eredeti héber szövegnek a tulajdonsága**.

**Módszertani tanulság — pontosítja a KJV≠ASV jelzés értelmezését:** egy ilyen ⚠️ jelzésnél a kézi ellenőrzésnek **nem mindig az a kérdése, "melyik forrás téved"** — gyakran azt kell megállapítani, hogy **maga az eredeti szöveg enged-e több értelmezést**. Ez utóbbi eset **önmagában is értékes exegetikai megfigyelés**, ami akár egy jövőbeli tanulmány ⚠️ vitatott pontjának alapja is lehet (a saját kritérium 5. pontja szerint: "a szó jelentése önmagában ad okot egy vitatott pontra") — nem csupán technikai zajként kezelendő.

### 4.10 getbible.net API — megvizsgálva, lezárva, nem használjuk

**A kísérlet célja:** kideríteni, van-e egyetlen letöltéssel elérhető, teljes KJV/ASV Strong-taggelt bulk-forrás (a fejezetenkénti scraping helyett), a `getbible.net` API-n keresztül.

**Eredmény:** a `getbible.net` (minden aldomainjével, így `api.getbible.net`-tel együtt) **szervezeti szintű hálózati tiltás alatt áll** a claude.ai munkakörnyezetben — Claude Code-ban végzett teszt sem tudta közvetlenül lekérdezni, a proxy explicit policy denial (403) választ adott.

**Közvetett bizonyíték, GitHub-forrásokból (nem a tiltott API-ból):**
- Az ASV fordítás kulcsa ebben az API-ban ténylegesen `asv` (megerősítve a `getbible/v2` repó gyökérszerkezetéből)
- A `getbible/v2` repóban a `kjv/` mappák **csak metaadatot/SHA-ellenőrzőösszeget** tartalmaznak, a tényleges verstartalmat élőben szolgálja ki a szerver — statikus bulk-fájl **nincs** a repóban magában
- A `getbible/getbiblesword` (az adatfeldolgozó motor) README-je explicit megkülönbözteti a *"rendered text"* (megjelenítésre szánt, feltehetően tag-mentes) és a *"decoded base64 bytes as authoritative"* (nyers, hiteles forrás) fogalmakat — ez arra utal, hogy a publikus JSON `"text"` mezője valószínűleg **tag-mentes**, a Strong-adat csak a mögöttes SWORD-modulban van jelen

**Elsőkézből való megerősítés:** a felhasználó saját gépéről közvetlenül tesztelte a `getbible.net` API-t (a hálózati tiltás miatt itt nem volt lehetséges) — **megerősítve: nincs Strong-szám** a kimenetben. Ez a közvetett GitHub-bizonyítékot véglegesen igazolja.

**Mintázat-felismerés:** ez már **második, egymástól független, ténylegesen ellenőrzött eset** (az első a scrollmapper-KJV volt), ahol egy kényelmes, felhasználóbarát API/JSON-forrás **ígéri** a Strong-taggelést a nevében/metaadatában, de a **tényleges kimenet nem tartalmazza** — a mögöttes, valódi taggelt adat mindkét esetben egy SWORD-modulban van, amit a kényelmi réteg "letisztít" emberi olvasásra. **Ez általános óvatossági elvvé emelhető**: bármely jövőbeli, hasonlóan kényelmes API/JSON-forrást eleve gyanakvással kell kezelni, amíg tételesen nem ellenőrizzük a tényleges kimenetet, a névre/metaadatra hagyatkozás helyett.

**Végleges döntés: nem keresünk tovább bulk API-alternatívát.** A validált, ténylegesen ellenőrzött módszer (`studybible.info/[KJV_Strongs|ASV_Strongs]/[Könyv]`, könyv-szintű navigációval, fejezetenkénti lekérdezéssel) marad az egyetlen működő út — ezzel a módszerrel készült el ténylegesen a teljes Példabeszédek KJV+ASV dataset (lásd 0. szakasz).

### 4.11 Károli-Strong tartalom-alapú párosítás — validálva külső referenciával

**A validáció célja:** a projekt saját, STEPBible-alapú tartalom-alapú Károli-Strong azonosítási módszere (lásd 4.2) eddig kizárólag **belső** ellenőrzéssel (a saját logika önmagával való konzisztenciájával) volt alátámasztva. A felhasználó egy külső, feltehetően Biblia-Felfedezőből vagy hasonló professzionális forrásból származó, Strong-taggelt Károli-referenciát adott meg 1Móz 1:2-4-re, ami **első alkalommal** tette lehetővé egy **független** forrással való összevetést.

**Eredmény: 1Móz 1:3-4-en 13/14 szó pontosan egyezett** — beleértve két, elsőre bonyolultnak tűnő esetet is, amik a módszer megbízhatóságát különösen jól próbára tették:

- **"látá"** — a referencia egyetlen Károli szóra **kettős taggelést** ad: H0853 (tárgyeset-jelölő) + H7200 (látott). Ez pontosan megfelel a `TAHOT_kivonat.tsv` két külön sorának ugyanahhoz a héber szóhoz (H0853 + H7200G) — a projekt saját, morfémánkénti szétbontási logikája (lásd a TAHOT-kivonat módszertana, `konkordancia/TAHOT_TAGNT_README.md`) itt függetlenül igazolódott.
- **"elválasztá" / "a sötétségtől"** — a héber kettős "között...között" szerkezet (H0996 kétszer) helyesen oszlik meg a két Károli kifejezés között, nem csúszik el egy pozícióval — ez pontosan az a fajta eset, ahol a 4.2-ben elvetett, pozíció-alapú interpoláció korábban megbukott, és amit a tartalom-alapú módszer volt hivatva megoldani.

**Az egyetlen eltérés — dokumentálandó, nem hiba:** a "jó" szónál a referencia H2896-ot ad, a `TAHOT_kivonat.tsv` H2895-öt. Ez a טוֹב (tov) gyök **két szomszédos Strong-száma** (H2895 igei alak, "jónak lenni"; H2896 melléknévi alak, "jó") — nyelvtanilag mindkét elemzés védhető erre a mondatra ("hogy jó a világosság"), a kétértelműség **magának a szónak a tulajdonsága** (hasonlóan a 4.9-es ásér/H0834-es esethez), nem fordítási vagy módszertani hiba.

**Jelentősége:** ez az első alkalom, hogy a projekt saját, belső STEPBible-alapú Károli-Strong módszertanát **külső, független forrással** vetettük össze. A 13/14 (93%) egyezés — beleértve a bonyolultabb, kettős-taggelésű eseteket is — megerősíti, hogy a 4.7-es pontban rögzített döntés (saját, tartalom-alapú módszer a közkincs HunKar-ra építve, nem a Biblia-Felfedező) **technikailag életképes és megbízható eredményt ad**, nem csupán jogilag a legtisztább út.

**Mellékfelismerés:** a validáció során derült ki, hogy a felhasznált külső referencia egy **másik, szövegszerűen eltérő Károli-revízióból** származhat, más jogi státusszal — lásd 4.7 és 8. szakasz.

### 4.12 Join-tábla lefedettség — gyors áttekintés

Ez a táblázat minden alkalommal frissítendő, amikor egy tanulmány új sorokat ad a `konkordancia/Karoli_Strong_kivonat.tsv`-hez (lásd `Join_tabla_folyamat_magyarazat.md`). A "Feldolgozott versek száma" a benne szereplő **egyedi** igehelyek száma (nem a szósorok száma), az "Összes vers a könyvben" a `Konyv_normalizalo_tabla.tsv` és a `Karoli_1908.tsv` alapján számolható.

**Jelenlegi állapot (2026.08.24):** a `Karoli_Strong_kivonat.tsv` most jött létre, üres fejléc-fájlként — a korábbi kézi kísérletek (1Móz 1:2-4) ebben a chat-munkamenetben készültek, nem a repóban, ezért egyelőre nem számítanak bele. A táblázat minden könyvnél 0-val indul.

| Könyv | Feldolgozott versek száma | Összes vers a könyvben | Lefedettség |
|---|---|---|---|
| 1Móz | 0 | 1533 | 0% |
| 2Móz | 0 | 1213 | 0% |
| 3Móz | 0 | 859 | 0% |
| 4Móz | 0 | 1288 | 0% |
| 5Móz | 0 | 959 | 0% |
| Józs | 0 | 658 | 0% |
| Bír | 0 | 618 | 0% |
| Ruth | 0 | 85 | 0% |
| 1Sám | 0 | 811 | 0% |
| 2Sám | 0 | 695 | 0% |
| 1Kir | 0 | 817 | 0% |
| 2Kir | 0 | 719 | 0% |
| 1Krón | 0 | 942 | 0% |
| 2Krón | 0 | 822 | 0% |
| Ezsd | 0 | 280 | 0% |
| Neh | 0 | 406 | 0% |
| Eszt | 0 | 167 | 0% |
| Jób | 0 | 1070 | 0% |
| Zsolt | 0 | 2527 | 0% |
| Péld | 0 | 915 | 0% |
| Préd | 0 | 222 | 0% |
| Én | 0 | 117 | 0% |
| Ézs | 0 | 1292 | 0% |
| Jer | 0 | 1364 | 0% |
| Sir | 0 | 154 | 0% |
| Ez | 0 | 1273 | 0% |
| Dán | 0 | 357 | 0% |
| Hós | 0 | 197 | 0% |
| Jóel | 0 | 73 | 0% |
| Ámós | 0 | 146 | 0% |
| Abd | 0 | 21 | 0% |
| Jón | 0 | 48 | 0% |
| Mik | 0 | 105 | 0% |
| Náh | 0 | 47 | 0% |
| Hab | 0 | 56 | 0% |
| Sof | 0 | 53 | 0% |
| Hag | 0 | 38 | 0% |
| Zak | 0 | 211 | 0% |
| Mal | 0 | 55 | 0% |
| Mt | 0 | 1071 | 0% |
| Mk | 0 | 680 | 0% |
| Luk | 0 | 1151 | 0% |
| Ján | 0 | 879 | 0% |
| ApCsel | 0 | 1007 | 0% |
| Róm | 0 | 431 | 0% |
| 1Kor | 0 | 436 | 0% |
| 2Kor | 0 | 256 | 0% |
| Gal | 0 | 149 | 0% |
| Ef | 0 | 155 | 0% |
| Fil | 0 | 104 | 0% |
| Kol | 0 | 95 | 0% |
| 1Thessz | 0 | 89 | 0% |
| 2Thessz | 0 | 47 | 0% |
| 1Tim | 0 | 113 | 0% |
| 2Tim | 0 | 83 | 0% |
| Tit | 0 | 46 | 0% |
| Filem | 0 | 25 | 0% |
| Zsid | 0 | 303 | 0% |
| Jak | 0 | 108 | 0% |
| 1Pét | 0 | 105 | 0% |
| 2Pét | 0 | 61 | 0% |
| 1Ján | 0 | 105 | 0% |
| 2Ján | 0 | 13 | 0% |
| 3Ján | 0 | 15 | 0% |
| Júd | 0 | 25 | 0% |
| Jel | 0 | 405 | 0% |

### 4.13 Önellenőrzési mechanizmus — kereszt-ellenőrzés és megbízhatósági jelölés

**Miért a KJV/ASV a kereszt-ellenőrző forrás, nem közvetlenül a STEPBible:** a Károli-Strong sor ELEVE a STEPBible (TAHOT/TAGNT) Strong-számából és angol glosszából születik, tartalom-alapú azonosítással (lásd 4.2 pont). A STEPBible tehát az ELSŐDLEGES BEMENET ehhez a lépéshez, nem egy második, független forrás — önmagával nem lehet kereszt-ellenőrizni, mert az körkörös lenne (saját magunk munkáját saját magunkkal igazolnánk vissza, új információ nélkül). A KJV és az ASV ezzel szemben VALÓDI, FÜGGETLEN források — nem a STEPBible-ből származnak, külön projektek, külön fordítói döntésekkel (Bible Foundation/CrossWire, illetve a Cross Word Project, lásd 4.8-4.9 pont). Amikor egy Károli-szóhoz generált Strong-számot összevetjük azzal, amit a KJV/ASV ugyanahhoz a Strong-számhoz, ugyanahhoz a vershez rendel, ez valódi, független megerősítés — pontosan úgy, ahogy a Pro.23.1 "ki"/"him"/"what" esetnél is működött (4.9 pont).

Minden új Károli-Strong sor generálásakor, MIELŐTT a `Karoli_Strong_kivonat.tsv`-be kerülne:

1. Ellenőrizd, van-e `KJV_Strongs_[Könyv].tsv` vagy `ASV_Strongs_[Könyv].tsv` adat ugyanarra az igehelyre és Strong-számra.
2. HA VAN és egyezik → "magas" megbízhatóság.
3. HA VAN, de ELTÉR → ÁLLJ MEG, ne generáld automatikusan — ez explicit kézi vizsgálatot igényel (lásd a Gen.1.1 "what"/"him" KJV≠ASV esetet a 4.9 pontban mintaként — lehet, hogy maga az eredeti szöveg enged több értelmezést).
4. HA NINCS KJV/ASV-adat arra a könyvre → "közepes" megbízhatóság.
5. Ha a szó Strong-száma vagy nyelvtani szerepe MAGA is vitatott (két szomszédos, rokon Strong-szám közül bármelyik védhető) → "bizonytalan", a vitát röviden dokumentálva a sor mellett vagy a `Validacios_naplo.md`-ben.

Minden 10. újonnan generált sornál (mintavételesen) érdemes egy független forrással (pl. egy külső, kézzel ellenőrzött referenciával, ha rendelkezésre áll) össze is vetni, és az eredményt a `Validacios_naplo.md`-be rögzíteni — ez korai riasztást ad, ha a módszer valahol szisztematikusan félrecsúszna.

**A `Karoli_Strong_kivonat.tsv` "Megbízhatóság" oszlopának lehetséges értékei, egységesen, csak ezek közül:**
- **"magas"** — egyértelmű, és ha van KJV/ASV-adat arra a versre, az is megerősíti
- **"közepes"** — tartalom-alapú azonosítás, de nincs KJV/ASV kereszt-ellenőrzés (mert arra a könyvre/versre nincs KJV/ASV-Strongs adat a `konkordancia/` mappában)
- **"bizonytalan"** — a szó jelentése/nyelvtani szerepe MAGA is vitatott a forrásokban (pl. mint a Gen.1.4-nél a H2895/H2896 kettős Strong-lehetőség "jó" szóra)
- **"—"** — nincs önálló magyar megfelelés (funkciószó, mint névelő vagy tárgyeset-jel)

### 4.14 A Károli-Strong lefedettség növelésének várható előnyei — nem lineáris haszon

Ahogy a `Karoli_Strong_kivonat.tsv` lefedettsége nő (több könyv, több tanulmányból származó adat), a haszon NEM egyenletesen jelentkezik — érdemes megkülönböztetni a korai és a csak nagy léptéknél jelentkező előnyöket.

**Korai haszon — már kis lefedettségnél is jelentkezik:**

1. **Pontosabb lexikai vs. tematikus megkülönböztetés a 3/b pontnál.** A `Karoli_kereszthivatkozasok.tsv` jelenleg csak azt adja meg, mely versek kapcsolódnak — nem azt, hogy lexikailag vagy csak tematikusan. Ha egyre több kapcsolódó vershez van Károli-Strong adat is, gépileg ellenőrizhető, hogy két kapcsolódó vers ugyanazt a Strong-számot használja-e — ez a lexikai/tematikus elhatárolás egy részét gépi ellenőrzéssel is támogathatóvá teszi.

2. **A tematikus tanulmányok találati listájának gyorsabb feldolgozása.** Egy motívum keresésekor a találati lista Strong-számokat ad; ha az adott könyvben már van Károli-Strong lefedettség, a Károli-szó azonosítása egyszerű grep-pé egyszerűsödik, nem igényel új tartalom-alapú mérlegelést minden egyes találatnál.

3. **A kumulatív modell (7.1-7.2 pont) határköltsége csökken.** Minél több Károli-Strong sor van már meglévő tanulmányokból, annál kevesebb új generálás kell egy jövőbeli tanulmánynál.

**Csak nagyobb lefedettségnél jelentkező haszon:**

4. **Fordított irányú keresés — magyar szó felől.** Elég nagy lefedettségnél ellenőrizhetővé válik, hogy a Károli egy adott magyar szava mindig ugyanazt a héber/görög Strong-számot fedi-e le, vagy több különböző fogalmat mos össze — ez pontosan az a fajta "elmosódás", amit a bővített sablon 2. kiválasztási kritériuma keres, de most objektív, adatalapú jelzést kapna, nem csak egyedi felismerést.

5. **Statisztikai mintázat-felismerés — jövőbeli, nem jelenleg tervezett lehetőség.** Nagy lefedettségnél elméletileg kereshetővé válna, mely Strong-számok fordulnak elő szokatlanul gyakran ugyanazzal a Károli-szóval — objektív jelzést adhatna olyan motívum-jelöltekre, amiket eddig csak kézi, tartalmi munka tárt fel.

---

## 5. Hozzáférési korlátok — mit lehet elérni honnan

| Felület | Publikus repó (GitHub) | Privát repó (GitHub) |
|---|---|---|
| **claude.ai chat** (ez a rendszer) | ✅ klónozható, olvasható (`bash_tool`, `web_fetch`) | ❌ hitelesítés hiányában nem érhető el, hacsak nincs megadva egy szűk hatókörű PAT |
| **Claude Code** (felhasználó saját gépén) | ✅ | ✅ — a felhasználó már meglévő git-hitelesítésével natívan működik, nincs szükség tokent megosztani |

**Push/írás:** a claude.ai chat **soha nem tud közvetlenül commitolni/push-olni** semmilyen repóba (se publikusba, se privátba) — hiányzik az írási hitelesítés. Ez csak Claude Code-ban lehetséges, a felhasználó saját jogosultságával.

**Claude Code kontextus-korlátja:** Claude Code **nem látja** a claude.ai memóriarendszerét és a korábbi chat-történetet — csak azt, ami ténylegesen a repó fájljaiban van. **Ez a jelen fájl** pontosan ezt a rést hidalja át: minden itt rögzített döntés innentől fájlból, nem csak beszélgetés-emlékezetből érhető el.

---

## 6. Változtatási workflow — hogyan frissül ez a rendszer a jövőben

**Alapelv:** minden érdemi módszertani döntés, ami korábban csak beszélgetésben hangzott el, **ebbe a fájlba (vagy egy utódjába) kerül rögzítésre**, mielőtt Claude Code-alapú munka épülne rá.

### 6.1 Ha egy sablon módosul (pl. STEPBible-lépés tényleges bevezetése)
1. A módosítás **itt, ebben a fájlban** (vagy közvetlenül a sablonfájlban, changelog-fejléccel) kerül rögzítésre
2. A sablonfájl saját verziószáma és changelog-fejléce frissül (a projekt már meglévő konvenciója szerint)
3. Commit-üzenet a `GitHub_feltoltesi_workflow.md`-ben rögzített konvenciót követi: `vXX — [dátum]: [changelog lényege, 1 mondatban]`

### 6.2 Ha új könyv kerül a privát SzPA-adatbázisba
1. **Jogosultság-ellenőrzés először:** van-e legálisan megvásárolt példány a felhasználónál? Ha nincs, a feldolgozás nem indul (vagy engedélykérés a SzPA felé: sb@szpa.hu / jegyzet@szpa.hu)
2. Két tábla elkészítése a megbeszélt formátumban (verses szöveg + lábjegyzet-szótár)
3. Join-tábla elkészítése a megfelelő STEPBible-kivonattal, Strong-szám alapon, a 3. opció (explicit hiányjelzés) szerint
4. Minden új fájl a privát repó megfelelő mappájába kerül, **soha nem a nyilvánosba**

### 6.3 Ha egy már lezárt tematikus tanulmányt visszamenőleg STEPBible-lel ellenőrzünk
1. Az adott motívum Strong-számainak azonosítása
2. Teljes körű, versen belüli és szomszédos-verses egyezés-keresés a TAGNT/TAHOT-on
3. Új találatok esetén: explicit értékelés (valódi lexikai egyezés vs. csak felszíni Strong-egyezés eltérő referenssel — lásd a pneuma/pszükhé-eset Mat 12:18/1Pét 1:22 kizárását mintaként)
4. Ha új előfordulás igazolódik: a tematikus sablon 10 pontos lezárási checklistje **újra végigfuttatva** (nem csak a napló egy sorát módosítva)
5. A tanulmány saját changelog-fejléce és a napló fejléc-changelogja is frissül

### 6.4 Verziókövetés elve mindenhol
- Fájlnév-verziószám **csak explicit felhasználói kérésre** emelkedik (motívumlog-konvenció, ami minden fájlra kiterjeszthető)
- Changelog-fejléc **minden érdemi tartalmi változásnál** frissül, még ha a fájlnév-verzió nem is
- Rule-konfliktus esetén (két korábbi döntés összeütközik) — explicit rákérdezés, nem önkényes döntés (ez már korábban is rögzített projektelv)

### 6.5 Új munkamenet indításakor (akár claude.ai, akár Claude Code)
Javasolt első lépés: **ennek a fájlnak a beolvasása** a repóból, mielőtt bármilyen tanulmány- vagy sablon-munka elindul — ez biztosítja, hogy a munkamenet ne a nulláról induljon, és ne ismételje meg a már meghozott döntéseket vagy azok mérlegelését.

---

## 7. Tanulmány-készítési munkafolyamat a GitHub-alapú tudásbázissal

**Fontos megkülönböztetés:** ez a szakasz **nem a sablonok szövegét** módosítja (azt lásd külön: `Sablon_modositasok_es_motivumlog_valtozasok.md`), hanem azt írja le, **hogyan változik magának egy sablon alapján készülő tanulmány elkészítésének gyakorlata**, most hogy a teljes projekt-tudásbázis (motívumlog, sablonok, korábbi tanulmányok, tanítói lista, gyorsreferencia) egységesen, kereshetően elérhető a GitHub-repóból, nem csak beszélgetés-kontextusból vagy memóriából.

**A lényegi különbség egy szóban: verifikáció.** Eddig a sablonok által előírt "belső önellenőrzés" **deklaratív** volt (állítás, hogy megtörtént, memóriára/kontextusra támaszkodva). Mostantól **tényleges, grep-alapú ellenőrzéssé** válhat, mert minden korábbi anyag egy helyen, kereshető formában áll rendelkezésre.

**Melyik sablon-pont hogyan verifikálódik ténylegesen a repóból:**

| Sablon-pont | Korábbi gyakorlat | Új gyakorlat (repó-alapú) |
|---|---|---|
| 0. Sorozat-kontextus | kontextusból/memóriából rekonstruált | `grep` a "Feldolgozott igeszakaszok" táblán |
| 2. Eredeti nyelvi tábla | emlékezetből + esetenkénti `web_search` | STEPBible-lekérdezés közvetlenül a repóból (+ SzPA-adat, ha releváns könyv és van hozzá privát adat, Strong-szám alapú összekapcsolással) |
| 3/b. Ismétlődő motívum ellenőrzése | "eszembe jutott-e" a korábbi előfordulás | `grep` a teljes motívumlogon és korábbi tanulmányfájlokon a releváns kulcsszóra, *mielőtt* a kereszthivatkozás megfogalmazódik |
| 5. Alkalmazás (named teacher) | a jóváhagyott lista emlékezetből reprodukálva | `PaRDeS_tanitok_lista.md` közvetlen olvasása a repóból |
| Terminológiai/formai szabályok | emlékezetből betartva | `PaRDeS_gyorsreferencia.md` és a sablon saját szövege ellenőrzésként újraolvasva véglegesítés előtt |
| Napló-frissítés (7 szekció) | feltételezés alapján, mely szekció érintett | `grep`-pel ellenőrizve, ténylegesen mely szekciók tartalmaznak releváns bejegyzést |

**Gyakorlati sorrend egy új tanulmány elkészítésekor:**
1. Repó-frissítés (klónozás vagy `git pull`) a munkamenet elején
2. 0. pont: grep a "Feldolgozott igeszakaszok" táblán
3. 2. pont: STEPBible-lekérdezés (+ SzPA, ha releváns) a szakasz kulcsszavaira
4. 3/b pont: grep a motívumlogon és korábbi tanulmányokon a lehetséges ismétlődő motívumokra
5. 5. pont: grep a jóváhagyott tanítói listán, ha nevesített forrás kell
6. Belső önellenőrzés: a terminológiai szabályok tényleges újraolvasása/ellenőrzése
7. Napló-frissítés: grep-pel ellenőrizve, mely szekciók valóban érintettek, mielőtt a frissítés megtörténik

**Amit ez nem vált ki:** a tartalmi, teológiai munkát (Peshat/Remez/Drash/Sod kidolgozása, named teacher-anyag valódi keresése és értékelése, ⚠️ vitatott pontok névvel jelölt képviselőinek azonosítása) — ezek továbbra is minden egyes tanulmánynál újra elvégzendő, tartalmi munkát igénylő lépések, amiket a repó-alapú verifikáció csak **megalapoz és ellenőriz**, nem helyettesít.

### 7.1 A bővített sablon 2. pontjának kulcsszó-kiválasztási kritériumai

A max. 6-8 szó/vers kiválasztása eddig kimondatlan, csak gyakorlatban alkalmazott szempontok szerint történt. Explicit kritériumlista (legalább egynek teljesülnie kell):
1. **Teológiai súly** — a szó jelentése önmagában állítást hordoz, ami a Peshat-értelmezést érdemben alakítja
2. **Elmosódás a Károli/SzPA fordításban** — két vagy több eredeti szó egyetlen magyar szóvá olvad össze
3. **Motívum-kapcsolódás** — a szó egy már nyomon követett motívumhoz köthető
4. **Kereszthivatkozási potenciál** — a szó ritka, erős 3/b kapcsolódást tehet lehetővé
5. **Exegetikai vita forrása** — a szó jelentése önmagában ad okot egy ⚠️ vitatott pontra
6. **Objektív ritkaság (STEPBible-adat alapján)** — tájékoztató küszöb: kevesebb mint 15-20 előfordulás összesen; **nem helyettesíti**, csak kiegészíti az 1-5. szempontot

*(A pontos, beillesztendő sablon-szöveg: lásd `Sablon_modositasok_es_motivumlog_valtozasok.md`, 1.1/A pont.)*

**Tanulmányvezérelt, kumulatív generálás — hol jelentkezik a célzottság a bővítettnél:** a szűkítés **a keresés előtt**, magánál a kulcsszó-kiválasztásnál történik (a fenti 6-pontos lista alapján), nem utólag.
```
1. Kulcsszó-lista összeállítása a kritériumlista alapján (max 6-8 szó/vers)
2. Minden kiválasztott szónál: ELLENŐRZÉS — van-e már rá sor az
   osszekapcsolt.tsv-ben (grep igehely/Strong-szám szerint)?

   → HA VAN: kész, azonnal felhasználható, nulla plusz költség
   → HA NINCS:
     a) STEPBible-sor lekérése (grep TAGNT/TAHOT) — olcsó, gépi
     b) SzPA-lábjegyzet keresése, ha releváns könyv (grep) — olcsó, gépi
     c) CSAK HA a szónak nincs SzPA-lábjegyzete, DE a tanulmány mégis
        hivatkozna rá magyar szóként → tartalom-alapú (angol gloss)
        azonosítás — ez az egyetlen "drága" lépés, és csak 1-2 szót érint
3. Az újonnan generált sorok VISSZAÍRÁSA (append) az osszekapcsolt.tsv-be
4. A tanulmány 2. pontja ebből az adatból épül fel
```
**A gyakorlati tapasztalat:** egy átlagos bővített tanulmánynál a 10-20 kiválasztott kulcsszóból jellemzően csak **1-3 szükségel** ténylegesen tartalom-alapú azonosítást — a többi vagy lábjegyzet-alapú (ha van SzPA-adat), vagy egyszerűen nem is igényel magyar szó-azonosítást (a Strong-adat és a szótő önmagában is elég a Peshat-elemzéshez).

### 7.2 Tematikus sablonra épülő tanulmányok — eltérő munkafolyamat

A tematikus sablon **szerkezetileg más léptékű** feladat, mint a bővített: nem egy szakasz kulcsszavainak kiválasztásáról van szó, hanem arról, hogy **a teljes kánonban** megtaláljuk egy motívum összes előfordulását.

**Miért más a token-gazdaságossági profil:**
- **A keresési lépés maga olcsó, gépi feladat** — `grep` a teljes TAGNT/TAHOT-on egy-két Strong-számra pillanatok alatt lefut (lásd a pneuma/pszükhé-ellenőrzés precedensét)
- **A találati lista értékelése** (valódi lexikai egyezés vs. felszíni Strong-egyezés eltérő referenssel, mint a Mat 12:18/1Pét 1:22 kizárása) igényel tartalmi mérlegelést, de ez jellemzően **néhány, legfeljebb egy-két tucat jelöltre** korlátozódik — hasonló nagyságrendű munka, mint egy bővített tanulmány kulcsszó-elemzése, nem egy teljes könyv minden szava

**Az SzPA-integráció itt eltérő korlátba ütközik:** egy motívum előfordulásai jellemzően **sok különböző könyvet** érintenek (a pneuma/pszükhé-motívum pl. 1Móz, 1Thessz, Zsid, 1Kor, Luk, Fil, Mt, 1Pét helyeket is érint), miközben a privát SzPA-adatbázis **jelenleg csak két könyvet** fed le (Példabeszédek, ApCsel 1-14). Ez azt jelenti, hogy egy tematikus tanulmány találatainak **túlnyomó része** nem fog SzPA-adattal rendelkezni — a "nincs SzPA-lábjegyzet, csak STEPBible-adat" eset itt **tipikus**, nem kivételes, amíg a privát adatbázis nem bővül.

**Konkrét workflow tematikus tanulmánynál:**
```
1. Motívum kulcsszavának Strong-száma azonosítva (motívumlog vagy felhasználói megadás alapján)
2. Teljes körű grep TAGNT/TAHOT-on (mindkettőn, ha a motívum ÓSZ-ÚSZ ívet ír le)
3. Találati lista → egyenkénti tartalmi értékelés: valódi egyezés vagy kizárandó
4. A megerősített előfordulásoknál: van-e SzPA-lefedettség (jelenleg csak Péld/ApCsel)?
   → ha VAN: join-tábla ellenőrzés/bővítés, ugyanaz a kumulatív modell, mint a bővített sablonnál
   → ha NINCS: explicit jelzés, csak STEPBible-adat szerepel
5. Napló-frissítés + a Lezárási checklist 11. pontja (🔍 STEPBible-ellenőrizve, keresési paraméterekkel)
```

**Fontos egybeesés:** ez pontosan az a workflow, ami a négy már lezárt tematikus tanulmány (tehóm, segítségül hívni, Rafeusok, hádész) visszamenőleges felülvizsgálatánál is alkalmazandó lenne (lásd 8. szakasz, nyitott pontok) — nem külön eljárás, hanem ugyanaz a lépéssor.

**Hol jelentkezik a célzottság a tematikusnál — strukturálisan fordítva, mint a bővítettnél:** itt **nincs előzetes válogatás**, mert a feladat maga (egy motívum összes előfordulásának megtalálása) megköveteli a teljes kánon átfésülését — a szűkítés **a keresés eredménye után**, a találati listánál jelentkezik. A találati lista (jellemzően néhány, legfeljebb 1-2 tucat vers) **már eleve** a "célzott halmaz" — nincs szükség külön, keresés előtti válogatásra, mint a bővítettnél.

**A két modell közötti kulcskülönbség egy mondatban:**
- **Bővítettnél:** előre eldöntjük, mely szavak érdekesek (kritériumlista), *utána* nézzük meg őket
- **Tematikusnál:** a keresés maga dönti el, mi érdekes (a Strong-szám találati listája), *utána* értékeljük, melyik valódi

Mindkét esetben ugyanaz a **kumulatív alapelv** érvényesül: minden generált sor **visszakerül** a privát join-táblába, így egy következő tanulmány, ami ugyanarra a versre/szóra hivatkozik, **már nem generál újra semmit** — csak `grep`-el.

---

## 8. Nyitott pontok (ide kerül minden, ami eldöntetlen maradt)

- [⏸️] **SzPA-integráció felfüggesztve, bizonytalan időre (felhasználói döntés, 2026.08.24).** A privát repó, a két-táblás SzPA-struktúra (versek + lábjegyzetek) és a háromoszlopos [Károli+SzPA] join-tábla terve VÁLTOZATLANUL ÉRVÉNYES marad, csak AKTÍV BŐVÍTÉSE szünetel. A már elkészült minták (Péld 1:1-9, ApCsel 1:1-4) megmaradnak referenciaként. Gyakorlati következmény: minden jövőbeli join-tábla-építés a "csak Károli" (kétoszlopos: Strong + Károli, SzPA-oszlop nélkül) formában készül, publikus repóban — nincs szükség a privát repó aktív használatára, amíg ez a felfüggesztés fennáll. Ha egyszer az SzPA-munka újraindul, a korábban rögzített 4.1-4.2, 6.2, 7.1-es pontok módszertana változtatás nélkül alkalmazható.
- [ ] **Károli-kiadás ellenőrzése:** a scrollmapper HunKar-adat az 1908-as revideált Károli-kiadás — ellenőrizendő, hogy a projekt korábbi tanulmányaiban idézett Károli-szövegek ugyanezzel a kiadással egyeznek-e, mielőtt a strukturált adatbázist visszamenőleg is hitelesítő/ellenőrző forrásként használnánk
- [x] **Strong-taggelt Károli — lezárva, döntés megszületett (4.7).** Mélykutatással azonosítva: Biblia-Felfedező (Bible-Discovery, Zsidó Miklós) — valódi, teljes, szó-szintű Strong-párosítás, de zárt licenc, adatkiemelés csak egyedi engedéllyel. **A projekt saját Károli-datasete emiatt nem erre épül**, hanem a közkincs HunKar-szövegre és a már kidolgozott tartalom-alapú generálási módszerre; a Biblia-Felfedező legfeljebb ellenőrző referenciaként vonható be, ha valaha hozzáférhető lesz.
- [x] **A tematikus/bővített/mélyelemzés sablonok tényleges szövegmódosítása a STEPBible-lépésekkel — lezárva (v22).** `2_PaRDeS_bovitett_sablon.md` (v7→v8): a 2. pontba felvéve a kulcsszó-kiválasztás 6 szempontos kritériumlistája (ez korábban csak a döntési fájl 7.1 pontjában, a sablonfájlban nem volt jelen); a 3/b pont végére felvéve a STEPBible TAGNT/TAHOT kötelező ellenőrzés. `4_PaRDeS_tematikus_sablon.md` (v3→v4): az 1. pont táblázata után felvéve a kötelező STEPBible-egyezés-ellenőrzés; a Lezárási checklist kiegészítve egy **új 11. ponttal** — **ellenőrizve, hogy a checklist a módosítás előtt ténylegesen csak 10 pontos volt** (nem duplikálva semmit). `5_Melyelemzes_prompt_sablon.md` (v2→v3): a 2. pont végére felvéve a STEPBible-lekérdezés. Mindhárom fájlban a pontos, előre egyeztetett szöveg került beillesztésre.
- [ ] **A négy már lezárt tematikus tanulmány visszamenőleges STEPBible-ellenőrzése és Károli-Strong join-építése** (lásd 4.12-es lefedettségi táblázat és `Join_tabla_folyamat_magyarazat.md` — ez most kettős haszonnal jár: validál ÉS join-adatot generál):
  - [ ] Tehóm/Abüsszosz tematikus tanulmány
  - [ ] Segítségül hívni az Úr nevét tematikus tanulmány
  - [ ] Rafeusok/óriás-népek tematikus tanulmány
  - [ ] Hádész tematikus tanulmány
- [x] **TIPNR-lekérdezés Ábrahám/Ábrám névalakjaira — lezárva (v19).** A teljes TIPNR legenerálva `konkordancia/TIPNR_kivonat.tsv`-be; Ábrahám (H0085) és Ábrám (H0087), ill. Sára (H8283) és Szárai (H8297) külön Strong-számmal, teljes előfordulási listával szerepel — az 1Móz 17-es tanulmány előkészítése kész.
- [ ] Php 1:27 végleges döntés — bekerüljön-e ötödik (korporatív jellegű) előfordulásként a pneuma/pszükhé tanulmányba
- [ ] A teljes Példabeszédek és ApCsel könyvek tényleges feldolgozása a két-táblás + join struktúrában (eddig csak minta készült, 1:1-9 ill. 1:1-8 terjedelemben)
- [ ] Döntés arról, hogy a claude.ai chat-felületen történő jövőbeli munkához készül-e szűk hatókörű PAT a privát repóhoz, vagy a munka véglegesen Claude Code-ra kerül át
- [x] **ESV Strong-taggelt hozzáférés — lezárva, nem járható út.** Megvizsgálva: (1) Crossway API — max. 500 vers/fél könyv tárolható helyben; (2) Crossway formális engedélykérés (`crossway.org/permissions/`) — egyedi elbírálású, nincs önkiszolgáló opció; (3) Accordance Bible "ESV with Strong's" modul ($19,90-39,99) — a szoftvergyártó saját dokumentációja explicit kimondja, hogy a megvásárolt szövegek tömeges exportálása más formátumba "gyakran sérti a licencfeltételeket". **Egyik út sem ad jogilag tiszta, azonnal járható megoldást** — a STEPBible interlineáris angol gloss + tartalom-alapú azonosítás marad az elsődleges módszer.
- [ ] **Figyelendő, jelenleg még nem elérhető STEPBible-adatállományok:** a STEPBible-Data README "Datasets coming" szakasza szerint két, fejlesztés alatti forrás érdemi haszonnal járna, ha megjelenik:
  - **TAGOT** (Translators Amalgamated Greek OT — Septuaginta, teljes taggelt szöveg) — ez pótolná a mélyelemzés-sablonnál azonosított hiányzó láncszemet (annak ellenőrzése, hogy egy ÚSZ-i idézet a LXX ugyanazon görög szavát használja-e, mint a héber eredeti fordítása — a "tudatos idézet vs. véletlen egybeesés" kérdés eldöntéséhez)
  - **TBCWG** (Translators Biblical Concept Word Groups — rokon jelentésű szócsoportok, szinonima-elhatárolással) — ez közvetlenül segítené a motívumlog "rokon motívum-csoport küszöbszámítás" elvét
  - Kisebb jelentőségű, szintén készülő: **TOTMM/TNTMM** (kéziratos tanú-adatok szövegkritikai variánsokhoz), **TFBDB** (teljes BDB héber lexikon)
- [x] **Könyv-rövidítés normalizáló tábla — lezárva (v19).** Elkészült `konkordancia/Konyv_normalizalo_tabla.tsv` néven, mind a 66 könyvre (STEPBible angol rövidítés ↔ magyar rövidítés ↔ teljes magyar könyvnév). Két korpuszbeli ellentmondás (Máté/Mt, Ezékiel/Ez↔Ezék) felhasználói egyeztetéssel eldőlt: `Mt`, `Ez`.
- [ ] **Károli-revízió sokféleség — nyitva, nem eldöntött (v21-ben azonosítva, lásd 4.7 és 4.11).** A "Károli" név alatt legalább két, szövegszerűen eltérő kiadás létezik: a jelenleg publikus datasetként használt **1908-as HunKar** (scrollmapper, közkincs) és a **"Revideált Károli" (Veritas Kiadó, 2011)** — modernizált alakokkal (pl. "volt"/"sötétség"/"lebegett" a "vala"/"setétség"/"lebeg vala" helyett), © védett, **nem közkincs** (forrás: karolibiblia.hu, Protestáns Média Alapítvány szakbizottsága). A Biblia-Felfedező program (Baranyi László Zsolt, a Veritas Kiadó engedélyével) feltehetően ezt a 2011-es revíziót futtatja. **Nyitott kérdés:** ha a felhasználó igazolt, jogszerű hozzáféréssel rendelkezik a Veritas 2011-es szöveghez, érdemes-e azt egy külön, **privát** datasetként (a SzPA-mintára, `Bible-Study-privat/`-ba) felépíteni, összevetés/kereszt-ellenőrzés céljából a publikus HunKar mellett? A publikus `Karoli_1908.tsv` semmiképp nem cserélendő rá.
