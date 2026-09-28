# ellenoriz.py -- SEMA §3 + Q-kapu gépi része (F8.5)

## Tábla-szabályok (`adat/SEMA.md` §3)

**1. Hivatkozási épség**: RENDBEN

**2. Nincs közvetlen út**: RENDBEN

**3. Proveniencia-kényszer**: RENDBEN

**4. Horgony-kényszer**: RENDBEN

**5. Károli-triplet**: RENDBEN

**6. Gate-kényszer (4.6)**: RENDBEN

**7. Ütközés-/részhalmaz-jelentés (gate.py)**: JELENTÉS -- 5 osztozó igehely, 4 átfedő motívumpár, 0 részhalmaz-gyanús pár (l. `python eszkozok/gate.py` a részletekért)

**8. Dataset-lefedettség (gépi)**: RENDBEN (mindig)

**8/b. Feltételes datasetek**: KÉZI (9) -- a feltétel teljesülése ítélet, l. F8_BRIEF.md F8.5a
  - KJV_ASV_Strongs (KJV_Strongs_*.tsv, ASV_Strongs_*.tsv)
  - LSJ (LSJ_teljes.tsv)
  - LXX_kivonat (LXX_kivonat_*.tsv)
  - SECE_G (SECE_G_teljes.tsv)
  - SECE_H (SECE_H_teljes.tsv)
  - Strong_szotar (Strong_szotar.tsv)
  - TAGNT (TAGNT_kivonat.tsv)
  - TIPNR (TIPNR_kivonat.tsv)
  - Thayer (Thayer_teljes.tsv)

**8/c. Kézi dataset-lefedettség**: KÉZI (9)
  - ALVIL-001 -- fedetlen: BDB (nincs lekérdező), Karoli_1908 (retroaktív, F3), Karoli_KH (retroaktív, F3), TAHOT (retroaktív, F3), TSK (retroaktív, F3) | ember ellenőrizze: `tematikus_lezart/Hadesz_Seol_tematikus.md` + `tematikus_lezart/naplok/Hadesz_Seol_kereszthivatkozas_naplo.md`
  - ANTROP-001 -- fedetlen: BDB (nincs lekérdező), Karoli_1908 (retroaktív, F3), Karoli_KH (retroaktív, F3), TAHOT (retroaktív, F3), TSK (retroaktív, F3) | napló nincs (csak generált próba: `generalt_proba/tematikus_lezart/naplok/ANTROP-001_kereszthivatkozas_naplo_GENERALT.md`, nem a study eredeti keresése)
  - HAMART-001 -- fedetlen: BDB (nincs lekérdező), Karoli_1908 (retroaktív, F3), Karoli_KH (retroaktív, F3), TAHOT (retroaktív, F3), TSK (retroaktív, F3) | ember ellenőrizze: `tematikus_lezart/Bun_kovetkezmenyeinek_gyuruzese_tematikus.md` + `tematikus_lezart/naplok/Bun_kovetkezmenyeinek_gyuruzese_kereszthivatkozas_naplo.md`
  - HODIT-001 -- fedetlen: BDB (nincs lekérdező), Karoli_1908 (retroaktív, F3), Karoli_KH (retroaktív, F3), TAHOT (retroaktív, F3), TSK (retroaktív, F3) | ember ellenőrizze: `tematikus_lezart/Rafaim_tematikus.md` + `tematikus_lezart/naplok/Rafaim_kereszthivatkozas_naplo.md`
  - ISTENTISZT-001 -- fedetlen: BDB (nincs lekérdező), Karoli_1908 (retroaktív, F3), Karoli_KH (retroaktív, F3), TAHOT (retroaktív, F3), TSK (retroaktív, F3) | ember ellenőrizze: `tematikus_lezart/Segitsegul_hivni_az_Urat_tematikus.md` + `tematikus_lezart/naplok/Segitsegul_hivni_az_Urat_kereszthivatkozas_naplo.md`
  - KIRALY-001 -- fedetlen: BDB (nincs lekérdező), Karoli_1908 (retroaktív, F3), Karoli_KH (retroaktív, F3), TAHOT (retroaktív, F3), TSK (retroaktív, F3) | ember ellenőrizze: `tematikus_lezart/Melkizedek_tematikus.md` + `tematikus_lezart/naplok/Melkizedek_tematikus_kereszthivatkozas_naplo.md`
  - MENNY-001 -- fedetlen: BDB (nincs lekérdező), Karoli_1908 (retroaktív, F3), Karoli_KH (retroaktív, F3), TAHOT (retroaktív, F3), TSK (retroaktív, F3) | ember ellenőrizze: `tematikus_lezart/Isten_fiai_Nefilim_Gibborim_tematikus.md` + `tematikus_lezart/naplok/Isten_fiai_Nefilim_Gibborim_kereszthivatkozas_naplo.md`
  - TEREMT-001 -- fedetlen: BDB (nincs lekérdező), Karoli_1908 (retroaktív, F3), Karoli_KH (retroaktív, F3), TAHOT (retroaktív, F3), TSK (retroaktív, F3) | ember ellenőrizze: `tematikus_lezart/Tehom_tematikus.md` + `tematikus_lezart/naplok/Tehom_kereszthivatkozas_naplo.md`
  - TEREMT-002 -- fedetlen: BDB (nincs lekérdező) | ember ellenőrizze: (nincs tematikus_lezart forrás_study) | napló nincs

**9. 'teljes'/'részlet' jelentes_szam korlatok (SEMA 2.2.2)**: RENDBEN

**10. LEXV2_2 tablak (forditas_ubs -- RETIRED S1.1, lxx_dontesek)**: RENDBEN -- forditas_ubs.tsv rész RETIRED (a tábla megszűnt, SZOTAR S1.1, l. adat/SEMA.md 2.10) -- a kulcs-/hash-ellenőrzés a 13. szabályban fut

**11. Rés-forrás egyezés (tanulmány/adat ≡ tábla + tanulmány)**: RENDBEN

**12. `lap` forrású rés-sorok száma**: JELENTÉS (0) -- a RENDER_BRIEF.md 2. menetének végére 0-ra csökken (G12)

**13. Fordítási gyorsítótár (kulcs egyediség, forras_hash)**: RENDBEN

**14. Kiejtés és terminológia (JELENTÉS)**: JELENTÉS -- terminológia-verzió elmaradás: 51/51 sor (jelenlegi verzió: v1); héber kiejtés-kivétel sorok: 2 (a D28 26-os hatóköre az S1.7/ÁLLJ jóváhagyása után kerül be, S2.1)

## Összesítő

RENDBEN: 11 | SÉRTÉS: 0 | KÉZI: 2 | JELENTÉS: 3
