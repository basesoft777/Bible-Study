# F06 zárójelentés — új források 2. felmérése (FELADATOK #6)

Ág: `claude/f06-forrasfelmeres` · HEAD a zárás előtt: `91a3aca` · Futtatás: GitHub Actions (helyi gép nem kellett) · Jelentés: `naplok/F06_forras_jelentes.md`

- **BSB (N30):** 98,83% (1515/1533 vers) a előre rögzített 95%-os küszöb fölött; javaslat: IMPORT. A küszöb és a definíció a mérés előtt rögzült (`kuszob.txt`, `1a9bd6a`).
- **Macula (N31):** a letöltés teljes (39 könyv, 929 fájl), az 1Sám–2Krón megvan; az FJ1 „hiánya” hipotézis szerint fájlnév-minta hiba (nem reprodukálva). Javaslat: FELTÉTELLEL.
- **#8 bemenete:** a 87 függő helyből 39 kap LXX-megfelelőt a Maculától; 38 héber szó görög Strong nélkül (ebből 26-ban van valódi görög szóalak, 12-ben nincs; a `{δ}` jelölő nem szóalak), 8 helyen nem volt mit keresni, 2 vers hiányzik. Csak javaslat, kézi megerősítés kell.
- **KJV/ASV (N29):** az eBible USFM teljes, KJV 31099/31102 vers szó-szintű Strong-címkés; javaslat: IMPORT, mintaellenőrzéssel.
- **Nave (N27):** `basokant/nave` FELTÉTELLEL (nincs LICENSE-fájl), `theonize` FELTÉTELLEL (GPLv3), `elcafe7/lex` NEM.
- **MiniMax-költség:** 0,011927 USD, 29 hívás (plafon 1 USD); a licencítéletek javaslatok, a végső döntés a felhasználóé.
- **Ellenőrzés:** `naplok/ELLENOR_F06.md` 13 eltérést talált; az 1–7. pontot a F06.7 javította (mérés újrafuttatása nélkül). Újraellenőrzés nem futott.
- **Egyeztetett eltérés:** a BSB-nevezőt (TAHOT-tal rendelkező versek) a felhasználó a javaslat részeként hagyta jóvá.
- **Egyeztetett eltérés:** a `scrollmapper/bible_databases` címkéje „NEM MÉRT (időkorlát)” a brief hármas skálája (IMPORT/FELTÉTELLEL/NEM) helyett; a felhasználó jóváhagyta.
- **Nyitott:** N27, N29–N31 lezárása a felhasználó döntése; a CI E16 miatt a PR címe `[ELLENŐRZŐ]` előtagú.
