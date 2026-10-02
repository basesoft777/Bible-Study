# DT3 lezárása (E17 küszöb)

**Döntés (felhasználó, chat, 2026.10.02):** a bontási napló küszöbe abszolút, |Δ sorszám| ≥ 10 táblánként, a main-hez képest. Az 1% és az 5% elvetve.
**Indok:** a táblák mérete 1 és kb. 469 ezer sor között van, ezért egyetlen százalékos küszöb a kis táblákon túl érzékeny, a nagyokon túl laza.
**Módosított fájlok:** `.claude/agents/fuggetlen-ellenor.md` (4. pont), `DONTESEK.md` (DT3 sora: Állapot, Döntés, Napló).

`grep -rn "E17" --include=*.md . | grep -v konkordancia/` — a megengedett négy fájlon kívüli találatok:
- brieffek: `F20_BEFOGADAS_BRIEF.md:192`, `F37_TANULMANY_ELLENORZES_BRIEF.md:130`, `F40_HIVATKOZAS_ELLENORZES_BRIEF.md:79` (csak a szám foglaltsága);
- ellenőri jelentések: `naplok/ELLENOR_{DT27,F16,F18,F21P,F21P_6,F22_1Moz,F24,F28}.md`; egyéb naplók: `naplok/F18_import_naplo.md:123`, `naplok/F20_B0_felmeres.md:10`, `naplok/orkesztrator-15_zaras.md` — múltbeli megállapítások, nem módosítva (felhasználói jóváhagyás: 2026.10.02).

Az F15 brief 103. és 124. sora (1%-os javaslat) lezárt brief történeti szövege; az érvényes küszöb a fuggetlen-ellenor.md 4. pontjában és a DT3-ban.

Gépi E17 (CI) nincs; ha kell, külön feladat a chat jóváhagyásával.
