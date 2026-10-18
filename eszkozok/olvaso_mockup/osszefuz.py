import sys, json, os
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
d = os.path.dirname(os.path.abspath(__file__))
k = json.load(open(os.path.join(d, 'konk.json'), encoding='utf-8'))
b = json.load(open(os.path.join(d, 'bdb.json'), encoding='utf-8'))
van = {r['r'] for r in k['sorok']}
# jelentés-csomópontok: felső szint (törzs/szám) és alpont; versenként a csomópontok halmaza
cs, vers = [], {}
for j in b['jel']:
    top = f"{j['torzs']}/{j['jel'] or '-'}"
    sajat = list(j['refek'])
    alok = []
    for a in j['al']:
        p = f"{top}/{a['jel']}"
        alok.append({'p': p, 'jel': a['jel'], 'c': a['cimke'], 'n': len(a['refek'])})
        for ih in a['refek']:
            if ih in van:
                vers.setdefault(ih, set()).update([top, p])
    for ih in sajat:
        if ih in van:
            vers.setdefault(ih, set()).add(top)
    cs.append({'p': top, 'torzs': j['torzs'], 'jel': j['jel'], 'c': j['cimke'],
               'n': len(sajat) + sum(x['n'] for x in alok), 'al': alok})
k['bdb'] = {'cs': cs, 'vers': {ih: sorted(s) for ih, s in vers.items()}, 'hiv_n': b['hiv_n'], 'talal_n': b['talal_n']}
json.dump(k, open(os.path.join(d, 'konk2.json'), 'w', encoding='utf-8'), ensure_ascii=False)
print('versek jelentéssel', len(vers), 'csomópont', len(cs))
