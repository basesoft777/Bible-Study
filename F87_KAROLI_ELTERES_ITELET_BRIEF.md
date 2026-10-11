---
feladat: 87
cim: A #65 három eltérő Károli-sorának kézi ítélete (KIRALY-001 2Móz 19:6, TEREMT-001 2Móz 15:5, ALVIL-001 Jób 17:13)
kod: KAROLI_ELTERES_ITELET
tipus: feladat
fazis: 1
modell: opus
munka: adat
allapot: brief_kell
ad: a három eltérő sor soronkénti kézi ítélete (melyik Károli-szó tartozik a Stronghoz, illetve az ALVIL-001-nél a Károli-kulcs), a javítás a kanonikus sorokon döntéssel és indoklással
kovetkezo: brief írása a #65 merge-e után
olvas: [naplok/KAROLI_ELLENORZES_elteresek.tsv, naplok/KAROLI_ELLENORZES_zaras.md, adat/karoli_strong/, adat/SEMA.md, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv]
ir: [adat/elofordulasok.tsv, adat/jeloltek.tsv, naplok/KAROLI_ELTERES_ITELET.md]
fugg: [65]
---

# F87_KAROLI_ELTERES_ITELET_BRIEF — csonk

*FELADATOK #87 · csonk-brief: nem végrehajtható · forrás: a #65 (KAROLI_ELLENORZES, PR #287) eltéréslistája, felhasználói kérés 2026-10-11*

- **Mit ad, ha kész:** a #65 eltéréslistáján (`naplok/KAROLI_ELLENORZES_elteresek.tsv`) gépi javítás nélkül maradt három `elter` sor kézi ítélete, és a javítás a kanonikus sorokon (`elofordulasok.tsv`, `jeloltek.tsv`), döntéssel és indoklással:
  - KIRALY-001, 2Móz 19:6, `papok` (H3548+H4467): a gépi párokból hiányzik a H4467;
  - TEREMT-001, 2Móz 15:5, `a mélységbe` (H8415): a gépi pár H4688, a H8415 más szóhoz tartozik;
  - ALVIL-001, Jób 17:13, `A sírnak` (H7585): az eltéréslista szerint nem szóeltérés, hanem kulcshiba (verseltolás, Károli-kulcs: Jób 17:12); a #22 a régi arany `Job.17.13` hármasát kulcshibásként tartja (`f21p/regi_arany_hibas.tsv`).
- **Határ:** a régi sor csak döntéssel változik; a `Karoli_Strong_kivonat.tsv` generált nézet, nem ennek a feladatnak a tárgya (N-F65a).
- **Függés:** #65 (merge, PR #287).

A valódi briefet a `/befogad` csonk-kitöltése váltja fel, ugyanezen a számon és néven.
