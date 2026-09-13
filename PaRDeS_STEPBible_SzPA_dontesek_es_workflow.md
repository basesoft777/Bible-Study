# PaRDeS-projekt: STEPBible/SzPA integráció és GitHub-architektúra — döntési összefoglaló (v36)

*Teljes változástörténet (v15–v36): `PaRDeS_dontesek_CHANGELOG.md` (kiszervezve F0.6, 2026.09.13).*

*Ez a fájl híd a claude.ai memóriarendszerében felhalmozott kontextus és a Claude Code / bármely jövőbeli munkamenet között. Célja, hogy egy új munkamenet — akár claude.ai chatben, akár Claude Code-ban — enélkül a beszélgetés-történet nélkül is teljes képet kapjon a meghozott döntésekről és azok indoklásáról. A `Rendszerfejlesztesi_playbook.md` a projekt saját, ismétlődően bevált fejlesztési MUNKAMÓDSZERÉT dokumentálja, ez a fájl pedig a TARTALMI DÖNTÉSEKET — a kettő együtt adja a teljes képet.*

---

## 0. Dataset-leltár — gyors áttekintés

*Ez a szakasz csak összegzés; a részletes indoklás és a technikai formátum a lenti szakaszokban található (lásd a hivatkozott pontokat).*

| # | Dataset | Tartalom | Hely | Státusz | Forrás | Részletek |
|---|---|---|---|---|---|---|
| 1 | **TAGNT/TAHOT kivonat** | 8 oszlop: igehely, Strong, alak, kiejtés, szótő, szótári jelentés, angol gloss, kritikai kiadás | Publikus repó | Letöltve, generálva (teljes ÓSZ+ÚSZ) | STEPBible-Data (CC BY) | 2. szakasz |
| 2 | **Karoli_1908.tsv** | Igehely + teljes Károli-vers | Publikus repó | Letöltve, generálva (teljes Biblia, 31 170 vers) | scrollmapper/HunKar (közkincs) | 4.1, 4.7 |
| 3 | **SzPA versek + lábjegyzetek** | 2 tábla könyvenként (Példabeszédek, ApCsel) | Privát repó | Minta kész (1:1-9, 1:1-4), teljes könyv még nem (felfüggesztve) | Saját feltöltés (jogosult tulajdon) | 3. szakasz |
| 4 | **Összekapcsolt (join) tábla — Károli-Strong** | Igehely + Strong + Károli-szó + azonosítás módja + forrás-tanulmány + megbízhatóság + szófaj + gyök/származtatás (8 oszlop) | Publikus repó | Betöltve (212 sor, Gen.1-16 + 34 újabb, motívumnapló v47 alapján — ld. v30/v32/v35 changelog); a szófaj+gyök oszlopok a `Strong_szotar.tsv`-ből összefésülve | Az 1. és 2. összefésülése + `Strong_szotar.tsv` | 4.1-4.2, 4.13 |
| 5 | **KJV-Strongs** | Híd-forrás, Példabeszédek (31 fej.) + 1Mózes (50 fej.) + 2Mózes (40 fej.), szavankénti bontásban tárolva | Publikus repó | Letöltve, validálva (Példabeszédek + 1Mózes + 2Mózes) | biblehub.com/kjvs, studybible.info/KJV_Strongs (közkincs) | 4.8 |
| 6 | **ASV-Strongs** | Második híd-forrás, Példabeszédek (31 fej.) + 1Mózes (50 fej.) + 2Mózes (40 fej.), kereszt-ellenőrzésre | Publikus repó | Letöltve, validálva (Példabeszédek + 1Mózes + 2Mózes) | studybible.info/ASV_Strongs (közkincs) | 4.9 |
| 7 | **byztxt szövegkritikai variánsok** | Tényleges eltérő szövegváltozatok (nem csak "van/nincs") | Publikus repó | Azonosítva, beépítésre vár | byztxt/byzantine-majority-text (Unlicense) | 4.6 |
| 8 | **Károli-specifikus kereszthivatkozások** | Versenkénti hivatkozás-lista, szentiras.hu eredetű | Publikus repó | Letöltve, generálva (teljes Biblia, 32 407 sor) | krisek/HunKar (SWORD OSIS, közkincs) | 4.6 |
| 9 | **TSK (Treasury of Scripture Knowledge) kereszthivatkozások** | Versenkénti, szavazat-súlyozott hivatkozás-jelöltek, kiegészítő szerepű | Publikus repó | Letöltve, generálva (432 949 sor, TSK/OpenBible.info alapú, scrollmapper GitHub-tükörről, votes-súlyozva, 0 nem-illeszthető sor) | scrollmapper/bible_databases (MIT) | `TSK_kereszthivatkozasok_README.md` |
| 10 | **TIPNR névelőfordulások** | Tulajdonnév-alakváltozatok (pl. Ábrám/Ábrahám) | Publikus repó | Letöltve, generálva (teljes Biblia, 35 522 sor) | STEPBible-Data (CC BY) | 8. szakasz |
| 11 | **Könyv-rövidítés normalizáló tábla** | STEPBible angol ↔ magyar igehely-formátum | Publikus repó | Elkészült (mind a 66 könyv) | STEPBible README | 8. szakasz |
| 12 | **Strong-szótár (deduplikált, 6 oszlopos)** | Strong-szám + szótő + kiejtés + szófaj + gyök/származtatás + jelentés, egyedi soronként | Publikus repó | Elkészült (teljes Biblia, 14 347 egyedi Strong-szám: 8718 héber + 5629 görög) | TAHOT/TAGNT-kivonat + openscriptures/HebrewLexicon + openscriptures/GreekResources összefésülése | ld. v31 changelog, `Strong_szotar_README.md` |
| 13 | **LXX versificációs térkép** | TVTMS Expanded-alapú Renumber/Concatenation eltérések (LXX vs. maszoréta/Károli), Károli-illesztéssel | Publikus repó | Fázis 0-2 kész (5426 sor); Fázis 3 tudatosan elnapolva | STEPBible-Data TVTMS (CC BY) | ld. v36 changelog |

