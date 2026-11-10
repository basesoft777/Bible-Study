---
feladat: 188
cim: A menetek könyvelési és ellenőrzési terhének csökkentése — egy jelentésfájl, gépi előjavítás, kockázat szerinti ellenőrzés, main-őr
kod: TEHER_CSOKKENTES
tipus: feladat
fazis: folyamat
modell: opus
allapot: dontesre_var
ag: claude/f188-teher-csokkentes
ad: feladatonként egy jelentésfájl, gépi formai előjavítás a commit előtt, a CI-t újra nem futtató és kockázat szerint szintezett független ellenőr, main-őr a /kovetkezo-ban; előtte-utána mérés (admin ≤ tartalmi, javítókör ≤ 1, ellenőr ≤ 15 perc)
kovetkezo: "Te: [elteres_kor 2/2] ELLENOR_F188_3 1. tartalmi (DT-F188d, zár), 2. tartalmi (DT-F188e, naplók olvasói bemenete). Utána: T7 — a merge utáni első 3 PR mérése (python eszkozok/ellenorzes/teher_meres.py --pr <n1> <n2> <n3>, N-F188e); a SEMA-rész (a T2 CI-szabállyá emelése és szövege, N-F188a) a #104 merge-e után"
munka: folyamat
olvas: [CLAUDE.md, DONTESEK.md, F184_DOKU_EGY_FORRAS_BRIEF.md, naplok/F184_jelentes.md, naplok/, eszkozok/ellenorzes/]
ir: [.claude/commands/kovetkezo.md, .claude/commands/elteres.md, .claude/commands/befogad.md, .claude/agents/fuggetlen-ellenor.md, .claude/agents/vegrehajto-haiku.md, .claude/agents/vegrehajto-opus.md, .claude/agents/vegrehajto-sonnet.md, BRIEF_SABLON.md, MUNKAMENET.md, adat/SEMA.md, eszkozok/feladatok.py, eszkozok/teszt_feladatok.py, eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/tesztek/, eszkozok/ellenorzes/elojavit.py, eszkozok/ellenorzes/teher_meres.py, eszkozok/ellenorzes/futtat.py, eszkozok/teszt_futtat.py, naplok/F188_jelentes.md]
fugg: []
---

# Brief-tervezet — A menetek könyvelési és ellenőrzési terhének csökkentése (TEHER_CSOKKENTES)

*Orkesztrátori tervezet, 2026-11-10. A felhasználó: „csökkentsük a terhet”. Előtte ezt kérdezte: „akkor miért nem csökkent a teher”, és azt jelezte: „az ellenőrzések, a független és a githubos is, sokáig futnak”. Befogadásra (`/befogad`, külön sessionben).*

**Javasolt fejléc [javaslat]:** `tipus: feladat`, `fazis: folyamat`, `modell: opus`, `munka: folyamat`.

`olvas` / `ir` [a befogadó vezesse le]. A fő fájlok:
- `.claude/commands/kovetkezo.md`, `elteres.md`, `befogad.md`
- `.claude/agents/fuggetlen-ellenor.md`, `vegrehajto-*.md`
- `BRIEF_SABLON.md`, `MUNKAMENET.md`
- `eszkozok/ellenorzes/*` (CI-futtató, PR-komment), egy új előzetes formai javító szkript
- `adat/SEMA.md`, ha érinti
- `naplok/F<nn>_jelentes.md`

`fugg` [javaslat]: a #184 kanonikus helyeit követi. Ütközés: a #182 F26-ja (`.claude/agents/hatar-ellenor.md`, `eszkozok/ellenoriz.py`). A befogadó vezesse le, és ha kell, írja elő a sorrendet.

## Kiindulás — mért teher (2026-11-10)
**Admin és tartalmi fájlok PR-onként** (admin: `naplok/`, `dontesek/uj`, `nyitott/uj`, `*_BRIEF.md`, `NYITOTT_FELADATOK.md`, `FELADATOK.md`, `DONTESEK.md`):

| PR | Commit | Admin | Tartalmi |
|---|---|---|---|
| #664 | 26 | 14 | 8 |
| #666 | 19 | 10 | 5 |
| #668 | 8 | 9 | 1 |
| #665 | 30 | 11 | 20 |

