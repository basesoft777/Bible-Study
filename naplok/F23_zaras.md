# F23 zárás — M0 felmérés (#23 MOTIVUM_FORRAS)

*2026.10.07 · ág: `claude/f23-motivum-forras` · állapot: megállt az M0 ⛔-pontján; az ELLENOR_F23 (F23.4–F23.7) és az ELLENOR_F23_2 (F23.9–F23.13) eltérései javítva. M1 várja: #12a.*

- Az öt M0-kimenet: `naplok/MOTIVUM_FORRAS_lekepezes.tsv` (77 sor, kézi besorolás, 35 `javaslat`), `_torzscikk_egyedi.tsv`, `_parositas.tsv`, `_naplo_keveredes.tsv`, `_atfedes.tsv`; minden sor `forras_parancs` oszlopot visel.
- A számokat a `python naplok/MOTIVUM_FORRAS_M0.py` adja (csak olvas). Hatókör: `tematikus_lezart/*.md` + `tematikus_lezart/naplok/*.md` (+ `motivumok/*.md` az M0/4-ben).
- Leképezés: `generalt` 26, `kezi_forras` 21, `sablonszabaly` 16 (javasolt negyedik érték, egységes szabállyal: szabály, eljárás, kimenet-szerkezet vagy tartalom nélküli megszűnt kimenet), `adat` 14.
- Fő eredmény: csak-törzscikk állítás a gépi előbesorolás szerint nincs; 87 NAPLO-blokk, mellettük 324 gyanús sor; ⭐-küszöb = 1 a KIRALY-001, MENNY-001, HODIT-001 esetén — nem mérési hiba (a mező a napló tanulmány előtti kiváltó-számát őrzi), a D37 alkalmazási köre a kérdés.
- Összesítés, a javaslat-besorolások listája és a kérdések: `DONTESEK.md` DT-F23a (🟡).
- Tartalmi fájl nem változott: a diff a `naplok/` fájljai, a `DONTESEK.md` egy sora és a brief fejléce (v1.5: `ir` a szkripttel, ezzel a fájllal és a két ellenőri jelentéssel).
- A második javítókör után teljes ellenőrzés nem futott (az orkesztrátor szerint nem kell).

## Folytatási pont

1. Döntés a DT-F23a-ról (a: javaslatok, b: `sablonszabaly`, c: ⭐-küszöb, d: M1 indítása).
2. A #12a próza-próba (DT-F32a) lefutása; az M1 ennek eredményét veszi bemenetként.
3. Utána `/kovetkezo`: M1/1–4 (forrássablon-tervezet, SEMA-alfejezet, CI-terv, pilot-terv).
