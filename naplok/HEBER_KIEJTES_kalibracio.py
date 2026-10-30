"""Kalibráló minta a gépi magyaros héber kiejtéshez (N-F131w, a felhasználó
kérésére: „most kalibráljunk”). Kísérleti, csak naplót ír, adatot nem.

A lexikonlapok (lexikon/*_TUDOMANYOS.md) motívumainak héber verseiből
(adat/elofordulasok.tsv) a TAHOT-sorokból (konkordancia/TAHOT_kivonat.tsv)
TELJES szót rak össze (előtag + tő + toldalék), és rögzített seed-del
(20261030) kb. 50 alakos mintát vesz nyolc nehéz kategóriából. Minden alakhoz
pontosan három különböző kiejtési változat tartozik, kevert sorrendben (A/B/C):
  gépi        -- a mai szabályok (naplok/HEBER_KIEJTES_meres.py NIQQUD-átírója,
                 a 26-on kalibrált paraméterekkel: ס = s, שׂ = sz, ח = ch,
                 a szókezdő begadkefat kemény [D34], kámec kátán meteg nélküli
                 zárt szótagban; plusz a teljes szóhoz kellő két kapcsoló:
                 szókezdő kötőszói וּ = ú, makkef előtti zárt szótag kámece = o)
  javaslat    -- a session javasolt helyes alakja (manual)
  alternatíva -- egy harmadik, nyelvileg védhető változat (manual)
A javaslat és az alternatíva a naplok/HEBER_KIEJTES_kalibracio_javaslat.tsv-ből
jön (kézi, proveniencia: manual). Ha az a fájl még nincs, a szkript csak a
mintát és a gépi változatokat írja ki (első menet).

Kimenet:
  naplok/HEBER_KIEJTES_kalibracio.json       -- az oldalnak (forrás nélkül)
  naplok/HEBER_KIEJTES_kalibracio_kulcs.json -- betű -> forrás (az oldalra NEM kerül)
  naplok/HEBER_KIEJTES_kalibracio.md         -- táblázat a chatbe („1A 2C …”)
  naplok/HEBER_KIEJTES_kalibracio_minta.tsv  -- a minta gépi segédoszlopokkal

TSV: split('\\t') / '\\t'.join() (CLAUDE.md).
"""

import json
import os
import random
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'naplok'))
import HEBER_KIEJTES_meres as m  # noqa: E402

N = os.path.join(ROOT, 'naplok')
KI_MINTA = os.path.join(N, 'HEBER_KIEJTES_kalibracio_minta.tsv')
JAVASLAT = os.path.join(N, 'HEBER_KIEJTES_kalibracio_javaslat.tsv')
KI_JSON = os.path.join(N, 'HEBER_KIEJTES_kalibracio.json')
KI_KULCS = os.path.join(N, 'HEBER_KIEJTES_kalibracio_kulcs.json')
KI_MD = os.path.join(N, 'HEBER_KIEJTES_kalibracio.md')
SEED = 20261030
TS = '2026-10-30'

KVOTA = [('kamec_katan', 7), ('nem_szokezdo_seva', 6), ('furtiv_patah', 6), ('dages_forte', 6),
         ('ketiv_qere', 5), ('makkef', 6), ('szokezdo_begadkefat', 7), ('szamech_sin', 7)]
KAT_NEV = {'kamec_katan': 'kámec kátán (gyanú)', 'nem_szokezdo_seva': 'nem szókezdő sevá',
           'furtiv_patah': 'furtív patah', 'dages_forte': 'dáges forte', 'ketiv_qere': 'ketiv/qere',
           'makkef': 'makkef', 'szokezdo_begadkefat': 'szókezdő begadkefat dáges nélkül',
           'szamech_sin': 'ס és שׂ (sz vagy s)', 'vegyes': 'vegyes (nem nehéz)'}
MENET = 1
CEL = 50
KIZART = set()  # a 2. menetben: az 1. minta alakjai

