# GLOSSZA_FORDITAS — M1 napló (folyamatban)

*F140 (#140) · M1 · a fordító modell: `claude-sonnet-5-5` (a `modell` mezőben a session saját környezetéből vett név) · állapot: **az M1 kész (11 677 / 11 677); az M2 átnézési lista a `GLOSSZA_FORDITAS_atnezes.tsv`-ben***

Proveniencia: `scope=konkordancia/TBESH.txt + konkordancia/Strong_szotar.tsv + konkordancia/TAHOT_kivonat.tsv + adat/glosszak_heber_hu.tsv | forras=helyi-futtatas (eszkozok/glossza_forditas.py --ellenoriz) | ts=2026-10-25`.

## Folytatási pont

Az M1 kötegenként halad, a legnagyobb TAHOT-előfordulású Strongokkal kezdve (a részleges futás is a legfontosabbat adja). A folytatás nem igényel külön állapotfájlt: a tábla (`adat/glosszak_heber_hu.tsv`) maga az állapot, a következő köteg mindig a még hiányzó (glossza, szófaj) párokból áll.

1. Modell-ellenőrzés (sonnet); a `modell` mezőbe a tényleges név kerül.
2. `python eszkozok/glossza_forditas.py --koteg <ideiglenes_fajl> --csak-bemenet` — a következő 100 pár bemenete (a szabályok a `PROMPT_V1`-ben és a `naplok/GLOSSZA_FORDITAS_M0.md` 3. szakaszában állnak; a 8. szabály terminológia-sora a fájl első sora).
3. Fordítás; a válasz soronként `entry_id | magyar jelentés [| ?]` (a ` | ` vagy TAB tagolás egyaránt jó; az azonosító a bemenet első oszlopa, a pár minden sorára érvényes).
4. `python eszkozok/glossza_forditas.py --rogzit <valasz_fajl> --modell <tényleges modellnév>` — kapuk; a bukó párokat kiírja (`KAPUHIBA`), a többit rögzíti. A bukott párt újra kell fordítani; a második bukásnál `--masodik` mellett a pár a `naplok/GLOSSZA_FORDITAS_elakad.tsv`-be kerül.
5. `python eszkozok/glossza_forditas.py --ellenoriz` (0 hiba), `python eszkozok/teszt_glossza_forditas.py`, commit (`F140.<n>: …`), push.

## Tanácsok a folytatáshoz (Opus-előkészítő, a felhasználó jóváhagyásával rögzítve)

*Rögzítette: `claude-sonnet-5-5`, F140.23; csak dokumentálás és mérés, a tábla nem változott.*

**a) K2 szám.** A mérvadó a végrehajtó mérése: **1 304 / 83 / 5**. Az Opus-előkészítő 1 305 / 87-e nem vonta le külön a K5-ös Strongokat, és a normalizálás is eltért. Az összeg mindkét oldalon **1 392**. A folytató a végrehajtó számát használja.

**b) Kontextus-hossz.** Az árnyalat-soroknál (`a Meaning of`) 90 karakter elég, de ez eltérés a brief ~200 karakteres irányától: **az M2 zárójelentésben rögzítendő**. A kapcsolat nélküli és a homonima-soroknál (a/b, pl. H2763A/B) 200 marad, mert a definíció választja szét a jelentéseket.
- *Mérés* (`scope=eszkozok/glossza_forditas.py hatokor() + adat/glosszak_heber_hu.tsv, 2 771 kész sor | forras=helyi-futtatas | ts=2026-10-25`): a korábbi kód a 90 karakteres szabályt a glosszában lévő `:` jelre építette (`':' in glossza`), nem a kapcsolatra. Ezért a **kész homonima-sorok közül 20 ment 90-nel** (736 ment 200-zal; a teljes hatókörben 1 010 alapnak van több kapcsolat nélküli sora), és 72 kapcsolat nélküli, nem homonima sor is 90-et kapott (1 215 ment 200-zal). Az `a Meaning of` sorok közül 436 ment 90-nel, 14 200-zal (ezeknél nincs `:`).
- *Szúrópróba-lista:* a 20 érintett (strong, entry_id) pár a `naplok/GLOSSZA_FORDITAS_homonima_szuroproba.tsv`-ben áll (H1004B, H1121A, H1197A, H1350A, H1419A, H1870K, H1984B, H2342A, H2470A, H2490C, H2491A, H3559A, H5158A, H5612A, H5800A, H6485A, H6924G, H6963H, H6999A, H7760A). A fordításuk gyanús abban, hogy a kétértelműséget a rövid kontextus nem oldotta fel; átnézéskor ezeket kell először nézni. A 72 nem homonima, kapcsolat nélküli sor kisebb kockázat (egy főjelentés), de az átnézésnél szintén `:`-os glosszák.
- *Kód:* a `kontextus_hossz()` mostantól `kapcsolat == 'a Meaning of'` esetén ad 90-et, minden másnál 200-at (a homonimánál is); a következő kötegektől így érvényes. A 15 teszt zöld, `--ellenoriz`: 0 hiba. A már rögzített sorokat a kód nem érinti.

