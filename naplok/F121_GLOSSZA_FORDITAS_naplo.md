# F121 napló — F121.0 (a „nevezni” tétel), TBESG G1941 `1`

*2026-10-27 · proveniencia: manual (felhasználói döntés: DT379, 2026-10-27) · végrehajtó: claude-sonnet-5-5*

**Hatókör.** Csak a `TBESG G1941 G1941 1 forditas_hu` sor. A Thayer G1941 `teljes` sor és a terminológia-sorok az F121.0 hátralévő része, nem érintettek.

**Eltérés a brief szövegétől.** A brief 2b szakasza „más néven is nevezni” alakot írt; a DT379 szerint a helyette: „nevet adni; ragadványnevet adni, ha a mellékes név a lényeg”. A „nevezni”/„elnevezni” rendben van. A döntés az irányadó.

**Diff (szöveges).**
- előtte: `hívni, nevezni, melléknevet adni: tárgyesettel (klasszikus), …`
- utána: `hívni, nevezni, nevet adni: tárgyesettel (klasszikus), …`
- `allapot=kezi`, `modell` üres, `datum` és `forras_hash` (`794c6af8…`) változatlan; a `megjegyzes` az F121.0-jelölést kapja.

**Ellenőrzés.** Írás előtt a tábla soronkénti összevetése: pontosan 1 sor tért el. `eszkozok/ellenoriz.py`: SÉRTÉS 0. Mérés: a TBESG-sorok `forditas_hu` mezőjében „melléknevet adni”/„melléknéven nevez” előfordulás: 0. `eszkozok/teszt_forditas_kapuk.py`: 90 teszt OK; a `test_meglevo_forditasok` engedélye `{Thayer G1941}`-re szűkítve.

## 2. F121.1 — mérés az ISTENTISZT-001 lapon (2026-10-28)

*proveniencia: scope=`lexikon/ISTENTISZT-001_TUDOMANYOS.md` (main, f3f9372b) és a repón kívüli `general.py --cel lexikon --id ISTENTISZT-001` render a `lexikon_general.forditas_ehhez` hívásainak naplózásával | forras=`eszkozok/glossza_lexikon_forditas.py lista` | ts=2026-10-28*

**Mit számol melyik szám.**

