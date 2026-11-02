#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
karoli_kh_epseg.py -- a `konkordancia/Karoli_kereszthivatkozasok.tsv` épségének felmérése (olvasói kapu, 4. pont).

Az átvilágítás (2026-11-02, A5/T5/G1) szerint a Károli-KH sorok egy része más vers listája: az `Act.2.27` sorai
azonosak az `Act.7.14`-ével, az `Isa.34.11`-é az `Isa.40.11`-ével. Ez az eszköz a teljes táblán méri, hány
forrásvers hordoz ilyen másolt listát. Csak olvas; adatot nem javít (a javítás: N-F156a).

Gyanús (másolt) egy forrásvers, ha
  (1) a KH-listája szó szerint megegyezik legalább egy másik forrásvers listájával, ÉS
  (2) a saját listájának egyetlen eleme sem támogatott, ÉS
  (3) a vele azonos listájú versek közül legalább egy támogatott.
Egy elem (forrás → cél) támogatott, ha a TSK a forrást a cél fejezetének ±3 vers széles környezetével köti
össze (bármely irányban), vagy a cél saját Károli-KH listája visszamutat a forrás ±3 versére.

A szabály a másolat-típusú hibát fogja meg; az egyedi, nem duplikált hibás listát (pl. ApCsel 22:16 → Jón 1:5)
nem. Ez korlát, nem negatív lelet.

Használat:
    python eszkozok/karoli_kh_epseg.py [--jelentes naplok/KAROLI_KH_EPSEG_jelentes.md] [--tsv naplok/KAROLI_KH_gyanus.tsv]
