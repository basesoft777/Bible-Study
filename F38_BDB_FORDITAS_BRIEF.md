---
feladat: 38
cim: A teljes BDB héber szótár magyar fordítása, megállási pontokkal
kod: BDB_FORDITAS
tipus: feladat
fazis: 1
modell: sonnet
allapot: megallt
ag: ccr-ecfe0c66-bujfae
pr: https://github.com/basesoft777/Bible-Study/pull/471
ad: a BDB_teljes_unabridged.tsv mind a 8 090 szócikkének teljes magyar fordítása az adat/forditasok.tsv-ben (allapot=sonnet; az 1–4. adagra is, DT-F38e), gyakorisági sorrendben, adagonként commitolva; ami a futás leállításáig nem készül el, angol marad
kovetkezo: "Te: a 98 N-F107b Strong újrafordítása (DT-F38l (1)), a 8. adag előtt: az 1. szelet kész (2026.10.25: H3068, H0834, H3605, H3808, H3588, H6213, H3117, H1004, H5971, H3027, 360 szakaszsor, 155 058 forrás-karakter, allapot=sonnet, a régi teljes sorok elavultak), a 2. szelet is kész (H1980, H7200, H9008, H4480, H0259, H5869, H3947, H7725, H7971, 416 szakaszsor, 153 463 forrás-karakter, allapot=sonnet), a többi ~76 Strong (a H8415 a DT290 (3) szerint a felhasználó jóváhagyására vár, a H2416 és H5315 a #28 Opus-menete); A 7. adag 7a, 7b, 7c és 7d szelete kész (2026.10.25: 7a 85 szócikk H6571–H6343 + H4725, 7b 92 szócikk H6453–H8096, 7c 102 szócikk H8438–H8065, 7d 37 szócikk H8084–H4581, szakaszonként, allapot=sonnet; a 8. kapu «-javítása DT-F38j; a H2809 `-os jelölése DT-F38k (2)); a H4912 rögzítve (F38.366, kapu-felülbírálás: 11_konyvek, DT-F38k); a 9. adag előtt a #67 kapuja (DT55); a 8. adagtól adagonként a Károli-lefedettség mérése, indulás csak ≥85%-nál (DT56, naplok/BDB_FORDITAS_karoli_lefedettseg.py)"
olvas: [konkordancia/BDB_teljes_unabridged.tsv, adat/forditasok.tsv, adat/terminologia.tsv, adat/SEMA.md, eszkozok/emeles.py, eszkozok/normalizal.py, eszkozok/forditas_kapuk.py, konkordancia/Konyv_normalizalo_tabla.tsv, F28_EMELES_BRIEF.md, naplok/EMELES_naplo.md, DONTESEK.md, FELADATOK.md, konkordancia/Strong_szotar.tsv, konkordancia/TAHOT_kivonat.tsv]
ir: [adat/forditasok.tsv, naplok/BDB_FORDITAS_naplo.md, naplok/BDB_FORDITAS_sorrend.tsv, naplok/BDB_FORDITAS_hibas.tsv, DONTESEK.md, FELADATOK.md, konkordancia/Konyv_normalizalo_tabla.tsv, eszkozok/normalizal.py, eszkozok/teszt_normalizal.py, eszkozok/teszt_forditas_kapuk.py, beerkezo/BDB_KONYVFELOLDASI_AUDIT.md, eszkozok/forditas_kapuk.py, eszkozok/emeles.py, forditas/prompt_v4.md, naplok/BDB_FORDITAS_kapuk.py, naplok/BDB_FORDITAS_regresszio.py, naplok/FORDITAS_kisnagybetu_csere.tsv, naplok/BDB_FORDITAS_gyokcsoportok.tsv, naplok/BDB_FORDITAS_zaras2.py, naplok/BDB_FORDITAS_zaras3.py, naplok/BDB_FORDITAS_zaras_javitasok.tsv, eszkozok/teszt_bdb_zaras.py, NYITOTT_FELADATOK.md, naplok/ELLENOR_F38_zaras_2.md, naplok/ELLENOR_F38_zaras_3.md, beerkezo/F38d_SZELLEM_TESZT_JAVITAS_BRIEF_TERVEZET.md, naplok/BDB_FORDITAS_gyokcsoport_meres.py, naplok/F38_zaras.md, naplok/ELLENOR_F38_adag6.md, naplok/ELLENOR_F38_adag6_2.md, naplok/BDB_FORDITAS_karoli_lefedettseg.py, naplok/EMELES_munka.tsv, naplok/BDB_FORDITAS_adag7_bontas.md, eszkozok/teszt_emeles.py]
fugg: [34, 56, 72, 73, 107, 128]
nem_fugg: [9, 11]
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

