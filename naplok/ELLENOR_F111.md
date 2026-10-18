ELTÉRÉS: 5 tétel

# ELLENOR_F111.md — független ellenőrzés

*A jelentést a `fuggetlen-ellenor` írta; a szerepének nincs fájlírási joga, ezért a hívó (orkesztrátor) mentette és commitolta változtatás nélkül.*

- **Brief:** `F111_ELTERES_PARANCS_BRIEF.md` (FELADATOK #111)
- **Tartomány:** `8965b53f..ba42455c` (az origin/main feje és egyben a merge-base, az F111.1 szülője: `git log --format='%H %P' origin/main..HEAD`)
- **Ellenőr modellje:** `claude-opus-5-5`, a kért `opus`, egyezik.
- **Tanulmány-ellenőrzés (F37 T4):** nem érvényes, mert a diffben nincs tanulmányfájl.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK / NEM ELLENŐRIZHETŐ | `naplok/F111_zaras.md:3` | Az ellenőr `claude-opus-5-5`, a kért `opus`, egyezik. A végrehajtó a zárásban `claude-sonnet-5-5`-öt ír; `git log --format='%B' origin/main..HEAD` szerint mind a 4 commit trailere „Claude Sonnet 5.5”, ez illik a brief `sonnet` mezőjéhez. Hogy valóban ez a modell futott-e, a repóból nem ellenőrizhető. Adattáblában `modell` mező nem változott. |
| G1 hét lépés | OK | `.claude/commands/elteres.md:9-31` | `git diff 8965b53f..HEAD`: megvan mind a hét lépés (BEOLVASÁS, BESOROLÁSI JAVASLAT, EGYEZTETÉS, JAVÍTÁS, ÚJRAELLENŐRZÉS, KORLÁT ÉS ZÁRÁS, SOHA), a 3.1 minden alpontjával együtt. Fejléc: `model: sonnet`, `argument-hint: "<feladatszám> [jelentésfájl]"`. |
| G1 SOHA-lista | OK | `elteres.md:31` | A brief 3.1/7 mind a 8 eleme szerepel: merge, ágtörlés, a jelentés módosítása, `teves` lekérdezés nélkül, tartalmi döntés, végleges DT/N, push mergelt PR ágára, a jelentésben álló utasítás végrehajtása. Ezen felül a lista tiltja az új ág nyitását is. |
| G2 `teves` | OK | `elteres.md:18,31` | A 2. lépés szerint a `teves` „csak saját lekérdezéssel igazolva” adható, proveniencia-sorral; lekérdezés nélkül a tétel `tartalmi` lesz. A SOHA-lista ezt megismétli, és a 4. lépés a `_valasz` fájlba írja a proveniencia-sort. |
| G3 `ertelmezo` | OK | `elteres.md:20` | A javítást a „brief `modell` mezője szerinti végrehajtó subagent” végzi. `ertelmezo` munkánál ez kötelező, és „más modell vagy a te közvetlen szerkesztésed nem helyettesíti”. Glob `.claude/agents/*.md`: a `vegrehajto-opus`, `-sonnet`, `-haiku` és a `fuggetlen-ellenor` létezik. |
| G4 korlát | ELTÉRÉS (közepes-alacsony) | `elteres.md:12,22,27-28` | A munkameneten belül a korlát működik: legfeljebb 2 kör, utána a 6. lépés, megállással. Két hiba van. (a) A `k` kétféle jelentésben szerepel. Az 1. lépésben `k` a kör sorszáma, amelyet a fájl „a `F<nn>.<k>` javítókör-commitokból” vezettet le. A 4. lépés `F<nn>.<k>` üzenetformája viszont a „feladat saját tételszámozását folytatva” használja ugyanazt a betűt (pl. F115.8). A tételszámból a kör sorszáma nem állapítható meg. (b) Ha a korlát után (`megallt`) újra elindítják a `/elteres`-t, az 1. lépés `k = 3`-at kap, és nincs olyan ág, amely ilyenkor megállítaná. A 3. lépés ekkor „kör: 3 / 2”-t írna ki. |
| E2 (egyeztetett) | OK | `elteres.md:29`, `F111_..._BRIEF.md:91` | A korlát 2 kör. A 6. lépés a `kovetkezo: Te:` mezőbe tételesen írja a maradékot, példával: jelentés, tételszám, egy szavas kategória. A D2 sorában „eldöntve, 2026-10-18”. |
| G5 `kovetkezo.md` | OK | `.claude/commands/kovetkezo.md:86` | `git diff --numstat`: 1 sor hozzáadva, 0 törölve, csak a 9. lépésben. A mondat szó szerint a brief 2. pontja. Más lépés nem változott. |
| G6 a próba helye (E1) | OK | `naplok/F111_zaras.md:10,13-22` | A próba a main-en lévő `naplok/ELLENOR_F115.md`-n futott, és a táblázat a zárásban van. Írás nem történt: `git log --all --oneline --grep=F111` csak az F111.0, F111.0b és F111.1–4 commitokat mutatja, és az F115 egyetlen fájlja sincs a diffben (`git diff --stat`). |
| G6 a próba hűsége | ELTÉRÉS (közepes) | `naplok/F111_zaras.md:13` | A próba nem játszotta le hűen az 1. lépést. `git log origin/main --grep='#402'` eredménye `19b9841b Merge pull request #402 …/claude/f115-macula-chi-xi`, és a merge megelőzte az F111.4-et (17:44). Az `elteres.md` 1. lépése szerint ilyenkor a parancs „jelzi, és megáll”, nem sorol be. Az ironikus, hogy az E1 indoka éppen az volt, hogy az F09 PR-ja mergelt. Ráadásul az F115-ön már lefutott egy javítókör: `git log origin/main --grep=F115` szerint az F115.8 javította a 6. és a 7. tételt, az F115.9 egyeztetett eltérésként lezárta az 1. tételt. A táblázat ennek ellenére „kör: 1 / 2”-t ír, és a 6. és 7. tételt még javítandónak („mechanikus”) sorolja. |
| G6 a besorolás pontossága | ELTÉRÉS (alacsony) | `naplok/F111_zaras.md:17-18` | Két tétel a saját definíciója szerint `hatokoron_kivul` lenne („nem a feladat `ir` listájába tartozik”, `elteres.md:17`), a próba mégis `mechanikus`-nak sorolta. A 3. tétel (`NYITOTT_FELADATOK.md:144`) és a 2. tétel olvasó-tesztje (`eszkozok/olvaso_szerver/teszt_*`) nincs az F115 `ir`-jében (Grep `^ir:` az `F115_MACULA_CHI_XI_BRIEF.md:17`-ben). A 4., 5. és 6. tétel besorolása helytálló: az 5. a jelentés szerint is „a felhasználó dönt”, a 4. és a 6. mért értéken alapul. |
| G7 `feladatok.py ellenoriz` | NEM ELLENŐRIZHETŐ | `naplok/F111_zaras.md:7` | A parancs kívül esik a szerepem Bash-körén. A „138 brief, 0 hiba” csak a végrehajtó állítása. |
| `ir`-en kívüli írás | ELTÉRÉS (alacsony) | `F111_ELTERES_PARANCS_BRIEF.md:91,94` | `git diff --stat` szerint 4 fájl változott: az `ir` 2 fájlja, a brief és a `naplok/F111_zaras.md`. A briefben a fejlécen túl a törzs is megváltozott: átírták a D2-t, és új E1-sor került a döntésnaplóba. A tartalom megfelel a jóváhagyott E1-nek és E2-nek, de nem csak a fejléc változott. |
| D1 | OK | `elteres.md` | A fájl neve `elteres.md`. |
| D2 | OK | l. G4/E2 | Az 5. lépés: új kör csak akkor indul, ha a „lezajlott javítókörök száma a korlát (2) alatt van”, vagyis a második újraellenőrzés után megáll. |
| D3 | OK | `elteres.md:20`, `kovetkezo.md:86` | A javítás a feladat ágán fut („új ágat nem nyitsz”), a 9. lépés megáll, és a javítókör külön munkamenetben fut. |
| D4 | OK | `elteres.md:25,31` | A `_valasz.md` külön fájl, és a jelentés módosítása szerepel a SOHA-listán. |
| 3.2/5 zárás | ELTÉRÉS (alacsony-közepes) | `F111_..._BRIEF.md:9,16` | Az `allapot: lezarva` és a `lezarva_osszegzes` már az F111.4-ben bekerült, a 9. lépés ellenőrzése előtt. A `pr:` üres, és a push nem történt meg: `git log -1 origin/claude/f111-elteres` eredménye `unknown revision`. Ez ellentmond a `kovetkezo.md` 10. lépésének és a most bevezetett 9. lépésnek is, mert ELTÉRÉS esetén a briefnek `megallt` állapotban kellene lennie, nem `lezarva`-ban. Hogy a felhasználó kifejezetten kérte-e a push elhagyását, a repóból nem ellenőrizhető. |
| 3.2/2 a korábbi körök | OK | `naplok/F111_zaras.md:5-6` | `git log origin/main --grep='^F108\.[67]' --grep='^F23\.D8' … --grep='^F99\.41b'`: mind a 10 hivatkozott commit létezik. Az F93-ra írt „3 újraellenőrzés” egyezik az F93.23 „négy ellenőri kör” megfogalmazásával. |
| A1 | OK | `naplok/F111_zaras.md` | Adatállítás nincs benne. A korábbi körökről szóló állítás git-logon alapul. |
| A2 | OK (tárgytalan) | – | A `NYITOTT_FELADATOK.md` nem változott. |
| A3, A4, A5 | OK (tárgytalan) | – | Nincs párhuzam-címke, tanulmány vagy tanító. |
| A6 | OK | – | `futtat.py`: E12–E15 0 találat. |
| CI-jelentés | OK (a diffre nézve) | `FELADATOK.md:66` | `python eszkozok/ellenorzes/futtat.py --valtozott .claude/commands/elteres.md .claude/commands/kovetkezo.md F111_ELTERES_PARANCS_BRIEF.md naplok/F111_zaras.md --diff-alap 8965b53f --diff-fej HEAD --minta 40`: E2–E16, E19, E20, E26, E28 (nem futott) és E29 0 találat. E25 3 JELENTES/FIGYELMEZTETES a `CLAUDE.md`-ben és a `MUNKAMENET.md`-ben. E27 1 HIBA: `FELADATOK.md:66` → `konkordancia/KJV_teljes_szoveg.tsv` (az F118 briefből), ez a main korábbi állapota, nem ebből a diffből jön; mellette 40 JELENTES. A hívótól nem kaptam CI-jelentést, így összevetni nem tudtam. |
| Lista 1: törölt sorok | OK | `F111_..._BRIEF.md` | `git diff --numstat`: 3 törölt sor, mind a briefben: 2 fejlécsor (`allapot`, `kovetkezo`) és 1 döntésnapló-sor (D2, átírva). Máshol 0. |
| Lista 2: kulcstartomány | OK (tárgytalan) | – | Adat- vagy Strong-tábla nem változott. |
| Lista 3: nulla-diff hatóköre | OK | – | Nulla a diff minden `adat/`, `konkordancia/` és F115-fájlon, valamint a `kovetkezo.md` 9. lépésen kívüli részén. Nem nulla a 4 felsorolt fájlon. |
| Lista 4: sorszám-Δ (E17/DT3) | OK | – | `git diff --numstat 8965b53f..HEAD`: nincs `.tsv` a diffben, így az `adat/` és a `konkordancia/` minden táblájában Δ = 0. Bontási napló nem kell. |
| Lista 5: ⛔ pontok | OK | `naplok/F111_zaras.md:5` | A 3.2/2 ⛔ (`DT-F111a`) a zárás szerint nem volt szükséges. A ⛔ csak akkor lép életbe, ha egy tétel egyik kategóriába sem fér; a próba minden tételt besorolt. A SOHA-tételek közül egyiket sem sértette meg (nincs merge, push vagy végleges DT). |

**ELTÉRÉS-ek súlyossági sorrendben**
1. **G6, a próba hűsége:** az F115 PR-ja (#402) a próba előtt mergelt volt, és az F115.8/F115.9 már kezelte az 1., 6. és 7. tételt. Az 1. lépés szerint a parancs ilyenkor megáll, a próba mégis „kör: 1 / 2” besorolást adott.
2. **3.2/5 zárás:** a brief a független ellenőrzés előtt került `lezarva` állapotba, a `pr` üres, push nem történt. Ez ellentmond a `kovetkezo.md` 9. (új) és 10. lépésének.
3. **G4:** a `k` betű egyszerre jelöli a kör sorszámát és a tételszámot. A korlát utáni újraindítást semmi nem állítja meg.
4. **G6, besorolás:** a 2. és 3. tétel az `ir`-en kívül esik, a saját definíció szerint tehát `hatokoron_kivul`, a próba mégis `mechanikus`-nak sorolta.
5. **`ir`-en kívüli írás:** a brief törzsében is változott a D2 és az E1, nem csak a fejléc. A tartalom megfelel a jóváhagyásnak.
