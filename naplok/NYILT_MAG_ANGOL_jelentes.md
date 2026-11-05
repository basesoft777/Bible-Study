# A nyílt mag angol rétege — jelentés (F170, FELADATOK #170)

*2026-11-05 · session: claude-opus-5-5 (a brief `modell: opus`, egyezik) · fordítás: két előfizetéses Sonnet-alügynök,
saját kiírt modellnevük `claude-sonnet-5-5` · ág: `claude/gifted-bardeen-54a98d` · döntések: DT-F170a (a); a glossza-oszlop
és a fordítás „mehet”-je az orkesztrátortól, a felhasználó felhatalmazásával (2026-11-05)*

A számok a futások kimenetéből: `python eszkozok/nyilt_mag_export.py`, `python eszkozok/nyilt_mag_kapu.py`,
`python eszkozok/teszt_nyilt_mag.py`, `python eszkozok/nyilt_mag_angol.py allapot`, `python naplok/F170_szuroproba.py`.
A felmérés: `naplok/NYILT_MAG_ANGOL_felmeres.md`.

## 1. Mi került a csomagba

| Elem | Hol | Szám |
|---|---|---:|
| OSIS-igehelykulcs (`<oszlop>_osis`) | 6 tábla, minden igehely-oszlop mellett | 11 oszlop, 7 234 cella; leképezhetetlen: 0 |
| zárt értékek angol címkéje (`<oszlop>_en`) | 8 tábla | 34 oszlop, 4 157 cella; a kódkönyvben 186 értéksor `cimke_en`-nel |
| szabad szöveg gépi angol párja (`<oszlop>_en`) + `forditas_modja` | `motivumok`, `elofordulasok`, `kizarasok`, `beepitesi_dontesek`, `dontesnaplo` | 12 oszlop; 869 cella, 541 egyedi szöveg; fordított 869, hiányzó 0, elavult 0 |
| angol szófogódzó (`strong_glossza_en`) | `elofordulasok.tsv` | 247 sorból 247 (minden Strong-számos sor) |
| kódkönyv | `adat/nyilt_kodkonyv.tsv` → `kodkonyv.tsv`, `KODKONYV.md` | 351 sor (213 → 351: +11 OSIS, +108 címke/`_en`, +18 angol réteg, +1 a TBESH/TBESG új leltár-szerepe) |

**OSIS.** Lánc: magyar rövidítés → STEPBible (`Konyv_normalizalo_tabla.tsv`) → OSIS 2.1.1 könyvkód (rögzített 66 sor).
A fejezet- és versszám a Károli-számozás; a kódkönyv minden `_osis` sora kimondja (hu/en), hogy ahol ez eltér a KJV-
vagy a STEPBible-számozástól, a kulcs a Károli-verset jelöli. A forrásbeli `Sir` (TAHOT-alak, 23 csoport-tag) a
csomagban `JSir`; minden más ismeretlen könyvnévre az export megáll.

**Zárt címkék (DT-F170a (a)).** A zárt oszlopok listája egy helyen áll (`nyilt_mag_export.ZART`); új zárt oszlop: a
`kizaras_oka`, a `forrasok_es_licencek.ok`, a `forras_megnevezes` (3 tábla) és a `kapcsolatok.lekerdezes_tipusa`. A
145 különböző címkét a szerkesztő írta (`naplok/F170_cimkek.tsv`), nem gépi soronkénti fordítás.

**Szabad szöveg.** Tár: `adat/nyilt_angol.tsv` (kulcs: tábla + oszlop + sorkulcs, forrás-hash, modell, dátum). A
`forditas_modja` soronként: `gépi fordítás (claude-sonnet-5-5)` — 805 sor; a három javított cella sorában
`… claude-sonnet-5-5; javítás: claude-opus-5-5` — 3 sor; üres (a sorban nincs szabad szöveg) — 139 sor.

A tár (`adat/nyilt_angol.tsv`, 0 → 869 sor, új tábla) tábla–oszlop szerinti bontása: `beepitesi_dontesek.indoklas`
257, `kizarasok.indoklas` 418, `kizarasok.korabbi_minosites` 17, `elofordulasok.funkcio` 116, `dontesnaplo.kerdes` 8,
`dontesnaplo.dontes` 8, `motivumok` `cim`/`rovid_cimke`/`tema`/`negativ_kriterium`/`folerendelt_fogalom` 5 × 9.
A motívum-meghatározások (a brief 7. lépése, F170.4) ugyanabban a fordítási menetben készültek, ezért az F170.3
commitjában vannak, nem külön commitban.

