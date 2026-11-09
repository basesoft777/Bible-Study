---
feladat: 184
cim: Egy szabály, egy hely — a folyamat-dokumentumok egyszerűsítése
kod: DOKU_EGY_FORRAS
tipus: feladat
fazis: folyamat
modell: opus
allapot: fut
ag: claude/doku-egy-forras
ad: a többszörösen leírt folyamat-szabályok egy kanonikus helyen, a többi hivatkozik; a kapuk szabálylistája a kódból generált GENERÁLT blokk CI-őrrel; menet- és zárójelentés egy fájlban; hivatkozás-kapu teszttel
kovetkezo: "F184 D1–D5 fut (a D0 jóváhagyva, 2026-11-09)"
munka: folyamat
olvas: [DONTESEK.md, eszkozok/ellenorzes/]
ir: [CLAUDE.md, MUNKAMENET.md, BRIEF_SABLON.md, adat/SEMA.md, "sablonok/6_*", "sablonok/9_*", "sablonok/10_*", .claude/commands/kovetkezo.md, .claude/commands/elteres.md, eszkozok/olvasoi_kapu.py, eszkozok/ellenoriz.py, eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/tesztek/test_szabalyok.py, eszkozok/feladatok.py, eszkozok/teszt_feladatok.py, .github/workflows/ellenorzes.yml, naplok/F184_leltar_azonositok.py, naplok/F184_leltar_kifejezesek.py, dontesek/uj/doku-egy-forras.md, nyitott/uj/doku-egy-forras.md, NYITOTT_FELADATOK.md, "sablonok/1_*", "sablonok/2_*", "sablonok/4_*", "sablonok/5_*", sablonok/PaRDeS_gyorsreferencia.md, .claude/commands/lap-javit.md, .claude/commands/kiadas.md, .claude/commands/befogad.md, naplok/F184_jelentes.md]
fugg: []
---

# Brief-tervezet — Egy szabály, egy hely: a folyamat-dokumentumok egyszerűsítése (DOKU_EGY_FORRAS)

*Orkesztrátori tervezet, 2026-11-09, a felhasználó jóváhagyásával („mehet”). Befogadásra (`/befogad`, külön sessionben). A #182 (HAMART javító menet) **előtt** fut, hogy az már az egyszerűsített rendben dolgozzon.*

**Javasolt fejléc [javaslat]:** `tipus: feladat`, `fazis: folyamat`, `modell: opus`, `munka: folyamat` (motívumfájlt és prózát nem ír), `fugg: []`; `olvas`/`ir`: a befogadó vezesse le (fő fájlok: `CLAUDE.md`, `MUNKAMENET.md`, `BRIEF_SABLON.md`, `adat/SEMA.md`, `sablonok/6_*`, `sablonok/9_*`, `sablonok/10_*`, `.claude/commands/kovetkezo.md` és `elteres.md` (vagy ahol a parancsok élnek), `eszkozok/olvasoi_kapu.py`, `eszkozok/ellenoriz.py`, `eszkozok/ellenorzes/szabalyok.py`, `eszkozok/feladatok.py`, `naplok/F<nn>_jelentes.md`).

## Probléma (mért esetek, 2026-11-08–09)
Ugyanaz a szabály több dokumentumban szó szerint vagy átfogalmazva áll, és a független ellenőr szinte minden körben talál közöttük elcsúszást — a kör a dokumentumok egymás közti egyezésére megy el, nem a lapra:
- #178: a visszhang-szabály a lapon, a SEMA 2.53-ban, a 6-os sablonban, a MUNKAMENET C-vh-ban és a DT-F178g-ben; eltérés: C-vh rövidebb, V1–V6 vs. V1–V7, a DT tartalma módosult jelölés nélkül (ELLENOR_F178_2, _3);
- #166: a SEMA 2.50 címe rossz szabályt nevezett meg, a nyitott tétel a régi címet idézte (ELLENOR_F166, _2);
- feladatonként sok, kézzel karbantartott fájl: brief-fejléc, jelentés, zárójelentés, ELLENOR-fájlok, dontesek/uj, nyitott/uj.

## Cél
Egy szabály egy helyen áll; minden más hivatkozik rá. Ami gépből jön (szabály-azonosítók, kapulista), az generált. Feladatonként kevesebb kézi fájl.

## Tételek
- **D0** — modell-ellenőrzés; leltár: a szabály-szövegek, amelyek legalább két folyamat-dokumentumban állnak (gépi kereséssel: azonos szabály-azonosítók, DT-hivatkozások, kapunevek; plusz a fenti esetek), táblában: szabály → előfordulások → javasolt kanonikus hely. ⛔ a táblát az orkesztrátor hagyja jóvá.
- **D1 — kanonikus helyek rögzítése** (a CLAUDE.md „Ezt olvasd” táblájába egy sor): lapszabály → `sablonok/6_*`; forrás-/cikkszabály → `sablonok/9_*` / `10_*`; adatszabály → `adat/SEMA.md`; munkamenet-lépés → `MUNKAMENET.md` (csak a lépés és a hivatkozás, a szabály szövege nem); döntés → `DONTESEK.md` (a döntés, nem a szabály teljes szövege).
- **D2 — a másolatok cseréje hivatkozásra** a D0 táblája szerint (a tartalom nem változik; ahol a másolatok eltérnek, a kanonikus marad, az eltérés a jelentésbe — tartalmi döntés esetén ⛔).
- **D3 — generált szabálylista:** a kapuk szabály-azonosítói és rövid leírása (olvasói kapu V*, `ellenoriz.py` sorszámai, CI E*) a kódból generálódjon egy `GENERÁLT` blokkba (a sablonba vagy a SEMA-ba, egy helyre), CI-őrrel, hogy a dokumentum és a kód ne csúszhasson el.
- **D4 — kevesebb fájl feladatonként:** a menetjelentés és a zárójelentés egy fájl (`naplok/F<nn>_jelentes.md`, a végén „Zárás” szakasz); az ELLENOR-fájlok külön maradnak (az ellenőr szövege változtatás nélkül); a `/kovetkezo` 10. lépése és a BRIEF_SABLON ehhez igazítva; a régi `_zaras.md` fájlokhoz nem nyúl.
- **D5 — hivatkozás-kapu:** az E27 (vagy új szabály) azt ellenőrizze, hogy a hivatkozott szabály/szakasz létezik, nem a másolatok egyezését; teszttel.
- **D6 — jelentés, független ellenőr, draft PR.**

## Nem része
A lap tartalma; a régi briefek szövege (csak ha kanonikus szabályt másolnak és a D2 cseréli — ez is a jelentésben); a motívumfájlok.
