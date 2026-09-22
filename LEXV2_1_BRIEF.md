# LEXV2_1_BRIEF.md — v1

Lexikon-oldal v2, 1. menet: adatforrások. UBS Dictionary of New Testament Greek (jelentések + igehely-hivatkozások) és Open Scriptorium Rahlfs-LXX importja, próba-hozzárendelés, összevetés. **Generátor nem változik.**

## 0. Kiindulás — mérve, `f9142a4` (2026.09.22)

- A `konkordancia/SDGNT_domenek.tsv` az UBS görög szótárból (`ubsicap/ubs-open-license` @ `3a6edd8`, `UBSGreekNTDic-v1.1-en.JSON`) csak a doméneket vette át. A JSON jelentésenként tartalmazza: `LEXEntryCode` (Louw–Nida), `LEXSenses[en].DefinitionShort/DefinitionLong/Glosses/Comments`, `LEXReferences` (14 jegyű: `BBBCCCVVVWWWWW`, könyv 040 = Mt … 066 = Jel, utolsó 5 jegy a szópozíció). 5 507 bejegyzés.
- Az `elofordulasok.tsv` 42 ÚSZ-sorából 36-nak van G-tokenje; próbamérés szerint 32 sor egyértelműen UBS-jelentéshez köthető a verskulcs + Strong egyezésével, 17 különböző jelentéssel. Nem ment: 3 igehely-tartomány (Róm 8:20-22, Zsid 6:7-8, Zsid 7:1-28) és 1Kor 2:15 (G4151 nincs a versben).
- A `konkordancia/LXX_kivonat_*.tsv` licence `tisztazatlan` (N15). Jelölt forrás: Open Scriptorium Rahlfs-LXX (openscriptorium.org, szöveg közkincs, szószintű adat lxx-morph, CC BY 4.0); a szavakon `strongs_number` üres, a Strong a lemma-táblából jön (`lemma.id` → `strongs_numbers`, lista).

## 1. A feladat

(a) UBS NT-szótár jelentés- és hivatkozás-kivonata; (b) próba-hozzárendelés az ÚSZ-sorokhoz; (c) Open Scriptorium LXX-kivonat; (d) összevetés a régi LXX-kivonattal és számozás-eltérés-jelentés; (e) N15 állapotfrissítés.

## 2. G-döntések

- **G1:** az UBS-import ugyanarra a rögzített commitra (`3a6edd8`) és sha256-ra épül, mint az SDBH/SDGNT-import. Licenc: CC BY-SA 4.0, a README meglévő forrásmegjelölésével.
- **G2:** a hozzárendelés **származtatott**, nem kerül az `elofordulasok.tsv`-be. Csak próba-jelentés készül; a lexikon-oldal a 2. menetben renderidőben számolja.
- **G3:** igehely-tartománynál (`Róm 8:20-22`) a tartomány minden versét vizsgáld; több egyező jelentésnél mind kerüljön a jelentésbe `egyertelmu=nem` jelöléssel.
- **G4:** az Open Scriptorium-adat a teljes SQLite-letöltésből jön (nem az API-ból). Az URL-t a `https://openscriptorium.org/downloads` oldalról vedd; rögzítsd az URL-t, a letöltés dátumát és az sha256-ot. A licencet a letöltött adatbázis saját metaadatából is olvasd ki, és rögzítsd.
- **G5:** az LXX-kivonat az LXX **saját számozását** tartja (`igehely_lxx`), és mellé tesz egy `igehely_karoli` oszlopot. Ahol a kettő eltérhet (legalább: Zsoltárok, Jeremiás, Dániel, Eszter), a `igehely_karoli` üresen marad, hacsak az adatbázis maga nem ad megfeleltetést. Számozás-leképezést ez a menet nem talál ki. ⛔ Ha a szükséges versek (5. pont) több mint 10%-ánál hiányzik a Károli-igehely, állj meg.
- **G6:** a régi `LXX_kivonat_*.tsv` fájlok maradnak (a generátor még azokat használja). Az új kivonat mellé kerül.

## 3. Mi NEM hatókör

Generátor-, sablon- vagy lexikon-oldal-változás; `elofordulasok.tsv`, `lexikon_hivatkozasok.tsv` módosítása; fordítás; a héber SDBH-definíciók.

## 4. Tételek

### V1.0 — kiindulás *(nem commitol)*
HEAD szülője `f9142a4`, tiszta fa, `ellenoriz.py` 6·0·3·1.

### V1.1 — UBS NT-szótár kivonat
Új szkript: `eszkozok/ubs_dntg_import.py` (a `sdbh_sdgnt_import.py` letöltő- és sha-ellenőrző logikáját használja). Kimenet, fejléc-kommentben forrással, sha-val, licenccel:
- `konkordancia/UBS_DNTG_jelentesek.tsv`: `strong | strong_kod | lemma | main_id | lexid | entry_kod | domen_kod | domen | definicio_rovid | definicio_hosszu | glosszak | megjegyzes` (a glosszák `; `-vel; a mezőkön belüli tab/újsor szóközzé).
- `konkordancia/UBS_DNTG_referenciak.tsv`: `lexid | strong | igehely | szopozicio | ref_kod` (az igehely Károli-rövidítéssel, `ApCsel 2:21` formában; a könyvkód-táblát a szkript tartalmazza, 040=Mt … 066=Jel).
A `konkordancia/SDBH_SDGNT_README.md` kapjon egy „UBS NT-szótár: jelentések és hivatkozások" szakaszt (fájlok, oszlopok, sorszámok).

