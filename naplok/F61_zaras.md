# F61 zárójelentés — A lekérdező maga naplózzon (LEKERDEZ_NAPLO)

*2026-10-11 · ág: `claude/f61-lekerdez-naplo` · modell: sonnet · M0 → DT102 → M1 → ellenőr → DT103 → alkalmazás*

- **Kész:** a `lekerdez.py` minden alparancsa `--naplo ID --lepes {A5,B2,B3,B4,adhoc}` kapcsolóval maga fűzi a proveniencia-sorát (`csatorna=cli`): létező motívum → `adat/auditok.tsv`, `^F\d+$` → `naplok/<KÓD>_lekerdezesek.tsv`, más → hiba, exit 1. Csak hozzáfűzés, duplikáció-szűrés, `csv` nélkül; kapcsoló nélkül a kimenet bájtra azonos.
- **`ellenoriz.py`:** a `csatorna` megengedett proveniencia-kulcs. **SEMA 2.9:** `adhoc` lépésérték, „Önnaplózás” bekezdés, commitolási szabály.
- **DT102** (🟢): a három ágú `--naplo`, `csatorna=cli`. **DT103** (🟢): az `# napló:` állapotsor a stderr-re megy; a motívum auditsorai csak a „mindig”-datasetek teljes lefedése után commitolandók.
- **Ellenőr** (`naplok/ELLENOR_F61.md`): 5 eltérés; ebből a 8. szabály X1 (egy új motívum első auditsora SÉRTÉS (3), ideiglenes másolaton mérve; a mai adaton látens) és az utolsó-sor (K2) a DT-F61b-ben dőlt el és alkalmazva; a main beolvasztva (E5), a PR-cím `[ELLENŐRZŐ]` (E16); az N-F helyőrző felvéve.
- **Tesztek:** `teszt_lekerdez_naplo.py` 8/8, `teszt_lekerdez_sir.py` OK, `ellenoriz.py` SÉRTÉS 0, `feladatok.py ellenoriz` 0 hiba, CI E5/E16 0.
- **Nyitott:** N-F61a (a `naplok/*_lekerdezesek.tsv` formai ellenőrzése, helyőrző); a `_ProvFogo` sorvég nélküli utolsó sort elnyelne (ma nincs `end=`, látens).
- **Egyeztetett eltérés:** a `PILOT-…` ág nincs megvalósítva (nincs használatban); az ellenőr-jelentés neve `ELLENOR_F61.md` (a brief hivatkozása igazítva).
- **Merge:** nincs, a felhasználóé.
