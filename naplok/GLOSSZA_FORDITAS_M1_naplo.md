# GLOSSZA_FORDITAS — M1 napló (folyamatban)

*F140 (#140) · M1 · a fordító modell: `claude-sonnet-5-5` (a `modell` mezőben a session saját környezetéből vett név) · állapot: **fut, folytatandó***

Proveniencia: `scope=konkordancia/TBESH.txt + konkordancia/Strong_szotar.tsv + konkordancia/TAHOT_kivonat.tsv + adat/glosszak_heber_hu.tsv | forras=helyi-futtatas (eszkozok/glossza_forditas.py --ellenoriz) | ts=2026-10-25`.

## Folytatási pont

Az M1 kötegenként halad, a legnagyobb TAHOT-előfordulású Strongokkal kezdve (a részleges futás is a legfontosabbat adja). A folytatás nem igényel külön állapotfájlt: a tábla (`adat/glosszak_heber_hu.tsv`) maga az állapot, a következő köteg mindig a még hiányzó (glossza, szófaj) párokból áll.

1. Modell-ellenőrzés (sonnet); a `modell` mezőbe a tényleges név kerül.
2. `python eszkozok/glossza_forditas.py --koteg <ideiglenes_fajl> --csak-bemenet` — a következő 100 pár bemenete (a szabályok a `PROMPT_V1`-ben és a `naplok/GLOSSZA_FORDITAS_M0.md` 3. szakaszában állnak; a 8. szabály terminológia-sora a fájl első sora).
3. Fordítás; a válasz soronként `entry_id | magyar jelentés [| ?]` (a ` | ` vagy TAB tagolás egyaránt jó; az azonosító a bemenet első oszlopa, a pár minden sorára érvényes).
4. `python eszkozok/glossza_forditas.py --rogzit <valasz_fajl> --modell <tényleges modellnév>` — kapuk; a bukó párokat kiírja (`KAPUHIBA`), a többit rögzíti. A bukott párt újra kell fordítani; a második bukásnál `--masodik` mellett a pár a `naplok/GLOSSZA_FORDITAS_elakad.tsv`-be kerül.
5. `python eszkozok/glossza_forditas.py --ellenoriz` (0 hiba), `python eszkozok/teszt_glossza_forditas.py`, commit (`F140.<n>: …`), push.

## Állás

A 2026-10-25-i session (`claude-sonnet-5-5`) 17 köteget rögzített (a 12 fix istennév-sor mellett): **2 771 sor / 11 677** (23,7%), **1 670 Strong / 8 718** legalább egy sorral; kapuhiba 0 (`--ellenoriz`), elakadó 0 (`naplok/GLOSSZA_FORDITAS_elakad.tsv` nem jött létre), bizonytalan (`?` a `megjegyzes`-ben) 20 sor. Hátra: **6 481 (glossza, szófaj) pár ≈ 65 köteg** (100 pár/köteg). A sorrend TAHOT-gyakoriság szerinti csökkenő, tehát a leggyakoribb szavak készek; a 300 leggyakoribb Strong jó része már a táblában van. A `fo` jelölt (1 632 sor `igen`) a K2-szabály szerint számolt; a részben kész 38 Strongnak a `fo` sora még fordításra vár.

## Megfigyelések (az M2 zárójelentés és a felhasználói átnézés számára)

- **A TBESH-glossza és a szócikk jelentése eltérhet** (pl. H6310 `lip`, miközben a szócikk „mouth”): a prompt szabálya szerint a glossza a fő támpont, ezért a fordítás a glosszát követi („ajak”). Az ilyen helyek a 300-as átnézőlistára tartoznak.
- A **kötőszavak, előtag- és utótag-elemek** (H9001–H9048) glosszái nyelvtani elemek („his”, „[the]”, „to/for”); a fordításuk toldalék-alak („-ja/-je”, „-hoz/-hez”). A H9023 „his” és a H9024 „her” fordítása a rögzítéskor nem különbözteti meg a nemet (a „her” női jelölést kapott); a kézi átnézésnél érdemes egységesíteni.
- A kérdőjel a szövegben tilos (kapu), ezért a kérdő névmás glosszája („what?”, „who?”) „mi (kérdő)”, „ki (kérdő)”.
- A **hossz-korlát** (50 karakter) a hosszú összetett glosszákat („megszentségteleníteni/kezdeni: …”) megrövidített szóra kényszerítette („gyalázni/kezdeni: …”).
- A köteg-bemenet a kettőspontos árnyalat-soroknál 90 karakteres definíció-kontextust használ (a nem-árnyalat soroknál 200): a szülő-szócikk szövege az árnyalat-soroknál ismétlődik, az árnyalat-címke az első karakterekben áll.

## A K8 javaslata (nem végrehajtva; a #140 nem nyúl az `sqlite_epit.py`-hoz)

Külön kisfeladat: az `eszkozok/sqlite_epit.py` `ADAT_LICENC` szótárába `'glosszak_heber_hu': ['TBESH', 'TAHOT', 'projekt_adat']`. Időzítés: a tábla main-re és a `pardes.db`-be kerülése előtt (különben a CC BY 4.0 forrásjelölés nélkül töltődik be). A SEMA 2.34 licenc-bekezdése ugyanezt rögzíti.

## Összhang a #138-cal

Az istennév-alakok (K5: „az ÚR”, „Isten”, „Úr”, „isten”, „Felséges”, „Jah”, „Mindenható”, „Seregek”, „Baáli”) összhangban kell legyenek a #138 DT-F138b-jével (még 🟡). A #140 ezt nem dönti el; a megjegyzés a `DONTESEK.md` DT-F140b sorában áll.
