# DT54 — a #22 könyvsorrendje a #38 adatblokkja szerint: Zsoltárok a Bírák előtt?

*2026-10-07 · kérdés a #22-höz (KAROLI_STRONG), a #38 (BDB_FORDITAS) és a #56 (BDB_ADATBLOKK) mérése alapján · mérő szkript: `naplok/F22_konyvsorrend_meres.py`*

## 1. A kérdés

A #22 következő könyve a Bírák (felhasználói döntés, 2026-10-05). A #38 adatblokkjának Károli-szakasza ugyanakkor kizárólag a #22 kész könyveiből él (`adat/karoli_strong/parok_*.tsv`: 1–5Móz, Józs). A BDB gyakorisági sorrendjében előrehaladva a szócikkek egyre inkább a költői, prófétai és arámi szövegekben állnak, ahol nincs Károli-pár. Kérdés: maradjon-e a kanonikus sorrend (Bírák), vagy a Zsoltárok (illetve egy nyereség szerinti sorrend) kerüljön előre?

## 2. Mérés

Proveniencia: `scope=BDB_FORDITAS_sorrend.tsv; lefedett: 1Móz, 2Móz, 3Móz, 4Móz, 5Móz, Józs | forras=eszkozok/bdb_adatblokk.py (adat/karoli_strong/parok_*.tsv + konkordancia/TAHOT_kivonat.tsv) | ts=2026-10-07T05:58:31Z`

Kategória szócikkenként: **van** = legalább 5 Károli-pár; **kevés** = 1–4 pár; **NINCS** = a blokkban `[NINCS KÁROLI-ALAK]`.

| szakasz | szócikk | van | kevés | NINCS | TAHOT-előfordulás a lefedett könyvekben |
|---|---|---|---|---|---|
| 6. adag (407–648, kész) | 242 | 77,3% | 11,2% | 11,6% | 28,7% |
| 7. adag (649–969, következő) | 321 | 63,6% | 22,7% | 13,7% | 25,6% |
| hátralévő sor (649–) | 7 416 | 12,5% | 27,9% | **59,5%** | 24,3% |

**Nyereség könyvenként:** a NINCS/kevés szócikkek TAHOT-előfordulásai az adott könyvben (zárójelben: hány NINCS-szócikk fordul elő benne).

| könyv | Károli-vers | 6. adag | 7. adag | hátralévő sor | hátralévő / 100 vers |
|---|---|---|---|---|---|
| **Zsolt** | 2 527 | **639** (7) | **741** (18) | **3 172** (669) | 126 |
| Ézs | 1 290 | 290 (3) | 536 (21) | 3 129 (856) | 243 |
| 1Krón | 942 | — | 292 (29) | 2 292 (732) | 243 |
| Jer | 1 364 | 317 (13) | 417 (20) | 2 272 (522) | 167 |
| Ez | 1 273 | 107 | 340 (12) | 2 093 (452) | 164 |
| Dán | 357 | 476 (11) | — | 2 022 (475) | 566 |
| Jób | 1 068 | 184 (2) | 191 (11) | 1 623 (494) | 152 |
| Péld | 914 | 170 (4) | 250 (11) | 1 555 (365) | 170 |
| **Bír** | 618 | **48** (1) | **187** (6) | **1 029** (205) | 167 |

*A „—” azt jelzi, hogy a könyv nincs az adott szakasz első 12 könyve között. A versszám a `naplok/F22_versbeosztas.md` 1. táblájából való. A NINCS-szócikkek darabszáma könyvek között átfed, ezért nem összeadható.*

A 6. adag 28 NINCS-szócikke a `Strong_szotar.tsv` szófaja és az előfordulások eloszlása szerint: 13 személynév, 7 arámi szó (csak Dán/Ezsd, legfeljebb egy Jer-hely), 8 héber szókincselem (H1964, H8605, H4210, H5542, H5329, H1077, H3684, H3064). A 8-ból 5 főleg a Zsoltárokban áll.

## 3. Mit mutat a mérés

