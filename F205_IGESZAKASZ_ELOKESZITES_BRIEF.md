---
feladat: 205
cim: Az igeszakasz-tanulmány előkészíti a motívumcikket — igehelyenkénti jelölt blokkok, kinyerés a jeloltek.tsv-n át, a szakasz hiányzó szótári fordításai egy kötegben
kod: IGESZAKASZ_ELOKESZITES
tipus: feladat
fazis: folyamat
modell: opus
allapot: nem_indult
ad: a 2. sablonban igehelyenként hat jelölt blokk (funkció, negatív próba, jelentéspont, vita, visszhang, versszámozás) üres-jelöléssel; a MUNKAMENET A-szakaszában a helyük a vak olvasás sorrendjében; egy kinyerő, amely a blokkokból csak jelölt-sort ír a jeloltek.tsv-be manual provenienciával; a jelentéspont saját olvasata külön mezőben, a BDB-kártya érintetlen; a szakasz Strong-szavainak hiányzó fordítása egy kötegben; a SEMA és a tesztek; a mérési terv a következő tanulmányra
kovetkezo: "a HAMART-001 1. kiadása (/kiadas, PR #696) merge-e után indul; első lépés az M0 séma-javaslat ⛔"
munka: folyamat
olvas: [MUNKAMENET.md, sablonok/2_PaRDeS_bovitett_sablon.md, sablonok/9_PaRDeS_motivum_forras_sablon.md, sablonok/10_PaRDeS_U3_proza_prompt_sablon.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, sablonok/PaRDeS_gyorsreferencia.md, sablonok/KESZ_LAP_KOVETELMENY.md, adat/SEMA.md, adat/jeloltek.tsv, adat/visszhang_tanuk.tsv, adat/visszhang_megfelelok.tsv, adat/vitatott_forrasok.tsv, eszkozok/general.py, eszkozok/ellenoriz.py, eszkozok/gerinc_kartya.py, eszkozok/forditas_vedelem.py, naplok/F182_jelentes.md]
ir: [MUNKAMENET.md, adat/SEMA.md, adat/jelentespont_olvasat.tsv, eszkozok/tanulmany_kinyer.py, eszkozok/teszt_tanulmany_kinyer.py, eszkozok/szakasz_forditas.py, eszkozok/teszt_szakasz_forditas.py, F205_IGESZAKASZ_ELOKESZITES_BRIEF.md]
fugg: [125]
---

# F205_IGESZAKASZ_ELOKESZITES_BRIEF.md — Az igeszakasz-tanulmány előkészíti a motívumcikket

*FELADATOK #205 · Modell: opus · v1 · 2026.11.11*

