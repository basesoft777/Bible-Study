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

## 3. Másodlagos címke: a Strong a BDB.lexicon-ban van, a táblában nincs sora (DT-F57a, DT-F57c)

- 529 Strong (a H0136 és a H0341 is ide tartozik): a BDB.lexicon `H<n>` kulcsa létezik, a szócikk fejlécében a Strong másik Strong mellett áll, ezért a 3. kizárási szabály miatt nem párosítható.
- **Alias-feltétel (DT-F57c, nyelvi szűrés nélkül):** a testvér-Strong táblasora ugyanabból a BDB-szócikkből származik (a testvér `H<n>` kulcsának `bdb_id`-je egyezik a másodlagos címke `bdb_id`-jével), és a sor szövege hasonlít a szócikk szövegére (alfanumerikus ujjlenyomat, `difflib`, küszöb 0.6). A korábbi „címszó mássalhangzói rész-sztringként a testvér-sorban” teszt nem igazolás, kivezetve.
- **Alias** (`konkordancia/BDB_strong_alias.tsv`): 290 sor (héber 276, arámi 14). **Elvetett, jelölt marad** (`konkordancia/BDB_strong_alias_elvetett.tsv`): 239 sor (héber 66, arámi 173).
- Elvetés oka: a bdb_id egyezik, de a testvér-sor szövege nem a szócikk szövege: 14; a testvér-sor nem ebből a BDB-szócikkből származik: 220; kezi_ellenorzesre (határsáv 0,55-0,59, kézzel beemelhető): 5.
- Több testvéres sor a megmaradt 290 aliasban: **0** (ellenőrizve; a több testvéres sorok a szövegegyezési küszöbön nem mennek át, DT-F57e). A határsáv (hasonlóság 0,55-0,59, két tizedesre kerekítve) 5 sora `kezi_ellenorzesre` indokkal áll az elvetett listán, kézzel beemelhető; a küszöb (0.6) nem változott.
- **Arámi szócikkek: két szám összevetése.** A BDB.lexicon nyelvjelölése szerint a 529 másodlagos címke között **187** arámi szócikk van (BDB9264-től; ez a felhasználó 187-es száma). A független ellenőr 198-at talált; ez a szám a BDB.lexicon nyelvjelöléséből nem reprodukálható (a legközelebbi mérések: arámi szócikk 187; arámi másodlagos OSHL-Strong héber testvérsorral 174), a különbség (11) okát nem tudtuk azonosítani. Mérvadó a `bdb_id`-feltétel, nem a szám: ez az arámi szócikkek közül 173-et ejt az aliasból, 14 marad (olyan arámi szócikk, amelynek testvérsora is ugyanabból a szócikkből származik).
- **Nyitott tétel:** az elvetett arámi szócikkek tényleges pótlása (a BDB.lexicon szövegéből új táblasorok) külön feladat a `/befogad` útján, nem az F57 része.
