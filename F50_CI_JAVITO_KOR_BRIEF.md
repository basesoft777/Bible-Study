---
feladat: 50
cim: Korlátozott javító kör: push után a CI olvasása és a saját PR hibáinak javítása
kod: CI_JAVITO_KOR
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: nem_indult
ad: a /befogad és a /kovetkezo záró lépése push után elolvassa a CI-t; ha a hiba a saját PR tartalmából jön (fejléc-mező, fájlnév, formai hiba), legfeljebb két körben javítja új commitban; minden mást (CI-szabály, másik feladat, függési kör, tartalmi döntés) nem javít, hanem jelent
kovetkezo: "futtatható a #32 (KONTEXTUS) és a #45 (MODELL_ELLENORZES) lezárása és mergelése után, mert mindkettő a .claude/commands/kovetkezo.md-t írja"
olvas: [.claude/commands/befogad.md, .claude/commands/kovetkezo.md, CLAUDE.md, MUNKAMENET.md, DONTESEK.md, eszkozok/feladatok.py, .github/workflows/]
ir: [.claude/commands/befogad.md, .claude/commands/kovetkezo.md, naplok/CI_JAVITO_KOR_naplo.md]
fugg: []
helyi_gep: nem
---

# Fnn_CI_JAVITO_KOR_BRIEF.md — Korlátozott javító kör a CI hibáira

*FELADATOK #nn (a számot a `/befogad` adja) · Modell: sonnet · v1 · 2026.10.04*

## 1. Cél

A `/befogad` és a `/kovetkezo` a PR megnyitásával (push, draft PR) véget ér; a CI eredményét nem olvassa el, és piros CI-re nem reagál. Dokumentált eset: a PR #158 (F48 befogadása) `feladatkovetes` ellenőrzése megbukott, mert a `feladat:` mező üres maradt, a befogadó session pedig a logot nem nézte meg, és a hibát helytelenül függési körnek tulajdonította. A feladat: egy **szűk, korlátozott** javító kör, amely a saját PR-ból eredő formai hibát kijavítja, minden mást jelent, és sosem dönt tartalmi kérdésben.

## 2. Hatókör

**Benne van**
- a `.claude/commands/befogad.md` záró lépése és a `.claude/commands/kovetkezo.md` 10. lépése (ZÁRÁS) új alpontja: a CI elolvasása és a korlátozott javítás;
- a javítható és a nem javítható hibák osztályozása (3. szakasz);
- a javító kör naplója (`naplok/CI_JAVITO_KOR_naplo.md`).

