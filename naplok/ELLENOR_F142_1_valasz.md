# ELLENOR_F142 — javítókör 1/2, válasz a 3. tételre (TÉVES)

*A `naplok/ELLENOR_F142.md` 3. tétele (elfogadási feltétel 5. pontja: a végrehajtó mérése szerint `teszt_lanc.py` 1, `teszt_bont.py` 2 hiba; hogy a main-en is fennáll-e, nincs igazolva). Az `ELLENOR_F142.md`-t ez a fájl nem módosítja.*

## Besorolás: TÉVES (a hiányzó igazolás pótolva; a hibák nem a #142 változtatásaiból erednek)

**Tétel.** `python eszkozok/thayer_jelolt/teszt_lanc.py`: 1 hiba; `python eszkozok/thayer_jelolt/teszt_bont.py`: 2 hiba (a HEAD-en, helyi futtatással újramérve: 34 teszt/1 hiba, illetve 23 teszt/2 hiba).

**Indok.** A 3 hiba azonosan megvan az `origin/main`-en is (`47c87b1`), vagyis a #142 (F142.1–F142.30) nem okozza őket:

- `teszt_lanc.py`: `Sigla.test_tabla_determinisztikus_es_kezi_vedett` (a sigla-tábla gépi újragenerálása eltér a jóváhagyott `adat/thayer_sigla.tsv`-től: `ELTÉR: adat/thayer_sigla.tsv`);
- `teszt_bont.py`: `Determinizmus.test_ellenoriz` és `Javitas.test_forras_javit_ellenoriz`.

A `teszt_bont.py` két hibáját a #133 javítja (nem a #142 hatóköre). A #142 a tesztfájlokat nem módosította, a lánc, a prompt, a javítótábla és a sigla-tábla változatlan (`ELLENOR_F142.md` „Rendben”).

**Proveniencia.** `scope=thayer_jelolt/teszt_lanc.py + teszt_bont.py, origin/main 47c87b1 vs HEAD | forras=helyi-futtatas | ts=2026-10-27`
