"""#134 M4: böngészős elrendezés-mérés és képernyőképek a szerveren, a #60 pilotban és a mockup 9. változatában.

Headless Chrome a DevTools-protokollon (CDP), csak stdlib (saját websocket-kliens). Szélességenként
(375 telefon-emulációval, 768, 920, 1280) jelenetet nyit, kattint (valódi egéresemény a koordinátán), mér
(getBoundingClientRect, scrollWidth, ragadós/fix elemek, görgetődobozok, kis érintési célok) és PNG-t ment.

Futtatás:
    python m4_bongeszo_meres.py --chrome <chrome.exe> --szerver http://127.0.0.1:8799 \
        --pilot <pilot.html> --mockup <v9.html> --ki <képkönyvtár> --json <mérés.json>
Csak olvas: a szervertől GET-kéréseket kér, a repóba nem ír (a képkönyvtáron és a JSON-on kívül).
"""
import argparse
import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

SZELESSEGEK = [(375, 812, True), (768, 1024, False), (920, 900, False), (1280, 900, False)]


# ---------------------------------------------------------------- minimális websocket + CDP
class WS:
    def __init__(self, url):
        assert url.startswith('ws://')
        hostport, path = url[5:].split('/', 1)
        host, port = hostport.split(':')
        self.s = socket.create_connection((host, int(port)), timeout=120)
        kulcs = base64.b64encode(os.urandom(16)).decode()
        self.s.sendall((f'GET /{path} HTTP/1.1\r\nHost: {hostport}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\n'
                        f'Sec-WebSocket-Key: {kulcs}\r\nSec-WebSocket-Version: 13\r\n\r\n').encode())
        valasz = b''
        while b'\r\n\r\n' not in valasz:
            valasz += self.s.recv(4096)
        fej, self.puffer = valasz.split(b'\r\n\r\n', 1)
        assert b' 101 ' in fej.split(b'\r\n')[0], fej

    def kuld(self, szoveg):
        adat = szoveg.encode()
        fej = bytearray([0x81])
        n = len(adat)
        if n < 126:
            fej.append(0x80 | n)
        elif n < 65536:
            fej.append(0x80 | 126); fej += struct.pack('>H', n)
        else:
            fej.append(0x80 | 127); fej += struct.pack('>Q', n)
        maszk = os.urandom(4)
        fej += maszk
        self.s.sendall(bytes(fej) + bytes(b ^ maszk[i % 4] for i, b in enumerate(adat)))

    def _olvas(self, n):
        while len(self.puffer) < n:
            d = self.s.recv(1 << 20)
            if not d:
                raise ConnectionError('a websocket lezárult')
            self.puffer += d
        ki, self.puffer = self.puffer[:n], self.puffer[n:]
        return ki

    def fogad(self):
        darabok = []
        while True:
            b1, b2 = self._olvas(2)
            fin, op, n = b1 & 0x80, b1 & 0x0f, b2 & 0x7f
            if n == 126:
                n = struct.unpack('>H', self._olvas(2))[0]
            elif n == 127:
                n = struct.unpack('>Q', self._olvas(8))[0]
            adat = self._olvas(n)
            if op == 9:      # ping
                continue
            darabok.append(adat)
            if fin:
                return b''.join(darabok).decode('utf-8', 'replace')


class CDP:
    def __init__(self, ws):
        self.ws, self.n, self.esemenyek = ws, 0, []

    def hiv(self, metodus, **param):
        self.n += 1
        az = self.n
        self.ws.kuld(json.dumps({'id': az, 'method': metodus, 'params': param}))
        while True:
            u = json.loads(self.ws.fogad())
            if u.get('id') == az:
                if 'error' in u:
                    raise RuntimeError(f'{metodus}: {u["error"]}')
                return u.get('result', {})
            self.esemenyek.append(u)

    def var_esemeny(self, nev, ido=30):
        hatar = time.time() + ido
        for i, e in enumerate(self.esemenyek):
            if e.get('method') == nev:
                del self.esemenyek[:i + 1]
                return e
        self.ws.s.settimeout(ido)
        while time.time() < hatar:
            u = json.loads(self.ws.fogad())
            if u.get('method') == nev:
                return u
        raise TimeoutError(nev)

    def js(self, kifejezes):
        r = self.hiv('Runtime.evaluate', expression=kifejezes, returnByValue=True, awaitPromise=True)
        if 'exceptionDetails' in r:
            raise RuntimeError(json.dumps(r['exceptionDetails'], ensure_ascii=False)[:600])
        return r.get('result', {}).get('value')