# a mai szabályok: a 26-on kalibrált paraméterek (naplok/HEBER_KIEJTES_meres.md 4.1)
P_MAI = m.a_priori(m.PARAM_TER_NIQQUD)
P_MAI.update({'szamech': 's', 'kotoszo_u': True, 'makkef_katan': True})
# segédváltozatok a javaslat-íráshoz (nem kerülnek az oldalra)
VALTOZAT = {
    'sz_sz': dict(P_MAI, szamech='sz', sin='sz'),
    's_s': dict(P_MAI, szamech='s', sin='s'),
    'pont': dict(P_MAI, szokezdo_begadkefat='pont_szerint'),
    'kamec_alt': dict(P_MAI, kamec_katan=False, seva_hosszu_utan='hangzo'),
    'sz_pont': dict(P_MAI, szamech='sz', sin='sz', szokezdo_begadkefat='pont_szerint'),
}
P_GEPI = P_MAI  # a gépi változat szabályai (1. menet: a mai; 2. menet: DT-F131y)
GEPI_NEV = 'mai szabály (ס = s, שׂ = sz; szókezdő begadkefat kemény)'


def beallit(menet):
    """A 2. menet (DT-F131y után, 2026-10-30): más seed, az 1. minta alakjai kizárva,
    a gépi változat a DT-F131y szabályaival, plusz egy „vegyes” (nem nehéz) kategória."""
    global MENET, KI_MINTA, JAVASLAT, KI_JSON, KI_KULCS, KI_MD, SEED, KVOTA, KIZART, P_GEPI, GEPI_NEV
    if menet == 1:
        return
    MENET = 2
    regi = KI_MINTA
    KI_MINTA = os.path.join(N, 'HEBER_KIEJTES_kalibracio2_minta.tsv')
    JAVASLAT = os.path.join(N, 'HEBER_KIEJTES_kalibracio2_javaslat.tsv')
    KI_JSON = os.path.join(N, 'HEBER_KIEJTES_kalibracio2.json')
    KI_KULCS = os.path.join(N, 'HEBER_KIEJTES_kalibracio2_kulcs.json')
    KI_MD = os.path.join(N, 'HEBER_KIEJTES_kalibracio2.md')
    SEED = 20261107
    KVOTA = [('kamec_katan', 6), ('nem_szokezdo_seva', 6), ('furtiv_patah', 5), ('dages_forte', 5),
             ('ketiv_qere', 5), ('makkef', 5), ('szokezdo_begadkefat', 5), ('szamech_sin', 5), ('vegyes', 0)]
    for r in m.tsv_sorok(regi, 'sorszam'):
        KIZART.add(unicodedata.normalize('NFC', r['heber']))
    P_GEPI = m.dt_f131y()
    GEPI_NEV = 'DT-F131y'
ELOTAGOK = {'H900%d' % i for i in range(1, 10)}


def lexikon_motivumok():
    d = os.path.join(ROOT, 'lexikon')
    return sorted(f[:-len('_TUDOMANYOS.md')] for f in os.listdir(d) if f.endswith('_TUDOMANYOS.md'))


def celhelyek(motivumok):
    """{igehely: {strong4: set(motivum)}} -- a lexikon-motívumok héber előfordulásai."""
    ki = {}
    for r in m.tsv_sorok(m.ELOFORDULASOK, 'id'):
        if r['id'] not in motivumok:
            continue
        for st in r['strong'].split('+'):
            st = st.strip()
            if st.startswith('H') and st[1:5].isdigit():
                ki.setdefault(r['igehely'], {}).setdefault(st[:5], set()).add(r['id'])
    return ki


