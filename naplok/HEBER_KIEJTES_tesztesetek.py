"""Az `eszkozok/heber_kiejtes.py` teszteseteinek előállítása a két kalibráló mintából (DT-F131y, N-F131w).

Kimenet: `eszkozok/teszt_heber_kiejtes_esetek.tsv` -- alakonként a teljes (kantillált) héber szó, az előtag
betűszáma, a makkef-jelzés, az elfogadott alakok (|-vel), a preferált, a modul kimenete és az állapot:
  egyezik        -- a modul kimenete elfogadott alak (ezt a teszt kikényszeríti)
  ismert_elteres -- a modul a DT-F131y döntése szerint tudatosan mást ad, mint a jelölés (ok-kal; a teszt a
                    modul mai kimenetét rögzíti, hogy a változás látsszon)
A 2. minta 41. sorának jelölését az orkesztrátor javította (DT-F131y kiegészítés: a קָרָאוּ pauzális, a „káráú”
helyes); ez itt a javított jelöléssel áll.

Proveniencia: scope=naplok/HEBER_KIEJTES_kalibracio*.json + _kulcs.json + _valasztas.txt | forras=naplok/HEBER_KIEJTES_tesztesetek.py | ts=2026-10-30
TSV: '\\t'.join() (CLAUDE.md).
"""

import json
import os
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'naplok'))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import heber_kiejtes as HK  # noqa: E402
import HEBER_KIEJTES_kalibracio as K  # noqa: E402
import HEBER_KIEJTES_kalibracio_kiertekel as KE  # noqa: E402

KI = os.path.join(ROOT, 'eszkozok', 'teszt_heber_kiejtes_esetek.tsv')
N = os.path.join(ROOT, 'naplok')

# A tudatos eltérések oka (manual; naplok/HEBER_KIEJTES_kalibracio_ujrameres.md és _kalibracio2_ertekeles.md)
OK = {
    (1, 4): 'R4 elutasítva: a meteg nélküli kámec utáni sevá néma (a jelölés: hájetá)',
    (1, 11): 'R8: ח = ch (a jelölés itt h-t választott)',
    (1, 17): 'nyitott: a zajin alatti sevá kiejtése; szabály nem fedi',
    (1, 19): 'nyitott: cere + jod furtív előtt (réjach); nem lett szabály',
    (1, 24): 'nyitott: a kettőzött betű alatti sevát a jelölő nem ejtette (missól)',
    (1, 37): 'R3: torokhang előtt kiejtett sevá (a jelölés: kisól)',
    (1, 41): 'nyitott: hosszúság (a jelölés: vesalém)',
    (1, 46): 'R1 + R8: chámász (a jelölés: hámász)',
    (1, 48): 'R8: ח = ch (a jelölés: hamasz)',
}
JAVITOTT_JELOLES = {(2, 41): {'preferalt': 'C', 'elfogadhato': ['C'], 'egyeni': None}}


def esetek(menet):
    K.beallit(menet)
    _, _, _, _, valasztott = K.minta()
    sfx = '' if menet == 1 else str(menet)
    with open(os.path.join(N, 'HEBER_KIEJTES_kalibracio%s.json' % sfx), encoding='utf-8') as f:
        tetelek = {t['sorszam']: t for t in json.load(f)['tetelek']}
    with open(os.path.join(N, 'HEBER_KIEJTES_kalibracio%s_valasztas.txt' % sfx), encoding='utf-8') as f:
        valasztas = KE.chat_beolvas(f.read())
    ki = []
    for w in valasztott:
        n = w['sorszam']
        t = tetelek[n]
        if t['heber'] != w['tiszta']:
            raise SystemExit('%d/%d: a minta eltér a JSON-tól' % (menet, n))
        v = JAVITOTT_JELOLES.get((menet, n), valasztas[n])
        kiejt = {x['betu']: x['kiejtes'] for x in t['variansok']}
        elf = [kiejt[b] for b in v['elfogadhato']] + ([v['egyeni']] if v.get('egyeni') else [])
        pref = kiejt.get(v['preferalt']) if v['preferalt'] in kiejt else (v.get('egyeni') or '')
        elotag = ''.join(r[2] for r in w['reszek'][:w['elotag_db']])
        elotag_hossz = len(HK._betuk(HK.tisztit(elotag)))
        gepi = HK.kiejt(w['alak'], elotag_hossz, w['makkef'])
        if gepi in elf:
            allapot, ok = 'egyezik', ''
        else:
            allapot, ok = 'ismert_elteres', OK.get((menet, n), 'NINCS OK -- ellenőrizendő')
        ki.append([str(menet), str(n), t['kategoria'], unicodedata.normalize('NFC', w['alak']), str(elotag_hossz),
                   'igen' if w['makkef'] else 'nem', '|'.join(elf), pref, gepi, allapot, ok])
    return ki


def main():
    sorok = esetek(1) + esetek(2)
    fej = ['minta', 'sorszam', 'kategoria', 'heber', 'elotag_hossz', 'makkef', 'elfogadott', 'preferalt',
           'gepi', 'allapot', 'ok']
    with open(KI, 'w', encoding='utf-8', newline='\n') as f:
        f.write('# A heber_kiejtes.py tesztesetei a két kalibráló mintából (DT-F131y). GENERÁLT: naplok/HEBER_KIEJTES_tesztesetek.py\n')
        f.write('# scope=naplok/HEBER_KIEJTES_kalibracio*.json + _kulcs.json + _valasztas.txt | forras=naplok/HEBER_KIEJTES_tesztesetek.py | ts=2026-10-30\n')
        f.write('\t'.join(fej) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    for m in ('1', '2'):
        ms = [s for s in sorok if s[0] == m]
        print('%s. minta: %d eset, egyezik %d, ismert eltérés %d' % (
            m, len(ms), sum(s[9] == 'egyezik' for s in ms), sum(s[9] == 'ismert_elteres' for s in ms)))
    for s in sorok:
        if s[9] != 'egyezik':
            print(' ', s[0], s[1], s[3], s[8], '|', s[6], '|', s[10])


if __name__ == '__main__':
    main()
