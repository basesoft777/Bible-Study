ELTÉRÉS: 5 tétel (ebből 2 a jelentés után javítva, l. „Utólagos ellenőrzés és javítás”)
# ELLENOR_LXX_BRIDGE — F43_LXX_BRIDGE_BRIEF.md · ece75b71328fcd5e16f6b333c8f06d912493de0f..4b79671

*A `fuggetlen-ellenor` jelentése (fájlíró eszköz híján az orkesztrátor mentette változatlan tartalommal); az utolsó szakaszt az orkesztrátor írta.*

| pont | eredmény | fájl:sor | parancs / indok |
|---|---|---|---|
| Hatókör | OK | – | `git diff --name-status B..4b79671`: M DONTESEK.md, M F43_LXX_BRIDGE_BRIEF.md, M adat/kulso/LICENC.md, A eszkozok/lxx_bridge_egyezes.py, A naplok/LXX_BRIDGE_egyezes.tsv, A naplok/LXX_BRIDGE_naplo.md. A brief `ir` listáján kívül csak a DONTESEK.md és a brief fejléce változott (l. ⛔-sor). |
| (1) / D2 / Elfog. 3 | OK | `adat/lxx_dontesek.tsv` | `git diff B..4b79671 -- adat/lxx_dontesek.tsv`: 0 bájt. |
| (2) Determinizmus / Elfog. 6 | NEM ELLENŐRIZHETŐ (az ellenőrnek) | `eszkozok/lxx_bridge_egyezes.py` | Futtatás nem megengedett parancs. Kódolvasás: rendezett glob, rendezés `(-count, G)` kulcsra, kimenet listasorrendben, hálózati import nincs. Lappangó kockázat: a 228. sor `next(iter(sz_ok))` halmazon fut; több eltérő `strong_ok` érték esetén hash-seedfüggő lehet. A mostani kimenetben (LD058, LD064) egyetlen érték áll. |
| (3) Kategóriaszámok | OK | `naplok/LXX_BRIDGE_egyezes.tsv:3-88` | Grep count: egyezik 24, elter 3, nincs_adat 46, nem_alkalmazhato 8, nyitott_jelolt 4, lxx_minusz_osszhang 1 = 86. Bizonyosság×kategória: biztos 23/3/35; valószínű 1/1/11; nyitott 4; n.a. 8 — egyezik a napló 4. szakaszával és a DT23 61/13/4/8 arányával. `vers_strong_hiany` összege 167, 64 nem nulla soron. |
| (4) Szúrópróba | OK | `adat/kulso/lxx_bridge.tsv:37-38,463-466,932-934,999-1002,1346-1347,2915-2916,3235` | H2555 → G0093:10, G0094:10, G0763:8, G0458:6; H1121 → G5207:3957, G3588:58, G5043:54, G1537:32; H8415 → G0012:24. Versszint (LXX_OS): Gen 4:7 G0264+G3588, G0266 nincs (LD017 elter ✓); Job 1:6, 2:1 G0032+G3588, υἱός nincs (LD084/085 elter ✓); Gen 6:2 G5207 (LD082 ✓); Mic 6:12 G0763 (LD035 ✓); Ex 19:6 nincs G2409 (LD080 nincs_adat ✓); Isa 7:11 G1519, G0899 (LD009 ✓). |
| (5) TSV-olvasás | OK | `eszkozok/lxx_bridge_egyezes.py:74-81,301-306` | `split('\t')` / `'\t'.join`; `csv` csak a docstringben. |
| (6) DT-F43 – LICENC – napló 8. | ELTÉRÉS (közepes) → JAVÍTVA | `naplok/LXX_BRIDGE_naplo.md:81,93`; `DONTESEK.md:79`; `adat/kulso/LICENC.md:9-11` | A LICENC Forráspolitika-szövege szó szerint egyezik a napló 8(d)-vel. A napló viszont elavult volt („NEM beírva”, „felfüggesztve”). |
| ⛔ (brief 5. lépés) | ELTÉRÉS (közepes) | `DONTESEK.md:79`, commit 943cdf8 | A brief: „a döntési javaslatot a napló végére írd, a DONTESEK.md-be ne”; az F43.4 mégis beírta (a CLAUDE.md menetszabályával ütközés miatt). A megállás megtörtént. Az F43.5 a felhasználó chatben hozott döntését rögzíti; ez lekérdezéssel nem ellenőrizhető. |
| Elfog. 5 | ELTÉRÉS (alacsony) | `naplok/LXX_BRIDGE_naplo.md:13,34,51` | A `nincs_adat` 31/14/1 bontása és a 167/64 nem a napló parancsából jön, a 13. sori grep-ből hiányzik a H7043. Saját lekérdezéssel az értékek helyesek. |
| A2 / D7 | ELTÉRÉS (alacsony) | `NYITOTT_FELADATOK.md:343` | A D7 szerint az N29 lezárandó ezzel a döntéssel; nyitva maradt. A NYITOTT_FELADATOK.md nincs az `ir` listán — a brief hiánya. |
| Git-konvenció | ELTÉRÉS (alacsony) | `git log B..4b79671` | Az `F43.2:` előtag két commiton (6ea23be, 0dd7625), és az első megelőzi az F43.1-et. |
| D1, D3, D4, D5, D6 | OK | – | D3: `egyezik` csak `dg in vers_g` esetén; D4: 86 sor `OS+kivonat`, forrás mindenhol LXX_OS; D5: 3302 sor = fejléc + 3301 (SHA-256 nem ellenőrizhető az ellenőrnek); D6: nincs tiltott forrás a diffben. |
| Elfog. 1–2 | OK | – | LD005–LD090 hézag nélkül, 86/86; 3301 sor igazolva (az egyedi Strong-számok nem újraszámolva). |
| A1 | OK (megjegyzéssel) → JAVÍTVA | `DONTESEK.md:79` | A DT-F43 „a חָמָס szokásos megfelelője az ἀδικία” állítása túlzó: a bridge-ben ἀδικία 10 = ἄδικος 10 > ἀσέβεια 8. |
| A3–A5 | nem alkalmazható | – | – |
| A6 | OK | – | `futtat.py --valtozott <6 fájl> --diff-alap B --diff-fej 4b79671 --esemeny pull_request`: E2–E16, E19 0 találat. A `--teljes` jelzései a változott fájlokon 0. |
| Lista 1–4 | OK | – | Törlés csak a brief 2 fejlécmezőjében; kulcstartomány 86/86; nulla-diff hatóköre csak `adat/lxx_dontesek.tsv`; tábla-Δ: csak `adat/kulso/LICENC.md` +4, E17 küszöb nincs átlépve. |

