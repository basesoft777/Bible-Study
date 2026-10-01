#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.47 — a prompt_v3 / prompt_v2 hosszarány (R) pontos definíciója és számítása.

DEFINÍCIÓ (a naplok/F21P_hosszarany.md és a f21p/hosszarany.tsv ezt írja):

    R = Σ_k L_v3(k) / Σ_k L_v2(k)

ahol k a 200 verses minta 20 kötegének (10 vers/köteg, a minta.tsv sorrendjében) egyike, és
L_v(k) a k. köteg ELSŐ PRÓBÁLKOZÁSÁNAK TELJES bemeneti üzenete a prompt_v (v = v2 ill. v3)
szerint: a prompt utasításrésze (a PROMPT-KEZDET/VÉGE jelölők között, a példaversblokkok
kibontásával) + a keret („=== A FELDOLGOZANDÓ VERSEK (n) ===”) + az összes versblokk,
pontosan ahogy a bemenet.kotegszoveg összeállítja, KJV-támponttal a minta szerint (kjv=True).
Az L mértékegysége a KARAKTER (Unicode kódpont, Python len(str)); mellette az UTF-8 BÁJTSZÁM is
(a héber/görög/magyar szöveg miatt a kettő eltér). A két arány külön: R (karakter), R (bájt).
A versblokkok összhossza a két prompttal azonos; a különbség kizárólag az utasításrészből jön.

Nincs hálózat, nincs titok. Kimenet: f21p/hosszarany.tsv (gépi, proveniencia-fejléc) és
naplok/F21P_hosszarany.md (generált).
    python eszkozok/karoli_strong/hosszarany.py [--onteszt]
