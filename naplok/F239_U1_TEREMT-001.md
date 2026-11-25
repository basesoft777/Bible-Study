# F239 U1 — TEREMT-001 (tehóm), gépi adat-előkészítés: összesítő

*FELADATOK #239 · U1 · végrehajtó: `claude-sonnet-5-5` (kért: `sonnet`, egyezik) · 2026-11-23 · ág: `claude/nervous-kare-9d2361` · alap: main `fe37880b` + a #239 befogadó commitja `1b34dd1f`.*
*Az U1 csak mér és listáz: jelentéstartományt nem választ, prózát nem ír, jelöltet nem dönt el. Az egyetlen adatírás: 28 `nyitva` jelölt-blokksor az `adat/jeloltek.tsv`-be (2. pont). A `motivumok/`, `lexikon/`, `tematikus_lezart/` fájlokhoz nem nyúltam; az `eszkozok/` alatti kódot nem módosítottam.*
*Egyszeri szkriptek: `naplok/F239_U1_*.py` (a pontoknál megnevezve). A lekérdezés-naplózás: `naplok/F239_lekerdezesek.tsv` (54 sor; `lekerdez.py --naplo F239`), a nyers kimenetek: `naplok/F239_U1_TEREMT-001_lekerdezesek.txt`.*

**Gerinc-elem:** a motívum azonossága lexikai (`adat/motivumok.tsv`: `azonossag_tipusa=lexikai`), a hordozó a תְּהוֹם (H8415) és az LXX-közvetített ἄβυσσος (G0012). Egyetlen szó a gerinc, ezért minden előfordulás-sor a H8415-ön vagy a G0012-n „lóg” (`gerinc_elem` oszlop a TSK-kban).

## 1. A hét lépés determinisztikus része (1., 3., 4., 5., 6. lépés)

**1. lépés, gerinc-metszet (levezetés)** — futtatva: `python eszkozok/lekerdez.py gerinc --naplo F239 --lepes B2 <szakaszok>` (a futtató szkript: `naplok/F239_U1_01_futtat.py`):

| bemenet | metszet | grammatikai szűrő kiveszi | gerinc |
|---|---|---|---|
| 1Móz 1:2 + 7:11 + 8:2 (14 / 23 / 11 egyedi Strong) | 3 | H9002, H9009 | **H8415** |
| mind a 35 H8415-vers (a Jób 41:32-vel) | 1 | (nincs) | **H8415** |
| Zsolt 33:7 + Jób 38:16 + Ézs 51:10 + Jón 2:6 + Hab 3:10 | 1 | (nincs) | **H8415** |
| a 9 G0012-vers (Jel 9:1, 9:2, 9:11, 11:7, 17:8, 20:1, 20:3, Luk 8:31, Róm 10:7) | 2 | G3588 | **G0012** |
| 1Móz 1:2 + Jel 20:1 (ÓSZ–ÚSZ kontroll) | 0 | (nincs) | üres: a két nyelv gerince nem közös Strong; az összekötés az LXX-híd (6. pont) |

Proveniencia (a legszélesebb futás; a többi a `F239_lekerdezesek.tsv`-ben): `scope=range:1Móz 1:2+1Móz 7:11+1Móz 8:2+… (35 szakasz) | forras=TAHOT_kivonat.tsv | n=1 | ts=2026-11-23T11:58Z`; `scope=range:Jel 9:1+…+Róm 10:7 | forras=TAGNT_kivonat.tsv | n=1 | ts=2026-11-23T11:58Z`.
A gerinc-metszet nem generál mező-hipotézist (2. lépés): az az U2 dolga.

