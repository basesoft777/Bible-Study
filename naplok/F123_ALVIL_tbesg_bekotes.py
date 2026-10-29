"""F123.ALVIL.J18 (ELLENOR_F123_ALVIL-001_2 E5, DT-F123l): a G0086 TBESG-bekötése a `adat/lexikon_hivatkozasok.tsv`-ben.

Döntés (DT-F123l, orkesztrátor, a felhasználó felhatalmazásával, 2026-10-29): a bekötés a TBESG azon jelentésére szól, amely az
alvilágot, a halottak lakhelyét jelenti (TBESG G0086 „__2. the abode of Hades, the underworld; in NT, the abode of departed
spirits, Hades”), a Hádész istenre („__1. in Hom., Hades (Pluto), the god of the underworld”) nem. Ez a jóváhagyott
szakaszcímke-döntés (DT-F123h) következménye: a Thayer `-/2/-` hordozó, a `-/1/-` nem.

A szakasz szövege a `konkordancia/TBESG.txt` G0086-sorának utolsó mezőjéből, a G1941-sorok mintájára
(`eszkozok/f6_3_lexikon_hivatkozasok_toltes.py` `g1941_szegmensek`: HTML-címkék ki, szóköz-normalizálás, `__<n>.` szerinti
bontás). Írás előtt összevetés: a meglévő sorok bájtra változatlanok, a kulcs (`G0086 TBESG G0086 2`) még nincs a táblában, a
szöveg részlánca a normalizált forrásnak; eltérésnél megáll. TSV: `split('\\t')` / `'\\t'.join()`.

    python naplok/F123_ALVIL_tbesg_bekotes.py [--ir]
"""
import io
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TBESG = os.path.join(GY, 'konkordancia', 'TBESG.txt')
LEXHIV = os.path.join(GY, 'adat', 'lexikon_hivatkozasok.tsv')


def tbesg_szegmensek(strong):
    with io.open(TBESG, encoding='utf-8') as f:
        nyers = next(s.rstrip('\n').split('\t')[-1] for s in f if s.startswith(strong + '\t'))
    tiszta = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', nyers)).strip()
    reszek = re.split(r'\s*__(\d+)\.\s*', tiszta)
    seg = {reszek[i]: reszek[i + 1].strip() for i in range(1, len(reszek) - 1, 2)}
    return tiszta, seg


def main():
    ir = '--ir' in sys.argv
    tiszta, seg = tbesg_szegmensek('G0086')
    assert sorted(seg) == ['1', '2'], ('a TBESG G0086 tagolása nem 1/2', sorted(seg))
    assert 'god of the underworld' in seg['1'], seg['1'][:80]
    assert seg['2'].startswith('the abode of Hades, the underivorld'), seg['2'][:80]
    szoveg = seg['2']
    assert szoveg in tiszta and '\t' not in szoveg and '\n' not in szoveg
    uj = ['G0086', 'TBESG', 'G0086', '2', szoveg, 'konkordancia/TBESG.txt']
    eredeti = io.open(LEXHIV, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in eredeti else '\n'
    L = eredeti.split(nl)
    fej_i = next(i for i, x in enumerate(L) if x and not x.startswith('#'))
    assert L[fej_i].split('\t') == ['strong', 'szotar', 'entry_id', 'jelentes_szam', 'szoveg_en', 'forrasfajl'], L[fej_i]
    kulcsok = [tuple(x.split('\t')[:4]) for x in L[fej_i + 1:] if x and not x.startswith('#')]
    assert ('G0086', 'TBESG', 'G0086', '2') not in kulcsok
    utolso = max(i for i, x in enumerate(L) if x.startswith('G0086\t'))
    L2 = L[:utolso + 1] + ['\t'.join(uj)] + L[utolso + 1:]
    # összevetés: a régi sorok sorrendben, bájtra változatlanok
    assert L2[:utolso + 1] == L[:utolso + 1] and L2[utolso + 2:] == L[utolso + 1:]
    print('ÚJ SOR (a %d. sor után): %s' % (utolso + 1, '\t'.join(uj[:4])))
    print('szoveg_en: %s' % szoveg)
    if ir:
        io.open(LEXHIV, 'w', encoding='utf-8', newline='').write(nl.join(L2))
        print('ÍRVA: %s' % os.path.relpath(LEXHIV, GY))
    else:
        print('próba (--ir nélkül): nem írt')


if __name__ == '__main__':
    main()
