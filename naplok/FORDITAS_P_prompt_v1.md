# FORDITAS_P_prompt_v1 — FORDITAS_PILOT_BRIEF.md FP2, fordítói prompt

*Ezt a fájlt az `eszkozok/fordit.py` szó szerint olvassa be, és a `{{...}}` jelölőket
tölti ki szócikkenként/darabonként. Kézzel szerkeszthető (prompt-verzió: emeld a fájl
nevében is, ha a szöveg érdemben változik, l. G7 gyorsítótár-kulcs).*

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
