#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lapnezet.py -- F165 (LAPJAVIT_ARTIFACT): a lexikonlap olvasható nézete (Artifact-oldal) bekezdésenkénti
„Kérdezz / javasolj” gombbal, a `lapnezet_sablon.html`-ből.

A nézet a generált `lexikon/<ID>_TUDOMANYOS.md`-t rendereli (a munkafán, vagy `--ref`-fel egy git-ág/commit
állapotából), és minden bekezdéshez, listaelemhez, idézethez gombot tesz. A gomb a néző saját Claude-fiókján
(`sample` capability) kérdez; a modell CSAK JAVASOL. A néző (a lap tulajdonosa) által jóváhagyott javaslat a
lap `db`-jének `javaslatok` gyűjteményébe kerül; onnan a session `ArtifactData`-val olvassa ki, és a `/lap-javit`
szabályai szerint írja be a forrásba (`.claude/commands/lap-javit.md`, „Artifact-mód”; segéd: `javaslatok.py`).

A kézi rések helyét a nézet az `adat/res_forras.tsv` `tanulmany` forrású soraiból ismeri (a `fejlec` mező a lapon
álló címsor): az alattuk álló bekezdés „kézi próza” jelölést és forrásfájl-tippet kap, a többi „generált rész”.
Ez tipp, nem osztályozás: az osztályt (próza / adat / forrás / generátor) a session mondja ki.

A kimenetet az Artifact-eszköz publikálja ezekkel a képességekkel (a `capabilities()` adja vissza, a teszt őrzi):
    {"sample": {}, "user": {}, "db": {"rules": [{"path": "javaslatok", "read": "view", "write": "owner"}]}}
A `write: owner` miatt javaslatot csak a lap tulajdonosa (a felhasználó) menthet: a `jovahagyta` mező így a
felhasználó (DT599: modell nem hagyhat jóvá). Az `artifact` (önpublikálás) képességet a nézet NEM kapja: a lap
önmagát nem írhatja át.

    python eszkozok/lektor_felulet/lapnezet.py <ID> <kimenet.html> [--ref <ág|commit>]
"""
import argparse
import json
import os
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HELY = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HELY))
SABLON = os.path.join(HELY, 'lapnezet_sablon.html')
HELYORZOK = ('__ADAT__', '__META__', '__CIM__', '__FORRAS_JEL__')


def capabilities():
    """Az Artifact-publikálás `capabilities` paramétere (F165). A `javaslatok` csak a tulajdonosé."""
    return {'sample': {}, 'user': {},
            'db': {'rules': [{'path': 'javaslatok', 'read': 'view', 'write': 'owner'}]}}


def _git(root, *args):
    return subprocess.run(['git', '-C', root] + list(args), check=True, capture_output=True).stdout.decode('utf-8')


def _fajl(root, ut, ref):
    """Repó-relatív fájl szövege a munkafáról vagy egy git-ref állapotából."""
    if ref:
        return _git(root, 'show', '%s:%s' % (ref, ut))
    with open(os.path.join(root, ut), encoding='utf-8') as f:
        return f.read()


def kezi_resek(res_szoveg, motivum):
    """A motívum kézi rései a `res_forras.tsv`-ből (`split('\\t')`): [{fejlec, res, forras}], csak `tanulmany` forrású sorok."""
    sorok = [x.rstrip('\r') for x in res_szoveg.split('\n') if x.strip() and not x.startswith('#')]
    fej = sorok[0].split('\t')
    if fej[:5] != ['id', 'res', 'fejlec', 'forras', 'tanulmany']:
        raise ValueError('res_forras.tsv: váratlan fejléc %r' % fej)
    ki = []
    for x in sorok[1:]:
        r = dict(zip(fej, x.split('\t')))
        if r['id'] == motivum and r['forras'] == 'tanulmany' and r.get('tanulmany', '').strip():
            ki.append({'fejlec': r['fejlec'].strip(), 'res': r['res'], 'forras': r['tanulmany'].strip()})
    return ki


def cim(md, motivum):
    for sor in md.split('\n'):
        if sor.startswith('# '):
            return sor[2:].replace('📖', '').strip()
    return motivum


def _js(ertek):
    return json.dumps(ertek, ensure_ascii=False).replace('</', '<\\/')


def epit(motivum, ref=None, root=ROOT):
    lap_ut = 'lexikon/%s_TUDOMANYOS.md' % motivum
    md = _fajl(root, lap_ut, ref)
    commit = _git(root, 'rev-parse', '--short=8', ref or 'HEAD').strip()
    meta = {'id': motivum, 'cim': cim(md, motivum), 'lap': lap_ut, 'commit': commit,
            'kezi': kezi_resek(_fajl(root, 'adat/res_forras.tsv', ref), motivum)}
    with open(SABLON, encoding='utf-8') as f:
        sablon = f.read()
    for h in HELYORZOK:
        if sablon.count(h) != 1:
            raise ValueError('a sablon %s helyőrzője hiányzik vagy ismétlődik' % h)
    forras_jel = '%s @ %s · %s' % (ref or 'munkafa', commit, lap_ut)
    # a szöveges helyőrzők HTML-szövegbe kerülnek: escape
    def esc(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    return (sablon.replace('__ADAT__', _js(md)).replace('__META__', _js(meta))
            .replace('__CIM__', esc('%s lapnézet' % motivum)).replace('__FORRAS_JEL__', esc(forras_jel))), meta


def main():
    ap = argparse.ArgumentParser(description='F165 -- lapnézet „Kérdezz / javasolj” gombbal')
    ap.add_argument('motivum')
    ap.add_argument('kimenet')
    ap.add_argument('--ref', default=None, help='git-ág vagy commit, amelynek állapotából a lap készül (alap: munkafa)')
    a = ap.parse_args()
    kimenet = os.path.abspath(a.kimenet)
    if kimenet.startswith(os.path.abspath(ROOT) + os.sep):
        raise ValueError('a kimenet a repón kívülre menjen (scratch), ne a repóba')
    html, meta = epit(a.motivum, a.ref)
    with open(kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('  %s: %s @ %s, %d kézi rés, %d bájt' % (kimenet, meta['id'], meta['commit'], len(meta['kezi']), len(html.encode('utf-8'))),
          file=sys.stderr)
    print('  capabilities: %s' % json.dumps(capabilities(), ensure_ascii=False), file=sys.stderr)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
