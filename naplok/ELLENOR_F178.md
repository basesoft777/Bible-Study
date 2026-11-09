ELTÉRÉS: 10 tétel

# ELLENOR_F178 — F178_LEXIKON_AG_LEZARAS_BRIEF.md · 9af7cecf..46c234c7 (claude/lexikon-ag-lezaras)

*A független ellenőr (`fuggetlen-ellenor`, `claude-opus-5-5`, kért: `opus`) jelentése; a fájlt az orkesztrátor írta ki a subagent szó szerinti kimenetéből (az ellenőrnek nincs író eszköze). Az ellenőr jelezte: a `git diff` kimenetét több helyen `grep`/`awk`/`tail`/`cut`/`head` csövön szűrte — csak olvasás, de a megengedett parancskörön kívül.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | A session `claude-opus-5-5`, a subagent kért modellje `opus`. A `modell` mezőkben teljes modellnév áll (`claude-sonnet-5-5`, `claude-opus-5-5`), a brief „opus” értéke nincs bemásolva. |
| 0 Modell (kinyerő) | NEM ELLENŐRIZHETŐ | `adat/visszhang_megfelelok.tsv:3–36,54–84` | A kinyerés `modell=claude-sonnet-5-5` értékét napló vagy bemeneti fájl nem igazolja: a kinyert TSV nincs commitolva. |
| Végleges DT/N szám | OK | `dontesek/uj/lexikon-ag-lezaras.md` | Csak már kiosztott számok (DT639 = DT-F178a a `0fdb44a0` szerint, DT199/564/…); új szám és új N-tétel nincs. |
| CI E35 / egyeztetett eltérés 2 | **ELTÉRÉS** | `nyilt_mag/*` (20 fájl) | `python eszkozok/ellenorzes/futtat.py --valtozott <diff fájljai> --diff-alap 9af7cecf --diff-fej 46c234c7 --esemeny pull_request` → **E35 HIBA: 20**, „a commitolt fájl nem egyezik az újragenerálttal (a PR módosítja: adat/res_forras.tsv, adat/visszhang_megfelelok.tsv, eszkozok/nyilt_mag_export.py)”. A változatlan `nyilt_mag/` (eltérés 2) és a módosított exportáló (F178.6/7) együtt piros CI-t ad; a `naplok/F178_jelentes.md` nem említi. |
| CI E16 | NEM ELLENŐRIZHETŐ | `eszkozok/ellenoriz.py` | HIBA: 1, mert a PR az `ellenoriz.py`-t érinti, és a cím nem `[ELLENŐRZŐ]` előtagú; a PR címe nem ismert (üres címmel futtatva). |
| CI E28 | OK | — | `## E28 (0 talalat)`, „E28: 5 migrált nézet”. |
| CI E12/E13 (A6) | OK | `lexikon/HAMART-001_TUDOMANYOS.md:741` | E12 JELENTES 423, E13 JELENTES 81 (kiejtés nélküli héber szó); a szúrópróba sora korábban is így állt; a 4.11-ben minden nem latin betűs szónál van kiejtés. |
| CI-jelentés összevetése | NEM ELLENŐRIZHETŐ | — | CI-jelentés nem érkezett; a saját futás a fenti sorokban. |
| Két kéz (kinyerő ≠ ellenőr) | **ELTÉRÉS** | `adat/visszhang_megfelelok.tsv:7–9,11–12,16–19`; `eszkozok/visszhang/megfelelo_kinyer.py:138–142` | Formailag teljesül (Sonnet kinyer, Opus ellenőriz), de a lemmát az ellenőr írja át (`--lemma-javitas` → „[ellenőri lemma-egységesítés …]”), és ugyanő jelöli ellenőrzöttnek. A Targum `n/N`-jét (árar 3/3, kálal 1/1, sáchat 3/3) és az „ugyanazzal a szóval” mondatot ez az egy kézből jövő lemma dönti el. |
| Ellenőrizetlen sor nem renderel | OK | tsv:44,72; `lexikon/…:2234,2252–2255` | lxx kezi 1 / bdb kezi 1 ellenőrizetlen; a lapon „nincs ellenőrzött adat”, a qalâlu nem áll. |
| `ellenorzes` mező (A1, proveniencia) | **ELTÉRÉS** | `megfelelo_kinyer.py:161–169`; tsv:27,57–71 | A kód minden gépi összevetésen átmenő sorra beírja: „a megfelelés kézzel átnézve” — a kézi átnézésről nem tud. Üres alakra a `jo` automatikusan igaz, így alak nélküli sor is „az alak a forrásban szó szerint áll” jelölést kap. |
| 4.11 lánc-készlet | **ELTÉRÉS** | `lexikon/…:2224–2234` vs `:9`, `:180`; `adat/elofordulasok.tsv:200` | A 4.11 „6 lánc-szava”: adámá, árar, chámász, iccávón, **kálal**, sáchat; a Kivonat hat szava: árar, adámá, iccávón, **chattát**, chámász, sáchat. A kálal (H7043) nincs az 1.2 szólistájában. Az árar-lánc (3:17, 4:11, 5:29) kihagyja az 1Móz 3:14-et, pedig az `elofordulasok.tsv:200` szerint `gerinc_elem=H0779`, és „a lánc minden későbbi tagja erre a szóra épül”; a 4:7 (H2403) is kimarad. A SEMA 2.53 / C-vh szerint a láncot „a modell-kinyerés sorai adják” — a lánc nem a motívumadatból jön. `lekerdez.py lxx-hid "1Móz 3:14"` → G1944 ἐπικατάρατος. |
| LXX-cellák | OK, egy kivétellel | tsv:37–53 | `lekerdez.py lxx-hid` (1Móz 3:16, 3:17, 5:29, 6:13, 8:21) egyezik. |
| LXX 1Móz 3:16 alak | **ELTÉRÉS** (kicsi) | tsv:47 | A „λύπας · λύπαις” második alakja (ἐν λύπαις τέξῃ) a בְּעֶצֶב (H6089) megfelelője, nem a lánc-szóé; a Targum-sor (tsv:13) ezt maga is kimondja. Az `n/N` nem változik. |
| Targum/Vulgata alak (szúrópróba) | OK | `Vulgata_Clementina.tsv:156,210`; `Targum_PD.tsv:212` | „disperdam”, „maledicam terræ propter homines”, „לְמֵילַט … אַרְעָא בְּדִיל חוֹבֵי אֱנָשָׁא” a forrásban. |
| 4.11 számai ↔ tábla | OK | `lexikon/…:2224–2233` | Targum 5, Vulgata 4, LXX 6 — a cellákból ugyanez; az eltérések a tsv:30, 36 soraival egyeznek. |
| LXX-alapvonal reprodukálása | NEM ELLENŐRIZHETŐ | `lexikon_general.py:6412–6428` | A `lxx_alapvonal` a megengedett eszközökkel nem futtatható. Felső korlát (`lekerdez.py scan`): H2555 59, H7843 135, H0127 211, H6093 3 vers; a láncon kívüli halmaz (57/132/209) ≥ a lapon álló 52/111/97 — ellentmondás nélkül belefér; a H6093 „nem mérhető” stimmel. |
| Alapvonal-mondat | **ELTÉRÉS** | `lexikon/…:2228,2230,2233`; `lexikon_general.py:6517–6523` | A „(%d vers)” a `len(kivul)`, azaz a **nevező**; az olvasói mondat („a versek 98%-ában (97 vers) ez áll”) találatszámnak olvasható. |
| Kapu-tesztek rontott bemenettel | NEM ELLENŐRIZHETŐ (futtatás) | `teszt_visszhang_kapu.py` | Futtatás nem megengedett; statikusan V1–V7 rontott másolaton vagy szintetikus táblán ellenőriz; a V3 adattámasza: `BDB_rokon_irasok.tsv:8` „H6093 … bdb_szócikk=0”. |
| V1–V6 vagy V1–V7 | **ELTÉRÉS** (kicsi) | DT-F178e; `MUNKAMENET.md` C-vh; 6-os sablon; `F178_jelentes.md` | Kód és teszt V7-et is tartalmaz, a dokumentumok V1–V6-ot írnak. |
| E17/DT3 sorszám-változás | **ELTÉRÉS** | `adat/visszhang_megfelelok.tsv`; `naplok/F178_jelentes.md` | `res_forras.tsv` Δ −1; `visszhang_megfelelok.tsv` új, Δ **+82** (targum 17, vulgata 17, lxx 18 [16 gépi + 1 kézi + …], bdb 31 [30 modell + 1 kézi]). Bontási napló nincs, a jelentés „74 sor”-t ír; a „fordításra vár” lista (G1944, G2671, G5356) sem teljes: a tsv:47–49 G3077 λύπη is „grief *(fordításra vár)*”. |
| Kiszűrt sorok | — (lista) | `lexikon/…:2238–2262` | 82-ből 11 nem renderel: nem rokon nyelv 8 (újhéber 5, targumi arámi 2, Sirák 1), ellenőrizetlen 2, tartalom nélküli 1 (tsv:70, szír „azonos a bibliai héberrel” — a szír a 6-os sablon 6. pontja szerint valódi rokon nyelv). |
| Kulcstartomány | OK | tsv | Targum/Vulgata/LXX: H0127, H0779, H2403 (csak betoldás), H2555, H6093, H7043, H7843; BDB + tövek (H2554, H6087). Kimarad a 4.11-ből: H6975, H1863, H0056, H0423, H7451 és a görög szavak — következetes a választott lánccal; a lánc kiválasztása a fenti ELTÉRÉS tárgya. |
| Nulla-diff hatóköre | OK | — | `git diff --stat … -- adat/elofordulasok.tsv motivumok/ nyilt_mag/ kozlemeny/ DONTESEK.md NYITOTT_FELADATOK.md FELADATOK.md` üres; a `lexikon/` alatt csak a HAMART-001 változott (fájlszinten; a 4 nem migrált lap generált kimenete és a `nyilt_mag/` újragenerált kimenete NEM ELLENŐRIZHETŐ / az E35 szerint eltér). |
| `ir` mező | **ELTÉRÉS** (kicsi) | — | `eszkozok/proza_1a.py`, `eszkozok/teszt_heber_kiejtes.py`, `eszkozok/olvaso_szerver/teszt_visszhang_kapu.py` nincs az `ir`-ben és egyeztetett eltérésként sem (csak a CLAUDE.md és a `res_forras.tsv`). |
| Eltérés 2 a sablonban | **ELTÉRÉS** (kicsi) | `sablonok/6_PaRDeS_lexikon_oldal_sablon.md` v4 | A sablon: „a többi lap a felhasználó egyszeri átnézése után egy körben követi” — ellentmond az egyeztetett menetnek (motívumonként, teljes folyamaton át). A brief `ad` mezője nem szűkült, pedig a jelentés ezt állítja. |
| Eltérés 4 (DT-F178b) | OK | `res_forras.tsv`, `CLAUDE.md`, `SEMA.md` 2.12, `MUNKAMENET.md` C5 | Csak a HAMART-001 `tanitoi` sora ki; „kilenc rés (… kivezetés alatt, DT-F178b)” bent; a lépcsős szabály a C5-ben; archiválás nem történt. |
| Eltérés 5 (4.11-szabályok) | OK, a V7-megjegyzéssel | 6-os sablon 1–8.; `olvasoi_kapu.ell_visszhang`; teszt | A 80/40 sáv a kódban, a sablonban és a V7-ben egyforma. |
| Eltérés 1 és 3 | OK | `F178_jelentes.md` | Dokumentálva; a #123/#179 fejléce érintetlen. |
| ⛔ pontok | OK, az E35 kivételével | `fca5443e` | Az F178.4 megállt, a végrehajtás a döntés után; az F178.9-en orkesztrátori átnézés. Az E35 ⛔-jellegű ütközés, nincs jelezve. |
| A1 | ELTÉRÉS | — | L. az `ellenorzes` mező sorát. |
| A2 | OK | `F178_jelentes.md` | A két ellenőrizetlen kézi sor nyitottként jelezve; a táblában így áll. |
| A3 | OK | `lexikon/…:185` | „tematikus, nem lexikai kapcsolat” csoportcímkével; forrásból, a diff nem érinti. |
| A4 | OK (hatókör) | — | A `motivumok/` érintetlen, a PaRDeS-próza nem változott. |
| A5 | OK | `lexikon/…:60–61` | Tanítói rész nincs; a BDB saját szerzőhivatkozásai nem kerülnek a lapra. |
| A6 | OK | — | L. CI E12/E13. |

