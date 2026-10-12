# F79 zárás -- SQLITE_EPIT (pardes.db)

*2026.10.12 · ág: `claude/f79-sqlite-epit` · döntés: DT-F79a (🟢, a felhasználó, 2026.10.12) · az ellenőrzést a koordinátor futtatja (`naplok/ELLENOR_F79.md`)*

- **Eszköz:** `eszkozok/sqlite_epit.py` (`--mod minta|teljes`, `--proba`, `--naplo`), tesztek: `eszkozok/teszt_sqlite_epit.py` (30, zöld).
- **Teljes építés:** `pardes.db` 59 tábla, **786,1 MB**, 42–47 s; két teljes építés táblánkénti tartalom-hash-e azonos (G2). Nem commitolt (`.gitignore`, G1).
- **Integritás:** az `ellenoriz.py` 1–8 (7. jelentés) + 9., 10., 11., 13. szabálya a betöltés előtt, mind RENDBEN; sértésnél nincs fájl (negatív teszt: 1–6., 8., 9., 13.). A 10. és 11. szabályra nincs külön negatív teszt.
- **Kis minta próbája (M3):** az ADATVAGYON 1–6., 13–15. pontja 9/9 egyezik a forrással megnevezett várt eredménnyel (`naplok/SQLITE_EPIT_meres_minta.md`); az 5. pont többlet-találatai (névadó „hívta a nevét”) jelölve.
- **Méret (a #86 N-F86b bemenete):** a `licenc_*` három oszlop tartalma 212,1 MB a 786,1 MB-ból (27,0%); a legnagyobb táblák: `token_karoli`, `frazis_pozicio`, `strong_parok`, `token_par`. A mérés: `naplok/SQLITE_EPIT_meres.md`. Az ADATVAGYON 7. becslése (50–150 MB) tehát soronkénti licenc-oszlopokkal nem tartható; táblaszintű licenc-tárolás kb. 200 MB-ot spórolna.
- **Nem betöltött:** Macula_*, LXX_OS, KJV_/ASV_*, TBESG/H, Karoli_Strong_kivonat és a BDB-segédtáblák (a briefben/DT-F79a-ban nincs nevesítve); lista a mérés Megjegyzések szakaszában.
- **Nyitott (helyőrző):** N-F79a (licencsor a `karoli_strong/*` és `karoli_variancia` táblákhoz), N-F79b (nem létező Károli-versre mutató `kh`/TIPNR/BSB sorok) a `NYITOTT_FELADATOK.md`-ben.
- **Megállapítások:** a TIPNR 2741 különböző Strong-értéke betűutótagos (`G0001G`), a `strong` NULL, a nyers érték a `strong_nyers`-ben; a `Lam`→`JSir` / `Sir` kulcs-eltérés álnévvel kezelve (337 kh, 58 tipnr sor menne néma nem-találatba).
- **Az adatréteg érintetlen:** a diff nem érint `adat/`, `konkordancia/`, `motivumok/`, `lexikon/` fájlt (G1).
