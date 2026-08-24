# Károli-kivonat, TIPNR tulajdonnév-index, könyv-rövidítés normalizáló tábla

Ez a dokumentum a `konkordancia/Karoli_1908.tsv`, `konkordancia/TIPNR_kivonat.tsv` és
`konkordancia/Konyv_normalizalo_tabla.tsv` fájlokat írja le: forrás, licenc, generálás
módszere. Lásd még a döntési fájl 4.1/4.7 pontját (Károli-forrás döntése) és a 8. szakasz
nyitott pontjait (TIPNR, könyv-rövidítés tábla).

---

## 1. Karoli_1908.tsv

**Forrás:** [scrollmapper/bible_databases](https://github.com/scrollmapper/bible_databases)
(GitHub, MIT licenc a repóra), `formats/json/HunKar.json` — "HunKar: Revideált Károli
Biblia 1908". Maga a Károli-szöveg **közkincs**.

**Letöltés dátuma:** 2026-08-24 (`raw.githubusercontent.com`-ról közvetlen letöltés).

**Struktúra:** `{"translation": "...", "books": [{"name": "Genesis", "chapters": [{"verses":
[{"verse": 1, "text": "..."}]}]}]}` — 66 könyv, standard kánoni sorrendben (megegyezik a
STEPBible README könyv-sorrendjével), összesen 1189 fejezet (a teljes Biblia standard
fejezetszáma — ez önmagában is megerősíti, hogy egyetlen könyv sem hiányzik).

**Oszlopok:**
```
Igehely | Károli-szöveg (teljes vers)
```
- **Igehely:** magyar formátumban, a projekt saját konvenciója szerint — `[Rövidítés]
  [fejezet]:[vers]` (pl. `1Móz 1:1`), szóköz nélkül a rövidítés és a szám között, ahogy a
  `PaRDeS_gyorsreferencia.md` és a sablonfájlok is előírják ("Igehely-rövidítések
  egységesen, szóköz nélkül, pl. „1Móz 2:7"").
- A magyar könyv-rövidítés forrása: lásd lent, `Konyv_normalizalo_tabla.tsv`.

**Sorok száma:** 31 170 vers.

**Validáció:** `1Móz 1:1` szövege pontosan `"Kezdetben teremté Isten az eget és a földet."`
— egyezik a korábban (a döntési fájl 4.1 pontjában) már ellenőrzött scrollmapper-mintával.
Kereszt-ellenőrzésként `Péld 23:7` szövege is egyezik a korábbi körben (KJV/ASV-Strongs
feladatnál) idézett fordítással ("...számítgatja...magában...egyél és igyál...mondja...
akarattal...").

---

## 2. TIPNR_kivonat.tsv

**Forrás:** STEPBible-Data repó, `Proper Nouns/TIPNR - Translators Individualised Proper
Names with all References - STEPBible.org CC BY.txt`. Licenc: CC BY 4.0, Tyndale House
Cambridge / STEPBible.org.

**Nyersadat mérete:** 36 205 sor, ~8,3 MB — nem igényelt könyv-szintű szűkítést, a teljes
fájl feldolgozásra került.

**A nyersadat szerkezete:** minden névvel jelölt személy/hely/egyéb entitáshoz egy
"fejléc-sor" tartozik (pl. `Abraham@Gen.11.26-1Pe=H0085\t...`, ahol `H0085` a személy
**egyesített** Strong-száma, az `Abraham@...` rész pedig a **normalizált, egységes név**),
amit egy vagy több "al-sor" követ (`– Named`, `– Greek`, `– Spelled` stb. kezdettel) —
ezek adják meg a **ténylegesen előforduló névváltozatokat**, mindegyiket saját
(disambiguated) Strong-számmal és teljes előfordulási listával.

**Kulcsfelismerés — egy személynek TÖBB névváltozata is lehet, külön Strong-számmal és
külön előfordulási listával.** Pl. Ábrahám (uStrong `H0085`) fejléc-sora alatt **három**
al-sor található: `H0085` (héber "Abraham", névváltás UTÁNI alak, 119 előfordulás),
`H0087` (héber "Abram", névváltás ELŐTTI alak, 61 előfordulás), `G0011` (görög "Abraham",
ÚSZ). Ez pontosan megfelel a validációs elvárásnak — lásd lent.

**Oszlopok:**
```
Név (normalizált) | Névváltozat | Strong-szám | Nyelv | Igehely
```
- **Név (normalizált):** a fejléc-sor egységesített neve (pl. `Abraham`) — ugyanaz minden
  névváltozat-sorban, ami ugyanahhoz a személyhez/helyhez tartozik.
- **Névváltozat:** az adott al-sor "Translated name" mezője, azaz a ténylegesen használt
  névalak (pl. `Abraham` vagy `Abram`).
- **Strong-szám:** az al-sor saját (disambiguated) Strong-száma — ez különbözik
  névváltozatonként, még ha ugyanahhoz a személyhez tartoznak is.
- **Nyelv:** `héber` (H-Strong) vagy `görög` (G-Strong).
- **Igehely:** STEPBible-natív formátumban (pl. `Gen.17.5`), mint a TAHOT/TAGNT-kivonatnál
  — az "All Refs" mező pontosvesszővel tagolt listájának minden eleme külön sort kap. Ha
  egy versen belül a név többször is előfordul, a forrás egy záró kisbetűvel jelöli
  (pl. `Gen.17.23a`, `Gen.17.23b`) — ezt a kisbetűt a kivonat levágja, de **minden
  előfordulást külön sorban tart meg** (tehát `Gen.17.23` két sorban is szerepelhet).

**Ismert, dokumentált forrás-sajátosság — LXX-only hivatkozások.** 24 sor (0,07%)
`LXX.[Könyv].[fejezet].[vers]` formátumú hivatkozást tartalmaz (pl. `LXX.Gen.46.20`) — ez
a forrás saját jelölése olyan névelőfordulásokra, amik **csak a Septuagintában** (görög
ÓSZ-fordítás), nem a héber maszoréta szövegben szerepelnek. Ez nem hiba, hanem a forrás
dokumentált konvenciója (lásd a nyersfájl saját magyarázatát); a kivonat változatlanul
megtartja ezt a jelölést.

**Kihagyott sorok:** a forrás minden entitáshoz ad egy `– Total` összesítő al-sort is
(minden névváltozat egyesített, rövidített hivatkozás-listájával) — ez **redundáns** a
már felsorolt egyedi névváltozat-sorokkal, ezért a kivonat kihagyja.

**Sorok száma:** 35 522 (4260 egyedi név-entitás, 5775 névváltozat-sor kibontva).

**Validáció:**
- **Ábrahám/Ábrám:** `Abraham` normalizált néven belül `Abraham` (H0085, héber, 247 sor —
  ez a héber+görög "Abraham" alak összesen) és `Abram` (H0087, héber, 61 sor) **külön
  Strong-számmal, külön, teljes előfordulási listával** szerepel — a névváltás előtti és
  utáni alak egyaránt megtalálható.
- **Szárai/Sára:** `Sarah` normalizált néven belül `Sarah` (H8283, héber, 38 sor) és
  `Sarai` (H8297, héber, 17 sor) szintén külön szerepel.
- 0 hibás formátumú Strong-szám, 0 üres Igehely-mező.

---

## 3. Konyv_normalizalo_tabla.tsv

**Cél:** a TAHOT/TAGNT-kivonat STEPBible-natív hivatkozásait (pl. `Gen.1.1`) össze lehessen
kötni a Karoli_1908.tsv és a TIPNR_kivonat.tsv magyar/STEPBible hivatkozásaival.

**Forrás:** a STEPBible-Data repó gyökér `README.md`-jének "Bible reference abbreviations"
szakasza (a hivatalos angol könyv-rövidítés lista, UBS-alapú), párosítva a
Karoli_1908.tsv generálásakor megállapított magyar rövidítésekkel.

**A magyar rövidítések forrása és a két megoldott bizonytalanság.** A rövidítéseket
elsődlegesen a `motivumlog/PaRDeS_motivumok.md` "Könyv szerinti index" szakaszában és a
lezárt tanulmányokban ténylegesen használt formák alapján állapítottam meg (nem
kitalálva). Két könyvnél a korpusz **két, egymásnak ellentmondó** alakot is használt —
ezeknél a felhasználóval egyeztetve dőlt el a végleges forma:
- **Máté evangéliuma:** a korpuszban előfordul kiírva ("Máté 27:51", a Könyv szerinti
  index táblázatban) és rövidítve is ("Mt 27:45", két tanulmány folyószövegében) →
  **`Mt`** lett a végleges (a másik három evangéliummal — Mrk→Mk, Luk, Ján —
  konzisztensebb rövid forma).
- **Ezékiel könyve:** előfordul `Ez` (motívumlog, tematikus tanulmányok, 3×) és `Ezék`
  (Genezis 9 tanulmány, 1×) alakban is → **`Ez`** lett a végleges.

Azoknál a könyveknél, amik még nem szerepeltek egyetlen tanulmányban sem, a Károli-
hagyomány szabványos rövidítését alkalmaztam, a meglévő mintával konzisztens stílusban
(pl. `2Móz`, `3Móz`, `4Móz`, `5Móz` az attesztált `1Móz` mintájára).

**Oszlopok:**
```
STEPBible-rövidítés | Magyar rövidítés | Teljes magyar könyvnév
```

**Sorok száma:** 66 (39 ÓSZ + 27 ÚSZ) — a teljes kánon, egyszeri, végleges táblázatként
(a döntési fájl 8. szakaszának előírása szerint, hogy ne kelljen később könyvenként
bővíteni).

**Validáció:**
| STEPBible | Magyar | Teljes név |
|---|---|---|
| `Gen` | `1Móz` | Mózes első könyve |
| `Pro` | `Péld` | Példabeszédek könyve |
| `Ezk` | `Ez` | Ezékiel könyve |
| `Mat` | `Mt` | Máté evangéliuma |

---

## Közös megjegyzés a licencekhez

- **Károli-szöveg:** közkincs; a scrollmapper/bible_databases repó maga MIT licencű.
- **TIPNR:** CC BY 4.0 (STEPBible.org / Tyndale House Cambridge).
- **STEPBible README könyv-rövidítés lista:** CC BY 4.0 (ugyanaz a forrás, mint a
  TAHOT/TAGNT — lásd `TAHOT_TAGNT_README.md`).
