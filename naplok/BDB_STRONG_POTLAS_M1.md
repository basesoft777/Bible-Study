# BDB_STRONG_POTLAS M1 — párosítás (F57)

*Generálta: `python eszkozok/bdb_strong_potlas.py --m1` · scope=konkordancia/lexikonok_nyers/BDB.lexicon + konkordancia/OSHL_lexikalis_index.tsv + konkordancia/BDB_teljes_unabridged.tsv | forras=eszkozok/bdb_strong_potlas.py (cimszo-egyezes) | ts=2026-10-05*

## 1. Párosítási szabály (szó szerint, BRIEF §3 M1)

1. Címszó-egyezés: az OSHL-lemma és a BDB-címszó normalizált alakja egyezik; a normalizálás egységesíti a holem-waw írásváltozatokat (U+05BA -> U+05B9), eltávolítja a kantillációs jeleket (U+0591-05AF) és a meteget/rafét; a magánhangzópontok megmaradnak. Címszó: a szófaj-jelölő előtti első `<bdbheb>`; nyelv (héber/arámi) egyezik.
2. Homonímia: ha több jelölt van, az OSHL `def_en` és a BDB glosszái közti szóegyezés dönt; ha nem dönt egyértelműen, `tobb_jelolt`.
3. Kizárás: ha a BDB-szócikknek már van Strong-címkéje, vagy a Strong-számnak már van sora a táblában (vagy `H<n>` kulcsa a BDB.lexicon-ban), nem párosítható.
Gyök-hivatkozás ("√ of following", szófaj nélkül) mindig `nincs_par`.

## 2. Eredmény a címke nélküli szócikkekre

- Sorok: 846; állapotok: {'nincs_par': 843, 'egyertelmu': 3}.
- A `BDB_strong_potlas.tsv` a **címke nélküli** BDB-szócikkeket (BDB-azonosító szerint) sorolja; a Strong-oszlop a pár.

### Egyértelmű párok (mind)

| BDB | Strong | címszó | OSHL-lemma | indok |
|---|---|---|---|---|
| BDB754 | H0747 | אֲרִיסַי | אֲרִיסַי | egyedi címszó-egyezés (mindkét irányban 1:1); BDB glossza: son of Haman / OSHL def_en: Arisai |
| BDB2246 | H4123 | מַהֲתַלּוֺת | מַֽהֲתַלּוֹת | egyedi címszó-egyezés (mindkét irányban 1:1); BDB glossza: deceptions / OSHL def_en: illusions |
| BDB7372 | H4725 | מָקוֺם | מָקוֹם | egyedi címszó-egyezés (mindkét irányban 1:1); BDB glossza: standing-place, place; standing-place / OSHL def_en: standing-place |

### Tobb_jelolt sorok (mind)

Nincs.


### Nincs_par, mássalhangzó-egyezési tipppel (nem párosítás; kézi döntéshez)

| BDB | címszó | tipp |
|---|---|---|
| BDB1362 | בשׂם | H1313 |
| BDB4531 | מהר | H4118 |

## 3. Másodlagos címke: a Strong a BDB.lexicon-ban van, a táblában nincs sora (DT-F57a, DT-F57c, DT-F57f, DT-F57g, DT-F57h)

- 529 Strong (a H0136 és a H0341 is ide tartozik): a BDB.lexicon `H<n>` kulcsa létezik, a szócikk fejlécében a Strong másik Strong mellett áll, ezért a 3. kizárási szabály miatt nem párosítható.
- **Alias-feltétel (DT-F57f/g/h, nyelvi szűrés nélkül):** (1) a testvér-Strong táblasora ugyanabból a BDB-szócikkből származik (a testvér `H<n>` kulcsának `bdb_id`-je egyezik a másodlagos címke `bdb_id`-jével); (2) **mérőszám** (`elejegyezes`): a szócikk ujjlenyomatának (CSAK latin betűk; a héber szöveg és a bibliai hivatkozások kimaradnak; legfeljebb 1500 karakter) az a hányada, amely a testvérsor elején megvan: a testvérsor (a `H<n>.` előtag nélküli) ujjlenyomatának első `hossz + 60` karaktere az ablak, az érték a `difflib.SequenceMatcher` egyező blokkjainak karakterszáma osztva a szócikk ujjlenyomatának hosszával; **küszöb ≥ 0.9**; (3) ha több azonos szócikkbeli testvér van, pontosan **egy** felel meg a (2)-nek, és az az alias célja (2+ megfelelő esetén `tobb_testveres`, elvetve; ilyen sor jelenleg nincs); (4) a kézi kivételek (`KIZART`) kint maradnak.
- A héber szöveg azért marad ki, mert a DictBDB a többszavas héber kifejezések szórendjét megfordítja (pl. H3347: ugyanaz a szöveg fordított sorrendben); a hivatkozások azért, mert a két forrás eltérően rövidíti őket (1Kgs/1Kin, 13:20 ; 13:21 / 13:20-21). Korlát: csonk szócikknél (rövid latin szöveg, pl. BDB515, BDB3121) az egyezés triviálisan magas lehet; az alias oldalán a mintában ebből hamis alias nem lett, de a mérőszám ott gyenge bizonyíték.
- **Az alias azt mondja meg, hol áll a BDB-szövege, nem azt, hogy a két szó azonos.** Pl. az Abel-összetett helynevek (H0059, H0063–H0067) a H0058 ʾābēl sorára oldódnak fel, mert a BDB alpontként tárgyalja őket.
- A H3071, H3073, H3074 (JHVH-nisszí, JHVH-sálóm, JHVH-sammá; a BDB a második tag szócikkében tárgyalja őket: נֵס, שָׁלוֹם, שָׁם) alias: ugyanaz a minta, mint az Abel-helyneveknél; az alias azt mondja meg, hol áll a BDB-szövege, nem azt, hogy a két szó azonos (DT-F57i).
- **Alias** (`konkordancia/BDB_strong_alias.tsv`): 296 sor (héber 282, arámi 14). **Elvetett, jelölt marad** (`konkordancia/BDB_strong_alias_elvetett.tsv`): 233 sor (héber 60, arámi 173).
- Elvetés oka (az `indok_kod` oszlop kódjai; darab, ebből arámi): `a_testversor_mas_szocikk`: 9 (arámi 1); `kifejezes_tarscimke`: 1 (arámi 0); `kuszob_alatt`: 3 (arámi 0); `nem_ebbol_a_szocikkbol`: 220 (arámi 172).
- Több testvéres sor a megmaradt 296 aliasban: **0** (ellenőrizve). A `testver_strong` oszlop az elvetett listán csak az azonos szócikkbeli testvéreket sorolja fel (kivéve a `nem_ebbol_a_szocikkbol` sorokat, ahol nincs ilyen: ott a más szócikkből származó testvérek állnak).
- **Az elvárástól való eltérés (DT-F57h/i).** A várakozás kb. 294 alias volt (a DT-F57h ~291 + a H3071, H3073, H3074); a tényleges szám **296**: a H5853 és a H5855 → H5852 a szabály szerint alias (mérőszám 0,981: a H5852 sora szó szerint a BDB5999 szócikke), nem `kuszob_alatt` (az előzetes felhasználói mérés 0,86 volt). A két sor az aliasban van; ha mégis kint kellene tartani őket, a `KIZART` bővítendő.
- **Külön listázott sorok (a felhasználó ellenőrizheti; a mérőszám három tizedessel):**

