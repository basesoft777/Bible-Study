# Átadási dokumentum — Motívumlexikon-pilot (ISTENTISZT-001)

*Készült: 2026.09.07, a chat-felület (Claude Sonnet 5) által, egy
teljes munkamenet lezárásaként. Cél: hogy egy ÚJ kontextusablak (vagy
Basesoft saját maga) reprodukálni tudja a munkamódszert, és onnan
folytatni tudja, ahol ez a kör abbamaradt — anélkül, hogy a teljes
gondolkodási utat újra végig kellene járni.*

---

## 1. Mi ez a pilot, és hol tart

A `Bibliai_Motivumlexikon_tervezesi_naplo.md` (2026.08.30 körül) egy
jövőbeli, réteges Motívumlexikon-architektúrát vázolt fel, de a
KAPCSOLATOK-réteget csak elméletileg. Ez a pilot **egyetlen, valós
motívumon** (ISTENTISZT-001, "Segítségül hívni az Úr nevét") próbálta
ki a réteget a gyakorlatban, kis mintás, explicit megállási ponttal —
a projekt saját, már bevált módszertani elve szerint (l. LXX-híd,
tematikus audit).

**Jelenlegi állapot:** a pilot **két teljes lexikon-oldal-változatot**
eredményezett (tudományos + olvasható), **2026.09.07-én a repóba
emelve** a `motivumlog/lexikon_pilot/` könyvtárba.

### A pilot fájljai (repó-elérési út)

| Fájl | Tartalom | Elérés |
|---|---|---|
| `ISTENTISZT-001_TUDOMANYOS.md` | Teljes, minden forrást idéző referencia-lap | `motivumlog/lexikon_pilot/ISTENTISZT-001_TUDOMANYOS.md` |
| `ISTENTISZT-001_OLVASHATO.md` | Rövid, prózai, nyomtatható változat | `motivumlog/lexikon_pilot/ISTENTISZT-001_OLVASHATO.md` |
| `Motivum_kapcsolatok_PILOT.tsv` | A KAPCSOLATOK-réteg pilot-adata, 18 sor | `motivumlog/lexikon_pilot/Motivum_kapcsolatok_PILOT.tsv` |
| Ez az átadási dokumentum | Módszertan + reprodukálhatóság | `motivumlog/lexikon_pilot/Atadasi_dokumentum_Motivumlexikon_pilot_2026-09-07.md` |
| A 12 SQLite-lexikonfájl (Thayer, LSJ, BDB, TBESH, TBESG, SECE, MCGED, MGLNT, LXX, ConcordanceBook, Morphology, ConcordanceMorphology) | Nyers forrás-adatbázisok, l. 3. pont | `konkordancia/lexikonok_nyers/` — **licenc-státusz még nincs tisztázva, l. 3.3 pont** |

---

## 2. A módszertan — hogyan épült fel a 21 igehelyes lista

Ez a projekt legfontosabb, újrafelhasználható eredménye — NEM csak
ehhez az egy motívumhoz szól, hanem bármilyen jövőbeli "rögzült
frázis" jellegű motívum-auditnál alkalmazható.

### 2.1 — A probléma, amit meg kellett oldani

Egy motívum, ami egy **több szavas, rögzült formula** (itt: קָרָא
בְשֵׁם יְהוָה), nem kutatható puszta Strong-szám-grep-pel — az egyes
szavak (H7121, H8034) önmagukban túl gyakoriak, több száz irreleváns
találatot adnak (pl. "és nevezé nevét X-nek" névadás-formula).

### 2.2 — A 8 rétegű ellenőrzési sorozat (végrehajtási sorrendben)

1. **Nyers Strong-szám grep** — kiindulópont, tudottan zajos (itt: 153
   találat).
2. **Kalibrált, pozíció-alapú frázis-keresés** — megmérni a
   tényleges szó-távolságot a MÁR ISMERT, biztos találatokban (itt:
   2-4 pozíció), majd ezt az ablakot alkalmazni a teljes korpuszon,
   megkövetelve egy harmadik elem (itt: isteni név) explicit
   jelenlétét a közelben. **Kód:** `eszkozok/frazis_kereses_pozicio_
   alapon.py` (repóba már bekerült, l. 5. pont).
3. **Hamis-negatív teszt, tágabb ablakkal** — megnézni, mi esik ki a
   szűk ablak alól/fölé, hogy a kalibráció ne vágjon le valós
   találatot. (Itt: 0 új valódi találat a tágabb sávban — megerősítés,
   nem hiba.)
4. **Anaforikus bővítés** — a névmásos ("az ő neve") formákat is
   elfogadni találatnak, HA az isteni név korábban szerepel a
   versben. **Kritikus figyelmeztetés:** ez hamis pozitívokat is hoz
   (itt: 4 db, "valakit néven szólítani" jelentésű, homonim szerkezet)
   — MINDEN jelöltet egyenként, tartalmilag kell ellenőrizni.
