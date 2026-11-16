# -*- coding: utf-8 -*-
"""
karoli_egyutt.py -- a két nyílt Károli-csomag README-jének és OLVASSEL-jének „A két adatkészlet együtt” szakasza
(F175.N). A szakasz minden példasora a generált adatból jön (a két exportáló saját átalakító függvényével, egy
versre szűkítve), kézzel írt példa nincs benne.

Kör-importot kerül: az exportálók a `szakasz()`-t hívják, a szakasz pedig a hívás pillanatában importálja a két
exportálót (addigra mindkettő betöltött). A példa eredménye gyorsítótárban áll (egy folyamatban egyszer fut).

TSV-olvasás `split('\\t')`, írás `'\\t'.join()` (nem `csv`).
"""
import functools
import os

VERS = '1Móz 1:1'                 # a példa verse (Károli-kulcs)
OSIS = 'Gen.1.1'
KONYV_FAJL = '01_Gen.tsv'
KONYV_FORRAS = '1Moz'             # az adat/karoli_strong/parok_1Moz.tsv, szavak_1Moz.tsv
SZAVAK_DB = 3                     # a példa magyar szavai (token <= 3)
FORRAS_DB = 5                     # a példa eredeti szavai (token <= 5)


@functools.lru_cache(maxsize=1)
def pelda():
    """A példa sorai a két csomag táblájának alakjában: (parok, konyvek, er_szavak) listák."""
    import karoli_strong_export as KS
    import karoli_modern_export as KM
    ks_dir = os.path.dirname(KS.PAROK)
    parok = [p for p in KS.tsv('%s/parok_%s.tsv' % (ks_dir, KONYV_FORRAS))[1] if p['vers'] == VERS]
    szavak = [s for s in KS.tsv('%s/szavak_%s.tsv' % (ks_dir, KONYV_FORRAS))[1] if s['vers'] == VERS]
    versek = [v for v in KS.tsv(KS.KAROLI)[1] if v['Igehely'] == VERS]
    if not parok or not szavak or len(versek) != 1:
        raise SystemExit('egyutt: a példa verse (%s) nincs a forrástáblákban' % VERS)
    konyvek, _ = KS.atalakit(versek, parok, szavak, [])
    (kk, ps, ss), = konyvek
    # a modernizált csomag sorai ugyanarra a versre
    modern = [t for t in KM.tsv(KM.MODERN)[1] if t['igehely'] == VERS]
    mparok = {}
    for p in parok:
        mparok.setdefault((p['vers'], p['hu_sorszam']), []).append(p)
    allapot = {(s['vers'], s['sorszam']): s for s in szavak if s['oldal'] == 'hu'}
    mk = KM.vetit(modern, mparok, allapot)
    (mkk, msorok), = mk
    if kk != mkk or not OSIS.startswith(kk + '.'):
        raise SystemExit('egyutt: a két csomag könyve eltér')
    ki_par = [s for s in ps if int(s[1]) <= SZAVAK_DB]
    ki_mod = [s for s in msorok if int(s[1]) <= SZAVAK_DB]
    ki_er = [s for s in ss if s[1] == 'er' and int(s[2]) <= FORRAS_DB]
    if not ki_par or not ki_mod or not ki_er:
        raise SystemExit('egyutt: üres példa')
    return ki_par, ki_mod, ki_er


def _tabla(fej, sorok):
    ki = ['| ' + ' | '.join('`%s`' % f for f in fej) + ' |', '|' + '---|' * len(fej)]
    ki += ['| ' + ' | '.join(sor) + ' |' for sor in sorok]
    return '\n'.join(ki)


