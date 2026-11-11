# Vak kitöltés — BDB igehely → jelentéspont (seed-103)

Ez a feladat egy vak mérés kitöltése. A BDB (Brown–Driver–Briggs) héber szótár szócikkeiben egy-egy igehely-hivatkozás áll.
Soronként azt kell megállapítanod, hogy a hivatkozás melyik bibliai versre mutat, és a szócikk melyik jelentéspontja alatt áll.

## Vakság — kötelező

- **Csak ebből a mappából olvashatsz:** `UTASITAS.md`, a köteged `munkalap.tsv`-je és `szocikkek.txt`-je.
- Más fájlt nem nyitsz meg, más könyvtárban nem keresel (Grep, Glob, ls sem). A másik köteg és a többi kitöltő eredménye sem nyitható meg.
- Különösen tilos minden repó: `E:\Claude\Bible-Study\...`, `C:\Users\bases\Desktop\Bible-Study\...`.
- Webet nem használsz.
- Ha egy sort nem tudsz eldönteni, a `megjegyzes`-be írd a bizonytalanságot. Ne keress hozzá máshol segítséget.

## Bemenet

- **`munkalap.tsv`** — a `#` sorok fejléc-megjegyzések. Az oszlopok: `azon strong nyers jelolve kornyezet konyv_mt jelentespont resz megjegyzes`.
  - `nyers`: a hivatkozás alakja a forrásban.
  - `kornyezet`: kb. ±100 karakteres ablak, ebben a hivatkozás `⟦…⟧` között áll.
- **`szocikkek.txt`** — a szócikkek nyers forrásbekezdései, `=== H#### ===` fejléccel. A mért hely előtt `⟦azon⟧` jelölő áll. A szöveg a jelölt helyek után véget érhet.
- A szöveg bekezdéshatárai **a forrás bekezdései, nem a tagolás**. A jelentéspontot a szöveg tartalma dönti el, vagyis a fejek: római szám, törzsnév, szám, betű. Hogy egy rész új bekezdésben kezdődik-e, az nem számít.
- Ha `jelolve` = `nem`, a helyet a `kornyezet` alapján keresd meg a szócikkben.

## Amit kitöltesz, soronként

**`konyv_mt`** — a hivatkozott hely könyve és MT fejezet:verse, magyar rövidítéssel (pl. `1Móz 32:1`, `Zsolt 109:4`).
- A könyv a szócikkben korábban is állhat. A „but 13:10”, „18t.” és a tartomány-alakok esetén a szövegből oldd fel. Tartománynál a kezdővers kell.
- Egyfejezetes könyvnél a fejezet 1.
- Ha a hivatkozás nem bibliai hely (kommentár, nem bibliai mű, szótárhivatkozás), ezt írd: `alhivatkozás: <ok>`.

**`jelentespont`** — a BDB tagolása szerinti hely. Alakja: `[római szakasz ]törzs/jelentés/alpont`, pl. `II Qal/2/a`, `-/1/b`, `Hiph`il/6/c`, `I Pi`el/1`.
- Ha nincs törzs, a törzs helyén `-` áll.
- `fej`: a hely a címsorban, a nyelvi háttérben vagy az alaktanban áll, az első jelentéspont előtt.
- `tagolatlan`: a szócikknek nincs törzse, számozott jelentése és alpontja.

**A római szám:**
1. Ha a forrás a címszó előtt római számot ír (pl. „H3499. yether I. …”, „II. [יָאַל] verb”), azt a fő címszónál is írd: `I fej`, `II Hiph`il`.
2. A szócikk római számos fő tagolását („I. of man: 1 … II. of God: 1 …”, „I. preposition … II. conjunction”) a **`resz`** oszlopba írd, csak a római számot. Ez nem a jelentéspontba megy.
   - Például: „III. עַד … I. preposition … 3 …” → `jelentespont` = `III -/3`, `resz` = `I`.
   - Igénél a tagolás a törzsön belül értendő. A következő törzs, pl. a Niph`al, már nem tartozik hozzá, ott a `resz` üres.
3. Római számot csak akkor írj, ha a forrás kiírja. Következtetett számot ne.
4. A szócikk belsejében álló, **héber címszóval** kezdődő római fej (pl. „II. פְּנֵי with prepositions”) címszó-szakasz, nem rész. Ezt a jelentéspont elejére írd.
5. A jelöletlen második címszónak római szám nélkül add meg a saját törzs/jelentés útvonalát.

**Nem fej:** a kereszthivatkozásban álló jelölő („see 1 above”, „compare Pi`el”, „cf. 2 b”). Ugyanígy nem fej a zárójeles megjegyzésben vagy hivatkozás után álló szám vagy betű. Fej az, amely a tagolásban új pontot nyit.

**Mélység:**
- Írd ki a legmélyebb szintet, amely számmal vagy kisbetűvel jelölt: `törzs/szám/betű`.
- A zárójeles szintet, pl. „(2)”, „(c)”, a `megjegyzes`-be írhatod, de nem kötelező.
- Nagybetűs csoportot (A–H) és görög betűs szintet ne írj az útvonalba.

**`megjegyzes`** — itt jelezd a bizonytalanságot, a forráshiba gyanúját vagy a két lehetséges olvasatot. Rövid, egy sor.

## Magyar könyvrövidítések

1Móz 2Móz 3Móz 4Móz 5Móz Józs Bír Ruth 1Sám 2Sám 1Kir 2Kir 1Krón 2Krón Ezsd Neh Eszt Jób Zsolt Péld Préd Én Ézs Jer JSir Ez Dán Hós Jóel Ámós Abd Jón Mik Náh Hab Sof Hag Zak Mal

A forrás angol rövidítései: Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Psa Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Micah Nah Hab Zeph Hag Zech Mal. Ugyanebben a sorrendben felelnek meg a fentieknek.

A fejezet:vers a forrás számozása (MT). Ne számold át.

## Kimenet

A kimenetet a feladatban megadott fájlba írd: UTF-8, tabbal elválasztva, első sora a fejléc, utána a munkalap minden sora, ugyanabban a sorrendben.

```
azon	konyv_mt	jelentespont	resz	megjegyzes
```

Üres mező üres string legyen. Tab egyik mezőben se álljon. A végén ellenőrizd, hogy a sorok száma egyezik a munkalap adatsorainak számával.
