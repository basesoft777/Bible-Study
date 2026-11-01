# F22_Mk_jelentes.md — a Mk könyv Károli–Strong párosítása (22.9 D csomag)

*Proveniencia: scope=Mk (678 Károli-vers, 11869 TAGNT-token) | forras=`adat/karoli_strong/{parok,szavak}_Mk.tsv`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py`, `tokenszint_vershatar.py`, `nem_tr_lista.py` (szkriptkimenetek, split('\t'); összeállítás: `f22_konyvjelentes.py`) | ts=2026-11-01. Módszer: D45, DT-F22i/j és a brief 22.9 szerint: Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul (`prompt_sha256_12` = 84f12ca7aafb), csak-Sonnet (DT-F22c).*

## 1. Menet

- **Versbeosztás:** `naplok/F22_versbeosztas_jovahagyas.md` (orkesztrátori jóváhagyás, 2026-11-01); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve.
- **Minta:** `f22/minta_Mk.tsv`, 678 vers a modellhez, 68 köteg.
- **Batchek** (`f22/api_termeles/batchek.tsv`, címke `d_mk_1`):
  - 1. kör: `msgbatch_01Vi5aBjwAu6PKn8WrWCLfaK`, 68 kérés, beküldve 2026-11-01T08:15:11+00:00
  - 2. kör: `msgbatch_0196N3RMPJeqnH796ibygzPf`, 5 kérés, beküldve 2026-11-01T08:19:06+00:00
- **Futásnapló** (Mk: 73 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`; a `prompt_sha256_12` minden sorban 84f12ca7aafb (bájtszintű hash, mint a C csomagban). **P3:** `sonnet_koteg.prompt_hash_hiba()` a jelentés összeállításakor: nincs hiba (az LF-normalizált tartalom sha256-ja egyezik az `f21p/prompt_v3.sha256`-tal).

## 2. Eredmény

| mutató | érték |
|---|---|
| Károli-vers / modellhez ment | 678 / 678 |
| hívás | 73 |
| kapuhiba (f22_statisztika.py) | Sonnet: 68 köteg, 678 vers; kapuhiba első próbára 2.1% (14/678); végleg 0.0% (0/678) |
| javító körbe került köteg | 5: k033, k046, k050, k063, k065 |
| ebből egész köteg formátumhiba (érvénytelen JSON, `_munka/Mk_k*.json`) | 1: k063 |
| link (`parok_Mk.tsv`) | 10658, bizonyosság: alacsony 10658, forrás: S |
| szósor (`szavak_Mk.tsv`) | 23620 = 11751 Károli + 11869 eredeti |
| Károli-oldal: párosítva / betoldás / fuggoben | 9500 / 2251 / 0 |
| eredeti oldal: párosítva / fordítatlan / fuggoben | 9753 / 2116 / 0 |
| költség | 3.6827 USD (0.00543 USD/vers; bemenet 707054, kimenet 595137 token) |

`egyesit.py --konyv Mk --ellenoriz`: „ellenőrzés: rendben” (P1: a szósorok száma a Károli- és az eredeti tokenek összegével egyezik; P2: a `strong` a TAGNT-ből levezethető). Mivel csak a Sonnet futott, nincs `magas` bizonyosság: minden link `alacsony`, forrás `S`.

**Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`, kizárás nélkül):
- Minden régi-arany hármas a könyvben: 0; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** n.é. (0/0).

## 3. Tokenszintű vershatár és kézi versek (N-F22e)

A `tokenszint_vershatar.py --lazabb Mk` kimenete:

```
Mk       arány 0.990  σ 2.8  jelölt 0
összesen: 0 jelölt (küszöb: abs ≥ 4, arány ≥ 0.4)
```

A könyvben nincs `kezi` kényszerített vers.

## 4. A `[nem TR]` tokenek: 663, ebből 57 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a)):

| vers | er | alak | Strong | Károli-szó |
|---|---|---|---|---|
| Mk 3:8 | 20 | ἀκούοντες | G0191 | mikor hallották |
| Mk 3:11 | 8 | ἐθεώρουν, | G2334 | meglátták |
| Mk 3:11 | 9 | προσέπιπτον | G4363 | leborulának |
| Mk 3:11 | 12 | ἔκραζον | G2896 | kiáltának |
| Mk 3:11 | 13 | λέγοντες | G3004 | mondván |
| Mk 3:28 | 16 | ὅσα | G3745 | mind a melyekkel |
| Mk 3:28 | 17 | ἐὰν | G1437 | melyekkel |
| Mk 4:36 | 15 | πλοῖα | G4143 | hajók |
| Mk 5:2 | 2 | ἐξελθόντος | G1831 | kiméne |
| Mk 5:2 | 8 | ὑπήντησεν | G5221 | elébe méne |
| Mk 5:3 | 7 | μνήμασιν. | G3418 | sírboltokban |
| Mk 5:3 | 9 | οὐδὲ | G3761 | sem |
| Mk 5:3 | 10 | ἁλύσει | G0254 | lánczokkal |
| Mk 5:3 | 11 | οὐκέτι | G2089+G3756 | már sem |
| Mk 5:5 | 3 | παντὸς | G3956 | mindig |
| Mk 5:7 | 5 | λέγει· | G3004 | monda |
| Mk 5:9 | 9 | λέγει | G3004 | mondván |
| Mk 5:9 | 11 | λεγιὼν | G3003 | Légió |
| Mk 5:23 | 2 | παρακαλεῖ | G3870 | kéré |
| Mk 5:23 | 21 | ζήσῃ.¶ | G2198 | éljen |
| Mk 5:34 | 5 | θυγάτηρ, | G2364 | Leányom |
| Mk 5:36 | 5 | παρακούσας | G3878 | hallá |
| Mk 6:21 | 11 | ἐποίησεν | G4160 | ad |
| Mk 6:22 | 11 | ἤρεσεν | G0700 | megtetszék |
| Mk 6:23 | 6 | τι | G5100 | Bármit |
| Mk 6:41 | 25 | παρατιθῶσιν | G3908 | tegyék elé |
| Mk 6:45 | 20 | ἀπολύει | G0630 | elbocsátja |
| Mk 7:4 | 6 | ἔλθωσιν | G2064 | jövén |
| Mk 7:24 | 8 | ὅρια | G3725 | határaiba |
| Mk 7:26 | 15 | ἐκβάλῃ | G1544 | űzze ki |
| Mk 8:36 | 3 | ὠφελεῖ | G5623 | használ |
| Mk 8:36 | 7 | κερδῆσαι | G2770 | megnyeri |
| Mk 8:36 | 12 | ζημιωθῆναι | G2210 | kárt vall |
| Mk 8:37 | 4 | δοῖ | G1325 | adhat |
| Mk 8:38 | 3 | ἐὰν | G1437 | valaki |
| Mk 9:6 | 5 | ἀποκριθῇ, | G0611 | beszél |
| Mk 9:6 | 8 | ἐγένοντο.¶ | G1096 | megrémülének |
| Mk 9:7 | 7 | ἐγένετο | G1096 | jöve |
| Mk 9:9 | 5 | ἐκ | G1537 | hegyről |
| Mk 9:12 | 4 | ἔφη | G5346 | monda |
| Mk 9:13 | 12 | ἤθελον | G2309 | akartak |
| Mk 9:19 | 4 | αὐτοῖς | G0846 | néki |
| Mk 9:20 | 12 | συνεσπάραξεν | G4952 | szaggatá |
| Mk 9:21 | 16 | ἐκ | G1537 | óta |
| Mk 9:26 | 2 | κράξας | G2896 | kiáltás |
| Mk 9:26 | 5 | σπαράξας | G4682 | szaggatás |
| Mk 9:26 | 13 | τοὺς | G3588 | sokan |
| Mk 9:27 | 7 | αὐτοῦ | G0846 | kezét |
| Mk 10:2 | 5 | ἐπηρώτων | G1905 | megkérdezék |
| Mk 12:26 | 16 | πῶς | G4459 | hogy mi módon |
| Mk 12:33 | 31 | περισσότερόν | G4054 | többet |
| Mk 14:6 | 14 | ἐν | G1722 | velem |
| Mk 14:6 | 15 | ἐμοί. | G1473 | én velem |
| Mk 14:44 | 17 | ἀπάγετε | G0520 | vigyétek el |
| Mk 15:30 | 4 | καταβὰς | G2597 | szállj le |
| Mk 15:35 | 7 | ἴδε, | G2396 | Ímé |
| Mk 15:36 | 3 | τις | G5100 | Egy ember |

**A `[nem TR]` tokenek állapota (`szavak_Mk.tsv`):** forditatlan 606, parositva 57.

**Figyelem:** a `[nem TR]` jelölés azt mondja, hogy a párosított eredeti token nem a TR-ben áll; a link a kritikai szöveg alakjáé (D45 (a)), a Károli forrásszövege (TR) ettől eltérhet, ezért a Strong-szám nem feltétlenül a Károli szavának lexikai megfelelője.