**Indítási feltétel.** A HAMART-001 1. kiadása (a `/kiadas` menete, F125; PR #696) a `main`-en van. Addig a menet nem indul: a HAMART javítóköre ugyanezeket a fájlokat írhatja (`MUNKAMENET.md`, sablonok). A `fugg: [125]` ezt a függést jelöli; ha a kiadás más feladatszám alatt zárul, a futtató az indításkor a PR állapotát nézi, nem a számot.

**A fejléc `ir` mezője a befogadáskor szűkített (2026-11-11).** A feladat ezeket is írja: `sablonok/2_PaRDeS_bovitett_sablon.md`, `sablonok/9_PaRDeS_motivum_forras_sablon.md`, `sablonok/10_PaRDeS_U3_proza_prompt_sablon.md`, `eszkozok/general.py`, `eszkozok/ellenoriz.py`. A befogadáskor ezek nem állhattak az `ir`-ben: a #125 (és a #74, #123, #178, #193) olvassa őket, a #205 pedig a #125 után fut, és a `feladatok.py fuggesek` ebből függési kört számolt (KOR 74 121 123 125 156 157 178 179 190 193 205). **Az M0 első lépése ezért a fejléc `ir` bővítése** ezzel az öt fájllal, a menet saját briefjén. Utána `python eszkozok/feladatok.py ellenoriz` és `fuggesek`: ha a kör megmarad (az olvasó feladatok egyike még nincs lezárva), ⛔, a felhasználó dönt. A futási időben olvasott adat (`adat/forditasok.tsv`, `adat/bdb_vers_jelentes.tsv`, `adat/thayer_vers_jelentes.tsv`, `f22/versosszevonas.tsv`) és a meglévő fordítási láncok (`eszkozok/thayer_api_koteg.py`, `eszkozok/bdb_api_koteg.py`, `eszkozok/glossza_forditas.py`) nem áll az `olvas`-ban: ezeket a menet csak futtatja vagy lekérdezi, sorrendet nem kívánnak; a #7 és a #38 hosszú fordítási menete nem tarthatja vissza.

**Bemenet.** A felhasználó elfogadott elve (2026-11-10, „igen”, és a jelentéspontra vonatkozó pontosítása). A felvetés szövege a session-jegyzetekben áll (`IGESZAKASZ_TANULMANY_ELORE_2026-11-10.md`, az orkesztrátor jegyzetmappájában); a lényege ebben a briefben teljes, a végrehajtáshoz a jegyzet nem kell, ezért az `olvas` mezőben sem áll.

## 1. Cél

A tanulmány egy igehelyet egyszer és alaposan olvas, kontextusban. A motívumcikk sok igehelyet olvas futólag (a HAMART-001-nél 48 sort). A HAMART késői leletei (F1–F35, `naplok/F182_jelentes.md`) többnyire igehelyenkénti ítéletek voltak, és a cikk-menet utólag, drágán pótolta őket: határ, jelentéspont, hiányzó fordítás, versszámozás, vita, visszhang, funkció-mondat. **Amit az alapos olvasás úgyis lát, azt a tanulmány rögzítse olyan formában, amelyet a motívumcikk átvehet.** A költségmodellben (keret% = fix + soronkénti + Strong-onkénti + prózaszavankénti) ez a cikk **soronkénti** és **Strong-onkénti** tagját csökkenti.

| Késői lelet (HAMART / ANTROP / ALVIL / ISTENTISZT) | Igehelyenkénti blokk a tanulmányban |
|---|---|
| 1/a: minden igehely alatt kerek mondat + „Funkció:” | 1. funkció |
| határ-K-k (F23); Júd 1:19 a negatív kritérium ellen (ANTROP) | 2. negatív próba |
| BDB/Thayer jelentéspont (#185: 94%, a kétes esetek) | 3. jelentéspont |
| hiányzó Vitatott pontok (ALVIL: Luk 16:23) | 4. vita |
| hiányzó visszhang (ANTROP, ALVIL, ISTENTISZT) | 5. visszhang |
| LXX/Károli/MT versszámozás (F32) | 6. versszámozás |
| hiányzó fordítás (F31) | gépi lépés, nem blokk (4. teendő) |

## 2. Hatókör

**Benne van:**
1. A 2. sablon (`sablonok/2_PaRDeS_bovitett_sablon.md`) új pontja: **igehelyenkénti jelölt blokkok** a hat ponttal, gépileg olvasható jelölőkkel.
2. A `MUNKAMENET.md` A-szakaszának kiegészítése: hol készül a hat pont a vak olvasás sorrendjében, és hol fut a kinyerés és a fordítás-köteg.
3. Kinyerő (`eszkozok/tanulmany_kinyer.py`): a blokkokból **csak jelölt-sort** ír az `adat/jeloltek.tsv`-be, döntés nélkül (`dontes=nyitva`), `manual` provenienciával.
4. Gépi lépés (`eszkozok/szakasz_forditas.py`): a szakasz Strong-szavainak hiányzó szótári fordítása egy kötegben, a meglévő fordítási láncokon át.
5. A jelentéspont saját olvasatának helye az adatrétegben (külön mező vagy tábla, l. M0), és a motívumcikk szabálya, ha az olvasatunk eltér a BDB-étől (`sablonok/9_…`, hivatkozással a `10_` promptban).
6. `adat/SEMA.md`: az új jelölt-fajták, a mezők, a kinyerés jelölőnkénti táblája (a 3.10.5 mintájára), a gépi kapuk listája (3.11, generált).
7. Mérési terv: mit és hogyan mér a következő igeszakasz-tanulmány és az abból dolgozó cikk.

**Nincs benne:**
- **Visszamenőleges tanulmány nincs.** A 9 lexikonlaphoz nem készül tanulmány, és a meglévő tanulmányok sem kapnak utólag blokkot.
- **A határt nem a tanulmány zárja.** A tanulmány jelöltet és indoklást ad, ítéletet nem; a határt a motívum menete zárja (B5, `hatar-ellenor`).
- Új tanulmány írása. A próba tanulmánya saját feladat (`munka: ertelmezo`), a felhasználó választja ki a szakaszt; ez a feladat csak a formát, a kinyerőt és a mérési tervet adja.
- A lexikonlap generátorának (`lexikon_general.py`) módosítása. Ha az M0 azt mutatja, hogy az eltérő jelentéspont-olvasat a lapon csak generátorral jelenhet meg, az ⛔ és külön feladat.
- A BDB-kártya, a `bdb_vers_jelentes.tsv` és a `JELENTESPONT_KEZI` tábla. A `jp_kezi` továbbra is csak a BDB félreolvasásának javítására szolgál.

## 3. Korlátok (minden lépésre)

- **K1 — egyirányúság (DT28; CLAUDE.md 2. szabály).** A tanulmány forrás. A blokkokból a kinyerő csak a `jeloltek.tsv`-be ír, `dontes=nyitva`-val. Közvetlenül `elofordulasok.tsv`, `kapcsolatok.tsv`, `visszhang_tanuk.tsv`, `vitatott_forrasok.tsv` vagy a jelentéspont-tábla sorát nem írja; azokba a jelölt-sor csak döntéssel jut (SEMA 3/2, 3.10.6). A kinyerő a tanulmányba nem ír vissza.
- **K2 — a vak olvasás sorrendje (A4-torzítás) marad.** Az A1–A2 a gerinc-kártya nélkül készül. Ami a motívumot nem feltételezi (jelentéspont, vita, visszhang, versszámozás), az az A1–A2-ben is kitölthető. Ami a motívumot feltételezi (funkció, negatív próba), az a kártya és az A4 ⛔ után. A blokk sablonszövege nem hivatkozhat a kártyára.
- **K3 — üres pont explicit.** Csak azt a pontot kötelező kitölteni, amelyre a szakaszban van anyag. A többi `üres` jelölést kap, rövid okkal. Gyenge vagy asszociatív anyaggal nem töltjük ki (CLAUDE.md 3. szabály). A kinyerő a hiányzó pontot (sem érték, sem `üres`) hibának veszi, nem csendes kihagyásnak.
- **K4 — proveniencia.** A blokk minden kitöltött pontja `scope=manual`; ha egy pont lekérdezésből jön (versszámozás, jelentéspont-tábla), a lekérdezés saját proveniencia-sora áll mellette (CLAUDE.md 1. szabály).
- **K5 — a jelentéspont a mi olvasatunk.** Külön mezőben áll, `manual` provenienciával; a BDB-kártyát nem írja felül. Ha eltér a BDB-étől, a motívum-rétegben ez áll: „a BDB X-hez sorolja; mi Y-nak olvassuk, mert …”. Érdemi eltérésnél a Vitatott pontok közé is kerül.
- **K6 — egy szabály, egy hely (F184).** A blokk formája a 2. sablonban, a munkamenet-lépés a `MUNKAMENET.md`-ben (csak lépés és hivatkozás), az adatszabály a `SEMA.md`-ben, a cikkszabály (K5 megjelenése) a 9. sablonban. Máshol csak hivatkozás.

## 4. Lépések (⛔ a kötelező megállások)

**M0 — felmérés és séma-javaslat ⛔.**
1. Modell-ellenőrzés (CLAUDE.md). Az indítási feltétel ellenőrzése (PR #696 a `main`-en), `git fetch`, friss ág az `origin/main`-ből. A fejléc `ir` bővítése (l. fent, „A fejléc `ir` mezője a befogadáskor szűkített”), `feladatok.py ellenoriz` és `fuggesek`; függési körnél ⛔.
2. Felmérés, fájlba (`naplok/F205_jelentes.md`, 1. szakasz): a hat pont mindegyikénél mi a meglévő célhely az adatrétegben (`jeloltek.tsv`, `elofordulasok.tsv` funkció-mezője, `visszhang_tanuk.tsv`, `vitatott_forrasok.tsv`, `bdb_vers_jelentes.tsv`/`thayer_vers_jelentes.tsv`, a versszámozás meglévő forrásai: TAHOT-kulcs, `f22/versosszevonas.tsv`, `lxx_versszam`). A versszámozásnál külön: mennyi deríthető ki gépileg; ami gépi, azt a blokk a lekérdezésből veszi át, és a kinyerés csak ellenőriz (`ADAT-HIV` mintája, SEMA 3.10.7 4.).
3. Séma-javaslat a felhasználónak, `dontesek/uj/<ágnév>.md`-be (DT-F205a). Az ajánlott változat:
   - a `jeloltek.tsv` `jelolt_tipus` mezője új értékeket kap (a DT277 `motivumkozi` mintájára): `jelentespont`, `vita`, `visszhang`, `versszam`. A funkció és a negatív próba az `elofordulas` jelölt-sor `indoklas` mezőjébe kerül (a negatív próba a SEMA 2.4 „csak a fölérendelt fogalmon keresztül” mintája szerint);
   - az előfordulás-jelöltet olvasó eszközök továbbra is csak az `elofordulas` sorokat olvassák (DT279 (1)); a `general.JELOLT_TIPUSOK` és az `ellenoriz.py` 2/b. szabálya bővül;
   - a jelentéspont saját olvasata az `adat/jelentespont_olvasat.tsv`-ben (javasolt mezők: `strong`, `igehely`, `szotar`, `szotar_pont`, `olvasat`, `elter`, `indoklas`, `proveniencia`, `modell`, `datum`); a `jelentespont` jelölt döntés után ide léptetődik elő.
   
   Az alternatívák (új oszlopok a `jeloltek.tsv`-ben; külön tanulmány-jelölt tábla) indoklással a döntési tételben. **Megállás: a felhasználó dönt.**

**M1 — a 2. sablon új pontja.** A „4. Kapcsolódó igehelyek” után (vagy a végrehajtó javaslata szerint, indokolva) új pont: *Igehelyenkénti jelölt blokkok (a motívumcikknek)*. Igehelyenként egy blokk, saját sorban álló kezdő- és zárójelölővel (a SEMA 3.10.2 alakjának mintájára, pl. `<!-- IGEHELY-BLOKK: [igehely] | motivum: [ID vagy „új”] | gerinc: [gerinc_elem] -->` … `<!-- IGEHELY-BLOKK-VÉGE -->`). A pontos alakot az M1 rögzíti, a SEMA-val egyezően. A hat pont:
1. **funkció** — egy kerek mondat (az 1/a mércéje: teljes mondat, nem töredék);
2. **negatív próba** — „csak a fölérendelt fogalmon át tartozik ide?” igen/nem, indoklással; a fölérendelt fogalom a `motivumok.tsv`-ből;
3. **jelentéspont** — Strong, a szótár pontja (ha van), a mi olvasatunk, és hogy eltér-e (K5);
4. **vita** — a versre vonatkozó érdemi értelmezési vita, nevesített képviselővel; homályos „egyesek szerint” nem elég;
5. **visszhang** — a visszhang-réteg formájában (`visszhang_megfelelok` / `visszhang_tanuk` mezői szerint: hagyomány, tanú, mű, egy saját szavas mondat, forrás); idézet nélkül;
6. **versszámozás** — eltérés Károli / MT / LXX között, a lekérdezés proveniencia-sorával, vagy `üres`.

Mellé: K2 (melyik pont mikor tölthető), K3 (`üres` + ok), és egy kitöltött példa egy kitalált igehely nélkül, a HAMART-001 egy meglévő sorával (csak minta, adat nem keletkezik belőle). A sablon fejléc-changelogja: v23.

**M2 — `MUNKAMENET.md`, A-szakasz.** Új vagy kiegészített sorok, csak lépés és hivatkozás (K6):
- A1–A2: a motívumtól független pontok (jelentéspont, vita, visszhang, versszámozás) itt tölthetők;
- A2 után: **szakasz-fordítás** (`python eszkozok/szakasz_forditas.py --szakasz "…"`), gépi;
- A4 ⛔ után: a funkció és a negatív próba;
- A4 után: **kinyerés** (`python eszkozok/tanulmany_kinyer.py <tanulmány>`), kinyerési jelentéssel; a jelölt-sorokról a döntés a B5-ben vagy a motívum menetében születik.
A „ma mivel fut” oszlop csak létező parancsot nevezhet meg (a fájl szabálya).

**M3 — kinyerő.** `eszkozok/tanulmany_kinyer.py` (+ `teszt_tanulmany_kinyer.py`):
- a `general.py` meglévő kinyerési logikáját (`kinyeres_elemez`, `kinyeresi_jelentes`, a `JELÖLT`-jelölő szabályai) importálja, nem másolja; ha ehhez a `general.py`-ban szétválasztás kell, az a minimális, és a kimenete a meglévő `motivumok/` kinyerésnél bájtra azonos (teszttel);
- csak jelölt-sort ír, `dontes=nyitva`, `forras_kereses` = `scope=manual | forras=<tanulmány>#<igehely> | ts=<DATUM>`; meglévő kulcsnál nem ír, a jelentés jelzi;
- `üres` pontból sort nem ír; hiányzó pontot, hiányzó gerinc-elemet (`elofordulas`-nál), párosítatlan jelölőt hibának vesz, és megáll;
- az `indoklas` olvasói szöveg (SEMA 2.4; a 29. szabály mintái), a belső jel a `dontes_ref`-be kerül;
- írás előtt az eredetivel összeveti a sorokat, eltérésnél megáll (CLAUDE.md „TSV-olvasás”; `split('\t')` / `'\t'.join()`);
- alapból száraz futás (`--ir` nélkül csak jelentés); a tesztek fixture-ön, repón kívüli könyvtárban futnak.

**M4 — szakasz-fordítás.** `eszkozok/szakasz_forditas.py` (+ teszt): a szakasz Strong-szavai (TAHOT/TAGNT, Károli-kulcs szerint olvasva, CLAUDE.md „Adat-tár”) → melyiknek hiányzik érvényes fordítása az `adat/forditasok.tsv`-ben (Thayer-szakasz, TBESG-glossza, BDB-szakasz; az `allapot` szerint, ahogy az F182.17 mérte). Kimenet: egy Strong-lista, amely a meglévő láncok bemenete (`thayer_api_koteg.py --strongok`, a BDB- és a glossza-lánc). Új fordítómotor nincs; a `forditas_vedelem.py` őre érvényes sort nem fordít újra. Ebben a feladatban fordítás nem fut (költség nincs): a lista és a száraz becslés készül el, egy meglévő szakaszon kipróbálva.

**M5 — `SEMA.md` és a cikkszabály.**
- `SEMA.md`: a 2.4 új `jelolt_tipus` értékei (M0 döntése szerint), az új tábla (ha van) saját szakasza, a kinyerés jelölőnkénti táblája (a 3.10.5 mintájára, a tanulmány mint forrás), a 3.11 újragenerálva.
- `sablonok/9_PaRDeS_motivum_forras_sablon.md`: a K5 cikkszabálya (a BDB-től eltérő olvasat mondata a motívum-rétegben; érdemi eltérésnél a Vitatott pontok); a `10_` promptban csak hivatkozás rá.
- Ha az M0 döntése új `jelolt_tipus` értéket hoz: `general.py` `JELOLT_TIPUSOK` és `ellenoriz.py` 2/b. szabálya, teszttel; a meglévő `jeloltek.tsv` sorai bájtra változatlanok.

**M6 — mérési terv.** A `naplok/F205_jelentes.md` mérési szakasza:
- **alapvonal:** a soronkénti egységköltség (keret% / igehely-sor: U1-adat, visszhang két kézzel, kapcsolatok) és a Strong-onkénti (hiányzó fordítás, szótári blokk) a meglévő mérésekből (#182 2. fázis, #183, az ISTENTISZT-001 mérése, ha addig elkészül); amit nem mértek, az „nincs mérés”, nem becsült szám;
- **próba:** a következő igeszakasz-tanulmány a blokkokkal készül; mérve a tanulmány többletköltsége (a blokkok kitöltése, keret%), és az abból dolgozó cikk soronkénti költsége azoknál a soroknál, amelyekhez van blokk, a blokk nélküli sorokhoz és az alapvonalhoz képest;
- **siker:** a cikk soronkénti költsége a blokkos soroknál csökken, és a csökkenés nagyobb, mint a tanulmány többletköltsége soronként; ha nem, a blokkokat szűkíteni kell (melyik pont nem térült meg).
A próba és a mérés későbbi feladat (a következő tanulmány és cikk ütemezése a felhasználóé); erre a menet nyitott tételt nyit (`nyitott/uj/<ágnév>.md`, N-F205a).

**M7 — ellenőrzés és zárás.** Tesztek (`teszt_tanulmany_kinyer`, `teszt_szakasz_forditas`, a `general.py`/`ellenoriz.py` érintett tesztjei), `python eszkozok/ellenoriz.py` (0 új SÉRTÉS), `python eszkozok/feladatok.py ellenoriz` 0. Egy `fuggetlen-ellenor` futás, legfeljebb egy javítókör (a `/kovetkezo` szerint), jelentés a `naplok/F205_jelentes.md`-be. Draft PR; **a merge nem ennek a sessionnek a dolga.**

## 5. Elfogadási feltételek

- G1: a diff csak az `ir` fájlokat érinti (és a közös koordinációs fájlokat); a `lexikon/`, a `motivumok/` és a meglévő tanulmányok bájtra változatlanok.
- G2: a 2. sablonban a hat pont a jelölőkkel, az `üres` szabállyal, a K2 sorrenddel és egy mintával áll; a sablon nem hivatkozik a kártyára az A1–A2 részében.
- G3: a `MUNKAMENET.md` A-szakasza megnevezi a hat pont helyét, a szakasz-fordítás és a kinyerés lépését, létező paranccsal.
- G4: a kinyerő a fixture-ön csak `dontes=nyitva` jelölt-sort ír, `scope=manual` provenienciával; más táblát nem ír; hiányzó pontnál, hiányzó gerinc-elemnél és ütközésnél jelent és megáll; a `motivumok/` kinyerése bájtra azonos.
- G5: a jelentéspont saját olvasata külön helyen áll; a `bdb_vers_jelentes.tsv`, a `JELENTESPONT_KEZI` és a BDB-kártya változatlan.
- G6: a szakasz-fordítás egy meglévő szakaszon kiadja a hiányzó Strongok listáját és a száraz becslést; fordítás és API-hívás nem fut.
- G7: a `SEMA.md` és a 9. sablon a K6 szerint egy helyen mondja ki a szabályt; a 3.11 generált listája friss.
- G8: a mérési terv alapvonala csak mért számot tartalmaz; az N-F205a nyitva.
- ⛔ Az M0 séma-döntése nélkül adatséma nem változik.

## 6. Döntésnapló

- 2026-11-10 — a felhasználó elfogadta az elvet („igen”): a tanulmány egy igehelyet egyszer, alaposan olvas, a cikk sok igehelyet futólag; igehelyenként hat pont, gépi lépésként a hiányzó fordítás.
- 2026-11-10 — a felhasználó pontosítása („de attól mi még juthatunk eltérő véleményre”): a tanulmány jelentéspontja a mi olvasatunk, külön mezőben, `manual` provenienciával; a BDB-kártyát nem írja felül; a `jp_kezi` csak a BDB félreolvasásának javítása.
- 2026-11-11 — brief és befogadás; a végrehajtás a HAMART-001 1. kiadása után.
