#!/usr/bin/env python
"""A `Thayer_teljes.tsv` szövegvesztésének javítótáblája (F132; FELADATOK #132; DT-F132i (2); a DT228 / `bdb_forras_javitas.tsv` mintája).

A DT-F132a (b) szerint a Thayer-szakasz szövege a `konkordancia/Thayer_teljes.tsv`-ből jön. 15 Strongban a TSV egy-egy
összefüggő szövegrészt elveszít a `Thayer.lexicon`-hoz képest (a TSV-konverzió hibája, M1). Ez az eszköz a lyukakat
**a nyers fájlok és a szakasztábla érintése nélkül** rögzíti: a hiányzó szöveg a lexikon adott bekezdésének címkék nélküli
szövegéből (`bont.sima`) jön, soronként igazolva. A bontó (`bont.py`) a táblát csak a szakaszhatárokhoz használja (a
`thayer_szakaszok.tsv` `szoveg` mezője nyers marad, az illesztés `javitassal`); a javított szöveg **nézet**
(`thayer_bemenet.szakaszok`).

Egy sor = egy lyuk (`hiba = tsv_szovegvesztes`). Feltétel (`allapot = javitva`), mind gépi:
  1. a Strong illesztése a nyers TSV-vel `reszleges`, és a lexikon (szóközök nélkül) és a TSV (szóközök nélkül) eltérése
     egyetlen törlés (difflib: egy nem `equal` művelet, `delete`), amely egyetlen bekezdés belsejébe esik;
  2. a beszúrandó szöveg (`javitott_alak`) a lexikonbekezdés sima szövege a lyuk előtti utolsó nem-szóköz karakter utántól a
     lyuk utolsó karakteréig (a lyuk előtti szóköz is a lexikoné);
  3. a beszúrással a Strong illesztése `egyezik` (`bont.illeszt_javitassal`), a beszúrás egy sor belsejébe esik, és a javított
     sor szövege (szóközök nélkül, `jel`-lel) = a lexikonbekezdés sima szövege (szóközök nélkül).
Ha bármelyik nem teljesül: `jelolt_marad` (nincs javítás, a sor indoka a hibát mondja; a bontó `reszleges`-t ír).

  python eszkozok/thayer_jelolt/forras_javit.py [--ts NAP] [--ellenoriz]
TSV: split('\\t') / '\\t'.join, csv modul nélkül.
"""
import argparse
import datetime
import difflib
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
if ITT not in sys.path:
    sys.path.insert(0, ITT)
import bont  # noqa: E402

KI_UT = bont.JAV_UT
FEJLEC = ['strong', 'sorszam', 'hiba', 'tsv_poz', 'sor_poz', 'elotte', 'javitott_alak', 'utana', 'hossz', 'allapot', 'indok',
          'proveniencia']
KORNYEZET = 20
WS = re.compile(r'\s+')


def kod_hash():
    h = hashlib.sha256()
    for ut in (os.path.abspath(__file__), os.path.join(ITT, 'bont.py'), os.path.join(ITT, 'kulcs.py')):
        with open(ut, 'rb') as f:
            h.update(f.read().replace(b'\r\n', b'\n'))
    return h.hexdigest()


def nows(s):
    return WS.sub('', s)


