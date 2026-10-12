# F90_jelentes.md — a TAGNT-kivonat zárójeles sorainak pótlása: munkajelentés

*Brief: `F90_TAGNT_ZAROJELES_BRIEF.md`. Ág: `claude/f90-tagnt-zarojeles`. Állapot: az 1–5. lépés kész; a pótlás eredménye a felhasználó és a független ellenőr átnézésére vár (K5).*

## 1. lépés — a nyers fájl rögzítése és az eltérés mérése

**Engedély:** DT-F90a, 1. változat (felhasználó, 2026.10.12, az orkesztrátoron át): blob nélküli klón a session scratchpadjében, a repón kívül; csak letöltés és eltérés-mérés.

**Letöltés:** `git clone --filter=blob:none --no-checkout https://github.com/STEPBible/STEPBible-Data` (2026.10.12), majd `git cat-file -p <commit>:<út>` a két TAGNT-fájlra két commitnál. A nyers fájlok a repóba nem kerülnek (DT-F33a/f).

**A 2026.08.24-i commit kijelölése.** Az F22.9 rögzített adata (`naplok/F22_TAGNT_zarojeles_sorok.md`) csak a mai klónt (`aca7d691414e`) nevezi meg; az `adat/licencek.tsv` TAGNT-sora szerint a 08.24-i letöltés commitja „nincs rögzítve”. A kijelölés ezért dátum szerinti: `git rev-list -1 --before="2026-08-24T23:59:59Z" HEAD` = `efe428a0047bf7b9c3ce2624f60c252c6e435945` (2026-08-21T21:12:51+01:00). | proveniencia: scope=a 08.24-i commit kijelölése | forras=manual (dátum szerinti következtetés, a letöltés commitja nincs rögzítve) | ts=2026-10-12

A kijelölés pontatlansága itt nem számít: a két TAGNT-fájl utolsó módosítása a forrásrepóban `5af032662c1d` (2024-12-19); a `git log -- <a két fájl>` szerint azóta egyik sem változott, tehát 2024.12.19 és 2026.10.10 között minden commit ugyanazt a blobot hordozza.

| commit | út (`Translators Amalgamated OT+NT/…`) | blob | méret (bájt) | sha256 |
|---|---|---|---|---|
| `efe428a0047bf7b9c3ce2624f60c252c6e435945` | `TAGNT Mat-Jhn - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt` | `705c1bc1cf752e013efcef99b8d9a3b7853bf843` | 14 189 032 | `ab8eaaeb68e17a1dcfa34e1e9350358f22f03bc2a97244d848750ad81044bc8e` |
| `efe428a0047bf7b9c3ce2624f60c252c6e435945` | `TAGNT Act-Rev - Translators Amalgamated Greek NT - STEPBible.org CC-BY.txt` | `4bbea2c14681b01eb889d5a2d1dc0856858a32de` | 15 939 932 | `524e32375361e6d3fa2f7ef00b87605fdc4317a762f395651a05fdc31ad031b7` |
| `aca7d691414e00b0d669157d98bfd68195e64e1e` (HEAD, 2026-10-10) | `TAGNT Mat-Jhn - …` | `705c1bc1cf752e013efcef99b8d9a3b7853bf843` | 14 189 032 | `ab8eaaeb68e17a1dcfa34e1e9350358f22f03bc2a97244d848750ad81044bc8e` |
| `aca7d691414e00b0d669157d98bfd68195e64e1e` (HEAD, 2026-10-10) | `TAGNT Act-Rev - …` | `4bbea2c14681b01eb889d5a2d1dc0856858a32de` | 15 939 932 | `524e32375361e6d3fa2f7ef00b87605fdc4317a762f395651a05fdc31ad031b7` |

(A licenc-ellenőrzés commitja, `b99716b0cddb…`, ugyanezt a két blobot hordozza.) | proveniencia: scope=STEPBible-Data, TAGNT Mat-Jhn + Act-Rev, két commit | forras=github.com/STEPBible/STEPBible-Data (git ls-tree, git cat-file, sha256sum) | ts=2026-10-12

