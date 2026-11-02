# THAYER_B_UT napló — F159 (a Thayer-kötegelő B-útja, szűkített adatblokk, kalibrált becslő, mérő batch)

*Modell: claude-sonnet-5-5 (a brief `modell: sonnet`-jével egyezik). Ág: `claude/f159-thayer-b-ut-83b0a2` (main `0c597b1e`). A mért értékek forrása: `forditas/thayer_api/adag1591/` (effort=high) és `adag1592/` (effort=medium) `futasnaplo.tsv`, `valaszok.jsonl`, `kapu_eredmeny.jsonl`; proveniencia: `scope=60 Strong (naplok/THAYER_B_UT_mero_strongok.txt) | forras=thayer_api_koteg.py bbekuld/begyujt/kapuz/javit | ts=2026-11-02`. Ami nem mért, `manual`-lal jelölt.*

## 1. Felmérés: a `bdb_api_koteg.py` B-útjából mi vehető át

| Elem | Állapot |
|---|---|
| `b_prompt`, `b_csoportok_epit`, `b_szetbont`, `json_tomb`, `kot_unio` | átvéve, a Thayerre igazítva (Strong-szám és karakterkorlát, `Thayer-szócikk` szöveg, a szabály-rész a `forditas.prompt_epit`-ből, nem másolat) |
| `bbekuld` plafonja | **új**: a BDB becslés-alapú plafonjával szemben a mért futó összeg + a másik adag mért költsége + a be nem gyűjtött batchek beküldéskori becslése + az új becslés (N-F27b) |
| becslő | **új**: kalibrált (N-F27a), a kérésenkénti állandót a szűkített prompt adja |
| terminológia- és Károli-tábla szűkítése | **új** (BDB-ben nincs) |
| `effort` | **új**: `--effort high|medium` (a `bdb_api_koteg.py`-ban konstans, ezért a Thayerben saját `kerelem_params`) |
| javító kör | a bukott/hiányzó Strong egyenként (A-stílus); ha nincs mit javítani (üres B-válasz-objektum), friss kérés assistant-forduló nélkül |

A `bdb_api_koteg.py`, az `api_koteg.py`, a `thayer_jelolt/` eszközei és a `prompt_v5_1.md` változatlanok (`git diff main --stat`: csak a `thayer_api_koteg.py` és a tesztje).

## 2. Az adatblokk szűkítése (2. követelmény)

Szabály: a terminológiából azok a sorok maradnak, amelyek angol kulcsa a kérés forrásainak (nézet) uniójában illeszkedik (`forditas_kapuk._angol_minta`, az 5. kapu illesztése, a `kapu=nem` sorokkal együtt); a Károli-táblából az a sor, amelynek STEPBible-rövidítése, forrás-alakja vagy angol könyvneve (`Angol_konyvnev_STEPBible_tabla.tsv`) szerepel a forrásban. A rövidítés-feloldást a `normalizal.py` utólag gépileg is végzi, ezért a Károli-tábla szűkítése alacsony kockázatú. A teszt (`test_szukites_pontos_sorhalmaz`) ellenőrzi: a szűkített blokk a kérés minden releváns sorát tartalmazza, mást nem; a kötelező-alak lista (5. kapu) minden kulcsa benne van.

| Állandó rész kérésenként (szabályok, terminológia, Károli, séma, példa) | karakter | token |
|---|---|---|
| szűkítés előtt (G25 egy Strongos kérés; F27 M1 mért 17 136 token) | 36 257 | 17 136 |
| szűkítés után, egy Strongos kérés (G25 / G1941) | 26 463 / 29 398 | kb. 12 500 (`manual`) |
| szűkítés után, B-kérés (a mérő adag első 3 kérése átlaga) | kb. 22 000 | kb. 10 400 (`manual`; mért: 11–14 ezer, l. 5. pont) |

## 3. Száraz becslés a mérő adagra (5. lépés ⛔ előtt)

60 Strong (41 kicsi, 19 közepes, 32 718 forráskarakter) a `naplok/FP3_sorrend.tsv`-ből egyenletes lépésközzel (az M1 nélkül); B-út, 20 Strong / 16 000 karakter / kérés → 4 B-kérés (13, 20, 20, 7 Strong). Becslés (`manual`, kalibrált, Batch-ár, cache nélkül): **0,77 USD ágankénti** (a becslő az effortot nem különbözteti meg), kb. 1,6 USD összesen ≤ 4 USD → a ⛔ feltétel nem állt, a beküldést az orkesztrátor jóváhagyta (üzenet, 2026-11-02: „a javaslatod 1–4. pontja szerint”).

## 4. Mért összevetés (mérő batch, valódi beküldés)