### V1.2 — próba-hozzárendelés
Új szkript: `eszkozok/ubs_hozzarendeles.py`. Az `elofordulasok.tsv` minden ÚSZ-sorára (G3 szerint tartományokkal): a sor G-tokenjei × a vers(ek) UBS-referenciái. Kimenet: `naplok/LEXV2_ubs_hozzarendeles_proba.tsv`: `id | igehely | strong | lexid | entry_kod | glosszak | egyertelmu | megjegyzes`. Nem egyező sornál `lexid` üres, a `megjegyzes` az okot írja (pl. „a token nincs a versben").

### V1.3 — Open Scriptorium LXX-kivonat
Új szkript: `eszkozok/lxx_os_import.py` (`--letolt` letölt, egyébként a helyi példányból dolgozik; a SQLite **nem** kerül a repóba, csak a szkript, az sha és a kivonat). Először írd le a séma releváns tábláit a README-be. Kimenet könyvenként: `konkordancia/LXX_OS/<könyv>.tsv`: `igehely_lxx | igehely_karoli | pozicio | szoalak | normalizalt | lemma | lemma_id | strong | morf | proveniencia` (`strong` a lemma `strongs_numbers` listája `;`-vel; üres, ha nincs). README: `konkordancia/LXX_OS/README.md` — forrás, URL, dátum, sha256, licenc (Rahlfs 1935 közkincs; szószintű adat: lxx-morph, `git.sr.ht/~sethkush/lxx-morph`, CC BY 4.0, kötelező megjelöléssel), oszlopok, sorszámok könyvenként, számozási megjegyzés.

### V1.4 — összevetés
Új szkript: `eszkozok/lxx_osszevetes.py`. A régi kivonat és az új kivonat összevetése a 8 motívum ÓSZ-igehelyein a motívumok G-tokenjeire (amit a generátor ma keres). Kimenet: `naplok/LEXV2_lxx_osszevetes.tsv`: `id | igehely | strong | regi_talalat | uj_talalat | uj_szoalak | uj_lemma | megjegyzes`, és a zárójelentésben összesítő: egyezik / csak régi / csak új / számozás miatt nem párosítható.

### V1.5 — N15 állapot
A `NYITOTT_FELADATOK.md` N15 blokkjának végére új bekezdés: `  **Állapot (LEXV2_1, 2026.09.22):** az Open Scriptorium-kivonat elkészült (\`konkordancia/LXX_OS/\`), összevetés: \`naplok/LEXV2_lxx_osszevetes.tsv\`; a generátor átállítása a lexikon-oldal v2 (2. menet) része. Az N15 akkor zárul, ha a régi kivonat kikerül a generált rétegből.`

## 5. Várt számok

| Mérés | Várt |
|---|---|
| UBS NT bejegyzés | 5 507 |
| `UBS_DNTG_jelentesek.tsv` sor | mérendő (a SDGNT 9 178 jelentés-egységéhez közel) |
| ÚSZ-sor / G-tokennel | 42 / 36 |
| Próba: egyértelműen hozzárendelt sor | ≥ 32 (tartományokkal várhatóan 35) |
| Próba: különböző jelentés | ≈ 17–20 |
| LXX_OS: könyvek száma | mérendő; a Rahlfs-korpusz könyvei |
| Szükséges versek Károli-igehely nélkül | ≤ 10% (G5 ⛔) |

## 6. Elfogadási kritériumok

- **K1:** mindkét UBS-kivonat fejléce tartalmazza a forrást, a commitot, az sha-t és a licencet; a szkript `--letolt` nélkül is reprodukálja a kimenetet.
- **K2:** a próba-hozzárendelés minden ÚSZ-sort tartalmaz (42), a nem egyezőket okkal.
- **K3:** az LXX_OS README-je rögzíti az URL-t, dátumot, sha256-ot, a licencet (az adatbázis saját metaadatával együtt) és a sémát.
- **K4:** a SQLite nincs a repóban; a legnagyobb kivonat-fájl < 50 MB.
- **K5:** az összevetés-táblában minden régi találat szerepel, párosítva vagy okkal.
- **K6:** `ellenoriz.py` 6·0·3·1; `general.py --cel mind --ellenoriz` semmit nem jelez változónak (a generált réteg érintetlen).
- **K7:** `git diff --stat` csak új fájlokat, a két README-t és a `NYITOTT_FELADATOK.md`-t mutatja.
- **K8:** a zárójelentés tartalmazza az 5. pont összes mért értékét és a számozási eltérések listáját.

## 7. Commitok

1. `LEXV2_1_BRIEF.md v1`
2. `V1.1: UBS NT-szótár jelentés- és hivatkozás-kivonat`
3. `V1.2: UBS-jelentés próba-hozzárendelés (ÚSZ-sorok)`
4. `V1.3: Open Scriptorium Rahlfs-LXX kivonat`
5. `V1.4: LXX régi–új összevetés`
6. `V1.5: N15 állapot`

Push a K1–K8 teljesülése után. ⛔ Utána megállás: a 2. menet (generátor) külön brief.

## Döntésnapló

| Verzió | Dátum | Döntés |
|---|---|---|
| v1 | 2026.09.22 | A felhasználó elfogadta a lexikon-oldal v2 javaslatot, az LXX-híd megújítását (N15) és az UBS NT-szótár beépítését. Két menet: 1. adatforrások (ez), 2. generátor. A UBS-jelentés hozzárendelése származtatott (nem az `elofordulasok.tsv`-be); az LXX saját számozás + Károli-oszlop, leképezés kitalálása nélkül; ⛔ megállás a menet végén. |
