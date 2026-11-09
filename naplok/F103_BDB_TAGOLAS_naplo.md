# F103 — BDB_TAGOLAS: munkanapló

*FELADATOK #103 · ág `claude/f103-bdb-tagolas` · végrehajtó: `claude-opus-5-5` (kért: `opus`) · 2026-11-09*

Mérőszkript: `naplok/F103_BDB_TAGOLAS_meres.py` (előtte és utána ugyanez; csak olvas, a `--tsv` a régi alakok listáját írja a
`naplok/`-ba). A mérések definíciója a szkript docstringjében. Az aranyminta 184 `csoport` sora a teszteset (brief 3./1.).

## 1. Előtte-mérés (F103.1)

*proveniencia: scope=aranyminta (adat/bdb_aranyminta.tsv) + teljes angol BDB (8099) + magyar BDB (8099) | forras=BDB_teljes_unabridged.tsv@d4b15b2faea6
+ forditasok.tsv@0be309b96bc3 + bdb_aranyminta.tsv@ea74da96324d + bdb_szelet.py@dc48b1a0af51 (HEAD 3e6ed664) + naplok/F103_BDB_TAGOLAS_meres.py | ts=2026-11-09T19:01*

| mérés | előtte |
|---|---|
| aranyminta, angol: várt csoport | 184 |
| egyező csoport | **0** (a szeletelő nem bont csoportra) |
| hamis határ (angol) | 0 |
| aranyminta, magyar: várt bontás (szülő-csomópont, ahol minden angol csoportnak van magyar horgonya) | 47 |
| magyar bontás | 0 |
| jelentéspont, seed-102 véletlen 200 (`m2_minta_osszevet.py --mai-tabla`) | **183** (91,5%) — azonos a #102 zárómérésével |
| könyv/vers, seed-102 | 199 |

A magyar BDB ma 8099 szócikk (a DT167 idején 674): a 2. pont „674 kész szócikk” mérése a mai teljes magyar állományon fut.
