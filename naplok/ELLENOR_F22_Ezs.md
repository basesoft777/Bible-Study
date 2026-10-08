# ELLENOR_F22_Ezs.md — független ellenőri kör: Ézsaiás (F22.Ézs)

*A `fuggetlen-ellenor` subagent jelentése, az orkesztrátor mentette változatlan tartalommal (a subagentnek nincs fájlíró eszköze; a Zsolt-precedens szerint). Összesítés: ELTÉRÉS: 8 tétel. A javítások: `naplok/F22_Ezs_jelentes.md` 6. pont.*

- **Brief:** `F22_KAROLI_STRONG_BRIEF.md` (22.4, 22.5, K1–K4, K9, D16) és `F77_API_VAKPROBA_BRIEF.md` (DT73 (a))
- **Tartomány:** `d288e08~1..6185011`. A `cab9f48` (F77.10) csak kontextusként szerepel.
- **Nem futtattam:** `f22_statisztika.py`, `egyesit.py --ellenoriz`, `f22_elemzes.py`, valamint a scratchpad-szkriptek. Ezek kívül esnek a megengedett parancskörön. A számokat helyettük Grep-számlálással (ripgrep, count mód) és `lekerdez.py`-jal ellenőriztem.
- **Eljárási bevallás:** néhány `git diff`/`git log` hívás kimenetét `grep`/`head`/`tail`/`wc`/`echo` pipe-pal szűrtem. Ez túlment a szigorú parancskörön. Csak olvasás volt, írás nem történt.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| Szám: parok 25 488 link | OK | `adat/karoli_strong/parok_Ezs.tsv` | `git diff --numstat` → 25490 sor (proveniencia + fejléc + 25488). Grep `\talacsony\tS$` → 25488. Grep `\t(magas\|kezi)\t` → 0. |
| Szám: szavak 50 069 | OK | `szavak_Ezs.tsv` | numstat 50071 = 2 + 50069. Grep `\thu\t` → 24847, `\ter\t` → 25222. |
| Szám: hu bontás | OK | `szavak_Ezs.tsv` | parositva 20581, betoldas 4226, fuggoben 40 (Grep count), összesen 24847 |
| Szám: er bontás | OK | `szavak_Ezs.tsv` | parositva 23961, forditatlan 1219, fuggoben 42, összesen 25222 |
| Szám: 2.1 fejezetsorok (szúrópróba) | OK | jelentés 52, 80, 107 | Grep `^Ézs 9:` → szavak 825, parok 390. `^Ézs 64:` szavak → 436. `^Ézs 37:` parok → 811. A kezi 43 = 20 hu + 23 er (9. fejezet), 39 = 20 + 19 (64. fejezet). |
| Szám: régi arany 17 | OK (szúrópróba) | jelentés 115 | Grep `^Isa\.` a `Karoli_Strong_kivonat.tsv`-ben → 17. A szavak táblában Ézs 7:11 „mélységben” H7585, 26:19 „árnyakat” H7496, 51:10 „mélység” H8415 egyezik. `lekerdez.py scan H7585 --szakasz "Ézs 7:11"` → 1 igehely, `proveniencia: scope=range:Ézs 7:11 \| forras=TAHOT_kivonat.tsv \| strong=H7585 \| n=1 \| ts=2026-10-08T10:03Z` |
| Szám: kapuhiba 29/1290, 16 köteg | OK | `f22/api_termeles/futasnaplo.tsv:12…125` | Grep a `kapuhiba_db>0` sorokra: 16 sor, összegük 29. A kötegek {14,21,27,33,42,45,47,54,60,62,68,73,74,81,93,94}, egyeznek a jelentés 18. sorával. |
| Szám: költség körönként | OK | `futasnaplo.tsv:130,146` | A `futo_osszeg_usd` oszlop: az 1. kör végén 6.754311, a 2. kör vége 7.083442 (Δ 0.329131). A token-összegek ezzel konzisztensek: 1.351156 + 5 × 1.080631 = 6.754311, és 0.193661 + 5 × 0.027094 = 0.329131 (batch-ár 1/5 USD/MTok, az 1. sorból levezetve). |
| Szám: 145 sor, end_turn, hash | OK | `futasnaplo.tsv` | Grep `\tend_turn\t84f12ca7aafb\t` → 145. A régi `f22/futasnaplo.tsv`-ben ugyanez a hash 391 sorban szerepel. |
| Szám: `egyesit.py --ellenoriz` (8 könyv, bájtazonosság) | NEM ELLENŐRIZHETŐ | jelentés 30 | A szkript futtatása nem megengedett. Statikus olvasat: az `egyesit.py` `api_futas()` hamisat ad a régi könyvekre, ezért ott a „subagent” szöveg változatlan. A `_kezi_sorok` csak Ézs-sorokat tartalmaz. |
| Szám: 1292 nyers vers | NEM ELLENŐRIZHETŐ | jelentés 7 | Disztinkt versszám Greppel nem számolható. A 25180 + 42 = 25222 egyezik a TAHOT-tal. |
| K1 darabszám | OK | `szavak_Ezs.tsv` | er 25222 = Grep `^Ézs ` a `TAHOT_kivonat.tsv`-ben → 25222. Versek: `\thu\t1\t` → 1290, `\ter\t1\t` → 1290; a `Karoli_1908.tsv`-ben `^Ézs ` → 1290. `+1000`-es vers: 0. |
| K1 „pontosan egyszer” | NEM ELLENŐRIZHETŐ | | Duplikátum-szűrés és a hu-tokenösszeg a `tokenek.tokenizal`-lal szkript nélkül nem végezhető el. A darabszámok egyeznek. |
| K2 | OK (szúrópróba) | `szavak_Ezs.tsv:7046,7218–7240,47421–47465` | Grep: a nem `H\d{4}` er-sor 0 (25222/25222 illeszkedik). Ézs 9:17 er 1–20 = TAHOT 9:16 Strongjai (H5921, H3651, H0970 …). 9:20 er 19–41 = TAHOT 9:20 (H4519 … H5186). 64:1 er 10–28 = TAHOT 64:2. 64:2 er 1–12 = TAHOT 64:3. `lekerdez.py scan H4519 --szakasz "Ézs 9:20"` → 2 előfordulás; `scan H6919 --szakasz "Ézs 64:2"` → 1; `"Ézs 64:1"` → 0. |
| K3 | OK, pontatlan leírással | `eszkozok/karoli_strong/api_koteg.py:199–203` | Az `f21p/` diffje üres (`git diff --stat … -- f21p/`). A hash-ellenőrzést az `api_koteg.prompt_szoveg` végzi (`sonnet_koteg.prompt_hash_hiba`), nem a `prompt_ir`, ahogy a jelentés 10. sora állítja (l. ELTÉRÉS 5). |
| K4 | OK | jelentés 12–18, 23–25, 38, 113–119 | Benne van a kapuhiba, az arányok, a régi arany és a költség. A `/usage` helyett az API-költség szerepel, indokolva. |
| K9 | ELTÉRÉS | `adat/datasetek.tsv:90,93,96,99`; `adat/SEMA.md:936` | A tartományban egyik fájl sem változott (`git diff --stat`). A datasetek felsorolása „1Móz … Józs és Zsolt”. A SEMA 2.20 nem említi az Ézst. A jóváhagyott lista nincs frissítve (Ézs nélkül), és a `versmegfeleltetes_kezi.tsv` sincs dokumentálva. A Zsolt-körben ugyanez az 1. eltérés volt. |
| (3) Versmegfeleltetés, Ézs 9 | OK | `f22/versmegfeleltetes_kezi.tsv:4–7`; `f22/versosszevonas.tsv:6` | `lekerdez.py karoli "Ézs 9:17"` … `"9:20"`: K 9:17 „ifjaiban sem gyönyörködik” = TAHOT 9:16 (`'al-ken 'al-bachurav`). K 9:18 „gonoszság felgerjedt, mint a tűz” = TAHOT 9:17. K 9:19 = TAHOT 9:18. K 9:20 1–14. szó („…karjoknak húsát eszik”) = TAHOT 9:19 (18 token), a 15–34. szó („Manassé Efraimot …”) = TAHOT 9:20 (23 token). K 9:21 nincs („Nincs Károli-szöveg”). Az `_kezi_javitas` logikája törli a detektor `('', 'Ézs 9:17', nincs_karoli)` sorát. |
| (3) Versmegfeleltetés, Ézs 64 | OK | `versmegfeleltetes_kezi.tsv:8–10`; `versosszevonas.tsv:7` | K 64:1 1–11. szó („megszakasztanád az egeket … elolvadnának”) = TAHOT 64:1 (`lu' qara'ta shamayim`, 9 token). A 12–31. szó („mint a tűz meggyújtja a rőzsét …”) = TAHOT 64:2 (`kiqdoach 'esh hamasim`, 19 token). K 64:2 = TAHOT 64:3 (`ba'asotkha nora'ot`). K 64:12 nincs. Proveniencia: `lekerdez.py karoli` → `scope=range:Ézs 64:1 \| forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv \| n=1 \| ts=2026-10-08T10:00Z` |
| (4) jsonl formátum | OK | `f22/valaszok/sonnet/Ezs.jsonl` | A kulcssorrend Greppel (`"[a-z_]+": `) azonos a `Zsolt.jsonl`-éval: futas, modell, koteg, igehelyek, nyers, hivasok, probalkozas, forras, versek, allapot, hibak. Grep `"igehelyek": \[("Ézs …", ){9}"Ézs …"\]` → 129 sor (129 × 10 = 1290). A `"koteg"` értékek 1–129 közt mind előfordulnak, ismétlés nélkül. `git diff HEAD:f22/api_termeles/high/Ezs.jsonl HEAD:f22/valaszok/sonnet/Ezs.jsonl` → üres (az átvezetés bájtazonos). |
| (5) Korábbi könyvek táblái | OK | | `git diff --numstat cab9f48..HEAD -- adat/ konkordancia/` és `d288e08~1..HEAD`: csak a `parok_Ezs.tsv` és a `szavak_Ezs.tsv` jelenik meg, törlés 0. A `konkordancia/` nem változott. |
| (6) Proveniencia-sor | OK, nyelvi hibával | `parok_Ezs.tsv:1`, `szavak_Ezs.tsv:1` | Az alak `scope=manual \| forras=…versmegfeleltetes_kezi.tsv, versosszevonas.tsv… \| ts=manual`. A szövegben „a API (Batch)-futásnak” áll (l. ELTÉRÉS 4). |
| D16 | OK | `F22_KAROLI_STRONG_BRIEF.md:167` | Csak Sonnet, Batch, `effort=high` (futásnapló: `adaptive,effort=high`), kézi javítás, 7,08 USD; minden a fentiek szerint igazolva. |
| D16 / verziónapló | ELTÉRÉS | `F22_KAROLI_STRONG_BRIEF.md:173–183` | A D16-hoz nincs v2.10 sor; a legutóbbi a v2.9. A Zsolt-körben ugyanez a 2. eltérés volt. |
| Brief `ir` | ELTÉRÉS | `F22_KAROLI_STRONG_BRIEF.md:14` | Az `f22/api_termeles/*` (`futasnaplo`, `batchek`, `high/Ezs.jsonl`, `_munka/*.json`, `javitando.txt`) hiányzik az `ir` mezőből. |
| DT73 (a) | ELTÉRÉS | `api_koteg.py:54` | A DONTESEK.md:143 szerint „előtte a költségplafon (PLAFON_USD) a könyv méretére állítandó”. A `PLAFON_USD = 110.00` (F77.8) a teljes hátralévő ÓSZ-ra szól, az Ézsre nem lett méretezve. Kár nem lett belőle (7,08 USD). |
| DT57 | OK | brief:12, 167 | A D-sor és a `kovetkezo` alkalmazza (Ézs, utána Jer). |
| Futásnapló-címke | ELTÉRÉS | `futasnaplo.tsv:2–146` | A `futas` mező éles futáson is `vakproba/high/Ezs` (a cab9f48 kódja, `api_koteg.py:269`). |
| Ág / „session = egy feladat” | ELTÉRÉS | jelentés 136 | A végrehajtó maga jelezte. `git log main..HEAD`: az ág az F77.1–F77.10 commitokat is hordozza (9 F77 + 7 F22.Ézs). Felhasználói döntés kell. |
| ⛔ 2. megállás | OK | brief:9–11 | `allapot: megallt`; a `kovetkezo` a szúrópróbát, a 9:20/64:1 átnézést és az ágdöntést a felhasználóra hagyja. |
| Kulcs a diffben | OK | | `git diff d288e08~1..HEAD \| grep -c -E 'sk-ant\|x-api-key\|PARDES_API_KEY='` → 0 |
| CI | OK (egyezik) | | `futtat.py --valtozott $(git diff --name-only d288e08~1..HEAD) --diff-alap d288e08~1 --diff-fej HEAD`: kilépési kód 0. E2–E16, E19, E20, E26: 0 találat. E25: 3 JELENTES (CLAUDE.md:33, MUNKAMENET.md:67/181). E27: 90 JELENTES (FELADATOK.md, repószintű), HIBA nincs. Ugyanez `--diff-alap cab9f48` mellett. E17 nem jelzett. |
| A1 | OK | jelentés 7, 28 | A versmegfeleltetés tartalmi állítását lekérdezéssel igazoltam (l. 3). A modell-kimenet „javaslat”, nem „ellenőrizve”. |
| A2 | OK | jelentés 138–142 | A 22.6 szúrópróba és az `ELLENOR_F22_Ezs.md` valóban nyitott: a fájl a HEAD-en nem létezik. |
| A3–A5 | nem értelmezett | | Nincs tanulmány, párhuzam vagy tanító a diffben. |
| A6 | OK | | E12–E15: 0 találat |
| Lista 1: törölt sorok | OK | | `git diff --numstat`: 15 törölt sor. Brief 3 (`ag`, `kovetkezo`, `ir` cserélve), `api_koteg.py` 8 (F77.10, kontextus), `egyesit.py` 2 (formázósor), `tokenek.py` 1 (a jóváhagyott tuple), jóváhagyási napló 1 (a „függőben Ézs 9:17–20” sor kiváltva). Adatsor-törlés 0. |
| Lista 2: kulcstartomány | OK | | 66 fejezet (jelentés 2.1), 1290/1290 Károli-vers. A Strong mindenhol `H\d{4}` (25222/25222 er-sor). |
| Lista 3: nulla-diff hatóköre | rögzítve | | Üres az `f21p/` diffje és a régi `adat/karoli_strong/*` diffje (fájlszinten), a `konkordancia/` változatlan. Nem igazolt: a régi könyvek újraépítésének bájtazonossága az új `egyesit.py`/`tokenek.py`-jal (`--ellenoriz` nem futott). |
| Lista 4: táblasor Δ | OK | | `parok_Ezs.tsv` +25 488 adatsor (új tábla), `szavak_Ezs.tsv` +50 069 (új). Minden más `adat/` és `konkordancia/` tábla Δ 0. A bontás a jelentés 28. sorában van, az állapotonkénti számokat fent igazoltam. |
| Lista 5: ⛔ pontok | OK | | A versbeosztás-jóváhagyás (d288e08) a futás előtt történt. A ⛔ 2.-nél megállt. A párhuzamos (Batch) futást a DT73 (a) hagyta jóvá. |
| Tanulmány-ellenőrzés (F37 T4) | nem értelmezett | | Nincs `*_bovitett.md` / `*_tanulmany.md` a diffben. |

