#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F21.47 / F21.70 — a kalibráló trigger (SONNETV3, koteg_max=1) utáni gépi ellenőrzés. Nincs API-hívás.

A repóban lévő f21p/futasnaplo.tsv-ből, f21p/valaszok/SONNETV3.jsonl-ből és (ha van)
f21p/valaszok/SONNETV3.hibak.jsonl-ből deterministikusan megmondja:

  (a) elutasította-e a modell a kérést ÉS a gondolkodási lánc minden lépése elutasított-e
      (F21.70: a Sonnet gondolkodása MINIMÁLIS szinten fut; futtat.S_REASONING_LANC:
      reasoning.max_tokens=1024 -> reasoning.effort=low). Bizonyíték: (i) a hibak.jsonl-ben
      (futtat.hiba_ment) 4xx HTTP-kód (429 és 408 kivételével), `lanc_tovabb` jelzés NÉLKÜL — a
      köteg hívása a lánc végén is hibára futott, köteg-sor/napló nem készült; (ii) a köteg-sor
      hivasok[].hiba mezője (a 200-as válasz hibatestje, futtat.hivas). A `lanc_tovabb=true` sor a
      lánc egy elutasított, de a következő lépéssel folytatott lépése: NEM megállási ok, csak
      naplózott "lánc: tovább" jelzés (a kilépési kód ilyenkor is lehet 0). A hibaüzenet kulcsszavai
      (reasoning, temperature) megnevezik, melyik paraméter. A mért gondolkodási tokent (napló
      gondolkodas_token, jsonl hivasok[].usage) külön kiírja; ha a hívásonkénti mért gondolkodási token
      meghaladja a konfigurált max_tokens keretet (gondolkodas_mod: reasoning_max_tokens=N), FIGYELMEZTETÉST
      ad (F21.75: pl. 5109 > 1024; a modell a keretet nem tartja be) — NEM megállási ok.
      F21.75: az elutasítás-ág (hibak.jsonl) csak a legutóbbi SIKERES köteg (a SONNETV3 legutóbbi naplósora)
      UTÁNI hívási hibákat számítja; a korábbi hibasorok (ts < a legutóbbi sikeres köteg ts-e: egy előző,
      kikapcsolt-gondolkodású kísérlet 400-asa) "korábbi, a sikeres köteg előtti: nem számít" jelzést kapnak.
  (b) a mért köteg-költség és a vetített kumulatív összeg:
        vetített = napló összege (az F3V3 kész + a kalibráló köteg; minden futás) +
                   hátralévő köteg × átlagos mért köteg-költség × újrakérési szorzó,
      ahol az átlagos mért köteg-költség a SONNETV3 első próbálkozású hívásainak költsége
      kötegenként átlagolva, az újrakérési szorzó M = Σcost / Σcost(első próba) a kalibráló
      kötegek saját mért adatából, ha volt újrakérés; ha nem volt, konzervatív 1.3.
      A küszöb-összehasonlítás (felhasználói döntés) erre a mért vetítésre vonatkozik.
      Tájékoztatóul: a köteg-költség felső becslése a Sonnet saját mért legnagyobb
      bemeneti és kimeneti tokenjéből (max token × ár; futtat.ARAK), és az ebből vetített összeg.

Kilépési kód: 0 = mehet tovább; 4 = megállni (a lánc minden lépését elutasította, vagy a
vetített kumulatív összeg > küszöb [4.90]); 2 = adathiba (hiányzó/üres bemenet, nincs mért
köteg és nincs elutasítás-bizonyíték). A kimenet olvasható, a végén a DÖNTÉS sorral; a fejléc
proveniencia-sor (scope | forras | ts).

    python eszkozok/karoli_strong/kalibralas_ellenoriz.py [--forras-dir <könyvtár>] [--kuszob 4.90] [--onteszt]
