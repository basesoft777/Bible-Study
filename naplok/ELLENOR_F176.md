ELTÉRÉS: 9 tétel

# ELLENOR_F176 — `F176_VISSZHANG_ADAT_BRIEF.md` · `afbf4844..4364299e` (ág: `claude/f176-visszhang-adat-c1579f`)

*A `fuggetlen-ellenor` subagent jelentése (modell: `claude-opus-5-5`); a subagent fájlíró eszköz nélkül futott, a szöveget az orkesztrátor mentette változtatás nélkül, a második CI-futás sorával kiegészítve. Utólagos megjegyzés az orkesztrátortól a végén.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | Saját modellem `claude-opus-5-5`, a kért `opus`: egyezik. A végrehajtó a jelentésében `claude-sonnet-5-5`-öt ír (`naplok/F176_jelentes.md:3`). Ezt nem tudom ellenőrizni, és adattáblába nem került `modell` mező. |
| Hatókör: `ir` | ELTÉRÉS (indokolt, alacsony) | `nyilt_mag/*` (6 fájl) | `git log --stat afbf4844..HEAD`: a `0809170a` csak a `nyilt_mag/`-t írja. A `forrasok_es_licencek.tsv` +5 sora megegyezik a `licencek.tsv` +5 sorával; a többi változás hash, sorszám (54→59) és a kizárt-lista. Mechanikus következmény, külön commitban, a jelentés 5. pontja megindokolja. Az `ir` mezőn mégis kívül esik. |
| Hatókör: lexikon | OK | — | `git log afbf4844..HEAD -- eszkozok/lexikon_general.py lexikon/` → 0 commit. `git diff --name-only … -- lexikon eszkozok/lexikon_general.py konkordancia/BDB_teljes_unabridged.tsv .github` → üres. |
| 6.3 / 6.5 ⛔ (Sefaria ÁSZF, BDB-licencmező) | ELTÉRÉS (súlyos) | `adat/licencek.tsv` (Targum_PD, BDB_rokon_irasok sor); `dontesek/uj/…md:2` | Az ÁSZF szövege szerint („…commercial use is strictly prohibited … unless expressly stated otherwise”) a forrás nem szabadon „kimenetbe tehető”. A végrehajtó maga állította a két sort `kereskedelmi=feltetelesen`-re, ez eltérés a várt „közkincs” értéktől. A BDB-nél a brief „licencmezőt” várt, de licencmező nincs (`F176_jelentes.md:135`). Mindkettő a 6.3 („eltér a várt értéktől”) és a 6.5 alá esik („tartalmi döntés … helyőrzővel, **majd megállás**”). A DT-F176b létrejött, a megállás elmaradt: az F176.3 ugyanazon ÁSZF alatt API-ról töltött. A nyílt magból kizárás nem elég, mert a brief 2. pontja szerint a fizetős lexikonlap is kimenet, a DT-F176b (a) opciója pedig éppen ott engedné. |
| 6.5 ⛔ / 4.2 (versszámozás, DT-F176a) | ELTÉRÉS (közepes) | `konkordancia/Vulgata_Clementina.tsv:14358`, `Targum_PD.tsv:14344`, `Vulgata…:22001` | Az `igehely` a forrás számozását hordozza magyar könyvnévvel, és a `karoli_kulcs=igen` hamis egyezést jelez. Igazolás: `lekerdez.py karoli "Zsolt 23:1"` → „Az Úr az én pásztorom”, miközben a Vulgata „Zsolt 22:1” = „Dominus regit me” (`igen`). `karoli "Jóel 2:28"` → „kiöntöm lelkemet”, ez a Targum „Jóel 3:1”-e (`igen`). `karoli "Dán 3:24"` → Nabukodonozor megijed, a Vulgata „Dán 3:24” viszont az Azariás-kiegészítés (`igen`). Ez a CLAUDE.md F85-konvenciójával (igehely = Károli-vers) ellentétes, és igehely szerinti join esetén csendes hibát ad. A brief 6.5 ezt az esetet („versszámozás-feloldás”) kifejezetten megállási pontnak írja. |
| F176.1 sorrend | ELTÉRÉS (alacsony) | — | `git log --format="%h %ad %s"`: az F176.2 adatcommit (`34728ffb`, 09:41) a licenc-commit (`54f02993`, 09:57) előtt van. Ha egy licenc NC lett volna, az adat már a történetben lenne (a brief 2. pontja: „NC … a privát repóban is” kizáró). |
| Licencsorok szó szerint | NEM ELLENŐRIZHETŐ | `licencek.tsv` +5 sor; `VISSZHANG_README.md:39–113` | Webes elsődleges helyek, lekérdezéssel nem igazolhatók. Belső összhang: a `licencek.tsv`, a README és a jelentés 1. pontja ugyanazokat a mondatokat idézi (`git diff … -- adat/licencek.tsv`). |
| 3. pont / ⛔ 3 (NC/BY-SA) | OK | `eszkozok/visszhang/targum_import.py:48` | A kód nem-PD verziónál `SystemExit`-tel áll meg. A Targum fejléce: „csak a license=Public Domain verziók”. Más kizárt forrás nem került be: `git diff --name-only`. |
| Targum 1Móz 1:1 | OK | `Targum_PD.tsv:8` | „בְּקַדְמִין בְּרָא יְיָ…”, Onkelos. `lekerdez.py karoli "1Móz 1:1"` → „Kezdetben teremté Isten…”. |
| SBLGNT szúrópróba | OK | `SBLGNT_apparatus.tsv:4799, 6940` | A Róm 3:31 `nem` jelzése helyes: `lekerdez.py karoli "Róm 3:31"` → „Nincs Károli-szöveg”, mert a Károli a 3:30-ba vonja. A Jel 22:21 jegyzete szó szerint áll, alapszöveg nincs. |
| THGNT-szöveg | OK (megjegyzéssel) | `TAGNT_valtozatok.tsv:845, 4668, 6560, 9066` | Grep `\tTyn\t`: a 4 csak-Tyn sor `gorog` mezője üres, a Meaning/Spelling oszlop nincs a táblában. Megjegyzés, nem a diff hibája: a meglévő `TAGNT_kivonat.tsv:12292` már hordoz csak-Tyn alakot („Ἰησοῦ,”). |
| TAGNT `hianyzik_ebbol` | ELTÉRÉS (alacsony) | `TAGNT_valtozatok.tsv:501, 5803` | Grep `[»«]\d+[»«]\d+` → 2 sor. A `Tyn»4»4` / `Tyn»1»1` alaknál a `re.sub(r'[»«]\d+$','',…)` csak egy utótagot vág le, ezért a `hianyzik_ebbol`-ba tévesen „Tyn” kerül, holott a Tyn-ben a szó megvan (csak áthelyezve). |
| `csv` modul | OK | `eszkozok/visszhang/*.py`, `teszt_visszhang.py` | Grep `import csv\|csv\.(reader\|writer\|Dict)` → 0. Az írás a `kozos.ir_tsv` `'\t'.join`-jával megy, tab- és sortörés-őrrel. |
| BDB: H7843 alakjai | OK | `BDB_rokon_irasok.tsv:14–17` | arab „سَحَتَ”, etióp „ሰሐጠ”, szír „ܫܰܚܶܛ”. Ellenpróba a repó BDB-szövegével (Grep `^H7843\t` a `BDB_teljes_unabridged.tsv`-ben): „Arabic extirpate; Ethiopic injure”, vagyis az írásjelek ott valóban elvesztek. |
| BDB: tokenminőség | ELTÉRÉS (alacsony) | `BDB_rokon_irasok.tsv:17` | Az egyetlen „ܬ” betű („assim. of ܬ”) nem rokon szóalak, mégis `szír` sorként szerepel. |
| BDB: `kontextus` | ELTÉRÉS (alacsony, dokumentált) | `F176_jelentes.md:177` | A brief „a BDB-fej rövid szakaszát” kérte, a kód a token körüli ablakot veszi. Megindokolva, de eltér. |
| BDB: hézagok | OK | `BDB_rokon_irasok.tsv:5, 8` | `bdb_szócikk=0` a H1863-nál és a H6093-nál. A jelentés „hiány”-nak jelöli, nem negatív leletnek; nyitva tartja az N-F176b. |
| BDB: második futás | NEM ELLENŐRIZHETŐ (futtatással) | `teszt_visszhang.py:134–149` | A teszt létezik: második futás `keres2 == 0`, a lekérő hívása `AssertionError`. Kódolvasás alapján a `fut()` a `# lekérdezve:` sorral kihagyja a lekérést. Futtatni nem tudtam, a parancs a szerepkörömön kívül esik. |
| User-Agent | OK | `bdb_rokon.py` `UA = 'PaRDeS-research/1.0'`, `MIN_KOZ = 1.1` | Grep `User-Agent\|@[a-z]` az `eszkozok/visszhang`-ban: e-mail nincs. |
| Arány-kapu: küszöb | OK | `nyilt_mag_kapu.py` `ARANY_FIGY=1.0`, `ARANY_HIBA=5.0` | A szigorú `>` miatt a pontos 1%, illetve 5% még nem lép át; a teszt (`:77–81`) ezt rögzíti. A tételszám a README `tetel` oszlopából vagy a `datasetek.tsv` `fajl`-sorszámából jön, nincs a kódba írva. |
| Arány-kapu: ismeretlen tételszám | ELTÉRÉS (alacsony) | `nyilt_mag_kapu.py` `ell_arany` | A `ismeretlen` szint csak infósort ír, se FIGY, se BUKÁS nem lesz belőle. A TBESG (6 tétel) így semmilyen szinten nem jelez: Grep `TBESG` a `datasetek.tsv`-ben → nincs saját dataset-sora. |
| `teszt_visszhang` / `nyilt_mag_kapu` / `ellenoriz` / `feladatok ellenoriz` | NEM ELLENŐRIZHETŐ | `F176_jelentes.md:196–220` | A szerepköröm szerint ezeket nem futtathatom. A jelentés zöldnek mondja őket, ezt nem fogadom el igazolásnak. |
| CI (`futtat.py`) | OK (nincs HIBA) | — | Parancs: `python eszkozok/ellenorzes/futtat.py --valtozott <a 27 változott fájl> --diff-alap afbf4844 --diff-fej HEAD`, kilépési kód 0. Az E2–E16, E19, E20, E26, E28, E29, E31–E33 és E35 0 találatot adott. E25: 3 JELENTÉS (régi). E27: 42 JELENTÉS (régi hivatkozások). E30: 2 FIGYELMEZTETÉS, a `54f02993` commit üzenetében ékezet nélkül áll a „kozkincs” és a „tisztazott”. E34: 45 FIGYELMEZTETÉS (régi `elofordulasok.tsv`). Végrehajtói CI-jelentés nem volt a bemenetben, így nincs mivel összevetni. |
| DT/N végleges szám | OK | — | `git diff … ':!konkordancia/*.tsv' \| grep "^+" \| grep -o -E "(DT\|N)-?F?[0-9]+[a-z]?"`: csak DT-F176a/b, N-F176a/b/c, illetve a meglévő DT-F33d/g. A csupasz `(DT\|N)[0-9]+` minta 0 találatot ad. Az `eszkozok/`-ban nincs helyőrző string-literálban (E32). |
| Nyers fájl | OK | — | `git diff --name-only … \| grep -E "\.(zip\|json\|usfm\|txt)$"`: csak a generált `nyilt_mag/KIADAS.txt` és `RELEASE.txt`. Törölt fájl nincs. |
| Ellenőrzőlista 1: kiszűrt sorok | OK | `F176_jelentes.md:153–157` | Vulgata: 12 968 lábjegyzet és 7 deuterokanonikus könyv kimaradt. SBLGNT: 27 címblokk. TAGNT: 142 095 szóból 130 318 kiszűrve. Targum: üres vers 0. Törölt sor a diffben nincs (numstat: `…\t0\t…`). |
| Ellenőrzőlista 2: kulcstartomány | OK | — | Targum 26 mű: Onkelos 5 könyv, Jonatán 21 = Josh–Mal prófétai kánon. A HAMART-001 mind a 8 Strongja szerepel a `# lekérdezve:` sorokban. |
| Ellenőrzőlista 3: nulla-diff | OK | — | Nulla-diff: lexikonlapok, `lexikon_general.py`, `BDB_teljes_unabridged.tsv`, `.github/`. Nem nulla: a `nyilt_mag/` (l. hatókör). |
| Ellenőrzőlista 4: sor-Δ (fejlécsor és `#` nélkül) | ELTÉRÉS (alacsony) | `F176_jelentes.md:145–157` | `git diff --numstat` alapján: `datasetek.tsv` +5, `licencek.tsv` +5, `Targum_PD` +15 142 (új), `Vulgata_Clementina` +31 434 (új), `SBLGNT_apparatus` +6 934 (új), `TAGNT_valtozatok` +11 777 (új), `BDB_rokon_irasok` +6 (új). A Targum Onkelos/Jonatán bontása darabszám nélkül áll a naplóban. Saját mérés: Grep `\tOnkelos\t` → 5 846, `\tJonatan\t` → 9 296, összesen 15 142. `karoli_kulcs=nem`: Targum 96, Vulgata 1 269 (Grep), egyezik a naplóval. |
| Ellenőrzőlista 5: ⛔ | ELTÉRÉS | — | A 6.3 és a 6.5 nem teljesült (l. fent). A 6.1, 6.2 (#162, #170 `allapot: lezarva`) és a 6.4 OK: az ÁSZF a letöltést és az API-t megengedi (idézet a naplóban, webes forrás, nem ellenőrizhető). |
| A1 | OK | `F176_jelentes.md:34, 37–43` | A webes és jogi állítások értelmezésként vannak jelölve („jogi véleményt nem adok”, „Leltár, nem jogi vélemény”). |
| A2 | OK | `nyitott/uj/…md:1–3` | Az N-F176c valóban nyitott: Grep `teszt_visszhang` a `.github`-ban → 0. Az N-F176b nyitott: `bdb_szócikk=0`. |
| A3–A5 | n/a | — | Nincs tanulmány, párhuzam vagy nevesített tanító a diffben, ezért a Tanulmány-ellenőrzés (F37 T4) sem él. |
| A6 | OK | — | E12–E15: 0 találat (`futtat.py`). |

ELTÉRÉS-ek súlyosság szerint:
1. **⛔ 6.3/6.5 – nem állt meg.** A Sefaria ÁSZF kereskedelmi korlátozása és a hiányzó BDB-licencmező eltérés a várt licenctől, és a DT-F176b tartalmi döntés. A helyőrző elkészült, a megállás elmaradt, az F176.3 lekérései utána futottak.
2. **Igehely-kulcs és `karoli_kulcs` hamis egyezés** (Zsolt 22/23, Jóel 3/2:28, Dán 3:24), a 6.5 versszámozás-pontjánál ugyanígy megállás nélkül.
3. A licenc-commit az adatcommit után jött.
4. A TAGNT `hianyzik_ebbol` 2 sorban hibás.
5. Egybetűs szír token a BDB-táblában.
6. Az arány-kapu ismeretlen tételszámnál nem jelez.
7. A `kontextus` nem a BDB-fejből jön.
8. A `nyilt_mag/` írása az `ir` mezőn kívül esik (indokolt).
9. A Targum sorbontása darabszám nélkül áll a naplóban.

## Orkesztrátori megjegyzés (2026-11-08, az ellenőrzés után)

- Az 1. tétel kérdését (DT-F176b) a felhasználó az ellenőrzés után eldöntötte (a lexikon-orkesztrátoron át, szó szerint: „szerintem ez az irányadó”; „mehet”): `kereskedelmi=igen`. Átvezetve: F176.6 / F176.6b. A megállás elmaradása mint folyamathiba a javítókör (`/elteres F176`) tárgya marad.
- A 2–9. tétel nyitott; a 2. (DT-F176a, versszámozás) tartalmi döntés.
