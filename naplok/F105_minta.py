"""F105 (FELADATOK #105) ⛔ 3. lépés előkészítése: 50 idézetes kézi minta és az ütközéslista.

Bemenet: a `naplok/F105_meres.py` futamtáblája (`F105_futamok.tsv`, a `--be` könyvtárban).
  - Jelölt halmaz: a futamok, amelyeket a mai megjelenítés (DT445) nem javít (`dt445` = `jelolt_marad`, `nincs_sor`,
    `reszleges`), és a hivatkozott vers a lexikon nélküli R_hib-et igazolja, a forrásalakot nem (`itelet` = `F0_M0_R1`).
  - Minta: 50 futam a jelölt halmazból, véletlenszerűen (seed 105), Strong és pozíció szerint rendezve.
  - Ütközés: a DT445 `javitva` vagy `valodi_sorrend` sora, ahol a hivatkozott vers a lexikon nélküli R_hib-et igazolja, a megjelenített alakot
    nem (a DT445 bármely TAHOT-versen mért; ez a hivatkozott versen mér).
A helyreállított alak: a lexikon nélküli R_hib (`F105_meres.py`: geres nélkül R0, geresnél a DT445 R_str-je), utána a rafe-maqqéf feloldása (a U+05BF-et hordozó, nem első betű elé
maqqéf U+05BE, a rafe ki; az előző betű végbetű-alakra, ha van). Csak ebben a mintában áll: a megjelenítés nem változott.
A vers héber szövege (csak olvasásra; a gépi ellenőrzés a TAHOT-on fut): a Macula (`Macula_heber_*.tsv`) szavai a `karoli`
oszlop szerinti Károli-versen, a morfémák az `xml_id` szerint szóvá fűzve (a TAHOT morfématagolása szóhatárt nem ad).

Kimenet: `--ki-md` (a napló mintatáblája, Markdown) és `--ki-utkozes` (TSV).
Futtatás: python naplok/F105_minta.py --be <könyvtár> --ki-md <fájl> --ki-utkozes <fájl>
"""
import argparse
import os
import random
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KONK = os.path.join(REPO, 'konkordancia')
RAFE, MAQQEF = 'ֿ', '־'
VEG = dict(zip('כמנפצ', 'ךםןףץ'))


def tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r').split('\t') for s in f if not s.startswith('#')]
    return [dict(zip(sorok[0], s)) for s in sorok[1:]]


def betu(c):
    return 'א' <= c <= 'ת'


def maqqef(token):
    """A rafe-maqqéf feloldása egy tokenben (l. a docstringet)."""
    s = unicodedata.normalize('NFD', token)
    ki, utolso = [], None          # utolso: a legutóbbi betű indexe a `ki`-ben
    for c in s:
        if betu(c):
            utolso = len(ki)
        if c == RAFE and utolso:
            # az utolso betű elé maqqéf; az előtte álló (az első szó utolsó) betűje végbetű
            elozo = max((j for j in range(utolso) if betu(ki[j])), default=None)
            if elozo is not None and ki[elozo] in VEG:
                ki[elozo] = VEG[ki[elozo]]
            ki.insert(utolso, MAQQEF)
            utolso += 1
            continue
        ki.append(c)
    return unicodedata.normalize('NFC', ''.join(ki))


def vers_szoveg(morfemak):
    """[(xml_id, szó)] → szavak szóközzel; az azonos szóhoz (xml_id utolsó jegye nélkül) tartozó morfémák egybe."""
    szavak = {}
    for xid, m in morfemak:
        szavak.setdefault(xid[:-1], []).append(m)
    return ' '.join(''.join(v) for _k, v in sorted(szavak.items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--be', required=True)
    ap.add_argument('--ki-md', required=True)
    ap.add_argument('--ki-utkozes', required=True)
    a = ap.parse_args()
    futam = tsv(os.path.join(a.be, 'F105_futamok.tsv'))
    jelolt = [d for d in futam if d['itelet'] == 'F0_M0_R1' and d['dt445'] in ('jelolt_marad', 'nincs_sor', 'reszleges')]
    utk = [d for d in futam if d['itelet'] == 'F0_M0_R1' and d['dt445'] in ('javitva', 'valodi_sorrend')]
    rnd = random.Random(105)
    minta = sorted(rnd.sample(jelolt, 50), key=lambda d: (d['strong'], int(d['poz'])))
    kell = {d['karoli_vers'] for d in minta + utk}
    vers = {}
    for fn in sorted(os.listdir(KONK)):
        if fn.startswith('Macula_heber_') and fn.endswith('.tsv'):
            for d in tsv(os.path.join(KONK, fn)):
                for kv in (d.get('karoli') or '').split(';'):
                    if kv.strip() in kell:
                        vers.setdefault(kv.strip(), []).append((d['xml_id'], d['szo']))
    with open(a.ki_md, 'w', encoding='utf-8', newline='\n') as f:
        f.write('| # | Strong | DT445 | nyers forrás | helyreállított alak | vers | a vers héber szövege (Macula) | kézi ítélet |\n')
        f.write('|---|---|---|---|---|---|---|---|\n')
        for i, d in enumerate(minta, 1):
            hely = ' '.join(maqqef(t) for t in d['r_hib'].split(' '))
            f.write('| %d | %s | %s | %s | %s | %s | %s |  |\n' % (
                i, d['strong'], d['dt445'], d['forras'], hely, d['karoli_vers'], vers_szoveg(vers.get(d['karoli_vers'], []))))
    with open(a.ki_utkozes, 'w', encoding='utf-8', newline='\n') as f:
        f.write('strong\tpoz\tdt445\tforras\tmegjelenites\tr_hib\tkaroli_vers\tvers_macula\n')
        for d in utk:
            f.write('\t'.join([d['strong'], d['poz'], d['dt445'], d['forras'], d['megjelenites'], d['r_hib'], d['karoli_vers'],
                               vers_szoveg(vers.get(d['karoli_vers'], []))]) + '\n')
    print('jelölt:', len(jelolt), '| minta:', len(minta), '| ütközés:', len(utk),
          '| a mintában rafe-maqqéf:', sum(d['rafe_maqqef'] == '1' for d in minta),
          '| geres:', sum(d['geres'] == '1' for d in minta))


if __name__ == '__main__':
    main()
