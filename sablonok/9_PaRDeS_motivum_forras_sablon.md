# 9. PaRDeS motívum-forrás sablon (`motivumok/[ID].md`)

**Állapot: v2 (F178, 2026-11-08): a HAMART-001 mint arany — a lezárás hét szabálya (4. pont).** Előző: v1 (a #123 DT585 tétele, 2026-11-03). A v1 a v0.5 és az ALVIL-001 új cikkének öt tanulsága mint sablonszabály (4. pont, „Az új cikk öt szabálya”); a menetszabályok a `MUNKAMENET.md` „A lezárás menete motívumonként” szakaszában állnak. A #12-höz igazítás kérdése tárgytalan (a #12 2026-11-02-án lezárult, a TEREMT-002 a #123-é). Az első motívum, amely a v1-re íródik: ANTROP-001.

*v2 — 2026.11.08 (F178.2–F178.3, a felhasználó jóváhagyásával, 2026-11-08: a 4. pontban az öt szabály után „A HAMART-001 mint arany: a lezárás hét szabálya” — U2/U3 két kézben, határ-frissesség, a Kivonat fordulópontja, szerkezeti indok, kerek 1/a, Nave, U3-prompt.)*

*v1 — 2026.11.03 (DT585, az orkesztrátor döntése a felhasználó felhatalmazásával: »az orkesztrátor vegye magához a döntéseket és hozza is meg« (2026-11-03); az ALVIL-001 új cikkének (PR #604, #606) tanulságai: a 4. pontban, a teljesség-mérés után „Az új cikk öt szabálya” — saját elutasítási okok, lexémánként egy blokk-sor, a negatív kritérium ÚSZ-mércéje (DT563), a Septuaginta-többlet, az idézet jelölése. Szabály a v0.5-höz képest csak ez; a 9. pont záró mondata a véglegesítéshez igazítva.)*

*v0.5 — 2026.11.02 (F123.3, a felhasználó 2026-11-02-i döntései, DT546, DT548: a hátralévő motívumok új cikkként készülnek. A 4. pontban, a Kivonat határ-elemei után három új bekezdés: „Az 1/a igehelyenkénti prózája — kötelező forma” (a `kapcsolodas` kerek mondat, a `funkcio` „címke — magyarázat”, minta: ISTENTISZT-001, 1Móz 4:26), „A próza nem hivatkozik a régi tanulmány pontszámaira”, „Teljesség-mérés — három háló”; a 8. pontban a gépi kapuk (24., 25. szabály, olvasói kapu). Változatlanul tervezet.)*

*v0.4 — 2026.11.02 (a lexikon ág 1. lépése, az ISTENTISZT-001 1. kiadásának tanulsága: a 4. pont után „A Kivonat két kötelező határ-eleme” — a negatív kritérium szó szerint ellenőrizhető, kivétel név szerint; a fölérendelt fogalom mondata olvasói nyelven. Szabály-kiegészítés; a v1 véglegesítése (DT585) továbbra is nyitott, változatlanul tervezet.)*

*v0.3 — 2026.10.19 (F11 T1–T2: a 7. pont záró mondata az átírás tényéhez igazítva — a `2_` v21 és a `4_` v18 a B-beli alakot hordozza. Szabály nem változott; változatlanul tervezet.)*

*v0.2 — 2026.10.18 (F11 M2, DT202: mind a négy alpont (a), felhasználó, 2026-10-18): a szakasz-felismerés (4. pont), az `ADAT-HIV` kulcs- és az `ADAT-ÉRTÉK` kifejezés-alakja, a `JELÖLT` gerinc-helye (6. pont); a generátor (`eszkozok/general.py` `--cel forras`, `--cel kinyeres`) ezeket valósítja meg. Változatlanul tervezet.)*

*v0.1 — 2026.10.17 (F23, a DT84 átvezetése: a `javaslat`-jelölések feloldva a felhasználó 2026-10-12-i döntése szerint, (1)–(13) a; a (7) kiegészítése a bővített sablon v18 tükörszabályára, a (10) kiegészítése a „kiadható `apparatus` nézet” megnevezésre és a `【NAPLO】` egyenkénti ítéletére. Változatlanul tervezet.)*

*v0 — 2026.10.08 (F23 M1/1, `F23_MOTIVUM_FORRAS_BRIEF.md`). Döntések: D34 (B út: motívumonként egy kézi forrás), D36 (három mélységi szint, a `belso` buildkor kimarad), D37 + DT66 (c) (aktiválás), DT28 (egyirányúság), DT66 (a)–(b) (szakasz-besorolás, `naplok/MOTIVUM_FORRAS_lekepezes.tsv`), DT68 (1)–(2) (a próza helye, a mérce), DT74 (1), (5) (a #78 váza mint aranyminta), DT76 (9) (13–14. szerep). Bemenet: a #64 mérése (`naplok/TEREMT002_PROZA_PROBA_meres.md` 3. szakasz), a #78 mérése (`naplok/F78_meres.md`). A v0 `javaslat` jelölésű pontjairól a `DONTESEK.md` DT84 tétele döntött (🟢, 2026-10-12); az eredményt a 9. pont foglalja össze.*

**Kimenet nyelve:** magyar

---

## 0. Mire szolgál ez a sablon

A `motivumok/[ID].md` a motívum **egyetlen kézi forrása** (D34). Összefüggő érvelés, amelyben jelölők állnak; a generátor ezekből a jelölőkből nyer ki adatot, és ezekből állítja össze a nézeteket. **Nem adatséma, amelybe prózamezők vannak beszúrva** (F32 KONTEXTUS K1/2): a sablon szakaszsorrendet és jelölőket ad, mezőhatárt nem. Az értelmező próza egy kézben, egy modellel készül, és aki belenyúl, az egészet olvassa (KONTEXTUS K1).

A forrásból generált nézetek (kimenet, kézzel nem szerkeszthetők):

| Nézet | Mélység | Mi lesz belőle |
|---|---|---|
| motívumcikk (a tematikus tanulmány utódja) | `apparatus` | a forrás összes aktív szakasza + az `ADAT-NÉZET` helyére generált táblák |
| lexikonoldal (`lexikon/[ID]_TUDOMANYOS.md`) | `apparatus` | a lexikonoldal-sablon (`6_…`) szakaszai; a kézi rések a forrás `RÉS` jelölői közül |
| olvasói nézet (a törzscikk utódja, #25/#76) | `olvasoi` | csak az `olvasoi` blokkok és az olvasói szintű generált táblák |
| szerkesztői nézet | `belso` | minden, a `【NAPLO】` blokkokkal együtt; nem kiadható |

**Kiadható nézet** az `olvasoi` és az `apparatus` szintű: a motívumcikk és a lexikonoldal **kiadható `apparatus` nézet (a DT-F86a szerint prémium)**, a `belso` réteg buildkor kimarad belőlük, az E29 rájuk is fut (DT84 (10)). A licenc szerinti szűrés nyitott: a #86 DT-F86c pontja (BY-SA-eredetű blokk zárt rétegben ne álljon) ma *javaslat*, nem döntés, ez a sablon nem épít rá. A közös build-idejű szűrő: N-F23b.

A törzscikk (`8_PaRDeS_torzscikk_sablon.md`) a #11-ben megszűnik (D34); csak-törzscikk tartalom nincs (`naplok/MOTIVUM_FORRAS_torzscikk_egyedi.tsv`).

## 1. Három réteg, egy irány (DT28)

A forrás a (b) réteg. Az adat két irányban mozog, és csak ebben a kettőben:

- **(b) → (a) kinyerés:** a forrás kinyerő jelölőiből a generátor jelölt-sort ír (`adat/jeloltek.tsv`), `manual` provenienciával; a sorról ember dönt (`adat/SEMA.md` 3/2, 3.10).
- **(a) → (c) generálás:** a nézetek az adatból és a forrásból generálódnak.

**(a) → (b) út nincs.** A generátor a forrásba nem ír; egyetlen jelölő sem jelent visszaírást; az adatból a forrásba semmi nem kerül vissza. Generált jelölő (`GENERÁLT-KEZDET`, `GENERÁLT`, `ÜRES-BLOKK`, `ÜRES-NYELV`) a forrásban tilos: ha ott áll, az visszaírás-gyanú (`naplok/MOTIVUM_FORRAS_pilot_terv.md` 7. szakasz).

## 2. Mélységi szintek

Három szint: `olvasoi` ⊂ `apparatus` ⊂ `belso` (a nézet a saját szintjét és az alatta lévőket mutatja: az `apparatus` nézet az `olvasoi` blokkokat is). A szabály teljes leírása: `adat/SEMA.md` 3.10.

- **A szakasz alapszintje** a 4. pont táblázatában áll; ehhez a forrásban jelölő nem kell.
- **Eltérés** a szakaszon belül blokkszintű jelölőpárral: `<!-- SZINT-KEZDET: belso -->` … `<!-- SZINT-VÉGE: belso -->`. A pár csak mélyebb szintre válthat (pl. `olvasoi` szakaszon belül `apparatus` vagy `belso` blokk), és nem nyúlhat át `##` címsoron (DT84 (1): a hatókör így gépileg ellenőrizhető). A #64 ideiglenes, egyjelölős `<!-- SZINT: x -->` alakja (a következő jelölőig tartott, kimondott hatókör nélkül; #64 mérés 3. szakasz, 2. tanulság) nem használható.
- **A `【NAPLO: …】` mindig `belso`,** bármilyen szintű szakaszban áll (DT66 (a) 1. kivétel). Jelölő nem kell hozzá: a `【NAPLO` maga a jelölő. Ezért a `【NAPLO】` csak folyamat-nyomot hordozhat (dátum, ki/mikor, forrás elérhetősége). Az állítás megbízhatóságát érintő módszertani figyelmeztetés nem `【NAPLO】`: apparátus-szöveg a Minősítés, a Módszertan vagy a Nyitott kérdések helyén. Az örökölt lapok `【NAPLO】`-jait a #11 szétválasztása egyenként ítéli meg (DT84 (10) (ii); pilot-terv 5. és 8. szakasz).

## 3. Aktiválás

A szakasz aktiválási feltétele a 4. pont táblázatában áll. Inaktív szakasz **üres címmel nem áll a forrásban**; a helyén egy sor: `<!-- INAKTÍV: [szakasz] — a feltétel nem áll fenn: [ok] -->`. A generált nézet az inaktív szakaszt kihagyja.

**A tematikus szakaszok (3., 5., és a lexikonoldal 6. Értelmezés rése) aktiválása (D37, DT66 (c)):**

> aktív, ha `COUNT(DISTINCT fo_elofordulas) ≥ 3` (⭐ küszöb, SEMA 2.2.3) **VAGY** a motívum `statusz` mezője `publikálható` vagy `véglegesített` (`adat/motivumok.tsv`).

A második ág a DT66 (c) „van lezárt tematikus forrás” feltételének B-beli alakja: a migráció után a lezártság a `statusz` mezőben áll, nem egy `tematikus_lezart/` fájl létezésében. A küszöb a tanulmány *indítására* szól, nem a meglévő szakaszokra; a `fo_elofordulas` adatot nem bővítjük (DT66 (c)). *Mért állapot (2026.10.08):* a 9 motívumból 8 `publikálható` (köztük a küszöb alatti KIRALY-001, MENNY-001, HODIT-001: 1-1 csoport), a TEREMT-002 `feldolgozás alatt`, 3 csoporttal; mind a kilenc aktív (`scope=adat/motivumok.tsv+adat/elofordulasok.tsv | forras=manual (szkript, split('\t')) | ts=2026-10-08`).

**Értelmezői aktiválás.** A „⚠️ Vitatott pontok” és a „4. Kapcsolódás a kutatási sablonhoz” feltétele értelmezői ítélet, gépi feltétel nélkül (#64 mérés 5. szakasz, 1–2. pont). Az inaktív állapot ilyenkor a „nincs adat” tényt rögzíti, nem a „nincs vonatkozás” tényt; az `INAKTÍV` sor indoka kötelező, és ezt kimondja (DT84 (6)).

## 4. Szakaszok, sorrendben

Oszlopok: **réteg** = a szakasz célrétege a B szerkezetben (`naplok/MOTIVUM_FORRAS_lekepezes.tsv` `B_helye`; `kezi_forras` = a forrásban próza, `adat` = táblából generált, `generalt` = adatból vagy a forrásból generált); **szint** = alapszint; **aktiválás**; **jelölő** = ami a forrásban a szakasz helyén áll.

| # | Szakasz | Réteg | Szint | Aktiválás | Jelölő a forrásban |
|---|---|---|---|---|---|
| F | Forrásréteg-fejléc | `generalt` (cím, ID a `motivumok.tsv`-ből) | `belso` | mindig | `<!-- FORRÁSRÉTEG … -->`; a fejléc-proveniencia `【NAPLO】` (DT66 (a) 3.) |
| K | Kivonat | `kezi_forras` | `olvasoi` | mindig | `RÉS: kivonat` |
| 0 | Forrás-összegyűjtés a meglévő anyagból | `adat` (a jelölt → `jeloltek.tsv` `forras_kereses`, a `JELÖLT` jelölőn át; `auditok.tsv`-sor a prózából nem keletkezik, az audit-sort a lekérdezést futtató fő szál rögzíti: DT84 (2), SEMA 2.9; a régi folyamat-nyom próza `archivum`) | `belso` | feltételes: örökölt motívum, van előzményanyag | natívnál `INAKTÍV`; örököltnél `ADAT-NÉZET` |
| 1.P | Friss keresés, P1–P7 | `adat` (a jelölt → `jeloltek.tsv` a `JELÖLT` jelölőn át; a lekérdezés audit-sorát a futtató fő szál rögzíti, SEMA 2.9, a lábjegyzetből nincs kinyerés: DT84 (2)); a P2 indoklása `kezi_forras` | `belso` | mindig | a P2 próza; a P1, P3–P6 eredménye proveniencia-lábjegyzettel |
| 1.T | Előfordulások — 7 oszlopos tábla | `adat` (`elofordulasok.tsv`, a `jeloltek.tsv`-n át) | `apparatus` | mindig | `ADAT-NÉZET` (`--cel study`) |
| 1.L | Logikai kötőszó szerinti bontás | `kezi_forras` | `apparatus` (a tudatos kihagyás jelölése `belso`) | feltételes: van igehely-tartományú előfordulás-sor | próza vagy `INAKTÍV` |
| 2 | Eredeti nyelvi összevetés | `kezi_forras` (a szótári idézet `adat`: `lexikon_hivatkozasok.tsv`) | `apparatus` | mindig | próza + `ADAT-HIV` a szótári sorra |
| 2.S | Szótári háttér — szerepmátrix | `generalt` (5. pont) | `apparatus` | mindig | `ADAT-NÉZET` (`--cel lexikon#…#szocikkek`) |
| 2/b | Kiegészítő szótári adatok | `adat` (`lexikon_hivatkozasok.tsv`, SEMA 2.5) | `apparatus` | feltételes: van a generált blokkon túli szótári anyag | nincs kézi blokk; a kísérő mondatok a „Miért fontos” résbe |
| 2.M | Miért fontos ez a lelet | `kezi_forras` | `apparatus` | feltételes: többforrásos szerep-blokk | `RÉS: miert_fontos` |
| 3 | PaRDeS: Peshat, Remez, Drash, Sod | `kezi_forras` | `olvasoi` | tematikus (3. pont) | `RÉS: ertelmezes` |
| 3.V | ⚠️ Vitatott pontok | `kezi_forras` | `olvasoi` | értelmezői: tudományosan vitatott | próza vagy `INAKTÍV` |
| 3.U | Új felismerés | `kezi_forras` (a 3. szakasz része) | `olvasoi` | feltételes: van ilyen | próza a 3. szakaszon belül |
| 4 | Kapcsolódás a kutatási sablonhoz | `kezi_forras` | `apparatus` | értelmezői: van pünkösdi/karizmatikus szakirodalmi vonatkozás | próza vagy `INAKTÍV` |
| 5 | Alkalmazás és tanítványság — *kivezetve (F17, B04, DT756): új cikknél nem írandó; a tudományos lapon nem áll, a meglévő szöveg archívumba kerül* | `kezi_forras` | `olvasoi` | tematikus (3. pont) | próza |
| 5.T | Nevesített tanítói egyezés | `kezi_forras` (hivatkozó mondat a 7. lépés saját fájljára, beemelés nélkül; DT66 (a) 2.) | `olvasoi` | feltételes: lefutott a 7. lépés | hivatkozó mondat vagy `INAKTÍV` |
| 6 | Napló-frissítés (státusz) | `adat` (`motivumok.tsv` `statusz`) | `belso` | mindig | `ADAT-NÉZET` (`--cel naplo`) |
| 7.K | Kereszthivatkozások + Minősítés | `adat` (`jeloltek.tsv` `dontes` + `indoklas`, SEMA 2.4); a „független megerősítés” a minősítés-nézetben generált (TSK-találat ∩ beépített sor), séma-bővítés nélkül (DT84 (8)) | `apparatus` | mindig | `ADAT-NÉZET`; a kétpontos modellbe nem férő tárgyalás kézi próza |
| 7.A | Kapcsolatok + Alátámasztás | `adat` (`kapcsolatok.tsv`, új `indoklas` oszloppal: DT84 (8); a séma-bővítés nem e terv része, SEMA 3.10.7; helye: DT183) | `apparatus` | feltételes: van `kapcsolatok.tsv` sor | `ADAT-NÉZET`; a kétpontos modellbe nem férő eset kézi próza |
| 7.M | Módszertan — ellenőrzési rétegek | `generalt` (a meglévő `auditok.tsv`-sorokból; a régi kézi módszertan-tábla a #11-ben archívum, DT84 (8)) | `belso` | mindig | `ADAT-NÉZET` |
| 7.N | Nyitott kérdések | `kezi_forras` tételenként (l. alább) | `apparatus` | feltételes: van nyitott tétel | `RÉS: modszertan` (csak a tartalmi tételek) |
| 7.Q | Minőségi kapu, verzió-címke | `adat` (`motivumok.tsv` `sablon_verzio`); a kapu-eredmény nézete a meglévő audit-sorokból, a régi kézi kapu-eredmény a #11-ben archívum (DT84 (8)) | `belso` | mindig | `ADAT-NÉZET` |
| P | Proveniencia-sorok | `kezi_forras` (a lábjegyzetek gyűjtőhelye) | `belso` | mindig, ha van lábjegyzet | lábjegyzet-definíciók |

**Szakasz-felismerés** (DT202 (a); ebből jön az alapszint): a szakasz a `##` címsor, és a címsor **eleje** azonosítja: `Kivonat`, `0.`–`7.` (szám, pont, szóköz), `Proveniencia-sorok` (a #64 próza-próbájának alakja, `motivumok/TEREMT-002.md`). A több sorból álló csoport (1, 2, 3, 5, 7) alapszintje a kézi prózát hordozó soráé (1: `apparatus`, 2: `apparatus`, 3: `olvasoi`, 5: `olvasoi`, 7: `apparatus`); a csoport `belso` alsorai `ADAT-NÉZET`-ek a saját `SZINT:` mezőjükkel (7.M, 7.Q), kivéve az **1.P**-t: az 1. szakasz „P1–P7”-et tartalmazó `###` alcíme `belso`. Minden más `###` alcím a szakasz szintjét örökli. Az első `##` előtti rész (cím, `FORRÁSRÉTEG`) az F sor: `belso`. A listán nem szereplő `##` szakasz `belso` (zárt alapérték, SEMA 3.10.2), és a generátor figyelmeztet rá. **P-lépés-figyelmeztetés:** ha az 1. szakaszban egy `###` alcím P-lépést említ (`P1`–`P7`), de a szintje nem `belso` (nem a „P1–P7” alcím, és nem `SZINT-KEZDET: belso` pár áll előtte), a generátor figyelmeztet: a P-levezetés így a kiadható nézetbe kerülne, és ezt az E29 nem látja.

**A Kivonat két kötelező határ-eleme** (v0.4; az ISTENTISZT-001 1. kiadásának tanulsága, 2026-11-02). A `motivumok.tsv` `negativ_kriterium` és `folerendelt_fogalom` mezőjének prózai párja a Kivonatban (`RÉS: kivonat`), az olvasói rétegben:

1. **A negatív kritérium szó szerint ellenőrizhető.** Megnevezi, mely alakok tartoznak ide és melyek nem, úgy, hogy egy igehelyről a szövegből (a Károli-szóból és az eredeti nyelvű alakból) eldönthető legyen; tág minősítés („lényegében”, „jellemzően”) nem elég. Minta (a #151 K4 tanulsága, `naplok/HATAR_ISTENTISZT-001.md`): „a *besém* után az Úr neve, JHVH áll; ahol névmás áll a helyén („nevedet”, „nevét”), az nem tartozik ide” — a ragos alak (*besimchá*, „a te neveden”) és a más név (*besém Jaakóv*) nem. **A kivétel név szerint áll**, indokkal: ha egy hely a minimális jegy nélkül is a motívumban marad, a Kivonat vagy a 3. szakasz megnevezi, és megmondja, milyen szerepben (minta: az 1Kir 18:25–26, ahol a *sém* után nem JHVH, hanem „a ti istenteknek”, illetve Baál neve áll; a hely kontrasztként, kimondott kivételként marad, K5). Ami így nem fogalmazható meg, az határkérdés: a C-h határ-ellenőrzés (`MUNKAMENET.md`) elé kerül, nem a prózába.
2. **A fölérendelt fogalom mondata olvasói nyelven.** A Kivonat kimondja, mi tartozik ide és mi nem, és miért nem a szó (az ige) dönt, hanem a minimális jegy. Belső szó (gerinc, szerep, negatív kritérium, fölérendelt fogalom, hígulás) és forrásnév (BDB, Thayer, TAHOT, SDBH) nincs benne. Minta: a `motivumok/ISTENTISZT-001.md` Kivonatának 2. bekezdése (a felhasználó választása, 2026-11-01): „A motívum nem az imádság általában, hanem az, amikor valaki az Úr nevét kimondva fordul hozzá segítségért. Ha a név nem hangzik el, a segélykiáltás a tágabb körbe tartozik. Az Újszövetségben ezt nem az ige dönti el, mert az mindkét esetben ugyanaz, hanem a név (…).”

**Az 1/a igehelyenkénti prózája — kötelező forma** (v0.5; DT546, a 25. szabály; az ok és a mérés: `naplok/1A_PROZA_jelentes.md`, PR #593). A lexikonoldal 1/a-ja igehelyenként a Károli-vers alatt két sort mutat: a leíró prózát és a „Funkció:” sort. **Mindkettő adat**, nem a `motivumok/[ID].md` szövege: az `adat/elofordulasok.tsv` `kapcsolodas` és `funkcio` mezője (SEMA 2.2). A prózai menet írja őket, a `jeloltek.tsv`-n át, döntéssel, `manual` provenienciával (DT28; 2. szabály); a forrásba nem kerülnek vissza.

1. **A `kapcsolodas`: legalább egy kerek mondat.** Nagybetűvel kezdődik, ponttal zárul, és megmondja, mi történik ezen a helyen a motívummal: ki, kinek, milyen helyzetben, és mi benne a motívumbeli jegy. Nem lehet csak idézet, címszó, gondolatjeles töredék vagy „ua.” (a régi 2/b-csoportpróza szétbontásából maradt alak). A 25. szabály mérője az idézőjeles és zárójeles betéten, valamint a héber/görög szón kívül legalább 7 magyar szót kér (az arany lap legrövidebb kerek prózája ennyi); ez alsó korlát, nem a minőség mércéje. Az idézőjeles betét a fölötte álló Károli-szöveg szó szerinti része; ha nem az (saját vagy más fordítás), a mondat ezt kimondja. Idézőjel a magyar „…”.
2. **A `funkcio`: „címke — magyarázat”.** A gondolatjel (` — `) előtt a rövid címke (pl. `🌱 alap-előfordulás`), utána a motívumbeli szerep egy tagmondatban: mit tesz ez a hely a motívum egészében (első megjelenés, ismétlés, kontraszt, betöltés, kivétel stb.). A generátor a gondolatjel utáni részt írja a „Funkció:” sorba, a címkét az 1. tábla „Funkció (a motívumban)” oszlopába. A kettőspontos (`címke: magyarázat`) és a csak címkés alak nem ez a forma: a generátor kiírja (DT-F1Ab), de a prózai menet „címke — magyarázat” alakra hozza.
3. **Minden igehelyen mindkettő.** Igehely nem maradhat próza vagy „Funkció:” sor nélkül; a tartomány-sor minden verse külön mondatot kap, ha a funkciója más.

**Minta — ISTENTISZT-001, 1Móz 4:26** (az arany lap; `adat/elofordulasok.tsv`, szó szerint):

| mező | érték |
|---|---|
| `kapcsolodas` | A formula első előfordulása — Séth fia, Énós nemzedéke; a Kain-vonal önerős civilizációépítése utáni korszakváltás jele. |
| `funkcio` | 🌱 alap-előfordulás — a motívum legelső megjelenése a kánonban, minden későbbi eset erre vezethető vissza |

A lapon (`lexikon/ISTENTISZT-001_TUDOMANYOS.md`, 1/a):

```
**1Móz 4:26**
*Séthnek is született fia, és nevezé annak nevét Énósnak. Akkor kezdték segítségül hívni az Úrnak nevét.*
A formula első előfordulása — Séth fia, Énós nemzedéke; a Kain-vonal önerős civilizációépítése utáni korszakváltás jele.
Funkció: a motívum legelső megjelenése a kánonban, minden későbbi eset erre vezethető vissza
```

**A próza nem hivatkozik a régi tanulmány pontszámaira** (v0.5; a TEREMT-002 lapjának tanulsága, 2026-11-02). A régi tematikus tanulmány és a régi motívumforrás saját számozása („3. pont, Remez”, „7. pont”, „P2/P3/P4”) a lapon más szakaszra mutat, vagy sehova. A forrás prózája csak a lap saját szakaszaira hivatkozik, a szakasz nevével (pl. „az LXX-fordítói döntések szakasza”); a P1–P7 lépésjel, a DT-, N-, F-szám, a `.tsv`-fájlnév és a belső szó (gerinc, szerep) az olvasói rétegben nem áll (ha kell, `belso` blokk vagy `【NAPLO】`, 2. pont). A régi tanulmány csak alapanyag: az új cikk mondata nem költözik belőle bájtra (DT546).

**Teljesség-mérés — három háló** (v0.5; DT548). Minden új cikk prózája előtt lefut, és a levezetés üres eredménynél is dokumentált (CLAUDE.md, kutatási menet):

| háló | mit keres | mivel |
|---|---|---|
| (1) Strong-scan | a motívum gerinc-Strongjainak minden előfordulása az ÓSZ-ben és az ÚSZ-ben | `eszkozok/lekerdez.py` |
| (2) Károli-szavak | a motívum Károli-megfelelőinek (`karoli_szo`, a szótári alakok a szótövező táblán át) minden előfordulása a Károli-szövegben | Károli-szöveg + szótövezés |
| (3) szótári igehelyek | a BDB és a Thayer által a motívum Strongjainál idézett igehelyek | `adat/bdb_vers_jelentes.tsv`, Thayer-hivatkozások |

Mindhárom háló találata a motívum `elofordulasok.tsv`- és `jeloltek.tsv`-soraival vetendő össze. **Az eltérés** (a háló talál, az adat nem ismeri) a `jeloltek.tsv`-be kerül `nyitva` sorként, a háló nevével az indoklásban; döntés a B5 szerint, gyenge vagy asszociatív anyaggal nem tölthető ki (3. szabály). A mérés helye a motívum naplója (a #123-ban: `naplok/F123_teljesseg_<ID>.md`), hálónként a találat, az egyezés és az eltérés száma, proveniencia-sorral. **Fogalmi és strukturális azonosság-hordozónál** (`motivumok.tsv` `azonossag_tipusa`) a Kivonat egy olvasói mondatban kimondja, hogy az előfordulások listája keresési módszer eredménye, nem kimerítő felsorolás.

**Az új cikk öt szabálya** (v1; DT585, az ALVIL-001 új cikkének tanulsága, 2026-11-03). Minden új cikkre kötelező, a teljesség-mérés és a próza között:

1. **Saját elutasítási okok.** A motívum jellemző elutasítási okai (pl. „csak az egyik szó áll a mondatban”, „a Septuaginta többlete”, „szótári összevető hely”) motívumonkénti mintasorként az `adat/elutasitasi_okok.tsv`-be kerülnek (SEMA 2.43), a `jeloltek.tsv` elutasító `indoklas`-ának elejére illesztve. Enélkül az 1/b. blokk összesítője a be nem sorolt indoklást a közös „a formula nincs a versben” okhoz teszi, és az olvasó rossz okot lát (ALVIL-001, F123.ALVIL2.6); ha egyik minta sem illik, a generálás megáll („egyéb” kategória nincs, F123.EGYEB; kapu: `ellenoriz.py` 28.).
2. **Lexémánként egy blokk-sor.** A teljesség-mérés más szavas (más lexémát hordozó) találatai nem egyenként, hanem lexémánként **egy** `jeloltek.tsv`-sorba kerülnek (`elutasítva`, az indoklásban a versszám és a lista helye; minta: DT503, DT564). Egyenként csak az a hely bírálandó el, amelyben a motívum szava (a negatív kritérium jegye) a versben áll.
3. **A negatív kritérium ÚSZ-mércéje.** A negatív kritérium (4. pont, „A Kivonat két kötelező határ-eleme”) szó szerint ellenőrizhető, és kimondja az újszövetségi mércét: **a Károli alapszövege, a Textus Receptus**; ahol a kritikai szövegkiadás (a TAGNT NA28/SBL olvasata) eltér, a lap jelöli (DT563, általános szabály). Minden újszövetségi előfordulás- és jelölt-helyen a TR/kritikai eltérés megnézendő, és az eredmény (eltérés van / nincs) a motívum naplójában áll.
4. **A Septuaginta-többlet nem előfordulás.** Ha a görög fordítás a motívum szavát hozza ott, ahol a héber szövegben nem áll, a hely nem előfordulás (a motívum a héber szövegre épül); a próza tényként említheti (a fordítók értelmezése), és a `jeloltek.tsv`-ben elutasított sor (DT564 (1)).
5. **Idézet jelöléssel.** Az olvasói rétegben idézőjeles szöveg csak a fölötte álló (vagy a mondatban megnevezett) Károli-vers szó szerinti része lehet; ha más (saját vagy más fordítás), a mondat ezt kimondja („saját fordításban”). Az olvasói kapu IDEZET-osztálya ezt méri.

**A HAMART-001 mint arany: a lezárás hét szabálya** (v2; F178.2–F178.3, a felhasználó szavai, 2026-11-08: „a hamart lesz az új arany / fontos hogy most már visszaesés ne legyen innen”). A HAMART-001 1. kiadás előtti javítókörei (határ-ellenőrzés 52 soron, lezárás 60 soron, 11 átcsúszott határhiba; a Kivonat hamis „feszültsége” a 8:21 és a 9:25 között) hét szabályt adtak. Minden új cikkre és minden 2. kiadásra kötelező, az öt szabály után:

1. **A határ (U2) és a próza (U3) két kézben.** A határdöntést (melyik sor beépített, melyik elutasított, milyen indokkal) hozó session nem írja a prózát; ha mégis egy session viszi a kettőt, a független határ-ellenőrzés (`MUNKAMENET.md` C-h, modelles rész) **az U3 előtt** fut, és az U3 csak a határkör döntései után indul. Ok: aki a határt húzta, a prózában a saját döntését igazolja, nem méri.
2. **A határ-ellenőrzés a mai soron.** A C-h modelles része a motívum beépített sorainak egy állapotára készül; az állapotot a rész első sora rögzíti (`<!-- SORÁLLAPOT: n=… ujj=… -->`, a jel: `python eszkozok/ellenoriz.py --hatar-ujjlenyomat <ID>`). Minden sor-változás (új, törölt vagy módosított `elofordulasok.tsv`-sor) után a C-h újrafuttatandó; nem friss modelles résszel a lap nem adható ki (Feed 5. kritérium, `ellenoriz.py` 39. szabály: jelentés minden érintett motívumra). **Kivétel, és nincs újabb kör (F182, F26):** (a) a határ-ellenőrzés nem veti fel újra azt a sort vagy kérdést, amelyre szerkesztői döntés (`manual` DT/N, a `jeloltek.tsv` `dontes_ref`-je vagy a `DONTESEK.md`) van: a jelentésben „lezárt (DT…)” jelöléssel sorolja fel; (b) ha a sor-változás magából a határ-ellenőrzés kérdéseinek döntéséből ered (a `jeloltek.tsv`-n át, DT-hivatkozással), a döntés commitja a `naplok/HATAR_<ID>.md` modelles részének végére (a jelölők közé, mert a gépi rész újrafuttatáskor csak az marad meg) határdöntés-jelet ír (`<!-- HATÁRDÖNTÉS: n=… ujj=… \| DT-… -->`, a mai jel a `--hatar-ujjlenyomat` kimenetéből, a döntések azonosítóival); a 39. szabály az ezzel egyező állapotot frissnek veszi, és a határ lezárt: új modelles határ-kör nem indul, csak új (nem a határdöntésből eredő) sor-változás után.
3. **A Kivonat 1. bekezdése a lánc fordulópontját is kimondja**, nem csak a lépéseit: hol fordul meg, áll meg vagy vált irányt a lánc. A fordulópont adatból igazolt (a beépített sorok `funkcio`-ja, a szó és az igealak), nem a próza feltevése. *Tanulság: a HAMART-001 első Kivonata a 8:21 és a 9:25 között „feszültséget” állított, amelyet az adat nem hordozott: a 8:21 más igével (kálal) zárja ki a föld további átkát, a 9:25 átka Kánaánra szól.*
4. **A beépítés indoka szerkezeti jegy**, nem a szó puszta egyezése (strukturális és fogalmi hordozón: `ellenoriz.py` 38. szabály); a beépített sor nem eshet a lap saját csoportos kizárási okába (37. szabály).
5. **Kerek 1/a és „Funkció:” sor minden igehelyen**; minden idézet a fölötte álló Károli-vers szó szerinti része (25. szabály, olvasói kapu IDEZET).
6. **A Nave-blokk (Tematikus index) nem üres**, a döntések az `adat/tematikus_temak.tsv`-ben (DT595).
7. **A próza nulláról, egy kézből, a `sablonok/10_PaRDeS_U3_proza_prompt_sablon.md` szerint** (`MUNKAMENET.md` C-w).

A szabályok gépi része a lexikonlap regressziós HIBA-kapuja (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`, „A HAMART-001 regressziós kapui”); ahol egy meglévő lap elbukik, a hiba a lap 2. kiadásának tétele, nem kivétel és nem kézi folt.

**A 7.N tételenkénti besorolása** (DT66 (a) 4.; a lekepezes `7. Nyitott kérdések` sora): a *tartalmi* nyitott kérdés (értelmezési, exegetikai) `kezi_forras`, `apparatus`, a 7.N-ben marad; a *séma-korlát* (a tábla nem tudja ábrázolni) és az *adatállapot* (forrás hiányzik, bekötés hiányzik) nem a motívum érvelése: N-tétel a `NYITOTT_FELADATOK.md`-ben (a `/befogad` útján), a forrásban legfeljebb `【NAPLO】` mutató; a *lezárt* tétel (áthúzott) a migrációban archívum (DT84 (5); az ISTENTISZT-001 öt tételére alkalmazva: pilot-terv 4.4).

**Két új szakasz a tematikus sablonhoz képest** (#64 mérés 3. szakasz, 4. tanulság: a tematikus sablonból hiányzott; felvéve: DT84 (4)): a **7.N Nyitott kérdések** (a lexikonoldal `modszertan` résének kézi része) és a **P Proveniencia-sorok** (lábjegyzet-alak, az ISTENTISZT-001 és a TEREMT-002 mintája).

**Ami nem szakasz** (`sablonszabaly`, DT66 (b)): a „Mikor használandó”, a terminológiai és formai szabályok, a konfliktuskezelés, a Lezárási checklist, a licenc, a fájlnév-konvenció, a lexikonoldal Minőségi kapuja (a CI veszi át: `naplok/MOTIVUM_FORRAS_ci_terv.md`), a megszűnt kimenetek (OLVASHATÓ, KÉT fájl, törzscikk). Ezek a 6–8. pontba kerültek, vagy megszűnnek.

**Örökölt motívum `motivumok/[ID].md` blokkjai** (ma a napló archív másolatai): a Tematikus áttekintés, a Kulcsszó-index és a Lezárt tanulmányok indexe `generalt` (a #11-ben archívum); a ⭐-bekezdés száma és igehely-listája `generalt`, értelmező mondatai a Kivonat/3. szakasz anyaga; a „Kulcsszavak részletesen” igehely-listája és státusza `adat`, a maradék értelmező szöveg a Kivonat/3. szakasz anyaga (lekepezes, `szetvalasztando`).

## 5. A szótári szakasz (2.S) — a szerepmátrix szerint

A szótári háttér **generált**: a forrás nem tartalmazza, csak a helyét jelöli (`ADAT-NÉZET`). A váz a #78 aranymintája (`generalt_proba/F78_szerepmatrix_proba/lexikon/ISTENTISZT-001_TUDOMANYOS.md`, 2. szakasz; `naplok/F78_meres.md` 9–11., 14.):

- **Sorrend:** nyelvenként (görög, héber), azon belül az `adat/szotar_szerepek.tsv` `sorrend` mezője szerint (1–10); a mindkét nyelven azonos (szerep, forrás, állapot) sorok (12–14.) egyszer, a „Nyelvfüggetlen szerepek” alatt; a végén a „Rokon szavak”. A 11. sorszám nincs kiosztva (SEMA 2.13).
- **Állapot → blokk** (ATALAKITASI 13.3, DT80, DT82):
  - `adatosítva` + van sor → a forrás(ok) blokkja;
  - `adatosítva`, de a tartalom máshol él → hivatkozás („l. 2/b”, „l. 3. szakasz”, „l. 1. szakasz UBS-oszlop”), nem üres blokk;
  - `adatosítva`, de a tokenhez nincs sor → jelölt üres blokk `adatosítva, nincs bekötve` állapottal, mutató a #9-re;
  - `nincs adatosítva` / `javaslat` → **explicit üres blokk**: `<!-- ÜRES-BLOKK: [szerep] | [állapot] -->` + látható zárójeles sor; részadat (TWOT-szám, kiejtés-lemma) esetén a sor kimondja, hogy csak részadat áll;
  - `nincs forrás` → nincs blokk;
  - token nélküli nyelv → `<!-- ÜRES-NYELV: [nyelv] | nincs Strong-token -->`.
- **13. Károli-megfelelők (+ SZPA)** és **14. Rejtett / hamis párhuzam:** `javaslat` állapotú szerepek (DT-M4, DT76 (9)); amíg a #22 nem teljes, explicit üres blokk.

A 26 sor (13 szerep × 2 nyelv) a forrásban **nem** ismétlődik; az alábbi váz csak azt mutatja, hova mutat a forrás kézi anyaga:

```
### Görög szavak / ### Héber szavak
#### 1. Alapjelentés             ← generált (TBESG / TBESH)
#### 2. Mélységi szócikk         ← generált (Thayer / BDB)
#### 3. Teológiai szócikk        ← üres blokk (nincs adatosítva); héber: TWOT-szám részadat
#### 4. Jelentésszerkezet        ← generált (SDGNT / SDBH domén)
#### 5. Tömör jelentés           ← görög: generált vagy hivatkozás; héber: üres blokk
#### 6. LXX-híd                  ← hivatkozás a lexikonoldal 3. szakaszára
#### 7. Megfelelők               ← ma „l. 2/b”; a B-ben a 2/b adata (lexikon_hivatkozasok) tölti
#### 8. Nyelvi háttér            ← görög: LSJ vagy hivatkozás; héber: üres blokk
#### 9. Versenkénti jelentés     ← görög: hivatkozás az 1. szakaszra; héber: üres blokk
#### 10. Kiejtés                 ← részadat + üres blokk
### Nyelvfüggetlen szerepek
#### 12. Tematikus index          ← üres blokk (javaslat)
#### 13. Károli-megfelelők (+ SZPA) ← üres blokk (javaslat)
#### 14. Rejtett / hamis párhuzam  ← üres blokk (javaslat)
### Rokon szavak
```

**Mit ír a forrás a szótári részhez:** csak értelmezést, a 2. szakaszban (Eredeti nyelvi összevetés) és a 2.M-ben (Miért fontos). Szótári idézetet a próza nem másol be: az `ADAT-HIV` jelölővel a `lexikon_hivatkozasok.tsv` sorára mutat (6. pont). Kitöltetlen szerepet a próza nem pótol (CLAUDE.md 3. szabály): az üres blokk a generált nézetben látszik, és ez elfogadott kimenet. A 2/b kézi blokk a B-ben megszűnik: a szó szerinti kivonatai a `lexikon_hivatkozasok.tsv`-be kerülnek (a #9 vagy a #11 adatútján, a jelölt-folyamaton át), és a szerepmátrix 5., 7. és 8. blokkját töltik; a kísérő mondatai a Miért fontos résbe.

## 6. Jelölők — mit nyer ki belőlük a generátor

Minden jelölő HTML-megjegyzés, saját sorban (kivéve a `【NAPLO】` és a lábjegyzet). **Szerkezeti** jelölőből a generátor semmit nem nyer ki; **kinyerő** jelölőből jelölt-sort ír; **ellenőrző** jelölőből semmit nem ír, csak összevet. A kinyerés részletes szabálya (kulcs, ütközés, proveniencia): `adat/SEMA.md` 3.10.5.

| Jelölő | Alak | Fajta | Mit nyer ki a generátor | Melyik táblába |
|---|---|---|---|---|
| Forrásréteg | `<!-- FORRÁSRÉTEG (F4 G2) — kézzel írt, szabadon szerkeszthető. NEM generált fájl. -->` | szerkezeti | semmit | — |
| Szint | `<!-- SZINT-KEZDET: [szint] -->` … `<!-- SZINT-VÉGE: [szint] -->` | szerkezeti (szűrő) | semmit; a nézet mélysége szerint szűr | — |
| Napló | `【NAPLO: …】` | szerkezeti (mindig `belso`) | semmit (DT66 (a) 1.: az `adat` alternatíva elvetve) | — |
| Inaktív | `<!-- INAKTÍV: [szakasz] — [ok] -->` | szerkezeti | semmit; a szakasz kimarad a nézetből | — |
| Rés | `<!-- RÉS-KEZDET: [rés] -->` … `<!-- RÉS-VÉGE: [rés] -->` | szerkezeti | semmit; a törzs a lexikonoldal résébe kerül (a `res_forras.tsv` `tanulmany` mezője a `motivumok/[ID].md`-re mutat) | — |
| Adat-nézet | `<!-- ADAT-NÉZET: [szakasz] \| forrás: [tábla (mezők)] \| cél: [general.py --cel …] \| SZINT: [szint] -->` | szerkezeti | semmit; a nézetben ide kerül a generált tábla | — |
| Jelölt | `<!-- JELÖLT: [igehely] \| gerinc: [gerinc_elem] \| [rövid indoklás] -->` | kinyerő | egy jelölt-sort, `dontes=nyitva` értékkel (a jelölő nem dönthet); `indoklas` = `gerinc: [gerinc_elem] — [rövid indoklás]`, a `forras_kereses` szakasz-mutatója a `##` címsor szövege (DT202 (d)) | `adat/jeloltek.tsv` (nem közvetlenül az `elofordulasok.tsv`: SEMA 3/2) |
| Proveniencia-lábjegyzet | `[^kulcs]: proveniencia: [a lekerdez.py sora szó szerint]` | szerkezeti (hivatkozás) | semmit; az audit-sort a lekérdezést futtató fő szál rögzíti (SEMA 2.9). Audit-kinyerés a lábjegyzetből nincs (DT84 (2)): a lábjegyzet a fő szál által már rögzített nyom másolata, nem új adat; a SEMA 3/9 és 2.9 változatlan | — |
| Adat-hivatkozás | `<!-- ADAT-HIV: [tábla] \| [mező]=[érték]; [mező]=[érték]; … -->` | ellenőrző | semmit; ellenőrzi, hogy pontosan egy sor egyezik (alább); eltérésnél kinyerési jelentés-sor, a futás megáll | — (a hiányzó sort a #9 / a döntéssel írt adatút pótolja) |
| Adatból számolt érték | `[érték]<!-- ADAT-ÉRTÉK: [tábla] \| count([szűrő]) -->` vagy `… \| count_distinct([mező]; [szűrő]) -->` | ellenőrző | semmit; ha a prózában álló érték eltér a táblából számolttól, hiba (alább) | — |

**Az ellenőrző jelölők gépi alakja** (DT202 (b), (c); a generátor: `eszkozok/general.py --cel kinyeres`):

- **`ADAT-HIV`:** a `[tábla]` az `adat/` alatti fájl neve (pl. `lexikon_hivatkozasok.tsv`); utána `mező=érték` párok `; ` elválasztóval, **a tábla SEMA-kulcsának minden mezőjével, és csak azokkal** (`adat/SEMA.md` 2. szakasz „Kulcs:” sorai; pl. `<!-- ADAT-HIV: lexikon_hivatkozasok.tsv | szotar=BDB; strong=H7121; entry_id=…; jelentes_szam=… -->`). Pontosan egy sornak kell egyeznie (az érték karakterre). Hiba: a táblában nem létező (elírt) mezőnév, hiányos vagy kulcson kívüli mezővel bővített kulcs, nulla vagy több egyező sor, kulcs nélküli tábla (pl. `auditok.tsv`).
- **`ADAT-ÉRTÉK`:** a jelölő közvetlenül az érték után áll (köztük nincs szóköz); az érték nemnegatív egész szám. A kifejezés **zárt készlet** (a forrásból kód nem fut): `count([szűrő])` — a szűrőnek megfelelő sorok száma; `count_distinct([mező]; [szűrő])` — a szűrőnek megfelelő sorokban a mező különböző, nem üres értékeinek száma (pl. `3<!-- ADAT-ÉRTÉK: elofordulasok.tsv | count_distinct(fo_elofordulas; id=ISTENTISZT-001) -->`). A szűrő az `ADAT-HIV` `mező=érték; …` alakja, legalább egy feltétellel, kulcs-megkötés nélkül; a mezőnek a táblában léteznie kell. Az érték karakterre egyezik a számolttal (`04` ≠ `4`). Hiba: ismeretlen függvény, rossz szűrő (pl. `=` nélküli tag, nem létező mező), eltérő érték, hiányzó vagy nem egész érték.

**Nem igehely-kulcsú adat a prózában** (szótári idézet, LXX-megfelelő, kapcsolat-indoklás, kapu-eredmény): a `jeloltek.tsv` kulcsa `id` + `igehely`, ezért ezekre jelölt-sor nem írható (`naplok/F78_meres.md` 12. szakasz, 2. pont). Az út az `ADAT-HIV` (DT84 (3)): a próza a meglévő sorra hivatkozik; ha a sor hiányzik, a generátor kinyerési jelentésben jelzi, és a sort döntéssel, `forras=manual` provenienciával a megfelelő meglévő adatút írja. Új jelölt-tábla nem igehely-kulcsú adatra nincs; a kérdés a #9 adatosítás tapasztalata után nyitható újra.

**Generált jelölők a forrásban tilosak** (1. pont): `GENERÁLT-KEZDET`, `GENERÁLT-VÉGE`, `GENERÁLT:`, `ÜRES-BLOKK`, `ÜRES-NYELV`.

## 7. A tematikus sablon szabályai — mi kerül át

A `4_PaRDeS_tematikus_sablon.md` v16 (a v17 a P2 domén-mondatát pontosította, tartalmi követelmény nélkül) szabályai:

| Szabály | Sorsa a B-ben |
|---|---|
| 1. pont: mind a hét oszlop kötelező; üres cella `—` (v16, F5.1) | **átkerül a generátorba:** a tábla `ADAT-NÉZET`, a hét oszlopot a `--cel study` írja |
| Jelentés-szöveg: BDB eredeti angol + magyar a cellán belül (v15) | **átkerül a generátorba:** `elofordulasok.tsv` `jelentes_en` + a `forditasok.tsv`; a prózai, bővebb magyarítás a forrásban marad |
| P1–P7 checklist, proveniencia-sor kötelező (v16, F5.3) | **változatlan**; a proveniencia-sor lábjegyzetben áll (6. pont) |
| Logikai kötőszó szerinti bontás (v13) | **változatlan** (1.L szakasz) |
| Kiejtés minden héber/görög szónál | **változatlan** |
| Mélység-engedmény a 2. pontban (2026.09.03) | **változatlan** |
| PaRDeS-rétegfegyelem (a lexikonoldal L7-je) | **változatlan** |
| Napló-jelölés kötelező, a négy trigger, formázási szabály (üres sor a `【NAPLO】` előtt) | **változatlan**; kiegészül: a `【NAPLO】` mindig `belso` (2. pont) |
| Idézés-formázás (blockquote csak eredeti nyelv) | **változatlan** |
| Hangnem (harmadik személy, nincs „mi”-hang) | **változatlan** |
| Nevesített tanítói módszer (öt lépés), forrás-megbízhatóság (✅/⚠️) | **a 7. lépés saját fájljában él**; a forrás hivatkozik rá (DT66 (a) 2.) |
| Fájlnév `[Motívum]_tematikus.md` | **megszűnik**: a forrás `motivumok/[ID].md` |
| Index-frissítés, generált blokkok újragenerálása | **változatlan** (`general.py`) |
| Utólagos bővítés: adat- és naplóréteg ugyanabban a PR-ben | **változatlan** az (a) pontban; a (b) „Kulcsszavak részletesen” kézi frissítése megszűnik (generált) |
| Verzió-címke tanúsítás, nem dátum (v16, F5.2) | **adat**: `motivumok.tsv` `sablon_verzio`; a forrásban nem ismétlődik |
| Minőségi kapu Q1–Q7 | **a forrás kapuja a 8. pont**; a Q2 és a Q7 forrás-oldali nyoma az adatrétegben ellenőrizhető (E4, SEMA 3.8) |
| Lezárási checklist 1. (`/mnt/user-data/outputs/`), 12. (visszahivatkozás a bővítettbe) | **megszűnik / generált**: a visszamutató link az `elofordulasok.tsv` `felmerult_tanulmany` mezőjéből (DT66 (a) 5.); a mező ma erre nem alkalmas (vegyes fájlnév és szabad szöveg), a normalizálásáról a #11 briefje dönt (N-F23a) |
| „Tartalmi visszaírás bővített tanulmányokba” (v10) | **megszűnik** (DT84 (7)): a lelet kézi bemásolása egy másik kézi forrásba második igazságforrást hoz létre (D34: hivatkozás másolás helyett; DT28). A visszamutató link generált (fenti sor, N-F23a); a már visszaírt lelet a #11-ben archívum vagy törlés (DT66 (a) 5.) |
| Terminológia: „Szent Szellem”, igehely-forma (`1Thessz 5:23`), SZPA csak rövid idézet | **változatlan** |
| Konfliktuskezelés: ütközésnél rákérdezés | **változatlan** |

**A tükörpár: a tanulmány (bővített) sablon v18 „Tartalmi visszaírás lezárt tematikus tanulmányba” szabálya** (`2_PaRDeS_bovitett_sablon.md` 7. pont) **átalakul** (DT84 (7) kiegészítése). A B-beli alakja:

1. A tanulmányban felmerült, igehely-szintű lelet **adatrésze** a `jeloltek.tsv`-n át, döntéssel kerül az adatrétegbe (SEMA 3/2, 3/9; `manual` provenienciával), nem a motívum forrásának szövegébe.
2. Ha a motívumról **értelmezés** is születik, az saját szöveggel a `motivumok/[ID].md`-be kerül (a motívum egyetlen kézi forrása); a tanulmányban csak hivatkozás áll rá.
3. **Kézi másolás egyik irányban sincs:** sem a tanulmányból a motívum-forrásba, sem vissza; a túloldali mutató generált (a fenti sor, N-F23a).

A propose-then-confirm fegyelem (a lelet egyenként megbeszélve) a jelölt-döntésben él tovább. A `2_PaRDeS_bovitett_sablon.md` szövegének teljes átírása nem e tervezet része: a DT182 (felhasználó, 2026-10-17: c.) szerint a v18 szabály, a tematikus sablon v10 szabálya és a Lezárási checklist 12. pontja előbb felfüggesztő sort kapott (F23.D14), a teljes átírás a #11-ben készült el (F11 T1–T2, 2026-10-19: `2_PaRDeS_bovitett_sablon.md` v21, `4_PaRDeS_tematikus_sablon.md` v18).

## 8. Minőségi kapu (a forrásra)

A mérce: a lexikonoldal-sablon Minőségi kapuja **L1–L7** + a **DT2 két rés-szabálya** (DT68 (2), DT74 (5)), a szótári részen a **#78 váza**. A forrásra a #64 mérése szerinti átfordítással (`naplok/TEREMT002_PROZA_PROBA_meres.md` 2. szakasz):

- **L1** szerkezeti teljesség: a 4. pont minden aktív `kezi_forras` szakasza jelen van; az inaktív `INAKTÍV`-jelölővel, üres cím nélkül; az `adat` szakasz `ADAT-NÉZET`-jelölővel.
- **L2** napló-jelölés: dátum-, eredet-, döntés-, folyamat- és állapotmondat csak `【NAPLO】`-ban.
- **L3** lexikai vs. tematikus: a nem lexikai kapcsolat „tematikus, nem lexikai” jelölést kap.
- **L4** kereszt-motívum szennyeződés kizárva.
- **L5** nevesített tanítói szakasz: hivatkozás a 7. lépés fájljára, vagy `INAKTÍV` hiányjelzéssel.
- **L6** a)–f) fegyelem; **L7** PaRDeS-rétegfegyelem.
- **DT2/1** minden rés kitöltött vagy explicit hiányjelölésű; **DT2/2** az adatból generált rész `adat`-forrás-jelölésű (`ADAT-NÉZET`).
- **Szótári rész:** a generált nézet 2. szakasza a 5. pont szerint; kitöltetlen szerep explicit üres blokk.

A nézetekre vonatkozó két gépi ellenőrzés (bájtazonosság, nulla `belso` a kiadható kimenetben): `naplok/MOTIVUM_FORRAS_ci_terv.md` (E28, E29).

**Gépi kapuk a generált lapon** (v0.5; DT546, DT547). A forrás és az adat akkor kész, ha a belőlük generált lap átmegy a lexikonoldal-sablon Minőségi kapujának L8 pontján (`sablonok/6_PaRDeS_lexikon_oldal_sablon.md`: 24. és 25. szabály, teljesség-mérés, olvasói kapu). A kapuk a szerkezetet és a gépesíthető olvasói hibát mérik; a mondat minősége (kerek-e, és a Funkció tényleg a motívumbeli szerepet mondja-e) a lektori kör és a felhasználó vizuális átnézése (`MUNKAMENET.md` C-v).

## 9. A v0 nyitott pontjai — eldöntve (DT84, 🟢, felhasználó, 2026-10-12)

A zárójeles szám a DT84 pontjának száma (DT84 (1)–(8), (10)); a DT84 (9), (11)–(13) a pilot-tervben áll.

- **(1) Szintjelölő:** `SZINT-KEZDET` / `SZINT-VÉGE` pár, alapszint jelölő nélkül, csak mélyebb szint felé, `##`-en át nem (2. pont).
- **(2) Proveniencia-lábjegyzet:** csak hivatkozás, audit-kinyerés nincs; az audit-sort a fő szál rögzíti (SEMA 2.9); a SEMA 3/9 változatlan (6. pont).
- **(3) Nem igehely-kulcsú adat:** `ADAT-HIV` + kinyerési jelentés; a hiányzó sort a meglévő adatút írja döntéssel, `forras=manual` provenienciával; új jelölt-tábla nincs (6. pont).
- **(4) Két új szakasz** (7.N, P) felvéve (4. pont).
- **(5) A 7.N tételenkénti besorolása** és az ISTENTISZT-001 öt tételének besorolása elfogadva (4. pont; pilot-terv 4.4).
- **(6) Értelmezői aktiválás:** értelmezői döntés, az `INAKTÍV` indoka kötelező, és a „nincs adat” tényt rögzíti (3. pont).
- **(7) „Tartalmi visszaírás”:** a tematikus v10 szabálya megszűnik, a tükörpárja (a tanulmány-sablon v18) átalakul; a mutató generált (N-F23a); a már visszaírt lelet a #11-ben archívum vagy törlés (7. pont). A `2_…` és a `4_…` sablon szövegének módosítása: DT182.
- **(8) Séma-kérdések:** Alátámasztás → új `indoklas` oszlop a `kapcsolatok.tsv`-ben; független megerősítés → a minősítés-nézetben generált, séma-bővítés nélkül; Módszertan-tábla és kapu-eredmény → archívum, a nézet a meglévő audit-sorokból (4. pont; SEMA 3.10.7).
- **(10) Kiadható nézet:** a lexikonoldal és a motívumcikk kiadható `apparatus` nézet (a DT-F86a szerint prémium), az E29 rájuk is fut; a `【NAPLO】` csak folyamat-nyom (0. és 2. pont). A DT84 (9), (11)–(12) a pilot-tervet érinti (`naplok/MOTIVUM_FORRAS_pilot_terv.md` 8. szakasz); a (13): lent.

A sablon a pilotok után válik véglegessé (DT84 (13): a #11 1. lépcsője a v0.1-en fut, a #12 a két pilot tapasztalatával véglegesít); addig tervezet. *A #12 2026-11-02-án lezárult; a véglegesítés (v1) a #123 DT585 tétele (DT497 (2)) — 2026-11-03-án megtörtént (lent a fejléc).*
