# F22_ApCsel_jelentes.md — a ApCsel könyv Károli–Strong párosítása (22.9 F csomag)

*Proveniencia: scope=ApCsel (1006 Károli-vers, 18986 TAGNT-token) | forras=`adat/karoli_strong/{parok,szavak}_ApCsel.tsv`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py`, `tokenszint_vershatar.py`, `nem_tr_lista.py` (szkriptkimenetek, split('\t'); összeállítás: `f22_konyvjelentes.py`) | ts=2026-11-01. Módszer: D45, DT-F22i/j és a brief 22.9 szerint: Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul (`prompt_sha256_12` = 84f12ca7aafb), csak-Sonnet (DT-F22c).*

## 1. Menet

- **Versbeosztás:** `naplok/F22_versbeosztas_jovahagyas.md` (orkesztrátori jóváhagyás, 2026-11-01); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve.
- **Minta:** `f22/minta_ApCsel.tsv`, 1006 vers a modellhez, 101 köteg.
- **Batchek** (`f22/api_termeles/batchek.tsv`, címke `f_apcsel_1`):
  - 1. kör: `msgbatch_01YBykNKnx2GSPhqpZqahnD8`, 101 kérés, beküldve 2026-11-01T08:34:50+00:00
  - 2. kör: `msgbatch_01X9WCT5W9KAbJC33Kah7FqG`, 17 kérés, beküldve 2026-11-01T08:39:18+00:00
- **Futásnapló** (ApCsel: 118 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`; a `prompt_sha256_12` minden sorban 84f12ca7aafb (bájtszintű hash, mint a C csomagban). **P3:** `sonnet_koteg.prompt_hash_hiba()` a jelentés összeállításakor: nincs hiba (az LF-normalizált tartalom sha256-ja egyezik az `f21p/prompt_v3.sha256`-tal).

## 2. Eredmény

| mutató | érték |
|---|---|
| Károli-vers / modellhez ment | 1006 / 1006 |
| hívás | 118 |
| kapuhiba (f22_statisztika.py) | Sonnet: 101 köteg, 1006 vers; kapuhiba első próbára 2.7% (27/1006); végleg 0.0% (0/1006) |
| javító körbe került köteg | 17: k008, k009, k021, k025, k030, k031, k032, k046, k049, k051, k053, k057, k059, k067, k070, k072, k088 |
| ebből egész köteg formátumhiba (érvénytelen JSON, `_munka/ApCsel_k*.json`) | 1: k025 |
| link (`parok_ApCsel.tsv`) | 17408, bizonyosság: alacsony 17408, forrás: S |
| szósor (`szavak_ApCsel.tsv`) | 37786 = 18800 Károli + 18986 eredeti |
| Károli-oldal: párosítva / betoldás / fuggoben | 15363 / 3366 / 71 |
| eredeti oldal: párosítva / fordítatlan / fuggoben | 15863 / 3053 / 70 |
| költség | 6.0141 USD (0.00598 USD/vers; bemenet 1205715, kimenet 961680 token) |

`egyesit.py --konyv ApCsel --ellenoriz`: „ellenőrzés: rendben” (P1: a szósorok száma a Károli- és az eredeti tokenek összegével egyezik; P2: a `strong` a TAGNT-ből levezethető). Mivel csak a Sonnet futott, nincs `magas` bizonyosság: minden link `alacsony`, forrás `S`.

**Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`, kizárás nélkül):
- Minden régi-arany hármas a könyvben: 5; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 60.0% (3/5).

## 3. Tokenszintű vershatár és kézi versek (N-F22e)

A `tokenszint_vershatar.py --lazabb ApCsel` kimenete:

```
ApCsel   arány 0.990  σ 2.8  jelölt 2
    ApCsel 13:32 → ApCsel 13:33  többlet +9.0 / -10.9  (Károli 19, eredeti 10 | Károli 16, eredeti 27)
    ApCsel 24:2 → ApCsel 24:3  többlet -14.9 / +18.0  (Károli 8, eredeti 23 | Károli 28, eredeti 10)
