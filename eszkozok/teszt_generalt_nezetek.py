#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teszt_generalt_nezetek.py -- F217.4: az `eszkozok/generalt_nezetek.py` tesztje.

Esetek: a jegyzék kapuja (a valós jegyzéken, és negatív esetekkel); a sorrend; a befagyasztott lap kimarad;
a kiadott lap őrzése (a három kivétellel); az idempotencia és a dátumszabály (hamis generátorral, ideiglenes
git-repóban); a hiba nem ír félig; a kivezetett E28-lista tiltása. A valós lapgenerátort nem futtatja (azt a
CI ideiglenes generálása és az E28 méri).

Fut: python eszkozok/teszt_generalt_nezetek.py (a CI szabály-teszt lépésében is). Kilépési kód: 0 = zöld.
"""

import os
import shutil
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import generalt_nezetek as G

HIBAK = []
OSZLOP = G.OSZLOPOK

HAMIS_GEN = r'''# -*- coding: utf-8 -*-
import os, sys
args = sys.argv[1:]
azon = args[args.index('--id') + 1]
ki = args[args.index('--kimenet') + 1]
gyoker = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tartalom = open(os.path.join(gyoker, 'adat', 'forras.txt'), encoding='utf-8').read()
if 'HIBA' in tartalom:
    sys.exit(4)
os.makedirs(os.path.join(ki, 'lexikon'), exist_ok=True)
with open(os.path.join(ki, 'lexikon', azon + '_TUDOMANYOS.md'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('<!-- GENERÁLT: hamis | ts=%s -->\n%s' % (os.environ['PARDES_DATUM'], tartalom))
'''

HAMIS_EXPORT = r'''# -*- coding: utf-8 -*-
import os, sys
ki = sys.argv[sys.argv.index('--kimenet') + 1]
gyoker = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.makedirs(ki, exist_ok=True)
for nev in os.listdir(os.path.join(gyoker, 'lexikon')):
    with open(os.path.join(gyoker, 'lexikon', nev), encoding='utf-8') as f:
        sorok = f.read().split('\n')
    with open(os.path.join(ki, nev + '.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(sorok[-1])
'''


def ellenoriz(feltetel, nev):
    if feltetel:
        print('RENDBEN  ' + nev)
    else:
        print('BUKOTT   ' + nev)
        HIBAK.append(nev)


def _ir(gy, relut, szoveg):
    ut = os.path.join(gy, *relut.split('/'))
    os.makedirs(os.path.dirname(ut), exist_ok=True)
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write(szoveg)


def _sor(azon, **m):
    alap = {'id': azon, 'utvonal': 'lexikon/<ID>_TUDOMANYOS.md', 'leiras': 'teszt',
            'parancs': 'python eszkozok/hamis_gen.py --id {id} --kimenet {gyoker}', 'bemenetek': '-',
            'utana': '-', 'orzes': 'kiadas;befagyasztas', 'determinizmus': 'det:PARDES_DATUM', 'kapuk': '-',
            'gazda': 'action', 'futtato': 'jegyzek', 'allapot': 'aktiv', 'forras': 'manual'}
    alap.update(m)
    return '\t'.join(alap[o] for o in OSZLOP)


def _jegyzek(gy, *sorok, fej=None):
    _ir(gy, G.JEGYZEK, '# teszt\n' + '\t'.join(fej or OSZLOP) + '\n' + '\n'.join(sorok) + '\n')


def _git(gy, *args):
    subprocess.run(['git'] + list(args), cwd=gy, check=True, capture_output=True)


def _repo():
    """Ideiglenes git-repó hamis generátorral, egy kiadott (A-001) és egy befagyasztott (B-001) lappal."""
    gy = tempfile.mkdtemp(prefix='teszt_gn_')
    _ir(gy, 'eszkozok/hamis_gen.py', HAMIS_GEN)
    _ir(gy, 'eszkozok/hamis_export.py', HAMIS_EXPORT)
    _ir(gy, 'adat/forras.txt', 'tartalom-1')
    _ir(gy, 'adat/lap_befagyasztas.tsv', 'id\tok\tdontes\tdatum\nB-001\tteszt\tteszt\t2026-11-15\n')
    _ir(gy, 'adat/kiadasok.tsv', '# teszt\nid\tkiadas\tdatum\tvaltozas\tproza_modell\tforras\n'
                                 'A-001\t1\t2026.11.01\tteszt\tmanual\tmanual\n')
    _ir(gy, 'adat/lap_javitasok.tsv', '# teszt\nid\thely\n')
    for azon in ('A-001', 'B-001', 'C-001'):
        _ir(gy, 'motivumok/%s.md' % azon, 'forrás\n')
    _ir(gy, 'lexikon/A-001_TUDOMANYOS.md', '<!-- GENERÁLT: hamis | ts=2026-01-01 -->\ntartalom-1')
    _ir(gy, 'lexikon/B-001_TUDOMANYOS.md', '<!-- GENERÁLT: hamis | ts=2026-01-01 -->\nrégi, befagyasztott')
    _jegyzek(gy, _sor('G01'),
             _sor('G07', utvonal='kimenet/', parancs='python eszkozok/hamis_export.py --kimenet {gyoker}/kimenet',
                  utana='G01', orzes='szabad', determinizmus='det', bemenetek='G01'))
    _git(gy, 'init', '-q')
    _git(gy, 'config', 'user.email', 'teszt@example.invalid')
    _git(gy, 'config', 'user.name', 'teszt')
    _git(gy, 'config', 'core.autocrlf', 'false')
    _git(gy, 'add', '-A')
    env = dict(os.environ, GIT_COMMITTER_DATE='2026-03-04T12:00:00Z', GIT_AUTHOR_DATE='2026-03-04T12:00:00Z')
    subprocess.run(['git', 'commit', '-q', '-m', 'alap'], cwd=gy, check=True, capture_output=True, env=env)
    return gy


def _olvas(gy, relut):
    with open(os.path.join(gy, *relut.split('/')), encoding='utf-8') as f:
        return f.read()


def teszt_valos_jegyzek():
    hibak = G.jegyzek_ellenoriz()
    ellenoriz(not hibak, 'a valós jegyzék átmegy a kapun' + ('' if not hibak else ': %s' % hibak[:3]))
    ids = [d['id'] for d in G.futtatando()]
    ellenoriz(ids.index('G07') > ids.index('G01'), 'sorrend: a nyílt mag (G07) a lap (G01) után')
    ellenoriz('G08' not in ids and 'G11' not in ids, 'a workflow- és a kézi sort a végrehajtó nem futtatja')
    ellenoriz(not G.regi_lista_ellenoriz(), 'a kivezetett E28-listában nincs adatsor')


def teszt_negativ():
    eset = [
        ('rossz fejléc', None, {'fej': OSZLOP[:-1]}),
        ('rossz id', _sor('X01'), {}),
        ('ismeretlen őrzés', _sor('G01', orzes='kiadas;valami'), {}),
        ('ismeretlen determinizmus', _sor('G01', determinizmus='talan'), {}),
        ('ismeretlen kapu', _sor('G01', kapuk='E99'), {}),
        ('üres mező', _sor('G01', leiras=''), {}),
        ('nem létező utana', _sor('G01', utana='G05'), {}),
        ('nem futtatható parancs', _sor('G01', parancs='python eszkozok/nincs.py --kimenet {gyoker}'), {}),
        ('nemdet az Actionben', _sor('G01', determinizmus='nemdet'), {}),
        ('hibás bemenet', _sor('G01', bemenetek='C12'), {}),
    ]
    for nev, sor_, extra in eset:
        gy = tempfile.mkdtemp(prefix='teszt_gnn_')
        try:
            _ir(gy, 'eszkozok/hamis_gen.py', HAMIS_GEN)
            if extra.get('fej'):
                _jegyzek(gy, _sor('G01'), fej=extra['fej'])
            else:
                _jegyzek(gy, sor_)
            ellenoriz(bool(G.jegyzek_ellenoriz(gy)), 'a kapu jelzi: %s' % nev)
        finally:
            shutil.rmtree(gy, ignore_errors=True)
    gy = tempfile.mkdtemp(prefix='teszt_gnn_')
    try:
        _ir(gy, 'eszkozok/hamis_gen.py', HAMIS_GEN)
        _jegyzek(gy, _sor('G01', utana='G02'), _sor('G02', utana='G01'))
        ellenoriz(any('kör' in h for h in G.jegyzek_ellenoriz(gy)), 'a kapu jelzi: kör az utana-ban')
        _jegyzek(gy, _sor('G01', bemenetek='B01;B99'))
        ellenoriz(not G.jegyzek_ellenoriz(gy), 'bemeneti jegyzék nélkül a B-hivatkozás nem bukik')
        _ir(gy, G.BEMENETI_JEGYZEK, '# teszt\nid\tutvonal\nB01\tadat/x.tsv\n')
        ellenoriz(any('B99' in h for h in G.jegyzek_ellenoriz(gy)), 'a kapu jelzi: a B99 nincs a bemeneti jegyzékben')
        _jegyzek(gy, _sor('G01'))
        _ir(gy, G.REGI_LISTA, 'id\tfajl\tcel\tmelyseg\tfeladat\tdatum\nA-001\tlexikon/A-001_TUDOMANYOS.md\tlexikon\tapparatus\t1\t-\n')
        ellenoriz(any('kivezetve' in h for h in G.jegyzek_ellenoriz(gy)), 'a kapu tiltja a régi lista adatsorát')
    finally:
        shutil.rmtree(gy, ignore_errors=True)


def teszt_ir_es_orzes():
    gy = _repo()
    try:
        ellenoriz(G.aktiv_lapok(gy) == ['A-001'], 'a befagyasztott (B-001) és a lap nélküli (C-001) kimarad')
        # 1. idempotencia: a bemenet nem változott -> nincs írás
        kod, jel = G.ir(gy)
        ellenoriz(kod == 0 and 'ts=2026-01-01' in _olvas(gy, 'lexikon/A-001_TUDOMANYOS.md'),
                  'változatlan bemenet: a lap és a dátuma marad (%d)' % kod)
        ellenoriz(_olvas(gy, 'kimenet/A-001_TUDOMANYOS.md.txt') == 'tartalom-1', 'a lap utáni sor (G07) lefutott')
        # 2. a kiadott lap tartalma változna, kivétel nélkül -> nem íródik ki, kód 2
        _ir(gy, 'adat/forras.txt', 'tartalom-2')
        kod, jel = G.ir(gy)
        ellenoriz(kod == 2 and 'tartalom-1' in _olvas(gy, 'lexikon/A-001_TUDOMANYOS.md'),
                  'őrzött lap: kivétel nélkül nem változik (kód %d)' % kod)
        # 3. (c) új lapjavítás-sor -> átmegy, a HEAD dátumával
        _ir(gy, 'adat/lap_javitasok.tsv', '# teszt\nid\thely\nA-001\t1/a\n')
        kod, jel = G.ir(gy)
        lap = _olvas(gy, 'lexikon/A-001_TUDOMANYOS.md')
        ellenoriz(kod == 0 and 'tartalom-2' in lap, '(c) új lap_javitasok-sor: a lap változhat (kód %d)' % kod)
        ellenoriz('ts=2026-03-04' in lap, 'dátumszabály: tartalomváltozáskor a HEAD commit dátuma')
        ellenoriz(_olvas(gy, 'kimenet/A-001_TUDOMANYOS.md.txt') == 'tartalom-2', 'a nyílt mag a friss lapból')
        kod, _ = G.ir(gy)
        ellenoriz(kod == 0 and _olvas(gy, 'lexikon/A-001_TUDOMANYOS.md') == lap, 'idempotencia: a második futás nem ír')
        _git(gy, 'add', '-A')
        _git(gy, 'commit', '-q', '-m', 'lap')
        # 4. (b) csak DT-szám
        _ir(gy, 'adat/forras.txt', 'tartalom-2 DT-F12a')
        _ir(gy, 'lexikon/A-001_TUDOMANYOS.md', lap + ' DT812')
        _git(gy, 'add', '-A')
        _git(gy, 'commit', '-q', '-m', 'dt')
        kod, _ = G.ir(gy)
        ellenoriz(kod == 0 and 'DT-F12a' in _olvas(gy, 'lexikon/A-001_TUDOMANYOS.md'),
                  '(b) csak DT-szám változik: átmegy (kód %d)' % kod)
        _git(gy, 'add', '-A')
        _git(gy, 'commit', '-q', '-m', 'dt2')
        # 5. (a) új kiadás
        _ir(gy, 'adat/forras.txt', 'tartalom-3')
        kod, _ = G.ir(gy)
        ellenoriz(kod == 2, 'kiadás nélkül újra őrzött (kód %d)' % kod)
        with open(os.path.join(gy, 'adat', 'kiadasok.tsv'), 'a', encoding='utf-8', newline='\n') as f:
            f.write('A-001\t2\t2026.11.15\tteszt\tmanual\tmanual\n')
        kod, _ = G.ir(gy)
        ellenoriz(kod == 0 and 'tartalom-3' in _olvas(gy, 'lexikon/A-001_TUDOMANYOS.md'),
                  '(a) új kiadasok-sor: a lap változhat (kód %d)' % kod)
        # 6. generálási hiba -> semmi nem íródik, kód 1
        elotte = _olvas(gy, 'lexikon/A-001_TUDOMANYOS.md')
        _ir(gy, 'adat/forras.txt', 'HIBA')
        kod, jel = G.ir(gy)
        ellenoriz(kod == 1 and _olvas(gy, 'lexikon/A-001_TUDOMANYOS.md') == elotte,
                  'generálási hiba: kód 1, a lap érintetlen (%d)' % kod)
        # 7. átnézés a repón kívül
        _ir(gy, 'adat/forras.txt', 'tartalom-4')
        cel = tempfile.mkdtemp(prefix='teszt_gnk_')
        try:
            G.ROOT, regi_root = gy, G.ROOT
            kod, _ = G.gyoker_mod(cel)
        finally:
            G.ROOT = regi_root
        ellenoriz(kod == 0 and 'tartalom-4' in _olvas(cel, 'lexikon/A-001_TUDOMANYOS.md')
                  and 'tartalom-3' in _olvas(gy, 'lexikon/A-001_TUDOMANYOS.md'),
                  '--gyoker: a repón kívül generál, a repóba nem ír')
        shutil.rmtree(cel, ignore_errors=True)
    finally:
        shutil.rmtree(gy, ignore_errors=True)


def teszt_nincs_regi_fogyaszto():
    """A kivezetett lista nevét csak ez a modul és a tesztjei ismerik (a kapu tiltja a nyerset)."""
    gyoker = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    engedett = {'generalt_nezetek.py', 'teszt_generalt_nezetek.py'}
    talalt = []
    for gy, _, nevek in os.walk(os.path.join(gyoker, 'eszkozok')):
        for n in nevek:
            if n.endswith('.py') and n not in engedett:
                with open(os.path.join(gy, n), encoding='utf-8', errors='replace') as f:
                    if 'e28_migralt_nezetek' in f.read():
                        talalt.append(n)
    ellenoriz(not talalt, 'a kivezetett E28-listát egy szkript sem olvassa' + ('' if not talalt else ': %s' % talalt))


def teszt_dt_normalizalas():
    """3.4 (b): a számkiosztás a lapon a DT-tokent és a feloldott döntésdátumot hozza (lexikon_general _DT_RX)."""
    ellenoriz(G._dt_norm('(szerkesztői döntés) DT-F12a') == G._dt_norm('(szerkesztői döntés, 2026-10-19) DT812'),
              '(b) a feloldott döntésdátum és a DT-szám egyaránt normalizált')
    ellenoriz(G._dt_norm('2026-10-19 más szöveg') != G._dt_norm('2026-10-20 más szöveg'),
              '(b) a döntésen kívüli dátum nem normalizált')


def main():
    teszt_dt_normalizalas()
    teszt_valos_jegyzek()
    teszt_negativ()
    teszt_ir_es_orzes()
    teszt_nincs_regi_fogyaszto()
    print('\n%s: %d bukott' % ('BUKOTT' if HIBAK else 'RENDBEN', len(HIBAK)))
    return 1 if HIBAK else 0


if __name__ == '__main__':
    sys.exit(main())