| Strong | testvér | bdb_id | kimenet | mérőszám / indok |
|---|---|---|---|---|
| H3347 | H4169 | BDB3686 | alias | 1.000 |
| H3606 | H6903 | BDB9612 | elvetett | a testvérsor más szócikk (a bdb_id egyezik, de a szócikk szövege nem a testvérsor elején áll, és a testvérsor nem ugyanazzal a címszóval kezdődik; elejegyezés 0.244, a feltétel: >= 0.9) |
| H2088 | H6258 | BDB6199 | elvetett | a BDB6199 fejlécében [H6258 H2088 H2009 H5704 H3588] a „zeh” egy attá-kifejezés miatt kapott társcímkét; a saját szócikke máshol van, ezért valódi téves alias volna (a BDB6199 az עַתָּה szócikke); elejegyezés 0.991 |
| H3071 | H5251 | BDB5242 | alias | 0.999 |
| H3073 | H7965 | BDB8734 | alias | 0.990 |
| H3074 | H8033 | BDB8775 | alias | 0.995 |
| H8550 | H8537 | BDB9190 | alias | 1.000 |
| H6990 | H5354 | BDB7356 | alias | 0.967 |
| H0206 | H0205 | BDB223 | alias | 1.000 |
| H7929 | H7926 | BDB8670 | alias | 0.991 |
| H5853 | H5852 | BDB5999 | alias | 0.981 |
| H5855 | H5852 | BDB5999 | alias | 0.981 |
| H8625 | H4484 | BDB9673 | alias | 1.000 |

- **`kuszob_alatt` sorok (3):** a testvérsor ugyanazzal a címszóval kezdődik, de a mérőszám a küszöb (0.9) alatt van; jelöltként maradnak. A #57-ben nincs egyenkénti beemelés (DT-F57i); az `indok_kod` oszlop `kuszob_alatt` értéke szűrhető, egy későbbi feladat beemelheti őket.

| Strong | testvér | bdb_id | címszó | mérőszám |
|---|---|---|---|---|
| H0706 | H0702 | BDB7718 | אַרְבַּע | 0.832 |
| H6737 | H6735 | BDB7058 | צִיר | 0.858 |
| H8112 | H8110 | BDB8860 | שִׁמְרוֺן | 0.873 |

- **Arámi szócikkek: két szám összevetése.** A BDB.lexicon nyelvjelölése szerint a 529 másodlagos címke között **187** arámi szócikk van (BDB9264-től; ez a felhasználó 187-es száma). A független ellenőr 198-at talált; ez a szám a BDB.lexicon nyelvjelöléséből nem reprodukálható (a legközelebbi mérések: arámi szócikk 187; arámi másodlagos OSHL-Strong héber testvérsorral 174), a különbség (11) okát nem tudtuk azonosítani. Mérvadó a feltétel, nem a szám: az arámi szócikkek közül 173 kerül elvetésre (ebből `nem_ebbol_a_szocikkbol`: 172, `a_testversor_mas_szocikk`: 1), 14 marad aliasban.
- **Nyitott tétel:** (DT-F57d) az elvetett arámi szócikkek tényleges pótlása (a BDB.lexicon szövegéből új táblasorok) külön feladat a `/befogad` útján, nem az F57 része.
