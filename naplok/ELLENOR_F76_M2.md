# Független ellenőrzés — #76 OLVASOI_KONKORDANCIA, M2 (alkalmazás)

*Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`, a kért `opus`-szal egyezik). Tartomány: `origin/main..HEAD` = `250e1b1d..efe5c402` (F76.10–F76.13). Brief: `F76_OLVASOI_KONKORDANCIA_BRIEF.md`. A jelentést az ellenőr fájlíró eszköz hiányában szövegben adta át; az orkesztrátor mentette, a tartalmát lényegében változtatás nélkül.*

**Eredmény: ELTÉRÉS, 7 tétel** (súlyossági sorrendben).

| # | Súly | Tétel | Hely | Indok |
|---|---|---|---|---|
| 1 | közepes | **K1 / D2-egyezés nem „0 eltérés”** | `naplok/OLVASOI_KONKORDANCIA_M0.md:297`, brief `:73` | A `gorog_szo:usz_elofordulas` blokkcsoport 27 (1Móz 1–25) és 11 (Zsolt 22) görög szó-lapon eltér a #60 pilottól. Ok (igazolt a TSV-oldalon): a pilot `hnorm` regexe (`olvaso_pilot/adat.py:61-66, 465-469`) a „+” Strong-láncot egészében elveti; a TAGNT-ban 255 ilyen lánc-sor van, és `lekerdez.py scan G1563 --szakasz "Mt 5:23"` → n=0 (`scope=range:Mt 5:23 \| forras=TAGNT_kivonat.tsv \| strong=G1563 \| n=0 \| ts=2026-10-14T10:56Z`). A DB-oldali (`token_strong`) 27/11-es szám nem volt ellenőrizhető (sqlite-hozzáférés nincs). A fejléc „M2 kész”-t ír, miközben a K1 szó szerint nem teljesül. **Döntés kell.** |
| 2 | közepes | K3: modell-kimenet jelölés nélkül a szövegoszlopban | `sablonok/fejezet.html:5, 16-17, 26`; `alap.html:28` | Az Olvasópult aláhúzott szavai és az Interlineáris szópárok a `token_par`-ból (regiszterben `modell` jellegű) jelleg-címke és forrássor nélkül jelennek meg; a pilotban magyarázó sor volt (`sablon.html:389`). A lábléc állítása a szövegoszlopra nem igaz. |
| 3 | közepes–alacsony | A D2-teszt nem őrzi az eltérés okát | `teszt_olvaso_szerver.py:622-628, 656` | A `felvesz()` eldobja az `ok` mezőt; bármilyen okú `usz_elofordulas`-eltérés átmegy. A docstring (576–578) többet állít. |
| 4 | alacsony–közepes | Jelleg-összevetés a pilottal hiányzik | `OLVASOI_KONKORDANCIA_M0.md:96`; `blokkok.py:552,553,556,572,579` | Az M0 3.4 ígérte a tesztet; nincs. Öt blokk jellege eltér a pilotétól (`vers.versszamozas`, `szo.usz`, `vers.bsb`, `szo.tbesh`, `vers.tipnr`). |
| 5 | alacsony | `telepit.sh`: a frissességi feltétel nincs kikényszerítve | `telepit.sh:17,19,33-35` | Az `indit` nem követeli az `ellenorzes` sikerét; a `.venv` és a `frissesseg_eredmeny.txt` ignore nélkül a repón belül jön létre. |
| 6 | alacsony | `hozzaferes.toml`: ismeretlen blokk-azonosító nincs ellenőrizve | `hozzaferes.py:23-25, 50` | Elgépelt kulcs csendben elvész, a blokk a `default = "nyilvanos"` szintre esik (nyitva marad). Ma következmény nélküli. |
| 7 | alacsony | A döntéskérés csak a naplóban áll | `OLVASOI_KONKORDANCIA_zaras.md:23` | `DT-F76…` helyőrző a `DONTESEK.md`-ben nincs. |

**OK (igazolva):** a DB nem kerül ki (`/pardes.db` → 404, csak `statikus/` kiszolgálás); SQL minden `?`-paraméteres; XSS: autoescape, CSP inline nélkül; kiadási kapcsoló és authorizer (KJV nyilvánosból, MCGED kereskedelmiből kimarad); a süti csak `/nezet/<nev>`-nél jön létre; K2 (nézetek, kezdőlap); az Interlineáris pozíció szerint illeszt (`token_par.hu_sorszam = token_karoli.sorszam`); 56 teszt (darabszám egyezik); `ir` mezőn kívüli változás nincs (27 fájl); fejléc `megallt`, ⛔ M5–M7 érintetlen; nincs `csv` modul; magyar commitok `F76.1x:` előtaggal; proveniencia az M0 4.4-ben; `adat/` és `konkordancia/` Δ = 0; `futtat.py` CI-ellenőrzés exit 0.

**Nem ellenőrizhető az ellenőr szerepkörében:** a tesztek futtatása (3.12, WSL) — az „56 zöld” a végrehajtó állítása; a DB-oldali 27/11-es szám; N-F76b/N-F76c (M3/M4-hez kötött).
