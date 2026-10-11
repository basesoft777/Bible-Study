# F22_1Kir_jelentes.md — Károli–Strong párosítás: 1Királyok (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv 1Kir`, `egyesit.py --konyv 1Kir` és `--ellenoriz`, `f22_elemzes.py --konyv 1Kir`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` 1Kir-sorainak összesítése: `futas = api_termeles/high/1Kir`, `cimke = 1kir`). Ág: `claude/f22-1kir`. Módszer: `prompt_v3` változatlanul, Sonnet a Message Batches API-n, `effort=high` (DT73 (a)), a C (Gemini) kimarad (DT-F22c), 10 verses kötegek.*

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint az 1Kir tiszta (817/817 vers, 22 fejezet), a listában nincs sora; nincs kézi javítás, nincs 1:2 / 2:1 beolvasztás. A `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve (`'1Kir'`).
- **Minta:** `f22/minta_1Kir.tsv`, 817 vers, 82 köteg.
- **Batchek** (`f22/api_termeles/batchek.tsv`): 1. kör `msgbatch_01RJgdMzbpW5oGEwUNSeox85`, 82 kérés; javító kör `msgbatch_01EoT7P2PY1VvPw9SL1GyawP`, 15 kérés.
- **Futásnapló:** 97 sor (82 + 15), összköltség 6,252 USD (könyvplafon: 9,07 USD).
- **Kapu:** első próbára 27/817 vers (3,3%) bukott, a javító kör után végleges kapuhiba 0/817.
- **Egyesítés:** `adat/karoli_strong/parok_1Kir.tsv` 19 827 sor, `szavak_1Kir.tsv` 39 945 sor, mind `alacsony` bizonyosságú (egy modell, nincs egyezés-alapú `magas`); átnézési sor: 0 vers. `egyesit.py --ellenoriz`: rendben.
- **Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`): 5 hármas, mind egyezik (5/5); a minta kicsi, ezért nem általánosítható.

**Nyitott (a felhasználóé):** a független ellenőr (`naplok/ELLENOR_F22_1Kir.md`, ⛔ 2.), PR, ready és merge. A `f22/api_termeles/high/_munka/1Kir_k*.json` a kapuhibás kötegek hibaüzenetei.
