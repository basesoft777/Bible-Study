#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.17 — a két C-futás (F3: prompt v1, F3V2: prompt v2) eltérése a közös arany v2-n.

Mit mér: F3 és F3V2 különbségét (Δ = F3V2 − F3) pontosságban, lefedettségben
(60 aranyvers, arany v2), kapuhiba-arányban (200 vers), rétegenként; a
verszintű link-halmaz egyezést (azonos linkhalmazú versek, és a Σ|∩|/Σ|∪|
arány); és a Δ 90%-os bootstrap-intervallumát (a versek felett, rétegenként
rétegzett újramintavétellel, 1000 ismétlés, mag 20260930; a két futás
ugyanazon versein párosítva).

Mit NEM mér: a futások közti ingadozást önmagában. A két futás promptja is
különbözik, ezért Δ = prompthatás + futásközi ingadozás (+ kölcsönhatás), és egy-
egy futásból a kettő nem választható szét. A bootstrap-intervallum a
versminta bizonytalanságát fedi (ha ugyanezt a két futást más versekre is
elvégeztük volna), a futás megismétlésének szórását nem. A |Δ| ezért a
„futások közötti eltérés” (prompt és ingadozás együtt) felső becslése, nem az
ingadozásé; az ingadozás ennél kisebb és nagyobb is lehet (a kettő hatása ki is
olthatja egymást).

Kimenet: f21p/ingadozas.tsv (generált).
    python eszkozok/karoli_strong/ingadozas.py
