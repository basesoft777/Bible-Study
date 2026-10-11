# F63 JELOLTEK_RETRO — zárójelentés (tervezet; az ellenőr és a PR az orkesztrátoré)

**Adat:** `adat/jeloltek.tsv` 344 → 588 sor (+244, csak hozzáfűzés, meglévő sor változatlan; `elofordulasok.tsv` érintetlen). `gate.py` és `ellenoriz.py`: SÉRTÉS 0. Írás: `nem_vizsgalt.py hozzafuz --ir`, munkalapról (`naplok/JELOLTEK_RETRO_<ID>_sorok.tsv`), proveniencia `scope=manual`.

| motívum | pótolt | ebből `nyitva` | ★ még nem vizsgált |
|---|---|---|---|
| ALVIL-001 | 2 | 0 | 3 |
| ANTROP-001 | 0 (nincs napló, explicit) | 0 | 2 |
| HAMART-001 | 170 | 7 | 0 (+ 526 csoportos kizárás, 501 szűkítendő) |
| HODIT-001 | 1 | 0 | 0 |
| ISTENTISZT-001 | 60 | 0 | 17 (+ 156 pontatlan kollokáció) |
| KIRALY-001 | 8 | 1 | 6 (+ 631 szűkítendő) |
| MENNY-001 | 1 | 0 | 0 (+ 269 pontatlan kollokáció) |
| TEREMT-001 | 2 | 0 | 1 |

**Eszköz:** `eszkozok/nem_vizsgalt.py` (`lista`, `hozzafuz`, `lelet`, `meres`) + `teszt_nem_vizsgalt.py`; a scan-halmaz futáskor az `elofordulasok.strong`-ból; egy kategorizálás (csoportos / pontatlan / szűkítendő / tematikus horgony) a `lista` és a lelet-mérés között; `auditok.tsv` nem változott.
**Lelet:** ANTROP-001 minta `naplok/JELOLTEK_RETRO_lelet_ANTROP.md` (3 ★: 1 `nyitva`, 2 még nem vizsgált; 61 vers tematikus horgony); mind a 8 motívum mérése `naplok/JELOLTEK_RETRO_lelet_meres.md` (csak mérés; HAMART, ISTENTISZT, KIRALY, MENNY: olvasói lelet-lap nem készül).
**K-ellenőrzés:** K1–K3 teljesül (forrás a `forras_kereses`-ben, `nyitva` a dokumentálatlan, `ellenoriz.py` zöld); K4 az ANTROP-001-nél nem teljesül (explicit, DT-F63a (5), DT-F63b); K5 az ellenőrre vár.
**Döntések:** DT-F63a, DT-F63b, DT-F63c (🟢, számot a `szamkiosztas` ad). **Nyitott:** N-F63a (3 beépítve↔hiányzó `elofordulasok`-sor), N-F63b (ANTROP napló), N-F63c (`nyitva` sorok), N-F63d (szószintű/±1 kollokáció), N-F63e (HAMART/KIRALY gerinc felülvizsgálata).
**Hátra:** `fuggetlen-ellenor` (`naplok/ELLENOR_JELOLTEK_RETRO.md`, 10 sor visszakeresése a forrásban), draft PR, a brief lezárása — az orkesztrátor.