> **Szakaszonkénti út (#128, DT181 (b), DT285–e; 2026.10.21).** A 7. adag előtti újrafordító adagtól (a 98 N-F107b Strong,
> DT289) a BDB szakaszonként fordul: `emeles.py szakasz_elokeszit` (tokenes bemenet `⟪sorszam⟫` határtokenekkel,
> `forditas/prompt_v5.md`, 20 000 karakter fölött ≤ ~10 000 karakteres csoportok) → `szakasz_ellenoriz` (14. szakasz-kapu, 9.
> tagolás szakaszonként) → `szakasz_rogzit` → `szakasz_beir --regi-elavult` (`jelentes_szam = sz<sorszam>`; a régi `teljes`
> sor `elavult`). A 9 táblán kívüli Strong a régi úton (prompt v4, `rogzit` / `beir`). Séma: `adat/SEMA.md` 2.14; napló:
> `naplok/F128_BDB_SZAKASZ_ELOKESZITES_naplo.md`. A H8415 (`kezi`): újrafordul, a szakaszsorai `--kezi-marad`-dal kerülnek be, és
> csak a felhasználó jóváhagyása után kapnak `kezi`-t (DT290 (3)); az olvasók a közös összefűzőt használják (DT291 (a)).

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

## ⛔ Mj — a forrás tagolás-jelölői (a következő adag előtt; DT181, 2026.10.16)

*Felvéve a felhasználó kérésére, a #102 előzetes leletéből (`F102_BDB_SZELETELO_JAVITAS_BRIEF.md` 1a–1b., PR #359). Proveniencia:
`manual` (kézi szúrópróba és egyszeri, csak olvasó szkript a repón kívül, 2026.10.16).*

**A lelet.** A fordítás forrása, a `BDB_teljes_unabridged.tsv`, a `DictBDB.json` HTML-jének sima szöveggé alakított változata. A
tagolás-jelölők (jelentéspont, fő szakasz, gyakoriságszám) ebben már nincsenek meg; a `konkordancia/lexikonok_nyers/BDB.lexicon`
ugyanezt a szöveget jelölőkkel őrzi (`class="point"` 20 515, `class="section"` 913). A magyar fordítás ezért szintén jelölők nélküli.
A konverziós maradványokat a fordítás átviszi: az „N_M” alakú (gyakoriságszámmal tapadt) jelölő az angol TSV 9 szócikkében áll, ebből
7 már le van fordítva, és mind a 7 magyar szövegben szó szerint megmaradt (`2_46`, `3_39`); a „2 145:törzs” (H7626) forráshiba szintén.
A tapadt „N.szó” alakot a fordító részben szétválasztotta (EN 9 → HU 7 szócikk; H0559 „263.1Say” → „263. 1 Mondani”).