**Eltérés a két nyers változat között: 0** (azonos blob, azonos sha256). A 48 csoporton kívül tehát nincs eltérés; a brief 1. lépésének ⛔-ja nem lép életbe.

**Kiegészítő mérés: a nyers fájl és a meglévő kivonat.** A nyers fájl nem `[..]`/`{..}` jelölésű szó-sorait (141 720 jelöletlen + 26 NA `(..)`) a README mezőképzésével (Greek → alak + kiejtés; `sStrong+Instance` → Strong, `_instance` le, vesszős lista `+`-szal; `Dictionary form = Gloss` → szótő + jelentés, ` + `-os krázis-alak `+`-szal; English → angol, szélei levágva; editions változatlanul), a `Konyv_normalizalo_tabla.tsv` könyvcseréjével és a README 4 `KAROLI_DONTES` esetével vetítve: **141 746 sor, a meglévő `TAGNT_kivonat.tsv` 141 746 sorával sorról sorra, pozíció szerint 0 eltérés.** A kivonat tehát a nyers fájl nyers sorrendű, teljes vetülete, a 350 `[..]`/`{..}` sort kivéve. A generátor nincs a repóban, de a mezőképzése ezzel reprodukálva van; a pótló szkript ugyanezt használja. | proveniencia: scope=TAGNT nyers (aca7d691414e) nem [..]/{..} sorai ↔ konkordancia/TAGNT_kivonat.tsv, soronként | forras=STEPBible-Data/aca7d691414e + konkordancia/TAGNT_kivonat.tsv + konkordancia/Konyv_normalizalo_tabla.tsv | ts=2026-10-12

A nyers szó-sorok jelölés szerint: jelöletlen 141 720, `(..)` (NA) 26, `[..]` (KJV) 235, `{..}` (egyéb) 115. A `[..]` + `{..}` = **350 sor, 48 csoport**: egyezik a F22.9 leletével. Mind a 48 csoport a nyersben folytonos sorblokk.

## 2. lépés — a 48 csoport Károli-kulcsa (jóváhagyva: DT-F90b)

A tábla: `naplok/F90_karoli_dontesek.tsv` (oszlopok: nyers hivatkozás, jelölés, szószám, nyers sorszám-tartomány, NRSV-kulcs, alternatív kulcs, Károli-kulcs, választott, indok, állapot). Módszer: a csoport görög szavai és angol tükörfordítása összevetve a `Karoli_1908.tsv` két jelölt versével; a Károli-kulcs az a vers, amelynek szövegében a csoport tartalma áll (a README `KAROLI_DONTES` és a `Verzifikacios_elteres_tabla.tsv` mintájára). | proveniencia: scope=48 csoport Károli-kulcsa | forras=manual (értelmező szövegösszevetés: TAGNT nyers aca7d691414e + konkordancia/Karoli_1908.tsv) | ts=2026-10-12

Összesítés a javaslatban (a DT-F90b módosítása előtt): **21 csoport NRSV-kulcsra, 27 az alternatív (KJV / egyéb) kulcsra** (157 szó-sor). Jelölés × választás: KJV→alt 24, KJV→NRSV 14, egyéb→NRSV 7, egyéb→alt 3.

A teljesen hiányzó 9 vers mind Károli-kulcsot kap, a kivonatban ma nem létező kulccsal: 2Kor 13:13, 3Ján 1:15, Fil 1:16, Fil 1:17, Jel 12:18, Ján 7:53, Róm 16:25–27. Az ott nem létező alternatív kulcsok (2Kor 13:14, 1Tim 6:22, Róm 14:24–26) nem jelennek meg.

**Beszúrási hely és sorrend.** A kivonat a nyers sorrendet követi, és ez egyben kulcs-sorrend. A 48 csoportból 47-nél a nyers hely a Károli-kulcs szerint is helyes: a vers végén álló, a következő versbe sorolt csoport és a vers elején álló, az előző versbe sorolt csoport egyaránt a két vers határán áll. **Kivétel a Fil 1:16–17:** a nyersben a `Php.1.16[1.17]` (= Károli Fil 1:17) áll elöl, a `Php.1.17[1.16]` (= Károli Fil 1:16) utána. Kulcs-sorrendben a Fil 1:16 sorai kerülnek előre; a versen belüli szórend változatlan.