def szavak(helyek):
    """A TAHOT sorainak összerakása teljes szóvá a célversekben.
    Előtag: H9001-H9009 (vav, elöljárók, -ש, kérdő hé, névelő); toldalék: H9010-től
    (irányjelölő hé, paragogikus nun, névmási toldalékok, pl. Ps3m). Makkef: a szó
    utolsó elemének STEP-átírása '-'-re végződik."""
    soronkent = {}
    with open(m.TAHOT, encoding='utf-8') as f:
        next(f)
        for l in f:
            r = l.rstrip('\n').split('\t')
            if len(r) < 5 or r[0] not in helyek:
                continue
            soronkent.setdefault(r[0], []).append(r)
    ki = []
    for hely, sorok in soronkent.items():
        elotag, aktualis = [], None
        for r in sorok:
            st = r[1]
            if st[:5] in ELOTAGOK:
                if aktualis:
                    ki.append(aktualis)
                    aktualis = None
                elotag.append(r)
                continue
            if st.startswith('H9') and aktualis:
                aktualis['reszek'].append(r)
                continue
            if aktualis:
                ki.append(aktualis)
            aktualis = {'igehely': hely, 'strong': st[:5], 'lemma': unicodedata.normalize('NFC', r[4]),
                        'reszek': elotag + [r], 'elotag_db': len(elotag)}
            elotag = []
        if aktualis:
            ki.append(aktualis)
    for w in ki:
        w['alak'] = unicodedata.normalize('NFC', ''.join(x[2] for x in w['reszek']))
        w['step'] = ' + '.join(x[3] for x in w['reszek'])
        w['makkef'] = w['reszek'][-1][3].strip().endswith('-')
        w['tiszta'] = unicodedata.normalize('NFC', m.tisztit(w['alak']).replace(m.METEG, ''))
    return ki


def kiejt(w, p):
    alak = m.tisztit(w['alak']) + (m.MAKKEF if w['makkef'] else '')
    g, nyom = m.niqqud(alak, p, elso_elotag=w['elotag_db'] > 0)
    return g.rstrip('-'), nyom


def jegyek(w):
    """Szerkezeti jegyek a pontozott alakból + az átíró döntésnyomai."""
    _, nyom = kiejt(w, P_MAI)
    gepi = kiejt(w, P_GEPI)[0]
    ls = m.betuk(m.tisztit(w['alak']))
    j = set()
    for i, b in enumerate(ls):
        if m.KAMEC_KATAN in b['j'] or m.HATAF_KAMEC in b['j']:
            j.add('kamec_katan')
        if m.KAMEC in b['j']:
            for k in range(i + 1, len(ls)):
                if ls[k]['b'] in (m.VAV, m.JOD, m.HE, m.ALEF) and not (ls[k]['j'] & (m.MAGANHANGZO | {m.SEVA, m.DAGES})):
                    continue
                if m.SEVA in ls[k]['j'] and k != len(ls) - 1:
                    j.add('kamec_katan')
                break
            if w['makkef']:
                j.add('kamec_katan')
        if m.SEVA in b['j'] and 0 < i < len(ls) - 1 and i >= w['elotag_db']:
            j.add('nem_szokezdo_seva')
        if b['b'] in (m.SZAMEH, m.SIN) and (b['b'] == m.SZAMEH or m.SZIN_PONT in b['j']):
            j.add('szamech_sin')
    if ls and ls[0]['b'] in (m.BET, m.KAF, m.PE) and m.DAGES not in ls[0]['j']:
        j.add('szokezdo_begadkefat')
    if 'kamec_katan' in nyom:
        j.add('kamec_katan')
    if 'furtiv' in nyom:
        j.add('furtiv_patah')
    if 'dages_forte' in nyom:
        j.add('dages_forte')
    massal = ''.join(c for c in unicodedata.normalize('NFD', w['alak']) if m.ALEF <= c <= m.TAV)
    if 'tetragramma' in nyom or 'ירושל' in massal:
        j.add('ketiv_qere')
    if w['makkef']:
        j.add('makkef')
    return gepi, j


