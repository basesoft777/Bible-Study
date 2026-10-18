# KJV_SZOVEG M1 — kis minta (#118, `F118_KJV_SZOVEG_BRIEF.md` 4. pont, M1)

**Jóváhagyva (DT213, felhasználó, 2026-10-18):** „a minta jóváhagyva; 1. Elotte/Utoirat marad; 2. olvasós alakban; 3. az 1Jn 2:23 a forrás szerint, veszteségnaplóban említve; 4. a \wj a Szöveg_jelolt-ban ‹…› jelöléssel; 5. a feliratok 0. versként. Mehet az M2.” A 3. pont mintája a döntés szerinti, `‹…›`-es `\wj`-jelöléssel újragenerálva (F118.11); a minta-versek elvárt értékei az `eszkozok/teszt_kjv_szoveg_import.py`-ban rögzítve.

**Egyeztetett eltérés: új csomag (sha256 `00532b6db1825cb78fd34de2097fc280ce03ee22ef0bdac5243ef4beaca4d447`, 2026-10-17).** A döntések (felhasználó, 2026-10-18): DT210 1., DT211 (a), DT212 (d) második példánnyal (`DONTESEK.md`). Előzmény: `naplok/KJV_SZOVEG_M0.md`.

Az importáló az `eszkozok/kjv_szoveg_import.py`, a mintát a `naplok/KJV_SZOVEG_M1_minta.py` állítja elő (`python -I`, a zip kibontás nélkül, `zipfile`-lal). A teljes tábla **nem** került a `konkordancia/`-ba, mert az az M2. A próbafutás a scratchpadbe ment, a repón kívülre. Az egységtesztek az `eszkozok/teszt_kjv_szoveg_import.py`-ban vannak (19 teszt, szintetikus USFM-en, OK). A minta-versek rögzített elvárt értékei a ⛔ jóváhagyás után kerülnek a tesztbe.

## 1. A táblaforma élőben: az `Elotte` és az `Utoirat` oszlop

Öt oszlop: `Igehely` · `Szöveg` · `Szöveg_jelolt` · `Elotte` · `Utoirat`. A két új oszlopban összesen 36 nem üres cella van: 22 `Elotte` (a Zsolt 119 akrosztichon-fejlécei) és 14 `Utoirat` (a páli utóiratok, Róm 16:27 … Zsid 13:25). Minden más sorban a két oszlop üres.

| `Igehely` | `Szöveg` (rövidítve) | `Elotte` | `Utoirat` |
|---|---|---|---|
| `Psa.119.1` | Blessed are the undefiled in the way, … | `א ALEPH.` | |
| `Psa.119.8` | I will keep thy statutes: O forsake me not utterly. | *(üres; az F19-logika ide fűzte volna a „ב BETH.”-et)* | |
| `Psa.119.9` | Wherewithal shall a young man cleanse his way? … | `ב BETH.` | |
| `Rom.16.27` | To God only wise, be glory through Jesus Christ for ever. Amen. | | `Written to the Romans from Corinthus, and sent by Phebe servant of the church at Cenchrea.` |

## 2. Táblaforma-kérdések a ⛔-hez

1. **Az `Elotte`/`Utoirat` oszlop** marad-e (javaslat: igen), vagy a 36 `\s1`-sor kimaradjon, és csak a veszteségnapló számolja?
2. **Az `Elotte`/`Utoirat` olvasószöveg-alakú.** A 14 utóiratban 7 `\add` áll (pl. „\add and sent\add*”), ezek jelölése ott elvész, és a `# veszteség:` fejlécsor ezt külön számolja. Alternatíva: a két oszlop a jelölt alakot hordozza (`[and sent]`). Javaslat: maradjon az olvasószöveg.
3. **Az 1Jn 2:23 szó szerinti szögletes zárójele** (a minta utolsó verse). Itt a forrás maga írja a „[but]” szót egy `\add`-on belül (a KJV hagyományos írásmódja). A `Szöveg`-ben ezért egy `[but]` áll, a `Szöveg_jelolt`-ban pedig egymásba ágyazott zárójel: `[[but] he that … also]`. A 66 kanonikus könyvben ez az egyetlen szó szerinti `[`/`]` (a zip többi részében még 6 ilyen sor van az apokrifokban és 17 az előszóban). Opciók: (a) a `[…]` konvenció marad, az 1Jn 2:23 dokumentált kivétel (a tesztben rögzítve); (b) az `\add` a `Szöveg_jelolt`-ban más jelet kap (pl. `⸤…⸥` vagy `{…}`), amely a forrásban nem fordul elő. Javaslat: (a), mert egyetlen vers, és a forrás hű. **Döntés: a forrás szerint, a veszteségnaplóban említve.**
4. **`\wj` (Jézus szavai, 2 038)**: a jelölés mindkét szövegmezőből kimarad (M0, 2. pont). A három címke nélküli vers közül a Mk 9:43 és a Lk 6:41 teljes egészében `\wj`, `\w`-címke nélkül, ezért címke nélküliek. A ⛔ kérheti, hogy a `Szöveg_jelolt` jelölje (pl. `‹…›`). Javaslat: maradjon jelöletlen. **Döntés (DT213 (4)): a `Szöveg_jelolt`-ban `‹…›`**; minden vers önállóan zárt jelölést kap (versen átnyúló `\wj` a forrásban nincs, a lezárás számlálója 0).
5. **A zsoltárfelirat 0. versként** saját sort kap (`Psa.3.0`), mint a `KJV_Strongs_teljes.tsv`-ben. Javaslat: így marad.

