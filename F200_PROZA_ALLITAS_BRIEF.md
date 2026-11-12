---
feladat: 200
cim: Próza-állítás ellenőrző — a versre hivatkozó állítások a vers szövege és az adat mellett, a lektor előtt
kod: PROZA_ALLITAS
tipus: feladat
fazis: folyamat
modell: opus
allapot: lezarva
lezarva_osszegzes: a próza versállítás-ellenőrzője (eszkozok/proza_allitas.py), a MUNKAMENET C-a lépése és a 10. sablon; a független ellenőrzés és a javítókör kész
ag: claude/f200-versallitas-e49cf6
pr: 697
ad: gépi ellenőrző a kézi forrás értelmező prózájához — szójelenlét, szópár és alanya, fordulat, idézet, szám gépi ítélettel, a többi ellenőrzési listán (Károli + héber/görög sor), JELENTÉS szinten; a MUNKAMENET C-szakaszában és a 10-es sablonban új lépés az U3 után, a lektor előtt
kovetkezo: "lezárva; a PR #697 a main-en (2026-11-11)"
munka: folyamat
olvas: [motivumok/HAMART-001.md, adat/elofordulasok.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_1908.tsv, eszkozok/olvasoi_kapu.py, eszkozok/lekerdez.py, eszkozok/heber_kiejtes.py, eszkozok/ellenorzes/szabalyok.py, MUNKAMENET.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md]
ir: [eszkozok/proza_allitas.py, eszkozok/teszt_proza_allitas.py, naplok/ALLITAS_HAMART-001.md, naplok/F200_jelentes.md, naplok/ELLENOR_F200.md, MUNKAMENET.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, .github/workflows/ellenorzes.yml, dontesek/uj/f200-versallitas-e49cf6.md, nyitott/uj/f200-versallitas-e49cf6.md, F200_PROZA_ALLITAS_BRIEF.md]
fugg: []
nem_fugg: [38, 104, 121, 123, 138, 178, 181, 188]
---

# F200_PROZA_ALLITAS_BRIEF.md — Próza-állítás ellenőrző

*FELADATOK #200 · Modell: opus · v1 · 2026.11.11*

**Jóváhagyás (a felhasználó, 2026-11-11, szó szerint).** A kérdés: „nem tudjuk ezeket a hibákat elkerülni?” A javaslat: „Állítás-ellenőrzés közvetlenül a prózaírás után, még a lektor előtt …” A jóváhagyás: „csináljuk meg a generátor hibákat”.

