#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F22 — a két modell (Sonnet + C) válaszainak egyesítése könyvenként; API és hálózat nélkül,
determinisztikus (ugyanazokból a bemenetekből bájtra azonos kimenet).

Bemenet: f22/minta_<könyv>.tsv, f22/valaszok/sonnet/<könyv>.jsonl, f22/valaszok/c/<könyv>.jsonl,
konkordancia/Karoli_1908.tsv (tokenizálás: tokenek.py), konkordancia/TAHOT_kivonat.tsv.
A Strong-számot a modell nem írja: a `strong` oszlopot a szkript veszi a TAHOT-ból, a linkelt
eredeti szó sorszáma alapján.

Kimenet:
  adat/karoli_strong/parok_<könyv>.tsv   linkenként egy sor
     vers, hu_sorszam, hu_szo, er_sorszam, er_szo, strong, bizonyossag (magas|alacsony|kezi), forras (S+C|S|C)
  adat/karoli_strong/szavak_<könyv>.tsv  tokenenként egy sor (minden Károli- és minden eredeti token)
     vers, oldal (hu|er), sorszam, szo, allapot (parositva|betoldas|forditatlan|fuggoben),
     partner_sorszam, strong, bizonyossag, forras
  naplok/F22_<könyv>_atnezes.tsv         a `kezi` versek (mindkét modell kapuhibás), linkek nélkül

Bizonyossági szabály (a brief 22.4):
  * `magas`: mindkét modell ugyanazt a linket adta (link-szint); token-szinten: a két modell ugyanazt
    a partnerhalmazt, vagy ugyanazt a betoldas/forditatlan döntést hozta;
  * `alacsony`: a két modell eltér; a Sonnet változata kerül a táblába (forras S);
  * ha csak az egyik modell ment át a kapun: annak változata, alacsony, forras S vagy C;
  * `kezi`: mindkét modell kapuhibás; a vers az átnézési sorba kerül, linkek nélkül (a szavak tábla
    soraiban allapot=fuggoben).
A C-nek csak a Sonnet változatától eltérő linkjei nem kerülnek a táblába.

Használat:
    python eszkozok/karoli_strong/egyesit.py --konyv 1Móz            # a két tábla és az átnézési sor írása
    python eszkozok/karoli_strong/egyesit.py --konyv 1Móz --ellenoriz   # lefedettség + Strong-levezethetőség, írás nélkül
    python eszkozok/karoli_strong/egyesit.py --onteszt

