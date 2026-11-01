# F22_Luk_jelentes.md — a Luk könyv Károli–Strong párosítása (22.9 E csomag)

*Proveniencia: scope=Luk (1151 Károli-vers, 20141 TAGNT-token) | forras=`adat/karoli_strong/{parok,szavak}_Luk.tsv`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py`, `tokenszint_vershatar.py`, `nem_tr_lista.py` (szkriptkimenetek, split('\t'); összeállítás: `f22_konyvjelentes.py`) | ts=2026-11-01. Módszer: D45, DT-F22i/j és a brief 22.9 szerint: Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul (`prompt_sha256_12` = 84f12ca7aafb), csak-Sonnet (DT-F22c).*

## 1. Menet

- **Versbeosztás:** `naplok/F22_versbeosztas_jovahagyas.md` (orkesztrátori jóváhagyás, 2026-11-01); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve.
- **Minta:** `f22/minta_Luk.tsv`, 1151 vers a modellhez, 116 köteg.
- **Batchek** (`f22/api_termeles/batchek.tsv`, címke `e_luk_1`):
  - 1. kör: `msgbatch_01CdXZpA5GrwL1k2M5GyegKE`, 116 kérés, beküldve 2026-11-01T08:24:20+00:00
  - 2. kör: `msgbatch_01NzNNUQvw2VQqznh89SDAVD`, 11 kérés, beküldve 2026-11-01T08:26:50+00:00
- **Futásnapló** (Luk: 127 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`; a `prompt_sha256_12` minden sorban 84f12ca7aafb (bájtszintű hash, mint a C csomagban). **P3:** `sonnet_koteg.prompt_hash_hiba()` a jelentés összeállításakor: nincs hiba (az LF-normalizált tartalom sha256-ja egyezik az `f21p/prompt_v3.sha256`-tal).

## 2. Eredmény

| mutató | érték |
|---|---|
| Károli-vers / modellhez ment | 1151 / 1151 |
| hívás | 127 |
| kapuhiba (f22_statisztika.py) | Sonnet: 116 köteg, 1151 vers; kapuhiba első próbára 3.5% (40/1151); végleg 0.0% (0/1151) |
| javító körbe került köteg | 11: k011, k018, k024, k027, k031, k041, k042, k089, k100, k102, k110 |
| ebből egész köteg formátumhiba (érvénytelen JSON, `_munka/Luk_k*.json`) | 3: k027, k041, k110 |
| link (`parok_Luk.tsv`) | 18818, bizonyosság: alacsony 18818, forrás: S |
| szósor (`szavak_Luk.tsv`) | 40291 = 20150 Károli + 20141 eredeti |
| Károli-oldal: párosítva / betoldás / fuggoben | 16552 / 3598 / 0 |
| eredeti oldal: párosítva / fordítatlan / fuggoben | 17129 / 3012 / 0 |
| költség | 6.2651 USD (0.00544 USD/vers; bemenet 1233534, kimenet 1006316 token) |

`egyesit.py --konyv Luk --ellenoriz`: „ellenőrzés: rendben” (P1: a szósorok száma a Károli- és az eredeti tokenek összegével egyezik; P2: a `strong` a TAGNT-ből levezethető). Mivel csak a Sonnet futott, nincs `magas` bizonyosság: minden link `alacsony`, forrás `S`.

**Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`, kizárás nélkül):
- Minden régi-arany hármas a könyvben: 5; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (5/5).

## 3. Tokenszintű vershatár és kézi versek (N-F22e)

A `tokenszint_vershatar.py --lazabb Luk` kimenete:

```
Luk      arány 1.000  σ 3.0  jelölt 0
összesen: 0 jelölt (küszöb: abs ≥ 4, arány ≥ 0.4)
```

A könyvben nincs `kezi` kényszerített vers.

## 4. A `[nem TR]` tokenek: 709, ebből 67 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a)):

| vers | er | alak | Strong | Károli-szó |
|---|---|---|---|---|
| Luk 2:3 | 8 | ἑαυτοῦ | G1438 | maga |
| Luk 2:14 | 11 | εὐδοκίας.¶ | G2107 | jó akarat |
| Luk 2:15 | 17 | ἐλάλουν | G2980 | mondának |
| Luk 4:41 | 7 | κραυγάζοντα | G2905 | kiáltozván |
| Luk 4:42 | 12 | ἐπεζήτουν | G1934 | felkeresé |
| Luk 4:43 | 19 | ἐπὶ | G1909 | azért |
| Luk 4:43 | 21 | ἀπεστάλην. | G0649 | küldettem |
| Luk 5:2 | 15 | ἔπλυνον | G4150 | mossák |
| Luk 5:5 | 22 | δίκτυα. | G1350 | hálót |
| Luk 6:4 | 13 | λαβὼν | G2983 | vette el |
| Luk 6:49 | 23 | συνέπεσεν, | G6081 | összeomlott |
| Luk 9:3 | 11 | ῥάβδον | G4464 | pálczákat |
| Luk 9:5 | 5 | δέχωνται | G1209 | be fogadnak |
| Luk 9:5 | 19 | ἀποτινάσσετε | G0660 | verjétek le |
| Luk 9:7 | 20 | ἠγέρθη | G1453 | támadt fel |
| Luk 9:8 | 11 | τις | G5100 | valamelyik |
| Luk 9:10 | 18 | πόλιν | G4172 | városnak |
| Luk 9:10 | 19 | καλουμένην | G2564 | nevű |
| Luk 9:11 | 8 | ἀποδεξάμενος | G0588 | fogadván |
| Luk 9:23 | 10 | ἔρχεσθαι, | G2064 | jőni |
| Luk 9:23 | 11 | ἀρνησάσθω | G0720 | tagadja meg |
| Luk 9:27 | 8 | αὐτοῦ | G0847 | itt |
| Luk 9:27 | 13 | γεύσωνται | G1089 | meg kóstolják |
| Luk 10:21 | 6 | ἐν | G1722 | lelkében |
| Luk 11:49 | 20 | διώξουσιν | G1377 | elüldöznek |
| Luk 12:26 | 3 | οὐδὲ | G3761 | sem |
| Luk 12:28 | 18 | ἀμφιέζει, | G6005 | ruházza |
| Luk 12:29 | 7 | καὶ | G2532 | vagy |
| Luk 12:30 | 8 | ἐπιζητοῦσιν· | G1934 | kérdezik |
| Luk 12:31 | 6 | αὐτοῦ | G0846 | országát |
| Luk 12:36 | 10 | ἀναλύσῃ | G0360 | jő meg |
| Luk 12:38 | 7 | κἂν | G1437+G2532 | és ha |
| Luk 12:39 | 20 | διορυχθῆναι | G1358 | törjön |
| Luk 12:56 | 17 | οἴδατε | G6063 | tudtok |
| Luk 12:56 | 18 | δοκιμάζειν; | G1381 | ítéletet tenni |
| Luk 12:58 | 28 | παραδώσει | G3860 | át adjon |
| Luk 12:58 | 35 | βαλεῖ | G0906 | vessen |
| Luk 13:8 | 20 | κόπρια· | G2874 | megtrágyázom |
| Luk 13:11 | 9 | δεκαοκτὼ | G3638+G1176 | tizennyolcz |
| Luk 13:14 | 24 | αὐταῖς | G0846 | azokon |
| Luk 14:28 | 18 | εἰς | G1519 | mivel |
| Luk 14:31 | 13 | βουλεύσεται | G1011 | tanácskozik |
| Luk 14:31 | 20 | ὑπαντῆσαι | G5221 | szembeszállhat |
| Luk 16:26 | 16 | ἔνθεν | G6033 | innét |
| Luk 17:4 | 6 | ἁμαρτήσῃ | G0264 | vétkezik |
| Luk 17:4 | 14 | πρὸς | G4314 | hozzád |
| Luk 17:6 | 6 | ἔχετε | G2192 | volna |
| Luk 17:27 | 4 | ἐγαμίζοντο, | G1061 | férjhezmentek |
| Luk 17:27 | 19 | πάντας. | G3956 | mindeneket |
| Luk 17:28 | 2 | καθὼς | G2531 | mint |
| Luk 17:29 | 16 | πάντας· | G3956 | mindenkit |
| Luk 17:30 | 3 | αὐτὰ | G0846 | azon |
| Luk 21:22 | 7 | πλησθῆναι | G4130 | beteljesedjenek |
| Luk 22:30 | 14 | καθήσεσθε | G2521 | üljetek |
| Luk 22:32 | 8 | ἐκλίπῃ | G1587 | el fogyatkozzék |
| Luk 22:34 | 9 | φωνήσει | G5455 | szól |
| Luk 22:34 | 12 | ἕως | G2193 | míg |
| Luk 22:36 | 2 | δὲ | G1161 | azért |
| Luk 24:4 | 5 | ἀπορεῖσθαι | G0639 | megdöbbenének |
| Luk 24:4 | 16 | ἐσθῆτι | G2066 | öltözetben |
| Luk 24:4 | 17 | ἀστραπτούσῃ. | G0797 | fényes |
| Luk 24:5 | 8 | πρόσωπα | G4383 | orczájokat |
| Luk 24:19 | 13 | Ναζαρηνοῦ, | G3479 | Názáretbeli |
| Luk 24:44 | 3 | πρὸς | G4314 | nékik |
| Luk 24:44 | 4 | αὐτούς· | G0846 | nékik |
| Luk 24:47 | 8 | εἰς | G1519 | és |
| Luk 24:47 | 15 | ἀρξάμενοι | G0757 | elkezdve |

**A `[nem TR]` tokenek állapota (`szavak_Luk.tsv`):** forditatlan 642, parositva 67.

**Figyelem:** a `[nem TR]` jelölés azt mondja, hogy a párosított eredeti token nem a TR-ben áll; a link a kritikai szöveg alakjáé (D45 (a)), a Károli forrásszövege (TR) ettől eltérhet, ezért a Strong-szám nem feltétlenül a Károli szavának lexikai megfelelője.
