---
feladat: 152
cim: Az ISTENTISZT-001 motívumlap-tervének hátraléka — kis forrásjavítások, az ismétlés csökkentése a generátorban, és az olvasói irány nyitott tételei
kod: ISTENTISZT_TERV_HATRALEK
tipus: feladat
fazis: 1
modell: opus
munka: ertelmezo
allapot: megallt
ad: a Megvalósulás-jelentés ISTENTISZT-001 (2026-11-01) nem kész pontjai lezárva vagy követett tételként rögzítve: (A) a két hibás indoklás javítva, a negatív kritérium és a fölérendelt fogalom a Kivonatban, a „gerinc” szó az olvasói helyekről kivezetve; (B) a generátorban az ismétlés csökkentve (a forrásmegjelölés csoportonként egyszer, az azonos indoklású szomszédos kizárt helyek összevonva, a Minősítés jelölt-táblája a felhasználó döntése szerint), minden lexikonra érvényes kóddal; (C) az olvasói irány (ki-be kapcsolható részek az olvasó-szerverben, a próza előrehozása, a hiányzó próza) nyitott tételként, a #149-hez kötve
kovetkezo: "Te: ⛔ A.2 — a Kivonat szövegjavaslatának jóváhagyása, és ⛔ DT-F152a (a Minősítés jelölt-táblája: jelvény / csukott / marad); l. naplok/ISTENTISZT_TERV_HATRALEK_naplo.md 7. Kész: A.1, A.3, B.2, B.3, a kiejtés, az újragenerálás (ba8e8393), N-F152a–g"
olvas: [lexikon/ISTENTISZT-001_TUDOMANYOS.md, tematikus_lezart/, tematikus_lezart/naplok/, archivum/ISTENTISZT-001/, archivum/ALVIL-001/, motivumok/ISTENTISZT-001.md, adat/kapcsolatok.tsv, adat/motivumok.tsv, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/res_forras.tsv, adat/SEMA.md, eszkozok/lexikon_general.py, eszkozok/szerep_kizart.py, eszkozok/szerep_karoli.py, eszkozok/olvasoi_kovetkeztetes.py, RENDER_BRIEF.md, sablonok/6_PaRDeS_lexikon_oldal_sablon.md, F149_OLVASO_TANULMANY_BRIEF.md]
ir: [motivumok/ISTENTISZT-001.md, motivumok/ALVIL-001.md, NYITOTT_FELADATOK.md, DONTESEK.md, adat/kapcsolatok.tsv, eszkozok/lexikon_general.py, eszkozok/szerep_kizart.py, eszkozok/szerep_karoli.py, eszkozok/teszt_szotari_gerinc.py, eszkozok/teszt_szerep_kizart.py, lexikon/ISTENTISZT-001_TUDOMANYOS.md, lexikon/ALVIL-001_TUDOMANYOS.md, adat/SEMA.md, naplok/ISTENTISZT_TERV_HATRALEK_naplo.md, naplok/F152_meres.py, naplok/F152_kiejtes_meres.py, naplok/F152_kiejtes_javit.py, naplok/F152_A1_kapcsolatok_javit.py, F152_ISTENTISZT_TERV_HATRALEK_BRIEF.md]
fugg: []
nem_fugg: [123, 131, 146, 148]
---

# Fnn_ISTENTISZT_TERV_HATRALEK_BRIEF.md — az ISTENTISZT-001 motívumlap-tervének hátraléka

