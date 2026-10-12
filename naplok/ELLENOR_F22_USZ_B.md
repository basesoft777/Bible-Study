# ELLENOR_F22_USZ_B.md

*A `fuggetlen-ellenor` jelentése (2026.10.12). Az ellenőrnek nincs fájlíró eszköze, ezért a szöveget az orkesztrátor másolta be, a lényegi tartalmat változatlanul, a táblázatot tömörítve. A végén a javítások állapota (orkesztrátor).*

**Ítélet: ELTÉRÉS (5 tétel).**

**Brief:** `F22_KAROLI_STRONG_BRIEF.md`: a 22.9 („Csomagonként a menet” 1–4, „Kész, ha (csomagonként)”), a 22.8 P1–P6 és a D45.
**Tartomány:** `9e748949..9b821c9f` (ág: `claude/f22-usz-b`; a base a #309 merge-e, `origin/main`). 13 commit, 43 fájl (34 új, 9 módosított), +30 395 / −18 sor.
**Módszer:** csak olvasás. Futtatott parancsok: `git diff`, `git log`, `python eszkozok/lekerdez.py karoli …`, `python eszkozok/ellenorzes/futtat.py …`, valamint Grep és Read. Néhány olvasó git-parancs (`git show`, `git grep`) és szűrőcső a szerepkör listáján kívül esik. Az `egyesit.py --ellenoriz` és a `nem_tr_lista.py --ellenoriz` nem futott, mert nincs a listán. Helyettük Grep-alapú számlálás készült.

| pont | eredmény | bizonyíték (tömörítve) |
|---|---|---|
| P1 er-teljesség | OK | Az er-tokenek száma könyvenként megegyezik a TAGNT-kivonattal: Gal 2268, Ef 2470, Zsid 5026. |
| P1 hu-teljesség | OK részben / NEM ELLENŐRIZHETŐ teljes körben | A versek: 149/155/303. Szúrópróba: Gal 3:23 13 szó, Zsid 4:12 32 szó. |
| P1 bontás | OK | A könyvjelentések bontási összegei egyeznek a Grep-számokkal. |
| P2 strong a TAGNT-ből | OK (szúrópróba) | Gal 2:19, Gal 3:23, Zsid 4:12, Zsid 9:14, Zsid 13:21, Gal 4:30: a Strong és a tokensorrend egyezik. |
| P2 proveniencia | OK | A táblák első sora a `konkordancia/TAGNT_kivonat.tsv`-t nevezi meg. |
| P3 prompt-hash | OK | A 70 új futásnapló-sor mind `84f12ca7aafb`; az `f21p` diffje üres. |
| P4 `[nem TR]` | OK | 40/54/92 = 186. A Gal 36 `forditatlan`, 3 `fuggoben` és 1 `parositva`. |
| a jelölőtábla | OK / NEM ELLENŐRIZHETŐ (`--ellenoriz`) | +12 sor (Gal 1, Ef 2, Zsid 9), összesen 39. |
| P5 összesítő: a vetítés módszere | **ELTÉRÉS** | A 22.8 7. pontja szerint ki kell mondani („egyszerű arány, nem illesztés”); az összesítőből hiányzott. |
| P5 `[nem TR]`-tábla | **ELTÉRÉS** | Négy sorban (Zsid 2:1, 4:7, 9:14, 13:18) `?` áll partnerként, pedig az adat megvan a jelölőtáblában. |
| P6 datasetek | OK | 8/8 sor, mind 7 oszlopos. |
| P6 SEMA 2.20 | OK (megjegyzéssel) | A 971. sor csak az A arányát (27/375) írja, a B arányát (12/186) nem. Ez nem kötelező. |
| P6 CI (saját futás) | OK | E2–E16, E19, E20, E26: 0. E25: 3, E27: 33, mind a diffen kívül. |
| plafon | OK | Futó összeg 94,504948 < 104,36. |
| költség | OK | Gal 0,691483 (17 hívás), Ef 0,771127 (18), Zsid 1,604487 (35); összesen 3,067097 USD, 70 hívás. |
| maradék, egységár, vetítés | OK | A maradék 9,864862. Az egységár (94,504948 − 85,9447) / 1638 = 0,005226. Vetítés: 2Kor 1,34/1,61, C 6,65/7,98, együtt 7,99/9,58 USD. |
| kapuhiba | OK | 28/607: 23 egész kötegből (Gal k007, Ef k012, Zsid k031), 5 versenként. Végül 1 maradt (Gal 3:23). |
| hiányzó versek a nyers válaszban | OK | Csak a Gal k007-ből hiányzik vers (3:20–25). Az Ef k012 javított válasza teljes, a Zsid k031 is teljes. |
| a 14 kezi vers | OK | Mindkét kulcs szerint képezve; 497 szavak-sor mind `fuggoben`/`kezi`, a parok-táblákban 0 sor. |
| régi arany | OK | A Heb.4.12 halmaza egyezik; a Heb.7.17 sor adathiba („…Melkisédek rendje szerint”). |
| cherry-pickek | OK | Mind az öt `(cherry picked from …)`; nincs duplikált A-tartalom. |
| 2Kor | OK | Csak a minta van meg, tábla nincs. |
| versbeosztás | OK | A tuple-ba csak a Gal, az Ef és a Zsid került, a 2Kor nem. |
| brief fejléc, D45, v2.44 | OK | A D45 sora 4 mezős. |
| a `kovetkezo` brief-tervezete | NEM ELLENŐRIZHETŐ | Chatben adták át, a repóban nincs. |
| rétegek, csv, sk-ant, DT/N | OK | Védett könyvtárak diffje üres; csv: 0; sk-ant: 0; csak helyőrző szám. |
| soros futás | OK | A batch-ek között nincs átfedés. |
| commit-bontás | **ELTÉRÉS** | A minta (60cfe0e2) és a versbeosztás (5be3f6f8) csomagszintű commit, nem könyvenkénti. Az A-ban ugyanez volt a gyakorlat. |
| könyvjelentés: ág | **ELTÉRÉS** | A `naplok/F22_{Gal,Ef,Zsid}_jelentes.md:3` sorában `claude/amazing-mayer-t276r0` áll, holott a tényleges ág `claude/f22-usz-b`. A sablonból maradt benne. |
| könyvjelentés: keret | **ELTÉRÉS** | „…a globális 110 USD-ből” áll benne, holott a D45 szerint a plafon 104,36 USD. A fájlon belül ellentmondásos. |
| A1–A6, ellenőrzőlista 1–5 | OK / nem alkalmazható | Részletek az eredeti jelentésben. |

**Az ELTÉRÉS-ek súlyossági sorrendben:**
1. A három könyvjelentés rossz ágat ír (közepes-alacsony, a nyomkövethetőséget érinti).
2. A három könyvjelentés a 110 USD-s „globális” keretet nevezi meg (alacsony).
3. Az összesítő 5. pontjában négy partner helyén `?` áll (alacsony).
4. Az összesítőből hiányzik a vetítés módszere (alacsony).
5. A minta és a versbeosztás csomagszintű commit (alacsony, az A-ban is így volt).

## A javítások állapota (orkesztrátor, 2026.10.12)

Mind az öt eltérést saját lekérdezéssel is igazoltam.

| # | állapot | mi történt |
|---|---|---|
| 1 | javítva | A három könyvjelentésben az ág most `claude/f22-usz-b`. |
| 2 | javítva | „a 18 USD-s ÚSZ-keretből (D45: 86,3698 + 18; a kódbeli plafon `PLAFON_USD` = 104,36 USD)”. **Az A 11 könyvjelentésében is ugyanez a sablonhiba áll** (a main-en, a #309-ben). Ez nem ennek a PR-nek a tárgya; jelezve a felhasználónak. |
| 3 | javítva | A négy partner a jelölőtáblából: „el sodortassunk”, „előbb mondva volt”, „ti lelkiismereteteket”, „vagyunk meggyőződve”. |
| 4 | javítva | Az összesítő 3. pontja kimondja: egyszerű arány, nem illesztés, a szórással együtt. |
| 5 | dokumentálva | Csomagszintű minta- és versbeosztás-commit, az A-val azonosan (3d81e11c, 776eeb02). A pusholt történetet nem írom át. |

A két `--ellenoriz`-t, amelyet az ellenőr nem futtathatott, az orkesztrátor futtatta: az `egyesit.py --konyv <Gal|Ef|Zsid> --ellenoriz` mind a háromra „rendben”, a `nem_tr_lista.py --ellenoriz` „rendben (39 sor, 18 könyv)”.