def minta():
    motivumok = lexikon_motivumok()
    helyek = celhelyek(set(motivumok))
    jeloltek = []
    for w in szavak(helyek):
        mot = helyek[w['igehely']].get(w['strong'])
        w['motivum_szo'] = 'igen' if mot else 'nem'
        w['motivum'] = ', '.join(sorted(mot or set().union(*helyek[w['igehely']].values())))
        w['gepi'], w['jegyek'] = jegyek(w)
        for k, p in VALTOZAT.items():
            w[k] = kiejt(w, p)[0]
        jeloltek.append(w)
    latott, egyedi = set(), []
    for w in sorted(jeloltek, key=lambda x: (x['motivum_szo'] != 'igen', x['igehely'], x['tiszta'])):
        if w['tiszta'] in latott or w['tiszta'] in KIZART:
            continue
        latott.add(w['tiszta'])
        egyedi.append(w)
    rnd = random.Random(SEED)
    valasztott, vett = [], set()
    for kat, db in KVOTA:
        if kat == 'vegyes':
            db = CEL - len(valasztott)  # a maradék a vegyes (nehéz jegy nélküli) szavakból
        jel = [w for w in egyedi if (not w['jegyek'] if kat == 'vegyes' else kat in w['jegyek'])
               and w['tiszta'] not in vett]
        rnd.shuffle(jel)
        jel.sort(key=lambda w: w['motivum_szo'] != 'igen')  # stabil: a motívumszavak előre
        for w in jel[:db]:
            w['kategoria'] = kat
            valasztott.append(w)
            vett.add(w['tiszta'])
    van = lambda w, kat: (not w['jegyek']) if kat == 'vegyes' else kat in w['jegyek']
    stat = {kat: (sum(van(w, kat) and w['motivum_szo'] == 'igen' for w in egyedi),
                  sum(van(w, kat) for w in egyedi)) for kat, _ in KVOTA}
    for i, w in enumerate(valasztott, 1):
        w['sorszam'] = i
    return motivumok, jeloltek, egyedi, stat, valasztott


def javaslat_beolvas():
    """{heber_alak: (javaslat, alternativa, alternativa2, megjegyzes)} -- kézi tábla (manual).
    Az `alternativa2` csak akkor kell, ha a gépi alak egyezik a javaslattal."""
    if not os.path.exists(JAVASLAT):
        return None
    ki = {}
    for r in m.tsv_sorok(JAVASLAT, 'heber'):
        ki[unicodedata.normalize('NFC', r['heber'])] = (r['javaslat'], r['alternativa'], r.get('alternativa2', ''),
                                                        r.get('megjegyzes', ''))
    return ki