**c) H6310 (gloss `lip`).** A `H6310G` sor ma `ajak` fordítást hordoz `?` nélkül; a szócikk jelentése „mouth”. A megjegyzésbe `?` kerülne. A táblát a szkript védelme miatt (`tabla_ir`: a meglévő sor nem változhat) kézzel nem írtam át, és a szkriptnek nincs megengedett módja meglévő sor módosítására. **Teendő a folytatónak:** az átnézés `allapot=kezi` soraihoz felvenni a H6310G-t (`?` a megjegyzésben, a fordítás eldöntése: `ajak` vagy `száj`), vagy a `tabla_ir` védelmét kiegészíteni egy dokumentált, naplózott javító móddal.

**d) H90xx utótag-csoport (H9023 `his`, H9024 `her`).** Egy egységes forma kell a teljes H90xx csoportra, az átnézésnél dől el. Javaslat: `-a/-e, -ja/-je (hímn. 3. sz.)` vagy `ő… (hímn.)`. A ma rögzített H9023 `-ja/-je` és H9024 `-ja/-je (női)` eltérő szerkezetű. **A folytató ne rögzítsen újabb H90xx sort eltérő formában**; a H90xx sorok (ma 37) egységesítése az átnézés feladata.

**e) K8.** Az `ADAT_LICENC`-bejegyzés (`'glosszak_heber_hu': ['TBESH', 'TAHOT', 'projekt_adat']`, a fenti szakasz szerint) **a tábla main-re kerülése ELŐTT** kell, különben a CC BY 4.0 forrásjelölés nélkül töltődik be. **A zárójelentésnek (M2) ezt külön jeleznie kell**, és a merge előtt a kisfeladatot el kell végezni.

## Állás

A 2026-10-25-i session (`claude-sonnet-5-5`) 17 köteget rögzített (a 12 fix istennév-sor mellett): **2 771 sor / 11 677** (23,7%), **1 670 Strong / 8 718** legalább egy sorral; kapuhiba 0 (`--ellenoriz`), elakadó 0 (`naplok/GLOSSZA_FORDITAS_elakad.tsv` nem jött létre), bizonytalan (`?` a `megjegyzes`-ben) 20 sor. Hátra: **6 481 (glossza, szófaj) pár ≈ 65 köteg** (100 pár/köteg). A sorrend TAHOT-gyakoriság szerinti csökkenő, tehát a leggyakoribb szavak készek; a 300 leggyakoribb Strong jó része már a táblában van. A `fo` jelölt (1 632 sor `igen`) a K2-szabály szerint számolt; a részben kész 38 Strongnak a `fo` sora még fordításra vár.

## Megfigyelések (az M2 zárójelentés és a felhasználói átnézés számára)

- **A TBESH-glossza és a szócikk jelentése eltérhet** (pl. H6310 `lip`, miközben a szócikk „mouth”): a prompt szabálya szerint a glossza a fő támpont, ezért a fordítás a glosszát követi („ajak”). Az ilyen helyek a 300-as átnézőlistára tartoznak.
- A **kötőszavak, előtag- és utótag-elemek** (H9001–H9048) glosszái nyelvtani elemek („his”, „[the]”, „to/for”); a fordításuk toldalék-alak („-ja/-je”, „-hoz/-hez”). A H9023 „his” és a H9024 „her” fordítása a rögzítéskor nem különbözteti meg a nemet (a „her” női jelölést kapott); a kézi átnézésnél érdemes egységesíteni.
- A kérdőjel a szövegben tilos (kapu), ezért a kérdő névmás glosszája („what?”, „who?”) „mi (kérdő)”, „ki (kérdő)”.
- A **hossz-korlát** (50 karakter) a hosszú összetett glosszákat („megszentségteleníteni/kezdeni: …”) megrövidített szóra kényszerítette („gyalázni/kezdeni: …”).
- A köteg-bemenet a kettőspontos árnyalat-soroknál 90 karakteres definíció-kontextust használt a 17. kötegig (`:` a glosszában); a 18. köteg ELŐTT a szabály a kapcsolatra váltott, l. a Tanácsok b) pontját: a szülő-szócikk szövege az árnyalat-soroknál ismétlődik, az árnyalat-címke az első karakterekben áll.

## A K8 javaslata (nem végrehajtva; a #140 nem nyúl az `sqlite_epit.py`-hoz)

Külön kisfeladat: az `eszkozok/sqlite_epit.py` `ADAT_LICENC` szótárába `'glosszak_heber_hu': ['TBESH', 'TAHOT', 'projekt_adat']`. Időzítés: a tábla main-re és a `pardes.db`-be kerülése előtt (különben a CC BY 4.0 forrásjelölés nélkül töltődik be). A SEMA 2.34 licenc-bekezdése ugyanezt rögzíti.

## Összhang a #138-cal

Az istennév-alakok (K5: „az ÚR”, „Isten”, „Úr”, „isten”, „Felséges”, „Jah”, „Mindenható”, „Seregek”, „Baáli”) összhangban kell legyenek a #138 DT-F138b-jével (még 🟡). A #140 ezt nem dönti el; a megjegyzés a `DONTESEK.md` DT346 sorában áll.