**3. lépés, teljes ÓSZ/ÚSZ scan** — `python eszkozok/lekerdez.py scan H8415` és `scan G0012` (`--naplo F239 --lepes B2`):
- H8415: **35 igehely, 36 szó-előfordulás** (Zsolt 42:8-ban kétszer áll); G0012: **9 igehely, 9 előfordulás**. Összesen 44 vers.
- Mind a 44 vers az adatban is áll (`E` = `adat/elofordulasok.tsv` és `J:beépítve` = `adat/jeloltek.tsv`): **eltérés 0** (a Strong-háló nem talál olyat, amit az adat ne ismerne). A Jel 9:1–2 és a Jel 20:1–3 az adatban tartomány-sor; a scan a verseket külön adja (a 20:2-ben nincs G0012).
- Részletes lista, gerinc-elemmel és adat-állapottal: `naplok/F239_U1_TEREMT-001_scan.tsv` (44 sor).
- Proveniencia: `scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H8415 | n=35 | ts=2026-11-23T11:57Z`; `scope=TAGNT-teljes | forras=TAGNT_kivonat.tsv | strong=G0012 | n=9 | ts=2026-11-23T11:57Z`. (A `TAHOT-teljes` a kivonat egészét jelenti, nem az ÓSZ kánonját: CLAUDE.md „Adat-tár”.)

**4. lépés, kollokáció (szópár egy versben)** — `lekerdez.py kollokacio <gerinc> <társ>`; a társ-szavak jelöltlistája gépi (a H8415-versekben legalább 5, a G0012-versekben legalább 3 versben álló, nem grammatikai Strong); a mező-hipotézis az U2 dolga. 10 pár, `naplok/F239_U1_TEREMT-001_kollokacio.tsv`:
H8415 + H4325 (víz) 14 vers · + H7227 (sok) 8 · + H8064 (ég) 7 · + H3220 (tenger) 7 · + H0776 (föld) 6 · + H3605 (mind) 6 · + H3068 (JHVH) 5; G0012 + G1492 3 · + G0032 (angyal) 3 · + G0305 (felmegy) 3. A korpuszszintű találatszám minden párnál megegyezik a gerinc-versek közötti számmal (a társ-szó csak e versekben áll együtt a gerinc-szóval, természetesen).
Proveniencia pl.: `scope=TAHOT-teljes+TAGNT-teljes | forras=TAGNT_kivonat.tsv+TAHOT_kivonat.tsv | strong=H8415+H4325 | n=14 | ts=2026-11-23T11:58Z`.

**5. lépés, igealak-ellenőrzés** — `lekerdez.py igealak H8415` / `G0012` (`naplok/F239_U1_TEREMT-001_igealak.tsv`: 36 + 9 sor). A H8415 főnév (nem igealak): egyes (תְּהוֹם) és többes (תְּהוֹמוֹת/תְּהֹמוֹת) alakok, előtagokkal; a G0012 egyes (ἄβυσσον, ἀβύσσου) alak. A binyan/alak szerinti csoportosítás igealak híján nem értelmezhető; az „EMBERI DÖNTÉS” sort az eszköz írja. Proveniencia: `scope=TAHOT-teljes | forras=TAHOT_kivonat.tsv | strong=H8415 | n=36 | ts=…`, `scope=TAGNT-teljes | … | strong=G0012 | n=9 | ts=…` (a `F239_lekerdezesek.tsv` B4 sorai).

**6. lépés, LXX-híd** — `lekerdez.py lxx-hid <igehely>` a 35 H8415-versen (`F239_U1_01_futtat.py`; `naplok/F239_U1_TEREMT-001_lxx_hid.tsv`: a vers tartalmi LXX-szavai, a G0012 jelölve; a héber és a görög szó párosítása nem gépi) és a G0012 oldal (`naplok/F239_U1_06_lxx_g0012.py`; `naplok/F239_U1_TEREMT-001_lxx_g0012.tsv`):
- a 35 H8415-versből **30**-ban áll az LXX-versben ἄβυσσος (G0012); **5**-ben nem: 2Móz 15:5 (βυθός), 2Móz 15:8, 1Móz 49:25, Péld 8:27, Péld 8:28.
- az LXX 34 Károli-kulccsal rendelkező G0012-versének **30**-ban H8415 áll a héber versben; **4**-ben nem: Ézs 44:27, Jób 36:16, Jób 41:31, Zsolt 71:21 (a Zsolt 71:21 valószínűleg versszámozás-eltolás a Zsolt 71:20-hoz; az LXX többlete vagy más héber szó az U2 kérdése). További 14 G0012-token (Dán, Ódák) nem kapott Károli-kulcsot: kihagyva.
- az ÚSZ 9 G0012-helye (az ÚSZ-ben nincs LXX-vers): Luk 8:31, Róm 10:7, Jel 9:1, 9:2, 9:11, 11:7, 17:8, 20:1, 20:3. Az `lxx-hid` ÚSZ-versre nem fut („Nincs LXX_OS-fájl ehhez a könyvhöz”: hibaüzenet, nem adat); az ÚSZ-helyek idézet-kapcsolata (pl. Róm 10:7 ↔ 5Móz 30:13 / Zsolt 107:26) gépi forrás nélkül nem mérhető, az U2 olvassa.
- Proveniencia pl.: `scope=range:1Móz 1:2 | forras=LXX_OS/genesis.tsv+TAGNT_kivonat.tsv | n=19 | ts=2026-11-23T11:54Z`; a G0012-oldalra: `scope=LXX_OS-teljes (G0012) × TAHOT_kivonat.tsv (H8415) + TAGNT_kivonat.tsv (G0012) | forras=konkordancia/LXX_OS/*.tsv | ts=2026-11-23`.

