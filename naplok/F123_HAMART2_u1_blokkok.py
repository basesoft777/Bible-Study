# -*- coding: utf-8 -*-
"""F123 HAMART-001 U1 — a teljesség-mérés eltéréseinek lexéma-blokkjai és a `nyitva` jelölt-blokksorok.

Bemenet: naplok/F123_teljesseg_HAMART-001.tsv (eszkozok/teljesseg_meres.py kimenete).
Kimenet:
  naplok/F123_teljesseg_HAMART-001_blokkok.tsv        — blokkonként a vers-lista (háló, blokk, vers, gerinc_a_versben)
  naplok/F123_U1_HAMART-001_jelolt_sorok_A.tsv         — jeloltek.tsv-séma, `nyitva`, lexémánként egy blokk-sor (DT-F123o minta)
Döntés nélküli gépi osztályozás: a Károli-háló eltéréseinél a vers TAHOT/TAGNT-tokenjei közül azok a Strongok,
amelyek angol glosszája a Károli-szó jelentéskörébe esik. Az osztálytalan sor kézi olvasásra marad.
TSV: split('\\t'), '\\t'.join(); csv modul nincs."""
import os
import re
import sys
from collections import defaultdict, OrderedDict

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GY, 'eszkozok'))
import lekerdez as L  # noqa: E402

MID = 'HAMART-001'
DATUM = '2026.11.03'
TS = '2026-11-03'

# Károli-szó (tő) → osztály, glossza-minta
KAROLI_OSZTALY = [
    ('átok', re.compile(r'^(átok|átkoz|elátkoz|megátkoz)'), re.compile(r'curs|accurs|imprecat', re.I)),
    ('romlás', re.compile(r'^(roml|megront|elront|romol|megromol)'),
     re.compile(r'corrupt|destroy|ruin|spoil|decay|waste|perish|ravag|devast|mar\b', re.I)),
    ('erőszak', re.compile(r'^erőszak'), re.compile(r'violen|robber|oppress|wrong|plunder', re.I)),
    ('tövis', re.compile(r'^tövis'), re.compile(r'thorn|brier|bramble|thistle|nettle|bush', re.I)),
]

SZEREP = {
    'H7451': 'a רַע (ra‘, gonoszság, rossz)',
    'H2403': 'a חַטָּאת (chattát, bűn, bűnáldozat)',
    'H0127': 'az אֲדָמָה (adamá, föld, talaj)',
    'H7843': 'a שָׁחַת (sáchat, megront, elpusztít)',
    'H7043': 'a קָלַל (qalal, megátkoz, könnyűvé tesz)',
    'H2555': 'a חָמָס (chámász, erőszak)',
    'H6975': 'a קוֹץ (kóc, tövis)',
}


def olvas_teljesseg():
    sorok = [s.rstrip('\n').split('\t') for s in open(
        os.path.join(GY, 'naplok', 'F123_teljesseg_%s.tsv' % MID), encoding='utf-8') if not s.startswith('#')]
    fej = sorok[0]
    return [dict(zip(fej, s)) for s in sorok[1:]]


