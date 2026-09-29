"""TBESH_konszolidalt.tsv -- a TBESH.txt es TBESH.lexicon uniojja.

SZOTAR_BRIEF.md S4: "unio, nem csere" -- egyik forras sem valtja ki a
masikat, mert 9-nel a .txt, 13-nal a .lexicon bovebb (a 26 motivum-token
mereten, l. §0 0.5). Ez a szkript az ELJES heber Strong-keszletre
altalanositja ugyanezt a dontesi szabalyt: szocikkenkent a hosszabb
(tisztitott) szoveget valasztja, a forrast (`forras` = txt/lexicon/egyenlo)
soronkent rogziti.

Forrasok:
  - konkordancia/TBESH.txt: tobb alsor/Strong (pl. H7121G/H/I harom
    kulon-mikrojelentesenek roevid glosszaja, col7), a teljes, szamozott
    definicio (col8) azonban a legtobb esetben AZONOS az adott Strong
    osszes alsoraban -- ezert Strongonkent EGYETLEN (dedupikalt) teljes
    szoveget ad, plusz a roevid glosszak listajat. FONTOS: "Strongonkent"
    itt a STEP-forras sajat, betu-utotagos kulcsat jelenti (pl. "H1121a"),
    NEM feltetlenul a 4-jegyu alapszamot -- egy alapszamnak tobb, kulon
    betu-utotagos alszocikke is lehet (pl. H1121 "ben" csak "H1121a"/
    "H1121b" alakban letezik a TBESH.txt-ben, sima "H1121" sosem), es
    ezek KULON sorkent maradnak a kimenetben (D38) -- nem vonjuk
    ossze oket az alapszamba, es nem is dobjuk el. Az `alap_strong`
    oszlop koti vissza az utotagos sorokat az alapszamukhoz.
  - konkordancia/lexikonok_nyers/TBESH.lexicon (SQLite): egyetlen,
    konszolidalt HTML-bejegyzes Strongonkent (ugyanez a betu-utotagos
    konvencio, kis reszben nem-nullaval-toltott szamresszel).

TSV-iras kizarolag '\\t'.join() (CLAUDE.md).
"""

import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

import hashlib
import os
import re
import sqlite3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONKORDANCIA = os.path.join(ROOT, 'konkordancia')
TXT_UT = os.path.join(KONKORDANCIA, 'TBESH.txt')
LEXICON_UT = os.path.join(KONKORDANCIA, 'lexikonok_nyers', 'TBESH.lexicon')
KIMENET = os.path.join(KONKORDANCIA, 'TBESH_konszolidalt.tsv')

TAG_RE = re.compile(r'<[^>]+>')
WS_RE = re.compile(r'\s+')
# 4 szamjegy, opcionalisan egy STEP-alszocikk-betuvel (D38). A
# projekt STRONG tipusa (SEMA 1.2) maga 4 jegyu; a betu-utotag ("H1121G",
# a raw sor 1. oszlopaban kisbetus "H1121a" alakban) a STEP-forrasok sajat
# alszocikk-jeloleset adja at -- l. NYERS_KULCS_RE es alap_strong_szamol().
# (H7121-nek magának NINCS betu-utotagos kulcsa -- a tobb mikro-jelentese
# a raw sorokban csak a 2. oszlopban kulonbozik, "H7121G/H/I", az 1.
# oszlop mindharomnal sima "H7121" marad; ezt a mar meglevo dedup-logika
# (rovid_lista/teljes_lista) kezeli, nem az itteni betu-utotag-szures.)
STRONG_H_RE = re.compile(r'^H\d{4}[a-zA-Z]?$')
# A H9xxx tartomany a TBESH.txt sajat fejleconek megfogalmazasa szerint is
# ("prefixes, suffixes, personal pronoun endings and punctuation") nem
# szotari tetel, hanem morfologiai komponens -- ugyanaz a konvencio, mint
# az adat/grammatikai_strongok.tsv H9xxx-szures. Kiszurve. (Csak a 4-jegyu
# ALAPSZAMRA illik -- betu-utotagos H9xxx nem fordul elo egyik forrasban
# sem, ellenorizve.)
H9XXX_RE = re.compile(r'^H9\d{3}$')
# Nyers kulcs -- 1-4 szamjegy, opcionalis egy betu-utotaggal. A csoport(1)
# a szamresz, a csoport(2) a betu-utotag (ures string, ha nincs).
NYERS_KULCS_RE = re.compile(r'^H(\d{1,4})([a-zA-Z]?)$')
# Az alapszam kinyerese egy mar-normalizalt (4-jegyu, opcionalis betus)
# kulcsbol.
ALAP_STRONG_RE = re.compile(r'^(H\d{4})[a-zA-Z]?$')


