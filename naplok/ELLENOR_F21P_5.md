# ELLENOR_F21P_5.md — F21_KAROLI_STRONG_PILOT_BRIEF.md · 5. kör (DT21 f–k átvezetése, h/i javítás) · `28a5cd2..dd3b66c` (7b1cfa9, 1c3a03e, dd3b66c)

*A `fuggetlen-ellenor` 5. körös jelentése; a fájlba az orkesztrátor mentette (az ellenőrnek nincs fájlíró eszköze). Ítélet: **hiba és figyelmeztetés nélkül** — megjegyzés: 2 (az 1. az ellenőrzés után javítva: a `f21p/regi_arany_hibas.tsv` `# MANUAL:` fejléce `ts=` mezőt kapott). A mérő- és vetítő szkriptek újrafuttatása a szerepkorlát miatt nem volt ellenőrizhető; mindent kódolvasással és a generált TSV-kből vett kézi számolással ellenőrzött.*

| pont | eredmény | indok |
|---|---|---|
| 1a i): mért = kizárás nélküli, a kizárásos tájékoztató | OK | C (F3V2 és F3V2B): „MÉRT” 30/32 = 93,8%, „TÁJÉKOZTATÓ” 30/31 = 96,8%; A+B: 18/32 és 18/31; A+B+C: 28/32 és 28/31 (a 13:4 nem-egyezésként visszakerült, a nevező +1, a számláló változatlan). A jelentés: „mért (kizárás nélkül) 93.8% (30/32) — a 95% alatt; … 96.8% (30/31) (tájékoztató, nem minősít)”. |
| 1b a kód a mért értékkel minősít | OK | `meres_p3b.py`, `meres_v2.py`, `meres.py`, `c_diff.py`: a `feltetel['3']` a kizárás nélküli értékből jön, a „tájékoztató” minősítés-sor külön kulccsal; a `regi_hibas()` átugorja a `#`-sort. |
| 1c a régi 100% (30/30) csak a történetben | OK | Grep: egyetlen találat a `F21P_meres_v1.md:83`, egy nem kapcsolódó kapuhiba-keresztellenőrzés (30/30). |
| 1d `regi_arany_hibas.tsv` | OK / megjegyzés | Csak az 1Móz 6:17 sor maradt; a 13:4 kikerült, a fejléc jelöli. A `# MANUAL:` fejlécből hiányzott a `ts=` mező — **javítva**. |
| 1e `c_regi_arany_besorolas.tsv`: a 13:4 osztálya | OK | (d)→(b), „VISSZAVONT (d)-jelölés (DT21 i, felhasználói döntés): vitatható …”; osztályonként: (b) 1, (d) 1, (e) 6. |
| 2a h): a rétegbesorolás | OK | `koltseg_vetit.py`: ÓSZ-próza 17 könyv (Ruth és Eszt is), költészet 6 (Jób, Zsolt, Péld, Préd, Én, Sir), próféta 16 (Dán is), evangélium+ApCsel 5, levél+Jel 22; összesen 66; kettős fedést `assert` zárja ki. |
| 2b a „Sir” jelentése | OK | `konkordancia/Konyv_normalizalo_tabla.tsv:26`: `Lam Sir Jeremiás siralmai` — a Sir a Siralmak. |
| 2c versszám | OK | 12871+5001+5332+4785+3169 = **31158**; a pilot-4 besorolással konzisztens (ÓSZ 23204 = 14006+3712+5486; ÚSZ 7954). |
| 2d pilot-4 tájékoztató bitre | OK | A+B+C 85.7455 [79.6322–92.3303], C (F3V2) 42.0298 [38.1586–46.2713], A 22.8348, B 5.1197, A+B 27.9545; P3: F3 42.2328, F3V2 42.0298. Mind azonos a korábbi körökével. |
| 2e F22-értékek, belső konzisztencia | OK | A 22.8359 + B 5.1204 = 27.9563 (A+B); 27.9563 + döntőbírói rész 57.9511 = 85.9074 [79.5981–92.6267]; C 42.0329. |
| 2f g): leave-one-out | OK | F1V2 −0,111, F2V2 −0,276, F3V2 −0,148, F3V2B −0,077, F4V2 +0,321, F3 −0,149. |
| 3a brief | OK | `lezarva_osszegzes` egy sor, „85,91 USD [79,60–92,63]”; PD12 jelzi a PD9 módosítását; v1.5 megvan; a PD9 és a v1.2 sor változatlan (történeti). |
| 3b DONTESEK | OK | `git diff --numstat 28a5cd2..HEAD -- DONTESEK.md` → csak a DT21 sor; DT21 🟢, az a–e regressziós mérésre vár; DT22 ✅; DT5, DT6, DT7, DT18, DT19, DT20 érintetlen. |
| 3c zárás | OK | `naplok/F21_zaras.md` 15 sor; nincs benne ellentmondó régi szám (85,75; 60,0%; PD9-cel 100%; „DT21 f, nyitott”; „a–k”). |
| 4a nulla-diff | OK | `git diff --numstat 28a5cd2..HEAD -- adat konkordancia FELADATOK.md` + az összes befagyasztott fájl + `f21p/valaszok` + `f21p/futasnaplo.tsv` + `.github` → 0. |
| 4b régi számok a jelentésben | OK | Csak a kizárásos 100% (30/30) és 60,0% (18/30) tűnt el, az orkesztrátor döntése szerint; a többi régi szám megvan. |
| 4c kulcs-grep | OK | 0 találat. |
| 4d CI | OK | `eszkozok/ellenorzes/futtat.py … --pr-cim "[ELLENŐRZŐ] F21: …"` → minden szabály 0 találat (fej: dd3b66c). |
| 5a–5c az orkesztrátori döntések | OK | A 13:4 a (b) osztályban marad; a régi 100% nem kerül vissza (a git-történetben és az ellenőri jelentésekben visszakereshető); az A+B+C összesített ellenőrzése mintán belüli, jelölve. |
| Szkriptek újrafuttatása | NEM ELLENŐRIZHETŐ | Szerepkorlát. |
| 6 régi commit-üzenetek (75496f0, 6d94610, ac6fb49) | megjegyzés, elfogadva | A történet nem íródik át. |

**Hiba és figyelmeztetés nélkül.** (Megjegyzés: 2 — egy javítva, egy elfogadva.)
