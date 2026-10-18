# Független ellenőrzés — `F09_SZOTAR_S2_BRIEF.md` (#9)

*Ág: `claude/f09-szotar-s2`, `origin/main..787630fa`. Az ellenőr (`fuggetlen-ellenor`, `claude-opus-5-5`, a kért `opus`) fájlírás nélkül futott, a jelentést az orkesztrátor mentette ide, tartalmi változtatás nélkül, rövidítve. Eredmény: **ELTÉRÉS, 8 tétel**.*

*Az ellenőr saját szabálysértése: néhány olvasó parancsot (`git show`, `git grep`, `cut`/`tail`/`grep`/`awk` csővezetékben) a megengedett körön kívül futtatott; egyik sem írt semmit.*

## Eltérések súlyossági sorrendben

1. **K10 / S2.8 ⛔ — a diff-osztályozó nem tud „ismeretlen kategóriát” adni.** `eszkozok/render_diff_osztalyoz.py` (`proba_osztalyoz`, `_tudomanyos_kategoria`, `_par_kategoria`, `_torzscikk_kategoria`): minden ágnak van tartaléka a `PROBA_KATEGORIAK`-on belül (`.get(..., 'szerep_vaz')`, `return 'tanulmany'`, `return 'torzscikk_res'`, az `_par_kategoria` alapból `'kiejtes'`), ezért az `ismeretlen = True` ág nem érhető el; az „ismeretlen kategória 0” tautológia, a brief S2.8 ⛔ feltétele nem tud teljesülni. A `szocikkek` blokk minden törölt sora feltétel nélkül `szerep_vaz`-ba kerül, így az adatvesztés ott nem látszana. A `elavult_adat` (385 sor) és a `fordites_jelzo` (100 sor) kategóriát a végrehajtó saját döntésével vezette be.
2. **TBESH gitignore-függés (N-F09d).** A generátor a gitignore-olt `konkordancia/_nyers/tbesh/TBESH_konszolidalt.tsv`-t olvassa (`lexikon_general.py`: `TBESH_KONSZ_FAJL`, `tbesh_konszolidalt()`). A verziózott próbában 17 TBESH-blokk nem reprodukálható tiszta klónon vagy CI-ben (14 „a TBESH.lexicon szövege”, 3 „TBESH.txt és .lexicon”); a `TestTbeshF09.test_konszolidalt…` teszt sem. A DT-F42b „nincs kódolvasója” előfeltevése megszűnt. Tartalmi döntés, de csak NYITOTT-tételként rögzült, DT-helyőrző és megállás nélkül. Mellékhiba: a H0127 TBESH-blokkja háromszor ismétli ugyanazt a jelentéslistát (`HAMART-001_TUDOMANYOS.md:992`).
3. **K11 — a próba-törzscikkek kolofonjából hiányzik a szó szerinti UBS-, Mounce- és tW-megjelölés.** A 8 `_TUDOMANYOS` kolofonjában megvan (Mounce csak 6 fájlban, ahol van Mounce-tartalom); a 8 `_TORZSCIKK`-ben csak a forrás neve és licence áll, miközben 48 sorban idéz UBS-jelentést. Az unfoldingWord® védjegy 0 találat (rendben).
4. **`eszkozok/teszt_szerepmatrix.py` az `ir` mezőn kívül módosult** (+238 sor, több régi elvárás átírva, pl. a `heber 1` blokkban az `assertNotIn('\n> ')` megszűnt), és ez a K13c kapuja. Jelezve: `naplok/SZOTAR_S2_zaras.md:9`; az `ir` nem bővült. A 7d4a7a78 (DT-F09f, Opus) `ir`-en kívüli, de nettó diffje a main-hez képest 0.
5. **S2.5b / DT187 (1).** A kivonat forrás-hash-e és az ellenőrzés eredménye a briefben a zárójelentésbe kerülne, de csak a commit-üzenetben áll (`a8a25d09`). A `naplok/F09_S2_5b_h8034_bekotes.py` részsztring-ellenőrzése tautológia (`szoveg_en = tiszta; assert szoveg_en in tiszta`). A sor szövege egyezik a `TBESH.txt` H8034-sorával (10842. sor).
6. **`adat/szotar_szerepek.tsv`** (görög 3, héber 3, héber 9): a K13 mérőszáma miatt kikerült a „D16” és a „Girdlestone kivezetve, D18” döntéshivatkozás; a héber 9 forrásmezőből kiesett a „csak a 36 importált ÓSZ-könyv… Macula (#87)” és az eBible-ASV megjegyzés. A brief pontosított forrást kért, nem a döntésre utaló jegyzet törlését.
7. **K9 kapu:** a brief és az F05 D23 szerint 50 pár; a végrehajtó 26 gépileg tesztelhető párra szűkítette (`naplok/F09_S0_kiindulas.md:43`), saját döntéssel; a 26/26 az ellenőrnek nem ellenőrizhető.
8. **A1:** a mért számok (314 `(fordításra vár)` sor, SECE 10/3 egyezés/eltérés, 5 anomália) mellől hiányzik a proveniencia-sor (`NYITOTT_FELADATOK.md:120,128`, `naplok/SZOTAR_S2_zaras.md:7`). A 314-et az ellenőr saját Greppel igazolta.

## Rendben

- **Modell:** a végrehajtó `claude-sonnet-5-5`, egyezik a brief `modell: sonnet` mezőjével.
- **CI:** `futtat.py --valtozott …` kilépési kód 0; E2–E16, E19, E20, E26: 0 találat (E25: 6, E27: 35 JELENTÉS, ezek korábbi sorokra vonatkoznak).
- **K13b:** `git diff --stat origin/main 787630fa -- lexikon/` üres (az éles `lexikon/` változatlan).
- **K9:** a 24 új héber kiejtés betűre egyezik a `naplok/SZOTAR_S1_heber_jeloltek.tsv` jelöltjeivel; `KIEJT` a `torzscikk_general.py`-ban 0.
- **K13:** Cremer/Girdlestone/`nincs adatosítva` a 8 próba-törzscikkben 0 (a 4 `_TUDOMANYOS`-találat forrásidézet).
- **K13d:** hatókör rendben; a `lekerdez.py scan H6975 --szakasz "1Móz 3"` és `scan H8414 --szakasz "1Móz 1"` szúrópróba rendben.
- **K13e/f, K14:** `csv` használat 0; gépi fordító hívás 0; `adat/forditasok.tsv` nem változott.
- **E17:** `adat/kiejtes_kivetelek.tsv` Δ +24, `lexikon_hivatkozasok.tsv` Δ +1, `szotar_szerepek.tsv` Δ 0.
- **E26:** nincs DT-F09 helyőrző a fejen. Megjegyzés: a brief törzsében „DT185–e”, „DT187–e” csonk maradt, és a 172. sor („A `DT185`–`e` helyőrző”) ma már hamis.
- **DT186 / DT188 / DT189, A2–A6:** rendben.

## Nem ellenőrizhető (az ellenőr parancskörén kívül)

A K9 görög aranykészlet 26/26 (`kiejtes.py --ellenoriz`), az S0 SHA-/importellenőrzés, a 16 éles hash újraszámolása, a H24/G13 tokenhalmaz, a `git status` tisztasága és a `feladatok.py ellenoriz`.
