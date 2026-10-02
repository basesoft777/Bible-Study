---
feladat: 33
cim: Forrásaink licencének rendezése (az F24 utófeladata)
kod: LICENC_RENDEZES
ag: claude/f33-licenc-rendezes
tipus: feladat
fazis: 1
modell: sonnet
allapot: fut
ad: a licenc-leltár egy mércével, szó szerinti licencidézetekkel; a régi LXX_kivonat kivezetve; a TBESH/STEPBible terjesztési feltételei rögzítve
kovetkezo: "Te: DT-F33a fájlonkénti mozgatási döntés (TBESG marad-e) és az olvasók átírásának új tétele; utána L5, független ellenőrzés, PR"
fugg: [24]
olvas: [adat/licencek.tsv, adat/datasetek.tsv, adat/SEMA.md, DONTESEK.md, naplok/F24_zaras.md, naplok/ELLENOR_F24.md, konkordancia/, eszkozok/]
ir: [adat/licencek.tsv, adat/datasetek.tsv, DONTESEK.md, naplok/LICENC_RENDEZES_zaras.md, naplok/ELLENOR_LICENC_RENDEZES.md, "konkordancia/LXX_kivonat_*.tsv", eszkozok/lexikon_general.py]
---

# Forrásaink licencének rendezése (az F24 utófeladata)

*v1 · 2026.10.01 · Bemenet: a DT-F24 döntés (🟢, alkalmazásra vár), a `naplok/F24_zaras.md` „Maradék” pontja. A feladatszámot a `/befogad` adja.*

## 1. Miért

Az F24 elkészítette a licenc-leltárt (39 sor: 15 `tisztazott`, 24 `tisztazatlan`), de két mércével: hét `tisztazott` sor csak README-összefoglalóra épül. A DT-F24 döntés egy mércét ír elő. Ez a menet alkalmazza, és lezárja a leltár nyitott tételeit.

## 2. Hatókör

Benne van:
- a szó szerinti licencidézetek lekérése;
- az átsorolás egy mérce szerint;
- a TBESH és a STEPBible-sorok terjesztési feltételeinek rögzítése;
- a régi `LXX_kivonat` kivezetése, ha semmi nem olvassa.

Nincs benne: a generált lexikonoldalak és törzscikkek tartalma, a share-alike kérdés (a kereskedelmi döntésig halasztva), a repó láthatósága (a DT-F24 szerint nyilvános marad).

**Futtatási hely:** helyi gép. A cloud proxy korábban blokkolta a külső forrásoldalakat (N27, N29–N31), ez a menet pedig külső LICENSE-fájlokat kér le.

## 3. Lépések

### L0 — Felmérés (csak olvas)

1. Az `adat/licencek.tsv` aktuális állása: sorszám, `tisztazott`/`tisztazatlan` darabszám. Ha eltér a 15/24-től, állj meg és jelentsd.
2. A README-összefoglalóra épülő `tisztazott` sorok listája a `DONTESEK.md` DT-F24 tételéből és a `naplok/F24_zaras.md` „Maradék” pontjából. Várhatóan 7 sor.
3. A régi `LXX_kivonat` olvasói: `grep -rn "LXX_kivonat"` az `eszkozok/`, `adat/`, `lexikon/`, `generalt_proba/`, `.github/` alatt és a gyökér `.md` fájlokban. Az eredmény a zárónaplóba kerül, olvasónként egy sorral (fájl, sor, szerep: kód / adat / dokumentáció / történeti).

### L1 — Szó szerinti licencidézetek

Minden sorhoz, amely `tisztazott` akar lenni vagy maradni:
- a licencszöveg **szó szerinti** idézete a forrás saját LICENSE-fájljából vagy licencoldaláról (nem README-összefoglalóból, nem harmadik fél leírásából);
- a forrás helye (URL, GitHub esetén a commit-hash is), és a lekérés dátuma.

Ezt végezd el a L0/2 sorain, és a 24 `tisztazatlan` sor közül mindazokon, ahol a forrásnak van elérhető LICENSE-fájlja vagy licencoldala. Ahol nincs, a sor marad `tisztazatlan`, és a megjegyzésbe kerül, mit kerestél és hol.

### L2 — Átsorolás egy mérce szerint

- `tisztazott`: csak az a sor, amelyhez L1 szó szerinti idézetet adott.
- `tisztazatlan`: minden más. Ha a README vagy egy forrásoldal állít valamit a licencről, az a megjegyzésbe kerül („a README szerint: …”), az állapotot nem emeli.
- A Mounce (MCGED) sora az F6 D16 szerint marad, a kötelező szó szerinti megjelöléssel. Ezt a sort ne sorold át.

### L3 — Terjesztési feltételek (rögzítés, nem döntés)

