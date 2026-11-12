#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
nyilt_mag_szovegek.py -- a nyílt motívum-adatmag (`nyilt_mag/`) nyilvános szövegei (F208, FELADATOK #208).

A csomag leíró szövegeinek prózája itt áll: OLVASSEL/README, MODSZER/METHODS, ATTRIBUCIO, LICENSE, CITATION.cff,
a `kozlemeny/` hu/en tervezete és a `.gitattributes`. A szerkezet a modernizált Károli – Strong csomag (F174)
mintáját követi. Minden szám a `nyilt_mag_export.py` által a generált táblákból számolt `sz` szótárból jön; itt
szám nem áll. Az export importálja ezt a modult; ez a modul az exportot nem importálja.

Használat: csak az exportból (`nyilt_mag_export.export`).
"""
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KOZLEMENY_DIR = 'kozlemeny/'

# a Markdown-fájlok GENERÁLT-jelölése HTML-megjegyzés: a „#” kezdetű sor a Markdownban főcím lenne (F208)
MD_FEJLEC = '<!-- GENERÁLT: a(z) %s nyílt adatmagjának exportja, a projekt adataiból generálva; kézzel nem szerkesztendő. -->'
MD_FEJLEC_EN = '<!-- GENERATED: export of the %s open data core, generated from the project data; do not edit by hand. -->'


def ezres(n, nyelv='hu'):
    """Ezres tagolás: magyarul szóközzel (31 158), angolul vesszővel (31,158)."""
    s = '{:,}'.format(n)
    return s.replace(',', ' ') if nyelv == 'hu' else s


def fmt(sz, nyelv):
    """A számok szótára az adott nyelv formájában (egész → tagolt szöveg; a többi változatlan). A `…_hu` / `…_en`
    kulcs az adott nyelven a végződés nélküli kulcsot is kitölti (pl. `lezart_lista_hu` → `lezart_lista`)."""
    ki = {k: (ezres(v, nyelv) if isinstance(v, int) and not isinstance(v, bool) else v) for k, v in sz.items()}
    for k in list(ki):
        if k.endswith('_' + nyelv):
            ki[k[:-len(nyelv) - 1]] = ki[k]
    return ki


def felsorol(elemek, nyelv):
    elemek = list(elemek)
    if len(elemek) < 2:
        return ''.join(elemek)
    es = ' és ' if nyelv == 'hu' else ' and '
    return ', '.join(elemek[:-1]) + es + elemek[-1]


# ----------------------------------------------------------------------------------- tartalomjegyzék

FAJL_LEIRAS = [
    # (fájl, magyar leírás, angol leírás)
    ('motivumok.tsv', 'a motívumok: cím, meghatározás, az azonosság hordozója, kizáró jegy, fölérendelt fogalom, '
     'feldolgozási állapot',
     'the motifs: title, definition, carrier of identity, exclusion criterion, superordinate concept, processing stage'),
    ('elofordulasok.tsv', 'az előfordulások: igehely, a horgonyszó és Strong-száma, szótári jelentés, Károli-szó, '
     'eredetjelölés', 'the occurrences: passage, anchor word and its Strong\'s number, dictionary sense, Károli word, '
     'provenance'),
    ('beepitesi_dontesek.tsv', 'a felvett helyek döntése, indoklással', 'the inclusion decisions, with rationale'),
    ('kizarasok.tsv', 'a vizsgált, de kizárt helyek, okkal és indoklással; az összesítő sor egy csoportot képvisel',
     'the passages examined but excluded, with reason and rationale; a summary row stands for a group'),
    ('kizaras_csoportok.tsv', 'az összesítő sorok csoportjainak minden verse', 'every verse of the summary-row groups'),
    ('kapcsolatok.tsv', 'igehely-kapcsolatok egy motívumon belül', 'relations between passages within a motif'),
    ('motivum_kapcsolatok.tsv', 'kapcsolatok két motívum között', 'relations between two motifs'),
    ('dontesnaplo.tsv', 'a hivatkozott szerkesztői döntések (`NYD-nnn`)', 'the editorial decisions referred to '
     '(`NYD-nnn`)'),
    ('visszhang_megfelelok.tsv', 'a horgonyszavak megfelelője a Targumban, a Vulgatában és a Septuagintában',
     'the counterparts of the anchor words in the Targum, the Vulgate and the Septuagint'),
    ('visszhang_tanuk.tsv', 'egyházatyai, rabbinikus és Glossa Ordinaria-tanúk, idézet nélkül',
     'patristic, rabbinic and Glossa Ordinaria witnesses, without quotation'),
    ('vitatott_forrasok.tsv', 'a vitatott pontok lektorált szakirodalma (bibliográfiai adat)',
     'the peer-reviewed literature on the disputed points (bibliographic data)'),
    ('sblgnt_apparatus.tsv', 'az SBL Greek New Testament kritikai apparátusa az újszövetségi helyekhez',
     'the critical apparatus of the SBL Greek New Testament for the New Testament passages'),
    ('forrasok_es_licencek.tsv', 'a projekt forrásleltára: licenc és szerep a csomagban',
     'the project\'s source inventory: licence and role in the package'),
    ('kodkonyv.tsv', 'az oszlopok, értékek és kódok leírása (magyarul és angolul)',
     'description of the columns, values and codes (Hungarian and English)'),
    ('KODKONYV.md', 'ugyanez olvasható formában', 'the same in readable form'),
    ('cc_by_sa_reteg/szemantikai_domenek.tsv', 'szemantikai domének (UBS SDBH/SDGNT), **külön licenc: CC BY-SA 4.0**',
     'semantic domains (UBS SDBH/SDGNT), **separate licence: CC BY-SA 4.0**'),
    ('cc_by_sa_reteg/OLVASSEL.md', 'a külön réteg licence és forrásmegjelölése', 'licence and attribution of the '
     'separate layer'),
    ('MODSZER.md', 'hogyan készült az adat (angolul: `METHODS.md`)', 'how the data were made (Hungarian: '
     '`MODSZER.md`)'),
    ('ISMERT_HIBAK.md', 'ismert hibák és korlátok (angolul: `KNOWN_ISSUES.md`)', 'known issues and limitations '
     '(Hungarian: `ISMERT_HIBAK.md`)'),
    ('ATTRIBUCIO.md', 'forrásmegjelölés, licencek, kizárt források', 'attribution, licences, excluded sources'),
    ('LICENSE', 'a csomag licence', 'the licence of the package'),
    ('CITATION.cff', 'idézési adatok', 'citation metadata'),
    ('KIADAS.txt', 'a kiadás azonosítója és tartalmi hash-e (angolul: `RELEASE.txt`)', 'release identifier and content '
     'hash (Hungarian: `KIADAS.txt`)'),
    ('ELLENORZO_OSSZEG.sha256', 'minden fájl SHA-256 összege', 'SHA-256 checksum of every file'),
]


def tartalom_tabla(stat, nyelv):
    """A tartalomjegyzék: fájl, leírás, sorszám (a TSV-knél). Minden kiadott fájl szerepel (a kapu méri)."""
    if nyelv == 'hu':
        ki = ['| fájl | tartalom | sor |', '|---|---|---:|']
    else:
        ki = ['| file | content | rows |', '|---|---|---:|']
    for rel, hu, en in FAJL_LEIRAS:
        nev = ANGOL_PAR.get(rel, rel) if nyelv == 'en' else rel
        ki.append('| `%s` | %s | %s |' % (nev, hu if nyelv == 'hu' else en,
                                         ezres(stat[rel], nyelv) if rel in stat else ''))
    return ki


# az angol tartalomjegyzékben a kétnyelvű pár angol tagja áll elöl (a leírás a magyar tagot nevezi meg)
ANGOL_PAR = {'MODSZER.md': 'METHODS.md', 'ISMERT_HIBAK.md': 'KNOWN_ISSUES.md', 'KIADAS.txt': 'RELEASE.txt'}


# ----------------------------------------------------------------------------------- OLVASSEL / README

def olvassel(sz, hogyan, stat, adatmag_lexikon):
    f = fmt(sz, 'hu')
    ki = ['# {cim_hu} — nyílt adatmag: bibliai motívumok'.format(**f), '', MD_FEJLEC % f['cim_hu'], '',
          'Bibliai motívumok nyílt adatkészlete: a motívumok meghatározó és kizáró jegyei, előfordulásaik a héber és '
          'görög szöveg szavain, a megvizsgált, de kizárt helyek okkal, az igehely-kapcsolatok és a döntésnapló. A '
          '{cim_hu} nyílt adatmagjainak egyike. *English version: `README.md`.*'.format(**f), '',
          '- **Licenc:** CC BY 4.0 (`LICENSE`); a `cc_by_sa_reteg/` könyvtár külön, CC BY-SA 4.0 licenc alatt áll. A '
          'felhasznált külső adatok forrásmegjelölése és a kizárt források: `ATTRIBUCIO.md`.',
          '- **DOI:** {doi} — a kiadás azonosítója és a tartalmi hash: `KIADAS.txt`.'.format(**f),
          '- **Szerző:** {szerzo} (ORCID {orcid}).'.format(**f), '',
          '## Tartalom', ''] + tartalom_tabla(stat, 'hu') + [
          '', '## Számokban', '',
          '- {mot} motívum: {lezart} lezárt kiadás, {regi} régi feldolgozás, amely a későbbi változatokban frissül '
          '(`motivumok.tsv`, `feldolgozasi_allapot`).'.format(**f),
          '- {elo} előfordulás és {beep} felvételi döntés.'.format(**f),
          '- {kiz} kizárás-sor {okok} okkal: {kiz_egyedi} egyenként eldöntött hely, és {osszesito} összesítő sor, '
          'amely {csoport_vers} verset képvisel.'.format(**f),
          '- {kap} igehely-kapcsolat, {mkap} motívumközi kapcsolat, {dontes} nyilvános szerkesztői döntés.'.format(**f),
          '- A visszhang-rétegben {vh_megf} megfelelő, {vh_tanu} tanú, {vit} vitatott pont és {sbl} '
          'apparátus-jegyzet.'.format(**f), '',
          '**Ismert hibák:** `ISMERT_HIBAK.md` (angolul: `KNOWN_ISSUES.md`). **Módszer:** `MODSZER.md`.', '',
          ] + hogyan + [
          '## Mi van benne, mi nincs (az adatmag és a lexikon)', '',
          adatmag_lexikon, '',
          '**Benne van (adatréteg):** a motívum azonosítója, címe és kizáró jegye; az előfordulások (igehely, '
          'szóbázis, szótári jelentés, Károli-szó); a kizárások és a felvételi döntések indoklással; a '
          'kapcsolatok; az eredetjelölés (a forrás megnevezése, licence, a lekérdezés típusa, dátum); a '
          'döntésnapló.', '',
          '**Nincs benne (a lexikon):** az értelmező próza (kivonat, értelmezés, igehelyenkénti '
          'kifejtés), a magyar szótári fordítások, a kötetanyag és a lexikonlapok.', '',
          '**Nincs a csomagban továbbá:** a még el nem döntött jelöltek ({nyitva}); a források szövege (idézet); a '
          'belső munkajelek (azonosítók, munkafájlok, lekérdezés-nyomok). Ahol egy sor döntésre hivatkozik, a '
          'nyilvános azonosító (`NYD-nnn`) a `dontesnaplo.tsv`-ben oldható fel.'.format(**f), '',
          '## Idézés és közzétételi hely', '',
          '**Idézd így:** {szerzo} (ORCID: {orcid}): {cim_hu} — nyílt adatmag: bibliai motívumok. DOI: {doi}. Az idézési adatok: '
          '`CITATION.cff`.'.format(**f), '',
          'A csomag kanonikus közzétételi helye: `{kanonikus}`. A változatot a kiadás azonosítója jelöli (`KIADAS.txt`: '
          'az adatállapot dátuma és a tartalmi hash), nem egy fejlesztői tár vagy commit. A lexikon honlapja: '
          '`https://{domain}`.'.format(**f), '',
          '## Kapcsolódó adatkészletek', '',
          '- Károli 1908 – Strong szóillesztés: https://doi.org/{doi_karoli_strong}'.format(**f),
          '- Modernizált Károli – Strong: https://doi.org/{doi_karoli_modern}'.format(**f), '',
          'A Károli-szöveg teljes Strong-párosítása ezekben áll; ez a csomag csak a motívumszó Károli-megfelelőjét '
          'adja.', '',
          '## Ellenőrzés', '',
          'Az `ELLENORZO_OSSZEG.sha256` minden kiadott fájl SHA-256 összegét tartalmazza; az export újrafuttatva '
          'bájtazonos. A `kozlemeny/` mappa a megjelenési közlemény tervezete, nem része a kiadásnak.', '']
    return '\n'.join(ki)


def readme(sz, how, stat, adatmag_lexikon_en):
    f = fmt(sz, 'en')
    ki = ['# {cim_en} — open data core: biblical motifs'.format(**f), '', MD_FEJLEC_EN % f['cim_en'], '',
          'An open dataset of biblical motifs: the defining and excluding features of the motifs, their occurrences '
          'on the words of the Hebrew and Greek text, the passages examined but excluded with reasons, the relations '
          'between passages, and the decision log. One of the open data cores of the {cim_en}. *Magyar változat: '
          '`OLVASSEL.md`.*'.format(**f), '',
          '- **Licence:** CC BY 4.0 (`LICENSE`); the `cc_by_sa_reteg/` directory is under a separate licence, CC BY-SA '
          '4.0. Attribution of the third-party data used, and the excluded sources: `ATTRIBUCIO.md`.',
          '- **DOI:** {doi} — release identifier and content hash: `RELEASE.txt`.'.format(**f),
          '- **Author:** {szerzo} (ORCID {orcid}).'.format(**f), '',
          '## Contents', ''] + tartalom_tabla(stat, 'en') + [
          '', '## In numbers', '',
          '- {mot} motifs: {lezart} closed releases, {regi} from an earlier stage that will be updated in later '
          'versions (`motivumok.tsv`, `feldolgozasi_allapot`).'.format(**f),
          '- {elo} occurrences and {beep} inclusion decisions.'.format(**f),
          '- {kiz} exclusion rows with {okok} reasons: {kiz_egyedi} passages decided one by one, and {osszesito} '
          'summary rows standing for {csoport_vers} verses.'.format(**f),
          '- {kap} relations between passages, {mkap} relations between motifs, {dontes} public editorial '
          'decisions.'.format(**f),
          '- In the echo layer: {vh_megf} counterparts, {vh_tanu} witnesses, {vit} disputed points and {sbl} apparatus '
          'notes.'.format(**f), '',
          '**Known issues:** `KNOWN_ISSUES.md`. **Methods:** `METHODS.md`.', '',
          ] + how + [
          '## What is in it and what is not (the data core and the lexicon)', '',
          adatmag_lexikon_en, '',
          '**Included (data layer):** the motif identifier, title and exclusion criterion; the occurrences '
          '(passage, lexical base, dictionary meaning, Károli word); the exclusions and inclusion decisions with '
          'rationale; the relations; provenance (the naming of the source, its licence, the type of query, the '
          'date); the decision log.', '',
          '**Not included (the lexicon):** the interpretive prose (summary, interpretation, passage-by-passage '
          'exposition), the Hungarian dictionary translations, the volume material and the lexicon pages.', '',
          '**Also not in the package:** candidates not yet decided ({nyitva}); the text of the sources (quotation); '
          'internal working marks (identifiers, working files, query traces). Where a row refers to a decision, the '
          'public identifier (`NYD-nnn`) can be resolved in `dontesnaplo.tsv`.'.format(**f), '',
          '## Citation and place of publication', '',
          '**Cite as:** {szerzo} (ORCID: {orcid}): {cim_en} — open data core: biblical motifs. DOI: {doi}. Citation metadata: '
          '`CITATION.cff`.'.format(**f), '',
          'The canonical place of publication of the package: `{kanonikus}`. A version is identified by the release '
          'identifier (`RELEASE.txt`: the date of the data state and the content hash), not by a development '
          'repository or a commit. The website of the lexicon: `https://{domain}`.'.format(**f), '',
          '## Related datasets', '',
          '- Károli 1908 – Strong word alignment: https://doi.org/{doi_karoli_strong}'.format(**f),
          '- Modernised Károli – Strong: https://doi.org/{doi_karoli_modern}'.format(**f), '',
          "The full Strong's alignment of the Károli text is in these; this package gives only the Károli counterpart "
          'of the motif word.', '',
          '## Verification', '',
          'The file `ELLENORZO_OSSZEG.sha256` contains the SHA-256 sum of every released file; rerunning the export is '
          'byte-identical. The `kozlemeny/` folder holds the draft announcement; it is not part of the release.', '']
    return '\n'.join(ki)


# ----------------------------------------------------------------------------------- MODSZER / METHODS

MODSZER = """# Módszer — a motívum-adatmag

*{cim_hu} — nyílt adatmag · adatállapot: {datum} · DOI: {doi}*

## 1. Mi ez az adatkészlet

Bibliai motívumok nyílt adatkészlete. Motívumnak olyan visszatérő bibliai témát nevezünk, amelynek jelenléte egy
versben a héber vagy a görög szövegen ellenőrizhető: egy szón, egy állandó szókapcsolaton vagy szavak
együttállásán. A csomag {mot} motívumot tartalmaz, {elo} előfordulással. Mellettük ugyanolyan részletesen áll a
másik oldal is: {kiz} kizárás-sor rögzíti indoklással azokat a helyeket, amelyeket megvizsgáltunk, de a
motívumhoz nem soroltunk.

{adatmag_lexikon} Az adatmagban döntések és rövid indoklások állnak, értelmező próza nem.

## 2. A motívum meghatározása

Egy motívum akkor kap azonosítót, ha négy kérdésre megvan a válasz: mi hordozza az azonosságát; mi az a legkisebb
jegy, amely nélkül egy hely nem tartozik ide (a kizáró jegy); ha egy hely két motívumhoz is tartozik, más-e a
szerepe a kettőben; és nem részhalmaza-e egy másik motívumnak. Minden motívum megnevezi azt a tágabb fogalmat is,
amely felé a határa szétfolyna (fölérendelt fogalom). Ha egy hely csak ezen keresztül kapcsolódik, kimarad.

A `motivumok.tsv` ezt három oszlopban adja: az azonosság hordozója (`azonossag_tipusa`; ebben a kiadásban
{tipus_hu}), a kizáró jegy (`negativ_kriterium`) és a fölérendelt fogalom (`folerendelt_fogalom`). Az olvasói
meghatározás (`meghatarozas`) egy-két mondatban mondja meg, mi a motívum; ebben a kiadásban {meghat} motívumnál áll,
a többinél üres. A motívum határát azonban nem a meghatározás rajzolja meg, hanem a kizárások.

## 3. A jelöltek gyűjtése

A lehetséges előfordulásokat (jelölteket) rögzített sorrendű keresések hozzák elő:

1. a motívum törzshelyein közösen előforduló szavak Strong-számai, a névelők, kötőszók és más nyelvtani szavak
   nélkül;
2. a szemantikai mező feltevése: ez az egyetlen nem gépi lépés, ezért a mező szavait rögzítjük;
3. a teljes ó- és újszövetségi szöveg átvizsgálása Strong-szám szerint, a STEPBible címkézett szövegén (TAHOT,
   TAGNT);
4. két szó együttes előfordulása egy versben;
5. az igealak ellenőrzése;
6. a Septuaginta-megfelelés.

Az 1. és a 3–6. lépést program végzi, ugyanarra a bemenetre ugyanazt az eredményt adja. Jelöltet hoztak még a
kereszthivatkozások (Treasury of Scripture Knowledge; a Károli-kiadás kereszthivatkozásai, l. `ISMERT_HIBAK.md`),
szótári szócikkek és a szerkesztői teljességi felmérés. Hogy egy döntött jelölt honnan jött, a `kizarasok.tsv` és
a `beepitesi_dontesek.tsv` `keresesi_mod` oszlopa mondja meg (ebben a kiadásban {keresesi_modok} keresési mód).

## 4. Döntés minden jelöltről

Keresési találatból nem lesz közvetlenül előfordulás. Minden jelöltről döntés születik, indoklással. A felvett
jelölt az `elofordulasok.tsv`-be kerül, a döntés indoklása a `beepitesi_dontesek.tsv`-be ({beep} sor); az
elutasított a `kizarasok.tsv`-be, egy kizárási okkal ({okok} ok) és indoklással.

A kizárás-sorok közül {kiz_egyedi} egy-egy helyről szól. {osszesito} sor összesítő: egy csoportot képvisel,
amelynek minden versét ugyanabból az okból utasítottuk el; a csoportok {csoport_vers} versét a
`kizaras_csoportok.tsv` sorolja fel, és az összesítő sor indoklása a csoport minden versére érvényes.

Ha egy keresés üres, az eredmény üres marad: a hiányt nem töltjük ki gyenge vagy asszociatív anyaggal. A még el
nem döntött jelöltek ({nyitva}) nincsenek a csomagban. Ahol egy sor szerkesztői döntésre hivatkozik, a döntés
nyilvános azonosítója (`NYD-nnn`) a `dontesnaplo.tsv`-ben oldható fel ({dontes} döntés).

## 5. Az előfordulás sora

Minden előfordulás egy igehely, és megnevezi, mire épül a besorolása (`horgony_tipus`, `horgony`): {horgony_hu}.
A `strong` oszlop a horgonyszó Strong-száma, a `jelentes_en` a szótári jelentés kivonata, a `strong_glossza_en` a
STEPBible rövid angol glosszája.

**A Károli-szó.** {karoli_hol} ott áll a Károli-fordítás megfelelő szava is. A Károli-szó nem bizonyíték:
azt mutatja meg, mit lát a helyből a magyar olvasó. A párosítást (`azonositas_modja`) {karoli_tartalom} esetben a
szerkesztő végezte a Károli-szöveg olvasásával, {karoli_gepi} esetben gépi szópárosítás adta (csak magas
bizonyosságú pár igazolhat sort), {karoli_kovet} esetben következtetés. A bizonyosság (`megbizhatosag`)
{karoli_magas} esetben magas, {karoli_kozepes} esetben közepes. A vers többi szavának párosítása nem része ennek az
adatkészletnek; az a kapcsolódó Károli – Strong adatkészletekben áll.

**Eredetjelölés.** Minden sor megnevezi, honnan származik: ha lekérdezésből, akkor a lekérdezés típusát, a forrást,
annak licencét és a dátumot; ha nem, azt, hogy kézi döntés, lekérdezés nélkül. Az előfordulások közül {kezi}
kézi döntés, {lekerd} egy lekérdezés közvetlen eredménye. A „kézi döntés” nem azt jelenti, hogy a sor ellenőrzött,
hanem azt, hogy nem egyetlen lekérdezés adta. A Strong-hozzárendelést {tahot_igazolt} sorban a TAHOT héber szövegén
tételesen visszakerestük (`igazolas`).

## 6. Feldolgozási állapot

{lezart} motívum lezárt kiadás ({lezart_lista}): a lexikonlapjuk kiadott, és hiba nélkül átment az olvasói kapun. A
többi {regi} a projekt korábbi szakaszában, régebbi eljárással készült. Adataik a mai sémában állnak, és ugyanazon
a kapun mennek át, de a kiadási eljárás átnézései rájuk még nem vonatkoznak, és a későbbi változatokban
módosulhatnak. Az állapot a `motivumok.tsv` `feldolgozasi_allapot` oszlopában áll; aki csak a lezárt anyaggal
dolgozna, ezen szűrhet.

## 7. A visszhang-réteg

Négy tábla a motívumok ókori fordításbeli és értelmezői visszhangját adja, forrásonként a licenccel:

- `visszhang_megfelelok.tsv` ({vh_megf} sor): a horgonyszavak megfelelője a Targumban ({vh_targum}), a
  Vulgatában ({vh_vulgata}) és a Septuagintában ({vh_lxx});
- `visszhang_tanuk.tsv` ({vh_tanu} sor): egyházatyai, rabbinikus és Glossa Ordinaria-tanúk: ki, melyik műben, mit
  lát a helyen, saját szavas egy mondatban, idézet nélkül;
- `vitatott_forrasok.tsv` ({vit} sor): a vitatott pontok lektorált szakirodalma, csak bibliográfiai adat; az üres
  szerző azt jelenti, hogy a vizsgált adatbázisokban a pontról lektorált forrás nem került elő;
- `sblgnt_apparatus.tsv` ({sbl} sor): az újszövetségi helyek kritikai apparátusa.

Csak ellenőrzött sor kerül be. A Septuaginta-megfelelők közül azokat, amelyeknél a versben egyetlen lemma jön
szóba, gép ellenőrizte; minden más sort egy második kéz nézett át. Nincs a csomagban: a Chain Lineage Browser
tanúi (a böngésző licencet nem közöl), a BDB rokon nyelvi sorai (külön döntésre várnak), és a források szövege.

## 8. Az angol réteg

Az oszlopnevek és az értékek magyarok; mellettük angol párhuzamos oszlopok állnak.

- **Igehely:** minden igehely-oszlop mellett `…_osis`, szabványos OSIS-kulccsal. A könyvkód szabványos, a fejezet- és
  versszám a Károli-fordítás számozása; ahol ez eltér a STEPBible-számozástól, a kulcs a Károli-verset jelöli.
- **Zárt értékek:** minden zárt értékkészletű oszlop mellett `…_en`, a kódkönyv szerkesztett angol címkéjével.
- **Szabad szöveg** (indoklás, funkció, a motívum meghatározása, a döntésnapló): `…_en` párhuzamos mező, **gépi
  fordítás** ({modellek_hu}). A sor `forditas_modja` oszlopa megnevezi a modellt, és kimondja a hiányt
  ({nincs_ford} sorban hiányzik a fordítás teljesen vagy részben).

## 9. Licencszűrés

A csomag csak közkincs, CC0 vagy CC BY 4.0 licencű forrásból vesz át értéket, a projekt licencleltára szerint.
{kizart_db} forrást kizártunk: nem kereskedelmi vagy GPL licencűt, tisztázatlan licencűt, és a projekt zárt,
származtatott rétegeit. A kizárt források listája és oka az `ATTRIBUCIO.md`-ben és a `forrasok_es_licencek.tsv`-ben
áll. A CC BY-SA 4.0 licencű szemantikai domének (UBS SDBH/SDGNT) külön könyvtárban vannak (`cc_by_sa_reteg/`),
mert a ShareAlike feltétel a belőlük származó munkára is kiterjed; a csomag többi része ettől független. A leltár
nem jogi vélemény.

## 10. A mesterséges intelligencia használata

A keresések determinisztikus programok. Hogy egy jelölt a motívumhoz tartozik-e, arról mesterséges intelligenciával
segített munkamenet dönt, a szerkesztő irányításával, és minden döntés indoklással rögzül. Gép végezte még a
Károli-szó gépi párosítását (5. pont), a szabad szöveges mezők angol fordítását (8. pont) és a Septuaginta-megfelelők
egyértelmű eseteinek ellenőrzését (7. pont). Az adattáblákat program állítja elő az adatból, nyelvi modell nem írja
őket; ugyanabból az adatból mindig ugyanaz a csomag készül. A leíró szövegeket (ez a módszerleírás, az olvass-el és
a közlemény) nyelvi modell fogalmazta, a számokat az export adja, a szöveget a szerkesztő hagyta jóvá. A modell nem
szerző; a tartalomért a szerző felel.

## 11. Ellenőrzés

A csomag saját gépi kapuja minden kiadás előtt fut. Méri a belső munkajelölést, a kódkönyv lefedettségét (minden
oszlop és zárt érték, mindkét nyelven), a licencszűrést, a döntés- és motívum-hivatkozások feloldását, az összesítő
sorok tagszámát, az OSIS-kulcsokat, a fordítás frissességét és a bájtazonos újragenerálást. Az
`ELLENORZO_OSSZEG.sha256` minden kiadott fájl SHA-256 összegét tartalmazza; a `KIADAS.txt` tartalmi hash-e ennek a
listának az összege.

A kiadott lexikonlapon az olvasói kapu nulla hibát követel. A munka minden lépésének változásait egy friss
kontextusú modell saját lekérdezéssel újra ellenőrzi; a motívum határát egy második modell nézi át. Ez nem
független szakmai lektorálás: a szerzőn kívül minden ellenőr program vagy nyelvi modell.

## 12. Korlátok

- Lezárt kiadás csak {lezart} motívum; {regi} régi feldolgozás (6. pont).
- A teljesség nem bizonyított. A keresések azt mérik, mennyit fog meg a lista a lexikai jegyek alapján; a
  tematikus kapcsolatot nem.
- Független szakmai lektorálás és annotátorok közötti egyezésmérés nem volt.
- A motívumokat a kutatási program választotta ki; nem reprezentatív mintái a Bibliának.
- A forrásadatok ismert hibáit és kezelésüket az `ISMERT_HIBAK.md` írja le.
"""

METHODS = """# Methods — the motif data core

*{cim_en} — open data core · data state: {datum} · DOI: {doi}*

## 1. What this dataset is

An open dataset of biblical motifs. A motif here is a recurring biblical theme whose presence in a verse can be
checked on the Hebrew or Greek text: on a word, a fixed phrase or a co-occurrence of words. The package contains
{mot} motifs with {elo} occurrences. The other side is recorded in the same detail: {kiz} exclusion rows give, with
a rationale, the passages that were examined but not assigned to the motif.

{adatmag_lexikon} The data core holds decisions and short rationales, not interpretive prose.

## 2. Defining a motif

A motif receives an identifier once four questions are answered: what carries its identity; what is the smallest
feature without which a passage does not belong to it (the exclusion criterion); if a passage belongs to two motifs,
does it play a different role in each; and is it a subset of another motif. Every motif also names the broader
concept towards which its boundary would dissolve (the superordinate concept). A passage connected only through
that concept is left out.

`motivumok.tsv` gives this in three columns: the carrier of identity (`azonossag_tipusa`; in this release
{tipus_en}), the exclusion criterion (`negativ_kriterium`) and the superordinate concept (`folerendelt_fogalom`).
The reader-facing definition (`meghatarozas`) says in one or two sentences what the motif is; in this release it is
given for {meghat} of the motifs and empty for the rest. The boundary of a motif, however, is drawn by the exclusions,
not by the definition.

## 3. Gathering candidates

Possible occurrences (candidates) are brought up by searches in a fixed order:

1. the Strong's numbers of the words shared by the core passages of the motif, without articles, conjunctions and
   other grammatical words;
2. a hypothesis of the semantic field: the only step not done by machine, so the words of the field are recorded;
3. a scan of the whole Old and New Testament by Strong's number, on the tagged STEPBible text (TAHOT, TAGNT);
4. two words occurring together in one verse;
5. a check of the verb form;
6. the Septuagint correspondence.

Steps 1 and 3–6 are run by programs and give the same result for the same input. Candidates also came from
cross-references (Treasury of Scripture Knowledge; the cross-references of the Károli edition, see
`KNOWN_ISSUES.md`), dictionary entries and editorial completeness surveys. Where a decided candidate came from is
given in the `keresesi_mod` column of `kizarasok.tsv` and `beepitesi_dontesek.tsv` ({keresesi_modok} search modes
in this release).

## 4. A decision on every candidate

A search hit never becomes an occurrence directly. Every candidate receives a decision with a rationale. An included
candidate goes to `elofordulasok.tsv`, the rationale of the decision to `beepitesi_dontesek.tsv` ({beep} rows); a
rejected one goes to `kizarasok.tsv`, with a reason ({okok} reasons) and a rationale.

Of the {kiz} exclusion rows, {kiz_egyedi} concern a single passage. {osszesito} rows are summary rows: each stands
for a group of verses rejected for the same reason; `kizaras_csoportok.tsv` lists the {csoport_vers} verses of the
groups, and the rationale of a summary row applies to every verse of its group.

If a search is empty, the result stays empty: a gap is not filled with weak or associative material. Candidates not
yet decided ({nyitva}) are not in the package. Where a row refers to an editorial decision, its public identifier
(`NYD-nnn`) can be resolved in `dontesnaplo.tsv` ({dontes} decisions).

## 5. The occurrence row

Every occurrence is a passage and names what its assignment rests on (`horgony_tipus`, `horgony`): {horgony_en}.
The `strong` column is the Strong's number of the anchor word, `jelentes_en` an excerpt of the dictionary sense,
and `strong_glossza_en` the short English STEPBible gloss.

**The Károli word.** {karoli_hol} the corresponding word of the Károli translation. The Károli word
is not evidence: it shows what the Hungarian reader sees of the passage. The pairing (`azonositas_modja`) was made
in {karoli_tartalom} cases by the editor reading the Károli text, in {karoli_gepi} cases by machine word alignment
(only a high-confidence pair may justify a row), and in {karoli_kovet} cases by inference. The confidence
(`megbizhatosag`) is high in {karoli_magas} cases and medium in {karoli_kozepes}. The alignment of the other words of
the verse is not part of this dataset; it is in the related Károli – Strong datasets.

**Provenance.** Every row names its origin: if it comes from a query, the type of query, the source, its licence and
the date; if not, that it is an editorial decision without a query. Of the {elo} occurrences, {kezi} are editorial
decisions and {lekerd} the direct result of a query. "Editorial decision" does not mean that the row is verified, only
that no single query produced it. For {tahot_igazolt} rows the Strong's assignment was traced item by item in the
Hebrew text of TAHOT (`igazolas`).

## 6. Processing stage

{lezart} motifs are closed releases ({lezart_lista}): their lexicon pages are released and passed the reader check
without error. The other {regi} were made at an earlier stage of the project with an older procedure. Their data are
in the current schema and pass the same check, but the reviews of the release procedure do not yet cover them, and
they may change in later versions. The stage is in the `feldolgozasi_allapot` column of `motivumok.tsv`; to work only
with the closed material, filter on it.

## 7. The echo layer

Four tables give the echo of the motifs in the ancient translations and interpreters, with the licence for each
source:

- `visszhang_megfelelok.tsv` ({vh_megf} rows): the counterparts of the anchor words in the Targum ({vh_targum}), the
  Vulgate ({vh_vulgata}) and the Septuagint ({vh_lxx});
- `visszhang_tanuk.tsv` ({vh_tanu} rows): patristic, rabbinic and Glossa Ordinaria witnesses: who, in which work,
  what they see in the passage, in one sentence in our own words, without quotation;
- `vitatott_forrasok.tsv` ({vit} rows): the peer-reviewed literature on the disputed points, bibliographic data only;
  an empty author means that no peer-reviewed source on the point was found in the databases searched;
- `sblgnt_apparatus.tsv` ({sbl} rows): the critical apparatus for the New Testament passages.

Only verified rows are included. Of the Septuagint counterparts, those where a single lemma comes into question in
the verse were checked by machine; every other row was reviewed by a second hand. Not in the package: the witnesses
of the Chain Lineage Browser (the browser states no licence), the cognate-language rows of the BDB (they await a
separate decision), and the text of the sources.

## 8. The English layer

Column names and values are Hungarian; English parallel columns stand next to them.

- **Passages:** next to every passage column, `…_osis`, with a standard OSIS key. The book code is standard; chapter
  and verse follow the versification of the Károli translation, and where this differs from the STEPBible numbering,
  the key denotes the Károli verse.
- **Closed values:** next to every closed-vocabulary column, `…_en`, with the edited English label of the codebook.
- **Free text** (rationale, function, the definition of the motif, the decision log): an `…_en` parallel field, a
  **machine translation** ({modellek_en}). The `forditas_modja` column of the row names the model and states any gap
  (the translation is missing wholly or in part in {nincs_ford} rows).

## 9. Licence filtering

The package takes values only from public-domain, CC0 or CC BY 4.0 sources, following the project's licence
inventory. {kizart_db} sources were excluded: those under a non-commercial or GPL licence, those with an unclear
licence, and the project's closed derived layers. The list of excluded sources and the reason for each are in
`ATTRIBUCIO.md` and `forrasok_es_licencek.tsv`. The semantic domains (UBS SDBH/SDGNT), under CC BY-SA 4.0, are in a
separate directory (`cc_by_sa_reteg/`), because the ShareAlike condition extends to work derived from them; the rest
of the package is independent of it. The inventory is not a legal opinion.

## 10. Use of artificial intelligence

The searches are deterministic programs. Whether a candidate belongs to the motif is decided in a working session
assisted by artificial intelligence, under the direction of the editor, and every decision is recorded with a
rationale. Machines also made the machine alignment of the Károli word (section 5), the English translation of the
free-text fields (section 8) and the check of the unambiguous Septuagint counterparts (section 7). The data tables
are produced from the data by a program, not written by a language model; the same data always yield the same
package. The descriptive texts (these methods, the read-me and the announcement) were drafted by a language model,
the numbers come from the export, and the text was approved by the editor. The model is not an author; the author is
responsible for the content.

## 11. Verification

The package's own automatic check runs before every release. It measures internal working marks, codebook coverage
(every column and closed value, in both languages), licence filtering, the resolution of decision and motif
references, the member counts of summary rows, the OSIS keys, the freshness of the translation, and byte-identical
regeneration. `ELLENORZO_OSSZEG.sha256` contains the SHA-256 sum of every released file; the content hash in
`RELEASE.txt` is the sum of that list.

On a released lexicon page the reader check requires zero errors. The changes of every step of the work are
re-checked by a fresh-context model with its own queries; the boundary of the motif is reviewed by a second model.
This is not independent peer review: apart from the author, every checker is a program or a language model.

## 12. Limitations

- Only {lezart} motifs are closed releases; {regi} come from an earlier stage (section 6).
- Completeness is not proven. The searches measure how much the list catches on lexical features; thematic links
  are not measured.
- There was no independent peer review and no inter-annotator agreement measurement.
- The motifs were chosen by the research programme; they are not a representative sample of the Bible.
- The known errors of the source data and their handling are described in `KNOWN_ISSUES.md`.
"""


def modszer(sz, adatmag_lexikon):
    return MODSZER.format(adatmag_lexikon=adatmag_lexikon, **fmt(sz, 'hu'))


def methods(sz, adatmag_lexikon_en):
    return METHODS.format(adatmag_lexikon=adatmag_lexikon_en, **fmt(sz, 'en'))


# ----------------------------------------------------------------------------------- ATTRIBUCIO

# A csomagban forrásként szereplő datasetek leírása (magyar összetevő, magyar megjegyzés, angol összetevő, angol
# megjegyzés). A licenc-címke a leltárból jön (`forrasok_es_licencek.tsv`); ha egy forrás-szerepű datasetnek itt
# nincs leírása, az export megáll.
FORRAS_LEIRAS = {
    'Karoli_1908': ('Károli Gáspár fordítása, 1908-as kiadás', 'a Károli-szó; közkincs a szöveg kora miatt',
                    "Gáspár Károli's translation, 1908 edition", 'the Károli word; public domain by age'),
    'TAHOT': ('STEPBible TAHOT (héber Ószövetség, Strong-számokkal)', 'a Strong-számok és a teljes szöveges keresés',
              "STEPBible TAHOT (Hebrew Old Testament with Strong's numbers)", "Strong's numbers and full-text search"),
    'TAGNT': ('STEPBible TAGNT (görög Újszövetség, Strong-számokkal)', 'a Strong-számok és a teljes szöveges keresés',
              "STEPBible TAGNT (Greek New Testament with Strong's numbers)", "Strong's numbers and full-text search"),
    'TBESH': ('STEPBible TBESH (rövid héber szótár)', 'a `strong_glossza_en` angol glosszája',
              'STEPBible TBESH (brief Hebrew lexicon)', 'the English gloss in `strong_glossza_en`'),
    'TBESG': ('STEPBible TBESG (rövid görög szótár)', 'a `strong_glossza_en` angol glosszája',
              'STEPBible TBESG (brief Greek lexicon)', 'the English gloss in `strong_glossza_en`'),
    'TSK': ('Treasury of Scripture Knowledge (OpenBible.info)', 'kereszthivatkozás-alapú jelöltek',
            'Treasury of Scripture Knowledge (OpenBible.info)', 'cross-reference candidates'),
    'LXX_OS': ('OpenScriptorium LXX-morph (Septuaginta, Rahlfs)', 'a Septuaginta-megfelelők; a Rahlfs-szöveg közkincs',
               'OpenScriptorium LXX-morph (Septuagint, Rahlfs)', 'the Septuagint counterparts; the Rahlfs text is '
               'public domain'),
    'Targum_PD': ('Targum Onkelos és Jonatán (a Sefaria által közölt közkincs kiadás)', 'versenként egy-egy szóalak; '
                  'a Sefaria-kiadás szövegéből a csomag mást nem tartalmaz', 'Targum Onkelos and Jonathan (the '
                  'public-domain edition published by Sefaria)', 'one word form per verse; the package contains '
                  'nothing else from the text of the Sefaria edition'),
    'Vulgata_Clementina': ('Vulgata Clementina (1598)', 'a Vulgata-megfelelők', 'Clementine Vulgate (1598)',
                           'the Vulgate counterparts'),
    'Glossa_Ordinaria': ('Glossa Ordinaria (Migne, 1880)', 'tanú-sor: metaadat és saját mondat',
                         'Glossa Ordinaria (Migne, 1880)', 'witness row: metadata and a sentence of our own'),
    'Tanu_atyak_index': ('HistoricalChristianFaith kommentár-adatbázis', 'egyházatyai tanúk metaadata; a gyűjtemény '
                         'közkincs-nyilatkozata a kompilációra és a metaadatra szól, az idézetszövegek nincsenek a '
                         'csomagban', 'HistoricalChristianFaith commentaries database', 'metadata of the patristic '
                         "witnesses; the collection's public-domain dedication covers the compilation and the "
                         'metadata, the quotation texts are not in the package'),
    'Tanu_rabbinikus_index': ('Sefaria kapcsolat-adatkészlet', 'a rabbinikus tanú metaadata (szűrés és '
                              'Károli-átvezetés); a Sefaria szövegéből a csomag semmit nem tartalmaz',
                              "Sefaria's links dataset", 'metadata of the rabbinic witness (filtering and conversion '
                              'to Károli numbering); the package contains nothing of the Sefaria text'),
    'SBLGNT_apparatus': ('SBL Greek New Testament, kritikai apparátus', 'az `sblgnt_apparatus.tsv` jegyzetei',
                         'SBL Greek New Testament, critical apparatus', 'the notes of `sblgnt_apparatus.tsv`'),
}

STEP_ATTRIBUCIO = 'Data created by www.STEPBible.org based on work at Tyndale House Cambridge (CC BY 4.0)'
SBLGNT_ATTRIBUCIO = ('SBL Greek New Testament, Copyright 2010 Society of Biblical Literature and Logos Bible '
                     'Software (CC BY 4.0), https://sblgnt.com')


def attribucio(sz, forrasok, kizartak):
    """`forrasok`: [(dataset, licenc-címke magyarul, licenc-címke angolul)] a forrás-szerepű datasetekre."""
    hianyzik = [ds for ds, _, _ in forrasok if ds not in FORRAS_LEIRAS]
    if hianyzik:
        raise SystemExit('ATTRIBUCIO: forrás-szerepű dataset leírás nélkül: %s' % ', '.join(hianyzik))
    rend = list(FORRAS_LEIRAS)
    forrasok = sorted(forrasok, key=lambda x: rend.index(x[0]))
    f_hu, f_en = fmt(sz, 'hu'), fmt(sz, 'en')
    kiz = ', '.join('`%s`' % k for k in kizartak)
    ki = ['# Forrásmegjelölés és licencek / Attribution and licences', '', MD_FEJLEC % f_hu['cim_hu'], '',
          '## Magyarul', '',
          '| összetevő | licenc | szerepe a csomagban |', '|---|---|---|',
          '| a motívumadatok, a döntések és indoklásuk, a kódkönyv, a leíró szövegek | CC BY 4.0 | a projekt saját '
          'munkája ({szerzo}) |'.format(**f_hu)]
    ki += ['| %s | %s | %s |' % (FORRAS_LEIRAS[ds][0], hu, FORRAS_LEIRAS[ds][1]) for ds, hu, _ in forrasok]
    ki += ['| UBS SDBH és SDGNT (szemantikai domének) | CC BY-SA 4.0 | csak a `cc_by_sa_reteg/` könyvtárban; a szó '
           'szerinti forrásmegjelölés az ottani `OLVASSEL.md`-ben |', '',
           'A STEPBible-adatok (TAHOT, TAGNT, TBESH, TBESG) kötelező forrásmegjelölése, szó szerint:', '',
           '> ' + STEP_ATTRIBUCIO, '',
           'Az SBL Greek New Testament apparátusáé:', '', '> ' + SBLGNT_ATTRIBUCIO, '',
           'A csomag a források szövegét nem tartalmazza: a héber és görög szövegből Strong-számok és az indoklásokban '
           'említett egyes szavak állnak benne, a visszhang-forrásokból egy-egy szóalak, metaadat és saját szavas egy '
           'mondat. A Chain Lineage '
           'Browser adatai nincsenek a csomagban (a böngésző licencet nem közöl).', '',
           '**Kizárt források** ({kizart_db}; a csomag értéket nem tartalmaz belőlük): '.format(**f_hu) + kiz +
           '. Okuk soronként a `forrasok_es_licencek.tsv` `ok` oszlopában áll (nem kereskedelmi vagy GPL licenc, '
           'tisztázatlan licenc, a projekt zárt származtatott rétege). Ez leltár, nem jogi vélemény.', '',
           '## In English', '',
           '| component | licence | role in the package |', '|---|---|---|',
           "| the motif data, the decisions and their rationale, the codebook, the descriptive texts | CC BY 4.0 | the "
           "project's own work ({szerzo}) |".format(**f_en)]
    ki += ['| %s | %s | %s |' % (FORRAS_LEIRAS[ds][2], en, FORRAS_LEIRAS[ds][3]) for ds, _, en in forrasok]
    ki += ['| UBS SDBH and SDGNT (semantic domains) | CC BY-SA 4.0 | only in the `cc_by_sa_reteg/` directory; the '
           'verbatim attribution is in the `OLVASSEL.md` there |', '',
           'Required attribution of the STEPBible data (TAHOT, TAGNT, TBESH, TBESG), verbatim:', '',
           '> ' + STEP_ATTRIBUCIO, '',
           'Of the SBL Greek New Testament apparatus:', '', '> ' + SBLGNT_ATTRIBUCIO, '',
           'The package does not contain the text of the sources: of the Hebrew and Greek text it holds Strong\'s '
           'numbers and single words mentioned in the rationales, of the echo sources a single word form, metadata and '
           'one sentence in our own words. No data of the Chain Lineage Browser are included (the browser states no licence).', '',
           '**Excluded sources** ({kizart_db}; the package contains no value from them): '.format(**f_en) + kiz +
           '. The reason for each is in the `ok` column of `forrasok_es_licencek.tsv` (non-commercial or GPL licence, '
           "unclear licence, the project's closed derived layer). This is an inventory, not a legal opinion.", '']
    return '\n'.join(ki)


# ----------------------------------------------------------------------------------- LICENSE, CITATION, .gitattributes

LICENSE = """{cim_hu} — nyílt adatmag / {cim_en} — open data core
Copyright (c) 2026 {szerzo}

A csomag saját része (a motívumadatok, a döntések és indoklásuk, a kódkönyv és a leíró szövegek) licence:
The package's own part (the motif data, the decisions and their rationale, the codebook and the descriptive texts)
is licensed under:

Creative Commons Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/

Kivétel: a cc_by_sa_reteg/ könyvtár tartalma CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/).
Exception: the contents of the cc_by_sa_reteg/ directory are under CC BY-SA 4.0.

