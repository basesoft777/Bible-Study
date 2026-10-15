---
feladat: 98
cim: Tervező mód az olvasói szerveren — elem kiválasztása, azonnali előnézet, mentés külön gombbal
kod: TERVEZO_MOD
tipus: feladat
fazis: 1
modell: opus
munka: folyamat
allapot: lezarva
ag: claude/tervezo-mod
ad: tervező mód a belső kiadásban: elem kiválasztása a futó felületen, csak az elem tulajdonságai magyar néven, azonnali előnézet, „Küldés a szerverre” külön gombbal egy arculati token-fájlba; elem-regiszter és regiszter-őr teszt, tartalék a regisztrálatlan elemekre; a méretek változókra cserélve, a megjelenés változatlan; szinkron-kimenet a design systemhez
kovetkezo: "Lezárva; merge a felhasználótól (draft PR). Nyitva: DT-F98g (a helyi-kérés feltétel alapértelmezett nginx mögött); utána a #76 M3"
olvas: [F76_OLVASOI_KONKORDANCIA_BRIEF.md, eszkozok/olvaso_szerver/README.md, eszkozok/olvaso_szerver/statikus/olvaso.css, eszkozok/olvaso_szerver/sablonok/alap.html, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/hozzaferes.py, eszkozok/olvaso_szerver/konfig/szerver.toml, naplok/OLVASOI_KONKORDANCIA_M0.md]
ir: [eszkozok/olvaso_szerver/, naplok/TERVEZO_MOD_M0.md, naplok/TERVEZO_MOD_zaras.md]
lezarva_osszegzes: "Tervező mód a belső kiadásban: 83 elemes regiszter (elemek.toml), regiszter-őr (sablonok, blokkok, kliens classList; a néma minták hibát adnak), token-fájl (arculat.json) /arculat.css?v=<hash> útvonallal, mentési végpont (helyi kérés, egyszeri kód, értékszűrés, atomi írás, előző állapot), kliens (tervezo.js), szinkron-szkript; a megjelenés-azonosság 0 eltérés (M1). Független ellenőr: 5 eltérés, a 3 kisebb javítva (F98.23–F98.25), a proxy-kérdés DT-F98g-ként nyitva; az F98.9/F98.11–13 BDB-jelentésszerkezet a felhasználó külön munkája az ágon. Tesztek: 48+22+13+22+71 OK. Napló: naplok/TERVEZO_MOD_zaras.md, Zárás."
fugg: []
nem_fugg: [76]
---

# F98_TERVEZO_MOD_BRIEF.md — Tervező mód az olvasói szerveren: elem kiválasztása, azonnali előnézet, mentés külön gombbal

*Befogadásra váró brief-tervezet · v1 · 2026.10.14 · forrás: a felhasználó döntései a chatben (2026-10-14): a felület arculatát a futó szerveren, interaktívan akarja állítani; az elemből indul ki, nem a token-listából; azonnali előnézetet akar, és a szerverre küldést egy külön gombbal; a tervező mód az M3 (keresés) elé kerül.*

