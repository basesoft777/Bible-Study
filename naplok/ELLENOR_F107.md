ELTÉRÉS: 6 tétel

# ELLENOR_F107.md — független ellenőrzés

- **Brief:** `F107_BDB_JELOLT_SZOVEG_BRIEF.md` (FELADATOK #107)
- **Tartomány:** `89b30c2e..590f897c` (46 commit, F107.0–F107.45; ág `claude/f107-bdb-jelolt-szoveg`)
- **Ellenőr modellje:** `claude-opus-5-5` (kért: `opus`, egyezik)
- **Rögzítés:** az ellenőr (`fuggetlen-ellenor` subagent) fájlíró eszköz nélkül futott; a jelentést a visszaadott szövegéből az orkesztrátor írta fájlba, tartalmi változtatás nélkül. Az ellenőr két saját eltérése: néhány `git diff` kimenetét `grep`/`sort`/`wc`/`cut` szűrte (a megengedett parancskörön kívül); a `teszt_bont.py` és a `--ellenoriz` futtatását a subagent-szabálya tiltja, ezért azok NEM ELLENŐRIZHETŐ eredményt kaptak.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | Az ellenőr modellje `claude-opus-5-5`, a kért `opus`: egyezik. A napló fejléce („Futtatta: claude-opus-5-5”, `naplok/F107_BDB_JELOLT_SZOVEG_naplo.md:3`) tényleges modellnevet ír. Az új táblákban nincs `modell` oszlop. Hogy a végrehajtó valóban ez a modell volt-e, nem igazolható. |
| D DT225 (forrás, licenc, megőrzés) | OK | `DONTESEK.md`, `konkordancia/lexikonok_nyers/DictBDB.json` | `git diff --raw --abbrev=40 base head -- konkordancia/lexikonok_nyers/DictBDB.json` → `A`, blob `9d6011ea9e3c61833be7a905d6d18e2363aaf37c`, egyezik a `licencek.tsv` BDB-sorában az F33 óta rögzített blobbal. A hibrid forrást a tábla fejléce mutatja: `DictBDB.json@5d826c580a4d` + `BDB.lexicon@c998a70b432f`. |
| D DT225: SHA-256 | NEM ELLENŐRIZHETŐ | `licencek.tsv:7`, a két README, `bont.py:51` | Az `5d826c58…e33d` mind a négy helyen azonos (diff alapján); a SHA-256 a megengedett parancsokkal nem számolható. A blob-SHA-1 egyezése tartalmi azonosságot mutat. |
| D DT226 (playbook) | OK | `Rendszerfejlesztesi_playbook.md:84-97` | F107.5 (döntés 🟢) után F107.6 (playbook); CI-kapu nincs, a döntés szerint. |
| D DT227 (`bdb_id` nélküli sor) | OK | `adat/bdb_szakaszok.tsv` | `sorszam=1`: 8 090 Strong; `egyezik` 7 916; `reszleges\|sikertelen\|csonk` 144. Üres `bdb_id` egyező vagy `szocikk_resze` sorban: 0; `BDB…` azonosító nem egyező sorban: 0. A hiány explicit, nincs kitöltve. |
| D DT228 (pe/mem) | OK | `adat/bdb_forras_javitas.tsv` | 7 200 sor; `pe_mem … javitva` 3 823; `hivatkozas` 412; `kezi` 7, mind `manual` (6785–6791. sor). |
| D DT229/h (4. lépés ⛔) | OK | `DONTESEK.md`, napló 4.5–4.8 | Mindkét kör megállt (F107.20, F107.26: `dontesre_var`), döntés után folytatódott. A 4. szabály elvetett első változata nem került commitba. |
| 4. lépés: ≥ 99%-os mérce | ELTÉRÉS | napló `:485-487`, `:779-781` | Aranyminta `forras_hiba` nélkül 411/416 = 98,8%. A `DONTESEK.md`-ben nincs felhasználói döntés a 99% alatti elfogadásról; a DT230 feltétele csak a „ne romoljon” volt. |
| D DT231 (6. lépés ⛔) | OK | — | `git diff --stat base head -- konkordancia/BDB_teljes_unabridged.tsv adat/forditasok.tsv konkordancia/lexikonok_nyers/BDB.lexicon eszkozok/forditas_kapuk.py` → üres. |
| D DT232 (7. lépés ⛔) | OK | `adat/bdb_szakasz_hu.tsv` | 674 Strong; soronként `illeszkedik` 6 395, `horgonnyal` 202, `elakad` 606, egyezik a SEMA 2.32 és az F38-átadás számaival. A Strong-szintű 409/85/98/82 saját lekérdezéssel NEM ELLENŐRIZHETŐ. |
| D DT190 | OK | SEMA 2.30, `datasetek.tsv`, F102/F38 átadás | `DONTESEK.md:265` 🟡; mindenütt „nincs befagyasztva”. |
| végleges DT/N szám | OK | — | Csak a meglévő DT174, DT181, DT190; az új tételek helyőrzősek (DT225–h, N-F107a/b). |
| `ir` mező / F102–F38 fejléc | OK | — | Minden fájl az `ir`-ben, ill. a `DONTESEK.md`/`NYITOTT_FELADATOK.md` saját soraiban. Bővítés: F107.7 (`licencek.tsv`), F107.41 (F102, F38). Az F102/F38 diffje csak törzsbeszúrás, a fejléc nem változott. |
| `licencek.tsv` | OK | `adat/licencek.tsv:7` | numstat 1/1; csak a BDB-sor 3. mezője bővült. |
| TSV-írás / wrapper | OK | `eszkozok/bdb_jelolt/*.py` | `import csv\|csv\.` → 0. A `reconfigure` blokk mind a 9 fájlban az importok után. Írás `'\t'.join`, `newline='\n'`. |
| teszt / `--ellenoriz` | NEM ELLENŐRIZHETŐ | — | Az ellenőr szerepe nem engedi. (Az orkesztrátor saját futása: `python eszkozok/bdb_jelolt/teszt_bont.py` → OK.) |
| reprodukálhatóság (CRLF) | ELTÉRÉS | `bont.py:94-99`, `:630-632`; `.gitattributes` | A `sha256_fajl` a munkafa nyers bájtjait hasheli; `.json`-szabály nincs, a repó `autocrlf=true`. CRLF-es checkouton a `bont.py` „HIBA: a DictBDB.json hash-e eltér” üzenettel leáll. Ebben a worktreeben a fájl LF-es. |
| 3 szabály: proveniencia | OK | táblák, napló | Minden táblasorban `proveniencia`, fejlécben `# forras:` hash-ekkel; kézi sorok `manual`. Kivétel: az N-F107a 2 782-es száma repón kívüli egyszeri szkriptből (NEM ELLENŐRIZHETŐ). |
| 3 szabály: nincs közvetlen út | OK | — | `elofordulasok.tsv`, `jeloltek.tsv` változatlan; az új táblák „nem study-adat”. |
| 3 szabály: memória vs. lekérdezés (A1) | OK | napló `:36`, `:493` | Az értelmező állítások jelölve. |
| brief 5. (H7626 „145:”) | ELTÉRÉS | napló `:491-493`, `:784` | A brief 5. lépésének példája nincs a javítótáblában; jelezve, alacsony súlyú. |
| elfogadás: TSV-Strong lefedés | OK | SEMA 2.30 | H0747, H4123, H4725, H1753, H3367, H3848, H6433, H7560, H8065 nincs a táblában (listázva); H1296 `csonk`, `bdb_id` nélkül. |
| elfogadás: nézet-eltérés osztályozva | NEM ELLENŐRIZHETŐ | napló 6.1 | „egyéb 0” a napló állítása. |
| aranyminta, seed-101, korpusz | NEM ELLENŐRIZHETŐ | F102 1c., napló 4.8 | Szúrópróba: a seed-101 M102/M117/M162 kézi sorai léteznek. A H6440 II. szakaszában nincs `-/3` csomópont (2/b után 4); a `jel` 10. sorában „7. 2. a.” áll, kézi sor nélkül (vö. H1242 „2. g.”). |
| A2 (NYITOTT) | ELTÉRÉS | `NYITOTT_FELADATOK.md` N-F107b | Az N-F107b szövege elavult: „A #38 briefjét a #107 nem írja (nincs az `ir` mezőben)”, holott az F107.41–43 beírta. |
| kozmetikai elavulás | ELTÉRÉS | `adat/datasetek.tsv` (4 új sor), SEMA 2.30/2.31 | „az aranyminta-mérés a #107 4. lépésében” — már elkészült; a SEMA 2.30 forráshivatkozó sora duplán áll; a SEMA 2.31 „Állapot (F107.23)” mellett „7 200 sor (F107.33)”. |
| A3 / A4 / A5 | OK (nem alkalmazható) | — | Nincs párhuzam, Remez/Sod, nevesített tanító. |
| A6 (E12–E15) | OK | — | E12–E15: 0 találat. |
| CI-jelentés | NEM ELLENŐRIZHETŐ | — | Saját futás (`futtat.py --valtozott … --diff-alap 89b30c2e… --diff-fej 590f897c…`): exit 0, HIBA nincs; E25 3 és E27 40 találat, egyik sem a diff fájljában. |
| CL1 kiszűrt / törölt sorok | OK | — | Törlés: `licencek.tsv` 1 (cserélt sor), brief 3 (fejléc). Kiszűrt: 9 TSV-Strong (F57 3, F72 6); a `hu`-tábla a 674 lefordított Strongot tartalmazza; a H7626 nincs a javítótáblában. |
| CL2 kulcstartomány | OK | — | 8 090 + 9 listázott = 8 099 TSV-sor; a `hu`-tábla 674/674. |
| CL3 nulla-diff hatóköre | OK | — | `forditasok.tsv`, `BDB_teljes_unabridged.tsv`, `BDB.lexicon`, `forditas_kapuk.py`, `_convert_bdb.py` változatlan; a generált táblák bájtos reprodukálhatóságára nem terjed ki. |
| CL4 sorszám-Δ (E17/DT3) | OK | — | `bdb_szakaszok` +36 621, `bdb_forras_javitas` +7 200, `bdb_szakasz_hu` +9 664 (mind új, kategóriás bontással: SEMA 2.30–2.32); `datasetek` +4; `licencek` 0 (1/1). |
| CL5 ⛔ pontok | OK | — | 1. lépés: F107.3 → .4 → .5, playbook csak utána; 4.: .20/.26; 6.: .31 → .32; 7.: .36 → .37. A döntések az orkesztrátoron át érkeztek; a felhasználói eredet NEM ELLENŐRIZHETŐ. |
| merge-kockázat | ELTÉRÉS | — | A main a base óta 149 committal előrébb. `DONTESEK.md` és `datasetek.tsv`: mindkét ág a fájl végére ír → szöveges ütközés. `NYITOTT_FELADATOK.md`: ütközhet. Nem ütközik: `licencek.tsv`, F102, SEMA. A main SEMA-ja (KJV, F118) hivatkozik a `DT226` helyőrzőre — a `szamkiosztas`-nak azt is követnie kell. A #38 `fut`, az F38 törzse később ütközhet. |

**Az ELTÉRÉS-ek súlyossági sorrendben:**

1. A ≥ 99%-os aranyminta-mérce nem teljesül (98,8%), és az elfogadásáról nincs felhasználói döntés a `DONTESEK.md`-ben.
2. Reprodukálhatóság: CRLF-es checkouton a `bont.py` a munkafa-hash miatt leáll; `.gitattributes`-szabály nincs.
3. Merge-kockázat: biztos szöveges ütközés a `DONTESEK.md`-ben és a `datasetek.tsv`-ben; a main hivatkozik a `DT226` helyőrzőre.
4. Az N-F107b szövege elavult.
5. A brief 5. lépésének H7626 „145:” példája hiányzik a javítótáblából (jelezve).
6. Kozmetikai elavulás a `datasetek.tsv` szövegében és a SEMA 2.30/2.31 állapotsoraiban.