5. **A négyforrásos módszertan kötelező alkalmazása** (`PaRDeS_
   gyorsreferencia.md` szerint — ez nem opcionális!): 🔤 Strong, 📖
   Károli-KH (`Karoli_kereszthivatkozasok.tsv`, STEPBible-natív
   kulcsformátum, pl. `Gen.4.26`), 📚 TSK (`TSK_kereszthivatkozasok.
   tsv`, Votes ≥ 15 szűréssel), 🧠 Claude-tudás — **MINDEN vizsgált
   igehelyre, nem csak alkalmi mintavétellel.** *(Ez volt az egyetlen
   tényleges módszertani mulasztás ebben a körben — eleinte csak
   alkalmilag futott le a TSK, ez utólag lett pótolva.)*
6. **BDB szótári idézet-ellenőrzés** — a szótár SAJÁT citációs listája
   (nem csak a definíció szövege) önálló találat-forrás lehet (itt:
   Jer 10:25 = Zsolt 79:6 innen jött elő).
7. **Kétirányú szórend-ellenőrzés** — a formula szórendje fordulhat
   (fő elem elöl vs. hátul, pl. tagadó/hangsúlyos szerkezetben) — ezt
   is le kell futtatni, nem csak az egyik irányt.
8. **Szisztematikus LXX-egyeztetés MINDEN igehelyre** — nem csak
   néhány mintavételre. Ez adta a legtöbb korrekciót: kiderült, hogy
   egy korábbi, kevésbé alapos kör téves "3 különböző görög ige"
   állítást eredményezett — a teljes, szisztematikus ellenőrzés
   kiderítette, hogy valójában 15/17 igehely ugyanazt a görög igét
   használja (csak néhánynál hiányzott a Strong-címke egy eltérő
   kritikai szövegalap miatt).

**A módszertani tanulság, ami mindebből következik:** minden egyes
réteg talált valamit, amit az előző kihagyott vagy tévesen állított —
beleértve a SAJÁT korábbi hibáinkat is. Ez a "mélyebbre fúrás" valódi
tartalma: nem egyetlen módszer egyszeri alkalmazása, hanem egymást
ellenőrző, egymást korrigáló rétegek.

---

## 3. Az új lexikon-fájlok — hogyan lettek beszerezve és hasznosítva

### 3.1 — A beszerzési út (ha meg kell ismételni)

A `biblematedata` (Eliran Wong, `github.com/eliranwong/biblematedata`)
Python-csomag forráskódjában (`package/biblematedata/main.py`)
található egy `"lexicons": ((), "1xlvJ6GURwYCxPnYwo2xuyREutWTeWMcH")`
bejegyzés — ez egy Google Drive fájl-azonosító. Letöltési minta a
forráskódból:

```
https://docs.google.com/uc?export=download&id=1xlvJ6GURwYCxPnYwo2xuyREutWTeWMcH
```

**Chat-Claude ezt NEM tudja saját maga letölteni** (a `docs.google.com`
nincs az engedélyezett hálózati listán a sandbox-ban) — ezt Basesoft
töltötte le és töltötte fel közvetlenül a chatbe, mint fájlmellékletet.

### 3.2 — A fájlok formátuma és lekérdezési módja

12 SQLite-fájl (`.lexicon` kiterjesztéssel), mindegyik egyetlen
`Lexicon` táblával, `Topic`/`Definition` oszlopokkal. Python-
lekérdezési minta:

```python
import sqlite3, re
conn = sqlite3.connect('Thayer.lexicon')
cur = conn.cursor()
cur.execute('SELECT Definition FROM Lexicon WHERE Topic=?', ('G1941',))
row = cur.fetchone()
text = re.sub('<[^>]+>', ' ', row[0])   # HTML-tagek eltávolítása
text = re.sub(r'\s+', ' ', text).strip()
```

**FONTOS kulcs-formátum eltérések fájlonként** (ez okozott hibát a
munka közben, érdemes elsőre tesztelni):

- `Thayer.lexicon`, `LSJ.lexicon`, `SECE.lexicon`, `MGLNT.lexicon` —
  görög Strong-szám nullák NÉLKÜL (`G1`, `G994`, `G1941` — NEM
  `G0994`!).
- `MCGED.lexicon` — KÉTFÉLE kulcs egyszerre létezik: `G####` (Strong)
  ÉS `gkG5####` (Goodrick-Kohlenberger) — **ugyanaz a szám a két
  rendszerben MÁS szót jelenthet** — mindig `G####`-vel keresendő a
  Strong-alapú lekérdezéshez, a `gkG5####`-t figyelmen kívül hagyva.