**Kiegészítő, "meta" jellegű dokumentum (nem dataset):**
`Rendszerfejlesztesi_playbook.md` — a projekt saját, ismétlődően bevált fejlesztési módszerének kivonata (kontextus-beolvasás → forrás/licenc-ellenőrzés → mintavalidáció → teljes feldolgozás explicit megállási szabállyal → naplózás → leltár-frissítés). Új rendszerfejlesztési kérés esetén EZT a fájlt is érdemes elolvasni a döntési fájl mellett — gyorsabb tájékozódást ad, mint a teljes verziótörténet végigolvasása.

**Nem önálló dataset, csak referencia-eszköz** (nem kerül tárolásra nyers adatként):
- TBESH/TBESG/TFLSJ lexikonok — csak átfogalmazva idézhetők
- Biblia-Felfedező — kizárólag kézi ellenőrzésre (4.7-es döntés)
- TAGOT, TBCWG — jövőbeli, még nem elérhető STEPBible-fejlesztések

---

## 1. Architekturális váltás: GitHub mint elsődleges forrás

**Döntés:** a `project_knowledge_search` (Claude Projects szemantikus keresés) helyett a **GitHub-repó** (`basesoft777/Bible-Study`) grep-alapú keresése lesz az elsődleges módszer, minden munkamenet elején repó-klónozással/pull-lal.

**Fontos, gyakorlati megjegyzés:** a repó időközben átköltözött **kisbetűs** `basesoft777/Bible-Study` névre (korábban `Basesoft777/Bible-Study`) — a régi URL jelenleg még átirányít, de érdemes az új, kisbetűs formát használni jövőbeli klónozásnál/hivatkozásnál, nehogy az átirányítás egyszer megszűnjön.

**Indoklás:**
- A `project_knowledge_search` eddig is csak azokra a fájlokra terjedt ki, amiket ténylegesen visszatöltöttünk a Claude Projects-be — ez már eddig is következetlen volt (nem minden tanulmány került vissza)
- A motívumlog (`PaRDeS_motivumok.md`) **teljes fájlként beolvasva** jobb eredményt ad, mint egy szemantikus top-N töredék-keresés — a teljes napló-kontextus értelmezhető, összefüggések felismerhetők
- A grep **kiszámítható**: pontosan tudható, mi van a repóban és mi nem
- **Korlát, amit tudni kell:** egy adott tanulmány *mélyebb tartalmára* (konkrét érvelés, nevesített tanító pontos szövege) a motívumlog önmagában nem ad választ — ehhez a teljes tanulmányfájl szükséges, ami viszont szintén a repóban van, tehát elérhető, csak explicit meg kell nyitni.

**Gyakorlati következmény:** a Claude Projects-feltöltés gyakorlata megszűnhet/opcionálissá válhat; a GitHub lesz az egyetlen "igazságforrás".

---

## 2. STEPBible-integráció (nyilvános adat, nyilvános repó-rész)

**Mi:** STEPBible-Data (Tyndale House, Cambridge), CC BY licenc, TAGNT (görög ÚSZ) + TAHOT (héber ÓSZ).

**Végleges kivonat-formátum (8 oszlop):**
```
Igehely | Strong-szám | Ragozott alak | Kiejtés | Szótő | Rövid jelentés (szótári) | Angol tükörfordítás (kontextuális) | Kritikai kiadások (csak TAGNT-nál)
```
A 7. oszlop (**új**: kontextuális angol tükörfordítás, pl. "proverbs of", "to teach") **különbözik** a 6. oszloptól (szótári alapjelentés, pl. "proverb", "to teach"): míg a 6. oszlop a szó lexikai alapjelentését adja, a 7. oszlop azt mutatja, **hogyan szerepel a szó ténylegesen ebben a versben, ebben a mondatbeli szerepben** — ez teszi lehetővé a **tartalom-alapú (nem pozíció-alapú) párosítást** a magyar SzPA-szöveggel, mert a magyar és héber szórend gyakran jelentősen eltér (lásd a Péld 1:1-4 kísérletet, ahol a pozíció-alapú interpoláció megbukott, de az angol gloss alapú tartalom-keresés minden szónál sikeres párosítást adott).

A 8. oszlop (mely kiadásokban szerepel a szó: NA28, TR, Byz stb.) teszi lehetővé a szövegkritikai ⚠️ pontok automatikus jelzését — ha egy szó nem szerepel minden kiadásban, az valódi eltérés a Károli/TR-hagyomány és a modern kritikai szöveg között.

