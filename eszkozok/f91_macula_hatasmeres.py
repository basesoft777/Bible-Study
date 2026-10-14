"""F91 M2b: macula_kk.py hatásmérés (csak mér, nem ír a repóba). A Macula-sorok `karoli`/`kk_mod`/`allapot` értékét
hasonlítja három forgatókönyvben: (1) A1 előtti vs mostani Karoli_versmegfeleltetes.tsv; (2) a térkép kulcsainak hipotetikus
KJV->Károli átkulcsolása (ha a macula_kk helyesen KJV-kulcsként kezelné). Futtatás: python eszkozok/f91_macula_hatasmeres.py"""
import sys, os, re, glob, subprocess, collections, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'f17'))
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import macula_kozos as K, macula_kk, macula_import as M
sys.stdout.reconfigure(encoding='utf-8')
usfm_mag,_,_,kanoni=K.konyvtablak()
# Macula sorok
rows=[]  # (usfm-book-mag, fej, v, karoli, kk_mod, allapot)
for p in sorted(glob.glob('konkordancia/Macula_heber_*.tsv')):
    first=True
    for ln in open(p,encoding='utf-8'):
        ln=ln.rstrip('\n')
        if not ln or ln.startswith('#'): continue
        if first: first=False; continue
        f=ln.split('\t'); m=M.REF_RE.match(f[1])
        rows.append((usfm_mag[m.group(1)],int(m.group(2)),int(m.group(3)),f[2],f[3],f[4]))
print('Macula heber morfema-sor',len(rows))
mt_versek=collections.defaultdict(set)
for b,c,v,*_ in rows: mt_versek[b].add((c,v))
mt_versek=dict(mt_versek)
orig=K.tsv_olvas
OLD=os.path.join(tempfile.gettempdir(),'f91_A_old.tsv')
open(OLD,'wb').write(subprocess.run(['git','show','8be00828^:konkordancia/Karoli_versmegfeleltetes.tsv'],capture_output=True).stdout)
# KJV->Karoli atvaltas az (uj) A tablabol
fej,asor=orig('konkordancia/Karoli_versmegfeleltetes.tsv')
rev=collections.defaultdict(list)
for s in asor:
    if s[1] and re.fullmatch(r'\d+:\d+',s[1]): rev[s[0].split(' ')[0]+' '+s[1]].append(s[0])
def run(a_path=None, kjv_terkep=False):
    def patched(ut):
        base=os.path.basename(ut)
        if a_path and base=='Karoli_versmegfeleltetes.tsv': return orig(a_path)
        if kjv_terkep and base=='LXX_versificacios_terkep.tsv':
            h,ss=orig(ut); out=[]
            for s in ss:
                k=rev.get(s[0])
                if k and len(k)==1: s=[k[0]]+s[1:]
                out.append(s)
            return h,out
        return orig(ut)
    K.tsv_olvas=patched
    try:
        ki,st,ut=macula_kk.karoli_mt_terkep(mt_versek)
    finally:
        K.tsv_olvas=orig
    inv=macula_kk.mt_karoli_index(ki)
    return ki,inv,st,ut
def sorertek(inv):
    r={}
    for k in {(b,c,v) for b,c,v,*_ in rows}:
        r[k]=M.kk_ertek(inv.get(k))
    return r
S0=run(); Sold=run(OLD); Skjv=run(None,True)
E0,Eold,Ekjv=[sorertek(s[1]) for s in (S0,Sold,Skjv)]
# szinkron a commitolt Macula-oszloppal
elt=sum(1 for b,c,v,k,m_,a in rows if E0[(b,c,v)]!=(k,m_,a))
print('commitolt Macula-oszlop vs mostani kod+adat (morfema-sor):',elt)
eltold=sum(1 for b,c,v,k,m_,a in rows if Eold[(b,c,v)]!=(k,m_,a))
print('commitolt Macula-oszlop vs A1-elotti A tabla (morfema-sor):',eltold)
def hatas(nev,Ea,Eb):
    vers=[k for k in Ea if Ea[k]!=Eb[k]]
    sor=sum(1 for b,c,v,*_ in rows if Ea[(b,c,v)]!=Eb[(b,c,v)])
    kon=collections.Counter(k[0] for k in vers)
    print(nev,': ervelt MT-vers',len(vers),'morfema-sor',sor,'konyvek',dict(kon))
    zs=sorted({k[1] for k in vers if k[0]=='Zsolt'})
    print('   Zsolt fejezetek',len(zs),zs[:70])
    kar=sum(1 for k in vers if Ea[k][0]!=Eb[k][0]); mod=sum(1 for k in vers if Ea[k][1]!=Eb[k][1]); al=sum(1 for k in vers if Ea[k][2]!=Eb[k][2])
    print('   ebbol karoli-oszlop valt',kar,'kk_mod valt',mod,'allapot valt',al)
    return vers
v1=hatas('(1) A1: A1-elotti A  ->  mostani A (terkep valtozatlan)',Eold,E0)
v2=hatas('(2) terkep KJV->Karoli atkulcsolva (hipotetikus, ha macula_kk KJV-kulcsot kezelne helyesen)',E0,Ekjv)
# (3) atnevezes: poziciós olvasás
print('(3) atnevezes: macula_kk pozicio szerint (s[0], s[1], s[5]) olvas; az oszlopnev nem szerepel -> 0 hatas')
print('stat S0',{k:v for k,v in S0[2].items() if k!='kezi_fejezetek'})
print('stat Sold',{k:v for k,v in Sold[2].items() if k!='kezi_fejezetek'})
# mintak
for k in sorted(v1)[:3]: print('minta1',k,Eold[k],E0[k])
for k in sorted(v2)[:3]: print('minta2',k,E0[k],Ekjv[k])
# terkep kulcs szerinti atkulcsolas mennyi sort ert
h,ts=orig('konkordancia/LXX_versificacios_terkep.tsv')
atk=sum(1 for s in ts if len(rev.get(s[0],[]))==1 and rev[s[0]][0]!=s[0])
print('terkep sorok, amelyek kulcsa KJV->Karoli atvaltasnal valtozna:',atk,'/',len(ts))

print('utkozes (terkep vs KK) db: mostani',len(S0[3]),'| terkep atkulcsolva',len(Skjv[3]))
ujak=set(map(tuple,[(u[0],u[1],u[2]) for u in Skjv[3]])); regiek=set(map(tuple,[(u[0],u[1],u[2]) for u in S0[3]]))
print('  utkozes-konyvek mostani',dict(collections.Counter(u[0] for u in S0[3]).most_common(8)))
print('  utkozes-konyvek atkulcsolva',dict(collections.Counter(u[0] for u in Skjv[3]).most_common(8)))