## 3. A minta (a brief M1-listája, plusz egy páli utóirat és az 1Jn 2:23)

Mindegyik versnél mind a négy szövegmező, alatta a vers nyers USFM-szövege a forrásból (lábjegyzettel és a vers utáni tagoló- és `\s1`-sorokkal).

<!-- proveniencia: scope=KJV_SZOVEG M1 minta (16 vers) + épség a teljes, memóriabeli kimeneten | forras=kjv.zip sha256=00532b6db1825cb78fd34de2097fc280ce03ee22ef0bdac5243ef4beaca4d447 | ts=2026-10-18T15:43:13Z -->

#### `Gen.1.1`

| mező | érték |
|---|---|
| `Szöveg` | In the beginning God created the heaven and the earth. |
| `Szöveg_jelolt` | In the beginning God created the heaven and the earth. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 1 In the \w beginning|strong="H7225"\w* \w God|strong="H0430"\w* \w created|strong="H1254"\w* the \w heaven|strong="H8064"\w* \w and|strong="H0853"\w* the \w earth|strong="H0776"\w*.
```

#### `Gen.1.2`

| mező | érték |
|---|---|
| `Szöveg` | And the earth was without form, and void; and darkness was upon the face of the deep. And the Spirit of God moved upon the face of the waters. |
| `Szöveg_jelolt` | And the earth was without form, and void; and darkness [was] upon the face of the deep. And the Spirit of God moved upon the face of the waters. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 2 And the \w earth|strong="H0776"\w* \w was|strong="H1961"\w* without \w form|strong="H8414"\w*, and \w void|strong="H0922"\w*; and \w darkness|strong="H2822"\w* \add was\add* upon the \w face|strong="H6440"\w* of the \w deep|strong="H8415"\w*. And the \w Spirit|strong="H7307"\w* of \w God|strong="H0430"\w* \w moved|strong="H7363"\w* \w upon|strong="H5921"\w* the \w face|strong="H6440"\w* of the \w waters|strong="H4325"\w*.
\p
```

#### `Gen.1.3`

| mező | érték |
|---|---|
| `Szöveg` | And God said, Let there be light: and there was light. |
| `Szöveg_jelolt` | And God said, Let there be light: and there was light. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 3 And \w God|strong="H0430"\w* \w said|strong="H0559"\w*, Let there \w be|strong="H1961"\w* \w light|strong="H0216"\w*: and there was \w light|strong="H0216"\w*.
```

#### `Psa.3.0`

| mező | érték |
|---|---|
| `Szöveg` | A Psalm of David, when he fled from Absalom his son. |
| `Szöveg_jelolt` | A Psalm of David, when he fled from Absalom his son. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\d A \w Psalm|strong="H4210"\w* of \w David|strong="H1732"\w*, when he \w fled|strong="H1272"\w* \w from|strong="H6440"\w* \w Absalom|strong="H0053"\w* his \w son|strong="H1121"\w*.
```

#### `Psa.3.1`

| mező | érték |
|---|---|
| `Szöveg` | LORD, how are they increased that trouble me! many are they that rise up against me. |
| `Szöveg_jelolt` | LORD, how are they increased that trouble me! many [are] they that rise up against me. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 1  \nd \+w LORD|strong="H3068"\+w*\nd*, how are they \w increased|strong="H7231"\w* that \w trouble|strong="H6862"\w* me! \w many|strong="H7227"\w* \add are\add* they that rise \w up|strong="H6965"\w* against me.
\q1
```

#### `Psa.3.2`

| mező | érték |
|---|---|
| `Szöveg` | Many there be which say of my soul, There is no help for him in God. Selah. |
| `Szöveg_jelolt` | Many [there be] which say of my soul, [There is] no help for him in God. Selah. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 2 \w Many|strong="H7227"\w* \add there be\add* which \w say|strong="H0559"\w* of my \w soul|strong="H5315"\w*, \add There is\add* no \w help|strong="H3444"\w* for him in \w God|strong="H0430"\w*. \w Selah|strong="H5542"\w*.
\q1
```