**Javasolt fejléc-adatok:** `tipus: feladat` · `fazis: 1` · `modell: opus` · `munka: folyamat` [javaslat] · `nem_fugg: [76]` (a #76 M2 és az arculat, PR #346, a main-en van; a két feladat kizárja egymást, nem fut párhuzamosan) · `kovetkezo: "/kovetkezo; ⛔ M0 (az elem-regiszter és a token-fájl formája), ⛔ M3 (a felhasználó kipróbálja)"` · `olvas: [F76_OLVASOI_KONKORDANCIA_BRIEF.md, eszkozok/olvaso_szerver/README.md, eszkozok/olvaso_szerver/statikus/olvaso.css, eszkozok/olvaso_szerver/sablonok/alap.html, eszkozok/olvaso_szerver/alkalmazas.py, eszkozok/olvaso_szerver/hozzaferes.py, eszkozok/olvaso_szerver/konfig/szerver.toml, naplok/OLVASOI_KONKORDANCIA_M0.md]` · `ir: [eszkozok/olvaso_szerver/, naplok/TERVEZO_MOD_M0.md, naplok/TERVEZO_MOD_zaras.md]` · **ütközés:** a #76 ugyanazt az `ir`-t írja (`eszkozok/olvaso_szerver/`), ezért a #76 M3 a #98 lezárása után indul.

## 1. Cél

A kutatói olvasó felületének arculatát (színek, betűméretek, térközök, lekerekítések) a felhasználó **a futó szerveren, az elemekből kiindulva** állíthassa:

1. A belső kiadásban bekapcsolható **tervező mód**: az oldalon rámutatott elem keretet kap, és egy címke megnevezi („Héber szócsempe”, „Versszám”, „Jelleg-címke: modell-kimenet”).
2. **Kattintásra panel** nyílik, amely **csak az adott elem állítható tulajdonságait** mutatja, érthető magyar néven, a jelenlegi értékkel: csúszka (méret, térköz, lekerekítés) vagy színminta a palettából.
3. Minden állítás **azonnal látszik az egész oldalon**, csak a felhasználó böngészőjében (előnézet). Ha egy színtokent ír át (nem csak az elemét), a panel kiírja, hány helyen szerepel. A változások listája látszik, egyenként és egészben visszavonható.
4. **Regiszteren kívüli elem:** a regiszterben nem szereplő elem is kiválasztható. A panel ilyenkor jelzi, hogy „nem regisztrált elem”, és a tokenből jövő tulajdonságait (szín, betűméret, térköz, lekerekítés) gépi névvel kínálja állításra, a „Felvétel a regiszterbe” jelzéssel. Így egy új funkció (pl. a #76 M3 keresőoldala) elemei azonnal állíthatók, a magyar név később kerül melléjük.
5. **„Küldés a szerverre” gomb** (külön lépés): a változtatások a repó egyetlen arculati token-fájljába íródnak. Onnantól a szerver minden lapon, minden nézetben így adja az oldalt, újraindítás nélkül. A mentés látható git-változás. A commitot és a PR-t a végrehajtó vagy a felhasználó készíti, nem a szerver.

A háttér: a token-lista (a design system Colors/Typography lapja) a felhasználónak nem mondja meg, melyik érték mit állít. A tervező mód az elemből indul, és csak az elemhez tartozó tulajdonságokat mutatja.

## 2. Hatókör

- **Benne:**
  - **Előkészítés:** a szerver stíluslapjában (`statikus/olvaso.css`) a betűméretek, térközök és lekerekítések változókra cserélése. A megjelenés nem változhat: a lapok renderelése a csere előtt és után pixelre azonos legyen a mért lapokon, vagy az eltérés listázva.
  - **Arculati token-fájl** a repóban, ebből generálódik a szerver token-blokkja (a mai `:root`), világos és sötét témában. Egyetlen forrás: a stíluslap a token-értékeket nem ismétli.
  - **Elem-regiszter** (konfigurációban, nem kódban): a kiválasztható elemek (CSS-szelektor), a magyar nevük, és elemenként az állítható tulajdonságok (magyar név → token). Mellette a **kizárt osztályok listája**: a tisztán szerkezeti, nem állítandó elemek, egyenként indokolva.
  - **Regiszter-őr:** gépi teszt, amely a szerver sablonjaiban és blokkjaiban (`sablonok/`, `blokkok.py`, `oldalak.py`) használt minden CSS-osztályt összevet a regiszterrel és a kizárt listával. Az ismeretlen osztály hibát ad, megnevezve az osztályt és a helyét. Így új elem csak regisztrálva vagy tudatosan kizárva kerülhet a felületre; a #76 további szakaszainak (M3-tól) ez elfogadási feltétele.
  - **Tartalék a regiszteren kívüli elemekre** (1. cél 4. pont).
  - **A tervező mód kliensoldala:** kapcsoló a fejlécben (a szintváltó mellett), kiemelés, panel, előnézet CSS-változókkal, változáslista, visszavonás, „Küldés a szerverre”.
  - **Mentési végpont** a szerveren.
  - **Tesztek.**
  - **Szinkron-kimenet a design systemhez:** a token-fájlból előállítható a design system `tokens.json`-ja (szkript), hogy a „PaRDeS olvasó” design system (https://claude.ai/artifact/AtQvPhFShiG71apnGPm2AU) frissíthető legyen.
- **Nincs benne:**
  - elrendezés-szerkesztés (elemek mozgatása, hozzáadása, törlése);
  - a sablonok és a blokk-tartalom módosítása;
  - a pilot (`eszkozok/olvaso_pilot/`) módosítása;
  - a design system automatikus feltöltése (azt a felhasználó kérésére végzi az ügynök, az Artifact eszközzel);
  - a nyilvános kiadás bármilyen szerkesztési lehetősége.

## 3. Biztonsági követelmények (kötelező, tesztelve)

- A tervező mód, a kapcsoló, a szkript és a mentési végpont **csak `belso` kiadásban** létezik. `nyilvanos` és `kereskedelmi` kiadásban a végpont 404, a kapcsoló és a szkript nincs a HTML-ben (a szintváltó mintájára).
- **Mentés csak helyi kérésre** (a kérés forrása loopback: 127.0.0.1 vagy ::1), csak `POST`, **egyszeri ellenőrző kóddal** (CSRF-token a lapban). Hiányzó vagy rossz kód: 403.
- A mentés **csak a regiszterben szereplő tokeneket** írhatja, és csak érvényes értékekkel: szín hex vagy `rgb()`/`hsl()`, hossz `px`/`rem`/`em` adott tartományon belül. Minden más elutasítva. A fájlba **semmilyen szabad szöveg** nem kerül.
- A CSP nem lazul: a szkript saját fájl (`script-src 'self'`), inline szkript és inline stílus nincs. Az előnézet CSS-változók beállításával dolgozik.
- A mentés atomi (ideiglenes fájlba írás, majd átnevezés), és az előző állapot visszaállítható. A szerver a token-fájlt és a gyorsítótárat a mentés után újratölti. Az ETag és a gyorsítótár-kulcs a token-fájl tartalmát is tartalmazza, különben a látogató elavult lapot kapna.

## 4. Lépések

1. **M0 — terv (csak olvas). ⛔ Jóváhagyás.**
   - a) **Az elem-regiszter tervezete:** a kiválasztható elemek listája a szerver valódi lapjai alapján (fejléc, folyó szöveg, versszám, kötött szó, szócsempék, LXX-sor, interlineáris csempe, angol csempe, blokkcím, jelleg-címkék, forrássor, szó-lap fejléc, BDB-apparátus, fülek, útmutató, számláló címkék), elemenként a magyar név és az állítható tulajdonságok magyar néven.
   - b) **A token-fájl formája és helye** (javaslat: JSON a szerver konfigurációja mellett, a design system `tokens.json`-jával megfeleltethető nevekkel).
   - c) **A méret-tokenek névjegyzéke** (betűméretek, térközök, lekerekítések), a mai `olvaso.css` értékeiből.
   - d) **A panel működésének vázlata.**

   A felhasználó a regiszterben a magyar neveket és a tulajdonságok körét hagyja jóvá. Napló: `naplok/TERVEZO_MOD_M0.md`.
