"""TSK-versszám felmérés (csak olvas, adatot nem ír).

Kérdés: a `konkordancia/TSK_kereszthivatkozasok.tsv` `Igehely` és `Kapcsolódó igehely`
kulcsa magyar könyvnevű, de KJV-számozású; a fogyasztók (lexikon_general.tsk_index,
lekerdez.cmd_tsk, nem_vizsgalt.tsk_kor, sqlite_epit, olvaso_pilot) Károli-kulcsként
használják. Ahol a Károli és a KJV versszámozása eltér, a TSK-sorok rossz Károli-versre
kerülnek. A szkript megméri:

  A. a teljes TSK-n: hány forrás- és célkulcs esik eltérő számozású versre;
  B. az `adat/elofordulasok.tsv` igehelyein: hány versnél tér el a Károli- és a
     KJV-kulcs, és ezeknél hány TSK-jelölt kerül ma rossz versre / marad el
     (minden Votes-érték és a generátor Votes >= 15 küszöbe szerint is);
  C. az `adat/jeloltek.tsv` TSK-eredetű sorain: hány sor igehelye vagy forrásverse
     esik eltérő számozású versre, és milyen döntéssel.

A megfeleltetés forrása: `konkordancia/Karoli_versmegfeleltetes.tsv` (csak ÓSZ; az ÚSZ-t
a tábla nem fedi, ott azonosság feltételezve — ezt a jelentés jelöli).

Kimenet: stdout-összegzés + részletes TSV a megadott könyvtárba (alapértelmezés: a
repón kívüli ideiglenes könyvtár). Használat:
    python eszkozok/tsk_versszam_felmeres.py [--kimenet DIR]
"""
import argparse
import datetime
import os
import re
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONK = os.path.join(REPO, 'konkordancia')
ADAT = os.path.join(REPO, 'adat')
KUSZOB = 15  # lexikon_general.blokk_kereszthivatkozasok Votes-küszöbe


def tsv(path):
    """Kommentsorokat (#) átugró TSV-olvasó, split('\\t')-tel (CLAUDE.md)."""
    with open(path, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:] if s]