#### `Psa.119.1`

| mező | érték |
|---|---|
| `Szöveg` | Blessed are the undefiled in the way, who walk in the law of the LORD. |
| `Szöveg_jelolt` | Blessed [are] the undefiled in the way, who walk in the law of the LORD. |
| `Elotte` | א ALEPH. |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 1 \w Blessed|strong="H0835"\w* \add are\add* the \w undefiled|strong="H8549"\w* in the \w way|strong="H1870"\w*, who \w walk|strong="H1980"\w* in the \w law|strong="H8451"\w* of the \nd \+w LORD|strong="H3068"\+w*\nd*.\f + \fr 119.1 \ft undefiled: or, perfect, or, sincere\f*
\q1
```

#### `Psa.119.8`

| mező | érték |
|---|---|
| `Szöveg` | I will keep thy statutes: O forsake me not utterly. |
| `Szöveg_jelolt` | I will keep thy statutes: O forsake me not utterly. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 8 I will \w keep|strong="H8104"\w* thy \w statutes|strong="H2706"\w*: O \w forsake|strong="H5800"\w* me not \w utterly|strong="H3966"\w*.
\s1 \tl  ב BETH.\tl*
\q1
```

#### `Psa.119.9`

| mező | érték |
|---|---|
| `Szöveg` | Wherewithal shall a young man cleanse his way? by taking heed thereto according to thy word. |
| `Szöveg_jelolt` | Wherewithal shall a young man cleanse his way? by taking heed [thereto] according to thy word. |
| `Elotte` | ב BETH. |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 9 Wherewithal shall a young \w man|strong="H5288"\w* \w cleanse|strong="H2135"\w* his \w way|strong="H0734"\w*? by taking \w heed|strong="H8104"\w* \add thereto\add* according to thy \w word|strong="H1697"\w*.
\q1
```

#### `Mat.1.1`

| mező | érték |
|---|---|
| `Szöveg` | The book of the generation of Jesus Christ, the son of David, the son of Abraham. |
| `Szöveg_jelolt` | The book of the generation of Jesus Christ, the son of David, the son of Abraham. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 1 The \w book|strong="G0976"\w* of the \w generation|strong="G1078"\w* of \w Jesus|strong="G2424"\w* \w Christ|strong="G5547"\w*, the \w son|strong="G5207"\w* of \w David|strong="G1138"\w*, the \w son|strong="G5207"\w* of \w Abraham|strong="G0011"\w*.
```

#### `Rev.22.21`

| mező | érték |
|---|---|
| `Szöveg` | The grace of our Lord Jesus Christ be with you all. Amen. |
| `Szöveg_jelolt` | The grace of our Lord Jesus Christ [be] with you all. Amen. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 21 The \w grace|strong="G5485"\w* of \w our|strong="G2257"\w* \w Lord|strong="G2962"\w* \w Jesus|strong="G2424"\w* \w Christ|strong="G5547"\w* \add be\add* \w with|strong="G3326"\w* \w you|strong="G5216"\w* \w all|strong="G3956"\w*. \w Amen|strong="G0281"\w*.
```

#### `Mrk.9.43`

| mező | érték |
|---|---|
| `Szöveg` | And if thy hand offend thee, cut it off: it is better for thee to enter into life maimed, than having two hands to go into hell, into the fire that never shall be quenched: |
| `Szöveg_jelolt` | ‹And if thy hand offend thee, cut it off: it is better for thee to enter into life maimed, than having two hands to go into hell, into the fire that never shall be quenched:› |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 43 \wj And if thy hand offend thee, cut it off: it is better for thee to enter into life maimed, than having two hands to go into hell, into the fire that never shall be quenched:\wj*
```

#### `Luk.6.41`

| mező | érték |
|---|---|
| `Szöveg` | And why beholdest thou the mote that is in thy brother’s eye, but perceivest not the beam that is in thine own eye? |
| `Szöveg_jelolt` | ‹And why beholdest thou the mote that is in thy brother’s eye, but perceivest not the beam that is in thine own eye?› |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 41 \wj And why beholdest thou the mote that is in thy brother’s eye, but perceivest not the beam that is in thine own eye?\wj*
```

#### `Luk.17.36`

| mező | érték |
|---|---|
| `Szöveg` | Two men shall be in the field; the one shall be taken, and the other left. |
| `Szöveg_jelolt` | ‹Two [men] shall be in the field; the one shall be taken, and the other left.› |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 36 \wj Two \+add men\+add* shall be in the field; the one shall be taken, and the other left.\wj*
```

#### `Rom.16.27`

