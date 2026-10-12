# ELLENOR_F22_Jon — F22_KAROLI_STRONG_BRIEF.md (D35, v2.29), `7be3977a..01b46a8e`

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-jon` (külön worktree); commitok: `ae91a884`, `62b906d8`, `01b46a8e`.*

ELTÉRÉS: 1 tétel

## Igazolt (saját lekérdezéssel)

- **48/48 vers, 4 fejezet (16 + 11 + 10 + 11):** a `Karoli_1908.tsv` `^Jón ` sorai 48; minden versnek van hu 1 és er 1 sora; a kötegek 10 + 10 + 10 + 10 + 8.
- **parok_Jon 1 052:** mind `alacsony / S`; fejezetenként 391 / 177 / 216 / 268; `magas` / `kezi` / `fuggoben` / C-forrás 0.
- **szavak_Jon 2 071:** hu 991 (827 `parositva`, 164 `betoldas`), er 1 080 (1 000 `parositva`, 80 `forditatlan`); er = a `TAHOT_kivonat.tsv` `^Jón ` sorai.
- **Kapuhiba 2/48 → 0:** Jón 1:8 (k1) és Jón 4:2 (k4); a javító kör `kapuhiba_db` 0 / `igen`.
- **Költség:** 1. kör 0,235696, 2. kör 0,048469, összesen 0,284165 USD; tokenek 53 371 / 36 465 és 27 684 / 4 157; plafon 1,00 (minimum); versenként 0,00592. Kumulatív 77,507351 USD: a 7 Jon-sor `futo_osszeg_usd` értéke a 77,223186-ról indul, mind = előző + a sor költsége.
- **Batchek:** 5 + 2 kérés, 15:06:47Z és 15:09:30Z. **Prompt-hash:** mind `84f12ca7aafb`.
- **Régi arany 2/2:** `Jon.2.6 H8415` és `Jon.2.3 H7585`; `lekerdez.py karoli` és `scan` egyezik (n=1).
- **Versbeosztás:** a `versmegfeleltetes.tsv`, `versmegfeleltetes_kezi.tsv`, `versosszevonas.tsv` fájlokban 0 Jón-sor; a jóváhagyási naplósor a diffben.
- **K9:** `adat/datasetek.tsv` 8 sor (8/8 csere, a 4 parok-sor jelentéslistájában a Jón), `adat/SEMA.md` 2.20; az 1Kir/Neh/2Kir/Dán/Ruth megmaradt, duplázás nincs. **`tokenek.py`:** `…, '2Kir', 'Dán', 'Ruth', 'Jón')`.
- **Jóváhagyás időrendje:** a jóváhagyó commit (15:06:42Z) 5 másodperccel az 1. batch (15:06:47Z) előtt készült.
- **A 14 megmaradt kis könyv:** 1 492 vers; parok-fájl egyiknek sincs; a Hós (1:11, 11:11) és a Préd (2:26) 2:1 beolvasztása a `versosszevonas.tsv`-ben megvan, a többi 12 könyvé nincs.
- **Sorrend-indoklás:** nem tartalmaz memóriából írt állítást; a Ruth-hiba nem ismétlődött.
- **Kulcs-grep:** üres. **CI-eszköz:** exit 0; E2–E20, E26: 0; E25: 3 és E27: 33, repószintű, nem e diffből; E12–E15: 0.

## ELTÉRÉS

1. **(alacsony)** A brief Keretek-szabálya („A session egyedül fut, más Code-session közben nem dolgozik”, `F22_KAROLI_STRONG_BRIEF.md:43`) a jelentés saját beismerése szerint nem teljesült: a menet külön worktree-ben, párhuzamos session mellett készült. Az adatot ez a mért pontokon nem érintette. A szabály vagy API-módú felmentést kap a briefben (D-sor), vagy a felhasználó dönt róla; a Ruth-menetben is így volt, jelzés nélkül. **Lezárva: a felhasználó döntése D36** (2026.10.11, API Batch módú futásra felmentés, saját worktree feltétellel); a brief D36 sora és v2.30.

## Nem ellenőrizhető a szerepkörből

A K1 hu-oldala (a `karoli_szo` oszlop összege), K7 (`egyesit.py` újraépítés / `--ellenoriz`; a fő session futása: „rendben”), a detektor „tiszta” ítélete a Jónásra és a 12 kis könyvre, a chatben adott jóváhagyás („mehet a Jónás”), a CI-jelentés összevetése (nem kapott jelentést).