## Eltérések súlyossági sorrendben

1. **Közepes: K9.** Az Ézs-táblák nincsenek bejegyezve az `adat/datasetek.tsv`-be (90, 93, 96, 99. sor) és a SEMA 2.20-ba (936. sor). A SEMA jóváhagyott listája és a `versmegfeleltetes_kezi.tsv` mechanizmusa sem dokumentált.
2. **Enyhe–közepes: az ág.** Az F22.Ézs commitok az F77 commitjaival egy ágon vannak; felhasználói döntés kell.
3. **Enyhe: plafon.** A DT73 (a) könyvméretű plafonja nem valósult meg (110 USD maradt).
4. **Enyhe: proveniencia-sor.** „a API (Batch)-futásnak” helyesen „az API (Batch)-futásnak”. A hiba az `egyesit.py` 325–328. sorának formázásából jön.
5. **Enyhe: K3 a jelentésben.** A hash-ellenőrzést az `api_koteg.prompt_szoveg` végzi, nem a `prompt_ir`.
6. **Enyhe: verziónapló.** A briefből hiányzik a v2.10 sor (D16).
7. **Enyhe: brief `ir`.** Az `f22/api_termeles/*` hiányzik belőle.
8. **Enyhe: futásnapló-címke.** A `futas` mező éles futáson is `vakproba/high/Ezs`.

*Egyéb, nem számolt:* a jelentésben két „## 2.” címsor van. Üres `f22/api_termeles/javitando.txt` került a repóba.