def tablak():
    """A három példatábla (markdown) és a nem fordított eredeti szavak (n, strong) a példában."""
    ps, ms, es = pelda()
    t_par = _tabla(['token', 'alak_1908', 'eredeti_token', 'strong', 'kapcsolat'],
                   [[s[1], s[2], s[3], s[4], s[5]] for s in ps])
    # modern: osis, token, alak_1908, alak_modern, valtozott, kieso, gazda_token, bizonytalan, allapot, strong,
    # eredeti_token, kapcsolat
    t_mod = _tabla(['token', 'alak_1908', 'alak_modern', 'valtozott', 'eredeti_token', 'strong', 'kapcsolat'],
                   [[s[1], s[2], s[3], s[4], s[10], s[9], s[11]] for s in ms])
    t_er = _tabla(['token', 'allapot', 'partner_token', 'strong'], [[s[2], s[4], s[5], s[6]] for s in es])
    fordit = [(s[2], s[6]) for s in es if s[4] == 'forditatlan']
    return t_par, t_mod, t_er, fordit


SZEKCIO_EN = """## Using the two datasets together

This dataset and {masik_en} (https://doi.org/{masik_doi}) describe the same words of the 1908 text and can be joined
row by row.

- **Common key.** `osis` + `token`: the position of a word in the 1908 text. {kulcs_en}
- **Reading the modernised text.** Take the rows of `data/konyvek/NN_Konyv.tsv` with an empty `kieso` column in `token`
  order, once per word, and read `alak_modern`. A row with a `kieso` value is a word that drops out of the modern text;
  its `gazda_token` is the position of the host word in the same verse, and its Strong's number belongs to that host
  word in the modern text.
- **The source side.** The complete list of the source words, including the Hebrew and Greek words that the Károli
  does not translate with a separate Hungarian word, is only in {szavak_en}; join it on `osis` + `eredeti_token`.

**Example: Genesis 1:1 (`Gen.1.1`), the first three words.** Word alignment (`data/parok/{fajl}`):

{t_par}

The modernised dataset (`data/konyvek/{fajl}`), the same words:

{t_mod}

The source words, the first five (`data/szavak/{fajl}`, `oldal` = `er`):

{t_er}
{fordit_en}"""

SZEKCIO_HU = """## A két adatkészlet együtt

Ez az adatkészlet és {masik_hu} (https://doi.org/{masik_doi}) az 1908-as szöveg ugyanazon szavait írja le, és sorról
sorra összekapcsolható.

- **Közös kulcs.** Az `osis` + `token` az 1908-as szöveg szavának helye. {kulcs_hu}
- **A modern szöveg olvasása.** A `data/konyvek/NN_Konyv.tsv` sorai közül a `kieso` oszlop üres soraiból, `token`
  sorrendben, szavanként egyszer olvasható az `alak_modern`. A `kieso` oszlopban értéket hordozó sor olyan szó, amely a
  modern szövegből kiesik; a `gazda_token` a gazdaszó helye ugyanabban a versben, és a Strong-száma a modern szövegben
  a gazdaszóhoz tartozik.
- **A forrásoldal teljes listája.** Az eredeti szavak teljes listája, köztük azokkal a héber és görög szavakkal,
  amelyeket a Károli magyarul külön szóval nem fordít, csak {szavak_hu}; az `osis` + `eredeti_token` szerint kapcsolható.

**Példa: 1Móz 1:1 (`Gen.1.1`), az első három szó.** A szóillesztés (`data/parok/{fajl}`):

{t_par}

A modernizált adatkészlet (`data/konyvek/{fajl}`), ugyanezek a szavak:

{t_mod}

Az eredeti szavak, az első öt (`data/szavak/{fajl}`, `oldal` = `er`):

{t_er}
{fordit_hu}"""

