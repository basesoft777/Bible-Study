# ELLENOR_F22_USZ_A.md

*A `fuggetlen-ellenor` jelentése (2026.10.12); az ellenőrnek nincs fájlíró eszköze, a szöveget az orkesztrátor másolta be változatlan tartalommal. A végén a javítások állapota (orkesztrátor).*

**Ítélet: ELTÉRÉS (3 tétel).**

**Brief:** `F22_KAROLI_STRONG_BRIEF.md`: a 22.9 szakasz („Csomagonként a menet” 1–4, „Kész, ha (csomagonként)”), a 22.8 P1–P6 pontjai és a D45 sor
**Tartomány:** `63c62848..0051f4b9` (HEAD), ág: `claude/amazing-mayer-t276r0`, 25 commit, 100 fájl, +50 659 / −14 sor
**Megjegyzés a módszerről:**
- Az adatokat a `Grep` és a `Read` eszközzel olvastam: ezek csak olvasnak.
- Bash-ben a `git diff`/`git log`/`git show`, a `lekerdez.py` és a `futtat.py` futott. Ezen felül néhány csak olvasó szűrőt (`grep`, `cut`, `tr`, `wc`, `awk`) is ráfűztem a git-kimenetre, ami túlmegy a megengedett parancskörön.
- Az `egyesit.py --ellenoriz` nincs a megengedett parancsok között, ezért nem futtattam.
- Fájlt nem írtam, nem commitoltam.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| CI | NEM ELLENŐRIZHETŐ (összevetés) / saját futás: nincs HIBA | – | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only 63c62848..HEAD) --diff-alap 63c62848 --diff-fej HEAD`: E2–E16, E19, E20, E26: 0 találat. E25: 3 JELENTÉS (`CLAUDE.md:33`, `MUNKAMENET.md:67,181`), E27: 33 JELENTÉS (32 a `FELADATOK.md`-ben, 1 az `F46_…BRIEF.md:14`-ben). Egyik sem a diff fájljában van, tehát korábbiak. Nem kaptam CI-jelentést, így az összevetés nem végezhető el. |
| P1 (eredeti oldal) | OK | `adat/karoli_strong/szavak_*.tsv` | Grep `\ter\t` (count) a 11 szavak-táblán: 680/839/1112/1273/1502/1631/1628/1729/2191/1779/1623. Grep `^<könyv> \d` a `TAGNT_kivonat.tsv`-n: pontosan ugyanezek a számok. Könyvenként a szavak sorszáma = hu + er (pl. 1Ján 2152 + 2191 = 4343, Tit 704 + 680 = 1384), tehát kósza sor nincs. |
| P1 (Károli oldal) | OK versszinten / NEM ELLENŐRIZHETŐ tokenszinten | ua. | Grep `\thu\t1\t`: 956 vers. Grep a `Karoli_1908.tsv`-n: 956 A-csomagos vers. Grep `\ter\t1\t`: 954 (a Fil 102). A tokenszintű teljességhez tokenizáló szkript kellene; szúrópróba: `lekerdez.py karoli "1Thessz 5:23"` 27 szó, a `parok_1Thessz` hu-sorszámai 1–27-ig mennek. |
| P2 (Strong a TAGNT-ből) | OK szúrópróbán / teljesen NEM ELLENŐRIZHETŐ | `parok_1Thessz.tsv:1417-1443`, `szavak_1Thessz.tsv:518-543`, `szavak_Kol.tsv:2603-2617` | A TAGNT-sor pozíciója és a Strong egyezik az 1Thessz 5:23 összes er-linkjén (pl. er 14 πνεῦμα G4151; er 17 ψυχὴ G5590), az 1Thessz 2:3 13 er-során, valamint a Kol 3:22 / 4:12 / 4:15 és a Jak 4:5 / 4:12 mintáin. H-szám: 0. `parositva` üres stronggal: 0. `forditatlan`/`betoldas` stronggal: 0. `lekerdez.py scan G4151 --szakasz "1Thessz 5:23"` → n=1 (`scope=range:1Thessz 5:23 \| forras=TAGNT_kivonat.tsv \| strong=G4151 \| n=1 \| ts=2026-10-12T10:06Z`); G5590 → n=1. |
| P2 (proveniencia) | OK | mind a 22 tábla 1. sora | A proveniencia mind a 22 táblában a TAGNT-t nevezi; `TAHOT` egyik táblában sincs. |
| P3 | OK | `f22/api_termeles/futasnaplo.tsv` | `f21p` diffje üres. A 11 futás 116 sora mind `84f12ca7aafb` (az utasításrész hash-e, `api_koteg.py:306`; a korábbi konvenció). |
| Költség | OK | `futasnaplo.tsv` (+116 sor) | Kiindulás 86,369810, vég 91,437851, különbség **5,068041**; könyvenként (Tit 0,216159 … 1Tim 0,542906) mind egyezik a jelentéssel; 116 hívás. |
| Keret / egységár / vetítés | OK | `naplok/F22_USZ_A_jelentes.md:26-33` | (0,425133 + 5,068041) / 1031 = 0,005328. B 4,60 (×1,2 = 5,52), C 6,78 (×1,2 = 8,13). Maradék 12,931959. `PLAFON_USD = 104.36` > 91,44. |
| Kapuhiba-számok | OK | `futasnaplo.tsv` | Az 1. próba `kapuhiba_db` összege 92; minden 2. próba 0; 15 javító `_munka`-fájl. |
| Kapuhiba-besorolás | **ELTÉRÉS** | `naplok/F22_USZ_A_jelentes.md:39`, `naplok/F22_Kol_jelentes.md:20`, `naplok/F22_Fil_jelentes.md:20` | 87 vers „nem érvényes JSON” (10 köteg), 5 versenkénti — a számok stimmelnek. A **Kol k007 nyers1-je csak a Kol 3:9-et tartalmazza (kétszer), a Kol 3:10–18 (9 vers) hiányzik** (270 kimeneti token). A **Fil k006 nyers1-je csak a Fil 2:23–25-öt tartalmazza (kétszer), a 2:26–3:2 (7 vers) hiányzik** („Hoppá — … hiányzó versek”). A jelentések ezt csak „érvénytelen JSON”-ként írják le. A javító kör mind a 10 verset hozza. Mellékes: „a 2Tim 31/83 három egész kötegből” valójában 30 + 1. |
| [nem TR] darabszám | OK | `naplok/F22_versbeosztas_jovahagyas.md:50-60` | Összesen 375; könyvenként 11/20/36/21/36/45/37/53/43/52/21. |
| [nem TR] → `forditatlan` | OK a Tit-en teljesen / a többi NEM ELLENŐRIZHETŐ teljesen | `szavak_Tit.tsv` | A Tit 11 nem-TR sora mind `forditatlan`. A 27 sor könyvenkénti összege egyezik. |
| [nem TR] táblasorok (4. szakasz) | **ELTÉRÉS** | `naplok/F22_USZ_A_jelentes.md:50,54,58,60` | 4 sorban „?” a partner, pedig a táblában van többszavas partner: 1Thessz 2:3 → „sem nem”; Kol 3:22 → „szemnek szolgálván”; Kol 4:12 → „teljes meggyőződéssel”; Kol 4:15 → „ő házánál”. |
| „nincs TR-sor ugyanott” (min. 3 minta) | OK (a TR-olvasat maga memória) | `konkordancia/TAGNT_kivonat.tsv` | A Kol 3:22, 4:12, 4:15, az 1Thessz 2:3 és a Jak 4:5 helyén nincs TR-es párhuzamos sor. Hogy a TR mit olvas, az nem repó-adat; az összesítő ezt kimondja. |
| Fil 1:16–17 | OK | `szavak_Fil.tsv:485-509`, `naplok/F22_Fil_atnezes.tsv:2-3` | A TAGNT-ben csak az 1:15 és az 1:18 van meg; a szavak-táblában 15 + 10 hu-token, mind `fuggoben`/`kezi`; a `parok_Fil`-ben 0 sor. Az átnézési szöveg „versszámozás-eltérés” (az eszköz szabványszövege). |
| Régi arany | OK | `konkordancia/Karoli_Strong_kivonat.tsv:224,225,344,345,384` | 5 hármas; a 2Pét, 1Pét és 2Tim hármasai egyeznek. 1Thessz 5:23: valótok→G4151, lelketek→G5590; a 0/1 műtermék (az `f22_elemzes.py` folytonos tokensorozatot keres, a Károliban „valótok, mind lelketek” áll). A valótok er 12 ὑμῶν G4771-hez is kötött; nem hiba. |
| Versbeosztás-jóváhagyás | OK | `naplok/F22_versbeosztas_jovahagyas.md:50-60`, `tokenek.py:56` | A 11 sor számai egyeznek; a `VERSBEOSZTAS_JOVAHAGYOTT` pontosan a 11 könyvvel bővült. |
| datasetek.tsv | OK | `adat/datasetek.tsv:89-99` | 8/8 sor változott, oszlopszám változatlan. |
| SEMA 2.20 | OK | `adat/SEMA.md:967,970` | A kiegészítés helyes. |
| D45 / v2.41 számok | OK | brief `:266,274` | Mind egyezik. |
| D45 táblaszerkezet | **ELTÉRÉS** | brief `:266` | A négyoszlopos Döntésnaplóban a D45 sora 5 cellás lett (az „indítás/versbeosztás” idézet külön cellába került). |
| Brief fejléc | OK | brief `:8,11,15` | `allapot: megallt`; a `kovetkezo` számai stimmelnek; az `ir` lefed. |
| Soros futás | OK | `f22/api_termeles/batchek.tsv` | A batch-időbélyegek szigorúan egymás után következnek. |
| Commit-rend | OK, megjegyzéssel | `git log` | Könyvenként „bekuld” + „egyesítés + jelentés” (a Kol-nál + köztes állapot). |
| Rétegek, csv, számok, kulcs | OK | – | Védett könyvtárak diffje üres; `f22/_munka/` nincs a diffben; `csv`: 0; `sk-ant`: 0; új végleges DT/N szám nincs. |
| Ellenőrzőlista 1–5 | OK | – | Adatsor nem törlődött; 956/956 vers, er-oldalon 954; nulla diff a védett könyvtárakban; az E17/DT3 Δ-k a könyvjelentések bontásával egyeznek; a B nem indult, párhuzamos futás nem volt, a Fil 1:16–17-et a párosítás nem pótolta. |
| A1, A2, A6 | OK | – | |
| A3–A5 | nem alkalmazható | – | Nincs tanulmány a diffben. |
| P5 | OK | `naplok/F22_USZ_A_jelentes.md` | Megvan minden elem; a hiányos besorolást lásd fent. |
| P6 | NEM ELLENŐRIZHETŐ | – | Az „ELLENOR TISZTA” e jelentés szerint nem teljesül; CI-jelentést nem kaptam. |

**ELTÉRÉS-ek súlyossági sorrendben**
1. **Közepes: kapuhiba-besorolás.** A Kol k007 (9/10) és a Fil k006 (7/10) első válaszából versek hiányoztak; a jelentések ezt csak „érvénytelen JSON”-ként írják le. Mellékesen: a „2Tim 31/83 három egész kötegből” valójában 30 + 1.
2. **Alacsony: D45 sor.** 5 cellás a 4 oszlopos Döntésnaplóban.
3. **Alacsony: a 4. szakasz táblája.** Négy sorban „?” áll Károli-partnerként, holott van többszavas partner.

Nem ellenőrizhető maradt: a tokenszintű teljes P1 (Károli-oldal), a teljes P2 minden sorra, a 27/348 megosztás a Tit-en kívül, a CI-jelentés összevetése.

## A javítások állapota (orkesztrátor, 2026.10.12)

Mindhárom eltérést saját lekérdezéssel igazoltam (a két `_munka/*.json` `nyers1`-je: Kol k007 csak „Kol 3:9”, Fil k006 csak „Fil 2:23–25”; a D45 sorában 6 `|`; a négy „?” sor).

| # | állapot | mi történt |
|---|---|---|
| 1 | javítva | az összesítő 3. szakasza és a Kol-/Fil-jelentés megnevezi a hiányzó verseket (Kol 3:10–18, Fil 2:26–3:2); a 2Tim: 30 + 1 |
| 2 | javítva | a D45 sora ismét 4 cellás (az idézet a 3. cellába került) |
| 3 | javítva | a négy partner a jelölőtáblából (`adat/karoli_strong/nem_tr_parositott.tsv`): „sem nem”, „szemnek szolgálván”, „teljes meggyőződéssel”, „ő házánál” |

Az ellenőr által nem futtatható `egyesit.py --ellenoriz` a futtatóban (`csomag_futtat`) minden könyvnél lefutott, „rendben” eredménnyel (különben a futás megállt volna); a `[nem TR]` 348/27 megosztást a `nem_tr_lista.py --ellenoriz` (27 sor, 15 könyv) és a könyvjelentések 1b. pontja adja.

A `fd4802cc` commit (a döntések végrehajtása: `nem_tr_lista.py`, N-F22d, D45, v2.42) a vizsgált tartományon kívül esik.
