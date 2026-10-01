#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/emeles.py -- F28_EMELES_BRIEF.md: a lexikonba kerulo Strong-szamok
teljes Thayer- (G) es BDB- (H) szocikkenek emelese (Opus-forditasa).

Alparancsok:

  lista   E0: a Strong-halmaz (adat/elofordulasok.tsv `strong` mezojenek G/H
          tokenjei, a `+` menten bontva, meg az adat/lexikon_hivatkozasok.tsv
          Thayer- es BDB-sorainak `strong`-ja), szotaranként a teljes szocikk
          karakterszamaval es a meglevo `kezi` sorokkal ->
          naplok/EMELES_lista.tsv. Kimarad (kimarad=igen), amelynek mar van
          `teljes` szintu `kezi` forditasa.

  prompt  E1/E4: a prompt v4 kitoltese egy Strong-szamra (vagy annak egy
          darabjara) -> stdout vagy --ki fajl.

  forras  a teljes forras-szocikk kiirasa (--ki fajlba), a forditashoz.

  darabok E4: a darabolasi javaslat (jelentes-/torzshatar) kiirasa.

    python eszkozok/emeles.py lista
    python eszkozok/emeles.py prompt H7121 --ki /tmp/.../H7121_prompt.md
    python eszkozok/emeles.py forras H7121 --ki /tmp/.../H7121_forras.txt

