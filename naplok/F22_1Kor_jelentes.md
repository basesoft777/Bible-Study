# F22_1Kor_jelentes.md — Károli–Strong párosítás: 1Kor (csak Sonnet, Message Batches API)

*Proveniencia: scope=1Kor (436 Károli-vers, 6 986 TAGNT-token) | forras=`adat/karoli_strong/{parok,szavak}_1Kor.tsv`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py`, `nem_tr_lista.py` (szkriptkimenetek, split('\t')) | ts=2026-10-20. Ág: `claude/f22-2kor`. Módszer: D45 és a brief 22.9 szerint: `prompt_v3` változatlanul (`prompt_sha256_12 = 84f12ca7aafb`), csak Sonnet (`claude-sonnet-5-5`), Message Batches API, `effort=high`, 10 verses kötegek, a plafon-őr (`api_koteg.PLAFON_USD` 104,36) és a részletekben küldés (DT-F22h (b)).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.19):** `naplok/F22_versbeosztas_jovahagyas.md` (a felhasználó „Mehet”-je a `naplok/F22_C_elokeszites.md` alapján); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'1Kor'`).
- **Minta:** `f22/minta_1Kor.tsv`, 436 vers a modellhez, 44 köteg.
- **Batchek** (`f22/api_termeles/batchek.tsv`):
- `c_1kor_2` (1. kör): `msgbatch_018zMNqYAd2xUWMUR2pyFKMT`, 35 kérés, beküldve 2026-10-20T05:02:11+00:00
- `c_1kor_2` (2. kör): `msgbatch_01VyC1sLLA7YygU5Q8KxuTsP`, 5 kérés, beküldve 2026-10-20T05:05:29+00:00
- `c_1kor_3` (1. kör): `msgbatch_01BXT7uXMVXYykcxXiyoVJXH`, 9 kérés, beküldve 2026-10-20T05:08:42+00:00
- `c_1kor_3` (2. kör): `msgbatch_013N8mB4rbateLMb8JNi9rS9`, 1 kérés, beküldve 2026-10-20T05:10:54+00:00
- **Futásnapló** (1Kor: 50 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

## 2. Eredmény

| mutató | érték |
|---|---|
| Károli-vers / modellhez ment | 436 / 436 (a TAGNT-ban 437 vers: l. 3.) |
| hívás | 50 |
| kapuhiba 1. próbára | 7/436 (1.6%); végleges 0/436 (0,0%) |
| javító körbe került köteg | 6: k020, k022, k029, k034, k035, k038 |
| link (`parok_1Kor.tsv`) | 6686, mind `alacsony`, forrás `S` |
| szósor (`szavak_1Kor.tsv`) | 14273 = 7 287 Károli + 6 986 eredeti |
| Károli-oldal: párosítva / betoldás / fuggoben | 6024 / 1257 / 6 |
| eredeti oldal: párosítva / fordítatlan / fuggoben | 6049 / 931 / 6 |
| költség | 2.0566 USD (0.00472 USD/vers; bemenet 470 394, kimenet 317 233 token) |

Az `egyesit.py --konyv 1Kor --ellenoriz`: „rendben”. A szósorok száma a Károli- és az eredeti tokenek összegével egyezik. Mivel csak a Sonnet futott, nincs `magas` bizonyosság: minden link `alacsony`, mint az A és B csomagban.

**Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`, kizárás nélkül): 50,0% (2/4).

## 3. A Károli-összevonások (N-F22c) útja

Az 1Kor 3:22 (hu 20–25) a TAGNT 1Kor 3:23-mal (6 token) vonódik egybe: `fuggoben`/`kezi`, link nélkül (`naplok/F22_1Kor_atnezes.tsv`).

**Tokenszintű vershatár-vizsgálat** (`tokenszint_vershatar.py`, `naplok/F22_C_elokeszites.md` 3.): a 1Kor-ben nincs jelölt.

## 4. A `[nem TR]` tokenek: 180, ebből 23 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a); a tábla újraépítve).

| vers | er | alak | Strong | forrás |
|---|---|---|---|---|
| 1Kor 3:4 | 13 | οὐκ | G3756 | nem |
| 1Kor 3:4 | 14 | ἄνθρωποί | G0444 | testiek |
| 1Kor 3:5 | 1 | Τί | G5101 | kicsoda |
| 1Kor 3:5 | 5 | τί | G5101 | kicsoda |
| 1Kor 3:10 | 13 | ἔθηκα, | G5087 | vetettem |
| 1Kor 5:2 | 10 | ἀρθῇ | G0142 | kivettetnék |
| 1Kor 5:2 | 18 | πράξας; | G4238 | cselekedte |
| 1Kor 8:8 | 5 | παραστήσει | G3936 | tesz kedvesekké |
| 1Kor 8:9 | 12 | ἀσθενέσιν. | G0772 | erőteleneknek |
| 1Kor 10:9 | 14 | ἀπώλλυντο. | G0622 | elveszének |
| 1Kor 10:10 | 3 | καθάπερ | G2509 | miképen |
| 1Kor 10:11 | 4 | τυπικῶς | G9992 | példaképen |
| 1Kor 10:11 | 5 | συνέβαινεν | G4819 | estek |
| 1Kor 10:11 | 18 | κατήντηκεν.¶ | G2658 | elérkezett |
| 1Kor 11:5 | 13 | αὐτῆς· | G0846 | ő |
| 1Kor 11:31 | 2 | δὲ | G1161 | Mert |
| 1Kor 12:9 | 14 | ἑνὶ | G1520 | egy |
| 1Kor 13:8 | 4 | πίπτει.¶ | G4098 | el fogy |
| 1Kor 14:16 | 3 | εὐλογῇς | G2127 | mondasz áldást |
| 1Kor 14:16 | 4 | ἐν | G1722 | lélekkel |
| 1Kor 14:21 | 11 | ἑτέρων | G2087 | idegen |
| 1Kor 14:35 | 15 | γυναικὶ | G1135 | asszonynak |
| 1Kor 15:24 | 5 | παραδιδῷ | G3860 | átadja |
