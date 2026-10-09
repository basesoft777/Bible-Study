#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F85.3 — az esetlista finomítása: (1) a 3 valodi_hiany_tahot sor fejezeten átnyúló újramérése (Préd 2:25, Hós 2:1,
Hós 12:3 és a Hós 12 környezete), (2) a csak-detektoros (szint=B) eltolás-sorok független ellenőrzése.

Bemenet: naplok/F85_esetlista.tsv (az `eszkozok/tahot_verskulcs_esetlista.py` kimenete). Kimenet: ugyanaz a fájl két új
oszloppal (`b_ellenorzes`, `megjegyzes`) és a javított sorokkal; naplok/F85_b_ellenorzes.tsv (a B sorok jelei).
Csak olvas minden más táblát. Az esetlista-szkript újrafuttatása után ezt is újra kell futtatni (idempotens).

A B-ellenőrzés jelei soronként (+1 támogat / 0 nincs adat / -1 ellentmond):
  kjv   : a Károli-vers KJV-megfelelője (Karoli_versmegfeleltetes.igehely_kjv) Strong-Jaccardja a TAHOT-verssel
          (>= 0,5: +1; < 0,3: -1)
  tvtms : a Károli-vers TVTMS/MT-megfelelője (csak osztaly=MT sorok) egyezik-e a WLC-vel igazolt MT-verssel
  hossz : a Károli-szószám / TAHOT-szószám arány eltérése a könyv mediánjától a javasolt párosításnál vs. az azonos
          kulcsú Károli-versnél (a javasolt jobb: +1; rosszabb: -1)
Besorolás: ellentmond = kjv vagy tvtms -1; igazolt = legalább 2 jel +1 (a hossz -1 zajos, nem blokkol); különben nem_igazolt.
Külön oszlop: a kézi szövegolvasás (`OLVASVA` halmaz) - a gépi besorolást nem írja felül.

