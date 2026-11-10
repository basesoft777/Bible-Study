"""F105: a két vak kitöltő ítéletének összevetése a kulccsal, Wilson-intervallummal (95%). Futtatás: python naplok/F105_vak_osszevet.py"""
import sys, math
sys.stdout.reconfigure(encoding='utf-8')
d='naplok/'
def rd(f):
    L=open(d+f,encoding='utf-8').read().splitlines()
    return {r.split('\t')[0]:r.split('\t')[1] for r in L[1:] if r.strip()}
k=rd('F105_vak_kulcs.tsv'); a=rd('F105_vak_kitolto_1.tsv'); b=rd('F105_vak_kitolto_2.tsv')
def wilson(x,n,z=1.96):
    p=x/n; den=1+z*z/n; c=(p+z*z/(2*n))/den; h=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return c-h,c+h
elter=[s for s in k if a.get(s)!=b.get(s)]
print('n',len(k),'kitolto-elteres',elter)
for nev,f in (('k1',a),('k2',b)):
    x=sum(1 for s in k if f.get(s)==k[s]); print(nev,x,len(k),'%.3f-%.3f'%wilson(x,len(k)))
egy=[s for s in k if a.get(s)==b.get(s)]
x=sum(1 for s in egy if a[s]==k[s]); print('egyezo',x,len(egy),'%.3f-%.3f'%wilson(x,len(egy)))
print('rossz (helyreallitott ellen):',[s for s in egy if a[s]!=k[s]])
k2={s:v for s,v in k.items() if s!='4'}
x=sum(1 for s in k2 if a.get(s)==b.get(s)==k2[s]); print('4. nelkul',x,len(k2),'%.3f-%.3f'%wilson(x,len(k2)))
