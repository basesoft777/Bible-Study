---
feladat: 40
cim: Hivatkozás-ellenőrzés a feladatkövetőben (CI új szabálya)
kod: HIVATKOZAS_ELLENORZES
tipus: feladat
fazis: 1
modell: sonnet
allapot: dontesre_var
ad: a CI minden PR-nál jelzi, ha a FELADATOK.md vagy egy brief nem létező fájlra, ágra vagy commitra mutat, illetve ha egy PR áthelyez vagy töröl egy hivatkozott fájlt anélkül, hogy a mutatót frissítené
ag: claude/hivatkozas-ellenorzes
kovetkezo: "Te: DT-F40a (az E27 hatóköre) és DT-F40b (átfedés az E18-cal) döntése; utána a javítás, a PR címe [ELLENŐRZŐ] előtagú (E16), a 4–6. ellenőri pont (kivételek, tesztek, 16 teszt) a javításban"
olvas: [FELADATOK.md, NYITOTT_FELADATOK.md, CLAUDE.md, .github/workflows/, eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/futtat.py, eszkozok/ellenorzes/tesztek/test_szabalyok.py, BRIEF_SABLON.md]
ir: [eszkozok/ellenorzes/szabalyok.py, eszkozok/ellenorzes/futtat.py, eszkozok/ellenorzes/tesztek/, .github/workflows/ellenorzes.yml, CLAUDE.md, naplok/ELLENOR_HIVATKOZAS.md]
fugg: [2]
---

# Hivatkozás-ellenőrzés a feladatkövetőben (CI új szabálya)

*A fájlnévben az `F00` helyőrző: a végleges feladatszámot a `/befogad` adja. A szabály munkaneve E25; ha a szám foglalt, a következő szabad E-számot kapja.*

## 1. Miért

A `FELADATOK.md` „Hol” oszlopa és a briefek fejlécei ágakra, fájlokra és commitokra mutatnak. Ezek csendben elavulnak: ágat törlünk, briefet áthelyezünk, naplót átnevezünk. A chat ilyenkor hibás mutató alapján dolgozik, és a hibát csak tokenigényes rekonstrukcióval veszi észre. A szabály ezt gépi ellenőrzéssé teszi, ugyanazon az elven, mint a meglévő E-szabályok.

## 2. Mit ellenőriz

| Ellenőrzés | Mit vizsgál | Szint |
|---|---|---|
| A — fájlútvonal | A `FELADATOK.md` és a `NYITOTT_FELADATOK.md` backtickes útvonalai (van bennük `/`, vagy `.md`, `.tsv`, `.py`, `.json`, `.yml` végű) léteznek-e a PR kódjában | hiba |
| B — ág | A `claude/…` alakú ágnevek léteznek-e a távoli repóban (egy `git ls-remote --heads` hívás, nem ágonként) | hiba nyitott sorban, figyelmeztetés a „Kész” szakaszban |
| C — commit | A 7–40 jegyű hexa commit-azonosítók léteznek-e (`git cat-file -e`) | figyelmeztetés |
| D — brief fejléce | A repóban lévő `*_BRIEF.md` fájlok YAML-fejlécének `olvas` mezőjében felsorolt útvonalak léteznek-e | figyelmeztetés (lehet, hogy egy függő feladat állítja elő) |
| E — áthelyezés mutató nélkül | A PR diffjében törölt vagy átnevezett fájl (`git diff --name-status` D és R sorai) szerepel-e még hivatkozásként a fenti fájlokban | hiba, üzenet: „frissítsd a mutatót ugyanabban a commitban” |

**Kivételek:**

- Az a sor, amelynek „Hol” cellája a „csak chatben” szöveget tartalmazza, nem ad A-hibát (a brief még nincs a repóban, ez szándékos állapot).
- Az `ir` mező nem ellenőrzendő (a feladat még nem hozta létre a fájlokat).
- Könyvtárra mutató útvonal (`/` végű) akkor jó, ha a könyvtár létezik.