"""

import argparse
import hashlib
import os
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bemenet  # noqa: E402
import tokenek  # noqa: E402

F21P = os.path.join(tokenek.ROOT, 'f21p')
MINTA_UT = os.path.join(F21P, 'minta.tsv')
TSV_UT = os.path.join(F21P, 'hosszarany.tsv')
MD_UT = os.path.join(tokenek.ROOT, 'naplok', 'F21P_hosszarany.md')
KOTEG = 10
# A törölt ág (claude/f21-regresszio) prompt_v3-jával mért 20 köteg összhossza: MANUAL, koordinátori közlés
# (nem ebből a repóból számolt; az ág törölve van). Az 1.0491 arány ennek és a v2 összhosszának hányadosa.
TOROLT_AG_OSSZ_KARAKTER = 317730
TOROLT_AG_ARANY = 1.0491


def igehelyek(minta_ut=None):
    with open(minta_ut or MINTA_UT, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip()]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t')))['igehely'] for s in sorok[1:]]


def mereres(ig_all, prompt_ut, kjv=True):
    """Egy prompt mérése a kötegekre. Visszaad: dict (karakter és bájt: utasítás, versblokkok, keret, összes)."""
    kotegek = bemenet.kotegek(ig_all, KOTEG)
    utas = bemenet.prompt_utasitas(prompt_ut)
    o_k = o_b = vb_k = vb_b = ut_k = ut_b = 0
    for k in kotegek:
        uzenet = bemenet.kotegszoveg(k, kjv, prompt_ut)
        blokk = '\n\n'.join(bemenet.versblokk(ig, kjv) for ig in k)
        o_k += len(uzenet)
        o_b += len(uzenet.encode('utf-8'))
        vb_k += len(blokk)
        vb_b += len(blokk.encode('utf-8'))
        ut_k += len(utas)
        ut_b += len(utas.encode('utf-8'))
    return {'kotegek': len(kotegek), 'utasitas_k': ut_k, 'utasitas_b': ut_b, 'versblokk_k': vb_k, 'versblokk_b': vb_b,
            'keret_k': o_k - ut_k - vb_k, 'keret_b': o_b - ut_b - vb_b, 'osszes_k': o_k, 'osszes_b': o_b,
            'utasitas_egy_k': len(utas), 'utasitas_egy_b': len(utas.encode('utf-8')),
            'sha12': hashlib.sha256(utas.encode('utf-8')).hexdigest()[:12]}


def szamol(ig_all=None, v2_ut=None, v3_ut=None, kjv=True):
    """{'v2': mérés, 'v3': mérés, 'R_k', 'R_b'}; az R a definíció szerint."""
    ig_all = ig_all or igehelyek()
    m2 = mereres(ig_all, v2_ut or bemenet.PROMPT_V2_UT, kjv)
    m3 = mereres(ig_all, v3_ut or bemenet.PROMPT_V3_UT, kjv)
    return {'v2': m2, 'v3': m3, 'R_k': m3['osszes_k'] / m2['osszes_k'], 'R_b': m3['osszes_b'] / m2['osszes_b']}


def sorok_keszit(r):
    m2, m3 = r['v2'], r['v3']
    ki = [['mero', 'v2', 'v3', 'megjegyzes'],
          ['prompt_sha256_12 (utasításrész)', m2['sha12'], m3['sha12'], 'a futásnapló prompt_sha256_12 oszlopa'],
          ['kotegek_szama', m2['kotegek'], m3['kotegek'], '10 vers/köteg, a minta.tsv sorrendjében'],
          ['utasitasresz_karakter (1 köteg)', m2['utasitas_egy_k'], m3['utasitas_egy_k'], 'példaversblokkokkal kibontva'],
          ['utasitasresz_bajt (1 köteg)', m2['utasitas_egy_b'], m3['utasitas_egy_b'], 'UTF-8'],
          ['utasitasresz_karakter (20 köteg)', m2['utasitas_k'], m3['utasitas_k'], ''],
          ['versblokkok_karakter (20 köteg)', m2['versblokk_k'], m3['versblokk_k'], 'azonos a két prompttal'],
          ['keret_karakter (20 köteg)', m2['keret_k'], m3['keret_k'], '„=== A FELDOLGOZANDÓ VERSEK (n) ===” és a sortörések'],
          ['osszhossz_karakter (20 köteg)', m2['osszes_k'], m3['osszes_k'], 'L = Σ_k az első próbálkozás teljes bemeneti üzenete'],
          ['osszhossz_bajt (20 köteg)', m2['osszes_b'], m3['osszes_b'], 'UTF-8 bájt'],
          ['R_karakter', '', '%.4f' % r['R_k'], 'R = Σ L_v3 / Σ L_v2 (Unicode kódpont)'],
          ['R_bajt', '', '%.4f' % r['R_b'], 'R = Σ L_v3 / Σ L_v2 (UTF-8 bájt)'],
          ['utasitasresz_hozzajarulas_a_kulonbsegnek', '', '%.1f%%' % (100 * (m3['utasitas_k'] - m2['utasitas_k']) / (m3['osszes_k'] - m2['osszes_k'])),
           'a v3 − v2 összhossz-különbség ennyi százaléka az utasításrészből jön (a versblokkok azonosak)'],
          ['torolt_ag_v3_osszhossz_karakter', '', TOROLT_AG_OSSZ_KARAKTER,
           'MANUAL (koordinátori közlés): a törölt ág (claude/f21-regresszio) rövidebb prompt_v3-ja; nem ebből a repóból számolt'],
          ['torolt_ag_arany', '', TOROLT_AG_ARANY, 'MANUAL (koordinátori közlés)'],
          ['kulonbseg_a_torolt_aghoz_karakter', '', m3['osszes_k'] - TOROLT_AG_OSSZ_KARAKTER, 'a mi v3 − a törölt ág v3 (20 köteg)'],
          ['kulonbseg_kotegenkent_karakter', '', '%.0f' % ((m3['osszes_k'] - TOROLT_AG_OSSZ_KARAKTER) / m3['kotegek']), 'a prompt különbsége kötegenként']]
    return [[str(x) for x in s] for s in ki]


def fejlec(ts, r):
    return ('GENERÁLT: eszkozok/karoli_strong/hosszarany.py | scope=a prompt_v3/prompt_v2 hosszarány (R = Σ L_v3 / Σ L_v2, a 20 köteg első '
            'próbálkozásának teljes bemeneti üzenete, KJV a minta szerint), 200 verses minta, v2 sha %s, v3 sha %s | '
            'forras=f21p/prompt_v2.md, f21p/prompt_v3.md, f21p/minta.tsv, konkordancia/Karoli_1908.tsv, konkordancia/TAHOT_kivonat.tsv, '
            'konkordancia/TAGNT_kivonat.tsv, konkordancia/KJV_Strongs_*.tsv; a törölt ág értékei MANUAL (koordinátori közlés) | '
            'ts=%s (a generálás ideje; ismételt futáskor csak ez a sor tér el) | kézzel szerkeszteni tilos'
            % (r['v2']['sha12'], r['v3']['sha12'], ts))


def kiir(r, tsv_ut, md_ut, ts):
    sorok = sorok_keszit(r)
    fej = fejlec(ts, r)
    with open(tsv_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# ' + fej + '\n')
        for s in sorok:
            assert all('\t' not in x for x in s)
            f.write('\t'.join(s) + '\n')
    m2, m3 = r['v2'], r['v3']
    md = ['# F21P_hosszarany.md — a prompt_v3 / prompt_v2 hosszarány (R)', '', '<!-- %s -->' % fej, '',
          '## Definíció', '',
          '**R = Σ_k L_v3(k) / Σ_k L_v2(k)**, ahol k a 200 verses minta 20 kötegének (10 vers/köteg) egyike, és L(k) a k. köteg '
          '**első próbálkozásának teljes bemeneti üzenete**: a prompt utasításrésze (a példaversblokkokkal kibontva) + a keret + az '
          'összes versblokk, ahogy a `bemenet.kotegszoveg` összeállítja, KJV-támponttal a minta szerint. L = **karakterszám '
          '(Unicode kódpont)**; mellette az **UTF-8 bájtszám** (a héber/görög/magyar szöveg miatt a kettő eltér).', '',
          '## Eredmény (a befagyasztott promptokra)', '',
          '| mérőszám | v2 (%s) | v3 (%s) |' % (m2['sha12'], m3['sha12']), '|---|---|---|',
          '| utasításrész, 1 köteg (karakter) | %d | %d |' % (m2['utasitas_egy_k'], m3['utasitas_egy_k']),
          '| utasításrész, 1 köteg (bájt) | %d | %d |' % (m2['utasitas_egy_b'], m3['utasitas_egy_b']),
          '| utasításrész, 20 köteg (karakter) | %d | %d |' % (m2['utasitas_k'], m3['utasitas_k']),
          '| versblokkok, 20 köteg (karakter) | %d | %d |' % (m2['versblokk_k'], m3['versblokk_k']),
          '| keret, 20 köteg (karakter) | %d | %d |' % (m2['keret_k'], m3['keret_k']),
          '| **összhossz, 20 köteg (karakter)** | **%d** | **%d** |' % (m2['osszes_k'], m3['osszes_k']),
          '| összhossz, 20 köteg (bájt) | %d | %d |' % (m2['osszes_b'], m3['osszes_b']), '',
          '**R (karakter) = %.4f; R (UTF-8 bájt) = %.4f.** A versblokkok összhossza a két prompttal azonos (%d karakter); a '
          'különbség (%d karakter) kizárólag az utasításrészből jön (%d karakter/köteg).' % (
              r['R_k'], r['R_b'], m3['versblokk_k'], m3['osszes_k'] - m2['osszes_k'], m3['utasitas_egy_k'] - m2['utasitas_egy_k']), '',
          '## A törölt ág 1,0491-es értéke', '',
          'A törölt ág (`claude/f21-regresszio`) 1,0491-et mért (MANUAL, koordinátori közlés). Ennek oka **nem a definíció, hanem a prompt**: '
          'az ő prompt_v3-ja rövidebb volt (a 20 köteg összhossza %d karakter), a mienk a befagyasztott prompt_v3 (%d karakter). '
          'A különbség %d karakter, azaz kötegenként ~%.0f karakter. A v2 összhossza (%d) ugyanaz, így a két arány a prompt eltéréséből adódik; '
          'a pilot aranya és promptja a befagyasztott (R = %.4f). A szárazbecslés (`futtat.py --szaraz`) ezt az R-t használja.' % (
              TOROLT_AG_OSSZ_KARAKTER, m3['osszes_k'], m3['osszes_k'] - TOROLT_AG_OSSZ_KARAKTER,
              (m3['osszes_k'] - TOROLT_AG_OSSZ_KARAKTER) / m3['kotegek'], m2['osszes_k'], r['R_k']), '']
    with open(md_ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(md) + '\n')


def onteszt():
    hibak = []

    def ellen(f, leiras):
        if not f:
            hibak.append(leiras)
    # szintetikus promptok: ismert hosszak, nem ASCII karakterekkel (a bájt ≠ karakter)
    mappa = tempfile.mkdtemp(prefix='f21p_onteszt_hosszarany_')
    try:
        def prompt(ut, szoveg):
            with open(ut, 'w', encoding='utf-8', newline='\n') as f:
                f.write('fej\n%s\n%s\n%s\nláb\n' % (bemenet.KEZDET, szoveg, bemenet.VEGE))
            return ut
        p2 = prompt(os.path.join(mappa, 'p2.md'), 'űáé' * 10)         # 30 karakter, 60 bájt
        p3 = prompt(os.path.join(mappa, 'p3.md'), 'űáé' * 25)         # 75 karakter, 150 bájt
        ig = igehelyek()[:20]
        r = szamol(ig, p2, p3)
        ellen(r['v2']['utasitas_egy_k'] == 30 and r['v3']['utasitas_egy_k'] == 75
              and r['v2']['utasitas_egy_b'] == 60 and r['v3']['utasitas_egy_b'] == 150, 'az utasításrész hossza (karakter/bájt) hibás: %s' % r['v2'])
        ellen(r['v2']['versblokk_k'] == r['v3']['versblokk_k'] and r['v2']['keret_k'] == r['v3']['keret_k'],
              'a versblokk/keret hossza nem azonos a két prompttal')
        # független számítás: a teljes üzenetek összhossza
        h2 = sum(len(bemenet.kotegszoveg(k, True, p2)) for k in bemenet.kotegek(ig, 10))
        h3 = sum(len(bemenet.kotegszoveg(k, True, p3)) for k in bemenet.kotegek(ig, 10))
        ellen(r['v2']['osszes_k'] == h2 and r['v3']['osszes_k'] == h3 and abs(r['R_k'] - h3 / h2) < 1e-12, 'R (karakter) nem a definíció szerinti')
        ellen(r['v3']['osszes_b'] - r['v2']['osszes_b'] == 2 * (r['v3']['utasitas_k'] - r['v2']['utasitas_k']),
              'a bájtkülönbség nem az utasításrész bájtkülönbsége (a versblokkok azonosak)')
        ellen(r['R_k'] != r['R_b'], 'a karakter- és a bájtarány azonos (nem ASCII szövegnél eltér)')
        # keret + utasítás + versblokk = összes
        ellen(r['v3']['osszes_k'] == r['v3']['utasitas_k'] + r['v3']['versblokk_k'] + r['v3']['keret_k'], 'az összetevők összege nem az összhossz')
        # kiírás és determinizmus
        t1, m1 = os.path.join(mappa, 'a.tsv'), os.path.join(mappa, 'a.md')
        kiir(r, t1, m1, 'T1')
        t2, m2_ = os.path.join(mappa, 'b.tsv'), os.path.join(mappa, 'b.md')
        kiir(r, t2, m2_, 'T2')
        with open(t1, encoding='utf-8') as f:
            a = f.read()
        with open(t2, encoding='utf-8') as f:
            b = f.read()
        ellen(a.replace('ts=T1 ', 'ts=T2 ') == b and a.startswith('# GENERÁLT: ') and ' | forras=' in a.split('\n')[0] and ' | ts=T1 ' in a.split('\n')[0],
              'a TSV nem determinisztikus / nincs proveniencia-fejléc')
        ellen(all(len(s.split('\t')) == 4 for s in a.split('\n')[1:] if s), 'a TSV-sorok nem 4 mezősek')
    finally:
        import shutil
        shutil.rmtree(mappa, ignore_errors=True)
    # a valódi promptokra: R > 1, a versblokkok azonosak, a sha-k a naplóéi
    rv = szamol()
    ellen(rv['R_k'] > 1 and rv['v2']['versblokk_k'] == rv['v3']['versblokk_k'], 'a valódi R nem > 1 / a versblokkok eltérnek')
    ellen(rv['v3']['kotegek'] == 20 and rv['v2']['sha12'] == bemenet.prompt_sha256(bemenet.PROMPT_V2_UT)[:12]
          and rv['v3']['sha12'] == bemenet.prompt_sha256(bemenet.PROMPT_V3_UT)[:12], 'a köteg-szám / sha nem a várt')
    import p3c_mock
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'a régi kimenetek megváltoztak: %s' % p3c_mock.regi_kimenetek_hibak())
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('hosszarany önteszt rendben (szintetikus promptok: karakter ≠ bájt, független R, összetevők, determinizmus; valódi R=%.4f)' % rv['R_k'])
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--onteszt', action='store_true')
    args = ap.parse_args()
    if args.onteszt:
        return onteszt()
    r = szamol()
    kiir(r, TSV_UT, MD_UT, tokenek.generalas_ts())
    print('R (karakter) = %.4f; R (UTF-8 bájt) = %.4f; v2 %d, v3 %d karakter (20 köteg) -> %s, %s' % (
        r['R_k'], r['R_b'], r['v2']['osszes_k'], r['v3']['osszes_k'], TSV_UT, MD_UT))
    return 0


if __name__ == '__main__':
    sys.exit(main())
