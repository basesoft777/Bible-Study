# F152 — az ISTENTISZT-001 motívumlap-tervének hátraléka: napló

*FELADATOK #152 · brief: `F152_ISTENTISZT_TERV_HATRALEK_BRIEF.md` · ág: `claude/f152-hatralek-b7d3b3` · modell: claude-opus-5-5
(a brief `modell` mezője: opus — egyezik) · 2026-11-01*

## 0. Indítás

- Modell-ellenőrzés: kért `opus`, tényleges `claude-opus-5-5` — egyezik.
- Korábbi ág / worktree a #152-höz: nincs (helyi és távoli ágak, `git worktree list`); az ág a main `9cf0e43a`-ról indul.
- Próba-regenerálás a változás előtt (`PARDES_DATUM=2026-10-29 python eszkozok/general.py --cel lexikon --id <ID> --ir`,
  ISTENTISZT-001 és ALVIL-001): tartalmi nulla-diff (csak sorvég), az alapállapot reprodukálható.
- A C rész öt nyitott tétele a `NYITOTT_FELADATOK.md`-ben: N-F152a–e (F152.0).

## 1. B0 — mérés a változás előtt (main `9cf0e43a`)

`python naplok/F152_meres.py lexikon/ISTENTISZT-001_TUDOMANYOS.md lexikon/ALVIL-001_TUDOMANYOS.md`

| Mérőszám | ISTENTISZT-001 | ALVIL-001 |
|---|---|---|
| méret | 258 544 bájt (252,5 KB), 2 237 sor | 144 254 bájt (140,9 KB), 1 583 sor |
| a 6. Értelmezés kezdete | 1 713. sor, a lap 80%-ánál | 1 373. sor, a lap 86%-ánál |
| `scope=manual` | 162 | 74 |
| `forras=Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` | 120 (60 az 1/b.-ben, 60 a Minősítésben) | — |
| `forras=Segitsegul_hivni_az_Urat_tematikus.md` | 41 (31 az 1.-ben: 23 ts=2026-09-05, 7 ts=2026-09-08, 1 egyéb; 10 az 1/b.-ben) | — |
| proveniencia-sor (scope / forras / ts) | 231, ebből ugyanabban a szakaszban ismétlődő 181 (a `lekerdez.py` hat mezős sorával együtt, l. 8.) | 84, ebből ismétlődő 73 (59 + 13 az 1.-ben) |
| „gerinc” sor | 25, ebből nem dőlt üzemeltetői mondat 18 (oszlopfej 1, hamis-párhuzam sor 17) | 10, ebből 4 (oszlopfej 1, sor 3) |
| az 1Móz 25:21–26 azonos indoklású sora az 1/b.-ben | 6 | — |
| Minősítés jelölt-tábla | 61 sor, 20,3 KB (a címsortól a tábla végéig) | — |

A brief 2. szakaszának számai (az orkesztrátor mérése, `a06e76eb`) egyeznek; a méret 252,5 KB (a brief: 252,3), a jelölt-tábla
20,3 KB (a brief: 22,6 — más határral mérve). A „gerinc” a két nem dőlt, félkövér bevezetőben is áll (a 14. blokk „Rejtett
párhuzam” és „Hamis párhuzam” bekezdése); az elfogadási feltétel („az olvasónak szóló szövegben nem szerepel”) miatt ezek is
javítva (F152.2).

*(proveniencia: scope=lexikon/ISTENTISZT-001_TUDOMANYOS.md, lexikon/ALVIL-001_TUDOMANYOS.md @ 9cf0e43a | forras=naplok/F152_meres.py
(split('\n')) | ts=2026-11-01)*

## 2. A.1 — a két hibás indoklás (F152.1)

`python naplok/F152_A1_kapcsolatok_javit.py --ir` — sorösszevetés: 42 sor, eltérés 3 sor, csak az `indoklas` mezőben.