A felhasznált külső adatok licence és forrásmegjelölése: ATTRIBUCIO.md.
Licences and attribution of the third-party data used: ATTRIBUCIO.md.

A lexikon (értelmező szövege, a szótárak magyar fordítása és a kötet) önálló mű, minden jog fenntartva; nem része
ennek a csomagnak.
The lexicon (its interpretive text, the Hungarian translation of the dictionaries and the volume) is a separate
work, all rights reserved; it is not part of this package.
"""

CITATION = """cff-version: 1.2.0
message: "Ha az adatokat használja, kérjük, ezt az adatkészletet idézze. / If you use the data, please cite this dataset."
type: dataset
title: "{cim_hu} — nyílt adatmag: bibliai motívumok / {cim_en} — open data core: biblical motifs"
authors:
  - family-names: "{csaladnev}"
    given-names: "{utonev}"
    orcid: "https://orcid.org/{orcid}"
doi: "{doi}"
license:
  - CC-BY-4.0
  - CC-BY-SA-4.0
abstract: >-
  Bibliai motívumok nyílt adatkészlete: {mot} motívum, {elo_hu} előfordulás és {kiz_hu}
  kizárás-sor. Minden motívumhoz rögzített kizáró jegy és a tágabb fogalom
  tartozik, amely felé hígulna; minden előfordulás a héber vagy görög szöveg
  egy szaván áll, mellette a Károli-fordítás szavával; a megvizsgált, de
  kizárt helyek indoklással szerepelnek; minden sor megnevezi az eredetét. A
  szemantikai domének külön rétege CC BY-SA 4.0, a csomag többi része CC BY
  4.0. A nyílt adatmag a lexikon adatrétege; maga a lexikon önálló mű, minden
  jog fenntartva.
  (English) An open dataset of biblical motifs: {mot} motifs, {elo_en} occurrences and
  {kiz_en} exclusion rows. Every motif has a fixed exclusion criterion and the broader
  concept towards which it would dilute; every occurrence rests on a word of
  the Hebrew or Greek text, with the word of the Károli translation; passages
  examined but excluded are listed with a rationale; every row names its
  origin. The separate layer of semantic domains is under CC BY-SA 4.0, the
  rest of the package under CC BY 4.0. The open data core is the data layer
  of the lexicon; the lexicon itself is a separate work, all rights reserved.
