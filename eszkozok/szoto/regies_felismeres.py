"""F94.2 / K6 (FELADATOK #94): a teljes Károli leggyakoribb N „régies igealakként felismert” szóalakja a szigorítás
előtt (hibrid_v2) és után (hibrid, v3), a kézi besoroláshoz (ige / nem ige; a besorolás a naplóba kerül, manual).

„Felismert régies igealak”: a köznévi ágon a régies igevégződés-réteg (`_regies_ige`) fogadta el az alakot
(a kivételtábla és a név-ág előtte kiszűrve); a v3-ban a mai felszólító -j- leválasztás (nem régies) nem számít.
A gyakoriság a korpusz-lexikon kisbetűs + mondatkezdő előfordulása (kisbetűsítve).

Használat: python eszkozok/szoto/regies_felismeres.py [--n 200] [--valtozat A]   (markdown a standard kimenetre)"""
import argparse
import collections
import datetime
import hashlib
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ITT)
import hibrid  # noqa: E402
import hibrid_v2  # noqa: E402


def gyakorisag():
    """Kisbetűsített alak -> előfordulás; és a név-alakok halmaza: amelyek nagybetűs írásmódja a mondat belsejében
    gyakoribb, mint a kisbetűs (a hibrid névágán mennek, a köznévi régies igeréteg nem éri el őket; pl. Szela)."""
    f = collections.Counter()
    nb_max, kis = collections.Counter(), collections.Counter()
    for l in open(hibrid._LEX, encoding='utf-8'):
        if l.startswith('#') or l.rstrip('\n') == 'alak\tkisbetus\tnagy_belul\tnagy_kezdo':
            continue
        w, k, nb, nk = l.rstrip('\n').split('\t')
        f[w.lower()] += int(k) + int(nk)
        kis[w.lower()] += int(k)
        nb_max[w.lower()] = max(nb_max[w.lower()], int(nb))
    return f, {w for w in f if nb_max[w] > kis[w]}


def v2_regies(w):
    """A v2 köznévi ága a régies igeréteg előtt; visszaadja a régies igeként kapott tövet, vagy None-t."""
    m = hibrid_v2
    if m._kivetel(w):
        return None
    w2 = m._helyesiras(w)
    if m._kivetel(w2):
        return None
    if w2.endswith('ök') and not m._ismert(w2) and m._ismert(w2[:-2] + 'ük'):
        w2 = w2[:-2] + 'ük'
    return m._regies_ige(w2)


def v3_regies(w):
    e = hibrid.elemez(w)
    r = [n for n in hibrid._NYOM if n[0] == 'R' and n[1] != 'jm']
    if not r or e['modszer'] != 'szabaly':
        return None
    return e['szotari_alak_mai'], r[0][1], e['regies_jegy']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--n', type=int, default=200)
    ap.add_argument('--valtozat', default='A')
    a = ap.parse_args()
    hibrid.valtozat(a.valtozat)
    hibrid_v2.valtozat('A' if a.valtozat == 'A' else 'C')
    f, nevek = gyakorisag()
    rend = sorted(f.items(), key=lambda x: (-x[1], x[0]))
    elotte, utana = [], []
    for w, n in rend:
        if w in nevek:
            continue
        if len(elotte) < a.n:
            t = v2_regies(w)
            if t:
                elotte.append((w, n, t))
        if len(utana) < a.n:
            t = v3_regies(w)
            if t:
                utana.append((w, n) + t)
        if len(elotte) >= a.n and len(utana) >= a.n:
            break
    ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:12]
    print(f'#### Előtte (hibrid_v2, {a.valtozat}): a {a.n} leggyakoribb felismert régies igealak\n')
    print('; '.join(f'{w} ({n}) → {t}' for w, n, t in elotte))
    print(f'\n#### Utána (hibrid v3, {a.valtozat}): a {a.n} leggyakoribb felismert régies igealak (végződés, jegy)\n')
    print('; '.join(f'{w} ({n}) → {t} [{j}]' for w, n, t, v, j in utana))
    print(f'\nscope=a teljes Károli korpusz-lexikona ({len(f)} kisbetűsített alak) | forras=eszkozok/szoto/regies_felismeres.py + '
          f'hibrid_v2.py (sha256:{h(os.path.join(ITT, "hibrid_v2.py"))}) + hibrid.py (sha256:{h(os.path.join(ITT, "hibrid.py"))}) + '
          f'karoli_lexikon.tsv (sha256:{h(hibrid._LEX)}) | ts={ts}')


if __name__ == '__main__':
    main()