- 1Móz 4:26 → Jóel 2:32: a régi szöveg az ApCsel/Róm-kapcsolat másolata volt; az új a formula szó szerinti egyezése (az első
  ószövetségi hely és a prófétai csúcspont), a két vers Károli-szövegével (`konkordancia/Karoli_1908.tsv`).
- Zsolt 116:4 → 116:13, 116:13 → 116:17: „ugyanabban a zsoltárban, három versben (116:4, 116:13, 116:17)”.

## 3. A.3, B.2, B.3 — a generátor (F152.2)

- **A.3:** a kulcsszó-tábla oszlopfeje „Héber/görög szavak”; a hamis-párhuzam soraiban „*a motívum szavaiból a versben: kárá
  (H7121)*” (`lexikon_general._szo_kiejtessel`, a `blokk_14` új `szo_nev` paraméterén át); a két bevezetőben „szókapcsolat”,
  „motívumszó”. A dőlt üzemeltetői mondatok („Szótári gerinc (DT272) …”, „Gerinc-kombinációnként …”) maradnak.
- **B.2:** `szerep_kizart.kozos_proveniencia`: a blokkban legalább kétszer álló proveniencia-sor a helyén jellé rövidül (az F152.6 óta
  blokkonként egyedi: ‹E1›, ‹K1›, ‹M1› …; eredetileg †, ‡), és a blokk alá egyszer kerül („*Minden sor forrásmegjelölése
  (‹K1›): …*”, ill. „*A közös forrásmegjelölések: ‹K1› = … (n sor)*”); az egyszer álló sor a helyén marad. Bekötve: az 1. előfordulás-lábjegyzetei, az 1/b. lábjegyzetei, a Minősítés
  jelölt-táblájának „Forrás-keresés” oszlopa. Minden lexikonra.
- **B.3:** `szerep_kizart.osszevon`: az 1/b. csoportján belül az egymást követő versek (ugyanaz a könyv és fejezet), azonos
  „miért lett jelölt”, döntés, indok és lábjegyzet mellett egy sorban, tartományként („1Móz 25:21–26”); a lábjegyzet egyszer áll
  (azonos szövegű volt), a csoport darabszáma a jelölteké marad.
- Tesztek: `teszt_szerep_kizart` (+6 eset), `teszt_szotari_gerinc` (oszlopfej).

## 4. Kiejtés a kézi prózában (F152.3; az orkesztrátor feladatlistájáról, ugyanezen az ágon)

`python naplok/F152_kiejtes_javit.py`, mérés: `python naplok/F152_kiejtes_meres.py`. A kiejtés a `kiejtes_szoveg.kiejtes`
javaslata (DT430: gépi magyaros, „gépi” jelölés nélkül). Az orkesztrátor „pesat” alakja helyett a szabály szerinti
**pesát** (a ש alatti kámec: á).

| Forrás | Szó | Előtte | Utána |
|---|---|---|---|
| `motivumok/ISTENTISZT-001.md` | פְּשָׁט (pesát), רֶמֶז (remez), דְּרַשׁ (deras), סוֹד (szód) | 4 hiány | 0 |
| `motivumok/ALVIL-001.md` | שְׁאוֹל (seól, 2. szakasz), תְּהוֹם (tehóm, Kivonat) | 2 hiány | 0 |

A forrás összes kézi hiánya: ISTENTISZT-001 9 → 5, ALVIL-001 7 → 5. A megmaradt hiányok nem e tétel hatókörei (a felhasználó
kérése a négy PaRDeS-szóra és a seólra, tehómra szólt): ISTENTISZT-001 אֵשֶׁל (ésel), בְּ (be), שֵׁם (sém, 3. szakasz),
σωθήσεται, διεσώθησαν; ALVIL-001 ἄβυσσος (abüsszosz), ᾍδης (Hadész) négy szakaszban. A `motivumok/ALVIL-001.md` nem volt a brief
`ir` mezőjében — felvéve.

