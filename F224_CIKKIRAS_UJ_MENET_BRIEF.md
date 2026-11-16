---
feladat: 224
cim: A cikkírás új menete — szerepfájlok, kinyerés, bizonyítéklap, szabályhelyek és elfogadási próba
kod: CIKKIRAS_UJ_MENET
tipus: feladat
fazis: folyamat
sav: SYSTEMS
modell: opus
allapot: megallt
ag: claude/f224-cikkiras-uj-menet
ad: a jóváhagyott 3. változat (2026-11-15) tizenhárom tétele a saját szabályhelyén — új bíráló- (Sonnet) és állítás-ellenőr szerepfájl (Opus, DT-F224b), szűkített lektor (Fable marad), állításonkénti kinyerés, bizonyítéklap-eszköz, érvnapló, tanulmányblokk-szabály, mérőtábla, a határ-ellenőr Sonnetre —, és egy elfogadási próba a két ismert hibahalmazon, számszerű küszöbbel
kovetkezo: "Te: ⛔ DT-F224e (az érvnapló helye: naplok/ERVNAPLO_<ID>.md vagy a forrás az F218 után) — utána a brief-zárás (a jelentés Zárás szakasza, allapot: lezarva); a független ellenőrzés és a javítókör kész (naplok/F224_jelentes.md); N-F224b, N-F224g nyitva"
munka: folyamat
olvas: [CLAUDE.md, MUNKAMENET.md, BRIEF_SABLON.md, .claude/agents/lektor.md, .claude/agents/hatar-ellenor.md, .claude/agents/fuggetlen-ellenor.md, .claude/commands/kiadas.md, eszkozok/proza_allitas.py, eszkozok/teszt_proza_allitas.py, eszkozok/lekerdez.py, eszkozok/tanulmany_kinyer.py, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, adat/SEMA.md, adat/jeloltek.tsv, adat/kapcsolatok.tsv, konkordancia/, motivumok/HAMART-001.md, motivumok/ISTENTISZT-001.md, naplok/ALLITAS_HAMART-001.md, naplok/ALLITAS_ISTENTISZT-001.md, naplok/KIADAS_HAMART-001_lektor.md, naplok/HIBA_MECHANIZMUSOK.md, DONTESEK.md]
ir: [.claude/agents/allitas-ellenor.md, .claude/agents/biralo.md, .claude/agents/lektor.md, .claude/agents/hatar-ellenor.md, .claude/commands/kiadas.md, eszkozok/proza_allitas.py, eszkozok/teszt_proza_allitas.py, eszkozok/bizonyiteklap.py, eszkozok/teszt_bizonyiteklap.py, adat/SEMA.md, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, MUNKAMENET.md, naplok/F224_jelentes.md, naplok/F224_proba.md, naplok/F224_proba/, naplok/SZIVARGAS_HAMART-001.tsv, naplok/SZIVARGAS_ISTENTISZT-001.tsv]
fugg: [218]
nem_fugg: [70, 74, 123, 205, 212, 217, 221]
---

# F224_CIKKIRAS_UJ_MENET_BRIEF.md — A cikkírás új menete

*FELADATOK #224 · Modell: opus · v1 (tervezet) · 2026.11.15 · forrás: `TERV_CIKKIRAS_v3_EGYSEGES_2026-11-15.md` (a felhasználó jóváhagyása 2026-11-15: a konszenzusos terv „mehet” a hat döntéssel; a 3. változat modellkiosztása: „így menjen / a lektor még marad fable”; a küszöbök a 10. szakasz szerint), a mérés: `MERES_VISSZAJATSZAS_2026-11-15.md` (mindkettő az orkesztrátor megosztott jegyzetmappájában). Alap: main `f5a8d2e7`.*

