# F239 — döntések (a TEREMT-001 cikke)

*Az integrátor döntései a menet kérdéseire (MUNKAMENET „Szereposztás”, #835); forrás: szerkesztői döntés (az integrátor, a felhasználó felhatalmazásával).*

**D1** (2026-11-23, U4b; az integrátor: `local_ee039369`). *Kérdés:* hova kerüljön a mérőtáblában az U3b-ben megfogott pontossági hiba (2Móz 15:5 βυθός → πόντος)? A SEMA 2.72 `hol` értékkészletében nem volt helye. — *Döntés:* (A) új `hol` érték: `visszhang` (a visszhang-réteg összevetése a prózával, U1b/U3b), és S022 sor a hibával, `sulyos=igen`. — *Indok:* a mérőtábla minden megfogott pontossági hibát számol; a kimaradó sor a „hol fogtuk meg” arányt torzítja, a lépés pedig a cikkírás menetének állandó része (C-vh a próza előtt, az összevetés utána). — *Végrehajtva:* S022 a `naplok/SZIVARGAS_TEREMT-001.tsv`-ben; a szabályhely a SEMA 2.72 és a MUNKAMENET C-sz (külön commit). Az értékkészletet gépi kapu nem ellenőrzi.

## Az U5 döntései (a szerkesztő, 2026-11-23)

*Forrás mindegyiknél: **a szerkesztő döntése** (az U5-nézés, 2026-11-23; az integrátor kérdései, a szerkesztő minden pontnál a javasolt változatot választotta). A tétel-jelek a `naplok/F239_U5_csomag.md` jelei. A motívum határáról a D26 szól (a motívum határáról szóló szabály szerint): a szerkesztő szava, nem az integrátoré. A D24 és a D25 a határ szövegéről, a lapon álló megfogalmazásról szól. *(A fejléc a D27 szerint javítva, 2026-11-24.)*

**D2** (L37) *Kérdés:* tagolódjon-e a Kivonat első bekezdése (8 mondat, 21 igehely, a fordulópont középen)? — *Döntés:* két bekezdés; a fordulópontnál (ÓSZ víz → ÚSZ zárt hely) új bekezdés, a tartalom nem változik. — *Indok:* olvashatóság.

**D3** (L38) *Kérdés:* mennyire általánosíthat a fordulópont („ÓSZ: a tehóm víz; ÚSZ: az abüsszosz zárt hely”)? — *Döntés:* gyengítve („többnyire” jellegű megfogalmazás), a kivételek megnevezésével (Zsolt 71:20: seól; Róm 10:7, Luk 8:31, Jel 11:7, 17:8: nem zárás); az irány megmarad. — *Indok:* a mondat a kivételekre nem igaz.

**D4** (L18, L27, L30) *Kérdés:* Jel 20:3 — a mélységet vagy a sárkányt zárják be (TR, Károli „bezárá azt”)? — *Döntés:* közös olvasat: „a sárkányt a mélységbe vetik és bezárják”; a pecsét a kritikai szöveg szerint „fölötte”, ezt jelölve. Az L30 „mindkét helyen a mélységet zárják be” mondata ennek megfelelően pontosodik (az 1Móz 8:2-ben a források záródnak). — *Indok:* mindkét szöveghagyományban igaz megfogalmazás.

**D5** (L29, L44) *Kérdés:* „a mélységnek királya / uralkodója van” (Jel 9:11)? — *Döntés:* a vers szerint: „a sáskák királya a mélység angyala, a Vesztő”, mindkét helyen (Remez és a 2. szakasz Funkció-mondata). — *Indok:* a vers ezt mondja.

**D6** (L9, L20) *Kérdés:* „a mélység áldásai, mely alant terül” az 5Móz 33:13-ra is hivatkozik, ahol a Károli „mélységes vizeket” mond. — *Döntés:* az idézet csak az 1Móz 49:25-é; az 5Móz 33:13 a saját Károli-szövegével, párhuzamként áll (Kivonat és Peshat). Ezzel az F1 79. sora (E41) is rendeződik. — *Indok:* az idézet szó szerinti egyezése.

**D7** (L24) *Kérdés:* a Drash mondata a Jón 2:6 „felhozásáról” (a 2:7 mondja, más szóval; az érvnapló a közös jegyet elvetette)? — *Döntés:* átíródik: a Jón 2:6 a mélység körülzárásáról szól, a felhozás nem közös jegy; a mondat az érvnaplóhoz igazodik. — *Indok:* a vers és az érvnapló.

**D8** (L25) *Kérdés:* „nagy mélység” négy vagy öt versben (Zsolt 78:15 nem egyértelmű)? — *Döntés:* „négy versben biztosan, a Zsolt 78:15-ben vitatottan”, a bizonytalanság jelölve. — *Indok:* a BDB és a Károli sem egyértelmű.

**D9** (L28) *Kérdés:* a „Septuaginta” és a „görög Ószövetség” azonosítása? — *Döntés:* az első előfordulásnál „Septuaginta (a görög Ószövetség)”, utána egy kifejezés a lapon végig. — *Indok:* egységes szóhasználat.

**D10** (L23) *Kérdés:* „hullámok” a 2Móz 15:5-ben és a 15:8-ban? — *Döntés:* versenként, a saját Károli-szavával (15:5 hullámok, 15:8 mélységes vizek). — *Indok:* a szöveg pontossága.

**D11** (L6) *Kérdés:* a Ráháb/sárkány/vízi szörnyek helyein „nincs a mélység szava” — de a Zsolt 148:7 és a Jób 41:32 tartalmazza. — *Döntés:* a mondat csak azokra a helyekre szól, ahol valóban nincs (pl. Ézs 51:9), a két kivétel megnevezve; a „lexikai keresés” olvasóibb szóra cserélődik. — *Indok:* a mondat két helyre nem igaz.

**D12** (L41) *Kérdés:* a helyek száma bontással nőtt 42-ről 43-ra. — *Döntés:* egy mondat: „a helyek száma azért 43, mert egy hely kettébomlott; új hely nem került be.” — *Indok:* az olvasó különben új helyet sejt.

**D13** (L8) *Kérdés:* Róm 10:7 — tény és nyitott kérdés egy mondatban. — *Döntés:* kettéválik: előbb a tény, külön mondatban a nyitott kérdés, kérdésként jelölve (mint a Vitatott pontban). — *Indok:* tény és olvasat szétválasztása.

**D14** (L10) *Kérdés:* „a négy hely négy különböző dolgot mond” (jelöletlen olvasat) és „a későbbi könyvek ezeket hozzák vissza” (átvételt állít). — *Döntés:* az első rész olvasatként jelölve; a második „ugyanez a szó tér vissza” alakban, átvételt nem állít. — *Indok:* az adat csak szóismétlést mutat.

**D15** (L15) *Kérdés:* „hét versben áll együtt a leszállás vagy a felhozás igéjével” — négy versben nem a mélységbe/-ből való mozgás. — *Döntés:* a szám és a versek csak ott, ahol a mozgás a mélységbe vagy onnan történik; a többi kimarad vagy külön áll. — *Indok:* a mondat négy versre nem igaz.

**D16** (L11) *Kérdés:* a „2Móz 15-ben a mélység a tenger része” érv nincs az érvnaplóban. — *Döntés:* bekerül az érvnaplóba az adat támogatásával; a próza marad. — *Indok:* az adat alátámasztja.

**D17** (L12) *Kérdés:* Tiámat — „nem cselekszik Isten ellen” csak a másik olvasat érveként áll, holott hiányérv, a „demitologizált átvétel” olvasattal is összefér. — *Döntés:* a próza kimondja: a hiányérv mindkét olvasattal összefér, egyikük döntő érveként sem áll. — *Indok:* az érvnapló minősítése.

**D18** (L36) *Kérdés:* a „szóbeli kapcsolat nincs” mondat (az elvetett „közös zár-ige hiánya” érv). — *Döntés:* kimarad. — *Indok:* az érvnapló elvetette.

**D19** (L21) *Kérdés:* Sod — „a mélység határa mindig kívülről, felülről szabott” mind a 43 helyre. — *Döntés:* szűkül a határról beszélő helyekre (megnevezve); az „Isten akaratából” olvasatként jelölve. — *Indok:* határról csak néhány hely beszél; a második rész következtetés.

**D20** (L22) *Kérdés:* „a kulcs egyszer sem a mélységé” — a vers szerint „a mélységnek kulcsa”. — *Döntés:* átfogalmazódik („a mélység kulcsa nem a mélységnél van, más kapja” jelleggel), és a kikötés: a kulcs és a nyit–zár a Jelenések általános szókincse. — *Indok:* a vers szövege.

**D21** (O45) *Kérdés:* Zsolt 36:7 — az ismétlő „hasonlat … két végpontjával méri” mondat. — *Döntés:* kimarad, az előző marad. — *Indok:* ismétlés.

**D22** (O8) *Kérdés:* a Septuaginta-többlet 3 vagy 4 vers, és hova tartozik a Jób 41:31? — *Döntés:* az adat dönt: a javítókör lekérdezéssel megállapítja a számot és a Jób 41:31 helyét (proveniencia-sorral), a próza mindkét helyen ehhez igazodik. — *Indok:* a szám adat, nem értelmezés.

**D23** (O87) *Kérdés:* 1Móz 49:25 — a táblázat γῆ-t ad („eltérő”), a próza szerint a görögben nincs a mélység szava. — *Döntés:* egy mondat a kettőről: „a görögben a mélység helyén a »föld« (γῆ) áll”; a próza és a táblázat ugyanazt mondja. — *Indok:* a kettő nem mond ellent, csak külön áll.

**D24** (O98) *Kérdés:* a Kivonat két szomszéd motívumot ígér (köztük a tohú va-vohút), a 8. szakaszban az ALVIL-001 és egy döntésre váró ISTENTISZT-001 áll. — *Döntés:* a próza az adathoz igazodik: a Kivonat csak azt ígéri, ami a motívumközi kapcsolatok adatában áll; a tohú va-vohú kimarad; új kapcsolat nem kerül be. — *Indok:* a próza az adat nézete.

**D25** (O107) *Kérdés:* Euszébiosz, *De ecclesiastica theologia* „3. sz.”. — *Döntés:* adathiba: a visszhang-tábla kora 4. sz.-ra javítva, forrással igazolva, a javítókörben. — *Indok:* a mű 4. századi.

**D26** (O3, O5 — a motívum határának szövege, a határ-szabály szerint; **a szerkesztő szava**) *Kérdés:* a negatív kritérium „gyököt kell tartalmaznia” formulája (O3) és a fölérendelt fogalom „lexémán kívül” formulája (O5) maradjon-e? — *Döntés:* mindkettő marad. — *Indok:* minden lexémai motívum egységes formulája; csere csak az összesben egyszerre, külön döntéssel. A határ tartalma nem változik. (Az O3 kisbetű/pont-hibája generátorhiba, J1, a 218c-é.)

## A (b) csoport (javítás gazdával, döntés nélkül)
Az L17 (= K36) és az O7 (= K9, K70, a „95”), valamint a 12 forrástétel (F2: K2, K9, K19, K20, K36, K47, K69, K70, K99; F1 79. sor; a független ellenőr két prózai ELTÉRÉS-e) a javítókörben javul, a fenti döntésekkel összhangban (a K2 Kivonat-része: D7; a K19/K20: a BDB-helyek válogatás voltának jelzése; az F1 79. sora: D6).

## Az U6 utáni döntések (az integrátor, 2026-11-24)

*Forrás mindegyiknél: szerkesztői döntés (az integrátor, `local_5140778b`, a felhasználó felhatalmazásával; MUNKAMENET „Szereposztás”).*

**D27** *Kérdés:* a döntésnapló fejléce szerint „a D24 és a D25 a motívum határának szövegéről szól”, a határ-döntés viszont a D26; javuljon-e? — *Döntés:* igen: a fejléc szerint a motívum határáról a D26 szól, a D24 és a D25 a határ szövegéről (a lapon álló megfogalmazásról). — *Indok:* a fejléc félrevezető, és a határ a szerkesztőé, ezért pontosan kell látszania, melyik döntés az. — *Végrehajtva:* a fejléc javítva (F239.41).

**D28** *Kérdés:* behozza-e most az ág a main-t (az ág 127 committal a main mögött jár)? — *Döntés:* most nem; a kiadás az átállás (218c) után jön, akkor egyszer, a végleges generátorral. — *Indok:* kétszeri összefésülés helyett egy.

**D29** *Kérdés:* a szerkesztő elé kerül-e most az U6 változásnézete (33 blokk)? — *Döntés:* most nem; a kiadás nézési csomagjába kerül (C-v: próza, nyitott döntések, változáslista), egyetlen nézéssel. Az `adat/lap_javitasok.tsv` `jovahagyta` sora akkor kerül be. — *Indok:* a szerkesztő egyszer nézze a végleges, új generátoros lapot.

**D30** *Kérdés:* kell-e külön újramérés a 13, az U6-ban javított F2-kifogásra (a jelentés H38–H49 sorai)? — *Döntés:* nem; a kiadás előtti lektor és átnézés (2.7) a hibahely-táblán át célzottan nézi őket. — *Indok:* egy ellenőrzés, egy javítókör; a célzott nézés a kiadás menetében úgyis lefut.
