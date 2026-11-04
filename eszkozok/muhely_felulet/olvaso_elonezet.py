#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F156: az olvasói Feed és Stash önálló előnézete (sima HTML-oldal, A. Olvasó arculat, mindig világos).

A `generalt/muhely/feed_nyilvanos.json` és `stash.json` adatából épül; csak előrehaladást mutat (DT-F156j):
állapotlánc, feldolgozott igehelyek, teljesült lépések, heti történés, a Stash leírása és statja. Piros kapu,
akadály, hibaszám, nyitott döntés nem szerepel. A kimenet az Artifact-oldal tartalma (a keretet a publikálás adja).

Használat: python eszkozok/muhely_felulet/olvaso_elonezet.py <kimeneti fájl.html>"""
import html
import json
import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

G = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'generalt', 'muhely')
e = html.escape

CSS = """
  /* Elrendezés: egy oszlop, fent az összegzés, alatta motívumkártyák és a Stash; mindig világos (A. Olvasó). */
  :root { color-scheme: light; --papir: #f6f6f3; --lap: #ffffff; --tinta: #1c1f24; --halvany: #5d636d; --vonal: #dcddd8;
          --kiemel: #1f5f7a; --kiemel-hatter: #e1eef3; --elfogad: #1d6b3f; --elfogad-hatter: #e0f0e6;
          --cim: "Source Serif 4", Georgia, serif; --szoveg: "IBM Plex Sans", system-ui, sans-serif;
          --adat: "IBM Plex Mono", ui-monospace, monospace; --sugar: 4px; }
  body { background: var(--papir); color: var(--tinta); font-family: var(--szoveg); line-height: 1.5;
         padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
         padding-block: 28px 56px; }
  .o { max-width: 62rem; margin-inline: auto; display: flex; flex-direction: column; gap: 28px; }
  h1 { font-family: var(--cim); font-weight: 600; font-size: 2.25rem; line-height: 1.12; letter-spacing: -0.01em; margin: 0;
       text-wrap: balance; }
  h2 { font-family: var(--cim); font-weight: 600; font-size: 1.4rem; margin: 0 0 10px; }
  h3 { font-size: 1.05rem; font-weight: 600; margin: 0; }
  p { margin: 0; }
  .al { color: var(--halvany); max-width: 60ch; margin-top: 8px; }
  .csempek { display: grid; grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); gap: 10px; }
  .csempe, .kartya { background: var(--lap); border: 1px solid var(--vonal); border-radius: var(--sugar); padding: 14px 16px; min-width: 0; }
  .csempe b { display: block; font-family: var(--cim); font-weight: 600; font-size: 2.2rem; line-height: 1.1;
              font-variant-numeric: tabular-nums; }
  .csempe span { color: var(--halvany); font-size: 0.85rem; }
  .kartyak { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 24rem), 1fr)); gap: 12px; }
  .kartya { display: flex; flex-direction: column; gap: 10px; }
  .kartya .fej { display: flex; justify-content: space-between; align-items: baseline; gap: 10px; flex-wrap: wrap; }
  .azon { font-family: var(--adat); font-size: 0.75rem; color: var(--halvany); }
  .lanc { display: flex; gap: 4px; flex-wrap: wrap; list-style: none; margin: 0; padding: 0; }
  .lanc li { font-size: 0.75rem; padding: 3px 10px; border-radius: 99px; border: 1px solid var(--vonal); color: var(--halvany); }
  .lanc li.kesz { background: var(--elfogad-hatter); border-color: transparent; color: var(--elfogad); }
  .lanc li.aktualis { background: var(--kiemel); border-color: var(--kiemel); color: var(--papir); font-weight: 600; }
  .mondat { font-size: 0.92rem; }
  .lepesek { margin: 0; padding: 0; list-style: none; display: flex; flex-direction: column; gap: 4px; font-size: 0.85rem; }
  .lepesek li::before { content: "✓"; color: var(--elfogad); margin-right: 8px; font-weight: 600; }
  .tab { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; font-size: 0.88rem; background: var(--lap); border: 1px solid var(--vonal); }
  th, td { text-align: left; padding: 8px 12px; border-bottom: 1px solid var(--vonal); vertical-align: top; }
  th { color: var(--halvany); font-weight: 500; font-size: 0.78rem; letter-spacing: 0.02em; }
  td.adat { font-family: var(--adat); font-variant-numeric: tabular-nums; }
  .ures { color: var(--halvany); }
  dl.leiras { margin: 0; display: grid; grid-template-columns: max-content 1fr; gap: 4px 14px; font-size: 0.85rem; }
  dl.leiras dt { color: var(--halvany); }
  dl.leiras dd { margin: 0; min-width: 0; overflow-wrap: anywhere; }
  footer { color: var(--halvany); font-size: 0.78rem; }
