# ELLENŐR — F45_MODELL_ELLENORZES_BRIEF.md · origin/main..01c6f125

*Független ellenőr (`fuggetlen-ellenor`, tényleges modellje a saját közlése szerint `claude-opus-5-5`). Az ellenőr eszközkészletében nincs Write, ezért a jelentés szövegét az orkesztrátor írta fájlba, tartalmi változtatás nélkül, rövidítve (a nem érintett OK-sorok összevonva).*

**Eredmény: ELTÉRÉS, 6 tétel.** A CI-hez a PR címe `[ELLENŐRZŐ]` előtagot kap (E16).

## Eltérések, súlyossági sorrendben

1. **(súlyos) Ellentmondás a szabály szövegei között.** `CLAUDE.md:77` szerint a `/kovetkezo`, a végrehajtó subagent és a független ellenőr egyaránt a *brief* `modell` mezőjével veti össze a saját modelljét. A `fuggetlen-ellenor.md:29` viszont a saját frontmatterével (`opus`) vet össze, a `kovetkezo.md` orkesztrátora pedig a subagentre bízza az ellenőrzést. Szó szerint alkalmazva a CLAUDE.md szövege minden opus/haiku briefnél megállítaná a sonnet orkesztrátort, és minden nem-opus briefnél az ellenőrt. A forrás a brief 1. céljának szó szerinti szövege; a `fuggetlen-ellenor.md` tartalmilag helyes.
2. **(közepes) E16 CI-hiba:** a PR érinti az ellenőrt (`.claude/agents/fuggetlen-ellenor.md`), ezért a PR címe `[ELLENŐRZŐ]` előtagú legyen. E2–E15, E19, E20, E26: 0 hiba.
3. **(enyhe) A jelzésminta nem egységes:** `CLAUDE.md:77` és `fuggetlen-ellenor.md:29` beégetett `opus`-t ír, a `vegrehajto-*.md:11` `<kért>`-et; az ellenőrnél „a brief `opus`-t kér” áll, holott ott a frontmatter a kért modell.
4. **(enyhe) `kovetkezo.md:11`, „Csatolt brief” sor:** túlmegy a brief 4. lépésén (az csak a 6. és 6b. lépést nevezi meg), és félreolvasható helyen áll, mintha a csatolt briefet modell-ellenőrzéssel futtatni lehetne.
5. **(enyhe, a briefből örökölt) `kovetkezo.md:62`:** a subagent nélküli esetben a 6. lépés az „5. lépésbeli egyeztetésen” jelzést írja elő, de a 4./5. lépés nem lett bővítve (időrendi fordítottság).
6. **(enyhe) `kovetkezo.md:58–62`:** az `allapot: fut` commit megelőzi a modell-ellenőrzést; eltérésnél `fut` állapotú ág marad hátra.

## Rendben (összevonva)

- A szabály mind az öt helyen benne van (CLAUDE.md, BRIEF_SABLON.md, kovetkezo.md 6/6b, `vegrehajto-*.md`, `fuggetlen-ellenor.md`); a CLAUDE.md-szakasz a „Három szabály” után áll; a sablon két mondata betűre egyezik a brief 3. lépésével.
- Meglévő címsor szövege nem változott (7 törölt sor, mind módosítás, 0 kiszűrt adatsor).
- Nulla adat-diff: az `adat/` és `konkordancia/` nem változott, TSV-sorszám Δ = 0 (E17 nem alkalmazható), A1–A6 nem alkalmazható, a briefben nincs ⛔.
- A napló első bejegyzése a modell-ellenőrzés (formailag OK; tartalma lekérdezéssel nem igazolható, a végrehajtó modellje a commit-trailerből és a napló közléséből `claude-sonnet-5-5`).

## Nem ellenőrizhető az ellenőr körében

`python eszkozok/feladatok.py ellenoriz` (az orkesztrátor futtatta: l. zárójelentés), a PR és a CI-jelentés (a PR a zárással jön létre).
