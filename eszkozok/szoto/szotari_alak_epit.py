"""F94.3/5 (FELADATOK #94): a teljes Károli szótárialak-táblája — `adat/szoto/karoli_szotari_alak.tsv` (generált).

A KIADOTT hibrid a C+K változat (DT-F94e, a felhasználó döntése, 2026-10-13): saját szabályok + kivételtábla + Károli-
lexikon + a felhasználó által ellenőrzött K tábla, **simplemma nélkül**. A szkript a simplemma importját letiltja
(`sys.modules['simplemma'] = None`), így a tábla akkor is simplemma nélkül készül, ha a csomag telepítve van; az A
változat itt nem futtatható.

Alakonként egy sor: a korpusz-lexikon minden írásmódja (kis- és nagybetűs alak külön, ahogy a szövegben áll).
Oszlopok (brief .3/5, SEMA 2.27): alak, szotari_alak, szotari_alak_mai, alapige, tovabbi_elfogadhato, modszer,
szabaly_forras, regies_jegy. A fejlécben `# GENERÁLT: …` proveniencia-sor, a v3 sha256-ja, a változat és a keresési
mód figyelmeztetése. Kézzel nem szerkeszthető: a javítás a kivételtáblában, a szabályban vagy a K táblában történik.

Használat: python eszkozok/szoto/szotari_alak_epit.py [--ts …] [--kimenet <tsv>]"""
import sys

sys.modules['simplemma'] = None  # a kiadott út simplemma nélkül (DT-F94e): az import ImportError-ral bukik

import argparse  # noqa: E402
import collections  # noqa: E402
import datetime  # noqa: E402
import hashlib  # noqa: E402
import os  # noqa: E402
import platform  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(ITT))
sys.path.insert(0, ITT)
import hibrid  # noqa: E402

KI = os.path.join(REPO, 'adat', 'szoto', 'karoli_szotari_alak.tsv')
OSZLOP = ['alak', 'szotari_alak', 'szotari_alak_mai', 'alapige', 'tovabbi_elfogadhato', 'modszer', 'szabaly_forras', 'regies_jegy']


def sha(p, n=None):
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return h[:n] if n else h


def alakok():
    ki = []
    for l in open(hibrid._LEX, encoding='utf-8'):
        if l.startswith('#') or l.rstrip('\n') == 'alak\tkisbetus\tnagy_belul\tnagy_kezdo':
            continue
        ki.append(l.split('\t')[0])
    return ki


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ts', default=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'))
    ap.add_argument('--kimenet', default=KI)
    a = ap.parse_args()
    if hibrid.simplemma is not None:
        sys.exit('HIBA: a simplemma betöltődött; a kiadott tábla simplemma nélkül készül')
    hibrid.valtozat('CK')
    sorok, modszer, jegy = [], collections.Counter(), collections.Counter()
    for w in alakok():
        e = hibrid.elemez(w)
        if e['modszer'] == 'simplemma':
            sys.exit(f'HIBA: simplemma-eredetű szótári alak: {w}')
        modszer[e['modszer']] += 1
        if e['regies_jegy']:
            jegy[e['regies_jegy']] += 1
        sor = [w] + [e[k] for k in OSZLOP[1:]]
        if any('\t' in x or '\n' in x for x in sor):
            sys.exit(f'HIBA: tab/sortörés: {w}')
        sorok.append(sor)
    with open(a.kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(f'# GENERÁLT: eszkozok/szoto/szotari_alak_epit.py (F94.3) — kézzel nem szerkeszthető | scope=a Károli 1908 korpusz-lexikonjának '
                f'minden írásmódja ({len(sorok)} alak) | forras=hibrid v3, C+K változat, simplemma nélkül (hibrid.py sha256:{sha(os.path.join(ITT, "hibrid.py"))}) '
                f'+ adat/szoto/gyakori_alakok.tsv (K tábla, felhasználó által ellenőrzött; sha256:{sha(hibrid._KTAB, 12)}) + adat/szoto/karoli_lexikon.tsv '
                f'(sha256:{sha(hibrid._LEX, 12)}; konkordancia/Karoli_1908.tsv, közkincs) | ts={a.ts}\n')
        f.write('# allapot: a kiadott hibrid a C+K (DT-F94e); a simplemma csak fejlesztési mérce, a táblába simplemma-eredetű szótári alak nem kerül. '
                'FIGYELEM, keresési mód: a mért pontosság a (c) módra érvényes (szótári alak VAGY Strong): a 4. (független) mintán az M2 (c) 98,4% '
                '(a K nélküli lemmákon 98,0%); tisztán szótári alakra keresve (a) a K nélküli lemmákon 91,8%, és a ritka alakokon alakonként '
                'gyengébb (N-F94g). A kereső (#76) a szótári alakot a Strong-ággal együtt használja.\n')
        f.write('# megjegyzes: modszer = k_tabla | kivetel | nev | szabaly | lexikon; szabaly_forras = korpusz_strong | manual | '
                'modell_ellenorizetlen | üres; regies_jegy értékkészlete: SEMA 2.27. A szótári alakok modell-állítások (szabály, kivételtábla) '
                'vagy a felhasználó által ellenőrzött K tábla; ismert korlátok: naplok/SZOTOVEZES_meres.md 11.6, 16. szakasz\n')
        f.write('\t'.join(OSZLOP) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    print(f'{a.kimenet}: {len(sorok)} sor | Python {platform.python_version()} | modszer: {dict(modszer)} | regies_jegy: {dict(jegy)}')


if __name__ == '__main__':
    main()