összesen: 2 jelölt (küszöb: abs ≥ 4, arány ≥ 0.4)
```

`f22/kezi_versek_ApCsel.tsv` (link nélkül, `fuggoben`; a pótlás az N-F22e-é): ApCsel 13:32, ApCsel 13:33, ApCsel 24:2, ApCsel 24:3.

## 4. A `[nem TR]` tokenek: 634, ebből 37 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a)):

| vers | er | alak | Strong | Károli-szó |
|---|---|---|---|---|
| ApCsel 2:23 | 12 | χειρὸς | G5495 | kezeitekkel |
| ApCsel 9:8 | 13 | οὐδὲν | G3762 | senkit |
| ApCsel 11:28 | 13 | μεγάλην | G3173 | nagy |
| ApCsel 11:28 | 20 | ἥτις | G3748 | a mely |
| ApCsel 14:10 | 12 | ἥλατο | G0242 | felszökött |
| ApCsel 15:7 | 3 | ζητήσεως | G2214 | vetekedés |
| ApCsel 17:2 | 14 | διελέξατο | G1256 | vetekedék |
| ApCsel 19:12 | 6 | ἀποφέρεσθαι | G0667 | elvivék |
| ApCsel 19:12 | 25 | ἐκπορεύεσθαι | G1607 | kimenének |
| ApCsel 19:13 | 23 | ὁρκίζω | G3726 | Kényszerítünk |
| ApCsel 19:16 | 2 | ἐφαλόμενος | G2177 | ugorván |
| ApCsel 21:3 | 13 | κατήλθομεν | G2718 | köténk ki |
| ApCsel 21:4 | 18 | ἐπιβαίνειν | G1910 | menjen fel |
| ApCsel 21:5 | 28 | προσευξάμενοι | G4336 | imádkozánk |
| ApCsel 21:6 | 1 | ἀπησπασάμεθα | G0782 | elbúcsúzván |
| ApCsel 21:6 | 4 | ἀνέβημεν | G0305 | beülénk |
| ApCsel 21:8 | 9 | ἤλθομεν | G2064 | érkezénk |
| ApCsel 22:22 | 22 | καθῆκεν | G2520 | illik |
| ApCsel 23:6 | 15 | ἔκραζεν | G2896 | felkiálta |
| ApCsel 23:6 | 25 | Φαρισαίων· | G5330 | farizeus |
| ApCsel 24:27 | 12 | χάριτα | G5485 | kedveskedni |
| ApCsel 25:2 | 2 | τε | G5037 | pedig |
| ApCsel 25:2 | 5 | ἀρχιερεῖς | G0749 | főpap |
| ApCsel 25:4 | 9 | εἰς | G1519 | Czézáreában |
| ApCsel 25:4 | 10 | Καισάρειαν, | G2542 | Czézáreában |
| ApCsel 25:5 | 14 | ἄτοπον, | G0824 | gonoszság |
| ApCsel 25:7 | 15 | καταφέροντες | G2702 | hozván fel |
| ApCsel 25:9 | 20 | κριθῆναι | G2919 | ítéltetni meg |
| ApCsel 25:13 | 13 | ἀσπασάμενοι | G0782 | köszöntsék |
| ApCsel 26:22 | 13 | μαρτυρόμενος | G3143 | bizonyságot tévén |
| ApCsel 26:24 | 10 | φησιν· | G5346 | monda |
| ApCsel 26:28 | 13 | ποιῆσαι. | G4160 | legyek |
| ApCsel 26:29 | 14 | μεγάλῳ | G3173 | nagyon |
| ApCsel 26:31 | 13 | τι | G5100 | dolgot |
| ApCsel 27:42 | 13 | διαφύγῃ. | G1309 | el szaladhasson |
| ApCsel 28:27 | 33 | ἰάσομαι | G2390 | meg gyógyítsam |
| ApCsel 28:28 | 9 | τοῦτο | G3778 | ez |

**A `[nem TR]` tokenek állapota (`szavak_ApCsel.tsv`):** forditatlan 596, fuggoben 1, parositva 37.

Nem `forditatlan`, hanem `fuggoben` (a `kezi` versek tokenjei, link nélkül): ApCsel 24:2 er 15 (διορθωμάτων, G1357).

**Figyelem:** a `[nem TR]` jelölés azt mondja, hogy a párosított eredeti token nem a TR-ben áll; a link a kritikai szöveg alakjáé (D45 (a)), a Károli forrásszövege (TR) ettől eltérhet, ezért a Strong-szám nem feltétlenül a Károli szavának lexikai megfelelője.

Az ApCsel 13:32–33 és 24:2–3 tokenszintű vershatár-eltérése (N-F22e, DT-F22k) szövegen igazolt: `f22/kezi_versek_ApCsel.tsv`, a négy vers link nélkül, `fuggoben`; a pótlás az N-F22e-é.

**Ismert pontatlanság (az ellenőri jelentés nyomán, ELLENOR_F22_USZ_F):** az ApCsel 2:27 és 2:31 „sírban” szavának párja csak az εἰς (G1519); az ᾅδην (G0086) mindkét versben `forditatlan`, és a 2:31 „nem hagyatott” `betoldas`. Ez a régi arany két hibás hármasa (3/5), a Hádész–Seól motívum két kulcshelye: a Strong-index itt hiányos, a `alacsony` bizonyosság ezt jelzi; a javítás az N-F22e / későbbi átnézés dolga.
