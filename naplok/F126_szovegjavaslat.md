# F126 — szövegjavaslat (ISTENTISZT001_PROZA, 4. lépés ⛔)

*FELADATOK #126 · `F126_ISTENTISZT001_PROZA_BRIEF.md` 3. szakasz 4. lépés · 2026-10-20 · modell: claude-opus-5-5*

**A forrásba (`motivumok/ISTENTISZT-001.md`) a jóváhagyásig semmi nem kerül.** Kérlek, bekezdésenként (A1 … C1) jelezd: **jóváhagyva / javítandó (mit) / elvetve**. Az elvetett bekezdés helyére nem kerül pótlás.

A mérés: `naplok/F126_meres.md` (minden szám ott van, lekérdezésenként). A proveniencia-sorok a bekezdés alatti dőlt sorban állnak: a `【NAPLO】` a lapról kivágódik (`adat/SEMA.md` 3.10.3), ezért a proveniencia látható apparátus-sorként megy.

Közös forma minden bekezdésre: a mért tény és az értelmezés külön mondatban; az értelmező mondat „Értelmezés (szint):” kezdetű. Új Sod nincs, motívumközi állítás nincs (ALVIL-001, HAMART-001, TEREMT-001 nem szerepel), idézés-állítás nincs, új adatsor nincs.

## Beszúrási pontok

| Pont | Rés | Hol, a forrásban | Bekezdések |
|---|---|---|---|
| **A** | `ertelmezes` | a „PaRDeS keretrendszer” alszakaszban, a **Peshat** bekezdés két felsorolás-sora után (az „**1Móz 21:33** — az egyetlen genezisi hely …” sor után), a „**Remez:**” bekezdés előtt | A1–A4 |
| **B** | `ertelmezes` | ugyanott, a „**Lexikai kiegészítés … — Remez-szint**” blokk után (a „**3. A Róm 10:12**” bekezdés és az utána álló `【NAPLO: … 22/18-ra javító …】` után), a „**Drash:**” bekezdés előtt | B1–B7 |
| **C** | `modszertan` | a „A BDB H7121 2.c citációs listájának egyezése …” bekezdés után, a „#### A "be nem sorolható" eset mögötti hármas tipológia (A/B/C)” cím előtt | C1 |

Mindhárom pont a meglévő `<!-- RÉS-KEZDET -->` / `<!-- RÉS-VÉGE -->` jelölőkön belül van (RENDER_BRIEF G1/G2). Szakasz nem rendeződik át, meglévő mondat nem változik.

---

## A — Peshat (az `ertelmezes` rés, a Peshat bekezdés után)

### A0 — bevezető sor

```markdown
**Peshat — a motívum közepe【NAPLO: F126, 2026-10-20 — a próza-felmérés (naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md) 1., 7., 9. és 10. összefüggése, saját méréssel: naplok/F126_meres.md】:**
```

### A1 — A Kármel-jelenet (1. összefüggés) · Peshat · lefedi: 1Kir 18:25, 1Kir 18:26

```markdown
**A Kármel-jelenet (1Kir 18:24–26).** A három vers egy próba lefolyását adja. A 18:24-ben Illés kimondja a mércét: „a mely isten tűz által felel, az az Isten”. A 18:25-ben Baál prófétái kapják a felszólítást: „hívjátok segítségül a ti istenteknek nevét, de tüzet ne tegyetek alája”. A 18:26-ban végrehajtják: „segítségül hívák a Baálnak nevét reggeltől fogva délig, mondván: Baál! hallgass meg minket! De nem jött szó, sem felelet.” A „felel” ige (עָנָה, ánáh, H6030) a 18:26-ban kétszer áll: a hívók kérik („hallgass meg minket”), és a felelet elmarad („sem felelet”). A segítségül hívás szerkezete (קָרָא בְּשֵׁם, kárá besém) a két félnél azonos; a 18:25–26-ban a megszólított név Baálé (H1168).

Értelmezés (Peshat): a jelenetben a segítségül hívás választ váró kérés, és a próba tárgya nem a hívás, hanem a felelet: a hívás formája mindkét félnél ugyanaz, a különbséget az mutatja meg, hogy jön-e válasz.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAHOT_kivonat.tsv+Karoli_1908.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z · scope=range:1Kir 18:24, range:1Kir 18:25, range:1Kir 18:26 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | ts=2026-10-20T10:08Z | csatorna=cli*
```

