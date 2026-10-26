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
  neki          néki → neki (DT128 példája) és a nék- család: néked, nékem, nékik, nékünk, néktek →
                neked, nekem, nekik, nekünk, nektek (DT-F96j); a Nékó, Nékhusta (név) és a nékie nem
  szoto_94      a #94 `szotari_alak_mai` helyesírási eltérése (ékezet, e/ö, kettőzés) az alak elejére
                vihető (setétség → sötétség, kivül → kívül, vajjon → vajon); a lemmaváltás
                (e → ez, férfiú → férfi, leány → lány, mostan → most) NEM (DT-F96e a)
  kivetel       a #94 tábla megfigyelt hibái (N-F96b): kivűl → kívül (a tábla: kivül), a gyűl- és
                dűl-család és a jóhiszeműleg változatlan (a tábla mai alakja ott hibás: gyül, dül)
  rea           reá- → rá- (DT-F96e b)
  szotag        dícs- → dics-, paizs → pajzs (manual; a mintán mérendő)
  jok           a j-s birtokos T/3 -jok/-jök → -juk/-jük (atyjok → atyjuk, rájok → rájuk; DT-F96g); a
                többes számú tolvajok, bajok, tutajok- kizárva; a j nélküli (kezöket, szívök) marad
  nevmas        „a” + ki-/mely-/mi- és a vonatkozó határozószók (mint, mikor, hol, míg, hová …)
                különírt alakja egybe: a kik → akik (DT128, N-F94f). Az „a” token kieső
                (`kieso=osszevonva`), az összevont alak a névmás tokenjén áll.
  ami           a puszta „a mi” (DT-F96i): birtokos, változatlan, ha utána (B1) vagy a második szón
                (B2) -nk birtokos főnév áll (a mi Istenünk, a mi mindennapi kenyerünket); különben
                vonatkozó (→ ami), ha előtte írásjel (V1), mindazt/mindent/semmit (V2) vagy ige (V3),
                vagy utána ige (V4) áll; támpont nélkül a régi döntés (a puszta „a mi” → ami), illetve
                a nagybetűs / személyes névmás utáni eset `bizonytalan` (változatlan, a felhasználó dönt)

Nem e lépcső dolga (a .2-ben jön): igealak (teremté, monda, -ván/-vén), *vala*, *lőn*. A *-jék*
felszólító E/3 nem változik (DT-F96e d); a mintában alternatívaként szerepel.

Ír (generált, kézzel nem szerkeszthető):
  adat/karoli_modern/helyesiras_alakok.tsv   alakonként a változó alakok (alak → modern alak)
  adat/karoli_modern/helyesiras_tokenek.tsv  a változó, kieső vagy bizonytalan tokenek, token-kulccsal
  adat/karoli_modern/helyesiras_minta.tsv    rögzített magú minta a felhasználói ellenőrzésre (--minta;
                                             --minta-frissit: a kiválasztás és a kitöltött oszlopok maradnak)
  adat/karoli_modern/helyesiras_ami_proba.tsv, helyesiras_ami_ellenorzes.tsv   a DT-F96i mérése (--ami-proba)

Önellenőrzés (K2): a modern versszöveg újratokenizálva pontosan a nem kieső tokenek modern
alakjait adja, sorrendben; a nem-betű váz (írásjel, szóköz) az összevonások szóközén kívül
változatlan. Eltérésnél a szkript megáll, és nem ír.

Használat:
    python eszkozok/karoli_modern/helyesiras.py
    python eszkozok/karoli_modern/helyesiras.py --minta-frissit  (a meglévő minta újraszámolása is)
    python eszkozok/karoli_modern/helyesiras.py --minta          (új minta; a DT-F96i óta más verseket ad)
    python eszkozok/karoli_modern/helyesiras.py --kimenet <könyvtár>   (próba a repón kívülre)
    python eszkozok/karoli_modern/helyesiras.py --ami-proba     (DT-F96i mérése és ellenőrző fájlja)