### A javaslat nyitott kérdései (DT-F90b)

1. **1Thessz 2:11/12 (`1Th.2.12[2.11]`, 6 szó).** Az első öt szó (παρακαλοῦντες ὑμᾶς καὶ παραμυθούμενοι καὶ) a Károli 2:11-ben áll („úgy intettünk és buzdítgattunk”). A hatodik (μαρτυρόμενοι) megfelelője valószínűleg a Károli 2:12 eleje („És kérve kértünk”). Javaslat: a csoport egészben a 1Thessz 2:11-re kerül, mert a brief csoportonként dönt. Másik lehetőség: a #06 a 2:12-re kerül, szó szintű bontással.
2. **Zsid 12:22/23 (`Heb.12.22[12.23]`, 1 szó: πανηγύρει).** A „seregéhez” szót (Károli 12:23 eleje) a πανήγυρις megfelelőjének olvasom, mert a μυριάσιν ἀγγέλων = „az angyalok ezreihez” a 12:22 vége. Javaslat: Zsid 12:23. Ez közepes bizonyosságú döntés.
3. **A TR-utóiratok** (Róm 16:27 #14–#26, 2Kor 13:13 #22–#33, 1Tim 6:21 #13–#24). A Károliban nincs meg a szövegük. Javaslat: maradjanak a csoport kulcsán, a kivonat meglévő precedense szerint (a Gal 6:18 TR-utóirata a vers kulcsán áll).
4. **A Fil 1:16–17 sorrendje:** javaslat a kulcs-sorrend (l. fent). A másik lehetőség a nyers sorrend.

### A DT-F90b döntése (felhasználó, 2026.10.12, az orkesztrátoron át)

A tábla jóváhagyva, egy módosítással. A tábla állapot oszlopa `jóváhagyva (DT-F90b, 2026.10.12)`.
1. **b)** A `1Th.2.12[2.11]` szétvágva: #01–#05 → 1Thessz 2:11, #06 (μαρτυρόμενοι) → 1Thessz 2:12. Ez az egyetlen szétvágott csoport; a táblában két sort kap, így a tábla 49 sor / 48 csoport. A végleges összesítés: 22 csoportrész NRSV-kulcsra, 27 alternatív kulcsra (156 sor).
2. a) Zsid 12:23.
3. a) A TR-utóirat-sorok a vers kulcsán maradnak (l. a soronkénti listát lent).
4. a) Kulcs-sorrend.

## 3. lépés — a pótlás (F90.4)

`python eszkozok/tagnt_zarojeles_potlas.py --nyers <…/Translators Amalgamated OT+NT> --ir`. A nyers fájlok a session scratchpadjében, a repón kívül voltak. A szkript a CRLF→LF normalizált sha256-ot az 1. lépés értékeivel veti össze, mert a `core.autocrlf=true` checkout CRLF-et írt a munkafába. | proveniencia: scope=konkordancia/TAGNT_kivonat.tsv, +350 sor | forras=eszkozok/tagnt_zarojeles_potlas.py + STEPBible-Data/aca7d691414e + naplok/F90_karoli_dontesek.tsv | ts=2026-10-12

