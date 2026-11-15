# F219 jelentés — gépi lezárás a merge-kor (A. rész)

*2026-11-15 · sonnet · `claude/dreamy-hugle-c875f6`*

## Hova épült
A meglévő `feladatok.yml` (feladatok-frissítés) Actionbe, egy új lépésként: a számkiosztás és az újragenerálás **után**, a `feladatok.py ellenoriz` és a FELADATOK.md-generálás **előtt**. Új workflow nincs. A commit-üzenet első sora változatlan (E30/E32); az üzenet törzse kapja a `brief-lezárás: #nn, …` sort (`gepi_commit_uzenet.py --torzs-fajl`). A lépés `continue-on-error`: hibája nem akasztja a számkiosztás-commitot.

## A lezárás pontos feltétele (mindegyik egyszerre)
1. `tipus`: feladat vagy naplózás; `allapot`: `fut` vagy `megallt`.
2. A `kovetkezo` `Te:`-vel kezdődik, megnevezi a merge-et, és nincs benne más teendő jele (`utána`/`után`, ⛔, döntés/`DT…`, `hátra`, `maradék`, `nyitva`/`nyitott`, N-tétel, `elteres_kor`, `korlát`, `újragener`, `mérés`, `Folytatás`).
3. Van `ag:` vagy `pr:`, és a main first-parent történetében van olyan PR-merge, amelynek az ágneve az `ag`, vagy száma a `pr`.
4. Az `allapot`, a `kovetkezo` és a `lezar` a merge PR-ágán (a merge második szülője) ugyanaz, mint ma a main-en: a merge óta senki nem nyúlt a menet állapotához.

Ha bármelyik nem teljesül, a gép nem nyúl a briefhez. A lezárás: `allapot: lezarva`, `kovetkezo: "lezárva: a PR #N mergelve (dátum, gépi lezárás …)"`; a `lezar:` N-tételei a `NYITOTT_FELADATOK.md`-ben az N153 mintájára: `**N<n> — LEZÁRVA (dátum, a #PR merge-ével, F<nn>) — …`. Allapotalapú és idempotens: egy elveszett futást a következő pótol.

## Átfedés az F201-gyel és az F217-tel
- **F201** (gépi commitok összevonása): már a main-en; a lépés a `feladatok.yml` meglévő egyetlen commitjába kerül, nincs új commit és új workflow. Közös fájl: `.github/workflows/feladatok.yml`, `eszkozok/gepi_commit_uzenet.py` (csak egy új, opcionális `--torzs-fajl`).
- **F217** (generált nézetek a main-en, `nem_indult`): a saját `generalt_nezetek.yml`-jét és az `ellenorzes.yml`-t tervezi; ebből ennek a PR-nak csak egy tesztsor jut az `ellenorzes.yml`-ben (`brief_lezaras.py tesztek`), a `feladatok.yml`-hez nem nyúl. Ha az F217 a `feladatok.yml` lépéseit átrendezi, ez a lépés a „szamkiosztas után, ellenoriz előtt” helyen marad.
- Az F201 brief maga is mergelt (#698), de `fut` állapotú: a száraz futás szerint ezt a gép zárná le.

## Száraz futás a mai main-en (`--szaraz`)
2 brief zárna le (F192 / PR #685, F201 / PR #698), 0 N-tétel (a `lezar:` mező ma még egy briefben sincs). Kihagyva 25 mergelt, de nem lezárt brief; az okuk: 7 a `kovetkezo` nem nevezi meg a merge-et, 5 nem `Te:`-vel kezdődik, 10 más teendőt is jelez, 2 `dontesre_var`, 1 a merge óta folytatódott. (Az F165 briefjének nincs `ag:`/`pr:` mezője, ezért a PR-ja nem azonosítható: ez a 26. kihagyott, a kapu nem látja.) Ezeket a #sav PR kötegelt takarítása kezeli; a `--kapu` ma 27 jelentést ad (a 25 + a 2 zárható).

## Mi hiányzik (B. rész, a #sav PR mergelése után)
A `feladatok.py ellenoriz` JELENTÉS-bekötése (a logika kész: `brief_lezaras.kapu_jelentesek`, `--kapu`), a `lezar` kulcs a `KULCSOK`/`LISTA_KULCSOK`-ban, a brief-sablon (`lezar:` és a kanonikus `Te: merge` alak), a `adat/SEMA.md`/sablon említés. A #sav PR a jelentés idején nincs a main-en. Amíg a `lezar` kulcsot a fejléc-elemző nem ismeri, a szkript nyersen olvassa, és az „ismeretlen kulcs” hibát nem tekinti akadálynak.

## B. rész (2026-11-15, külön PR)
Kész: a `lezar` kulcs a `feladatok.py` sémájában (azonosító-alak HIBA), az `ellenoriz` JELENTÉS-sorai (`brief_lezaras.kapu_jelentesek`; a mai main-en 22 jelentés, 0 hiba), a `BRIEF_SABLON.md` (`lezar` mező, kanonikus `Te: … merge` alak, hatókör-szűkítés DT-F221a). A `sav` mezőt az F219/F220/F221 briefben pótoltam (SYSTEMS): a #734-gyel párhuzamosan mergelődtek, és a main `ellenoriz`-e emiatt piros volt. A fenti „Mi hiányzik” szakasz ezzel teljesült.

## A `sav` értékkészlete: öt elem (DT856, a felhasználó döntése, 2026-11-15)
`SYSTEMS / CONTENT / SERVER / USER / BUSINESS` (`feladatok.py`, `BRIEF_SABLON.md`, `heti_attekinto.py` sávlistája, tesztek; a FELADATOK.md táblái a `SAVOK` sorrendjében csoportosítanak). Átsorolás (briefenként egy sor):
- `F86_ELOFIZETES_FEED_BRIEF.md`: `USER` → `BUSINESS` (előfizetési szintek, szállítás, lejárat: a #86 üzleti oldala).
- Nincs más `USER` brief; `SERVER` → `USER` átsorolandó nincs (a 25 `SERVER` brief olvasói felület, adatbázis, tervező mód, kereső: az olvasó funkciói, nem felhasználókezelés).
- Megtartva: `F156_MUHELY_FEED_STASH` (`SYSTEMS`: belső műhelyállapot, nem üzlet).