## 2. Teljesség-mérés három hálóval

Futtatva: `python eszkozok/teljesseg_meres.py TEREMT-001 --karoli-szavak "mélység,mély,mélységes,örvény,fenékig" --ki naplok/F239_U1_TEREMT-001_teljesseg` (a szótári alakok listáját az eszköz adta: `a 32, mélység 28, víz 7, nagy 4, mély 4, mélységes 3, hullámok 2, ár 2, … örvény 1, … fenékig 1, … kút 1`; a mélység-csoport alakjait választottam: a kontextus-szavak (víz, nagy, föld, tenger, a) tömegesen jelölnének, ezért kimaradnak). Az eszköz maga nem ír adattáblát.

| háló | találat | E | J | ELTÉRÉS |
|---|---|---|---|---|
| Strong (H8415 + G0012) | 44 | 44 | 0 | **0** |
| Károli szavai (5 szótári alak) | 136 | 40 | 1 | **95** (gerinc a versben: 0) |
| szótár (BDB, Thayer példahelyei) | 44 | 43 | 0 | **1** (Jób 42:8: „BDB H8415 sorszam 27”; gerinc a versben: nincs) |

- E-vers, amelyet egyik háló sem ad: Jel 20:2 (a Jel 20:1–3 tartomány-sor kibontásának mellékterméke: a 20:2-ben nincs G0012; nem eltérés a háló felől).
- A teljes eltérés-lista: `naplok/F239_U1_TEREMT-001_teljesseg.tsv` (224 sor).
- A 96 eltérés gépi osztályozása (döntés nélkül: a vers TAHOT/TAGNT-tokenjei közül az, amelynek angol glosszája mélység-szó: `naplok/F239_U1_02_osztaly.py`) → **30 blokk** (29 a Károli-szó hálón, 1 a szótár-hálón), a vers-listák: `naplok/F239_U1_TEREMT-001_teljesseg_blokkok.tsv`. A legnagyobbak: H6013 (עָמֹק, „deep”) 15 vers, „osztálytalan: mélység” 15 vers, H4688 (מְצוֹלָה, „depth”) 10, H0953 (בּוֹר, „pit”) 9, „osztálytalan: mély” 8, H6009 7, H8639 (תַּרְדֵּמָה, „deep sleep”) 6, G0899 (βάθος) 6.
- **`jeloltek.tsv`-be írt sorok: 28 `nyitva` blokksor** (DT-F123o minta: lexémánként egy sor, a sor igehelye a blokk egy, még nem használt verse; a többi vers a blokkok-fájlban áll; a 30 blokkból kettőt teljesen elnyeltek a már felhasznált versek (a verseik már másik blokk sorának igehelyei); ezek jelölése a másik sor indoklásának kiegészítő mondata). Ebből a **Károli-szó háló** 27 sor (indoklás: „Károli-szó háló”; `forras_kereses`: a mérés proveniencia-sora), a **szótár-háló (BDB/Thayer)** 1 sor (Jób 42:8). A **Strong-háló nem hozott** sort. Az írás: `python naplok/F239_U1_02_jelolt_sorok.py --ir` (kulcs-ütközés ellenőrzés, a régi 929 sor soronkénti összevetése írás előtt és után: eltérés nincs; `git diff --stat adat/jeloltek.tsv`: +28, 0 törlés). A sorok másolata: `naplok/F239_U1_TEREMT-001_jelolt_sorok.tsv`.
- A sorok a mérés eltéréseit rögzítik, **döntést nem hordoznak**: a mélység-szavak (עָמֹק, מְצוֹלָה, בּוֹר, βάθος, βυθός …) mind a Károli „mély/mélység/örvény” szavával fordított, de nem תְּהוֹם/ἄβυσσος helyek; a lexikai negatív kritérium (a תְּהוֹם gyököt kell tartalmaznia) szerint várhatóan elutasítás, de ezt az U2 dönti blokkonként.
- Proveniencia: `scope=Karoli_1908-teljes | forras=Karoli_1908.tsv+adat/szoto/karoli_szotari_alak.tsv | szotari_alak=fenékig+mély+mélység+mélységes+örvény | n=136 | ts=2026-11-23T11:55Z`; `scope=G0012+H8415 | forras=adat/bdb_vers_jelentes.tsv+adat/thayer_vers_jelentes.tsv (karoli_vers) | n=44 | ts=2026-11-23T11:55Z`; `scope=TAHOT-teljes+TAGNT-teljes | … | strong=G0012+H8415 | n=44 | ts=2026-11-23T11:55Z`.

