#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lapnezet.py -- F165 (LAPJAVIT_ARTIFACT): a lexikonlap olvasható nézete (Artifact-oldal) látható blokkjelekkel, a
`lapnezet_sablon.html`-ből.

A nézet CSAK a generált `lexikon/<ID>_TUDOMANYOS.md`-t mutatja (a munkafáról, vagy `--ref`-fel egy git-ág/commit
állapotából): gomb, panel, Claude-hívás és javaslat-tár nincs benne (a felhasználó 2026-11-08-i kérése, DT-F165a).
Minden blokk (bekezdés, lista, táblázat, idézet, kódblokk) mellett rövid, látható jel áll (pl. `1/a·12`): a
felhasználó a chatben erre (vagy idézetre) mutat rá, a javítás kontextusa és menete a sessionben van
(`/lap-javit`), a jóváhagyás után a session vezeti át a javítást, és újra kiteszi a nézetet.

A blokkokra bontás itt, Pythonban történik, és a nézet ezt a listát rendereli: a lapon látható jel és a
`--jel` által kiírt szöveg így ugyanabból a bontásból jön.

Blokk: üres sorral határolt szakasz (a kódkerítésen belül az üres sor nem határ); a címsor önálló blokk, jel nélkül.
Jel: `<szakasz>·<n>`, ahol a szakasz a legutóbbi `## ` címsor sorszáma (`1`, `1/b`, `6/b`), vagy számozatlan
címsornál maga a cím (`Kivonat`, `Kolofon`); az `n` a szakaszon belüli blokk-sorszám 1-től.

    python eszkozok/lektor_felulet/lapnezet.py <ID> <kimenet.html> [--ref <ág|commit>]
    python eszkozok/lektor_felulet/lapnezet.py <ID> --jel "1/a·12" [--ref <ág|commit>]