Mindkét ágon ugyanaz a 60 Strong és ugyanaz a csoportbontás (`b_csoportok.json` másolva). Modell a Batch-válaszból: `claude-sonnet-5-5`. Az `adat/forditasok.tsv` nem változott, a `beir`/`rogzit` nem futott.

| | effort=high | effort=medium |
|---|---|---|
| B-batch | `msgbatch_01RLYh5N9HyrGeGXW7uEB5TX` | `msgbatch_01UTN1nuoCvvvtXnydoQLDXM` |
| javító batch | `msgbatch_011JLtF14rip7TAyfMz67WBe` (8 kérés) | `msgbatch_01YL8E9Dj8rgSvP8sKjssYi8` (7 kérés) |
| 1. kör: bemenet token | 161 687 | 161 687 |
| 1. kör: kimenet token (gondolkodással) | 67 328 | 49 111 (−27%) |
| 1. kör költsége (mért) | **0,4983 USD** | **0,4072 USD** |
| javító kör: bemenet / kimenet token | 110 792 / 9 226 | 100 116 / 4 912 |
| javító kör költsége (mért) | **0,1569 USD** (8 kérés, 0,0196/kérés) | **0,1247 USD** (7 kérés, 0,0178/kérés) |
| **összesen (mért)** | **0,6552 USD** | **0,5319 USD** |
| USD / 1000 forráskarakter (1. kör / összesen) | 0,0152 / 0,0200 | 0,0124 / 0,0163 |
| USD / Strong (1. kör / összesen) | 0,0083 / 0,0109 | 0,0068 / 0,0089 |
| max_tokens (beállított / használt kimenet, B001–B004) | 64 000, 64 000, 64 000, 39 489 / 25 366, 22 664, 14 311, 4 987 | ugyanaz / 21 418, 16 484, 9 433, 1 776 |
| stop_reason | mind `end_turn` | mind `end_turn` |

**Mért teljes költség: 1,187 USD ≤ 4 USD** (K3). Összehasonlításul az F27 M1 egy Strongos útja a kicsi Strongokra 0,071 USD / 1000 karakter volt (`naplok/FP3_naplo.md`); a B-út összesen 0,016–0,020, vagyis a kicsi/közepes Strongokon kb. 3,5–4,3-szer olcsóbb (a minta kicsi: 60 Strong).

### Kapubukás (Strong-szinten, kapunként)

| | high | medium |
|---|---|---|
| 1. kör: bukott Strong | **8 / 60 = 13,3%** | **7 / 60 = 11,7%** |
| `11_konyvek` (apokrif könyvnevek: Makk, Tób, Judit) | 4 (G2837, G0163, G5009, G2253) | 4 (G2837, G0163, G5009, G2253) |
| `16_sigla` | 2 (G5009, G5086) | 4 (G2837, G0163, G5009, G5086) |
| `9_tagolas` | 2 (G4270, G5086) | 2 (G4270, G5086) |
| `8_idezojel` | 1 (G2722) | 2 (G2917, G5009) |
| `4_formazas` | 1 (G1463) | 0 |
| javító kör után bukott (a kétszer bukott) | **0 / 60 = 0%** | **4 / 60 = 6,7%** (G2837 `11_konyvek`, G4270 `9_tagolas`, G5009 `16_sigla`, G5086 `9_tagolas`) |

A medium első körös bukása nem rosszabb a high-énál (−1,7 pontnyi), a javító kör után 6,7 százalékponttal rosszabb → **a 10 pontos megállási feltétel nem teljesül**. A bukások ágak között nagyrészt azonos Strongokra esnek (G2837, G4270, G0163, G5009, G2253, G5086 mindkettőn), tehát forrás- és kapu-specifikusak (apokrif könyvnevek, szakaszhatár-jelölők, siglák), nem az effort vagy a B-út következményei; ezt egyenként a #7 briefje vizsgálja. Második javító kört nem futtattam (a brief: első + javító kör).

### A B-út saját kockázata: visszabontási hibák (külön sor)

| | high | medium |
|---|---|---|
| B-kérés válaszában hiányzó Strong-objektum | **0 / 60** | **0 / 60** |
| idegen vagy kétszer szereplő `strong` | 0 | 0 |
| objektumszám = csoportméret (13, 20, 20, 7) | igen mind a 4 | igen mind a 4 |
| helyőrző-hiba (hiányzó/többszörös ⟦n⟧) a kapuk előtt | 0 | 0 |
| max_tokens / refusal / hibás válasz a B-kérésen | 0 | 0 |

Egyetlen Strong sem hiányzott, nem folyt össze másikkal; a Strongonkénti kapuk minden Strongra lefutottak. (Az összefolyás közvetlen jele a helyőrző-hiba és a szakaszhatár-token hiba lenne; ilyen nem fordult elő. A 9_tagolas-bukások két Strongon mindkét ágon azonosak, ezért nem csoportos keveredésre, hanem a forrásra vallanak.)

