# ELLENOR_F22_Pred — F22_KAROLI_STRONG_BRIEF.md (D38, v2.32), `7953519e..2b3fb0b7`

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-pred` (külön worktree); commitok: `620225d7`, `1a1e56f0`, `2b3fb0b7`.*

TISZTA

## Igazolt (saját lekérdezéssel)

- **221/221 vers, 12 fejezet:** a `Karoli_1908.tsv` `^Préd ` sorai 221 (Préd 1:1–12:16, a 13. fejezet nincs); minden versnek van hu 1 és er 1 sora.
- **parok_Pred 4 440:** 4 442 sor = proveniencia + fejléc + 4 440; mind `alacsony / S`; a fejezetenkénti linkszámok összege 4 440.
- **szavak_Pred 9 114:** hu 4 659 (3 636 `parositva`, 1 015 `betoldas`, 8 `fuggoben`), er 4 455 (4 062 `parositva`, 384 `forditatlan`, 9 `fuggoben`); er = a `TAHOT_kivonat.tsv` `^Préd ` sorai (4 455).
- **A 17 `fuggoben` / `kezi` token** mind a Préd 2:26-ból való (hu 1–8. szó „Mert kicsoda ehetnék és élhetne gyönyörűségére rajtam kivül” és a TAHOT 2:25 tokenjei, H3588 H4310 H0398 H9002 H4310 H2363 H2351 H4480 H9030); a TAHOT `Préd 2:26` sorai 47 = 38 + 9.
- **Kapuhiba 4/221 → 0:** Préd 1:2 (k1), 1:16 (k2), 5:6 (k9), 8:8 (k15); a javító kör négy sora `kapuhiba_db` 0 / `igen`.
- **Költség:** 1. kör 1,268193, 2. kör 0,078123, összesen 1,346316 USD; tokenek 236 788 / 206 281 és 46 953 / 6 234; kumulatív 79,103940 USD (a Náh utolsó sora 77,757624), a 27 sor monoton. Plafon 2,45; versenként 0,00609.
- **Batchek:** 23 + 4 kérés, 16:17:13Z és 16:21:41Z. **Prompt-hash:** mind az 1 521 `api_termeles/` sor `84f12ca7aafb`.
- **Versbeosztás:** a `versmegfeleltetes.tsv`, `versmegfeleltetes_kezi.tsv` fájlokban 0 Préd-sor; a `versosszevonas.tsv`-ben pontosan egy (14. sor), a diffben változatlan; a jóváhagyás (2026.10.09, F85.10, DT92) a `naplok/F85_jelentes.md:250` és a `DONTESEK.md:167` szerint megvan; az átnézési fájl 1 sora Préd 2:26.
- **Jóváhagyó commit időrendje:** `620225d7` (16:16:57Z) 16 másodperccel az 1. batch (16:17:13Z) előtt.
- **K9:** `adat/datasetek.tsv` 8 sor (8/8 csere, nincs új sor, nincs duplázás), `adat/SEMA.md` 2.20; a korábbi könyvek megmaradtak. **`tokenek.py`:** `…, 'Ruth', 'Jón', 'Náh', 'Préd')`.
- **A 12 megmaradt kis könyv:** 1 224 vers; parok-fájl egyiknek sincs; beolvasztás csak a Hós 1:11 és 11:11 (a `versosszevonas.tsv` 12–13. sora).
- **Régi arany 0/1:** az `Ecc.9.10 H7585 „a Seolban”`; a Károli-datasetben a „Seolban” a `Préd 9:12`-ben áll (`Préd 9:10`: „A te ruháid mindenkor legyenek fejérek…”), a `parok_Pred.tsv`-ben `Préd 9:12 Seolban → H7585`, a `lekerdez.py scan H7585` ugyanezt adja. A „kulcs-műtermék” indoklás tényszerű (`NYITOTT_FELADATOK.md:72` N-F85c és :521–523 N-F08a); az `Ecc.9.10` nincs az `f21p/regi_arany_hibas.tsv`-ben, ezért a javaslat külön tétel.
- **Sorrend-indoklás:** nem tartalmaz memóriából írt állítást. **D36:** az ág a külön worktree-ben áll, API Batch mód (`batch_ar_szamolt`).
- **Kulcs-grep, CI-eszköz:** E2–E16, E19, E20, E26: 0; E25: 3 és E27: 33, repószintű, nem e diffből; E12–E15: 0.

## ELTÉRÉS

Nincs.

## Megjegyzések (nem eltérések)

- A Préd 2:26 er-sorszámai (39–47) nem a TAHOT-kulcson elfoglalt helyet (1–9) követik; ez a dokumentált konvenció (`naplok/F85_jelentes.md:280`).
- Az `adat/SEMA.md` `kezi` példalistájából hiányzik a Préd 2:26 (csak példa, „pl.”).

## Nem ellenőrizhető a szerepkörből

A chatben adott jóváhagyás („mehet a Prédikátor”), a K2 és K7 teljes köre (`egyesit.py`; a fő session futása: „rendben”), a távoli CI-állapot, a `84f12ca7aafb` és a `prompt_v3.sha256` viszonya (a korábbi könyvekkel azonos), hogy a munka a futás teljes ideje alatt a worktree-ben folyt.
