# ELLENOR_F100 — F100_OLVASO_INDITO_BRIEF.md · `origin/main..cfbc4432` (7 commit)

*Független ellenőr (`fuggetlen-ellenor`, claude-opus-5-5), 2026-10-15. Az ellenőr nem tudott fájlt írni; a jelentést az orkesztrátor rögzítette, lényegében szó szerint, a javításokkal kiegészítve.*

ELTÉRÉS: 5 tétel (mind javítva az F100.9 commitban)

| pont | eredmény | indok |
|---|---|---|
| modell | OK | ellenőr: `claude-opus-5-5` (kért: `opus`); a végrehajtó naplója `claude-sonnet-5-5` |
| DT160 (c) | OK | `teszt_futtat.py` a (c) változatot valósítja meg; 🟢 a DONTESEK-ben |
| DT161 | OK (megjegyzés) | az ütemezett feladat nem jött létre; a tennivaló csak a DONTESEK-ben élt → a brief M2.2 lépésébe felvéve |
| 5/1 kétszeri kattintás | OK (gépi); parancsikonnal nem ellenőrizhető | `flock`-os soros indítás; M2.2 a felhasználóé |
| 5/2 ≤5 mp újraindulás | OK (napló szerint) | 1,0–1,1 mp, legrosszabb 3,3 mp |
| 5/3 szinkron | OK | kulcs: `meta.epites_ts` (nem mtime); `cp` → ideiglenes név → `mv -f` (atomi) |
| 5/4 lábléc, regiszter-őr | OK (statikusan) | nincs új `class=`; futtatással nem ellenőrizte |
| 5/5 tesztidő | számtan OK, az idők nem ellenőrizhetők | 215 teszt, az összegek egyeznek |
| **E1** | ELTÉRÉS → javítva | `teszt_futtat.py` WSL-ből, Flask nélküli Pythonnal hamis zöldet adott → most újraindul a WSL venv-jével, ennek hiányában (és hiányzó adatbázisnál) 2-es kilépési kóddal megáll |
| **E2** | ELTÉRÉS → javítva | az M1 napló indítási tartománya kihagyta az M2 napló 13,3 mp-ét → 6,4–13,3 mp, a nem igazolható futások jelölve |
| **E3** | ELTÉRÉS → javítva | az óraeltérés-magyarázat proveniencia nélküli → „oka nem ismert” |
| **E4** | ELTÉRÉS → javítva | az elfogadási feltétel körkörös lett („a mért idő alatt”) → együtt 5 perc (300 mp); mért: 274,6 s |
| **E5** | ELTÉRÉS → javítva | az `ir` mezőből hiányzott az M0-napló, a DONTESEK.md, az ellenőri jelentés |
| .bat tartalék-ág | OK (megjegyzés) | `indit.sh` hiányában a régi indítás fut, figyelmeztetéssel; a főcheckout most a `claude/tervezo-mod` ágon áll |
| CI-ellenőrzés | OK | hibaszintű találat nincs (E25/E27 meglévő jelentések) |
| Ell.1–5, ⛔ pontok | OK | az M0 és az M2 ⛔ betartva |