**Elhelyezés a repóban:**
```
Bible-Study/
├── konkordancia/
│   ├── TAGNT_kivonat.tsv
│   ├── TAHOT_kivonat.tsv
│   └── README.md (forrás, licenc, generálás dátuma)
```
Ez a rész **nyilvános** maradhat (CC BY engedi).

**Alternatív/kiegészítő források, megvizsgálva:**
- **OSHB/morphhb** (CC BY 4.0) — pontosabb morfológia, de nincs kiejtés/jelentés beépítve → csak másodlagos, finom nyelvtani kérdésekhez
- **byztxt/byzantine-majority-text** (Unlicense, a legtisztább licenc) — teljes bizánci alapszöveg, de a STEPBible TAGNT már jelzi a Byz/TR-jelenlétet is → csak akkor kell, ha a teljes bizánci szöveget kell megjeleníteni

**Sablon-integráció (még nem hajtva végre, de eldöntött terv):**
- **Tematikus sablon (4.):** kötelező STEPBible-ellenőrzés az 1. pontban (előfordulás-gyűjtés) + 11. checklist-pont a lezáráskor, ami dokumentálja, milyen paraméterekkel futott az ellenőrzés
- **Bővített sablon (2.):** 3/b pontban a "célzott konkordancia-ellenőrzés" mostantól STEPBible-alapú, nem csak `web_search`
- **Mélyelemzés sablon (5.):** 2. pontban (nyelvi/filológiai összevetés) kötelező STEPBible-adat beépítése a válaszba

**Visszamenőleges felülvizsgálat (még nem indítva el):** a már lezárt 4 tematikus tanulmány (tehóm, segítségül hívni, Rafeusok, hádész) nem STEPBible-lel készült — érdemes lenne visszamenőleg ellenőrizni őket.

---

## 3. SzPA-fordítások integrációja (védett, privát adat, privát repó-rész)

**Jogi alap:** a Szent Pál Akadémia Példabeszédek- és Apostolok Cselekedetei-fordítása **"Minden jog fenntartva"** védelem alatt áll. A felhasználó **legálisan megvásárolt, kereskedelmi példánnyal** rendelkezik mindkettőből — ez megalapozza a magáncélú másolás/feldolgozás elvét, **privát** (nem nyilvános) repóban tárolva.

**Két-táblás struktúra minden feldolgozott könyvhöz:**

*1. tábla — verses szöveg:*
```
Igehely | SzPA-szöveg (teljes vers)
```

*2. tábla — lábjegyzet-szótár:*
```
Igehely | Lj.# | Magyar kifejezés | Eredeti szó | Kiejtés | Jelentés-árnyalatok
```
(Az ApCsel-nél opcionális 7. oszlop: **Típus** — nyelvi/szómagyarázat vs. kontextuális/történeti megjegyzés, mert itt vegyesebbek a lábjegyzetek, mint a Példabeszédeknél.)

**Forrás-minőség, amit tudni kell:**
- **Példabeszédek** (2006, Grüll Tiborné fordítása, Hack Márta lektorálása): tiszta, jó minőségű digitális szöveg, academia.edu-ról (Eszter Csalog publikációi közt) és a felhasználó saját PDF-jéből is elérhető
- **ApCsel 1-14** (2002, Új Exodus XIII/2, Grüll Tibor és Csalog Eszter fordítása): **korábbi, nem a 2023-as végleges kiadás szövege** — a felhasználó saját PDF-je jobb minőségű, mint az academia.edu-s OCR-es verzió, de még ez is tartalmaz kisebb OCR-hibákat

---

## 4. Az összekapcsolás: STEPBible ↔ SzPA join Strong-szám alapján

**Kiszervezve:** `PaRDeS_STEPBible_SzPA_join_adatcsatorna.md` (F0.7, 2026.09.13) — az SzPA-integráció v23 óta (2026.08.24) felfüggesztett alrendszer, a szakasz teljes tartalma (4.1–4.15+) ott olvasható, változatlanul.

---

## 5. Hozzáférési korlátok — mit lehet elérni honnan

| Felület | Publikus repó (GitHub) | Privát repó (GitHub) |
|---|---|---|
| **claude.ai chat** (ez a rendszer) | ✅ klónozható, olvasható (`bash_tool`, `web_fetch`) | ❌ hitelesítés hiányában nem érhető el, hacsak nincs megadva egy szűk hatókörű PAT |
| **Claude Code** (felhasználó saját gépén) | ✅ | ✅ — a felhasználó már meglévő git-hitelesítésével natívan működik, nincs szükség tokent megosztani |

**Push/írás:** a claude.ai chat **soha nem tud közvetlenül commitolni/push-olni** semmilyen repóba (se publikusba, se privátba) — hiányzik az írási hitelesítés. Ez csak Claude Code-ban lehetséges, a felhasználó saját jogosultságával.

**Claude Code kontextus-korlátja:** Claude Code **nem látja** a claude.ai memóriarendszerét és a korábbi chat-történetet — csak azt, ami ténylegesen a repó fájljaiban van. **Ez a jelen fájl** pontosan ezt a rést hidalja át: minden itt rögzített döntés innentől fájlból, nem csak beszélgetés-emlékezetből érhető el.

---

## 6. Változtatási workflow — hogyan frissül ez a rendszer a jövőben

**Alapelv:** minden érdemi módszertani döntés, ami korábban csak beszélgetésben hangzott el, **ebbe a fájlba (vagy egy utódjába) kerül rögzítésre**, mielőtt Claude Code-alapú munka épülne rá.

