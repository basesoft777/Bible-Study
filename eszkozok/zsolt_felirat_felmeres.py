"""F91 M0: a feliratos zsoltárok Károli–KJV számozásának felmérése (csak olvas).

Kimenet: naplok/ZSOLT_FELIRAT_SZAMOZAS_M0.md (gépi; a szkript újrafuttatható).
TSV-olvasás: split('\t') (a csv modul tilos ezeken a táblákon).
"""
import sys
import re
import os
import datetime
from collections import defaultdict, Counter

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'konkordancia')


def sorok(path):
    with open(path, encoding='utf-8') as f:
        for ln in f:
            ln = ln.rstrip('\n').rstrip('\r')
            if not ln or ln.startswith('#'):
                continue
            yield ln.split('\t')


def vs(s):
    """'3:16' -> (3,16)"""
    m = re.fullmatch(r'(\d+):(\d+)', s.strip())
    return (int(m.group(1)), int(m.group(2))) if m else None


# --- Károli ---
kar = defaultdict(dict)  # fejezet -> vers -> szöveg
for r in sorok(os.path.join(K, 'Karoli_1908.tsv')):
    m = re.fullmatch(r'Zsolt (\d+):(\d+)', r[0])
    if m:
        kar[int(m.group(1))][int(m.group(2))] = r[1] if len(r) > 1 else ''

# --- TAHOT (vers-kulcs, Károli-kulcsú az F85.6 óta) ---
tah = defaultdict(set)
for r in sorok(os.path.join(K, 'TAHOT_kivonat.tsv')):
    m = re.fullmatch(r'Zsolt (\d+):(\d+)', r[0])
    if m:
        tah[int(m.group(1))].add(int(m.group(2)))

# --- KJV (eBible) ---
kjv = defaultdict(set)
for r in sorok(os.path.join(K, 'KJV_Strongs_teljes.tsv')):
    m = re.fullmatch(r'Psa\.(\d+)\.(\d+)', r[0])
    if m:
        kjv[int(m.group(1))].add(int(m.group(2)))

# --- LXX_OS etalon: Károli-vers -> KJV-vers halmaz, ok ---
et = defaultdict(lambda: defaultdict(set))  # c -> v -> {kjv v}
et_ok = defaultdict(lambda: defaultdict(set))
for r in sorok(os.path.join(K, 'LXX_OS', 'psalms-lxx.tsv')):
    if r[0] == 'igehely_lxx':
        continue
    m = re.fullmatch(r'Zsolt (\d+):(\d+)', r[2])
    if not m:
        continue
    c, v = int(m.group(1)), int(m.group(2))
    et_ok[c][v].add(r[3])
    if r[1]:
        for part in r[1].split(','):
            x = vs(part)
            if x and x[0] == c:
                et[c][v].add(x[1])

# --- A tábla: Karoli_versmegfeleltetes ---
tA = defaultdict(dict)  # c -> v -> (kjv_str, osztaly)
for r in sorok(os.path.join(K, 'Karoli_versmegfeleltetes.tsv')):
    if r[0] == 'igehely_karoli':
        continue
    m = re.fullmatch(r'Zsolt (\d+):(\d+)', r[0])
    if m:
        tA[int(m.group(1))][int(m.group(2))] = (r[1], r[3], r[4])

# --- B tábla: LXX_versificacios_terkep ---
tB = defaultdict(lambda: defaultdict(list))
for r in sorok(os.path.join(K, 'LXX_versificacios_terkep.tsv')):
    if r[0] == 'Karoli_igehely':
        continue
    m = re.fullmatch(r'Zsolt (\d+):(\d+)', r[0])
    if m:
        tB[int(m.group(1))][int(m.group(2))].append(r[1])


def heber_halmaz(s, c):
    """'Psa.22:1-2' / 'Psa.52:1-2,3' -> {1,2,...}; csak a c fejezetre."""
    out = set()
    for blk in s.split(';'):
        m = re.fullmatch(r'\s*Psa\.(\d+):(.*)', blk.strip())
        if not m or int(m.group(1)) != c:
            continue
        for p in m.group(2).split(','):
            p = p.strip()
            mm = re.fullmatch(r'(\d+)(?:-(\d+))?[a-z]*', p)
            if mm:
                a = int(mm.group(1))
                b = int(mm.group(2) or a)
                out.update(range(a, b + 1))
    return out


