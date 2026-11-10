"""F105 (FELADATOK #105) 1. lépés: a BDB többszavas héber futamainak mérése a mai megjelenítéshez képest.

Mit mér (csak olvas; a forrás, az adat és a lexikon nem változik):
  1. a `konkordancia/BDB_teljes_unabridged.tsv` szócikkeiben (a szeletelő `lapit` alakjában) a többszavas héber futamok
     számát (legalább két szóköz-tagolt héber token; a rafe-maqqéffel egybeírt tokent külön is számolja);
  2. a futamok állapotát a DT445 javítótáblája szerint (`adat/bdb_forras_javitas.tsv`, `heber_sorrend`): `javitva`
     (a megjelenítés ma cseréli), `valodi_sorrend`, `jelolt_marad`, vagy nincs sora;
  3. a TAHOT-tal ellenőrizhető hányadot: a futamot közvetlenül (legfeljebb írásjel, zárójel és „&c.” közbeiktatásával)
     követi egy hivatkozás, amelynek az `adat/bdb_vers_jelentes.tsv`-ben Károli-verse van és nincs kiszűrve; a vers héber
     szövege a `TAHOT_kivonat.tsv` `Ragozott alak` oszlopa a Károli-kulcson;
  4. a hivatkozott versen a gépi egyezést: a forrásalak (F), a mai megjelenítés (M, a DT445 cseréje) és a lexikon nélküli
     R_hib (R: geres nélkül a tokenek megfordítása, R0; geresnél a DT445 R_str-je, `eszkozok/bdb_jelolt/heber_sorrend.py`)
     mássalhangzó-vázának előfordulását a vers vázfolyamában (teljes szó = betűi; geresszel rövidített token = betűi,
     utána legfeljebb 8 betűnyi rés; betű nélküli token (ellipszis) legfeljebb 60 betűnyi rés; a rafe-maqqéffel egybeírt
     token két szó, köztük nincs rés; a pe/mem forráshiba miatt a váz a פ-t és a מ-t egybeveszi).

Kimenet: `--ki <könyvtár>`: `F105_futamok.tsv` (futamonként egy sor) és `F105_osszesites.txt`.
Futtatás: python naplok/F105_meres.py --ki <könyvtár>
"""
import argparse
import os
import re
import sys
import unicodedata
from collections import Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'olvaso_szerver'))
sys.path.insert(0, os.path.join(REPO, 'eszkozok'))
import bdb_szelet as B  # noqa: E402
import bdb_rovidites as R  # noqa: E402
sys.path.insert(0, os.path.join(REPO, 'eszkozok', 'bdb_jelolt'))
import heber_sorrend as HS  # noqa: E402  (a DT445 szabályai: r0, r_str)

BDB_EN = os.path.join(REPO, 'konkordancia', 'BDB_teljes_unabridged.tsv')
TAHOT = os.path.join(REPO, 'konkordancia', 'TAHOT_kivonat.tsv')
VJ = os.path.join(REPO, 'adat', 'bdb_vers_jelentes.tsv')
JAV = os.path.join(REPO, 'adat', 'bdb_forras_javitas.tsv')

HEB = '֑-ׇא-״יִ-ﭏ'
TOKEN = '[%s]+' % HEB
FUTAM_RE = re.compile(r'%s(?: +%s)+' % (TOKEN, TOKEN))       # legalább két token, csak szóközzel
GERES = '׳'
RAFE = 'ֿ'
# a futam és a hivatkozás között megengedett: írásjel, zárójel, szóköz, „&c.”, LRM
KOZ_RE = re.compile(r'^(?:[\s,;:.()\[\]‎]|&c\.?)*$')


def tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r').split('\t') for s in f if not s.startswith('#')]
    fej = sorok[0]
    return [dict(zip(fej, s)) for s in sorok[1:]]


def pad(st):
    m = re.match(r'^H(\d+)(.*)$', st or '')
    return 'H%04d%s' % (int(m.group(1)), m.group(2)) if m else st


def betuk(s):
    """Mássalhangzó-váz: NFD, minden pont/akcentus/jel ki, a végbetű alapbetűre."""
    s = unicodedata.normalize('NFD', s)
    s = ''.join(c for c in s if 'א' <= c <= 'ת')
    # a végbetű alapbetűre; a pe/mem forráshibát (SEMA 2.31) a váz egybeveszi (mint a DT445 mérése)
    return s.translate(str.maketrans('ךםןףץפ', 'כמנמצמ'))


def szavak(token):
    """Egy token szavai: a rafe-maqqéf (U+05BF a nem első betű után) két szóra bont."""
    nfd = unicodedata.normalize('NFD', token)
    reszek, akt = [], ''
    i = 0
    betu_idx = []
    for c in nfd:
        if 'א' <= c <= 'ת':
            betu_idx.append(len(akt))
        akt += c
    # a rafe-et hordozó betű előtt vágunk (ha nem az első betű)
    vagas = []
    utolso_betu = None
    for j, c in enumerate(akt):
        if 'א' <= c <= 'ת':
            utolso_betu = j
        elif c == RAFE and utolso_betu:
            vagas.append(utolso_betu)
    kezd = 0
    for v in vagas:
        reszek.append(akt[kezd:v])
        kezd = v
    reszek.append(akt[kezd:])
    return [r for r in reszek if betuk(r)]


