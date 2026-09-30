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
