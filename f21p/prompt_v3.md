# f21p/prompt_v3.md — a Károli–Strong mérőpilot promptja (v3, előkészítve, NEM futott, NEM befagyasztott)

Dokumentáció, nem megy ki a modellnek. A modellnek csak a két jelölő közötti rész
megy ki (`eszkozok/karoli_strong/bemenet.py`, `prompt_utasitas(<prompt-fájl>)`); a
versblokkok az utasítás után, hívásonként 10 vers. Használja: a regressziós mérés (P3c,
PD13) F3V3 (C) és Sonnet-futása, 200 vers. A futás indítása és a prompt befagyasztása
(sha256) külön felhasználói jóváhagyásra vár; sha256-fájl nincs.

- Tervezés: F21.41, a felhasználó DT21 a–e döntése (PD13). A v2 szerkezete szó szerint
  megmarad (bemenet, feladat, v1 1–4. pont, párosítási szabályok, kötelező szabályok,
  kimenet, két példa). A párosítási szabályok: a `f21p/arany_opus_jegyzetek_v2.md`
  konvenciói (A–J = K1–K10, K = a v1 5. pontja, a TR-szabály, L = K11). A v2-höz képest
  csak a DT21 a–e pontjai változtatnak, más új szabály nincs:
  - **C** (DT21 b, K3 v2): a szabály csak az *'et* + rag esetére szól; a megfelelő nélküli
    magyar tárgyi névmás `betoldas`, nem kötődik az igéhez;
  - **D** (DT21 e, K4 v2): a rag a megfelelő (ugyanarra a személyre utaló) személyragot
    viselő magyar szóra megy, birtokos szerkezetben is;
  - **G** (DT21 a, K7 v2): a kivétel a jegyzet megfogalmazására szűkül (egy eredeti
    igealak többtagú fordítása, ahol a segédige maga az igealak; nem: a *vala*, *fog*,
    *volna* mint segédige, a határozószó, a kötőszó);
  - **L** (új, DT21 c, K11): korrelatív *azt/azért … hogy*: a mutató névmás `betoldas`,
    ha nincs eredetije, a *hogy* a kötőszóra;
  - DT21 d (2Móz 26:13 *is*): a prompt nem változik (az I szabály a v2-é).
  Az illusztráló magyar szerkezetek általánosak; a pilotmintából (`f21p/minta.tsv`) vett
  példa nincs benne.
