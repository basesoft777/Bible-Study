---
feladat: 174
cim: A modernizált Károli Strong-vetítése
kod: KAROLI_MODERN_STRONG
tipus: feladat
fazis: folyamat
modell: opus
munka: adat
allapot: nem_indult
ad: a Károli–Strong párok determinisztikus, modell nélküli átvetítése a régies szövegről a modernizáltra, a helyesírás-token és a páros-fájl közös kulcsán; egyetlen régi pár sem vész el, új nem keletkezik
kovetkezo: "Csonk, indítás előtt kidolgozandó: a /befogad után a brief kidolgozása, majd /kovetkezo; a brief rögzíti a #137-hez való viszonyt és a DT305-tel való összhangot"
olvas: [adat/karoli_modern/, adat/karoli_strong/, adat/SEMA.md, F137_KAROLI_MODERN_DB_BRIEF.md]
ir: [adat/karoli_modern/, eszkozok/karoli_modern/, naplok/KAROLI_MODERN_STRONG_meres.md]
fugg: [172, 96]
---

# F174_KAROLI_MODERN_STRONG_BRIEF — csonk

*FELADATOK #174 · csonk-brief · Modell: opus · v1 · 2026.11.05 · **csonk, indítás előtt kidolgozandó**; a felhasználó jóváhagyása (2026-11-05): „a modernizált károli strongozását vegyük fel jövőbeni feladatnak / most csak brief csonk”.*

## 1. Cél

A Strong-párok átvetítése a régies szövegről a modernizáltra az `adat/karoli_modern/helyesiras_tokenek.tsv` (igehely, sorszám, alak_1908, alak_modern, kieso) és az `adat/karoli_strong/parok_*.tsv` (igehely, hu_sorszam) közös kulcsán, determinisztikusan, modell nélkül. Kezelendő: egy-egy; összevonás (két régi szó → egy modern: mindkét Strong); kieső szó (jelölve, nem vész el); igealak-modernizálás (egy-egy). Licenc: a párosítás nyílt adat (DT-F172b), a megjelenítés fizetős lehet.

## 2. Nyitott kérdések (a kidolgozás dönti)

- **A #137-hez (KAROLI_MODERN_DB) való viszony [javaslat]:** a #174 külön tétel, és a #137 keresési Strong-kötésének előfeltétele; a brief rögzíti, hogy a #137 DT314 (kieső token → gazdaszó Strongja) ebből vagy közvetlenül a #22-ből táplálkozik-e.
- **Összhang a DT305-tel:** a DT305 szerint a modernizált réteg nem tárol Strongot, join-nal éri el. A vetítés eredménye ezért külön származtatott tábla vagy nézet legyen, nem a modern réteg oszlopa; a döntés új helyőrzős tétel a kidolgozáskor.
- Függés: a #172 (a párosítás pontossága) és a #96 (lezárva).

## 3. Mi a kész

- [ ] Minden régi pár átvetítve; egy sem vész el, új nem keletkezik (kapu: darabszám- és kulcs-összevetés).
- [ ] Az összevonás, a kieső szó és az igealak-modernizálás esete tesztelve.
- [ ] A kimenet származtatott, proveniencia-jelölt, a `bizonyossag` öröklődik.
- [ ] A #137-hez való viszony és a DT305-összhang a briefben rögzítve.
