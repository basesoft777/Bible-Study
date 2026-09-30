# ELLENŐRZÉS — F18 (Nave-import, basokant) — összefoglaló

*Ág `claude/nave-import`, base `4525a63`. A `fuggetlen-ellenor` (szerepe szerint csak olvas) két kört futott; a teljes soronkénti jelentés a session kimenetében volt, ide a lényeg került. Az orkesztrátor a végső számokat saját Grep-számlálással újramérte.*

## 1. kör (head `f468ac7`) — ELTÉRÉS: 8 tétel
Javítva az `ac73572`-ben (F18.6): egyfejezetes könyvek (250 hibás `X 1:1` → 21, ebből 17 valódi `:1`, 4 jelölt); 688 `:szám`-os cimke → 0; „100%” és „hibák jelölve” állítás átfogalmazva; `nincs_a_tablaban` szétválasztva (145 `a_tablaban_nincs_kjv_megfelelo` + 582); proveniencia-sorok; brief `ir:`; szerepmátrix állapota `nincs adatosítva`.

## 2. kör (head `ac73572`) — ELTÉRÉS: 8 tétel
OK volt: 85 116 adatsor (77 985 `vers`, 4 368 `lasd`, 2 763 `szoveg`), 5 322 `tema_id`-maximum, státuszok, `X 1:1`, `:szám`-os cimke, sorcsökkenés (0 törlés `adat/`, `konkordancia/` alatt), saját-sor szabály, theonize-adat hiánya, E2–E16 (E11: `szotar_szerepek.tsv:5`, base előtti sor).
Eltérések és sorsuk (javítva az `679723e`-ben, F18.7):
1. ≥29 jelöletlen összeolvadt hibás kijelzés (`DISP_RE` 6 betűs korlát) → töredék-alapú felismerés; `gyanus_kijelzes` 22 → 52 sor (54 jelölés), 49 `toredek`/`javaslat`; `igehely` nem írva át.
2. `igehely_osis` szintetizált a 296 egyfejezetes soron → `eredeti_osis:` megjegyzés (296).
3. Szerepmátrix `sorrend=12` → **nyitva marad**, DT18 (j): a SEMA 2.13 egységes frissítése a #16–#19 után.
4. „24 sor” valójában 22 sor / 24 jelölés → pontosítva.
5. Jelölt sorok `azonos` Károli-státusza → `nem_ertekelt`.
6. Brief `cim`/`ad` → frissítve.
7. „nulla-diff” hatóköre → pontosítva.
8. Négy korai commit-üzenet ékezet nélküli (862085b, de63846, 468feb7, 7c00d63) → **nem javítható** az ág újraírása nélkül; nyitott, kozmetikai.

## Orkesztrátori újramérés (head `679723e`)
85 116 adatsor · `gyanus_kijelzes` 52 sor · `javaslat:` 49 · `eredeti_osis:` 296 · `:szám`-os cimke 0 · jelöletlen `Ki/Ch/Sa/Ti/Co/Th/Pe/Jn`-töredék 0 · `X 1:1` az öt könyvön 21 · `git diff --numstat`: 0 törlés · `feladatok.py ellenoriz`: 47 brief, 0 hiba.

## Nem ellenőrzött (a 3. kör nem futott)
Az F18.7 javítását (töredék-szabály) független ellenőr nem nézte meg; a szabály nem bizonyítottan fog meg minden összeolvadás-osztályt (DT18 (k)). A nyers `nave.txt` újrafuttatása, a Gemini 0 USD költség és az 1..5322 azonosító-hézagmentesség független igazolása nem történt meg. A teljes független kiadás-összevetés hiányzik.

**Verdikt: TISZTA FELTÉTELEKKEL — az import `javaslat` státuszú; a DT18 nyitott tételei a felhasználóé.**

## 3. kör (célzott, F18.7 = `679723e`, head `e641566`) — ELTÉRÉS: 7 tétel

Kérdés: lefedi-e a töredék-szabály az összes összeolvadás-osztályt? **Válasz: RÉSZBEN.** A nyers forrás 49 `</ref>[A-Za-z]` előfordulásából mind a 49 jelölt (52 `gyanus_kijelzes` sor, 54 jelölés, 49 `toredek`/`javaslat`, 296 `eredeti_osis`, 85 116 sor — Grep-pel igazolva). Az ellenőrzés a megengedett Bash-parancsokkal és Greppel futott, a parszolót nem futtatta újra.

| # | lelet | súly | sorsa |
|---|---|---|---|
| 1 | Töredék önálló `<ref>`-fel (`Titus 2` + `Col.8.x`): 12 jelöletlen sor (16103–16106, 19518–19519, 51735–51737, 52528–52530), 8 nem létező Kol-hely (valójában 2Kor) | magas | nyitott, DT18 (3. kör javaslat) |
| 2 | Napló/README „Tit 2”, „Co” lefedettnek mondva | közepes | **helyesbítve** (napló 2.7, README) |
| 3 | 15 sor római számos név után `<ref>` nélküli hivatkozás (12 igehely nem lett `vers`-sor) | közepes | nyitott, DT18 |
| 4 | „with N:N” folytató-hivatkozás: 72 `utotag` + 54 `cimke` sor, a címke öröklődik | közepes | nyitott, DT18 |
| 5 | `javaslat` a tartományt/listát az első versre csonkolja (≥8 sor) | alacsony | dokumentálva, nyitott |
| 6 | DT18: az „Alkalmazva” szöveg a Napló oszlopba került; a `javaslat` állapotérték felvétele a SEMA 2.13-ba nem alkalmazott | alacsony | szöveg áthelyezve a Döntés cellába; az állapotérték **halasztva** (import `javaslat`-státusza a `nincs adatosítva` értékkel jelölt) |
| 7 | `Jer 2` (84711) „valószínűleg helyes” minősítés téves | alacsony | helyesbítve (napló 2.7) |

OK: `datasetek.tsv` 4 új sor (72 adatsor, 7 mező, nincs `mindig`/`felteteles`), SEMA 2.6/2.13 számai (72; 22 sor, sorrend 1–10 és 12), E8 0, E2–E16 a változott fájlokon 0 (E9: 2 jelentés `SEMA.md:235-236`, a diffen kívüli régi sorok), `javaslat` szúrópróba 8/8 helytálló, `nem_ertekelt` mind az 52 jelölt soron, sorcsökkenés 0.
Nem ellenőrzött: a fejezetszám-egyezés teljes összevetése (77 673/77 685), E17 (DT3 nyitott), ⛔ pontok (célzott kör).

**Verdikt 3. körre: ELTÉRÉS: 7 tétel (2 helyesbítve, 1 áthelyezve, 4 nyitott DT18-ban). A PR-ben lévő adat `javaslat`-állapotú, teljes jelölési lefedettséget nem állít.**
