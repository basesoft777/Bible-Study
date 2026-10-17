import sys, json, os
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
d = os.path.dirname(os.path.abspath(__file__))
# használat: epit.py <adat.json> <sablon.html> <kimenet.html>
data = json.load(open(os.path.join(d, sys.argv[1]), encoding='utf-8'))
s = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')
t = open(os.path.join(d, sys.argv[2]), encoding='utf-8').read()
assert t.count('__DATA__') == 1
open(os.path.join(d, sys.argv[3]), 'w', encoding='utf-8').write(t.replace('__DATA__', s))
print('kész', len(s))
