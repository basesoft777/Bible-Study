# PaRDeS gyorsreferencia

*v8 — 2026.08.27 (Motívum-felismerés módszertana kiegészítve a 3/b-próba
tapasztalataival: lexikai/tematikus tengely-függetlenség explicit rögzítve,
kifejezés-szintű Strong-keresés bevezetve, önigazoló-hajlam figyelmeztetés
hozzáadva; kisebb javítás: FIGYELEM hivatkozás iránya)*
*v7 — 2026.08.27 (3/b és 3/c önálló, főszintű ponttá alakítva: „Kereszthivatkozási
réteg" mostantól „4. Kereszthivatkozási réteg", a Rabbinikus/patrisztikus hivatkozás
5-re változott; a Mélyelemzés szakasz "3/b."-re mutató visszacsatolása "4. pont"-ra
frissítve)*
*v6 — 2026.08.26 (új „Motívum-felismerés módszertana" szakasz beillesztve a 3/b után:
négyforrásos jelölt-gyűjtés — 🔤 Strong / 📖 Károli-KH / 📚 TSK / 🧠 Claude-tudás —
és háromkategóriás tartalmi minősítés — ✅/❌/🔶; sablon-verziók frissítve: bővített
v10, tematikus v5, mélyelemzés v4)*
*v5 — 2026.08.14 (frissítve: rokon motívum-csoport küszöbszámítás, tematikus sablon feltételes 2. pontja, napló új „Előrejelzett" alszakasza, belső önellenőrzés kiegészítve a lexikai vs. tematikus kapcsolat explicit ellenőrzésével; sablon-verziók frissítve: alap v2, bővített v6, tematikus v3)*

Tömör, kulcsszavas áttekintés a memóriában rögzített szabályokról. A teljes szöveg a sablon-fájlokban és a memóriában érhető el.

## Nyelv és terminológia
- Kiejtés minden görög/héber szó mellett
- „Szent Szellem", nem „Szentlélek"
- Sod-nál „spirituális", nem „misztikus"
- Igehely-rövidítés szóköz nélkül (pl. „1Thessz 5:23")
- Fordítás: Károli teljes versekhez; Szent Pál Akadémia csak rövid idézetben

## Alapkérdések / Kiegészítő szempontok
- 🌍 Történelmi háttér: Alapkérdéseknél rövid (2-3 mondat); Kiegészítőnél konkrét, célzott
- ⚠️ Vitatott pont: csak ha érdemi vita van, nevesített képviselőkkel — nem erőltetve
- Alap sablon Alkalmazás pontja: tömör, kérdéslista nélkül
- Bővített sablon Alkalmazás pontja: 3 konkrét záró kérdés (alapból szöveg-immanens; explicit kérésre nevesített külső tanító szemszögéből is megválaszolható, forrásmegjelöléssel — lásd lent)

## PaRDeS-rétegek
- Remez: csak felismerés/azonosítás, következtetés nélkül
- Drash: normatív, következtető, alkalmazó
- Sod: fegyelmezett, csak szövegből levezethető, gematria/allegorizálás nélkül
- Arány: Alapkérdések rövid; Peshat + Drash legrészletesebb; Sod tömör

## Bővített sablon specifikus pontok
- 0. Sorozat-kontextus: csak ha van korábbi tanulmány ugyanabból a könyvből
- 1/b. Idővonal/térkép: csak ha 2+ helyszín/időpont vagy sorrend kulcsfontosságú
- 2. Eredeti nyelv: max 6-8 kulcsszó/vers + szó szerinti tükörfordítás a Károli mellett
- 5. Rabbinikus/patrisztikus: mindkettő, ha van; ha csak egyik, jelezd miért

## 4. Kereszthivatkozási réteg
- Inline, PaRDeS-szint alatt, nem külön táblázatban
- Irányjelölés: ← előkép / ↔ párhuzam / ⇒ beteljesedés
- Max 1-2 igehely szintenként
- **Kereséskor:** a 2. pont kulcsszavai közül a ritkább/egyedibb szavakra célzott, konkordancia-jellegű előfordulás-ellenőrzés az egész Bibliában, mielőtt a legerősebb kapcsolódást kiválasztod — ne csak ismert/asszociatív motívumokból dolgozz
- Közös motívum-szó félkövérrel kiemelve
- Vizuálisan elkülönített blokk, 🔗 jelöléssel, tényleges bibliai idézettel (Károli)
- Zárójelben: magyar kulcsszó + eredeti szó kiejtéssel
- Záró összegző mondat
- Ismétlődő motívum jelzése a PaRDeS_motivumok.md alapján
- Gazdag/vitatott kapcsolatnál: felajánlás önálló mélyelemzésre
- **Rokon motívum-csoport küszöbszámítás:** ha egy motívum tematikusan rokon, de lexikailag önálló egy másik naplózott motívummal, az egyéni számláló mellett jelöld a rokon-csoport összesített előfordulását is (figyelmeztetésként); mindig indoklással, nem automatikusan

## Motívum-felismerés módszertana

Mielőtt egy kulcsszóhoz/motívumhoz kereszthivatkozást vagy előfordulást választunk,
NÉGY párhuzamos forrásból gyűjtünk jelöltet, mindegyiket forrás-cimkével megjelölve:

- 🔤 [Strong] — teljes körű grep a releváns Strong-számra a TAHOT_kivonat.tsv /
  TAGNT_kivonat.tsv teljes állományán (LEXIKAI jelölt: ugyanaz a szó). HA egy
  vizsgált versben 2+ olyan tartalmi szó van, ami egyedül-egyedül túl gyakori
  ahhoz, hogy önmagában érdemi szó-szintű találatot adjon (ld. FIGYELEM lent),
  futtass egy KOMBINÁLT keresést: melyik más versekben fordul elő UGYANAZ a 2+
  Strong-szám EGYÜTT — ez a kombináció jellemzően sokkal ritkább, mint bármelyik
  szó önmagában, és visszaadja a lexikai pontosságot a gyakori, de együttesen
  jellegzetes szókombinációkra (pl. "Isten" + "teremt" együtt egy versben sokkal
  szűkebb halmaz, mint bármelyik külön-külön).
- 📖 [Károli-KH] — Karoli_kereszthivatkozasok.tsv lekérdezése (EDITORIÁLIS/TEMATIKUS
  jelölt, szentiras.hu szerkesztői hálózat, nincs erősség-jelzés)
- 📚 [TSK] — TSK_kereszthivatkozasok.tsv lekérdezése, Votes ≥ 15 szűréssel
  (EDITORIÁLIS/TEMATIKUS jelölt, Treasury of Scripture Knowledge, erősség-jelzéssel)
- 🧠 [Claude-tudás] — saját, adatforrás nélküli javaslat (a leggyengébb
  megalapozottságú, mindig explicit jelölve marad)

Minden jelöltet HÁROM kategóriába sorolunk, TARTALMI olvasással (nem mechanikus
szűréssel):
- ✅ valódi, releváns találat
- ❌ hamis találat (felszíni/homonim egyezés)
- 🔶 rokon, de eltérő szerkezetű/kategóriájú

FIGYELEM — a két granularitás nem helyettesíti egymást: a [Strong] forrás
ritkasági küszöbe (ld. lent) KIZÁRÓLAG a lexikai (szó-szintű) csatornát szűkíti.
Egy szó kiesése a szó-szintű szűrőn NEM jelenti, hogy nincs erős kapcsolódása —
csak azt, hogy új LEXIKAI találatot nem fogunk vele találni. A [Károli-KH]/[TSK]
vers-szintű keresés mindig, minden igehelyre lefut, függetlenül attól, hogy a
benne szereplő szavak ritkák-e. A leggyakoribb teológiai szavak (Isten, teremt,
van, mond) jellemzően a LEGTÖBB és LEGERŐSEBB vers-szintű találatot vonzzák,
éppen központi jelentőségük miatt — ne értelmezd egy szó szó-szintű kiesését úgy,
mintha az adott fogalom kevésbé volna fontos.

FONTOS: a [Strong]-jelölt "valódi" minősítése LEXIKAI állítást tesz (azonos szó). A
[Károli-KH] és [TSK] jelöltek "valódi" minősítése CSAK tematikus/teológiai kapcsolatot
igazol — ha lexikai rokonságot is állítunk, azt KÜLÖN, Strong-számmal kell
megerősíteni (lásd: lexikai vs. tematikus fegyelem, Munkafolyamat szakasz).

A [Claude-tudás] eredetű, végül ✅-nak minősített jelölt a végleges kimenetben is
MEGTARTJA a forrás-cimkéjét — nem olvad bele észrevétlenül az adatvezérelt
találatok közé.

Csak a minősítés UTÁN történik a végleges kiválasztás (legerősebb 1-2 a bővítettnél,
teljes lista a tematikusnál).

Módszertani önellenőrzés: ha egy nagyobb mintán (pl. sok tanulmány
újraellenőrzésekor) a módszer tartósan NULLA vagy közel nulla arányban minősít
❌/🔶-nak korábban már bekerült idézeteket, ez önmagában is vizsgálandó jel —
lehet, hogy a korábbi (memória-alapú) választások tényleg jók voltak, de az is
lehet, hogy a minősítési lépés nem elég szigorú. Ne tekintsd automatikusan
sikernek, ha a módszer mindig megerősíti a régi döntéseket.

## Alkalmazás pont — nevesített külső tanítói forrás (opcionális)
- Alapértelmezés: a 3 kérdésre adott válasz a tanulmány saját Peshat/Remez/Drash/Sod rétegeiből épül
- Explicit kérésre: nevesített tanító szemszögéből is megválaszolható, kizárólag ellenőrizhető forrásra támaszkodva, forrásmegjelöléssel; ha nincs elég forrás, jelezd explicit módon (ne pótold gyengébb anyaggal)
- **Derek Prince mellett/helyett szóba jöhető nevesített tanítók:**
  - Közvetlen munkatársak (Christian Growth Ministries / „Fort Lauderdale Five"): Bob Mumford, Don Basham, Ern Baxter, Charles Simpson
  - Tágabb Word of Faith/karizmatikus kör: Kenneth Hagin, Kenneth Copeland, Oral Roberts, T. L. Osborn, Charles Capps
- **Motívum-specifikus tanító-lista:** a "pneuma/pszükhé megkülönböztetés" tematikus tanulmányánál mindhárom releváns tanító (Kenneth Hagin — "Spirit, Soul and Body", Derek Prince, Charles Capps) szemszögéből is elkészítendő az Alkalmazás pont, forrásmegjelöléssel

## Research sablon
- Modulok: A) Lukács-ApCsel, B) páli levelek, C) ószövetség
- Minden tudósnál felekezeti/irányzati hovatartozás zárójelben
- Alapmű vs. legfrissebb (5-10 év) szakirodalom megkülönböztetve
- Ha nincs elég forrás, jelezd explicit módon
- Max 2-3 bekezdés pontonként
- Záró "Hogyan építsd be" szakasz

