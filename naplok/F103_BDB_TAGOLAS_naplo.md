# F103 — BDB_TAGOLAS: munkanapló

*FELADATOK #103 · ág `claude/f103-bdb-tagolas` · végrehajtó: `claude-opus-5-5` (kért: `opus`) · 2026-11-09*

Mérőszkript: `naplok/F103_BDB_TAGOLAS_meres.py` (előtte és utána ugyanez; csak olvas, a `--tsv` a régi alakok listáját írja a
`naplok/`-ba). A mérések definíciója a szkript docstringjében. Az aranyminta 184 `csoport` sora a teszteset (brief 3./1.).

## 1. Előtte-mérés (F103.1)

*proveniencia: scope=aranyminta (adat/bdb_aranyminta.tsv) + teljes angol BDB (8099) + magyar BDB (8099) | forras=BDB_teljes_unabridged.tsv@d4b15b2faea6
+ forditasok.tsv@0be309b96bc3 + bdb_aranyminta.tsv@ea74da96324d + bdb_szelet.py@dc48b1a0af51 (HEAD 3e6ed664) + naplok/F103_BDB_TAGOLAS_meres.py | ts=2026-11-09T19:01*

| mérés | előtte |
|---|---|
| aranyminta, angol: várt csoport | 184 |
| egyező csoport | **0** (a szeletelő nem bont csoportra) |
| hamis határ (angol) | 0 |
| aranyminta, magyar: várt bontás (szülő-csomópont, ahol minden angol csoportnak van magyar horgonya) | 47 |
| magyar bontás | 0 |
| jelentéspont, seed-102 véletlen 200 (`m2_minta_osszevet.py --mai-tabla`) | **183** (91,5%) — azonos a #102 zárómérésével |
| könyv/vers, seed-102 | 199 |

A magyar BDB ma 8099 szócikk (a DT167 idején 674): a 2. pont „674 kész szócikk” mérése a mai teljes magyar állományon fut.

## 2. Csoportbontás és utána-mérés (F103.2–F103.4)

*proveniencia: scope=aranyminta + teljes angol BDB (8099) + magyar BDB (8099) | forras=BDB_teljes_unabridged.tsv@d4b15b2faea6 + forditasok.tsv@0be309b96bc3
+ bdb_aranyminta.tsv@ea74da96324d + bdb_szelet.py@0620e7ae9686 (HEAD 1e08840a) + naplok/F103_BDB_TAGOLAS_meres.py | ts=2026-11-09T19:15*

A bontás a `bdb_szelet.py` kiegészítő függvényeiben (`csoport_bont`, `csoport_magyar`, `csoport_bejar`, `csoport_savok`); a `szeletel()`
kimenete változatlan (teszt: `test_szeletel_kimenete_valtozatlan`), ezért a lexikonlapok és a 2.29 `utvonal`-a nem mozdul. Szabály: DT167 (1) (a);
a kódolt részletek: zárójelen belüli bevezető nem nyit (a szeletelő 400 karakteres `_zarojelben` szabálya, a lezáratlan OCR-zárójel nem némít);
a törzs számozott jelentései előtti alaklista nem kap csoportot; a zárójeles harmadik szint sorozat (1-től / a-tól, legalább két tag; `(I)`,
`-2`, görög betű is), a prózai felsorolás („by (1) … and (2) …”, kötő- vagy viszonyszó után, a csomópont fején túl) nem; a bevezető közvetlenül
a zárójeles jelölő előtt egy csoport („especially (3)”). Magyarul: DT-F103b.

| mérés | előtte | utána |
|---|---|---|
| aranyminta, angol: egyező csoport / 184 | 0 | **164** |
| hiányzó csoport | 184 | 20 — mind szerkezeti okú (a szülő-csomópont hiányzik a szeletelőben; N-F103c) |
| hamis határ (angol) | 0 | 18 — mind szerkezeti okú (rossz szülő); **csoportszinten 0** |
| aranyminta-sorrend eltérés (a horgony a szülő másik csoportjánál; H7121 Qal 4/a, a minta E11-es sora +2-ként került a szövegben előbb álló csoport mögé) | — | 2 |
| magyar: bontott szülő / ebből a minta szerint várt | 0 | 41 / 39 |
| magyar: eltérő jelölőkkel bontott | 0 | **0** |
| magyar: a minta szerint várt, nem bontott (a mai fordítás jelölő-sorozata eltér: DT167 (5) (a) szerint helyes) | 47 | 8 |
| magyar: bontott, a mintában horgony nélkül (H8213 Qal/1 „képletesen” — a minta magyar horgonya üres; H0834 8/f — szerkezeti) | — | 2 |
| teljes angol BDB: csoport / csoportos csomópont | 0 | 3707 / 1846 |
| teljes magyar BDB: bontott csomópont (egyező sorozat) / csoport | 0 | 742 / 1376 (angol nélküli bontás: 0) |
| jelentéspont, seed-102 véletlen 200 | 183 | **183** (nem romlott; a 2.29 sorai bájtra azonosak) |

