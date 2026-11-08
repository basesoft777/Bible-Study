---
feladat: 176
cim: A visszhang-réteg adatrétege — ókori fordítások, ÚSZ szövegváltozat, BDB rokon írások gyorsítótára, arány-kapu
kod: VISSZHANG_ADAT
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: megallt
ag: claude/f176-visszhang-adat-c1579f
ad: új licencelt adatkészletek (Sefaria PD Targum, Clementina, SBLGNT-apparátus, TAGNT-változatjelölés) a konkordancia/ alatt, datasetek.tsv és licencek.tsv soraival; BDB rokon írások gyorsítótára és lekérő szkript, első futás a HAMART-001 láncszavaira; forrásonkénti arány-kapu a nyílt mag kapujában (1% / 5%)
kovetkezo: Te: /elteres F176 — az ELLENOR_F176 ELTÉRÉS (9 tétel; a DT-F176b eldöntve és átvezetve, a DT-F176a versszámozás nyitott: igehely = forrásszámozás, hamis karoli_kulcs)
munka: folyamat
olvas: [adat/datasetek.tsv, adat/licencek.tsv, adat/SEMA.md, Rendszerfejlesztesi_playbook.md, konkordancia/README.md, konkordancia/BDB_teljes_unabridged.tsv, konkordancia/TAGNT_kivonat.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, adat/elofordulasok.tsv, eszkozok/nyilt_mag_kapu.py]
ir: [konkordancia/Targum_PD.tsv, konkordancia/Vulgata_Clementina.tsv, konkordancia/SBLGNT_apparatus.tsv, konkordancia/TAGNT_valtozatok.tsv, konkordancia/BDB_rokon_irasok.tsv, konkordancia/VISSZHANG_README.md, adat/datasetek.tsv, adat/licencek.tsv, adat/SEMA.md, eszkozok/visszhang/, eszkozok/nyilt_mag_kapu.py, eszkozok/teszt_visszhang.py, naplok/F176_jelentes.md, nyilt_mag/]
fugg: [162, 170]
nem_fugg: [38, 48, 123, 146]
---

# F176_VISSZHANG_ADAT_BRIEF.md — A visszhang-réteg adatrétege

*FELADATOK #176 · Modell: sonnet · v1 · 2026.11.08*

*Befogadva a felhasználó jóváhagyásával („Mehet”, 2026-11-08). Előzmény: a nevesített tanítói réteg kivezetésének terve és a helyette javasolt „visszhang” (háttér + recepció) réteg; a forráskutatás négy + három + egy köre (2026-11-08) és a #86 megvalósítási terv 1.7b szakasza („Forrásjelöltek a repóba”, arány-kapu) és 6. szakaszának 13. pontja (jogi összegzés).*

## 1. Cél

A lexikonlap „visszhang” rétegéhez szükséges **adatok** bekerülnek a konkordancia-rétegbe, licencelten és provenienciával, és a nyílt mag kapuja megkapja a forrásonkénti arány-mérést. **A lexikonlap ebben a feladatban nem változik**: a generátor (`eszkozok/lexikon_general.py`) érintetlen, újragenerálás nincs. A lapra írás a HAMART-001 lapmintájának (Döntési út, olvasható döntések) elfogadása után, a lapszerkezeti átalakítással egy generátor-körben jön (külön feladat).

## 2. Mérce: „kimenetbe tehető”

A fejlesztői repó privát; a mérce az, hogy mi kerülhet a **kimenetbe** (a fizetős lexikonlap és a Zenodón közzétett nyílt mag).

- **NC (nem kereskedelmi) licenc: kizáró ok**, a privát repóban is (a lexikon kereskedelmi).
- **Közkincs, CC0, CC BY**: mehet (CC BY-nál forrásmegnevezés kötelező).
- **CC BY-SA, GPL**: csak belső jelölt-forrásként, vagy elkülönített rétegben; ebben a feladatban ilyet nem emelsz be.
- Minden licencállítást az **elsődleges helyen** (LICENSE-fájl, licencmező, nyers fájlfejléc) újraellenőrzöl, és a szó szerinti sort a `licencek.tsv`-be és a `VISSZHANG_README.md`-be írod. A kutatás egy része összefoglaló modellen át olvasott, ezért a korábbi állítás **nem** bizonyíték.
- Ha az elsődleges hely mást mond, mint az alábbi tábla: ⛔ **megállsz**, és jelzed (a beemelés tartalmi döntés).

