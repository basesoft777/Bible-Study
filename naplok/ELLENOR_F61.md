# ELLENOR_F61 — F61_LEKERDEZ_NAPLO_BRIEF.md · `origin/main...HEAD` (claude/f61-lekerdez-naplo, 65b63737)

*Független ellenőr (fuggetlen-ellenor), 2026-10-11. A jelentést fájlba az orkesztrátor mentette (az ellenőrnek nincs íróeszköze); az X1 mérését az orkesztrátor végezte el ideiglenes másolaton.*

Az ág a main mögött jár (F22.Ruth, #280): a kétpontos diff ezért törlésként mutatja a Ruth-fájlokat. Az ág saját változása a háromtagú diff: 7 fájl, +388/−16.

| pont | eredmény | indok |
|---|---|---|
| D (DT-M3, DT-M7, nem_fugg 55) | OK | `lepes` = `A5\|B2\|B3\|B4\|adhoc`, `csatorna=cli` a proveniencia-sorban; nincs MCP-fájl |
| D (DT-F61a (1), három ág) | OK | `naplo_celfajl`; `NINCSILYEN-999` → hiba, exit 1; a `PILOT-…` ág feltételes, nincs használatban, a teszt hibát vár rá |
| D (DT-F61a (2), csatorna) | OK | `ellenoriz.py:48` halmaz: `strong`, `n`, `csatorna` |
| D (DT-F61a mellékhatás) | **ELTÉRÉS** | az N-F helyőrző a `naplok/*_lekerdezesek.tsv` formai ellenőrzésére nem került a `NYITOTT_FELADATOK.md`-be |
| K1 (minden alparancs) | OK | 8/8 alparancs `parents=[szulo]`, `futtat_naplozva` |
| K1 (kapcsoló nélkül bájtra azonos) | részben ellenőrizve | az M1 ügynök mérése szerint azonos; az ellenőr a régi kimenettel nem vetette össze; a `--lepes` önmagában most exit 1 (régen argparse exit 2) |
| K2 / SEMA 2.9 „utolsó sor” | **ELTÉRÉS** | `--naplo` esetén a stdout utolsó sora `# napló: hozzáfűzve -> …` (`lekerdez.py:949`), nem a proveniencia-sor; ellentmond a docstringnek (7. sor) és a SEMA 2.9-nek |
| K3 (nincs csv, csak hozzáfűzés) | OK | `"\t".join`, `split("\t")`, `open(…,"a")`; a duplikáció-szűrés a teljes sorra megy (a `ts` percre kerekített, gyakorlatilag egyenértékű) |
| K4 (CI) | **ELTÉRÉS** | E5 HIBA 13: az ág a main mögött jár (beolvasztás kell); E16 HIBA 1: a PR-címnek `[ELLENŐRZŐ]` előtag kell, mert az `ellenoriz.py` változik. `--diff-alap 871f2988` és `[ELLENŐRZŐ]` PR-címmel mindkettő 0 |
| A1, A6, Ell.1, Ell.2, Ell.4, Ell.5 | OK | nincs adatsor-változás, 5/5 lépéskód egyezik, a `szabalyok.py` nincs a diffben |
| Apróság: `_ProvFogo` | OK (látens) | a sorvég nélküli utolsó kimeneti sor a pufferben maradna; `end=` ma nincs a `lekerdez.py`-ban |

## X1 — külön kérés: `--naplo X --lepes adhoc`, X a `motivumok.tsv`-ben van, az `auditok.tsv`-ben nincs

**ELTÉRÉS, igazolva méréssel.** A `naplo_celfajl` a lépéstől függetlenül minden motívum-ID-t az `auditok.tsv`-be irányít; a `_id_szerint_provok` ezt a 8. szabály ID-listájába veszi (a `RETROAKTIV_IDK` kivétel), és a „mindig” datasetek teljes lefedését követeli.

**Mérés (orkesztrátor, ideiglenes másolat a repón kívül, mára törölve):** az `adat/` másolatán egy új, nem retroaktív motívum (`UJ-001`, a `motivumok.tsv`-be felvéve) és egyetlen `adhoc`/`tsk` sor az `auditok.tsv`-ben:

- `**8. Dataset-lefedettség (gépi)**: SÉRTÉS (3)` — `UJ-001` hiányzik: `Karoli_1908`, `Karoli_KH`, `TAHOT`;
- a CI E1 lépése (`if: always()`, exit 1 SÉRTÉSnél) ettől piros;
- a repó eredeti `adat/`-ján: SÉRTÉS 0 (az ellenőr és az M1 ügynök mérése).

**A mai adaton látens:** a `motivumok.tsv` 9 ID-t tartalmaz; az `auditok.tsv` mind a 222 sora `TEREMT-002`; a másik 8 ID az `elofordulasok.tsv`-ben szerepel és `RETROAKTIV_IDK`, náluk az adhoc sor nem ad SÉRTÉST. Az első új motívumnál jelentkezik. Nem csak az `adhoc`-ra igaz: a B2/B3 lépés is kiváltja, ha a kutatás közben, lépésenként kerül commitba.

Két lehetőség (javítás nem történt, tartalmi döntés, DT-F61b):
- **(a)** megjegyzés a SEMA 2.9 „Önnaplózás” bekezdésébe: a motívum-ID-re irányított sor a 8. szabály hatálya alá helyezi a motívumot, ezért új motívumnál az `adhoc` `F<nn>` feladatkóddal naplózandó, vagy csak teljes lefedés után commitolandó;
- **(b)** az `ellenoriz.py` 8. és 8/c szabályában a `_id_szerint_provok` hagyja ki a `lepes == 'adhoc'` sorokat (CI-ellenőrző módosítás, `[ELLENŐRZŐ]` PR).

*Megjegyzés: a másolaton a 13. szabály is SÉRTÉST adott (714) — ez a másolat műterméke lehet (a gyorsítótár-útvonal), nem vizsgáltuk; a repón a 13. szabály RENDBEN.*

## Összegzés — eltérések súlyossági sorrendben
1. X1: a 8. szabály az első új motívum önnaplózott soránál piros CI-t ad (mai adaton látens) → DT-F61b (1).
2. K2: `--naplo` esetén a stdout utolsó sora nem a proveniencia-sor → DT-F61b (2).
3. CI E5: a main beolvasztása az ágba (mechanikus).
4. CI E16: a PR-cím `[ELLENŐRZŐ]` előtaggal.
5. A DT-F61a mellékhatás N-F helyőrzője hiányzik a `NYITOTT_FELADATOK.md`-ből.
