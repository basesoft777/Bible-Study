# F84_zaras.md — #84 TAHOT_JOB41 zárójelentés

*2026.10.09 · ág: `claude/f84-tahot-job41` · modell: sonnet (`vegrehajto-sonnet`) · jelentés: `naplok/F84_jelentes.md` · ellenőrzés: `naplok/ELLENOR_F84.md`*

**Eredmény.** A `TAHOT_kivonat.tsv`-be 332 sor került (Károli Jób 41:1–34, Károli-kulccsal), a Jób 40:24 után, a Jób 42:1 elé; a meglévő 468 968 sor bájtazonos, a tábla 469 300 adatsor. A `TAHOT_kivonat_nyitott_esetek.tsv`-ből ugyanez a 332 sor törlődött, a fejléc maradt. A 34 vers Strong-halmaza egyezik a Macula MT-versével (Jaccard min. 0,83; az eltérés a H4480 előtag TAHOT-kezelése). A `lekerdez.py scan H3882 --szakasz "Jób 41:1-41:34"` → Jób 41:1.

**Döntés** (felhasználó, chat, 2026.10.09): DT-F84a (a) 1 — törlés a nyitott fájlból; (b) 1 — a Jób 41:25 jelölés nélkül bekerül (az „összeolvadt vers” jelölés elavult).

**Dokumentáció.** CLAUDE.md TAHOT-mondata a mért állapotra (maradó korlát: a Jób 40 MT-kulcsú számozása); README mérettábla; generátor-megjegyzés ([javaslat]: `ELSODLEGES` a 41-re); N-F83a és N-F34b lezárva (helyőrzővel).

**Ellenőrzés.** 4 eltérés; a README, a pótló szkript hatástalan őre és a brief-fejléc az F84.4-ben javítva.

**Nyitott (a #22-é).** Az `f22/versmegfeleltetes.tsv` (generált, ts=2026-10-02) 26 Jób 41-es verset ma is `nincs_eredeti`-nek jelöl: a `versbeosztas.py`-t a Jób-menet előtt újra kell generálni. Addig a brief `ad`-jának „a #22 egy menetben futtathatja” része nem igazolt. A #41 BSB `Számozás` oszlopának Jób 41 `kjv`-jelölése az N-F41g-hez megy.
