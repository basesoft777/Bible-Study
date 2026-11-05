Feladat (F172, vak ellenőrzés): bibliaversek Károli (1908) szavaihoz kell megjelölnöd a megfelelő eredeti (héber vagy görög) szavakat.

Minden versnél kapod a VERS igehelyét, a KÁROLI számozott szavait, az EREDETI számozott szavait (sorszám, ragozott alak, Strong-szám, angol tükörfordítás [szögletes zárójelben]; a héber elöljárók, kötőszavak, névelők és toldalékok, H9xxx, külön szónak számítanak), és a CÉL sort: a Károli-szavak sorszámait, amelyekről döntened kell. Csak a CÉL szavakról dönts, de a vers egészét olvasd el.

Minden CÉL Károli-szóhoz add meg az összes eredeti szó sorszámát, amelynek megfelel (egy vagy több), vagy üres listát, ha a szónak nincs eredeti megfelelője (betoldás: pl. az önálló magyar névelő, a segédige, Károli magyarázó betoldása). A vitás eseteket az alábbi szabályok döntik el; ezek ugyanazok, amelyek szerint a párosítás készült.

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

Kimenet: egyetlen JSON-objektum a megadott fájlba, semmi más:
{"modell": "<a saját tényleges modellazonosítód, pl. claude-opus-5-5>", "koteg": <köteg száma>, "versek": [{"vers": "<igehely>", "jeloles": [[<Károli-sorszám>, [<eredeti sorszám>, ...]], ...]}, ...]}
- a versek sorrendje a bemeneté; minden vers minden CÉL sorszáma pontosan egyszer szerepel a `jeloles`-ben;
- csak létező eredeti sorszámot írj; Strong-számot ne írj;
- ha bizonytalan vagy, a legvalószínűbb, szövegből megalapozott jelölést add; a bizonytalanságot ne írd a fájlba.
