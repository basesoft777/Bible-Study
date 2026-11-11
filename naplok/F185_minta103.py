"""F185 seed-103 — a BDB vers → jelentéspont vak mintája (P5 előkészítése; a #186 seed-204 eljárásának mintájára).

A kitöltő a szócikk NYERS forrásbekezdéseit kapja: a `DictBDB.json` szócikkének `<p>` bekezdései, a `bont.sima` tisztításával, a
gépi vágás (a `bont.json_blokkok` középfej-bontása, a sorbelső fejek) és minden gépi döntés (útvonal, jel, bizonyosság) NÉLKÜL.
A mért hivatkozás elé `⟦azon⟧` jelölő kerül; a helyét a 2.29 `nyers` hivatkozásának szövegkeresése adja a nyers bekezdések
egymásutánjában (a hivatkozások sorrendjében, kurzorral; a vers-folytatás az előző találat után 40 karakteren belül) — ez nem
a szakasztábla, hanem a nyers szöveg. Ha nincs találat, a jelölő elmarad, és a kitöltő a `kornyezet` (a BDB TSV-szövegének
±100 karakteres ablaka) szerint keresi meg a helyet.

Minta: 200 egyszerű véletlen sor az `adat/bdb_vers_jelentes.tsv`-ből (`random.Random(103)`, a sorok (strong, sorszam) szerint
rendezve), a seed-99/100/101/102 kulcsainak (strong, poz) sorai kizárva; azonosító `N001`–`N200`. A szöveg minden szócikkben az
utolsó jelölt bekezdés utáni bekezdésnél véget ér (a jelentéspontot a jelölő előtti fejek döntik el).

Kimenet (naplok/): `BDB_SZELETELO_M2_minta_seed103_vak.tsv` (a kitöltőé), `BDB_SZELETELO_M2_minta_seed103_szocikkek.txt` (a
kitöltőé), `BDB_SZELETELO_M2_minta_seed103_kulcs.tsv` (a kitöltőnek NEM adandó). Használat (a repó gyökeréből):
  python naplok/F185_minta103.py
"""
import collections
import json
import os
import random
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(R, 'eszkozok', 'bdb_jelolt'))
sys.path.insert(0, os.path.join(R, 'eszkozok', 'olvaso_szerver'))
import bont  # noqa: E402
import bdb_szelet as B  # noqa: E402

N = 200
SEED = 103
ELOTAG = 'N'
KI = os.path.join(R, 'naplok', 'BDB_SZELETELO_M2_minta_seed103_')
KIZAR = ['BDB_SZELETELO_M2_minta_kulcs.tsv', 'BDB_SZELETELO_M2_minta_seed100_kulcs.tsv',
         'BDB_SZELETELO_M2_minta_seed101_kulcs.tsv', 'BDB_SZELETELO_M2_minta_seed102_kulcs.tsv']
KULCS_MEZOK = ['azon', 'strong', 'sorszam', 'poz', 'nyers', 'konyv_feloldas', 'mt_vers', 'karoli_vers', 'szakasz', 'resz',
               'utvonal', 'okkod', 'szurt', 'bizonyossag', 'jelolve']


def olvas(ut):
    sorok = [s.rstrip('\n').split('\t') for s in open(ut, encoding='utf-8') if s.strip() and not s.startswith('#')]
    return [dict(zip(sorok[0], s + [''] * (len(sorok[0]) - len(s)))) for s in sorok[1:]]


def nyers_bekezdesek(defhtml):
    """A szócikk `<p>` bekezdései (és a bekezdésen kívüli szöveg) sima szövegként, vágás nélkül."""
    belso = defhtml
    if belso.startswith('<div>') and belso.endswith('</div>'):
        belso = belso[5:-6]
    ki, poz = [], 0
    for m in re.finditer(r'<p(?:\s[^>]*)?>|</p>', belso):
        t = bont.sima(belso[poz:m.start()])
        if t:
            ki.append(t)
        poz = m.end()
    t = bont.sima(belso[poz:])
    if t:
        ki.append(t)
    return ki


def jelolok(bekezdesek, hivatkozasok, cel):
    """{(bekezdés, eltolás): azon} — a hivatkozások sorrendjében, a teljes Strong-hivatkozáslistán kurzorral (mint a 2.29)."""
    t = ' '.join(bekezdesek)
    hatar, p = [], 0
    for i, b in enumerate(bekezdesek):
        hatar.append((p, p + len(b), i))
        p += len(b) + 1
    kurzor, utolso, ki = 0, None, {}
    for h in hivatkozasok:
        nyers = h['nyers'].strip().lstrip(', ').strip()
        k = -1
        if nyers and h['konyv_feloldas'] == 'folytatas' and utolso is not None and ':' not in nyers:
            m = re.compile(r'(?<![\d:])%s(?![\d:])' % re.escape(nyers)).search(t, utolso, utolso + 40 + len(nyers))
            k = m.start() if m else -1
        if k < 0 and nyers:
            k = t.find(nyers, kurzor)
        if k < 0:
            continue
        kurzor, utolso = k + len(nyers), k
        if h['sorszam'] in cel:
            b = next(x for x in hatar if x[0] <= k < x[1] + 1)
            ki[(b[2], k - b[0])] = cel[h['sorszam']]
    return ki


