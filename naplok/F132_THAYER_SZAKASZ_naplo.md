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

### 2. Licenc (DT327 alapja)

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

*Pontosítás (F132.19, ELLENOR_F132 2. tétel, DT337 (a)):* a `G0813` sor (motívumhely 1) a KIRALY-001 / Zsid 7:1-28 sor hibás
`strong` mezőjéből (`G5010+G0813+G0282`) jött, ellenőrzés nélkül átvéve; a G0813 a Zsid 7:1-28-ban nem fordul elő (egyetlen helye
az 1Thessz 5:14), az *ἀπάτωρ* a Zsid 7:3-ban G0540. A mező az F132.19-ben `G5010+G0540+G0282`; a 6. tábla G0813-sora a mérés pillanatának
állapota, a G0540-re ez a tábla nem mért (a lekérdezés sorai: a „Javítókör 1” szakasz, F132.19).

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

A felhasználó elé: DT327, DT328, DT329, DT330, DT331 (`DONTESEK.md`). A DT282 eldöntött,
nem kérdezett újra. A döntésig kódírás nincs.

## Döntések (2026-10-25)

A felhasználó (chat, szó szerint): „mind a javaslat szerint, az M3 külön Sonnet-menetben”. Átvezetve
(`DONTESEK.md`, 🟢; a brief 6. döntésnaplója és `ir` mezője):

- **DT327 (b):** szerkezet és `bcv` a `Thayer.lexicon`-ból, szöveg a `Thayer_teljes.tsv`-ből illesztéssel.
- **DT328 (1)+(2)+(3)+(4):** a két tábla a SEMA 2.30 / 2.29 mintájára, `Strong_padded`, fordítási kulcs
  `sz<sorszam>`, a normalizálás egy függvény.
- **DT329 (a)+(i)+(ii):** újrafordítás; a 8 gerinc-`opus` sor `elavult`, az 5 `kezi` a jóváhagyásig érvényes.
- **DT330 (1)+(S):** közös lánc, a #128 fájljai nem változnak; Sonnet; **az M3 külön Sonnet-menetben**.
- **DT331 (b):** a #132 építi a tiltott-fordulat táblát és kaput, `15_tiltott` számmal.

## Egyeztetett eltérés

- **Hatókör (DT332 (1), felhasználó, 2026-10-25, chat: „1, újrafuttatható M3”):** az M3 nem a brief 2.
  szakaszának rögzített 13 görög gerincszavára fut, hanem a motívumok aktuális görög gerincszavaira, a futás
  pillanatában (`adat/elofordulasok.tsv` `strong`, `Strong_padded`); a már érvényes (nem `elavult`,
  `forras_hash`-egyező) szakaszos fordítású szavak kimaradnak. Az M3 újrafuttatható; a listát egy tesztelt
  eszköz állítja elő az `eszkozok/thayer_jelolt/`-ban (M3-előfeltétel). A brief M3-a, 5. (3. pont) és 6.
  szakasza, valamint az `ad` mező átírva.

## M1 — bontó (2026-10-25)

`eszkozok/thayer_jelolt/bont.py` (a `bdb_jelolt/bont.py` mintájára), `kulcs.py` (a `G12` → `G0012` normalizálás egyetlen
függvénye, DT328 (4)), `teszt_bont.py` (16 teszt, zöld). Kimenet: `adat/thayer_szakaszok.tsv` (SEMA 2.34), `--ts 2026-10-25`,
`--ellenoriz` azonos.

*(proveniencia: `scope=konkordancia/lexikonok_nyers/Thayer.lexicon, konkordancia/Thayer_teljes.tsv | forras=eszkozok/thayer_jelolt/bont.py --ts 2026-10-25 (a fejlécsor hash-eivel); m1_felmer*.py, m1_elter.py, m1_veszt.py (eseti, a repón kívül) | ts=2026-10-25`)*

### Felmérés (a szabályok alapja)

- A határ: a `<p>`, `</p>`, `<div>`, `</div>` jelölő; a címkék nélkül nem üres darab a bekezdés. Így 17 093 bekezdés (= a forrás
  `<p>`-száma). 112 szócikkben a HTML egymásba ágyazott vagy lezáratlan `<p>`-t tartalmaz (pl. G21: második címsor `<p><p>…</p>, (…`;
  G687: `<div></p><p><p>…`), ezért a `<p>…</p>` pár nem használható határnak.
- Fejek a bekezdés elején: `<b>1.</b>` szám 3 274, `<b>a.</b>` betű 2 536, `<span class="lexheading">I.</span>` római 162, sima
  `A. ` nagybetű 13 (G1223, G1325, G1519, G1909). Bekezdésen belüli félkövér fej: 0; kombinált fej (`1. a.`): 0.
- Címsor: `<b>G… — …</b>` 5 537, `<b>G…a: …</b>` 20 (al-címszó, pl. G299a). 6 szócikk első bekezdése nem a saját címe (G299 →
  G299a, G687 lezáratlan stb.).

### Eredmény

| Mért | Érték |
|---|---|
| Strong | 5 426 (a TSV-ben a lexikonon kívül: 0) |
| sor (bekezdés) | 17 093: `cim` 5 557, `fej` 5 545, fejes 5 985, fej nélküli örökölt 6 |
| fejes szócikk | 1 687 (a brief 1 685-öt mért a `<b>` fejekre; +2 a csak római / nagybetűs fejű szócikk) |
| illesztés | `egyezik` 5 411, `reszleges` 15, `sikertelen` 0 |

Az M0 3. pontja 7 eltérő szócikket mért (a „TSV a lexikon része” részsztring-próbával); a sorrendhű bekezdésenkénti illesztés
szigorúbb, 15-öt talál. Mind a 15-ben **egyetlen összefüggő szövegrész hiányzik a TSV-ből** (TSV-többlet 0):

| Strong | lexikon (szóköz nélkül) | TSV | hiány | a hiány előtti alak |
|---|---|---|---|---|
| G0260 | 455 | 295 | 160 | `πρωι` |
| G0575 | 11 509 | 11 431 | 78 | `πρωι` |
| G0846 | 11 313 | 11 208 | 105 | `νοι` |
| G1100 | 2 935 | 2 313 | 622 | `νοι` |
| G1909 | 27 276 | 27 195 | 81 | `πρωι` |
| G2675 | 1 515 | 1 341 | 174 | `νοι` |
| G3536 | 256 | 165 | 91 | `Νινευι` |
| G3563 | 1 362 | 1 177 | 185 | `νοι` |
| **G4151** | 19 530 | 19 512 | 18 | `νοι` („1Co 14:15, 1Co 14:16.”) |
| G4404 | 530 | 30 | 500 | `πρωι` |
| G4405 | 363 | 61 | 302 | `πρωι` |
| G4406 | 367 | 269 | 98 | `πρωι` |
| G4407 | 269 | 169 | 100 | `πρωι` |
| G5132 | 1 443 | 1 251 | 192 | (a `Fritzsche on Additions to` után) |
| G5567 | 909 | 900 | 9 | `νοι` |

Összesen 2 715 karakter. A tábla ezeket `reszleges` jelöléssel, közelítő (a difflib egyező blokkjaira vetített) szakaszhatárral
hordozza; üres szakasz nincs. A G4151 gerincszó: az M3 előtt döntés kell (**DT333**, `DONTESEK.md`, 🟡; javaslat: javítótábla
a DT228 mintájára).

### G1941 aranyminta (kézzel ellenőrizve a forrás HTML-jén)

| sorszam | utvonal | jel | a szöveg eleje |
|---|---|---|---|
| 1 | `cim` | | G1941 — ἐπικαλέω |
| 2 | `fej` | | ἐπικαλῶ: 1 aorist ἐπεκαλεσα; … the Sept. very often for קָרָא; |
| 3 | `-/1/-` | 1. | to put a name upon, to surname: … |
| 4 | `-/2/-` | 2. | ἐπικαλεῖται τό ὄνομα τίνος ἐπί τινα, after the Hebrew … |
| 5 | `-/3/-` | 3. | τίνι with the accusative of the object; … |
| 6 | `-/4/-` | 4. | to call upon (like German anrufen), to invoke; … |
| 7 | `-/5/-` | 5. | Hebraistically (like יְהוָה בְּשֵׁם קָרָא …) |