## 3. Felmérő lekérdezés és próza-lefedettség

Futtatva: `python eszkozok/motivum_felmeres.py TEREMT-001 --ki naplok/F239_U1_TEREMT-001_felmeres` és `python eszkozok/proza_lefedettseg.py TEREMT-001 --kimenet naplok/F239_U1_TEREMT-001_proza_lefedettseg.md`.
- Felmérés: (a) **251 kísérő Strong** a 45 motívumversben (46 grammatikai Strong kizárva); (b) **9 fejezet × másik motívum** pár, 5 másik motívum (ALVIL-001 3, HAMART-001 3, ISTENTISZT-001, MENNY-001, TEREMT-002 1–1): közös vers csak az 1Móz 1 × TEREMT-002 és az Ez 31 × ALVIL-001 fejezetben; (c) **4 válasz-találat** (H6030/H8085/G0191, 3 motívumvershez: Ézs 51:10, Jón 2:6, Jel 9:11). A jelölt-sort nem írtam (2. szabály: ezek jelöltként mehetnek tovább, az U2 dönt). Fájlok: `…_felmeres.md`, `…_kiserok.tsv`, `…_szomszedok.tsv`, `…_valasz.tsv`.
  Proveniencia (a `felmeres.md`-ből): `scope=TEREMT-001 előfordulási versei (42 sor, 45 vers) | forras=adat/elofordulasok.tsv + konkordancia/TAHOT_kivonat.tsv + TAGNT_kivonat.tsv, szűrés: adat/grammatikai_strongok.tsv (46 grammatikai Strong kizárva) | ts=2026-11-23T11:59Z`; `scope=TEREMT-001 fejezetei (36 fejezet) × adat/elofordulasok.tsv többi motívuma | … | ts=2026-11-23T11:59Z`; `scope=TEREMT-001 előfordulásai ±3 vers, azonos fejezet | … | valasz=H6030+H8085+G0191+G1522+G0611 | ts=2026-11-23T11:59Z`.
- Próza-lefedettség (mérés, nem ítélet; az eszköz nem ír proveniencia-sort): a `motivumok/TEREMT-001.md` 3 bekezdés, 2085 karakter; **42 előfordulásból 9 megnevezett, 33 nem**; kapcsolat, motívumközi kapcsolat, nyitott jelölt: 0 sor. Egyenetlenség: mindkét tartalmi blokk „kevés próza az elemre”. Proveniencia (általam): `scope=motivumok/TEREMT-001.md × adat/elofordulasok.tsv, kapcsolatok.tsv, motivum_kapcsolatok.tsv, jeloltek.tsv (a 2. pont előtti állapot) | forras=eszkozok/proza_lefedettseg.py | ts=2026-11-23`. A „nyitott jelölt: 0” a 28 új sor beírása előtti állapot.

