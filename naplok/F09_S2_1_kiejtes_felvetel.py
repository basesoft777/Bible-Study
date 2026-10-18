"""F09 S2.1: a 26 jovahagyott heber lemma-kiejtes rogzitese az adat/kiejtes_kivetelek.tsv-be.

Forras: naplok/SZOTAR_S1_heber_jeloltek.tsv (F05 D34-D37, jovahagyva 2026.09.29),
valtoztatas nelkul. A kulcs (alak) a TBESH-lemma NFC alakja (ezt adja a
lexikon_general.lemma_kiejtes); a H7121 es a H8034 (kodbeli KIEJT-migracios
sorok, STEP-atiras kulcsal) mar benne van, azokat nem ismetli.
Iras: '\t'.join, csv nelkul; az iras elott a meglevo sorok osszevetese.
"""
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')
import os, unicodedata
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import lexikon_general as LG

JEL = os.path.join(ROOT, 'naplok', 'SZOTAR_S1_heber_jeloltek.tsv')
KIV = os.path.join(ROOT, 'adat', 'kiejtes_kivetelek.tsv')

def olvas(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        return f.read()

jelolt = {}
for l in olvas(JEL).split('\n'):
    if not l or l.startswith('#') or l.startswith('strong\t'):
        continue
    f = l.split('\t')
    jelolt[f[0]] = f
assert len(jelolt) == 26, len(jelolt)

regi = olvas(KIV)
regi_sorok = regi.split('\n')
adat_regi = [s.split('\t') for s in regi_sorok if s and not s.startswith('#') and not s.startswith('nyelv\t')]
assert len(adat_regi) == 5, len(adat_regi)
letezo_step = {(s[0], s[1]): s[2] for s in adat_regi}

uj = []
lemma_kulcsok = {}
for strong, f in sorted(jelolt.items()):
    ertek = f[4]
    lk = LG.lemma_kiejtes(strong)
    assert lk, strong
    lemma, step = lk
    if ('heber', step) in letezo_step:
        assert letezo_step[('heber', step)] == ertek, (strong, ertek)
        print('mar benne van (STEP-kulcs):', strong, step, ertek)
        continue
    kulcs = unicodedata.normalize('NFC', lemma)
    assert kulcs not in lemma_kulcsok, ('lemma-utkozes', strong, lemma_kulcsok.get(kulcs))
    lemma_kulcsok[kulcs] = strong
    megj = ('F05 S1.7 jelölt (naplok/SZOTAR_S1_heber_jeloltek.tsv), jóváhagyva 2026.09.29 (D34-D37), %s; '
            'kulcs: TBESH-lemma; manual' % strong)
    if strong == 'H2555':
        megj = 'F05 D36 kézi kivétel (hámás), jóváhagyva 2026.09.29, %s; kulcs: TBESH-lemma; manual' % strong
    uj.append('\t'.join(['heber', kulcs, ertek, megj]))

print('uj sorok:', len(uj))
uj_szoveg = regi if regi.endswith('\n') else regi + '\n'
uj_szoveg += '\n'.join(uj) + '\n'
# sor-osszevetes: a meglevo sorok bajtra valtozatlanok (elotag)
assert uj_szoveg.startswith(regi), 'a meglevo sorok valtoztak'
if '--ir' in sys.argv:
    with open(KIV, 'w', encoding='utf-8', newline='') as f:
        f.write(uj_szoveg)
    print('irva:', KIV)