7 bekezdés, 5 fej, `egyezik` — a brief száma. Megjegyzés az M2-höz: az 5. pontban az „Act 9:14,21; 22:16” sorozatból csak az
ApCsel 9:14 `bcv`-jelölt, a 9:21 és a 22:16 a forrásban jelöletlen szöveg (a `bcv`-tábla nem pótolja, l. M2).

Kimaradt (nem a brief `ir`-e): az `adat/datasetek.tsv` `Thayer_szakaszok` sora (a `BDB_szakaszok` mintájára) — külön tételben.
*Megtörtént az F132.23-ban (ELLENOR_F132 6. tétel; a felhasználó jóváhagyásával az `ir` bővült): `Thayer_szakaszok` és `Thayer_vers_jelentes`, l. „Javítókör 1”.*

## M2 — igehely → jelentéspont (2026-10-25)

`eszkozok/thayer_jelolt/vers_jelentes.py`, `teszt_vers_jelentes.py` (9 teszt, zöld). Kimenet: `adat/thayer_vers_jelentes.tsv`
(SEMA 2.35), `--ts 2026-10-25`, `--ellenoriz` azonos.

*(proveniencia: `scope=Thayer.lexicon (bcv), Konyv_normalizalo_tabla.tsv, Karoli_1908.tsv, adat/elofordulasok.tsv (G1941) | forras=eszkozok/thayer_jelolt/vers_jelentes.py --ts 2026-10-25; m2_meres.py (eseti, a repón kívül) | ts=2026-10-25`)*

**Sémaeltérés (a végrehajtóé, jóváhagyásra):** a DT328 (2) nyolc oszlopa mellé egy kilencedik került, a `szakasz` (a
hivatkozást tartalmazó bekezdés sorszáma, a `thayer_szakaszok.tsv` kulcsa). A `sorszam` a 2.29 mintájára a hivatkozás sorszáma
(egyedi kulcs); a `szakasz` nélkül a hivatkozás nem köthető egyértelműen a szakaszsorhoz, mert az örökölt útvonalú bekezdések
útvonala nem egyedi.

| Mért | Érték |
|---|---|
| sor = `bcv` | 63 953 (ÚSZ 58 266, ÓSZ 5 687) — a brief száma; `bcv` nélküli `<ref>`: 0 |
| ismeretlen könyvszám | 0 |
| `karoli_vers` üres, ÚSZ | 28: Róm 17 (3:31 ×9, 8:39 ×8: a `Karoli_1908.tsv` Róm 8-a 38, Róm 3-a 30 versű), Ján 1:52 ×6, ApCsel 19:41 ×2, 1Kor 3:23 ×2, 1Tim 6:22 ×1 |
| `karoli_vers` üres, ÓSZ | 12: Zsolt 4 (21:23, 77:56, 103:30, 15:8 — LXX-számozás), Jób 3 (40:22, 38:41, 17:16), Péld 12:28, Préd 10:20, Jóel 3:24, Hós 13:16, Dán 3:98 |
| ÓSZ-sor a Zsoltárokban | 499 (a létező, de LXX-szerint eltolt vers nem mérhető ebből; nincs átkulcsolás, a brief szerint mérni, nem kitölteni) |
| jelöletlen igehely-folytatás (becslés: `</ref>` után `,<vers>` vagy `; f:v`) | ≈ 228 — nincs a táblában |

A Siralmak: a könyvtábla `JSir`-t ad, a `Karoli_1908.tsv` `Sir`-t; a `karoli_vers` a Károli-kulcsot írja (a
`bdb_vers_jelentes.py` `KAROLI_KONYV` mintája). Enélkül 18 JSir-hivatkozás néma nem-találat lett volna (az első mérésben az volt).

### G1941: a 10 motívumhely (az `elofordulasok.tsv` szerint) a Thayerben

| Motívumhely | `bcv`-vel idézi? | szakasz | jelentéspont |
|---|---|---|---|
| 1Pét 1:17 | igen | 3 | `-/1/-` (to put a name upon, to surname) |
| ApCsel 2:21 | igen | 7 | `-/5/-` (Hebraistically … to invoke) |
| ApCsel 9:14 | igen | 7 | `-/5/-` |
| Róm 10:12 | igen | 7 | `-/5/-` |
| Róm 10:13 | igen | 7 | `-/5/-` |
| 1Kor 1:2 | igen | 7 | `-/5/-` |
| 2Tim 2:22 | igen | 7 | `-/5/-` |
| ApCsel 9:21 | nem — a forrásban jelöletlen („Act 9:14,21”) | (7) | — |
| ApCsel 22:16 | nem — a forrásban jelöletlen („; 22:16>”) | (7) | — |
| Róm 10:14 | nem idézi | — | — |

A motívum magja tehát a Thayer 5. jelentéspontja (segítségül hívni az Úr nevét); az 1Pét 1:17 az 1. pont („atyának nevezni”).
A két jelöletlen ApCsel-hely a szövegben az 5. pont alatt áll, de a tábla nem tölti ki (CLAUDE.md 3. szabály).

## M3-előfeltétel 1 — tiltott fordulatok és a `15_tiltott` kapu (DT331 (b), 2026-10-25)

