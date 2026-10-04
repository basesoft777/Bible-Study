# F22 — Józsué: zárójelentés

*Ág: `claude/f22-jozs` · 2026.10.04 · orkesztrátor: Opus; kötegek: `vegrehajto-sonnet` (66 subagent, sorban); ellenőr: `fuggetlen-ellenor`*

- **Mi történt:** a Józsué (658 vers, 66 köteg) Károli–Strong párosítása csak Sonnettel (D12, DT-F22c), a felhasználó jóváhagyásával („mehet a Józsué”); a detektor szerint tiszta könyv, jóváhagyott listára véve.
- **Eredmény:** `parok_Jozs.tsv` 15 023 link, `szavak_Jozs.tsv` 30 405 token (hu 14 668, er 15 737 = TAHOT), mind `alacsony`/`S`; kapuhiba első próbára 6/658, végleg 0; `egyesit.py --ellenoriz` rendben, az újraépítés bájtra azonos; régi arany 5/5.
- **Keret:** heti „all models” 9% → 13% (4 pont).
- **Ellenőrzés:** `naplok/ELLENOR_F22_Jozs.md` — ELTÉRÉS: 1 (közepes): a SEMA 2.20 jóváhagyott-könyv felsorolásából hiányzott a Józs; javítva (F22.28).
- **Eljárási megjegyzés:** az 53. köteg subagentje a megbízásán túl segédszkriptet írt a nem verziózott `f22/_munka/` alá; a mentett válasz kapun átment, Strongot nem tartalmaz.
- **Brief-fejléc:** `allapot: megallt`, `kovetkezo`: „Te: a Józs PR merge-e, és döntés a következő könyvről (⛔ 2.)”.
- **Nyitott:** a C-futás (bizonyosság-jelölés); Jób előtt döntés az 1:2 / 2:1 támogatásról; Ézs 9:17–20 megfeleltetése hamis; a zárt összevetés (`zart_osszevet.py --konyv Józs`) a felhasználóé.
