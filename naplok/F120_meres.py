"""F120.1 (3.1): a tényleges hibamód újramérése (csak olvas, semmit nem ír a repóba; a kimenet a stdout).

A BSB-klón (bsb-data-output) nélkül fut: a bsb_import tényleges `allapot`-a a display-JSON nélkül nem számolható,
ezért az R4-et a feltétele szintjén méri (kk_max_tabla x TAHOT-max), a veszélyeztetett sorokat pedig a mai
BSB_Strongs.tsv-n számolja.

1. R4 (bsb_import.konyv_megfeleltetes): azok a (könyv, MT-fejezet) párok, ahol a Károli-kulcs igehely_mt-maximuma
   (kk_max_tabla) eltér a TAHOT fejezet-maximumától (az F85.6 óta Károli-kulcs), a régi (F117.3 előtti) és a mai
   táblán; fejezetenként a mai BSB_Strongs.tsv sorai/versei ebben a fejezetben (ezek esnének ki `illesztetlen`-ként,
   ha a BSB-fejezet erre az MT-fejezetre képez).
2. fejezet_eltolasok (csak a bsb_verseltolas_diag hívja, csak a Zsoltárokra): a TAHOT-max == KK-MT-max feltétel
   mely Zsoltár-fejezeteken sérül (a k = 0..2 feltétel a text_only versszám, azaz a klón nélkül nem mérhető).
3. sqlite_epit._bsb_szamozas szimulációja a mai BSB_Strongs.tsv-n (a kód logikája, az őr nélkül): ütközések
   (Károli-vers két különböző BSB-kulccsal), a leképezés módja fejezetenként (mt_tabla / azonos_feltetelezett),
   és ahol az azonos_feltetelezett célja egyben egy mt_tabla-pár célja.
4. A mai BSB_Strongs.tsv Igehely-kulcsának szemantikája (a 3.2-höz): a BSB-vers Strong-halmazát a WLC (Macula)
   azonos számú versével és a TAHOT azonos számú (Károli-kulcsú) versével veti össze, a Károli != MT sorokon
   (igehely_mt kitöltve és eltér a Károli-számtól). Ha a BSB-kulcs MT, a BSB[MT] a TAHOT[Károli]-val egyezik.

Használat: python naplok/F120_meres.py <regi_versmegfeleltetes.tsv> [mai_versmegfeleltetes.tsv]
(a 2. argumentummal a 3–5. rész a megadott táblán fut; alapértelmezés a repó mai táblája)
(a régi tábla: git show 8f616529^:konkordancia/Karoli_versmegfeleltetes.tsv)
"""
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'fj2'))

import kozos  # noqa: E402
import wlc_versek  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

K = os.path.join(ROOT, 'konkordancia')
VERS = re.compile(r'^(.+) (\d+):(\d+)$')
STEP = re.compile(r'^([1-3]?[A-Za-z]+)\.(\d+)\.(\d+)[a-z]?$')
ALIAS = {'JSir': 'Sir'}  # sqlite_epit.KONYV_ALIAS, bsb_import.TAHOT_NEV


def tabla(path):
    fej, sorok = kozos.tsv_olvas(path)
    idx = [fej.index(n) for n in ('igehely_karoli', 'igehely_kjv', 'igehely_mt', 'osztaly')]
    return [tuple(s[i] if len(s) > i else '' for i in idx) for s in sorok]


def kk_max_tabla(t):
    """bsb_import.kk_max_tabla másolata."""
    ki = {}
    for kar, kjv, mt, osz in t:
        m = re.fullmatch(r'(\d+):(\d+)', mt)
        if not m:
            continue
        d = ki.setdefault(kar.rsplit(' ', 1)[0], {})
        f, v = int(m.group(1)), int(m.group(2))
        d[f] = max(d.get(f, 0), v)
    return ki


