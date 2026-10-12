# F22_TAGNT_zarojeles_sorok.md — a nyers TAGNT `[..]` / `{..}` jelölésű szó-sorai, amelyek a `TAGNT_kivonat.tsv`-ből kimaradtak

*Lekérdezés (2026.10.12): a STEPBible-Data repó (`git clone --depth 1 --filter=blob:none --sparse`, `STEPBible-Data/aca7d691414e`, 2026.10.10) `Translators Amalgamated OT+NT/TAGNT Mat-Jhn …` és `TAGNT Act-Rev …` fájljai, a hivatkozás-mező regexe `^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)([\[{](\d+)\.(\d+)[\]}])#(\d+)=`; összevetve a `konkordancia/TAGNT_kivonat.tsv` és a `konkordancia/Karoli_1908.tsv` kulcsaival. Szkript: a session scratchpadje (`zarojeles.py`), API nélkül. **Figyelem:** a kivonat a 2026.08.24-i letöltésből készült; a mostani nyers fájl ennél frissebb, a két változat eltérhet.* | proveniencia: scope=TAGNT nyers (Mat–Rev), [..]/{..} hivatkozás | forras=STEPBible-Data/aca7d691414e + konkordancia/TAGNT_kivonat.tsv + konkordancia/Karoli_1908.tsv | ts=2026-10-12

A nyers fájl fejléce: *„Reference: Versification as used by NRSV. Differences are marked in square brackets for KJV, bround brackets for NA and curley brackets for others.”* A kivonat-generátor regexe (`konkordancia/TAHOT_TAGNT_README.md`) csak a kerek zárójelet (NA) ismeri; a szögletes (KJV) és a kapcsos (egyéb) jelölésű sorok kimaradtak.

**Összesen 48 csoport (vers + jelölés), 350 szó-sor.** 9 csoportnál az NRSV-kulcs a kivonatban egyáltalán nincs meg (teljes vers hiányzik); 39-nél a kulcs megvan, de a vers szavainak egy része hiányzik (részleges vers). A „futott” oszlop: az F22 eddig párosított ÚSZ-könyveiben (22.8, 22.9 A, a B futó Gal/Ef/Zsid).

| nyers hivatkozás | szó | NRSV-kulcs a kivonatban? (sor) | NRSV-kulcs a Károliban? | alternatív kulcs a Károliban? | F22-ben futott |
|---|---|---|---|---|---|
| Mat.15.6{15.5} | 11 | igen (10) | igen | igen Mt 15:5 | — |
| Mat.17.15[17.14] | 2 | igen (21) | igen | igen Mt 17:14 | — |
| Mat.20.5[20.4] | 3 | igen (10) | igen | igen Mt 20:4 | — |
| Mrk.3.20[3.19] | 4 | igen (12) | igen | igen Mk 3:19 | — |
| Luk.1.73[1.74] | 3 | igen (8) | igen | igen Luk 1:74 | — |
| Luk.6.18[6.17] | 10 | igen (8) | igen | igen Luk 6:17 | — |
| Luk.7.18[7.19] | 9 | igen (9) | igen | igen Luk 7:19 | — |
| Jhn.7.53{8.1} | 7 | NEM (0) | igen | igen Ján 8:1 | — |
| Act.2.11[2.10] | 4 | igen (13) | igen | igen ApCsel 2:10 | — |
| Act.3.20[3.19] | 9 | igen (7) | igen | igen ApCsel 3:19 | — |
| Act.4.5[4.6] | 2 | igen (15) | igen | igen ApCsel 4:6 | — |
| Act.5.39[5.40] | 3 | igen (13) | igen | igen ApCsel 5:40 | — |
| Act.9.28[9.29] | 8 | igen (9) | igen | igen ApCsel 9:29 | — |
| Act.24.19[24.18] | 6 | igen (12) | igen | igen ApCsel 24:18 | — |
| Rom.1.10[1.9] | 5 | igen (14) | igen | igen Róm 1:9 | — |
| Rom.7.10[7.9] | 3 | igen (11) | igen | igen Róm 7:9 | — |
| Rom.9.12[9.11] | 7 | igen (8) | igen | igen Róm 9:11 | — |
| Rom.16.25{14.24} | 20 | NEM (0) | igen | nem Róm 14:24 | — |
| Rom.16.26{14.25} | 20 | NEM (0) | igen | nem Róm 14:25 | — |
| Rom.16.27{14.26} | 26 | NEM (0) | igen | nem Róm 14:26 | — |
| 2Co.1.7{1.6} | 7 | igen (11) | igen | igen 2Kor 1:6 | — |
| 2Co.8.13[8.14] | 3 | igen (8) | igen | igen 2Kor 8:14 | — |
| 2Co.10.4[10.5] | 2 | igen (15) | igen | igen 2Kor 10:5 | — |
| 2Co.13.12[13.13] | 5 | igen (5) | igen | igen 2Kor 13:13 | — |
| 2Co.13.13[13.14] | 33 | NEM (0) | igen | nem 2Kor 13:14 | — |
| Gal.2.19[2.20] | 2 | igen (9) | igen | igen Gal 2:20 | **igen** |
| Eph.1.10{1.11} | 2 | igen (22) | igen | igen Ef 1:11 | **igen** |
| Eph.2.14[2.15] | 6 | igen (17) | igen | igen Ef 2:15 | **igen** |
| Eph.5.14[5.13] | 6 | igen (15) | igen | igen Ef 5:13 | **igen** |
| Php.1.16[1.17] | 11 | NEM (0) | igen | igen Fil 1:17 | **igen** |
| Php.1.17[1.16] | 15 | NEM (0) | igen | igen Fil 1:16 | **igen** |
| Php.2.7[2.8] | 5 | igen (10) | igen | igen Fil 2:8 | **igen** |
| Col.1.11{1.12} | 2 | igen (15) | igen | igen Kol 1:12 | **igen** |
| Col.1.22[1.21] | 3 | igen (18) | igen | igen Kol 1:21 | **igen** |
| 1Th.1.2[1.3] | 1 | igen (14) | igen | igen 1Thessz 1:3 | **igen** |
| 1Th.2.7[2.6] | 7 | igen (13) | igen | igen 1Thessz 2:6 | **igen** |
| 1Th.2.12[2.11] | 6 | igen (16) | igen | igen 1Thessz 2:11 | **igen** |
| 2Th.1.8{1.7} | 3 | igen (17) | igen | igen 2Thessz 1:7 | **igen** |
| 1Ti.6.21{6.22} | 17 | igen (7) | igen | nem 1Tim 6:22 | **igen** |
| Heb.3.10[3.9] | 2 | igen (18) | igen | igen Zsid 3:9 | **igen** |
| Heb.7.20[7.21] | 8 | igen (6) | igen | igen Zsid 7:21 | **igen** |
| Heb.12.22[12.23] | 1 | igen (13) | igen | igen Zsid 12:23 | **igen** |
| 1Pe.3.16[3.15] | 5 | igen (19) | igen | igen 1Pét 3:15 | **igen** |
| 1Jn.2.14[2.13] | 7 | igen (26) | igen | igen 1Ján 2:13 | **igen** |
| 3Jn.1.15[1.14] | 11 | NEM (0) | igen | igen 3Ján 1:14 | **igen** |
| Rev.2.28[2.27] | 7 | igen (7) | igen | igen Jel 2:27 | — |
| Rev.12.18[13.1] | 7 | NEM (0) | igen | igen Jel 13:1 | — |
| Rev.17.9[17.10] | 4 | igen (18) | igen | igen Jel 17:10 | — |
