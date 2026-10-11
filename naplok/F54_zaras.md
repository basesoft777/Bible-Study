# F54 — LXX_OS_LEFEDETTSEG: zárójelentés-tervezet

*2026.10.11 · tervezet (az orkesztrátor zár) · részletek: `naplok/LXX_OS_LEFEDETTSEG_M0.md`, `…_M2.md`, `…_osztalyozas.tsv`, `naplok/F54_parok_kulonbseg.md`*

- **Hatókör:** az 503 `csak_regi_vers` Károli-vers mindegyikéről ítélet (K1): A 438 (kulcsolási rés), B 3 (Ézs 3:1, Jer 7:27, Jer 27:17), C 5 (nem létező Károli-vers), bizonytalan 57.
- **Pótolt kulcs:** 304 vers az általános importszabállyal (tábla-kjv, zsoltár-felirat, sorrend-beágyazás; `lxx_os_import.py --ujrabesorol-lefedettseg`), 130 vers felülbírálati sorral (2Móz 35, Dán 3, Hós 2/13/14, Jób 37; fejezetenként tartalmi mintavétellel) — összesen 434 az 503-ból, K2.
- **Extra kulcs (503-on kívül, 6):** Zsolt 13:6, Zsolt 54:2, Én 5:17–19, Ézs 64:1 — tételesen: M2 7. szakasz.
- **Kimaradt (4):** 2Móz 37:4, 37:13, 38:1, 1Kir 4:27 — üresek (nincs általános szabályos alátámasztás); M2 7. szakasz.
- **Üres, explicit (K3):** 57 bizonytalan (Péld 12 27, Jób 17 15, 2Móz 36 11, Jer 48:40–41, 2Móz 39:38, Zsolt 13:5), 3 B, 5 C; N-F54a (Péld 12, Jób 17, 2Móz 36).
- **Zsolt 13 (DT-F54b):** a hibás kulcsok javítva (LXX 12:n → Zsolt 13:n); kettős kulcs 9 → 8 (mind jogos összevonás: az LXX egy Károli-verset két versre bont), idegen kulcs 0 (K4).
- **K5:** csak az `igehely_karoli` és a `karoli_ok` oszlop változott (a javító `assert`-je futáskor ellenőrzi).
- **K6:** `teszt_lekerdez_sir.py` zöld; az F54.3-ban talált hiba (A2: versenként csak az első szósor kulcsolt) az F54.4-ben javítva; CI és független ellenőr: az orkesztrátor dolga.
- **Mintavétel (M2):** 17 A osztályú vers `lxx-hid` kimenete (3 Jób, 2 Hóseás, 4 zsoltár), tartalmi egyezés mindegyiken; a 6 A2 fejezetből mindegyik átment (Jób 37: 4-ből 3 szoros).
- **Nyitott: DT-F54c** — a `LXX_versszintu_parok.tsv` újragenerálása: a Zsolt 13-on kívül is 352 sor tűnik el (az F85 TAHOT-átkulcsolás miatt, nem az F54 miatt), ezért nincs commitolva; a fájl az M1 438 kulcsa miatt elavult.
- **Állítás-határ:** az A2 és A3 sorok kulcsa szószám-korrelációra és szomszédkulcsra épül, a tartalmi egyezést a végrehajtó állapította meg (`manual`); a besorolás nem „ellenőrzött” a független ellenőr előtt.
- **Következmény más feladatra:** a #55 (zsoltár-újraellenőrzés) olvas mezője tartalmazza az M0 jelentést; a régi kivonat 129/438 esetben eltolt szöveget adott (M0 2. megfigyelés).
