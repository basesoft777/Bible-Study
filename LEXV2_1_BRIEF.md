# LEXV2_1_BRIEF.md — v4

Lexikon-oldal v2, 1. menet: adatforrások. UBS Dictionary of New Testament Greek (jelentések + igehely-hivatkozások) és Open Scriptorium Rahlfs-LXX importja, próba-hozzárendelés, összevetés. **Generátor nem változik.**

## 0. Kiindulás — mérve, `f9142a4` (2026.09.22)

- A `konkordancia/SDGNT_domenek.tsv` az UBS görög szótárból (`ubsicap/ubs-open-license` @ `3a6edd8`, `UBSGreekNTDic-v1.1-en.JSON`) csak a doméneket vette át. A JSON jelentésenként tartalmazza: `LEXEntryCode` (Louw–Nida), `LEXSenses[en].DefinitionShort/DefinitionLong/Glosses/Comments`, `LEXReferences` (14 jegyű: `BBBCCCVVVWWWWW`, könyv 040 = Mt … 066 = Jel, utolsó 5 jegy a szópozíció). 5 507 bejegyzés.
- Az `elofordulasok.tsv`-ben **47 ÚSZ-sor** van, ebből **41-nek van G-tokenje** (36 egyverses sor + 5 igehely-tartomány: `Zsid 7:1-28`, `Róm 8:20-22`, `Zsid 6:7-8`, `Jel 9:1-2`, `Jel 20:1-3`). A maradék 6 sornak nincs G-tokenje (`MENNY-001` × 3, `HAMART-001` × 3: `Mt 15:19`, `Mk 7:21-23`, `2Pét 3:6-7`) — ezek a V1.2-ben „nincs G-token" jelöléssel szerepelnek, hozzárendelési kísérlet nélkül. Próbamérés szerint a 36 egyverses sorból 32 egyértelműen UBS-jelentéshez köthető a verskulcs + Strong egyezésével, 17 különböző jelentéssel; nem ment 1Kor 2:15 (G4151 nincs a versben) és a `Róm 8:20-22`/`Zsid 6:7-8`/`Zsid 7:1-28` tartományok (l. javítás alább — **a v1-ben itt tévesen 42/36 szerepelt, l. a döntésnaplót**).
- A `konkordancia/LXX_kivonat_*.tsv` licence `tisztazatlan` (N15). Jelölt forrás: Open Scriptorium Rahlfs-LXX (openscriptorium.org, szöveg közkincs). **V1.3 előtt kiderült** (l. a döntésnapló v3 bejegyzését): az Open Scriptorium letölthető bulk SQLite-ja (339 MB, `openscriptorium.org/downloads/openscriptorium.sqlite3`) **nem tartalmaz lemma-táblát és a `words.strongs_number` mezője a teljes rahlfs-lxx műre üres** (288 471/288 471 sor) — a `lemma.id → strongs_numbers` leképezés csak az élő API-n (`/api/v1/lemmas/:id`) érhető el, ott is csak szóalak-szintű `lemma.id`-vel, Strong nélkül a fejezet-válaszban. Emiatt a G4 forrása megváltozott: nem az SQLite és nem az API, hanem az **lxx-morph** projekt saját, szavankénti `lemma` mezőt tartalmazó JSON-kivonata (`github.com/OpenScriptorium/lxx-morph`, CC BY 4.0), a Strong-szám az **Open Scriptures Septuagint Project GreekWordList**-jéből (`github.com/openscriptures/GreekResources`, CC BY 4.0; csak az ÚSZ-ben is előforduló lemmáknak van Strong-száma — ez a forrás saját korlátja, nem hiba). A Károli-vers-megfeleltetéshez az lxx-morph saját, TVTMS-alapú `db/seeds/mt_alignment/verse_pairs.jsonl` fájlja ad angol/KJV-számozást; a KJV→Károli lépést a `konkordancia/Karoli_1908.tsv` fejezetenkénti versszám-egyezése dönti el (l. G5).

## 1. A feladat

(a) UBS NT-szótár jelentés- és hivatkozás-kivonata; (b) próba-hozzárendelés az ÚSZ-sorokhoz; (c) Open Scriptorium LXX-kivonat; (d) összevetés a régi LXX-kivonattal és számozás-eltérés-jelentés; (e) N15 állapotfrissítés.

