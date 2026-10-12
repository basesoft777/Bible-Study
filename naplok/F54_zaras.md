# F54 — LXX_OS_LEFEDETTSEG: zárójelentés-tervezet

*2026.10.11 · tervezet (az orkesztrátor zár) · részletek: `naplok/LXX_OS_LEFEDETTSEG_M0.md`, `…_M2.md`, `…_osztalyozas.tsv`, `naplok/F54_parok_kulonbseg.md`*

- **Hatókör:** az 503 `csak_regi_vers` Károli-vers mindegyikéről ítélet (K1): A 438 (kulcsolási rés), B 3 (Ézs 3:1, Jer 7:27, Jer 27:17), C 5 (nem létező Károli-vers), bizonytalan 57 az M0-ban, **56** a végállapotban (a Zsolt 13:5 a DT99 javítása óta kulcsolt).
- **K2: 435 A osztályú vers kulcsolva, 4 explicit üres (2Móz 37:4, 37:13, 38:1, 1Kir 4:27), okkal; a felhasználó elfogadta üresnek, 2026-10-11.** Tárgyilag: az osztályozó táblában (M0 pillanatkép) a Zsolt 13:5 „bizonytalan”, a DT99 javítása óta kulcsolt, és ebben a 435-ben benne van (438 − 4 + 1).
- **Pótolt kulcs:** 304 vers az általános importszabállyal (tábla-kjv, zsoltár-felirat, sorrend-beágyazás; `lxx_os_import.py --ujrabesorol-lefedettseg`), 130 vers felülbírálati sorral (2Móz 35, Dán 3, Hós 2/13/14, Jób 37; fejezetenként tartalmi mintavétellel) — összesen 434 az 503-ból, K2.
- **Extra kulcs (503-on kívül, 6):** Zsolt 13:6, Zsolt 54:2, Én 5:17–19, Ézs 64:1 — tételesen: M2 7. szakasz.
- **Kimaradt (4):** 2Móz 37:4, 37:13, 38:1, 1Kir 4:27 — üresek (nincs általános szabályos alátámasztás); M2 7. szakasz.
- **Üres, explicit (K3):** 56 bizonytalan (Péld 12 27, Jób 17 15, 2Móz 36 11, Jer 48:40–41, 2Móz 39:38), 3 B, 5 C; N-F54a (Péld 12, Jób 17, 2Móz 36).
- **Zsolt 13 (DT99):** a hibás kulcsok javítva (LXX 12:n → Zsolt 13:n); kettős kulcs 9 → 8 (mind jogos összevonás: az LXX egy Károli-verset két versre bont), idegen kulcs 0 (K4).
- **K5:** csak az `igehely_karoli` és a `karoli_ok` oszlop változott (a javító `assert`-je futáskor ellenőrzi).
- **K6:** `teszt_lekerdez_sir.py` zöld; az F54.3-ban talált hiba (A2: versenként csak az első szósor kulcsolt) az F54.4-ben javítva; `eszkozok/ellenorzes/futtat.py --valtozott` a változott fájlokra: HIBA 0 (E25/E27 JELENTÉS-ek a változás előttiek); CI és független ellenőr: az orkesztrátor dolga.
- **Mintavétel (M2):** 17 A osztályú vers `lxx-hid` kimenete (3 Jób, 2 Hóseás, 4 zsoltár), tartalmi egyezés mindegyiken; a 6 A2 fejezetből mindegyik átment (Jób 37: 4-ből 3 szoros).
- **`LXX_versszintu_parok.tsv` (DT100, 1. opció):** teljesen újragenerálva két commitban: F54.7 az F85-örökség (DT92: +4 597 / −352 sor, 34 eltűnt pár tételesen a `naplok/F54_parok_kulonbseg.md`-ben, 3 mintázandó pár: H7043 Préd 10:10, H0430 Hós 12:4, H5315 4Móz 30:3), F54.8 az F54-hatás (+932 / −15, a 15 mind Zsolt 13). A fájl egyetlen fogyasztója az F05 szótár (S13), amelynek generátora még nem olvassa (egy `.py` sem hivatkozza a fájlt az `lxx_versszintu_import.py`-n kívül), így az újragenerálásnak ma nincs lefelé hatása.
- **Állítás-határ:** az A2 és A3 sorok kulcsa szószám-korrelációra és szomszédkulcsra épül, a tartalmi egyezést a végrehajtó állapította meg (`manual`); a besorolás nem „ellenőrzött” a független ellenőr előtt.
- **Következmény más feladatra:** a #55 (zsoltár-újraellenőrzés) olvas mezője tartalmazza az M0 jelentést; a régi kivonat 129/438 esetben eltolt szöveget adott (M0 2. megfigyelés).
- **Eltérések a brieftől:** a zárás fájlja `naplok/F54_zaras.md` (a brief M3: `LXX_OS_LEFEDETTSEG_zaras.md`), az ellenőri jelentés `naplok/ELLENOR_F54.md` (a brief: `ELLENOR_LXX_OS_LEFEDETTSEG.md`) — a fájlok nincsenek átnevezve. A commit-azonosítók ismétlődnek (F54.1 és F54.2 kétszer szerepel: a döntés-commitok a menet előtti számot kapták); a történet nem lett átírva.
