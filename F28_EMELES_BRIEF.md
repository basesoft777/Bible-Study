---
feladat: 28
cim: A lexikon Thayer- és BDB-szócikkeinek Opus-fordítása, javítóréteggel és CI-őrrel
kod: EMELES
tipus: feladat
fazis: 1
modell: opus
allapot: lezarva
ad: a lexikonba kerülő minden Strong-szám teljes Thayer- vagy BDB-szócikke magyarul (allapot opus, szúrópróbával kezi) az adat/forditasok.tsv-ben; közös javítóréteg és fordítási kapuk; CI-őr; az emelés mint munkafolyamat-lépés
kovetkezo: nyitott: DT26 (terminológia soronként, kalibrált kapus sorok, feladatjelöltek) — Te: döntés; merge csak a felhasználótól
olvas: [adat/elofordulasok.tsv, adat/lexikon_hivatkozasok.tsv, konkordancia/Thayer_teljes.tsv, konkordancia/BDB_teljes_unabridged.tsv, fp2/, eszkozok/fordit.py]
ir: [adat/forditasok.tsv, adat/terminologia.tsv, forditas/prompt_v4.md, eszkozok/normalizal.py, eszkozok/teszt_normalizal.py, eszkozok/forditas_kapuk.py, eszkozok/emeles.py, MUNKAMENET.md, .github/workflows/, eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/tesztek/test_szabalyok.py, eszkozok/ellenorzes/futtat.py, eszkozok/lekerdez.py, eszkozok/teszt_lekerdez_sir.py, eszkozok/teszt_forditas_kapuk.py, eszkozok/ellenoriz.py, eszkozok/teszt_ellenoriz_13.py, adat/SEMA.md, konkordancia/Konyv_normalizalo_tabla.tsv, naplok/EMELES_szentlelek_lista.py]
fugg: []
ag: claude/magical-goldberg-4xb1a0
pr: 100
lezarva_osszegzes: 39 Thayer/BDB szócikk teljes fordítása (10 kezi, 29 opus), kapuk + javítóréteg, CI E19, MUNKAMENET C0; ellenőrzés tiszta az ir-lista kiegészítése után; zárás naplok/F28_zaras.md (10.01)
nem_fugg: [27]
---

# F<nn>_EMELES_BRIEF.md — A lexikon szótári szócikkeinek Opus-fordítása

*FELADATOK #<nn> · Modell: opus · v4 · 2026.09.30 · D42–D45, D47–D50*

## 1. Cél

A lexikonba kerülő Strong-számok **teljes** Thayer-szócikkét (görög) és BDB-szócikkét (héber) az Opus fordítja magyarra. A lexikonba csak a motívumhoz illeszkedő jelentéstartomány kerül (D50), de ezt a render vágja ki a lefordított szócikkből. A fordítás ezért teljes szócikkre szól, és a forrás tagolását (1., 2., a., b., igetörzsek) meg kell őriznie.

A többi szócikk angol marad. A teljes szótár gépi alapfordítása halasztva van, amíg nincs böngésző felhasználó (D46).

## 2. Rögzített számok (a chat mérése a `main`-en, 2026.09.30; futtatással ellenőrizd)

| | Szócikk | Karakter | Leghosszabb |
|---|---|---|---|
| Thayer (G) | 18 | 51 437 | 23 705 (G4151) |
| BDB (H) | 29 | 136 426 | 14 948 (H1121) |
| **Összesen** | **47** | **187 863** | — |

A Strong-számok halmaza: az `adat/elofordulasok.tsv` G- és H-számai, meg az `adat/lexikon_hivatkozasok.tsv` Thayer- és BDB-soraié. **Kimarad**, amelynek már van `teljes` szintű `kezi` fordítása (ma: G1941). A meglévő jelentésszintű `kezi` BDB-fordítások (H7121 2.c és 3, H3548 1, H8034 részlet) megmaradnak, és a renderben elsőbbséget kapnak (D43).

## 3. Lépések

1. **E0 — Lista:** `eszkozok/emeles.py lista` → `naplok/EMELES_lista.tsv` (strong, szótár, karakterszám, meglévő `kezi` sorok). A számokat a 2. ponttal vesd össze, és az eltérést naplózd.