"""
import argparse
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KH = 'konkordancia/Karoli_kereszthivatkozasok.tsv'
TSK = 'konkordancia/TSK_kereszthivatkozasok.tsv'
NORM = 'konkordancia/Konyv_normalizalo_tabla.tsv'
KORNYEZET = 3


def sorok(rel):
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        ki = [s.rstrip('\n').rstrip('\r').split('\t') for s in f]
    return ki[1:]


def hu_step():
    """Magyar rövidítés -> STEPBible-rövidítés (a normalizáló táblából)."""
    return {m[1]: m[0] for m in sorok(NORM) if len(m) > 1}


def step_ref(ref):
    m = re.match(r'(\w+)\.(\d+)\.(\d+)', ref or '')
    return (m.group(1), int(m.group(2)), int(m.group(3))) if m else None


def betolt():
    """(KH-listák: forrás -> [cél], TSK-szomszédság: (könyv, fej, vers) -> {(könyv, fej, vers)})."""
    kh = collections.OrderedDict()
    for m in sorok(KH):
        if len(m) >= 2:
            kh.setdefault(m[0], []).append(m[1])
    norm = hu_step()
    tsk = collections.defaultdict(set)
    for m in sorok(TSK):
        if len(m) < 2:
            continue
        a, b = (re.match(r'(\S+) (\d+):(\d+)', x) for x in m[:2])
        if not a or not b or a.group(1) not in norm or b.group(1) not in norm:
            continue
        x = (norm[a.group(1)], int(a.group(2)), int(a.group(3)))
        y = (norm[b.group(1)], int(b.group(2)), int(b.group(3)))
        tsk[x].add(y)
        tsk[y].add(x)
    return kh, tsk


def tamogatott(forras, cel, kh, tsk):
    a = step_ref(forras)
    kezd = step_ref(cel.split('-')[0])
    veg = step_ref(cel.split('-')[-1]) or kezd
    if not a or not kezd:
        return True  # nem értelmezhető hivatkozás: nem ítélünk
    for x in tsk.get(a, ()):
        if x[0] != kezd[0] or x[1] not in (kezd[1], veg[1]):
            continue
        if kezd[1] != veg[1] or kezd[2] - KORNYEZET <= x[2] <= veg[2] + KORNYEZET:
            return True
    for vissza in kh.get('%s.%d.%d' % kezd, []):
        y = step_ref(vissza.split('-')[0])
        if y and y[0] == a[0] and y[1] == a[1] and abs(y[2] - a[2]) <= KORNYEZET:
            return True
    return False


# a lexikai támogatásnál csak az ennél kevesebb versben álló Strong számít. Kalibrálva a 9 lap 35 gyanús forrásversén
# (2026-11-02, naplok/KH_ELREJTES_igazolas.md): a valódi kapcsolatok közös szava Gézer 14, seol 64, Sion 139 vers; a
# másolatoké natah („kifeszít”) 205, mávet („halál”) 150 — ezért a határ 150 (szigorúan alatta). Kis mintán kalibrált.
RITKA_STRONG = 150
_STRONG = None


def strong_index():
    """({STEP-vers: {Strong}}, {Strong: versszám}) a TAHOT és a TAGNT kivonatból, a grammatikai Strongok nélkül.
    A TAHOT/TAGNT kulcsa a magyar igehely (Károli-vers); a STEP-alakra a normalizáló tábla fordít."""
    global _STRONG
    if _STRONG is None:
        norm = hu_step()
        gram = {m[0] for m in sorok('adat/grammatikai_strongok.tsv') if m and m[0][:1] in 'HG'}
        versek = collections.defaultdict(set)
        for rel in ('konkordancia/TAHOT_kivonat.tsv', 'konkordancia/TAGNT_kivonat.tsv'):
            for m in sorok(rel):
                if len(m) < 2:
                    continue
                r = re.match(r'(\S+) (\d+):(\d+)$', m[0])
                s = re.match(r'[HG]\d+', m[1] or '')
                if not r or not s or r.group(1) not in norm or s.group(0) in gram:
                    continue
                versek['%s.%s.%s' % (norm[r.group(1)], r.group(2), r.group(3))].add(s.group(0))
        gyak = collections.Counter(x for v in versek.values() for x in v)
        _STRONG = (versek, gyak)
    return _STRONG


def lexikai_tamogatas(forras, cel):
    """A forrásvers és a cél (a tartomány minden verse, egy fejezeten belül) közös ritka tartalmi Strong-számai.
    Ha van ilyen, a cél a forrással lexikailag is összefügg: nem lehet pusztán egy másik vers listájának másolata
    (pl. Hab 2:17 → Ézs 33:1, közös ige: „pusztít”; 1Krón 20:4 → Józs 21:21, közös név: Gézer)."""
    versek, gyak = strong_index()
    kezd = step_ref(cel.split('-')[0])
    veg = step_ref(cel.split('-')[-1]) or kezd
    if not kezd:
        return set()
    utolso = veg[2] if veg[0] == kezd[0] and veg[1] == kezd[1] else kezd[2]
    cel_strong = set()
    for v in range(kezd[2], utolso + 1):
        cel_strong |= versek.get('%s.%d.%d' % (kezd[0], kezd[1], v), set())
    return {s for s in versek.get(forras, set()) & cel_strong if gyak[s] < RITKA_STRONG}


def gyanus_forrasok(kh=None, tsk=None):
    """{forrásvers: [azonos listájú, támogatott forrásversek]} a gyanús (másolt) listákra.
    Pontosítás (az 52 lapsor kézi igazolása, 2026-11-02): nem gyanús az a lista, amelynek valamelyik eleme
    ritka tartalmi Strong-számon osztozik a forrásverssel (lexikai támogatás)."""
    if kh is None:
        kh, tsk = betolt()
    csoport = collections.defaultdict(list)
    for k, v in kh.items():
        csoport[tuple(sorted(v))].append(k)
    ki = {}
    for tagok in csoport.values():
        if len(tagok) < 2:
            continue
        tam = {k: sum(1 for c in kh[k] if tamogatott(k, c, kh, tsk)) for k in tagok}
        jo = [k for k in tagok if tam[k]]
        if not jo:
            continue
        for k in tagok:
            if not tam[k] and not any(lexikai_tamogatas(k, c) for c in kh[k]):
                ki[k] = jo
    return ki


def main():
    ap = argparse.ArgumentParser(description='A Károli-KH tábla másolt listáinak felmérése')
    ap.add_argument('--jelentes', help='Markdown-jelentés útvonala (a repó gyökeréhez képest)')
    ap.add_argument('--tsv', help='a gyanús forrásversek listája (TSV)')
    a = ap.parse_args()
    kh, tsk = betolt()
    gy = gyanus_forrasok(kh, tsk)
    csoport = collections.defaultdict(list)
    for k, v in kh.items():
        csoport[tuple(sorted(v))].append(k)
    dupl = sum(len(t) for t in csoport.values() if len(t) > 1)
    dupl2 = sum(len(t) for c, t in csoport.items() if len(t) > 1 and len(c) >= 2)
    nincs_tam = sum(1 for k in kh if not any(tamogatott(k, c, kh, tsk) for c in kh[k]))
    egy_konyv = sum(1 for k, p in gy.items() if any(step_ref(x)[0] == step_ref(k)[0] for x in p))
    sor_gy = sum(len(kh[k]) for k in gy)
    stat = [
        ('forrásvers (van KH-listája)', len(kh)),
        ('KH-sor összesen', sum(len(v) for v in kh.values())),
        ('a listája szó szerint megegyezik egy másik forrásversével', dupl),
        ('… ebből legalább kételemű listával', dupl2),
        ('egyetlen eleme sem támogatott (TSK ±3 vers, Károli-visszautalás)', nincs_tam),
        ('**gyanús (másolt) forrásvers**: duplikált + saját támogatás 0 + a pár támogatott', len(gy)),
        ('… a gyanús listák KH-sorai', sor_gy),
        ('… a támogatott pár ugyanabban a könyvben', egy_konyv),
    ]
    for n, v in stat:
        print('%s: %d' % (n.replace('**', ''), v))
    if a.tsv:
        with open(os.path.join(GYOKER, a.tsv), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# GENERÁLT: eszkozok/karoli_kh_epseg.py — kézzel szerkeszteni tilos\n')
            f.write('\t'.join(['forras', 'kh_lista', 'azonos_listaju_tamogatott']) + '\n')
            for k in kh:
                if k in gy:
                    f.write('\t'.join([k, ' '.join(kh[k]), ' '.join(gy[k])]) + '\n')
    if a.jelentes:
        with open(os.path.join(GYOKER, a.jelentes), 'w', encoding='utf-8', newline='\n') as f:
            f.write(jelentes(stat, gy, kh))
    return 0


def jelentes(stat, gy, kh):
    ki = ['# GENERÁLT: eszkozok/karoli_kh_epseg.py — kézzel szerkeszteni tilos', '',
          '# A Károli-KH tábla épsége (olvasói kapu, 4. pont)', '',
          '*scope=konkordancia/Karoli_kereszthivatkozasok.tsv | forras=eszkozok/karoli_kh_epseg.py | '
          'ts=%s*' % os.environ.get('PARDES_DATUM', '2026-11-02'), '',
          '| Mérőszám | Érték |', '|---|---|']
    ki += ['| %s | %d |' % (n, v) for n, v in stat]
    ki += ['', '## Ismert esetek (az átvilágításból)', '', '| Forrásvers | Gyanús? | Azonos listájú, támogatott |',
           '|---|---|---|']
    for k in ('Act.2.27', 'Act.2.31', 'Isa.34.11', 'Psa.116.13', 'Act.2.21', 'Act.9.14', 'Act.22.16', 'Ezk.31.15',
              'Jon.2.3', 'Isa.14.15', 'Pro.9.18'):
        ki.append('| %s | %s | %s |' % (k, 'igen' if k in gy else 'nem (a szabály nem fogja meg)',
                                        ', '.join(gy.get(k, [])) or '—'))
    ki.append('')
    return '\n'.join(ki) + '\n'


if __name__ == '__main__':
    sys.exit(main())
