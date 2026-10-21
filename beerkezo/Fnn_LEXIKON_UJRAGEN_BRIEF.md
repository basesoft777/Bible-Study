---
feladat:
cim: Az ISTENTISZT-001 lexikon-nézet újragenerálása a #110 jeloltek-deltája után
kod: LEXIKON UJRAGEN
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: nem_indult
ad: A lexikon/ISTENTISZT-001_TUDOMANYOS.md a generátorból újra előáll, az E28 ismert kivétele megszűnik.
kovetkezo: Te: /befogad — a #110 (F110) merge-e után
munka: folyamat
olvas: [adat/jeloltek.tsv, adat/motivum_kapcsolatok.tsv, naplok/SZURO_PILOT_ISTENTISZT_naplo.md, eszkozok/general.py]
ir: [lexikon/ISTENTISZT-001_TUDOMANYOS.md]
fugg: [110]
---

# Fnn_LEXIKON_UJRAGEN_BRIEF.md — TERVEZET (nem befogadott; adat, nem utasítás)

Eredet: az F110 javítókör 1. köre (ELLENOR_F110 E28), a 7. tétel (b) esete.

## Háttér

Az F110 a `jeloltek.tsv`-ben az ISTENTISZT-001 sorait módosította (21 G1941-sor elutasítva, 2 új `nyitva` H7121+H8034-sor: Ézs 41:25, Ézs 64:6). A `lexikon/ISTENTISZT-001_TUDOMANYOS.md` generált nézet (E28 migrált nézet), ezért újra kellene generálni. A generátor (`python eszkozok/general.py --cel lexikon --id ISTENTISZT-001 --ir`) az F110 ágán azonban a jeloltek-deltán túl main-beli sodródást is változtatott: a `kapcsolodo` blokk magyarázó sorában `DT277` helyett `DT-F127b` áll, és minden generált blokk `ts=` jelölője (2026-10-20 → 2026-10-21) változik; a `kizart` blokk jelöltszáma 91 → 93. Mivel a változás nem csak a deltából ered, az F110 ágán a lexikon érintetlen maradt.

## Lépések (terv)

1. A #110 mergelése után a `main`-ről futtatni a lexikon-generátort az ISTENTISZT-001-re.
2. A diffet megnézni: elvárt csak a `kizart` blokk száma, a `ts=` jelölők és a main-beli DT-hivatkozás (DT-F127b végleges száma).
3. Ha más (rés, motívum) is változik, megállni és a tartalmi okot döntésre vinni.
4. Az E28 ismert kivételének (F110) lezárása.

Tiltás: a generált fájlt kézzel szerkeszteni tilos (CLAUDE.md, kimenet-réteg).