- `SECE.lexicon` — mindkét nyelvet tartalmazza egyben (`G####` ÉS
  `H####` kulcsok is).
- `BDB.lexicon`, `TBESH.lexicon`, `TBESG.lexicon` — héber/görög
  Strong-szám, nullákkal kitöltve (`H7121`, nem `H07121`) — de a
  `TBESH.lexicon` (SQLite) **egyetlen, konszolidált bejegyzést** ad
  szavanként, szemben a meglévő `TBESH.txt` fájllal, ahol egy szónak
  akár 4 alsora is lehet (G/H/I/J, csak eltérő fejléc-gloss-szal).

### 3.3 — Az egyes fájlok értékelt haszna (teljes táblázat)

L. `konkordancia/Uj_lexikon_fajlok_2026-09-07.md` (már a repóban) —
ott van a teljes, 12 fájlra kiterjedő táblázat, rangsorolva.
Rövid összefoglaló:

- **Magas érték:** Thayer (teljes görög szótár, BDB párja),
  SECE (Louw-Nida szemantikai domain + teljes célnyelvi-megfelelő
  lista mindkét nyelven), TBESH.lexicon (konszolidált,
  módszertani problémát old meg)
- **Közepes érték:** MCGED (pontos NT-előfordulás-szám), BDB.lexicon
  (kb. 20%-kal teljesebb szöveg, mint a meglévő TSV)
- **Célzottan magas, egyébként alacsony:** LSJ (csak klasszikus/
  filozófiai gyökerű szavaknál ad sokat — pl. jövőbeli Pneuma/pszükhé
  study-hoz; összetett igéknél csak átirányít az alapigéhez)
- **Nem javasolt:** MGLNT (duplikátum), LXX.lexicon,
  ConcordanceBook, Morphology, ConcordanceMorphology (navigációs/
  nyelvtani segédeszközök, nem szó-specifikus tartalom)

### 3.4 — A fájlok jelenlegi helye

A 12 `.lexicon` fájl **2026.09.07-én a repóba emelve**, a
`konkordancia/lexikonok_nyers/` könyvtárba. **A licenc-státusz
ekkor még nem lett tisztázva** — a fájlok maguk nem tartalmaznak
explicit licenc-jelzést, ez utólagos, külön feladat marad.

---

## 4. Amit ez a pilot NEM tett meg — nyitva maradt döntések

1. ~~A pilot-oldalak repóba emelése~~ — **megtörtént 2026.09.07-én**,
   l. 1. pont táblázata.
2. **A 12 SQLite-lexikon licenc-tisztázása** — a fájlok maguk a
   repóba kerültek (`konkordancia/lexikonok_nyers/`), de explicit
   licenc-jelzést nem tartalmaznak — ez még nyitott.
3. **A `Segitsegul_hivni_az_Urat_tematikus.md` tényleges bővítése**
   Róm 10:14-gyel és a most felismert A/B/C hármas tipológiával —
   ez **szándékosan** csak a pilot-oldalakban van rögzítve, a study-
   fájlba explicit kérésre ("csak pilot") nem került be.
4. **A 2Móz 33:19/34:5 "be nem sorolható" eset felvétele** a
   `Bibliai_Motivumlexikon_tervezesi_naplo.md`-be mint általánosítható
   nyitott kérdés.
5. **Az 1Kir 18:24 egy-versen-belüli kontraszt** — a KAPCSOLATOK-séma
   (mindig két KÜLÖNBÖZŐ igehely) nem tudja natívan ábrázolni; ezt
   sem vitte be senki a tervezési naplóba.
6. **A `Karoli_Strong_kivonat.tsv` join-tábla bővítése** az új
   igehelyekkel — korábbról is nyitott, itt sem történt meg.

---

## 5. Mit érdemes elsőként megnézni egy új kontextusablakban

1. Ellenőrizd frissen a repót (`git clone` / `codeload.github.com`),
   NE bízz ennek a dokumentumnak az esetlegesen elavuló részleteiben.
2. Nézd meg, hogy a `konkordancia/Uj_lexikon_fajlok_2026-09-07.md` és
   `konkordancia/Javasolt_gorog_oldal_erositese.md` tartalma egyezik-e
   még a fentiekkel (előfordulhat, hogy Basesoft időközben döntött
   valamelyik nyitott kérdésben).
3. Ha a pilot-oldalak folytatása a cél: kérdezd meg, megvannak-e még
   a `/mnt/user-data/outputs/`-beli fájlok, vagy újra kell generálni
   őket ebből az átadási dokumentumból kiindulva.
4. Ha a 12 lexikon-fájl kellene: már ott vannak a repóban,
   `konkordancia/lexikonok_nyers/` alatt — a 3.2 pontban leírt
   módon dolgozz velük.
