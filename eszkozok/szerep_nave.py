"""A szótári szerepmátrix 12. szerepe (Tematikus index, Nave) — általános, motívumfüggetlen szűrő és építő (ISTENTISZT-001
arany lap, 2026-10-29; a szűrés a felhasználó döntése: a (C) változat).

Bemenet: a motívum `elofordulasok.tsv`-sorai; a `konkordancia/Nave_basokant.tsv` (közkincs, F18; a Károli-kulcs az
`igehely_karoli`, ha ki van töltve, különben az `igehely`; az egy fejezeten belüli tartomány a benne álló verseket fedi); az
`adat/tematikus_tiltolista.tsv` (motívumonként a tiltott témák, a motívum `folerendelt_fogalom`-ja szerint — adat, nem kód);
az `adat/nave_tema_hu.tsv` (a téma- és altételnevek magyar fordítása).

Szűrés: egy téma akkor áll a blokkban, ha legalább `MIN_VERS` (2) motívumverset érint, a motívumverseinek aránya a téma
összes verséhez legalább `MIN_ARANY` (1%), és nincs a motívum tiltólistáján. A sorrend: a motívumversek száma (csökkenő),
az arány (csökkenő), a téma-azonosító. Témánként az érintett altételek (`cimke`) és a motívumversek látszanak. A blokk csak
megjelenítés (tematikus index): jelölt csak a `jeloltek.tsv`-n át lesz.

TSV: split('\\t'), a '\\r' levágva; csv modul nélkül.
"""
import collections
import hashlib
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import szerep_karoli as SZK  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAVE = os.path.join(GYOKER, 'konkordancia', 'Nave_basokant.tsv')
TILTOLISTA = os.path.join(GYOKER, 'adat', 'tematikus_tiltolista.tsv')
TEMA_HU = os.path.join(GYOKER, 'adat', 'nave_tema_hu.tsv')

MIN_VERS = 2
MIN_ARANY = 0.01
TART = re.compile(r'^(.+ \d+):(\d+)-(\d+)$')
FORDITASRA_VAR = '*(fordításra vár)*'

_CACHE = {}


def _sorok(ut):
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n')]
    s = [x for x in s if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def sha1(szoveg):
    return hashlib.sha1(szoveg.encode('utf-8')).hexdigest()


def versek(hely):
    """A Nave-igehely Károli-versei: a fejezeten belüli tartomány kibontva."""
    m = TART.match(hely)
    if not m:
        return [hely]
    return ['%s:%d' % (m.group(1), v) for v in range(int(m.group(2)), int(m.group(3)) + 1)]


def nave_sorai(ut=None):
    """[(tema_id, tema, cimke, [vers, …])] a Nave-tábla soraiból (a Károli-kulccsal)."""
    ut = ut or NAVE
    if ('nave', ut) not in _CACHE:
        ki = []
        for r in _sorok(ut):
            hely = r.get('igehely_karoli') or r.get('igehely') or ''
            if hely:
                ki.append((r['tema_id'], r['tema'], r.get('cimke', ''), versek(hely)))
        _CACHE[('nave', ut)] = ki
    return _CACHE[('nave', ut)]


def tiltolista(motivum_id, ut=None):
    """{tema_id: indok} a motívum tiltott témái (`adat/tematikus_tiltolista.tsv`, `forras=Nave`)."""
    return {r['tema_id']: r['indok'] for r in _sorok(ut or TILTOLISTA)
            if r['id'] == motivum_id and r.get('forras') == 'Nave'}


def nave_temak(sorai, min_vers=MIN_VERS, min_arany=MIN_ARANY, tiltott=None, nave=None):
    """[{tema_id, tema, motivumversek, temavers, arany, cimkek: {cimke: [vers, …]}}] — l. a modul docstringjét.
    A `tiltott` (tema_id-halmaz) alapértelmezése a motívum tiltólistája."""
    nave = nave_sorai() if nave is None else nave
    mid = sorai[0]['id'] if sorai else ''
    tiltott = set(tiltolista(mid)) if tiltott is None else set(tiltott)
    sorrend = {s['igehely'] for s in sorai}
    nev, tema_vers = {}, collections.defaultdict(set)
    talalat = collections.defaultdict(lambda: collections.defaultdict(list))
    for tid, tema, cimke, vs in nave:
        nev[tid] = tema
        for v in vs:
            tema_vers[tid].add(v)
            if v in sorrend and v not in talalat[tid][cimke]:
                talalat[tid][cimke].append(v)
    ki = []
    for tid, cs in talalat.items():
        mv = sorted({v for vs in cs.values() for v in vs}, key=SZK.vers_kulcs)
        arany = len(mv) / len(tema_vers[tid])
        if len(mv) < min_vers or arany < min_arany or tid in tiltott:
            continue
        ki.append({'tema_id': tid, 'tema': nev[tid], 'motivumversek': mv, 'temavers': len(tema_vers[tid]),
                   'arany': arany, 'cimkek': collections.OrderedDict(
                       (c, sorted(v, key=SZK.vers_kulcs)) for c, v in sorted(cs.items(), key=lambda x: x[0]))})
    return sorted(ki, key=lambda t: (-len(t['motivumversek']), -t['arany'], t['tema_id']))


def magyar_nevek(ut=None):
    """{(tema_id, cimke_en): (magyar, forras_hash)} az `adat/nave_tema_hu.tsv`-ből; a témanév sorában a `cimke_en` üres."""
    return {(r['tema_id'], r['cimke_en']): (r['magyar'], r['forras_hash']) for r in _sorok(ut or TEMA_HU)
            if r.get('allapot') != 'elavult'}


def _hu(nevek, tid, cimke, angol):
    m = nevek.get((tid, cimke))
    if m and m[1] == sha1(angol):
        return '%s (*%s*)' % (m[0], angol)
    return '%s %s' % (angol, FORDITASRA_VAR)


def blokk_12(sorai, ts):
    """A 12. szerep bekezdései (lista); üres, ha nincs a szűrésen átmenő téma."""
    mid = sorai[0]['id'] if sorai else ''
    temak = nave_temak(sorai)
    if not temak:
        return []
    tiltott = tiltolista(mid)
    nevek = magyar_nevek()
    out = ['*Nave tematikus indexe (Nave\'s Topical Bible, 1897, közkincs): azok a témák, amelyek legalább %d motívumverset '
           'érintenek, a motívumversek aránya a téma összes verséhez legalább %d%%, és nincsenek a motívum tiltólistáján '
           '(`adat/tematikus_tiltolista.tsv`: %d téma, a fölérendelt fogalom felé). Csak megjelenítés: jelölt ezekből csak az '
           '`adat/jeloltek.tsv`-n át lesz.*' % (MIN_VERS, round(MIN_ARANY * 100), len(tiltott))]
    sorok = []
    for t in temak:
        sorok.append('- **%s** — %d motívumvers / %d témavers (%.1f%%): %s' % (
            _hu(nevek, t['tema_id'], '', t['tema']), len(t['motivumversek']), t['temavers'], 100 * t['arany'],
            ', '.join(t['motivumversek'])))
        for c, vs in t['cimkek'].items():
            if c:
                sorok.append('  - %s: %s' % (_hu(nevek, t['tema_id'], c, c), ', '.join(vs)))
    out.append('\n'.join(sorok))
    out.append('*(proveniencia: scope=adat/elofordulasok.tsv (id=%s) | forras=Nave_basokant.tsv+adat/tematikus_tiltolista.tsv'
               '+adat/nave_tema_hu.tsv (eszkozok/szerep_nave.py) | n=%d | ts=%s)*' % (mid, len(temak), ts))
    return out
