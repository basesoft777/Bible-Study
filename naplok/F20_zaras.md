# F20 — zárójelentés

*2026.09.30 · ág `claude/befogadas` · brief `F20_BEFOGADAS_BRIEF.md` v1.3 · ellenőrzés `naplok/ELLENOR_F20.md`*

- **Kész:** B0–B8. `eszkozok/feladatok.py` (general, ellenoriz, fuggesek `--extra`, atvetel, kovetkezo_szam) 42 teszttel; 40 brief fejléccel (#1–#5 átnevezve, 12 csonk, 20 archív); a FELADATOK.md táblái generáltak; `/befogad` új, a `/kovetkezo` fejlécet ír; BRIEF_SABLON.md, `beerkezo/`; E18 CI-job és `main`-re futó Action; `beerkezo/` kimarad a CI-ből.
- **Próba:** `naplok/F20_proba.md` (a–e és a `/kovetkezo` eset megfelelt; a (d) eset „jelölést javasol” elvárása indokoltan nem teljesült; E18 mindhárom mutációt megfogja).
- **⛔ felhasználói teendő (beállítás):** a `main` védett (PR kötelező, admin sem kerülheti meg), ezért a `feladatok.yml` push-a nem megy; az E18 (`feladatkovetes` job) sem kötelező check. Megoldás (a felhasználó dönt): ruleset-bypass a `github-actions` számára, vagy az Action PR-t nyisson; az E18 felvétele a kötelező check-ek közé. A beállításhoz nem nyúltam.
- **Jóváhagyandó eltérések:** a jel 🔎 (a másik nagyító az E2 jelölése); E18 E17 helyett; a (d) próba eredménye.
- **Merge után:** a `main`-re futó Action első futása várhatóan ⛔ (l. fent); az E18 tiltja, hogy PR a generált blokkot írja, ezért a blokk frissítése a védelem/Action-beállítás rendezéséig (a felhasználó döntése) nem megoldott: a blokk a B4 állapotán áll.
- **Nem része:** a Takarítás többi tétele; a csonkok valódi briefje (F07, F08, F10–F13, F16–F19).
