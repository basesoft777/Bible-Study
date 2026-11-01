# F22_Jan_jelentes.md — a Ján könyv Károli–Strong párosítása (22.9 E csomag)

*Proveniencia: scope=Ján (879 Károli-vers, 16076 TAGNT-token) | forras=`adat/karoli_strong/{parok,szavak}_Jan.tsv`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py`, `tokenszint_vershatar.py`, `nem_tr_lista.py` (szkriptkimenetek, split('\t'); összeállítás: `f22_konyvjelentes.py`) | ts=2026-11-01. Módszer: D45, DT-F22i/j és a brief 22.9 szerint: Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul (`prompt_sha256_12` = 84f12ca7aafb), csak-Sonnet (DT-F22c).*

## 1. Menet

- **Versbeosztás:** `naplok/F22_versbeosztas_jovahagyas.md` (orkesztrátori jóváhagyás, 2026-11-01); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve.
- **Minta:** `f22/minta_Jan.tsv`, 879 vers a modellhez, 88 köteg.
- **Batchek** (`f22/api_termeles/batchek.tsv`, címke `e_jan_1`):
  - 1. kör: `msgbatch_01WzjV5zzZLJf5XJFeKx8fei`, 88 kérés, beküldve 2026-11-01T08:29:24+00:00
  - 2. kör: `msgbatch_01MozoXoQUoUvGHcyk2jpKxG`, 14 kérés, beküldve 2026-11-01T08:32:08+00:00
- **Futásnapló** (Jan: 102 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`; a `prompt_sha256_12` minden sorban 84f12ca7aafb (bájtszintű hash, mint a C csomagban). **P3:** `sonnet_koteg.prompt_hash_hiba()` a jelentés összeállításakor: nincs hiba (az LF-normalizált tartalom sha256-ja egyezik az `f21p/prompt_v3.sha256`-tal).

## 2. Eredmény

| mutató | érték |
|---|---|
| Károli-vers / modellhez ment | 879 / 879 |
| hívás | 102 |
| kapuhiba (f22_statisztika.py) | Sonnet: 88 köteg, 879 vers; kapuhiba első próbára 3.6% (32/879); végleg 0.2% (2/879) |
| javító körbe került köteg | 14: k006, k012, k015, k027, k033, k034, k046, k050, k057, k061, k068, k076, k086, k088 |
| ebből egész köteg formátumhiba (érvénytelen JSON, `_munka/Jan_k*.json`) | 2: k015, k034 |
| link (`parok_Jan.tsv`) | 14824, bizonyosság: alacsony 14824, forrás: S |
| szósor (`szavak_Jan.tsv`) | 32098 = 16022 Károli + 16076 eredeti |
| Károli-oldal: párosítva / betoldás / fuggoben | 13198 / 2534 / 290 |
| eredeti oldal: párosítva / fordítatlan / fuggoben | 13420 / 2353 / 303 |
| költség | 4.7832 USD (0.00544 USD/vers; bemenet 1010768, kimenet 754481 token) |

`egyesit.py --konyv Ján --ellenoriz`: „ellenőrzés: rendben” (P1: a szósorok száma a Károli- és az eredeti tokenek összegével egyezik; P2: a `strong` a TAGNT-ből levezethető). Mivel csak a Sonnet futott, nincs `magas` bizonyosság: minden link `alacsony`, forrás `S`.

**Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`, kizárás nélkül):
- Minden régi-arany hármas a könyvben: 0; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** n.é. (0/0).

## 3. Tokenszintű vershatár és kézi versek (N-F22e)

A `tokenszint_vershatar.py --lazabb Ján` kimenete:

```
Ján      arány 0.997  σ 1.6  jelölt 3
    Ján 1:39 → Ján 1:40  többlet -8.0 / +5.0  (Károli 15, eredeti 23 | Károli 22, eredeti 17)
    Ján 1:42 → Ján 1:43  többlet -5.0 / +6.0  (Károli 19, eredeti 24 | Károli 23, eredeti 17)
    Ján 1:48 → Ján 1:49  többlet -5.0 / +5.0  (Károli 18, eredeti 23 | Károli 23, eredeti 18)
