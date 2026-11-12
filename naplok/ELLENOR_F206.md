ELTÉRÉS: 10 tétel

# Független ellenőrzés: F206 (`F206_PROZA_PROMPT_BRIEF.md`), `5b2d9fe1..0896aaf5`

*Ellenőr: `fuggetlen-ellenor`, tényleges modell `claude-opus-5-5` (a subagent-fájl kért modellje: `opus`; egyezik). A jelentést a fő szál írta ki az ellenőr válaszából, mert az ellenőrnek nincs fájlíró eszköze. A javítókör (F206.6) a `naplok/F206_jelentes.md` végén áll.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | `naplok/F206_jelentes.md:3`, commitok | „végrehajtó: claude-opus-5-5”; mind az 5 commit `Co-Authored-By: Claude Opus 5.5` sorral (`git log --format='%B' 5b2d9fe1..0896aaf5`). Adattábla `modell` mezőjét a menet nem írta. |
| G1 / 5. Hatókör | OK | — | `git diff --stat 5b2d9fe1..0896aaf5`: 8 fájl, mind `ir`, brief, `naplok/F206_*` vagy helyőrző. A tiltott fájlokra (`lexikon_general.py`, `lexikon`, `motivumok`, `adat`, `olvasoi_kapu.py`, 2. sablon, `MUNKAMENET.md`, `CLAUDE.md`) `git diff --name-only …` üres. |
| G2 | OK (statikusan) | `.github/workflows/ellenorzes.yml:153,185` | A „Szabaly-tesztek” lépés futtatja a `teszt_proza_allitas.py`-t; kilépési kód és kapuszint változatlan. |
| G3 | OK | `eszkozok/proza_allitas.py:93-107` | Az új `T_KAPCS` olvasása `tsv_dict`-tel (`split('\t')`), a `#` megjegyzéssort átugorja. |
| G4 / 2. Példapárok | OK | `sablonok/10_…:48,59-71`; `sablonok/9_…` (határ-elem 1.) | Mind a 9 pár ellenőrizve (`git diff --word-diff 5b2d9fe1 origin/claude/lap-javit-hamart -- motivumok/HAMART-001.md`, ugyanez az `adat/elofordulasok.tsv`-re): a rossz mondat betű szerint a main szövege, a jó a lap-javit szövege; eltérés csak a belső „” → »« és a (…) rövidítés, tartalmi átírás nincs. |
| D1 (DT793) | OK | `sablonok/10_…:3`, `9_…:5`, `dontesek/uj/epic-hawking-d0313a.md:1` | Mindkét fejléc kimondja a helyet. |
| 1. Lefedettség | OK | `naplok/F206_jelentes.md:54-99, 111-129, 133-148` | Lektor 1–46: 46 egymást követő sor. Ellenőr E1–E17 = a `ELLENOR_HAMART_lapjavit.md` 13 ELTÉRÉS-sora (a SEMA 2.49 négy, a CI-sor két tétel). Versellenőrzés: 2 szkript + 12 Sonnet = 14. |
| 1. Összesítő számok | OK | `naplok/F206_jelentes.md:103-105` | Újraszámolva: (a) 29, (b) 16 (ebből 5 (c)-vel), (c) 9; ellenőr (b) 6, (c) 6, folyamat 3; gépi 5, kézi 19, nem látja 10, „–” 12 = 46. |
| 1. Besorolás, szúrópróba (16 tétel) | ELTÉRÉS | `naplok/F206_jelentes.md:55` | 15 egyezik a lapjavit „A 46 tétel — hol és hogyan” táblájával (1, 4, 9, 15, 18, 19, 23, 32, 36, 45, 46, E4, E5, E14, E16). A 2. tétel nem: a „Negatív elhatárolás” címkét a generátor írja (`egyszerusitett_kolofon`, `AZONOSSAG_OLVASOI`), az F206 csak (c)+(a)-t ad, a (b) hiányzik. |
| 1/4. Mérési számok | ELTÉRÉS | `naplok/F206_jelentes.md:17,107,191`; commit `5a43a57b` | A szöveg „kézi 19 (⚑ 13)”-at és azt mondja, az új jelzés a 10., 12., 14. és 40. tételt fogja; a tábla „kézi ⚑” sorai csak 11 tételt adnak, „(új)” csak a 10., 14., 40.-nél. A 12. (Jer 51:46) az új logikával nem kaphat új jelzést: a `kapcsolodas`-ában nincs kapcsolat-ige, a rések nem említik, a hatókör-próba csak résen fut. |
| 4. A két másik motívum, „téves riasztás sincs” | ELTÉRÉS | `naplok/F206_jelentes.md:17` vs `:192` | „hat” vs hét motívum. A `kapcsolatok.tsv`-ben ALVIL, TEREMT-001, HODIT, MENNY sor nincs: a kapcsolat-próba négyen nem fut. `tematikus:` `gerinc_elem` csak a HAMART-001-ben van: a hatókör-próba egyiken sem tüzelhet. Elfedett téves riasztás: ISTENTISZT 1Móz 13:4 „Ábrám visszatér ugyanahhoz az oltárhoz” illeszkedik a `VISSZAUTAL`-ra, csak a `magas` sor miatt nem jelez. |
| 4. Logika | ELTÉRÉS | `eszkozok/proza_allitas.py:519-524, 706-707, 718-756` | (a) A résnél az ige a mondat egészében, nem a záradékban; (b) a szó szerinti „visszatér” is találat; (c) rokon fordulatot („kötődik a lánchoz”, „köti össze”) nem fog; (d) a `TEMATIKUS_KIMONDVA` bármely „nélkül” szóra elnémít. Egyik sincs a jelentés „Ami gépileg nem fogható” részében. |
| 4. Tesztek | ELTÉRÉS | `eszkozok/teszt_proza_allitas.py` (`test_ige_nelkul_nem_jelez`) | `kapcsolatok=[]`-vel a `_kapcsolat` már az első sorban üreset ad: nem méri, amit a neve mond; `KAPCS_MASIK`-kal volna érdemi. A metódusszám (29) egyezik. |
| 4. Futtatás | NEM ELLENŐRIZHETŐ | — | A szerep Bash-korlátja miatt; a fenti sorok statikus elemzésen alapulnak. |
| 3. Egy szabály, egy hely (6. sablon) | ELTÉRÉS | `sablonok/10_…:48`; `sablonok/6_PaRDeS_lexikon_oldal_sablon.md:582,584`; `nyitott/uj/…:1` | Az új belső-szó szabály tiltja a „Peshat-mag”, „alapvonal”, „láncvers” szót, a 6. sablon a generált bevezetőre előírja (:582, :584); az N-F206a kapuja a sablonhű kimenetet buktatná. Az ütközést sem a jelentés, sem az N-F206a nem nevezi meg. |
| 3/2. V11 proveniencia-sor | ELTÉRÉS | `sablonok/10_…:54` | Új szabálysor rossz/jó pár nélkül; formaszabály, amely a DT793 szerint a 9. sablon dolga (ott a lábjegyzet-alak áll); a CLAUDE.md 1. szabályát ismétli. |
| 3. Belső feszültség a 10. sablonban | ELTÉRÉS | `sablonok/10_…:49` vs `:66` | „a beépítés indoka szerkezeti jegy …, nem a szó puszta egyezése” vs az 5. szabály „közepes sornál a közös szót mondod, függést nem”: nincs kimondva, hogyan fér össze. |
| 3. Korábbi szabályok megmaradása | OK | `sablonok/10_…` diff | 4 törölt sor, mind átírás; a ⚑-bekezdés három régi teendője a 2., 3. és 6. szabályba került; a 9. sablonból egy sor változott. |
| 3. CLAUDE.md F184-tábla | OK (megjegyzés) | `CLAUDE.md` | A tábla „forrás-/cikkszabály → 9.”; a DT793 a mondatszintű prózaszabályt a 10.-be teszi. Helyőrzőként elfogadható; a CLAUDE.md-sor a döntés után igazítandó. |
| 5. Helyőrzők, végleges szám | OK | `dontesek/uj/…:1`, `nyitott/uj/…:1-2` | DT793, N-F206a/b a helyes mappában; a hozzáadott DT/N számok (DT766, DT768, DT785) meglévő hivatkozások. |
| 5. Brief fejléc | OK | `F206_PROZA_PROMPT_BRIEF.md:7,15-16` | `modell: opus`; a `nem_fugg` minden száma a `FELADATOK.md`-ben, mind „megállt”. A `feladatok.py ellenoriz`: NEM ELLENŐRIZHETŐ (szerepkorlát). |
| 6. Commitok, nyelv | OK | `git log --format='%B' 5b2d9fe1..0896aaf5` | `F206.0`–`F206.4` előtag, ékezetes magyar, Co-Authored-By sor. |
| A1 Memória vs. lekérdezés | ELTÉRÉS | `naplok/F206_jelentes.md:17,107,171,191-192` | A futtatásból származó számok mellől hiányzik a proveniencia-sor (CLAUDE.md 1. szabály). |
| A2 Nyitott tételek | ELTÉRÉS | `nyitott/uj/epic-hawking-d0313a.md:1` | Mindkettő valóban nyitott (a #699 nincs a main-en), de az N-F206a tétellistája kihagyja a V9-es 20. és 27. tételt. |
| A3 / A4 / A5 | OK / n. a. | — | A Jel 22:3 tematikus (`elofordulasok.tsv:246`); PaRDeS-tanulmány, nevesített tanító a diffben nincs. |
| A6 / CI | OK (utólag) | — | A zár felszabadulása után: `python eszkozok/ellenorzes/futtat.py --valtozott <a 8 fájl> --diff-alap 5b2d9fe1 --diff-fej 0896aaf5` → kilépési kód 0; E12–E15: 0 találat. Jelzés csak a diffen kívüli fájlokon: E25 (`CLAUDE.md:35`, `MUNKAMENET.md:70,251`), E27 (44, `FELADATOK.md`, `NYITOTT_FELADATOK.md`), E34 (41, `adat/elofordulasok.tsv`, KIRALY-001). A munkafán ekkor már az F206.5 is rajta volt. |
| Ellenőrzőlista 1–5 | OK | — | 7 törölt sor, mind átírás; kulcstartományok hézag nélkül; `adat`, `konkordancia`, `lexikon`, `motivumok`, `MUNKAMENET.md` diffje üres; `.tsv` Δ = 0; merge és végleges szám nincs. |
| Adat-szúrópróba | OK | — | `lekerdez.py scan H0776 --szakasz "1Móz 6:11-13"` → 3; `scan H0127` ugyanott → 0; `scan H0776 --szakasz "Jer 51:46"` → 1; `scan H0779 --szakasz "1Móz 9:25-26"` → 9:25; `scan H1288` → 9:26; `scan H0127` 1Kir 13:34 / 2Kir 17:23 → 1 / 1; `karoli "2Kir 17:23"`: „az ő földéből”; `karoli "Jer 6:7"`: „betegség és vereség van előttem szüntelen”; `kollokacio H2555 H8085` → 4 vers. |

## Az ELTÉRÉS-ek súlyosság szerint

1. A mérési számok ellentmondanak egymásnak (⚑ 13 a szövegben, 11 a táblában; a 12. tételre állított új jelzést a kód nem adhatja); ugyanez a `5a43a57b` commitüzenetében.
2. A „téves riasztás sincs” következtetés nem áll meg; a „hat/hét” ellentmondás.
3. Ütközés a 6. sablonnal (Peshat-mag, alapvonal) — sem a jelentés, sem az N-F206a nem nevezi meg.
4. Proveniencia-sor hiányzik a jelentés futtatásból vett számai mellől.
5. A V11-sor nem követi a menet szabályait.
6. A `proza_allitas.py` korlátai nincsenek dokumentálva.
7. Feszültség a 10. sablon :49 és az 5. szabály között.
8. Hibás besorolás: a 2. tételből hiányzik a (b).
9. Az N-F206a tétellistája hiányos (20., 27.).
10. Üres teszt: `test_ige_nelkul_nem_jelez`.

## Megjegyzések

- A más ágakon lévő fájlokat `git diff <üres fa> <ág> -- <fájl>` paranccsal olvasta; egy ideiglenes fájlt a repón kívül írt (a HAMART-001 word-diffje).
- Ellenőrzés közben az ágra felkerült az F206.5 (`84c7df3b`), ezt nem vizsgálta; futólag: a „Jó” példája a main „a kánon későbbi könyveiben” mondatát idézi, nem a javított szöveget — ez a G4-gyel ütközhet.
