---
feladat: 139
cim: A szó-lap fejlécének átrendezése — a címsorban a szótő és a magyar átírás, alatta kiemelve a magyar alapjelentés szófaj nélkül, az alcímben a Strong-szám és a szófaj (SZOLAP_FEJLEC)
kod: SZOLAP_FEJLEC
tipus: feladat
fazis: 1
modell: opus
allapot: nem_indult
ad: a héber szó-lap fejléce három sorban, egységes rendben: címsor = héber szótő + magyar átírás (a döntés szerinti forrásból, gépi esetben jelölve); kiemelt sor = az alapjelentés a szófaji előtag nélkül; alcím = Strong-szám · szófaj (magyarul); a STEP/Strong-szótár angol szótagolású kiejtése (pl. `cha.Rum`) a fejlécből kikerül
kovetkezo: "A /kovetkezo a #134 zárása után indíthatja (M0 ⛔: mérés és terv; ⛔ DT-F139a: a héber átírás forrása)"
munka: folyamat
olvas: [F134_OLVASO_ALAPNEZET_BRIEF.md, F138_ALAPJELENTES_JAVITAS_BRIEF.md, F05_SZOTAR_BRIEF.md, adat/kiejtes_kivetelek.tsv, adat/kiejtes_heber_kivetelek.tsv, eszkozok/heber_kiejtes_jeloltek.py, konkordancia/OSHL_lexikalis_index.tsv, konkordancia/Strong_szotar.tsv]
ir: [eszkozok/olvaso_szerver/sablonok/_szo_panel.html, eszkozok/olvaso_szerver/statikus/, eszkozok/olvaso_szerver/oldalak.py, eszkozok/olvaso_szerver/lekerdezesek.py, eszkozok/olvaso_szerver/blokkok.py, eszkozok/olvaso_szerver/teszt_olvaso_szerver.py, eszkozok/olvaso_szerver/teszt_szolap_fejlec.py, eszkozok/heber_atiras_general.py, adat/kiejtes_heber_atiras.tsv, adat/kiejtes_heber_jeloltszabalyok.tsv]
fugg: [134, 140]
---

# F139_SZOLAP_FEJLEC_BRIEF.md — A szó-lap fejlécének átrendezése

*FELADATOK #139 · Modell: opus · v1 · 2026.10.25*

## 1. Cél

A felhasználó kérése (2026-10-25, chat): a szó-lap tetején az olvasó elsőként a szó **magyar jelentését** lássa, és a kiejtés magyar átírásban álljon. A megbeszélés eredménye: a jelentés nem a címsorba kerül, hanem közvetlenül alá, kiemelve. A címsor azonosít (szótő, átírás), a jelentés értelmez. Ez a kettő külön sor marad, mert a jelentés ma gépi kinyerés eredménye, és a 7a adag 85 szócikkéből 13-nál hibás (mérés: `scope=adat/forditasok.tsv, 7a adag 85 Strong + eszkozok/olvaso_szerver/bdb_szelet.py | forras=helyi-futtatas | ts=2026-10-25`, a #138 tárgya).

A szó-lap fejléce ma (`sablonok/_szo_panel.html`, `oldalak.py` `szo_torzs`), héber szónál:

1. `h2.szocim`: `H2763 חָרַם` — Strong-szám és szótő;
2. `p.szoalcim`: `cha.Rum · ige` — a `Strong_szotar.tsv` `Kiejtés` oszlopa (angol szótagolású STEP-átírás) és `Szófaj` oszlopa (magyar);
3. `p.alapjel`: `Alapjelentés ige Hiph`il: átok alá vetni, szentelni, kiirtani` — `blokkok.alapjelentes` (DT-F76f).

Két mért hiba ebben:

- **A szófaj kétszer áll.** A `bdb_szelet.alap_jelentes` a rövid, tiszta első sort változatlanul adja vissza, a szófaji előtaggal együtt („főnév nőnemű: szépség, dicsőség”); a 7a adagban a 85-ből 48 ilyen. Az alcím a szófajt már kiírja.
- **A kiejtés nem magyar.** A `cha.Rum` alak a STEP-rendszeré, a magyar olvasónak nem olvasható.

A cél-fejléc:

```
חָרַם  [magyar átírás]                       ← címsor (h2)
átok alá vetni, szentelni, kiirtani          ← kiemelt alapjelentés, szófaji előtag nélkül
H2763 · ige · Hif'íl                          ← alcím (Strong-szám, szófaj, ha a forrás adja: binyan)
```

## 2. Hatókör

**Benne van:**

- a héber szó-lap fejlécének (`_szo_panel.html` és a `szo_torzs` által átadott mezők) átrendezése a fenti sorrendre, a kis és a nagy képernyős nézetben (a #134 elrendezésén belül);
- a kiemelt jelentés-sor forrás-sorrendje a DT302 (a) szerint (`blokkok.alapjelentes`): jóváhagyott kézi jelentés > a #140 magyar glosszája (`adat/glosszak_heber_hu.tsv`, a pardes.db-ben azonos nevű tábla) > a BDB-kivágás; ha egyik sincs, a sor jelölten üres („magyar jelentés még nincs”), angol szöveg nem kerül a helyére;
- a szófaji előtag (és a vezető nyelvtani címke, pl. `ige Hiph`il:`) leválasztása a megjelenített alapjelentésről **a megjelenítési rétegben**; ami leválik, az alcímbe kerülhet, ha a `Szófaj` mezőnél többet mond (binyan);
- a magyar átírás a címsorban, a DT-F139a döntés szerinti forrásból; gépi átírás esetén látható jelöléssel (pl. `title` és jelölő osztály);
- az angol szótagolású `Kiejtés` kivétele a fejlécből (a Strong-szótár blokkjában, lejjebb, megmaradhat);
- tesztek: a fejléc mezőinek sorrendje és tartalma legalább 10 Strongon (köztük a 7a adag hibás soraiból: H6659, H4948, H1945; ige binyannal: H2763; tulajdonnév: H7346), és hogy a szófaj nem ismétlődik.