def tahot():
    """({könyv: {fejezet: max}}, {igehely: set(Strong)})."""
    halm = kozos.tahot_strongok()
    mx = defaultdict(dict)
    for r in halm:
        m = VERS.match(r)
        if m:
            b, f, v = m.group(1), int(m.group(2)), int(m.group(3))
            mx[b][f] = max(mx[b].get(f, 0), v)
    return mx, halm


def step_hu():
    fej, sorok = kozos.tsv_olvas(os.path.join(K, 'Konyv_normalizalo_tabla.tsv'))
    ki = {}
    for s in sorok:
        hu = ALIAS.get(s[1], s[1])
        ki[s[0]] = hu
        for a in (s[3].split(',') if len(s) > 3 else []):
            if a.strip():
                ki.setdefault(a.strip(), hu)
    return ki


def bsb_sorok(sh):
    """[(könyv, f, v, Strong int vagy None, Számozás, step-kód)] a mai BSB_Strongs.tsv-ből."""
    ki = []
    with open(os.path.join(K, 'BSB_Strongs.tsv'), encoding='utf-8') as f:
        f.readline()
        for sor in f:
            m0 = sor.rstrip('\n').split('\t')
            m = STEP.match(m0[0])
            if not m or m.group(1) not in sh:
                continue
            ki.append((sh[m.group(1)], int(m.group(2)), int(m.group(3)), kozos.strong_szam(m0[2]), m0[6], m.group(1)))
    return ki


def jaccard(a, b):
    return len(a & b) / len(a | b) if (a or b) else 0.0


