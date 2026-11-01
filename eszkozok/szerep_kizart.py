"""Az 1/b. blokk („Kizárt és vizsgált helyek”) olvasói formája — általános, motívumfüggetlen (ISTENTISZT-001 arany lap,
2026-10-29).

Bemenet: a motívum elutasított / nyitva maradt `jeloltek.tsv`-sorai és az `adat/elutasitasi_okok.tsv` mintaszótára. Az adat
nem változik, csak a megjelenítés:
- **miért lett jelölt** — a `forras_kereses` mező szerkezetéből gépileg (`jeloles_oka`): TSK-ajánlás (melyik helyről, a
  szavazat vagy a találatszám, ha a mező hordozza), Károli-kereszthivatkozás, gépi keresés (Strong-keresés, szópár-keresés,
  motívumközi mérés), kutatói felvetés (a tematikus tanulmány, a kereszthivatkozás-napló, nevesített tanító, szótári
  felvetés); ami nem sorolható be: „Egyéb”;
- **döntés és indok** — a döntés, az elutasítás oka a mintaszótárból (`elutasitas_oka`; a be nem sorolható „egyéb”), és az
  `indoklas` szövege változatlanul (a `|` utáni proveniencia-farok nélkül);
- a forrás nyers szövege és az indoklás proveniencia-farka lábjegyzetbe kerül.

TSV: split('\\t'), a '\\r' levágva; csv modul nélkül.
"""
import collections
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OKOK = os.path.join(GYOKER, 'adat', 'elutasitasi_okok.tsv')

CSOPORTOK = ('TSK-ajánlás', 'Károli-kereszthivatkozás', 'Gépi keresés', 'Kutatói felvetés', 'Egyéb')
EGYEB_OK = 'egyéb'
EGYEB_LISTA = 10
HELY = re.compile(r'\b[1-5]?[A-ZÁÉÍÓÖŐÚÜŰ][a-záéíóöőúüű]{1,6} \d+:\d+(?:-\d+)?')
STRONG = re.compile(r'\b[HG]\d{4}\b')


def _sorok(ut):
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8', newline='') as f:
        s = [x.rstrip('\r') for x in f.read().split('\n')]
    s = [x for x in s if x and not x.startswith('#')]
    fej = s[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in s[1:]]


def okok(motivum_id, ut=None):
    """[(lefordított minta, címke)] a mintaszótárból: a motívum saját sorai és a `*` sorok, `sorrend` szerint."""
    sorok = [r for r in _sorok(ut or OKOK) if r['id'] in ('*', motivum_id)]
    return [(re.compile(r['minta'], re.IGNORECASE), r['cimke']) for r in sorted(sorok, key=lambda r: int(r['sorrend']))]


def elutasitas_oka(indoklas, minta):
    for m, cimke in minta:
        if m.search(indoklas or ''):
            return cimke
    return EGYEB_OK


def nevelo(szo):
    """A határozott névelő a kiejtés szerint: „az” magánhangzó és az egy / öt (1, 5) előtt, különben „a”."""
    if not szo:
        return 'a'
    return 'az' if szo[0].lower() in 'aáeéiíoóöőuúüű15' else 'a'


def _ahol(hely, rag):
    return '%s %s %s' % (nevelo(hely), hely, rag)


def _tsk_reszlet(fo):
    p = re.search(r'\(([^)]*)\)', fo)
    if not p:
        return ''
    t = p.group(1).strip()
    v = re.fullmatch(r'Votes=(-?\d+)', t)
    if v:
        return ', %s szavazat' % v.group(1)
    v = re.fullmatch(r'(\d+) találat', t)
    if v:
        return ', a forráshelyen %s TSK-találat' % v.group(1)
    if re.fullmatch(r'[\d\s,\-–]+', t):
        return ', szavazat: %s' % t
    return ''


