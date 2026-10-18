# KJV_SZOVEG M2 — mérés (#118, `F118_KJV_SZOVEG_BRIEF.md` 4. pont, M2.2)

**Egyeztetett eltérés: új csomag (sha256 `00532b6db1825cb78fd34de2097fc280ce03ee22ef0bdac5243ef4beaca4d447`, 2026-10-17).** A döntések: DT210 1., DT211 (a), DT212 (d), DT213 (a minta és a táblaforma; a `\wj` a `Szöveg_jelolt`-ban `‹…›`).

*proveniencia: scope=KJV_SZOVEG M2 mérés (M-a, M-b, M-c, F19-kérdés) | forras=konkordancia/KJV_teljes_szoveg.tsv sha256=f385295b957ba35cd99351b3ff500fc7d8e4c963fd854581f46b0eff2befe5ce + konkordancia/KJV_Strongs_teljes.tsv + naplok/F19_hianyok.tsv + kjv.zip sha256=00532b6db1825cb78fd34de2097fc280ce03ee22ef0bdac5243ef4beaca4d447 | ts=2026-10-18T15:47:52Z*

Mérőkód: `naplok/KJV_SZOVEG_meres.py` (`python -I`). Nem a generátorban van: a táblákat `split('\t')`-tel olvassa, a nyers zipet közvetlenül, a jelölőszámokat a generátortól függetlenül számolja. A futás kimenete: `naplok/KJV_SZOVEG_meres_kimenet.txt`. A tábla: `konkordancia/KJV_teljes_szoveg.tsv`, 31 218 sor, 8 717 061 bájt. A generátort újrafuttatva **bájtra azonos** táblát kaptam (sha256 `f385295b…`). *Pontosítás (F118.22, az ELLENOR_KJV_SZOVEG ELTÉRÉSE nyomán):* a bájtazonosság az **adatsorokra** (az oszlopfejléc és a 31 218 versor) mindig áll. A fejlécsorokra csak aznap, mert a proveniencia-sor `ts`-e a futás napja. Az importáló ezért írás előtt összeveti a meglévő táblát az újjal (`iras_dontes`): eltérő adatsornál megáll, és felülírni csak a `--felulir` kapcsolóval lehet. Ha csak a `ts` tér el, a meglévő tábla változatlanul marad.

## Eredmény

| Mérés | Elvárás (brief) | Mért | |
|---|---|---|---|
| **M-a** S ⊆ T | igen | igen; \|S ∖ T\| = 0; \|S\| = 31 215, \|T\| = 31 218 | ✔ |
| M-a T ∖ S | az `F19_hianyok.tsv` címke nélküli versei | Mk 9:43, Lk 6:41, Lk 17:36. Ez azonos az `F19_hianyok.tsv` 3 KJV-sorával. Címke nélküli 0. vers nincs (mind a 116 felirat címkés). | ✔ |
| M-a kanonikus versek | 31 102 | 31 102 (v>0) + 116 zsoltárfelirat (v=0); 66 könyv, kanonikus sorrendben | ✔ |
| **M-b** szóegyezés | minden Strong-címkés szó megtalálható, megmagyarázatlan eltérés 0 | 362 399 szóelem: 362 315 pontos, 76 összetett szó, 8 szótöredék-címke; **megmagyarázatlan: 0** | ✔ |
| **M-c** üres `Szöveg` | 0 | 0 (üres `Szöveg_jelolt` is 0) | ✔ |
| M-c vershidak | — | 0 (a nyers forrásban sincs `\v n-m`) | ✔ |
| M-c formai | — | backslash, szóköz az írásjel előtt, dupla szóköz, páratlan `[ ]` vagy `‹ ›`: 0. A `Szöveg` és a `Szöveg_jelolt` szavai egy versben térnek el: 1Jn 2:23, a forrás szerint (DT213 (3), lent) | ✔ |
| M-c kimaradt jelölők | az M0 leltára szerint | a tábla veszteség-sora és a nyers forrás független számolása mind a 9 tételben egyezik (táblázat lent) | ✔ |
| `Elotte` / `Utoirat` | 22 / 14 | 22 (Zsolt 119:1, 9, … 169) / 14 (Róm 16:27, 1Kor 16:24, 2Kor 13:14, Gal 6:18, Ef 6:24, Fil 4:23, Kol 4:18, 1Thessz 5:28, 2Thessz 3:18, 1Tim 6:21, 2Tim 4:22, Tit 3:15, Filem 25, Zsid 13:25) | ✔ |
| jelölt sorok | — | `‹…›` 2 028 vers; `[…]` 14 263 vers; `¶` 2 970 vers (`Szöveg_jelolt`) | — |

