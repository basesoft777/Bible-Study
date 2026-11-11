# F206 — a prózaíró prompt a HAMART-001 lektori körének tanulságával

*2026-11-11 · végrehajtó: claude-opus-5-5 (a kért modell: opus) · ág: `claude/epic-hawking-d0313a`*

**Eredmény.** A 46 lektori tétel, a független ellenőr 17 eltérése és az újraírt prózán futott gépi versellenőrzés 14 eltérése (2 szkript, 12 második kéz) 12 hibaosztályba esik.

- **(a) prompt- vagy forrásszabály hiánya:** 7 prózaosztály (V1–V7) új szabályt kapott a 10. sablonban, a határszabály (V8) a 9. sablonban, a belső szó (V9) a 10. sablon meglévő szabályának pontosításaként. Mindegyik mellett egy rossz/jó pár áll, a HAMART-001 valós, javított mondataiból.
- **(b) generátor:** a lektor 16 tétele és az ellenőr 6 eltérése; a CS3 viszi, itt csak jelölve.
- **(c) adat:** a lektor 9 és az ellenőr 6 tétele, önállóan vagy (a)/(b) mellett.
- **folyamat (a szabály megvolt, a végrehajtás hibázott):** az ellenőr 3 eltérése (E1, E14, E17).

**Gépi védelem.** A `proza_allitas.py` (F200) két új ⚑ jelzést kapott, teszttel:

- kapcsolat-állítás a kapcsolat-adat erején túl (V5);
- hatókör: a csoport minden helyére tett szó-állítás, miközben a csoportban tematikus hely is van (V4).

A HAMART-001 lektori próbáján a ⚑ jelzéssel kézi listára kerülő tételek száma 9-ről 13-ra nő, a „nem látja” 11-ről 10-re csökken. Hat másik motívumon nincs új jelzés, tehát téves riasztás sincs.

A belső szavak gépi bővítése (`olvasoi_kapu.py`) a #699 merge-e után jön: **N-F206a**. A javítás társ-példányainak kapuja: **N-F206b**.

## Bemenet

