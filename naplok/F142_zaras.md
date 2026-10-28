# F142 zárójelentés (THAYER_M3) — 2026-10-27, `claude-sonnet-5-5`

Ág: `ccr-676ffb53-9qo1to`. Lista (DT332 (1)): 13 görög Strong; fordítva az F142.4–F142.13-ban 5 (G0086, G0540, G1941, G2671, G5356), ebben a folytatásban 8.
- F142.21 G0012 · .22 G0282 · .23 G5010 · .24 G1311 · .25 G1944 · .26 G5351 · .27 G5590 · .28 G4151: mind minden gátoló kapun átment.
- Régi `teljes` sorok (DT329): nem `kezi` -> `elavult` (G0012, G1311, G5010, G5351); `kezi` -> érvényes marad (G0282, G1944, G4151, G5590).
- `bukottak.tsv`: üres (a 5 korábbi bukás a #145 kapujavításával feloldva).
- Független ellenőr (`ELLENOR_F142.md`): ELTÉRÉS 4 tétel, javítókör 1/2: G0282 sz6 újrafordítva `--kivetel Heb.`-val (F142.31); DT354 (G5351 `etc.`→`stb.`) a felhasználó döntésével (a) lezárva; a teszthibák téves tétel (`ELLENOR_F142_1_valasz.md`: mind a 3 az origin/main-en is bukik); a `DT-F132c` hivatkozás hatókörön kívül (`beerkezo/Fnn_THAYER_ELAVULT_HIVATKOZAS_BRIEF.md`).
- Mz: `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba; `teszt_forditas_kapuk.py` 90, `teszt_vers_jelentes.py` 9 zöld; `teszt_lanc.py` (1) és `teszt_bont.py` (2) hibája az origin/main-en is megvan.
- Egyeztetett eltérés: a javítókör után újraellenőrzés nem futott (a tartalmi tétel döntése után a felhasználó (a)-t választotta, további változtatás nincs).
- Nyitott: a `kezi` jóváhagyás a felhasználóé (DT290 (3)); a beerkezo-tervezet befogadása (`/befogad`).

## F142.38 — G1941 `sz3` újrafuttatás (DT-F131i, 2026-10-27)

*Végrehajtó: `claude-sonnet-5-5` (a brief `modell: sonnet`). Proveniencia: `scope=Thayer G1941 sz3 | forras=thayer_jelolt/forditas.py (lista, elokeszit, ellenoriz, rogzit, beir) | ts=2026-10-27`.*

- **Ok:** a `sz3` „nevet tenni valakire, más néven is nevezni” és „akit más néven is neveznek” nem természetes magyar (a *to put a
  name upon / to surname* tükörfordítása). A javított `adat/tiltott_fordulatok.tsv` (v2; új tétel „nevet tenni valakire”) a #131
  ágról (`ccr-6dc5ac47-lksrko`, F131.3.5) a `tiltott_fordulatok.tsv`, a `SEMA.md` és a `teszt_forditas_kapuk.py` fájlként került
  át; a #131 main-be olvasztásakor azonos tartalmú.
- **Lista:** `forditas.py lista` — G1941 `kihagyva / kesz` (érvényes szakaszsorok, régi `kezi` `teljes` sor, DT329 (ii)); az újrafutás
  tehát kézi felülírás, nem a lista `forditando` sora. Más Strong nem érintett.
- **Fordítás:** csak a `sz3`; a `sz1, sz2, sz4–sz7` szövege a meglévő sorokból változatlanul ment a vázlatba. Új alak: „nevet adni
  valakinek, elnevezni”, „akit elneveznek”, „megengedni, hogy elnevezzék”.
- **Kapuk:** `ellenoriz G1941` ATMENT — köztük `14_szakasz` (7 szakasz), `15_tiltott` (3 minta, 0 találat), `16_sigla` (28 besorolt
  sigla rendben). `rogzit` + `beir --kezi-marad`.
- **Írás:** a `beir`/`rogzit` újraírta a G1941 mind a 7 `sz` sorát (dátum) és a munkatábla sorrendjét; a `sz3`-on kívüli sorokat
  visszaállítottam az előző bájtokra: `git diff` = a `forditasok.tsv`-ben és a munkatáblában egyetlen sor (`sz3`).
- **Mérés** (`forditasok.tsv`, G1941, `sz*` sorok): „nevet tenni valakire” 0, „más néven (is) nevezni” 0, „melléknéven nevezni” 0.
  A régi `teljes` sor (`kezi`, archív, DT329) változatlan; a TBESG `1` sor is tartalmaz tiltott alakot (nem Thayer, nem érintett).
- **Ellenőrzés:** `ellenoriz.py` SÉRTÉS 0; `feladatok.py ellenoriz` 0 hiba; `teszt_forditas_kapuk.py` OK (91); a
  `thayer_jelolt/teszt_bont.py` (2) és `teszt_lanc.py` (1) hibája a változás nélküli bázison is fennáll (nem e feladat hibája; oka nem vizsgálva).
- **Nyitott:** az új `sz3` jóváhagyása a felhasználóé (DT290 (3)).
