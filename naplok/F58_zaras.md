# F58_MORF_KULCS zárása (#58) — 2026-10-05

**Kész:** M0 (`naplok/MORF_KULCS_M0.md`), M1 (jelkulcs-import), M2 (feloldó, teszt, lefedettség). Az M3 hátralévő része (független ellenőr, draft PR) az orkesztrátoré. Commitok: `git log claude/morf-kulcs` (F58.0–F58.3).
**Döntés:** DT35 🟢 (felhasználó, 2026-10-05): forrás OSHB `HebrewMorphologyCodes.html` (morphhb@3d15126f, CC BY 4.0), `nyelv` oszlop, nyelv-kivonat a Macula-XML-ből; `ir` bővítése tételként rögzítve (DONTESEK + brief `ir_bovites`).
**Tábla:** `adat/morf_kulcs_heber.tsv` 124 sor (szófaj 9, szerkezet 9, igetörzs H 27 / A 26, igetípus 11, típusok 26, személy 3, nem 4, szám 3, állapot 3, nyelv_jel 2, helykitöltő 1); minden sor forrásmegnevezésen áll, a magyar oszlop a megnevezés fordítása. `adat/morf_nyelv_aramai.tsv`: 7 549 arámi morféma (930 lowfat fájl, 475 911 szó; morf-eltérés 0).
**Licenc:** `adat/kulso/morf_kulcs_LICENC.txt` (szó szerint), `adat/licencek.tsv` +2 sor (`morf_kulcs_heber`, `morf_nyelv_aramai`; tisztazott, CC BY 4.0), `adat/datasetek.tsv` +4 sor, SEMA 2.22.
**Lefedettség (`naplok/MORF_KULCS_lefedettseg.md`):** 747 kód, 892 (kód, nyelv) pár a szó tényleges nyelvével: 874 teljes (473 228 szó), 18 `x`-helykitöltős (2 683 szó, külön állapot), részleges 0, ismeretlen 0.
**A 18 nem illeszkedő (M0) kód:** 17 arámi törzsjeles + `Nxxxa`; arámiként 17 teljes, a `Nxxxa` `helykitoltovel` (héber olvasatban is); a 17 arámi törzsjeles héber olvasatban részleges. A lefedettség-napló 3. táblája explicit listázza őket.
**Nyelv nélkül:** 377 kód / 68 668 szó kétértelmű (törzsjel mindkét nyelvben), ebből 1 014 szó tényleg arámi: nyelv nélkül csendes téves héber olvasat lenne; a feloldó ezt jelzi (`[nyelv ismeretlen]`, `[csak arámi olvasat]`).
**Teszt:** `python eszkozok/teszt_morf_feloldas.py` zöld (13 héber kód, arámi/nyelv nélküli esetek, x-helykitöltő, ismeretlen jel, adat-szintű lefedettség). CI/ellenőr nem futott.
**Nyitott:** a `common (verb)` nem-megnevezés névmásnál zavaró (`Pdxcp`), a magyar oszlop szó szerint tükrözi (SEMA 2.22/4.); a #59 szószedet dolga a magyarázat. Új ⛔ nincs.
