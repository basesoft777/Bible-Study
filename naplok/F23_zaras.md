# F23 zárás — M1 terv (#23 MOTIVUM_FORRAS)

*2026.10.08 · ág: `claude/f23-m1-forrassablon` · állapot: döntésre vár (DT-F23a 🟡, 13 `javaslat`-pont); az ELLENOR_F23_M1 2–4. tétele javítva (F23.M1.7–F23.M1.10).*

- A négy M1-kimenet: `sablonok/9_PaRDeS_motivum_forras_sablon.md` (tervezet v0, 23 szakasz), `adat/SEMA.md` 3.10 (szintjelölés és kinyerés), `naplok/MOTIVUM_FORRAS_ci_terv.md` (E28, E29; csak leírás), `naplok/MOTIVUM_FORRAS_pilot_terv.md` (a #12 és a #11 1. lépcsőjének bemenetei; ez a #11 briefjének közvetlen bemenete).
- A javaslat-pontok egy tételben: `DONTESEK.md` DT-F23a. A K3 a jóváhagyásig nem teljesül (várt állapot).
- ELLENOR_F23_M1: JAVÍTANDÓ, 5 tétel. A 2. tétel (a döntés nélküli `auditok.tsv`-út ütközik a SEMA 3/9-cel) normatív szövegből `javaslat` lett, DT-F23a (2). A 3–4. tétel javítva, az 5. (K4) itt. Az 1. tétel lent.
- **⛔ Ágszennyezés (nem javítva, a felhasználóé):** egy másik session menet közben ágat váltott a közös munkakönyvtárban, ezért az F23.M1.4–M1.5 (`4d6b469`, `fe9a870`) a pusholt `claude/f83-job-versbeosztas` ágra, az M1.1–M1.3 (`fecb6bb`, `a0040d0`, `f2b01f0`) a helyi `claude/befogadas-20261008-4` ágra is került. Az F83 PR merge-e előtt ki kell venni őket. A tartalom ezen az ágon cherry-pickkel teljes.
- Tartalmi fájl nem változott. K4, `git diff --stat adc8862..a8544ba`: `DONTESEK.md` +1; `F23_MOTIVUM_FORRAS_BRIEF.md` 12 ±; `adat/SEMA.md` +129; `naplok/ELLENOR_F23_M1.md` +37; `naplok/MOTIVUM_FORRAS_ci_terv.md` +122; `naplok/MOTIVUM_FORRAS_pilot_terv.md` +279; `sablonok/9_PaRDeS_motivum_forras_sablon.md` +204 (7 fájl, 779+, 5−).

## Folytatási pont (M1)

1. A DT-F23a döntése (Felhasználó); utána átvezetés ezen a briefen, és a DT66 ✅-ra állítása.
2. A #11 briefjének megírása a `naplok/MOTIVUM_FORRAS_pilot_terv.md` alapján.

---

# F23 zárás — M0 felmérés (#23 MOTIVUM_FORRAS)

*2026.10.07 · ág: `claude/f23-motivum-forras` · állapot: megállt az M0 ⛔-pontján; ELLENOR_F23 (F23.4–F23.7) és ELLENOR_F23_2 (F23.9–F23.13) javítva; a DT66 döntése átvezetve (F23.14–F23.16). M1 várja: #12a (#64).*

- Az öt M0-kimenet: `naplok/MOTIVUM_FORRAS_lekepezes.tsv` (77 sor; 30 „elfogadva”, 5 „kivétel” a DT66 szerint), `_torzscikk_egyedi.tsv`, `_parositas.tsv`, `_naplo_keveredes.tsv`, `_atfedes.tsv`; minden sor `forras_parancs` oszlopot visel.
- A számokat a `python naplok/MOTIVUM_FORRAS_M0.py` adja (csak olvas). Hatókör: `tematikus_lezart/*.md` + `tematikus_lezart/naplok/*.md` (+ `motivumok/*.md` az M0/4-ben).
- Leképezés: `generalt` 27, `kezi_forras` 21, `sablonszabaly` 15 (a DT66 (b) szerint bevezetett negyedik érték), `adat` 14; `szetvalasztando` 19.
- Fő eredmény: csak-törzscikk állítás a gépi előbesorolás szerint nincs; 87 NAPLO-blokk, mellettük 324 gyanús sor; ⭐-küszöb = 1 a KIRALY-001, MENNY-001, HODIT-001 esetén — nem mérési hiba; a DT66 (c): aktiválás = ⭐ küszöb VAGY lezárt tematikus forrás.
- `DONTESEK.md` DT66: 🟢 (Felhasználó, 2026.10.07); az (a)–(b) átvezetve, a (c)–(d) az M1-ben alkalmazandó.
- Tartalmi fájl nem változott: a diff a `naplok/` fájljai, a `DONTESEK.md` egy sora és a brief fejléce.
- A döntés átvezetése után ellenőrzés nem futott.

## Folytatási pont

1. A #12a (#64) próza-próba (DT-F32a) lefutása; az M1 ennek eredményét veszi bemenetként (DT66 d).
2. Utána `/kovetkezo`: M1/1–4 (forrássablon-tervezet a `sablonszabaly` értékkel és a (c) aktiválási feltétellel, SEMA-alfejezet, CI-terv, pilot-terv); a „7. Nyitott kérdések” tételenkénti besorolása is az M1-ben.
3. A DT66 ✅-ra állítása az M1 átvezetése után.
