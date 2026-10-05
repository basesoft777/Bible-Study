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

## 3. Másodlagos címke: a Strong a BDB.lexicon-ban van, a táblában nincs sora (DT-F57a, DT-F57c, DT-F57f, DT-F57g)

- 529 Strong (a H0136 és a H0341 is ide tartozik): a BDB.lexicon `H<n>` kulcsa létezik, a szócikk fejlécében a Strong másik Strong mellett áll, ezért a 3. kizárási szabály miatt nem párosítható.
- **Alias-feltétel (DT-F57f/g, nyelvi szűrés nélkül):** (1) a testvér-Strong táblasora ugyanabból a BDB-szócikkből származik (a testvér `H<n>` kulcsának `bdb_id`-je egyezik a másodlagos címke `bdb_id`-jével); (2) **mérőszám** (`elejegyezes`): a szócikk ujjlenyomatának (CSAK latin betűk; a héber szöveg és a bibliai hivatkozások kimaradnak; legfeljebb 1500 karakter) az a hányada, amely a testvérsor elején megvan: a testvérsor (a `H<n>.` előtag nélküli) ujjlenyomatának első `hossz + 60` karaktere az összevetés ablaka, az érték a `difflib.SequenceMatcher` egyező blokkjainak karakterszáma osztva a szócikk ujjlenyomatának hosszával; **küszöb ≥ 0.9**; (3) pontosan egy testvér-Strong sora származik ugyanabból a szócikkből (a több testvéres sorok kint maradnak); (4) a kézi kivételek (`KIZART`) kint maradnak.
- A héber szöveg azért marad ki, mert a DictBDB a többszavas héber kifejezések szórendjét megfordítja (pl. H3347: ugyanaz a szöveg fordított sorrendben); a hivatkozások azért, mert a két forrás eltérően rövidíti őket (1Kgs/1Kin, 13:20 ; 13:21 / 13:20-21). Korlát: csonk szócikknél (rövid latin szöveg, pl. BDB515, BDB3121) az egyezés triviálisan magas lehet; az alias oldalán a mintában ebből hamis alias nem lett, de a mérőszám ott gyenge bizonyíték.
- **Alias** (`konkordancia/BDB_strong_alias.tsv`): 256 sor (héber 243, arámi 13). **Elvetett, jelölt marad** (`konkordancia/BDB_strong_alias_elvetett.tsv`): 273 sor (héber 99, arámi 174).
- Elvetés oka (kód: db; ebből arámi): a_testversor_mas_szocikk: 12 (arámi 1); kezi_dontes: 3 (arámi 0); kifejezes_tarscimke: 1 (arámi 0); nem_ebbol_a_szocikkbol: 220 (arámi 172); tobb_testveres: 37 (arámi 1).
- Több testvéres sor a megmaradt 256 aliasban: **0** (ellenőrizve).
- **Az elvárástól való eltérés (DT-F57g).** A várakozás kb. 294 alias volt; a tényleges szám **256**, mert a több testvéres sorokat a szabály következetesen kint tartja (`tobb_testveres`: 37 sor, köztük a H8550, H6990, H0206, H7929; minden ilyen sorban az elvetett lista `testver_strong` oszlopa a jelölteket mutatja, így kézzel beemelhetők), és a 4 kézi kivétel is kint van.
- **Külön listázott sorok (a felhasználó ellenőrizheti; a mérőszám három tizedessel):**

| Strong | testvér | bdb_id | kimenet | mérőszám / indok |
|---|---|---|---|---|
| H3347 | H4169 | BDB3686 | alias | 1.000 |
| H3606 | H6903 | BDB9612 | elvetett | a_testversor_mas_szocikk |
| H2088 | H6258 | BDB6199 | elvetett | kifejezes_tarscimke |
| H3071 | H5251 | BDB5242 | elvetett | kezi_dontes |
| H3073 | H7965 | BDB8734 | elvetett | kezi_dontes |
| H3074 | H8033 | BDB8775 | elvetett | kezi_dontes |
| H8550 | H8537,H0224,H8549 | BDB9190 | elvetett | tobb_testveres |
| H6990 | H5354,H6962,H6985 | BDB7356 | elvetett | tobb_testveres |
| H0206 | H0205,H0204 | BDB223 | elvetett | tobb_testveres |
| H7929 | H7926,H7927 | BDB8670 | elvetett | tobb_testveres |

- **Arámi szócikkek: két szám összevetése.** A BDB.lexicon nyelvjelölése szerint a 529 másodlagos címke között **187** arámi szócikk van (BDB9264-től; ez a felhasználó 187-es száma). A független ellenőr 198-at talált; ez a szám a BDB.lexicon nyelvjelöléséből nem reprodukálható (a legközelebbi mérések: arámi szócikk 187; arámi másodlagos OSHL-Strong héber testvérsorral 174), a különbség (11) okát nem tudtuk azonosítani. Mérvadó a feltétel, nem a szám: az arámi szócikkek közül 174 kerül elvetésre (ebből `nem_ebbol_a_szocikkbol`: 172), 13 marad aliasban.
- **Nyitott tétel:** az elvetett arámi szócikkek tényleges pótlása (a BDB.lexicon szövegéből új táblasorok) külön feladat a `/befogad` útján, nem az F57 része (DT-F57d).
