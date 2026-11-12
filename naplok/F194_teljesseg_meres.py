"""F194.2 (K96, DT548): az ISTENTISZT-001 teljesség-mérése a 2. kiadás határán (DT-F194a).

A `naplok/F123_ISTTELJ_meres.py` három hálóját futtatja változatlanul, két eltéréssel:
- a motívum kifejezése az ÚSZ-ben: G1941 (epikaleó) és G3686 (onoma) legfeljebb 6 tokenre, és a név után legfeljebb
  6 tokenen belül az Úr megnevezése: G2962 (kürios) vagy G2424 (Iészúsz) (DT-F194a: a puszta „nevedet”, „ezt a nevet”
  nem a formula); az ÓSZ-feltétel változatlan (H7121 + H9003 + H8034 + H3068);
- a kimenet: `naplok/F194_teljesseg_ISTENTISZT-001.{md,tsv}` és `_blokkok.tsv` (az F123-as mérés fájljai, amelyekre a
  `jeloltek.tsv` összesítő sorai hivatkoznak, nem íródnak felül).
Csak olvas, adattáblát nem ír. Futtatás: python naplok/F194_teljesseg_meres.py [--lap]

`--lap` (F194.20, a 2. fázis; a teljesség-kapu, F212): a soronkénti kimenetet a lap mérésfájljába is kiírja
(`naplok/F123_teljesseg_ISTENTISZT-001.tsv`, ezt olvassa a `lexikon_general.teljesseg_halok`), a strong-háló
proveniencia-sorában a motívum mai Strong-halmazával (`strong=G1941+H7121+H8034`, a kapu ezt veti össze). Az F123-as
leírás (`.md`) és a kézzel bővített `_blokkok.tsv` (a `jeloltek.tsv` összesítő sorainak hivatkozása) nem íródik felül.
"""
import os
import sys

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'naplok'))
import F123_ISTTELJ_meres as M  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

UR = {'G2962', 'G2424'}


def kifejezes(toks):
    """'osz' / 'usz' / '' — az ÚSZ-ben a név után az Úr megnevezése is kell (DT-F194a)."""
    st = [s for s, _ in toks]
    for j, s in enumerate(st):
        if s == 'H8034' and j and st[j - 1] == 'H9003' and 'H3068' in st[j + 1:j + 3]:
            if 'H7121' in st[max(0, j - 9):j + 9]:
                return 'osz'
    for i, s in enumerate(st):
        if s == 'G1941':
            for j in range(max(0, i - 6), min(i + 7, len(st))):
                if st[j] == 'G3686' and UR & set(st[j + 1:j + 7]):
                    return 'usz'
    return ''


def main():
    M.kifejezes = kifejezes
    M.KI = os.path.join(GYOKER, 'naplok', 'F194_teljesseg_ISTENTISZT-001')
    M.main()
    ut = M.KI + '.md'
    with open(ut, encoding='utf-8') as f:
        t = f.read()
    fej = ('<!-- F194.2: a mérés a `naplok/F194_teljesseg_meres.py` futtatója, az F123-as hálókkal és az új ÚSZ-feltétellel '
           '(DT-F194a: ἐπικαλέω + ὄνομα + az Úr megnevezése, G2962/G2424). Az alábbi szöveg az F123-as szkript sablonja. -->\n')
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fej + t)


LAP_TSV = os.path.join(GYOKER, 'naplok', 'F123_teljesseg_ISTENTISZT-001.tsv')
MAI_STRONG = 'G1941+H7121+H8034'


def lap_tsv():
    """A mérés soronkénti kimenete a lap mérésfájljába; a strong-háló proveniencia-sora a mai Strong-halmazzal."""
    with open(M.KI + '.tsv', encoding='utf-8') as f:
        sorok = [x.rstrip('\n') for x in f]
    ki = ['# GENERÁLT: naplok/F194_teljesseg_meres.py --lap (az ISTENTISZT-001 2. kiadása; leírás: '
          'naplok/F194_teljesseg_ISTENTISZT-001.md) — kézzel nem szerkesztendő (DT548)']
    for x in sorok:
        if x.startswith('#'):
            continue
        c = x.split('\t')
        if c[0] == 'strong' and len(c) == 6 and 'strong=' not in c[5]:
            c[5] = c[5].replace(' | n=', ' | strong=%s | n=' % MAI_STRONG, 1)
        ki.append('\t'.join(c))
    with open(LAP_TSV, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(ki) + '\n')
    print('lap mérésfájl:', LAP_TSV, len(ki) - 2, 'sor')


if __name__ == '__main__':
    main()
    if '--lap' in sys.argv[1:]:
        lap_tsv()