def main():
    rows = olvas_teljesseg()
    tok = defaultdict(list)
    for r in list(L.load_tahot()) + list(L.load_tagnt()):
        tok[r['Igehely']].append(r)

    blokk = OrderedDict()  # (halo, kulcs) -> [(vers, gerinc)]
    strong_net_versek = {d['igehely'] for d in rows if d['halo'] == 'strong'}

    for d in rows:
        if not d['allapot'].startswith('ELT'):
            continue
        v, g, rs = d['igehely'], d['gerinc_a_versben'], d['reszlet']
        if d['halo'] == 'strong':
            for s in [x.strip() for x in rs.split(',')]:
                blokk.setdefault(('strong', s), []).append((v, g))
        elif d['halo'] == 'szotar':
            if g == 'igen':
                continue  # a gerincet hordozó vers a Strong-háló blokkjában áll
            ss = sorted(set(re.findall(r'(?:BDB|Thayer)\S*\s+([HG]\d{4})', rs)) or {'?'})
            for s in ss:
                blokk.setdefault(('szotar', s), []).append((v, g))
        elif d['halo'] == 'karoli':
            if g == 'igen':
                continue
            szo = rs.lower()
            osz = None
            for nev, rx, gl in KAROLI_OSZTALY:
                if rx.match(szo):
                    osz = (nev, gl)
                    break
            if not osz:
                blokk.setdefault(('karoli', 'osztálytalan-szó'), []).append((v, g))
                continue
            talalt = sorted({t['Strong-szám'] for t in tok.get(v, [])
                             if osz[1].search(t.get('Rövid jelentés', '') + ' ' + t.get('Angol tükörfordítás', ''))})
            if not talalt:
                blokk.setdefault(('karoli', osz[0] + '|osztálytalan'), []).append((v, g))
            for s in talalt:
                blokk.setdefault(('karoli', osz[0] + '|' + s), []).append((v, g))

    # egy vers egyszer egy blokkban
    for k in blokk:
        seen, out = set(), []
        for v, g in blokk[k]:
            if v not in seen:
                seen.add(v)
                out.append((v, g))
        blokk[k] = out

    ki = os.path.join(GY, 'naplok', 'F123_teljesseg_%s_blokkok.tsv' % MID)
    with open(ki, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/F123_HAMART2_u1_blokkok.py | scope=naplok/F123_teljesseg_HAMART-001.tsv ELTÉRÉS-sorai × '
                'TAHOT_kivonat.tsv+TAGNT_kivonat.tsv (glossza) | forras=split(\'\\t\') | ts=%s\n' % TS)
        f.write('halo\tblokk\tigehely\tgerinc_a_versben\n')
        for (h, k), vs in blokk.items():
            for v, g in vs:
                f.write('%s\t%s\t%s\t%s\n' % (h, k, v, g))

    haloszoveg = {
        'strong': 'Strong-háló',
        'karoli': 'Károli-szó háló',
        'szotar': 'szótár-háló (BDB/Thayer)',
    }
    sorok = []
    for (h, k), vs in blokk.items():
        n = len(vs)
        elso = vs[0][0]
        kulcs = k.replace('|', '=')
        forras = ('F123 U1 teljesség-mérés, %s, blokk-sor (DT-F123o minta): %d vers, az első itt; a lista: '
                  'naplok/F123_teljesseg_HAMART-001_blokkok.tsv (halo=%s, blokk=%s), naplok/F123_teljesseg_HAMART-001.md | '
                  'scope=manual | forras=eszkozok/teljesseg_meres.py, naplok/F123_HAMART2_u1_blokkok.py | ts=%s'
                  % (haloszoveg[h], n, h, k, TS))
        if h == 'strong':
            nf = ' A 651 listán kívüli Strongot hordozó vers (H7451, H7043, magányos H6975) az N-F63e-döntésre vár (DT-F123u).' \
                if k in ('H7451', 'H7043', 'H6975') else ''
            ind = ('Összesítő sor %d versre (az első itt áll): %s szava áll bennük, de sem előfordulás-sor, sem '
                   'jelölt-sor nincs rájuk; a mai TAHOT/TAGNT-scan találata, amelyet az F108 újrascan is látott, '
                   'de nem írt be. Elbírálás az értelmező menetben, blokkban.%s'
                   % (n, SZEREP.get(k, k), nf))
        elif h == 'karoli':
            nev, _, s = k.partition('|')
            if s in ('osztálytalan', ''):
                ind = ('Összesítő sor %d versre (az első itt áll): a Károli „%s”-csoport szava áll bennük, de a gépi '
                       'glossza-illesztés nem talált a Károli-szó jelentéskörébe eső héber/görög szót; kézi olvasásra '
                       'marad. A versekben a motívum egyik szava sem áll.' % (n, nev))
            elif k == 'osztálytalan-szó':
                ind = ('Összesítő sor %d versre: a Károli-szó nem tartozik a négy osztályba; kézi olvasásra marad.' % n)
            else:
                ind = ('Összesítő sor %d versre (az első itt áll): a Károli „%s”-csoport szava (%s) ezekben a '
                       'versekben a %s szót fordítja; a motívum szava (gerinc-Strongja) a versekben nem áll. '
                       'Elbírálás az értelmező menetben, blokkban.'
                       % (n, nev, nev, SZEREP.get(s, s)))
        else:
            ind = ('Összesítő sor %d versre (az első itt áll): a BDB/Thayer a %s Strongnál idézi a verset, de a '
                   'versben a motívum Strongjai nem állnak (versszámozás-eltolás vagy más lexéma); kézi '
                   'ellenőrzés az értelmező menetben.' % (n, k))
        szo = '' if h != 'karoli' else k.split('|')[0]
        sorok.append([MID, elso, forras, 'nyitva', ind, szo, '', '', DATUM, 'elofordulas', '', '', ''])
    p = os.path.join(GY, 'naplok', 'F123_U1_%s_jelolt_sorok.tsv' % MID)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: naplok/F123_HAMART2_u1_blokkok.py — jeloltek.tsv-séma, `nyitva`; az adat/jeloltek.tsv-be a #608 merge-e után kerül (rebase, majd beírás)\n')
        f.write('id\tigehely\tforras_kereses\tdontes\tindoklas\tkaroli_szo\tazonositas_modja\tmegbizhatosag\tdatum\tjelolt_tipus\tcel_id\tcel_igehely\tcel_alpont\n')
        for s in sorok:
            f.write('\t'.join(x.replace('\t', ' ') for x in s) + '\n')

    print('blokk\tvers')
    for (h, k), vs in blokk.items():
        print('%s\t%s\t%d' % (h, k, len(vs)))
    print('blokksor:', len(sorok))


if __name__ == '__main__':
    main()
