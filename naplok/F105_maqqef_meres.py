"""F105 (FELADATOK #105, DT-F105a): a rafe-maqqéf feloldási szabályának (`eszkozok/bdb_rovidites.maqqef_javit`) mérése.

Minden BDB-szócikk (`konkordancia/BDB_teljes_unabridged.tsv`, a megjelenítés szórend-cseréje után, `_sorrend_csere`)
minden rafét (U+05BF) hordozó szavára: a szabály kimenete (maqqéf a rafét hordozó betű előtt vagy után, vagy változatlan),
és az ellenkező oldali bontás. Próba: a bontás két része (mássalhangzó-váz, végbetű alapbetűre) a héber Biblia szókészletében
áll-e (a Macula szavai: a morfémák az `xml_id` szerint szóvá fűzve, a maqqéf nélkül). Ítélet: `jo` (a szabály bontásának
mindkét része ismert szó, az ellenkezőé nem), `rossz` (fordítva), `nem_dont` (mindkettő / egyik sem), `valtozatlan` (a szabály
nem bont). Kimenet: `--ki` fájl (összesítés és legfeljebb 20 `rossz` példa).
Futtatás: python naplok/F105_maqqef_meres.py --ki <fájl>
"""
import argparse
import collections
import os
import re
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import bdb_rovidites as R  # noqa: E402

KONK = os.path.join(REPO, 'konkordancia')
SZO_RE = re.compile(r'[֑-ֽֿ-ׇא-״]+')


def vaz(s):
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if 'א' <= c <= 'ת')
    return s.translate(str.maketrans('ךםןףץ', 'כמנפצ'))


def tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r').split('\t') for s in f if not s.startswith('#')]
    return [dict(zip(sorok[0], s)) for s in sorok[1:]]


def macula_szavak():
    szavak = collections.defaultdict(str)
    for fn in sorted(os.listdir(KONK)):
        if fn.startswith('Macula_heber_') and fn.endswith('.tsv'):
            for d in tsv(os.path.join(KONK, fn)):
                szavak[fn + d['xml_id'][:-1]] += d['szo']
    return {vaz(w) for w in szavak.values() if vaz(w)}


def bontas(szo, elotte_i):
    """A szó két része, ha a vágás a betű-index előtt van (vázban)."""
    v = vaz(szo)
    return v[:elotte_i], v[elotte_i:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ki', required=True)
    a = ap.parse_args()
    ismert = macula_szavak()
    c, pelda = collections.Counter(), []
    for d in tsv(os.path.join(KONK, 'BDB_teljes_unabridged.tsv')):
        st = d['Strong_padded']
        szoveg = R._sorrend_csere(d['Teljes_szocikk'], st)
        for m in SZO_RE.finditer(szoveg):
            szo = m.group(0)
            if R.RAFE not in szo:
                continue
            nfd = unicodedata.normalize('NFD', szo)
            # a rafét hordozó betű sorszáma a szó betűi között (az első rafe)
            bi, n = None, -1
            for ch in nfd:
                if 'א' <= ch <= 'ת':
                    n += 1
                elif ch == R.RAFE and bi is None:
                    bi = n
            if bi is None or bi < 0:
                c['nincs_betu'] += 1
                continue
            ki = R.maqqef_javit(szo + ' ')  # a szó utáni szóköz-esetet a szavon belül nem mérjük
            ki = ki[:-1] if ki.endswith(' ') else ki
            ossz = len(vaz(szo))
            if R.MAQQEF not in ki:
                c['valtozatlan'] += 1
                continue
            elol = vaz(ki.split(R.MAQQEF)[0])
            vag = len(elol)
            alt = bi + 1 if vag == bi else bi          # a másik oldal: a rafét hordozó betű után / előtt
            jo = all(p in ismert for p in bontas(szo, vag)) and 0 < vag < ossz
            alt_jo = all(p in ismert for p in bontas(szo, alt)) and 0 < alt < ossz
            it = 'jo' if jo and not alt_jo else 'rossz' if alt_jo and not jo else 'nem_dont'
            c[it] += 1
            c['%s_%s' % ('elotte' if vag == bi else 'utana', it)] += 1
            if it == 'rossz' and len(pelda) < 20:
                pelda.append('%s\t%s\t%s' % (st, szo, ki))
    with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
        for k, v in sorted(c.items()):
            f.write('%s\t%d\n' % (k, v))
        f.write('# rossz példák (strong, szó, a szabály kimenete)\n' + '\n'.join(pelda) + '\n')
    print(dict(c))


if __name__ == '__main__':
    main()
