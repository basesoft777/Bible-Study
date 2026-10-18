import sys, json, re, os
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
d = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(d, 'ez37.json'), encoding='utf-8'))
f = D['fejezet']
i = f.find('id="szoveg"'); print(f[i-40:i+1500]); print('...')
i = f.find('class="cimkek"'); print(f[i-20:i+900]); print('...')
i = f.find('class="szoveg-jegy"'); print(f[i-20:i+900]); print('...')
print('vers blokkok:', re.findall(r'data-blokk="([^"]+)"', D['versek']['1']))
print('vers blokk-címek:', re.findall(r'<h3>(.*?)</h3>', D['versek']['1'])[:20])
print('szó blokkok H7307:', re.findall(r'data-blokk="([^"]+)"', D['szavak']['H7307']))
s = D['szavak']['H7307']; print(s[:900])
print('ARCULAT', D['arculat_css'][:700])
print('OLVASO css méret', len(D['olvaso_css']), 'root-szelektorok', re.findall(r'[^{}]*:root[^{]*', D['olvaso_css'])[:10])
print('href minták', set(re.findall(r'href="(/[a-z]+/)', ''.join(D['versek'].values())+D['fejezet'])))
