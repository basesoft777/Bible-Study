"""A vers- és szó-töredékek blokkjainak címe, jelleg-címkéi, megjegyzése és forrássora (Ez 37:16 és H7307)."""
import sys, os, json, re, html
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
d = os.path.dirname(os.path.abspath(__file__))
E = json.load(open(os.path.join(d, 'ez37.json'), encoding='utf-8'))
t = lambda x: html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', x))).strip()
def lista(h):
    for m in re.finditer(r'<section class="blokk" id="b-[^"]+" data-blokk="([^"]+)">(.*?)</section>', h, re.S):
        b, body = m.group(1), m.group(2)
        h3 = re.search(r'<h3>(.*?)</h3>', body, re.S).group(1)
        cim = t(re.split(r'<span', h3)[0])
        jel = re.findall(r'class="jelleg [^"]+"[^>]*>(.*?)</span>', h3)
        megj = re.findall(r'<span class="megj">(.*?)</span>', h3)
        f = re.search(r'<p class="forras">(.*?)</p>', body, re.S)
        ures = 'ures' in body
        print(f"{b}\t{cim}\t{','.join(jel)}\t{t(' '.join(megj))}\t{t(f.group(1)) if f else ''}\t{'üres' if ures else ''}")
print('=== VERS 37:16'); lista(E['versek']['16'])
print('=== SZÓ H7307'); lista(E['szavak']['H7307'])
