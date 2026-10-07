"""F23 M0 felmérés (csak olvas) — FELADATOK #23, F23_MOTIVUM_FORRAS_BRIEF.md M0/2–5.

Futtatás (a repó gyökeréből):  python naplok/MOTIVUM_FORRAS_M0.py

Kimenet (csak ezeket írja, mást nem):
  naplok/MOTIVUM_FORRAS_torzscikk_egyedi.tsv   (M0/2)
  naplok/MOTIVUM_FORRAS_parositas.tsv          (M0/3)
  naplok/MOTIVUM_FORRAS_naplo_keveredes.tsv    (M0/4)
  naplok/MOTIVUM_FORRAS_atfedes.tsv            (M0/5)
A stdout-ra összesítő számokat és a ⭐-küszöb (COUNT(DISTINCT fo_elofordulas))
értékeit írja (az M0/1 aktiválási oszlopához).

Módszer:
  M0/2 — a törzscikk minden nem üres sora (táblasorban cellánként) egység;
         a horgony-linkek (`](#…)`) és az `<a id>` sorok kimaradnak, 4 szónál
         rövidebb egység kimarad. Egy egység „egyedi-jelölt”, ha a 3 szavas
         n-gramjainak kevesebb mint 50%-a található meg a referenciakorpuszban
         (a motívum _TUDOMANYOS.md-je + forrás-study + kereszthivatkozás-napló +
         motivumok/[ID].md + minden adat/*.tsv). A jelöltek kézi besorolása
         (hol_kellene_elnie) a futás után, a TSV-ben történik.
  M0/3 — adat/motivumok.tsv forras_study + adat/res_forras.tsv tanulmany oszlop.
  M0/4–5 hatóköre: tematikus_lezart/*.md + tematikus_lezart/naplok/*.md
         (az M0/4-ben ezen felül motivumok/*.md).
  M0/4 — 【NAPLO blokk = a „【NAPLO” kezdő jelek száma. A gyanús proveniencia-
         szöveget a 【NAPLO…】 szakaszok kivágása után számolja: dátum
         (20ÉÉ.HH.NN / 20ÉÉ-HH-NN), fájlnév (*.md/.tsv/.py/.txt), „l. X pont/
         szakasz”, és a „felismerve / visszaírva / audit során” szavak.
  M0/5 — 8 szavas n-gram (kisbetű, \\w+ tokenek) bekezdésenként (üres sorral
         határolt blokk); egy pár akkor kerül be, ha legalább 2 közös 8-gram van.
         Az a 8-gram, amely legalább 5 különböző bővített fájlban áll,
         sablonformula (pl. az 5. pont kérdés-címei), külön oszlopban számolva;
         a kategória (bekezdes_masolat ≥0,5 / reszleges ≥0,2 / rovid_egyezes)
         csak a nem-formula 8-gramok arányából jön; ha csak formula közös:
         sablonformula.
"""

import os
import re
import sys
import glob

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARANCS = 'python naplok/MOTIVUM_FORRAS_M0.py'
TOK = re.compile(r'\w+', re.UNICODE)


def olvas(rel):
    with open(os.path.join(GYOKER, rel), encoding='utf-8') as f:
        return f.read()


def tsv(rel):
    """TSV olvasás split('\\t')-vel (CLAUDE.md: csv modul tilos)."""
    sorok = [s for s in olvas(rel).split('\n') if s and not s.startswith('#')]
    fej = sorok[0].split('\t')
    return [dict(zip(fej, s.split('\t'))) for s in sorok[1:]]