# ---------------------------------------------------------------- mérőkód (a böngészőben fut)
MERO_JS = r"""
((sel) => {
  const vw = innerWidth, vh = innerHeight;
  const dq = (s, gy = document) => { if (!s) return null; const e = gy.querySelector(s); if (e) return e; for (const h of gy.querySelectorAll('*')) { if (h.shadowRoot) { const t = dq(s, h.shadowRoot); if (t) return t; } } return null; };
  const q = s => dq(s);
  const rr = e => { if (!e) return null; const r = e.getBoundingClientRect(); return {top: Math.round(r.top), bottom: Math.round(r.bottom), left: Math.round(r.left), right: Math.round(r.right), h: Math.round(r.height), w: Math.round(r.width), docTop: Math.round(r.top + scrollY)}; };
  const lathato = e => { if (!e) return false; const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden') return false; const r = e.getBoundingClientRect(); return r.width > 0 && r.height > 0; };
  const ki = {vw, vh, scrollY: Math.round(scrollY), docH: document.documentElement.scrollHeight};
  ki.tulfolyas = document.documentElement.scrollWidth - document.documentElement.clientWidth;
  ki.elsoVers = rr(q(sel.elsoVers));
  ki.fejlec = rr(q(sel.fejlec));
  if (q(sel.fejlec)) ki.fejlecPos = getComputedStyle(q(sel.fejlec)).position;
  const lap = q(sel.reszlet);
  ki.reszlet = lathato(lap) ? rr(lap) : null;
  if (lap && lathato(lap)) {
    const lr = lap.getBoundingClientRect();
    ki.reszletPos = getComputedStyle(lap).position;
    ki.reszletLathatoAViewportban = lr.top < vh && lr.bottom > 0;
    // a részleteken belüli vízszintes túlfolyás és kilógó táblák
    let maxBelso = 0, kilogo = 0, gorgTabla = 0, gord = [];
    lap.querySelectorAll('*').forEach(e => {
      if (!lathato(e)) return;
      const r = e.getBoundingClientRect();
      if (e.tagName === 'TABLE' && r.right > lr.right + 1) {
        let a = e.parentElement, vago = null;
        while (a && a !== lap) { const ox = getComputedStyle(a).overflowX; if (ox !== 'visible') { vago = a; break; } a = a.parentElement; }
        if (vago && vago.getBoundingClientRect().right <= lr.right + 1) gorgTabla++; else kilogo++;
      }
      const cs = getComputedStyle(e);
      if ((cs.overflowX === 'auto' || cs.overflowX === 'scroll') && e.scrollWidth > e.clientWidth + 1) maxBelso = Math.max(maxBelso, e.scrollWidth - e.clientWidth);
      if ((cs.overflowY === 'auto' || cs.overflowY === 'scroll') && e.scrollHeight > e.clientHeight + 1 && e !== lap) gord.push((e.className || e.tagName).toString().slice(0, 40) + ':' + Math.round(r.height));
    });
    const lcs = getComputedStyle(lap);
    ki.reszletSajatGorgetes = (lcs.overflowY === 'auto' || lcs.overflowY === 'scroll') && lap.scrollHeight > lap.clientHeight + 1;
    ki.reszletBelsoTulfolyas = maxBelso;
    ki.reszletKilogoTablak = kilogo;
    ki.reszletGorgethetoTablak = gorgTabla;
    ki.reszletVizszTulfolyas = lap.scrollWidth - lap.clientWidth;
    ki.reszletBelsoGorgetok = gord;
    ki.reszletTablakSzama = lap.querySelectorAll('table').length;
    ki.reszletBlokkok = lap.querySelectorAll(sel.blokk || '[data-blokk]').length;
  }
  const cel = q(sel.celVers);
  ki.celVers = rr(cel);
  if (cel && ki.reszlet) ki.celVersLatszikALapFolott = ki.celVers.bottom > 0 && ki.celVers.top >= 0 && (ki.reszletPos !== 'fixed' || ki.celVers.top < ki.reszlet.top);
  // tartós (fixed/sticky) látható elemek
  const tartos = [];
  document.querySelectorAll('body *').forEach(e => {
    const p = getComputedStyle(e).position;
    if ((p === 'fixed' || p === 'sticky') && lathato(e)) { const r = e.getBoundingClientRect(); if (r.bottom > 0 && r.top < vh) tartos.push(((e.className && e.className.toString()) || e.tagName).slice(0, 30) + ' ' + p + ' ' + Math.round(r.top) + '+' + Math.round(r.height)); }
  });
  ki.tartos = tartos;
  // érintési célok
  let osszes = 0, kicsi = 0;
  document.querySelectorAll('a[href], button, summary, input, select, [role=button], [tabindex="0"]').forEach(e => {
    if (!lathato(e)) return;
    const r = e.getBoundingClientRect();
    osszes++;
    if (r.width < 24 || r.height < 24) kicsi++;
  });
  ki.erintes = {kicsi, osszes};
  ki.cim = document.title;
  return ki;
})
"""

