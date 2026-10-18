ELTÉRÉS: 2 tétel

# ELLENOR_KJV_SZOVEG — független ellenőrzés

Brief: `F118_KJV_SZOVEG_BRIEF.md` (FELADATOK #118, KJV_SZOVEG) · tartomány: `origin/main..HEAD` = `8965b53f..93051c2d` (20 commit, F118.1–F118.20) · ellenőr: claude-opus-5-5 (kért: opus) · 2026-10-18

*A jelentést a `fuggetlen-ellenor` subagent írta; fájlíró eszköze nem volt, ezért a hívó (orkesztrátor) változtatás nélkül írta ki. A NEM ELLENŐRIZHETŐ pontok hívói pótlása a végén, külön szakaszban áll.*

Korlát: az ellenőr szerepe szerint Bash-sel csak `git diff/log`, `lekerdez.py` és `futtat.py` futhat. A zipet olvasó mérést, a teszteket, a generátort és a `feladatok.py`-t ezért nem futtattam, ezek NEM ELLENŐRIZHETŐ-k. A táblaszámokat Grep eszközzel igazoltam (minta és találatszám a sorban).

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | tényleges: claude-opus-5-5, kért: `opus`. A diffben nincs adattábla `modell` mező. `git diff origin/main..HEAD \| grep -niE "^\+.*(modell\|claude-\|opus\|sonnet)"`: csak a tervezet `modell: opus` brief-mezője, ez kért modell, nem tényleges. |
| E1 generált, fejlécek, sha | OK | `konkordancia/KJV_teljes_szoveg.tsv:1-5` | Read: GENERÁLT-, proveniencia- (sha256 00532b6d…d447), licenc-, ÁLLAPOT- és veszteség-sor. A brieftől eltérő sha256 felhasználói döntés: `naplok/KJV_SZOVEG_M0.md:3`, DT-F118a/d, és a hívó ezt egyeztetett eltérésként adta meg. Az importáló eltérő hash-nél megáll: `eszkozok/kjv_szoveg_import.py:277-278`. |
| E2 M-a | OK (tábla) / NEM ELLENŐRIZHETŐ (zipből) | `naplok/KJV_SZOVEG_meres.md:13-15` | Grep `^[1-3A-Za-z]+\.\d+\.[1-9]\d*\t` → 31 102; `\.0\t` → 116. Grep `^(Mrk\.9\.43\|Luk\.6\.41\|Luk\.17\.36)\t` a `konkordancia/KJV_*.tsv`-ben: csak a KJV_teljes_szoveg.tsv 24704/25310/25810. sorában van, a KJV_Strongs_teljes-ben nincs. Az S ⊆ T teljes halmazvizsgálatát és a zipből való újramérést nem futtattam (szerepkorlát). |
| E3 M-b | NEM ELLENŐRIZHETŐ | `naplok/KJV_SZOVEG_meres.md:16,26-35`; `naplok/KJV_SZOVEG_szoegyezes_hiany.tsv` | A szóegyezés újramérése kódfuttatást kér. A napló szerint 362 399 elem, 76 összetett szó, 8 szótöredék, megmagyarázatlan 0; a hiánytábla 87 sor (`git diff --numstat`), a 84 adatsor + fejléc ennek megfelel. Saját méréssel nem igazoltam. |
| E4 M-c, jelölőleltár | OK (részben) | `naplok/KJV_SZOVEG_M0_jelolok.tsv`; `eszkozok/teszt_kjv_szoveg_import.py:35-242` | Grep, üres Szöveg/Szöveg_jelolt mező (`^[^#\t][^\t]*\t\t\|^[^#\t][^\t]*\t[^\t]*\t\t`) → 0. Backslash és dupla szóköz: 1 találat, az 5. fejlécsor (veszteség-sor), adatsorban 0. A `‹` a jelölt mezőben 2 028 sorban (egyezik a naplóval). A leltár összegei egyeznek a veszteség-sorral: add 20 887+623=21 510, nd 6 876+16=6 892. Tesztnevek jelölőnként: w, add, nd, wj, ¶, f, tl, p/q1/b, s1, d, leltáron kívüli → hiba. A tesztek futását nem igazoltam. |
| E5 licenc/datasetek/SEMA | OK | `adat/licencek.tsv:58`, `adat/datasetek.tsv:114-117`, `adat/SEMA.md:395-401` | `git diff --numstat origin/main..HEAD -- adat/` → 7/0, 4/0, 1/0: csak hozzáfűzés. A licencsor `allapot=kozkincs`, az üres megjelölés-mező a Thayer- és Nave-sor mintáját követi (Grep, 8. mező). A DT-F118a 1. alkalmazva. |
| E5 `feladatok.py ellenoriz` | NEM ELLENŐRIZHETŐ | — | nem megengedett parancs |
| E6 érintetlenség | OK | — | `git diff --stat origin/main..HEAD -- konkordancia/KJV_Strongs_teljes.tsv naplok/F19_hianyok.tsv eszkozok/f19_ebible_import.py eszkozok/olvaso_szerver/ 'konkordancia/Karoli_versmegfeleltetes*' eszkozok/tsk_kulcs.py 'adat/bdb_*' eszkozok/bdb_jelolt/ eszkozok/sqlite_epit.py` → üres kimenet |
| E7 DT-F118c, tervezet | OK | `DONTESEK.md:285`; `beerkezo/KJV_SZOVEG_MEGJELENITES_BRIEF_TERVEZET.md:15` | A (b) felhasználói döntéssel. A tervezetben `fugg: [117, 118]`, az N-F117a szövegesen, a brief M4-listájának minden eleme megvan (tábla, egy–több vers, blokk, kiadási kapcsoló, mérés). |
| E8 | OK | — | ez a jelentés |
| G/D DT-F118a–e | OK | `DONTESEK.md:280-285` | helyőrzőkkel, végleges DT-szám nélkül. A ⛔-sorrend a `git log --oneline` szerint: M0 (F118.4 → .5 megállt → .6 döntés → .7 kód), M1 (.8 → .9 → .10 → .11), M4 (.17 → .18 → .19 → .20) |
| ELTÉRÉS: brief-fejléc | ELTÉRÉS | `F118_KJV_SZOVEG_BRIEF.md:12` | `kovetkezo: Te: M4 ⛔ — DT-F118c`, pedig a DT-F118c már eldőlt (F118.19), és a tervezet elkészült (F118.20). A CLAUDE.md szerint minden menet a saját fejlécét frissíti. |
| ELTÉRÉS: írás előtti összevetés | ELTÉRÉS | `eszkozok/kjv_szoveg_import.py:287-291` | Az importáló a meglévő táblát összevetés és megállás nélkül írja felül (CLAUDE.md „TSV-olvasás”, brief M3 utolsó pontja). A `ts=date.today()` miatt a proveniencia-sor naponta változik, így a napló „bájtra azonos” állítása (`naplok/KJV_SZOVEG_meres.md:7`) csak aznapi újrafuttatásra érvényes. |
| újragenerálás, tesztek | NEM ELLENŐRIZHETŐ | — | `kjv_szoveg_import.py` és `teszt_kjv_szoveg_import.py`: nem megengedett parancs |
| `ir` lista | OK | `F118_KJV_SZOVEG_BRIEF.md:14` | A `git diff --stat` szerint a lista mind a 7 eleme érintett. Ezen felül csak a brief fejléce, a `DONTESEK.md` és a `naplok/KJV_SZOVEG_*` íródott, ezeket a brief maga írja elő (M0-terv, M1-minta, mérési napló, mérőkód „a naplóban”). |
| letöltés tilalma, zip nincs a repóban | OK | `eszkozok/kjv_szoveg_import.py:7,36,203` | Grep `urllib\|requests\|http\.client\|extractall\|csv\.` → nincs találat; csak `zipfile.ZipFile` olvas. A diffben nincs zip. |
| A1 memória vs. lekérdezés | OK | `naplok/KJV_SZOVEG_M0.md:26`; `adat/licencek.tsv:58` | A licencértelmezés „értelmezés, nem jogi vélemény” jelöléssel áll. A CrossWire-hozzájárulás kérdése nyitott, kitöltés nélkül. |
| A2 nyitott tételek | OK | `adat/SEMA.md:400` | A zip második példánya „megadandó” (nyitott, egyezik a hívó közlésével). A DT126 nyitott. A NYITOTT_FELADATOK.md nem változott. |
| A3–A6 | nem alkalmazható | — | nincs tanulmány- vagy tanítóanyag a diffben; a futtat.py E12–E15 0 találat |
| CI-jelentés egyezése | NEM ELLENŐRIZHETŐ | — | CI-jelentést nem kaptam. Saját futtatás: `python eszkozok/ellenorzes/futtat.py --valtozott $(git diff --name-only origin/main..HEAD) --diff-alap origin/main --diff-fej HEAD` → exit=0. E2–E20, E26, E28, E29: 0 találat. E25: 3 JELENTES (CLAUDE.md, MUNKAMENET.md), E27: 40 JELENTES/FIGYELMEZTETES (FELADATOK.md ághivatkozások); egyik sem a diff fájljain. |
| L1 törölt sorok | OK | — | `git diff --numstat`: összes törlés 2, mindkettő a brief fejlécében (`allapot`, `kovetkezo` csere), adattörlés 0 |
| L2 kulcstartomány | OK (részben) | — | 66 könyv, 31 102 + 116 kulcs (Grep, lásd E2). A könyvenkénti teljességet zipből nem mértem újra. |
| L3 „nulla-diff” hatóköre | OK | — | A nulla-diff a védett fájlokra vonatkozik (E6) és az adat/ meglévő soraira (0 törlés). Nem vonatkozik a három adat/ fájl hozzáfűzött soraira és az új táblára. |
| L4 tábla-sorszám Δ (E17, DT3) | OK | `naplok/KJV_SZOVEG_meres.md:7,15` | konkordancia/KJV_teljes_szoveg.tsv: +31 218 (új tábla; bontás: 31 102 vers + 116 felirat). adat/datasetek.tsv: +4. adat/licencek.tsv: +1. Minden más adat/ és konkordancia/ `.tsv`: 0 (`git diff --numstat`). A futtat.py E17-et nem jelentett. |
| L5 ⛔ pontok | OK | — | M0, M1, M4 megállás és döntés a `git log` szerint (lásd G/D sor); a sha-eltérés ⛔-je: `naplok/KJV_SZOVEG_M0.md:3` |
| T4 tanulmány | nem él | — | a diffben nincs `*_bovitett.md` / `*_tanulmany.md` |

ELTÉRÉS-ek súlyossági sorrendben:
1. `eszkozok/kjv_szoveg_import.py:287-291`: a meglévő táblát összevetés nélkül írja felül; a `ts=today` miatt a „bájtra azonos” csak aznapra igaz.
2. `F118_KJV_SZOVEG_BRIEF.md:12`: elavult `kovetkezo` mező (M4 ⛔ a DT-F118c (b) döntése után is).

## Hívói pótlás a NEM ELLENŐRIZHETŐ pontokra (orkesztrátor, claude-opus-5-5, 2026-10-18, HEAD 93051c2d)

A végrehajtótól független futtatások; a mérőkód saját, nem a `naplok/KJV_SZOVEG_meres.py`.

| pont | eredmény | parancs / mért érték |
|---|---|---|
| újragenerálás | OK | `python eszkozok/kjv_szoveg_import.py --munka C:/Users/bases/Desktop/kjv_munka --kimenet <scratchpad>/ujra.tsv` → 31 218 sor; az adatsorok `cmp`-vel azonosak a commitolt táblával, a fejlécsorok `diff`-fel is (ugyanaznap) |
| tesztek | OK | `python eszkozok/teszt_kjv_szoveg_import.py` → 24 teszt, OK |
| `feladatok.py ellenoriz` | OK | 138 brief, 0 hiba, 0 figyelmeztetés |
| E2 M-a (teljes halmaz) | OK | saját szkript, `split('\t')`: \|S\| = 31 215, \|T\| = 31 218, S ⊆ T igaz, T ∖ S = {Luk.17.36, Luk.6.41, Mrk.9.43} |
| E3 M-b (saját normalizálással) | OK, egyező | saját sorrendtartó részsorozat-illesztés (`[a-z]+` tokenek, aposztróf el): 362 492 szóelem (az eltérés a napló 362 399-étől a tokenizálásé: a kötőjeles szavakat a saját mérés szétvágja), nem illeszkedő 90 elem 46 versben = a végrehajtó első futásának 90 eltérése; a hiánytábla 84 sora okkal: 76 `osszetett_szo`, 8 `szoreszlet`, megmagyarázatlan 0 |
| L2 könyvenkénti teljesség zipből | NEM ELLENŐRIZHETŐ | nem futott külön; a vershalmaz a #19-táblával való S ⊆ T egyezésen át igazolt |
