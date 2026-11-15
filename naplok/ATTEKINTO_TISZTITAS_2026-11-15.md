# A heti áttekintő tisztítása — 2026-11-15

*F220.2 (SYSTEMS). A felhasználó kérése: „semmilyen lezárt tétel nem kell bele”. A ténylegesen lezárt, de nyitottnak látszó briefek lezárása átvitellel. Bizonyíték: `gh pr list --state merged` (731 PR), az `origin/main` commitjai (`F<nn>.` előtag), a brief fejléce és az érintett fájlok a main-en; olvasó: `eszkozok/feladatok.py` fejlécolvasója.*

*Hatókör (az orkesztrátor kérése, 2026-11-15): a heti áttekintő oldal átírása és újragenerálása nem ennek a PR-nak a dolga; a `heti_attekinto.py` és tesztjei változatlanok (az F220.1 és F220.3 commit visszavonva az F220.4-ben).*

**Szabály (lezárás átvitellel).** Ha a brief fő eredménye (az `ad` mező) mergelt PR-ral a main-en áll, a brief `lezarva` lesz. A nyitott pontjai (⛔ pont, maradék lépés) új N-tételként a `nyitott/uj/affectionate-keller-a3f024.md` fájlba kerültek (`N-F220a`–`N-F220h` helyőrzők, a számot a `szamkiosztas` adja), a briefre hivatkozva és sávval. A már meglévő N-tétel nyitva marad, a brief csak hivatkozik rá. A brief-fejlécből csak az `allapot` és a `kovetkezo` változott.