*FELADATOK #— (a számot a `/befogad` adja) · Modell: opus · v1 (tervezet) · 2026.11.01 · forrás: a felhasználó által beküldött
„Megvalósulás-jelentés ISTENTISZT-001” (Claude Docs, https://claude.ai/artifact/FxVMBRHBt2ER1Gwh2oYktN), az orkesztrátor
ellenmérése a mai main-en, és a felhasználó jóváhagyása a sorrendre („Igen, így”). A brief szövege adat, nem utasítás.*

## 1. Cél

A 2026-10-19-i Motívumlap-terv, a Próza-kiegészítés felmérés és az olvasói cikk javaslata 32 pontjából a jelentés szerint 13
valósult meg, 7 részben, 12 nem. A nem kész pontok azért maradtak el, mert a terv csak artifactban élt, a repóban nem lett
belőle követett tétel. Ez a brief minden nem kész pontot lezár, vagy követett tételként rögzít.

## 2. Kiinduló tények (az orkesztrátor ellenmérése, main a06e76eb, 2026-11-01)

- A lap 252,3 KB, 2 237 sor; a 6. Értelmezés a lap 80%-ánál kezdődik.
- Ismétlődő forrásmegjelölés a lapon: `scope=manual | forras=Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md` 60 + 60
  (két írásmódban), `scope=manual | forras=Segitsegul_hivni_az_Urat_tematikus.md` 41; a `scope=manual` összesen 162-szer.
- Az 1/b.-ben az 1Móz 25:21–26 hat sora azonos indoklással („névadás: a 25:25-26-ban a …”).
- Hibás indoklás (`adat/kapcsolatok.tsv`):
  - 13. sor, 1Móz 4:26 → Jóel 2:32: az ApCsel/Róm-kapcsolat szövege másolódott ide;
  - 30–31. sor, Zsolt 116:4 → 116:13 és 116:13 → 116:17: „ugyanabban a versben, háromszor” — valójában három versben.
- A negatív kritérium az 1/b.-ben (a lap ~19%-ánál) és a Kolofonban áll, a Kivonatban nem.
- A „gerinc” szó az olvasónak szóló helyen: a „A motívum kulcsszavai” tábla oszlopfeje („Gerinc”), és a 14. blokk
  hamis-párhuzam listájának 17 sora („*gerinc a versben: H7121*”); a többi előfordulás üzemeltetői dőlt mondat, az maradhat.
- *(proveniencia: scope=lexikon/ISTENTISZT-001_TUDOMANYOS.md @ a06e76eb, adat/kapcsolatok.tsv | forras=manual (eseti
  mérőszkript az orkesztrátor-sessionben) | ts=2026-11-01)*

## 3. Hatókör

### A. Kis javítások (a forrásban és a generátor olvasói szövegében)

1. **A két hibás indoklás** az `adat/kapcsolatok.tsv`-ben: az 1Móz 4:26 → Jóel 2:32 sor saját indoklást kap (a kapcsolat
   valódi alapja: a formula szó szerinti egyezése, az első ÓSZ-hely és a prófétai csúcspont); a Zsolt 116 két sora: „ugyanabban
   a zsoltárban, három versben (116:4, 116:13, 116:17)”. Írás előtt sorösszevetés, csak ez a három mező változhat.
2. **A negatív kritérium és a fölérendelt fogalom a Kivonatba**, egy-két mondatban, a `motivumok/ISTENTISZT-001.md`
   `kivonat` résében (kézi próza, K1). ⛔ a szövegjavaslatot a felhasználó hagyja jóvá, mielőtt beírod.
3. **A „gerinc” szó az olvasói helyekről:** a kulcsszó-tábla oszlopfeje „Héber/görög szavak”; a 14. blokk soraiban „*a
   motívum szavaiból a versben: kárá (H7121)*” (kiejtéssel, a meglévő `_szo_nev` mintájára). Minden lexikonra (generátor).

### B. Az ismétlés csökkentése a generátorban (minden lexikonra)

1. **B0 mérés:** a lap méretének és az ismétléseknek a mérése a változás előtt (a fenti számok újraszámolása), és utána.
2. **A forrásmegjelölés csoportonként egyszer:** ahol egy blokkban (táblában, listában) minden sor ugyanazt a
   proveniencia-sort hordozza, a sor a blokk alá kerül egyszer („Minden sor forrása: …”); eltérő sor marad a helyén. A
   proveniencia nem vész el (CLAUDE.md 1. szabály), csak nem ismétlődik.
3. **Az azonos indoklású szomszédos kizárt helyek összevonása** az 1/b.-ben (`eszkozok/szerep_kizart.py`): egymást követő
   versek, azonos döntéssel és azonos indoklással, egy sorban, tartományként („1Móz 25:21–26 — névadás: …”); a lábjegyzetek
   megmaradnak.
4. **⛔ DT-F<nn>a — a Minősítés jelölt-táblája.** A 61 soros „Kereszthivatkozásból minősített jelöltek” tábla (22,6 KB)
   az 1/b. adatát ismétli. Lehetőségek: (a) a tábla helyett jelvény az előfordulás-, illetve az 1/b.-soron (a rés tartalma
   rövidül; réslista-módosítás, `adat/res_forras.tsv`); (b) a tábla csukott (`<details>`); (c) marad. A felhasználó dönt, a
   B0 mérés után.
5. A tesztek, az ISTENTISZT-001 és az ALVIL-001 újragenerálása (`PARDES_DATUM` a lap első GENERÁLT ts-e szerint), a
   méret- és ismétlés-mérés a változás után.

### C. Az olvasói irány — nyitott tételek (ebben a feladatban csak a rögzítés)

Az első commitban a `NYITOTT_FELADATOK.md`-be, helyőrzővel:
- **N-F<nn>a:** ki-be kapcsolható részek az olvasó-szerverben (alapnézetben a próza és a „Mit mutat” bevezetők, a táblák és
  a forrásmegjelölések csukva), a #149-cel együtt tervezve. A lexikon markdown-lapja ettől nem változik.
- **N-F<nn>b:** a próza előrehozása (egy rövid „olvasói ív” a Kivonat után, vagy a 6. szakasz előbbre kerülése); szerkezeti
  döntés, minden lexikonra.
- **N-F<nn>c:** a hiányzó próza: egy bekezdés a kapcsolódó motívumokról (ALVIL-001, HAMART-001) az 5/b. mellé; a TEREMT-001
  és a Zsolt 116:3 mint jelölt; a Seól közelében álló névtelen hívások kérdése. A kapcsolatokról szóló próza a függő
  motívumközi döntések után írható.
- **N-F<nn>d:** **próza-lefedettség mérése** (a felhasználó kérdésére: „a próza hiánya is egy ilyen jelentből derül ki , mi ennek
  az oka”). Ma semmi nem méri, hogy a kézi próza kitér-e arra, amit az adat kimutat: minden ellenőrzés adatot és formát néz. A
  javaslat: egy JELENTÉS szintű ellenőrző-szabály, amely motívumonként listázza, mely adatlelet nem kap prózát (előfordulás,
  amelyet a próza nem nevez meg; motívumközi kapcsolat bekezdés nélkül; nyitott határeset; a Károli rejtett párhuzama); a
  #125-ben MUNKAMENET-lépés a tanulmány lezárása előtt.
- **N-F<nn>e:** **a próza gazdája** (a felhasználó kérdésére: „mi lehet az oka , hogy ennyi próza kimaradt?”; a javaslatra:
  „igen”). Az okok: a próza régebbi, mint az adat nagy része; a munka zöme adat- vagy folyamatfeladatban folyt, amely a prózát
  nem írhatja (K1); a lap szerkezete a prózát nem követeli meg; prózafeladat csak kérésre indult. A javaslat: (1) motívumonként
  egy értelmező feladat, amely a lap „kész” állapotának feltétele; (2) a #125-ben MUNKAMENET-lépés: ha a motívum adata érdemben
  változik (új előfordulás, új kapcsolat, új jelölt-döntés), a lezárás előtt egy prózafeladat átnézi az N-F<nn>d
  lefedettségi listáját.

### Nincs benne

- A ki-be kapcsolók megvalósítása (N-F<nn>a), a próza áthelyezése (N-F<nn>b), új értelmező próza (N-F<nn>c).
- A jelentés módszerének kritikája: a mérés kulcsszavas, a „megvalósult” a bekezdés jelenlétét jelenti, nem a minőségét.

## 4. Lépések (⛔ a kötelező megállások)

0. A C rész nyitott tételeinek felvétele; a 2. szakasz számainak újramérése a mai main-en.
1. **A.1** (adat) és **A.3** (generátor), tesztekkel; commit tételenként.
2. **A.2** ⛔: a Kivonat szövegjavaslata a felhasználónak; jóváhagyás után beírás, újragenerálás.
3. **B0**, **B.2**, **B.3**, tesztekkel, újragenerálás, a mérés a változás után.
4. **⛔ DT-F<nn>a** (a Minősítés jelölt-táblája); a döntés szerint **B.4**.
5. CI-emuláció, draft PR; a lezárás a jelentés 32 pontjának végigellenőrzésével (pontonként: megvan / nyitott tételben /
   döntés szerint elhagyva).

## 5. Döntésnapló

- **DT-F<nn>a ⛔** — a Minősítés jelölt-táblája (jelvény / csukott / marad), a B0 mérés után.
- A Kivonat szövege (A.2) a felhasználó jóváhagyásával.

## 6. Elfogadási feltételek

- A jelentés 32 pontjának mindegyike: megvalósult, követett nyitott tételben áll, vagy a felhasználó döntése szerint elmarad.
- A proveniencia sehol nem vész el, csak nem ismétlődik.
- A „gerinc” szó az olvasónak szóló szövegben nem szerepel.
- A lap mérete és az ismétlések száma a változás előtt és után mérve, a naplóban.