def lyuk(sp, topic, d, tsv_szoveg, ts):
    """Egy `reszleges` Strong javítósora (dict), a modul docstringjének 1–3. feltétele szerint."""
    prov = 'scope=%s | forras=thayer_jelolt/forras_javit.py (fejléc) | ts=%s' % (sp, ts)
    ures = {'strong': sp, 'sorszam': '', 'hiba': 'tsv_szovegvesztes', 'tsv_poz': '', 'sor_poz': '', 'elotte': '',
            'javitott_alak': '', 'utana': '', 'hossz': '', 'allapot': 'jelolt_marad', 'indok': '', 'proveniencia': prov}
    szak = bont.szerkezet(d)
    darabok = [bont._nows(x['plain'])[0] for x in szak]
    L = ''.join(darabok)
    T, idx = bont._nows(tsv_szoveg)
    ops = [o for o in difflib.SequenceMatcher(None, L, T, autojunk=False).get_opcodes() if o[0] != 'equal']
    if len(ops) != 1 or ops[0][0] != 'delete':
        ures['indok'] = 'a lexikon és a TSV eltérése nem egyetlen törlés (%d művelet)' % len(ops)
        return ures
    _, a1, a2, b1, _ = ops[0]
    cum = [0]
    for x in darabok:
        cum.append(cum[-1] + len(x))
    bek = [k for k in range(len(darabok)) if cum[k] < a2 and cum[k + 1] > a1]
    if len(bek) != 1 or a1 == cum[bek[0]] or b1 == 0:
        ures['indok'] = 'a lyuk nem egyetlen bekezdés belsejében áll (bekezdés: %s)' % ','.join(str(k + 1) for k in bek)
        return ures
    k = bek[0]
    P = szak[k]['plain']
    _, pidx = bont._nows(P)
    la, lb = a1 - cum[k], a2 - cum[k]
    alak = P[pidx[la - 1] + 1:pidx[lb - 1] + 1]
    tsv_poz = idx[b1 - 1] + 1
    jr = bont.illeszt_javitassal(szak, tsv_szoveg, [(tsv_poz, alak)])
    if jr is None or len(jr[2]) != 1:
        ures['indok'] = 'a beszúrással az illesztés nem egyezik, vagy a beszúrás nem egy sor belsejébe esik'
        return ures
    _, szovegek, ((i, p, al),) = jr
    sor = szovegek[i]
    javitott = sor[:p] + al + sor[p:]
    if i != k or nows(szak[i]['jel'] + javitott) != nows(P):
        ures['indok'] = 'a javított sor szövege nem egyezik a lexikonbekezdéssel (sor %d, bekezdés %d)' % (i + 1, k + 1)
        return ures
    return {'strong': sp, 'sorszam': str(i + 1), 'hiba': 'tsv_szovegvesztes', 'tsv_poz': str(tsv_poz), 'sor_poz': str(p),
            'elotte': sor[max(0, p - KORNYEZET):p], 'javitott_alak': al, 'utana': sor[p:p + KORNYEZET], 'hossz': str(len(nows(al))),
            'allapot': 'javitva',
            'indok': 'a TSV a lexikon %s#%d bekezdéséből %d karaktert (szóközök nélkül) veszít, egyetlen törlésként; a beszúrással '
                     'a Strong illesztése egyezik, és a sor szövege (szóközök nélkül) = a lexikonbekezdés címkék nélküli szövege'
                     % (topic, k + 1, len(nows(al))),
            'proveniencia': prov}


def general(ts):
    lex = bont.lexikon_beolvas()
    tsv = bont.tsv_beolvas()
    ki = []
    for sp, (topic, d) in lex.items():
        if sp not in tsv:
            continue
        kat, _ = bont.illeszt(bont.szerkezet(d), tsv[sp])
        if kat != 'reszleges':
            continue
        r = lyuk(sp, topic, d, tsv[sp], ts)
        for m in FEJLEC:
            if '\t' in r[m] or '\n' in r[m]:
                raise ValueError('tab/sortörés: %s %s' % (sp, m))
        ki.append(r)
    return ki


def fajl_szoveg(sorok, ts):
    fej = ['# GENERÁLT: eszkozok/thayer_jelolt/forras_javit.py --ts %s — kézzel nem szerkesztendő (F132, DT-F132i (2); séma: '
           'adat/SEMA.md 2.38).' % ts,
           '# forras: konkordancia/lexikonok_nyers/Thayer.lexicon@%s (a hiányzó szöveg és az igazolás) + '
           'konkordancia/Thayer_teljes.tsv@%s + kód@%s'
           % (bont.sha256_fajl(bont.LEX_UT)[:12], bont.sha256_fajl(bont.TSV_UT)[:12], kod_hash()[:12]),
           '\t'.join(FEJLEC)]
    return '\n'.join(fej + ['\t'.join(r[m] for m in FEJLEC) for r in sorok]) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts')
    ap.add_argument('--ellenoriz', action='store_true')
    a = ap.parse_args()
    ts = a.ts or (bont.fajl_ts(KI_UT) if a.ellenoriz and os.path.exists(KI_UT) else None) or datetime.date.today().isoformat()
    sorok = general(ts)
    jav = [r for r in sorok if r['allapot'] == 'javitva']
    print('lyuk: %d; javitva: %d (%d karakter szóközök nélkül); jelolt_marad: %d'
          % (len(sorok), len(jav), sum(int(r['hossz']) for r in jav), len(sorok) - len(jav)))
    for r in sorok:
        print('  %s #%s %s %s' % (r['strong'], r['sorszam'], r['allapot'], r['hossz'] or r['indok']))
    szoveg = fajl_szoveg(sorok, ts)
    if a.ellenoriz:
        if not os.path.exists(KI_UT):
            print('NINCS: %s' % KI_UT)
            return 1
        with open(KI_UT, encoding='utf-8', newline='') as f:
            if f.read() != szoveg:
                print('ELTÉR: %s' % KI_UT)
                return 1
        print('azonos: %s' % KI_UT)
        return 0
    with open(KI_UT, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('írva: %s' % KI_UT)
    return 0


if __name__ == '__main__':
    sys.exit(main())
