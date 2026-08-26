# 5. Mélyelemzés prompt-sablon — két igehely összevetése

*v4 — 2026.08.26 (a 2. pont elé felvéve a "Motívum-felismerés módszertana"
[PaRDeS_gyorsreferencia.md] háromkategóriás verdiktje — a korábbi bináris "közös szó
van-e" kérdés helyett ✅/❌/🔶 minősítés)*
*v3 — 2026.08.24 (STEPBible-integráció beépítve: a 2. pont [Nyelvi/filológiai összevetés] végére felvéve a kötelező STEPBible TAGNT/TAHOT-lekérdezés — a `PaRDeS_STEPBible_SzPA_dontesek_es_workflow.md`-ben korábban rögzített, de a sablonfájlba eddig be nem épített döntés végrehajtása)*
*v2 — 2026.08.20*

**Kimenet nyelve:** magyar

Vesd össze részletesen **[igehely A]** és **[igehely B]** kapcsolatát, az alábbi szerkezetben:

---

**1. Szövegkörnyezet mindkét igehelyre**
2-3 mondatos kontextus mindkét oldalon — mit csinál ott a szó/fogalom, milyen érvelés/gondolatmenet része.

**2. Nyelvi/filológiai összevetés**
A két igehely kulcsszavának összevetése: NE csak igen/nem választ adj arra, hogy
"közös szó van-e" — a "Motívum-felismerés módszertana" (PaRDeS_gyorsreferencia.md)
három kategóriája szerint minősíts:
- ✅ valódi lexikai egyezés (azonos Strong-szám)
- ❌ nincs kapcsolat
- 🔶 rokon, de eltérő gyök/szó (tematikusan kapcsolódik, nyelvtanilag/lexikailag más)

Ha közös görög/héber szó van: pontosan ugyanazt jelenti-e mindkét kontextusban, vagy van árnyalatnyi eltérés? Ugyanaz a szerző használja mindkét helyen, vagy más szerző? A szó szórendje, alakja, mondatbeli szerepe eltér-e a két helyen?

**STEPBible-ellenőrzés:** ha közös szó feltételezett, futtass le egy STEPBible TAGNT/TAHOT lekérdezést (`konkordancia/TAGNT_kivonat.tsv`, `konkordancia/TAHOT_kivonat.tsv`) mindkét igehely releváns szavára, és a nyers adatot (Strong-szám, szótő, morfológiai alak) építsd be közvetlenül az összevetésbe — ez adja meg a végleges választ arra, hogy a kapcsolat lexikai vagy csak tematikus.

**3. Az irodalmi kapcsolat jellege**
Valódi idézet/tudatos utalás-e (a szerző ismerte és felhasználta a másik szöveget), vagy csak fogalmi/teológiai rokonság, egymástól függetlenül kialakult gondolat?

**4. Tudományos vélemények, ha vitatott**
⚠️ Nevesített szerzőkkel bemutatva, ha a kapcsolat értelmezése maga is vitatott kérdés a tudományos irodalomban — ne homályos "egyesek szerint" megfogalmazással.

**5. Záró mondat — visszacsatolás**
Érdemes-e ennek fényében frissíteni valamit? Két lehetséges célpont van, más-más triggerfeltétellel:

- **A) A fő tanulmány 3/b. pontja** — akkor frissítendő, ha a mélyelemzés *megváltoztatja vagy pontosítja* a 3/b.-ben már szereplő tömör megállapítást (pl. kiderül, hogy a kapcsolat nem tudatos szerzői utalás, csak fogalmi rokonság — ez pontosítaná az irányjelölést; vagy fordítva, kiderül, hogy a kapcsolat erősebb/konkrétabb, mint amit a tömör mondat sugallt).
- **B) A `PaRDeS_motivumok.md` napló** — akkor frissítendő, ha a mélyelemzés *új, önálló motívumot* azonosít, ami eddig nem szerepelt a naplóban, vagy *finomítja* egy már rögzített motívum leírását.

Ha a mélyelemzés csak *megerősíti* a már ismert kapcsolatot, nem hoz új felismerést — ezt is jelezd explicit módon (pl. "A fenti elemzés megerősíti a 3/b. pontban már szereplő megállapítást, nincs szükség módosításra"). Ez ugyanolyan legitim záró megállapítás, mint a frissítés — a lépés nem kényszeríti ki a változtatást, csak tudatosítja a döntést.

---

**Formai szabályok (a PaRDeS-tanulmányokkal megegyezően):**
- Minden görög/héber szótári szó mellett feltüntetve a kiejtés.
- Igehely-rövidítések egységesen, szóköz nélkül (pl. „1Thessz 5:23").
- Idézetekhez a közkincs Károli-fordítás használandó.

**Ha a mélyelemzés önálló, "lezárt" szálként rögzül a `PaRDeS_motivumok.md` naplóban** (nem csak a 3/b. pont pontosítása): a `Lezart_tematikus_tanulmanyok_index.md` fájlba is felveendő, a `4_PaRDeS_tematikus_sablon.md` szerinti tematikus lezárásoktól elkülönítve — más kategória, mivel a mélyelemzés nem a teljes tematikus sablon szerkezetét követi (nincs önálló, motívum-szintű Peshat/Remez/Drash/Sod bontás, sem nevesített tanítói keresés).
