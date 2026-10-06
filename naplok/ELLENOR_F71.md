# ELLENOR_F71 — F71_BSB_ZSOLT13_BRIEF.md · origin/main(115ef44)..claude/bsb-zsolt13

*Készítette a `fuggetlen-ellenor` (a jelentést az orkesztrátor mentette, mert az ellenőrnek nincs fájlíró eszköze). Tömörítve.*

| pont | eredmény | indok |
|---|---|---|
| EF1 hat MT-vers | **ELTÉRÉS** | csak MT 3–6 (41 sor, `BSB_Strongs.tsv:178405–178445`). A BSB 13:1 a display-JSON-hiány (DT6 (c)) miatt nincs meg; a felirat BSB-oldalon nem hordoz Strongot, a TAHOT szerint az MT 13:1 igen (H1732, H4210, H5329). Dokumentált, de nincs hozzá N-tétel → N-F71a. |
| `manual` proveniencia, kézi kivétel | OK | napló: `F41_bsb_megfeleltetes.tsv`, `F16_bsb_lefedettseg.tsv` fejléc; az 1Kir 22:43 mintája azonos (a BSB-táblában az `mt` nem különböztethető meg a WLC-vel igazolttól) |
| M3 nulladiff | OK | `41 0` a numstatban, egyetlen hunk, mind `Psa.13.`; 278 166 adatsor |
| M0 ⛔ | OK | MT 3–6 Strong-halmaza a `lekerdez.py gerinc` szerint egyezik; a ⛔ nem lépett életbe |
| M1 kód | OK | `KEZI_KIVETEL` részhalmaz-ellenőrzéssel, eltérésnél `SystemExit` |
| M2 `mt` | OK | 38 `forditva`, 3 `elhagyva`; a fejléc-számok egyeznek |
| M4 README | **ELTÉRÉS** | elavult számok (278 125, 247 173, 30 952/744, 260 243/20 180, 182) → **javítva** az orkesztrátor által |
| Kanonikus adatréteg | **ELTÉRÉS** | `adat/datasetek.tsv:77–80`, `adat/SEMA.md:379` „Zsolt 13 illesztetlen” → **javítva** |
| `F41_wlc_versszam_ellenorzes.tsv:501` | **ELTÉRÉS** | Zsolt 13 `nincs_bsb_sor`; WLC-összevetés nem futott → N-F71a-ban nyitva |
| `F16_bsb_zsolt_megfeleltetes.tsv` fejléc | ELTÉRÉS (alacsony) | kézi szerkesztés gépi fejléccel → N-F71a-ban nyitva |
| EF3, CI, M2 reprodukálhatóság | NEM ELLENŐRIZHETŐ | az ellenőr körén kívül; `futtat.py` (E2–E26) 0 találat a diffen |
| A2 | megjegyzés | DT-F41a és DT6 a merge után elavul — a lezárás a felhasználóé |