**Szófogódzó.** A `jelentes_en` marad (szótári kivonat: BDB 131 / Thayer 20 / TBESG 6 sor `szotar` szerint; 55
kitöltött); mellette a `strong_glossza_en` a TBESH/TBESG Gloss oszlopából (a fő bejegyzések; több fő bejegyzés ` / `,
több Strong-szám ` + `). A kódkönyv kimondja a kettő különbségét; az attribúció („Data created by www.STEPBible.org
based on work at Tyndale House Cambridge, CC BY 4.0”) a kódkönyvben és az `OLVASSEL.md`/`README.md` új „Angol réteg /
English layer” szakaszában áll; a TBESH és a TBESG a `forrasok_es_licencek.tsv`-ben `forrás (az angol szófogódzó
oszlopé)` szerepű (új zárt érték; a sorok forrásmegjelölésében a glossza nem áll, ezért nem a régi „forrás” érték).

## 2. Kapu és tesztek

`python eszkozok/nyilt_mag_kapu.py`: **0 BUKÁS, 17 FIGYELMEZTETÉS** (16 `KH_NEV`: a „KJV” szó a TSK-versszámozás
javításának megjegyzésében, magyarul és angolul — nem adat; 1 `ANGOL_SOR`: magyar cella idézett TAHOT-jelöléssel; a
#162 óta ismert jelleg). Új ellenőrzések: `OSIS` (a), `CIMKE` (b), `FORDITAS` (c)–(e), `GLOSSZA` (f; a glossza
újraszámolva egyezik a TBESH/TBESG-vel, tehát nem KJV-Strong eredetű). A meglévő `LICENC`-ellenőrzés az új oszlopokra
is fut (minden cellát vizsgál): kizárt dataset neve 0 helyen. Az angol szövegben a „manual” közszó nem belső jel (a
BELSO-minta `_en`/`_osis` oszlopon ezt nem méri).

`python eszkozok/teszt_nyilt_mag.py`: **59 teszt, OK** (új: 7 OSIS, 5 CIMKE, 7 FORDITAS/GLOSSZA).

E35: a commitolt `nyilt_mag/` az újragenerált exporttal bájtazonos (a kapu `BAJTAZONOS` ellenőrzése 0 BUKÁS).

**CI-szabályok (helyben, `eszkozok/ellenorzes/futtat.py` a diffre):** 0 HIBA. Két szabályhoz kellett illeszteni: az
**E9** a „sense” szót jelezte a kétnyelvű `KODKONYV.md`-ben (a kódkönyv angol szövegében „meaning” lett); az **E10** a
fordítás-tár 3 sorát (a Károli-idézet „lelki test” mögött a szó szerinti ["spiritual body"]). Az E10 a tárban most
csak az `angol` mezőt nézi, a magyar idézetek nélkül (DT-F170c, 🟡; teszt). Mivel a PR a nyílt mag kapuját és a
`szabalyok.py`-t is módosítja, a címe „[ELLENŐRZŐ]” előtagú (E16). A független ellenőr jelentése és a kezelés:
`naplok/ELLENOR_F170.md`.

## 3. Szúrópróba (30 cella, rögzített mag: 170; `naplok/F170_szuroproba.py`)

Egyedi szövegenként 30 véletlen cella, magyar–angol összevetés ebben a (claude-opus-5-5) sessionben.

| Eredmény | Db | Megjegyzés |
|---|---:|---|
| jó | 28 | hű, a szerkezet (zárójel, „ — ”) megmarad; a Károli-idézet magyarul marad, mögötte szögletes zárójelben szó szerinti angol fordítás; héber/görög, átírás, Strong-szám változatlan; igehely angol könyvnévvel, Károli-számmal |
| javítandó | 2 | mindkettő javítva, **csak a fordításon**; a független ellenőr saját mintájából egy harmadik is (l. lent) |

A két javítás:
1. `dontesnaplo.tsv` `kerdes` (NYD-008): a magyar forrásban egy szó hiányzik („a útjára”); a fordító „route”-tal
   pótolta. Javítva: „be put on their way” (a hiányt nem pótolja). A forráshiba: N-F170e.
