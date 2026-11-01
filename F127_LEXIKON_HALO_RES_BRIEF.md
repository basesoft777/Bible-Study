---
feladat: 127
cim: A lexikon két hiányzó része — alkalmazási és tanítói rés, motívumközi kapcsolat (pilot: ISTENTISZT-001)
kod: LEXIKON_HALO_RES
tipus: feladat
fazis: 1
modell: opus
allapot: lezarva
pr: 452
lezarva_osszegzes: "két új rés (alkalmazas, tanitoi) a 8 lexikonoldalon 6/b.-ként, res_forras 56 → 72; motívumközi jelölt-út (jeloltek kulcsbővítés 627 → 634, új motivum_kapcsolatok.tsv 3 sorral, generált 5/b. blokk); DT276–f; ellenőrzés ELTÉRÉS 5 → 2 → 2 (alacsony súlyú, két javítókör, a zárás jóváhagyva); merge-feltétel: pardes.db helyi újraépítése és teszt_futtat.py; zárónapló naplok/F127_zaras.md"
ag: claude/lexikon-halo-res
munka: folyamat
ad: eldöntött és bevezetett út két, ma hiányzó lexikonrészhez, motívumfüggetlenül: (a) a forrás alkalmazási kérdései és a tanítói összegzés a lapon (új rés, réslista, generátor); (b) motívumközi kapcsolat jelölt → döntés → kapcsolat úton, „Kapcsolódó motívumok” megjelenítéssel; pilot az ISTENTISZT-001 négy jelölt-kapcsolatán (ALVIL-001 kétszer: az alpontjához és az egészéhez; HAMART-001; TEREMT-001)
kovetkezo: "Te: merge előtt a pardes.db helyi újraépítése (nem a /mnt/c-ről) és `python eszkozok/teszt_futtat.py` (teszt_olvaso_szerver, teszt_pilot_aranymintaval: ellenőrizetlen); nyitott: N-F127a, N-F127b"
olvas: [naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md, RENDER_BRIEF.md, adat/SEMA.md, adat/res_forras.tsv, adat/kapcsolatok.tsv, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/motivumok.tsv, motivumok/ISTENTISZT-001.md, motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md, "tematikus_lezart/ISTENTISZT-001*", "tematikus_lezart/naplok/ISTENTISZT-001*", archivum/ISTENTISZT-001/, lexikon/, archivum/ALVIL-001/Hadesz_Seol_tematikus.md, archivum/ALVIL-001/Hadesz_Seol_kereszthivatkozas_naplo.md, tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md, tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md, tematikus_lezart/Tehom_tematikus.md, tematikus_lezart/naplok/Tehom_kereszthivatkozas_naplo.md, "tematikus_lezart/ALVIL-001*", "tematikus_lezart/naplok/ALVIL-001*", "tematikus_lezart/HAMART-001*", "tematikus_lezart/naplok/HAMART-001*", "tematikus_lezart/TEREMT-001*", "tematikus_lezart/naplok/TEREMT-001*", "tematikus_lezart/naplok/ANTROP-001*", "tematikus_lezart/naplok/HODIT-001*", "tematikus_lezart/naplok/KIRALY-001*", "tematikus_lezart/naplok/MENNY-001*", "tematikus_lezart/*_tematikus.md", sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/7_PaRDeS_tanitoi_kereses_sablon.md, MUNKAMENET.md, F123_MIGRACIO2_BRIEF.md, F10_LEXIKON_LEZARAS_BRIEF.md, eszkozok/general.py, eszkozok/lexikon_general.py, eszkozok/ellenoriz.py, eszkozok/lekerdez.py, eszkozok/ellenorzes/e28_migralt_nezetek.tsv, motivumlog/lexikon_pilot/Motivum_kapcsolatok_PILOT.tsv]
ir: [adat/res_forras.tsv, adat/jeloltek.tsv, adat/SEMA.md, adat/motivum_kapcsolatok.tsv, eszkozok/lexikon_general.py, eszkozok/general.py, eszkozok/ellenoriz.py, eszkozok/torzscikk_general.py, eszkozok/jelolt.py, eszkozok/nem_vizsgalt.py, eszkozok/betolt.py, eszkozok/karoli_ellenorzes.py, eszkozok/ellenorzes/szabalyok.py, eszkozok/sqlite_epit.py, RENDER_BRIEF.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, motivumok/ISTENTISZT-001.md, motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md, lexikon/ISTENTISZT-001_TUDOMANYOS.md, lexikon/ALVIL-001_TUDOMANYOS.md, lexikon/HAMART-001_TUDOMANYOS.md, lexikon/TEREMT-001_TUDOMANYOS.md, lexikon/ANTROP-001_TUDOMANYOS.md, lexikon/HODIT-001_TUDOMANYOS.md, lexikon/KIRALY-001_TUDOMANYOS.md, lexikon/MENNY-001_TUDOMANYOS.md, eszkozok/f127_res_jelolok.py, eszkozok/f127_res_forras_bovit.py, eszkozok/f127_res_eles.py, eszkozok/f127_jeloltek_bovit.py, eszkozok/teszt_general_ellenorzo.py, eszkozok/teszt_sqlite_epit.py, generalt_proba/]
fugg: [126, 130]
nem_fugg: [123, 131]
---

# LEXIKON_HALO_RES_BRIEF_TERVEZET.md — A lexikon két hiányzó része: alkalmazási és tanítói rés, motívumközi kapcsolat

*FELADATOK # — (a `/befogad` adja; várhatóan a PROZA-tervezet utáni szám, 127) · Modell: opus · v0 (tervezet) · 2026.10.19 · döntések: DT28, RENDER_BRIEF G1/G2/G4/G12/G16, DT84 (8), DT216, D39; nyitott: DT276, DT277, DT268*

