"""F127 A3 (DT-F127a): a „6/b. Alkalmazás és tanítói egyezés” szakasz és a
tartalomjegyzék élesítése a lexikonoldalakon, a többi blokk újragenerálása
NÉLKÜL.

Ok: a 7 nem migrált lexikonoldal a mai generátorhoz képest elavult (a teljes
újragenerálás a #36 dolga, DT74 (3), DT246); egy teljes `--cel lexikon --ir`
ezeket a változásokat is behozná. Ez a szkript a generátor saját függvényeit
hívja (lexikon_general.szakasz_6b_beszur, res_blokkok_alkalmaz, blokk_tartalom),
tehát a kimenet ugyanaz, mint a generátoré, csak a két érintett részre.

    python eszkozok/f127_res_eles.py --kimenet <könyvtár>   # próba: <könyvtár>/lexikon/
    python eszkozok/f127_res_eles.py --ir                    # éles: lexikon/
"""
import argparse
import io
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G  # noqa: E402
import lexikon_general as LG  # noqa: E402


def egy_lap(szoveg, m):
    szoveg = szoveg.replace('\r\n', '\n')
    uj = LG.res_blokkok_alkalmaz(szoveg, m)
    uj, _ = LG._blokk_beilleszt_fejleccel(uj, LG._cel_kulcs(m['id'], 'tartalom'), LG.blokk_tartalom(m))
    return szoveg, uj


def main():
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--kimenet')
    g.add_argument('--ir', action='store_true')
    a = p.parse_args()
    _, motivumok = G.tsv_beolvas(G.MOTIVUMOK_TSV)
    sorok = LG.res_forras_sorok()
    for m in motivumok:
        if LG.res_forras_teljesen_hianyzik_e(m['id']):
            continue
        lap = os.path.join(G.ROOT, 'lexikon', '%s_TUDOMANYOS.md' % m['id'])
        if not os.path.exists(lap):
            print('  %s: nincs lexikonoldal -- kihagyva' % m['id'])
            continue
        with io.open(lap, encoding='utf-8', newline='') as f:
            regi, uj = egy_lap(f.read(), m)
        cel = lap if a.ir else os.path.join(a.kimenet, 'lexikon', os.path.basename(lap))
        os.makedirs(os.path.dirname(cel), exist_ok=True)
        with io.open(cel, 'w', encoding='utf-8', newline='\n') as f:
            f.write(uj)
        print('  %s: %s (%s)' % (m['id'], os.path.relpath(cel, G.ROOT),
                                 'változatlan' if uj == regi else 'frissítve'))
    return 0


if __name__ == '__main__':
    sys.exit(main())
