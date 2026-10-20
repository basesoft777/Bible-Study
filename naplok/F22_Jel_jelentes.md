# F22_Jel_jelentes.md — Károli–Strong párosítás: Jel (csak Sonnet, Message Batches API)

*Proveniencia: scope=Jel (405 Károli-vers, 10 185 TAGNT-token) | forras=`adat/karoli_strong/{parok,szavak}_Jel.tsv`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py`, `nem_tr_lista.py` (szkriptkimenetek, split('\t')) | ts=2026-10-20. Ág: `claude/f22-2kor`. Módszer: D45 és a brief 22.9 szerint: `prompt_v3` változatlanul (`prompt_sha256_12 = 84f12ca7aafb`), csak Sonnet (`claude-sonnet-5-5`), Message Batches API, `effort=high`, 10 verses kötegek, a plafon-őr (`api_koteg.PLAFON_USD` 104,36) és a részletekben küldés (DT-F22h (b)).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.19):** `naplok/F22_versbeosztas_jovahagyas.md` (a felhasználó „Mehet”-je a `naplok/F22_C_elokeszites.md` alapján); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Jel'`).
- **Minta:** `f22/minta_Jel.tsv`, 405 vers a modellhez, 41 köteg.
- **Batchek** (`f22/api_termeles/batchek.tsv`):
- `c_jel_4` (1. kör): `msgbatch_01NtonEUTHNoZikwDVS7rFc9`, 23 kérés, beküldve 2026-10-20T05:13:25+00:00
- `c_jel_4` (2. kör): `msgbatch_015YnKNz2w7Y4niyAPa6Uxq6`, 3 kérés, beküldve 2026-10-20T05:24:50+00:00
- `c_jel_5` (1. kör): `msgbatch_01Tue5YHDmFYYS9wnepsUHoK`, 12 kérés, beküldve 2026-10-20T05:27:22+00:00
- `c_jel_5` (2. kör): `msgbatch_01Kc36wko3tQM61qGKsc3ZDX`, 3 kérés, beküldve 2026-10-20T05:31:44+00:00
- `c_jel_6` (1. kör): `msgbatch_01EDkymeNJPYByGPVUQ7ByS4`, 6 kérés, beküldve 2026-10-20T05:34:14+00:00
- `c_jel_6` (2. kör): `msgbatch_01P4jH78wnsvasz9eoSKA4Gx`, 1 kérés, beküldve 2026-10-20T05:37:31+00:00
- **Futásnapló** (Jel: 48 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

## 2. Eredmény

| mutató | érték |
|---|---|
| Károli-vers / modellhez ment | 405 / 405 (a TAGNT-ban 405 vers: l. 3.) |
| hívás | 48 |
| kapuhiba 1. próbára | 8/405 (2.0%); végleges 0/405 (0,0%) |
| javító körbe került köteg | 7: k001, k019, k020, k024, k026, k031, k041 |
| link (`parok_Jel.tsv`) | 8689, mind `alacsony`, forrás `S` |
| szósor (`szavak_Jel.tsv`) | 19929 = 9 744 Károli + 10 185 eredeti |
| Károli-oldal: párosítva / betoldás / fuggoben | 7565 / 2179 / 0 |
| eredeti oldal: párosítva / fordítatlan / fuggoben | 7929 / 2256 / 0 |
| költség | 3.2796 USD (0.00810 USD/vers; bemenet 553 950, kimenet 545 138 token) |

Az `egyesit.py --konyv Jel --ellenoriz`: „rendben”. A szósorok száma a Károli- és az eredeti tokenek összegével egyezik. Mivel csak a Sonnet futott, nincs `magas` bizonyosság: minden link `alacsony`, mint az A és B csomagban.

**Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`, kizárás nélkül): 100,0% (11/11).

## 3. A Károli-összevonások (N-F22c) útja

Összevonás nincs. A Jel 12:18 görög szövege az F90 óta megvan, rendes vers.

**Tokenszintű vershatár-vizsgálat** (`tokenszint_vershatar.py`, `naplok/F22_C_elokeszites.md` 3.): a Jel-ben nincs jelölt.

## 4. A `[nem TR]` tokenek: 641, ebből 44 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a); a tábla újraépítve).

| vers | er | alak | Strong | forrás |
|---|---|---|---|---|
| Jel 4:10 | 14 | προσκυνήσουσιν | G4352 | imádja |
| Jel 4:10 | 23 | βαλοῦσιν | G0906 | teszi |
| Jel 8:11 | 10 | ἐγένετο | G1096 | változék |
| Jel 8:11 | 14 | ὑδάτων | G5204 | folyóvizek |
| Jel 8:12 | 31 | φάνῃ | G5316 | fényljék |
| Jel 8:13 | 6 | ἀετοῦ | G0105 | angyalt |
| Jel 8:13 | 17 | κατοικοῦντας | G2730 | lakosainak |
| Jel 9:2 | 18 | ἐσκοτώθη | G4656 | meghomályosodék |
| Jel 9:4 | 6 | ἀδικήσουσιν | G0091 | bántsák |
| Jel 9:5 | 3 | αὐτοῖς | G0846 | azoknak |
| Jel 9:5 | 10 | βασανισθήσονται | G0928 | kínoztassanak |
| Jel 9:6 | 20 | φεύγει | G5343 | elmegy |
| Jel 11:6 | 13 | ἡμέρας | G2250 | idejében |
| Jel 11:11 | 14 | ἐν | G1722 | beléjök |
| Jel 11:11 | 15 | αὐτοῖς, | G0846 | beléjök |
| Jel 11:11 | 25 | ἐπέπεσεν | G1968 | esék |
| Jel 11:18 | 35 | μικροὺς | G3398 | kicsinyeknek |
| Jel 11:18 | 38 | μεγάλους, | G3173 | nagyoknak |
| Jel 16:1 | 14 | ἐκχέετε | G1632 | töltsétek ki |
| Jel 16:1 | 16 | ἑπτὰ | G2033 | hét |
| Jel 16:14 | 4 | δαιμονίων | G1140 | ördögi |
| Jel 16:14 | 7 | ἃ | G3739 | a kik |
| Jel 16:14 | 8 | ἐκπορεύεται | G1607 | elmennek |
| Jel 18:14 | 19 | ἀπώλετο | G0622 | eltávozott |
| Jel 18:14 | 27 | εὑρήσουσιν. | G2147 | meg találod |
| Jel 18:16 | 19 | χρυσίῳ | G5553 | aranynyal |
| Jel 18:16 | 24 | μαργαρίτῃ, | G3135 | gyöngyökkel |
| Jel 19:13 | 7 | κέκληται | G2564 | neveztetik |
| Jel 19:15 | 13 | πατάξῃ | G3960 | verje |
| Jel 20:9 | 9 | ἐκύκλευσαν | G6059 | körülvevék |
| Jel 20:11 | 10 | αὐτόν, | G0846 | rajta |
| Jel 20:12 | 13 | θρόνου, | G2362 | Isten |
| Jel 20:12 | 16 | ἠνοίχθησαν. | G0455 | nyittatának meg |
| Jel 20:12 | 20 | ἠνοίχθη | G0455 | nyittaték meg |
| Jel 21:4 | 7 | ἐκ | G1537 | szemeikről |
| Jel 21:5 | 7 | θρόνῳ· | G2362 | királyiszéken |
| Jel 21:6 | 4 | γέγοναν. | G1096 | Meglett |
| Jel 22:11 | 7 | ῥυπαρὸς | G4508 | fertelmes |
| Jel 22:11 | 8 | ῥυπανθήτω | G4510 | legyen fertelmes |
| Jel 22:11 | 13 | δικαιοσύνην | G1343 | igaz |
| Jel 22:11 | 14 | ποιησάτω | G4160 | legyen |
| Jel 22:12 | 16 | ἐστὶν | G1510 | lesz |
| Jel 22:13 | 4 | ἄλφα | G0001 | Alfa |
| Jel 22:16 | 27 | πρωϊνός. | G4407 | hajnali |
