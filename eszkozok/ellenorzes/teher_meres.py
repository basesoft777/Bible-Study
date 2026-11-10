#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
teher_meres.py -- F188 T0/T7: a menetek konyvelesi es ellenorzesi terhe PR-onkent
(F188_TEHER_CSOKKENTES_BRIEF.md, „T0 — mérés-alap”).

Mit mer PR-onkent (a `gh` es a helyi `git` adataibol, hálózati hibánál a mező
„nem mért”, soha nem üres):

- `admin` / `tartalmi`: a PR fájljainak száma. Admin: `naplok/`, `dontesek/uj/`,
  `nyitott/uj/`, `*_BRIEF.md`, `NYITOTT_FELADATOK.md`, `FELADATOK.md`,
  `DONTESEK.md`; minden más tartalmi.
- `commit`: a PR commitjai (a `gh pr view` listája); `merge_commit`: ebből a
  „Merge ” kezdetűek (a main beolvasztása, nem a menet munkája).
- `javitokor`: a lezajlott javítókörök száma, három jelből a legnagyobb:
  (a) a PR-ban álló `naplok/ELLENOR_F<nn>[_<n>].md` legnagyobb sorszáma − 1
      (az első ellenőrzés nem javítókör; `_ujra`/`_valasz` nem számít);
  (b) a commit-címekben álló `[elteres_kor k/2]` és „javítókör k/2” jelölő k-ja;
  (c) az ellenőri jelentést rögzítő commitok száma − 1 (az F188 T1 óta a
      jelentés a `naplok/F<nn>_jelentes.md` „Független ellenőrzés” szakaszába
      kerül; a commit címe `<tétel>: ellenőri jelentés (…)` alakú, l. BRIEF_SABLON
      „Jelentés”; a cím közepén álló „ellenőri jelentés” szó nem számít).
  Az összesítés az átlagot kétféle alapon adja: minden mért PR-on, és csak az
  ellenőrzött PR-okon (ahol volt ellenőr-commit).
  `ci_javitas`: a „CI-javítás” című commitok száma (a /kovetkezo 10. lépése).
- `ellenor_perc`: ellenőri futásonként a jelentést rögzítő commit és az azt
  megelőző PR-commit szerzői időbélyegének (`authoredDate`; a rebase ezt nem írja
  át, a committer-dátumot igen) különbsége (perc). **Korlát:** becslés, két irányban
  is torzíthat: benne van a session mentése és a menet esetleges állása (túlbecslés),
  és ha a session az ellenőr futása közben commitolt (pl. fejléc), a rés rövidebb
  (alulbecslés). Ha a PR-ban nincs ellenőr-commit, „nem mérhető”. Az összesítés a
  legnagyobbat adja.
- `ci_futas`, `ci_bukott`, `ci_perc_atlag`, `ci_perc_osszes`: az `ellenorzes`
  workflow futásai a PR ágán (`gh run list --branch`); a futás ideje az
  `updatedAt − createdAt` (a sorban állással együtt).

CLI:
    python eszkozok/ellenorzes/teher_meres.py --pr 664 665 666 668
    python eszkozok/ellenorzes/teher_meres.py --utolso 8 [--kimenet ki.tsv]

Kimenet: TSV a stdout-ra (vagy a `--kimenet` fájlba), utána az összesítés a
célokkal (admin ≤ tartalmi; átlagos javítókör ≤ 1; ellenőri futás ≤ 15 perc), és
a proveniencia-sor (`scope=… | forras=gh+git | ts=…`). A TSV `split('\\t')`-tel
olvasható; a `#` kezdetű sorok megjegyzések.
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

NEM_MERT = 'nem mért'
NEM_MERHETO = 'nem mérhető'
IDOKORLAT = 90  # mp, egy gh/git hívásra

ADMIN_KONYVTARAK = ('naplok/', 'dontesek/uj/', 'nyitott/uj/')
ADMIN_FAJLOK = ('NYITOTT_FELADATOK.md', 'FELADATOK.md', 'DONTESEK.md')
ADMIN_UTOTAG = '_BRIEF.md'

CEL_JAVITOKOR = 1.0
CEL_ELLENOR_PERC = 15.0

_ELLENOR_FAJL = re.compile(r'^naplok/ELLENOR_(F[0-9A-Za-z]+?)(?:_(\d+))?\.md$')
_KOR_JELOLO = re.compile(r'(?:\[elteres_kor\s+(\d)/2\]|[Jj]avítókör\s+(\d)/2)')
_ELLENORI_JELENTES_CIM = re.compile(r'^[^\s:]+:\s+ellenőri jelentés\b', re.IGNORECASE)
_CI_JAVITAS = re.compile(r'CI-javítás')
_TETEL_ELOTAG = re.compile(r'^([A-Z][A-Z0-9_-]*?)[.:]')