**Hatókör (DT-F40a, 2026.10.07):** a `FELADATOK.md` generált blokkjának nyitott sorain (a `kesz` blokkon kívüli blokkokon) a hiányzó fájl és a nem létező commit mindig HIBA (diff-hatókör nélkül), a nem létező ág FIGYELMEZTETÉS (a tervezett ág érvényes); a hibaüzenet a forrás-briefet nevezi meg. A brief `olvas`-mezőjének hiányzó fájlja mindig HIBA, kivéve ha egy `fugg`-beli feladat `ir` mezője fedi az útvonalat (egyezés, könyvtár-előtag vagy joker): akkor FIGYELMEZTETÉS. A `FELADATOK.md` Kész szakaszában a fájlhiány FIGYELMEZTETÉS (H2). A `NYITOTT_FELADATOK.md` és minden egyéb hely diff-hatókörű marad. A D-ág csak az `olvas` útvonalait ellenőrzi; a fejléc érvényessége (hibás YAML, lezáratlan fejléc) az E18-é (DT-F40b).

**A szabály kódbeli kivételei (a briefben eredetileg nem szerepeltek, a DT-F40 ellenőri jelentés 4. pontja nyomán dokumentálva és tesztelve):**

- Könyvtár nélküli rövid név (`ellenoriz.py`) akkor elfogadott, ha a repóban *bármely* helyen van azonos nevű fájl (a feladatkövető szövegei így hivatkoznak).
- Kiterjesztés nélküli `a/b` alak csak akkor fájlútvonal, ha az első tagja létező repó-bejegyzés (különben pl. `szervezet/repo` téves jelzés lenne).
- A `beerkezo/` és a `konkordancia/` (valamint a `.`-tal kezdődő és `node_modules`) könyvtárak briefjei nem tartoznak a D-ághoz (beérkezett vagy adat-jellegű anyag, nem feladatbrief).
- URL-ek, `claude/…` ágnevek és a `*`/`<`/`{` jelű minták nem fájlútvonalak.
- A `NYITOTT_FELADATOK.md:612/614` adatkészlet-belső rövidítései (`base/display/` stb.) NEM kapnak kivételt (DT-F40a (f)): a takarítási pontba mennek.

## 3. Hogyan

1. Python, csak standard könyvtár, a meglévő E-szabályok szkriptjeinek mintájára (parancssor, kimenet, kilépési kód ugyanúgy).
2. A hibák és figyelmeztetések GitHub-annotációként jelennek meg (`::error file=…,line=…::` és `::warning …`), sorszámmal, hogy a PR-ban a sorra mutassanak.
3. A munkafolyamatban `fetch-depth: 0`, különben a C-ellenőrzés sekély klónon téves figyelmeztetést ad.
4. CRLF-tűrő beolvasás (a szkript-karbantartás feladatával összhangban).
5. Tesztek tesztadatokkal: egy jó feladatkövető, egy hiányzó fájllal, egy törölt ággal nyitott sorban, egy törölt ággal a „Kész” szakaszban, egy „csak chatben” sorral, egy hibás YAML-fejlécű brieffel. Minden esetre ellenőrizni a szintet és a kilépési kódot.

## 4. Döntések menet közben

⛔ **Állj meg és kérdezz**, ha:

- a meglévő CI-ben már van olyan szabály, amely az A–E ellenőrzések bármelyikét részben végzi (ne legyen kettős ellenőrzés: jelezd, melyiket bővítsük);
- a B-ellenőrzés a GitHub Actions tokennel nem éri el a távoli ágakat.

## 5. A `CLAUDE.md`-be kerülő sor

„Ha egy commit fájlt áthelyez, átnevez vagy töröl, ugyanabban a commitban frissíti a rá mutató hivatkozásokat a `FELADATOK.md`-ben, a `NYITOTT_FELADATOK.md`-ben és a briefek `olvas` mezőjében.”

## 6. Kész, ha

