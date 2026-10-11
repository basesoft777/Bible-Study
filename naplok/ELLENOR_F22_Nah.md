# ELLENOR_F22_Nah — F22_KAROLI_STRONG_BRIEF.md (D37, v2.31), `85fa874c..4201930a`

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-nah` (külön worktree); commitok: `8c849149`, `f8208e71`, `4201930a`.*

TISZTA

## Igazolt (saját lekérdezéssel)

- **47/47 vers, 3 fejezet:** a `Karoli_1908.tsv` `^Náh ` sorai 47; csak az 1–3. fejezet van; minden versnek van hu 1 sora; a `valaszok/sonnet/Nah.jsonl`-ben mind a 47 vers `ok`.
- **parok_Nah 850:** 852 sor = proveniencia + fejléc + 850; mind `alacsony / S`.
- **szavak_Nah 1 641:** hu 813 (679 `parositva`, 134 `betoldas`), er 828 (792 `parositva`, 36 `forditatlan`); hu = a `minta_Nah.tsv` `karoli_szo` összege (265 + 218 + 330), er = `eredeti_szo` összege (259 + 225 + 344) = a `TAHOT_kivonat.tsv` `^Náh ` sorai; `kezi` / `fuggoben` / `magas` 0.
- **Kapuhiba 1/47 → 0:** Náh 1:13 (k2); a javító kör `kapuhiba_db` 0 / `igen`; az átnézési fájl csak fejléc.
- **Költség:** 1. kör 0,235636, 2. kör 0,014637, összesen 0,250273 USD; tokenek 48 516 / 37 424 és 11 687 / 590. Kumulatív 77,757624 USD: a 6 Nah-sor `futo_osszeg_usd` értéke a 77,507351-ről indul, mind = előző + a sor költsége. Plafon 1,00 (minimum); versenként 0,00533.
- **Batchek:** 5 + 1 kérés, 15:56:03Z és 15:58:46Z. **Prompt-hash:** mind `84f12ca7aafb` (azonos a korábbi könyvekével).
- **Versbeosztás:** a `versmegfeleltetes.tsv`, `versmegfeleltetes_kezi.tsv`, `versosszevonas.tsv` fájlokban 0 Náh-sor; a jóváhagyási naplósor a diffben.
- **Szúrópróba (lekerdez.py):** H5210 (Náh 1:1) n=1, H1319 (Náh 1:15) n=1, (Náh 2:1) n=0; a Károli 1:15 = MT 2:1 kulcs helyes.
- **K9:** `adat/datasetek.tsv` 8 sor (8/8 csere, a 4 parok-sor jelentéslistájában a Náh), `adat/SEMA.md` 2.20; a korábbi könyvek megmaradtak, duplázás nincs. **`tokenek.py`:** `…, 'Dán', 'Ruth', 'Jón', 'Náh')`.
- **Jóváhagyás időrendje:** a jóváhagyó commit (15:55:57Z) 6 másodperccel az 1. batch (15:56:03Z) előtt készült.
- **A 13 megmaradt kis könyv:** 1 445 vers; parok-fájl egyiknek sincs; a Hós (1:11, 11:11) és a Préd (2:26) 2:1 beolvasztása a `versosszevonas.tsv`-ben megvan, a többi 11 könyvé nincs.
- **Sorrend-indoklás:** nem tartalmaz memóriából írt állítást; a PR-hivatkozások (#274, #275, #277, #279, #280, #281) mind mergelt commitok a base-ben. **D36:** a base-ben megvan; az ág külön worktree-ben áll.
- **Kulcs-grep, CI-eszköz:** E2–E16, E19, E20, E26: 0; E25: 3 és E27: 33, repószintű, nem e diffből; E12–E15: 0.

## ELTÉRÉS

Nincs.

## Nem ellenőrizhető a szerepkörből

A K3 hash viszonya a `f21p/prompt_v3.sha256`-hoz (a `84f12ca7aafb` nem a fájl hash-ének előtagja, valószínűleg az összeállított kérésé; a korábbi könyvekkel azonos), a chatben adott jóváhagyás (a „mehet a Nehémiás” idézet a D31-ével azonos, a Náhumhoz a pontosító „Náhum” válasz köt), a K2 és K7 teljes köre (`egyesit.py`; a fő session futása: „rendben”), a detektor „tiszta” ítélete, a régi arany hiánya (az `f22_elemzes.py` futása), a futás helye (a futásnapló nem rögzít útvonalat), a CI-jelentés összevetése.
