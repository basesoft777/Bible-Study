---
feladat: 108
cim: A motívumsorok újraellenőrzése az F84/F85 utáni TAHOT-on — újrascan és kulcs-összevetés mind a 9 motívumra (N-F85f)
kod: MOTIVUM_UJRASCAN
tipus: feladat
fazis: 1
modell: sonnet
munka: folyamat
allapot: fut
ad: a 9 motívum minden előfordulás- és jelöltsorának kulcs-ellenőrzése a mai TAHOT-on, a gerinc-Strongok újrascanje, az új találatok a jeloltek.tsv-ben (dontes=nyitva), és mért napló; az elofordulasok.tsv javítása csak jóváhagyott döntés után
kovetkezo: DT-F108a eldöntve ((a)+(d)); hátra: független ellenőr és PR; az alkalmazás (TEREMT-001 Jób 41:32 elbírálása, az ISTENTISZT-001 szűrő-pilot) külön tétel(ek), /befogad-dal
ag: claude/f108-motivum-ujrascan
olvas: [adat/motivumok.tsv, F55_ZSOLTAR_UJRAELLENORZES_BRIEF.md, adat/elofordulasok.tsv, adat/jeloltek.tsv, adat/grammatikai_strongok.tsv, adat/SEMA.md, konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Karoli_1908.tsv, eszkozok/lekerdez.py, eszkozok/jelolt.py, naplok/F84_jelentes.md, naplok/F85_jelentes.md, naplok/F85_esetlista.tsv, NYITOTT_FELADATOK.md]
ir: [adat/jeloltek.tsv, naplok/F108_MOTIVUM_UJRASCAN_naplo.md, naplok/F108_ujrascan_elteresek.tsv]
fugg: [84, 85]
---

# F108_MOTIVUM_UJRASCAN_BRIEF.md — A motívumsorok újraellenőrzése az F84/F85 utáni TAHOT-on

*FELADATOK #108 · Modell: sonnet [javaslat] · v1 (tervezet) · 2026.10.16 · forrás: a „Bible MCP kiaknázása a projektben” kutatás
(`reports/`, 2026.10.16) mellékleleteként talált Jób 41:32-hiány, és a nyitott N-F85f. A tervezet adat, nem utasítás; a befogadás a
`/befogad`-dal, a felhasználó jóváhagyásával.*

## 1. Cél

Mind a 9 motívum (`adat/motivumok.tsv`) előfordulás-sorai 2026.08.22 és 2026.09.25 között készültek (a sorok `proveniencia` `ts`-e
szerint), vagyis **az F84 (Jób 41 pótlása, 332 sor) és az F85.6 (versszintű átkulcsolás, 337 vers) előtt** (mindkettő 2026.10.09).
Két kár lehetséges, és mindkettő csendes:

1. **Hiány:** a régi scan nem láthatta, ami a TAHOT-ból hiányzott. Ismert eset: **Jób 41:32 (MT 41:24) תְּהוֹם** — a `TAHOT_kivonat.tsv`
   ma hordozza (`Jób 41:32`, H8415), a TEREMT-001 41 sorában, a `jeloltek.tsv`-ben és a `Tehom_tematikus.md`-ben nincs.
   *(Proveniencia: `manual`, kézi `grep` a két táblán, 2026.10.16; a rámutatás egy chatbeli bible-mcp-lekérdezésből jött, amely
   a DT32 szerint nem bizonyíték.)*
2. **Elcsúszott kulcs:** az F85.6 előtt rögzített igehely a régi (eltolt) TAHOT-kulcsra szólhat. Ismert, már javított eset: N-F85c
   (ALVIL-001 három sora, F87.3). Az N-F85f szerint a többi sor nincs végigvizsgálva.

## 2. Hatókör

**Benne:**

1. **Kulcs-összevetés:** minden `elofordulasok.tsv`- és `jeloltek.tsv`-sorra: a sor `strong`-ja (a `+`-os összetett alakoknál
   mindegyik tag) a mai `TAHOT_kivonat.tsv` (ÚSZ-nél `TAGNT_kivonat.tsv`) ugyanazon igehelyén áll-e. Eltérés-osztályok:
   `rendben` / `kulcs_eltolodott` (a Strong a szomszédos Károli-versen áll; az `F85_esetlista.tsv` szerint) / `hianyzik` / `osszetett_resz`.