"""

import argparse
import collections
import datetime
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
    'neki': 'DT128, DT-F96j',
    'szoto_94': '#94 adat/szoto/karoli_szotari_alak.tsv szotari_alak_mai',
    'kivetel': 'N-F96b (manual)',
    'rea': 'DT-F96e b',
    'szotag': 'manual',
    'nevmas': 'DT128, N-F94f',
    'jok': 'DT-F96g',
}

# N-F96b: a #94 tábla hibás mai alakjai. Lemma → None: a helyesírási átvitel nem fut (változatlan);
# lemma → alak: a mai szótári alak helyett ez (az alak elejére vive).
KIVETEL_LEMMA = {
    'gyűl': None, 'egybegyűl': None, 'összegyűl': None,
    'dűl': None, 'ledűle': None, 'jóhiszeműleg': None,
    'kivűl': 'kívül',
}
NEK_CSALAD = {'néki', 'néked', 'nékem', 'nékik', 'nékünk', 'néktek'}
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

# DT-F96i (a felhasználó döntése, 2026-10-24): a puszta „a mi” birtokos vagy vonatkozó támpontjai.
# A *-nk* birtokos a nagybetűs főnéven is (a mi Istenünk, Urunk), minden esetraggal: a NK mintából
# hiányzik a -nknak, -nknél, -nkba, -nkéi (Urunknak, Istenünknél, ruhánkba), ezért ez külön minta; a
# -nk az atyánkfia-összetételben is; a ragos személyes névmás (nékünk, velünk) nem birtokos főnév, a magunk-család viszont az (a mi magunk).
NK_PROBA = re.compile(r'nk(nak|nek|at|et|ot|öt|hoz|hez|höz|ban|ben|ba|be|ból|ből|ra|re|ról|ről|tól|től|kal|kel|'
                      r'ért|on|en|ön|é|éi|ig|ká|ké|nál|nél)?$|nkfi[^\W_]*$')  # atyánkfiai: a -nk az összetételben
MAGUNK = {'magunk', 'magunkat', 'magunknak'}
AMI_ELOTTE = {'mindazt', 'mindent', 'semmit'}


def ami_proba_keszit(tabla, igei):
    """A DT-F96i döntése: (spans, szoveg, i) → ('birtokos'|'vonatkozo'|None, kritérium).

    Sorrend (az első illeszkedő dönt): B1 a következő szó -nk birtokos főnév; B2 a második szó az,
    szóközzel, és az első nem ige (a mi Jézus Krisztusunkban); V1 előtte vessző, pontosvessző vagy
    kettőspont; V2 előtte mindazt/mindent/semmit; V3 előtte ige; V4 utána ige. A melléknév-támpontot
    a repó adata nem hordozza (szófaj nincs), ezért nem fut. Az ige: a #94 tábla regies_jegy-e vagy
    a fedettseg.igei_tovek próbája a szótári alakon."""

    def ige(w):
        s = fedettseg.tablasor(tabla, w)
        return bool(s) and bool(s['regies_jegy'] or igei(s['szotari_alak']))

    def nk_fonev(w):
        wk = w.lower()
        return wk in MAGUNK or (wk not in SZEMELYES_NK and bool(NK_PROBA.search(wk)))

    def dont(spans, szoveg, i):
        b2 = spans[i + 1][1]
        k1 = spans[i + 2] if i + 2 < len(spans) and szoveg[b2:spans[i + 2][0]] == ' ' else None
        k2 = (spans[i + 3] if k1 and i + 3 < len(spans) and szoveg[k1[1]:spans[i + 3][0]] == ' '
              else None)
        if k1 and nk_fonev(k1[2]):
            return 'birtokos', 'B1_nk_utana'
        if k2 and nk_fonev(k2[2]) and not ige(k1[2]):
            return 'birtokos', 'B2_nk_masodik'
        elv = szoveg[spans[i - 1][1]:spans[i][0]] if i > 0 else ''
        if re.search(r'[,;:]', elv):
            return 'vonatkozo', 'V1_irasjel_elotte'
        if i > 0 and spans[i - 1][2].lower() in AMI_ELOTTE:
            return 'vonatkozo', 'V2_mindazt_elotte'
        if i > 0 and elv == ' ' and ige(spans[i - 1][2]):
            return 'vonatkozo', 'V3_ige_elotte'
        if k1 and ige(k1[2]):
            return 'vonatkozo', 'V4_ige_utana'
        return None, ''
    return dont


def sha(ut):
    h = hashlib.sha256()
    with open(os.path.join(ROOT, ut), 'rb') as f:
        h.update(f.read())
    return h.hexdigest()


def nagy(minta, uj):
    return uj[:1].upper() + uj[1:] if minta[:1].isupper() else uj


# A karakterszabály hibái (napló 4.1.5, a Hunspell-mérés cáfolatai; ELT-2): összetételi határon a kettős betű
# nem egyszerűsödik (kemény + nyakú), a paizs → pajzs a zszs → zzs elé tartozik, a strucz mai alakja strucc.
ALAK_KIVETEL = {
    'keménynyakú': 'keménynyakú', 'keménynyakúak': 'keménynyakúak',
    'paizszsal': 'pajzzsal',
    'strucz': 'strucc', 'struczok': 'struccok', 'struczmadarak': 'struccmadarak', 'struczmadár': 'struccmadár',
    'struczmadárnak': 'struccmadárnak',
}


def alak_modern(alak, sor, kis_szavak):
    """Egy alak helyesírási modern alakja (szövegkörnyezet nélkül): (alak, [szabályok])."""
    szab = []
    uj = alak
    kis = alak.lower()
    if kis in ALAK_KIVETEL:  # napló 4.1.5 (ELT-2)
        cel = ALAK_KIVETEL[kis]
        return (nagy(alak, cel), ['kivetel']) if cel != kis else (alak, ['kivetel'])
    if kis in NEK_CSALAD:  # DT128 (néki), DT-F96j (néked, nékem, nékik, nékünk, néktek)
        return nagy(alak, 'nek' + kis[3:]), ['neki']
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
    u2 = jok_alt(uj)  # DT-F96g: a j-s birtokos T/3 -jok/-jök → -juk/-jük (a j nélküli marad)
    if u2:
        uj = u2
        szab.append('jok')
    if szab == ['kivetel'] and uj == alak:
        return alak, ['kivetel']
    return uj, szab


def tamasz(modern, szab, kis_szavak):
    if 'szoto_94' in szab or 'kivetel' in szab:
        return 'szoto_94' if 'szoto_94' in szab else 'manual'
    if modern.lower() in kis_szavak:
        return 'korpusz'
    return 'modell_ellenorizetlen'


def cimke(szab, uj):
    return (szab + '+' + uj if szab else uj) if uj else szab


def nevmas_csalad(kis):
    for csal, rx in NEVMAS.items():
        if rx.match(kis):
            return csal
    return None


def vers_feldolgoz(igehely, szoveg, alakszotar, ami_proba=None, ami_naplo=None):
    """Egy vers: tokenlista [(sorszam, alak1908, modern, kieso, szabaly, bizonytalan)], modern szöveg.

    ami_proba: a DT-F96i „a mi”-döntése (spans, szoveg, i) → (dontes|None, kriterium); a kiadott futás
    mindig megadja, nélküle a régi (DT-F96i előtti) döntés fut. Ha ami_naplo is megadott, a puszta „a mi”
    minden tokenje oda kerül (régi és DT-F96i szerinti döntés)."""
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
                    regi = 'bizonytalan'
                elif NK.search(wk):
                    regi = 'birtokos'
                else:
                    regi = 'vonatkozo'
            else:
                regi = 'irasjel'
            dontes, krit = regi, ''
            if ami_proba is not None:  # DT-F96i (a kiadott futásban mindig; nélküle a régi döntés)
                d, krit = ami_proba(spans, szoveg, i)
                if d:
                    dontes = d
                elif regi in ('bizonytalan', 'irasjel'):
                    krit = 'nincs_tampont'
                else:
                    krit = 'regi_szabaly'
                if ami_naplo is not None:
                    ami_naplo.append((igehely, i + 2, regi, dontes, krit))
                krit = 'ami:' + krit
            if dontes == 'bizonytalan':
                sorok[i + 1][5] = 'mi_birtokos_vagy_vonatkozo'
                sorok[i + 1][4] = cimke(sorok[i + 1][4], krit)
                continue
            if dontes == 'irasjel':
                sorok[i + 1][5] = 'mi_irasjel_utan'
                sorok[i + 1][4] = cimke(sorok[i + 1][4], krit)
                continue
            if dontes == 'birtokos':
                sorok[i + 1][5] = ''
                sorok[i + 1][4] = cimke(cimke(sorok[i + 1][4], 'mi_birtokos_marad'), krit)
                continue
            sorok[i + 1][4] = cimke(sorok[i + 1][4], krit)
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
    ap.add_argument('--minta', action='store_true', help='új minta a maggal (más verseket választhat)')
    ap.add_argument('--minta-frissit', action='store_true',
                    help='a meglévő minta újraszámolása, a kiválasztás és a felhasználói oszlopok megtartásával')
    ap.add_argument('--kimenet', default=None, help='próba-kimenet könyvtára (a repón kívül)')
    ap.add_argument('--ami-proba', action='store_true',
                    help='DT-F96i mérése: csak a helyesiras_ami_proba.tsv-t és a helyesiras_ami_ellenorzes.tsv-t írja')
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
    dont = ami_proba_keszit(tabla, fedettseg.igei_tovek(tabla, kis_szavak))
    if a.ami_proba:
        ami_proba_fut(versek, alakszotar, dont, ki_dir)
        return

    tok_ki = []
    vers_ki = {}
    szab_tok = collections.Counter()
    bizonytalan = collections.Counter()
    for igehely, sz in versek:
        sorok, modern = vers_feldolgoz(igehely, sz, alakszotar, dont)
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
              'a puszta „a mi”: DT-F96i | Hunspell csak fejlesztési mérce (DT301, ítélete: helyesiras_hunspell.tsv), '
              'a tamasz=modell_ellenorizetlen a felhasználói mintán mérendő\n'
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
    elif a.minta_frissit:
        minta_frissit(vers_ki, tabla, kis_szavak, ki_dir, fejlec)


def felhasznaloi_oszlopok(ut, kulcs, oszlopok):
    """A már kitöltött felhasználói oszlopok (ellenorzes, megjegyzes) egy generált fájlból, kulcs szerint."""
    ki = {}
    if not os.path.exists(ut):
        return ki
    fej = None
    with open(ut, encoding='utf-8') as f:
        for l in f:
            if l.startswith('#'):
                continue
            m = l.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            d = dict(zip(fej, m))
            ki[tuple(d[k] for k in kulcs)] = [d.get(o, '') for o in oszlopok]
    return ki


def ami_proba_fut(versek, alakszotar, dont, ki_dir):
    """DT-F96i: a szabály nélküli (régi) és a DT-F96i szerinti „a mi”-döntés összevetése.

    Ír: helyesiras_ami_proba.tsv (minden puszta „a mi”) és helyesiras_ami_ellenorzes.tsv (a szöveget
    változtató döntések és a megmaradt bizonytalanok, felhasználói ellenőrzésre; a már kitöltött
    ellenorzes/megjegyzes értékek megmaradnak)."""
    naplo = []
    regi_modern, uj_modern = {}, {}
    uj_par = collections.Counter()
    for igehely, sz in versek:
        sorok_r, m_r = vers_feldolgoz(igehely, sz, alakszotar)
        sorok_u, m_u = vers_feldolgoz(igehely, sz, alakszotar, dont, naplo)
        regi_modern[igehely], uj_modern[igehely] = m_r, m_u
        for r, u in zip(sorok_r, sorok_u):
            if (r[2], r[3]) != (u[2], u[3]):
                uj_par[(u[1], u[2] or '(összevonva)')] += 1
    vszoveg = dict(versek)
    sorok_ki = []
    for igehely, n, regi, uj, krit in naplo:
        sp = [m.group(0) for m in BETU.finditer(vszoveg[igehely])]
        elozo = sp[n - 3] if n >= 3 else ''
        kov = ' '.join(sp[n:n + 2])
        sorok_ki.append([igehely, str(n), elozo, kov, regi, uj, krit, 'igen' if regi != uj else 'nem'])
    # a minta (112 vers): melyik sor modern szövege változna
    minta_valt = []
    with open(os.path.join(ROOT, KI_DIR, 'helyesiras_minta.tsv'), encoding='utf-8') as f:
        for l in f:
            m = l.rstrip('\n').split('\t')
            if l.startswith('#') or m[0] == 'minta_id':
                continue
            if uj_modern[m[2]] != m[4]:
                minta_valt.append('%s %s (%s)' % (m[0], m[2], m[1]))
    # Hunspell (DT301, csak mérce): az új alakpárok benne vannak-e a már megítélt párokban
    hs = {}
    with open(os.path.join(ROOT, KI_DIR, 'helyesiras_hunspell.tsv'), encoding='utf-8') as f:
        for l in f:
            m = l.rstrip('\n').split('\t')
            if l.startswith('#') or m[0] == 'alak_1908':
                continue
            hs[(m[0], m[1])] = m[8]
    hk = ('%s (sha256:%s) + %s (sha256:%s) + %s (sha256:%s)'
          % (KAROLI, sha(KAROLI)[:12], SZOTARI, sha(SZOTARI)[:12], SZKRIPT, sha(SZKRIPT)[:12]))
    with open(os.path.join(ki_dir, 'helyesiras_ami_proba.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: %s --ami-proba (F96.1, DT-F96i) — kézzel nem szerkeszthető; mérés, nem a kiadott '
                'réteg (az a DT-F96i óta a dontes_kiserleti oszlop szerint jár el) | forras=%s | scope=a Károli 1908 '
                'minden puszta „a mi” tokenje (%d): a DT-F96i előtti és a DT-F96i szerinti döntés, kritériummal '
                '| ts=%s\n'
                % (SZKRIPT, hk, len(sorok_ki), datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')))
        f.write('\t'.join(['igehely', 'sorszam', 'elozo', 'kovetkezo', 'dontes_regi', 'dontes_kiserleti',
                           'kriterium', 'valtozik']) + '\n')
        for s in sorok_ki:
            f.write('\t'.join(s) + '\n')
    ell_ut = os.path.join(ki_dir, 'helyesiras_ami_ellenorzes.tsv')
    regi_ell = felhasznaloi_oszlopok(ell_ut, ('igehely', 'sorszam'), ('ellenorzes', 'megjegyzes'))
    ell = []
    for s in sorok_ki:
        regi, uj = s[4], s[5]
        if uj == 'bizonytalan':
            tipus = 'bizonytalan'
        elif (regi == 'vonatkozo') != (uj == 'vonatkozo'):
            tipus = 'osszevonas_uj' if uj == 'vonatkozo' else 'osszevonas_visszavonva'
        else:
            continue
        ell.append([tipus, s[0], s[1], vszoveg[s[0]], regi_modern[s[0]], uj_modern[s[0]], s[6]]
                   + regi_ell.get((s[0], s[1]), ['', '']))
    with open(ell_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# GENERÁLT: %s --ami-proba (F96.1, DT-F96i) — kézzel nem szerkeszthető, kivéve az ellenorzes és a '
                'megjegyzes oszlopot, amelyet a felhasználó tölt, vagy a felhasználó által elfogadott modell-ellenőrzés '
                '(DT-F96h; jó / hibás; a bizonytalan sorokon: vonatkozó / birtokos); újragenerálásnál a kitöltött értékek megmaradnak | forras=%s | scope=a '
                'DT-F96i szerint szöveget változtató „a mi”-döntések és a megmaradt bizonytalanok (%d token) | ts=%s\n'
                % (SZKRIPT, hk, len(ell), datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')))
        f.write('\t'.join(['ae_id', 'tipus', 'igehely', 'sorszam', 'szoveg_1908', 'szoveg_modern_dt_f96i_elott',
                           'szoveg_modern', 'kriterium', 'ellenorzes', 'megjegyzes']) + '\n')
        for i, s in enumerate(ell, 1):
            f.write('\t'.join(['A%03d' % i] + s) + '\n')
    print('ellenőrző fájl: %d token; típusonként: %s' % (len(ell), dict(collections.Counter(s[0] for s in ell))))
    atm = collections.Counter((s[4], s[5]) for s in sorok_ki)
    print('puszta „a mi”: %d token' % len(sorok_ki))
    print('régi döntés: %s' % dict(collections.Counter(s[4] for s in sorok_ki)))
    print('kísérleti döntés: %s' % dict(collections.Counter(s[5] for s in sorok_ki)))
    print('átmenet (régi → kísérleti): %s' % dict(sorted(atm.items())))
    for (r, u), db in sorted(atm.items()):
        kr = collections.Counter(s[6] for s in sorok_ki if (s[4], s[5]) == (r, u))
        print('  %s → %s: %s' % (r, u, dict(kr)))
    print('változó vers (modern szöveg): %d' % sum(1 for k in versek if regi_modern[k[0]] != uj_modern[k[0]]))
    print('a mintában változó sor: %d %s' % (len(minta_valt), minta_valt))
    print('új alakpár (token): %s' % dict(uj_par))
    print('Hunspell-ítélet az új alakpárokra (helyesiras_hunspell.tsv): %s'
          % {'%s→%s' % p: hs.get(p, 'nincs a táblában') for p in uj_par})
    print('bemenet: %s' % hk)


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
    sorok_ki = [minta_sor('M%03d' % i, reteg, ih, vers_ki, tabla, kis_szavak) + ['', '']
                for i, (reteg, ih) in enumerate(valasztott, 1)]
    minta_ir(sorok_ki, ki_dir, fejlec, '')


def minta_frissit(vers_ki, tabla, kis_szavak, ki_dir, fejlec):
    """A meglévő minta újraszámolása a kiválasztás (minta_id, réteg, igehely) és a felhasználói
    oszlopok (ellenorzes, megjegyzes) megtartásával; a szabályváltozás (DT-F96i) így nem cseréli a verseket."""
    ut = os.path.join(ki_dir, 'helyesiras_minta.tsv')
    regi = []
    fej = None
    with open(ut, encoding='utf-8') as f:
        for l in f:
            if l.startswith('#'):
                continue
            m = l.rstrip('\n').split('\t')
            if fej is None:
                fej = m
                continue
            regi.append(dict(zip(fej, m)))
    sorok_ki = [minta_sor(d['minta_id'], d['reteg'], d['igehely'], vers_ki, tabla, kis_szavak)
                + [d['ellenorzes'], d['megjegyzes']] for d in regi]
    valt = [s[0] for s, d in zip(sorok_ki, regi) if (s[4], s[5]) != (d['szoveg_modern'], d['valtozasok'])]
    minta_ir(sorok_ki, ki_dir, fejlec, ' | a kiválasztás változatlan, a szabály szerint újraszámolva (--minta-frissit)')
    print('minta frissítve: %d sor; változott a szoveg_modern vagy a valtozasok: %s' % (len(sorok_ki), valt))


def minta_sor(mid, reteg, ih, vers_ki, tabla, kis_szavak):
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
    return [mid, reteg, ih, sz, modern, '; '.join(valt), alt]


def minta_ir(sorok_ki, ki_dir, fejlec, megj):
    with open(os.path.join(ki_dir, 'helyesiras_minta.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(fejlec.replace('\n', ' | scope=rögzített magú (%d) rétegzett minta, %d vers; az ellenorzes és a '
                               'megjegyzes oszlopot a felhasználó tölti, vagy a felhasználó által elfogadott '
                               'modell-ellenőrzés (DT-F96h; jó / hibás / A / B)%s\n'
                               % (MAG, len(sorok_ki), megj)))
        f.write('\t'.join(['minta_id', 'reteg', 'igehely', 'szoveg_1908', 'szoveg_modern', 'valtozasok',
                           'alternativa', 'ellenorzes', 'megjegyzes']) + '\n')
        for s in sorok_ki:
            f.write('\t'.join(s) + '\n')
    print('minta: %d vers; rétegenként: %s' % (len(sorok_ki), dict(collections.Counter(s[1] for s in sorok_ki))))


if __name__ == '__main__':
    main()