- **A lektor listája:** `naplok/KIADAS_HAMART-001_lektor.md` (`origin/claude/kiadas-hamart-d4c26f`, #696). 46 tétel: 1–43 a lektortól (`claude-fable-5-2`), 44–46 orkesztrátori.
- **A javítás jelentése:** `naplok/HAMART_lapjavit_jelentes.md` (`origin/claude/lap-javit-hamart`, #699), a „Szakaszonként” és „A 46 tétel — hol és hogyan” rész. A gyökérok-besorolás ezen alapul: ahol a jelentés generátort nevez meg, ott (b), ahol egybeírást vagy kapcsolódás-szöveget, ott (a).
- **A gépi versellenőrzés:** `naplok/HAMART_lapjavit_versellenorzes.md` (ugyanott). Ezek az eltérések az *újraírt* prózában álltak, a lektor listájának ismeretében. Ezért ezek a második előfordulás bizonyítékai (a gyökérok-szabály szerint: gépi védelem kell).
- **A független ellenőr jelentése:** `naplok/ELLENOR_HAMART_lapjavit.md` (ugyanott). 17 eltérés: a tábla 13 ELTÉRÉS-sora, ebből a SEMA 2.49-sor négy, a CI-sor két külön tétel.
- **A mai 9. és 10. sablon:** a `main`-en (F193 v1.1, F182.37, F200.3). A már meglévő szabályt itt nem ismétlem, csak hivatkozom rá, vagy pontosítom.

## A hibaosztályok

| Osztály | Mi a hiba | Gyökérok | Szabály helye | Gépi védelem |
|---|---|---|---|---|
| **V1 Versállítás** | a mondat mást mond a versről, mint a vers: alany, tárgy, megszólított; két tagmondat összevonva; a versben nem álló szó (ítélet, vér, vádló); hivatkozatlan vers; nem Károli-névalak | (a) | 10. sablon, „Állítás a versről” 1. | részben: `proza_allitas.py` szópár-alany és szójelenlét (ELTÉR); a többi a kézi listán, a második kéz és a lektor dolga (N-F200b) |
| **V2 Más héber/görög szó** | a magyar szó („föld”, „romlik”) a versben nem a lánc szavát fordítja (erec ↔ adámá; két különböző görög ige; csak a Septuagintán át azonos); a „más szó” állítás hamis | (a) | 10. sablon, 2. (a korábbi ⚑-teendő előre hozva, írás közbeni szabállyá) | megvan: `proza_allitas.py` ⚑ (implicit szó), „X szava nélkül” / „más szóval” ELTÉR |
| **V3 Kizárólagos szó lekérdezés nélkül** | „először”, „egyetlen”, „mindig”, „minden”, teljesnek ható felsorolás | (a) | 10. sablon, 3. | megvan: `proza_allitas.py` ABSZOLUT ⚑ |
| **V4 Hatókör és számlálási kör** | az állítás a csoport minden tagjára szól, de nem mindre igaz (tematikus hely); a szám mást számol, mint amit a mondat mond; egy versből következetesség | (a) | 10. sablon, 4. | **új:** `proza_allitas.py` hatókör ⚑; megvan: szám- és fordulatpróba (ELTÉR) |
| **V5 Kapcsolat az adatnál erősebben** | „a szópár maga utal vissza”, „visszatér” közepes vagy hiányzó kapcsolat-sorral; függést sugalló mondat; utalás olyan szakaszra, amely a kérdést nem tárgyalja | (a) | 10. sablon, 5.; a 9. sablon 1/a-szabálya hivatkozik rá | **új:** `proza_allitas.py` kapcsolat ⚑; a szakasz-utalás tartalma: lektor |
| **V6 Olvasat a szövegnek tulajdonítva** | következtetés a Peshat alatt; általános tétel („mindig”) a szöveg állításaként; forrásnak (Carr) többet tulajdonít | (a) | 10. sablon, 6. | nem fogható meg gépileg (F200 „Mit nem tud”); a „mindig” ⚑ részben; lektor |
| **V7 Bevezetetlen fogalom, nem fedő címke** | felosztás vagy keresés bevezetés nélkül („négy genezisi szakasz”, „Strong-keresés”); a címke nem a tartalmát mondja; felvett és kizárt hely összemosva; címismétlés | (a) | 10. sablon, 7. | nem gépi (a töredéket csak az 1/a-ban méri a `proza_1a.py`); lektor |
| **V8 A határszabály két helyen két szöveggel** | a lap eleje (`motivumok.tsv` `negativ_kriterium`) és a Kivonat határ-bekezdése eltér; a kizárás oka nem a valódi ok | (a)+(c) | 9. sablon, „A Kivonat két kötelező határ-eleme” 1. pontja alatt | nem gépi megbízhatóan (két szabad szöveg összevetése); lektor |
| **V9 Belső szó, műhelynyelv, munkaállapot** | „hígulna”, „séma-korlátok”, „Strong-keresés”, „mintakeresés”, „láncvers”, „Peshat-mag”, „alapvonal”, „cella”, „modell emeli ki, másik kéz ellenőrzi”, „még nem történt meg” | (a) a forrás prózájában, (b) a generált blokkban | 10. sablon, a meglévő belső-szó szabály pontosítva | **N-F206a:** `olvasoi_kapu.py` BELSO/MUNKASZAVAK bővítése a #699 merge-e után |
| **V10 Idézet nem betűhív** | az idézőjeles szöveg nem a Károli szövege („útja”, „elveszti”, „földjét”) | (a); a szabály megvolt (9. sablon, új cikk 5. szabálya) | — | megvan: `proza_allitas.py` idézetpróba, `olvasoi_kapu.py` IDEZET |
| **V11 Proveniencia hiányzik** | új lekérdezésből (TAHOT) vett állítás mellől hiányzik a proveniencia-sor | (a); a szabály megvolt (CLAUDE.md 1.) | 10. sablon, egysoros hivatkozás | nem gépi; független ellenőr |
| **V12 A javítás nem terjed át a társ-példányokra** | a lapon javult, a jelöltsorban és a nyílt magban nem (Ez 28:16 „fejedelem”, Ézs 60:18 „visszavonás”) | (c) | — (a `/lap-javit` menetének dolga) | **N-F206b:** a régi mondatrész keresése az `adat/` tábláiban a javítás után |

## Gyökérok tételenként

Jelölés: (a) prompt- vagy forrásszabály hiánya, (b) generátor (a CS3 viszi), (c) adat, „folyamat”: a szabály megvolt, a végrehajtás hibázott. A „Gépi” oszlop: mit tesz ma a `proza_allitas.py` a lektor által látott (javítás előtti) szövegen a mai main-en, az F206 bővítésével (`--lektor` próba). A „–” azt jelenti, hogy a tétel nem pontossági (nem az 1. vagy 4. kérdés), ezért a próba nem méri.

### A lektor 46 tétele

| # | Hely | Osztály | Gyökérok | Gépi |
|---|---|---|---|---|
| 1 | lap eleje, „A motívum.” | V7 (címismétlés) | (b) generátor + (c) `motivumok.tsv` | – |
| 2 | lap eleje, „Negatív elhatárolás” | V7 + V8 | (c) `negativ_kriterium` + (a) | – |
| 3 | lap eleje, „név szerint tartozik ide” | V9 | (c) `negativ_kriterium` | – |
| 4 | lap eleje, „hígulna” | V9 | (b) generátor | – |
| 5 | Kivonat, Ez 7:23 | V1 | (a) | ELTÉR |
| 6 | Kivonat, 1Kir 13:34, 2Kir 17:23 | V8 + V1 (az ok nem a valódi ok; a tárgy Jeroboám háza) | (a) | ELTÉR |
| 7 | Kivonat, Ez 12:19 és Sof 1:2-3 | V7 (felvett és kizárt hely összemosva) | (a) | – |
| 8 | Kivonat, „a görög szó”, a keresés köre | V4 | (a) | kézi ⚑ |
| 9 | 2.1 Jer 6:7 | V1 (két tagmondat összevonva; ítélet-szó nincs) | (a) a `kapcsolodas`-ban | kézi |
| 10 | 2.1 Jer 6:7, Hab 1:2 | V5 | (a) a `kapcsolodas`-ban | kézi ⚑ (új: kapcsolat) |
| 11 | 2.1 Hab 1:2 | V1 + V8 (határ, (A) döntés) | (a) | kézi |
| 12 | 2.1 Jer 51:46 | V2 (erec) + V5 (nincs kapcsolat-sor) | (a) | kézi ⚑ |
| 13 | 2.1 Ez 28:16 | V1 (megszólított, névalak) | (a) | kézi |
| 14 | 2.1 Ez 28:16, Sof 1:9 | V5 + V2 | (a) | kézi ⚑ (új: kapcsolat) |
| 15 | 6. Sof 1:9 KH-lista | — (másolt lista) | (b) | nem látja (generált) |
| 16 | 6. bevezető jegyzet | V9 | (b) | – |
| 17 | 7. következtetés-mondat | V5 (közepes → „bizonytalan”) | (b) | nem látja (generált) |
| 18 | 7. PaRDeS-szint oszlop | — (az oszlop jelentése) | (c) `kapcsolatok.tsv` + (b) jegyzet | nem látja (generált) |
| 19 | 7. Alátámasztás, „a lap prózája” | V5 (önhivatkozás) | (b) + (c) indoklás | nem látja (generált) |
| 20 | 7. Alátámasztás, „további 2 szó”, farok | V7 + V9 | (b) + (c) indoklás | – |
| 21 | Miért fontos, adámá | V3 + V7 + V2 | (a) | kézi ⚑ |
| 22 | Miért fontos, Károli-szavak | V3 (teljesnek ható felsorolás) | (a) | kézi |
| 23 | 9. Peshat-mag, láncvers | V9 + V4 | (b) | nem látja (generált) |
| 24 | 9. alapvonal, cella, kinyerő tábla | V9 | (b) | – |
| 25 | 9. egyverses sor a számlálásban | V4 | (b) | nem látja (generált) |
| 26 | 9. „a lánc görög szavai állnak” | V4 (tematikus Jel 22:3) | (b) | nem látja (generált) |
| 27 | 9. ókori értelmezők bevezetője | V7 (töredék) + V4 + V9 | (b) | nem látja (generált) |
| 28 | 10. Peshat, hordozó | V2 (erec) | (a) | kézi |
| 29 | 10. Peshat, 1Móz 6:12 | V1 (út ↔ föld) | (a) | kézi ⚑ |
| 30 | 10. Peshat, tükörítélet | V6 | (a) | nem látja (forrás, tétel nélkül) |
| 31 | 10. Remez, „először” | V3 | (a) | kézi ⚑ |
| 32 | 10. Remez, Ezékiel három helye | V1 | (a) (+ (c) a 12:19 kapcsolat-indoklása) | ELTÉR |
| 33 | 10. Remez ÚSZ, utalás a vitatott pontokra | V5 (az ígért tárgyalás nincs) | (a) | kézi |
| 34 | 10. Drash, „vádló” | V1 + V6 | (a) | kézi ⚑ |
| 35 | 10. Drash, „mindig” | V6 + V3 | (a) | kézi ⚑ |
| 36 | 10. Sod, „visszavonás” | V5 (a szó két jelentésben) | (a) + (c) Ézs 60:18 funkció | kézi |
| 37 | 10. Vitatott pontok, Carr | V6 (a forrásnak többet tulajdonít) | (a) | nem látja (forrás, tétel nélkül) |
| 38 | 11. 1 403 vers | V4 | (a) | kézi ⚑ |
| 39 | 11. Strong-keresés, mintakeresés | V7 + V9 | (a) | – |
| 40 | 11. „hat újszövetségi helyén” | V4 | (a) | kézi ⚑ (új: hatókör; korábban: nem látja) |
| 41 | 11. Nyitott 1., „föld színéről” | V4 + V9 (cím) | (a) | ELTÉR |
| 42 | 11. Nyitott 2., Jób-helyek | V1 + V2 | (a) | kézi |
| 43 | 11. Nyitott 3., „más kulcsszóval” | V2 (hamis „más szó”) | (a) | ELTÉR |
| 44 | 9. „modell emeli ki” | V9 | (b) | – |
| 45 | 4.8 chattát, „még nem történt meg” | V9 (munkaállapot) | (b) + (c) BDB-tő | – |
| 46 | 2. Jel 22:3, „(nincs görög szó)” | V9 | (b) | – |

**Összesen:**

- (a) 29 tétel (a 2. a (c)-vel együtt);
- (b) 16 tétel, ebből 5 (c)-vel együtt (1., 18., 19., 20., 45.);
- (c) önállóan vagy (a)/(b) mellett 9 tételnél (1., 2., 3., 18., 19., 20., 32., 36., 45.).

A lektor 34 pontossági tételéből a `proza_allitas.py` ma gépileg 5-öt fog meg, kézi listára tesz 19-et (ebből ⚑ jelzéssel 13), nem lát 10-et (8 generált blokkban, 2 a forrásban gépi tétel nélkül: a 30. és a 37., mindkettő V6).

### A független ellenőr 17 eltérése

| E | Tétel | Osztály | Gyökérok |
|---|---|---|---|
| E1 | `nyilt_angol.tsv` `modell` mező javítás után | — | folyamat (a szabály megvolt: CLAUDE.md, modell-ellenőrzés; a hely adat) |
| E2 | 2Kir 17:23, „a »szín« szava nélkül” | V1 | (a) |
| E3 | Ez 28:16/17 megszólítottja a jelöltsorokban és a nyílt magban | V12 | (c) |
| E4 | `nevelo_le`: kódblokk, inline kód, mondat-cella | — | (b) |
| E5 | „többsége közepes” feltétel | — | (b) |
| E6 | Hab 1:2, „fordulata itt … tér vissza” (függést sugall) | V5 | (a) |
| E7 | 9. maradék: „alapvonal nem mérhető”, „előképversében” | V9 | (b) |
| E8 | ismétlés a lap eleje és a Kivonat között; a chámász-kizárás a lap elején hiányzik | V8 + V7 | (a) + (c) `negativ_kriterium` |
| E9 | proveniencia hiányzik az új TAHOT-állítások mellől | V11 | (a); a szabály megvolt (CLAUDE.md 1.) |
| E10 | `lap_javitasok.tsv` `generátor` sorok `uj` mezője | — | (c) |
| E11 | „Emberi lektorálás” címke modell-lektort takar | — | (c) + (b) |
| E12 | „14.. tétele” elírás | — | (c) |
| E13 | Ézs 60:18 jelöltsora „visszavonás” | V12 + V5 | (c) |
| E14 | döntéshely `dontes/uj/` | — | folyamat (CLAUDE.md: `dontesek/uj/`) |
| E15 | 6. sablon: „NEVELO” a LISTA_NEVELO helyett, „(a teljes cím)” | — | (b) (a sablon a generátor leírása) |
| E16 | CI E28 HIBA a régi lap Kapcsolatok-mondatán | — | (b) |
| E17 | E30: ékezet nélküli „indoklas” egy commitüzenetben | — | folyamat (CLAUDE.md, commit) |

### A gépi versellenőrzés 14 eltérése az újraírt prózán

| V | Hely | Eltérés | Osztály |
|---|---|---|---|
| s1 | Értelmezés, 1Móz 6:12 | „útja” a Károli „útát” helyett | V10 |
| s2 | Értelmezés, 1Móz 6:13, 6:17 | „elveszti” a „elvesztem”, „elveszessek” helyett | V10 |
| 6 | Kivonat | a Jer 51:46-ban a hír hallatszik, nem az erőszak | V1 |
| 8 | Kivonat | a Sof 1:2-3 nem „ismétli” a felsorolást; az 1Móz 6:7 nincs hivatkozva | V1 |
| 11 | Miért fontos, árar | az „egyetlen hely tér el” hatóköre | V3 |
| 17 | Miért fontos, iccávón | a 3:16-ban a viselősség fájdalma | V1 |
| 24 | Miért fontos, görög | „földjét” alak nincs a versben | V10 |
| 39 | Remez | a tövis és bogáncs genezisi helye nincs hivatkozva | V1 (hivatkozatlan vers) |
| 41 | Remez | a Jel 19:2 és az 1Móz 6:11 azonossága csak a Septuagintán át | V2 |
| 44 | Remez ÚSZ | a Genezis-vers nincs hivatkozva | V1 (hivatkozatlan vers) |
| 46 | Remez ÚSZ | két különböző görög ige | V2 |
| 48 | Drash | következtetés, amelyet a vers nem mond (maradt, a lap olvasataként) | V6 |
| 64 | Módszertan, TR | a STEPBible TR-adata κατάθεμα | V1 (forrásállítás) |
| 71 | Módszertan, Nyitott 4. | a Gal 5:3 kötelezettségről szól | V1 |

**A második előfordulás.** Az újraírt prózában a lektor ismeretében is újra megjelent a V1 (7×), a V2 (2×), a V3 (1×) és a V10 (3×); az ellenőrnél a V5 (E6), a V9 (E7) és a V12 (E3, E13). A gyökérok-szabály szerint ezeknél gépi védelem kell, ahol fogható:

- **V2, V3, V10:** már van (F200);
- **V5:** új ⚑ (F206);
- **V9:** N-F206a;
- **V12:** N-F206b;
- **V1:** szerkezeti állítás (ki az alany, mit mond a vers), gépileg csak a szópár-alany és a szójelenlét része fogható. A többi a kézi lista második kezére tartozik (Sonnet, N-F200b), a lektor előtt. Ez a prompt 1. szabályának oka is.

## Szabályok — hol állnak

- **10. sablon** (`sablonok/10_PaRDeS_U3_proza_prompt_sablon.md`, v1.2):
  - új blokk: „Állítás a versről — írás közben”, V1–V7, szabályonként egy rossz/jó párral;
  - a belső-szó szabály pontosítva (V9), példapárral;
  - a proveniencia (V11) egy hivatkozó sorral;
  - az „Állítás-ellenőrzés” ⚑-bekezdése rövidebb lett: a javítás módja a fenti szabályokra mutat, a két új ⚑-fajta megnevezve;
  - a fejléc kimondja: a próza mondatszintű szabályai itt állnak, a forma szabályai a 9-esben (F184; DT-F206a).
- **9. sablon** (`sablonok/9_PaRDeS_motivum_forras_sablon.md`, v2.2):
  - „A Kivonat két kötelező határ-eleme” 1. pontja alatt: egy szabály, két hely, egy szöveg (V8), példapárral;
  - az 1/a 1. pontja egy mondattal hivatkozik a 10-es „Állítás a versről” szabályaira.
- **`MUNKAMENET.md`:** nem változott. A lépések sorrendje ugyanaz: az U3 → C-a állítás-ellenőrzés → lektor sorrend megmaradt.

A sablon mérete: a 10-es 9 806 bájtról 14 686 bájtra nő (+50%), a 9-es 50 312-ről 51 900 körülire. A növekmény hét szabályból és nyolc példapárból áll. A szabályszöveg tömörített, a ⚑-bekezdés rövidebb lett. A példák a valós mondatok rövidített (…) alakjai, egy sorban.

## Gépi védelem — a `proza_allitas.py` bővítése

- **Kapcsolat-állítás (V5).** A mondat kapcsolat-igét használ („utal vissza”, „visszatér”, „tér vissza”, „visszhang…”, „felidéz…”; a „visszatérés” főnév nem, mert tartalmi szó lehet).
  - A `kapcsolodas`-sornál ⚑, ha a sor helyének nincs `kapcsolatok.tsv`-sora, vagy egyik sora sem `magas` bizonyosságú.
  - A rés mondatánál ⚑, ha a megnevezett, a motívumban álló helynek nincs kapcsolat-sora.
  - Kapcsolat-adat nélküli motívumon (ALVIL-001) a próba nem fut: az adathiány, nem a mondat hibája.
- **Hatókör (V4).** A rés mondata helycsoportra szól („a motívum hat újszövetségi helyén”, „az újszövetségi helyeken”), és a lánc vagy a motívum szavát állítja. Ha a csoportban tematikus hely van (`gerinc_elem` `tematikus:`), és a mondat ezt nem mondja ki, ⚑ jár.
- **Tesztek:** `eszkozok/teszt_proza_allitas.py`, `F206` osztály, 9 teszt. Az esetek:
  - nincs sor / közepes / magas;
  - kapcsolat-ige nélkül;
  - a motívumon kívüli hely;
  - a motívum helye sor nélkül;
  - kapcsolat-adat nélküli motívum;
  - „visszatérés” főnév;
  - hatókör kimondva és kimondatlanul.
  
  Teljes futás: 29 OK.
- **Mérés:**
  - HAMART-001, javítás előtti forrás, `--lektor`: gépi 5, kézi 19 (⚑ 13), nem látja 10. Előtte: 5 / 18 (⚑ 9) / 11. Az új jelzés a 10., 12., 14. és 40. tételt fogja meg. A kézi lista 200 helyett 201 sor.
  - A többi motívum (ISTENTISZT-001, ALVIL-001, TEREMT-001, TEREMT-002, KIRALY-001, HODIT-001, MENNY-001): 0 új jelzés.
- **Kapu-szint:** változatlanul JELENTÉS (DT785).

## Ami gépileg nem fogható — a lektor dolga marad

- **V1 szerkezeti része:** ki az alany, mit mond a vers, melyik tagmondathoz tartozik egy szó. A kézi lista mutatja, az ítélet a második kézé (N-F200b) és a lektoré.
- **V6:** olvasat a szövegnek tulajdonítva, forrásnak (szerzőnek) tulajdonított többlet.
- **V7:** bevezetetlen fogalom, nem fedő címke, ismétlés.
- **V8:** a lap eleje és a Kivonat határszabályának egyezése (két szabad szöveg).
- **V11:** a proveniencia-sor megléte a rés új lekérdezés-állításai mellett (ezt a független ellenőr nézi).

## Nyitott (külön tétel)

- **N-F206a:** az `olvasoi_kapu.py` belső szavainak bővítése (V9) a #699 merge-e után.
- **N-F206b:** a `/lap-javit` javításának társ-példányai (V12).

## Független ellenőrzés és javítókör

*(a menet végén kerül ide)*
