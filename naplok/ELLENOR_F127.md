ELTÉRÉS: 5 tétel

# Független ellenőrzés — F127_LEXIKON_HALO_RES_BRIEF.md

*A jelentés szövegét a `fuggetlen-ellenor` subagent (agentId adc47c8e2c730c6bd) adta vissza; mivel a futásában nem volt fájlíró eszköze, a végrehajtó session írta ki szó szerint, változtatás nélkül (F127.18).*

- Brief: F127_LEXIKON_HALO_RES_BRIEF.md (C. lépés; 5. Elfogadási feltételek; 7. Eltérések); döntések: DONTESEK.md DT-F127a–f
- Tartomány: 9d6027940ed814b97148eedc1e3ab2672a63f4b2..6f7fa7eb (ág: claude/lexikon-halo-res; HEAD = 6f7fa7eb)
- Ellenőr modellje: claude-opus-5-5 (kért: opus — egyezik)
- Dátum: 2026-10-21
- Módszer: csak olvasás. Bash-ből git diff, git log, lekerdez.py és futtat.py futott; a fájlokat Read/Grep olvasta. Generátort, ellenoriz.py-t és tesztet nem futtattam, ezért a generátor-szintű nulla-diff és a tesztek NEM ELLENŐRIZHETŐ. Eljárási megjegyzés: egy hívásban `| head -60` vágta a lekerdez.py --help kimenetét; ez kívül esik a megengedett parancsformán, csak olvasott.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | claude-opus-5-5 = opus. A menet modell-mezőt nem írt (Grep "(?i)modell\|claude-\|opus\|sonnet" naplok/F127_* → 0). A commitok Co-Authored-By sora Claude Opus 5.5. |
| E1 (döntés, majd bevezetés) | OK | DONTESEK.md:351-352 | git log --name-only: b642c14b (DT-F127a/b) megelőzi a 3ad8ca9f (A1) commitot. A bevezetés a döntést követi; a `tematikus` típus kimaradt (MOTIVUM_KAPCSOLAT_TIPUSOK). |
| E2 / C3 (forrás bájtra azonos) | OK | motivumok/ISTENTISZT-001.md:376-384; motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md:124-154 | git diff és --numstat: mindkét fájl `4 0`; csak a RÉS-KEZDET/VÉGE pár és egy-egy üres sor új. |
| E2 (7 régi lap: átmeneti mondat) | OK | adat/res_forras.tsv:9-73 | Grep: 16 új sor, ISTENTISZT 2× tanulmany, 7 motívum 2× adat. Az „5. Alkalmazás és tanítványság” szakasz mind a 7 tematikus tanulmányban megvan (Grep → 7 fájl). |
| E3 / C4 (nincs kapcsolat döntés nélkül) | OK | adat/motivum_kapcsolatok.tsv:3-5; adat/jeloltek.tsv:630-636 | (b) és (d) beépítve, a dontes_ref egyezik, a pár illeszkedik a jelölt id/igehely + cel_igehely értékére. (a), (c) és a 3 soros (e) nyitva; az (a) cel_alpont-tal. A párok rendezettek, az alpont-mezők üresek. |
| E4 (régi blokkok változatlanok) | OK (lapok) / NEM ELLENŐRIZHETŐ (generátor) | lexikon/*_TUDOMANYOS.md | git diff --numstat: 31/2, 26/2, 30/2, 26/2, 61/1, 26/2, 26/2, 28/2. A törlés csak a tartalomjegyzék fejléce és a „12 szakaszának” sor; a hozzáadás a tartalomjegyzék, az 5/b. és a 6/b. Az 1/b. változatlan. |
| E5 (CI zöld) | ELTÉRÉS | eszkozok/ellenoriz.py:0 (E16) | futtat.py --valtozott $(git diff --name-only base head) --diff-alap base --diff-fej 6f7fa7eb → exit 1, E16 HIBA: a PR-cím nem [ELLENŐRZŐ] előtagú. A többi E-szabály nem ad HIBA-t. |
| E5 (ellenoriz.py, feladatok.py, tesztek) | NEM ELLENŐRIZHETŐ | — | nem megengedett parancs |
| DT-F127a | OK | SEMA 2.12; RENDER_BRIEF.md:53-57; CLAUDE.md:50-55; lexikon_general.py RES_SORREND/SZAKASZ_6B | 9 rés mindenütt; a 11. szabály a teljességet és az ismeretlen rést ellenőrzi; a törzscikk a 6/b-ig vág (az idx KeyError-ját a try elkapja, torzscikk_general.py:119-123). |
| DT-F127b | OK | SEMA 2.4, 2.33; ellenoriz.py szabaly2b_motivumkozi | A fejléc 13 mezője egyezik; a (C)-t a 2/b. őrzi. Megjegyzés: a pardes_szint zárt készletét és az igehely-formátumot a 2/b. nem ellenőrzi; a mai érték (Remez) érvényes. |
| DT-F127c | OK | lexikon/* (84e63e0a) | 5ffcb981 ⛔ → 84e63e0a; a f127_res_eles.py csak az 5/b-t, a 6/b-t és a tartalomjegyzéket cseréli. Licenc: projekt-adat → „minden jog fenntartva”, elfogadott mellékhatás. |
| DT-F127d (szűrés) | OK | general.py:265-279 + 9 eszköz | Minden előfordulás-olvasó szűr. A szabalyok.py E7 (:459-489) szűretlen, de csak dontes=bekerult-ra néz. Ismert: olvaso_mockup/kinyer.py:24 szűretlen, DT-F127d (b) rögzíti. |
| DT-F127d (627 sor, első 9 mező) | OK | adat/jeloltek.tsv:1-629 | git diff --word-diff=porcelain --word-diff-regex='[^TAB LF]+' → adatsorban törölt token 0 (csak a kommentsor); +elofordulas 626× + 1× a tabokkal együtt = 627. Grep: 635 sor 13 mezős. numstat 636/629. Korlát: a word-diff a tabot elválasztónak veszi; ezt a mezőszám-ellenőrzés ellensúlyozza. |
| DT-F127e | OK | adat/jeloltek.tsv:630-636 | Grep elofordulasok.tsv: mind a 12 oldal előfordulás (sorszámokkal). HAMART 12:3 „megfordítása”: Bun_…_tematikus.md:83; a 4:26-ra nincs találat; ALVIL Hadesz_Seol_tematikus.md:39; TEREMT Tehom_tematikus.md:131 (2/c. a 122. sortól). |
| DT-F127f | OK | lexikon/* (750c0ef8) | b8cf851d ⛔ → cb94156a → 750c0ef8; a 93bf01b2 nem írt lexikont. A döntésre váró számok (5/1/1/3) egyeznek a jelöltsorokkal. |
| C1 (SEMA 2.12) | ELTÉRÉS | adat/SEMA.md 2.12 `tanulmany` mező | A mezőleírás csak a tematikus_lezart/* fájlt és a naplót említi, a táblában viszont motivumok/… és motivumok/naplok/… is áll. Alacsony súlyú. |
| C2 / lista 3 (nulla-diff hatóköre) | OK / NEM ELLENŐRIZHETŐ | — | Igazolt a commitolt fájlokon: a lapok csak a 3 részen változtak; a TORZSCIKK, a naplók és a NYITOTT generált blokkja (769–841) nem változott, az N-F127a a 68. sorban áll. Nem igazolt: a base↔HEAD generátor-kimenet összevetése (nem futtatható). |
| C5 (proveniencia) | OK | naplok/F127_B2_szomszedsag.tsv:3-14; naplok/F127_lekerdezesek.tsv:3-21 | A 7 jelölt mind a saját scope-sorát hordozza. lekerdez.py karoli: ApCsel 2:21 n=1, 1Móz 12:8 n=0, Róm 10:7 n=1 (a szöveg egyezik a jeloltlap.md:63-mal), Zsolt 116:4 n=0 — mind egyezik a naplóval. A távolságok (23, 5) helyesek. |
| A1 | OK | adat/jeloltek.tsv:631 | A beszéd-szomszédság értelmezésként jelölt; a „nem bizonyít szándékos utalást” mondat minden indoklásban áll; a funkció felhasználói döntés szövege. |
| A2 | OK | NYITOTT_FELADATOK.md:68 | Az N-F127a nyitott: a tanítói fájl utalásai változatlanok. |
| A2-kieg. (N-F127a hatóköre) | ELTÉRÉS | lexikon/ISTENTISZT-001_TUDOMANYOS.md 6/b. alkalmazas, 1. kérdés; motivumok/ISTENTISZT-001.md:380 | Az „l. 3. pont” a forrásban a PaRDeS-szakaszra (112. sor) mutat, a lapon a „3. LXX-fordítói döntések” (1277. sor) a 3. szakasz. Az N-F127a csak a tanítói összegzést nevezi meg. Alacsony súlyú. |
| A3 | OK | motivum_kapcsolatok.tsv:3-5 | szomszédos típus; lexikai párhuzamot nem állít |
| A4 | OK | — | Sod-réteget nem ír; tanulmányfájl nincs a diffben, az F37 T4 nem él. |
| A5 | OK | ISTENTISZT 6/b. Tanítói egyezés | A #130 változatlan Összegzése, a gap explicit; a régi lapok a tanulmányok gap-jelzésére mutatnak (Tehom:175, Hadesz_Seol:164). |
| A6 | OK | lexikon/ALVIL-001_TUDOMANYOS.md:13 | E12 FIGYELMEZTETÉS a „14 szakaszának” mondatra: helyes, len(SZAKASZOK) = 14. E13: régi tartalom, nem diff-sor. E14 = E15 = 0. |
| 3 (CI-jelentés egyezése) | NEM ELLENŐRIZHETŐ | — | nem kaptam CI-jelentést; a saját futás az E5-sorban |
| Lista 1 (törölt sorok) | OK | — | jeloltek: 629 törölt = 1 komment + 1 fejléc + 627 bővítve visszaírt sor; adatvesztés 0. res_forras 0; motivumok 0; lapok: 2 (ISTENTISZT: 1) a tartalomjegyzékben. |
| Lista 2 (kulcs-lefedettség) | OK | adat/res_forras.tsv | Grep → 72 = 8 × 9; a 7 motívumközi kulcs egyedi. |
| Lista 4 (tábla-Δ, DT3) | ELTÉRÉS | adat/res_forras.tsv | jeloltek 627 → 634 (+7); motivum_kapcsolatok 0 → 3 (+3, új); res_forras 56 → 72 (+16); konkordancia/ 0. A +16-hoz nincs bontási napló (Grep res_forras naplok/F127_* → 0); a bontás (2 + 14) csak a DT-F127a-ban és az F127.4 commit-üzenetében áll. |
| Lista 5 (⛔ pontok) | OK | — | 0.2 → A1; A3 5ffcb981 → 84e63e0a; DT-F127d 7a6ae9d5 → d7968f07 → 120f2cef; B3 f4b826da → e8026b63 → 93bf01b2; B4 b8cf851d → cb94156a → 750c0ef8 |
| Brief ir | ELTÉRÉS | F127_LEXIKON_HALO_RES_BRIEF.md:14 | ANTROP/HODIT/KIRALY/MENNY _TUDOMANYOS.md és 4 új eszkozok/f127_*.py az ir-en kívül íródott, a 7. szakasz nem sorolja fel őket. Alacsony súlyú. |
| Ismert tételek | OK / NEM ELLENŐRIZHETŐ | — | F127.9 kétszer (7e35612c, 120f2cef): pontos. kinyer.py szűretlen: pontos. teszt_lelet és pardes.db: NEM ELLENŐRIZHETŐ (a sqlite_epit.py :500/:1223 szűr, a 2/b-t a :246 futtatja). |

ELTÉRÉS-ek súlyossági sorrendben:
1. E16 HIBA: a PR címe [ELLENŐRZŐ] előtagot kíván; enélkül az 5. elfogadási feltétel nem teljesül.
2. A brief ir-je hiányos (4 lexikonoldal, 4 új f127_*.py), és a 7. szakasz nem rögzíti.
3. Az N-F127a hatóköre szűk: az alkalmazas rés „l. 3. pont” utalása a lapon rossz szakaszra mutat.
4. A res_forras.tsv +16-hoz nincs bontási napló (DT3).
5. A SEMA 2.12 `tanulmany` mezőleírása nem frissült.