**Indok.** A HAMART-001 lektora 46 tételt adott (`naplok/KIADAS_HAMART-001_lektor.md`, #696); ebből 34 pontossági (a „Mi a gond” sor az 1. vagy a 4. kérdést nevezi): versre vonatkozó állítás, amely nem egyezik a vers szövegével vagy az adattal (Ez 7:23: a város telik meg erőszakkal, nem a föld; az 1Kir 13:34-ben és a 2Kir 17:23-ban ott áll az adámá, holott a próza „a föld szava nélkül” mondja). Ezek a hibák a lektornál derültek ki, a javítókörre maradtak. Az ISTENTISZT-001 új cikkének prózaírása előtt kell az eszköz, hogy a versállítás-hibák a prózaíró saját menetében derüljenek ki.

**Hatókör.** Nem nyúl: `lexikon/`, `eszkozok/lexikon_general.py`, `motivumok/HAMART-001.md` (a HAMART javítóköre dolgozik rajtuk; az eszköz a forrást csak olvassa), `adat/` (a SEMA 3.11 generált kapulistáját sem).

## Teendő

1. **Kinyerés.** A `motivumok/<ID>.md` értelmező rései (`RÉS-KEZDET` … `RÉS-VÉGE`, mondatonként) és az `adat/elofordulasok.tsv` motívumsorainak `kapcsolodas` prózája (soronként; a 2.1 „Az igehelyek szövege” prózája ebből generálódik, a lektor 9–14. tétele ott áll). Igehely-felismerés a `Konyv_normalizalo_tabla.tsv` könyvalakjaival, felsorolással („Ez 7:23, 8:17, 12:19”), könyvváltással és tartománnyal.
2. **A motívum szókészlete a forrásból és az adatból:** a lánc szavai a forrás „a föld (adámá)” megnevezéseiből és a `#### H0127 — … (adámá)` fejlécekből (az átírás feloldása a motívum verseinek TAHOT-szavain, a `heber_kiejtes.kiejt` kiejtésével), a görög szavak a motívum G-számaiból; a szópárok a forrás „szópárja (…; …)” felsorolásából és a `gerinc_elem` „málé+chámász” értékeiből.
3. **Gépi próbák** (ítélet: egyezik / ELTÉR):
   - **szójelenlét:** „a X szava nélkül”, „más (héber) szóval”, „a X szava … áll” → a vers TAHOT/TAGNT Strong-sorai;
   - **szópár és alanya:** mindkét szó a versben; ha a próza a szópár mellett lánc-szót nevez meg („a föld megtelt erőszakkal”), az a héber szórendben a szópár mellett áll-e;
   - **fordulat:** a kétszavas idézett fordulat („föld színéről”) szavai szomszédosak-e a héber szórendben;
   - **idézet:** a Károli 1908 szövege, az E34-gyel azonos egyeztetéssel és jelöléssel (saját fordítás, glossza);
   - **szám:** a lap/motívum egészére szóló szám az `elofordulasok.tsv`-hez; a fejléc Strong-számának versszáma a TAHOT/TAGNT-hez.
4. **Ellenőrzési lista (kézi):** egységenként az állítás, versenként a Károli-vers és a héber/görög sor (kiejtés, Strong, jelentés), a gépi jelzésekkel (⚑: a magyar szó a versben más héber/görög szót fordít, mint a lánc szava; a lánc szava nincs a versben; kizárólagos állítás). A listát olcsó modell (Sonnet) vagy ember nézi át; az eszköz modellt nem hív.
5. **Kimenet:** `naplok/ALLITAS_<ID>.md` (állítás | vers | gépi ítélet | bizonyíték); `--lektor <fájl>`: összevetés egy lektori listával, a jelentés első sora.
6. **Próba** a HAMART-001 mai (main) forrásán, összevetve a lektor 34 pontossági tételével: `naplok/F200_jelentes.md`.
7. **Beépítés:** a `MUNKAMENET.md` C-szakaszában új sor (C-a) a C-w után, a C-g és a lektor (C-k) előtt; a 10-es sablonban az önellenőrzés után új lépés. Kapu-szint: JELENTÉS.
8. **Tesztek** (`eszkozok/teszt_proza_allitas.py`) a CI „Szabaly-tesztek” lépésében.

## Garanciák és döntési napló

- G1: a diff csak a fenti `ir` fájlokat érinti.
- G2: a kilépőkód JELENTÉS szinten 0; a `--szigoru` 1-et ad ELTÉR-sornál.
- G3: a TSV-olvasás `split('\t')`; UTF-8 wrapper az importblokk után.
- G4: a Károli-párosítás (`adat/karoli_strong/`, modell-kimenet, javaslat) csak jelzésre és a magyar szó → Strong-szám feloldására szolgál; a gépi ítélet a TAHOT/TAGNT Strong-során, a Károli-szövegen vagy az adaton áll (DT786).
- D1 (DT784): a forrás a rések mellett a `kapcsolodas` próza is.
- D2 (DT785): JELENTÉS szint, E-szám nélkül; a CI csak a teszteket futtatja.
- D3 (DT786): a párosítás szerepe (G4).
- D4 (DT787): a szám gépi ítélete csak a lap/motívum egészére szóló számra.
- ⛔ A merge a felhasználóé (az orkesztrátor végzi a kérésére).
