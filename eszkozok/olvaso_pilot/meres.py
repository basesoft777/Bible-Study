"""Olvasói pilot: mérés (F60.2, M2).

A szakaszonkénti olvaso_pilot.json-ból (adat.py kimenete) mérőszámokat számol, és
naplok/OLVASOI_PILOT_meres.md-be írja, minden mérési szakaszhoz proveniencia-sorral
(scope=… | forras=… | ts=…). Csak olvas; a szakasz JSON-ját előbb elő kell állítani.
Futtatás: python eszkozok/olvaso_pilot/meres.py [--szakasz "1Móz 1:1-2:3" --szakasz "Zsolt 22"]
          [--ki naplok/OLVASOI_PILOT_meres.md]
Ha a JSON hiányzik, a program futtatja az adat.py-t a szakasz alap-kimeneti könyvtárába."""
import argparse
import datetime
import json
import os
import subprocess
import sys
import unicodedata

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from szakasz import GY, alap_kimenet, szakasz_cim  # noqa: E402

ap = argparse.ArgumentParser(description='Olvasói pilot: mérés')
ap.add_argument('--szakasz', action='append', default=None)
ap.add_argument('--ki', default=GY + 'naplok/OLVASOI_PILOT_meres.md')
args = ap.parse_args()
SZAKASZOK = args.szakasz or ['1Móz 1:1-2:3', 'Zsolt 22']
TS = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')


def betolt(szakasz):
    ut = os.path.join(alap_kimenet(szakasz), 'olvaso_pilot.json')
    if not os.path.exists(ut):
        subprocess.run([sys.executable, os.path.join(D, 'adat.py'), '--szakasz', szakasz], check=True)
    with open(ut, encoding='utf-8') as fh:
        return json.load(fh)


def csupasz(szo):
    t = unicodedata.normalize('NFD', szo or '')
    t = ''.join(c for c in t if unicodedata.category(c) != 'Mn')
    return t.lower().replace('ς', 'σ').strip('.,;·')


def szaz(a, b):
    return '%.1f%%' % (100.0 * a / b) if b else '–'


def lap_jelentesek(lap):
    a = lap.get('appar')
    if not a:
        return 0
    return sum(1 for t in a['torzsek'] for j in t['jelentesek'] if j['jel'])


