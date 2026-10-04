# F32 (KONTEXTUS) — zárójelentés

- **Ág:** `claude/f32-kontextus` · modell: sonnet · ellenőr: `naplok/ELLENOR_KONTEXTUS.md` (2 kör; 1. kör 6 eltérés, 2. kör 4 eltérés, 1 nyitott).
- **Kész:** négy kontextus-őrzési szabály; `munka` mező; `feladatok.py csomag` és `OLVAS_HIANY`; új brief `munka` nélkül motívumot írva E18 hiba; az F23 brief kiegészítve (`fugg: [32]`, ⛔ az M0 után); 19 új teszt a CI-ben; DT-F32a 🟢 (a #12 kettéválik), DT-F32b 🟢 (értelmező modell: opus); K3.2 korlát rögzítve.
- **Egyeztetett elfogadás (2026.10.04):** K5 1. opció az F23 ⛔ ponttal, az 1–3. javaslat, a teszt-követő tétel.
- **⛔ Nyitott döntés:** DT-F32c (🟡) — az F09/F36 `MUNKA_ELOZMENY` kivétel (a végrehajtás saját döntése) marad-e.
- **Javaslat a /befogad-hoz:** a #12a önálló brief (munka: ertelmezo, Opus); gépi motívum→tanulmány megfeleltetés a K3.2-höz; az F09/F36 `munka` mezőjének kitöltése.
- Az `allapot` `dontesre_var` a DT-F32c-ig.
