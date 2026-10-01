#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/normalizal.py -- F28_EMELES_BRIEF.md E2: determinisztikus
javitoreteg a szotari forditasok (Thayer, BDB) utofeldolgozasara.

A modell kimenetet nem irja at tartalmilag: csak a prompt v4 olyan
szabalyait kenyszeriti ki, amelyek gepileg, kontextus nelkul is
egyertelmuek. Minden szabaly szotaranként kapcsolhato (SZABALYOK), es
mindegyikhez teszt tartozik (eszkozok/teszt_normalizal.py).

Szabalyok:
  kk_k         a szam utani `ff.` / `ff` -> `kk.`, `f.` -> `k.` (v4 alt. 5.)
               -- csak szamjegy utan, hogy a BDB `n.f.` (noun feminine)
               jelolese ne serüljon.
  szerzonevek  egyseges szerzonevek (v4 alt. 7.): Philo/Filón -> Philón,
               Plutarch/Plutarchus/Plutarkhos -> Plutarkhosz,
               Tertullian/Tertullianusz -> Tertullianus, Josephusz/Flavius
               Josephus-alak marad: Josephus. Csak egesz szora, toldalek
               nelkuli alakra.
  igehely_rov  a forditasban bentmaradt angol/STEPBible/BDB-konyvrovidites
               igehely elott -> Karoli-rovidites (v4 alt. 4., masodik fele):
               `Exod 12:3` -> `2Móz 12:3`. Csak `fejezet:vers` elott.
  konyvnevek   a folyo szovegben bentmaradt angol konyvnev (szam nelkul)
               -> kiirt magyar konyvnev (v4 alt. 4., elso fele): `Hebrews`
               -> `a Zsidókhoz írt levél`-alak helyett a semleges
               `Zsidókhoz írt levél`. Csak a KONYVNEV_FOLYO zart listaja.

Hasznalat konyvtarkent:

    from normalizal import normalizal
    uj, valtozasok = normalizal(szoveg, 'BDB')

Parancssorbol (fajlon at, a CLAUDE.md shell-szabalya szerint):

    python eszkozok/normalizal.py --szotar BDB --be be.txt --ki ki.txt