## 2. G-döntések

- **G1:** az UBS-import ugyanarra a rögzített commitra (`3a6edd8`) és sha256-ra épül, mint az SDBH/SDGNT-import. Licenc: CC BY-SA 4.0, a README meglévő forrásmegjelölésével.
- **G2:** a hozzárendelés **származtatott**, nem kerül az `elofordulasok.tsv`-be. Csak próba-jelentés készül; a lexikon-oldal a 2. menetben renderidőben számolja.
- **G3:** igehely-tartománynál (`Róm 8:20-22`) a tartomány minden versét vizsgáld; több egyező jelentésnél mind kerüljön a jelentésbe `egyertelmu=nem` jelöléssel.
- **G4 (v3, módosítva):** az LXX szöveg + morfológia + lemma forrása az **lxx-morph** projekt `db/seeds/lxx_morph/<könyv>.json` fájljai (rögzített commit `c91f6b1e8fb3ba37df701e6ae31f675ace71a2b2`, CC BY 4.0). A Strong-szám forrása a **GreekWordList.js** (`openscriptures/GreekResources`, rögzített commit `dd5a2fd530ab3c6b748c174cec38966c356d8111`, CC BY 4.0); csak azoknak a lemmáknak van Strong-száma, amelyek az ÚSZ-ben is előfordulnak — ahol nincs, `strong` üres és `strong_ok=nincs_uszbeli_megfelelo`, ahol a lemma magában a GreekWordList-ben sincs, `strong_ok=lemma_nem_talalhato`. A Károli-vers-megfeleltetés forrása az lxx-morph `db/seeds/mt_alignment/verse_pairs.jsonl` (TVTMS-alapú, 99,57%-os auditált pontosság — ez a forrás saját auditja, nem a miénké) `mt_refs` mezője, **angol/KJV-számozásban** (`igehely_kjv` oszlop). Az Open Scriptorium bulk SQLite-ot (sha256 rögzítve, a repóba nem kerül) **csak ellenőrzésre** használja a szkript: könyvenként/versenként a szószám és a görög szóalak-sorozat egyezését veti össze az lxx-morph adatával, és a záró jelentésben listázza az eltéréseket. API-hívás nincs.
- **G5 (v3, módosítva):** az LXX-kivonat az LXX **saját számozását** tartja (`igehely_lxx`). Az `igehely_kjv` oszlop a `verse_pairs.jsonl` `mt_refs` értéke változtatás nélkül. Az `igehely_karoli` **csak akkor** kerül kitöltésre, ha az adott könyv+fejezetben a `Karoli_1908.tsv`-ben szereplő legmagasabb versszám **megegyezik** a `verse_pairs.jsonl` szerinti legmagasabb KJV-versszámmal abban a fejezetben (ez esetben vers-szinten megegyezőnek tekintjük a két számozást, és `igehely_karoli = igehely_kjv`). Ahol a fejezet két versszáma eltér, `igehely_karoli` üresen marad, `karoli_ok=szamozas_elteres` jelöléssel — ezeket a fejezeteket könyvenként listázza a jelentés. Külön jelölés jár azoknak a soroknak, ahol a versnek nincs MT-párja (`karoli_ok=nincs_mt_parositas`, a `verse_pairs.jsonl` `method=unpaired` sorai) és azoknak a könyveknek, amelyeknek nincs Károli-szövegük (deuterokanonikus/pszeudepigráf könyvek, `karoli_ok=nincs_karoli_konyv`). Saját KJV→Károli eltolási szabály nem épül; egy esetleges fejezet-szintű leképezés (a TVTMS héber oszlopa + Károli-versszám kézi ellenőrzése) külön N-tétel. ⛔ **A küszöb a szükséges versekre vonatkozik** (az `elofordulasok.tsv` ÓSZ-sorainak versei, tartományoknál minden vers — nem a teljes korpuszra): ha ezeknek több mint 10%-ánál `igehely_karoli` üres, állj meg.
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