## 5. Újraillesztett együtthatók (a 4 B-kérésre, legkisebb négyzetek, `manual`: 4 pont)

| | F27 M1 (egy Strongos, szűkítés nélkül) | B-út, high | B-út, medium |
|---|---|---|---|
| bemenet token / kérés | 17 136 | **14 426** | 14 426 |
| bemenet token / forráskarakter | 3,721 | **3,178** | 3,178 |
| kimenet token / Strong | (1 134 / kérés) | **343** | **74** |
| kimenet token / forráskarakter | 1,654 | **1,452** | **1,411** |

Az illesztés 4 ponton áll, a Strongonkénti kimeneti állandó nem megbízható (a high 343, a medium 74: a két paraméter együtt mozog), az összkimenet jó becslő: kb. 1 120 (high) és 820 (medium) token / Strong ezen a mintán. A bemeneti állandó (14,4 ezer token) a szűkített szabály-részé a kérésben, nagyobb a száraz 10,4 ezernél; a kalibráció tehát konzervatív volt a bemenetre (a becslő 0,77 USD, a mért 0,50/0,41 első körös). Az `ALLANDO_REF_KAR`, `BE_*`, `KI_*` konstansokat a #7 előtt a nagyobb mintával kell újraillesztetni; most nem írtam át őket (a mérő eredmény N-F27a lezárásához a mért értékek ebben a naplóban vannak).

## 6. Kivetítés a teljes Thayerre a B-úttal (`manual`, 60 Strong mintából)

Alap: 5 385 fordítandó Strong; kicsi/közepes 5 176 Strong (3 288 + 1 888), 2 914 221 forráskarakter, 289 B-kérés (20 Strong / 16 000 karakter); nagy/többcsoportos 209 Strong, 233 kérés, 1 474 862 karakter. A kicsi/közepes B-kérés költsége a 5. pont együtthatóival; a javító kör a mért arányokkal (high 13,3%, medium 11,7% Strongonként, a mért javító-kérés költségével); a nagyra **nincs mérés**: ott a mért bemeneti együtthatók, az M1 kimeneti illesztése (1 134 / kérés + 1,654 / karakter) és a mért javító arány, a medium kimenete a mért 0,729-es medium/high kimeneti aránnyal; ez extrapoláció, a nagy Strongok bukása valószínűleg magasabb.

| Kategória | high: 1. kör + javító | medium: 1. kör + javító |
|---|---|---|
| kicsi (3 288 Strong, 894 191 kar.) | 17,62 + 8,60 = **26,22** | 13,02 + 6,83 = **19,85** |
| közepes (1 888 Strong, 2 020 030 kar.) | 25,84 + 4,94 = **30,78** | 22,89 + 3,92 = **26,82** |
| nagy (209 Strong, 233 kérés; extrapoláció) | 21,57 + 0,61 = **22,18** | 17,91 + 0,48 = **18,39** |
| **összesen (USD, `manual`)** | **79,2** | **65,1** |

Összevetés: az F27 M1 egy Strongos útja 207–311 USD; a brief 79–113 USD-s B-út becslése; a kivetítés **79 (high) / 65 (medium) USD < 130 USD** → a megállási feltétel nem teljesül. A kivetítés bizonytalansága: a mérő minta 60 Strong (±), a kicsi/közepes kategória költségének kb. harmada a javító körből jön (egy Strongos javító kérés a teljes szabály-részt újra viszi: 13–14 ezer bemeneti token) → a #7 briefjének mérlegelnie kell a javító kör csoportosítását (B-stílusú javító kör), ami a kicsi/közepes javító költségét (high 13,5, medium 10,8 USD) jelentősen csökkentené. Számítás: `eszkozok`-on kívüli scratch-szkript (`proj.py`), az együtthatók és arányok ebben a naplóban teljesek.

## 7. Zárás

- N-F27a (becslő a mért modellre): a kalibrált együtthatók a kötegelőben (M1 illesztés) és az újraillesztés az 5. pontban → lezárásra javasolt.
- N-F27b (mért futó összeg a plafonban): `plafon_ellenorzes` + tesztek → lezárásra javasolt.
- N-F27d (prompt-cache) kívül marad. A max_tokens-bukások (G1722, G1510, G4151) a #7-é.
- Döntés-helyőrző javaslat a #7 briefjéhez: `effort=medium` a kicsi/közepes B-úton (−18% költség, első körös bukás nem rosszabb, de a javító kör után 4 / 60 marad) vs `high`; csoportméret 20 Strong / 16 000 karakter; a javító kör B-stílusú csoportosítása.
