# f21p/prompt_v2.md — a Károli–Strong mérőpilot promptja (v2, előkészítve, NEM futott)

Dokumentáció, nem megy ki a modellnek. A modellnek csak a két jelölő közötti rész
megy ki (`eszkozok/karoli_strong/bemenet.py`, `prompt_utasitas(PROMPT_V2_UT)`); a
versblokkok az utasítás után, hívásonként 10 vers. Használja: a `futtat.py` F3V2
futása (C modell, 200 vers, kimenet `f21p/valaszok/F3V2.jsonl`). A futás indítása
külön jóváhagyásra vár (a workflow és a `f21p/futtatas.txt` változatlan).

- Tervezés: F21.12 felhasználói döntés. A v1 szerkezete megmarad (bemenet, feladat,
  kötelező szabályok, kimenet, két példa); új a „Párosítási szabályok” szakasz: a
  `f21p/arany_opus_jegyzetek.md` 2. szakaszának tíz konvenciója szabályként
  (K1–K10 sorrendben, a prompt A–J pontja; a K pont a v1 TR-szabálya). A konvenciók szabályként, nem példa-túltöltéssel; az
  illusztráló magyar szerkezetek általánosak, a pilotmintából (`f21p/minta.tsv`) nem
  vett példa nincs benne.
- A két példa (1Móz 1:1, Mt 1:1) ugyanaz, mint a v1-ben; nincs a `f21p/minta.tsv`-ben,
  és a kimenetük a tíz szabálynak is megfelel. A `{{VERSBLOKK:<igehely>}}` helyőrző
  helyére a `bemenet.versblokk` kimenete kerül.
- A prompt változtatása új fájl (`prompt_v3.md`), nem a v2 módosítása: a futásnapló a
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

1. `parok`: a magyar szó sorszáma és a hozzá tartozó eredeti sorszámok listája: `[magyar, [eredeti, eredeti, ...]]`. Egy magyar szó több eredeti szóhoz, egy eredeti szó több magyar szóhoz is tartozhat (ilyenkor az eredeti sorszám több párban szerepel). A sorszám a szó helye a versen belül.
2. `betoldas`: az olyan magyar szavak sorszámai, amelyeknek nincs eredeti megfelelőjük.
3. `forditatlan`: az olyan eredeti szavak sorszámai, amelyeknek nincs magyar megfelelőjük.

Párosítási szabályok (ezek döntik el a vitás eseteket):

A. Névelők. A magyar önálló névelő (a, az) mindig `betoldas`. A héber határozott névelő (H9009) és a görög névelő `forditatlan` — kivéve, ha névmásként áll (vonatkozó névmás: aki, amely; önálló „ő, az” jelentés): ilyenkor a megfelelő magyar névmáshoz kösd.
B. Kettéírt Károli-kötőszó és vonatkozó névmás (a mint, a hogy, a miképen, a mely, a ki, a melyben stb.). Ha van eredeti megfelelője (kötőszó, vonatkozó névmás, névmásként álló névelő), a magyar kifejezés MINDKÉT szavát kösd hozzá. Ha a magyar vonatkozó mellékmondat egy eredeti melléknévi igenevet fordít, és külön vonatkozó szó nincs az eredetiben, a vonatkozó szó(k) `betoldas`, az igenév a magyar igéhez kötődik.
C. Tárgyjelölő névmási raggal (héber 'et + tárgyi rag). Az 'et (H0853) `forditatlan`; a magyar névmás (azt, őt, őket, téged stb.) csak a ragra (H90xx) kötődik.
D. Birtokos és névmási ragok (H9020–H9040), görög birtokos névmás (αὐτοῦ, μου stb.). Ahhoz a magyar szóhoz kösd, amelyik a személyragot viseli (az ő háza: a rag a „háza”-hoz); ha a magyar a névmást külön is kiteszi (az ő háza, az én atyám, ő vele), a rag a névmáshoz IS kötődik (ugyanaz az eredeti két párban).
E. Különírt igekötő (meg, el, ki, le, fel, be, által, oda, alá stb.): az ige eredetijéhez kötődik, nem `betoldas`.
F. Külön kitett magyar alanyi névmás (én, te, ő, mi, ti, ők), ha az eredetiben nincs külön névmás (az igealak hordozza a személyt): `betoldas`.
G. Segédige (vala, volt, fog, fogunk, van, vannak, volna, lészen), ha az eredetiben nincs külön ige: `betoldas`. Kivétel: a többtagú igei szerkezet (pl. meg van írva) minden tagja az egy eredeti igéhez kötődik.
H. A héber nyomatékos -āh (H9012) és a paragogikus nun (H9013): `forditatlan`.
I. A héber ve- (H9001, H9002) és a görög καί: ha a magyarban nincs a helyén kötőszó (és, s, pedig, is, de, hogy), `forditatlan` (ne kösd a következő igéhez vagy névszóhoz); ha van, ahhoz a kötőszóhoz kösd.
J. Összeolvadt névelő + elöljáró (pl. בַּ [in the], τῆς): ha Károli „e/ez” mutató névmással adja vissza, a mutató névmás az elöljáró/névelő sorához kötődik; az elöljáró a ragot viselő főnévhez is kötődhet.
K. Az ÚSZ-ben a `[nem TR]` jelölésű eredeti szavak nincsenek benne a Károli alapjául szolgáló szövegben (Textus Receptus): ezek mindig `forditatlan`.

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
