---
feladat: 24
cim: Forrásaink licencének átnézése
kod: LICENC
tipus: feladat
fazis: 1
modell: sonnet
allapot: nem_indult
ad: adatkészletenként egy licencsor (licenc, verzió, kereskedelmi felhasználás, share-alike, kötelező megjelölés) egyetlen táblában, amelyre a render és a nyilvános kiadás épít
kovetkezo: /kovetkezo; külön ⛔ nincs, a tisztázatlan tételek összesítve a DONTESEK.md-be
olvas: [konkordancia/, adat/datasetek.tsv, adat/szotar_szerepek.tsv, eszkozok/general.py, Rendszerfejlesztesi_playbook.md]
ir: [adat/licencek.tsv, adat/SEMA.md]
fugg: []
nem_fugg: [22]
---

# F<nn>_LICENC_BRIEF.md — Forrásaink licencének átnézése

*FELADATOK #<nn> · Modell: sonnet · v1 · 2026.09.30 · döntés: D41 (a naplózó brief rögzíti)*

## 1. Cél

Egy tábla arról, hogy melyik forrás milyen licenc alatt használható, és mi következik ebből egy nyilvános vagy kereskedelmi kiadásra. Ez adatréteg-kérdés (D41), és most olcsó: utólag minden generált nézetet érintene. A tábla nem jogi vélemény, hanem leltár. A kereskedelmi döntés előtt jogásznak kell átnéznie.

## 2. Hatókör

**Benne van:** minden adatkészlet a `konkordancia/`-ban és a `adat/datasetek.tsv`-ben, a szerepmátrix minden forrása (`adat/szotar_szerepek.tsv`), valamint a futó importok forrásai (BSB, Macula, Nave, KJV/ASV), ha már van soruk.

**Nincs benne:** a sorszintű proveniencia átírása. A licenc **adatkészlet-szinten** él, és a sor a dataset-azonosítón át örökli. A render módosítása sem tartozik ide.

## 3. Lépések

1. **Leltár:** az összes adatkészlet listája a három forrásból, duplikátum nélkül.
2. **Licenc forrásonként:** a licencet a forrás saját dokumentumából vedd (README, LICENSE, kiadói oldal), a pontos hellyel.
   - A repóban már rögzített besorolásokat (`general.py` licenc-konstans, `TISZTAZATLAN_SZOTARAK`, `konkordancia/*/README.md`) vesd össze a talált licenccel.
   - Minden eltérés `javaslat` jelölést kap.
3. **Tábla:** `adat/licencek.tsv`, oszlopok:
   `dataset` · `licenc` · `verzio_vagy_commit` · `forras_hely` · `kereskedelmi` (`igen` / `nem` / `feltetelesen`) · `share_alike` (`igen` / `nem`) · `kotelezo_megjeloles` (szó szerint, ha van) · `allapot` (`tisztazott` / `tisztazatlan`) · `megjegyzes`.
4. **SEMA:** rövid alfejezet a tábla sémájáról, és arról, hogy ez a licenc egyetlen forrása. Ha a `NYITOTT_FELADATOK.md` N9 tétele (a licenc-besorolás kettős forrása) még nyitott, a naplóban javasold, hogyan zárható le ezzel a táblával. A `general.py`-hoz ne nyúlj.
5. **Összesítő `DONTESEK.md`-tétel** a `tisztazatlan` és a `javaslat` sorokkal, és a kérdéssel: melyik forrás maradjon a nyilvános nézetből kihagyva a tisztázásig.

## 4. Munkaszabályok

1. Licencet nem találunk ki. Ha a forrás nem mond semmit, az érték `tisztazatlan`, nem feltételezés.
2. A `share_alike = igen` forrásoknál (pl. CC BY-SA) a megjegyzésbe kerüljön: a belőlük származó réteg nem zárható el, a kiadásban külön jelölendő.
3. Menet közben nincs ⛔. Minden kérdés az 5. pont összesítő tételébe gyűlik (D19).
4. Zárás a `/kovetkezo` szerint: `fuggetlen-ellenor`, zárójelentés, draft PR, a saját fejléc frissítése.

## 5. Kész, ha

- K1: a leltár minden adatkészletének van sora a `adat/licencek.tsv`-ben. Ezt a zárójelentés számokkal igazolja: leltár = sorszám.
- K2: minden `tisztazott` sornak van `forras_hely`-e.
- K3: a SEMA-alfejezet kész, és a `DONTESEK.md`-tétel nyitva van.
- K4: a `fuggetlen-ellenor` jelentése `TISZTA`.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.09.30 | első változat | adatkészlet-szintű licenc, nem soronkénti oszlop (kevesebb írás, egy igazságforrás); nem jogi vélemény, hanem leltár |