- 141 746 → **142 096 sor** (+350). A `git diff` szerint 350 beszúrás és 0 törölt vagy módosított sor (**K2**). A szkript írás előtt és után is ellenőrzi, hogy a régi sorok bájtazonosak.
- **Újrafuttatás:** „A kivonat már a teljes vetülettel egyezik (142096 sor); nincs teendő.” A szkript ilyenkor nem ír (**K1**).
- **Érintett kulcsok:** 49, ebből 9 új: Ján 7:53, Róm 16:25–27, 2Kor 13:13, Fil 1:16, Fil 1:17, 3Ján 1:15, Jel 12:18.
- **Beszúrt sorok kulcsonként:** Mt 15:5 +11, Mt 17:15 +2, Mt 20:5 +3, Mk 3:20 +4, Luk 1:73 +3, Luk 6:17 +10, Luk 7:18 +9, Ján 7:53 +7, ApCsel 2:10 +4, ApCsel 3:19 +9, ApCsel 4:5 +2, ApCsel 5:40 +3, ApCsel 9:29 +8, ApCsel 24:18 +6, Róm 1:10 +5, Róm 7:10 +3, Róm 9:11 +7, Róm 16:25 +20, Róm 16:26 +20, Róm 16:27 +26, 2Kor 1:6 +7, 2Kor 8:13 +3, 2Kor 10:5 +2, 2Kor 13:12 +5, 2Kor 13:13 +33, Gal 2:20 +2, Ef 1:11 +2, Ef 2:15 +6, Ef 5:13 +6, Fil 1:16 +15, Fil 1:17 +11, Fil 2:8 +5, Kol 1:11 +2, Kol 1:21 +3, 1Thessz 1:3 +1, 1Thessz 2:6 +7, 1Thessz 2:11 +5, 1Thessz 2:12 +1, 2Thessz 1:8 +3, 1Tim 6:21 +17, Zsid 3:9 +2, Zsid 7:20 +8, Zsid 12:23 +1, 1Pét 3:15 +5, 1Ján 2:13 +7, 3Ján 1:15 +11, Jel 2:27 +7, Jel 12:18 +7, Jel 17:10 +4.
- **Sorrend:** a stabil kulcs-rendezés a meglévő sorok sorrendjét nem változtatta meg; a szkript ezt írás előtt ellenőrzi. A Fil 1:16 (`Php.1.17[1.16]`, 15 sor) a Fil 1:17 (`Php.1.16[1.17]`, 11 sor) előtt áll.

### A TR-utóirat sorai (DT-F90b 3. a): a vers kulcsán

