---
feladat: 206
cim: A prózaíró prompt és a motívumforrás-sablon finomítása a HAMART-001 lektori körének tapasztalatából — hibaosztályok, szabályok példapárral, gépi védelem
kod: PROZA_PROMPT
tipus: feladat
fazis: folyamat
modell: opus
allapot: megallt
ag: claude/epic-hawking-d0313a
pr: 705
ad: gyökérok-tábla a lektor 46 tételére, a független ellenőr 17 eltérésére és a gépi versellenőrzés 14 eltérésére; a 10. sablonban „Állítás a versről — írás közben” hét szabállyal és valós rossz/jó példapárokkal, a belső-szó szabály pontosítva; a 9. sablonban a lap eleje és a Kivonat határszabályának egyezése; a proza_allitas.py két új ⚑ jelzése (kapcsolat-állítás, hatókör) teszttel
kovetkezo: "Te: a draft PR áttekintése és merge-e; utána az ISTENTISZT-001 U3 menete ezzel a prompttal fut; az olvasói kapu bővítése (N-F206a) a #699 merge-e után"
munka: folyamat
olvas: [sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, eszkozok/proza_allitas.py, eszkozok/teszt_proza_allitas.py, adat/kapcsolatok.tsv]
ir: [sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, eszkozok/proza_allitas.py, eszkozok/teszt_proza_allitas.py]
fugg: []
nem_fugg: [123, 125, 178, 193, 200]
---

# F206_PROZA_PROMPT_BRIEF.md — A prózaíró prompt a HAMART-001 lektori körének tanulságával

*FELADATOK #206 · Modell: opus · v1 · 2026.11.11*

**Indok.** A HAMART-001 lektora 46 tételt adott, a javítókör (#699) gépi versellenőrzése és független ellenőre az újraírt prózán is talált ugyanazokból a hibaosztályokból. Az ISTENTISZT-001 új cikkének prózája egyszer készüljön. A lektor ne találja meg újra ugyanazokat a hibaosztályokat. Ezért a tanulság a prózaíró promptba és a kapukba kerül, a próza előtt. Gyökérok-szabály: második előfordulásnál gépi védelem kell.

**Bemenet** (más ágakon, `git show`-val; a teljes lapot nem olvassa):

- `naplok/KIADAS_HAMART-001_lektor.md` (`origin/claude/kiadas-hamart-d4c26f`);
- `naplok/HAMART_lapjavit_jelentes.md`, `naplok/HAMART_lapjavit_versellenorzes.md`, `naplok/ELLENOR_HAMART_lapjavit.md` (`origin/claude/lap-javit-hamart`);
- a 9. és a 10. sablon a main-en (F193 v1.1, F182.37, F200.3).

**Hatókör.** Nem nyúl ezekhez:

- `eszkozok/lexikon_general.py`, `lexikon/*`, `motivumok/*`, `adat/*` (a #699, a CS3, az F202 és az F203 írja);
- a 2. sablon (az F205 írja);
- az `eszkozok/olvasoi_kapu.py` (a #699 írja; a bővítés nyitott tétel, N-F206a).

A `MUNKAMENET.md` nem változik: a lépések sorrendje ugyanaz.

**`nem_fugg`.** A #123, #125, #178, #193 és #200 is írja a 9. vagy a 10. sablont, illetve a `proza_allitas.py`-t. Ezek mind `megallt` állapotúak: a sablon- és eszközmunkájuk a main-en van, és ez a menet a mai main-re épít. A levezetett függésből ezért függési kör lett (#123 ↔ #125 ↔ #178 ↔ #193 ↔ #200 ↔ #206); a `nem_fugg` ezt oldja fel, ugyanúgy, ahogy az F193 és az F200 tette. Az F205 (nem indult) a saját M0 lépésében veszi fel a 9. és a 10. sablont az `ir`-be; a két menet sorrendjét a merge-ek sorrendje adja, és ezt az orkesztrátor dönti el.

## Teendő

1. **F206.1 Gyökérok-tábla** (`naplok/F206_jelentes.md`). Minden lektori tételhez, ellenőri eltéréshez és versellenőrzési eltéréshez meg kell adni, hogy a hiba oka (a) prompt- vagy forrásszabály hiánya, (b) generátor (a CS3 viszi), (c) adat, vagy folyamat. Utána a tételeket hibaosztályokba kell csoportosítani.
2. **F206.2 Szabályok** az (a) osztályokra, osztályonként egy szabállyal, egy helyen (F184):
   - a próza mondatszintű szabálya a 10. sablonba kerül, a forrásszabály a 9.-be;
   - minden szabály mellé rossz/jó példapár a HAMART valós, javított mondataiból;
   - ahol meglévő szabály pontosítható, ott pontosítás, nem új szabály.
3. **F206.3 Gépi védelem.**
   - Osztályonként meg kell nevezni a kaput.
   - A `proza_allitas.py` bővül, teszttel.
   - Az `olvasoi_kapu.py` bővítése csak a #699 merge-e után történhet: addig nyitott tétel (N-F206a).
   - Ami gépileg nem fogható, az a lektoré; ezt a jelentés kimondja.
4. **F206.4** Helyőrzők: `dontesek/uj/epic-hawking-d0313a.md` és `nyitott/uj/epic-hawking-d0313a.md`.
5. **F206.5** Egy `fuggetlen-ellenor` futás, legfeljebb egy javítókör, draft PR.

## Garanciák és döntési napló

- G1: a diff csak a fenti `ir` fájlokat, a briefet, a `naplok/F206_*` fájlokat és a helyőrző-fájlokat érinti.
- G2: a `proza_allitas.py` kapu-szintje változatlanul JELENTÉS (DT785); a tesztek a CI „Szabaly-tesztek” lépésében futnak.
- G3: a TSV-olvasás `split('\t')`.
- G4: példapár csak a HAMART-001 valós mondataiból áll (rossz: a lektor által látott main-szöveg; jó: a #699 javított szövege); kitalált példa nincs.
- D1 (DT793): a próza mondatszintű szabályai a 10. sablonban állnak, a forma- és szerkezeti szabályok a 9.-ben.
- ⛔ A merge a felhasználóé (az orkesztrátor végzi a kérésére).