Versek könyvenként: a `naplok/KJV_SZOVEG_meres_kimenet.txt` „M-c: versek könyvenként” sora (pl. 1Móz 1 533, Zsolt 2 577 a 116 felirattal, Mt 1 071, Jel 404).

### M-b: a két megmagyarázott osztály

Az első futás 90 nem illeszkedő szóelemet adott. Átnézve mind a forrás szóhatáron belüli címkézéséből jön, a szöveg nem veszít belőle semmit. A mérőkód ezért két osztályt ismer fel. Minden más megmagyarázatlan maradna, és ⛔-t váltana ki. A tételes lista: `naplok/KJV_SZOVEG_szoegyezes_hiany.tsv` (84 sor, a `token_a_szövegben` oszloppal).

| Osztály | db | Mi ez | Példák (a szövegbeli token) |
|---|---|---|---|
| `osszetett_szo` | 76 szóelem | egy írott szót több Strong-címkés rész alkot; a tábla `Angol szó`-i a részek | cannot (16), wherein (10), therein (8), whosoever (6), thereby (6), whereof (4), shewbread, midnight, nothing, likeminded, footstool, goatskins, burdensome, boldly, day's |
| `szoreszlet` | 8 szóelem | a címke csak a szó elejét fedi, a maradék címke nélküli (a nyers forrásban: `\w afrai\|strong="G5399"\w*d`, `\w agains\|strong="G4314"\w*t`) | Lk 8:25 afraid, Ef 6:12 against, Jn 13:20 és Gal 6:8 that, Mk 4:24 given, Lk 7:44 tears, Zsid 3:3 és 7:20 inasmuch |

Az első futás „sorrend” hibái (pl. Zsid 4:6, 8 elem) az összetett szó miatti mohó továbbugrás következményei voltak. A két osztály felismerése után eltűntek.

## Veszteségnapló (DT-F107d (2): mit dob el az importáló)

A tábla `# veszteség:` fejlécsora hordozza, a generátor számolja. A mérés a nyers forrásból függetlenül újraszámolta (66 kanonikus könyv, a lábjegyzeten belüli jelölők nélkül):

| Elem | A tábla veszteség-sora | Nyers forrás | Hová lesz |
|---|---|---|---|
| Strong-címke (`\w … strong=`) | 349 308 | 349 308 | kimarad (a `KJV_Strongs_teljes.tsv`-ben van; DT210, DT126) |
| lábjegyzet (`\f … \f*`) | 6 959 | 6 959 | kimarad (KJV-széljegyzetek) |
| `\p` / `\q1` / `\b` | 4 635 / 2 461 / 209 | ugyanaz | kimarad (bekezdés- és költői tagolás) |
| `\nd` | 6 892 | 6 892 | a jelölés kimarad, a szöveg („LORD”) marad |
| `\tl` | 22 | 22 | a jelölés kimarad (csak az `Elotte`-ben, Zsolt 119) |
| `\wj` | 2 038 | 2 038 | a `Szöveg`-ből kimarad; a `Szöveg_jelolt`-ban `‹…›` (2 028 vers); versen átnyúló lezárás 0 |
| `\add` | 21 510 | 21 510 | a `Szöveg`-ből kimarad; a `Szöveg_jelolt`-ban `[…]`; ebből 7 az utóiratokban, ott a jelölés elvész (DT213 (2)) |
| `¶` | 2 970 | — (karakter) | a `Szöveg`-ből kimarad, a `Szöveg_jelolt` megőrzi |
| könyvfejléc-sor (`\id \h \toc1-3 \mt1 \mt2`) | 398 | 66 × 6 + 2 | kimarad |