Csak a TR kiadású sorok tartoznak ide. Az utóiratok előtti ἀμήν (2Kor 13:13 #21, 1Tim 6:21 #12) `TR+Byz` kiadású, ezért nem utóirat. Összesen 37 sor.

| Károli-kulcs | nyers sor | alak | Strong | angol | kiadás |
|---|---|---|---|---|---|
| Róm 16:27 | `Rom.16.27{14.26}` #14 | πρός | G4314 | to | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #15 | Ῥωμαίους | G4514 | Romans | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #16 | ἐγράφη | G1125 | it was written | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #17 | ἀπό | G0575 | from | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #18 | Κορίνθου | G2882 | Corinth | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #19 | διὰ | G1223 | through | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #20 | φοίβης | G5402 | Phoebe | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #21 | τῆς | G3588 | the | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #22 | διακόνου | G1249 | servant | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #23 | τῆς | G3588 | <the> | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #24 | ἕν | G1722 | in | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #25 | Κεγχρεαῖς | G2747 | Cenchrea | TR |
| Róm 16:27 | `Rom.16.27{14.26}` #26 | ἐκκλησίας.¶ | G1577 | church. | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #22 | πρός | G4314 | to | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #23 | Κορινθίους | G2881 | Corinthians | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #24 | δευτέρᾳ | G1208 | second | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #25 | ἐγράφη | G1125 | it was written | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #26 | ἀπό | G0575 | from | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #27 | Φιλίππων | G5375 | Philippi | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #28 | τῆς | G3588 | <the> | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #29 | Μακεδονίας | G3109 | of Macedonia | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #30 | διά | G1223 | through | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #31 | Τίτου | G5103 | of Titus | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #32 | καί | G2532 | and | TR |
| 2Kor 13:13 | `2Co.13.13[13.14]` #33 | Λουκᾶ.¶ | G3065 | Luke. | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #13 | πρός | G4314 | to | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #14 | Τιμόθεον | G5095 | Timothy | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #15 | πρώτη | G4413 | first | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #16 | ἐγράφη | G1125 | it was written | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #17 | ἀπό | G0575 | from | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #18 | Λαοδικείας | G2993 | Laodicea | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #19 | ἥτις | G3748 | which | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #20 | ἐστίν | G1510 | is | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #21 | μητρόπολις | G3390 | capital | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #22 | φρυγίας | G5435 | of Phrygia | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #23 | τῆς | G3588 | <the> | TR |
| 1Tim 6:21 | `1Ti.6.21{6.22}` #24 | Πακατιανῆς.¶ | G3818 | of Pacatiana. | TR |

## 4. lépés — igazolás (F90.5)

- **Kulcs-összevetés** (`eszkozok/karoli_strong/eredeti_nelkuli_lista.py` → `naplok/F22_nincs_parja_versek.tsv`, újragenerálva):
  - „Károli-vers eredeti nélkül”: **0**. A 9 ÚSZ-kulcs megszűnt.
  - „eredeti Károli nélkül”: 3 (Róm 3:31, Róm 8:39, 1Kor 3:23). Ezek a Károli-dataset versösszevonásai, a brief szerint nem az F90 tárgyai.
  - A régi fájl 2026.10.02-i volt, ÓSZ-sorai (Jób 40–41, 2Móz 35:36 stb.) az F84/F85 óta elavultak; ezeket az újragenerálás szintén eltüntette.
  - A részleges versek szószáma kiegészült: a teljes vetület soronként egyezik a kivonattal, tehát minden Károli-kulcs a nyers fájl összes, oda döntött szavát hordozza.
- **`tokenek.py`:**
  - `betolt_eredeti(versmegf=False)`: 31 161 vers, sorszám-hiba 0. A sorszám versenként 1..n folytonos.
  - `betolt_eredeti(versmegf=True)`: lefut, 31 161 vers.
  - `[nem TR]`, példák: Mt 15:5: 28 szó, 1 nem-TR; 1Thessz 2:12: 17 szó, 2 nem-TR (köztük a μαρτυρόμενοι, `NA28+…+Treg+Byz`); 1Tim 6:21: 24 szó, 1 nem-TR; Jel 12:18: 7 szó, 1 nem-TR.
  - A logika nem változott; a `«14.26` toldalékú kiadásmező TR-esnek számít, mert a `+` mentén vágott `TR` elem önálló.
- **`eszkozok/karoli_strong/sorrend_ellenoriz.py`:** új `SOR_GOROG` minta a `[..]`, `(..)` és `{..}` jelölésre, csak a TAGNT-ágon (**K4**). A TAHOT-ág a régi mintán maradt: az ÓSZ nem tárgya az F90-nek, és a TAHOT nyers fájlja nem lett letöltve.
  - A TAGNT-ág futott: 8000 nyers csoport, 142 096 morféma = a kivonat sorszáma, 7957 kivonat-vers.
  - #NN-hiba 0, nyers megfelelő nélküli vers 0, részsorozat-hiba 0.
  - A teljes szkript (TAHOT + TAGNT) nem futott, mert a TAHOT nyers fájlja nincs meg.

| proveniencia: scope=TAGNT_kivonat.tsv (142 096 sor) ↔ Karoli_1908.tsv kulcsok; tokenek.py; sorrend_ellenoriz.py TAGNT-ág | forras=eszkozok/karoli_strong/eredeti_nelkuli_lista.py, tokenek.betolt_eredeti, sorrend_ellenoriz.ellenoriz(gorog=True) + STEPBible-Data/aca7d691414e | ts=2026-10-12

## 5. lépés — README és NYITOTT (F90.6)

- `konkordancia/TAHOT_TAGNT_README.md`:
  - a zárójeles szakasz bővült: a háromféle jelölés, a 48 csoport, a pótló szkript, a Károli-döntés szabálya és a sorrend;
  - a sorszám-tábla és az igehelyszám frissítve: 142 096 sor, 7 957 igehely.
- `NYITOTT_FELADATOK.md`: az N-F22c és az N-F22d pontosítva. A kivonat-rész kész; az érintett versek újrapárosítása (a Fil 1:16–17 is) és a 2Kor futtatása az F22 dolga, nyitva.

## Ami hátravan

- **K5:** a független ellenőrzés (`fuggetlen-ellenor`) és a CI.
- A felhasználó a merge előtt átnézi a pótlás eredményét.