keywords:
  - bibliai motívumok
  - kizárási döntések
  - Károli-biblia
  - biblical motifs
  - intertextuality
  - Hebrew Bible
  - New Testament
  - Septuagint
references:
  - type: dataset
    title: "Károli 1908 – Strong szóillesztés / Károli 1908 – Strong word alignment"
    authors:
      - family-names: "{csaladnev}"
        given-names: "{utonev}"
    doi: "{doi_karoli_strong}"
  - type: dataset
    title: "Modernizált Károli – Strong / Modernised Károli – Strong"
    authors:
      - family-names: "{csaladnev}"
        given-names: "{utonev}"
    doi: "{doi_karoli_modern}"
  - type: generic
    title: "{cim_hu} / {cim_en}"
    authors:
      - family-names: "{csaladnev}"
        given-names: "{utonev}"
    url: "https://{domain}"
    abstract: >-
      A lexikon, önálló mű: értelmező szövege, a szótárak magyar fordítása és a
      kötet. Minden jog fenntartva. (English) The lexicon, a separate work: its
      interpretive text, the Hungarian translation of the dictionaries and the
      volume. All rights reserved.
"""

GITATTRIBUTES = """# Sorvég: minden fájl LF-fel, minden checkouton (az ellenőrző összeg az LF-es bájtokra szól).
* text eol=lf
# A közlemény-tervezet a megjelenésig nem része a kiadásnak.
kozlemeny/ export-ignore
"""


def license_(sz):
    return LICENSE.format(**fmt(sz, 'hu'))


def citation(sz):
    f = fmt(sz, 'hu')
    f.update(elo_hu=ezres(sz['elo'], 'hu'), kiz_hu=ezres(sz['kiz'], 'hu'),
             elo_en=ezres(sz['elo'], 'en'), kiz_en=ezres(sz['kiz'], 'en'))
    return CITATION.format(**f)


# ----------------------------------------------------------------------------------- közlemény

KOZLEMENY_HU = """# Kizárva, okkal: bibliai motívumok nyílt adatkészlete