**Nincs benne**
- CI-szabályok vagy a `.github/workflows/` módosítása (D6: a CI-szabály hibáját külön ágon javítjuk);
- a `FELADATOK.md` generált blokkja (D25);
- bármely futó vagy másik feladat brief-fejlécének módosítása (pl. `nem_fugg` felvétele az #22-be);
- automatikus ismételt futtatás, időzített vagy ciklikus CI-lekérdezés (a desktop alkalmazás saját PR-figyelőjét — `ccd_pr` — használjuk, ha kell; a parancs maga nem pollol);
- az `Auto-fix` bekötése.

## 3. Szabályok (a parancsfájlokba kerülő szöveg alapja)

**3.1 Mikor olvas.** A push és a draft PR megnyitása után, egyszer. Ha a futás még nem ért véget, a parancs ezt jelzi („a CI még fut"), nem vár ciklusban, nem pollol.

**3.2 Hogyan olvas (csak olvasás).** `gh run list --branch <ág>` és `gh run view <id> --log-failed`. Minden idézett hiba a log szó szerinti sora legyen (szabály-azonosító, fájl, üzenet), a **proveniencia** a CLAUDE.md szerint: a futás azonosítója és a commit sha.

**3.3 Mit javíthat (a saját PR tartalmából eredő formai hiba).**
- hiányzó vagy érvénytelen fejléc-mező a PR által **befogadott vagy létrehozott** briefen (pl. `feladat`, `cim`, `modell`, `allapot`);
- fájlnév–szám egyezés (`F<nn>_…`), `git mv` a saját fájlra;
- a PR által hozzáadott fájl formai hibája, amelyet a CI megnevez (kódolás, sorvég, hiányzó UTF-8 commit-üzenet);
- ha a PR a generált blokkot módosította (E18), a módosítás **visszavonása** (a generált blokkot nem szerkeszti).

**3.4 Mit NEM javít, hanem jelent.**
- CI-szabály vagy workflow hibája (D6, külön ágon);
- függési kör (`KOR`), `kizar`-ütközés, vagy bármi, ami másik feladat fejlécének/fájljának módosítását kéri (`nem_fugg`, `fugg`);
- tartalmi vagy hatókör-döntés, licenc, titok, `DONTESEK.md`-tétel;
- ha a hiba okát nem a log egyértelműen mondja ki (nincs találgatás: a log szó szerinti sora az alap).

**3.5 Korlát.** Legfeljebb **két javító kör**; minden kör új commit (nem `--amend`, nem `--force`), üzenete `<tétel>.<n>: CI-javítás — <szabály-azonosító>`, UTF-8 fájlból (CLAUDE.md). A harmadik lépésnél vagy ha a hiba nem a 3.3 listából való, a parancs megáll és jelent.

**3.6 Jelentés.** A felhasználónak adott válasz első sora: PR-link + CI-állapot (ahogy ma), majd: „javító kör: n (javítva: …; jelentve: …)”. A jelentett hibánál a log szó szerinti sora és egy mondatos javaslat; döntést a felhasználó hoz.

**3.7 A `/befogad` különlegessége.** A befogadás **csak a saját befogadott fájlokra** javíthat (a `feladat` szám beírása, `git mv` név). A „meglévő brief tartalmának módosítása” továbbra is tilos (`befogad.md` 6. pont); a befogadott brief szövege nem változik.

## 4. Lépések

0. **Leltár.** A `befogad.md` és a `kovetkezo.md` jelenlegi záró lépései, és mely CI-szabályok (E-azonosítók) adnak a PR saját fájljaira formai hibát (a `eszkozok/ellenorzes/szabalyok.py` és a `feladatok.py ellenoriz` alapján). Napló: `naplok/CI_JAVITO_KOR_naplo.md`.
1. **Szöveg.** A 3. szakasz szabályai a két parancsfájlba, rövid, a meglévő számozásba illesztve (a `kovetkezo.md` 10. lépés új alpontja, a `befogad.md` 5. lépés vége). A meglévő lépések szövege nem romlik.
2. **Próba (csak olvas).** Az #158-as eset visszajátszása: a `6962818` commit CI-logjából (run 37195412826) az új szabály a `feladat` mező hiányát 3.3 szerint javíthatónak, egy hipotetikus `KOR`-hibát 3.4 szerint nem javíthatónak minősíti. A napló tartalmazza a besorolást.
3. **⛔ A szabályszöveg jóváhagyása.** A 3.3 és 3.4 lista tartalmi: a felhasználó hagyja jóvá, mielőtt a parancsfájlokba kerül.
4. **Ellenőrzés.** `python eszkozok/feladatok.py ellenoriz` 0 hiba; a CI-ellenőrzők a változott fájlokra; a parancsfájlok más lépései változatlanok.

## 5. Elfogadási feltételek

- A két parancsfájl záró lépése tartalmazza a 3.1–3.7 szabályokat; sem ciklikus lekérdezés, sem időzítés nincs benne.
- A javítható és a nem javítható hibák listája a felhasználó által jóváhagyott.
- A próba (2. lépés) az #158-as hibát helyesen osztályozza.
- Más feladat fejléce, a CI-szabályok és a generált blokk nem változtak.

## 6. Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | Legfeljebb két javító kör, saját PR-ból eredő formai hibára | a hiba oka a PR saját tartalmában van, a javítás nem tartalmi döntés | korlátlan automata javítás |
| D2 | A függési kör és a CI-szabály nem javítható | D6, D25; más feladat sora nem módosítható | a `nem_fugg` automatikus felvétele |
| D3 | A parancs nem pollol, az Auto-fix a desktop alkalmazás dolga | a CLAUDE.md szerint a CI-figyelést a `ccd_pr` eszközök végzik | időzített CI-lekérdezés |
| D4 | A feladat a #32 és #45 után fut | mindkettő a `kovetkezo.md`-t írja; a `kizar` kölcsönös kizárás | párhuzamos futás |