"""

import argparse
import json
import os
import re
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import futtat  # noqa: E402
import tokenek  # noqa: E402

FUTAS = 'SONNETV3'
KUSZOB = futtat.P3C_FELHASZNALOI_PLAFON       # 4.90 (plafon_usd)
KEMENY = futtat.PLAFON_USD                    # 5.0
KONZERVATIV_M = 1.3
KOD_RENDBEN, KOD_ADATHIBA, KOD_MEGALLNI = 0, 2, 4
PARAMETER = re.compile(r'reasoning|temperature', re.IGNORECASE)


def _olvas_tsv(ut):
    with open(ut, encoding='utf-8') as f:
        sorok = [s.rstrip('\n').rstrip('\r') for s in f if s.strip() and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def _jsonl(ut):
    if not os.path.exists(ut):
        return []
    with open(ut, encoding='utf-8') as f:
        return [json.loads(s) for s in f if s.strip()]


def ellenoriz(forras_dir=None, kuszob=KUSZOB, futas=FUTAS, minta=None):
    """Visszaad: dict ('kod', 'sorok' (olvasható sorok), 'elutasitva', 'vetitett', ...)."""
    forras_dir = forras_dir or futtat.F21P
    ki = {'kod': KOD_RENDBEN, 'sorok': [], 'elutasitva': False, 'vetitett': None, 'kuszob': kuszob, 'okok': [], 'figyelmeztetesek': [], 'lanc': []}
    s = ki['sorok']
    naplo_ut = futtat.naplo_ut(forras_dir)
    if not os.path.exists(naplo_ut):
        ki['kod'] = KOD_ADATHIBA
        s.append('ADATHIBA: nincs futásnapló: %s' % naplo_ut)
        return ki
    try:
        naplo = _olvas_tsv(naplo_ut)
        sorok_j = futtat.koteg_sorok(futas, forras_dir)
        hibak = _jsonl(futtat.hibak_ut(futas, forras_dir))
        minta = minta or futtat.minta_betolt()
        osszes_koteg = len(futtat.bemenet.kotegek(futtat.verslista(futas, minta, forras_dir), futtat.KOTEG_MERET))
    except (OSError, ValueError, KeyError, IndexError) as e:
        ki['kod'] = KOD_ADATHIBA
        s.append('ADATHIBA: a bemenet nem olvasható: %s' % e)
        return ki
    nr = [r for r in naplo if r['futas'] == futas]
    s.append('# scope=kalibráló ellenőrzés (%s, koteg_max=1) | forras=%s, %s%s | ts=%s' % (
        futas, os.path.join('f21p', 'futasnaplo.tsv') if forras_dir == futtat.F21P else naplo_ut,
        'valaszok/%s.jsonl' % futas, ', valaszok/%s.hibak.jsonl' % futas if hibak else '', tokenek.generalas_ts()))
    s.append('%s: %d mért köteg-sor, %d naplósor, %d rögzített hívás-hiba; a futás %d kötegű' % (
        futas, len(sorok_j), len(nr), len(hibak), osszes_koteg))

    # --- (a) elutasította-e a kérést (a gondolkodási lánc minden lépése) ------------------------------
    elutasitas, lanc, korabbi = [], [], []
    utolso_sikeres_ts = max((r['ts'] for r in nr), default=None)   # F21.75: a legutóbbi sikeres köteg (naplósor) ts-e
    for h in hibak:
        kod_ = h.get('http_hibakod')
        if utolso_sikeres_ts and str(h.get('ts', '')) < utolso_sikeres_ts:
            korabbi.append('HTTP %s a(z) %s. kötegnél (ts %s) — korábbi, a sikeres köteg előtti (%s): nem számít' % (
                kod_, h.get('koteg'), h.get('ts'), utolso_sikeres_ts))
            continue
        if h.get('lanc_tovabb'):
            lanc.append('%s. kötegnél a(z) %s lépés elutasítva (HTTP %s), lánc: tovább' % (
                h.get('koteg'), h.get('gondolkodas_mod', '?'), kod_))
            continue
        if kod_ is not None and 400 <= kod_ < 500 and kod_ not in (408, 429):
            par = sorted({m.lower() for m in PARAMETER.findall(h.get('hibauzenet', ''))})
            elutasitas.append('HTTP %d a(z) %s. kötegnél%s: %s' % (kod_, h.get('koteg'), ' (a hibaüzenet említi: %s)' % ', '.join(par) if par else '',
                                                               h.get('hibauzenet', '')[:200]))
    for sor in sorok_j:
        for hv in sor.get('hivasok', []):
            if hv.get('hiba'):
                par = sorted({m.lower() for m in PARAMETER.findall(hv['hiba'])})
                elutasitas.append('hibatest a 200-as válaszban (köteg %s, %s. próba)%s: %s' % (
                    sor.get('koteg'), hv.get('probalkozas'), ' (említi: %s)' % ', '.join(par) if par else '', hv['hiba'][:200]))
    ki['lanc'] = lanc
    ki['korabbi_hibak'] = korabbi
    for x in korabbi:
        s.append('(a) ' + x)
    for x in lanc:
        s.append('(a) ' + x)
    if elutasitas:
        ki['elutasitva'] = True
        ki['okok'].append('a modell elutasította a kérést%s' % (
            ' (a gondolkodási lánc minden lépése elutasítva: %d lépés tovább, majd a végső elutasítás)' % len(lanc) if lanc else ''))
        s.append('(a) ELUTASÍTÁS: igen')
        for x in elutasitas:
            s.append('    - ' + x)
    elif lanc:
        s.append('(a) elutasítás: nincs végleges (a lánc %d elutasított lépés után folytatódott: lánc: tovább)' % len(lanc))
    else:
        s.append('(a) elutasítás: nincs (se 4xx hibakód, se hibatest a válaszban)')
    mod = {r['gondolkodas_mod'] for r in nr}
    gond = sum(int(r['gondolkodas_token']) for r in nr)
    gond_usage = sum(futtat.gondolkodas_token(hv.get('usage') or {}) for sor in sorok_j for hv in sor.get('hivasok', []))
    rsz = sum(hv.get('reasoning_szoveg_karakter', 0) or 0 for sor in sorok_j for hv in sor.get('hivasok', []))
    ki['gondolkodas_token'] = gond
    ki['gondolkodas_token_usage'] = gond_usage
    if nr:
        s.append('    gondolkodas_mod a naplóban: %s; mért gondolkodási token: %d (napló), %d (jsonl usage); reasoning-szöveg: %d karakter' % (
            ', '.join(sorted(mod)), gond, gond_usage, rsz))
        s.append('    (a gondolkodás be van kapcsolva minimális szinten: a mért gondolkodási token a mért költségben benne van)')
        # F21.75: keret-túllépés — figyelmeztetés, NEM megállási ok
        keret = [int(m_.group(1)) for m_ in (re.search(r'max_tokens=([0-9]+)', r['gondolkodas_mod']) for r in nr) if m_]
        if keret:
            keret_max = max(keret)
            mert_max = max(int(r['gondolkodas_token']) for r in nr)
            mert_usage_max = max((futtat.gondolkodas_token(hv.get('usage') or {}) for sor in sorok_j for hv in sor.get('hivasok', [])), default=0)
            mert_max = max(mert_max, mert_usage_max)
            ki['gondolkodas_keret'] = keret_max
            ki['gondolkodas_mert_max'] = mert_max
            if mert_max > keret_max:
                f_ = ('FIGYELMEZTETÉS (nem megállási ok): a mért gondolkodási token (legnagyobb hívásonként: %d) meghaladja a konfigurált max_tokens keretet '
                      '(%d): a modell a keretet nem tartja be; a költség a mért tokent tartalmazza' % (mert_max, keret_max))
                ki['figyelmeztetesek'].append(f_)
                s.append('    ' + f_)

    # --- adathiány ---------------------------------------------------------------------------------
    if not sorok_j or not nr:
        if ki['elutasitva']:
            ki['kod'] = KOD_MEGALLNI
            s.append('(b) nincs mért köteg (a hívás elutasításra futott): a költség nem vetíthető')
            s.append('DÖNTÉS: MEGÁLLNI (4): %s' % '; '.join(ki['okok']))
            return ki
        ki['kod'] = KOD_ADATHIBA
        s.append('ADATHIBA: nincs mért %s köteg-sor/naplósor, és nincs elutasítás-bizonyíték%s' % (
            futas, ' (hibak.jsonl: %s)' % ', '.join(str(h.get('http_hibakod')) for h in hibak) if hibak else ''))
        s.append('DÖNTÉS: adathiba (2)')
        return ki

    # --- (b) költség és vetítés ---------------------------------------------------------------------
    p1 = [r for r in nr if r['probalkozas'] == '1']
    cost_ossz = sum(float(r['koltseg_usd']) for r in nr)
    cost_p1 = sum(float(r['koltseg_usd']) for r in p1)
    kesz = len(sorok_j)
    hatralevo = max(osszes_koteg - kesz, 0)
    volt_ujrakeres = any(r['probalkozas'] == '2' for r in nr)
    M = cost_ossz / cost_p1 if volt_ujrakeres and cost_p1 else KONZERVATIV_M
    atlag = cost_p1 / kesz
    eddig = futtat.naplo_osszeg(forras_dir)
    vetitett = eddig + hatralevo * atlag * M
    ki['vetitett'] = vetitett
    forrasok = sorted({r['koltseg_forras'] for r in nr})
    ar = futtat.ARAK[futtat.MODELLEK['S']]
    tabla = sum(int(r['bemenet_token']) * ar[0] / 1e6 + int(r['kimenet_token']) * ar[1] / 1e6 for r in nr)
    max_be = max(int(r['bemenet_token']) for r in nr)
    max_ki = max(int(r['kimenet_token']) for r in nr)
    felso = max_be * ar[0] / 1e6 + max_ki * ar[1] / 1e6
    felso_vet = eddig + hatralevo * felso * M
    ki['felso_koteg'] = felso
    ki['felso_vetitett'] = felso_vet
    s.append('(b) mért köteg-költség: %d kész köteg, a %s hívásainak költsége %.6f USD (ebből első próba %.6f); koltseg_forras: %s' % (
        kesz, futas, cost_ossz, cost_p1, ', '.join(forrasok)))
    s.append('    a mért cost / a táblaár (%.2f/%.2f USD/1M, mért tokenekkel): %.4f / %.4f USD' % (ar[0], ar[1], cost_ossz, tabla))
    s.append('    átlagos mért köteg-költség (első próba): %.6f USD; újrakérési szorzó M = %.4f (%s)' % (
        atlag, M, 'a mért adatból, Σcost/Σcost(első próba)' if volt_ujrakeres else 'nem volt újrakérés: konzervatív %.1f' % KONZERVATIV_M))
    s.append('    VETÍTETT KUMULATÍV ÖSSZEG = napló %.6f + %d hátralévő köteg × %.6f × %.4f = %.4f USD (küszöb %.2f, kemény %.1f)' % (
        eddig, hatralevo, atlag, M, vetitett, kuszob, KEMENY))
    s.append('    tájékoztató felső becslés: a legdrágább lehetséges köteg (mért max bemenet %d, max kimenet %d token × ár) = %.6f USD; '
             'ebből vetített kumulatív %.4f USD' % (max_be, max_ki, felso, felso_vet))
    if vetitett > kuszob:
        ki['okok'].append('a mért köteg-költségből vetített kumulatív összeg %.4f USD > %.2f USD küszöb%s' % (
            vetitett, kuszob, ' (és > a %.1f kemény plafon)' % KEMENY if vetitett > KEMENY else ''))
    if ki['okok']:
        ki['kod'] = KOD_MEGALLNI
        s.append('DÖNTÉS: MEGÁLLNI (4): %s' % '; '.join(ki['okok']))
    else:
        s.append('DÖNTÉS: mehet tovább (0): nincs elutasítás, a vetített kumulatív összeg %.4f USD <= %.2f USD küszöb' % (vetitett, kuszob))
    if felso_vet > kuszob and ki['kod'] == KOD_RENDBEN:
        s.append('    megjegyzés: a felső becslés szerinti kumulatív %.4f USD > %.2f, de a küszöb-összehasonlítás a mért költségre vonatkozik' % (felso_vet, kuszob))
    return ki


def onteszt():
    import contextlib
    import io
    import shutil
    import p3c_mock
    hibak = []

    def ellen(f, leiras):
        if not f:
            hibak.append(leiras)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'a régi kimenetek megváltoztak: %s' % p3c_mock.regi_kimenetek_hibak())
    ellen(KUSZOB == 4.9 and KEMENY == 5.0 and (KOD_RENDBEN, KOD_ADATHIBA, KOD_MEGALLNI) == (0, 2, 4), 'a küszöb/kilépési kódok nem a specifikáltak')
    minta = futtat.minta_betolt()
    teszt_kulcs = 'sk-' + 'or-v1-TESZTKULCS0123456789abcdef0123456789'
    mappak = []

    def uj(elotag):
        m = tempfile.mkdtemp(prefix=elotag)
        mappak.append(m)
        return m

    def csendben(fn, *a, **kw):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return fn(*a, **kw)

    def futtat_mock(mappa, kuldo, futasok, koteg_max):
        ctx = futtat.Kontextus(kuldo, teszt_kulcs, mappa)
        for f in futasok:
            csendben(futtat.futas, ctx, f, minta, koteg_max)
        return ctx

    def kezi(mappa):
        """A független számítás: a naplót és a jsonl-t a teszt maga olvassa."""
        sor = _olvas_tsv(os.path.join(mappa, 'futasnaplo.tsv'))
        s = [r for r in sor if r['futas'] == FUTAS]
        c_all = sum(float(r['koltseg_usd']) for r in s)
        c_p1 = sum(float(r['koltseg_usd']) for r in s if r['probalkozas'] == '1')
        kesz = len({r['koteg'] for r in s})
        return {'osszeg': sum(float(r['koltseg_usd']) for r in sor), 'c_all': c_all, 'c_p1': c_p1, 'kesz': kesz,
                'ujra': any(r['probalkozas'] == '2' for r in s), 'max_be': max(int(r['bemenet_token']) for r in s),
                'max_ki': max(int(r['kimenet_token']) for r in s), 'gond': sum(int(r['gondolkodas_token']) for r in s)}
    try:
        # 1. rendben: F3V3 kész + 1 Sonnet-köteg, újrakérés nélkül -> M = 1.3, kód 0
        m1 = uj('f21p_onteszt_kal_ok_')
        futtat_mock(m1, futtat.MockKuldo(), ['F3V3'], None)
        futtat_mock(m1, futtat.MockKuldo(), [FUTAS], 1)
        r1 = csendben(ellenoriz, m1)
        k1 = kezi(m1)
        varhato = k1['osszeg'] + 19 * k1['c_p1'] / k1['kesz'] * 1.3
        ellen(r1['kod'] == 0 and k1['kesz'] == 1 and not k1['ujra'] and abs(r1['vetitett'] - varhato) < 1e-9,
              'rendben-eset: kód %s, vetített %s vs független %s' % (r1['kod'], r1['vetitett'], varhato))
        szoveg1 = '\n'.join(r1['sorok'])
        ellen('DÖNTÉS: mehet tovább (0)' in szoveg1 and 'VETÍTETT KUMULATÍV ÖSSZEG' in szoveg1 and 'küszöb 4.90' in szoveg1
              and szoveg1.startswith('# scope=') and ' | forras=' in szoveg1.split('\n')[0] and ' | ts=' in szoveg1.split('\n')[0],
              'a kimenet nem tartalmazza a vetítést / küszöböt / döntést / proveniencia-sort')
        ar = futtat.ARAK[futtat.MODELLEK['S']]
        ellen(abs(r1['felso_koteg'] - (k1['max_be'] * ar[0] + k1['max_ki'] * ar[1]) / 1e6) < 1e-12 and r1['felso_koteg'] >= k1['c_p1'] * 0 and r1['felso_vetitett'] > 0,
              'a felső köteg-becslés nem a mért max token × ár')
        ellen(not r1['figyelmeztetesek'] and 'mért gondolkodási token: %d (napló), %d (jsonl usage)' % (k1['gond'], k1['gond']) in szoveg1
              and k1['gond'] > 0 and 'reasoning_max_tokens=1024' in szoveg1 and r1['gondolkodas_token'] == k1['gond'],
              'a mért gondolkodási token nincs (külön) kiírva / figyelmeztetés van: %s' % r1['figyelmeztetesek'])
        # 2. újrakérés a kalibráló kötegben: M a mért adatból
        m2 = uj('f21p_onteszt_kal_ujra_')
        futtat_mock(m2, futtat.MockKuldo(), ['F3V3'], None)
        ig0 = futtat.verslista(FUTAS, minta, m2)[2]
        futtat_mock(m2, futtat.MockKuldo(hibas_elso={ig0}), [FUTAS], 1)
        r2 = csendben(ellenoriz, m2)
        k2 = kezi(m2)
        M2 = k2['c_all'] / k2['c_p1']
        ellen(k2['ujra'] and M2 > 1.0 and abs(r2['vetitett'] - (k2['osszeg'] + 19 * k2['c_p1'] / k2['kesz'] * M2)) < 1e-9,
              'újrakérés-eset: a vetítés nem a mért M-et használja (M=%.4f, vetített %s)' % (M2, r2['vetitett']))
        ellen('a mért adatból' in '\n'.join(r2['sorok']), 'az M forrása nincs kiírva')
        # 3. túl drága: a vetített kumulatív összeg > 4.90 -> kód 4, indok
        m3 = uj('f21p_onteszt_kal_draga_')
        futtat_mock(m3, futtat.MockKuldo(), ['F3V3'], None)
        futtat_mock(m3, futtat.MockKuldo(koltseg_szorzo=40.0), [FUTAS], 1)
        r3 = csendben(ellenoriz, m3)
        ellen(r3['kod'] == 4 and not r3['elutasitva'] and r3['vetitett'] > 4.9 and 'küszöb' in '\n'.join(r3['okok']) and 'MEGÁLLNI (4)' in '\n'.join(r3['sorok']),
              'a túl drága eset nem 4-es kód: %s %s' % (r3['kod'], r3['vetitett']))
        # a küszöb paraméter: ugyanaz az adat 100 USD küszöbbel mehet
        r3b = csendben(ellenoriz, m3, 100.0)
        ellen(r3b['kod'] == 0, 'a küszöb-paraméter nem érvényesül')
        # 4. HTTP 400 (hibak.jsonl): elutasítás -> kód 4, a paraméter megnevezve
        m4 = uj('f21p_onteszt_kal_400_')
        futtat_mock(m4, futtat.MockKuldo(), ['F3V3'], None)

        class Elutasit:
            def __init__(self, kod, uzenet):
                self.kod, self.uzenet = kod, uzenet

            def __call__(self, model_id, uzenetek, api_key, extra):
                return futtat._MockValasz({'error': self.uzenet}, status=self.kod)
        futtat_mock(m4, Elutasit(400, 'Unsupported parameter: reasoning.enabled=false'), [FUTAS], 1)
        r4 = csendben(ellenoriz, m4)
        ellen(r4['kod'] == 4 and r4['elutasitva'] and len(r4['lanc']) == 1 and 'reasoning' in '\n'.join(r4['sorok']) and 'HTTP 400' in '\n'.join(r4['sorok'])
              and not os.path.exists(futtat.valasz_ut(FUTAS, m4)), 'a HTTP 400 nem 4-es kód / nincs megnevezve a paraméter: %s' % r4['kod'])
        # 4b. F21.75: régi 400 (a sikeres köteg ELŐTT) + utána sikeres köteg -> NEM elutasítás (kód 0)
        m12 = uj('f21p_onteszt_kal_regi400_')
        futtat_mock(m12, futtat.MockKuldo(), ['F3V3'], None)
        futtat_mock(m12, futtat.MockKuldo(), [FUTAS], 1)
        hut = futtat.hibak_ut(FUTAS, m12)
        os.makedirs(os.path.dirname(hut), exist_ok=True)
        regi = {'ts': '2000-01-01T00:00:00+00:00', 'futas': FUTAS, 'koteg': 1, 'modell': futtat.MODELLEK['S'], 'http_hibakod': 400,
                'hibauzenet': 'Reasoning is mandatory for this endpoint and cannot be disabled.'}
        with open(hut, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(regi) + '\n')
        r12 = csendben(ellenoriz, m12)
        sz12 = '\n'.join(r12['sorok'])
        ellen(r12['kod'] == 0 and not r12['elutasitva'] and len(r12['korabbi_hibak']) == 1
              and 'korábbi, a sikeres köteg előtti' in sz12 and 'nem számít' in sz12 and '(a) ELUTASÍTÁS: igen' not in sz12,
              'a sikeres köteg előtti régi 400 elutasításnak számít: %s %s' % (r12['kod'], sz12[:300]))
        # 4c. sikeres köteg UTÁN új 400 -> elutasítás (kód 4)
        m13 = uj('f21p_onteszt_kal_uj400_')
        futtat_mock(m13, futtat.MockKuldo(), ['F3V3'], None)
        futtat_mock(m13, futtat.MockKuldo(), [FUTAS], 1)
        hut13 = futtat.hibak_ut(FUTAS, m13)
        os.makedirs(os.path.dirname(hut13), exist_ok=True)
        uj_h = dict(regi, ts='2999-01-01T00:00:00+00:00', hibauzenet='Unsupported parameter: temperature')
        with open(hut13, 'w', encoding='utf-8', newline='\n') as f:
            f.write(json.dumps(regi) + '\n' + json.dumps(uj_h) + '\n')
        r13 = csendben(ellenoriz, m13)
        ellen(r13['kod'] == 4 and r13['elutasitva'] and len(r13['korabbi_hibak']) == 1 and 'temperature' in '\n'.join(r13['sorok']),
              'a sikeres köteg utáni új 400 nem elutasítás: %s' % r13['kod'])
        # 4d. gondolkodási keret-túllépés: figyelmeztetés (NEM megállási ok, a kód marad 0)
        m14 = uj('f21p_onteszt_kal_keret_')
        futtat_mock(m14, futtat.MockKuldo(), ['F3V3'], None)
        futtat_mock(m14, futtat.MockKuldo(), [FUTAS], 1)
        ut14 = os.path.join(m14, 'futasnaplo.tsv')
        with open(ut14, encoding='utf-8') as f:
            sorok14 = f.read().split('\n')
        fej14 = sorok14[0].split('\t')
        i_g14, i_f14 = fej14.index('gondolkodas_token'), fej14.index('futas')
        for i, s_ in enumerate(sorok14[1:], 1):
            m_ = s_.split('\t')
            if len(m_) == len(fej14) and m_[i_f14] == FUTAS:
                m_[i_g14] = '5109'
                sorok14[i] = '\t'.join(m_)
        with open(ut14, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok14))
        r14 = csendben(ellenoriz, m14)
        ellen(r14['kod'] == 0 and len(r14['figyelmeztetesek']) == 1 and 'FIGYELMEZTETÉS' in '\n'.join(r14['sorok'])
              and '5109' in r14['figyelmeztetesek'][0] and '(1024)' in r14['figyelmeztetesek'][0] and 'nem megállási ok' in r14['figyelmeztetesek'][0],
              'a keret-túllépés (5109 > 1024) nincs figyelmeztetésként kiírva / megállít: %s %s' % (r14['kod'], r14['figyelmeztetesek']))
        # 5. 200-as hibatest (temperature) a köteg-sorban -> kód 4
        m5 = uj('f21p_onteszt_kal_hibatest_')
        futtat_mock(m5, futtat.MockKuldo(), ['F3V3'], None)

        class Hibatest:
            def __call__(self, model_id, uzenetek, api_key, extra):
                return futtat._MockValasz({'error': {'code': 400, 'message': 'temperature is not supported'}})
        futtat_mock(m5, Hibatest(), [FUTAS], 1)
        r5 = csendben(ellenoriz, m5)
        ellen(r5['kod'] == 4 and r5['elutasitva'] and 'temperature' in '\n'.join(r5['sorok']), 'a 200-as hibatest nem 4-es kód: %s' % r5['kod'])
        # 6. 503 (nem elutasítás) mért köteg nélkül -> adathiba (2); 429 sem elutasítás
        m6 = uj('f21p_onteszt_kal_503_')
        futtat_mock(m6, futtat.MockKuldo(), ['F3V3'], None)
        ctx6 = futtat.Kontextus(Elutasit(503, 'overloaded'), teszt_kulcs, m6, alvas=lambda s_: None)
        csendben(futtat.futas, ctx6, FUTAS, minta, 1)
        r6 = csendben(ellenoriz, m6)
        ellen(r6['kod'] == 2 and not r6['elutasitva'] and 'ADATHIBA' in '\n'.join(r6['sorok']), 'a 503 mért köteg nélkül nem adathiba: %s' % r6['kod'])
        # 7. adathiba: üres könyvtár, hiányzó napló, hiányzó jsonl és hiba nélkül
        m7 = uj('f21p_onteszt_kal_ures_')
        ellen(csendben(ellenoriz, m7)['kod'] == 2, 'a hiányzó napló nem adathiba')
        m8 = uj('f21p_onteszt_kal_csaknaplo_')
        futtat_mock(m8, futtat.MockKuldo(), ['F3V3'], None)       # csak az F3V3: a SONNETV3-nak nincs sora
        ellen(csendben(ellenoriz, m8)['kod'] == 2, 'a SONNETV3 nélküli napló nem adathiba')
        # 7b. lánc: az 1. lépés (max_tokens=1024) elutasítva, a 2. (effort=low) sikeres -> kód 0, "lánc: tovább"
        m10 = uj('f21p_onteszt_kal_lanc_ok_')
        futtat_mock(m10, futtat.MockKuldo(), ['F3V3'], None)
        futtat_mock(m10, futtat.MockKuldo(s_max_tokens_400=True), [FUTAS], 1)
        r10 = csendben(ellenoriz, m10)
        sz10 = '\n'.join(r10['sorok'])
        ellen(r10['kod'] == 0 and not r10['elutasitva'] and len(r10['lanc']) == 1 and 'lánc: tovább' in sz10
              and 'reasoning_effort=low' in sz10 and 'DÖNTÉS: mehet tovább (0)' in sz10 and 'nincs végleges' in sz10
              and csendben(main, ['--forras-dir', m10]) == 0,
              'a lánc (1. elutasítva, 2. sikeres) nem 0-s kód / nincs "lánc: tovább": %s %s' % (r10['kod'], sz10[:300]))
        # 7c. lánc: mindkét lépés elutasítva -> kód 4 (a végső elutasítás + a lánc-lépés is látszik)
        m11 = uj('f21p_onteszt_kal_lanc_mind_')
        futtat_mock(m11, futtat.MockKuldo(), ['F3V3'], None)
        futtat_mock(m11, futtat.MockKuldo(s_minden_400=True), [FUTAS], 1)
        r11 = csendben(ellenoriz, m11)
        ellen(r11['kod'] == 4 and r11['elutasitva'] and len(r11['lanc']) == 1 and 'a gondolkodási lánc minden lépése elutasítva' in '\n'.join(r11['okok'])
              and csendben(main, ['--forras-dir', m11]) == 4,
              'a lánc mindkét lépésének elutasítása nem 4-es kód: %s' % r11['kod'])
        # 8. a gondolkodási token (mért) külön kiírva, nem figyelmeztetés
        m9 = uj('f21p_onteszt_kal_gond_')
        futtat_mock(m9, futtat.MockKuldo(), ['F3V3'], None)
        futtat_mock(m9, futtat.MockKuldo(), [FUTAS], 1)
        ut = os.path.join(m9, 'futasnaplo.tsv')
        with open(ut, encoding='utf-8') as f:
            sorok = f.read().split('\n')
        fej = sorok[0].split('\t')
        i_g, i_f = fej.index('gondolkodas_token'), fej.index('futas')
        for i, s_ in enumerate(sorok[1:], 1):
            m_ = s_.split('\t')
            if len(m_) == len(fej) and m_[i_f] == FUTAS:
                m_[i_g] = '77'
                sorok[i] = '\t'.join(m_)
        with open(ut, 'w', encoding='utf-8', newline='\n') as f:
            f.write('\n'.join(sorok))
        r9 = csendben(ellenoriz, m9)
        ellen(r9['kod'] == 0 and not r9['figyelmeztetesek'] and 'FIGYELMEZTETÉS' not in '\n'.join(r9['sorok'])
              and r9['gondolkodas_token'] == 77 * len([1 for r_ in _olvas_tsv(ut) if r_['futas'] == FUTAS]),
              'a naplóbeli gondolkodási token figyelmeztetést ad, vagy nem a naplóösszeg szerepel: %s' % r9['gondolkodas_token'])
        # 9. determinizmus: ugyanaz a bemenet, ugyanaz a kimenet (a ts-sor kivételével)
        ra = [x for x in csendben(ellenoriz, m1)['sorok'][1:]]
        rb = [x for x in csendben(ellenoriz, m1)['sorok'][1:]]
        ellen(ra == rb, 'az ellenőrzés nem determinisztikus')
        # 10. a main: kilépési kód
        ellen(csendben(main, ['--forras-dir', m1]) == 0 and csendben(main, ['--forras-dir', m3]) == 4 and csendben(main, ['--forras-dir', m7]) == 2,
              'a main() kilépési kódjai hibásak')
        # a kulcs nem szivárog a hibák fájljába
        szivarog = []
        for gy, _, fajlok in os.walk(m4):
            for fn in fajlok:
                with open(os.path.join(gy, fn), encoding='utf-8') as f:
                    if teszt_kulcs in f.read():
                        szivarog.append(fn)
        ellen(not szivarog, 'a kulcs megjelent a kimenetben: %s' % szivarog)
    finally:
        for m in mappak:
            shutil.rmtree(m, ignore_errors=True)
    ellen(p3c_mock.regi_kimenetek_hibak() == [], 'az önteszt megváltoztatta a régi kimeneteket: %s' % p3c_mock.regi_kimenetek_hibak())
    if hibak:
        print('ÖNTESZT HIBA:')
        for h in hibak:
            print('  ' + h)
        return 1
    print('kalibralas_ellenoriz önteszt rendben (0: rendben, M=1.3 / mért M független számítással; 4: túl drága, HTTP 400, 200-as hibatest; '
          '4: a lánc mindkét lépése elutasítva; 0: lánc 1. lépése elutasítva, a 2. sikeres; 2: adathiba, 503; mért gondolkodási token kiírása, küszöb-paraméter, determinizmus, régi kimenetek bájtazonossága)')
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--forras-dir', default=None, help='a valaszok/ és a futasnaplo.tsv könyvtára (alap: f21p/)')
    ap.add_argument('--kuszob', type=float, default=KUSZOB, help='a vetített kumulatív összeg küszöbe USD (alap: 4.90)')
    ap.add_argument('--onteszt', action='store_true')
    args = ap.parse_args(argv)
    if args.onteszt:
        return onteszt()
    r = ellenoriz(args.forras_dir, args.kuszob)
    for x in r['sorok']:
        print(x)
    return r['kod']


if __name__ == '__main__':
    sys.exit(main())
