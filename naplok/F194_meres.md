# F194 — az ISTENTISZT-001 új cikkének lépésenkénti mérése

*#194 ISTENTISZT_UJ_CIKK · a felhasználó: „a mérést ne felejtsük el” · cél: a többi lap arányosított becslése (lépés × egység)*

**Mértékegységek.** A keret: `get_usage` (`plan.windows`), „5 órás” és „heti, minden modell” %. A lap mérete: 22 előfordulás (ÓSZ 15, ÚSZ 7), 138 jelöltsor, 3 gerinc-Strong (H7121, H8034, G1941). Az idő UTC. Futás = eszköz- vagy szkriptfuttatás; ellenőrzés = az eredmény összevetése (kapu, teszt, kézi szúrópróba).

| # | Lépés | Modell · effort | Kezdés | Vége | Keret előtte (5 ó / heti) | Keret utána (5 ó / heti) | Futás | Ellenőrzés | Egység | Megjegyzés |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Kontextus: követelménylista, határnapló, adatállapot, brief | claude-opus-5-5 · alap (nem lekérdezhető) | ~12:13 (becslés) | 12:25 | — / — | 10% / 93% | 8 | 0 | — | a session kontextusa a lépés végén 178 k token (18%) |
| 1 (félbeszakadt) | Határ K6–K8; mellékmérés: a 138 jelölt indoklása (K47/K48) és az előfordulás-munkalap | claude-opus-5-5 · alap | 12:25 | 12:29 | 10% / 93% | 15% / 94% | 9 | 2 (K7: TAHOT a 12 versen; indoklás-mérés a HAMART-tal összevetve) | 3 határkérdés; 138 jelöltsor; 22 igehely | a K7 eldöntve, a K6/K8 a felhasználónál; a kontextus 289 k token (29%). Szünet a felhasználó döntésére (a HAMART `/kiadas`-áig) |

**Szünet, 2026-11-11 12:29 UTC.** A felhasználó döntése: az ISTENTISZT a HAMART kiadásáig áll. Az eddigi mérés érvényes, a folytatás innen indul.

**Mellékmérés (1. lépés):** `python naplok/F194_indoklas_meres.py` — 138 ISTENTISZT-jelöltsorból 94 indoklása sérti az olvasói kapu indoklás-szabályait: 73 írás kiejtés nélkül, 28 munkaszó, 15 belső tipológia-címke („D-minta”, „C-minta”), 12 hivatkozás „tanulmány”-ra vagy „napló”-ra, 2 névelő. A Strong-szám (119) nem hiba: a HAMART mai adatán is áll (89). Összevetésül a HAMART-001: 335 sorból csak Strong-szám (89) és 3 munkaszó („felhasználó”). A javítandó egység ezért kb. 95 indoklás. Ezen felül a „korábban (…)”-előzményrészek kivezetése (K06) és a „felhasználó döntése” → „szerkesztői döntés” csere (K04).