## Tematikus (motívum-alapú) sablon — v3
- Használat: ha egy motívum eléri a PaRDeS_motivumok.md ⭐ Emlékeztető küszöbét (3+ előfordulás), és a felhasználó explicit kéri az önálló feldolgozást
- Szerkezet (részletesen: `4_PaRDeS_tematikus_sablon.md`): (1) előfordulások táblázata, (2) eredeti nyelvi ÉS strukturális összevetés — feltételes: lexikai motívumnál (konkrét szópár/kulcsszó) nyelvi/kiejtéses összevetés; strukturális/narratív mintázatnál (pl. "bűn következményeinek gyűrűzése") a szerkezeti elemek (indító lépés, súlyosbodás lépcsői, lezárás) egymás mellé állítása, (3) PaRDeS keret a motívum egészére alkalmazva (nem egy versre), (4) opcionális kapcsolódás a research sablonhoz, (5) Alkalmazás — motívum-specifikus nevesített tanítókkal, ha van elmentett lista, (6) napló-frissítés: motívum megjelölése "lezárt/önállóan feldolgozott témaként" + fájlnév `[Motívum]_tematikus.md` formátumban + `Lezart_tematikus_tanulmanyok_index.md` frissítése
- Elkülönül a Mélyelemzéstől: az utóbbi két igehelyet vet össze, ez egy egész motívumot dolgoz fel

