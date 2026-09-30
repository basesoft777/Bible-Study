# FP2 prompt v3 — FORDITAS_STILUSPROBA_FP2_BRIEF.md v2, 2. lépés

*A v2 (`naplok/FORDITAS_P_prompt_v2.md`) szó szerinti másolata, kiegészítve az alábbi
stílusblokkal. A v2 egyetlen része sem módosult — a diff a `naplok/FP2_felmeres.md`
„2. lépés — v2→v3 diff” szakaszában. Viszonyítási alapként a brief a jóváhagyott G1941
„természetes hű” mintát javasolja; ilyen **nem létezik** a repóban (a `#7` sora,
`FELADATOK.md`, a v3-stílusdöntést még nyitva jelzi) — ezt a hiányt itt dokumentálom,
és pótlás nélkül haladok tovább.*

Te egy ógörög szótári szócikket (Thayer's Greek Lexicon) fordítasz magyarra. A forrás
angol nyelvű, héber/görög idézetekkel. KÖVESD PONTOSAN az alábbi szabályt (`adat/SEMA.md`
2.5, a `forditas_hu` mező szabálya, szó szerint idézve):

> A jelentés hű magyar fordítása — jelentésenként egyszer. Csak azt mondja, amit a
> szótár: a rövidítések feloldva (bizonytalan feloldásnál változatlanul hagyva), a
> bibliai helyek Károli-rövidítéssel; a forrás héber/görög idézetei változatlanok;
> betoldás, kiemelés és formázás nincs, számozás csak ha a forrásban is van.

További kötelező szabályok:

- A szövegkiadás-jelzeteket (`L`, `T`, `Tr`, `WH`, `Rec.`, és más kritikai-apparátus
  sziglák, pl. `R`, `G`) VÁLTOZATLANUL hagyd — ezeket ne fordítsd, ne oldd fel.
- A görög és héber betűs szakaszokat szó szerint, változatlanul másold át (a zárójeles
  átírásokat is, ha a forrás tartalmaz ilyet).
- Ne adj hozzá magyarázatot, zárójeles kiegészítést, kiemelést, Markdown-formázást
  (`*`, `_`, `#`, `**`) vagy kiejtési átírást, amit a forrás nem tartalmaz.
- Számozást csak akkor használj, ha a forrás is használ (a forrás saját 1., 2., a., b.
  tagolását megtartod, nem vezetsz be újat).
- Ha egy rövidítés feloldása bizonytalan (nincs az alábbi terminológiai listában, és a
  szövegkörnyezetből sem egyértelmű), hagyd a rövidítést változatlanul a fordításban, és
  nevezd meg a `bizonytalan_feloldasok` listában.

## Kiegészítő szabályok (v2)

1. A szócikk fejléce kötelező: a `G<szám> —` előtag, a görög címszó és minden nyelvtani
   adat (ragozás, igeidők, alakok, LXX-megfelelő) változatlan sorrendben szerepel. Ne
   kezdd a fordítást a jelentésnél.
2. Az `1 aorist`, `2 aorist`, `2 future` stb. magyarul `1. aorisztosz`, `2. aorisztosz`,
   `2. jövő idő` (sorszámnév, a jóváhagyott G1941-fordítás szerint); ez nyelvtani
   megjelölés, nem a szócikk jelentés-számozása, azzal ne keverd.
3. Az `A. V.` és `R. V.` utáni idézet angol bibliafordításból vett idézet: maradjon
   angolul, és ne helyettesítsd Károli-szöveggel vagy „Károli:” jelöléssel.
4. A `from X down` fordítása: „X-tól kezdve”, soha nem „lefelé”.
5. Könyv- és folyóiratcímeket (pl. `Studien und Kritiken`, `The Bible Doctrine of Man`)
   ne fordíts le.
6. A forrás görög és héber szavait akkor is betűre változatlanul hagyd, ha hibásnak vagy
   ékezet nélkülinek látszanak; ne javítsd őket, és ne tégy latin betűs végződést
   közvetlenül görög vagy héber szó után (`πνεῦμα-nak` helyes, `πνεῦμαnak` és `πνεῦμαti`
   hibás).

## Stílus: természetes hű

- A jelentéstartalom pontos: nincs kihagyás, nincs betoldás.
- A mondatszerkezet mai magyar, nem tükörfordítás. Az angol szórendet, az *of*-láncokat
  és a szenvedő szerkezeteket magyarosan oldd fel.
- Kerüld az archaizmust és a régies bibliai fordulatokat, kivéve, ha a szócikk éppen egy
  ilyen kifejezést tárgyal.
- Görög és héber szavak, Strong-számok, igehelyek, rövidítések és forráshivatkozások
  változatlanul maradnak, a v2 szabályai szerint.
- A terminológia kifejezéseit kötelezően használd.

## Kiegészítő szabályok (v4)

1. Az idézőjeleket és az idézett szerzőt tartsd meg. Ha a forrás mást idéz (pl.
   Bretschneidert), az idézet a fordításban is idézőjelben álljon, a hivatkozással együtt.
2. A jelentésszám (1., 2.) előtt álló bevezető mondat legyen teljes magyar mondat
   („Jelentése … eszerint:”), ne csonka szerkezet.
3. Az *equivalent to* fordítása „=” vagy „vagyis”, ne „megegyezik …-val”.
4. A könyvneveket a folyó szövegben írd ki („Márk evangéliuma”, „a Zsidókhoz írt levél”).
   Rövidítés csak igehelyben álljon, Károli-rövidítéssel.
5. Az *ff* / *f* magyarul „kk.” / „k.”
6. Az elosztó értelmű számokat tedd egyértelművé: *once in Matthew and Luke* →
   „egyszer-egyszer”.
7. A szerzőnevek egységes alakban álljanak (Philón, Josephus, Tertullianus, Plutarkhosz).
   Ha van szerzőnév-sor a terminológiai listában, az az irányadó.
8. Magyar mondatszerkezetet használj: az angol mellékmondat-láncot bontsd magyar
   mondatokra, de tartalmat ne hagyj el, és ne told be.

### Példapár (G26, részlet) — a fenti szabályok alkalmazása

Forrás (angol):

G26 — ἀγάπη (ης, ἡ, a purely Biblical and ecclesiastical word (for Wyttenbach, following Reiske's conjecture, long ago restored ἀγαπήσων in place of ἀγάπης, ὧν in Plutarch, sympos. quaestt. 7, 6, 3 (vol. viii., p. 835, Reiske edition)). Secular authors from (Aristotle), Plutarch on used ἀγάπησις. "The Sept. use ἀγάπη for אַהֲבָה, Song of Solomon 2:4, 5, 7; Song of Solomon 3:5, 10; Song of Solomon 5:8; Song of Solomon 7:6; Song of Solomon 8:4, 6, 7; ("It is noticeable that the word first makes its appearance as a current term in the Song of Solomon; — certainly no undesigned evidence respecting the idea which the Alexandrian LXX translators had of the love in this Song" (Zezschwitz, Profangraec. u. Biblical Sprachgeist, p. 63)); Jer 2:2; Ecc 9:1, Ecc 9:6; (2Sa 13:15). It occurs besides in Wis. 3:9 Wis. 6:19. In Philo and Josephus, I do not remember to have met with it. Nor is it found in the N. T. in Acts, Mark, or James; it occurs only once in Matthew and Luke, twice in Hebrews and Revelation, but frequently in the writings of Paul, John, Peter, Jude" (Bretschn. Lex. under the word); (Philo, deus immut. § 14). In signification it follows the verb ἀγαπάω; consequently it denotes

Célfordítás:

G26 — ἀγάπη, -ης, ἡ; tisztán bibliai és egyházi szó. (Plutarkhosznál, a Sympos. quaest. 7, 6, 3 helyén, Reiske-kiadás VIII. kötet, 835. o., ugyanis Wyttenbach már régen, Reiske sejtését követve, az ἀγάπης, ὧν olvasat helyére ἀγαπήσων alakot állított vissza.) A világi szerzők (Arisztotelésztől), Plutarkhosztól kezdve az ἀγάπησις alakot használták. „A Septuaginta az ἀγάπη szóval adja vissza az אַהֲבָה szót: Én 2:4, 5, 7; Én 3:5, 10; Én 5:8; Én 7:6; Én 8:4, 6, 7 (»Figyelemre méltó, hogy a szó bevett kifejezésként először az Énekek énekében bukkan fel. Ez bizonyosan nem véletlen, és elárulja, hogyan értették az alexandriai Septuaginta-fordítók az Énekben megénekelt szeretetet.« [Zezschwitz, Profangraec. u. bibl. Sprachgeist, 63. o.]); Jer 2:2; Préd 9:1, Préd 9:6; (2Sám 13:15). Előfordul még a Bölcs 3:9 és a Bölcs 6:19 helyen. Philónnál és Josephusnál nem emlékszem, hogy találkoztam volna vele. Az Újszövetségben az Apostolok cselekedetei, Márk evangéliuma és Jakab levele nem használja. Máté és Lukács evangéliumában egyszer-egyszer, a Zsidókhoz írt levélben és a Jelenések könyvében kétszer-kétszer fordul elő, Pál, János, Péter és Júdás írásaiban viszont gyakori.” (Bretschneider, Lexikon, a címszónál); (Philón, Deus immut. 14. §). Jelentése az ἀγαπάω igét követi, eszerint:

## Ideiglenes terminológia (kötelező megfeleltetés, amíg a 4a élesíti a saját tábláját)

{{TERMINOLOGIA}}

## Károli-rövidítéslista (a bibliai könyvek angol rövidítése → Károli-rövidítés)

{{KAROLI_TABLA}}

## Bemenet

Strong-szám: {{STRONG}}{{DARAB_MEGJEGYZES}}

Forrás (Thayer, angol):

{{FORRAS_SZOVEG}}

## Kimenet

KIZÁRÓLAG a következő JSON-sémájú választ add, semmi mást (sem Markdown code fence,
sem magyarázat a JSON előtt/után):

```json
{"strong": "<a fenti Strong-szám>", "forditas_hu": "<a hű magyar fordítás>", "bizonytalan_feloldasok": ["<rövidítés, ha van bizonytalan feloldás>"]}
```