def minta(tokenek):
    """Regex a vers vázfolyamára; None, ha nincs elég anyag (legalább egy teljes szó és még egy egység)."""
    darabok, teljes = [], 0
    for t in tokenek:
        if not betuk(t):                      # ellipszis (a forrás „…”-je): legfeljebb 60 betűnyi rés
            if darabok:
                darabok.append('.{0,60}?')
            continue
        rov = GERES in t
        for sz in szavak(t.replace(GERES, '')):
            b = betuk(sz)
            if not b:
                continue
            darabok.append(re.escape(b) + ('.{0,8}?' if rov else ''))
            teljes += 0 if rov else 1
    if teljes < 1 or len(darabok) < 2:
        return None
    return re.compile(''.join(darabok))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ki', required=True)
    a = ap.parse_args()
    os.makedirs(a.ki, exist_ok=True)

    # TAHOT: Károli-vers → vázfolyam
    vers = {}
    for d in tsv(TAHOT):
        vers.setdefault(d['Igehely'], []).append(betuk(d.get('Ragozott alak', '')))
    vers = {k: ''.join(v) for k, v in vers.items()}

    # vers-jelentés: Strong → [(poz, karoli_vers, szurt)]
    hiv = {}
    for d in tsv(VJ):
        hiv.setdefault(pad(d['strong']), []).append((int(d['poz']), d.get('karoli_vers', ''), d.get('szurt', '')))
    for v in hiv.values():
        v.sort()

    # DT445 javítótábla: Strong → forrás alak → állapot
    allapot = {}
    for d in tsv(JAV):
        if d.get('hiba') == 'heber_sorrend':
            allapot.setdefault(pad(d['strong']), {})[unicodedata.normalize('NFC', d['forras_alak'])] = d['allapot']

    sorok, c = [], Counter()
    for d in tsv(BDB_EN):
        st = d['Strong_padded']
        flat = B.lapit(d['Teljes_szocikk'])
        megj = R.heber_sorrend_javit(flat, st)
        refs = hiv.get(st, [])
        for m in FUTAM_RE.finditer(flat):
            run = m.group(0)
            tok = run.split(' ')
            c['futam'] += 1
            geres = GERES in run
            rafe = any(len(szavak(t)) > 1 for t in tok)
            c['futam_geres' if geres else 'futam_geres_nelkul'] += 1
            if rafe:
                c['futam_rafe_maqqef'] += 1
            # DT445 állapot: a futam vagy annak része
            alap = allapot.get(st, {})
            all_ = alap.get(unicodedata.normalize('NFC', run), '')
            if not all_:
                all_ = 'reszleges' if any(k in run for k in alap) else 'nincs_sor'
            c['dt445_' + all_] += 1
            # a mai megjelenítés alakja (ugyanaz a csere a futam szövegén)
            disp = R.heber_sorrend_javit(run, st)
            # a lexikon nélküli R_hib (DT445): geres nélkül R0, geresnél R_str
            r0 = HS.r0(run) if GERES not in run else HS.r_str(run)
            # hivatkozás közvetlenül utána
            kv = ''
            for poz, kar, szurt in refs:
                if poz >= m.end():
                    if KOZ_RE.match(flat[m.end():poz]) and kar and szurt != '1':
                        kv = kar
                    break
            itelet = ''
            if kv:
                c['ellenorizheto'] += 1
                vs = vers.get(kv, '')
                if not vs:
                    itelet = 'nincs_tahot'
                else:
                    mf, md, mr = minta(tok), minta(disp.split(' ')), minta(r0.split(' '))  # R = lexikon nélküli R_hib
                    if mf is None or md is None or mr is None:
                        itelet = 'kevés_anyag'
                    else:
                        tf, td, tr = bool(mf.search(vs)), bool(md.search(vs)), bool(mr.search(vs))
                        itelet = 'F%d_M%d_R%d' % (tf, td, tr)
                c['itelet_' + itelet] += 1
                c['itelet_%s_%s' % (all_, itelet)] += 1
            sorok.append([st, str(m.start()), run, disp, r0, all_, '1' if geres else '0', '1' if rafe else '0', kv, itelet])

    with open(os.path.join(a.ki, 'F105_futamok.tsv'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(['strong', 'poz', 'forras', 'megjelenites', 'r_hib', 'dt445', 'geres', 'rafe_maqqef',
                           'karoli_vers', 'itelet']) + '\n')
        for s in sorok:
            f.write('\t'.join(s) + '\n')
    with open(os.path.join(a.ki, 'F105_osszesites.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for k, v in sorted(c.items()):
            f.write('%s\t%d\n' % (k, v))
    print('futamok:', c['futam'], '| ellenőrizhető:', c['ellenorizheto'])


if __name__ == '__main__':
    main()
