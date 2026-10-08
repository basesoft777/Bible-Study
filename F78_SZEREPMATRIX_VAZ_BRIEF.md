---
feladat: 78
cim: Szerepmátrix-váz — a lexikonoldal szótári szakasza szerepenként (ISTENTISZT-001 aranyminta, TEREMT-002 második minta)
kod: SZEREPMATRIX_VAZ
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: lezarva
ag: claude/f78-szerepmatrix-vaz
pr: 254
lezarva_osszegzes: szerepmátrix-váz (szerep-sorrendű 2. szakasz, B-jelölés, ÜRES-NYELV, 26 soros szerep-tábla), próbarender ISTENTISZT-001 + TEREMT-002; DT83 nyitva; ellenőr 2 kör: naplok/ELLENOR_F78.md
ad: a lexikonoldal-generátor a `_TUDOMANYOS` 2. szakaszát szerepenként, az adat/szotar_szerepek.tsv sorrendjében rendereli, a nem adatosított szerep explicit üres blokk (adatosítás nélkül); próbarender az ISTENTISZT-001-re és a TEREMT-002-re a generalt_proba/ alá, mérési jelentéssel — ez a #23 M1, a #10 és a #11 aranymintája
kovetkezo: DT83 (a tábla héber 1. sorának forrása) a felhasználóé; merge a felhasználótól
olvas: [adat/szotar_szerepek.tsv, adat/SEMA.md, adat/lexikon_hivatkozasok.tsv, adat/forditasok.tsv, eszkozok/lexikon_general.py, eszkozok/general.py, eszkozok/torzscikk_general.py, lexikon/ISTENTISZT-001_TUDOMANYOS.md, motivumok/TEREMT-002.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, RENDER_BRIEF.md, ADATVAGYON_TERV.md, ATALAKITASI_TERV.md.md, naplok/TEREMT002_PROZA_PROBA_meres.md, naplok/TERV_INTEGRACIO_dontesi_lista.md]
ir: [eszkozok/lexikon_general.py, eszkozok/torzscikk_general.py, eszkozok/teszt_szerepmatrix.py, generalt_proba/, naplok/F78a_valtozatok/, adat/szotar_szerepek.tsv, adat/SEMA.md, DONTESEK.md, NYITOTT_FELADATOK.md, naplok/F78_meres.md, naplok/ELLENOR_F78.md, naplok/F78_zaras.md]
fugg: []
nem_fugg: [38, 52]
---

# F78_SZEREPMATRIX_VAZ_BRIEF — Szerepmátrix-váz

*FELADATOK #78 · Modell: sonnet · v1 · 2026.10.08 · döntés: DT74 (1)–(2), DT76 (9) · forrás: `naplok/TERV_INTEGRACIO_dontesi_lista.md` 1., 2. és 9. tétel, `naplok/TEREMT002_PROZA_PROBA_meres.md` 7. szakasz*

## 1. Cél

A lexikonoldal (`lexikon/[ID]_TUDOMANYOS.md`) 2. „Szótári háttér” szakasza ma Strong-szám → forrás sorrendű (TBESG, Thayer, BDB, LSJ), a szerepmátrixtól független. A váz ezt **szerepenként, az `adat/szotar_szerepek.tsv` sorrendjében** rendereli (ADATVAGYON_TERV 18.5: „a szó-lap a mátrix renderelése; a blokkok sorrendje és töltöttsége innen jön”). Az a szerep, amelynek nincs adata (`nincs adatosítva`, `javaslat`), **explicit üres, jelölt blokk** — ez a „memória vs. lekérdezés” szabály renderbeli alakja: a hiány látszik, nem töltődik ki.

Ez a #23 M1, a #10 és a #11 aranymintája, és megtöri a #23 M1 → aranyminta → #9-adat → #9 `fugg` #23 kört: a váz szerkezet, adat nélkül; a #23 és a #9 erre függ.

## 2. Hatókör

**Benne van**
- a `lexikon_general.py` 2. szakaszát előállító logika szerep-sorrendű átépítése (a `szerepek_sorok()` a sorrend forrása);
- a 13. (Károli-megfelelők + SZPA) és 14. (rejtett/hamis párhuzam) szerep felvétele a `szotar_szerepek.tsv`-be és a `SEMA.md` 2.13-ba, `javaslat` állapottal (DT-M4, DT76 (9)). **2 szerep × 2 nyelv (`gorog`, `heber`) = 4 új sor, a tábla 22-ről 26 sorra nő** [javaslat: nyelvfüggetlen szerepek, a 12. mintájára];
- a `torzscikk_general.py` 5. szakaszának követése az új sorokhoz;
- új teszt (`eszkozok/teszt_szerepmatrix.py`): a mátrix-sorrend és az üresblokk-jelölés automatikus ellenőrzése;
- próbarender: ISTENTISZT-001 (első minta) és TEREMT-002 (második minta, szótári rész) a `generalt_proba/` alá;
- mérési jelentés: `naplok/F78_meres.md`.

