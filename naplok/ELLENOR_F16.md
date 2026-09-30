# ELLENŐR — F16 (BSB-import), 3 kör, tömörítve

Ág: `claude/bsb-import`, base `origin/main` (4525a63). Ellenőr: `fuggetlen-ellenor`; a jelentés az orkesztrátor által mentett tömörítés (az ellenőrnek nincs írási eszköze).

**1. kör — ELTÉRÉS 5:** (1) Zak 12:1 hiányzik az importból, gyanú: `isdigit` szűrő; a Zsolt 116 vers is gyanús; (2) DT5 „valódi címkézési eltérés” állítás jelöletlen értelmezés; (3) az ÚSZ-mérés TAGNT-kiterjesztése nincs kimondva eltérésként; (4) BSB nincs a `datasetek.tsv`-ben és a README-ben; (5) a brief `ir:` hiányos.
**Javítás (F16.4):** a hiány forráshiány (BSB `base/display` 117 vers, mind 1. vers; a `text-only` CC0 megvan, a `hebrew-tsv`/`greek-tsv` licence nem kimondott), a szkript szűrt sorokat kategóriánként számol; értelmezések jelölve; ÚSZ-eltérés kimondva; regisztráció és `ir:` pótolva.

**2. kör — ELTÉRÉS 5:** (1) a DT5 „a BSB nem címkézi a névelőt” állítása hamis (a névelő elided span-ként címkézett); (2) 27 043 üres „Angol szó” sor (elided) nincs dokumentálva; (3) a napló szűrési fejlécének hatóköre (66 könyv) nincs kimondva; (4) `adat/SEMA.md` 2.6 elavult (17/68); (5) kozmetikai hiba a DT5-ban.
**Javítás (F16.5):** mind az öt.

**3. kör — ELTÉRÉS 1 (kicsi):** a README a 27 043 üres sor példájaként `G3588`-at említette, a fájlban 0 G-sor van. Az orkesztrátor javította (F16.6).
Nem ellenőrizhető: a névelő-elided állítás a repóból (a BSB forrás-JSON a scratchpadben volt; 2. körben az ellenőr közvetlenül igazolta); E1/E17 a CI-ben.

**Eredmény:** TISZTA a 3. kör kicsi README-javításától eltekintve. `BSB_Strongs.tsv` bájtra változatlan a 2. kör óta, licenc (CC0) és sorcsökkenés-⛔ rendben, saját CI-futtatás: E2–E16 0 találat (E9/E11 régi sorokon).
