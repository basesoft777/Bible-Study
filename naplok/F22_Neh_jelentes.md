# F22_Neh_jelentes.md — Károli–Strong párosítás: Nehémiás (csak Sonnet, Message Batches API)

*A számok szkriptkimenetből jönnek (`f22_statisztika.py --konyv Neh`, `egyesit.py --konyv Neh` és `--ellenoriz`, `f22_elemzes.py --konyv Neh`, a `f22/api_termeles/futasnaplo.tsv` és `batchek.tsv` Neh-soraiból: `futas = api_termeles/high/Neh`, `cimke = neh`). Ág: `claude/f22-neh` (a main-ről). Módszer: `prompt_v3` változatlanul, Sonnet a Message Batches API-n, `effort=high` (DT73 (a)), a C kimarad (DT-F22c), 10 verses kötegek.*

- **Versbeosztás-jóváhagyás (2026.10.11)**, `naplok/F22_versbeosztas_jovahagyas.md`: a detektor szerint tiszta (406/406 vers, 13 fejezet), nincs kézi javítás, nincs 1:2 / 2:1 eset. Jóváhagyás: a felhasználó chatben („mehet a Nehémiás”, 2026.10.11).
- **Minta:** `f22/minta_Neh.tsv`, 406 vers, 41 köteg.
- **Batchek:** 1. kör `msgbatch_01Jiyd74KHuNJC8v3jowKste`, 41 kérés; javító kör `msgbatch_0192dYe83iCeh1vNkf2nrQWE`, 10 kérés.
- **Futásnapló:** 51 sor, összköltség 2,448 USD (könyvplafon 4,51 USD).
- **Kapu:** első próbára 36/406 vers (8,9%) bukott, a javító kör után végleges kapuhiba 0/406.
- **Egyesítés:** `parok_Neh.tsv` 8 027 sor, `szavak_Neh.tsv` 16 169 sor, mind `alacsony` (egy modell); átnézési sor 0. `egyesit.py --ellenoriz`: rendben.
- **Régi arany:** a könyvben nincs hármas (0), ezért nincs mért érték.
- **Kumulatív költség** (a futásnapló ezen az ágon): 62,08 USD; az 1Kir (PR #274) költsége (6,25 USD) a két ág egyesítése után adódik hozzá.

**Nyitott (a felhasználóé):** a független ellenőr (`naplok/ELLENOR_F22_Neh.md`, brief ⛔ 2.), a brief fejlécének és a K9 (`adat/datasetek.tsv`, `adat/SEMA.md`) bejegyzéseinek frissítése, PR és merge. A két utóbbit az 1Kir ellenőre hiányolta, ezért itt még nincs megcsinálva.
