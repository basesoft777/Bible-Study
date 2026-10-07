# ELLENOR_F72 — F72_BDB_ARAM_BEEMELES_BRIEF.md · origin/main(73d4651)..claude/bdb-aram-beemeles(19dcaa7)

*A `fuggetlen-ellenor` jelentése; a fájlt az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze). Eredmény: ELTÉRÉS, 7 tétel.*

**Módszertani megjegyzések:** (a) a munkakönyvtár ellenőrzés közben átváltott a régi helyi `main`-re; a BDB-táblák a base és a head között csak az F72 diffjében térnek el, így a megállapítások mindkettőre érvényesek. (b) Két `git diff` kimenet `head`/`tail`-lel vágva; tartalmi hatás nincs. (c) A `lekerdez.py` alparancsai a BDB-táblákat nem kérdezik le; a táblaállításokat `git diff` és Grep igazolja.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| G1 (alias +164) | ELTÉRÉS | `konkordancia/BDB_strong_alias.tsv:298-459` | `git diff --numstat` → 162 hozzáadott sor; a brief 164-et ír. Oka: a KIZAR lista (H2298, H5839). A 162 sor hibátlan, a testvérkulcsok léteznek. |
| G2 (fő tábla +6 a végén, régi bájtok) | OK | `BDB_teljes_unabridged.tsv:8095-8100` | hunk `@@ -8092,3 +8092,9 @@`, csak `+` sorok; kulcssorrend egyezik. |
| G2b (alias régi bájtok) | OK | `BDB_strong_alias.tsv:295` | hunk `@@ -295,3 +295,165 @@`, 0 törölt sor. |
| G3 (H0004, H3769, H5013 nincs a táblákban) | OK | – | Grep: csak az `aram_potlas` és az `elvetett` táblában szerepelnek. |
| G4 (proveniencia) | OK | `BDB_strong_alias.tsv` | 162 találat a `forras=eszkozok/bdb_aram_beemeles.py --m2 … ts=2026-10-07` mintára; a fő tábla 3 oszlopos, a 6 sor proveniencia-sora a zárásban áll. |
| G5a (teszt zöld) | NEM ELLENŐRIZHETŐ | `eszkozok/teszt_bdb_aram_beemeles.py` | az ellenőr nem futtathatja; a kód olvasva rendben. |
| G5b (#38 nem lett újragenerálva) | OK | `naplok/BDB_ARAM_BEEMELES_zaras.md:13` | az F38 brief diffje üres; a brief fejlécének `ad` mezője ennek ellenére „újragenerálva” állapotot ír. |
| D1 / döntésnapló | ELTÉRÉS | `F72_…BRIEF.md:3,11,55,63-65` | a 164 → 162 változás és a KIZAR-döntés nincs v2 sorként a döntésnaplóban; a `cim`, `ad`, G1 még 164-et ír; „jelölt: 3” helyett 5. |
| KIZAR H5839 indoklása | ELTÉRÉS (súlyos) | `eszkozok/bdb_aram_beemeles.py:42` | az 5467. sor (H5838): „comrade of Daniel … = נְגוֺ עֲבֵד” a H5839 szövege; az elvetett tábla testvére is H5838. A helyes alias H5839 → H5838 lett volna, így a #38 nem éri el a H5839-et. |
| KIZAR H2298 indoklása | ELTÉRÉS | `bdb_aram_beemeles.py:40` | a H0259 sora (237.) tartalmazza a H2298 szövegét. A `kezi_elfogadott` döntés a BDB-azonosítóról (BDB9285) szólt, nem a táblasorról; a H2298 → H0259 alias BDB9285 `bdb_id`-vel nem mondana ellent. A brief célja két Strongon nem teljesül. |
| NK1 (elvetett tábla változatlan) | OK | – | `git diff --stat` üres. |
| NK2 (testvér nincs az elvetett táblában) | ELTÉRÉS (enyhe) | `szarazfutas.md:11` | a H3606 → H3605 kézi ellenőrzésének eredménye nincs rögzítve; tartalmilag helyes (3367. sor). |
| NK3 (részleges pótlás = teljes szócikk) | OK | `bdb_aram_beemeles.py:95` | a H1753 szövegének ismétlődő tagmondata a forrásból öröklődik. |
| Proveniencia formátuma | ELTÉRÉS (enyhe) | `bdb_aram_beemeles.py:45-48` | a brief `bdb_aram_potlas.py --duplikacio`-t ír elő; a sorokban `bdb_aram_beemeles.py --m2` áll; elírás: „sorveegen”. |
| A1, A3, A4, A5, A6 | OK | – | nincs értelmező próza, tanulmány, tanító a diffben; E12–E15 0 találat. |
| A2 (nyitott tételek) | ELTÉRÉS | `NYITOTT_FELADATOK.md:614`; README:141-142 | (1) az N51 nincs helyőrzővel lezárva (a brief 5. lépése); (2) a README elvetett-szakasza még „172 jelölt marad”-ot ír, pedig 168-at az F72 kezelt. |
| N-F72a helyőrző | OK | `NYITOTT_FELADATOK.md:55` | formátum rendben, végleges szám nincs. |
| CI-egyezés | NEM ELLENŐRIZHETŐ | – | helyi futás: E2–E16, E19, E26: 0 találat; E25: 3 találat a `CLAUDE.md`/`MUNKAMENET.md`-ben, nem a diffben. |
| Törölt/kiszűrt sorok; kulcstartomány; nulla-diff; sorszám-Δ | OK | – | táblasor nem törlődött; 170 elfogadott = 162 alias + 6 szöveg + 2 KIZAR; további jelölt 3. |
| ⛔2 jóváhagyás az írás előtt | NEM ELLENŐRIZHETŐ | `zaras.md:5` | a repóból nem igazolható; a commitsorrend megfelel a briefnek. |
| ⛔4 (#38 újragenerálása) | OK | – | nem futott. |
| SHA-256 | NEM ELLENŐRIZHETŐ | `zaras.md:9-11` | hash-számolás nem engedélyezett parancs. |

**ELTÉRÉS-ek súlyossági sorrendben**
1. H5839 kizárása: a helyes testvér (H5838) tartalmazza a szöveget, hiányzik egy elérhető alias.
2. H2298 kizárása: a szöveg a H0259 sorában van, az „ellentmondana” indoklás nem áll meg.
3. A döntésnaplóból hiányzik a v2 sor (164 → 162), a fejléc és a G1 elavult.
4. Az N51 nincs lezárva/frissítve; a README elvetett-szakasza elavult.
5. A H3606 kézi ellenőrzésének eredménye nincs dokumentálva.
6. A proveniencia `forras` mezője eltér a brieftől; elírás: „sorveegen”.

---

# 2. kör — origin/main(73d4651)..claude/bdb-aram-beemeles(c3a423f)

*A fájlt az orkesztrátor mentette. Eredmény: ELTÉRÉS, 6 enyhe (dokumentációs) tétel; az 1. kör mind a 7 eltérése megoldódott. A 6 tételt az F72.7 (e2253fe) javította.*

**Táblaadat — OK:** 164 alias-sor (`git diff --numstat`: 164/0); H5839 → H5838 (BDB9760) és H2298 → H0259 (BDB9285) megvan; a régi alias- (296) és fő tábla (8093) sorai bájtra azonos prefix, 0 törölt sor; az elvetett tábla, az F38 brief és a `BDB_FORDITAS_M0.py` változatlan; a #38 sorrendjének 648 soros kész előtagja változatlan, a 9 új sor (H1753, H3367, H3848, H6433, H7560, H8065, H0747, H4123, H4725) pontosan egyszer szerepel; H0004, H3769, H5013 egyik táblában sincs.

**2. köri eltérések (mind javítva az F72.7-ben):**
1. az újragenerálás nem volt dokumentálva a zárásban és az N51-ben (+9 bontása, H4725 gyakorisága 401, az adagok eltolódása → DT-F67a hivatkozás);
2. a brief v3 és a README a H2298 → H0259-et „indokolt felülírásnak” nevezte, pedig automatikus egyezés (0,947);
3. az `ir` fejlécből hiányzott a `bdb_sorrend_ujragen.py`, a `BDB_FORDITAS_sorrend.tsv`, az `ELLENOR_F72.md`;
4. N-F72a: 162 → 164;
5. a brief nyitott kérdéseiben elavult számok (161 → 162, kivétel 2);
6. README:141 alias-darabszám: 296 → 460.

**NEM ELLENŐRIZHETŐ (az ellenőr eszközeivel):** a teszt futtatása, a SHA-256, a CI-jelentés egyezése (helyi futás: E2–E16, E19, E26: 0 találat; E25 a diffen kívül), a #38 sorrend Strong-egyediségének teljes ellenőrzése, a ⛔2/⛔4 jóváhagyás (a repóból nem igazolható; a döntésnapló „felhasználó, chat”-ként rögzíti).
