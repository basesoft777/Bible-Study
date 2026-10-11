# ELLENOR_F22_Ruth — F22_KAROLI_STRONG_BRIEF.md (D34, v2.28), `3ceddf0a..eb762eb7`

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-ruth` (külön worktree); commitok: `4c820897`, `ab9171ea`, `eb762eb7`.*

ELTÉRÉS: 1 tétel

## Igazolt (saját lekérdezéssel)

- **85/85 vers, 4 fejezet:** a `Karoli_1908.tsv` `^Ruth ` sorai 85 (22 + 23 + 18 + 22 vers); a minta 85 sor; a TAHOT-ban nincs Károlin túli Ruth-kulcs.
- **parok_Ruth 2 078:** 2 080 sor = proveniencia + fejléc + 2 078; mind `alacsony / S`; fejezetenként 541 + 614 + 411 + 512.
- **szavak_Ruth 4 071:** hu 2 045 (1 663 `parositva`, 382 `betoldas`), er 2 026 (1 884 `parositva`, 142 `forditatlan`); hu = a `minta_Ruth.tsv` `karoli_szo` összege (514 + 605 + 411 + 515); er = a `TAHOT_kivonat.tsv` `^Ruth ` sorai; `kezi` / `fuggoben` / `magas` 0.
- **Kapuhiba 1/85 → 0:** a k3 (Ruth 2:3); a javító kör `kapuhiba_db` 0 / `igen`; az átnézési fájl csak fejléc.
- **Költség:** 1. kör 0,560952, 2. kör 0,021406, összesen 0,582358 USD; tokenek 99 812 / 92 228 és 13 491 / 1 583; plafon 1,00 (minimum); versenként 0,00685. Kumulatív 77,223186 USD: a 10 Ruth-sor `futo_osszeg_usd` értéke a 76,640828-ról indul, mind = előző + a sor költsége.
- **Batchek:** 9 + 1 kérés; **10 verses kötegek:** 8 × 10 + 5. **Versbeosztás:** a `versmegfeleltetes.tsv`, `versmegfeleltetes_kezi.tsv`, `versosszevonas.tsv` fájlokban 0 Ruth-sor.
- **K9:** `adat/datasetek.tsv` 8 sor (8/8 csere, a 4 parok-sor jelentéslistájában a Ruth), `adat/SEMA.md` 2.20; az 1Kir/Neh/2Kir/Dán megmaradt, duplázás nincs. **`tokenek.py`:** `…, '2Kir', 'Dán', 'Ruth')`.
- **Jóváhagyás időrendje:** a jóváhagyó commit (14:47:03Z) 8 másodperccel az 1. batch (14:47:11Z) előtt készült.
- **A 15 megmaradt kis könyv:** 1 540 vers; parok-fájl egyiknek sincs; a Hós (1:11, 11:11) és a Préd (2:26) 2:1 beolvasztása a `versosszevonas.tsv`-ben megvan, a többi 13 könyvé nincs.
- **Szúrópróba (lekerdez.py scan):** H1961 (Ruth 1:1), H1162 (Ruth 2:1): n=1 mind. **Idegen fájl a diffben:** nincs (15 fájl, mind Ruth-specifikus vagy a brief `ir` mezőjében).
- **Kulcs-grep:** üres. **CI-eszköz:** exit 0; E2–E16, E19, E20, E26: 0; E25: 3 és E27: 33, repószintű, nem e diffből; E12–E15: 0.

## ELTÉRÉS

1. **D34 / A1:** a „Ruth a hiányzó kis könyvek közül a legkisebb (85 vers)” állítás téves: az Abd 21, a Hag 38, a Náh 47 és a Jón 48 verssel kisebb. A futtatást és az adatokat nem érinti; a döntésnapló indoklása hibás volt. **Javítva** a briefben (D34) és a jelentésben.

## Nem ellenőrizhető a szerepkörből

`egyesit.py --ellenoriz` és a K7 újraépítés (a fő session futása: „rendben”), a K1 egyedisége, a K3 hash számítása, a chatben adott jóváhagyás („mehet a Ruth”), a CI-jelentés összevetése (nem kapott jelentést).
