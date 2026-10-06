# F38 BDB_FORDITAS — 6. adag zárása (claude/f38-adag6)

- **Elvégezve:** M0 5. pont gyökcsoport-mérés (F38.311); 6. adag, sorrend 407–648: 242 szócikk fordítva és rögzítve (`allapot=sonnet`, prompt v4.2, #56 adatblokk + fejezetszám-javítótábla), forrás 498 550 → fordítás 521 833 karakter.
- **Commitok:** F38.311 (mérés) és F38.312–F38.353 (fordítás, adagonként); a zárás: `F38.354`.
- **Kapuk/tesztek:** 242/242 RENDBEN a gátoló kapukon; `ellenoriz.py` SÉRTÉS 0; `teszt_forditas_kapuk` 69, `teszt_normalizal` 63, `teszt_emeles` 10, `teszt_ellenoriz_13` 9 OK.
- **Nyitott/hibás:** `teszt_bdb_zaras.py` 2 FAIL + 1 ERROR; a main-en (bdae91d) is bukik ugyanaz a 3 (H5674-ügy: `Zaras3Idempotencia.test_ir_ketszer_futtatva_nem_duplikal`, `DTF38g.test_dtf38g_kezi_javitasok`, `DTF38g.test_szellem_tabla_nagybetus_helyei`). Az ágon a `test_szellem_tabla_nagybetus_helyei` + H6743-at is jelzi — ezt e menet okozta (`SZELLEM_KOVETELT`). Nem javítottam.
- **13. kapu JELZES:** H3289 „Náh 7:5” (forráshiba, hűen átvéve).
- **Terminológia-kivételek (jóváhagyásra):** H4422, H6419, H5027 `see`; H0349 `emphatic`; H5324 `Sept.`; H0074 `accusative`.
- **Szellem-tábla:** +1 nagybetűs hely (H6743 Bír 14:6).
- **Döntésre vár:** `DONTESEK.md` DT-F38j (a) folytatás, (b) kivételek, (c) gyökcsoport hasznosítása, (d) Szellem-tábla/H5674-tesztek.
- **Gyökcsoport-mérés (újramérve):** 7 990 Strong; 5 702 (71,4%) kap `csak_bdb` többletet; TWOT-sal 5 486 közül 3 229 (58,9%); az ismétlődő Strong-sorok halmazként kezelve.
- **Eltérés rögzítve:** a commitok 4–9 szócikkesek (nem tétel-szintűek), az üzenetek `F38.<n>: 6. adag — …, Sonnet` alakúak; a történetet nem írtam át.
- **Folytatási pont:** a döntés után a 7. adag, sorrend 649– (kész összesen 648; hátra 7 416). Merge/ágtörlés nem történt; a független ellenőrzést az orkesztrátor futtatja, az eredményt nem minősítem „ellenőrzöttnek”.
