# Károli-specifikus kereszthivatkozások

Ez a dokumentum a `konkordancia/Karoli_kereszthivatkozasok.tsv` fájlt írja le: forrás,
licenc, generálás módszere. Lásd még a döntési fájl 4.6 pontját, ahol ez a forrás
eredetileg azonosításra került.

## Forrás

- **Repó:** [krisek/HunKar](https://github.com/krisek/HunKar) (GitHub, publikus) — önálló
  SWORD-modul repó a Károli 1908-as revideált fordításához.
- **Fájl:** `hunkaroli_rev.osis.xml` (OSIS XML formátum), ~11 MB.
- **Eredeti szövegforrás:** [szentiras.hu/KG](http://szentiras.hu/KG) (a kereszthivatkozások
  és a versszöveg innen származnak; az Énekek éneke könyve — forráshiba miatt — külön,
  [abibliamindenkie.hu](http://abibliamindenkie.hu/karoli/SNG/)-ról lett pótolva a
  krisek/HunKar repóban).
- **Letöltés dátuma:** 2026-08-24 (`git clone --depth 1`).
- **Licenc:** a modul saját `hunkar.conf` fájlja explicit rögzíti: `DistributionLicense=Public Domain`
  — a szöveg maga (Károli 1908-as revíziója) közkincs, ugyanaz a kiadás, mint amire a
  projekt publikus `Karoli_1908.tsv`-je épül (scrollmapper/HunKar).

## Kimeneti fájl és oszlopok

```
Igehely | Kapcsolódó igehely | Kapcsolódó igehely magyar megjelenítése
```

- **Igehely:** STEPBible-natív formátumban (pl. `Gen.1.1`) — az OSIS `<verse osisID="...">`
  attribútumból, könyv-kód konvertálva STEPBible-natívra (lásd lent).
- **Kapcsolódó igehely:** ugyanabban a formátumban, az OSIS `<reference osisRef="...">`
  attribútumból. Ha a hivatkozás versrange-t ad meg (pl. az eredeti `Gen.2.4-Gen.2.5`),
  ez **egyetlen sorként, tartományként** marad meg (`Gen.2.4-Gen.2.5`), nem lett szétbontva
  két külön hivatkozássá — a forrás minden vizsgált range-je konzisztensen teljes
  `Könyv.fejezet.vers-Könyv.fejezet.vers` alakot használ, rövidített/hiányos forma
  (pl. csak a végvers megadása) nem fordult elő.
- **Kapcsolódó igehely magyar megjelenítése:** a forrás `<reference>` elemének saját,
  megjelenítésre szánt szövege, változatlanul (pl. `Zsolt 33,6`, `1Móz 2,4-5`).

**Strong-szám nincs a fájlban** — ez a forrás kifejezetten csak kereszthivatkozási célra
lett feldolgozva, nem konkordanciának (a forrás maga sem tartalmaz Strong-adatot).

## Könyv-kód konverzió — OSIS ↔ STEPBible

Az OSIS-forrás **saját, STEPBible-től eltérő** hárombetűs (néha négy-öt betűs)
könyv-rövidítéseket használ (pl. `Exod`, `1Kgs`, `Acts`, `Ps`, `Matt`) — ezek **nem**
azonosak a projekt többi datasetjében (TAHOT/TAGNT/TIPNR/Karoli_1908) használt
STEPBible-natív kódokkal (pl. `Exo`, `1Ki`, `Act`, `Psa`, `Mat`). A generálás során **minden**
könyv-kód (mind az Igehely, mind a Kapcsolódó igehely oszlopban, a tartományok mindkét
végén is) egy fix, 66 elemű, pozíció alapú megfeleltető táblával STEPBible-natívra lett
konvertálva — ugyanazzal a kánoni sorrenddel, mint a `Konyv_normalizalo_tabla.tsv`
(mindkét lista Genezistől Jelenésekig azonos sorrendű, standard protestáns kánon).
0 konverziós hiba fordult elő a teljes fájlon.

## Fontos korlát — ez csak JELÖLTLISTA

**Ez a dataset kizárólag a 3/b pont (Kapcsolódó igehelyek) kiindulási jelöltlistájául
szolgál — nem helyettesíti a tartalmi mérlegelést.** A forrás (szentiras.hu szerkesztősége)
által összeállított kereszthivatkozás nem feltétlenül lexikai (közös görög/héber szó)
kapcsolat — lehet tematikus, teológiai vagy tipológiai összefüggés is. **Minden egyes
találatot a tanulmány szintjén, kézzel kell értékelni** (lexikai vs. tematikus
elhatárolás, STEPBible TAGNT/TAHOT-ellenőrzéssel — lásd a sablonfájlok STEPBible-lépéseit),
mielőtt egy adott kapcsolódás bekerül egy tanulmányba. Ez a szabály megegyezik azzal, ahogy
a projekt már korábban is kezelte az openbible.info-alapú kereszthivatkozás-adatot (lásd a
döntési fájl 4.6 pontja) — a Károli-specifikus forrás ennek **kiegészítője**, nem
helyettesítője; a kettő viszonya (melyik megbízhatóbb, kiegészítik-e egymást) továbbra is
nyitott, tényleges összevetéssel eldöntendő kérdés.

## Méret és validáció

| Mérőszám | Érték |
|---|---|
| Feldolgozott versek (teljes Biblia) | 31 168 |
| Versek, amikhez van kereszthivatkozás | 19 817 |
| Generált sorok (= összes kereszthivatkozás) | 32 407 |
| Fájlméret | ~1,1 MB |

**Validáció — Gen.1.1:** pontosan **8** kereszthivatkozás generálódott, számjegyre
egyezve a korábban kézzel ellenőrzött referenciával:

```
Gen.2.4-Gen.2.5, Psa.33.6, Psa.89.12, Psa.136.5, Act.14.15, Act.17.24, Heb.11.3, Job.33.4
```

(A referencia STEPBible-előtti, OSIS-natív alakja `Ps.33.6`/`Acts.14.15`/`Acts.17.24` volt
— a fenti a projekt STEPBible-natív konverziója utáni forma.)

Azok a versek, amikhez a forrásban nincs kereszthivatkozás, egyszerűen kimaradtak a
fájlból — nincs üres sor.
