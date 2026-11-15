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

## `sav` besorolás (2. lépés)

Értékkészlet: SYSTEMS · CONTENT · SERVER · USER (`BRIEF_SABLON.md`). A besorolás a cím és az `ir` mező alapján készült, kétes esetben a fő termék szerint. Kötelező a `feladat` és `naplozas` típusnál; az archív brieföknek nincs. Az F217 (SYSTEMS) és az F218 (CONTENT) briefje a saját PR-jában kapja meg; addig a `SAV_ATMENET_KIVETEL` mentesíti őket a kötelezőség alól (a PR-ok merge-e után a tuple üríthető).

| Sáv | Darab |
|---|---|
| SYSTEMS | 38 |
| CONTENT | 150 |
| SERVER | 25 |
| USER | 1 |

**SYSTEMS:** #2, #4, #15, #20, #26, #30, #32, #37, #39, #40, #45, #47, #49, #50, #51, #52, #53, #82, #111, #112, #113, #116, #125, #156, #157, #165, #184, #188, #189, #192, #193, #196, #200, #201, #207, #209, #216, #217

**SERVER:** #25, #60, #76, #79, #92, #97, #98, #100, #101, #104, #105, #122, #134, #135, #137, #139, #147, #149, #164, #187, #195, #204, #210, #213, #215

**USER:** #86

Minden más feladat- és naplózás-brief: CONTENT (150 db; a teljes lista a briefek `sav` mezőjében).

### Kétes esetek (az orkesztrátor átnézésére)

- #25: olvasói HTML → SERVER (a fő termék az olvasó)
- #26: egyforrású lánc döntései (naplózás) → SYSTEMS (brief-/dokumentumrendszer)
- #29: szótárfordítás döntései (naplózás) → CONTENT
- #52: terv-szinkron → SYSTEMS (dokumentum-karbantartás)
- #61: lekérdező naplózása → CONTENT (kutatási eszköz)
- #62: Strong-normalizáló → CONTENT (adateszköz)
- #79: SQLite-építő (pardes.db) → SERVER, az olvasó adatbázisa
- #92: pardes.db olvasói kiegészítése → SERVER
- #97: pardes.db újraépítése → SERVER
- #104: BDB-blokk megjelenítése → SERVER
- #105: BDB szórend a megjelenítésben → SERVER
- #124: gerinc-scan kártya → CONTENT (kutatási eszköz)
- #125: munkamenet és sablonok frissítése → SYSTEMS (a gerinc-kártya tartalma CONTENT)
- #137: modernizált Károli a keresőben és a pardes.db-ben → SERVER
- #138: szó-lap alapjelentés (adatjavítás) → CONTENT, bár a szó-lap olvasói felület
- #148: új motívum védőkorlátjai → CONTENT (kapuk, de motívum-tartalmi)
- #149: tanulmány-sáv az olvasóban (adat + olvasó) → SERVER
- #156: műhely Feed/Stash → SYSTEMS (belső áttekintő), nyilvános kirakat része CONTENT
- #157: lektor-felület (db capability artifact) → SYSTEMS (a munkafolyamat eszköze)
- #163: tudományos megfelelőség (közlemények) → CONTENT
- #165: /lap-javit lapnézet → SYSTEMS (parancs/eszköz)
- #166: adatszintű Károli-idézet kapu → CONTENT
- #187: Thayer olvasói kártya (adat + olvasó) → SERVER
- #190: lezárt lapkövetelmény-lista → CONTENT (sablonok)
- #200: próza-állítás ellenőrző (kapu) → SYSTEMS; tartalmat is érint
- #212: CS3 generátor-kör → CONTENT (lapgenerátor)
- #215: angol Thayer/BDB az olvasóban → SERVER
- #217: (a saját PR-jában kapja: F217 → SYSTEMS)
- #218: (a saját PR-jában kapja: F218 → CONTENT)

## Közvetített felhasználói döntések (az orkesztrátor üzenetei, 2026-11-14; a szavak szó szerint, a közvetítés nem ellenőrzött)

- **DT605 / DT606 → 🟢** („Igen, így mehet”): a `kozlemeny/MI_NYILATKOZAT.md` „Szerzőség és felelősség” bekezdése a jóváhagyott mondat (Logosz-lexikon, Demeter Tamás). Külön commit, `F163.` azonosítóval. Más helyőrző a fájlban nincs; a 5. sor megjegyzése („amíg helyőrző áll benne, a szöveg nem nyilvános”) általános és változatlan.
- **F163 brief NEM zárva.** Nyitva marad: a `CITATION.cff` helyőrzői (`A LEXIKON CÍME`, `SZERZŐ NEVE`; a 20., 22., 54., 56. sor; nem kérték), a DT607–d jóváhagyása az orkesztrátor által, és az `eszkozok/lexikon_general.py` `LEXIKON_CIM_HELYORZO` / `SZERZO_HELYORZO` állandói, amelyeknek a `lexikon/*_TUDOMANYOS.md` lapokon látható helyőrzők felelnek meg (ALVIL-001, ANTROP-001, HODIT-001, ISTENTISZT-001, KIRALY-001). Ezeket nem javítottam (generátor és generált lapok; az F218 újraírja a generátort, a lapokat a generátor állítja elő).
- **DT846** (N-F156e lezárva, DT559 pontosítása), **DT847** (a javított BDB-réteg zárt adat), **DT848** (a javított Károli-KH nyílt) helyőrzős sorok: `dontesek/uj/relaxed-proskuriakova-4e4ab6.md`; az N-F177a: `nyitott/uj/relaxed-proskuriakova-4e4ab6.md`.
- **Zárt BDB-réteg — ellenőrzés (nem javítottam):** a `nyilt_mag/`, a `nyilt_karoli_*` csomagok és az `eszkozok/nyilt_mag_export.py` egyik érintett fájlra (`bdb_vers_jelentes.tsv`, `bdb_szakaszok.tsv`, `bdb_szakasz_hu.tsv`, javítótáblák) sem hivatkozik; a `nyilt_mag/forrasok_es_licencek.tsv` a `BDB` sorát „engedett, de a csomag nem használja”-ként, a `BDB_forditas` sorát „kizárva”-ként jelöli. Az `adat/datasetek.tsv` a három táblát `korlatos` állapottal vezeti (ez nem nyíltság-jelölés). Nyíltnak jelölő vagy exportáló hely tehát nem található; a javított rétegnek (szórend-, tagolás-, hozzárendelés-táblák) nincs külön sora a `forrasok_es_licencek.tsv`-ben — ha zárt jelölést kell kapnia, az külön lépés.

## Push előtti kapu (2026-11-15)

Teljes futás részekben: E2–E39, E38, E39, a szabály- és feladatkövető tesztek, E18: RENDBEN. Az E1 21. szabálya (generált lap tisztasága) először egy SÉRTÉS-t jelzett, amelyet ez az ág okozott: az ISTENTISZT-001_TUDOMANYOS.md nyitott tételként hivatkozik az N59-re, én pedig lezártam. Az N59 lezárását visszavontam (a main 7f160363 lezártnak mondja; a lap újragenerálása után zárható, l. `naplok/NYITOTT_RENDEZES_2026-11-14.md`); utána az E1 21. szabálya RENDBEN. Az E1 többi sora a futás idejére nem volt külön ellenőrizve teljes kapufuttatásban (a teljes `push_elott.py` egy futásban a más session ellenőrzési zára és a 10 perces időkorlát miatt nem fért bele).
