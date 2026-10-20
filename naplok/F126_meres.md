# F126 — mérési napló (ISTENTISZT001_PROZA, 2. és 3. lépés)

*FELADATOK #126 · `F126_ISTENTISZT001_PROZA_BRIEF.md` 3. szakasz 2–3. lépés · 2026-10-20 · modell: claude-opus-5-5*

A felmérés (`naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md`) adatállításai itt **kiindulópontok, nem források**. Minden alábbi érték a feladat saját lekérdezéséből jön; a felmérés proveniencia-sora sehol nem forrás. Ahol a saját mérés eltér, a saját mérés érvényes.

## Módszer és eszközök

| Eszköz | Mit mér | Proveniencia |
|---|---|---|
| `lekerdez.py lxx-hid <igehely> --naplo F126 --lepes adhoc` (23 futás: a 22 ószövetségi előfordulás és a Zsolt 99:6) | az LXX-vers szóalakjai Stronggal | soronként a `naplok/F126_lekerdezesek.tsv`-ben, pl. `scope=range:Zsolt 79:6 \| forras=LXX_OS/psalms-lxx.tsv+TAGNT_kivonat.tsv \| n=19 \| ts=2026-10-20T10:07Z \| csatorna=cli` |
| `lekerdez.py karoli <igehely> …` (26 futás) | Károli-szöveg és Károli-KH | `scope=range:<igehely> \| forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv \| ts=2026-10-20T10:08Z \| csatorna=cli` |
| `lekerdez.py kollokacio H7121 <X> …` (9 futás: H6030, H0784, H4422, H3045, H3034, H4196, H3605, H1471, H8034) | a gerinc-ige és a kísérő szó együttes versei a teljes ÓSZ-ben | pl. `scope=TAHOT-teljes+TAGNT-teljes \| forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv \| strong=H7121+H6030 \| n=43 \| ts=2026-10-20T10:08Z \| csatorna=cli` |
| `lekerdez.py scan G1941 …` | a G1941 teljes ÚSZ-képe | `scope=TAGNT-teljes \| forras=TAGNT_kivonat.tsv \| strong=G1941 \| n=31 \| ts=2026-10-20T10:08Z \| csatorna=cli` |
| `naplok/F126_meres.py` (fájlba írt szkript, `split('\t')`, kódlap-őr) | a 32 előfordulás tokenjei (TAHOT/TAGNT), Károli-szöveg, BSB angol szó, `kapcsolatok.tsv`, `lxx_dontesek.tsv`, a tartalmi szavak metszete (`grammatikai_strongok.tsv` és H9xxx nélkül) | `scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) \| forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv+Karoli_1908.tsv+BSB_Strongs.tsv+kapcsolatok.tsv+lxx_dontesek.tsv+grammatikai_strongok.tsv (naplok/F126_meres.py, split('\t')) \| ts=2026-10-20T10:11Z` |
| `naplok/F126_lxx_osszesit.py` | a 23 `lxx-hid` kimenet összesítése (G1941/G2564/G0994/G4506/G4982) + `lxx_dontesek.tsv` | a 23 `lxx-hid` sor (fent) + `adat/lxx_dontesek.tsv` (LD001–LD004) |
| `naplok/F126_lefedetlen.py` | a H7121+H8034 kollokáció versei, amelyek sem előfordulások, sem ISTENTISZT-001-jelöltek | `scope=TAHOT-teljes+TAGNT-teljes \| forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv \| strong=H7121+H8034 \| n=196 \| ts=2026-10-20T10:13Z \| csatorna=cli` + `adat/elofordulasok.tsv`, `adat/jeloltek.tsv` |

A 32 igehely mindegyikéhez van token (TAHOT 22, TAGNT 10); tokennélküli igehely nincs.

## Összefüggésenként

Jelölés: **=** egyezik · **≠** eltér (miben) · **+** a saját mérés többet mutat.

