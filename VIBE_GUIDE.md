# Vibe coding guide — a PaRDeS munkaterv végigvitele Claude Code-dal

Oct 3, 2026 · @basesoft

## 1. Mi ez, és hogyan használd

Ez a guide a `MUNKATERV.md` kilenc tervezett feladatát (kódnévvel: TERV\_BEFOGAD … SZPA\_AUDIT; FELADATOK-számot a `/befogad` ad, DT-F52a; azóta: BDB\_ADATBLOKK = #56, STRONG\_NORMALIZAL = #62, JELOLTEK\_RETRO = #63, KAROLI\_ELLENORZES = #65, SQLITE\_EPIT = #79, OLVASOI\_KONKORDANCIA = #76 (= #25a), DT-M1, DT77 (12)) viszi végig Claude Code-dal úgy, hogy te irányítasz, Code végez, és a repó szabályai (CLAUDE.md, MUNKAMENET.md, playbook) betartatják magukat. Nem programozási tankönyv: azt mondja meg, **mit írj a promptba, mire figyelj a futás közben, és mikor állj meg.**

Három dokumentum együtt:

| dokumentum | mire | mikor nyitod |
| --- | --- | --- |
| `ADATVAGYON_TERV.md` | *miért* — a terv, a döntések, a séma-illesztés | ha egy feladat értelme kérdéses |
| `MUNKATERV.md` | *mit* — feladatok, sorrend, elfogadás, megállások | minden session előtt: melyik feladat jön |
| ez a guide | *hogyan* — a session menete, promptok, jelek | a session közben, nyitva |

A guide feltételezi: a repó klónozva, Claude Code a repó gyökerében fut, a `/kovetkezo` és `/befogad` parancsok élnek, és a 0. lépcső kézi fájljai bent vannak.

## 2. A vibe coding három szabálya ebben a projektben

A „vibe coding" itt nem azt jelenti, hogy leírod, mit szeretnél, és elfogadod, ami jön. Ebben a repóban az adat az érték, a kód csak hozzáfér; ezért a három szabály az adatot védi.

**1. Adat, nem kód.** Egy session sikerét nem az méri, hogy fut-e a script, hanem hogy az `adat/*.tsv` jó-e utána. Minden session végén egy kérdést teszel fel: *mi változott az `adat/`-ban, és miből tudom, hogy helyes?* Ha Code csak kódot mutat és nem TSV-diffet, nem vagy kész.

**2. Brief, nem chat.** Code nem a chatből dolgozik, hanem a `F<nn>_<NEV>_BRIEF.md`-ből. Ha menet közben jut eszedbe valami, nem a promptba írod, hanem a briefbe (Code-dal), és újraindítod a lépést. Így a következő session — vagy egy másik modell — ugyanazt kapja, és a döntés nem a chatben vész el.

**3. Kis minta, aztán ⛔.** Egyik feladat sem fut először teljes adaton. A `MUNKATERV` „kis minta" oszlopa a próba; azt nézed meg, és csak jóváhagyás után mondod: *most a teljes.* A ⛔ nem Code hibája, hanem a te lépésed — ha nem állsz meg, a hiba a teljes adaton ismétlődik.

És egy negyedik, ami a repóé: **proveniencia.** Minden szám, igehely, idézet, amit Code a kimenetbe ír, lekérdezésből jön, és a lekérdezés nyoma ott van (`scope=… | forras=… | ts=…`). Ha egy állítás mellett nincs, rákérdezel: *honnan?* — és ha fejből, akkor az nem adat.

## 3. Egy session anatómiája

Egy session = egy feladat (vagy egy feladat egy lépcsője). Hat lépés, mindig ugyanabban a sorrendben.

| # | lépés | te | Code | jel, hogy mehet tovább |
| --- | --- | --- | --- | --- |
| 1 | **tájékozódás** | `/kovetkezo` — vagy megmondod, melyik feladat | beolvassa a CLAUDE.md-t, a briefet (ha van), az `olvas:` listát; összefoglalja, mit fog csinálni | az összefoglaló egyezik a MUNKATERV sorával; a függések zöldek |
| 2 | **brief** | ha nincs brief: *írd meg a briefet a MUNKATERV #nn sora alapján, ne kezdj még semmit* | megírja a `F<nn>_<NEV>_BRIEF.md`-t: cél, bemenet, kimenet, kis minta, elfogadás, megállások | elolvasod; ami hiányzik vagy rossz, azt a briefbe íratod, nem a chatbe |
| 3 | **kis minta** | *futtasd a kis mintát, és állj meg* | lefuttatja, kiírja a kimenetet és a provenienciát | megnézed a mintát **adat-szinten** (TSV-sorok, nem log); 1–3 tétel kézzel ellenőrizve |
| 4 | **teljes futás** | *mehet a teljes* | lefuttatja, naplóz, PR-t nyit (draft) | a napló (`naplok/F<nn>_*.md`) tartalmazza a számokat; a TSV-diff olvasható |
| 5 | **ellenőr** | új session: *fuggetlen-ellenor a #nn PR-jére* | egy másik menet (Haiku/Sonnet) a brief elfogadási pontjai ellen nézi | az ellenőr jelentése 0 elutasított tételt ad, vagy a tételek javítva |
| 6 | **befogadás** | `/befogad` | commit UTF-8 üzenetfájlból, DONTESEK-sor ha kell, FELADATOK státusz | a `git log` egy feladatot mutat, a FELADATOK-sor ✅ |

**Mikor szakítod meg?** Ha Code (a) az `adat/`-ba ír a briefen kívül, (b) fejből mond igehelyet vagy számot, (c) a kis mintát átugorja, (d) egy másik feladatba nyúl („közben javítottam a…"), (e) a briefet a chat alapján módosítja magától. Mind az ötre a válasz: *állj, vond vissza, és írd a briefbe, mit akartál.*

**Mennyi egy session?** Egy feladat egy lépcsője; a MUNKATERV „menet" oszlopa (½, 1, 1–2, 2–3) a session-számot becsli. Ha egy session a harmadik javítókörnél tart, nem a modellt cseréled, hanem a briefet nézed meg: valószínűleg nem mondja ki, mit fogadsz el.

## 4. Prompt-sablonok

Rövid, utasító, és mindig megmondja, hol kell megállni. A `<…>` helyére a MUNKATERV sora kerül.

**4.1 Brief-íratás** (új feladatnál, a 2. lépés)

```
Olvasd el a MUNKATERV.md #<nn> sorát és az ADATVAGYON_TERV.md <szakasz> szakaszát.
Írd meg az F<nn>_<NEV>_BRIEF.md-t a repó brief-formája szerint:
cél, bemenet, kimenet, kis minta, elfogadási pontok, megállások (⛔), olvas: lista.
Ne futtass semmit. Ne módosíts más fájlt. Ha a MUNKATERV sora és a repó állapota
ellentmond, írd a brief „Nyitott kérdések" szakaszába, ne döntsd el.
```

**4.2 Kis minta** (3. lépés)

```
A F<nn> brief szerint futtasd a kis mintát: <mi a minta>.
Állj meg a minta után. Mutasd: (1) a módosított/létrehozott TSV-sorokat diffként,
(2) minden lekérdezés proveniencia-sorát, (3) amit nem tudtál adatból megválaszolni.
Az adat/ mappát ne commitold.
```

**4.3 Ellenőrző kérdések a minta után** (ezeket te teszed fel, egyenként)

```
A <konkrét sor>-t honnan vetted? Mutasd a lekérdezést.
Ez a szám a naplóban hogyan jön ki? Számold újra.
Melyik SEMA-szabály vonatkozik erre a sorra, és teljesül-e?
```

**4.4 Teljes futás** (4. lépés)

```
Mehet a teljes futás a F<nn> szerint. Naplózz a naplok/F<nn>_<nev>.md-be:
mit futtattál, hány sor, hány eltérés, mi maradt nyitva.
A végén nyiss draft PR-t egy ágon; a commit-üzenet UTF-8 fájlból.
Ha integritási szabály sérül, állj meg, ne javítsd kézzel.
```

**4.5 Független ellenőr** (5. lépés, új session)

```
fuggetlen-ellenor: a F<nn> brief elfogadási pontjai szerint nézd át a <PR>-t.
Minden pontra: teljesül / nem teljesül / nem eldönthető, egy sorban indokkal.
Ne javíts, csak jelents, a naplok/ELLENOR_F<nn>.md-be.
```

**4.6 Javítás** (ha az ellenőr talált valamit)

```
Az ELLENOR_F<nn>.md <tétel> pontját javítsd. Csak azt. Utána a kis mintát futtasd újra,
és mutasd a diffet. Ha a javítás a briefet is érinti, előbb a briefet módosítsd.
```

**4.7 Lezárás** (6. lépés)

```
/befogad
```

és ha döntés született közben: *vedd fel a DONTESEK.md-be: \<DT-tétel egy mondatban>, forrás: F\<nn>, dátum.*

**4.8 Ami sosem kerül a promptba:** „csináld meg ahogy jónak látod", „javítsd, ami kell", „commitold az egészet". Ezek a három szabály ellentétei.

## 5. Feladatonkénti vezérfonal

Minden feladathoz: mit mondasz az 1. lépésben, mire figyelsz a mintánál, mi a jó és a rossz jel. A részletek a MUNKATERV 4. szakaszában.

| # | első prompt (a sablon mellé) | a mintánál ezt nézed | jó jel | rossz jel |
| --- | --- | --- | --- | --- |
| TERV\_BEFOGAD | *Vedd be az ADATVAGYON\_TERV.md-t és a MUNKATERV.md-t a gyökérbe; a #23 és #25 brief olvas: listájába; az ATALAKITASI\_TERV 4.7-et jelöld elavultnak egy sorral, ne írd át; a CLAUDE.md KJV-sorát javítsd.* | a diff négy fájlt érint, mást nem | három rövid módosítás, egy commit | Code „közben rendbe tette" az ATALAKITASI\_TERV más részeit |
| #65 KAROLI\_ELLENORZES | *Kis minta: ANTROP-001. Csak `magas` link számít egyezésnek. A triplet-frissítést mutasd soronként, ne írd be, amíg nem jóváhagytam.* | 3 eltérés-sort kézzel: nyisd meg a Károli-verset és a `parok` sort | az eltérések egy része a tanulmány hibája, más része `alacsony` link — mindkettő külön listán | minden sor „egyezik" (gyanúsan tiszta), vagy a `tartalom-alapú` sorokat kérdés nélkül átírta |
| #62 STRONG\_NORMALIZAL | *Egy függvény, egy helyen; a `lekerdez.py` és a `betolt.py` ezt hívja; a 20 ismert alakra teszt.* | a teszt tényleges TSV-beli alakokat használ, nem kitaláltakat | a függvény 15 sor, a teszt zöld, a TSV-javítás diffje olvasható | regex-vadászat több fájlban; „kézzel javítottam a TSV-t" |
| #79 SQLITE\_EPIT | *Előbb a séma a SEMA.md-ből, tábláról táblára; mutasd a CREATE-eket, mielőtt betöltesz. A nyolc integritási szabály tesztként, sértésnél áll.* | 1Mózes + 8 motívum betöltve; 3 lekérdezés a 26 pontból, és az eredmény egyezik egy ismert tanulmány-ténnyel | 0 integritási sértés; a `pardes.db` a `.gitignore`-ban; a `szamozas` a BSB-értékkészletet használja | a script a `csv` modult használja; igehelyet nem normalizál; „kihagytam a szabály-tesztet, mert lassú" |
| MCP\_BUROK | *Legfeljebb 8 eszköz, mind a `lekerdez.py`-t hívja; minden hívás auditok-sort ír: a `lepes` a kutatási lépés kódja vagy `adhoc`, `csatorna=mcp` a proveniencia-sorban (DT-M3, DT49); csak olvasó.* | ugyanaz a kérdés CLI-n és eszközön át ugyanazt adja, provenienciával | az eszközteszt-napló egyezést mutat; az `auditok.tsv` új sorai szabályosak | 15 eszköz; az MCP SQL-t ír a `lekerdez.py` megkerülésével; író eszköz „kényelemből" |
| #56 BDB\_ADATBLOKK | *A 12.1 lekérés build-lépésként; a blokk minden száma és idézete eszköz-kimenetből; `terminologia.tsv` minden adagban.* | 10 szócikk blokkja: egy Károli-idézetet nyiss meg és vess össze | a blokk szabott (400–800 token), a hiányzó adat „—", nem pótolt | a modell magyarítja a példaverset; a blokk 2000 token; a #38 adagjai nélküle indultak |
| #63 JELOLTEK\_RETRO | *Motívumonként egy session. A `beépítve` csak napló-szöveggel; ha nincs, `nyitva`. A „még nem vizsgált" lista származtatott, ne töltsd ki kézzel.* | ANTROP-001: 5 `jeloltek`-sort a napló szövege mellett | minden ★-nak van `dontes` + `indoklas`; a nem vizsgált 0 | Code `beépítve`-t ad napló-hivatkozás nélkül; „kitaláltam az indoklást a tanulmányból" |
| #76 OLVASOI\_KONKORDANCIA | *Csak a `pardes.db`-ből; a szó-lap a szerepmátrix `allapot` oszlopa szerint tölt; minden blokk alatt forrás és licenc, a mód-szűrő a `licencek.tsv` `kereskedelmi` oszlopa szerint (DT-F33j, N-F33b). A hosting-döntés után.* | 20 vers + 20 Strong lapja: nincs blokk dataset-kulcs nélkül; kereskedelmi módban egy `kereskedelmi=nem` forrásból jövő mező sem látszik; az üres blokk jelölt | a lapok a 26-ból a motívum nélküli pontokat mind kiszolgálják; a backend-válaszban nincs nyers adat | a lap „szépítésként" fejből pótol; a TSV-t a böngészőbe küldi; a tipográfia-kapcsoló előbb kész, mint a mód-szűrő és a blokkonkénti forrásjelölés |
| SZPA\_AUDIT | *Csak jelentés, nem javítás: a C-táblázat a tanulmányok prózájára és a BDB-fordításra.* | 2 tanulmány + 50 szócikk sorai | a tiltólistás szavak száma és helye táblában; nincs átírás | Code „egyúttal kijavította" a tanulmány szövegét |

## 6. Határok

**Amit te nem csinálsz**

- Nem írsz kódot, és nem javítasz TSV-t kézzel. Ha egy sor rossz, Code-dal javíttatod, briefen át — így a javítás is provenienciát kap.
- Nem döntesz a chatben. A DT-tétel a `DONTESEK.md`-ben születik, a brief hivatkozza; a chat csak elmondja.
- Nem ugrasz feladatot. Ha az SQLITE\_EPIT közben az OLVASOI\_KONKORDANCIA jut eszedbe, a MUNKATERV-be írod (Code-dal), nem a folyó session promptjába.
- Nem olvasol nyers adatot a fő szálban. A TAHOT-kivonatot, a KJV-t nem nyitod meg a chatben; a `lekerdez.py` kivonatát kéred.

**Amit Code nem csinál** (és ha mégis, az a 3. szakasz megszakítási jele)

- Nem ír az `adat/`-ba a briefen kívül; nem commitol `pardes.db`-t; nem módosít briefet a chat alapján.
- Nem mond igehelyet, Strong-számot, idézetet fejből. Ha nem tud lekérdezni, azt mondja: *nem tudom lekérdezni*, és leírja, mi hiányzik.
- Nem dönt licencről, forrásról, sorrendről. Javasol, és ⛔-ban megáll.
- Nem futtat teljes adaton kis minta és jóváhagyás nélkül.
- Nem „takarít" más feladatok fájljaiban.

**Ami közös:** a session végén mindketten ugyanazt a három dolgot nézitek — a TSV-diffet, a naplót, és hogy a brief elfogadási pontjai pipálva vannak-e. Ha ebből bármelyik hiányzik, a session nincs kész, bármilyen jónak tűnik a kód.

## 7. Gyakori hibák és javításuk

| tünet | ok | javítás |
| --- | --- | --- |
| Code „kész"-t mond, de a TSV nem változott | kódot írt, adatot nem; vagy a kimenetet `naplok/`-ba tette | *Mutasd az `adat/` diffjét. Ha üres, mi volt a feladat kimenete a brief szerint?* |
| egy szám a naplóban nem egyezik a tanulmányéval | fejből, vagy más scope-pal (`range:` vs `TAHOT-teljes`) | *Melyik lekérdezés adta? Mutasd a proveniencia-sort.* Ha nincs, újrafuttatás; ha más scope, a napló jelölje |
| a kis minta „tökéletes", a teljes futás tele van hibával | a minta nem reprezentatív (csak könnyű eseteket vett) | a MUNKATERV „kis minta" oszlopa szerint a mintába kerül nehéz eset is (eltolódásos vers, `alacsony` link, binyan-jelentés) |
| Code több feladatot csinált egy sessionben | a prompt nyitva hagyta („és ha már ott vagy…") | vond vissza a többletet; egy session = egy feladat; a többlet a MUNKATERV-be |
| a brief minden sessionben változik | a chatben döntöttél, Code átírta | a brief csak explicit kérésre módosul; a döntés DT-tétel |
| az ellenőr mindent elfogad | ugyanaz a session nézi, ami csinálta | új session, más modell; az ellenőr briefje a kész brief elfogadási pontjai, nem a kód |
| Code a `csv` modult vagy inline bash-t használ héberrel | a CLAUDE.md shell-szabálya nem volt a kontextusban | *Olvasd el a CLAUDE.md shell-szakaszát, és írd át.* (N26: hook kell rá) |
| „nem fér a kontextusba" | nyers TSV-t olvasott be | a `lekerdez.py` kivonata, `minta=3`; nagy fájlt az SQLITE\_EPIT után a `pardes.db`-ből |
| a lap szép, de a licenc-jelölés és a mód-szűrő hiányzik | a vizuális munka előbb készült el | az OLVASOI\_KONKORDANCIA elfogadási pontja: blokk dataset-kulcs nélkül = 0, és kereskedelmi módban `kereskedelmi=nem` forrásból jövő mező = 0 (DT-F33j, N-F33b); ez előbb, a tipográfia utána |
| a session harmadik javítókörnél tart | a brief nem mondja ki az elfogadást | állj, a briefbe írd be az elfogadási pontot, és onnan indulj újra |

## 8. Döntésnapló

| dátum | döntés / változás | státusz |
| --- | --- | --- |
| 2026-10-03 | v1: vibe coding guide a MUNKATERV #47–#55 végigviteléhez — három szabály, hatlépéses session, nyolc prompt-sablon, feladatonkénti jelek, határok, hibatábla | tervezet |
| 2026-10-03 | A guide a repó meglévő szabályait (CLAUDE.md három szabály, MUNKAMENET lépések, playbook kis minta, `/befogad`, `fuggetlen-ellenor`) alkalmazza, nem ír újakat; a repóba `VIBE_GUIDE.md`-ként kerülhet | megjegyzés |
| 2026-10-04 | v2 (#52 TERV\_SZINKRON, 1. futás): a tervezett feladatok sorszám helyett kóddal (DT-F52a; az 1., 5., 6., 7. szakasz hivatkozásai); tartalmi változás nincs. Kérdéses, döntésre vár: az 5. szakasz OLVASOI\_KONKORDANCIA sorának és a 7. hibatábla licenc-sorának „STEPBible-származék = 0" állítása a DT-F33f/j után (a napló listázza) | szinkron |
| 2026-10-04 | v3 (#52, 1. futás, felhasználói döntés a chatben): a v2-ben kérdésesnek jelölt két licenc-sor (5. szakasz OLVASOI\_KONKORDANCIA, 7. hibatábla) a DT-F33f/j és az N-F33b szerint — blokkonkénti forrásjelölés és a `kereskedelmi` oszlop szerinti mód-szűrő a STEPBible-kizárás helyett; a MUNKATERV 6. szakaszával egyezően | szinkron |
| 2026-10-06 | v4 (#52, 2. futás): az 5. szakasz név oszlopában a számot kapott feladatok száma (#56, #62, #63, #65), az 1. szakasz bevezető mondata ennek megfelelően. A MUNKAMENET és a BRIEF\_SABLON szabálya a guide-ot nem érinti. Az 5. szakasz MCP\_BUROK sorának „`lepes=MCP`” állítása a DT-M3 szerint átírva (a `lepes` a kutatási lépés kódja vagy `adhoc`, `csatorna=mcp` a proveniencia-sorban; DT49, felhasználó, 2026-10-06) | szinkron |
| 2026-10-09 | v5 (#52, 3. futás): az 1. szakasz bevezető mondata és az 5. szakasz név oszlopa a számot kapott SQLITE\_EPIT = #79 és OLVASOI\_KONKORDANCIA = #76 (= #25a) szerint (DT77 (12), DT-M1). A MUNKAMENET (a #23 4. szabály mércéje: L1–L7 + DT2) és a BRIEF\_SABLON (`lexikon/` nem motívumfájl, `munka` kivételek) változása a guide-ot nem érinti. Az 5. szakasz MCP\_BUROK és SZPA\_AUDIT sorának „feltételes” jelölése (DT-M7, DT77 (13)) a brief 6. pontja szerint a felhasználó döntésére vár: DT91 | szinkron |