def main():
    vj = olvas(os.path.join(R, 'adat', 'bdb_vers_jelentes.tsv'))
    kizart = set()
    for f in KIZAR:
        ut = os.path.join(R, 'naplok', f)
        if os.path.exists(ut):
            kizart |= {(r['strong'], r['poz']) for r in olvas(ut)}
    pool = sorted([r for r in vj if (r['strong'], r['poz']) not in kizart], key=lambda r: (r['strong'], int(r['sorszam'])))
    rng = random.Random(SEED)
    minta = rng.sample(pool, N)
    rng.shuffle(minta)
    for i, r in enumerate(minta, 1):
        r['azon'] = '%s%03d' % (ELOTAG, i)
    print('sokaság: %d sor (kizárva %d); minta: %d sor, %d szócikk' % (len(pool), len(kizart), N, len({r['strong'] for r in minta})))
    dbdb = {'H%04d' % int(re.match(r'^H(\d+)', it['top']).group(1)) + it['top'][len(re.match(r'^H\d+', it['top']).group(0)):]: it['def']
            for it in json.load(open(bont.JSON_UT, encoding='utf-8')) if re.match(r'^H\d+', it.get('top', ''))}
    en = {r['Strong_padded']: r['Teljes_szocikk'] for r in olvas(os.path.join(R, 'konkordancia', 'BDB_teljes_unabridged.tsv'))}
    strong_hiv = collections.defaultdict(list)
    for r in vj:
        strong_hiv[r['strong']].append(r)
    cel = collections.defaultdict(dict)
    for r in minta:
        cel[r['strong']][r['sorszam']] = r['azon']
    szoveg, jelolve = {}, set()
    for st in sorted(cel):
        bek = nyers_bekezdesek(dbdb.get(st, ''))
        jel = jelolok(bek, strong_hiv[st], cel[st])
        jelolve |= set(jel.values())
        ki = []
        for i, b in enumerate(bek):
            for (bi, o), az in sorted(((k, v) for k, v in jel.items() if k[0] == i), key=lambda x: -x[0][1]):
                b = b[:o] + '⟦%s⟧ ' % az + b[o:]
            ki.append(b)
        utolso = max([k[0] for k in jel] or [len(bek) - 1])
        tovabb = len(ki) > utolso + 2
        szoveg[st] = '\n\n'.join(ki[:utolso + 2]) + ('\n\n[… a szócikk folytatódik; a jelölt hivatkozások mind a fenti részben állnak]'
                                                     if tovabb else '')
    with open(KI + 'szocikkek.txt', 'w', encoding='utf-8', newline='\n') as f:
        for st in sorted(szoveg):
            f.write('=== %s ===\n%s\n\n' % (st, szoveg[st]))
    with open(KI + 'vak.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# F185 seed-103 VAK munkalap (BDB vers → jelentéspont). Forrás: a szócikk nyers forrásbekezdései '
                '(BDB_SZELETELO_M2_minta_seed103_szocikkek.txt; a mért hely előtt ⟦azon⟧). Ha a szövegben nincs jelölő, a hely a '
                '`kornyezet` (a BDB TSV-szövegének ablaka, a hivatkozás ⟦…⟧ között) szerint keresendő. A kitöltés szabályai: '
                'naplok/F185_jelentes.md, „Seed-103: eljárás és kapu”.\n')
        f.write('\t'.join(['azon', 'strong', 'nyers', 'jelolve', 'kornyezet', 'konyv_mt', 'jelentespont', 'resz', 'megjegyzes']) + '\n')
        for r in sorted(minta, key=lambda r: r['azon']):
            flat = B.lapit(en.get(r['strong'], ''))
            p = int(r['poz'])
            hossz = len(r['nyers']) if flat[p:p + len(r['nyers'])] == r['nyers'] else len(r['nyers'].lstrip(', '))
            korny = flat[max(0, p - 100):p] + '⟦' + flat[p:p + hossz] + '⟧' + flat[p + hossz:p + hossz + 100]
            f.write('\t'.join([r['azon'], r['strong'], r['nyers'], 'igen' if r['azon'] in jelolve else 'nem',
                               korny.replace('\t', ' '), '', '', '', '']) + '\n')
    with open(KI + 'kulcs.tsv', 'w', encoding='utf-8', newline='\n') as f:
        f.write('# F185 seed-103 KULCS: a 2.29 (adat/bdb_vers_jelentes.tsv, a mintavételkori állapot) sorai a vak lap azonosítóival. '
                'A kitöltőnek NEM adandó.\n')
        f.write('\t'.join(KULCS_MEZOK) + '\n')
        for r in sorted(minta, key=lambda r: r['azon']):
            r['jelolve'] = 'igen' if r['azon'] in jelolve else 'nem'
            f.write('\t'.join(r.get(m, '') for m in KULCS_MEZOK) + '\n')
    karakter = sum(len(v) for v in szoveg.values())
    print('szócikk: %d; szöveg: %d karakter; jelölő nélkül: %d (%s)' % (len(szoveg), karakter, N - len(jelolve),
                                                                       ', '.join(sorted(set(r['azon'] for r in minta) - jelolve))))


if __name__ == '__main__':
    main()