| Össz. | A felmérés állítása | A saját mérés | Proveniencia | Ítélet |
|---|---|---|---|---|
| 1 | H6030 (felel) a 32-ből háromban: 1Kir 18:24, 18:26, Zak 13:9 | ugyanez a három. Versen belül: 1Kir 18:24-ben kétszer (Isten „tűz által felel”; „felelvén az egész sokaság” — a második a népre vonatkozik); 1Kir 18:26-ban kétszer (Károli: „hallgass meg minket” és „sem felelet”); Zak 13:9-ben egyszer („én felelni fogok”) | `F126_meres.py`; TAHOT-tokenek | = (+ a 18:24 második H6030-a nem Isten válasza) |
| 1 | H0784 (tűz) háromban: 1Kir 18:24, 18:25, Zak 13:9 | ugyanez | `F126_meres.py` | = |
| 1 | Károli: 18:26 „nem jött szó, sem felelet”, Zak 13:9 „én felelni fogok néki” | szó szerint megerősítve | `karoli 1Kir 18:26`, `karoli Zak 13:9` | = |
| 1 | — | **LXX:** Isten válaszára mindhárom helyen a G1873 ἐπακούω áll (1Kir 18:24 ἐπακούσῃ, 18:26 ἐπάκουσον ×2, Zak 13:9 ἐπακούσομαι); a nép válasza (18:24) más ige, G0611 ἀπεκρίθησαν | `lxx-hid 1Kir 18:24`, `18:26`, `Zak 13:9` | + |
| 1 | — | **LXX 1Kir 18:24:** a Baál-hívók felszólítása G0994 βοᾶτε, Illés saját hívása G1941 ἐπικαλέσομαι; a 18:25–26-ban a Baál-hívókra is G1941 áll | `lxx-hid 1Kir 18:24/25/26` | + |
| 1 | — | H1168 (Baál) a 18:25-ben és a 18:26-ban (×2) áll, a 18:24-ben nem (ott „a ti istenteknek nevét”) | `F126_meres.py` | + |
| 2 | H4422 (megmenekül) Zsolt 116:4 és Jóel 2:32; G4982 ApCsel 2:21, Róm 10:13 | ugyanez (a 32 közül pontosan ezek) | `F126_meres.py` | = |
| 2 | „négy helyen a hívást közvetlenül a szabadulás követi” | **LXX:** a Jóel 3:5 (LXX) G4982 σωθήσεται — ezt idézi az ApCsel 2:21 és a Róm 10:13 —, a Zsolt 116:4 LXX-e (114:4) viszont G4506 ῥῦσαι. A héber szó (H4422) a Zsolt 116:4-et a Jóel 2:32-vel, a görög (G4982) a Jóelt az ÚSZ-idézetekkel köti; a Zsolt 116:4 és az ÚSZ-helyek között közös szó nincs | `lxx-hid Zsolt 116:4`, `lxx-hid Jóel 2:32` | ≠ (a „lánc” nem egyetlen szón fut; a próza ezt kimondja) |
| — | Zsolt 116:13: egyik összefüggés sem ad új anyagot | a vers tartalmi szavai: H3068, H3444, H3563, H5375, H7121, H8034. A H3444 (Károli: „szabadulásért”), H3563 („pohár”), H5375 („felemel”) a 32 közül csak itt áll; a többi három a gerinc (H7121, H8034) és az Úr neve (H3068). A Jóel 2:32 „szabadulás” szava más héber szó (H6413) | `F126_meres.py` | = (megerősítve: nincs közös kísérő szó) |
| 6 | H3045 (ismer) öt helyen: 1Krón 16:8, Zsolt 105:1, Ézs 12:4, Zsolt 79:6, Jer 10:25 | ugyanez | `F126_meres.py` | = |
| 6 | H1471 (pogányok/népek) csak a két utolsóban | H1471 csak a Zsolt 79:6-ban és a Jer 10:25-ben; az első háromban a „nép” H5971 (עַם) — ez a Sof 3:9-ben is áll (a 1Kir 18:24-ben és a Zak 13:9-ben más értelemben: „sokaság”, „Népem”). A Zsolt 79:6 párja H4467 („országok”), a Jer 10:25-é H4940 („nemzetségek”) | `F126_meres.py` | + (a „népek” két különböző szó) |
| 6 | „a három első helyen megismertetni kell Isten tetteit, a két utolsóban vád” | Károli: H3045 = „hirdessétek” (1Krón 16:8, Zsolt 105:1, Ézs 12:4), „nem ismernek” (Zsolt 79:6, Jer 10:25). Az igetörzset a repó adata itt nem adja; a megkülönböztetés a Károli-fordításon mérhető | `karoli` ×5; `F126_meres.py` | = (a Károli-fordítás szintjén) |
| 6 | „a Sof 3:9 mindkettőt feloldja” | a Sof 3:9-ben H5971 + a formula áll, H3045 nincs | `F126_meres.py`, `karoli Sof 3:9` | ≠ (a „feloldás” értelmezés; a szóadat csak a népek és a hívás együttállását mutatja) |
| 7 | H3034 (hálát ad) pontosan három helyen | ugyanez: 1Krón 16:8, Zsolt 105:1, Ézs 12:4. Károli mindháromban mást ír: „Dícsérjétek”, „Magasztaljátok”, „Adjatok hálát” | `F126_meres.py`, `karoli` ×3 | = |
| 7 | tartalmi szavak: 1Krón 16:8 ↔ Zsolt 105:1 4/4; Ézs 12:4 mindkettővel 4/8 | a gerinccel és H3068-cal együtt: 7/7, illetve 7/11; a gerinc (H7121, H8034) és H3068 nélkül: 4/4 (H3034, H3045, H5949, H5971), illetve 4/8 (az Ézs 12:4 többlete: H0559, H2142, H3117, H7682) | `F126_meres.py` | = (módszerkülönbség: a felmérés a gerincet és a H3068-at kihagyta) |
| 7 | Ézs 12:4: LXX βοάω, Károli „magasztal” | LXX: G0994 βοᾶτε (LD003); Károli-szó (`elofordulasok.tsv`): „magasztaljátok az Ő nevét” | `lxx-hid Ézs 12:4`; `adat/lxx_dontesek.tsv` LD003 | = |
| 8 | H4196 (oltár) négy helyen: 1Móz 12:8, 13:4, 26:25, 1Kir 18:26 | ugyanez | `F126_meres.py` | = |
| 8 | „az, amely körül sántikáltak Baál papjai” | Károli 18:26: „ott sántikáltak az oltár körül, a melyet készítettek”; a megszólított név a 18:25–26-ban H1168 (Baál) | `karoli 1Kir 18:26`; `F126_meres.py` | = |
| 9 | H3605 (mind) a Jóel 2:32-ben és a Sof 3:9-ben a hívókra vonatkozik | H3605 a 32-ből négyben: Jóel 2:32, Sof 3:9 (a hívókra, Károli: „mindaz, a ki”, „mind”), 1Kir 18:24 („az egész sokaság”), 2Móz 33:19 (nem a hívókra) | `F126_meres.py`, `karoli` | = (+ két további, nem a hívókra vonatkozó előfordulás) |
| 9 | G3956 hat ÚSZ-helyen: ApCsel 2:21, 9:14, 9:21, Róm 10:12, 10:13, 1Kor 1:2 | ugyanez a hat. **De:** az ApCsel 9:21-ben a πάντες a hallgatókra vonatkozik (Károli: „Álmélkodnak vala pedig mindnyájan, a kik hallák”), a hívókra nem; a hívók ott „a kik ezt a nevet hívják segítségül” (G3778 τοῦτο), kvantor nélkül. A hívókra vonatkozó πᾶς öt helyen áll: ApCsel 2:21 πᾶς, 9:14 πάντας, Róm 10:12 πάντας, 10:13 πᾶς, 1Kor 1:2 πᾶσιν (és παντὶ τόπῳ, Károli: „bármely helyen”) | `F126_meres.py` (G3956-alakok), `karoli ApCsel 9:21` | ≠ (a 9. összefüggés az ApCsel 9:21-et nem fedi le) |
| 9 | Pálnál kifejezetten zsidóra és görögre (Róm 10:12) | G2453 és G1672 a 32 közül csak a Róm 10:12-ben | `F126_meres.py` | = |
| 10 | 2Kir 5:11 funkciója „ismétlődés, kívülálló szemszögéből”; Naámán azt várta, hogy a próféta segítségül hívja az Úr nevét | `elofordulasok.tsv` funkció: „🔁 ismétlődés, kívülálló szemszögéből”; Károli: „Íme én azt gondoltam, hogy kijő hozzám, és előállván, segítségül hívja az Úrnak, az ő Istenének nevét …”; a vers maga mondja a következményt: „megharaguvék Naámán és elment” | `F126_meres.py`, `karoli 2Kir 5:11` | = |
| 11 | 2Móz 33:19/34:5: BDB 3., LXX καλέω, BSB „proclaim”, Károli „kiált” | BDB 3 (`elofordulasok.tsv`, `jelentes_szam`); LXX G2564 καλέσω / ἐκάλεσεν (LD001, LD002, `lxx-hid`); BSB H7121: „and I will proclaim”, „and proclaimed”; Károli-szó: „kiáltom”, „kiáltá” | `F126_meres.py`; `lxx-hid 2Móz 33:19/34:5` | = |
| 11 | Ézs 12:4: LXX βοάω, BSB „proclaim”, Károli „magasztal”, a BDB viszont 2.c | ugyanez (BDB 2.c, G0994 βοᾶτε, BSB „proclaim”, Károli „magasztaljátok”) | `F126_meres.py`; `lxx-hid Ézs 12:4` | = |
| 11 | — | a többi 19 ószövetségi helyen a BSB H7121-fordítása mindenütt a „call” valamely alakja; a Károli „kiált” csak a két B-helyen, a „magasztal” csak az Ézs 12:4-ben áll | `F126_meres.py` | + |
| 11 | „négy független forrás” | a négy forrás egybeesése mérve; **függetlenségüket** (pl. a BSB fordítóinak szótárhasználatát) a repó adata nem méri | — | ≠ (a „független” jelző nem igazolt; a próza „egybeesést” mond) |
| 11 | — | a G0994 βοάω nem csak az Ézs 12:4 LXX-ében áll: az 1Kir 18:24-ben is (a Baál-hívók felszólítása); a vers mégis egyező, mert Illés hívására G1941 áll | `lxx-hid 1Kir 18:24` | + |
| 12 | Róm 10:14 a 10:13 közvetlen folytatása (`kapcsolatok.tsv`: Párhuzam, magas) | `Róm 10:13 → Róm 10:14 \| Párhuzam \| magas`; továbbá öt közepes Párhuzam a Róm 10:14-ből (1Kor 1:2, 2Tim 2:22, 1Pét 1:17, ApCsel 9:14, ApCsel 22:16) | `F126_meres.py` (`kapcsolatok.tsv`) | = |
| 12 | — | a versben: G1941 ἐπικαλέσωνται, G4100 ×2 (ἐπίστευσαν, πιστεύσωσιν), G0191 ×2 (ἤκουσαν, ἀκούσωσιν), G2784 κηρύσσοντος; Károli: „Mimódon hívják azért segítségül azt, a kiben nem hisznek? Mimódon hisznek pedig abban, a ki felől nem hallottak? Mimódon hallanának pedig prédikáló nélkül?” | `F126_meres.py`, `karoli Róm 10:14` | + |