### A2 — A kívülálló elvárása (10. összefüggés) · Peshat · (a 2Kir 5:11 nem a nyolc közül való; a brief 2. szakasza szerint)

```markdown
**A kívülálló elvárása (2Kir 5:11).** Naámán azt várta, hogy a próféta „kijő hozzám, és előállván, segítségül hívja az Úrnak, az ő Istenének nevét, és kezével megilleti a beteg helyeket”; a vers azzal kezdődik, hogy Naámán ezért megharagudott és elment. Az előfordulás funkciója a táblában: „ismétlődés, kívülálló szemszögéből”.

Értelmezés (Peshat): egy kívülálló számára a segítségül hívás látható, várt mozdulat — a próféta előáll, hív és kezet tesz —, és a történet éppen ezt az elvárást nem teljesíti.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=elofordulasok.tsv (funkcio)+Karoli_1908.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z · scope=range:2Kir 5:11 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | ts=2026-10-20T10:08Z | csatorna=cli*
```

### A3 — A liturgikus hármas (7. összefüggés) · Peshat · lefedi: 1Krón 16:8, Zsolt 105:1

```markdown
**A liturgikus hármas (1Krón 16:8; Zsolt 105:1; Ézs 12:4).** A „hálát ad, dicsér” ige (יָדָה, jádáh, H3034) a motívum 32 helye közül pontosan háromban áll: 1Krón 16:8, Zsolt 105:1, Ézs 12:4. A három vers kísérő szavai a gerincen (H7121, H8034) és az Úr nevén (H3068) kívül ugyanazok: hálát ad (H3034), ismer/megismertet (H3045), tett (H5949), nép (H5971). Az 1Krón 16:8 és a Zsolt 105:1 tartalmi szókészlete teljesen azonos (4/4), az Ézs 12:4 ehhez négy további szót tesz (4/8). A Károli a hálaadás igéjét mindhárom helyen másként fordítja: „Dícsérjétek”, „Magasztaljátok”, „Adjatok hálát”.

Értelmezés (Peshat): a két első versben a formula egy rögzült, háromtagú felszólítás része — hálaadás, a név segítségül hívása, Isten tetteinek hirdetése a népek között. Az Ézs 12:4-ben ugyanez a hármas áll, de ott a hívás igéjét a görög fordítás, a BSB és a Károli is másként adja vissza (l. 7. Módszertan).

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAHOT_kivonat.tsv+grammatikai_strongok.tsv+Karoli_1908.tsv (naplok/F126_meres.py, split('\t'); tartalmi szó: grammatikai_strongok és H9xxx nélkül) | ts=2026-10-20T10:11Z · scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H7121+H3034 | n=5 | ts=2026-10-20T10:08Z | csatorna=cli*
```

### A4 — ApCsel 9:21 · Peshat · lefedi: ApCsel 9:21

*Eltérés a felméréstől: a felmérés az ApCsel 9:21-et a 9. összefüggéssel („mindenki, aki”) fedte le. A saját mérés szerint a vers πάντες szava a hallgatókra vonatkozik, nem a hívókra (`naplok/F126_meres.md`, 9. sor), ezért a 9. összefüggés erre a helyre nem áll. A bekezdés a hely saját szövegéből indul.*