**1Jn 2:23 (DT213 (3), nem veszteség, de jelölendő):** a forrásban a vers második fele egyetlen `\add`, és benne szó szerint „[but]” áll. Ez a forrás szerint marad: a `Szöveg`-ben „… the Father: [but] he that acknowledgeth …”, a `Szöveg_jelolt`-ban egymásba ágyazva „[[but] he that acknowledgeth the Son hath the Father also]”. A 66 kanonikus könyvben ez az egyetlen szó szerinti szögletes zárójel. A tábla veszteség-sora is említi, a teszt rögzíti.

## F19-mellékkérdés: érinti-e a `KJV_Strongs_teljes.tsv`-t a `\s1`-hiba?

Az `f19_ebible_import.parse_usfm` a Zsolt 119 21 akrosztichon-fejlécét az előző vers *szövegéhez* fűzi, a 14 páli utóiratot pedig a levél utolsó versééhez (`naplok/KJV_SZOVEG_M0.md` 3. pont). A tábla csak a Strong-címkés szavakat veszi át, ezért az számít, van-e címke a `\s1`-sorokban. Mérve:

- a 66 kanonikus könyv 36 `\s1`-sorában a `strong=` attribútum **0**;
- az érintett 35 vers (Zsolt 119:8, 16 … 168 és a 14 utóiratos vers) 244 táblabeli szava mind illeszkedik a vers saját szövegére (amelyben a fejléc nincs benne); megmagyarázatlan eltérés **0**;
- az M0-ban az F19-generátor az új csomagból bájtra a `KJV_Strongs_teljes.tsv`-t adta.

**Válasz: nem érinti.** A hiba csak az F19 belső `szoveg` mezőjét rontja, és azt a tábla nem írja ki. N-tétel ezért nem kell; a régi táblához és az F19-importálóhoz nem nyúltam.

## Állapot

A tábla `# ÁLLAPOT:` sora: `importált, javaslat`, a fenti mérés összefoglalójával. A felhasználó elfogadása után következik az M3 (`licencek.tsv`, `datasetek.tsv`, `SEMA.md`); ezt ez a menet nem kezdte el.

## M3 — dataset-szabályok (F118.15–F118.16)

- A tábla `# ÁLLAPOT:` sora: `importált, elfogadva (felhasználó, 2026-10-18)`. Újragenerálás után a nem `#` kezdetű sorok (oszlopfejléc + 31 218 adatsor) bájtra azonosak az előzővel (sha256 `4d939e42…`), és csak az ÁLLAPOT-fejlécsor változott.
- `adat/licencek.tsv`: új `KJV_teljes_szoveg` sor (DT210 1.). Állapot `kozkincs` a DT-F33d (a)–(c) szerint: kor, sha256-tal azonosított kiadás, és a kiadó szó szerinti PD-nyilatkozata a zip `copr.htm`-jéből. `kereskedelmi=feltetelesen`, `share_alike=nem`, címke `közkincs`. A CrossWire szövegszintű hozzájárulásának kérdése nyitott, kitöltés nélkül.
- `adat/datasetek.tsv`: négy sor (`bovitett`, `tematikus`, `melyelemzes`, `lexikon_oldal`), `ajanlott`, `elerheto`.
- `adat/SEMA.md` 2.6: a dataset leírása a `KJV_Strongs_teljes` mellett. **Ez a bekezdés tölti be a DT-F107d dataset-README szerepét**: a szabály még nincs a main-en, és a brief `ir` listájában nincs README, ezért új README-fájl nem készült. Benne a nyers zip (elsődleges hely, sha256, méret; **a második példány helye: megadandó**, a felhasználó adja meg), az újrafuttatás és a veszteségnapló.
- Mindhárom fájlba csak hozzáfűzés történt (a #107 párhuzamosan írja őket). Írás előtt összevetettem: az eredeti sorok bájtra változatlanok. Az `eszkozok/ellenoriz.py` kimenete változatlan, a `general.py --cel lexikon --ellenoriz` 0.