def main():
    motivumok, jeloltek, egyedi, stat, valasztott = minta()
    prov = (f'scope=adat/elofordulasok.tsv ({", ".join(motivumok)}; héber Strongok) + konkordancia/TAHOT_kivonat.tsv '
            f'| forras=naplok/HEBER_KIEJTES_kalibracio.py (seed={SEED}) | ts={TS}')
    with open(KI_MINTA, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# HEBER_KIEJTES_kalibracio.py mintája (kísérleti, nem adat).\n# ' + prov + '\n')
        f.write(f'# jelölt szavak: {len(jeloltek)}, egyedi alak: {len(egyedi)}; '
                f'kategóriánként (egyedi; motívumszó, összes): {stat}\n')
        f.write('\t'.join(['sorszam', 'kategoria', 'osszes_jegy', 'motivum_szo', 'motivum', 'igehely', 'strong',
                           'lemma', 'heber', 'step', 'gepi', 'sz_sz', 's_s', 'pont', 'sz_pont', 'kamec_alt']) + '\n')
        for w in valasztott:
            f.write('\t'.join([str(w['sorszam']), w['kategoria'], ','.join(sorted(w['jegyek'])), w['motivum_szo'],
                               w['motivum'], w['igehely'], w['strong'], w['lemma'], w['tiszta'], w['step'],
                               w['gepi'], w['sz_sz'], w['s_s'], w['pont'], w['sz_pont'], w['kamec_alt']]) + '\n')
    jav = javaslat_beolvas()
    if jav is None:
        print(f'első menet: {len(valasztott)} alak -> {KI_MINTA}; a javaslat-tábla még hiányzik')
        return
    rnd = random.Random(SEED + 1)
    tetelek, kulcs, md = [], [], []
    hiba = []
    for w in valasztott:
        if w['tiszta'] not in jav:
            hiba.append(w['tiszta'])
            continue
        javaslat, alternativa, alternativa2, megj = jav[w['tiszta']]
        # három különböző változat; ha a gépi és a javaslat egybeesik, a második alternatíva tölt
        forras = []
        for cimke, k in (('gepi', w['gepi']), ('javaslat', javaslat),
                         ('alternativa', alternativa), ('alternativa2', alternativa2)):
            if not k:
                continue
            for x in forras:
                if x[1] == k:
                    x[0].append(cimke)
                    break
            else:
                if len(forras) < 3:
                    forras.append(([cimke], k))
        if len(forras) != 3:
            hiba.append(f"{w['tiszta']}: nincs három különböző változat {forras}")
            continue
        forras = [('+'.join(c), k) for c, k in forras]
        rnd.shuffle(forras)
        variansok = [{'betu': b, 'kiejtes': k} for b, (_, k) in zip('ABC', forras)]
        t = {'sorszam': w['sorszam'], 'strong': w['strong'], 'heber': w['tiszta'], 'lemma': w['lemma'],
             'igehely': w['igehely'], 'kategoria': KAT_NEV[w['kategoria']], 'variansok': variansok}
        if megj:
            t['megjegyzes'] = megj
        tetelek.append(t)
        kulcs.append({'sorszam': w['sorszam'], 'forras': {b: s for b, (s, _) in zip('ABC', forras)}})
    if hiba:
        raise SystemExit('hiányzó vagy hibás javaslat-sor: ' + '; '.join(hiba))
    with open(KI_JSON, 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'proveniencia': prov + ' | javaslat és alternatíva: manual',
                   'utmutato': 'Alakonként egy vagy több változat jelölhető elfogadhatónak, közülük egy preferált.',
                   'tetelek': tetelek}, f, ensure_ascii=False, indent=1)
        f.write('\n')
    with open(KI_KULCS, 'w', encoding='utf-8', newline='\n') as f:
        json.dump({'proveniencia': prov, 'megjegyzes': 'A betűk forrása; a kalibráló oldalra NEM kerül.',
                   'kulcs': kulcs}, f, ensure_ascii=False, indent=1)
        f.write('\n')
    # összesítés a session javaslatához mérve, a négy konvenció-kombinációval
    # (a felhasználói kalibrálás előtt; a kiértékelés a választás után:
    # naplok/HEBER_KIEJTES_kalibracio_kiertekel.py)
    oszlopok = [('gepi', GEPI_NEV)]
    if MENET == 1:
        oszlopok += [('sz_sz', 'ס és שׂ = sz'), ('pont', 'begadkefat a pontozás szerint'),
                     ('sz_pont', 'mindkettő')]
    ossz = {}
    for w in valasztott:
        javaslat, _, _, megj = jav[w['tiszta']]
        o = ossz.setdefault(w['kategoria'], {'n': 0, 'biz': 0})
        o['n'] += 1
        o['biz'] += bool(megj)
        for k, _ in oszlopok:
            o[k] = o.get(k, 0) + (w[k] == javaslat)
    md.append('# Gépi héber kiejtés — kalibráló minta (N-F131w)' if MENET == 1 else
              '# Gépi héber kiejtés — 2. kalibráló minta, független (N-F131w, DT-F131y után)')
    md.append('')
    md.append('*Kalibrálás, nem döntés: adat (`adat/`) nem változott, szabály nem módosult, lap nem generálódott. '
              'A felhasználó alakonként kiválasztja az elfogadható változato(ka)t és a preferáltat (⛔).*')
    md.append('')
    md.append(f'- **Proveniencia:** `{prov}`; a javasolt és az alternatív változatok: `manual` (a session nyelvtani ítélete, '
              f'`{os.path.relpath(JAVASLAT, ROOT).replace(os.sep, "/")}`).')
    md.append(f'- **Minta:** {len(valasztott)} alak; a 8 lexikonlap motívumainak héber verseiből; {len(jeloltek)} szó, '
              f'{len(egyedi)} egyedi pontozott alak; a TAHOT-sorokból teljes szóvá összerakva (előtag + tő + toldalék); '
              f'a motívum Strongján álló szavak előre, a többi a versek többi szavából. Kategóriánként kvóta, seed {SEED}.'
              + ('' if MENET == 1 else f' Az 1. minta {len(KIZART)} alakja kizárva (nincs átfedés); a gépi változat a '
                 'DT-F131y szabályaival készült; a „vegyes” kategória nehéz jegy nélküli szavakból az átlagos pontossághoz.'))
    md.append(f'- **Változatok:** alakonként három különböző kiejtés, kevert sorrendben (A/B/C, seed {SEED + 1}). '
              f'A forrásuk (gépi / javaslat / alternatíva) a `{os.path.relpath(KI_KULCS, ROOT).replace(os.sep, "/")}`-ban áll; '
              f'az az oldalra nem kerül. Géppel olvasható változat: `{os.path.relpath(KI_JSON, ROOT).replace(os.sep, "/")}`.')
    md.append('- **Válasz a chatben:** sorszám + betű, pl. „1A 2C 3B …”; több elfogadható változat is megadható '
              '(pl. „3BA”: az első betű, B a preferált, A is elfogadható). A kiértékelés két mértéke: '
              '(a) hibás, ha a gépi változat nem elfogadható; (b) konvenció-eltérés, ha elfogadható, de nem a preferált '
              '(`python naplok/HEBER_KIEJTES_kalibracio_kiertekel.py --chat "1A 2C 3BA …"`).')
    md.append('')
    md.append('## Összesítés a session javaslatához mérve (a felhasználói választás előtt)')
    md.append('')
    md.append('A „helyes” itt azt jelenti: a gépi alak megegyezik a javasolt alakkal. A javaslat konvenciója: '
              'ס és שׂ = sz, a szókezdő begadkefatról a pontozás dönt. Az sz/s és a kemény/lágy kérdés miatt '
              'a gépi alakot négy konvenció-kombinációval is összevetettem.' if MENET == 1 else
              'A „helyes” itt azt jelenti: a gépi alak (DT-F131y) megegyezik a javasolt alakkal. A javaslat a '
              'DT-F131y konvencióit követi (ס/שׂ = sz, ח = ch, kámec á a kivételekkel, R3, R5, Jahve, jerúsálajim).')
    md.append('')
    md.append('| kategória | n | ' + ' | '.join(f'helyes: {nev}' for _, nev in oszlopok) + ' | bizonytalan |')
    md.append('|---|---|' + '---|' * len(oszlopok) + '---|')
    tot = {k: 0 for k, _ in oszlopok}
    tot_n = tot_b = 0
    for kat, _ in KVOTA:
        o = ossz.get(kat, {'n': 0, 'biz': 0})
        md.append(f"| {KAT_NEV[kat]} | {o['n']} | " + ' | '.join(f"{o.get(k, 0)}" for k, _ in oszlopok)
                  + f" | {o['biz']} |")
        for k, _ in oszlopok:
            tot[k] += o.get(k, 0)
        tot_n += o['n']
        tot_b += o['biz']
    md.append(f'| **összesen** | {tot_n} | ' + ' | '.join(f'**{tot[k]}**' for k, _ in oszlopok) + f' | {tot_b} |')
    md.append('')
    md.append('## A minta')
    md.append('')
    md.append('| # | kategória | igehely | Strong | lemma | héber alak | A | B | C | megjegyzés |')
    md.append('|---|---|---|---|---|---|---|---|---|---|')
    for t in tetelek:
        v = {x['betu']: x['kiejtes'] for x in t['variansok']}
        md.append(f"| {t['sorszam']} | {t['kategoria']} | {t['igehely']} | {t['strong']} | {t['lemma']} | "
                  f"{t['heber']} | {v['A']} | {v['B']} | {v['C']} | {t.get('megjegyzes', '')} |")
    with open(KI_MD, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(md) + '\n')
    print(f'{len(tetelek)} tétel -> {KI_JSON}, {KI_KULCS}, {KI_MD}')


if __name__ == '__main__':
    beallit(int(sys.argv[sys.argv.index('--menet') + 1]) if '--menet' in sys.argv else 1)
    main()
