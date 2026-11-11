# Akadémiai jelöltek a három vitatott ponthoz (F183)

Dátum: 2026-11-11. Modell: claude-sonnet-5-5. Csak OpenAlex és Crossref eredményei szerepelnek; a DOAB REST-végpont (`https://directory.doabooks.org/rest/search?query=...`, két lekérdezés és két curl-próba) minden hívásra **HTTP 403**-at adott, ezért DOAB-találat nincs. Az absztraktokat a Crossref/OpenAlex adta; teljes szöveget egyiknél sem olvastam, ezért ahol az absztrakt nem említ valamit, azt nem állítom. Az OpenAlex-lekérdezések alapformája: `https://api.openalex.org/works?search=<kifejezés>&per-page=8`; a Crossref-é: `https://api.crossref.org/works?query=<kifejezés>&rows=8`.

## 1. Az 1Móz 8:21 hatóköre (a 3:17 földátok visszavonása-e)

**Eredmény: a kérdésről szóló, lektorált forrást nem találtam.** A 8:21 / qll–ʾrr / 5:29 kombinációra egyik API sem hozott olyan művet, amelynek absztraktja ezt a kérdést tárgyalná. Nem töltöm ki témaközeli anyaggal.

Csak jelzés-szintű nyomok (nem jelöltek):
- Morrison, Andrew: *The Contribution of the 'Cursed Ground' Motif to the Structure and Theme of Genesis 1-11*, TREN, DOI 10.2986/tren.023-0183. A cím pontosan a kérdéskörbe vág, de **disszertáció (nem lektorált folyóirat/kiadó), absztrakt és év nincs az API-ban**, nem olvastam. Ítélet: csak a címe alapján témába vágó; szöveg nélkül nem használható.
- Carr, David M.: „Precursors to the Flood Narrative (Gen 6:5–9:17)", in *The Formation of Genesis 1-11*, Oxford UP 2020, 141–177, DOI 10.1093/oso/9780190062545.003.0007. Az absztrakt a 8:21-et nem említi. Ítélet: csak a témáról (forrásrétegek, l. a 3. pontot).
- Hess, Richard S.: „Lamech in the Genealogies of Genesis", *Bulletin for Biblical Research* 1 (1991) 21–25, DOI 10.2307/26422205 (Crossref; absztrakt nincs). Lektorált, de a cím a Lámekh-genealógiákról szól; az 5:29 földátok-reményének és a 8:21-nek a kapcsolatáról nem tudok állítani. Ítélet: csak a témáról.

Lekérdezések (2026-11-11): `https://api.openalex.org/works?search=Genesis 8:21 curse ground`; `...search=Noah 5:29 curse ground Genesis 8:21`; `...search=Genesis 8:21 lifting of the curse on the ground flood`; `...search=cursed ground motif Genesis 5:29 Noah comfort curse`; `https://api.crossref.org/works?query=Genesis 8:21 curse ground Noah`; `...query=cursed ground motif Genesis 3:17 4:11 5:29 8:21 structure primeval history`; `...query=I will never again curse the ground Genesis 8:21 qll arr` (zaj, használhatatlan).

## 2. Örökölt bűn vagy terjedő következmény a Gen 1–11-ben

**Eredmény: közvetlenül a kérdésről szóló, lektorált forrást nem találtam.** Három témaközeli mű van, mindegyik „csak a témáról".

1. Mulzac, Kenneth D.: „The Theological Character of Gen 1-11 (The Primeval History)", *Journal of Asia Adventist Seminary* 3/1 (2000) 35, DOI 10.63201/mwpt2221. Lektorált folyóirat, nyílt elérés: https://journals.aiias.edu/jaas/article/download/423/378. Az OpenAlex-absztrakt csak a Gen 1–11 kutatástörténeti besorolásait sorolja (előtörténet, J/P megoszlás, Noth, Rendtorff), a bűn terjedéséről/öröklődéséről nem szól. Ítélet: csak a témáról; a teljes szöveg (OA) elolvasása után lehet eldönteni, hasznos-e.
2. Faro, Ingrid: „Defining Evil from the Hebrew Text of Genesis", *New Blackfriars* 105/6 (2024) 594–609, DOI 10.1017/nbf.2024.50 (nem nyílt). Lektorált. Az absztrakt szerint a רע-tő előfordulásait követi végig a Genezisben, és a rosszat a teremtési és szövetségi jó romlásaként írja le, nem a jó hiányaként. A bűn öröklődéséről vagy terjedéséről nem szól. Ítélet: csak a témáról (lexikai rokon, de más kérdés).
3. Gnuse, Robert: „A Process Theological Interpretation of the Primeval History in Genesis 2–11", *Horizons* 29/1 (2002) 23–41, DOI 10.1017/s0360966900009701. Lektorált. Az absztrakt Isten fejlődő, folyamat-teológiai szerepéről szól a J-előtörténetben. Ítélet: csak a témáról.

