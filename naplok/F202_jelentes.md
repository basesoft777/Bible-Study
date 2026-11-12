# F202 — a BDB-lánc javítása (C1, C2, C4, C5): jelentés

*Brief: `F202_BDB_LANC_BRIEF.md` · ág: `claude/epic-spence-e4ece9` · 2026-11-11 · végrehajtó: `claude-opus-5-5` (a brief `modell` mezője:
`opus`, egyezik)*

Forrás: a generátor-hibaleltár (2026-11-11) C1, C2, C4, C5 sora. A mérő szkriptek a repón kívül futottak (scratchpad); a számok
a commitolt táblákból újra előállíthatók (`hu_illeszt.szocikkhatar_jelentesek`, `bdb_vers_jelentes.tsv` `okkod`, a próbalapok).

## 1. Commitok

| Tétel | Commit | Mit |
|---|---|---|
| F202.0 | `00ae46e9` | brief |
| F202.1 | `a986c4a7` | C1: a 2.32 szócikkfeje a címszónál kezdődik (általános szabály; a `SZOCIKKHATAR_KEZI` kiürítve) |
| F202.2 | `ba7c5841` | C1/C2: a 2.30 szócikkhatára a zárójel-töredéknél; a lánc újragenerálva (2.30, 2.31, 2.29, 2.32) |
| F202.3 | `c6c1895f` | C5 + N101: a nem létező fejezetre öröklődő hely TAHOT-igazolt feloldása (`orokles_tahot`) |
| F202.4 | `8da9febb` | C4 / N102: a H1004 könyvnév-hibás helyei a 2.31 kézi soraival (könyvvel) |
| F202.5 | `22e970ac` | a `teszt_bont` három előzetesen bukó (elavult) elvárása és az F202.4 kézi sorai |
| F202.6 | `7a85f13d` | C1: a szócikkfej horgonya előbb a teljes vezető héber szósor (a lap-hatás próbájából, H7585) |
| F202.7 | (a jelentés commitja) | jelentés, N-tételek, helyőrzők |

## 2. Előtte–utána

| Mérés | Előtte | Utána | Hol mérve |
|---|---|---|---|
| C1: a 2.32 szócikkhatáron át elnyelt sora (a 27. szabály mérése minden Strongra) | 316 sor / 191 Strong | **4 / 3** | `hu_illeszt.szocikkhatar_jelentesek` |
| C1: a kézi szócikkhatár-tétel (`SZOCIKKHATAR_KEZI`) | 3 | **0** (a szabály bájtra azonosan vágja) | `teszt_hu_illeszt.SzocikkhatarValos` |
| C1/C2: rossz szócikkhez rendelt zárójel-töredék (2.30) | 7 Strong | 0 a mintán | `teszt_bont.F202Szocikkhatar` |
| C5: `orokles_hibas` (2.29) | 88 | **11** (77 → `orokles_tahot`) | `adat/bdb_vers_jelentes.tsv` |
| N101: az Abdiás-vers fejezetszámmal (H6215) | 6 hely feloldatlan | 6 → Abd 1:18, 1:9, 1:19, 1:21 | ua. |
| N102: H1004 2Krón 10:20/26, 13:2, 14:8 | `nem_letezo_vers` 2, rossz könyv 2 | 1Kir 12:20, 12:26, 13:2, 14:8 (`forras_javitas`) | ua. |
| a 2.31 héber szórend, a hivatkozott-vers-próba mellékhatása | — | 3 sor `jelolt_marad` → `javitva` (H1121, H4832, H6215) | `adat/bdb_forras_javitas.tsv` |
| vak minták (könyv/vers; szűrés) | seed-100 198/200; bizonytalan egyezés s101 20/25, s102 21/25 | 199/200; 23/25, 24/25 | `m2_minta_osszevet.py --mai-tabla` (a base `00ae46e9` és a fej) |
| N113: nem szomszédos azonos útvonal szócikken belül | 350 eset / 161 Strong (a hibaleltárban 231) | 348 / 160 | a 2.30, (strong, bdb_id, utvonal) |
| N122: pe/mem `jelolt_marad` | 333 (a hibaleltárban 556; az F185 P4 után) | 333 | a 2.31 |