**A `fugg` és a `nem_fugg` indoka** (a /befogad `fuggesek --extra` kimenetéből, 2026-11-15; ha más tétel is megjelenik, az ⛔, nem felülírás):
- **218 (fugg)** — a #729 (nyitott) a fejlécén kívül a `sablonok/9_PaRDeS_motivum_forras_sablon.md`-t is módosítja (v2.3–v2.4, a Kivonat határ-eleme), és az `adat/SEMA.md`-be 2.60–2.63 szakaszt ír; az F224.6 és az új SEMA-szakaszok (F224.5, F224.11) a #729 merge-e után, behozott main-nel készülnek, a szakaszszám a merge-kori következő szabad szám.
- **205** — a `MUNKAMENET.md` C) szakaszát és a 2_ sablon 4/b. pontját írjuk; az F205 hátralévő M3/M5 lépése a saját `kovetkezo` mezője szerint az ir-bővítés előtt main-t hoz be és `fuggesek`-et futtat, így az F224 utáni állapotra épül.
- **217** — a #725 a `kiadas.md`-hez nem nyúl; a mi változásunk a 3. lépésé, az F217-é (ha lesz) a 6. lépésé.
- **221** — a #733 mergelve; a brief állapota még `fut` (ez okozza a `KOR 218 221 224` jelentést).
- **74, 123** — nem indult / megállt; a 2_ és 9_ sablon közös, a sorrend: az F224 előbb.
- **70, 212** — csak olvasott fájl (`motivumok/ISTENTISZT-001.md`, `adat/jeloltek.tsv`); a próba rögzített commitokon fut.

## 1. Cél

A lexikoncikk ellenőrző fele úgy épül át, hogy **minden állítást az a szereplő nézzen át, aki a legjobban el tudja dönteni**, és a hiba a próza előtt derüljön ki. A menet: igeszakasz-blokkok (A) → bizonyítéklap (B) → érvvázlat és érvnapló (C) → bíráló (D) → határ → próza (E) → gépi kapuk (F1) → állítás-ellenőr (F2) → lektor (F3) → olvasói átolvasás (3/b) → a felhasználó → 1 javítókör → 1. kiadás.

A mérés szerint (2026-11-15) a bíráló a HAMART 1Móz 8:21-es pontján 5/5-öt fogott (Sonnet és Fable egyaránt), az állítás-ellenőr viszont az ISTENTISZT vers- és adatállításain csak 25%-ot, mert igehelyenként ítélt, nem állításonként. Ez a brief az állításonkénti ítéletet vezeti be, és egy elfogadási próbával méri.

**Alapelvek** (a szabályszöveg helye a tételeknél, itt csak a cél):
- a mankó nem ítélet: az igeszakasz-blokk jelölt és támasz; a bizonyítéklap és a cikk csak eldöntött jelölt-sort vesz át; az F2-nél az „igeszakasz” mutató, nem bizonyíték; a bíráló a blokkot vizsgálandó állításként kapja;
- a cél a szivárgási arány (melyik lépés fogta meg a hibát), nem a lektor darabszáma;
- a szerep modellje a szerepfájl `model` mezőjében áll, cserélhető (Pro-váltás kb. 2026-11-29).

## 2. Modellkiosztás (JÓVÁHAGYVA, 2026-11-15)

| Szerep | Modell | Szerepfájl |
|---|---|---|
| író (A, C, E) és e brief végrehajtója | Opus | — |
| D · bíráló | Sonnet | új `.claude/agents/biralo.md`, `model: sonnet` |
| F2 · állítás-ellenőr | Sonnet → **Opus** (DT-F224b, 2026-11-15) | új `.claude/agents/allitas-ellenor.md`, `model: opus` (eredetileg `sonnet`) |
| határ-ellenőr | Sonnet | `.claude/agents/hatar-ellenor.md`: `fable` → `sonnet` |
| F3 · lektor | **Fable marad** | `.claude/agents/lektor.md`, a `model` mező változatlan; a Pro-váltáskor újra dönteni |
| független ellenőr | Opus | változatlan |

## 3. Hatókör

**Benne:** a 4. pont tizenhárom tétele, mindegyik a saját szabályhelyén (F184: egy szabály, egy hely; máshol csak hivatkozás).

**Nincs benne:**
- a HAMART-lap javítása (a 8:21 és a keretezés a lapon): a próza gazdájától jön, külön tételben;
- az ISTENTISZT 2. kiadás és a TEREMT-001 a teljes menettel (a bevezetés 2–3. lépése; a TEREMT csak a sikeres próba után indul);
- a két állandó lektor-szerepfájl és a véleménynaplók (jóváhagyva, külön kis SYSTEMS-PR);
- a gépi kapuk tartalma (E1–E41) és súlyossága: az F1 új összevetései ebben a briefben K-tételek és JELENTÉS-sorok; HIBA-szintre emelésük külön döntés (N-F224a, l. F224.4);
- a lapgenerátor (`eszkozok/lexikon_general.py`, `eszkozok/lapgen/`) és a `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` (F218 írja).