def konyv_cv(ige):
    m = re.match(r'^(.+?) (\d+):(\d+)$', ige.strip())
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def kibont(ige):
    """Igehely -> versek listája. 'Könyv c:v', 'c:v-w', 'c:v-c2:w', 'c:v, w', 'c:v; c2:w'.
    Nem értelmezhető -> None."""
    ige = ige.strip().replace('–', '-')
    m = re.match(r'^(\S+(?: \S+)*?) (\d+:.*)$', ige)
    if not m:
        return None
    konyv, tobbi = m.group(1), m.group(2)
    ki = []
    fej = None
    for darab in re.split(r'[;,]\s*', tobbi):
        darab = darab.strip()
        if not darab:
            continue
        r = re.match(r'^(?:(\d+):)?(\d+)[a-z]?(?:-(?:(\d+):)?(\d+)[a-z]?)?$', darab)
        if not r:
            return None
        c1 = int(r.group(1)) if r.group(1) else fej
        if c1 is None:
            return None
        v1 = int(r.group(2))
        fej = c1
        if r.group(4) is None:
            ki.append('%s %d:%d' % (konyv, c1, v1))
            continue
        c2 = int(r.group(3)) if r.group(3) else c1
        v2 = int(r.group(4))
        if c2 == c1:
            ki.extend('%s %d:%d' % (konyv, c1, v) for v in range(v1, v2 + 1))
        else:
            # fejezethatáron átnyúló tartomány: csak a két végpontot és c1 első
            # 200 versét vesszük, a nem létező versek a kulcsoknál úgyis kiesnek
            ki.extend('%s %d:%d' % (konyv, c1, v) for v in range(v1, 200))
            for c in range(c1 + 1, c2):
                ki.extend('%s %d:%d' % (konyv, c, v) for v in range(1, 200))
            ki.extend('%s %d:%d' % (konyv, c2, v) for v in range(1, v2 + 1))
            fej = c2
    return ki


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--kimenet', default=os.path.join(tempfile.gettempdir(), 'tsk_versszam_felmeres'))
    a = ap.parse_args()
    os.makedirs(a.kimenet, exist_ok=True)
    ts = datetime.date.today().isoformat()

    # --- megfeleltetés -----------------------------------------------------
    k2j = {}       # Károli-vers -> KJV-vers ('' = nincs KJV-pár: felirat / ismeretlen)
    k2j_osztaly = {}
    for r in tsv(os.path.join(KONK, 'Karoli_versmegfeleltetes.tsv')):
        kk = r['igehely_karoli']
        b = konyv_cv(kk)
        kj = r['igehely_kjv'].strip()
        k2j[kk] = ('%s %s' % (b[0], kj)) if kj else ''
        k2j_osztaly[kk] = '%s/%s/%s' % (r['osztaly'], r['forras'], r['megjegyzes'])
    j2k = {}
    for kk, kj in k2j.items():
        if kj:
            j2k.setdefault(kj, []).append(kk)
    osz_konyvek = {konyv_cv(k)[0] for k in k2j}

    def karoli_to_kjv(kk):
        """Károli-vers -> (KJV-kulcs, státusz). Státusz: azonos / elter / nincs_kjv / usz_feltetelezett."""
        b = konyv_cv(kk)
        if b is None:
            return None, 'nem_ertelmezheto'
        if b[0] not in osz_konyvek:
            return kk, 'usz_feltetelezett'
        if kk not in k2j:
            return None, 'nincs_karoli_sor'
        kj = k2j[kk]
        if not kj:
            return None, 'nincs_kjv'
        return kj, ('azonos' if kj == kk else 'elter')

    def kjv_to_karoli(kj):
        b = konyv_cv(kj)
        if b is None or b[0] not in osz_konyvek:
            return [kj]
        return j2k.get(kj, [])

    # eltérő kulcsú Károli-versek: ahol a Károli-kulcs != KJV-kulcs, vagy nincs KJV-pár
    elter_karoli = {k for k in k2j if k2j[k] != k}
    # KJV-kulcsok, amelyek Károli-kulcsként olvasva más (vagy nem létező) Károli-versre esnek
    rossz_kjv_kulcs = set()
    for kj, kks in j2k.items():
        if kks != [kj]:
            rossz_kjv_kulcs.add(kj)

    # --- TSK ---------------------------------------------------------------
    tsk = tsv(os.path.join(KONK, 'TSK_kereszthivatkozasok.tsv'))
    tsk_idx = {}
    for r in tsk:
        tsk_idx.setdefault(r['Igehely'], []).append(r)

    # A. teljes TSK
    a_forras_osz = a_forras_rossz = a_cel_osz = a_cel_rossz = a_cel_osz_vers = 0
    for r in tsk:
        b = konyv_cv(r['Igehely'])
        if b and b[0] in osz_konyvek:
            a_forras_osz += 1
            if r['Igehely'] in rossz_kjv_kulcs or r['Igehely'] not in j2k:
                a_forras_rossz += 1
        cel = kibont(r['Kapcsolódó igehely']) or []
        if cel and konyv_cv(cel[0]) and konyv_cv(cel[0])[0] in osz_konyvek:
            a_cel_osz += 1
            if any(v in rossz_kjv_kulcs or v not in j2k for v in cel):
                a_cel_rossz += 1
    tsk_osz_kulcsok = {k for k in tsk_idx if konyv_cv(k) and konyv_cv(k)[0] in osz_konyvek}
    tsk_rossz_kulcsok = {k for k in tsk_osz_kulcsok if k in rossz_kjv_kulcs or k not in j2k}

    print('# A. Teljes TSK (ÓSZ-forrásoldal)')
    print('TSK-sor összesen: %d; ÓSZ-forrású: %d' % (len(tsk), a_forras_osz))
    print('ÓSZ-forráskulcs: %d egyedi, ebből Károli-kulcsként olvasva más/nem létező versre esik: %d (%d sor)'
          % (len(tsk_osz_kulcsok), len(tsk_rossz_kulcsok), a_forras_rossz))
    print('ÓSZ-célú sor: %d, ebből legalább egy célverse eltérő számozású: %d' % (a_cel_osz, a_cel_rossz))
    print('Eltérő kulcsú Károli-vers (megfeleltetés): %d / %d' % (len(elter_karoli), len(k2j)))
    print('proveniencia: scope=TSK-teljes | forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv | n=%d | ts=%s'
          % (len(tsk), ts))
    print()

    def tsk_halmaz(kulcs, kuszob=None):
        """kulcs -> {cél-igehely (KJV) : votes}"""
        out = {}
        for r in tsk_idx.get(kulcs, []) if kulcs else []:
            v = int(r['Votes'])
            if kuszob is None or v >= kuszob:
                out[r['Kapcsolódó igehely']] = v
        return out

    # --- B. elofordulasok ----------------------------------------------------
    elof = tsv(os.path.join(ADAT, 'elofordulasok.tsv'))
    stat = {}
    nem_bonthato = []
    reszlet = []
    vers_motivum = {}
    tartomany_sorok = 0
    for r in elof:
        versek = kibont(r['igehely'])
        if versek is None:
            nem_bonthato.append((r['id'], r['igehely']))
            continue
        if len(versek) > 1:
            tartomany_sorok += 1
        for v in versek:
            if v in k2j or konyv_cv(v)[0] not in osz_konyvek:
                vers_motivum.setdefault(v, set()).add(r['id'])
    for v in sorted(vers_motivum):
        kj, st = karoli_to_kjv(v)
        stat[st] = stat.get(st, 0) + 1
        if st in ('azonos', 'usz_feltetelezett'):
            continue
        ma = tsk_halmaz(v)                      # amit ma a fogyasztók kapnak
        jo = tsk_halmaz(kj) if kj else {}       # ami a Károli-vershez tartozna
        ma15 = {k for k, x in ma.items() if x >= KUSZOB}
        jo15 = {k for k, x in jo.items() if x >= KUSZOB}
        ma_karoli = kjv_to_karoli(v)            # mely Károli-versé valójában a mai sor
        reszlet.append({
            'vers_karoli': v, 'motivumok': ','.join(sorted(vers_motivum[v])), 'statusz': st,
            'kjv_kulcs': kj or '', 'osztaly': k2j_osztaly.get(v, ''),
            'ma_n': len(ma), 'jo_n': len(jo), 'kozos_n': len(set(ma) & set(jo)),
            'rossz_n': len(set(ma) - set(jo)), 'elmarad_n': len(set(jo) - set(ma)),
            'ma15_n': len(ma15), 'jo15_n': len(jo15), 'rossz15_n': len(ma15 - jo15),
            'elmarad15_n': len(jo15 - ma15),
            'mai_sor_valodi_karoli_verse': ';'.join(ma_karoli) if ma else '',
            'elmarado15_minta': '; '.join(sorted(jo15 - ma15)[:8]),
        })
    print('# B. elofordulasok.tsv')
    print('Sor: %d; tartomány-sor: %d; nem bontható: %d' % (len(elof), tartomany_sorok, len(nem_bonthato)))
    print('Egyedi vers (kibontva): %d; státusz: %s' % (len(vers_motivum), stat))
    erintett_motivumok = set()
    for x in reszlet:
        erintett_motivumok.update(x['motivumok'].split(','))
    sz = lambda k: sum(x[k] for x in reszlet)
    print('Eltérő/nincs-KJV vers: %d (%d motívumban)' % (len(reszlet), len(erintett_motivumok)))
    print('  minden Votes: ma %d sor, helyes %d, közös %d, rossz versről %d, elmarad %d'
          % (sz('ma_n'), sz('jo_n'), sz('kozos_n'), sz('rossz_n'), sz('elmarad_n')))
    print('  Votes>=%d: ma %d sor, helyes %d, rossz versről %d, elmarad %d'
          % (KUSZOB, sz('ma15_n'), sz('jo15_n'), sz('rossz15_n'), sz('elmarad15_n')))
    print('  vers, ahol ma van TSK-találat (>=15), de mind más versé: %d'
          % sum(1 for x in reszlet if x['ma15_n'] and x['rossz15_n'] == x['ma15_n']))
    print('  vers, ahol ma nincs találat (>=15), de helyesen lenne: %d'
          % sum(1 for x in reszlet if not x['ma15_n'] and x['jo15_n']))
    print('proveniencia: scope=elofordulasok.tsv (%d vers) | forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv | n=%d | ts=%s'
          % (len(vers_motivum), len(reszlet), ts))
    # motívumonkénti bontás
    mot = {}
    for x in reszlet:
        for m in x['motivumok'].split(','):
            d = mot.setdefault(m, [0, 0, 0])
            d[0] += 1
            d[1] += x['rossz15_n']
            d[2] += x['elmarad15_n']
    print('Motívumonként (vers / rossz>=15 / elmarad>=15), a 15 legérintettebb:')
    for m, d in sorted(mot.items(), key=lambda kv: -(kv[1][1] + kv[1][2]))[:15]:
        print('  %s\t%d\t%d\t%d' % (m, d[0], d[1], d[2]))
    print()

    # tartomány-sorok: a generátor kulcs szerint keres, a tartomány semmit nem talál
    tart_tsk = 0
    for r in elof:
        versek = kibont(r['igehely'])
        if versek and len(versek) > 1 and r['igehely'] not in tsk_idx:
            if any(tsk_halmaz(v, KUSZOB) for v in versek):
                tart_tsk += 1
    print('# B2. Mellékes: tartomány-igehely (%d sor) — a lexikon_general.tsk_index() pontos kulcsra keres;'
          ' ebből %d sor verseire volna >=15 TSK-találat, a blokk ezekre ma semmit nem ad'
          % (tartomany_sorok, tart_tsk))
    print()

    # B3. céloldal: a motívum-versek (ma kapott) >=15 TSK-találatai közül hány cél esik
    # eltérő számozású versre — a megjelenített hivatkozás ott más Károli-versre mutat
    cel_ossz = cel_rossz = 0
    cel_minta = []
    for v in vers_motivum:
        for c in tsk_halmaz(v, KUSZOB):
            cel_ossz += 1
            cv = kibont(c) or []
            if any(x in rossz_kjv_kulcs or (konyv_cv(x) and konyv_cv(x)[0] in osz_konyvek and x not in j2k)
                   for x in cv):
                cel_rossz += 1
                if len(cel_minta) < 12:
                    cel_minta.append('%s -> %s (Károli: %s)' % (
                        v, c, '/'.join('/'.join(kjv_to_karoli(x)) or '—' for x in cv[:1])))
    print('# B3. Céloldal: a motívum-versek mai >=%d TSK-találatai: %d cél, ebből eltérő számozású versre mutat: %d'
          % (KUSZOB, cel_ossz, cel_rossz))
    for x in cel_minta:
        print('  ' + x)
    print('proveniencia: scope=elofordulasok.tsv versei, Votes>=%d | forras=TSK_kereszthivatkozasok.tsv+Karoli_versmegfeleltetes.tsv | n=%d | ts=%s'
          % (KUSZOB, cel_ossz, ts))
    print()

    # --- C. jeloltek ---------------------------------------------------------
    jel = tsv(os.path.join(ADAT, 'jeloltek.tsv'))
    c_sorok = []
    for r in jel:
        fk = r.get('forras_kereses', '')
        if 'TSK' not in fk:
            continue
        versek = kibont(r['igehely']) or []
        cel_rossz = [v for v in versek if v in elter_karoli or (v in j2k and j2k[v] != [v])
                     or (konyv_cv(v) and konyv_cv(v)[0] in osz_konyvek and v not in j2k)]
        # forrásvers(ek) a forras_kereses mezőből: 'TSK <igehely>[, c:v]'
        forras_rossz = []
        m = re.search(r'TSK(?:/Károli-KH)? ([^\s;(]+ [\d:,\s\-]+?)(?:\s*\(|;|$)', fk)
        if m:
            for v in kibont(m.group(1).strip().rstrip(',')) or []:
                if v in elter_karoli:
                    forras_rossz.append(v)
        if cel_rossz or forras_rossz:
            c_sorok.append({'id': r['id'], 'igehely': r['igehely'], 'dontes': r['dontes'],
                            'cel_elter': ';'.join(cel_rossz), 'forras_elter': ';'.join(forras_rossz),
                            'cel_karoli_valojaban': ';'.join(
                                '/'.join(kjv_to_karoli(v)) or '—' for v in cel_rossz),
                            'forras_kereses': fk[:120]})
    tsk_jel = [r for r in jel if 'TSK' in r.get('forras_kereses', '')]
    print('# C. jeloltek.tsv')
    print('TSK-eredetű jelölt: %d; ebből eltérő számozású cél- vagy forrásvers: %d' % (len(tsk_jel), len(c_sorok)))
    dd = {}
    for x in c_sorok:
        dd[x['dontes']] = dd.get(x['dontes'], 0) + 1
    print('  döntés szerint: %s' % dd)
    for x in c_sorok:
        print('  %s\t%s\t%s\tcél_elt=%s\tforrás_elt=%s\t-> KJV-ként olvasva Károli: %s'
              % (x['id'], x['igehely'], x['dontes'], x['cel_elter'], x['forras_elter'], x['cel_karoli_valojaban']))
    print('proveniencia: scope=jeloltek.tsv TSK-eredetű sorai | forras=jeloltek.tsv+Karoli_versmegfeleltetes.tsv | n=%d | ts=%s'
          % (len(tsk_jel), ts))

    # TSK-proveniencijú elofordulasok-sorok
    print()
    print('# C2. elofordulasok.tsv TSK-említésű sorai (kapcsolodas/proveniencia/azonositas_modja)')
    for r in elof:
        if 'TSK' in r.get('proveniencia', '') + r.get('azonositas_modja', '') + r.get('igazolas', ''):
            versek = kibont(r['igehely']) or []
            el = [v for v in versek if v in elter_karoli]
            print('  %s\t%s\teltérő vers: %s' % (r['id'], r['igehely'], ';'.join(el) or '—'))

    # részletes kimenet
    with open(os.path.join(a.kimenet, 'B_elofordulas_versek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        mezok = list(reszlet[0].keys()) if reszlet else []
        f.write('\t'.join(mezok) + '\n')
        for x in reszlet:
            f.write('\t'.join(str(x[k]) for k in mezok) + '\n')
    with open(os.path.join(a.kimenet, 'C_jeloltek.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        mezok = ['id', 'igehely', 'dontes', 'cel_elter', 'forras_elter', 'cel_karoli_valojaban', 'forras_kereses']
        f.write('\t'.join(mezok) + '\n')
        for x in c_sorok:
            f.write('\t'.join(x[k] for k in mezok) + '\n')
    print()
    print('részletes kimenet: %s' % a.kimenet)
    if nem_bonthato:
        print('nem bontható igehelyek (%d): %s' % (len(nem_bonthato), '; '.join('%s %s' % x for x in nem_bonthato[:20])))


if __name__ == '__main__':
    main()
