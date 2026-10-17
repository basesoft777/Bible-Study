import sys, json, re, os
from html.parser import HTMLParser
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
d = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(d, 'ez37.json'), encoding='utf-8'))

class Vaz(HTMLParser):
    def __init__(self, mely):
        super().__init__(); self.m = 0; self.mely = mely; self.ki = []
    def handle_starttag(self, t, a):
        a = dict(a)
        if t in ('meta', 'link', 'br', 'img', 'input', 'wbr'):
            if t == 'input' and self.m <= self.mely:
                self.ki.append('  ' * self.m + f"<input {a.get('type')} id={a.get('id')}>")
            return
        if self.m <= self.mely and t not in ('span', 'a', 'b', 'i', 'em', 'strong', 'sup', 'small', 'td', 'tr', 'th'):
            self.ki.append('  ' * self.m + f"<{t} id={a.get('id','')} class={a.get('class','')} {('data:' + ','.join(k for k in a if k.startswith('data-'))) if any(k.startswith('data-') for k in a) else ''}>")
        self.m += 1
    def handle_endtag(self, t):
        if t not in ('meta', 'link', 'br', 'img', 'input', 'wbr'):
            self.m -= 1

v = Vaz(6); v.feed(D['fejezet']); print('\n'.join(v.ki[:120]))
print('=====VERS 1')
v = Vaz(3); v.feed(D['versek']['1']); print('\n'.join(v.ki[:60]))
print('=====SZÓ H7307')
k = [s for s in D['szavak'] if s.startswith('H7307')]
print(k)
v = Vaz(2); v.feed(D['szavak'][k[0]]); print('\n'.join(v.ki[:60]))
h = [s for s in D['szavak'] if s.startswith('H')]; g = [s for s in D['szavak'] if s.startswith('G')]
print('H', len(h), sum(len(D['szavak'][s]) for s in h), 'G', len(g), sum(len(D['szavak'][s]) for s in g))
print('script/link a fejezetben:', re.findall(r'<(?:script|link)[^>]*>', D['fejezet'])[:10])