SZERVER_SEL = {
    'elsoVers': '.szoveg-oszlop .vers, .szoveg-oszlop .il-vers',
    'fejlec': 'header.fejlec',
    'reszlet': '#reszletek',
    'celVers': '#v3',
    'blokk': '[data-blokk]',
}
PILOT_SEL = {
    'elsoVers': '#szoveg .vers',
    'fejlec': 'header.fej',
    'reszlet': 'aside.panel',
    'celVers': '#v-2',
    'blokk': 'section.blokk, .blokk',
}
MOCKUP_SEL = {
    'elsoVers': '.szoveg-oszlop .vers',
    'fejlec': 'header.top',
    'reszlet': 'aside.panel',
    'celVers': '#v12',
    'blokk': '[data-blokk]',
}


def chrome_indit(chrome, port):
    profil = tempfile.mkdtemp(prefix='m4_chrome_')
    p = subprocess.Popen([chrome, '--headless=new', f'--remote-debugging-port={port}', f'--user-data-dir={profil}',
                          '--no-first-run', '--no-default-browser-check', '--disable-gpu', '--hide-scrollbars',
                          '--force-color-profile=srgb', '--lang=hu-HU', 'about:blank'],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(100):
        try:
            urllib.request.urlopen(f'http://127.0.0.1:{port}/json/version', timeout=1).read()
            break
        except Exception:
            time.sleep(0.2)
    return p, profil


def uj_lap(port):
    req = urllib.request.Request(f'http://127.0.0.1:{port}/json/new?about:blank', method='PUT')
    info = json.loads(urllib.request.urlopen(req, timeout=10).read())
    c = CDP(WS(info['webSocketDebuggerUrl']))
    c.hiv('Page.enable')
    c.hiv('Runtime.enable')
    return c


def emulal(c, w, h, mobil):
    c.hiv('Emulation.setDeviceMetricsOverride', width=w, height=h, deviceScaleFactor=1, mobile=mobil,
          screenWidth=w, screenHeight=h)
    c.hiv('Emulation.setTouchEmulationEnabled', enabled=mobil, maxTouchPoints=5)
    c.hiv('Emulation.setEmulatedMedia', features=[{'name': 'prefers-color-scheme', 'value': 'light'},
                                                  {'name': 'prefers-reduced-motion', 'value': 'reduce'}])


def nyit(c, url, var=1.5):
    c.esemenyek.clear()
    c.hiv('Page.navigate', url=url)
    c.var_esemeny('Page.loadEventFired', 60)
    time.sleep(var)


def kattint(c, selektor, mobil, var=1.8):
    """Valódi egér-/érintés-esemény az elem közepén (előbb a látómezőbe görgetve, ha kell)."""
    pont = c.js(f"""(() => {{ const dq = (s, gy = document) => {{ const e = gy.querySelector(s); if (e) return e; for (const h of gy.querySelectorAll('*')) {{ if (h.shadowRoot) {{ const t = dq(s, h.shadowRoot); if (t) return t; }} }} return null; }}; const e = dq({json.dumps(selektor)}); if (!e) return null;
        let r = e.getBoundingClientRect(); if (r.top < 60 || r.bottom > innerHeight - 20) {{ e.scrollIntoView({{block: 'center'}}); r = e.getBoundingClientRect(); }}
        return [r.left + Math.min(r.width / 2, 12), r.top + r.height / 2]; }})()""")
    if not pont:
        return False
    x, y = pont
    if mobil:
        c.hiv('Input.dispatchTouchEvent', type='touchStart', touchPoints=[{'x': x, 'y': y}])
        c.hiv('Input.dispatchTouchEvent', type='touchEnd', touchPoints=[])
    else:
        c.hiv('Input.dispatchMouseEvent', type='mouseMoved', x=x, y=y)
        c.hiv('Input.dispatchMouseEvent', type='mousePressed', x=x, y=y, button='left', clickCount=1)
        c.hiv('Input.dispatchMouseEvent', type='mouseReleased', x=x, y=y, button='left', clickCount=1)
    time.sleep(var)
    return True


def kep(c, ut):
    d = c.hiv('Page.captureScreenshot', format='png')
    Path(ut).write_bytes(base64.b64decode(d['data']))


def mer(c, sel):
    return c.js(MERO_JS + '(' + json.dumps(sel) + ')')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--chrome', required=True)
    ap.add_argument('--szerver', required=True)
    ap.add_argument('--pilot', required=True)
    ap.add_argument('--mockup', required=True)
    ap.add_argument('--ki', required=True)
    ap.add_argument('--json', required=True)
    ap.add_argument('--port', type=int, default=9333)
    a = ap.parse_args()
    os.makedirs(a.ki, exist_ok=True)
    S = a.szerver.rstrip('/')
    pilot_url = Path(a.pilot).resolve().as_uri()
    mockup_url = Path(a.mockup).resolve().as_uri()

    proc, profil = chrome_indit(a.chrome, a.port)
    eredmeny = {'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'szerver': S, 'jelenetek': []}
    try:
        c = uj_lap(a.port)
        # a szerver a kutatói szinten (süti), mint a 6. szakasz mérése
        emulal(c, 1280, 900, False)
        nyit(c, S + '/szint/kutato', 0.5)

        def jelenet(nev, url, sel, w, h, mobil, kattintas=None, elokattintas=None, teljes=False):
            emulal(c, w, h, mobil)
            nyit(c, url)
            if elokattintas:
                kattint(c, elokattintas, mobil)
            ok = True
            if kattintas:
                ok = kattint(c, kattintas, mobil)
            m = mer(c, sel)
            m.update({'jelenet': nev, 'szelesseg': w, 'url': url, 'kattintas': kattintas, 'kattintas_ok': ok})
            fajl = f'{nev}_{w}{"_telefon" if mobil else ""}.png'
            kep(c, os.path.join(a.ki, fajl))
            m['kep'] = fajl
            m['telefon'] = mobil
            eredmeny['jelenetek'].append(m)
            print(nev, w, 'tel' if mobil else '', 'ok:', ok, 'reszlet:', m.get('reszlet'), 'elsoVers:', (m.get('elsoVers') or {}).get('docTop'), 'tulf:', m['tulfolyas'])

        def sorozat(w, h, mobil):
            # --- szerver, 1Móz 1 (a pilot hatóköre és a 6. szakasz oldala)
            jelenet('szerver_1moz1_ures', S + '/1Moz/1', SZERVER_SEL, w, h, mobil)
            jelenet('szerver_1moz1_szo', S + '/1Moz/1', SZERVER_SEL, w, h, mobil,
                    kattintas='#v3 a.szo[data-strong="H0216"]')
            jelenet('szerver_1moz1_vers', S + '/1Moz/1', SZERVER_SEL, w, h, mobil, kattintas='#v3 a.versszam')
            jelenet('szerver_1moz1_il_szo', S + '/1Moz/1?reteg=il', SZERVER_SEL, w, h, mobil,
                    kattintas='#v3 a.er-fo[href*="szo=H0216"]')
            # --- szerver, Ez 37 (a mockup oldala)
            jelenet('szerver_ez37_ures', S + '/Ez/37', dict(SZERVER_SEL, celVers='#v12'), w, h, mobil)
            jelenet('szerver_ez37_vers', S + '/Ez/37', dict(SZERVER_SEL, celVers='#v12'), w, h, mobil,
                    kattintas='#v12 a.versszam')
            # --- #60 pilot, 1Móz 1:1–2:3
            jelenet('pilot_1moz1_ures', pilot_url, PILOT_SEL, w, h, mobil)
            jelenet('pilot_1moz1_szo', pilot_url, PILOT_SEL, w, h, mobil,
                    kattintas='#v-2 .ow[title*="H0216"]')
            jelenet('pilot_1moz1_vers', pilot_url, PILOT_SEL, w, h, mobil, kattintas='#v-2 .vszam')
            # --- mockup 9. változat (Ez 37)
            jelenet('mockup9_ez37_ures', mockup_url, MOCKUP_SEL, w, h, mobil)
            jelenet('mockup9_ez37_vers', mockup_url, MOCKUP_SEL, w, h, mobil, kattintas='#v12 a.versszam')

        # a fő táblázat: asztali böngésző emulált szélességen (a 6. szakasz módszere)
        for w, h, _ in SZELESSEGEK:
            sorozat(w, h, False)
        # telefon-emuláció (mobil nézetablak, érintés): 375 × 812
        sorozat(375, 812, True)
    finally:
        try:
            proc.terminate(); proc.wait(10)
        except Exception:
            pass
        shutil.rmtree(profil, ignore_errors=True)
    Path(a.json).write_text(json.dumps(eredmeny, ensure_ascii=False, indent=1), encoding='utf-8')
    print('kész:', a.json)


if __name__ == '__main__':
    main()
