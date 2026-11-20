# JOHD-anyagok lektori szempontrendszere (v1, 2026-11-17)

*Kézi forrás. A `johd-lektor` subagent (`.claude/agents/johd-lektor.md`) e szerint dolgozik; az első lektorkör (Fable, 2026-11-17) szerint átírt kézirat: F175.J9.*

*Szigorú, „Reviewer 2” szemlélet: a lektor egy szkeptikus JOHD-bíráló szemével olvas, aki keresi a gyenge pontot, és csak azt fogadja el, amit az anyag vagy az adat alátámaszt. Udvariaskodás nincs; minden kifogás konkrét helyre mutat, idézettel.*

**Anyagok:** a JOHD-kézirat (`kozlemeny/data_paper/karoli_strong_kezirat_en.md`, a magyar csak összevetésre), a kísérőlevél (`kozlemeny/data_paper/johd_cover_letter_en.md`), és a kéziratban hivatkozott emberi validáció terve (a validációs készlet mappája, kozlemeny/data_paper/validacio, ha már a main-en van). A számokat és az állításokat a repó adatából és kódjából kell ellenőrizni, nem a kézirat szavára.

## A. Megfelelés a JOHD-nek
1. A data paper sablonja: Overview, Method (Steps, Sampling strategy, Quality control), Dataset Description (minden kötelező mező), Reuse Potential.
2. A szóhatár (1000–1500), a hivatkozási stílus, a kötelező nyilatkozatok (MI, finanszírozás, érdekütközés, adat-elérhetőség).
3. A kísérőlevél: tartalmazza-e a mentességi kérelmet és a bíráló-kizárást, és megfelel-e a műfajnak.

## B. Az adatkészlet hozzáférhetősége
4. Tartós azonosító (concept DOI), licenc (CC BY 4.0), formátum, verzió, kódkönyv: egyértelmű-e, és egyezik-e a Zenodóval és a csomaggal.
5. A forrásadatok (TAHOT, TAGNT, Károli 1908) licence és forrásmegjelölése rendben van-e.

## C. Módszer és megismételhetőség
6. Pontosan leírja-e a modell szerepét: a bemenetet (számozott szavak, Strong-szám, glossza), a kimenetet (csak sorszámpárok), a Strong-szám programozott hozzárendelését, és a KJV fejlesztési mondatát.
7. A determinizmus: a rögzített kimenet és a determinisztikus utólagos lépések; ki van-e mondva, mi nem ismételhető.
8. A konvenciók (névelő, segédige, alanyi névmás; 1:n és n:1) indokoltak és érthetők-e egy nem magyar bírálónak.
9. A gépi kapuk: mit ellenőriztek, és ez le van-e írva.

## D. Minőségmérés
10. A mintavétel (rétegzés, méret, CI) korrekt-e; a 95,06% definíciója egyértelmű-e.
11. A gépi bíráló (vak modell-ellenőr) érvényessége: elismeri-e a kézirat a korlátját, és az emberi validáció ezt kezeli-e.
12. A zárt, független kiadás: egyezésként, nem mérceként szerepel-e (98,72%); kimondja-e, hogy nem ellenőrizhető.
13. Az emberi validáció terve: elég-e a minta, megfelelő-e a kappa és a modell–ember egyezés, kezeli-e a szabály szerinti eseteket.

## E. Állítások és korlátok
14. Minden szám és állítás alátámasztott-e az adattal (szúrópróba legalább 5 számon). Nincs-e túlzás (elsőség, „pontos”, „teljes”).
15. A korlátok (Limitations) őszinték és teljesek-e: gépi bíráló, egy modell, konvenciók, zárt összevetés, nem megismételhető futás.

## F. Újrafelhasználhatóság
16. A Reuse Potential konkrét és hihető-e, nemzetközi olvasónak is. A motívumlexikon-mondat nem reklám-e, és nem utal-e kereskedelmi célra.

## G. MI-etika és átláthatóság
17. A COPE / Ubiquity elvárásai: az MI nem szerző, a használat jelölve van, a szerző felelőssége kimondva; a második modell semleges mondata megfelelő-e.

## H. Nyelv és érthetőség
18. Egy nem magyar, digitális bölcsész bíráló számára érthető-e (Károli, Strong-szám, magyar helyesírás-modernizálás). Tömör, pontos, egységes terminológiájú-e.

## Kimenet
- **Ítélet:** accept / minor revision / major revision / reject, egy mondatos indoklással.
- **Pontszám** szempontonként (1–5), egy-két mondat bizonyítékkal: a kézirat idézete és/vagy az adat/kód helye.
- **Kötelező javítások** számozott listája, súlyossági sorrendben, mindegyikhez konkrét javaslattal.
- **Ajánlott javítások**, külön.
- **Az 5 legvalószínűbb bírálói kifogás** és a hozzájuk tartozó megelőző válasz.
- **Amit nem tudott ellenőrizni**, és miért.