### 6.1 Ha egy sablon módosul (pl. STEPBible-lépés tényleges bevezetése)
1. A módosítás **itt, ebben a fájlban** (vagy közvetlenül a sablonfájlban, changelog-fejléccel) kerül rögzítésre
2. A sablonfájl saját verziószáma és changelog-fejléce frissül (a projekt már meglévő konvenciója szerint)
3. Commit-üzenet a `GitHub_feltoltesi_workflow.md`-ben rögzített konvenciót követi: `vXX — [dátum]: [changelog lényege, 1 mondatban]`

### 6.2 Ha új könyv kerül a privát SzPA-adatbázisba
1. **Jogosultság-ellenőrzés először:** van-e legálisan megvásárolt példány a felhasználónál? Ha nincs, a feldolgozás nem indul (vagy engedélykérés a SzPA felé: sb@szpa.hu / jegyzet@szpa.hu)
2. Két tábla elkészítése a megbeszélt formátumban (verses szöveg + lábjegyzet-szótár)
3. Join-tábla elkészítése a megfelelő STEPBible-kivonattal, Strong-szám alapon, a 3. opció (explicit hiányjelzés) szerint
4. Minden új fájl a privát repó megfelelő mappájába kerül, **soha nem a nyilvánosba**

### 6.3 Ha egy már lezárt tematikus tanulmányt visszamenőleg STEPBible-lel ellenőrzünk
1. Az adott motívum Strong-számainak azonosítása
2. Teljes körű, versen belüli és szomszédos-verses egyezés-keresés a TAGNT/TAHOT-on
3. Új találatok esetén: explicit értékelés (valódi lexikai egyezés vs. csak felszíni Strong-egyezés eltérő referenssel — lásd a pneuma/pszükhé-eset Mat 12:18/1Pét 1:22 kizárását mintaként)
4. Ha új előfordulás igazolódik: a tematikus sablon 10 pontos lezárási checklistje **újra végigfuttatva** (nem csak a napló egy sorát módosítva)
5. A tanulmány saját changelog-fejléce és a napló fejléc-changelogja is frissül

### 6.4 Verziókövetés elve mindenhol
- Fájlnév-verziószám **csak explicit felhasználói kérésre** emelkedik (motívumlog-konvenció, ami minden fájlra kiterjeszthető)
- Changelog-fejléc **minden érdemi tartalmi változásnál** frissül, még ha a fájlnév-verzió nem is
- Rule-konfliktus esetén (két korábbi döntés összeütközik) — explicit rákérdezés, nem önkényes döntés (ez már korábban is rögzített projektelv)

### 6.5 Új munkamenet indításakor (akár claude.ai, akár Claude Code)
Javasolt első lépés: **ennek a fájlnak a beolvasása** a repóból, mielőtt bármilyen tanulmány- vagy sablon-munka elindul — ez biztosítja, hogy a munkamenet ne a nulláról induljon, és ne ismételje meg a már meghozott döntéseket vagy azok mérlegelését.

---

## 7. Tanulmány-készítési munkafolyamat a GitHub-alapú tudásbázissal

**Fontos megkülönböztetés:** ez a szakasz **nem a sablonok szövegét** módosítja (azt lásd külön: `Sablon_modositasok_es_motivumlog_valtozasok.md`), hanem azt írja le, **hogyan változik magának egy sablon alapján készülő tanulmány elkészítésének gyakorlata**, most hogy a teljes projekt-tudásbázis (motívumlog, sablonok, korábbi tanulmányok, tanítói lista, gyorsreferencia) egységesen, kereshetően elérhető a GitHub-repóból, nem csak beszélgetés-kontextusból vagy memóriából.

**A lényegi különbség egy szóban: verifikáció.** Eddig a sablonok által előírt "belső önellenőrzés" **deklaratív** volt (állítás, hogy megtörtént, memóriára/kontextusra támaszkodva). Mostantól **tényleges, grep-alapú ellenőrzéssé** válhat, mert minden korábbi anyag egy helyen, kereshető formában áll rendelkezésre.

**Melyik sablon-pont hogyan verifikálódik ténylegesen a repóból:**

| Sablon-pont | Korábbi gyakorlat | Új gyakorlat (repó-alapú) |
|---|---|---|
| 0. Sorozat-kontextus | kontextusból/memóriából rekonstruált | `grep` a "Feldolgozott igeszakaszok" táblán |
| 2. Eredeti nyelvi tábla | emlékezetből + esetenkénti `web_search` | STEPBible-lekérdezés közvetlenül a repóból (+ SzPA-adat, ha releváns könyv és van hozzá privát adat, Strong-szám alapú összekapcsolással) |
| 3/b. Ismétlődő motívum ellenőrzése | "eszembe jutott-e" a korábbi előfordulás | `grep` a teljes motívumlogon és korábbi tanulmányfájlokon a releváns kulcsszóra, *mielőtt* a kereszthivatkozás megfogalmazódik |
| 5. Alkalmazás (named teacher) | a jóváhagyott lista emlékezetből reprodukálva | `PaRDeS_tanitok_lista.md` közvetlen olvasása a repóból |
| Terminológiai/formai szabályok | emlékezetből betartva | `PaRDeS_gyorsreferencia.md` és a sablon saját szövege ellenőrzésként újraolvasva véglegesítés előtt |
| Napló-frissítés (7 szekció) | feltételezés alapján, mely szekció érintett | `grep`-pel ellenőrizve, ténylegesen mely szekciók tartalmaznak releváns bejegyzést |

