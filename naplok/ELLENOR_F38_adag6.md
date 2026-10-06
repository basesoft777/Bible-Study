# ELLENOR_F38_adag6 — független ellenőrzés

- Brief: `F38_BDB_FORDITAS_BRIEF.md`
- Tartomány: `origin/main..HEAD` = `bdae91d..0ba75ea`, ág `claude/f38-adag6` (43 commit)
- Az ellenőr nem írhatott; a jelentést az orkesztrátor mentette, tartalmilag változatlanul (az OK sorok összevonva). A kapuk, `ellenoriz.py`, `forras_hash`, karakterszámok és tesztfuttatás az ellenőr szerepében nem futtathatók (NEM ELLENŐRIZHETŐ).
- Eredmény: **ELTÉRÉS, 4 tétel**

## Eltérések súlyossági sorrendben

1. **Gyökcsoport-mérés, módszerhiba** (`naplok/BDB_FORDITAS_gyokcsoport_meres.py:60`, `adat[r['strong']] = (gyok, t)`): az OSHL-indexben 8 581 héber sor, de csak 7 990 egyedi Strong; az ismétlődő sorok közül az utolsó felülírja a korábbiakat. Igazolt eset: H1121 (`254 b.ca.aa` és `— b.ca.aj`) → a kimenetben TWOT „—”, és mind a 23 BDB-rokon `csak_bdb`. A számok a kimenettel egyeznek, de a DT-F38j (c) alapja (71,0%, 2 532 TWOT nélküli) torzított lehet.
2. **„A H5674-teszthibák nem e menet okozták” hiányos** (`DONTESEK.md:60`, `naplok/F38_zaras.md:6`): a `teszt_bdb_zaras.py:182` `test_szellem_tabla_nagybetus_helyei` a H6743 (Bír 14:6 „a Szellem …”, `forditasok.tsv:671`) miatt is bukik, mert a `SZELLEM_KOVETELT` nem ismeri; ezt az ág okozta, a main-ről öröklött H5674-bukás elfedi. Kódolvasásból levezetve.
3. Tétel-granularitás: a F38.311 mérés a `F38.310a` commitban van, F38.311 előtagú commit nincs (alacsony).
4. A záró commit formátuma eltér a brief 3. megállási pontjától (`F38.354: …` a `BDB_FORDITAS adag <n>: …` helyett); az 5. adag is így volt (alacsony).

## Rendben (saját lekérdezéssel)

- `adat/forditasok.tsv`: +242, 0 törlés; a régi 497 sor bájtra azonos; a 242 sor = a sorrend-tábla `adag=6` sorai (H0123–H6466), duplikátum nincs; séma/proveniencia (`sonnet`, `claude-sonnet-5-5`, 2026.10.06, v3) 242/242.
- Kész 648, hátra 7 416 (8 090 − 26 − 648).
- Más `adat/*.tsv`, `konkordancia/*.tsv`: Δ=0; a `BDB_teljes_unabridged.tsv`, szerepmátrix, `terminologia.tsv` nem változott; a gyökcsoport import nélkül maradt (DT-F38j (c) nyitott).
- H3289 „Náh 7:5”, H7927, H5341: hű forrásátvétel (lekérdezéssel); a hat terminológia-kivétel pontosan hat; Szellem-tartalom (H6743) a forrás szerint nagybetűs; D11 hangrendi hiba 0.
- DT-F38j: 🟡, 8 oszlop, helyőrző; a brief fejléc csak `allapot`/`ag`/`kovetkezo` változott.
- `futtat.py --valtozott`: E2–E16, E19, E26: 0; E25 3 régi találat; `--teljes`: HIBA nincs.