## 4. Bizonyítéklap

`python eszkozok/bizonyiteklap.py --motivum TEREMT-001 --kimenet naplok/BIZONYITEK_TEREMT-001.md` → 42 adatsor, **45 vers** a tartományok kibontásával, 2 lánc-szó (H8415, G0012). Gyakorisági alapvonal: H8415 35 vers / 23204 (0,0015); G0012 9 / 7957 (0,0011). 44 versben egy lánc-szó áll; **egyben, a Jel 20:2-ben, a lánc szava nem áll** (a Jel 20:1–3 tartomány-sor kibontásának mellékterméke, l. 2. pont); a Zsolt 42:8-ban a H8415 kétszer áll. Fordított sorrendű ismétlés (a lánc két szavának ellentétes sorrendje) nincs. Proveniencia (a fájlból): `scope=45 vers; lánc: H8415, G0012 | forras=konkordancia/TAHOT_kivonat.tsv, konkordancia/TAGNT_kivonat.tsv (kulcs: Károli-vers), konkordancia/Karoli_1908.tsv | ts=2026-11-23T11:59Z`.

## 5. Igeszakasz-blokkok (C-ia)

A `genezis/`, `ujszovetseg/`, `melyelemzesek/` tanulmányai közül a H8415/G0012/tehóm szót csak három tartalmazza: `1Moz_1v2-2v3` (1Móz 1:2), `1Moz_7v1-24` (7:11, kereszthivatkozás a 8:2-höz), `1Moz_8v1-22` (8:2). A többi 21 tanulmány tartománya nem érint TEREMT-001-vers; ÚSZ-tanulmány (Róm 8:10, 1Thessz 5:23, Zsid 4:12) nem. Futtatva (`--ir` nélkül): `python eszkozok/tanulmany_kinyer.py genezis/<tanulmány>_bovitett.md --jelentes naplok/F239_U1_TEREMT-001_kinyer_<tanulmány>.md` → mindháromnál **0 blokk, 0 új jelölt-sor, 0 hiba**: a három tanulmányban nincs `<!-- IGEHELY-BLOKK: … -->` jelölő, vagyis kinyerhető blokk jelenleg nincs; a motívumot a három tanulmány próza-szinten említi. A kinyerés üres eredménye nem negatív lelet a tartalomra. A #74 (a három tanulmány újraírása) után a kinyerés ismétlendő. Proveniencia: `scope=genezis/1Moz_1v2-2v3_bovitett.md (+7v1-24, 8v1-22) | forras=eszkozok/tanulmany_kinyer.py (--ir nélkül) | ts=2026-11-23`.

## 6. Nave-jelöltlista

`python naplok/F239_U1_06_nave_jeloltek.py` (az `eszkozok/szerep_nave.py` `jeloltek()` szabálya: legalább 2 motívumvers, legalább 1% arány, `tiltott` kizárva) → `naplok/F239_U1_TEREMT-001_nave_jeloltek.tsv`: **11 jelölt-téma**, döntés nélkül (meglévő `tematikus_temak.tsv` döntés: 0). Elöl: NAVE-3885 PIT (3 motívumvers: Jel 9:11, 11:7, 17:8; arány 0,158), NAVE-0305 ANIMALS 3, NAVE-1400 DEW 2 (0,125), NAVE-1682 EPIC 2, NAVE-1213 CONTINENTS 2, NAVE-4643 SONG, NAVE-3906 POETRY, NAVE-1502 EARTH, NAVE-3189 MANASSEH, NAVE-1676 EPHRAIM, NAVE-3986 PSALMS. Proveniencia (a fájl fejléséből): `scope=TEREMT-001 adat/elofordulasok.tsv (42 sor) × konkordancia/Nave_basokant.tsv | forras=split('\t') | ts=2026-11-23`.