def jeloles_oka(forras_kereses):
    """(csoport, közérthető szöveg) a `forras_kereses` mezőből; a be nem sorolható: ('Egyéb', a mező fő része)."""
    nyers = (forras_kereses or '').split(' | ')[0].strip()
    fo = re.split(r';\s*napló:', nyers)[0].strip()
    helyek = HELY.findall(fo)
    hely = helyek[0] if helyek else ''
    if fo.startswith('TSK/Károli-KH'):
        return CSOPORTOK[1], ('TSK- és Károli-kereszthivatkozás %s' % _ahol(hely, 'helyről') if hely
                              else 'TSK- és Károli-kereszthivatkozás')
    if fo.startswith('TSK'):
        if 'alacsony szavazat' in fo:
            return CSOPORTOK[0], 'TSK-ajánlás, alacsony szavazattal'
        cel = (' ' + _ahol(helyek[1], 'helyre')) if ('→' in fo or '↔' in fo) and len(helyek) > 1 else ''
        szoveg = 'TSK-ajánlás %s%s%s' % (_ahol(hely, 'helyről'), cel, _tsk_reszlet(fo)) if hely else 'TSK-ajánlás'
        if 'Károli-KH is' in fo:
            szoveg += ' (a Károli is ajánlja)'
        if re.match(r'scan', fo):
            szoveg += ' és gépi Strong-keresés'
        return CSOPORTOK[0], szoveg
    if fo.startswith('Károli-KH'):
        return CSOPORTOK[1], ('Károli-kereszthivatkozás %s' % _ahol(hely, 'helyről') if hely
                              else 'Károli-kereszthivatkozás')
    if re.match(r'scan', fo):
        st = STRONG.findall(fo)
        szoveg = 'gépi Strong-keresés: %s' % ', '.join(st) if st else 'gépi Strong-keresés'
        if 'TSK' in fo:
            szoveg += ', TSK-ajánlással'
        return CSOPORTOK[2], szoveg
    if fo.startswith('kollokacio'):
        return CSOPORTOK[2], 'gépi szópár-keresés: %s' % ' + '.join(STRONG.findall(fo))
    if fo.startswith('motívumközi'):
        return CSOPORTOK[2], 'motívumközi mérés (szomszédos vers egy másik motívumban)'
    if 'Seol-scan' in fo:
        return CSOPORTOK[2], 'gépi keresés a szó környezetében (Seol-ablak)'
    if 'visszakeresés' in fo:
        return CSOPORTOK[2], 'gépi visszakeresés a héber szövegben'
    if fo.startswith('tematikus:'):
        p = re.search(r'\(([^)]*)\)\s*$', fo)
        return CSOPORTOK[3], 'a tematikus tanulmány felvetése' + (' (%s)' % p.group(1) if p else '')
    if fo.startswith('napló:') or (not fo and 'napló:' in nyers):
        return CSOPORTOK[3], 'a kereszthivatkozás-napló kutatói minősítése'
    if fo.startswith('nevesített tanító'):
        t = re.match(r'nevesített tanító:\s*([^(;]+)', fo)
        return CSOPORTOK[3], 'nevesített tanító felvetése' + (': %s' % t.group(1).strip() if t else '')
    if fo.startswith('BDB'):
        return CSOPORTOK[3], 'szótári felvetés (BDB)'
    if fo.startswith('study') or fo.startswith('döntési fájl'):
        return CSOPORTOK[3], 'a tanulmány felvetése'
    return CSOPORTOK[4], fo or '—'


def _cella(s):
    return s.replace('|', '\\|').replace('\n', ' ')


def blokk_torzs(sorok, motivum_id, okok_ut=None):
    """(törzs-sorok listája, lábjegyzetek listája, összesítő dict) az 1/b. blokkhoz."""
    minta = okok(motivum_id, okok_ut)
    csop = collections.OrderedDict((c, []) for c in CSOPORTOK)
    ok_szaml, forras_szaml, egyeb = collections.Counter(), collections.Counter(), []
    labj = []
    for r in sorok:
        c, miert = jeloles_oka(r.get('forras_kereses'))
        forras_szaml[c] += 1
        ind = r.get('indoklas') or ''
        fo_ind, _sep, farok = ind.partition(' | ')
        if r.get('dontes') == 'nyitva':
            dontes = '**nyitott döntés**'
            ok_szaml['nyitott döntés'] += 1
        else:
            ok = elutasitas_oka(fo_ind, minta)
            ok_szaml[ok] += 1
            if ok == EGYEB_OK:
                egyeb.append(r['igehely'])
            dontes = '**elutasítva** — %s' % ok
        lj = 'forrás: `%s`%s' % (r.get('forras_kereses') or '—', (' · ' + farok) if farok else '')
        csop[c].append((r['igehely'], _cella(miert), '%s: %s' % (dontes, _cella(fo_ind) or '—'), lj))
    ki = []
    for c, sorok_c in csop.items():
        if not sorok_c:
            continue
        sor_md = []
        for hely, miert, dont, lj in sorok_c:
            labj.append(lj)
            sor_md.append('| %s | %s[^k%d] | %s |' % (hely, miert, len(labj), dont))
        ki.append('**%s** (%d)' % (c, len(sorok_c)))
        ki.append('| Igehely | Miért lett jelölt | Döntés és indok |\n|---|---|---|\n' + '\n'.join(sor_md))
    ossz = {'ok': ok_szaml, 'forras': forras_szaml, 'egyeb': egyeb}
    return ki, labj, ossz


def osszesito_sor(ossz):
    """Az összesítő bekezdés: az elutasítás okai (gyakoriság szerint, az egyéb és a nyitott a végén), a jelölés forrásai."""
    ok = ossz['ok']
    rend = sorted((k for k in ok if k not in (EGYEB_OK, 'nyitott döntés')), key=lambda k: (-ok[k], k))
    reszek = ['%s %d' % (k, ok[k]) for k in rend]
    if ok.get(EGYEB_OK):
        eg = ossz['egyeb']
        reszek.append('%s %d (%s)' % (EGYEB_OK, ok[EGYEB_OK], ', '.join(eg) if len(eg) <= EGYEB_LISTA
                                       else 'a mintaszótár nem sorolja be; l. a táblázatokban'))
    sor = ['**Az elutasítás okai:** ' + (' · '.join(reszek) if reszek else '—')]
    if ok.get('nyitott döntés'):
        sor.append('**Nyitott döntés:** %d' % ok['nyitott döntés'])
    sor.append('**A jelölés forrása:** ' + ' · '.join('%s %d' % (c, ossz['forras'][c]) for c in CSOPORTOK
                                                     if ossz['forras'].get(c)))
    return '\n\n'.join(sor)
