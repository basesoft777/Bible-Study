# F79 zárás -- SQLITE_EPIT (pardes.db)

*2026.10.12 · ág: `claude/f79-sqlite-epit` · draft PR #300 · döntés: DT-F79a, DT-F79b · javító kör: `naplok/ELLENOR_F79.md` 9 eltérése (F79.9–F79.13), 2. kör: `naplok/ELLENOR_F79_2.md` (F79.15–F79.18)*

- **Eszköz:** `eszkozok/sqlite_epit.py` (`--mod minta|teljes`, `--proba`, `--naplo`, `--ketszer`, `--meret`); tesztek: `eszkozok/teszt_sqlite_epit.py` (37, zöld).
- **Teljes építés:** `pardes.db` 63 tábla, **845,4 MB**, 52,6 s; a második, ideiglenes építés táblánkénti hash-táblája azonos, a táblázat a mérésben (G2). Nem commitolt (`.gitignore`, G1). A diff nem érint `adat/`, `konkordancia/`, `motivumok/`, `lexikon/` fájlt.
- **Integritás:** az `ellenoriz.py` 1–8 (7. jelentés) + 9., 10., 11., 13. szabálya a betöltés előtt, mind RENDBEN; sértésnél nincs fájl (negatív teszt: 1–6., 8., 9., 10., 11., 13.).
- **Kis minta próbája (M3):** 9/9 egyezik a forrással megnevezett várt eredménnyel; külön napló: `naplok/SQLITE_EPIT_proba_minta.md` (a mérés újragenerálása nem írja felül).
- **Méret (a #86 N-F86b bemenete):** táblánkénti bájtméret indexestül, licenc_* nélküli változattal a `naplok/SQLITE_EPIT_meres.md`-ben; a három `licenc_*` oszlop valódi részesedése **250,4 MB (29,6%)**. A legnagyobb táblák: `token_karoli`, `frazis_pozicio`, `token_eredeti`, `token_par`, `strong_parok`.
- **Javítások (ELLENOR_F79):** betöltve a `Karoli_Strong_kivonat` (383), `KJV_Strongs_teljes`, `TBESG`, `TBESH`; a `morf_kulcs_heber`/`morf_nyelv_aramai` saját licenc-sora (CC BY 4.0); a TAGNT/TAHOT Károli-vers nélküli kulcsai névvel, tokenszámmal a jelentésben (TAGNT: 3 kulcs / 40 token; `token_eredeti.van_vers`); a „nincs nevesítve” és „#48 vezeti ki” indoklás téves volt: a #48 csak a régi `KJV_/ASV_Strongs_*`-t vezeti ki.
- **Szándékosan nem betöltött:** Macula_*, LXX_OS, KJV_/ASV_Strongs_{Genesis,Exodus,Proverbs}, BDB-segédtáblák, SDBH_SDGNT_domenfa (lista a mérés Megjegyzések szakaszában).
- **Nyitott (helyőrző, `NYITOTT_FELADATOK.md`):** N-F79a (licencsor a `karoli_strong/*` és `karoli_variancia` táblákhoz), N-F79b (nem létező Károli-versre mutató `kh`/TIPNR/BSB/KJV sorok), N-F79c (TIPNR: 16 928 sor NULL `strong`, nagybetűs utótag; az `utotag` szabály a felhasználó döntése, nem változott).
- **Megjegyzés:** a `Lam`→`JSir` / `Sir` kulcs-eltérés álnévvel kezelve; a BSB/KJV→Károli leképezés az N-F41a miatt megbízhatatlan lehet (`kk_leképezés` oszlop).