**Gyakorlati sorrend egy új tanulmány elkészítésekor:**
1. Repó-frissítés (klónozás vagy `git pull`) a munkamenet elején
2. 0. pont: grep a "Feldolgozott igeszakaszok" táblán
3. 2. pont: STEPBible-lekérdezés (+ SzPA, ha releváns) a szakasz kulcsszavaira
4. 3/b pont: grep a motívumlogon és korábbi tanulmányokon a lehetséges ismétlődő motívumokra
5. 5. pont: grep a jóváhagyott tanítói listán, ha nevesített forrás kell
6. Belső önellenőrzés: a terminológiai szabályok tényleges újraolvasása/ellenőrzése
7. Napló-frissítés: grep-pel ellenőrizve, mely szekciók valóban érintettek, mielőtt a frissítés megtörténik

**Amit ez nem vált ki:** a tartalmi, teológiai munkát (Peshat/Remez/Drash/Sod kidolgozása, named teacher-anyag valódi keresése és értékelése, ⚠️ vitatott pontok névvel jelölt képviselőinek azonosítása) — ezek továbbra is minden egyes tanulmánynál újra elvégzendő, tartalmi munkát igénylő lépések, amiket a repó-alapú verifikáció csak **megalapoz és ellenőriz**, nem helyettesít.

### 7.1 A bővített sablon 2. pontjának kulcsszó-kiválasztási kritériumai

A max. 6-8 szó/vers kiválasztása eddig kimondatlan, csak gyakorlatban alkalmazott szempontok szerint történt. Explicit kritériumlista (legalább egynek teljesülnie kell):
1. **Teológiai súly** — a szó jelentése önmagában állítást hordoz, ami a Peshat-értelmezést érdemben alakítja
2. **Elmosódás a Károli/SzPA fordításban** — két vagy több eredeti szó egyetlen magyar szóvá olvad össze
3. **Motívum-kapcsolódás** — a szó egy már nyomon követett motívumhoz köthető
4. **Kereszthivatkozási potenciál** — a szó ritka, erős 3/b kapcsolódást tehet lehetővé
5. **Exegetikai vita forrása** — a szó jelentése önmagában ad okot egy ⚠️ vitatott pontra
6. **Objektív ritkaság (STEPBible-adat alapján), szófajjal súlyozva.** Ha a szó előfordulás-száma alacsony (tájékoztató küszöb: kevesebb mint 15-20 előfordulás a teljes ÓSZ/ÚSZ-ben), ez önmagában felveti a kiválasztás lehetőségét. A Strong_szotar.tsv szófaj-mezője (most már elérhető) finomíthatja ezt a mérlegelést: egy ritka IGE gyakran nagyobb teológiai súlyt hordoz, mint egy hasonlóan ritka, de leíró jellegű melléknév vagy határozószó — ez nem szigorú szabály, csak további szempont a tartalmi mérlegeléshez, nem helyettesíti azt.

*(A pontos, beillesztendő sablon-szöveg: lásd `Sablon_modositasok_es_motivumlog_valtozasok.md`, 1.1/A pont.)*

**Tanulmányvezérelt, kumulatív generálás — hol jelentkezik a célzottság a bővítettnél:** a szűkítés **a keresés előtt**, magánál a kulcsszó-kiválasztásnál történik (a fenti 6-pontos lista alapján), nem utólag.
```
1. Kulcsszó-lista összeállítása a kritériumlista alapján (max 6-8 szó/vers)
2. Minden kiválasztott szónál: ELLENŐRZÉS — van-e már rá sor az
   osszekapcsolt.tsv-ben (grep igehely/Strong-szám szerint)?

   → HA VAN: kész, azonnal felhasználható, nulla plusz költség
   → HA NINCS:
     a) STEPBible-sor lekérése (grep TAGNT/TAHOT) — olcsó, gépi
     b) SzPA-lábjegyzet keresése, ha releváns könyv (grep) — olcsó, gépi
     c) CSAK HA a szónak nincs SzPA-lábjegyzete, DE a tanulmány mégis
        hivatkozna rá magyar szóként → tartalom-alapú (angol gloss)
        azonosítás — ez az egyetlen "drága" lépés, és csak 1-2 szót érint
3. Az újonnan generált sorok VISSZAÍRÁSA (append) az osszekapcsolt.tsv-be
4. A tanulmány 2. pontja ebből az adatból épül fel
```
**A gyakorlati tapasztalat:** egy átlagos bővített tanulmánynál a 10-20 kiválasztott kulcsszóból jellemzően csak **1-3 szükségel** ténylegesen tartalom-alapú azonosítást — a többi vagy lábjegyzet-alapú (ha van SzPA-adat), vagy egyszerűen nem is igényel magyar szó-azonosítást (a Strong-adat és a szótő önmagában is elég a Peshat-elemzéshez).

### 7.2 Tematikus sablonra épülő tanulmányok — eltérő munkafolyamat

A tematikus sablon **szerkezetileg más léptékű** feladat, mint a bővített: nem egy szakasz kulcsszavainak kiválasztásáról van szó, hanem arról, hogy **a teljes kánonban** megtaláljuk egy motívum összes előfordulását.

