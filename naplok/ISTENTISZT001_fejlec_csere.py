"""A Karoli_versmegfeleltetes.tsv generált fejléc-kommentjében a (DT-F146b) → (DT398); pontosan egy előfordulás,
csak `#`-sorban, bájtszinten."""
import sys

UT = 'konkordancia/Karoli_versmegfeleltetes.tsv'
with open(UT, 'rb') as f:
    regi = f.read()
if regi.count(b'(DT-F146b)') != 1:
    raise SystemExit('nem pontosan egy előfordulás')
i = regi.index(b'(DT-F146b)')
sor_eleje = regi.rfind(b'\n', 0, i) + 1
if not regi[sor_eleje:sor_eleje + 1] == b'#':
    raise SystemExit('nem kommentsorban áll')
with open(UT, 'wb') as f:
    f.write(regi.replace(b'(DT-F146b)', b'(DT398)'))
print('kész')