**Nincs benne**
- **új szótári adat.** A `szotar_szerepek.tsv` új sorai a mátrix *metaadatát* bővítik (melyik kérdéstípushoz van forrás), nem lexikai tartalom és nem adatosítás. Az adatosítás a #9 dolga, a 13. szerepé (Károli-megfelelők) a #22-re épül;
- az éles `lexikon/` írása: befagyasztva a #11 1. lépcsőjéig (DT74 (3)); csak `generalt_proba/`. Éles fájlhoz ellenőrzött fixpont és ⛔ megállás kell;
- a TEREMT-002 lexikonoldala és `res_forras.tsv`-sorai (0 sor, #64 mérés 4.) — ez a #12b.

## 3. Lépések (⛔ a kötelező megállások)

**M0 — mérés.** A mai ISTENTISZT-001 2. szakaszát vesd össze a mátrixszal szerepenként: melyik szerep hol áll, melyik hiányzik (#64 mérés 7.: a 9., 12., 13. hiányzik; az 5. és 7. a 2/b vegyes blokkban; a 4. Strong szerinti; a héber 3.-ból csak a TWOT-szám; a 10. részleges). Állapítsd meg, hogy a `blokk_szocikkek` szerkezetét kell-e érinteni. Eredmény: `naplok/F78_meres.md` M0 szakasza, `scope=… | forras=… | ts=…` proveniencia-sorral.
⛔ **Megállás, ha a blokkok átrendezése a `blokk_szocikkek` belső szerkezetét érinti.** A végrehajtó a *szűkített hatókört* javasolja (csak a 2. szakasz szerep-fejléc-sorrendje és az üres blokkok; a forrásonkénti belső render változatlan), és a felhasználó dönt. A #36 (`lexikon_general.py`-ra épül) emiatt nem áll le; a napló jelzi a #36 felé, külön egyeztetés nincs.

**M1 — mátrix-bővítés.** 13. és 14. szerep `javaslat` állapottal a `szotar_szerepek.tsv`-be és a SEMA 2.13-ba (a „22 sor” szöveg frissül); `torzscikk_general.py` 5. szakasza követi. Táblát író lépés előtt a sorokat vesd össze az eredetivel, eltérésnél állj meg; **`csv` modul tilos** (`split('\t')` / `'\t'.join()`).

**M2 — váz-render.** A szerep-sorrendű render és az üres blokk.
⛔ **DT80 (üres blokk jelölése): a végrehajtó nem dönt.** 2–3 jelölés-változatot hoz, **mindet ugyanazon az ISTENTISZT-001 szakaszon kirenderelve, egymás mellett** (ideiglenes könyvtárban, a repón kívül), nem egyetlen javaslatot. A felhasználó választ; a döntés `DT80` helyőrzővel a `DONTESEK.md`-be kerül.

**M3 — próbarender és mérés.** ISTENTISZT-001, majd TEREMT-002 a `generalt_proba/` alá (`--kimenet`). `naplok/F78_meres.md`: szerepenként töltöttség és üres blokk, a #64 7. szakaszának korlátjára hivatkozva.

**M4 — zárás.** Független ellenőr (`naplok/ELLENOR_F78.md`), `naplok/F78_zaras.md`, PR. Merge csak a felhasználótól.

## 4. Elfogadási feltételek

1. A 2. szakasz minden szerepe megjelenik, a `szotar_szerepek.tsv` sorrendjében; a nem adatosított szerep a jóváhagyott jelöléssel üres blokk.
2. A `szotar_szerepek.tsv` 26 soros, a 13–14. szerep `javaslat`; a SEMA 2.13 egyezik vele.
3. `eszkozok/teszt_szerepmatrix.py` zöld; `python eszkozok/feladatok.py ellenoriz` 0 hiba.
4. A próbarender csak `generalt_proba/`-ba ír; az éles `lexikon/` változatlan (`git diff` igazolja).
5. Kitöltetlen szerep sehol nincs gyenge vagy asszociatív anyaggal pótolva (3. szabály).
6. Független ellenőr jelentése eltérés nélkül.

## 5. Döntésnapló

- DT74 (1)–(2): a váz külön feladat, a TEREMT-002 a második minta — **rögzített**.
- DT76 (9): 13–14. szerep `javaslat` állapottal, a #78 menetében — **rögzített**.
- `DT80`: az üres blokk jelölése — **eldöntve** (B változat: gépi `<!-- ÜRES-BLOKK: szerep | állapot -->` + látható sor; csak `nincs adatosítva` / `javaslat` szerepnél).
- `DT81`: hatókör — **eldöntve** (szűkített S1–S5; a TWOT/domén/kiejtés a saját szerepe alá költözik).
- `DT82`: az ellenőr három tartalmi eltérése — **eldöntve** (harmadik állapot „adatosítva, nincs bekötve”; `ÜRES-NYELV` jelölő; a 7. szerep „l. 2/b”). A két héber TBESH-sor bekötése a #78-ban **NEM történt meg**: a felhasználó (2026-10-08, chat) a „negyedik utat” választotta (a DT-F42a érvényben marad; a héber 1. szerep a meglévő BDB-sorokra hivatkozik), l. `naplok/F78_meres.md` 12–13.
- `DT83`: a `szotar_szerepek.tsv` héber 1. sorának forrás-oszlopa a DT-F42a után — **nyitva** (a felhasználó külön döntése).