A TSV-olvasas split('\\t'), az iras '\\t'.join() (CLAUDE.md, TSV-olvasas).
"""

import argparse
import hashlib
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ELOFORDULASOK_UT = os.path.join(REPO, 'adat', 'elofordulasok.tsv')
LEX_HIV_UT = os.path.join(REPO, 'adat', 'lexikon_hivatkozasok.tsv')
FORDITASOK_UT = os.path.join(REPO, 'adat', 'forditasok.tsv')
TERMINOLOGIA_UT = os.path.join(REPO, 'adat', 'terminologia.tsv')
THAYER_UT = os.path.join(REPO, 'konkordancia', 'Thayer_teljes.tsv')
BDB_UT = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
KAROLI_UT = os.path.join(REPO, 'konkordancia', 'Konyv_normalizalo_tabla.tsv')
PROMPT_UT = os.path.join(REPO, 'forditas', 'prompt_v4.md')
LISTA_UT = os.path.join(REPO, 'naplok', 'EMELES_lista.tsv')
PROMPT_JELOLO = '\n<!-- PROMPT-KEZDET -->\n'

LISTA_FEJLEC = ['strong', 'szotar', 'entry_id', 'karakter', 'forras_hash',
                'forras_eredet', 'kezi_sorok', 'kimarad']

STRONG_TOKEN = re.compile(r'^[GH]\d{1,4}[a-z]?$')

# Daraboasi hatar (E4): ennel hosszabb szocikk darabolasi javaslatot kap.
DARAB_HATAR = 6000


# ---------------------------------------------------------------------------
# TSV
# ---------------------------------------------------------------------------

def tsv_sorok(ut):
    with open(ut, encoding='utf-8', newline='') as fh:
        for sor in fh.read().split('\n'):
            sor = sor.rstrip('\r')
            if sor:
                yield sor.split('\t')


def tsv_dict_sorok(ut):
    fejlec = None
    for m in tsv_sorok(ut):
        if m[0].startswith('#'):
            continue
        if fejlec is None:
            fejlec = m
            continue
        yield dict(zip(fejlec, m))


def tsv_ir(ut, fejlec, sorok, megjegyzes=None):
    with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
        if megjegyzes:
            fh.write('# ' + megjegyzes + '\n')
        fh.write('\t'.join(fejlec) + '\n')
        for sor in sorok:
            fh.write('\t'.join(str(sor.get(mezo, '')) for mezo in fejlec) + '\n')


# ---------------------------------------------------------------------------
# Strong-szamok
# ---------------------------------------------------------------------------

def strong_padded(s):
    """G12 -> G0012, H1121 -> H1121 (a konkordancia kulcsa)."""
    m = re.match(r'^([GH])(\d{1,4})([a-z]?)$', s)
    if not m:
        return None
    return '%s%04d%s' % (m.group(1), int(m.group(2)), m.group(3))


def strong_eredeti(s):
    m = re.match(r'^([GH])0*(\d+)([a-z]?)$', s)
    return '%s%s%s' % (m.group(1), m.group(2), m.group(3))


def szotar_strongnak(s):
    return 'Thayer' if s.startswith('G') else 'BDB'


def szotar_betolt(szotar):
    ut = THAYER_UT if szotar == 'Thayer' else BDB_UT
    return {r['Strong_padded']: r['Teljes_szocikk'] for r in tsv_dict_sorok(ut)}


def forras_hash(szoveg):
    return hashlib.sha1(szoveg.encode('utf-8')).hexdigest()


MINDEN_TOKEN = re.compile(r'\b([GH]\d{4})\b')


def strong_halmaz_szeles():
    """Osszevetesi halmaz (E0 eltérésnaplo): a ket tabla BARMELY mezojenek
    G/H-tokenje (kapcsolodas, karoli_szo, gerinc_elem, a TBESG/LSJ sorok is).
    A brief 2. pontjanak szamai ezzel a meressel egyeznek; a `lista`
    alapertelmezese NEM ez, hanem a brief szovege szerinti halmaz."""
    halmaz = {}
    for ut, nev in ((ELOFORDULASOK_UT, 'elofordulasok'), (LEX_HIV_UT, 'lexikon_hivatkozasok')):
        with open(ut, encoding='utf-8', newline='') as fh:
            for sor in fh.read().split('\n'):
                if not sor or sor.startswith('#'):
                    continue
                for t in MINDEN_TOKEN.findall(sor):
                    halmaz.setdefault(t, set()).add(nev)
    return halmaz


def strong_halmaz():
    """{strong_padded: set(eredet)} -- eredet: 'elofordulasok' / 'lexikon_hivatkozasok'."""
    halmaz = {}
    for r in tsv_dict_sorok(ELOFORDULASOK_UT):
        for tok in (r.get('strong') or '').split('+'):
            tok = tok.strip()
            if not tok or not STRONG_TOKEN.match(tok):
                continue
            halmaz.setdefault(strong_padded(tok), set()).add('elofordulasok')
    for r in tsv_dict_sorok(LEX_HIV_UT):
        if r.get('szotar') not in ('Thayer', 'BDB'):
            continue
        tok = (r.get('strong') or '').strip()
        if not STRONG_TOKEN.match(tok):
            continue
        halmaz.setdefault(strong_padded(tok), set()).add('lexikon_hivatkozasok')
    return halmaz


def kezi_sorok_strongra(forditasok, sp):
    """A meglevo kezi sorok (szotar:jelentes_szam) egy Strong-szamra, a
    Thayer/BDB szotarakbol (a TBESG/UBS stb. sorok a teljes szocikket nem
    helyettesitik, de jelezzuk oket)."""
    ki = []
    for r in forditasok:
        if r.get('allapot') != 'kezi':
            continue
        rs = r.get('strong') or ''
        if not STRONG_TOKEN.match(rs) or strong_padded(rs) != sp:
            continue
        ki.append('%s:%s' % (r['szotar'], r['jelentes_szam']))
    return ki


def lista_epit(szeles=False):
    halmaz = strong_halmaz_szeles() if szeles else strong_halmaz()
    forditasok = list(tsv_dict_sorok(FORDITASOK_UT))
    thayer = szotar_betolt('Thayer')
    bdb = szotar_betolt('BDB')
    sorok = []
    for sp in sorted(halmaz, key=lambda s: (s[0] != 'G', s)):
        szotar = szotar_strongnak(sp)
        szoveg = (thayer if szotar == 'Thayer' else bdb).get(sp)
        kezi = kezi_sorok_strongra(forditasok, sp)
        teljes_kezi = any(k == '%s:teljes' % szotar for k in kezi)
        sorok.append({
            'strong': sp,
            'szotar': szotar,
            'entry_id': strong_eredeti(sp),
            'karakter': len(szoveg) if szoveg is not None else 'NINCS_SZOCIKK',
            'forras_hash': forras_hash(szoveg) if szoveg is not None else '',
            'forras_eredet': '+'.join(sorted(halmaz[sp])),
            'kezi_sorok': ';'.join(kezi),
            'kimarad': 'igen' if teljes_kezi else 'nem',
        })
    return sorok


def cmd_lista(args):
    sorok = lista_epit(szeles=args.szeles)
    if args.szeles:
        print('(--szeles: osszevetes, a lista fajl nem irodik)')
    else:
        tsv_ir(LISTA_UT, LISTA_FEJLEC, sorok,
               megjegyzes='F28 E0 -- generalja: python eszkozok/emeles.py lista')
        print('irva: %s (%d sor)' % (os.path.relpath(LISTA_UT, REPO), len(sorok)))
    for szotar in ('Thayer', 'BDB'):
        mind = [s for s in sorok if s['szotar'] == szotar]
        akt = [s for s in mind if s['kimarad'] == 'nem' and isinstance(s['karakter'], int)]
        nincs = [s['strong'] for s in mind if not isinstance(s['karakter'], int)]
        kar = sum(s['karakter'] for s in akt)
        leghosszabb = max(akt, key=lambda s: s['karakter']) if akt else None
        print('%-6s osszes %2d | kimarad %d | forditando %2d | karakter %7d | leghosszabb %s (%s)%s'
              % (szotar, len(mind), sum(1 for s in mind if s['kimarad'] == 'igen'), len(akt), kar,
                 leghosszabb['strong'] if leghosszabb else '-',
                 leghosszabb['karakter'] if leghosszabb else '-',
                 ' | nincs szocikk: ' + ','.join(nincs) if nincs else ''))
    akt = [s for s in sorok if s['kimarad'] == 'nem' and isinstance(s['karakter'], int)]
    print('Osszesen forditando %d szocikk, %d karakter'
          % (len(akt), sum(s['karakter'] for s in akt)))


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

def terminologia_szoveg():
    sorok = list(tsv_dict_sorok(TERMINOLOGIA_UT))
    verziok = sorted({r['verzio'] for r in sorok if r.get('verzio')})
    jelen = verziok[-1] if verziok else ''
    ki = []
    for r in sorok:
        if r.get('megjegyzes'):
            ki.append('- `%s` = %s (%s)' % (r['angol'], r['magyar'], r['megjegyzes']))
        else:
            ki.append('- `%s` = %s' % (r['angol'], r['magyar']))
    return '\n'.join(ki), jelen


def karoli_szoveg():
    return '\n'.join('- `%s` → `%s`' % (r['STEPBible-rövidítés'], r['Magyar rövidítés'])
                     for r in tsv_dict_sorok(KAROLI_UT))


def darab_info_szoveg(i, n):
    if n == 1:
        return ''
    return (' (%d/%d. rész -- csak ezt a részt fordítsd önmagában álló szövegként; '
            'a folytatás külön hívásban érkezik, NE told ki a hiányzó résszel, és '
            'ne jelezd a szöveg részlegességét)') % (i + 1, n)


def prompt_epit(strong, forras_darab, darab_info=''):
    with open(PROMPT_UT, encoding='utf-8') as fh:
        sablon = fh.read()
    # a jelolo feletti resz (fejlec, verzionaplo) nem prompt
    sablon = sablon.split(PROMPT_JELOLO, 1)[1].lstrip('\n')
    term, _ = terminologia_szoveg()
    szotar = szotar_strongnak(strong)
    return (sablon
            .replace('{{SZOTAR}}', 'Thayer' if szotar == 'Thayer' else 'BDB')
            .replace('{{TERMINOLOGIA}}', term)
            .replace('{{KAROLI_TABLA}}', karoli_szoveg())
            .replace('{{STRONG}}', strong_eredeti(strong))
            .replace('{{DARAB_MEGJEGYZES}}', darab_info)
            .replace('{{FORRAS_SZOVEG}}', forras_darab))


def forras_szoveg(strong):
    sp = strong_padded(strong)
    szoveg = szotar_betolt(szotar_strongnak(sp)).get(sp)
    if szoveg is None:
        raise SystemExit('nincs szocikk: %s' % strong)
    return sp, szoveg


def kiir(szoveg, ut):
    if ut:
        with open(ut, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(szoveg)
        print('irva: %s (%d karakter)' % (ut, len(szoveg)))
    else:
        print(szoveg)


# ---------------------------------------------------------------------------
# Helyorzok (E4 segedeszkoz): a heber/gorog szakaszok szo szerinti
# megorzese. A forditando szovegben minden osszefuggo heber/gorog szakasz
# (szavak egyetlen szokozzel elvalasztva) ⟦n⟧ helyorzot kap; a forditas
# utan a `visszaallit` betuhiven visszairja oket. Igy a v4 BDB-blokk 3.
# szabalya (a heber szoveg valtozatlan, a jobbrol balra irassal egyutt)
# gepileg teljesul; a 1_gorog_heber kapu ezt utolag is ellenorzi.
# ---------------------------------------------------------------------------

_HG_KAR = 'Ͱ-Ͽἀ-῿֐-׿יִ-ﭏ̀-ͯ'
HG_SZAKASZ = re.compile(r'[%s]+(?: [%s]+)*' % (_HG_KAR, _HG_KAR))
HELYORZO = re.compile(r'⟦(\d+)⟧')


def helyorzo_bont(szoveg):
    szakaszok = []

    def _csere(m):
        szakaszok.append(m.group(0))
        return '⟦%d⟧' % len(szakaszok)
    return HG_SZAKASZ.sub(_csere, szoveg), szakaszok


def helyorzo_visszaallit(szoveg, szakaszok):
    hasznalt = []

    def _csere(m):
        i = int(m.group(1))
        hasznalt.append(i)
        return szakaszok[i - 1]
    ki = HELYORZO.sub(_csere, szoveg)
    hiany = sorted(set(range(1, len(szakaszok) + 1)) - set(hasznalt))
    tobbszor = sorted({i for i in hasznalt if hasznalt.count(i) > 1})
    return ki, hiany, tobbszor


def cmd_helyorzo(args):
    import json
    sp, szoveg = forras_szoveg(args.strong)
    bontott, szakaszok = helyorzo_bont(szoveg)
    alap = os.path.join(args.mappa, sp)
    kiir(bontott, alap + '_hely.txt')
    with open(alap + '_hely.json', 'w', encoding='utf-8') as fh:
        json.dump(szakaszok, fh, ensure_ascii=False, indent=0)
    print('helyorzo: %d szakasz' % len(szakaszok))


def cmd_visszaallit(args):
    import json
    sp = strong_padded(args.strong)
    with open(os.path.join(args.mappa, sp + '_hely.json'), encoding='utf-8') as fh:
        szakaszok = json.load(fh)
    with open(args.be, encoding='utf-8') as fh:
        vazlat = fh.read().strip('\n')
    ki, hiany, tobbszor = helyorzo_visszaallit(vazlat, szakaszok)
    if hiany or tobbszor:
        print('FIGYELEM: hianyzo helyorzok %s; tobbszor hasznalt %s' % (hiany, tobbszor))
    kiir(ki, args.ki)


def utofeldolgoz(strong, nyers):
    """E4: javitoreteg + kapuk. -> (vegleges, normalizalas_valtozasai, kapueredmenyek, atment)"""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import normalizal as N
    import forditas_kapuk as K
    sp, forras = forras_szoveg(strong)
    szotar = szotar_strongnak(sp)
    vegleges, valt = N.normalizal(nyers, szotar)
    eredm = K.kapuk_futtat(szotar, forras, vegleges)
    return vegleges, valt, eredm, K.atment(eredm)


def cmd_ellenoriz(args):
    import json
    sp = strong_padded(args.strong)
    with open(args.be, encoding='utf-8') as fh:
        vazlat = fh.read().strip('\n')
    if args.mappa:
        with open(os.path.join(args.mappa, sp + '_hely.json'), encoding='utf-8') as fh:
            szakaszok = json.load(fh)
        vazlat, hiany, tobbszor = helyorzo_visszaallit(vazlat, szakaszok)
        if hiany or tobbszor:
            print('FIGYELEM: hianyzo helyorzok %s; tobbszor hasznalt %s' % (hiany, tobbszor))
    vegleges, valt, eredm, ok = utofeldolgoz(sp, vazlat)
    print('javitoreteg: %s' % (', '.join('%s=%d' % v for v in valt) or 'nincs valtozas'))
    for n, e, r in eredm:
        print('  %-22s %-8s %s' % (n, e, r))
    print('ATMENT' if ok else 'BUKOTT')
    if args.ki:
        kiir(vegleges, args.ki)


FORDITASOK_FEJLEC = ['szotar', 'strong', 'entry_id', 'jelentes_szam', 'mezo', 'forras_hash',
                     'forditas_hu', 'allapot', 'modell', 'datum', 'terminologia_verzio', 'megjegyzes']
MUNKA_UT = os.path.join(REPO, 'naplok', 'EMELES_munka.tsv')


def cmd_rogzit(args):
    """A vegleges forditas rogzitese a munkatablaba (naplok/EMELES_munka.tsv),
    az adat/forditasok.tsv semajaval. Az adat/forditasok.tsv-be a
    jovahagyas utan kerul (E4a: kezi; E4: opus)."""
    import datetime
    sp, forras = forras_szoveg(args.strong)
    with open(args.be, encoding='utf-8') as fh:
        szoveg = fh.read().strip('\n')
    if '\t' in szoveg or '\n' in szoveg:
        raise SystemExit('a forditas tabot vagy sortorest tartalmaz -- TSV-be nem irhato')
    vegleges, valt, eredm, ok = utofeldolgoz(sp, szoveg)
    if vegleges != szoveg:
        raise SystemExit('a --be nem a javitoreteg kimenete (futtasd elobb: ellenoriz --ki)')
    if not ok:
        raise SystemExit('kapuhiba -- a sor nem rogzitheto (E4: onujraproba, utana bukottak)')
    _, term_verzio = terminologia_szoveg()
    sorok = list(tsv_dict_sorok(MUNKA_UT)) if os.path.exists(MUNKA_UT) else []
    szotar = szotar_strongnak(sp)
    uj = {
        # a lexikon_hivatkozasok.tsv konvencioja: strong = padded, entry_id = a
        # konkordancia Strong_eredeti mezoje (G0012 / G12)
        'szotar': szotar, 'strong': sp,
        'entry_id': strong_eredeti(sp), 'jelentes_szam': 'teljes', 'mezo': 'forditas_hu',
        'forras_hash': forras_hash(forras), 'forditas_hu': szoveg, 'allapot': args.allapot,
        'modell': args.modell, 'datum': args.datum or datetime.date.today().strftime('%Y.%m.%d'),
        'terminologia_verzio': term_verzio, 'megjegyzes': args.megjegyzes or '',
    }
    sorok = [r for r in sorok if not (r['szotar'] == uj['szotar'] and r['entry_id'] == uj['entry_id'])]
    sorok.append(uj)
    tsv_ir(MUNKA_UT, FORDITASOK_FEJLEC, sorok,
           megjegyzes='F28 munkatabla (adat/forditasok.tsv semaja) -- jovahagyas elott; '
                      'irja: python eszkozok/emeles.py rogzit')
    print('rogzitve: %s %s (%d karakter) -> %s' % (szotar, sp, len(szoveg), os.path.relpath(MUNKA_UT, REPO)))


def cmd_prompt(args):
    sp, szoveg = forras_szoveg(args.strong)
    kiir(prompt_epit(sp, szoveg), args.ki)


def cmd_forras(args):
    sp, szoveg = forras_szoveg(args.strong)
    kiir(szoveg, args.ki)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[1])
    al = ap.add_subparsers(dest='parancs', required=True)
    p = al.add_parser('lista')
    p.add_argument('--szeles', action='store_true',
                   help='osszevetes: a ket tabla barmely mezojenek G/H-tokenjei (nem ir fajlt)')
    p.set_defaults(fv=cmd_lista)
    p = al.add_parser('prompt')
    p.add_argument('strong')
    p.add_argument('--ki')
    p.set_defaults(fv=cmd_prompt)
    p = al.add_parser('forras')
    p.add_argument('strong')
    p.add_argument('--ki')
    p.set_defaults(fv=cmd_forras)
    p = al.add_parser('helyorzo')
    p.add_argument('strong')
    p.add_argument('--mappa', required=True)
    p.set_defaults(fv=cmd_helyorzo)
    p = al.add_parser('visszaallit')
    p.add_argument('strong')
    p.add_argument('--mappa', required=True)
    p.add_argument('--be', required=True)
    p.add_argument('--ki', required=True)
    p.set_defaults(fv=cmd_visszaallit)
    p = al.add_parser('ellenoriz')
    p.add_argument('strong')
    p.add_argument('--be', required=True, help='a forditas (helyorzos vazlat, ha --mappa adott)')
    p.add_argument('--mappa', help='a helyorzo-fajlok mappaja')
    p.add_argument('--ki', help='a vegleges (visszaallitott, normalizalt) forditas')
    p.set_defaults(fv=cmd_ellenoriz)
    p = al.add_parser('rogzit')
    p.add_argument('strong')
    p.add_argument('--be', required=True, help='a vegleges forditas (az ellenoriz --ki kimenete)')
    p.add_argument('--allapot', default='opus', choices=['opus', 'kezi'])
    p.add_argument('--modell', default='claude-opus-5-5')
    p.add_argument('--datum')
    p.add_argument('--megjegyzes')
    p.set_defaults(fv=cmd_rogzit)
    args = ap.parse_args()
    args.fv(args)


if __name__ == '__main__':
    main()