*Közlemény-tervezet · {cim_hu} — nyílt adatmag · DOI: {doi}*

Mikor tartozik egy vers egy bibliai motívumhoz, és mikor nem? A {cim_hu} szabad licenccel közreadja motívumkutatása
adatrétegét. Nemcsak azt rögzíti, hol fordul elő egy motívum, hanem azt is, melyik helyet vizsgálta meg, és miért
hagyta ki.

**Mi van benne.** {mot} motívum, köztük {lezart_cimkek}, összesen {elo} előfordulással. Minden előfordulás a héber
vagy a görög szöveg egy szaván áll, mellette a Károli-fordítás megfelelő szavával. A kizárások ugyanilyen részletesek:
{kiz_egyedi} egyenként eldöntött hely és {csoport_vers} csoportban elutasított vers, {okok} okkal és indoklással.

**Hogyan.** Minden motívum négy kérdéssel indul, és a legfontosabb közülük az, hogy mi az a legkisebb jegy, amely
nélkül egy hely nem tartozik ide. A jelölteket hat, rögzített sorrendű keresés hozza elő a héber és a görög
szövegből; öt közülük program, ugyanarra a bemenetre mindig ugyanazt adja, a hatodik, a szemantikai mező feltevése
emberi lépés, ezért a szavait rögzítjük. Találatból nem lesz közvetlenül előfordulás: minden jelöltről döntés
születik indoklással, és ezt a döntést mesterséges intelligenciával segített szerkesztői munkamenet hozza meg. A
„nem” ugyanúgy megmarad, mint az „igen”: az elutasított hely okot és indoklást kap, így a motívum határát nem a
meghatározása rajzolja meg, hanem a kizárásai. Minden sor megnevezi, honnan származik, lekérdezésből vagy kézi
döntésből. Ahol pedig a keresés üres volt, az adat is üres marad, mert az üres eredmény is eredmény.

