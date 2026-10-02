#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
macula_futtat.py -- F17: a Macula (heber + gorog) importjanak futtatoja.

Bemenet (ket helyi klon, --heber / --gorog):
  Clear-Bible/macula-hebrew  WLC/lowfat/*-lowfat.xml   (CC BY 4.0, Biblica)
  Clear-Bible/macula-greek   Nestle1904/tsv, SBLGNT/tsv (CC BY 4.0, Biblica)
Kimenet:
  konkordancia/Macula_heber_<Konyv>.tsv   (39 fajl, F17.9) morfema-szintu sorok, Strong + Karoli-kulcs (KK)
  konkordancia/Macula_gorog.tsv   szo-szintu sorok (N1904 + SBLGNT), Strong + Karoli-kulcs
  naplok/F17_illesztetlen.tsv     az illesztetlen versek / Strong-szamok listaja (javaslat)
  naplok/F17_87_hely.tsv          a #8 ellenorzo szama: a 87 fuggo hely LXX-megfeleloje
  naplok/F17_import_stat.json     a futas szamai (a naplo forrasa)

NEM importalt mezok: a heber `sdbh`, `lexdomain`, `coredomain`, `contextualdomain`,
`sensenumber` es a gorog `domain`, `ln` (UBS MARBLE/SDBH: "Used with permission", nem CC BY);
tovabba mandarin, transliteration, frame, participantref, subjref, referent.

Futtatas: python eszkozok/f17/macula_futtat.py --heber <klon> --gorog <klon>
"""

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import macula_kozos as K  # noqa: E402
import macula_kk  # noqa: E402
import macula_import as M  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

PARANCS = 'python eszkozok/f17/macula_futtat.py --heber <klon> --gorog <klon>'


def strong_szam(x):
    m = re.search(r'(\d+)', x or '')
    return int(m.group(1)) if m else None


def fut(args):
    usfm_mag, usfm_step, mag_usfm, kanoni = K.konyvtablak()
    szotar = M.szotar_strongok()
    karoli_v = K.karoli_versek()
    illesztetlen = []

    # ---------- HEBER ----------
    hsha = M.git_sha(args.heber)
    lista = M.heber_sorok(os.path.join(args.heber, 'WLC', 'lowfat'), usfm_mag)
    mt_versek = {}
    for nn_, fn_, a_ in lista:
        m_ = M.REF_RE.match(a_.get('ref', ''))
        if m_:
            mt_versek.setdefault(usfm_mag[K.USFM_OSZ[nn_ - 1]], set()).add((int(m_.group(2)), int(m_.group(3))))
    ki_kk, kk_stat, kk_utk = macula_kk.karoli_mt_terkep(mt_versek)
    inv = macula_kk.mt_karoli_index(ki_kk)
    kezi_fej = kk_stat.pop('kezi_fejezetek', [])
    stat = {'kk': kk_stat, 'kk_terkep_kk_eltérés': len(kk_utk)}
    funkcio_alapok = M.funkcio_alapok_gyujt(lista)
    heber = []
    konyv_elteres = 0
    hiba_ref = 0
    versek_macula = defaultdict(int)
    strong_db = Counter()
    strong_pelda = {}
    allapot_db = Counter()
    sill_db = Counter()
    fedett_karoli = set()
    szavak_vers = defaultdict(list)     # (mag, fej, v) -> [(strong_szam, szo, gorog, gorog_strong)]
    for nn, fn, a in lista:
        m = M.REF_RE.match(a.get('ref', ''))
        if not m:
            hiba_ref += 1
            continue
        usfm = K.USFM_OSZ[nn - 1]
        if m.group(1) != usfm:
            konyv_elteres += 1
        mag = usfm_mag[usfm]
        mtk = (mag, int(m.group(2)), int(m.group(3)))
        versek_macula[mtk] += 1
        karoli, mod, allapot = M.kk_ertek(inv.get(mtk))
        for kk, e in inv.get(mtk, []):
            fedett_karoli.add(kk)
        strong, sill = M.strong_feldolgoz(a.get('strongnumberx', ''), 'H', a.get('pos', ''), szotar, True, funkcio_alapok)
        sill_db[sill] += 1
        if sill != 'igen':
            kulcs = ('heber', a.get('strongnumberx', '') or '-', a.get('pos', ''), sill)
            strong_db[kulcs] += 1
            strong_pelda.setdefault(kulcs, (a['ref'], a['_szoveg'], a.get('gloss', '')))
        allapot_db[allapot.split(':')[0]] += 1
        gs = M.strong_ertek(a.get('greekstrong', ''), 'G')[0]
        heber.append([a['xml_id'], a['ref'], karoli, mod, allapot, a['_szoveg'], a.get('lemma', ''), strong,
                      a.get('strongnumberx', ''), sill, a.get('morph', ''), a.get('pos', ''), a.get('gloss', ''),
                      a.get('greek', ''), gs])
        szavak_vers[mtk].append((strong_szam(a.get('strongnumberx', '')), a['_szoveg'],
                                 a.get('greek', ''), a.get('greekstrong', '')))
    for kulcs, db in sorted(versek_macula.items()):
        if not inv.get(kulcs):
            illesztetlen.append(('macula_vers_nincs_karoli', 'heber', '%s %d:%d' % kulcs, '', '', db,
                                 'a KK/terkep alapjan nincs Karoli-megfelelo', ''))
    for kulcs in sorted(ki_kk):
        if kulcs not in fedett_karoli:
            e = ki_kk[kulcs]
            illesztetlen.append(('karoli_vers_nincs_macula', 'heber',
                                 ';'.join('%s %d:%d' % (kulcs[0], f, v) for f, v in e['mt']),
                                 M.karoli_cimke(kulcs), '', 0,
                                 'a KK szerinti MT-vers nincs a Maculaban / nincs igazolt MT-megfelelo (%s%s)' % (e['forras'], (': ' + e['ok']) if e['ok'] else ''), ''))
    kk_nelkuli = 0
    for konyv in kanoni[:39]:
        for (fej, v) in sorted(karoli_v.get(konyv, ())):
            if (konyv, fej, v) not in ki_kk:
                illesztetlen.append(('karoli_vers_nincs_macula', 'heber', '', M.karoli_cimke((konyv, fej, v)), '', 0,
                                     'a KK nem osztalyozza (EGYIK_SEM fejezet) es a terkepben sincs', ''))
                kk_nelkuli += 1
    fejl = M.fejlec_sorok(M.HEBER_URL, 'commit ' + hsha, 'CC BY 4.0 (Biblica, Inc); l. naplok/F17_import_naplo.md',
                          PARANCS, 'sorok: morfema-szint (lowfat <w>); ref = Macula (MT/WLC) szamozas; '
                          'karoli = KK-alapu Karoli-vers(ek), ;-vel elvalasztva')
    heber_fajlok = M.tsv_ir_konyvenkent(K.KONK, fejl, M.HEBER_OSZLOP, heber)
    stat['heber'] = {'sorok': len(heber), 'fajlok': dict(heber_fajlok), 'lowfat_w': len(lista), 'commit': hsha, 'allapot': dict(allapot_db),
                     'strong_illesztes': dict(sill_db), 'macula_versek': len(versek_macula),
                     'macula_versek_karolival': sum(1 for k in versek_macula if inv.get(k)),
                     'karoli_versek_kk_szerint': len(ki_kk), 'karoli_versek_macula_nelkul': len(ki_kk) - len(fedett_karoli),
                     'karoli_versek_kk_nelkul': kk_nelkuli,
                     'konyvkod_elteres': konyv_elteres, 'ref_hiba': hiba_ref}

    M.tsv_ir(os.path.join(K.REPO, 'naplok', 'F17_kezi_fejezetek.tsv'),
             ['GENERÁLT: eszkozok/f17/macula_futtat.py — kézzel nem szerkesztendő.',
              'proveniencia: scope=a KK KEZI-osztalyu sorai altal erintett KJV-fejezetek | forras=konkordancia/Karoli_versmegfeleltetes.tsv, naplok/KAROLI_KK1b_fejezetosztaly.tsv (kjv_max), Macula heber (MT-versszam) | ts=%s' % M.ma(),
              'az igazolt_mt_vers_db / nem_igazolt_mt_vers_db az MT-CELVERSEKET szamolja (egy Karoli-vers tobb MT-verset is kaphat: Pred 2:26 = MT 2:25+2:26, ezert 250 igazolt MT-vers vs. 249 igazolt kk_kjv Karoli-vers); a kezi_sor_db a KEZI-sorok szama fejezetenkent',
              'a kk_kjv kotes csak ott iranyado, ahol az elozo fejezet KJV- es MT-versszama azonos (elozo_kulonbseg=0) es a vers mindket oldalon letezik; egyebkent javaslat (nincs MT-megfelelo)'],
             ['konyv', 'kjv_fejezet', 'kjv_versszam', 'mt_versszam', 'elozo_fejezet_kulonbseg', 'kezi_sor_db',
              'igazolt_mt_vers_db', 'nem_igazolt_mt_vers_db', 'allapot'],
             [[r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], 'igazolt' if r[7] == 0 else 'javaslat'] for r in kezi_fej])

    # ---------- GOROG ----------
    vt_fej, vt_sorok = K.tsv_olvas(os.path.join(K.KONK, 'Verzifikacios_elteres_tabla.tsv'))
    step_usfm = {v: k for k, v in usfm_step.items()}
    nt_kiv = {}
    for s in vt_sorok:
        k = re.match(r'^(\S+) (\d+):(\d+)$', s[2])
        for oszlop in (0, 1):
            m = re.match(r'^(\w+)\.(\d+)\.(\d+)$', s[oszlop])
            if m and k and m.group(1) in step_usfm:
                nt_kiv[(usfm_mag[step_usfm[m.group(1)]], int(m.group(2)), int(m.group(3)))] = (
                    k.group(1), int(k.group(2)), int(k.group(3)))
    gsha = M.git_sha(args.gorog)
    gorog = []
    gfedett = defaultdict(set)
    gstat = {}
    for kiadas, alk, fnev in (('N1904', 'Nestle1904', 'macula-greek-Nestle1904.tsv'),
                              ('SBLGNT', 'SBLGNT', 'macula-greek-SBLGNT.tsv')):
        ix, sorok = M.gorog_sorok(os.path.join(args.gorog, alk, 'tsv', fnev))
        allapot_g = Counter()
        sill_g = Counter()
        versek_g = defaultdict(int)
        gk = 0
        for s in sorok:
            m = M.REF_RE.match(s[ix['ref']])
            if not m or m.group(1) not in mag_usfm.values():
                gk += 1
                continue
            mag = usfm_mag[m.group(1)]
            fej, v = int(m.group(2)), int(m.group(3))
            vk = (mag, fej, v)
            versek_g[vk] += 1
            if (fej, v) in karoli_v.get(mag, ()):
                cel, mod, allapot = vk, 'identitas', 'rendben'
            elif vk in nt_kiv:
                cel, mod, allapot = nt_kiv[vk], 'verzifikacios_tabla', 'javaslat:verzifikacios_tabla'
            else:
                cel, mod, allapot = None, 'nincs', 'javaslat:nincs_karoli_vers'
            if cel:
                gfedett[kiadas].add(cel)
            strong, sill = M.strong_feldolgoz(s[ix['strong']], 'G', s[ix['class']], szotar, False)
            sill_g[sill] += 1
            allapot_g[allapot.split(':')[0]] += 1
            if sill != 'igen':
                kulcs = ('gorog_' + kiadas, s[ix['strong']] or '-', s[ix['class']], sill)
                strong_db[kulcs] += 1
                strong_pelda.setdefault(kulcs, (s[ix['ref']], s[ix['text']], s[ix['gloss']]))
            gorog.append([kiadas, s[ix['xml:id']], s[ix['ref']], M.karoli_cimke(cel) if cel else '', mod, allapot,
                          s[ix['text']], s[ix['lemma']], strong, s[ix['strong']], sill, s[ix['morph']], s[ix['class']],
                          s[ix['gloss']], s[ix['english']]])
        for vk, db in sorted(versek_g.items()):
            if not ((vk[1], vk[2]) in karoli_v.get(vk[0], ()) or vk in nt_kiv):
                illesztetlen.append(('macula_vers_nincs_karoli', 'gorog_' + kiadas, '%s %d:%d' % vk, '', '', db,
                                     'a Karoli-szovegben nincs ilyen vers', ''))
        gstat[kiadas] = {'sorok': len(sorok), 'allapot': dict(allapot_g), 'strong_illesztes': dict(sill_g),
                         'versek': len(versek_g), 'ref_hiba': gk}
    for kulcs, db in sorted(strong_db.items(), key=lambda x: tuple(map(str, x[0]))):
        pelda = strong_pelda[kulcs]
        illesztetlen.append(('strong_nem_illesztheto', kulcs[0], pelda[0], '', kulcs[1], db,
                             kulcs[3].replace('javaslat:', ''),
                             '%s | %s | %s' % (kulcs[2], pelda[1], pelda[2])))
    nt_karoli_nincs = Counter()
    for mag in kanoni[39:]:
        for (fej, v) in sorted(karoli_v.get(mag, ())):
            for kiadas in ('N1904', 'SBLGNT'):
                if (mag, fej, v) not in gfedett[kiadas]:
                    illesztetlen.append(('karoli_vers_nincs_macula', 'gorog_' + kiadas, '',
                                         M.karoli_cimke((mag, fej, v)), '', 0,
                                         'a Karoli-vers nincs a Macula-kiadasban (azonos szamozassal)', ''))
                    nt_karoli_nincs[kiadas] += 1
    for kiadas in gstat:
        gstat[kiadas]['karoli_versek_macula_nelkul'] = nt_karoli_nincs[kiadas]
    stat['gorog'] = gstat
    stat['gorog_commit'] = gsha
    fejl = M.fejlec_sorok(M.GOROG_URL, 'commit ' + gsha, 'CC BY 4.0 (Biblica, Inc); l. naplok/F17_import_naplo.md',
                          PARANCS, 'sorok: szo-szint; kiadas = N1904 (Nestle 1904) | SBLGNT; ref = Macula; '
                          'karoli = Karoli-vers (ÚSZ: azonos szamozas, 8 verzifikacios kivetellel)')
    M.tsv_ir(os.path.join(K.KONK, 'Macula_gorog.tsv'), fejl, M.GOROG_OSZLOP, gorog)

    # ---------- illesztetlen ----------
    ill_oszlop = ['tipus', 'nyelv', 'igehely_macula', 'igehely_karoli', 'strong', 'sorok', 'ok', 'pelda', 'allapot']
    M.tsv_ir(os.path.join(K.REPO, 'naplok', 'F17_illesztetlen.tsv'),
             ['GENERÁLT: eszkozok/f17/macula_futtat.py — kézzel nem szerkesztendő.',
              'proveniencia: scope=Macula heber+gorog import illesztetlen elemei | forras=%s ; %s | ts=%s' % (
                  M.HEBER_URL, M.GOROG_URL, M.ma()),
              'minden sor allapota: javaslat (D19); strong_nem_illesztheto: Strong-szamonkent osszesitve (sorok = elofordulasok)'],
             ill_oszlop, [[str(x) for x in r] + ['javaslat'] for r in illesztetlen])
    stat['illesztetlen'] = dict(Counter((r[0], r[1]) for r in illesztetlen).most_common())
    stat['illesztetlen'] = {'%s|%s' % k: v for k, v in Counter((r[0], r[1]) for r in illesztetlen).items()}

    # ---------- a 87 fuggo hely (a #8 ellenorzo szama) ----------
    munka = os.path.join(K.REPO, 'naplok', 'FORRAS_FJ1_lxx_jeloltek.tsv')
    mfej, msorok = K.tsv_olvas(munka)
    mix = {n: mfej.index(n) for n in ('motivum', 'igehely', 'heber_kulcsszo', 'heber_strong')}
    f06fej, f06sorok = K.tsv_olvas(os.path.join(K.REPO, 'naplok', 'F06_macula_87_hely.tsv'))
    f06 = {(s[0], s[1]): s[4] for s in f06sorok}
    ki87 = []
    all87 = Counter()
    kulonbseg = 0
    for s in msorok:
        motivum, igehely = s[mix['motivum']], s[mix['igehely']]
        kulcsszo, munka_strong = s[mix['heber_kulcsszo']], s[mix['heber_strong']]
        m = re.match(r'^(\S+)\s+(\d+):(\d+)', igehely)
        mtv, mod = '', ''
        allapot, azon, hszo, glemma, gstrong, megj = '', '', '', '', '', ''
        szavak = []
        if not m:
            allapot = 'IGEHELY_NEM_ERTELMEZHETO'
        else:
            kulcs = (m.group(1), int(m.group(2)), int(m.group(3)))
            e = ki_kk.get(kulcs)
            if not e or not e['mt']:
                allapot = 'NINCS_VERS'
                megj = 'a KK/terkep szerint nincs MT-megfelelo'
            else:
                mod = e['forras'] + ('' if e['biz'] == 'rendben' else ':' + e['ok'])
                mtv = ';'.join('%d:%d' % x for x in e['mt'])
                for x in e['mt']:
                    szavak.extend(szavak_vers.get((kulcs[0], x[0], x[1]), []))
                if not szavak:
                    allapot = 'NINCS_VERS'
                    megj = 'az MT-vers nincs a Maculaban'
        if szavak:
            cel_strong = strong_szam(munka_strong) if munka_strong else None
            alak = M.alap_alak(kulcsszo.split('(')[0])
            talalt = []
            if cel_strong is not None:
                talalt = [w for w in szavak if w[0] == cel_strong]
                azon = 'strong'
            if not talalt and alak:
                talalt = [w for w in szavak if M.alap_alak(w[1]) == alak]
                azon = 'szoalak' if talalt else ''
            if not talalt:
                allapot = 'HEBER_SZO_NINCS_A_VERSBEN'
            else:
                hszo = '|'.join(w[1] for w in talalt)
                glemma = '|'.join(w[2] or '-' for w in talalt)
                gstrong = '|'.join(w[3] or '-' for w in talalt)
                van = [w for w in talalt if w[3]]
                allapot = 'LXX_MEGFELELO' if van else 'HEBER_SZO_GOROG_NELKUL'
                if len({w[3] for w in van}) > 1:
                    megj = 'tobb heber talalat, eltero gorog Strong'
        all87[allapot] += 1
        r06 = f06.get((motivum, igehely), '')
        if r06 != allapot:
            kulonbseg += 1
        ki87.append([motivum, igehely, mtv, mod, kulcsszo, munka_strong, allapot, azon, hszo, glemma, gstrong, r06,
                     'igen' if r06 == allapot else 'nem', megj])
    M.tsv_ir(os.path.join(K.REPO, 'naplok', 'F17_87_hely.tsv'),
             ['GENERÁLT: eszkozok/f17/macula_futtat.py — kézzel nem szerkesztendő.',
              'proveniencia: scope=87 fuggo LXX-hely (naplok/FORRAS_FJ1_lxx_jeloltek.tsv) | forras=%s@%s | ts=%s' % (
                  M.HEBER_URL, hsha, M.ma()),
              'a Karoli-szamozasu igehely -> MT-vers a KK alapjan (igehely_mt, KEZI osztalynal igehely_kjv; F06-ban ez a lepes hianyzott). Az `allapot` oszlop a gepi kereses kimenete (nem dontes): a LXX_MEGFELELO sorok gepi javaslatok, kezi megerositest kernek (az F06 szerint a Macula szo-szintu illesztese 78,3%). A `kk_mod` `:`-os utotagja a KK-kotes bizonytalansaga.',
              'sorok=%d ; %s' % (len(ki87), ', '.join('%s=%d' % kv for kv in sorted(all87.items())))],
             ['motivum', 'igehely_karoli', 'igehely_mt', 'kk_mod', 'heber_kulcsszo', 'heber_strong_munkalap', 'allapot',
              'azonositas', 'macula_heber_szo', 'macula_gorog', 'macula_gorog_strong', 'f06_allapot', 'egyezik_f06',
              'megjegyzes'], ki87)
    stat['hely87'] = {'sorok': len(ki87), 'allapot': dict(all87), 'f06_eltero_sor': kulonbseg}
    with open(os.path.join(K.REPO, 'naplok', 'F17_import_stat.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(stat, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write('\n')
    return stat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--heber', required=True)
    ap.add_argument('--gorog', required=True)
    args = ap.parse_args()
    stat = fut(args)
    print(json.dumps(stat, ensure_ascii=False, indent=1, sort_keys=True))


if __name__ == '__main__':
    main()
