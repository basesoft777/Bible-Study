ELTÉRÉS: 2 tétel

# ELLENOR_F116 — független ellenőrzés
*Brief: F116_GENERALT_NEZET_CI_BRIEF.md · tartomány: be85d5de..e9ef4f9c (10 commit) · ellenőr: fuggetlen-ellenor, kért modell opus, tényleges claude-opus-5-5 · 2026-10-18*
*A szerepfájl szerint Bash-sel csak git diff/log, lekerdez.py és futtat.py futott; a test_szabalyok.py, a general.py --ellenoriz és a feladatok.py ellenoriz ezen kívül esik → NEM ELLENŐRIZHETŐ.*
*Az ellenőrnek nincs fájlíró eszköze: a jelentés szövegét az orkesztrátor írta be szó szerint, és ő commitolta (F116.10).*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | naplok/GENERALT_NEZET_CI_meres.md:3 | saját: claude-opus-5-5 = opus. `git log --format="%h %(trailers:key=Co-Authored-By,valueonly)" be85d5de..HEAD` → 10× Claude Sonnet 5.5; a napló fejléce claude-sonnet-5-5 = brief sonnet; adattáblát a menet nem írt |
| G1 E28 sorvég | ELTÉRÉS | eszkozok/ellenorzes/szabalyok.py:1824,1878,1977,2015 | CI-terv 1/3: „sorvég-normalizálás nélkül”; a kód mindkét oldalon _lf()-et alkalmaz; a meres.md:137 (E1) megfelelésnek írja le, a :153 (E6) szerint „ellentmondás nincs” → az eltérés nincs dokumentálva |
| G1 E28 robusztusság | ELTÉRÉS | szabalyok.py:1916,1971; general.py:326-327 | a marker_par_keres ValueError-ja try nélkül → a futtat.py jelentés nélkül leáll (kódolvasás) |
| G1 E28 indítás | OK (megj.) | szabalyok.py:1840-1862 | az E28_INDITO_MINTAK megegyezik a brief 5. lépésével és a CI-tervvel; a Konyv_normalizalo_tabla.tsv (generátor-bemenet) nincs rajta |
| G1 E29 | OK | szabalyok.py:2032-2077 | a minták lefedik a CI-terv 2. szakaszát; a 【NAPLÓ többletet a napló E4 pontja jelöli |
| G2 | OK | — | `futtat.py --teljes` rc=0; E28 0 találat („E28: 0 migrált nézet”); E29 0 találat. A --teljes mód mindent JELENTES-re minősít (futtat.py:94-96, nem változott), ezért a 0 találat a mérvadó |
| G2 PR-szint | OK | futtat.py:97; szabalyok.py:45-46,57 | `futtat.py --valtozott <9 fájl> --diff-alap be85d5de --diff-fej HEAD --pr-cim "[ELLENŐRZŐ] F116" --esemeny pull_request` → rc=0, az E28 lefutott, 0 találat; FAJLSZINTU → HIBA, nincs D8-leminősítés; a pozitív HIBA-próba (meres.md:122) NEM ELLENŐRIZHETŐ |
| G3 | NEM ELLENŐRIZHETŐ (lefedettség OK) | test_szabalyok.py:1080-1310 | nem futtattam; kódolvasás: a G3 minden esetére van teszt, 13+10 tesztfüggvény; a _e28_commitolt helyettesítve (a blobút teszteletlen) |
| G4 | OK | szabalyok.py:2032-2077 | Grep `import |general|motivumok/|subprocess` → 0 találat a tartományban |
| G5 | OK | NYITOTT_FELADATOK.md:726-799; motivumlog/PaRDeS_motivumok.md:492-539 | `git diff -U0 be85d5de..HEAD`: a hunkok a markerpárokon belül vannak; `git log -S'Jób 17:12'` és `-S'Préd 9:12' -- adat/elofordulasok.tsv` → 98f22fc6; az elofordulasok 97/98/125. sora ALVIL-001 Jób 17:12/17:15, Préd 9:12; jeloltek: nyitva 50, beépítve 259, elutasítva 308 (Grep count) = a blokk 728. sora; a jóváhagyás a hívó közlése szerint megvolt |
| G6 | OK | eszkozok/ellenorzes/ | Grep csv → 0 találat; kozos.py:132-152 split('\t') |
| G7 | OK | szabalyok.py:26-29; futtat.py:35-38; test_szabalyok.py:25-28 | Grep reconfigure |
| D1 | OK | szabalyok.py:57 | `git log --remotes -S"'E28'"` és `-S"'E29'" -- *.py *.yml` → 0 |
| D2 | OK | e28_migralt_nezetek.tsv:1 | csak fejléc, 6 oszlop |
| D3 | OK | szabalyok.py:942-947 | az ONMODOSITAS_MINTAK része az eszkozok/ellenorzes/ |
| D4 | OK | — | újragenerálva, kivétellista nincs; --teljes: E28 0 találat |
| D5 | OK | szabalyok.py:2032-2077 | lásd G4 |
| D6 | OK | szabalyok.py:45-46,2071-2074 | fájlszintű, a jelentés soronkénti |
| D7 | OK | — | az F11 brief nincs a diffben |
| D8 | OK | — | Sonnet-trailerek |
| (2) trigger | OK | ellenorzes.yml:68-93 | csak lépésnév-változás; a szűrés az _e28_indul-ban |
| (3) blob | OK (lásd 1. ELTÉRÉS) | szabalyok.py:1866-1878 | git show HEAD:<út> |
| (6) ir | OK | — | `git diff --name-only`: 9 fájl, mind engedélyezett |
| A1 | OK | meres.md:7,92,105 | van proveniencia-sor; az adatforrást magam igazoltam |
| A2 | OK | NYITOTT_FELADATOK.md:728 | 50 nyitva = tábla; (a diffen kívül: a :704 kézi „16 sor” elavult) |
| A3-A5 | n.a. | — | nincs tanulmány |
| A6 | OK | — | E12 JELENTES 70, E13 JELENTES 29, mind régi |
| CI-jelentés | NEM ELLENŐRIZHETŐ | — | nem kaptam CI-jelentést; a saját PR-futásom rc=0 |
| general.py --ellenoriz | NEM ELLENŐRIZHETŐ (közvetett OK) | general.py:969-981 | az E28 ugyanazokat a függvényeket hívja ugyanazzal a == összevetéssel, és 0 találatot adott |
| feladatok.py ellenoriz | NEM ELLENŐRIZHETŐ | — | parancskörön kívül |
| ISTENTISZT-próba | NEM ELLENŐRIZHETŐ | meres.md:112-124 | ahhoz a listát módosítani kellett volna |
| Lista 1 törölt | OK | — | numstat: 35 = 23 NYITOTT-blokk (1+17+5) + 2 konyv_index + 4 workflow + 2 futtat-docstring + 3 szabalyok + 1 brief-állapot |
| Lista 2 | n.a. | — | nincs érintett Strong-/igehely-tartomány |
| Lista 3 nulla-diff | OK | — | general.py, lexikon_general.py, nulladiff.sh nem változott; csak a két marker-törzs; a lexikon/ és a generalt_proba/ érintetlen; a 0 eltérés a hat marker-blokkra érvényes, a befagyasztott lapokra nem |
| Lista 4 Δ | OK | — | `git diff --numstat -- adat konkordancia` → üres, minden Δ=0; az új lista 0 adatsorral |
| Lista 5 ⛔ | OK | — | a DONTESEK.md nincs a diffben; nincs generátor-módosítás |
| F37 T4 | n.a. | — | nincs tanulmányfájl |

ELTÉRÉS-ek: 1) E28 _lf()-normalizálás a CI-terv „sorvég-normalizálás nélkül” pontjával szemben, nincs dokumentálva (közepes). 2) szabalyok.py:1971 kezeletlen ValueError → a futtató leáll, jelentés nincs (alacsony).
