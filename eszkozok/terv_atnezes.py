#!/usr/bin/env python3
# terv_atnezes.py — a tervjegyzet szakaszainak gépi egybeolvasása a repó fájljaival.
# Nem értelmez: a szakaszokban álló hivatkozásokat (#nn, DT-…, Dnn, N…, SEMA x.y, Fnn) keresi
# ki a repó mai fájljaiból, és egymás mellé teszi. Használat:
#   python3 terv_atnezes.py --terv ADATVAGYON_TERV.md --repo <repo gyökér> --ki ATNEZES.md
import re, sys, os, argparse, datetime
# UTF-8 stdout/stderr (CLAUDE.md shell-szabály): Windowson a héber/görög kiírás enélkül hibát dob
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(encoding='utf-8', errors='replace')
    except Exception: pass

def olvas(p):
    try: return open(p, encoding='utf-8', errors='replace').read()
    except FileNotFoundError: return ''

def feladatok_sorok(t):
    d = {}
    for l in t.splitlines():
        if l.startswith('| ') and not l.startswith('| #') and not l.startswith('| ---'):
            c = [x.strip() for x in l.split('|')]
            if len(c) > 5 and c[1].isdigit():
                d[int(c[1])] = {'nev': c[2], 'statusz': c[4], 'fugg': c[5], 'sor': l}
    return d

def tabla_sorok(t, prefix_re):
    d = {}
    for l in t.splitlines():
        m = re.match(r'\|\s*(' + prefix_re + r')\s*\|', l)
        if m: d[m.group(1)] = l
    return d

def nyitott_tetelek(t):
    d = {}
    for m in re.finditer(r'\*\*(N-?[A-Z]?\d+[a-z]?)\s*[—-]\s*(.*?)\*\*', t):
        d[m.group(1)] = m.group(2)[:140]
    return d

def sema_szakaszok(t):
    d = {}
    for m in re.finditer(r'^###\s+(\d+\.\d+)\s+(.*)$', t, re.M):
        d[m.group(1)] = m.group(2)[:100]
    return d

def szakaszok(terv):
    parts = re.split(r'^(## .*)$', terv, flags=re.M)
    out = []
    for i in range(1, len(parts), 2):
        out.append((parts[i][3:].strip(), parts[i+1]))
    return out

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--terv', required=True); ap.add_argument('--repo', required=True); ap.add_argument('--ki', required=True)
    a = ap.parse_args()
    R = a.repo
    FEL = feladatok_sorok(olvas(os.path.join(R, 'FELADATOK.md')))
    DT = tabla_sorok(olvas(os.path.join(R, 'DONTESEK.md')), r'DT-?[A-Z]?\d+[a-z]?|D\d+')
    DFEL = tabla_sorok(olvas(os.path.join(R, 'FELADATOK.md')), r'D\d+')   # D34–D41 a FELADATOK-ban
    NY = nyitott_tetelek(olvas(os.path.join(R, 'NYITOTT_FELADATOK.md')))
    SEMA = sema_szakaszok(olvas(os.path.join(R, 'adat', 'SEMA.md')))
    briefek = {f[:3]: f for f in os.listdir(R) if re.match(r'F\d\d_.*BRIEF\.md$', f)}
    terv = olvas(a.terv)
    ki = []
    ki.append(f'# Terv-átnézés — {os.path.basename(a.terv)} ↔ repó\n\nGenerált: {datetime.date.today()} · `terv_atnezes.py` · nem értelmez, hivatkozásokat olvas egybe. Üres cella = a terv olyat mond, amire a repóban nincs hivatkozott sor.\n')
    osszes_fejbol = []
    for cim, szoveg in szakaszok(terv):
        ki.append(f'\n## {cim}\n')
        fel = sorted({int(x) for x in re.findall(r'#(\d{1,2})\b', szoveg)})
        dts = sorted(set(re.findall(r'\bDT-?[A-Z]?\d+[a-z]?\b', szoveg)))
        ds  = sorted(set(re.findall(r'\bD(\d{1,2})\b', szoveg)), key=int)
        ns  = sorted(set(re.findall(r'\bN-?[A-Z]?\d+[a-z]?\b', szoveg)))
        sem = sorted(set(re.findall(r'\b(\d\.\d{1,2})\b(?=[^\d]|$)', szoveg)))
        fs  = sorted(set(re.findall(r'\bF(\d{2})\b', szoveg)))
        rows = []
        for n in fel:
            if n in FEL: rows.append(('FELADATOK', f'#{n}', f"{FEL[n]['statusz']} · {FEL[n]['nev'][:90]} · függ: {FEL[n]['fugg'][:50]}"))
            else: rows.append(('FELADATOK', f'#{n}', '— nincs ilyen sor'))
        for d in dts:
            key = d if d in DT else next((k for k in DT if k.replace('-', '') == d.replace('-', '')), None)
            rows.append(('DONTESEK', d, (DT[key][:220] if key else '— nincs ilyen tétel')))
        for d in ds:
            k = 'D' + d
            src = DT.get(k) or DFEL.get(k)
            rows.append(('D-döntés', k, (src[:220] if src else '— nincs ilyen sor')))
        for n in ns:
            rows.append(('NYITOTT', n, NY.get(n, '— nincs ilyen tétel')))
        for s in sem:
            if s in SEMA: rows.append(('SEMA', s, SEMA[s]))
        for f in fs:
            rows.append(('brief', 'F' + f, briefek.get('F' + f, '— nincs brief fájl')))
        if rows:
            ki.append('| forrás | hivatkozás | a repó mai sora |\n| --- | --- | --- |')
            for r in rows: ki.append(f'| {r[0]} | {r[1]} | {r[2].replace("|", "¦")} |')
        # fejből-gyanús fogalmak: a terv saját szavai, amikre nincs repó-hivatkozás
        fogalmak = ['vers-lap', 'szó-lap', 'motívum-lap', 'lelet-lap', 'pardes.db', 'sqlite_epit', 'MCP', 'backend', 'serverless', 'cPanel', 'Netlify Function', 'AI-réteg', 'ujjlenyomat', 'variancia-térkép', 'adatblokk', 'terminologia_rogzit', 'dontes_rogzit']
        talalt = [f for f in fogalmak if f.lower() in szoveg.lower()]
        if talalt:
            ki.append(f'\n*A terv saját fogalmai ebben a szakaszban (repó-hivatkozás nélkül):* {", ".join(talalt)}')
            osszes_fejbol += talalt
    ki.append('\n## Összesítés — a terv saját fogalmai\n')
    from collections import Counter
    for f, n in Counter(osszes_fejbol).most_common():
        ki.append(f'- **{f}** — {n} szakaszban; a repóban nincs rá hivatkozott sor → a #23/#11 bemenete, vagy elesik')
    open(a.ki, 'w', encoding='utf-8').write('\n'.join(ki) + '\n')
    print('kész:', a.ki, len(ki), 'sor')

if __name__ == '__main__': main()
