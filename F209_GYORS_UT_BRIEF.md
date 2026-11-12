---
feladat: 209
cim: Gyors út a lexikonlap szövegszintű javítására (/lap-javit 7. pont, gyors szint, lapnézet --valtozas)
kod: GYORS_UT
tipus: feladat
fazis: folyamat
modell: sonnet
allapot: lezarva
ag: claude/lucid-meninsky-51e597
ad: a `/lap-javit` 7. pontja (gyors út), a `MUNKAMENET.md` `gyors` szint-sora, a `lapnezet.py --valtozas` kapcsoló teszttel
kovetkezo: "Te: a draft PR áttekintése; merge-et az orkesztrátor végzi; a HAMART-001 javítóköreiben az első gyors út"
munka: folyamat
olvas: [.claude/commands/lap-javit.md, MUNKAMENET.md, eszkozok/lektor_felulet/lapnezet.py, eszkozok/teszt_lektor_felulet.py]
ir: [.claude/commands/lap-javit.md, MUNKAMENET.md, eszkozok/lektor_felulet/lapnezet.py, eszkozok/teszt_lektor_felulet.py, nyitott/uj/lucid-meninsky-51e597.md]
fugg: []
nem_fugg: []
---

# F209_GYORS_UT_BRIEF.md — Gyors út a lap szövegszintű javítására

*FELADATOK #209 · Modell: claude-sonnet-5-5 · v1 · 2026.11.12*

Forrás: a jóváhagyott tervezet (`GYORS_UT_TERVEZET_2026-11-12.md`, a felhasználó „mehet”-je).

## Tételek
- **F209.1** `/lap-javit` 7. pont „Gyors út” (négy feltétel, menet, ami kimarad, biztosíték, `[GYORS]` előtag); az 1. pont K1-je mellett kimondott kivétel.
- **F209.2** `MUNKAMENET.md` „Menet-ellenőrzés”: `gyors` sor, hivatkozással a `/lap-javit`-ra.
- **F209.3** `lapnezet.py --valtozas <alap-commit>`: csak a változott blokkok, előtte–utána párban, kiemelve; önálló HTML, a `lapnezet_sablon.html`-hez nem nyúltunk (a #699 miatt); teszt: `teszt_lektor_felulet.py` `Valtozas`.
- **F209.4** `feladatok.py szint` nem módosult; nyitott tétel: N-F209a.

## Határ
Nem érintett: `lexikon_general.py`, `olvasoi_kapu.py`, `lexikon/*`, `motivumok/*`, `adat/*`, `nyilt_*`, `sablonok/*`, `CLAUDE.md`.
