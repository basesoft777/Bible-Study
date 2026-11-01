ELTÉRÉS: 4 tétel

# ELLENOR_F142 — `F142_THAYER_M3_BRIEF.md` (#142, THAYER_M3)

Tartomány: `origin/main..HEAD` (F142.20–F142.29), ág `ccr-676ffb53-9qo1to`. Ellenőr: `fuggetlen-ellenor` (`claude-opus-5-5`, a kért `opus`, egyezik). A jelentést az ellenőr szövege alapján az orkesztrátor írta fájlba (az ellenőrnek nincs Write eszköze).
Az ellenőr nem futtatta: `teszt_lanc.py`, `teszt_bont.py`, `ellenoriz.py`, `feladatok.py ellenoriz` (a szerepe nem engedi) — ezek a pontok NEM ELLENŐRIZHETŐK.

## Eltérések (súlyossági sorrendben)
1. **G0282 sz6** (`adat/forditasok.tsv:5389`): „Vö. Bleek a héb. II. köt., 2, o. 305 kk.” értelmetlen; a forrás „Bleek on Heb.” a Zsidókhoz írt levélre utal. A „kapu-kényszer” indoklás téves: a lánc `--kivetel Heb.` kapcsolója erre való (`forditas.py` 114–122., 171., 268., 277. sor), a `Heb.` nincs a `thayer_sigla.tsv`-ben; a régi `kezi` sor (61.) helyesen „a Zsidókhoz írt levélhez”. Az új sor megjegyzése üres.
2. **⛔ megállás be nem tartva:** a Heb./etc. szemantikai kérdés tartalmi, mégsem lett `DONTESEK.md`-tétel, a brief `lezarva` lett.
3. **Elfogadási feltétel 5. pontja:** a végrehajtó saját mérése szerint `teszt_lanc.py` 1, `teszt_bont.py` 2 hiba; hogy a main-en is fennáll-e, nincs igazolva.
4. **(enyhe)** a 4 `elavult` sor megjegyzésében `DT-F132c` áll DT329 helyett — az eszköz írja szövegszerűen (`forditas.py:219`), nem a végrehajtó hibája.

## Rendben
- DT332 (1): 2/7/6/2/17/6/2/10 = 52 szakaszsor, lefedettség teljes; Δ sorszám +52 (E17), más tábla Δ = 0.
- DT329: csak a 4 nem `kezi` `teljes` sor kapott `elavult` jelölést (G1311, G5010, G0012, G5351); a `kezi` sorok (G1944, G5590, G0282, G4151) változatlanok.
- `bukottak.tsv` kiürítése indokolt (az 5 bukás oka a #145 kapujavítása; mind az 5 Strong teljesen fordítva).
- G5351 `etc.`→`stb.` valóban kapu-kényszerű (16. kapu, nincs kivétel-paraméter); az angol idézet vegyes nyelvű lett — nyitott.
- Lánc, prompt, javítótábla, sigla-tábla nem változott; E12–E15: 0 találat. Proveniencia a naplóban megvan.
- `futtat.py` (a diff fájljaira): E27 2 HIBA a `FELADATOK.md:66/69` hivatkozott commitjaira — sekély klón miatt, a fájl nincs a diffben; E30 4 figyelmeztetés (`kezi` → `kézi` commit-üzenetekben).

Melléklet: G4151 sz16 és G5590 sz6 a forrás szakaszolási hibáit hűen viszi (`thayer_szakaszok.tsv:12848, 16986`) — a #132 bontójának kérdése.
