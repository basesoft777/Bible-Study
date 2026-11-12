ELTÉRÉS: 13 tétel

# ELLENŐR — F183 (VISSZHANG_USZ_TANU)

Brief: F183_VISSZHANG_USZ_TANU_BRIEF.md · tartomány: 7095bc63..27430a13 (merge-base origin/main..HEAD; saját commitok: 9ee3db17, fcf1bfd5, b1569fae, 49cf9c90, 7b3d621c, 27430a13; F183.5 merge) · egyeztetett hatókör: naplok/F183_jelentes.md · ellenőr: claude-opus-5-5 (kért: opus) · a lap és a nyilt_mag/ csak a 9. szakaszig olvasva (DT742)

*A jelentést a fő szál (claude-opus-5-5) írta ki az ellenőr válaszából szó szerint, mert az ellenőrnek nincs fájlíró eszköze. Az ellenőr megjegyzése: a `futtat.py` futás a közös ellenőrzési zárra várt (egy másik worktree tartotta), ezért a C1 sor NEM ELLENŐRIZHETŐ; a `chain_lineage.py`, `ellenoriz.py`, `teszt_hatastortenet.py` és `tanu_kinyer.py ellenoriz` futtatását a szerepe nem engedte.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | a session claude-opus-5-5, a kért modell opus. A commitok Co-Authored-By sora Opus 5.5. A `modell` mezők: claude-opus-5-5 kinyerő, claude-sonnet-5-5 ellenőr. Hogy a Sonnet ténylegesen futott-e: NEM ELLENŐRIZHETŐ |
| 1a Remez/Sod | OK | adat/visszhang_tanuk.tsv:3-12 | Grep `^HAMART-001\t…` az adat/elofordulasok.tsv-n. A tanúk helyei: 1Móz 4:10-11 Peshat/Remez (207), 5:29 Remez (210), 8:21 Remez (219), Róm 8:21 Drash/Sod (241), Gal 3:13-14 Remez (242), Zsid 6:7-8 Remez/Drash (243) |
| 1b hagyományonként egy | OK | adat/visszhang_tanuk.tsv | a 10 sorban minden (igehely, hagyomány) pár legfeljebb egyszer áll; kódban: `tanuk_lapra` (lexikon_general.py:8330), `tanu_kinyer.ellenoriz` |
| 1c `kapcsolat` nem idézet | OK | visszhang_tanuk.tsv:4-12 | a mondatok saját szavasak; a Jeromos-sor „fán függő átkozott” része bibliai idézet, nem az atyáé |
| 1d `kor` forrásból | ELTÉRÉS (7) | visszhang_tanuk.tsv:10,11 | Grep a hcf_id-kre a konkordancia/Tanu_atyak_index.tsv-ben: Chrysostom 407 (73425. sor), Jerome 420 (81872. sor) → a forrásév az 5. sz.; a „4–5. sz.” nem az évből jön. Efrém 373 → 4. sz. és Ambrus 397 → 4. sz.: OK. A CL-sorok kora a `chain_lineage.lekerdez` `century` mezőjéből (tanu_kinyer.py:178): OK |
| 1e proveniencia | OK | visszhang_tanuk.tsv:3-12 | mind a 10 sor `scope=…\|forras=…\|ts=…`, a HCF-soroknál hcf_id + sha256 |
| 1f Chain Lineage újrafuttatás | NEM ELLENŐRIZHETŐ | — | a `chain_lineage.py` nincs a megengedett parancsok között, és hálózatot kér |
| 1g idézet a táblában | ELTÉRÉS (8) | visszhang_tanuk.tsv:4 (`ellenorzes`) | a Glossa-sor `ellenorzes` mezője szó szerint idézi a latin jegyzetet („Notandum quod in peccato Adae … fratricidium addidit”). A tábla fejléce és a SEMA 2.57 szerint a táblában szöveg nincs. A szöveg közkincs, licenckár nincs, de a tábla saját szabályát sérti |
| 1h Aranyszájú-hely | NEM ELLENŐRIZHETŐ | visszhang_tanuk.tsv:11 | a HCF-index Róm 8:19–20-ra szól (Tanu_atyak_index.tsv:73425, `nt_feltetelezett`), a motívum helye Róm 8:21. A lap ezt kimondja („Tárgyalt hely: Róm 8:19-20”). A HCF-szöveg nincs a repóban |
| 2 Vulgata szó szerint | OK | adat/visszhang_megfelelok.tsv:35-40 | Grep a Vulgata_Clementina.tsv-n: Róm 8:21 „corruptionis”, Gal 3:13 „maledicto / maledictum / Maledictus”, Zsid 6:8 „maledicto”, Jel 11:18 „exterminandi / corruperunt”, Jel 19:2 „corrupit” — mind szó szerint áll |
| 2 Strong a versben | OK | uo. | `python eszkozok/lekerdez.py scan G5351 --szakasz "Jel 19:2"` → n=1; G1311 Jel 11:18 → n=1 (2 szó); G5356 Róm 8:21 → n=1; G2671 Zsid 6:8 → n=1; G1944 Gal 3:13 → n=1; G2671 Gal 3:13 → n=1 (2 szó). Proveniencia: `forras=TAGNT_kivonat.tsv … ts=2026-11-11T13:2xZ` |
| 2 szövegváltozat | OK | lap 3428 | TAGNT_valtozatok.tsv:11513 (G5351 ἔφθειρεν, Byz-ből hiányzik); SBLGNT_apparatus.tsv:6856 („ἔφθειρεν WH Treg NA28 ] διέφθειρεν RP”) |
| 3 Glossa fejléc, proveniencia | OK | konkordancia/Glossa_Ordinaria.tsv:1-6 | GENERÁLT-jelölés, forrás-URL, sha256, ts, licenc. A zip sha256-ja és a README táblájában álló fájl-sha256 NEM ELLENŐRIZHETŐ (hash-parancs nem megengedett) |
| 3 tétel- és sorszám | OK | VISSZHANG_README.md:24 | `git diff --numstat`: 12974 hozzáadott sor − 6 fejsor = 12968 = a README tétele = a fejléc „átvett sor” értéke |
| 3 licencek, datasetek | OK | adat/licencek.tsv (+1), adat/datasetek.tsv (+1) | közkincs, sha256, DT-F33d (a)(b) indoklás |
| 3 a Glossa-tanú igaz | OK | Glossa_Ordinaria.tsv:80 | „RAB. Notandum quod in peccato Adae terra maledicitur. Cain vero maledicitur, quia sciens damnationem primae praevaricationis, fratricidium addidit.” A tanú mondata ezt adja vissza; a lap 4:10-11 sorának (a föld átka a személyre száll) megfelel |
| 3 máshol nem mondja ki | OK (szúrópróba) | Glossa_Ordinaria.tsv:63,66,79,81,106,135,4127-4128,4653,4952,7474,11034-11036,11661,12228,12816 | Grep a Remez/Sod-helyekre (Vulgata-számozással: Zsolt 13, 52, 73). 6:13, 8:21, Zsolt 13:1-2, 52:1, 73:20, Jer 6:7, Róm 8:19-21, Gal 3:13, Zsid 6:7, Jel 11:18: a kapcsolatot egyik sem mondja ki. 5:29, 9:11, 9:15, 12:3, Zsid 6:8, Jel 19:2: nincs jegyzet. Megjegyzés: a Vulgata 52:2-hez nincs jegyzet, a „Dixit insipiens” jegyzet az 52:1-en áll (a jelentés „52:2”-t ír); a következtetést ez nem változtatja meg |
| 3 a 28 hely átnézése | NEM ELLENŐRIZHETŐ | lap 3452 | a helyenkénti átnézésről nincs napló vagy adatsor; csak a jelentés állítja (l. 3. tétel) |
| 4 generátor-függvények | OK, kivéve 1, 3 | lexikon_general.py:8222-8420 | `hatastortenet_athelyez` (`uj_szerkezet` őrrel), `blokk_hatas_usz`, `blokk_hatas_tanuk`, `tanuk_lapra`, `regi_szerkezetre` (6505-6510), `UJ_SZAKASZOK`/`UJ_CIMCSERE` (6426-6449) olvasva |
| 4 régi lapok | OK | lexikon_general.py:6419, 8810, 6503 | `UJ_LAPSZERKEZET={'HAMART-001'}`; a `szotari_pontok_jelmagyarazat` / `attekinto_beszur` / `blokk_dontesi_ut` hívói csak az új szerkezetben futnak (Grep). `git diff --stat … -- lexikon/` → csak a HAMART-001 változott |
| 4 „Mit mutat” számai | OK | lap 3424, 3428-3429 | Grep visszhang_megfelelok.tsv H7843: vulgata 6:11, 6:12 corrumpo; 6:13 disperdo; 6:17 interficio; 9:11 dissipo; LXX 9:15 üres → 2/5. H0779: maledico 4/4. ÚSZ: corru- 3/3, maled- 2/2; „2 családból 1” helyes |
| 4 „Mit mutat”: változat a családon belül | ELTÉRÉS (1) | lexikon_general.py:8281, 8307; lap 3428 | `_gorog_tovek('διέφθειρεν')` → {'εφθ'} (az ε-augmentum miatt), a család tövei {'φθε','αφθ','φθο'} → `valt_csaladon_belul=False`. A sablon 6 „9. szakasz” 2. szabálya által előírt mondat ezért nem áll a lapon, a K67b mégis „teljesül, a szócsaládon belül” jelölést kapott |
| 4 „nincs szabad forrás” | OK | lap 3431 | Grep: a kifejezés nem áll a lapon. A Peshitta-mondatot („szabad, digitális forrása nem áll rendelkezésre”) a brief V1 előírja; a VISSZHANG_README kizárt forrásai (ETCBC/SEDRA, NC) alátámasztják |
| 4 beégetett szöveg | ELTÉRÉS (3) | lexikon_general.py:8137, 8351 | a bevezető HAMART-specifikus tartalmat ír a közös generátorba („a bűn következménye az átok, a föld és a romlás láncán terjed”). A `GLOSSZA_MONDAT` feltétel nélkül állítja az átnézést, adat és proveniencia nélkül; más lapon hamis lesz (brief: Átvihetőség) |
| 4 bevezető vs. gépi sorok | ELTÉRÉS (2) | lap 3435, 3439, 3443, 3446, 3448 | a bevezető szerint minden tanú „ugyanazzal a kapcsolattal olvassa” a helyet. A 4 Chain Lineage-sor csak együtt-idézést mutat, a kapcsolatot senki nem ellenőrizte (tanu_kinyer.py:165-183). Sérül a brief V2, a sablon 6 3. szabálya és a K67d |
| 5 kapu | OK | olvasoi_kapu.py:1277-1281 | a VISSZHANG az „Ókori fordítások: Ószövetség” alszakaszt is méri. Futtatni nem tudtam: NEM ELLENŐRIZHETŐ |
| 5 teszt, rontott minta | OK (tanú-szabály) / ELTÉRÉS (5) | teszt_hatastortenet.py:89-116 | rontott minta van: ellenőrizetlen sor, Peshat-hely, két latin sor egy helyen, két ellenőrzött sor a táblában. Az ÚSZ-táblára nincs teszt, és a teszt nem fut a CI-ben (Grep `teszt_hatastortenet\|tanu_kinyer` a workflow-kban és az `ellenoriz.py`-ban: 0 találat). Futtatni nem tudtam |
| 6 SEMA 2.52/2.57/3.11 | OK, kivéve 11 | adat/SEMA.md:2091, 2245-2288, 3.11 VISSZHANG | a 2.57 teljes; a 2.52 címe még öt táblát sorol |
| 6 sablon 6, 9. szakasz | OK | 6_PaRDeS_lexikon_oldal_sablon.md (a diff +132-137) | az 1–4. szabály áll |
| 6 K65–K67f, A27 | ELTÉRÉS (1, 4, 5, 9, 10) | KESZ_LAP_KOVETELMENY.md:129-137, 239 | K67b „teljesül”, de hiányzik a mondat (1). K67f „nem része az 1. kiadásnak”, holott az N-F183a szerint a döntés nyitott, a K67/A27 pedig „kötelező az 1. kiadáshoz” (4). K67a ellenőrzés-oszlopa: „gépi: teszt_hatastortenet.py”, de az ÚSZ-táblát nem teszteli (5). K67d „7 helyen” (9). Hivatkozás „F183.2 (generátor)” F183.3 helyett (10). K67e arány-kapu: csak a Glossára él (README 7.), futtatni nem tudtam |
| 6 dontesek/uj, nyitott/uj | OK | dontesek/uj/visszhang-usz-tanu.md, nyitott/uj/visszhang-usz-tanu.md | helyőrzők DT-F183a–c és N-F183a–c; az ág nevéhez illő fájlnév |
| 6 végleges szám | OK | — | Grep a `+` sorokra (`\b(DT\|N)\d{2,3}\b`): csak a main számai (DT639–664, DT760, DT761, N155) |
| 6 A2: nyitott tételek | ELTÉRÉS (6) | NYITOTT_FELADATOK.md:841 | az N-F176a teljes egészében lezárva, de a Vulgata-kiadás kérdése (1592/1598/1880) eldöntetlen; a DT774 csak a Glossára szól. N-F176b/c: valóban nyitott |
| 7 csv | OK | eszkozok/visszhang/ | Grep `import csv\|csv\.`: 0 találat |
| 7 DT28 | OK | — | a generátor az adatból renderel; forrásba visszaírás nincs. A jeloltek.tsv két indoklásának szakaszhivatkozása adatrétegbeli javítás |
| 7 nincs közvetlen út | OK | lexikon_general.py:8323-8344 | a tanú csak a visszhang_tanuk.tsv ellenőrzött sorából jut a lapra |
| 7 új forrás leltára | ELTÉRÉS (12) | adat/datasetek.tsv, adat/licencek.tsv | Grep `Chain`: 0 találat. A Chain Lineage Browsernek (licence nincs megadva) nincs leltársora; a brief „Nem része” pontja előírja. A DT-F183c a döntés, a leltár nem |
| 8 ellenoriz.py, teszt | NEM ELLENŐRIZHETŐ | — | a szerepem Bash-köre nem engedi |
| C1 CI-jelentés | NEM ELLENŐRIZHETŐ | — | `python eszkozok/ellenorzes/futtat.py --valtozott <a 37 fájl> --diff-alap 7095bc63… --diff-fej HEAD`: a futás a közös zárra vár (`~/.pardes/ellenorzes.zar`: pid 12924, teszt_futtat.py --gyors, bdb-harmadik-tanu-618784, 14:25:28 óta); kimenet a jelentés lezárásáig nem volt. CI-jelentést nem kaptam |
| L1 törölt/kiszűrt sorok | OK | — | `git diff --numstat`: a törlések módosítások (jeloltek 2, nyilt_angol 2, KESZ 15, lexikon_general 11, lap 77, nyilt_mag 25). A Glossa-importban üres jegyzet miatt 0 sor maradt ki (fejléc: 12968/12968; glossza_import.py:72) |
| L2 kulcstartomány | OK (szúrópróba) | Glossa_Ordinaria.tsv | Grep `^(Mal\|Abd\|Fil\|2Ján\|3Ján\|Júd\|Filem) ` → 108 sor; 1Móz és Jel megvan. A „csomag lábjegyzetei” csak a 66 bejárt könyv lábjegyzeteit számolja (l. 11) |
| L3 nulla-diff hatóköre | OK | — | vonatkozik: a többi lexikonlap fájlja a diffben változatlan, a kódút őrzött. Nem vonatkozik: a regenerálás bájtazonosságát nem futtattam (E28: C1) |
| L4 sorszám-Δ (fejléc nélkül) | OK, kivéve 11 | — | adat/datasetek +1; jeloltek 0; licencek +1; nyilt_angol +8; visszhang_megfelelok +6; visszhang_tanuk +10 (új; bontás a jelentésben és a K67e-ben: 6 modell, 4 gépi); konkordancia/Glossa_Ordinaria +12968 (új; bontás: README 3b és fejléc, egy kategória). A többi .tsv: 0 |
| L5 tiltás-pontok | NEM ELLENŐRIZHETŐ / OK | brief V5 | a makett-jóváhagyás helyén egyeztetett eltérés áll (a felhasználó döntése az orkesztrátoron át, DT-F183a); a repóból nem igazolható. „A többi lap csak a HAMART után”: betartva (csak a HAMART lapja változott) |
| ir-mező | ELTÉRÉS (13) | — | az `ir`-en kívül írt fájlok: sablonok/*, MUNKAMENET.md, NYITOTT_FELADATOK.md, adat/jeloltek.tsv, licencek.tsv, nyilt_angol.tsv, konkordancia/Glossa_Ordinaria.tsv, olvasoi_kapu.py, teszt_*.py, nyilt_mag/*. Az egyeztetett eltérés a hatókört rögzíti, az `ir` bővítését nem mondja ki. Az `ir`-ben szereplő .github/workflows/ellenorzes.yml-t viszont nem érintette |
| Tanulmány-ellenőrzés | nem alkalmazandó | — | a diffben nincs *_bovitett.md vagy *_tanulmany.md |

ELTÉRÉS-tételek, súlyosság szerint:
1. (mechanikus, generátor) Az ÚSZ-tábla „Mit mutat” cellájából hiányzik a családon belüli változat mondata; ok: az augmentum a `_gorog_tovek`-ben (lexikon_general.py:8281). A K67b „teljesül” jelölése hamis, és nincs teszt, amely ezt fogná.
2. (tartalmi) A tanúblokk bevezetője minden tanúra a „ugyanazt a kapcsolatot látja” állítást mondja, holott a 4 Chain Lineage-sor csak együtt-idézés. Sérül a brief V2, a sablon 6 3. szabálya és a K67d.
3. (tartalmi) A közös generátorba beégetett szöveg: HAMART-specifikus bevezető és feltétel nélküli `GLOSSZA_MONDAT`; az átnézésnek nincs adatnyoma, a többi lapra így nem vihető át.
4. (tartalmi) K67f „nem része az 1. kiadásnak” és A27 „teljesül”, miközben az N-F183a szerint a döntés nyitott, a K67/A27 pedig kötelezőnek mondja.
5. (tartalmi) Az új szabályokra nincs HIBA-szintű kapu, és a CI-ben sincs ellenőrzés (`teszt_hatastortenet`, `tanu_kinyer ellenoriz`). A K67a ellenőrzés-oszlopa nem fedi a valóságot.
6. (tartalmi) Az N-F176a teljes lezárása a Vulgata-kiadás kérdésére is kiterjed, amely eldöntetlen.
7. (tartalmi, kis) A „4–5. sz.” kor a HCF 407-es és 420-as évéből nem vezethető le. A lapon Jeromos két különböző korral áll.
8. (mechanikus) Szó szerinti latin idézet a visszhang_tanuk.tsv `ellenorzes` mezőjében.
9. (mechanikus) „10 tanú 7 helyen” a jelentésben és a K67d-ben; a valóság 6 hely, ahogy a lap is írja.
10. (mechanikus) „F183.2 (generátor)” hivatkozás a K65 és a K67a–c sorában; a generátor-commit az F183.3 (49cf9c90).
11. (mechanikus) Elavult számok: chain_lineage.py docstringje „SEMA 2.58” (helyesen 2.57); VISSZHANG_README:4 és :26 „öt tábla” (már hat); a SEMA 2.52 címe öt táblát sorol; a Glossa-fejléc „a csomag lábjegyzetei” csak a 66 könyvet számolja.
12. (mechanikus) A Chain Lineage Browsernek nincs datasetek- és licencek-leltársora.
13. (mechanikus, alacsony) Az `ir`-mező túllépését a jelentés nem mondja ki; a workflow-fájl az `ir`-ben szerepel, mégsem módosult.