Kilépési kódok: 0 rendben; 1 az ellenőrzés hibát talált; 2 hibás paraméter/hiányzó bemenet.
"""

import argparse
import hashlib
import json
import os
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sonnet_koteg  # noqa: E402
import tokenek  # noqa: E402

ROOT = tokenek.ROOT
PAROK_FEJ = ['vers', 'hu_sorszam', 'hu_szo', 'er_sorszam', 'er_szo', 'strong', 'bizonyossag', 'forras']
SZAVAK_FEJ = ['vers', 'oldal', 'sorszam', 'szo', 'allapot', 'partner_sorszam', 'strong', 'bizonyossag', 'forras']
ATNEZES_FEJ = ['vers', 'sonnet_hiba', 'c_hiba']


def utak(konyv, gyoker=None):
    g = gyoker or ROOT
    n = sonnet_koteg.ascii_nev(konyv)
    return {
        'parok': os.path.join(g, 'adat', 'karoli_strong', 'parok_%s.tsv' % n),
        'szavak': os.path.join(g, 'adat', 'karoli_strong', 'szavak_%s.tsv' % n),
        'atnezes': os.path.join(g, 'naplok', 'F22_%s_atnezes.tsv' % n),
        'sonnet': os.path.join(g, 'f22', 'valaszok', 'sonnet', '%s.jsonl' % n),
        'c': os.path.join(g, 'f22', 'valaszok', 'c', '%s.jsonl' % n),
        'minta': os.path.join(g, 'f22', 'minta_%s.tsv' % n),
        'kezi_versek': os.path.join(g, 'f22', 'kezi_versek_%s.tsv' % n),
        # javító menet (a versbeosztás-detektor megfeleltetésével újrafuttatott versek): külön minta és válaszfájlok;
        # a javító menet verse felülírja a fő menet ugyanazon versének válaszát
        'minta_javito': os.path.join(g, 'f22', 'minta_%s_javito.tsv' % n),
        'sonnet_javito': os.path.join(g, 'f22', 'valaszok', 'sonnet', '%s_javito.jsonl' % n),
        'c_javito': os.path.join(g, 'f22', 'valaszok', 'c', '%s_javito.jsonl' % n),
    }


def jsonl_versek(ut):
    """{igehely: {'allapot','probalkozas','hibak','obj'}}; a kapuhibás versnek obj=None."""
    ki = {}
    if not os.path.exists(ut):
        return ki
    with open(ut, encoding='utf-8') as f:
        for s in f:
            if s.strip():
                ki.update(json.loads(s)['versek'])
    return ki


def vers_nezet(obj):
    """Egy modell-válasz (kapun átment objektum) szabványos nézete.

    Visszaad: (parok {hu: frozenset(er)}, betoldas frozenset, forditatlan frozenset).
    A `parok` listában ugyanaz a magyar sorszám többször is szerepelhet: az eredetik egyesülnek.
    """
    parok = {}
    for hu, ers in obj['parok']:
        parok.setdefault(hu, set()).update(ers)
    return ({h: frozenset(e) for h, e in parok.items()}, frozenset(obj['betoldas']), frozenset(obj['forditatlan']))


def partnerek_hu(nezet):
    return nezet[0]


def partnerek_er(nezet):
    """{er: frozenset(hu)} a nézet linkjeiből."""
    d = {}
    for hu, ers in nezet[0].items():
        for e in ers:
            d.setdefault(e, set()).add(hu)
    return {e: frozenset(h) for e, h in d.items()}


def egyesit_vers(ig, s, c, karoli_tokenek, eredeti, kezi_hu=None, extra_er=None):
    """Egy vers sorai. s, c: a modell objektuma vagy None (kapuhibás/hiányzó).

    Visszaad: (parok_sorok, szavak_sorok, atnezes_bool)."""
    nk, ne = len(karoli_tokenek), len(eredeti)
    kezi_hu = set(kezi_hu or ())
    extra_er = list(extra_er or [])

    def szur(nezet):
        # a kézi 1:2 beolvasztás Károli-tokenjei nem kapnak linket (a modell válaszából kiszűrve)
        return nezet if not kezi_hu or nezet is None else (
            {h: e for h, e in nezet[0].items() if h not in kezi_hu}, nezet[1] - kezi_hu, nezet[2])
    sn = szur(vers_nezet(s)) if s is not None else None
    cn = szur(vers_nezet(c)) if c is not None else None
    alap = sn if sn is not None else cn
    if alap is None:
        szavak = []
        for i, t in enumerate(karoli_tokenek, 1):
            szavak.append([ig, 'hu', i, t, 'fuggoben', '', '', 'kezi', ''])
        for i, w in enumerate(eredeti, 1):
            szavak.append([ig, 'er', i, w['alak'], 'fuggoben', '', w['strong'], 'kezi', ''])
        for w in extra_er:
            szavak.append([ig, 'er', w['sorsz'], w['alak'], 'fuggoben', '', w['strong'], 'kezi', ''])
        return [], szavak, True
    van_ketto = sn is not None and cn is not None
    vforras = 'S' if sn is not None else 'C'

    def tforras(magas):
        return 'S+C' if magas else vforras

    a_hu = partnerek_hu(alap)
    a_er = partnerek_er(alap)
    c_hu = partnerek_hu(cn) if van_ketto else None
    c_er = partnerek_er(cn) if van_ketto else None
    parok = []
    for hu in sorted(a_hu):
        for er in sorted(a_hu[hu]):
            magas = van_ketto and er in c_hu.get(hu, frozenset())
            parok.append([ig, hu, karoli_tokenek[hu - 1], er, eredeti[er - 1]['alak'], eredeti[er - 1]['strong'],
                          'magas' if magas else 'alacsony', tforras(magas)])
    szavak = []
    for i, t in enumerate(karoli_tokenek, 1):
        if i in kezi_hu:
            szavak.append([ig, 'hu', i, t, 'fuggoben', '', '', 'kezi', ''])
            continue
        if i in a_hu:
            allapot, partner = 'parositva', sorted(a_hu[i])
            strongok = []
            for e in partner:
                if eredeti[e - 1]['strong'] not in strongok:
                    strongok.append(eredeti[e - 1]['strong'])
            strong = '+'.join(strongok)
            magas = van_ketto and c_hu.get(i) == a_hu[i]
        else:
            allapot, partner, strong = 'betoldas', [], ''
            magas = van_ketto and (i in cn[1])
        szavak.append([ig, 'hu', i, t, allapot, ','.join(str(x) for x in partner), strong,
                       'magas' if magas else 'alacsony', tforras(magas)])
    for e, w in enumerate(eredeti, 1):
        if e in a_er:
            allapot, partner = 'parositva', sorted(a_er[e])
            magas = van_ketto and c_er.get(e) == a_er[e]
        else:
            allapot, partner = 'forditatlan', []
            magas = van_ketto and (e not in c_er)
        szavak.append([ig, 'er', e, w['alak'], allapot, ','.join(str(x) for x in partner), w['strong'],
                       'magas' if magas else 'alacsony', tforras(magas)])
    for w in extra_er:
        szavak.append([ig, 'er', w['sorsz'], w['alak'], 'fuggoben', '', w['strong'], 'kezi', ''])
    return parok, szavak, False


def kezi_felulir(konyv, gyoker=None):
    """{igehely: ok} az `f22/kezi_versek_<könyv>.tsv`-ből (fejléc: igehely, ok): azok a Károli-versek, amelyeket a
    modell-válaszoktól függetlenül `kezi` állapotba kell tenni, mert a Károli-kulcs szerinti TAHOT-vers nem a
    megfelelő (versszámozás-eltolódás). A fájl hiánya üres halmaz (az 1Móz kimenete így nem változik)."""
    ut = utak(konyv, gyoker)['kezi_versek']
    if not os.path.exists(ut):
        return {}
    ki = {}
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    for s in sorok[1:]:
        r = s.split('\t')
        ki[r[0]] = r[1] if len(r) > 1 else ''
    return ki


def minta_sorok(u):
    """A fő minta és (ha van) a javító menet mintája, igehely szerint egyszer."""
    sorok = sonnet_koteg.minta_olvas(u['minta'])
    if os.path.exists(u['minta_javito']):
        van = {s['igehely'] for s in sorok}
        sorok += [s for s in sonnet_koteg.minta_olvas(u['minta_javito']) if s['igehely'] not in van]
    return sorok


def modell_versek(u, kulcs):
    """A modell (`sonnet` | `c`) versenkénti válaszai: a fő menet, felülírva a javító menettel."""
    ki = jsonl_versek(u[kulcs])
    ki.update(jsonl_versek(u[kulcs + '_javito']))
    return ki


def sorrend_igehelyek(minta, kimaradt, karoli):
    """A minta versei és az eredeti nélküli (modellhez nem küldött) versek a Károli-tábla sorrendjében."""
    van = {sor['igehely'] for sor in minta} | set(kimaradt)
    return [ig for ig in karoli if ig in van]


def epit(konyv, gyoker=None, karoli=None, ered=None):
    """A két tábla és az átnézési sor tartalma memóriában: (parok, szavak, atnezes) sorlisták."""
    u = utak(konyv, gyoker)
    if not os.path.exists(u['minta']) or not os.path.exists(u['sonnet']):
        raise SystemExit('hiányzó bemenet: %s' % ', '.join(k for k in ('minta', 'sonnet') if not os.path.exists(u[k])))
    # a C-fájl hiánya: csak-Sonnet könyv (DT-F22c); ilyenkor minden link `alacsony`, `forras: S` (a brief szerint)
    karoli = karoli if karoli is not None else tokenek.betolt_karoli()
    ered = ered if ered is not None else tokenek.betolt_eredeti()
    minta = minta_sorok(u)
    sv, cv = modell_versek(u, 'sonnet'), modell_versek(u, 'c')
    parok, szavak, atnezes = [], [], []
    kimaradt = set(sonnet_koteg.eredeti_nelkuli_versek(konyv, karoli, ered))
    felul = kezi_felulir(konyv, gyoker)
    osszevon = {o['karoli']: o for o in tokenek.versosszevonasok() if tokenek.igehely_bont(o['karoli'])[0] == konyv}
    extra = tokenek.osszevont_extra()
    for ig in sorrend_igehelyek(minta, kimaradt, karoli):
        if ig in felul and ig not in kimaradt:
            p, sz, kezi = egyesit_vers(ig, None, None, tokenek.tokenizal(karoli[ig]), ered[ig])
            szavak += sz
            atnezes.append([ig, felul[ig], felul[ig]])
            continue
        if ig in kimaradt:
            p, sz, kezi = egyesit_vers(ig, None, None, tokenek.tokenizal(karoli[ig]), [])
            szavak += sz
            atnezes.append([ig, 'nincs eredeti vers a TAHOT-ban (versszámozás-eltérés)', 'nincs eredeti vers a TAHOT-ban (versszámozás-eltérés)'])
            continue
        s = sv.get(ig, {}).get('obj') if sv.get(ig, {}).get('allapot') == 'ok' else None
        c = cv.get(ig, {}).get('obj') if cv.get(ig, {}).get('allapot') == 'ok' else None
        o = osszevon.get(ig)
        p, sz, kezi = egyesit_vers(ig, s, c, tokenek.tokenizal(karoli[ig]), ered[ig],
                                   kezi_hu=range(o['hu_tol'], o['hu_ig'] + 1) if o else None,
                                   extra_er=extra.get(ig) if o else None)
        parok += p
        szavak += sz
        if o:
            atnezes.append([ig, 'hu %d–%d és a TAHOT %s: %s' % (o['hu_tol'], o['hu_ig'], o['eredeti'], o['megj']),
                            'kezi (kézi 1:2 beolvasztás)'])
        if kezi:
            atnezes.append([ig, '; '.join(sv.get(ig, {}).get('hibak', ['nincs válasz'])) or 'nincs válasz',
                            '; '.join(cv.get(ig, {}).get('hibak', ['nincs válasz'])) or 'nincs válasz'])
    for ig in sonnet_koteg.karoli_nelkuli_eredeti_versek(konyv, karoli, ered):
        p, sz, kezi = egyesit_vers(ig, None, None, [], ered[ig])
        szavak += sz
        atnezes.append([ig, 'nincs Károli-vers a Károli-kulcs szerint', 'nincs Károli-vers a Károli-kulcs szerint'])
    return parok, szavak, atnezes


def bemeneti_ts(konyv, gyoker=None):
    """A proveniencia `ts` mezője: a C futásnapló utolsó (adott könyvre vonatkozó) időbélyege, tehát a
    bemenetekből származik, és az újraépítés bájtra azonos marad; ha nincs napló: `manual`."""
    ut = os.path.join(gyoker or ROOT, 'f22', 'futasnaplo.tsv')
    if not os.path.exists(ut):
        return 'manual'
    nevek = ('c/%s' % sonnet_koteg.ascii_nev(konyv), 'c/%s_javito' % sonnet_koteg.ascii_nev(konyv))
    ts = None
    with open(ut, encoding='utf-8') as f:
        sorok = [x.rstrip('\n').rstrip('\r').split('\t') for x in f if x.strip()]
    if not sorok:
        return 'manual'
    fej = sorok[0]
    for r in sorok[1:]:
        d = dict(zip(fej, r))
        if d.get('futas') in nevek and (ts is None or d['ts'] > ts):
            ts = d['ts']
    return ts or 'manual'


def _kezi_sorok():
    """A kézi versmegfeleltetés-javítások nyers sorai (karoli, eredeti, tipus)."""
    with open(tokenek.VERSMEGF_KEZI, encoding='utf-8') as f:
        return [tuple((x.rstrip('\n').rstrip('\r').split('\t') + ['', '', ''])[:3]) for x in f if x.strip() and not x.startswith('#')][1:]


def api_futas(konyv, gyoker=None):
    """Az éles jsonl modell-mezője szerint API-futás volt-e (alapból subagentes)."""
    f = utak(konyv, gyoker)['sonnet']
    if not os.path.exists(f):
        return False
    with open(f, encoding='utf-8') as h:
        elso = h.readline()
    return '(API' in elso


def proveniencia_sor(konyv, gyoker=None):
    """A táblák első sora (SEMA 1.5/2.20): `#`-kezdetű, az olvasók átugorják; scope=manual, mert a tábla
    modell-kimenet (javaslat), nem `lekerdez.py`-eredmény."""
    n = sonnet_koteg.ascii_nev(konyv)
    u = utak(konyv, gyoker)
    csak_sonnet = not os.path.exists(u['c'])
    forras = ['f22/valaszok/sonnet/%s.jsonl' % n] + ([] if csak_sonnet else ['f22/valaszok/c/%s.jsonl' % n])
    if os.path.exists(u['sonnet_javito']) or os.path.exists(u['c_javito']):
        forras += ['f22/valaszok/sonnet/%s_javito.jsonl' % n, 'f22/valaszok/c/%s_javito.jsonl' % n]
    if any(tokenek.igehely_bont(r[0] or r[1])[0] == konyv for r in tokenek.versmegfeleltetes()):
        forras.append('f22/versmegfeleltetes.tsv')
    if os.path.exists(tokenek.VERSMEGF_KEZI) and any(
            tokenek.igehely_bont(r[0] or r[1])[0] == konyv for r in _kezi_sorok()):
        forras.append('f22/versmegfeleltetes_kezi.tsv')
    if any(tokenek.igehely_bont(o['karoli'])[0] == konyv for o in tokenek.versosszevonasok()):
        forras.append('f22/versosszevonas.tsv')
    forras += ['konkordancia/TAHOT_kivonat.tsv', 'konkordancia/Karoli_1908.tsv']
    if csak_sonnet:
        return ('# proveniencia: scope=manual | forras=%s | ts=manual (csak Sonnet, DT-F22c: nincs C futásnapló; '
                '%s-futásnak nincs lekérdezés-időbélyege) | modell-kimenet, javaslat: nem lekérdezés-eredmény; minden link '
                '`alacsony` (egy modell, nincs egyezés); a strong a TAHOT-ból, modell nem írja | előállítás: '
                'eszkozok/karoli_strong/egyesit.py' % (', '.join(forras), 'az API (Batch)' if api_futas(konyv, gyoker) else 'a subagent'))
    return ('# proveniencia: scope=manual | forras=%s | ts=%s (a C futásnapló utolsó hívása%s; az újraépítés '
            'így bájtra azonos) | modell-kimenet, javaslat: nem lekérdezés-eredmény; a bizonyossag '
            'nem "ellenőrizve"; a strong a TAHOT-ból, modell nem írja | előállítás: eszkozok/karoli_strong/egyesit.py'
            % (', '.join(forras), bemeneti_ts(konyv, gyoker),
               ', a javító menetét is beleértve' if len(forras) > 4 else ''))


def tsv_szoveg(fej, sorok, elso_sor=None):
    for s in sorok:
        for x in s:
            if '\t' in str(x) or '\n' in str(x):
                raise SystemExit('tab/újsor egy mezőben: %r' % (s,))
    elol = [elso_sor] if elso_sor else []
    return '\n'.join(elol + ['\t'.join(fej)] + ['\t'.join(str(x) for x in s) for s in sorok]) + '\n'


def ir(konyv, gyoker=None):
    u = utak(konyv, gyoker)
    parok, szavak, atnezes = epit(konyv, gyoker)
    prov = proveniencia_sor(konyv, gyoker)
    for kulcs, fej, sorok, elso in (('parok', PAROK_FEJ, parok, prov), ('szavak', SZAVAK_FEJ, szavak, prov),
                                    ('atnezes', ATNEZES_FEJ, atnezes, None)):
        os.makedirs(os.path.dirname(u[kulcs]), exist_ok=True)
        with open(u[kulcs], 'w', encoding='utf-8', newline='\n') as f:
            f.write(tsv_szoveg(fej, sorok, elso))
    return parok, szavak, atnezes


def olvas(ut):
    """TSV beolvasása a `#`-kezdetű (proveniencia-) sorok átugrásával; csak split('\t')."""
    with open(ut, encoding='utf-8') as f:
        sorok = [x.rstrip('\n').rstrip('\r') for x in f if not x.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, x.split('\t'))) for x in sorok[1:] if x.strip()]


def ellenoriz(konyv, gyoker=None, karoli=None, ered=None):
    """Lefedettségi és Strong-levezethetőségi ellenőrzés a MEGLÉVŐ táblákon; hibaüzenetek listája."""
    u = utak(konyv, gyoker)
    karoli = karoli if karoli is not None else tokenek.betolt_karoli()
    ered = ered if ered is not None else tokenek.betolt_eredeti()
    minta = minta_sorok(u)
    parok, szavak = olvas(u['parok']), olvas(u['szavak'])
    hibak = []
    var = {}
    extra = tokenek.osszevont_extra()
    teljes = lambda ig: ered.get(ig, []) + extra.get(ig, [])   # noqa: E731
    for ig in sorrend_igehelyek(minta, sonnet_koteg.eredeti_nelkuli_versek(konyv, karoli, ered), karoli):
        for i in range(1, len(tokenek.tokenizal(karoli[ig])) + 1):
            var[(ig, 'hu', i)] = 0
        for e in range(1, len(teljes(ig)) + 1):
            var[(ig, 'er', e)] = 0
    for ig in sonnet_koteg.karoli_nelkuli_eredeti_versek(konyv, karoli, ered):
        for e in range(1, len(ered[ig]) + 1):
            var[(ig, 'er', e)] = 0
    for r in szavak:
        k = (r['vers'], r['oldal'], int(r['sorszam']))
        if k not in var:
            hibak.append('a szavak táblában ismeretlen token: %s' % (k,))
            continue
        var[k] += 1
        if r['oldal'] == 'er' and r['strong'] != teljes(r['vers'])[int(r['sorszam']) - 1]['strong']:
            hibak.append('szavak: a strong nem a TAHOT-é: %s' % (k,))
        if r['oldal'] == 'hu':
            tl = tokenek.tokenizal(karoli[r['vers']])
            if r['szo'] != tl[int(r['sorszam']) - 1]:
                hibak.append('szavak: a Károli-szó eltér a tokenizálástól: %s' % (k,))
            if r['partner_sorszam']:
                lk = [ered[r['vers']][int(x) - 1]['strong'] for x in r['partner_sorszam'].split(',')]
                ut = []
                for s in lk:
                    if s not in ut:
                        ut.append(s)
                if '+'.join(ut) != r['strong']:
                    hibak.append('szavak: a hu strong nem a partnerekből vezethető le: %s' % (k,))
    for k, db in var.items():
        if db != 1:
            hibak.append('a token %s %d-szer szerepel a szavak táblában (1 kell)' % (k, db))
    for r in parok:
        ig, e, h = r['vers'], int(r['er_sorszam']), int(r['hu_sorszam'])
        if ig not in ered or not 1 <= e <= len(ered[ig]):
            hibak.append('parok: nem létező eredeti token: %s' % (r,))
            continue
        w = ered[ig][e - 1]
        if r['strong'] != w['strong'] or r['er_szo'] != w['alak']:
            hibak.append('parok: a strong/er_szo nem a TAHOT-é: %s %d' % (ig, e))
        if r['hu_szo'] != tokenek.tokenizal(karoli[ig])[h - 1]:
            hibak.append('parok: a hu_szo eltér a tokenizálástól: %s %d' % (ig, h))
        if r['bizonyossag'] not in ('magas', 'alacsony') or r['forras'] not in ('S+C', 'S', 'C'):
            hibak.append('parok: érvénytelen bizonyossag/forras: %s' % (r,))
    return hibak


def onteszt():
    hibak = []
    eredeti = [{'sorsz': 1, 'strong': 'H9003', 'alak': 'בְּ', 'tukor': 'in', 'nem_tr': False},
               {'sorsz': 2, 'strong': 'H7225', 'alak': 'רֵאשִׁית', 'tukor': 'first', 'nem_tr': False},
               {'sorsz': 3, 'strong': 'H0430', 'alak': 'אֱלֹהִים', 'tukor': 'God', 'nem_tr': False}]
    kt = ['Kezdetben', 'Isten', 'az']
    s = {'vers': 'X 1:1', 'parok': [[1, [1, 2]], [2, [3]]], 'betoldas': [3], 'forditatlan': []}
    c1 = {'vers': 'X 1:1', 'parok': [[1, [1, 2]], [2, [3]]], 'betoldas': [3], 'forditatlan': []}
    c2 = {'vers': 'X 1:1', 'parok': [[1, [1]], [2, [3]]], 'betoldas': [3], 'forditatlan': [2]}
    p, sz, kezi = egyesit_vers('X 1:1', s, c1, kt, eredeti)
    if kezi or any(r[6] != 'magas' or r[7] != 'S+C' for r in p) or any(r[7] != 'magas' for r in sz):
        hibak.append('egyező modellek nem mind magas')
    p, sz, kezi = egyesit_vers('X 1:1', s, c2, kt, eredeti)
    if [r[6] for r in p] != ['magas', 'alacsony', 'magas'] or [r[7] for r in p] != ['S+C', 'S', 'S+C']:
        hibak.append('link-szintű bizonyosság eltérésnél: %s' % ([r[6:] for r in p],))
    ek = {(r[1], r[2]): r[7] for r in sz}
    if ek[('hu', 1)] != 'alacsony' or ek[('er', 2)] != 'alacsony' or ek[('hu', 2)] != 'magas' or ek[('er', 3)] != 'magas':
        hibak.append('token-szintű bizonyosság eltérésnél: %s' % ek)
    p, sz, kezi = egyesit_vers('X 1:1', s, None, kt, eredeti)
    if kezi or any(r[6] != 'alacsony' or r[7] != 'S' for r in p):
        hibak.append('csak Sonnet: alacsony/S kell')
    p, sz, kezi = egyesit_vers('X 1:1', None, c1, kt, eredeti)
    if any(r[7] != 'C' for r in p):
        hibak.append('csak C: forras C kell')
    p, sz, kezi = egyesit_vers('X 1:1', None, None, kt, eredeti)
    if p or not kezi or any(r[7] != 'kezi' or r[4] != 'fuggoben' for r in sz) or len(sz) != 6:
        hibak.append('mindkettő kapuhibás: kezi/fuggoben, link nélkül kell')
    # a Strong a TAHOT-ból jön, nem a modellből: az er_szo/strong a eredeti-ből
    p, sz, kezi = egyesit_vers('X 1:1', s, c1, kt, eredeti)
    if [r[5] for r in p] != ['H9003', 'H7225', 'H0430']:
        hibak.append('strong nem a TAHOT-ból')
    # teljes folyamat (két futás bájtra azonos) a valódi 1Móz 1:1–3 adaton, ideiglenes gyökérben
    tmp = tempfile.mkdtemp()
    karoli = tokenek.betolt_karoli()
    ered = tokenek.betolt_eredeti()
    versek = [x for x in karoli if x.startswith('1Móz 1:')][:3]
    u = utak('1Móz', tmp)
    sonnet_koteg.minta_ir(u['minta'], [dict(s_, sorsz=i) for i, s_ in enumerate(
        [x for x in sonnet_koteg.minta_epit('1Móz', karoli, ered) if x['igehely'] in versek], 1)])

    def modell_sor(valtozat):
        sor = {'igehelyek': versek, 'versek': {}}
        for ig in versek:
            nk, ne = len(tokenek.tokenizal(karoli[ig])), len(ered[ig])
            parok = [[k, [min(k, ne)]] for k in range(1, nk + 1)]
            if valtozat and ne >= 2:
                parok[0] = [1, [2]]
            fedett = {e for p_ in parok for e in p_[1]}
            sor['versek'][ig] = {'allapot': 'ok', 'probalkozas': 1, 'hibak': [], 'obj': {
                'vers': ig, 'parok': parok, 'betoldas': [], 'forditatlan': sorted(set(range(1, ne + 1)) - fedett)}}
        return sor
    for kulcs, val in (('sonnet', False), ('c', True)):
        os.makedirs(os.path.dirname(u[kulcs]), exist_ok=True)
        with open(u[kulcs], 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(modell_sor(val), ensure_ascii=False) + '\n')
    ir('1Móz', tmp)
    h1 = [hashlib.sha256(open(u[k], 'rb').read()).hexdigest() for k in ('parok', 'szavak', 'atnezes')]
    ir('1Móz', tmp)
    h2 = [hashlib.sha256(open(u[k], 'rb').read()).hexdigest() for k in ('parok', 'szavak', 'atnezes')]
    if h1 != h2:
        hibak.append('az újraépítés nem bájtra azonos (K7)')
    hk = ellenoriz('1Móz', tmp, karoli, ered)
    if hk:
        hibak.append('ellenőrzés a teszt-táblán: %s' % hk[:3])
    # az ellenőrzés elkap egy rontott strong-ot
    with open(u['parok'], encoding='utf-8') as f:
        sz = f.read()
    with open(u['parok'], 'w', encoding='utf-8', newline='\n') as f:
        f.write(sz.replace('\tH7225\t', '\tH9999\t', 1))
    if not ellenoriz('1Móz', tmp, karoli, ered):
        hibak.append('az ellenőrzés nem vette észre a rontott strong-ot')
    for h in hibak:
        print('ÖNTESZT HIBA: ' + h, file=sys.stderr)
    print('önteszt: %s' % ('HIBA' if hibak else 'rendben'))
    return 1 if hibak else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--konyv', default=None, help='magyar rövidítés, pl. 1Móz (nincs alapérték)')
    ap.add_argument('--ellenoriz', action='store_true', help='a meglévő táblák lefedettségi és Strong-ellenőrzése, írás nélkül')
    ap.add_argument('--onteszt', action='store_true')
    a = ap.parse_args(argv)
    if a.onteszt:
        return onteszt()
    if not a.konyv:
        print('HIBA: --konyv kell (nincs alapérték)', file=sys.stderr)
        return 2
    if a.ellenoriz:
        hk = ellenoriz(a.konyv)
        print('ellenőrzés: %s' % ('%d hiba' % len(hk) if hk else 'rendben'))
        for x in hk[:30]:
            print('  ' + x)
        return 1 if hk else 0
    parok, szavak, atnezes = ir(a.konyv)
    kisz = {}
    for r in parok:
        kisz[r[6]] = kisz.get(r[6], 0) + 1
    ksz = {}
    for r in szavak:
        ksz[r[7]] = ksz.get(r[7], 0) + 1
    print('parok: %d sor %s; szavak: %d sor %s; átnézési sor: %d vers'
          % (len(parok), dict(sorted(kisz.items())), len(szavak), dict(sorted(ksz.items())), len(atnezes)))
    hk = ellenoriz(a.konyv)
    print('ellenőrzés: %s' % ('%d hiba' % len(hk) if hk else 'rendben'))
    for x in hk[:30]:
        print('  ' + x)
    return 1 if hk else 0


if __name__ == '__main__':
    sys.exit(main())
