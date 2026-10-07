# F23 zárás — M0 felmérés (#23 MOTIVUM_FORRAS)

*2026.10.07 · ág: `claude/f23-motivum-forras` · állapot: megállt az M0 ⛔-pontján. M1 várja: #12a.*

- Az öt M0-kimenet kész: `naplok/MOTIVUM_FORRAS_lekepezes.tsv` (67 sor, kézi besorolás), `_torzscikk_egyedi.tsv`, `_parositas.tsv`, `_naplo_keveredes.tsv`, `_atfedes.tsv`.
- A 2–5. pont számait a `python naplok/MOTIVUM_FORRAS_M0.py` adja (csak olvas; a módszer a docstringben). Minden sor `forras_parancs` oszlopot visel.
- Fő eredmény: csak-törzscikk állítás nincs; a ⭐-küszöb (`COUNT(DISTINCT fo_elofordulas)`) a KIRALY-001, MENNY-001 és HODIT-001 esetén 1, pedig van tematikus tanulmányuk.
- Összesítés és kérdések: `DONTESEK.md` DT-F23a (🟡).
- Tartalmi fájl nem változott: a diff csak `naplok/` új fájljai, a `DONTESEK.md` egy új sora és a brief fejléce.
- Eltérés az `ir`-mezőtől: a mérőszkript (`naplok/MOTIVUM_FORRAS_M0.py`) és ez a zárófájl nem szerepel benne; a TSV-k a brief oszlopain túl `forras_parancs` oszlopot kaptak (K1).
- Nincs ellenőrizve: a `fuggetlen-ellenor` nem futott.

## Folytatási pont

1. Döntés a DT-F23a-ról (a: javaslat-besorolások, b: ⭐-küszöb szabálya, c: M1 indítása).
2. A #12a próza-próba (DT-F32a) lefutása; az M1 ennek eredményét veszi bemenetként.
3. Utána `/kovetkezo`: M1/1–4 (forrássablon-tervezet, SEMA-alfejezet, CI-terv, pilot-terv).
