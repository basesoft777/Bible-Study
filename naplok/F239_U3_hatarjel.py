"""F239 U3 — a határdöntés-jel beírása a HATAR_TEREMT-001.md modelles részének végére (F182; a 9-es sablon
„hét szabály” 2. pontja: a döntés commitja írja; az F239.7-ből kimaradt). Utána a frissesség mérése."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'eszkozok'))
import ellenoriz as E

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

GY = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
ut = os.path.join(GY, 'naplok', 'HATAR_TEREMT-001.md')
t = open(ut, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in t else '\n'
nd, ujjd = E.hatar_ujjlenyomat(os.path.join(GY, 'adat'), 'TEREMT-001', dt_nelkul=True)
jel = ('*A határ lezárt: a fenti kérdések (K1–K5) és a szerkesztő kilenc kérdésének döntései a `jeloltek.tsv`-n és az '
       'adattáblákon át (F239.3, F239.7); a sorállapot a döntés állapota. Új modelles kör csak új, nem a határdöntésből '
       'eredő sor-változásnál.*' + nl + nl +
       '<!-- HATÁRDÖNTÉS: n=%d ujjd=%s | DT-F239a, DT-F239b, DT-F239c, DT-F239d -->' % (nd, ujjd) + nl + nl)
if 'HATÁRDÖNTÉS:' in t:
    print('már van határdöntés-jel; nem írok')
else:
    i = t.index('<!-- MODELLES-VEGE -->')
    t = t[:i] + jel + t[i:]
    open(ut, 'w', encoding='utf-8', newline='').write(t)
print(E.hatar_frissesseg(os.path.join(GY, 'adat'), 'TEREMT-001'))
