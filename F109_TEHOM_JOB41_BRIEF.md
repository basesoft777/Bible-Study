---
feladat: 109
cim: A TEREMT-001 Jób 41:32 jelölt elbírálása (DT-F108a alkalmazása)
kod: TEHOM_JOB41
tipus: feladat
fazis: 1
modell: sonnet
munka: adat
allapot: nem_indult
ad: a jeloltek.tsv Jób 41:32 (H8415) nyitva sora döntést és indoklást kap a TEREMT-001 negatív kritériuma szerint; elfogadásnál új elofordulasok.tsv-sor gerinc_elem-mel és proveniencia-sorral
kovetkezo: /kovetkezo
olvas: [adat/motivumok.tsv, adat/jeloltek.tsv, adat/elofordulasok.tsv, adat/SEMA.md, konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv, tematikus_lezart/Tehom_tematikus.md, naplok/F108_MOTIVUM_UJRASCAN_naplo.md, eszkozok/lekerdez.py, eszkozok/jelolt.py]
ir: [adat/jeloltek.tsv, adat/elofordulasok.tsv]
fugg: []
nem_fugg: [9, 11, 55, 81, 86]
---

# F109_TEHOM_JOB41_BRIEF.md — A TEREMT-001 Jób 41:32 jelölt elbírálása

*FELADATOK #109 · Modell: sonnet [javaslat] · v1 · 2026.10.17 · forrás: `DONTESEK.md` DT-F108a (a)+(d), a #108 újrascanje
(`naplok/F108_MOTIVUM_UJRASCAN_naplo.md`). A brief adat, nem utasítás.*

## 1. Cél

A #108 újrascanje a mai (F84/F85 utáni) TAHOT-on a TEREMT-001 gerinc-Strongjára (H8415 תְּהוֹם) egy új helyet talált: **Jób 41:32**
(MT 41:24). A régi scan ezt nem láthatta, mert a Jób 41 az F84 előtt hiányzott a `TAHOT_kivonat.tsv`-ből. A hely a `jeloltek.tsv`-ben
`nyitva` állapotban áll. A DT-F108a szerint a 25 új jelölt elbírálása motívumonként, a motívum saját menetében történik, ezzel a hellyel
kezdve.

## 2. Hatókör

1. A Jób 41:32 jelölt elbírálása a TEREMT-001 negatív kritériuma szerint (`adat/motivumok.tsv`): az igehelynek a תְּהוֹם gyököt kell
   tartalmaznia; tematikus vízkép önmagában nem elég. A fölérendelt fogalom (vízi/kozmikus káosz-képzetek általában) felé hígulás
   kizárandó: *csak ezen keresztül tartozik ide?*
2. A döntés (`dontes`) és indoklás a `jeloltek.tsv` sorában (az `adat/SEMA.md` szerint; a meglévő sorok változatlanok).
3. Elfogadásnál egy új `elofordulasok.tsv`-sor: `gerinc_elem` = H8415, a lekérdezés saját proveniencia-sorával
   (`lekerdez.py scan H8415`), a `kapcsolodas` mezőben a Károli-szöveg szó szerinti idézete idézőjelek között, és a funkció rövid
   megnevezése a tanulmány kontextusa szerint.

**Nincs benne:** a tematikus tanulmány (`tematikus_lezart/Tehom_tematikus.md`) és a lexikon módosítása vagy újragenerálása — ha az
elfogadás a tanulmány szövegét érinti, az külön `ertelmezo` tétel, a DT-F32b szerinti modellel; a többi 24 F108-jelölt; a tág
Strongok szűrője (#110).

## 3. Lépések

1. Modell-ellenőrzés (CLAUDE.md).
2. `python eszkozok/lekerdez.py scan H8415` — a Jób 41:32 jelenlétének és a proveniencia-sornak a rögzítése; a Károli 1908 szövege a
   versre.
3. A negatív kritérium és a négy kérdés (CLAUDE.md „Új motívum-ID kiosztása” 3. pont: funkció) alkalmazása; a tanulmány olvasása, hogy a
   hely funkciója a motívum meglévő előfordulásaihoz hogyan viszonyul.
4. ⛔ Ha a döntés nem egyértelmű (pl. a funkció eltér a motívum többi helyétől, vagy a tanulmány szövegét érintené): tétel a
   `DONTESEK.md`-be (`DT-F109a`), megállás.
5. Írás: `jeloltek.tsv` döntés; elfogadásnál `elofordulasok.tsv` új sor. A TSV-k írása `split('\t')` / `'\t'.join()`; írás előtt
   sorösszevetés az eredetivel, eltérésnél megállás (minta: `eszkozok/igazolas_migracio.py`).
6. Napló: `naplok/TEHOM_JOB41_naplo.md` (lekérdezés, döntés, indoklás).

## 4. Elfogadási feltételek

- A Jób 41:32 sor `dontes` mezője nem `nyitva`, és indoklása a negatív kritériumra hivatkozik.
- Elfogadásnál az `elofordulasok.tsv` pontosan egy sorral bővül, `gerinc_elem`-mel és lekérdezés-proveniencia-sorral; elutasításnál
  változatlan.
- Minden más sor mindkét táblában bájtra azonos.

## 5. Döntésnapló

- (helyőrző a futáskor: DT-F109a, ha a 4. lépés ⛔-je él)