OSZLOPOK = ('pr', 'feladat', 'ag', 'commit', 'merge_commit', 'admin', 'tartalmi', 'javitokor',
            'javitokor_forras', 'ci_javitas', 'ellenor_futas', 'ellenor_perc', 'ci_futas', 'ci_bukott',
            'ci_perc_atlag', 'ci_perc_osszes', 'megjegyzes')


def admin_e(ut):
    """Az F188 T0 admin-fájl meghatározása (a brief „Kiindulás” szakasza szerint)."""
    ut = ut.replace('\\', '/')
    if ut.startswith(ADMIN_KONYVTARAK):
        return True
    if ut in ADMIN_FAJLOK:
        return True
    return os.path.basename(ut).endswith(ADMIN_UTOTAG)


def fajlok_szama(utak):
    """(admin, tartalmi)."""
    admin = sum(1 for u in utak if admin_e(u))
    return admin, len(utak) - admin


def tetel_elotagok(cimek):
    """A commit-címek tétel-előtagjai (`F185.0.1: …` -> `F185`, `HATAR.GEPI: …` -> `HATAR`), vesszővel; a
    merge-commit és a gépi `szamkiosztas:` nem számít. Ha nincs, `-`."""
    ki = set()
    for cim in cimek:
        m = _TETEL_ELOTAG.match(cim)
        if m:
            ki.add(m.group(1))
    return ','.join(sorted(ki)) or '-'


def _ido(s):
    """ISO-8601 (`Z` vagy eltolás) -> aware datetime."""
    s = s.strip()
    if s.endswith('Z'):
        s = s[:-1] + '+00:00'
    return datetime.datetime.fromisoformat(s)


def _perc(a, b):
    return (_ido(b) - _ido(a)).total_seconds() / 60.0


def ellenor_commit_e(cim, fajlok):
    """Az ellenőri jelentést rögzítő commit: `naplok/ELLENOR_*.md`-t hoz létre (`fajlok`: a commit által
    HOZZÁADOTT fájlok; a meglévő jelentés kiegészítése nem új futás), vagy a címe `<tétel>: ellenőri jelentés`
    kezdetű (F188 T1 egy-fájlos jelentés)."""
    if fajlok and any(_ELLENOR_FAJL.match(f.replace('\\', '/')) for f in fajlok):
        return True
    return bool(_ELLENORI_JELENTES_CIM.search(cim or ''))


def javitokor(pr_fajlok, commitok):
    """(körök száma, forrás-leírás). `commitok`: [{'cim', 'fajlok' (a hozzáadott fájlok listája, vagy None)}]."""
    jelek = []
    legnagyobb = {}
    for f in pr_fajlok:
        m = _ELLENOR_FAJL.match(f.replace('\\', '/'))
        if m:
            n = int(m.group(2)) if m.group(2) else 1
            legnagyobb[m.group(1)] = max(legnagyobb.get(m.group(1), 0), n)
    if legnagyobb:
        jelek.append((max(legnagyobb.values()) - 1, 'ELLENOR-fájl'))
    kor = [int(a or b) for c in commitok for a, b in _KOR_JELOLO.findall(c.get('cim', ''))]
    if kor:
        jelek.append((max(kor), 'kör-jelölő'))
    ell = sum(1 for c in commitok if ellenor_commit_e(c.get('cim', ''), c.get('fajlok')))
    if ell:
        jelek.append((ell - 1, 'ellenőr-commit'))
    if not jelek:
        return 0, 'nincs jel'
    k = max(j[0] for j in jelek)
    return k, '+'.join(sorted({j[1] for j in jelek if j[0] == k}))


def ellenor_idok(commitok):
    """Perc-lista: minden ellenőr-commitra a megelőző commit óta eltelt idő (felső becslés). `commitok`
    időrendben: [{'cim', 'ido', 'fajlok'}]."""
    idok = []
    for i, c in enumerate(commitok):
        if i == 0 or not ellenor_commit_e(c.get('cim', ''), c.get('fajlok')):
            continue
        elozo = commitok[i - 1]
        if not c.get('ido') or not elozo.get('ido'):
            continue
        idok.append(max(0.0, _perc(elozo['ido'], c['ido'])))
    return idok


