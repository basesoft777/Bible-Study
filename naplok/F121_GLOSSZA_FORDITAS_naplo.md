# F121 napló — F121.0 (a „nevezni” tétel), TBESG G1941 `1`

*2026-10-27 · proveniencia: manual (felhasználói döntés: DT-F131i, 2026-10-27) · végrehajtó: claude-sonnet-5-5*

**Hatókör.** Csak a `TBESG G1941 G1941 1 forditas_hu` sor. A Thayer G1941 `teljes` sor és a terminológia-sorok az F121.0 hátralévő része, nem érintettek.

**Eltérés a brief szövegétől.** A brief 2b szakasza „más néven is nevezni” alakot írt; a DT-F131i szerint a helyette: „nevet adni; ragadványnevet adni, ha a mellékes név a lényeg”. A „nevezni”/„elnevezni” rendben van. A döntés az irányadó.

**Diff (szöveges).**
- előtte: `hívni, nevezni, melléknevet adni: tárgyesettel (klasszikus), …`
- utána: `hívni, nevezni, nevet adni: tárgyesettel (klasszikus), …`
- `allapot=kezi`, `modell` üres, `datum` és `forras_hash` (`794c6af8…`) változatlan; a `megjegyzes` az F121.0-jelölést kapja.

**Ellenőrzés.** Írás előtt a tábla soronkénti összevetése: pontosan 1 sor tért el. `eszkozok/ellenoriz.py`: SÉRTÉS 0. Mérés: a TBESG-sorok `forditas_hu` mezőjében „melléknevet adni”/„melléknéven nevez” előfordulás: 0. `eszkozok/teszt_forditas_kapuk.py`: 90 teszt OK; a `test_meglevo_forditasok` engedélye `{Thayer G1941}`-re szűkítve.