```markdown
**ApCsel 9:21.** A vers az ApCsel 9:14 megnevezését ismétli meg, más beszélő szájából. A 9:14 a megszólított Úrhoz szól („kik a te nevedet segítségül hívják”); a 9:21-ben a hallgatók beszélnek harmadik személyben arról, aki üldözte „azokat, a kik ezt a nevet hívják segítségül”. A vers „mindnyájan” szava (πάντες, pantesz) a hallgatókra vonatkozik („Álmélkodnak vala pedig mindnyájan, a kik hallák”), a hívókra nem: ők itt kvantor nélkül, „ezt a nevet” megjelöléssel állnak.

Értelmezés (Peshat): a formula itt külső megnevezés — a kívülállók ezzel jelölik azt a csoportot, amelyet üldözője el akart hurcolni. Ezen túl a hely a 9:14 ismétléseként tartozik a motívumhoz (Párhuzam, magas bizonyosság); további értelmezést a szöveg nem kínál.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAGNT_kivonat.tsv+Karoli_1908.tsv+kapcsolatok.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z · scope=range:ApCsel 9:14, range:ApCsel 9:21 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | ts=2026-10-20T10:08Z | csatorna=cli*
```

---

## B — Remez (az `ertelmezes` rés, a Lexikai kiegészítés után, a Drash előtt)

### B0 — bevezető sor

```markdown
**Remez — a motívum közepe【NAPLO: F126, 2026-10-20 — a próza-felmérés 1., 2., 6., 8., 9. és 12. összefüggése, saját méréssel: naplok/F126_meres.md】:** az alábbi felismerések a Peshat-kiegészítés helyeit kötik a motívum többi helyéhez. Ahol két hely közös szókészlete áll egymás mellett, az közös szókészlet, nem idézés és nem szándékos utalás.
```

### B1 — Hívás és felelet: Kármel és Zakariás (1. összefüggés) · Remez · lefedi: 1Kir 18:26 (a 18:24, 18:25 mellett)

```markdown
**Hívás és felelet.** A „felel” ige (H6030) és a „tűz” (אֵשׁ, és, H0784) a motívum 32 helye közül csak a Kármel-jelenetben (1Kir 18:24–26) és a Zak 13:9-ben áll. A görög fordítás Isten válaszára mindhárom helyen ugyanazt az igét adja (ἐπακούω, epakúó: 1Kir 18:24, 18:26, Zak 13:9); a nép válaszára az 1Kir 18:24-ben más igét (ἀποκρίνομαι, apokrinomai).

Értelmezés (Remez): a két hely közös szókészlete (hív, felel, tűz) egymás mellé állítja őket. A Kármelen a felelet a próba eldöntése; Zakariásnál ígéret a tűzben megtisztított maradéknak: „ő segítségül hívja az én nevemet és én felelni fogok néki”. A két hely között a motívum kapcsolat-táblája nem rögzít kapcsolatot, és a közös szókészlet nem bizonyít utalást.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAHOT_kivonat.tsv+Karoli_1908.tsv+kapcsolatok.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z · scope=range:1Kir 18:24, range:1Kir 18:26, range:Zak 13:9 | forras=LXX_OS/1-kings.tsv, LXX_OS/zechariah.tsv+TAGNT_kivonat.tsv | ts=2026-10-20T10:07Z–10:08Z | csatorna=cli*
```

### B2 — Két oltár (8. összefüggés) · Remez (Drash felé, a szöveg saját mércéjéig) · lefedi: 1Kir 18:26

```markdown
**Két oltár.** Az „oltár” (מִזְבֵּחַ, mizbéah, H4196) a motívum 32 helye közül négyben áll: a pátriárkák három oltáránál (1Móz 12:8; 13:4; 26:25) és a Kármelen, ahol Baál prófétái „sántikáltak az oltár körül, a melyet készítettek” (1Kir 18:26).

Értelmezés (Remez): a külső forma — oltár és a név segítségül hívása — a pátriárkáknál és Baál prófétáinál ugyanaz; a két helycsoportot a megszólított név választja el. Tanulságként csak annyi mondható, amennyit a szöveg maga kimond: a próba mércéje az, „a mely isten tűz által felel” (1Kir 18:24), nem a hívás formája.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAHOT_kivonat.tsv+Karoli_1908.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z · scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H7121+H4196 | n=18 | ts=2026-10-20T10:08Z | csatorna=cli*
```