def normalizal(strong):
    """"H122" -> "H0122"; "H122a" -> "H0122a" (D38: a betu-utotag
    MEGMARAD, csak a szamresz tolt 4 jegyre); mar rendben levo vagy
    felismerhetetlen kulcsot valtozatlanul hagy."""
    m = NYERS_KULCS_RE.match(strong)
    if m:
        szam, betu = m.groups()
        return 'H' + szam.zfill(4) + betu
    return strong


def alap_strong_szamol(strong):
    """"H0122a" -> "H0122"; "H0122" -> "H0122" (D38: a betu-utotagos
    kulcs sajat sor marad, de ez az oszlop koti az alapszamahoz -- a
    downstream kod, ha alapszam szerint illeszt, ezen keresztul tegye)."""
    m = ALAP_STRONG_RE.match(strong)
    return m.group(1) if m else strong


def clean(s):
    if not s:
        return ''
    s = TAG_RE.sub(' ', s)
    s = s.replace('&amp;', '&').replace('&#39;', "'").replace('&quot;', '"')
    return WS_RE.sub(' ', s).strip()


def sha_file(path, algo='sha256'):
    h = hashlib.new(algo)
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def txt_betolt(ut):
    """strong -> (lemma, atirat, pos_kod, rovid_glosszak[lista], teljes_szoveg)."""
    adat = {}
    with open(ut, encoding='utf-8-sig') as f:
        for sor in f:
            sor = sor.rstrip('\n\r')
            if not sor or '\t' not in sor:
                continue
            mezok = sor.split('\t')
            if len(mezok) < 8:
                continue
            strong = normalizal(mezok[0])
            if not STRONG_H_RE.match(strong) or H9XXX_RE.match(alap_strong_szamol(strong)):
                continue
            lemma = mezok[3] if len(mezok) > 3 else ''
            atirat = mezok[4] if len(mezok) > 4 else ''
            pos_kod = mezok[5] if len(mezok) > 5 else ''
            rovid = clean(mezok[6]) if len(mezok) > 6 else ''
            teljes = clean(mezok[7]) if len(mezok) > 7 else ''

            rekord = adat.setdefault(strong, {
                'lemma': lemma, 'atirat': atirat, 'pos_kod': pos_kod,
                'rovid_lista': [], 'teljes_lista': [],
            })
            if rovid and rovid not in rekord['rovid_lista']:
                rekord['rovid_lista'].append(rovid)
            if teljes and teljes not in rekord['teljes_lista']:
                rekord['teljes_lista'].append(teljes)
    kimenet = {}
    for strong, r in adat.items():
        teljes_szoveg = ' | '.join(r['teljes_lista']) if len(r['teljes_lista']) > 1 else (
            r['teljes_lista'][0] if r['teljes_lista'] else '')
        kimenet[strong] = {
            'lemma': r['lemma'], 'atirat': r['atirat'], 'pos_kod': r['pos_kod'],
            'rovid_glosszak': '; '.join(r['rovid_lista']),
            'teljes_szoveg': teljes_szoveg,
        }
    return kimenet


def lexicon_betolt(ut):
    """strong -> tisztitott teljes szoveg (HTML-mentesitve)."""
    conn = sqlite3.connect(ut)
    cur = conn.cursor()
    cur.execute("SELECT Topic, Definition FROM Lexicon WHERE Topic LIKE 'H%'")
    kimenet = {}
    for topic, html in cur.fetchall():
        topic = normalizal(topic)
        if not STRONG_H_RE.match(topic) or H9XXX_RE.match(alap_strong_szamol(topic)):
            continue
        kimenet[topic] = clean(html)
    conn.close()
    return kimenet


