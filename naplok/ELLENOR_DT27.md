# ELLENOR_DT27 — DT27 (`kapu` oszlop a terminológia-táblában), d4470df..bcb5e61

*A `fuggetlen-ellenor` jelentésének mentése az orkesztrátor által (az ellenőrnek nem volt fájlíró eszköze). Az ellenőr nem futtatta a teszteket, a `forditas_kapuk.py` kapufutását (a #2 construct próbafutását sem) és az `ellenoriz.py`-t: ezek NEM ELLENŐRIZHETŐ minősítést kaptak, kód- és adatolvasással igazolva.*

**Eredmény: ELTÉRÉS, 2 tétel.** Nem volt brief; a feladat a DONTESEK.md DT27 sora és a PR #102 leírása.

## ELTÉRÉSEK súlyosság szerint

1. **A `which see` (kapu=nem) részben kiveszi a kapu alól a kapu=igen `see → l.` (v1) sort** (`adat/terminologia.tsv:73`, `:9`; `eszkozok/forditas_kapuk.py:279-284`). A `_sajat_talalatok` a rövidebb kulcs azon előfordulásait, amelyek egy hosszabb kulcs találatán belül állnak, a hosszabb sorhoz rendeli, és a kapu értékét nem nézi. A „which see” belsejében álló `see` így a kapu=nem sorhoz tartozik, és a kapu=igen „see → l.” sort ott nem követeli meg. Ez a v1-es sor tényleges lazítása; sem a DT27, sem a napló nem említi, a DT27 indoklása kifejezetten „a kapu nem lazul”. Kiterjedés: `which see` a `Thayer_teljes.tsv`-ben 710, a `BDB_teljes_unabridged.tsv`-ben 6 sor; `adat/forditasok.tsv`-ben 0 (a meglévő fordításokat nem érinti, a jövőbeli Thayer-fordításokat igen). A többi új kapu=nem kulcsnál nem találtak ilyet. A `KapuOszlop.test_kapu_nem_hosszabb_kulcs_tovabbra_is_lefedi` ezt a viselkedést szándékosként rögzíti. *Lehetséges irány (a felhasználó dönt):* a kapu=nem sor ne vonja el a rövidebb kapu=igen sor találatait, vagy a mellékhatást rögzítse egy döntés.
2. **(enyhe) A DONTESEK.md DT26 „Alkalmazva” mezőjében elavult mondat maradt:** „A #1 „noun masculine”, #2 …, #20 felvétele a DT27-re vár” — a DT27 ✅, a mondat nem hivatkozik rá. A DT26 a (d) pont miatt helyesen 🟡 volt.

## OK (kódolvasás / mintavétel)

Változási kör: 4 commit (`F28.45:`), nincs váratlan fájl (DONTESEK 1/1, SEMA 6/0, terminologia 72/63, forditas_kapuk 10/0, teszt 39/0, naplo 12/0). Törölt sorok: a 63 = 1 fejléc + 62 adatsor, mind visszakerült; 58 sor csak `igen`-t kapott, 4 sor (id., ib., compare, מִן compare) `nem`-et + megjegyzés-fűzést, 9 új sor; angol/magyar/verzio mező változatlan. Kulcslefedettség: a 9 eset megvan; `kapu=nem` 13 sor (34, 35, 36, 56, 65–73). SEMA 2.15: a `kapu` mező és az üres = igen szabály leírva. Besorolás sorról sorra egyezik a jóváhagyott táblával. `kapus_sor()`: csak az explicit `nem` mentesít. Tesztek olvasva (5 eset). A prompt minden sort tartalmaz. `ellenoriz.py` nem változott, a 14. szabály független a `kapu`-tól. A `+` / `Nt.` / `absolute (használat)` megjegyzések indokolják a kapu=nem-et. Oszlopszám minden sorban 5 (71 adatsor). A #2 construct: a H7843 forrásban csupasz „construct” áll (BDB_teljes_unabridged.tsv:7327), a fordításban „constructus” „status” nélkül (forditasok.tsv:84) → kapu=igen mellett 1 sértés; a kapu=nem a megállapodás szerint. E12–E15: 0. A `futtat.py` (a diff fájljaira): E2–E8, E10–E16, E19 0; E9 2 JELENTÉS (`SEMA.md:236,237`, a diffen kívüli sorok).

## NEM ELLENŐRIZHETŐ az ellenőr által

A tesztek, a kapufutás és a #2 construct próbafutás, az `ellenoriz.py`; a napló „40 teljes sor kapu-eredménye változatlan” állítása; a CI-jelentéssel való egyezés.

## Megjegyzések (nem eltérés)

- A „v3” címke a 9 új sorral más halmazt jelöl, mint az F28.42 idején; a SEMA „a sorok tartalma nem változott” mondata csak az oszlop bevezetésére (angol/magyar/verzio) igaz. A verzió megtartását a felhasználó jóváhagyta.
- Sorszám-változás (E17): 62 → 71 adatsor (+14,5%); a DT3 küszöb eldöntetlen; a bontás a naplóban és a DT27-ben megvan.
