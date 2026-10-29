"""F131.3.10: a #121-nek — a 8 lexikonoldal ószövetségi soraihoz szükséges UBS DBH egységek (DT-F131j).

Csak olvas (kivéve a kimeneti TSV-t). Minden motívum (`adat/elofordulasok.tsv`), amelynek lexikonoldala van
(`lexikon/<ID>_TUDOMANYOS.md`), minden ÓSZ-sora, minden H-tokenje: a Károli-vers MT-re képezve
(`lexikon_general.karoli_mt_vers`, ugyanaz, mint a render), a `UBS_DBH_referenciak.tsv` hivatkozásai
→ egyedi (strong, lexid). Mezőnként (`definicio_hu`: ezt mutatja az „UBS-jelentés” cella; `glosszak_hu`:
a #121 egységszámításának párja) a `forditasok.tsv` jelenléte (`UBS_DBH`, entry_id = lexid,
jelentes_szam = —, nem `elavult`).

A #121 mai DBH-egységei: a 8 lexikonoldal héber „5. Tömör jelentés” tábláinak `(fordításra vár)` sorai
(Strong + lexid, mezőnként), ugyanúgy, ahogy a #121 a 454 egységét számolta. Mert az éles `lexikon/` 7 lapja a
generátorhoz képest elavult (DT344), a lapokat a mai generátor rendereli a repón kívülre (`--renderek`); az
ISTENTISZT-001-é az éles lap (a F131 előtti render; a próbarender a gerinc miatt DBH-táblát már nem hordoz).

Kimenet: naplok/F131_DBH_egysegek.tsv (lexikon, strong, lexid, mezo, van_hu) és összesítés a stdout-ra.
TSV `split('\\t')` / `'\\t'.join()`.

    python eszkozok/general.py --cel lexikon --kimenet <DIR a repón kívül>
    python naplok/F131_dbh_meres.py --renderek <DIR>
"""
import datetime
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(GYOKER, 'eszkozok'))

import general as G  # noqa: E402
import lexikon_general as LG  # noqa: E402

KI = os.path.join(GYOKER, 'naplok', 'F131_DBH_egysegek.tsv')
MEZOK = ('definicio_hu', 'glosszak_hu')


def f121_dbh_egysegek(lap):
    """{(strong, lexid, mezo)} a lap héber 5. szerepének DBH-táblájából, ahol `(fordításra vár)` áll."""
    with open(lap, encoding='utf-8') as f:
        szoveg = f.read()
    out = set()
    if '### Héber szavak' not in szoveg:
        return out
    heber = szoveg.split('### Héber szavak', 1)[1]
    heber = re.split(r'^### (?!Héber)', heber, flags=re.M)[0]
    m = re.search(r'^#### 5\. .*?$(.*?)^#### 6\.', heber, re.S | re.M)
    if not m:
        return out
    token = None
    for sor in m.group(1).split('\n'):
        tm = re.match(r'^\*\*(H\d{4}[a-z]?)\*\* · UBS DBH', sor)
        if tm:
            token = tm.group(1)
            continue
        rm = re.match(r'^\| `(\d+)` \| (.*?) \| (.*?) \| \d+ \|$', sor)
        if rm and token:
            if LG.FORDITASRA_VAR in rm.group(2):
                out.add((token, rm.group(1), 'glosszak_hu'))
            if LG.FORDITASRA_VAR in rm.group(3):
                out.add((token, rm.group(1), 'definicio_hu'))
    return out