1. **A Zsoltárok adja a legnagyobb abszolút nyereséget** mindhárom szakaszban, a közvetlenül következő 7. adagban is (741 előfordulás, a Bírák 187-tel szemben).
2. **Költségarányosan nem a Zsoltárok a legjobb.** A hátralévő sorban az Ézsaiás ugyanannyit hoz (3 129 vs. 3 172) feleannyi versből, és több NINCS-szócikket fed le (856 vs. 669). Az 1Krón hasonló arányú, de nyereségének jelentős része névlista (nemzetségtáblák; ezt nem mértem külön).
3. **A Dániel a leghatékonyabb (566/100 vers), de főleg arámi.** Nincs mérve, hogy a #22 promptja (`f21p/prompt_v3.md`) és kapuja az arámi szakaszon ugyanúgy működik-e.
4. **A Bírák a 6–7. adaghoz alig ad** (48, illetve 187). A teljes sorhoz közepesen ad: vershatékonysága (167) a Jeremiáséval egyezik.

## 4. Kockázatok és költség

- **Költség.** A Józs 658 verse a heti keretből 4 százalékpontot vitt (`naplok/F22_Jozs_jelentes.md`). Lineáris vetítéssel a Zsolt kb. 15, az Ézs kb. 8, a Bír kb. 4 pont. Ez becslés, nem mérés.
- **Versbeosztás.** A Zsoltárokban a Károli és az eredeti versszám egyezik (2 527 = 2 527, 0 eltolt pár), de 27 fejezet jelzett (főleg `GYENGE` korreláció). A brief szerinti kézi jóváhagyás (`tokenek.VERSBEOSZTAS_JOVAHAGYOTT`) itt nagyobb munka, mint a Bírák 0 jelzett fejezeténél. Az Ézsaiásban 4 jelzett fejezet és 28 eltolt pár van.
- **TAHOT-hiány.** A `CLAUDE.md` szerint a `TAHOT_kivonat.tsv`-ből hiányzik a Zsolt 88, 89, 140 és 142. Ezekre a versekre nincs eredeti oldal, `kezi` vagy kimaradás lesz.
- **Műfaj.** A #22 eddig csak prózát (ÓSZ-próza réteg) párosított. A költészet pontossága a #22-ben nincs mérve; a pilot rétegbesorolása (`naplok/F21P_jelentes.md`, DT-F21j h) külön rétegnek veszi. Az első költői könyvnél szúrópróba vagy zárt összevetés ajánlott.
- **A javító menet.** Bármelyik könyv a már kész adagokat csak a #38 javító menetében javítja. A 7. és a további adagokat viszont azonnal, ha a könyv előbb kész, mint az adag.

## 5. Opciók

- **(a)** Marad a kanonikus sorrend: a Bírák következik (a 2026-10-05-i döntés).
- **(b)** A Zsoltárok előre, utána a kanonikus sorrend (Bír, …).
- **(c)** Nyereség szerinti sorrend a #38 adatblokkjához. Hatékonyság szerint: Ézs → Zsolt → Jer → Ez → Jób → Péld, a történeti könyvek (Bír–Krón) utána. A Dán az arámi-próba után.
- **(d)** Mint (b) vagy (c), de a #38 7. adagja addig vár, amíg az első előrehozott könyv elkészül. Ellenkező esetben a 7. adag a mostani hat könyvvel fut, és a javító menet pótolja.

## 6. Javaslat

**(b), a 7. adag nem vár.** Indoklás:
- a Zsoltárok a közvetlenül következő 7. adagban is a legtöbbet adja;
- a 6. adag hiányzó valódi szókincsének (H1964, H8605, H4210, H5542, H5329) nagy része zsoltári;
- a nagyobb költség és a 27 jelzett fejezet egyszeri teher.

A (c) a teljes sorra hatékonyabb (Ézs előre). Ha a keret szűk, az Ézs-sel kezdés a jobb választás. A (d)-t nem javaslom, mert a #38 javító menete úgyis lefut.

Az első költői könyv előtt kell egy rövid pontossági szúrópróba (a #22 brief ⛔ 2. megállójának mintájára).

## 7. Döntés

**Felhasználó, 2026-10-07 (chat): (b), a 7. adag nem vár.** A #22 következő könyve a Zsoltárok, utána a kanonikus sorrend (Bír, Ruth, …). A #38 7. adagja nem vár; a Zsoltárok Károli-adatát a 7. adag a #38 javító menetében kapja meg. Alkalmazva az F22 briefben (D13, v2.7, `kovetkezo`).
