---
feladat: 178
cim: A lexikon ág lezárása — lapszerkezeti generátor-kör, sablonok, MUNKAMENET és HAMART-arany kapuk
kod: LEXIKON_AG_LEZARAS
tipus: feladat
fazis: folyamat
modell: opus
allapot: nem_indult
ad: egy generátor-körben minden lexikonlap az új lapszerkezettel (Döntési út, olvasható döntések, folyamatos számozás 1–12, áttekintő szótári tábla a 4. szakasz elején, visszhang-blokk, szerkesztői döntés, tanítói rész nélkül), a nyílt mag olvasói átírással és [A LEXIKON CÍME] helyőrzővel; a HAMART-001 szabályai a 6-os és 9-es sablonban, új U3-prompt sablon, MUNKAMENET C-h/C-w; HIBA-szintű kapuk (határ-frissesség, HAMART-regresszió, szerkesztői szóhasználat, Nave); a felhasználó egyszeri vizuális átnézése a kör után
kovetkezo: "Te: F178.0 — modell-ellenőrzés; a #123 HAMART-001 lezárása (PR #639) és a #176 a main-ben?"
munka: folyamat
olvas: [MUNKAMENET.md, CLAUDE.md, adat/SEMA.md, adat/elofordulasok.tsv, adat/res_forras.tsv, naplok/HATAR_HAMART-001.md, lexikon/HAMART-001_TUDOMANYOS.md, motivumok/HAMART-001.md, konkordancia/BDB_rokon_irasok.tsv, konkordancia/Targum_PD.tsv, konkordancia/Vulgata_Clementina.tsv, konkordancia/SBLGNT_apparatus.tsv, konkordancia/TAGNT_valtozatok.tsv, konkordancia/VISSZHANG_README.md, F176_VISSZHANG_ADAT_BRIEF.md, F123_MIGRACIO2_BRIEF.md]
ir: [eszkozok/lexikon_general.py, eszkozok/szerep_nave.py, eszkozok/nyilt_mag_export.py, eszkozok/nyilt_mag_kapu.py, eszkozok/olvasoi_kapu.py, eszkozok/ellenoriz.py, eszkozok/muhely_allapot.py, eszkozok/teszt_olvasoi_kapu.py, eszkozok/teszt_szerep_nave.py, eszkozok/teszt_nyilt_mag.py, eszkozok/teszt_muhely_allapot.py, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/7_PaRDeS_tanitoi_kereses_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, MUNKAMENET.md, "lexikon/*.md", "nyilt_mag/*", naplok/F178_jelentes.md]
fugg: [123, 176]
nem_fugg: [125, 151]
---

# F178_LEXIKON_AG_LEZARAS_BRIEF.md — A lexikon ág lezárása

*FELADATOK #178 · Modell: opus · v1 · 2026.11.08*