## 3. lépés — két célzott ellenőrzés

### N-F55d: „22 ószövetségi igehely közül 18”

| Igehely | LXX-vers | G1941 az LXX-versben | Megjegyzés |
|---|---|---|---|
| 1Móz 4:26; 12:8; 13:4; 21:33; 26:25 | Genesis, azonos | igen (×5) | |
| 2Móz 33:19 | Exodus 33:19 | **nem** — G2564 καλέσω | LD001 |
| 2Móz 34:5 | Exodus 34:5 | **nem** — G2564 ἐκάλεσεν | LD002 |
| 1Kir 18:24; 18:25; 18:26 | 1 Kings, azonos | igen (×3) | a 18:24-ben G0994 βοᾶτε is |
| 2Kir 5:11 | 2 Kings 5:11 | igen | |
| 1Krón 16:8 | 1 Chronicles 16:8 | igen | |
| **Zsolt 79:6** | Psalms (LXX) 78:6 | **igen** — ἐπεκαλέσαντο | az N-F55d kérdéses helye |
| Zsolt 105:1 | Psalms (LXX) 104:1 | igen | |
| Zsolt 116:4 | Psalms (LXX) 114:4 | igen | |
| Zsolt 116:13 | Psalms (LXX) 115:4 | igen | |
| Zsolt 116:17 | Psalms (LXX) 115:8 | **nem** — a tagmondat hiányzik (LXX-minusz) | LD004 |
| Ézs 12:4 | Isaiah 12:4 | **nem** — G0994 βοᾶτε | LD003 |
| Jer 10:25 | Jeremiah (LXX) 10:25 | igen | |
| Jóel 2:32 | Joel 3:5 | igen | |
| Sof 3:9 | Zephaniah 3:9 | igen | |
| Zak 13:9 | Zechariah 13:9 | igen | |
| *Zsolt 99:6 (külön sor, nem előfordulás)* | *Psalms (LXX) 98:6* | *igen — ἐπικαλουμένοις, ἐπεκαλοῦντο* | *a 22-be nem számít; l. lent, N-F126a* |

