# F224.13 — az elfogadási próba bemenetei

*Mentette: claude-opus-5-5, 2026-11-15. A bemenet-mappát az ügynökök a repón kívül (a session scratch-könyvtárában) kapták; itt a másolata áll, a forrásfájlok nélkül, amelyek a megnevezett commitból újra előállnak.*

| Mappa | Tartalom | Eredet (proveniencia) |
|---|---|---|
| `meres_2026-11-15/` | a 2026-11-15-i visszajátszás mellékletei: a 8:21-es érvvázlat és bizonyítéklap (a bíráló-próba bemenete, változatlanul), a régi Sonnet-bíráló és a régi F2 kimenete (az összevetéshez) | `scope=MERES_VISSZAJATSZAS_mellekletek/ (6 fájl) \| forras=az orkesztrátor megosztott jegyzetmappája (local_20eed447…), másolás változtatás nélkül \| ts=2026-11-15` |
| `ham/` | a HAMART-001 kézi listája az új kinyeréssel (118 K-tétel) és a két szelet K-listája | `scope=motivumok/HAMART-001.md, adat/elofordulasok.tsv, adat/kapcsolatok.tsv, lexikon/HAMART-001_TUDOMANYOS.md @f6da955e \| forras=python naplok/F224_proba/klista.py (eszkozok/proza_allitas.py, az ág feje) \| ts=2026-11-15` |
| `ist/` | az ISTENTISZT-001 kézi listája az új kinyeréssel (58 K-tétel) | ugyanígy, `@b2aea73f` |
| `dist/` | az ISTENTISZT bíráló-próba bemenete: a három vitatott pont szó szerint és a rájuk támaszkodó mondatok (gépi kivonat), a bizonyítéklap | `forras=python naplok/F224_proba/ervvazlat_kinyer.py ISTENTISZT-001 … @b2aea73f (forrás, elofordulasok, jeloltek)` |
| `d821/` | a 8:21-es bizonyítéklap az F224.5 eszközével | `forras=python naplok/F224_proba/bizonyitek_821.py (elofordulasok, jeloltek @f6da955e)` |

**Az ügynököknek adott, itt nem másolt fájlok** (újraelőállítás: `git show <commit>:<út>`): `ham_forras.md` = `motivumok/HAMART-001.md @f6da955e`; `ham_elofordulasok.tsv`, `ham_kapcsolatok.tsv` = `adat/elofordulasok.tsv`, `adat/kapcsolatok.tsv @f6da955e`; `ist_forras.md`, `ist_elofordulasok.tsv`, `ist_kapcsolatok.tsv` ugyanígy `@b2aea73f`. A K-listák hely-hivatkozásaiban a fájlnév `ham_forras.md` / `ist_forras.md` (a sorszám a forrásé).

**Vak szabály** (minden ügynöknek): nem nyithatta meg a `naplok/`, `lexikon/`, `motivumok/`, `archivum/`, `generalt*/` mappát, a git-történetet és a jegyzetmappákat; a motívum saját sorait a bemenet-mappából olvasta. A `konkordancia/` és a szótári `adat/*_vers_jelentes.tsv` megengedett volt (a 2026-11-15-i méréssel azonosan).
