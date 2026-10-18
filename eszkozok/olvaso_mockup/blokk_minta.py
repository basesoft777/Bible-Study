import sys, json, re, os
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
d = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(d, 'ez37.json'), encoding='utf-8'))
def blokk(v, b):
    m = re.search(r'<section class="blokk" id="b-%s"[^>]*>(.*?)</section>' % b.replace('.', '-'), E['versek'][v], re.S)
    return m.group(1) if m else None
for b in ('vers.par', 'vers.eredeti', 'vers.morf_hu', 'vers.tipnr', 'vers.bsb', 'vers.kjv', 'vers.lxx_szavak', 'vers.kh', 'vers.tsk', 'vers.motivum', 'vers.nave'):
    x = blokk('16', b)
    print('=====', b, len(x or ''))
    if x:
        print(re.sub(r'\s+', ' ', x)[:900])
hr = set()
for v, h in E['versek'].items():
    for s in ('vers.kh', 'vers.tsk'):
        x = blokk(v, s) or ''
        hr.update(re.findall(r'href="([^"]+)"', x))
print('KH href-ek', len(hr), sorted(hr)[:15])
