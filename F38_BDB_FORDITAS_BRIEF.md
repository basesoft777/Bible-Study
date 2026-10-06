---
feladat: 38
cim: A teljes BDB héber szótár magyar fordítása, megállási pontokkal
kod: BDB_FORDITAS
tipus: feladat
fazis: 1
modell: sonnet
allapot: dontesre_var
ag: claude/f38-adag6
pr: https://github.com/basesoft777/Bible-Study/pull/228
lezarva_osszegzes: "A 6. adag (sorrend 407–648, 242 szócikk) lefordítva és rögzítve; kapuk RENDBEN, ellenoriz.py SÉRTÉS 0; döntésre vár: DT-F38j."
ad: a BDB_teljes_unabridged.tsv mind a 8 090 szócikkének teljes magyar fordítása az adat/forditasok.tsv-ben (allapot=sonnet; az 1–4. adagra is, DT-F38e), gyakorisági sorrendben, adagonként commitolva; ami a futás leállításáig nem készül el, angol marad
kovetkezo: "Te: a (d) feladat befogadása és lezárása (`beerkezo/F38d_SZELLEM_TESZT_JAVITAS_BRIEF_TERVEZET.md`, DT-F38j (d)); utána a 7. adag (sorrend 649–) a claude/f38-adag7 ágon."
olvas: [konkordancia/BDB_teljes_unabridged.tsv, adat/forditasok.tsv, adat/terminologia.tsv, adat/SEMA.md, eszkozok/emeles.py, eszkozok/normalizal.py, eszkozok/forditas_kapuk.py, konkordancia/Konyv_normalizalo_tabla.tsv, F28_EMELES_BRIEF.md, naplok/EMELES_naplo.md, DONTESEK.md, FELADATOK.md, konkordancia/Strong_szotar.tsv, konkordancia/TAHOT_kivonat.tsv]
ir: [adat/forditasok.tsv, naplok/BDB_FORDITAS_naplo.md, naplok/BDB_FORDITAS_sorrend.tsv, naplok/BDB_FORDITAS_hibas.tsv, DONTESEK.md, FELADATOK.md, konkordancia/Konyv_normalizalo_tabla.tsv, eszkozok/normalizal.py, eszkozok/teszt_normalizal.py, eszkozok/teszt_forditas_kapuk.py, beerkezo/BDB_KONYVFELOLDASI_AUDIT.md, eszkozok/forditas_kapuk.py, eszkozok/emeles.py, forditas/prompt_v4.md, naplok/BDB_FORDITAS_kapuk.py, naplok/BDB_FORDITAS_regresszio.py, naplok/FORDITAS_kisnagybetu_csere.tsv, naplok/BDB_FORDITAS_gyokcsoportok.tsv, naplok/BDB_FORDITAS_zaras2.py, naplok/BDB_FORDITAS_zaras3.py, naplok/BDB_FORDITAS_zaras_javitasok.tsv, eszkozok/teszt_bdb_zaras.py, NYITOTT_FELADATOK.md, naplok/ELLENOR_F38_zaras_2.md, naplok/ELLENOR_F38_zaras_3.md]
fugg: [34, 56]
---

# A teljes BDB magyar fordítása (BDB_FORDITAS)

**Módosítva (2026.10.02): a fordítás Sonnettel folytatódik.** Indoklás: az Opus-vakpróba (H2617, H7307) után a Sonnet-fordítás közelebb áll a Károli-stílushoz; az 1–4. adag (269 szócikk) is Sonneten futott. (DT-F38e)

*v1.2 · 2026.10.02 · zárómenet 3. kör (DT-F38g; a fejléc frissítve, a DT-sorok változatlanok) · v1.1 · 2026.10.02 · M0 5. pont (BDB-gyökcsoportok felmérése) · v1 · 2026.10.01 · a #28 (EMELES) tapasztalatai alapján · cloud session, Claude Code kredit (túlfutás esetén a heti keretből)*

## Cél

A BDB (Brown–Driver–Briggs) mind a 8 090 szócikke teljes, hű magyar fordításban, adatként. A #28 eszközláncát használja változatlanul: a prompt v4-et, a helyőrzős héber–görög védelmet, a javítóréteget, a kapukat és a terminológia v3-at a `kapu` oszloppal. Új eszközt nem fejleszt, csak futtat.

A futás bármelyik megállási pontnál leállítható. Ami addig elkészült, az commitolva megmarad; a többi angol marad (a 2026.09.30-i döntés szerint ez elfogadható).

## Előfeltétel

**Az F34 (BDB „ψ”-javítás) legyen kész és beolvasztva.** Hibás forrást nem fordítunk le. Ha a menet indulásakor az F34 még nincs a `main`-en, a végrehajtó ne induljon el, csak jelezze.

## Számok és becslés

