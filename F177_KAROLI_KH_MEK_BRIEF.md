---
feladat: 177
cim: A Károli-kereszthivatkozások javítása a MEK 00161 kiadással mint független második tanúval
kod: KAROLI_KH_MEK
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: megallt
ag: claude/karoli-kh-mek
ad: a KH-karantén feloldása; MEK-kivonat (konkordancia/Karoli_KH_MEK.tsv) licencsorral; összevető szkript; javított, háromszintű KH-tábla (megerősített / kiesik / jelölt); N-F156a és N-F156c lezárása
kovetkezo: "Te: [elteres_kor 2/2] /elteres 177 — újraellenőrzés függ: naplok/ELLENOR_F177_3.md"
munka: folyamat
olvas: [konkordancia/Karoli_kereszthivatkozasok.tsv, konkordancia/Karoli_kereszthivatkozasok_README.md, konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv, konkordancia/Karoli_1908.tsv, konkordancia/TSK_kereszthivatkozasok.tsv, konkordancia/Konyv_normalizalo_tabla.tsv, eszkozok/karoli_kh_epseg.py, eszkozok/karoli_kh_szuro.py, naplok/KAROLI_KH_EPSEG_jelentes.md, adat/SEMA.md]
ir: [konkordancia/Karoli_KH_MEK.tsv, konkordancia/Karoli_kereszthivatkozasok_gyanus.tsv, eszkozok/karoli_kh_gyanus_general.py, konkordancia/Karoli_KH_MEK_README.md, konkordancia/Karoli_KH_javitott.tsv, eszkozok/karoli_kh_mek.py, eszkozok/teszt_karoli_kh_mek.py, eszkozok/karoli_kh_szuro.py, adat/datasetek.tsv, adat/licencek.tsv, adat/SEMA.md, naplok/F177_jelentes.md]
fugg: [176]
nem_fugg: [38]
---

# F177_KAROLI_KH_MEK_BRIEF.md — A Károli-kereszthivatkozások javítása a MEK-kel

*FELADATOK #177 · Modell: sonnet · v1 · 2026.11.08*

*Befogadva a felhasználó jóváhagyásával („Igen, vedd fel”, „akkor csak kh”, 2026-11-08). Előzmény: N-F156a (a `Karoli_kereszthivatkozasok.tsv` másolt KH-listái), N-F156c (a `kh_index` szűrője), DT558 (karantén, „amíg nincs licenc-tiszta, helyes forrás”). A Nave-alapú pótlás **nem** része (a felhasználó: „akkor csak kh”; a Nave tematikus kapcsolat, nem a Károli-margó, és a vers→vers kapcsolatra a TSK a forrás).*

## 1. Cél

A Károli-margó kereszthivatkozásait (KH) egy második, független tanúval ellenőrizni és javítani. A mai tábla (HunKar OSIS ← szentiras.hu KG) ismert hibája, hogy sok vers egy másik vers KH-listáját hordozza (N-F156a: 5 078 gyanús vers, karanténban). A MEK 00161 kiadás (*Szent Biblia*, Károli; MEK, 2002-10-01) versenként, a vers alatt adja a KH-t, a HunKar-tól függetlenül.

**Az orkesztrátor próbamérése** (scratchpad, 2026-11-08; nem bizonyíték, a végrehajtó újramér):

| | vers |
|---|---|
| a két forrás egyezik | 11 342 (+260 a gyanúsak közül) |
| gyanús, és a MEK-ben nincs KH | 4 769 / 5 078 |
| nem gyanús, és a MEK-ben nincs KH | 1 924 (szúrópróba: elcsúszott listák, pl. ApCsel 10:32, Zsid 8:13, Eszt 9:6) |
| eltér | 1 446 (+49) |
| csak a MEK-ben | 74 |

A MEK-nek **saját elírásai** vannak (pl. 2Móz 6:20 → „2Móz 26,59”, helyesen 4Móz 26,59; 5Móz 7:15 → „1Móz 15,26”; 5Móz 21:23 → „Gal 2,13”, helyesen Gal 3,13), ezért vakon nem vehető át.

## 2. Forrás és licenc

