# ELLENŐR: F38_BDB_FORDITAS_BRIEF.md — 5. adag

Tartomány: `f77d84c..ef2b0fc` (ág: `claude/f38-adag5`, 28 commit). Az ellenőr (`fuggetlen-ellenor`) jelentése; a fájlt a főszál mentette, mert az ellenőr nem tud fájlt írni.

## Eredmény: 6 eltérés, kezelésük

| # | Eltérés | Kezelés |
|---|---|---|
| 1 | **H7970 tartalmi félrefordítás:** a „követi / megelőzi” alany-tárgy viszonya fordított (az egyesek követik / a 100 követi) | Javítva (F38.310): „׳שׁ követi az egyeseket”, „követi a 100-at (1000-et stb.)” |
| 2 | Az N-F38a–c a `NYITOTT_FELADATOK.md`-ben nyitott maradt, a DT-F38g „három tétel nyitott” szövege nem frissült | Javítva: ✅ LEZÁRVA (DT-F38h), a DT-F38g sor kiegészítve |
| 3 | „hátra 7 659” helyesen 7 658; a „406 sorrend-sor (269 + 163)” ellentmondásos | Javítva a naplóban és a DT-F38i-ben (406 = 243 + 163; a 26 #28 sor nincs a sorrendben) |
| 4 | Hiányzik a `BDB_FORDITAS adag 5: …` záró commit és a push; a 3143734 tétel-azonosító nélküli, a brief törzsét is módosítja | A push és a PR ezzel a lépéssel megtörténik; a 3143734 a felhasználó kérte alakban („F38: modell sonnet (DT-F38e)”) készült; a törzs-megjegyzés szintén a felhasználó utasítása volt |
| 5 | A napló 5. adagos Szellem-tábla sorában a H6213 szerepelt (nem az adag szócikke) | Javítva: kivéve |
| 6 | H3532 stílus: „Mózes második könyve Mózes harmadik könyve Numeri” kevert könyvnevek | Nyitva, a naplóban jelölve (stílus, nem gátló) |

## Igazolt pontok (OK)
- 163 új sor (sorrend 244–406), `allapot=sonnet`, `modell=claude-sonnet-5-5`, terminológia v3; duplikált kulcs 0; a H6213/H6256 nettó diffje 0; a 10 kézi sor és a többi régi sor változatlan.
- H4390 (2Móz 31:3; 35:31 nagy, 28:3 kicsi), H7451 kicsi, H5674 1Kir 22:24 nagy; a 163 soron a nagybetűs Szellem helyei egyeznek a napló táblájával; Lélek/Szentlélek 0.
- H8050 `Heb.`, H5922 `accusative` kivétel indokolt a forrás szerint.
- A 13. kapus JELZES 16 szócikke függetlenül újraszámolva egyezik a naplóval.
- Forrás 499 783 → fordítás 522 506 karakter, 163 szócikk; a forrás hivatkozás- és „N t.” számai mind a 163 szócikkben megvannak a fordításban; a hangrendi toldalék-hiba 0.
- `futtat.py` (E2–E16, E19) 0 találat; E12–E15 0; táblasor-Δ csak az `adat/forditasok.tsv` (+163).

## Nem ellenőrizhető az ellenőr szerepével
A kapuk 1–13 és a tesztek futtatása, a „2. kapu egyszer sem bukott” állítás — ezeket a főszál futtatta (163/163 átment, `ellenoriz.py` SÉRTÉS 0).

*Az ellenőr két, csak olvasó eltérést jelentett a saját szabályaitól (szűrők a diff kimenetén, magyar könyvnév inline `awk`-ban); a parancsok hiba nélkül futottak.*
