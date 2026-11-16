# Útmutató az ellenőrzéshez — Károli 1908 – Strong szópárosítás

## Miről szól?

A Károli-biblia 1908-as szövegének minden szavát párosítottuk a héber, illetve görög eredeti megfelelő szavával, Strong-számokkal együtt. Az adat nyíltan elérhető a Zenodón (doi:10.5281/zenodo.24141883), és a *Journal of Open Humanities Data*-ba cikk készül róla. A párosítást nyelvi modell végezte. A modell csak rámutatott a forrásszóra, a Strong-szám a STEPBible héber és görög adatából jön. A pontosságot eddig szintén gép mérte, ezért kell most emberi szem. Ti ketten egymástól függetlenül, szúrópróbaszerűen nézitek át a mintát. Az eredményetek számként kerül a cikkbe, ti pedig, ha hozzájárultok, név szerint szerepeltek a köszönetnyilvánításban. A munka kb. 3–4 óra, több részletben. Egymással ne egyeztessetek; ha valamiben nem vagytok biztosak, a „bizonytalan” gomb a jó válasz. Mivel részt vesztek a munkában, a folyóiratnál nem lehettek a cikk bírálói.

**A feladat.** Az `ellenorzo.html` 380 tételt mutat, gépen és telefonon is (internet nem kell). **300 szópár**: egy Károli-szóhoz a gép egy héber vagy görög szót rendelt (TAHOT/TAGNT, Strong-számmal). **80 pár nélküli magyar szó**: a gép szerint ennek a szónak nincs eredetije. Mindkettőt a teljes vers ismeretében ítéld meg. Egy magyar szónak több eredetije is lehet, ilyenkor minden kapcsolat külön tétel. A vers többi párját a tétel alján látod.

**Kérjük, a másik ellenőrrel ne egyeztess, és ne nézd meg az ő válaszait.** Csak így mérhető, mennyire egyezik két független ítélet. Kérdésnél a szervezőt kérdezd, ne a másik ellenőrt.

## Mikor helyes, hibás, bizonytalan?

- **Helyes** – a magyar szó (legalább részben) ennek az eredeti szónak a fordítása, az alábbi szabályok szerint. Pár nélküli szónál: valóban nincs eredetije.
- **Hibás** – válaszd ki a hiba típusát is:
  - *rossz forrásszó*: a magyar szónak a vers egy másik eredeti szava felel meg (ha tudod, koppints rá);
  - *hiányzó pár*: ez a pár jó, de a magyar szóhoz még egy eredeti szó is tartozik, és az a párjai között nem szerepel;
  - *fölösleges pár*: a magyar szónak nincs eredetije (betoldás), mégis kapott párt;
  - *egyéb*: írd le a megjegyzésben.
  - Pár nélküli szónál a „Van (hibás)” azt jelenti, hogy a szónak van eredetije, a gép tehát kihagyta.
- **Bizonytalan** – ha a szabályok szerint sem dönthető el, vagy szövegváltozat, illetve Károli szabad fordítása miatt nem látszik a megfelelés. Írj egy mondatot az okáról. Ne ezt válaszd, ha csak lassabb volna eldönteni.

## A párosítás szabályai (röviden)

Ezek szerint készült a párosítás. A tetszés szerinti fordítói ítélet helyett ezeket kérjük alkalmazni.

1. **Névelő.** A magyar önálló névelő (*a, az*) mindig betoldás. A héber névelő (H9009) és a görög névelő nem kap magyar párt, kivéve, ha névmásként áll (*aki, amely*).
2. **Igekötő.** A különírt igekötő (*meg, el, ki, le, fel, által…*) az ige eredetijéhez tartozik.
3. **Segédige és alanyi névmás.** A *vala, volt, fog, van, volna, lészen* betoldás, ha az eredetiben nincs külön ige. Kivétel: ha a magyar egy eredeti igealakot többtagú szerkezettel ad vissza, a szerkezet minden igei tagja az egy igéhez tartozik. A külön kitett *én, te, ő…* betoldás, ha a személyt csak az igealak hordozza.
4. **Ragok.** A héber birtokos és névmási rag (H9020–H9040) ahhoz a magyar szóhoz tartozik, amelynek a személyragja ugyanarra a személyre utal. Ha a magyar a névmást külön is kiteszi (*az ő háza*), a névmás is ugyanahhoz a raghoz tartozik. Az *'et* (H0853) nem kap párt; a mellette álló tárgyi névmás (*azt, őt*) a ragjához tartozik.
5. **Kötőszó.** A héber *ve-* és a görög *καί* csak akkor kap párt, ha a magyarban a helyén kötőszó áll (*és, s, pedig, is, de, hogy*).
6. **[nem TR].** Az ÚSZ-ben a szürkén szedett, *[nem TR]* jelű szó nincs benne a Károli alapszövegében, ezért nem kaphat párt.