**Az ókori visszhang.** Egyes motívumoknál a kulcsszavak megfelelője is szerepel a Targumban, a Vulgatában és a
Septuagintában, egyházatyai és rabbinikus tanúkkal, idézet nélkül, forrásonként a licenccel.

**Állapot.** {lezart} motívum lezárt kiadás; {regi} egy korábbi feldolgozásból való, és a későbbi változatokban
frissül. Az állapot motívumonként az adatban áll, így a lezárt anyag külön is használható.

**Kinek.** Kutatóknak, akik bibliai intertextualitást vizsgálnak, és a felvétel mellett a kizárás dokumentált nyomát
is látni akarják; a magyar fordítástörténet kutatóinak, akik a Károli szóválasztását az eredeti szóval együtt
vizsgálnák; fejlesztőknek, akik indokolt felvételeket és kizárásokat használnának próbaanyagként.

Az adatkészlet CC BY 4.0 licenccel szabadon felhasználható (a szemantikai domének külön rétege CC BY-SA 4.0):
https://doi.org/{doi}
"""

KOZLEMENY_EN = """# Excluded, with reasons: an open dataset of biblical motifs

*Announcement draft · {cim_en} — open data core · DOI: {doi}*

When does a verse belong to a biblical motif, and when does it not? The {cim_en} releases the data layer of its motif
research under an open licence. It records not only where a motif occurs, but also which passages were examined
and why they were left out.