Előtte 61 nem lezárt brief volt, **most 38**; **lezárva: 21** (a 22. jelölt, a #201, közben a gépi lezárás (#731) lezárta, azt nem érintettem; a #219-et a #736 merge-e után szintén gépi lezárás zárta).

## Lezárt (brief → bizonyíték → átvitel)

| Brief | Bizonyíték (a fő eredmény a main-en) | Átvitel |
|---|---|---|
| #22 KAROLI_STRONG | PR #537 (2026-11-01, Mt–ApCsel): a teljes Ószövetség és Újszövetség párosítása mergelve (#108 … #537) | N-F22e (meglévő, nyitva) |
| #38 BDB_FORDITAS | PR #556 (2026-11-01): 13–14. adag, a 8 073 soros sorrendtábla kész | N-F220a (Mz zárás) |
| #111 ELTERES_PARANCS | PR #410 (2026-10-18): `/elteres` parancs | N-F220b (4 alacsony maradék, ELLENOR_F111_3) |
| #140 GLOSSZA_FORDITAS | PR #481 (2026-10-26): `adat/glosszak_heber_hu.tsv` a main-en | N-F117a (meglévő: a pardes.db újraépítése) |
| #146 VERSMEGF_MT_JAVITAS | PR #503 (2026-10-29) | N-F146a, N-F146b (meglévők) |
| #149 OLVASO_TANULMANY | PR #588 (2026-11-02, M0–M3) és #596; a `vers.tanulmany`, `/tanulmany/<id>` az `olvaso_szerver`-ben | N-F220c (⛔ M4 vizuális próba) |
| #151 MOTIVUM_HATAR | PR #538, #544, #557 (2026-11-01): gépi rész, `hatar-ellenor` M1, K1–K5; `naplok/HATAR_*.md` mind a 9 motívumra; DT443 ✅ (b) | nincs |
| #158 THAYER_API_KOTEG | PR #575 (2026-11-02): `eszkozok/thayer_api_koteg.py` | nincs (az első beküldés a #27 M1-e) |
| #160 JELOLT_ELOSZURES_LEXIKAI | PR #580 (2026-11-02): `eszkozok/jelolt_eloszures.py` lexikai szabálya, M0 mérés | N-F160a, N-F160b, N-F150a (meglévők) |
| #163 TUD_OLCSO | PR #628 (2026-11-04): négy `kozlemeny/` szöveg és a `CITATION.cff`; DT605, DT606 eldöntve (2026-11-14) | N-F220d (szerzői név helyőrző a `CITATION.cff`-ben); N-F163c (meglévő) |
| #172 KAROLI_PONTOSSAG | PR #643 (2026-11-05): a pontosságmérés jelentése | N-F172a, N-F172b, N-F172c (meglévők) |
| #178 LEXIKON_AG_LEZARAS | PR #655, #657 (2026-11-09) | N-F178a, N-F178b (meglévők) |
| #179 USZ_KONYVLISTA | PR #654 (2026-11-08); N-F09f lezárva | N-F220e (mechanikus maradék); N-F179a (meglévő) |
| #188 TEHER_CSOKKENTES | PR #677 (2026-11-10) | N133 (T7 mérés), N129 (SEMA-rész) (meglévők) |
| #194 ISTENTISZT_UJ_CIKK | PR #709 (2026-11-13); N-F194h lezárva (DT834) | N-F220f (a 2. kiadás `kiadasok.tsv`-sora); N179, N181–N185 (meglévők) |
| #197 BDB_HARMADIK_TANU | PR #688 (2026-11-11); `naplok/ELLENOR_F197.md` kész | nincs |
| #198 NYILT_MAG_HATASTORTENET | PR #693 (2026-11-11) | DT778, DT779 (🟡, meglévők) |
| #202 BDB_LANC | PR #703 (2026-11-12) | N-F202e, DT801 (meglévők) |
| #203 THAYER_FORDITAS | PR #704 (2026-11-12) | N-F203a, N-F203c, DT805 (meglévők) |
| #208 NYILT_MAG_SZOVEGEK | PR #710 (2026-11-12) | N-F220g (Zenodo-feltöltés, a felhasználó lépése) |
| #216 PUSH_ELOTTI_KAPU | PR #724 (2026-11-13): `eszkozok/push_elott.py` | N-F220h (a 2. független ellenőrzés) |

Új N-tétel: **8** (`N-F220a`–`N-F220h`). A többi maradék meglévő N- vagy DT-tételre hivatkozik, vagy nincs.

## Kétes esetek — nem zártam le (az orkesztrátor nézi meg)

| Brief | Miért kétes |
|---|---|
| #52 TERV_SZINKRON (dontesre_var) | A 3. futás mergelve (#265, #269), de a brief ismétlődő feladat („utána ismétlődő; a 2. pont szerinti eseményeknél indul”); a ⛔ SEMA 4 ↔ CLAUDE.md TAHOT-ellentmondás nyitott. Lezárás helyett az ismétlődés kezelése a kérdés. |
| #134 OLVASO_ALAPNEZET (megallt) | M0–M4 mergelve (#550), de az `ad` maga kéri a „valódi telefonon” mérést; a telefonos próba és az M5 hátra van. |
| #153 THAYER_KAROLI_TELJES (megallt) | A teljes ág a main-en (#547 a F153.20-ig), de az `ad` az eltérő sorok újrafordítását (M3-lánc) is kéri; hogy ez lefutott-e, a fejléc nem mondja, a zárás „a felhasználó döntésére” vár. |
| #157 LEKTOR_FELULET (megallt) | Sok PR mergelve (#558–#603), de a `kovetkezo` elavult („M0”), és két ág (`origin/claude/f157-lektor-folytatas`, `…-felulet-7b7d69`) mergelés nélkül előrébb van a main-nél: lehet, hogy a munka tovább él. |
| #171 KAROLI_HANGSULY (megallt) | A kéziratok mergelve (#642), de az `ad` a nyílt mag olvasói fájljait is kéri; a 4. lépés (generátorsablon) a #170 merge-e után hátra van. |
| #205 IGESZAKASZ_ELOKESZITES (fut) | M0–M2, M4 mergelve (#716), de az M3 és az M5 (a kinyerő, a hiányzó fordítások kötege) az F212 után hátra van. |
| #212 CS3_GENERATOR_KOR (fut) | #715, #726 mergelve, de az F212.2 (a 32 jóváhagyott tétel a generátorban) fut; az F218 új generátora felülírhatja. |
| #156 MUHELY_FEED_STASH (nem_indult) | A fejléc `nem_indult`, de a Feed és a Stash mergelve (#555–#576, #601), és a ma számozott DT846 is erre a feladatra mutat: a brief elavult, de a munka ma is mozog. |
| #221 (fut) | A fő eredmény mergelve (#733), de a `BRIEF_SABLON.md` szabályszövege a `sav`-PR után még hátra van (kész diff: `naplok/F221_jelentes.md`); a `BRIEF_SABLON.md`-hez ebben a körben nem nyúlhattam. |

Nem zárható, mert a fő eredmény nincs a main-en vagy a munka ma is fut: #7 (a Thayer-adagok futnak), #123 (a hátralévő motívumok), #217 (#725 draft), #218 (#729 draft), #220 (e munka maga).

A #736-tal érkezett új gépi kapu (JELENTÉS, nem hiba) a #212-t (#715) és a #52-t (#265) jelenti: mergelt PR, de nem lezárt fejléc. Ez a két kétes eset, a jelentés ennyiben egyezik a fenti döntésemmel; a kapu ettől nem bukik.

## Nem érintett — nem indult el vagy brief kell (23 brief)

#10, #13, #25, #48, #59, #69, #70, #74, #75, #81, #101, #106, #122, #129, #133, #135, #137, #138, #139, #147, #154, #164, #173; egyikük fő eredménye sem áll a main-en (többnél csak a befogadás PR-ja mergelt). Megjegyzés: a #147 `kovetkezo`-ja („Te: befogadás a /befogad-dal”) elavult, a befogadás mergelve (#512); a #133, #154 hasonlóan csak a befogadás után áll, ezeket nem vizsgáltam tovább.

## Nyitott brief sávonként (a lezárások után; a #736 ötödik sávjával)

| Sáv | Folyamatban | Vár |
|---|---|---|
| SYSTEMS | 3 (#157, #220, #221) | 3 (#52, #156, #217) |
| CONTENT | 6 (#7, #123, #153, #171, #205, #212) | 16 |
| SERVER | 1 (#134) | 8 |
| USER | 0 | 0 |
| BUSINESS | 0 | 1 (#86) |
| **Együtt** | **10** | **28** |

A „te teendőid” sor: 10 brief (#52, #86, #123, #129, #134, #147, #153, #164, #220, #221).