## 5. B.5 — újragenerálás és mérés a változás után (F152.4, `ba8e8393`; a számok az F152.6 utániak)

`PARDES_DATUM=2026-10-29 python eszkozok/general.py --cel lexikon --id <ID> --ir` (a lap első GENERÁLT ts-e), majd
`python naplok/F152_meres.py …` és `python naplok/F152_kiejtes_meres.py`.

| Mérőszám | ISTENTISZT-001 előtte → utána | ALVIL-001 előtte → utána |
|---|---|---|
| méret | 252,5 KB, 2 237 sor → **232,9 KB**, 2 209 sor (−19,6 KB, −7,8%) | 140,9 KB → **135,4 KB** (−5,5 KB) |
| a 6. Értelmezés kezdete | a lap 80%-ánál → 79%-ánál | 86% → 85% |
| `scope=manual` | 162 → 7 | 74 → 3 |
| `forras=…kereszthivatkozas_naplo.md` / `…tematikus.md` | 120 / 41 → 2 / 4 (a blokk alatti egy-egy megjegyzés-sorban) | — |
| ugyanabban a szakaszban ismétlődő proveniencia-sor | 181 → 6 (a maradék 6 a 6. Értelmezés kézi NAPLO-soraiban: a kézi forrás része, a generátor nem írja) | 73 → 0 |
| olvasói „gerinc” | 18 → 0 (a maradék 5 dőlt üzemeltetői mondat) | 4 → 0 |
| 1/b.: 1Móz 25:21–26 | 6 sor → 1 sor (+ Jer 7:10–11 és a többi szomszédos pár) | — |
| Minősítés jelölt-tábla | 20,3 KB → 15,4 KB (61 sor; a DT-F152a tárgya) | — |
| kiejtés-hiány a lapon (kézi) | 4 (a PaRDeS négy szava) → 0 | 6 → 4 (a seól, a tehóm javítva; maradt: ἄβυσσος, ᾍδης ×3) |

A Motívumlap-terv becslése (40–45 KB tartalomvesztés nélkül) a Minősítés-tábla (DT-F152a) és az N-F152f tételei nélkül nem
érhető el; a mostani −19,6 KB a forrásmegjelölésből és a tartomány-összevonásból jön. A proveniencia nem veszett el: minden
jel (‹E1›, ‹K1›, ‹M1› …) a blokk alatti sorban a teljes `scope=… | forras=… | ts=…` alakot hordozza, a soronkénti szám mellett.

CI-emuláció (`eszkozok/ellenorzes/futtat.py`, 9cf0e43a..ba8e8393): kilépés 0, SÉRTÉS 0; FIGYELMEZTETÉS 4 — az ALVIL-001 Kivonat
ἄβυσσος kiejtése (e tétel hatókörén kívül, l. 4.), a MUNKAMENET.md két régi D34-helye (nem e tétel), és egy commit-üzenet
`indoklas` mezőnév-szava.

*(proveniencia: scope=lexikon/ISTENTISZT-001_TUDOMANYOS.md, lexikon/ALVIL-001_TUDOMANYOS.md @ ba8e8393 | forras=naplok/F152_meres.py,
naplok/F152_kiejtes_meres.py | ts=2026-11-01)*

## 6. A Megvalósulás-jelentés 32 pontja