- A két példa változatlan: 1Móz 1:1 és Ján 1:1. Egyik sincs a `f21p/minta.tsv`-ben
  (metszet: 0, gépi ellenőrzés F21.41); nincs bennük Qere/Ketiv, X-sor, `[nem TR]` token,
  „való”, tárgyi névmás, birtokos rag, korrelatív „azt/azért … hogy”, sem más nyitott
  jelenség (a nyers STEPBible-fájlban ellenőrizve: 1Móz 1:1 mind a 7 sora `=L`, a Ján 1:1
  mind a 17 sora `=NKO`, TR-es). A példa-JSON a v3 szabályaival konzisztens: az A (a
  magyar névelő `betoldas`, a héber H9009 és a görög névelő `forditatlan`), az I (*és* ←
  *ve-*, καί), a C első fele (az *'et* `forditatlan`; magyar névmás nincs), a G feltétele
  (a Ján 1:1 *vala* a külön eredeti igéhez, ἦν, kötődik, tehát nem segédige-betoldás);
  mindkettő átmegy a kapun (kapu.vers_ellenoriz, F21.41). A `{{VERSBLOKK:<igehely>}}`
  helyőrző helyére a `bemenet.versblokk` kimenete kerül.
- A prompt változtatása új fájl (`prompt_v4.md`), nem a v3 módosítása: a futásnapló a
  prompt sha256-ját rögzíti.

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

Párosítási szabályok (ezek döntik el a vitás eseteket):

A. Névelők. A magyar önálló névelő (a, az) mindig `betoldas`. A héber határozott névelő (H9009) és a görög névelő `forditatlan` — kivéve, ha névmásként áll (vonatkozó névmás: aki, amely; önálló „ő, az” jelentés): ilyenkor a megfelelő magyar névmáshoz kösd.
B. Kettéírt Károli-kötőszó és vonatkozó névmás (a mint, a hogy, a miképen, a mely, a ki, a melyben stb.). Ha van eredeti megfelelője (kötőszó, vonatkozó névmás, névmásként álló névelő), a magyar kifejezés MINDKÉT szavát kösd hozzá. Ha a magyar vonatkozó mellékmondat egy eredeti melléknévi igenevet fordít, és külön vonatkozó szó nincs az eredetiben, a vonatkozó szó(k) `betoldas`, az igenév a magyar igéhez kötődik.
C. Tárgyjelölő névmási raggal (héber 'et + tárgyi rag). Az 'et (H0853) `forditatlan`; a magyar névmás (azt, őt, őket, téged stb.) csak a ragra (H90xx) kötődik. Ez a szabály csak az 'et + rag esetére szól. Ha a magyar tárgyi névmásnak (azt, ezt, őt stb.) nincs eredeti megfelelője (nincs 'et + rag, sem más eredeti névmás vagy névmási rag), `betoldas`: ne kösd az igéhez, és ne kösd más szóhoz. (Az igén vagy elöljárón álló névmási ragról a D szabály szól.)
D. Birtokos és névmási ragok (H9020–H9040), görög birtokos névmás (αὐτοῦ, μου stb.). Ahhoz a magyar szóhoz kösd, amelyik a megfelelő személyragot viseli, vagyis amelyiknek a személyragja ugyanarra a személyre utal, mint az eredeti rag (az ő háza: a rag a „háza”-hoz). Ha két személyragos magyar szó áll egymás mellett (birtokos szerkezet, pl. „fia házát” ← „az ő fiának háza”), a rag arra megy, amelyiknek a személyragja a rag személyét jelöli (itt a „fia”), nem a másikra. Ha a magyar a névmást külön is kiteszi (az ő háza, az én atyám, ő vele), a rag a névmáshoz IS kötődik (ugyanaz az eredeti két párban).
E. Különírt igekötő (meg, el, ki, le, fel, be, által, oda, alá stb.): az ige eredetijéhez kötődik, nem `betoldas`.
F. Külön kitett magyar alanyi névmás (én, te, ő, mi, ti, ők), ha az eredetiben nincs külön névmás (az igealak hordozza a személyt): `betoldas`.
G. Segédige (vala, volt, fog, fogunk, van, vannak, volna, lészen), ha az eredetiben nincs külön ige: `betoldas`. Ez az ige mellé tett múlt idejű „vala” (pl. látja vala, jár vala), a jövő idejű „fog” és a feltételes „volna” esetére is áll. Egyetlen kivétel: ha a magyar egyetlen eredeti igealakot többtagú igei szerkezettel ad vissza, és a segédige maga az igealak (idő, szenvedő alak) fordítása (pl. „meg van írva” egy eredeti befejezett szenvedő igére), a szerkezet igei tagjai (igekötő, segédige, igenév) az egy eredeti igéhez kötődnek. A kivétel nem terjed ki a szerkezet melletti határozószóra vagy kötőszóra: azok `betoldas`, ha nincs eredetijük. Ha az eredetiben van külön ige, és a magyar azt segéd- vagy létigével adja vissza, a szó az igéhez kötődik.
H. A héber nyomatékos -āh (H9012) és a paragogikus nun (H9013): `forditatlan`.
I. A héber ve- (H9001, H9002) és a görög καί: ha a magyarban nincs a helyén kötőszó (és, s, pedig, is, de, hogy), `forditatlan` (ne kösd a következő igéhez vagy névszóhoz); ha van, ahhoz a kötőszóhoz kösd.
J. Összeolvadt névelő + elöljáró (pl. בַּ [in the], τῆς): ha Károli „e/ez” mutató névmással adja vissza, a mutató névmás az elöljáró/névelő sorához kötődik; az elöljáró a ragot viselő főnévhez is kötődhet.
K. Az ÚSZ-ben a `[nem TR]` jelölésű eredeti szavak nincsenek benne a Károli alapjául szolgáló szövegben (Textus Receptus): ezek mindig `forditatlan`.
L. Korrelatív mutató névmás a „hogy” előtt („azt … hogy”, „azért … hogy”). Ha a mutató névmásnak (azt, azért) nincs külön eredeti megfelelője, `betoldas`; a „hogy” a kötőszóhoz kötődik (pl. כִּי, ἵνα, ὅτι, ve-). Ha a mutató névmásnak van eredetije (eredeti mutató névmás), ahhoz kösd.

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

{{VERSBLOKK:Ján 1:1}}

Második példa (kimenet):

{"vers":"Ján 1:1","parok":[[1,[1,2]],[2,[3]],[4,[5]],[5,[6]],[7,[8]],[8,[9]],[10,[10,12]],[11,[13]],[12,[14]],[13,[15]],[15,[17]]],"betoldas":[3,6,9,14],"forditatlan":[4,7,11,16]}
<!-- PROMPT-VÉGE -->