### B3 — Hívás és megmenekülés (2. összefüggés) · Remez · lefedi: Zsolt 116:4

```markdown
**Hívás és megmenekülés.** A Zsolt 116:4-ben a segítségül hívás tartalma egy kérés: „Kérlek Uram, szabadítsd meg az én lelkemet!” A „megment, megmenekül” ige (מָלַט, málat, H4422) a motívum 32 helye közül csak itt és a Jóel 2:32-ben áll („mindaz, a ki az Úrnak nevét hívja segítségül, megmenekül”). A görög oldalon a szál másik szón fut: a Jóel 2:32 görög szövege a σῴζω (szódzó) igét adja, és ezt idézi az ApCsel 2:21 és a Róm 10:13; a Zsolt 116:4 görög fordítása viszont más igét használ (ῥύομαι, rhüomai).

Értelmezés (Remez): a hívás és a megmenekülés együttállása a személyes imában (Zsolt 116:4) és a közösségnek szóló ígéretben (Jóel 2:32) ugyanazzal a héber szóval áll; az újszövetségi idézetek a Jóel görög szövegéhez kapcsolódnak, a zsoltárhoz nem. A három lépés — személyes ima, prófétai ígéret, újszövetségi idézet — egymás mellé állítása felismerés, nem egyetlen szón végigfutó lánc.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv+Karoli_1908.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z · scope=range:Zsolt 116:4 | forras=LXX_OS/psalms-lxx.tsv+TAGNT_kivonat.tsv | n=11 | ts=2026-10-20T10:08Z | csatorna=cli · scope=range:Jóel 2:32 | forras=LXX_OS/joel.tsv+TAGNT_kivonat.tsv | n=28 | ts=2026-10-20T10:08Z | csatorna=cli*
```

### B4 — Zsolt 116:13 · nincs új anyag · lefedi: Zsolt 116:13

```markdown
**Zsolt 116:13.** A vers a formula második előfordulása ugyanabban a zsoltárban: „A szabadulásért való poharat felemelem, és az Úrnak nevét hívom segítségül.” Kísérő szavai közül a „szabadulás” (H3444), a „pohár” (H3563) és a „felemel” (H5375) a motívum 32 helye közül csak itt áll; a Jóel 2:32 „szabadulás” szava más héber szó (H6413). A hely a zsoltáron belüli ismétlés révén tartozik a motívumhoz (Zsolt 116:4 → 116:13 → 116:17); a motívum többi helyéhez az adat új összefüggést nem ad, ezért a próza itt nem értelmez tovább.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAHOT_kivonat.tsv+Karoli_1908.tsv+kapcsolatok.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z*
```

### B5 — Ismerni és nem ismerni: a népek tengelye (6. összefüggés) · Remez · lefedi: 1Krón 16:8, Zsolt 105:1 (a Zsolt 79:6, Jer 10:25 mellett)

```markdown
**Ismerni és nem ismerni.** Az „ismer” ige (יָדַע, jáda, H3045) a motívum 32 helye közül ötben áll. A három liturgikus versben (1Krón 16:8; Zsolt 105:1; Ézs 12:4) a Károli „hirdessétek” fordítással adja, a Zsolt 79:6-ban és a Jer 10:25-ben „nem ismernek” fordítással. A népeket a liturgikus versek az עַם (am, H5971), a két vádló vers a גּוֹי (gój, H1471) szóval nevezik.

Értelmezés (Remez): ugyanaz a szópár — ismerni és segítségül hívni — az egyik csoportban küldetés (a népek között kell megismertetni Isten tetteit), a másikban vád (a nemzetek nem ismerik, és nem hívják segítségül a nevét). A Sof 3:9-ben a népek (H5971) maguk a hívók: „hogy mind segítségül hívják az Úr nevét”; az „ismer” ige ott nem áll, ezért a Sof 3:9 e két csoport mellé állítása felismerés, nem szóadat.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAHOT_kivonat.tsv+Karoli_1908.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z · scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H7121+H3045 | n=37 | ts=2026-10-20T10:08Z | csatorna=cli*
```

