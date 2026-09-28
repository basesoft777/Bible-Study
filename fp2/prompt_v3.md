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