# --- zsoltáronkénti mérés ---
sor = []
for c in range(1, 151):
    kmax = max(kar[c]) if kar[c] else 0
    jmax = max(kjv[c]) if kjv[c] else 0
    tmax = max(tah[c]) if tah[c] else 0
    d = kmax - jmax
    # etalon eltolás: Károli v - KJV v, a nem üres kulcsú versekre
    elt = Counter()
    for v, s in et[c].items():
        if len(s) == 1:
            elt[v - next(iter(s))] += 1
    etalon_d = max(elt) if elt else None
    # A tábla: a várt KJV-vers = v - d (v > d), felirat (v <= d) -> nincs
    a_rossz = 0
    a_fel_rossz = 0
    a_hiany = 0
    a_kjv_azonos = 0
    for v in kar[c]:
        if v not in tA[c]:
            a_hiany += 1
            continue
        kjs, osz, _ = tA[c][v]
        x = vs(kjs) if kjs else None
        if kjs == '':
            continue
        if v <= d:
            if kjs:
                a_fel_rossz += 1
        else:
            if x != (c, v - d) and not (x is None):
                a_rossz += 1
        if x == (c, v):
            a_kjv_azonos += 1
    # A tábla vs etalon (közvetlen): ahol az etalon egyértelmű és a két érték eltér
    a_vs_et = 0
    for v in kar[c]:
        if v in tA[c] and len(et[c].get(v, ())) == 1 and tA[c][v][0]:
            x = vs(tA[c][v][0])
            if x and x[1] != next(iter(et[c][v])):
                a_vs_et += 1
    # B tábla: a várt Héber-halmaz = {v}
    b_rossz = 0
    b_hiany = 0
    for v in kar[c]:
        if v not in tB[c]:
            b_hiany += 1
            continue
        u = set()
        for h in tB[c][v]:
            u |= heber_halmaz(h, c)
        if u != {v}:
            b_rossz += 1
    # etalon eltérése a d-szabálytól (v > d: KJV = v - d; v <= d: felirat)
    et_kiv = []
    for v in sorted(kar[c]):
        ks = et[c].get(v, set())
        if v > d and ks and ks != {v - d}:
            et_kiv.append(f'{v}->{"+".join(str(k) for k in sorted(ks))}')
    felirat = ''
    if d > 0 and 1 in kar[c]:
        felirat = kar[c][1][:40]
    sor.append(dict(c=c, kmax=kmax, jmax=jmax, tmax=tmax, d=d, etd=etalon_d,
                    a_rossz=a_rossz, a_fel=a_fel_rossz, a_hiany=a_hiany,
                    a_vs_et=a_vs_et, et_kiv=et_kiv, b_rossz=b_rossz, b_hiany=b_hiany,
                    felirat=felirat))

# --- Nave ---
nave_c = Counter()
nave_p = []
hdr = None
for r in sorok(os.path.join(K, 'Nave_basokant.tsv')):
    if hdr is None:
        hdr = r
        continue
    row = dict(zip(hdr, r))
    m = re.fullmatch(r'Zsolt (\d+):(\d+)', row.get('igehely', ''))
    if m and row.get('hely_tipus') == 'vers':
        c, v = int(m.group(1)), int(m.group(2))
        dd = sor[c - 1]['d']
        nave_c[(dd > 0, row.get('karoli_allapot'),
                'karoli_kitoltve' if row.get('igehely_karoli') else 'karoli_ures')] += 1
        if dd > 0 and len(nave_p) < 3:
            nave_p.append((row['igehely'], row['karoli_allapot'], row['igehely_karoli']))
    elif row.get('igehely', '').startswith('Zsolt ') and row.get('hely_tipus') != 'vers':
        nave_c[('nem_vers:' + str(row.get('hely_tipus')), row.get('karoli_allapot'), '')] += 1