Használat:  python eszkozok/tahot_verskulcs_finomit.py
"""
import math
import os
import re
import statistics
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'karoli_strong'))
import tahot_verskulcs_esetlista as E  # noqa: E402
import tokenek  # noqa: E402

ROOT = E.ROOT
LISTA = os.path.join(ROOT, 'naplok', 'F85_esetlista.tsv')
BEL = os.path.join(ROOT, 'naplok', 'F85_b_ellenorzes.tsv')

# a fejezeten átnyúló esetek: (extra TAHOT-vers, a Károli-vers, amelynek a szavai közt van, a fő TAHOT-vers)
OSSZEVONAS = [
    ('Préd 2:25', 'Préd 2:26', 'Préd 2:26'),
    ('Hós 2:1', 'Hós 1:11', 'Hós 1:11'),
    ('Hós 12:1', 'Hós 11:11', 'Hós 11:11'),
]
# kézi szövegolvasás (a Károli-vers és a TAHOT-glossza tartalmi egyezése; F85.3, manual): a ténylegesen elolvasott T-kulcsok
OLVASVA = {'2Móz 36:1', '2Móz 36:2', '2Móz 36:3', '2Móz 36:4', '2Móz 36:5', '2Móz 36:6', '2Móz 36:7', '2Móz 36:9', '2Móz 36:38',
           'Én 6:11', 'Én 6:12', 'Én 6:13', 'Ézs 8:23', 'Ézs 64:12', 'Hós 2:23', 'Hós 13:16', 'Hós 14:1', 'Hós 14:2', 'Hós 14:3', 'Hós 14:4', 'Hós 14:5', 'Hós 14:6',
           'Hós 14:7', 'Hós 14:8', 'Hós 14:9', '4Móz 30:2', '4Móz 30:4', '4Móz 30:5', '4Móz 30:10', '4Móz 30:13', '4Móz 30:15',
           '4Móz 30:16', '4Móz 30:17'}
HOS12_ELTOLAS = [('Hós 12:2', 'Hós 12:1'), ('Hós 12:3', 'Hós 12:2')]


def tvtms_tabla():
    m = {}
    for r in E.olvas_tsv(os.path.join(E.K, 'Karoli_versmegfeleltetes.tsv')):
        if len(r) >= 5 and r[0]:
            m[r[0]] = (r[1], r[2], r[3])
    return m


def f2(x):
    return '-' if x is None else '%.2f' % x


def main():
    tver = E.betolt_tahot()
    ktxt = E.betolt_karoli_szoveg()
    klen = {k: len(tokenek.tokenizal(s)) for k, s in ktxt.items()}
    kjv = E.betolt_kjv()
    tv = tvtms_tabla()
    macula = E.betolt_macula()
    with open(LISTA, encoding='utf-8') as fh:
        sorok = [s.rstrip('\n') for s in fh]
    fejlec_hash = [s for s in sorok if s.startswith('#')]
    adat = [s.split('\t') for s in sorok if not s.startswith('#')]
    fej = adat[0]
    rows = [r[:6] for r in adat[1:]]
    rows = [r + [''] * (6 - len(r)) for r in rows]

    # --- 1. WLC-Jaccard a szükséges versekre (igazítás a Préd és Hós könyvre) ---
    wlc = {}
    for konyv in ('Préd', 'Hós'):
        tk = sorted((E.bont(ig)[1], E.bont(ig)[2]) for ig in tver if E.bont(ig)[0] == konyv)
        mver = macula[konyv]
        mk = sorted(mver)
        for ti, mj, jj in E.igazit(tk, mk, tver, mver, konyv):
            if ti is not None:
                wlc['%s %d:%d' % (konyv, *tk[ti])] = ('%s %d:%d' % (konyv, *mk[mj]) if mj is not None else '-', jj)

    def tl(t):
        return tver[t][1]

    def mediana(konyv):
        l = [math.log(klen[k] / tl(k)) for k in klen if k.startswith(konyv + ' ') and k in tver and tl(k) > 0 and klen[k] > 0]
        return statistics.median(l)

    # --- 2. a három hiány + a Hós 12 javítása ---
    torol = {x for o in OSSZEVONAS for x in (o[0], o[2])} | {'Hós 12:2', 'Hós 12:3'}
    rows = [r for r in rows if r[2] not in torol]
    uj = []
    bekov = {}
    for extra, k, fo in OSSZEVONAS:
        konyv = k.split(' ')[0]
        mu = mediana(konyv)
        arany = klen[k] / (tl(extra) + tl(fo))
        for t in (extra, fo):
            m, jj = wlc.get(t, ('-', 0.0))
            tip = 'osszevonas_2_1'
            ig = ('szint=S | szövegtartalom + szóarány (a Károli-vers két TAHOT-vers tartalmát hordozza: %s és %s; Károli szószám %d, TAHOT-szószámok %d + %d, arány %.2f, a könyv mediánja %.2f) | WLC=%s J=%.2f | Strong-igazolás a Károli-oldalra nincs; a szövegtartalmi egyezés kézi olvasás (a Károli-szakasz és a TAHOT-glossza összevetése), megerősítésre vár'
                  % (extra, fo, klen[k], tl(extra), tl(fo), arany, math.exp(mu), m, jj))
            uj.append([k.split(' ')[0], str(E.bont(t)[1]), t, k, tip, ig])
    for t, k in HOS12_ELTOLAS:
        konyv = 'Hós'
        m, jj = wlc.get(t, ('-', 0.0))
        ig = ('szint=S | #22-tipus=hiányzó/azonos-kulcs (a mai tábla hibás; javítás: kézi eltolt sor) | szóarány: Károli %d / TAHOT %d = %.2f (könyv mediánja %.2f); az azonos kulcsú Károli-vers (%s) %d szó -> %.2f | WLC=%s J=%.2f | hosszkorreláció (fejezet) r(azonos)=-0.09, r(Macula)=0.89 | a Károli-szöveg tartalma = a TAHOT-glossza (K 12:1 „Széllel táplálkozik Efraim” = T 12:2 „Ephraim feeding wind”; K 12:2 „Pere van az Úrnak a Júdával” = T 12:3 „case at law Yahweh with Judah”)'
              % (klen[k], tl(t), klen[k] / tl(t), math.exp(mediana(konyv)), t, klen.get(t, 0), (klen.get(t, 0) / tl(t)) if t in klen else 0, m, jj))
        uj.append(['Hós', '12', t, k, 'eltolas', ig])
    rows += uj

    # --- 3. a B sorok független ellenőrzése ---
    mu_cache = {}
    bsorok = []
    kimenet = []
    for r in rows:
        r = r + [''] * (9 - len(r))
        m = re.search(r'szint=B(?![+\w])', r[5])
        if m and r[4] == 'eltolas':
            t, k = r[2], r[3]
            konyv = t.split(' ')[0]
            mm = re.search(r'WLC=([^ ]+ [0-9:]+) J=', r[5])
            mt_v = mm.group(1) if mm else None
            # kjv
            kj_s, kj_j = 0, None
            kj = tv.get(k)
            if kj and kj[0]:
                kjk = '%s %s' % (k.split(' ')[0], kj[0])
                if kjk in kjv:
                    kj_j = E.jaccard(tver[t][0], kjv[kjk])
                    kj_s = 1 if kj_j >= 0.5 else (-1 if kj_j < 0.3 else 0)
            # tvtms
            tv_s = 0
            if kj and kj[2] == 'MT' and kj[1] and mt_v:
                tv_s = 1 if ('%s %s' % (konyv, kj[1])) == mt_v else -1
            # hossz
            mu = mu_cache.setdefault(konyv, mediana(konyv))
            e22 = abs(math.log(klen[k] / tl(t)) - mu) if k in klen and tl(t) else None
            eid = abs(math.log(klen[t] / tl(t)) - mu) if t in klen and tl(t) else None
            h_s = 0
            if e22 is not None:
                if eid is not None:
                    h_s = 1 if e22 + 0.15 < eid else (-1 if e22 > eid + 0.15 else 0)
                else:
                    h_s = 1 if e22 < 0.5 else (-1 if e22 > 0.9 else 0)
            jelek = (kj_s, tv_s, h_s)
            r[7] = 'olvasva_egyezik' if t in OLVASVA else 'nem_olvasott'
            if kj_s == -1 or tv_s == -1:
                b = 'ellentmond'
            elif sum(1 for x in jelek if x == 1) >= 2:
                b = 'igazolt'
            else:
                b = 'nem_igazolt'
            r[6] = b
            r[8] = 'kjv=%+d(J=%s) tvtms=%+d hossz=%+d(err#22=%s, err_azonos=%s; a -1 rövid versekben zajos, nem blokkol)' % (kj_s, f2(kj_j), tv_s, h_s, f2(e22), f2(eid))
            if b == 'ellentmond' and tv_s == -1 and kj_s == 1:
                r[8] += ' | a Karoli_versmegfeleltetes TVTMS-sora (MT-szám) a KJV-tanúval és a szövegolvasással ellentétes: a TVTMS-tábla sora gyanús'
            bsorok.append((r[0], r[2], r[3], b, r[7], r[8]))
        kimenet.append(r)
    kimenet.sort(key=lambda s: (E_idx(s[0]), int(s[1]), E.bont(s[2])[2], s[2]))

    with open(LISTA, 'w', encoding='utf-8', newline='\n') as fh:
        for s in fejlec_hash:
            fh.write(s + '\n')
        fh.write('\t'.join(fej[:6] + ['b_ellenorzes', 'megjegyzes']) + '\n')
        for r in kimenet:
            fh.write('\t'.join(r[:8]) + '\n')
    with open(BEL, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# GENERÁLT: eszkozok/tahot_verskulcs_finomit.py | a szint=B (csak #22-detektor) eltolás-sorok független ellenőrzése (kjv, tvtms, hossz jelek; l. a szkript docstringje)\n')
        fh.write('konyv\ttahot_kulcs\tkaroli_vers\tb_ellenorzes\tjelek\n')
        for b in bsorok:
            fh.write('\t'.join(b) + '\n')
    import collections
    c = collections.Counter((b[0], b[3], b[4]) for b in bsorok)
    print('B sorok:', len(bsorok), dict(collections.Counter(b[3] for b in bsorok)))
    for k_, v_ in sorted(c.items()):
        print(k_, v_)
    tip = collections.Counter(r[4] for r in kimenet)
    print('típusok:', dict(tip))
    return 0


_KONYVEK = None


def E_idx(b):
    global _KONYVEK
    if _KONYVEK is None:
        _KONYVEK = []
        for ig in E.betolt_tahot():
            bb = E.bont(ig)[0]
            if bb not in _KONYVEK:
                _KONYVEK.append(bb)
    return _KONYVEK.index(b)


if __name__ == '__main__':
    sys.exit(main())
