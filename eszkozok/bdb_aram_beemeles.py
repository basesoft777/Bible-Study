#!/usr/bin/env python
"""Az arámi pótlás beemelése a BDB fő táblába (F72, #72; N51).

Bemenet (csak olvas): konkordancia/BDB_aram_potlas.tsv (F66; az elfogadott sorok: egyertelmu +
kezi_elfogadott), konkordancia/BDB_teljes_unabridged.tsv, konkordancia/BDB_strong_alias.tsv.

Felhasználói döntés (N51, 2026-10-06): a duplikált sorok (mérőszám >= 0,8) NEM szövegsorként,
hanem alias-sorként kerülnek be a héber testvérsorra mutatva; szöveges pótlásként csak a valódi
hiányok (mérőszám < 0,8: 5 részleges + H6433) mennek a fő tábla végére. H0004, H3769, H5013
(nem elfogadott állapot) jelölt marad.

Módok:
  --m0 [--kimenet MAPPA]   szárazfutás: a két bővítést a MAPPÁBA írja (alapértelmezés: a repón kívüli
                           ideiglenes könyvtár), a repót nem érinti; --kivonat FÁJL a szöveges összesítőt írja
  --m2 --jovahagyva        éles írás: alias-sorok a BDB_strong_alias.tsv végére, 6 sor a fő tábla végére
                           (a meglévő bájtok prefixként változatlanok). Jóváhagyás nélkül nem fut.

A mérés a `bdb_aram_potlas.py --duplikacio` módszere (importált segédfüggvényekkel), de 3 tizedesre.
TSV-olvasás split('\\t'), írás '\\t'.join() (nem csv modul).
"""
import sys
import os
import argparse
import datetime
import tempfile
import subprocess

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bdb_aram_potlas as A  # noqa: E402
import bdb_strong_potlas as B  # noqa: E402

KUSZOB = 0.8
NL, TAB, CR = bytes([10]), bytes([9]), bytes([13])
# Indokolt felülírás (felhasználói döntés, 2026-10-07, chat; az F72 ellenőr-jelentése alapján): a legjobb
# mérőszámú sor helyett a megnevezett testvérsorra mutat az alias. A mérőszámot ennek a sornak a
# szövegén is kiszámolja a szkript (>= KUSZOB kell). A korábbi kizárások (H2298, H5839) téves alapon
# álltak: a szöveg mindkét esetben a testvérsor végén van; a `kezi_elfogadott` (H2298 -> BDB9285)
# döntés a szócikk-azonosításról szólt, nem a táblasorról.
TABLA_FELULIR = {
    'H5839': ('H5838', 'a legjobb mérőszámú sor a H5665 (Abed-Negó) volt; a H5838 sora (comrade of Daniel, '
                       '= נְגוֺ עֲבֵד) tartalmazza a BDB9760 szövegét, és az elvetett tábla testvére is H5838'),
}
# Kézi ellenőrzések eredménye (a szárazfutás-kivonatba kerül).
KEZI_ELLENORZES = {
    'H3606': 'H3606 -> H3605: elfogadva (arámi–héber kol, ugyanaz a lemma; a testvér az elvetett táblában H6903, '
             'de a szöveg a H3605 sorának végén áll)',
}
KIZAR = {}
MARKER = 'bdb_aram_beemeles.py'
ELFOGADOTT = ('egyertelmu', 'kezi_elfogadott')
PROV_SABLON = ('scope=konkordancia/BDB_aram_potlas.tsv + konkordancia/BDB_teljes_unabridged.tsv | '
               'forras=eszkozok/bdb_aram_potlas.py --duplikacio (ujjlenyomat-meres >= 0,8: a szocikk szovege mar a '
               'heber testversor sorvegen all; beemeles: eszkozok/bdb_aram_beemeles.py --m2; arami masodlagos '
               'Strong; N51, felhasznaloi dontes 2026-10-06) | ts=%s')


def olvas(path):
    with open(path, encoding='utf-8', newline='') as f:
        sorok = [l.split('\t') for l in f.read().split('\n') if l]
    return sorok[0], sorok[1:]


