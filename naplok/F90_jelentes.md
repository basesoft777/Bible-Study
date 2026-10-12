# F90_jelentes.md — a TAGNT-kivonat zárójeles sorainak pótlása: munkajelentés

*Brief: `F90_TAGNT_ZAROJELES_BRIEF.md`. Ág: `claude/f90-tagnt-zarojeles`. Állapot: az 1. lépés kész, a 2. lépés döntési táblája jóváhagyásra vár (DT-F90b).*

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

## 2. lépés — a 48 csoport Károli-kulcsa (javaslat, jóváhagyásra vár)

A tábla: `naplok/F90_karoli_dontesek.tsv` (oszlopok: nyers hivatkozás, jelölés, szószám, nyers sorszám-tartomány, NRSV-kulcs, alternatív kulcs, Károli-kulcs, választott, indok, állapot). Módszer: a csoport görög szavai és angol tükörfordítása összevetve a `Karoli_1908.tsv` két jelölt versével; a Károli-kulcs az a vers, amelynek szövegében a csoport tartalma áll (a README `KAROLI_DONTES` és a `Verzifikacios_elteres_tabla.tsv` mintájára). | proveniencia: scope=48 csoport Károli-kulcsa | forras=manual (értelmező szövegösszevetés: TAGNT nyers aca7d691414e + konkordancia/Karoli_1908.tsv) | ts=2026-10-12

Összesítés: **21 csoport NRSV-kulcsra, 27 az alternatív (KJV / egyéb) kulcsra** (157 szó-sor). Jelölés × választás: KJV→alt 24, KJV→NRSV 14, egyéb→NRSV 7, egyéb→alt 3.

A teljesen hiányzó 9 vers mind Károli-kulcsot kap, a kivonatban ma nem létező kulccsal: 2Kor 13:13, 3Ján 1:15, Fil 1:16, Fil 1:17, Jel 12:18, Ján 7:53, Róm 16:25–27. Az ott nem létező alternatív kulcsok (2Kor 13:14, 1Tim 6:22, Róm 14:24–26) nem jelennek meg.

**Beszúrási hely és sorrend.** A kivonat a nyers sorrendet követi, és ez egyben kulcs-sorrend. A 48 csoportból 47-nél a nyers hely a Károli-kulcs szerint is helyes: a vers végén álló, a következő versbe sorolt csoport és a vers elején álló, az előző versbe sorolt csoport egyaránt a két vers határán áll. **Kivétel a Fil 1:16–17:** a nyersben a `Php.1.16[1.17]` (= Károli Fil 1:17) áll elöl, a `Php.1.17[1.16]` (= Károli Fil 1:16) utána. Kulcs-sorrendben a Fil 1:16 sorai kerülnek előre; a versen belüli szórend változatlan.

### Nyitott kérdések a táblában (DT-F90b)

1. **1Thessz 2:11/12 (`1Th.2.12[2.11]`, 6 szó).** Az első öt szó (παρακαλοῦντες ὑμᾶς καὶ παραμυθούμενοι καὶ) a Károli 2:11-ben áll („úgy intettünk és buzdítgattunk”). A hatodik (μαρτυρόμενοι) megfelelője valószínűleg a Károli 2:12 eleje („És kérve kértünk”). Javaslat: a csoport egészben a 1Thessz 2:11-re kerül, mert a brief csoportonként dönt. Másik lehetőség: a #06 a 2:12-re kerül, szó szintű bontással.
2. **Zsid 12:22/23 (`Heb.12.22[12.23]`, 1 szó: πανηγύρει).** A „seregéhez” szót (Károli 12:23 eleje) a πανήγυρις megfelelőjének olvasom, mert a μυριάσιν ἀγγέλων = „az angyalok ezreihez” a 12:22 vége. Javaslat: Zsid 12:23. Ez közepes bizonyosságú döntés.
3. **A TR-utóiratok** (Róm 16:27 #14–#26, 2Kor 13:13 #22–#33, 1Tim 6:21 #13–#24). A Károliban nincs meg a szövegük. Javaslat: maradjanak a csoport kulcsán, a kivonat meglévő precedense szerint (a Gal 6:18 TR-utóirata a vers kulcsán áll).
4. **A Fil 1:16–17 sorrendje:** javaslat a kulcs-sorrend (l. fent). A másik lehetőség a nyers sorrend.

## 3–5. lépés

Nem indult el; a DT-F90b jóváhagyására vár.