**Hatókör-szűkítés (`BRIEF_SABLON.md`, DT-F221a).** Az F224.3 két ponton szűkíti a lektor hatókörét, a 10_ sablon (F224.9) egy ponton az íróét:
1. *A lektor nem olvassa újra az F2 „igazolt” tételeit.* (a) Ellenőrzés nélkül marad: az F2 téves „igazolt” ítélete. (b) Méri helyette: vak minta az F2 igazolt tételeiből (10%, legalább 5 tétel), a lektor olvassa; ha hibát talál, a „lektor nem olvassa újra” szabály az adott lapon felfüggesztve, és a teljes igazolt halmaz a lektorhoz kerül; a szivárgás a mérőtáblában (F224.11).
2. *A négy érvelési kérdés (az 1. változat 32. tételének c) pontja: érvek egyensúlya, valódi ereje, hiányzó érv, szintkeverés) a lektortól a bírálóhoz kerül.* (a) Ellenőrzés nélkül marad: az a gyengeség, amely a próza írásakor keletkezik, az érvvázlatban még nem állt. (b) Méri helyette: a lektor új kérdése, „a próza az érvnapló szerint íródott-e”; a bíráló elutasított tételei a lektorhoz is eljutnak.
3. *A ⚑ tételeket nem az író nézi át, hanem az F2.* (a) Ellenőrzés nélkül marad: semmi új — az író átnézése önellenőrzés volt. (b) Méri helyette: az F2 minden K-tételt állításonként ítél; a „vitatott” és „nem eldönthető” a lektorhoz megy.

## 4. Tételek

Minden tétel saját commit (`F224.<n>: …`), a jelentés `naplok/F224_jelentes.md`. A szabály szövege csak a megnevezett szabályhelyre kerül.

### F224.1 — Az állítás-ellenőr szerepfájlja
**Szabályhely:** új `.claude/agents/allitas-ellenor.md` (`model: sonnet`; 0. lépés: modell-ellenőrzés a `lektor.md` mintájára; írási jog nincs, a kimenetet a hívó menti).
**Mi kerül bele** (a terv 3. szakasza):
- bemenet: a teljes kézi lista állításonként (egy K-tétel = egy állítás, a benne idézett igehelyekkel; a ⚑ csak sorrend), a forrás, a motívum adatsorai, a `konkordancia/`, a lekérdező;
- hét kötelező kérdés minden állításnál: **Ki?** (beszélő, cselekvő, megszólított); **Mit?** (tárgy, szó, héber/görög szó); **Milyen sorrendben, szerkezetben?** (szerkezeti szabály minden felsorolt helyen); **Hány?** (darabszám a felsorolással és a táblával); **Mekkora a kvantor?** („először”, „mindig”, „mind”, „csak”); **Egy versből a csoportra?**; **A lap másik helye** ugyanerről mást mond? — mindegyik a mérés egy példájával (ISTENTISZT K50, Zsolt 116, K25, Jézus Krisztus neve; HAMART erec/adámá, K39, K47);
- ítélet az **állítmányra**: igazolt / hamis / vitatott / nem eldönthető; ha bármelyik kérdésre „nem”, az ítélet nem lehet „igazolt”; bizonyítéktípus: versszöveg / adatsor / lekérdezés / szótár; az igehelysor a bizonyítékoszlopba kerül; az „igeszakasz” mutató, nem bizonyíték;
- kétirányú tilalom: emlékezetből sem igazol, sem cáfol;
- kimenet: `naplok/ALLITAS_<ID>_itelet.md`, állításonként egy sor; összesítés; a „nem eldönthető” arány.
**Kész:** a fájl a fenti elemekkel; a `model: sonnet`; a hívás helye az F224.8-ban hivatkozva; `python eszkozok/feladatok.py ellenoriz` 0 hiba.

