# ELLENŐR — F193_SZABALYHELYEK_BRIEF.md · `origin/main..872c40a2` (5 commit, F193.0–F193.5)

*A `fuggetlen-ellenor` jelentése (modell: `claude-opus-5-5`, a kért `opus`-szal egyezik), 2026-11-11. A subagentnek nem volt fájlíró eszköze, ezért a jelentést a fő szál írta ki, tartalmában változatlanul, tömörítve. Hatókör: csak a szabályszöveg; a `lexikon/`, `eszkozok/`, `adat/`, `konkordancia/` és a `KESZ_LAP_KOVETELMENY.md` diffje üres.*

## RENDBEN

- Hatókör, törölt sor, táblasor-Δ (E17): rendben; a DONTESEK 7/7 sorcsere, a fájl vége érintetlen.
- B01 (`6_`:111), B02 (`6_`:474), B03 (`6_`:266, 519), B04 (`6_`:557, `9_`:93, `10_`:35), B05 (`6_`:287), B11 (`6_`:305), B12 (`6_`:139; `9_`:116–130, a HAMART-001 1Móz 3:17 mintája a Károli-szöveggel és az `elofordulasok.tsv` soraival egyezik; `lekerdez.py karoli "1Móz 3:17"`, ts=2026-11-11T12:44Z).
- A szakaszrend mind a négy fájlban: 9. Hatástörténet, 10. Értelmezés, 11. Módszertan, 12. Irodalom; régi szám csak az elavultként jelölt A) részben.
- J1 (`6_`:559), J2–J4 (`9_`:165–170, a `10_` hivatkozik).
- A tanúforrások és a Glossa a brief idézett döntéseivel egyeznek (DT740: Sefaria CC BY).
- DT-F193d: a `dontes_allapot.py` a `**RÉSZBEN FELÜLÍRVA` jelölést nem veszi érvénytelennek; a jelölt sorok tartalma helyes (DT276, DT547, DT566, DT730, DT733, DT756).
- DT-F193a–c: az idézetek egyeznek a brieffel és a közös jegyzettel.
- CI E9–E37: E25 JELENTÉS 3, E27 JELENTÉS 43, E34 FIGY 41 (meglévők); E26 0. E28 HIBA a `lexikon/HAMART-001_TUDOMANYOS.md:1147`-en: a main elsodródása, nem az ágé (az ág a `lexikon/`-hoz nem nyúl).

## ELTÉRÉS (súlyossági sorrendben)

1. **Átnézés ↔ javítókör** (`MUNKAMENET.md`:80, 93–97): a C-v sora a javítókör előtt rögzül, a javítás után a SEMA 2.48 szerint érvénytelen, a szöveg mégis azt mondja, hogy „második nincs”; az 5. lépés („változáslista”) nem mondja meg, hogy új átnézési sor-e.
2. **A C-h helye** (`MUNKAMENET.md`:76–77, 89–97): hiányzik a kötött sorrendből; a C-g, a C-h sor és az új bekezdés ellentmond egymásnak.
3. **DT-F193d** (`dontesek/uj/…`:4): a végrehajtó döntése eltér a felhasználó B17/B19 szövegétől, mégis 🟢; a brief szerint „tartalmi döntés nincs”. Döntés kell.
4. **Alcím-szabály** (`6_`:557, 561): a „nem kérdő” előírás mellett megmarad az „1.3 Mi esett ki és miért” és az „1.4 Mi maradt és miért”.
5. **A „visszhang” szó** (`6_`:569): a tilalom a 2. tábla „⚖️ visszhang” funkció-címkéjét is tiltaná.
6. **A C-o sor** (`MUNKAMENET.md`:79) nincs az új sorrendhez igazítva.
7. **A `/kiadas` parancsfájl** (`.claude/commands/kiadas.md`:2, 7) még a régi szerepet írja („második kiadás”, „nem kötelező”).
8. **A sablon 10 új előfeltétele** miatt az ISTENTISZT-001 prózája a #183 végéig nem indulhat; a brief `kovetkezo` mezője mást mond.
9. **A Targum** a C-vh-ban az ÚSZ-ág forrása, a sablon 6 2(b) pontjában nem; a C-vh megismétli a forrásszabályt (F184).
10. **Elavult 4.11-utalás** (`MUNKAMENET.md`:60, a B9 sor).

## A javítókör (F193.6, a fő szál)

Mind a tíz eltérés javítva: (1) az 5. lépés: a változáslista jóváhagyása új `lap_atnezesek.tsv`-sor a javított lap commitjával, és nem új átnézési kör; (2) a C-h az 1. pontban, a próza előtt, ha a határt és a prózát egy kéz viszi; (3) a DT-F193d 🟡 javaslat, a brief „Megállás” ⛔ a jóváhagyásra; (4) a „nem kérdő” kikerült, az 1.3–1.5 a DT760 szerint marad; (5) a tilalom csak a rétegnévre szól, a funkció-címke marad; (6) a C-o sor igazítva; (7) a `kiadas.md` leírása és bevezetője igazítva; (8) a brief `kovetkezo` mezője igazítva; (9) a C-vh csak hivatkozik a sablon 6 2–5. pontjára; (10) a B9 sor a 9. Hatástörténetre mutat. A K67d Glossa-mondata a #183 hatóköre, az N-F193a-ba került. Második kör nincs.