**Mi véd ma.** A tagolás-kapu (`eszkozok/forditas_kapuk.py`, „tagolas”) a forrás minden általa felismert jelölőjét sorrendben
megköveteli a fordításban. A jelentésszámok így a magyar szövegben is az angolt követik — de csak ott, ahol a sima szövegből a
jelölő felismerhető; ahol a szeletelő téved (#102 seed-101: 13 hely), ott a kapu sem lát jelölőt.

**Miért most.** A 8 099 szócikkből 674 kész (≈ 8%). A tagolás forrásáról a #102 1. lépése dönt (DT-F102d helyőrző, #102 1a.);
ha a jelölt forrásra vált, a magyar szövegnek is hordoznia kell a jelentéshatárokat, különben az angol és a magyar tagolás elválik.
Minél több adag készül el addig, annál drágább az utólagos illesztés vagy újrafordítás.

**Döntés (`DONTESEK.md` DT181):** l. ott az opciókat. A döntésig a következő adag nem indul.

**Eldöntve (2026.10.20, felhasználó, chat).** A DT181 szünete a DT231 (d) döntésével (2026.10.18) lejárt; a DT181 választása **(b)**:
a következő adagtól a fordító szakaszonként kapja a szöveget (`adat/bdb_szakaszok.tsv`, kulcs `strong` + `sorszam`), a szakaszhatár
változatlan tokenként megy át, és ugyanígy fordul újra a N-F107b 98 elakadó Strongja. A pe/mem kérdésben (`DONTESEK.md` DT269) **(1)**:
a bemenet a nyers szöveg a `hivatkozas` javításokkal (`nezet_general.py` `--pe-mem` nélkül); a pe/mem csere a TSV-cserével, egyben
a kész fordításokra is. A szakaszonkénti módhoz előkészítő feladat kell (#128, `F128_BDB_SZAKASZ_ELOKESZITES_BRIEF.md`);
**az adag addig nem indul** (fejléc: `allapot: megallt`). Károli-lefedettség (DT56) 2026.10.20: a következő 3 adagban 100%
(`naplok/BDB_FORDITAS_karoli_lefedettseg.py`, ts=2026-10-20 08:18).

## Átadás a #107-ből (2026.10.18)

*A #107 (BDB_JELOLT_SZOVEG) 8. lépése; a felhasználó döntése szerint (2026-10-18) egyeztetett eltérésként a #107 írja ezt a szakaszt —
csak a törzset, a fejlécet nem. Forrás: `naplok/F107_BDB_JELOLT_SZOVEG_naplo.md` 6.1, 7., 7.1.*

- **A kész fordítás szakaszhatárai:** `adat/bdb_szakasz_hu.tsv` (SEMA 2.32) — a 674 lefordított Strong 9 664 szakasza a szakasztábla
  (`adat/bdb_szakaszok.tsv`, SEMA 2.30) soraihoz illesztve; **szakaszkulcs: `strong` + `sorszam`** (a `bdb_id` + `utvonal` mellette; az
  útvonal-formátum nincs befagyasztva, DT190 🟡). A táblasor a fordítás `forras_hash`-ét is hordozza. Az `adat/forditasok.tsv`-t a #107 nem
  írta.
- **Mért számok** (Strong-szint, horgonnyal): illeszkedik **409**, horgonnyal **85**, elakad **98**, tagolatlan **82** (a 2026-10-16-i
  kiinduló, a kapu szigorú módszerével: 355 / — / 230 / 89; ugyanazzal a módszerrel a szakasztáblán ma 380 / — / 200 / 94). Soronként:
  illeszkedik 6 395, horgonnyal 202, elakad 606, jelölő nélküli 2 461.
- **DT232 (felhasználó, 2026-10-18):** „(d), majd (c)” — a magyar jelölő-felismerés bővítése megtörtént; **kézi illesztés nincs**; a
  maradék elakadó Strong a #38 **következő adagjában szakaszonként újrafordítandó**.
- **N-F107b:** a 98 Strong (606 elakadt szakasz) tételes listája: `naplok/F107_BDB_JELOLT_SZOVEG_naplo.md` **7.1** (Strong, `sorszam`:`utvonal`,
  jelölőtípus); `NYITOTT_FELADATOK.md` N-F107b.
- **DT231 (d) (felhasználó, 2026-10-18):** a `konkordancia/BDB_teljes_unabridged.tsv` **változatlan**; a 674 fordítás `forras_hash`-e addig a
  változatlan TSV-hez kötődik; a TSV cseréje a táblából generált nézetre (`eszkozok/bdb_jelolt/nezet_general.py`) és az olvasók átállása
  **külön, `/befogad`-dal felvett feladat** (a nézettel a fordítássorok 446–546 `forras_hash`-e változna).
- **N-F107a (pe/mem):** a `DictBDB.json` és belőle a TSV a dagesses pét dagesses memként írja; a 678 BDB-fordítássorban 2 782 dagesses mem,
  0 dagesses pe; a javítás a `adat/bdb_forras_javitas.tsv` `pe_mem` sorai (3 823 `javitva`) — a szakaszonkénti újrafordítás bemenete a
  javított nézet lehet (döntés a #38-ban / a TSV-csere feladatában).

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
- **Egy végrehajtó, egy kontextus.** Nincs subagent; a terminológia egységessége ezen múlik. (Megerősítve 2026-10-07: a párhuzamos, szilánkos futtatás elvetve, DT56.)
- **Szinkron a Károli–Strong párosítással (DT56, 2026-10-07).** Minden adag előtt: `python naplok/BDB_FORDITAS_karoli_lefedettseg.py`. Az adag csak akkor indul, ha a sorrendtartományának legalább 85%-a Károli-párt kap az adatblokkban; ha nem, a menet nem indul, és a `kovetkezo` a #22 következő könyvére mutat.
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
