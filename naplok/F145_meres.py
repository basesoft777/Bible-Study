#!/usr/bin/env python
"""F145 M0 / Mz mérés: a 16. kapu (és a vele ütköző 5., 11. kapu) eredménye a #142 két csoportján.

  python naplok/F145_meres.py --gyoker <fa> [--ki <tsv>]

`--gyoker`: az a git-fa, amelynek eszközeit ÉS adattábláit a mérés használja (az eszközök importja a fa `eszkozok/`-jából).
M0: a #142 ágának fája (a javítás előtti kód); Mz: ugyanez a fa a javított fájlokkal.

Két csoport:
  A) a #142 már rögzített 5 Strongja (G0086, G0540, G1941, G2671, G5356): a `forditasok.tsv` `Thayer` `sz<n>` sorainak végleges
     szövege, a teljes kapusor (`thayer_kapuk.kapuk_futtat_thayer`), a rögzítéskor használt terminológia-kivételekkel.
  B) a 8 érintett Strong (G0012, G0282, G4151, G1311, G1944, G5010, G5351, G5590), amelyekhez nincs végleges fordítás (a bukott
     vázlatok szövege nem maradt meg). **Kontroll-próba (nem fordítás):** a tokenes forrás, a `Homer down` → `Homérosztól kezdve`
     (terminológia, 5. kapu) cserével, a `normalizal.py` javítóréteggel (Károli-rövidítések), a könyvnevek a 11. kapu saját táblája szerint (`4 Macc. 2:19` → `4Makk 2:19`), majd minden
     besorolt sigla a tábla szerinti magyar alakra cserélve — kivéve a G0012 német műcímét (`Philo's Lehre von der
     Weltschöpfung`, a prompt 5. szabálya szerint változatlan). A próba csak azt mutatja, hogy a három kapu egyszerre
     teljesíthető-e; a többi kapu (angol szöveg maradt) nem értelmezhető, azokat nem jelentjük.
TSV: split('\\t'), csv modul nélkül.
"""
import argparse
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

OTT = ['G1311', 'G5351', 'G1944', 'G5010', 'G5590', 'G0012', 'G0282', 'G4151']
REGI_OT = ['G0086', 'G0540', 'G1941', 'G2671', 'G5356']


def tsv_dict(ut):
    with open(ut, encoding='utf-8', newline='') as f:
        sorok = [s.rstrip('\r') for s in f.read().split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gyoker', required=True)
    ap.add_argument('--ki')
    a = ap.parse_args()
    gy = os.path.abspath(a.gyoker)
    for u in (os.path.join(gy, 'eszkozok', 'thayer_jelolt'), os.path.join(gy, 'eszkozok')):
        sys.path.insert(0, u)
    import thayer_bemenet as TB
    import thayer_kapuk as TK
    import forditas_kapuk as K
    import normalizal as N
    sigla = TK.sigla_betolt(os.path.join(gy, 'adat', 'thayer_sigla.tsv'))
    _, term = K._betolt()
    sorok = []

    def jelent(strong, csop, kapu, er, reszlet):
        sorok.append((strong, csop, kapu, er, reszlet.replace('\t', ' ').replace('\n', ' ')))

    # A) a már rögzített 5
    ford = [r for r in tsv_dict(os.path.join(gy, 'adat', 'forditasok.tsv'))
            if r['szotar'] == 'Thayer' and r['jelentes_szam'].startswith('sz') and r['allapot'] != 'elavult']
    for sp in REGI_OT:
        sajat = sorted((r for r in ford if r['strong'] == sp), key=lambda r: int(r['jelentes_szam'][2:]))
        szak = TB.szakaszok(sp)
        hu_tok = '\n'.join('%s %s' % (TB.token(int(r['jelentes_szam'][2:])), r['forditas_hu']) for r in sajat)
        kivetel = []
        for r in sajat:
            m = re.search(r'terminológia-kivétel \(bizonytalan_feloldasok\): ([^;]+)', r['megjegyzes'])
            if m:
                kivetel += [x.strip() for x in m.group(1).split(',')]
        for nev, er, rt in TK.kapuk_futtat_thayer(TB.tokenes(szak), hu_tok, bizonytalan=kivetel, sigla=sigla):
            jelent(sp, 'rogzitett', nev, er, rt)

    # B) a 8 érintett Strong kontroll-próbája
    for sp in OTT:
        szak = TB.szakaszok(sp)
        f_tok = TB.tokenes(szak)
        f_nt = K.szakasz_nelkul(f_tok)
        p = re.sub(r'(?:from )?Homer down', 'Homérosztól kezdve', f_tok)
        p, _ = N.normalizal(p, 'Thayer')
        # könyvnevek a 11. kapu saját táblája szerint (`4 Macc. 2:19` → `4Makk 2:19`, `Wisdom 3:13` → `Bölcs 3:13`)
        lek, f_minta, _h = K._konyv_mintak()
        p = f_minta.sub(lambda m: lek[m.group(1)] + ' ', p)
        for r in sorted((r for r in sigla if r['allapot'] == 'besorolt' and r.get('forrasalak')
                         and r['magyar_alak'] not in ('', TK.NINCS_EGYSEGES, TK.VALTOZATLAN)
                         and r['forrasalak'] not in ('R', 'G', 'L', 'T')), key=lambda r: -len(r['forrasalak'])):
            p = re.sub(r'(?<![\w])' + re.escape(r['forrasalak']) + (r'(?![\w])' if r['forrasalak'][-1].isalnum() else ''),
                       lambda m, r=r: m.group(0) if (r['forrasalak'] == 'Philo' and p[m.end():m.end() + 13].startswith("'s Lehre"))
                       else r['magyar_alak'], p)
        p_nt = K.szakasz_nelkul(p)
        t5 = K.ellenoriz_terminologia(f_nt, p_nt, term, [])
        jelent(sp, 'proba', '5_terminologia (csak Homer/down)', 'SERTES' if any(
            'Homer' in x or ' down' in x for x in t5[1].split('; ')) else 'RENDBEN',
            '; '.join(x for x in t5[1].split('; ') if 'Homer' in x or ' down' in x))
        jelent(sp, 'proba', '11_konyvek', *K.ellenoriz_konyvek(f_nt, p_nt))
        jelent(sp, 'proba', '16_sigla', *TK.ellenoriz_sigla(f_nt, p_nt, sigla))
        # a forrásban álló besorolt siglák (a 16. kapu követelményei)
        kov = ['%s×%d' % (r['forrasalak'], len(TK._re(r['forrasalak']).findall(f_nt))) for r in sigla
               if r['allapot'] == 'besorolt' and r.get('forrasalak') and TK._re(r['forrasalak']).search(f_nt)
               and r['magyar_alak'] not in ('', TK.NINCS_EGYSEGES)]
        jelent(sp, 'forras', 'besorolt sigla a forrásban', str(len(kov)), ', '.join(kov))
        raw_philo = len(re.findall('Philo', f_nt))
        if raw_philo:
            jelent(sp, 'forras', 'Philo (nyers részlet / regex-találat)', '%d/%d' % (raw_philo, len(TK._re('Philo').findall(f_nt))), '')

    for s in sorok:
        print('%s\t%s\t%s\t%s\t%s' % s)
    if a.ki:
        with open(a.ki, 'w', encoding='utf-8', newline='\n') as f:
            f.write('strong\tcsoport\tkapu\teredmeny\treszlet\n')
            for s in sorok:
                f.write('\t'.join(s) + '\n')


if __name__ == '__main__':
    main()
