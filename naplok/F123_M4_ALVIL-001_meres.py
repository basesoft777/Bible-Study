"""F123 X.M4 (ALVIL-001): a migráció mérése — (c) visszaírás, (d) egység két rétegben, és a próza ↔ adat számai.

(c) A forrásból kinyerés: a `general.py --cel kinyeres` jelentése (0 új jelölt-sor) — itt a forrás jelölőit számolja
    (JELÖLT, ADAT-HIV, ADAT-ÉRTÉK: kinyerő/ellenőrző jelölő nincs, tehát visszaírás sincs), és hogy generált jelölő
    (GENERÁLT-KEZDET/-VÉGE, GENERÁLT:, ÜRES-BLOKK, ÜRES-NYELV) nem áll a forrásban.
(d) Egység két rétegben: a régi tanulmány minden `archivum`/`generalt`/`adat` egységének 8-szavas n-gramjai közül hány
    áll az új forrásban (elvárt: 0, kivéve a `forras` egységekkel közös szakaszokat — azokat a mérés kiveszi).
(számok) A forrásban álló számok és a ténylegesen lefutott lekérdezések (`adat/auditok.tsv` ALVIL-001) és az adat
    (`adat/elofordulasok.tsv`) összevetése.

    python naplok/F123_M4_ALVIL-001_meres.py
"""
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

GY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORRAS = os.path.join(GY, 'motivumok', 'ALVIL-001.md')
REGI = os.path.join(GY, 'archivum', 'ALVIL-001', 'Hadesz_Seol_tematikus.md')
TABLA = os.path.join(GY, 'naplok', 'F123_szetvalasztas_ALVIL-001.tsv')


def tsv(ut):
    L = [l.rstrip('\n').rstrip('\r').split('\t') for l in open(ut, encoding='utf-8') if not l.startswith('#')]
    return [dict(zip(L[0], r)) for r in L[1:] if r and r[0]]


def ngram(s, n=8):
    w = re.findall(r'\w+', s.lower())
    return {' '.join(w[i:i + n]) for i in range(len(w) - n + 1)}


def main():
    f = open(FORRAS, encoding='utf-8').read()
    regi = open(REGI, encoding='utf-8').read().replace('\r\n', '\n').split('\n')[1:]
    # (c)
    kinyero = {k: f.count(k) for k in ('<!-- JELÖLT:', '<!-- ADAT-HIV:', '<!-- ADAT-ÉRTÉK:')}
    generalt = {k: f.count(k) for k in ('GENERÁLT-KEZDET', 'GENERÁLT-VÉGE', 'GENERÁLT:', 'ÜRES-BLOKK', 'ÜRES-NYELV')}
    print('(c) kinyerő/ellenőrző jelölő a forrásban:', kinyero)
    print('(c) generált jelölő a forrásban (elvárt 0):', generalt)
    # (d)
    T = tsv(TABLA)
    forras_ng = set()
    for r in T:
        if r['fajl'].endswith('Hadesz_Seol_tematikus.md') and r['kategoria'] == 'forras':
            for n in range(int(r['sor_tol']), int(r['sor_ig']) + 1):
                forras_ng |= ngram(regi[n - 1])
    f_ng = ngram(f)
    kozos = 0
    peldak = []
    for r in T:
        if r['fajl'].endswith('Hadesz_Seol_tematikus.md') and r['kategoria'] != 'forras':
            for n in range(int(r['sor_tol']), int(r['sor_ig']) + 1):
                ng = (ngram(regi[n - 1]) & f_ng) - forras_ng
                if ng:
                    kozos += len(ng)
                    peldak.append((n, r['kategoria'], sorted(ng)[:2]))
    print('(d) nem-forras egység 8-gramja a forrásban (a forras egységekkel közös nélkül; elvárt 0):', kozos)
    for p in peldak[:10]:
        print('    ', p)
    # számok
    aud = [l.rstrip('\n').split('\t') for l in open(os.path.join(GY, 'adat', 'auditok.tsv'), encoding='utf-8')
           if l.startswith('ALVIL-001\t')]
    def n_of(parancs_strong, scope):
        for a in aud:
            if 'strong=%s' % parancs_strong in a[2] and scope in a[2]:
                yield int(re.search(r'\| n=(\d+)', a[2]).group(1))
    E = [l.rstrip('\n').split('\t') for l in open(os.path.join(GY, 'adat', 'elofordulasok.tsv'), encoding='utf-8')
         if l.startswith('ALVIL-001\t')]
    osz_sor = sum(1 for e in E if e[6] == 'H7585')
    print('számok: H7585 scan n =', sorted(set(n_of('H7585', 'TAHOT-teljes'))), '| G0086 scan n =',
          sorted(set(n_of('G0086', 'TAGNT-teljes'))), '| elofordulasok ÓSZ-sor (strong=H7585) =', osz_sor,
          '| ÚSZ-sor =', len(E) - osz_sor)
    for minta in (r'64 egyedi igehelyen', r'tíz ᾍδης-előfordulásban', r'63 egyedi igehelyen', r'64 egyedi verset',
                  r'nyers 66-os', r'63 új igehely'):
        print('  a forrásban: %-28s %d×' % (minta, len(re.findall(minta, f))))


if __name__ == '__main__':
    main()
