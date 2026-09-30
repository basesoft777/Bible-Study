"""S1.7 (F05_SZOTAR_BRIEF.md): heber kiejtes-jeloltek a D28 hatokoru 26 lemmara.

Bemenet: a 9 motivum (adat/elofordulasok.tsv `strong` mezoje, `+`-on
szetbontva, H-prefixummal) egyedi Strong-halmaza, es minden Strong OSHL
"atiras" mezoje + pontozott "lemma" mezoje (konkordancia/
OSHL_lexikalis_index.tsv).

A jelolt harom lepesben keszul (a felhasznaloi ALLJ utani javitas, D34-D37):
  1. begadkefat-spirantizacio (D34): a pontozott lemma alapjan a
     ב/כ/פ betuk lagy (v/ch/f) vagy kemeny (b/k/p) valtozatra cserelve
     az ATIRAS-ban, MIELOTT a szabalytabla lefutna (az OSHL "atiras" maga
     ezt nem kulonbozteti meg, mindig sima b/k/p-t ad).
  2. adat/kiejtes_heber_jeloltszabalyok.tsv szekvencialis, literalis
     csereje (aleph/ajin elesik, š/ṣ/ṭ/ḥ/q/y atirasa, hosszu/redukalt
     maganhangzok).
  3. adat/kiejtes_heber_kivetelek.tsv kezi felulbiralasai (D36, pl. H2555).

NEM ir a kivetel-tablaba (adat/kiejtes_kivetelek.tsv) -- csak jelolt-listat
allit elo kezi jovahagyasra (F05_SZOTAR_BRIEF.md §3 S1.7, ÁLLJ).

Kimenet: naplok/SZOTAR_S1_heber_jeloltek.tsv.

TSV-kezeles kizarolag split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ELOFORDULASOK = os.path.join(ROOT, 'adat', 'elofordulasok.tsv')
OSHL = os.path.join(ROOT, 'konkordancia', 'OSHL_lexikalis_index.tsv')
SZABALYOK = os.path.join(ROOT, 'adat', 'kiejtes_heber_jeloltszabalyok.tsv')
HEBER_KIVETELEK = os.path.join(ROOT, 'adat', 'kiejtes_heber_kivetelek.tsv')
KIVETELEK = os.path.join(ROOT, 'adat', 'kiejtes_kivetelek.tsv')
KIMENET = os.path.join(ROOT, 'naplok', 'SZOTAR_S1_heber_jeloltek.tsv')

# Begadkefat-betuk (D34): heber Unicode-pont -> (vegso/nem-vegso alak, lagy atirasa).
BEGADKEFAT = {
    'ב': ('b', 'v'),   # bet -> b (kemeny) / v (lagy)
    'כ': ('k', 'ch'),  # kaf -> k (kemeny) / ch (lagy)
    'ך': ('k', 'ch'),  # kaf szo-vegi alak (final kaf) -- csak dagesh-detektalashoz
    'פ': ('p', 'f'),   # pe -> p (kemeny) / f (lagy)
    'ף': ('p', 'f'),   # pe szo-vegi alak (final pe)
}
DAGESH = 'ּ'
HEB_LETTER_LO, HEB_LETTER_HI = 'א', 'ת'


def sorok_beolvas(ut, fejlec_eleji_kulcs):
    """[dict] -- az elso, `fejlec_eleji_kulcs\\t`-vel kezdodo sortol, a
    kommentsorok (# vagy ures) kihagyasaval."""
    with open(ut, encoding='utf-8') as f:
        nyers = [l.rstrip('\n\r') for l in f]
    fejlec_idx = None
    for i, sor in enumerate(nyers):
        if sor.startswith(fejlec_eleji_kulcs + '\t') or sor == fejlec_eleji_kulcs:
            fejlec_idx = i
            break
    if fejlec_idx is None:
        raise ValueError('nincs fejlecsor %r-vel a %s fajlban' % (fejlec_eleji_kulcs, ut))
    fejlec = nyers[fejlec_idx].split('\t')
    ki = []
    for sor in nyers[fejlec_idx + 1:]:
        if not sor or sor.startswith('#'):
            continue
        mezok = sor.split('\t')
        ki.append(dict(zip(fejlec, mezok)))
    return ki


def h_tokenek_a_9_motivumbol():
    """{strong: set(motivum_id)} -- a `strong` mezo `+`-on szetbontva, csak
    a H-kezdetu tokenek, a lexikon_general.py strong_tokens logikajaval
    egyezoen."""
    sorok = sorok_beolvas(ELOFORDULASOK, 'id')
    tokenek = {}
    for sor in sorok:
        motivum_id = sor.get('id', '')
        strong_mezo = sor.get('strong', '') or ''
        for tok in strong_mezo.split('+'):
            tok = tok.strip()
            if tok.startswith('H') and tok:
                tokenek.setdefault(tok, set()).add(motivum_id)
    return tokenek


def oshl_index():
    """{strong: [dict, ...]} -- az OSHL_lexikalis_index.tsv sorai
    Strong-onkent csoportositva, a fajl eredeti (oshl_id-szerinti)
    sorrendjeben."""
    sorok = sorok_beolvas(OSHL, 'strong')
    idx = {}
    for sor in sorok:
        idx.setdefault(sor['strong'], []).append(sor)
    return idx


def szabalytabla_betolt():
    """[(minta, csere)] -- sorszam szerint rendezve."""
    sorok = sorok_beolvas(SZABALYOK, 'sorszam')
    sorok.sort(key=lambda r: int(r['sorszam']))
    return [(r['minta'], r.get('csere', '') or '') for r in sorok]


def heber_kivetelek_betolt():
    """{strong: ertek} -- adat/kiejtes_heber_kivetelek.tsv (D36)."""
    if not os.path.exists(HEBER_KIVETELEK):
        return {}
    sorok = sorok_beolvas(HEBER_KIVETELEK, 'strong')
    return {r['strong']: r['ertek'] for r in sorok}


def begadkefat_dontesek(lemma):
    """[(ascii_kemeny, ascii_lagy, kemeny_e)] -- a pontozott lemma ב/כ/פ
    elofordulasai SORRENDBEN: dagesh vagy szokezdo pozicio -> kemeny,
    kulonben lagy (D34). A szokezdo pozicio a lemma ELSO heber betuje."""
    chars = list(lemma)
    elso_betu_idx = None
    for i, ch in enumerate(chars):
        if HEB_LETTER_LO <= ch <= HEB_LETTER_HI:
            elso_betu_idx = i
            break

    dontesek = []
    for i, ch in enumerate(chars):
        if ch not in BEGADKEFAT:
            continue
        kemeny_alak, lagy_alak = BEGADKEFAT[ch]
        van_dagesh = False
        j = i + 1
        while j < len(chars) and not (HEB_LETTER_LO <= chars[j] <= HEB_LETTER_HI):
            if chars[j] == DAGESH:
                van_dagesh = True
            j += 1
        kemeny = van_dagesh or (i == elso_betu_idx)
        dontesek.append((kemeny_alak, lagy_alak, kemeny))
    return dontesek


def spirantize(lemma, atiras):
    """A nyers OSHL-atirast (meg a szabalytabla elott) igazitja a
    begadkefat-dontesekhez: a lemma-ban felismert b/k/p elofordulasok
    SORRENDJEBEN cristo -- az atirasban ugyanabban a sorrendben elofordulo,
    azonos betut jelolo karaktereket kemenyre/lagyra alakitja. A `q`
    (qof) ekkor meg nem lett `k`-ra cserelve (az a szabalytabla dolga),
    ezert nincs utkozes a kaf `k`-javal."""
    dontesek = begadkefat_dontesek(lemma)
    if not dontesek:
        return atiras
    ki = []
    di = 0
    for ch in atiras:
        if di < len(dontesek) and ch in ('b', 'k', 'p'):
            kemeny_alak, lagy_alak, kemeny = dontesek[di]
            if ch == kemeny_alak:
                di += 1
                ki.append(kemeny_alak if kemeny else lagy_alak)
                continue
        ki.append(ch)
    return ''.join(ki)


def atir(atiras, szabalyok):
    ki = atiras
    for minta, csere in szabalyok:
        ki = ki.replace(minta, csere)
    return ki


def jovahagyott_heber_jelentesek():
    """{strong: ertek} -- a ket letezo, mar jovahagyott heber kivetel
    (adat/kiejtes_kivetelek.tsv, KIEJT-migracio). Nincs kozvetlen kulcs
    a kivetelek.tsv-ben (az 'alak' mezo nem OSHL-formatumu), ezert kezzel,
    a ket ismert Strong szerint parositva -- csak ez a ket Strong van a
    D28 26-os keszleteben, amelyre mar van jovahagyott ertek."""
    return {
        'H7121': 'kárá',
        'H8034': 'sém',
    }


def run():
    tokenek = h_tokenek_a_9_motivumbol()
    oshl = oshl_index()
    szabalyok = szabalytabla_betolt()
    jovahagyott = jovahagyott_heber_jelentesek()
    heber_kivetelek = heber_kivetelek_betolt()

    strongok = sorted(tokenek, key=lambda s: int(s[1:]))
    sorok = []
    hianyzo_oshl = []
    egyezik = 0
    eltero = 0
    nincs_referencia = 0
    kivetel_darab = 0

    for strong in strongok:
        motivumok = ', '.join(sorted(tokenek[strong]))
        oshl_sorok = oshl.get(strong, [])
        if not oshl_sorok:
            hianyzo_oshl.append(strong)
            sorok.append((strong, motivumok, '', '', '', 'nincs_referencia',
                          'nincs OSHL_lexikalis_index.tsv sor ehhez a Stronghoz'))
            nincs_referencia += 1
            continue
        # tobb OSHL-sor eseten (homograf/inflektalt valtozat) az elso, fajl-
        # sorrend szerinti bejegyzes a reprezentativ (nincs kulon gyakorisagi
        # mezo a valasztashoz) -- ha tobb van, a megjegyzes jelzi.
        elso = oshl_sorok[0]
        lemma = elso.get('lemma', '')
        atiras = elso.get('atiras', '')

        spirantizalt = spirantize(lemma, atiras)
        jelolt = atir(spirantizalt, szabalyok)

        felulbirat = heber_kivetelek.get(strong)
        if felulbirat is not None:
            jelolt = felulbirat
            arany = 'kivetel'
            kivetel_darab += 1
            megjegyzes = 'adat/kiejtes_heber_kivetelek.tsv kezi felulbiralas (D36)'
        else:
            vart = jovahagyott.get(strong)
            if vart is None:
                arany = 'nincs_referencia'
                nincs_referencia += 1
                megjegyzes = ''
            elif vart == jelolt:
                arany = 'egyezik'
                egyezik += 1
                megjegyzes = 'adat/kiejtes_kivetelek.tsv jóváhagyott értékével egyezik'
            else:
                arany = 'ELTER'
                eltero += 1
                megjegyzes = 'adat/kiejtes_kivetelek.tsv jóváhagyott értéke: %s' % vart

        if len(oshl_sorok) > 1:
            tovabbi = '; '.join('%s/%s' % (r.get('lemma', ''), r.get('atiras', ''))
                                 for r in oshl_sorok[1:])
            megjegyzes = (megjegyzes + ('; ' if megjegyzes else '') +
                          'további OSHL-változat(ok), nem választva: %s' % tovabbi)

        sorok.append((strong, motivumok, lemma, atiras, jelolt, arany, megjegyzes))

    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# S1.7 heber kiejtes-jeloltek (D28, 26 H-token, a 9 motivum '
                '(8 lexikon-motivum + TEREMT-002) elofordulasaibol).\n')
        f.write('# JAVITVA a felhasznaloi ALLJ utan (D34-D37): begadkefat-\n')
        f.write('# spirantizacio a pontozott lemmabol, h->ch, H2555 kezi kivetel.\n')
        f.write('# JELOLT, NEM VEGLEGES -- kezi jovahagyas utan kerulhet az '
                'adat/kiejtes_kivetelek.tsv-be (S2.1). Nem ir a kivetel-tablaba.\n')
        f.write('# scope=adat/elofordulasok.tsv (9 motivum, D28) + '
                'konkordancia/OSHL_lexikalis_index.tsv "atiras"/"lemma" mezo | '
                'forras=eszkozok/heber_kiejtes_jeloltek.py + '
                'adat/kiejtes_heber_jeloltszabalyok.tsv + '
                'adat/kiejtes_heber_kivetelek.tsv | ts=2026-09-29\n')
        f.write('\t'.join(['strong', 'motivumok', 'oshl_lemma', 'oshl_atiras',
                            'jelolt', 'arany_egyezes', 'megjegyzes']) + '\n')
        for row in sorok:
            f.write('\t'.join(row) + '\n')

    print('H-tokenek (D28 hatokor): %d' % len(strongok))
    print('OSHL-referencia hianyzik: %d (%s)' % (len(hianyzo_oshl), hianyzo_oshl))
    print('meglevo jovahagyott ertekkel egyezik: %d' % egyezik)
    print('meglevo jovahagyott ertektol elter: %d' % eltero)
    print('kezi kivetel (D36): %d' % kivetel_darab)
    print('nincs jovahagyott referencia (uj jelolt): %d' % nincs_referencia)
    print('irva: %s' % KIMENET)


if __name__ == '__main__':
    run()