**Eredmény:** 22 hely, ebből 18-ban áll G1941; a négy kivétel pontosan a kézi forrásban megnevezett négy (καλέω ×2, βοάω, LXX-minusz), és mind a négynek van `lxx_dontesek.tsv`-sora (LD001–LD004). A Zsolt 79:6 a mai `LXX_OS`-en G1941-et ad, tehát a 18 között van; a régi kivonat hiánya (a #42 eltéréslistája) a mai számot nem érinti. **A „22 ószövetségi igehely közül 18” állítás megerősítve; javítás nem kell.** Javaslat: az N-F55d lezárása. *(proveniencia: a 23 `lxx-hid` sor a `naplok/F126_lekerdezesek.tsv`-ben, ts=2026-10-20T10:07Z–10:08Z, összesítve: `naplok/F126_lxx_osszesit.py`)*

### Róm 10:14: a TR/Byz eltérés

A `konkordancia/TAGNT_kivonat.tsv` Róm 10:14-ében 18 token áll. Három szóalak `Kritikai kiadás` mezője `NA28+NA27+Tyn+SBL+WH+Treg` (a TR és a Byz nélkül): **G1941 ἐπικαλέσωνται** (a motívum kulcsszava), G4100 πιστεύσωσιν, G0191 ἀκούσωσιν; a többi 15 token mind a nyolc kiadásban áll. A TR/Byz alakja a kivonatban nem szerepel, ezért **a repó adatából nem állapítható meg, mi az eltérés**. Az eltérés tehát a motívum szavát érinti; a próza csak ezt a mért tényt mondhatja ki, szövegkritikai következtetés nélkül. Ez az N61 (`NYITOTT_FELADATOK.md`) mérésével azonos; az N61 nyitva marad (a TR/Byz alak forrásból való megállapítása nem e feladat dolga). *(proveniencia: `naplok/F126_meres.py`, ts=2026-10-20T10:11Z; a brief e tételt „N-F126c”-ként említi — a main-en a végleges száma N61)*

## Mellékleletek (nem próza; N-tétel vagy kérdés)

1. **N-F126a (javaslat) — két A-mintájú, lefedetlen H7121+H8034 vers.** A H7121+H8034 kollokáció 196 verséből 162 sem előfordulás, sem ISTENTISZT-001-jelölt (túlnyomórészt névadás). Közülük kettőben a Károli is „segítségül hív”-ot ír, és a szerkezet a motívum A-mintája: **Zsolt 99:6** („Sámuel az ő nevét segítségül hívókkal egybe … és meghallgatá őket”; TAHOT: קֹרְאֵי שְׁמוֹ, H7121+H8034, a versben H6030 is) és **Ézs 64:6** (Károli-számozás; „S nem volt, a ki segítségül hívta volna nevedet”, tagadó forma). Egyik sincs az `elofordulasok.tsv`-ben, sem a `jeloltek.tsv`-ben. A harmadik „segítségül”-találat (Bír 15:19) helynév, nem formula. Teendő (nem e feladaté): a két vers jelöltként a `jeloltek.tsv`-be, döntéssel (2. szabály); a próza addig nem szól róluk. *(proveniencia: `scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H7121+H8034 | n=196 | ts=2026-10-20T10:13Z | csatorna=cli` + `naplok/F126_lefedetlen.py`)*
2. **A felmérés számlálásának korlátja.** A felmérés az ApCsel 9:21-et és a Róm 10:14-et „egyszer sem megnevezett” helynek számolta; a lexikonoldal kézi prózája rövid alakban mindkettőt említi („ApCsel 9:14, 21” a Kivonatban és a Thayer-bekezdésben; „Róm 10:13-14” a Remez-ívben). A felmérés maga jelzi ezt a korlátot (tartományos említés). Értelmezést egyik hely sem kap ma; a feladat hatóköre ettől nem változik.
3. **ApCsel 9:21 és a 9. összefüggés:** l. fent (a πάντες a hallgatókra vonatkozik). A szövegjavaslat a 9:21-hez nem a 9. összefüggést használja.

## Összegzés a szövegjavaslathoz

- Megerősítve: 1., 2. (szavanként), 6. (a Károli-fordítás szintjén), 7., 8., 10., 11. (egybeesésként), 12.
- Pontosítva: 2. (a héber és a görög lánc más-más szón fut), 6. (a „népek” két szó), 9. (a 9:21 kiesik), 11. (függetlenség nem igazolt).
- Új mért tények: az LXX ἐπακούω a három „felel”-helyen; az 1Kir 18:24 βοάω/ἐπικαλέομαι-kettőssége.
- Zsolt 116:13: nincs közös kísérő szó → „nincs új anyag” megerősítve.
- N-F55d: megerősítve (18/22). Róm 10:14: az N61 mérése megerősítve.
- Seól (A4): a mérés a Zsolt 116:3-at nem érintette.