### B6 — „Mindaz, a ki” (9. összefüggés) · Remez · (a nyolc helyből egyet sem fed le; a brief 2. szakasza szerint benne van)

```markdown
**„Mindaz, a ki”.** A hívókra vonatkozó „mind” az ószövetségi helyek közül a Jóel 2:32-ben („mindaz, a ki”) és a Sof 3:9-ben („mind”) áll (כֹּל, kol, H3605), az újszövetségiek közül öt helyen (πᾶς, pász: ApCsel 2:21; 9:14; Róm 10:12; 10:13; 1Kor 1:2). A genezisi helyeken a hívó egyetlen személy (Károli: „segítségűl hívá”, 1Móz 12:8; 13:4; 21:33; 26:25).

Értelmezés (Remez): a formula egyes szereplők gyakorlatából a „mindaz, a ki segítségül hívja” képletévé tágul; a Róm 10:12 ezt kifejezetten zsidóra és görögre mondja ki (l. fent, 3.).

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv+Karoli_1908.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z*
```

### B7 — Hit, hirdetés, hívás (12. összefüggés) · Peshat és Remez · lefedi: Róm 10:14

```markdown
**Róm 10:14.** A vers a 10:13 Jóel-idézetét kérdéssorral folytatja: „Mimódon hívják azért segítségül azt, a kiben nem hisznek? Mimódon hisznek pedig abban, a ki felől nem hallottak? Mimódon hallanának pedig prédikáló nélkül?” A versben a „segítségül hív” (ἐπικαλέομαι, epikaleomai) mellett a „hisz” (πιστεύω, pisztueó) és a „hall” (ἀκούω, akúó) kétszer, a „hirdet” (κηρύσσω, kérüsszó) egyszer áll. Szövegi adat: a TAGNT szerint a „hívják segítségül” alak (ἐπικαλέσωνται), valamint a „hisznek” és a „hallanának” alakja hat kiadásban áll (NA28, NA27, Tyndale House, SBL, Westcott–Hort, Tregelles), a Textus Receptus és a bizánci szöveg nélkül; az utóbbiak alakját a repó adata nem tartalmazza.

Értelmezés (Peshat): a kérdéssor visszafelé halad: a hívás előtt a hit, a hit előtt a hallás, a hallás előtt a hirdető áll. Értelmezés (Remez): így a Jóel-ígéret („minden, a ki segítségül hívja az Úr nevét, megtartatik”, 10:13) egy sor utolsó tagja lesz, amelynek első tagja a hirdető.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=TAGNT_kivonat.tsv (Kritikai kiadás)+Karoli_1908.tsv+kapcsolatok.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z · scope=range:Róm 10:14 | forras=Karoli_1908.tsv+Karoli_kereszthivatkozasok.tsv | ts=2026-10-20T10:08Z | csatorna=cli*
```

---

## C — Módszertan (a `modszertan` rés)

### C1 — Négy forrás egybeesése a határeseteken (11. összefüggés) · módszertan

