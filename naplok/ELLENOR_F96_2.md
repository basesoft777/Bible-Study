ELTÉRÉS: 2 tétel

# ELLENOR_F96_2 — független újraellenőrzés (`/elteres`, 1. javítókör)

- **Brief:** `F96_KAROLI_MODERN_BRIEF.md` (FELADATOK #96, KAROLI_MODERN)
- **Tartomány:** `b8334a64..207aafc2`, ág `ccr-a680d019-39s73e`, 6 commit: `e9f85589`, `d4660006`, `c700f16b`, `ccc555b4`, `575df622`, `207aafc2`
- **Bemenet:** `naplok/ELLENOR_F96.md` 4. kör (5 ELTÉRÉS, a felhasználó mind az ötöt `mechanikus`-nak hagyta jóvá). Külön CI-jelentést nem kaptam, ezért csak a saját futtatásom áll a táblában.
- **Fájlírás:** ebben a környezetben nincs írási eszközöm, és a Bash a szerepem szerint csak olvas. A jelentést a hívónak kell `naplok/ELLENOR_F96_2.md` néven mentenie.

## 0. Modell-ellenőrzés
- A tényleges modellem `claude-opus-5-5`, a subagent-fájl `model` mezője `opus`: egyezik.
- A diff `modell` mezői a tényleges modellt mutatják: az `igealak_llm_kor3/4/5.tsv:1` fejlécében `modell=claude-opus-5-5`, a napló 15. szakasza szerint a végrehajtó is `claude-opus-5-5` volt.
- A hívásnaplók (`*_hivasok.jsonl`) a tartományban nem változtak: nincsenek a `git diff --stat b8334a64..207aafc2` kimenetében.

## Táblázat

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 4. kör 1. — `ek_E1_T3` a Préd 2-ben | OK | `adat/karoli_modern/karoli_modern_versek.tsv:17404`, `:17405`, `:17408`; `karoli_modern.tsv:333437`, `:333440`, `:333451`, `:333492` | Grep `^Préd 2:[4-9]\t` a versek-táblán és a `konkordancia/Karoli_1908.tsv`-n. Most: 2:5 „építettem magamnak … ültettem magamnak”, 2:6 „Csináltam … ültettem beléjük”, 2:9 „Gyűjtöttem magamnak … szereztem”. Mind a 4 token `ek_E1_T3`, E/1, egy versen belül sincs keveredő személy. |
| 1. — új hiba a *magam-* E/1 fordításból | OK (0 hamis találat) | `eszkozok/karoli_modern/igealak.py:146-153`, `:819-833` | `git diff -U0 … karoli_modern_versek.tsv`: a tartományban csak a Préd 2:5/2:6/2:9 tokenjei fordultak E/1-re, más T/3 nem lett E/1. Grep `t[éá]k magam\|magam\w*\b[^.;:!?]{0,60}\w+tt[ae]m\b` a versek-táblán: nincs *-ték/-ták* T/3 alak a *magam-* névmás mellett, és a 31 találat között hamis E/1 sincs. `ek_E1_T3` darabszám (Grep count, `karoli_modern.tsv`): 694, egyezik a 15.1-gyel (692 + 2). A logika ellenőrizve: `ültették`[:-2] + `em` = `ültettem`; `-ták` → `-tam`. |
| 1. — N-F96f státusz (A2) | OK | `F96_KAROLI_MODERN_BRIEF.md:112` | A státusz „részben megoldva”. A 3 nyitott maradék valóban nyitott: Grep `^(1Móz 39:15\|Dán 7:16\|Ez 22:30)\t\d+\t(kezdék\|kérék\|keresék)\t` → `karoli_modern.tsv:22280` *kezdték*, `:410546` *keresték*, `:431542` *kérték*, mind `ek_E1_T3`. |
| 4. kör 2. — `nevelo_utan` névmási *az* után | OK | `igealak.py:563-574`; `karoli_modern.tsv` (21 sor) | `git diff -U0 … karoli_modern.tsv`: 27 token modern alakja változott (26 `nevelo_utan` + Dán 8:22 *letöretett*), mind helyes igealak a versében (*az monda → mondta* ×14, *mondá* ×2, *felele* ×2, *fogada* ×2, *szűle*, *szűlé*, *beméne*, *méne*, *jöve*, *felkelvén* ×2, *letöretteték*). 1908-as szöveg: Grep a `Karoli_1908.tsv`-n (1Móz 4:25, 25:2, Dán 8:22 stb.). A maradék Grep `\tnevelo_utan$`-szal 21 token: 14 névszó (*tevék* ×4, *küldöttek* ×3, *megmaradott(ak)* ×5, *megfáradott* ×2) és 7 kihagyás (*elfuta*, *elbeszélé*, *esék*, *elküldé*, *eljő* ×2, Jel 6:1 *egy monda*). Ez pontosan a 15.2 listája; 26 + 5 + 2 + 14 = 47, egyezik a 4. kör számával. Az S0072 *felele*: 1Móz 22:1 és 1Kir 13:16 most *felelt*. |
| 2. — új hiba az *az* + mássalhangzós szabályból | OK (0 hamis találat) | `karoli_modern.tsv` diff | A tartományban a szabály 39 sort érint, mindegyik a diffben látszik. A 27 alakváltozás mind ige. A 12 csak címkét kapott sor a modern alakot nem változtatja: 7 korábbi `token_opus` sor, valamint *vigye*, *vette*, *tőled*, *leszek*, *lenne*. Az utóbbi 5 az 1908 szerint (`Karoli_1908.tsv:2772`, `:6798`, `:7740`, `:18582`, `:19140`) mind névmási „az” + mássalhangzós szó. Az „a” + magánhangzós ágon egy token sem változott. |
| 2. — a napló leírása a 7 `token_opus` sorról | **ELTÉRÉS** (kisebb) | `naplok/KAROLI_MODERN_meres.md` 15.2, a „felnövekedék, … bevádoltaték” felsorolás | A napló szerint „most a .2 szabálya cseréli ugyanarra az alakra”. A táblában a címke `…+tobbseg:szabaly+sonnet+opus`, a Luk 16:1-nél `…+tobbseg:sonnet+opus`, szabály nélkül. Ez a DT-F96l többségi ága, nem a .2 szabálya (`git diff -U0 … igealak_tokenek.tsv`). A `token_opus` 205 → 198 száma helyes: Grep count `\ttoken_opus$` 198. |
| 4. kör 3. — `lonek_lo` szóhatárral | OK | `igealak.py:155-159`, `:734`; `karoli_modern.tsv:594312`, `:229554` | Grep `\tlőnek\t` a `karoli_modern.tsv`-n: 42 token. 41 `lettek`/`lon`, a Jel 11:19 is. 1 `lonek_lo` (1Krón 12:2 *lőttek*). Grep `(^\|[^\w…])[Ll]őnek($\|[^\w…])` a `Karoli_1908.tsv`-n: a 42 vers közül csak az 1Krón 12:2 a *lő* ige („nyíllal lőnek vala”). A szűkítés nem okozott hamis *lettek*-et. |
| 4. kör 4. — `ts=` és kör-címke | OK | `regies_szken.tsv:1`, `regies_szken_kor4.tsv:1`, `regies_szken_kor5.tsv:1`, `igealak_tokenek.tsv:1`, `igealak_alakok.tsv:1`, `igealak_minta.tsv:1`, `igealak_minta2.tsv:1`, `igealak_llm_kor3/4/5.tsv:1` | Grep `^# GENERÁLT.*\| ts=` → 12 fájl; Grep `forras=…scope=` → 10 fájl. A `regies_szken_kor4.tsv:1` címkéje most „--kor 4 (F96.3, 4. kör: DT-F96r, 2. opció …)”. Az LLM-táblákban `futas_ts` = 08:31Z / 10:09Z / 10:42Z. |
| 4. — a szken- és LLM-táblák a fejlécen kívül változatlanok | OK | ugyanez a 9 tábla | `git diff -U0 b8334a64..207aafc2 -- <9 tábla>`: mindegyiknél egyetlen hunk, `@@ -1 +1 @@`. `git diff --numstat`: mind 1/1. |
| 4. — a napló a `karoli_modern.py` `ts=`-éről | **ELTÉRÉS** | `naplok/KAROLI_MODERN_meres.md` 15.4 („Nem változott: a `karoli_modern.py` saját fejléce (a `ts=` itt sincs …)”) és 15.6 „Nyitva marad” 4. pont | Hamis nyitott tétel (A2). Grep `ts=` → `eszkozok/karoli_modern/karoli_modern.py:166` `… \| ts=%s\n`. Grep `\| ts=…` → `karoli_modern.tsv:1` és `karoli_modern_versek.tsv:1` `ts=2026-10-25T12:10Z`. A javítókör előtti fejlécben is ott volt: `ts=2026-10-25T10:45Z` (`git diff -U0 … karoli_modern_versek.tsv`, „−” sor). |
| 4. kör 5. — E17-bontás (`igealak_tokenek`) | OK | napló 15.5 | Az új sorok összege: 690 + 162 + 131 + 41 + 29 + 12 + 11 + 7 + 1 = 1 084. A módosult sorok: 398 + 281 = 679. Táblán (Grep count, `igealak_tokenek.tsv`): fájlsor 67 687 = 67 685 + 2 fejléc; `kor3:szabaly\+opus` 690; `kor4:szabaly\+opus` 184 = 162 + 22; `kor5:token_opus\+meglevo` 198 = 131 + 67; `kor5_token_opus:` 105 = 41 + 64 (a 4. körben 106; a Dán 8:22 jelöltje kiesett, a diff mutatja); `opus_tanusitott` 58 = 29 + 7 + 22. A tartomány 44 módosult sora (4 + 39 + 1) = numstat 45 − 1 fejléc. Az 1 084 / 679 kulcsonkénti összevetése nem futtatható: NEM ELLENŐRIZHETŐ, a részösszegek egyeznek. |
| napló: változó token és vers | OK | napló 15.2, 15.3, 15.6 | Grep `\tigen$` a versek-táblán: 21 621; az 1Kir 13:16 most `nem` → `igen`. A változó tokenek száma 50 491 → 50 517 (+26). A diffből levezetve: 27 alakváltozás a 15.2-ből, ebből 2 (*szűle*, *szűlé*) már a .1-ben is eltért, ez 25; ehhez jön 1 a 15.3-ból. A Préd-tokenek már korábban is eltértek. A teljes 50 517 közvetlen megszámolása oszlop-összevetést kíván: NEM ELLENŐRIZHETŐ. |
| DT-F96v nyitva, döntés nélkül | OK | `DONTESEK.md:395` | `git diff … DONTESEK.md`: csak a leírás bővült (94,8%, 5 kihagyás; a javítókör az *az méne* és a *lőnek* kihagyást javította). Állapot 🟡, döntésmező `—`, ajánlás „1.”. A brief `allapot: megallt`, a `kovetkezo` az újraellenőrzésre mutat. Megjegyzés, nem ELTÉRÉS: a forrás-oszlop „14.”, a szöveg „14., 15.2”-t idéz. |
| SEMA 2.34 | OK | `adat/SEMA.md:1437`, `:1442` | A `nevelo_utan` jelentése leírva (a / az + hangtani próba, egy). A „Proveniencia (napló 15.4)” bekezdés egyezik a fejlécekkel (Grep fent). |
| K2 (szórend, tokenszám) | OK, részben | `karoli_modern.tsv`, `karoli_modern_versek.tsv` | numstat 45/45 és 32/32: sorszám-változás nincs. A 31 változott vers diffjében csak a jelzett tokenek cserélődnek, a szórend és az írásjel azonos (`git diff -U0`). A gépi K2 újrafuttatása a parancskörön kívül esik: NEM ELLENŐRIZHETŐ. |
| K3 / K3b (Strong) | OK, részben | — | `git diff --stat b8334a64..207aafc2 -- adat/karoli_strong konkordancia adat/szoto eszkozok/karoli_strong eszkozok/karoli_modern/igeragozas.py …/helyesiras.py …/karoli_modern.py adat/karoli_modern/helyesiras_tokenek.tsv`: üres kimenet. A diff minden „−/+” párja azonos (igehely, sorszám) kulcson áll. A generátor újrafuttatása: NEM ELLENŐRIZHETŐ. |
| CI | OK | `FELADATOK.md` (a diffen kívül) | `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only b8334a64..207aafc2) --diff-alap b8334a64 --diff-fej 207aafc2`: E2–E16, E19, E20, E26, E28–E31 0 találat (E28: 1 migrált nézet); E25 4 JELENTES/FIGYELMEZTETES (`CLAUDE.md:33`, `MUNKAMENET.md`); E27 42 JELENTES/FIGYELMEZTETES (`FELADATOK.md`, nem létező ágak). HIBA nincs, egyik találat sem diffbeli fájlban. Összevetendő CI-jelentést nem kaptam. |
| csv / abszolút út / kódolási őr | OK | `igealak.py`, `regies_szken.py` | `git diff … -- eszkozok \| grep -nE '^\+.*(import csv\|csv\.\|/home/\|/mnt/\|C:\\)'`: nincs találat (rc=1). |
| E17 / DT3 (sorszám-Δ) | OK (tartomány) / NEM ELLENŐRIZHETŐ (az egész ág) | `adat/karoli_modern/*.tsv` | Tartomány: `git diff --numstat b8334a64..207aafc2`. Δ = 0 minden táblán: `igealak_tokenek` 45/45, `karoli_modern` 45/45, `karoli_modern_versek` 32/32, `igealak_alakok`, `igealak_minta`, `igealak_minta2`, `igealak_llm_kor3/4/5`, `regies_szken`, `regies_szken_kor4/5` mind 1/1. A `konkordancia/` és az `adat/` többi `.tsv`-je nincs a diffben. A main-hez (`git merge-base origin/main 207aafc2` = `61714f36`) mérve minden `adat/karoli_modern/*.tsv` új tábla (pl. `karoli_modern.tsv` +599 369, `igealak_tokenek` +67 687 fájlsor), `adat/licencek.tsv` +1. Ezek bontását a korábbi körök vizsgálták, ebben a körben újra nem ellenőriztem. |
| kiszűrt / törölt sorok | OK | — | A tartományban 0 törölt sor. Módosult: `igealak_tokenek` 44 (15.1: 4; 15.2: 39; 15.3: 1), `karoli_modern` 44 (ugyanígy), `karoli_modern_versek` 31 vers; 12 melléktábla csak fejlécet (numstat). |
| kulcstartomány-lefedettség | OK | — | A `karoli_modern.tsv` 599 369 és a `karoli_modern_versek.tsv` 31 160 fájlsora a tartományban változatlan (numstat). |
| nulla-diff hatóköre | — | — | **Vonatkozik:** a Strong-, szótő-, konkordancia- és .1-bemenetekre, valamint a `karoli_modern.py`-ra (bájtra, üres `--stat`); a 9 szken/LLM-táblára (a fejlécen kívül); a hívásnaplókra. **Nem vonatkozik:** a generátor reprodukálhatóságára (a 15.4 „bájtra azonos” próbája végrehajtói állítás, `manual`) és a fejlécek sha256-értékeire. |
| ⛔ pontok | OK | brief 3. pont | Új LLM-futás nincs (a hívásnaplók változatlanok). Végleges DT/N-szám nincs. A diff minden fájlja az `ir` listán van. A javítókör az újraellenőrzésen megállt. |
| A1 | OK | napló 15. bevezető | „A számok a végrehajtó session mérései (`manual`)”: a „mind helyes” állítások végrehajtói állításként jelöltek. |
| A2 | **ELTÉRÉS** | l. a `ts=` sort | A 15.6 egyik „nyitva marad” tétele valójában nem nyitott. Az N-F96f maradéka valóban nyitott (OK). |
| A3 / A4 / A5 | nem alkalmazható | — | Nincs tanulmány, PaRDeS-réteg vagy tanító a diffben. A Tanulmány-ellenőrzés (F37 T4) nem él: nincs `*_bovitett.md` vagy `*_tanulmany.md`. |
| A6 | OK | — | E12–E15 0 találat (a fenti `futtat.py`). |

## ELTÉRÉS-ek, súlyossági sorrendben

1. **Hamis nyitott tétel a naplóban.** A `naplok/KAROLI_MODERN_meres.md` 15.4 és 15.6 szerint a `karoli_modern.py` fejlécéből hiányzik a `ts=`. Valójában megvan: `eszkozok/karoli_modern/karoli_modern.py:166`, `karoli_modern.tsv:1`, `karoli_modern_versek.tsv:1`, és a javítókör előtt is ott volt (`ts=2026-10-25T10:45Z`). Csak dokumentációs hiba, az adat helyes.
2. **Pontatlan leírás a 15.2-ben.** A volt `token_opus` 7 sorát a napló szerint „a .2 szabálya cseréli”. A táblában a DT-F96l többségi címkéje áll (`tobbseg:szabaly+sonnet+opus`, a Luk 16:1-nél `tobbseg:sonnet+opus`). A modern alak és a 198-as szám helyes.

## A 4. kör öt tétele
- **1.** Javítva: a Préd 2:5/2:6/2:9 4 tokenje E/1, hamis E/1-fordítás a korpuszban nincs.
- **2.** Javítva: a `nevelo_utan` hangtani próbát kapott, a kizárás le van írva a kódban, a SEMA-ban és a naplóban; 26 + 1 token cserélt, hamis találat nincs, a maradék 21 token tételesen egyezik.
- **3.** Javítva: a Jel 11:19 *lőnek → lettek*; a 42 *lőnek* közül csak az 1Krón 12:2 maradt *lőttek*, helyesen.
- **4.** Javítva: `ts=` és kör-címke a 12 érintett fejlécben; a szken- és LLM-táblák a fejlécen kívül változatlanok.
- **5.** Javítva: a +1 084 bontása a táblával egyezik.

**Nem ellenőrizhető** (a megengedett parancskörön kívül): a generátorok újrafuttatása (K2/K3/K3b gépi része), a sha256-ok és a 15.5 kulcsonkénti összevetése.

## Megfigyelések, nem e kör tárgya
- A Hós 3:2 *megszerzém azt magamnak* változatlan (`karoli_modern_versek.tsv`, `valtozott=nem`): ez a korábbi E/1 *-ém* kihagyás-osztályba tartozik.
- A 4. kör *béméne* (1Móz 16:4) kihagyása szintén maradt.

Fájlok:
- /home/user/bible-study/naplok/KAROLI_MODERN_meres.md
- /home/user/bible-study/eszkozok/karoli_modern/igealak.py
- /home/user/bible-study/eszkozok/karoli_modern/karoli_modern.py
- /home/user/bible-study/adat/karoli_modern/karoli_modern.tsv
- /home/user/bible-study/adat/karoli_modern/karoli_modern_versek.tsv
- /home/user/bible-study/adat/karoli_modern/igealak_tokenek.tsv
- /home/user/bible-study/DONTESEK.md
- /home/user/bible-study/naplok/ELLENOR_F96_2.md (ide kell menteni ezt a jelentést; én nem írtam bele)