**Miért más a token-gazdaságossági profil:**
- **A keresési lépés maga olcsó, gépi feladat** — `grep` a teljes TAGNT/TAHOT-on egy-két Strong-számra pillanatok alatt lefut (lásd a pneuma/pszükhé-ellenőrzés precedensét)
- **A találati lista értékelése** (valódi lexikai egyezés vs. felszíni Strong-egyezés eltérő referenssel, mint a Mat 12:18/1Pét 1:22 kizárása) igényel tartalmi mérlegelést, de ez jellemzően **néhány, legfeljebb egy-két tucat jelöltre** korlátozódik — hasonló nagyságrendű munka, mint egy bővített tanulmány kulcsszó-elemzése, nem egy teljes könyv minden szava

**Az SzPA-integráció itt eltérő korlátba ütközik:** egy motívum előfordulásai jellemzően **sok különböző könyvet** érintenek (a pneuma/pszükhé-motívum pl. 1Móz, 1Thessz, Zsid, 1Kor, Luk, Fil, Mt, 1Pét helyeket is érint), miközben a privát SzPA-adatbázis **jelenleg csak két könyvet** fed le (Példabeszédek, ApCsel 1-14). Ez azt jelenti, hogy egy tematikus tanulmány találatainak **túlnyomó része** nem fog SzPA-adattal rendelkezni — a "nincs SzPA-lábjegyzet, csak STEPBible-adat" eset itt **tipikus**, nem kivételes, amíg a privát adatbázis nem bővül.

**Konkrét workflow tematikus tanulmánynál:**
```
1. Motívum kulcsszavának Strong-száma azonosítva (motívumlog vagy felhasználói megadás alapján)
2. Teljes körű grep TAGNT/TAHOT-on (mindkettőn, ha a motívum ÓSZ-ÚSZ ívet ír le)
3. Találati lista → egyenkénti tartalmi értékelés: valódi egyezés vagy kizárandó
4. A megerősített előfordulásoknál: van-e SzPA-lefedettség (jelenleg csak Péld/ApCsel)?
   → ha VAN: join-tábla ellenőrzés/bővítés, ugyanaz a kumulatív modell, mint a bővített sablonnál
   → ha NINCS: explicit jelzés, csak STEPBible-adat szerepel
5. Napló-frissítés + a Lezárási checklist 11. pontja (🔍 STEPBible-ellenőrizve, keresési paraméterekkel)
```

**Fontos egybeesés:** ez pontosan az a workflow, ami a négy már lezárt tematikus tanulmány (tehóm, segítségül hívni, Rafeusok, hádész) visszamenőleges felülvizsgálatánál is alkalmazandó lenne (lásd 8. szakasz, nyitott pontok) — nem külön eljárás, hanem ugyanaz a lépéssor.

**Hol jelentkezik a célzottság a tematikusnál — strukturálisan fordítva, mint a bővítettnél:** itt **nincs előzetes válogatás**, mert a feladat maga (egy motívum összes előfordulásának megtalálása) megköveteli a teljes kánon átfésülését — a szűkítés **a keresés eredménye után**, a találati listánál jelentkezik. A találati lista (jellemzően néhány, legfeljebb 1-2 tucat vers) **már eleve** a "célzott halmaz" — nincs szükség külön, keresés előtti válogatásra, mint a bővítettnél.

**A két modell közötti kulcskülönbség egy mondatban:**
- **Bővítettnél:** előre eldöntjük, mely szavak érdekesek (kritériumlista), *utána* nézzük meg őket
- **Tematikusnál:** a keresés maga dönti el, mi érdekes (a Strong-szám találati listája), *utána* értékeljük, melyik valódi

Mindkét esetben ugyanaz a **kumulatív alapelv** érvényesül: minden generált sor **visszakerül** a privát join-táblába, így egy következő tanulmány, ami ugyanarra a versre/szóra hivatkozik, **már nem generál újra semmit** — csak `grep`-el.

---

## 8. Nyitott pontok (ide kerül minden, ami eldöntetlen maradt)