## 3. Tételenként

**C1 (N147, N100, K56) — javítva.** A horgonyos illesztés a jelölő nélküli szócikkfejnek (a sor `bdb_id`-je más, mint az előző soré)
eddig nem keresett kezdetet. Most a forrássor címszó-előtagja (homonimaszám, „[”, a vezető héber szósor, ennek híján az első szó) a
horgony, az előző és a következő illesztett pozíció között; több találatnál az első tagolásjel utáni, különben az utolsó; a következő fej
csak az előző fej horgonya után. A maradék 4 sor három külön ok (N-F202b). A gyökérok egyik fele a 2.30-ban volt: a bontó a rövid,
zárójelet záró töredéket („compare | Niph`al )”) a következő szócikk-kezdethez vonta; ez is javítva (F202.2).

**C2 — részben.** Javítva: a szócikkhatár a zárójel-töredéknél (F202.2; N103 (2) rokon osztálya). Az N99 2.30-as része már az F185 óta
helyes (H2403 13. sor `-/4/-` `bekezdes`, a 14–16. sor `-/4/a`–`-/4/c`); a generátor-kapu része a #182-é. Nyitva, indoklással:
N113 (a „1” újrakezdés két különböző oka: a BDB előzetes felsorolása, H0389, és a jelöletlen alcímszó, H0310 „Plural only construct …”;
a kettő eltérő útvonal-szabályt kíván, döntés kell), N103 maradék és N142 (seed-pontonkénti osztályok, új vak mérést kívánnak), N109 (a
szeletelő csoportszülői; a 2.29 jelentéspontját a tábla adja, a szeletelő csak tanú). Az N125, N126 Thayer-tétel: a `thayer_*` az F203-é.

**C4 — részben.** Javítva: N101 (általános szabállyal, F202.3), N102 (F202.4). Az N120 és az N121 helye a 2.31-ben már `javitva` (az F185 P4
tanús döntése: H0127 `׳מְּנֵי` → `׳פְּנֵי`, `׳עָפָד` → `׳עָפָר`); a lapon az újragenerálással jelenik meg. Az N122 rendszerszintű osztálya
nyitva marad (333 `jelolt_marad`; a gyakoriak valódi mem-alakok vagy rövidítés-töredékek, `׳הַמּ` 53, `מִמֶּנִּי` 5). Nyitva: N104 — a
`BDB.lexicon` és a `DictBDB.json` is H6920-nak (és H1106-nak) címkézi a Cóar szócikkét (BDB7165; a H6820 mindkét forrásból hiányzik);
a címszó–lemma összevetés 197 zajos jelöltet ad, ezért nem gépi javítás, hanem kulcstábla-döntés kell.

**C5 (N141) — javítva.** A seed-102 M039 (1Krón 15:15), M127 (1Sám 17), M196 (1Móz 30:14) feloldása most a vak kitöltéssel egyezik; az
M060 (H6920) az N104 miatt marad.

## 4. Gépi védelem

`teszt_hu_illeszt.Szocikkhatar` (7 szabályteszt) és `SzocikkhatarValos` (felső korlát 4 a commitolt táblán; a HAMART három sora);
`teszt_bont.F202Szocikkhatar`; `teszt_bdb_vers_jelentes` (`orokles_tahot` egység, H6666, H6215, H0343 negatív eset, H1004 könyvvel).
A `teszt_bdb_vers_jelentes.REGI_OSZLOPOK_SHA256` indoklással frissítve.

## 5. A lexikonlapokra gyakorolt hatás (nem generálva újra; próba a repón kívül)

A base (`00ae46e9`) és a fej adataival, ugyanazzal a generátorral (`general.py --cel lexikon --kimenet <ideiglenes>`):

- **HAMART-001: nem változik** (a kézi szócikkhatár-tételek bájtra azonosan állnak elő; a H2403 „51:4” feloldása a lapon nem jelenik meg).
- **ISTENTISZT-001: 3 blokk** (814., 820., 822. sor; H8034): a BDB9963 (arámi שֻׁם) feje saját magyar szöveget kap, a „szócikkhatáron át”
  jelölések eltűnnek. Javulás.
- **ALVIL-001: 4 blokk** (1035., 1039., 1080., 1135. sor; H7585): a BDB8375 feje saját szöveget kap, a kiemelések megmaradnak, a
  „szócikkhatáron át” jelölés eltűnik. **Figyelem:** az 1135. sor szótári összefoglalójából kiesik a „gyök (√): kétséges · rokon
  nyelvi adat” rész, mert a generátor (`lexikon_general.py`) az első szócikk fejéből veszi, és az most helyesen csak a rövid utaló
  szócikk (BDB8371). Ez a generátor hibája (N-F202e); az ALVIL újragenerálása előtt javítandó.
- a többi lap változatlan.

**Újragenerálás (F202.12, 2026-11-12; a HAMART-001 1. kiadása után, az orkesztrátor (c) útja szerint).** Az `origin/main`
beolvasztva (F202.10). A lapok a saját dátumukkal (`PARDES_DATUM`, az E28 szerint) próbagenerálva, a main generátorával is: a
HAMART-001 és a többi lap generált kimenete nem változik (a 2026-10-20-as régi lapok sodródása a main generátorával azonos, nem ezé az
ágé). Újragenerálva (`--ir`): ISTENTISZT-001 (3 blokk) és ALVIL-001 (3 blokk). Az N-F202e a generátorban javítva (a puszta utaló első
szócikk helyett a fő szócikk feje), így az ALVIL H7585 nyelvi háttere megmarad. `eszkozok/ellenorzes/futtat.py` a diff fájljain: 0 HIBA.

## 6. Tesztek

- `bdb_jelolt`: `teszt_bont.py` 79/79, `teszt_hu_illeszt.py` 29/29 zöld. `teszt_szakasz_bemenet.py`: 1 előzetes bukás (a base-en is; N-F202d).
- `teszt_futtat.py --gyors`: zöld, kivéve a `teszt_olvaso_szerver.py` (2) és a `teszt_pilot_aranymintaval.py` (2) bukását — mind a
  négy a base-en is bukik, azonos hibaüzenettel (előzetes, nem e csomagé).
- `ellenoriz.py`: 0 SÉRTÉS (a 27. szabály a base-en JELENTÉS (2), most RENDBEN). `--ellenoriz`: `bont.py --ts 2026-11-11`, `hu_illeszt.py --ts 2026-11-11`, `forras_javit.py` (a fejléc `--ts`-eivel), `bdb_vers_jelentes.py
  --ts 2026-11-10` bájtra azonos.

## 7. Nyitott tételek és döntés (helyőrzővel)

`nyitott/uj/epic-spence-e4ece9.md`: N-F202a (a 2.29 nem különíti el a homonimaszám nélküli második szócikket; mért hatás 1 069 sor),
N-F202b (a C1 maradék 4 sora), N-F202c (a forrás könyvnév-hibája ismétlődő osztály, gépi felismerés nélkül), N-F202d (a
`teszt_szakasz_bemenet` előzetes hibái), N-F202e (a generátor szótári összefoglalója az első szócikk fejéből). `dontesek/uj/epic-spence-e4ece9.md`:
DT-F202a (a H5973 2.29-címkéje, 🟡). Lezárva a `NYITOTT_FELADATOK.md`-ben: N100, N101, N102, N120, N121, N141, N147; kiegészítve: N99, N104,
N113, N122.
