# F32 (KONTEXTUS) — zárójelentés

- **Ág:** `claude/f32-kontextus` · modell: sonnet · ellenőr: `naplok/ELLENOR_KONTEXTUS.md` (2 kör; 1. kör 6 eltérés, 2. kör 4 eltérés, mind kezelve).
- **Kész:** négy kontextus-őrzési szabály; `munka` mező; `feladatok.py csomag` és `OLVAS_HIANY`; új brief `munka` nélkül motívumot írva E18 hiba; az F23 brief kiegészítve (`fugg: [32]`, ⛔ az M0 után); 20 teszt a CI-ben; DT-F32a 🟢 (a #12 kettéválik), DT-F32b 🟢 (értelmező modell: opus), DT-F32c 🟢 (1. opció); K3.2 korlát rögzítve.
- **Egyeztetett elfogadás (2026.10.04):** K5 1. opció az F23 ⛔ ponttal, az 1–3. javaslat, a teszt-követő tétel; DT-F32c 1. opció.
- **DT-F32c alkalmazása:** az F09/F36 előzmény-kivétel marad (`FIGYELEM`, a CI nem törik), de a `jeloltek` a `munka` mező kitöltéséig kihagyja őket, és a `/kovetkezo` nem ajánlja őket.
- **Javaslat a /befogad-hoz:** a #12a önálló brief (munka: ertelmezo, Opus); gépi motívum→tanulmány megfeleltetés a K3.2-höz; az F09/F36 `munka` mezőjének kitöltése.
- Az `allapot` `lezarva`; merge a felhasználótól.
