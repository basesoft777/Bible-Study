# F20 B4 — a generált FELADATOK.md és a v1.3 eltéréslistája

*2026.09.30 · összevetés: a v1.3 (PR #77, `51f9291`) táblái ↔ `feladatok.py general` kimenete. Minden cella egyezik, kivéve az alábbiakat; a B2 munkalap 4. pontja szerint jóváhagyott eltérések.*

**Tábla-cellák** (a `naplok/` szkript `cmp.py` kimenete; a #6 sor a v1.3 táblájában nincs, a #20 új):

- **Állapot:** `⬜ nem futott` / `⬜` → `⬜ brief kell` (csonk-brief; jóváhagyott, B2 1/B). A #9 `⬜` változatlan.
- **Függ ettől:** lezárt függés „(kész)” jelöléssel; a #9 → #7 levezetett (`#7*`, `adat/forditasok.tsv`); a v1.3 zárójeles megjegyzései („terminológia, kiejtés”, „Macula-import”) elmaradnak.
- **Hol:** a #10, #11, #13 „brief csak chatben” / „—” helyén a csonk neve; #9: `F05_SZOTAR_BRIEF.md#2. menet`; #7: a „v3” kiegészítés a csonk törzsébe került.
- **#12 Megjegyzés:** „D29” → „SZOTAR-D29” (Q10).
- **#20:** új sor a „Folyamat és eszközök” táblában.

**Új generált blokkok:** „Folyamat és eszközök” (#20), „Naplózás” (üres).

**„Kész” lista:** generált, `- cím (#n, kód): összegzés` formátumban. A 14 napos ablak dátuma a `lezarva_osszegzes` első zárójeles `HH.NN` dátumából jön (a korábban kézzel vezetett tételek merge-napja); ha nincs ilyen, a `git log --first-parent -S` merge-commitja. *(A B4 első változatának „a git log a valódi dátumot adja” állítása téves volt: az átállás merge-e minden korábbi tétel `git log`-dátuma lenne; az ellenőri jelentés D26 pontja nyomán javítva.)* A korábbi 3 szám nélküli tétel (FJ 1. menet, TEREMT-002 1–2. lépés, Szótári brief v1.1) kézi „Korábbi, szám nélküli lezárt tételek” szakaszba került (Q4). A #1–#6, #14, #15 szövege a v1.3 „Kész” sorából származik, a zárójeles kód a régi szövegből.

**#12 „Hol”:** a generátor a `forras` mezőt írja ki, ha van; a #12 csonk `forras: TEREMT002_KUTATAS_BRIEF.md`, így a cella egyezik a v1.3-mal (`TEREMT002_KUTATAS_BRIEF.md`). A B2 munkalap 4.3 pontja „a csonk”-ot írt; a v1.3-egyezést tartottam meg.

**Felfedezett hiba, kezelve:** a #7 csonk `olvas` listájában szereplő `adat/kiejtes_kivetelek.tsv`-t a #9 S2.1-je írja, ezért a #7 → #9 függés (kör a #9 → #7-tel) adódott. Megoldás: `nem_fugg: [9]` a #7 fejlécében (a v1.3-ban nincs ilyen függés).

**Egyéb:** a „lezárva, még ágon” állapot jele `🔀` (a másik nagyító, U+1F50D az E2 szabályban „ellenőrizve” jelölés, a brief saját sorait is pirosra színezte). Idempotencia: a `general` kétszer futtatva „változatlan”.

**Az ellenőri jelentés (ELLENOR_F20, 1. kör) utáni javítások:**
- a `konkordancia/Karoli_versmegfeleltetes.tsv` proveniencia-komment sora változatlanul marad (a történeti proveniencia nem írható át; a `forras=KAROLI_KULCS_BRIEF.md` a régi név, a git-történetben megtalálható) — a K3 kivétele a `naplok/` mellett;
- a nyitó prompt szakaszokban (`KOZVETLEN_FUTTATAS`) a brief-nevek a régi alakban maradtak, mert a prompt szövege nem változhat (F01, F03, F04, F05, RENDER; a blokkok szövege bájtra azonos a régi fájlokéval);
- a #9 `ir` listája kiegészült (`adat/forditasok.tsv`, `eszkozok/kiejtes.py`), így a #7–#9 írás–írás ütközés látszik; a F20 `ir` a ténylegesen írt fájlokra bővült;
- a `feladatok.yml` gépi commitja `-F` fájlból megy.