Lekérdezések (2026-11-11): `https://api.openalex.org/works?search=spread of sin Genesis 1-11`; `...search=original sin Genesis 3 Hebrew Bible`; `...search=Genesis 1-11 sin judgment grace Westermann Primeval history`; `https://api.crossref.org/works?query=spread of sin Genesis 1-11 original sin`; `...query=inherited guilt Genesis 3 Hebrew Bible Fall interpretation Old Testament sin spreading`; `...query=Genesis 1-11 sin escalation Cain Lamech flood Babel theme`. (Egy Crossref-találat, Wright, David: „Sin (Hebrew Bible/Old Testament)", *Oxford Bibliographies in Biblical Studies*, 2013, DOI 10.1093/obo/9780195393361-0158, absztrakt nélkül; a tartalmát nem láttam, ezért nem jelölt.)

## 3. Forrásrétegek: J (átok, föld) szemben P (שחת, חמס) az özönvíz-elbeszélésben

**Eredmény: van használható, lektorált forrás a flood-elbeszélés forráskritikai megosztásáról, de a konkrét szókincs-megoszlást (שחת/חמס a P-ben, átok/föld a J-ben) egyik absztrakt sem nevezi meg**, ezt a szövegben kell ellenőrizni.

1. **Carr, David M.: „Precursors to the Flood Narrative (Gen 6:5–9:17)"**, in *The Formation of Genesis 1-11*, Oxford University Press 2020, 141–177. DOI https://doi.org/10.1093/oso/9780190062545.003.0007. Lektorált (tudományos kiadó, könyvfejezet); nem nyílt (OpenAlex: closed). Absztrakt, saját szavakkal: a nem-P özönvíz-elbeszélés önálló, pre-P forrásként keletkezett, nem a P kiegészítéseként; mindkét változat mezopotámiai hagyományra épült (Atrahaszisz, Gilgames XI), és a P hatást is vett a nem-P-től; a mai 6:5–9:17 a P és a nem-P összeolvasztása utólagos koordináló kiegészítésekkel. Ítélet: **igen** a flood J/nem-P és P szerinti megosztásáról; a חמס/שחת szókincsről az absztrakt hallgat. Lekérdezés: `https://api.crossref.org/works?query=Carr Formation of Genesis 1-11 flood story non-P`; részletek: `https://api.crossref.org/works/10.1093/oso/9780190062545.003.0007`. 2026-11-11.
2. **Carr, David M.: „The Priestly Primeval History and Conflation of P and Non-P"**, in *The Formation of Genesis 1-11*, Oxford UP 2020, 250–264. DOI https://doi.org/10.1093/oso/9780190062545.003.0010. Lektorált, nem nyílt. Absztrakt: a Gen 1–11 három P-szintje (Toledot-könyv; P-forrás teljes özönvíz-elbeszéléssel és a 10. fejezettel; végül a P és nem-P összeolvasztása P-keretben). Ítélet: **igen** a P-réteg kereteiről; a szókincsről nem szól az absztrakt. Lekérdezés: `https://api.crossref.org/works/10.1093/oso/9780190062545.003.0010`. 2026-11-11. (A J-oldalhoz: ugyanő, „The Non-P Primeval History", 223–249, DOI 10.1093/oso/9780190062545.003.0009; az absztrakt szerint az önálló nem-P előtörténet Éden–testvér–apa-fiú történetekre épül, a flood későbbi kiterjesztés. Ítélet: igen a J-oldalra, szókincs nélkül.)
3. **Berman, Joshua A.: „Source Criticism and Its Biases: The Flood Narrative of Genesis 6–9"**, Oxford University Press 2017 (Oxford Scholarship Online fejezet; a Crossref a kötetcímet nem adja meg), DOI https://doi.org/10.1093/acprof:oso/9780190658809.003.0014. Lektorált (tudományos kiadó), nem nyílt. Absztrakt: bírálja a flood-szétosztás forráskritikai paradigmáját, nyolc módszertani hibát lát benne, a Gilgames XI-re és a chiasztikus szerkezetre hivatkozik. Ítélet: **csak részben**: ugyanarról a flood-szétosztásról szól, de ellenvélemény, a J/P-szókincset nem adja; ellenpontnak használható.

Lekérdezések (2026-11-11): `https://api.openalex.org/works?search=composition of the flood narrative Yahwist Priestly` (zaj: Römer, Schmid áttekintések); `https://api.crossref.org/works?query=flood narrative Priestly corruption violence source criticism`; `...query=J and P flood narrative Genesis 6-9 composition`; `...query=Priestly flood hamas shachat Genesis 6:11 corrupt violence`; `...query=Genesis 1-11 primeval history sin and grace Westermann Gen 3-11`.

## Jelentés
- 1. pont: nincs jelölt; a kérdésről szóló lektorált forrás nem található ezekben az API-kban (a Morrison TREN-disszertáció csak nyom).
- 2. pont: nincs közvetlen találat; a legjobb témaközeli Mulzac (JAAS 2000, nyílt), csak a témáról.
- 3. pont: legjobb Carr, *The Formation of Genesis 1-11* (OUP 2020), 7. fejezet (Gen 6:5–9:17); ellenpont Berman 2017.
- DOAB: HTTP 403, nem használható.
