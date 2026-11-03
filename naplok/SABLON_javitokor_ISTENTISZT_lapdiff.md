# Az ISTENTISZT-001 lapjának változása a sablon-javítókörben (N87, 2026-11-03)

Az 1. kiadás lapja a generátor javítása miatt változott — **a 2. kiadás függő változása** (az `OLVJ_ISTENTISZT_lapdiff.md` módján).
Adatváltozás és tartalmi állítás nincs; csak a forma (a felhasználó lapnézet-észrevételei, 2026-11-03):

| Változás | Cserélt sor (93-ból) | Példa |
|---|---|---|
| „Mit mutat ez a rész?” címke kikerül, az összefoglaló marad (láthatatlan jel a bekezdés végén) | 51 | `**Mit mutat ez a rész?** A lap szakaszai…` → `A lap szakaszai…` |
| ikon a „Funkció (a motívumban)” oszlopban kikerül | 21 | `🌱 alap-előfordulás` → `alap-előfordulás` |
| a 15 jegyű UBS-/DBH-kód nem látszik a jelentés-cellában | 16 | `` `006562001006000` — to cry out `` → `to cry out` |
| külön ⓘ a lábjegyzet-jel mellett kikerül | 22 | `· 1 ⓘ[^1]` → `· 1[^1]` |
| az 1/a „Funkció:” sora új bekezdésben | minden igehely | üres sor a magyarázat és a `Funkció:` között |

(Egy cserélt sor több változást is hordozhat, ezért az oszlop nem összegződik 93-ra.)
Teendő: a következő kiadás-sor (`kiadas=2`) `valtozas` mezője ezt is nevezze meg. A lap szó szerinti diffje:
`git diff main -- lexikon/ISTENTISZT-001_TUDOMANYOS.md` a PR-ban.