2. **E1 — Prompt v4:** `forditas/prompt_v4.md`. Az `fp2/prompt_v3.md` szó szerinti másolata, plusz két kiegészítő blokk. A v3 kiejtés-tilalma érvényes marad; a kiejtés a külön táblából jön.

   **Általános (v4):**
   1. Az idézőjel és az idézett szerző megmarad. Ha a forrás mást idéz (pl. Bretschneidert), a fordításban is idézőjelben, a hivatkozással.
   2. A jelentésszám előtti bevezető legyen teljes magyar mondat („Jelentése … eszerint:”).
   3. Az *equivalent to* fordítása „=” vagy „vagyis”.
   4. A könyvnevek a folyó szövegben kiírva; rövidítés csak igehelyben, Károli-rövidítéssel.
   5. Az *ff* / *f* magyarul „kk.” / „k.”
   6. Az elosztó számok egyértelműek: *once in Matthew and Luke* → „egyszer-egyszer”.
   7. Szerzőnevek egységesen: Philón, Josephus, Tertullianus, Plutarkhosz; a terminológia az irányadó.
   8. Magyar mondatszerkezet: az angol mellékmondat-láncot magyar mondatokra bontod, tartalom elhagyása és betoldás nélkül.
   9. **A forrás tagolása változatlan:** minden jelentésszám és betűjel (1., 2., a., b., I., II.) a forrás sorrendjében, a forrás helyén.

   **BDB-blokk:**
   1. Az igetörzsek neve változatlan (Qal, Niph., Pi., Pu., Hiph., Hoph., Hithp. és a ritkábbak), a sorrend a forrásé.
   2. A rokon nyelvek neve magyarul (arab, arámi, szír, asszír/akkád, etióp, föníciai); az idegen írású alakok változatlanok.
   3. A héber szöveg változatlan, a jobbról balra írással együtt.
   4. *cf.* → vö.; *q.v.* → l. ott; `sense` → jelentés; a forrás- és kiadássziglák (Ges., Thes., Sam., MT stb.) változatlanok.

   Példapárként a prompt végére az 1. melléklet G26-részlete kerül.

3. **E2 — Javítóréteg:** `eszkozok/normalizal.py`, determinisztikus utófeldolgozás: kk./k., szerzőnevek, könyvnevek a folyó szövegben. Szótáranként kapcsolható; minden szabályhoz teszt (`eszkozok/teszt_normalizal.py`).

4. **E3 — Kapuk:** `eszkozok/forditas_kapuk.py`, az `fp2/kapuk.py` alapján:
   - héber–görög token-egyezés;
   - idézőjel-kapu (az idézőjel-párok száma egyezik);
   - **tagolás-kapu** (a jelentésszámok és betűjelek sorozata azonos; enélkül a render nem tud jelentést kivágni);
   - **törzskapu** a BDB-nél (az igetörzs-címkék azonos sorrendben).

5. **⛔ E4a — Első adag (beépített pilot):** előbb csak 5 szócikk fordul, a lenti E4 szerint, rétegzetten:
   - 1 rövid Thayer-szócikk (a lista legrövidebb Thayer-szócikke);
   - a G5590 (hosszú Thayer);
   - 1 rövid BDB-szócikk (a lista legrövidebb BDB-szócikke);
   - a H7121 (igetörzses BDB-ige; a meglévő kézi jelentései 2.c és 3 összevethetők);
   - a H1121 (óriás, darabolással, ha kell).

   Ha valamelyik nincs a listán, a legközelebbi hasonló lép a helyére; ezt naplózd. Kimenet: `naplok/EMELES_elso_adag.md` (forrás és fordítás egymás mellett, kapueredmények, a H7121-nél a kézi jelentések is). **Várj a felhasználóra.** Ha rendben van, jöhet a maradék. Ha nem, a prompt v4 javul (a változást naplózd a `forditas/prompt_v4.md` verziójában), és az 5 szócikk újrafordul, ugyanezzel a megállással. A jóváhagyott 5 szócikk `kezi` állapotú lesz.

6. **E4 — Fordítás** (az E4a-ban az első 5, a jóváhagyás után a többi szócikkre): szócikkenként egy `vegrehajto-opus` subagent, a prompt v4-gyel, a terminológiával és a forrásszöveggel. Darabolás csak akkor, ha a kimenet nem fér el; ilyenkor a jelentés- vagy törzshatáron, az FP2 utáni darab-megjegyzéssel. Utána javítóréteg, kapuk. Kapuhibánál egy önújrapróba; ha az is bukik, a szócikk a `naplok/EMELES_bukottak.tsv`-be kerül.

   Írás az `adat/forditasok.tsv`-be: `szotar`, `strong`, `entry_id`, `jelentes_szam = teljes`, `mezo = forditas_hu`, `forras_hash`, `forditas_hu`, `allapot = opus`, `modell`, `datum`, `terminologia_verzio`.

   Az új szakkifejezések `javaslat` jelöléssel kerülnek az `adat/terminologia.tsv`-be, és a záró tételbe gyűlnek.

7. **⛔ E5 — Szúrópróba (D49):** az első adag utáni szócikkek 10%-a, de legalább 5, rétegzetten: Thayer és BDB, köztük legalább egy 10 000 karakternél hosszabb (`naplok/EMELES_szuroproba.md`, forrás és fordítás egymás mellett). Amit a felhasználó jóváhagy, `kezi` lesz. Ha a kifogásolt arány 20% fölött van, a menet megáll, és `DONTESEK.md`-tétel nyílik a promptról.

8. **E6 — CI-őr (D44):** új szabály a következő szabad E-számmal. Hiba, ha az `adat/lexikon_hivatkozasok.tsv` egy Thayer- vagy BDB-sorához az `adat/forditasok.tsv`-ben nincs `opus` vagy `kezi` fordítás, sem ugyanarra a `jelentes_szam`-ra, sem `teljes` szintre. Tesztesettel: egy direkt hiányzó sornak hibát kell adnia.

