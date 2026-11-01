# F120.1 — a tényleges hibamód újramérése (3.1, csak olvas)

*Eszköz: `naplok/F120_meres.py` (csak olvas, a repóba nem ír). Futtatás:*

```bash
git show 8f616529^:konkordancia/Karoli_versmegfeleltetes.tsv > <ideiglenes>/regi_vm.tsv
python naplok/F120_meres.py <ideiglenes>/regi_vm.tsv
python naplok/F120_meres.py <ideiglenes>/regi_vm.tsv <ideiglenes>/regi_vm.tsv   # a 3–5. rész a régi táblán
```

*Régi tábla: a `Karoli_versmegfeleltetes.tsv` az F117.3 előtt (8f616529^); mai tábla: a 9cf0e43a munkafáé (F117.3 + F146.2). BSB: a mai `konkordancia/BSB_Strongs.tsv` (F71.2, 73b47116, 2026-10-06; 278 166 sor). TAHOT: a mai `TAHOT_kivonat.tsv` (Károli-kulcsú, F85.6). WLC: `Macula_heber_*.tsv`.*

**A BSB-klón (`bsb-data-output/`) a gépen nincs meg** (keresve: `C:\Users\bases` 4–8 szint mélyen, `D:\`, a WSL `pardes` disztribúció `/`-tól 6 szintig; 2026-11-01). A `bsb_import` tényleges `allapot`-a a display-JSON nélkül nem számolható, ezért az 1. pont az R4 **feltételét** méri (`kk_max_tabla` × TAHOT-max), a veszélyeztetett sorokat pedig a mai `BSB_Strongs.tsv`-n számolja. A klón a 3.5-höz kell; hálózatról nem töltöttem le.

*proveniencia: scope=Karoli_versmegfeleltetes.tsv régi (8f616529^) és mai (9cf0e43a), TAHOT_kivonat.tsv, BSB_Strongs.tsv (F71.2), Macula_heber_*.tsv | forras=repó-adat, BSB-klón nélkül | eszkoz=naplok/F120_meres.py | n_bsb_sor=278166 | ts=2026-11-01*

## 0. Változás a brief óta

A brief 174 `KEZI` + kitöltött `igehely_mt` sort és 13 fejezetet ír. Az F146.2 (2026-10-29, DT398) a Jóel 26 sorát `KEZI` + mt-vé tette, ezért ma **200 sor** (`awk -F'\t' '$4=="KEZI" && $3!=""'`, a mai táblán) és **15 fejezet** (a 13 + Jóel 3, Jóel 4). *(proveniencia: scope=Karoli_versmegfeleltetes.tsv | forras=awk, 9cf0e43a | ts=2026-11-01)*

## 1. A `bsb_import` R4: csendes `illesztetlen`, nem leállás

A kódolvasás (scope=manual) megerősíti a brief 3.1 feltevését: a `fejezet_eltolasok()` (a `SystemExit` forrása) a fő úton nem hívódik; a fő út (`fut()` → `ot_konyv()` → `konyv_megfeleltetes(…, kk_max)`) R4-eltérésnél `kk_max_eltérés`-t ír az `allapot[f]`-be, és a fejezet minden verse `illesztetlen`-ként kimarad a `BSB_Strongs.tsv`-ből. Leállás nincs.

A feltétel (`kk_max_tabla` MT-fejezet-maximuma ≠ TAHOT fejezet-maximuma):

| | fejezet | a mai `BSB_Strongs.tsv`-ben ezekben a fejezetekben |
|---|---|---|
| régi tábla | 0 | — |
| mai tábla | **15** | **325 vers, 3 625 sor** |

| MT-fejezet | KK-MT-max | TAHOT-max (Károli-kulcs) | BSB vers / sor |
|---|---|---|---|
| 1Sám 20 | 42 | 43 | 42 / 696 |
| 1Sám 21 | 1 | 15 | 15 / 271 |
| 2Móz 36 | 38 | 37 | 38 / 515 |
| Hós 2 | 25 | 22 | 23 / 284 |
| Jób 17 | 16 | 15 | 16 / 110 |
| Jób 37 | 24 | 23 | 24 / 187 |
| Jób 40 | 5 | 19 | 24 / 163 |
| Jóel 3 | 5 | 21 | 21 / 268 |
| Jóel 4 | 21 | — (a TAHOT-ban nincs Jóel 4) | 0 / 0 |
| Préd 10 | 3 | 17 | 20 / 191 |
| Péld 12 | 28 | 27 | 28 / 200 |
| Én 6 | 12 | 10 | 13 / 123 |
| Én 7 | 1 | 13 | 13 / 125 |
| Ézs 2 | 22 | 21 | 22 / 250 |
| Ézs 3 | 26 | 27 | 26 / 242 |

Két különböző hibaok, nem egy:
- **(i) Károli-max ↔ MT-max** (2Móz 36, Hós 2, Jób 17, 37, Péld 12, Én 6, Ézs 2, 3, 1Sám 20): a TAHOT Károli-kulcsú, a `kk_max` MT; a kettő nem összevethető (brief 1. pont).
- **(ii) részleges MT-fejezet** (1Sám 21 = 1, Jób 40 = 5, Préd 10 = 3, Én 7 = 1, Jóel 3 = 5): a `kk_max_tabla` csak a kitöltött `igehely_mt`-jű sorokból számol, és ezekben az MT-fejezetekben csak az előző Károli-fejezet átnyúló sorai (pl. Károli 1Sám 20:43 → MT 21:1) hordoznak mt-t; a fejezet többi sora `KJV` osztályú, üres mt-vel. A „max” így 1–5, és bármely TAHOT-maximummal eltér. Ez a hiba a Károli/MT kulcskérdéstől függetlenül is fennállna.

A tényleges veszteség a klónnal pontosítandó (a BSB-fejezet → MT-fejezet `leker` a display-JSON-ból jön); a 325 vers felső becslés a mai fájl fejezetei szerint.

## 2. `fejezet_eltolasok()` (`bsb_verseltolas_diag.py`, csak a Zsoltárokra)

A TAHOT-max = KK-MT-max feltétel a régi és a mai táblán is **0** Zsoltár-fejezetben sérül. A `k` = 0..2 feltétel a BSB `text_only` versszámát kívánja: a klón nélkül nem mérhető. A brief 3.1 2. kérdésére: a mai táblán a diag a TAHOT-feltételen nem állna le; a `k`-feltétel nyitott.

## 3. `sqlite_epit._bsb_szamozas()` szimuláció (az őr nélkül, a mai `BSB_Strongs.tsv`-n)

| | régi tábla | mai tábla |
|---|---|---|
| ütközés (egy Károli-vers két különböző BSB-kulccsal) | 0 | **11** |
| „nincs ilyen Károli-vers” (eldobott BSB-vers) | 266 | 32 |
| `mt_tabla` / `azonos_feltetelezett` vers | 1 583 / 20 112 | 1 752 / 19 911 |

A 11 ütközés: az F117 hat esete (Hós 2:1–3, Jób 17:1, Jób 37:1, Péld 12:1), és az F146.2 óta öt új (**Jóel 2:28–32** ← BSB 2:28–32 azonossággal és BSB 3:1–5 `mt_tabla`-val). Vegyes (`mt_tabla` és `azonos_feltetelezett`) leképezésű BSB-fejezet 12: 1Kir 22, 1Sám 21, Hós 2, Jób 17, 37, 40, Jóel 3, Préd 10, Péld 12, Én 7, Ézs 2, 64.

## 4. A mai `BSB_Strongs.tsv` `Igehely`-kulcsa nem egységesen MT (a 3.2-höz)

A 200 Károli ≠ MT soron a BSB-vers Strong-halmazát (Jaccard) a TAHOT[Károli] halmazával vetettem össze, három jelölt BSB-kulccsal: az MT-, a Károli- és a KJV-számmal. Azonos számú jelölt egy kulcsnak számít.

| a BSB-kulcs, amelyen a BSB-vers a TAHOT[Károli]-val egyezik | sor | fejezetek |
|---|---|---|
| MT (= KJV szám) | 150 | 2Móz 35–36, Jób 17, 37, 39, Préd 9, Péld 12, Én 5–6, Ézs 3 |
| **KJV (≠ MT, ≠ Károli)** | **23** | **Hós 2** (22), Én 6 (1) |
| **Károli (= KJV, ≠ MT)** | **26** | **Jóel 2–3** |
| egyik sem (J < 0,5) | 1 | 1Sám 20:43 |

Példa: Hós 2:1 (MT 2:4, KJV 2:2): J(BSB[2:2]) = 1,00, J(BSB[2:4]) = 0,17, J(BSB[2:1]) = 0,00. Jóel 2:28 (MT 3:1): J(BSB[2:28]) = 1,00, J(BSB[3:1]) = 0,03; a BSB-ben Jóel 4 nincs.

Következmény: a mai fájlban a `Számozás`=`mt` sorok kulcsa (a WLC-vel igazolt) MT, de az `ellenorizetlen` és a `Számozás` nélküli fejezetekben a kulcs az F85.6 előtti TAHOT-számozás, amely Hós 2-ben KJV-, Jóel 3-ban Károli/KJV-szerű volt. A `sqlite_epit` `mt_kk`-ja ezeket a kulcsokat MT-nek veszi: a BSB 3:1–5 (valójában KJV 3:1–5 = MT 4:1–5) a Károli 2:28–32-re kerülne.

## 5. A mai leképezés tartalmi helyessége (BSB[kulcs] ↔ TAHOT[cél Károli-vers])

Minden BSB-versre: a mai kód szerinti Károli-cél, és a BSB-vers Strong-halmazának egyezése a cél TAHOT-versével (J ≥ 0,5 = egyezik).

| | régi tábla (erre épült a ma élő `pardes.db`, 2026-10-14) | mai tábla |
|---|---|---|
| `azonos_feltetelezett`, nem egyezik | 336 vers | 184 vers |
| `mt_tabla`, nem egyezik | 46 vers | 66 vers |
| **összesen rossz Károli-versre kerülő BSB-vers** | **382** | **250** |

A mai táblán a nem egyező versek fejezetei (≥ 3 vers): 4Móz 13 (33), 4Móz 30 (14), Hós 2 (23), Hós 12 (14), Hós 14 (9), Jób 39 (30), Jób 40 (14), Jóel 3 (5), Préd 2 (25), Préd 9 (18), Préd 10 (14), Préd 12 (14), Ézs 9 (19), Ézs 64 (11). Ezek nagyrészt a CLAUDE.md-ben felsorolt F85.6 előtti TAHOT-eltolások fejezetei (Jób 40, Préd 2, Hós 2/12, Ézs 9, 4Móz 30): a BSB-kulcs a régi TAHOT-számozást hordozza. A J < 0,5 küszöb gépi mérce; a fejezetenkénti csoportosulás rendszerszintű kulcseltérést jelez, nem fordítási eltérést.

**Ebből a 3.2-re:** a (c) út (a mai fájl, csak a `sqlite_epit` javul) a 3.4 ütközés-őrével a 11 ütközést megszüntetné, de a 250 rossz helyre kerülő verset nem: a kulcs ott nem MT, és ezt a `sqlite_epit` a fájlból nem tudja megállapítani. A 3.4-ben előírt őr (az azonosság-tartalék elvetése, ha a cél egy `mt_kk`-pár célja) a Jóel 3-ban éppen a helyes sort (BSB 2:28 = Károli 2:28) dobná el, és a hibásat (BSB 3:1 → Károli 2:28) tartaná meg.

## Mi nem mérhető a klón nélkül

- a `bsb_import` tényleges `allapot`-a (melyik BSB-fejezet melyik MT-fejezetre képez, és ebből hány lesz `illesztetlen`);
- a `fejezet_eltolasok()` `k`-feltétele;
- egy újrafuttatás kimenete (a 3.5).