- **A #181 három javítóköre 17 tételt hozott.** Ezek többsége könyvelés: elavult szám a nyitott-tétel szövegében, helyőrző-literál (E32), címsor-jelölés (E5), igehely-formátum adatidézetben (E8), README-példa, nyílt mag eltérése (E35).
- **GitHub CI:** futásonként 1–2 perc. Maga a futás nem lassú; a sok futás a sok kör miatt van.
- **Független ellenőr:** sokszor 20–60 perc. Újrafuttatja a teljes tesztsort, és az E28 miatt mind az öt lexikonlapot újragenerálja (#104, 2026-11-10).
- **A main 2026-11-09 17:52 óta piros volt** (21. szabály), és ez nem tűnt fel: a PR-mód csak a diffet nézi, a main teljes futását senki nem figyelte.
- **Előzmény:** a #184 a szabályok másolatait szüntette meg, a feladatonkénti könyvelést nem.

## Tételek
- **T0 — mérés-alap:** egy szkript, amely PR-onként kiírja az admin és a tartalmi fájlok számát, a commitszámot, a javítókörök számát, valamint az ellenőr és a CI idejét. A cél előre rögzítve: admin ≤ tartalmi, átlagos javítókör ≤ 1, ellenőri futás ≤ 15 perc.
- **T1 — egy jelentésfájl feladatonként.** A napló, a zárójelentés és a független ellenőr jelentése egy fájlba kerül, külön szakaszokban, az ellenőr szakaszát a session menti. Az `olvas`/`ir`, a parancsok és a BRIEF_SABLON igazítása. Régi fájlokat nem írunk át.
- **T2 — számot csak egy helyen.** Nyitott-tétel, README és jelentés nem ismételheti meg egy tábla számait: hivatkozik rájuk, vagy a szám egy generált blokkból jön. A szabály a #184 szerinti kanonikus helyre kerül. A kapu a duplikált számot jelentésként jelzi, nem gátol.
- **T3 — előzetes formai javító** (pl. `eszkozok/ellenorzes/elojavit.py`), amely a commit előtt fut, a végrehajtó lépései között. Gépiesen javítja:
  - a helyőrző-literált (E32: számfüggetlen szövegre cseréli);
  - a TÖRLÉS-SZÁNDÉKOS címsor-jelölést (E5);
  - az adatidézet kódformázását (E8).

  Amit nem tud egyértelműen javítani, azt csak jelzi. Teszt kell rá.
- **T4 — ellenőr-diéta.** A `fuggetlen-ellenor`:
  - a CI eredményét olvassa (zöld/piros, bukott szabály), és nem futtatja újra azt, amit a CI már lefuttatott;
  - az E28-hoz csak a diff által érintett lapot generálja újra;
  - a teljes tesztsort csak akkor futtatja, ha a diff kódot érint.
- **T5 — kockázat szerinti ellenőrzés.**
  - Adat- és tartalmi feladat (adat/, motivumok/, lexikon): teljes ellenőrzés, 2 javítókör.
  - Mechanikus vagy infrastruktúra-feladat, formai CI-javítás: könnyített ellenőrzés, legfeljebb 1 kör.
  - A tisztán formai, gépileg javított tétel nem nyit új kört.
  - A szint a brief fejlécéből jön (`munka`/`tipus`); ha kell, egy új mező. A befogadó vezesse le.
- **T6 — main-őr.** Ha a main teljes CI-futása piros, ez jelenjen meg ott, ahol a sessionök és az orkesztrátor látják: a `/kovetkezo` 1. lépése kiírja, a Feed/Stash jelzi. Indítást nem blokkol, de jelez.
- **T7 — mérés utána:** a T0 szkriptje az első 3 új PR-on, a mért célokkal összevetve. Jelentés, független ellenőr (a saját T4–T5 szabálya szerint), draft PR.

## Nem része
Tartalmi szabályok, a lexikonlap generátora, adatok, lapok.

## Kockázat
- A T1 és a T5 a folyamat-dokumentumokat érinti: a #184 kanonikus helyeit be kell tartani, az E36 és az E37 maradjon zöld.
- A T5 nem gyengítheti a tartalmi ellenőrzést. A felhasználó célja: nincs visszaesés, de nincs fölösleges kör.
