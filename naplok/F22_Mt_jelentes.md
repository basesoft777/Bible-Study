# F22_Mt_jelentes.md — a Mt könyv Károli–Strong párosítása (22.9 D csomag)

*Proveniencia: scope=Mt (1071 Károli-vers, 18898 TAGNT-token) | forras=`adat/karoli_strong/{parok,szavak}_Mt.tsv`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py`, `tokenszint_vershatar.py`, `nem_tr_lista.py` (szkriptkimenetek, split('\t'); összeállítás: `f22_konyvjelentes.py`) | ts=2026-11-01. Módszer: D45, DT434/j és a brief 22.9 szerint: Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul (`prompt_sha256_12` = 84f12ca7aafb), csak-Sonnet (DT-F22c).*

## 1. Menet

- **Versbeosztás:** `naplok/F22_versbeosztas_jovahagyas.md` (orkesztrátori jóváhagyás, 2026-11-01); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve.
- **Minta:** `f22/minta_Mt.tsv`, 1071 vers a modellhez, 108 köteg.
- **Batchek** (`f22/api_termeles/batchek.tsv`, címke `d_mt_1`):
  - 1. kör: `msgbatch_015nQ74J77jH1UZVRe6Ck6HZ`, 108 kérés, beküldve 2026-11-01T08:08:48+00:00
  - 2. kör: `msgbatch_01FCCC5By9WisrHtJVFNiR19`, 25 kérés, beküldve 2026-11-01T08:11:59+00:00
- **Futásnapló** (Mt: 133 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`; a `prompt_sha256_12` minden sorban 84f12ca7aafb (bájtszintű hash, mint a C csomagban). **P3:** `sonnet_koteg.prompt_hash_hiba()` a jelentés összeállításakor: nincs hiba (az LF-normalizált tartalom sha256-ja egyezik az `f21p/prompt_v3.sha256`-tal).

## 2. Eredmény

| mutató | érték |
|---|---|
| Károli-vers / modellhez ment | 1071 / 1071 |
| hívás | 133 |
| kapuhiba (f22_statisztika.py) | Sonnet: 108 köteg, 1071 vers; kapuhiba első próbára 10.6% (113/1071); végleg 0.0% (0/1071) |
| javító körbe került köteg | 25: k003, k010, k024, k027, k033, k034, k043, k046, k048, k051, k060, k061, k064, k068, k077, k078, k081, k083, k086, k093, k098, k101, k103, k106, k107 |
| ebből egész köteg formátumhiba (érvénytelen JSON, `_munka/Mt_k*.json`) | 9: k010, k033, k046, k048, k051, k077, k083, k101, k107 |
| link (`parok_Mt.tsv`) | 17515, bizonyosság: alacsony 17515, forrás: S |
| szósor (`szavak_Mt.tsv`) | 37685 = 18787 Károli + 18898 eredeti |
| Károli-oldal: párosítva / betoldás / fuggoben | 15413 / 3374 / 0 |
| eredeti oldal: párosítva / fordítatlan / fuggoben | 15876 / 3022 / 0 |
| költség | 5.8060 USD (0.00542 USD/vers; bemenet 1308423, kimenet 899511 token) |

`egyesit.py --konyv Mt --ellenoriz`: „ellenőrzés: rendben” (P1: a szósorok száma a Károli- és az eredeti tokenek összegével egyezik; P2: a `strong` a TAGNT-ből levezethető). Mivel csak a Sonnet futott, nincs `magas` bizonyosság: minden link `alacsony`, forrás `S`.

**Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`, kizárás nélkül):
- Minden régi-arany hármas a könyvben: 2; a Károli-szó/kifejezés nem található a vers tokenjei közt: 0.
- **Mért érték (kizárás nélkül, minden link):** 100.0% (2/2).

## 3. Tokenszintű vershatár és kézi versek (N-F22e)

A `tokenszint_vershatar.py --lazabb Mt` kimenete:

```
Mt       arány 0.994  σ 2.9  jelölt 0
összesen: 0 jelölt (küszöb: abs ≥ 4, arány ≥ 0.4)
```

A könyvben nincs `kezi` kényszerített vers.

## 4. A `[nem TR]` tokenek: 458, ebből 47 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a)):

| vers | er | alak | Strong | Károli-szó |
|---|---|---|---|---|
| Mt 6:5 | 3 | προσεύχησθε, | G4336 | imádkozol |
| Mt 6:5 | 5 | ἔσεσθε | G1510 | légy |
| Mt 6:5 | 6 | ὡς | G5613 | olyan mint |
| Mt 6:12 | 10 | ἀφήκαμεν | G0863 | megbocsátunk |
| Mt 7:9 | 9 | αἰτήσει | G0154 | kér |
| Mt 7:10 | 5 | αἰτήσει, | G0154 | kér |
| Mt 7:16 | 11 | σταφυλάς, | G4718 | szőlőt |
| Mt 7:24 | 12 | ὁμοιωθήσεται | G3666 | hasonlítom |
| Mt 8:22 | 4 | λέγει | G3004 | monda |
| Mt 8:28 | 2 | ἐλθόντος | G2064 | mikor eljutott |
| Mt 8:28 | 11 | Γαδαρηνῶν | G1046 | Gadarénusok |
| Mt 9:27 | 15 | υἱὸς | G5207 | fia |
| Mt 10:42 | 3 | ἂν | G0302 | a ki |
| Mt 11:16 | 9 | παιδίοις | G3813 | gyermekekhez |
| Mt 11:16 | 14 | ἃ | G3739 | kik |
| Mt 11:16 | 15 | προσφωνοῦντα | G4377 | kiáltoznak |
| Mt 11:16 | 17 | ἑτέροις | G2087 | társaiknak |
| Mt 11:19 | 26 | ἔργων | G2041 | fiaitól |
| Mt 11:23 | 8 | ὑψωθήσῃ; | G5312 | felmagasztaltattál |
| Mt 11:23 | 11 | καταβήσῃ, | G2597 | megaláztatni |
| Mt 11:23 | 16 | ἐγενήθησαν | G1096 | történnek |
| Mt 11:23 | 23 | ἔμεινεν | G3306 | megmaradt |
| Mt 11:25 | 19 | ἔκρυψας | G2928 | elrejtetted |
| Mt 12:36 | 10 | λαλήσουσιν | G2980 | beszélnek |
| Mt 13:7 | 12 | ἔπνιξαν | G4155 | megfojták |
| Mt 13:15 | 33 | ἰάσομαι | G2390 | meg gyógyítsam |
| Mt 13:28 | 12 | λέγουσιν | G3004 | mondának |
| Mt 13:29 | 3 | φησιν· | G5346 | monda |
| Mt 13:36 | 18 | διασάφησον | G1285 | Magyarázd meg |
| Mt 15:32 | 15 | ἡμέραι | G2250 | napja |
| Mt 16:25 | 3 | ἐὰν | G1437 | a |
| Mt 20:15 | 11 | ἢ | G2228 | avagy |
| Mt 20:19 | 17 | ἐγερθήσεται.¶ | G1453 | feltámad |
| Mt 21:38 | 18 | σχῶμεν | G2192 | foglaljuk el |
| Mt 21:46 | 8 | ἐπεὶ | G1893 | mivelhogy |
| Mt 24:18 | 11 | ἱμάτιον | G2440 | ruháját |
| Mt 24:49 | 6 | αὐτοῦ, | G0846 | ő szolgatársait |
| Mt 24:49 | 7 | ἐσθίῃ | G2068 | enni |
| Mt 24:49 | 10 | πίνῃ | G4095 | inni |
| Mt 25:18 | 10 | γῆν | G1093 | földbe |
| Mt 25:18 | 12 | ἔκρυψεν | G2928 | elrejté |
| Mt 27:44 | 9 | σὺν | G4862 | együtt |
| Mt 27:44 | 12 | αὐτόν.¶ | G0846 | szemére |
| Mt 27:56 | 13 | Ἰωσὴφ | G2501 | Józsé |
| Mt 27:57 | 14 | ἐμαθητεύθη | G3100 | tanítványa volt |
| Mt 27:59 | 9 | ἐν | G1722 | gyolcsba |
| Mt 28:9 | 12 | ὑπήντησεν | G5221 | szembe jöve |

**A `[nem TR]` tokenek állapota (`szavak_Mt.tsv`):** forditatlan 411, parositva 47.

**Figyelem:** a `[nem TR]` jelölés azt mondja, hogy a párosított eredeti token nem a TR-ben áll; a link a kritikai szöveg alakjáé (D45 (a)), a Károli forrásszövege (TR) ettől eltérhet, ezért a Strong-szám nem feltétlenül a Károli szavának lexikai megfelelője.

**Lexikailag hamis link (az ellenőri jelentés, ELLENOR_F22_USZ_D, nyomán):** Mt 11:19 „fiaitól” ↔ ἔργων (G2041, „work”). A Károli a TR τέκνων szavát fordítja, amely nincs a kivonatban; a link a `[nem TR]` jelölőtáblában áll (`nem_tr_parositott.tsv`, `parok_Mt.tsv`), de lexikailag nem megfelelő. A `[nem TR]` párosítások ezért nem használhatók lexikai bizonyítékként a jelölőtábla átnézése nélkül; a javítás az N-F22e / későbbi átnézés dolga.
