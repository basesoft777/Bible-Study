# F194 — az ISTENTISZT-001 új cikkének lépésenkénti mérése

*#194 ISTENTISZT_UJ_CIKK · a felhasználó: „a mérést ne felejtsük el” · cél: a többi lap arányosított becslése (lépés × egység)*

**Módszer (az orkesztrátor pontosítása, 2026-11-12).** A lépés költsége a session **saját tokenje** a saját átiratból (JSONL): az időablakba eső assistant-üzenetek `usage` mezőinek összege. Egy üzenet többször is szerepelhet az átiratban (streamelt, több tartalomblokkos üzenet), ezért üzenet-azonosítónként a mezők maximuma számít, az ablakhoz pedig az első előfordulás ideje köti. Külön áll az input, az output, a cache-olvasás és a cache-írás, a subagentek tokenje külön táblában. A számoló szkript a repón kívül van, a session scratchpadjében: `tokenek2.py`. Az átirat: `~/.claude/projects/E--Claude-Bible-Study-istentiszt-uj-cikk-992f57/1cb85370-….jsonl`, a subagenteké ugyanennek a `subagents/` könyvtárában. Az ablakok egész percre kerekítettek, és hézag nélkül csatlakoznak egymáshoz (UTC). A keret% csak tájékoztató, **párhuzamos terhelés mellett, nem a lépés költsége**. *Az első változat (`tokenek.py`) az ismétlődő üzenetet az első előfordulásával számolta, és ha egy üzenet átnyúlt az ablakhatáron, mindkét ablakban beszámította; a lenti számok már a 2. változattal készültek.*

**A lap mérete:**
- előfordulás: 20 (ÓSZ 16, ÚSZ 4) a 2. kiadás határán; korábban 22 volt;
- jelöltsor: 142, ebből `elofordulas` 135, `motivumkozi` 7;
- gerinc-Strong: H7121, H8034, G1941;
- visszhang: 36 modell-megfelelő, 20 LXX-sor, 2 tanú.

**Modell és effort.** A fő szál mindenütt claude-opus-5-5, effortja a session alapértéke (nem lekérdezhető). A subagentek külön táblában állnak (lent). A kontextus-tömörítés (11-12, 08:10 előtt) költsége az átiratban nem látszik. A 10. és a 11. lépés között a session állt.

## A fő szál

