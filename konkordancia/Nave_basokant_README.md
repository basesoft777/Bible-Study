# Nave_basokant.tsv — Nave's Topical Bible (1897), témák és igehely-hivatkozások

*F18 · 2026.09.30 · állapot: **javaslat** (l. `naplok/F18_import_naplo.md`, „Küszöb”). Generált fájl: `eszkozok/nave_import.py` — kézzel nem szerkesztendő.*

## Forrás és licenc

- **Forrás:** `github.com/basokant/nave`, commit `4f35c7d4ffd4933f4db1b9d5182db90dc04bd235`, a **nyers szövegfájl** (`data/nave.txt`, sha256 `560dcb1a9cdaccd8df50ed0b714f9d380203795970de8ef79b47d1819052f43a`).
- **Nem vettük át:** a basokant szkriptjeit (`bin/parse.ts`, `bin/scrape.ts`) és a `data/parsed-nave.json`-t; a parszoló saját (`eszkozok/nave_import.py`). A `theonize/bible_database`-t (GPLv3) a DT5 döntés szerint sem a repóba, sem elemzéshez nem használtuk.
- **Licenc:** a mű (Nave, 1897) közkincs a basokant README-je szerint; **licencfájl nincs**. A repó adatfájljára külön licenc nincs deklarálva; az adat a `naves-topical-bible.com` lekaparása. Részletek: `naplok/F18_licenc.md`.
- A nyers `nave.txt` **nincs a repóban** (4,5 MB): a commit-hash és a sha256 reprodukálhatóvá teszi; a generátor `--forras <nave.txt>` paramétert kér.

## Szerkezet

Egy sor = egy hivatkozás (`kapcsolat=vers`), egy „lásd” utalás (`lasd`), vagy egy hivatkozás nélküli szövegegység (`szoveg`). A `nave.txt` hierarchiája a lekaparáskor elveszett (behúzás nincs), ezért a tábla a **forrás sorszerkezetét** őrzi, nem tulajdonít altéma-fát:

| Oszlop | Tartalom |
|---|---|
| `tema_id` | `NAVE-0001`… a fájlbeli sorrend szerint (két cím ismétlődik: `REVERENCE`, `SIN` — külön entry, külön id) |
| `tema` | az entry címe (nagybetűs, ahogy a forrásban) |
| `sor` | a sor sorszáma az entry-n belül (1-től) |
| `sor_jel` | `→` (altéma-sor) · `szam:N` (számozott jelentés) · `folyt` (jel nélküli folytatósor) |
| `tetel` | `0` = a sor feje; `1..n` = a sorban álló `<list><item>` k-adik eleme |
| `cimke` | az egység hivatkozásokat megelőző szövege (a legutóbbi nem-elválasztó szöveg) |
| `kapcsolat` | `vers` · `lasd` · `szoveg` |
| `igehely` | repó-formátum, magyar könyvrövidítéssel, **KJV-számozással** (`2Móz 6:16-20`, `Mt 5:1-7:29`, fejezet: `1Krón 24`) |
| `igehely_osis` | az `osisRef`; **a 296 javított egyfejezetes sorban szintetizált** (`Jude.1.8-Jude.1.13` — a forrás `Jude.1.1`-jéből és a `<ref>` utáni versszámból képezve), ezekben az eredeti forrás-osisRef a `megjegyzes` `eredeti_osis:<osisRef>` eleme; minden más sorban az `igehely_osis` a nyers forrás-osisRef |
| `hely_tipus` | `vers` · `tartomany` · `fejezet` · `fejezettartomany` · `konyvhatar_tartomany` · `ismeretlen_konyv` · `hibas` |
| `karoli_allapot` | egyes versekre a `Karoli_versmegfeleltetes.tsv` szerint: `azonos` · `eltero` · `tobbes` · **`nem_ertekelt`** (a sor `gyanus_kijelzes`-t visel, a hivatkozás megbízhatatlan, ezért a Károli-egyezésre nem ítélünk — minden `gyanus_kijelzes`-sorra, hely_típustól függetlenül) · `a_tablaban_nincs_kjv_megfelelo` (a tábla ismeri a c:v számot, de csak MT-számozásként, üres `igehely_kjv`-vel — pl. 1Sám 17:13; **nem** azonos és nem hiány) · `nincs_a_tablaban` (a c:v szám a táblában sem KJV-, sem MT-oldalon nincs) · `ujszovetseg_nincs_tabla` (a tábla ÓSZ-i); tartományra/fejezetre `tartomany`/`fejezet`; `n.a.` |
| `igehely_karoli` | csak `eltero`/`tobbes` esetén: a Károli-igehely(ek) |
| `cel_tema` | `lasd`-nál a `Nave:` cél (a forrás `target` attribútuma) |
| `megjegyzes` | `gyanus_kijelzes:…` (a kijelzett szöveg nem szabályos hivatkozás-alak, VAGY a `</ref>` után szóköz nélkül hivatkozás-töredék áll, l. lent), `toredek:…` (az elnyelt töredék, pl. `Ch 34:20`), `javaslat:…` (a töredékből és a kijelzés számjegyéből rekonstruált hely, **csak javaslat**, az `igehely` nem íródik át; a töredék első helye), `eredeti_osis:…` (l. `igehely_osis`), `utotag:…` (a hivatkozás utáni egyéb szöveg), `kijelzett:…` (a „lásd” kijelzett szövege eltér a céltól), `vegyes_veg…`, `egyfejezetes_versszam_a_ref_utan:<spec>` (az egyfejezetes könyvek versszáma, l. lent) |

