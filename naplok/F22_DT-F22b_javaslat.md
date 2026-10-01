# DT-F22b (helyőrző) — a 2Mózes promptjának javaslata: névmagyarázat és idióma linkelési konvenciója

*Állapot: a felhasználó döntött (l. 6.); a javaslat 1–5. szakasza az eredeti, változatlan szöveg. A javaslat maga nem módosít promptot, adatot vagy briefet; a `DONTESEK.md`-be a PR merge-e után kerül, a számot a DT-F22b helyőrző helyett a kiosztás adja (F30 helyőrző-szabály). Proveniencia: `scope=manual | forras=ideiglenes szkriptek (nem a repóban) az adat/karoli_strong/parok_1Moz.tsv és a TAHOT-kivonat olvasásával | ts=2026-10-01`. A prompt (`f21p/prompt_v3.md`) befagyasztott, ezért bármelyik opció új prompt-változatot (új hash) és kis regressziós ellenőrzést jelent a 2Mózes futtatása előtt.*

## 1. Kiindulás: az 1Móz régi arany hat eltérése

Az arany halmaz-szabálya: a hármas Strong-összetevőinek mind szerepelniük kell a Károli-kifejezés tokenjeihez linkelt eredeti Strongok között (a többlet link nem bukik).

| Igehely | Károli-kifejezés | Arany | A jelenlegi linkek az arany-összetevőkre | Típus |
|---|---|---|---|---|
| 5:29 | vígasztal | H5146+H5162 | H5162 igen (*vígasztal*, *meg*); a H5146 (Noé) csak a *Noénak*-hoz | névmagyarázat |
| 16:11 | meghallá Isten | H3458 | a H3458 csak az *Ismáelnek*-hez | névmagyarázat |
| 16:13 | látomás | H0410+H7210 | H7210 igen; a H0410 csak az *Istene*-hez | névmagyarázat |
| 13:4 | segítségűl hívá | H7121+H3068 | H7121 igen (*hívá*); a H3068 csak az *Úrnak*-hoz | idióma |
| 14:22 | Felemeltem az én kezemet | H5375+H3027 | H3027 igen; **a H5375 nincs a TAHOT-versben** (az ige H7311) | idióma (l. 4.) |
| 6:17 | élő lélek | H5315+H2416 | a H5315 nincs a versben | aranyhiba (marad) |

Mind a hat sor `magas`/`alacsony` megoszlása: Károli-tokenek 11 magas / 1 alacsony (az alacsony a 13:4 *segítségűl*). Vagyis a két modell egyezett, és mindketten a lexikai (tő-) konvenciót követték.

## 2. Névmagyarázat (5:29, 16:11, 16:13)