def szamol(ts):
    """A beemelés számítása a repó állapotából; visszaad: (alias_sorok, potlas_sorok, tobbi)."""
    fej, ki = A.olvas_tabla()
    fo = []
    aram_kulcsok = {r['Strong_padded'] for r in ki}  # a pótlás-tábla Strongjai: az idempotens méréshez kimaradnak
    with open(B.TABLA, encoding='utf-8', newline='') as f:
        for n, sor in enumerate(f.read().split('\n'), 1):
            if n == 1 or not sor:
                continue
            m = sor.split('\t', 2)
            if m[0] in aram_kulcsok:
                continue
            fo.append((n, m[0], A._ujj(m[2]), B.kons(m[2])))
    fo_kulcsok = {k for _, k, _, _ in fo}
    elv = {r['masodlagos_strong']: r for r in A.elvetett_aram()}
    alias, potlas, kimarad = [], [], []
    for r in ki:
        s = r['Strong_padded']
        if r['allapot'] not in ELFOGADOTT:
            kimarad.append((s, r['allapot']))
            continue
        torzs = r['Teljes_szocikk'].split(' ', 2)[2] if r['Teljes_szocikk'].count(' ') >= 2 else r['Teljes_szocikk']
        u = A._ujj(torzs)
        szeletek = {u[i:i + 12] for i in range(max(1, len(u) - 11))}
        ck = B.kons(r['cimszo'])
        legjobb = (0.0, 0, '')
        for n, k, uj, ko in fo:
            if ck not in ko:
                continue
            h = sum(1 for x in szeletek if x in uj) / len(szeletek)
            if h > legjobb[0]:
                legjobb = (h, n, k)
        if s in TABLA_FELULIR:
            cel = TABLA_FELULIR[s][0]
            sor_cel = [(n, k, uj) for n, k, uj, ko in fo if k == cel]
            assert len(sor_cel) == 1, cel
            h = sum(1 for x in szeletek if x in sor_cel[0][2]) / len(szeletek)
            assert h >= KUSZOB, (s, cel, h)
            legjobb = (h, sor_cel[0][0], cel)
        if legjobb[0] >= KUSZOB and s in KIZAR:
            kimarad.append((s, 'kizárt: ' + KIZAR[s].split(';')[0]))
        elif legjobb[0] >= KUSZOB:
            tars = elv[s]['testver_strong'] if s in elv else ''
            alias.append({'s': s, 'tabla': legjobb[2], 'sor': legjobb[1], 'bid': r['bdb_id'],
                          'cim': r['cimszo'], 'h': legjobb[0], 'tars_elv': tars,
                          'elv_egyezik': bool(tars) and legjobb[2] in tars.split(',')})
        else:
            potlas.append({'s': s, 'bid': r['bdb_id'], 'h': legjobb[0],
                           'sor': '\t'.join([s, 'H' + str(int(s[1:])), r['Teljes_szocikk'].replace('\t', ' ')]),
                           'reszleges': legjobb[0] >= 0.5})
    return alias, potlas, kimarad, fo_kulcsok


def ellenoriz(alias, potlas, kimarad, fo_kulcsok):
    """Ütközések és kulcs-létezés; visszaad egy hibalistát (üres = rendben)."""
    hibak = []
    _, regi_alias = olvas(B.ALIAS)
    regi_masod = {r[0] for r in regi_alias if MARKER not in r[-1]}  # a saját korábbi sorok újraépíthetők
    for a in alias:
        if a['tabla'] not in fo_kulcsok:
            hibak.append('a testvérkulcs nincs a fő táblában: %s -> %s' % (a['s'], a['tabla']))
        if a['s'] in fo_kulcsok:
            hibak.append('az arámi Strong már a fő táblában van: %s' % a['s'])
        if a['s'] in regi_masod:
            hibak.append('már az alias-táblában: %s' % a['s'])
    for p in potlas:
        if p['s'] in fo_kulcsok:
            hibak.append('a pótlás kulcsa már a fő táblában van: %s' % p['s'])
        if p['s'] in regi_masod:
            hibak.append('a pótlás kulcsa az alias-táblában van: %s' % p['s'])
    for lista, nev in ((alias, 'alias'), (potlas, 'pótlás')):
        ks = [x['s'] for x in lista]
        if len(ks) != len(set(ks)):
            hibak.append('duplikált kulcs a %s listában' % nev)
    if {a['s'] for a in alias} & {p['s'] for p in potlas}:
        hibak.append('egy Strong alias is és pótlás is')
    tiltott = {s for s, _ in kimarad}
    if tiltott & ({a['s'] for a in alias} | {p['s'] for p in potlas}):
        hibak.append('jelölt Strong került a beemelésbe')
    return hibak