def ci_osszegzes(futasok):
    """(futások, bukott, átlag perc, összes perc) a `gh run list` JSON-jából; csak a befejezett futás számít
    az időbe."""
    kesz = [f for f in futasok if f.get('status') == 'completed' and f.get('createdAt') and f.get('updatedAt')]
    percek = [max(0.0, _perc(f['createdAt'], f['updatedAt'])) for f in kesz]
    bukott = sum(1 for f in kesz if f.get('conclusion') not in ('success', 'skipped', 'neutral'))
    osszes = sum(percek)
    atlag = osszes / len(percek) if percek else None
    return len(futasok), bukott, atlag, osszes


def _futtat(parancs):
    """A parancs stdout-ja, vagy None (hiba, időtúllépés, hiányzó program)."""
    try:
        kimenet = subprocess.run(parancs, cwd=ROOT, capture_output=True, timeout=IDOKORLAT, check=True)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired, OSError):
        return None
    return kimenet.stdout.decode('utf-8', errors='replace')


def _gh_json(parancs):
    ki = _futtat(['gh'] + parancs)
    if ki is None:
        return None
    try:
        return json.loads(ki)
    except ValueError:
        return None


def _commit_fajlok(oid):
    """A commit által hozzáadott fájlok (`git show --name-status`, `A` sorok), vagy None."""
    ki = _futtat(['git', 'show', '--name-status', '--format=', oid])
    if ki is None:
        return None
    uj = []
    for sor in ki.splitlines():
        mezok = sor.split('	')
        if len(mezok) >= 2 and mezok[0].startswith('A'):
            uj.append(mezok[-1].strip())
    return uj


def _fmt(x, tizedes=1):
    if x is None:
        return NEM_MERHETO
    if isinstance(x, float):
        return ('%.' + str(tizedes) + 'f') % x
    return str(x)


def pr_meres(szam):
    """Egy PR sora (dict, OSZLOPOK kulcsokkal). Hálózati vagy git-hibánál az érintett mező „nem mért”."""
    sor = {k: NEM_MERT for k in OSZLOPOK}
    sor['pr'] = '#%d' % szam
    sor['megjegyzes'] = ''
    adat = _gh_json(['pr', 'view', str(szam), '--json', 'number,headRefName,commits,files'])
    if adat is None:
        sor['megjegyzes'] = 'gh pr view sikertelen'
        return sor
    sor['ag'] = adat.get('headRefName', '') or NEM_MERT
    utak = [f.get('path', '') for f in adat.get('files') or []]
    sor['admin'], sor['tartalmi'] = (str(x) for x in fajlok_szama(utak))
    nyers = adat.get('commits') or []
    sor['commit'] = str(len(nyers))
    sor['merge_commit'] = str(sum(1 for c in nyers if (c.get('messageHeadline') or '').startswith('Merge ')))
    sor['feladat'] = tetel_elotagok(c.get('messageHeadline') or '' for c in nyers)
    commitok = []
    git_hiany = 0
    for c in nyers:
        fajlok = _commit_fajlok(c.get('oid', ''))
        if fajlok is None:
            git_hiany += 1
        commitok.append({'cim': c.get('messageHeadline') or '',
                         'ido': c.get('authoredDate') or c.get('committedDate') or '',
                         'fajlok': fajlok})
    if all(c['ido'] for c in commitok):
        commitok.sort(key=lambda c: _ido(c['ido']))
    k, forras = javitokor(utak, commitok)
    sor['javitokor'], sor['javitokor_forras'] = str(k), forras
    sor['ci_javitas'] = str(sum(1 for c in commitok if _CI_JAVITAS.search(c['cim'])))
    idok = ellenor_idok(commitok)
    sor['ellenor_futas'] = str(sum(1 for c in commitok if ellenor_commit_e(c['cim'], c['fajlok'])))
    sor['ellenor_perc'] = ';'.join(_fmt(p, 0) for p in idok) if idok else NEM_MERHETO
    if git_hiany:
        sor['megjegyzes'] = '%d commit fájllistája nem elérhető helyben (git fetch?)' % git_hiany
    futasok = _gh_json(['run', 'list', '--branch', sor['ag'], '--workflow', 'ellenorzes', '--limit', '100',
                        '--json', 'status,conclusion,createdAt,updatedAt'])
    if futasok is None:
        for k2 in ('ci_futas', 'ci_bukott', 'ci_perc_atlag', 'ci_perc_osszes'):
            sor[k2] = NEM_MERT
    else:
        n, b, atlag, osszes = ci_osszegzes(futasok)
        sor['ci_futas'], sor['ci_bukott'] = str(n), str(b)
        sor['ci_perc_atlag'] = _fmt(atlag)
        sor['ci_perc_osszes'] = _fmt(osszes) if n else NEM_MERHETO
    return sor


