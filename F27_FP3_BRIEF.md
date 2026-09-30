---
feladat: 27
cim: Thayer-fordítás: Opus és Gemini összevetése, Max-keret méréssel
kod: FP3
tipus: feladat
fazis: 1
modell: opus
allapot: nem_indult
ad: mért adat a #7 modellválasztásához (A: Opus mindenre, B: vegyes hosszhatárral, vagy Gemini marad): minőség hosszkategóriánként, gépi kapuk, Max-keret fogyása és kivetítése a teljes Thayerre
kovetkezo: halasztva (D46): a gépi alap modellválasztásához kell, a #7-tel együtt veszi elő a felhasználó
olvas: [konkordancia/Thayer_teljes.tsv, fp2/, adat/terminologia.tsv, eszkozok/fordit.py, naplok/FP2_jelentes.md, naplok/FORDITAS_P1_minta.tsv]
ir: [fp3/]
fugg: []
helyi_gep: igen
---

# F<nn>_FP3_BRIEF.md — Thayer-fordítás: Opus és Gemini összevetése, Max-keret méréssel

*FELADATOK #<nn> · Modell: opus · v1 · 2026.09.30 · a #7 (Thayer éles) modellválasztását készíti elő*

## 1. Cél

A felhasználó szerint a Gemini 3.1 Flash Lite v3 fordítása (pl. G26) nem elég jó magyarul, az Opus fordítása sokkal jobb. A próba két kérdésre ad mért választ:

1. **Minőség:** mennyivel jobb az Opus hosszkategóriánként (rövid, közepes, hosszú)?
2. **Keret:** mennyit fogyaszt az Opus a Max-keretből, és ebből mennyi idő a teljes Thayer (A út) vagy csak a hosszú szócikkek (B út)?

A #7 briefje ennek az eredménynek az alapján készül. Ez a feladat a #7-hez nem nyúl.

## 2. Hatókör

**Benne van:** prompt v4; 40 szócikkes minta; Opus-fordítás a Code-sessionben; Gemini-fordítás OpenRouteren, ugyanazzal a prompttal; gépi kapuk, köztük egy új idézőjel-kapu; vak pontozás; a felhasználó vak olvasása; Max-mérés; jelentés és döntési tétel.

**Nincs benne:** a C út (Gemini fordít, Opus javít); az `F07_THAYER_ELES_BRIEF.md` módosítása; bármi írása az `fp3/`-on kívül, kivéve a saját `naplok/FP3_*` fájlokat és a `DONTESEK.md`-tételt.

**Helyi gépen fut** (`helyi_gep: igen`). A cloud session a kreditből fogyaszt, nem a Max-keretből, így a mérés értelmetlen lenne. Az OpenRouter-kulcs a helyi környezetből jön. Ha nincs meg, ⛔ állj meg és jelezd.

## 3. Rögzített számok (a chat jóváhagyta, 2026.09.30)

| Tétel | Érték |
|---|---|
| Hosszkategóriák | rövid ≤ 300 karakter; közepes 300–2000; hosszú > 2000 (az FP2 határai) |
| A teljes Thayer (a chat mérése a `main`-en, 2026.09.30) | rövid 2103 / 404 265 kar.; közepes 2917 / 2 017 809 kar.; hosszú 406 / 2 018 010 kar.; összesen 5426 / 4 440 084 kar. Ellenőrizd újramérve, eltérésnél a te mérésed az irányadó, és naplózd. |
| Minta | az `fp2/minta.tsv` 30 szócikke (6 rövid, 17 közepes, 6 hosszú, 1 arany) + 10 új hosszú, seed = 20260930, az FP2 és a kor2 szócikkeinek kizárásával. Összesen 40: 6 rövid, 17 közepes + 1 arany, 16 hosszú. |
| Modellek | Opus (ez a session, `vegrehajto-opus` subagentekkel); Gemini 3.1 Flash Lite (`eszkozok/fordit.py`, OpenRouter, az FP2 provider-zárolásával) |
| Gemini-plafon | 1 USD a teljes próbára |
| Vak olvasás | 10 pár: 4 rövid vagy közepes, 6 hosszú |

## 4. Lépések

**P0 — Prompt v4** (`fp3/prompt_v4.md`)

Az `fp2/prompt_v3.md` szó szerinti másolata, plusz egy „Kiegészítő szabályok (v4)” blokk. A v3 egyetlen sora sem változik; a diff kerüljön a naplóba. A v4 szabályai:

1. Az idézőjeleket és az idézett szerzőt tartsd meg. Ha a forrás mást idéz (pl. Bretschneidert), az idézet a fordításban is idézőjelben álljon, a hivatkozással együtt.
2. A jelentésszám (1., 2.) előtt álló bevezető mondat legyen teljes magyar mondat („Jelentése … eszerint:”), ne csonka szerkezet.
3. Az *equivalent to* fordítása „=” vagy „vagyis”, ne „megegyezik …-val”.
4. A könyvneveket a folyó szövegben írd ki („Márk evangéliuma”, „a Zsidókhoz írt levél”). Rövidítés csak igehelyben álljon, Károli-rövidítéssel.
5. Az *ff* / *f* magyarul „kk.” / „k.”
6. Az elosztó értelmű számokat tedd egyértelművé: *once in Matthew and Luke* → „egyszer-egyszer”.
7. A szerzőnevek egységes alakban álljanak (Philón, Josephus, Tertullianus, Plutarkhosz). Ha van szerzőnév-sor a `fp2/terminologia_v3.tsv`-ben, az az irányadó.
8. Magyar mondatszerkezetet használj: az angol mellékmondat-láncot bontsd magyar mondatokra, de tartalmat ne hagyj el, és ne told be.

