"""F91 E1 (CSAK MÉRÉS): az lxx_os_import.py gap-fill lépésének offline újrafuttatása a commitolt LXX_OS-en.

Nem ír a repóba. A commitolt LXX_OS gap-fill-eredetű sorait (karoli_ok: zsolt_felirat_eltolas, versmegfeleltetes_tabla,
sorrend_beagyazas) kulcs nélkülire állítja, majd lefuttatja a lefedettseg_javit_konyv()-et a REGI (a megadott git-revízió)
és az UJ (munkafa) Karoli_versmegfeleltetes.tsv-vel;
a felirat-versek KJV-kulcsát az importer maga képzi a közös felirat-halmazból (DT-F91d (a)): a replay a módosított
importer-függvényt hívja, nem másolt logikát. Kimenet: könyvenként az eltérő vers/token. A teljes újragenerálás (--letolt) nem része.

Regressziós ellenőrzés (DT-F91d (iii)): elvárt kimenet minden könyvre 0/0 mindkét A-táblával, kilépési kód 0;
bármely eltérésnél 1. Futtatás: python eszkozok/f91_lxx_os_replay.py [regi_revizio, alapertelmezes 25e39a1a]
Proveniencia: scope=LEFEDETTSEG_KONYVEK | forras=konkordancia/LXX_OS/*.tsv + eszkozok/lxx_os_import.py | ts=2026-10-14
"""
import os
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'eszkozok'))
import lxx_os_import as L  # noqa: E402

GAP_OK = {'zsolt_felirat_eltolas', 'versmegfeleltetes_tabla', 'sorrend_beagyazas'}
UJ = os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')


def beolvas(slug):
    sorok, hdr = [], None
    with open(os.path.join(L.LXX_OS_DIR, slug + '.tsv'), encoding='utf-8', newline='') as f:
        for ln in f.read().split('\n'):
            ln = ln.rstrip('\r')
            if not ln or ln.startswith('#'):
                continue
            if hdr is None:
                hdr = ln
                continue
            sorok.append(ln.split('\t'))
    assert hdr.split('\t') == L.LXX_OS_HEADER
    return sorok


def replay(slug, tabla_path):
    L.VERSMEGFELELTETES_TSV = tabla_path
    L._TABLA_CACHE = None
    comm = beolvas(slug)
    run = [list(p) for p in comm]
    for p in run:
        if p[3] in GAP_OK:
            p[2], p[3] = '', ''
    L.lefedettseg_javit_konyv(slug, run)
    elt_vers = {p[0] for p, q in zip(comm, run) if p[2:4] != q[2:4]}
    elt_tok = sum(1 for p, q in zip(comm, run) if p[2:4] != q[2:4])
    kulcs_veszt = {p[0] for p, q in zip(comm, run) if p[2] and not q[2]}
    return len(comm), len(elt_vers), elt_tok, len(kulcs_veszt)


if __name__ == '__main__':
    rev = sys.argv[1] if len(sys.argv) > 1 else '25e39a1a'
    tmp = tempfile.mkdtemp()
    regi = os.path.join(tmp, 'regi.tsv')
    with open(regi, 'wb') as f:
        f.write(subprocess.check_output(['git', '-C', ROOT, 'show', '%s:konkordancia/Karoli_versmegfeleltetes.tsv' % rev]))
    print('könyv | token-sor | régi A-tábla: eltérő vers/token | új A-tábla: eltérő vers/token (kulcsot vesztett vers)')
    ossz = 0
    for konyv in L.LEFEDETTSEG_KONYVEK:
        slug = L.elsodleges_slug(konyv)
        n, rv, rt, _ = replay(slug, regi)
        _, uv, ut, uk = replay(slug, UJ)
        print('%s | %d | %d/%d | %d/%d (%d)' % (konyv, n, rv, rt, uv, ut, uk))
        ossz += rv + rt + uv + ut + uk
    print('ELTERES-OSSZEG: %d (elvart: 0)' % ossz)
    sys.exit(1 if ossz else 0)
