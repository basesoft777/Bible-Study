# F224 — A cikkírás új menete: jelentés

*Végrehajtó: claude-opus-5-5 (a kért `opus`, egyezik). Ág: `claude/f224-cikkiras-uj-menet`, alap: main `56da26c0`. A brief: `F224_CIKKIRAS_UJ_MENET_BRIEF.md`.*

## Ütközésvizsgálat (a fájlírás előtt, 2026-11-15)

`python eszkozok/feladatok.py fuggesek` és a nyitott PR-ok fájllistája (`gh api …/pulls/<n>/files`, lapozva):
- **#729 (F218a)** a brief `ir` mezőjéből két fájlt ír: `adat/SEMA.md` és `sablonok/9_PaRDeS_motivum_forras_sablon.md`. Ezekhez ez az ág nem nyúl a #729 merge-éig (a brief `fugg: [218]`): az F224.6 (érvnapló) és az F224.5, F224.11 SEMA-szakasza vár.
- **#725 (F217.1)** egyik fájlunkat sem írja.
- A Károli-csomagok PR-ja (#737) mergelve.

## Menet tételenként

### F224.1 — Az állítás-ellenőr szerepfájlja
Új `.claude/agents/allitas-ellenor.md` (`model: sonnet`, 0. lépés: modell-ellenőrzés; íróeszköz nincs). A hét kötelező kérdés a mérés példáival (ISTENTISZT K50 = a lektor 1. tétele, Zsolt 116 = 2., „hét helyből öt” = 10. (K25), Jézus Krisztus neve = 3.; HAMART erec/adámá, K39, K47); a 7. kérdés példája a lektor 6. tétele. A példák szövege a `2ae45dae:naplok/KIADAS_ISTENTISZT-001_lektor.md` és a mérés F2-mellékletei szerint. Ítélet az állítmányra, „nem” válasznál nem lehet „igazolt”; bizonyítéktípus; kétirányú tilalom; kimenet: a hívó menti a `naplok/ALLITAS_<ID>_itelet.md`-be. A menetbeli hely: `MUNKAMENET.md` C) F2 sor (F224.8).
*(proveniencia: scope=TERV_CIKKIRAS_v3 3. szakasz; MERES_VISSZAJATSZAS_2026-11-15 4–5. szakasz; 2ae45dae lektori lista | forras=manual | ts=2026-11-15)*

### F224.2 — A bíráló szerepfájlja
Új `.claude/agents/biralo.md` (`model: sonnet`). Bemenet: az érvvázlat vitatott pontjai, a bizonyítéklap, a blokkok vizsgálandó állításként, a lap Kivonat-/Remez-/Sod-/Módszertan-mondatai. Hét kérdés súllyal (egyensúly, valódi erő a 12:3-as példával, hiányzó érv a „-ért” példájával, szintkeverés, a lap két helyének ellentmondása, szakirodalmi hatókör, szerkezet jelölése); legfeljebb 10 lekérdezés vitatott pontonként, naplózva; „lekérdezendő”; határról nem ítél; elutasított tételek a lektorhoz és a felhasználóhoz.
*(proveniencia: scope=TERV_CIKKIRAS_v3 4. szakasz; BIRALO_821_sonnet.md (a mérés) | forras=manual | ts=2026-11-15)*

### F224.3 — A lektor szűkítése
`.claude/agents/lektor.md`: a bemenet egy eredetjelölés nélküli tétellista; ötödik kérdés: „a próza az érvnapló szerint íródott-e”; a négy érvelési kérdés a bírálóé (az 1. változat 32/c pontja a repóba sosem került be, ezért itt „nem a te kérdésed” mondat áll); minden ellenőrzendő tételre sor („rendben” is), hogy a hívó a vak mintát mérhesse. `model: fable` változatlan. `.claude/commands/kiadas.md` 3. lépés: a lektor bemenete (jelölt helyek, az F2 „vitatott”/„nem eldönthető” tételei, a bíráló elutasított tételei, vak minta az F2 „igazolt” tételeiből 10%, legalább 5), a felfüggesztés hibás mintánál, a három hatókör-szűkítés (a)/(b) mondata, hivatkozással a `BRIEF_SABLON.md` DT-F221a szabályára.

