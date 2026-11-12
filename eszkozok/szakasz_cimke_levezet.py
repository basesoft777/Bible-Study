#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
eszkozok/szakasz_cimke_levezet.py -- F148 (c): a szakaszcímke gépi levezetése a `jelentes_szam`-ból
(F148_UJ_MOTIVUM_VEDOKORLAT_BRIEF.md 3. lépés, DT438, DT439; SEMA 2.40).

Az előfordulás-sor `lexikon_szotar` + `lexikon_entry_id` + `jelentes_szam` hármasából a szótár szakaszát
vezeti le, csak a `bdb_szakaszok.tsv` / `thayer_szakaszok.tsv` létező útvonalai közül (BDB: binyan + számozás,
`2.c` → `Qal/2/c`, `1` → `-/1/-`; Thayer: `2` → `-/2/-`; TBESG: a `lexikon_hivatkozasok.tsv` kulcsa).
Eltérésnél JELEZ, nem választ és nem tölt ki (CLAUDE.md 3. szabály):
  J1 a szótár saját példahelye más pontra mutat, és egyik sem esik a másik alá (GerincHiba-eset, DT374)
  J2 két pont: alternatíva (`Nif'ál / Hif'íl`), két szám, több binyan, vagy a példák két útvonalra mutatnak
  J3 üres mező
  J4 a jelnek nincs útvonala a szótárban
  J5 tagolatlan szócikk (DT438)
  J6 minősítő alak (`2.c (tagadva)`)
  J7 a címke gépileg nem képezhető (DT439: üres / fordításra váró glossza, tiltott minta)
  J8 a levezetett szakasz eltér a táblában álló kézi leképezéstől, vagy a szakasz sora más kulcsra mutat

    python eszkozok/szakasz_cimke_levezet.py ellenoriz --id ALVIL-001 [--ki FAJL]
    python eszkozok/szakasz_cimke_levezet.py ellenoriz --id ALVIL-001 --ir