## Példák a mintán kívülről (a tárgyalt pár a mai adatban)

| Vers | Magyar szó | Pár | Ítélet és ok |
|---|---|---|---|
| 1Móz 1:1 *teremté Isten **az** eget* | az | nincs | **helyes**: a magyar névelő betoldás; a héber הַ sem kap párt (1.) |
| Mt 4:10 *Eredj **el** Sátán* | el | ὕπαγε (G5217) | **helyes**: a különírt igekötő az igéhez tartozik (2.) |
| Mt 4:10 *mert **meg van írva*** | meg, van, írva | mindhárom: γέγραπται (G1125) | **helyes**: többszavas magyar szerkezet egy eredeti igealakra (3.) |
| 1Móz 1:2 *és setétség **vala** a mélység színén* | vala | nincs | **helyes**: Károli betoldása (névmondat, nincs ige). Ugyanebben a versben *puszta vala* ← הָיְתָה (H1961) szintén helyes pár, mert ott van eredeti ige |
| 2Sám 14:10 *hozd **ide** előmbe* | ide | nincs | **helyes**: Károli magyarázó betoldása |
| 1Móz 4:4 *az **ő** juhainak* | ő | וֹ (H9023, „his”) | **helyes**: a külön kitett névmás és a *juhainak* is a ragot kapja (4.) |
| Péld 3:18 ***Életnek** fája ez* | Életnek | עֵץ (H6086, „tree”) | **hibás, rossz forrásszó**: az *Életnek* a חַיִּים (H2416, „life”) fordítása, a *fája* pedig a עֵץ-é; a gép felcserélte őket |

## Gyakorlati tudnivalók

- **Indítás.** Nyisd meg az `ellenorzo.html`-t egy böngészőben, és add meg a neved, mindig ugyanazt. A tételek sorrendje ellenőrönként más.
- **Mentés, több részletben.** A munka bármikor abbahagyható és folytatható: minden kattintás után automatikusan ment. A mentés azonban ehhez a böngészőhöz és ehhez az eszközhöz kötött. Ne dolgozz privát vagy inkognitóablakban, mert annak bezárásakor a mentés elvész. 50 kész tételenként az oldal felajánl egy biztonsági exportot; nem kötelező, de érdemes elfogadni.
- **Eszközváltás.** A régi eszközön „Mentés / export” → **Exportálás**. Az újon nyisd meg ugyanezt az oldalt, add meg ugyanazt a nevet, majd „Mentés / export” → **Betöltés**, és válaszd ki a fájlt. Ha mindkét helyen vannak válaszaid, tételenként a később módosított marad meg. Más mintához tartozó fájlt az oldal nem tölt be.
- **Tippek.** Ha egy magyar szóra koppintasz, látod a párjait. Ha egy eredeti szóra koppintasz, látod a Strong-számát és a jelentését. A pontozott aláhúzás pár nélküli eredeti szót jelöl.
- **Alaktan.** A héber kód a Macula/OSHB jelölése: pl. *Ncmsa* = köznév, hímnem, egyes szám, abszolút állapot; *Vqp3ms* = ige, qal, perfectum, E/3 hímnem; *Sp3ms* = névmási rag, E/3 hímnem; *R* = elöljáró; *C* = kötőszó; *Td* = névelő. A görög kód Robinson-féle: pl. *V-PAP-NSM* = ige, praesens activum participium, alanyeset, egyes szám, hímnem.
- **Leadás.** Ha végeztél, a „Mentés / export” gombbal letöltöd a `<neved>_valaszok.json` fájlt; ezt küldd el a szervezőnek. Ha a letöltés nem indul el, ugyanott kimásolhatod a szöveget.
- **Becsült idő.** Szópárnál átlagosan kb. fél perc, pár nélküli szónál 15–20 másodperc: összesen **kb. 3–4 óra**. A névelők és a kötőszók gyorsan mennek, a ragos és többszavas esetek lassabban. Érdemes több, legfeljebb egyórás részletben dolgozni.
