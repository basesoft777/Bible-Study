import sys
if hasattr(sys.stdout,'reconfigure'): sys.stdout.reconfigure(encoding='utf-8')
def read(p):
    L=[l.rstrip('\n').split('\t') for l in open(p,encoding='utf-8') if l.strip() and not l.startswith('#')]
    h=L[0]; return [dict(zip(h,r+['']*(len(h)-len(r)))) for r in L[1:]]
key={r['azon']:r for r in read('BDB_SZELETELO_M2_minta_kulcs.tsv')}
ell={}
for f in ('A','B'):
    for r in read(f'BDB_SZELETELO_M2_minta_kitoltott_{f}.tsv'): ell[r['azon']]=r
def np(p):
    p=p.strip()
    while p.endswith('/-'): p=p[:-2]
    return p
rows=[]
for a,k in key.items():
    e=ell[a]
    mt_k=k['mt_vers']; mt_e=e['konyv_mt'].split(' (')[0]
    ok_vers=(mt_k==mt_e)
    kar_k=k['karoli_vers'] or ''
    kar_e=e['karoli_vers']; kar_e=mt_e if kar_e=='=' else kar_e
    # checker's short karoli like '92:12' -> same book as mt
    if kar_e and ':' in kar_e and ' ' not in kar_e: kar_e=mt_e.rsplit(' ',1)[0]+' '+kar_e
    ok_kar=(kar_k==kar_e) or (not kar_k and kar_e in('-',''))
    ok_jp=(np(k['utvonal'])==np(e['jelentespont']))
    szk='filtered' if k['szurt']=='1' else ('bizonytalan' if k['okkod'] else 'bibliai')
    sze='filtered' if e['szures'].startswith('alhiv') else ('bizonytalan' if e['szures'].startswith('bizony') else 'bibliai')
    rows.append((a,k['reteg'],ok_vers,ok_kar,ok_jp,szk,sze,k,e))
v=[r for r in rows if r[1]=='veletlen']
print('veletlen',len(v))
print('konyv/vers (MT) egyezik:',sum(r[2] for r in v))
print('karoli egyezik:',sum(r[3] for r in v))
print('jelentespont egyezik:',sum(r[4] for r in v))
for r in rows:
    a,l,ov,ok,oj,szk,sze,k,e=r
    if l=='veletlen':
        if not ov: print('VERS',a,k['strong'],k['nyers'],'| kulcs:',k['mt_vers'],'| ell:',e['konyv_mt'])
for r in rows:
    a,l,ov,ok,oj,szk,sze,k,e=r
    if l=='veletlen' and ov and not ok: print('KAROLI',a,'| kulcs:',k['karoli_vers'],'| ell:',e['karoli_vers'])
for r in rows:
    a,l,ov,ok,oj,szk,sze,k,e=r
    if l=='veletlen' and not oj: print('JP',a,k['strong'],'| kulcs:',k['utvonal'],'| ell:',e['jelentespont'])
for l in ('szurt','bizonytalan'):
    s=[r for r in rows if r[1]==l]
    print(l,len(s),'szures-egyezes:',sum(r[5]==r[6] for r in s))
    for r in s:
        if r[5]!=r[6]: print('SZ',r[0],r[7]['nyers'],'| kulcs:',r[5],r[7]['okkod'],'| ell:',r[8]['szures'][:70])
