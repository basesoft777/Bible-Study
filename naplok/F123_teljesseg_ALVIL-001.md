# F123 U1 — az ALVIL-001 teljesség-mérése három hálóval (DT548)

*#123 MIGRACIO2 v2 · U1 (`munka: adat`) · ág: `claude/alvil-uj-cikk-b72389` · modell: claude-opus-5-5 · 2026-11-02*

*Döntés nélküli mérés. Eszköz: `eszkozok/teljesseg_meres.py` (teszt: `eszkozok/teszt_teljesseg_meres.py`), az első motívumnál készült, motívumfüggetlen. Soronkénti kimenet: `naplok/F123_teljesseg_ALVIL-001.tsv` (537 sor, minden sor mellett a háló proveniencia-sora). A Károli-háló eltéréseinek gépi lexéma-osztályozása: `naplok/F123_teljesseg_ALVIL-001_karoli_osztaly.tsv` (`naplok/F123_ALVIL2_karoli_osztaly.py`). Az LXX-híd a teljes ÓSZ-re: `naplok/F123_ALVIL2_lxx_hid.tsv` (`naplok/F123_ALVIL2_lxx_hid.py`). A hét lépés determinisztikus részének mai futása: `naplok/F123_ALVIL2_u1_kimenet.txt` (`naplok/F123_ALVIL2_u1_futtat.sh`, naplózva az `adat/auditok.tsv`-be, B4).*

## 0. A mért állapot

- Strongok (az `elofordulasok.tsv` `strong` mezője): **H7585** (שְׁאוֹל, seól), **G0086** (ᾍδης, hádész).
- Előfordulás-versek: 73 (72 sor; a Jel 20:13-14 két vers). Jelölt-versek (`elofordulas`): 78.
- A Károli-háló szótári alakjai (`--karoli-szavak`): **sír, koporsó, pokol, Seol, alvilág, mélység**. Kiválasztás: a 72 `karoli_szo` mező szavainak szótári alakja közül azok, amelyek a seól/hádész fordításai; a környezet szavai (kötél, kéz, torok, fenék, üreg, út, visz, kapu, közép, hatalom, szorongattatás, mély) és a névelők kimaradnak. A „holtak országa” (Jób 14:13) kétszavas fordítás, ezért a háló nem fogja meg (l. 4.). A jelölt alakok soronkénti darabszáma az eszköz konzolkimenetében: `a 65, sír 27, Seol 18, pokol 15, koporsóba 5, …`.

## 1. Összegzés

| Háló | Találat (vers) | E | J | ELTÉRÉS | ebből a versben áll a motívum szava |
|---|---|---|---|---|---|
| 1. Strong (TAHOT + TAGNT) | 74 | 73 | 1 (Mt 16:18, `elutasítva`) | **0** | — |
| 2. Károli-szó | 372 | 72 | 2 (Mt 16:18, 1Kor 15:55) | **298** | 0 |
| 3. Szótár (BDB H7585, Thayer G0086) | 91 | 71 | 2 (Mt 16:18, 1Kor 15:55) | **18** | 0 |
| fordított irány: E-vers, amelyet egyik háló sem ad | | | | **0** | |

**Eredmény.** A Strong-háló szerint a lista teljes: a motívum két szavának minden előfordulása (64 ÓSZ-vers, 10 ÚSZ-vers) az adatban van, egyetlen kivétellel, az Mt 16:18-cal, amely meglévő döntéssel kizárt jelölt (a 2026-11-02-i határdöntés óta bekerül, l. `naplok/F123_ALVIL2_naplo.md`). A másik két háló eltérése mind olyan vers, amelyben a motívum szava (a Károli alapszövegében) nem áll: a 2. és a 3. háló új helyet nem hozott, amely a lexikai negatív kritériumon („a versben a שְׁאוֹל vagy a ᾍδης áll”) átmenne. Ez mért tény; a jelöltek minősítése az U2 döntése.

Proveniencia:
- `scope=TAHOT-teljes+TAGNT-teljes | forras=TAHOT_kivonat.tsv+TAGNT_kivonat.tsv | strong=G0086+H7585 | n=74 | ts=2026-11-02T19:45Z`
- `scope=Karoli_1908-teljes | forras=Karoli_1908.tsv+adat/szoto/karoli_szotari_alak.tsv | szotari_alak=Seol+alvilág+koporsó+mélység+pokol+sír | n=372 | ts=2026-11-02T19:45Z`
- `scope=G0086+H7585 | forras=adat/bdb_vers_jelentes.tsv+adat/thayer_vers_jelentes.tsv (karoli_vers) | n=91 | ts=2026-11-02T19:45Z`