```markdown
**Négy forrás egybeesése a határeseteken【NAPLO: F126, 2026-10-20 — a próza-felmérés 11. összefüggése, saját méréssel: naplok/F126_meres.md】.** A 2Móz 33:19-ben és a 34:5-ben négy forrás jelöli ugyanazt az eltérést a motívum többi helyétől: a BDB a 3. jelentéshez sorolja („kihirdetni”; a többi hely 2.c), a görög fordítás a καλέω (kaleó) igét adja (a 22 ószövetségi hely közül 18-ban ἐπικαλέομαι áll), a BSB „proclaim”-et ír (a többi helyen a „call” valamely alakját, az Ézs 12:4 kivételével), a Károli „kiált”-ot (csak e két helyen). Az Ézs 12:4-ben három forrás tér el: a görög fordítás βοάω (boaó), a BSB „proclaim”, a Károli „magasztaljátok”; a BDB viszont 2.c-t ad. A B-eset határa tehát nem egyetlen szótári besoroláson áll: négy fordítói és szótári forrás ugyanazt a két verset különíti el, az Ézs 12:4 átmeneti eset. Korlát: a négy forrás egybeesése mért, a függetlenségük nem (a BSB fordítóinak szótárhasználatát a repó adata nem mutatja), ezért ez egybeesés, nem független megerősítés. A βοάω nem csak az Ézs 12:4 görög szövegében áll: az 1Kir 18:24-ben a Baál-hívók felszólítását is ez adja, Illés saját hívását ott az ἐπικαλέομαι, ezért a vers az egyező helyek között van.

*Proveniencia: scope=adat/elofordulasok.tsv (id=ISTENTISZT-001, n=32) | forras=elofordulasok.tsv (jelentes_szam, karoli_szo)+BSB_Strongs.tsv+Konyv_normalizalo_tabla.tsv+lxx_dontesek.tsv (naplok/F126_meres.py, split('\t')) | ts=2026-10-20T10:11Z · scope=range:<a 22 ószövetségi hely> | forras=LXX_OS/*.tsv+TAGNT_kivonat.tsv | ts=2026-10-20T10:07Z–10:08Z | csatorna=cli (23 sor: naplok/F126_lekerdezesek.tsv; összesítés: naplok/F126_lxx_osszesit.py)*
```

---

## Mérce-tábla — a 8 meg nem nevezett hely

| Hely | Teljesítés | A mondat, amely teljesíti |
|---|---|---|
| 1Kir 18:25 | megalapozott értelmezés (Peshat) | A1: „A 18:25-ben Baál prófétái kapják a felszólítást …” + „Értelmezés (Peshat): a jelenetben a segítségül hívás választ váró kérés …” |
| 1Kir 18:26 | megalapozott értelmezés (Peshat, Remez) | A1: „A »felel« ige … a 18:26-ban kétszer áll …”; B1: „A Kármelen a felelet a próba eldöntése …”; B2: „a két helycsoportot a megszólított név választja el” |
| 1Krón 16:8 | megalapozott értelmezés (Peshat, Remez) | A3: „a két első versben a formula egy rögzült, háromtagú felszólítás része …”; B5: „az egyik csoportban küldetés …” |
| Zsolt 105:1 | megalapozott értelmezés (Peshat, Remez) | A3 és B5, mint fent |
| Zsolt 116:4 | megalapozott értelmezés (Remez) | B3: „a hívás és a megmenekülés együttállása a személyes imában (Zsolt 116:4) és a közösségnek szóló ígéretben (Jóel 2:32) ugyanazzal a héber szóval áll …” |
| **Zsolt 116:13** | **nincs új anyag** — a próza kimondja | B4: „a motívum többi helyéhez az adat új összefüggést nem ad, ezért a próza itt nem értelmez tovább.” |
| ApCsel 9:21 | megalapozott értelmezés (Peshat); a formai rész kimondva | A4: „a formula itt külső megnevezés …” + „Ezen túl a hely a 9:14 ismétléseként tartozik a motívumhoz …; további értelmezést a szöveg nem kínál.” |
| Róm 10:14 | megalapozott értelmezés (Peshat, Remez) | B7: „a kérdéssor visszafelé halad …” + „a Jóel-ígéret … egy sor utolsó tagja lesz …” |

Eredmény: 7/8 megalapozott értelmezés (az ApCsel 9:21-nél a formai tartozás is kimondva), a Zsolt 116:13-nál a próza kimondja, hogy nincs új anyag (elfogadási feltétel 1.).

## Külön sorok