## Munkafolyamat
- Motívum-napló (PaRDeS_motivumok.md) frissítése minden tanulmány után — beleértve az "Előrejelzett, konkrét igehelyen megerősítendő motívumok" alszakaszt is (⭐ küszöb és Kulcsszó-index között; a következő tanulmány elején automatikusan ellenőrizendő)
- Ütköző szabályoknál: explicit rákérdezés, nem önkényes döntés
- **Véglegesítés előtti belső önellenőrzés kiegészítve:** valahányszor a szöveg azt állítja/sugallja, hogy két igehely közös szótő/szócsalád (lexikai) kapcsolatban áll, ellenőrizni kell, hogy ténylegesen ugyanaz-e a görög/héber szó — ha csak tematikus/fogalmi a kapcsolat, ezt explicit jelezni kell ("tematikus, nem lexikai párhuzam")
- Sorozatfeldolgozásnál: következő igeszakasz felajánlása
- Új memória-szabálynál: jelzés, hogy a sablon-fájl is frissítendő
- Fájlnév-konvenció: `[Könyv]_[fejezet]v[vers]_[típus].md` (pl. `1Moz_1v1_bovitett.md`); tartománynál `[Könyv]_[fejezet]v[vers]-[fejezet]v[vers]_[típus].md` (pl. `1Moz_1v2-2v3_bovitett.md`); teljes fejezetnél vers-komponens nélkül (`1Moz_14_bovitett.md`)
- Sablon-fájlokon verziószám/dátum feltüntetése

## Mélyelemzés (két igehely összevetése)
Csak explicit kérésre, önálló dokumentumként: (1) szövegkörnyezet, (2) nyelvi összevetés, (3) kapcsolat jellege, (4) tudományos vélemények, (5) visszacsatolás a 4. ponthoz vagy a naplóhoz.