# csomagonként: a másik adatkészlet neve és a kulcs-/forrásoldal mondatai
SOROK = {
    'strong': {
        'masik_en': 'Modernised Károli – Strong', 'masik_hu': 'a Modernizált Károli – Strong',
        'kulcs_en': ('A row of `data/konyvek/NN_Konyv.tsv` in the modernised dataset extends the rows of '
                     '`data/parok/NN_Konyv.tsv` here: the same `token`, `eredeti_token`, `strong` and `kapcsolat`, '
                     'and next to them `alak_modern`, `valtozott`, `kieso` and `gazda_token`. A word without a pair '
                     'has one row there, with empty `strong` and `eredeti_token`.'),
        'kulcs_hu': ('A modernizált adatkészlet `data/konyvek/NN_Konyv.tsv` sora ennek az adatkészletnek a '
                     '`data/parok/NN_Konyv.tsv` soraiból bővül: ugyanaz a `token`, `eredeti_token`, `strong` és '
                     '`kapcsolat`, mellette az `alak_modern`, a `valtozott`, a `kieso` és a `gazda_token`. A pár '
                     'nélküli szónak ott egy sora van, üres `strong` és `eredeti_token` oszloppal.'),
        'szavak_en': 'the `data/szavak/NN_Konyv.tsv` table of this dataset (`oldal` = `er`)',
        'szavak_hu': 'ennek az adatkészletnek a `data/szavak/NN_Konyv.tsv` táblájában van (`oldal` = `er`)',
    },
    'modern': {
        'masik_en': 'Károli 1908 – Strong word alignment', 'masik_hu': 'a Károli 1908 – Strong szóillesztés',
        'kulcs_en': ('A row of `data/konyvek/NN_Konyv.tsv` here extends the rows of `data/parok/NN_Konyv.tsv` of the '
                     'word alignment dataset: the same `token`, `eredeti_token`, `strong` and `kapcsolat`, and next '
                     'to them `alak_modern`, `valtozott`, `kieso` and `gazda_token`. A word without a pair has one '
                     'row here, with empty `strong` and `eredeti_token`.'),
        'kulcs_hu': ('Ennek az adatkészletnek a `data/konyvek/NN_Konyv.tsv` sora a szóillesztés '
                     '`data/parok/NN_Konyv.tsv` soraiból bővül: ugyanaz a `token`, `eredeti_token`, `strong` és '
                     '`kapcsolat`, mellette az `alak_modern`, a `valtozott`, a `kieso` és a `gazda_token`. A pár '
                     'nélküli szónak itt egy sora van, üres `strong` és `eredeti_token` oszloppal.'),
        'szavak_en': 'the `data/szavak/NN_Konyv.tsv` table of the word alignment dataset (`oldal` = `er`), not in this one',
        'szavak_hu': 'a szóillesztés `data/szavak/NN_Konyv.tsv` táblájában van (`oldal` = `er`), ebben az adatkészletben nincs',
    },
}


def szakasz(csomag, nyelv):
    """A szakasz szövege (markdown), a `csomag` (`strong`/`modern`) és a `nyelv` (`hu`/`en`) szerint."""
    import karoli_strong_export as KS
    s = SOROK[csomag]
    t_par, t_mod, t_er, fordit = tablak()
    masik_doi = KS.DOI_MODERN if csomag == 'strong' else KS.DOI
    if fordit:
        n, strong = fordit[0]
        fordit_en = ('\nSource word %s (`%s`) has `allapot` = `forditatlan`: it has no row in `data/parok/`, and appears '
                     'only in `data/szavak/`.\n' % (n, strong))
        # a névelőt a hívó exportáló nevelo_javit()-ja igazítja a szám kiejtéséhez
        fordit_hu = ('\nA %s. eredeti szó (`%s`) `allapot` oszlopa `forditatlan`: a `data/parok/` táblában nincs '
                     'sora, csak a `data/szavak/` táblában szerepel.\n' % (n, strong))
    else:
        fordit_en = fordit_hu = ''
    adat = dict(masik_doi=masik_doi, fajl=KONYV_FAJL, t_par=t_par, t_mod=t_mod, t_er=t_er)
    if nyelv == 'hu':
        return SZEKCIO_HU.format(masik_hu=s['masik_hu'], kulcs_hu=s['kulcs_hu'], szavak_hu=s['szavak_hu'],
                                 fordit_hu=fordit_hu, **adat).rstrip('\n')
    return SZEKCIO_EN.format(masik_en=s['masik_en'], kulcs_en=s['kulcs_en'], szavak_en=s['szavak_en'],
                             fordit_en=fordit_en, **adat).rstrip('\n')