# --- kimenet ---
ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
prov = lambda f: f'`scope=Zsolt 1–150 | forras={f} | ts={ts}`'
fel = [x for x in sor if x['d'] > 0]
nincs = [x for x in sor if x['d'] == 0]
o = []
o.append('# ZSOLT_FELIRAT_SZAMOZAS_M0.md — a feliratos zsoltárok számozásának felmérése (F91 M0)')
o.append('')
o.append('*Gép által generált (`eszkozok/zsolt_felirat_felmeres.py`), csak olvas; kézzel nem szerkesztendő. Mért adat, nem becslés.*')
o.append('')
o.append('## 1. Módszer')
o.append('')
o.append('- **Felirat-hossz** `d` = Károli-maximumvers − KJV-maximumvers zsoltáronként. Okfejtés: a Károli az MT szerint számoz (a felirat számozott vers); a KJV a feliratot nem számozza. Ahol a két maximum azonos, a Károli és a KJV számozása egyezik.')
o.append('- **Etalon:** az `LXX_OS/psalms-lxx.tsv` Károli-kulcsa (`igehely_karoli` ↔ `igehely_kjv`, F54, `karoli_ok = zsolt_felirat_eltolas` a feliratversekre, `mt_szamozas_kovetes` a többire). Az etalon KJV-oszlopa a KJV-szöveggel egyező (verse_pairs.jsonl TVTMS-alapú MT–KJV kulcs); a felirat-versek KJV-célja duplikált (a felirat a következő KJV-verssel közös célra mutat), ezért a felirat-verseket a `d` alapján, nem az etalon KJV-oszlopa alapján azonosítom.')
o.append('- **Független KJV-hossz:** `KJV_Strongs_teljes.tsv` (eBible) különböző versszáma fejezetenként.')
o.append('- **A tábla** = `Karoli_versmegfeleltetes.tsv` (Károli → `igehely_kjv`). Várt: `v ≤ d` felirat → nincs KJV-vers; `v > d` → KJV `v − d`. Hibás: felirat-versre van KJV-érték (`A_fel`); vagy `v > d` és az érték ≠ `v − d` (`A_hibas`).')
o.append('- **B tábla** = `LXX_versificacios_terkep.tsv` (Károli → `Heber_vers`). Mivel a Károli az MT-számozást követi, a várt Héber-halmaz egyetlen elem: a vers maga. Hibás (`B_hibas`): a Károli-vers sorainak Héber-halmaz-uniója ≠ {v}.')
o.append('')
o.append('Proveniencia: ' + ' · '.join([prov('konkordancia/Karoli_1908.tsv'), prov('konkordancia/TAHOT_kivonat.tsv'),
         prov('konkordancia/KJV_Strongs_teljes.tsv'), prov('konkordancia/LXX_OS/psalms-lxx.tsv'),
         prov('konkordancia/Karoli_versmegfeleltetes.tsv'), prov('konkordancia/LXX_versificacios_terkep.tsv'),
         prov('konkordancia/Nave_basokant.tsv')]))
o.append('')

# összesítők
dc = Counter(x['d'] for x in sor)
o.append('## 2. Fő számok')
o.append('')
o.append(f'- Zsoltárfejezet összesen: {len(sor)}.')
o.append(f'- Feliratos (`d > 0`): **{len(fel)}**; ebből `d = 1`: {dc.get(1,0)}, `d = 2`: {dc.get(2,0)}, más: {sum(v for k,v in dc.items() if k not in (0,1,2))}.')
o.append(f'- Nem feliratos (`d = 0`, Károli = KJV): {len(nincs)}; `d < 0` (Károli rövidebb): {sum(v for k,v in dc.items() if k<0)}.')
o.append(f'- A tábla hibás vers (Károli v > d, érték ≠ v − d): {sum(x["a_rossz"] for x in sor)}; feliratversre adott KJV-érték: {sum(x["a_fel"] for x in sor)}; A-ban hiányzó Károli-vers: {sum(x["a_hiany"] for x in sor)}.')
o.append(f'- B tábla hibás Károli-vers (Héber-halmaz ≠ {{v}}): {sum(x["b_rossz"] for x in sor)}; B-ben hiányzó Károli-vers: {sum(x["b_hiany"] for x in sor)}.')
o.append(f'- A tábla közvetlen ellentmondása az etalon KJV-oszlopával (egyértelmű etalon-soron): {sum(x["a_vs_et"] for x in sor)} vers.')
o.append(f'- Károli-max ≠ TAHOT-max (a TAHOT-kulcs F85.6 óta Károli-kulcsú): {sum(1 for x in sor if x["kmax"] != x["tmax"])} zsoltár.')
o.append(f'- Az etalon alapján kivétel-jelölt (d = 0 a maximumok szerint, mégis eltolt): {", ".join("Zsolt "+str(x["c"]) for x in sor if x["d"]==0 and x["etd"] not in (0,None)) or "nincs"}.')
o.append(f'- Összes érintett zsoltár (feliratos + kivétel): {len([x for x in sor if x["d"]>0 or x["etd"] not in (0,None)])}.')
z22 = sor[21]
o.append(f'- **Zsolt 22:** d = {z22["d"]}, Károli {z22["kmax"]} vers, KJV {z22["jmax"]} vers; A_hibas = {z22["a_rossz"]}, A_fel = {z22["a_fel"]}, A vs etalon = {z22["a_vs_et"]}, B_hibas = {z22["b_rossz"]}.')
o.append('')
o.append('## 3. Zsoltáronkénti táblázat (csak a feliratos zsoltárok, `d > 0`)')
o.append('')
o.append('| Zsolt | Károli max | KJV max | TAHOT max | d | etalon d | A_hibas | A_fel | A_hiany | A vs etalon | B_hibas | B_hiany | v1 kezdete |')
o.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|')
for x in fel:
    o.append(f'| {x["c"]} | {x["kmax"]} | {x["jmax"]} | {x["tmax"]} | {x["d"]} | {x["etd"]} | {x["a_rossz"]} | {x["a_fel"]} | {x["a_hiany"]} | {x["a_vs_et"]} | {x["b_rossz"]} | {x["b_hiany"]} | {x["felirat"]} |')