1. **TBESH:** a fejlécben álló Online Bible-záradék és a továbbterjesztésre vonatkozó kérés szó szerint a `licencek.tsv`-be. Állapítsd meg, hogy a nyers TBESH-fájl követett fájl-e a repóban.
2. **TAGNT, TAHOT, TIPNR:** a kereskedelmi felhasználás feltétele szó szerint, ha a forrás tartalmaz ilyet.
3. Ha bármelyik feltétel a mostani nyilvános repóval ütközhet: ⛔ **állj meg**, és a kérdést új döntési tételként írd a `DONTESEK.md`-be (helyőrző: `DT-F<nn>`), két lehetőséggel (pl. „marad a repóban” / „a gitignore-olt `_nyers/` alá kerül”). Fájlt ne mozgass.

### L4 — A régi `LXX_kivonat` kivezetése

- **Ha L0/3 szerint nincs kód- vagy adat-olvasója:** a `konkordancia/LXX_kivonat_*.tsv` fájlok törlése, a `datasetek.tsv` sorának törlése, a `lexikon_general.py` licenc-konstansából az `LXX_kivonat`-sor törlése, a `licencek.tsv` sorában az állapot megjegyzése „kivezetve, kiváltója: LXX_OS”.
- **Ha van olvasója:** ⛔ **állj meg**, és jelentsd az olvasókat. Nem törölsz.
- Ellenőrzés a törlés után: `python eszkozok/general.py --cel lexikon --ellenoriz` kilépési kódja 0, a `git diff -- lexikon/ generalt_proba/` üres, a CI 8/b listájából az `LXX_kivonat` eltűnt.

### L5 — A DT-F24 lezárása

A DT-F24 állapota 🟢 → alkalmazva, alatta egy sor: a végső darabszámok és a zárónapló hivatkozása. A meglévő címsor szövegét ne módosítsd, az állapotváltozás a címsor alá kerül.

## 4. Elfogadási kritériumok

| # | Kritérium | Ellenőrzés |
|---|---|---|
| K1 | Egy mérce | minden `tisztazott` sor `forras_hely` mezője szó szerinti licencidézetre mutat, URL-lel és dátummal; README-re hivatkozó `tisztazott` sor 0 |
| K2 | Számok a táblából | a zárónapló darabszámai a végső `licencek.tsv`-ből számolva (nem a menet közbeni jelentésekből) |
| K3 | Mounce érintetlen | az MCGED sor bájtazonos az F24 utáni állapottal |
| K4 | LXX_kivonat | vagy kivezetve az L4 ellenőrzéseivel, vagy ⛔ jelentés az olvasókkal |
| K5 | Szűk hatókör | a `git diff --stat` csak a fejlécben felsorolt `ir` fájlokat érinti |
| K6 | DT-F24 | állapot „alkalmazva”, címsor változatlan |

## 5. Ellenőrzés és zárás

- Független ellenőrzés: `fuggetlen-ellenor`, jelentés a `naplok/ELLENOR_LICENC_RENDEZES.md`-be.
- **Legfeljebb két javítókör.** Ha a 2. kör után sem TISZTA, ne indíts harmadikat: a maradék a zárónapló „Maradék” pontjába kerül, döntési kérdésként. (Az F24 öt köre nem konvergált.)
- Push, draft PR a main-be.
- A záró összefoglaló első sora a PR linkje és a CI állapota.
- **Mérés:** a záró összefoglaló utolsó sora a `/usage` Session blokkjának számai (input, output, cache, modell szerinti bontás), a `/clear` előtt leolvasva.

<!-- KOZVETLEN_FUTTATAS -->
Olvasd el ezt a briefet, majd futtasd az L0–L5 lépéseket sorrendben, saját ágon, külön worktree-ben. A ⛔ pontoknál állj meg és jelentsd, mit találtál. Commit lépésenként, a lépés azonosítójával az üzenet elején. A zárás az 5. pont szerint.
<!-- KOZVETLEN_FUTTATAS -->

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| D1 | Egy mérce: `tisztazott` csak szó szerinti licencidézettel | a README-összefoglaló nem bizonyíték; kereskedelmi irány esetén ez kell | README elfogadása külön fokozattal |
| D2 | A Mounce nem kerül újra vizsgálatra | az F6 D16 (2026.09.19) már eldöntötte | újranyitás az F24 „All Rights Reserved” jelzése miatt |
| D3 | A terjesztési ütközés csak rögzítés, nem fájlmozgatás | a döntés a felhasználóé (DONTESEK.md) | a menet maga teszi át `_nyers/` alá |
| D4 | Legfeljebb két ellenőrzési kör | az F24 öt köre nem konvergált | körök a TISZTA eredményig |
| D5 | Helyi gépen fut | külső LICENSE-fájlok kellenek, a cloud proxy blokkolt | cloud session |
| D6 | A feladat végén `/usage` Session-mérés | párhuzamos sessionök mellett a plan-százalék nem mutatja a feladat költségét | plan-keret két leolvasásának különbsége |