def ir_tsv(rel, fej, sorok):
    with open(os.path.join(GYOKER, rel), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\t'.join(fej) + '\n')
        for s in sorok:
            f.write('\t'.join(str(x).replace('\t', ' ').replace('\n', ' ') for x in s) + '\n')


def tokenek(szoveg):
    return TOK.findall(szoveg.lower())


def ngramok(tok, n):
    return {tuple(tok[i:i + n]) for i in range(len(tok) - n + 1)}


def kivonat(szoveg, n=15):
    t = re.sub(r'[`*_>#|]', '', szoveg)
    return ' '.join(t.split()[:n])


def bekezdesek(szoveg):
    """(kezdősor, szöveg) párok, üres sorral határolt blokkok."""
    ki, buf, kezd = [], [], None
    for i, sor in enumerate(szoveg.split('\n'), 1):
        if sor.strip():
            if kezd is None:
                kezd = i
            buf.append(sor)
        elif buf:
            ki.append((kezd, '\n'.join(buf)))
            buf, kezd = [], None
    if buf:
        ki.append((kezd, '\n'.join(buf)))
    return ki


motivumok = tsv('adat/motivumok.tsv')
res = tsv('adat/res_forras.tsv')
elof = tsv('adat/elofordulasok.tsv')

# ---------------------------------------------------------------- ⭐-küszöb
print('== ⭐-küszöb: COUNT(DISTINCT fo_elofordulas) ID-nként (adat/elofordulasok.tsv)')
for m in motivumok:
    fo = {e['fo_elofordulas'] for e in elof if e['id'] == m['id'] and e.get('fo_elofordulas', '').strip()}
    sorok = sum(1 for e in elof if e['id'] == m['id'])
    print(f"  {m['id']}\tfo_elofordulas={len(fo)}\telofordulas_sor={sorok}")

# ---------------------------------------------------------------- M0/3
tem_fajlok = sorted(glob.glob(os.path.join(GYOKER, 'tematikus_lezart', '*.md')))
tem_rel = [os.path.relpath(p, GYOKER).replace('\\', '/') for p in tem_fajlok]
# M0/4–5: a tematikus_lezart/naplok/ kereszthivatkozás-naplói is a mérés részei (ELLENOR_F23 3. pont)
tem_naplo_rel = sorted(os.path.relpath(p, GYOKER).replace(os.sep, '/') for p in glob.glob(os.path.join(GYOKER, 'tematikus_lezart', 'naplok', '*.md')))
par_sorok = []
lefedett_id = set()
for rel in tem_rel:
    ms = [m['id'] for m in motivumok if rel in m.get('forras_study', '').split(';')]
    rs = sorted({r['id'] for r in res if r.get('tanulmany') == rel})
    ids = sorted(set(ms) | set(rs))
    tanulmany = rel.endswith('_tematikus.md')
    if ids:
        for i in ids:
            lefedett_id.add(i)
            alap = []
            if i in ms:
                alap.append('motivumok.tsv:forras_study')
            if i in rs:
                alap.append('res_forras.tsv:tanulmany')
            par_sorok.append([rel, i, 'tanulmany' if tanulmany else 'nem_tanulmany', '+'.join(alap), '', PARANCS])
    else:
        elso = olvas(rel).split('\n', 1)[0].lstrip('# ').strip()
        par_sorok.append([rel, '—', 'tanulmany' if tanulmany else 'nem_tanulmany', 'nincs motívum-hivatkozás',
                          'első sor: ' + kivonat(elso), PARANCS])
for m in motivumok:
    if m['id'] not in lefedett_id:
        par_sorok.append(['—', m['id'], 'nincs_tematikus', 'motivumok.tsv:forras_study=' + (m.get('forras_study') or 'üres'),
                          'statusz=' + m.get('statusz', ''), PARANCS])
ir_tsv('naplok/MOTIVUM_FORRAS_parositas.tsv',
       ['fajl', 'motivum_id', 'besorolas', 'parositas_alapja', 'megjegyzes', 'forras_parancs'], par_sorok)
print(f'== M0/3: {len(tem_rel)} fájl a tematikus_lezart/ gyökerében; {len(par_sorok)} sor')

# ---------------------------------------------------------------- M0/2
adat_korpusz = []
for p in sorted(glob.glob(os.path.join(GYOKER, 'adat', '*.tsv'))):
    with open(p, encoding='utf-8') as f:
        adat_korpusz.append(f.read())
LINK = re.compile(r'\]\(#[^)]*\)|\(#[^)]*\)')
adat_tok = tokenek('\n'.join(adat_korpusz))
adat_3 = ngramok(adat_tok, 3)

def besorol(e, szak):
    """Gépi előbesorolás: render-szerkezet vs. valódi tartalom. A 'nem_besorolt'
    sorokat kézzel kell átnézni (a TSV-ben ez a jelölés marad)."""
    s = re.sub(r'[*`_\[]', '', e).strip()
    if s.lstrip('#').strip() == szak.split(' / ')[-1] or szak.startswith('Tartalom'):
        return 'render_szerkezet: generalt (címsor/tartalomjegyzék)'
    if s.startswith('- LXX:'):
        return 'atrendezett_adat: generalt (LXX-blokk; átírás a torzscikk_general.py KIEJT-táblájából)'
    if s.startswith('- Kapcsolatok:'):
        return 'atrendezett_adat: generalt (adat/kapcsolatok.tsv)'
    if s.startswith('- TSK-kereszthivatkozás') or s.startswith('- Károli-kereszthivatkozás'):
        return 'atrendezett_adat: generalt (konkordancia TSK/Károli-KH)'
    if '·' in s and ' — ' in szak and ' / ' not in szak and re.search(r'\b[GH]\d{4}\)', s):
        return 'atrendezett_adat: generalt (törzsadat-kártya „Fő szavak”: adat/elofordulasok.tsv strong + kiejtés)'
    if s.startswith('- Strong') or s.startswith('- Kulcsszó') or s.startswith('- UBS-jelentés'):
        return 'atrendezett_adat: generalt (adat/elofordulasok.tsv)'
    if re.match(r'^\d+ \(\d+ ÓSZ / \d+ ÚSZ\)$', s):
        return 'szamolt_ertek: generalt (adat/elofordulasok.tsv)'
    if szak.startswith('5. Szótári háttér'):
        return 'render_szoveg: generalt (adat/szotar_szerepek.tsv + torzscikk_general.py)'
    if szak.startswith('Források és licenc') or s.startswith('Kereszthivatkozási törzscikk'):
        return 'render_szoveg: generalt (torzscikk_general.py sablonszöveg)'
    return 'nem_besorolt'


egyedi_sorok = []
egyseg_ossz = 0
for m in motivumok:
    mid = m['id']
    tz = f'lexikon/{mid}_TORZSCIKK.md'
    if not os.path.exists(os.path.join(GYOKER, tz)):
        continue
    ref = [olvas(f'lexikon/{mid}_TUDOMANYOS.md')]
    if os.path.exists(os.path.join(GYOKER, f'motivumok/{mid}.md')):
        ref.append(olvas(f'motivumok/{mid}.md'))
    for fs in m.get('forras_study', '').split(';'):
        if fs and os.path.exists(os.path.join(GYOKER, fs)):
            ref.append(olvas(fs))
    for r in res:
        if r['id'] == mid and r.get('tanulmany', '').endswith('.md') and os.path.exists(os.path.join(GYOKER, r['tanulmany'])):
            ref.append(olvas(r['tanulmany']))
    ref_tok = tokenek(LINK.sub('', '\n'.join(ref)))
    ref_3 = ngramok(ref_tok, 3) | adat_3
    sz2, sz3 = '(fejléc előtt)', ''
    for sor in olvas(tz).split('\n'):
        s = sor.strip()
        if not s or s.startswith('<!--') or s.startswith('<a id'):
            continue
        if s.startswith('### '):
            sz3 = s[4:].strip()
        elif s.startswith('#'):
            sz2, sz3 = s.lstrip('#').strip(), ''
        if s.startswith('|') and set(s) <= set('|-: '):
            continue
        s = LINK.sub('', s)
        egysegek = [c for c in s.strip('|').split('|')] if s.startswith('|') else [s]
        for e in egysegek:
            t = tokenek(e)
            if len(t) < 4:
                continue
            egyseg_ossz += 1
            g = [tuple(t[i:i + 3]) for i in range(len(t) - 2)]
            arany = sum(1 for x in g if x in ref_3) / len(g)
            if arany < 0.5:
                szak = sz2 + (' / ' + sz3 if sz3 else '')
                egyedi_sorok.append([mid, szak, kivonat(e), f'{arany:.2f}', besorol(e, szak), PARANCS])
ir_tsv('naplok/MOTIVUM_FORRAS_torzscikk_egyedi.tsv',
       ['motivum', 'szakasz', 'kivonat', 'lefedettseg_3gram', 'hol_kellene_elnie', 'forras_parancs'], egyedi_sorok)
print(f'== M0/2: {egyseg_ossz} vizsgált egység, {len(egyedi_sorok)} egyedi-jelölt')
szak_db = {}
for s in egyedi_sorok:
    k = (s[0], s[1].split(' / ')[0])
    szak_db[k] = szak_db.get(k, 0) + 1
for k in sorted(szak_db):
    print(f'  {k[0]}\t{k[1]}\t{szak_db[k]}')

# ---------------------------------------------------------------- M0/4
NAPLO_SPAN = re.compile(r'【NAPLO.*?】', re.S)
MINTAK = {
    'datum': re.compile(r'\b20\d\d[.\-]\d\d[.\-]\d\d\b'),
    'fajlnev': re.compile(r'[\w\-]+\.(?:md|tsv|py|txt)\b'),
    'l_pont': re.compile(r'\bl\.\s[^\n]{0,40}?\b(?:pont|szakasz)', re.I),
    'felismerve_visszairva_audit': re.compile(r'felismerve|visszaírva|audit során', re.I),
}
kev_sorok = []
ossz = {'naplo': 0, **{k: 0 for k in MINTAK}, 'gyanus_sor': 0}
for rel in tem_rel + tem_naplo_rel + sorted(os.path.relpath(p, GYOKER).replace('\\', '/') for p in glob.glob(os.path.join(GYOKER, 'motivumok', '*.md'))):
    sz = olvas(rel)
    naplo = sz.count('【NAPLO')
    kint = NAPLO_SPAN.sub('', sz)
    db = {k: len(r.findall(kint)) for k, r in MINTAK.items()}
    gy = sum(1 for sor in kint.split('\n') if any(r.search(sor) for r in MINTAK.values()))
    sorok = sz.count('\n') + 1
    kev_sorok.append([rel, naplo, db['datum'], db['fajlnev'], db['l_pont'], db['felismerve_visszairva_audit'], gy, sorok, PARANCS])
    ossz['naplo'] += naplo
    ossz['gyanus_sor'] += gy
    for k in MINTAK:
        ossz[k] += db[k]
ir_tsv('naplok/MOTIVUM_FORRAS_naplo_keveredes.tsv',
       ['fajl', 'naplo_blokk', 'datum', 'fajlnev', 'l_pont', 'felismerve_visszairva_audit', 'gyanus_sor', 'sorok', 'forras_parancs'],
       kev_sorok)
print(f'== M0/4: {len(kev_sorok)} fájl; összesen {ossz}')

# ---------------------------------------------------------------- M0/5
N = 8
FORMULA_KUSZOB = 5
bov = sorted(os.path.relpath(p, GYOKER).replace('\\', '/') for p in glob.glob(os.path.join(GYOKER, 'genezis', '*_bovitett.md')))
index = {}
for rel in bov:
    for kezd, b in bekezdesek(olvas(rel)):
        for g in ngramok(tokenek(b), N):
            index.setdefault(g, set()).add((rel, kezd))
atf_sorok = []
kat_db = {}
for rel in tem_rel + tem_naplo_rel:
    for kezd, b in bekezdesek(olvas(rel)):
        gs = ngramok(tokenek(b), N)
        if not gs:
            continue
        talalat, formula = {}, {}
        for g in gs:
            celok = index.get(g, ())
            # sablonformula: a 8-gram legalább FORMULA_KUSZOB különböző bővített fájlban áll
            f_db = len({c[0] for c in celok})
            for cel in celok:
                if f_db >= FORMULA_KUSZOB:
                    formula[cel] = formula.get(cel, 0) + 1
                else:
                    talalat[cel] = talalat.get(cel, 0) + 1
        for cel in sorted(set(talalat) | set(formula)):
            db, fdb = talalat.get(cel, 0), formula.get(cel, 0)
            if db + fdb < 2:
                continue
            arany = db / len(gs)
            if db < 2:
                kat = 'sablonformula'
            else:
                kat = 'bekezdes_masolat' if arany >= 0.5 else ('reszleges' if arany >= 0.2 else 'rovid_egyezes')
            kat_db[kat] = kat_db.get(kat, 0) + 1
            atf_sorok.append([rel, kezd, cel[0], cel[1], db, fdb, len(gs), f'{arany:.2f}', kat, kivonat(b), PARANCS])
ir_tsv('naplok/MOTIVUM_FORRAS_atfedes.tsv',
       ['tematikus_fajl', 'tematikus_sor', 'bovitett_fajl', 'bovitett_sor', 'kozos_8gram', 'formula_8gram', 'tematikus_8gram',
        'arany', 'kategoria', 'kivonat', 'forras_parancs'], atf_sorok)
print(f'== M0/5: {len(bov)} bővített fájl; {len(atf_sorok)} átfedő bekezdéspár; kategóriák: {kat_db}')
fp = {}
for s in atf_sorok:
    fp[(s[0], s[2])] = fp.get((s[0], s[2]), 0) + 1
for k in sorted(fp):
    print(f'  {k[0]} ↔ {k[1]}: {fp[k]}')