| # | Lépés | Ablak (UTC) | Output | Input (nem cache) | Cache-olvasás | Cache-írás | Üzenet | Futás / ellenőrzés | Egység | Keret (5 ó / heti), tájékoztató |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Kontextus: követelménylista, határnapló, adatállapot, brief | 11-11 12:23–12:25 | 5 935 | 32 | 2 310 506 | 129 829 | 16 | 8 / 0 | — | — / 93% → 10% / 93% |
| 1 | Határ (félbeszakadt): K6–K8, indoklás-mérés, munkalap; szünet | 11-11 12:25–12:32 | 32 662 | 74 | 8 431 819 | 107 406 | 35 | 9 / 2 | 3 határkérdés; 138 jelöltsor; 22 igehely | 10/93 → 15/94% |
| 2a | Folytatás: main behozása, a döntés olvasása, becslés | 11-12 06:48–06:50 | 3 619 | 10 | 1 294 656 | 268 247 | 5 | 3 / 0 | — | 11% / 22% |
| 2 | F194.1 határ: kritérium, 131 indoklás olvasói átírása, 2+2 sor ki, határnapló | 11-12 06:50–06:58 | 51 358 | 28 | 4 822 775 | 74 109 | 14 | 6 / 4 (besorolás, kapu, idézet, 39. szabály) | 131 jelöltsor; 4 döntés | — |
| 3 | F194.2 teljesség (3 háló) és LXX-híd, 4 új jelöltsor | 11-12 06:58–07:03 | 24 830 | 34 | 6 990 060 | 48 006 | 17 | 5 / 3 (blokkszűrés, besorolás, `ellenoriz.py`) | 3 háló; 67 LXX-vers; 17 új vers | 19% / 24% (07:03) |
| 4 | F194.3 a 15 lektori tétel besorolása | 11-12 07:03–07:04 | 3 810 | 10 | 2 242 781 | 20 453 | 5 | 1 / 0 | 15 lektori tétel | — |
| 5 | F194.4 Nave: jelöltképzés a 20 versen, 8 indok | 11-12 07:04–07:06 | 11 380 | 14 | 3 258 234 | 17 845 | 7 | 5 / 1 | 22 téma (8 kiválasztott) | — |
| 6 | Visszhang-felmérés (lánc, tanúindex, HCF-szöveg, Targum/Vulgata) | 11-12 07:06–07:09 | 15 637 | 34 | 8 040 380 | 47 424 | 16 | 11 / 0 | 20 igehely; 2 tanújelölt | — |
| 7 | F194.5 a `motivumok.tsv` visszaállítása (ütközés a #699-cel) | 11-12 07:09–07:10 | 6 044 | 16 | 3 706 399 | 10 254 | 7 | 3 / 0 | 1 sor | — |
| 8 | Mérés átállítása (szkript, ablakok) | 11-12 07:10–07:11 | 5 437 | 14 | 3 799 955 | 14 317 | 7 | 4 / 0 | — | — |
| 9 | Visszhang első kéz: 36 megfelelő, 2 tanú kinyerése; a második kéz indítása | 11-12 07:11–07:14 | 16 828 | 18 | 5 021 510 | 19 012 | 9 | 6 / 0 | 36 + 2 sor | — |
| 10 | Leállás (a felhasználó: „állj”), a subagent leállítása | 11-12 07:14–07:15 | 1 288 | 14 | 2 862 781 | 5 768 | 5 | 1 / 0 | — | — |
| 11 | Folytatás: beolvasók, gépi próba, a második kéz indítása | 11-12 08:10–08:23 | 6 778 | 14 | 770 185 | 69 076 | 7 | 6 / 1 (gépi összevetés szárazon) | — | — |
| 12 | F194.6 meghatározás (DT830), N-F194c/d (a második kéz futása alatt) | 11-12 08:23–08:24 | 5 598 | 16 | 1 060 696 | 11 555 | 8 | 7 / 1 | 1 döntés; 2 N-tétel | — |
| 13 | Javítókör: 2 elvetett sor javítása, újranézés kérése | 11-12 08:24–08:27 | 3 255 | 12 | 712 560 | 7 102 | 5 | 4 / 1 (kiejtés) | 2 sor | — |
| 14 | F194.7 beolvasás (megfelelők, tanúk, LXX), N182, napló | 11-12 08:27–08:28 | 7 612 | 20 | 1 359 912 | 12 626 | 9 | 7 / 1 (`ellenoriz` ×2) | 56 + 2 táblasor | — |
| 15 | Lezárás-előkészítés: mérés újraszámolása, helyi CI ×3, F194.8 (kódkönyv), F194.9 (generált nézetek) | 11-12 08:28–09:06 | 24 834 | 66 | 5 726 306 | 51 227 | 31 | 14 / 3 (helyi CI) | 2 kódkönyvsor; 4 generált nézet | — |
| 16 | A független ellenőr futása alatt (a fő szál vár) | 11-12 09:06–09:24 | 1 722 | 6 | 632 371 | 3 212 | 3 | 1 / 0 | — | — |
| 17 | F194.10–11: a jelentés mentése, javítókör (8 tétel), Glossa/SBLGNT, a mérés zárása | 11-12 09:24–09:31 | 27 403 | 54 | 6 230 794 | 50 004 | 26 | 15 / 3 (261 mérése, ujjlenyomat, Glossa) | 11 ellenőri tétel | — |
| 18 | F194.15: a main behozása (5 generált ütközés), a kritérium és a meghatározás a `motivumok.tsv`-ben, a fordítás újramérése; a 2. adag felmérése és első keze (LXX, Glossa) | 11-12 13:38–13:46 | 29 703 | 78 | 5 350 110 | 124 568 | 39 | 12 / 3 (sorösszevetés, export, fordítási lista) | 1 merge; 2 mező; 14 LXX-sor; 15 Glossa-hely | — |
| 19 | F194.16: a második kéz alatt N183/g, javítókör (3 megjegyzés), beolvasás, generált nézetek, napló | 11-12 13:46–13:53 | 15 453 | 42 | 3 748 731 | 28 127 | 19 | 8 / 2 (`ellenoriz`, Glossa-kulcsok) | 14 LXX-sor; 1 elvetett tanújelölt | — |
| 20 | F194.19–21: a main behozása, a teljesség-mérés a mai halmazzal, a lap az új szerkezetben (két szópár-kapu, teszt), a függési kör | 11-12 19:24–19:47 | 42 294 | 152 | 23 881 929 | 340 398 | 73 | — | 3 háló; 1 lap; 2 kapu | — |
| 21 | F194.22: a 9. szakasz ószövetségi táblázata szópárra (DT833), teszt | 11-12 19:47–19:55 | 21 434 | 50 | 10 058 786 | 38 612 | 24 | — | 1 generátor-ág; 16 vers | — |
| 22 | F194.23–25: a generátor HAMART-kapcsolói és olvasói leképezése, a BDB rokon nyelvi sorok (2. kéz), a próza nulláról és a 20 1/a-sor | 11-12 19:55–20:20 | 102 680 | 180 | 52 995 818 | 231 545 | 90 | — | 20 1/a-sor; 4 értelmező rés; 7 bdb-sor | — |
| 23 | F194.26–28: Jahve, pontozatlan rokon alak, a HAMART 3 sora, az 1. kiadás-sor, a kézi állítás-tételek javítása | 11-12 20:20–20:33 | 33 665 | 88 | 29 815 610 | 52 500 | 43 | — | 54 kézi tétel (9 HIBA) | — |
| 24 | F194.29–30: a szabály-tesztek, a lektor, a javítókör (22 tétel) | 11-12 20:33–20:50 | 39 990 | 78 | 26 927 274 | 70 814 | 36 | — | 22 lektori tétel | — |
| 25 | A független ellenőr futása alatt; F194.31 (a javítókör 1. része) | 11-12 20:50–21:28 | 17 952 | 40 | 14 681 268 | 34 416 | 18 | — | 10 ellenőri tétel | — |
| 26 | F194.32: az ellenőr maradék hat eltérése, a brief, a mérés (a keret-szünet után) | 11-12 21:28– (a mérés zárásáig) | 23 981 | 80 | 33 003 161 | 39 660 | 39 | — | 6 ellenőri tétel | — |

**Összesen (fő szál, 0–19, 1. fázis):** output 301 186, input 606, cache-olvasás 78 373 521, cache-írás 1 120 167, 290 üzenet.

**Összesen (fő szál, 20–26, 2. fázis):** output 281 996, input 668, cache-olvasás 191 363 846, cache-írás 807 945, 323 üzenet. *A 2. fázis ablakait a commitok ideje határolja; a 26. lépés a mérés zárásáig tart, a végső main-behozás, a nyílt mag exportja, a helyi CI és a push nincs mérve. A 25. és a 26. lépés között a session a keret elfogyása miatt állt.*

## Subagentek

| # | Szerep | Modell | Ablak (UTC) | Output | Input (nem cache) | Cache-olvasás | Cache-írás | Üzenet | Egység |
|---|---|---|---|---|---|---|---|---|---|
| S1 | Második kéz, 1. indítás (a leállításkor megszakítva, kimenet nélkül) | claude-sonnet-5-5 | 11-12 07:13–07:14 | 5 036 | 10 | 309 669 | 88 065 | 5 | — |
| S2 | Második kéz: 36 megfelelő, 2 tanú átnézése | claude-sonnet-5-5 | 11-12 08:23–08:26 | 24 638 | 24 | 1 002 481 | 111 646 | 12 | 38 sor (2 elvetve) |
| S3 | Második kéz, javítókör: 2 sor újranézése | claude-sonnet-5-5 | 11-12 08:27 | 3 262 | 12 | 570 032 | 6 407 | 5 | 2 sor |
| S4 | Független ellenőr (`fuggetlen-ellenor`), teljes szint, 99da7c34..20cc4c15 | claude-opus-5-5 | 11-12 09:06–09:24 | 58 265 | 162 | 10 213 080 | 202 572 | 81 | 13 commit; 11 eltérés |
| S5 | Második kéz, 2. adag: 14 LXX-sor, 1 Glossa-tanújelölt, a Glossa-nyom | claude-sonnet-5-5 | 11-12 13:46–13:50 | 26 936 | 38 | 1 724 171 | 121 424 | 19 | 15 sor (3 + 1 elvetve) |
| S6 | Második kéz, 2. adag javítóköre: 3 LXX-sor | claude-sonnet-5-5 | 11-12 13:51 | 2 437 | 8 | 371 133 | 6 118 | 3 | 3 sor |
| S7 | BDB rokon nyelv, első kéz (H7121), javítókörrel | claude-sonnet-5-5 | 11-12 20:07–20:09 | 5 334 | 24 | 717 561 | 85 666 | 10 | 7 sor |
| S8 | Állítás-ellenőrzés, kézi tételek (K1–K54) | claude-sonnet-5-5 | 11-12 20:20–20:29 | 45 234 | 66 | 5 394 273 | 228 429 | 33 | 54 tétel |
| S9 | Lektor (`lektor`), a teljes értelmező próza | claude-fable-5-2 | 11-12 20:38–20:43 | 29 939 | 18 | 768 848 | 174 583 | 9 | 22 tétel |
| S10 | Független ellenőr (`fuggetlen-ellenor`), efefb910..2ae45dae | claude-opus-5-5 | 11-12 20:49–21:19 | 108 397 | 494 | 56 152 136 | 322 450 | 247 | 12 commit; 10 eltérés |

**Összesen (subagentek, S1–S6, 1. fázis):** output 120 574, input 254, cache-olvasás 14 190 566, cache-írás 536 232, 125 üzenet. **S7–S10 (2. fázis):** output 188 904, input 602, cache-olvasás 63 032 818, cache-írás 811 128, 299 üzenet.

**Megjegyzés a 2. lépéshez:** a jelöltindoklások olvasói átírása (131 sor, ebből 94 sértette a kapu-szabályokat) **többletmunka, amely a HAMART-nál ebben a fázisban nem volt**: a HAMART indoklásait a #182 javító menete hozta olvasói alakra (F182.33, F182.53). Arányosításnál ezt az egységet külön kell számolni.

**A mérés korlátja (a felhasználóval, 2026-11-11):** az ISTENTISZT 2. kiadás, a határa nagyrészt ismert. A lektori tételek száma ezért nem általánosítható új motívumra; az 1. és a 2. kiadás összevetésére viszont jó. Az összevetéshez a lektor hatókörének egyeznie kell a HAMART-éval (a teljes értelmező próza, 2 kör). Az 1. kiadás lektora csak a jelölt helyeket olvasta, ezért a régi 15 tétel és a HAMART 46 tétele nem vethető össze közvetlenül.
