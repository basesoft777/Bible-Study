# F121.2: az egyszeri rögzítő szkript (term | kapu | rogzit); a naplo 4. szakaszához
import sys, os, hashlib
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,'eszkozok')
EM='\u2014'
T='\t'
term=[
 ('call on (someone\'s) name','valakinek a nevét segítségül hívni','F121 DT-F121d (felhasználó, 2026-10-28): kapu=nem — a zárójeles kulcs a forrásban nem illeszthető regexszel; a Károli „segítségül hív”','v4','nem'),
 ('cry out (someone\'s) name','valakinek a nevét kiáltani','F121 DT-F121d: kapu=nem — zárójeles kulcs; Károli 2Móz 33:19 „kiáltom előtted az Úr nevét”','v4','nem'),
 ('deity','istenség','F121 DT-F121d: nyelvközi egység (DT238), a BDB/Thayer-fordításban is „istenség”','v4','igen'),
 ('core of one\'s identity','azonosságának magja','F121 DT-F121d: kapu=nem — szabad szövegű kifejezés','v4','nem'),
]
src={}
for l in open('naplok/F121_GLOSSZA_FORDITAS_lista.tsv',encoding='utf-8').read().split('\n')[1:]:
    c=l.split(T)
    if len(c)>=9 and c[7]=='hianyzik': src[(c[0],c[1],c[2],c[3],c[4])]=(c[5],c[8])
hu={
 ('UBS_DBH','H7121','006562001001000',EM,'definicio_hu'):'= olyan cselekvés, amellyel emberek vagy istenségek hangosan beszélnek, gyakran azért, hogy magukra vagy helyzetükre felhívják a figyelmet, és azt várják, hogy valaki így vagy úgy válaszoljon',
 ('UBS_DBH','H7121','006562001009000',EM,'definicio_hu'):'szó szerint: valakinek (valaminek) a nevét kiáltani; innen: = olyan cselekvés, amellyel emberek nevet adnak egy személynek vagy helynek',
 ('UBS_DBH','H7121','006562001011000',EM,'definicio_hu'):'szó szerint: valakinek a nevét segítségül hívni; innen: = olyan cselekvés, amellyel emberek elismernek egy istenséget, és hajlandók ennek az istenségnek néhány követelménye szerint élni',
 ('UBS_DBH','H8034','007442001001000',EM,'definicio_hu'):'= egy vagy több szó, amellyel egy személyt, istenséget, helyet vagy tárgyat ismernek, megszólítanak, emlegetnek vagy amellyel rá utalnak; ≈ amelyet az ember azonossága alapvető elemének tekintenek',
 ('UBS_DBH','H8034','007442001004000',EM,'definicio_hu'):'szó szerint: név; innen: = az azonosság magja, amely a lény lényegét tükrözi',
 ('UBS_DNTG','G1941','001957001003000','56.15','glosszak_hu'):'ügyében fellebbezni; magasabb bírósághoz fellebbezni',
}
assert set(hu)==set(src), set(hu)^set(src)
if sys.argv[1]=='term':
    p='adat/terminologia.tsv'; b=open(p,'rb').read(); assert b.endswith(b'\n')
    add=''.join(T.join(r)+'\n' for r in term)
    open(p,'wb').write(b+add.encode('utf-8')); print('terminologia +4'); sys.exit()
import forditas_kapuk as K
bukott=0
for k,h in hu.items():
    forras=src[k][1]
    ered=K.kapuk_futtat(k[0],forras,h)
    print(k[2],[(n,e) for n,e,_ in ered if e!='RENDBEN' or n in('5_terminologia','15_tiltott')],'ATMENT' if K.atment(ered) else 'BUKOTT')
    for n,e,r in ered:
        if e not in('RENDBEN',): print('   ',n,e,r)
    bukott+= not K.atment(ered)
if sys.argv[1]=='kapu' or bukott: sys.exit()
p='adat/forditasok.tsv'; reg=open(p,'rb').read(); assert reg.endswith(b'\n')
sorok=''
for k,h in hu.items():
    cols=[k[0],k[1],k[2],k[3],k[4],src[k][0],h,'sonnet','claude-sonnet-5-5','2026.10.28','v4','F121 (DT-F121b): ISTENTISZT-001 lap; D1 1. opció (CC BY-SA 4.0 forrás); proveniencia: scope=lexikon/ISTENTISZT-001 | forras=glossza_lexikon_forditas.py lista | ts=2026-10-28']
    sorok+=T.join(cols)+'\n'
open(p,'wb').write(reg+sorok.encode('utf-8'))
uj=open(p,'rb').read(); assert uj.startswith(reg); print('rogzitve +6, a meglevo bajtra azonos')
