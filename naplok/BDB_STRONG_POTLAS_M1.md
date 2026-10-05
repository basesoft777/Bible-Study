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

## 3. Másodlagos címke: a Strong a BDB.lexicon-ban van, a táblában nincs sora (DT-F57a, DT-F57c, DT-F57f)

- 529 Strong (a H0136 és a H0341 is ide tartozik): a BDB.lexicon `H<n>` kulcsa létezik, a szócikk fejlécében a Strong másik Strong mellett áll, ezért a 3. kizárási szabály miatt nem párosítható.
- **Alias-feltétel (DT-F57f, nyelvi szűrés nélkül):** (1) a testvér-Strong táblasora ugyanabból a BDB-szócikkből származik (a testvér `H<n>` kulcsának `bdb_id`-je egyezik a másodlagos címke `bdb_id`-jével), ÉS (2) a szócikk szövege a testvérsor **elején** áll: a mérés a szócikk ujjlenyomatát (hivatkozások nélkül, csak betűk; legfeljebb 1500 karakter) veti össze a testvérsor azonos hosszúságú elejével (a sorfej miatt +60 karakter ablak), a szócikk karaktereinek hányada, amely a sor elején megvan; küszöb **≥ 0.9**. Az előző, teljes szöveget mérő `difflib`-arány (DT-F57e, 0,6) rendszerszinten alulmért, mert a DictBDB-sor a saját szócikke után további szócikkeket is tartalmazhat (pl. H6130 az ʿĀqān után az עקר gyököt). A hivatkozások kihagyása azért kell, mert a két forrás eltérően rövidíti és tömöríti őket (1Kgs/1Kin, 13:20 ; 13:21 / 13:20-21).
- **Alias** (`konkordancia/BDB_strong_alias.tsv`): 248 sor (héber 234, arámi 14). **Elvetett, jelölt marad** (`konkordancia/BDB_strong_alias_elvetett.tsv`): 281 sor (héber 108, arámi 173).
- Elvetés oka: a testvér-sor nem ebből a BDB-szócikkből származik: 220; a testvérsor más szócikk (a szócikk nem a testvérsor elején áll): 61.
- Több testvéres sor a megmaradt 248 aliasban: **0** (ellenőrizve).
- **Az elvárástól való eltérés (DT-F57f).** A várakozás ~300 alias volt (290 + a visszakerülő ~10). A tényleges szám **248**, mert a 0,9-es küszöb a korábbi 0,6-os küszöbnél szigorúbb: a bdb_id-egyező sorok közül a küszöb alatt (0,79–0,90 kerekítve) marad 52, olyan sor is, ahol a szöveg ténylegesen ugyanaz a szócikk, de a két forrás szövege az elején is eltér (átfogalmazott hivatkozások, kihagyott megjegyzések). Ezek jelöltek maradnak az elvetett listán; a küszöböt nem állítottuk.
- **Külön listázott sorok (a felhasználó ellenőrizheti):**

| Strong | testvér | bdb_id | kimenet | elejegyezés |
|---|---|---|---|---|
| H3292 | H6130 | BDB6328 | alias | 0.96 |
| H3347 | H4169 | BDB3686 | elvetett | 0.85 |
| H5761 | H5757 | BDB5872 | alias | 1.00 |
| H6978 | H6979 | BDB7348 | alias | 0.94 |
| H8284 | H7791 | BDB8569 | alias | 0.93 |
| H0532 | H0526 | BDB515 | alias | 1.00 |
| H7485 | H7480 | BDB8020 | alias | 1.00 |
| H2753 | H2752 | BDB3121 | alias | 0.91 |
| H0868 | H0866 | BDB9203 | alias | 1.00 |
| H0869 | H0866 | BDB9203 | alias | 1.00 |
| H3606 | H6903 | BDB9612 | elvetett | 0.07 |

- **Arámi szócikkek: két szám összevetése.** A BDB.lexicon nyelvjelölése szerint a 529 másodlagos címke között **187** arámi szócikk van (BDB9264-től; ez a felhasználó 187-es száma). A független ellenőr 198-at talált; ez a szám a BDB.lexicon nyelvjelöléséből nem reprodukálható (a legközelebbi mérések: arámi szócikk 187; arámi másodlagos OSHL-Strong héber testvérsorral 174), a különbség (11) okát nem tudtuk azonosítani. Mérvadó a feltétel, nem a szám: az arámi szócikkek közül 173 kerül elvetésre, 14 marad aliasban.
- **Nyitott tétel:** az elvetett arámi szócikkek tényleges pótlása (a BDB.lexicon szövegéből új táblasorok) külön feladat a `/befogad` útján, nem az F57 része (DT-F57d).