Könyvnév-konverzió: OSIS → STEPBible-rövidítés (a parszolóban) → magyar rövidítés a `Konyv_normalizalo_tabla.tsv`-ből. A 13 `ismeretlen_konyv` sor (12 × `PrAzar.1.2`, 1 × `Wis.2`) nem valódi deuterokanonikus hivatkozás: a lekaparás a névvel összeolvadt „2Ch” / könyvrövidítést értelmezte rosszul (pl. „Azariah 2Ch 31:10” → `PrAzar.1.2`, „Wisdom 2Ch 1:12” → `Wis.2`); a nyers osisRef marad. Mindkettő `gyanus_kijelzes`-t és `toredek:`/`javaslat:`-ot kap (az F18.7 előtt a `Wis.2` szabályosnak látszott, mert a „Wisdom 2” > 6 betű és a töredék a `utotag`-ban volt, de nem ismertük fel hibásnak).

## Figyelmeztetések

- **Egyfejezetes könyvek (Abd, Filem, 2Ján, 3Ján, Júd).** A forrás itt a hivatkozás `osisRef`-jét csak `X.1.1`-re tölti ki, a valódi versszám a `<ref>` UTÁN áll (`<ref osisRef="Jude.1.1">Jude 1</ref>:8-13`). Az első változat ezt nem vette észre: 250 sor lett `X 1:1`, és a versszám a következő sor `cimke` mezőjébe vagy az `utotag`-ba csúszott (688 sor `cimke`-je kezdődött `:<szám>`-mal). A javított parszoló a `<ref>` után álló `:szám`/`:szám-szám`/`:szám,szám` listát a hivatkozáshoz rendeli (vesszős lista = külön sor versenként; tartomány = egy tartomány-sor), és `egyfejezetes_versszam_a_ref_utan:<spec>` megjegyzést tesz. 246 hivatkozás javult; **4 nem javítható biztosan** (versszám a ref után nincs: 2 × „Obadiah 1” a névvel összeolvadt hibás ref, 2 × a „See the EPISTLES OF JOHN” szövegből a `2John.1.1`/`3John.1.1`): ezek `gyanus_kijelzes:egyfejezetes_nincs_versszam` jelölést kapnak, az `X 1:1` érték náluk nem megbízható. A javítás után 0 sor `cimke`-je és 0 sor `utotag`-ja kezdődik `:<szám>`-mal.

