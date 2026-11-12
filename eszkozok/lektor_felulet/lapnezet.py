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

    python eszkozok/lektor_felulet/lapnezet.py <ID> <kimenet.html> --valtozas <alap-commit> [--ref <ág|commit>]
    python eszkozok/lektor_felulet/lapnezet.py <ID> --valtozas <alap-commit> [--ref <ág|commit>]   (szöveges kiírás)

`--valtozas` (F209, gyors út, `/lap-javit` 7. pont): csak a változott blokkokat mutatja, előtte–utána párban,
kiemelve (a törölt szó áthúzva, az új szó kiemelve). Az alap a lap fájlja az `<alap-commit>`-ban, az „utána” a
munkafa vagy a `--ref`. Önálló, rövid HTML (a `lapnezet_sablon.html`-t nem használja); `--jel`-lel nem együtt.

A kimenet a repón kívülre megy; a publikálás `capabilities` nélkül (vagy `{}`-vel, ha a tárolt képességeket
törölni kell).
"""
import argparse
import difflib
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


def valtozasok(regi_md, uj_md):
    """[{tipus, jel, hely, regi, uj}] a megváltozott blokkokról: `csere` (módosult), `uj` (beszúrt), `torolt`.
    Az illesztés a blokkok szövege szerint megy (difflib); a jel a mai (utána) lap jele, törölt blokknál a régié."""
    r, u = blokkok(regi_md), blokkok(uj_md)
    op = difflib.SequenceMatcher(None, [b['md'] for b in r], [b['md'] for b in u], autojunk=False).get_opcodes()
    ki = []
    for tag, i1, i2, j1, j2 in op:
        if tag == 'equal':
            continue
        regi, uj = r[i1:i2], u[j1:j2]
        for k in range(max(len(regi), len(uj))):
            a = regi[k] if k < len(regi) else None
            b = uj[k] if k < len(uj) else None
            x = b or a
            ki.append({'tipus': 'csere' if a and b else ('torolt' if a else 'uj'),
                       'jel': x['jel'] or x['md'][:40], 'hely': x['hely'],
                       'regi': a['md'] if a else '', 'uj': b['md'] if b else ''})
    return ki


def _szoveg_diff(regi, uj):
    """(regi_html, uj_html): szószintű kiemelés (del / ins)."""
    ra, ub = re.findall(r'\s+|\S+', regi), re.findall(r'\s+|\S+', uj)
    ho, hu = [], []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ra, ub, autojunk=False).get_opcodes():
        x, y = _esc(''.join(ra[i1:i2])), _esc(''.join(ub[j1:j2]))
        if tag == 'equal':
            ho.append(x)
            hu.append(y)
            continue
        if x:
            ho.append('<del>%s</del>' % x)
        if y:
            hu.append('<ins>%s</ins>' % y)
    return ''.join(ho), ''.join(hu)


CSS = ('body{font:15px/1.5 system-ui,sans-serif;margin:16px;max-width:1100px;background:#fff;color:#111}'
       '.par{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:0 0 20px;border-top:2px solid #888;padding-top:6px}'
       '.jel{grid-column:1/3;font:12px monospace;color:#555}.c{white-space:pre-wrap;border:1px solid #ccc;padding:8px}'
       'del{background:#fbb;text-decoration:line-through}ins{background:#bfb;text-decoration:none}'
       '@media(max-width:700px){.par{grid-template-columns:1fr}.jel{grid-column:1}}'
       '@media(prefers-color-scheme:dark){body{background:#111;color:#eee}del{background:#722}ins{background:#252}'
       '.c{border-color:#555}.jel{color:#aaa}}')


def valtozas_html(motivum, vl, alap, meta):
    reszek = []
    for v in vl:
        ho, hu = _szoveg_diff(v['regi'], v['uj'])
        reszek.append('<div class="par"><div class="jel">%s · %s · %s</div><div class="c">%s</div><div class="c">%s</div></div>'
                      % (_esc(v['jel']), v['tipus'], _esc(v['hely']), ho or '<i>(nem volt)</i>', hu or '<i>(törölve)</i>'))
    fej = '%s változások: %s → %s · %d blokk' % (motivum, alap, meta['commit'], len(vl))
    return ('<!doctype html><html lang="hu"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,'
            'initial-scale=1"><title>%s változásnézet</title><style>%s</style></head><body><h1>%s</h1>%s</body></html>'
            % (_esc(motivum), CSS, _esc(fej), ''.join(reszek) or '<p>Nincs változott blokk.</p>'))


def main():
    ap =argparse.ArgumentParser(description='F165 -- lexikonlap-nézet blokkjelekkel')
    ap.add_argument('motivum')
    ap.add_argument('kimenet', nargs='?')
    ap.add_argument('--ref', default=None, help='git-ág vagy commit, amelynek állapotából a lap készül (alap: munkafa)')
    ap.add_argument('--jel', default=None, help='egy blokk szövegének kiírása a jele alapján (pl. "1/a·12")')
    ap.add_argument('--valtozas', default=None, metavar='ALAP_COMMIT',
                    help='csak a változott blokkok, előtte–utána párban (a régi: a lap fájlja az alap-commitban)')
    a = ap.parse_args()
    if a.valtozas:
        if a.jel:
            raise ValueError('--valtozas és --jel nem együtt')
        regi = _fajl(ROOT, 'lexikon/%s_TUDOMANYOS.md' % a.motivum, a.valtozas)
        md, meta = betolt(a.motivum, a.ref)
        vl = valtozasok(regi, md)
        if a.kimenet:
            kimenet = os.path.abspath(a.kimenet)
            if kimenet.startswith(os.path.abspath(ROOT) + os.sep):
                raise ValueError('a kimenet a repón kívülre menjen (scratch), ne a repóba')
            with open(kimenet, 'w', encoding='utf-8', newline='\n') as f:
                f.write(valtozas_html(a.motivum, vl, a.valtozas, meta))
            print('  %s: %d változott blokk' % (kimenet, len(vl)), file=sys.stderr)
        else:
            for v in vl:
                print('[%s] %s · %s\n- %s\n+ %s\n' % (v['tipus'], v['jel'], v['hely'], v['regi'].replace('\n', ' '),
                                                     v['uj'].replace('\n', ' ')))
        return 0
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