## 2. A Károli-háló 298 eltérése, lexémánként (gépi osztályozás)

A Károli ugyanazzal a magyar szóval több héber és görög szót fordít; a szótövező a „sír” főnevet és a „sír” igét sem választja szét. Az eltérő versekben a Károli-szó a következő szavak fordítása (a vers tokenjeinek angol glosszája szerint; egy vers több osztályba is eshet):

| Osztály | Vers | Leggyakoribb szó (vers) |
|---|---|---|
| „sír” ige (sírni) | 128 (+11 vegyes) | H1058 בָּכָה 75, G2799 κλαίω 31, H5594 סָפַד 12, H1065 בְּכִי 10 |
| mélység/verem | 62 (+12 vegyes) | H8415 תְּהוֹם 24, H0953 בּוֹר 11, G0012 ἄβυσσος 9, H4688 מְצוֹלָה 7, H7845 שַׁחַת 7 |
| sír/koporsó főnév | 51 (+21 vegyes) | G3419 μνημεῖον 31, H6913 קֶבֶר 26, G5028 τάφος 7, H6900 קְבוּרָה 5 |
| halál | 2 (+22 vegyes) | H4191 מוּת 10, H4194 מָוֶת 5 |
| osztálytalan (kézzel olvasva) | 20 | mélység (ÓSZ: hegyek, tenger, Isten mélysége), „sír” ige, Mt 28:2 sír, Luk 7:14 koporsó |

A közeli szavak, amelyeket a Károli „pokol” szóval ad vissza, de a versben nem a seól áll: **Jób 28:22** (H0011 אֲבַדּוֹן, abaddón: „A pokol és halál”), **Jób 31:12** (abaddón: „pokolig emésztene”), **2Pét 2:4** (G5020 ταρταρόω, tartaroó: „mélységbe taszítván”). Ezek jelöltsorként kerülnek a `jeloltek.tsv`-be (U2); a többi 295 vers más lexéma (sír-főnév, verem, tehóm/abüsszosz, sírás), lexémánként összesítve itt áll, egyenként nem jelölt (javaslat az U2-ben).

Proveniencia: `scope=naplok/F123_teljesseg_ALVIL-001.tsv karoli ELTÉRÉS × TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (glossza) | forras=naplok/F123_ALVIL2_karoli_osztaly.py, split('\t') | ts=2026-11-02`

## 3. A szótár-háló 18 eltérése

A BDB a H7585 szócikkében a seól-helyek mellett összevető helyeket is idéz (a sötétség földje, a halottak nyugalma, a remény a halálon túl); a Thayer a ᾅδης szócikkében a Septuaginta helyeit és egy szövegváltozatot. Egyik versben sem áll a seól vagy a hádész a Károli alapszövegében:

| Vers | Forrás | Mi áll a versben |
|---|---|---|
| Jób 3:17 | BDB sorszam 60 (-/1) | „Ott a gonoszok megszűnnek …” — a halottak helyének leírása, szó nélkül |
| Jób 10:21 | BDB 58, 89; Thayer 2 | „a sötétségnek és a halál árnyékának földébe” |
| Jób 14:21 | BDB 64 | a halott nem tud fiai sorsáról |
| Jób 16:22 | BDB 59 | „vár rám a sír” (a Károli „sír”-ja itt nem a seól) |
| Jób 19:25 | BDB 90 | „az én megváltóm él” |
| Jób 21:23 | BDB 61 | „Ez meghal …” |
| Jób 26:5 | BDB 35 | „A halottak is megremegnek” (רְפָאִים, refáím) |
| Jób 38:17 | Thayer 11 | „a halálnak kapui” (LXX: πυλωροὶ ᾅδου) |
| Jón 2:7 | BDB 37 | „bezáródtak a föld závárjai” |
| Préd 9:7 | BDB 62 | a BDB a Préd 9:5-öt idézi („a halottak semmit nem tudnak”), amely a Károli-számozásban a 9:7 (versszintű átkulcsolás) |
| Zsolt 16:11; 17:15; 73:23; 73:25 | BDB 81, 82, 84, 85 | a remény a halálon túl |
| Zsolt 88:5 | BDB 71 | „a sírba szállókhoz” (בוֹר) |
| Ézs 26:19 | BDB 96 | „visszaadja a föld az árnyakat” |
| Ézs 57:1 | BDB 86 | „az igaz elvész” |
| ApCsel 2:24 | Thayer 14 | „a halál fájdalmait” (a Thayer a „hádész fájdalmai” szövegváltozatot említi) |