| Tétel | Eredmény | Javaslat |
|---|---|---|
| **N-F55d** (Zsolt 79:6, 99:6 G1941) | a „22 ószövetségi igehely közül 18” **megerősítve**: a 22 helyből 18-ban áll G1941 a mai `LXX_OS`-en, a Zsolt 79:6 is köztük; a négy kivétel pontosan a megnevezett négy, mind a négynek van `lxx_dontesek.tsv`-sora (LD001–LD004). A Zsolt 99:6 (nem előfordulás) LXX-ében G1941 ×2 | a forrásban nincs javítás; **az N-F55d lezárása** a zárásnál. *(proveniencia: a 23 `lxx-hid` sor, `naplok/F126_lekerdezesek.tsv`, ts=2026-10-20T10:07Z–10:08Z)* |
| **Róm 10:14** (TR/Byz) | a G1941 ἐπικαλέσωνται, a G4100 πιστεύσωσιν és a G0191 ἀκούσωσιν csak hat kiadásban áll (TR, Byz nélkül); a TR/Byz alak nincs a kivonatban. Az eltérés a motívum szavát érinti → B7 csak a mért tényt mondja ki | **az N61 nyitva marad** (a TR/Byz alak forrásból való megállapítása nem e feladaté). A brief ezt „N-F126c”-nek nevezi; a main-en a végleges száma N61. *(proveniencia: `naplok/F126_meres.py`, ts=2026-10-20T10:11Z)* |
| **Seól-határ (A4)** | a szövegjavaslat a Zsolt 116:3-at **nem érinti** (B3 csak a 116:4-ről szól) | nincs jelölendő pont; az A4 a felhasználóé, nyitott |
| **N-F126a (új, javaslat)** — két lefedetlen A-mintájú vers | a H7121+H8034 kollokáció 196 verséből a **Zsolt 99:6** („Sámuel az ő nevét segítségül hívókkal egybe … és meghallgatá őket”; a versben H6030 is) és az **Ézs 64:6** (Károli; „S nem volt, a ki segítségül hívta volna nevedet”) sem előfordulás, sem jelölt | **kérdés hozzád:** felvegyem-e N-F126a helyőrzővel a `NYITOTT_FELADATOK.md`-be (a zárás commitjában)? A próza nem szól róluk; a két vers jelöltként, döntéssel kerülhet be (2. szabály), külön feladatban. *(proveniencia: `scope=TAHOT-teljes+TAGNT-teljes \| forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv \| strong=H7121+H8034 \| n=196 \| ts=2026-10-20T10:13Z \| csatorna=cli` + `naplok/F126_lefedetlen.py`)* |

## Eltérések a felméréstől és a brieftől (tájékoztatás)

1. **ApCsel 9:21:** nem a 9. összefüggéssel, hanem a saját szövegéből (A4); a felmérés 9. összefüggése a 9:21-re nem áll (a πάντες a hallgatókra vonatkozik).
2. **2. összefüggés:** a felmérés „láncot” javasolt (személyes ima → közösségi ígéret → evangélium); a mérés szerint a héber és a görög szál más-más szón fut, ezért B3 a láncot felismerésként, kimondott korláttal adja.
3. **6. összefüggés:** a „Sof 3:9 mindkettőt feloldja” helyett B5 csak az együttállást mondja ki (a Sof 3:9-ben az „ismer” ige nem áll).
4. **11. összefüggés:** a „független” jelző helyett „egybeesés”, kimondott korláttal (C1).
5. **12. összefüggés:** a felmérés „Remez, Drash felé” szintet javasolt; B7 Peshat és Remez, Drash nélkül (a hirdetésre vonatkozó tanulság túlmegy a vers adatán).
6. **Commit-számozás:** a brief a beírást `F126.1`, az újragenerálást `F126.2` jelöléssel írja; az ágon a mérés már `F126.2` (a lépés-számot követi), ezért a beírás `F126.5`, az újragenerálás `F126.6` lesz.

## Ami a jóváhagyás után következik (5–6. lépés)

5. A jóváhagyott bekezdések beírása a forrásba a fenti pontokra, változtatás nélkül (commit: `F126.5`).
6. `python eszkozok/general.py --cel lexikon` (ISTENTISZT-001); várt diff: csak a lexikonoldal „6. Értelmezés” és „7. Módszertan” szakasza; `python eszkozok/ellenoriz.py`, `python eszkozok/feladatok.py ellenoriz` (commit: `F126.6`). Utána a független ellenőrzés (7.) és a zárás (8.).