### F224.4 — A kinyerés bővítése
`eszkozok/proza_allitas.py`: három új K-fajta a rés mondatain (`UJ_FAJTAK`): **szám-kapcsolat** (a kapcsolat-tábla sorai bizonyosság szerint; „N helyből M”: a bekezdés felsorolt igehelyei), **belső utalás** (a célpont a forrás vagy a generált lap címsorai, félkövér bekezdés-címei között), **nem dönti el** (a pont igehelyei a bekezdésből, a pont címéből is; a lap más mondatai ugyanezekre a helyekre, legfeljebb 8). Gépi ELTÉR-ítélet az új fajtából soha nem lesz: ahol a gép dönt, a bizonyíték `JELENTÉS (ELTÉR-jellegű, F224.4)` kezdetű, ⚑-gel, és a `--kapu` motívumonként külön `JELENTÉS` sort ír. A régi K-tételek számozása nem változik (a régi fajták egységei kapják előbb a számot). A HIBA-szintre emelés javaslata: N-F224a (`nyitott/uj/f224-cikkiras-uj-menet.md`).

**Mérés** (a K-tétel-szám a futtatás előtt és után; `scratchpad/f224/klista.py`, a forrás, az `elofordulasok.tsv`, a `kapcsolatok.tsv` és a lap a megnevezett commitról):

| Forrás | K előtte | K utána | Új K-tétel |
|---|---|---|---|
| ISTENTISZT-001, `b2aea73f` | 54 | 58 | K55 (89. sor, Remez: „három kapcsolat erős” — **a lektor 4. tétele**; ELTÉR-jellegű: 3 ↔ 13 magas sor), K56 (99., 2Móz 33:19/34:5 „nem dönti el”), K57 (101., 1Móz 4:26 „nem dönti el” — **a lektor 9. tétele**), K58 (103., Róm 10:13 „nem dönti el”) |
| HAMART-001, `f6da955e` | 114 | 118 | K115 (15., Kivonat), K116 (101.), K117 (105.), K118 (152., Módszertan) |
| ISTENTISZT-001, main | 62 | 64 | 2 |
| HAMART-001, main | 123 | 128 | 5 |

- A régi K-tételek: a számuk és a helyük mind a négy forráson változatlan; új bizonyítéksort (és ezzel ⚑-et) kapott: ISTENTISZT `b2aea73f` K25 („hét helyéből ötben” — a lektor 10. tétele; a bekezdés öt felsorolt igehelye) és K42 (Módszertan, „22 helyből 20”); HAMART `f6da955e` K54; a main forrásain ISTENTISZT K26, K48, K50, K52, HAMART K47, K60.
- A lektor 11. tétele („jelentés a névből”) értelmezés, nem lett K-tétel (a brief szerint nem elvárt).
- A `--kapu` kimenete a main forrásain bájtra azonos a változtatás előttivel (`diff` üres; ELTÉR 0, egyezik és kézi-számláló változatlan, a kézi-számláló csak a régi fajtákat számolja), kilépőkód 0.
- A 113 helyett 114 K-tétel a `f6da955e`-n: a mérés (2026-11-15) óta az eszköz változott; a régi K-számok a mai eszközzel és a mai eszköz után egyeznek, a 113-as szám a mérés napjáé.
- Teszt: `eszkozok/teszt_proza_allitas.py` 51 teszt OK (11 új, `F224_4` osztály: mindhárom fajtára pozitív és negatív eset, a stabil számozás és a kapu JELENTÉS-sora).
*(proveniencia: scope=motivumok/ISTENTISZT-001.md @b2aea73f, motivumok/HAMART-001.md @f6da955e, a main két forrása | forras=eszkozok/proza_allitas.py (az ág feje) | ts=2026-11-15)*

### F224.12 — A határ-ellenőr modellje
`.claude/agents/hatar-ellenor.md`: `model: sonnet`, a 0. lépés modellneve `sonnet`; a bemenet a határesetek negatív próbáival bővült, a negatív kritérium szűkebb és tágabb változatával. `grep -i fable .claude/agents/hatar-ellenor.md`: 0 találat. A `MUNKAMENET.md` C-h sorának modellneve az F224.8-ban.