- `adat/tiltott_fordulatok.tsv` (új, kézi, SEMA 2.36): 2 tétel, a DT241 / `F121_GLOSSZA_FORDITAS_BRIEF.md` 2a/2 első elemei
  („melléknéven nevezni”, „melléknevet adni”; helyette „más néven (is) nevezni”). Más tételt a végrehajtó nem vett fel (tartalom:
  a #121 és a javítások).
- `eszkozok/forditas_kapuk.py`: `tiltott_betolt`, `ellenoriz_tiltott`, a `15_tiltott` a `GATOLO`-ban, a `kapuk_futtat` végén
  (a szakaszos futtatás is átveszi). A `14` foglalt (`14_szakasz`), ezért `15`.
- `eszkozok/teszt_forditas_kapuk.py`: `Tiltott` osztály, 7 teszt; a modul 88 tesztje zöld. `teszt_bdb_zaras.py` 21 teszt zöld.
- Mérés a `forditasok.tsv`-n *(proveniencia: `scope=adat/forditasok.tsv (forditas_hu) | forras=tiltott_meres.py (eseti, a repón kívül) @aee1355 | ts=2026-10-25`)*:
  találat 4 hely, mind a G1941 két sorában (Thayer `teljes` `kezi`: 3; TBESG `1` `kezi`: 1) — egyezik a F121 2b/4 mérésével;
  a „melléknév” szóalakot tartalmazó 98 sor egyike sem találat. A két G1941-sor javítása a #121 0. tétele (nem ez a feladat);
  az M3 Thayer-sora a kapun megy át.
- **Mellékhatás (az `ir` bővült: `adat/bdb_szakasz_hu.tsv`):** a `bdb_jelolt/hu_illeszt.py` a kimenet `# forras:` fejlécsorába a
  `forditas_kapuk.py` hash-ét írja, ezért a kapuváltozás után az `--ellenoriz` eltért. Újragenerálva (`--ts 2026-10-18`, a fájl saját
  napja): **csak a fejlécsor hash-e változott** (`8ce0a55f14eb` → az új), adatsor nem.
- Megfigyelés (nem e feladat változása): a `bdb_jelolt/teszt_bont.py` két determinizmus-tesztje (`bont.py --ellenoriz`,
  `forras_javit.py --ellenoriz`) e környezetben a változtatás **előtt** is eltér (tiszta `aee1355` állapoton mérve) — a
  `bdb_szakaszok.tsv` / `bdb_forras_javitas.tsv` újragenerálása környezetfüggő; nem javítottam (nem e feladat fájljai).

## M3-előfeltétel 2 — a lánc: betöltő, szólista, sigla, adatblokk, parancssor (2026-10-25)

*(proveniencia: `scope=F132 M3-előfeltételek | forras=kódolvasás és próbafuttatás @a558dbb (eszkozok/thayer_jelolt/forditas.py elokeszit G1941, G4151 a scratchpadbe) | ts=2026-10-25`)*

| Fájl | Mit ad |
|---|---|
| `eszkozok/thayer_jelolt/thayer_bemenet.py` | a Thayer-betöltő (DT330 (1)): a #128 `bdb_jelolt/szakasz_bemenet.py` szótárfüggetlen függvényeit **importálja** (saját modulnéven, a #128 fájlja változatlan): `⟪n⟫`, `sz<n>`, SHA-1, `csoportok`, `strong_magyar`; a szakasz szövege `jel` + `szoveg`. `--ellenoriz`: 5 426 Strong, 17 093 szakasz, rendben; 10 Strong több csoportos (a G4151: 3 csoport, 6 920 / 7 584 / 9 261 karakter) |
| `eszkozok/thayer_jelolt/szolista.py` | az újrafuttatható M3 listája (DT332): ma **13 Strong, mind `forditando` / `nincs_szakaszos`** (= a brief 13 szava; 42 600 karakter), ebből 5-nek van régi `kezi` `teljes` sora (G0282, G1941, G1944, G4151, G5590: DT329 (ii)), 1 `reszleges` illesztésű (G4151: DT333) |
| `eszkozok/thayer_jelolt/sigla_gyujt.py`, `adat/thayer_sigla.tsv` (SEMA 2.37) | 254 gépi jelölt, 90 a gerincszavakban; besorolt 0 (**DT335**) |
| `eszkozok/thayer_jelolt/thayer_kapuk.py` | a közös kapusor (`kapuk_futtat_szakaszos`: 1–13., `14_szakasz`, `15_tiltott`) + `16_sigla` (besorolt sorra gátoló) |
| `eszkozok/thayer_jelolt/adatblokk.py` | csoportonként: 1. Károli-alakok (a párosítás le nem fedett ÚSZ-könyvei — Mt, Mk, Luk, Ján, ApCsel — explicit), 2. az idézett versek Károli-szövege (`thayer_vers_jelentes.tsv`; hiánynál `[nincs Károli-vers]`), 3. siglák (a terminológiai alak elsőbb), 4. nyelvközi híd (héber `ref0` → `Strong_szotar.tsv` pontos szótő → a meglévő magyar BDB-fordítás eleje); `reszleges` illesztésnél figyelmeztetés (DT333) |
| `eszkozok/thayer_jelolt/forditas.py` | az M3 parancsai: `lista`, `elokeszit`, `ellenoriz`, `rogzit` (munkatábla: `naplok/F132_THAYER_SZAKASZ_munka.tsv`), `beir` (DT329 (i)/(ii) szerint; minden más sor bájtra változatlan) — az `emeles.py` szakaszos ágának Thayer-párja, az `emeles.py` függvényeit importálva |
| `eszkozok/thayer_jelolt/teszt_lanc.py` | 18 teszt, zöld (betöltő, szólista ideiglenes táblákon, sigla-kapu, sigla-tábla kézi oszlopainak védelme, adatblokk, prompt, szakaszsorok, beírás ideiglenes másolaton: opus `teljes` → `elavult`; `kezi` `teljes` mellett csak `--kezi-marad`, csak hozzáfűzés) |

Próba (fordítás nélkül, a scratchpadbe): `elokeszit G1941` → 7 szakasz, 1 csoport, 37 helyőrző, prompt 51 313 bájt (benne az
adatblokk ≈ 13 KB: 41 idézett vers); `elokeszit G4151` → 17 szakasz, 3 csoport, 291 helyőrző, promptok 80–107 KB (az
idézett versek miatt). A forrást „fordításként” visszaadva az `ellenoriz` a várt módon bukik (5. terminológia: `cf.` → `vö.` stb.;
8. idézőjel), a `14_szakasz`, `15_tiltott` rendben, a `16_sigla` JELZES (31 besorolatlan sigla) — a lánc a kapukig végigfut.

Megfigyelés: a terminológiai szójegyzék 10 sigla-jelöltre már ad kötelező alakot (`cf.` → `vö.`, `Sept.` → `Septuaginta`, `i. e.`
→ `azaz`, `p.` → `o.`, `etc.` → `stb.`, `Plato` → `Platón`, `Xenophon` → `Xenophón`, `Herodotus`, `Aristotle`, `id.`); az adatblokk
ezt jelzi, a sigla-besorolásnak ehhez kell igazodnia (DT335).

## M3-előfeltétel 3 — a prompt

A `forditas/prompt_v5.md` változatlan (a #128 fájlja). A Thayer-prompt ugyanazokat a helyőrzőket kapja, az `{{ADATBLOKK}}` helyén a
Thayer-adatblokkal. A v5 szövege a határtoken-blokkban és az adatblokk-szabályban a BDB-t nevezi meg: **DT336** (🟡; javaslat:
új `prompt_v5_1.md` Thayer-kiegészítéssel).

## M3 indítása (⛔ itt állok meg; a fordítás nem fut ebben az Opus-menetben)

**Nyitott döntések az M3 előtt:** DT334 (az indítás módja), DT333 (a TSV szövegvesztése; a G4151-et érinti), DT335
(sigla-besorolás), DT336 (a prompt Thayer-ága). A DT334 opciói (`DONTESEK.md`):

1. **Külön M3-brief** (`F<nn>_THAYER_M3_BRIEF.md`, `modell: sonnet`, `fugg: [132]`, `/befogad`-dal) — *javaslat*: a CLAUDE.md
   modell-ellenőrzése változatlanul működik (a `vegrehajto-sonnet` a saját briefje `modell: sonnet` mezőjéhez mér); egy brief = egy
   modell; az M3 újrafuttatható (DT332), ezért saját feladat illik hozzá; a #132 az Mz-vel (SEMA, mérés, független ellenőrzés)
   az M3 előtt lezárható.
2. **Lépésszintű modell-mező** a #132 briefben (pl. `modell_m3: sonnet`) — a CLAUDE.md modell-ellenőrzésének, a `/kovetkezo`-nak és
   a `feladatok.py`-nak is tudnia kell róla: rendszerszabály-változás.
3. **A `modell` mező átváltása** `sonnet`-re az M3 előtt — egyszerű, de a futó feladat modellje menet közben változik, és az M0–M2
   Opus-commitjai a fejléc szerint már nem azonosíthatók.
4. Subagent nélküli Sonnet-session — a CLAUDE.md szerint ott is a brief `modell` mezője a mérce, ezért a (2) vagy a (3) nélkül nem
   működik.

**Az M3 Sonnet-menetének lépései (bármelyik opcióval, a modell-ellenőrzés után):**

```
python eszkozok/thayer_jelolt/forditas.py lista --ki <scratchpad>/m3_lista.tsv      # DT332: a futás listája, okkal
python eszkozok/thayer_jelolt/forditas.py elokeszit <STRONG> --mappa <scratchpad>/m3
#   a <STRONG>_c<i>_prompt.md fordítása (csoportonként), a helyőrzős vázlat: <scratchpad>/m3/<STRONG>_vazlat.txt
python eszkozok/thayer_jelolt/forditas.py ellenoriz <STRONG> --be <vázlat> --mappa <scratchpad>/m3 --ki <végleges>
python eszkozok/thayer_jelolt/forditas.py rogzit <STRONG> --be <végleges> --allapot sonnet --modell <a saját tényleges modellnév>
python eszkozok/thayer_jelolt/forditas.py beir <STRONG> --allapot sonnet --regi-elavult      # opus régi sor (DT329 (i))
python eszkozok/thayer_jelolt/forditas.py beir <STRONG> --allapot sonnet --kezi-marad        # kezi régi sor (DT329 (ii))
```

Kapubukásnál egy önújrapróba, utána `naplok/F132_THAYER_SZAKASZ_bukottak.tsv`; commit adagonként.

## Döntések (2026-10-25, második kör)

A felhasználó (chat, szó szerint): „mehet, g(1), i(2), j(3), k(2)”, erre a kérdésre: „Mehet így, g(1), i(2), j(3), k(2) és a két
eltérés elfogadva?”. Átvezetve (`DONTESEK.md`, 🟢; a brief 6. döntésnaplója):

- **DT334 (1):** külön M3-brief (`modell: sonnet`, `fugg: [132]`); a tervezet a `beerkezo/`-ban, a befogadás nem e menet dolga.
  Az M3 kikerül a #132 hatóköréből; a #132 az Mz-vel zárul.
- **DT333 (2):** javítótábla `adat/thayer_forras_javitas.tsv` (a DT228 mintája).
- **DT335 (3):** gépi sigla-javaslat a `thayer_sigla.tsv`-ben, javaslat-jelöléssel; a jóváhagyás a felhasználóé.
- **DT336 (2):** új `forditas/prompt_v5_1.md`, a v5 változatlan.

**Egyeztetett eltérések (a fenti válasz „a két eltérés elfogadva” része):**

1. Az `adat/thayer_vers_jelentes.tsv` kilencedik oszlopa, a `szakasz` (l. M2 „Sémaeltérés”) — elfogadva, a tábla és a SEMA 2.35 marad.
2. Az `adat/bdb_szakasz_hu.tsv` fejlécsorának hash-újragenerálása (l. M3-előfeltétel 1 „Mellékhatás”) — elfogadva, az `ir` bővülése marad.

## F132.11 — DT333 (2): a `Thayer_teljes.tsv` javítótáblája (2026-10-25)

*(proveniencia: `scope=konkordancia/lexikonok_nyers/Thayer.lexicon, konkordancia/Thayer_teljes.tsv | forras=eszkozok/thayer_jelolt/forras_javit.py --ts 2026-10-25, bont.py --ts 2026-10-25 (a fejlécsorok hash-eivel); i_meres.py, i_diff.py (eseti, a repón kívül) | ts=2026-10-25`)*

- **Új:** `eszkozok/thayer_jelolt/forras_javit.py` → `adat/thayer_forras_javitas.tsv` (generált, SEMA 2.38). Egy sor = egy lyuk; a
  beszúrt szöveg a lexikonbekezdés címkék nélküli szövegéből, soronként gépileg igazolva (egyetlen törlés egyetlen bekezdésben; a
  beszúrással a Strong illesztése `egyezik`; a javított sor szóközök nélkül = a lexikonbekezdés). Eredmény: **15 lyuk, mind `javitva`,
  2 715 karakter** (szóközök nélkül; az M1 száma), `jelolt_marad` 0. A G4151 6. sora: „1Co 14:15, 1Co 14:16.” (18).
- **A bontó** (`bont.py`) a táblát csak a határokhoz olvassa: a 15 Strong illesztése `reszleges` → **`javitassal`** (175 sor `illesztes`
  mezője; a `szoveg` mező **egyetlen sorban sem változott**, a difflib-vetítés határai pontosak voltak). A tábla nyers marad.
- **A nézet:** `thayer_bemenet.szakaszok` a `javitassal` sorba a `sor_poz` helyén beszúrja a `javitott_alak`-ot (az `elotte` mezővel
  igazolva). Ezt kapja a fordítás (a `forras_hash` is erről), az adatblokk (a „hiányt ne pótold” figyelmeztetés helyett tájékoztató
  sor) és a sigla-gyűjtés (`sigla_gyujt.py` a nézetre állt: 255 jelölt, ebből 91 a gerincszavakban; korábban 254 / 90).
- Mellékhatás: a `thayer_vers_jelentes.tsv` fejlécsora (a `bont.py` kód-hash-e) újragenerálva, adatsor nem változott.
- Tesztek: `teszt_bont.py` 23 (új `Javitas` osztály, 7 teszt), `teszt_lanc.py` 18, `teszt_vers_jelentes.py` 9 — zöld; `--ellenoriz`:
  `forras_javit.py`, `bont.py`, `sigla_gyujt.py`, `vers_jelentes.py` azonos; `thayer_bemenet.py --ellenoriz` RENDBEN.

## F132.12 — DT336 (2): `forditas/prompt_v5_1.md` (2026-10-25)

- **Új:** `forditas/prompt_v5_1.md` = a `prompt_v5.md` szó szerinti másolata (a v5 fejléce is, változatlanul) + egyetlen új blokk,
  „Kiegészítő szabály (v5.1) — Thayer-szócikk” (a v5 határtoken-blokkja után): (1) a határtoken-szabály 1–6. pontja a Thayerre;
  (2) a v4 általános szabályai és a v4.1 érvényesek, a v4 BDB-blokkja nem; (3) a v4.2 adatblokk-szabályából az 1–3. és 6. pont, a 4.
  (`[kihagyva …]`) és 5. (`[BDB: X]`) nem; a Thayer-blokk négy része (Károli-alakok a le nem fedett könyvekkel; idézett versek,
  `[nincs Károli-vers …]`; siglák a három jelöléssel, a terminológia elsőbb; nyelvközi híd, rangsor: terminológia > Károli > BDB >
  szótár, `[nincs Strong-egyezés]` esetén nincs kitalált megfelelő); (4) a javított forrásszöveg (DT333 (2)) teljes.
- A `prompt_v5.md` és a #128 fájljai változatlanok; a `thayer_jelolt/forditas.py` `PROMPT_UT`-ja a v5.1-re állt.
- Teszt: `teszt_lanc.py` `test_prompt_v5_1` (a v5.1 törzse a blokk nélkül bájtra = a v5; a prompt tartalmazza a blokkot, a
  jelölő fölötti rész nem kerül bele); a modul 19 tesztje zöld.

## F132.13 — DT335 (3): gépi sigla-javaslat jóváhagyásra (2026-10-25)

*(proveniencia: `scope=adat/thayer_sigla.tsv (tipus, jelentes, magyar_alak) | forras=manual — modell-javaslat (claude-opus-5-5), nem lekérdezés: a gerincszavak javított nézetének szövegkörnyezete (j_ktx.py, eseti, a repón kívül) és az adat/terminologia.tsv alapján | ts=2026-10-25`)*

- **A tábla** (`adat/thayer_sigla.tsv`): a gerincszavakban előforduló **91 jelölt mindegyike `allapot = javaslat`** (`tipus`,
  `jelentes`, `magyar_alak`); új kézi oszlop: `besorolas_proveniencia` (`forras=manual — modell-javaslat (claude-opus-5-5), nem
  lekérdezés …; jóváhagyásra vár`). A javaslat **nem jóváhagyás**: a 16. kapu és az adatblokk besorolatlannak veszi; a `besorolt` a
  felhasználó jóváhagyásával lesz (az M3 előfeltétele). A többi 164 jelölt `jelolt` maradt. Írás előtt összevetve: csak a 91 sor kézi
  oszlopai változtak; a `sigla_gyujt.py --ellenoriz` azonos (a kézi oszlopokat az eszköz nem írja át).
  *Pontosítás (F132.24, ELLENOR_F132 7. tétel): a mondat tartalmilag igaz, bájtszinten nem. Mért: `git diff --numstat e41710e~1
  e41710e -- adat/` → `thayer_sigla.tsv` 258/258 (a 2 megjegyzés-sor, a fejléc és mind a 255 adatsor): az új `besorolas_proveniencia`
  oszlop minden sorban (a 164 `jelolt` sorban üresen) és a fejlécben, a `# FÉLIG KÉZI` sor szövege és a `# forras:` sor kód-hash-e
  (`kód@67a23018df55` →); a régi oszlopok közül tartalmilag csak a 91 `jelolt` → `javaslat` sor kézi oszlopai változtak (`tipus` 91,
  `jelentes` 91, `allapot` 91, `magyar_alak` 84 — a 7 üres alak üres maradt), a számoszlopok és a többi 164 sor nem; `SEMA.md` 8/4.*
  *(proveniencia: `scope=adat/thayer_sigla.tsv @e41710e~1..e41710e | forras=git diff --numstat, git diff --word-diff=porcelain és
  eseti oszloponkénti összevető szkript (scratchpad, split('\t')) | ts=2026-10-25T12:14Z`)*
- **Elv:** a terminológiai kapus kulcs alakja kötelező (`cf.`, `Sept.`, `i. e.`, `p.`, `etc.`, `Plato`, `Xenophon`, `Herodotus`,
  `Aristotle` — teszt); a többi görög szerző a szójegyzék névalakjainak mintájára, a prompt v4 7. szabályával (Philón, Plutarkhosz,
  Josephus); az általános rövidítések a szójegyzék párjainak mintájára (`ibid.` → `uo.` az `id.` → `ua.` mellett; `viz.` → `ti.` az
  `sc.` → `ti.` mellett; `vol.` → `köt.` a `vol. ii` → `II. köt.` mellett); a kiadás-siglák, a grammatikák, a modern szerzők és a
  műcím-rövidítések (forráshivatkozás) `változatlan`; ahol egy alak több szerepben áll és egyiknek sincs egységes magyar alakja, a
  `magyar_alak` üres (a kapu nem ellenőrzi). *Az F132.21 óta (ELLENOR_F132 4. tétel) ez explicit érték: `nincs_egyseges`.*
- **Kapu** (`thayer_kapuk.py`): a `besorolt`, de üres `magyar_alak`-ú sor nem ellenőrzött és nem besorolatlan *(az F132.21 óta:
  `nincs_egyseges` = nem ellenőrzött; az üres = kitöltetlen, JELZES)*; a `javaslat`
  besorolatlan (JELZES, nem gátol). Tesztek (`teszt_lanc.py`, 22, zöld): a javaslat nem gátol; a proveniencia `manual`, modellnévvel; a
  gerinc minden jelöltje javaslat vagy besorolt; a terminológiai kulcsú sorok alakja a szójegyzéké (9).

### Jóváhagyási lista (91 sor; a teljes indoklás a tábla `jelentes` mezőjében)

**Magyar alakot kap (22):** cf. → vö. · Cf. → Vö. · i. e. → azaz · Sept. → Septuaginta · p. → o. · pp. → o. · etc. → stb. ·
ibid. → uo. · viz. → ti. · vol. → köt. · Plato → Platón · Xenophon → Xenophón · Herodotus → Hérodotosz · Aristotle → Arisztotelész ·
Philo → Philón · Plutarch → Plutarkhosz · Homer → Homérosz · Polybius → Polübiosz · Thucydides → Thuküdidész ·
**Macc. → Makk · Sir. → Sir · Wis. → Bölcs** (apokrif könyvek; a Károli-rövidítéslistában nincsenek — külön figyelmet kér).

**Nincs egységes alak, a kapu nem ellenőrzi (7):** `N.` / `O.` (az `N. T.` / `O. T.` része: folyó szövegben Újszövetség /
Ószövetség, műcímben változatlan) · `e.` / `g.` (az `e. g.` = pl. és az `i. e.` része; Stephanus-lapszakasz) · `i.` (az `i. e.` része;
kötetszám) · `ii.` (kötetszám; a szójegyzék `vol. ii` → `II. köt.`) · `al.` (`et al.` = és mások; igehely-sor után: és máshol).

**Változatlan (62):**
- kiadás-sigla (11): Rec. · R · G · L · T · Tr · WH · Tdf. · Lachmann · A. · V. (az `A. V.` / `R. V.` része) — *figyelem:* a `T` és a
  `G` a kapu szóhatáros keresésében az `N. T.`, illetve a `G. L. Hahn` alakban is találat, ezért ahol a csoport egyetlen `T`-je az
  `N. T.`-ben áll, a kapu bukhat; *javítva az F132.20-ban (ELLENOR_F132 3. tétel):* a kapu (`thayer_kapuk._re`) az egybetűs siglát
  (`R`, `G`, `L`, `T`, `V` …) a betű-pont(-szóköz)-betű-pont láncban (`N. T.`, `O. T.`, `A. V.`, `R. V.`, `G. L. Hahn`, `N.T.`) nem
  találja, a forrásban és a fordításban sem; teszt: `teszt_lanc.py` `test_kapu_egybetus_sigla_tobbtagu_rovidites`. Mért hatás a 13
  gerincszó szakaszain (a régi és az új minta szakaszonként, l. „Javítókör 1”, F132.20);
- kézirat-sigla (1): Vat.;
- grammatika (4): Winers Grammar · Winer's Grammar · Buttmann · B. (`B. §`, `B. D.`);
- modern szerző (6): Trench · Grimm · Meyer · Gesenius · Schmidt · Lob.;
- antik szerző (2): Josephus · Cass. (`Dio Cass.`);
- műcím-rövidítés (25): D. (`B. D.`) · mem. · Cor. (Római Kelemen, nem bibliai) · Theol. · legg. · diss. · Gram. · Lex. · Dict. ·
  Tim. (Platón) · Magn. · eth. · Ep. · Phaedr. · Bib. · Sacr. · mund. · opif. · div. · rer. · haer. · El. · anab. · Path. · educ.;
- rövidítés (1): iii. (kötetszám);
- nem sigla (12): b. · c. · d. · bb. (betűjel, Stephanus-lapszakasz) · h. · v. · j. (`v. h.`, `b. j.`) · u. · theol. (német műcím) ·
  St. · J. · Chr. (névelem).

## F132.14 — DT334 (1): az M3 brief-tervezete; az M3 kikerül a #132 hatóköréből (2026-10-25)

- **Tervezet:** `beerkezo/Fnn_THAYER_M3_BRIEF.md` (`modell: sonnet`, `fugg: [132]`, `munka: adat`, `allapot: nem_indult`, a
  `BRIEF_SABLON.md` szerint): az újrafuttatható M3 a DT329, d, h, i, j, k szerint; a parancssor a fenti „M3 indítása”
  szakaszból (a prompt már a v5.1); 1. lépése ⛔ előfeltétel: a sigla-javaslatok felhasználói jóváhagyása (`javaslat` → `besorolt`,
  a jóváhagyás proveniencia-sorával). A befogadás nem e menet dolga (`/befogad`, a felhasználó jóváhagyásával).
- **A #132 briefje:** az `ad` mező, a 3. hatókör (benne / nincs benne), az M3 szakasz eleje („Kikerült e feladat hatóköréből”), az Mz
  és az 5. elfogadási feltétel 3. pontja a DT334 (1) szerint; az `ir` mezőben a tervezet útvonala.
- A `thayer_jelolt/forditas.py` docstringje a promptot még v5-nek írta: javítva (`prompt_v5_1.md`, a kód az F132.12 óta azt használta).

## Mz — zárás (2026-10-25; az M3 a DT334 (1) szerint külön feladat)

*(proveniencia: `scope=adat/thayer_*.tsv, eszkozok/thayer_jelolt/ | forras=a generátorok --ellenoriz módja; forditas.py lista / elokeszit (a scratchpadbe, fordítás nélkül); a tesztek @2fe54b8 | ts=2026-10-25`)*

| Mért | Érték |
|---|---|
| `thayer_szakaszok.tsv` | 5 426 Strong, 17 093 sor; illesztés `egyezik` 5 411, `javitassal` 15, `reszleges` 0, `sikertelen` 0; fejes szócikk 1 687 |
| `thayer_forras_javitas.tsv` | 15 lyuk, mind `javitva`, 2 715 karakter (szóközök nélkül) |
| `thayer_vers_jelentes.tsv` | 63 953 sor = a forrás `bcv`-száma (ÚSZ 58 266, ÓSZ 5 687); üres `karoli_vers`: ÚSZ 28, ÓSZ 12 (M2) |
| `thayer_sigla.tsv` | 255 jelölt, 91 a gerincszavakban; `javaslat` 91 (magyar alak 22, `változatlan` 62, üres 7), `besorolt` 0 |
| `tiltott_fordulatok.tsv` | 2 tétel, kapu `15_tiltott` |
| M3-lista (`forditas.py lista`, DT332) | 13 Strong, mind `forditando` / `nincs_szakaszos`; ebből 1 `javitassal` (G4151, 3 csoport), a többi `egyezik` (1 csoport) |
| M3-lánc próbája (fordítás nélkül) | `elokeszit G1941`: 7 szakasz, 1 csoport, 37 helyőrző; `elokeszit G4151`: 17 szakasz, 3 csoport, 291 helyőrző, a prompt a v5.1 blokkjával és a javítás tájékoztató sorával |
| G1941 motívumhelyei | l. M2: 7 / 10 `bcv`-vel idézve (1 az 1. pont alatt, 6 az 5. pont alatt), 2 jelöletlen, 1 nem idézett |

**Determinizmus (`--ellenoriz`):** `bont.py`, `forras_javit.py`, `vers_jelentes.py`, `sigla_gyujt.py` azonos; `thayer_bemenet.py`
RENDBEN; `bdb_jelolt/hu_illeszt.py --ts 2026-10-18` azonos (a `--ts` nélküli hívás a mai napot írná a fejlécbe, ezért tér el — nem
adateltérés).

**Tesztek:** `thayer_jelolt/teszt_bont.py` 23, `teszt_lanc.py` 22, `teszt_vers_jelentes.py` 9, `teszt_forditas_kapuk.py` 88,
`teszt_bdb_zaras.py` 21, `bdb_jelolt/teszt_szakasz_bemenet.py` 25, `teszt_feladatok.py` 115 — mind zöld. `python eszkozok/ellenoriz.py`:
SÉRTÉS 0 (RENDBEN 14, KÉZI 2, JELENTÉS 3). `python eszkozok/feladatok.py ellenoriz`: 160 brief, 0 hiba, 1 figyelmeztetés (az
`F131_SZOTARI_GERINC_BRIEF.md` fázis-függése a #132-re; a main-en is fennáll, nem e feladat változása).

**Nyitva a felhasználónak:** (1) a 91 sigla-javaslat jóváhagyása (lista: F132.13; különösen a három apokrif-rövidítés és a 7 üres
alak) — az M3 előfeltétele; (2) az M3 tervezetének befogadása (`beerkezo/Fnn_THAYER_M3_BRIEF.md`, `/befogad`, a #132 merge-e után).
A #132 lezárása a független ellenőrzés után (orkesztrátor).

## Javítókör 1 (`/elteres 132`, ELLENOR_F132; 2026-10-25)

A felhasználó jóváhagyott besorolása: `DONTESEK.md` DT337 (a 2. tétel döntése és az 1., 3.–7. tétel javaslatának jóváhagyása).
Végrehajtó: `claude-opus-5-5`. Tételenként külön commit (F132.18–F132.24).

- **F132.18 (1. tétel, CI E5):** a brief M3-címsorának cseréje alatt látható megjegyzés; a `TÖRLÉS-SZÁNDÉKOS:` jelölés a commit-üzenet
  sor elején áll, mert az E5 csak azt olvassa (`eszkozok/ellenorzes/szabalyok.py` `SZANDEKOS_JELOLES_MINTA`; a CI a PR összes
  commit-üzenetét `--commit-uzenet-fajl`-ként adja).
- **F132.19 (2. tétel, DT337 (a)):** `adat/elofordulasok.tsv` KIRALY-001 / Zsid 7:1-28 `strong`: `G5010+G0813+G0282` →
  `G5010+G0540+G0282`; a sor `proveniencia` mezője `scope=manual`, a lekérdezésre hivatkozva. Írás előtt összevetve: a 262 sorból
  csak ez az egy változott (bájtra). A lekérdezések saját proveniencia-sora:

  ```
  # scan G0813 — 0 igehely, 0 szó-előfordulás
  proveniencia: scope=range:Zsid 7:1-28 | forras=TAGNT_kivonat.tsv | strong=G0813 | n=0 | ts=2026-10-25T12:04Z
  # scan G0540 — 1 igehely, 1 szó-előfordulás
  Zsid 7:3
  proveniencia: scope=range:Zsid 7:1-28 | forras=TAGNT_kivonat.tsv | strong=G0540 | n=1 | ts=2026-10-25T12:04Z
  # scan G0813 — 1 igehely, 1 szó-előfordulás
  1Thessz 5:14
  proveniencia: scope=TAGNT-teljes | forras=TAGNT_kivonat.tsv | strong=G0813 | n=1 | ts=2026-10-25T12:04Z
  ```

  Következmények (újragenerálva, `--ts 2026-10-25`): `adat/thayer_sigla.tsv` — a `# forras:` sor `elofordulasok.tsv` hash-e és 10 sor
  `gerinc_elofordulas` mezője; a kézi oszlopok változatlanok (a gerincszavakban előforduló jelölt 91 → 90: az `educ.` gerinc-előfordulása
  0 lett, `javaslat` marad). A szólista (`szolista.py`, csak stdout) ma: 13 Strong, mind `forditando` / `nincs_szakaszos`, a G0813 helyett
  G0540 (2 szakasz, 214 karakter). A `lexikon/KIRALY-001_TUDOMANYOS.md` és `_TORZSCIKK.md` generált nézet a régi tokent mutatja (G0813
  szócikk-alszakasz); a #132 `ir`-én kívül esik, újragenerálása nem e kör része (az E28 hatóköre csak az ISTENTISZT-001); nyitott tétele: `NYITOTT_FELADATOK.md` N-F132a (F132.27).
- **F132.20 (3. tétel, 16. kapu, egybetűs sigla):** `thayer_kapuk._re` — egybetűs alaknál a betű-pont(-szóköz)-betű-pont lánc tagja
  nem találat (előtte és utána is; a szomszéd betű önálló kell legyen, a `Gen. T` `T`-je találat). Az `adatblokk.py` ugyanezt a
  függvényt használja (3. rész, siglák), így egységes. Új teszt (`teszt_lanc.py`, 23, zöld): 7 negatív és 6 pozitív minta, a kapu
  RENDBEN az `N. T.` / `R. V.` / `G. L. Hahn` esetén, SERTES, ha az önálló `T` hiányzik és a fordításban csak az `N. T.` áll.
  Mért hatás (szakaszonként: a régi minta talál, az új nem, mert a betű csak láncban áll — besorolt sigla esetén ezek lettek volna
  hamis SERTES-ek): `R` 11 → 8 (G5590:5, G5356:3, G5351:2), `G` 9 → 8 (G0012:2), `L` 11 → 11, `T` 13 → 10 (G1941:5, G4151:10,
  G5356:3).

  *(proveniencia: `scope=a 13 gerincszó (szolista.gerinc_strongok) javított nézetű szakaszai | forras=eseti mérőszkript (scratchpad, a repón kívül): a régi `(?<!\w)X(?!\w)` és az új `thayer_kapuk._re` @4afe60c0 + a javítás | ts=2026-10-25`)*
- **F132.21 (4. tétel, 16. kapu, üres `magyar_alak`):** explicit érték `nincs_egyseges` (`thayer_kapuk.NINCS_EGYSEGES`). A kapu: a
  `besorolt` + `nincs_egyseges` nem ellenőrzött; a `besorolt` + üres `magyar_alak` kitöltetlen besorolás → JELZES (a besorolatlan
  sorral azonos, nem gátoló szint: a hiba a táblában van, nem a fordításban; a SERTES elsőbb), a forrásalakok felsorolásával. Az
  adatblokk a `nincs_egyseges` sort „[nincs egységes magyar alak: a szövegkörnyezet szerint — <jelentes>]” alakban adja, nem
  `→ nincs_egyseges`-ként. `adat/thayer_sigla.tsv`: a 7 `javaslat` sor (`N.`, `e.`, `ii.`, `i.`, `O.`, `g.`, `al.`) `magyar_alak`
  mezője üres → `nincs_egyseges`, a `besorolas_proveniencia` kiegészítve (a javaslat tartalma nem változott). A `magyar_alak` kézi
  oszlop, a `sigla_gyujt.py` nem állítja elő (a javaslat az F132.13-ban kézzel került be), ezért a módosítás szkripttel, összevetéssel
  történt: 7 sor, soronként csak a `magyar_alak` és a `besorolas_proveniencia` mező; a `sigla_gyujt.py --ellenoriz` azonos (a kézi
  oszlopot az eszköz átmásolja). SEMA 2.37 frissítve. Tesztek (`teszt_lanc.py`, 25, zöld): a besorolt üres alak JELZES, a SERTES
  elsőbb; a `nincs_egyseges` nem ellenőrzött; a táblában `javaslat` / `besorolt` sor `magyar_alak`-ja nem üres; az adatblokk jelölése.
- **F132.22 (5. tétel, `ir` maradvány):** a brief `ir` mezőjéből kikerült az `adat/forditasok.tsv`, a
  `naplok/F132_THAYER_SZAKASZ_munka.tsv` és a `naplok/F132_THAYER_SZAKASZ_bukottak.tsv` (DT334 (1): az M3 külön briefbe került; a
  #132 egyiket sem írja). A tervezet (`beerkezo/Fnn_THAYER_M3_BRIEF.md`) `ir`-je mindhármat tartalmazza; nem változott.
- **F132.23 (6. tétel, `datasetek.tsv`):** az `adat/datasetek.tsv`-be 8 sor került: `Thayer_szakaszok`
  (`adat/thayer_szakaszok.tsv`) és `Thayer_vers_jelentes` (`adat/thayer_vers_jelentes.tsv`), mindkettő a négy study-típusra
  (`bovitett`, `tematikus`, `melyelemzes`, `lexikon_oldal`), `ajanlott`, `korlatos` — a BDB-pár (`BDB_szakaszok`,
  `BDB_vers_jelentes`) mintájára, amely ugyanígy négy-négy sorral szerepel. A leírás a SEMA 2.34/2.35-ből és az M1/M2 méréseiből
  (korlát: a 15 javított Strong, a csak aranymintás szakaszolás; a jelöletlen igehely-folytatás, az üres `karoli_vers`, az ÓSZ-számozás).
  Csak hozzáfűzés: a meglévő sorok bájtra változatlanok. A brief `ir` mezője bővült az `adat/datasetek.tsv`-vel. `python
  eszkozok/ellenoriz.py`: SÉRTÉS 0 (RENDBEN 14, KÉZI 2, JELENTÉS 3).
- **F132.24 (7. tétel):** a napló F132.13-mondata („csak a 91 sor kézi oszlopai változtak”) alatt pontosítás a mért
  állapottal (numstat 258/258, új oszlop minden sorban + fejléc + kód-hash; tartalmilag csak a 91 sor kézi oszlopai), proveniencia-sorral.

## F142.1 — DT335 (3): a sigla-javaslat jóváhagyásának átvezetése (2026-10-26)

*(proveniencia: `scope=adat/thayer_sigla.tsv (allapot, besorolas_proveniencia, magyar_alak) | forras=manual — felhasználói jóváhagyás (chat, 2026-10-26, az orkesztrátoron át: „1, mehet”); átvezetés: Sonnet 5.5 (claude-sonnet-5-5), eseti szkript (scratchpad, split('\t')) | ts=2026-10-26`)*

- **Átvezetve:** a 91 `javaslat` sor mind `allapot = besorolt`; a `besorolas_proveniencia` a meglévő javaslat-proveniencia tartalmát
  megtartja, és kiegészül: ` | jóváhagyás: forras=manual — felhasználói jóváhagyás (chat, 2026-10-26); allapot javaslat → besorolt`.
- **Egy eltérés a javaslattól:** a `Sir.` sor `magyar_alak`-ja `Sir` helyett `Sirák` (a proveniencia-sorban: `magyar_alak
  felhasználói módosítással: Sir → Sirák`). Ok: a repó eszközei (`eszkozok/lekerdez.py`, `teszt_lekerdez_sir.py`,
  `eszkozok/nave_bontas.py:33`) a „Sir” alakot a Jeremiás siralmai (JSir) aliasaként kezelik, így a fordításban a „Sir 24” csendben
  Siralmaknak olvasódna.
- **Összevetés írás előtt (szkript):** csak a 91 sor `allapot` és `besorolas_proveniencia` mezője, plusz a `Sir.` sor `magyar_alak`-ja
  változott; a fejléc-/megjegyzéssorok és minden más mező bájtra azonos (a szkript `assert`-tel megállt volna eltérésnél).
- **Ellenőrzés:** `sigla_gyujt.py --ts 2026-10-25 --ellenoriz` → `ELTÉR`, de ugyanúgy a **kiinduló állapoton** is (a `git stash`-sel
  mért HEAD is `ELTÉR`): az újragenerált fájl és a tábla egyetlen sorban tér el, a `# forras:` fejléc bemenet-hash-eiben
  (`thayer_szakaszok@50e03d…` stb. a tábla szerint, `@d71764…` stb. a mostani bemenetekből; az F132 lezárása óta a bemenetek más
  hash-t adnak ebben a környezetben). Az adatsorok (a 91 + 164) az újragenerálttal **azonosak**. A fejlécsort nem írtam át (gépi
  sor, nem tartozik a 91 sorhoz); a kiinduló `ELTÉR` pre-existens, az F142.1 nem okozta.
  A `teszt_bont.py` két hibája (`test_ellenoriz`, `test_forras_javit_ellenoriz`) és a `teszt_lanc.py`
  `test_tabla_determinisztikus_es_kezi_vedett` hibája ugyanezen a kiinduló eltérésen áll (mérve a kiinduló állapoton is).
- **Új teszt-hiba az átvezetés következményeként:** `teszt_lanc.py::Adatblokk.test_g1941_reszei` a 216. sorban a `cf.` sor
  `[besorolatlan a sigla-táblában; …]` jelölését várja (azaz a `javaslat` állapotot rögzíti); a jóváhagyás után az adatblokk helyesen
  `` `cf.` → `vö.` ``-t ad. A #132 teszt módosítása e feladat hatókörén kívül (brief 2.), ezért nem módosítottam; tétel: `DT350`
  (`DONTESEK.md`), a fordítás nem függ tőle.
- **Kapuk a `Sirák` alakkal:** `teszt_forditas_kapuk.py` (90) zöld, `teszt_vers_jelentes.py` (9) zöld; a `Sirák` miatt nincs bukás.

## F142.2 — az M3 futási listája és az első megállás (2026-10-26)

*(proveniencia: `scope=adat/elofordulasok.tsv@f8284bffc6a8 + adat/forditasok.tsv@07f20f3d57c1 + adat/thayer_szakaszok.tsv@d71764889b02 | forras=python eszkozok/thayer_jelolt/forditas.py lista (szolista.py --ts 2026-10-26) | ts=2026-10-26`)*

- **Lista (DT332 (1)):** 13 Strong, mind `forditando` (ok: `nincs_szakaszos`), kihagyott 0: G0012 (2 szakasz), G0086 (4), G0282 (7; régi
  `kezi` `teljes` sor), G0540 (2), G1311 (6), G1941 (7; `kezi`), G1944 (2; `kezi`), G2671 (3), G4151 (17 szakasz, 3 csoport,
  `javitassal`; `kezi`), G5010 (6), G5351 (2), G5356 (3), G5590 (10; `kezi`). Az illesztés G4151 kivételével `egyezik`.
- **G0012, első menet (modell: claude-sonnet-5-5):** az `elokeszit` rendben (2 szakasz, 1 csoport, 14 helyőrző). Az első vázlat
  kapubukása három javítható ok volt (`8_idezojel`: a forrás `'the deep'` aposztróf-idézetét „…”-ra cseréltem; `16_sigla`: `ibid.`
  → `uo.`), a javított vázlatnál **két hiba marad**, amely nem a fordításon múlik:
  1. `11_konyvek` SÉRTÉS (`a forditasbol hianyzik: Sir×2`): a kapu a `normalizal.py` `APOKRIF_ALIAS`-át (`Sir. → Sir`, `Ecclus → Sir`)
     használja, és a fordításban a `Sir` könyvnevet várja; a felhasználó által jóváhagyott `Sirák` (F142.1) nem felel meg neki. Az
     érintett Strongok: G0012 (2 hely), G4151 (1 hely). A felhasználó utasítása szerint a `Sirák`-kal bukó kapunál megállás.
  2. `16_sigla` SÉRTÉS (`Philo -> Philón hiányzik`): a G0012 (és a G0282, G4151) forrásában a `Philo` a „Philo's Lehre von der
     Weltschöpfung” német műcímben áll (G0012 `⟪2⟫`); a prompt 5. szabálya a műcímet változatlanul hagyja, a 16. kapu viszont
     minden `Philo`-hoz `Philón`-t vár.
  Rögzítés nem történt; a `forditasok.tsv` és a munkatábla nem változott.

## F142.3–F142.14 — az M3 fordítása a 10 független Strongra; Mz-mérés (2026-10-26)

*(proveniencia: `scope=G0086, G0540, G1311, G1941, G1944, G2671, G5010, G5351, G5356, G5590 | forras=python eszkozok/thayer_jelolt/forditas.py lista/elokeszit/ellenoriz/rogzit/beir (Sonnet 5.5, claude-sonnet-5-5); eszkozok/ellenoriz.py; eszkozok/feladatok.py ellenoriz; a tesztek; eseti mérőszkript (scratchpad, split('\t')) | ts=2026-10-26`)*

- **F142.3 (DT351 (A)):** a `Sir.` sigla `magyar_alak`-ja vissza `Sir` (a 11. kapuval és a `normalizal.APOKRIF_ALIAS`-szal egyező);
  a `besorolas_proveniencia` kiegészítve (`magyar_alak felhasználói döntéssel visszaállítva: Sirák → Sir (DT351 (A), chat,
  2026-10-26)`); írás előtt összevetve: csak ez a sor, csak ez a két mező. N-F142a helyőrző a `NYITOTT_FELADATOK.md`-ben.
  (B): a G0012, G0282, G4151 vár (a 16. kapu műcím-kérdése külön feladat).
- **Eredmény (Strongonként; szakasz / csoport / kapu / önújrapróba):**

| Strong | szakasz | csoport | eredmény | önújrapróba | megjegyzés |
|---|---|---|---|---|---|
| G0086 | 4 | 1 | kész (F142.4) | 1 (a helyőrző-sorszámozás hibája, `1_gorog_heber`; `16_sigla`: `vol.`, `pp.`) | régi `teljes` sor `elavult` |
| G0540 | 2 | 1 | kész (F142.5) | 0 | régi `teljes` sor `elavult` |
| G1941 | 7 | 1 | kész (F142.7) | 0 | régi `kezi` `teljes` sor érvényes (`--kezi-marad`) |
| G2671 | 3 | 1 | kész (F142.9) | 0 | régi `teljes` sor `elavult` |
| G5356 | 3 | 1 | kész (F142.12) | 1 (`16_sigla`: ragozott szerzőnevek) | régi `teljes` sor `elavult` |
| G1311 | 6 | 1 | **bukott** (F142.6) | 1 | `5_terminologia` + `16_sigla` (Homérosz) |
| G1944 | 2 | 1 | **bukott** (F142.8) | 2 | `11_konyvek` + `16_sigla` (Makk) |
| G5010 | 6 | 1 | **bukott** (F142.10) | 1 | `11_konyvek` + `16_sigla` (Makk) |
| G5351 | 2 | 1 | **bukott** (F142.11) | 1 | `5_terminologia` + `16_sigla` (Homérosz) |
| G5590 | 10 | 1 | **bukott** (F142.13) | 0 (vázlat nélkül) | a fenti két ok a forrásból következik |

- **A bukások oka (a lánc hibája, nem a fordításé; `bukottak.tsv`, DT352):** (i) a 5. kapu a `from Homer down` fordítását
  `Homérosztól kezdve` alakban köti, a 16. kapu (`_re`, `(?![\w])`) a `Homer` siglához a ragozatlan `Homérosz`-t vár — egyetlen
  `Homer`-előfordulásnál egyszerre nem teljesíthető; (ii) a `Macc.` -> `Makk` sigla a 16. kapunál önálló szó, a 11. kapu viszont
  `4Makk` / `2Makk` alakot köt, amelyben a `Makk` a számjegy mögött áll. A 16. kapu ragozást nem tűrő illesztése a fordítható
  Strongokban is kerülőt kívánt (a szerzőnév mint önálló szó: `Platón, Arisztotelész, Plutarkhosz`; `Aeschylus és Hérodotosz óta`).
- **Mz — G1941 motívumhelyei (10 hely, ISTENTISZT-001; `adat/elofordulasok.tsv` × `adat/thayer_vers_jelentes.tsv` × a magyar
  szakaszok):** 1Kor 1:2, 2Tim 2:22, ApCsel 9:14, ApCsel 2:21, Róm 10:13, Róm 10:12 -> sz7 (a hivatkozás a magyar sz7-ben áll);
  1Pét 1:17 -> sz3 (a hivatkozás a magyar sz3-ban áll); Róm 10:14 (a Thayer nem idézi), ApCsel 9:21 és ApCsel 22:16 (a Thayerben
  jelöletlen folytatás: `Act 9:14,21; 22:16>`) -> a `thayer_vers_jelentes.tsv`-ben nincs sor, a magyar szöveg a sz7-ben közli az
  utóbbi kettőt. Az `elofordulasok.tsv` `jelentes_szam` mezője mind a 10 sorban `2` (a régi, jelentésszámos hozzárendelés; e feladat
  nem módosítja).
- **`python eszkozok/ellenoriz.py`: SÉRTÉS 1 (13. szabály, 19 sor) — a #132/#128 eszközének hézaga, nem a fordítás hibája.** A 13.
  szabály (`_szakasz_szoveg`, `eszkozok/ellenoriz.py`) csak a `BDB` `sz<n>` sorokhoz keres forrásszöveget; a Thayer szakaszsorokat
  `nincs hozzá forrásszöveg` miatt sértésnek veszi: mind a 19 új sor (4+2+7+3+3) és csak azok. A kiinduló állapot SÉRTÉS 0 volt.
  Tétel: DT353 (az eszköz nem módosult).
- **`python eszkozok/feladatok.py ellenoriz`:** 164 brief, 0 hiba, 0 figyelmeztetés.
- **Tesztek:** `teszt_forditas_kapuk.py` (90) és `teszt_vers_jelentes.py` (9) zöld. A `teszt_bont.py` 2 hibája és a
  `teszt_lanc.py::Sigla.test_tabla_determinisztikus_es_kezi_vedett` a kiinduló (main-en is fennálló) `# forras:` hash-eltérésen áll.
  A `teszt_lanc.py` két új hibája a valódi futás állapotfüggése (DT350): `Adatblokk.test_g1941_reszei` (a jóváhagyott `cf.`) és
  `Lanc.test_beir_kezi_marad` (a teszt a G1941 szakaszsorainak hiányát várja a valódi `forditasok.tsv`-ben; a G1941 sorai most már
  bent vannak, így a „csak hozzáfűzés” összevetés elbukik).

## F142 folytatás (2026-10-27, `claude-sonnet-5-5`, ág `ccr-676ffb53-9qo1to`)

- **F142.20–F142.28:** a lista újrafuttatva (DT332 (1); `lista`, proveniencia: `scope=… | forras=thayer_jelolt/szolista.py | ts=2026-10-27`):
  8 `forditando` (G0012, G0282, G1311, G1944, G4151, G5010, G5351, G5590), 5 `kihagyva/kesz`. A fordítás a #145 kapujavításai után fut.
- **Eredmény (szakasz / csoport / kapu / önújrapróba / régi sor):** G0012 2/1/átment/1 (`1_gorog_heber`, `8_idezojel`: kézi javítás a vázlatban)/elavult;
  G0282 7/1/átment/1 (`5_terminologia` Heb.→héb., `8_idezojel`)/kezi marad; G1311 6/1/átment/0/elavult; G1944 2/1/átment/1 (`16_sigla` ragozás)/kezi marad;
  G5010 6/1/átment/0/elavult; G5351 2/1/átment/1 (`etc.`→`stb.` idézett angol szövegrészben)/elavult; G5590 10/1/átment/1 (`8_idezojel`: magyar „…”)/kezi marad;
  G4151 17/3/átment/2 (`9_tagolas`: jelölő sorrend; kézi hibajavítás)/kezi marad. Bukott: 0 (a `bukottak.tsv` 5 korábbi sora feloldva, a fájl üres, fejléccel).
- **Megjegyzés (nyitott szövegminőség):** a kapu a `Heb.` -> `héb.` kulcsot a G0282 „Bleek on Heb.” helyén is előírja, noha ott a Zsidókhoz írt levél a jelentés;
  a G5351 angol `R. V. waxeth corrupt etc.` idézetében az `etc.` a 16. kapu miatt `stb.`-re változott. Mindkettő a kapu szóalak-érzékenysége; felhasználói felülvizsgálat tárgya (`kezi` jóváhagyás).
- **Mz:** `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 165 brief, 0 hiba; `teszt_forditas_kapuk.py` (90) és `teszt_vers_jelentes.py` (9) zöld;
  `teszt_lanc.py` 1 és `teszt_bont.py` 2 hiba a kiinduló (a változások nélküli ágon is fennálló) `# forras:` hash-eltérés.
