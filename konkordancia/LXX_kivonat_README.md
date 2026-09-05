# LXX kivonat — teljes Ószövetség (39 könyv)

Ez a dokumentum a `konkordancia/LXX_kivonat_[Könyv].tsv` fájlok **közös**
módszertanát, oszlopformátumát, licenc-státuszát és ismert korlátait írja le —
egyetlen helyen, minden könyvre érvényesen. A könyvenkénti egyedi jelenségek a
4. szakaszban vannak felsorolva, csak ott, ahol van mit mondani.

## 1. Forrás és módszertan

- **Weboldalak:** [studybible.info](https://studybible.info/) két oldaltípusának
  kombinálása, fejezetenként:
  - `LXX_WH` (Septuagint OT, Westcott-Hort) — **elsődleges** forrás, megtartja a
    morfológiai kódot.
  - `/interlinear/` (ABP — Apostolic Bible Polyglot) — **kiegészítő** forrás:
    csak azokhoz a szavakhoz nyúlunk hozzá, amiket az LXX_WH oldal nem taggel
    Strong-számmal, és csak akkor, ha a közvetlen szövegkörnyezet (előző/
    következő Strong-szám) mindkét oldalon egyértelműen egyezik.
- **Szkript:** `eszkozok/lxx_kivonat_fetch_v2.py --konyv <Angol könyvnév>
  --fejezet-tol 1 --fejezet-ig <utolsó fejezet> --kimenet
  konkordancia/LXX_kivonat_<Könyv>.tsv [--versifikacios-terkep
  konkordancia/LXX_versificacios_terkep.tsv --karoli-konyv-prefix <Károli-
  rövidítés>]`. A `--versifikacios-terkep` opció azoknál a könyveknél
  szükséges, ahol a görög LXX belső fejezet-/versszámozása eltér a
  maszoretai/Károli számozástól (a legtöbb könyvnél ez fennáll valamilyen
  mértékben — pl. a zsoltár-feliratok saját LXX-vers-számot kapnak, Jóelnél a
  nyers oldal belső zárójeles hivatkozásai a héber 4 fejezetes számozást
  használják a Károli 3 fejezetes számozása helyett).
- **Letöltés dátuma:** 2026-09-05 (Genezis/Zsoltárok/Jóel), 2026-09-06
  (a többi 36 könyv és a Sámuel/Királyok-kör).

### Oszlopformátum

```
Igehely | Strong-szám | Görög szóalak | Morfológiai kód | Forrás
```

A `Forrás` oszlop értékei soronként:
- `LXX_WH` — a szó eredetileg is Strong-taggelt volt az LXX_WH oldalon.
- `ABP-pótolt` — a Strong-számot az ABP oldalról pótoltuk, kizárólag
  egyértelmű szövegkörnyezeti egyezés esetén.
- `ELTERO_SZOVEGALAP` — a vers szövegcsalád-eltérés miatt jelzett rése (l. 2.
  szakasz) — nincs pótlás.
- *(üres)* — sem az LXX_WH, sem az ABP nem ad Strong-számot erre a szóra
  (jellemzően valódi tulajdonnév, vagy — l. 2. szakasz — explicit kizárt
  térkép-hivatkozás).

### Licenc-státusz — explicit gap

A studybible.info-n (sem az LXX_WH, sem az ABP verziónál) nem található
explicit copyright- vagy licencnyilatkozat a görög szövegre vagy a
Strong-taggelésre vonatkozóan. **Ez az egész `LXX_kivonat_*.tsv` adatállomány
kizárólag belső munkafolyamat-célú, nem publikus** kimenet, amíg a
licenckérdés nem tisztázódik (pl. a studybible.info üzemeltetőjének
megkeresésével, vagy alternatív, explicit CC-licencű LXX-forrás keresésével).

## 2. Ismert, dokumentált korlátok (minden könyvre érvényes)

- **`ELTERO_SZOVEGALAP`** — az LXX_WH és az ABP nem ugyanazt a szövegcsaládot
  követi (nagyjából Rahlfs/Westcott-Hort vs. Vaticanus-Sixtine hagyomány), ezért
  egy adott versen belül eltérő szórendet/szóhasználatot adhatnak. Ilyenkor a
  szkript **nem választ automatikusan** egyik forrás javára — a vers meglévő
  LXX_WH-adata megmarad, az esetleges rések üresen, külön jelölve maradnak.
- **`konkordancia/Betu_utotag_kizarva.tsv`** — néhány könyvben a
  `LXX_versificacios_terkep.tsv` betű-utótagos al-vers-hivatkozásokat dokumentál
  (pl. `Exo.28:22a` → `2Móz 28:23`), jelezve, hogy egy görög félvers több,
  külön Károli-versre bomlik. Empirikusan ellenőrizve (Exodus, Zsoltárok,
  1 Királyok stb.): **a nyers studybible.info oldal ezeket szónkénti szinten
  nem különbözteti meg** — vagy egyáltalán nincs zárójel, vagy van, de más
  értékre mutat, mint amit a térkép állít. A szavak szétosztása ezért tartalmi
  döntés lenne, nem mechanikus kulcs-egyeztetés — a szkript **explicit
  kizárja** ezeket (nem becsül/oszt szét), és minden kizárt sort naplóz ebbe a
  közös, könyvek között gyülekező riportfájlba (oszlopok: `Karoli_konyv_prefix`,
  `Karoli_igehely`, `Oszlop`, `Nyers_ertek`).
- **`konkordancia/Nem_parszolhato_terkep_ertekek.tsv`** — a fentitől
  megkülönböztetve: azok a `Gorog_LXX_vers`/`Heber_vers` térkép-értékek, amiket
  a feldolgozó regex **egyáltalán nem tud értelmezni** (pl. `"X / Y"` többszörös
  hivatkozás, `"*a-w"` stílusú többbetűs tartomány, vesszős/pontosvesszős
  listák, ismert korrupt duplikált könyv-prefixek). Ezek is explicit
  naplózódnak (ugyanolyan oszlopokkal), nem tűnnek el csendben. A puszta `"--"`
  végű értékek (explicit "nincs LXX-megfelelő" dokumentáció) **nem** kerülnek
  ebbe a fájlba, mert azok szándékos jelölések, nem hibák.
- **Apokrif toldalékok (Eszter, Dániel)** — a protestáns Károli-kánon nem
  tartalmazza a görög deuterokanonikus toldalékokat (Eszter 11-16, Zsuzsanna,
  Bél és a sárkány, Azarjás imája stb.). A `LXX_versificacios_terkep.tsv` ezekre
  nem ad valódi, létező Károli-célt — a szkript ellenőrzi minden térkép-sor
  célját a `Karoli_1908.tsv` ellenében, és ha az nem létezik, a sort kizárja
  (nem fabrikál hamis Igehely-címkét).
- **1 Sámuel, 2 Sámuel, 1 Királyok, 2 Királyok** könyvnevek a studybible.info
  oldalon a szokásos angol elnevezéssel érhetők el (`1 Samuel`, `1 Kings` stb.)
  — a Septuaginta saját, eltolt "Βασιλειῶν I-IV" könyvhatár-konvenciója nem
  okoz gyakorlati problémát, mert a forrásoldal ezt már feloldva, a megszokott
  könyvhatárok szerint szolgáltatja.
- **Számmal kezdődő könyvrövidítések (1Ch, 2Ch, 1Sa, 2Sa, 1Ki, 2Ki)** — a
  térkép feldolgozó regexe eredetileg csak betűkkel kezdődő rövidítéseket
  ismert fel, ezért ezek a STEP-rövidítések soha nem illeszkedtek — ez a hiba
  javítva. Amíg élt, gyakorlati hatása csak ott volt, ahol a könyv **saját**
  rövidítése is számmal kezdődik (1 és 2 Krónika, l. 4. szakasz) — a Sámuel/
  Királyok könyveknél a rájuk mutató (más könyvekből eredő) kereszthivatkozások
  vesztek volna el csendben, ha a javítás nem előzi meg a feldolgozásukat.

## 3. Összesített lefedettségi táblázat (mind a 39 könyv)

Ez a hivatalos, egy helyen karbantartott forrás — nem kell könyvenként
keresgélni.

| Könyv | Sor | LXX_WH | ABP-pót | ELTÉRŐ | Üres | Lefed.% |
|---|---|---|---|---|---|---|
| Genezis | 32565 | 29727 | 1075 | 1559 | 204 | 94.6% |
| Exodus | 24422 | 22057 | 1050 | 1030 | 285 | 94.6% |
| Leviticus | 19082 | 17564 | 661 | 572 | 285 | 95.5% |
| Numeri | 25046 | 22106 | 1179 | 1376 | 385 | 93.0% |
| Deuteronomium | 22990 | 21536 | 535 | 757 | 162 | 96.0% |
| Józsué | 14436 | 12556 | 687 | 989 | 204 | 91.7% |
| Bírák | 15947 | 14176 | 598 | 995 | 178 | 92.6% |
| Ruth | 2072 | 1805 | 91 | 155 | 21 | 91.5% |
| 1 Sámuel | 20094 | 18040 | 651 | 1243 | 160 | 93.0% |
| 2 Sámuel | 17914 | 15608 | 724 | 1366 | 216 | 91.2% |
| 1 Királyok | 18736 | 16714 | 632 | 1176 | 214 | 92.6% |
| 2 Királyok | 18781 | 16735 | 622 | 1214 | 210 | 92.4% |
| 1 Krónika | 16235 | 13214 | 1193 | 1331 | 497 | 88.7% |
| 2 Krónika | 21037 | 19175 | 667 | 908 | 287 | 94.3% |
| Ezsdrás | 5586 | 4830 | 317 | 367 | 72 | 92.1% |
| Nehémiás | 7676 | 6748 | 391 | 380 | 157 | 93.0% |
| Eszter | 3757 | 3258 | 208 | 242 | 49 | 92.3% |
| Jób | 13291 | 12038 | 525 | 696 | 32 | 94.5% |
| Zsoltárok | 34848 | 32575 | 987 | 1178 | 108 | 96.3% |
| Példabeszédek | 8909 | 8100 | 423 | 370 | 16 | 95.7% |
| Prédikátor | 4546 | 4305 | 122 | 95 | 24 | 97.4% |
| Énekek éneke | 2004 | 1758 | 88 | 155 | 3 | 92.1% |
| Ézsaiás | 27037 | 25214 | 796 | 883 | 144 | 96.2% |
| Jeremiás | 28408 | 26235 | 788 | 1205 | 180 | 95.1% |
| Siralmak | 2349 | 2164 | 84 | 99 | 2 | 95.7% |
| Ezékiel | 29658 | 27346 | 1029 | 984 | 299 | 95.7% |
| Dániel | 9357 | 8609 | 282 | 354 | 112 | 95.0% |
| Hóseás | 3859 | 3565 | 77 | 205 | 12 | 94.4% |
| Jóel | 1580 | 1469 | 56 | 39 | 16 | 96.5% |
| Ámós | 3210 | 2924 | 112 | 146 | 28 | 94.6% |
| Abdiás | 472 | 438 | 7 | 22 | 5 | 94.3% |
| Jónás | 1069 | 988 | 37 | 39 | 5 | 95.9% |
| Mikeás | 2368 | 2160 | 80 | 113 | 15 | 94.6% |
| Náhum | 937 | 832 | 49 | 52 | 4 | 94.0% |
| Habakuk | 1105 | 1020 | 33 | 51 | 1 | 95.3% |
| Sofóniás | 1223 | 1118 | 40 | 51 | 14 | 94.7% |
| Aggeus | 947 | 874 | 24 | 31 | 18 | 94.8% |
| Zakariás | 4963 | 4596 | 173 | 165 | 29 | 96.1% |
| Malakiás | 1416 | 1341 | 34 | 39 | 2 | 97.1% |
| **ÖSSZESEN (39 könyv)** | **469932** | **425518** | **17127** | **22632** | **4655** | **94.2%** |

*Lefedettség = (LXX_WH + ABP-pótolt) / összes sor.*

## 4. Könyv-specifikus egyedi megjegyzések

Csak azoknál a könyveknél, ahol van valódi, önálló magyarázatot igénylő
jelenség.

- **Genezis** — 31:55–32:32 (és kisebb mértékben 5:32/6:1) fejezethatár-
  eltolódás: a studybible.info nyers oldal-helyi vers-számozása ezen a
  szakaszon nem egyezik a Károlival (amit a nyers oldal "32:1"-nek jelöl, az
  valójában Károli 31:55, és a további versek is +1 eltolással követik). Ez a
  `--versifikacios-terkep` opcióval helyesen fel van oldva — ez az esemény
  vezetett a `load_versifikacios_terkep()` egyik korábbi hibájának
  felfedezéséhez és javításához (a trivális Gorog/Heber-önhivatkozások téves
  indexelése).
- **Zsoltárok** — Zsolt 37:1 és Zsolt 54:1 vers-összevonás: ezek a versek a
  Károliban egy versbe olvasztják össze a görög/héber hagyomány külön (cím-
  felirat + tartalom) számozott LXX-verseit; ezen bukkant fel és lett javítva
  a fenti önhivatkozási hiba. Emellett a Zsolt 150:6 korábban tévesen elnyelte
  a rákövetkező, apokrif 151. zsoltár teljes szövegét (egy zárójel-kezelési
  hiba miatt) — ez javítva, a 151. zsoltár helyesen kimarad. Néhány, betűvel
  megkülönböztetett fél-vers határánál (pl. Zsolt 13:5/13:6) a pontos
  elválasztás nem rekonstruálható, a tartalom az egyik oldalra kerül, a másik
  üresen marad.
- **1 Krónika** — a legalacsonyabb lefedettség (88,7%) a 39 könyv között: sok
  genealógiai tulajdonnév (nemzetségtáblázatok), amit egyik forrás sem taggel
  Strong-számmal. (A 2. szakaszban leírt, számmal kezdődő könyvrövidítések
  hibája ezt a könyvet és a 2 Krónikát érintette a legérzékenyebben — mindkettő
  újragenerálva a javítás után.)
- **Jób** — a 42:17 utáni nagy LXX-toldalék (Jób családfája és feltámadása)
  a héber szövegben nincs benne, ezért ott magas az `ELTERO_SZOVEGALAP` arány.
- **Jeremiás** — mintegy 100 vers hiányzik: ez jól dokumentált LXX/maszoretai
  szöveg-rövidülés (a görög Jeremiás kb. 1/8-dal rövidebb a héber szövegnél) és
  a nemzetek elleni jövendölések LXX-beli átrendezése miatt van így — nem hiba,
  hanem a forrásszöveg valódi jellemzője.
- **Eszter, Dániel** — a görög apokrif toldalékok (Eszter 11-16, Zsuzsanna,
  Bél és a sárkány, Azarjás imája) helyesen kizárva, nem fabrikálnak nem
  létező Károli-verscímkét.
- **1 Királyok** — 44 térkép-sor explicit kizárva a
  `Nem_parszolhato_terkep_ertekek.tsv`-n keresztül: ezek a Jeroboám
  királyságáról szóló elbeszélés LXX-beli, a maszoretai szövegtől jelentősen
  eltérő sorrendű, szétszórt, összetett kereszthivatkozásokkal (pl.
  `"1Ki.12:24*a-w [=11:19, 21-22, 24, 26-28, ...]"`) dokumentált változatát
  jelentik — nem próbáltuk rekonstruálni/szétosztani a szavakat.
- **Hóseás, Ézsaiás** — néhány vers (pl. Hós 11:12/13:16/2:23, Ézs 9:21/64:12)
  a Károlinál nem létező LXX-többlet miatt helyesen üres marad.