def meres(d):
    m = {}
    versek = d['versek']
    # 1. Károli-szavak kötése
    tok = [w for v in versek for w in v['hu_szavak']]
    kotott = [w for w in tok if w['fo']]
    m['hu_ossz'] = len(tok)
    m['hu_kotott'] = len(kotott)
    m['hu_magas'] = sum(1 for w in kotott if w['biz'] == 'magas')
    m['hu_alacsony'] = sum(1 for w in kotott if w['biz'] != 'magas')
    m['hu_csak_nyelvtani'] = sum(1 for w in tok if not w['fo'] and w['strongok'])
    m['hu_par_nelkul'] = sum(1 for w in tok if not w['strongok'])
    # 2. héber szó-lapok
    lapok = d['lapok']
    hu = [s for s, l in lapok.items() if l['bdb_hu']]
    en = [s for s, l in lapok.items() if not l['bdb_hu'] and l['bdb_en']]
    nincs = [s for s, l in lapok.items() if not l['bdb_hu'] and not l['bdb_en']]
    m['lap_ossz'], m['lap_hu'], m['lap_en'], m['lap_nincs'] = len(lapok), len(hu), len(en), nincs
    # 3. BDB-bontás
    bomlo, egyben, nincs_appar = [], [], []
    for s, l in sorted(lapok.items()):
        n = lap_jelentesek(l)
        cim = '%s %s' % (s, l['lemma'])
        (bomlo if n >= 2 else egyben if n == 1 else nincs_appar).append((cim, n))
    m['bomlo'], m['egyben'], m['nincs_appar'] = bomlo, egyben, nincs_appar
    # 4. görög szó-lapok
    g = d['gor_lapok']
    m['gor_ossz'] = len(g)
    m['gor_hu'] = sum(1 for x in g.values() if x['hu'])
    m['gor_usz'] = sum(1 for x in g.values() if x['usz_db'] > 0)
    m['gor_heber'] = sum(1 for x in g.values() if x['heber'])
    m['gor_tbesg'] = sum(1 for x in g.values() if x['tbesg'])
    # 5. görög szóalak forrása, χ/ξ
    hw = [w for v in versek for w in v['heber']]
    m['heber_szo'] = len(hw)
    m['macula_nincs'] = sum(1 for w in hw if not w.get('macula'))
    mw = [w['macula'] for w in hw if w.get('macula')]
    m['gorog_szo'] = [x for x in mw if x['lxx']]
    m['lxx_os'] = sum(1 for x in mw if x['lxx'] and x.get('lxx_forras') == 'LXX_OS')
    m['macula_marad'] = sum(1 for x in mw if x['lxx'] and x.get('lxx_forras') == 'Macula')
    m['gorog_nincs'] = sum(1 for x in mw if not x['lxx'])
    elter = [x for x in mw if x.get('lxx_macula') and csupasz(x['lxx_macula']) != csupasz(x['lxx'])]
    cx = 0
    for x in elter:
        a, b = csupasz(x['lxx_macula']), csupasz(x['lxx'])
        if len(a) == len(b) and all(p == q or {p, q} == {'χ', 'ξ'} for p, q in zip(a, b)):
            cx += 1
    m['alak_elter'] = len(elter)
    m['alak_cx'] = cx
    m['macula_marad_cx'] = sum(1 for x in mw if x['lxx'] and x.get('lxx_forras') == 'Macula' and ('χ' in x['lxx'] or 'ξ' in x['lxx']))
    # 6. UBS, versszámozás
    tart = [w for w in hw if not w['nyelvtani'] and w['strong'] in lapok]
    m['ubs_tart'] = len(tart)
    m['ubs_van'] = sum(1 for w in tart if w['ubs'])
    m['ubs_lap_ossz'] = len({w['strong'] for w in tart})
    m['ubs_lap_van'] = len({w['strong'] for w in tart if w['ubs']})
    vs = [(v['igehely'], v['versszam']) for v in versek]
    m['vs_kjv_hianyzik'] = [i for i, x in vs if not x['kjv']]
    m['vs_lxx_hianyzik'] = [i for i, x in vs if not x['lxx']]
    m['vs_kjv_ne_karoli'] = [i for i, x in vs if x['kjv'] and not i.endswith(' ' + x['kjv'])]
    m['vs_ellentmond'] = [i for i, x in vs if x['kjv_lxx'] and x['kjv_lxx'] != x['kjv']]
    m['vs_mt_ne_karoli'] = [i for i, x in vs if x['mt'] and not i.endswith(' ' + x['mt'])]
    m['vers_ossz'] = len(versek)
    return m


def fej(sz):
    return szakasz_cim(sz)


def sor(cimke, *ertekek):
    return '| %s | %s |' % (cimke, ' | '.join(str(e) for e in ertekek))


def tabla(fejlec, sorok):
    return '\n'.join(['| %s | %s |' % (fejlec, ' | '.join(fej(s) for s in SZAKASZOK)),
                      '|---|%s' % ('---|' * len(SZAKASZOK))] + sorok)


def lista(elemek, kor=60):
    return ', '.join(c for c, n in elemek[:kor]) + (' …(+%d)' % (len(elemek) - kor) if len(elemek) > kor else '')