"""

import os
import random
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import meres  # noqa: E402
import meres_v2  # noqa: E402
import tokenek  # noqa: E402

KIMENET = os.path.join(tokenek.ROOT, 'f21p', 'ingadozas.tsv')
MAG = 20260930
N_BOOT = 1000
RETEGEK = meres.RETEGEK + [meres.OSSZES]


def main():
    adat, g = meres_v2.betolt()
    g2 = g['v2']
    rnd = random.Random(MAG)
    arany_v = [ig for ig in adat.versek if ig in adat.arany and adat.ok('F3', ig) and adat.ok('F3V2', ig)]
    per = {}
    for ig in arany_v:
        gl = g2(ig)
        row = {}
        for f in ('F3', 'F3V2'):
            cl = adat.linkek(f, ig)
            row[f] = (len(cl & gl), len(cl), len(gl))
        per[ig] = row
    kapu = {}
    for f in ('F3', 'F3V2'):
        _, _, elso = meres.hibatipusok(adat, f)
        kapu[f] = {ig: (ig in elso, adat.futas[f][ig]['allapot'] != 'ok') for ig in adat.versek}

    def ret_of(ig):
        return adat.reteg[ig]

    def merok(vs):
        s = {f: [sum(per[ig][f][i] for ig in vs) for i in range(3)] for f in ('F3', 'F3V2')}
        out = {}
        for f in s:
            t, c, a = s[f]
            out[f] = (t / c if c else float('nan'), t / a if a else float('nan'))
        return out

    def kapumerok(vs):
        return {f: (sum(kapu[f][ig][0] for ig in vs) / len(vs), sum(kapu[f][ig][1] for ig in vs) / len(vs)) for f in kapu}

    sorok = [['szakasz', 'reteg', 'mero', 'F3', 'F3V2', 'delta', 'delta_also90', 'delta_felso90', 'abs_delta_felso95', 'n', 'megjegyzes']]
    reteg_arany = {r: [ig for ig in arany_v if r == meres.OSSZES or ret_of(ig) == r] for r in RETEGEK}
    reteg_200 = {r: [ig for ig in adat.versek if r == meres.OSSZES or ret_of(ig) == r] for r in RETEGEK}
    strata_a = {r: [ig for ig in arany_v if ret_of(ig) == r] for r in meres.RETEGEK}
    strata_2 = {r: [ig for ig in adat.versek if ret_of(ig) == r] for r in meres.RETEGEK}
    # bootstrap: rétegzett újramintavétel (az Összes a négy réteg együtt)
    boot_a = {r: [] for r in RETEGEK}
    boot_k = {r: [] for r in RETEGEK}
    for _ in range(N_BOOT):
        mint_a = {r: [s[rnd.randrange(len(s))] for _ in s] for r, s in strata_a.items()}
        mint_2 = {r: [s[rnd.randrange(len(s))] for _ in s] for r, s in strata_2.items()}
        for r in RETEGEK:
            va = sum(mint_a.values(), []) if r == meres.OSSZES else mint_a[r]
            v2_ = sum(mint_2.values(), []) if r == meres.OSSZES else mint_2[r]
            m = merok(va)
            k = kapumerok(v2_)
            boot_a[r].append((m['F3V2'][0] - m['F3'][0], m['F3V2'][1] - m['F3'][1]))
            boot_k[r].append((k['F3V2'][0] - k['F3'][0], k['F3V2'][1] - k['F3'][1]))

    def iv(lista):
        s = sorted(lista)
        a = sorted(abs(x) for x in lista)
        return s[int(0.05 * len(s))], s[int(0.95 * len(s)) - 1], a[int(0.95 * len(a)) - 1]

    for r in RETEGEK:
        m = merok(reteg_arany[r])
        for i, nev in ((0, 'pontossag'), (1, 'lefedettseg')):
            lo, hi, ab = iv([b[i] for b in boot_a[r]])
            sorok.append(['arany_v2', r, nev, '%.4f' % m['F3'][i], '%.4f' % m['F3V2'][i],
                          '%.4f' % (m['F3V2'][i] - m['F3'][i]), '%.4f' % lo, '%.4f' % hi, '%.4f' % ab,
                          str(len(reteg_arany[r])), 'aranyversek (mindkét futásban kapun átment)'])
        k = kapumerok(reteg_200[r])
        for i, nev in ((0, 'kapuhiba_elso_probara'), (1, 'kapuhiba_vegleg')):
            lo, hi, ab = iv([b[i] for b in boot_k[r]])
            sorok.append(['kapu', r, nev, '%.4f' % k['F3'][i], '%.4f' % k['F3V2'][i],
                          '%.4f' % (k['F3V2'][i] - k['F3'][i]), '%.4f' % lo, '%.4f' % hi, '%.4f' % ab,
                          str(len(reteg_200[r])), 'a 200 verses minta'])
    # verszintű link-halmaz egyezés
    for halmaz_nev, vs0 in (('arany (60)', arany_v), ('minta (200)', [ig for ig in adat.versek if adat.ok('F3', ig) and adat.ok('F3V2', ig)])):
        for r in RETEGEK:
            vs = [ig for ig in vs0 if r == meres.OSSZES or ret_of(ig) == r]
            az = sum(1 for ig in vs if adat.linkek('F3', ig) == adat.linkek('F3V2', ig))
            m_ = sum(len(adat.linkek('F3', ig) & adat.linkek('F3V2', ig)) for ig in vs)
            u_ = sum(len(adat.linkek('F3', ig) | adat.linkek('F3V2', ig)) for ig in vs)
            sorok.append(['linkhalmaz', r, 'azonos_linkhalmazu_versek [%s]' % halmaz_nev, '', '', '%d' % az, '', '', '',
                          str(len(vs)), 'F3 és F3V2 linkhalmaza azonos (a kizárásokkal)'])
            sorok.append(['linkhalmaz', r, 'link_egyezes Σ|∩|/Σ|∪| [%s]' % halmaz_nev, '', '', '%.4f' % (m_ / u_ if u_ else 0),
                          '', '', '', str(len(vs)), '%d/%d' % (m_, u_)])
    with open(KIMENET, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# GENERÁLT: eszkozok/karoli_strong/ingadozas.py | F3 vs F3V2 az arany v2-n | mag=%d, bootstrap=%d | '
                 'Δ = prompthatás + futásközi ingadozás, szét nem választható | kézzel szerkeszteni tilos\n' % (MAG, N_BOOT))
        for s in sorok:
            fh.write('\t'.join(s) + '\n')
    for s in sorok[1:]:
        if s[1] == meres.OSSZES:
            print(' | '.join(s[:10]))
    print('-> %s' % KIMENET)


if __name__ == '__main__':
    main()