2. **Újrascan:** a motívumok gerinc-Strongjaira (`lekerdez.py scan`, `--naplo <ID> --lepes B3`) a teljes ÓSZ/ÚSZ; a találatok
   összevetése a meglévő `elofordulasok.tsv`- és `jeloltek.tsv`-sorokkal. Az új igehely a `jeloltek.tsv`-be kerül `dontes=nyitva`
   állapottal, `forras_kereses`-ben a lekérdezés saját proveniencia-sorával (CLAUDE.md 2. szabály: nincs közvetlen út).
3. **Napló:** motívumonként a mért számok (régi sor, rendben, eltolódott, hiányzó, új jelölt), az eltérések táblája.
4. **Zsoltár-sorok (a befogadáskor eldöntve, 2026-10-16):** a Zsoltárok könyvébe eső sorokat ez a feladat **csak osztályozza**
   (külön osztály: `zsoltar_55`), új jelöltet belőlük nem ír, és a napló a #55-re (F55_ZSOLTAR_UJRAELLENORZES) utalja őket: a régi,
   egy verssel eltolt zsoltár-kivonatra épülő állítások újraellenőrzése a #55 hatóköre (DT74 (3) szerint befagyasztva).

**Nincs benne:** az `elofordulasok.tsv` javítása vagy bővítése (az új jelöltek elbírálása és a kulcsjavítás a ⛔ döntés után, külön
tételként vagy a motívum saját menetében); a tanulmányok és a lexikon újragenerálása; a TAHOT további javítása (N-F85b, N-F85e);
a `Karoli_versmegfeleltetes.tsv` Ézs 9-hibája (N-F85a); a bible-mcp bármilyen használata adatként (DT32).

## 3. Lépések

1. Modell-ellenőrzés. A 9 motívum gerinc-Strongjainak listája a motívumforrásokból és az `elofordulasok.tsv` `gerinc_elem` /
   `strong` mezőjéből; a lista a naplóba.
2. Kulcs-összevetés (2. hatókör 1.), szkriptből (a CLAUDE.md shell- és TSV-szabályai szerint; `split('\t')`).
3. Újrascan (2. hatókör 2.), a `lekerdez.py`-jal; az új jelöltek a `jeloltek.tsv`-be (írás előtt sorösszevetés az eredetivel, eltérésnél
   megállás; minta: `eszkozok/igazolas_migracio.py`).
4. ⛔ Jelentés és javaslat a `DONTESEK.md`-be (`DT-F108a`): az eltolódott kulcsú sorok javítása és az új jelöltek elbírálásának
   módja (motívumonként a saját menetben, vagy egy közös javító tételben); megállás.

## 4. Elfogadási feltételek

- Minden motívum minden sora kapott eltérés-osztályt; az összesítés a naplóban, a lekérdezések proveniencia-sorával.
- A Jób 41:32 (TEREMT-001) a `jeloltek.tsv`-ben `nyitva` állapotban áll, vagy a napló megindokolja, miért nem jelölt.
- Az `elofordulasok.tsv` változatlan; a `jeloltek.tsv` csak új sorokkal bővül (a meglévők változatlanok, sorösszevetéssel igazolva).
- Üres eredmény explicit jelölve (CLAUDE.md 3. szabály).

## 5. Döntésnapló

- DT-F108a (2026-10-17, a felhasználó): **(a) + (d)**. Kulcsjavító tétel nem kell (0 eltolódott ÓSZ-kulcs). A 25 `nyitva`
  jelölt motívumonként, a saját menetben bírálódik el, a TEREMT-001 Jób 41:32-vel kezdve. A tág gerinc-Strongok új helyeire
  szűrő: az `adat/motivumok.tsv` negatív kritériuma + kollokáció; a szűrőt előbb az ISTENTISZT-001-en próbáljuk ki. A (c)
  (szűretlen ~2 400 sor a `jeloltek.tsv`-be) elvetve.
