# F16 zárójelentés (FELADATOK #16; ág: `claude/bsb-import`)

**Elkészült:** BSB (CC0, `base/display/`, commit a4a2c05) importja a 30 küszöböt elérő ÓSZ-könyvre: `konkordancia/BSB_Strongs.tsv` (224 807 sor); lefedettségi mérés mind a 66 könyvre (`naplok/F16_bsb_lefedettseg.tsv`, 1Móz 98,83% = F06); verseltolás-diagnózis; dataset-regisztráció (`datasetek.tsv`, README, SEMA 2.6); szerepmátrix-bejegyzés; N30 lezárva.

**Eredmény:** 30 könyv ELÉRI (mind ÓSZ), 36 NEM_ÉRI_EL (9 ÓSZ + 27 ÚSZ). Az ÚSZ-mérés az F06-ban nem használt kiterjesztés (forrás: TAGNT), kimondva.

**Leletek:** Zak 12:1 és 116 zsoltárvers hiányzik a BSB `display` állományából (forráshiány); a névelő elided span-ként címkézett; 27 043 sor üres „Angol szó”-val (README-ben rögzítve).

**Nyitott (DONTESEK DT-F16, 🟡, javaslat-tétel):** a küszöb alatti könyvek kezelése (számozás-esetek külön feladat, verstérképpel; ÚSZ külön feladat N37 után), a hiányzó 117 vers forrása (licenc), az elided sorok jelölése (f). A tétel azonosítója `DT-F16` (a `DT<n>` sorozat helyett, ütközés-kerülés a csomagban); átszámozás a merge-kor.

**Nem érintett:** `FELADATOK.md`. `NYITOTT_FELADATOK.md:46` „feltétele az N30” szövege elavult, nem módosítottam.

**Ellenőrzés:** `naplok/ELLENOR_F16.md` (3 kör; 1–2. kör 5–5 eltérés javítva, 3. kör kicsi README-javítás).