def konszolidal(txt_adat, lex_adat):
    # A kulcs mar normalizalt (4 jegy + opcionalis 1 betu-utotag) -- a
    # rendezes elsodlegesen a szamresz (s[1:5]), masodlagosan a betu-utotag
    # (s[5:], ures string < barmilyen betu, tehat az alapszam a sajat
    # utotagos alszocikkei elott all).
    strongok = sorted(set(txt_adat) | set(lex_adat), key=lambda s: (int(s[1:5]), s[5:]))
    sorok = []
    szamlalo = {'txt': 0, 'lexicon': 0, 'egyenlo': 0, 'csak_txt': 0, 'csak_lexicon': 0}
    for strong in strongok:
        t = txt_adat.get(strong)
        l_szoveg = lex_adat.get(strong)

        if t and l_szoveg is None:
            forras = 'txt'
            teljes = t['teljes_szoveg']
            szamlalo['csak_txt'] += 1
        elif not t and l_szoveg is not None:
            forras = 'lexicon'
            teljes = l_szoveg
            szamlalo['csak_lexicon'] += 1
        else:
            txt_hossz = len(t['teljes_szoveg'])
            lex_hossz = len(l_szoveg)
            if txt_hossz == 0 and lex_hossz == 0:
                forras = 'egyenlo'
                teljes = ''
            elif abs(txt_hossz - lex_hossz) <= 0.05 * max(txt_hossz, lex_hossz, 1):
                forras = 'egyenlo'
                teljes = t['teljes_szoveg'] if txt_hossz >= lex_hossz else l_szoveg
            elif txt_hossz > lex_hossz:
                forras = 'txt'
                teljes = t['teljes_szoveg']
            else:
                forras = 'lexicon'
                teljes = l_szoveg
            szamlalo[forras] += 1

        lemma = t['lemma'] if t else ''
        atirat = t['atirat'] if t else ''
        pos_kod = t['pos_kod'] if t else ''
        rovid_glosszak = t['rovid_glosszak'] if t else ''

        sorok.append((strong, alap_strong_szamol(strong), lemma, atirat, pos_kod,
                       rovid_glosszak, teljes, forras,
                       str(len(t['teljes_szoveg']) if t else 0),
                       str(len(l_szoveg) if l_szoveg is not None else 0)))
    return sorok, szamlalo


def run():
    txt_adat = txt_betolt(TXT_UT)
    lex_adat = lexicon_betolt(LEXICON_UT)
    sorok, szamlalo = konszolidal(txt_adat, lex_adat)

    txt_hash = sha_file(TXT_UT)
    lex_hash = sha_file(LEXICON_UT)

    header = ['strong', 'alap_strong', 'lemma', 'atirat', 'pos_kod', 'rovid_glosszak',
              'teljes_szoveg', 'forras', 'txt_hossz', 'lexicon_hossz']
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: eszkozok/tbesh_konszolidalt_import.py — kézzel nem szerkesztendő.\n')
        f.write('# forras: konkordancia/TBESH.txt (STEPBible.org CC BY) sha256=%s | '
                'konkordancia/lexikonok_nyers/TBESH.lexicon (biblematedata) sha256=%s\n'
                % (txt_hash, lex_hash))
        f.write('# unio-szabaly: szocikkenkent a hosszabb tisztitott szoveg (forras=txt/lexicon), '
                '+-5%% elteresnel forras=egyenlo. Dok.: konkordancia/TBESH_TBESG_README.md\n')
        f.write('# strong: a STEP-forras sajat kulcsa, betu-utotaggal is lehet (pl. H1121G a '
                'TBESH.txt-ben "H1121a" alakban -- STEP-alszocikk/mikro-jelentes, D38). '
                'alap_strong: a 4-jegyu Strong-szam utotag nelkul -- ha a downstream kod '
                'alapszam szerint illeszt, EZEN az oszlopon keresztul tegye, ne a strong '
                'oszlopon (annak tobb sora is tartozhat egy alapszamhoz).\n')
        f.write('\t'.join(header) + '\n')
        for row in sorok:
            f.write('\t'.join(row) + '\n')

    print('sorok: %d' % len(sorok))
    print('csak .txt-ben: %d' % szamlalo['csak_txt'])
    print('csak .lexicon-ban: %d' % szamlalo['csak_lexicon'])
    print('mindketto, .txt bovebb: %d' % szamlalo['txt'])
    print('mindketto, .lexicon bovebb: %d' % szamlalo['lexicon'])
    print('mindketto, kb. egyenlo: %d' % szamlalo['egyenlo'])
    print('irva: %s' % KIMENET)


if __name__ == '__main__':
    run()