**What is in it.** {mot} motifs, among them {lezart_cimkek}, with {elo} occurrences in all. Every occurrence rests on
a word of the Hebrew or Greek text, with the corresponding word of the Károli translation beside it. The exclusions
are just as detailed: {kiz_egyedi} passages decided one by one and {csoport_vers} verses rejected in groups, with
{okok} reasons and a rationale.

**How.** Every motif starts with four questions, and the most important of them is this: what is the smallest
feature without which a passage does not belong here? Candidates are brought up from the Hebrew and the Greek text
by six searches in a fixed order; five of them are programs and always give the same result for the same input, while
the sixth, the hypothesis of the semantic field, is a human step, so its words are recorded. A hit never becomes an
occurrence directly: every candidate receives a decision with a rationale, and that decision is made in an editorial
working session assisted by artificial intelligence. The “no” is kept just as the “yes” is: a rejected passage
receives a reason and a rationale, so the boundary of the motif is drawn not by its definition but by its
exclusions. Every row names its origin, a query or a decision made by hand. And where a search was empty, the data
stay empty, because an empty result is a result too.

**The ancient echo.** For some motifs the counterparts of the key words in the Targum, the Vulgate and the
Septuagint are included, with patristic and rabbinic witnesses, without quotation, and with the licence of each
source.

**Status.** {lezart} motifs are closed releases; {regi} come from an earlier stage and will be updated in later
versions. The status of each motif is part of the data, so the closed material can be used on its own.

**For whom.** Researchers of biblical intertextuality who want to see the documented trace of exclusion as well as
of inclusion; researchers of Hungarian translation history who would study Károli's word choices together with the
original word; developers who would use reasoned inclusions and exclusions as test material.

The dataset is freely usable under CC BY 4.0 (the separate layer of semantic domains is under CC BY-SA 4.0):
https://doi.org/{doi}
"""


def kozlemeny_hu(sz):
    return KOZLEMENY_HU.format(**fmt(sz, 'hu'))


def kozlemeny_en(sz):
    return KOZLEMENY_EN.format(**fmt(sz, 'en'))
