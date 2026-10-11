# F63 JELOLTEK_RETRO — zárójelentés (tervezet; az ellenőr és a PR az orkesztrátoré)

**Adat:** `adat/jeloltek.tsv` 344 → 594 sor (+250: 244 + 6 KIRALY-001 BDB-„chieftain” elutasítás az ellenőri javításban; csak hozzáfűzés, 4 sor forras_kereses/indoklas mezője pontosítva; `elofordulasok.tsv` érintetlen). Írás: `nem_vizsgalt.py hozzafuz --ir`, munkalapról (`naplok/JELOLTEK_RETRO_<ID>_sorok.tsv`), proveniencia `scope=manual`. A 244 sort egyetlen commit (F63.5), a 6 sort az F63.15 fűzte hozzá; a brief M1-je motívumonkénti külön commitot írt elő.

| motívum | pótolt | ebből `nyitva` | ★ még nem vizsgált |
|---|---|---|---|
| ALVIL-001 | 2 | 0 | 3 |
| ANTROP-001 | 0 (nincs napló, explicit) | 0 | 2 |
| HAMART-001 | 170 | 7 | 0 (+ 537 csoportos kizárás, 501 szűkítendő) |
| HODIT-001 | 1 | 0 | 0 |
| ISTENTISZT-001 | 60 | 0 | 17 (+ 156 pontatlan kollokáció) |
| KIRALY-001 | 14 | 1 | 6 (+ 621 szűkítendő) |
| MENNY-001 | 1 | 0 | 0 (+ 269 pontatlan kollokáció) |
| TEREMT-001 | 2 | 0 | 1 |

**Eszköz:** `eszkozok/nem_vizsgalt.py` (`lista`, `hozzafuz`, `lelet`, `meres`) + `teszt_nem_vizsgalt.py`; a scan-halmaz futáskor az `elofordulasok.strong`-ból; egy kategorizálás (csoportos / pontatlan / szűkítendő / tematikus horgony) a `lista` és a lelet-mérés között; `auditok.tsv` nem változott.
**Lelet:** ANTROP-001 minta `naplok/JELOLTEK_RETRO_lelet_ANTROP.md` (3 ★: 1 `nyitva`, 2 még nem vizsgált; 61 vers tematikus horgony); mind a 8 motívum mérése `naplok/JELOLTEK_RETRO_lelet_meres.md` (csak mérés; HAMART, ISTENTISZT, KIRALY, MENNY: olvasói lelet-lap nem készül). A HAMART-001 „0 még nem vizsgált” értéke NEM jelenti, hogy a motívum végig van vizsgálva: azért 0, mert 501 vers ideiglenesen „szűkítendő” lett, amíg az N-F63e el nem dől. Ugyanez a MENNY-001: 0 mellett 269 „pontatlan” vers áll (az N-F63d-re vár).
**K-ellenőrzés (valós eredmény):** `gate.py` rc 0; `ellenoriz.py` SÉRTÉS 0; `ellenorzes/futtat.py --valtozott` (diff-alap: merge-base) E9 = 0 (a DT-F63c „sense” szava javítva), HIBA 0; `teszt_nem_vizsgalt.py` rendben. K1–K3: az ellenőri 2., 5., 8. eltérés javítva, a 9. (ISTENTISZT-001 1Pét 1:6-7 indoklása) a napló szövegeltérése miatt döntésre vár; K4 az ANTROP-001-nél nem teljesül (explicit, DT-F63a (5), DT-F63b); K5 az ellenőr 2. körére vár. A zárás fájlneve `F63_zaras.md` (a brief `JELOLTEK_RETRO_zaras.md` nevétől eltér).
**Döntések:** DT-F63a, DT-F63b, DT-F63c (🟢, számot a `szamkiosztas` ad); felhasználó, 2026-10-11, chat: „a DT-F63b és DT-F63c döntését megerősítem”. **Nyitott:** N-F63a (3 beépítve↔hiányzó `elofordulasok`-sor), N-F63b (ANTROP napló), N-F63c (`nyitva` sorok), N-F63d (szószintű/±1 kollokáció), N-F63e (HAMART/KIRALY gerinc felülvizsgálata).
**Hátra:** `fuggetlen-ellenor` (`naplok/ELLENOR_JELOLTEK_RETRO.md`, 10 sor visszakeresése a forrásban), draft PR, a brief lezárása — az orkesztrátor.