### V1.3 — LXX-kivonat (lxx-morph + GreekWordList, SQLite csak ellenőrzésre)
Új szkript: `eszkozok/lxx_os_import.py` (`--letolt` letölt a rögzített commitokról, egyébként a helyi példányból dolgozik; sem a bulk SQLite, sem a nyers forrásfájlok nem kerülnek a repóba, csak a szkript és a kivonat). Kimenet könyvenként: `konkordancia/LXX_OS/<könyv>.tsv`, fejléc: `igehely_lxx | igehely_kjv | igehely_karoli | karoli_ok | pozicio | szoalak | normalizalt | lemma | morf | strong | strong_ok | proveniencia`.
- `igehely_lxx` — a könyv saját (lxx-morph `ref`) fejezet:vers címe.
- `igehely_kjv` — `verse_pairs.jsonl` `mt_refs` értéke(i), `;`-vel, ha több.
- `igehely_karoli` / `karoli_ok` — G5 szerint (`szamozas_elteres` / `nincs_mt_parositas` / `nincs_karoli_konyv` / üres `karoli_ok`, ha egyezik).
- `pozicio` — a szó 1-alapú sorszáma a versen belül.
- `szoalak` / `normalizalt` — az lxx-morph `surface`, illetve ékezet nélkülire normalizált alakja.
- `lemma` / `morf` — az lxx-morph `lemma`, illetve `pos`+`parsing` összefűzve.
- `strong` / `strong_ok` — a GreekWordList szerint (üres `strong_ok`, ha van Strong; `nincs_uszbeli_megfelelo` / `lemma_nem_talalhato` egyébként).
- `proveniencia` — `forras=lxx-morph@<commit> | forras=GreekWordList@<commit> | ts=<dátum>`.
README: `konkordancia/LXX_OS/README.md` — mindkét forrás URL-je, rögzített commitja, licence (lxx-morph és GreekWordList: CC BY 4.0; Rahlfs 1935 szövege: közkincs), a bulk SQLite ellenőrző szerepe (URL, letöltés dátuma, sha256, a repóba nem kerül), oszlopok, könyvenkénti sorszámok, a `karoli_ok≠üres` fejezetek/könyvek listája.

### V1.4 — összevetés
Új szkript: `eszkozok/lxx_osszevetes.py`. A régi kivonat és az új kivonat összevetése a 8 motívum ÓSZ-igehelyein a motívumok G-tokenjeire (amit a generátor ma keres). Kimenet: `naplok/LEXV2_lxx_osszevetes.tsv`: `id | igehely | strong | regi_talalat | uj_talalat | uj_szoalak | uj_lemma | megjegyzes`, és a zárójelentésben összesítő: egyezik / csak régi / csak új / számozás miatt nem párosítható.

### V1.5 — N15 állapot
A `NYITOTT_FELADATOK.md` N15 blokkjának végére új bekezdés: `  **Állapot (LEXV2_1, 2026.09.22):** az Open Scriptorium-kivonat elkészült (\`konkordancia/LXX_OS/\`), összevetés: \`naplok/LEXV2_lxx_osszevetes.tsv\`; a generátor átállítása a lexikon-oldal v2 (2. menet) része. Az N15 akkor zárul, ha a régi kivonat kikerül a generált rétegből.`

## 5. Várt számok

| Mérés | Várt |
|---|---|
| UBS NT bejegyzés | 5 507 |
| `UBS_DNTG_jelentesek.tsv` sor | mérendő (a SDGNT 9 178 jelentés-egységéhez közel) |
| ÚSZ-sor / G-tokennel | 47 / 41 (36 egyverses + 5 tartomány) |
| Próba: egyértelműen hozzárendelt sor | ≥ 32 (tartományokkal várhatóan 35) |
| Próba: különböző jelentés | ≈ 17–20 |
| LXX_OS: könyvek száma | mérendő; a Rahlfs-korpusz könyvei |
| Szükséges versek Károli-igehely nélkül | ≤ 10% (G5 ⛔) |

## 6. Elfogadási kritériumok