### F224.2 — A bíráló szerepfájlja
**Szabályhely:** új `.claude/agents/biralo.md` (`model: sonnet`; 0. lépés: modell-ellenőrzés).
**Mi kerül bele** (a terv 4. szakasza):
- bemenet: az érvvázlat minden vitatott pontja, a bizonyítéklap, a tanulmány blokkjai vizsgálandó állításként, a lap Kivonat-, Remez-, Sod- és Módszertan-mondatai, amelyek ugyanarra a pontra támaszkodnak;
- kérdések, súllyal: érvek egyensúlya (melyik vett hallgatásból); az érv valódi ereje (ugyanaz a jelenség másutt; példa: a qalal és az árar együtt az 1Móz 12:3-ban); hiányzó szövegbeli érv (példa: a „-ért” ismétlése a 8:21-en); szintkeverés (szövegtanú vagy recepció, megnevezve); **a lap két helyének ellentmondása** („nem dönti el”, de a Kivonat dönt); a szakirodalom-állítás hatóköre; a szerkezet jelölése („keret”, „khiazmus” mindig értelmezés; az [adat] csak a szóismétlés ténye);
- korlát: legfeljebb 10 lekérdezés, naplózva; fölötte „nem eldönthető”; a gyanú „lekérdezendő” jelöléssel; határról nem ítél;
- kimenet: `naplok/BIRALAT_<ID>.md`; az elutasított tételek a lektorhoz és a felhasználóhoz is eljutnak.
**Kész:** a fájl a fenti elemekkel; a `model: sonnet`; a hívás helye az F224.8-ban hivatkozva.

### F224.3 — A lektor szűkítése
**Szabályhely:** `.claude/agents/lektor.md` (a szerep és a kérdések); `.claude/commands/kiadas.md` 3. lépés (mit kap a lektor).
**Mi kerül bele:**
- a lektor bemenete: a jelölt helyek, az F2 maradéka („vitatott”, „nem eldönthető”), a bíráló elutasított tételei, **vak minta az F2 igazolt tételeiből** (10%, legalább 5 tétel; a minta kiválasztása a hívó dolga, a lektor nem tudja, melyik tétel melyik halmazból jön);
- egy új kérdés: a próza az érvnapló szerint íródott-e;
- a négy érvelési kérdés a bírálóé (az 1. változat 32/c pontjának módosítása); a lektor négy mai kérdése (adat-ellentmondás, érthetőség, belső szakszó, alátámasztatlan állítás) marad;
- a vak minta lelete szerinti felfüggesztés (3. pont, 1. szűkítés);
- a `model: fable` **változatlan**.
**Kész:** a két fájl a fenti elemekkel; a hatókör-szűkítés (a)/(b) mondatai a `kiadas.md` 3. lépésében hivatkozással (a szabály szövege a `BRIEF_SABLON.md`-ben marad).

### F224.4 — A kinyerés bővítése
**Szabályhely:** `eszkozok/proza_allitas.py`, teszt: `eszkozok/teszt_proza_allitas.py`.
**Mi kerül bele:**
- új K-tétel-fajták: (a) **szám + kapcsolat/erősség** állítás („három kapcsolat erős”, „hét helyből öt”), a kapcsolattábla soraival; (b) **belső utalás** („a vitatott pontok tárgyalja”, „l. 10. szakasz”) a célpont létezésének gépi jelzésével; (c) **„nem dönti el”** típusú mondat, a lap ugyanarra a pontra támaszkodó más mondataival együtt;
- a kimenet állításonként: egy K-tétel = egy állítás, a benne idézett igehelyekkel (az F224.1 bemenete);
- ahol a gép eldönti (a belső utalás célja nem létezik; a szám nem egyezik a táblával), ELTÉR-jellegű JELENTÉS-sor a motívumra; a CI E41 HIBA-szintje és hatóköre **nem változik**. A HIBA-szintre emelés javaslata új nyitott tétel: N-F224a (`nyitott/uj/<ágnév>.md`).
**Kész:** a teszt mindhárom új fajtára pozitív és negatív esettel zöld; az ISTENTISZT-en (`b2aea73f` forrás) a mérés három „nincs a kézi listán” tétele (4, 9, 11) közül legalább a 4. és a 9. K-tétellé válik (a 11. „jelentés a névből” értelmezés, nem elvárt); a meglévő tesztek és a `--kapu` kimenete a main-hez képest változatlan a régi K-tételeken; a futtatás előtti és utáni K-tétel-szám a jelentésben.

