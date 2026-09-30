# f21p/prompt_v1.md — a Károli–Strong mérőpilot promptja (v1)

Dokumentáció, nem megy ki a modellnek. A modellnek csak a két jelölő közötti rész
megy ki (`eszkozok/karoli_strong/bemenet.py`, `prompt_utasitas()`); a versblokkok
(`bemenet.versblokk`) az utasítás után, hívásonként 10 vers.

- Tervezés: F21 brief P0.3 és F22 brief 22.1. A modell csak sorszámokat ír; a
  Strong-számot a mérőszkript veszi a TAHOT/TAGNT-ből.
- A két példa (1Móz 1:1, Mt 1:1) nincs a `f21p/minta.tsv`-ben. A példabemenet nem
  kézzel beírt: a `{{VERSBLOKK:<igehely>}}` helyőrző helyére a `bemenet.versblokk`
  kimenete kerül (a héber/görög alakok így pontosan az adatból jönnek). Az önteszt
  (`python eszkozok/karoli_strong/kapu.py --onteszt`) ellenőrzi, hogy a példakimenet
  átmegy a kapun.
- A prompt változtatása új fájl (`prompt_v2.md`), nem a v1 módosítása: a
  futásnapló a prompt sha256-ját rögzíti.

<!-- PROMPT-KEZDET -->
Feladat: bibliaversek magyar (Károli 1908) szavait kell párosítanod az eredeti héber vagy görög szavakkal, szó-szinten.

Minden versnél ezt kapod:
- `VERS`: az igehely;
- `KÁROLI (számozott szavak)`: a magyar vers szavai 1-től sorszámozva (az írásjel nem szó);
- `EREDETI (számozott szavak)`: az eredeti szöveg szavai 1-től sorszámozva, szórendben: sorszám, ragozott alak, Strong-szám, angol tükörfordítás [szögletes zárójelben]. A héber elöljárók, kötőszavak, névelők és toldalékok (H9xxx számúak) külön szónak számítanak és külön sorszámot kapnak;
- `KJV-TÁMPONT` (csak néhány versnél): az angol KJV-szöveg Strong-címkékkel. Ez csak segítség: megmutatja, melyik angol szó melyik eredeti szónak felel meg. A döntés a magyar szövegen múlik.

A Strong-számok a bemenetben csak tájékoztatásul állnak. A kimenetedben SEMMILYEN Strong-szám nem szerepelhet (nem írhatsz H1234 vagy G1234 alakú karakterláncot): csak sorszámokat írj.

Amit versenként meg kell adnod:

1. `parok`: a magyar szó sorszáma és a hozzá tartozó eredeti sorszámok listája: `[magyar, [eredeti, eredeti, ...]]`.
   - Egy magyar szó több eredeti szóhoz is tartozhat (pl. a *Kezdetben* az elöljáró és a főnév együtt).
   - Egy eredeti szó több magyar szóhoz is tartozhat (ha a magyar két szóval fordítja). Ilyenkor az eredeti sorszám több párban is szerepel.
   - A magyar és az eredeti szórend eltérhet; a sorszám a szó helye a versen belül, nem a fontossága.
2. Nyelvtani előtagok és toldalékok (H9xxx): ha a magyarban raggal, névutóval vagy kötőszóval jelennek meg, ahhoz a magyar szóhoz tartoznak, amelyiken a rag áll, vagy amelyik a kötőszó (az *és* a héber *ve-* előtaggal párosul). Ha a magyarban nincs nyoma, `forditatlan`.
3. `betoldas`: az olyan magyar szavak sorszámai, amelyeknek nincs eredeti megfelelőjük: az önálló magyar névelő (*a*, *az*), a segédige (pl. *vala*, *lőn*, ha az eredetiben nincs külön szó), a Károli magyarázó betoldása.
4. `forditatlan`: az olyan eredeti szavak sorszámai, amelyeknek nincs magyar megfelelőjük: pl. a tárgyjelölő *'et* (H0853), a héber határozott névelő (H9009) és a görög névelő, ha a magyar önálló névelője `betoldas`-ba került, vagy ha a magyarban nincs névelő. Ha az eredeti névelő névmásként áll (pl. *aki*, *a ki*), kösd a megfelelő magyar szóhoz.
5. Az ÚSZ-ben a `[nem TR]` jelölésű eredeti szavak nincsenek benne a Károli alapjául szolgáló szövegben (Textus Receptus): ezek mindig `forditatlan`.

Kötelező szabályok (egy gép ellenőrzi őket; hibás válasz esetén újra kell írnod):
- Minden magyar sorszám PONTOSAN EGYSZER szerepel: vagy a `parok` bal oldalán, vagy a `betoldas`-ban.
- Minden eredeti sorszám LEGALÁBB EGYSZER szerepel: vagy a `parok` jobb oldalán, vagy a `forditatlan`-ban.
- Csak létező sorszámot használj.
- Egy verset mindig egészében dolgozz fel; egyet se hagyj ki, és a válasz sorrendje a bemeneté legyen.
- Ne találj ki párosítást: ha nem biztos, a legvalószínűbb, szövegből megalapozott párosítást add meg; a KJV-támpont nélküli verseknél is csak az angol tükörfordításra és a szövegre támaszkodj.

Kimenet: KIZÁRÓLAG egy JSON-tömb, versenként egy objektummal, semmi más szöveg (se magyarázat, se markdown-kerítés). Az objektum alakja:

{"vers":"<igehely a bemenetből>","parok":[[magyar,[eredeti,...]],...],"betoldas":[magyar,...],"forditatlan":[eredeti,...]}

Üres lista megengedett (`[]`).

Első példa (bemenet):

{{VERSBLOKK:1Móz 1:1}}

Első példa (kimenet):

{"vers":"1Móz 1:1","parok":[[1,[1,2]],[2,[3]],[3,[4]],[5,[7]],[6,[8]],[8,[11]]],"betoldas":[4,7],"forditatlan":[5,6,9,10]}

Második példa (bemenet):

{{VERSBLOKK:Mt 1:1}}

Második példa (kimenet):

{"vers":"Mt 1:1","parok":[[1,[3]],[2,[4]],[3,[6]],[4,[5]],[5,[8]],[6,[7]],[7,[2]],[9,[1]]],"betoldas":[8],"forditatlan":[]}
<!-- PROMPT-VÉGE -->