A 2. mellékletben lévő G26-részlet példapárként kerül a prompt végére.

**P1 — Minta** (`fp3/minta.tsv`)

Az `fp2/mintavalaszto.py` mintájára, rögzített seed-del. Oszlopok, mint az `fp2/minta.tsv`-ben, plusz `forras` (`fp2` / `uj`).

**P2 — Kapuk** (`fp3/kapuk.py`)

Az `fp2/kapuk.py` másolata, egy új kapuval: **idézőjel-kapu**, amely ellenőrzi, hogy az idézőjel-párok száma a forrásban és a fordításban megegyezik. Egyenes és tipográfiai idézőjelek egyaránt számítanak. A beágyazott idézetnél a »…« a „…” megfelelője.

**⛔ P3 — Max-alapállapot**

Kérd meg a felhasználót, hogy olvassa le a `/usage`-et: az ötórás ablak és a heti Opus- (vagy nehézmodell-) keret százalékát, valamint a csomagot (Max 5x vagy 20x). Az értékek az `fp3/max_meres.tsv`-be kerülnek. Amíg a P4 fut, más Code-munka ne fusson, mert az torzítja a mérést.

**P4 — Opus-fordítás** (`fp3/forditas/opus/kimenet.tsv`)

A 40 szócikk szócikkenként egy `vegrehajto-opus` subagenttel készül. A subagent csak a prompt v4-et, a terminológiát és a forrásszöveget kapja, a Gemini kimenetét nem. A kimenet formátuma az FP2 kimenet-TSV-jéé. Darabolás csak ott, ahol az FP2 is darabolt, ugyanazzal a határral. Minden szócikkhez naplózd a kezdés és a befejezés idejét.

**⛔ P5 — Max-záróállapot**

A felhasználó újra leolvassa a `/usage`-et. Ebből: fogyás a 40 szócikkre, karakterenként, hosszkategóriánként. Ha egy ablak közben újraindult, azt jelölni kell, és a mérést a ténylegesen látott értékekből kell számolni, becslés nélkül.

**P6 — Gemini-fordítás** (`fp3/forditas/gemini/kimenet.tsv`)

Ugyanaz a 40 szócikk, prompt v4, `eszkozok/fordit.py`. A költséget a válaszok `usage` mezőjéből számold. Ha a kivetített költség eléri az 1 USD-t, állj meg.

**P7 — Kapuk és vak pontozás**

A kapuk mindkét kimeneten lefutnak. Utána anonimizálás (`fp2/anonimizal.py` mintájára, címke A/B, szócikkenként véletlen sorrend, seed = 20260930), és a `fuggetlen-ellenor` a kor2/FP2 rubrikájával pontoz, 0–10-ig (`naplok/FP2_jelentes.md`). A bíráló nem láthatja a kulcsot. Mivel a bíráló is Opus, a jelentésben ezt torzítási kockázatként kell jelölni. Ezért kell a P8.

**⛔ P8 — A felhasználó vak olvasása** (`fp3/vak_olvasas.md`)

10 pár a 3. pont szerinti bontásban, A/B címkével, modellnév nélkül. Soronként: melyik a jobb (A / B / egyforma), és egy mondat indoklás. Várj, amíg a felhasználó kitölti.

**P9 — Jelentés** (`naplok/FP3_jelentes.md`) **és döntési tétel**

- Átlagpontszám modellenként és hosszkategóriánként, a kritikus hibák aránya, kapueredmények (külön az idézőjel-kapu).
- A felhasználó vak olvasásának eredménye, és az, hogy egyezik-e a pontszámokkal.
- Max-kivetítés: az A útra (a teljes szöveg) és a B útra (csak a hosszú szócikkek), az ötórás ablakok és a heti keret szerint. Ide kerül a Gemini-költség is a B út maradékára.
- A döntési szabályt az 5. pont szerint alkalmazd, és egy `DONTESEK.md`-tételt nyiss a gépi javaslattal.

## 5. Döntési szabály (javaslat, a DONTESEK-tételben a felhasználó dönt)

| Út | Feltétel |
|---|---|
| **A) Opus mindenre** | az Opus a rövid és a közepes szócikkeken is legalább +1,0 ponttal jobb, és a kivetített idő a felhasználónak elfogadható |
| **B) Vegyes** | a rövid és a közepes szócikkeken a különbség < 0,5, a hosszúakon ≥ 1,0. A hosszhatárt a pontkülönbség adataiból javasold (hol lépi át az 1,0-t). |
| **Gemini marad** (prompt v4) | minden más esetben |

