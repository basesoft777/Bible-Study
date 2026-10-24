#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F96.1 — a modernizált Károli-réteg helyesírási lépcsője (DT128, DT-F96e, DT-F96f).

Determinisztikus, API és LLM nélkül; Hunspell nélkül (DT301: csak fejlesztési mérce, a kiadott
alakba nem kerül belőle semmi). Csak olvas: `konkordancia/Karoli_1908.tsv`,
`adat/szoto/karoli_szotari_alak.tsv` (a #94 kiadott táblája). A tokenizálás a
`eszkozok/karoli_strong/tokenek.py` `tokenizal` függvénye: a token sorszáma ugyanaz, amelyen a
#22 Károli–Strong párosítás `hu_sorszam`-a áll, így a Strong token-kulcson illeszthető; a réteg
Strongot nem tárol és nem ellenőriz (DT-F96f).

Szabályok (a sorrend számít; minden szabály forrása a `szabaly_forras` oszlopban):

  karakter      cz → c, czcz → cc, nyny → nny, lyly → lly, gygy → ggy, tyty → tty, szsz → ssz,
                zszs → zzs, cscs → ccs (manual: általános helyesírás-történet; a #94-ben is manual)
  neki          néki → neki (DT128 példája)
  szoto_94      a #94 `szotari_alak_mai` helyesírási eltérése (ékezet, e/ö, kettőzés) az alak elejére
                vihető (setétség → sötétség, kivül → kívül, vajjon → vajon); a lemmaváltás
                (e → ez, férfiú → férfi, leány → lány, mostan → most) NEM (DT-F96e a)
  kivetel       a #94 tábla megfigyelt hibái (N-F96b): kivűl → kívül (a tábla: kivül), a gyűl- és
                dűl-család és a jóhiszeműleg változatlan (a tábla mai alakja ott hibás: gyül, dül)
  rea           reá- → rá- (DT-F96e b)
  szotag        dícs- → dics-, paizs → pajzs (manual; a mintán mérendő)
  nevmas        „a” + ki-/mely-/mi- és a vonatkozó határozószók (mint, mikor, hol, míg, hová …)
                különírt alakja egybe: a kik → akik (DT128, N-F94f). Az „a” token kieső
                (`kieso=osszevonva`), az összevont alak a névmás tokenjén áll. A puszta „a mi”
                birtokos (a mi Istenünk) változatlan; ahol a heurisztika nem dönt, `bizonytalan`
                (változatlan, a mintában a felhasználó dönt)

Nem e lépcső dolga (a .2-ben jön): igealak (teremté, monda, -ván/-vén), *vala*, *lőn*. A *-jék*
felszólító E/3 (DT-F96e d) és a *-jok/-jök* birtokos T/3 itt nem változik: a mintában
alternatívaként szerepel, a felhasználó dönt.

Ír (generált, kézzel nem szerkeszthető):
  adat/karoli_modern/helyesiras_alakok.tsv   alakonként a változó alakok (alak → modern alak)
  adat/karoli_modern/helyesiras_tokenek.tsv  a változó, kieső vagy bizonytalan tokenek, token-kulccsal
  adat/karoli_modern/helyesiras_minta.tsv    rögzített magú minta a felhasználói ellenőrzésre (--minta)

Önellenőrzés (K2): a modern versszöveg újratokenizálva pontosan a nem kieső tokenek modern
alakjait adja, sorrendben; a nem-betű váz (írásjel, szóköz) az összevonások szóközén kívül
változatlan. Eltérésnél a szkript megáll, és nem ír.

Használat:
    python eszkozok/karoli_modern/helyesiras.py
    python eszkozok/karoli_modern/helyesiras.py --minta          (a minta újragenerálása is)
    python eszkozok/karoli_modern/helyesiras.py --kimenet <könyvtár>   (próba a repón kívülre)
"""

import argparse
import collections
import hashlib
import os
import random
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_modern'))
import tokenek  # noqa: E402
import fedettseg  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

KAROLI = fedettseg.KAROLI
SZOTARI = fedettseg.SZOTARI
KI_DIR = os.path.join('adat', 'karoli_modern')
MAG = 20261024
SZKRIPT = 'eszkozok/karoli_modern/helyesiras.py'

FORRAS = {
    'karakter': 'manual (helyesírás-történet; #94: manual)',
    'neki': 'DT128',
    'szoto_94': '#94 adat/szoto/karoli_szotari_alak.tsv szotari_alak_mai',
    'kivetel': 'N-F96b (manual)',
    'rea': 'DT-F96e b',
    'szotag': 'manual',
    'nevmas': 'DT128, N-F94f',
}

# N-F96b: a #94 tábla hibás mai alakjai. Lemma → None: a helyesírási átvitel nem fut (változatlan);
# lemma → alak: a mai szótári alak helyett ez (az alak elejére vive).
KIVETEL_LEMMA = {
    'gyűl': None, 'egybegyűl': None, 'összegyűl': None,
    'dűl': None, 'ledűle': None, 'jóhiszeműleg': None,
    'kivűl': 'kívül',
}
SZOTAG = [(re.compile(r'dícs'), 'dics'), (re.compile(r'Dícs'), 'Dics'),
          (re.compile(r'^paizs'), 'pajzs'), (re.compile(r'^Paizs'), 'Pajzs'),
          (re.compile(r'^rézpaizs'), 'rézpajzs')]

NEVMAS = {
    'ki': re.compile(r'^ki(t|k|ket|nek|knek|ben|kben|ből|kből|re|kre|ről|kről|hez|khez|től|ktől|vel|kkel|'
                     r'ért|kért|n|ken|nél|knél|é|ké)?$'),
    'mely': re.compile(r'^mely(ek)?(et|nek|ben|ből|be|re|ről|hez|től|lyel|llyel|kel|ért|en|nél|ig)?$'),
    'mi': re.compile(r'^mi(t|k|ket|nek|ben|ből|re|ről|hez|től|vel|ért|n|kre|kről|kben|je|jét)?$'),
    'hatarozo': re.compile(r'^(mint|mikor|hol|míg|mig|hová|hova|honnan|honnét|milyen|milyenek|miképen|'
                           r'miképpen|miként|merre|mióta|meddig|mennyi|mennyire|mennyit|mennyiben|hogy|'
                           r'minő|minemű)$'),
}
SZEMELYES_NK = {
    'nékünk', 'nekünk', 'velünk', 'tőlünk', 'hozzánk', 'bennünk', 'belőlünk', 'rólunk', 'ránk', 'reánk',
    'nálunk', 'minket', 'értünk', 'előttünk', 'közöttünk', 'mellettünk', 'alattunk', 'felettünk',
    'fölöttünk', 'mögöttünk', 'miénk', 'mienk', 'utánunk', 'ellenünk', 'körülünk', 'körűlünk',
    'általunk', 'magunk', 'magunkat', 'magunknak', 'mindnyájan', 'mindnyájunk', 'mindnyájunkat',
}
NK = re.compile(r'(nk|nkat|nket|nknek|nkhoz|nkhez|nkhöz|nkban|nkben|nkból|nkből|nkra|nkre|nkról|nkről|'
                r'nktól|nktől|nkkal|nkkel|nkért|nkon|nken|nkön|nké|nkig|nkká|nkké)$')

BETU = re.compile(r'[^\W_]+', re.UNICODE)


def sha(ut):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, ut), 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def nagy(minta, uj):
    return uj[:1].upper() + uj[1:] if minta[:1].isupper() else uj


def alak_modern(alak, sor, kis_szavak):
    """Egy alak helyesírási modern alakja (szövegkörnyezet nélkül): (alak, [szabályok])."""
    szab = []
    uj = alak
    kis = alak.lower()
    if kis == 'néki':
        return nagy(alak, 'neki'), ['neki']
    lemma = sor['szotari_alak'] if sor else ''
    mai = sor['szotari_alak_mai'] if sor else ''
    atvitt = False
    if sor and lemma in KIVETEL_LEMMA:
        cel = KIVETEL_LEMMA[lemma]
        if cel is not None:
            u2, mod = fedettseg.helyesiras_atvitel(alak, lemma, cel)
            if u2 and u2 != alak:
                uj, atvitt = u2, True
                szab.append('kivetel')
        else:
            szab.append('kivetel')
            atvitt = True  # szándékosan változatlan (a karakterszabály sem érinti ezeket)
    elif sor and lemma != mai and fedettseg.vaz(lemma) == fedettseg.vaz(mai):
        u2, mod = fedettseg.helyesiras_atvitel(alak, lemma, mai)
        if u2 and u2 != alak:
            uj, atvitt = u2, True
            szab.append('karakter' if mod == 'karakter' else 'szoto_94')
    if not atvitt:
        k = fedettseg.karakter_szabaly(alak)
        if k != alak:
            uj = k
            szab.append('karakter')
    if uj.lower().startswith('reá'):
        uj = uj[:1] + 'á' + uj[3:] if uj[:1] in 'rR' else uj
        szab.append('rea')
    for rx, cserel in SZOTAG:
        u2 = rx.sub(cserel, uj)
        if u2 != uj:
            uj = u2
            szab.append('szotag')
    if szab == ['kivetel'] and uj == alak:
        return alak, ['kivetel']
    return uj, szab


def tamasz(modern, szab, kis_szavak):
    if 'szoto_94' in szab or 'kivetel' in szab:
        return 'szoto_94' if 'szoto_94' in szab else 'manual'
    if modern.lower() in kis_szavak:
        return 'korpusz'
    return 'modell_ellenorizetlen'


def nevmas_csalad(kis):
    for csal, rx in NEVMAS.items():
        if rx.match(kis):
            return csal
    return None


def vers_feldolgoz(igehely, szoveg, alakszotar):
    """Egy vers: tokenlista [(sorszam, alak1908, modern, kieso, szabaly, bizonytalan)], modern szöveg."""
    spans = [(m.start(), m.end(), m.group(0)) for m in BETU.finditer(szoveg)]
    sorok = []
    for i, (a, b, t) in enumerate(spans):
        m, szab = alakszotar[t]
        sorok.append([i + 1, t, m, '', '+'.join(szab), ''])
    torles = set()  # a kieső „a” span-indexe
    for i in range(len(spans) - 1):
        a, b, t = spans[i]
        if t not in ('a', 'A'):
            continue
        a2, b2, t2 = spans[i + 1]
        if szoveg[b:a2] != ' ':
            continue
        kov_mod = sorok[i + 1][2]
        csal = nevmas_csalad(t2.lower())
        if csal is None:
            continue
        if csal == 'mi' and t2.lower() == 'mi':
            if i + 2 < len(spans) and szoveg[b2:spans[i + 2][0]] == ' ':
                w = spans[i + 2][2]
                wk = w.lower()
                if wk in SZEMELYES_NK or w[:1].isupper():
                    sorok[i + 1][5] = 'mi_birtokos_vagy_vonatkozo'
                    continue
                if NK.search(wk):
                    sorok[i + 1][5] = ''
                    sorok[i + 1][4] = (sorok[i + 1][4] + '+' if sorok[i + 1][4] else '') + 'mi_birtokos_marad'
                    continue
            else:
                sorok[i + 1][5] = 'mi_irasjel_utan'
                continue
        uj = (t[:1] + kov_mod.lower()) if t == 'A' else ('a' + kov_mod.lower() if kov_mod[:1].islower() else None)
        if uj is None:  # „a Ki…” nagybetűvel a vers közepén: nem vonjuk össze
            sorok[i + 1][5] = 'nagybetu'
            continue
        sorok[i][2] = ''
        sorok[i][3] = 'osszevonva'
        sorok[i][4] = 'nevmas'
        sorok[i + 1][2] = uj
        sorok[i + 1][4] = (sorok[i + 1][4] + '+' if sorok[i + 1][4] else '') + 'nevmas:' + csal
        torles.add(i)
    # modern szöveg
    ki = []
    poz = 0
    for i, (a, b, t) in enumerate(spans):
        ki.append(szoveg[poz:a])
        if i in torles:
            poz = spans[i + 1][0]  # az „a ” (betű + egy szóköz) kiesik
            continue
        ki.append(sorok[i][2])
        poz = b
    ki.append(szoveg[poz:])
    modern = ''.join(ki)
    # K2 önellenőrzés
    vart = [s[2] for s in sorok if s[3] != 'osszevonva']
    if tokenek.tokenizal(modern) != vart:
        raise SystemExit('K2 hiba (tokenek): %s' % igehely)
    vaz_e = BETU.sub('', szoveg)
    vaz_m = BETU.sub('', modern)
    if len(vaz_e) - len(vaz_m) != len(torles) or vaz_m.replace(' ', '') != vaz_e.replace(' ', ''):
        raise SystemExit('K2 hiba (írásjel-váz): %s' % igehely)
    return sorok, modern


def jek_alt(alak, sor, kis_szavak):
    """-jék felszólító E/3 (ik-ige) → -jon/-jen/-jön alternatíva (DT-F96e d); None, ha nem ez."""
    if not sor or sor['regies_jegy'] or not sor['szotari_alak'].endswith('ik'):
        return None
    k = alak.lower()
    if not k.endswith('ék') or len(k) < 5:
        return None
    to = sor['szotari_alak'][:-2]
    if to in kis_szavak:  # a tő önálló szó (megismer): tárgyas T/3, nem ik-ige
        return None
    elo = k[:-2]
    if not (elo.endswith('j') or (len(elo) > 1 and elo[-1] == elo[-2]) or elo.endswith(('gy', 'ssz', 'zz'))):
        return None
    mgh = [c for c in elo if c in 'aáeéiíoóöőuúüű']
    v = mgh[-1] if mgh else 'e'
    if mgh and all(c in 'ií' for c in mgh):
        veg = 'on'  # csak i/í: mély hangrendű ige (iszik → igyon, hív → hívjon)
    else:
        veg = 'on' if v in 'aáoóuú' else ('ön' if v in 'öőüű' else 'en')
    return alak[:-2] + veg


JOK_KIZAR = {'tolvajok', 'bajok', 'tutajokra', 'tutajokon'}  # többes szám, nem birtokos T/3
JOK = re.compile(r'j(o|ö)k(nak|nek|at|et|ot|öt|ban|ben|ba|be|ból|ből|ra|re|ról|ről|hoz|hez|höz|tól|től|kal|kel|ért|on|en|ön|ig)?$')


def jok_alt(alak):
    if alak.lower() in JOK_KIZAR:
        return None
    m = JOK.search(alak)
    if not m:
        return None
    return alak[:m.start()] + 'j' + ('u' if m.group(1) == 'o' else 'ü') + 'k' + (m.group(2) or '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--minta', action='store_true')
    ap.add_argument('--kimenet', default=None, help='próba-kimenet könyvtára (a repón kívül)')
    a = ap.parse_args()
    ki_dir = a.kimenet or os.path.join(ROOT, KI_DIR)
    tabla = fedettseg.tabla_beolvas()
    versek = []
    with open(os.path.join(ROOT, KAROLI), encoding='utf-8') as f:
        next(f)
        for l in f:
            m = l.rstrip('\n').split('\t')
            if len(m) >= 2:
                versek.append((m[0], m[1]))
    gy = collections.Counter(t for _, sz in versek for t in tokenek.tokenizal(sz))
    kis_szavak = set(t.lower() for t in gy)
    alakszotar = {}
    for alak in gy:
        alakszotar[alak] = alak_modern(alak, fedettseg.tablasor(tabla, alak), kis_szavak)

    tok_ki = []
    vers_ki = {}
    szab_tok = collections.Counter()
    bizonytalan = collections.Counter()
    for igehely, sz in versek:
        sorok, modern = vers_feldolgoz(igehely, sz, alakszotar)
        vers_ki[igehely] = (sz, modern, sorok)
        for s in sorok:
            if s[1] != s[2] or s[3] or s[5]:
                tok_ki.append([igehely, str(s[0]), s[1], s[2], s[3], s[4], s[5]])
                for r in s[4].split('+'):
                    if r and s[1] != s[2]:
                        szab_tok[r.split(':')[0] if not r.startswith('nevmas:') else r] += 1
                if s[5]:
                    bizonytalan[s[5]] += 1

    tokszam = sum(gy.values())
    valt_tok = sum(1 for r in tok_ki if r[2] != r[3])
    kieso = sum(1 for r in tok_ki if r[4])
    valt_vers = sum(1 for v in vers_ki.values() if v[0] != v[1])
    hk = ('%s (sha256:%s) + %s (sha256:%s) + %s (sha256:%s)'
          % (KAROLI, sha(KAROLI)[:12], SZOTARI, sha(SZOTARI)[:12], SZKRIPT, sha(SZKRIPT)[:12]))
    fejlec = ('# GENERÁLT: %s (F96.1) — kézzel nem szerkeszthető; a javítás a szabályban vagy a kivételtáblában '
              '| forras=%s | tokenizálás: eszkozok/karoli_strong/tokenek.py tokenizal (a #22 hu_sorszam-a; '
              'Strong token-kulcson illeszthető, DT-F96f) | a helyesírási lépcső (.1), az igealak (.2) nélkül; '
              'Hunspell nem futott (DT301), a tamasz=modell_ellenorizetlen a felhasználói mintán mérendő\n'
              % (SZKRIPT, hk))

    os.makedirs(ki_dir, exist_ok=True)
    alak_sorok = []
    for alak in sorted(gy):
        m, szab = alakszotar[alak]
        if m != alak:
            alak_sorok.append([alak, str(gy[alak]), m, '+'.join(szab),
                               '; '.join(FORRAS[s] for s in szab), tamasz(m, szab, kis_szavak)])
    with open(os.path.join(ki_dir, 'helyesiras_alakok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=a szövegkörnyezet nélkül változó alakok (%d)\n' % len(alak_sorok)))
        f.write('\t'.join(['alak', 'gyakorisag', 'alak_modern', 'szabaly', 'szabaly_forras', 'tamasz']) + '\n')
        for s in alak_sorok:
            f.write('\t'.join(s) + '\n')
    with open(os.path.join(ki_dir, 'helyesiras_tokenek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=a változó, kieső vagy bizonytalan tokenek (%d) a %d tokenből\n'
                               % (len(tok_ki), tokszam)))
        f.write('\t'.join(['igehely', 'sorszam', 'alak_1908', 'alak_modern', 'kieso', 'szabaly', 'bizonytalan']) + '\n')
        for s in tok_ki:
            f.write('\t'.join(s) + '\n')

    print('versek: %d, tokenek: %d; változó vers: %d; változó token: %d; kieső (összevont „a”): %d'
          % (len(versek), tokszam, valt_vers, valt_tok, kieso))
    print('változó alak (szövegkörnyezet nélkül): %d; tamasz: %s'
          % (len(alak_sorok), dict(collections.Counter(s[5] for s in alak_sorok))))
    print('szabályonként (token): %s' % dict(sorted(szab_tok.items(), key=lambda x: -x[1])))
    print('bizonytalan (változatlan, mintába): %s' % dict(bizonytalan))
    jek = collections.Counter()
    jok = collections.Counter()
    for igehely, (sz, modern, sorok) in vers_ki.items():
        for s in sorok:
            if jek_alt(s[1], fedettseg.tablasor(tabla, s[1]), kis_szavak):
                jek[s[1]] += 1
            if jok_alt(s[2] or s[1]):
                jok[s[1]] += 1
    print('-jék felszólító E/3 (ik-ige, DT-F96e d): %d alak, %d token' % (len(jek), sum(jek.values())))
    print('-jok/-jök (birtokos T/3): %d alak, %d token' % (len(jok), sum(jok.values())))
    print('bemenet: %s' % hk)

    if a.minta:
        minta(vers_ki, tabla, kis_szavak, ki_dir, fejlec)


RETEGEK = [  # (réteg, darab)
    ('karakter', 14), ('neki', 8), ('szoto_94', 14), ('rea', 8), ('nevmas:ki', 10), ('nevmas:mely', 10),
    ('nevmas:mi', 8), ('mi_birtokos_marad', 4), ('bizonytalan', 4), ('nevmas:hatarozo', 8),
    ('kivetel_szotag', 4), ('jek', 8), ('jok', 6), ('valtozatlan', 6),
]


def minta(vers_ki, tabla, kis_szavak, ki_dir, fejlec):
    rnd = random.Random(MAG)
    jelolt = collections.defaultdict(list)
    for igehely, (sz, modern, sorok) in vers_ki.items():
        rek = set()
        for s in sorok:
            for r in s[4].split('+'):
                if not r:
                    continue
                if r in ('kivetel', 'szotag'):
                    rek.add('kivetel_szotag')
                elif r.startswith('nevmas:') or r in ('karakter', 'neki', 'szoto_94', 'rea', 'mi_birtokos_marad'):
                    rek.add(r)
            if s[5]:
                rek.add('bizonytalan')
            if jek_alt(s[1], fedettseg.tablasor(tabla, s[1]), kis_szavak):
                rek.add('jek')
            if jok_alt(s[2] or s[1]):
                rek.add('jok')
        if sz == modern and not rek:
            rek.add('valtozatlan')
        for r in rek:
            jelolt[r].append(igehely)
    valasztott = []
    hasznalt = set()
    for reteg, db in RETEGEK:
        l = sorted(jelolt[reteg])
        rnd.shuffle(l)
        n = 0
        for ih in l:
            if n >= db:
                break
            if ih in hasznalt:
                continue
            hasznalt.add(ih)
            valasztott.append((reteg, ih))
            n += 1
    sorok_ki = []
    for i, (reteg, ih) in enumerate(valasztott, 1):
        sz, modern, sorok = vers_ki[ih]
        valt = []
        alt = modern
        alt_valt = []
        for s in sorok:
            if s[1] != s[2] and not s[3]:
                valt.append('%d:%s→%s' % (s[0], s[1], s[2]))
            elif s[3]:
                valt.append('%d:%s→(összevonva)' % (s[0], s[1]))
            if s[5]:
                valt.append('%d:%s?(%s)' % (s[0], s[1], s[5]))
            if 'mi_birtokos_marad' in s[4]:
                valt.append('%d:%s=(birtokos, marad)' % (s[0], s[1]))
            if s[4] == 'kivetel' and s[1] == s[2]:
                valt.append('%d:%s=(N-F96b kivétel, marad)' % (s[0], s[1]))
            if reteg in ('jek', 'jok'):
                modern_alak = s[2] or s[1]
                if reteg == 'jek':
                    cel = jek_alt(s[1], fedettseg.tablasor(tabla, s[1]), kis_szavak)
                    cel = (modern_alak[:-2] + cel[-2:]) if cel else None
                else:
                    cel = jok_alt(modern_alak)
                if cel:
                    alt_valt.append((modern_alak, cel))
        if alt_valt:
            for regi, uj in alt_valt:
                alt = re.sub(r'(?<![^\W_])' + re.escape(regi) + r'(?![^\W_])', uj, alt, count=1)
        else:
            alt = ''
        sorok_ki.append(['M%03d' % i, reteg, ih, sz, modern, '; '.join(valt), alt, '', ''])
    with open(os.path.join(ki_dir, 'helyesiras_minta.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=rögzített magú (%d) rétegzett minta, %d vers; az ellenorzes és a '
                               'megjegyzes oszlopot a felhasználó tölti (jó / hibás / A / B), a modell nem\n'
                               % (MAG, len(sorok_ki))))
        f.write('\t'.join(['minta_id', 'reteg', 'igehely', 'szoveg_1908', 'szoveg_modern', 'valtozasok',
                           'alternativa', 'ellenorzes', 'megjegyzes']) + '\n')
        for s in sorok_ki:
            f.write('\t'.join(s) + '\n')
    print('minta: %d vers; rétegenként: %s' % (len(sorok_ki), dict(collections.Counter(s[1] for s in sorok_ki))))


if __name__ == '__main__':
    main()