9. **E7 — Munkafolyamat (D48):** a `MUNKAMENET.md`-be egy lépés: új motívum vagy előfordulás után `eszkozok/emeles.py lista`, majd az E4–E5 a hiányzó szócikkekre. A forrássablonba (#23) nem írsz; ha a #23 már lezárult, a naplóban jelezd, hogy hivatkozó sor kell.

10. **E8 — Keretmérés (nem kötelező):** ha a menet helyben, Max-kerettel fut, a felhasználó az E4 előtt és után leolvassa a `/usage`-et. Ebből a naplóban: fogyás 1000 karakterre, a jövőbeli motívumok tervezéséhez. Cloudban ez a lépés kimarad.

## 4. Munkaszabályok

1. Számok csak futtatott parancsból.
2. Megállás csak az E4a és az E5 ⛔ pontnál és a 20%-os küszöbnél (D19). Minden más kérdés a záró `DONTESEK.md`-tételbe gyűlik (terminológia-javaslatok, bukottak).
3. A meglévő `kezi` sorok védettek, nem írod felül.
4. Zárás a `/kovetkezo` szerint: `fuggetlen-ellenor`, zárójelentés, draft PR, a saját fejléc.

## 5. Kész, ha

- K1: a `normalizal.py` tesztjei zöldek; a kapuk lefutottak.
- K2: az E0 listájának minden szócikke `opus` vagy `kezi`, vagy indoklással a bukottak listáján.
- K3: az első adag jóvá van hagyva, és a szúrópróba lezárult.
- K4: az új CI-szabály zöld a `main`-en, és a tesztesetén hibát ad.
- K5: a `MUNKAMENET.md` lépése bent van; a záró tétel nyitva; a `fuggetlen-ellenor` jelentése `TISZTA`.

## 1. melléklet — Példapár (G26, részlet; a chatben jóváhagyva)

**Forrás:** a `konkordancia/Thayer_teljes.tsv` G0026 sorának eleje, a „consequently it denotes” szavakig.

**Célfordítás:**

> G26 — ἀγάπη, -ης, ἡ; tisztán bibliai és egyházi szó. (Plutarkhosznál, a Sympos. quaest. 7, 6, 3 helyén, Reiske-kiadás VIII. kötet, 835. o., ugyanis Wyttenbach már régen, Reiske sejtését követve, az ἀγάπης, ὧν olvasat helyére ἀγαπήσων alakot állított vissza.) A világi szerzők (Arisztotelésztől), Plutarkhosztól kezdve az ἀγάπησις alakot használták. „A Septuaginta az ἀγάπη szóval adja vissza az אַהֲבָה szót: Én 2:4, 5, 7; Én 3:5, 10; Én 5:8; Én 7:6; Én 8:4, 6, 7 (»Figyelemre méltó, hogy a szó bevett kifejezésként először az Énekek énekében bukkan fel. Ez bizonyosan nem véletlen, és elárulja, hogyan értették az alexandriai Septuaginta-fordítók az Énekben megénekelt szeretetet.« (Zezschwitz, Profangraec. u. bibl. Sprachgeist, 63. o.)); Jer 2:2; Préd 9:1, Préd 9:6; (2Sám 13:15). Előfordul még a Bölcs 3:9 és a Bölcs 6:19 helyen. Philónnál és Josephusnál nem emlékszem, hogy találkoztam volna vele. Az Újszövetségben az Apostolok cselekedetei, Márk evangéliuma és Jakab levele nem használja. Máté és Lukács evangéliumában egyszer-egyszer, a Zsidókhoz írt levélben és a Jelenések könyvében kétszer-kétszer fordul elő, Pál, János, Péter és Júdás írásaiban viszont gyakori.” (Bretschneider, Lexikon, a címszónál); (Philón, Deus immut. 14. §). Jelentése az ἀγαπάω igéét követi, eszerint:

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.09.30 | első változat (gépi alap + Opus-emelés) | — |
| v2 | 2026.09.30 | jelentésszintű emelés, szűkítési lépéssel | — |
| v3 | 2026.09.30 | teljes szócikk Opus-fordítása csak a lexikon Strong-számaira; gépi alap halasztva; a szűkítés a render dolga; a prompt v4, a javítóréteg és a kapuk itt készülnek, mert az FP3 halasztva | a felhasználó döntése: nincs böngésző felhasználó, a többi szócikk addig angol maradhat; a tagolás-kapu a render előfeltétele; a Max-mérés csak helyi futásnál |
| v4 | 2026.09.30 | beépített pilot: E4a első adag 5 szócikkel, ⛔ megállással; a szúrópróba az első adag utáni szócikkekből | a prompt v4-et, a javítóréteget és a tagolás-kaput eddig semmi nem próbálta ki (az FP3 halasztva); a hiba így 5 szócikknél derül ki, nem 47-nél; a H7121 a kézi fordítással összevethető |
