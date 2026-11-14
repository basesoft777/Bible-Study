# Brief-fejléc lezárás — 2026-11-14

*Kötegelt fejléc-karbantartás (SYSTEMS). A bizonyíték: `gh pr list --state all` (729 PR) és az `origin/main` commitjai (`F<nn>…` előtag), `eszkozok/feladatok.py` fejlécolvasójával. Zárási szabály: mergelt PR + a brief saját pontjai közül nincs nyitva hagyott ⛔, N-tétel, döntés vagy lépés. Kétes esetben nem zártunk. Kihagyva: F217 (#725) és F218 (#729) nyitott PR-ja.*

Előtte 66 nem lezárt brief volt (23 nem_indult, 3 brief_kell, 11 fut, 23 megallt, 6 dontesre_var). **Lezárva: 8.**

## Lezárt (brief → bizonyíték)

| Brief | Bizonyíték |
|---|---|
| #102 F102_BDB_SZELETELO_JAVITAS_BRIEF.md | PR #664 mergelve (2026-11-09); a maradék 4 mechanikus tétel ismert napló-pontatlanság, orkesztrátori döntéssel rögzítve |
| #121 F121_GLOSSZA_FORDITAS_BRIEF.md | ALVIL-001 menet = PR #509 (ág f121-alvil-13) mergelve 2026-10-29; a további F121-PR-ok (#514, #518) is mergelve |
| #161 F161_GLOSSZA_LANC_BRIEF.md | a draft PR = #610 mergelve 2026-11-03; a hivatkozott további lépések más sessionek dolga |
| #165 F165_LAPJAVIT_ARTIFACT_BRIEF.md | PR #641 mergelve 2026-11-08; a ⛔ 4. lépés (próba) kész |
| #181 F181_KAROLI_KH_JELOLTEK_BRIEF.md | PR #675 mergelve 2026-11-10; a két maradék tétel rögzítve (F181.48, F181.49) |
| #191 F191_TANUINDEX_BRIEF.md | PR #684 mergelve 2026-11-11; nincs nyitva hagyott ⛔ vagy N-tétel |
| #192 F192_ELLENOR_SZUKITES_BRIEF.md | PR #685 mergelve 2026-11-11 |
| #195 F195_DESIGN_SYSTEM_BRIEF.md | PR #692 mergelve 2026-11-11; az N156 ELVETVE (felhasználói döntés 2026-11-11, lezárta az F212) |

## Nem zárt — részben teljesült vagy folyamatban

| Brief | Állapot | Miért |
|---|---|---|
| #7 | fut | A4 adag (új session) hátra |
| #13 | brief_kell | brief kell (a #11 után) |
| #22 | megallt | a D, E, F csomag PR-ja és N-F22e hátra; a brief él |
| #25 | brief_kell | brief kell (a #11 1. lépcsője után) |
| #38 | megallt | a 13–14. adag ellenőrzése és az Mz zárás a felhasználó jelzésére vár |
| #52 | dontesre_var | ismétlődő feladat; DT90/SEMA↔CLAUDE.md ⛔ nyitva |
| #86 | dontesre_var | DT-F86a–g döntés hátra |
| #111 | megallt | 1. tartalmi maradék nyitva (dontesre_var ágon nem nő a k); #410 mergelve |
| #123 | megallt | több HAMART-utáni lap új cikk-menete (F10) még hátra; a brief tovább él |
| #134 | megallt | telefonos próba, M5 hátra |
| #137 | brief_kell | brief kell (a #96 után) |
| #140 | megallt | #481 mergelve, de a pardes.db újraépítése az N-F117a javításával még hátra |
| #146 | megallt | #503 mergelve; N-F146a, N-F146b nyitva |
| #149 | dontesre_var | M0 mérés ⛔ hátra |
| #151 | megallt | DT443 döntés és az 1. lépés (hatar-ellenor) hátra |
| #153 | megallt | #547 mergelve; a zárás a felhasználó döntésére vár, kézi sor G1941 |
| #157 | megallt | M0 és a db capability ellenőrzés hátra |
| #158 | fut | a #27 M1 hátra |
| #160 | fut | ⛔ MENNY-001 NT-helyei és a bevezetés hátra |
| #163 | dontesre_var | ⛔ DT605 és DT606 (szerző, terméknév) vár |
| #171 | megallt | #642 mergelve; a 4. lépés (generátorsablon, nyilt_mag) hátra |
| #172 | dontesre_var | #643 mergelve; a jelentés 6. pontjának kétes esetei felhasználói átnézésre várnak |
| #178 | megallt | #655 mergelve; N-F178a, N-F178b nyitva |
| #179 | megallt | #654 mergelve; 1 mechanikus maradék (a 3. teendő DT-F179a-ra utalása) nem igazolt javítottnak |
| #188 | fut | T7 (a merge utáni első 3 PR mérése, N133) és a SEMA-rész (N129) hátra |
| #194 | dontesre_var | #709 mergelve; N-F194h döntés, a 2. kiadás sora, N179–N185 nyitva |
| #198 | fut | #693 mergelve; DT778 és DT779 🟡 (licenc-kérdések) nyitva |
| #201 | fut | #698 mergelve; a workflow_dispatch próba a merge után nem igazolt |
| #202 | megallt | #703 mergelve; N-F202e és DT801 nyitva |
| #203 | megallt | #704 mergelve; DT805, N-F203a nyitva |
| #205 | fut | M3 és M5 hátra (az F212 után); a brief fut |
| #208 | megallt | #710 mergelve; a Zenodo-feltöltés a felhasználó lépése, nincs igazolva |
| #212 | fut | F212.2 és a további lépések futnak (#715, #726 mergelve, a brief él) |
| #216 | megallt | #724 mergelve, de az 1. javítókör utáni 2. független ellenőrzés nem igazolt (ELLENOR_F216 fájl nincs) |

## Nem zárt — nem indult el (23)

Csak befogadási/átszámozási PR-juk vagy főágra beolvasztott commitjuk van, a munka nem kezdődött el (az F217 és F218 külön PR-ban nyitott): #10, #48, #59, #69, #70, #74, #75, #81, #101, #106, #122, #129, #133, #135, #138, #139, #147, #154, #156, #164, #173, #217, #218.
