# KAROLI_MODERN zárás (F96)

*scope=adat/karoli_modern/karoli_modern.tsv (599 367 token) + karoli_modern_versek.tsv (31 158 vers) | forras=eszkozok/karoli_modern/karoli_modern.py (a .1 helyesiras.py, a .2 igealak.py kimenetére) + naplok/ELLENOR_F96*.md | ts=2026-10-25*

- **Kiadott réteg:** a Károli 1908 modernizált szövege, helyesírás + igealak (DT128). A szókincs, szórend, írásjel és betoldás-jelölés változatlan. 50 517 változó token, 21 621 változó vers.
- **Kulcs:** vers + `tokenizal`-sorszám. A Strong nem változik, a réteg nem tárol Strongot (DT305, DT314). A K3b: mind a 418 633 Strongos token kulcsa a táblában van, a kieső tokenek a gazdaszón át illeszthetők.
- **Önellenőrzés:** a K2 (újratokenizálás, írásjel-váz) és a K3 minden versen teljesül.
- **K1:** a cserék pontossága a mintákon 0 hiba (`igealak_minta.tsv`, `igealak_minta2.tsv`).
- **Lefedettség:** igealakra 94,8% a független ellenőr friss mintáján (92 csere, 5 kihagyás; `naplok/ELLENOR_F96.md` 4. kör). A minta2 véletlen rétegének 100%-a torzított (napló 14.4, 15.2).
- **LLM** (Claude Code subagent, előfizetésből, API nélkül; a token a hívásnaplókban):
  - sonnet: 1,42 M;
  - opus: 0,31 M (vitatott) + 0,60 M (3. kör) + 0,28 M (4. kör) + 0,29 M (5. kör).
- **Döntések:** DT-F96b–v, mind 🟢 (helyőrző, végleges szám a main-en).
- **Független ellenőr:** 4 kör, `naplok/ELLENOR_F96.md`. Utána két javítókör (`ELLENOR_F96_2`, `_3`), a korlát betelt; az utolsó dokumentációs tétel a zárásban javítva.
- **Maradék:** N-F96h (napló 16.); a betöltés és a kereső a #137 (`F137_KAROLI_MODERN_DB_BRIEF.md`).