2. `kizarasok.tsv` `indoklas` (ANTROP-001, 2Kor 1:22-23): „léleknek zálogát” → „the pledge of the Spirit”: a nagybetű
   értelmez (a magyar kisbetűs). Javítva: „the pledge of the spirit”.
3. (a független ellenőr 17 soros mintájából) `beepitesi_dontesek.tsv` `indoklas` (ANTROP-001, 1Kor 15:45): a magyar
   idézet a fordításban megváltozott (`"élő lelkével"` → `"élő lelke"`). Javítva: `"élő lelkével" ["with living soul"]`.

Gépi átnézés az egész táron (`adat/nyilt_angol.tsv`, 869 cella): „product” 0; magyar könyvrövidítés az angol szövegben
0; archaikus angol bibliai alak (thee/thou/hath/saith) 0; „KJV” 8 (mind a forrás versszámozási megjegyzésének
fordítása). Ingadozás (nem hiba): „Surplus of the Septuagint” a címke „a Septuagint plus” alakja mellett; a forrás magyar
átírása (pszükhé, Abüsszosz, Nefilim) helyenként megmaradt, máshol angolos (psyche) — a szabály a megtartást kérte.

## 4. Az MI-nyilatkozatba szánt sor (nem írtam be; az orkesztrátor kérése szerint itt adom)

- **hu:** A nyílt adatmag angol párhuzamos mezői (`…_en`: indoklás, funkció-címke, a motívum meghatározása, a
  döntésnapló) gépi fordítások (claude-sonnet-5-5); a fordítás módját a sorok `forditas_modja` oszlopa jelöli, a zárt
  értékek angol címkéi és a kódkönyv szerkesztett szövegek.
- **en:** The English parallel fields of the open data core (`…_en`: rationale, function label, motif definition,
  decision log) are machine translations (claude-sonnet-5-5); the `forditas_modja` column of each row marks how the
  translation was made, while the English labels of closed values and the codebook are edited texts.

## 5. Ami nem e feladaté — nyitott tételek (`nyitott/uj/gifted-bardeen-54a98d.md`)

- **N-F170a** (befogadáskor nyitva): a `kozlemeny/data_paper/kezirat_en.md` „Hungarian column names and values”
  korlát-mondata e merge után pontatlan — a #171 vagy a data paper következő átírása frissíti. Ehhez a feladathoz a
  kéziratokhoz nem nyúltam.
- **N-F170c:** KJV-/STEPBible-versszámozásra átkulcsolt OSIS-kulcs (a versmegfeleltetés licence miatt nem most).
- **N-F170d:** a `datum` oszlopok vegyes alakja (ISO 8601-re egységesítés).
- **N-F170e:** két forrásszöveg-hiba a döntésnaplóban (hiányzó szó; a `hatar-ellenor` belső név szivárgása, amelyet a
  BELSO-minta nem fog meg).
- **N-F170f:** adatváltozás után az angol pár elavulhat; a CI ezt nem méri (az E35 csak bájtazonosságot), a pótlás
  menete: `kigyujt` → Sonnet-alügynök → `betolt`.

## 6. Elfogadási feltételek

| Feltétel | Állapot |
|---|---|
| minden igehelyes sorban érvényes OSIS-kulcs; 0 leképezhetetlen | teljesül (7 234 cella; kapu `OSIS` 0) |
| minden zárt értéknek angol címkéje | teljesül (kapu `CIMKE` 0) |
| minden szabad szövegű mezőnek angol párja és gépi-fordítás jelölése (modellnév a futásból) | teljesül (869/869; `forditas_modja`) |
| a forrás-hash egyezik; a kapu bukik, ha a magyar forrás változott | teljesül (elavult 0; teszt: `test_elavult_forditas`) |
| 0 KJV-Strong-eredetű érték; a szójelentés-fogódzó STEPBible-glossza, attribúcióval | teljesül (kapu `GLOSSZA`, `LICENC` 0) |
| `nyilt_mag_kapu.py` 0 BUKÁS, `teszt_nyilt_mag.py` zöld, E35 zöld | teljesül helyben; a CI a PR-en |
| kódkönyv: minden új oszlop és érték hu/en; az MI-nyilatkozat mondata | kódkönyv teljesül; a mondat a 4. pontban (DT-F170b: az orkesztrátor döntése, nem a nyilatkozatban) |
| a szúrópróba eredménye a jelentésben | teljesül (3. pont: 30-ból 28 jó, 2 javítva; + 1 javítás az ellenőr mintájából) |
