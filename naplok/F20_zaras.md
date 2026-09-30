# F20 — zárójelentés

*2026.09.30 · ág `claude/befogadas` · brief `F20_BEFOGADAS_BRIEF.md` v1.4 · ellenőrzés `naplok/ELLENOR_F20.md`*

- **Kész:** B0–B8. `eszkozok/feladatok.py` (general, ellenoriz, fuggesek `--extra`, atvetel, kovetkezo_szam) 42 teszttel; 40 brief fejléccel (#1–#5 átnevezve, 12 csonk, 20 archív); a FELADATOK.md táblái generáltak; `/befogad` új, a `/kovetkezo` fejlécet ír és a `forras`-t olvassa; BRIEF_SABLON.md, `beerkezo/`; E18 CI-job (minden PR-on fut, nincs `paths`-szűrő) és a `main`-re futó Action; a `beerkezo/` kimarad a CI-ből.
- **Védelem (v1.4):** a `main`-t ruleset védi („main védelem”: PR kötelező 0 jóváhagyással, kötelező checkek `ellenorzes` és `feladatkovetes`, up to date, force push és törlés tiltva, bypass: csak a `pardes-feladatok` GitHub App); a klasszikus védelem megszűnt. A `feladatok.yml` az App tokenjével (`actions/create-github-app-token`, pinelt SHA) pushol; a workflow `GITHUB_TOKEN`-je `contents: read`; a többi workflow-ban sincs `contents: write` (az `f06_forrasfelmeres.yml` is `read`: újrafuttatásához, ha push kell, külön döntés).
- **Próba:** `naplok/F20_proba.md` (a–e és a `/kovetkezo` eset; a (d) eset újrafuttatva a kötelező jelölés-javaslat lépéssel; E18 mindhárom mutációt megfogja).
- **Jel:** a „lezárva, még ágon” jele 🔀 (a nagyító-jelek közül a U+1F50D nagyító az E2 „ellenőrizve” jelölése, ezért kerülendő).
- **Merge után:** a `main`-re futó Action első futása az App-tokennel várhatóan lefut; ha hibázik (titok/jogosultság), a FELADATOK.md blokkja a B4 állapotán marad.
- **Nem része:** a Takarítás többi tétele; a csonkok valódi briefje (F07, F08, F10–F13, F16–F19).