## 3. Források (jelöltek; a 2. pont szerint ellenőrizendők)

| Tétel | Forrás | Várt licenc | Feltétel |
|---|---|---|---|
| Targum | Sefaria: Onkelos (toratemetfreeware verzió), Jonathan a Prófétákhoz (Mikraot Gedolot verzió) | közkincs (Sefaria `license` mező) | **verziónként**; `merged` fájl nem; a jemeni (Taj) verzió CC BY-SA → kimarad; a Metsudah NC → kimarad |
| Vulgata | eBible `latVUC` (Clementina) | közkincs | a kiadás (1592/1598/1880 stb.) azonosítva a README-ben |
| ÚSZ kritikai szöveg + apparátus | SBLGNT + apparátus (github.com/LogosBible/SBLGNT vagy az SBL saját oldala) | CC BY 4.0 | a korábbi EULA-szöveg archiválása a naplóban |
| ÚSZ változatjelölés | STEPBible TAGNT (meglévő `konkordancia/TAGNT_kivonat.tsv` forrása) | CC BY 4.0 | a szavankénti szövegforma-jelölés (TR / NA / SBLGNT / Byz / WH / THGNT) kivonata; a THGNT **szövege** nem jöhet át, csak a jelölés, hogy egy szó mely kiadásban áll |
| BDB rokon írások | Sefaria „BDB Dictionary” és „BDB Aramaic Dictionary” | közkincs (licencmező) | nincs tömeges exportban → szócikkenkénti API-lekérés, l. 4.3 |

Kizárt, nem keresed újra: ETCBC és SEDRA Peshitta (NC), Nova Vulgata, THGNT-szöveg, Sahidica, AlHaTorah, a Sefaria NC- és „unknown” verziói. Szabad Peshitta-szöveg nincs; a szír ág ebben a feladatban kimarad, ezt a README kimondja.

## 4. Tételek

