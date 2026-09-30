# f21p/prompt_biro_v2.md — a döntőbírói prompt kiegészítése (F21 F4 futás, v2)

Dokumentáció, nem megy ki a modellnek. A modellnek csak a két jelölő közötti rész
megy ki, **a `prompt_v1.md` utasításrésze után fűzve** (`eszkozok/karoli_strong/futtat.py`,
`biro_utasitas()`). A v1 (`prompt_biro_v1.md`) megmarad, a futás már nem használja.

Miért v2 (F21.8, a P3 döntései): a v1-ben a döntőbíró újraírhatta a teljes párosítást,
így az A–B egyező linkek is változhattak volna, és a G4 „magas” (két modell egyezése)
elvesztette volna az értelmét. A v2-ben:

- **az A és B egyező linkjei rögzítettek**: a C csak a vitatott magyar szavakról dönt;
- a rögzített linkeket és a vitatott magyar szavakat **a szkript számolja ki és
  írja a versblokk után**, a modellnek nem kell kitalálnia;
- a kimenet sémája ugyanaz, mint az A és B kimenete (teljes, önálló versobjektum), és
  ugyanazon az ötpontos kapun megy át; nincs benne Strong-szám (K5);
- a rögzítést **gép kényszeríti** (`futtat.biro_kenyszer`, hatodik kapupont): a
  C válaszában minden rögzített link szerepel, és a nem vitatott magyar szavak
  állapota (linkjei, betoldás) azonos az A–B egyezővel; eltérés esetén egy újrakérés
  a hibaüzenettel, másodszori eltérésnél `kapuhiba`;
- ahol az A vagy a B kapuhibás maradt, nincs mit rögzíteni: ott a C a teljes
  párosítást adja.

A két válasz megjelölés nélküli modellnévvel („A”, „B”) megy, sorrendjük rögzített.
A futásnapló a döntőbírói utasítás sha256-ját külön rögzíti. Változtatás új fájl
(`prompt_biro_v3.md`), nem ennek módosítása.

<!-- PROMPT-KEZDET -->
DÖNTŐBÍRÓI SZEREP. A fenti feladatot ezúttal döntőbíróként kell elvégezned. Minden versnél a versblokk után két független korábbi megoldást kapsz ugyanarra a párosításra (`A MODELL VÁLASZA` és `B MODELL VÁLASZA`, ugyanabban a JSON-alakban, mint amit neked kell adnod), és mellettük a gép által kiszámolt sorokat:
- `RÖGZÍTETT LINKEK`: azok a `[magyar, eredeti]` párok, amelyekben A és B egyetért. Ezek végleges, NEM vitathatók: a válaszodnak mindegyiket tartalmaznia kell, pontosan így.
- `RÖGZÍTETT BETOLDÁS`: azok a magyar szavak, amelyeket A és B egyaránt betoldásnak vett. Ezek is véglegesek: maradjanak a `betoldas`-ban.
- `VITATOTT MAGYAR SZAVAK`: azok a magyar sorszámok, amelyeknél A és B eltér (más eredeti szóhoz kötötte, vagy az egyik betoldásnak vette, a másik nem). Csak ezekről döntesz.

Mit tegyél:
1. A vitatott magyar szavaknál a magyar szöveg, az eredeti szavak angol tükörfordítása és (ha van) a KJV-támpont alapján döntsd el, melyik megoldás helyes: az A-é, a B-é, vagy ha egyik sem, add meg a helyeset.
2. A nem vitatott magyar szavak párosítását (a rögzített linkek és a rögzített betoldás) ne változtasd meg: ne törölj belőlük, ne adj hozzájuk új linket, és ne vedd át más kötéssel. Ha szerinted valamelyik rögzített link hibás, akkor is változatlanul hagyd, mert azt nem te bírálod.
3. Ha egy vitatott magyar szó mellett rögzített link is áll (A és B egy részében egyetért), az egyező rész szintén marad.
4. Ahol a `RÖGZÍTETT` sorok helyén az áll, hogy nincs rögzítés (mert az egyik vagy mindkét modell válasza gépileg elfogadhatatlan volt, `KAPUHIBA`), ott nincs mihez igazodnod: add meg a teljes párosítást a saját olvasatod szerint, a meglévő (elfogadható) válasz tájékoztató.
5. A két korábbi válasz nem kötelező érvényű a vitatott szavaknál: lehet, hogy mindkettő téves. A döntésed a szövegen múljon, ne azon, melyik válasz a több vagy a magabiztosabb.

A kimeneted ugyanaz, mint a fenti feladatban: KIZÁRÓLAG egy JSON-tömb, versenként egy teljes, önálló objektummal (`vers`, `parok`, `betoldas`, `forditatlan`), a bemenet sorrendjében. Ne a különbséget add meg, hanem a teljes, végleges párosítást: a rögzített részt változatlanul, és benne a vitatott szavakról hozott döntésedet. Ugyanazok a kötelező szabályok érvényesek rá, mint fent (minden magyar sorszám pontosan egyszer, minden eredeti sorszám legalább egyszer, csak létező sorszám, SEMMILYEN Strong-szám a kimenetben). A gép ellenőrzi, hogy a rögzített rész változatlan; eltérés esetén újra kell írnod.
<!-- PROMPT-VÉGE -->