## 7. Fordítás- és szakaszcímke-lista

- `python eszkozok/glossza_lexikon_forditas.py lista --id TEREMT-001 --kimenet <repón kívül> --ki naplok/F239_U1_TEREMT-001_forditas_lista.tsv` → **nem készült lista**: „TEREMT-001: BEFAGYASZTVA — a lap nem generálódik újra (adat/lap_befagyasztas.tsv)”, majd „a lap nem renderelődött (TEREMT-001): nincs fordítás-hívás vagy kimenet — a lista nem készült”. Az eszköz a befagyasztott lapot nem rendereli; az eszköz módosítása nem az én dolgom. A hiba: parancs fent, első üzenet: „TEREMT-001: BEFAGYASZTVA…”. Folytatás a befagyasztás feloldása (vagy az új generátor `--kimenet`-es próbafutása) után az U2/U3 technikai része.
- `python eszkozok/szakasz_cimke_levezet.py ellenoriz --id TEREMT-001 --ki naplok/F239_U1_TEREMT-001_szakasz_cimke.tsv` → **42 sor, levezetve 0, egyezik 0, eltér 0, jelzés 42**: minden sorra `[J3] üres mező: lexikon_szotar, lexikon_entry_id, jelentes_szam` (a régi TEREMT-001 sorokból e három mező üres). Jelzésnél csak lista (a `--ir` nem futott). Proveniencia: `scope=adat/elofordulasok.tsv TEREMT-001 sorai | forras=eszkozok/szakasz_cimke_levezet.py ellenoriz | ts=2026-11-23`.

## 8. LXX gépi megfelelők és BDB nyelvi háttér — KIHAGYVA

`python eszkozok/visszhang/megfelelo_kinyer.py lxx --motivum TEREMT-001` nem futott: az `lxx` alparancsnak nincs száraz módja és `--kimenet` kapcsolója, csak írni tud (`tabla_ir(uj)` újraírja az `adat/visszhang_megfelelok.tsv`-t, a hívás a `--motivum` argumentumon kívül mást nem fogad), és a TEREMT-001-nek ma 0 sora van a táblában (a brief szerint a lánc még nincs eldöntve), így a futás sem hozna gépi bemenetet (a `parok_szuksegesek` a már felvett targum/vulgata sorokból épül). A feladat írásmentes szabálya szerint kihagytam. A hiányt részben fedi a 6. pont LXX-hídja (a vers LXX-szavai, a ἄβυσσος jelölve). A BDB nyelvi háttér (BDB/Thayer a példahelyeken) a 2. pont szótár-hálójában áll (44 hely).

## 9. Határ gépi része

`python eszkozok/motivum_hatar.py --motivum TEREMT-001 --kimenet <repón kívül>` (a kimenet másolata: `naplok/F239_U1_TEREMT-001_hatar_gepi.md`; a `naplok/HATAR_TEREMT-001.md` fájlt nem írtam felül, az az U2 bemenete):
- hordozó: `lexikai`; beépített sor 42 (45 vers); **részhalmaz-kérdés 0** (egyik másik motívummal sincs A ⊆ B vagy ≥80% átfedés); közös vers: ALVIL-001 1 vers (2%/1%), TEREMT-002 1 vers (2%/33%); kapcsolat egyikkel sincs.
- negatív-kritérium próba: **nem fut** (nem formulaikus hordozó; a lexikai kiterjesztés az N-F150a).
- Megjegyzés: az eszköz fejlécében álló `ts=2026-11-16T14:07Z` az eszköz saját, régebbi bemenet-pillanatképének ideje (`bemenet=…@…` hash-ek); az eszköz ma futott. Proveniencia (a fájlból): `scope=elofordulasok.tsv (beépített igehelyek, verssé bontva) + motivumok.tsv + motivum_kapcsolatok.tsv | forras=motivum_hatar.py | motivum=TEREMT-001 | ts=2026-11-16T14:07Z`.

## 10. A régi adat alakja az új generátorhoz

