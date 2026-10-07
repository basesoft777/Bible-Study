# F23 zárás — M0 felmérés (#23 MOTIVUM_FORRAS)

*2026.10.07 · ág: `claude/f23-motivum-forras` · állapot: megállt az M0 ⛔-pontján; az ELLENOR_F23 8 eltérése javítva (F23.4–F23.7). M1 várja: #12a.*

- Az öt M0-kimenet: `naplok/MOTIVUM_FORRAS_lekepezes.tsv` (77 sor, kézi besorolás, 33 `javaslat`), `_torzscikk_egyedi.tsv`, `_parositas.tsv`, `_naplo_keveredes.tsv`, `_atfedes.tsv`; minden sor `forras_parancs` oszlopot visel.
- A 2–5. pont számait a `python naplok/MOTIVUM_FORRAS_M0.py` adja (csak olvas). Hatókör: `tematikus_lezart/*.md` + `tematikus_lezart/naplok/*.md` (+ `motivumok/*.md` az M0/4-ben).
- A leképezés javaslatként negyedik B_helye-értéket vezet be: `sablonszabaly` (13 sor; szabályblokk, nem dokumentumszakasz).
- Fő eredmény: csak-törzscikk állítás a gépi előbesorolás szerint nincs; 324 gyanús sor a NAPLO-blokkokon kívül; ⭐-küszöb (`COUNT(DISTINCT fo_elofordulas)`) = 1 a KIRALY-001, MENNY-001, HODIT-001 esetén.
- Összesítés, a javaslat-besorolások listája és a kérdések: `DONTESEK.md` DT-F23a (🟡).
- Tartalmi fájl nem változott: a diff a `naplok/` fájljai, a `DONTESEK.md` egy sora és a brief fejléce (`ir` kiegészítve a szkripttel és ezzel a fájllal).
- A javítások után a `fuggetlen-ellenor` nem futott újra.

## Folytatási pont

1. Döntés a DT-F23a-ról (a: javaslatok, b: `sablonszabaly`, c: ⭐-küszöb, d: M1 indítása).
2. A #12a próza-próba (DT-F32a) lefutása; az M1 ennek eredményét veszi bemenetként.
3. Utána `/kovetkezo`: M1/1–4 (forrássablon-tervezet, SEMA-alfejezet, CI-terv, pilot-terv).