**Nincs benne:**

- a BDB-kivágás (`bdb_szelet.py`) javítása és a „LORD” a forrásfájlokban: a #138; ez a feladat a `bdb_szelet.py`-t nem írja;
- a magyar glosszák előállítása: a #140.
- a görög szó-lap fejléce (a TBESG-ág): külön mérés után, ha a felhasználó kéri;
- a H1581-es forráshiba (a szomszédos גַּמְלִיאֵל szócikk a H1581 szakaszai elején): külön nyitott tétel.

## 3. Lépések

**M0 — mérés és terv.** ⛔

1. A #134 lezárt állapotán a szó-lap fejlécének tényleges szerkezete (sablon, CSS-osztályok, kis és nagy képernyő).
2. A magyar átírás lefedettsége: hány héber Strongnál van jóváhagyott átírás a `adat/kiejtes_kivetelek.tsv`-ben (2026-10-25: 26 `heber` sor), és hánynál adna a jelölt-gépezet (`eszkozok/heber_kiejtes_jeloltek.py`, az OSHL `atiras` mezője + `kiejtes_heber_jeloltszabalyok.tsv` + `kiejtes_heber_kivetelek.tsv`) átírást, ha a hatókörét a 26 lemmáról minden héber Strongra kiterjesztjük. Vak mintán (legalább 50 Strong, vegyesen ige, főnév, tulajdonnév) a gépi átírás hibaaránya kézi ellenőrzéssel.
3. A szófaji előtag leválasztásának szabálya a mai alapjelentés-kimeneten (a 674+ kész BDB-soron): hány sornál válik le előtag, és hány sornál marad a leválasztás után üres vagy csonka szöveg.
4. ⛔ **DT-F139a — a héber átírás forrása a címsorban.** Az F05 S3 ma kimondja: „Héber: a render nem generál; lemma-kiejtés csak a kézi `adat/kiejtes_kivetelek.tsv`-ből.” A választás:
   - (a) csak a jóváhagyott kivételtábla: a legtöbb szónál nincs átírás a címsorban (a mai 26 lemmán kívül);
   - (b) gépi átírás minden héber Strongra a jelölt-gépezettel, generált adattáblába (`adat/kiejtes_heber_atiras.tsv`, provenienciával, `allapot=gepi`), a fejlécben „gépi átírás” jelöléssel; a jóváhagyott kivétel elsőbbséget kap. Ez az F05 S3 módosítása, DONTESEK-tétel kell;
   - (c) mint (b), de a gépi átírás csak a vak minta mért hibaaránya alatti küszöb esetén élesedik, addig (a).

   *Előmérés a befogadáskor (`scope=konkordancia/Strong_szotar.tsv H-sorai, a 7a adag 85 Strongja, adat/kiejtes_kivetelek.tsv heber sorai + eszkozok/heber_kiejtes_jeloltek.py (spirantize, atir, kiejtes_heber_kivetelek) | forras=helyi-futtatas | ts=2026-10-25`):* a gépezet a 8 718 héber Strongból **8 673-ra (99,5%)** ad átírást (a maradék 45-nek nincs OSHL-sora). A jóváhagyott 26 lemmából 13-at lehetett lemma szerint az OSHL-hez kötni, és mind a **13 egyezik**; a többi 13 a niqqud-sorrend vagy a nem lemma-alakú kulcs (pl. `qa.ra`) miatt nem kötődött, ezt az M0 normalizálással méri újra (az F05 S1.7 a 26-ból 26 egyezést rögzített). A 85-ös mintán a kimenet zöme olvasható magyar átírás (H2763 `cháram`, H8597 `tifárá`, H7346 `rechavám`, H0530 `emúná`). Látható hibaosztályok, amelyeket az M0 vak mintája mér: (1) az OSHL első sora nem a szótő (H7442 `rún` a `ránan` helyett, H6887 `cúr` a `cárar` helyett — gemináló igék); (2) a vav átírása `w` (H7723 `sáwe`, H6172 `erwá`, H5766 `áwel`), szabálytábla-kérdés; (3) a `ś` (sin) megtartása (H8040 `śemól`). A befogadó javaslata ezért a **(b)**: a gépezet determinisztikus (a pontozott lemmából szabállyal számol, nem becsül), és a fenti hibaosztályok a szabálytáblában és a szótő-választásban javíthatók; a jelölés („gépi átírás”) a jóváhagyásig marad.

   A terv (M0 1–3 eredménye + a javasolt választás) a `naplok/SZOLAP_FEJLEC_terv.md`-be; megállás a felhasználó döntéséig.