def main():
    if len(sys.argv) != 3 or sys.argv[1] != '--renderek':
        sys.exit(__doc__)
    renderek = sys.argv[2]
    _, elo = G.tsv_beolvas(G.ELOFORDULASOK_TSV)
    lapok = sorted(f[:-len('_TUDOMANYOS.md')] for f in os.listdir(os.path.join(GYOKER, 'lexikon'))
                   if f.endswith('_TUDOMANYOS.md'))
    _jel, hiv, _db = LG.ubs_dbh_adatok()
    fidx = LG.forditasok_index()

    def van_hu(strong, lexid, mezo):
        r = fidx.get(('UBS_DBH', strong, lexid, LG.EM_DASH, mezo))
        return bool(r and r.get('allapot') != 'elavult' and r.get('forditas_hu'))

    sorok = []
    osz_sorok = {}
    nincs = []
    for mid in lapok:
        for s in elo:
            if s['id'] != mid:
                continue
            tokenek = [t for t in (s.get('strong') or '').split('+') if t.startswith('H')]
            if not tokenek:
                continue
            for vers in LG.igehely_lista(s['igehely']):
                mt, ok = LG.karoli_mt_vers(vers)
                if mt is None and ok == 'a Károli-vers nincs a versmegfeleltető táblában':
                    continue
                osz_sorok[mid] = osz_sorok.get(mid, 0) + 1
                for t in tokenek:
                    lexidek = sorted(set(hiv.get((t, mt), []))) if mt else []
                    if not lexidek:
                        nincs.append('%s %s %s (%s)' % (mid, vers, t, ok or 'keresett MT-vers: %s' % mt))
                    for lx in lexidek:
                        sorok.append((mid, t, lx))
    egyedi_sor = sorted(set(sorok))
    tsv = []
    for mid, t, lx in egyedi_sor:
        for mezo in MEZOK:
            tsv.append([mid, t, lx, mezo, 'igen' if van_hu(t, lx, mezo) else 'nem'])
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    prov = ('# proveniencia: scope=%d lexikonoldal (%s), ÓSZ-sorok H-tokenjei | forras=naplok/F131_dbh_meres.py; '
            'adat/elofordulasok.tsv, konkordancia/Karoli_versmegfeleltetes.tsv, konkordancia/UBS_DBH_referenciak.tsv, '
            'adat/forditasok.tsv | ts=%s' % (len(lapok), ', '.join(lapok), ts))
    with open(KI, 'w', encoding='utf-8', newline='\n') as f:
        f.write(prov + '\n')
        f.write('# a definicio_hu az „UBS-jelentés” cella mezője (DT-F131j); a glosszak_hu a #121 egységszámításának párja\n')
        f.write('\t'.join(['lexikon', 'strong', 'lexid', 'mezo', 'van_hu']) + '\n')
        for r in tsv:
            f.write('\t'.join(r) + '\n')

    print(prov[2:])
    print('lexikonoldalak:', ', '.join(lapok))
    print('ÓSZ-versek (sor × vers) lapnként:', osz_sorok)
    print('sorok a TSV-ben (lexikon × strong × lexid × mezo): %d' % len(tsv))
    egyedi = sorted({(t, lx) for _m, t, lx in egyedi_sor})
    print('egyedi (strong, lexid) a 8 lapon együtt: %d' % len(egyedi))
    for mezo in MEZOK:
        n = sum(1 for t, lx in egyedi if van_hu(t, lx, mezo))
        print('  %s: lefordítva %d, hiányzik %d' % (mezo, n, len(egyedi) - n))
    print('lapnként egyedi lexid: %s' % {m: len({(t, lx) for mm, t, lx in egyedi_sor if mm == m}) for m in lapok})
    f121 = set()
    for mid in lapok:
        alap = GYOKER if mid in LG.SZOTARI_GERINC_MOTIVUMOK else renderek
        f121 |= f121_dbh_egysegek(os.path.join(alap, 'lexikon', '%s_TUDOMANYOS.md' % mid))
    uj = {(t, lx, mezo) for t, lx in egyedi for mezo in MEZOK}
    print('#121 DBH-egységei a 8 lapon (strong, lexid, mező; fordításra vár): %d (lexid: %d)'
          % (len(f121), len({(t, lx) for t, lx, _ in f121})))
    atf = uj & f121
    print('átfedés (a mostani #121-egységek közül a cellához is kell): %d egység; a cellához kell, de a #121-ben '
          'nincs: %d egység' % (len(atf), len(uj - f121)))
    print('  ebből definicio_hu: átfedés %d, új %d' % (
        sum(1 for x in atf if x[2] == 'definicio_hu'), sum(1 for x in uj - f121 if x[2] == 'definicio_hu')))
    for x in sorted(uj - f121):
        print('    új: %s %s %s' % x)
    print('hivatkozás nélküli ÓSZ-vers × token: %d' % len(nincs))
    for x in nincs:
        print('    %s' % x)
    print('kiírva: %s' % KI)


if __name__ == '__main__':
    main()