**ELTÉRÉS-ek súlyossági sorrendben:**
1. (közepes) ⛔: a DT-F43 a brief tiltása ellenére került a DONTESEK.md-be (F43.4).
2. (közepes) A napló 8. szakasza elavult a ✅ DT-F43-hoz képest. → javítva
3. (alacsony) Elfog. 5 részben: néhány naplószám nem a napló parancsából reprodukálható (az értékek helyesek).
4. (alacsony) Az N29 nyitva maradt a NYITOTT_FELADATOK.md-ben.
5. (alacsony) `F43.2:` előtag két commiton.

Lappangó, ma 0 sort érintő: az `egyezik_lexema` ág tágabb a briefnél; `next(iter(sz_ok))` elvben hash-seedfüggő.

## Utólagos ellenőrzés és javítás (orkesztrátor, 2026.10.04)

- **Determinizmus (2):** `PYTHONHASHSEED=0`, `1`, `12345` mellett a `python eszkozok/lxx_bridge_egyezes.py` kimenete mindháromszor bájtra azonos a commitolt `naplok/LXX_BRIDGE_egyezes.tsv`-vel (`git diff --quiet` üres). OK.
- **feladatok.py figyelmeztetések:** a base-en (`ece75b7`) és a head-en is `71 brief, 0 hiba, 3 figyelmeztetés` (F09, F36: E18; F37: `ir`-minta) — nem az F43 okozza. OK.
- **(6) javítva:** a napló 8. szakaszának címe és záró „Megállás” sora a DT-F43 ✅ döntésre frissítve.
- **A1 javítva:** a DT-F43 LD035-indoklása a bridge tényleges H2555-párjaira cserélve (ἀδικία 10, ἄδικος 10, ἀσέβεια 8, ἀνομία 6).
- **Nem javítva (felhasználói hatáskör / alacsony):** ⛔-eltérés (történeti, a döntés megtörtént); Elfog. 5; N29 (a NYITOTT_FELADATOK.md nincs az `ir` listán); commit-előtag.