**M1 — az átírás-tábla** (csak a DT-F139a (b) vagy (c) választása esetén). A `eszkozok/heber_atiras_general.py` a jelölt-gépezet szabályaival generálja az `adat/kiejtes_heber_atiras.tsv`-t (séma a `adat/SEMA.md`-be, a 2.18 mellé); a szabálytábla (`adat/kiejtes_heber_jeloltszabalyok.tsv`) és a szótő-választás a vak minta hibaosztályai szerint javul; ⛔ a pardes.db-be töltés (`eszkozok/sqlite_epit.py`) nincs az `ir`-ben (a #122, #135, #137 ne várjon erre): fejléc-bővítéssel vagy külön feladatként, a felhasználó döntésével; a jóváhagyott `kiejtes_kivetelek.tsv` sor elsőbbséget kap. A generátor determinisztikus, kétszeri futása bájtazonos.

**M2 — a fejléc.** Sablon, `szo_torzs` mezők, CSS, a szófaji előtag leválasztása a megjelenítési rétegben. A `teszt_szolap_fejlec.py` a 2. pont tesztjeivel.

**M3 — mérés és zárás.** A tesztek (`python eszkozok/teszt_futtat.py`) zöldek; képernyőkép 375 és 1280 px-en három szóról (ige binyannal, főnév, tulajdonnév) a `naplok/SZOLAP_FEJLEC_zaras.md`-be. ⛔ a felhasználó megnézi a képeket.

## 4. Elfogadási feltételek

- A héber szó-lap fejléce a cél-sorrendben áll; a szófaj sehol nem ismétlődik a fejlécben.
- A címsorban a magyar átírás a DT-F139a szerint áll; gépi átírásnál a jelölés látható; az angol szótagolású kiejtés a fejlécben nem szerepel.
- A kiemelt jelentés-sor a DT302 (a) sorrendjét követi (kézi > TBESH-glossza fordítása > BDB-kivágás); angol szöveg a kiemelt sorban nem áll, a hiány jelölt; a `bdb_szelet.py` változatlan.
- `python eszkozok/teszt_futtat.py` zöld; az új fejléc-teszt legalább 10 Stronggal.
- (M1 esetén) az `adat/kiejtes_heber_atiras.tsv` minden sora provenienciával; a generátor kétszeri futása bájtazonos.

## 5. Döntésnapló

- **DT302** (🟢, 2026-10-25, a felhasználó): a kiemelt jelentés forrása és sorrendje (a), a #139 függése a #140-től (d); átvezetve ebbe a briefbe a befogadáskor.
- **DT-F139a** (nyitott, M0 ⛔): a héber átírás forrása a címsorban, (a)/(b)/(c), l. M0 4.
- Előzmény (2026-10-25, chat, `manual`): a felhasználó jóváhagyta, hogy a jelentés ne a címsorban, hanem közvetlenül alatta, kiemelve álljon, és hogy a megjelenítés a #138-tól külön feladat legyen.
