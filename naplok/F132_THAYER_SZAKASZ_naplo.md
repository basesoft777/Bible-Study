# F132_THAYER_SZAKASZ — napló

*FELADATOK #132 · brief: `F132_THAYER_SZAKASZ_BRIEF.md` · ág: `claude/thayer-szakasz` (alap: origin/main `14d3484`)*
*Végrehajtó modell: `claude-opus-5-5` (a brief `modell: opus` mezőjével egyezik, modell-ellenőrzés 2026-10-25).*

## M0 — felmérés (2026-10-25, csak olvasva)

A mérések eseti szkriptekkel futottak, a repón kívül (a session scratchpadjében: `m0_meres.py`,
`m0_illeszt.py`, `m0_thayer_sorok.py`), a TSV-ket `split('\t')` olvasta. Kódot a repóba az M0 nem írt.

*(proveniencia, ha egy pont mást nem mond: `scope=konkordancia/lexikonok_nyers/Thayer.lexicon (Lexicon(Topic, Definition)), konkordancia/Thayer_teljes.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, adat/karoli_strong/parok_*.tsv, adat/elofordulasok.tsv (strong), adat/forditasok.tsv (szotar=Thayer) | forras=m0_meres.py, m0_illeszt.py, m0_thayer_sorok.py (eseti, a repón kívül) @1654e0d3 | ts=2026-10-25`)*

### 1. A brief 2. szakaszának megismétlése

| Mért | Brief (2026-10-21) | Ma (2026-10-25) |
|---|---|---|
| `G…` szócikk a `Thayer.lexicon`-ban | 5 426 | 5 426 |
| `<p>` | 17 093 | 17 093 |
| `<ref … bcv(k,f,v)>` összesen | 63 953 | 63 953 |
| G1941 `bcv` | 43 | 43 (ÚSZ 35, ÓSZ 8) |
| G4151 `bcv` | 497 | 497 (ÚSZ 473, ÓSZ 24) |
| `Thayer_teljes.tsv` sor | 5 426 | 5 426 (+ fejléc) |

A jelentéspont-fejek száma (1 685 szócikk) a bontó (M1) mérése; az M0 nem ismételte meg.
Tag-leltár (a szerkezet jelölői): `ref0` 64 478 (a héber/görög szóhivatkozás, a nyelvközi híd alapja,
2a/6), `ref` 63 953, `b` 30 519, `p` 17 093, `i` 15 930, `div` 5 426, `span` 671; ritka: `TOPIC` 338,
`REFERENCE` 224, `DATE` 171, `FOOTNOTE` 65, `BITMAP` 31, `ref2` 22, `ERROR` 12.

### 2. Licenc (DT-F132a alapja)

- `konkordancia/lexikonok_nyers/README.md` 17. sor (Thayer): „1886/1889, közkincs; a modul anyagát Tim
  Morton (Bible Analyzer) formázta, engedéllyel” — besorolás: „`közkincs` — a formázási réteg eredete
  másodkézből, ezt a README rögzíti”. Fenntartás ugyanott: a megállapítás a szerző forrásoldaláról
  származik, a fájlok licenc-jelzést nem tartalmaznak.
- `adat/licencek.tsv` Thayer-sora: közkincs (DT-F33g). A sor `javaslat`-a szó szerint: „a formázási
  réteg (Tim Morton / Bible Analyzer, "used with permission") feltételei nem ismertek, és a digitális
  kiadás commitja nincs rögzítve; a kivétel ezt a formázási réteget nem igazolja, csak a felhasználói
  döntést rögzíti.” A `lexikonok_nyers` sor: `tisztazatlan`, javaslat: a nyers `.lexicon` fájlok nem
  kerülnek a nyilvános kiadásba, csak a belőlük generált, tisztázott táblák.
- **Következtetés (értelmezés, nem lekérdezés):** a licencmondat a formázási réteg (HTML-jelölés, `bcv`-
  attribútum) adatkénti használatát **nem engedi kifejezetten**: az engedély létét másodkézből rögzíti,
  a feltételeit nem. A brief javaslatának feltétele („(a), ha a licencmondat megengedi”) így nem
  teljesül, a javaslat a (b).
