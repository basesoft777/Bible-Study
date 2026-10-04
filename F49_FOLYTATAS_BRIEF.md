---
feladat: 49
cim: Félbemaradt feladatok folytatása: a /kovetkezo lássa a fut és megallt állapotú feladatokat
kod: FOLYTATAS
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: nem_indult
ad: a feladatok.py jeloltek a félbemaradt (fut, „Folytatás:” kezdetű kovetkezo) feladatot folytatási jelöltként adja, a felhasználóra váró (fut/megallt, „Te:”) feladatot külön sorban mutatja; a /kovetkezo 8. lépése ezt a jelölést írja, a javaslat mindkettőt kiírja
kovetkezo: "futtatható a #32 (KONTEXTUS) és a #45 (MODELL_ELLENORZES) lezárása és mergelése után, mert mindkettő a .claude/commands/kovetkezo.md-t írja"
olvas: [.claude/commands/kovetkezo.md, BRIEF_SABLON.md, MUNKAMENET.md, eszkozok/feladatok.py, eszkozok/teszt_feladatok.py, eszkozok/tesztek/test_feladatok_fugges.py, .github/workflows/]
ir: [.claude/commands/kovetkezo.md, eszkozok/feladatok.py, eszkozok/tesztek/test_feladatok_folytatas.py, BRIEF_SABLON.md, naplok/FOLYTATAS_naplo.md]
fugg: []
helyi_gep: nem
---

# Fnn_FOLYTATAS_BRIEF.md — Félbemaradt feladatok folytatása a /kovetkezo-ban

*FELADATOK #nn (a számot a `/befogad` adja) · Modell: sonnet · v1 · 2026.10.04*

## 1. Cél

A `/kovetkezo` csak `nem_indult` és `dontesre_var` állapotú feladatot választ (`eszkozok/feladatok.py`, `jeloltek()`: `if b.allapot not in ('nem_indult', 'dontesre_var')`). A parancs 8. lépése (KERETKIMERÜLÉS) viszont `fut` állapotban hagyja a félbemaradt feladatot, és azt írja: „A következő `/kovetkezo` onnan folytatja.” A kettő ellentmond egymásnak: a félbemaradt feladatot a választó `KIHAGYVA #nn állapot: fut` sorral elejti, és a javaslatban nem jelenik meg.

**Dokumentált eset (2026.10.04):** a #22 (F22, Károli–Strong) az 1–5Móz után keretkimerülés miatt állt meg, `allapot: fut`, `kovetkezo: "… Heti nullázás után: (1) 5Móz ellenőri kör …"`. A `/kovetkezo` a #43-at javasolta, a #22-t csak a kihagyottak között említette. A felhasználó megkérdezte, miért nem tudja folytatni a Károli Strong-számozását. Kézi megkerülés: a brief `megallt` állapotot és „Te: a Józs indítása” `kovetkezo`-t kapott (PR #160), de a választó ezt sem mutatja.

Másodlagos kár: a félbemaradt `fut` feladat a választó szemében FUTÓ marad, ezért a `kizar`-párjait (`×`) is visszatartja (`kizár (futó): #nn`), pedig valójában semmi nem fut.

## 2. Hatókör

**Benne van**
- a `fut` állapot két jelentésének szétválasztása a `kovetkezo` mező előtagjával (nem új állapottal, hogy a `ALLAPOTOK`, a `FELADATOK.md`-generátor és a CI ne változzon):
  - `fut` + „Folytatás:” kezdetű `kovetkezo` = félbemaradt, folytatható;
  - `fut` minden más `kovetkezo`-val = egy session ténylegesen dolgozik rajta (a mai jelentés);
- a `feladatok.py jeloltek` két új kimeneti sora:
  - `FOLYTATAS #nn <cím> — <kovetkezo>`: a félbemaradt feladat folytatási jelölt; függés- és helyigép-szűrés ugyanaz, mint a többi jelöltnél;
  - `VAR_RAD #nn <cím> — <kovetkezo>`: `fut` vagy `megallt` állapot „Te:” kezdetű `kovetkezo`-val; tájékoztató sor, nem jelölt;
- a FUTÓ-vizsgálat (kizar) a „Folytatás:” kezdetű `fut` feladatot nem tekinti futónak;
- a `.claude/commands/kovetkezo.md`:
  - 3. lépés: a FOLYTATAS jelölt elsőbbsége (l. D1);
  - 5a: a javaslat külön sorban kiírja a FOLYTATAS és a VAR_RAD feladatokat;
  - 8. lépés: keretkimerüléskor a `kovetkezo` mező „Folytatás:” kezdetű legyen;
