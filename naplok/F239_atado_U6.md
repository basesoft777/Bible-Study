# F239 átadó — U6 (egy javítókör) → a szerkesztő változásnézése, majd U7 (a 218c után)

*2026-11-23 · író: `claude-opus-5-5` (kért: `opus`, egyezik) · ág: `claude/nervous-kare-9d2361` (PR #820). A javítás és a kapuk: `naplok/F239_jelentes.md`, „U6”; az érvek: `naplok/ERVNAPLO_TEREMT-001.md` D4; a döntések: `naplok/F239_dontesek.md` D2–D26.*

## Mi kész

- A szerkesztő U5-döntései (D2–D26) szó szerint a döntésnaplóban (F239.36).
- A próza javítóköre egy kézben, a teljes próza újraolvasásával (F239.37): a `motivumok/TEREMT-001.md` négy rése és az `adat/elofordulasok.tsv` négy 1/a-sora; a hibahely-tábla 37 sora (H1–H37) a jelentésben. A (b) csoport mind a 14 tétele (L17, O7, F2: K2, K9, K19, K20, K36, K47, K69, K70, K99; F1 79.; a független ellenőr két eltérése) javítva.
- D25 (F239.38): a Chain Lineage-tanúk kora a HCF-évből; a gyökérok (a CL `century` a születési század) a kinyerőben kezelve, teszttel; a Hippolütosz-sor is (ugyanaz a mechanizmus).
- F2 a javított helyeken (friss `allitas-ellenor`, 65 állítás): 52 igazolt, 4 hamis, 8 vitatott, 1 nem eldönthető. A korábbi kilenc hamis tétel új szövege mind igazolt; a 13 kifogás az U6 új mondataiban állt, és ugyanabban a körben javult (H38–H49, F239.39), független újramérés nélkül.
- Kapuk az előnézeten (a H38–H49 után): 1/a 43/43; olvasói kapu 7 BUKÁS / 23 FIGYELMEZTETÉS, ugyanannyi, mint az U5-előnézeten, a prózában 0 BUKÁS; E41 zöld (ELTÉR 0); `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba.

## A szerkesztő elé

- **Változásnézet** (a repón kívül, nem publikálva): `C:\Users\bases\AppData\Local\Claude-Data\claude_pzs8sxrjxfjjc\side-session-notes\local_911d4923-53b0-4b46-9fc5-ccdde3608420\F239_U6_TEREMT-001_valtozas.html` — 33 változott blokk az U5-előnézethez képest, előtte–utána párban, szószintű kiemeléssel (a csak a generálási bélyegben eltérő blokkok kihagyva). Az U6-előnézet ugyanott: `F239_U6_elonezet/lexikon/`.
- **`adat/lap_javitasok.tsv`:** nem írtam bele sort. A szerkesztő a döntések irányát hagyta jóvá, a konkrét új szöveget még nem látta; a `jovahagyta` mezőbe csak a változásnézet utáni, szó szerinti jóváhagyás kerülhet (`/lap-javit` 4. pont, `ellenoriz.py` 30.).

## Nyitott, gazdával

- A (c) csoport (N-F239c, 112 generátorhiba) a 218c-é (#241). Az olvasói kapu 7 bukása ennek része.
- A kiadás feltételei változatlanok: N-F239a, N-F239b (218c), a BDB-versjelentés hibája (#240), N-F240a (πόντος → „Pontusz”).
- A döntésnapló fejlécében (az integrátor szövege, szó szerint átvéve) „A D24 és a D25 a motívum határának szövegéről szól” áll, a határ-döntés viszont a D26; az integrátornak jelezve.

## Mit NEM kell elolvasni

Az U6 diffjét a hibahely-tábla összefoglalja; a `naplok/F239_U6_*.py` szkriptek a commit-üzenetekben leírva.
