# F30 — számkiosztás: napló

*2026.10.05 · `claude/szamozas` · végrehajtó: Sonnet 5.5 (a brief `modell: sonnet`)*

## SZ.0 Felmérés (a `main` 2026.10.05-i állapota, `bd39b91`)

**A brief előfeltevései részben elavultak**, mert a main azóta sokat nőtt:

| Kérdés | Lelet |
|---|---|
| `DONTESEK.md` végleges DT-azonosítói | DT1–DT7, **DT18**, DT19, DT22–DT28 (DT20, DT21 az F21-ben DT-F21i/j-re nevezve át) |
| Helyőrzők (definíciós sorral) a main-en | **99**: 70 DT-F (F21, F22, F24, F26, F32, F33, F34, F35, F38, F39, F41, F42, F43, F46, F52) és 29 N-F (F08, F17, F21, F22, F33, F34, F35, F41, F46, F53) |
| Árva helyőrző (csak hivatkozás, nincs definíciós sor) | 17: DT-F16, DT-F17, DT-F22, DT-F22b, DT-F22d, DT-F28, DT-F37, DT-F42, DT-F51, DT-F52, N-F08, N-F17, N-F22, N-F33, N-F38a–c |
| `NYITOTT_FELADATOK.md` legnagyobb N-száma | **N46** (a többi N-F helyőrző) |
| Nyitott távoli ágak (13 nincs mergelve) azonosítói | `claude/befogad-jeloltek`, `claude/f38-opus-vakproba`: csak a main-en meglévő DT25-re hivatkoznak; `claude/macula-import`: elavult ág, a #87 squash-sal mergelve (a DT7 ma is a main-en); a többi nem hoz `DT<n>`/`N<n>` azonosítót. **Helyőrzőre átállítandó ág nincs.** |
| D-sorozat (`FELADATOK.md` „Döntésnapló”, D1–D50) | **kézzel nő** (a generált blokkokon kívül áll), tehát a 4. pont érvényes: `D-F<nn>` helyőrző; az Action és az E26 kezeli |

Következő szabad számok a futás előtt: DT29 (a DT28 után), N47, D51.

## SZ.4 a DT18

A DT18 a #18 (Nave) feladatszámából képzett szám (a `naplok/F16_zaras.md` is „a DT5-ig és DT18-ig foglalt” alakban említi, nem tartalmi számként), tehát **nem szándékos**. Átszámozva **DT29**-re (a DT28 utáni első szabad). Cserélt fájlok: `DONTESEK.md`, `F18_NAVE_IMPORT_BRIEF.md`, `NYITOTT_FELADATOK.md`, `adat/SEMA.md`, `adat/datasetek.tsv`, `naplok/F18_import_naplo.md`, `naplok/F18_zaras.md`. **Változatlan marad** a lezárt ellenőri jelentések (`naplok/ELLENOR_*.md`) és a `naplok/F16_zaras.md` régi említése, a `FELADATOK.md` (generált, a main-Action írja) és a F30 brief; a DT29 sora „korábbi azonosító: DT18” jelzést kap (mint az F21-átnevezésnél).

Mellékleletek (a `N-F30a` tételben): a DT19 sora (#19 KJV/ASV) ugyanilyen feladatszám-alakú, és a régi F21-kimenetekben a „DT19” az F21-re is utal (ütközés); az átszámozása nem az F30 tárgya.

## Eszköz, Action, CI

- `eszkozok/szamkiosztas.py` (`--proba`, `--ir`, `--uzenet-fajl`, `--gyoker`): a definíciós sor fájlbeli sorrendjében oszt számot (DT: `DONTESEK.md` sor eleje; N: `NYITOTT_FELADATOK.md` felsorolás; D: `FELADATOK.md` táblázatsor). A következő szám: a fájlban előforduló legnagyobb szám + 1 (kimaradt számot nem használ újra; **egy szöveges említés is számít**, ezért a döntéssorok ne írjanak le még ki nem osztott számot). Sorvég- és UTF-8-megőrző (bájtszintű írás), csv-modul nélkül, idempotens. A `szamkiosztas-kihagy` jelölésű sor és a magyarázó fájlok (`KIZART`) kimaradnak a cseréből.
- `eszkozok/szamkiosztas_oroklott.txt`: a **99 már meglévő helyőrző**; amíg itt állnak, nem kapnak számot. Indok: kiosztásuk 138 fájlban 2237 cserét jelentene (köztük `adat/forditasok.tsv`, `adat/licencek.tsv`, `naplok/*.tsv`, lezárt jelentések), nyitott ágak ütközésével; ez tartalmi döntés (**DT-F30a**, ⛔).
- `.github/workflows/szamkiosztas.yml`: main-pushra, a `feladatok.yml` mintájára (App-token, `[bot]`-guard, közös concurrency-csoport, `ref: main`); csere után újragenerálja a FELADATOK.md-t és a feladattérképet, és egy gépi commitot tesz `szamkiosztas: DT-F.. → DT.., …` üzenettel.
- **E26** (a következő szabad E-szám; E20–E24 foglalt): `szabalyok.e26_vegleges_szam_agon`, PR-eseményen HIBA, ha a diff új végleges azonosítót definiál, base-nél nagyobb DT-/N-számra hivatkozik, vagy egy helyőrzőt kétszer definiál. Üzenet: „Az ágon helyőrző kell (DT-F<nn>), a végleges számot a merge adja.” Kivétel: `SZÁMKIOSZTÁS-SZÁNDÉKOS:` kezdetű sor a commit-üzenetben (az F30 DT18→DT29 átszámozása így megy át) és a push-esemény (main).
- Tesztek: `eszkozok/ellenorzes/tesztek/test_szamkiosztas.py` (10 teszt, zöld).

## SZ.6 Próba

Lásd a lap alját (a helyi próba kimenete).
