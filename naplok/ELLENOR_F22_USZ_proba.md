# ELLENOR_F22_USZ_proba.md

*A `fuggetlen-ellenor` jelentése (2026.10.12); az ellenőrnek nincs fájlíró eszköze, a szöveget az orkesztrátor másolta be változatlan tartalommal. A végén a javítások állapota (orkesztrátor).*

**Ítélet: ELTÉRÉS (8 tétel).**

- **Brief:** `F22_KAROLI_STRONG_BRIEF.md`: a 22.8 szakasz (1–8. lépés, P1–P6) és a D44 sor.
- **Tartomány:** `56f8dbf4..3d2d34e6` (ág: `claude/amazing-mayer-t276r0`), 9 commit, 39 fájl, +4423/−23 sor.
- **Kapott CI-jelentés:** nem kaptam, ezért az összevetés NEM ELLENŐRIZHETŐ. Az alábbi CI-sor a saját futtatásom eredménye.

**A megengedett parancskör megsértése (tisztán olvasó lépések, fájlt nem írtak).** Több helyen `git show`-t, illetve a git-kimenetre csövezett `grep`/`cut`/`awk`/`sed`/`wc`/`head` parancsot futtattam. Ezek kívül esnek a megengedett körön. A hívó kérte, de a szerepem szerint **nem** futtattam: `egyesit.py --ellenoriz`, `--onteszt`, az ÓSZ-táblák újraépítése (ez fájlt írna) és az `sha256sum`. Ezeket a pontokat statikus kódolvasással és `Grep`-pel váltottam ki, és így jelölöm.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| CI (saját futtatás) | OK (részben NEM ELLENŐRIZHETŐ) | — | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 56f8dbf4..3d2d34e6) --diff-alap 56f8dbf4 --diff-fej 3d2d34e6`. E2–E20: 0 találat. E25: 3 találat (CLAUDE.md, MUNKAMENET.md, a diffen kívül). E27: 32 JELENTES/FIGYELMEZTETES, a kimenet „... es tovabbi 29”-nél levágva; a látható 3 a diffen kívüli. HIBA szintű sor nincs. A levágott 29 sort nem láttam. |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | — | Nem kaptam CI-jelentést, amellyel összevethetném. |
| P1: tokenek egyszer | OK részben / NEM ELLENŐRIZHETŐ (az `--ellenoriz` futása) | `adat/karoli_strong/szavak_*.tsv` | `Grep ^[^\t#]+\ter\t` (count): Filem 349, 2Jan 249, 3Jan 210, Jud 468. Ez egyezik a `Grep ^<könyv> ` számával a TAGNT_kivonat.tsv-ben (349/249/210/468). `\thu\t`: 354/236/249/486. Fájlsor = 2 + er + hu mind a négy táblában (705/487/461/956). A (vers, oldal, sorszám) egyediségét és a `--ellenoriz` „rendben” kimenetét nem futtathattam. A hu-szám Filemnél (354) és Júdnál (486) eggyel több a brief szóközös számánál (353, 485); ez a tokenizálóból adódik, nem hiba. |
| P2: strong a TAGNT-ből | OK (szúrópróba) | `parok_Jud.tsv:153-174`, `szavak_3Jan.tsv:440-449` | `Grep ^Júd 1:9\t` a parok_Jud-ban és a TAGNT-ben: mind a 22 linknél a strong és az er_szo pozíció szerint egyezik. Ugyanígy a 3Ján 1:14 mind a 10 er-sora. `python eszkozok/lekerdez.py scan G1252 --szakasz "Júd 1:1-25"`: Júd 1:9, Júd 1:22, n=2 (`proveniencia: scope=range:Júd 1:1-25 \| forras=TAGNT_kivonat.tsv \| strong=G1252 \| n=2 \| ts=2026-10-12T08:09Z`). `scan G2112 --szakasz "3Ján 1:14"`: n=1. Modell által írt Strong-szám nincs: `Grep \bG\d{3,4}\b` a `f22/valaszok/sonnet/{Filem,2Jan,3Jan,Jud}.jsonl`-ben 0 találat. A teljes gépi ellenőrzést nem futtattam. |
| P2: proveniencia | OK | `szavak_3Jan.tsv:1` | A fejléc: `forras=…, konkordancia/TAGNT_kivonat.tsv, …`, valamint „a strong a TAGNT-ből”. |
| P2: az ÓSZ-kimenet változatlan | OK (statikusan) / NEM ELLENŐRIZHETŐ (újraépítés) | `eszkozok/karoli_strong/egyesit.py:55-63, 261-274, 337-349` | `git diff … -- eszkozok/`: ÓSZ-könyvre `eredeti_kivonat` a ('TAHOT_kivonat.tsv','TAHOT','a TAHOT-ból','a TAHOT-ban') értéket adja. Behelyettesítve minden kiírt sztring (proveniencia, átnézés) karakterre a régi. A `forras` lista hossza (a `>4` feltétel) nem változik. A TAGNT minden sora a 27 ÚSZ-könyvé: `Grep ^(Mt\|…\|Jel) \d+:\d+\t` 141 746 sor, `Grep ^` 141 747 sor (1 a fejléc). Ezért ÓSZ-könyv nem kerülhet a TAGNT-ágra. A Sir/Mal/Hós újraépítése fájlt írna, nem futtattam. |
| P2: a 2Móz/Jób fejléc-eltérése régebbi | OK (statikusan) | `parok_2Moz.tsv:1`, `parok_Job.tsv:1` | Mindkét fejléc `forras`-a tartalmazza az `f22/versmegfeleltetes.tsv`-t, a Jóbé a `_kezi.tsv`-t is. `Grep Móz\|Jób` az `f22/versmegfeleltetes*.tsv`-ben: nincs sor, csak `Ján 7:53` és `3Ján 1:15`. A feltételes ág (`egyesit.py:330-336`) a diffben nem változott, tehát az eltérés a módosítás nélkül is fennáll. Mindkét tábla utoljára a main-en változott (`git log -1 -- adat/karoli_strong/parok_2Moz.tsv`: 4435a173). |
| P2: `--onteszt` | NEM ELLENŐRIZHETŐ | `egyesit.py:465-468` | Nem futtattam. Az önteszt üzenete („strong nem a TAHOT-ból”) és a docstring 8. sora még csak a TAHOT-ot nevezi meg (kozmetikai). |
| P3: prompt_v3 | OK (változatlanság) / NEM ELLENŐRIZHETŐ (hash) | `f21p/prompt_v3.sha256:1` | `git diff --stat 56f8dbf4..3d2d34e6 -- f21p/`: üres. A .sha256 tartalma `5937e6abac58…`, egyezik a jelentésben állított előtaggal. Az SHA-256-ot nem számolhattam újra. A futásnapló `prompt_sha256_12=84f12ca7aafb` mind a 12 új sorban azonos a korábbi Sir-sorokéval. |
| P4: [nem TR] 9/5/9/28 | OK | `konkordancia/TAGNT_kivonat.tsv:118485-131572` | A négy könyv sorai: `Grep ^(Filem\|2Ján\|3Ján\|Júd) ` = 1276. Ebből a kritikai mezőben TR-t tartalmazó (`…([^\t]*\t){6}[^\t]*TR`) 1225, a különbség 51. Listázva: Filem 9, 2Ján 5, 3Ján 9, Júd 28. A `TR»1` a TR-be számít. |
| P4: mind `forditatlan` | OK | `szavak_*.tsv` (pl. `szavak_Jud.tsv:933-948`) | `Grep \ter\t\d+\t[^\t]*\tforditatlan`: az 51 nem-TR tokenből mindegyik `forditatlan`, versenként és alak szerint egyeztetve (pl. Júd 1:25 er 6–11 és 18–21). A forditatlan er-sorok száma 50/34/30/80, egyezik a könyvjelentésekkel. |
| Költség (futásnapló) | OK | `f22/api_termeles/futasnaplo.tsv:1670-1681` | Filem 0,041061+0,039959+0,018903 = 0,099923. 2Ján 0,008427+0,056700+0,018058 = 0,083185. 3Ján 0,053519+0,022862 = 0,076381. Júd 0,008562+0,065776+0,064201+0,027105 = 0,165644. Összesen 0,425133, 12 hívás. A futó összeg 85,944677-ről 86,369810-re nő, a maradék 23,6302. USD/vers: 0,0040 / 0,0064 / 0,0055 (14 versre) / 0,0066, összesen 0,005521. A tokenösszegek egyeznek. |
| Kapuhiba | OK | `futasnaplo.tsv` `kapuhiba_db` | 2Jan k002 1. próba: 3, ok=nem. Jud k003 1. próba: 5, ok=nem. Minden más sor: 0. Első próbára 8/77 = 10,4%, végleg 0. A batch-sorok (`batchek.tsv`, 6 új sor) egyeznek a könyvjelentésekkel. |
| Javító körök oka | ELTÉRÉS (alacsony) | `naplok/F22_USZ_proba_jelentes.md:36`; `f22/api_termeles/high/_munka/Jud_k003.json` | A jelentés szerint „a JSON-tömb után további szöveg” volt. Valójában egyik válasz sem JSON-tömb, hanem tömb nélküli objektumok, köztük próza. A Júd k003 nyers válasza csak a Júd 1:21-et tartalmazza (kétszer, „Ellenőrzés után javított változat” közbeszúrással); a Júd 1:22–25 hiányzik belőle. A hiba tehát részben tartalmi hiány is. A „tartalmi kapuhiba 0” állítás ezekre a versekre nem mérhető. |
| Vetítés | OK / NEM ELLENŐRIZHETŐ (szószám) | `F22_USZ_proba_jelentes.md:17-24, 71` | `Grep` a 27 ÚSZ-könyvnévre a Karoli_1908.tsv-ben: 7954. Mt+Mk+Luk+Ján+ApCsel: 4785. 7954−4785−78 = 3091. 7954×0,0055212 = 43,92; 7876× = 43,49; 3091× = 17,07; 4785× = 26,42; 23,6302/0,0055212 = 4280. Szóarányosan 0,425133/1311 × 142 048 = 46,06. A 142 048-as és az 1323-as szószámot nem tudtam újraszámolni. |
| 3Ján 1:15 | OK | `szavak_3Jan.tsv:450-461`; `naplok/F22_3Jan_atnezes.tsv:2` | `Grep ^3Ján 1:1[45]\t` a TAGNT-ben: csak az 1:14 (10 sor, az utolsó `λαλήσομεν.`). `lekerdez.py karoli "3Ján 1:15"`: 12 szó (`proveniencia: scope=range:3Ján 1:15 \| forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv \| n=1 \| ts=2026-10-12T08:06Z`). A szavak táblában 12 hu-sor `fuggoben`. A parok_3Jan-ban 0 sor. Az átnézési fájlban 1 adatsor. A `f22/minta_3Jan.tsv`-ben 14 vers, az 1:15 nincs benne. |
| 3Ján 1:15 átnézési címke | ELTÉRÉS (alacsony) | `naplok/F22_3Jan_atnezes.tsv:2` | Az adatsor szövege „versszámozás-eltérés”. A brief és az N-F22b szerint viszont a kivonat hiányáról van szó. A jelentés ezt kimondja, de a táblában a téves ok marad. |
| D44 / brief: „3Ján 1:15 `kezi`” | ELTÉRÉS (alacsony) | brief D44, `kovetkezo`; `naplok/F22_versbeosztas_jovahagyas.md` | A táblában `allapot=fuggoben` áll, a `bizonyossag=kezi`; a „`kezi`” megnevezés az állapotoszlopra értve pontatlan. |
| N-F22b: 9 + 3 kulcs | OK | `NYITOTT_FELADATOK.md:55` | A csak-Károli 9 kulcs a TAGNT-ben nincs meg; a csak-TAGNT 3 kulcs a Károliban nincs meg. 7954−9+3 = 7948. |
| N-F22b: összevont Károli-sorok | ELTÉRÉS (közepes) | `NYITOTT_FELADATOK.md:55`; `konkordancia/Karoli_1908.tsv:28490` | A Róm 3:30 és a Róm 8:38 valóban a következő vers szövegét is hordozza. Ugyanez áll az **1Kor 3:22**-re is („… Ti pedig Krisztusé, Krisztus pedig Istené.” = TAGNT 1Kor 3:23). Az N-F22b ezt nem nevezi meg. |
| N-F22b: azonosító-ütközés | ELTÉRÉS (közepes) | `NYITOTT_FELADATOK.md:55` és `:586` | Két különböző tétel viseli ugyanazt a helyőrzőt: az 55. sor az új ÚSZ-verskulcs tétel, az 586. sor a régi, lezárt „Gemini-újrapróba” tétel (`git log -S 'N-F22b'`: 7f344968). |
| P5: a 7. pont öt eleme | OK | `F22_USZ_proba_jelentes.md` 1–5. szakasz | Mind az öt elem megvan. |
| P6/K9: datasetek | OK részben | `adat/datasetek.tsv:89` és még 7 sor | 8 sor változott, mindben egyetlen csere; az oszlopszám 7 előtte és utána is. |
| P6/K9: jelentéslista | ELTÉRÉS (alacsony) | `adat/datasetek.tsv:89`; `adat/SEMA.md:970` | A négy új jelentést egyik fájl sem nevezi meg, eltérően az összes ÓSZ-könyvtől. |
| SEMA 2.20 | OK | `adat/SEMA.md:970` | A bekezdés tartalma helyes. |
| Brief 2. lépés: külön commit | ELTÉRÉS (alacsony) | commit c5dc0b21 | Az `egyesit.py` javítása ugyanabban a commitban ment be, mint a minták és a száraz próba; a brief 2. lépése „külön commit”-ot ír elő. |
| Brief 4. lépés: jóváhagyás utáni bővítés | OK | commit 250bd900 | A `tokenek.py` bővítése a jóváhagyási naplóval egy commitban, a minták után. A jóváhagyás ténye (chat) NEM ELLENŐRIZHETŐ. |
| Futó összeg teljessége | ELTÉRÉS (alacsony, jelezve) | `F22_USZ_proba_jelentes.md:65` | A szinkron próbahívás költsége nincs a futásnaplóban; a 86,3698 / 23,6302 USD nem a teljes költés. |
| Rétegek: védett könyvtárak | OK | — | `f21p/ konkordancia/ lexikon/ generalt_proba/ motivumlog/`: üres diff. Generált fájl nincs a diffben. `f22/_munka/` nem került be; a `f22/api_termeles/high/_munka/` 2 fájlja precedens szerinti. |
| csv modul | OK | — | 0 találat. |
| Végleges DT/N szám | OK | — | Új végleges szám nincs. |
| API-kulcs | OK | — | `sk-ant-`: 0. |
| ⛔ (22.8 8. lépés) | OK / NEM ELLENŐRIZHETŐ | — | Csak a négy próbakönyv táblái kerültek be. |
| E17/DT3: sorszám-Δ | OK | `adat/` | Új táblák: `parok_Filem` +340, `parok_2Jan` +236, `parok_3Jan` +217, `parok_Jud` +426, `szavak_Filem` +703, `szavak_2Jan` +485, `szavak_3Jan` +459, `szavak_Jud` +954; `datasetek.tsv` Δ0. |
| Kiszűrt/törölt sorok | OK | — | Adattáblából sor nem törlődött. |
| Kulcs-lefedettség | OK | — | 78 Károli-versből 77-nek van er-sora; a hiányzó a 3Ján 1:15, dokumentált. |
| A1 | OK | — | A számok szkript- vagy futásnapló-eredetűek. |
| A2 | OK | — | Az N-F22b valóban nyitott. |
| A3–A6 | nem értelmezett | — | Nincs tanulmány és értelmező próza. |

**ELTÉRÉS-ek súlyossági sorrendben**

1. N-F22b azonosító-ütközés (`NYITOTT_FELADATOK.md:55` és `:586`).
2. Hiányos N-F22b-felsorolás: az 1Kor 3:22 hiányzik.
3. Pontatlan javítókör-leírás: a Júd k003 válaszából 4 vers (1:22–25) hiányzott.
4. Hiányzó jelentés-hivatkozások a `datasetek.tsv`-ben és a SEMA-ban.
5. Commit-szerkezet: a 2. lépés kódigazítása nem külön commitban.
6. Téves ok az átnézési adatsorban (3Ján 1:15: „versszámozás-eltérés”).
7. „kezi” vs. „fuggoben” megnevezés.
8. Hiányos futásnapló (a szinkron próbahívás).

**Amit a szerepkorlát miatt nem futtattam** (NEM ELLENŐRIZHETŐ): `egyesit.py --ellenoriz` és `--onteszt`, a Sir/Mal/Hós újraépítése, a prompt_v3 SHA-256-ja, a 142 048-as és az 1323-as szószám.

## A javítások állapota (orkesztrátor, 2026.10.12)

Mind a nyolc eltérést saját lekérdezéssel is igazoltam (a `NYITOTT_FELADATOK.md` 55. és 586. sora; a `Karoli_1908.tsv` 1Kor 3:22 sora; a két `_munka/*.json` nyers válasza; a `datasetek.tsv` és a `SEMA.md` jelentéslistája).

| # | állapot | mi történt |
|---|---|---|
| 1 | javítva | az új tétel helyőrzője **N-F22c** (a `NYITOTT_FELADATOK.md`, a brief, a SEMA, a jóváhagyási napló és a jelentések minden új hivatkozásában); a régi, lezárt N-F22b változatlan |
| 2 | javítva | az N-F22c felsorolja az 1Kor 3:22-t is (a csak-TAGNT 3 kulcs éppen a három összevont Károli-vers párja) |
| 3 | javítva | az összesítő és a 2Ján-/Júd-jelentés leírja a tömb nélküli objektumokat és a Júd 1:22–25 hiányát; a „tartalmi kapuhiba” első próbára e két kötegre nem mérhetőként áll |
| 4 | javítva | a négy könyvjelentés és az összesítő a `datasetek.tsv` 4 sorában és a SEMA 2.20 jelentéslistájában |
| 5 | dokumentálva | a pusholt ág története nem íródik át; az összesítő 6. szakasza rögzíti |
| 6 | dokumentálva | az átnézési címke az `egyesit.py` általános szövege; a megkülönböztetés kódváltozás volna; az összesítő és a 3Ján-jelentés kimondja a valódi okot |
| 7 | javítva | a brief (`kovetkezo`, D44, 22.8 4. lépés) és a jóváhagyási napló: „`fuggoben` állapotú, `kezi` bizonyosságú” |
| 8 | dokumentálva | az összesítő megnevezi a hiányzó költséget (kb. 0,00008 USD) |

Az ellenőr által nem futtatható pontokat az orkesztrátor futtatta (a menet közben, l. a könyvjelentések 1a. pontját és az összesítő 6. szakaszát): `egyesit.py --ellenoriz` mind a négy könyvre „rendben”; `egyesit.py --onteszt` „rendben”; Sir, Mal, Hós újraépítve 0 eltéréssel; `sha256sum f21p/prompt_v3.md` = `5937e6ab…`, egyezik.