### F224.5 — A bizonyítéklap
**Szabályhely:** új `eszkozok/bizonyiteklap.py` (+ `eszkozok/teszt_bizonyiteklap.py`); a kimenet formája az `adat/SEMA.md`-ben (új 2.x szakasz, a merge-kori következő szabad számmal).
**Mi kerül bele:**
- bemenet: a motívum kulcsversei, a lánc szavai (Strong);
- kimenet: versenként az együttállások és jelöltek, gyakorisági alapvonallal (véletlen-alapvonal), **ítélet nélkül**; a „fordított sorrendű ismétlés” gépi jelölt csak versen belül, alapvonallal; láncon átívelő „keret” jelölt nincs;
- a tanulmány adatát nem ismétli, hivatkozik rá; minden sor proveniencia-sorral (`scope=… | forras=… | ts=…`);
- a cikk és a bizonyítéklap csak eldöntött (`jeloltek.tsv`-n átment) jelölt-sort vesz át.
**Kész:** a HAMART 8:21-re a kimenet tartalmazza a mérés bizonyítéklapjának (`biralo_bizonyitek.md`) adatait; teszt zöld (alapvonal, versen belüli korlát, ítélet-mező hiánya); SEMA-szakasz.

### F224.6 — Az érvnapló
**Szabályhely:** `sablonok/9_PaRDeS_motivum_forras_sablon.md` (új szakasz; a #729 merge-e után, l. a `fugg` indokát).
**Mi kerül bele:** állítás · érvtípus (szövegtanú / hiány / recepció) · bizonyíték vagy „lekérdezendő” · döntés; a vitás pont **egy helyen**, az érvnaplóban (a vita máshol nem él, csak hivatkozik); a bíráló kérdéseire adott válasz helye.
**Kész:** a szakasz a sablonban; a 10_ sablon és a `MUNKAMENET.md` csak hivatkozik rá.

### F224.7 — A tanulmány blokkjai
**Szabályhely:** `sablonok/2_PaRDeS_bovitett_sablon.md` (a 4/b. pont, F205/DT803).
**Mi kerül bele** (az F205 állapotához igazítva, a meglévő hat blokkot nem írja újra): a szakaszhatár a blokkok előtt, **független indokkal** kijelölve; a vita-blokkban név csak forrással; „pótolt blokk, nem vak olvasás” jelölés a meglévő tanulmányokba utólag pótolt blokkra; a funkció-blokk a **szakaszbeli** szerepet adja (F224.10).
**Kész:** a három kiegészítés a 4/b. pontban; az F205 kinyerője (`eszkozok/tanulmany_kinyer.py`) a „pótolt” jelölést olvasni tudja, vagy a jelentés megmondja, miért nem kell.

### F224.8 — A menet
**Szabályhely:** `MUNKAMENET.md` C) szakasz.
**Mi kerül bele:** a lépéssor (A igeszakasz-blokkok → B bizonyítéklap → C érvvázlat/érvnapló → D bíráló → határ → E próza → F1 gépi kapuk → F2 állítás-ellenőr → F3 lektor → 3/b → a felhasználó → 1 javítókör → 1. kiadás), mindegyik lépés a szabályhelyére mutató hivatkozással, **a szabály szövege nélkül**; a mai C-a sor átírása (a „kézi listát olcsó modell vagy ember nézi” helyett az F2-szerep); a C-h sorban a `hatar-ellenor` modellje Sonnet.
**Kész:** a C) táblában minden új lépés egy sor, hivatkozással; a hivatkozás-ellenőrzés (E27) zöld.