A kimenet a repón kívülre megy; a publikálás `capabilities` nélkül (vagy `{}`-vel, ha a tárolt képességeket
törölni kell).
"""
import argparse
import json
import os
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

HELY = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HELY))
SABLON = os.path.join(HELY, 'lapnezet_sablon.html')
HELYORZOK = ('__BLOKKOK__', '__META__', '__CIM__', '__FORRAS_JEL__')
SZAKASZ_SZAM = re.compile(r'^(\d+(?:/[a-z])?)\.\s')
CIMSOR = re.compile(r'^(#{1,6})\s+(.*)$')


def _git(root, *args):
    return subprocess.run(['git', '-C', root] + list(args), check=True, capture_output=True).stdout.decode('utf-8')


def _fajl(root, ut, ref):
    """Repó-relatív fájl szövege a munkafáról vagy egy git-ref állapotából."""
    if ref:
        return _git(root, 'show', '%s:%s' % (ref, ut))
    with open(os.path.join(root, ut), encoding='utf-8') as f:
        return f.read()


def _darabol(md):
    """Üres sorral határolt szakaszok; kódkerítésen belül az üres sor nem határ. A címsor önálló darab."""
    darabok, akt, kerites = [], [], False
    for sor in md.replace('\r\n', '\n').split('\n'):
        if sor.lstrip().startswith('```'):
            kerites = not kerites
        if not kerites and CIMSOR.match(sor) and not akt:
            darabok.append(sor)
            continue
        if not kerites and CIMSOR.match(sor) and akt:
            darabok.append('\n'.join(akt))
            akt = []
            darabok.append(sor)
            continue
        if not kerites and not sor.strip():
            if akt:
                darabok.append('\n'.join(akt))
                akt = []
            continue
        akt.append(sor)
    if akt:
        darabok.append('\n'.join(akt))
    return darabok


def szakasz_kulcs(cim):
    cim = cim.replace('*(kézi)*', '').replace('(kézi)', '').strip()
    m = SZAKASZ_SZAM.match(cim)
    return m.group(1) if m else cim.strip('*_ ')


def blokkok(md):
    """[{jel, md, hely, cimsor}] a lap sorrendjében. A címsor-blokk `jel` mezője üres; a `hely` a címsor-útvonal
    (a `# ` cím nélkül)."""
    ki, utvonal, szakasz, szamlalo = [], [], '', 0
    for d in _darabol(md):
        m = CIMSOR.match(d) if '\n' not in d else None
        if m:
            szint, cim = len(m.group(1)), m.group(2).strip()
            if szint > 1:
                utvonal = [u for u in utvonal if u[0] < szint] + [(szint, cim.replace('*(kézi)*', '').strip())]
            if szint == 2:
                szakasz, szamlalo = szakasz_kulcs(cim), 0
            ki.append({'jel': '', 'md': d, 'hely': ' › '.join(u[1] for u in utvonal), 'cimsor': szint})
            continue
        szamlalo += 1
        ki.append({'jel': '%s·%d' % (szakasz or 'fej', szamlalo), 'md': d,
                   'hely': ' › '.join(u[1] for u in utvonal), 'cimsor': 0})
    return ki


def keres(bl, jel):
    jel = jel.strip().replace('.', '·') if '·' not in jel else jel.strip()
    talalt = [b for b in bl if b['jel'] == jel]
    if len(talalt) != 1:
        raise ValueError('a(z) %r jel %d blokkot jelöl (1 kell)' % (jel, len(talalt)))
    return talalt[0]


def cim(md, motivum):
    for sor in md.split('\n'):
        if sor.startswith('# '):
            return sor[2:].replace('📖', '').strip()
    return motivum


def _js(ertek):
    return json.dumps(ertek, ensure_ascii=False).replace('</', '<\\/')


def _esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def betolt(motivum, ref=None, root=ROOT):
    lap_ut = 'lexikon/%s_TUDOMANYOS.md' % motivum
    md = _fajl(root, lap_ut, ref)
    commit = _git(root, 'rev-parse', '--short=8', ref or 'HEAD').strip()
    return md, {'id': motivum, 'cim': cim(md, motivum), 'lap': lap_ut, 'commit': commit, 'ref': ref or 'munkafa'}


def epit(motivum, ref=None, root=ROOT):
    md, meta = betolt(motivum, ref, root)
    bl = blokkok(md)
    jelek = [b['jel'] for b in bl if b['jel']]
    if len(jelek) != len(set(jelek)):
        raise ValueError('ismétlődő blokkjel a lapon (két azonos nevű számozatlan szakasz?)')
    with open(SABLON, encoding='utf-8') as f:
        sablon = f.read()
    for h in HELYORZOK:
        if sablon.count(h) != 1:
            raise ValueError('a sablon %s helyőrzője hiányzik vagy ismétlődik' % h)
    html = (sablon.replace('__BLOKKOK__', _js([{'jel': b['jel'], 'md': b['md'], 'cimsor': b['cimsor']} for b in bl]))
            .replace('__META__', _js(meta))
            .replace('__CIM__', _esc('%s lapnézet' % motivum))
            .replace('__FORRAS_JEL__', _esc('%s @ %s · %s' % (meta['ref'], meta['commit'], meta['lap']))))
    return html, meta, bl


def main():
    ap = argparse.ArgumentParser(description='F165 -- lexikonlap-nézet blokkjelekkel')
    ap.add_argument('motivum')
    ap.add_argument('kimenet', nargs='?')
    ap.add_argument('--ref', default=None, help='git-ág vagy commit, amelynek állapotából a lap készül (alap: munkafa)')
    ap.add_argument('--jel', default=None, help='egy blokk szövegének kiírása a jele alapján (pl. "1/a·12")')
    a = ap.parse_args()
    if a.jel:
        md, meta = betolt(a.motivum, a.ref)
        b = keres(blokkok(md), a.jel)
        print('%s %s @ %s · %s\n\n%s' % (a.motivum, b['jel'], meta['commit'], b['hely'], b['md']))
        return 0
    if not a.kimenet:
        raise ValueError('kimeneti fájl vagy --jel kell')
    kimenet = os.path.abspath(a.kimenet)
    if kimenet.startswith(os.path.abspath(ROOT) + os.sep):
        raise ValueError('a kimenet a repón kívülre menjen (scratch), ne a repóba')
    html, meta, bl = epit(a.motivum, a.ref)
    with open(kimenet, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print('  %s: %s @ %s, %d blokkjel, %d bájt' % (kimenet, meta['id'], meta['commit'], sum(1 for b in bl if b['jel']),
                                                  len(html.encode('utf-8'))), file=sys.stderr)
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except Exception as exc:  # noqa: BLE001
        print('HIBA: %s' % exc, file=sys.stderr)
        sys.exit(2)