- a `BRIEF_SABLON.md` `kovetkezo`-sora: a „Folytatás:” előtag leírása a „Te:” mellett;
- tesztek: `eszkozok/tesztek/test_feladatok_folytatas.py`;
- napló: `naplok/FOLYTATAS_naplo.md`.

**Nincs benne**
- más feladat briefjének átírása vagy migrálása (a #22 és a többi `fut`/`megallt` feladat fejléce marad; a napló csak felsorolja, melyik esne melyik új sorba);
- új `allapot` érték, a `FELADATOK.md` generált blokkja, a CI-szabályok;
- a `/befogad` parancs.

## 3. Lépések

1. **Felmérés.** A `main` minden `fut` és `megallt` állapotú briefje: szám, állapot, `kovetkezo` első 80 karaktere, és hogy az új szabály szerint FOLYTATAS, VAR_RAD vagy valódi futó lenne. Ha van ág, az utolsó commit dátuma (`git log -1 --format=%cs origin/<ag>`), tájékoztatásul. Táblázat a naplóba.
2. **`feladatok.py`.** `jeloltek()` és a parancssori kimenet bővítése (FOLYTATAS, VAR_RAD), a FUTÓ-vizsgálat szűkítése. A `csomag()` a FOLYTATAS jelöltet a többi jelölttel azonos ütközésszabállyal kezeli; `ir` nélküli (régi fejlécű) feladat továbbra is csak egyedül fut.
3. **Tesztek.** Legalább: (a) `fut` + „Folytatás:” → FOLYTATAS; (b) `fut` + más → kihagyva, futó; (c) `megallt` + „Te:” → VAR_RAD; (d) `fut` + „Te:” → VAR_RAD; (e) a „Folytatás:” kezdetű `fut` nem tart vissza `kizar`-párt; (f) függésre váró félbemaradt feladat → `vár: #nn`, nem FOLYTATAS. A meglévő tesztek változatlanul zöldek.
4. **`kovetkezo.md` és `BRIEF_SABLON.md`** szövegének módosítása a 2. szakasz szerint, a D1 döntésével (a FOLYTATAS jelölt megelőzi az új jelölteket; több FOLYTATAS között a kritikus út, majd a feladatszám dönt).
5. **Napló és zárás.** A napló végén a régi és az új `feladatok.py jeloltek` kimenete a `main`-en egymás mellett.

## 4. Elfogadási feltételek

- `python eszkozok/feladatok.py ellenoriz` 0 hibával fut; a meglévő és az új tesztek zöldek.
- A `main` mai állapotán az új `jeloltek` kimenetében a #22 VAR_RAD sorban jelenik meg („Te: a Józs indítása”), ha a PR #160 mergelve van; ha nem, valódi futóként.
- A `kovetkezo.md` 8. lépése és a `jeloltek()` ugyanazt az előtagot használja (egy konstans a `feladatok.py`-ban, a parancsfájl erre hivatkozik).
- Más feladat briefje nem változott (`git diff --stat` csak az `ir` fájljait és a saját briefet mutatja).

## 5. Döntésnapló

| # | Kérdés | Opciók | Javaslat | Állapot |
|---|---|---|---|---|
| D1 | A FOLYTATAS jelölt elsőbbsége | (a) megelőzi az új (`nem_indult`) jelölteket; (b) a feladatszám-sorrendben áll a többi között; (c) csak alternatívaként jelenik meg | (a): a megkezdett munka befejezése olcsóbb, mint új kontextus nyitása, és a félbemaradt ág elavulását is megelőzi | ✅ **(a)** — felhasználó, 2026.10.04 (chat, a brief írásakor) |
| D2 | Az előtag szövege | „Folytatás:” · „Folytat:” · más | „Folytatás:” — magyar főnév, párhuzamos a „Te:” és a „halasztva” előtaggal | ✅ **„Folytatás:”** — felhasználó, 2026.10.04 (chat, a brief írásakor) |
| D3 | Új állapot helyett előtag | új `allapot: felbe` · `kovetkezo`-előtag | előtag: az `ALLAPOTOK`, a generátor és a CI változatlan marad | javaslat (a brief rögzíti) |