| Szám | Mit számol | Érték |
|---|---|---|
| `grep -c 'fordításra vár'` | sorok | 23 |
| `grep -o '(fordításra vár)' \| wc -l` (PR #497 leírása) | előfordulások | 46 |
| ebből a DBH-definíciók cellái (előfordulás, az UBS-jelentés oszlop 22 sora) | | 44 |
| ebből a 56.15 doménnév (UBS-doménsor) | | 1 |
| ebből a lap magyarázó lábjegyzete (136. sor), nem jelölt egység | | 1 |
| **egyedi egység** (kulcs: szotar+strong+entry_id+jelentes_szam+mezo) | | **6** |

A 46 tehát nem 46 fordítandó szöveg: ugyanaz az 5 DBH-definíció ismétlődik a 22 ÓSZ-sorban (H7121 három lexid, H8034 két lexid).

**A 6 egység** (`naplok/F121_GLOSSZA_FORDITAS_lista.tsv`, forrás-hash-sel):

| szotar | strong | entry_id | jelentes_szam | mezo |
|---|---|---|---|---|
| UBS_DBH | H7121 | 006562001001000 | — | definicio_hu |
| UBS_DBH | H7121 | 006562001009000 | — | definicio_hu |
| UBS_DBH | H7121 | 006562001011000 | — | definicio_hu |
| UBS_DBH | H8034 | 007442001001000 | — | definicio_hu |
| UBS_DBH | H8034 | 007442001004000 | — | definicio_hu |
| UBS_DNTG | G1941 | 001957001003000 | 56.15 | glosszak_hu |

A lista-eszköz további 6 hívást is lát, amelyeknek nincs forrásszövege a táblában (SECE_G ×3, SECE_H ×2, TBESH H8034 `teljes`): ezek a lapon nem viselnek jelölést, nem hiányok (`allapot=nincs_forras`).

**Miért tért el a 454-től.** A #131 (DT371) a tW-t, a TBESH-t, a Mounce-ot és a teljes UBS-szócikkeket levette a lapról (mutatóra cserélte); a 62 egységből (48 DBH, 2 DNTG, 1 TBESH, 1 Mounce, 10 tW) csak a most látható UBS-jelentés-oszlop és a doménsor maradt.

**Eszköz és 13. szabály.** Új: `eszkozok/glossza_lexikon_forditas.py` (`lista`, `dbh_forras_idx` = a UBS_DBH forrásszöveg-feloldó; DT-F121c). Az `ellenoriz.py` 13. szabálya ezt a feloldót importálja (egy feloldó, nem két másolat): `UBS_DBH` + lexid + `—` + `definicio_hu`/`glosszak_hu` → `UBS_DBH_jelentesek.tsv` `definicio_rovid`/`glosszak` (strongonként az első sor). Teszt: `teszt_ellenoriz_13.py` `Szabaly13DBH` (helyes hash, elrontott hash, ismeretlen lexid). `ellenoriz.py`: SÉRTÉS 0.

## 3. ⛔ Megállás — jóváhagyásra váró pontok (2026-10-28)

A 6 sor még nincs a `forditasok.tsv`-ben. Két dolog előzi meg az írást; a javaslat mindkettőre mellette áll.

**D1 (DT234) — licenc.** A 6 sor CC BY-SA 4.0 forrás (UBS DBH, UBS DNTG) fordítása. *Javaslat: 1. opció.* A `forditasok.tsv` sorainak licence a `szotar` forrásáé (CC BY-SA 4.0), a `projekt_adat` „minden jog fenntartva” erre nem terjed ki. Ez séma-változás nélkül megy, és a 40 meglévő `UBS_DNTG` `kezi` sor már így áll (a `licencek.tsv` UBS_DBH/UBS_DNTG sora ezt tartalmazza). Új `licencek.tsv` sor nem kell.

**Terminológia v4 (DT238–242 szerint; a szójegyzék csak jóváhagyott sorral bővül).** A 6 egység angol kulcskifejezései, amelyek új `terminologia.tsv` sort kívánnak (a Károli-alak a lap 1Móz 4:26 stb. soraiból, az adatblokk-lekérdezés nélkül nem idézve):

| angol | magyar (javaslat) | indok | kapu |
|---|---|---|---|
| call on (someone's) name | valakinek a nevét segítségül hívni | Károli „segítségül hív” (a lap sorai); a BDB H7121 2.c „hívni ׳י nevével (azaz használni azt a segítségül hívásban)” | igen (a végleges sor: **nem**, l. 4.) |
| cry out (someone's) name | valakinek a nevét kiáltani | a lap Károli-sorai (2Móz 33:19 „kiáltom előtted az Úr nevét”) | igen |
| deity | istenség | nyelvközi egység (DT238): a Thayer/BDB-fordításban is „istenség” | igen |
| core of one's identity | azonosságának magja | a lap „2. Szótári háttér” H8034 BDB-szakasza „azonosság” szóhasználatot nem ad; új sor | nem (szabad szövegű kifejezés) |

A „call” szó önmagában többjelentésű, ezért erre nincs kapus sor; a nevezni-család (DT379: „nevet adni”) ebben a 6 egységben csak az 009000 jelentésben fordul elő („nevet adnak egy személynek vagy helynek”).

**A 6 fordítás tervezete** (nem rögzítve; jóváhagyás után kapuk, önújrapróba, `rogzit`, `allapot=sonnet`, `modell=claude-sonnet-5-5`, `terminologia_verzio=v4`):

1. 006562001001000: „= olyan cselekvés, amellyel emberek vagy istenségek hangosan beszélnek, gyakran azért, hogy magukra vagy helyzetükre felhívják a figyelmet, és azt várják, hogy valaki így vagy úgy válaszoljon”
2. 006562001009000: „szó szerint: valakinek (valaminek) a nevét kiáltani; innen: = olyan cselekvés, amellyel emberek nevet adnak egy személynek vagy helynek”
3. 006562001011000: „szó szerint: valakinek a nevét segítségül hívni; innen: = olyan cselekvés, amellyel emberek elismernek egy istenséget, és kész(ek) ennek az istenségnek néhány követelménye szerint élni”
4. 007442001001000: „= egy vagy több szó, amellyel egy személyt, istenséget, helyet vagy tárgyat ismernek, megszólítanak, emlegetnek vagy amellyel rá utalnak; ≈ az ember azonossága alapvető elemének tekintik”
5. 007442001004000: „szó szerint: név; innen: = az azonosság magja, amely a lény lényegét tükrözi”
6. UBS DNTG G1941 56.15 (`glosszak_hu`): „ügyében fellebbezni; magasabb bírósághoz fellebbezni”

**Mit nem csináltam.** `terminologia.tsv`, `licencek.tsv`, `forditasok.tsv`: változatlan. Az F121.0 hátralévő része (Thayer G1941 `teljes` sor, a tiltott-fordulat tábla) a #131/#142 óta más úton van (DT379), nem e szűkített menet tárgya.

## 4. F121.2 — rögzítés és repón kívüli próbarender (2026-10-28)

*A jóváhagyás: DT234 (D1 1. opció) és DT-F121d (v4 első 4 sor + két nyelvi javítás), felhasználó, 2026-10-28, „Igen, jóváhagyom” (`DONTESEK.md`).*

- `adat/terminologia.tsv`: +4 `v4` sor (`deity` kapu=igen; a többi kapu=nem).
- `adat/forditasok.tsv`: +6 sor (`UBS_DBH` ×5 `definicio_hu`, `UBS_DNTG` G1941 56.15 `glosszak_hu`), `allapot=sonnet`, `modell=claude-sonnet-5-5`, `terminologia_verzio=v4`, `forras_hash` a `lista`-ból. Írás előtt-után bájt-összevetés: a meglévő 14 672 sor bájtra azonos, csak 6 sor került a végére.
- **Kapuk** (`forditas_kapuk.kapuk_futtat`, mind a 6 sorra): minden gátló kapu RENDBEN (`5_terminologia`, `15_tiltott` (a brief 14_tiltott néven említi; a kód 15_tiltott) is); bukott sor 0, önújrapróba nem kellett, `…_bukottak.tsv` nem jött létre.
- `ellenoriz.py`: SÉRTÉS 0, a 13. szabály RENDBEN a 6 új sorra is (a 14. szabály JELENTÉS, nem gátol).
- **Próbarender** (repón kívül): a `(fordításra vár)` jelölés a 46-ból 1-re csökkent; a megmaradt egy a lap magyarázó lábjegyzete (136. sor), amely a jelölést mint fogalmat említi — nem fordítatlan egység. A UBS-doménsor: „56.15 ügyében fellebbezni; magasabb bírósághoz fellebbezni”.
- **Ismert eltérés, nem e menet hibája:** a próbarender és az élő lap között 8 további sor különbözik, mert a generátor-kód még a `DT381`/`DT373`/`DT382` helyett a helyőrzőket (`DT-F131k`/`DT-F131c`/`DT-F131l`) tartalmazza. Az élő lapot ez a menet nem írta; a szám-névcserét a main-en a `szamkiosztas` végzi, az élő lap nulladiffje addig ezen is múlik.
- **Más lapok:** az új `UBS_DBH` H7121/H8034 sorok a többi lapot is érinthetik, ha azokon ugyanez a lexid szerepel; az élő lapok újragenerálása nem történt meg, a hatás a #36-é.

**⛔ Olvasás:** a próbarender: `F121_proba_ISTENTISZT-001_TUDOMANYOS.md` a közös jegyzetmappában. Az élő `lexikon/ISTENTISZT-001_TUDOMANYOS.md` felülírása a felhasználó döntésére vár.

## 5. F121.3 — a #131 helyőrzőinek cseréje az `eszkozok/` alatt (2026-10-28)

*Felhasználó, 2026-10-28 (az orkesztrátor chatjében, szó szerint idézve): „Mehet: a próbalapot elfogadom. Előbb a generátorban (és a teszt/forrás-kommentekben) a DT-F131k/c/l helyőrzőket cseréld a végleges DT381/DT373/DT382-re (az ir bővítésével, mechanikus), utána az élő lap felülírása, nulladiff, CI, független ellenőr és draft PR.”*

A megfeleltetés a `szamkiosztas: … ` commit (f3f9372b) üzenetéből és a `DONTESEK.md` sorokból: a→371, b→372, c→373, d→374, e→375, **h→376, f→377**, g→378, i→379, j→380, k→381, l→382, m→383, n→384, o→385; DT-F141a→370 (a h/f sorrend nem betűrendes). Csere: csak az `eszkozok/` fájljaiban, szóhatáros regexszel. Cserélt helyőrzők (előfordulás): DT-F131a ×8, b ×3, c ×4, d ×4, i ×3, j ×4, k ×11, l ×11, m ×4, n ×1, DT-F141a ×2 — 13 fájlban (a lista a brief `ir` mezőjében). A `naplok/`, brief és más dokumentumokban maradt helyőrzők nem e menet hatóköre.

Tesztek: `teszt_forditas_kapuk` 110 OK, `teszt_szerepmatrix` 44 OK, `teszt_szotari_gerinc` 39 OK. Két teszt a csere előtt is bukik ezen az ágon (a cserétől független, a stash-sel mérve): `bdb_jelolt/teszt_bont.py` 4 hiba, `olvaso_szerver/teszt_bdb_vers_jelentes.py` `test_bajtra_azonos` — a bemeneti fájlok hash-e tér el (Windows-checkout sorvége), nem a `forditasok.tsv`.