### F224.9 — A ⚑-szabály ellentmondása
**Szabályhely:** `sablonok/10_PaRDeS_U3_proza_prompt_sablon.md`, „⚑ tétel a kézi listán” bekezdés (ma: „Mindet magad nézed át”; a terv a 6_ vagy 9_ sablont nevezte, de a szabály a 10_-ben áll).
**Mi kerül bele:** az „író nézi át” kikerül; hivatkozás az F2-szerepre (`.claude/agents/allitas-ellenor.md`) és a `MUNKAMENET.md` C-a sorára. Ezzel megszűnik a sablon és a munkamenet ellentmondása.
**Kész:** a 10_ sablonban nincs önátnézési szabály; a hatókör-szűkítés 3. pontja a jelentésben.

### F224.10 — A funkció két mezője (döntés)
**Szabályhely:** `dontesek/uj/<ágnév>.md` (DT-F224a, helyőrzővel).
**Mi kerül bele:** a DT803 módosítása: a funkció két mezőre bomlik — **szakaszbeli szerep** (a tanulmány funkció-blokkjából) és **láncbeli szerep** (a cikkben, az érvnapló döntése szerint); a szakaszon belüli szerkezet gazdája az igeszakasz-tanulmány rétegrendje, a motívumlapon nincs saját helye (legfeljebb a 10. Értelmezés rendes mondataként, címke nélkül). Forrás: a jóváhagyott terv 5. szakasza (a 3. döntés módosítva).
**Kész:** a DT-F sor 🟢 állapotban, a jóváhagyás idézetével. ⛔ **Ha a megfogalmazás a terv 5. szakaszán túlmegy** (pl. új mező a sémában, a lapgenerátort érintő változás), a sor 🟡, és a felhasználó dönt.

### F224.11 — A mérőtábla
**Szabályhely:** `adat/SEMA.md` (a `naplok/SZIVARGAS_<ID>.tsv` formája, új 2.x szakasz); a küszöbök a `MUNKAMENET.md` C) szakaszában hivatkozással.
**Mi kerül bele:** egyetlen mérőtábla motívumonként; minden pontossági hiba egy sor; oszlopok: hely · mechanizmus (`naplok/HIBA_MECHANIZMUSOK.md` kód) · hol fogták meg (F1 / F2 / D / határ / F3 / 3/b / felhasználó / kiadás után) · súly · generált blokk-e. Küszöbök: a felhasználóig jutó pontossági hiba legfeljebb az összes 10%-a, súlyos 0; F2 „nem eldönthető” legfeljebb 15%; vak minta 10%, legalább 5 tétel. Költség: lépésenként a heti keret %-a, a mérési napló szerint.
**Kész:** a SEMA-szakasz; a HAMART és az ISTENTISZT mérőtáblája a próba (F224.13) eredményéből kitöltve.

### F224.12 — A határ-ellenőr modellje
**Szabályhely:** `.claude/agents/hatar-ellenor.md`.
**Mi kerül bele:** `model: fable` → `sonnet`, a 0. lépés modellneve ennek megfelelően; a bemenet bővítése: a negatív próbák a határeseteken, a kritérium változatával (a terv 2. szakasza, „Határ” sor). A `lektor.md` modellje változatlan.
**Kész:** a fájl `model: sonnet`; a szöveg sehol nem hivatkozik Fable-ra mint a határ-ellenőr modelljére (`grep`).

### F224.13 — Elfogadási próba (utolsó tétel)
**Szabályhely:** `naplok/F224_proba.md`; az ügynökök nyers kimenete `naplok/F224_proba/`.
**Mi kerül bele:** visszajátszás az új szerepekkel (F224.1, F224.2; a 2. pont kiosztásával), vakon (az ügynökök nem látják a lektori listákat, a naplókat, a javítás utáni git-történetet), a javítás előtti állapoton:

| Halmaz | Bemenet | Mérő | Küszöb (JÓVÁHAGYVA) | Alapvonal (2026-11-15) |
|---|---|---|---|---|
| HAMART, a lektor 18 kézi listás tétele (a 34 pontossági tételből) | `motivumok/HAMART-001.md` és az új kinyerés a `f6da955e`-n | F2 | **legalább 80%** | 56% (részlegessel 67%) |
| ISTENTISZT, a lektor 10 vers- és adatállítás-tétele (1, 2, 5, 8, 10, 12, 13, 15, 16, 17) | `motivumok/ISTENTISZT-001.md` és az új kinyerés a `b2aea73f`-en | F2 | **legalább 80%** | 25% |
| ISTENTISZT, a 6 bíráló-típusú tétel (3, 6, 7, 9, 14, 18) | érvvázlat a javítás előtti forrás vitatott pontjaiból (az író, Opus) + bizonyítéklap (F224.5) | D | **legalább 4/6** | nem mérve |
| HAMART 8:21, öt ismert pont | a mérés érvvázlata + az F224.5 bizonyítéklapja | D | 5/5 (regresszió-őr) | Sonnet 5/5 |
| az F2 többlet-jelzései | vak minta, legalább 10 tétel | — | a hamis riasztás **legfeljebb 30%** | nem mérve |

