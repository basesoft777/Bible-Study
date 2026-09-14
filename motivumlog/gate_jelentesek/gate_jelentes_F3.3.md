<!-- GENERÁLT: eszkozok/gate.py — kézzel szerkeszteni tilos, a forrás (adat/motivumok.tsv + adat/elofordulasok.tsv) változása után újragenerálandó -->

# gate.py — ütközés- és részhalmaz-jelentés

Generálva: `eszkozok/gate.py`, ts=2026-09-14T07:47Z

Vizsgált motívumok (7 db, az `adat/motivumok.tsv`-ben és az `adat/elofordulasok.tsv`-ben egyaránt jelen lévők): ALVIL-001, ANTROP-001, HODIT-001, ISTENTISZT-001, KIRALY-001, MENNY-001, TEREMT-001

**Ez a fájl kimenet, nem döntés** — minden ütközés/részhalmaz-gyanú a 4.6 gate négy kérdése szerint emberi mérlegelést igényel (l. `ATALAKITASI_TERV.md.md` 4.6).

---

## 1. Ütközés-jelentés — motívumpáronként osztozó igehelyek

| A | B | osztozó igehelyek (n) | igehelyek |
|---|---|---|---|
| ALVIL-001 (Hádész (Seól) — a halottak birodalma) | HODIT-001 (Rafeusok/óriás-népek) | 2 | Péld 9:18; Ézs 14:9 |
| ALVIL-001 (Hádész (Seól) — a halottak birodalma) | TEREMT-001 (Tehóm (תְּהוֹם) — Abüsszosz (ἄβυσσος): a mélység motívuma) | 1 | Ez 31:15 |
| HODIT-001 (Rafeusok/óriás-népek) | MENNY-001 (Isten fiai — Nefilim — Gibborim motívum-komplexum) | 1 | 4Móz 13:34 |

## 2. Egy igehelyen osztozó motívumok — vers-központú nézet

| Igehely | Motívumok |
|---|---|
| 4Móz 13:34 | HODIT-001, MENNY-001 |
| Ez 31:15 | ALVIL-001, TEREMT-001 |
| Péld 9:18 | ALVIL-001, HODIT-001 |
| Ézs 14:9 | ALVIL-001, HODIT-001 |

## 3. Részhalmaz-ellenőrzés — B ⊆ A (B minden igehelye A-ban is megvan)

A 4.6 gate 4. kérdése: *ha B minden előfordulása benne van A-ban, B nem új ID, hanem A alpontja.* Az alábbi sorok jelzések, nem döntések — egy egyetlen közös igehely (n=1) önmagában nem indokolja az alpont-besorolást, csak akkor releváns, ha B teljes (nem csak egy-két elemű) halmaza esik A-ba.

Nincs B ⊆ A viszony egyetlen motívumpár között sem.

## 4. Hatókör — mely ID-k maradtak ki

Minden `motivumok.tsv`-beli ID-hez van legalább egy `elofordulasok` sor.
