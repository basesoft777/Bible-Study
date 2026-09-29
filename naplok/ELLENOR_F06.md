# ELLENOR_F06 — F06_FORRASFELMERES_BRIEF.md · `origin/main..HEAD` (`32175e2..1cae02b`, 13 commit, 59 fájl)

*Készítette: `fuggetlen-ellenor` (a fájlba az orkesztrátor mentette, mert az ellenőrnek nincs Write-eszköze). Eljárási eltérések: `git fetch`-et nem futtatott (a base a helyi `origin/main` = `32175e2`); két git-hívásnál pipe-szűrő futott; az idézet- és sorszám-ellenőrzés egy része Grep/Read-del ment.*

**Összegzés: ELTÉRÉS, 13 tétel.** A javítás után újraellenőrzés kell a 1–5. pontra.

## Rendben (OK)

- **D1** Actions: a mérés-commitok szerzője `github-actions[bot]`.
- **D2** LLM csak licencre: `F06_koltseg.tsv` mind a 29 sora `minimax/minimax-m3`; a mérőszkriptek nem hívnak modellt.
- **D3** ≤12 000 karakter, nincs darabolás: 6 `kezi_hosszu` (`F06_licenc.tsv:7,13,19,29,30,32`), `licenc.py:33` `PROMPT_LIMIT = 12000`.
- **D4** idézetkapu: `licenc.py:56`; a 13 nem üres idézet szó szerint (whitespace-normalizálva) megvan a `F06_licenc_szovegek/` fájlokban.
- **D5** BSB-küszöb előre rögzítve: `kuszob.txt` egyetlen commitja `1a9bd6a` (17:08 UTC), az első mérés `bbbbdfa` (17:35 UTC); azóta nem módosult.
- **D6** nincs adat az `adat/`, `konkordancia/`, `lexikon/` alatt (`git diff --stat` üres); 8697 hozzáadott, 0 törölt sor.
- **Kulcs-grep:** csak névhivatkozás és `${{ secrets… }}`; `git log -G"sk-or-v1"` nincs találat; a kulcs csak a `licenc` job `env`-jében van.
- **`FORRAS_jelentes.md`:** csak a fejléc változott (+2 sor, 0 törölt).
- **Számok visszakereshetősége:** a Nave, KJV/ASV, BSB és Macula számok mind egyeznek a TSV-kkel (részletes lista az ellenőr jegyzetében: 5322, 32253, 4980, 92609; 31102/31099/30978; 1533/1515/18/98,83; 39/929/167/4807/4806; 87 = 39+38+8+2).
- **Saját olvasatú idézetek** (Macula, eBible, `basokant` README, `theonize` LICENSE, `elcafe7` LICENSING.md, BSB README): szó szerint megvannak.
- **`nincs_adat` értelmezése**, **IMPORT-javaslatok**, **A2/A3/A4/A5/A6**, **Lista 1–4**: OK.
- **A1** `lekerdez.py scan H2895` és `H0582 --szakasz "1Móz 32"` egyezik; mellékesen a `CLAUDE.md` TAHOT-hiánylistája (Zsolt 88 stb.) elavultnak látszik (`scan H3068 --szakasz "Zsolt 88"` → 4 igehely). Nem a diff hibája.

## Eltérések (súlyossági sorrendben)

1. **A #8 bemenetének leírása rossz** (`F06_forras_jelentes.md:58-59,62`):
   - `HEBER_SZO_GOROG_NELKUL` (38 sor): a jelentés „görög társ nincs rendelve”, de 27/38 sorban van görög szóalak (pl. `F06_macula_87_hely.tsv:26,28,51,85`), csak görög Strong nincs hozzá; valóban görög nélküli: 11. Az állapotot a `macula.py:147-150` a `greekstrong` alapján adja.
   - `HEBER_SZO_NINCS_A_VERSBEN` (8 sor): mind a 8 sor kulcsszava `—`, Strong üres (`F06_macula_87_hely.tsv:20,45-49,79-80`), tehát nem volt mit keresni; a jelentés számozási okkal („N28”) magyarázza és „nem talált”-nak nevezi, ami téves. A számozás csak a 2 `NINCS_VERS`-re magyarázat (4Móz 13:34).
2. **CI E16 HIBA:** a PR érinti az ellenőrzőt (`.github/workflows/f06_forrasfelmeres.yml`), ezért a PR címe `[ELLENŐRZŐ]` előtagot kér. E2–E15: 0 találat.
3. **Idézet nélküli „idézettel” ítéletek** (`F06_forras_jelentes.md:26,28,29,30`): kjvstudy ISC, 1John419 GPL-3.0, scripture-intelligence MIT, luvlylavnder KJV/NIV MIT; a KJV-Strongs-EBook „GPL-3.0” jelöletlen saját olvasat (README `:279-294`, `kezi_hosszu`). Sérti a brief 4. lépését.
4. **kennethreitz:** a `F06_kjv_asv.tsv:38` `szo_szintu_strong_bizonyitek = igen`, a jelentés (`:29`) szerint „nincs címkézett adatfájl”; az ellentmondást nem nevezi meg.
5. **„Minden szám F06-kimenetből jön” (`:5`) hamis:** a „900 mp” (`:31`) csak a `94de78d` commitüzenetben van (a TSV `420 mp`-et mutat); a 78% (FJ1) és a 32254/4951/92610 (FJ4) más forrásból való.
6. **Jelöletlen vagy túl erős értelmezések:** Macula versszám-eltérés „versszámozási” (`:47`; Jób: Macula 1070, TAHOT 1036, `csak_macula=42`, `csak_tahot=8`); „nem letöltési hiba” tényként (`:48`; a példakód `1Sam`, a mért fájlkód `1Sa`); Macula „licenc rendben” (`:50`; az SDBH `macula_hebrew__LICENSE.md.txt:21` szerint „Used with permission”, nem CC BY); a 2895-ös „tövesítési eltérés” tényként (`:41`, az FJ3 csak „feltehetően”-t írt).
7. **Kisebbek:** `F06_koltseg.tsv:1` fejléc `0.011926` vs. sorösszeg 0,011927; a brieffel nem egyező javaslat-kategóriák („NEM (hézag)”, „nem minősítve”; `:27,31`); elavult állapotsor a `F06_felmeres.md:68`-on („a válasz még nincs meg”).

## Nem ellenőrizhető

- Az összköltség a 36606454914-es futásra (nincs F06.4-commitja).
- A ⛔ válasz a repóból (`F06_felmeres.md:81-88`; tartalmi tétje nincs: `nincs_tahot=0`, a két nevező azonos).
- CI-jelentés nem állt rendelkezésre; a zárás (zárójelentés, `FELADATOK.md`, PR) még nincs a diffben.
