# Módszer — a modernizált Károli és a Strong-összekapcsolás

*Modernizált Károli – Strong · Logosz-lexikon · adatállapot: 2026-11-01 · DOI: 10.5281/zenodo.24141950*

## 1. Mi ez az adatkészlet

Károli Gáspár fordításának 1908-as szövege mai helyesírással és mai igealakokkal, szavanként összekapcsolva a héber
és görög eredeti szavak Strong-számaival. A szöveg 66 könyvet, 31 158 verset és 599 367 szót tartalmaz. A
modernizálás 64 388 szót (a kieső szavakkal együtt, 4.3) és 21 636 verset érint; a többi szó és vers változatlan.

A modernizált szöveg a projekt saját munkája. A szópárosítás a Károli 1908 szövegén készült, és önálló
adatkészletként is megjelenik (https://doi.org/10.5281/zenodo.24141884). Ez az adatkészlet a kettő összekapcsolása.

## 2. A kiinduló szöveg és a kulcs

A kiinduló szöveg a Károli 1908 közkincs szövege. Minden vers szavakra (tokenekre) bontva áll; egy szót a vers és a
versen belüli sorszáma azonosít. A modernizálás ezt a kulcsot nem változtatja meg: minden modern alak az 1908-as szó
helyén áll. Ezért kapcsolható össze a modern szöveg a párosítással szótár, újrapárosítás és modell nélkül.

## 3. A modernizálás határa

A szerkesztői döntés szerint a modernizálás két dologra terjed ki: a **helyesírásra** és az **igealakokra**. A
szókincs, a szórend, az írásjelek és a fordító betoldásainak jelölése változatlan. Ahol egy alak a határon állt, ott a
szerkesztő mérés után döntött:

- a mutató *e* (*ez*), az *oh*, a *férfiú*, a *leány* és a hasonló szóváltozatok maradnak: ez szókincs, nem helyesírás;
- a *reá* → *rá* és a *néki, nékem, néked, nékik* → *neki, nekem…* csere a helyesírás része;
- a birtokos *-jok/-jök* → *-juk/-jük* része; a *j* nélküli *-ök* → *-ük* csak ott, ahol a szó többes száma
  egyértelműen más (*szívök* → *szívük*); a mély hangrendű *-ok* marad, mert ott a többes számmal egybeesik;
- a puszta *a mi* csak akkor lesz *ami*, ha a szövegkörnyezet vonatkozó névmást mutat (*a mi Istenünk* marad);
- a kötőhangzós régi múlt (*mondotta* → *mondta*, *szólott* → *szólt*) cserélődik; a felszólító *-jál/-jél*
  (*cselekedjél*) és a *-jék* marad, mert a mai nyelvben is élő, választékos változat;
- a jövő idejű *-nd-* (*mondándok*) marad.

## 4. Az eljárás

### 4.1 Helyesírás

Szabálykészlet, szavanként. A fő szabályok: a különírt vonatkozó névmás egybeírása (*a kik* → *akik*, *a mely* →
*amely*; az „a” a következő szóba olvad); a régi betűkapcsolatok (*cz* → *c*, *lyl* → *ll*, *szsz* → *ssz*); a
*néki*-család és a *reá*; a szótagolási régiségek (*dícsér* → *dicsér*); végül egy saját szótári tábla, amely a Károli
szavainak mai szótári alakját adja, és amelynek helyesírási eltéréseit (*miképen* → *miképpen*, *kivül* → *kívül*) a
szabály átveszi. A magyar Hunspell helyesírási szótár csak mérce volt: a szabályok ellenőrzésére futott, a kiadott
szöveget nem befolyásolta.

### 4.2 Igealak

Szabálykészlet a gyakori régi igealakokra (*teremté* → *teremtette*, *monda* → *mondta*, *lőn* → *lett*,
*vagyon* → *van*, *jő* → *jön*), saját igeragozó modullal (rendhagyó tövek, hangkivetés, hangrend). A *vala* két
szerepét a szabály választja szét: a létigei *vala* → *volt*; a segédigei *vala* a múlt idejű igealakba olvad
(*mondja vala* → *mondta*), és a modern szövegből kiesik. A tárgyas és alanyi ragozás választása a régi alakból nem
mindig olvasható ki: ott a szabály a tagmondatban álló határozott tárgyat keresi, és a szót bizonytalannak jelöli.

A ritka és a jegy nélküli régies alakokra a szabály csak jelöltet ad. Ezeket nyelvi modell nézte át, 5
körben, vakon (a modell a szabály jelöltjét nem látta):

1. egy első modell (Claude Sonnet) minden ritka és gyanús alakot;
2. egy második modell (Claude Opus) a vitatott alakokat, ahol a szabály és az első modell eltért;
3–5. a második modell három további körben: két körben a teljes szövegen újra felmért régies alakokat, az utolsóban
   szavanként, a teljes verssel, a szövegkörnyezettől függő eseteket.

A modell válasza önmagában semmit nem írt át. Csere ott történt, ahol legalább két jelölt (a szabály, az első és a
második modell) egyezett, és a tőellenőrzés átengedte: a modern alak egyetlen szó, és megtartja a régi alak
igekötőjét és igetövét, így a modell nem cserélhette másik szóra. Ahol nem volt egyezés, a szó változatlan
maradt. A modellek előfizetésből futottak (Claude Code), a felhasznált token a hívásnaplók szerint: az első
modell 1,42 M, a második 1,48 M.

Néhány alak kézi kivétellistába került, ahol a szabály vagy a szótári tábla hibás alakot adott volna (*gyűl-*,
*dűl-* marad; *érte* névutós névmás, nem ige).

### 4.3 Kiesés és összevonás

Két esetben tűnik el szó a modern szövegből: az egybeírt vonatkozó névmás „a”-ja (11 128 szó) és a segédigei
*vala* (2 618 szó). A kieső szó nem törlődik: saját sorában marad, a `kieso` oszlop jelöli, a `gazda_token`
pedig megadja, melyik szóba olvadt. Ha a kieső szónak Strong-párja van (6 723 ilyen szó), az a pár
megmarad, és a modern szövegben a gazdaszóhoz tartozik. Összevonásnál így mindkét régi szó Strong-száma megmarad.

### 4.4 Önellenőrzés és ellenőrzés

Minden versen gépi önellenőrzés fut: a modern szöveget újra szavakra bontva pontosan a nem kieső szavak modern
alakjait kell adnia, sorrendben, és az írásjelek váza nem változhat. Minden szó kulcsa a táblában van.

A szöveget független ellenőr négy körben vizsgálta, ezek után két javítókör következett. A mérés mintákon (a
Wilson-féle 95%-os intervallumot a kiadás számolja a mért darabszámokból):

- helyesírás: a minta 230 cseréjéből 230 helyes (a hibaarány 95%-os felső határa
  1,6%); a puszta *a mi* 102 elemes ellenőrző halmazán 1 hiba (101/102,
  99,0%);
- igealak: a 120 verses mintán 120 vers hibátlan; a második, 140 verses mintán
  216 csere, ebből 0 hibás (felső határ 1,7%); a független ellenőr friss,
  100 verses mintáján 92 csere, ebből 0 hibás (felső határ 4,0%);
- lefedettség (maradt-e régies igealak): ugyanezen a friss mintán 94,8% (92 csere, 5
  kihagyás; 95%: 88,5–97,8%). Ebből a teljes szövegben kb. 1 560 régies alakban maradt igealak
  becsülhető (95%-os Poisson-sáv kb. 500–3 600). A második minta magasabb lefedettsége torzított, mert a
  későbbi körök éppen a kihagyásait vették célba.

A maradék ismert hibákat az `ISMERT_HIBAK.md` sorolja fel.

## 5. A Strong-párosítás és a pontossága

A szópárosítás nyelvi modellek javaslata a STEPBible TAHOT (héber) és TAGNT (görög) szövegén: minden magyar szóhoz a
modell kijelöli a héber vagy görög szavakat, a Strong-szám ezekből a forrásokból jön, a modell nem írja. Mózes első
két könyvében két független modell párosított; ahol egyeztek, a pár `magas` bizonyosságú (52 844 pár), máshol egy
modell javaslata (`alacsony`, 545 871 pár). Minden pár „javaslat” állapotú.

A pontosságot rétegzett véletlen mintán mértük, vak ellenőrrel, és egy független, Strong-számos Károli-kiadással:

- a teljes párkészlet (mellékszavakkal, morfémákkal) egyezése a vak ellenőrrel: 95,06% (95%: 93,81–96,32%);
- a fő szavak párjai a független forrással összevetve, 2 663 páron: 98,72% (95%: 98,22–99,08%); a
  háromutas ítélet után, amely az eltéréseket a vak ellenőr bevonásával döntötte el, 99,81%;
- a héber előtag- és ragmorfémák párjai: 90,74% (95%: 87,18–94,29%); ezeket a független forrás
  nem jelöli.

## 6. Az összekapcsolás

A modern szöveg és a párosítás összekapcsolása kulcs szerinti illesztés: a vers és a szó sorszáma. Új pár nem
keletkezik, és egy sem vész el. Gépi kapu igazolja: mind a 598 715 pár átkerült, mind a 488 659 párosított
szó kulcsa megvan a modern táblában, azonos 1908-as alakkal; minden modern szó szerepel; a csomag újragenerálva
bájtra azonos. A betoldott (109 914) és a függőben lévő (794) szónak nincs párja.

## 7. Korlátok

- A párosítás gépi javaslat; a pontossága fent, az ismert hibák az `ISMERT_HIBAK.md`-ben.
- A modernizálás nem fordítás és nem revízió: a szókincs és a szórend a Károlié.
- A szövegkörnyezettől függő igealakok egy része bizonytalannak jelölt (2 361 szó).