Bevezetőnként (teljes angol BDB): with 1187, zárójeles 919, followed by 523, absolute 375, figurative 356, especially 267, opposed to 64,
in phrase 14, Inf. abs. as adverb 2. Az utolsó kicsi szám valós: a mondatkezdő „Inf(initive) abs(olute)” a forrásban szinte mindig alaklista
(„Infinitive absolute הַבְדֵּל Isa 56:3; construct …”), nem határozószói használat.

A 2.29 tábla újragenerálva (`bdb_vers_jelentes.py --ts 2026-11-09`, kilépési kód 0; mtime 18:52:44 → 19:14:24; `--ellenoriz`: bájtra azonos,
kód 0): csak a `# forras:` fejléc kód-hash-e változott (`bdb_szelet.py` d1c18ba93efe → 0620e7ae9686), a 162 053 sor azonos.

Terminológia (a 4. lépés mérése, N-F103a): `naplok/F103_BDB_TAGOLAS_regi_alakok.tsv` (2327 sor, szócikkenként), összesítés a nyitott tételben.

## 3. ⛔ Megállás: a tábla csoportszintje `ir`-en kívüli fájlt kíván (DT-F103a)

A brief 2. pontja a 2.29 csoport-szintű útvonalát kéri, de a csoport a táblába csak a `bdb_vers_jelentes.py` (új oszlop) vagy az `utvonal`
`/+n` bővítése útján kerülhet; az utóbbi a `lexikon_general.py` 2.29 ↔ 2.30 útvonal-illesztését töri. Mindkettő `ir`-en kívüli fájl, ezért
a hatókör 4. pontja szerint itt megállok; a SEMA 2.29 bővítése a döntés után (a választott alak szerint) készül. Opciók és javaslat: DT-F103a.

## 4. A döntés után: a 2.29 csoport-oszlopai (F103.7; DT-F103a (A), DT-F103b (a), orkesztrátori döntés, 2026-11-09)

*proveniencia: scope=adat/bdb_vers_jelentes.tsv (162 053 sor) | forras=bdb_vers_jelentes.py --ts 2026-11-09 + naplok/F103_oszlop_hash.py +
m2_minta_osszevet.py --mai-tabla (seed-102) | ts=2026-11-09*

| feltétel | eredmény |
|---|---|
| (1) csak két új oszlop, a régiek bájtra azonosak | `csoport`, `csoport_jel` a `szurt` után; a régi 15 oszlop SHA-256-ja a main-en (94c4c2ac), F103.4-ben és F103.7-ben azonos: `63373512b29fe3cb5b3a37494c9b411da240df7270c2999c7821b264e2347447` (teszt: `CsoportOszlop.test_regi_oszlopok_bajtra_azonosak`) |
| (2) `utvonal` változatlan, #102-mérés | `+` nincs az `utvonal`-ban (teszt); seed-102: könyv/vers 199, jelentéspont **183 / 200** (azonos) |
| (3) `lexikon_general.py` nem változik, E28 | a fájl nem változott; E28: a 10. pont szerint |
| (4) SEMA 2.29 | a két oszlop leírva |
| (5) `ir` | a brief `ir`-je: `eszkozok/olvaso_szerver/bdb_vers_jelentes.py` |

Újragenerálás: kilépési kód 0, mtime 19:14:24 → 19:20:31, `--ellenoriz` bájtra azonos (kód 0). Csoportos sor: 29 634 / 162 053 (with 7767,
especially 3936, absolute 2490, (a) 1846, figurative 1766, (b) 1708, (2) 1080, (1) 973 …).
