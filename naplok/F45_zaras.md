# F45 — zárójelentés (Modell-ellenőrzés minden brief futtatásának elején)

*Ág: `claude/f45-modell-ellenorzes` · 2026.10.12 · végrehajtó: sonnet (`claude-sonnet-5-5`) · napló: `naplok/MODELL_ELLENORZES_naplo.md` · ellenőrzés: `naplok/ELLENOR_MODELL_ELLENORZES.md`*

- **Kész:** a modell-ellenőrzés szabálya az öt helyen (`CLAUDE.md` új szakasz, `BRIEF_SABLON.md`, `.claude/commands/kovetkezo.md` 6/6b, `vegrehajto-{opus,sonnet,haiku}.md`, `fuggetlen-ellenor.md`). `feladatok.py ellenoriz`: 0 hiba.
- **Egyeztetett eltérés:** a `kovetkezo.md` „Csatolt brief” sora is egy mondattal bővült (az orkesztrátor kérésére); az ellenőr szerint ez túlmegy a brief 4. lépésén és félreolvasható (ELTÉRÉS 4).
- **Ellenőr: ELTÉRÉS, 6 tétel.** Az 1. súlyos: a `CLAUDE.md:77` szövege ellentmond a `fuggetlen-ellenor.md`-nek és a `kovetkezo.md`-nek (az ellenőr és az orkesztrátor a brief `modell` mezőjéhez mérné magát, a gyakorlatban a saját frontmatterjéhez). A 3–6. enyhe (jelzésminta, „Csatolt brief” sor, 4./5. lépés be nem kötve, `fut`-commit a ellenőrzés előtt).
- **Nem javítva:** a javítás a szabály szövegét módosítja (tartalmi döntés), ezért a PR draft marad, javítás a felhasználó döntése után új commitban.
- **PR:** a címe `[ELLENŐRZŐ]` előtagú (E16: a PR az ellenőr fájlját érinti).
- **Nyitott:** az 1. eltérés feloldása (melyik szöveg az irányadó); merge a felhasználótól.
