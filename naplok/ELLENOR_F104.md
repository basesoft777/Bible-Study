ELTÉRÉS: 2 tétel
# ELLENOR_F104 — `F104_BDB_MEGJELENITES_BRIEF.md`, `1dbf7854..9259543f`

*A `fuggetlen-ellenor` jelentése (modell: claude-opus-5-5). Az ellenőrnek nincs fájlíró eszköze, ezért a szöveget az orkesztrátor írta ki szó szerint és commitolta.*

Az ellenőr két szabálysértést jelzett magáról. Kétszer túllépte a megengedett Bash-kört: egyszer `git grep … | awk | sort | uniq -c` (a H7843 sorainak útvonalankénti száma), egyszer `git diff … | grep` (eredmény nélkül). Írás egyik sem volt. Ezért a `teszt_futtat.py`-t és a generátort sem futtatta.

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 Modell | OK | — | A session `claude-opus-5-5`, a kért `opus`. A napló és a zárás `modell`-jelölése `claude-opus-5-5`, a tényleges modell. Adattábla nem változott. |
| Brief 4. „semmi nem rejtődik” | OK (kód és teszt) | `teszt_olvaso_szerver.py:1512` | `git diff` alapján: a jelölés nélküli blokk azonos a vers nélküli lapéval. Nem futtatta. |
| Brief 4. „nem idézi”: nincs kiemelés, nincs tippelt pont (DT178, külön kérés (2)) — szerver | OK | `blokkok.py` `VersJelolo.__init__`, `_ebben_html` | Az erős és a gyenge jelölés csak a `karoli_vers == ig` táblasorból jön. A nem köthető `_dom` nem kap kiemelést. Idézet nélküli versnél csak a törzs-`div` kap jelölést, `li` nem. Tesztek: `:1454`, `:1529`. |
| (2) DT178 — lexikonlap 4.2 | **ELTÉRÉS** | `lexikon_general.py:3661–3687`, `bdb_olvasoi_reteg` | Tippelt pont nincs: a nem idézett, a tartományban idézett és a pont nélküli helyet külön mondat mondja ki. **Viszont** a bizonytalan okkódú sor (`sigla_kozel`, `forras_hiba` stb.) az „A motívum helyein” sorban az erőssel azonos alakban áll. A DT178 és a szerver szerint ez gyenge („vonatkozhat”) szint. Az `adat['bdb_vj']` csak a `szurt` és a `karoli_vers` mezőre szűr (`:2696–2700`). Grep: 176 bizonytalan okkódú sor a `bdb_vers_jelentes.tsv`-ben. A HAMART-001 öt fő Strongján nincs ilyen sor, tehát ma látens. |
| Brief 4. a gyenge jelölés vizuálisan és szövegesen is különbözik | OK | `olvaso.css` diff, `_jelzes` | A két jelölés más tokent kap (`accent-soft` / `gold-soft`), a gyenge felirata dőlt, és a szöveg is más („a BDB itt idézi” / „vonatkozhat”). |
| Brief 4. a „próba” felirat és a pontosság egy dobozban | OK | `_ebben_html` | A `proba` a `bdb-ebben` dobozon belül áll. Teszt: `:1554`. |
| (3) a pontosság egy forrásból | OK | `konfig/bdb_pontossag.toml:9–16` | Grep a `91[,.]5\|86[,.]7\|183/200` mintára az `eszkozok/` alatt: csak a toml-ban és a tesztben fordul elő. A `blokkok.py` a toml-ból számol. Proveniencia-sor van, súgóban is. A brief 92,0%-át a DT658 (a) (`DONTESEK.md:689`) írja felül. A brief szövege nem frissült. |
| Brief 2. pont: `?vers=` | OK (döntéssel elhalasztva) | `alkalmazas.py:191–194` | A `/szo/<strong>` nem vesz át paramétert, az N-F104b valóban nyitott. A DT-F104c (2) szerint kimarad. |
| Brief 4. a regiszter-őr | NEM ELLENŐRIZHETŐ | `elemek.toml` (+5 elem), `olvaso.css` | Nem futtatta. Megfigyelés: a `.bdb-ebben` a `space-utmutato-fugg` és `space-utmutato-vizsz` tokent is használja, a regiszterbejegyzés ezeket nem sorolja fel. |
| (1) E28 — öt TUDOMÁNYOS lap | OK | `e28_migralt_nezetek.tsv` | Saját `futtat.py --valtozott <19 fájl> --diff-alap 1dbf7854 --diff-fej HEAD` futtatás: „E28 (0 talalat) — E28: 5 migrált nézet”. A regenerálást a CI saját kódja végezte. |
| (1) E28 — „generált társnézetek” (TORZSCIKK) | NEM ELLENŐRIZHETŐ | — | Az E28 listáján csak az öt `_TUDOMANYOS.md` áll. A generátort a megengedett parancsokkal nem futtathatta. |
| (4) csak az `ir` szerinti fájlok változtak | OK, megjegyzéssel | `git diff --numstat 1dbf7854..HEAD` | 19 fájl. Minden kódfájl szerepel a végső `ir`-ben. A többi: napló, `dontesek/uj`, `nyitott/uj`, a brief fejléce. A `teszt_tervezo.py`, `teszt_pilot_aranymintaval.py`, `bdb_pontossag.toml` és a lexikon-fájlok utólag kerültek az `ir`-be (F104.2). A napló 1. szakasza ezt egyeztetett eltérésként rögzíti. |
| (5) az új tesztek zöldek; a régi bukások a base-en is | NEM ELLENŐRIZHETŐ | — | A `teszt_futtat.py` nincs a megengedett parancsai között. A napló 7. szakasza zöld eredményt és változatlan régi bukásokat állít, de ezt nem igazolta. |
| (6) TSV-kezelés `csv` nélkül | OK | `olvasoi_kapu.py` `_bdb_jelek_rx` | Grep az `import csv\|csv\.(reader\|writer\|Dict)` mintára a négy módosított modulban: nincs találat. Az új TSV-olvasás `sor.split('\t')`. |
| (7) „csak alakot közöl (N hely)” — Pi'el, H7843 | OK | minta: `HAMART-001_4.2_heber.md:441` | A `bdb_szakasz_hu.tsv:33123` szövegében 5 hivatkozás áll, a `bdb_vers_jelentes.tsv`-ben 5 `Pi'el/-` sor (146662–146666). N = 5 helyes. Megjegyzés: a Pi'el alatt az 1. és 2. jelentés glosszával áll, így a „csak alakot közöl” a törzs fejbekezdésére igaz, a törzsre nem. |
| (7) „csak alakot közöl (N hely)” — Hiph'il, H7843 | **ELTÉRÉS** | `lexikon_general.py` `bdb_olvasoi_reteg` (`n = len(hivatkozasok_a_szovegben(hu))`); minta `:444` | A kód „(1 hely)”-et ír. A tábla szerint 13 `Hiph'il/-` sor van, az angol fejbekezdésben (`bdb_szakaszok.tsv:33126`) szintén 13 hivatkozás. Ok: a magyar bontás az angol „1 singular”-t „1.” pontnak vette (`bdb_szakasz_hu.tsv:33127`), így a Hiph'il magyar fejbekezdésében csak 1 hely maradt. Az N tehát a magyar szakaszszöveg regexéből jön, nem a táblából; hibás bontásnál téves. Ugyanez érinti az `_osszecsukva_uj` „(N hivatkozás)” címét is. |
| 3 CI-jelentés összevetése | NEM ELLENŐRIZHETŐ | — | Végrehajtói CI-jelentés nem volt. A saját futtatás eredményei: E25 3 (JELENTÉS/FIGY); **E27 1 HIBA** + 43 JELENTÉS (a HIBA a csonkolt „további 41” között van, nem tudható, ehhez a diffhez tartozik-e); E28 0; E32 1 (`blokkok.py:1681` DT-F76d, nem a diff hunkjaiban); E34 41 FIGY (`elofordulasok.tsv`, nem változott); E36 1. Kilépési kód 0. |
| A1–A6 | OK / nem értelmezhető | — | Nincs tanulmány és nincs motívumadat, ezért az A1, A3, A4, A5 és A6 nem értelmezhető. A2: az N-F104b nyitott (`alkalmazas.py:191`). Az N-F104a (hiányzó BDB-jelek) állítását nem mérte: NEM ELLENŐRIZHETŐ. |
| Lista 1. kiszűrt vagy törölt sorok | OK | `git diff --numstat` | 56 törölt sor, mind kód vagy tesztcsere. Adatsor nem törlődött. |
| Lista 2. kulcstartomány-lefedettség | nem értelmezhető | — | Adattábla nem változott. |
| Lista 3. a „nulla-diff” hatóköre | OK, megjegyzéssel | — | A bájtazonosság az E28 öt TUDOMÁNYOS nézetére igazolt, kikapcsolt kapcsolóval (`KETRETEGU_BDB_KARTYA = frozenset()`, a diffben). A TORZSCIKK-re és a bekapcsolt állapotra nem vonatkozik. |
| Lista 4. a táblák sorszámának változása (E17, DT3) | OK | `git diff --numstat 1dbf7854..HEAD` | Az `adat/` és a `konkordancia/` alatt egyetlen `.tsv` sem változott; minden tábla Δ = 0. |
| Lista 5. a ⛔ pontok | OK | brief fejléce: `allapot: megallt` | A 4. lépés (felhasználói próba) előtt megállt. Az F104.5–8 a DT-F104a/c alapján készült, lapot nem generált újra. |

## Az ELTÉRÉS-ek súlyossági sorrendben

1. **(7) Hiph'il:** a „(N hely)” szám a magyar szakaszszöveg regexéből jön, nem a vers → jelentés táblából. A H7843 Hiph'il-nál ez 1, a valós érték 13. A kapcsoló ki van kapcsolva, így ma egyik lapon sem jelenik meg, de a #182 bekapcsolásával megjelenne.
2. **DT178 a lexikonlap 4.2-ben:** a bizonytalan okkódú táblasor az olvasói rétegben erős pontként áll, a szerverrel ellentétben nem kap gyenge jelölést. Ma látens: a kapcsoló ki van kapcsolva, és a HAMART fő Strongjain nincs ilyen sor.

## Nyitva maradt

- az E27 HIBA hovatartozása (a PR CI-futásából olvasandó);
- a tesztfuttatás igazolása (`teszt_futtat.py --gyors`);
- a regiszter-őr futtatása, és a `.bdb-ebben` két nem felsorolt tokenje.