- A Nave-hivatkozások **KJV-számozásúak**. Az `azonos`/`eltero` csak egyes versekre és csak az ÓSZ-re ítél; a `nincs_a_tablaban` **nem** „azonos”, hanem „a tábla a c:v számot egyik oldalon sem tartalmazza”; az `a_tablaban_nincs_kjv_megfelelo` „a tábla MT-oldalon ismeri, KJV-megfelelő nélkül” (proveniencia-szabály). A két érték az első változatban egybe volt vonva (`nincs_a_tablaban` 727); a szétválasztás után 582 + 145.
- **A névvel összeolvadt hivatkozások (F18.7).** A lekaparás a könyvnév számjegyét a rövidített névhez ragasztotta: `Son of <ref osisRef="Mic.2">Micah 2</ref>Ch 34:20` (a TSV 125. sora, `NAVE-0011 ABDON`, igehely `Mik 2`, jelölve; `javaslat:2Krón 34:20`) valójában „Son of **2Ch 34:20**”, a `</ref>` után szóköz nélkül maradt betűs töredék. Az első két változat a kijelzést csak akkor jelölte, ha az nem illett a `[rövidítés] szám…` mintába, amely a legfeljebb 6 betűs könyvneveket (Micah, Ezra, Joel, Amos, Titus, Isaiah, Joshua, Daniel, Jonah, So) szabályosnak vette, így ≥29 hamis fejezet-hivatkozás (`Mik 2`, `Ezsd 1`, `Tit 2`, `Jóel 1` …) jelöletlen maradt. A javított felismerés: minden `osisRef`, amelynek a `</ref>` utáni, szóköz nélküli szövege `Ch|Ki|Sa|Ti|Co|Th|Pe|Jn` + szám alakú töredék, `gyanus_kijelzes`-t, `toredek:`-ot kap (a töredéket levágjuk a következő hivatkozás `cimke`-jéről, ezért a 4 korábban cimkébe csúszott töredék — `Ki 14:25`, `Ch 24:20`, `Ki 15:2`, `Ch 6:6,51` — is a megfelelő sor `toredek`-jébe került). Ha a kijelzés számjegye egyezik az osisRef fejezetszámával (ismeretlen könyvnél ez nem követelhető meg), és szám+töredék létező könyvrövidítés (2+Ch = 2Ch), a megjegyzés `javaslat:2Krón 34:20` alakot kap — **az `igehely` nem íródik át** (a rekonstrukció valószínű, de a forrásból nem bizonyítható; a forrást nem javítjuk). A `karoli_allapot` minden jelölt sorra `nem_ertekelt`.
- **Mennyi a jelölt sor (mérve, F18.7 után).** **52 `gyanus_kijelzes`-sor, 54 jelölés-előfordulás** (a `gyanus_kijelzes:` címkék száma a megjegyzésekben; a 2 Abd 1:1-sor kétszer jelölt: összeolvadás + hiányzó versszám). Bontás (sor): 49 összeolvadt-töredékes (mind 49-nek van `javaslat:`-a; ebből 13 `ismeretlen_konyv`: 12 × `PrAzar.1.2`, 1 × `Wis.2`; 36 valódi névvel: Mik/Ezsd/Zak/Jóel/Ézs/Abd/Dán/Tit/Józs/Jón/Ámós/Én …), 2 egyfejezetes versszám nélküli (`2Ján 1:1`, `3Ján 1:1`, a „See the EPISTLES OF JOHN” szövegből; nincs töredék, nincs javaslat), 1 „Jeremiah 2” (`Jer 2`, NAVE-5235: az osisRef `Jer.2` és a kijelzés egyezik, a hivatkozás valószínűleg helyes — a jelölés csak a szokatlan teljes-névalakra szól). A 2 Abd 1:1-sor a 49-be tartozik (mindkettő töredékes: `Ki 18:12`, `Ki 18:3,4`), ezért a jelölés-előfordulás 52 + 2. **A README korábbi „hibák jelölve” állítása így pontosítva:** a jelölés az összeolvadás-osztályt a `</ref>`-utáni töredék-szabállyal fogja meg; hogy nincs más, ettől eltérő hibaosztály, **nem bizonyított** (a teljes független kiadás-összevetés hiányzik).
- A hivatkozás-sorok nem szó szerinti verslisták; a tartományokat nem bontjuk versekre.
- Ez **nem** a lexikai (Strong-alapú) gerinc része; nem mérőeszköz a motívum-azonosításhoz, hanem tematikus index, amelynek minden bejegyzése csak jelölt lehet (`adat/jeloltek.tsv`).

## Mit mér és mit nem mér a generátor (ellenőrzési állítások)

- A sor-szintű szám (82 303 `<ref>` a nyers fájlban (77 935 `osisRef` + 4 368 `target`) ↔ 77 985 `vers` + 4 368 `lasd` sor a kimenetben; a +50 az egyfejezetes vesszős listák (`:9,10`) versenkénti felbontása, l. napló 2.1) **darabszám-egyezés**, nem helyesség: azt mutatja, hogy a parszoló nem nyelt el és nem duplázott hivatkozást. Az egyfejezetes hiba épp ilyen volt: a darabszám egyezett, a versszám mégis hibás.
- A tartalmi ellenőrzés, amit a javítás után futtattam: a `<ref>` kijelzett szövegének (`Ex 6:16-20`, `10`, `Gen 1`) első fejezet:vers száma egyezik-e az `osisRef`-fel — 77 685 nem-egyfejezetes `osisRef`-ből 77 673 egyezik, 12 nem (mind a fent jelölt `PrAzar.1.2` lekaparási hiba). **Ez az ellenőrzés az összeolvadás-osztályt nem fogta meg** (a `Mic.2` és a „Micah 2” egymással egyezik; a hiba a `</ref>` utáni töredékben van), ezért kell hozzá a töredék-szabály (l. fent). Ez a **forrás két mezőjének belső konzisztenciája**, nem a nyomtatott Nave-hoz vagy független kiadáshoz mért helyesség.
- Nem mért: hogy a `nave.txt` maga hűen adja-e a Nave 1897-es szövegét; a témák/altémák hierarchiája (a lekaparáskor elveszett); a `cimke` helyessége.

## Proveniencia

`scope=teljes-Nave | forras=basokant/nave@4f35c7d data/nave.txt | ts=2026-09-30`. Sorszámok: `naplok/F18_import_naplo.md`; a kimenet sorai: 85 116 (77 985 `vers`, 4 368 `lasd`, 2 763 `szoveg`), 5 322 `tema_id` — `scope=teljes-Nave | forras=eszkozok/nave_import.py --forras nave.txt | ts=2026-09-30`.