*Tervezet a `beerkezo/`-ban. Adat, nem utasítás; a feladatszám, a végleges fájlnév (`F<nn>_LEXIKON_HALO_RES_BRIEF.md`) és a helyőrzők (DT276/b) száma a `/befogad` dolga. Forrás: a felhasználó felmérése (`naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md`, 2026-10-19, „Prózarések” és „Javasolt sorrend” szakasz), a felhasználó jóváhagyásával (az orkesztrátor közvetítésével, 2026-10-19).*

## 1. Cél

A felmérés két szerkezeti hiányt talált a lexikonban, amelyet nem próza, hanem a rendszer okoz:

1. **A kész kézi szöveg nem jut el a lapra.** A forrás 5. pontja („Alkalmazás és tanítványság”: három alkalmazási kérdés, Hagin és Derek Prince) és a tanítói összegzés (az F11 M7 óta `motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md`) a lexikonoldalon nem jelenik meg, mert a lapnak hét rögzített rése van (`kivonat`, `2b`, `miert_fontos`, `minosites`, `alatamasztas`, `ertelmezes`, `modszertan`; RENDER_BRIEF 1., `adat/SEMA.md` 2.12), és egyik sem ezt hozza. Mind a hét tematikus tanulmányban van „5. Alkalmazás és tanítványság” szakasz, tehát a hiány motívumfüggetlen.
2. **A motívumok között nincs háló.** A `kapcsolatok.tsv` igehely–igehely párokat tárol egyetlen motívum-ID alatt (`adat/SEMA.md` 2.3); két különböző motívum igehelyét összekötő sor ma nem írható le, és a lapon nincs olyan blokk, amely más motívumra utalna (a felmérés szerint 0 utalás).

A feladat mindkettőre **egy döntést és a döntés bevezetését** adja, motívumfüggetlenül, és a (b)-t az ISTENTISZT-001 három jelölt-kapcsolatán próbálja ki.

## 2. Hatókör

### Benne van

