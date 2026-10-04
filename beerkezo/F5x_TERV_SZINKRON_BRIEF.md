---
cim: TERV_SZINKRON — a tervdokumentumok átvezetése a repó állapotára
sorszam: "#5x (a FELADATOK.md-ben véglegesítendő)"
nev: TERV_SZINKRON
verzio: 1.0
datum: 2026-10-04
munka: folyamat
modell: sonnet
fugg: [47]
olvas:
  - ADATVAGYON_TERV.md
  - MUNKATERV.md
  - VIBE_GUIDE.md
  - FELADATOK.md
  - DONTESEK.md
  - NYITOTT_FELADATOK.md
  - adat/SEMA.md
  - CLAUDE.md
  - MUNKAMENET.md
  - a kiváltó esemény fájljai (lásd 2. pont)
ir:
  - ADATVAGYON_TERV.md
  - MUNKATERV.md
  - VIBE_GUIDE.md
  - naplok/F5x_TERV_SZINKRON_<datum>.md
kovetkezo: "ismétlődő; a 2. pont eseményeinél indul"
---

# F5x — TERV_SZINKRON

*A fejléc mezőit a `BRIEF_SABLON.md` aktuális alakjához kell igazítani (a `munka`,
`modell`, `fugg`, `olvas`, `ir` mezők a KONTEXTUS K-D4 és a `feladatok.py` ellenőrzése
szerint). Ez a brief `munka: folyamat`: nem ír motívumfájlt, csomagolható.*

## 1. Cél

A három tervdokumentum (`ADATVAGYON_TERV.md`, `MUNKATERV.md`, `VIBE_GUIDE.md`) a repó
**hatályos** állapotát írja le, ne a megírásuk napján érvényeset. A feladat minden
futása egy szinkron: a kiváltó esemény óta született döntéseket és státuszváltozásokat
átvezeti a dokumentumok érintett szakaszain — **és csak azokon** —, a döntésnaplóba
verziósort ír, és naplózza, mit változtatott és miért.

A szinkron nem újraírás. Ami nem változott a repóban, az a tervdokumentumban sem
változik; stilisztikai vagy szerkezeti javítás nem a feladat része.

## 2. Mikor fut (kiváltó események)

A feladat ismétlődő. Egy futás akkor indul, ha az alábbiak egyike bekövetkezett
a legutóbbi szinkron óta (a napló utolsó bejegyzése a viszonyítási pont):

| esemény | miért kiváltó |
| --- | --- |
| a `#23` M0 ⛔ jelentése befogadva | eldönti a motívum-sémát és a mélységi szinteket; a tervjegyzet 16. és 22. szakasza, a MUNKATERV 4–5. szakasza ettől függ |
| új `DT-` tétel a `DONTESEK.md`-ben, amelynek *érintett fájlja* a három tervdokumentum egyike, vagy amely licencet, forrást, sorrendet, sémát módosít | a tervdokumentum döntés előtti állapotot írna |
| a `#51` KONZISZTENCIA CI-szabálya a három dokumentum egyikét jelzi | gépi jelzés a driftre |
| a MUNKATERV egy hulláma lezárult (a hullám minden feladata ✅ vagy ⛔) | a következő hullám bemenetei változhattak |
| a felhasználó kéri | — |

Ha egyszerre több esemény áll fenn, egy futás kezeli mindet.

## 3. Bemenet

- a három tervdokumentum (a repó gyökerében, hatályos példány)
- `FELADATOK.md` (státuszok, függések, új sorok), `DONTESEK.md` (új DT-tételek),
  `NYITOTT_FELADATOK.md` (új N-tételek), `adat/SEMA.md` (séma-változás),
  `CLAUDE.md`, `MUNKAMENET.md` (szabály-változás)
- a kiváltó esemény saját fájljai: a `#23` M0 jelentése (`naplok/F23_M0_*.md`),
  az új brief-verziók, a `#51` jelzése
- a legutóbbi szinkron naplója (`naplok/F5x_TERV_SZINKRON_*.md`), benne a
  viszonyítási commit

## 4. Lépések

1. **Viszonyítási pont.** Olvasd a legutóbbi szinkron-napló `kiindulasi_allapot`
   sorát (commit, dátum, FELADATOK-verzió). Ha nincs napló: a tervdokumentumok
   döntésnaplójának utolsó sora a viszonyítási pont.
2. **Delta-lista.** Gyűjtsd össze, mi változott a viszonyítási pont óta:
   - `git diff <commit>..HEAD -- FELADATOK.md DONTESEK.md NYITOTT_FELADATOK.md adat/SEMA.md CLAUDE.md MUNKAMENET.md`
   - az új DT- és N-tételek sorszáma és egy mondata
   - a FELADATOK-sorok státuszváltozása (⬜/▶/⛔/✅), függés-változása, új sorai
   Írd a naplóba táblaként: `változás | forrás (fájl, tétel) | érinti-e a tervet (igen/nem) | melyik szakaszt`.
