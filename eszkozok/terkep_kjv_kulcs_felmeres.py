"""F91 M0b/a: a LXX_versificacios_terkep.tsv Karoli_igehely oszlopa KJV-kulcsu-e az osszes konyvre (csak olvas).

Kimenet: naplok/ZSOLT_FELIRAT_SZAMOZAS_M0b_terkep.md (gepi; ujrafuttathato).
TSV-olvasas: split('\t') (a csv modul tilos ezeken a tablakon).
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


# konyvnev-normalizalo: STEPBible -> magyar
sb2hu = {}
for r in list(sorok(os.path.join(K, 'Konyv_normalizalo_tabla.tsv')))[1:]:
    sb2hu[r[0]] = r[1]
    for a in (r[3].split(',') if len(r) > 3 and r[3] else []):
        sb2hu.setdefault(a.strip(), r[1])

# Karoli
kar = defaultdict(set)  # konyv -> {(c,v)}
for r in sorok(os.path.join(K, 'Karoli_1908.tsv')):
    m = re.fullmatch(r'(\S+) (\d+):(\d+)', r[0])
    if m:
        kar[m.group(1)].add((int(m.group(2)), int(m.group(3))))

# KJV (eBible)
kjv = defaultdict(set)
for r in sorok(os.path.join(K, 'KJV_Strongs_teljes.tsv')):
    m = re.fullmatch(r'([0-9A-Za-z]+)\.(\d+)\.(\d+)', r[0])
    if m and m.group(1) in sb2hu:
        kjv[sb2hu[m.group(1)]].add((int(m.group(2)), int(m.group(3))))

# A tabla: Karoli -> kjv
A = defaultdict(dict)
for r in sorok(os.path.join(K, 'Karoli_versmegfeleltetes.tsv')):
    if r[0] == 'igehely_karoli':
        continue
    m = re.fullmatch(r'(\S+) (\d+):(\d+)', r[0])
    if m:
        A[m.group(1)][(int(m.group(2)), int(m.group(3)))] = (r[1], r[2], r[3])


def heber_halmaz(s):
    """'Hos.12:1' / '1Ki.5:30a' / 'Psa.52:1-2,3' -> (set((c,v)), ok_bool)"""
    out = set()
    for blk in s.split(';'):
        m = re.fullmatch(r'\s*([0-9A-Za-z]+)\.(\d+):(.*)', blk.strip())
        if not m:
            return out, False
        c = int(m.group(2))
        for p in m.group(3).split(','):
            p = p.strip()
            mm = re.fullmatch(r'(\d+)[a-z]*(?:-(\d+)[a-z]*)?', p)
            if not mm:
                return out, False
            a = int(mm.group(1))
            b = int(mm.group(2) or a)
            for x in range(a, b + 1):
                out.add((c, x))
    return out, True


def cv_halmaz(x, b):
    m = re.fullmatch(r'(\d+):(\d+)', x.strip()) if x else None
    return {(int(m.group(1)), int(m.group(2)))} if m else None


kjv2kar = defaultdict(lambda: defaultdict(set))  # konyv -> kjv-kulcs -> {karoli-vers}
for b_, d_ in A.items():
    for w_, (kj_, mt_, o_) in d_.items():
        kk_ = cv_halmaz(kj_, b_)
        if kk_:
            kjv2kar[b_][next(iter(kk_))].add(w_)

hip = defaultdict(Counter)
stat = defaultdict(Counter)
keys_in_map = defaultdict(set)
ex_nonexist = defaultdict(list)
hos = []
for r in sorok(os.path.join(K, 'LXX_versificacios_terkep.tsv')):
    if r[0] in ('Karoli_igehely', 'KJV_igehely'):   # F91.12: az oszlop átnevezve (KJV_igehely)
        continue
    m = re.fullmatch(r'(\S+) (\d+):(\d+)', r[0])
    if not m:
        stat['(NEM_MEGHATAROZHATO)']['sor'] += 1
        continue
    b, c, v = m.group(1), int(m.group(2)), int(m.group(3))
    key = (c, v)
    s = stat[b]
    s['sor'] += 1
    keys_in_map[b].add(key)
    in_kar = key in kar[b]
    in_kjv = key in kjv[b]
    if not in_kar:
        s['kulcs_nem_karoli'] += 1
        if in_kjv:
            s['kulcs_nem_karoli_de_kjv'] += 1
        if len(ex_nonexist[b]) < 3:
            ex_nonexist[b].append(r[0])
    hl, okl = heber_halmaz(r[2])
    if okl:
        s['latin_ertelm'] += 1
        if hl == {key}:
            s['latin_eq_kulcs'] += 1
    hs, ok = heber_halmaz(r[1])
    # kulcs-hipotezis vizsgalat: csak ahol Karoli-vers k KJV-erteke nem k (a ketto megkulonboztetheto)
    if ok and key in A[b]:
        kj_, mt_, o_ = A[b][key]
        kjk = cv_halmaz(kj_, b)
        if kjk == {key}:
            hip[b]['K=KJV (nem megkulonboztetheto)'] += 1
        else:
            # Karoli-hipotezis: a Karoli-vers MT-je (ha az A-tablaban van) == Heber
            mtk = cv_halmaz(mt_, b) if mt_ else None
            ws = kjv2kar[b].get(key, set())
            mtw = set()
            okw = bool(ws)
            for w_ in ws:
                m2 = cv_halmaz(A[b][w_][1], b) if A[b][w_][1] else None
                if m2 is None:
                    okw = False
                else:
                    mtw |= m2
            hk = (mtk == hs) if mtk is not None else None
            hj = (mtw == hs) if okw else None
            hip[b][f'Karoli-hip={hk} KJV-hip={hj}'] += 1
    elif ok and key not in A[b]:
        hip[b]['kulcs nincs az A-tablaban (nem Karoli-vers)'] += 1
    if not ok:
        s['heber_nem_ertelmezheto'] += 1
    elif hs != {key}:
        s['heber_ellentmond'] += 1
        if not in_kar:
            s['ellentmond_es_nem_karoli'] += 1
    if r[0] == 'Hós 11:12':
        hos.append('\t'.join(r))

o = []
ts = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
prov = lambda f: f'`scope=minden könyv | forras={f} | ts={ts}`'
o.append('# ZSOLT_FELIRAT_SZAMOZAS_M0b_terkep.md — a LXX_versificacios_terkep `Karoli_igehely` oszlopának kulcsossága, minden könyv (F91 M0b/a)')
o.append('')
o.append('*Gép által generált (`eszkozok/terkep_kjv_kulcs_felmeres.py`), csak olvas. Mért adat.*')
o.append('')
o.append('Proveniencia: ' + ' · '.join(prov(f) for f in ['konkordancia/LXX_versificacios_terkep.tsv', 'konkordancia/Karoli_1908.tsv', 'konkordancia/KJV_Strongs_teljes.tsv', 'konkordancia/Karoli_versmegfeleltetes.tsv', 'konkordancia/Konyv_normalizalo_tabla.tsv']))
o.append('')
o.append('Oszlopok: sor = a térkép sorai; nemKár = a sor kulcsa nem létező Károli-vers; nemKár∧KJV = ebből KJV-ben létező vers; Héber≠ = a Héber_vers halmaza ≠ {a sor saját verse}; Héber≠∧nemKár = mindkettő; ≠értelm = a Héber_vers nem értelmezhető (pl. `--`); Latin=kulcs = a Latin_vers (Vulgata-számozás, a KJV-hoz közel áll) halmaza = {a sor kulcsa}; hiányzó = a térképben nem szereplő Károli-vers a könyvben (a térkép kivétel-lista, ezért nem hiba önmagában).')
o.append('')
o.append('| Könyv | sor | nemKár | nemKár∧KJV | Héber≠ | Héber≠∧nemKár | ≠értelm | Latin=kulcs / értelmezhető | hiányzó Károli-vers | Károli-versek | minta nemKár |')
o.append('|---|---|---|---|---|---|---|---|---|---|---|')
T = Counter()
for b in sorted(stat, key=lambda x: -stat[x]['sor']):
    s = stat[b]
    if b.startswith('('):
        o.append(f'| {b} | {s["sor"]} | | | | | | | | |')
        T['sor'] += s['sor']
        continue
    hiany = len(kar[b] - keys_in_map[b])
    o.append(f'| {b} | {s["sor"]} | {s["kulcs_nem_karoli"]} | {s["kulcs_nem_karoli_de_kjv"]} | {s["heber_ellentmond"]} | {s["ellentmond_es_nem_karoli"]} | {s["heber_nem_ertelmezheto"]} | {s["latin_eq_kulcs"]}/{s["latin_ertelm"]} | {hiany} | {len(kar[b])} | {", ".join(ex_nonexist[b])} |')
    for k in ('sor', 'kulcs_nem_karoli', 'kulcs_nem_karoli_de_kjv', 'heber_ellentmond', 'ellentmond_es_nem_karoli', 'heber_nem_ertelmezheto', 'latin_eq_kulcs', 'latin_ertelm'):
        T[k] += s[k]
    T['hiany'] += hiany
o.append(f'| **Összes** | {T["sor"]} | {T["kulcs_nem_karoli"]} | {T["kulcs_nem_karoli_de_kjv"]} | {T["heber_ellentmond"]} | {T["ellentmond_es_nem_karoli"]} | {T["heber_nem_ertelmezheto"]} | {T["latin_eq_kulcs"]}/{T["latin_ertelm"]} | {T["hiany"]} | | |')
o.append('')
o.append('## Hós 11:12 példa')
o.append('')
o.append(f'- Károli: Hós 11 versei: {sorted(v for c, v in kar["Hós"] if c == 11)} (max {max(v for c, v in kar["Hós"] if c == 11)}); KJV: Hós 11 max {max(v for c, v in kjv["Hós"] if c == 11)}.')
o.append(f'- Térkép-sor(ok) (Karoli_igehely, Heber_vers, Latin, Gorog, Elteres, egyezik): {hos}')
o.append(f'- A_tabla: Hós 11:11 → KJV {A["Hós"].get((11, 11), ('',))[0]}; Hós 12:1 → KJV {A["Hós"].get((12, 1), ('',))[0]}; Hós 12:2 → KJV {A["Hós"].get((12, 2), ('',))[0]}.')
o.append('')
o.append('## Kulcs-hipotézis próba (a sor kulcsa Károli- vagy KJV-vers?)')
o.append('')
o.append('Csak ott megkülönböztethető, ahol a Károli-vers `k` KJV-értéke (A tábla) nem `k`. Karoli-hip: a Károli-vers `k` MT-értéke (A.igehely_mt) = a Heber_vers halmaza. KJV-hip: azoknak a Károli-verseknek az MT-értéke, amelyek KJV-értéke `k`, = a Heber_vers halmaza. `None` = nem eldönthető (az A tábla igehely_mt üres).')
o.append('')
GT = Counter()
for b in sorted(hip, key=lambda x: -sum(hip[x].values())):
    o.append(f'- **{b}**: ' + '; '.join(f'{k}: {n}' for k, n in sorted(hip[b].items())))
    GT.update(hip[b])
o.append('')
o.append('Összes: ' + '; '.join(f'{k}: {n}' for k, n in sorted(GT.items())))
o.append('')
with open(os.path.join(ROOT, 'naplok', 'ZSOLT_FELIRAT_SZAMOZAS_M0b_terkep.md'), 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(o) + '\n')
print('kész')
