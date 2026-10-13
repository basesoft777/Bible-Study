# ELLENOR_F89 — F89_LICENC_RENDEZES_BRIEF.md

*Tartomány: `49c77c32..996a0176` (merge-base(origin/main, claude/f89-licenc-rendezes)..fej) · ellenőr: claude-opus-5-5 (kért: opus) · 2026-10-13*
*A bemenetként várt CI-jelentést nem kaptam meg; a CI-sor a saját futtatásomon alapul. A jelentést az orkesztrátor írta ki a fájlba az ellenőr szövegéből (az ellenőrnek nincs Write eszköze).*

ELTÉRÉS: 8 tétel

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| 0 modell | OK | — | tényleges: claude-opus-5-5; kért: opus |
| 0 modell-mezők | NEM ELLENŐRIZHETŐ | `naplok/F89_M0_felmeres.md:3` | a végrehajtó tényleges modelljét lekérdezéssel nem lehet igazolni; adattáblába a menet nem írt `modell` mezőt |
| G1 | OK | `adat/licencek.tsv:11,33,34,49,53–55` | `git diff --numstat` → 7/4: 4 módosított és 3 új sor, más hunk nincs; az író szkript `csv`-mentessége csak a naplóból igazolt |
| G2 | OK | `adat/licencek.tsv:49,53–55` | projekt_adat `tisztazott`, forras_hely LICENSE + DT-F89a, kereskedelmi=igen, share_alike=nem; az új sorok minden mezője kitöltött |
| G3 | NEM ELLENŐRIZHETŐ | `naplok/F89_M0_felmeres.md:90` | DT-F89b (2.) miatt a lexikon nem generálódott újra; az éles `lexikon/` 146 helyen `projekt-adat` címkét hordoz (8 fájl); szabad licenc-jelölés nincs |
| G4 | OK (kódszinten) / pardes.db NEM ELLENŐRIZHETŐ | `eszkozok/sqlite_epit.py` | licenc_* oszlopok kikerültek, minden tábla `tabla_licenc`-sort kap; az FTS árnyéktáblák (`fts_motivum_%`) nem kapnak sort |
| G5 | OK | `naplok/SQLITE_EPIT_meres.md` | 878,9 → 619,0 MB; tisztazatlan 1 (`kjv`), CC BY-SA/MCGED 9, NC 0; megjegyzés: az NC-detektálás a `cimke`-ben „BY-NC”-t keres, a tisztazatlan NC-sor címkéje `tisztázatlan` |
| G6 | NEM ELLENŐRIZHETŐ | `naplok/SQLITE_EPIT_meres.md:19–21` | építés és teszt nem futtatható az ellenőrben |
| D1–D3, DT116/DT113 | OK | `LICENSE`, `adat/SEMA.md:921,957–959` | a döntések szerint |
| DT-F89b | ELTÉRÉS | `DONTESEK.md:206–208` | üres sor került a DT-F89a és a DT-F89b közé, a fájl végéről hiányzik az újsor; a DT-F89a „Alkalmazás” szövege (lexikon-újragenerálás) elavult; a brief döntésnaplójában nincs DT-F89b sor |
| A1 | OK | `naplok/F89_M0_felmeres.md` | a számok lekérdezéssel stimmelnek (50 sor a licencek.tsv-ben, 8 tisztazatlan, 146/8) |
| A2 | ELTÉRÉS | `NYITOTT_FELADATOK.md:54`; `DONTESEK.md:208` | a „külön feladat” (a lexikon újragenerálása és a címkeváltás) sehol nincs nyilvántartva (nincs N-F89a helyőrző) |
| A3–A5 | nem értelmezett | — | — |
| A6 | OK | — | `futtat.py` E12–E15: 0 találat |
| CI | ELTÉRÉS | `naplok/SQLITE_EPIT_meres.md:91` | E5 HIBA: 1 — törölt címsor TÖRLÉS-SZÁNDÉKOS jelölés nélkül: „## Táblánkénti bájtméret és a `licenc_*` oszlopok részesedése (a #86 N-F86b bemenete)”; E25/E27: régi jelentések |
| SEMA 2.19/2 | ELTÉRÉS | `adat/licencek.tsv:11,33,34` | a `tisztazott` sor megjegyzése nem mondhat ellent: jelöletlenül maradt „A projekt-adat saját licence még nincs rögzítve” és „… ezért tisztazatlan marad” |
| kotelezo_megjeloles | ELTÉRÉS | `adat/licencek.tsv:11,33,34` | a Strong_szotar, ill. a TAHOT (CC BY 4.0) megjelölése hiányzik a mezőből a három újraértékelt soron |
| integritás-napló | ELTÉRÉS | `naplok/SQLITE_EPIT_integritas.md:3` | a main-en véglegesített „DT109 (3), (7)” hivatkozás „DT-F79a (3), (7)” helyőrzőre íródott vissza (a generátor sablonja) |
| NYITOTT formátum | ELTÉRÉS | `NYITOTT_FELADATOK.md:54` | párosítatlan `**` az N-F79a sorban |
| ⛔ M0, M2 | OK | `git log` | az M0 után változott kód/adat; a lexikon és a `generalt_proba/` érintetlen |
| Listák 1–5 | OK | — | törölt adatsor 0; csak a `licencek.tsv` sorszáma változott (46 → 49, Δ=+3); nulla-diff: `lexikon/`, `generalt_proba/`, `konkordancia/`, a licencek.tsv többi 42 sora |

## ELTÉRÉS-ek súlyossági sorrendben

1. CI E5 HIBA (`SQLITE_EPIT_meres.md`: törölt címsor jelölés nélkül).
2. `DONTESEK.md` DT-F89b sor: üres sor a táblában, hiányzó záró újsor, elavult DT-F89a „Alkalmazás” szöveg, nincs sor a brief döntésnaplójában.
3. A2: a lexikon-újragenerálás nincs nyilvántartva.
4. SEMA 2.19 2. szabály: ellentmondó megjegyzések a három `tisztazott` soron.
5. `kotelezo_megjeloles` hiánya a három újraértékelt soron.
6. `SQLITE_EPIT_integritas.md`: visszaírt DT-F79a helyőrző.
7. `NYITOTT_FELADATOK.md:54`: párosítatlan `**`.