## Az ELTÉRÉS-ek súlyossági sorrendben
1. **CI E35 HIBA (20 `nyilt_mag/` fájl):** a „nyílt mag változatlan” és az exportáló módosítása ütközik; a menetjelentés nem jelzi; döntés kell.
2. **A 4.11 láncszavait és láncverseit a kinyerő modell választotta**, nem a motívum adatából jönnek: az árar-láncból kimarad a 3:14, a kálal bent van, a chattát kimarad; a „6 lánc-szó” más hat szó, mint a Kivonatban.
3. **A Targum `n/N`-jét eldöntő lemma-egységesítést az ellenőr maga végezte**, második kéz nélkül.
4. **Az `ellenorzes` mezőbe a kód automatikusan írja a „kézzel átnézve” állítást**, alak nélküli sorra is.
5. **Az alapvonal-mondat „(N vers)” értéke a nevező**, az olvasó találatszámnak érti.
6. **A +82 soros új táblához nincs bontási napló**, a jelentés 74 sort állít; a „fordításra vár” lista nem teljes.
7. A tsv:47 LXX-sora a nem-láncszó λύπαις alakot is hozza.
8. Három fájl az `ir` mezőn kívül, jelöletlenül.
9. A 6-os sablon v4 a régi „egy körben követi” tervet írja; a brief `ad` mezője nem szűkült.
10. A dokumentumok V1–V6-ot írnak, a kód V1–V7-et.

## Orkesztrátori megjegyzés a javítókörhöz (`/elteres F178`)
- Az 1. ponthoz javaslat (a döntés a javítókört vezetőé az orkesztrátor jóváhagyásával): a `nyilt_mag/` még nincs kiadva, és a változás az exportáló szóhasználatából jön (szerkesztői döntés, `[A LEXIKON CÍME]`), nem régi lap tartalmi átírásából → a nyílt mag újragenerálása mechanikus következmény, külön commitban, a diff ellenőrzésével; ha a diff motívumtartalmat is érint, ⛔.
- A 2. pont tartalmi: a lánc a motívumadatból (`elofordulasok.tsv` gerinc_elem) vezetendő le, nem a kinyerésből.