o.append('')
o.append('## 4. Nem feliratos zsoltárok, amelyeknél a mérés mégis eltérést jelez (`d = 0`, de hibás sor van, vagy az etalon más `d`-t ad)')
o.append('')
for x in nincs:
    if x['a_rossz'] or x['b_rossz'] or x['a_hiany'] or x['b_hiany'] or x['a_vs_et'] or (x['etd'] not in (0, None)):
        o.append(f'- Zsolt {x["c"]}: Károli {x["kmax"]}, KJV {x["jmax"]}, TAHOT {x["tmax"]}, etalon d = {x["etd"]}, A_hibas {x["a_rossz"]}, A_hiany {x["a_hiany"]}, B_hibas {x["b_rossz"]}, B_hiany {x["b_hiany"]}, A vs etalon {x["a_vs_et"]}')
o.append('')
o.append('## 5. Etalon és a független `d` összevetése')
o.append('')
elt_elter = [x for x in sor if x['etd'] is not None and x['etd'] != x['d']]
o.append(f'Az etalon legnagyobb eltolása (`etalon d`) és a Károli−KJV maximum-különbség (`d`) eltér {len(elt_elter)} zsoltárban: ' +
         (', '.join(f'Zsolt {x["c"]} (d={x["d"]}, etalon={x["etd"]})' for x in elt_elter) if elt_elter else 'sehol.'))
o.append('')
kiv = [x for x in sor if x['et_kiv']]
o.append('Az etalon KJV-oszlopa eltér a `d`-szabálytól (Károli v → KJV v−d), vagyis kivétel-jelölt (v → KJV-vers; több KJV-vers = a KJV két verse egy Károli-versben):')
o.append('')
for x in kiv:
    o.append(f'- Zsolt {x["c"]} (d = {x["d"]}, etalon d = {x["etd"]}): ' + ', '.join(x['et_kiv']))
if not kiv:
    o.append('- nincs.')
o.append('')
o.append('## 6. Nave `karoli_allapot` (csak a Zsoltárok vers-szintű sorai)')
o.append('')
o.append('| feliratos fejezet | karoli_allapot | igehely_karoli |  sor |')
o.append('|---|---|---|---|')
for k, n in sorted(nave_c.items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]), str(kv[0][2]))):
    o.append(f'| {k[0]} | {k[1]} | {k[2]} | {n} |')
o.append('')
o.append('Minta feliratos fejezet sorokból (igehely, karoli_allapot, igehely_karoli): ' + '; '.join(str(p) for p in nave_p))
o.append('')

out = os.path.join(ROOT, 'naplok', 'ZSOLT_FELIRAT_SZAMOZAS_M0.md')
with open(out, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(o) + '\n')
print('kész:', out, 'feliratos:', len(fel))