def main():
    regi = tabla(sys.argv[1])
    uj = tabla(sys.argv[2] if len(sys.argv) > 2 else os.path.join(K, 'Karoli_versmegfeleltetes.tsv'))
    tmax, th = tahot()
    sh = bsb_sorok_sh = step_hu()
    bsb = bsb_sorok(sh)
    bsb_fv = defaultdict(lambda: [0, set()])  # (könyv, f) -> [sorok, versek]
    bsb_halm = defaultdict(set)               # (könyv, f, v) -> Strong-halmaz
    bsb_szam = {}
    for b, f, v, s, sz, kod in bsb:
        bsb_fv[(b, f)][0] += 1
        bsb_fv[(b, f)][1].add(v)
        if s is not None and s < 9000:
            bsb_halm[(b, f, v)].add(s)
        bsb_szam[(b, f, v)] = sz

    print('## 1. R4 (kk_max_tabla x TAHOT-max)')
    for nev, t in (('régi', regi), ('mai', uj)):
        kk = kk_max_tabla(t)
        elt = []
        for b in sorted(kk):
            for f in sorted(kk[b]):
                if tmax.get(b, {}).get(f, 0) != kk[b][f]:
                    elt.append((b, f, kk[b][f], tmax.get(b, {}).get(f)))
        sor_ossz = sum(bsb_fv[(b, f)][0] for b, f, _, _ in elt)
        vers_ossz = sum(len(bsb_fv[(b, f)][1]) for b, f, _, _ in elt)
        print('%s tábla: %d fejezet; a mai BSB_Strongs.tsv-ben ezekben a fejezetekben %d vers, %d sor' % (nev, len(elt), vers_ossz, sor_ossz))
        for b, f, k, t_ in elt:
            print('  %s %d\tKK-MT-max %d\tTAHOT-max %s\tBSB %d vers / %d sor' % (b, f, k, t_, len(bsb_fv[(b, f)][1]), bsb_fv[(b, f)][0]))

    print('\n## 2. fejezet_eltolasok (Zsolt): TAHOT-max != KK-MT-max')
    for nev, t in (('régi', regi), ('mai', uj)):
        kk = kk_max_tabla(t).get('Zsolt', {})
        elt = ['%d (KK %d, TAHOT %s)' % (f, kk[f], tmax['Zsolt'].get(f)) for f in sorted(kk) if tmax['Zsolt'].get(f) != kk[f]]
        print('%s tábla: %d Zsoltár-fejezet: %s' % (nev, len(elt), '; '.join(elt) or '-'))

    print('\n## 3. sqlite_epit._bsb_szamozas szimuláció (mai tábla, mai BSB_Strongs.tsv)')
    karoli = {r[0] for r in uj}
    mt_kk = {}
    for kar, kjv, mt, osz in uj:
        if mt:
            mt_kk[(kar.rsplit(' ', 1)[0], mt)] = kar
    cel = defaultdict(set)
    mod_fej = defaultdict(Counter)
    nincs = Counter()
    for b, f, v in sorted(bsb_halm.keys() | {(x[0], x[1], x[2]) for x in bsb}):
        kulcs = '%d:%d' % (f, v)
        if (b, kulcs) in mt_kk:
            kk_, mod = mt_kk[(b, kulcs)], 'mt_tabla'
        else:
            kk_, mod = '%s %s' % (b, kulcs), 'azonos_feltetelezett'
        if kk_ not in karoli:
            nincs[b] += 1
            continue
        cel[kk_].add((kulcs, mod))
        mod_fej[(b, f)][mod] += 1
    utk = {k: sorted(v) for k, v in cel.items() if len({x[0] for x in v}) > 1}
    print('ütközés (Károli-vers két különböző BSB-kulccsal): %d' % len(utk))
    for k in sorted(utk, key=lambda x: (x.rsplit(' ', 1)[0], tuple(int(y) for y in x.rsplit(' ', 1)[1].split(':')))):
        print('  %s <- %s' % (k, ', '.join('%s (%s)' % x for x in utk[k])))
    print('nincs ilyen Károli-vers (BSB-vers): %d %s' % (sum(nincs.values()), dict(nincs)))
    vegyes = [(bf, c) for bf, c in sorted(mod_fej.items()) if c['mt_tabla'] and c['azonos_feltetelezett']]
    print('vegyes leképezésű BSB-fejezet (mt_tabla és azonos_feltetelezett is): %d' % len(vegyes))
    for (b, f), c in vegyes:
        print('  %s %d\tmt_tabla %d\tazonos_feltetelezett %d' % (b, f, c['mt_tabla'], c['azonos_feltetelezett']))
    print('összesen: mt_tabla %d vers, azonos_feltetelezett %d vers' % (
        sum(c['mt_tabla'] for c in mod_fej.values()), sum(c['azonos_feltetelezett'] for c in mod_fej.values())))

    print('\n## 4. A BSB-kulcs szemantikája a Károli != MT sorokon')
    wlc = {}
    kodok = {}
    for s, hu in sh.items():
        kodok.setdefault(hu, s)
    eredm = Counter()
    eredm_osz = defaultdict(Counter)
    peldak = defaultdict(list)
    for kar, kjv, mt, osz in uj:
        m = VERS.match(kar)
        if not m or not re.fullmatch(r'\d+:\d+', mt):
            continue
        b = m.group(1)
        kcv = '%s:%s' % (m.group(2), m.group(3))
        if mt == kcv:
            continue
        mf, mv = (int(x) for x in mt.split(':'))
        kf, kv = int(m.group(2)), int(m.group(3))
        t_k = th.get(kar)
        if not t_k:
            eredm['tahot_nincs'] += 1
            continue
        jel = {'MT': (mf, mv), 'Karoli': (kf, kv)}
        mk = re.fullmatch(r'(\d+):(\d+)', kjv)
        if mk:
            jel['KJV'] = (int(mk.group(1)), int(mk.group(2)))
        j = {n: jaccard(bsb_halm.get((b,) + fv, set()), t_k) for n, fv in jel.items()}
        if not any(bsb_halm.get((b,) + fv) for fv in jel.values()):
            eredm['bsb_nincs'] += 1
            eredm_osz[osz]['bsb_nincs'] += 1
            continue
        j_mt, j_k = j['MT'], j['Karoli']
        if b not in wlc:
            try:
                wlc[b] = wlc_versek.wlc_konyv(wlc_versek.macula_kod(kodok[b] if b != 'Sir' else 'Lam'))
            except Exception:
                wlc[b] = {}
        w = wlc[b].get((mf, mv), set())
        legj = max(j.values())
        nyertes = sorted(n for n in j if j[n] == legj)
        # azonos számú jelöltek (pl. KJV-szám = MT-szám) egy kulcsnak számítanak: a nyertes név '=' jellel összevonva
        nyertes_kulcsok = {jel[n] for n in nyertes}
        if legj < 0.5:
            o = 'egyik_sem (max J < 0,5)'
        elif len(nyertes_kulcsok) > 1:
            o = 'eldonthetetlen (' + '/'.join(nyertes) + ')'
        else:
            o = 'BSB_kulcs_' + '='.join(nyertes)
        eredm[o] += 1
        eredm_osz[osz][o] += 1
        sz = bsb_szam.get((b, mf, mv), '')
        eredm_osz['Számozás(BSB[MT])=' + sz][o] += 1
        eredm_osz['könyv-fejezet ' + kar.rsplit(':', 1)[0]][o] += 1
        if len(peldak[o]) < 8:
            peldak[o].append('%s (MT %s, KJV %s): J(BSB[x],TAHOT[K]) %s; J(TAHOT[K],WLC[MT])=%.2f; Számozás(BSB[MT])=%s' % (
                kar, mt, kjv, ' '.join('%s=%.2f' % kv for kv in sorted(j.items())), jaccard(t_k, w), sz))
    print('összesen: %s' % dict(eredm))
    for k, c in sorted(eredm_osz.items()):
        print('  %s: %s' % (k, dict(c)))
    for o, p in sorted(peldak.items()):
        print('  példák, %s:' % o)
        for x in p:
            print('    ' + x)
    print('\n## 5. A mai _bsb_szamozas leképezésének tartalmi helyessége (BSB[kulcs] vs TAHOT[cél Károli-vers])')
    # minden BSB-vers: a mai kód szerinti cél (mt_tabla / azonos_feltetelezett); J(BSB[kulcs], TAHOT[cél]) és J(BSB[kulcs], TAHOT[azonos szám])
    jo = Counter()
    rossz_fej = defaultdict(Counter)
    for (b, f, v), hb in sorted(bsb_halm.items()):
        kulcs = '%d:%d' % (f, v)
        if (b, kulcs) in mt_kk:
            celv, mod = mt_kk[(b, kulcs)], 'mt_tabla'
        else:
            celv, mod = '%s %s' % (b, kulcs), 'azonos_feltetelezett'
        tc = th.get(celv)
        if not tc or not hb:
            jo[(mod, 'nincs_osszevetheto')] += 1
            continue
        jc = jaccard(hb, tc)
        if jc >= 0.5:
            jo[(mod, 'egyezik (J>=0,5)')] += 1
        else:
            jo[(mod, 'nem_egyezik (J<0,5)')] += 1
            rossz_fej[(b, f)][mod] += 1
    for k, n in sorted(jo.items()):
        print('  %s / %s: %d vers' % (k[0], k[1], n))
    print('  nem egyező versek fejezetenként (ahol >= 3):')
    for (b, f), c in sorted(rossz_fej.items()):
        if sum(c.values()) >= 3:
            print('    %s %d\t%s' % (b, f, dict(c)))

    print('\nproveniencia: scope=Karoli_versmegfeleltetes.tsv régi (8f616529^) és mai, TAHOT_kivonat.tsv, BSB_Strongs.tsv (F71.2), '
          'Macula_heber_*.tsv | eszkoz=naplok/F120_meres.py | n_bsb_sor=%d | BSB-klón: nincs (allapot nem mérve) | ts=2026-11-01' % len(bsb))


if __name__ == '__main__':
    main()
