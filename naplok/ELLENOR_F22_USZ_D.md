# ELLENOR_F22_USZ_D — F22_KAROLI_STRONG_BRIEF.md 22.9, D csomag (Mt, Mk) · `194151b1..da0a8ea1` (F22.45–F22.48) · 1. kör

*Az ellenőr (`fuggetlen-ellenor`, `claude-opus-5-5`) szerepe csak olvasó (Read/Grep/Glob, Bash: git, lekerdez.py, futtat.py), ezért a jelentést a végrehajtó mentette ide, tartalmilag változatlanul (rövidítve a táblázat sorai). Amit az ellenőr nem tudott futtatni, NEM ELLENŐRIZHETŐ jelölést kapott.*

**Verdikt: ELTÉRÉS, 10 tétel.**

| pont | eredmény | indok |
|---|---|---|
| CI | **ELTÉRÉS** | `futtat.py --valtozott …`: E27 29 HIBA és E28 1 HIBA a `NYITOTT_FELADATOK.md`-n: az F22.46 a fájl teljes sorvégét átírta (979/979 sor, `--ignore-cr-at-eol` mellett 1/1). |
| P1 | OK (számok) / NEM ELLENŐRIZHETŐ („pontosan egyszer”) | Mt 18 787 / 18 898, Mk 11 751 / 11 869 token; az `egyesit.py --ellenoriz` futtatása nem volt az ellenőr szerepében. |
| P2 | OK (szúrópróba) | a `strong` oszlop nem üres, a TAGNT-sorszámmal egyezik (Mt 1:1, 1:3, 11:19). |
| P3 | OK (egységesség) / NEM ELLENŐRIZHETŐ (hash) | 206/206 sor `claude-sonnet-5-5`, `adaptive,effort=high`, `84f12ca7aafb`, `batch_ar_szamolt`. |
| P4 | OK (formailag) | `[nem TR]`: Mt 458, Mk 663; párosított 47 + 57 = 104 sor. |
| P4 tartalom | **ELTÉRÉS** (enyhe) | Mt 11:19: „fiaitól” ↔ ἔργων (G2041) lexikailag hamis; a Károli a TR τέκνων szavát fordítja. A jelentés nem mondja ki. |
| költség | OK | Mt 5,805978 + Mk 3,682739 = 9,488717 USD; futó összeg 113,019556; `PLAFON_USD` 141,53. |
| kapuhiba | OK (szám) / **ELTÉRÉS** (állítás) | Hamis az „egész köteg formátumhiba nem fordult elő”: 10 köteg (Mt 9, Mk 1) „nem érvényes JSON”; a szám nem szkriptkimenet. |
| átnézés | OK | az `atnezes.tsv`-k üresek, `kezi`/`fuggoben` 0. |
| P6 | **ELTÉRÉS** | Mt, Mk nincs a `datasetek.tsv`-ben és a `SEMA.md`-ben. |
| `[nem TR]` táblaméret | enyhe (a végrehajtó ellenőrzése: a 223 a D commitban helyes; az ellenőr a későbbi, Luk utáni munkafát látta) | |
| granularitás | **ELTÉRÉS** (enyhe) | a brief könyvenként két commitot kér, a D két könyvre egy-egy commitot kapott. |
| DT434/j | OK / **ELTÉRÉS** (formai) | a DT435 „választás” mezője „a”, az opciók (b)/(c)/(d); a Ján 1:38–51 döntése külön sor nélkül. |
| tokenszint-próba | NEM ELLENŐRIZHETŐ | bemásolt kimenet: 0 jelölt. |
| Ján 1:38–51 | OK / pontatlanság | az eltolódás igazolt; a „Károli 1:51 = TAGNT 1:50 + 1:51 eleje” helyesen: a TAGNT 1:51 egésze. |
| ApCsel 13:32–33, 24:2–3 | OK | igazolt. |
| brief fejléce / 22.9 | **ELTÉRÉS** | `allapot`, `ag`, `kovetkezo`, `ir` nem frissült. |
| ⛔ versbeosztás | **ELTÉRÉS** (a felhasználó döntse el) | a brief a felhasználó közvetlen ellenőrzését kéri, a napló orkesztrátori jóváhagyást rögzít („Vedd át a döntéseket”). |
| E17/DT3, törölt sorok, kulcstartomány, A2 | OK | sorszám-Δ és kulcsok rendben; az N-F22e valóban nyitott. |

**Súlyossági sorrend:** (1) `NYITOTT_FELADATOK.md` sorvége (CI piros); (2) hamis formátumhiba-állítás; (3) P6; (4) brief fejléce; (5) ⛔ versbeosztás orkesztrátori jóváhagyása; (6) Mt 11:19 hamis link; (7) `[nem TR]` táblaméret; (8) nem könyvenkénti commit; (9) DT435 jelölés; (10) Ján 1:51 megfogalmazás.