### F176.0 — Modell-ellenőrzés és előkészítés
A CLAUDE.md szerinti modell-ellenőrzés (kért: `sonnet`). A `fugg` feladatok (#162, #170) állapota: ha a fejlécük még `fut`, de a munkájuk a `main`-ben van, jelezd, és folytasd; ha a munka nincs a `main`-ben, ⛔ állj meg.

### F176.1 — Licencellenőrzés
A 3. pont minden tételére: elsődleges hely, szó szerinti licencsor, dátum, URL → `naplok/F176_jelentes.md` 1. szakasz. Eltérésnél ⛔.

### F176.2 — Adatkészletek beemelése
- Letöltés **saját, üres könyvtárba a repón kívül** (scratchpad), a nyers fájlokat a repóba nem teszed; a konverziós szkript az `eszkozok/visszhang/` alatt, a letöltött könyvtáron kívül, `python -I`-vel olvasva.
- Kimenet: `konkordancia/Targum_PD.tsv`, `konkordancia/Vulgata_Clementina.tsv`, `konkordancia/SBLGNT_apparatus.tsv`, `konkordancia/TAGNT_valtozatok.tsv`. Kulcs: a repó igehely-formátuma (`1Móz 3:16`), a `Konyv_normalizalo_tabla.tsv`-vel normalizálva; a versszámozási eltérést (pl. Targum/MT ↔ Károli) **nem** javítod némán: a forrás saját versszáma külön oszlopban marad.
- TSV írás/olvasás `split('\t')` / `'\t'.join()` (CLAUDE.md), `csv` modul nem.
- Minden táblához SHA-256 és sorszám a `VISSZHANG_README.md`-ben; `adat/datasetek.tsv` és `adat/licencek.tsv` új sorai a `SEMA.md` szerint.

### F176.3 — BDB rokon írások gyorsítótára
- **Előbb** a Sefaria API felhasználási feltételeinek elolvasása (developers.sefaria.org vagy a Sefaria honlapjának Terms oldala): a releváns mondatok szó szerint és dátummal a jelentésbe. Ha tömeges vagy automatizált lekérést tilt: ⛔.
- Szkript (`eszkozok/visszhang/bdb_rokon.py`): bemenet egy Strong-lista (vagy egy motívum-ID → az `elofordulasok.tsv` láncszavai); a Sefaria BDB szócikkét a `strong_numbers` mező alapján illeszti; kimenet a `konkordancia/BDB_rokon_irasok.tsv` (oszlopok: `strong`, `sefaria_ref`, `nyelv`, `szoalak`, `kontextus` (a BDB-fej rövid szakasza, ≤ 120 karakter), `proveniencia`). Csak a nem héber és nem latin írású tokenek (arab, etióp, szír; Unicode-blokk szerint), nyelvtipp a blokkból.
- **Gyorsítótár:** a szkript először a táblában keres, és csak a hiányzó szócikket kéri le; lassú ráta (≥ 1 s a kérések között), azonosító User-Agent felhasználói e-mail nélkül.
- **Első futás: a HAMART-001 láncszavai** (H0779, H0127, H6093, H2403, H2555, H7843, H6975, H1863). Ellenpróba: a H7843-ra az arab, etióp és szír alak megvan; a H2555, H6093, H6975-re a BDB nem ad rokon szót (ez nem hiba, a tábla ezt nem sorként, hanem a jelentésben rögzíti).
- A meglévő `BDB_teljes_unabridged.tsv` **nem** változik.

### F176.4 — Arány-kapu
- `eszkozok/nyilt_mag_kapu.py`: forrásonként (a nyílt mag soraiban hivatkozott külső adatkészlet) kiírja: `<forrás>: <nyílt mag tételei> / <forrás tételszáma> = <arány>%`. **1% felett FIGYELMEZTETÉS** (átnézés a következő kiadás előtt), **5% felett HIBA** (a kapu megáll; további átvétel a felhasználó döntésével vagy ügyvédi vélemény után). A forrás tételszáma a `VISSZHANG_README.md`-ből / a `datasetek.tsv`-ből jön, nem kódba írva.
- A küszöbök indoka (a jelentésbe): óvatos mérnöki értékek, jogi alapjuk nincs (a #86 terv 6. szakasz 13. pont). A mai nyílt magra a kapu jelzés-szinten fut le (új visszhang-tétel még nincs benne).
- Teszt: `eszkozok/teszt_visszhang.py` (a kapu 0,5% / 2% / 6% mesterséges esetre a három szintet adja; a gyorsítótár második futása nem kér le újra).

### F176.5 — Jelentés és ellenőrzés
- `naplok/F176_jelentes.md`: licenc-sorok, sorszámok, hash-ek, a HAMART-futás eredménye (szavanként: van/nincs rokon írás), az API-feltételek idézete, a nyitott kérdések.
- `python eszkozok/ellenoriz.py`, a meglévő tesztek és a `nyilt_mag_kapu.py` zöld; `python eszkozok/feladatok.py ellenoriz` 0.
- Független ellenőr (`fuggetlen-ellenor`), draft PR. Merge a felhasználóé.

## 5. Kizárt ebből a feladatból
- a lexikonlapra írás és a `lexikon_general.py` bármilyen módosítása; újragenerálás;
- a tanúréteg (sermonindex Commentaries-index, Sefaria kapcsolattábla, NuBerea-adatkészletek) — következő fázis;
- Peshitta, kopt, akadémiai igehely-index;
- a `BDB_teljes_unabridged.tsv` javítása.

## 6. Megállási pontok (⛔)
1. A kért modell eltér (F176.0).
2. A `fugg` feladatok munkája nincs a `main`-ben.
3. Bármely licenc az elsődleges helyen eltér a 3. pont várt értékétől, vagy NC / BY-SA (F176.1).
4. A Sefaria API-feltételei tiltják az automatizált lekérést (F176.3).
5. A beemelés tartalmi döntést igényel (pl. versszámozás-feloldás, kiadásválasztás): tétel a `dontesek/uj/<ágnév>.md`-be helyőrzővel, majd megállás.