*Meghatározás (javasolt):* a Károli-szöveg maga mondja ki, hogy egy név értelmét magyarázza („nevezé … mondván", „nevezd nevét …", „azért nevezé"), és a név az eredetiben a versben áll.

| Opció | A magyarázó szó kötődik… | Az arany-összetevők teljesülése | Ára |
|---|---|---|---|
| **N1 — tő** (jelenlegi) | csak a saját tövéhez | 0/3 vers teljes (5:29 és 16:13 fele, 16:11 semmi) | — |
| **N2 — név** | a névhez (Noé, Ismáel, El-roi) | csak a 16:11 teljesül | a tő elveszne |
| **N3 — mindkettő** | a tövéhez **és** a név szavaihoz | 3/3 teljesül, mert a halmaz-szabály többletet tűr | több link, a név szavához többszörös kötés |

**Javaslat: N3.** Szövegtervezet a promptba (L után, új szabály):
> M. Névmagyarázat. Ha a magyar szöveg egy név értelmét adja („nevezé … mondván: ez vígasztal"), a magyarázó szó a saját eredeti szavához és a név eredeti szavához (szavaihoz) is kötődik. Csak akkor alkalmazd, ha a név ténylegesen áll a versben; egyébként a szokásos szabály érvényes.

Megfogalmazott kizárás: a névvel egy versben álló, de értelmét nem magyarázó szó nem kapja a névlinket.

## 3. Idióma (13:4)

*Meghatározás (javasolt):* olyan állandó szókapcsolat, amelynek jelentése nem a tagok összege, és az eredetiben is kapcsolat áll (*segítségül hív az Úr nevét* ← *qārā' bə-šēm YHWH*).

| Opció | Kötés | Az arany teljesülése |
|---|---|---|
| **I1 — tagonként** (jelenlegi) | minden magyar szó a saját eredeti szavához; a *segítségűl* a *be-* elöljáróhoz (alacsony, S) | a 13:4 nem teljesül |
| **I2 — kifejezés-szint** | az idióma magyar szavai az idióma minden tartalmas eredeti szavához, a tárgy-névvel együtt (*segítségűl hívá* ← H7121 + H8034 + H3068) | teljesül |
| **I3 — fő szó** | csak az igéhez (H7121) | nem teljesül (a H3068 hiányzik) |

**Javaslat: I2**, szűk meghatározással: csak ott, ahol a szótár (BDB/Thayer) is állandó kapcsolatként kezeli, hogy a szabály ne terjedjen vissza a hétköznapi igeragozásra. Szövegtervezet:
> N. Idióma. Ha a magyar szavak állandó szókapcsolatot adnak vissza, amelynek jelentése nem a tagok összege, a kapcsolat szavai az eredeti kapcsolat minden tartalmas szavához kötődnek, a tárgyi névvel együtt; a tagok a saját szavukhoz is megtartják a kötést.

## 4. Amit a döntés előtt tudni kell

1. **A 14:22 nem konvenció-kérdés.** Az arany H5375 (*nāśā'*) nincs a TAHOT-versben (az ige H7311), így semmilyen linkelési szabály nem teljesítheti; ugyanúgy a versben nem álló Strong, mint a 6:17-nél. Az idióma-szabály (N) a H7311+H3027 kötést adná, de az aranyt nem. Javaslat: az 1Móz 14:22 jelölése a 6:17-hez hasonlóan aranyhiba (`f21p/regi_arany_hibas.tsv`), felhasználói döntéssel; ez a javaslat azt a besorolást nem vette át, mert az idióma-típusba tetted.
2. **Az arany nem egységes a három névmagyarázatnál:** a 16:11 csak a nevet (H3458) adja, az 5:29 a nevet és a tövet, a 16:13 a név két alkotóját (El és Roi). Az N3 mindhármat teljesíti, de az arany maga is döntés kérdése.
3. **Mérési veszély:** a halmaz-szabály többletet nem bünteti, ezért az N3 és az I2 az arany-egyezést felfelé viszi akkor is, ha a linkek hasznossága nem nő. A bevezetés előtt külön pontossági ellenőrzés kell a többlet-linkekre (a kizárás nélküli arany-egyezés mellett).
4. **Az eddigi mérések:** az 1Móz 96,9% (188/194) kizárás nélkül; a hat sor módosítás nélkül marad az 1Mózesben, a konvenció a 2Mózes (és az újrafuttatás) promptját érinti.
5. **Hatókör:** hat hely nem elég a szabály általánosításához; az N és az M szabály általános alkalmazásának gyakorisága a 2Mózesben nincs mérve.

## 5. Döntéshez (javaslattal)

| Kérdés | Javaslat |
|---|---|
| Névmagyarázat: tő / név / mindkettő | **mindkettő (N3)** |
| Idióma: tagonként / kifejezés-szint / fő szó | **kifejezés-szint (I2)**, szűk meghatározással |
| 14:22: idióma-eset vagy aranyhiba | **aranyhiba** (a H5375 nincs a versben) |
| Új prompt-változat bevezetése | a 2Mózes futtatása előtt, új hash-sel és kis regressziós ellenőrzéssel |

## 6. Döntés (felhasználó, 2026.10.01, DT-F22b)

| # | Döntés | Következmény |
|---|---|---|
| 1 | Az 1Móz 14:22 és 6:17 **aranyhiba**. | A régi arany egyezése újraszámolva (az alábbi táblában). A `f21p/regi_arany_hibas.tsv` ebben a menetben **nem módosult** (befagyasztott F21-adat; jelenleg csak a 6:17 szerepel benne); a 14:22 felvétele külön kézi lépés. |
| 2 | A `prompt_v3` változatlan marad a 2Mózesre. | Új prompt-változat és új hash nincs; a 2Mózes az 1Mózessel azonos prompttal fut. |
| 3 | Névmagyarázat: a „mindkettő” konvenció (N3) elfogadva, a kikötésekkel (a Károli kimondja a névadást, és a név a versben áll). | Megvalósítás: **későbbi, külön javítómenet** a névadó versekre, nem promptszabály. Felvéve **N-F22 helyőrzőként** (`NYITOTT_FELADATOK.md`). **Az 1Móz 16:11 aranyát (H3458, csak a név) ehhez a konvencióhoz kell igazítani.** |
| 4 | Idióma-szabály: **halasztva**, a szótári állandó-szókapcsolat lista függvényében. | Az I2 (kifejezés-szint) nem épül be; az 1Móz 13:4 az 1Mózesben változatlan marad. |

Az 5. pont (a döntés rögzítése) ez a szakasz; a `DONTESEK.md` a helyőrző-szabály szerint a merge után kap végleges számot.

### Az újraszámolt régi arany egyezés (1Móz, 194 hármas)

*Proveniencia: `scope=manual | forras=ideiglenes szkript (nem a repóban), az f22_elemzes.py régi-arany logikájának ismétlése az adat/karoli_strong/parok_1Moz.tsv és szavak_1Moz.tsv alapján | ts=2026-10-01`. A kizárás nélküli sor egyezik a jelentés 2.2 szakaszával (96,9%; 96,4%; 97,0%).*

| Kizárás | Nevező | Minden link | Csak `magas` link | `magas` tokenekre korlátozva |
|---|---|---|---|---|
| nincs (a mért érték, a jelentés szerint) | 194 | 96,9% (188/194) | 96,4% (187/194) | 97,0% (164/169) |
| csak 6:17 (a jelenlegi `regi_arany_hibas.tsv`, tájékoztató) | 193 | 97,4% (188/193) | 96,9% (187/193) | 97,6% (164/168) |
| **6:17 és 14:22 (DT-F22b)** | **192** | **97,9% (188/192)** | **97,4% (187/192)** | **98,2% (164/167)** |

A két kizárt hármas egyikének sem volt egyező linkje, ezért a számláló (188, 187, 164) nem változik, csak a nevező csökken. A kizárás a DT-F21j i) döntése szerint tájékoztató: a mért érték a kizárás nélküli, a jelentés (`naplok/F22_1Moz_jelentes.md`) 2.2 szakasza ezzel nem módosult.
