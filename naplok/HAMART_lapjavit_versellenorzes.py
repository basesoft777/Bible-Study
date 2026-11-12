# -*- coding: utf-8 -*-
"""lap-javit HAMART-001 (egybeírás, 2026-11-11) — gépi versellenőrzés az értelmező rések új prózáján.

A kézi forrás (`motivumok/HAMART-001.md`) négy értelmező résének (kivonat, miert_fontos, ertelmezes, modszertan) minden
mondatából kigyűjti az igehely-hivatkozásokat, és mondatonként, versenként összeveti:
  (1) idézet: a „…” idézet, ha közvetlenül utána a vers áll, betűhíven (kis-nagybetű és írásjel nélkül) benne van-e a
      Károli-versben (`konkordancia/Karoli_1908.tsv`);
  (2) szójelenlét: a mondatban megnevezett héber/görög szó (a kiejtése vagy az írása szerint, `SZO`) Strong-száma
      a hivatkozott versek közül legalább egyben áll-e (`TAHOT_kivonat.tsv`, `TAGNT_kivonat.tsv`, kulcs: Károli-vers);
  (3) a vers léte: a hivatkozott vers megvan-e a Károli-szövegben.
A gépies rész eredménye a jelentés (`naplok/HAMART_lapjavit_versellenorzes.md`); a mondatonkénti versszöveg
(`--sonnet <tsv>`) a második kéz (Sonnet-subagent) bemenete: alany, szám, tartalom. TSV `split('\\t')`.
Futtatás a repó gyökeréből: python naplok/HAMART_lapjavit_versellenorzes.py [--sonnet <tsv>]"""
import io
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

FORRAS = 'motivumok/HAMART-001.md'
RESEK = ('kivonat', 'miert_fontos', 'ertelmezes', 'modszertan')
KONYVEK = ['1Móz', '5Móz', '1Kir', '2Kir', 'Jób', 'Zsolt', 'Ézs', 'Jer', 'Ez', 'Hós', 'Ámós', 'Mik', 'Hab', 'Sof', 'Mal',
           'Róm', 'Gal', 'Zsid', 'Jel', 'Ján', 'Jón']
SZO = {  # a prózában megnevezett szó → Strong-szám(ok)
    'árar': ['H0779'], 'adámá': ['H0127'], 'iccávón': ['H6093'], 'chattát': ['H2403'], 'chámász': ['H2555'],
    'sáchat': ['H7843'], 'erec': ['H0776'], 'qalal': ['H7043'], 'kéc': ['H7093'], 'málé': ['H4390'],
    'sámá': ['H8085'], 'álá': ['H0423'], 'epikataratosz': ['G1944'], 'katara': ['G2671'],
    'ftheiró': ['G5351', 'G1311', 'G2704'], 'diaftheiró': ['G1311'], 'fthora': ['G5356'], 'katathema': ['G2652'],
}
REF_RX = re.compile(r'(?:(%s) )?(\d+):(\d+)(?:-(\d+))?' % '|'.join(re.escape(k) for k in KONYVEK))


def tsv_vers(ut, mezo):
    d = {}
    for l in io.open(ut, encoding='utf-8'):
        p = l.rstrip('\n').split('\t')
        if len(p) > mezo:
            d.setdefault(p[0], []).append(p[mezo])
    return d


def norm(t):
    return re.sub(r'[^\wáéíóöőúüű ]', '', t.lower().replace('’', '')).split()


def resek_szovege():
    s = io.open(FORRAS, encoding='utf-8').read().replace('\r\n', '\n')
    ki = []
    for r in RESEK:
        t = s.split('<!-- RÉS-KEZDET: %s -->' % r)[1].split('<!-- RÉS-VÉGE: %s -->' % r)[0]
        for bek in t.split('\n'):
            if not bek.strip() or bek.startswith(('*Proveniencia', '<!--', '#')):
                continue
            for mondat in re.split(r'(?<=[.!?])\s+(?=[A-ZÁÉÍÓÖŐÚÜŰ„*(\d])', bek):
                ki.append((r, mondat.strip()))
    return ki


def hivatkozasok(mondat):
    ki, konyv = [], None
    for m in REF_RX.finditer(mondat):
        if m.group(1):
            konyv = m.group(1)
        if not konyv:
            continue
        f, a, b = int(m.group(2)), int(m.group(3)), int(m.group(4) or m.group(3))
        ki.append(('%s %d:%d' % (konyv, f, a), ['%s %d:%d' % (konyv, f, v) for v in range(a, b + 1)], m.start(), m.end()))
    return ki


def main():
    karoli = {k: v[0] for k, v in tsv_vers('konkordancia/Karoli_1908.tsv', 1).items()}
    strong = tsv_vers('konkordancia/TAHOT_kivonat.tsv', 1)
    for k, v in tsv_vers('konkordancia/TAGNT_kivonat.tsv', 1).items():
        strong.setdefault(k, []).extend(v)
    sorok, hibak, n_hiv = [], [], 0
    for res, mondat in resek_szovege():
        hiv = hivatkozasok(mondat)
        if not hiv:
            continue
        n_hiv += len(hiv)
        osszes_vers = [v for _, vv, _, _ in hiv for v in vv]
        for cim, versek, kezd, _veg in hiv:
            for v in versek:
                if v not in karoli:
                    hibak.append((res, mondat, cim, 'a vers nincs a Károli-szövegben'))
        # (1) az idézet a közvetlenül utána álló vers szövegében
        for m in re.finditer(r'„([^”]+)”[^„(]{0,40}\(([^)]*)\)', mondat):
            belso = [h for h in hivatkozasok(m.group(2))]
            if not belso:
                continue
            idezet = ' '.join(norm(m.group(1)))
            szoveg = ' '.join(norm(' '.join(karoli.get(v, '') for _, vv, _, _ in belso for v in vv)))
            if idezet and idezet not in szoveg:
                hibak.append((res, mondat, m.group(2), 'az idézet („%s”) nem betűhív a Károli-versben' % m.group(1)))
        # (2) a megnevezett szó a hivatkozott versek valamelyikében
        for szo, strongok in SZO.items():
            if re.search(r'\b%s\b' % re.escape(szo), mondat):
                if not any(s in strong.get(v, []) for v in osszes_vers for s in strongok):
                    hibak.append((res, mondat, ', '.join(h[0] for h in hiv),
                                  'a megnevezett szó (%s, %s) a hivatkozott versek egyikében sem áll' % (szo, '/'.join(strongok))))
        sorok.append((res, mondat, '; '.join(h[0] for h in hiv),
                       ' || '.join('%s: %s' % (v, karoli.get(v, '—')) for v in dict.fromkeys(osszes_vers))))
    return sorok, hibak, n_hiv


if __name__ == '__main__':
    sorok, hibak, n = main()
    print('mondat igehellyel: %d · hivatkozás: %d · gépi eltérés: %d' % (len(sorok), n, len(hibak)))
    for r, m, c, ok in hibak:
        print('- [%s] %s — %s :: %s' % (r, c, ok, m[:160]))
    if '--sonnet' in sys.argv:
        ut = sys.argv[sys.argv.index('--sonnet') + 1]
        with io.open(ut, 'w', encoding='utf-8', newline='') as f:
            f.write('\t'.join(['res', 'mondat', 'hivatkozas', 'karoli']) + '\n')
            for s in sorok:
                f.write('\t'.join(x.replace('\t', ' ') for x in s) + '\n')
