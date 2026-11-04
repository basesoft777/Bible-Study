# F123.GENKOR — az olvasói kapu mérése előtte és utána (2026-11-04)

Mérő: `python eszkozok/olvasoi_kapu.py --osszes` (BUKÁS-szám laponként). „Előtte”: a main lapjai (`845b987b`; az ALVIL-001 és az ANTROP-001 a #616 után is ugyanígy, `d88e6155`), a régi
és az új kapuval; „utána”: az ág lapjai az új kapuval. Az új kapu két szabálya szigorúbb: a BDB_JEL a betűkészlet többi
torz jelét (¹ µ £ ¥ ‰ ƒ ‡ ¢) is BUKÁS-nak veszi (DT-F181a), a BELSO a „(kézi)” / „(generált)” szerzőségi jelölést
(DT-F181c); a csupasz Strong-szám továbbra is BUKÁS, a jelölt alak nem (DT-F181b).

| Lap | előtte (régi kapu) | előtte (új kapu) | utána | ebből BELSO / BDB_JEL / ZAROJEL utána |
|---|---|---|---|---|
| ALVIL-001 | 0 | 8 | 0 | 0 / 0 / 0 |
| ANTROP-001 | 0 | 9 | 0 | 0 / 0 / 0 |
| HAMART-001 | 124 | 131 | 131 | 33 / 0 / 0 |
| HODIT-001 | 78 | 85 | 85 | 23 / 0 / 0 |
| ISTENTISZT-001 | 25 | 34 | 21 | 10 / 0 / 0 |
| KIRALY-001 | 53 | 60 | 60 | 23 / 0 / 0 |
| MENNY-001 | 45 | 52 | 52 | 21 / 0 / 0 |
| TEREMT-001 | 110 | 117 | 117 | 22 / 0 / 0 |
| TEREMT-002 | 17 | 25 | 16 | 5 / 0 / 0 |

- **ISTENTISZT-001 a #623 behozása után: 0 BUKÁS** (6 FIGYELMEZTETÉS). Mérve egy repón kívüli worktree-ben: az ág +
  `origin/claude/suspicious-rubin-389e3a` (a #623 feje, `8055bfcf`) összefésülve, a lap ütközése a #623 oldalával
  feloldva, majd `PARDES_DATUM=2026-11-03 python eszkozok/general.py --cel lexikon --id ISTENTISZT-001 --ir`. A main-en
  álló 21 BUKÁS mind a kézi prózában van, és mind a #623 javítja; a négy generátor-bukás (C1 BDB_JEL, C2–C3 ZAROJEL, B1
  Strong) ezen az ágon megszűnt.
- **Az öt nem migrált lap** (HAMART-001, HODIT-001, KIRALY-001, MENNY-001, TEREMT-001) a main változatán maradt: az
  újragenerálás a CI E9-et (angol „sense” az adatban) és az E5-öt érintené (N-F181a). Az új kapu rajtuk lapnként 7
  szerzőségi jelölést mér (a „(kézi)” címsorok); a tartalmuk nem változott. Próbagenerálással (repón kívül) a BUKÁS mind
  az ötön csökkenne: 131 → 103, 85 → 63, 60 → 36, 52 → 31, 117 → 89.
- **A kiadott lapokon (ISTENTISZT-001, ALVIL-001, ANTROP-001) csak generált rész és jelölés változott:**
  `python naplok/GENKOR_dt569_igazolas.py` — a kézi sorok normalizálva (címsorjelölés, olvasói bevezető, Strong-jelölés)
  azonosak: 434 / 434, 144 / 144, 147 / 147 sor, 0 eltérés.

## A C1–C3 hibafajta kiterjedése (`adat/bdb_szakaszok.tsv`, `adat/bdb_szakasz_hu.tsv`)

| Mérés | Érték |
|---|---|
| a torz betűkészlet valamely jele (® ° ¹ µ £ ¥ ‰ ƒ ‡ ¢ †) az angol forrásszövegben | 422 Strong, 427 BDB-szócikk |
| ebből a kapu jeleivel (® ° ¹ µ £ ¥ ‰ ƒ ‡ ¢) | 405 Strong; a „®” 33 Strongja (Seól-család, DT581) javított, 372 javítatlan (N89) |
| jelenként (Strong) | ® 33 · ° 68 · ¹ 47 · µ 29 · £ 12 · ¥ 10 · ‰ 77 · ƒ 113 · ‡ 105 · ¢ 11 · † 30 |
| a lapokon, a ® / °-on túl | 1 hely: ANTROP-001 „Leµi” (H2416) — kézi `atiras` sorral javítva |
| nyitott zárójel az angol szakaszsorban | 1 149 sor, 843 Strong (nagy része szakaszhatáron átnyúló zárójel) |
| a vázlatsor nyitott zárójele (magyar szakasz) | 3 212 sor / 2 874 szócikk → 5 sor / 5 szócikk (zárójel-tudatos vágás) |

A H7121 hibái (C1–C3) a nyers forrásban állnak: a DictBDB.json és a BDB.lexicon ugyanígy hordozza őket („(the
'†or°¹n), the †or°a¹n”, „be read aloud compare Qal 4 )”, „be summoned (compare Qal 5 : Isa 31:4”); a konverzió
(`_convert_bdb.py`, `bdb_szakaszok.tsv`) és a fordítás (`forditasok.tsv`, `bdb_szakasz_hu.tsv`) híven vitte tovább. A
H8034 5. pontjának nyitott zárójele (C3) generátorhiba volt: a vázlatsor a zárójelen belüli „;”-nél vágott.