*Befogadva a felhasználó jóváhagyásával (2026-11-08). Minden tétel jóváhagyott; a felhasználó szavai a tételeknél idézve. Előzmény: a HAMART-001 (#123, PR #639) határ- és prózajavítása, a lapmakett (artifact `BWNbfmsofYpnfT9v87of1G`), a #176 visszhang-adatréteg. A sorrend elve: a lapszerkezet **egy** generátor-körben változik, minden lapon, és a felhasználó **egyszer** nézi át, a kör után — a kétszeri szerkezetváltás kétszeres újragenerálás és kétszeres átnézés volna.*

## 1. Cél és határ

A lexikon ág lezárása: a HAMART-001 mint új arany szabályai rögzítve (sablon, prompt, munkamenet, gépi kapu), és minden lexikonlap egy generátor-körben az új szerkezettel újragenerálva.

**A felhasználó (2026-11-08):** „a hamart lesz az új arany / fontos hogy most már visszaesés ne legyen innen”; „Elfogadom / minden itteni javaslatod a lexikon ág lezárására / Számozzuk is át / ne legyen b/ alszekció. Folyamatos számozás”.

**Nem része:**
- a lapok **tartalmi** (határ-, próza-) javítása — az a motívum forrásában, a saját menetében történik (#123); itt csak generált nézet változik;
- a közlemény (`kozlemeny/`, data paper) szövege: kézi forrás, a következő javítókörében igazodik; itt csak a kapu méri;
- a belső adat (`DONTESEK.md`, briefek, `adat/` indoklásai): nem változik;
- a visszhang tanúrétege (sermonindex, Sefaria links): 2. fázis.

A lexikonlap generált kimenet (CLAUDE.md, DT28): minden változás a generátorban, a sablonban vagy a forrásban történik, laponkénti kézi folt nincs; a hibaosztályt CI-kapu zárja.

## 2. Tételek

### F178.0 — Modell-ellenőrzés és előfeltételek
A CLAUDE.md szerinti modell-ellenőrzés (kért: `opus`). A `fugg` feladatok: a HAMART-001 lezárása (#123, PR #639) és a #176 munkája a `main`-ben van-e. Ha nincs, ⛔ állj meg. A #639-ben elvégzett Nave- és gépi őr-munkát (8. tétel; a két gépi őr: beépített sor nem eshet a lap csoportos kizárási okába, „csak a szó miatt” indoklás HIBA) mérd fel, és csak a hiányzó részt végezd el.

### F178.1 — Határ-frissességi kapu
**A felhasználó:** „csináljuk”.
- Gépi kapu (HIBA): a lap nem adható ki, ha a `naplok/HATAR_<ID>.md` modelles része régebbi, mint az `adat/elofordulasok.tsv` motívumsorainak utolsó változása (a mérés módja — git-időbélyeg vagy a naplóba írt sorszám/ellenőrzőösszeg — a végrehajtó javaslata, a jelentésben indokolva).
- `MUNKAMENET.md` C-h: kötelező, és minden sor-változás után újrafuttatandó.
- **Ok:** a HAMART-001 határ-ellenőrzése 52 soron futott, a lezárás 60 soron, és 11 határhiba csúszott át.

### F178.2 — U2/U3 szétválasztás
**A felhasználó:** „csináljuk”.
- A határdöntés (U2) és a próza (U3) ne ugyanazé a sessioné, vagy a független határ-ellenőr az U3 előtt fusson.
- Helye: `sablonok/9_PaRDeS_motivum_forras_sablon.md` és `MUNKAMENET.md`.

### F178.3 — HAMART-001 az új arany: sablonok, U3-prompt, regressziós kapuk
**A felhasználó:** „a hamart lesz az új arany / fontos hogy most már visszaesés ne legyen innen”.
- A 9-es és a 6-os sablon frissítése a HAMART-001 szabályaival.
- Új U3-prompt sablon (`sablonok/10_PaRDeS_U3_proza_prompt_sablon.md`): nulláról, egy kézből írt teljes próza; a `MUNKAMENET.md` C-w hivatkozzon rá minden új cikknél.
- A Kivonat 1. bekezdése a lánc fordulópontját is mondja ki, nem csak a lépéseit (a fordulópont adatból igazolt legyen — a HAMART 8:21↔9:25 hamis „feszültsége” a tanulság).
- Regressziós HIBA-kapuk minden lapra: kerek 1/a + „Funkció:” sor; Károli-idézet egyezés; belső jel 0; olvasói kapu **kivételek nélkül**; a Döntési út számai összeadódnak; döntés nélküli vers 0; Nave-blokk nem üres.
- Ahol egy meglévő lap a kapun elbukik: a hiba a jelentésbe kerül (tétel a lap 2. kiadására), nem kivétel és nem kézi folt.

### F178.4 — Lapszerkezet
**A felhasználó:** „Elfogadom / minden itteni javaslatod a lexikon ág lezárására / Számozzuk is át / ne legyen b/ alszekció. Folyamatos számozás”.
- **Döntési út** blokk a makett szerint (artifact `BWNbfmsofYpnfT9v87of1G`).
- **Olvasható döntések**: a döntés indoklása olvasói mondatként a lapon.
- **Belső jel olvasói formára** — átírás, nem törlés.
- **Folyamatos számozás:** 1. Döntési út … 12. Irodalom; a szótári szerep-blokkok 4.1–4.14; „/b” alszekció nincs (az 1/b, 5/b, 6/b megszűnik).
- **A nevesített tanítói rész kivezetése:** a 6/b tanítói egyezés a lapról, a B9 a `MUNKAMENET.md`-ből, a 7-es sablon archív jelöléssel (nem törlés). A `tanitoi` rés (`adat/res_forras.tsv`, CLAUDE.md) kezelése: ⛔ a végrehajtó javaslatot tesz, a döntés a felhasználóé.
- **Az olvasói kapu kivételeinek megszüntetése.**
- **Áttekintő tábla a Szótári háttér (4. szakasz) elején** (a felhasználó jóváhagyásával, 2026-11-08, „mehet”; a javaslat: „a 4. szakasz elejére az áttekintő táblát. Szavanként egy sor: kiejtés, alapjelentés, LXX-megfelelő, a helyek száma.”): generált tábla, a motívum minden Strong-szavára egy sor. Oszlopok: szó (héber/görög + kiejtés), alapjelentés (a 4.1 szerepből), LXX-megfelelő (a 4.6 szerepből; a görög szónál a héber megfelelő), a helyek száma a motívumban. Csak megjelenítés, új adat nincs. **Nem része:** a 4. szakasz szerepenkénti rendje az md-ben marad; a szavankénti kártyás elrendezés az olvasó motívum-lapjának tétele (előnézet: artifact `TvTH6tzAK9mhYQJWasDJT8`). A felhasználó: „md-ben maradhat így — majd az olvasóban rendbe rakjuk”.

### F178.5 — Visszhang-blokk
- A lapon a #176 adatrétegéből: ókori fordítás, ÚSZ szövegváltozat, BDB rokon írások.
- A Károli-vers a nézetoldali versmegfeleltetéssel (DT630).
- A tanúréteg nélkül.

### F178.6 — „Szerkesztői döntés”
**A felhasználó:** „vegyük fel / mehet”.
- A generátor és a nyílt mag exportja (`nyilt_mag_export.py`) olvasói átírással: „a felhasználó döntése” → „szerkesztői döntés”; „az orkesztrátor döntése a felhasználó felhatalmazásával” → „szerkesztői döntés”; „a felhasználó átnézése” → „szerkesztői átnézés”; angolul „editorial decision”.
- Kapu: „felhasználó” / „orkesztrátor” a lapon, a nyílt magban és a közleményben HIBA (a közleményben a kapu jelez, a szöveg a közlemény javítókörében javul).
- A belső adat nem változik.
- Mért kiindulás (2026-11-08): nyílt mag 33, lexikon 35, közlemény 10 előfordulás.

### F178.7 — PaRDeS ki a központi keretezésből, nem kiirtva
**A felhasználó:** „akkor majd így menjen a pardes javítás a javaslatod szerint”.
- A nyílt mag címei, GENERÁLT-fejléce, a lapfej márkaneve → `[A LEXIKON CÍME]` helyőrző (munkanév: „Bibliai motívum-kereszthivatkozás lexikon” / „Biblical Motif Cross-Reference Lexicon”).
- A „PaRDeS-szint” oszlop és a tartalmi említések maradnak.

### F178.8 — Nave
**A felhasználó:** „A NAVe javítás is a javaslatod szerint”.
Ha a #639 (HAMART) nem végezte el teljesen, generátor-szinten (`szerep_nave.py`), minden Nave-lapra:
- az angol eredeti csak `title`-ben (felugró), az olvasói szövegben nem;
- a nyers karakterkód (pl. `&#8221`) feloldva;
- kapu: angol témanév és nyers `&#` az olvasói szövegben HIBA.

### F178.9 — Újragenerálás egy körben, egyszeri átnézés
- Minden lap újragenerálása egy körben, a kapuk zöldje után.
- A felhasználó vizuális átnézése **egyszer**, a kör után (`MUNKAMENET.md` C-v: a renderelt lap, nem a markdown). ⛔ Itt megállsz; a merge a felhasználóé.

## 3. Megállási pontok (⛔)
- F178.0: a függések nincsenek a `main`-ben.
- F178.4: a `tanitoi` rés sorsa.
- Bármely kapu, amelyet egy meglévő lap a mai adattal nem tud teljesíteni, és amelyhez tartalmi döntés kell (nem kivétel, hanem tétel).
- F178.9: a felhasználó átnézése.

## 4. Kimenet
- Commit tételenként (`F178.<n>: …`), UTF-8 fájlból.
- `naplok/F178_jelentes.md`: tételenként mit változtatott, a kapuk eredménye laponként, a 2. kiadásra átadott hibák.
- Draft PR a `main`-be.
