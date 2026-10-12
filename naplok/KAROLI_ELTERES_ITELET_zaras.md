# F87 zárás — a #65 eltéréslistájának öt sora (KAROLI_ELTERES_ITELET)

proveniencia: scope=F87 M0–M2 | forras=konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, adat/karoli_strong/parok_{2Moz,Job,Pred}.tsv, eszkozok/karoli_ellenorzes.py | ts=2026-10-12T06:42:35Z (M0), 2026-10-12T06:56:15Z (variancia) | levezetés: `naplok/KAROLI_ELTERES_ITELET_M0.md`; döntés: DT-F87b (soronként elfogadva), DT-F87a (1.: napló + `indoklas`-hivatkozás), felhasználó, 2026-10-12

| # | Sor | Régi → új (`elofordulasok` + `jeloltek`) | Forráslekérdezés (Károli 1908 / TAHOT / gépi pár) | Új ítélet, mód |
|---|---|---|---|---|
| 1 | KIRALY-001 2Móz 19:6 | `karoli_szo` `papok` → `papok birodalma` | „papok birodalma”; TAHOT H3548, H4467; papok=H3548, birodalma=H4467 (`magas`) | `egyezik`/`magas` → `szó-szintű-gépi` |
| 2 | TEREMT-001 2Móz 15:5 | `karoli_szo` `a mélységbe` → `a hullámok` | „Elborították őket a hullámok”; TAHOT H8415; hullámok=H8415 (`magas`) | `egyezik`/`magas` → `szó-szintű-gépi` |
| 3 | ALVIL-001 | `igehely` Jób 17:13 → Jób 17:12; `karoli_szo` `A sírnak` → `a sír` | 17:12 „a sír már az én házam”; TAHOT 17:12 H7585 (17:13: H7845); sír=H7585 (`alacsony`) | `egyezik`/`alacsony`, `tartalom-alapú` |
| 4 | ALVIL-001 | `igehely` Jób 17:16 → Jób 17:15 | 17:16 nem Károli-vers; 17:15 „a sír üregébe”; TAHOT H7585; sír=H7585 (`alacsony`) | `egyezik`/`alacsony` (részleges: üregébe:H0905), `tartalom-alapú` |
| 5 | ALVIL-001 | `igehely` Préd 9:10 → Préd 9:12 | 9:12 „nincs a Seolban”; TAHOT 9:12 H7585 (9:10: nincs); Seolban=H7585 (`alacsony`) | `egyezik`/`alacsony`, `tartalom-alapú` |

- A `jeloltek.tsv` öt sorának `indoklas` mezője a végén `[F87: … javítva, l. naplok/KAROLI_ELTERES_ITELET_zaras.md]` hivatkozást kapott; `proveniencia`, `megbizhatosag`, `datum`, `igazolas` változatlan (az átkulcsolt sorok `TAHOT-igazolt`-ja az új kulcson igaz). Az `azonositas_modja`-t csak a `--frissit --ir` állította (1–2. sor); második futás: 0 sor.
- `adat/karoli_variancia.tsv`: két új `megerosites`-sor; a táblát az eszköz egyetlen futása írta újra (ts=2026-10-12T06:56:15Z, F87.6, az ellenőr 1. eltérése után); a ts-en kívül a többi sor változatlan. Eltéréslista újragenerálva; mellékhatás: 10 más sor új ítélete a #22 azóta párosított könyveiből (N-F87c).
- **Régi hivatkozás maradt (hatókörön kívül, kézi forrás / generált nézet):** `tematikus_lezart/Hadesz_Seol_tematikus.md` (3 hely), `motivumlog/PaRDeS_motivumok.md` (2), `lexikon/ALVIL-001_TORZSCIKK.md` (11), `lexikon/ALVIL-001_TUDOMANYOS.md` (16); a régi Károli-szó: `lexikon/TEREMT-001_*` („a mélységbe”, 2Móz 15:5), `lexikon/KIRALY-001_*` és `motivumok/KIRALY-001.md` („papok”). A lexikon újragenerálásig a régi kulcsot mutatja (N-F65b).
- **Nyitott:** N-F87a (LD008 Préd 9:10 feloldható; `forditasok.tsv` BDB-szöveg), N-F87b (KIRALY-001 2Móz 19:6 `igazolas`), N-F87c (Zak 6:13, Hab 3:10 új `elter`). N-F85c elvégezve.
