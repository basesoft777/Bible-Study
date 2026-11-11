# /lap-javit HAMART-001 — jelentés és változáslista

*2026-11-11 · végrehajtó: claude-opus-5-5 (a kért modell: opus) · ág: `claude/lap-javit-hamart` · PR: basesoft777/Bible-Study#699*

*Bemenet:*
- *a lektor listája (`naplok/KIADAS_HAMART-001_lektor.md`, a #696 ágán): 46 tétel, ebből 43 lektori, 3 orkesztrátori;*
- *az orkesztrátori névelő-tétel;*
- *a lapnézet kommentjei (https://claude.ai/artifact/39x5VLDvyq9z2AJ9zjww3K): komment nem volt.*

*Döntések (a felhasználó, az orkesztrátor továbbításában, 2026-11-11):*
- *„mehet a javaslatokkal”;*
- *a határkérdésekre „a/a”;*
- *a menet módjára „mehet az egybeírás”;*
- *a 18. tételben orkesztrátori döntés született.*

*A menet:*
- *az értelmező rések (Kivonat, Miért fontos, Értelmezés a vitatott pontokkal, Módszertan és nyitott kérdések) egy kézzel, egy olvasásban újraírva a kézi forrásban (`motivumok/HAMART-001.md`);*
- *a lap elejének szövege (`motivumok.tsv` és a generátor) ehhez igazítva;*
- *a generátorszintű tételek a generátorban, kapuval;*
- *az új prózán gépi versellenőrzés, szkripttel és Sonnet-subagenttel: `naplok/HAMART_lapjavit_versellenorzes.md`.*

*A korábbi, tételenkénti változatot (F125.LJ2) az egybeírás felülírja.*

## Összegzés

- **A határ nem változott:** 47 hely, 54 vers; a felvett és a kizárt helyek ugyanazok. A 6. (A) és a 11. (A) döntés a szöveget pontosította.
- **A szerkezet változatlan:** szakaszok, alcímek, harmadik személy; a forrás négy rése szól újra, egy hangon.
- **Adat:**
  - a lap elejének szövege (`motivumok.tsv` `negativ_kriterium`);
  - az előfordulás-tábla 6 kapcsolódás-szövege és 1 funkciója, a jelöltek beépített során át;
  - a kapcsolat-tábla 56 indoklás-szövege: a döntés, a bizonyosság és a szint változatlan.
- **Generátor és kapu:** 16 tétel.
  - Két gyökérok, gépi védelemmel:
    - **15. Károli-KH részlista-másolat.** A szabály a teljes táblán +27 forrásverset szűr, a KH_MASOLT kapu az új szerkezetű lapon BUKÁS.
    - **Névelő.** A LISTA_NEVELO kapu BUKÁS; a javítás előtt 464 elem állt névelővel, utána 0.
  - A régi lapok szövege nem változik (E28): az új viselkedés csak az új szerkezetű lapon fut.
- **Gépi versellenőrzés:** 71 mondat, 174 hivatkozás. A szkript 2 eltérését és a Sonnet 11 eltérését javítottam. Egy eltérés nem javult: a Drash olvasata a lap kimondott olvasataként marad.
- **Kapuk:**
  - olvasói kapu: 0 BUKÁS, 14 figyelmeztetés (előtte 15);
  - `ellenoriz.py`: 0 SÉRTÉS;
  - nyílt mag kapu: 0 BUKÁS. A hat változott szöveg angol párja F170 szerint készült (claude-sonnet-5-5).
- **Tesztek:** `teszt_kesz_lap_hamart` 42 OK, `teszt_olvasoi_kovetkeztetes` 13 OK, `teszt_karoli_kh_gyanus` 3 OK, `teszt_nyilt_mag` 79 OK.
- **Napló:** `adat/lap_javitasok.tsv`, 48 sor; a próza-sorok új szövege az egybeírt végszöveg. A Kolofonban: „Emberi lektorálás | 32 hely”.

## Szakaszonként — mi változott a régihez képest

**A lap eleje.**
- „A motívum.” a cím ismétlése helyett az azonosság hordozóját mondja: szerkezeti motívum, az adatból.
- A második címke „Mi tartozik ide, és mi nem.”, mert a negatív kritérium a pozitív feltételt is tartalmazza.
- A lánc első említése önmagában érthető.
- A kizárás oka a szövetség rendje.
- Az erőszak a hallás igéjével ugyanabban a versben.
- A tematikus helyeket olvasói mondat írja le.
- A fölérendelt fogalom zárójele a „hígulna” nélkül áll.

**Kivonat.** Négy bekezdés maradt.
- A lánc leírása feszesebb.
- Az Ez 7:23 a várost, az Ez 8:17 a földet mondja.
- A Jer 6:7 a próféták hallás-mondatának példája.
- A határ-bekezdés:
  - a lap elejével egyező szabályt mond, a hallás igéjének három esetével (Jer 6:7, 51:46, Hab 1:2);
  - a két Királyok-helyet a valódi ok, a szövetség rendje zárja ki („a föld szava nélkül” helyett);
  - az Ez 12:19 és a Sof 1:2-3 felvett helyként, a különbség megnevezésével áll.
- A tematikus helyek olvasói mondattal állnak, a belső „jelölés” szó nélkül.

**Miért fontos ez a lelet.**
- árar: a törzsbeli eltérés pontos hatókörrel.
- adámá: mért szám (12 genezisi vers és a 12:3); a „négy genezisi szakasz” kimaradt. Az 1Móz 6:11-13 földje az erec.
- iccávón: a viselősség fájdalma.
- chámász és sáchat: a vers szövege szerinti idézet, a két prófétai szókapcsolat helyes leírása.
- A görög szavak: a „föld” alakja helyes.
- A Károli-szavak: teljes felsorolás.

**10. Értelmezés.**
- Peshat:
  - az alany-sorban a következmény verse (6:13) áll;
  - a hordozó a 6:11-13 erec-ével;
  - a minőség a 6:12 szövege szerint;
  - a tükörítélet következtetése átkerült a Drash második tételébe.
- Remez:
  - a 12:3 a 9:25-26-tal összevetve áll (az „először” helyett);
  - Ezékiel három helye a saját tárgyával;
  - a tövis és bogáncs (1Móz 3:18) és a Zsid 6:8 genezisi helye (1Móz 3:17-18) hivatkozva;
  - a Jel 19:2 a Septuagintán át;
  - a Róm 8:20-21 utalása a valós tartalomra mutat.
- Drash:
  - 4:10-11 a vers szövege szerint;
  - a második tétel a tükörítélettel;
  - a zárómondat a „mindig” nélkül.
- Sod: a „visszavonás” egy jelentésben; a lap nem dönt az átok mint állapot kérdésében.
- Vitatott pontok: a forrásrétegek bekezdésében Carr állítása külön áll, a szó és a forrás megfeleltetése olvasatként.

**11. Módszertan és nyitott kérdések.**
- A keresések köre és megnevezése egységes; az 577 és az 1 403 viszonya kimondva.
- A második ellenőrzés kizárásai a valós helyekkel szerepelnek: a Hab 2:8 és 2:17 kint, a Hab 1:2 bent.
- A TR-mérce mondata: öt lexikai hely, és a Jel 22:3 tematikus; a Jel 22:3 alakváltozata mindkét forrással.
- Nyitott kérdések (a cím „séma-korlátok” nélkül):
  - a föld színe csak két helyen áll;
  - a két Jób-hely külön szerepel;
  - a „vég” szava közös, de nem lánc-szó;
  - a Galata-olvasat a Gal 3:10-zel.

**A generált szakaszok** (a generátorban):
- 6. Kereszthivatkozások: olvasói jegyzet; a Sof 1:9 másolt listája kimaradt.
- 7. Kapcsolatok:
  - a következtetés mondata;
  - a PaRDeS-oszlop jelentése;
  - az 56 indoklás: a mért egyezés a tanú, a lap prózája nem;
  - a farok egyszer áll.
- 9. Hatástörténet: bevezetők és jegyzetek olvasói nyelven, egyverses szó nélküli számokkal; a tematikus Jel 22:3 kimaradása kimondva; „előkép” nélkül.
- 4.8: a chattát cellája.
- 2.: a Jel 22:3 cellája.
- Minden lista és tábla névelő nélkül.

## A 46 tétel — hol és hogyan

| # | Hol | Hogyan |
|---|---|---|
| 1, 2, 3, 4 | a lap eleje | generátor (`egyszerusitett_kolofon`, `AZONOSSAG_OLVASOI`) + `motivumok.tsv` |
| 5, 6, 7, 8, 11 | Kivonat | egybeírás; a 6. és a 11. a felhasználó (A) döntése szerint |
| 9, 10, 11, 12, 13, 14 | 2.1 | `elofordulasok.tsv` kapcsolódás a jelöltek során át (Jer 6:7, Hab 1:2, Jer 51:46, Ez 28:16, Sof 1:9, Mik 6:12) |
| 15 | 6. Kereszthivatkozások | generátor + kapu (DT-F125i) |
| 16 | 6., jegyzet | generátor |
| 17 | 7., következtetés | generátor (csak az új szerkezetben) |
| 18 | 7., PaRDeS-oszlop | orkesztrátori döntés; jegyzet + az indoklás (DT-F125h) |
| 19, 20 | 7., Alátámasztás | `kapcsolatok.tsv` indoklás (`naplok/F125_lapjavit_kapcsolat.py`) + generátor (farok) |
| 21, 22 | Miért fontos | egybeírás |
| 23, 24, 25, 26, 27, 44 | 9. Hatástörténet | generátor |
| 28, 29, 30, 31, 32, 33, 34, 35, 36, 37 | 10. Értelmezés | egybeírás; a 32. a kapcsolat-indoklásban is (Ez 12:19); a 36. az Ézs 60:18 funkciójában is |
| 38, 39, 40, 41, 42, 43 | 11. Módszertan | egybeírás |
| 45 | 4.8 | generátor; a tő sorai: N-F125f |
| 46 | 2. Előfordulások | generátor |
| névelő | minden lista és tábla | generátor + kapu (DT-F125g) |

## A 12 nyitott tétel döntése

(A lektor 2. köre itt nem adott szöveget. A 6. és a 11. a felhasználóé, a 18. az orkesztrátoré.)

**1. „A motívum.”**
- Döntés: az azonosság hordozója áll a lap elején, az adatból.
- Miért: a cím a címsorban már áll, és a hordozó az új ID első kérdése.

**2. A második címke**
- Döntés: „Mi tartozik ide, és mi nem.”; ugyanaz a szabály áll a lap elején és a Kivonatban.
- Miért: a negatív kritérium a pozitív feltételt is tartalmazza.

**4. „hígulna”**
- Döntés: a zárójel a „hígulna” szó nélkül áll.
- Miért: a második fele magában is érthető.

**6. (A) A két Királyok-hely**
- Döntés: kint maradnak; az ok a szövetség rendje, a két hely a saját tartalma szerint megnevezve.
- Miért: a „föld szava nélkül” hamis volt; a felhasználó döntése.

**9. Jer 6:7**
- Döntés: a vers két állítása külön áll; az „ítélet felel” kimaradt.
- Miért: a versben nincs ítélet-szó.

**11. (A) Hab 1:2**
- Döntés: bent marad; a meghatározás a hallás igéjének három esetével áll.
- Miért: a felhasználó döntése. A kizárt Hab 2:8 és 2:17 kint marad (nincs bennük hallás).

**15. Sof 1:9**
- Döntés: részlista-szabály és kapu.
- Miért: a csak teljes egyezést kereső szabály nem fogta meg; a Sof 1:2-3-nak nincs KH-listája a lapon.

**18. A PaRDeS-szint**
- Döntés: a kapcsolat jellege; a jegyzet kimondja.
- Miért: orkesztrátori döntés; az adat nem változik.

**19. A „lap prózája”**
- Döntés: a mért egyezés a tanú; ahol hagyományos gyűjtemény nem köt össze, kimondja.
- Miért: a lap nem hivatkozhat önmagára; a DT748 változatlan.

**35. „mindig”**
- Döntés: a lap olvasataként, „mindig” nélkül.
- Miért: a szöveg eseteket mond, szabályt nem.

**36. „visszavonás”**
- Döntés: a Sod-mondat az ige szintjén áll; az Ézs 60:18 funkciója „megfordítás”; a lap nem dönt.
- Miért: így a szó egy jelentésben áll, és a Vitatott pontok nyitott kérdése nyitva marad.

**45. chattát**
- Döntés: „Nincs rokon nyelvi alak a BDB szócikkében; az igei tő … ad rokon alakokat”; a tő sorai külön tétel.
- Miért: a cella a szóról szól; a tő kinyerése két kéz munkája.

## Nyitott (külön tétel)

- N-F125f: a chattát tövének rokon nyelvi sorai.
- N-F125g: a részlista-szabály hatása a régi lapokra és a #177 MEK-összevetésre.
- N-F125h: az ISTENTISZT-001 négy ismétlődő kulcsa a `lap_javitasok.tsv`-ben.