- a szabály zöld a jelenlegi main-en, vagy a piros eredményei valódi elavult hivatkozások, és ezek listája a záró összefoglalóban szerepel (javítani nem ennek a menetnek a dolga, csak felsorolni);
- a tesztek zöldek;
- a menetzárás a szokásos: `fuggetlen-ellenor` jelentés `naplok/ELLENOR_HIVATKOZAS.md`, push, draft PR, a záró összefoglaló első sora a PR linkje és a CI állapota.

## 7. Nyitó prompt

<!-- KOZVETLEN_FUTTATAS -->
Olvasd el ezt a briefet, a `CLAUDE.md`-t és a meglévő CI-szabályok szkriptjeit. Valósítsd meg az új hivatkozás-ellenőrző szabályt a 2–3. pont szerint, a meglévő E-szabályok mintáját követve. Előbb ellenőrizd, hogy a szabály munkaszáma (E25) szabad-e, és hogy van-e átfedés meglévő szabállyal; átfedés esetén állj meg és kérdezz (4. pont). Írd meg a teszteket, kösd be a munkafolyamatba, add hozzá a `CLAUDE.md` sorát (5. pont), majd zárd a menetet a 6. pont szerint. A main-en talált elavult hivatkozásokat ne javítsd, csak sorold fel a záró összefoglalóban.
<!-- /KOZVETLEN_FUTTATAS -->

## Döntésnapló

| # | Döntés | Indok | Elvetett alternatíva |
|---|---|---|---|
| H1 | A szabály a CI része, PR-onként fut | a mutatót a hibát okozó PR-ban kell javítani, ott a legolcsóbb | külön éjszakai ütemezett futás (az ágtörlés PR nélkül is történhet, de ezt a következő PR B-ellenőrzése elkapja) |
| H2 | Ág és fájl hiánya nyitott sorban hiba, a „Kész” szakaszban és commitnál figyelmeztetés | merge után az ág törlése normális, a régi commit-hivatkozás nem blokkolhat | mindenhol hiba |
| H3 | A „csak chatben” sor nem hiba | szándékos, átmeneti állapot; a takarítási pont kezeli | a sor hibát ad, amíg a brief nincs a repóban |
| H4 | A main-en talált régi hibákat a menet nem javítja | a feladat a szabály, nem a takarítás; a javítás a takarítási ponthoz tartozik | a menet a szabály mellett a main-t is kitakarítja |
| H5 | A szabály száma E25 | az E17–E24 foglalt (F15, F37) | E17 |
| H1a | *(DT-F40a, 2026.10.07, a H1 pontosítása)* A „következő PR elkapja” a generált blokk nyitott sorain és a brief `olvas`-mezőjén diff-hatókör nélkül, mindig HIBA; a többi hely diff-hatókörű | a generált blokkot PR nem szerkeszti, a diff-hatókör ott soha nem hibázna | minden mindig HIBA (a régi hibák javítása külön tétel) |
| H2a | *(DT-F40a (c), a H2 pontosítása)* A Kész szakaszban a fájlhiány is figyelmeztetés (nem csak az ág); az `olvas`-mező hiányzó fájlja figyelmeztetés, ha egy `fugg`-beli feladat `ir` mezője fedi | a kód a Kész szakaszban hibát adott, ellentétben a H2-vel | marad a hiba a Kész szakaszban |
| H5a | A szabály száma E27 (a H5 elavult) | az E25 (döntés-átvezetés) és az E26 (végleges szám az ágon) foglalt | E25 |
| H7 | *(DT-F40b)* A D-ág csak az `olvas` útvonalait ellenőrzi; a fejléc-érvényesség az E18-é | nincs kettős ellenőrzés; a végrehajtó a 4. pontnál nem állt meg, ez eltérés (naplok/F40_zaras.md) | a D-ág fejléc-ellenőrzése marad |
| H6 | A menet nem írja a FELADATOK.md-t | a generált blokkot a D25/E18 szerint csak a main-Action írja | a saját sor frissítése a menet végén |
