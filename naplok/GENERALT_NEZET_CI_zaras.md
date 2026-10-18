# GENERALT_NEZET_CI — zárójelentés (FELADATOK #116)

*Ág: `claude/f116-generalt-nezet-ci` (be85d5de-ről) · végrehajtó: claude-sonnet-5-5 (kért: sonnet) · orkesztrátor és ellenőr: claude-opus-5-5 · 2026-10-18*

- **Kész:** az E28 (a generált nézet bájtra, sorvéggel együtt egyezik a commitolt blobbal) és az E29 (a kiadható kimenetben nincs `belso`, `【NAPLO`, illetve `olvasoi` mélységnél markerjelölés) a `szabalyok.py`-ban, bekötve a `futtat.py`-ba és a workflow-ba. Mindkettő HIBA szintű és fájlszintű (D6). Az engedélyezőlista üres (`e28_migralt_nezetek.tsv`, D2).
- **Mérés** (`naplok/GENERALT_NEZET_CI_meres.md`): az M0 egyezik a brief feltevéseivel. A `futtat.py --teljes` E28/E29 0 találatot ad. Az ISTENTISZT-001 próbája ideiglenes listával, commit nélkül: az E29 14 `【NAPLO` sort jelez, az E28 1 eltérést. Tesztek: 142 OK. A `feladatok.py ellenoriz` 0 hibát ad.
- **F116.3:** a `naplo#konyv_index` (4 diff-sor) és a `nyitott` (79 diff-sor) blokk újragenerálva, a felhasználó előzetes jóváhagyásával. Minden diff-sor visszavezethető commitolt adatváltozásra (98f22fc6, a0c3cd95, 4f85d54c, b5e60b5c).
- **Egyeztetett eltérés:** a `NYITOTT_FELADATOK.md` írása a brief `ir` mezőjén kívül (a felhasználó jóváhagyta, 2026-10-18, (a) változat).
- **Független ellenőrzés** (`naplok/ELLENOR_F116.md`):
  - az első kör 2 ELTÉRÉST talált (sorvég-normalizálás a CI-tervvel szemben; kezeletlen `ValueError`), ezt javította az F116.11–13;
  - az újraellenőrzés további 2 kisebb eltérést talált (a blob-ág teszteletlen; elavult docstring), ezt javította az F116.14.
  - Nyitott eltérés nincs. A második javítókört az orkesztrátor ellenőrizte, nem a független ellenőr.
- **Eltérések a briefhez képest:**
  - a 3. lépésben a markerek `ts=` értéke nem változott (a generátor a meglévő markert nem írja át);
  - az E29 mintakészlete bővebb (`【NAPLÓ`, `SZINT: belso`).
- **Tudnivaló a #11-nek:** a lista sorát felvevő PR `[ELLENŐRZŐ]` előtagot kap (D3). Az `adat/jeloltek.tsv`-t, `motivumok.tsv`-t vagy `elofordulasok.tsv`-t író PR ugyanabban a PR-ben újragenerálja a marker-blokkot (D4). A #11 fejlécére vonatkozó javaslat: D7.
- **Nyitva:** push és draft PR (`[ELLENŐRZŐ]` előtaggal) a felhasználó kérésére. A CI-t csak a PR futtatja: Python 3.11, a helyi mérés 3.14-gyel ment.
