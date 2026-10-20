# F22_Rom_jelentes.md — Károli–Strong párosítás: Róm (csak Sonnet, Message Batches API)

*Proveniencia: scope=Róm (431 Károli-vers, 7 261 TAGNT-token) | forras=`adat/karoli_strong/{parok,szavak}_Rom.tsv`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py`, `nem_tr_lista.py` (szkriptkimenetek, split('\t')) | ts=2026-10-20. Ág: `claude/f22-2kor`. Módszer: D45 és a brief 22.9 szerint: `prompt_v3` változatlanul (`prompt_sha256_12 = 84f12ca7aafb`), csak Sonnet (`claude-sonnet-5-5`), Message Batches API, `effort=high`, 10 verses kötegek, a plafon-őr (`api_koteg.PLAFON_USD` 104,36) és a részletekben küldés (DT-F22h (b)).*

## 1. Menet

- **Versbeosztás-jóváhagyás (2026.10.19):** `naplok/F22_versbeosztas_jovahagyas.md` (a felhasználó „Mehet”-je a `naplok/F22_C_elokeszites.md` alapján); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'Róm'`).
- **Minta:** `f22/minta_Rom.tsv`, 431 vers a modellhez, 44 köteg.
- **Batchek** (`f22/api_termeles/batchek.tsv`):
- `c_rom_1` (1. kör): `msgbatch_01Q4iDwHhXFhivDQYrJRDyZJ`, 44 kérés, beküldve 2026-10-20T04:56:24+00:00
- `c_rom_1` (2. kör): `msgbatch_01SKVxgzmiCBkNgbjY5BUwWP`, 3 kérés, beküldve 2026-10-20T04:59:45+00:00
- **Futásnapló** (Rom: 47 sor): modell `claude-sonnet-5-5`, `adaptive,effort=high`, `koltseg_forras=batch_ar_szamolt`.

## 2. Eredmény

| mutató | érték |
|---|---|
| Károli-vers / modellhez ment | 431 / 431 (a TAGNT-ban 433 vers: l. 3.) |
| hívás | 47 |
| kapuhiba 1. próbára | 3/431 (0.7%); végleges 0/431 (0,0%) |
| javító körbe került köteg | 3: k004, k007, k032 |
| link (`parok_Rom.tsv`) | 6871, mind `alacsony`, forrás `S` |
| szósor (`szavak_Rom.tsv`) | 14750 = 7 489 Károli + 7 261 eredeti |
| Károli-oldal: párosítva / betoldás / fuggoben | 6047 / 1404 / 38 |
| eredeti oldal: párosítva / fordítatlan / fuggoben | 6158 / 1069 / 34 |
| költség | 2.1407 USD (0.00497 USD/vers; bemenet 444 957, kimenet 339 142 token) |

Az `egyesit.py --konyv Róm --ellenoriz`: „rendben”. A szósorok száma a Károli- és az eredeti tokenek összegével egyezik. Mivel csak a Sonnet futott, nincs `magas` bizonyosság: minden link `alacsony`, mint az A és B csomagban.

**Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`, kizárás nélkül): 50,0% (1/2).

## 3. A Károli-összevonások (N-F22c) útja

A Róm 3:30 (hu 16–31) a TAGNT Róm 3:31-gyel (11 token), a Róm 8:38 (hu 20–41) a TAGNT Róm 8:39-cel (23 token) vonódik egybe: a két vers a `f22/versosszevonas.tsv` régi alakú sora szerint `fuggoben`/`kezi` állapotú, link nélkül (`naplok/F22_Rom_atnezes.tsv`). A Róm 8-ban a detektor a rossz TAGNT-verset jelölte gazdátlannak (8:38 helyett 8:39), a kézi tábla (`f22/versmegfeleltetes_kezi.tsv`) javítja.

**Tokenszintű vershatár-vizsgálat** (`tokenszint_vershatar.py`, `naplok/F22_C_elokeszites.md` 3.): a Róm-ben egy téves jelzés (Róm 4:16–17, a határ rendben).

## 4. A `[nem TR]` tokenek: 107, ebből 7 párosított

A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a); a tábla újraépítve).

| vers | er | alak | Strong | forrás |
|---|---|---|---|---|
| Róm 3:28 | 2 | γὰρ | G1063 | tehát |
| Róm 4:1 | 7 | προπάτορα | G6074 | atyánk |
| Róm 10:14 | 3 | ἐπικαλέσωνται | G1941 | hívják segítségül |
| Róm 10:14 | 10 | πιστεύσωσιν | G4100 | hisznek |
| Róm 10:14 | 16 | ἀκούσωσιν | G0191 | hallanának |
| Róm 14:4 | 16 | δυνατεῖ | G1414 | képes |
| Róm 14:4 | 20 | κύριος | G2962 | Úr által |
