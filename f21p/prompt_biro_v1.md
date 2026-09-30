# f21p/prompt_biro_v1.md — a döntőbírói prompt kiegészítése (F21 F4 futás, v1)

Dokumentáció, nem megy ki a modellnek. A modellnek csak a két jelölő közötti rész
megy ki, **a `prompt_v1.md` utasításrésze után fűzve** (`eszkozok/karoli_strong/futtat.py`,
`biro_utasitas()`): a döntőbíró ugyanazt a feladatot, ugyanazt a kimeneti alakot és
ugyanazokat a kötelező szabályokat kapja, mint a párosító modellek, és ehhez jön a
két korábbi válasz.

- Forrás: a fő brief (`F22_KAROLI_STRONG_BRIEF.md`) 22.3: „C látja A és B válaszát, és
  egyik mellett dönt, vagy saját választ ad”. A fő brief külön döntőbírói promptot nem
  dolgoz ki; ez a minimális változat, amely e mondat szellemét követi (F21.7,
  a jelentésben jelezve).
- A döntőbíró csak azokat a verseket kapja, ahol A és B link-szinten eltér, vagy
  valamelyikük kapuhibás maradt.
- A két válasz megjelölés nélküli modellnévvel („A”, „B”) megy, sorrendjük rögzített; a
  jelölők a versblokk után állnak. A kapuhibás válasz helyén `KAPUHIBA` áll.
- A döntőbíró válasza ugyanazon az ötpontos gépi kapun megy át (egy újrakéréssel).
- A futásnapló a döntőbírói utasítás sha256-ját külön rögzíti.
- Változtatás új fájl (`prompt_biro_v2.md`), nem ennek módosítása.

<!-- PROMPT-KEZDET -->
DÖNTŐBÍRÓI SZEREP. A fenti feladatot ezúttal döntőbíróként kell elvégezned. Minden versnél a versblokk után két független korábbi megoldást is kapsz ugyanarra a párosításra: `A MODELL VÁLASZA` és `B MODELL VÁLASZA`, ugyanabban a JSON-alakban, mint amit neked kell adnod. Ahol az egyik válasz helyén `KAPUHIBA` áll, az a modell nem adott gépileg elfogadható megoldást; ott a másik válaszra és a saját olvasatodra támaszkodj.

A két válasz ott tér el egymástól, ahol valamelyik magyar szót más eredeti szóhoz (vagy máshoz, vagy sehova) kötötte. Ezeket az eltéréseket kell eldöntened:
- Minden vitatott magyar szónál a magyar szöveg, az eredeti szavak angol tükörfordítása és (ha van) a KJV-támpont alapján döntsd el, melyik megoldás helyes; ha egyik sem, add meg a helyes párosítást.
- Ahol A és B egyezik, ne változtass, hacsak nem egyértelműen hibás.
- A két válasz nem kötelező érvényű: lehet, hogy mindkettő téves. A döntésed a szövegen múljon, ne azon, melyik válasz a több vagy a magabiztosabb.

A kimeneted ugyanaz, mint a fenti feladatban: KIZÁRÓLAG egy JSON-tömb, versenként egy teljes, önálló objektummal (`vers`, `parok`, `betoldas`, `forditatlan`), a bemenet sorrendjében. Ne a két válasz különbségét add meg, hanem a teljes, végleges párosítást, és ugyanazok a kötelező szabályok érvényesek rá (minden magyar sorszám pontosan egyszer, minden eredeti sorszám legalább egyszer, csak létező sorszám, Strong-szám nélkül). A két korábbi válaszban szereplő sorszámok ugyanarra a versblokkra vonatkoznak, mint a tiéd.
<!-- PROMPT-VÉGE -->