2. **M1 — előkészítés.**
   - A token-fájl létrehozása a mai értékekkel, és a szerver token-blokkjának generálása belőle.
   - A méretek változókra cserélése az `olvaso.css`-ben.
   - **Megjelenés-azonosság:** a két pilot-szakasz (1Móz 1:1–2:3, Zsolt 22) és egy ÚSZ-fejezet lapjai a csere előtt és után azonosan renderelnek (a számított stílusok összevetése, vagy képernyőkép-összevetés). Eltérésnél ⛔ megállás.
3. **M2 — tervező mód és mentés.**
   - Kliensoldal: kapcsoló, kiemelés, panel, előnézet, változáslista, visszavonás, „Küldés a szerverre”.
   - Mentési végpont a 3. pont szerint.
   - Szinkron-szkript a design system `tokens.json`-jához.
   - Tesztek:
     - a biztonsági követelmények mind (kiadásonként a végpont, a kapcsoló és a szkript jelenléte; loopback; CSRF; értékszűrés; atomi írás);
     - a mentett érték a következő lapkérésnél megjelenik, és az ETag változik;
     - a regiszter minden szelektora legalább egy valódi lapon talál elemet;
     - a regiszter-őr: a mai sablonokban nincs ismeretlen osztály, és egy próbaként hozzáadott, regisztrálatlan osztály hibát ad;
     - a tartalék: egy regisztrálatlan elem kiválasztásakor a panel a tokenből jövő tulajdonságait kínálja, és az előnézet működik.
4. **M3 — ⛔ felhasználói próba.** A felhasználó a futó szerveren kipróbálja: kiválaszt, állít, előnézetben lát, visszavon, ment. Az észrevételei a zárónaplóba kerülnek, a javítás ugyanebben a menetben.
5. **Zárás.** Zárónapló: `naplok/TERVEZO_MOD_zaras.md`. Független ellenőr, draft PR. A felhasználó első mentett arculata külön commit lehet ugyanebben vagy egy későbbi PR-ben.

## 5. Elfogadás

- **Előnézet:** a tervező módban egy elem kiválasztása után a panel csak az elem regiszterbeli tulajdonságait mutatja, magyar néven. Az állítás azonnal, újratöltés nélkül látszik az oldalon.
- **Mentés:** a „Küldés a szerverre” után egy új lapkérés a mentett értékkel jelenik meg (más böngészőből, süti nélkül is), és a változás a token-fájl git-diffjében látszik.
- **Megjelenés-azonosság:** az M1 után a megjelenés a mért lapokon azonos; a mérés naplózva, proveniencia-sorral.
- **Új elemek:** a regiszter-őr teszt zöld a main sablonjain. A regisztrálatlan elem kiválasztható, és a tokenből jövő tulajdonságai állíthatók.
- **Biztonság:** a 3. pont minden követelménye teszttel igazolva. Nyilvános kiadásban a tervezés semmilyen nyoma nincs a HTML-ben.
- **Tesztek:** a szerver tesztjei zöldek (Python 3.12). A nem futtatható teszt kifejezetten jelölve, nem zöldként.
- **Ellenőrzés:** a `feladatok.py ellenoriz` 0 hibát ad.

## 6. Kapcsolódás

- **#76 (OLVASOI_KONKORDANCIA):** ugyanaz a szerver. A #76 M3 (keresés) a #98 lezárása után indul, mert közös az `ir`. Az M3-tól a #76 új elemeit a regiszterbe kell venni, vagy tudatosan kizárni (a regiszter-őr ezt gépileg ellenőrzi). A #76 M5 próbaüzemében a tervező mód a felhasználó eszköze.
- **Előzmények:** a PR #346 (arculat: a pilot tokenjei a szerveren) és a „PaRDeS olvasó” design system (https://claude.ai/artifact/AtQvPhFShiG71apnGPm2AU), amely a token-fájlból frissíthető.
- **#86 (ELOFIZETES_FEED):** nincs kapcsolat; a tervező mód nem hozzáférési szint.

## 7. Döntésnapló

*(üres)*
