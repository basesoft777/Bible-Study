# ELLENOR_F22_Abd — F22_KAROLI_STRONG_BRIEF.md (D39, v2.33), `b622b928..7517136d` (plusz a merge-feloldás `a9b6b9ba`)

*A független ellenőr (`fuggetlen-ellenor` subagent, friss kontextus, 2026.10.11) jelentése. Írásra nem volt eszköze, a fájlt a fő session mentette el, tartalmilag változtatás nélkül, rövidítve. Ág: `claude/f22-abd` (külön worktree); commitok: `08c37b21`, `099d5e1a`, `a9b6b9ba` (merge), `7517136d`.*

ELTÉRÉS: 2 tétel

## Igazolt (saját lekérdezéssel)

- **21/21 vers, 1 fejezet:** a `Karoli_1908.tsv` `^Abd ` sorai 21; minden versnek van hu 1 és er 1 sora (42); csak `Abd 1:` kulcs van.
- **parok_Abd 446:** 448 sor = proveniencia + fejléc + 446; mind `alacsony / S`.
- **szavak_Abd 867:** hu 433 (348 `parositva`, 85 `betoldas`), er 434 (410 `parositva`, 24 `forditatlan`); er = a `TAHOT_kivonat.tsv` `^Abd ` sorai; `kezi` / `fuggoben` nincs.
- **Kapuhiba 0/21, nincs javító kör:** a 3 Abd-sor `probalkozas=1`; az átnézési fájl csak fejléc.
- **Költség:** 0,075001 + 0,044185 + 0,005962 = 0,125148 USD; tokenek 26 778 / 19 674; plafon 1,00 (minimum); versenként 0,00596. A futó összeg a Préd utolsó sorától (79,103940) indul, monoton, 79,229088-cal zár.
- **A régebbi futásnapló- és batch-sorok bájtra változatlanok** (`git diff --numstat`: futásnapló 3/0, batchek 1/0, jóváhagyási napló 1/0, adattábla-törlés 0).
- **Merge-feloldás:** a `tokenek.py` tuple vége `…, 'Jón', 'Náh', 'Préd', 'Abd')`; a `batchek.tsv`, `futasnaplo.tsv`, jóváhagyási napló mindkét oldal sorait tartalmazza, duplázás és konfliktusjel nélkül.
- **Versbeosztás:** a `versmegfeleltetes*.tsv`, `versosszevonas.tsv` fájlokban 0 Abd-sor; a jóváhagyási naplósor a diffben.
- **Jóváhagyás időrendje:** a jóváhagyó commit (16:51:32Z) 5 másodperccel az 1. batch (16:51:37Z) előtt készült.
- **K9:** `adat/datasetek.tsv` 8 sor (8/8 csere), `adat/SEMA.md` 2.20 (1/1 csere); a Préd megmaradt, az Abd hozzáadva, duplázás nincs.
- **A 11 megmaradt kis könyv:** 1 203 vers (117 + 154 + 195 + 73 + 146 + 105 + 56 + 53 + 38 + 211 + 55); parok-fájl egyiknek sincs; a Hós 1:11 és 11:11 beolvasztása a `versosszevonas.tsv`-ben megvan, a többi 10 könyvé nincs.
- **Szúrópróba (lekerdez.py scan):** H5662, H2377 (Abd 1:1), H4410, H8199, H6215 (Abd 1:21): n=1 mind. **Régi arany:** `^Oba` a `Karoli_Strong_kivonat.tsv`-ben 0, ezért nincs mért érték. **Kulcs-grep, CI-eszköz:** E2–E16, E19, E20, E26: 0; E25: 3 és E27: 33, repószintű; E12–E15: 0.

## ELTÉRÉS

1. **DT72 / D19 (közepes), LEZÁRVA a D40-nel (a felhasználó döntése, 2026.10.11):** az `a9b6b9ba` merge a futásnapló 3 Abd-sorának `futo_osszeg_usd` értékét átírta (77,83… → 79,17…). Az új értékek számszerűen helyesek, a régi sorok érintetlenek, de a D19 (DT72) szerint a futásnapló csak kifejezett jóváhagyással írható át, és a saját ágon lévő, még ki nem adott sorokra nincs kivétel. Lezárás: a felhasználó kivételt hagyott jóvá a D19 alól (brief D40, v2.34): a main-re még be nem került, saját ágon lévő sorok futó összege a main beolvasztásakor a main utolsó sorához igazítható; a main-en lévő sorok csak kifejezett jóváhagyással írhatók át, és a beolvasztás után a diff a main-hez képest csak hozzáfűzés lehet.
2. **D39 sor (alacsony), javítva:** a „többi hiányzó könyv nagyobb: Hag 38, Náh 47, Jón 48, Hab 56 …” felsorolás két kész könyvet (Náh, Jón) mutatott hiányzóként, és kihagyta a Sof (53) és a Mal (55) könyvet. Helyesen: „Hag 38, Sof 53, Mal 55, Hab 56 …”. Az „Abd a legkisebb hiányzó” állítás igaz.

## Nem ellenőrizhető a szerepkörből

A futó összeg és az összes `api_termeles/` sor költségösszegének egyezése (a teljes oszlop összegzése), a chatben adott jóváhagyás („mehet a következő könyv”, majd „Abdiás”), a K3 hash viszonya a `prompt_v3.sha256`-hoz, a K2/K7 teljes köre (`egyesit.py`), a CI-jelentés összevetése és az E27 maradék 30 tétele (a kimenet csonkolt).