| | Szócikk | Forrás (karakter) |
|---|---|---|
| Teljes BDB | 8 090 | 6,40 millió |
| ebből 2 000 karakter fölött | 626 | – |
| ebből 20 000 karakter fölött | 11 | max. 45 ezer |
| A #28 39 szócikke (összevetéshez) | 39 | 0,17 millió |
| Már kész héber szócikk (#28), kimarad | 26 | 0,13 millió |
| **Fordítandó** | **8 064** | **kb. 6,27 millió** |

**Költségbecslés (durva):** kb. 120–300 USD a teljes BDB-re. A tartomány oka, hogy a héber szöveg tokenizálása és a session rezsije (fájlolvasás, kapufuttatás, a kontextus újraolvasása) csak méréssel pontosítható. A kimenet (kb. 2,5–3 millió token magyar szöveg) adja a költség nagyobb részét. A #28-nál drágább volt a karakterenkénti ár, mert ott sok volt a döntési és ellenőri kör; itt ilyen nincs.

**Az M1 mérő adag után ezt a becslést pontosítjuk:** a felhasználó leolvassa a kreditet az adag előtt és után, és abból számolunk.

## Sorrend

A szócikkek a Károli Ószövetségben mért **Strong-gyakoriság szerint csökkenő** sorrendben fordulnak, hogy ha a futás korán leáll, a legtöbbet használt szavak készen legyenek. A ritka szavak és a tulajdonnevek a végére kerülnek.

A gyakoriságot az M0 számolja egy Strong-címkés ószövetségi szövegből a `konkordancia/` alól (közkincs vagy nyílt licencű forrásból; melyiket használta, írja a naplóba). Egyenlő gyakoriságnál a Strong-szám a sorrend.

## Lépések

### M0 — Felmérés (csak olvas)

1. Ellenőrzi, hogy az F34 a `main`-en van, és a 13. kapu csak a jóváhagyott F34-maradékon és az N-F34c körén jelezhet. Ha nem, megáll és jelez. *(Javítva 2026.10.01, DT-F38 (b): az eredeti „a 13. kapu a forráson 0 jelzést ad” feltétel hibás volt, mert az F34 a ψ-hiba B/R maradékát a DT-F34b/c szerint szándékosan hagyta meg; a mért 91 jelző szócikk — 83 F34-maradék, 8 N-F34c — a futást nem állítja meg.)*
2. Elkészíti a `naplok/BDB_FORDITAS_sorrend.tsv`-t: `sorszam`, `strong`, `gyakorisag`, `karakter`, `adag`. A már lefordított szócikkek (az `adat/forditasok.tsv` `teljes` sorai) kimaradnak.
3. Kijelöli a 20 000 karakter fölötti szócikkek szegmenshatárait (jelentésszámok mentén, ahogy a #28 a G4151-nél és a H1121-nél tette).
4. Adagokra osztja a listát: **M1 mérő adag kb. 150 000 karakter**, utána **adagonként kb. 500 000 karakter** (kb. 13 adag).
5. **BDB-gyökcsoportok felmérése (csak mérés, import nélkül; kiegészítés 2026.10.02).** Forrás: `openscriptures/HebrewLexicon`, `LexicalIndex.xml`, commit `21c9add1` (CC BY 4.0; GitHubról letölthető, a cloud proxyn átmegy). A BDB gyökcsoportjai (1 432 gyök, 4 616 Strong a bcv-commons `bdb_roots` mérése szerint) összevetése a `konkordancia/Strong_szotar.tsv` TWOT-számával: hány héber Strong-nál ad a BDB-gyök olyan rokon Strong-ot, amely nem ugyanazon TWOT-szám alatt áll. Kimenet: `naplok/BDB_FORDITAS_gyokcsoportok.tsv` (`strong`, `bdb_gyok`, `twot`, `bdb_rokonok`, `twot_rokonok`, `csak_bdb`), és az M0 jelentésébe három szám: a lefedett Strong-ok száma, a `csak_bdb` többletet kapó Strong-ok száma és aránya. A fájl neve, commitja és licencsora a naplóba. **Nem kerül be** a `BDB_teljes_unabridged.tsv`-be, az `adat/forditasok.tsv`-be vagy a szerepmátrixba; a hasznosításáról (a szócikkek „rokon szavak” adata-e) a ⛔ M1 megállási ponton a felhasználó dönt.

### M1 — Mérő adag

Az első kb. 150 000 karakter lefordítása a #28 módszerével. A végén **megállási pont** (l. lent), a szokásos rövid jelentésen felül ezekkel:
- az adag szócikkszáma, karakterszáma, a kapuk eredménye;
- 5 véletlenszerűen választott szócikk Strong-száma különböző hosszúságból, hogy a felhasználó beleolvashasson (`naplok/BDB_FORDITAS_naplo.md`, forrás és fordítás egymás alatt).

**⛔ M1:** a felhasználó leolvassa a kreditet, és dönt: folytatás, prompt- vagy terminológiajavítás, vagy leállás.

Az M0 5. pontjának eredménye alapján itt dönt arról is, hogy a BDB-gyökcsoport bekerül-e a szócikkek adatai közé (új mező az `adat/forditasok.tsv`-ben vagy külön tábla, SEMA-bővítéssel) vagy a felmérés lezárul import nélkül; a döntés a `DONTESEK.md`-be kerül.

### M2 … Mn — Éles adagok

Adagonként kb. 500 000 karakter, a sorrend szerint. Minden adag végén megállási pont. A felhasználó „folytasd” üzenetére jön a következő adag, ugyanabban vagy új sessionben.

### Mz — Zárás (a felhasználó jelzésére, vagy ha a lista elfogyott)

1. A terminológiai javaslatok egy táblában (angol · magyar · előfordulás · hol), soronkénti jóváhagyásra. Az `adat/terminologia.tsv` csak jóváhagyás után változik.
2. Szúrópróba: 10 szócikk különböző hosszúságból és gyakoriságból, a naplóban egymás alatt.
3. A `naplok/BDB_FORDITAS_hibas.tsv` összesítése.
4. `DONTESEK.md` záró tétel, `FELADATOK.md` saját sor, menetzárás (független ellenőr, push, draft PR).

**⛔ Mz:** a terminológia és a szúrópróba jóváhagyása.

## Megállási pont (minden adag végén)

1. Az adag fordításai az `emeles.py rogzit` útján az `adat/forditasok.tsv`-be kerülnek, `allapot=sonnet` (~~`opus`~~ — a DT-F38e szerint), `modell` a tényleges modellnév (kötelező, nincs alapérték).
2. Lefut a teljes kapusor, az `ellenoriz.py` és a `futtat.py`. Piros esetén nem commitol, csak jelent (szabály, sor).
3. **Commit és push** az ágra. Commit-üzenet: `BDB_FORDITAS adag <n>: <szócikk> szócikk, <karakter> karakter`.
4. Rövid jelentés a chatnek (legfeljebb 8 sor): adag száma, szócikk, karakter, összesen kész / hátra (szócikk és karakter), kapuhibák száma, a hibás listára került szócikkek száma, a commit.
5. **Megáll, és vár.** A következő adag csak a felhasználó „folytasd” üzenetére indul.

A folytatáshoz elég ez a brief és a `naplok/BDB_FORDITAS_sorrend.tsv`: a következő adag az első olyan sorral kezdődik, amelynek Strong-számához még nincs `teljes` sor az `adat/forditasok.tsv`-ben. Új session indításakor a végrehajtó ebből tájékozódik, a korábbi beszélgetést nem kell összefoglalni.

## Szabályok a #28 tanulságaiból

- **Egy session = egy ág = egy PR.** Ezen az ágon más session nem dolgozik. Ha a felhasználó új sessiont nyit a folytatáshoz, az előző már nem pushol.
- **Minden adag után commit és push.** A scratchpadben semmi nem maradhat, ami kell.
- **Egy végrehajtó, egy kontextus.** Nincs subagent; a terminológia egységessége ezen múlik.
- **A prompt és a terminológia futás közben nem változik.** Javítás csak megállási ponton, a felhasználó jóváhagyásával; a már kész adagokat ez nem fordítja újra, csak ha a felhasználó kéri.
- **Kapuhiba:** egy önújrapróba; ha az sem megy át, a szócikk a `naplok/BDB_FORDITAS_hibas.tsv`-be kerül (strong, kapu, szegmens, ok), és a futás továbbmegy. Kapukalibrálás csak megállási ponton, jóváhagyással.
- **Forráshiba** (pl. lehetetlen igehely, mint a „Dán 22:14”): a fordítás hűen átveszi, a 13. kapu jelzése a naplóba kerül; a forrást ez a menet nem javítja.
- **Szent Szellem:** az isteni πνεῦμα / רוּחַ (Spirit of God, Holy Spirit) fordítása „Isten Szelleme”, „Szent Szellem”, „a Szellem” (2026.10.01-i döntés, terminológia v3).
- **Rövidítések:** a `Konyv_normalizalo_tabla.tsv` szerint (Siralmak = JSir, Ámós = Ámós; a „Sir” csak Sirák fia).
- **`kezi` sorhoz** a menet nem nyúl.
- **Shell:** magyar szöveget tartalmazó szkript fájlból fusson, ne heredocból.

## Nem cél

- A Thayer fordítása (külön feladat, ha lesz rá keret).
- Az éles `lexikon/` újragenerálása (F36).
- Forráshibák javítása a BDB-ben (az F34 ψ-hibán túl).
- A terminológia v3 módosítása futás közben.
- Új eszköz vagy kapu fejlesztése.

## Nyitó prompt

<!-- KOZVETLEN_FUTTATAS -->
Olvasd el a `BDB_FORDITAS_BRIEF.md`-t, és hajtsd végre az M0-t és az M1-et. Előbb ellenőrizd az előfeltételt (F34 a main-en); ha nem teljesül, ne indulj el, csak jelezd. A #28 eszközláncát (emeles.py, normalizal.py, forditas_kapuk.py, prompt v4, terminológia v3) változtatás nélkül használd. Az M1 végén a brief „Megállási pont” szakasza szerint commitolj, pusholj, jelents, és állj meg. Új ágon dolgozz a friss main-ről (`claude/bdb-forditas`); ezen az ágon más session nem dolgozik.
<!-- KOZVETLEN_FUTTATAS -->

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | A teljes BDB Opusszal, cloud kreditből; túlfutás a heti keretből | a #28 Opus-minősége meggyőző; a felhasználó vállalja a túlfutást (2026.10.01) | olcsó külső modell (a Gemini-próba minősége nem tetszett) |
| D2 | Megállási pont minden adag után: commit, push, jelentés, várakozás | a futás bármikor leállítható, semmi nem vész el | egyetlen, megállás nélküli futás |
| D3 | Gyakorisági sorrend (Károli ÓSZ Strong-gyakoriság) | korai leállásnál is a legtöbbet használt szavak készek | Strong-szám szerinti sorrend |
| D4 | M1 mérő adag (kb. 150 ezer karakter) ⛔-val | a 120–300 USD-s becslés csak méréssel pontosítható | becslés alapján azonnali éles futás |
| D5 | F34 (ψ-javítás) előfeltétel | hibás forrást ne fordítsunk le | fordítás most, javítás utólag |
| D6 | Kevés ⛔ (M1, Mz), a többi megállás csak „folytasd”-ra vár | a #28-ban a sok döntési kör vitte a költség és az idő nagy részét | minden adag után tartalmi ellenőrzés |
| D7 | Egy végrehajtó, subagent nélkül | egységes terminológia, egy kontextus (#28 tapasztalata) | párhuzamos subagentek |
| D8 (DT-F38d) | (a) az 5. adag a következő menetben indul (~~Opus-menetben~~ — a DT-F38e szerint Sonnettel); (b), (c), (d) igen, a zárómenetben végrehajtva. | felhasználói döntés, 2026.10.02; l. `DONTESEK.md` DT-F38d | — |
| D-új (DT-F38e) | a teljes BDB Sonnettel, a D1-et felülírja. | felhasználói döntés, 2026.10.02: az Opus-vakpróba (H2617, H7307) után a Sonnet szóhasználata közelebb áll a Károlihoz, és nincs benne szembeötlő félrefordítás; a Sonnet szabálykövetési hiányait kapuk és normalizáló pótolják; l. `DONTESEK.md` DT-F38e | a teljes BDB Opusszal (D1) |
| D9 (DT-F38e) | ~~Az 1–4. adagot Opus újrafordítja, új ágon (felhasználói döntés, 2026.10.02).~~ **Felülírva a D-új-vel** (a teljes BDB Sonnettel). | l. `DONTESEK.md` DT-F38e | — |
| D10 (DT-F38f) | (1) a gépi normalizáló-szabályok a #28 soraira is érvényesek (az `allapot` és a `modell` nem változik); (2) az 5. kapu a `spirit` kulcsnál a szellem/Szellem alakot és ragozott alakjaikat is elfogadja (kapuszabály; a H5307, H5414, H7760 kivétele megszűnt); (3) a Szellem-szabály: a BDB H7307 9. pontja nagybetűs, Isten által küldött rossz szellem, az emberi szellem és a szél kisbetűs, a kétséges marad és listára kerül; (4) a normalizáló a tartományos és a vershoz tapadt „N t.” alakot is kezeli; (5) ami a forrásban RV/AV/RVm után áll, angolul, szó szerint marad. | felhasználói döntés, 2026.10.02; l. `DONTESEK.md` DT-F38f | — |
| D11 (DT-F38f) | a „-szor/-szer/-ször” toldalék a szám kiejtett utolsó szava szerinti hangrendhez igazodik (4-szer, 5-ször, 33-szor). | felhasználói döntés, 2026.10.02 | egységes „-szor” |
| D-gyok | A BDB-gyökcsoportok csak felmérés az M0-ban, import nélkül; forrás az OpenScriptures `LexicalIndex.xml` (GitHub), nem a HF `bdb_roots` CSV | a TWOT-szám már gyökalapú csoportosítás a szerepmátrixban; a többlet mérés nélkül nem ismert; a GitHub-forrás a cloud sessionből is elérhető, a HF nem |
