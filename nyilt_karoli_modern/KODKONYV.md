# Kódkönyv / Codebook

*Modernizált Károli – Strong / Modernised Károli – Strong*

## `konyvek/NN_Konyv.tsv`

| oszlop / column | érték / value | leírás | description |
|---|---|---|---|
| `osis` |  | A vers OSIS-azonosítója (könyv.fejezet.vers), a Károli-versszámozás szerint. | OSIS verse identifier (book.chapter.verse), in Károli versification. |
| `token` |  | A szó sorszáma a versben (1-től), az 1908-as szöveg szavai szerint; a (osis, token) pár a szó kulcsa. | Position of the word in the verse (from 1), counted on the 1908 text; (osis, token) is the word key. |
| `alak_1908` |  | A szó alakja a Károli 1908-as szövegében. | Word form in the 1908 Károli text. |
| `alak_modern` |  | A szó modernizált alakja; üres, ha a szó a modern szövegből kiesik (l. kieso). | Modernised word form; empty if the word drops out of the modern text (see kieso). |
| `valtozott` | `igen` | A modern alak eltér az 1908-astól, vagy a szó kiesik. | The modern form differs from the 1908 form, or the word drops out. |
| `kieso` | `osszevonva` | A szó egybeíródott a következővel (a kik → akik); a modern alak a gazdaszón áll. | The word merged with the following one (a kik → akik); the modern form is on the host word. |
| `kieso` | `segedige` | Segédigei „vala”, amely a modern múlt időben kiesik (mondja vala → mondta); a gazdaszó az ige. | Auxiliary "vala", dropped in the modern past tense (mondja vala → mondta); the host word is the verb. |
| `gazda_token` |  | Kieső szónál a gazdaszó sorszáma ugyanabban a versben; a kieső szó Strong-párja ehhez a szóhoz tartozik a modern szövegben. | For a dropped word, the position of its host word in the same verse; its Strong pair belongs to that word in the modern text. |
| `bizonytalan` | `igen` | A modern alak szabályos, de a választás szövegkörnyezettől függ (pl. tárgyas vagy alanyi ragozás); a szöveg ezen a szón óvatosan kezelendő. | The modern form is regular, but the choice depends on context (e.g. definite or indefinite conjugation); treat with care. |
| `allapot` | `javaslat` | A sor egy szópár: gépi párosítási javaslat, mért pontossággal (MODSZER.md 5.). | The row is a word pair: a machine alignment proposal with measured accuracy (METHODS.md 5). |
| `allapot` | `betoldas` | A fordító betoldása: a szónak nincs héber vagy görög megfelelője. | Translator's addition: the word has no Hebrew or Greek counterpart. |
| `allapot` | `fuggoben` | A szó párosítása függőben van (kézi döntésre vár); pár nincs. | Alignment of the word is pending (awaiting a manual decision); no pair. |
| `strong` |  | A párosított eredeti szó Strong-száma (H… héber, G… görög), a STEPBible TAHOT/TAGNT szerint; „+” két számot köt össze, ha az eredeti szó összetett. | Strong's number of the aligned source word (H… Hebrew, G… Greek), from STEPBible TAHOT/TAGNT; "+" joins two numbers for a compound source word. |
| `eredeti_token` |  | Az eredeti szó sorszáma a TAHOT/TAGNT versében (a Károli-vers kulcsán). | Position of the source word in the TAHOT/TAGNT verse (keyed to the Károli verse). |
| `kapcsolat` | `szo` | A pár egy eredeti szóhoz köti a magyar szót. | The pair links the Hungarian word to a source word. |
| `kapcsolat` | `morfema` | A pár egy héber előtag- vagy ragmorfémához köti (H9001–H9049: névelő, kötőszó, elöljáró). | The pair links it to a Hebrew prefix or suffix morpheme (H9001–H9049: article, conjunction, preposition). |
| `bizonyossag` | `magas` | Két független nyelvi modell ugyanazt a párt adta (Mózes 1–2. könyve). | Two independent language models gave the same pair (Genesis and Exodus). |
| `bizonyossag` | `alacsony` | Egy nyelvi modell javaslata; a pontosságát a mérés adja meg (MODSZER.md 5.). | Proposal of one language model; its accuracy is given by the measurement (METHODS.md 5). |

## `versek.tsv`

| oszlop / column | érték / value | leírás | description |
|---|---|---|---|
| `osis` |  | A vers OSIS-azonosítója. | OSIS verse identifier. |
| `szoveg_modern` |  | A modernizált vers szövege, írásjelekkel. | Modernised verse text, with punctuation. |
| `valtozott` | `igen` | A vers szövege változott a modernizálásban. | The verse text changed in the modernisation. |
| `valtozott` | `nem` | A vers szövege változatlan. | The verse text is unchanged. |