`python naplok/F239_U1_10_regi_adat.py` → `naplok/F239_U1_TEREMT-001_regi_adat.tsv`. Csak lista; a javítás az U3 technikai része.
- **`jeloltek.tsv` `forras_kereses` alakjai** (a ma felvett 28 sor nélkül, 44 sor): 41 × „TAHOT_kivonat.tsv visszakeresés (eszkozok/f3_2_betoltes.py), retroaktív F3.2 betöltés” (`beépítve`); 2 × „napló: Tehom_kereszthivatkozas_naplo.md §…” (`elutasítva`: 2Pét 2:4, Jel 21:1); **1 × „scan H8415” (`beépítve`, Jób 41:32) — ez a régi `scan H…` alak, amely a TEREMT-002-n B04-et adott**; az U3 technikai része javítsa. A lapgen nem futott, a hatás nem mért.
- **`res_forras.tsv`** 9 sora mind **nem** a `motivumok/TEREMT-001.md` kézi forrásra mutat: `kivonat`, `2b`, `miert_fontos`, `ertelmezes`, `modszertan` → `tematikus_lezart/Tehom_tematikus.md`; `minosites` → `tematikus_lezart/naplok/Tehom_kereszthivatkozas_naplo.md`; `alatamasztas`, `alkalmazas`, `tanitoi` → `adat` (szöveg a sorban). A `alkalmazas` sor áll, pedig a DT756 kivezette. A kivonat-sor miatt az új generátor `B47`-et ad (a brief 1. pontja).
- **N58 (Jób 41:32)**: nyitva. A `tematikus_lezart/Tehom_tematikus.md` 51. sora még „35-ször”, a 84. sor „egyedi versek száma emiatt 34”; a mai scan 36 szó-előfordulás / 35 igehely; a Jób 41:32-t a régi tanulmány nem említi. Az adatban a Jób 41:32 E-sor és beépített jelölt (`scan H8415`) áll.

## Átadás az U2-nek

- **Új `nyitva` jelölt: 28 sor** az `adat/jeloltek.tsv`-ben (27 a **Károli-szó háló**, 1 a **szótár-háló** hozta; a Strong-háló 0-t). Ezek lexéma-blokkok (30 blokk, vers-listák a `…_teljesseg_blokkok.tsv`-ben); az elbírálás az U2 dolga.
- **Elbukott / kihagyott pontok:** a 7. pont fordítás-listája (a lap BEFAGYASZTVA, a lista nem készült); a 8. pont (`megfelelo_kinyer.py lxx` csak írni tud; kihagyva); az 5. pontban kinyerhető blokk 0 (a három tanulmányban nincs IGEHELY-BLOKK jelölő); a `szakasz_cimke_levezet` 42 jelzést ad (üres szótár-mezők); az `lxx-hid` ÚSZ-versre nem fut.
- **Nem hiba, de az U2 kérdése:** az LXX 4 G0012-verse H8415 nélkül (Ézs 44:27, Jób 36:16, Jób 41:31, Zsolt 71:21); a H8415 5 verse G0012 nélkül az LXX-ben; a szótár-háló Jób 42:8; a régi `scan H8415` alak a Jób 41:32-n; N58; a `res_forras` kivonat-sor.
- **U2 bemenete (fájlnevek, mind `naplok/`):** `F239_U1_TEREMT-001.md` (ez), `F239_U1_TEREMT-001_scan.tsv`, `…_kollokacio.tsv`, `…_igealak.tsv`, `…_lxx_hid.tsv`, `…_lxx_g0012.tsv`, `…_teljesseg.tsv`, `…_teljesseg_blokkok.tsv`, `…_jelolt_sorok.tsv`, `…_felmeres.md` (+ `_kiserok/_szomszedok/_valasz.tsv`), `BIZONYITEK_TEREMT-001.md`, `…_nave_jeloltek.tsv`, `…_hatar_gepi.md`, `…_regi_adat.tsv`, `…_szakasz_cimke.tsv`, `…_proza_lefedettseg.md`, `F239_lekerdezesek.tsv`; valamint az átadó: `F239_atado_U1.md`. A régi tanulmányból csak célzott szakasz kell (a brief 3. pontja szerint a próza a táblákból készül).
