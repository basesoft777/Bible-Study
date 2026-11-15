# Kódkönyv

*Károli 1908 – Strong szóillesztés*

## `data/parok/NN_Konyv.tsv`

| oszlop | érték | leírás |
|---|---|---|
| `osis` |  | A vers OSIS-azonosítója (könyv.fejezet.vers), a Károli-versszámozás szerint. |
| `token` |  | A magyar szó sorszáma a versben (1-től; az írásjel nem szó). |
| `alak_1908` |  | A magyar szó alakja a Károli 1908-as szövegében. |
| `eredeti_token` |  | Az eredeti szó sorszáma a TAHOT/TAGNT versében, a Károli-vers kulcsán (l. docs/hu/MODSZER.md 3.); a héber előtag és rag külön szónak számít. |
| `strong` |  | Az eredeti szó Strong-száma (H… héber, G… görög) a STEPBible TAHOT/TAGNT szerint; „+” két számot köt össze, ha a forrás egy szóhoz kettőt ad. A modell nem ír Strong-számot: a szám a sorszámból jön. |
| `kapcsolat` | `szo` | A pár egy eredeti szóhoz köti a magyar szót. |
| `kapcsolat` | `morfema` | A pár egy héber előtag- vagy ragmorfémához köti (H9001–H9049: névelő, kötőszó, elöljáró, személyrag). |
| `allapot` | `javaslat` | Gépi párosítási javaslat, mért pontossággal; nem kézzel ellenőrzött pár. |
| `nem_tr` | `igen` | Az eredeti görög szó nem szerepel a Textus Receptusban, amelyet Károli fordított; a Strong-szám a kritikai szöveg alakjáé (l. docs/hu/ISMERT_HIBAK.md). |

## `data/szavak/NN_Konyv.tsv`

| oszlop | érték | leírás |
|---|---|---|
| `osis` |  | A vers OSIS-azonosítója, a Károli-versszámozás szerint. |
| `oldal` | `hu` | Magyar szó (Károli 1908). |
| `oldal` | `er` | Eredeti szó (héber vagy görög, TAHOT/TAGNT); az alakja nincs a csomagban, a sorszáma és a Strong-száma azonosítja. |
| `token` |  | A szó sorszáma a versben, az oldalán belül (1-től). Minden magyar és minden eredeti szó pontosan egy sorban áll. |
| `alak_1908` |  | A magyar szó alakja; az eredeti szónál üres. |
| `allapot` | `parositva` | A szónak van párja a másik oldalon (l. partner_token). |
| `allapot` | `betoldas` | Magyar szó eredeti megfelelő nélkül: a fordító betoldása, önálló névelő, segédige, kitett alanyi névmás. |
| `allapot` | `forditatlan` | Eredeti szó magyar megfelelő nélkül (pl. a héber tárgyjelölő, a névelő, ha a magyar nem fordítja). |
| `allapot` | `fuggoben` | A vers párosítása kézi döntésre vár (a versek megfeleltetése szavanként nem állt össze, vagy a válasz nem ment át a gépi kapun); pár nincs. |
| `partner_token` |  | A pár(ok) sorszáma a másik oldalon, vesszővel elválasztva. |
| `strong` |  | Eredeti szónál a saját Strong-száma; magyar szónál a partnerei Strong-számai „+”-szal fűzve. |

## `data/versek.tsv`

| oszlop | érték | leírás |
|---|---|---|
| `osis` |  | A vers OSIS-azonosítója, a Károli-versszámozás szerint. |
| `szoveg_1908` |  | A vers Károli 1908 szövege, írásjelekkel; a szavak sorszáma ebből számolódik. |

## `data/meres.tsv`

| oszlop | érték | leírás |
|---|---|---|
| `szakasz` | `reteg` | Rétegenkénti (könyvcsoportonkénti) egyezés a vak ellenőrrel: rétegenként egyszerű véletlen minta; Mózes öt könyvében két részminta, a pársúlyukkal összegezve. |
| `szakasz` | `sulyozott` | A rétegek pársúlyával súlyozott becslés (ÓSZ, ÚSZ, összes). |
| `szakasz` | `bontas` | Kapcsolattípus szerinti bontás (tartalmi szó, morféma), leíró. |
| `szakasz` | `hibatipus` | A vak ellenőrtől eltérő párok típus szerint (`<réteg>:<típus>`; n = az eltérések száma a rétegben). |
| `szakasz` | `leiro` | Leíró szám, nem a pontosság része (hianyzo_par: ahol a vak ellenőr több eredeti szót jelölt). |
| `szakasz` | `kalibracio` | A vak ellenőr és a gépi pár egyezése egy korábbi, kézzel összeállított mintával. |
| `szakasz` | `kulso` | Összevetés egy független, Strong-számos Károli-kiadással, a fő szavak párjain (`_haromutas`: az eltérések háromutas ítélete után). |
| `cimke` |  | A sor tárgya: réteg (OSZ_mozes: Mózes öt könyve; OSZ_tortenet: történeti könyvek; OSZ_koltoi: költői könyvek; OSZ_profeta: próféták; USZ_evangelium: evangéliumok és Apostolok cselekedetei; USZ_level: levelek; USZ_jelenesek: Jelenések), csoport vagy hibatípus (folos_par, szomszedos_token, rossz_szo_a_versben, azonos_lexema_mas_elofordulas). |
| `n` |  | A mért párok száma. |
| `x` |  | Az egyező (helyes) párok száma; hibatípusnál az adott típusú eltérések száma. |
| `p` |  | Arány (x / n; a súlyozott soroknál és a Mózes-rétegnél a súlyozott becslés). |
| `also95` |  | A 95%-os konfidencia-intervallum alsó széle. |
| `felso95` |  | A 95%-os konfidencia-intervallum felső széle. |
| `modszer` | `wilson95` | Wilson-intervallum. |
| `modszer` | `retegzett_normal95` | Rétegzett becslés, normál közelítésű intervallum. |
| `modszer` | `retegzett_leiro` | Rétegzett (a réteg teljes súlyával), leíró. |
| `modszer` | `darab` | Darabszám, intervallum nélkül. |
