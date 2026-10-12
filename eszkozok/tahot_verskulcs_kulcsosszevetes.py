#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F85.23 — a teljes ÓSZ-os versszintű kulcs-összevetés (Károli-vers <-> TAHOT-kulcs); a #85 7. tételének EP1-je.

Csak olvas. Bemenetek: konkordancia/TAHOT_kivonat.tsv (Igehely mező), konkordancia/Karoli_1908.tsv, naplok/F85_kulcsvaltas.tsv
(az összevonások azonosítására), f22/versosszevonas.tsv; másodlagos, független jel: a versbeosztás-detektor (versbeosztas.elemez,
vershossz-alapú; nem ír semmit). Vizsgálatok:
  1. TAHOT-kulcsok Károli-vers nélkül (várt: 0);
  2. ÓSZ-Károli-versek TAHOT-sor nélkül (várt: 0);
  3. a közös kulcson álló két TAHOT-vers (az összevonások): jelölve, NEM hiba; egyezés az f22/versosszevonas.tsv Károli-kulcsaival;
  4. a kulcsok formátuma (könyv fejezet:vers) és az ÓSZ-könyvlista egyezése;
  5. a detektor az ÓSZ-ben: eltolt / nincs_eredeti / nincs_karoli sorok száma (várt: 0).
Kimenet: naplok/F85_kulcsosszevetes.tsv és naplok/F85_kulcsosszevetes.md (proveniencia-sorral). Más fájlt nem ír.
Kilépési kód: 0 = nincs váratlan eltérés; 1 = van (ilyenkor a futtató megáll és jelent).

