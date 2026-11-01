#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 22.9 — a könyvjelentés (`naplok/F22_<könyv>_jelentes.md`) számainak összeállítása szkriptkimenetekből.

Olvas: adat/karoli_strong/{parok,szavak}_<könyv>.tsv, f22/api_termeles/{futasnaplo,batchek}.tsv,
adat/karoli_strong/nem_tr_parositott.tsv, f22/kezi_versek_<könyv>.tsv, f22/minta_<könyv>.tsv,
f21p/prompt_v3.sha256; a f22_statisztika.py, f22_elemzes.py és tokenszint_vershatar.py kimenetét
(alfolyamatként). Nem hív hálózatot; a Markdown a --ki fájlba (vagy a standard kimenetre) megy.

Használat:
    python eszkozok/karoli_strong/f22_konyvjelentes.py --konyv Mt --cimke d_mt_1 --csomag D --ki naplok/F22_Mt_jelentes.md
"""

import argparse
import glob
import json
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

_ITT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _ITT)
import sonnet_koteg  # noqa: E402
import tokenek  # noqa: E402

ROOT = tokenek.ROOT


def tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def alfolyamat(*arg):
    env = dict(os.environ, PYTHONIOENCODING='utf-8')
    r = subprocess.run([sys.executable] + list(arg), cwd=ROOT, capture_output=True, text=True, encoding='utf-8', env=env)
    return r.stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--konyv', required=True)
    ap.add_argument('--cimke', required=True, help='a batch-címke (batchek.tsv)')
    ap.add_argument('--csomag', required=True)
    ap.add_argument('--ki', default=None)
    ap.add_argument('--megjegyzes', default=None, help='a jelentés végére kerülő kézi megjegyzés (egy bekezdés)')
    a = ap.parse_args()
    k = a.konyv
    n = sonnet_koteg.ascii_nev(k)
    minta = tsv(os.path.join(ROOT, 'f22', 'minta_%s.tsv' % n))
    vers = len(minta)
    kotegek = (vers + 9) // 10
    log = [r for r in tsv(os.path.join(ROOT, 'f22', 'api_termeles', 'futasnaplo.tsv')) if r['futas'] == 'api_termeles/high/%s' % n]
    koltseg = sum(float(r['koltseg_usd'] or 0) for r in log)
    bem = sum(int(r['bemenet_token'] or 0) for r in log)
    kim = sum(int(r['kimenet_token'] or 0) for r in log)
    javito = sorted({int(r['koteg']) for r in log if r['probalkozas'] == '2'})
    munka = sorted(glob.glob(os.path.join(ROOT, 'f22', 'api_termeles', 'high', '_munka', '%s_k*.json' % n)))
    json_hiba = [os.path.basename(f)[len(n) + 2:-5] for f in munka if 'nem érvényes JSON' in json.dumps(json.load(open(f, encoding='utf-8')).get('uzenet'), ensure_ascii=False)]
    hashek = sorted({r['prompt_sha256_12'] for r in log})
    batch = [r for r in tsv(os.path.join(ROOT, 'f22', 'api_termeles', 'batchek.tsv')) if r['cimke'] == a.cimke]
    parok = tsv(os.path.join(ROOT, 'adat', 'karoli_strong', 'parok_%s.tsv' % n))
    szavak = tsv(os.path.join(ROOT, 'adat', 'karoli_strong', 'szavak_%s.tsv' % n))
    hu = [s for s in szavak if s['oldal'] == 'hu']
    er = [s for s in szavak if s['oldal'] == 'er']

    def db(lista, allapot):
        return sum(1 for s in lista if s['allapot'] == allapot)
    karoli_szo = len(hu)
    er_token = len(er)
    tagnt = [r for r in tokenek._sorok(tokenek.TAGNT) if r[0].rsplit(' ', 1)[0] == k]
    import re
    nem_tr = [r for r in tagnt if not re.search(r'\bTR\b|TR»|TR«', r[7])]
    nem_tr_p = [r for r in tsv(os.path.join(ROOT, 'adat', 'karoli_strong', 'nem_tr_parositott.tsv')) if r['vers'].rsplit(' ', 1)[0] == k]
    kezi_ut = os.path.join(ROOT, 'f22', 'kezi_versek_%s.tsv' % n)
    kezi = tsv(kezi_ut) if os.path.exists(kezi_ut) else []
    hash_hiba = sonnet_koteg.prompt_hash_hiba()
    stat = alfolyamat('eszkozok/karoli_strong/f22_statisztika.py', '--konyv', k).strip().split('\n')
    elemzes = alfolyamat('eszkozok/karoli_strong/f22_elemzes.py', '--konyv', k).split('\n')
    arany = [s for s in elemzes if s.startswith('- **Mért érték') or s.startswith('- Minden régi-arany')]
    vh = alfolyamat('eszkozok/karoli_strong/tokenszint_vershatar.py', '--lazabb', k).strip().split('\n')
    ell = alfolyamat('eszkozok/karoli_strong/egyesit.py', '--konyv', k, '--ellenoriz').strip().split('\n')[-1]

    L = []
    w = L.append
    w('# F22_%s_jelentes.md — a %s könyv Károli–Strong párosítása (22.9 %s csomag)\n' % (n, k, a.csomag))
    w('*Proveniencia: scope=%s (%d Károli-vers, %d TAGNT-token) | forras=`adat/karoli_strong/{parok,szavak}_%s.tsv`, `f22/api_termeles/futasnaplo.tsv`, `batchek.tsv`, `f22_statisztika.py`, `f22_elemzes.py`, `egyesit.py`, `tokenszint_vershatar.py`, `nem_tr_lista.py` (szkriptkimenetek, split(\'\\t\'); összeállítás: `f22_konyvjelentes.py`) | ts=2026-11-01. Módszer: D45, DT-F22i/j és a brief 22.9 szerint: Sonnet, Message Batches API, `effort=high`, `prompt_v3` változatlanul (`prompt_sha256_12` = %s), csak-Sonnet (DT-F22c).*\n' % (k, vers, len(tagnt), n, ', '.join(hashek)))
    w('## 1. Menet\n')
    w('- **Versbeosztás:** `naplok/F22_versbeosztas_jovahagyas.md` (orkesztrátori jóváhagyás, 2026-11-01); `tokenek.VERSBEOSZTAS_JOVAHAGYOTT` bővítve.')
    w('- **Minta:** `f22/minta_%s.tsv`, %d vers a modellhez, %d köteg.' % (n, vers, kotegek))
    w('- **Batchek** (`f22/api_termeles/batchek.tsv`, címke `%s`):' % a.cimke)
    for b in batch:
        w('  - %d. kör: `%s`, %s kérés, beküldve %s' % (int(b['kor']), b['batch_id'], b['kerelmek_db'], b['ts']))
    w('- **Futásnapló** (%s: %d sor): modell `%s`, `%s`, `koltseg_forras=%s`; a `prompt_sha256_12` minden sorban %s (bájtszintű hash, mint a C csomagban). **P3:** `sonnet_koteg.prompt_hash_hiba()` a jelentés összeállításakor: %s (az LF-normalizált tartalom sha256-ja egyezik az `f21p/prompt_v3.sha256`-tal).\n' % (
        n, len(log), log[0]['modell'], log[0]['gondolkodas_mod'], log[0]['koltseg_forras'], ', '.join(hashek), 'nincs hiba' if not hash_hiba else 'HIBA: %s' % hash_hiba))
    w('## 2. Eredmény\n')
    w('| mutató | érték |\n|---|---|')
    w('| Károli-vers / modellhez ment | %d / %d |' % (vers, vers))
    w('| hívás | %d |' % len(log))
    w('| %s | %s |' % ('kapuhiba (f22_statisztika.py)', stat[0].replace('|', '/')))
    w('| javító körbe került köteg | %d: %s |' % (len(javito), ', '.join('k%03d' % x for x in javito)))
    w('| ebből egész köteg formátumhiba (érvénytelen JSON, `_munka/%s_k*.json`) | %d%s |' % (n, len(json_hiba), (': ' + ', '.join('k' + x for x in json_hiba)) if json_hiba else ''))
    w('| link (`parok_%s.tsv`) | %d, bizonyosság: %s, forrás: %s |' % (n, len(parok), ', '.join('%s %d' % (b, sum(1 for p in parok if p['bizonyossag'] == b)) for b in sorted({p['bizonyossag'] for p in parok})), ', '.join(sorted({p['forras'] for p in parok}))))
    w('| szósor (`szavak_%s.tsv`) | %d = %d Károli + %d eredeti |' % (n, len(szavak), karoli_szo, er_token))
    w('| Károli-oldal: párosítva / betoldás / fuggoben | %d / %d / %d |' % (db(hu, 'parositva'), db(hu, 'betoldas'), db(hu, 'fuggoben')))
    w('| eredeti oldal: párosítva / fordítatlan / fuggoben | %d / %d / %d |' % (db(er, 'parositva'), db(er, 'forditatlan'), db(er, 'fuggoben')))
    w('| költség | %.4f USD (%.5f USD/vers; bemenet %d, kimenet %d token) |\n' % (koltseg, koltseg / vers, bem, kim))
    w('`egyesit.py --konyv %s --ellenoriz`: „%s” (P1: a szósorok száma a Károli- és az eredeti tokenek összegével egyezik; P2: a `strong` a TAGNT-ből levezethető). Mivel csak a Sonnet futott, nincs `magas` bizonyosság: minden link `alacsony`, forrás `S`.\n' % (k, ell))
    w('**Régi arany** (`konkordancia/Karoli_Strong_kivonat.tsv`, kizárás nélkül):')
    for s in arany:
        w(s)
    w('\n## 3. Tokenszintű vershatár és kézi versek (N-F22e)\n')
    w('A `tokenszint_vershatar.py --lazabb %s` kimenete:\n' % k)
    w('```')
    for s in vh:
        w(s)
    w('```\n')
    if kezi:
        w('`f22/kezi_versek_%s.tsv` (link nélkül, `fuggoben`; a pótlás az N-F22e-é): %s.\n' % (n, ', '.join(r['igehely'] for r in kezi)))
    else:
        w('A könyvben nincs `kezi` kényszerített vers.\n')
    w('## 4. A `[nem TR]` tokenek: %d, ebből %d párosított\n' % (len(nem_tr), len(nem_tr_p)))
    w('A párosítottak a jelölőtáblában (`adat/karoli_strong/nem_tr_parositott.tsv`, D45 (a)):\n')
    if nem_tr_p:
        w('| vers | er | alak | Strong | Károli-szó |\n|---|---|---|---|---|')
        for r in nem_tr_p:
            w('| %s | %s | %s | %s | %s |' % (r['vers'], r['er_sorszam'], r['er_szo'], r['strong'], r['hu_szo']))
    else:
        w('(nincs párosított)')
    # a `[nem TR]` tokenek állapot szerinti bontása (P4): a nem párosítottak vagy `forditatlan`, vagy listázva
    sorsz, nem_tr_all = {}, set()
    for r in tagnt:
        sorsz[r[0]] = sorsz.get(r[0], 0) + 1
        if not re.search(r'\bTR\b|TR»|TR«', r[7]):
            nem_tr_all.add((r[0], sorsz[r[0]]))
    allapot = {}
    for sz in er:
        if (sz['vers'], int(sz['sorszam'])) in nem_tr_all:
            allapot.setdefault(sz['allapot'], []).append(sz)
    w('\n**A `[nem TR]` tokenek állapota (`szavak_%s.tsv`):** %s.' % (n, ', '.join('%s %d' % (x, len(v)) for x, v in sorted(allapot.items()))))
    if allapot.get('fuggoben'):
        w('\nNem `forditatlan`, hanem `fuggoben` (a `kezi` versek tokenjei, link nélkül): ' + ', '.join('%s er %s (%s, %s)' % (x['vers'], x['sorszam'], x['szo'], x['strong']) for x in allapot['fuggoben']) + '.')
    w('\n**Figyelem:** a `[nem TR]` jelölés azt mondja, hogy a párosított eredeti token nem a TR-ben áll; a link a kritikai szöveg alakjáé (D45 (a)), a Károli forrásszövege (TR) ettől eltérhet, ezért a Strong-szám nem feltétlenül a Károli szavának lexikai megfelelője.')
    if a.megjegyzes:
        w('\n' + a.megjegyzes)
    s = '\n'.join(L) + '\n'
    if a.ki:
        with open(os.path.join(ROOT, a.ki), 'w', encoding='utf-8', newline='\n') as f:
            f.write(s)
    else:
        print(s)


if __name__ == '__main__':
    main()