Proveniencia: l. 1. (szótár-háló sora).

## 4. A fordított irány és a hálók vakfoltja

- **E-vers, amelyet egyik háló sem ad: 0.** A Károli-háló egy E-verset nem fog meg: **Jób 14:13** („a holtak országában”, kétszavas fordítás); a Strong- és a szótár-háló megfogja.
- **LXX-többlet** (a 6. lépés a teljes ÓSZ-re, `naplok/F123_ALVIL2_lxx_hid.tsv`): a kanonikus LXX 8 versben hoz ᾅδης-t ott, ahol a héber szövegben nincs seól: Jób 33:22, Jób 38:17, Péld 2:18, Péld 14:12, Péld 16:25, Zsolt 94:17, Zsolt 115:17, Ézs 14:19. A seól 64 versének LXX-megfelelője: 57 ᾅδης, 5 más szó (2Sám 22:6, Ez 32:21, Jób 24:19, Péld 23:14, Ézs 7:11), 2 versnek nincs LXX-megfelelője (Jób 17:12, 17:15). Proveniencia: `scope=TAHOT-teljes H7585 × LXX_OS kanonikus könyvek (38 fájl, elsodleges_slug) | forras=TAHOT_kivonat.tsv+LXX_OS/*.tsv (igehely_karoli, lemma) | ts=2026-11-02T19:46Z`.
- **Szövegváltozat:** az 1Kor 15:55 a Károli alapszövegében (TR) ᾅδη, a TAGNT kritikai szövegében θάνατε; a Strong-háló ezért nem adja, a Károli- és a szótár-háló igen.

## 5. A hét lépés mai futása (1., 3–6.)

| Lépés | Eredmény | Proveniencia |
|---|---|---|
| 1. gerinc-metszet | Zsolt 16:10 × ApCsel 2:27: 0; Hós 13:14 × 1Kor 15:55: 0 (héber és görög Strong nem metszhető; a híd az LXX, 6.) | `scope=range:Zsolt 16:10+ApCsel 2:27 … n=0 | ts=2026-11-02T19:46Z`; `scope=range:Hós 13:14+1Kor 15:55 … n=0 | ts=2026-11-02T19:46Z` |
| 3. scan | H7585: 64 vers, 66 szó; G0086: 10 vers | `strong=H7585 | n=64 | ts=2026-11-02T19:46Z`; `strong=G0086 | n=10 | ts=2026-11-02T19:47Z` |
| 4. kollokáció | H7585+H4194 (halál) 15 vers; +H0011 (abaddón) 2; +H3381 (leszáll) 26; +H0953 (verem) 5; G0086+G2288 (halál) 4 (Jel 1:18, 6:8, 20:13, 20:14) | `naplok/F123_ALVIL2_u1_kimenet.txt`, ts=2026-11-02T19:47Z |
| 5. igealak | H7585: 66 alak; G0086: 10 alak | ts=2026-11-02T19:47Z |
| 6. LXX-híd | Zsolt 16:10 (Psalms 15:10) és Hós 13:14: ᾅδης; teljes ÓSZ: l. 4. | ts=2026-11-02T19:47Z |

A korábbi X.A-hoz (`naplok/F123_adat_ALVIL-001.md`, 2026-10-29) képest: **eltérés nincs** (64/10 vers, gerinc-elemet érintő változás nincs).

## 6. Az eltérések elbírálása (U2, DT-F123o, 2026-11-02)

A 28 egyenkénti jelölt (a 3. szakasz 18 helye, a 2. szakasz 3 közeli szava, a 4. szakasz 7 LXX-többlete; a Jób 38:17 kettős) `elutasítva`. A Károli-háló további 295 eltérése lexémánként egy blokk-sorként áll a `jeloltek.tsv`-ben: tehóm/abüsszosz 33, verem (bór, sahat) 18, temetkezési sír (kever, mnémeion) 68, sírás 130, egyéb (más mélység, siratóének, a sír/koporsó más szóért) 46 vers. A besorolás gépi, a vers Strongjai szerint, elsőbbségi sorrendben; versenkénti lista: `naplok/F123_teljesseg_ALVIL-001_blokkok.tsv`.
