"""F194 (K43, K40): az ISTENTISZT-001 előfordulásainak munkalapja a próza (`kapcsolodas`, `funkcio`) írásához.

Igehelyenként: a Károli-vers (szó szerint), a mai `kapcsolodas` és `funkcio`, és a motívum szavai a versben
(héber: TAHOT, a teljes szó a `heber_kiejtes.kiejt` magyaros kiejtésével; görög: TAGNT, a `kiejtes.atir`
kiejtésével), a formula környezetével. Csak olvas; a kimenet a parancssori `--kimenet` fájlba megy (nem a repóba).
Futtatás: python naplok/F194_munkalap.py --kimenet <fájl> [--igehely "Zsolt 99:6" ...]
"""
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))
import heber_kiejtes as hk  # noqa: E402
import kiejtes as gk  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

ID = 'ISTENTISZT-001'
FORMULA = {'H7121', 'H8034', 'H3068', 'H0430', 'H1168', 'G1941', 'G3686', 'G2962', 'G2424', 'G5547'}


def tsv(ut):
    fej, ki = None, []
    for s in open(os.path.join(GYOKER, ut), encoding='utf-8').read().split('\n'):
        if not s or s.startswith('#'):
            continue
        m = s.split('\t')
        if fej is None:
            fej = m
            continue
        ki.append(dict(zip(fej, m)))
    return ki


def versek(ut, kulcsok):
    d = {}
    for s in open(os.path.join(GYOKER, ut), encoding='utf-8'):
        k = s.split('\t', 1)[0]
        if k in kulcsok:
            m = s.rstrip('\n').split('\t')
            d.setdefault(k, []).append(m)
    return d


def main():
    ki_ut = sys.argv[sys.argv.index('--kimenet') + 1]
    elof = [r for r in tsv('adat/elofordulasok.tsv') if r['id'] == ID]
    helyek = [r['igehely'] for r in elof]
    extra = [sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == '--igehely']
    kulcs = set(helyek + extra)
    karoli = {r['Igehely']: r['Károli-szöveg (teljes vers)'] for r in tsv('konkordancia/Karoli_1908.tsv')
              if r['Igehely'] in kulcs}
    tahot = versek('konkordancia/TAHOT_kivonat.tsv', kulcs)
    tagnt = versek('konkordancia/TAGNT_kivonat.tsv', kulcs)
    tahot_fej = ['Igehely', 'Strong-szám', 'Ragozott alak', 'Kiejtés', 'Szótő', 'Rövid jelentés', 'Angol tükörfordítás']
    sz, kv = gk.szabalyok_betolt(), gk.kivetelek_betolt()
    sorrend = [(r['igehely'], r) for r in elof] + [(h, None) for h in extra]
    with open(ki_ut, 'w', encoding='utf-8') as f:
        for h, r in sorrend:
            f.write('## %s\n' % h)
            f.write('Károli: %s\n' % karoli.get(h, '(nincs)'))
            if r:
                f.write('kapcsolodas: %s\nfunkcio: %s\nszint: %s · jsz: %s · karoli_szo: %s\n' % (
                    r['kapcsolodas'], r['funkcio'], r['pardes_szint'], r['jelentes_szam'], r['karoli_szo']))
            if h in tahot:
                sorok = [dict(zip(tahot_fej, m)) for m in tahot[h]]
                tok = []
                for i, s in enumerate(sorok):
                    st = s['Strong-szám'][:5]
                    if st.startswith('H9') and st not in ('H9003',):
                        continue
                    alak, eh, mk = hk.teljes_szo(sorok, i)
                    jel = '*' if st in FORMULA else ''
                    tok.append('%s%s(%s)%s[%s]' % (jel, hk.tisztit(alak), hk.kiejt(alak, eh, mk), st,
                                                   s['Angol tükörfordítás']))
                f.write('TAHOT: %s\n' % ' '.join(tok))
            if h in tagnt:
                tok = []
                for m in tagnt[h]:
                    st = m[1][:5]
                    jel = '*' if st in FORMULA else ''
                    tok.append('%s%s(%s)%s{%s}' % (jel, m[2], gk.atir(m[3], sz, kv), st, m[7] if len(m) > 7 else ''))
                f.write('TAGNT: %s\n' % ' '.join(tok))
            f.write('\n')
    print('kész:', ki_ut, len(sorrend), 'igehely')


if __name__ == '__main__':
    main()
