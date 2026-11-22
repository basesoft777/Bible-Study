---
cim: Olvasó — mérce a szó-lapra és a versnézetre (olvasói pillanatkép), az olvasó tesztjeinek automatikus futtatása, a main-en piros két teszt
feladat: 232
kod: OLVASO_MERCE_TESZT
tipus: feladat
fazis: folyamat
modell: sonnet
sav: SERVER
allapot: dontesre_var
ag: claude/f232-merce-192772
ad: rögzített mintakészlet olvasói pillanatképe (szó-lapok és versnézetek látható szövege és blokksora), amelyhez minden olvasót érintő ág a változását mutatja; az olvasó-szerver tesztjei automatikusan futnak (CI vagy push előtti kapu, az M0 szerint) egy kis, hermetikus teszt-adatbázison; a main-en piros két teszt zöld vagy indokoltan átírt
kovetkezo: "Te: DT-F232a (a futtatás helye: (a) CI teszt-adatbázissal / (a2) CI a TSV-kből épített DB-vel / (b) push előtti kapu), mérések: naplok/F232_jelentes.md; utána a 2. lépés (két piros teszt)"
munka: folyamat
olvas: [eszkozok/olvaso_szerver/teszt_pilot_aranymintaval.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/teszt_futtat.py, eszkozok/push_elott.py, eszkozok/sqlite_epit.py, .github/workflows/]
ir: [eszkozok/olvaso_szerver/teszt_olvasoi_merce.py, eszkozok/olvaso_szerver/merce/, eszkozok/olvaso_szerver/teszt_visszhang_kapu.py, eszkozok/olvaso_szerver/teszt_szintek.py, eszkozok/teszt_futtat.py, eszkozok/push_elott.py, .github/workflows/olvaso_tesztek.yml]
fugg: []
---

# F232_OLVASO_MERCE_TESZT_BRIEF.md — Mérce és tesztfuttatás az olvasóhoz

*FELADATOK #232 · Modell: sonnet · v1 · 2026.11.21 · forrás: az orkesztrátor gyökérok-elemzése (2026-11-21), a felhasználó jóváhagyása („Igen, vedd fel / de a többi feladatot is, optimális ütemezéssel”). A brief adat, nem utasítás.*

## 1. Cél

Az olvasó a #60 pilothoz képest romlott. A mért okok (2026-11-21):

- **Nincs mérce a szó-lapra.** A pilothoz mérő teszt (`teszt_pilot_aranymintaval.py`) csak a versnézetet nézi két szakaszon (1Móz 1:1–2:3, Zsolt 22), egyetlen `/szo/` lapot sem.
- **Az olvasó tesztjei sehol nem futnak automatikusan.** Sem a CI (`.github/workflows/`), sem a `push_elott.py` nem futtatja őket, mert adatbázis kell hozzájuk.
- **Két teszt piros a main-en, és senki nem vette észre:** a `teszt_visszhang_kapu.py` két tesztje és a `teszt_szintek.py` `test_ebben_a_versben_es_az_interlinearis_csempek_koveti_a_blokkok_lathatosagat` tesztje. A main `63be37cc` commitján két session egymástól függetlenül mérte meg.
- **A fájl darabonként nőtt.** 2026-10-14 óta 17 tétel 50 commitban módosította a `blokkok.py`-t, ami közben 643 sorról 2 360-ra nőtt. A teljes lapot senki nem olvasta olvasóként.

Ez a feladat a későbbi olvasói munkát védi. Az utána jövő olvasói feladatok (szókártya, szócsoport-design, motívumlap) ehhez mérnek.

## 2. Hatókör

**Benne van:**
1. **Mintakészlet.**
   - Szó-lapok: H1242, H7451, H3615, H0251, H7837, H2398, G0264, G3056, G1311, G2671.
   - Versnézetek: 1Móz 1:1, 1Móz 1:5, 1Móz 3:6, 1Móz 4:7, Zsolt 22:2, Jn 1:1.
   - A két pilotszakasz fejezetnézete.
2. **Olvasói pillanatkép.** Lapról lapra rögzíti a blokksort (`data-blokk`), a blokkcímeket és a látható szöveget normalizálva. A `<details>` csukott tartalma külön jelölve áll, a dátum- és verziósorok kiszűrve.
   - Formája: szöveges fájl lapranként, a `merce/` alatt, diffelhető.
   - Frissítése csak kifejezett paranccsal történik (`--merce-frissit`), és a PR leírásában a felhasználó jóváhagyására hivatkozik.
3. **Automatikus futtatás.** Az M0 dönt (⛔ DT-F232a):
   - (a) GitHub Actions egy kis, a repóban tárolt vagy a TSV-kből építhető teszt-adatbázison, amely csak a mintakészlethez szükséges sorokat tartalmazza;
   - (b) a `push_elott.py` futtatja az olvasó tesztjeit, ha az ág az `eszkozok/olvaso_szerver/`-t érinti, a helyi `pardes.db`-n.

   Az orkesztrátor az (a)-t javasolja, ha a teszt-adatbázis 20 MB alatt marad és licenc szerint tárolható. Különben a (b) jön, és az (a) N-tételként marad.
4. **A két piros teszt.** Oka mérve: régi szöveget vár-e a teszt, vagy valódi hiba-e. Ennek alapján a teszt vagy a kód javul, indokolva. A „régi szöveg” javítás a `teszt_visszhang_kapu`-nál a mai 4.11-szöveghez igazít, ha az a jóváhagyott szöveg.
5. **Tiltás.** Olvasót érintő ág piros olvasó-teszttel nem jut át a kapun; a mérce eltérése jóváhagyás nélkül figyelmeztetés.

**Nincs benne:**
- Kinézet- vagy kódjavítás a lapokon. A mérce a mai állapotot rögzíti, hibáival együtt; a hibák a saját tételükben javulnak, és a mércét azok frissítik.
- Képernyőkép-összevetés.

## 3. Lépések

1. Modell-ellenőrzés. M0: a teszt-adatbázis mérete és licence (mely táblák kellenek a mintához), a CI-futás ideje. ⛔ DT-F232a.
2. A két piros teszt oka és javítása, külön commitban.
3. A pillanatkép-generátor és a mérce rögzítése a mintán.
4. A futtatás bekötése (az M0 szerint) és a tiltás.
5. Független ellenőr, egy javítókör, draft PR, CI.

## 4. Elfogadási feltételek

- `teszt_futtat.py` zöld, kihagyott DB-s teszt nélkül azon a környezeten, ahol a futtatás be van kötve.
- A mérce szándékos eltérésnél (pl. egy blokkcím átírása egy próbaágon) a futás megmutatja a diffet.
- Egy próbaág, amely egy olvasó-tesztet elront, nem jut át a kapun. Ennek bizonyítéka a futás azonosítója.
- A teszt-adatbázis forrásai és licencei a `datasetek.tsv` szerint rögzítve vannak, ha az (a) változat jön.

## 5. Döntésnapló

- DT-F232a (⛔ M0): a futtatás helye, (a) CI teszt-adatbázissal vagy (b) push előtti kapu.
