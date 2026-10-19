# ELLENOR_F112 — F112_COMMIT_EKEZET_BRIEF.md · `1a6a6eef..06e130e1`

*Független ellenőr (`fuggetlen-ellenor`, `claude-opus-5-5`, a kért `opus`). A jelentést a végrehajtó mentette el, mert az ellenőrnek nincs fájlíró eszköze; a tartalom az ellenőr jelentése, a „Kezelés” oszlop a végrehajtóé.*

**Eredmény: ELTÉRÉS (7 tétel), mind mechanikus vagy dokumentációs; a javítás az F112.5 commitban.** Az ellenőr a tesztet és az `e30_meres`-t D6 miatt nem futtatta; a végrehajtó futtatta (l. a végén).

| pont | eredmény | indok |
|---|---|---|
| G1 kizárások | OK | próba: kétértelmű szó, kódrész, fájlút, `forras=`, azonosító nem jelöl; egyetlen találat `mezo -> mező` valódi hiba |
| G1 tesztek zöldek | nem ellenőrizte az ellenőr | a végrehajtó futtatta: 154 teszt zöld (F112.3), a TestE30 10 teszt az F112.4 után is |
| G2 újrafuttathatóság | ELTÉRÉS | az `e30_meres()` alapfeje `origin/main`, az azóta mozog; az M0b lista helye nincs megadva |
| G2 besorolás | ELTÉRÉS | a `kiegeszitve` valódi hiba (M0a 16., M0b 35.): helyes pontosság 84% / 90% |
| G3 szint a döntés szerint | OK | `SZINT['E30']='FIGYELMEZTETES'` |
| G3/D2 a döntés forrása | ELTÉRÉS | az F112.3 „Felhasználó”, az F112.4 „Orkesztrátor, a felhasználó felhatalmazásával” szöveget ír |
| DT253 állapotjel | ELTÉRÉS | 🟢 jel mellett „Megvalósítva” szöveg állt |
| G4 csak PR | OK | push → 0 találat; PR-módban találatok; `--teljes` → `[]` |
| G5 ok és forrás | OK | 21 adatsor, mind 3 mezős, zárt `ok`-készlet |
| G6 nincs csv | OK | 0 találat az `eszkozok/ellenorzes`-ben |
| D1, D3 | OK | E30 szabad szám; a kétértelmű párok bent vannak |
| felismerési rés | ELTÉRÉS | a nagybetűs (mondatkezdő, csupa nagy) ékezetlen szót nem jelzi, és ez nem volt dokumentálva |
| hatókör (`ir`) | ELTÉRÉS | a `.github/workflows/ellenorzes.yml` (lépésnév) nem volt az `ir` listán |
| zárás | ELTÉRÉS | nincs zárójelentés, `allapot: fut`, `pr` üres — az ellenőrzés után következik |
| A1–A6, C1–C5 | OK / nem alkalmazható | adat, tanulmány, tanító nincs a diffben; E12–E15 0 találat; E17 Δ = 0 |

## Kezelés (F112.5)

1. **G2 újrafuttathatóság** — a napló parancsa a `1a6a6eef` fejre van rögzítve (`e30_meres('', '1a6a6eef')`); az M0b lista a `c668bb36` fájljából reprodukálható (a napló kimondja).
2. **Besorolás** — a `kiegeszitve` két sora „valódi hiba”; a pontosság 84% / 90%; a napló, a DT253 és a `N-F112a` számai frissítve. A szintdöntést ez nem érinti.
3. **Döntés forrása** — a végállapot egységes (orkesztrátor, a felhasználó felhatalmazásával, 2026-10-19; a szülő session üzenete szerint). Az F112.3 „Felhasználó” szövegét az F112.4 felülírta; a történet két állapota nem hiba, a végleges sor az irányadó.
4. **Állapotjel** — a 🟢 marad (az orkesztrátor kérte), a szöveg „Alkalmazásra vár: a PR merge-e”-re javítva.
5. **Nagybetűs szó** — dokumentált korlát a naplóban (szándékos, D3), az újraértékelés (N-F112a) tárgya.
6. **`ir`** — a workflow-fájl felvéve a brief `ir` listájára.
7. **Zárás** — zárójelentés, `lezarva`, `pr`, `lezarva_osszegzes`: lásd a brief fejlécét.

Az ellenőr megjegyzései: a PR címének `[ELLENŐRZŐ]` előtaggal kell kezdődnie, különben az E16 pirosra fut (l. a PR-leírás); a FIGYELMEZTETÉS-találatot a jelentés-formázó „JELENTES: n” alakban számolja (régi viselkedés).
