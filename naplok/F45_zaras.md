# F45 — zárójelentés (Modell-ellenőrzés minden brief futtatásának elején)

*Ág: `claude/f45-modell-ellenorzes` · 2026.10.12 · végrehajtó: sonnet (`claude-sonnet-5-5`) · napló: `naplok/MODELL_ELLENORZES_naplo.md` · ellenőrzés: `naplok/ELLENOR_MODELL_ELLENORZES.md`*

- **Kész:** a modell-ellenőrzés szabálya az öt helyen (`CLAUDE.md` új szakasz, `BRIEF_SABLON.md`, `.claude/commands/kovetkezo.md` 6/6b, `vegrehajto-{opus,sonnet,haiku}.md`, `fuggetlen-ellenor.md`). `feladatok.py ellenoriz`: 0 hiba.
- **Egyeztetett eltérés:** a `kovetkezo.md` „Csatolt brief” sora is egy mondattal bővült (az orkesztrátor kérésére); az ellenőr szerint ez túlmegy a brief 4. lépésén és félreolvasható (ELTÉRÉS 4).
- **Ellenőr: ELTÉRÉS, 6 tétel.** Az 1. súlyos: a `CLAUDE.md:77` szövege ellentmond a `fuggetlen-ellenor.md`-nek és a `kovetkezo.md`-nek (az ellenőr és az orkesztrátor a brief `modell` mezőjéhez mérné magát, a gyakorlatban a saját frontmatterjéhez). A 3–6. enyhe (jelzésminta, „Csatolt brief” sor, 4./5. lépés be nem kötve, `fut`-commit a ellenőrzés előtt).
- **Javítva (F45.4, felhasználói jóváhagyással):** az 1. és a 3. eltérés: a `CLAUDE.md` szakasza szerepenként adja meg a kért modellt (végrehajtó: a brief `modell` mezője; független ellenőr: a saját subagent-fájlja `model` mezője; orkesztrátor: a végrehajtóra hárul), és az öt helyen egységes a jelzésminta („A kért modell `<kért>`, a session `<tényleges név>`…”). A 4–6. eltérés is javítva (F45.5, `kovetkezo.md`): a „Csatolt brief” sor bővítése visszavonva; a subagent nélküli eset az 5. lépés javaslatába kötve; az `allapot: fut` commit a végrehajtó modell-ellenőrzése után történik.
- **PR:** a címe `[ELLENŐRZŐ]` előtagú (E16: a PR az ellenőr fájlját érinti).
- **Nyitott:** ellenőrző kör a javítás (F45.4–F45.5) után; merge a felhasználótól.
