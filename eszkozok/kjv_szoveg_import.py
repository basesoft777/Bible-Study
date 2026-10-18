#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
kjv_szoveg_import.py -- #118 (F118, KJV_SZOVEG): a teljes KJV-szoveg importja versenkent az eBible USFM-bol.

Bemenet (--munka mappa):
  kjv.zip   https://ebible.org/Scriptures/eng-kjv_usfm.zip (a szkript NEM tolt le; zipfile-lal olvas, nem bont ki)
Kimenet (--kimenet, alapertelmezes: konkordancia/KJV_teljes_szoveg.tsv):
  Igehely | Szöveg | Szöveg_jelolt | Elotte | Utoirat

Dontesek: DT-F118b (a) -- sajat importalo; az f19_ebible_import-bol a konyvlista es a regex-mintak jonnek
(kodmasolas nelkul), a vers-szetvagas es a szovegtisztitas sajat, mert az F19 parse_usfm a vers nelkuli sort
az elozo vershez fuzi (Zsolt 119 \\s1, pali utoiratok), es a zaro jelolo helyen szokozt hagy (naplok/KJV_SZOVEG_M0.md).
DT-F118a 1. -- a szovegreteg kozkincs; Strong-cimke nincs benne (a cimkereteg: KJV_Strongs_teljes.tsv, DT126).
DT-F118d (d) -- a zip a repon kivul marad; a hash a fejlecben.

Szabalyok (naplok/KJV_SZOVEG_M0.md 2. es 4. pont):
  Igehely       STEP-alak (Gen.1.1), KJV-szamozas, a zsoltarfelirat (\\d) verse 0
  Szöveg        olvasoszoveg: jelolo, lab-jegyzet es pilcrow nelkul; \\w -> a szo; \\add, \\nd, \\wj, \\tl -> a szoveg
  Szöveg_jelolt mint a Szöveg, de \\add -> [..], \\wj -> ‹..› (DT-F118e (4); versenkent zarva), es a pilcrow (¶) megmarad;
                az 1Jn 2:23 forrasbeli „[but]”-ja a forras szerint marad (DT-F118e (3))
  Elotte        a vers elotti \\s1 cimsor (Zsolt 119 akrosztichon), olvasoszovegkent
  Utoirat       a konyv utolso verse utani \\s1 (pali utoiratok), olvasoszovegkent
A leltaron kivuli jelolo hibat dob (nem nemán esik ki). TSV-iras: '\\t'.join, csv modul nelkul.