def main():
    adatok = {s: betolt(s) for s in SZAKASZOK}
    M = {s: meres(adatok[s]) for s in SZAKASZOK}
    try:
        commit = subprocess.run(['git', '-C', GY, 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True,
                                encoding='utf-8').stdout.strip()
    except OSError:
        commit = '?'
    adat_ts = {s: adatok[s]['prov']['heber'].split('ts=')[-1] for s in SZAKASZOK}
    out = []
    w = out.append
    w('<!-- GENERÁLT: eszkozok/olvaso_pilot/meres.py — kézzel nem szerkesztendő. -->')
    w('# Olvasói pilot — mérés (F60.2)')
    w('')
    w('*Gép által generált (`eszkozok/olvaso_pilot/meres.py`), kézzel nem szerkesztendő; a #60 M2 lépése. Mért adatállapot: repó-commit `%s` (az `ág: claude/olvasoi-pilot` feje a mérés előtt), a szakasz-adatok `ts` ideje: %s.*'
      % (commit, ', '.join('%s %s' % (fej(s), adat_ts[s]) for s in SZAKASZOK)))
    w('')
    w('A pilot az aktuális adatállapotot méri (a #7, #9, #22, #38, #54, #56, #57 lezárása után újrafuttatható). A számok a pilot-oldalra kerülő adatot jellemzik, nem a repó egészét.')
    w('')

    def proveniencia(forras, zart=True):
        for s in SZAKASZOK:
            w('- `scope=%s | forras=%s | ts=%s`' % (fej(s), forras, TS))
        w('')

    # 1
    w('## 1. A Károli-szavak kötése héber szóhoz')
    w('')
    proveniencia('adat/karoli_strong/parok_*.tsv (modell-kimenet, #22) + konkordancia/Karoli_1908.tsv; feldolgozás: eszkozok/olvaso_pilot/adat.py (fő szó választása)')
    w(tabla('Mérőszám', [
        sor('Károli-szó (írásjelekkel együtt, szótoken)', *[M[s]['hu_ossz'] for s in SZAKASZOK]),
        sor('kötött tartalmas héber szóhoz (kattintható, szó-lappal)', *['%d (%s)' % (M[s]['hu_kotott'], szaz(M[s]['hu_kotott'], M[s]['hu_ossz'])) for s in SZAKASZOK]),
        sor('— ebből „magas” bizonyosság', *['%d (%s a kötöttekből)' % (M[s]['hu_magas'], szaz(M[s]['hu_magas'], M[s]['hu_kotott'])) for s in SZAKASZOK]),
        sor('— ebből nem „magas” (alacsony)', *['%d (%s a kötöttekből)' % (M[s]['hu_alacsony'], szaz(M[s]['hu_alacsony'], M[s]['hu_kotott'])) for s in SZAKASZOK]),
        sor('csak nyelvtani elemhez kötött (nincs szó-lap)', *['%d (%s)' % (M[s]['hu_csak_nyelvtani'], szaz(M[s]['hu_csak_nyelvtani'], M[s]['hu_ossz'])) for s in SZAKASZOK]),
        sor('párosítás nélkül', *['%d (%s)' % (M[s]['hu_par_nelkul'], szaz(M[s]['hu_par_nelkul'], M[s]['hu_ossz'])) for s in SZAKASZOK]),
    ]))
    w('')
    # 2
    w('## 2. Héber szó-lapok: BDB-szócikk')
    w('')
    proveniencia('adat/forditasok.tsv (BDB, magyar) + konkordancia/BDB_teljes_unabridged.tsv (angol)')
    w(tabla('Mérőszám', [
        sor('héber szó-lap (nem nyelvtani Strong-szám)', *[M[s]['lap_ossz'] for s in SZAKASZOK]),
        sor('van magyar BDB-szócikk', *['%d (%s)' % (M[s]['lap_hu'], szaz(M[s]['lap_hu'], M[s]['lap_ossz'])) for s in SZAKASZOK]),
        sor('csak angol BDB-szócikk', *['%d (%s)' % (M[s]['lap_en'], szaz(M[s]['lap_en'], M[s]['lap_ossz'])) for s in SZAKASZOK]),
        sor('egyik sincs (csak a Strong-szótár rövid jelentése)', *['%d (%s)' % (len(M[s]['lap_nincs']), szaz(len(M[s]['lap_nincs']), M[s]['lap_ossz'])) for s in SZAKASZOK]),
    ]))
    w('')
    for s in SZAKASZOK:
        if M[s]['lap_nincs']:
            w('- %s: BDB-szócikk nélküli szó-lapok: %s' % (fej(s), ', '.join(M[s]['lap_nincs'])))
    w('')
    # 3
    w('## 3. BDB-bontás (gépi szeletelés)')
    w('')
    proveniencia('adat/forditasok.tsv + konkordancia/BDB_teljes_unabridged.tsv; bontás: eszkozok/olvaso_pilot/bdb_szelet.py (gépi feldolgozás); „jelentés” = a szócikk számozott (1, 2 …) első szintű pontja')
    w(tabla('Mérőszám', [
        sor('legalább 2 jelentésre bomlik', *['%d (%s)' % (len(M[s]['bomlo']), szaz(len(M[s]['bomlo']), M[s]['lap_ossz'])) for s in SZAKASZOK]),
        sor('egyben marad (1 számozott jelentés)', *['%d (%s)' % (len(M[s]['egyben']), szaz(len(M[s]['egyben']), M[s]['lap_ossz'])) for s in SZAKASZOK]),
        sor('nincs számozott jelentés a szeletelésben (0)', *['%d (%s)' % (len(M[s]['nincs_appar']), szaz(len(M[s]['nincs_appar']), M[s]['lap_ossz'])) for s in SZAKASZOK]),
    ]))
    w('')
    for s in SZAKASZOK:
        w('- %s, egyben maradó szócikkek (%d): %s' % (fej(s), len(M[s]['egyben']), lista(M[s]['egyben'], 400)))
        w('- %s, számozott jelentés nélkül (%d): %s' % (fej(s), len(M[s]['nincs_appar']), lista(M[s]['nincs_appar'], 400)))
        w('- %s, bomló szócikkek (%d), jelentésszám szerint csökkenően: %s' % (
            fej(s), len(M[s]['bomlo']), ', '.join('%s (%d)' % (c, n) for c, n in sorted(M[s]['bomlo'], key=lambda t: -t[1])[:25]) + (' …' if len(M[s]['bomlo']) > 25 else '')))
    w('')
    # 4
    w('## 4. Görög szó-lapok')
    w('')
    proveniencia('konkordancia/TBESG.txt + Thayer_teljes.tsv + adat/forditasok.tsv (Thayer, UBS_DNTG) + konkordancia/TAGNT_kivonat.tsv + adat/kulso/lxx_bridge.tsv; a görög szavak köre: LXX_OS + Macula a szakasz verseire')
    w(tabla('Mérőszám', [
        sor('görög szó-lap', *[M[s]['gor_ossz'] for s in SZAKASZOK]),
        sor('van magyar jelentés (adat/forditasok.tsv: Thayer / UBS_DNTG)', *['%d (%s)' % (M[s]['gor_hu'], szaz(M[s]['gor_hu'], M[s]['gor_ossz'])) for s in SZAKASZOK]),
        sor('van újszövetségi előfordulás (TAGNT)', *['%d (%s)' % (M[s]['gor_usz'], szaz(M[s]['gor_usz'], M[s]['gor_ossz'])) for s in SZAKASZOK]),
        sor('van héber háttér (lxx_bridge)', *['%d (%s)' % (M[s]['gor_heber'], szaz(M[s]['gor_heber'], M[s]['gor_ossz'])) for s in SZAKASZOK]),
        sor('van TBESG szótári szöveg (angol)', *['%d (%s)' % (M[s]['gor_tbesg'], szaz(M[s]['gor_tbesg'], M[s]['gor_ossz'])) for s in SZAKASZOK]),
    ]))
    w('')
    # 5
    w('## 5. A görög szóalak forrása')
    w('')
    proveniencia('konkordancia/Macula_heber_*.tsv (héber–görög párosítás) + konkordancia/LXX_OS/*.tsv (szóalak); összevetés: eszkozok/olvaso_pilot/adat.py (gépi feldolgozás)')
    w(tabla('Mérőszám', [
        sor('héber szó (TAHOT-sor, a nyelvtani elemekkel együtt)', *[M[s]['heber_szo'] for s in SZAKASZOK]),
        sor('nincs Macula-párja (a görög megfelelő nem is képezhető)', *['%d (%s)' % (M[s]['macula_nincs'], szaz(M[s]['macula_nincs'], M[s]['heber_szo'])) for s in SZAKASZOK]),
        sor('Macula-párral rendelkező szó', *[M[s]['heber_szo'] - M[s]['macula_nincs'] for s in SZAKASZOK]),
        sor('— van görög megfelelője', *['%d (%s)' % (len(M[s]['gorog_szo']), szaz(len(M[s]['gorog_szo']), M[s]['heber_szo'] - M[s]['macula_nincs'])) for s in SZAKASZOK]),
        sor('— a szóalak az LXX_OS-ből (egyezés Strong-szám + alak szerint)', *['%d (%s a görögből)' % (M[s]['lxx_os'], szaz(M[s]['lxx_os'], len(M[s]['gorog_szo']))) for s in SZAKASZOK]),
        sor('— a szóalak a Maculából marad (nincs LXX_OS-egyezés)', *['%d (%s a görögből)' % (M[s]['macula_marad'], szaz(M[s]['macula_marad'], len(M[s]['gorog_szo']))) for s in SZAKASZOK]),
        sor('— ebből χ vagy ξ van a Macula-alakban (a Macula-oszlop χ/ξ-hibás)', *[M[s]['macula_marad_cx'] for s in SZAKASZOK]),
        sor('— nincs görög megfelelő (a Macula `gorog_lxx` üres)', *[M[s]['gorog_nincs'] for s in SZAKASZOK]),
        sor('Macula-alak ≠ LXX_OS-alak (ékezet és hehezet nélkül)', *[M[s]['alak_elter'] for s in SZAKASZOK]),
        sor('— ebből a χ/ξ felcserélése magyarázza', *[M[s]['alak_cx'] for s in SZAKASZOK]),
    ]))
    w('')
    # 6
    w('## 6. UBS-jelentés lefedettsége, versszámozás')
    w('')
    proveniencia('konkordancia/UBS_DBH_referenciak.tsv + UBS_DBH_jelentesek.tsv (CC BY-SA 4.0); konkordancia/Karoli_versmegfeleltetes.tsv + LXX_OS/*.tsv (versszám)')
    w(tabla('Mérőszám', [
        sor('nem nyelvtani héber szó-előfordulás', *[M[s]['ubs_tart'] for s in SZAKASZOK]),
        sor('— van UBS-jelentés-besorolás (előfordulásonként)', *['%d (%s)' % (M[s]['ubs_van'], szaz(M[s]['ubs_van'], M[s]['ubs_tart'])) for s in SZAKASZOK]),
        sor('különböző héber szó-lap', *[M[s]['ubs_lap_ossz'] for s in SZAKASZOK]),
        sor('— legalább egy előfordulásához van UBS-jelentés', *['%d (%s)' % (M[s]['ubs_lap_van'], szaz(M[s]['ubs_lap_van'], M[s]['ubs_lap_ossz'])) for s in SZAKASZOK]),
        sor('vers a szakaszban', *[M[s]['vers_ossz'] for s in SZAKASZOK]),
        sor('— a versmegfeleltető tábla szerint nincs KJV-megfelelő', *['%d' % len(M[s]['vs_kjv_hianyzik']) for s in SZAKASZOK]),
        sor('— nincs LXX-szó a versre (LXX_OS)', *['%d' % len(M[s]['vs_lxx_hianyzik']) for s in SZAKASZOK]),
        sor('— a tábla KJV- vagy MT-száma eltér a Károli-számtól', *['%d' % len(set(M[s]['vs_kjv_ne_karoli']) | set(M[s]['vs_mt_ne_karoli'])) for s in SZAKASZOK]),
        sor('— a versmegfeleltető tábla és az LXX_OS saját KJV-oszlopa ellentmond', *['%d' % len(M[s]['vs_ellentmond']) for s in SZAKASZOK]),
    ]))
    w('')
    for s in SZAKASZOK:
        for kulcs, cim in (('vs_kjv_hianyzik', 'nincs KJV-megfelelő'), ('vs_lxx_hianyzik', 'nincs LXX-szó'),
                           ('vs_ellentmond', 'a két tábla KJV-száma ellentmond')):
            if M[s][kulcs]:
                w('- %s, %s: %s' % (fej(s), cim, ', '.join(M[s][kulcs][:40]) + (' …(+%d)' % (len(M[s][kulcs]) - 40) if len(M[s][kulcs]) > 40 else '')))
    w('')
    os.makedirs(os.path.dirname(args.ki), exist_ok=True)
    with open(args.ki, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write('\n'.join(out) + '\n')
    print('kész:', args.ki)


main()
