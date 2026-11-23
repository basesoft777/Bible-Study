"""F239 U3 — a határdöntés-jel frissítése a próza után (naplok/HATAR_TEREMT-001.md). Előbb igazolja, hogy az
`elofordulasok.tsv` TEREMT-001 sorai a HEAD-hez képest csak határon kívüli mezőben változtak (kapcsolodas, funkcio,
proveniencia, karoli_szo, lexikon_szotar, lexikon_entry_id, jelentes_szam); az igehelyek halmaza és minden más mező
azonos. Csak ekkor írja át a jel `n=… ujjd=…` részét (a döntések listája változatlan), és a jel elé egy mondatot.
Futtatás: python naplok/F239_U3_hatarjel_frissit.py [--ir]"""
import os, subprocess, sys
sys.path.insert(0, 'eszkozok')
import ellenoriz as E
sys.stdout.reconfigure(encoding='utf-8')
SZABAD = {'kapcsolodas', 'funkcio', 'proveniencia', 'karoli_szo', 'lexikon_szotar', 'lexikon_entry_id', 'jelentes_szam'}


def sorok(szoveg):
    l = [x for x in szoveg.replace('\r\n', '\n').split('\n') if x and not x.startswith('#')]
    fej = l[0].split('\t')
    return {d['igehely']: d for d in (dict(zip(fej, x.split('\t'))) for x in l[1:]) if d['id'] == 'TEREMT-001'}


head = sorok(subprocess.run(['git', 'show', 'HEAD:adat/elofordulasok.tsv'], capture_output=True).stdout.decode('utf-8'))
most = sorok(open('adat/elofordulasok.tsv', encoding='utf-8').read())
if set(head) != set(most):
    sys.exit('HIBA: az igehelyek halmaza változott: %s' % (set(head) ^ set(most)))
mezok = set()
for ih in head:
    for k in head[ih]:
        if head[ih][k] != most[ih].get(k):
            mezok.add(k)
if mezok - SZABAD:
    sys.exit('HIBA: határt érintő mező változott: %s' % sorted(mezok - SZABAD))
print('változott mezők:', sorted(mezok), '· igehelyek: %d, azonos' % len(most))
nd, ujjd = E.hatar_ujjlenyomat('adat', 'TEREMT-001', dt_nelkul=True)
ut = 'naplok/HATAR_TEREMT-001.md'
t = open(ut, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'
m = E.HATARDONTES_RX.search(t)
regi = m.group(0)
uj = '<!-- HATÁRDÖNTÉS: n=%d ujjd=%s | %s -->' % (nd, ujjd, m.group(3))
mondat = ('*A jel frissítve a próza után (F239 U3, 2026-11-23): az előfordulás-sorokban csak határon kívüli mező '
          'változott (%s; `naplok/F239_U3_hatarjel_frissit.py`); az igehelyek és a döntések azonosak.*' % ', '.join(sorted(mezok)))
t = t.replace(regi, mondat + nl + nl + uj)
if '--ir' in sys.argv:
    open(ut, 'w', encoding='utf-8', newline='').write(t)
    print(E.hatar_frissesseg('adat', 'TEREMT-001'))
else:
    print('(próba)', uj)