- Az ismert hibahalmaz forrása: `naplok/KIADAS_HAMART-001_lektor.md`; az ISTENTISZT-é a Fable-lektor 18 tétele (`2ae45dae`); a 8:21-é a mérés mellékletei (a végrehajtó a jegyzetmappából a `naplok/F224_proba/` alá másolja, proveniencia-sorral).
- A többlet-jelzések minősítése (valódi hiba / hamis riasztás) versszöveggel vagy adatsorral, forrás szerint; ami így nem dönthető el, külön számlálva, nem hamis riasztás. A minősítést a felhasználó a jelentésben látja.
- A számolás: „megfogta” = az ítélet nem „igazolt”, és az indok a lektori tétel hibáját nevezi meg; „részben” külön oszlop, a küszöbbe nem számít.
- A 3/b (a generált blokkok) és a lektor (F3) nem része a próbának: a mérőtábla (F224.11) ezeket „nem mérve” jelöléssel viszi.
- Költség: lépésenként a heti keret %-a és a token, a jelentésben.

⛔ **A próba előtt:** keret-ellenőrzés (`get_usage`). A becslés a 2026-11-15-i mérésből: kb. 1 millió token Sonneten, kb. 1–2 százalékpont a heti keretből (×1,7 biztonsági szorzóval számolva). Ha az 5 órás vagy a heti keret nem fedi, megállás, a felhasználó dönt az időpontról.

**Ha a próba a küszöb alatt marad:** a hiányt okozó szerepfájl (F224.1 vagy F224.2) **egy** javítókört kap a hiba mechanizmusa szerint (a terv 10. szakasza, jóváhagyva), majd a próba az adott halmazon megismétlődik. ⛔ **Ha az ismétlés is a küszöb alatt marad**, megállás: a jelentés halmazonként adja az eredményt, a meg nem fogott tételek mechanizmusát és egy javaslatot; a felhasználó dönt (küszöb, szerep, modell). A TEREMT-001 a teljes menettel addig nem indul.

**Kész:** a `naplok/F224_proba.md` halmazonként a táblázat mérőszámait, a meg nem fogott tételek listáját mechanizmussal, a költséget és a mérőtáblák (F224.11) kitöltött sorait tartalmazza; mind az öt küszöb teljesül, vagy a ⛔ a felhasználónál van.

## 5. Elfogadási feltételek

- mind a 13 tétel a saját szabályhelyén; a szabály szövege máshol csak hivatkozásként áll (F184);
- `python eszkozok/feladatok.py ellenoriz` 0 hiba; a hivatkozás-ellenőrzés (E27) zöld; `python eszkozok/push_elott.py` zöld;
- `eszkozok/teszt_proza_allitas.py` és `eszkozok/teszt_bizonyiteklap.py` zöld; a `proza_allitas.py --kapu` kimenete a régi K-tételeken változatlan;
- az elfogadási próba (F224.13) öt küszöbe teljesül, vagy a ⛔ a felhasználónál van;
- a független ellenőr (`fuggetlen-ellenor`) jelentése a `naplok/F224_jelentes.md`-ben.

## 6. Döntésnapló

- DT-F224a — a funkció két mezője (a DT803 módosítása), F224.10.
- N-F224a — az F1 új összevetéseinek HIBA-szintre emelése (javaslat, F224.4).
- A jóváhagyások (2026-11-15): a konszenzusos terv a hat döntéssel; a 3. változat modellkiosztása; a küszöbök (F2 legalább 80% a vers- és adatállításokon, bíráló legalább 4/6, hamis riasztás legfeljebb 30%).