Futtatas:  python eszkozok/kjv_szoveg_import.py --munka <mappa> [--kimenet <fajl>]
"""

import argparse
import collections
import datetime
import hashlib
import os
import re
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import f19_ebible_import as f19  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = f19.REPO
BS = f19.BS
E = f19.E
VART_SHA256 = '00532b6db1825cb78fd34de2097fc280ce03ee22ef0bdac5243ef4beaca4d447'  # DT-F118 egyeztetett elteres: a 2026-10-17-i csomag
FORRAS_URL = 'https://ebible.org/Scriptures/eng-kjv_usfm.zip'
PILCROW = '¶'
WJ_NYIT, WJ_ZAR = '‹', '›'  # ‹ › -- a \wj jelolese a Szöveg_jelolt-ban (DT-F118e (4))

# a leltar (naplok/KJV_SZOVEG_M0_jelolok.tsv) jeloloi, bánásmód szerint
FEJLEC_JELOLOK = {'id', 'h', 'toc1', 'toc2', 'toc3', 'mt1', 'mt2'}      # az elso \c elott: kimarad
BEKEZDES_JELOLOK = {'p', 'q1', 'b'}                                       # tagolas: kimarad (vesztesegkent szamolva)
KARAKTER_JELOLOK = {'nd', 'wj', 'tl'}                                     # a szoveg marad, a jelolo kimarad
RE_JEL = re.compile(E + r'(\+?)([a-z]+[0-9]*)(?:(\*)| ?)')  # nyito: egy szokozt elnyel; zaro (*): semmit
RE_W_ATTR_NELKUL = re.compile(E + r'\+?w ([^|' + E + r']*?)' + E + r'\+?w\*')


class IsmeretlenJelolo(ValueError):
    pass


def tisztit(nyers, jelolt=False, szamlalo=None):
    """Egy vers (vagy cimsor) nyers USFM-szovegebol olvasoszoveg. A labjegyzetet a hivo mar eltavolitotta
    (f19.RE_FN), de biztonsagbol itt is torolve. jelolt=True: \\add -> [..], a pilcrow marad."""
    sz = szamlalo if szamlalo is not None else collections.Counter()
    t = f19.RE_FN.sub('', nyers)
    sz['w'] += len(f19.RE_W.findall(t))
    t = f19.RE_W.sub(lambda m: m.group(1), t)
    t = RE_W_ATTR_NELKUL.sub(lambda m: m.group(1), t)

    def jel(m):
        nev, zaro = m.group(2), m.group(3) == '*'
        if nev == 'add':
            sz['add'] += 0 if zaro else 1
            if jelolt:
                return ']' if zaro else '['
            return ''
        if nev == 'wj' and jelolt:  # DT-F118e (4): Jezus szavai a Szöveg_jelolt-ban ‹…›
            return WJ_ZAR if zaro else WJ_NYIT
        if nev in KARAKTER_JELOLOK:
            sz[nev] += 0 if zaro else 1
            return ''
        if nev in BEKEZDES_JELOLOK and not zaro:
            sz[nev] += 1
            return ' '
        raise IsmeretlenJelolo('leltaron kivuli jelolo: %r a szovegben: %r' % (m.group(0), nyers[:80]))

    # a zaro jelolo utani szokoz a szoveghez tartozik: csak a nyito jelolo utani egy szokozt nyeli el a minta
    t = RE_JEL.sub(jel, t)
    if PILCROW in t:
        sz['pilcrow'] += 0 if jelolt else t.count(PILCROW)
        if not jelolt:
            t = t.replace(PILCROW, ' ')
    t = re.sub(r'\s+', ' ', t).strip()
    if jelolt:
        t = t.replace('[ ', '[').replace(' ]', ']').replace(WJ_NYIT + ' ', WJ_NYIT).replace(' ' + WJ_ZAR, WJ_ZAR)
        t = wj_lezar(t, sz)
    return t


def wj_lezar(t, sz):
    """Minden vers onalloan zart ‹…›-et kap: a versen atnyulo \\wj (nyitas az elozo versben, vagy zaras a kovetkezoben)
    a vers elejen/vegen lezarodik. A forrasban (2026-10-17-i csomag) ilyen vers nincs (naplok/KJV_SZOVEG_meres.md);
    a ‹ › jel a forrasszovegben nem fordul elo, ezert a jeloles egyertelmu."""
    melyseg = 0
    elol = 0
    for ch in t:
        if ch == WJ_NYIT:
            melyseg += 1
        elif ch == WJ_ZAR:
            if melyseg == 0:
                elol += 1
            else:
                melyseg -= 1
    if elol or melyseg:
        sz['wj_atnyulo_lezaras'] += elol + melyseg
    return WJ_NYIT * elol + t + WJ_ZAR * melyseg


def parse_konyv(szoveg, szamlalo=None):
    """-> (versek, anomaliak). versek: OrderedDict {(fej, vers): {'nyers': str, 'elotte': nyers|None, 'utoirat': nyers|None}}"""
    sz = szamlalo if szamlalo is not None else collections.Counter()
    sz['labjegyzet'] += len(f19.RE_FN.findall(szoveg))
    szoveg = f19.RE_FN.sub('', szoveg)
    versek = collections.OrderedDict()
    anom = []
    fej = None
    vers = None
    fuggo_s1 = []  # a kovetkezo vers elotti \s1 cimsor(ok)
    for sor in szoveg.split('\n'):
        sor = sor.rstrip()
        if fej is None:
            m = re.match(E + r'([a-z]+[0-9]*)', sor)
            if m and m.group(1) in FEJLEC_JELOLOK:
                sz['fejlec_sor'] += 1
                continue
        m = re.match(E + r'c ([0-9]+)\s*$', sor)
        if m:
            if fuggo_s1:
                anom.append((fej, vers, 'cimsor_fejezethataron: ' + fuggo_s1[0][:60]))
            fej = int(m.group(1))
            vers = None
            continue
        if fej is None:
            if sor.strip():
                anom.append((None, None, 'fejezet_elotti_sor: ' + sor[:60]))
            continue
        if re.match(E + r's1( |$)', sor):
            fuggo_s1.append(sor[3:].strip())
            continue
        if sor.startswith(BS + 'd ') or sor == BS + 'd':
            vers = 0
            rec = versek.setdefault((fej, 0), {'nyers': '', 'elotte': None, 'utoirat': None})
            rec['nyers'] = (rec['nyers'] + ' ' + sor[2:].strip()).strip()
            continue
        darabok = []
        pos = 0
        for mv in f19.RE_V.finditer(sor):
            if mv.start() > pos:
                darabok.append((vers, sor[pos:mv.start()], False))
            vers = int(mv.group(1))
            if mv.group(2):
                sz['vershid'] += 1
            darabok.append((vers, '', True))
            pos = mv.end()
        darabok.append((vers, sor[pos:], False))
        for v, d, uj in darabok:
            if uj:
                rec = versek.setdefault((fej, v), {'nyers': '', 'elotte': None, 'utoirat': None})
                if fuggo_s1:
                    rec['elotte'] = ' '.join(fuggo_s1)
                    fuggo_s1 = []
                continue
            if not tisztit(d, szamlalo=collections.Counter()):
                sz['csak_jelolo_sor'] += 1 if d.strip() else 0
                # csak bekezdesjelolo (\p, \q1, \b): a tagolas szamolva, szoveg nincs
                tisztit(d, szamlalo=sz)
                continue
            if v is None:
                anom.append((fej, v, 'vers_elotti_szoveg: ' + d[:60]))
                continue
            rec = versek[(fej, v)]
            if rec['nyers']:
                sz['vers_folytatas_sor'] += 1
            rec['nyers'] = (rec['nyers'] + ' ' + d.strip()).strip()
    if fuggo_s1:
        if not versek:
            anom.append((fej, vers, 'utoirat_vers_nelkul'))
        else:
            utolso = next(reversed(versek))
            versek[utolso]['utoirat'] = ' '.join(fuggo_s1)
    return versek, anom


def olvas(zippath, konyvek=None, szamlalo=None):
    """-> ({step: versek}, anomaliak, {step: nyers usfm})"""
    konyvek = konyvek or f19.lista_konyvek()
    sz = szamlalo if szamlalo is not None else collections.Counter()
    z = zipfile.ZipFile(zippath)
    fajlok = {}
    for n in z.namelist():
        m = re.match(r'^[0-9]+-([0-9A-Z]{3})eng-kjv\.usfm$', n)
        if m:
            fajlok[m.group(1)] = n
    out, anom, nyers = {}, [], {}
    for step, usfm in konyvek:
        if usfm not in fajlok:
            raise SystemExit('hianyzo USFM-fajl: %s' % usfm)
        t = z.read(fajlok[usfm]).decode('utf-8-sig')
        nyers[step] = t
        v, a = parse_konyv(t, sz)
        out[step] = v
        anom += [(step,) + x for x in a]
    return out, anom, nyers


def sorok(adat, konyvek, szamlalo=None):
    """-> [(Igehely, Szöveg, Szöveg_jelolt, Elotte, Utoirat)] kanonikus sorrendben (fejezet, vers szerint)"""
    sz = szamlalo if szamlalo is not None else collections.Counter()
    jsz = collections.Counter()  # a Szöveg_jelolt tisztitasanak szamlaloi (csak a ‹…›-lezaras szamit)
    kiser = collections.Counter()  # az Elotte/Utoirat tisztitasanak szamlaloi (ott a \\add-jeloles is elvesz)
    out = []
    for step, _ in konyvek:
        for (f, v) in sorted(adat[step]):
            rec = adat[step][(f, v)]
            out.append(('%s.%d.%d' % (step, f, v),
                        tisztit(rec['nyers'], False, sz),
                        tisztit(rec['nyers'], True, jsz),
                        tisztit(rec['elotte'], False, kiser) if rec['elotte'] else '',
                        tisztit(rec['utoirat'], False, kiser) if rec['utoirat'] else ''))
    sz['wj_atnyulo_lezaras'] += jsz['wj_atnyulo_lezaras']
    for k, n in kiser.items():
        sz[k] += n
        sz['kiser_' + k] += n
    return out


def sha256(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


ALLAPOT = ('# ÁLLAPOT: importált, elfogadva (felhasználó, 2026-10-18). Mérés (manual, mért 2026-10-18, naplok/KJV_SZOVEG_meres.py; nem a generátor számolja; naplok/KJV_SZOVEG_meres.md): '
           'M-a: a KJV_Strongs_teljes.tsv versei ⊆ e tábla versei, a különbség pontosan a 3 címke nélküli vers (Mk 9:43, Lk 6:41, Lk 17:36; naplok/F19_hianyok.tsv); '
           '31 102 kanonikus vers + 116 zsoltárfelirat (0. vers). M-b: 362 399 Strong-szóelem, megmagyarázatlan eltérés 0 '
           '(76 összetett szó, pl. where+in = wherein, és 8 szótöredék-címke, pl. afrai|…+d: naplok/KJV_SZOVEG_szoegyezes_hiany.tsv). '
           'M-c: üres Szöveg 0, vershíd 0, a veszteség-sor számai a nyers jelölőszámokkal egyeznek.')


def fejlecsorok(zsha, ts, sz):
    vesz = ('a Strong-címke (\\w strong=) %d; lábjegyzet (\\f) %d; bekezdés/költői tagolás \\p %d, \\q1 %d, \\b %d; '
            '\\nd %d, \\tl %d jelölés (a szöveg marad); a Szöveg-ből a \\wj %d (a Szöveg_jelolt-ban ‹…›), a ¶ %d (a Szöveg_jelolt megőrzi) '
            'és a \\add-jelölés %d (a Szöveg_jelolt-ban [..]; ebből az Elotte/Utoirat-ban %d, ott a jelölés elvész); '
            'könyvfejléc-sor (\\id \\h \\toc \\mt) %d; versen átnyúló ‹…› lezárása %d. '
            'Nem veszteség, de jelölendő: az 1Jn 2:23 forrásbeli „[but]” szögletes zárójele a forrás szerint marad (a Szöveg-ben is), '
            'a Szöveg_jelolt-ban ezért egymásba ágyazott: „[[but] … also]” (DT-F118e (3))' % (
                sz['w'], sz['labjegyzet'], sz['p'], sz['q1'], sz['b'], sz['nd'], sz['tl'], sz['wj'], sz['pilcrow'], sz['add'],
                sz['kiser_add'], sz['fejlec_sor'], sz['wj_atnyulo_lezaras']))
    return ['# GENERÁLT: eszkozok/kjv_szoveg_import.py — kézzel nem szerkesztendő.',
            '# proveniencia: scope=KJV teljes (66 kanonikus könyv, angol számozás) | forras=%s sha256=%s | ts=%s' % (FORRAS_URL, zsha, ts),
            '# licenc: közkincs (KJV; eBible copr.htm: „Public Domain”, „You may copy the King James Version of the Holy Bible freely.”); '
            'kereskedelmi: feltételesen (UK Korona-szabadalom); share_alike: nem; Strong-címkét nem tartalmaz (DT-F118a; a címkeréteg: KJV_Strongs_teljes.tsv, DT126)',
            ALLAPOT,
            '# veszteség (DT-F107d (2); mit dob el az importáló): ' + vesz]


class AdatElteres(SystemExit):
    pass


RE_TS = re.compile(r'(\| ts=)\S+')


def _bont(tartalom):
    """-> (fejlecsorok, adatsorok): a '#' kezdetu sorok es a tobbi (oszlopfejlec + adatsorok), sorrendben."""
    sorok = tartalom.split('\n')
    if sorok and sorok[-1] == '':
        sorok = sorok[:-1]
    return [s for s in sorok if s.startswith('#')], [s for s in sorok if not s.startswith('#')]


def iras_dontes(regi, uj, felulir=False):
    """Iras elotti osszevetes (CLAUDE.md, TSV-olvasas; minta: eszkozok/igazolas_migracio.py).
    regi: a meglevo tabla tartalma (None, ha nincs), uj: az uj tartalom.
    -> ('ir', uzenet) vagy ('valtozatlan', uzenet); eltero adatsornal AdatElteres, hacsak felulir=True.
    Az adatsorok (oszlopfejlec + versek) bajtra osszevetve; a fejlecsorok a proveniencia ts-e nelkul
    (a ts naponta valtozik): ha csak a ts ter el, a meglevo fajl marad (stabil tartalom)."""
    if regi is None:
        return 'ir', 'új tábla'
    rf, ra = _bont(regi)
    uf, ua = _bont(uj)
    if ra != ua:
        elter = [i for i, (x, y) in enumerate(zip(ra, ua)) if x != y]
        leiras = 'adatsor eltér: régi %d, új %d sor; az első eltérő sorindexek: %s' % (len(ra), len(ua), elter[:5])
        if not felulir:
            raise AdatElteres('⛔ ' + leiras + ' -- a meglévő tábla nem íródik felül; szándékos felülírás: --felulir')
        return 'ir', 'felülírás (--felulir): ' + leiras
    fej_elter = [i for i, (x, y) in enumerate(zip(rf, uf)) if RE_TS.sub(r'\1', x) != RE_TS.sub(r'\1', y)]
    if len(rf) != len(uf):
        fej_elter.append('sorszam')
    if not fej_elter:
        return 'valtozatlan', 'az adatsorok bájtra azonosak, a fejléc csak a ts-ben tér el (vagy abban sem): a meglévő tábla marad'
    return 'ir', 'az adatsorok bájtra azonosak; a fejlécsorok közül eltér: %s (a ts-en kívül)' % fej_elter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--munka', required=True)
    ap.add_argument('--kimenet', default=os.path.join(REPO, 'konkordancia', 'KJV_teljes_szoveg.tsv'))
    ap.add_argument('--felulir', action='store_true', help='eltérő adatsorok esetén is felülírja a meglévő táblát (szándékos felülírás)')
    a = ap.parse_args()
    zp = os.path.join(a.munka, 'kjv.zip')
    zsha = sha256(zp)
    if zsha != VART_SHA256:
        raise SystemExit('a kjv.zip sha256-ja eltér: %s (várt: %s) -- ⛔ megállás (brief 3. pont)' % (zsha, VART_SHA256))
    konyvek = f19.lista_konyvek()
    sz = collections.Counter()
    adat, anom, _ = olvas(zp, konyvek, sz)
    if anom:
        for x in anom[:20]:
            print('ANOMALIA', x)
        raise SystemExit('parse-anomália: %d' % len(anom))
    rs = sorok(adat, konyvek, sz)
    ts = datetime.date.today().isoformat()
    fej = fejlecsorok(zsha, ts, sz)
    sor = fej + ['\t'.join(['Igehely', 'Szöveg', 'Szöveg_jelolt', 'Elotte', 'Utoirat'])] + ['\t'.join(r) for r in rs]
    uj = '\n'.join(sor) + '\n'
    regi = open(a.kimenet, 'rb').read().decode('utf-8') if os.path.exists(a.kimenet) else None
    dontes, uzenet = iras_dontes(regi, uj, a.felulir)
    print('összevetés:', uzenet)
    if dontes == 'ir':
        with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(uj)
    print('sorok=%d; ures Szöveg=%d; Elotte=%d; Utoirat=%d; vershid=%d; folytatas-sor=%d' % (
        len(rs), sum(1 for r in rs if not r[1]), sum(1 for r in rs if r[3]), sum(1 for r in rs if r[4]), sz['vershid'], sz['vers_folytatas_sor']))
    print('kimenet:', a.kimenet)


if __name__ == '__main__':
    main()