Futtatás a repó gyökeréből:  python eszkozok/tahot_verskulcs_kulcsosszevetes.py
"""
import collections
import datetime
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok', 'karoli_strong'))
import tokenek  # noqa: E402
import versbeosztas  # noqa: E402

TAHOT = os.path.join(ROOT, 'konkordancia', 'TAHOT_kivonat.tsv')
KAROLI = os.path.join(ROOT, 'konkordancia', 'Karoli_1908.tsv')
VALT = os.path.join(ROOT, 'naplok', 'F85_kulcsvaltas.tsv')
OSSZ = os.path.join(ROOT, 'f22', 'versosszevonas.tsv')
KI_TSV = os.path.join(ROOT, 'naplok', 'F85_kulcsosszevetes.tsv')
KI_MD = os.path.join(ROOT, 'naplok', 'F85_kulcsosszevetes.md')
TS = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def bont(ig):
    k, r = ig.rsplit(' ', 1)
    c, v = r.split(':')
    return k, int(c), int(v)


def main():
    sor_ki = []     # (vizsgalat, tárgy, eredmeny, reszlet)

    def jelent(viz, targy, eredmeny, reszlet=''):
        sor_ki.append((viz, targy, eredmeny, reszlet))
        print('%s | %s | %s | %s' % (viz, targy, eredmeny, reszlet))

    # --- bemenetek ---
    tahot_sor = collections.Counter()
    konyvsorrend = []
    with open(TAHOT, encoding='utf-8') as fh:
        next(fh)
        for s in fh:
            k = s.split('\t', 1)[0]
            tahot_sor[k] += 1
            b = k.rsplit(' ', 1)[0]
            if b not in konyvsorrend:
                konyvsorrend.append(b)
    karoli_mind = []
    with open(KAROLI, encoding='utf-8') as fh:
        next(fh)
        for s in fh:
            karoli_mind.append(s.split('\t', 1)[0])
    ot = set(konyvsorrend)
    karoli = [k for k in karoli_mind if k.rsplit(' ', 1)[0] in ot]
    kset, tset = set(karoli), set(tahot_sor)

    # 4. formátum
    rossz = []
    for k in tset:
        try:
            bont(k)
        except Exception:   # noqa: BLE001
            rossz.append(k)
    jelent('4', 'a TAHOT-kulcsok formátuma (könyv fejezet:vers)', 'OK' if not rossz else 'ELTÉRÉS', '%d kulcs, %d hibás %s' % (len(tset), len(rossz), rossz[:5]))
    jelent('4', 'ÓSZ-könyvek a TAHOT-ban', 'OK' if len(ot) == 39 else 'ELTÉRÉS', '%d könyv' % len(ot))
    jelent('4', 'a TAHOT-sorok száma', 'OK', '%d sor (fejléc nélkül), %d különböző kulcs' % (sum(tahot_sor.values()), len(tset)))

    # 1., 2.
    k_nelkul = sorted(tset - kset, key=lambda x: (konyvsorrend.index(x.rsplit(' ', 1)[0]), bont(x)[1:]))
    t_nelkul = [k for k in karoli if k not in tset]
    jelent('1', 'TAHOT-kulcs Károli-vers nélkül', 'OK' if not k_nelkul else 'ELTÉRÉS', '%d kulcs %s' % (len(k_nelkul), k_nelkul[:20]))
    jelent('2', 'ÓSZ-Károli-vers TAHOT-sor nélkül', 'OK' if not t_nelkul else 'ELTÉRÉS', '%d vers (a %d ÓSZ-Károli-versből) %s' % (len(t_nelkul), len(karoli), t_nelkul[:20]))

    # 3. összevonások: a közös kulcson két TAHOT-vers (átkulcsolás előtti címkék a naplóból)
    forras = collections.defaultdict(set)    # új kulcs -> a naplóban szereplő régi TAHOT-versek
    with open(VALT, encoding='utf-8') as fh:
        for s in fh:
            if s.startswith('#') or s.startswith('sorszam\t'):
                continue
            p = s.rstrip('\n').split('\t')
            forras[p[2]].add(p[1])
    kozos_log = {k for k, v in forras.items() if len(v) > 1}
    ossz_kulcsok = set()
    with open(OSSZ, encoding='utf-8') as fh:
        sorok = [s.rstrip('\n') for s in fh if s.strip() and not s.startswith('#')]
    for s in sorok[1:]:
        ossz_kulcsok.add(s.split('\t')[0])
    # a naplóban csak a kulcsot váltó vers szerepel; az összevonás partnere a saját (nem váltó) címkéjén áll: az f22/versosszevonas.tsv Károli-kulcsai a hiteles lista
    jelent('3', 'összevonás: a közös Károli-kulcson két TAHOT-vers (jelölve, NEM hiba)', 'OK' if len(ossz_kulcsok) == 9 and ossz_kulcsok <= kset and ossz_kulcsok <= tset else 'ELTÉRÉS',
           '%d közös kulcs: %s' % (len(ossz_kulcsok), ', '.join(sorted(ossz_kulcsok, key=lambda x: (konyvsorrend.index(x.rsplit(' ', 1)[0]), bont(x)[1:])))))
    jelent('3', 'az összevonó kulcsok mind létező Károli-versek és TAHOT-kulcsok', 'OK' if ossz_kulcsok <= kset and ossz_kulcsok <= tset else 'ELTÉRÉS', '')
    jelent('3', 'a naplóban több régi versből jövő új kulcsok ⊆ az f22/versosszevonas.tsv kulcsai', 'OK' if kozos_log <= ossz_kulcsok else 'ELTÉRÉS', '%d kulcs a naplóban, %d az összevonás-fájlban' % (len(kozos_log), len(ossz_kulcsok)))

    # per könyv
    per = []
    for b in konyvsorrend:
        kb = [k for k in karoli if k.rsplit(' ', 1)[0] == b]
        tb = [k for k in tset if k.rsplit(' ', 1)[0] == b]
        per.append((b, len(kb), len(tb), sum(tahot_sor[k] for k in tb), len([k for k in tb if k not in kset]), len([k for k in kb if k not in tset]),
                    len([k for k in ossz_kulcsok if k.rsplit(' ', 1)[0] == b])))
        jelent('K', 'könyv %s' % b, 'OK' if per[-1][4] == 0 and per[-1][5] == 0 else 'ELTÉRÉS',
               'Károli %d vers, TAHOT %d kulcs / %d sor, Károli nélküli kulcs %d, TAHOT nélküli Károli-vers %d, összevonó kulcs %d' % per[-1][1:])

    # 5. a detektor (vershossz-alapú, független jel); nem ír
    eredmeny = versbeosztas.elemez()
    elt = kh = eh = 0
    reszl = []
    for konyv, k, e, parok, fs in eredmeny:
        if konyv not in ot:
            continue
        gep = versbeosztas.szegmensek(parok)
        a = sum(1 for _, _, t in gep if t == 'eltolt')
        b_ = sum(1 for _, _, t in gep if t == 'nincs_eredeti')
        c = sum(1 for _, _, t in gep if t == 'nincs_karoli')
        elt, kh, eh = elt + a, kh + b_, eh + c
        if a or b_ or c or len(k) != len(e):
            reszl.append('%s: eltolt %d, nincs_eredeti %d, nincs_karoli %d, Károli %d / eredeti %d vers' % (konyv, a, b_, c, len(k), len(e)))
    jelent('5', 'a versbeosztás-detektor az ÓSZ-ben (vershossz-alapú, független jel): eltolt / nincs_eredeti / nincs_karoli', 'OK' if (elt, kh, eh) == (0, 0, 0) and not reszl else 'ELTÉRÉS',
           '%d / %d / %d %s' % (elt, kh, eh, reszl[:5]))

    # tahot_lefedettseg_ellenoriz.py
    r = subprocess.run([sys.executable, os.path.join(ROOT, 'eszkozok', 'tahot_lefedettseg_ellenoriz.py')], capture_output=True, cwd=ROOT)
    kimenet = r.stdout.decode('utf-8', errors='replace').strip().split('\n')
    jelent('L', 'tahot_lefedettseg_ellenoriz.py (fejezet-szint)', 'OK' if r.returncode == 0 and any('hiányzó fejezet: 0' in x for x in kimenet) else 'ELTÉRÉS',
           'kilépési kód %d; %s' % (r.returncode, ' | '.join(x for x in kimenet if x.strip())[:300]))

    elteres = [x for x in sor_ki if x[2] == 'ELTÉRÉS']
    with open(KI_TSV, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# proveniencia: scope=teljes ÓSZ (39 könyv, %d TAHOT-kulcs, %d Károli-vers) | forras=konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv, naplok/F85_kulcsvaltas.tsv, f22/versosszevonas.tsv, versbeosztas.py (detektor, csak olvas), tahot_lefedettseg_ellenoriz.py | ts=%s\n' % (len(tset), len(karoli), TS))
        fh.write('# GENERÁLT: eszkozok/tahot_verskulcs_kulcsosszevetes.py (csak olvas)\n')
        fh.write('vizsgalat\ttargy\teredmeny\treszlet\n')
        for x in sor_ki:
            fh.write('\t'.join(c.replace('\t', ' ') for c in x) + '\n')
    with open(KI_MD, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('# F85_kulcsosszevetes.md — a teljes ÓSZ-os versszintű kulcs-összevetés (Károli-vers ↔ TAHOT-kulcs)\n\n')
        fh.write('*proveniencia: scope=teljes ÓSZ (39 könyv, %d TAHOT-kulcs, %d Károli-vers) | forras=konkordancia/TAHOT_kivonat.tsv, konkordancia/Karoli_1908.tsv, naplok/F85_kulcsvaltas.tsv, f22/versosszevonas.tsv, versbeosztas.py (detektor, csak olvas), tahot_lefedettseg_ellenoriz.py | ts=%s*\n\n' % (len(tset), len(karoli), TS))
        fh.write('*Generálta: `eszkozok/tahot_verskulcs_kulcsosszevetes.py` (csak olvas). %d vizsgálat, %d váratlan eltérés.*\n\n' % (len(sor_ki), len(elteres)))
        fh.write('| vizsgálat | tárgy | eredmény | részlet |\n|---|---|---|---|\n')
        for x in sor_ki:
            fh.write('| ' + ' | '.join(c.replace('|', '/') for c in x) + ' |\n')
    print('írva: %s, %s; váratlan eltérés: %d' % (KI_TSV, KI_MD, len(elteres)))
    return 1 if elteres else 0


if __name__ == '__main__':
    sys.exit(main())