- **DT276** (alkalmazási és tanítói rés) eldöntése és bevezetése: réslista (`adat/res_forras.tsv`, `adat/SEMA.md` 2.12 `res` értékkészlete, RENDER_BRIEF 1. „Fogalmak”), generátor (`eszkozok/lexikon_general.py`: a rés helye a `VAZ_SABLON`-ban, a tartalomjegyzék), ellenőrzés (`eszkozok/ellenoriz.py` 11. szakasz), lexikonsablon; a 8 éles lap `res_forras.tsv`-sora; az ISTENTISZT-001-nél a jelölők a forrásban.
- **DT277** (motívumközi kapcsolat) eldöntése és bevezetése: séma (`adat/SEMA.md`), a jelölt-út, a megjelenítés a generátorban.
- **Pilot:** az ISTENTISZT-001 jelölt-kapcsolatai a felmérés 3–5. összefüggéséből — jelöltként, döntéssel, a döntés után kapcsolatként, és a lapon megjelenítve. Az ALVIL-001-gyel **két külön jelölt** (a #123 Seól-határ-döntése (felhasználó, 2026-10-19: az ISTENTISZT-001 határa marad, a „kiáltás a Seól szorításából” az ALVIL-001 ↳ alpontja; DT-F123d, PR #436, `56046a40`; a végleges szám a befogadáskor)): (a) Zsolt 116:3 ↔ Zsolt 116:4, az ALVIL-001 „kiáltás a Seól szorításából” alpontjához kötve; (b) ApCsel 2:21 ↔ ApCsel 2:27, 31, az ALVIL-001 egészéhez. A HAMART-001 (1Móz 4. fejezet ↔ 4:26; 1Móz 12:3 ↔ 12:8) és a TEREMT-001 (Róm 10:7 ↔ 10:12–14) jelöltje változatlan.
- A CLAUDE.md „hét rése” mondatának frissítése, ha a DT276 a réslistát bővíti (a CLAUDE.md közös fájl, az `ir`-be nem kell).

### Nincs benne

- **Próza** a motívumközi kapcsolatokról: a jóváhagyott kapcsolat után külön, értelmező feladat (egy kéz, a másik motívum értelmezését is olvasva; a felmérés „Szabályok” táblájának K1-sora). Ez a feladat csak adatot és generált megjelenítést ad.
- **Szöveg írása az alkalmazási résbe:** a rés a meglévő kézi szöveget hozza; a szöveg nem változik (a RENDER_BRIEF G9 mintája: „a jelölők a meglévő szöveg köré kerülnek”).
- **A Seól-határ (A4)** eldöntve: a #123 Seól-határ-döntése (felhasználó, 2026-10-19: az ISTENTISZT-001 határa marad, a „kiáltás a Seól szorításából” az ALVIL-001 ↳ alpontja; DT-F123d, PR #436, `56046a40`; a végleges szám a befogadáskor). E feladat ezt nem nyitja újra, és az ALVIL-001 alpontját sem hozza létre (az a #123 ALVIL-001-ciklusáé); csak a kapcsolat célját köti hozzá, ha a DT277 így dönt.
- A Kármel–Zakariás visszhang (4. kérdés): motívumon belüli, nem motívumközi kapcsolat.
- A felmérés motívumfüggetlen felmérő eszköze (`eszkozok/motivum_felmeres.py`): a #123 2d. szakaszáé. A pilot a jelölteket saját lekérdezéssel méri, eszközt nem fejleszt.
- A 7 nem migrált motívum forrásának jelölése (l. DT276, javaslat): a #123 ciklusaiban.
- A törzscikk (`lexikon/[ID]_TORZSCIKK.md`): kivezetés alatt (D34), az ISTENTISZT-001-é archív (E28).

## 3. Nyitott döntések (⛔ 0.2; döntéshozó: a felhasználó, vagy az orkesztrátor a felhasználó felhatalmazásával)

### DT276 — alkalmazási és tanítói rés

**Kérdés:** kapjon-e a lexikonoldal új rést a forrás alkalmazási kérdéseinek és a tanítói összegzésnek; ha igen, hány rést, honnan generálódnak, hol állnak a lapon, és hogyan módosul a réslista?

**Mért helyzet** *(proveniencia: scope=adat/res_forras.tsv, motivumok/ISTENTISZT-001.md, motivumok/naplok/ISTENTISZT-001_tanitoi_kereses.md, tematikus_lezart/*_tematikus.md | forras=manual (grep `^## 5. Alkalmazás`, `RÉS-KEZDET`) | ts=2026-10-19)*:
- a `res_forras.tsv` 8 motívumot × 7 rést tart; `alkalmazas`/`tanitoi` rés nincs;
- az ISTENTISZT-001 forrásában az „5. Alkalmazás és tanítványság” szakasz rés-jelölőn kívül áll (a jelölők: `kivonat`, `miert_fontos`, `ertelmezes`, `modszertan`), az alkalmazási kérdések ott vannak, a tanítói egyezés csak hivatkozás a saját fájlra;
- a tanítói fájlnak van „4. Összegzés” szakasza;
- a 7 tematikus tanulmány mindegyikében van `## 5. Alkalmazás és tanítványság`.

**Opciók:**
1. **Nincs új rés.** A szöveg a forrásban marad, a lap nem mutatja; a hiány a lapon generált mondattal jelölt. Olcsó, de a kész kézi szöveg rejtve marad.
2. **Egy új rés (`alkalmazas`)**, forrása a motívum forrásának 5. pontja (jelölők a meglévő szöveg köré); a tanítói összegzés helyett generált hivatkozó mondat a saját fájlra.
3. **Két új rés: `alkalmazas` és `tanitoi`.** Az `alkalmazas` a forrás 5. pontjából, a `tanitoi` a tanítói fájl „Összegzés” szakaszából, mindkettő a meglévő jelölő-mechanizmussal (G1/G2), saját `res_forras.tsv`-sorral (a `tanulmany` mező a megfelelő fájl). Egy lap-szakaszban jelennek meg.
4. **Egy rés két forrásfájlból:** a `res_forras.tsv` `tanulmany` mezője több útvonalat fogad. Séma-változás a mezőben, a G2 „egy fájl, több jelölőpár” szabálya sérül.

**Részkérdések (mindegyik opciónál, ahol értelmes):**
- *Hely a lapon:* (i) új „6/b. Alkalmazás és tanítói egyezés *(kézi)*” szakasz a 6. Értelmezés után — a szakaszszámozás és a tartalomjegyzék-szöveg („12 szakasz”) a 8 lapon nem tolódik el, az „1/b.” mintájára; (ii) új 9. szakasz; (iii) a 6. Értelmezésen belül.
- *A 7 nem migrált motívum:* (i) a rés most mind a 8 lapon megnyílik; ahol a forrás még nincs jelölve, `forras=adat` rögzített mondattal („Az alkalmazási rész a motívum migrációjával kerül a lapra (#123).”), és a jelölőket a #123 X.M-ciklusa teszi a forrásba; (ii) a 7 tematikus tanulmányba most kerülnek jelölők (7 motívumfájl írása, ütközés a #123-mal, D39).
- *Törzscikk:* a rés ott nem jelenik meg (kivezetés alatt, D34).

**Javaslat: 3., a lap-hely (i), a 7 motívumra (i), törzscikkben nem.** Indok: a 3. a meglévő mechanizmust használja (G1/G2), a két kézi szöveg két külön forrásfájlban él, és mindkettő megmarad a saját helyén (DT28: a tanítói fájl a B9 saját fájlja, DT66 (a) 2.); a 4. sémát és a G2-t módosítaná; az 1. a kész szöveget elrejtené. A „6/b” nem tolja el a 8 lap szakaszszámait. A 7 motívum jelölése a #123 ciklusaiba kerül, mert ott úgyis minden blokk leképeződik (X.M1), és így ez a feladat nem ír 7 motívumfájlt.

**Ha a 3. elfogadva, a bevezetés:**
- a `res` értékkészlet bővül (`adat/SEMA.md` 2.12); a RENDER_BRIEF 1. „Fogalmak” mondata („Hét rögzített rés van”) kilencre módosul, hivatkozással erre a döntésre; a CLAUDE.md réslistás mondata ugyanígy;
- a `res_forras.tsv` 8 × 2 új sor: az ISTENTISZT-001-nél `tanulmany`, a többinél `adat` rögzített mondattal;
- az ISTENTISZT-001 forrásában `<!-- RÉS-KEZDET: alkalmazas -->` … `<!-- RÉS-VÉGE: alkalmazas -->` az alkalmazási kérdések köré, a tanítói fájlban `tanitoi` az Összegzés köré; **a szöveg nem változik** (bájt-összevetés a jelölők nélkül);
- a generátor és az `ellenoriz.py` 11. szakasza az új résekkel; a #123 X.M1-lépése (leképezési tábla) a két új rést is kezeli — ezt N-tétel rögzíti a #123-nak.

### DT277 — motívumközi kapcsolat

**Kérdés:** hol éljen a két motívum közötti kapcsolat (a `kapcsolatok.tsv`-ben vagy új táblában), milyen úton kerül be (jelölt → döntés → kapcsolat), és hogyan jelenik meg a lapon?

**Mért helyzet** *(proveniencia: scope=adat/kapcsolatok.tsv, adat/jeloltek.tsv, adat/elofordulasok.tsv, eszkozok/lexikon_general.py | forras=manual (split('\t') szkript; grep `jeloltek_sorok`) | ts=2026-10-19)*:
- a `kapcsolatok.tsv` kulcsa `forras_igehely + cel_igehely + id`, egyetlen motívum-ID-vel; az ISTENTISZT-001-nek 25 sora van; a `tipus` zárt (`Előkép | Párhuzam | Beteljesedés | Kontraszt | Variáns`, KAPCSOLATOK Típus-mező v1, 2026.09.09);
- az `adat/SEMA.md` 4. szakasza már rögzít egy névütközést: a `Motivum_kapcsolatok_PILOT.tsv` „Típus” oszlopa (`LEXIKAI`/`NARRATÍV`/`STRUKTURÁLIS`/`TEMATIKUS`) másik tengely, mint a `tipus`;
- a `jeloltek.tsv` kulcsa `id + igehely`, és jelentése: *a motívum lehetséges előfordulása*. A generátor 1/b. blokkja (`lexikon_general.py`, `jeloltek_sorok`) a motívum minden `elutasítva` és `nyitva` sorát kizárt vagy nyitott jelöltként rendereli;
- **kulcsütközés:** a pilot ISTENTISZT-001 oldali igehelyei mind beépített előfordulások a `jeloltek.tsv`-ben (pl. `ISTENTISZT-001 · Zsolt 116:4 · beépítve`); a másik motívum igehelyével kulcsolt sor (`ISTENTISZT-001 · Zsolt 116:3 · nyitva`) pedig a lap 1/b. blokkjában kizárt jelöltként jelenne meg — hamisan;
- a pilot másik oldala az `elofordulasok.tsv`-ben: ALVIL-001 · Zsolt 116:3, ApCsel 2:27, ApCsel 2:31; HAMART-001 · 1Móz 4:2-3, 4:7, 4:10-11, 4:12, 4:14, 12:3; TEREMT-001 · Róm 10:7.
- a `NYITOTT_FELADATOK.md` F6-tétele („Formula és Kapcsolódó motívum mező hiánya a `motivumok.tsv`-ben”) ugyanezt a hiányt a motívum-törzstábla felől jelzi.

**Opciók — tárolás:**
1. **A `kapcsolatok.tsv` változatlanul:** a motívumközi pár az egyik motívum ID-je alatt áll. A másik motívum nem tud róla, a `tipus` tengelye (Előkép…Variáns) a szomszédságot nem írja le. Nem alkalmas.
2. **A `kapcsolatok.tsv` bővítése** egy `cel_id` oszloppal (üres = motívumon belüli), és a `tipus` bővítésével. A 25+ meglévő sort és minden olvasóját (generátor, `ellenoriz.py`, `kapcsolatok`- és `alatamasztas`-blokk) érinti, a lezárt Típus-mezőt újranyitja.
3. **Új tábla: `adat/motivum_kapcsolatok.tsv`** (motívum–motívum, az alapul szolgáló igehely-párokkal). Javasolt mezők: `id_a`, `igehely_a`, `id_b`, `igehely_b` (kulcs: a négy együtt, rendezett párként), `tipus` (új, zárt tengely, pl. `szomszédos` — ugyanabban a fejezetben vagy beszédben áll, `közös_igehely`, `tematikus`; a végleges készlet a pilot után), `funkcio`, `bizonyossag`, `pardes_szint`, `indoklas`, `dontes_ref` (a jelölt sorra mutat), `proveniencia`. Szimmetrikus: mindkét motívum lapján megjelenik.

**Opciók — a jelölt útja (2. szabály: nincs közvetlen út):**
- (i) **a `jeloltek.tsv` egy új `jelolt_tipus` oszloppal** (`elofordulas` alapértelmezett | `motivumkozi`) és egy `cel_id` oszloppal; a kulcs `id + igehely + jelolt_tipus + cel_id`-re bővül; a generátor 1/b. blokkja és a `minosites` rés csak az `elofordulas` sorokat olvassa. Egy kapu marad (a `jeloltek.tsv`), de a tábla kulcsa és minden olvasója változik.
- (ii) **külön jelölttábla** (`adat/motivumkozi_jeloltek.tsv`, a `jeloltek.tsv` mezőivel + `cel_id`, `cel_igehely`). A meglévő tábla és olvasói nem változnak; két jelöltkapu lesz.
- (iii) **a `jeloltek.tsv` változatlan sémával**, a `forras_kereses` `motívumközi:` előtaggal jelölve, a generátor előtag szerint szűr. Séma-változás nincs, de a jelentést szabad szöveg hordozza, és a kulcsütközés (fent) megmarad.

**Opciók — a kapcsolat célszintje** (az ALVIL-001 pilot (a) jelöltje veti fel): kell-e a motívum–motívum kapcsolatnak alpont-szintű célja (melyik funkcióhoz, ↳ alponthoz kötődik), vagy elég a motívum-szint?
*Mért helyzet:* az alpontnak ma nincs adatbeli azonosítója: az `adat/motivumok.tsv` mezői között (`id`, `cim`, … `forras_study`) nincs ↳ alpont, az `adat/SEMA.md` csak az új ID 4. kérdésének szabályaként nevezi meg („B nem önálló ID, hanem ↳ alpont”, 3. szakasz); az ALVIL-001 forrásában és tanulmányában „↳”/„alpont” nem szerepel. *(proveniencia: scope=adat/motivumok.tsv fejléce, adat/SEMA.md, motivumok/ALVIL-001.md, tematikus_lezart/Hadesz_Seol_tematikus.md | forras=manual (grep `↳|alpont`) | ts=2026-10-19)*
- (A) **csak motívum-szint:** az alpont legfeljebb az `indoklas` szabad szövegében áll. Egyszerű, de az (a) és a (b) jelölt ugyanarra a célra (ALVIL-001) mutat, a különbségük a lapon nem látszik, és az alpont későbbi kialakításakor kézzel kell visszakeresni.
- (B) **opcionális `alpont_a` / `alpont_b` mező szabad címkével** (üres = a motívum egésze). Most bevezethető, de a címke nem kulcs: elírás vagy átnevezés csendben szétválasztja az összetartozókat.
- (C) **opcionális `alpont_a` / `alpont_b` mező, amelynek értéke csak létező alpont-azonosító lehet** (a #123 ALVIL-001-ciklusa vagy egy külön séma-tétel vezeti be; az `ellenoriz.py` a létezést ellenőrzi; üres = a motívum egésze). Amíg az azonosító nem létezik, az alponthoz kötött jelölt `nyitva` marad, indoklásában a célalpont nevével, kapcsolat-sor nem keletkezik belőle.

**Javaslat: (C).** Indok: a Seól-döntés éppen azt rögzíti, hogy a kapcsolat az ALVIL-001-nek nem az egészéhez, hanem egy funkciójához (↳ alpont) kötődik, tehát a célszint adat, nem megjegyzés (CLAUDE.md fő szabálya: a kereszthivatkozás adat); a (B) szabad címkéje a negatív-kritérium-fegyelmet (a határt a kizárások rajzolják) nem tudja gépileg őrizni. *Következmény a sorrenddel (DT268):* ha e feladat a #123 előtt fut, az ALVIL-001 alpontja még nincs adatosítva, ezért a pilot (a) jelöltje a B3-ban legfeljebb `nyitva` döntést kaphat, és a kapcsolat-sora a #123 ALVIL-001-ciklusa után kerül be; a (b), a HAMART-001 és a TEREMT-001 jelölt ettől független. Ha az orkesztrátor az (a)-t is lezárva akarja a pilotban, a DT268 3. opciója (a B rész a #123 ALVIL-001-ciklusa után) a megoldás.

**Opciók — megjelenítés:**
- (α) **generált „5/b. Kapcsolódó motívumok” blokk** a 5. Kapcsolatok után: a jóváhagyott sorok adatként (másik motívum, igehely-pár, típus, indoklás), proveniencia-sorral, mindkét motívum lapján;
- (β) új kézi rés („Rokon motívumok”), amelyet a próza tölt;
- (γ) mindkettő: a generált blokk most, a próza később a meglévő `ertelmezes` résben.

**Javaslat: tárolás 3. (a célszint-részkérdés (C) javaslatával: `alpont_a`/`alpont_b` mező), jelölt-út (i), megjelenítés (α) most, a próza később az `ertelmezes` résben (γ felé).** Indok: a motívumközi kapcsolat más tengely, mint a motívumon belüli (a SEMA 4. szakaszának névütközése ugyanezt mutatja), ezért külön tábla kell; ez a meglévő 25+ sort és a lezárt Típus-mezőt nem érinti. A jelölt-út a (i), mert a 2. szabály egyetlen kapuja a `jeloltek.tsv` marad (a felhasználói kérés is ezt nevezi meg: „a `jeloltek.tsv`-n át”); a kulcsütközés és a hamis 1/b.-megjelenés csak a kulcs bővítésével és a generátor szűrésével kerülhető el. *Ha a kulcsbővítés a többi olvasón túl nagy beavatkozás, a tartalék a (ii) — ez a szabály betűjétől tér el (két kapu), a szellemétől nem.* A (iii)-t nem javaslom: a kulcsütközést nem oldja meg. A megjelenítés adat (α), mert a pilot után még nincs próza; új kézi rés (β) most üres maradna.

## 4. Lépések (⛔ a kötelező megállások)

**0. Modell-ellenőrzés** (CLAUDE.md): a tényleges modellnév összevetése a `modell: opus` mezővel; eltérésnél megállás.

**0.1 Előfeltételek:** a felmérés a main-en (`naplok/PROZA_FELMERES_ISTENTISZT-001_20261019.md`); a PROZA-feladat (`ISTENTISZT001_PROZA`) `lezarva` (ugyanazt a forrásfájlt írja, l. 6.); az `ir` fájljain nem fut más feladat (D39; a #123 a `jeloltek.tsv`-t és a `res_forras.tsv`-t is írja — ha fut, ⛔).

**0.2 ⛔ DT276 és DT277 eldöntése** a 3. szakasz opciói és javaslatai szerint, a `DONTESEK.md`-be helyőrzős tételként. A felhasználó (vagy az orkesztrátor a felhasználó felhatalmazásával) dönt; a végrehajtás a döntés után indul.

**A — alkalmazási és tanítói rés (a DT276 döntése szerint; az alábbi a 3. opció útja):**
- **A1** séma és dokumentáció: `adat/SEMA.md` 2.12, RENDER_BRIEF 1. (a döntésre hivatkozva), lexikonsablon, CLAUDE.md. Commit.
- **A2** jelölők az ISTENTISZT-001 forrásában és tanítói fájljában; bájt-összevetés: a jelölők nélküli szöveg azonos a régivel (szkript-fájllal). Commit.
- **A3** `res_forras.tsv` (8 × új sor), generátor, `ellenoriz.py` 11. szakasz. Próba-render a `generalt_proba/`-ba (nem a repón kívüli ideiglenes könyvtárba, mert verziózott próba; CLAUDE.md), a 8 lapra: a várt diff csak az új szakasz (és a tartalomjegyzék). **⛔ a próba-render jóváhagyása**, utána éles újragenerálás. Commit.

**B — motívumközi kapcsolat (a DT277 döntése szerint; az alábbi a javaslat útja):**
- **B1** séma: az új tábla (`adat/motivum_kapcsolatok.tsv`, fejléc, `adat/SEMA.md` új szakasz) és a `jeloltek.tsv` kulcsbővítése (a meglévő sorok `jelolt_tipus=elofordulas`, a többi új mező üres); táblát író szkript, írás előtt sor-összevetés az eredetivel, eltérésnél megállás (CLAUDE.md, TSV-szabály; minta: `eszkozok/igazolas_migracio.py`); a generátor 1/b. és `minosites` szűrése. A `jeloltek.tsv` minden meglévő sorára nulla-diff a lapokon (`eszkozok/nulladiff.sh`). Commit.
- **B2** pilot-jelöltek: a felmérés 3–5. összefüggésének mért alapja **saját lekérdezéssel** (a másik motívum előfordulása a `elofordulasok.tsv`-ben; a fejezet-, ill. beszéd-szomszédság `lekerdez.py karoli` / szkript-fájl alapján), `--naplo F<nn> --lepes adhoc`; a felmérés számai nem források. Jelölt soronként, `dontes=nyitva`, indoklással; az ALVIL-001-gyel két külön jelölt: (a) Zsolt 116:3 ↔ 116:4 az alpont-céllal (a célszint-részkérdés döntése szerint), (b) ApCsel 2:21 ↔ 2:27, 31 a motívum egészére. **K1:** az író az ALVIL-001, a HAMART-001 és a TEREMT-001 tematikus tanulmányát és kereszthivatkozás-naplóját egészben olvassa, mielőtt jelöltet ír (`olvas`). A TEREMT-001-nél a felmérés maga kéri az előzetes olvasást („óvatosan”). Commit.
- **B3 ⛔ Jelöltdöntés a felhasználótól** (a B5 jelöltminősítés emberi döntés, `F123_MIGRACIO2_BRIEF.md` 2c.): soronként `beépítve` / `elutasítva` / `nyitva`, érdemi indoklással. A közös fejezet vagy a közös szókészlet önmagában **nem** bizonyít szándékos utalást; a jelölt indoklása csak a mért szomszédságot mondja ki. A Seól-határ eldöntött (a #123 Seól-határ-döntése (felhasználó, 2026-10-19: az ISTENTISZT-001 határa marad, a „kiáltás a Seól szorításából” az ALVIL-001 ↳ alpontja; DT-F123d, PR #436, `56046a40`; a végleges szám a befogadáskor)); ha egy jelöltdöntés ettől eltérne vagy újranyitná, ⛔, és a kérdés a felhasználóé.
- **B4** a `beépítve` sorokból kapcsolat-sor (`dontes_ref`-fel), generált „5/b. Kapcsolódó motívumok” blokk mindkét érintett lapon; próba-render a `generalt_proba/`-ba, **⛔ jóváhagyás**, utána éles újragenerálás (a pilot négy lapja: ISTENTISZT-001, ALVIL-001, HAMART-001, TEREMT-001). Commit.

**C. Független ellenőrzés** (`fuggetlen-ellenor`, `naplok/ELLENOR_<KÓD>.md`) a base..head diffen: séma ↔ tábla ↔ generátor egyezése; nulla-diff a nem érintett blokkokon; a jelölők nélküli forrásszöveg bájtra azonos; nincs kapcsolat-sor jelölt-döntés nélkül; minden jelölt mögött saját proveniencia-sor. ELTÉRÉS esetén `/elteres` (2 kör).

**D. Zárás:** brief fejléce, zárónapló, a #123-nak szóló N-tétel (a két új rés és a motívumközi jelölt-út az X.M1-ben), a F6-os „Kapcsolódó motívum” NYITOTT-tétel állapota.

## 5. Elfogadási feltételek

1. A DT276 és a DT277 el van döntve, és a bevezetés a döntést követi.
2. (a) Az ISTENTISZT-001 lapján az alkalmazási kérdések és a tanítói összegzés megjelenik; a forrás- és a tanítói fájl szövege a jelölőkön kívül bájtra változatlan; a többi 7 lapon az új rés kimondott hiány- vagy átmeneti mondattal áll, nem üresen (DT2).
3. (b) Minden motívumközi kapcsolat-sor mögött `beépítve` jelölt áll felhasználói döntéssel és érdemi indoklással; jelölt nélkül nincs kapcsolat.
4. A meglévő jelöltek és kapcsolatok megjelenése nem változik (nulla-diff a régi blokkokon); motívumközi jelölt nem jelenik meg kizárt jelöltként.
5. Az `ellenoriz.py`, a `feladatok.py ellenoriz` és a CI zöld; a független ellenőrzés zöld; a felhasználó a ⛔-pontokon jóváhagyott.

## 6. Döntésnapló és sorrend (helyőrzők; végleges számot a `szamkiosztas` Action ad)

- **DT276** — alkalmazási és tanítói rés (3. szakasz). *Eldöntendő a 0.2-ben.* Javaslat: 3. opció, „6/b” hely, a 7 motívum a #123-ban, törzscikkben nem.
- **DT277** — motívumközi kapcsolat: tárolás, jelölt-út, megjelenítés (3. szakasz). *Eldöntendő a 0.2-ben.* Javaslat: új tábla, `jeloltek.tsv` kulcsbővítéssel, generált 5/b. blokk.
- **A4 (Seól-határ):** eldöntve, a #123 Seól-határ-döntése (felhasználó, 2026-10-19: az ISTENTISZT-001 határa marad, a „kiáltás a Seól szorításából” az ALVIL-001 ↳ alpontja; DT-F123d, PR #436, `56046a40`; a végleges szám a befogadáskor). Itt csak a pilot két ALVIL-001-jelöltjét és a célszint-részkérdést (DT277) alakítja. *Azonosító:* a Seól-döntés a #123-ban DT-F123d (az orkesztrátor feloldása, 2026-10-19); a #123 DT-F123c-je a `9_` sablon v1-véglegesítése, másik tétel.
- **Sorrend a PROZA-feladattal** (`beerkezo/ISTENTISZT001_PROZA_BRIEF_TERVEZET.md`): mindkettő írja a `motivumok/ISTENTISZT-001.md`-t, és ez a feladat írja a `jeloltek.tsv`-t, amelyet az olvas; a `feladatok.py` kölcsönös levezetett függést adna (DT-F39g: kizárás, a kisebb sorszám előre). **A befogadáskor:** e feladat `fugg`-ja a PROZA számát kapja, a PROZA `nem_fugg`-ja e feladatét. Indok: a próza az aranymintát rendezi, a jelölők és a pilot utána jönnek.
- **DT268 — sorrend a #123-mal** (befogadási döntés). A #123 is írja a `jeloltek.tsv`-t és a `res_forras.tsv`-t, és olvassa a `jeloltek.tsv`-t; a két feladat egyszerre nem futhat (D39 a közös táblákra is). Opciók: **1.** PROZA → e feladat → #123 (e feladat `nem_fugg: [123]`; a #123 levezetetten vár erre); **2.** e feladat a #123 után (a #123 fejlécébe `nem_fugg` kell e feladat számával, e feladatéba `fugg: [123]`; a 7 motívum jelölői ekkor e feladatban kerülnek a már migrált forrásokba: 7 motívumfájl írása); **3.** szétválasztás: az A rész (rés) a #123 előtt, a B rész (pilot) utána. **Javaslat: 1.** Indok: a #123 X.M1-je így már az új réseket és a jelölt-utat látja, a 7 motívum jelölőit a saját ciklusa teszi be (DT276 javaslata), és a felmérés is a lap-megjelenítést teszi a próza-munka elé („Javasolt sorrend”); ára, hogy a #123 e feladat zárásáig vár. A fejléc ezért már most `nem_fugg: [123]`. A PROZA számával kiegészítve a próbafutás 0 hibát, kör nélküli sorrendet adott (#110 → e feladat a számsorrendből, PROZA → e feladat → #123 a függésből); a 2. opcióval a próbafutás a #110-en át függési kört adott. *(proveniencia: scope=a két tervezet ideiglenes `F126_*`/`F127_*` másolata a repó gyökerében, a futás után törölve | forras=`python eszkozok/feladatok.py ellenoriz` és `fuggesek` | ts=2026-10-19)*
- **`munka: folyamat`, de motívumfájlt ír** (a jelölőket a forrásban és a tanítói fájlban): a `feladatok.py` ezért `ertelmezo`-ként kezeli (nem csomagolható, K3.1), és a K3.2 szerint az `olvas` a motívum teljes anyagát tartalmazza. Ez a szándék: a pilot jelöltdöntései értelmező munkák, egy kézben. Ha a befogadás a két részt szétválasztaná (A: folyamat, motívumfájl nélkül; B: értelmező pilot), az A-ból a jelölés átkerül a B-be vagy a #123-ba.

## 7. Eltérések a brieftől (végrehajtás közben, jóváhagyva)

- **`eszkozok/torzscikk_general.py` módosítása** (F127.4) — a fájl nincs az `ir`-listán. A DT276 „törzscikkben nem” pontja csak itt valósítható meg: a törzscikk a lexikonoldal 6. szakaszát a 7.-ig másolta, így a 6/b. is átkerült volna; a módosítás után a 6. szakasz a 6/b-ig tart (a próbán 7/7 törzscikk 0 eltérés). Jóváhagyta: a felhasználó, 2026-10-20 (DT278). A független ellenőr vizsgálja.
- **Az élesítés módja** (DT278 (a)): nem teljes `--cel lexikon --ir`, hanem az `eszkozok/f127_res_eles.py --ir` (csak a 6/b. szakasz és a tartalomjegyzék), mert a 7 nem migrált lap teljes újragenerálása a #36 függő változásait is behozná. Mellékhatás: a 7 régi lapon a tartalomjegyzék-blokk fejlécében a licenc-érték frissül.
- **N-F127a** (új nyitott tétel): a tanítói összegzés belső utalásai a lapon a tanítói fájl szakaszaira mutatnak; a forrásban javítandó.
- **Az `ir` bővítése a `jeloltek.tsv` kulcsbővítéséhez** (DT279 (1), orkesztrátor, 2026-10-20): `eszkozok/jelolt.py`, `eszkozok/nem_vizsgalt.py` (írók: új fejléc), `eszkozok/betolt.py`, `eszkozok/karoli_ellenorzes.py`, `eszkozok/ellenorzes/szabalyok.py`, `eszkozok/sqlite_epit.py` (olvasók: `jelolt_tipus=elofordulas` szűrés); a `torzscikk_general.py` is az `ir`-be került. A jelölt-sor két további, nem kulcs oszlopa: `cel_igehely`, `cel_alpont`. D39-ellenőrzés indulás előtt: egyik nem mergelt ág és egyik futó/megállt brief sem írja ezeket (git fetch, 2026-10-20). A `pardes.db` újraépítése nem a /mnt/c-ről fut, helyi teendő.
- **Az `ir` utólagos bővítése a ténylegesen írt fájlokkal** (a független ellenőrzés 2. ELTÉRÉS-tétele, `naplok/ELLENOR_F127.md`; a javítókör 1. köre, F127.19; a besorolást mechanikusnak a felhasználó hagyta jóvá, 2026-10-21): az `ir`-en kívül íródott, most felvéve —
  - `lexikon/ANTROP-001_TUDOMANYOS.md`, `lexikon/HODIT-001_TUDOMANYOS.md`, `lexikon/KIRALY-001_TUDOMANYOS.md`, `lexikon/MENNY-001_TUDOMANYOS.md`: a 8 éles lap közül a 4, amely nem volt az `ir`-en; az A3 élesítése (F127.6, `84e63e0a`: 6/b. szakasz és tartalomjegyzék, DT278 (a)) és a B4 élesítése (F127.16, `750c0ef8`: 5/b. blokk, DT281 (a)) írta őket;
  - `eszkozok/f127_res_jelolok.py` (F127.3, `7d23ae7f`: a rés-jelölők beírása), `eszkozok/f127_res_forras_bovit.py` és `eszkozok/f127_res_eles.py` (F127.4, `72e00b2b`: a `res_forras.tsv` 16 sora, ill. a részleges élesítő), `eszkozok/f127_jeloltek_bovit.py` (F127.9, `120f2cef`: a `jeloltek.tsv` kulcsbővítése): a feladat egyszeri, új segédszkriptjei.
  *(proveniencia: scope=9d602794..82a1873a | forras=`git diff --name-only`, `git log --diff-filter=A` | ts=2026-10-21)*
  - `eszkozok/teszt_general_ellenorzo.py` és `eszkozok/teszt_sqlite_epit.py` (F127.9, `120f2cef`: a kulcs-tábla a `jeloltek.tsv` bővített kulcsával és a `motivum_kapcsolatok.tsv`-vel, a táblaszám 23, az `ellenoriz.py`-szabályok száma 15 a 2/b. miatt) szintén az `ir`-en kívül íródott; az F127.26 vette fel őket (a független újraellenőrzés 1. ELTÉRÉS-tétele, `naplok/ELLENOR_F127_2.md`; a besorolást mechanikusnak a felhasználó hagyta jóvá, 2026-10-21).
  - **Következmény az `olvas`-ban** (F127.23): a négy új motívum-ID az `ir`-ben a K3.2 / E18 szabály szerint a kereszthivatkozás-naplót is kéri az `olvas`-ban (`python eszkozok/feladatok.py ellenoriz` → 4 HIBA az F127.19 után); az `olvas` a meglévő ALVIL/HAMART/TEREMT-mintára `tematikus_lezart/naplok/ANTROP-001*`, `…/HODIT-001*`, `…/KIRALY-001*`, `…/MENNY-001*` bejegyzéssel bővül (a tanulmányt a `tematikus_lezart/*_tematikus.md` már fedi). A négy lapot csak a mechanikus élesítő írta (6/b., 5/b., tartalomjegyzék), értelmező prózát nem. Az öt jóváhagyott tételen kívüli, a 2. tételből következő lépés; **elfogadva** (a felhasználó, 2026-10-21, a javítókör 2. körében, az újraellenőrzés megjegyzése nyomán, `naplok/ELLENOR_F127_2.md`). Kimondva: a négy `tematikus_lezart/naplok/<ID>*` minta (ANTROP-001, HODIT-001, KIRALY-001, MENNY-001) **csak formális**: kizárólag az E18 / K3.2 kielégítésére került be, egyetlen fájlra sem illeszkedik (a naplók tartalmi néven állnak), és a menet ezeket a naplókat **nem olvasta**, mert a négy lapot csak a mechanikus élesítő írta. A régi ALVIL-001 / HAMART-001 / TEREMT-001 minták ugyanígy egyetlen fájlra sem illeszkednek; ott a valódi naplók név szerint is szerepelnek az `olvas`-ban (`Hadesz_Seol_…`, `Bun_kovetkezmenyeinek_gyuruzese_…`, `Tehom_kereszthivatkozas_naplo.md`). A szabály gyengesége: N-F127b.
- **Az `ELLENOR_F127_3` két maradéka** (a javítókör 2/2 köre után, alacsony súlyú; a zárást ezekkel együtt a felhasználó hagyta jóvá, 2026-10-21): (1) a 2. kör végén elavult `kovetkezo` — az F127.30 (`29744c76`) fejléce rendezte; (2) az F127.27 (`44196cdb`) és az F127.28 (`5c6c5672`) üzenetének „(ELLENOR_F127_2 2.)”, ill. „(ELLENOR_F127_2 3.)” hivatkozása nem a jelentés számozását követi (ott a 2. tétel a `kovetkezo`, 3. tétel nincs, az F127.23 megjegyzés): oka, hogy a 2. kör jóváhagyó üzenete saját 1/2/3-as tagolást használt, és a commitok ezt követték. Force-push nélkül, a történet változatlan.
- **WSL-es tesztek: ellenőrizetlen.** A `python eszkozok/teszt_futtat.py` futásában a `teszt_olvaso_szerver` és a `teszt_pilot_aranymintaval` piros, de a régi (WSL-natív) `pardes.db`-t olvasták, miközben az ág módosította a `sqlite_epit.py`-t és az adatbázis sémáját (a `jeloltek` tábla 4 új oszlopa, új `motivum_kapcsolatok` tábla); a base-en nem futottak. **Merge-feltétel** (a felhasználó kikötése, 2026-10-21): a `pardes.db` helyi újraépítése (nem a /mnt/c-ről), majd a `python eszkozok/teszt_futtat.py` újrafuttatása a merge előtt. A `teszt_nem_vizsgalt.py` `teszt_lelet` hibája a base-en (`9d602794`) is piros (ott futott).