összesen: 3 jelölt (küszöb: abs ≥ 4, arány ≥ 0.4)
```

`f22/kezi_versek_Jan.tsv` (link nélkül, `fuggoben`; a pótlás az N-F22e-é): Ján 1:38, Ján 1:39, Ján 1:40, Ján 1:41, Ján 1:42, Ján 1:43, Ján 1:44, Ján 1:45, Ján 1:46, Ján 1:47, Ján 1:48, Ján 1:49, Ján 1:50, Ján 1:51.

## 4. A `[nem TR]` tokenek: 423, ebből 42 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a)):

| vers | er | alak | Strong | Károli-szó |
|---|---|---|---|---|
| Ján 2:15 | 26 | ἀνέτρεψεν, | G0396 | feldönté |
| Ján 2:17 | 14 | καταφάγεταί | G2719 | emészt |
| Ján 3:25 | 9 | Ἰουδαίου | G2453 | judeaiak |
| Ján 3:27 | 9 | οὐδὲ | G3761 | semmit |
| Ján 3:27 | 10 | ἓν | G1520 | semmit |
| Ján 4:1 | 5 | Ἰησοῦς | G2424 | Úr |
| Ján 4:6 | 21 | ὡς | G5613 | Mintegy |
| Ján 4:34 | 9 | ποιήσω | G4160 | cselekedjem |
| Ján 5:25 | 14 | ἀκούσουσιν | G0191 | hallják |
| Ján 5:25 | 24 | ζήσουσιν.¶ | G2198 | élnek |
| Ján 5:28 | 14 | ἀκούσουσιν | G0191 | meghallják |
| Ján 6:51 | 19 | ζήσει | G2198 | él |
| Ján 6:57 | 17 | ζήσει | G2198 | él |
| Ján 8:12 | 19 | περιπατήσῃ | G4043 | járhat |
| Ján 8:25 | 6 | εἶ; | G1510 | vagy |
| Ján 8:26 | 20 | λαλῶ | G2980 | beszélem |
| Ján 8:54 | 5 | δοξάσω | G1392 | dicsőítem |
| Ján 8:54 | 24 | ἡμῶν | G3165 | ti Istenetek |
| Ján 8:55 | 17 | ὑμῖν | G4771 | hozzátok |
| Ján 9:30 | 20 | ἤνοιξέν | G0455 | megnyitotta |
| Ján 10:14 | 12 | γινώσκουσίν | G1097 | ismernek |
| Ján 10:14 | 13 | με | G3165 | engem |
| Ján 10:14 | 14 | τὰ | G3588 | enyéim |
| Ján 10:14 | 15 | ἐμά, | G1473 | enyéim |
| Ján 10:16 | 22 | γενήσονται | G1096 | lészen |
| Ján 10:22 | 2 | τότε | G5119 | pedig |
| Ján 11:21 | 14 | ἀπέθανεν | G0599 | halt meg |
| Ján 13:38 | 1 | ἀποκρίνεται | G0611 | Felele |
| Ján 13:38 | 18 | φωνήσῃ | G5455 | szól |
| Ján 13:38 | 21 | ἀρνήσῃ | G0720 | megtagadsz |
| Ján 16:15 | 15 | λαμβάνει | G2983 | vesz |
| Ján 16:25 | 20 | ἀπαγγελῶ | G0518 | beszélek |
| Ján 17:13 | 20 | ἑαυτοῖς. | G1438 | magokban |
| Ján 18:10 | 18 | ὠτάριον | G6090 | fülét |
| Ján 18:13 | 2 | ἤγαγον | G0071 | vivék |
| Ján 18:14 | 12 | ἀποθανεῖν | G0599 | veszszen el |
| Ján 18:20 | 7 | λελάληκα | G2980 | szólottam |
| Ján 18:20 | 21 | πάντες | G3956 | mindenünnen |
| Ján 18:21 | 3 | ἐρωτᾷς; | G2065 | kérdesz |
| Ján 18:21 | 4 | ἐρώτησον | G2065 | Kérdezd |
| Ján 18:28 | 13 | πρωΐ. | G4404 | reggel |
| Ján 18:29 | 9 | φησίν· | G5346 | monda |

**A `[nem TR]` tokenek állapota (`szavak_Jan.tsv`):** forditatlan 372, fuggoben 9, parositva 42.

Nem `forditatlan`, hanem `fuggoben` (a `kezi` versek tokenjei, link nélkül): Ján 1:38 er 20 (μεθερμηνευόμενον, G3177), Ján 1:39 er 5 (ὄψεσθε.¶, G3700), Ján 1:39 er 7 (οὖν, G3767), Ján 1:41 er 3 (πρῶτον, G4413), Ján 1:42 er 18 (Ἰωάννου·, G2491), Ján 1:46 er 13 (ὁ, G3588), Ján 1:50 er 9 (ὅτι, G3754), Ján 2:8 er 10 (οἱ, G3588), Ján 2:8 er 11 (δὲ, G1161).

**Figyelem:** a `[nem TR]` jelölés azt mondja, hogy a párosított eredeti token nem a TR-ben áll; a link a kritikai szöveg alakjáé (D45 (a)), a Károli forrásszövege (TR) ettől eltérhet, ezért a Strong-szám nem feltétlenül a Károli szavának lexikai megfelelője.

**Végleges kapuhiba: 2/879 (Ján 2:8 és Ján 4:30; indokolt maradék: a javítókör egy újabb próbát ad).** Ján 2:8: az 1. próbán a „többször szereplő magyar szó” kapuhiba (3. pont, `_munka/Jan_k006.json`). Ján 4:30: az 1. próbán a 4:29–4:38 köteg érvénytelen JSON volt (`_munka/Jan_k015.json`). **A 2. próbán mindkét vers benne volt a válaszban, de a `vers` kulcsuk vezető szóközzel állt** (`" Ján 2:8"`, `" Ján 4:30"`; `high/Jan.jsonl` 75. és 85. sor), a kapu ezt nem normalizálja, ezért a verset „hiányzik a válaszból” hibával `kezi`-re tette. A két végleges kapuhiba közös oka a kulcs normalizálásának hiánya a kapuban; a kapu módosítása külön tétel (a futtatás szabályait ez a menet nem változtatta). A két vers `kezi` (link nélkül, `fuggoben`; `naplok/F22_Jan_atnezes.tsv`) a Ján 1:38–51 14 verse mellett (N-F22e): összesen 16 `kezi` vers a Jánban.