Forrás: „Megvalósulás-jelentés ISTENTISZT-001” (Claude Docs, rev 7, 2026-11-01), a négy pontcsoport táblái. Állapot: **kész**
(a #152 előtt vagy ebben), **⛔** (ebben a feladatban, döntésre vár), **N** (követett nyitott tétel).

| # | Pont (a jelentés szerint) | Jelentés | Most |
|---|---|---|---|
| P1 | Hívás és felelet | megvalósult | kész |
| P2 | Hívás és megmenekülés (a Zsolt 116 → Jóel → ApCsel, Róm lánc) | részben | N-F152c |
| P3 | A halál szorításában (ALVIL-001, Zsolt 116:3) | részben | N-F152c |
| P4 | Bűn utáni válasz (HAMART-001) | részben | N-F152c |
| P5 | A mélység kérdése (TEREMT-001) | nem | N-F152c |
| P6 | Ismerni és nem ismerni | megvalósult | kész |
| P7 | A liturgikus hármas | megvalósult | kész |
| P8 | Két oltár | megvalósult | kész |
| P9 | „Mindenki, aki” (az egyetemessé válás) | részben | N-F152c |
| P10 | A kívülálló elvárása | megvalósult | kész |
| P11 | Négy forrás egybeesése | megvalósult | kész |
| P12 | Hit, hirdetés, hívás (Róm 10:14) | megvalósult | kész |
| E1 | Az alkalmazási rész a lapon | megvalósult | kész |
| E2 | „Mit mutat” mondat minden adatblokk előtt | megvalósult | kész |
| E3 | Határ-összefoglalás okonként | megvalósult | kész |
| E4 | Kulcsszavak egy helyen | megvalósult | kész (az oszlopfej „Gerinc” → „Héber/görög szavak”, F152.2) |
| E5 | Kapcsolódó motívumok — próza a kapcsolatról | részben | N-F152c |
| E6 | Kilenclépéses prózasablon a `sablonok/`-ba | nem | N-F152g |
| E7 | A névtelen hívás és a Seól | nem | N-F152c |
| L1 | Minden elutasított jelölt háromszor (Minősítés-tábla, 4. KH nyers lista) | részben | ⛔ DT-F152a (a tábla); N-F152f (a 4. lista) |
| L2 | Ugyanaz a forrásmegjelölés 120-szor | nem | **kész** (F152.2/F152.4: 120 → 2) |
| L3 | Egy előfordulás átlag 7 (ma 10,2) szakaszban | nem | N-F152f |
| L4 | Tartományok szétbontva (1Móz 25:21–26) | nem | **kész** (F152.2/F152.4) |
| L5 | Ugyanaz az érték egy oszlopban | nem | N-F152f |
| L6 | Kétszer leírt mezők (a PaRDeS-szintek magyarázata) | nem | N-F152f |
| L7 | Lefordítatlan szótári anyag | megvalósult | kész |
| L8a | 1Móz 4:26 → Jóel 2:32 másolt indoklása | nem | **kész** (F152.1) |
| L8b | Zsolt 116: „ugyanabban a versben, háromszor” | nem | **kész** (F152.1) |
| L8c | A negatív kritérium a lap elejére | nem | ⛔ A.2 (a Kivonat szövege) |
| O1 | A próza vezesse az olvasót | részben | N-F152b |
| O2 | Ki/be kapcsolható appárátusok | nem | N-F152a |
| O3 | Jelölt üres hely, ahol nincs próza | megvalósult | kész |

Összesen 32: kész 17 (13 korábbi + 4 most), ⛔ 2 (L1 egy része, L8c), követett nyitott tételben 13 (N-F152a–g). A jelentés
„belső szó az olvasói szövegben” megjegyzése (a „gerinc”, nem számozott pont) szintén kész (F152.2). A brief N-F<nn>a–e tételein
túl az N-F152f (L1 4. lista, L3, L5, L6) és az N-F152g (E6) új, és az N-F152c a P2-vel és a P9-cel bővült — ezek nélkül a 6.
elfogadási feltétel („mindegyik … követett nyitott tételben áll”) nem teljesülne.

## 7. ⛔ Megállás — két döntés a felhasználónál

### 7.1 A.2 — a Kivonat szövegjavaslata (`motivumok/ISTENTISZT-001.md`, `kivonat` rés)

A meglévő Kivonat első bekezdése után, új bekezdésként:

> A motívum határát a szerkezet húzza meg: csak az aktív, invokáló קָרָא בְּשֵׁם (kárá besém) tartozik ide, amelyben valaki
> segítségül hívja Isten nevét. A passzív נִקְרָא … עַל (nikrá … al) szerkezet, amely a név alatti hovatartozást fejezi ki
> (2Sám 6:2; Jer 7:10), akkor sem, ha ugyanazt a két gyököt használja. A motívum nem az imádság vagy az istentisztelet
> általában: a formulán kívüli segítségül hívás (például ApCsel 7:59) a tágabb fogalomhoz tartozik, ide nem.

Alap: a negatív kritérium és a fölérendelt fogalom a `motivumok.tsv`-ben (`negativ_kriterium`, `folerendelt_fogalom`); a 2Sám 6:2,
a Jer 7:10 és az ApCsel 7:59 az 1/b.-ben ezzel az indokkal elutasított jelölt (`jeloltek.tsv`). Jóváhagyás után beírás és
újragenerálás.

### 7.2 DT-F152a — a Minősítés jelölt-táblája (`DONTESEK.md`)

A 61 soros tábla minden sora az 1/b.-ben (60 elutasított) vagy az előfordulás-táblában (Róm 10:12, beépítve) is áll, ugyanazzal
a döntéssel és indokkal; mérete a B.2 után 15,4 KB. (a) jelvény a soron, a tábla megszűnik (réslista-módosítás,
`adat/res_forras.tsv`); (b) csukva (`<details>`); (c) marad. Javaslat: (b).

## 8. Az ellenőr eltérései és a javítás (F152.6)

`naplok/ELLENOR_F152.md` (9cf0e43a..531d1f62): ELTÉRÉS 3 — mindhárom javítva.

1. **B.2 lefedettség.** A `PROV_HARMAS` a `lekerdez.py` hat mezős sorát (`scope | forras | strong | n | ts | csatorna`) nem
   ismerte fel; az 1/b. „Gépi keresés” 21 lábjegyzetében ugyanaz a sor maradt. Javítva: a minta a forras és a ts közötti
   további mezőket és a ts utáni `csatorna=`-t is elfogadja (új teszt: `test_lekerdezes_mezoi`). A B0 újramérve ezzel a
   mintával (a mérőszkript a generátor mintáját importálja): 192 → 231 proveniencia-sor, 161 → 181 ismétlődő; utána 6.
2. **B.2 jel-ütközés.** A † / ‡ blokkonként mást jelentett, és ütközött az Abbott-Smith † jelével. Javítva: blokkonként egyedi
   előtagú jel (‹E1› az előfordulások, ‹K1› a kizárt helyek, ‹M1› a minősítés), és a Jelmagyarázatban új bekezdés
   („Közös forrásmegjelölés”) — ez a közös Jelmagyarázat-blokk, minden lexikonlapra érvényes. A † a lapon már csak az
   Abbott-Smith jeleként áll (3 előfordulás).
3. **A napló 1. táblája.** A tematikus forrásmegjelölés bontása 31 + 10 (javítva).

A „NEM ELLENŐRIZHETŐ” A.1-sor nyomán az 1Móz 4:26 → Jóel 2:32 indoklása pontosítva: „az 1Móz 4:26-ban áll először az
Ószövetségben” helyett „az 1Móz 4:26-ban, a motívum első ószövetségi helyén” (az előfordulás-tábla szerint; a Strong-hármas
névadásban már az 1Móz 2:19-ben is együtt áll) — `naplok/F152_A1b_joel_pontosit.py`, sorösszevetés: 1 sor, 1 mező.

A CL3 („a többi 6 lexikonlap nincs újragenerálva”): a brief B.5-je csak az ISTENTISZT-001 és az ALVIL-001 újragenerálását írja
elő; a generátor-változás a többi lapon a következő újrageneráláskor jelenik meg (a #36 / #123 menetében).