- Tény a (b) mellett: a `Thayer_teljes.tsv` ugyanennek a modulnak a lapított szövege (brief 2.), tehát
  a (b) a formázási rétegtől való függést csökkenti (a kiadott szöveg nem a HTML), de nem szünteti meg
  (a szerkezet és a `bcv` koordinátái onnan jönnek). A koordináták (könyv, fejezet, vers) és a Thayer
  1889-es jelentéspont-számozása a műhöz, illetve tényadathoz tartoznak; a DT225 (BDB) mintája ugyanez
  volt: a lexikonból csak azonosító és szerkezet.

### 3. A lexikon szövege és a TSV szövege (a (b) illesztésének költsége)

A címkék nélküli `Definition` (HTML-entitások feloldva) és a `Teljes_szocikk` (a `G… — ` előtag nélkül),
szóközök nélkül összevetve, Strongonként:

| Viszony | Szócikk |
|---|---|
| azonos | 5 |
| a TSV szövege a lexikon szövegének része (a többlet összesen 32 949 karakter, átlag ≈ 6 / szócikk: a fejléc) | 5 414 |
| eltér | 7 |
| összesen | 5 426 |

Vagyis a szakaszhatárok 5 419/5 426 szócikkben gépileg átvihetők a TSV szövegére. A 7 eltérőt az M1
listázza (a #107 `reszleges`/`sikertelen` mintájára). A BDB-n a megfelelő arány 7 869/8 090 volt (DT227).

### 4. Mit hozott a #128 (lezárva, PR #456, DT285–DT291)

- **Megvan:** a szakaszhatár-token `⟪n⟫` és a darabolás (`eszkozok/bdb_jelolt/szakasz_bemenet.py`:
  `token`, `jelentes_szam` = `sz<sorszam>`, `sha1`, `csoportok`, `strong_magyar` közös összefűző);
  a `14_szakasz` kapu (`eszkozok/forditas_kapuk.py`, `kapuk_futtat_szakaszos`); a `forditas/prompt_v5.md`
  (a v4.2 + szakaszhatár-token blokk). Döntések: kulcs `jelentes_szam = sz<sorszam>` (DT285 (a)),
  `forras_hash` = SHA-1 a fordítónak átadott szakaszszövegről (DT286 (1)), 20 000 karakterig egy hívás,
  fölötte ≤ ~10 000 karakteres csoportok tokenhatáron (DT287 (2)), a felváltott régi sor `elavult`
  (DT289), jóváhagyott `kezi` sor a szakaszsorok jóváhagyásáig érvényes (DT290 (3)).
- **Szótárhoz kötött:** a `szakasz_bemenet.py` a `adat/bdb_szakaszok.tsv`-t (`TABLA`) és a
  `bdb_szakasz_hu.tsv`-t (`HU_TABLA`) tölti be; a `prompt_v5.md` fejléce szerint „csak a BDB szakaszonkénti
  bemenetéhez … A régi `teljes` út (…; a Thayer) a v4-et használja”. A v4 tartalmaz Thayer-ágat (a
  prompt 54. sora: „Te egy ógörög szótári szócikket (Thayer's Greek Lexicon) fordítasz magyarra”).
- **Nincs meg:** az `adat/tiltott_fordulatok.tsv` és a hozzá tartozó kapu. A repóban csak a
  `F121_GLOSSZA_FORDITAS_BRIEF.md` (`allapot: nem_indult`, `fugg: [11]`) és ez a brief említi; a #140
  briefje nem. **A `14`-es kapuszám foglalt** (`14_szakasz`); a brief 2a/2 `14_tiltott` neve ütközne.

### 5. A 14 kész Thayer-sor (`forditasok.tsv`, `szotar = Thayer`)

Mind `jelentes_szam = teljes`. 13 a gerincszavaké, 1 (G0994) gerincen kívül. Állapot:

| Állapot | Strong | Megjegyzés (a sorból) |
|---|---|---|
| `kezi` (jóváhagyott) 5 | G1941, G1944, G5590, G0282, G4151 | G1944, G5590: DT24 (a); G0282, G4151: DT25 (a) szúrópróba; G1941: `modell` üres, 2026.09.22 |
| `opus` 9 | G0012, G0086, G0813, G0994, G1311, G2671, G5010, G5351, G5356 | mind `claude-opus-5-5`, 2026.10.01 (#28) |

A 13 gerincszóból tehát 5 jóváhagyott `kezi` sor: ugyanaz a helyzet, mint a DT290-ben a H8415-tel.
Mind a 14 Opus-fordítás (vagy kézi), Sonnet-sor nincs.

### 6. Mankó 2a/3 — Károli-lefedettség a 13 gerincszón

A `parok_*.tsv` 61 fájl, ebből 22 tartalmaz görög Strongot (ÚSZ-könyv). Hiányzik: **Mt, Mk, Luk, Ján,
ApCsel** (a `Konyv_normalizalo_tabla.tsv` 40–44. sora). Strongonként:

| Strong | motívumhely | ebből a hiányzó 5 könyvben | Thayer `bcv` ÚSZ | ebből a hiányzó 5 könyvben | Thayer `bcv` ÓSZ | `parok`: vers | `parok`: különböző Károli-alak | motívumhely a `parok`-ban |
|---|---|---|---|---|---|---|---|---|
| G0012 | 7 | 1 | 8 | 1 | 3 | 8 | 4 | 4/7 |
| G0086 | 8 | 5 | 12 | 8 | 6 | 4 | 2 | 2/8 |
| G0282 | 1 | 0 | 1 | 0 | 0 | 1 | 2 | 0/1 |
| G0813 | 1 | 0 | 2 | 0 | 0 | 1 | 1 | 0/1 |
| G1311 | 1 | 0 | 6 | 1 | 0 | 3 | 4 | 1/1 |
| G1941 | 10 | 4 | 35 | 27 | 8 | 9 | 7 | 6/10 |
| G1944 | 2 | 0 | 3 | 1 | 2 | 2 | 1 | 2/2 |
| G2671 | 1 | 0 | 6 | 0 | 1 | 5 | 4 | 0/1 |
| G4151 | 7 | 2 | 473 | 228 | 24 | 184 | 36 | 4/7 |
| G5010 | 4 | 0 | 10 | 1 | 1 | 8 | 4 | 3/4 |
| G5351 | 1 | 0 | 8 | 0 | 0 | 7 | 9 | 1/1 |
| G5356 | 1 | 0 | 9 | 0 | 2 | 8 | 9 | 0/1 |
| G5590 | 7 | 2 | 95 | 55 | 23 | 38 | 30 | 3/7 |
| **össz.** | **51** | **14** | **668** | **322** | **70** | **278** | — | **26/51** |

*A „motívumhely” az `elofordulasok.tsv` `strong` mezőjében (a `+`-szal összetett értékek bontva) a
Stronghoz tartozó különböző igehely; a `parok`: vers a Stronghoz párosított különböző vers.*

- A motívumhelyek **14/51**-e (27%), a Thayer által idézett ÚSZ-helyek **322/668**-a (48%) a hiányzó öt
  könyvre esik. A G1941 10 motívumhelyéből 4 (ApCsel 2:21, 9:14, 9:21, 22:16), 35 idézett ÚSZ-helyéből 27.
- A lefedett könyvekben is van hiány: a 37 nem hiányzó könyvbeli motívumhelyből 26 van a `parok`-ban, 11
  nincs (a vers párosított, de a Strongot a #22 nem kötötte szóhoz, vagy a vers nincs a párosításban).
  Okonkénti bontás nem készült (M3 adatblokkja jelzi soronként).
- A hiány a blokkban és a naplóban explicit marad, nem pótoljuk (CLAUDE.md 3. szabály, brief 2a/3).
- Az ÓSZ-hivatkozás a 13 szónál 70 (főleg LXX-utalás); ezek Károli-szövegéhez a számozási eltérés az M2
  mérése.

### 7. Mankó 2a/5 — siglák előzetes listája (a forrásból, gépi, nem besorolt)

Előre megadott jelölt-minták a teljes Thayer címkék nélküli szövegén; a darabszám a minta találata
(egy minta több alakot is fog, pl. `Winer` / `W. `), a besorolás (mi ez, magyar alak) az M1 utáni kézi lépés.

| Jelölt (minta) | előfordulás | szócikk | a 13 gerincszóban |
|---|---|---|---|
| kiadás-sigla-sor (`G L T Tr WH`, `T Tr WH`, `Tr WH`) | 2 011 | 970 | 15 |
| `Rec.` | 1 046 | 678 | 19 |
| `Lachmann` | 297 | 253 | 1 |
| `Tdf.` | 541 | 403 | 1 |
| `Griesbach` / `Grsb.` | 60 | 57 | 0 |
| `Winer` / `W. ` | 3 137 | 1 547 | 10 |
| `Buttmann` / `B. <szám>` | 2 313 | 1 129 | 7 |
| `Sept.` | 1 652 | 1 449 | 12 |
| `cf.` | 7 243 | 2 855 | 61 |
| `i. e.` | 2 340 | 1 318 | 31 |
| `Xen.` / `Xenophon` | 909 | 766 | 8 |
| `Plat.` / `Plato` | 974 | 855 | 12 |
| `Hom.` / `Homer` | 1 570 | 1 397 | 7 |
| `Hdt.` / `Herod.` | 932 | 850 | 7 |
| `Thuc.` | 391 | 365 | 2 |
| `Joseph.` / `Josephus` | 841 | 680 | 2 |
| `Philo` | 384 | 340 | 3 |
| `Polyb.` | 635 | 567 | 3 |
| `Plut.` | 856 | 798 | 4 |
| `Lucian` / `Luc.` | 278 | 272 | 0 |
| `Aristot.` | 416 | 396 | 3 |
| `Vulg.` | 295 | 276 | 0 |
| `Grimm` | 129 | 115 | 1 |
| `Schmidt` | 97 | 91 | 1 |
| `Meyer` | 451 | 355 | 4 |
| `Lightfoot` / `Bp.` | 349 | 293 | 0 |
| `Trench` | 177 | 170 | 2 |
| `Apocr.` | 50 | 44 | 0 |

Generikus mérés (`Xxx.` alakú nagybetűs rövidítés): **1 209 különböző alak**, ebből 84 legalább 20-szor,
25 legalább 100-szor fordul elő; a 13 gerincszóban 66 különböző alak, 164 előfordulás. A leggyakoribbak:
`Sept.` 1 652, `V.` 1 272, `Rec.` 1 046, `A.` 966, `Macc.` 863, `T.` 807, `N.` 655, `Cf.` 590, `B.` 560,
`Sir.` 542, `Tdf.` 541, `D.` 451, `I.` 423, `R.` 421, `Wis.` 393, `Phryn.` 300, `Vulg.` 293, `Lob.` 283,
`O.` 217, `Proleg.` 212. Az egybetűs alakok (`V.`, `A.`, `T.`, `N.`, `B.`, `D.`, `I.`, `R.`, `O.`) vegyesek
(sigla, kötetszám, személynév-kezdőbetű, mondatvég); a sigla-tábla gyűjtése ezért az M1 szakaszaiból,
kontextussal készül, nem ebből a listából. A `q. v.` és a `Mdl.` / `Pass.` minta 0 találat (más írásmód;
az M1 gyűjtése pótolja, ha van).

### 8. ⛔ M0 — döntések

A felhasználó elé: DT-F132a, DT-F132b, DT-F132c, DT-F132d, DT-F132f (`DONTESEK.md`). A DT282 eldöntött,
nem kérdezett újra. A döntésig kódírás nincs.