- [⏸️] **SzPA-integráció felfüggesztve, bizonytalan időre (felhasználói döntés, 2026.08.24).** A privát repó, a két-táblás SzPA-struktúra (versek + lábjegyzetek) és a háromoszlopos [Károli+SzPA] join-tábla terve VÁLTOZATLANUL ÉRVÉNYES marad, csak AKTÍV BŐVÍTÉSE szünetel. A már elkészült minták (Péld 1:1-9, ApCsel 1:1-4) megmaradnak referenciaként. Gyakorlati következmény: minden jövőbeli join-tábla-építés a "csak Károli" (kétoszlopos: Strong + Károli, SzPA-oszlop nélkül) formában készül, publikus repóban — nincs szükség a privát repó aktív használatára, amíg ez a felfüggesztés fennáll. Ha egyszer az SzPA-munka újraindul, a korábban rögzített 4.1-4.2, 6.2, 7.1-es pontok módszertana változtatás nélkül alkalmazható.
- [ ] **Károli-kiadás ellenőrzése:** a scrollmapper HunKar-adat az 1908-as revideált Károli-kiadás — ellenőrizendő, hogy a projekt korábbi tanulmányaiban idézett Károli-szövegek ugyanezzel a kiadással egyeznek-e, mielőtt a strukturált adatbázist visszamenőleg is hitelesítő/ellenőrző forrásként használnánk
- [x] **Strong-taggelt Károli — lezárva, döntés megszületett (4.7).** Mélykutatással azonosítva: Biblia-Felfedező (Bible-Discovery, Zsidó Miklós) — valódi, teljes, szó-szintű Strong-párosítás, de zárt licenc, adatkiemelés csak egyedi engedéllyel. **A projekt saját Károli-datasete emiatt nem erre épül**, hanem a közkincs HunKar-szövegre és a már kidolgozott tartalom-alapú generálási módszerre; a Biblia-Felfedező legfeljebb ellenőrző referenciaként vonható be, ha valaha hozzáférhető lesz.
- [x] **A tematikus/bővített/mélyelemzés sablonok tényleges szövegmódosítása a STEPBible-lépésekkel — lezárva (v22).** `2_PaRDeS_bovitett_sablon.md` (v7→v8): a 2. pontba felvéve a kulcsszó-kiválasztás 6 szempontos kritériumlistája (ez korábban csak a döntési fájl 7.1 pontjában, a sablonfájlban nem volt jelen); a 3/b pont végére felvéve a STEPBible TAGNT/TAHOT kötelező ellenőrzés. `4_PaRDeS_tematikus_sablon.md` (v3→v4): az 1. pont táblázata után felvéve a kötelező STEPBible-egyezés-ellenőrzés; a Lezárási checklist kiegészítve egy **új 11. ponttal** — **ellenőrizve, hogy a checklist a módosítás előtt ténylegesen csak 10 pontos volt** (nem duplikálva semmit). `5_Melyelemzes_prompt_sablon.md` (v2→v3): a 2. pont végére felvéve a STEPBible-lekérdezés. Mindhárom fájlban a pontos, előre egyeztetett szöveg került beillesztésre.
- [x] **A négy már lezárt tematikus tanulmány visszamenőleges STEPBible-ellenőrzése — feltáró fázis lezárva (v34).** A teljes körű TAHOT/TAGNT-grep lefutott mind a négy tanulmány kulcs Strong-számára/számaira, `tematikus_lezart/Konnyu_ellenorzes_4_lezart_tanulmany.md` — 199 "ÚJ ELŐFORDULÁS TALÁLVA" + 5 "ROKON GYÖKŰ JELÖLT" + 4 "NEM ELLENŐRIZHETŐ, konkordancia-rés" jelölt, emberi döntésre várva. **A Károli-Strong join-építés még NEM történt meg** — ez, valamint a talált jelöltek tartalmi értékelése (valódi lexikai egyezés vs. felszíni egybeesés) külön, következő lépés marad:
  - [x] **Tehóm tematikus tanulmány — lezárva (v47).** Mind a 24 új jelölt tartalmi értékelése megtörtént, mind a 24 BEKERÜLT (új 2/b alpont, négy meglévő teológiai regiszterbe rendezve; kiemelve 5Móz 33:13 és Péld 8:27-28 szoros párhuzamai) + a 24 sor felkerült a join-táblába.
  - [ ] Segítségül hívni az Úr nevét tematikus tanulmány — 94 új jelölt tartalmi értékelése (⚠️ a keresési módszer zajos, első lépésként érdemes eldönteni, szándékosan szűk-e a tanulmány tárgya) + join-építés — **szándékosan kihagyva a v47-es körből**, továbbra is nyitott
  - [x] **Rafeusok/óriás-népek tematikus tanulmány — lezárva a helynévi ág tekintetében (v47).** Mind a 6 új jelölt (Refáim-völgy) tartalmi értékelése megtörtént, mind a 6 BEKERÜLT (harmadik jelentéskategóriaként, "Refáim mint helynév") + a 6 sor felkerült a join-táblába. **A 3 rokon gyökű jelölt (H8655 teráfim, H7504, H7510) továbbra is nyitott**, nem volt e kör tárgya.
  - [x] **Hádész (+ Tehóm/Abüsszosz/Tartarosz-komplexum) tematikus tanulmány — lezárva a G0086 ág tekintetében (v47).** A 4 G0086-os jelölt tartalmi értékelése megtörtént: 3 BEKERÜLT (Jel 6:8 a fő ívbe; Luk 10:15 + Mat 11:23 önálló "hübrisz/megaláztatás" alágként), 1 KIZÁRVA (Mat 16:18, ekkleziológiai regiszter) — mind a 4 sor felkerült a join-táblába (a kizárt is, jelölve). **A hádész-komplexum 46 seól-jelöltje (H7585 teljes lexikai mező) továbbra is nyitott**, szándékosan kihagyva e körből.