- A nyers fájlok a felhasználó gépén: `E:\Letöltések\00161.rtf` (és `.pdf`, `.epub`, `.prc` — ugyanaz a kiadás; az RTF elég). **A nyers fájl nem kerül a repóba**; a repóba a kivonat (`Karoli_KH_MEK.tsv`) és a konverziós szkript kerül. A forrás-URL: https://mek.oszk.hu/00100/00161/. A fájl SHA-256-ja a README-be.
- A fájlban nincs impresszum; a szöveg helyesírása az 1908-as revízióé. A kiadás azonosítását (melyik nyomtatott kiadás) a README rögzítse, ha kideríthető; ha nem, „nem azonosított”.
- **⛔ Licenc.** A MEK szerzői jogi oldala (https://www.mek.oszk.hu/html/allando/copyright.htm) személyes, nem kereskedelmi másolást enged, forrásmegjelöléssel; a szöveg a Szjt. IV/B. fejezete szerinti általános szöveg, nem biztos, hogy erre a közkincs dokumentumra vonatkozik. A felhasználó elve (2026-11-08, a Sefariánál): közkincs tartalomnál a szerzői jog az irányadó. **A MEK-re ezt a felhasználónak külön meg kell erősítenie**, mielőtt a MEK-ből származó bármi a kimenetbe (lap, nyílt mag) kerül. Addig a `licencek.tsv` sora `kereskedelmi=feltetelesen`, a MEK belső tanú. A javított tábla (3. pont) a saját döntésünk; a MEK szövege a nyílt magba nem kerül.

## 3. Tételek

### F177.0 — Modell-ellenőrzés, függés
A CLAUDE.md szerinti modell-ellenőrzés (kért: `sonnet`). A #176 (`fugg`) a `licencek.tsv`-t, a `datasetek.tsv`-t és a `SEMA.md`-t is írja: ha a munkája még nincs a `main`-ben, ⛔.

### F177.1 — MEK-kivonat
- `eszkozok/karoli_kh_mek.py kivonat <rtf>`: RTF-dekódolás (a `\'xx` cp1250, `\uN`), a könyvpárosítás a MEK saját tartalomjegyzéke szerint (66 cím, kánoni sorrend, a `Konyv_normalizalo_tabla.tsv` STEPBible-kódjaira), fejezet: `N.` sor, vers: `N. szöveg` sor (ha a vers 1-re ugrik fejezetsor nélkül, új fejezet), a KH-sor a vers után.
- A MEK a tartományt **két végponttal** sorolja (a két végpont két külön hivatkozásként áll, pl. 1Móz 2:4 és 1Móz 2:5, ami az 1Móz 2:4-5 tartomány; a MEK szó szerinti alakja a kivonat `mek_alak` oszlopába kerül) — ezt a kivonat megőrzi, és az összevetés így kezeli.
- Könyv-aliasok a két forrás között (próbamérésből: Máté/Mát, Hag/Agge, Sir/Siral, Énekek/Én, Nehem/Neh) — a táblában rögzítve, nem kódba szórva.
- Kimenet: `konkordancia/Karoli_KH_MEK.tsv` (oszlopok: `igehely` STEPBible-alakban, `kapcsolodo` STEPBible-alakban, `mek_alak` szó szerint, `proveniencia`). TSV `split('\t')` / `'\t'.join()`, `csv` nem.

### F177.2 — Versellenőrzés és összevetés
- Minden hivatkozott vers létezése a `Karoli_1908.tsv`-ben (a MEK-elírások és a HunKar-hibák itt buknak ki); a nem létező vers `hibas_hivatkozas` jelöléssel marad, nem javítod találgatással.
- Versenkénti összevetés a `Karoli_kereszthivatkozasok.tsv`-vel; TSK-támogatás (`TSK_kereszthivatkozasok.tsv`, a `karoli_kh_epseg.py` ±3 vers szabálya) az eltérő és az egyoldalú sorokra.

### F177.3 — Javított, háromszintű tábla
`konkordancia/Karoli_KH_javitott.tsv` (oszlopok: `igehely`, `kapcsolodo`, `szint`, `forras`, `indok`, `proveniencia`):
- **`megerositett`**: a két forrás egyezik (a gyanús versen is: a MEK megerősíti, a karantén alól kikerül);
- **`kiesik`**: csak a HunKar-ban van, a MEK-ben azon a versen nincs KH (gyanús és nem gyanús egyaránt) — a sor megmarad a táblában `kiesik` szinttel, nem törlődik;
- **`jelolt`**: eltérő lista, vagy csak a MEK-ben szereplő hivatkozás; versellenőrzés + TSK-támogatás jelölve; **döntés nélkül** (CLAUDE.md 2. szabály).
- A `karoli_kh_szuro.py` a javított táblát használja: a `megerositett` szint jut a lapra, a `kiesik` nem, a `jelolt` nem (a jelöltlistán marad).

### F177.4 — Lezárás és jelentés
- N-F156a és N-F156c lezárása a `NYITOTT_FELADATOK.md`-ben (meglévő sor szerkesztése, a mért számokkal); a DT558 karanténja a `kiesik` szinttel váltódik ki — az ehhez szükséges döntés helyőrzővel a `dontesek/uj/<ágnév>.md`-be (DT-F177a).
- **A karantén feloldása (a felhasználó, 2026-11-08: „utána a karantént fel kell oldani”):** a javított tábla elkészülte után a karantén (`Karoli_kereszthivatkozasok_gyanus.tsv` és a `karoli_kh_szuro.py` mai kizárása) megszűnik: a `megerositett` sorok — a korábban gyanúsak közül a MEK által megerősítettek is — visszakerülnek a KH-indexbe, a `kiesik` sorok végleg kimaradnak. A `Karoli_kereszthivatkozasok_gyanus.tsv` archiválva marad (ARCHÍV fejléc, nem törlés), a generátora (`karoli_kh_gyanus_general.py`) a javított táblára mutató megjegyzést kap. A lapokon a változás a lapszerkezeti generátor-körben jelenik meg.
- `naplok/F177_jelentes.md`: a mérések, a MEK-elírások listája, a kiadás-azonosítás eredménye, a licenc-állapot.
- `python eszkozok/ellenoriz.py`, a meglévő tesztek, `teszt_karoli_kh_mek.py` zöld; független ellenőr; draft PR. Merge a felhasználóé.

## 4. Kizárt
- a lapok újragenerálása és a `lexikon_general.py` minden olyan módosítása, amely a lapot változtatná — a lapszerkezeti generátor-körben;
- Nave-alapú kereszthivatkozás-pótlás;
- a `jelolt` sorok eldöntése (külön, a felhasználóé vagy egy későbbi menet).

## 5. Megállási pontok (⛔)
1. A kért modell eltér, vagy a #176 munkája nincs a `main`-ben (F177.0).
2. A MEK licence a kimenet szempontjából a felhasználó megerősítésére vár (2. pont) — a munka belső tanúként folytatható, a kimenetbe semmi nem kerül.
3. A kiadás nem azonosítható, és a KH-margó a próbamérésnél lényegesen nagyobb mértékben tér el (pl. az egyezés 60% alatti a nem gyanús verseken): megállás, jelentés.
4. Tartalmi döntés (pl. egy vers KH-jának kézi javítása): tétel a `dontesek/uj/`-ba, megállás.