"""

import argparse
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAROLI_UT = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')

# Szotaranként kapcsolhato szabalyok: szabaly -> azon szotarak, amelyekre fut.
SZABALYOK = {
    'kk_k': {'Thayer', 'BDB'},
    'szerzonevek': {'Thayer', 'BDB'},
    'igehely_rov': {'Thayer', 'BDB'},
    'konyvnevek': {'Thayer', 'BDB'},
}
SZABALY_SORREND = ['igehely_rov', 'kk_k', 'szerzonevek', 'konyvnevek']


# ---------------------------------------------------------------------------
# kk_k
# ---------------------------------------------------------------------------

KK_MINTA = re.compile(r'(?<=\d)(\s?)ff\.?(?![\w])')
K_MINTA = re.compile(r'(?<=\d)(\s?)f\.(?![\w])')


def szabaly_kk_k(szoveg):
    szoveg, n1 = KK_MINTA.subn(lambda m: m.group(1) + 'kk.', szoveg)
    szoveg, n2 = K_MINTA.subn(lambda m: m.group(1) + 'k.', szoveg)
    return szoveg, n1 + n2


# ---------------------------------------------------------------------------
# szerzonevek
# ---------------------------------------------------------------------------

SZERZONEVEK = [
    ('Philo', 'Philón'),
    ('Philon', 'Philón'),
    ('Filón', 'Philón'),
    ('Filon', 'Philón'),
    ('Plutarch', 'Plutarkhosz'),
    ('Plutarchus', 'Plutarkhosz'),
    ('Plutarkhos', 'Plutarkhosz'),
    ('Plutarkosz', 'Plutarkhosz'),
    ('Tertullian', 'Tertullianus'),
    ('Tertullianusz', 'Tertullianus'),
    ('Josephusz', 'Josephus'),
    ('Joszephusz', 'Josephus'),
]
# egesz szo: elotte nem betu, utana nem betu es nem kotojel (a toldalekos
# alakhoz -- Philónnál, Plutarkhosznál -- nem nyulunk)
_BETU = r'A-Za-zÀ-ɏ'


def _egesz_szo(minta):
    # utana nem allhat betu, kotojel vagy aposztrof (Philónnál; Philo's Lehre -- cim)
    return re.compile(r"(?<![%s])%s(?![%s\-'’])" % (_BETU, re.escape(minta), _BETU))


SZERZO_MINTAK = [(_egesz_szo(a), b) for a, b in SZERZONEVEK]


def szabaly_szerzonevek(szoveg):
    n = 0
    for minta, csere in SZERZO_MINTAK:
        szoveg, k = minta.subn(csere, szoveg)
        n += k
    return szoveg, n


# ---------------------------------------------------------------------------
# igehely_rov
# ---------------------------------------------------------------------------

# A Thayer es a BDB sajat (nem STEPBible) konyvrovidítesei -> STEPBible-alak;
# a STEPBible -> Karoli lepest a Konyv_normalizalo_tabla.tsv adja. A tabla
# `Forrás-alakok` oszlopa (F38) tovabbi forras-alakokat ad hozza (lent,
# a KAROLI betoltesekor).
FORRAS_ALIAS = {
    # Thayer
    'Joh': 'Jhn', 'Mar': 'Mrk', 'Jam': 'Jas', 'Phi': 'Php', 'Eze': 'Ezk',
    'Joe': 'Jol', '1Jo': '1Jn', '2Jo': '2Jn', '3Jo': '3Jn', 'Jude': 'Jud',
    'Psalm': 'Psa', 'Song of Solomon': 'Sng',
    # BDB
    'Exod': 'Exo', 'Deut': 'Deu', 'Josh': 'Jos', 'Judg': 'Jdg', 'Ruth': 'Rut',
    '1Sam': '1Sa', '2Sam': '2Sa', '1Kin': '1Ki', '2Kin': '2Ki',
    '1Kgs': '1Ki', '2Kgs': '2Ki', '1Chr': '1Ch', '2Chr': '2Ch', '2Chron': '2Ch',
    'Ezra': 'Ezr', 'Esth': 'Est', 'Prov': 'Pro', 'Eccl': 'Ecc', 'Song': 'Sng',
    'Ezek': 'Ezk', 'Hosea': 'Hos', 'Joel': 'Jol', 'Amos': 'Amo', 'Obad': 'Oba',
    'Jonah': 'Jon', 'Micah': 'Mic', 'Nahum': 'Nam', 'Zeph': 'Zep', 'Zech': 'Zec',
    'Matt': 'Mat', 'Mark': 'Mrk', 'Luke': 'Luk', 'John': 'Jhn', 'Acts': 'Act',
    '1Cor': '1Co', '2Cor': '2Co', 'Phil': 'Php', '1Thess': '1Th', '2Thess': '2Th',
    '1Tim': '1Ti', '2Tim': '2Ti', 'Phlm': 'Phm', '1Pet': '1Pe', '2Pet': '2Pe',
    '1John': '1Jn', '2John': '2Jn', '3John': '3Jn',
    # BDB/Thayer kiirt konyvnevei igehely elott
    '1 Samuel': '1Sa', '2 Samuel': '2Sa', '1 Kings': '1Ki', '2 Kings': '2Ki',
    '1 Chronicles': '1Ch', '2 Chronicles': '2Ch', 'Leviticus': 'Lev', 'Numbers': 'Num',
    'Nehemiah': 'Neh', 'Ecclesiastes': 'Ecc', 'Isaiah': 'Isa', 'Jeremiah': 'Jer',
    'Zechariah': 'Zec', 'Psalms': 'Psa', 'Genesis': 'Gen', 'Exodus': 'Exo',
    'Deuteronomy': 'Deu', 'Joshua': 'Jos', 'Judges': 'Jdg', 'Obadiah': 'Oba',
}

# Apokrif/deuterokanonikus konyvek (nincs Karoli-alakjuk; a forditas a
# FORDITAS_P4 APOKRIF_KIVETEL magyar alakjat irja). A 11. kapu (forditas_kapuk)
# a konyvnev-egyezeshez hasznalja; a javitoreteg NEM csereli oket.
APOKRIF_ALIAS = {
    'Wis': 'Bölcs', 'Wisdom': 'Bölcs', 'Sir': 'Sir', 'Sirach': 'Sir', 'Ecclus': 'Sir',
    'Ecclesiasticus': 'Sir', 'Macc': 'Makk', '1 Macc': '1Makk', '2 Macc': '2Makk',
    '3 Macc': '3Makk', '4 Macc': '4Makk', '1Macc': '1Makk', '2Macc': '2Makk',
    'Tob': 'Tób', 'Tobit': 'Tób', 'Bar': 'Báruk', 'Baruch': 'Báruk', 'Jdt': 'Judit',
    'Judith': 'Judit',
}


def _karoli_tabla():
    """-> ({STEP: (Karoli-rovidites, teljes nev)}, {forras-alak: STEP}).
    A masodik a tabla `Forrás-alakok` oszlopa (F38, DT-F38 (c)): a BDB
    igehely elotti, a FORRAS_ALIAS-ban nem szereplo konyvalakjai,
    vesszovel elvalasztva."""
    tabla = {}
    alakok = {}
    with open(KAROLI_UT, encoding='utf-8') as fh:
        sorok = fh.read().split('\n')
    fejlec = sorok[0].split('\t')
    for sor in sorok[1:]:
        if not sor.strip():
            continue
        r = dict(zip(fejlec, sor.split('\t')))
        tabla[r['STEPBible-rövidítés']] = (r['Magyar rövidítés'], r['Teljes magyar könyvnév'])
        for a in (r.get('Forrás-alakok') or '').split(','):
            if a.strip():
                alakok[a.strip()] = r['STEPBible-rövidítés']
    return tabla, alakok


KAROLI, TABLA_ALAKOK = _karoli_tabla()
# a tabla forras-alakjai a FORRAS_ALIAS-ba (a kodbeli alias elsobbseggel);
# igy a javitoreteg (IGE_LEK) es a 11. kapu (forditas_kapuk._konyv_mintak)
# ugyanazt a lekepezest latja
for _a, _s in TABLA_ALAKOK.items():
    FORRAS_ALIAS.setdefault(_a, _s)
_KAROLI_ROV = {v[0] for v in KAROLI.values()}


def _ige_lekepezes():
    """{forras-alak: karoli-rovidites}; a Karoli-alakkal azonos kulcs kimarad
    (pl. Jer, Gal, Hab -- a csere ott ures), es kimarad minden olyan kulcs,
    amely egy MASIK konyv Karoli-roviditese (utkozes-ved)."""
    lek = {}
    for step, (rov, _) in KAROLI.items():
        if step != rov:
            lek[step] = rov
    for alias, step in FORRAS_ALIAS.items():
        if step in KAROLI and alias != KAROLI[step][0]:
            lek[alias] = KAROLI[step][0]
    for k in list(lek):
        if k in _KAROLI_ROV and lek[k] != k:
            del lek[k]
    return lek


IGE_LEK = _ige_lekepezes()
_IGE_KULCSOK = sorted(IGE_LEK, key=len, reverse=True)
IGE_MINTA = re.compile(
    r'(?<![%s0-9])(%s)\.?(\s+)(?=\d{1,3}:\d)' % (_BETU, '|'.join(re.escape(k) for k in _IGE_KULCSOK)))


def szabaly_igehely_rov(szoveg):
    return IGE_MINTA.subn(lambda m: IGE_LEK[m.group(1)] + ' ', szoveg)


# ---------------------------------------------------------------------------
# konyvnevek (folyo szoveg)
# ---------------------------------------------------------------------------

# Csak egyertelmu angol konyvnevek (a John, James, Mark, Jude szemelynevkent
# is allhat -- ezek kimaradnak).
KONYVNEV_FOLYO = [
    ('Song of Solomon', 'Énekek éneke'),
    ('Ecclesiastes', 'Prédikátor könyve'),
    ('Deuteronomy', 'Mózes ötödik könyve'),
    ('Leviticus', 'Mózes harmadik könyve'),
    ('Genesis', 'Mózes első könyve'),
    ('Exodus', 'Mózes második könyve'),
    ('Hebrews', 'Zsidókhoz írt levél'),
    ('Revelation', 'Jelenések könyve'),
    ('Proverbs', 'Példabeszédek könyve'),
    ('Psalms', 'Zsoltárok könyve'),
    ('Lamentations', 'Jeremiás siralmai'),
]
# angol konyvcimben (`Lange on Revelation`, `Commentary in Genesis`) a nev
# nem folyo szoveg -- angol eloljaro utan nem cserelunk (G0086)
KONYVNEV_MINTAK = [
    (re.compile(r'(?<![%s])(?<!\bon )(?<!\bin )(?<!\bof )%s(?![%s\-])(?!\.?\s*\d)'
                % (_BETU, re.escape(a), _BETU)), b)
    for a, b in KONYVNEV_FOLYO
]


def szabaly_konyvnevek(szoveg):
    n = 0
    for minta, csere in KONYVNEV_MINTAK:
        szoveg, k = minta.subn(csere, szoveg)
        n += k
    return szoveg, n


FUGGVENYEK = {
    'kk_k': szabaly_kk_k,
    'szerzonevek': szabaly_szerzonevek,
    'igehely_rov': szabaly_igehely_rov,
    'konyvnevek': szabaly_konyvnevek,
}


def normalizal(szoveg, szotar, kikapcsolt=()):
    """(uj_szoveg, [(szabaly, csere_db), ...]) -- csak a nem nulla
    cserek kerulnek a listaba."""
    valtozasok = []
    for nev in SZABALY_SORREND:
        if nev in kikapcsolt or szotar not in SZABALYOK[nev]:
            continue
        szoveg, n = FUGGVENYEK[nev](szoveg)
        if n:
            valtozasok.append((nev, n))
    return szoveg, valtozasok


def main():
    ap = argparse.ArgumentParser(description='F28 E2 javitoreteg')
    ap.add_argument('--szotar', required=True, choices=['Thayer', 'BDB'])
    ap.add_argument('--be', required=True)
    ap.add_argument('--ki', required=True)
    ap.add_argument('--kikapcsol', nargs='*', default=[], choices=sorted(SZABALYOK))
    args = ap.parse_args()
    with open(args.be, encoding='utf-8') as fh:
        szoveg = fh.read()
    uj, valt = normalizal(szoveg, args.szotar, args.kikapcsol)
    with open(args.ki, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(uj)
    print('valtozasok: %s' % (', '.join('%s=%d' % v for v in valt) or 'nincs'))


if __name__ == '__main__':
    main()