3. **Érintettség.** Minden delta-sorra döntsd el, érinti-e a három dokumentum
   valamelyik szakaszát. A szabály: akkor érint, ha a szakasz egy állítása a
   változás után **hamis** vagy **hiányos** lenne. Nem érint, ha csak részletesebb
   lehetne. A nem érintő sorokat is a naplóban hagyd (`nem`), hogy a következő
   futás ne nézze újra.
4. **Átvezetés.** Az érintett szakaszokat írd át a változás mértékéig:
   - státusz, sorszám, név, függés: a sor cseréje;
   - döntés, amely egy állítást megfordít (pl. licenc, sorrend): az állítás cseréje
     és a döntés hivatkozása (`DT-…`), a régi állítás nem marad meg áthúzva;
   - új feladat a repóban: a MUNKATERV 4a térképébe sor, a hullámokba besorolás,
     ha a terv feladatai közé illik;
   - a MUNKATERV javasolt sorszámai (`#5x`) a FELADATOK-ban véglegesített számra
     cserélve, ha ott már állnak.
   Amit a döntés nem érint, ahhoz ne nyúlj.
5. **Döntésnapló-sor** mindhárom dokumentumban, ha változott: `dátum | vN: <mi
   változott, melyik DT/N/#-re hivatkozva> | státusz`. A verziószám eggyel nő.
6. **Kiindulási állapot sor** az `ADATVAGYON_TERV.md` döntésnaplója fölé (vagy a
   meglévő frissítése): `kiindulási állapot: FELADATOK <verzió>, merge <commit>,
   <dátum>` — ez a következő szinkron viszonyítási pontja.
7. **Napló.** `naplok/F5x_TERV_SZINKRON_<datum>.md`: a 2–3. pont táblája, az
   átírt szakaszok listája (dokumentum, szakasz, egy mondat), a nem átvezetett,
   de kérdéses tételek (lásd 6. pont), a `kiindulasi_allapot` sor.
8. **PR.** Egy draft PR, a commit-üzenet UTF-8 fájlból; a `fuggetlen-ellenor` a 7.
   pont elfogadási pontjai ellen.

## 5. Kis minta

Az első futás a 2026-10-04-i állapotra (merge `117bafc`): a delta-lista és a 3. pont
érintettsége **csak** az `ADATVAGYON_TERV.md` 0., 2., 17.1 szakaszára (licenc,
DT-F33e–j) és a MUNKATERV 2. szakaszára (DT-M6). Ezt mutasd meg, állj meg; a
teljes átvezetés a jóváhagyás után.

## 6. Megállások (⛔)

- Ha egy változás a tervdokumentum **alapfeltevését** fordítja meg (példa: a
  licenc-döntés a hosting-utat; a #23 M0 a motívum-séma alakját), a 4. pont előtt
  állj meg: a naplóban írd le, mely szakaszok érintettek és milyen irányban, és
  nyiss `DONTESEK.md`-tételt a `DONTES_KERDES_SABLON.md` szerint. A felhasználó
  dönt, mi kerüljön a tervbe.
- Ha két forrás ellentmond (pl. a FELADATOK és egy brief fejléce), ne dönts: a
  naplóba, és ⛔.
- A `VIBE_GUIDE.md`-t csak akkor írd át, ha a MUNKAMENET vagy a BRIEF_SABLON
  szabálya változott; a feladat-vezérfonalat (5. szakasz) csak a sorszámok és nevek
  cseréjéig.

## 7. Elfogadási pontok

1. A naplóban minden delta-sor szerepel, `igen/nem` érintettséggel és indokkal.
2. Az átírt szakaszok listája és a `git diff` egyezik: nincs olyan módosított sor a
   három dokumentumban, amely nem szerepel a listában.
3. Minden átírt állítás mellett ott a hivatkozott DT-/N-/#-tétel.
4. A tervdokumentumokban nem maradt olyan állítás, amelyet a delta-lista egy tétele
   megfordít (teszt: a delta-lista `igen` sorai a dokumentum szövegében keresve nem
   adnak régi alakot).
5. A döntésnapló-sor és a kiindulási állapot sor bent van.
6. A dokumentum többi része bájtazonos a futás előttivel.

## 8. Nincs benne

A tervdokumentumok tartalmi továbbgondolása, új szakasz, új javaslat; a repó más
fájljainak módosítása; a FELADATOK/DONTESEK szerkesztése (az a kiváltó eseményé);
a `#51` CI-szabály implementálása.

## 9. Megjegyzés a chat-dokumentumokhoz

A claude.ai-ban élő három doc a repóba költözés után **nem forrás**. Ha a felhasználó
a chatben akarja átnézni, az md-t viszi oda; a chatben tett módosítás csak akkor
hatályos, ha md-ként visszakerül a repóba és ezen a briefen átmegy.

## Verziók

| verzió | dátum | változás | ok |
| --- | --- | --- | --- |
| 1.0 | 2026-10-04 | első változat | a tervdokumentumok elavulása a D34–D41 / DT-F33e–j átvezetése után; a szinkron ritmusát a repó eseményei adják, nem a chat |
