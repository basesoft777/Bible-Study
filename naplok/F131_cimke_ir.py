"""F131.1: az `adat/szotar_szakasz_cimke.tsv` írása (DT-F131b 2., DT-F131c 1.+(a) átmenet: 2., DT-F131d (a)).

A tábla kézi (manual proveniencia); ez a szkript csak a kézzel rögzített sorokat
írja ki, és a Thayer G1941 kézi szakaszhatárait (hu_kezdet, hu_hossz) a
`forditasok.tsv` `Thayer G1941 teljes` magyar sorából számolja ki a lent
rögzített kezdő szövegrészek helyéről. A címkék szövege a végrehajtó
javaslata (DT-F131d (a)); jóváhagyásuk a DT-F131f-nél.

Ha a tábla már létezik, írás előtt összeveti a sorokat az újonnan
előállítottakkal, és eltérésnél megáll (CLAUDE.md TSV-szabály; minta:
eszkozok/igazolas_migracio.py). `--felulir` csak akkor ír eltérő tartalmat.

Olvasás `split('\\t')`, írás `'\\t'.join()`; a `csv` modul nem használható.

    python naplok/F131_cimke_ir.py [--felulir]
"""
import hashlib
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CEL = os.path.join(GYOKER, 'adat', 'szotar_szakasz_cimke.tsv')
TS = '2026-10-26'
FEJLEC = ['szotar', 'strong', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu',
          'hu_kezdet', 'hu_hossz', 'forditas_hash', 'proveniencia', 'megjegyzes']
PROV = 'scope=manual | forras=F131 (DT-F131b–d, a végrehajtó javaslata; jóváhagyás: DT-F131f) | ts=%s' % TS
PROV_THAYER = ('scope=G1941 | forras=adat/forditasok.tsv (Thayer G1941 teljes) kézi határokkal, '
               'naplok/F131_cimke_ir.py (DT-F131c 2., átmenet a #142-ig) | ts=%s' % TS)

# (szotar, strong, szakasz, lexikon_jelentes_szam, cimke_hu, megjegyzes)
KEZI = [
    ('BDB', 'H7121', 'Qal/2/c', '2.c', 'segítségül hívni', ''),
    ('BDB', 'H7121', 'Qal/3/-', '3', 'kihirdetni', ''),
    ('BDB', 'H7121', 'Qal/3/b', '', 'a nevet kihirdetni', ''),
    ('BDB', 'H8034', '-/3/-', '', 'név: Isten megjelölése', ''),
    ('BDB', 'H8034', '-/4/-', '', 'név: hamis istenekről', ''),
    ('TBESG', 'G1941', '2', '2', 'segítségül hívni, folyamodni valakihez',
     'a TBESG tagolása (a lexikon_hivatkozasok.tsv kulcsa); DT-F131c (a)'),
]

# A Thayer G1941 magyar `teljes` sorának kézi határai: a szakasz a megadott
# szövegrész első előfordulásánál kezdődik; a cím a szöveg elején.
THAYER_HATAR = [
    ('cim', None, '', ''),
    ('fej', 'ἐπικαλῶ (epikaló):', '', ''),
    ('-/1/-', '1. nevet tenni valakire', 'elnevezni', ''),
    ('-/2/-', '2. ἐπικαλεῖται τό ὄνομα', '', ''),
    ('-/3/-', '3. τίνι (tini), a tárgy', '', ''),
    ('-/4/-', '4. segítségül hívni (mint a német anrufen)', '', ''),
    ('-/5/-', '5. héber mintára', 'segítségül hívni a név kimondásával', ''),
]


def tabla(rel):
    fej = None
    sorok = []
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        for nyers in f:
            s = nyers.rstrip('\n')
            if not s or s.startswith('#'):
                continue
            m = s.split('\t')
            if fej is None:
                fej = m
                continue
            sorok.append(dict(zip(fej, m + [''] * (len(fej) - len(m)))))
    return sorok


def thayer_sorok():
    teljes = [r for r in tabla('adat/forditasok.tsv')
              if r['szotar'] == 'Thayer' and r['strong'] == 'G1941' and r['jelentes_szam'] == 'teljes'
              and r['mezo'] == 'forditas_hu']
    if len(teljes) != 1:
        sys.exit('HIBA: a Thayer G1941 teljes sora nem egyértelmű (%d)' % len(teljes))
    hu = teljes[0]['forditas_hu']
    h = hashlib.sha1(hu.encode('utf-8')).hexdigest()
    utvonalak = [r['utvonal'] for r in tabla('adat/thayer_szakaszok.tsv') if r['strong'] == 'G1941']
    if utvonalak != [t[0] for t in THAYER_HATAR]:
        sys.exit('HIBA: a thayer_szakaszok G1941 útvonalai eltérnek: %r' % utvonalak)
    kezdetek = []
    for ut, minta, _c, _m in THAYER_HATAR:
        if minta is None:
            kezdetek.append(0)
            continue
        if hu.count(minta) != 1:
            sys.exit('HIBA: a(z) %s határmintája nem egyszer áll (%d): %r' % (ut, hu.count(minta), minta))
        kezdetek.append(hu.index(minta))
    if kezdetek != sorted(kezdetek):
        sys.exit('HIBA: a határok nem növekvők: %r' % kezdetek)
    out = []
    for i, (ut, _minta, cimke, megj) in enumerate(THAYER_HATAR):
        k = kezdetek[i]
        v = kezdetek[i + 1] if i + 1 < len(kezdetek) else len(hu)
        szelet = hu[k:v].rstrip()
        out.append(['Thayer', 'G1941', ut, '', cimke, str(k), str(len(szelet)), h, PROV_THAYER, megj])
    return out


def main():
    felulir = '--felulir' in sys.argv[1:]
    sorok = [[sz, st, ut, ljsz, c, '', '', '', PROV, megj] for sz, st, ut, ljsz, c, megj in KEZI]
    sorok += thayer_sorok()
    szoveg = '\t'.join(FEJLEC) + '\n' + ''.join('\t'.join(s) + '\n' for s in sorok)
    for s in sorok:
        if any('\t' in x or '\n' in x for x in s):
            sys.exit('HIBA: tab vagy sortörés egy mezőben: %r' % s)
    if os.path.exists(CEL):
        with open(CEL, encoding='utf-8') as f:
            regi = f.read()
        if regi == szoveg:
            print('változatlan: %s (%d sor)' % (CEL, len(sorok)))
            return
        regi_sorok = regi.split('\n')
        uj_sorok = szoveg.split('\n')
        for i in range(max(len(regi_sorok), len(uj_sorok))):
            a = regi_sorok[i] if i < len(regi_sorok) else '<nincs>'
            b = uj_sorok[i] if i < len(uj_sorok) else '<nincs>'
            if a != b:
                print('eltérés a(z) %d. sorban:\n  régi: %s\n  új:   %s' % (i + 1, a, b))
        if not felulir:
            sys.exit('MEGÁLL: a tábla eltér; --felulir nélkül nem írok.')
    with open(CEL, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)
    print('megírva: %s (%d sor)' % (CEL, len(sorok)))


if __name__ == '__main__':
    main()
