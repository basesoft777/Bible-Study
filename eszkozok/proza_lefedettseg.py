"""Próza-lefedettség és próza-egyenetlenség mérése egy motívumon (F125, JELENTÉS szint).

Olvas: motivumok/[ID].md (a kézi próza), adat/elofordulasok.tsv, adat/kapcsolatok.tsv,
adat/motivum_kapcsolatok.tsv, adat/jeloltek.tsv. Nem ír adatot; a kimenet stdout vagy --kimenet.

Lefedettség: mely adatlelet nincs megnevezve a prózában (előfordulás, kapcsolat,
motívumközi kapcsolat, nyitott jelölt). Egyenetlenség: az egy elemre jutó próza hossza
a blokkok között. Nem ítél minőségről. A névmatch heurisztika (l. megnevezett()).
"""
import argparse
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = Path(__file__).resolve().parent.parent
CSOPORTOS = re.compile(r'\d+\s+(?:egyedi\s+)?igehely')  # „63 egyedi igehelyen”: gyűjtő mondat
KEVES_PROZA = 150      # karakter/elem alatt „kevés” (M0 javaslat, DT-F125a)
ELTERES_ARANY = 4.0    # két blokk elemre jutó prózája ennyiszeres eltérés fölött jelölt
MIN_ELEM = 3           # ennél kevesebb elemű blokkot nem hasonlítunk


