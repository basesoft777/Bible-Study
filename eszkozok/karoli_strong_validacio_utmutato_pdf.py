#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""F175.V — az ellenőrök útmutatója PDF-ben (UTMUTATO.md -> UTMUTATO.pdf).

A Markdown-részhalmaz, amelyet az útmutató használ (címsor, bekezdés, felsorolás egy beágyazási szinttel,
számozott lista, táblázat, félkövér, dőlt, kód), egyszerű HTML-lé alakul (a héber és a görög a rendszerfontból;
a héber szakasz izolált jobbról balra futás, sortörés nélkül; a kötőjellel kezdődő toldalék nem törik el),
majd a Microsoft Edge vagy a Chrome fejléc nélküli nyomtatása PDF-et készít belőle. Külső csomag nem kell.

Használat (a repó gyökeréből):
    python eszkozok/karoli_strong_validacio_utmutato_pdf.py
"""

import html
import os
import re
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

GYOKER = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
VALIDACIO = os.path.join(GYOKER, 'kozlemeny', 'data_paper', 'validacio')
BONGESZOK = [r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
             r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
             r'C:\Program Files\Google\Chrome\Application\chrome.exe']

STILUS = """
@page { size: A4; margin: 16mm 15mm; }
body { font: 10.5pt/1.45 "Segoe UI", Arial, sans-serif; color: #1d1d1b; }
h1 { font-size: 16pt; margin: 0 0 8pt; } h2 { font-size: 12.5pt; margin: 14pt 0 5pt; } h3 { font-size: 11pt; }
p { margin: 5pt 0; } ul, ol { margin: 4pt 0 4pt 18pt; padding: 0; } li { margin: 2pt 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9.5pt; }
td, th { border: 1px solid #bbb; padding: 3pt 5pt; vertical-align: top; text-align: left; }
code { font-family: Consolas, monospace; font-size: 9.5pt; background: #f2f0ea; padding: 0 2pt; }
.heb { font-family: "SBL Hebrew", "Ezra SIL", "Times New Roman", "David", serif; font-size: 12pt;
       unicode-bidi: isolate; white-space: nowrap; }
.nw { white-space: nowrap; }
"""


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<b><i>\1</i></b>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<![\w*])\*([^*\n]+)\*(?![\w*])', r'<i>\1</i>', s)
    # kötőjellel kezdődő toldalék („-ban”, -ben): a kötőjel után nem törhet a sor (F175.V26)
    s = re.sub(r'(?<![\w-])(„?-\w+”?)', r'<span class="nw">\1</span>', s)
    s = re.sub(r'([\u0590-\u05FF][\u0590-\u05FF\u05BE\s]*[\u0590-\u05FF])', r'<span class="heb" dir="rtl">\1</span>', s)
    return s


def md_html(md):
    ki, lista, tabla_sorok = [], [], []

    def lista_zar():
        while lista:
            ki.append('</%s>' % lista.pop())

    def tabla_zar():
        if tabla_sorok:
            ki.append('<table>')
            for i, s in enumerate(tabla_sorok):
                if i == 1 and re.match(r'^\|[-|\s:]+\|$', s):
                    continue
                cellak = [c.strip() for c in s.strip('|').split('|')]
                tag = 'th' if i == 0 else 'td'
                ki.append('<tr>' + ''.join('<%s>%s</%s>' % (tag, inline(c), tag) for c in cellak) + '</tr>')
            ki.append('</table>')
            tabla_sorok.clear()

    for sor in md.split('\n'):
        if sor.startswith('|'):
            lista_zar()
            tabla_sorok.append(sor)
            continue
        tabla_zar()
        m = re.match(r'^(#{1,3}) (.*)$', sor)
        if m:
            lista_zar()
            n = len(m.group(1))
            ki.append('<h%d>%s</h%d>' % (n, inline(m.group(2)), n))
            continue
        m = re.match(r'^( *)([-*]|\d+\.) (.*)$', sor)
        if m:
            szint = len(m.group(1)) // 2 + 1
            tipus = 'ol' if m.group(2)[0].isdigit() else 'ul'
            while len(lista) > szint:
                ki.append('</%s>' % lista.pop())
            while len(lista) < szint:
                lista.append(tipus)
                ki.append('<%s>' % tipus)
            ki.append('<li>%s</li>' % inline(m.group(3)))
            continue
        if not sor.strip():
            lista_zar()
            continue
        if sor.strip() == '---':
            lista_zar()
            ki.append('<hr>')
            continue
        lista_zar()
        ki.append('<p>%s</p>' % inline(sor))
    lista_zar()
    tabla_zar()
    return '\n'.join(ki)


def main():
    md_ut = os.path.join(VALIDACIO, 'UTMUTATO.md')
    pdf_ut = os.path.join(VALIDACIO, 'UTMUTATO.pdf')
    with open(md_ut, encoding='utf-8') as f:
        md = f.read()
    oldal = ('<!doctype html><html lang="hu"><head><meta charset="utf-8"><title>Útmutató</title><style>%s</style>'
             '</head><body>%s</body></html>' % (STILUS, md_html(md)))
    bongeszo = next((b for b in BONGESZOK if os.path.exists(b)), None)
    if not bongeszo:
        raise SystemExit('nincs Edge vagy Chrome a PDF-hez')
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, 'utmutato.html')
        with open(h, 'w', encoding='utf-8') as f:
            f.write(oldal)
        subprocess.run([bongeszo, '--headless', '--disable-gpu', '--no-pdf-header-footer',
                        '--print-to-pdf=%s' % pdf_ut, 'file:///' + h.replace('\\', '/')],
                       check=True, capture_output=True, timeout=120)
    print('útmutató PDF: %s (%d bájt)' % (pdf_ut, os.path.getsize(pdf_ut)))


if __name__ == '__main__':
    main()