- [ ] **Új, a fenti ellenőrzés során felfedezett adatminőségi kérdés: a `TAHOT_kivonat.tsv` lefedettségi rése.** A `TAHOT_TAGNT_README.md` "39 könyv, teljes ÓSZ"-t állít, de ténylegesen hiányzik belőle legalább 1Móz 32 teljes fejezete, Zsolt 88/89/140/142 (150-ből 88 zsoltárfejezet van jelen), és Jóel 3. fejezete — a `Konnyu_ellenorzes_4_lezart_tanulmany.md` derítette ki, miközben Zsolt 88:11-et (Rafeusok-tanulmány) és Zsolt 42:8-at (Hádész-komplexum tanulmány) próbálta ellenőrizni. Tisztázandó: elgépelés/feldolgozási hiba a generáló szkriptben, vagy a forrás STEPBible-fájlokban is hiányoznak ezek a fejezetek? Mindenképp befolyásolja minden jövőbeli "teljes körű grep" alapú ellenőrzés megbízhatóságát.
- [x] **TIPNR-lekérdezés Ábrahám/Ábrám névalakjaira — lezárva (v19).** A teljes TIPNR legenerálva `konkordancia/TIPNR_kivonat.tsv`-be; Ábrahám (H0085) és Ábrám (H0087), ill. Sára (H8283) és Szárai (H8297) külön Strong-számmal, teljes előfordulási listával szerepel — az 1Móz 17-es tanulmány előkészítése kész.
- [ ] Php 1:27 végleges döntés — bekerüljön-e ötödik (korporatív jellegű) előfordulásként a pneuma/pszükhé tanulmányba
- [ ] A teljes Példabeszédek és ApCsel könyvek tényleges feldolgozása a két-táblás + join struktúrában (eddig csak minta készült, 1:1-9 ill. 1:1-8 terjedelemben)
- [ ] Döntés arról, hogy a claude.ai chat-felületen történő jövőbeli munkához készül-e szűk hatókörű PAT a privát repóhoz, vagy a munka véglegesen Claude Code-ra kerül át
- [x] **ESV Strong-taggelt hozzáférés — lezárva, nem járható út.** Megvizsgálva: (1) Crossway API — max. 500 vers/fél könyv tárolható helyben; (2) Crossway formális engedélykérés (`crossway.org/permissions/`) — egyedi elbírálású, nincs önkiszolgáló opció; (3) Accordance Bible "ESV with Strong's" modul ($19,90-39,99) — a szoftvergyártó saját dokumentációja explicit kimondja, hogy a megvásárolt szövegek tömeges exportálása más formátumba "gyakran sérti a licencfeltételeket". **Egyik út sem ad jogilag tiszta, azonnal járható megoldást** — a STEPBible interlineáris angol gloss + tartalom-alapú azonosítás marad az elsődleges módszer.
- [ ] **Figyelendő, jelenleg még nem elérhető STEPBible-adatállományok:** a STEPBible-Data README "Datasets coming" szakasza szerint két, fejlesztés alatti forrás érdemi haszonnal járna, ha megjelenik:
  - **TAGOT** (Translators Amalgamated Greek OT — Septuaginta, teljes taggelt szöveg) — ez pótolná a mélyelemzés-sablonnál azonosított hiányzó láncszemet (annak ellenőrzése, hogy egy ÚSZ-i idézet a LXX ugyanazon görög szavát használja-e, mint a héber eredeti fordítása — a "tudatos idézet vs. véletlen egybeesés" kérdés eldöntéséhez)
  - **TBCWG** (Translators Biblical Concept Word Groups — rokon jelentésű szócsoportok, szinonima-elhatárolással) — ez közvetlenül segítené a motívumlog "rokon motívum-csoport küszöbszámítás" elvét
  - Kisebb jelentőségű, szintén készülő: **TOTMM/TNTMM** (kéziratos tanú-adatok szövegkritikai variánsokhoz), **TFBDB** (teljes BDB héber lexikon)
- [x] **Könyv-rövidítés normalizáló tábla — lezárva (v19).** Elkészült `konkordancia/Konyv_normalizalo_tabla.tsv` néven, mind a 66 könyvre (STEPBible angol rövidítés ↔ magyar rövidítés ↔ teljes magyar könyvnév). Két korpuszbeli ellentmondás (Máté/Mt, Ezékiel/Ez↔Ezék) felhasználói egyeztetéssel eldőlt: `Mt`, `Ez`.
- [ ] **Károli-revízió sokféleség — nyitva, nem eldöntött (v21-ben azonosítva, lásd 4.7 és 4.11).** A "Károli" név alatt legalább két, szövegszerűen eltérő kiadás létezik: a jelenleg publikus datasetként használt **1908-as HunKar** (scrollmapper, közkincs) és a **"Revideált Károli" (Veritas Kiadó, 2011)** — modernizált alakokkal (pl. "volt"/"sötétség"/"lebegett" a "vala"/"setétség"/"lebeg vala" helyett), © védett, **nem közkincs** (forrás: karolibiblia.hu, Protestáns Média Alapítvány szakbizottsága). A Biblia-Felfedező program (Baranyi László Zsolt, a Veritas Kiadó engedélyével) feltehetően ezt a 2011-es revíziót futtatja. **Nyitott kérdés:** ha a felhasználó igazolt, jogszerű hozzáféréssel rendelkezik a Veritas 2011-es szöveghez, érdemes-e azt egy külön, **privát** datasetként (a SzPA-mintára, `Bible-Study-privat/`-ba) felépíteni, összevetés/kereszt-ellenőrzés céljából a publikus HunKar mellett? A publikus `Karoli_1908.tsv` semmiképp nem cserélendő rá.
- [ ] **Bibliai Motívumlexikon — koncepcionális tervezés elindult (2026.08.30).** Réteges architektúra-vízió (Szöveg → Konkordancia → Lexikon → Motívum → Kapcsolat → Tanulmány → PaRDeS), egyelőre vázlatos állapotban. Napló: `motivumlog/Bibliai_Motivumlexikon_tervezesi_naplo.md`. Nincs elindított implementáció.