def _szam(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def osszesites(sorok):
    """Az összesítés sorai a célokkal (szöveg-lista)."""
    ki = []
    mert = [s for s in sorok if _szam(s['admin']) is not None]
    jo = [s for s in mert if _szam(s['admin']) <= _szam(s['tartalmi'])]
    ki.append('admin ≤ tartalmi: %d / %d PR teljesíti (cél: mind)' % (len(jo), len(mert)))
    korok = [_szam(s['javitokor']) for s in sorok if _szam(s['javitokor']) is not None]
    if korok:
        atlag = sum(korok) / len(korok)
        ki.append('átlagos javítókör: %.2f (cél: ≤ %.0f) — %s' % (
            atlag, CEL_JAVITOKOR, 'teljesül' if atlag <= CEL_JAVITOKOR else 'nem teljesül'))
        ell = [_szam(s['javitokor']) for s in sorok
               if _szam(s['javitokor']) is not None and (_szam(s.get('ellenor_futas')) or 0) > 0]
        if ell:
            a2 = sum(ell) / len(ell)
            ki.append('átlagos javítókör az ellenőrzött PR-okon: %.2f (%d PR) — %s' % (
                a2, len(ell), 'teljesül' if a2 <= CEL_JAVITOKOR else 'nem teljesül'))
    else:
        ki.append('átlagos javítókör: %s' % NEM_MERT)
    percek = []
    for s in sorok:
        for p in (s['ellenor_perc'] or '').split(';'):
            if _szam(p) is not None:
                percek.append(_szam(p))
    if percek:
        tul = sum(1 for p in percek if p > CEL_ELLENOR_PERC)
        ki.append('ellenőri futás: %d mért, legnagyobb %.0f perc, %d a %.0f perces cél fölött (becslés)'
                  % (len(percek), max(percek), tul, CEL_ELLENOR_PERC))
    else:
        ki.append('ellenőri futás: %s (nincs ellenőr-commit a mért PR-okban)' % NEM_MERHETO)
    ci = [_szam(s['ci_perc_atlag']) for s in sorok if _szam(s['ci_perc_atlag']) is not None]
    futas = [_szam(s['ci_futas']) for s in sorok if _szam(s['ci_futas']) is not None]
    if ci:
        ki.append('CI: %d futás, átlagosan %.1f perc futásonként' % (sum(futas), sum(ci) / len(ci)))
    return ki


def tsv(sorok):
    ki = ['\t'.join(OSZLOPOK)]
    for s in sorok:
        mezok = []
        for k in OSZLOPOK:
            ertek = str(s.get(k, '')).replace('\t', ' ')
            if not ertek and k != 'megjegyzes':
                ertek = NEM_MERT  # üres mező nem lehet (CLAUDE.md 1. szabály)
            mezok.append(ertek)
        ki.append('\t'.join(mezok))
    return ki


def utolso_mergelt(n):
    adat = _gh_json(['pr', 'list', '--state', 'merged', '--limit', str(n), '--json', 'number'])
    if adat is None:
        return None
    return sorted(int(p['number']) for p in adat)


def main(argv=None):
    ap = argparse.ArgumentParser(description='F188 T0: admin/tartalmi fájlok, javítókörök, ellenőri és CI-idő '
                                             'PR-onként.')
    ap.add_argument('--pr', nargs='*', type=int, default=[], help='PR-számok')
    ap.add_argument('--utolso', type=int, default=0, help='a legutóbbi N mergelt PR is')
    ap.add_argument('--kimenet', default=None, help='a TSV ide (az összesítés a stdout-ra megy)')
    args = ap.parse_args(argv)
    szamok = list(args.pr)
    if args.utolso:
        u = utolso_mergelt(args.utolso)
        if u is None:
            print('# a legutóbbi mergelt PR-ok listája: %s (gh pr list)' % NEM_MERT, file=sys.stderr)
        else:
            szamok += u
    szamok = sorted(set(szamok))
    if not szamok:
        ap.error('--pr vagy --utolso kell')
    sorok = [pr_meres(n) for n in szamok]
    ts = datetime.datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M%z')
    head = (_futtat(['git', 'rev-parse', '--short', 'HEAD']) or NEM_MERT).strip()
    prov = '# scope=PR %s | forras=gh+git (teher_meres.py @ %s) | ts=%s' % (
        ', '.join('#%d' % n for n in szamok), head, ts)
    tabla = tsv(sorok) + [prov]
    if args.kimenet:
        with open(args.kimenet, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(tabla) + '\n')
    else:
        print('\n'.join(tabla))
    print()
    print('## Összesítés')
    for s in osszesites(sorok):
        print('- ' + s)
    print(prov.lstrip('# '))
    return 0


if __name__ == '__main__':
    sys.exit(main())