"""


def kartya(m):
    lanc = ''.join('<li class="%s">%s</li>' % (x['allapot'], e(x['nev'])) for x in m['lanc'])
    lepesek = ''.join('<li>%s</li>' % e(k['olvasoi_nev']) for k in m['teljesult_lepesek'])
    return ('<article class="kartya"><div class="fej"><h3>%s</h3><span class="azon">%s</span></div>'
            '<ul class="lanc" aria-label="Állapot">%s</ul><p class="mondat">%s</p>'
            '<ul class="lepesek" aria-label="Teljesült lépések">%s</ul></article>'
            % (e(m['cim']), e(m['id']), lanc, e(m['olvasoi_mondat']), lepesek))


def stash_kartya(x):
    """A Stash leírása és statja (DT-F156e: negatív kritérium és fölérendelt fogalom is)."""
    sor = [('Téma', x['tema']), ('PaRDeS-szint', x['pardes_szint']), ('Fölérendelt fogalom', x['folerendelt_fogalom']),
           ('Ide nem tartozik', x['negativ_kriterium']), ('Terjedelem', '%s szó' % x['terjedelem_szo']),
           ('Kötet', x['kotet_olvasoi'])]
    if x.get('kiadas_allapot'):  # DT-F156m: a kiadott lap a következő kiadás nyitott javítandóival is itt marad
        sor.insert(0, ('Kiadás', x['kiadas_allapot']))
    stat = '%s ószövetségi és %s újszövetségi hely, %s kapcsolat' % (x['elofordulas_osz'], x['elofordulas_usz'],
                                                                      x['kapcsolatok_db'])
    return ('<article class="kartya"><div class="fej"><h3>%s</h3><span class="azon">%s</span></div><p class="mondat">%s</p>'
            '<dl class="leiras">%s</dl></article>' % (e(x['cim']), e(x['id']), e(stat), ''.join(
                '<dt>%s</dt><dd>%s</dd>' % (e(k), e(str(v))) for k, v in sor)))


def main():
    ki = sys.argv[1]
    ny = json.load(open(os.path.join(G, 'feed_nyilvanos.json'), encoding='utf-8'))
    st = json.load(open(os.path.join(G, 'stash.json'), encoding='utf-8'))
    mots = ny['motivumok']
    o = ny['merok_osszesen']
    beepitett = sum(m['beepitett_jelolt_db'] for m in mots)
    elvetett = sum(m['elvetett_jelolt_db'] for m in mots)
    csempek = [(o['kesz_db'], 'motívum kész'), (o['kapu_zold'], 'teljesült ellenőrzési lépés'),
               (beepitett, 'igehely a motívumokban'), (elvetett, 'igehely kizárva, indoklással')]
    tortenes = ''.join('<tr><td class="adat">%s</td><td>%s</td><td>%s</td></tr>'
                       % (e(x['datum']), e(x['motivum']), e(x['olvasoi_esemeny'])) for x in ny['heti_tortenes'])
    tetelek = st['tetelek']
    if tetelek:
        stash = '<div class="kartyak">%s</div>' % ''.join(stash_kartya(x) for x in tetelek)
    else:
        stash = '<p class="ures">A kész motívumok leírása és számai itt jelennek meg.</p>'
    oldal = (
        '<title>Műhely előrehaladás</title><meta name="claude:viewport-fit-sides" content="cover">'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@400;600'
        '&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">'
        '<style>%s</style><div class="o"><header><h1>A motívumlexikon előrehaladása</h1>'
        '<p class="al">%d motívum, %d teljesült ellenőrzési lépés a %d-ből. „Kész” az a motívum, amelynél mind a kilenc '
        'ellenőrzési lépés teljesül, vagy amelynek lapja kiadást kapott.</p></header>'
        '<section class="csempek">%s</section>'
        '<section><h2>Hol tart az egyes motívum</h2><div class="kartyak">%s</div></section>'
        '<section><h2>Az elmúlt 7 nap</h2><div class="tab"><table><thead><tr><th>Dátum</th><th>Motívum</th><th>Mi történt'
        '</th></tr></thead><tbody>%s</tbody></table></div></section>'
        '<section><h2>Kész motívumok</h2>%s</section>'
        '<footer>Állapot: %s, verzió: %s. Generálta: eszkozok/muhely_felulet/olvaso_elonezet.py.</footer></div>'
        % (CSS, o['motivum_db'], o['kapu_zold'], o['kapu_ossz'],
           ''.join('<div class="csempe"><b>%s</b><span>%s</span></div>' % (n, e(s)) for n, s in csempek),
           ''.join(kartya(m) for m in mots), tortenes, stash, e(ny['generalva']), e(str(ny['commit']))))
    with open(ki, 'w', encoding='utf-8', newline='\n') as f:
        f.write(oldal)
    print('kész:', ki, len(oldal))


if __name__ == '__main__':
    main()
