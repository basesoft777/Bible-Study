# PaRDeS Strong-annotáció — LibreOffice Writer bővítmény

Ez a bővítmény a [eszkozok/inline_strong_megjelenito.py](../eszkozok/inline_strong_megjelenito.py)
parancssoros referenciaszkript logikáját teszi elérhetővé közvetlenül
LibreOffice Writerben: egy igehely (pl. `1Móz 1:1` vagy `Gen.1.1`) Károli
1908-as szövegét szúrja be a dokumentumba úgy, hogy a
`konkordancia/Karoli_Strong_kivonat.tsv` join-táblában már feldolgozott
szavak után beszúrja a Strong-számot szögletes zárójelben.

## Forrásstruktúra

```
bovitmenyek/
  build_oxt.py                      — csomagoló szkript (lásd lent)
  pardes_strong_annotator/          — a bővítmény forrása (nem tömörítve)
    META-INF/manifest.xml
    description.xml
    description/description_hu.txt, description_en.txt
    registration/license_hu.txt, license_en.txt   — PLACEHOLDER, nincs
                                                      még licencdöntés
    Addons.xcu                      — menüregisztráció (Eszközök > Kiegészítők)
    Scripts/python/pardes_strong.py — a teljes UNO-logika (egyetlen modul)
    data/                           — build_oxt.py generálja, NEM verziózott
```

## Miért csomagolja be a bővítmény a TSV-ket, ahelyett hogy a repóra
## hivatkozna relatív úton?

Egy telepített LibreOffice-bővítmény nem tudhatja előre, hogy a
felhasználó gépén hol van (vagy hogy egyáltalán megvan-e) ez a Git-repó —
a bővítményt bárki telepítheti anélkül, hogy a `Bible-Study` mappát
lekérte volna, vagy másik gépre másolva teljesen más útvonalon van. Az
`.oxt` telepítési helye a `PackageInformationProvider` UNO-szolgáltatással
mindig megbízhatóan lekérdezhető, egy külső, felhasználó által megadott
repó-útvonal viszont törékeny lenne (konfigurációt igényelne, és
elromlana, ha a repó elköltözik). Ezért a `build_oxt.py` **másolatot**
készít a 3 szükséges TSV-ről (`Karoli_1908.tsv`,
`Karoli_Strong_kivonat.tsv`, `Konyv_normalizalo_tabla.tsv`) a bővítmény
`data/` almappájába, és ez kerül be a `.oxt`-be. A `data/` mappa és a
generált `.oxt` a `.gitignore`-ban van, hogy ne duplázzuk a ~4,4 MB-os
`Karoli_1908.tsv`-t a repóban.

**Következmény:** ha a `konkordancia/` TSV-k tartalma módosul (pl. új
join-tábla sorok kerülnek be), a bővítményt **újra kell csomagolni és
újratelepíteni**, hogy a változás megjelenjen benne — a bővítmény nem
olvassa élőben a repót.

## Csomagolás (.oxt előállítása)

```bash
python bovitmenyek/build_oxt.py
```

Ez létrehozza (felülírva, ha már létezik) a
`bovitmenyek/pardes_strong_annotator.oxt` fájlt. A szkript két lépést
végez: bemásolja a szükséges TSV-ket a `data/` almappába, majd ZIP-eli az
egész `pardes_strong_annotator/` mappát `.oxt` kiterjesztéssel.

Futtasd újra ezt a szkriptet minden alkalommal, amikor a `konkordancia/`
TSV-k változnak, és a bővítményt frissíteni akarod.

## Telepítés

1. LibreOffice Writer → **Eszközök > Bővítménykezelő…**
2. **Hozzáadás…**, majd válaszd ki a `pardes_strong_annotator.oxt` fájlt.
3. Fogadd el a licenc-placeholder szöveget (a mező még nincs kitöltve
   véglegesen — lásd `registration/license_hu.txt`).
4. Indítsd újra a LibreOffice-t, ha kéri.

Frissítéskor (új `.oxt` build után): **Bővítménykezelő** → jelöld ki a
régi verziót → **Eltávolítás** → majd **Hozzáadás…** az újjal. (A
Bővítménykezelő ugyanazon azonosítóval — `org.pardes.strong_annotator` —
felismeri, ha frissítés történik, és felajánlja a csere lehetőségét is,
ha közvetlenül az új fájlt adod hozzá.)

## Használat

1. Nyiss meg (vagy hozz létre) egy Writer-dokumentumot.
2. Opcionálisan jelölj ki egy igehely-hivatkozást a szövegben (pl.
   `1Móz 1:1` vagy `Gen.1.1`) — ez előtölti a párbeszédablak mezőjét.
3. **Eszközök > Kiegészítők > PaRDeS Strong-annotáció…**
4. A megnyíló ablakban:
   - add meg (vagy hagyd jóvá az előtöltött) igehelyet, VAGY
   - pipáld be a "Teljes fejezet beszúrása" opciót, és add meg a könyv
     STEPBible-rövidítését (pl. `Gen`) és a fejezetszámot.
5. **OK** — a bővítmény a kijelölt szöveget lecseréli (ha volt kijelölés),
   vagy a kurzorpozícióba szúrja be az annotált Károli-vers(ek) szövegét.

Ha az igehelyhez nincs Károli-szöveg, vagy fejezet-módban egyáltalán nem
található vers, a bővítmény felugró figyelmeztetést/hibaüzenetet ad a
dokumentumba írás helyett (nem konzolra ír, mint a parancssoros
referenciaszkript).

## Függőségek

Nincs pip-csomag igény — csak a Python standard könyvtár és a
LibreOffice saját `uno`/`unohelper` modulja (ezeket a LibreOffice
telepítése biztosítja a beépített Python-futtatókörnyezetében).

## Tesztelés

Ez a forráscsomag és a `build_oxt.py` nem lett futtatható LibreOffice
hiányában telepítve/tesztelve ténylegesen Writerben — a build szkript
lefutott és érvényes `.oxt` ZIP-et állít elő (ellenőrizve), de a
UNO-dialógus és a menüintegráció tényleges viselkedését telepítés után
kell ellenőrizni.
