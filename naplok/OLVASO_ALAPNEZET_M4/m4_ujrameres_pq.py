"""#134 M4 kiegészítés: a DT-F134p/q utáni újramérés (375 / 768 / 920 / 1280 px; szó- és versmód, 900 px alatt a teljes nézet is), képekkel.

Futtatás: python m4_ujrameres_pq.py <képkönyvtár>  (szerver: 127.0.0.1:8799; a m4_bongeszo_meres.py mellette)."""
import sys, json, os, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import m4_bongeszo_meres as m

sys.stdout.reconfigure(encoding='utf-8')
KI = sys.argv[1]
S = 'http://127.0.0.1:8799'
JS = r"""(() => { const lap = document.querySelector('#reszletek'); const lr = lap.getBoundingClientRect();
  const lat = e => { const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const gord = [], kilogo = [], dobozGorget = [];
  lap.querySelectorAll('*').forEach(e => { if (!lat(e)) return; const cs = getComputedStyle(e); const r = e.getBoundingClientRect();
    if ((cs.overflowY === 'auto' || cs.overflowY === 'scroll') && e.scrollHeight > e.clientHeight + 1) gord.push(String(e.className) + ':' + Math.round(r.height));
    if (e.classList.contains('tabla-doboz')) { if (e.scrollWidth > e.clientWidth + 1) dobozGorget.push((e.closest('[data-blokk]') || {}).getAttribute?.('data-blokk') + ':+' + (e.scrollWidth - e.clientWidth)); if (r.right > lr.right + 1) kilogo.push('doboz ' + Math.round(r.right - lr.right)); }
    if (e.tagName === 'TABLE' && !e.closest('.tabla-doboz') && r.right > lr.right + 1) kilogo.push('tabla ' + Math.round(r.right - lr.right)); });
  return {lapTeteje: Math.round(lr.top), lapVizszTulfolyas: lap.scrollWidth - lap.clientWidth, oldalTulfolyas: document.documentElement.scrollWidth - document.documentElement.clientWidth,
          lapSajatGorget: lap.scrollHeight > lap.clientHeight + 1, belsoGorgetok: gord, kilogo, gorgethetoDobozok: dobozGorget,
          dobozok: lap.querySelectorAll('.tabla-doboz').length, gordul: lap.querySelectorAll('.gordul').length}; })()"""

p, prof = m.chrome_indit('C:/Program Files/Google/Chrome/Application/chrome.exe', 9337)
ered = []
try:
    c = m.uj_lap(9337)
    m.emulal(c, 1280, 900, False); m.nyit(c, S + '/szint/kutato', 0.5)
    for w, h in ((375, 812), (768, 1024), (920, 900), (1280, 900)):
        for nev, url, k in [('szo', S + '/1Moz/1', '#v3 a.szo[data-strong="H0216"]'),
                            ('vers', S + '/1Moz/1', '#v3 a.versszam'),
                            ('ez37vers', S + '/Ez/37', '#v12 a.versszam')]:
            m.emulal(c, w, h, False); m.nyit(c, url, 1.5); ok = m.kattint(c, k, False, 2)
            r = c.js(JS); r.update({'szelesseg': w, 'jelenet': nev, 'kattintas_ok': ok}); ered.append(r)
            if w < 900:
                c.js("(() => { const b = document.querySelector('.lap-teljes'); if (b) b.click(); })()"); time.sleep(0.8)
                t = c.js("(() => { const l = document.querySelector('#reszletek').getBoundingClientRect(); return {teljesTeteje: Math.round(l.top), teljesMagassag: Math.round(l.height), nezetablak: innerHeight, egesz: document.body.classList.contains('lap-egesz')}; })()")
                t2 = c.js(JS); r.update(t); r['teljesNezetben'] = {k: t2[k] for k in ('lapVizszTulfolyas', 'belsoGorgetok', 'kilogo')}
            print(json.dumps(r, ensure_ascii=False))
    # képek: 375 px, teljes nézet, a táblához / a BDB-blokkhoz görgetve
    for nev, url, k, cel in [('vers', S + '/1Moz/1', '#v3 a.versszam', '[data-blokk="vers.eredeti"]'),
                             ('ez37vers', S + '/Ez/37', '#v12 a.versszam', '[data-blokk="vers.ubs"]'),
                             ('szo', S + '/1Moz/1', '#v3 a.szo[data-strong="H0216"]', '.gordul')]:
        for w, h in ((375, 812), (768, 1024)):
            m.emulal(c, w, h, False); m.nyit(c, url, 1.5); m.kattint(c, k, False, 2)
            c.js("(() => { const b = document.querySelector('.lap-teljes'); if (b) b.click(); })()"); time.sleep(0.8)
            c.js("(() => { const t = document.querySelector('#reszletek " + cel + "'); if (t) t.scrollIntoView({block: 'start'}); const l = document.querySelector('#reszletek'); l.scrollTop -= 120; })()")
            time.sleep(0.6)
            m.kep(c, os.path.join(KI, f'pq_szerver_{nev}_{w}.png'))
finally:
    p.terminate()
with open(os.path.join(KI, 'meres_pq.json'), 'w', encoding='utf-8') as f:
    json.dump({'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'jelenetek': ered}, f, ensure_ascii=False, indent=1)