**A felhasználó vak olvasásának elsőbbsége** (javaslat): ha ellentmond a pontszámnak, a vak olvasás az irányadó, mert a magyar stílus mércéje a felhasználó ízlése.

## 6. Munkaszabályok

1. **Számok:** csak a menetben futtatott parancsból vagy a felhasználó által leolvasott `/usage`-értékből. Becslést nem írsz be mért értékként.
2. **Megállás** csak a P3, P5 és P8 ⛔ pontjainál, és ha az OpenRouter-kulcs hiányzik, vagy a Gemini-plafon elérné az 1 USD-t. Minden más kérdés a P9 tételébe gyűlik (D19).
3. **Egyenlő feltételek:** a két modell azonos promptot, terminológiát és darabolást kap. Eltérés csak naplózva lehet.
4. **Zárás a `/kovetkezo` szerint:** `fuggetlen-ellenor` (a menet ellenőrzése, külön a P7 pontozástól), zárójelentés, draft PR, a saját fejléc frissítése.

## 7. Kész, ha

- K1: `fp3/minta.tsv` 40 sorral, a 3. pont bontásában.
- K2: mindkét kimenet 40 sorral; a kapuk lefutottak.
- K3: `fp3/max_meres.tsv` a P3 és a P5 leolvasásával, a csomag megjelölésével.
- K4: vak pontozás és a felhasználó 10 vak párja kész.
- K5: `naplok/FP3_jelentes.md` és a `DONTESEK.md`-tétel nyitva.
- K6: a `fuggetlen-ellenor` jelentése `TISZTA`.

## 1. melléklet — Miért most

A G26 Gemini-fordításában a chat hibái (2026.09.30):

- elveszett idézőjelek, ezért Bretschneider mondata Thayer szavának látszik;
- csonka bevezető mondat („következésképpen jelöli 1. …”);
- tükörfordítások („lakozást vevő”, „megegyezik a…”);
- félrevivő glosszák („szerelem” az 1. jelentésben; „felgyújtott”, „szerzője”);
- rövidített könyvnevek a folyó szövegben;
- vegyes „ff / kk” jelölés.

A HTML-szeletelés ezek közül csak a formai hibákat takarná el.

## 2. melléklet — Példapár a prompt v4-hez (G26, részlet)

**Forrás:** a `konkordancia/Thayer_teljes.tsv` G0026 sorának eleje, a „consequently it denotes” szavakig.

**Célfordítás** (a chatben jóváhagyott, kiejtés nélkül, a v3 szabálya szerint):

> G26 — ἀγάπη, -ης, ἡ; tisztán bibliai és egyházi szó. (Plutarkhosznál, a Sympos. quaest. 7, 6, 3 helyén, Reiske-kiadás VIII. kötet, 835. o., ugyanis Wyttenbach már régen, Reiske sejtését követve, az ἀγάπης, ὧν olvasat helyére ἀγαπήσων alakot állított vissza.) A világi szerzők (Arisztotelésztől), Plutarkhosztól kezdve az ἀγάπησις alakot használták. „A Septuaginta az ἀγάπη szóval adja vissza az אַהֲבָה szót: Én 2:4, 5, 7; Én 3:5, 10; Én 5:8; Én 7:6; Én 8:4, 6, 7 (»Figyelemre méltó, hogy a szó bevett kifejezésként először az Énekek énekében bukkan fel. Ez bizonyosan nem véletlen, és elárulja, hogyan értették az alexandriai Septuaginta-fordítók az Énekben megénekelt szeretetet.« [Zezschwitz, Profangraec. u. bibl. Sprachgeist, 63. o.]); Jer 2:2; Préd 9:1, Préd 9:6; (2Sám 13:15). Előfordul még a Bölcs 3:9 és a Bölcs 6:19 helyen. Philónnál és Josephusnál nem emlékszem, hogy találkoztam volna vele. Az Újszövetségben az Apostolok cselekedetei, Márk evangéliuma és Jakab levele nem használja. Máté és Lukács evangéliumában egyszer-egyszer, a Zsidókhoz írt levélben és a Jelenések könyvében kétszer-kétszer fordul elő, Pál, János, Péter és Júdás írásaiban viszont gyakori.” (Bretschneider, Lexikon, a címszónál); (Philón, Deus immut. 14. §). Jelentése az ἀγαπάω igéét követi, eszerint:

*Megjegyzés a P2-höz:* a Zezschwitz-idézet szögletes zárójele a forrás kerek zárójelét váltja fel, hogy az idézet és a hivatkozás elváljon. Ha az idézőjel-kapu vagy a zárójel-egyezés ezt hibának jelzi, a példapárban kerek zárójel álljon. Formai kérdés, nem tartalmi.

## Verziónapló

| Verzió | Dátum | Változás | Döntés |
|---|---|---|---|
| v1 | 2026.09.30 | első változat | C út kihagyva; helyi gép, mert a cloud a kreditből fogyaszt; a bíráló Opus, ezért kötelező a felhasználó vak olvasása; a v3 kiejtés-tilalma marad, ezért a példapárban nincs kiejtés, és a chatbeli „vö.” betoldás kimaradt |
