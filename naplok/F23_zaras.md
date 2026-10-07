# F23 zárás — M0 felmérés (#23 MOTIVUM_FORRAS)

*2026.10.07 · ág: `claude/f23-motivum-forras` · állapot: megállt az M0 ⛔-pontján; ELLENOR_F23 (F23.4–F23.7) és ELLENOR_F23_2 (F23.9–F23.13) javítva; a DT-F23a döntése átvezetve (F23.14–F23.16). M1 várja: #12a (#64).*

- Az öt M0-kimenet: `naplok/MOTIVUM_FORRAS_lekepezes.tsv` (77 sor; 30 „elfogadva”, 5 „kivétel” a DT-F23a szerint), `_torzscikk_egyedi.tsv`, `_parositas.tsv`, `_naplo_keveredes.tsv`, `_atfedes.tsv`; minden sor `forras_parancs` oszlopot visel.
- A számokat a `python naplok/MOTIVUM_FORRAS_M0.py` adja (csak olvas). Hatókör: `tematikus_lezart/*.md` + `tematikus_lezart/naplok/*.md` (+ `motivumok/*.md` az M0/4-ben).
- Leképezés: `generalt` 27, `kezi_forras` 21, `sablonszabaly` 15 (a DT-F23a (b) szerint bevezetett negyedik érték), `adat` 14; `szetvalasztando` 19.
- Fő eredmény: csak-törzscikk állítás a gépi előbesorolás szerint nincs; 87 NAPLO-blokk, mellettük 324 gyanús sor; ⭐-küszöb = 1 a KIRALY-001, MENNY-001, HODIT-001 esetén — nem mérési hiba; a DT-F23a (c): aktiválás = ⭐ küszöb VAGY lezárt tematikus forrás.
- `DONTESEK.md` DT-F23a: 🟢 (Felhasználó, 2026.10.07); az (a)–(b) átvezetve, a (c)–(d) az M1-ben alkalmazandó.
- Tartalmi fájl nem változott: a diff a `naplok/` fájljai, a `DONTESEK.md` egy sora és a brief fejléce.
- A döntés átvezetése után ellenőrzés nem futott.

## Folytatási pont

1. A #12a (#64) próza-próba (DT-F32a) lefutása; az M1 ennek eredményét veszi bemenetként (DT-F23a d).
2. Utána `/kovetkezo`: M1/1–4 (forrássablon-tervezet a `sablonszabaly` értékkel és a (c) aktiválási feltétellel, SEMA-alfejezet, CI-terv, pilot-terv); a „7. Nyitott kérdések” tételenkénti besorolása is az M1-ben.
3. A DT-F23a ✅-ra állítása az M1 átvezetése után.
