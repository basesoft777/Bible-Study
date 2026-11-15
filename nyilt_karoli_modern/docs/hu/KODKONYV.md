# Kódkönyv

*Modernizált Károli – Strong*

## `data/konyvek/NN_Konyv.tsv`

| oszlop | érték | leírás |
|---|---|---|
| `osis` |  | A vers OSIS-azonosítója (könyv.fejezet.vers), a Károli-versszámozás szerint. |
| `token` |  | A szó sorszáma a versben (1-től), az 1908-as szöveg szavai szerint; a (osis, token) pár a szó kulcsa. |
| `alak_1908` |  | A szó alakja a Károli 1908-as szövegében. |
| `alak_modern` |  | A szó modernizált alakja; üres, ha a szó a modern szövegből kiesik (l. kieso). |
| `valtozott` | `igen` | A modern alak eltér az 1908-astól, vagy a szó kiesik. |
| `kieso` | `osszevonva` | A szó egybeíródott a következővel (a kik → akik); a modern alak a gazdaszón áll. |
| `kieso` | `segedige` | Segédigei „vala”, amely a modern múlt időben kiesik (mondja vala → mondta); a gazdaszó az ige. |
| `gazda_token` |  | Kieső szónál a gazdaszó sorszáma ugyanabban a versben; a kieső szó Strong-párja ehhez a szóhoz tartozik a modern szövegben. |
| `bizonytalan` | `igen` | A modern alak szabályos, de a választás szövegkörnyezettől függ (pl. tárgyas vagy alanyi ragozás); a szöveg ezen a szón óvatosan kezelendő. |
| `allapot` | `javaslat` | A sor egy szópár: gépi párosítási javaslat, mért pontossággal (docs/hu/MODSZER.md 5.). |
| `allapot` | `betoldas` | A fordító betoldása: a szónak nincs héber vagy görög megfelelője. |
| `allapot` | `fuggoben` | A szó párosítása függőben van (kézi döntésre vár); pár nincs. |
| `strong` |  | A párosított eredeti szó Strong-száma (H… héber, G… görög), a STEPBible TAHOT/TAGNT szerint; „+” két számot köt össze, ha az eredeti szó összetett. |
| `eredeti_token` |  | Az eredeti szó sorszáma a TAHOT/TAGNT versében (a Károli-vers kulcsán). |
| `kapcsolat` | `szo` | A pár egy eredeti szóhoz köti a magyar szót. |
| `kapcsolat` | `morfema` | A pár egy héber előtag- vagy ragmorfémához köti (H9001–H9049: névelő, kötőszó, elöljáró). |

## `data/versek.tsv`

| oszlop | érték | leírás |
|---|---|---|
| `osis` |  | A vers OSIS-azonosítója. |
| `szoveg_modern` |  | A modernizált vers szövege, írásjelekkel. |
| `valtozott` | `igen` | A vers szövege változott a modernizálásban. |
| `valtozott` | `nem` | A vers szövege változatlan. |
