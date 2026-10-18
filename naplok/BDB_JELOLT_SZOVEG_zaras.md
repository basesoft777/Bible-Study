# BDB_JELOLT_SZOVEG_zaras.md — F107 zárójelentés (merge függőben)

*Proveniencia: scope=F107 végrehajtás (`claude/f107-bdb-jelolt-szoveg`, F107.0–F107.53) | forras=`konkordancia/lexikonok_nyers/DictBDB.json` (SHA-256 5d826c58…e33d) + `BDB.lexicon` (szerkezeti metaadat), `eszkozok/bdb_jelolt/` | ts=2026-10-18 | modell: claude-opus-5-5 (végrehajtó és ellenőr)*

- **Forrás (DT-F107a, DT-F107d):** hibrid bontás — a szöveg és a bekezdés-tagolás a `DictBDB.json`-ból (a repóba került, `*.json -text`), a `bdb_id`, a szócikkhatár és a `section`/`remarks` a lexikonból; a `_convert_bdb.py` szerkezetvesztése utólag naplózva; a playbook 2. pontja kiegészítve (két szabály, CI-kapu nélkül).
- **Szakasztábla:** `adat/bdb_szakaszok.tsv` 36 621 sor, 8 090 JSON-Strong; illesztés 7 916 `egyezik`, 144 Strong `bdb_id` nélkül (explicit hiány, DT-F107e); 9 JSON-kulcs nélküli TSV-Strong listázva (SEMA 2.30).
- **Mérce:** aranyminta 411/425 (96,7%) teljes, 411/416 (98,8%) forráshiba nélkül — elfogadva (DT-F107i), a maradék 5 csomópont az N-F107c-ben; seed-101 9/13 (9/10); korpusz a mai szeletelővel 85,4%.
- **Javítótábla:** `adat/bdb_forras_javitas.tsv` 7 202 sor: 6 781 pe/mem (DT-F107f; 3 823 `javitva`), 412 F34/F46 hivatkozás-javítás (DT-F107c (d)), 9 kézi forráshiba (`manual`).
- **Nézet:** `nezet_general.py` a táblából + javítótáblából; a `BDB_teljes_unabridged.tsv` és az `adat/forditasok.tsv` változatlan; ismeretlen okú eltérés 0. A TSV cseréje és az olvasók átállása külön feladat (`/befogad`).
- **Magyar illesztés:** `adat/bdb_szakasz_hu.tsv` 9 664 sor, 674 Strong: 409 illeszkedik, 85 horgonnyal, 98 elakad, 82 tagolatlan (kiinduló: 355/–/230/89); a 98 Strong (606 szakasz) a #38-nak (N-F107b, DT-F107b).
- **Tesztek:** `eszkozok/bdb_jelolt/teszt_bont.py` 45 OK; a három tábla `--ellenoriz`-e bájtra azonos (a merge után is); `feladatok.py ellenoriz` 140 brief, 0 hiba; `ellenorzes/futtat.py` exit 0.
- **Független ellenőrzés (`naplok/ELLENOR_F107.md`):** ELTÉRÉS 6 tétel, mind kezelve a javítókörben (F107.47–F107.52; napló „Javítókör”).
- **Egyeztetett eltérések (a felhasználó döntései, 2026-10-18):** az `ir` bővült az `adat/licencek.tsv`-vel, az F102 és F38 brief törzsével (átadás, fejléc nem) és a `.gitattributes`-szel; a ≥ 99%-os mérce helyett 98,8% (DT-F107i).
- **Döntések és nyitott tételek (helyőrzők):** DT-F107a–i (🟢); N-F107a (pe/mem a kész fordításokban), N-F107b (a #38 újrafordítandó listája), N-F107c (aranyminta-maradék, H7626 „145:”). A DT190 🟡: a kulcs nincs befagyasztva.
- **Merge:** az origin/main beolvasztva (F107.53); ütközés a `DONTESEK.md`, `NYITOTT_FELADATOK.md`, `adat/datasetek.tsv` végén, mindkét oldal sorai megmaradtak. A main SEMA-ja (F118) a `DT-F107d` helyőrzőre hivatkozik — a `szamkiosztas`-nak ezt is követnie kell. A #38 fut: az F38 brief törzse később ütközhet.