Kimenet: a `--ki`, különben a repón kívüli ideiglenes könyvtár `F148_levezetes_<ID>.tsv`-je (F203, N-F12e: a repóba csak
kifejezett `--ki` ír), soronként proveniencia-sorral. Az `--ir` csak a jelzés nélküli
sorokat írja a `adat/szotar_szakasz_cimke.tsv`-be: új sort (gépi címkével, DT439 (1)), vagy egy meglévő
sor üres `lexikon_jelentes_szam`-ját pótolja; meglévő címkét nem ír felül. Írás előtt az eredeti sorokkal
összevet, eltérésnél megáll (minta: `eszkozok/igazolas_migracio.py`).
"""

import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import general as G  # noqa: E402
import lexikon_general as LG  # noqa: E402

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = G.ROOT
CIMKE_TSV = os.path.join(ROOT, LG.SZAKASZ_CIMKE_FAJL)
CIMKE_FEJ = ['szotar', 'strong', 'bdb_id', 'szakasz', 'lexikon_jelentes_szam', 'cimke_hu', 'proveniencia', 'megjegyzes']
KI_FEJ = ['id', 'igehely', 'szotar', 'strong', 'jelentes_szam', 'bdb_id', 'levezetett_szakasz', 'kezi_szakasz', 'egyezik',
          'jelzes', 'jelzes_reszlet', 'cimke_hu_javaslat', 'teendo', 'proveniencia']
TAGOLATLAN = 'tagolatlan'
SZAM_RE = re.compile(r'^\d+(?:\.[0-9a-zα-ω]+)*$')
# 17. szabály (ellenoriz.py SZAKASZ_CIMKE_TILTOTT) mintája: a címke nem minősít
CIMKE_TILTOTT = re.compile(r'(?i)(motívum|invokál|invokáci|(?<![\wáéíóöőúüű])nem(?![\wáéíóöőúüű]))')
GLOSSZA_VEG_RE = re.compile(r'[,;(\[֐-׿Ͱ-Ͽἀ-῿]|\s\d|\s[IVX]+\.|=')
JEL_ELEJE_RE = re.compile(r'^\s*(?:\d+\.?|[a-zα-ω]\.)\s+')
GLOSSZA_NEM_JO_RE = re.compile(r'(?i)^(?:pl\.|vö\.|l\.|ld\.|stb\.)')
# A binyan a vers héber morfológiájából (Macula-héber `morf`, OSHB-jelölés: `V` + törzsbetű), ha a `jelentes_szam`
# számozása több binyan alatt is áll (pl. H7121 `2.c`: Qal és Niph'al). Csak az egyértelmű megfeleltetés.
MACULA_GLOB = 'Macula_heber_'
TORZS_BINYAN = {'q': 'Qal', 'N': "Niph'al", 'p': "Pi'el", 'P': "Pu'al", 'h': "Hiph'il", 'H': "Hoph'al",
                't': "Hithpa'el", 'l': 'Pilpel', 'f': 'Hithpalpel', 'm': "Po'el", 'r': "Hithpo'el"}


VERSMEGF_TSV = os.path.join(ROOT, 'konkordancia', 'Karoli_versmegfeleltetes.tsv')
_macula_cache = {}
_versmegf_cache = {}


def _versmegf():
    """{Károli-igehely: MT-vers (`64:6`)} a `Karoli_versmegfeleltetes.tsv`-ből (a mai kulcs; F117, F146); csak az
    MT-t adó sorok."""
    if not _versmegf_cache:
        for r in G.tsv_beolvas(VERSMEGF_TSV)[1]:
            if r.get('igehely_mt'):
                _versmegf_cache[r['igehely_karoli']] = r['igehely_mt']
    return _versmegf_cache


def macula_torzsek(strong):
    """Károli-vers → {törzsbetű} (`MaculaKaroli`) a Strong igei tokenjeire, a `konkordancia/Macula_heber_*.tsv`-ből (`split('\\t')`).
    A kulcs a Macula MT-hivatkozásából (`ref`, pl. `ISA 64:6!2`) a mai versmegfeleltetésen át képzett Károli-vers;
    a Macula saját `karoli` oszlopát csak a könyv azonosítására használja (az F17-ben, a #117/#146 előtti
    megfeleltetéssel készült: az Ézs 64:6 MT ott Károli 64:7, a mai táblában 64:6)."""
    if strong in _macula_cache:
        return _macula_cache[strong]
    mt_szerint, konyv, macula_karoli = {}, {}, {}
    konk = os.path.join(ROOT, 'konkordancia')
    for nev in sorted(os.listdir(konk)):
        if not (nev.startswith(MACULA_GLOB) and nev.endswith('.tsv')):
            continue
        with open(os.path.join(konk, nev), encoding='utf-8') as f:
            fej = None
            for s in f:
                if s.startswith('#'):
                    continue
                m = s.rstrip('\r\n').split('\t')
                if fej is None:
                    fej = {k: i for i, k in enumerate(m)}
                    continue
                kod, mt = m[fej['ref']].split('!')[0].split(' ')
                konyv.setdefault(m[fej['karoli']].rsplit(' ', 1)[0], kod)
                macula_karoli.setdefault((kod, mt), m[fej['karoli']])
                if m[fej['strong']] != strong:
                    continue
                morf = m[fej['morf']]
                if morf.startswith('V') and len(morf) > 1:
                    mt_szerint.setdefault((kod, mt), set()).add(morf[1])
    out = MaculaKaroli(mt_szerint, konyv, macula_karoli)
    _macula_cache[strong] = out
    return out


class MaculaKaroli(object):
    """Károli-vers → {törzsbetű}: az MT-vers a versmegfeleltetésből. Ahol a tábla nem ad MT-t (a KJV osztályú
    sorok), a Károli fejezet:verse csak akkor MT, ha a Macula saját `karoli` oszlopa ugyanezt a verset adja;
    eltérésnél (pl. Mik 5:1: az MT 5:1 a Maculában Károli 5:2) nincs morfológia, a levezetés jelez (ELLENOR_F148 2.)."""

    def __init__(self, mt_szerint, konyv, macula_karoli=None):
        self.mt_szerint, self.konyv, self.macula_karoli = mt_szerint, konyv, macula_karoli or {}

    def get(self, karoli, alap=None):
        if ' ' not in karoli:
            return alap
        konyvnev, cv = karoli.rsplit(' ', 1)
        kod = self.konyv.get(konyvnev)
        mt = _versmegf().get(karoli)
        if not mt:
            mt = cv
            if self.macula_karoli.get((kod, mt), karoli) != karoli:
                return alap
        return self.mt_szerint.get((kod, mt), alap)


def vag(ut):
    return LG.gerinc_utvonal_vag(ut)


def ala_esik(a, b):
    """a az b alá esik (vagy azonos): a levágott útvonalak szegmensei szerint."""
    sa, sb = vag(a).split('/'), vag(b).split('/')
    return sa[:len(sb)] == sb


def szotar_utvonalak(adat, szotar, strong):
    """A szócikk szakaszútvonalai (`cim`/`fej` nélkül)."""
    return [k[1] for k in szotar_kulcsok(adat, szotar, strong)]


def szotar_kulcsok(adat, szotar, strong):
    """A szakaszok kulcsai (bdb_id, utvonal), `cim`/`fej` nélkül (F123.BDBGER: a BDB-útvonal csak a szócikken belül
    egyedi; a Thayer kulcsa ('', utvonal))."""
    kulcs = {'BDB': 'bdb_sz', 'Thayer': 'th_sz'}.get(szotar)
    if not kulcs:
        return []
    return [(r.get('bdb_id', '') if szotar == 'BDB' else '', r['utvonal'])
            for r in adat[kulcs].get(strong, []) if r['utvonal'] not in ('cim', 'fej')]


def tagolatlan_szocikk(adat, szotar, strong):
    return szotar == 'BDB' and bool(adat['bdb_sz'].get(strong)) and not szotar_utvonalak(adat, szotar, strong)


def peldak(adat, szotar, strong, vers):
    """A szótár saját példahelyeinek útvonalai a versre (`fej`/`cim`/`tagolatlan` nélkül)."""
    kulcs = {'BDB': 'bdb_vj', 'Thayer': 'th_vj'}.get(szotar)
    if not kulcs:
        return []
    return sorted({r['utvonal'] for r in adat[kulcs].get((strong, vers), [])
                   if r['utvonal'] not in ('fej', 'cim', TAGOLATLAN, '')})


def levezet_sor(adat, sor, lexhiv):
    """(levezetett szakaszkulcs (bdb_id, utvonal) vagy None, [(jelzés, részlet)])."""
    szotar, strong = sor.get('lexikon_szotar', ''), sor.get('lexikon_entry_id', '')
    jsz = (sor.get('jelentes_szam') or '').strip()
    if not (szotar and strong and jsz):
        return None, [('J3', 'üres mező: %s' % ', '.join(m for m, v in (('lexikon_szotar', szotar),
                      ('lexikon_entry_id', strong), ('jelentes_szam', jsz)) if not v))]
    if jsz == TAGOLATLAN or tagolatlan_szocikk(adat, szotar, strong):
        return None, [('J5', 'tagolatlan szócikk (%s %s)' % (szotar, strong))]
    jelzes = []
    kulcs, minosito = LG.kutatoi_kulcs(jsz)
    if minosito:
        jelzes.append(('J6', 'minősítő: „%s”' % minosito))
    if '/' in kulcs or ',' in kulcs or ' és ' in kulcs:
        return None, jelzes + [('J2', 'alternatíva vagy két szám: „%s”' % kulcs)]
    if szotar == 'TBESG':
        if (szotar, strong, kulcs) in lexhiv:
            return ('', kulcs), jelzes
        return None, jelzes + [('J4', 'a TBESG-kulcs nincs a lexikon_hivatkozasok.tsv-ben: %s' % kulcs)]
    if not SZAM_RE.match(kulcs):
        return None, jelzes + [('J4', 'a jel nem számozás („%s”), nincs útvonala' % kulcs)]
    szegm = kulcs.split('.')
    jeloltek = sorted({k for k in szotar_kulcsok(adat, szotar, strong) if vag(k[1]).split('/')[1:] == szegm})
    if not jeloltek:
        return None, jelzes + [('J4', '„%s”: nincs ilyen útvonal a %s %s szócikkben' % (kulcs, szotar, strong))]
    if len({k[0] for k in jeloltek}) > 1:
        # F123.BDBGER: a számozás a Strong több BDB-szócikkében is áll; a jelentésszám nem mondja meg, melyikben
        return None, jelzes + [('J2', 'több szócikk: %s' % ', '.join('%s %s' % k for k in jeloltek))]
    if len(jeloltek) > 1 and szotar == 'BDB':
        torzsek = (adat.get('macula') or macula_torzsek)(strong).get(sor.get('igehely', ''), set())
        binyanok = {TORZS_BINYAN.get(t, '?%s' % t) for t in torzsek}
        szukitett = [k for k in jeloltek if k[1].split('/')[0] in binyanok]
        if len(szukitett) == 1 and len(binyanok) == 1:
            jeloltek = szukitett
            jelzes.append(('I', 'binyan a Macula-héber morfológiájából (V%s)' % next(iter(torzsek))))
        else:
            return None, jelzes + [('J2', 'több binyan: %s; a vers morfológiája (Macula): %s'
                                    % (', '.join(k[1] for k in jeloltek), ', '.join(sorted(binyanok)) or 'nincs igei token'))]
    if len(jeloltek) > 1:
        return None, jelzes + [('J2', 'több útvonal: %s' % ', '.join(k[1] for k in jeloltek))]
    ut = jeloltek[0]
    pl = peldak(adat, szotar, strong, sor.get('igehely', ''))
    kulon = sorted({vag(p) for p in pl})
    if len(kulon) > 1 and not all(ala_esik(a, b) or ala_esik(b, a) for a in kulon for b in kulon):
        jelzes.append(('J2', 'a szótár példái két útvonalra mutatnak: %s' % ', '.join(kulon)))
    for p in kulon:
        if not (ala_esik(p, ut[1]) or ala_esik(ut[1], p)):
            jelzes.append(('J1', 'a szótár példahelye %s, a levezetett %s (egyik sem esik a másik alá)' % (p, vag(ut[1]))))
    return ut, jelzes


def elso_glossza(szoveg):
    """DT439 (1): a magyar szakaszszöveg első glosszája (a jel, a címkeszerű előtag és a héber/görög,
    igehely, zárójel előtti rész)."""
    if not szoveg:
        return ''
    s = JEL_ELEJE_RE.sub('', szoveg.strip())
    m = GLOSSZA_VEG_RE.search(s)
    s = s[:m.start()] if m else s
    if ':' in s:
        s = s.split(':', 1)[1]
    return s.strip(' .:—–-')


def szakasz_hu(adat, szotar, strong, k):
    """A szakasz (kulcs: (bdb_id, utvonal)) magyar szövege: BDB a `bdb_szakasz_hu.tsv`-ből, Thayer a #142 `sz<n>`
    soraiból; None, ha nincs."""
    ut = k[1]
    if szotar == 'BDB':
        for r in adat['bdb_sz'].get(strong, []):
            if r.get('bdb_id', '') == k[0] and r['utvonal'] == ut:
                hu = adat['bdb_hu'].get((strong, r['sorszam'])) or {}
                return hu.get('szoveg_hu') or None
        return None
    if szotar == 'Thayer':
        for u, _jel, hu, _angol, _forras in LG.thayer_gerinc_szakaszok(adat, strong):
            if u == ut:
                return hu
    return None


def cimke_javaslat(adat, szotar, strong, ut, tiltott):
    """(címke vagy '', [jelzés])."""
    hu = szakasz_hu(adat, szotar, strong, ut)
    if not hu:
        return '', [('J7', 'nincs magyar szakaszszöveg (fordításra vár)')]
    g = elso_glossza(hu)
    if not g or GLOSSZA_NEM_JO_RE.match(g):
        return '', [('J7', 'az első glossza üres vagy nem glossza: „%s”' % g)]
    if CIMKE_TILTOTT.search(g):
        return '', [('J7', 'a glossza tiltott minősítést tartalmaz: „%s”' % g)]
    for t in tiltott:
        if t.get('minta') and re.search(t['minta'], g, re.I):
            return '', [('J7', 'a glossza tiltott fordulatot tartalmaz (%s): „%s”' % (t.get('magyar_alak'), g))]
    return g, []


def ellenoriz(motivum_id, adat=None, elofordulasok=None, lexhiv=None, ts=None):
    """A motívum soraira: [kimeneti sor dict], és a javasolt írások {(szotar, strong, szakasz): teendő}."""
    adat = adat or LG.gerinc_adat()
    if elofordulasok is None:
        elofordulasok = G.tsv_beolvas(G.ELOFORDULASOK_TSV)[1]
    if lexhiv is None:
        lexhiv = {(r['szotar'], r['strong'], r['jelentes_szam'])
                  for r in G.tsv_beolvas(os.path.join(ROOT, 'adat', 'lexikon_hivatkozasok.tsv'))[1]}
    ts = ts or datetime.date.today().isoformat()
    tiltott = adat.get('tiltott') or []
    ki = []
    for sor in [r for r in elofordulasok if r['id'] == motivum_id]:
        szotar, strong = sor.get('lexikon_szotar', ''), sor.get('lexikon_entry_id', '')
        ut, jelzes = levezet_sor(adat, sor, lexhiv)
        info = [r for j, r in jelzes if j == 'I']
        jelzes = [(j, r) for j, r in jelzes if j != 'I']
        kulcs, _m = LG.kutatoi_kulcs(sor.get('jelentes_szam', ''))
        try:
            kezi = LG.kutatoi_szakasz(adat, szotar, strong, kulcs) if kulcs and szotar else None
        except LG.GerincHiba as exc:
            kezi, jelzes = None, jelzes + [('J8', str(exc))]
        egyezik = ''
        teendo = ''
        cimke = ''
        if ut and kezi:
            egyezik = 'igen' if (ut[0], vag(ut[1])) == (kezi[0], vag(kezi[1])) else 'nem'
            if egyezik == 'nem':
                jelzes.append(('J8', 'a táblában álló kézi leképezés: %s' % ' '.join(x for x in kezi if x)))
        elif ut:
            meglevo = adat['cimke'].get((szotar, strong) + ut)
            if meglevo is not None and meglevo.get('lexikon_jelentes_szam'):
                jelzes.append(('J8', 'a %s szakasz sora más kulcsra mutat: „%s”' % (ut[1], meglevo['lexikon_jelentes_szam'])))
            elif meglevo is not None:
                teendo, cimke = 'kulcs_potlas', meglevo.get('cimke_hu', '')
            else:
                cimke, cj = cimke_javaslat(adat, szotar, strong, ut, tiltott)
                jelzes += cj
                teendo = 'uj_sor' if not cj else ''
        if teendo and (szotar, strong, kulcs) not in lexhiv:
            # 17. szabály: a `lexikon_jelentes_szam` létező `lexikon_hivatkozasok.tsv`-kulcs (ELLENOR_F148 3.)
            jelzes.append(('J8', 'a kulcs (%s %s %s) nincs a lexikon_hivatkozasok.tsv-ben' % (szotar, strong, kulcs)))
        if jelzes:
            teendo = ''
        ki.append({
            'id': sor['id'], 'igehely': sor['igehely'], 'szotar': szotar, 'strong': strong,
            'jelentes_szam': sor.get('jelentes_szam', ''), 'bdb_id': (ut or kezi or ('', ''))[0],
            'levezetett_szakasz': ut[1] if ut else '', 'kezi_szakasz': kezi[1] if kezi else '',
            'egyezik': egyezik, 'jelzes': ','.join(sorted({j for j, _ in jelzes})),
            'jelzes_reszlet': ' · '.join(r for _, r in jelzes), 'cimke_hu_javaslat': cimke, 'teendo': teendo,
            'proveniencia': 'scope=%s %s (%s %s „%s”) | forras=szakasz_cimke_levezet.py%s | ts=%s'
                            % (sor['id'], sor['igehely'], szotar, strong, sor.get('jelentes_szam', ''),
                               ' (%s; konkordancia/Macula_heber_*.tsv)' % info[0] if info else '', ts)})
    return ki


def irasok(ki):
    """{(szotar, strong, bdb_id, szakasz): (teendő, kulcs, címke)} a jelzés nélküli sorokból; ugyanarra a szakaszra két
    különböző kulcs vagy teendő: ValueError (nem választ)."""
    out = {}
    for r in ki:
        if not r['teendo']:
            continue
        k = (r['szotar'], r['strong'], r['bdb_id'], r['levezetett_szakasz'])
        ertek = (r['teendo'], LG.kutatoi_kulcs(r['jelentes_szam'])[0], r['cimke_hu_javaslat'])
        if k in out and out[k] != ertek:
            raise ValueError('ugyanarra a szakaszra két írás: %s → %s / %s' % (k, out[k], ertek))
        out[k] = ertek
    return out


def ir_tabla(ut, irando, ts):
    """A szotar_szakasz_cimke.tsv frissítése: új sor a végére, vagy üres `lexikon_jelentes_szam` pótlása.
    Írás előtt és után összevet: minden eredeti sor változatlan, kivéve a pótolt mezőt."""
    with open(ut, encoding='utf-8', newline='') as f:
        nyers = f.read()
    sorveg = '\r\n' if '\r\n' in nyers else '\n'
    sorok = nyers.split(sorveg)
    if sorok and sorok[-1] == '':
        sorok = sorok[:-1]
    fej = sorok[0].split('\t')
    if fej != CIMKE_FEJ:
        raise SystemExit('a szotar_szakasz_cimke.tsv fejléce eltér: %s' % fej)
    uj, potolt = list(sorok), set()
    idx = {tuple(s.split('\t')[:4]): i for i, s in enumerate(sorok) if i}
    for k, (teendo, kulcs, cimke) in sorted(irando.items()):
        if teendo == 'kulcs_potlas':
            i = idx[k]
            mezok = uj[i].split('\t')
            if mezok[4]:
                raise SystemExit('megállás: a %s sor kulcsa nem üres („%s”)' % (k, mezok[4]))
            mezok[4] = kulcs
            mezok[7] = ('%s; ' % mezok[7] if mezok[7] else '') + \
                'lexikon_jelentes_szam: szakasz_cimke_levezet.py (gépi, F148), ts=%s' % ts
            uj[i] = '\t'.join(mezok)
            potolt.add(i)
        elif teendo == 'uj_sor':
            if k in idx:
                raise SystemExit('megállás: a %s sor már létezik' % (k,))
            uj.append('\t'.join([k[0], k[1], k[2], k[3], kulcs, cimke,
                                 'scope=%s %s %s | forras=szakasz_cimke_levezet.py (gépi, DT439) | ts=%s'
                                 % (k[0], k[1], k[3], ts), '']))
    for i, s in enumerate(sorok):
        if i not in potolt and uj[i] != s:
            raise SystemExit('megállás: az eredeti %d. sor megváltozott volna' % i)
    for i in potolt:
        a, b = sorok[i].split('\t'), uj[i].split('\t')
        if [x for j, x in enumerate(a) if j not in (4, 7)] != [x for j, x in enumerate(b) if j not in (4, 7)]:
            raise SystemExit('megállás: a pótolt %d. sorban más mező is változott volna' % i)
    with open(ut, 'w', encoding='utf-8', newline='') as f:
        f.write(sorveg.join(uj) + sorveg)
    with open(ut, encoding='utf-8', newline='') as f:
        vissza = f.read().split(sorveg)[:-1]
    if vissza != uj:
        raise SystemExit('megállás: a visszaolvasott tábla eltér a megírttól')
    return len(potolt), len(uj) - len(sorok)


def kiir(ki, ut):
    with open(ut, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(KI_FEJ) + '\n')
        for r in ki:
            f.write('\t'.join(str(r[k]).replace('\t', ' ').replace('\n', ' ') for k in KI_FEJ) + '\n')


def ki_ut_alap(mid):
    """F203 (N-F12e): a `--ki` nélküli kimenet a repón kívül (az ideiglenes könyvtárban), nem a `naplok/`-ban."""
    import tempfile
    return os.path.join(tempfile.gettempdir(), 'F148_levezetes_%s.tsv' % mid)


def main():
    a = sys.argv[1:]
    if not a or a[0] != 'ellenoriz' or '--id' not in a:
        raise SystemExit('hasznalat: szakasz_cimke_levezet.py ellenoriz --id <ID> [--ki FAJL] [--ir]')
    mid = a[a.index('--id') + 1]
    ki_ut = a[a.index('--ki') + 1] if '--ki' in a else ki_ut_alap(mid)
    ts = datetime.date.today().isoformat()
    ki = ellenoriz(mid, ts=ts)
    kiir(ki, ki_ut)
    jelzett = [r for r in ki if r['jelzes']]
    elter = [r for r in ki if r['egyezik'] == 'nem']
    print('%s: %d sor, levezetve %d, egyezik a kézivel %d, eltér %d, jelzés %d; kimenet: %s'
          % (mid, len(ki), sum(1 for r in ki if r['levezetett_szakasz']), sum(1 for r in ki if r['egyezik'] == 'igen'),
             len(elter), len(jelzett), ki_ut))
    for r in jelzett:
        print('  %s %s [%s] %s' % (r['igehely'], r['jelentes_szam'], r['jelzes'], r['jelzes_reszlet']))
    irando = irasok(ki)
    print('írandó (jelzés nélkül): %d' % len(irando))
    for k, v in sorted(irando.items()):
        print('  %s → %s' % (k, v))
    if '--ir' in a and irando:
        p, u = ir_tabla(CIMKE_TSV, irando, ts)
        print('írva: %d kulcspótlás, %d új sor (%s)' % (p, u, CIMKE_TSV))


if __name__ == '__main__':
    main()