def alias_sorok_szoveg(alias, ts):
    prov = PROV_SABLON % ts
    return [('\t'.join([a['s'], a['tabla'], a['bid'], 'aram', a['cim'], '%.3f' % a['h'], prov]) + '\n') for a in alias]


def potlas_sorok_szoveg(potlas):
    return [p['sor'] + '\n' for p in potlas]


def m0(kimenet, kivonat, ts):
    alias, potlas, kimarad, fo_kulcsok = szamol(ts)
    hibak = ellenoriz(alias, potlas, kimarad, fo_kulcsok)
    os.makedirs(kimenet, exist_ok=True)
    with open(os.path.join(kimenet, 'alias_uj_sorok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(alias_sorok_szoveg(alias, ts)))
    with open(os.path.join(kimenet, 'fo_tabla_uj_sorok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(''.join(potlas_sorok_szoveg(potlas)))
    nem_elv = [a for a in alias if not a['elv_egyezik']]
    L = ['# BDB_ARAM_BEEMELES — szárazfutás kivonata (F72, M0)\n',
         '*Generálta: `python eszkozok/bdb_aram_beemeles.py --m0` · scope=konkordancia/BDB_aram_potlas.tsv + '
         'konkordancia/BDB_teljes_unabridged.tsv + konkordancia/BDB_strong_alias.tsv | '
         'forras=eszkozok/bdb_aram_beemeles.py --m0 | ts=%s*\n' % ts,
         'A kivonat a szárazfutás eredménye (a `--m0` a repó fájljait nem írja).\n',
         '- Kézi ellenőrzés: %s Indokolt felülírás: %s.\n' % (' '.join(KEZI_ELLENORZES.values()), '; '.join(
             '%s -> %s (%s)' % (k, v[0], v[1]) for k, v in TABLA_FELULIR.items()) or '—'),
         '- Alias-jelölt (mérőszám >= 0,8): **%d**; szöveges pótlás: **%d** (ebből részleges 0,5–0,8: %d); jelölt marad: %d (%s).' % (
             len(alias), len(potlas), sum(1 for p in potlas if p['reszleges']), len(kimarad),
             ', '.join('%s (%s)' % x for x in kimarad)),
         '- Ütközés / hiba: %s.' % ('nincs' if not hibak else '; '.join(hibak)),
         '- Minden alias-sor testvérkulcsa létezik a fő táblában: %s.' % ('igen' if not any('nincs a fő' in h for h in hibak) else 'NEM'),
         '- Az alias-sorok testvére szerepel a #57 elvetett táblájának `testver_strong` oszlopában: %d/%d.' % (
             len(alias) - len(nem_elv), len(alias)),
         '- Ahol nem (kézi ellenőrzésre): %s.\n' % ('; '.join('%s -> %s (elvetett-tábla testvére: %s)' % (
             a['s'], a['tabla'], a['tars_elv'] or '—') for a in nem_elv) or '—'),
         '## A 6 szöveges pótlás (a fő tábla végére)\n']
    for p in potlas:
        szoveg = p['sor'].split('\t')[2]
        L.append('- **%s** (%s, mérőszám %.2f): %s … *(%d karakter)*' % (p['s'], p['bid'], p['h'], szoveg[:200], len(szoveg)))
    L.append('\n## Az alias-sorok mintája (első 6 és az elvetett táblában nem szereplő testvérű sor)\n')
    L.append('| masodlagos_strong | tabla_strong | bdb_id | nyelv | szoveg_hasonlosag |')
    L.append('|---|---|---|---|---|')
    minta = alias[:6] + [a for a in nem_elv if a not in alias[:6]]
    for a in minta:
        L.append('| %s | %s | %s | aram | %.3f |' % (a['s'], a['tabla'], a['bid'], a['h']))
    L.append('\nTeljes lista: a `--kimenet` mappa `alias_uj_sorok.tsv` fájlja (a repón kívül). Proveniencia-sablon: `%s`' % (PROV_SABLON % ts))
    if kivonat:
        with open(kivonat, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(L) + '\n')
    print('M0 kész: alias %d, pótlás %d, jelölt %d, hiba %d' % (len(alias), len(potlas), len(kimarad), len(hibak)))
    for h in hibak:
        print('HIBA:', h)
    return alias, potlas, hibak


def m2(ts):
    alias, potlas, kimarad, fo_kulcsok = szamol(ts)
    hibak = ellenoriz(alias, potlas, kimarad, fo_kulcsok)
    if hibak:
        raise SystemExit('megállok: ' + '; '.join(hibak))
    if len(alias) != 164 or len(potlas) != 6:
        raise SystemExit('megállok: a várt 164 alias / 6 pótlás helyett %d / %d' % (len(alias), len(potlas)))
    # fő tábla: a 6 sor a végén; ha már ott áll, nem írunk újra
    uj_fo = ''.join(potlas_sorok_szoveg(potlas)).encode('utf-8')
    with open(B.TABLA, 'rb') as f:
        fo = f.read()
    if CR in fo or not fo.endswith(NL):
        raise SystemExit('CRLF vagy hiányzó záró újsor: fő tábla')
    if fo.endswith(uj_fo):
        print('fő tábla: a 6 pótlás már a végén áll, változatlan')
    else:
        kulcsok = {l.split(TAB)[0].decode() for l in fo.split(NL)}
        if any(p['s'] in kulcsok for p in potlas):
            raise SystemExit('megállok: a pótlás kulcsa részben már a fő táblában')
        with open(B.TABLA, 'wb') as f:
            f.write(fo + uj_fo)
    # alias-tábla: a saját korábbi sorok (MARKER a proveniencián) újraépítése; a többi bájtra azonos
    with open(B.ALIAS, 'rb') as f:
        al = f.read()
    if CR in al or not al.endswith(NL):
        raise SystemExit('CRLF vagy hiányzó záró újsor: alias-tábla')
    nl, tab = NL.decode(), TAB.decode()
    sorok = al.decode('utf-8').split(nl)[:-1]
    regi = [l for l in sorok if MARKER not in l.split(tab)[-1]]
    regi_bajt = (nl.join(regi) + nl).encode('utf-8')
    r = subprocess.run(['git', 'show', 'origin/main:konkordancia/BDB_strong_alias.tsv'], capture_output=True, cwd=B.GYOKER)
    if r.returncode == 0 and regi_bajt != r.stdout:
        raise SystemExit('megállok: a nem-F72 alias-sorok nem azonosak az origin/main tartalmával')
    utana = regi_bajt + ''.join(alias_sorok_szoveg(alias, ts)).encode('utf-8')
    with open(B.ALIAS, 'wb') as f:
        f.write(utana)
    print('M2 kész: %d alias-sor, %d szöveges pótlás' % (len(alias), len(potlas)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--m0', action='store_true')
    ap.add_argument('--m2', action='store_true')
    ap.add_argument('--jovahagyva', action='store_true')
    ap.add_argument('--kimenet', default=os.path.join(tempfile.gettempdir(), 'bdb_aram_beemeles_szaraz'))
    ap.add_argument('--kivonat', default=None)
    ap.add_argument('--ts', default=datetime.date.today().isoformat())
    a = ap.parse_args()
    if a.m0:
        m0(a.kimenet, a.kivonat, a.ts)
    if a.m2:
        if not a.jovahagyva:
            raise SystemExit('az éles írás a felhasználói jóváhagyás után, --jovahagyva kapcsolóval fut')
        m2(a.ts)


if __name__ == '__main__':
    main()