| mező | érték |
|---|---|
| `Szöveg` | To God only wise, be glory through Jesus Christ for ever. Amen. |
| `Szöveg_jelolt` | To God only wise, [be] glory through Jesus Christ for ever. Amen. |
| `Elotte` | *(üres)* |
| `Utoirat` | Written to the Romans from Corinthus, and sent by Phebe servant of the church at Cenchrea. |

Nyers USFM:

```
\v 27 To \w God|strong="G2316"\w* \w only|strong="G3441"\w* \w wise|strong="G4680"\w*, \add be\add* \w glory|strong="G1391"\w* \w through|strong="G1223"\w* \w Jesus|strong="G2424"\w* \w Christ|strong="G5547"\w* \w for|strong="G1519"\w* \w ever|strong="G0165"\w*. \w Amen|strong="G0281"\w*.
\s1 Written to the Romans from Corinthus, \add and sent\add* by Phebe servant of the church at Cenchrea.
```

#### `1Jn.2.23`

| mező | érték |
|---|---|
| `Szöveg` | Whosoever denieth the Son, the same hath not the Father: [but] he that acknowledgeth the Son hath the Father also. |
| `Szöveg_jelolt` | Whosoever denieth the Son, the same hath not the Father: [[but] he that acknowledgeth the Son hath the Father also]. |
| `Elotte` | *(üres)* |
| `Utoirat` | *(üres)* |

Nyers USFM:

```
\v 23 \w Whosoever|strong="G3956"\w* \w denieth|strong="G0720"\w* the \w Son|strong="G5207"\w*, the same \w hath|strong="G2192"\w* \w not|strong="G3761"\w* the \w Father|strong="G3962"\w*: \add [but] \+w he that acknowledgeth|strong="G3670"\+w* \+w the Son|strong="G5207"\+w* \+w hath|strong="G2192"\+w* \+w the Father|strong="G3962"\+w* \+w also|strong="G2532"\+w*\add*.
```

**Épség a teljes, memóriabeli kimeneten** (a tábla nem íródott a `konkordancia/`-ba):

- sorok: 31218; üres `Szöveg`: 0; `Elotte`: 22; `Utoirat`: 14; vershíd: 0; folytatás-sor: 0; parse-anomália: 0
- a versek halmaza azonos a `f19.parse_usfm`-éval: True (saját 31218, F19 31218)
- formai hibák (backslash, szóköz írásjel előtt, dupla szóköz, páratlan/üres `[ ]`, ¶ a `Szöveg`-ben, a két szövegmező szavai eltérnek): {'Szoveg_es_jelolt_szavai_elternek': 1}
- veszteség-számlálók: w=349308, labjegyzet=6959, p=4635, q1=2461, b=209, nd=6892, wj=2038, tl=22, pilcrow=2970, add=21510, kiser_add=7, fejlec_sor=398, wj_atnyulo_lezaras=0

## 4. Megjegyzés a mintához

- Az 1Jn 2:23 nyers sora a kódblokkban teljes hosszában áll. A vers második fele egyetlen `\add`, benne `\+w` szavakkal.
- A minta nem fed le minden jelölőt. A `\b`, a `\p` és a `\f` a teljes kimeneten számolva van (épség, fent), a jelölőnkénti egységtesztek a tesztfájlban vannak.

## 5. DT212 (d): a második példány — a felhasználó teendője

A menet a második példányt nem hozta létre, és nem másolta sehová (az orkesztrátor utasítása szerint). Ami kell hozzá:

| | |
|---|---|
| fájl | `C:\Users\bases\Desktop\kjv_munka\kjv.zip` |
| sha256 | `00532b6db1825cb78fd34de2097fc280ce03ee22ef0bdac5243ef4beaca4d447` |
| méret | 2 766 294 bájt |
| forrás | https://ebible.org/Scriptures/eng-kjv_usfm.zip (a zip bejegyzései 2026-10-17-esek; az eBible gördülő kiadású, ez a csomag később nem tölthető le újra) |
| javasolt hely | a repón kívül, egy második, a felhasználó által megnevezett helyen; lehetőleg más meghajtón vagy mentésben, mint az asztal (az M0-terv csak a „második példány a felhasználó által megnevezett helyen” elvet rögzítette, konkrét helyet nem). Javasolt fájlnév: `eng-kjv_usfm_2026-10-17.zip` |
| ellenőrzés a másolás után | PowerShellben: `Get-FileHash <a másolat útvonala> -Algorithm SHA256`, az eredménynek a fenti hash-nek kell lennie |
| ezután | a felhasználó megadja a helyet; az M3 a dataset leírásába (`adat/SEMA.md`, l. DT212 egyeztetendő pont) a hash-sel együtt beírja mindkét helyet |