- **K1:** mindkét UBS-kivonat fejléce tartalmazza a forrást, a commitot, az sha-t és a licencet; a szkript `--letolt` nélkül is reprodukálja a kimenetet.
- **K2:** a próba-hozzárendelés minden ÚSZ-sort tartalmaz (42), a nem egyezőket okkal.
- **K3:** az LXX_OS README-je rögzíti mindkét forrás (lxx-morph, GreekWordList) URL-jét, commitját, licencét, az ellenőrző SQLite URL-jét/dátumát/sha256-ját, és a sémát.
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
| v2 | 2026.09.22 | V1.1 után, V1.2 előtt kiderült: a 0. és 5. pont „42 ÚSZ-sor / 36 G-tokenes" száma hibás volt — a tényleges `f9142a4` állapotban 47 ÚSZ-sor van, 41 G-tokennel (a v1 száma az 5 igehely-tartomány sort tévesen kihagyta az alapszámból, miközben a G3 tétel kifejezetten előírja a tartományok feldolgozását). A felhasználó döntése: a V1.2 mind a 41 G-tokenes sort dolgozza fel a tartományokkal együtt (G3 szerint); a 0. és 5. pont száma erre javítva; a 6 G-token nélküli sor a próba-jelentésben „nincs G-token" jelöléssel szerepel. |
| v3 | 2026.09.22 | V1.2 után, V1.3 közben két blokkoló felfedezés: (1) az Open Scriptorium bulk SQLite-ja nem tartalmaz lemma-táblát, a `words.strongs_number` a teljes rahlfs-lxx műre üres — a lemma/Strong csak az élő API-n érhető el, ami ütközik az eredeti G4-gyel; (2) a G5 eredeti ⛔ küszöbe (≤10% hiányzó Károli-igehely) és a Zsoltárok/Jeremiás helyes (üres) kezelése összeegyeztethetetlen a teljes korpuszon (a két könyv önmagában 16,6%). A felhasználó döntése: (1) G4 forrása lxx-morph (szavankénti lemma, CC BY 4.0) + GreekWordList (lemma→Strong, CC BY 4.0) + lxx-morph saját TVTMS-alapú MT↔LXX vers-megfeleltetése (`mt_alignment/verse_pairs.jsonl`); a bulk SQLite csak ellenőrzésre, API-hívás nincs. (2) A G5 ⛔ küszöbe a szükséges versekre (az `elofordulasok.tsv` ÓSZ-sorainak versei) vonatkozik, nem a teljes korpuszra; a teljes korpuszon a Zsoltárok/Jeremiás üres `igehely_karoli`-ja küszöb nélkül helyes. A KJV→Károli lépés a `Karoli_1908.tsv` fejezetenkénti versszám-egyezésén alapul, saját eltolási szabály építése nélkül. |
| v4 | 2026.09.22 | **Független ellenőrzés hibát talált a leadott V1.3-ban**: az `igehely_karoli` rossz Károli-célt adott (pl. LXX(Zsolt) 50:3 → hibásan „Zsolt 50:3" a helyes „Zsolt 51:3" helyett). Ok: a `LXX_versificacios_terkep.tsv` a studybible.info saját belső oldal-verszámozására épült, ami cím-viselő zsoltároknál nem esik egybe az lxx-morph saját `ref`-jeivel. **V1.3a javítás:** a térkép teljesen kikerült az `igehely_karoli` számításából; új algoritmus: (1) `KEZI_ELTOLASOK` (raw-alapú, változatlan); (2) KJV-fejezet-egyezés (`verse_pairs.jsonl` + `Karoli_1908.tsv` fejezetenkénti legmagasabb versszám-összevetés); (3) Zsoltár cím-eltolás (`d`∈{1,2}, `karoli_ok=zsolt_felirat_eltolas`), „ellenpróbával" a cím-többesértelműségre (több LXX-forrás egy KJV-célra — csak a legmagasabb/utolsó kapja az eltolást); (4) minden más eltérés üres + `szamozas_elteres`. Új automatikus ellenőrzés minden futáskor (Károli-fejezet = KJV-fejezet a kitöltött sorokban, kivéve a kézi táblákat) — 0 figyelmeztetés. Tartalmi szúrópróba (27 minta) mind egyezik. G5-küszöb újramérve: 11/229 = 4,80% (a hibás verzióban 6,55%). A V1.4 összevetés újrafuttatva. A felfedezés gyanút keltett a **régi**, még mindig használt `LXX_kivonat_Zsoltarok.tsv`-re is — külön N-tételként (N17) rögzítve, e menetnek nem hatóköre. |
