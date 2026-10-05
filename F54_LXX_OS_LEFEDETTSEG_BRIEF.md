---
feladat: 54
cim: Az LXX_OS lefedetlen versei — valódi görög hiány vagy versszámozási rés
kod: LXX_OS_LEFEDETTSEG
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: brief_kell
ad: az 503 Károli-vers mindegyikéről (az lxx-hid az LXX_OS-ből n=0-t ad, a régi LXX_kivonat adott) eldöntve és dokumentálva, hogy valódi görög hiány (helyes üres eredmény) vagy versszámozási rés; a rések pótolva az lxx_os_import.py besorolásában
kovetkezo: brief kell (a /befogad csonk-kitöltése)
fugg: [42]
olvas: ["konkordancia/LXX_OS/*.tsv", konkordancia/Karoli_versmegfeleltetes.tsv, naplok/FORRASKIVEZETES_M5_M7.md, naplok/FORRASKIVEZETES_M5_eltereslista.tsv]
ir: [eszkozok/lxx_os_import.py, "konkordancia/LXX_OS/*.tsv", konkordancia/LXX_OS/README.md]
---

# F54_LXX_OS_LEFEDETTSEG_BRIEF — csonk

*FELADATOK #54 · csonk-brief (F20 B3): nem végrehajtható, csak a feladat fejlécét hordozza. Forrás: a #42 (FORRASKIVEZETES, PR #176) nyitott tétele, `naplok/FORRASKIVEZETES_M5_M7.md` (f3).*

- **Mit ad, ha kész:** az 503 vers (Jób 78, Zsolt 66, Jer 59, Hós 57, Péld 50, 2Móz 46, 1Sám 34, Dán 30, Én 28, Józs 27, Ézs 24, Jón 2, 4Móz 1, 1Kir 1) kettéválasztva: valódi görög hiány (pl. az LXX rövidebb Jób- és Jeremiás-szövege) vagy versszámozási rés (pl. Hós fejezethatár); a rések pótolva, a hiányok explicit üres eredményként dokumentálva.
- **Következő lépés:** a brief megírása.

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