def tsv(nev, gyoker=GYOKER):
    sorok = (Path(gyoker) / 'adat' / nev).read_text(encoding='utf-8').split('\n')
    sorok = [s for s in sorok if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t') + [''] * len(fej))) for s in sorok[1:]]


def bekezdesek(id_, gyoker=GYOKER):
    """[(blokk, szöveg)] — a kézi próza bekezdései; táblasor, jelölő és napló kihagyva."""
    szoveg = (Path(gyoker) / 'motivumok' / f'{id_}.md').read_text(encoding='utf-8')
    blokk, ki = '(fej)', []
    for par in re.split(r'\n\s*\n', szoveg):
        p = par.strip()
        m = re.match(r'(#{2,3})\s+(.*)', p)
        if m and m.group(1) == '##':
            blokk = m.group(2).split('\n')[0][:60]
        if not p or p.startswith(('<!--', '【NAPLO', '|')):
            continue
        if p.startswith('#') and '\n' not in p:
            continue
        ki.append((blokk, p))
    return ki


def igehely_bontas(ih):
    """'Zsolt 116:4,13,17' -> ('Zsolt', 116, {4,13,17}); fejezet-tartomány esetén None."""
    m = re.match(r'^(\S+(?: \S+)?)\s+(\d+):([\d,\-–\s]+)', ih.strip())
    if not m:
        m = re.match(r'^(\S+)\s+(\d+)()$', ih.strip())
        return (m.group(1), int(m.group(2)), set()) if m else None
    versek = set()
    for t in re.split(r'\s*,\s*', m.group(3).strip()):
        r = re.split(r'[-–]', t)
        try:
            a, b = int(r[0]), int(r[-1])
        except ValueError:
            continue
        versek.update(range(a, b + 1))
    return m.group(1), int(m.group(2)), versek


def megnevezett(ih, par):
    """Igaz, ha a bekezdés megnevezi az igehelyet (könyv fejezet:vers, vagy a könyv
    említése mellett puszta fejezet:vers). Heurisztika: a vershatár-eltérések és a
    „12. vers” szóbeli alakok nem látszanak."""
    b = igehely_bontas(ih)
    if not b:
        return ih in par
    kony, fej, versek = b
    for m in re.finditer(re.escape(kony) + r'\s*' + str(fej) + r':([\d,\-–\s]+)', par):
        if not versek:
            return True
        vv = igehely_bontas(f'{kony} {fej}:{m.group(1)}')
        if vv and vv[2] & versek:
            return True
    if re.search(re.escape(kony) + r'\s*' + str(fej) + r'\b', par) and not versek:
        return True
    if kony in par:
        for m in re.finditer(r'(?<![\w:])' + str(fej) + r':([\d,\-–]+)', par):
            vv = igehely_bontas(f'{kony} {fej}:{m.group(1)}')
            if vv and (not versek or vv[2] & versek):
                return True
    return False


def mer(id_, gyoker=GYOKER):
    par = bekezdesek(id_, gyoker)
    el = [r for r in tsv('elofordulasok.tsv', gyoker) if r['id'] == id_]
    kap = [r for r in tsv('kapcsolatok.tsv', gyoker) if r['id'] == id_]
    mk = [r for r in tsv('motivum_kapcsolatok.tsv', gyoker) if id_ in (r['id_a'], r['id_b'])]
    nyit = [r for r in tsv('jeloltek.tsv', gyoker) if r['id'] == id_ and r['dontes'] == 'nyitva']

    # elemenként: a megnevezésüket tartalmazó bekezdések
    def lefed(kell):
        talal = []
        for blokk, p in par:
            if all(megnevezett(ih, p) for ih in kell):
                talal.append((blokk, p))
        return talal

    ered = {'el': [], 'kap': [], 'mk': [], 'nyit': []}
    for r in el:
        ered['el'].append((r, lefed([r['igehely']])))
    for r in kap:
        ered['kap'].append((r, lefed([r['forras_igehely'], r['cel_igehely']])))
    for r in mk:
        masik = r['id_b'] if r['id_a'] == id_ else r['id_a']
        sajat = r['igehely_a'] if r['id_a'] == id_ else r['igehely_b']
        t = [(b, p) for b, p in par if masik in p or megnevezett(sajat, p)]
        ered['mk'].append((r, t))
    for r in nyit:
        ered['nyit'].append((r, lefed([r['igehely']])))
    # DT-F125a: a gyűjtő mondat (szám + „igehely”) külön kategória, nem hamis hiány — csak az
    # előfordulásokra; melyik igehelyet fedi, a mérő nem tudja, ezért csak szám szerint kezeli
    csoportos = any(CSOPORTOS.search(p) for _, p in par)
    return par, ered, csoportos


def osszesit(id_, gyoker=GYOKER):
    """{rovat: (adat, megnevezve, csoportosan_fedett, hiany)} — a JELENTÉS-szabály bemenete."""
    _, ered, csoportos = mer(id_, gyoker)
    ki = {}
    for k, lista in ered.items():
        n = len(lista)
        meg = sum(1 for _, t in lista if t)
        nincs = n - meg
        csop = nincs if (k == 'el' and csoportos) else 0
        ki[k] = (n, meg, csop, nincs - csop)
    return ki


def sorcim(kat, r):
    if kat == 'el':
        return f"{r['igehely']} ({r['pardes_szint']})"
    if kat == 'kap':
        return f"{r['forras_igehely']} → {r['cel_igehely']} ({r['tipus']})"
    if kat == 'mk':
        return f"{r['id_a']} {r['igehely_a']} ↔ {r['id_b']} {r['igehely_b']} ({r['tipus']})"
    return f"{r['igehely']} ({r.get('jelolt_tipus', '')}; {r['indoklas'][:60]})"


def jelentes(id_):
    par, ered, csoportos = mer(id_)
    nev = {'el': 'előfordulás', 'kap': 'kapcsolat', 'mk': 'motívumközi kapcsolat',
           'nyit': 'nyitott jelölt'}
    ki = [f'## {id_}', '',
          f'Próza: {len(par)} bekezdés, {sum(len(p) for _, p in par)} karakter '
          f'(táblasor, jelölő és napló nélkül).', '',
          '### Lefedettség (a próza nem nevezi meg)', '',
          '| rovat | adat | megnevezve | csoportosan fedett | nem |', '|---|---|---|---|---|']
    hianyok = []
    for k in ('el', 'kap', 'mk', 'nyit'):
        h = [r for r, t in ered[k] if not t]
        csop = len(h) if (k == 'el' and csoportos) else 0
        ki.append(f'| {nev[k]} | {len(ered[k])} | {len(ered[k]) - len(h)} | {csop} | {len(h) - csop} |')
        if not csop:
            hianyok += [(k, r) for r in h]
    ki += ['', 'Név nélküli elemek (a csoportosan fedett előfordulás nélkül):', '']
    ki += [f'- {nev[k]}: {sorcim(k, r)}' for k, r in hianyok] or ['- nincs']
    ki += ['', '*A „Károli rejtett párhuzama” (14. szerep) nem mérhető: nincs gépi adatforrása '
           '(l. DT424); a mérő ezt nem tölti ki.*', '']

    # egyenetlenség: blokkonként elemszám és az elemre jutó próza
    ki += ['### Egyenetlenség (blokkonként)', '',
           '| blokk | karakter | megnevezett elem | karakter/elem | jel |', '|---|---|---|---|---|']
    blokkok = {}
    for k in ('el', 'kap', 'mk', 'nyit'):
        for r, t in ered[k]:
            for b in {b for b, _ in t}:
                blokkok.setdefault(b, set()).add((k, sorcim(k, r)))
    hossz = {}
    for b, p in par:
        hossz[b] = hossz.get(b, 0) + len(p)
    sur = {}
    for b, h in hossz.items():
        n = len(blokkok.get(b, ()))
        sur[b] = (h / n) if n else None
    ertek = [v for b, v in sur.items() if v and len(blokkok[b]) >= MIN_ELEM]
    kozep = sorted(ertek)[len(ertek) // 2] if ertek else None
    for b, h in hossz.items():
        n = len(blokkok.get(b, ()))
        jel = ''
        if n >= MIN_ELEM and sur[b] and sur[b] < KEVES_PROZA:
            jel = 'kevés próza az elemre'
        if kozep and n >= MIN_ELEM and sur[b] and (sur[b] > kozep * ELTERES_ARANY
                                                   or sur[b] < kozep / ELTERES_ARANY):
            jel = (jel + '; ' if jel else '') + f'a medián ({kozep:.0f}) {ELTERES_ARANY:.0f}x-ánál távolabb'
        ki.append(f'| {b} | {h} | {n} | {sur[b]:.0f} | {jel} |' if sur[b]
                  else f'| {b} | {h} | {n} | – | {jel} |')
    ki += ['', f'Küszöbök (javaslat, DT-F125a): kevés = {KEVES_PROZA} karakter/elem alatt; '
           f'eltérés = {ELTERES_ARANY:.0f}x a blokkok mediánjától; legalább {MIN_ELEM} megnevezett elem.']
    nevezett = {p for k in ered for _, t in ered[k] for _, p in t}
    ki += ['', 'Adatelemet egyáltalán nem megnevező bekezdés (értelmező, módszertani): '
           f'{sum(1 for _, p in par if p not in nevezett)} / {len(par)}']
    return '\n'.join(ki), hianyok


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('id', nargs='+')
    ap.add_argument('--kimenet')
    a = ap.parse_args()
    out = []
    for i in a.id:
        szoveg, _ = jelentes(i)
        out.append(szoveg)
    szoveg = '\n\n'.join(out) + '\n'
    if a.kimenet:
        Path(a.kimenet).write_text(szoveg, encoding='utf-8', newline='\n')
    else:
        print(szoveg)


if __name__ == '__main__':
    main()
